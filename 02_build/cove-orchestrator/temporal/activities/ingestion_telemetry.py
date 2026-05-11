"""Load-bearing telemetry for the v0.3 ingestion writer (AMP-302).

The pre-v0.3 pipeline logged ``pipeline_runs`` only at workflow completion
on a best-effort basis, which is why the live DB shows ``pipeline_runs=0``
and ``audit_log=0`` even though rows exist. Telemetry was designed but not
load-bearing.

This module is the contract:

* ``start_run`` inserts a ``pipeline_runs`` row at the moment a run begins.
  Status = ``running``.
* ``audit_batch`` writes one ``ingestion_audit_log`` row per batch.
* ``fail_run`` / ``finish_run`` close out the ``pipeline_runs`` row with a
  terminal status. Failure is a *status* not a missing row — a failed run
  still appears in the table.

If any of these telemetry writes fails, the caller is expected to surface
that as a workflow error. Telemetry is not optional.

Engineer B / AMP-302 / 2026-05-11
"""

from __future__ import annotations

import json
import logging
from datetime import datetime, timezone
from typing import Any, Optional, Protocol

logger = logging.getLogger("cove.ingestion.telemetry")


# ─── Status enum ────────────────────────────────────────────────────────────
RUN_STATUS_RUNNING = "running"
RUN_STATUS_COMPLETED = "completed"
RUN_STATUS_COMPLETED_NOOP = "completed_noop"
RUN_STATUS_FAILED_INGESTION = "failed_ingestion"
RUN_STATUS_FAILED_PUDDING = "failed_pudding"
RUN_STATUS_FAILED_MEMORY = "failed_memory"
RUN_STATUS_FAILED_TELEMETRY = "failed_telemetry"

TERMINAL_STATUSES = frozenset({
    RUN_STATUS_COMPLETED,
    RUN_STATUS_COMPLETED_NOOP,
    RUN_STATUS_FAILED_INGESTION,
    RUN_STATUS_FAILED_PUDDING,
    RUN_STATUS_FAILED_MEMORY,
    RUN_STATUS_FAILED_TELEMETRY,
})


# ─── DB protocol — tiny so tests can swap in a fake ─────────────────────────


class TelemetryConnection(Protocol):
    async def execute(self, query: str, *args: Any) -> Any: ...


# ─── pipeline_runs ──────────────────────────────────────────────────────────


_START_RUN_SQL = """
INSERT INTO pipeline_runs (run_id, started_at, status)
VALUES ($1, $2, $3)
ON CONFLICT (run_id) DO UPDATE
    SET started_at = LEAST(pipeline_runs.started_at, EXCLUDED.started_at)
"""

_FINISH_RUN_SQL = """
INSERT INTO pipeline_runs (
    run_id, started_at,
    ingestion_new_files, ingestion_total_unique, ingestion_elapsed,
    pudding_labelled, pudding_skipped, pudding_errors,
    memory_pg_vectors, memory_pg_entities, memory_errors,
    completed_at, status
) VALUES (
    $1, $2, $3, $4, $5, $6, $7, $8, $9, $10, $11, $12, $13
)
ON CONFLICT (run_id) DO UPDATE SET
    ingestion_new_files     = EXCLUDED.ingestion_new_files,
    ingestion_total_unique  = EXCLUDED.ingestion_total_unique,
    ingestion_elapsed       = EXCLUDED.ingestion_elapsed,
    pudding_labelled        = EXCLUDED.pudding_labelled,
    pudding_skipped         = EXCLUDED.pudding_skipped,
    pudding_errors          = EXCLUDED.pudding_errors,
    memory_pg_vectors       = EXCLUDED.memory_pg_vectors,
    memory_pg_entities      = EXCLUDED.memory_pg_entities,
    memory_errors           = EXCLUDED.memory_errors,
    completed_at            = EXCLUDED.completed_at,
    status                  = EXCLUDED.status
"""


async def start_run(conn: TelemetryConnection, run_id: str) -> datetime:
    """Insert the ``running`` row. Returns the started_at timestamp."""
    if not run_id:
        raise ValueError("run_id is required")
    started_at = datetime.now(timezone.utc)
    await conn.execute(_START_RUN_SQL, run_id, started_at, RUN_STATUS_RUNNING)
    logger.info("pipeline_runs start: run_id=%s started_at=%s", run_id, started_at.isoformat())
    return started_at


async def finish_run(
    conn: TelemetryConnection,
    *,
    run_id: str,
    started_at: datetime,
    status: str,
    ingestion_new_files: int = 0,
    ingestion_total_unique: int = 0,
    ingestion_elapsed: float = 0.0,
    pudding_labelled: int = 0,
    pudding_skipped: int = 0,
    pudding_errors: int = 0,
    memory_pg_vectors: int = 0,
    memory_pg_entities: int = 0,
    memory_errors: int = 0,
) -> None:
    """Close the run with a terminal status."""
    if status not in TERMINAL_STATUSES:
        raise ValueError(f"status must be terminal, got {status!r}")
    completed_at = datetime.now(timezone.utc)
    await conn.execute(
        _FINISH_RUN_SQL,
        run_id,
        started_at,
        ingestion_new_files,
        ingestion_total_unique,
        ingestion_elapsed,
        pudding_labelled,
        pudding_skipped,
        pudding_errors,
        memory_pg_vectors,
        memory_pg_entities,
        memory_errors,
        completed_at,
        status,
    )
    logger.info("pipeline_runs finish: run_id=%s status=%s", run_id, status)


async def fail_run(
    conn: TelemetryConnection,
    *,
    run_id: str,
    started_at: datetime,
    failure_stage: str,
    error: str,
) -> None:
    """Convenience wrapper: terminal failure status from a stage name."""
    status_map = {
        "ingestion":   RUN_STATUS_FAILED_INGESTION,
        "pudding":     RUN_STATUS_FAILED_PUDDING,
        "memory":      RUN_STATUS_FAILED_MEMORY,
        "memory_store": RUN_STATUS_FAILED_MEMORY,
        "telemetry":   RUN_STATUS_FAILED_TELEMETRY,
    }
    status = status_map.get(failure_stage, RUN_STATUS_FAILED_TELEMETRY)
    await finish_run(conn, run_id=run_id, started_at=started_at, status=status)
    # Audit row capturing the human-readable error message
    await audit_event(
        conn,
        run_id=run_id,
        event="run_failed",
        stage=failure_stage,
        details={"error": error[:2000]},
    )


# ─── ingestion_audit_log ────────────────────────────────────────────────────

_AUDIT_SQL = """
INSERT INTO ingestion_audit_log (
    run_id, event_at, event, stage,
    batch_index, batch_size, rows_written, rows_skipped, rows_failed, details
) VALUES ($1, $2, $3, $4, $5, $6, $7, $8, $9, $10::jsonb)
"""


async def audit_event(
    conn: TelemetryConnection,
    *,
    run_id: str,
    event: str,
    stage: Optional[str] = None,
    batch_index: Optional[int] = None,
    batch_size: Optional[int] = None,
    rows_written: Optional[int] = None,
    rows_skipped: Optional[int] = None,
    rows_failed: Optional[int] = None,
    details: Optional[dict[str, Any]] = None,
) -> None:
    """Write one ``ingestion_audit_log`` row.

    ``event`` is free text — common values are ``run_start``, ``run_end``,
    ``batch_start``, ``batch_end``, ``row_failed``, ``run_failed``.
    """
    if not run_id:
        raise ValueError("run_id is required")
    if not event:
        raise ValueError("event is required")
    await conn.execute(
        _AUDIT_SQL,
        run_id,
        datetime.now(timezone.utc),
        event,
        stage,
        batch_index,
        batch_size,
        rows_written,
        rows_skipped,
        rows_failed,
        json.dumps(details or {}),
    )


async def audit_batch(
    conn: TelemetryConnection,
    *,
    run_id: str,
    stage: str,
    batch_index: int,
    batch_size: int,
    rows_written: int,
    rows_skipped: int = 0,
    rows_failed: int = 0,
    details: Optional[dict[str, Any]] = None,
) -> None:
    """Shorthand for the common batch-completion audit event."""
    await audit_event(
        conn,
        run_id=run_id,
        event="batch_end",
        stage=stage,
        batch_index=batch_index,
        batch_size=batch_size,
        rows_written=rows_written,
        rows_skipped=rows_skipped,
        rows_failed=rows_failed,
        details=details,
    )


__all__ = [
    "RUN_STATUS_RUNNING",
    "RUN_STATUS_COMPLETED",
    "RUN_STATUS_COMPLETED_NOOP",
    "RUN_STATUS_FAILED_INGESTION",
    "RUN_STATUS_FAILED_PUDDING",
    "RUN_STATUS_FAILED_MEMORY",
    "RUN_STATUS_FAILED_TELEMETRY",
    "TERMINAL_STATUSES",
    "TelemetryConnection",
    "start_run",
    "finish_run",
    "fail_run",
    "audit_event",
    "audit_batch",
]

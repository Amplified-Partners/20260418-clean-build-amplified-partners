"""Tests for the load-bearing ingestion telemetry contract (AMP-302).

Pre-v0.3 the workflow only logged ``pipeline_runs`` once at the end on a
best-effort basis (``except: warning``), which is why the live DB shows
``pipeline_runs=0``. These tests pin the new contract:

* ``start_run`` writes a row with status=running at the start.
* Failure paths still produce a terminal row — failure is a *status*,
  not a missing row.
* Each batch produces an ``ingestion_audit_log`` row.
* Status values are restricted to the documented enum.
"""

from __future__ import annotations

import json
from datetime import datetime, timezone
from typing import Any

import pytest

from temporal.activities import ingestion_telemetry as tlm


class FakeConnection:
    def __init__(self) -> None:
        self.calls: list[tuple[str, tuple[Any, ...]]] = []
        # crude in-memory stand-in for pipeline_runs and ingestion_audit_log
        self.pipeline_runs: dict[str, dict[str, Any]] = {}
        self.audit_log: list[dict[str, Any]] = []

    async def execute(self, query: str, *args: Any) -> None:
        self.calls.append((query, args))
        if "INSERT INTO pipeline_runs" in query and "completed_at" not in query:
            # start_run shape
            run_id, started_at, status = args
            existing = self.pipeline_runs.get(run_id)
            if existing:
                existing["started_at"] = min(existing["started_at"], started_at)
            else:
                self.pipeline_runs[run_id] = {
                    "run_id": run_id, "started_at": started_at, "status": status,
                }
        elif "INSERT INTO pipeline_runs" in query and "completed_at" in query:
            (run_id, started_at, inf, itu, ie, pl, ps, pe,
             mv, men, merr, completed_at, status) = args
            self.pipeline_runs[run_id] = {
                "run_id": run_id, "started_at": started_at,
                "ingestion_new_files": inf, "ingestion_total_unique": itu,
                "ingestion_elapsed": ie,
                "pudding_labelled": pl, "pudding_skipped": ps, "pudding_errors": pe,
                "memory_pg_vectors": mv, "memory_pg_entities": men, "memory_errors": merr,
                "completed_at": completed_at, "status": status,
            }
        elif "INSERT INTO ingestion_audit_log" in query:
            (run_id, event_at, event, stage, batch_index, batch_size,
             rows_written, rows_skipped, rows_failed, details) = args
            self.audit_log.append({
                "run_id": run_id, "event_at": event_at, "event": event,
                "stage": stage, "batch_index": batch_index, "batch_size": batch_size,
                "rows_written": rows_written, "rows_skipped": rows_skipped,
                "rows_failed": rows_failed,
                "details": json.loads(details) if isinstance(details, str) else details,
            })


# ─── start_run ──────────────────────────────────────────────────────────────


@pytest.mark.asyncio
async def test_start_run_writes_running_row() -> None:
    conn = FakeConnection()
    started = await tlm.start_run(conn, "run-1")
    assert "run-1" in conn.pipeline_runs
    assert conn.pipeline_runs["run-1"]["status"] == tlm.RUN_STATUS_RUNNING
    assert isinstance(started, datetime)


@pytest.mark.asyncio
async def test_start_run_rejects_empty_id() -> None:
    conn = FakeConnection()
    with pytest.raises(ValueError):
        await tlm.start_run(conn, "")


# ─── finish_run / fail_run ──────────────────────────────────────────────────


@pytest.mark.asyncio
async def test_finish_run_writes_terminal_status() -> None:
    conn = FakeConnection()
    started = await tlm.start_run(conn, "run-2")
    await tlm.finish_run(
        conn,
        run_id="run-2",
        started_at=started,
        status=tlm.RUN_STATUS_COMPLETED,
        ingestion_new_files=10,
        memory_pg_vectors=50,
    )
    row = conn.pipeline_runs["run-2"]
    assert row["status"] == tlm.RUN_STATUS_COMPLETED
    assert row["ingestion_new_files"] == 10
    assert row["memory_pg_vectors"] == 50
    assert row["completed_at"] is not None


@pytest.mark.asyncio
async def test_finish_run_rejects_non_terminal_status() -> None:
    conn = FakeConnection()
    started = datetime.now(timezone.utc)
    with pytest.raises(ValueError):
        await tlm.finish_run(
            conn, run_id="run-x", started_at=started, status="running",
        )


@pytest.mark.asyncio
async def test_fail_run_still_produces_row_and_audit() -> None:
    """A failure run is a *status*, not a missing row.

    This is the headline regression we're preventing: pre-v0.3 a failure
    in the workflow would skip the log step and leave pipeline_runs empty.
    """
    conn = FakeConnection()
    started = await tlm.start_run(conn, "run-fail")
    await tlm.fail_run(
        conn,
        run_id="run-fail",
        started_at=started,
        failure_stage="memory",
        error="connection refused",
    )
    assert conn.pipeline_runs["run-fail"]["status"] == tlm.RUN_STATUS_FAILED_MEMORY
    # an audit row was written
    audit = [a for a in conn.audit_log if a["event"] == "run_failed"]
    assert len(audit) == 1
    assert audit[0]["details"]["error"] == "connection refused"


@pytest.mark.asyncio
async def test_fail_run_maps_known_stages_to_status_enum() -> None:
    conn = FakeConnection()
    started = datetime.now(timezone.utc)
    for stage, expected in [
        ("ingestion", tlm.RUN_STATUS_FAILED_INGESTION),
        ("pudding", tlm.RUN_STATUS_FAILED_PUDDING),
        ("memory", tlm.RUN_STATUS_FAILED_MEMORY),
        ("memory_store", tlm.RUN_STATUS_FAILED_MEMORY),
        ("telemetry", tlm.RUN_STATUS_FAILED_TELEMETRY),
    ]:
        run_id = f"run-{stage}"
        await tlm.start_run(conn, run_id)
        await tlm.fail_run(
            conn, run_id=run_id, started_at=started,
            failure_stage=stage, error="x",
        )
        assert conn.pipeline_runs[run_id]["status"] == expected


# ─── audit_batch ────────────────────────────────────────────────────────────


@pytest.mark.asyncio
async def test_audit_batch_writes_row() -> None:
    conn = FakeConnection()
    await tlm.audit_batch(
        conn,
        run_id="run-3",
        stage="memory_store",
        batch_index=0,
        batch_size=100,
        rows_written=98,
        rows_skipped=1,
        rows_failed=1,
        details={"note": "first batch"},
    )
    assert len(conn.audit_log) == 1
    row = conn.audit_log[0]
    assert row["event"] == "batch_end"
    assert row["stage"] == "memory_store"
    assert row["rows_written"] == 98
    assert row["details"] == {"note": "first batch"}


@pytest.mark.asyncio
async def test_audit_event_requires_run_id_and_event() -> None:
    conn = FakeConnection()
    with pytest.raises(ValueError):
        await tlm.audit_event(conn, run_id="", event="x")
    with pytest.raises(ValueError):
        await tlm.audit_event(conn, run_id="r", event="")


# ─── Terminal status enum stays load-bearing ───────────────────────────────


def test_terminal_statuses_documented() -> None:
    """Tests pin the enum so a silent rename in code breaks here."""
    expected = {
        "completed", "completed_noop",
        "failed_ingestion", "failed_pudding", "failed_memory", "failed_telemetry",
    }
    assert tlm.TERMINAL_STATUSES == expected

"""Database connection helpers and active current-model retrieval.

Connects as brain_writer for writes, brain_reader for reads.
All connections target the amplified_brain database on Beast.

Signed-by: Devon-d493 | 2026-05-19 | devin-d49302e4179d43d0892997a7f3a9f57f
"""

from __future__ import annotations

import logging
import os
from typing import Any

log = logging.getLogger("brain_curator.db")

# ---------------------------------------------------------------------------
# DSN — required via environment variable. No default credentials.
# On Beast these are set in the cove-orchestrator Docker env.
# ---------------------------------------------------------------------------

BRAIN_WRITER_DSN = os.environ.get("BRAIN_WRITER_DSN", "")
BRAIN_READER_DSN = os.environ.get("BRAIN_READER_DSN", "")


async def connect_writer() -> Any:
    """Connect as brain_writer (INSERT/UPDATE/DELETE on curation tables)."""
    import asyncpg

    if not BRAIN_WRITER_DSN:
        raise RuntimeError("BRAIN_WRITER_DSN environment variable not set")
    return await asyncpg.connect(BRAIN_WRITER_DSN)


async def connect_reader() -> Any:
    """Connect as brain_reader (SELECT only)."""
    import asyncpg

    if not BRAIN_READER_DSN:
        raise RuntimeError("BRAIN_READER_DSN environment variable not set")
    return await asyncpg.connect(BRAIN_READER_DSN)


# ---------------------------------------------------------------------------
# Active current-model retrieval query
# ---------------------------------------------------------------------------

ACTIVE_CURRENT_MODEL_QUERY = """\
SELECT bp.*
FROM brain_packets bp
WHERE bp.packet_type IN ('working_model', 'decision', 'method', 'doctrine')
  AND bp.status = 'active'
  AND bp.route IN ('keep', 'freeze')
  AND bp.epistemic_tier IN ('STRUCTURED', 'MEASURED', 'PROVEN')
  AND (bp.valid_from IS NULL OR bp.valid_from <= now())
  AND (bp.valid_to IS NULL OR bp.valid_to > now())
ORDER BY bp.last_verified_at DESC NULLS LAST, bp.updated_at DESC
LIMIT $1
"""

EVIDENCE_FOR_PACKETS_QUERY = """\
SELECT bpe.packet_id, bpe.chunk_id, bpe.evidence_role, bpe.confidence,
       kv.content, kv.file_path, kv.metadata
FROM brain_packet_evidence bpe
JOIN knowledge_vectors kv ON kv.id = bpe.chunk_id
WHERE bpe.packet_id = ANY($1::uuid[])
ORDER BY bpe.packet_id, bpe.confidence DESC
"""


async def fetch_active_current_model(
    limit: int = 20,
) -> list[dict[str, Any]]:
    """Retrieve active governed packets with evidence from knowledge_vectors.

    Returns packets with epistemic tier >= STRUCTURED, active status,
    and keep/freeze route. INTUITED packets are excluded by design —
    they must not reach default agent retrieval.
    """
    conn = await connect_reader()
    try:
        packets = await conn.fetch(ACTIVE_CURRENT_MODEL_QUERY, limit)
        if not packets:
            return []

        packet_ids = [row["packet_id"] for row in packets]
        evidence_rows = await conn.fetch(EVIDENCE_FOR_PACKETS_QUERY, packet_ids)

        evidence_by_packet: dict[str, list[dict[str, Any]]] = {}
        for row in evidence_rows:
            pid = str(row["packet_id"])
            evidence_by_packet.setdefault(pid, []).append(dict(row))

        result = []
        for p in packets:
            entry = dict(p)
            entry["evidence"] = evidence_by_packet.get(str(p["packet_id"]), [])
            result.append(entry)

        return result
    finally:
        await conn.close()


# ---------------------------------------------------------------------------
# Curation run helpers
# ---------------------------------------------------------------------------


async def start_curation_run(
    conn: Any,
    run_id: str,
    stage: str,
    code_version: str | None = None,
    config_hash: str | None = None,
    input_scope: dict[str, Any] | None = None,
) -> None:
    """Record the start of a curation stage run."""
    import json

    from brain_curator.config import CODE_VERSION

    _version = code_version or CODE_VERSION
    await conn.execute(
        """INSERT INTO brain_curation_runs
           (run_id, stage, code_version, config_hash, input_scope, status)
        VALUES ($1, $2, $3, $4, $5::jsonb, 'running')
        ON CONFLICT (run_id) DO UPDATE SET status = 'running', started_at = now()""",
        run_id,
        stage,
        _version,
        config_hash,
        json.dumps(input_scope or {}),
    )


async def complete_curation_run(
    conn: Any,
    run_id: str,
    status: str = "completed",
    metrics: dict[str, Any] | None = None,
    error: str | None = None,
) -> None:
    """Record the completion of a curation stage run."""
    import json

    await conn.execute(
        """UPDATE brain_curation_runs
        SET completed_at = now(), status = $2, metrics = $3::jsonb, error = $4
        WHERE run_id = $1""",
        run_id,
        status,
        json.dumps(metrics or {}),
        error,
    )

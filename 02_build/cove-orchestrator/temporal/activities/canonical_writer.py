"""Canonical writer — manifest → Postgres index.

AMP-302 Ticket 3: The single write path into canonical amplified_brain.
Reads a JSONL manifest, inserts into knowledge_vectors with full provenance.
Records pipeline_runs and audit_log entries.

Contract:
- Only brain_writer_pipeline role writes
- Every row joins to a manifest line
- Idempotent (ON CONFLICT DO UPDATE)
- No DELETE, no inline entity/relationship mutation
- Deterministic IDs: UUID5(namespace, file_hash + ':' + chunk_index)

Pipeline position: after manifest generation, before derived rebuild.

Signed-by: Devon-0de2 | 2026-05-11 | devin-0de27df281514f96ba3921354d7c31ae
"""

from __future__ import annotations

import json
import logging
import os
import uuid as _uuid
from dataclasses import dataclass
from datetime import datetime, timezone
from pathlib import Path

from temporalio import activity

logger = logging.getLogger("cove.canonical_writer")

PIPELINE_VERSION = "amplified-pipeline-v0.3"
PROVENANCE = "amplified-pipeline-v0.3"
SIGNED_BY = "brain_writer_pipeline"

BRAIN_DSN = os.getenv(
    "BRAIN_DSN",
    "postgresql://brain_writer@cove-postgres:5432/amplified_brain",
)

# Stable namespace for UUID5 generation
NAMESPACE_INGESTION = _uuid.UUID("a1b2c3d4-e5f6-7890-abcd-ef1234567890")


# ═══════════════════════════════════════════════════════════════════════
# Data classes
# ═══════════════════════════════════════════════════════════════════════

@dataclass
class CanonicalWriterInput:
    """Input for the canonical writer activity."""
    run_id: str
    manifest_path: str
    manifest_hash: str
    brain_dsn: str = BRAIN_DSN
    batch_size: int = 100
    dry_run: bool = False


@dataclass
class CanonicalWriterResult:
    """Result from the canonical writer activity."""
    success: bool
    rows_written: int = 0
    rows_skipped: int = 0
    files_processed: int = 0
    errors: int = 0
    dry_run: bool = False
    error: str | None = None


# ═══════════════════════════════════════════════════════════════════════
# Helpers
# ═══════════════════════════════════════════════════════════════════════

def deterministic_id(file_hash: str, chunk_index: int) -> _uuid.UUID:
    """UUID5 from file_hash + chunk_index. Same input → same UUID."""
    name = f"{file_hash}:{chunk_index}"
    return _uuid.uuid5(NAMESPACE_INGESTION, name)


def read_file_content_for_chunk(
    file_path: str, line_start: int, line_end: int
) -> str:
    """Read the specific line range from the source file."""
    try:
        with open(file_path, "r", encoding="utf-8", errors="ignore") as f:
            lines = f.readlines()
        selected = lines[line_start - 1 : line_end]
        return "".join(selected)
    except (OSError, IndexError) as e:
        logger.warning(f"Cannot read lines {line_start}-{line_end} from {file_path}: {e}")
        return ""


# ═══════════════════════════════════════════════════════════════════════
# Temporal activity
# ═══════════════════════════════════════════════════════════════════════

@activity.defn(name="write_canonical_vectors")
async def write_canonical_vectors(input: CanonicalWriterInput) -> CanonicalWriterResult:
    """Read JSONL manifest, insert canonical knowledge_vectors rows.

    Every row gets full provenance metadata. IDs are deterministic so
    reruns are idempotent.
    """
    import asyncpg

    manifest_path = Path(input.manifest_path)
    if not manifest_path.exists():
        return CanonicalWriterResult(
            success=False,
            error=f"Manifest not found: {manifest_path}",
        )

    # Parse manifest
    manifest_lines: list[dict] = []
    for raw_line in manifest_path.read_text(encoding="utf-8").strip().split("\n"):
        if raw_line.strip():
            manifest_lines.append(json.loads(raw_line))

    activity.logger.info(
        f"Canonical writer: {len(manifest_lines)} files from {manifest_path.name}"
    )

    total_chunks = sum(len(ml.get("chunks", [])) for ml in manifest_lines)

    if input.dry_run:
        activity.logger.info(
            f"DRY RUN: would write {total_chunks} rows from "
            f"{len(manifest_lines)} files"
        )
        return CanonicalWriterResult(
            success=True,
            rows_written=total_chunks,
            files_processed=len(manifest_lines),
            dry_run=True,
        )

    # Connect
    try:
        conn = await asyncpg.connect(input.brain_dsn)
    except Exception as e:
        return CanonicalWriterResult(
            success=False,
            error=f"PostgreSQL connection failed: {e}",
        )

    rows_written = 0
    rows_skipped = 0
    errors = 0
    now_iso = datetime.now(timezone.utc).isoformat()

    try:
        # Record pipeline run start
        await conn.execute(
            """INSERT INTO pipeline_runs
               (run_id, started_at, status)
            VALUES ($1, $2, 'writing')
            ON CONFLICT (run_id) DO UPDATE SET status = 'writing'""",
            input.run_id,
            now_iso,
        )

        # Record manifest in ingestion_manifests
        await conn.execute(
            """INSERT INTO ingestion_manifests
               (run_id, source_root, file_count, chunk_count,
                manifest_hash, manifest_path, signed_by)
            VALUES ($1, $2, $3, $4, $5, $6, $7)
            ON CONFLICT (run_id) DO UPDATE SET
               manifest_hash = EXCLUDED.manifest_hash""",
            input.run_id,
            manifest_lines[0].get("source_root", "") if manifest_lines else "",
            len(manifest_lines),
            total_chunks,
            input.manifest_hash,
            str(manifest_path),
            SIGNED_BY,
        )

        # Process manifest lines in batches
        for i in range(0, len(manifest_lines), input.batch_size):
            batch = manifest_lines[i : i + input.batch_size]

            for ml in batch:
                file_path = ml["file_path"]
                file_hash = ml["file_hash"]

                for chunk in ml.get("chunks", []):
                    try:
                        chunk_idx = chunk["idx"]
                        row_id = deterministic_id(file_hash, chunk_idx)

                        content = read_file_content_for_chunk(
                            file_path,
                            chunk["line_start"],
                            chunk["line_end"],
                        )

                        if not content.strip():
                            rows_skipped += 1
                            continue

                        metadata = json.dumps({
                            "chunk_type": chunk.get("chunk_type", "prose"),
                            "parent_heading": chunk.get("parent_heading", ""),
                        })

                        await conn.execute(
                            """INSERT INTO knowledge_vectors
                               (id, content, source, source_type, metadata,
                                provenance, pipeline_version, run_id,
                                file_path, file_hash, chunk_hash, chunk_index,
                                line_start, line_end, parent_heading,
                                prev_hash, next_hash, signed_by, ingested_at)
                            VALUES ($1,$2,$3,$4,$5::jsonb,
                                    $6,$7,$8,
                                    $9,$10,$11,$12,
                                    $13,$14,$15,
                                    $16,$17,$18,now())
                            ON CONFLICT (id) DO UPDATE SET
                               content = EXCLUDED.content,
                               metadata = EXCLUDED.metadata,
                               chunk_hash = EXCLUDED.chunk_hash,
                               updated_at = now()""",
                            row_id,
                            content[:4000],
                            file_path,
                            "document",
                            metadata,
                            PROVENANCE,
                            PIPELINE_VERSION,
                            input.run_id,
                            file_path,
                            file_hash,
                            chunk["chunk_hash"],
                            chunk_idx,
                            chunk.get("line_start"),
                            chunk.get("line_end"),
                            chunk.get("parent_heading", ""),
                            chunk.get("prev_hash"),
                            chunk.get("next_hash"),
                            SIGNED_BY,
                        )
                        rows_written += 1

                    except Exception as e:
                        errors += 1
                        activity.logger.warning(
                            f"Write failed for {file_path} chunk {chunk.get('idx')}: {e}"
                        )

            activity.logger.info(
                f"Batch {i // input.batch_size + 1}: "
                f"written={rows_written}, skipped={rows_skipped}, errors={errors}"
            )

        # Audit log entry
        await conn.execute(
            """INSERT INTO audit_log
               (actor, action, resource_type, resource_id, details)
            VALUES ($1, $2, $3, $4, $5::jsonb)""",
            SIGNED_BY,
            "ingestion.canonical_write",
            "pipeline_run",
            input.run_id,
            json.dumps({
                "rows_written": rows_written,
                "rows_skipped": rows_skipped,
                "errors": errors,
                "manifest_hash": input.manifest_hash,
                "files_processed": len(manifest_lines),
            }),
        )

        # Update pipeline run status
        final_status = "completed" if errors == 0 else "completed_with_errors"
        await conn.execute(
            """UPDATE pipeline_runs
               SET completed_at = $1,
                   status = $2,
                   memory_pg_vectors = $3,
                   memory_errors = $4
               WHERE run_id = $5""",
            datetime.now(timezone.utc).isoformat(),
            final_status,
            rows_written,
            errors,
            input.run_id,
        )

    finally:
        await conn.close()

    activity.logger.info(
        f"Canonical write complete: {rows_written} written, "
        f"{rows_skipped} skipped, {errors} errors"
    )

    return CanonicalWriterResult(
        success=errors == 0,
        rows_written=rows_written,
        rows_skipped=rows_skipped,
        files_processed=len(manifest_lines),
        errors=errors,
        error=f"{errors} write failures" if errors else None,
    )

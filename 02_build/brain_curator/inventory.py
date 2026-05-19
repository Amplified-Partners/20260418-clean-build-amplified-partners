"""01_inventory — backfill brain_documents from existing knowledge_vectors.

Groups chunks by file_path, extracts document-level metadata from the
first chunk's frontmatter, and writes to brain_documents.

Does NOT modify knowledge_vectors.content — read-only access to source.

Signed-by: Devon-d493 | 2026-05-19 | devin-d49302e4179d43d0892997a7f3a9f57f
"""

from __future__ import annotations

import json
import logging
import uuid
from typing import Any

from brain_curator.config import CODE_VERSION, PIPELINE_PROVENANCE
from brain_curator.db import complete_curation_run, connect_writer, start_curation_run

log = logging.getLogger("brain_curator.inventory")


async def backfill_documents(
    run_id: str,
    provenance_filter: str = PIPELINE_PROVENANCE,
) -> dict[str, Any]:
    """Read knowledge_vectors, group by file_path, write brain_documents.

    Returns metrics dict with counts.
    """
    conn = await connect_writer()
    try:
        await start_curation_run(
            conn,
            run_id=run_id,
            stage="inventory",
            code_version=CODE_VERSION,
            input_scope={"provenance_filter": provenance_filter},
        )

        # Group chunks by file_path — read-only query against knowledge_vectors
        rows = await conn.fetch(
            """
            SELECT file_path,
                   file_hash,
                   COUNT(*) AS chunk_count,
                   MIN(metadata) AS first_metadata,
                   MIN(ingested_at) AS earliest_ingested,
                   MIN(created_at) AS earliest_created
            FROM knowledge_vectors
            WHERE provenance = $1
            GROUP BY file_path, file_hash
            ORDER BY file_path
            """,
            provenance_filter,
        )

        documents_created = 0
        documents_skipped = 0

        for row in rows:
            file_path = row["file_path"]
            file_hash = row["file_hash"]

            # Skip if already inventoried
            existing = await conn.fetchval(
                """SELECT 1 FROM brain_documents
                WHERE source_path = $1 AND file_hash_sha256 = $2
                LIMIT 1""",
                file_path,
                file_hash,
            )
            if existing:
                documents_skipped += 1
                continue

            # Extract metadata from first chunk
            meta_raw = row["first_metadata"]
            fm_metadata: dict[str, Any] = {}
            raw_frontmatter: dict[str, Any] = {}
            title: str | None = None
            document_type: str | None = None

            if meta_raw:
                if isinstance(meta_raw, str):
                    try:
                        fm_metadata = json.loads(meta_raw)
                    except (json.JSONDecodeError, TypeError):
                        fm_metadata = {}
                elif isinstance(meta_raw, dict):
                    fm_metadata = meta_raw

                raw_frontmatter = fm_metadata.get("frontmatter", {})
                if isinstance(raw_frontmatter, str):
                    try:
                        raw_frontmatter = json.loads(raw_frontmatter)
                    except (json.JSONDecodeError, TypeError):
                        raw_frontmatter = {}
                title = (
                    raw_frontmatter.get("title")
                    or fm_metadata.get("title")
                    or _title_from_path(file_path)
                )
                document_type = (
                    fm_metadata.get("document_type")
                    or fm_metadata.get("type")
                    or _infer_document_type(file_path, fm_metadata)
                )

            doc_id = uuid.uuid4()
            await conn.execute(
                """INSERT INTO brain_documents
                   (document_id, source_path, source_system, file_hash_sha256,
                    raw_frontmatter, fm_metadata, title, document_type,
                    ingested_at, pipeline_version, chunk_count, status)
                VALUES ($1, $2, $3, $4, $5::jsonb, $6::jsonb, $7, $8, $9, $10, $11, 'inventoried')
                ON CONFLICT DO NOTHING""",
                doc_id,
                file_path,
                provenance_filter,
                file_hash,
                json.dumps(raw_frontmatter),
                json.dumps(fm_metadata),
                title,
                document_type,
                row["earliest_ingested"],
                provenance_filter,
                row["chunk_count"],
            )
            documents_created += 1

        metrics = {
            "source_groups": len(rows),
            "documents_created": documents_created,
            "documents_skipped": documents_skipped,
        }
        await complete_curation_run(conn, run_id, status="completed", metrics=metrics)
        log.info("Inventory complete: %s", metrics)
        return metrics

    except Exception as e:
        await complete_curation_run(
            conn, run_id, status="failed", error=str(e)
        )
        raise
    finally:
        await conn.close()


def _title_from_path(file_path: str) -> str | None:
    """Extract a title from the file path stem."""
    if not file_path:
        return None
    parts = file_path.rsplit("/", 1)
    name = parts[-1] if len(parts) > 1 else parts[0]
    if name.endswith(".md"):
        name = name[:-3]
    return name.replace("-", " ").replace("_", " ").strip() or None


def _infer_document_type(
    file_path: str, metadata: dict[str, Any]
) -> str | None:
    """Heuristic document type from path patterns."""
    path_lower = file_path.lower()
    if "decision" in path_lower:
        return "decision"
    if "method" in path_lower or "process" in path_lower:
        return "method"
    if "doctrine" in path_lower or "principle" in path_lower:
        return "doctrine"
    if "failure" in path_lower or "post-mortem" in path_lower:
        return "failure"
    if "prompt" in path_lower:
        return "prompt_pattern"
    if "conversation" in path_lower or "thread" in path_lower:
        return "conversation"
    return "reference"

"""02_version_families — exact and metadata-based version family detection.

Identifies duplicate and version-family relationships among documents
without modifying any source content.

Canonical selection: best provenance > most complete frontmatter >
highest quality gate status > most recent (if current-working-model) >
earliest (if source-history).

Signed-by: Devon-d493 | 2026-05-19 | devin-d49302e4179d43d0892997a7f3a9f57f
"""

from __future__ import annotations

import json
import logging
import uuid
from typing import Any

from brain_curator.config import CODE_VERSION
from brain_curator.db import complete_curation_run, connect_writer, start_curation_run

log = logging.getLogger("brain_curator.version_families")


async def detect_version_families(run_id: str) -> dict[str, Any]:
    """Detect exact duplicates and metadata-based version families.

    Writes clusters to brain_dedupe_clusters and members to
    brain_dedupe_members.
    """
    conn = await connect_writer()
    try:
        await start_curation_run(
            conn, run_id=run_id, stage="version_families", code_version=CODE_VERSION
        )

        exact_clusters = await _detect_exact_families(conn)
        metadata_clusters = await _detect_metadata_families(conn)

        metrics = {
            "exact_clusters": exact_clusters,
            "metadata_clusters": metadata_clusters,
        }
        await complete_curation_run(conn, run_id, status="completed", metrics=metrics)
        log.info("Version families complete: %s", metrics)
        return metrics

    except Exception as e:
        await complete_curation_run(conn, run_id, status="failed", error=str(e))
        raise
    finally:
        await conn.close()


async def _detect_exact_families(conn: Any) -> int:
    """Group documents by file_hash_sha256 — exact content duplicates."""
    groups = await conn.fetch(
        """
        SELECT file_hash_sha256, array_agg(document_id) AS doc_ids
        FROM brain_documents
        GROUP BY file_hash_sha256
        HAVING COUNT(*) > 1
        """
    )

    clusters_created = 0
    for group in groups:
        file_hash = group["file_hash_sha256"]
        doc_ids: list[uuid.UUID] = group["doc_ids"]

        # Check if cluster already exists for this hash
        existing = await conn.fetchval(
            """SELECT cluster_id FROM brain_dedupe_clusters
            WHERE cluster_type = 'exact' AND method = 'sha256'
              AND metadata->>'file_hash' = $1
            LIMIT 1""",
            file_hash,
        )
        if existing:
            continue

        cluster_id = uuid.uuid4()
        canonical_id = await _select_canonical(conn, doc_ids)

        await conn.execute(
            """INSERT INTO brain_dedupe_clusters
               (cluster_id, cluster_type, method, canonical_member_id, metadata)
            VALUES ($1, 'exact', 'sha256', $2, $3::jsonb)""",
            cluster_id,
            canonical_id,
            json.dumps({"file_hash": file_hash, "member_count": len(doc_ids)}),
        )

        for doc_id in doc_ids:
            role = "canonical" if doc_id == canonical_id else "member"
            await conn.execute(
                """INSERT INTO brain_dedupe_members
                   (member_id, cluster_id, chunk_id, member_role, confidence)
                VALUES ($1, $2, $3, $4, 1.0)""",
                uuid.uuid4(),
                cluster_id,
                doc_id,
                role,
            )

        clusters_created += 1

    return clusters_created


async def _detect_metadata_families(conn: Any) -> int:
    """Group documents by normalised title — metadata-based families."""
    groups = await conn.fetch(
        """
        SELECT lower(trim(title)) AS norm_title, array_agg(document_id) AS doc_ids
        FROM brain_documents
        WHERE title IS NOT NULL AND trim(title) != ''
        GROUP BY lower(trim(title))
        HAVING COUNT(*) > 1
        """
    )

    clusters_created = 0
    for group in groups:
        norm_title = group["norm_title"]
        doc_ids: list[uuid.UUID] = group["doc_ids"]

        existing = await conn.fetchval(
            """SELECT cluster_id FROM brain_dedupe_clusters
            WHERE cluster_type = 'metadata_family' AND method = 'title_path'
              AND metadata->>'norm_title' = $1
            LIMIT 1""",
            norm_title,
        )
        if existing:
            continue

        cluster_id = uuid.uuid4()
        canonical_id = await _select_canonical(conn, doc_ids)

        await conn.execute(
            """INSERT INTO brain_dedupe_clusters
               (cluster_id, cluster_type, method, canonical_member_id, metadata)
            VALUES ($1, 'metadata_family', 'title_path', $2, $3::jsonb)""",
            cluster_id,
            canonical_id,
            json.dumps({"norm_title": norm_title, "member_count": len(doc_ids)}),
        )

        for doc_id in doc_ids:
            role = "canonical" if doc_id == canonical_id else "member"
            await conn.execute(
                """INSERT INTO brain_dedupe_members
                   (member_id, cluster_id, chunk_id, member_role, confidence)
                VALUES ($1, $2, $3, $4, 0.8)""",
                uuid.uuid4(),
                cluster_id,
                doc_id,
                role,
            )

        clusters_created += 1

    return clusters_created


async def _select_canonical(
    conn: Any, doc_ids: list[uuid.UUID]
) -> uuid.UUID:
    """Select the canonical member from a set of documents.

    Priority: best provenance > most complete frontmatter >
    highest chunk count > most recent ingested_at.
    """
    docs = await conn.fetch(
        """
        SELECT document_id, source_system, raw_frontmatter, chunk_count, ingested_at
        FROM brain_documents
        WHERE document_id = ANY($1::uuid[])
        ORDER BY
            CASE WHEN source_system = 'amplified-pipeline-v0.3' THEN 0 ELSE 1 END,
            jsonb_typeof(raw_frontmatter) IS NOT NULL DESC,
            chunk_count DESC,
            ingested_at DESC
        LIMIT 1
        """,
        doc_ids,
    )
    return docs[0]["document_id"] if docs else doc_ids[0]

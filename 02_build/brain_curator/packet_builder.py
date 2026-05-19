"""03_packet_builder — build initial packets from documents with evidence links.

For each document in brain_documents, creates a packet with initial
status='draft' and attaches evidence chunks from knowledge_vectors.

Enforces: active working_model/decision/method/doctrine packets must
have at least one evidence chunk.

Signed-by: Devon-d493 | 2026-05-19 | devin-d49302e4179d43d0892997a7f3a9f57f
"""

from __future__ import annotations

import json
import logging
import uuid
from typing import Any

from brain_curator.config import CODE_VERSION, GOVERNED_PACKET_TYPES
from brain_curator.db import complete_curation_run, connect_writer, start_curation_run

log = logging.getLogger("brain_curator.packet_builder")

# Content pattern keywords for packet type inference
_TYPE_PATTERNS: dict[str, list[str]] = {
    "decision": ["decision", "decided", "we chose", "approved", "rejected"],
    "working_model": ["working model", "current model", "hypothesis", "assumption"],
    "method": ["method", "process", "procedure", "workflow", "how to", "sop"],
    "doctrine": ["principle", "doctrine", "rule", "policy", "must always", "must never"],
    "failure": ["failure", "post-mortem", "postmortem", "incident", "what went wrong"],
    "prompt_pattern": ["prompt", "system prompt", "instruction template"],
}


async def build_packets(run_id: str) -> dict[str, Any]:
    """Build packets from brain_documents and attach evidence chunks.

    Returns metrics dict.
    """
    conn = await connect_writer()
    try:
        await start_curation_run(
            conn, run_id=run_id, stage="packet_builder", code_version=CODE_VERSION
        )

        # Get all inventoried documents that don't have packets yet
        docs = await conn.fetch(
            """
            SELECT bd.document_id, bd.source_path, bd.title, bd.document_type,
                   bd.fm_metadata, bd.file_hash_sha256
            FROM brain_documents bd
            LEFT JOIN brain_packets bp ON bp.source_document_id = bd.document_id
            WHERE bd.status = 'inventoried' AND bp.packet_id IS NULL
            ORDER BY bd.created_at
            """
        )

        packets_created = 0
        evidence_attached = 0
        skipped_no_evidence = 0

        for doc in docs:
            doc_id = doc["document_id"]
            source_path = doc["source_path"]

            # Find evidence chunks from knowledge_vectors
            chunks = await conn.fetch(
                """SELECT id, content, metadata
                FROM knowledge_vectors
                WHERE file_path = $1
                ORDER BY chunk_index""",
                source_path,
            )

            # Determine packet type
            packet_type = doc["document_type"] or _infer_packet_type(
                source_path, [r["content"] for r in chunks]
            )

            # Governed types must have evidence
            if packet_type in GOVERNED_PACKET_TYPES and not chunks:
                skipped_no_evidence += 1
                log.warning(
                    "Skipping governed packet for %s — no evidence chunks",
                    source_path,
                )
                continue

            packet_id = uuid.uuid4()
            title = doc["title"] or _title_from_path(source_path)

            await conn.execute(
                """INSERT INTO brain_packets
                   (packet_id, packet_type, title, status,
                    source_document_id, metadata)
                VALUES ($1, $2, $3, 'draft', $4, $5::jsonb)
                ON CONFLICT DO NOTHING""",
                packet_id,
                packet_type,
                title,
                doc_id,
                json.dumps({"source_path": source_path}),
            )
            packets_created += 1

            # Attach evidence
            for chunk in chunks:
                await conn.execute(
                    """INSERT INTO brain_packet_evidence
                       (evidence_id, packet_id, chunk_id, evidence_role, confidence)
                    VALUES ($1, $2, $3, 'supports', 1.0)
                    ON CONFLICT DO NOTHING""",
                    uuid.uuid4(),
                    packet_id,
                    chunk["id"],
                )
                evidence_attached += 1

        metrics = {
            "documents_processed": len(docs),
            "packets_created": packets_created,
            "evidence_attached": evidence_attached,
            "skipped_no_evidence": skipped_no_evidence,
        }
        await complete_curation_run(conn, run_id, status="completed", metrics=metrics)
        log.info("Packet builder complete: %s", metrics)
        return metrics

    except Exception as e:
        await complete_curation_run(conn, run_id, status="failed", error=str(e))
        raise
    finally:
        await conn.close()


def _infer_packet_type(path: str, contents: list[str]) -> str:
    """Infer packet type from file path and content patterns."""
    path_lower = path.lower()
    combined = " ".join(contents).lower()[:5000]

    for ptype, keywords in _TYPE_PATTERNS.items():
        if any(kw in path_lower for kw in keywords):
            return ptype
        if any(kw in combined for kw in keywords):
            return ptype

    return "reference"


def _title_from_path(file_path: str) -> str | None:
    if not file_path:
        return None
    name = file_path.rsplit("/", 1)[-1]
    if name.endswith(".md"):
        name = name[:-3]
    return name.replace("-", " ").replace("_", " ").strip() or None

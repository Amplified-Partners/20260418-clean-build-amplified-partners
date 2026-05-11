"""Manifest-first canonical writer (v0.3) — AMP-302.

Contract:

    Disk source material = truth.
    Manifest               = proof.
    DB (knowledge_vectors) = rebuildable / searchable index.

The writer consumes **manifest rows** — not a directory scan — and produces
deterministic UUIDs from ``(file_hash, chunk_index)``. Path is informational
only. Rows carry strict provenance: ``file_hash``, ``chunk_index``,
``chunk_total``, ``manifest_id``, ``writer_version``, ``ingested_at``.

The writer does NOT mutate ``entities`` or ``relationships``. Entity
derivation is a separate downstream step, so a re-ingest never silently
rewrites graph edges.

Idempotency: writing the same manifest row twice MUST produce the same
``id`` and the same provenance fingerprint. Re-runs are safe and free.

Engineer B / AMP-302 / 2026-05-11
"""

from __future__ import annotations

import hashlib
import json
import logging
import os
import uuid as _uuid
from dataclasses import dataclass, field, asdict
from datetime import datetime, timezone
from typing import Any, Iterable, Protocol

logger = logging.getLogger("cove.ingestion.writer_v03")

WRITER_VERSION = "v0.3"
WRITER_NAMESPACE = _uuid.UUID("00000000-0000-0000-0000-000000000302")


# ═════════════════════════════════════════════════════════════════════════════
# Data classes
# ═════════════════════════════════════════════════════════════════════════════


@dataclass(frozen=True)
class ManifestRow:
    """One row of an ingestion manifest.

    A manifest is the proof layer between disk (truth) and DB (index). It
    pins exactly which bytes produced which row and is the only thing the
    writer is allowed to consume.
    """
    manifest_id: str           # opaque id from manifest builder; stable per (file_hash, chunk_index)
    file_hash: str             # sha256 hex of the source file bytes
    chunk_index: int           # 0-based; 0 for non-chunked files
    chunk_total: int           # total chunks; 1 for non-chunked files
    content: str               # the chunk text/body to be indexed
    source_path: str           # informational; not part of the ID
    source_type: str           # e.g. 'pudding_md', 'raw_email', 'compound_design'
    metadata: dict[str, Any] = field(default_factory=dict)

    def __post_init__(self) -> None:
        # Frozen dataclass — assert via object.__setattr__ guard is heavy.
        # Cheap, explicit validation at construction.
        if not self.file_hash or len(self.file_hash) < 16:
            raise ValueError(f"file_hash must be a non-trivial hash, got {self.file_hash!r}")
        if self.chunk_index < 0:
            raise ValueError(f"chunk_index must be >= 0, got {self.chunk_index}")
        if self.chunk_total < 1:
            raise ValueError(f"chunk_total must be >= 1, got {self.chunk_total}")
        if self.chunk_index >= self.chunk_total:
            raise ValueError(
                f"chunk_index ({self.chunk_index}) must be < chunk_total ({self.chunk_total})"
            )
        if not self.manifest_id:
            raise ValueError("manifest_id is required")
        if not self.source_type:
            raise ValueError("source_type is required")


@dataclass
class WriteResult:
    rows_written: int = 0
    rows_skipped: int = 0
    rows_failed: int = 0
    ids: list[str] = field(default_factory=list)
    errors: list[str] = field(default_factory=list)

    @property
    def success(self) -> bool:
        return self.rows_failed == 0


# ═════════════════════════════════════════════════════════════════════════════
# Deterministic ID derivation
# ═════════════════════════════════════════════════════════════════════════════


def derive_row_id(file_hash: str, chunk_index: int) -> _uuid.UUID:
    """Deterministic UUIDv5 of ``(file_hash, chunk_index)``.

    The same input MUST always produce the same UUID. Path is intentionally
    not part of the input — moving or renaming a file does not produce a
    new row.
    """
    if not file_hash:
        raise ValueError("file_hash is required for ID derivation")
    if chunk_index < 0:
        raise ValueError("chunk_index must be >= 0")
    name = f"{file_hash}:{chunk_index}"
    return _uuid.uuid5(WRITER_NAMESPACE, name)


def provenance_fingerprint(row: ManifestRow) -> str:
    """Stable fingerprint of the provenance triple. Used in tests and audit."""
    payload = f"{row.file_hash}|{row.chunk_index}|{row.chunk_total}|{row.manifest_id}"
    return hashlib.sha256(payload.encode("utf-8")).hexdigest()


# ═════════════════════════════════════════════════════════════════════════════
# DB protocol — kept tiny so tests can swap in an in-memory fake
# ═════════════════════════════════════════════════════════════════════════════


class WriterConnection(Protocol):
    """Minimal interface the writer needs.

    Implementations: ``asyncpg.Connection`` in prod, ``FakeConnection``
    in tests. We deliberately do not depend on asyncpg at import time so
    these modules can be unit-tested without a database.
    """

    async def execute(self, query: str, *args: Any) -> Any: ...


# ═════════════════════════════════════════════════════════════════════════════
# Writer
# ═════════════════════════════════════════════════════════════════════════════


# The single INSERT/UPDATE statement the writer is allowed to use against
# knowledge_vectors. ON CONFLICT (id) — combined with the deterministic ID —
# is what makes the writer idempotent.
_UPSERT_SQL = """
INSERT INTO knowledge_vectors (
    id, content, source, source_type, metadata,
    file_hash, chunk_index, chunk_total, manifest_id, writer_version, ingested_at
) VALUES (
    $1, $2, $3, $4, $5::jsonb,
    $6, $7, $8, $9, $10, $11
)
ON CONFLICT (id) DO UPDATE SET
    content        = EXCLUDED.content,
    source         = EXCLUDED.source,
    source_type    = EXCLUDED.source_type,
    metadata       = EXCLUDED.metadata,
    file_hash      = EXCLUDED.file_hash,
    chunk_index    = EXCLUDED.chunk_index,
    chunk_total    = EXCLUDED.chunk_total,
    manifest_id    = EXCLUDED.manifest_id,
    writer_version = EXCLUDED.writer_version,
    ingested_at    = EXCLUDED.ingested_at,
    updated_at     = now()
"""


def build_metadata(row: ManifestRow) -> dict[str, Any]:
    """Compose the metadata blob written to knowledge_vectors.metadata.

    Caller-supplied metadata is preserved verbatim under ``user``. Writer
    stamps under ``provenance`` so a reader can always trust the writer
    fields regardless of upstream shape.
    """
    return {
        "user": dict(row.metadata or {}),
        "provenance": {
            "manifest_id":    row.manifest_id,
            "file_hash":      row.file_hash,
            "chunk_index":    row.chunk_index,
            "chunk_total":    row.chunk_total,
            "source_path":    row.source_path,
            "writer_version": WRITER_VERSION,
            "fingerprint":    provenance_fingerprint(row),
        },
    }


async def write_manifest_row(conn: WriterConnection, row: ManifestRow) -> _uuid.UUID:
    """Upsert exactly one manifest row. Returns the deterministic row id."""
    row_id = derive_row_id(row.file_hash, row.chunk_index)
    metadata = build_metadata(row)
    now = datetime.now(timezone.utc)

    await conn.execute(
        _UPSERT_SQL,
        row_id,
        row.content,
        row.source_path,
        row.source_type,
        json.dumps(metadata),
        row.file_hash,
        row.chunk_index,
        row.chunk_total,
        row.manifest_id,
        WRITER_VERSION,
        now,
    )
    return row_id


async def write_manifest_batch(
    conn: WriterConnection,
    rows: Iterable[ManifestRow],
) -> WriteResult:
    """Upsert a batch. Each row is independent — one failure does not abort the batch."""
    result = WriteResult()
    for row in rows:
        try:
            rid = await write_manifest_row(conn, row)
            result.rows_written += 1
            result.ids.append(str(rid))
        except Exception as e:
            result.rows_failed += 1
            err = f"{row.manifest_id}: {type(e).__name__}: {e}"
            result.errors.append(err)
            logger.warning("write_manifest_row failed: %s", err)
    return result


# ═════════════════════════════════════════════════════════════════════════════
# Re-export the writer version so callers (telemetry, tests) agree
# ═════════════════════════════════════════════════════════════════════════════

__all__ = [
    "WRITER_VERSION",
    "WRITER_NAMESPACE",
    "ManifestRow",
    "WriteResult",
    "WriterConnection",
    "derive_row_id",
    "provenance_fingerprint",
    "build_metadata",
    "write_manifest_row",
    "write_manifest_batch",
]

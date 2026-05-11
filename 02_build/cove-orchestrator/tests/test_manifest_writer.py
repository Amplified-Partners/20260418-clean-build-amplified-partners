"""Tests for the v0.3 manifest-first canonical writer (AMP-302).

These tests do not touch a real PostgreSQL. The writer's only DB
dependency is a ``conn.execute(query, *args)`` coroutine, so we hand it
a tiny in-memory fake. The point is to lock in the *contract*:

* Deterministic IDs from (file_hash, chunk_index) — never from path.
* Required provenance metadata on every row.
* Idempotency under re-run (same input → same id, no growth).
* No inline mutation of entities/relationships.
* The canonical view filter (writer-stamped fields present) is what
  qualifies a row as canonical.
"""

from __future__ import annotations

import json
import re
import uuid
from typing import Any

import pytest

from temporal.activities.manifest_writer import (
    WRITER_VERSION,
    ManifestRow,
    build_metadata,
    derive_row_id,
    provenance_fingerprint,
    write_manifest_batch,
    write_manifest_row,
)


# ─── Fake DB ────────────────────────────────────────────────────────────────


class FakeConnection:
    """In-memory stand-in for asyncpg.Connection.

    Records every ``execute`` call as a (query, args) tuple. The writer
    treats it as a plain upsert sink. We also model an ``id``-keyed store
    so we can assert idempotency.
    """

    def __init__(self) -> None:
        self.calls: list[tuple[str, tuple[Any, ...]]] = []
        # id -> last-written row (mirrors knowledge_vectors as ON CONFLICT DO UPDATE)
        self.rows: dict[str, dict[str, Any]] = {}

    async def execute(self, query: str, *args: Any) -> None:
        self.calls.append((query, args))
        if "INSERT INTO knowledge_vectors" in query:
            (
                row_id, content, source, source_type, metadata,
                file_hash, chunk_index, chunk_total, manifest_id,
                writer_version, ingested_at,
            ) = args
            self.rows[str(row_id)] = {
                "id": row_id,
                "content": content,
                "source": source,
                "source_type": source_type,
                "metadata": json.loads(metadata) if isinstance(metadata, str) else metadata,
                "file_hash": file_hash,
                "chunk_index": chunk_index,
                "chunk_total": chunk_total,
                "manifest_id": manifest_id,
                "writer_version": writer_version,
                "ingested_at": ingested_at,
            }


def _row(
    *,
    manifest_id: str = "m-1",
    file_hash: str = "a" * 64,
    chunk_index: int = 0,
    chunk_total: int = 1,
    content: str = "body",
    source_path: str = "/opt/amplified/archive/store_b_clean/file.md",
    source_type: str = "pudding_md",
    metadata: dict[str, Any] | None = None,
) -> ManifestRow:
    return ManifestRow(
        manifest_id=manifest_id,
        file_hash=file_hash,
        chunk_index=chunk_index,
        chunk_total=chunk_total,
        content=content,
        source_path=source_path,
        source_type=source_type,
        metadata=metadata or {"k": "v"},
    )


# ─── Deterministic ID ───────────────────────────────────────────────────────


def test_derive_row_id_is_deterministic() -> None:
    a = derive_row_id("a" * 64, 0)
    b = derive_row_id("a" * 64, 0)
    assert a == b
    assert isinstance(a, uuid.UUID)


def test_derive_row_id_changes_with_chunk_index() -> None:
    assert derive_row_id("a" * 64, 0) != derive_row_id("a" * 64, 1)


def test_derive_row_id_changes_with_file_hash() -> None:
    assert derive_row_id("a" * 64, 0) != derive_row_id("b" * 64, 0)


def test_derive_row_id_ignores_path() -> None:
    """Path is not part of the ID. This is the core invariant of v0.3."""
    rid_via_row_a = derive_row_id("c" * 64, 0)
    rid_via_row_b = derive_row_id("c" * 64, 0)  # same file_hash, would-be different path
    assert rid_via_row_a == rid_via_row_b


def test_derive_row_id_rejects_empty_hash() -> None:
    with pytest.raises(ValueError):
        derive_row_id("", 0)


# ─── ManifestRow validation ─────────────────────────────────────────────────


def test_manifest_row_rejects_bad_chunk_index() -> None:
    with pytest.raises(ValueError):
        _row(chunk_index=-1)
    with pytest.raises(ValueError):
        _row(chunk_index=5, chunk_total=5)  # must be strictly less than total


def test_manifest_row_rejects_short_hash() -> None:
    with pytest.raises(ValueError):
        _row(file_hash="abc")


def test_manifest_row_rejects_missing_manifest_id() -> None:
    with pytest.raises(ValueError):
        _row(manifest_id="")


# ─── Provenance metadata shape ──────────────────────────────────────────────


def test_build_metadata_stamps_provenance() -> None:
    row = _row(metadata={"taxonomy": "PUDDING_2026"})
    meta = build_metadata(row)
    assert meta["user"] == {"taxonomy": "PUDDING_2026"}
    prov = meta["provenance"]
    for k in (
        "manifest_id", "file_hash", "chunk_index", "chunk_total",
        "source_path", "writer_version", "fingerprint",
    ):
        assert k in prov, f"missing provenance key: {k}"
    assert prov["writer_version"] == WRITER_VERSION
    assert prov["fingerprint"] == provenance_fingerprint(row)


def test_provenance_fingerprint_is_stable() -> None:
    r1 = _row()
    r2 = _row()
    assert provenance_fingerprint(r1) == provenance_fingerprint(r2)


def test_provenance_fingerprint_changes_on_any_field() -> None:
    base = _row()
    assert provenance_fingerprint(base) != provenance_fingerprint(
        _row(chunk_index=0, chunk_total=2)
    )
    assert provenance_fingerprint(base) != provenance_fingerprint(_row(file_hash="d" * 64))


# ─── Upsert behaviour ───────────────────────────────────────────────────────


@pytest.mark.asyncio
async def test_write_row_emits_required_columns() -> None:
    conn = FakeConnection()
    row = _row()
    row_id = await write_manifest_row(conn, row)
    assert str(row_id) in conn.rows
    written = conn.rows[str(row_id)]
    assert written["file_hash"] == row.file_hash
    assert written["chunk_index"] == row.chunk_index
    assert written["chunk_total"] == row.chunk_total
    assert written["manifest_id"] == row.manifest_id
    assert written["writer_version"] == WRITER_VERSION
    # writer_version must satisfy the migration CHECK constraint
    assert re.match(r"^v[0-9]+\.[0-9]+", written["writer_version"])
    assert "provenance" in written["metadata"]
    assert "user" in written["metadata"]


@pytest.mark.asyncio
async def test_writer_is_idempotent_under_rerun() -> None:
    """Same manifest row written twice → same id, no new row created."""
    conn = FakeConnection()
    row = _row()
    rid_a = await write_manifest_row(conn, row)
    rid_b = await write_manifest_row(conn, row)
    assert rid_a == rid_b
    assert len(conn.rows) == 1


@pytest.mark.asyncio
async def test_writer_id_unchanged_when_path_changes() -> None:
    """Moving a file on disk does NOT produce a new row.

    This is the headline behaviour of v0.3: ID depends only on the file's
    content hash and chunk index. Pre-v0.3 derived IDs from the path,
    which is why re-organising disk could cause silent row duplication.
    """
    conn = FakeConnection()
    rid_a = await write_manifest_row(conn, _row(source_path="/old/path/file.md"))
    rid_b = await write_manifest_row(conn, _row(source_path="/new/path/file.md"))
    assert rid_a == rid_b
    assert len(conn.rows) == 1


@pytest.mark.asyncio
async def test_writer_different_chunks_distinct_rows() -> None:
    conn = FakeConnection()
    rid0 = await write_manifest_row(
        conn, _row(chunk_index=0, chunk_total=3, content="part 0")
    )
    rid1 = await write_manifest_row(
        conn, _row(chunk_index=1, chunk_total=3, content="part 1")
    )
    rid2 = await write_manifest_row(
        conn, _row(chunk_index=2, chunk_total=3, content="part 2")
    )
    assert len({rid0, rid1, rid2}) == 3
    assert len(conn.rows) == 3


@pytest.mark.asyncio
async def test_writer_never_touches_entities_or_relationships() -> None:
    """Audit guard: the v0.3 writer must only write knowledge_vectors.

    Entity/relationship derivation is a separate downstream step. This
    test fails if anyone slips an INSERT INTO entities into the writer.
    """
    conn = FakeConnection()
    await write_manifest_row(conn, _row())
    sqls = " ".join(q for q, _ in conn.calls).lower()
    assert "entities" not in sqls
    assert "relationships" not in sqls


# ─── Batch behaviour ────────────────────────────────────────────────────────


@pytest.mark.asyncio
async def test_batch_writes_all_rows_and_returns_ids() -> None:
    conn = FakeConnection()
    rows = [
        _row(manifest_id=f"m-{i}", file_hash=f"{i:064x}")
        for i in range(5)
    ]
    result = await write_manifest_batch(conn, rows)
    assert result.success
    assert result.rows_written == 5
    assert result.rows_failed == 0
    assert len(result.ids) == 5
    assert len(conn.rows) == 5


@pytest.mark.asyncio
async def test_batch_continues_after_single_row_failure() -> None:
    """One bad row must not abort the whole batch."""

    class FlakyConnection(FakeConnection):
        async def execute(self, query: str, *args: Any) -> None:
            # Fail on manifest_id == "m-bad"
            if args and args[8] == "m-bad":
                raise RuntimeError("boom")
            await super().execute(query, *args)

    conn = FlakyConnection()
    rows = [
        _row(manifest_id="m-1", file_hash="1" * 64),
        _row(manifest_id="m-bad", file_hash="2" * 64),
        _row(manifest_id="m-3", file_hash="3" * 64),
    ]
    result = await write_manifest_batch(conn, rows)
    assert result.rows_written == 2
    assert result.rows_failed == 1
    assert any("m-bad" in e for e in result.errors)


# ─── Canonical view qualification ───────────────────────────────────────────


@pytest.mark.asyncio
async def test_writer_stamps_all_canonical_view_columns() -> None:
    """The canonical view filters on file_hash, manifest_id, writer_version.

    Every row the writer produces MUST set those three columns, otherwise
    the row would never appear in knowledge_vectors_canonical and would
    be invisible to canonical readers.
    """
    conn = FakeConnection()
    await write_manifest_row(conn, _row())
    [(_id, row)] = conn.rows.items()
    assert row["file_hash"] is not None
    assert row["manifest_id"] is not None
    assert row["writer_version"] is not None

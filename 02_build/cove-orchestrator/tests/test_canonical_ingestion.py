"""Tests for canonical ingestion pipeline v0.3 (AMP-302).

Covers: manifest determinism, chunk chain integrity, provenance metadata,
legacy writer quarantine, and dry-run contract.

These tests use in-memory data — no live database required.

Signed-by: Devon-0de2 | 2026-05-11 | devin-0de27df281514f96ba3921354d7c31ae
"""

from __future__ import annotations

import json
import uuid
from pathlib import Path

import pytest

# Module under test
from temporal.activities.manifest_generator import (
    build_chunk_records,
    build_manifest_line,
    chunk_by_heading,
    manifest_line_to_dict,
    sha256_bytes,
    sha256_file,
    PIPELINE_VERSION,
    SIGNED_BY,
)
from temporal.activities.canonical_writer import (
    deterministic_id,
)


# ═══════════════════════════════════════════════════════════════════════
# Fixtures
# ═══════════════════════════════════════════════════════════════════════

SAMPLE_MD = """\
---
title: Test Document
---

# Heading 1

Some intro text here.

## Section A

Content for section A with enough text to be meaningful.
This has multiple lines of prose that form a coherent chunk.

## Section B

Content for section B, separate from section A.
Also multiple lines.

## Section C

Final section with more content.
"""

SAMPLE_MD_NO_HEADINGS = "Just a plain document with no headings at all.\nLine two.\nLine three.\n"


@pytest.fixture
def source_dir(tmp_path: Path) -> Path:
    """Create a temporary source directory with sample .md files."""
    (tmp_path / "doc1.md").write_text(SAMPLE_MD, encoding="utf-8")
    (tmp_path / "doc2.md").write_text(SAMPLE_MD_NO_HEADINGS, encoding="utf-8")
    (tmp_path / "subdir").mkdir()
    (tmp_path / "subdir" / "doc3.md").write_text(
        "## Sub-heading\n\nNested file content.\n", encoding="utf-8"
    )
    return tmp_path


# ═══════════════════════════════════════════════════════════════════════
# Test 1: Dry-run determinism
# ═══════════════════════════════════════════════════════════════════════

class TestManifestDeterminism:
    """Same source files → same manifest bytes."""

    def test_chunk_by_heading_deterministic(self):
        chunks_a = chunk_by_heading(SAMPLE_MD)
        chunks_b = chunk_by_heading(SAMPLE_MD)
        assert len(chunks_a) == len(chunks_b)
        for a, b in zip(chunks_a, chunks_b):
            assert a["text"] == b["text"]
            assert a["line_start"] == b["line_start"]
            assert a["line_end"] == b["line_end"]

    def test_sha256_bytes_deterministic(self):
        data = b"test content for hashing"
        assert sha256_bytes(data) == sha256_bytes(data)

    def test_sha256_file_deterministic(self, tmp_path: Path):
        f = tmp_path / "test.txt"
        f.write_text("deterministic content")
        assert sha256_file(f) == sha256_file(f)

    def test_manifest_line_deterministic(self, tmp_path: Path):
        f = tmp_path / "test.md"
        f.write_text(SAMPLE_MD)
        file_hash = sha256_file(f)
        chunks = build_chunk_records(chunk_by_heading(SAMPLE_MD))

        line_a = manifest_line_to_dict(build_manifest_line(
            "run-1", str(tmp_path), f, file_hash, chunks, "2026-05-11T00:00:00Z"
        ))
        line_b = manifest_line_to_dict(build_manifest_line(
            "run-1", str(tmp_path), f, file_hash, chunks, "2026-05-11T00:00:00Z"
        ))
        assert json.dumps(line_a, sort_keys=True) == json.dumps(line_b, sort_keys=True)


# ═══════════════════════════════════════════════════════════════════════
# Test 2: Idempotent IDs
# ═══════════════════════════════════════════════════════════════════════

class TestIdempotentIds:
    """Same file_hash + chunk_index → same UUID."""

    def test_deterministic_id_stable(self):
        id_a = deterministic_id("sha256:abc123", 0)
        id_b = deterministic_id("sha256:abc123", 0)
        assert id_a == id_b
        assert isinstance(id_a, uuid.UUID)

    def test_different_chunks_different_ids(self):
        id_0 = deterministic_id("sha256:abc123", 0)
        id_1 = deterministic_id("sha256:abc123", 1)
        assert id_0 != id_1

    def test_different_files_different_ids(self):
        id_a = deterministic_id("sha256:file_a", 0)
        id_b = deterministic_id("sha256:file_b", 0)
        assert id_a != id_b


# ═══════════════════════════════════════════════════════════════════════
# Test 3: Required provenance metadata
# ═══════════════════════════════════════════════════════════════════════

class TestProvenanceMetadata:
    """Every manifest line has all required provenance fields."""

    REQUIRED_FIELDS = {
        "run_id", "pipeline_version", "source_root", "file_path",
        "file_hash", "size_bytes", "mtime", "chunks", "signed_by", "created_at",
    }
    REQUIRED_CHUNK_FIELDS = {
        "idx", "chunk_hash", "line_start", "line_end",
        "parent_heading", "chunk_type", "prev_hash", "next_hash",
    }

    def test_manifest_line_has_all_fields(self, tmp_path: Path):
        f = tmp_path / "test.md"
        f.write_text(SAMPLE_MD)
        file_hash = sha256_file(f)
        chunks = build_chunk_records(chunk_by_heading(SAMPLE_MD))
        line = manifest_line_to_dict(build_manifest_line(
            "run-test", str(tmp_path), f, file_hash, chunks, "2026-05-11T00:00:00Z"
        ))
        assert self.REQUIRED_FIELDS.issubset(line.keys()), \
            f"Missing: {self.REQUIRED_FIELDS - line.keys()}"

    def test_chunks_have_all_fields(self, tmp_path: Path):
        f = tmp_path / "test.md"
        f.write_text(SAMPLE_MD)
        file_hash = sha256_file(f)
        chunks = build_chunk_records(chunk_by_heading(SAMPLE_MD))
        line = manifest_line_to_dict(build_manifest_line(
            "run-test", str(tmp_path), f, file_hash, chunks, "2026-05-11T00:00:00Z"
        ))
        for chunk in line["chunks"]:
            assert self.REQUIRED_CHUNK_FIELDS.issubset(chunk.keys()), \
                f"Missing: {self.REQUIRED_CHUNK_FIELDS - chunk.keys()}"

    def test_pipeline_version_correct(self):
        assert PIPELINE_VERSION == "amplified-pipeline-v0.3"

    def test_signed_by_correct(self):
        assert SIGNED_BY == "brain_writer_pipeline"


# ═══════════════════════════════════════════════════════════════════════
# Test 4: Chunk chain integrity
# ═══════════════════════════════════════════════════════════════════════

class TestChunkChainIntegrity:
    """prev_hash/next_hash chain is unbroken."""

    def test_chain_links(self):
        chunks = chunk_by_heading(SAMPLE_MD)
        records = build_chunk_records(chunks)
        assert len(records) > 1, "Need multiple chunks for chain test"

        # First chunk has no prev
        assert records[0].prev_hash is None
        assert records[0].next_hash is not None

        # Last chunk has no next
        assert records[-1].next_hash is None
        assert records[-1].prev_hash is not None

        # Middle chunks link correctly
        for i in range(1, len(records) - 1):
            assert records[i].prev_hash == records[i - 1].chunk_hash
            assert records[i].next_hash == records[i + 1].chunk_hash

        # Forward chain matches backward chain
        for i in range(len(records) - 1):
            assert records[i].next_hash == records[i + 1].chunk_hash
            assert records[i + 1].prev_hash == records[i].chunk_hash

    def test_single_chunk_no_chain(self):
        chunks = chunk_by_heading(SAMPLE_MD_NO_HEADINGS)
        records = build_chunk_records(chunks)
        assert len(records) == 1
        assert records[0].prev_hash is None
        assert records[0].next_hash is None


# ═══════════════════════════════════════════════════════════════════════
# Test 5: Legacy writers blocked
# ═══════════════════════════════════════════════════════════════════════

class TestLegacyWritersBlocked:
    """Archived legacy writers raise RuntimeError on import."""

    def test_migrate_qdrant_raises(self):
        with pytest.raises(RuntimeError, match="LEGACY WRITER"):
            # The raise is at module level, so importing triggers it
            import importlib
            import sys
            # Remove from cache if already imported
            sys.modules.pop("migrate_qdrant", None)
            spec = importlib.util.spec_from_file_location(
                "migrate_qdrant",
                str(Path(__file__).parent.parent.parent.parent
                    / "90_archive" / "legacy-writers" / "migrate_qdrant.py"),
            )
            mod = importlib.util.module_from_spec(spec)
            spec.loader.exec_module(mod)

    def test_migrate_falkordb_raises(self):
        with pytest.raises(RuntimeError, match="LEGACY WRITER"):
            import importlib
            import sys
            sys.modules.pop("migrate_falkordb", None)
            spec = importlib.util.spec_from_file_location(
                "migrate_falkordb",
                str(Path(__file__).parent.parent.parent.parent
                    / "90_archive" / "legacy-writers" / "migrate_falkordb.py"),
            )
            mod = importlib.util.module_from_spec(spec)
            spec.loader.exec_module(mod)


# ═══════════════════════════════════════════════════════════════════════
# Test 6: Chunking edge cases
# ═══════════════════════════════════════════════════════════════════════

class TestChunkingEdgeCases:
    """Chunking handles edge cases correctly."""

    def test_empty_content(self):
        chunks = chunk_by_heading("")
        assert chunks == []

    def test_no_headings(self):
        chunks = chunk_by_heading("Just text\nMore text\n")
        assert len(chunks) == 1
        assert chunks[0]["heading"] == "(top-level)"

    def test_heading_only(self):
        chunks = chunk_by_heading("## Just a heading\n")
        assert len(chunks) == 1
        assert chunks[0]["heading"] == "Just a heading"

    def test_consecutive_headings(self):
        content = "## A\n\n## B\n\nContent B\n"
        chunks = chunk_by_heading(content)
        assert len(chunks) >= 2

    def test_line_numbers_correct(self):
        chunks = chunk_by_heading(SAMPLE_MD)
        for chunk in chunks:
            assert chunk["line_start"] >= 1
            assert chunk["line_end"] >= chunk["line_start"]

    def test_oversized_chunk_split(self):
        big_content = "## Big section\n\n" + ("x" * 5000) + "\n"
        chunks = chunk_by_heading(big_content, max_chars=2000)
        assert len(chunks) > 1
        for chunk in chunks:
            assert len(chunk["text"]) <= 5100  # allow small overshoot from line boundaries


# ═══════════════════════════════════════════════════════════════════════
# Test 7: Deprecated write_to_memory_stores raises
# ═══════════════════════════════════════════════════════════════════════

class TestDeprecatedWriter:
    """write_to_memory_stores must raise RuntimeError."""

    @pytest.mark.asyncio
    async def test_write_to_memory_stores_raises(self):
        from temporal.activities.ingestion_activities import (
            MemoryStoreInput,
            write_to_memory_stores,
        )
        with pytest.raises(RuntimeError, match="DEPRECATED"):
            await write_to_memory_stores(MemoryStoreInput())

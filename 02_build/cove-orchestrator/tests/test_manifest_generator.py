"""Tests for the canonical manifest generator (AMP-302).

Covers:
    * Dry-run is deterministic and emits no manifest file / no DB writes.
    * Chunk chain integrity: prev_hash / next_hash form a valid singly-linked
      chain across the chunks of a file.
    * Required manifest fields are present on every record.
    * Path-independence: identical bytes at different on-disk paths produce
      identical file_hash + chunk_hash sequences.

Signed-by: Claude Code instance A | 2026-05-11 | AMP-302
"""

from __future__ import annotations

import json
from pathlib import Path

import pytest

from ingestion.manifest_generator import (
    PIPELINE_VERSION,
    SIGNED_BY,
    ManifestGenerator,
    chunk_text,
    generate_manifest,
)


REQUIRED_FILE_FIELDS = {
    "run_id",
    "pipeline_version",
    "source_root",
    "file_path",
    "file_hash",
    "size_bytes",
    "mtime",
    "chunks",
    "signed_by",
    "created_at",
}

REQUIRED_CHUNK_FIELDS = {
    "idx",
    "chunk_hash",
    "line_start",
    "line_end",
    "parent_heading",
    "chunk_type",
    "prev_hash",
    "next_hash",
}


# ── fixtures ────────────────────────────────────────────────────────


def _seed_corpus(root: Path) -> None:
    (root / "subdir").mkdir(parents=True, exist_ok=True)
    (root / "alpha.md").write_text(
        "# Heading One\n"
        "line two of alpha\n"
        "line three of alpha\n"
        "## Subheading\n"
        "line five of alpha\n",
        encoding="utf-8",
    )
    (root / "subdir" / "beta.txt").write_text(
        "\n".join(f"beta line {i}" for i in range(1, 121)) + "\n",
        encoding="utf-8",
    )
    (root / "ignored.bin").write_bytes(b"\x00\x01\x02\x03")


@pytest.fixture
def corpus(tmp_path: Path) -> Path:
    root = tmp_path / "store_b_clean"
    root.mkdir()
    _seed_corpus(root)
    return root


# ── dry-run determinism ─────────────────────────────────────────────


def test_dry_run_writes_nothing(corpus: Path, tmp_path: Path) -> None:
    out = tmp_path / "manifest.jsonl"
    summary = generate_manifest(
        source_root=corpus,
        output_path=out,
        run_id="fixed-run",
        dry_run=True,
    )
    assert summary.dry_run is True
    assert summary.manifest_path is None
    assert not out.exists()
    assert summary.file_count >= 2
    assert summary.chunk_count >= 1
    assert summary.predicted_db_rows["knowledge_vectors"] == summary.chunk_count
    assert summary.predicted_db_rows["pipeline_runs"] == 1
    assert summary.predicted_db_rows["audit_log"] == summary.file_count


def test_dry_run_deterministic_across_invocations(corpus: Path) -> None:
    a = generate_manifest(source_root=corpus, run_id="run-A", dry_run=True)
    b = generate_manifest(source_root=corpus, run_id="run-A", dry_run=True)
    assert a.file_count == b.file_count
    assert a.chunk_count == b.chunk_count
    assert a.predicted_db_rows == b.predicted_db_rows


# ── chunk chain integrity ───────────────────────────────────────────


def test_chunk_chain_integrity(corpus: Path, tmp_path: Path) -> None:
    out = tmp_path / "manifest.jsonl"
    generate_manifest(
        source_root=corpus,
        output_path=out,
        run_id="chain-run",
        dry_run=False,
        chunk_lines=10,
    )
    records = [json.loads(line) for line in out.read_text().splitlines()]
    multichunk = [r for r in records if len(r["chunks"]) > 1]
    assert multichunk, "fixture should produce at least one multi-chunk file"
    for rec in multichunk:
        chunks = rec["chunks"]
        assert chunks[0]["prev_hash"] is None
        assert chunks[-1]["next_hash"] is None
        for i in range(len(chunks) - 1):
            assert chunks[i]["next_hash"] == chunks[i + 1]["chunk_hash"]
            assert chunks[i + 1]["prev_hash"] == chunks[i]["chunk_hash"]
        for i, ch in enumerate(chunks):
            assert ch["idx"] == i
            assert ch["line_start"] <= ch["line_end"]


def test_chunk_text_unit_chain() -> None:
    chunks = chunk_text("a\nb\nc\nd\ne\nf\n", chunk_lines=2)
    assert len(chunks) == 3
    assert chunks[0].prev_hash is None
    assert chunks[-1].next_hash is None
    assert chunks[0].next_hash == chunks[1].chunk_hash
    assert chunks[1].prev_hash == chunks[0].chunk_hash


# ── required fields ─────────────────────────────────────────────────


def test_required_manifest_fields(corpus: Path, tmp_path: Path) -> None:
    out = tmp_path / "manifest.jsonl"
    generate_manifest(
        source_root=corpus,
        output_path=out,
        run_id="fields-run",
        dry_run=False,
    )
    lines = out.read_text().splitlines()
    assert lines, "manifest should not be empty"
    for raw in lines:
        rec = json.loads(raw)
        missing = REQUIRED_FILE_FIELDS - set(rec.keys())
        assert not missing, f"missing top-level fields: {missing}"
        assert rec["pipeline_version"] == PIPELINE_VERSION
        assert rec["signed_by"] == SIGNED_BY
        assert rec["run_id"] == "fields-run"
        for ch in rec["chunks"]:
            missing_c = REQUIRED_CHUNK_FIELDS - set(ch.keys())
            assert not missing_c, f"missing chunk fields: {missing_c}"


# ── path independence ──────────────────────────────────────────────


def test_path_independent_content_hashes(tmp_path: Path) -> None:
    """Identical bytes at different paths must produce identical hashes.

    file_hash is over content bytes only.
    chunk_hash is over chunk body bytes only.
    Neither should depend on source_root, parent directory, or filename
    placement *within* the corpus — only on the file content + chunk size.
    """
    content = "alpha\nbeta\ngamma\ndelta\nepsilon\n" * 5

    root_a = tmp_path / "A" / "store_b_clean"
    root_b = tmp_path / "B" / "elsewhere"
    (root_a / "deep" / "nest").mkdir(parents=True)
    (root_b / "flat").mkdir(parents=True)
    (root_a / "deep" / "nest" / "doc.md").write_text(content, encoding="utf-8")
    (root_b / "flat" / "doc.md").write_text(content, encoding="utf-8")

    out_a = tmp_path / "a.jsonl"
    out_b = tmp_path / "b.jsonl"
    generate_manifest(source_root=root_a, output_path=out_a, run_id="x", dry_run=False)
    generate_manifest(source_root=root_b, output_path=out_b, run_id="x", dry_run=False)

    rec_a = json.loads(out_a.read_text().splitlines()[0])
    rec_b = json.loads(out_b.read_text().splitlines()[0])
    assert rec_a["file_hash"] == rec_b["file_hash"]
    assert [c["chunk_hash"] for c in rec_a["chunks"]] == [
        c["chunk_hash"] for c in rec_b["chunks"]
    ]
    # file_path is path-relative-to-source_root, so it SHOULD differ here —
    # this asserts the contract intentionally.
    assert rec_a["file_path"] != rec_b["file_path"]


def test_empty_source_root(tmp_path: Path) -> None:
    empty = tmp_path / "empty"
    empty.mkdir()
    summary = generate_manifest(source_root=empty, dry_run=True)
    assert summary.file_count == 0
    assert summary.chunk_count == 0
    assert summary.predicted_db_rows["knowledge_vectors"] == 0
    assert summary.predicted_db_rows["audit_log"] == 0


def test_generator_class_matches_function(corpus: Path, tmp_path: Path) -> None:
    out_fn = tmp_path / "fn.jsonl"
    out_cls = tmp_path / "cls.jsonl"
    generate_manifest(
        source_root=corpus, output_path=out_fn, run_id="match", dry_run=False
    )
    ManifestGenerator(
        source_root=corpus, output_path=out_cls, run_id="match", dry_run=False
    ).run()
    # Top-level created_at differs by second; compare the stable subset.
    def _stable(line: str) -> dict:
        rec = json.loads(line)
        rec.pop("created_at", None)
        for c in rec.get("chunks", []):
            c.pop("created_at", None)
        return rec

    fn_recs = [_stable(line) for line in out_fn.read_text().splitlines()]
    cls_recs = [_stable(line) for line in out_cls.read_text().splitlines()]
    assert fn_recs == cls_recs

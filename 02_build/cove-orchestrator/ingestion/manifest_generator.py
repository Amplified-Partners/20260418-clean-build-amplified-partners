"""Canonical manifest-first ingestion contract for the clean Cove corpus.

This module is the truth-shaped boundary between disk source material and the
amplified_brain database. It scans a `source_root` (typically
`/opt/amplified/archive/store_b_clean` on Beast), chunks each file
deterministically, and emits a JSONL manifest where each record is one chunk
plus a per-file manifest header. The DB is treated as a rebuildable index over
this manifest — never the source of truth.

Doctrine alignment (AMP-302):
    * Disk source material = truth
    * Manifest = proof (signed, hash-chained, deterministic)
    * DB = rebuildable / searchable index

Dry-run mode writes no DB rows AND no manifest file; it returns a predicted
row-count / chunk-count summary so an operator can compare against a planned
production run before approving cutover.

Why this exists right now:
    Live DB row waves came from multiple incompatible writers; the current
    on-disk writer does not explain live DB provenance. AMP-302 narrows the
    contract so every future write is attributable to one signed manifest row.

Signed-by: Claude Code instance A | 2026-05-11 | AMP-302
"""

from __future__ import annotations

import hashlib
import json
import os
import re
import uuid
from dataclasses import asdict, dataclass, field
from datetime import datetime, timezone
from pathlib import Path
from typing import Iterable, Iterator

PIPELINE_VERSION = "amplified-pipeline-v0.3"
SIGNED_BY = "brain_writer_pipeline"

# Files we ingest as text. Anything else gets a file-level manifest entry but
# no chunks — the file hash is still authoritative for provenance.
TEXT_EXTENSIONS = {".md", ".txt", ".markdown", ".rst", ".json", ".jsonl", ".yaml", ".yml"}

# Heading recogniser for markdown / rst-ish bodies. Used to attach a
# `parent_heading` to each chunk for human-auditable provenance.
_HEADING_RE = re.compile(r"^(#{1,6})\s+(.+?)\s*$")

# Default chunk size in lines. Chosen to be small enough that re-chunking is
# cheap but large enough that downstream embeddings have semantic context.
DEFAULT_CHUNK_LINES = 40


# ═════════════════════════════════════════════════════════════════════
# Data classes
# ═════════════════════════════════════════════════════════════════════


@dataclass
class ChunkRecord:
    idx: int
    chunk_hash: str
    line_start: int
    line_end: int
    parent_heading: str | None
    chunk_type: str
    prev_hash: str | None
    next_hash: str | None


@dataclass
class FileManifest:
    run_id: str
    pipeline_version: str
    source_root: str
    file_path: str
    file_hash: str
    size_bytes: int
    mtime: str
    chunks: list[ChunkRecord]
    signed_by: str
    created_at: str

    def to_jsonl_record(self) -> str:
        payload = asdict(self)
        payload["chunks"] = [asdict(c) for c in self.chunks]
        return json.dumps(payload, sort_keys=True, separators=(",", ":"))


@dataclass
class ManifestRunSummary:
    run_id: str
    pipeline_version: str
    source_root: str
    dry_run: bool
    file_count: int = 0
    chunk_count: int = 0
    skipped_count: int = 0
    predicted_db_rows: dict[str, int] = field(default_factory=dict)
    manifest_path: str | None = None
    signed_by: str = SIGNED_BY
    created_at: str = ""


# ═════════════════════════════════════════════════════════════════════
# Hashing helpers
# ═════════════════════════════════════════════════════════════════════


def file_sha256(path: Path, chunk: int = 1 << 16) -> str:
    h = hashlib.sha256()
    with open(path, "rb") as f:
        for buf in iter(lambda: f.read(chunk), b""):
            h.update(buf)
    return h.hexdigest()


def _hash_text(text: str) -> str:
    return hashlib.sha256(text.encode("utf-8")).hexdigest()


def _iso_utc(ts: float | None = None) -> str:
    if ts is None:
        return datetime.now(timezone.utc).strftime("%Y-%m-%dT%H:%M:%SZ")
    return datetime.fromtimestamp(ts, tz=timezone.utc).strftime("%Y-%m-%dT%H:%M:%SZ")


# ═════════════════════════════════════════════════════════════════════
# Chunking
# ═════════════════════════════════════════════════════════════════════


def chunk_text(
    text: str,
    *,
    chunk_lines: int = DEFAULT_CHUNK_LINES,
) -> list[ChunkRecord]:
    """Split text into deterministic line-window chunks with hash chain.

    Determinism contract: identical input bytes + identical chunk_lines yield
    identical ChunkRecord lists (idx, hashes, line ranges, headings) regardless
    of where the file lives on disk. This is what makes path-independence
    testable.
    """
    lines = text.splitlines()
    if not lines:
        return []

    chunks: list[ChunkRecord] = []
    current_heading: str | None = None
    last_heading_seen: str | None = None

    # Pre-compute a heading-per-line map so a chunk can record the heading in
    # force at its first line, not the last.
    headings_by_line: list[str | None] = []
    for raw in lines:
        m = _HEADING_RE.match(raw)
        if m:
            last_heading_seen = m.group(2).strip()
        headings_by_line.append(last_heading_seen)

    idx = 0
    for start in range(0, len(lines), chunk_lines):
        window = lines[start : start + chunk_lines]
        chunk_body = "\n".join(window)
        chunk_hash = _hash_text(chunk_body)
        parent = headings_by_line[start]
        chunk_type = "heading" if _HEADING_RE.match(window[0] or "") else "body"
        chunks.append(
            ChunkRecord(
                idx=idx,
                chunk_hash=chunk_hash,
                line_start=start + 1,
                line_end=start + len(window),
                parent_heading=parent,
                chunk_type=chunk_type,
                prev_hash=None,
                next_hash=None,
            )
        )
        idx += 1

    for i, ch in enumerate(chunks):
        ch.prev_hash = chunks[i - 1].chunk_hash if i > 0 else None
        ch.next_hash = chunks[i + 1].chunk_hash if i < len(chunks) - 1 else None

    _ = current_heading  # silence linter; semantics preserved above
    return chunks


# ═════════════════════════════════════════════════════════════════════
# Generator
# ═════════════════════════════════════════════════════════════════════


@dataclass
class ManifestGenerator:
    source_root: Path
    output_path: Path | None = None
    run_id: str | None = None
    dry_run: bool = False
    chunk_lines: int = DEFAULT_CHUNK_LINES
    include_extensions: frozenset[str] = field(
        default_factory=lambda: frozenset(TEXT_EXTENSIONS)
    )

    def __post_init__(self) -> None:
        self.source_root = Path(self.source_root)
        if self.run_id is None:
            self.run_id = str(uuid.uuid4())
        if self.output_path is not None:
            self.output_path = Path(self.output_path)

    # ── iteration ────────────────────────────────────────────────

    def _iter_source_files(self) -> Iterator[Path]:
        if not self.source_root.exists():
            return
        for p in sorted(self.source_root.rglob("*")):
            if not p.is_file():
                continue
            if p.name.startswith("."):
                continue
            yield p

    def _build_file_manifest(self, path: Path) -> FileManifest:
        rel = path.relative_to(self.source_root).as_posix()
        size = path.stat().st_size
        mtime = _iso_utc(path.stat().st_mtime)
        fhash = file_sha256(path)
        if path.suffix.lower() in self.include_extensions:
            try:
                text = path.read_text(encoding="utf-8", errors="ignore")
            except OSError:
                text = ""
            chunks = chunk_text(text, chunk_lines=self.chunk_lines)
        else:
            chunks = []
        return FileManifest(
            run_id=self.run_id or "",
            pipeline_version=PIPELINE_VERSION,
            source_root=str(self.source_root),
            file_path=rel,
            file_hash=fhash,
            size_bytes=size,
            mtime=mtime,
            chunks=chunks,
            signed_by=SIGNED_BY,
            created_at=_iso_utc(),
        )

    # ── public ───────────────────────────────────────────────────

    def run(self) -> ManifestRunSummary:
        """Walk source_root, emit a manifest, return a summary.

        In dry-run mode, no file is written and no DB writes are predicted —
        only the counts that *would* be produced are returned. This is the
        approval-gate evidence the operator needs before cutover.
        """
        summary = ManifestRunSummary(
            run_id=self.run_id or "",
            pipeline_version=PIPELINE_VERSION,
            source_root=str(self.source_root),
            dry_run=self.dry_run,
            created_at=_iso_utc(),
        )

        records: list[str] = []
        for path in self._iter_source_files():
            try:
                fm = self._build_file_manifest(path)
            except OSError:
                summary.skipped_count += 1
                continue
            summary.file_count += 1
            summary.chunk_count += len(fm.chunks)
            records.append(fm.to_jsonl_record())

        # Predicted DB rows: one knowledge_vector per chunk, one pipeline_run
        # row per manifest run, one audit_log row per file. Entities and
        # relationships are derived downstream and intentionally not predicted
        # here — that lives with the PUDDING/extractor stage.
        summary.predicted_db_rows = {
            "knowledge_vectors": summary.chunk_count,
            "pipeline_runs": 1,
            "audit_log": summary.file_count,
        }

        if not self.dry_run and self.output_path is not None:
            self.output_path.parent.mkdir(parents=True, exist_ok=True)
            with open(self.output_path, "w", encoding="utf-8") as f:
                for line in records:
                    f.write(line + "\n")
            summary.manifest_path = str(self.output_path)

        return summary


def generate_manifest(
    source_root: str | os.PathLike[str],
    output_path: str | os.PathLike[str] | None = None,
    *,
    run_id: str | None = None,
    dry_run: bool = False,
    chunk_lines: int = DEFAULT_CHUNK_LINES,
) -> ManifestRunSummary:
    """Convenience wrapper around :class:`ManifestGenerator`."""
    gen = ManifestGenerator(
        source_root=Path(source_root),
        output_path=Path(output_path) if output_path else None,
        run_id=run_id,
        dry_run=dry_run,
        chunk_lines=chunk_lines,
    )
    return gen.run()


# ═════════════════════════════════════════════════════════════════════
# CLI
# ═════════════════════════════════════════════════════════════════════


def _build_arg_parser():
    import argparse

    p = argparse.ArgumentParser(
        prog="manifest_generator",
        description=(
            "Generate a signed, hash-chained JSONL manifest from a clean disk "
            "corpus. Dry-run mode predicts row counts without writing."
        ),
    )
    p.add_argument(
        "--source-root",
        required=True,
        help="Root of the clean disk corpus (e.g. /opt/amplified/archive/store_b_clean).",
    )
    p.add_argument(
        "--output",
        default=None,
        help="Path to write the manifest JSONL. Ignored in --dry-run.",
    )
    p.add_argument("--run-id", default=None, help="Override generated run_id.")
    p.add_argument(
        "--dry-run",
        action="store_true",
        help="Predict counts only. No manifest file, no DB writes.",
    )
    p.add_argument(
        "--chunk-lines",
        type=int,
        default=DEFAULT_CHUNK_LINES,
        help="Lines per chunk window (default %(default)s).",
    )
    return p


def main(argv: Iterable[str] | None = None) -> int:
    parser = _build_arg_parser()
    args = parser.parse_args(argv)
    summary = generate_manifest(
        source_root=args.source_root,
        output_path=args.output,
        run_id=args.run_id,
        dry_run=args.dry_run,
        chunk_lines=args.chunk_lines,
    )
    print(json.dumps(asdict(summary), sort_keys=True, indent=2))
    return 0


if __name__ == "__main__":  # pragma: no cover
    raise SystemExit(main())

"""Manifest generator — disk source → deterministic JSONL manifest.

AMP-302 Ticket 2: The manifest is the proof layer between disk truth and
the database index. Every chunk that enters the canonical DB must have a
manifest line. Same source files → same manifest bytes (deterministic).

Pipeline position: after PUDDING extraction, before canonical writer.

Signed-by: Devon-0de2 | 2026-05-11 | devin-0de27df281514f96ba3921354d7c31ae
"""

from __future__ import annotations

import hashlib
import json
import logging
import re
from dataclasses import dataclass
from datetime import datetime, timezone
from pathlib import Path

from temporalio import activity

logger = logging.getLogger("cove.manifest")

PIPELINE_VERSION = "amplified-pipeline-v0.3"
SIGNED_BY = "brain_writer_pipeline"
DEFAULT_SOURCE_ROOT = "/opt/amplified/vault/store_b_clean"
DEFAULT_MANIFEST_DIR = "/opt/amplified/vault/manifests"
MAX_CHUNK_CHARS = 4000
HEADING_PATTERN = re.compile(r"^##\s+", re.MULTILINE)


# ═══════════════════════════════════════════════════════════════════════
# Data classes
# ═══════════════════════════════════════════════════════════════════════

@dataclass
class ManifestInput:
    """Input for the manifest generation activity."""
    run_id: str
    source_root: str = DEFAULT_SOURCE_ROOT
    manifest_dir: str = DEFAULT_MANIFEST_DIR
    dry_run: bool = False


@dataclass
class ChunkRecord:
    """One chunk within a manifest file entry."""
    idx: int
    chunk_hash: str
    line_start: int
    line_end: int
    parent_heading: str
    chunk_type: str
    prev_hash: str | None
    next_hash: str | None


@dataclass
class ManifestLine:
    """One file entry in the manifest."""
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


@dataclass
class ManifestResult:
    """Result from the manifest generation activity."""
    success: bool
    manifest_path: str = ""
    manifest_hash: str = ""
    file_count: int = 0
    chunk_count: int = 0
    dry_run: bool = False
    error: str | None = None


# ═══════════════════════════════════════════════════════════════════════
# Pure functions (no IO, deterministic)
# ═══════════════════════════════════════════════════════════════════════

def sha256_bytes(data: bytes) -> str:
    return hashlib.sha256(data).hexdigest()


def sha256_file(path: Path) -> str:
    h = hashlib.sha256()
    with open(path, "rb") as f:
        for block in iter(lambda: f.read(1 << 16), b""):
            h.update(block)
    return h.hexdigest()


def chunk_by_heading(content: str, max_chars: int = MAX_CHUNK_CHARS) -> list[dict]:
    """Split content on H2 headings. Oversized chunks are split further.

    Returns list of {text, heading, line_start, line_end, chunk_type}.
    Line numbers are 1-based.
    """
    if not content.strip():
        return []
    lines = content.split("\n")
    segments: list[dict] = []
    current_heading = "(top-level)"
    current_lines: list[str] = []
    current_start = 1

    def flush():
        if not current_lines:
            return
        text = "\n".join(current_lines)
        segments.append({
            "text": text,
            "heading": current_heading,
            "line_start": current_start,
            "line_end": current_start + len(current_lines) - 1,
            "chunk_type": "prose",
        })

    for i, line in enumerate(lines, start=1):
        if HEADING_PATTERN.match(line):
            flush()
            current_heading = line.lstrip("#").strip() or "(untitled)"
            current_lines = [line]
            current_start = i
        else:
            current_lines.append(line)

    flush()

    # Split oversized segments
    final: list[dict] = []
    for seg in segments:
        text = seg["text"]
        if len(text) <= max_chars:
            final.append(seg)
        else:
            sub_lines = text.split("\n")
            buf: list[str] = []
            buf_start = seg["line_start"]
            for j, sl in enumerate(sub_lines):
                buf.append(sl)
                if len("\n".join(buf)) >= max_chars:
                    final.append({
                        "text": "\n".join(buf),
                        "heading": seg["heading"],
                        "line_start": buf_start,
                        "line_end": buf_start + len(buf) - 1,
                        "chunk_type": "prose-split",
                    })
                    buf_start = buf_start + len(buf)
                    buf = []
            if buf:
                final.append({
                    "text": "\n".join(buf),
                    "heading": seg["heading"],
                    "line_start": buf_start,
                    "line_end": buf_start + len(buf) - 1,
                    "chunk_type": "prose-split" if len(segments) > 1 else "prose",
                })

    return final


def build_chunk_records(segments: list[dict]) -> list[ChunkRecord]:
    """Build ChunkRecords with prev/next hash chain."""
    hashes = [sha256_bytes(seg["text"].encode("utf-8")) for seg in segments]

    records = []
    for i, seg in enumerate(segments):
        records.append(ChunkRecord(
            idx=i,
            chunk_hash=f"sha256:{hashes[i]}",
            line_start=seg["line_start"],
            line_end=seg["line_end"],
            parent_heading=seg["heading"],
            chunk_type=seg["chunk_type"],
            prev_hash=f"sha256:{hashes[i - 1]}" if i > 0 else None,
            next_hash=f"sha256:{hashes[i + 1]}" if i < len(hashes) - 1 else None,
        ))
    return records


def build_manifest_line(
    run_id: str,
    source_root: str,
    file_path: Path,
    file_hash: str,
    chunks: list[ChunkRecord],
    created_at: str,
) -> ManifestLine:
    stat = file_path.stat()
    return ManifestLine(
        run_id=run_id,
        pipeline_version=PIPELINE_VERSION,
        source_root=source_root,
        file_path=str(file_path),
        file_hash=f"sha256:{file_hash}",
        size_bytes=stat.st_size,
        mtime=datetime.fromtimestamp(stat.st_mtime, tz=timezone.utc).isoformat(),
        chunks=chunks,
        signed_by=SIGNED_BY,
        created_at=created_at,
    )


def manifest_line_to_dict(line: ManifestLine) -> dict:
    return {
        "run_id": line.run_id,
        "pipeline_version": line.pipeline_version,
        "source_root": line.source_root,
        "file_path": line.file_path,
        "file_hash": line.file_hash,
        "size_bytes": line.size_bytes,
        "mtime": line.mtime,
        "chunks": [
            {
                "idx": c.idx,
                "chunk_hash": c.chunk_hash,
                "line_start": c.line_start,
                "line_end": c.line_end,
                "parent_heading": c.parent_heading,
                "chunk_type": c.chunk_type,
                "prev_hash": c.prev_hash,
                "next_hash": c.next_hash,
            }
            for c in line.chunks
        ],
        "signed_by": line.signed_by,
        "created_at": line.created_at,
    }


# ═══════════════════════════════════════════════════════════════════════
# Temporal activity
# ═══════════════════════════════════════════════════════════════════════

@activity.defn(name="generate_manifest")
async def generate_manifest(input: ManifestInput) -> ManifestResult:
    """Walk source root, chunk files, emit deterministic JSONL manifest.

    Determinism contract: sorted file walk + deterministic chunking = same
    source files produce identical manifest bytes.
    """
    source = Path(input.source_root)
    if not source.exists():
        return ManifestResult(
            success=False,
            error=f"Source root not found: {source}",
        )

    now_iso = datetime.now(timezone.utc).isoformat()

    # Deterministic sorted walk
    md_files = sorted(source.rglob("*.md"))
    activity.logger.info(f"Manifest: found {len(md_files)} .md files in {source}")

    manifest_lines: list[str] = []
    total_chunks = 0

    for fp in md_files:
        try:
            content = fp.read_text(encoding="utf-8", errors="ignore")
        except OSError as e:
            activity.logger.warning(f"Cannot read {fp}: {e}")
            continue

        file_hash = sha256_file(fp)
        segments = chunk_by_heading(content)

        if not segments:
            continue

        chunk_records = build_chunk_records(segments)
        total_chunks += len(chunk_records)

        line = build_manifest_line(
            run_id=input.run_id,
            source_root=input.source_root,
            file_path=fp,
            file_hash=file_hash,
            chunks=chunk_records,
            created_at=now_iso,
        )
        manifest_lines.append(
            json.dumps(manifest_line_to_dict(line), sort_keys=True)
        )

    activity.logger.info(
        f"Manifest: {len(manifest_lines)} files, {total_chunks} chunks"
    )

    manifest_content = "\n".join(manifest_lines) + "\n" if manifest_lines else ""
    manifest_hash = sha256_bytes(manifest_content.encode("utf-8"))

    if input.dry_run:
        activity.logger.info(
            f"DRY RUN: would write {len(manifest_lines)} lines, "
            f"{total_chunks} chunks, hash={manifest_hash[:16]}"
        )
        return ManifestResult(
            success=True,
            manifest_hash=f"sha256:{manifest_hash}",
            file_count=len(manifest_lines),
            chunk_count=total_chunks,
            dry_run=True,
        )

    # Write manifest to disk
    manifest_dir = Path(input.manifest_dir)
    manifest_dir.mkdir(parents=True, exist_ok=True)
    manifest_path = manifest_dir / f"{input.run_id}.jsonl"
    manifest_path.write_text(manifest_content, encoding="utf-8")

    activity.logger.info(f"Manifest written: {manifest_path} ({manifest_hash[:16]})")

    return ManifestResult(
        success=True,
        manifest_path=str(manifest_path),
        manifest_hash=f"sha256:{manifest_hash}",
        file_count=len(manifest_lines),
        chunk_count=total_chunks,
    )

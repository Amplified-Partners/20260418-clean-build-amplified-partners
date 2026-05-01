#!/usr/bin/env python3
"""
Sidecar-to-Label adapter — routes non-harvest content into the PUDDING Labeler.

Pipeline position:  [External sources] --> [this adapter] --> Label

"Sidecar" content is anything that enters the APDS pipeline outside the normal
Harvest stage: vault documents, MCP server outputs, manual drops, CRM
extractions, marketing engine artefacts, or ad-hoc files placed on the Porch.

This adapter normalises sidecar inputs into HarvestRecords (the same shape
used by harvest_to_label) then labels them, so downstream stages (Match, Score,
Graph) see a uniform interface regardless of origin.

Supported sidecar sources:
    - File paths (single file or directory)
    - Raw text blobs (programmatic callers)
    - Vault-format markdown (YAML frontmatter + body)
    - Dict/JSON payloads from MCP servers or API responses

Usage:
    from sidecar_to_label import label_file, label_text, label_vault_doc

    # Single file
    record = label_file("/path/to/doc.md", source="vault")

    # Raw text from an MCP tool
    record = label_text(title="CRM Insight", content="...", source="mcp:crm-search")

    # Vault doc with frontmatter
    record = label_vault_doc("/path/to/vault/doc.md")

Signed-by: Devon (Devin session f32d587cc3e54f959c5309d93f72bc97) - 2026-05-01
"""

from __future__ import annotations

import hashlib
import json
import logging
import re
from dataclasses import field
from datetime import datetime, timezone
from pathlib import Path
from typing import Any

try:
    from .harvest_to_label import (
        HarvestRecord,
        LabeledRecord,
        label_harvested_item,
    )
except ImportError:
    from harvest_to_label import (  # type: ignore[no-redef]
        HarvestRecord,
        LabeledRecord,
        label_harvested_item,
    )

logger = logging.getLogger("apds.sidecar_to_label")


# ---------------------------------------------------------------------------
# Vault frontmatter parser (lightweight, no PyYAML dependency)
# ---------------------------------------------------------------------------

_FRONTMATTER_RE = re.compile(r"^---\s*\n(.*?)\n---\s*\n", re.DOTALL)
_KV_RE = re.compile(r"^(\w[\w\-]*):\s*(.+)$", re.MULTILINE)


def _parse_frontmatter(text: str) -> tuple[dict[str, str], str]:
    """Extract YAML-ish frontmatter from a markdown document.

    Returns (metadata_dict, body_without_frontmatter).
    Uses regex rather than PyYAML to avoid an external dependency.
    """
    match = _FRONTMATTER_RE.match(text)
    if not match:
        return {}, text

    raw = match.group(1)
    body = text[match.end():]
    meta: dict[str, str] = {}
    for kv in _KV_RE.finditer(raw):
        key = kv.group(1).strip()
        val = kv.group(2).strip().strip('"').strip("'")
        meta[key] = val

    return meta, body


# ---------------------------------------------------------------------------
# Sidecar entry points
# ---------------------------------------------------------------------------

def label_text(
    *,
    title: str,
    content: str,
    source: str = "sidecar",
    source_tier: str = "T1",
    metadata: dict[str, Any] | None = None,
) -> LabeledRecord:
    """Label a raw text blob from any programmatic source.

    This is the lowest-level entry point. All other sidecar functions
    ultimately call this.
    """
    external_id = hashlib.sha256(f"{title}:{content[:200]}".encode()).hexdigest()[:16]
    record = HarvestRecord(
        source_name=source,
        external_id=external_id,
        title=title,
        content=content,
        source_tier=source_tier,
        metadata=metadata or {"origin": "sidecar", "source": source},
    )
    return label_harvested_item(record, source_tier=source_tier)


def label_file(
    filepath: str | Path,
    *,
    source: str = "sidecar:file",
    source_tier: str = "T1",
) -> LabeledRecord:
    """Label a single file from the filesystem."""
    p = Path(filepath)
    if not p.is_file():
        raise FileNotFoundError(f"Sidecar file not found: {p}")

    content = p.read_text(encoding="utf-8", errors="replace")
    title = p.stem.replace("-", " ").replace("_", " ").title()

    return label_text(
        title=title,
        content=content,
        source=source,
        source_tier=source_tier,
        metadata={"origin": "sidecar:file", "filename": p.name, "path": str(p)},
    )


def label_vault_doc(
    filepath: str | Path,
    *,
    source_tier: str = "T1",
) -> LabeledRecord:
    """Label a vault-format markdown document (YAML frontmatter + body).

    Extracts frontmatter metadata (title, type, tags, date) and uses it
    to enrich the HarvestRecord before labeling.
    """
    p = Path(filepath)
    if not p.is_file():
        raise FileNotFoundError(f"Vault document not found: {p}")

    raw = p.read_text(encoding="utf-8", errors="replace")
    meta, body = _parse_frontmatter(raw)

    title = meta.get("title", p.stem.replace("-", " ").replace("_", " ").title())
    doc_type = meta.get("type", "unknown")
    tags = meta.get("tags", "")
    date_str = meta.get("date", "")

    published_at = None
    if date_str:
        try:
            parsed = datetime.fromisoformat(date_str)
            published_at = parsed if parsed.tzinfo else parsed.replace(tzinfo=timezone.utc)
        except ValueError:
            pass

    record = HarvestRecord(
        source_name=f"vault:{doc_type}",
        external_id=hashlib.sha256(p.name.encode()).hexdigest()[:16],
        title=title,
        content=body,
        published_at=published_at,
        source_tier=source_tier,
        metadata={
            "origin": "vault",
            "filename": p.name,
            "path": str(p),
            "frontmatter": meta,
            "doc_type": doc_type,
            "tags": tags,
        },
    )
    return label_harvested_item(record, source_tier=source_tier)


def label_dict(
    payload: dict[str, Any],
    *,
    source: str = "sidecar:api",
    source_tier: str = "T1",
) -> LabeledRecord:
    """Label a dict/JSON payload from an MCP server or API response.

    Expected keys: ``title``, ``content`` (required). Optional: ``url``,
    ``source_name``, ``metadata``.
    """
    title = payload.get("title", "Untitled")
    content = payload.get("content", "")
    if not content:
        raise ValueError("Payload must include non-empty 'content' field")

    return label_text(
        title=title,
        content=content,
        source=payload.get("source_name", source),
        source_tier=source_tier,
        metadata=payload.get("metadata", {"origin": source}),
    )


# ---------------------------------------------------------------------------
# Batch: label all files in a directory (vault scan, corpus import, etc.)
# ---------------------------------------------------------------------------

SUPPORTED_EXTENSIONS = {".md", ".txt", ".json", ".yaml", ".yml", ".csv"}


def label_sidecar_directory(
    directory: str | Path,
    *,
    source: str = "sidecar:directory",
    source_tier: str = "T1",
    vault_mode: bool = False,
    output_jsonl: str | Path | None = None,
) -> list[LabeledRecord]:
    """Label all supported files in a directory.

    If ``vault_mode`` is True, treats files as vault documents with
    YAML frontmatter.
    """
    dirpath = Path(directory)
    if not dirpath.is_dir():
        raise FileNotFoundError(f"Sidecar directory not found: {dirpath}")

    files = sorted(
        f for f in dirpath.iterdir()
        if f.is_file() and f.suffix in SUPPORTED_EXTENSIONS
    )

    if not files:
        logger.info("No sidecar files in %s", dirpath)
        return []

    logger.info("Labeling %d sidecar files from %s", len(files), dirpath)
    results: list[LabeledRecord] = []

    for filepath in files:
        try:
            if vault_mode:
                labeled = label_vault_doc(filepath, source_tier=source_tier)
            else:
                labeled = label_file(filepath, source=source, source_tier=source_tier)
            results.append(labeled)
            logger.debug("  [%s] %s", labeled.pudding_label, filepath.name)
        except Exception as exc:
            logger.warning("Failed to label %s: %s", filepath.name, exc)

    if output_jsonl:
        out = Path(output_jsonl)
        out.parent.mkdir(parents=True, exist_ok=True)
        with open(out, "a", encoding="utf-8") as f:
            for r in results:
                f.write(json.dumps(r.to_dict(), default=str) + "\n")
        logger.info("Wrote %d records to %s", len(results), out)

    return results


# ---------------------------------------------------------------------------
# CLI
# ---------------------------------------------------------------------------

if __name__ == "__main__":
    import argparse

    logging.basicConfig(level=logging.INFO, format="%(name)s %(levelname)s %(message)s")

    parser = argparse.ArgumentParser(description="APDS Sidecar-to-Label adapter")
    parser.add_argument("path", help="File or directory to label")
    parser.add_argument("--source", default="sidecar:cli", help="Source identifier")
    parser.add_argument("--tier", default="T1", help="Source tier (T1-T4)")
    parser.add_argument("--vault", action="store_true", help="Treat files as vault docs with frontmatter")
    parser.add_argument("--output", help="JSONL output file")
    args = parser.parse_args()

    target = Path(args.path)
    if target.is_file():
        if args.vault:
            result = label_vault_doc(target, source_tier=args.tier)
        else:
            result = label_file(target, source=args.source, source_tier=args.tier)
        print(f"[{result.pudding_label}] {result.harvest.title}")
    elif target.is_dir():
        results = label_sidecar_directory(
            target,
            source=args.source,
            source_tier=args.tier,
            vault_mode=args.vault,
            output_jsonl=args.output,
        )
        print(f"\nLabeled {len(results)} sidecar items:")
        for r in results:
            print(f"  [{r.pudding_label}] {r.harvest.title}")
    else:
        print(f"Error: {target} not found")
        raise SystemExit(1)

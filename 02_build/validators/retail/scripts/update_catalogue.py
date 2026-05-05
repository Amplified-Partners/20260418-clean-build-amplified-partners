#!/usr/bin/env python3
# Authored by Devon-9a6b, 2026-05-03 (session devin-9a6bd256bd7c4a90a083a471fa94a810)
"""Append a VALIDATION: line to each retail entry in the insight catalogue.

The line is appended *after* the existing STATUS: line and *before* the next
horizontal rule ('---'). Existing fields are not modified — this is purely
additive, in line with the additive-edit policy in 00_authority/AGENTS.md.

Idempotent: running twice updates the existing VALIDATION: line rather than
duplicating it.

Usage:
  PYTHONPATH=02_build python -m validators.retail.scripts.update_catalogue
"""
from __future__ import annotations

import json
import re
import sys
from pathlib import Path

REPO = Path(__file__).resolve().parents[4]
CATALOGUE = REPO / "01_truth" / "schemas" / "research-index" / "00-insight-catalogue_v1.md"
RESULTS = Path(__file__).resolve().parents[1] / "results"


def _verdict_for(ins_id: str) -> dict | None:
    p = RESULTS / ins_id / "verdict.json"
    if not p.exists():
        return None
    return json.loads(p.read_text())


def _format_validation_line(v: dict) -> str:
    # signed_by is a full SIGNATURES.md signature ("<agent> | <date> | <session>")
    # when AMP_SIGNED_BY is set (the conventional shape). The catalogue line
    # already carries `run=<date>` so the date+session would just duplicate; show
    # the leading agent token only here. Full sig still lives in verdict.json.
    raw_signed_by = v.get("signed_by", "unknown")
    agent = raw_signed_by.split("|", 1)[0].strip()
    bits = [
        f"verdict={v['verdict']}",
        f"test={v['test_class']}",
        f"conf={v.get('confidence', 0)}",
        f"run={v.get('run_at_utc', '?')[:10]}",
        f"signed_by={agent}",
    ]
    return f"**VALIDATION (AMP-66):** {' | '.join(bits)} — {v['summary']}"


def main() -> int:
    text = CATALOGUE.read_text()
    # Use [ \t]* (NOT \s*) so the trailing newline after '---' is preserved
    # in the chunk that follows it. Otherwise '---'.join(chunks) eats blank
    # lines and corrupts catalogue formatting.
    entries = re.split(r"^---[ \t]*$", text, flags=re.MULTILINE)
    out_chunks: list[str] = []
    updated = 0
    skipped = 0

    for chunk in entries:
        m_id = re.search(r"^\*\*ID:\*\*\s*(INS-\d+)", chunk, re.MULTILINE)
        m_v = re.search(r"^\*\*VERTICAL:\*\*\s*(\w+)", chunk, re.MULTILINE)
        if not (m_id and m_v):
            out_chunks.append(chunk)
            continue
        ins_id = m_id.group(1)
        if m_v.group(1).lower() != "retail":
            out_chunks.append(chunk)
            continue
        verdict = _verdict_for(ins_id)
        if not verdict:
            out_chunks.append(chunk)
            skipped += 1
            continue
        line = _format_validation_line(verdict)

        # Replace any existing VALIDATION line; otherwise append after STATUS line.
        # Use lambdas for the replacement so the summary text in `line` is
        # never interpreted as a backreference (e.g. a literal '\1' in the
        # summary would otherwise be expanded by re.sub).
        if re.search(r"^\*\*VALIDATION \(AMP-66\):\*\*", chunk, re.MULTILINE):
            new_chunk = re.sub(
                r"^\*\*VALIDATION \(AMP-66\):\*\* .*$",
                lambda _m: line,
                chunk,
                count=1,
                flags=re.MULTILINE,
            )
        else:
            status_pat = re.compile(r"(^\*\*STATUS:\*\* [\w\-]+)", re.MULTILINE)
            if status_pat.search(chunk):
                new_chunk = status_pat.sub(lambda m: m.group(1) + "\n" + line, chunk, count=1)
            else:
                new_chunk = chunk.rstrip() + f"\n{line}\n"

        out_chunks.append(new_chunk)
        updated += 1

    CATALOGUE.write_text("---".join(out_chunks))
    print(f"updated {updated} retail entries; skipped {skipped} (missing verdict)")
    return 0


if __name__ == "__main__":
    sys.exit(main())

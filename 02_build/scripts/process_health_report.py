#!/usr/bin/env python3
"""
Process health metrics for governed handovers (signal for the system, not blame).

Scans 03_shadow/job-wrapups/*_wrapup.md for:
  - YAML status (finished / paused / parked / handed-off)
  - Heuristic completeness of SOP minimum prompts (headings / keywords)

Exit 0 always; prints markdown to stdout. Intended for:
  - GitHub Actions (append to GITHUB_STEP_SUMMARY)
  - Local: python3 02_build/scripts/process_health_report.py
"""

from __future__ import annotations

import argparse
import re
import sys
from collections import Counter
from datetime import date, timedelta
from pathlib import Path


WRAPUP_GLOB = "*_wrapup.md"
FRONTMATTER_STATUS = re.compile(r"(?m)^status:\s*([^\s#]+)")
DATE_PREFIX = re.compile(r"^(\d{4}-\d{2}-\d{2})_.*\.md$")

# Heuristic markers aligned to SOP minimum prompts (presence, not quality).
CHECKS: tuple[tuple[str, re.Pattern[str]], ...] = (
    ("resume_instruction", re.compile(r"resume\s+instruction", re.I)),
    ("current_state", re.compile(r"current\s+state", re.I)),
    ("negative_signals", re.compile(r"negative\s+signals|repulsion\s+score", re.I)),
    ("smallest_next_step", re.compile(r"smallest\s+next\s+step", re.I)),
    ("baton_pass_test", re.compile(r"baton\s+pass\s+test", re.I)),
)


def parse_args() -> argparse.Namespace:
    p = argparse.ArgumentParser(description=__doc__)
    p.add_argument(
        "--repo-root",
        type=Path,
        default=Path(__file__).resolve().parents[2],
        help="Repository root (default: parent of 02_build/)",
    )
    p.add_argument(
        "--window-days",
        type=int,
        default=14,
        help="Rolling window from today (UTC date) for filename-dated wrapups",
    )
    p.add_argument(
        "--wrapup-dir",
        type=str,
        default="03_shadow/job-wrapups",
        help="Relative path to wrapups directory",
    )
    return p.parse_args()


def filename_date(path: Path) -> date | None:
    m = DATE_PREFIX.match(path.name)
    if not m:
        return None
    try:
        y, mo, d = (int(x) for x in m.group(1).split("-"))
        return date(y, mo, d)
    except ValueError:
        return None


def frontmatter_status(text: str) -> str | None:
    if not text.startswith("---"):
        return None
    end = text.find("\n---", 3)
    if end == -1:
        return None
    block = text[3:end]
    m = FRONTMATTER_STATUS.search(block)
    return m.group(1).strip().lower() if m else None


def score_checks(text: str) -> tuple[int, list[str]]:
    missing: list[str] = []
    passed = 0
    for key, pat in CHECKS:
        if pat.search(text):
            passed += 1
        else:
            missing.append(key)
    return passed, missing


def main() -> int:
    args = parse_args()
    root: Path = args.repo_root
    wrap_dir = root / args.wrapup_dir
    if not wrap_dir.is_dir():
        print(f"# Process health report\n\n**Error:** `{wrap_dir}` not found.")
        return 0

    today = date.today()
    cutoff = today - timedelta(days=args.window_days)

    wrapups = sorted(wrap_dir.glob(WRAPUP_GLOB))
    in_window: list[Path] = []
    for p in wrapups:
        fd = filename_date(p)
        if fd is not None and fd >= cutoff:
            in_window.append(p)

    status_counts: Counter[str] = Counter()
    rows: list[tuple[str, str | None, int, int, str]] = []

    for path in in_window:
        text = path.read_text(encoding="utf-8", errors="replace")
        st = frontmatter_status(text)
        if st:
            status_counts[st] += 1
        passed, missing = score_checks(text)
        score_pct = int(round(100 * passed / len(CHECKS)))
        rows.append(
            (
                path.name,
                st,
                passed,
                score_pct,
                ", ".join(missing) if missing else "",
            )
        )

    avg_pct = (
        int(round(sum(r[3] for r in rows) / len(rows))) if rows else None
    )

    lines: list[str] = []
    lines.append("# Process health (handover discipline)")
    lines.append("")
    lines.append("**Interpretation:** This measures whether **wrapup artifacts**")
    lines.append("exist and carry **SOP-shaped signals** in a time window. Low")
    lines.append("scores usually mean **process friction** (time, template drift,")
    lines.append("unclear ownership), not individual fault.")
    lines.append("")
    lines.append(f"- **Repo root:** `{root}`")
    lines.append(f"- **Window:** last **{args.window_days}** days (filename date)")
    lines.append(f"- **Wrapups in window:** {len(rows)}")
    if avg_pct is not None:
        lines.append(f"- **Mean heuristic completeness:** **{avg_pct}%**")
    else:
        lines.append("- **Mean heuristic completeness:** _n/a (no wrapups)_")
    if status_counts:
        lines.append("- **Frontmatter `status` in window:**")
        for k, v in sorted(status_counts.items(), key=lambda kv: (-kv[1], kv[0])):
            lines.append(f"  - `{k}`: {v}")
    lines.append("")
    lines.append("## Checks (heuristic)")
    lines.append("")
    lines.append("| Key | Meaning |")
    lines.append("|-----|---------|")
    for key, pat in CHECKS:
        lines.append(f"| `{key}` | pattern `{pat.pattern}` |")
    lines.append("")
    lines.append("## Per-file (window)")
    lines.append("")
    lines.append("| File | status | checks | % | missing keys |")
    lines.append("|------|--------|--------|---|----------------|")
    for name, st, passed, pct, miss in rows:
        st_s = f"`{st}`" if st else "_none_"
        miss_s = miss.replace("|", "\\|") if miss else "_—_"
        lines.append(f"| `{name}` | {st_s} | {passed}/{len(CHECKS)} | {pct} | {miss_s} |")
    if not rows:
        lines.append("| _none_ | | | | |")
    lines.append("")
    lines.append("## Exception notes")
    exc = sorted(wrap_dir.glob("*_wrapup-exception.md"))
    recent_exc = [p for p in exc if (d := filename_date(p)) and d >= cutoff]
    lines.append(f"- **Total `*_wrapup-exception.md`:** {len(exc)}")
    lines.append(f"- **In window:** {len(recent_exc)}")
    lines.append("")

    sys.stdout.write("\n".join(lines))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())

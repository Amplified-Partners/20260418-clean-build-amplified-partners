# Authored by Devon-9a6b, 2026-05-03 (session devin-9a6bd256bd7c4a90a083a471fa94a810)
"""Retail-vertical validator CLI.

Usage:
  python -m validators.retail.cli list
  python -m validators.retail.cli run [--ins INS-067 INS-073 ...]
  python -m validators.retail.cli summary
  python -m validators.retail.cli ticket-comment

Run from repo root with `PYTHONPATH=02_build` so the validators package is importable.
"""
from __future__ import annotations

import argparse
import json
import sys
import time
from collections import Counter

from .insights import INSIGHTS
from .verdict import RESULTS_ROOT, Verdict


def _list() -> int:
    print("retail-vertical insights (catalogue order):")
    for ins_id, runner in INSIGHTS.items():
        print(f"  {ins_id}  {runner.__module__}")
    print(f"\ntotal: {len(INSIGHTS)}")
    return 0


def _run(insight_ids: list[str] | None) -> int:
    targets = insight_ids or list(INSIGHTS.keys())
    missing = [t for t in targets if t not in INSIGHTS]
    if missing:
        print(f"unknown insight ids: {missing}", file=sys.stderr)
        return 2

    print(f"running {len(targets)} insight(s)...")
    out: list[Verdict] = []
    for ins in targets:
        t0 = time.time()
        try:
            v = INSIGHTS[ins]()
        except Exception as e:
            # Runtime crash. NOT a DEFERRED (which is reserved for explicit
            # policy refusal — ToS-bound scraping, legal review pending —
            # and would otherwise contaminate the headline DEFERRED count
            # that should only ever reflect deliberate refusals like
            # INS-077). Per the schema doc 2026-05_public-data-validation_v1
            # § "Three bands", BLOCKED = "validation cannot be attempted in
            # the current environment" — a runtime exception (network down,
            # source returned malformed payload, missing dependency) is
            # exactly that.
            v = Verdict(
                insight_id=ins,
                title="(error)",
                vertical="Retail",
                verdict="BLOCKED",
                test_class="error",
                summary=f"runner raised {type(e).__name__}: {e}",
                evidence=[{"test": "error", "exception": repr(e)}],
                notes=[f"runner failed: {e}"],
                confidence=0,
            )
        path = v.write()
        elapsed = time.time() - t0
        print(f"  {ins} -> {v.verdict:<9}  ({elapsed:5.1f}s)  {path.relative_to(RESULTS_ROOT.parent)}")
        out.append(v)

    counts = Counter(v.verdict for v in out)
    print("\nsummary:")
    for band in ("PROVEN", "PLAUSIBLE", "DISPROVEN", "DEFERRED", "BLOCKED"):
        if counts.get(band):
            print(f"  {band:<9}  {counts[band]:>3}")
    print(f"  total      {len(out):>3}")
    return 0


def _summary() -> int:
    rows: list[dict] = []
    for ins_id in INSIGHTS:
        path = RESULTS_ROOT / ins_id / "verdict.json"
        if path.exists():
            rows.append(json.loads(path.read_text()))
    if not rows:
        print("no verdicts yet — run `python -m validators.retail.cli run` first")
        return 1
    print(f"{'INS':<8} {'VERDICT':<9} {'CONF':<5} TITLE")
    print("-" * 100)
    for r in rows:
        print(f"{r['insight_id']:<8} {r['verdict']:<9} {r.get('confidence', 0):<5} {r['title'][:80]}")
    counts = Counter(r["verdict"] for r in rows)
    print()
    for band in ("PROVEN", "PLAUSIBLE", "DISPROVEN", "DEFERRED", "BLOCKED"):
        if counts.get(band):
            print(f"  {band:<9}  {counts[band]:>3}")
    print(f"  total      {len(rows):>3}")
    return 0


def _ticket_comment() -> int:
    """Render a markdown summary suitable for posting back to Linear AMP-66."""
    rows: list[dict] = []
    for ins_id in INSIGHTS:
        path = RESULTS_ROOT / ins_id / "verdict.json"
        if path.exists():
            rows.append(json.loads(path.read_text()))
    if not rows:
        print("no verdicts yet")
        return 1
    counts = Counter(r["verdict"] for r in rows)
    proven = [r for r in rows if r["verdict"] == "PROVEN"]
    plausible = [r for r in rows if r["verdict"] == "PLAUSIBLE"]
    disproven = [r for r in rows if r["verdict"] == "DISPROVEN"]
    deferred = [r for r in rows if r["verdict"] == "DEFERRED"]
    blocked = [r for r in rows if r["verdict"] == "BLOCKED"]

    headline = (
        f"verdicts: PROVEN={counts.get('PROVEN', 0)} / "
        f"PLAUSIBLE={counts.get('PLAUSIBLE', 0)} / "
        f"DISPROVEN={counts.get('DISPROVEN', 0)} / "
        f"DEFERRED={counts.get('DEFERRED', 0)}"
    )
    if counts.get("BLOCKED"):
        headline += f" / BLOCKED={counts['BLOCKED']}"
    headline += f" (total {len(rows)})"

    out = [
        "**AMP-66 — retail vertical validation**",
        "",
        headline,
        "",
    ]
    for label, group in [
        ("PROVEN", proven),
        ("PLAUSIBLE", plausible),
        ("DISPROVEN", disproven),
        ("DEFERRED", deferred),
        ("BLOCKED", blocked),
    ]:
        if not group:
            continue
        out.append(f"**{label}**")
        for r in group:
            out.append(f"- `{r['insight_id']}` — {r['title'][:90]} — {r['summary'][:160]}")
        out.append("")
    out.append("Signed, **Devon-9a6b** | 2026-05-03 | devin-9a6bd256bd7c4a90a083a471fa94a810")
    print("\n".join(out))
    return 0


def main() -> int:
    parser = argparse.ArgumentParser(prog="validators.retail.cli")
    sub = parser.add_subparsers(dest="cmd", required=True)
    sub.add_parser("list")
    pr = sub.add_parser("run")
    pr.add_argument("--ins", nargs="*", help="restrict to specific INS-NNN ids")
    sub.add_parser("summary")
    sub.add_parser("ticket-comment")
    args = parser.parse_args()
    if args.cmd == "list":
        return _list()
    if args.cmd == "run":
        return _run(args.ins)
    if args.cmd == "summary":
        return _summary()
    if args.cmd == "ticket-comment":
        return _ticket_comment()
    return 1


if __name__ == "__main__":
    raise SystemExit(main())

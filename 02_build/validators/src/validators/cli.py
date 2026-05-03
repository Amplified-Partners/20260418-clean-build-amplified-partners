# Authored by Devon-6264, 2026-05-03 (session devin-6264b0ba42c6453b86b166bebc3d868a)
"""Validators CLI.

    python -m validators run --vertical trades
    python -m validators run --insight INS-006
    python -m validators report --vertical trades
"""

from __future__ import annotations

import argparse
import json
import logging
import sys
from collections.abc import Iterable

from . import core
from .core import RESULTS_DIR, Verdict, VerdictBand
from .insights import TRADES_PILOT, runner_for

logger = logging.getLogger("validators.cli")


def _vertical_ids(vertical: str) -> list[str]:
    if vertical.lower() == "trades":
        return list(TRADES_PILOT)
    raise SystemExit(f"unknown vertical: {vertical}")


def _run_ids(ids: Iterable[str]) -> list[Verdict]:
    verdicts: list[Verdict] = []
    for insight_id in ids:
        try:
            runner = runner_for(insight_id)
        except ModuleNotFoundError:
            logger.warning("no module for %s — skipping", insight_id)
            continue
        try:
            verdict = runner()
        except Exception as exc:  # noqa: BLE001
            logger.exception("%s raised", insight_id)
            verdict = Verdict(
                insight_id=insight_id,
                verdict=VerdictBand.SKIPPED,
                test_class="error",
                evidence=core.Evidence(notes=f"runner crashed: {exc!r}"),
                reason=f"crash:{type(exc).__name__}",
            )
            verdict.write()
        verdicts.append(verdict)
        print(
            f"{verdict.insight_id}  {verdict.verdict.value:<10}  "
            f"{verdict.test_class:<14}  {verdict.evidence.metric or verdict.reason}"
        )
    return verdicts


def _cmd_run(args: argparse.Namespace) -> int:
    if args.insight:
        ids = [args.insight.upper()]
    else:
        ids = _vertical_ids(args.vertical or "trades")
    _run_ids(ids)
    return 0


def _cmd_report(args: argparse.Namespace) -> int:
    ids = _vertical_ids(args.vertical or "trades")
    rows: list[dict[str, str]] = []
    for insight_id in ids:
        path = RESULTS_DIR / f"{insight_id}.json"
        if not path.exists():
            rows.append({"id": insight_id, "verdict": "—", "metric": "(no result file)"})
            continue
        data = json.loads(path.read_text())
        rows.append(
            {
                "id": insight_id,
                "verdict": data.get("verdict", "—"),
                "metric": (data.get("evidence", {}) or {}).get("metric", ""),
            }
        )
    print("# Trades Validation Report\n")
    print("| Insight | Verdict | Metric |")
    print("|---------|---------|--------|")
    for row in rows:
        print(f"| {row['id']} | {row['verdict']} | {row['metric'][:120]} |")
    return 0


def _cmd_apply(args: argparse.Namespace) -> int:
    """Write the VALIDATION: line into the catalogue for each result file."""
    ids = _vertical_ids(args.vertical or "trades") if not args.insight else [args.insight.upper()]
    written = 0
    for insight_id in ids:
        path = RESULTS_DIR / f"{insight_id}.json"
        if not path.exists():
            continue
        data = json.loads(path.read_text())
        verdict = data.get("verdict", "")
        if verdict not in (VerdictBand.PROVEN.value, VerdictBand.PLAUSIBLE.value, VerdictBand.DISPROVEN.value):
            continue
        evidence = data.get("evidence", {}) or {}
        metric = evidence.get("metric", "").replace("|", "/")
        line = (
            f"**VALIDATION:** {verdict} | test_class={data.get('test_class', '')} | "
            f"metric=\"{metric[:240]}\" | evidence=03_shadow/validators/{insight_id}/ | "
            f"run={data.get('verdict_at', '')}"
        )
        if core.upsert_validation_line(insight_id, line):
            print(f"updated {insight_id}")
            written += 1
        else:
            print(f"unchanged {insight_id}")
    print(f"\n{written} insight blocks updated in {core.CATALOGUE_PATH.name}")
    return 0


def main(argv: list[str] | None = None) -> int:
    logging.basicConfig(level=logging.INFO, format="%(levelname)s %(name)s %(message)s")
    parser = argparse.ArgumentParser(prog="ap-validators")
    sub = parser.add_subparsers(dest="cmd", required=True)

    p_run = sub.add_parser("run", help="run validators and write verdicts")
    p_run.add_argument("--vertical", default="trades")
    p_run.add_argument("--insight", help="single insight id (e.g. INS-006)")
    p_run.set_defaults(func=_cmd_run)

    p_report = sub.add_parser("report", help="markdown summary of latest verdicts")
    p_report.add_argument("--vertical", default="trades")
    p_report.set_defaults(func=_cmd_report)

    p_apply = sub.add_parser("apply", help="write VALIDATION: lines back into the catalogue")
    p_apply.add_argument("--vertical", default="trades")
    p_apply.add_argument("--insight", help="single insight id")
    p_apply.set_defaults(func=_cmd_apply)

    args = parser.parse_args(argv)
    return args.func(args)


def __main__() -> None:  # pragma: no cover
    sys.exit(main())


if __name__ == "__main__":  # pragma: no cover
    sys.exit(main())

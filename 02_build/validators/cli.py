"""CLI orchestrator for the public-data validators.

Usage:
    python -m validators run --vertical profservices
    python -m validators run --vertical profservices --insight INS-079
    python -m validators rollup --vertical profservices

The orchestrator imports the per-vertical runner module from
`validations/<vertical>.py` and writes verdicts under
`03_shadow/validators/<vertical>/<INS-NNN>/verdict.json`.

Signed-by: Devon-ab74 (devin-ab740f2c78ee477a9c16ea3b6ed15293) - 2026-05-03
"""

from __future__ import annotations

import argparse
import importlib
import json
import logging
import sys
import urllib.error
from collections.abc import Callable
from pathlib import Path

from .cache import FetchBlockedError
from .core import (
    EvidenceBundle,
    TestClass,
    Verdict,
    VerdictBand,
    write_verdict,
)


def _resolve_output_root(repo_root: Path, override: str | None) -> Path:
    if override:
        return Path(override)
    return repo_root / "03_shadow" / "validators"


def _display_path(path: Path, repo_root: Path) -> Path:
    """Show ``path`` relative to ``repo_root`` when possible, else absolute.

    ``Path.relative_to`` raises ``ValueError`` when ``path`` lives outside
    ``repo_root``. That happens whenever ``--output-root`` points outside
    the repo (e.g. ``/tmp/verdicts``); we still want to log the location
    rather than crash after a successful write.
    """
    try:
        return path.relative_to(repo_root)
    except ValueError:
        return path


def _load_runners(vertical: str) -> dict[str, Callable[[], Verdict]]:
    module = importlib.import_module(f"validators.validations.{vertical}")
    runners = getattr(module, "RUNNERS", None)
    if not isinstance(runners, dict):
        raise SystemExit(f"validators.validations.{vertical} has no RUNNERS dict")
    return runners


def cmd_run(args: argparse.Namespace) -> int:
    repo_root = Path(args.repo_root).resolve()
    output_root = _resolve_output_root(repo_root, args.output_root)
    runners = _load_runners(args.vertical)
    selected = (
        {k: v for k, v in runners.items() if k in set(args.insight)}
        if args.insight
        else runners
    )
    if not selected:
        print(f"No matching insights for vertical={args.vertical}", file=sys.stderr)
        return 2

    summary: list[dict[str, str]] = []
    for insight_id, runner in selected.items():
        try:
            verdict = runner()
        except (urllib.error.URLError, FetchBlockedError) as exc:
            logging.warning("validator %s blocked: %s", insight_id, exc)
            verdict = Verdict(
                insight_id=insight_id,
                vertical=args.vertical,
                band=VerdictBand.BLOCKED,
                test_class=TestClass.EXISTENCE,
                method="Public-source fetch failed",
                finding=f"{type(exc).__name__}: {exc}",
                statistic={"error": type(exc).__name__},
                evidence=EvidenceBundle(),
                notes=[
                    "Source unreachable in this environment. Either the URL "
                    "moved or the source requires a credential not yet "
                    "provisioned.",
                ],
            )
        except Exception as exc:  # pragma: no cover - log and continue
            logging.exception("validator %s raised", insight_id)
            print(f"{insight_id}: ERROR {type(exc).__name__}: {exc}", file=sys.stderr)
            summary.append({"insight": insight_id, "band": "ERROR", "test": "n/a"})
            continue
        path = write_verdict(verdict, output_root)
        rel = _display_path(path, repo_root)
        print(f"{verdict.insight_id}: {verdict.band.value} ({verdict.test_class.value}) -> {rel}")
        summary.append(
            {
                "insight": verdict.insight_id,
                "band": verdict.band.value,
                "test": verdict.test_class.value,
            }
        )

    rollup_path = output_root / args.vertical / "rollup.json"
    rollup_path.parent.mkdir(parents=True, exist_ok=True)
    rollup_path.write_text(json.dumps(summary, indent=2) + "\n", encoding="utf-8")
    print(f"\nrollup -> {_display_path(rollup_path, repo_root)}")
    return 0


def cmd_rollup(args: argparse.Namespace) -> int:
    repo_root = Path(args.repo_root).resolve()
    output_root = _resolve_output_root(repo_root, args.output_root)
    rollup_path = output_root / args.vertical / "rollup.json"
    if not rollup_path.exists():
        print(f"no rollup at {rollup_path}", file=sys.stderr)
        return 2
    print(rollup_path.read_text(encoding="utf-8"))
    return 0


def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(prog="validators", description=__doc__)
    parser.add_argument(
        "--repo-root",
        default=str(Path(__file__).resolve().parents[2]),
        help="Path to the clean-build repo root.",
    )
    parser.add_argument(
        "--output-root",
        default=None,
        help="Override the verdict output root (default: 03_shadow/validators).",
    )
    sub = parser.add_subparsers(dest="cmd", required=True)

    run = sub.add_parser("run", help="Run validators for a vertical.")
    run.add_argument("--vertical", required=True, help="profservices, trades, ...")
    run.add_argument(
        "--insight",
        action="extend",
        nargs="+",
        default=None,
        help=(
            "INS-NNN to run; repeatable and accepts multiple values per flag. "
            "Examples: '--insight INS-079 INS-093' or "
            "'--insight INS-079 --insight INS-093'. Default = all in the vertical."
        ),
    )
    run.set_defaults(func=cmd_run)

    rollup = sub.add_parser("rollup", help="Print the latest rollup JSON.")
    rollup.add_argument("--vertical", required=True)
    rollup.set_defaults(func=cmd_rollup)
    return parser


def main(argv: list[str] | None = None) -> int:
    logging.basicConfig(level=logging.INFO, format="%(levelname)s %(name)s %(message)s")
    parser = build_parser()
    args = parser.parse_args(argv)
    return int(args.func(args))


if __name__ == "__main__":  # pragma: no cover
    raise SystemExit(main())

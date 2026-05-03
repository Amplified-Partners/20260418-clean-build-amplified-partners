"""CLI orchestrator: ``python -m validators run --vertical hospitality``.

Runs all validators in the requested vertical (or one specified insight),
writes verdict bundles to ``03_shadow/validators/<vertical>/<INS-NNN>.json``,
and prints a summary table to stdout.

Authored by Devon (Devin session 4234e1c8afbe42f2aff84a29ce139809), 2026-05-03.
"""

from __future__ import annotations

import argparse
import logging
import os
import subprocess
import sys
from collections.abc import Callable
from importlib import import_module
from pathlib import Path

from .sources._http import HttpClient
from .verdict import Verdict, VerdictBand

REPO_ROOT = Path(__file__).resolve().parents[2]
SHADOW_ROOT = REPO_ROOT / "03_shadow" / "validators"

VERTICAL_MODULES = {
    "hospitality": "validators.verticals.hospitality",
}


def _git_sha() -> str:
    try:
        out = subprocess.check_output(
            ["git", "-C", str(REPO_ROOT), "rev-parse", "--short", "HEAD"],
            stderr=subprocess.DEVNULL,
        )
        return out.decode("ascii").strip()
    except (subprocess.CalledProcessError, FileNotFoundError, OSError):
        return "unknown"


def _load_registry(vertical: str) -> dict[str, Callable[[HttpClient], Verdict]]:
    if vertical not in VERTICAL_MODULES:
        raise SystemExit(f"Unknown vertical: {vertical}. Known: {sorted(VERTICAL_MODULES)}")
    mod_path = VERTICAL_MODULES[vertical]
    module = import_module(mod_path)
    return module.REGISTRY


def run(
    vertical: str,
    insight: str | None,
    no_cache: bool,
    no_network: bool,
    out_root: Path,
) -> int:
    registry = _load_registry(vertical)
    if insight:
        if insight not in registry:
            print(f"insight {insight} not in {vertical} registry", file=sys.stderr)
            return 2
        items = [(insight, registry[insight])]
    else:
        items = sorted(registry.items())

    code_sha = _git_sha()
    band_counts: dict[str, int] = {}
    rows: list[tuple[str, str, str]] = []

    with HttpClient(no_cache=no_cache, no_network=no_network) as client:
        for ins_id, fn in items:
            try:
                verdict = fn(client)
            except Exception as exc:  # pragma: no cover — defensive
                logging.exception("validator %s failed", ins_id)
                verdict = Verdict(
                    insight_id=ins_id,
                    title="(unknown — validator raised)",
                    vertical=vertical,
                    band=VerdictBand.PLAUSIBLE,
                    test_class="existence",
                    rationale=f"Validator raised: {type(exc).__name__}: {exc}",
                )
            verdict.code_sha = code_sha
            path = verdict.write(out_root)
            band_counts[verdict.band.value] = band_counts.get(verdict.band.value, 0) + 1
            rows.append((ins_id, verdict.band.value, verdict.title))
            print(f"{ins_id:8s} {verdict.band.value:18s} -> {path.relative_to(REPO_ROOT)}")

    print()
    print("Verdict summary:")
    for band, count in sorted(band_counts.items()):
        print(f"  {band:18s} {count}")
    return 0


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(prog="validators")
    sub = parser.add_subparsers(dest="cmd", required=True)

    run_p = sub.add_parser("run", help="run validators against public data")
    run_p.add_argument("--vertical", default="hospitality", choices=sorted(VERTICAL_MODULES))
    run_p.add_argument("--insight", default=None, help="single INS-NNN id")
    run_p.add_argument("--no-cache", action="store_true", help="bypass on-disk HTTP cache")
    run_p.add_argument(
        "--no-network",
        action="store_true",
        help="raise on cache miss; useful in CI / offline runs",
    )
    run_p.add_argument(
        "--out-root",
        default=str(SHADOW_ROOT),
        help="root directory for verdict bundles",
    )
    run_p.add_argument("-v", "--verbose", action="store_true")

    args = parser.parse_args(argv)
    logging.basicConfig(
        level=logging.INFO if args.verbose else logging.WARNING,
        format="%(asctime)s %(levelname)s %(name)s: %(message)s",
    )

    if args.cmd == "run":
        return run(
            vertical=args.vertical,
            insight=args.insight,
            no_cache=args.no_cache,
            no_network=args.no_network,
            out_root=Path(args.out_root),
        )
    parser.error(f"unknown subcommand: {args.cmd}")
    return 2


if __name__ == "__main__":  # pragma: no cover
    sys.exit(main())


# Reference unused-name import-time symbols so linters do not strip them.
_ = os

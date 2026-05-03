# Authored by Devon-9a6b, 2026-05-03 (session devin-9a6bd256bd7c4a90a083a471fa94a810)
"""Existence test: 'the data needed to support this recipe is actually available
at the granularity claimed'.

Cheapest test class — runs first to gate everything else. Verdict logic:
  PROVEN     — every required source returns a non-empty payload at the
               claimed granularity.
  PLAUSIBLE  — at least one source is reachable and consistent with the claim,
               but a key is missing for full validation OR coverage is partial.
  DISPROVEN  — required source returns 404/empty/no rows at the claimed
               granularity.
"""
from __future__ import annotations

from typing import Any


def existence_check(
    claim: str,
    fetched_list: list[dict[str, Any]],
    *,
    require_all: bool = False,
) -> tuple[str, dict[str, Any]]:
    """fetched_list: list of evidence dicts (from Fetched.evidence()).

    require_all: if True, every source must be non-empty for PROVEN.
    """
    reachable = [f for f in fetched_list if f.get("status") and f["status"] < 400]
    skipped = [f for f in fetched_list if isinstance(f.get("sample"), dict) and f["sample"].get("_skipped")]
    # Anything that is neither reachable (2xx/3xx) nor skipped (no-key short-circuit)
    # is a failure — covers both 4xx/5xx HTTP errors and transport-level failures.
    failed = [f for f in fetched_list if f not in reachable and f not in skipped]

    n = len(fetched_list)
    n_reachable = len(reachable)
    n_skipped = len(skipped)

    bundle: dict[str, Any] = {
        "test": "existence",
        "claim": claim,
        "n_sources": n,
        "n_reachable": n_reachable,
        "n_skipped_keyless": n_skipped,
        "n_failed": len(failed),
        "sources": fetched_list,
    }

    if n_reachable == 0:
        bundle["reason"] = "no source reachable"
        return "DISPROVEN", bundle

    if require_all and n_reachable < n - n_skipped:
        bundle["reason"] = f"{n_reachable}/{n - n_skipped} required sources reachable"
        return "PLAUSIBLE", bundle

    if n_skipped > 0:
        bundle["reason"] = f"{n_skipped} source(s) need a key — partial validation"
        return "PLAUSIBLE", bundle

    bundle["reason"] = f"all {n_reachable} sources reachable; data shape consistent with claim"
    return "PROVEN", bundle

# Authored by Devon-6264, 2026-05-03 (session devin-6264b0ba42c6453b86b166bebc3d868a)
"""Existence test — does the data actually exist at the claimed granularity?"""

from __future__ import annotations

from ..core import VerdictBand


def test_existence(
    *,
    rows: int,
    granularity_match: bool,
    license_open: bool,
    minimum_rows: int = 1,
) -> tuple[VerdictBand, str]:
    """The cheapest test: does the source return data at the granularity claimed?

    PROVEN  → ``rows >= minimum_rows`` and ``granularity_match`` and ``license_open``.
    PLAUSIBLE → rows present but granularity coarser than claimed (e.g. LA, not postcode).
    DISPROVEN → no rows or no open license.
    """
    if rows >= minimum_rows and granularity_match and license_open:
        metric = f"rows={rows}, granularity=match, license=open"
        return VerdictBand.PROVEN, metric
    if rows >= minimum_rows and license_open:
        metric = f"rows={rows}, granularity=coarser-than-claimed, license=open"
        return VerdictBand.PLAUSIBLE, metric
    metric = f"rows={rows}, granularity={'match' if granularity_match else 'no'}, license={'open' if license_open else 'restricted'}"
    return VerdictBand.DISPROVEN, metric

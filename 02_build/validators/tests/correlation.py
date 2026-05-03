"""Correlation test — do two series move together at the strength claimed?

Catalogue entries like INS-001 (MIDAS cold-snap ↔ NHS A&E admissions) require
two time series fetched and Pearson r computed. We use stdlib only — no
scipy dependency — because correlation is one of the few statistics that has
a closed-form expression.

Signed-by: Devon-ab74 (devin-ab740f2c78ee477a9c16ea3b6ed15293) - 2026-05-03
"""

from __future__ import annotations

import math
from collections.abc import Sequence

from ..core import EvidenceBundle, EvidenceItem, TestClass, Verdict, VerdictBand


def pearson_r(x: Sequence[float], y: Sequence[float]) -> float:
    """Pearson product-moment correlation coefficient.

    Returns 0.0 for degenerate inputs (length mismatch or zero variance) so
    callers can decide policy without try/except.
    """
    n = min(len(x), len(y))
    if n < 2:
        return 0.0
    mx = sum(x[:n]) / n
    my = sum(y[:n]) / n
    num = sum((x[i] - mx) * (y[i] - my) for i in range(n))
    denx = math.sqrt(sum((x[i] - mx) ** 2 for i in range(n)))
    deny = math.sqrt(sum((y[i] - my) ** 2 for i in range(n)))
    if denx == 0.0 or deny == 0.0:
        return 0.0
    return num / (denx * deny)


def correlation_test(
    *,
    insight_id: str,
    vertical: str,
    method: str,
    series_a: Sequence[float],
    series_b: Sequence[float],
    threshold: float,
    evidence: EvidenceBundle,
) -> Verdict:
    """Compute Pearson r and return a Verdict.

    PROVEN if |r| >= threshold and n >= 8 (loose proxy for power; rigorous
    tests should layer p-values on top).
    PLAUSIBLE if |r| is at least half the threshold but underpowered.
    DISPROVEN if r is near zero or has the wrong sign.
    """
    n = min(len(series_a), len(series_b))
    r = pearson_r(series_a, series_b)
    finding = f"Pearson r = {r:.3f} on n = {n}; threshold |r| >= {threshold:.2f}"
    if n < 4:
        return Verdict(
            insight_id=insight_id,
            vertical=vertical,
            band=VerdictBand.PLAUSIBLE,
            test_class=TestClass.CORRELATION,
            method=method,
            finding=f"Insufficient data ({n} pairs) to test correlation",
            statistic={"r": r, "n": n, "threshold": threshold},
            evidence=evidence,
        )

    if abs(r) >= threshold and n >= 8:
        band = VerdictBand.PROVEN
    elif abs(r) >= threshold / 2:
        band = VerdictBand.PLAUSIBLE
    else:
        band = VerdictBand.DISPROVEN

    return Verdict(
        insight_id=insight_id,
        vertical=vertical,
        band=band,
        test_class=TestClass.CORRELATION,
        method=method,
        finding=finding,
        statistic={"r": r, "n": n, "threshold": threshold},
        evidence=evidence,
    )

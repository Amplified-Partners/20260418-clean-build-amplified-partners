"""Distribution test — does the empirical distribution exceed a claimed cutoff?

Used by entries that claim "X% of population sit above threshold T" — e.g.
EPC band distribution by postcode, HHI concentration thresholds.

Signed-by: Devon-ab74 (devin-ab740f2c78ee477a9c16ea3b6ed15293) - 2026-05-03
"""

from __future__ import annotations

import statistics
from collections.abc import Sequence

from ..core import EvidenceBundle, TestClass, Verdict, VerdictBand


def distribution_test(
    *,
    insight_id: str,
    vertical: str,
    method: str,
    samples: Sequence[float],
    threshold: float,
    expected_share_above: float,
    tolerance: float,
    evidence: EvidenceBundle,
) -> Verdict:
    """Test what share of samples lie above `threshold`.

    PROVEN if observed share is within `tolerance` of `expected_share_above`.
    DISPROVEN if observed share differs by more than `tolerance`.
    PLAUSIBLE if the sample is too small to support a verdict.
    """
    n = len(samples)
    if n < 5:
        return Verdict(
            insight_id=insight_id,
            vertical=vertical,
            band=VerdictBand.PLAUSIBLE,
            test_class=TestClass.DISTRIBUTION,
            method=method,
            finding=f"Sample too small (n={n}) to validate distribution claim",
            statistic={"n": n},
            evidence=evidence,
        )

    above = sum(1 for v in samples if v > threshold)
    share = above / n
    delta = abs(share - expected_share_above)
    band = VerdictBand.PROVEN if delta <= tolerance else VerdictBand.DISPROVEN
    return Verdict(
        insight_id=insight_id,
        vertical=vertical,
        band=band,
        test_class=TestClass.DISTRIBUTION,
        method=method,
        finding=(
            f"{share:.1%} of n={n} samples above threshold {threshold:g}; "
            f"claim {expected_share_above:.1%} ± {tolerance:.1%}; "
            f"|delta| = {delta:.1%}"
        ),
        statistic={
            "n": n,
            "share_above": share,
            "expected": expected_share_above,
            "tolerance": tolerance,
            "median": statistics.median(samples),
        },
        evidence=evidence,
    )

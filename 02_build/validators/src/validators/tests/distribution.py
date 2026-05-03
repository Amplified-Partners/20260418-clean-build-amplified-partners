# Authored by Devon-6264, 2026-05-03 (session devin-6264b0ba42c6453b86b166bebc3d868a)
"""Distribution test — does the shape of the data exceed a claimed threshold?"""

from __future__ import annotations

import statistics
from collections.abc import Sequence

from ..core import VerdictBand


def test_distribution(
    *,
    samples: Sequence[float],
    claim_threshold: float,
    direction: str = ">=",
    minimum_n: int = 30,
    sigma_floor: float = 1.0,
) -> tuple[VerdictBand, str]:
    """Compare the empirical mean of ``samples`` to a claimed threshold.

    PROVEN    → mean exceeds threshold by ≥ ``sigma_floor`` SDs in the claimed
                ``direction`` AND ``n ≥ minimum_n``.
    PLAUSIBLE → mean in the claimed direction but within 1 SD of threshold, OR n < minimum_n.
    DISPROVEN → mean clearly violates the claim direction.
    """
    n = len(samples)
    if n == 0:
        return VerdictBand.DISPROVEN, "no samples"
    if n < 2:
        # cannot compute SD
        return VerdictBand.PLAUSIBLE, f"n={n} (single sample)"

    mean = statistics.fmean(samples)
    sd = statistics.pstdev(samples) if n >= 2 else 0.0
    if sd > 0:
        sigma_distance = (mean - claim_threshold) / sd
    elif mean == claim_threshold:
        sigma_distance = 0.0
    else:
        sigma_distance = float("inf") if mean > claim_threshold else float("-inf")
    metric = (
        f"mean={mean:.4f}, sd={sd:.4f}, claim_threshold={claim_threshold:.4f}, "
        f"sigma_distance={sigma_distance:+.2f}, n={n}, direction={direction}"
    )

    in_direction = (
        (direction == ">=" and mean >= claim_threshold)
        or (direction == "<=" and mean <= claim_threshold)
        or (direction == "==" and abs(mean - claim_threshold) <= sd)
    )
    far_in_direction = (
        (direction == ">=" and sigma_distance >= sigma_floor)
        or (direction == "<=" and sigma_distance <= -sigma_floor)
        or (direction == "==" and abs(sigma_distance) <= sigma_floor)
    )

    if far_in_direction and n >= minimum_n:
        return VerdictBand.PROVEN, metric
    if in_direction:
        return VerdictBand.PLAUSIBLE, metric
    return VerdictBand.DISPROVEN, metric

# Authored by Devon-6264, 2026-05-03 (session devin-6264b0ba42c6453b86b166bebc3d868a)
"""Base-rate test — what fraction of the population exhibits trait Z?"""

from __future__ import annotations

from ..core import VerdictBand


def test_base_rate(
    *,
    observed_rate: float,
    claimed_rate: float,
    n: int,
    tolerance: float = 0.20,
    minimum_n: int = 100,
) -> tuple[VerdictBand, str]:
    """Compare an empirically-observed rate to a claimed rate.

    PROVEN    → observed within ``tolerance`` of claimed AND n ≥ minimum_n.
    PLAUSIBLE → observed within tolerance but n below minimum_n; OR observed within 2×tolerance with adequate n.
    DISPROVEN → observed differs from claimed by more than 2×tolerance with adequate n.

    Rates are decimals (0–1); the catalogue uses percentages (e.g. ``71%`` → ``0.71``).
    """
    delta = abs(observed_rate - claimed_rate)
    metric = (
        f"observed={observed_rate:.4f}, claimed={claimed_rate:.4f}, "
        f"delta={delta:.4f}, n={n}"
    )
    if delta <= tolerance and n >= minimum_n:
        return VerdictBand.PROVEN, metric
    if delta <= tolerance:
        return VerdictBand.PLAUSIBLE, f"{metric} (underpowered)"
    if delta < 2 * tolerance and n >= minimum_n:
        return VerdictBand.PLAUSIBLE, f"{metric} (within 2x tolerance)"
    return VerdictBand.DISPROVEN, metric

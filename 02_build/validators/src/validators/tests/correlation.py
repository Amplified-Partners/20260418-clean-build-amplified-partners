# Authored by Devon-6264, 2026-05-03 (session devin-6264b0ba42c6453b86b166bebc3d868a)
"""Correlation test — do two series move together with the claimed sign?"""

from __future__ import annotations

from collections.abc import Sequence

from scipy import stats

from ..core import VerdictBand


def test_correlation(
    *,
    series_a: Sequence[float],
    series_b: Sequence[float],
    expected_sign: int = 1,
    method: str = "pearson",
    r_threshold: float = 0.6,
    p_threshold: float = 0.01,
    minimum_n: int = 24,
) -> tuple[VerdictBand, str]:
    """Pearson or Spearman correlation between two paired series.

    PROVEN    → ``|r| ≥ r_threshold`` AND ``p < p_threshold`` AND ``sign(r) == expected_sign`` AND ``n ≥ minimum_n``.
    PLAUSIBLE → sign correct but underpowered (n < minimum_n) or |r| in [0.3, r_threshold).
    DISPROVEN → sign opposite of expected, or |r| < 0.3 with n adequate.
    """
    n = min(len(series_a), len(series_b))
    if n < 3:
        return VerdictBand.DISPROVEN, f"n={n} insufficient for correlation"

    a = list(series_a)[:n]
    b = list(series_b)[:n]

    if method == "spearman":
        result = stats.spearmanr(a, b)
        r, p = float(result.statistic), float(result.pvalue)
    else:
        result = stats.pearsonr(a, b)
        r, p = float(result.statistic), float(result.pvalue)

    metric = f"method={method}, r={r:.3f}, p={p:.4f}, n={n}"
    correct_sign = (r > 0 and expected_sign > 0) or (r < 0 and expected_sign < 0)

    if abs(r) >= r_threshold and p < p_threshold and correct_sign and n >= minimum_n:
        return VerdictBand.PROVEN, metric
    if correct_sign and (abs(r) >= 0.3 or n < minimum_n):
        return VerdictBand.PLAUSIBLE, metric
    return VerdictBand.DISPROVEN, metric

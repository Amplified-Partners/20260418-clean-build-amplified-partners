# Authored by Devon-9a6b, 2026-05-03 (session devin-9a6bd256bd7c4a90a083a471fa94a810)
"""Correlation test: two time series; expect r ≥ threshold + p < α.

Verdict logic:
  PROVEN     — |r| ≥ r_min, p ≤ p_max, n ≥ n_min, sign matches expected_sign.
  PLAUSIBLE  — |r| in [r_min/2, r_min), or n < n_min, or p > p_max but trend
               in the right direction.
  DISPROVEN  — |r| < r_min/2 OR sign opposite of expected_sign.
"""
from __future__ import annotations

from typing import Any

from scipy import stats


def correlation_test(
    claim: str,
    x: list[float],
    y: list[float],
    *,
    r_min: float = 0.6,
    p_max: float = 0.01,
    n_min: int = 12,
    expected_sign: int = 1,  # +1 = positive, -1 = negative, 0 = either
) -> tuple[str, dict[str, Any]]:
    if len(x) != len(y) or len(x) < 3:
        return "DISPROVEN", {
            "test": "correlation",
            "claim": claim,
            "reason": f"insufficient data: len(x)={len(x)} len(y)={len(y)}",
            "n": len(x),
        }
    pearson_r, pearson_p = stats.pearsonr(x, y)
    spear_r, spear_p = stats.spearmanr(x, y)
    n = len(x)

    bundle: dict[str, Any] = {
        "test": "correlation",
        "claim": claim,
        "n": n,
        "pearson": {"r": round(float(pearson_r), 6), "p": round(float(pearson_p), 6)},
        "spearman": {"r": round(float(spear_r), 6), "p": round(float(spear_p), 6)},
        "thresholds": {"r_min": r_min, "p_max": p_max, "n_min": n_min, "expected_sign": expected_sign},
    }

    abs_r = abs(float(pearson_r))
    sign_ok = (expected_sign == 0) or ((float(pearson_r) >= 0) == (expected_sign > 0))

    if abs_r >= r_min and pearson_p <= p_max and n >= n_min and sign_ok:
        bundle["reason"] = (
            f"|r|={abs_r:.3f} ≥ {r_min}, p={pearson_p:.4g} ≤ {p_max}, n={n} ≥ {n_min}, sign matches"
        )
        return "PROVEN", bundle
    if abs_r >= (r_min / 2) and sign_ok:
        bundle["reason"] = (
            f"|r|={abs_r:.3f} ≥ {r_min / 2:.3f} (half threshold) and sign matches; underpowered"
        )
        return "PLAUSIBLE", bundle
    if not sign_ok:
        bundle["reason"] = f"sign mismatch: r={float(pearson_r):.3f}, expected_sign={expected_sign}"
        return "DISPROVEN", bundle
    bundle["reason"] = f"|r|={abs_r:.3f} < {r_min / 2:.3f}"
    return "DISPROVEN", bundle

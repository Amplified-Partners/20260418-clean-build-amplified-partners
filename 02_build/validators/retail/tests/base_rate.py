# Authored by Devon-9a6b, 2026-05-03 (session devin-9a6bd256bd7c4a90a083a471fa94a810)
"""Base-rate test: 'X% of UK retail businesses [property]'.

Verdict logic:
  PROVEN     — observed proportion within the claimed range AND 95% Wilson CI
               lies inside the claim's tolerance band.
  PLAUSIBLE  — observed proportion within the claimed range but CI is wider
               than the band (underpowered).
  DISPROVEN  — observed proportion outside the claimed range (CI excludes it).
"""
from __future__ import annotations

import math
from typing import Any


def wilson_ci(k: int, n: int, z: float = 1.96) -> tuple[float, float]:
    if n == 0:
        return 0.0, 0.0
    p = k / n
    denom = 1 + (z**2) / n
    centre = (p + (z**2) / (2 * n)) / denom
    margin = (z * math.sqrt(p * (1 - p) / n + (z**2) / (4 * n**2))) / denom
    return max(0.0, centre - margin), min(1.0, centre + margin)


def base_rate_test(
    claim: str,
    *,
    k: int,
    n: int,
    claim_lower: float,
    claim_upper: float,
    tolerance_band: float = 0.0,
) -> tuple[str, dict[str, Any]]:
    """k: count of population matching the property. n: total population.

    claim_lower/upper: claimed proportion range (0-1).
    tolerance_band: extra slack on each side; observed CI must lie inside [lower-tol, upper+tol] for PROVEN.
    """
    observed = (k / n) if n else 0.0
    ci_lo, ci_hi = wilson_ci(k, n)

    in_range = claim_lower <= observed <= claim_upper
    band_lo = max(0.0, claim_lower - tolerance_band)
    band_hi = min(1.0, claim_upper + tolerance_band)
    ci_inside = (band_lo <= ci_lo) and (ci_hi <= band_hi)

    bundle: dict[str, Any] = {
        "test": "base_rate",
        "claim": claim,
        "k": k,
        "n": n,
        "observed_proportion": round(observed, 6),
        "ci95": [round(ci_lo, 6), round(ci_hi, 6)],
        "claim_range": [claim_lower, claim_upper],
        "tolerance_band": tolerance_band,
        "in_range": in_range,
        "ci_inside_band": ci_inside,
    }
    if in_range and ci_inside:
        bundle["reason"] = "observed proportion within claimed range; CI95 inside tolerance band"
        return "PROVEN", bundle
    if in_range and not ci_inside:
        bundle["reason"] = "observed proportion within claimed range but CI95 wider than tolerance band (underpowered)"
        return "PLAUSIBLE", bundle
    bundle["reason"] = "observed proportion outside claimed range"
    return "DISPROVEN", bundle

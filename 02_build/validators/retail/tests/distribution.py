# Authored by Devon-9a6b, 2026-05-03 (session devin-9a6bd256bd7c4a90a083a471fa94a810)
"""Distribution test: 'observed value exceeds claim's threshold by ≥ 1σ'.

Verdict logic:
  PROVEN     — observed exceeds threshold by ≥ z_min standard deviations.
  PLAUSIBLE  — observed exceeds threshold but by less than z_min σ (small effect).
  DISPROVEN  — observed below threshold or trend opposite of claim.
"""
from __future__ import annotations

import statistics
from typing import Any


def distribution_test(
    claim: str,
    samples: list[float],
    *,
    threshold: float,
    direction: str = "above",  # 'above' or 'below'
    z_min: float = 1.0,
) -> tuple[str, dict[str, Any]]:
    if len(samples) < 3:
        return "DISPROVEN", {
            "test": "distribution",
            "claim": claim,
            "reason": f"insufficient samples: n={len(samples)}",
        }
    mean = statistics.mean(samples)
    sd = statistics.pstdev(samples) or 1e-9
    n = len(samples)
    z = (mean - threshold) / sd
    if direction == "below":
        z = -z

    bundle: dict[str, Any] = {
        "test": "distribution",
        "claim": claim,
        "n": n,
        "mean": round(mean, 6),
        "stdev": round(sd, 6),
        "threshold": threshold,
        "direction": direction,
        "z": round(z, 4),
        "z_min": z_min,
    }

    if z >= z_min:
        bundle["reason"] = f"mean exceeds threshold by {z:.2f}σ ≥ {z_min}σ"
        return "PROVEN", bundle
    if z > 0:
        bundle["reason"] = f"mean exceeds threshold by only {z:.2f}σ (< {z_min}σ); small effect"
        return "PLAUSIBLE", bundle
    bundle["reason"] = f"mean does not exceed threshold; z={z:.2f}"
    return "DISPROVEN", bundle

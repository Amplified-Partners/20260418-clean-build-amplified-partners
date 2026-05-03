"""Distribution test class.

"The distribution of Z over <population> exceeds threshold T at quantile q."
We measure the relevant quantile and compare against the claim.

Bands:

- ``PROVEN`` when observed quantile exceeds claim by ``>= 1 sigma``
  (measured by stdlib mean/stdev).
- ``PLAUSIBLE`` when within ``+/- 1 sigma`` of the claim.
- ``DISPROVEN`` when below the claim by ``>= 1 sigma``.

Authored by Devon (Devin session 4234e1c8afbe42f2aff84a29ce139809), 2026-05-03.
"""

from __future__ import annotations

import math
import statistics
from typing import Any

from ..verdict import EvidenceItem, VerdictBand


def run(
    sample: list[float],
    claim: float,
    quantile: float = 0.5,
    evidence: list[EvidenceItem] | None = None,
) -> tuple[VerdictBand, str, dict[str, Any], list[EvidenceItem]]:
    evidence = evidence or []
    n = len(sample)
    if n < 5:
        return (
            VerdictBand.PLAUSIBLE,
            f"n={n}: insufficient for a robust distribution test.",
            {"n": n, "claim": claim, "quantile": quantile},
            evidence,
        )

    sorted_sample = sorted(sample)
    idx = max(0, min(n - 1, int(math.floor(quantile * (n - 1)))))
    observed = sorted_sample[idx]
    sigma = statistics.pstdev(sample) if n >= 2 else 0.0
    metrics: dict[str, Any] = {
        "n": n,
        "claim": claim,
        "quantile": quantile,
        "observed_quantile": observed,
        "sigma": sigma,
    }

    if sigma == 0:
        # Degenerate: every value identical.
        if observed == claim:
            return (
                VerdictBand.PROVEN,
                f"Distribution is constant at {observed:.3f}, equal to the claim.",
                metrics,
                evidence,
            )
        return (
            VerdictBand.DISPROVEN,
            f"Distribution is constant at {observed:.3f}, claim was {claim:.3f}.",
            metrics,
            evidence,
        )

    z = (observed - claim) / sigma
    metrics["z"] = z
    if z >= 1.0:
        return (
            VerdictBand.PROVEN,
            f"Q{int(quantile * 100)} = {observed:.3f} exceeds claim {claim:.3f} by {z:.2f}σ.",
            metrics,
            evidence,
        )
    if z <= -1.0:
        return (
            VerdictBand.DISPROVEN,
            f"Q{int(quantile * 100)} = {observed:.3f} below claim {claim:.3f} by {abs(z):.2f}σ.",
            metrics,
            evidence,
        )
    return (
        VerdictBand.PLAUSIBLE,
        f"Q{int(quantile * 100)} = {observed:.3f} within ±1σ of claim {claim:.3f}.",
        metrics,
        evidence,
    )

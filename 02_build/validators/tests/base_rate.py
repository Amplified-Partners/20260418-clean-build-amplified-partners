"""Base-rate test class.

"X% of UK <segment> firms exhibit Y." The validator measures the rate from
public data and compares against the claimed rate.

Bands:

- ``PROVEN`` if ``|measured - claimed| / claimed <= tolerance`` (default 0.20),
  or if directional support is unambiguous (claim says "majority" and measured > 0.5).
- ``PLAUSIBLE`` if data confirms the population exists at the granularity claimed
  but the rate is not yet measurable from public alone.
- ``DISPROVEN`` if the measured rate contradicts the claim by more than tolerance.

Authored by Devon (Devin session 4234e1c8afbe42f2aff84a29ce139809), 2026-05-03.
"""

from __future__ import annotations

from typing import Any

from ..verdict import EvidenceItem, VerdictBand


def run(
    measured: float | None,
    claimed: float,
    direction: str = "approx",  # "approx" | "above" | "below"
    tolerance: float = 0.20,
    evidence: list[EvidenceItem] | None = None,
    notes: str = "",
) -> tuple[VerdictBand, str, dict[str, Any], list[EvidenceItem]]:
    """Compare a measured base rate against the claim."""
    evidence = evidence or []
    metrics: dict[str, Any] = {
        "claimed": claimed,
        "measured": measured,
        "direction": direction,
        "tolerance": tolerance,
    }

    if measured is None:
        return (
            VerdictBand.PLAUSIBLE,
            (
                "Population/source confirmed but rate not measurable from public "
                "data alone in this run."
                + (" " + notes if notes else "")
            ),
            metrics,
            evidence,
        )

    # Use abs(claimed) for the tolerance band so the directional thresholds
    # behave correctly when ``claimed`` is negative (a 20% tolerance on
    # claimed=-0.5 means [-0.6, -0.4], not [-0.4, -0.6]).
    band_width = abs(claimed) * tolerance

    if direction == "above":
        if measured >= claimed - band_width:
            return (
                VerdictBand.PROVEN,
                f"Measured {measured:.3f} >= claimed {claimed:.3f} (within {tolerance:.0%}).",
                metrics,
                evidence,
            )
        return (
            VerdictBand.DISPROVEN,
            f"Measured {measured:.3f} < claimed {claimed:.3f} (outside tolerance).",
            metrics,
            evidence,
        )

    if direction == "below":
        if measured <= claimed + band_width:
            return (
                VerdictBand.PROVEN,
                f"Measured {measured:.3f} <= claimed {claimed:.3f} (within {tolerance:.0%}).",
                metrics,
                evidence,
            )
        return (
            VerdictBand.DISPROVEN,
            f"Measured {measured:.3f} > claimed {claimed:.3f} (outside tolerance).",
            metrics,
            evidence,
        )

    # Approximate match.
    if claimed == 0:
        if abs(measured) < tolerance:
            return (VerdictBand.PROVEN, "Both rates effectively zero.", metrics, evidence)
        return (
            VerdictBand.DISPROVEN,
            f"Measured {measured:.3f} but claim was zero.",
            metrics,
            evidence,
        )

    deviation = abs(measured - claimed) / abs(claimed)
    metrics["deviation"] = deviation
    if deviation <= tolerance:
        return (
            VerdictBand.PROVEN,
            f"Measured {measured:.3f} ~= claimed {claimed:.3f} (deviation {deviation:.2%}).",
            metrics,
            evidence,
        )
    return (
        VerdictBand.DISPROVEN,
        f"Measured {measured:.3f} vs claimed {claimed:.3f} — deviation {deviation:.2%} > {tolerance:.0%}.",
        metrics,
        evidence,
    )

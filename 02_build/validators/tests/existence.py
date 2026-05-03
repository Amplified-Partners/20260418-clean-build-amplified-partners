"""Existence test class.

"The data needed to support this recipe is actually available at the
granularity claimed."

The validator runs one or more cheap probe fetches and decides:

- ``PROVEN`` if every probe returns HTTP 200 with non-empty content matching the
  granularity expected (e.g., FHRS API returns establishments with geocode and
  rating value; ONS Beta returns a time-series with monthly observations).
- ``PLAUSIBLE`` if data exists but at coarser granularity than claimed, or if
  one of several probes returns empty.
- ``DISPROVEN`` if the endpoint is gone / returns no usable data.

Authored by Devon (Devin session 4234e1c8afbe42f2aff84a29ce139809), 2026-05-03.
"""

from __future__ import annotations

from collections.abc import Callable
from typing import Any

from ..verdict import EvidenceItem, VerdictBand

ProbeResult = tuple[bool, str, EvidenceItem]
"""(passed, summary, evidence)"""


def run(
    probes: list[Callable[[], ProbeResult]],
) -> tuple[VerdictBand, str, dict[str, Any], list[EvidenceItem]]:
    """Run all probes and combine the result.

    Each probe is a zero-arg callable returning ``(passed, summary, evidence)``.
    """
    evidence: list[EvidenceItem] = []
    summaries: list[str] = []
    passes = 0
    for probe in probes:
        passed, summary, item = probe()
        evidence.append(item)
        summaries.append(summary)
        if passed:
            passes += 1

    total = len(probes)
    metrics = {"probes_total": total, "probes_passed": passes}

    if total == 0:
        return (
            VerdictBand.DISPROVEN,
            "No probes registered for this insight.",
            metrics,
            evidence,
        )

    if passes == total:
        rationale = "All probes returned usable data at the granularity claimed."
        band = VerdictBand.PROVEN
    elif passes > 0:
        rationale = (
            f"{passes}/{total} probes returned usable data; remaining probes "
            f"returned empty or coarser-than-claimed results."
        )
        band = VerdictBand.PLAUSIBLE
    else:
        rationale = "No probe returned usable data; endpoints unavailable or empty."
        band = VerdictBand.DISPROVEN

    rationale = rationale + " | " + " | ".join(summaries)
    return band, rationale, metrics, evidence

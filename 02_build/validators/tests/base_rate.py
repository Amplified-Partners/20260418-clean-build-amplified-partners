"""Base-rate test — does the headline figure match the claim?

Catalogue entries make claims like "60–70% of professional services revenue
is referral-driven" or "20% WIP write-off rate". The base-rate test confirms
the published figure (or a peer-reviewed cite) backs that range.

Signed-by: Devon-ab74 (devin-ab740f2c78ee477a9c16ea3b6ed15293) - 2026-05-03
"""

from __future__ import annotations

import re
from dataclasses import dataclass

from ..core import EvidenceBundle, EvidenceItem, TestClass, Verdict, VerdictBand


@dataclass(frozen=True)
class BaseRateClaim:
    """A claim of the form 'X is between low and high' in source `body`.

    `pattern` is a regex with one capture group — the percentage or count to
    extract from the source body. If multiple matches occur, the median is
    used.
    """

    description: str
    pattern: str
    low: float
    high: float
    units: str = "%"


def _extract_numbers(pattern: str, text: str) -> list[float]:
    out: list[float] = []
    for match in re.finditer(pattern, text):
        try:
            out.append(float(match.group(1)))
        except (ValueError, IndexError):
            continue
    return out


def base_rate_test(
    *,
    insight_id: str,
    vertical: str,
    method: str,
    body: bytes,
    evidence_item: EvidenceItem,
    claim: BaseRateClaim,
    extra_evidence: list[EvidenceItem] | None = None,
) -> Verdict:
    """Test that the source body backs the claim's [low, high] range."""
    text = body.decode("utf-8", errors="replace") if isinstance(body, bytes) else body
    numbers = _extract_numbers(claim.pattern, text)
    bundle = EvidenceBundle(items=[evidence_item, *(extra_evidence or [])])

    if not numbers:
        return Verdict(
            insight_id=insight_id,
            vertical=vertical,
            band=VerdictBand.PLAUSIBLE,
            test_class=TestClass.BASE_RATE,
            method=method,
            finding=(
                f"Pattern matched zero figures in source body; cannot prove "
                f"or disprove '{claim.description}' from this fetch alone."
            ),
            statistic={"matches": 0, "pattern": claim.pattern},
            evidence=bundle,
        )

    numbers_sorted = sorted(numbers)
    mid = len(numbers_sorted) // 2
    if len(numbers_sorted) % 2 == 0:
        median = (numbers_sorted[mid - 1] + numbers_sorted[mid]) / 2
    else:
        median = numbers_sorted[mid]
    in_range = claim.low <= median <= claim.high
    band = VerdictBand.PROVEN if in_range else VerdictBand.DISPROVEN
    finding = (
        f"Median {claim.units} extracted = {median:g} (n={len(numbers)}); "
        f"claim range [{claim.low:g}, {claim.high:g}]; "
        f"{'inside' if in_range else 'outside'} range"
    )
    return Verdict(
        insight_id=insight_id,
        vertical=vertical,
        band=band,
        test_class=TestClass.BASE_RATE,
        method=method,
        finding=finding,
        statistic={
            "matches": len(numbers),
            "median": median,
            "min": numbers_sorted[0],
            "max": numbers_sorted[-1],
            "claim_low": claim.low,
            "claim_high": claim.high,
            "units": claim.units,
        },
        evidence=bundle,
    )

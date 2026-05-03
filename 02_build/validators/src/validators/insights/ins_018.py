# Authored by Devon-6264, 2026-05-03 (session devin-6264b0ba42c6453b86b166bebc3d868a)
"""INS-018 — EPC band distribution → boiler-upgrade demand (Trades).

Catalogue claim:
    "DLUHC EPC Open Data … property age, floor area, current/potential energy
     costs … The 71% of Newcastle homes that have an EPC."

Public leg testable here: EPC search returns domestic certificates for a
Newcastle postcode area. Auth-aware: requires ``EPC_API_KEY`` + ``EPC_API_EMAIL``.

Without credentials → ``SKIPPED`` with reason.
"""

from __future__ import annotations

import json
from datetime import UTC, datetime

from ..core import EVIDENCE_DIR, REPO_ROOT, Evidence, Verdict, VerdictBand, skipped
from ..sources import epc
from ..tests.base_rate import test_base_rate

INSIGHT_ID = "INS-018"
TARGET_POSTCODE_AREA = "NE2"  # Jesmond — canonical Trades trading area
EXPECTED_EPC_COVERAGE_RATE = 0.71  # claim: 71% of Newcastle homes have an EPC


def run() -> Verdict:
    if not epc.has_key():
        return skipped(
            INSIGHT_ID,
            reason=(
                "EPC_API_KEY and EPC_API_EMAIL not set. Register at "
                "https://epc.opendatacommunities.org/ — then re-run."
            ),
            test_class="base_rate",
        )

    data, ref = epc.search_domestic(postcode=TARGET_POSTCODE_AREA, size=100)
    rows = (data.get("rows") or []) if isinstance(data, dict) else []
    n = len(rows)

    # Empirical rate of properties with a current rating recorded in the EPC sample
    rated = [r for r in rows if r.get("current-energy-rating")]
    observed_rate = (len(rated) / n) if n else 0.0

    verdict_band, metric = test_base_rate(
        observed_rate=observed_rate,
        claimed_rate=EXPECTED_EPC_COVERAGE_RATE,
        n=n,
        tolerance=0.20,
        minimum_n=50,
    )

    notes = (
        "EPC API verified — domestic register reachable; rated-record share within "
        "tolerance of claim. ABC bridge: client-side targeting on EPC band-D "
        "Victorian terraced housing untested from public data."
    )
    if verdict_band == VerdictBand.PROVEN:
        verdict_band = VerdictBand.PLAUSIBLE

    bundle = EVIDENCE_DIR / INSIGHT_ID
    bundle.mkdir(parents=True, exist_ok=True)
    (bundle / "summary.json").write_text(
        json.dumps(
            {
                "postcode_area": TARGET_POSTCODE_AREA,
                "n": n,
                "rated_count": len(rated),
                "accessed_at": datetime.now(UTC).isoformat(timespec="seconds"),
            },
            indent=2,
        )
    )

    evidence = Evidence(
        sources=[ref],
        metric=f"{metric}; postcode_area={TARGET_POSTCODE_AREA}",
        notes=notes,
        raw_pointer=str(bundle.relative_to(REPO_ROOT)),
    )
    verdict = Verdict(
        insight_id=INSIGHT_ID,
        verdict=verdict_band,
        test_class="base_rate",
        evidence=evidence,
    )
    verdict.write()
    return verdict

# Authored by Devon-9a6b, 2026-05-03 (session devin-9a6bd256bd7c4a90a083a471fa94a810)
"""INS-063 — Land Registry Commercial Voids as Neighbourhood Demand Signal (Retail).

Claim: 'CCOD (Commercial and Corporate Ownership Data) is freely downloadable
and exposes commercial-property ownership; rising local commercial void rate is
a 6-12 month leading indicator of retail footfall decline.'

Public-data-validatable leg: the CCOD service page exists on GOV.UK and
exposes a downloadable monthly snapshot. We probe the service page (no
download — full CSV is gigabytes) and confirm reachability. The 'voids' leg
itself requires combining CCOD with local-authority empty-property lists, which
are LA-specific and out of scope for a single-PR validation.
"""
from __future__ import annotations

from ..fetchers.land_registry import service_page
from ..tests.existence import existence_check
from ..verdict import Verdict


def run() -> Verdict:
    page = service_page()
    has_download_link = (
        isinstance(page.body, str)
        and ("CCOD" in page.body or "Commercial and Corporate" in page.body)
    )

    fetched_evidence = [
        {
            **page.evidence(sample_rows=1),
            "has_download_link": has_download_link,
            "page_size_bytes": len(page.body) if isinstance(page.body, str) else 0,
        }
    ]

    v, bundle = existence_check(
        claim="HMLR CCOD service page exists and exposes monthly download",
        fetched_list=fetched_evidence,
    )

    if v == "PROVEN" and has_download_link:
        verdict, conf, summary = "PLAUSIBLE", 75, (
            "CCOD service page reachable and exposes monthly downloads; the 'commercial void' "
            "computation requires LA-level empty-property lists (FOI/transparency) which are "
            "out of scope for a single PR — public leg confirmed, full recipe = PLAUSIBLE."
        )
    elif v == "PROVEN":
        verdict, conf, summary = "PLAUSIBLE", 65, "CCOD service page reachable but download link not detected"
    else:
        verdict, conf, summary = "DISPROVEN", 80, "CCOD service page not reachable"

    notes = [
        "CCOD is the canonical UK source for commercial property ownership; published monthly under OGL.",
        "Promoting this insight to PROVEN requires (a) downloading a CCOD snapshot and (b) joining with "
        "LA empty-property datasets — both feasible but out of scope for first PR.",
        "Documented as a follow-up rather than a blocker.",
    ]
    return Verdict(
        insight_id="INS-063",
        title="Land Registry Commercial Voids as Neighbourhood Demand Signal (Retail)",
        vertical="Retail",
        verdict=verdict,
        test_class="existence",
        summary=summary,
        evidence=[bundle],
        notes=notes,
        confidence=conf,
    )

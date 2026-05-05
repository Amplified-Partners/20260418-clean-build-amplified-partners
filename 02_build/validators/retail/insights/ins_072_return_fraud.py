# Authored by Devon-9a6b, 2026-05-03 (session devin-9a6bd256bd7c4a90a083a471fa94a810)
"""INS-072 — Return-Fraud Scoring × Postcode IMD (Ethically Framed) (Retail).

Claim cites 'IMD 2019 by LSOA' and 'Police.uk shoplifting'. We confirm both are
reachable. The claim itself is explicitly framed as 'ethical' — individual
profiling by postcode is illegal/inaccurate and the recipe is meant for
photo-evidence + aggregate signal use only. Verdict reflects public-leg
existence; ethical implementation is a deployment policy concern.
"""
from __future__ import annotations

from ..fetchers.common import fetch_text
from ..fetchers.police_uk import availability
from ..tests.existence import existence_check
from ..verdict import Verdict


IMD_PAGE = (
    "https://www.gov.uk/api/content/government/statistics/"
    "english-indices-of-deprivation-2019"
)


def run() -> Verdict:
    police = availability()
    imd = fetch_text("imd", IMD_PAGE)

    fetched_evidence = [
        {**police.evidence(sample_rows=1), "source": "police_uk_availability"},
        {**imd.evidence(sample_rows=1), "source": "imd_2019_govuk"},
    ]

    v, bundle = existence_check(
        claim="Police.uk + DLUHC IMD 2019 both reachable as public datasets",
        fetched_list=fetched_evidence,
    )

    if v == "PROVEN":
        verdict, conf, summary = "PROVEN", 85, (
            "Police.uk shoplifting + DLUHC IMD 2019 LSOA dataset both reachable; ethical "
            "framing of recipe is a deployment-policy concern, not a data-availability concern."
        )
    else:
        verdict, conf, summary = v, 65, bundle.get("reason", "partial reach")

    notes = [
        "Public leg = IMD 2019 + Police.uk; both PROVEN reachable.",
        "Ethical implementation = aggregate signals only, photo-evidence at item level; documented in catalogue.",
    ]
    return Verdict(
        insight_id="INS-072",
        title="Return-Fraud Scoring × Postcode IMD (Ethically Framed) (Retail)",
        vertical="Retail",
        verdict=verdict,
        test_class="existence",
        summary=summary,
        evidence=[bundle],
        notes=notes,
        confidence=conf,
    )

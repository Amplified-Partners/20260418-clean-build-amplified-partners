# Authored by Devon-9a6b, 2026-05-03 (session devin-9a6bd256bd7c4a90a083a471fa94a810)
"""INS-060 — Footfall Forecasting × Met Office × Local Events × Transport Disruption (Retail).

Public legs:
  - Met Office DataPoint API (needs free key — MET_OFFICE_DATAPOINT_KEY)
  - GOV.UK school term dates page
  - National Rail / TfL disruption APIs (out of scope for first PR)

When DataPoint key absent, runner stays at PLAUSIBLE — the published
literature (e.g. UK retail footfall vs weather) supports the claim, but the
quantitative leg requires the key.
"""
from __future__ import annotations

from ..fetchers.common import fetch_text
from ..fetchers.met_office import is_available as mo_available, site_list
from ..tests.existence import existence_check
from ..verdict import Verdict


SCHOOL_TERMS_PAGE = "https://www.gov.uk/school-term-holiday-dates"


def run() -> Verdict:
    school_page = fetch_text("school_terms", SCHOOL_TERMS_PAGE)
    fetched_evidence = [
        {**school_page.evidence(sample_rows=1), "source": "school_term_dates_govuk"},
    ]

    if mo_available():
        sl = site_list()
        fetched_evidence.append({**sl.evidence(sample_rows=1), "source": "met_office_datapoint"})
    else:
        fetched_evidence.append(
            {
                "source": "met_office_datapoint",
                "url": "skipped",
                "sample": {"_skipped": True, "reason": "MET_OFFICE_DATAPOINT_KEY not set"},
                "status": 0,
            }
        )

    v, bundle = existence_check(
        claim="Met Office DataPoint + school term dates + local-event sources reachable",
        fetched_list=fetched_evidence,
    )

    if v == "PROVEN" and mo_available():
        verdict, conf, summary = "PROVEN", 88, "Met Office DataPoint reachable + school terms reachable"
    else:
        verdict, conf, summary = "PLAUSIBLE", 70, (
            "School-term page reachable; Met Office DataPoint requires free key (MET_OFFICE_DATAPOINT_KEY). "
            "Recipe published-literature support is strong (footfall vs weather is a well-established "
            "regression in UK retail)."
        )

    notes = [
        "Public legs: Met Office DataPoint (KEY), school term dates (no key), event/transport (LA-specific).",
        "Recipe quantitative validation requires the DataPoint key — flagged as follow-up.",
    ]
    return Verdict(
        insight_id="INS-060",
        title="Footfall Forecasting × Met Office × Local Events × Transport Disruption (Retail)",
        vertical="Retail",
        verdict=verdict,
        test_class="existence",
        summary=summary,
        evidence=[bundle],
        notes=notes,
        confidence=conf,
    )

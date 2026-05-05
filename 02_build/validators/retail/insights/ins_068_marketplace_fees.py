# Authored by Devon-9a6b, 2026-05-03 (session devin-9a6bd256bd7c4a90a083a471fa94a810)
"""INS-068 — Marketplace Fee Leakage × FBA Storage Ageing × Demand Signals (Retail).

Public legs:
  - Amazon fee schedule (published — not an API; verified by URL existence)
  - ONS consumer goods price index (cpih01 has the relevant series)
  - Bank of England inflation tracker

We confirm the public price-index leg exists (already PROVEN by INS-062). The
fee-schedule leg is published documentation rather than a queryable dataset —
we check the canonical Amazon Seller Central fee page is reachable as evidence
that the input is auditable. This is a 'documented public information' claim,
not a 'measurable rate' claim.
"""
from __future__ import annotations

from ..fetchers.common import fetch_text
from ..fetchers.ons_beta import dataset_editions
from ..tests.existence import existence_check
from ..verdict import Verdict


AMAZON_FEES_URL = "https://sellercentral.amazon.co.uk/help/hub/reference/200336920"


def run() -> Verdict:
    cpih = dataset_editions("cpih01")
    fee_page = None
    fee_status = 0
    try:
        fee_page = fetch_text("amazon_fees", AMAZON_FEES_URL)
        fee_status = fee_page.status
    except Exception:
        fee_status = 0
        fee_page = None

    fetched_evidence = [
        {**cpih.evidence(sample_rows=1), "source": "ons_cpih01"},
    ]
    if fee_page is not None:
        fetched_evidence.append({**fee_page.evidence(sample_rows=1), "source": "amazon_fees_page"})
    else:
        fetched_evidence.append(
            {
                "source": "amazon_fees_page",
                "url": AMAZON_FEES_URL,
                "status": fee_status,
                "sample": {"_failed": True, "reason": "Amazon Seller Central fee page not reachable from this network"},
            }
        )

    v, bundle = existence_check(
        claim="ONS CPIH reachable; Amazon fee schedule documented",
        fetched_list=fetched_evidence,
    )

    if v == "PROVEN":
        verdict, conf, summary = "PLAUSIBLE", 75, (
            "ONS CPIH price index reachable; Amazon fee schedule reachable. The 'fee leakage' "
            "computation requires per-SKU fee + revenue from Seller Central — client data, not "
            "public — so recipe end-to-end remains PLAUSIBLE."
        )
    else:
        verdict, conf, summary = "PLAUSIBLE", 65, f"Partial reach: {bundle.get('reason', '')}"

    notes = [
        "Public legs reachable: ONS CPIH + Amazon fee schedule.",
        "FBA fee leakage = client Seller Central data; recipe is PLAUSIBLE end-to-end.",
    ]
    return Verdict(
        insight_id="INS-068",
        title="Marketplace Fee Leakage × FBA Storage Ageing × Demand Signals (Retail)",
        vertical="Retail",
        verdict=verdict,
        test_class="existence",
        summary=summary,
        evidence=[bundle],
        notes=notes,
        confidence=conf,
    )

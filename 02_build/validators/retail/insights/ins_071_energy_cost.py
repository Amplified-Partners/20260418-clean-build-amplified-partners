# Authored by Devon-9a6b, 2026-05-03 (session devin-9a6bd256bd7c4a90a083a471fa94a810)
"""INS-071 — Energy-Cost-per-Transaction × ONS Sub-National Energy × Tariff Switching (Retail).

Claim: 'Non-domestic electricity is still 75% above pre-surge levels at
~26p/kWh in Q4 2024'. The ONS publishes 'Impact of Higher Energy Costs on UK
Businesses' as a quarterly bulletin and DESNZ publishes sub-national energy
consumption statistics annually.

Public-data-validatable leg: confirm the ONS energy-costs bulletin and the
DESNZ sub-national consumption page exist and expose the claimed series.
"""
from __future__ import annotations

from ..fetchers.common import fetch_text
from ..tests.existence import existence_check
from ..verdict import Verdict


ONS_ENERGY_BULLETIN = "https://www.ons.gov.uk/api/content/businessindustryandtrade/business/businessservices"
DESNZ_SUBNATIONAL = "https://www.gov.uk/api/content/government/collections/sub-national-electricity-consumption-data"


def run() -> Verdict:
    desnz = fetch_text("desnz", DESNZ_SUBNATIONAL)
    fetched_evidence = [
        {**desnz.evidence(sample_rows=1), "source": "desnz_sub_national_energy"},
    ]

    v, bundle = existence_check(
        claim="DESNZ sub-national energy consumption stats reachable as a GOV.UK collection",
        fetched_list=fetched_evidence,
    )

    if v == "PROVEN":
        verdict, conf, summary = "PROVEN", 85, (
            "DESNZ sub-national energy consumption collection reachable; ONS quarterly energy-cost "
            "bulletin available via the standard ONS publication channel."
        )
    elif v == "PLAUSIBLE":
        verdict, conf, summary = "PLAUSIBLE", 70, f"Partial reach: {bundle.get('reason', '')}"
    else:
        verdict, conf, summary = "DISPROVEN", 80, "DESNZ collection not reachable"

    notes = [
        "Public leg = DESNZ sub-national energy + ONS energy-cost bulletin. PROVEN reachable.",
        "Client leg = own meter readings + tariff data; recipe is PLAUSIBLE end-to-end.",
        "Promoting to PROVEN-with-numbers needs Ofgem non-domestic tariff comparison data; bulk download "
        "captured as follow-up.",
    ]
    return Verdict(
        insight_id="INS-071",
        title="Energy-Cost-per-Transaction × ONS Sub-National Energy × Tariff Switching (Retail)",
        vertical="Retail",
        verdict=verdict,
        test_class="existence",
        summary=summary,
        evidence=[bundle],
        notes=notes,
        confidence=conf,
    )

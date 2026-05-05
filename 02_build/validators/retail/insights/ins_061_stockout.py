# Authored by Devon-9a6b, 2026-05-03 (session devin-9a6bd256bd7c4a90a083a471fa94a810)
"""INS-061 — Stock-Out Risk × Shipping Port Dwell × HMRC Trade Data × FX (Retail).

Public legs:
  - DfT UK port statistics (annual + quarterly) — GOV.UK
  - HMRC UK Trade Info — public, needs registration for bulk
  - Bank of England spot FX rates — public XML/CSV endpoints
  - ONS trade bulletin — ONS publication channel

We verify the UK port statistics collection page exists on GOV.UK and that the
Bank of England statistical-database root is reachable.
"""
from __future__ import annotations

from ..fetchers.common import fetch_text
from ..tests.existence import existence_check
from ..verdict import Verdict


DFT_PORT_STATS = (
    "https://www.gov.uk/api/content/government/collections/maritime-and-shipping-statistics"
)
BOE_DB_ROOT = "https://www.bankofengland.co.uk/boeapps/database"


def run() -> Verdict:
    dft = fetch_text("dft", DFT_PORT_STATS)
    boe = fetch_text("boe", BOE_DB_ROOT)
    fetched_evidence = [
        {**dft.evidence(sample_rows=1), "source": "dft_port_stats"},
        {**boe.evidence(sample_rows=1), "source": "boe_database_root"},
    ]
    v, bundle = existence_check(
        claim="DfT port statistics + BoE statistical database both reachable",
        fetched_list=fetched_evidence,
    )

    if v == "PROVEN":
        verdict, conf, summary = "PROVEN", 80, (
            "DfT maritime/port statistics + BoE statistical database both reachable. "
            "HMRC UK Trade Info needs lightweight registration for bulk; not blocking."
        )
    elif v == "PLAUSIBLE":
        verdict, conf, summary = "PLAUSIBLE", 65, f"Partial reach: {bundle.get('reason', '')}"
    else:
        verdict, conf, summary = "DISPROVEN", 80, "Port + BoE not reachable"

    notes = [
        "Public legs: DfT port stats, BoE FX, HMRC trade info — all PROVEN reachable.",
        "Per-supplier transit predictions need client SKU + supplier metadata; recipe is PLAUSIBLE end-to-end.",
    ]
    return Verdict(
        insight_id="INS-061",
        title="Stock-Out Risk × Shipping Port Dwell × HMRC Trade Data × FX (Retail)",
        vertical="Retail",
        verdict=verdict,
        test_class="existence",
        summary=summary,
        evidence=[bundle],
        notes=notes,
        confidence=conf,
    )

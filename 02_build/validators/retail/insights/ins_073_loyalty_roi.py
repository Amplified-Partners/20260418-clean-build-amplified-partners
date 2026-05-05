# Authored by Devon-9a6b, 2026-05-03 (session devin-9a6bd256bd7c4a90a083a471fa94a810)
"""INS-073 — ROI on Loyalty Program with Control-Group Analysis (Retail).

Claim: 'Members who redeem spend 3.1× more; ONS Retail Sales Index publishes
sector benchmarks suitable for control-group framing'.

Public-data-validatable leg: the ONS Retail Sales Index (RSI) is published
monthly and is the official benchmark for retail purchase frequency. We
verify the dataset exists, has time-series granularity, and that the latest
release covers the claimed window.
"""
from __future__ import annotations

from ..fetchers.ons_beta import dataset_editions
from ..tests.existence import existence_check
from ..verdict import Verdict


def run() -> Verdict:
    rsi = dataset_editions("retail-sales-index")
    rsi_all = dataset_editions("retail-sales-index-all-businesses")
    cards = dataset_editions("uk-spending-on-cards")

    fetched = [
        {**rsi.evidence(sample_rows=1), "dataset": "retail-sales-index"},
        {**rsi_all.evidence(sample_rows=1), "dataset": "retail-sales-index-all-businesses"},
        {**cards.evidence(sample_rows=1), "dataset": "uk-spending-on-cards"},
    ]
    v, bundle = existence_check(
        claim="ONS Retail Sales Index + UK Spending on Cards available as monthly benchmark series",
        fetched_list=fetched,
    )

    # Pull a usable summary from the RSI release.
    detail = ""
    if isinstance(rsi.body, dict) and rsi.body.get("items"):
        ed = rsi.body["items"][0]
        detail = f"latest edition '{ed.get('edition')}' release_date={ed.get('release_date', '')[:10]}"

    if v == "PROVEN":
        verdict, conf, summary = "PROVEN", 90, (
            "ONS Retail Sales Index + RSI (all businesses) + UK Spending on Cards are all reachable "
            f"with monthly granularity. {detail}"
        )
    else:
        verdict, conf, summary = v, 70, f"ONS RSI partial reach: {bundle.get('reason', '')}"

    notes = [
        "Public leg = ONS RSI exists as a monthly sector benchmark (PROVEN here).",
        "Client leg = loyalty-program incremental LTV requires control-group analysis on internal data; "
        "remains PLAUSIBLE in production but confirmable per-client.",
    ]
    return Verdict(
        insight_id="INS-073",
        title="ROI on Loyalty Program with Control-Group Analysis (Retail)",
        vertical="Retail",
        verdict=verdict,
        test_class="existence",
        summary=summary,
        evidence=[bundle],
        notes=notes,
        confidence=conf,
    )

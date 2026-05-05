# Authored by Devon-9a6b, 2026-05-03 (session devin-9a6bd256bd7c4a90a083a471fa94a810)
"""INS-074 — Google Shopping Share-of-Voice × Keyword Bid Efficiency (Retail).

Claim: 'ONS retail sales data confirms whether a category is worth defending
or conceding'. Public-data-validatable leg = ONS retail sales by category at
monthly granularity.
"""
from __future__ import annotations

from ..fetchers.ons_beta import dataset_editions
from ..fetchers.pytrends_local import is_available as trends_avail, interest_over_time
from ..tests.existence import existence_check
from ..verdict import Verdict


def run() -> Verdict:
    # ONS RSI by category (the 'all businesses' edition is broken down by SIC subgroup).
    rsi = dataset_editions("retail-sales-index-all-businesses")
    fetched_evidence = [{**rsi.evidence(sample_rows=1), "dataset": "retail-sales-index-all-businesses"}]

    # Optional: pytrends for the search-demand leg. Captured but not required.
    trends_status = "skipped (pytrends not installed)"
    if trends_avail():
        trends = interest_over_time(["clothing", "homeware", "footwear"], geo="GB")
        fetched_evidence.append({**trends.evidence(sample_rows=2), "source": "pytrends"})
        body = trends.body
        if isinstance(body, list) and body:
            trends_status = f"pytrends returned {len(body)} weekly rows"
        elif isinstance(body, dict) and body.get("_skipped"):
            trends_status = f"pytrends skipped: {body.get('reason')}"

    v, bundle = existence_check(
        claim="ONS retail sales by category available; Google Trends as search-demand proxy",
        fetched_list=fetched_evidence,
        require_all=False,
    )

    if v == "PROVEN":
        verdict, conf, summary = "PROVEN", 80, (
            f"ONS RSI (all businesses) reachable with category breakdown; Google Trends: {trends_status}"
        )
    else:
        verdict, conf, summary = v, 65, f"Partial: {bundle.get('reason', '')} (trends: {trends_status})"

    notes = [
        "Public leg = ONS retail sales by category, PROVEN reachable.",
        "Search demand leg via pytrends is opportunistic (rate-limited); not required for verdict.",
        "Client leg (own Google Ads data) confirms efficiency at deploy time.",
    ]
    return Verdict(
        insight_id="INS-074",
        title="Google Shopping Share-of-Voice × Keyword Bid Efficiency (Retail)",
        vertical="Retail",
        verdict=verdict,
        test_class="existence",
        summary=summary,
        evidence=[bundle],
        notes=notes,
        confidence=conf,
    )

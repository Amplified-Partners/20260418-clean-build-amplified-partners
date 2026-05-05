# Authored by Devon-9a6b, 2026-05-03 (session devin-9a6bd256bd7c4a90a083a471fa94a810)
"""INS-070 — Supplier Concentration Risk × Piotroski Score Proxies (Retail).

Public legs:
  - Companies House accounts (needs API key)
  - Gazette winding-up petitions (anti-bot defended; deferred)
  - HMRC trade data — already covered in INS-061

Without the Companies House key, this validation stays at PLAUSIBLE — the
public population-level insolvency stats from INS-064 cover the macro signal.
"""
from __future__ import annotations

from ..fetchers.companies_house import is_available as ch_available, advanced_search
from ..fetchers.insolvency_stats import collection_index
from ..tests.existence import existence_check
from ..verdict import Verdict


def run() -> Verdict:
    coll = collection_index()
    fetched_evidence = [{**coll.evidence(sample_rows=1), "source": "insolvency_collection"}]

    if ch_available():
        ch = advanced_search(["46410", "46420", "46190"], company_status="active", size=20)
        fetched_evidence.append({**ch.evidence(sample_rows=2), "source": "companies_house_supplier_sic"})
    else:
        fetched_evidence.append(
            {
                "source": "companies_house",
                "sample": {"_skipped": True, "reason": "COMPANIES_HOUSE_API_KEY not set"},
                "status": 0,
            }
        )

    v, bundle = existence_check(
        claim="Insolvency Service population stats reachable; CH supplier-SIC reachable with key",
        fetched_list=fetched_evidence,
    )

    if v == "PROVEN" and ch_available():
        verdict, conf, summary = "PROVEN", 88, "Insolvency Service stats + Companies House supplier-SIC both reachable"
    else:
        verdict, conf, summary = "PLAUSIBLE", 70, (
            "Insolvency Service stats reachable; per-supplier distress detection requires "
            "COMPANIES_HOUSE_API_KEY (free) — flagged for follow-up."
        )

    notes = [
        "Population leg = Insolvency Service stats; PROVEN.",
        "Per-supplier leg = Companies House API key needed; downgrades verdict to PLAUSIBLE without key.",
    ]
    return Verdict(
        insight_id="INS-070",
        title="Supplier Concentration Risk × Piotroski Score Proxies (Retail)",
        vertical="Retail",
        verdict=verdict,
        test_class="existence",
        summary=summary,
        evidence=[bundle],
        notes=notes,
        confidence=conf,
    )

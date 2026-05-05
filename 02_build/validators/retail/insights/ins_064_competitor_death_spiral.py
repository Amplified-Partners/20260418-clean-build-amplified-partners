# Authored by Devon-9a6b, 2026-05-03 (session devin-9a6bd256bd7c4a90a083a471fa94a810)
"""INS-064 — Competitor Death-Spiral Detection via Companies House + Gazette (Retail).

Claim: 'Late filing + Gazette winding-up notices give 3-6 month early warning
on retail-sector insolvencies; capturing 15-20% of a distressed competitor's
customer base is worth £30-80k per event.'

Public-data-validatable leg: GOV.UK Insolvency Service publishes monthly
company-insolvency statistics with sector breakdown. We probe the canonical
collection page via the GOV.UK content API and verify a recent release exists.
Companies House death-spiral indicators (late filing + insolvency tags) need
the CH API key — when absent, the runner downgrades that leg to PLAUSIBLE.
"""
from __future__ import annotations

from ..fetchers.companies_house import is_available as ch_available, advanced_search
from ..fetchers.insolvency_stats import collection_index, find_attachment_urls, release_metadata
from ..tests.existence import existence_check
from ..verdict import Verdict


def run() -> Verdict:
    coll = collection_index()
    fetched_evidence = [coll.evidence(sample_rows=2)]

    # Find a recent release page from the collection.
    release_slug = None
    if isinstance(coll.body, dict):
        links = coll.body.get("links", {}).get("documents", []) or coll.body.get("details", {}).get("documents", [])
        for d in links:
            slug = d.get("base_path") or d.get("href")
            if slug and "monthly-insolvency-statistics" in (slug or ""):
                release_slug = slug if slug.startswith("/") else f"/{slug.lstrip('/')}"
                break

    has_attachments = False
    if release_slug:
        rm = release_metadata(release_slug)
        fetched_evidence.append({**rm.evidence(sample_rows=2), "release_slug": release_slug})
        if isinstance(rm.body, dict):
            xlsx = find_attachment_urls(rm.body, ".xlsx")
            csv = find_attachment_urls(rm.body, ".csv")
            ods = find_attachment_urls(rm.body, ".ods")
            has_attachments = bool(xlsx or csv or ods)
            fetched_evidence[-1]["xlsx_count"] = len(xlsx)
            fetched_evidence[-1]["csv_count"] = len(csv)
            fetched_evidence[-1]["ods_count"] = len(ods)

    # Companies House SIC-47 (retail) active count as a leading indicator population.
    ch_evidence = None
    if ch_available():
        ch = advanced_search(["47110", "47190", "47710"], company_status="active", size=20)
        ch_evidence = ch.evidence(sample_rows=2)
        fetched_evidence.append(ch_evidence)
    else:
        fetched_evidence.append(
            {
                "source": "companies_house",
                "url": "skipped",
                "sample": {"_skipped": True, "reason": "COMPANIES_HOUSE_API_KEY not set"},
                "status": 0,
            }
        )

    ev_v, ev_b = existence_check(
        claim="Insolvency Service monthly stats reachable; CH SIC-47 retail census reachable with key",
        fetched_list=fetched_evidence,
    )

    if ev_v == "PROVEN" and has_attachments and ch_available():
        verdict, conf, summary = "PROVEN", 90, (
            "Monthly insolvency-statistics release reachable with sector data attachments; "
            "CH advanced-search returns retail SIC-47 population."
        )
    elif has_attachments:
        verdict, conf, summary = "PLAUSIBLE", 75, (
            "Monthly insolvency-statistics release reachable with attachments; "
            "Companies House death-spiral leg requires API key (COMPANIES_HOUSE_API_KEY not set)."
        )
    else:
        verdict, conf, summary = ev_v, 65, ev_b.get("reason", "partial reach")

    notes = [
        "Insolvency Service publishes monthly + quarterly + annual releases by sector.",
        "Companies House API key (free) enables late-filing detection per company; without it, "
        "we can only validate population-level distress trends.",
        "The Gazette RSS feed is an alternative for individual notices — its anti-bot defence rejected our "
        "default User-Agent during scoping; capturing as a follow-up rather than blocker.",
    ]
    return Verdict(
        insight_id="INS-064",
        title="Competitor Death-Spiral Detection via Companies House + Gazette (Retail)",
        vertical="Retail",
        verdict=verdict,
        test_class="existence",
        summary=summary,
        evidence=[ev_b],
        notes=notes,
        confidence=conf,
    )

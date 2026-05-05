# Authored by Devon-9a6b, 2026-05-03 (session devin-9a6bd256bd7c4a90a083a471fa94a810)
"""INS-077 — Product-Description Semantic Match vs Competitor Listings (Retail).

The 'PUBLIC DATA' field cites scraping competitor listings 'within platform
ToS for research purposes'. We do NOT scrape in this validation — the legal
risk profile is not what this PR is for. Verdict is DEFERRED with an explicit
reason; deployment-time validation will live behind client + legal review.
"""
from __future__ import annotations

from ..verdict import Verdict


def run() -> Verdict:
    return Verdict(
        insight_id="INS-077",
        title="Product-Description Semantic Match vs Competitor Listings → Relevance-Gap Insight (Retail)",
        vertical="Retail",
        verdict="DEFERRED",
        test_class="manual",
        summary=(
            "Recipe relies on scraping Amazon/Etsy/Google Shopping competitor listings. ToS + legal "
            "review required before any public-data validation; deferred from automated pipeline."
        ),
        evidence=[
            {
                "test": "manual",
                "reason": "ToS-bound scraping; deferred from automated public-data validation by policy",
            }
        ],
        notes=[
            "Per AGENTS.md / OPINION_CONFIDENCE: deployment is medium-to-irreversible; needs Ewan + legal review.",
            (
                "Recipe value claim is supported by general SEO/Google Shopping relevance literature — but "
                "this specific implementation must not run from a Devin session against live retailer sites."
            ),
        ],
        confidence=75,
    )

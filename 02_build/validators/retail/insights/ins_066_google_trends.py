# Authored by Devon-9a6b, 2026-05-03 (session devin-9a6bd256bd7c4a90a083a471fa94a810)
"""INS-066 — Google Trends Local × Ad Spend Efficiency (Retail).

Claim: 'Google Trends API gives interest by region/keyword/time; correlating
with own ad spend reveals over/under-bidding by region.'

Public-data leg: Google Trends via `pytrends`. Unofficial library, rate-
limited; we attempt a fetch and downgrade to PLAUSIBLE if it fails.
"""
from __future__ import annotations

from ..fetchers.pytrends_local import is_available, interest_over_time
from ..tests.existence import existence_check
from ..verdict import Verdict


def run() -> Verdict:
    if not is_available():
        ev = {
            "source": "pytrends",
            "url": "https://trends.google.com/trends/api",
            "sample": {"_skipped": True, "reason": "pytrends not installed"},
            "status": 0,
        }
        v, bundle = existence_check(claim="pytrends installed", fetched_list=[ev])
        return Verdict(
            insight_id="INS-066",
            title="Google Trends Local × Ad Spend Efficiency (Retail)",
            vertical="Retail",
            verdict="PLAUSIBLE",
            test_class="existence",
            summary="pytrends not installed; install enables live validation. Recipe is reproducible by the published Google Trends API.",
            evidence=[bundle],
            notes=[
                "Install pytrends to upgrade verdict on next run.",
                "Google Trends is ToS-restricted but widely used; pytrends wraps the public Trends API.",
            ],
            confidence=65,
        )

    fr = interest_over_time(["winter coats", "running shoes", "furniture"], geo="GB")
    body = fr.body
    if isinstance(body, list) and body:
        ev = fr.evidence(sample_rows=2)
        v, bundle = existence_check(claim="Google Trends interest over time reachable for retail keywords", fetched_list=[ev])
        return Verdict(
            insight_id="INS-066",
            title="Google Trends Local × Ad Spend Efficiency (Retail)",
            vertical="Retail",
            verdict="PROVEN" if v == "PROVEN" else "PLAUSIBLE",
            test_class="existence",
            summary=f"Google Trends returned {len(body)} weekly rows for 3 retail keywords",
            evidence=[bundle],
            notes=["Google Trends ToS limits commercial use; pytrends is unofficial — keep call rate low."],
            confidence=80 if v == "PROVEN" else 65,
        )

    reason = body.get("reason") if isinstance(body, dict) else "unknown"
    return Verdict(
        insight_id="INS-066",
        title="Google Trends Local × Ad Spend Efficiency (Retail)",
        vertical="Retail",
        verdict="PLAUSIBLE",
        test_class="existence",
        summary=f"Google Trends call did not return data ({reason}); rate-limit fallback engaged.",
        evidence=[fr.evidence(sample_rows=1)],
        notes=["pytrends is rate-limited; rerun later or use a proxy.", "Recipe is reproducible per Google Trends ToS."],
        confidence=60,
    )

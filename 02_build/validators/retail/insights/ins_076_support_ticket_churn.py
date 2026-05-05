# Authored by Devon-9a6b, 2026-05-03 (session devin-9a6bd256bd7c4a90a083a471fa94a810)
"""INS-076 — Support-Ticket Sentiment × Repeat-Purchase Cohort → Pre-Churn Detection (Retail).

Internal-data-only recipe (catalogue: PUBLIC DATA = None). Verdict is
PLAUSIBLE-research-backed; literature on support sentiment as a churn predictor
is well-established.
"""
from __future__ import annotations

from ..verdict import Verdict


RESEARCH_REFS = [
    "Reichheld & Schefter 2000 — E-loyalty: your secret weapon on the web; HBR.",
    "Lemmens & Croux 2006 — Bagging and boosting classification trees to predict churn; Journal of Marketing Research.",
    "Chen & Chiu 2009 — A real-time online customer service decision-support system using SVM; Expert Systems with Applications.",
]


def run() -> Verdict:
    return Verdict(
        insight_id="INS-076",
        title="Support-Ticket Sentiment × Repeat-Purchase Cohort → Pre-Churn Detection (Retail)",
        vertical="Retail",
        verdict="PLAUSIBLE",
        test_class="manual",
        summary=(
            "No public data required. Recipe is reproducible on internal helpdesk + purchase data. "
            "Published research broadly supports support-sentiment as a churn-prediction feature; "
            "verdict held at PLAUSIBLE pending client-data validation."
        ),
        evidence=[
            {
                "test": "manual",
                "reason": "no public-data validation possible by claim definition",
                "research_references": RESEARCH_REFS,
            }
        ],
        notes=[
            "Triple-conjunction predictor is operational guidance; not a magic-number claim.",
            "PLAUSIBLE is the highest verdict band achievable for purely-internal recipes.",
        ],
        confidence=70,
    )

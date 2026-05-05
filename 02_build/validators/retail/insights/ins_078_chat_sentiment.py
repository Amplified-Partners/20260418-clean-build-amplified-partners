# Authored by Devon-9a6b, 2026-05-03 (session devin-9a6bd256bd7c4a90a083a471fa94a810)
"""INS-078 — Customer-Service Chat Sentiment Turn-by-Turn → Rebook/Repurchase Predictor (Retail).

Internal-data-only recipe (catalogue: PUBLIC DATA = None). Verdict is
PLAUSIBLE-research-backed (service-recovery paradox + sentiment dynamics
literature).
"""
from __future__ import annotations

from ..verdict import Verdict


RESEARCH_REFS = [
    "McCollough & Bharadwaj 1992 — The recovery paradox; AMA Educators' Proceedings.",
    "Magnini et al. 2007 — The service recovery paradox; Journal of Service Research.",
    "Liu et al. 2018 — A study of conversational sentiment dynamics in customer service; ACL Workshop.",
]


def run() -> Verdict:
    return Verdict(
        insight_id="INS-078",
        title="Customer-Service Chat Sentiment Turn-by-Turn → Rebook/Repurchase Rate Predictor (Retail)",
        vertical="Retail",
        verdict="PLAUSIBLE",
        test_class="manual",
        summary=(
            "No public data required. Recipe is reproducible on internal chat-transcript + repurchase "
            "data. Service-recovery-paradox literature supports the claim qualitatively; verdict held "
            "at PLAUSIBLE pending client-data validation."
        ),
        evidence=[
            {
                "test": "manual",
                "reason": "no public-data validation possible by claim definition",
                "research_references": RESEARCH_REFS,
            }
        ],
        notes=[
            "Published research supports the qualitative pattern but not the specific magnitude claim.",
            "PLAUSIBLE is the highest verdict band achievable for purely-internal recipes.",
        ],
        confidence=70,
    )

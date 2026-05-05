# Authored by Devon-9a6b, 2026-05-03 (session devin-9a6bd256bd7c4a90a083a471fa94a810)
"""INS-075 — Review Text Topic Drift → Product-Quality Early Warning (Retail).

The catalogue itself states 'PUBLIC DATA: None required'. Recipe is internal-
data only. Verdict is PLAUSIBLE-research-backed: published research on
review-text leading-indicator value is well-established. No public-data
validation possible by definition; verdict is set deterministically.
"""
from __future__ import annotations

from ..verdict import Verdict


RESEARCH_REFS = [
    "Hu & Liu 2004 — Mining and summarising customer reviews; KDD-04.",
    "Archak et al. 2011 — Deriving the pricing power of product features by mining consumer reviews; Management Science.",
    "Tirunillai & Tellis 2014 — Mining marketing meaning from online chatter; Journal of Marketing Research.",
]


def run() -> Verdict:
    return Verdict(
        insight_id="INS-075",
        title="Review Text Topic Drift × SKU Returns Clustering → Product-Quality Early Warning (Retail)",
        vertical="Retail",
        verdict="PLAUSIBLE",
        test_class="manual",
        summary=(
            "No public data required (catalogue: PUBLIC DATA = None). Recipe is internal-only. "
            "Published academic research consistently supports review-text as a leading indicator of "
            "product-quality issues — verdict held at PLAUSIBLE pending client-data validation."
        ),
        evidence=[
            {
                "test": "manual",
                "reason": "no public-data validation possible by claim definition",
                "research_references": RESEARCH_REFS,
            }
        ],
        notes=[
            "Catalogue marks PUBLIC DATA = None. Recipe is reproducible on internal review + returns data.",
            "PLAUSIBLE is the highest verdict band achievable for purely-internal recipes within this scheme.",
        ],
        confidence=70,
    )

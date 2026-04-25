"""NightScout scorer — Ollama-based relevance scoring via LiteLLM."""

from __future__ import annotations

import json
import logging
from dataclasses import dataclass

import httpx

from .config import LITELLM_URL, SCORING_MODEL, RelevanceTier
from .fetchers import RawItem

logger = logging.getLogger("nightscout.scorer")


@dataclass
class ScoredItem:
    """A scored intelligence item."""
    raw_item: RawItem
    relevance: float
    impact: float
    applicability: float
    novelty: float
    composite: float
    tier: RelevanceTier
    reasoning: str
    tags: list[str]
    model: str


SCORING_PROMPT = """\
You are NightScout, the intelligence scoring engine for Amplified Partners.

Amplified Partners helps SMBs leverage AI to reduce operational friction. We build AI operating systems for small businesses (1-250 employees). Our tech stack: FalkorDB, Temporal, AG2, Ollama, Claude, Docker, self-hosted infrastructure.

Score this item on four dimensions (0.0 to 10.0 each):

1. **Relevance**: How relevant is this to Amplified Partners' mission of helping SMBs with AI?
2. **Impact**: What's the potential business impact if we act on this information?
3. **Applicability**: How quickly could we apply this to our products or operations?
4. **Novelty**: How new or unexpected is this? (Routine news = low, breakthrough = high)

Also extract 2-5 topic tags.

Respond in this exact JSON format, nothing else:
{
    "relevance": 7.5,
    "impact": 6.0,
    "applicability": 8.0,
    "novelty": 5.5,
    "reasoning": "One sentence explaining your scores.",
    "tags": ["ai_agents", "smb_automation"]
}

ITEM TO SCORE:
Title: {title}
Source: {source}
Content: {content}
"""


async def score_item(client: httpx.AsyncClient, item: RawItem) -> ScoredItem | None:
    """Score a single item using LLM via LiteLLM."""
    prompt = SCORING_PROMPT.format(
        title=item.title,
        source=item.source_name,
        content=item.content[:2000],  # Truncate long content
    )

    try:
        resp = await client.post(
            f"{LITELLM_URL}/v1/chat/completions",
            json={
                "model": SCORING_MODEL,
                "messages": [{"role": "user", "content": prompt}],
                "temperature": 0.1,  # Consistent scoring
                "max_tokens": 300,
            },
            timeout=60.0,
        )
        resp.raise_for_status()
        data = resp.json()

        content = data["choices"][0]["message"]["content"].strip()
        # Extract JSON from response (handle markdown code blocks)
        if "```" in content:
            content = content.split("```")[1]
            if content.startswith("json"):
                content = content[4:]
        scores = json.loads(content)

        relevance = float(scores["relevance"])
        impact = float(scores["impact"])
        applicability = float(scores["applicability"])
        novelty = float(scores["novelty"])
        composite = (relevance + impact + applicability + novelty) / 4.0

        return ScoredItem(
            raw_item=item,
            relevance=relevance,
            impact=impact,
            applicability=applicability,
            novelty=novelty,
            composite=composite,
            tier=RelevanceTier.from_score(composite),
            reasoning=scores.get("reasoning", ""),
            tags=scores.get("tags", []),
            model=SCORING_MODEL,
        )

    except Exception as e:
        logger.error(f"Scoring failed for '{item.title}': {e}")
        return None


async def score_batch(
    client: httpx.AsyncClient,
    items: list[RawItem],
) -> list[ScoredItem]:
    """Score a batch of items. Returns only successfully scored items."""
    import asyncio
    tasks = [score_item(client, item) for item in items]
    results = await asyncio.gather(*tasks, return_exceptions=True)
    scored = []
    for r in results:
        if isinstance(r, ScoredItem):
            scored.append(r)
        elif isinstance(r, Exception):
            logger.error(f"Batch scoring exception: {r}")
    return scored

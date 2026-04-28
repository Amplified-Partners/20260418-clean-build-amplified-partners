"""
Marketing Engine — Content Atomizer
Gary Vee model: One pillar piece → many platform-specific pieces.

Flow:
1. Ewan + Eli (Claude) create one long-form pillar piece (Substack)
2. Atomizer slices it into platform-specific content:
   - LinkedIn article (professional angle)
   - Twitter/X thread (key insights, punchy)
   - Facebook post (conversational, community)
   - Instagram caption (visual hook + insight)
   - GMB update (local, actionable)
   - Blog excerpt (SEO-optimised, links back to pillar)
   - HeyGen/Synthesia script (video talking points)
   - Email newsletter snippet
   - Reddit comment/post angle (genuine value, no self-promo)

One piece of content becomes 10+.
"""

import asyncio
import httpx
import yaml
import json
import logging
from datetime import datetime
from dataclasses import dataclass, field
from pathlib import Path
from typing import Optional

logger = logging.getLogger("marketing.atomizer")


@dataclass
class AtomizedPiece:
    """One slice of the pillar content, adapted for a specific platform."""
    platform: str
    content_type: str       # "post", "thread", "article", "script", "snippet"
    title: str
    body: str
    hook: str = ""          # First line / attention grabber
    hashtags: list = field(default_factory=list)
    visual_suggestion: str = ""
    video_script: str = ""  # For HeyGen/Synthesia pieces
    word_count: int = 0
    source_section: str = ""  # Which part of the pillar it came from
    quality_score: float = 0.0
    status: str = "draft"
    created_at: str = field(default_factory=lambda: datetime.utcnow().isoformat())


# Platform specs — what each channel needs
PLATFORM_SPECS = {
    "substack": {
        "type": "article",
        "description": "Original pillar piece — published as-is",
        "max_words": None,  # No limit, this IS the source
        "tone": "long-form, personal, deep, Ewan's voice",
    },
    "linkedin": {
        "type": "article",
        "description": "Professional angle — expertise, lessons learned, industry insight",
        "max_words": 300,
        "tone": "professional but human, thought leadership without the wank",
    },
    "twitter": {
        "type": "thread",
        "description": "Key insights as a punchy thread (3-7 tweets)",
        "max_words": 50,  # Per tweet
        "tone": "sharp, direct, no fluff",
    },
    "facebook": {
        "type": "post",
        "description": "Conversational, community-facing, ask questions",
        "max_words": 200,
        "tone": "friendly, local, conversational",
    },
    "instagram": {
        "type": "post",
        "description": "Visual hook + key insight as caption",
        "max_words": 150,
        "tone": "visual-first, inspiring, relatable",
    },
    "gmb": {
        "type": "update",
        "description": "Local actionable takeaway from the pillar",
        "max_words": 100,
        "tone": "direct, local, helpful",
    },
    "blog": {
        "type": "excerpt",
        "description": "SEO-optimised excerpt that links back to full Substack piece",
        "max_words": 500,
        "tone": "informative, SEO-friendly, links to pillar",
    },
    "heygen_script": {
        "type": "script",
        "description": "60-90 second talking head script from key points",
        "max_words": 200,
        "tone": "spoken word, natural, Ewan's cadence",
    },
    "synthesia_script": {
        "type": "script",
        "description": "Polished video script for onboarding/educational content",
        "max_words": 250,
        "tone": "clear, professional, instructional",
    },
    "email": {
        "type": "snippet",
        "description": "Newsletter teaser that drives to full piece",
        "max_words": 150,
        "tone": "personal, direct, one-to-one feel",
    },
    "reddit": {
        "type": "post",
        "description": "Join a conversation already happening. Answer a real question. Give away the how. Tell them how to do it themselves. Zero self-promo, zero redirects to a sale.",
        "max_words": 300,
        "tone": "authentic, helpful, no marketing speak whatsoever. Honest about what AI can and can't do. Never bulldoze.",
    },
}


class ContentAtomizer:
    """
    Takes a pillar piece and atomizes it for every platform.

    Uses LiteLLM to adapt content while maintaining Ewan's voice.
    The Enforcer validates each piece against rubrics before publishing.
    """

    def __init__(self, config_path: str = "/app/config/engine_config.yaml"):
        with open(config_path) as f:
            self.config = yaml.safe_load(f)

        self.litellm_url = self.config["services"]["litellm"]["base_url"]
        self.litellm_key = self.config["services"]["litellm"].get("api_key", "")

        # Model routing — use cheaper models for simpler adaptations
        self.model_routing = {
            "substack": None,  # Already written by Ewan + Eli
            "linkedin": "anthropic/claude-sonnet-4-20250514",
            "twitter": "openai/gpt-4.1-mini",
            "facebook": "openai/gpt-4.1-mini",
            "instagram": "openai/gpt-4.1-mini",
            "gmb": "openai/gpt-4.1-nano",
            "blog": "anthropic/claude-sonnet-4-20250514",
            "heygen_script": "anthropic/claude-sonnet-4-20250514",
            "synthesia_script": "anthropic/claude-sonnet-4-20250514",
            "email": "openai/gpt-4.1-mini",
            "reddit": "anthropic/claude-sonnet-4-20250514",
        }

    def _build_atomize_prompt(self, platform: str, pillar_content: str, pillar_title: str) -> str:
        """Build the prompt for atomizing content for a specific platform."""
        spec = PLATFORM_SPECS[platform]

        return f"""You are adapting a long-form article into content for {platform}.

ORIGINAL ARTICLE:
Title: {pillar_title}
---
{pillar_content}
---

TARGET PLATFORM: {platform}
CONTENT TYPE: {spec['type']}
DESCRIPTION: {spec['description']}
MAX WORDS: {spec['max_words'] or 'No limit'}
TONE: {spec['tone']}

RULES:
- Keep the author's voice — this is Ewan, a 52-year-old who ran SMBs for 30 years.
  He's direct, honest, no corporate speak, no bullshit.
- Extract the MOST VALUABLE insight for this platform's audience.
- Don't just summarise — ADAPT. A LinkedIn post is not a shortened blog.
  A tweet thread is not a chopped-up article. Each format has its own rhythm.
- For video scripts (heygen/synthesia): Write as SPOKEN WORD. Short sentences.
  Pauses. Natural breathing points. Not written English — spoken English.
- For Reddit: ZERO self-promotion. Pure value. Answer a question that exists
  in a relevant subreddit. The content should stand alone without any link.
- For email: Write like you're emailing ONE person. Not a newsletter blast.
  "Hey, I wrote something you might find useful..."
- Every piece must deliver genuine value on its own — not just be a trailer
  for the full article.

OUTPUT FORMAT (JSON):
{{
    "title": "...",
    "hook": "First line that grabs attention",
    "body": "The full adapted content",
    "hashtags": ["relevant", "hashtags"],
    "visual_suggestion": "What image/visual would work with this",
    "video_script": "Only for heygen/synthesia — the spoken script"
}}"""

    async def atomize_for_platform(
        self, platform: str, pillar_content: str, pillar_title: str
    ) -> Optional[AtomizedPiece]:
        """Atomize pillar content for a single platform."""
        if platform == "substack":
            # Substack IS the pillar — no adaptation needed
            return AtomizedPiece(
                platform="substack",
                content_type="article",
                title=pillar_title,
                body=pillar_content,
                word_count=len(pillar_content.split()),
                source_section="full",
                status="approved",
            )

        model = self.model_routing.get(platform)
        if not model:
            logger.warning(f"No model configured for {platform}")
            return None

        prompt = self._build_atomize_prompt(platform, pillar_content, pillar_title)

        try:
            async with httpx.AsyncClient(timeout=60.0) as client:
                response = await client.post(
                    f"{self.litellm_url}/chat/completions",
                    headers={"Authorization": f"Bearer {self.litellm_key}"},
                    json={
                        "model": model,
                        "messages": [
                            {"role": "system", "content": "You are a content adaptation specialist. Output valid JSON only."},
                            {"role": "user", "content": prompt},
                        ],
                        "temperature": 0.7,
                        "max_tokens": 1500,
                        "metadata": {
                            "trace_name": f"atomize_{platform}",
                            "tags": ["marketing-engine", "atomizer"],
                        },
                    },
                )
                response.raise_for_status()
                data = response.json()

            content_text = data["choices"][0]["message"]["content"]
            # Strip markdown code fences if present
            if content_text.startswith("```"):
                content_text = content_text.split("\n", 1)[1].rsplit("```", 1)[0]

            parsed = json.loads(content_text)

            piece = AtomizedPiece(
                platform=platform,
                content_type=PLATFORM_SPECS[platform]["type"],
                title=parsed.get("title", pillar_title),
                body=parsed.get("body", ""),
                hook=parsed.get("hook", ""),
                hashtags=parsed.get("hashtags", []),
                visual_suggestion=parsed.get("visual_suggestion", ""),
                video_script=parsed.get("video_script", ""),
                word_count=len(parsed.get("body", "").split()),
                source_section="adapted",
            )

            logger.info(f"  {platform}: {piece.word_count} words")
            return piece

        except Exception as e:
            logger.error(f"  {platform} atomization failed: {e}")
            return None

    async def atomize(
        self,
        pillar_content: str,
        pillar_title: str,
        platforms: list[str] = None,
    ) -> list[AtomizedPiece]:
        """
        Atomize pillar content into pieces for all target platforms.

        Args:
            pillar_content: The full long-form article (from Ewan + Eli)
            pillar_title: Title of the pillar piece
            platforms: Specific platforms to target (default: all)
        """
        if platforms is None:
            platforms = list(PLATFORM_SPECS.keys())

        logger.info(f"Atomizing '{pillar_title}' for {len(platforms)} platforms")
        logger.info(f"  Pillar: {len(pillar_content.split())} words")

        # Run all platform adaptations concurrently
        tasks = [
            self.atomize_for_platform(p, pillar_content, pillar_title)
            for p in platforms
        ]
        results = await asyncio.gather(*tasks)

        pieces = [r for r in results if r is not None]
        logger.info(f"Atomized into {len(pieces)} pieces from {len(platforms)} platforms")

        return pieces

    async def atomize_from_file(self, filepath: str, platforms: list[str] = None) -> list[AtomizedPiece]:
        """Atomize from a markdown file (the Substack draft)."""
        path = Path(filepath)
        content = path.read_text()

        # Extract title from first H1 or first line
        lines = content.strip().split("\n")
        title = lines[0].lstrip("# ").strip() if lines else "Untitled"
        body = "\n".join(lines[1:]).strip() if len(lines) > 1 else content

        return await self.atomize(body, title, platforms)


if __name__ == "__main__":
    logging.basicConfig(level=logging.INFO)
    print("Content Atomizer ready.")
    print(f"Platforms configured: {list(PLATFORM_SPECS.keys())}")
    print(f"That's {len(PLATFORM_SPECS)} pieces from 1 pillar article.")

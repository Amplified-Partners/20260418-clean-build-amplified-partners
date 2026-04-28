"""
Marketing Engine — Content Agent
Generates marketing content from research briefs.

Runs daily at 7am on The Beast, after research agent.
Uses LiteLLM for LLM routing, applies rubrics for quality control.
"""

import asyncio
import httpx
import yaml
import json
import logging
from datetime import datetime
from dataclasses import dataclass, field
from pathlib import Path

logger = logging.getLogger("marketing.content")


@dataclass
class ContentPiece:
    """One piece of generated content."""
    client_id: str
    content_type: str       # "social_post", "blog_article", "gmb_update", "email", "review_response"
    platform: str           # "facebook", "instagram", "gmb", "email", etc.
    title: str
    body: str
    hashtags: list[str] = field(default_factory=list)
    media_suggestions: list[str] = field(default_factory=list)
    quality_score: float = 0.0
    status: str = "draft"   # "draft", "approved", "published", "rejected"
    created_at: str = field(default_factory=lambda: datetime.utcnow().isoformat())
    metadata: dict = field(default_factory=dict)


class ContentAgent:
    """
    Generates marketing content using LLMs via LiteLLM.

    Flow:
    1. Receive research brief from research agent
    2. Select content types needed based on schedule
    3. Generate content using appropriate model tier
    4. Apply rubrics (tone, quality, compliance)
    5. Score each piece
    6. Output approved content for publishing agent
    """

    def __init__(self, config_path: str = "/app/config/engine_config.yaml"):
        with open(config_path) as f:
            self.config = yaml.safe_load(f)

        self.litellm_url = self.config["services"]["litellm"]["base_url"]
        self.quality_threshold = self.config["quality"]["minimum_score"]

    async def call_llm(self, model: str, messages: list[dict], temperature: float = 0.7, max_tokens: int = 1000) -> str:
        """Call LLM via LiteLLM proxy."""
        import os
        async with httpx.AsyncClient(timeout=60) as client:
            try:
                resp = await client.post(
                    f"{self.litellm_url}/v1/chat/completions",
                    headers={
                        "Authorization": f"Bearer {os.environ.get('LITELLM_MASTER_KEY', '')}",
                        "Content-Type": "application/json",
                    },
                    json={
                        "model": model,
                        "messages": messages,
                        "temperature": temperature,
                        "max_tokens": max_tokens,
                    },
                )
                resp.raise_for_status()
                data = resp.json()
                return data["choices"][0]["message"]["content"]
            except Exception as e:
                logger.error(f"LLM call failed: {e}")
                return ""

    def build_system_prompt(self, client_config: dict, content_type: str) -> str:
        """Build system prompt with brand voice and constraints."""
        brand = client_config.get("brand", {})
        voice = brand.get("voice", "professional")
        personality = brand.get("personality", "")
        avoid_words = brand.get("avoid_words", [])
        tone_keywords = brand.get("tone_keywords", [])

        return f"""You are a marketing content writer for {client_config['client']['name']}.

BRAND VOICE: {voice}
PERSONALITY: {personality}
TONE KEYWORDS: {', '.join(tone_keywords)}
WORDS TO AVOID: {', '.join(avoid_words)}

CONTENT TYPE: {content_type}
LOCATION: {client_config['business']['location']['area']}, {client_config['business']['location']['city']}
SERVICES: {', '.join(client_config['business'].get('services', [])[:5])}

RULES:
- Write in the brand voice described above
- Be genuinely helpful, not salesy
- Include local references where natural
- Never make claims that can't be substantiated
- Keep it authentic — no corporate buzzwords
- For social posts: concise, engaging, include a call to action
- For blog articles: informative, well-structured, SEO-friendly
- For GMB updates: short, actionable, local-focused
"""

    async def generate_social_post(self, client_config: dict, topic: str, platform: str) -> ContentPiece:
        """Generate a social media post."""
        model_config = self.config["models"]["content_social"]
        system_prompt = self.build_system_prompt(client_config, "social_post")

        platform_guidance = {
            "facebook": "Write a Facebook post (100-200 words). Conversational, can be longer. Include a question to encourage comments.",
            "instagram": "Write an Instagram caption (50-150 words). Visual-focused, use line breaks for readability. Suggest image concept.",
            "twitter": "Write a tweet (under 280 characters). Punchy, shareable. Include 1-2 relevant hashtags.",
            "linkedin": "Write a LinkedIn post (100-300 words). Professional but personable. Share expertise.",
        }

        user_prompt = f"""Write a {platform} post about: {topic}

{platform_guidance.get(platform, 'Write a social media post.')}

Return JSON with: {{"title": "...", "body": "...", "hashtags": [...], "media_suggestion": "..."}}
"""

        response = await self.call_llm(
            model=model_config["model"],
            messages=[
                {"role": "system", "content": system_prompt},
                {"role": "user", "content": user_prompt},
            ],
            temperature=model_config["temperature"],
            max_tokens=model_config["max_tokens"],
        )

        # Parse response (with fallback)
        try:
            data = json.loads(response)
        except json.JSONDecodeError:
            data = {"title": topic, "body": response, "hashtags": [], "media_suggestion": ""}

        return ContentPiece(
            client_id=client_config["client"]["id"],
            content_type="social_post",
            platform=platform,
            title=data.get("title", topic),
            body=data.get("body", response),
            hashtags=data.get("hashtags", []),
            media_suggestions=[data.get("media_suggestion", "")],
            metadata={"topic": topic, "model": model_config["model"]},
        )

    async def generate_blog_article(self, client_config: dict, topic: str) -> ContentPiece:
        """Generate a blog article."""
        model_config = self.config["models"]["content_blog"]
        system_prompt = self.build_system_prompt(client_config, "blog_article")

        user_prompt = f"""Write a blog article about: {topic}

Requirements:
- 500-800 words
- Include an engaging title
- Use subheadings for structure
- Include practical tips the reader can use
- End with a soft call to action (not salesy)
- SEO-friendly: include the main keyword naturally 3-5 times

Return the article in markdown format.
"""

        response = await self.call_llm(
            model=model_config["model"],
            messages=[
                {"role": "system", "content": system_prompt},
                {"role": "user", "content": user_prompt},
            ],
            temperature=model_config["temperature"],
            max_tokens=model_config["max_tokens"],
        )

        # Extract title from first line if markdown
        lines = response.strip().split("\n")
        title = lines[0].lstrip("#").strip() if lines else topic

        return ContentPiece(
            client_id=client_config["client"]["id"],
            content_type="blog_article",
            platform="website",
            title=title,
            body=response,
            metadata={"topic": topic, "model": model_config["model"], "word_count": len(response.split())},
        )

    async def generate_gmb_update(self, client_config: dict, topic: str) -> ContentPiece:
        """Generate a Google My Business update."""
        model_config = self.config["models"]["content_gmb"]
        system_prompt = self.build_system_prompt(client_config, "gmb_update")

        user_prompt = f"""Write a Google My Business update about: {topic}

Requirements:
- 50-100 words maximum
- Actionable and local-focused
- Include a call to action (call us, visit us, book now)
- Mention the service area if relevant

Return just the update text, no formatting.
"""

        response = await self.call_llm(
            model=model_config["model"],
            messages=[
                {"role": "system", "content": system_prompt},
                {"role": "user", "content": user_prompt},
            ],
            temperature=model_config["temperature"],
            max_tokens=model_config["max_tokens"],
        )

        return ContentPiece(
            client_id=client_config["client"]["id"],
            content_type="gmb_update",
            platform="gmb",
            title=topic,
            body=response.strip(),
            metadata={"topic": topic, "model": model_config["model"]},
        )

    async def score_content(self, piece: ContentPiece, client_config: dict) -> float:
        """Score content quality using LLM as judge."""
        model_config = self.config["models"]["quality_check"]

        scoring_prompt = f"""Score this marketing content on a scale of 1-10.

BRAND VOICE: {client_config['brand']['voice']}
TONE KEYWORDS: {', '.join(client_config['brand'].get('tone_keywords', []))}
WORDS TO AVOID: {', '.join(client_config['brand'].get('avoid_words', []))}

CONTENT TYPE: {piece.content_type}
PLATFORM: {piece.platform}

CONTENT:
{piece.body}

Score on these criteria (1-10 each):
1. Brand voice match
2. Engagement potential
3. Accuracy/safety (no false claims)
4. Call to action effectiveness
5. Platform appropriateness

Return JSON: {{"scores": {{"voice": N, "engagement": N, "accuracy": N, "cta": N, "platform": N}}, "overall": N, "feedback": "..."}}
"""

        response = await self.call_llm(
            model=model_config["model"],
            messages=[{"role": "user", "content": scoring_prompt}],
            temperature=model_config["temperature"],
            max_tokens=model_config["max_tokens"],
        )

        try:
            data = json.loads(response)
            return float(data.get("overall", 5.0))
        except (json.JSONDecodeError, ValueError):
            return 5.0  # Default middle score if parsing fails

    async def run(self, client_id: str, research_brief: dict = None) -> list[ContentPiece]:
        """Generate content for a client based on research brief."""
        client_path = Path(f"/app/config/clients/{client_id}.yaml")
        with open(client_path) as f:
            client_config = yaml.safe_load(f)

        logger.info(f"Generating content for {client_id}")

        # Determine what to generate based on config
        content_pieces = []
        platforms = client_config.get("content", {}).get("platforms", {})
        topics = client_config.get("content", {}).get("topics", {}).get("evergreen", [])

        if not topics:
            logger.warning(f"No topics configured for {client_id}")
            return []

        # Pick a topic (in production, this would be smarter — using research brief)
        topic = topics[datetime.now().timetuple().tm_yday % len(topics)]

        # Generate for each enabled platform
        tasks = []
        for platform, settings in platforms.items():
            if settings.get("enabled", False):
                if platform in ("facebook", "instagram", "twitter", "linkedin"):
                    tasks.append(self.generate_social_post(client_config, topic, platform))
                elif platform == "google_my_business":
                    tasks.append(self.generate_gmb_update(client_config, topic))

        # Run generation concurrently
        if tasks:
            content_pieces = await asyncio.gather(*tasks)

        # Score all content
        for piece in content_pieces:
            piece.quality_score = await self.score_content(piece, client_config)
            piece.status = "approved" if piece.quality_score >= self.quality_threshold else "draft"
            logger.info(f"  {piece.platform}: score={piece.quality_score:.1f} status={piece.status}")

        logger.info(f"Content generation complete: {len(content_pieces)} pieces, "
                     f"{sum(1 for p in content_pieces if p.status == 'approved')} approved")

        return list(content_pieces)


if __name__ == "__main__":
    logging.basicConfig(level=logging.INFO)
    agent = ContentAgent()
    pieces = asyncio.run(agent.run("jesmond-plumbing"))
    for p in pieces:
        print(f"\n{'='*50}")
        print(f"Platform: {p.platform} | Score: {p.quality_score:.1f} | Status: {p.status}")
        print(f"Title: {p.title}")
        print(f"Body: {p.body[:200]}...")

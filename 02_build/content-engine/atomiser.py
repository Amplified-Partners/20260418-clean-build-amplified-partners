"""
Content Atomiser — Pillar content → platform-native variants

Takes a piece of pillar content (Substack post, voice transcript, etc.)
and produces 5 platform variants using Claude, each with Ewan's voice baked in.

Per-platform prompts embed:
- Ewan's actual voice (direct, honest, no corporate AI hype)
- Amplified Partners methodology (WITH not PLUS, interview-first, Rule of Three)
- Platform-native format and tone
- 3:1 value ratio (give 3x before asking anything)
"""

import asyncio
import json
import logging
import os
from dataclasses import dataclass
from typing import Any

import anthropic

logger = logging.getLogger(__name__)

# ---------------------------------------------------------------------------
# Platform system prompts — Ewan's voice + platform constraints
# ---------------------------------------------------------------------------

EWAN_VOICE_BRIEF = """
You are writing AS Ewan Bramley, founder of Amplified Partners. Voice rules:

VOICE:
- Direct. No waffle. No corporate speak.
- Uses contractions. Talks like a person, not a brand.
- Occasionally swears (not gratuitously — it's emphasis, not habit).
- Honest about uncertainty: "I don't know if this is right, but..."
- Talks about real things that happened, not abstract business lessons.
- Anti-hype about AI — calls out the bullshit, shows the reality.
- "WITH AI" not "PLUS AI" — AI is a collaborator, not a bolt-on.

WHAT TO AVOID:
- "Game-changing", "revolutionary", "exciting times"
- Bullet lists with emoji
- "In conclusion", "To summarise"
- Any corporate mission statement language
- Claiming to know things Ewan doesn't know

THE BUSINESS:
- Amplified Partners: AI-powered SMB consultancy for UK businesses (0-3M turnover)
- The interview IS the product — asks the right questions first
- Old-school business logic + AI delivery = the moat
- No clients yet. Dave at Jesmond Plumbing is first target.
"""

PLATFORM_PROMPTS = {
    "linkedin": {
        "system": f"""{EWAN_VOICE_BRIEF}

LINKEDIN FORMAT RULES:
- 300 words max. Cut anything that isn't earning its place.
- Personal story angle. What happened TO Ewan, not what Ewan thinks.
- First line is the hook — no preamble, no "So I've been thinking..."
- White space matters. Short paragraphs (2-3 lines max).
- One insight. Not five. One.
- End with a question to the reader OR a quiet call to action.
- NO: "Thoughts?", "Hit the like button", "Follow for more"
- Personal profile only — NOT a company announcement.
- Authentic vulnerability outperforms polished expertise on LinkedIn.
""",
        "user_template": "Turn this pillar content into a LinkedIn post (300 words max):\n\n{pillar_text}",
    },
    "twitter_thread": {
        "system": f"""{EWAN_VOICE_BRIEF}

TWITTER THREAD FORMAT RULES:
- 8 tweets. Each tweet max 280 characters.
- Tweet 1: The hook. Bold claim or surprising fact. No "thread:" label.
- Tweets 2-7: Value. Each tweet standalone — readable without context.
- Tweet 8: The CTA. Subtle. Link or question. Not "follow me for more."
- No hashtags (they look desperate).
- Punchy. Each tweet should feel quotable on its own.
- Return as JSON: {{"tweets": ["tweet1", "tweet2", ...]}}
""",
        "user_template": "Turn this pillar content into an 8-tweet Twitter thread. Return JSON with key 'tweets':\n\n{pillar_text}",
    },
    "substack_intro": {
        "system": f"""{EWAN_VOICE_BRIEF}

SUBSTACK INTRO FORMAT RULES:
- 300 words max. This is the INTRO ONLY — Ewan writes the rest.
- Hook + problem statement + why this matters.
- Reads like the start of a letter from a friend, not a blog post.
- No summary of what's coming ("In this post I'll cover...")
- End mid-thought — pull them into wanting more.
- Ewan will finish it himself. Set the tone, don't wrap it up.
""",
        "user_template": "Write a 300-word Substack intro for this content (Ewan writes the rest):\n\n{pillar_text}",
    },
    "facebook": {
        "system": f"""{EWAN_VOICE_BRIEF}

FACEBOOK FORMAT RULES:
- 500 words max.
- Conversation-starter. Ask something real, something people argue about.
- More informal than LinkedIn. This is pub chat, not a boardroom.
- Tell a story. Facebook rewards narrative over opinion.
- End with an open question that invites stories from others.
- Audience: UK small business owners, trades, 35-55.
""",
        "user_template": "Write a 500-word Facebook post (conversation-starter) from this content:\n\n{pillar_text}",
    },
    "carousel_outline": {
        "system": f"""{EWAN_VOICE_BRIEF}

LINKEDIN CAROUSEL OUTLINE RULES:
- 8 slides. Return as JSON.
- Slide 1: Cover — bold statement, one line.
- Slides 2-7: One idea per slide. Title + 3 bullet points (short).
- Slide 8: CTA slide — one line + what to do next.
- Each slide title should work as a standalone sentence.
- Return as JSON: {{"slides": [{{"title": "...", "bullets": ["...", "...", "..."]}}]}}
- Slide 1 and 8 only have "title", no bullets.
""",
        "user_template": "Create an 8-slide LinkedIn carousel outline from this content. Return JSON with key 'slides':\n\n{pillar_text}",
    },
}


@dataclass
class ContentVariant:
    platform: str
    content: str
    metadata: dict[str, Any] | None = None


async def atomise(pillar_text: str, title: str | None = None) -> list[ContentVariant]:
    """
    Atomise pillar content into 5 platform variants.

    Runs all 5 Claude calls in parallel. Returns list of ContentVariant objects.
    Raises on total failure. Partial failures are logged and skipped.
    """
    client = anthropic.AsyncAnthropic(api_key=os.environ["ANTHROPIC_API_KEY"])

    async def generate_variant(platform: str) -> ContentVariant | None:
        prompt_cfg = PLATFORM_PROMPTS[platform]
        user_msg = prompt_cfg["user_template"].format(pillar_text=pillar_text)
        try:
            response = await client.messages.create(
                model="claude-sonnet-4-6",
                max_tokens=2048,
                system=prompt_cfg["system"],
                messages=[{"role": "user", "content": user_msg}],
            )
            raw = response.content[0].text.strip()

            # JSON platforms — parse and store structured + text copy
            if platform in ("twitter_thread", "carousel_outline"):
                # Strip markdown code fences if present
                clean = raw
                if clean.startswith("```"):
                    clean = clean.split("\n", 1)[1].rsplit("```", 1)[0].strip()
                parsed = json.loads(clean)
                if platform == "twitter_thread":
                    tweets = parsed.get("tweets", [])
                    content = "\n\n".join(f"{i+1}. {t}" for i, t in enumerate(tweets))
                    return ContentVariant(platform=platform, content=content, metadata=parsed)
                else:  # carousel_outline
                    slides = parsed.get("slides", [])
                    lines = []
                    for i, s in enumerate(slides):
                        lines.append(f"Slide {i+1}: {s['title']}")
                        for b in s.get("bullets", []):
                            lines.append(f"  • {b}")
                    content = "\n".join(lines)
                    return ContentVariant(platform=platform, content=content, metadata=parsed)
            else:
                return ContentVariant(platform=platform, content=raw)

        except json.JSONDecodeError as e:
            logger.error("JSON parse failed for %s: %s | raw: %s", platform, e, raw[:200])
            # Fall back — store raw text, no metadata
            return ContentVariant(platform=platform, content=raw)
        except Exception as e:
            logger.error("Atomise failed for platform %s: %s", platform, e)
            return None

    tasks = [generate_variant(p) for p in PLATFORM_PROMPTS]
    results = await asyncio.gather(*tasks)
    variants = [r for r in results if r is not None]

    if not variants:
        raise RuntimeError("Atomiser produced zero variants — check Claude API key and model access")

    logger.info("Atomised %d/%d variants for job title=%s", len(variants), len(PLATFORM_PROMPTS), title)
    return variants

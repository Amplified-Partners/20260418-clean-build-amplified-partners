"""
X/Twitter Publisher — Thread posting via Late.dev API

Official X API costs $100+/month. Late.dev is OAuth-based, fraction of cost,
same capabilities. If Late.dev changes, Postiz has native X integration as fallback.

Setup needed:
  LATE_DEV_API_KEY=...

To get a Late.dev API key:
  1. Sign up at late.dev
  2. Connect your X/Twitter account
  3. Generate an API key in settings

Thread format: variant.metadata["tweets"] is a list of strings.
If no metadata (plain text), split on double-newline as fallback.
"""

import logging
import os
from dataclasses import dataclass

import httpx

logger = logging.getLogger(__name__)

LATE_DEV_API_BASE = "https://api.late.dev/v1"


@dataclass
class TwitterPostResult:
    success: bool
    thread_id: str | None = None
    first_tweet_url: str | None = None
    error: str | None = None


async def post_thread(tweets: list[str]) -> TwitterPostResult:
    """
    Post a thread of tweets via Late.dev API.

    Args:
        tweets: List of tweet strings (max 280 chars each)

    Returns:
        TwitterPostResult with success flag and first tweet URL.
    """
    api_key = os.environ.get("LATE_DEV_API_KEY")
    if not api_key:
        logger.warning("LATE_DEV_API_KEY not set")
        return TwitterPostResult(
            success=False,
            error="LATE_DEV_API_KEY not configured. Add to ~/.amplified/keys.env",
        )

    if not tweets:
        return TwitterPostResult(success=False, error="No tweets provided")

    # Truncate each tweet to 280 chars (hard limit)
    safe_tweets = [t[:280] for t in tweets]

    payload = {
        "posts": [{"text": tweet} for tweet in safe_tweets],
        "type": "thread",
    }

    headers = {
        "Authorization": f"Bearer {api_key}",
        "Content-Type": "application/json",
    }

    try:
        async with httpx.AsyncClient(timeout=30.0) as client:
            response = await client.post(
                f"{LATE_DEV_API_BASE}/posts",
                json=payload,
                headers=headers,
            )
            response.raise_for_status()

        data = response.json()
        thread_id = str(data.get("id", ""))
        first_tweet_url = data.get("url")

        logger.info("Twitter thread posted: %s (%d tweets)", thread_id, len(tweets))
        return TwitterPostResult(success=True, thread_id=thread_id, first_tweet_url=first_tweet_url)

    except httpx.HTTPStatusError as e:
        error_body = e.response.text[:500]
        logger.error("Late.dev API error %d: %s", e.response.status_code, error_body)
        return TwitterPostResult(
            success=False,
            error=f"Late.dev API {e.response.status_code}: {error_body}",
        )
    except Exception as e:
        logger.error("Twitter thread post failed: %s", e)
        return TwitterPostResult(success=False, error=str(e))


async def post_variant(content: str, metadata: dict | None = None) -> TwitterPostResult:
    """
    Convenience wrapper — extract tweets from metadata or split content.
    Called by scheduler with a ContentVariantORM.
    """
    if metadata and "tweets" in metadata:
        tweets = metadata["tweets"]
    else:
        # Fallback: split plain text on double newline, filter empties
        tweets = [t.strip() for t in content.split("\n\n") if t.strip()]
        # Strip leading "1. " numbering if present (from atomiser text format)
        clean = []
        for t in tweets:
            if len(t) > 3 and t[0].isdigit() and t[1] in ".)" and t[2] == " ":
                t = t[3:].strip()
            clean.append(t)
        tweets = clean

    return await post_thread(tweets)

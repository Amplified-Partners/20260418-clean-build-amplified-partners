"""
LinkedIn Publisher — Personal Profile Only

Posts to Ewan's personal LinkedIn profile via official LinkedIn API (OAuth 2.0).
Personal profile only — NOT company page (60% organic reach drop on company pages).

Setup needed (OAuth dance — do this once):
  LINKEDIN_CLIENT_ID=...
  LINKEDIN_CLIENT_SECRET=...
  LINKEDIN_ACCESS_TOKEN=...   (long-lived token after OAuth)
  LINKEDIN_PERSON_URN=...     (your person URN: urn:li:person:XXXXXXX)

To get LINKEDIN_PERSON_URN:
  curl -H "Authorization: Bearer YOUR_TOKEN" https://api.linkedin.com/v2/userinfo
  Look for 'sub' field — that's your URN suffix.

OAuth flow: POST /content/auth/linkedin → redirects to LinkedIn → callback stores token.
(Not implemented here — set up manually via LinkedIn developer portal first.)

Rate limits: 100 posts/day for personal profile. We'll never hit that.
"""

import logging
import os
from dataclasses import dataclass

import httpx

logger = logging.getLogger(__name__)

LINKEDIN_API_BASE = "https://api.linkedin.com/v2"


@dataclass
class LinkedInPostResult:
    success: bool
    post_id: str | None = None
    post_url: str | None = None
    error: str | None = None


async def post_to_linkedin(content: str) -> LinkedInPostResult:
    """
    Post text content to Ewan's personal LinkedIn profile.

    Args:
        content: The post text (max ~3000 chars, hard limit ~3600)

    Returns:
        LinkedInPostResult with success flag and post URL.
    """
    access_token = os.environ.get("LINKEDIN_ACCESS_TOKEN")
    person_urn = os.environ.get("LINKEDIN_PERSON_URN")

    if not access_token:
        logger.warning("LINKEDIN_ACCESS_TOKEN not set")
        return LinkedInPostResult(
            success=False,
            error="LINKEDIN_ACCESS_TOKEN not configured. Add to ~/.amplified/keys.env",
        )
    if not person_urn:
        logger.warning("LINKEDIN_PERSON_URN not set")
        return LinkedInPostResult(
            success=False,
            error="LINKEDIN_PERSON_URN not configured. Add to ~/.amplified/keys.env",
        )

    # LinkedIn UGC Post payload
    payload = {
        "author": f"urn:li:person:{person_urn}",
        "lifecycleState": "PUBLISHED",
        "specificContent": {
            "com.linkedin.ugc.ShareContent": {
                "shareCommentary": {"text": content},
                "shareMediaCategory": "NONE",
            }
        },
        "visibility": {"com.linkedin.ugc.MemberNetworkVisibility": "PUBLIC"},
    }

    headers = {
        "Authorization": f"Bearer {access_token}",
        "Content-Type": "application/json",
        "X-Restli-Protocol-Version": "2.0.0",
    }

    try:
        async with httpx.AsyncClient(timeout=30.0) as client:
            response = await client.post(
                f"{LINKEDIN_API_BASE}/ugcPosts",
                json=payload,
                headers=headers,
            )
            response.raise_for_status()

        post_id = response.headers.get("x-restli-id", "")
        # LinkedIn doesn't return a post URL directly — construct from person URN
        post_url = f"https://www.linkedin.com/feed/update/{post_id}/" if post_id else None

        logger.info("LinkedIn post published: %s", post_id)
        return LinkedInPostResult(success=True, post_id=post_id, post_url=post_url)

    except httpx.HTTPStatusError as e:
        error_body = e.response.text[:500]
        logger.error("LinkedIn API error %d: %s", e.response.status_code, error_body)
        return LinkedInPostResult(
            success=False,
            error=f"LinkedIn API {e.response.status_code}: {error_body}",
        )
    except Exception as e:
        logger.error("LinkedIn publish failed: %s", e)
        return LinkedInPostResult(success=False, error=str(e))

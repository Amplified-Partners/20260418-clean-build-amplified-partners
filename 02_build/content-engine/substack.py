"""
Substack Publisher — Draft Creation Only

Creates DRAFT posts on Substack. Ewan presses publish himself. Always.

Uses the substack-api library (JPres-Projects). Cookie-based auth — unofficial
but stable for draft creation. Worst case if it breaks: manual copy-paste.
Nothing catastrophic because we never auto-publish.

Setup needed (add to ~/.amplified/keys.env):
  SUBSTACK_COOKIE=...         (session cookie from browser — see below)
  SUBSTACK_PUBLICATION_URL=...  (e.g. amplifiedpartners.substack.com)

To get the cookie:
1. Log into Substack in Chrome
2. F12 → Application → Cookies → substack.com
3. Copy the value of 'substack.sid' cookie
4. Paste as SUBSTACK_COOKIE in keys.env

IMPORTANT: Substack accounts need to be created manually first (SHARED-BOARD item).
Three streams: Ewan's, Eli's (pudding-press), Covered AI / Local Business Help.
"""

import logging
import os
from dataclasses import dataclass

logger = logging.getLogger(__name__)


@dataclass
class SubstackDraftResult:
    success: bool
    draft_id: str | None = None
    draft_url: str | None = None
    error: str | None = None


async def create_draft(
    title: str,
    body: str,
    subtitle: str | None = None,
    publication_url: str | None = None,
) -> SubstackDraftResult:
    """
    Create a Substack draft. Returns draft ID and URL.

    Args:
        title: Post title
        body: Post body (markdown)
        subtitle: Optional subtitle
        publication_url: Override default publication URL from env

    Returns:
        SubstackDraftResult with success flag and draft URL.
    """
    cookie = os.environ.get("SUBSTACK_COOKIE")
    pub_url = publication_url or os.environ.get("SUBSTACK_PUBLICATION_URL")

    if not cookie:
        logger.warning("SUBSTACK_COOKIE not set — skipping draft creation")
        return SubstackDraftResult(
            success=False,
            error="SUBSTACK_COOKIE not configured. Add to ~/.amplified/keys.env",
        )

    if not pub_url:
        logger.warning("SUBSTACK_PUBLICATION_URL not set — skipping draft creation")
        return SubstackDraftResult(
            success=False,
            error="SUBSTACK_PUBLICATION_URL not configured. Add to ~/.amplified/keys.env",
        )

    try:
        # substack-api library (pip install substack-api)
        # Import here so missing library doesn't break module load
        from substack_api import SubstackClient  # type: ignore

        client = SubstackClient(pub_url=pub_url, cookie=cookie)
        draft = client.create_draft(
            title=title,
            body=body,
            subtitle=subtitle or "",
        )

        draft_id = str(draft.get("id", ""))
        draft_url = f"https://{pub_url.rstrip('/')}/p/{draft.get('slug', draft_id)}"

        logger.info("Substack draft created: %s (%s)", title, draft_url)
        return SubstackDraftResult(success=True, draft_id=draft_id, draft_url=draft_url)

    except ImportError:
        logger.error("substack-api not installed. Run: pip install substack-api")
        return SubstackDraftResult(
            success=False,
            error="substack-api library not installed. Run: pip install substack-api",
        )
    except Exception as e:
        logger.error("Substack draft creation failed: %s", e)
        return SubstackDraftResult(success=False, error=str(e))

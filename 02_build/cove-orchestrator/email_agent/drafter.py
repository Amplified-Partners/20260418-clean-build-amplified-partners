"""Email draft generator — creates contextual response drafts."""

from __future__ import annotations

import json
import logging
import re
from dataclasses import dataclass
from typing import Any

import httpx

from .config import DRAFT_MODEL, LITELLM_URL
from .fetcher import FetchedEmail

logger = logging.getLogger("email_agent.drafter")


@dataclass
class DraftResponse:
    """Generated draft email response."""

    to_addresses: list[str]
    cc_addresses: list[str]
    subject: str
    body_text: str
    tone: str
    model: str


DRAFT_PROMPT = """\
You are the Email Drafting Agent for Amplified Partners. You write responses \
on behalf of Ewan Bramley, founder.

VOICE GUIDELINES:
- Professional but warm — Ewan is direct, honest, and genuinely helpful
- No corporate waffle. Say what you mean.
- Radically transparent — if we can't do something, say so
- Always focused on helping the recipient
- Sign off as "Ewan" (never "Ewan Bramley" unless it's a first-ever contact)
- British English spelling (colour, organisation, etc.)

TONE CALIBRATION:
- Client emails: warm, attentive, solution-oriented
- Partner/vendor emails: professional, direct
- Team/internal: casual, efficient
- Cold outreach responses: brief, friendly
- Complaints/issues: empathetic, action-oriented

STRUCTURAL RULES:
- Open with context acknowledgement (never "I hope this email finds you well")
- Body: address every point raised, in order
- Close with clear next step or call to action
- Keep it concise — respect the reader's time
- No bullet points in email body unless listing items

Respond with valid JSON:
{
  "subject": "Re: <original subject or updated>",
  "body": "The full email body text",
  "tone": "one of: warm, professional, casual, empathetic, direct"
}
"""


async def generate_draft(
    client: httpx.AsyncClient,
    email_item: FetchedEmail,
    triage_reasoning: str,
    contact_context: str | None = None,
) -> DraftResponse:
    """
    Generate a draft response for an email.

    Uses the medium-tier model (Sonnet) for quality drafts.
    """
    # Build the context
    body_text = (email_item.body_text or "")[:4000]

    user_prompt_parts = [
        "Generate a response to this email.",
        "",
        f"Triage assessment: {triage_reasoning}",
        "",
        f"From: {email_item.from_name} <{email_item.from_address}>",
        f"Subject: {email_item.subject}",
        f"Date: {email_item.received_at.isoformat()}",
    ]
    if email_item.has_attachments:
        user_prompt_parts.append(f"Attachments: {', '.join(email_item.attachment_names)}")
    if contact_context:
        user_prompt_parts.extend(["", f"Sender context: {contact_context}"])
    user_prompt_parts.extend(["", "Original email:", body_text])

    user_prompt = "\n".join(user_prompt_parts)

    try:
        resp = await client.post(
            f"{LITELLM_URL}/v1/chat/completions",
            json={
                "model": DRAFT_MODEL,
                "messages": [
                    {"role": "system", "content": DRAFT_PROMPT},
                    {"role": "user", "content": user_prompt},
                ],
                "temperature": 0.4,
                "max_tokens": 1500,
                "metadata": {
                    "task_id": f"email-draft-{email_item.message_id[:20]}",
                    "agent_role": "email_agent",
                    "trace_name": "email-draft",
                },
            },
            timeout=60.0,
        )
        resp.raise_for_status()
        data = resp.json()
        content = data["choices"][0]["message"]["content"].strip()

        # Parse JSON
        if content.startswith("```"):
            content = re.sub(r"^```(?:json)?\s*", "", content)
            content = re.sub(r"\s*```$", "", content)

        parsed = json.loads(content)

        # Determine reply-to address
        reply_to = email_item.raw_headers.get("Reply-To")
        to_addr = reply_to if reply_to else email_item.from_address

        return DraftResponse(
            to_addresses=[to_addr],
            cc_addresses=[],  # Don't CC unless explicitly needed
            subject=parsed.get("subject", f"Re: {email_item.subject}"),
            body_text=parsed["body"],
            tone=parsed.get("tone", "professional"),
            model=DRAFT_MODEL,
        )

    except Exception as exc:
        logger.error("Draft generation failed for '%s': %s", email_item.subject[:50], exc)
        # Return a placeholder draft that flags the issue
        return DraftResponse(
            to_addresses=[email_item.from_address],
            cc_addresses=[],
            subject=f"Re: {email_item.subject}",
            body_text=f"[DRAFT GENERATION FAILED — manual response needed]\n\nError: {exc}",
            tone="error",
            model="none",
        )

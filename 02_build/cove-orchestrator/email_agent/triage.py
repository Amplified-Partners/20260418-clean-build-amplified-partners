"""Email triage — classify priority and action using LLM."""

from __future__ import annotations

import json
import logging
import re
from typing import Any

import httpx

from .config import (
    AUTO_ARCHIVE_DOMAINS,
    CONFIDENCE_THRESHOLD,
    EmailAction,
    EmailPriority,
    LITELLM_URL,
    TRIAGE_MODEL,
    TriageResult,
)
from .fetcher import FetchedEmail

logger = logging.getLogger("email_agent.triage")

TRIAGE_PROMPT = """\
You are the Email Triage Agent for Amplified Partners, an AI consultancy \
helping SMBs leverage AI to reduce operational friction. The founder is \
Ewan Bramley.

Classify this email on two dimensions:

1. **Priority** (one of: critical, urgent, normal, low)
   - critical: Revenue at risk, legal matter, key client escalation, system down
   - urgent: Client request needing same-day response, time-sensitive opportunity
   - normal: Standard business correspondence, follow-ups, proposals
   - low: Newsletters, notifications, FYI, marketing, automated messages

2. **Action** (one of: respond, delegate, archive, defer, escalate)
   - respond: Draft a response (most business emails)
   - delegate: Forward to appropriate team/agent (specify who)
   - archive: No response needed (newsletters, confirmations, notifications)
   - defer: Not urgent, revisit later (save for weekly review)
   - escalate: Needs Ewan's direct attention (contracts, key relationships, strategy)

3. **Confidence** (0.0 to 1.0): How confident are you in this classification?

Consider:
- Known Amplified Partners clients get priority boost
- Emails from domains like noreply@, notifications@ are almost always archive
- Thread context: is this a reply chain that's been going on?
- Attachment presence may indicate something actionable
- "Precedence: bulk" or "List-Unsubscribe" headers suggest newsletters

Respond ONLY with valid JSON:
{
  "priority": "...",
  "action": "...",
  "confidence": 0.X,
  "reasoning": "One sentence explaining the classification"
}
"""


def _check_auto_archive(email_item: FetchedEmail) -> TriageResult | None:
    """Check if email matches auto-archive rules (skip LLM)."""
    from_lower = email_item.from_address.lower()

    # Auto-archive known notification senders
    for pattern in AUTO_ARCHIVE_DOMAINS:
        if from_lower.startswith(pattern) or pattern in from_lower:
            return TriageResult(
                priority=EmailPriority.LOW,
                action=EmailAction.ARCHIVE,
                confidence=0.95,
                reasoning=f"Auto-archive: sender matches pattern '{pattern}'",
            )

    # Auto-archive if List-Unsubscribe header present and no reply chain
    if email_item.raw_headers.get("List-Unsubscribe") and not email_item.subject.lower().startswith("re:"):
        return TriageResult(
            priority=EmailPriority.LOW,
            action=EmailAction.ARCHIVE,
            confidence=0.90,
            reasoning="Auto-archive: newsletter (List-Unsubscribe header present)",
        )

    # Auto-archive if Precedence: bulk
    if email_item.raw_headers.get("Precedence", "").lower() == "bulk":
        return TriageResult(
            priority=EmailPriority.LOW,
            action=EmailAction.ARCHIVE,
            confidence=0.90,
            reasoning="Auto-archive: bulk precedence header",
        )

    return None


def _build_triage_input(email_item: FetchedEmail) -> str:
    """Build the user prompt with email details for triage."""
    # Truncate body for triage (first 2000 chars is enough for classification)
    body_preview = (email_item.body_text or "")[:2000]

    parts = [
        f"From: {email_item.from_name} <{email_item.from_address}>",
        f"To: {', '.join(email_item.to_addresses)}",
    ]
    if email_item.cc_addresses:
        parts.append(f"Cc: {', '.join(email_item.cc_addresses)}")
    parts.extend([
        f"Subject: {email_item.subject}",
        f"Date: {email_item.received_at.isoformat()}",
        f"Thread: {'Reply chain' if email_item.subject.lower().startswith('re:') else 'New conversation'}",
        f"Attachments: {', '.join(email_item.attachment_names) if email_item.has_attachments else 'None'}",
        f"Headers: Precedence={email_item.raw_headers.get('Precedence', 'none')}, "
        f"List-Unsubscribe={'present' if email_item.raw_headers.get('List-Unsubscribe') else 'absent'}",
        "",
        "Body:",
        body_preview,
    ])
    return "\n".join(parts)


async def triage_email(
    client: httpx.AsyncClient,
    email_item: FetchedEmail,
    contact_context: str | None = None,
) -> TriageResult:
    """
    Classify a single email. Tries rule-based first, then LLM.

    Args:
        client: httpx async client
        email_item: parsed email
        contact_context: optional context about the sender from Graphiti
    """
    # 1. Rule-based auto-archive check
    auto = _check_auto_archive(email_item)
    if auto:
        logger.info("Auto-archived: %s from %s", email_item.subject[:50], email_item.from_address)
        return auto

    # 2. LLM triage
    user_prompt = _build_triage_input(email_item)
    if contact_context:
        user_prompt += f"\n\nSender Context (from knowledge graph):\n{contact_context}"

    try:
        resp = await client.post(
            f"{LITELLM_URL}/v1/chat/completions",
            json={
                "model": TRIAGE_MODEL,
                "messages": [
                    {"role": "system", "content": TRIAGE_PROMPT},
                    {"role": "user", "content": user_prompt},
                ],
                "temperature": 0.1,
                "max_tokens": 300,
                "metadata": {
                    "task_id": f"email-triage-{email_item.message_id[:20]}",
                    "agent_role": "email_agent",
                    "trace_name": "email-triage",
                },
            },
            timeout=30.0,
        )
        resp.raise_for_status()
        data = resp.json()
        content = data["choices"][0]["message"]["content"].strip()

        # Parse JSON (handle markdown code blocks)
        if content.startswith("```"):
            content = re.sub(r"^```(?:json)?\s*", "", content)
            content = re.sub(r"\s*```$", "", content)

        parsed = json.loads(content)

        result = TriageResult(
            priority=EmailPriority(parsed["priority"]),
            action=EmailAction(parsed["action"]),
            confidence=float(parsed["confidence"]),
            reasoning=parsed.get("reasoning", "No reasoning provided"),
        )

        # If confidence below threshold, escalate
        if result.confidence < CONFIDENCE_THRESHOLD:
            logger.warning(
                "Low confidence (%.2f) for '%s' — escalating",
                result.confidence,
                email_item.subject[:50],
            )
            return TriageResult(
                priority=result.priority,
                action=EmailAction.ESCALATE,
                confidence=result.confidence,
                reasoning=f"Low confidence ({result.confidence:.2f}): {result.reasoning}",
            )

        return result

    except Exception as exc:
        logger.error("Triage failed for '%s': %s", email_item.subject[:50], exc)
        # Fail safe: escalate
        return TriageResult(
            priority=EmailPriority.NORMAL,
            action=EmailAction.ESCALATE,
            confidence=0.0,
            reasoning=f"Triage error: {exc}",
        )


async def triage_batch(
    client: httpx.AsyncClient,
    emails: list[FetchedEmail],
) -> list[tuple[FetchedEmail, TriageResult]]:
    """Triage a batch of emails concurrently."""
    import asyncio

    tasks = [triage_email(client, e) for e in emails]
    results = await asyncio.gather(*tasks, return_exceptions=True)

    triaged: list[tuple[FetchedEmail, TriageResult]] = []
    for email_item, result in zip(emails, results):
        if isinstance(result, Exception):
            logger.error("Batch triage error: %s", result)
            result = TriageResult(
                priority=EmailPriority.NORMAL,
                action=EmailAction.ESCALATE,
                confidence=0.0,
                reasoning=f"Batch error: {result}",
            )
        triaged.append((email_item, result))

    return triaged

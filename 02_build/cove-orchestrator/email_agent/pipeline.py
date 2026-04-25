"""Email Agent pipeline — fetch → triage → draft → store → notify."""

from __future__ import annotations

import asyncio
import logging
import uuid
from datetime import datetime, timezone
from typing import Any

import asyncpg
import httpx

from .config import (
    CONFIDENCE_THRESHOLD,
    EmailAction,
    EmailPriority,
    EmailAccountConfig,
    GMAIL_ADDRESS,
    GMAIL_APP_PASSWORD,
    GMAIL_DISPLAY_NAME,
    POSTGRES_DSN,
    TELEGRAM_BOT_TOKEN,
    TELEGRAM_CHAT_ID,
)
from .drafter import DraftResponse, generate_draft
from .fetcher import FetchedEmail, fetch_emails
from .triage import TriageResult, triage_batch

logger = logging.getLogger("email_agent.pipeline")


async def _get_account(pool: asyncpg.Pool) -> tuple[uuid.UUID, int | None]:
    """Get or create the primary email account, return (account_id, last_uid)."""
    row = await pool.fetchrow(
        "SELECT id, last_sync_uid FROM email_accounts WHERE email_address = $1",
        GMAIL_ADDRESS,
    )
    if row:
        return row["id"], row["last_sync_uid"]

    # Create account
    account_id = await pool.fetchval(
        """INSERT INTO email_accounts (email_address, display_name, auth_method)
           VALUES ($1, $2, 'app_password')
           RETURNING id""",
        GMAIL_ADDRESS,
        GMAIL_DISPLAY_NAME,
    )
    return account_id, None


async def _store_inbound(
    pool: asyncpg.Pool,
    account_id: uuid.UUID,
    email_item: FetchedEmail,
    triage: TriageResult,
) -> uuid.UUID | None:
    """Store email + triage result. Returns email ID, or None if duplicate."""
    try:
        email_id = await pool.fetchval(
            """INSERT INTO emails_inbound (
                account_id, message_id, imap_uid, from_address, from_name,
                to_addresses, cc_addresses, subject, body_text, body_html,
                received_at, thread_id, has_attachments, attachment_names,
                raw_headers, priority, action, confidence, triage_reasoning,
                triaged_at, triaged_model
            ) VALUES (
                $1, $2, $3, $4, $5,
                $6, $7, $8, $9, $10,
                $11, $12, $13, $14,
                $15, $16, $17, $18, $19,
                now(), $20
            )
            ON CONFLICT (account_id, message_id) DO NOTHING
            RETURNING id""",
            account_id,
            email_item.message_id,
            email_item.imap_uid,
            email_item.from_address,
            email_item.from_name,
            email_item.to_addresses,
            email_item.cc_addresses,
            email_item.subject,
            email_item.body_text,
            email_item.body_html,
            email_item.received_at,
            email_item.thread_id,
            email_item.has_attachments,
            email_item.attachment_names,
            email_item.raw_headers,
            triage.priority.value,
            triage.action.value,
            float(triage.confidence),
            triage.reasoning,
            "rule-based" if triage.confidence >= 0.90 and triage.action == EmailAction.ARCHIVE else "llm",
        )
        return email_id
    except Exception as exc:
        logger.error("Failed to store email '%s': %s", email_item.subject[:50], exc)
        return None


async def _store_draft(
    pool: asyncpg.Pool,
    inbound_id: uuid.UUID,
    account_id: uuid.UUID,
    draft: DraftResponse,
) -> uuid.UUID | None:
    """Store a draft response."""
    try:
        draft_id = await pool.fetchval(
            """INSERT INTO email_drafts (
                inbound_id, account_id, to_addresses, cc_addresses,
                subject, body_text, tone, draft_model
            ) VALUES ($1, $2, $3, $4, $5, $6, $7, $8)
            RETURNING id""",
            inbound_id,
            account_id,
            draft.to_addresses,
            draft.cc_addresses,
            draft.subject,
            draft.body_text,
            draft.tone,
            draft.model,
        )
        return draft_id
    except Exception as exc:
        logger.error("Failed to store draft: %s", exc)
        return None


async def _mark_auto_handled(
    pool: asyncpg.Pool,
    inbound_id: uuid.UUID,
    action_desc: str,
) -> None:
    """Mark an email as auto-handled (archive, etc.)."""
    await pool.execute(
        """UPDATE emails_inbound
           SET handled = true, handled_at = now(), handled_action = $2
           WHERE id = $1""",
        inbound_id,
        action_desc,
    )


async def _update_watermark(
    pool: asyncpg.Pool,
    account_id: uuid.UUID,
    max_uid: int,
) -> None:
    """Update the IMAP UID watermark after successful sync."""
    await pool.execute(
        """UPDATE email_accounts
           SET last_sync_uid = $2, last_sync_at = now()
           WHERE id = $1""",
        account_id,
        max_uid,
    )


async def _notify_critical(
    client: httpx.AsyncClient,
    critical_emails: list[tuple[FetchedEmail, TriageResult]],
) -> None:
    """Send Telegram notification for critical/escalated emails."""
    if not TELEGRAM_BOT_TOKEN or not TELEGRAM_CHAT_ID:
        logger.warning("Telegram not configured — skipping critical notification")
        return

    lines = ["🚨 *Email Agent — Critical Items*\n"]
    for email_item, triage in critical_emails:
        lines.append(
            f"• *{email_item.subject[:60]}*\n"
            f"  From: {email_item.from_name or email_item.from_address}\n"
            f"  Priority: {triage.priority.value} | Action: {triage.action.value}\n"
            f"  {triage.reasoning}\n"
        )

    text = "\n".join(lines)

    try:
        await client.post(
            f"https://api.telegram.org/bot{TELEGRAM_BOT_TOKEN}/sendMessage",
            json={
                "chat_id": TELEGRAM_CHAT_ID,
                "text": text,
                "parse_mode": "Markdown",
            },
            timeout=10.0,
        )
    except Exception as exc:
        logger.error("Telegram notification failed: %s", exc)


async def _create_pipeline_run(
    pool: asyncpg.Pool,
    account_id: uuid.UUID,
) -> uuid.UUID:
    """Create a pipeline run record."""
    return await pool.fetchval(
        "INSERT INTO email_pipeline_runs (account_id) VALUES ($1) RETURNING id",
        account_id,
    )


async def _complete_pipeline_run(
    pool: asyncpg.Pool,
    run_id: uuid.UUID,
    stats: dict[str, Any],
) -> None:
    """Update pipeline run with results."""
    import json as json_mod

    await pool.execute(
        """UPDATE email_pipeline_runs
           SET completed_at = now(),
               emails_fetched = $2,
               emails_triaged = $3,
               drafts_created = $4,
               auto_handled = $5,
               errors = $6::jsonb
           WHERE id = $1""",
        run_id,
        stats["emails_fetched"],
        stats["emails_triaged"],
        stats["drafts_created"],
        stats["auto_handled"],
        json_mod.dumps(stats.get("errors", [])),
    )


async def run_pipeline() -> dict[str, Any]:
    """
    Execute the full email pipeline:
    1. Fetch new emails via IMAP
    2. Triage each email (rules + LLM)
    3. Generate drafts for 'respond' actions
    4. Auto-handle archive actions
    5. Notify on critical/escalated items
    6. Update watermark
    """
    if not GMAIL_ADDRESS or not GMAIL_APP_PASSWORD:
        raise RuntimeError("GMAIL_ADDRESS and GMAIL_APP_PASSWORD must be set")

    stats: dict[str, Any] = {
        "emails_fetched": 0,
        "emails_triaged": 0,
        "drafts_created": 0,
        "auto_handled": 0,
        "critical_count": 0,
        "errors": [],
    }

    pool = await asyncpg.create_pool(POSTGRES_DSN, min_size=2, max_size=5)

    try:
        # Get account
        account_id, last_uid = await _get_account(pool)
        run_id = await _create_pipeline_run(pool, account_id)

        account_config = EmailAccountConfig(
            email_address=GMAIL_ADDRESS,
            display_name=GMAIL_DISPLAY_NAME,
            app_password=GMAIL_APP_PASSWORD,
        )

        # PHASE 1: Fetch emails (sync, uses imaplib which is blocking)
        logger.info("Phase 1: Fetching emails...")
        loop = asyncio.get_event_loop()
        emails = await loop.run_in_executor(
            None, fetch_emails, account_config, last_uid,
        )
        stats["emails_fetched"] = len(emails)

        if not emails:
            logger.info("No new emails — pipeline complete")
            await _complete_pipeline_run(pool, run_id, stats)
            return stats

        # PHASE 2: Triage
        logger.info("Phase 2: Triaging %d emails...", len(emails))
        async with httpx.AsyncClient() as client:
            triaged = await triage_batch(client, emails)
            stats["emails_triaged"] = len(triaged)

            # PHASE 3: Store + process by action
            logger.info("Phase 3: Processing triaged emails...")
            critical_items: list[tuple[FetchedEmail, TriageResult]] = []

            for email_item, triage in triaged:
                inbound_id = await _store_inbound(pool, account_id, email_item, triage)
                if inbound_id is None:
                    continue  # duplicate

                # Handle by action
                if triage.action == EmailAction.ARCHIVE:
                    await _mark_auto_handled(pool, inbound_id, "auto-archived")
                    stats["auto_handled"] += 1

                elif triage.action == EmailAction.RESPOND:
                    # Generate draft
                    draft = await generate_draft(
                        client, email_item, triage.reasoning,
                    )
                    draft_id = await _store_draft(pool, inbound_id, account_id, draft)
                    if draft_id:
                        stats["drafts_created"] += 1

                elif triage.action in (EmailAction.ESCALATE, EmailAction.DELEGATE):
                    if triage.priority in (EmailPriority.CRITICAL, EmailPriority.URGENT):
                        critical_items.append((email_item, triage))

                # Defer items just stay in the DB unhandled

            # PHASE 4: Notify critical
            if critical_items:
                logger.info("Phase 4: Notifying %d critical items...", len(critical_items))
                await _notify_critical(client, critical_items)
                stats["critical_count"] = len(critical_items)

        # Update watermark to highest UID fetched
        max_uid = max(e.imap_uid for e in emails)
        await _update_watermark(pool, account_id, max_uid)

        await _complete_pipeline_run(pool, run_id, stats)

        logger.info(
            "Pipeline complete: %d fetched, %d triaged, %d drafts, %d auto-handled, %d critical",
            stats["emails_fetched"],
            stats["emails_triaged"],
            stats["drafts_created"],
            stats["auto_handled"],
            stats["critical_count"],
        )

        return stats

    finally:
        await pool.close()

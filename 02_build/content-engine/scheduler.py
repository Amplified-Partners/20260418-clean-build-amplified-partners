"""
Content Scheduler — DB-backed queue with platform-optimal UK timing

APScheduler runs as background thread alongside CRM server.
Polls the content_variants table every 5 minutes for approved, queued variants
and fires at the next optimal publishing window for each platform.

Platform timing (UK time — Europe/London):
  LinkedIn:        Tuesday/Wednesday, 08:00–09:00
  X/Twitter:       Wednesday, 10:00–11:00
  Substack draft:  Monday/Thursday, 09:00 (Ewan publishes at 17:00)
  Facebook:        Wednesday, 13:00–14:00
  Carousel:        Same as LinkedIn (it's a LinkedIn format)

The scheduler doesn't publish blindly on schedule. It picks the next available
window AFTER a variant is approved. If a window has passed this week, it waits
for next week's window.

Nothing publishes without Ewan's Telegram approval first. The scheduler only
processes variants with review_status='approved' and publish_status='queued'.
"""

import logging
import os
from datetime import datetime, timedelta
from typing import Optional
from zoneinfo import ZoneInfo

from apscheduler.schedulers.asyncio import AsyncIOScheduler
from apscheduler.triggers.interval import IntervalTrigger
from sqlalchemy import select

from app.content.models_orm import ContentVariantORM, ContentAnalyticsORM
from app.database import async_session_maker

logger = logging.getLogger(__name__)

UK_TZ = ZoneInfo("Europe/London")

# Platform publishing windows: (weekday, hour) — weekday 0=Monday, 6=Sunday
# Multiple windows per platform = more flexibility if Ewan approves late
PLATFORM_WINDOWS: dict[str, list[tuple[int, int]]] = {
    "linkedin": [(1, 8), (2, 8), (1, 12), (4, 8)],     # Tue/Wed 8AM, Thu 8AM
    "twitter_thread": [(2, 10), (3, 10), (1, 10)],      # Wed/Thu 10AM, Mon 10AM
    "substack_intro": [(0, 9), (3, 9)],                  # Mon/Thu 9AM
    "facebook": [(2, 13), (3, 13), (1, 13)],             # Wed/Thu 1PM
    "carousel_outline": [(1, 8), (2, 8)],                # Tue/Wed 8AM (same as LinkedIn)
}


def next_publish_window(platform: str, after: datetime | None = None) -> datetime:
    """
    Return the next optimal publish datetime (UK time) for a given platform.

    Args:
        platform: Platform key (e.g. 'linkedin')
        after: Find window after this datetime (default: now)

    Returns:
        datetime in UK timezone for next window.
    """
    now = after or datetime.now(UK_TZ)
    windows = PLATFORM_WINDOWS.get(platform, [(1, 9)])  # Default: Monday 9AM

    candidates = []
    for days_ahead in range(8):  # Look up to 1 week ahead
        candidate_date = now.date() + timedelta(days=days_ahead)
        candidate_weekday = candidate_date.weekday()
        for weekday, hour in windows:
            if candidate_weekday == weekday:
                candidate_dt = datetime(
                    candidate_date.year, candidate_date.month, candidate_date.day,
                    hour, 0, 0, tzinfo=UK_TZ
                )
                if candidate_dt > now:
                    candidates.append(candidate_dt)

    if not candidates:
        # Fallback: 24 hours from now
        return now + timedelta(hours=24)

    return min(candidates)


async def _publish_variant(variant: ContentVariantORM, session) -> None:
    """Execute publish for a single approved variant."""
    from app.content.publishers import linkedin, twitter, substack

    content = variant.final_content
    metadata = variant.metadata_
    success = False
    post_id = None
    error = None

    try:
        if variant.platform == "linkedin":
            result = await linkedin.post_to_linkedin(content)
            success = result.success
            post_id = result.post_id
            error = result.error

        elif variant.platform == "twitter_thread":
            result = await twitter.post_variant(content, metadata)
            success = result.success
            post_id = result.thread_id
            error = result.error

        elif variant.platform == "substack_intro":
            # Create draft only. Ewan publishes.
            result = await substack.create_draft(
                title="[Draft] " + (variant.job.title or "Untitled"),
                body=content,
            )
            success = result.success
            post_id = result.draft_id
            error = result.error

        elif variant.platform in ("facebook", "carousel_outline"):
            # Facebook and carousel: no automated publisher yet (Phase 2).
            # Mark as needing manual action and log.
            logger.info(
                "Platform '%s' (variant %d) queued for manual publish — no automated publisher yet",
                variant.platform, variant.id
            )
            success = True  # Don't retry — just flag it
            error = "Manual publish required (no automated publisher for this platform yet)"

        else:
            logger.warning("Unknown platform '%s' for variant %d", variant.platform, variant.id)
            success = False
            error = f"Unknown platform: {variant.platform}"

    except Exception as e:
        logger.error("Publish exception for variant %d: %s", variant.id, e)
        success = False
        error = str(e)

    # Update variant record
    now = datetime.now(UK_TZ)
    variant.published_at = now if success else None
    variant.publish_status = "published" if success else "failed"
    variant.publish_error = error if not success else None

    # Create or update analytics row
    existing_analytics = None
    for a in variant.analytics:
        existing_analytics = a
        break

    if not existing_analytics and success:
        analytics = ContentAnalyticsORM(
            variant_id=variant.id,
            platform=variant.platform,
            published_at=now,
            platform_post_id=post_id,
        )
        session.add(analytics)

    await session.commit()

    if success:
        logger.info("✅ Published variant %d (%s)", variant.id, variant.platform)
    else:
        logger.error("❌ Publish failed for variant %d (%s): %s", variant.id, variant.platform, error)


async def _check_and_publish() -> None:
    """
    Main scheduler job — runs every 5 minutes.

    Finds variants that are approved+queued and scheduled_for <= now, then publishes.
    Also schedules variants that have no scheduled_for yet.
    """
    now = datetime.now(UK_TZ)

    async with async_session_maker() as session:
        # 1. Assign scheduled_for to newly approved variants
        result = await session.execute(
            select(ContentVariantORM).where(
                ContentVariantORM.review_status == "approved",
                ContentVariantORM.publish_status == "queued",
                ContentVariantORM.scheduled_for.is_(None),
            )
        )
        unscheduled = result.scalars().all()
        for v in unscheduled:
            v.scheduled_for = next_publish_window(v.platform)
            logger.info(
                "Scheduled variant %d (%s) for %s",
                v.id, v.platform, v.scheduled_for.isoformat()
            )
        if unscheduled:
            await session.commit()

    async with async_session_maker() as session:
        # 2. Find variants ready to publish now
        result = await session.execute(
            select(ContentVariantORM).where(
                ContentVariantORM.review_status == "approved",
                ContentVariantORM.publish_status == "queued",
                ContentVariantORM.scheduled_for <= now,
            )
        )
        ready = result.scalars().all()

    if not ready:
        return

    logger.info("Scheduler: %d variant(s) ready to publish", len(ready))
    async with async_session_maker() as session:
        for v in ready:
            # Re-fetch inside session for relationship loading
            variant = await session.get(ContentVariantORM, v.id)
            if variant:
                await _publish_variant(variant, session)


async def _send_weekly_digest() -> None:
    """
    Weekly Telegram digest: top 3 performing pieces of the week.
    Fires every Monday at 9AM UK time.
    """
    try:
        from app.content.telegram_gate import _get_bot_token, _get_chat_id
        from telegram import Bot

        async with async_session_maker() as session:
            # Top 3 by likes + shares this week
            week_ago = datetime.now(UK_TZ) - timedelta(days=7)
            result = await session.execute(
                select(ContentAnalyticsORM).where(
                    ContentAnalyticsORM.published_at >= week_ago
                ).order_by(
                    (ContentAnalyticsORM.likes + ContentAnalyticsORM.shares).desc()
                ).limit(3)
            )
            top = result.scalars().all()

        if not top:
            return

        lines = ["📊 *Weekly content digest — top performers:*\n"]
        for i, a in enumerate(top, 1):
            lines.append(
                f"{i}. *{a.platform.title()}* — 👍 {a.likes} likes, "
                f"🔁 {a.shares} shares, 💬 {a.comments} comments"
            )

        bot = Bot(token=_get_bot_token())
        await bot.send_message(
            chat_id=_get_chat_id(),
            text="\n".join(lines),
            parse_mode="Markdown",
        )
        logger.info("Weekly digest sent to Telegram")

    except Exception as e:
        logger.error("Weekly digest failed: %s", e)


# ---------------------------------------------------------------------------
# Scheduler lifecycle
# ---------------------------------------------------------------------------

_scheduler: AsyncIOScheduler | None = None


def start_content_scheduler() -> None:
    """
    Start the content scheduler. Call from CRM startup (after event loop is running).
    Registers two jobs:
    1. Every 5 minutes: check_and_publish
    2. Every Monday 9AM UK: weekly digest
    """
    global _scheduler
    _scheduler = AsyncIOScheduler(timezone=UK_TZ)

    _scheduler.add_job(
        _check_and_publish,
        trigger=IntervalTrigger(minutes=5),
        id="content_check_and_publish",
        name="Content: check and publish approved variants",
        replace_existing=True,
    )

    _scheduler.add_job(
        _send_weekly_digest,
        trigger="cron",
        day_of_week="mon",
        hour=9,
        minute=0,
        id="content_weekly_digest",
        name="Content: weekly Telegram digest",
        replace_existing=True,
        timezone=UK_TZ,
    )

    _scheduler.start()
    logger.info("Content scheduler started (check every 5 min, weekly digest Mon 9AM UK)")


def stop_content_scheduler() -> None:
    global _scheduler
    if _scheduler and _scheduler.running:
        _scheduler.shutdown(wait=False)
        _scheduler = None
        logger.info("Content scheduler stopped")

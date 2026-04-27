"""
Content Review Gate — Telegram Bot

EWAN APPROVES EVERYTHING. Nothing publishes without his say-so.

Flow per variant:
1. Bot sends variant text with platform label + inline buttons
2. Ewan clicks:
   - ✅ Approve → variant marked approved, queued to scheduler
   - ✏️ Edit → bot asks Ewan to send edited text, waits for reply
   - ❌ Reject → variant dropped, reason logged
3. Bot confirms each action

Setup needed (add to ~/.amplified/keys.env):
  CONTENT_TELEGRAM_BOT_TOKEN=...   (can reuse existing bot or create new one)
  CONTENT_TELEGRAM_CHAT_ID=...     (Ewan's chat ID — get from @userinfobot)

NOTE: Uses long-polling (not webhook) so it can run alongside the CRM server
without needing a public URL. Start it with the background scheduler.
"""

import asyncio
import logging
import os
from typing import Optional

from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession
from telegram import Bot, InlineKeyboardButton, InlineKeyboardMarkup, Update
from telegram.ext import (
    Application,
    CallbackQueryHandler,
    ContextTypes,
    MessageHandler,
    filters,
)

from app.content.models_orm import ContentVariantORM
from app.database import async_session_maker

logger = logging.getLogger(__name__)

# Callback data prefixes
CB_APPROVE = "ca"   # ca:{variant_id}
CB_REJECT = "cr"    # cr:{variant_id}
CB_EDIT = "ce"      # ce:{variant_id}

PLATFORM_LABELS = {
    "linkedin": "LinkedIn",
    "twitter_thread": "X/Twitter Thread",
    "substack_intro": "Substack Intro",
    "facebook": "Facebook",
    "carousel_outline": "LinkedIn Carousel",
}


def _get_bot_token() -> str:
    token = os.environ.get("CONTENT_TELEGRAM_BOT_TOKEN") or os.environ.get("TELEGRAM_BOT_TOKEN")
    if not token:
        raise RuntimeError(
            "No Telegram bot token found. Add CONTENT_TELEGRAM_BOT_TOKEN to ~/.amplified/keys.env"
        )
    return token


def _get_chat_id() -> int:
    chat_id = os.environ.get("CONTENT_TELEGRAM_CHAT_ID") or os.environ.get("TELEGRAM_CHAT_ID")
    if not chat_id:
        raise RuntimeError(
            "No Telegram chat ID found. Add CONTENT_TELEGRAM_CHAT_ID to ~/.amplified/keys.env\n"
            "Get your chat ID from @userinfobot on Telegram."
        )
    return int(chat_id)


async def send_variant_for_review(variant_id: int) -> None:
    """
    Send a single content variant to Ewan's Telegram for review.
    Called by the router after atomisation completes.
    """
    async with async_session_maker() as session:
        variant = await session.get(ContentVariantORM, variant_id)
        if not variant:
            logger.error("send_variant_for_review: variant %d not found", variant_id)
            return

    label = PLATFORM_LABELS.get(variant.platform, variant.platform.upper())
    header = f"📝 *Content Review — {label}*\n\n"
    body = variant.content

    # Truncate if too long for Telegram (4096 char limit)
    max_body = 3800
    if len(body) > max_body:
        body = body[:max_body] + "\n\n[...truncated — full text in DB]"

    message_text = header + body

    keyboard = InlineKeyboardMarkup([
        [
            InlineKeyboardButton("✅ Approve", callback_data=f"{CB_APPROVE}:{variant_id}"),
            InlineKeyboardButton("✏️ Edit", callback_data=f"{CB_EDIT}:{variant_id}"),
            InlineKeyboardButton("❌ Reject", callback_data=f"{CB_REJECT}:{variant_id}"),
        ]
    ])

    bot = Bot(token=_get_bot_token())
    chat_id = _get_chat_id()

    msg = await bot.send_message(
        chat_id=chat_id,
        text=message_text,
        reply_markup=keyboard,
        parse_mode="Markdown",
    )

    # Store Telegram message ID so we can edit it after review
    async with async_session_maker() as session:
        variant = await session.get(ContentVariantORM, variant_id)
        if variant:
            variant.telegram_message_id = msg.message_id
            await session.commit()

    logger.info("Sent variant %d (%s) to Telegram for review", variant_id, variant.platform)


async def send_job_variants_for_review(job_id: int) -> None:
    """
    Send all variants from a job to Telegram, one at a time with a short delay.
    Called after atomisation completes.
    """
    async with async_session_maker() as session:
        result = await session.execute(
            select(ContentVariantORM).where(ContentVariantORM.job_id == job_id)
        )
        variants = result.scalars().all()

    logger.info("Sending %d variants for job %d to Telegram", len(variants), job_id)
    for v in variants:
        await send_variant_for_review(v.id)
        await asyncio.sleep(1.5)  # Don't flood


# ---------------------------------------------------------------------------
# Callback handlers
# ---------------------------------------------------------------------------

async def _on_callback(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    """Handle inline button presses from Ewan."""
    query = update.callback_query
    await query.answer()

    data = query.data
    if ":" not in data:
        return

    prefix, variant_id_str = data.split(":", 1)
    variant_id = int(variant_id_str)

    if prefix == CB_APPROVE:
        await _handle_approve(query, variant_id, context)
    elif prefix == CB_REJECT:
        await _handle_reject(query, variant_id, context)
    elif prefix == CB_EDIT:
        await _handle_edit_request(query, variant_id, context)


async def _handle_approve(query, variant_id: int, context) -> None:
    async with async_session_maker() as session:
        variant = await session.get(ContentVariantORM, variant_id)
        if not variant:
            await query.edit_message_text("❌ Variant not found.")
            return
        variant.review_status = "approved"
        variant.publish_status = "queued"
        await session.commit()

    label = PLATFORM_LABELS.get(variant.platform, variant.platform)
    await query.edit_message_text(
        f"✅ *{label}* approved — queued for publishing at optimal time.",
        parse_mode="Markdown",
    )
    logger.info("Variant %d approved by Ewan", variant_id)


async def _handle_reject(query, variant_id: int, context) -> None:
    async with async_session_maker() as session:
        variant = await session.get(ContentVariantORM, variant_id)
        if not variant:
            await query.edit_message_text("❌ Variant not found.")
            return
        variant.review_status = "rejected"
        variant.reject_reason = "Rejected via Telegram"
        await session.commit()

    label = PLATFORM_LABELS.get(variant.platform, variant.platform)
    await query.edit_message_text(
        f"❌ *{label}* rejected — dropped from queue.",
        parse_mode="Markdown",
    )
    logger.info("Variant %d rejected by Ewan", variant_id)


async def _handle_edit_request(query, variant_id: int, context) -> None:
    """Ask Ewan to send the edited version as a reply."""
    async with async_session_maker() as session:
        variant = await session.get(ContentVariantORM, variant_id)
        if not variant:
            await query.edit_message_text("❌ Variant not found.")
            return

    label = PLATFORM_LABELS.get(variant.platform, variant.platform)
    await query.edit_message_text(
        f"✏️ *{label}* — send me your edited version as a reply to this message.",
        parse_mode="Markdown",
    )
    # Store variant_id in user_data so the next message handler knows what to update
    context.user_data["editing_variant_id"] = variant_id
    logger.info("Edit requested for variant %d", variant_id)


async def _on_edit_reply(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    """Handle Ewan's edited text for a variant."""
    variant_id = context.user_data.get("editing_variant_id")
    if not variant_id:
        return  # Not editing anything — ignore

    edited_text = update.message.text
    async with async_session_maker() as session:
        variant = await session.get(ContentVariantORM, variant_id)
        if not variant:
            await update.message.reply_text("❌ Variant not found.")
            return
        variant.edited_content = edited_text
        variant.review_status = "approved"
        variant.publish_status = "queued"
        await session.commit()

    context.user_data.pop("editing_variant_id", None)
    label = PLATFORM_LABELS.get(variant.platform, variant.platform)
    await update.message.reply_text(
        f"✅ *{label}* updated and approved — queued for publishing.",
        parse_mode="Markdown",
    )
    logger.info("Variant %d edited and approved by Ewan", variant_id)


# ---------------------------------------------------------------------------
# Bot lifecycle — run as background task alongside CRM server
# ---------------------------------------------------------------------------

_application: Application | None = None


async def start_review_bot() -> None:
    """
    Start the Telegram review bot using long-polling.
    Called from the scheduler startup, not from main.py lifespan directly
    (to avoid blocking if Telegram token isn't set up yet).
    """
    global _application
    try:
        token = _get_bot_token()
    except RuntimeError as e:
        logger.warning("Content Telegram bot not started: %s", e)
        return

    _application = Application.builder().token(token).build()
    _application.add_handler(CallbackQueryHandler(_on_callback))
    _application.add_handler(
        MessageHandler(filters.TEXT & ~filters.COMMAND, _on_edit_reply)
    )

    logger.info("Content review bot starting (long-polling)")
    try:
        await _application.initialize()
        await _application.start()
        await _application.updater.start_polling(drop_pending_updates=True)
        logger.info("Content review bot running")
    except Exception as e:
        logger.warning(
            "Content review bot failed to start (%s). "
            "Set CONTENT_TELEGRAM_BOT_TOKEN to a dedicated bot token — "
            "currently falling back to TELEGRAM_BOT_TOKEN which is already in use by Sam.",
            e,
        )
        _application = None


async def stop_review_bot() -> None:
    global _application
    if _application:
        await _application.updater.stop()
        await _application.stop()
        await _application.shutdown()
        _application = None
        logger.info("Content review bot stopped")

"""NightScout pipeline — the master fetch→score→fork→store orchestrator."""

from __future__ import annotations

import asyncio
import logging
import time
from datetime import datetime, timezone

import asyncpg
import httpx

from .config import (
    POSTGRES_DSN,
    SCORING_BATCH_SIZE,
    SOURCES,
    RelevanceTier,
    SourceDef,
)
from .fetchers import RawItem, fetch_source
from .scorer import ScoredItem, score_batch

logger = logging.getLogger("nightscout.pipeline")


async def run_pipeline() -> dict:
    """Execute the full NightScout pipeline.

    Returns summary stats dict.
    """
    start = time.monotonic()
    stats = {
        "sources_fetched": 0,
        "items_fetched": 0,
        "items_scored": 0,
        "items_briefing": 0,
        "items_rd": 0,
        "items_critical": 0,
        "errors": [],
    }

    pool = await asyncpg.create_pool(POSTGRES_DSN, min_size=2, max_size=5)
    run_id = await _create_run(pool)

    try:
        async with httpx.AsyncClient() as client:
            # ── PHASE 1: Fetch from all sources concurrently ──
            enabled_sources = [s for s in SOURCES if s.enabled]
            logger.info(f"Fetching from {len(enabled_sources)} sources...")

            fetch_tasks = [fetch_source(client, s) for s in enabled_sources]
            fetch_results = await asyncio.gather(*fetch_tasks, return_exceptions=True)

            all_items: list[RawItem] = []
            for i, result in enumerate(fetch_results):
                if isinstance(result, Exception):
                    stats["errors"].append(f"{enabled_sources[i].name}: {result}")
                    continue
                stats["sources_fetched"] += 1
                all_items.extend(result)

            stats["items_fetched"] = len(all_items)
            logger.info(f"Fetched {len(all_items)} items from {stats['sources_fetched']} sources")

            # ── PHASE 2: Dedup against existing items ──
            all_items = await _dedup_items(pool, all_items)
            logger.info(f"After dedup: {len(all_items)} new items")

            if not all_items:
                logger.info("No new items to score. Pipeline complete.")
                await _complete_run(pool, run_id, stats, start)
                return stats

            # ── PHASE 3: Store raw items ──
            source_id_map = await _ensure_sources(pool, enabled_sources)
            await _store_raw_items(pool, all_items, source_id_map)

            # ── PHASE 4: Score in batches ──
            all_scored: list[ScoredItem] = []
            for i in range(0, len(all_items), SCORING_BATCH_SIZE):
                batch = all_items[i : i + SCORING_BATCH_SIZE]
                scored = await score_batch(client, batch)
                all_scored.extend(scored)
                logger.info(f"Scored batch {i // SCORING_BATCH_SIZE + 1}: {len(scored)} items")

            stats["items_scored"] = len(all_scored)

            # ── PHASE 5: Fork by tier ──
            for item in all_scored:
                if item.tier == RelevanceTier.BRIEFING:
                    stats["items_briefing"] += 1
                elif item.tier == RelevanceTier.RD_PIPELINE:
                    stats["items_rd"] += 1
                elif item.tier == RelevanceTier.CRITICAL:
                    stats["items_critical"] += 1

            # ── PHASE 6: Store scored items ──
            await _store_scored_items(pool, all_scored, source_id_map)

            # ── PHASE 7: Handle critical items (immediate notification) ──
            critical = [s for s in all_scored if s.tier == RelevanceTier.CRITICAL]
            if critical:
                await _notify_critical(client, critical)

    except Exception as e:
        stats["errors"].append(f"Pipeline error: {e}")
        logger.exception("Pipeline failed")
    finally:
        await _complete_run(pool, run_id, stats, start)
        await pool.close()

    return stats


# ============================================================
# Database helpers
# ============================================================

async def _create_run(pool: asyncpg.Pool) -> str:
    """Create a pipeline run record, return its ID."""
    row = await pool.fetchrow(
        "INSERT INTO ns_pipeline_runs DEFAULT VALUES RETURNING id"
    )
    return str(row["id"])


async def _complete_run(pool: asyncpg.Pool, run_id: str, stats: dict, start: float) -> None:
    """Mark pipeline run as complete."""
    duration_ms = int((time.monotonic() - start) * 1000)
    status = "completed" if not stats["errors"] else "completed_with_errors"
    error_text = "\n".join(stats["errors"]) if stats["errors"] else None
    await pool.execute(
        """UPDATE ns_pipeline_runs SET
            completed_at = now(), status = $1,
            sources_fetched = $2, items_fetched = $3, items_scored = $4,
            items_briefing = $5, items_rd = $6, items_critical = $7,
            error = $8, duration_ms = $9
        WHERE id = $10""",
        status, stats["sources_fetched"], stats["items_fetched"],
        stats["items_scored"], stats["items_briefing"], stats["items_rd"],
        stats["items_critical"], error_text, duration_ms, run_id,
    )
    logger.info(f"Pipeline run {run_id}: {status} in {duration_ms}ms")


async def _dedup_items(pool: asyncpg.Pool, items: list[RawItem]) -> list[RawItem]:
    """Remove items that already exist in the database."""
    if not items:
        return []
    ext_ids = [i.external_id for i in items]
    existing = await pool.fetch(
        "SELECT external_id FROM ns_raw_items WHERE external_id = ANY($1)",
        ext_ids,
    )
    existing_set = {r["external_id"] for r in existing}
    return [i for i in items if i.external_id not in existing_set]


async def _ensure_sources(pool: asyncpg.Pool, sources: list[SourceDef]) -> dict[str, str]:
    """Ensure all sources exist in DB, return name→id map."""
    source_map = {}
    for s in sources:
        row = await pool.fetchrow(
            """INSERT INTO ns_sources (name, source_type, url, category, fetch_config)
            VALUES ($1, $2, $3, $4, $5)
            ON CONFLICT (name, source_type, url, category) DO UPDATE SET name = EXCLUDED.name
            RETURNING id""",
            s.name, s.source_type.value, s.url, s.category, "{}",
        )
        if row:
            source_map[s.name] = str(row["id"])
    return source_map


async def _store_raw_items(
    pool: asyncpg.Pool,
    items: list[RawItem],
    source_map: dict[str, str],
) -> None:
    """Bulk insert raw items."""
    for item in items:
        source_id = source_map.get(item.source_name)
        if not source_id:
            continue
        await pool.execute(
            """INSERT INTO ns_raw_items (source_id, external_id, title, url, content, published_at, metadata)
            VALUES ($1, $2, $3, $4, $5, $6, $7)
            ON CONFLICT (source_id, external_id) DO NOTHING""",
            source_id, item.external_id, item.title, item.url,
            item.content[:10000], item.published_at, "{}",
        )


async def _store_scored_items(
    pool: asyncpg.Pool,
    scored: list[ScoredItem],
    source_map: dict[str, str],
) -> None:
    """Store scored items with their ratings."""
    for s in scored:
        # Get the raw_item_id
        source_id = source_map.get(s.raw_item.source_name)
        if not source_id:
            continue
        raw_row = await pool.fetchrow(
            "SELECT id FROM ns_raw_items WHERE source_id = $1 AND external_id = $2",
            source_id, s.raw_item.external_id,
        )
        if not raw_row:
            continue
        await pool.execute(
            """INSERT INTO ns_scored_items
            (raw_item_id, relevance, impact, applicability, novelty, tier, scoring_model, reasoning, tags)
            VALUES ($1, $2, $3, $4, $5, $6, $7, $8, $9)""",
            raw_row["id"], s.relevance, s.impact, s.applicability, s.novelty,
            s.tier.value, s.model, s.reasoning, s.tags,
        )


async def _notify_critical(client: httpx.AsyncClient, critical: list[ScoredItem]) -> None:
    """Send immediate Telegram notification for critical items."""
    from .config import TELEGRAM_BOT_TOKEN, TELEGRAM_CHAT_ID
    if not TELEGRAM_BOT_TOKEN or not TELEGRAM_CHAT_ID:
        logger.warning("Telegram not configured — skipping critical notification")
        return

    for item in critical[:5]:  # Cap at 5 notifications
        text = (
            f"🚨 *CRITICAL INTELLIGENCE*\n\n"
            f"*{item.raw_item.title}*\n"
            f"Score: {item.composite:.1f}/10\n"
            f"Source: {item.raw_item.source_name}\n"
            f"Tags: {', '.join(item.tags)}\n\n"
            f"_{item.reasoning}_\n\n"
            f"{item.raw_item.url or 'No URL'}"
        )
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
        except Exception as e:
            logger.error(f"Telegram notification failed: {e}")

"""NightScout morning briefing generator."""

from __future__ import annotations

import logging
from datetime import datetime, timedelta, timezone

import asyncpg

from .config import POSTGRES_DSN

logger = logging.getLogger("nightscout.briefing")


async def generate_morning_briefing(hours_back: int = 24) -> str:
    """Generate a markdown morning briefing from the last N hours of scored items.

    Returns the briefing as markdown text.
    """
    pool = await asyncpg.create_pool(POSTGRES_DSN, min_size=1, max_size=3)

    try:
        cutoff = datetime.now(timezone.utc) - timedelta(hours=hours_back)

        # Get all scored items from the period, joined with raw items
        rows = await pool.fetch(
            """SELECT
                s.relevance, s.impact, s.applicability, s.novelty,
                s.composite_score, s.tier, s.reasoning, s.tags,
                r.title, r.url, r.content, r.published_at,
                src.name as source_name, src.category
            FROM ns_scored_items s
            JOIN ns_raw_items r ON s.raw_item_id = r.id
            JOIN ns_sources src ON r.source_id = src.id
            WHERE s.scored_at >= $1 AND s.tier != 'noise'
            ORDER BY s.composite_score DESC""",
            cutoff,
        )

        if not rows:
            return _empty_briefing(cutoff)

        # Group by tier
        critical = [r for r in rows if r["tier"] == "critical"]
        rd = [r for r in rows if r["tier"] == "rd_pipeline"]
        briefing_items = [r for r in rows if r["tier"] == "briefing"]

        # Category stats
        categories: dict[str, int] = {}
        for r in rows:
            cat = r["category"]
            categories[cat] = categories.get(cat, 0) + 1

        # Build markdown
        now = datetime.now(timezone.utc)
        md = f"""# 🌅 NightScout Morning Briefing
**Generated:** {now.strftime('%A %d %B %Y, %H:%M UTC')}
**Period:** Last {hours_back} hours | **Items scored:** {len(rows)} above noise threshold

---

## 📊 Overview

| Category | Items |
|----------|-------|
"""
        for cat, count in sorted(categories.items(), key=lambda x: -x[1]):
            md += f"| {cat.replace('_', ' ').title()} | {count} |\n"

        # Critical section
        if critical:
            md += f"\n---\n\n## 🚨 Critical ({len(critical)} items)\n\n"
            for r in critical:
                md += _format_item(r)

        # R&D Pipeline section
        if rd:
            md += f"\n---\n\n## 🔬 R&D Pipeline ({len(rd)} items)\n\n"
            md += "_These items scored 7+/10 and should be evaluated through the R&D Rubric._\n\n"
            for r in rd[:10]:  # Top 10
                md += _format_item(r)

        # Briefing section
        if briefing_items:
            md += f"\n---\n\n## 📰 Briefing ({len(briefing_items)} items)\n\n"
            for r in briefing_items[:15]:  # Top 15
                md += _format_item_compact(r)

        # Footer
        md += f"""
---

_NightScout v1.0 — Amplified Partners Intelligence Pipeline_
_Sources: {len(set(r['source_name'] for r in rows))} active | Items above noise: {len(rows)}_
"""

        # Store the briefing
        briefing_id = await pool.fetchval(
            """INSERT INTO ns_briefings
            (period_start, period_end, summary_md, item_count, top_score, categories)
            VALUES ($1, $2, $3, $4, $5, $6)
            RETURNING id""",
            cutoff, now, md, len(rows),
            rows[0]["composite_score"] if rows else None,
            dict(categories),
        )

        logger.info(f"Generated briefing {briefing_id}: {len(rows)} items")
        return md

    finally:
        await pool.close()


def _format_item(r: asyncpg.Record) -> str:
    """Format a single item in full detail."""
    tags = ", ".join(r["tags"]) if r["tags"] else "—"
    url_line = f"[Read more]({r['url']})" if r["url"] else ""
    return f"""### {r['title']}
**Score:** {r['composite_score']:.1f}/10 (R:{r['relevance']} I:{r['impact']} A:{r['applicability']} N:{r['novelty']})
**Source:** {r['source_name']} | **Tags:** {tags}
{r['reasoning']}
{url_line}

"""


def _format_item_compact(r: asyncpg.Record) -> str:
    """Format a single item compactly."""
    url_part = f" — [link]({r['url']})" if r["url"] else ""
    return f"- **{r['title']}** ({r['composite_score']:.1f}/10, {r['source_name']}){url_part}\n"


def _empty_briefing(cutoff: datetime) -> str:
    """Return briefing when no items found."""
    return f"""# 🌅 NightScout Morning Briefing
**Generated:** {datetime.now(timezone.utc).strftime('%A %d %B %Y, %H:%M UTC')}

No items scored above noise threshold in the last period (since {cutoff.strftime('%H:%M UTC')}).

All quiet on the intelligence front. Either the sources had nothing notable, or the pipeline hasn't run yet.

_NightScout v1.0 — Amplified Partners Intelligence Pipeline_
"""

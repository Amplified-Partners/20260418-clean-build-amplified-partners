"""NightScout MCP Server — Intelligence tools for agents.

Lets any agent in the system query NightScout intelligence:
- Get latest briefing
- Search scored items
- Get pipeline status
- Trigger a pipeline run
"""

from __future__ import annotations

from datetime import datetime, timezone
from typing import Any

import asyncpg
from mcp.server.fastmcp import FastMCP
from pydantic import BaseModel, ConfigDict, Field

SERVICE_NAME = "nightscout"

mcp = FastMCP(
    f"{SERVICE_NAME}_mcp",
    instructions="MCP server for querying NightScout intelligence pipeline data.",
)

# ── Database ──
_pool: asyncpg.Pool | None = None


async def get_pool() -> asyncpg.Pool:
    global _pool
    if _pool is None:
        import os
        dsn = os.getenv("POSTGRES_DSN", "postgresql://cove:cove@localhost:5432/cove")
        _pool = await asyncpg.create_pool(dsn, min_size=1, max_size=5)
    return _pool


# ── Input Models ──

class GetBriefingInput(BaseModel):
    model_config = ConfigDict(strict=True)
    hours_back: int = Field(default=24, description="How many hours back to cover", ge=1, le=168)


class SearchIntelInput(BaseModel):
    model_config = ConfigDict(strict=True)
    query: str = Field(description="Search term for titles and content")
    category: str | None = Field(default=None, description="Filter by category")
    min_score: float = Field(default=4.0, description="Minimum composite score", ge=0, le=10)
    limit: int = Field(default=20, description="Max results", ge=1, le=100)


class GetStatsInput(BaseModel):
    model_config = ConfigDict(strict=True)
    days_back: int = Field(default=7, description="How many days of stats", ge=1, le=90)


# ── Tools ──

@mcp.tool(
    name=f"{SERVICE_NAME}_get_briefing",
    description="Get the latest NightScout morning briefing as markdown.",
    annotations={"readOnlyHint": True, "destructiveHint": False, "idempotentHint": True, "openWorldHint": False},
)
async def get_briefing(input: GetBriefingInput) -> str:
    pool = await get_pool()
    row = await pool.fetchrow(
        """SELECT summary_md, generated_at, item_count, top_score
        FROM ns_briefings
        WHERE period_start >= now() - interval '1 hour' * $1
        ORDER BY generated_at DESC LIMIT 1""",
        input.hours_back,
    )
    if not row:
        return f"No briefing found for the last {input.hours_back} hours. Run the pipeline first."
    return row["summary_md"]


@mcp.tool(
    name=f"{SERVICE_NAME}_search_intel",
    description="Search scored intelligence items by keyword, category, or minimum score.",
    annotations={"readOnlyHint": True, "destructiveHint": False, "idempotentHint": True, "openWorldHint": False},
)
async def search_intel(input: SearchIntelInput) -> str:
    pool = await get_pool()

    conditions = ["s.composite_score >= $1"]
    params: list[Any] = [input.min_score]
    idx = 2

    if input.query:
        conditions.append(f"(r.title ILIKE ${idx} OR r.content ILIKE ${idx})")
        params.append(f"%{input.query}%")
        idx += 1

    if input.category:
        conditions.append(f"src.category = ${idx}")
        params.append(input.category)
        idx += 1

    conditions.append(f"LIMIT ${idx}")
    params.append(input.limit)

    where = " AND ".join(conditions[:-1])  # Don't include LIMIT in WHERE
    query = f"""
        SELECT r.title, r.url, s.composite_score, s.tier,
               s.reasoning, s.tags, src.category, src.name as source_name,
               s.scored_at
        FROM ns_scored_items s
        JOIN ns_raw_items r ON s.raw_item_id = r.id
        JOIN ns_sources src ON r.source_id = src.id
        WHERE {where}
        ORDER BY s.composite_score DESC
        LIMIT ${idx}
    """

    rows = await pool.fetch(query, *params)
    if not rows:
        return f"No intelligence items found matching your criteria."

    lines = [f"## Intelligence Search Results ({len(rows)} items)\n"]
    for r in rows:
        tags = ", ".join(r["tags"]) if r["tags"] else "—"
        url = f" — [link]({r['url']})" if r["url"] else ""
        lines.append(
            f"- **{r['title']}** ({r['composite_score']:.1f}/10, {r['tier']})\n"
            f"  Source: {r['source_name']} | Category: {r['category']} | Tags: {tags}{url}\n"
            f"  _{r['reasoning']}_\n"
        )
    return "\n".join(lines)


@mcp.tool(
    name=f"{SERVICE_NAME}_pipeline_status",
    description="Get NightScout pipeline run statistics.",
    annotations={"readOnlyHint": True, "destructiveHint": False, "idempotentHint": True, "openWorldHint": False},
)
async def pipeline_status(input: GetStatsInput) -> str:
    pool = await get_pool()
    rows = await pool.fetch(
        """SELECT id, started_at, status, sources_fetched, items_fetched,
                  items_scored, items_briefing, items_rd, items_critical, duration_ms
        FROM ns_pipeline_runs
        WHERE started_at >= now() - interval '1 day' * $1
        ORDER BY started_at DESC LIMIT 10""",
        input.days_back,
    )
    if not rows:
        return f"No pipeline runs in the last {input.days_back} days."

    lines = [f"## Pipeline Runs (last {input.days_back} days)\n"]
    for r in rows:
        duration = f"{r['duration_ms']}ms" if r["duration_ms"] else "running"
        lines.append(
            f"- **{r['started_at'].strftime('%Y-%m-%d %H:%M')}** — {r['status']} ({duration})\n"
            f"  Sources: {r['sources_fetched']} | Fetched: {r['items_fetched']} | "
            f"Scored: {r['items_scored']} | Briefing: {r['items_briefing']} | "
            f"R&D: {r['items_rd']} | Critical: {r['items_critical']}\n"
        )
    return "\n".join(lines)


@mcp.tool(
    name=f"{SERVICE_NAME}_run_pipeline",
    description="Trigger a NightScout pipeline run. This fetches from all sources, scores items, and generates a briefing.",
    annotations={"readOnlyHint": False, "destructiveHint": False, "idempotentHint": False, "openWorldHint": True},
)
async def run_pipeline_tool() -> str:
    from nightscout.pipeline import run_pipeline
    stats = await run_pipeline()
    return (
        f"Pipeline complete. Fetched {stats['items_fetched']} items from "
        f"{stats['sources_fetched']} sources. Scored {stats['items_scored']}. "
        f"Briefing: {stats['items_briefing']}, R&D: {stats['items_rd']}, "
        f"Critical: {stats['items_critical']}."
    )


if __name__ == "__main__":
    mcp.run(transport="stdio")

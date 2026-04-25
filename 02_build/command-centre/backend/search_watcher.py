"""
Search Watcher — Background worker that refreshes watched searches.

Runs as an asyncio background task inside the FastAPI app.
Checks every 60 seconds for watched searches due for refresh,
re-runs them via SearXNG, and diffs the results.
"""

import asyncio
import json
import httpx
from datetime import datetime
from search_db import (
    get_due_watches, get_recent_searches, diff_results,
    save_search, save_diff, mark_refreshed,
)

SEARXNG_URL = "https://search.beast.amplifiedpartners.ai"
CHECK_INTERVAL = 60  # seconds between checks

from typing import Optional


async def refresh_search(query: str, categories: str = "general") -> Optional[dict]:
    """Run a search and return the results."""
    try:
        async with httpx.AsyncClient(timeout=15.0) as client:
            r = await client.get(
                f"{SEARXNG_URL}/search",
                params={"q": query, "format": "json", "categories": categories},
            )
            data = r.json()
            results = []
            for item in data.get("results", [])[:15]:
                results.append({
                    "title": item.get("title", ""),
                    "url": item.get("url", ""),
                    "content": item.get("content", ""),
                    "engine": item.get("engine", ""),
                })
            return {
                "results": results,
                "total": len(data.get("results", [])),
            }
    except Exception as e:
        print(f"[watcher] Error refreshing '{query}': {e}")
        return None


async def process_due_watches():
    """Find and refresh all due watched searches."""
    due = get_due_watches()
    if not due:
        return

    print(f"[watcher] {len(due)} watched searches due for refresh")

    for watch in due:
        query = watch["query"]
        categories = watch.get("categories", "general")
        schedule = watch.get("schedule", "daily")

        print(f"[watcher] Refreshing: '{query}'")

        # Get the most recent saved results for this query
        from search_db import get_db
        conn = get_db()
        old_row = conn.execute(
            "SELECT results FROM searches WHERE query = ? ORDER BY searched_at DESC LIMIT 1",
            (query,),
        ).fetchone()
        conn.close()

        old_results = json.loads(old_row["results"]) if old_row else []

        # Run the fresh search
        new_data = await refresh_search(query, categories)
        if not new_data:
            continue

        new_results = new_data["results"]

        # Save the new search
        save_search(query, categories, new_results, new_data["total"])

        # Diff and save
        diff = diff_results(old_results, new_results)
        save_diff(query, diff)

        # Mark as refreshed
        mark_refreshed(query, schedule)

        if diff["has_changes"]:
            print(f"[watcher] '{query}' has changes: +{diff['new_count']} -{diff['removed_count']}")
        else:
            print(f"[watcher] '{query}' — no changes")


async def watcher_loop():
    """Main watcher loop — runs forever."""
    print("[watcher] Search watcher started")
    while True:
        try:
            await process_due_watches()
        except Exception as e:
            print(f"[watcher] Error in watcher loop: {e}")
        await asyncio.sleep(CHECK_INTERVAL)

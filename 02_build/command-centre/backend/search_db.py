"""
Search Intelligence — SQLite persistence + watched search logic.

Every search is saved. Important ones can be "watched" and auto-refresh
via Beast's SearXNG on a schedule (daily/weekly).
"""

import sqlite3
import json
import os
from datetime import datetime, timedelta
from typing import Optional

DB_PATH = os.path.join(os.path.dirname(__file__), "searches.db")


def get_db() -> sqlite3.Connection:
    """Get a connection with row_factory for dict-like access."""
    conn = sqlite3.connect(DB_PATH)
    conn.row_factory = sqlite3.Row
    conn.execute("PRAGMA journal_mode=WAL")
    return conn


def init_db():
    """Create tables if they don't exist."""
    conn = get_db()
    conn.executescript("""
        CREATE TABLE IF NOT EXISTS searches (
            id          INTEGER PRIMARY KEY AUTOINCREMENT,
            query       TEXT NOT NULL,
            categories  TEXT DEFAULT 'general',
            results     TEXT NOT NULL,
            total       INTEGER DEFAULT 0,
            searched_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
        );

        CREATE TABLE IF NOT EXISTS watched_searches (
            id          INTEGER PRIMARY KEY AUTOINCREMENT,
            query       TEXT NOT NULL UNIQUE,
            categories  TEXT DEFAULT 'general',
            schedule    TEXT DEFAULT 'daily',
            last_run    TIMESTAMP,
            next_run    TIMESTAMP,
            has_changes BOOLEAN DEFAULT 0,
            created_at  TIMESTAMP DEFAULT CURRENT_TIMESTAMP
        );

        CREATE TABLE IF NOT EXISTS search_diffs (
            id           INTEGER PRIMARY KEY AUTOINCREMENT,
            query        TEXT NOT NULL,
            new_urls     TEXT,
            removed_urls TEXT,
            new_count    INTEGER DEFAULT 0,
            removed_count INTEGER DEFAULT 0,
            diffed_at    TIMESTAMP DEFAULT CURRENT_TIMESTAMP
        );

        CREATE INDEX IF NOT EXISTS idx_searches_query ON searches(query);
        CREATE INDEX IF NOT EXISTS idx_searches_time ON searches(searched_at DESC);
        CREATE INDEX IF NOT EXISTS idx_watched_next ON watched_searches(next_run);
    """)
    conn.commit()
    conn.close()


# ── Save & Retrieve ───────────────────────────────────

def save_search(query: str, categories: str, results: list, total: int) -> int:
    """Save a search and its results. Returns the search ID."""
    conn = get_db()
    cur = conn.execute(
        "INSERT INTO searches (query, categories, results, total) VALUES (?, ?, ?, ?)",
        (query, categories, json.dumps(results), total),
    )
    search_id = cur.lastrowid
    conn.commit()
    conn.close()
    return search_id


def get_recent_searches(limit: int = 30) -> list[dict]:
    """Get recent searches, most recent first."""
    conn = get_db()
    rows = conn.execute(
        "SELECT id, query, categories, total, searched_at FROM searches ORDER BY searched_at DESC LIMIT ?",
        (limit,),
    ).fetchall()
    conn.close()
    return [dict(r) for r in rows]


def get_search_by_id(search_id: int) -> Optional[dict]:
    """Get a single search with full results."""
    conn = get_db()
    row = conn.execute("SELECT * FROM searches WHERE id = ?", (search_id,)).fetchone()
    conn.close()
    if row:
        d = dict(row)
        d["results"] = json.loads(d["results"])
        return d
    return None


# ── Watch / Unwatch ───────────────────────────────────

def watch_search(query: str, categories: str = "general", schedule: str = "daily") -> dict:
    """Start watching a search query. Returns the watch record."""
    conn = get_db()
    now = datetime.utcnow()
    next_run = now + (timedelta(days=1) if schedule == "daily" else timedelta(weeks=1))

    conn.execute(
        """INSERT INTO watched_searches (query, categories, schedule, last_run, next_run)
           VALUES (?, ?, ?, ?, ?)
           ON CONFLICT(query) DO UPDATE SET schedule=?, next_run=?, has_changes=0""",
        (query, categories, schedule, now.isoformat(), next_run.isoformat(),
         schedule, next_run.isoformat()),
    )
    conn.commit()

    row = conn.execute("SELECT * FROM watched_searches WHERE query = ?", (query,)).fetchone()
    conn.close()
    return dict(row)


def unwatch_search(query: str) -> bool:
    """Stop watching a query."""
    conn = get_db()
    cur = conn.execute("DELETE FROM watched_searches WHERE query = ?", (query,))
    conn.commit()
    conn.close()
    return cur.rowcount > 0


def get_watched_searches() -> list[dict]:
    """List all watched searches."""
    conn = get_db()
    rows = conn.execute(
        "SELECT * FROM watched_searches ORDER BY created_at DESC",
    ).fetchall()
    conn.close()
    return [dict(r) for r in rows]


def is_watched(query: str) -> bool:
    """Check if a query is being watched."""
    conn = get_db()
    row = conn.execute("SELECT id FROM watched_searches WHERE query = ?", (query,)).fetchone()
    conn.close()
    return row is not None


# ── Diffing ───────────────────────────────────────────

def diff_results(old_results: list[dict], new_results: list[dict]) -> dict:
    """Compare two result sets and return the diff."""
    old_urls = {r.get("url", "") for r in old_results}
    new_urls = {r.get("url", "") for r in new_results}

    added = new_urls - old_urls
    removed = old_urls - new_urls

    return {
        "new_urls": list(added),
        "removed_urls": list(removed),
        "new_count": len(added),
        "removed_count": len(removed),
        "has_changes": len(added) > 0 or len(removed) > 0,
    }


def save_diff(query: str, diff: dict):
    """Save a diff result."""
    conn = get_db()
    conn.execute(
        "INSERT INTO search_diffs (query, new_urls, removed_urls, new_count, removed_count) VALUES (?, ?, ?, ?, ?)",
        (query, json.dumps(diff["new_urls"]), json.dumps(diff["removed_urls"]),
         diff["new_count"], diff["removed_count"]),
    )
    # Mark the watched search as having changes
    if diff["has_changes"]:
        conn.execute("UPDATE watched_searches SET has_changes = 1 WHERE query = ?", (query,))
    conn.commit()
    conn.close()


def get_diffs_for_query(query: str, limit: int = 10) -> list[dict]:
    """Get diff history for a query."""
    conn = get_db()
    rows = conn.execute(
        "SELECT * FROM search_diffs WHERE query = ? ORDER BY diffed_at DESC LIMIT ?",
        (query, limit),
    ).fetchall()
    conn.close()
    results = []
    for r in rows:
        d = dict(r)
        d["new_urls"] = json.loads(d["new_urls"]) if d["new_urls"] else []
        d["removed_urls"] = json.loads(d["removed_urls"]) if d["removed_urls"] else []
        results.append(d)
    return results


def get_due_watches() -> list[dict]:
    """Get watched searches that are due for refresh."""
    conn = get_db()
    now = datetime.utcnow().isoformat()
    rows = conn.execute(
        "SELECT * FROM watched_searches WHERE next_run <= ?", (now,),
    ).fetchall()
    conn.close()
    return [dict(r) for r in rows]


def mark_refreshed(query: str, schedule: str):
    """Update last_run and next_run after a refresh."""
    conn = get_db()
    now = datetime.utcnow()
    next_run = now + (timedelta(days=1) if schedule == "daily" else timedelta(weeks=1))
    conn.execute(
        "UPDATE watched_searches SET last_run = ?, next_run = ? WHERE query = ?",
        (now.isoformat(), next_run.isoformat(), query),
    )
    conn.commit()
    conn.close()


def clear_changes(query: str):
    """Mark a watched search's changes as seen."""
    conn = get_db()
    conn.execute("UPDATE watched_searches SET has_changes = 0 WHERE query = ?", (query,))
    conn.commit()
    conn.close()


# Initialize on import
init_db()

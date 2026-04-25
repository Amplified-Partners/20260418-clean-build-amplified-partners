"""Email Agent status — inbox overview and pending actions."""

from __future__ import annotations

import asyncpg

from .config import POSTGRES_DSN


async def get_inbox_status() -> str:
    """Generate a markdown summary of inbox state."""
    pool = await asyncpg.create_pool(POSTGRES_DSN, min_size=1, max_size=2)

    try:
        # Unhandled counts by priority
        priority_rows = await pool.fetch(
            """SELECT priority, count(*) as cnt
               FROM emails_inbound
               WHERE NOT handled
               GROUP BY priority
               ORDER BY CASE priority
                   WHEN 'critical' THEN 1
                   WHEN 'urgent' THEN 2
                   WHEN 'normal' THEN 3
                   WHEN 'low' THEN 4
               END"""
        )

        # Pending drafts
        draft_count = await pool.fetchval(
            "SELECT count(*) FROM email_drafts WHERE status = 'pending_review'"
        )

        # Recent pipeline run
        last_run = await pool.fetchrow(
            """SELECT started_at, completed_at, emails_fetched, emails_triaged,
                      drafts_created, auto_handled
               FROM email_pipeline_runs
               ORDER BY started_at DESC
               LIMIT 1"""
        )

        # Unhandled by action
        action_rows = await pool.fetch(
            """SELECT action, count(*) as cnt
               FROM emails_inbound
               WHERE NOT handled
               GROUP BY action"""
        )

        lines = ["# 📬 Email Agent — Inbox Status\n"]

        # Priority breakdown
        lines.append("## Unhandled by Priority")
        total_unhandled = 0
        for row in priority_rows:
            emoji = {"critical": "🔴", "urgent": "🟠", "normal": "🟡", "low": "🟢"}.get(
                row["priority"], "⚪"
            )
            lines.append(f"- {emoji} **{row['priority'].title()}**: {row['cnt']}")
            total_unhandled += row["cnt"]
        if not priority_rows:
            lines.append("- ✅ Inbox zero!")
        lines.append(f"\n**Total unhandled: {total_unhandled}**\n")

        # Action breakdown
        lines.append("## Pending Actions")
        for row in action_rows:
            lines.append(f"- {row['action'].title()}: {row['cnt']}")

        # Drafts
        lines.append(f"\n## Drafts Awaiting Review: {draft_count}\n")

        # Last run
        if last_run:
            lines.append("## Last Pipeline Run")
            lines.append(f"- Started: {last_run['started_at']}")
            if last_run["completed_at"]:
                lines.append(f"- Completed: {last_run['completed_at']}")
            lines.append(f"- Fetched: {last_run['emails_fetched']}")
            lines.append(f"- Triaged: {last_run['emails_triaged']}")
            lines.append(f"- Drafts: {last_run['drafts_created']}")
            lines.append(f"- Auto-handled: {last_run['auto_handled']}")

        return "\n".join(lines)

    finally:
        await pool.close()

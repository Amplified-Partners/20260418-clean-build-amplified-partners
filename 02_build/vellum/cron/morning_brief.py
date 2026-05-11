"""Morning Brief cron — 06:25 generate, 06:30 deliver.

Scheduled job that:
1. Creates a new Brief sheet for the Jesmond tenant
2. Calls each researcher agent (Stripe, Calendar, SearXNG)
3. Calls the Synthesiser to compose the narrative
4. Writes the brief entries to the sheet
5. At 06:30: generates a phone-bound share token and sends via iMessage

Environment variables:
    JESMOND_BOB_PHONE     — recipient phone number (E.164)
    BRIEF_BASE_URL        — API root (default: https://api.amplifiedpartners.ai)
    BRIEF_TOKEN_SECRET    — HMAC secret for generating share tokens
    IMESSAGE_HOST         — Mac SSH host (used by delivery.imessage)
    IMESSAGE_USER         — Mac SSH user
    IMESSAGE_KEY_PATH     — Mac SSH key path
"""

from __future__ import annotations

import asyncio
import hashlib
import hmac
import logging
import os
from datetime import datetime, timezone
from uuid import uuid4

from vellum.agents import ResearcherOutput
from vellum.delivery.imessage import send_brief_link
from vellum.delivery.share_links import generate_share_url
from vellum.models import Sheet, SheetEntry, SheetMeta, ShareToken

logger = logging.getLogger(__name__)

# ---------------------------------------------------------------------------
# Researcher stubs — real implementations live in agents/ (daughter #2).
# These are safe to import when available, with graceful fallback.
# ---------------------------------------------------------------------------

_SECTION_UNAVAILABLE = "[section unavailable]"


async def _call_researcher(
    name: str,
    fetch_coro: object | None,
    tenant_id: str,
    date: datetime,
) -> ResearcherOutput | None:
    """Call a researcher, returning None on any failure."""
    if fetch_coro is None:
        logger.warning("Researcher %s not available — skipping", name)
        return None
    try:
        result: ResearcherOutput = await fetch_coro  # type: ignore[misc]
        logger.info("Researcher %s returned: %s", name, result.summary)
        return result
    except Exception:
        logger.exception("Researcher %s failed", name)
        return None


def _try_import_researcher(module_path: str, class_name: str) -> object | None:
    """Attempt to import a researcher class; return None if unavailable."""
    try:
        import importlib

        mod = importlib.import_module(module_path)
        return getattr(mod, class_name, None)
    except (ImportError, AttributeError):
        return None


async def _gather_research(
    tenant_id: str,
    date: datetime,
) -> list[ResearcherOutput | None]:
    """Run all researcher agents concurrently."""
    researcher_specs = [
        ("vellum.agents.researcher_stripe", "StripeResearcher", "stripe"),
        ("vellum.agents.researcher_calendar", "CalendarResearcher", "calendar"),
        ("vellum.agents.researcher_searxng", "SearXNGResearcher", "searxng"),
    ]

    tasks: list[asyncio.Task[ResearcherOutput | None]] = []
    for module_path, class_name, label in researcher_specs:
        cls = _try_import_researcher(module_path, class_name)
        if cls is not None:
            try:
                instance = cls()  # type: ignore[operator]
                coro = instance.fetch(tenant_id, date)
            except Exception:
                logger.exception("Failed to instantiate %s", class_name)
                coro = None
        else:
            coro = None
        tasks.append(
            asyncio.create_task(
                _call_researcher(label, coro, tenant_id, date),
            )
        )

    return list(await asyncio.gather(*tasks))


async def _synthesise(
    research_results: list[ResearcherOutput | None],
) -> str:
    """Compose narrative from researcher outputs.

    Falls back to a concatenation of summaries if the Synthesiser agent
    is not available yet (daughter #2).
    """
    synth_cls = _try_import_researcher(
        "vellum.agents.synthesiser", "Synthesiser"
    )

    available = [r for r in research_results if r is not None]

    if synth_cls is not None:
        try:
            synth = synth_cls()  # type: ignore[operator]
            return await synth.compose(available)  # type: ignore[union-attr]
        except Exception:
            logger.exception("Synthesiser failed — falling back to summary concat")

    # Fallback: stitch available summaries together
    if not available:
        return "No research data available today."

    parts: list[str] = []
    source_labels = {"stripe": "Stripe", "calendar": "Calendar", "searxng": "SearXNG"}
    seen_sources = {r.source for r in available}

    for r in available:
        parts.append(f"**{source_labels.get(r.source, r.source)}:** {r.summary}")

    for label_key, label_name in source_labels.items():
        if label_key not in seen_sources:
            parts.append(f"**{label_name}:** {_SECTION_UNAVAILABLE}")

    return "\n\n".join(parts)


def _create_sheet(tenant_id: str, date: datetime) -> Sheet:
    """Create a new Brief sheet for the given tenant and date."""
    title = f"Morning Brief — {date.strftime('%A %d %B %Y')}"
    meta = SheetMeta(
        tenant_id=tenant_id,
        title=title,
        mode="brief",
        created_by="Devon-cron/morning_brief",
    )
    return Sheet(meta=meta)


def _write_entry(sheet: Sheet, content: str, author: str = "synthesiser") -> SheetEntry:
    """Append an entry to the sheet, maintaining the hash chain."""
    prev_hash = sheet.latest_hash
    entry = SheetEntry(
        sheet_id=sheet.meta.id,
        author=author,
        content=content,
        prev_hash=prev_hash,
        entry_type="agent_write",
    )
    sheet.entries.append(entry)
    sheet.latest_hash = entry.entry_hash
    return entry


def _generate_phone_bound_token(
    sheet_id: str,
    phone_number: str,
    secret: str,
) -> ShareToken:
    """Generate a phone-bound share token.

    Uses HMAC-SHA256 to create a deterministic but opaque token_id
    bound to the sheet and phone number. When the full auth module is
    available (daughter #1), this should be replaced with JWT issuance.
    """
    raw = hmac.new(
        secret.encode(),
        f"{sheet_id}:{phone_number}".encode(),
        hashlib.sha256,
    ).hexdigest()

    return ShareToken(
        token_id=raw,
        sheet_id=sheet_id,
        role="read",
        bound_to=phone_number,
    )


# ---------------------------------------------------------------------------
# Main entry point
# ---------------------------------------------------------------------------


async def run_morning_brief(tenant_id: str = "jesmond") -> bool:
    """Execute the full morning brief pipeline.

    Returns ``True`` if the brief was generated and delivered,
    ``False`` if delivery failed (brief may still be generated).
    """
    phone = os.environ.get("JESMOND_BOB_PHONE")
    base_url = os.environ.get("BRIEF_BASE_URL", "https://api.amplifiedpartners.ai")
    token_secret = os.environ.get("BRIEF_TOKEN_SECRET", str(uuid4()))

    if not phone:
        logger.error("JESMOND_BOB_PHONE not set — cannot deliver brief")
        return False

    now = datetime.now(timezone.utc)
    logger.info("Starting morning brief for tenant=%s date=%s", tenant_id, now.date())

    # 1. Create sheet
    sheet = _create_sheet(tenant_id, now)
    logger.info("Created sheet %s: %s", sheet.meta.id, sheet.meta.title)

    # 2. Gather research
    results = await _gather_research(tenant_id, now)

    # 3. Synthesise narrative
    narrative = await _synthesise(results)

    # 4. Write entries to sheet
    _write_entry(sheet, narrative, author="synthesiser")

    available_count = sum(1 for r in results if r is not None)
    logger.info(
        "Brief composed: %d/%d researchers returned data, %d entries",
        available_count,
        len(results),
        len(sheet.entries),
    )

    # 5. Generate phone-bound token and share URL
    token = _generate_phone_bound_token(sheet.meta.id, phone, token_secret)
    share_url = generate_share_url(base_url, sheet.meta.id, token.token_id)

    # 6. Deliver via iMessage
    message = f"Good morning! Your brief for {now.strftime('%A %d %B')} is ready."
    delivered = await send_brief_link(phone, share_url, message)

    if delivered:
        logger.info("Brief delivered to %s via iMessage", phone)
    else:
        logger.error("Brief delivery FAILED for %s — sheet %s still available at %s",
                      phone, sheet.meta.id, share_url)

    return delivered


# ---------------------------------------------------------------------------
# APScheduler runner — standalone execution with scheduled triggers
# ---------------------------------------------------------------------------


def _run_scheduler() -> None:
    """Start an APScheduler loop that fires the brief at 06:25 and delivers at 06:30.

    The generate step runs at 06:25 UTC; the iMessage push is built into
    ``run_morning_brief`` (it sends as soon as synthesis completes, which
    should land around 06:30 given ~5 min of researcher + LLM work).
    """
    from apscheduler.schedulers.asyncio import AsyncIOScheduler
    from apscheduler.triggers.cron import CronTrigger

    scheduler = AsyncIOScheduler()
    scheduler.add_job(
        run_morning_brief,
        trigger=CronTrigger(hour=6, minute=25, timezone="UTC"),
        id="morning_brief",
        name="Morning Brief — generate + deliver",
        replace_existing=True,
    )

    logger.info("APScheduler started — morning brief at 06:25 UTC daily")
    scheduler.start()

    loop = asyncio.get_event_loop()
    try:
        loop.run_forever()
    except (KeyboardInterrupt, SystemExit):
        logger.info("Scheduler shutting down")
        scheduler.shutdown()


if __name__ == "__main__":
    import sys

    logging.basicConfig(
        level=logging.INFO,
        format="%(asctime)s [%(levelname)s] %(name)s: %(message)s",
    )

    if "--schedule" in sys.argv:
        _run_scheduler()
    else:
        # Manual one-shot execution
        tenant = sys.argv[1] if len(sys.argv) > 1 else "jesmond"
        result = asyncio.run(run_morning_brief(tenant))
        sys.exit(0 if result else 1)

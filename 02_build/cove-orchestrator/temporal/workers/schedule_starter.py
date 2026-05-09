"""Register the APDS 10-minute Temporal Schedule (AMP-158).

Idempotent — safe to call on every worker boot. If the schedule already
exists, this is a no-op. If Temporal is unreachable, the error is logged
and the worker continues without the schedule.

Usage (called from workers/main.py on startup):

    await register_apds_schedule(client)

Architect directive: ``*/10 * * * *`` cadence, hardcoded.

Signed-by: Devon-ad8f | 2026-05-09 | devin-ad8f2a94b2ca4d9a8e7690fcec0c11bb
"""

from __future__ import annotations

import logging

from temporalio.client import (
    Client,
    Schedule,
    ScheduleActionStartWorkflow,
    ScheduleSpec,
)

from temporal.workflows.apds_ingestion_workflow import (
    APDS_CRON_SCHEDULE,
    APDS_SCHEDULE_ID,
    APDS_TASK_QUEUE,
    APDS_WORKFLOW_ID_PREFIX,
    APDSIngestionInput,
    APDSIngestionWorkflow,
)

log = logging.getLogger("cove.schedule")


async def register_apds_schedule(client: Client) -> None:
    """Create (or verify) the APDS 10-minute ingestion schedule.

    Uses ``ScheduleSpec.cron_expressions`` with the architect-mandated
    cron string ``*/10 * * * *``.  The schedule launches
    ``APDSIngestionWorkflow`` with default inputs on the shared
    ``cove-build-queue`` task queue.

    Idempotent: if the schedule already exists Temporal returns
    ``ALREADY_EXISTS`` — we catch that and log it.
    """
    try:
        handle = client.get_schedule_handle(APDS_SCHEDULE_ID)
        desc = await handle.describe()
        log.info(
            "APDS schedule '%s' already registered (next: %s)",
            APDS_SCHEDULE_ID,
            desc.info.next_action_times[:1]
            if desc.info.next_action_times
            else "unknown",
        )
        return
    except Exception:
        pass

    try:
        await client.create_schedule(
            APDS_SCHEDULE_ID,
            Schedule(
                action=ScheduleActionStartWorkflow(
                    APDSIngestionWorkflow.run,
                    arg=APDSIngestionInput(),
                    id=APDS_WORKFLOW_ID_PREFIX,
                    task_queue=APDS_TASK_QUEUE,
                ),
                spec=ScheduleSpec(
                    cron_expressions=[APDS_CRON_SCHEDULE],
                ),
            ),
        )
        log.info(
            "APDS schedule '%s' created: cron=%s queue=%s",
            APDS_SCHEDULE_ID,
            APDS_CRON_SCHEDULE,
            APDS_TASK_QUEUE,
        )
    except Exception as e:
        error_str = str(e)
        if "ALREADY_EXISTS" in error_str or "already exists" in error_str.lower():
            log.info("APDS schedule '%s' already exists (race-safe)", APDS_SCHEDULE_ID)
        else:
            log.error("Failed to register APDS schedule (AMP-282 blocker?): %s", e)

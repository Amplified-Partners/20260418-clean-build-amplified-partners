"""
Temporal Worker — Main Entry Point
===================================
Registers all workflows and activities, then starts the worker.
Run: python -m temporal.workers.main
"""

import asyncio
import os
import logging

from temporalio.client import Client
from temporalio.worker import Worker

from temporal.workflows.build_workflow import ProjectBuildWorkflow
from temporal.workflows.polish_gate_workflow import PolishGateWorkflow
from temporal.workflows.apds_ingestion_workflow import APDSIngestionWorkflow
from temporal.activities.agent_activities import (
    run_agent,
    request_approval,
    check_approval_status,
    update_task_status,
    log_agent_run,
)
from temporal.activities.polish_activities import (
    screenshot_pr_preview,
    uiclip_score,
    rubric_score,
    evaluate_polish_gate,
    post_pr_comment,
    langfuse_log_polish_score,
)
from temporal.activities.ingestion_activities import (
    run_unified_ingestion,
    run_pudding_extraction,
    write_to_memory_stores,
    log_pipeline_run,
)
from temporal.workers.schedule_starter import register_apds_schedule

TEMPORAL_ADDRESS = os.getenv("TEMPORAL_ADDRESS", "localhost:7233")
TASK_QUEUE = "cove-build-queue"

logging.basicConfig(level=logging.INFO, format="%(asctime)s [worker] %(message)s")
log = logging.getLogger("cove_worker")


async def main():
    log.info(f"Connecting to Temporal at {TEMPORAL_ADDRESS}")
    client = await Client.connect(TEMPORAL_ADDRESS)

    log.info(f"Starting worker on queue: {TASK_QUEUE}")
    # Register the APDS 10-min schedule (AMP-158, idempotent)
    await register_apds_schedule(client)

    worker = Worker(
        client,
        task_queue=TASK_QUEUE,
        workflows=[ProjectBuildWorkflow, PolishGateWorkflow, APDSIngestionWorkflow],
        activities=[
            run_agent,
            request_approval,
            check_approval_status,
            update_task_status,
            log_agent_run,
            screenshot_pr_preview,
            uiclip_score,
            rubric_score,
            evaluate_polish_gate,
            post_pr_comment,
            langfuse_log_polish_score,
            run_unified_ingestion,
            run_pudding_extraction,
            write_to_memory_stores,
            log_pipeline_run,
        ],
    )
    await worker.run()


if __name__ == "__main__":
    asyncio.run(main())

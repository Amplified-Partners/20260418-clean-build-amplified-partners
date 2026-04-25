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
from temporal.activities.agent_activities import (
    run_agent,
    request_approval,
    check_approval_status,
    update_task_status,
    log_agent_run,
)

TEMPORAL_ADDRESS = os.getenv("TEMPORAL_ADDRESS", "localhost:7233")
TASK_QUEUE = "cove-build-queue"

logging.basicConfig(level=logging.INFO, format="%(asctime)s [worker] %(message)s")
log = logging.getLogger("cove_worker")


async def main():
    log.info(f"Connecting to Temporal at {TEMPORAL_ADDRESS}")
    client = await Client.connect(TEMPORAL_ADDRESS)

    log.info(f"Starting worker on queue: {TASK_QUEUE}")
    worker = Worker(
        client,
        task_queue=TASK_QUEUE,
        workflows=[ProjectBuildWorkflow],
        activities=[
            run_agent,
            request_approval,
            check_approval_status,
            update_task_status,
            log_agent_run,
        ],
    )
    await worker.run()


if __name__ == "__main__":
    asyncio.run(main())

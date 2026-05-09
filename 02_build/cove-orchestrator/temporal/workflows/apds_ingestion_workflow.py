"""APDSIngestionWorkflow — 10-minute scheduled APDS pipeline (AMP-158).

Architect directive (Ewan Bramley): APDS ingestion pipeline runs on a
**10-minute cadence** (``*/10 * * * *``). This schedule is hardcoded here
and registered on worker boot.

Pipeline stages (sequential):

    1. run_unified_ingestion   — dedup raw files into store_b_clean
    2. run_pudding_extraction  — PUDDING taxonomy labelling via Claude Haiku
    3. write_to_memory_stores  — upsert into amplified_brain PostgreSQL
    4. log_pipeline_run        — observability record to pipeline_runs table

The workflow is designed to be started by a Temporal Schedule with a
10-minute interval. The ``APDSScheduleStarter`` helper registers that
schedule on first boot; subsequent worker restarts are idempotent.

Signed-by: Devon-ad8f | 2026-05-09 | devin-ad8f2a94b2ca4d9a8e7690fcec0c11bb
"""

from __future__ import annotations

from dataclasses import dataclass
from datetime import timedelta
from typing import Optional

from temporalio import workflow
from temporalio.common import RetryPolicy

with workflow.unsafe.imports_passed_through():
    from temporal.activities.ingestion_activities import (
        IngestionInput,
        PuddingInput,
        MemoryStoreInput,
        PipelineRun,
        run_unified_ingestion,
        run_pudding_extraction,
        write_to_memory_stores,
        log_pipeline_run,
    )

# ── Schedule constants (Architect directive, AMP-158) ─────────────────
# Cron: */10 * * * *  — every 10 minutes, on the minute.
APDS_CRON_SCHEDULE = "*/10 * * * *"
APDS_SCHEDULE_ID = "apds-ingestion-10min"
APDS_TASK_QUEUE = "cove-build-queue"
APDS_WORKFLOW_ID_PREFIX = "apds-ingestion"


@dataclass
class APDSIngestionInput:
    """Optional overrides for a single pipeline run."""

    full_rebuild: bool = False
    max_ingestion_workers: int = 8
    max_pudding_workers: int = 4
    pudding_limit: int = 0


@dataclass
class APDSIngestionResult:
    run_id: str
    success: bool
    ingestion_new: int = 0
    ingestion_total: int = 0
    pudding_labelled: int = 0
    memory_vectors: int = 0
    memory_entities: int = 0
    error: Optional[str] = None


@workflow.defn(name="apds_ingestion")
class APDSIngestionWorkflow:
    """Full APDS pipeline: ingest -> label -> store -> log.

    Runs on a 10-minute Temporal Schedule (``*/10 * * * *``).
    Each stage is a separate Temporal activity with its own retry policy.
    If ingestion finds zero new files, PUDDING extraction and memory
    writes are skipped (idempotent no-op).
    """

    @workflow.run
    async def run(self, input: APDSIngestionInput) -> APDSIngestionResult:
        run_id = f"apds-{workflow.info().workflow_id}-{workflow.now().strftime('%Y%m%dT%H%M')}"

        retry = RetryPolicy(
            initial_interval=timedelta(seconds=10),
            backoff_coefficient=2.0,
            maximum_interval=timedelta(minutes=5),
            maximum_attempts=3,
        )

        pipeline = PipelineRun(
            run_id=run_id,
            started_at=workflow.now().isoformat(),
        )

        # ── Stage 1: Unified Ingestion ────────────────────────────────
        try:
            ingestion = await workflow.execute_activity(
                run_unified_ingestion,
                args=[
                    IngestionInput(
                        full_rebuild=input.full_rebuild,
                        max_workers=input.max_ingestion_workers,
                    )
                ],
                start_to_close_timeout=timedelta(minutes=15),
                retry_policy=retry,
            )
            pipeline.ingestion = ingestion
        except Exception as e:
            pipeline.status = "failed_ingestion"
            pipeline.completed_at = workflow.now().isoformat()
            await self._log_run(pipeline)
            return APDSIngestionResult(
                run_id=run_id, success=False, error=f"Ingestion failed: {e}"
            )

        if not ingestion.success:
            pipeline.status = "failed_ingestion"
            pipeline.completed_at = workflow.now().isoformat()
            await self._log_run(pipeline)
            return APDSIngestionResult(
                run_id=run_id,
                success=False,
                error=ingestion.error or "Ingestion returned success=False",
            )

        # Short-circuit: no new files means nothing to label or store.
        if ingestion.new_files == 0:
            pipeline.status = "completed_noop"
            pipeline.completed_at = workflow.now().isoformat()
            await self._log_run(pipeline)
            workflow.logger.info("No new files — skipping PUDDING + memory store")
            return APDSIngestionResult(
                run_id=run_id,
                success=True,
                ingestion_new=0,
                ingestion_total=ingestion.total_unique,
            )

        # ── Stage 2: PUDDING Extraction ───────────────────────────────
        try:
            pudding = await workflow.execute_activity(
                run_pudding_extraction,
                args=[
                    PuddingInput(
                        target_dir=ingestion.clean_archive,
                        max_workers=input.max_pudding_workers,
                        limit=input.pudding_limit,
                    )
                ],
                start_to_close_timeout=timedelta(minutes=30),
                retry_policy=retry,
            )
            pipeline.pudding = pudding
        except Exception as e:
            pipeline.status = "failed_pudding"
            pipeline.completed_at = workflow.now().isoformat()
            await self._log_run(pipeline)
            return APDSIngestionResult(
                run_id=run_id,
                success=False,
                ingestion_new=ingestion.new_files,
                ingestion_total=ingestion.total_unique,
                error=f"PUDDING extraction failed: {e}",
            )

        # ── Stage 3: Memory Store Write ───────────────────────────────
        try:
            memory = await workflow.execute_activity(
                write_to_memory_stores,
                args=[
                    MemoryStoreInput(
                        source_dir=ingestion.clean_archive,
                    )
                ],
                start_to_close_timeout=timedelta(minutes=15),
                retry_policy=retry,
            )
            pipeline.memory_store = memory
        except Exception as e:
            pipeline.status = "failed_memory"
            pipeline.completed_at = workflow.now().isoformat()
            await self._log_run(pipeline)
            return APDSIngestionResult(
                run_id=run_id,
                success=False,
                ingestion_new=ingestion.new_files,
                ingestion_total=ingestion.total_unique,
                pudding_labelled=pudding.labelled if pudding else 0,
                error=f"Memory store write failed: {e}",
            )

        # ── Stage 4: Log & Return ─────────────────────────────────────
        pipeline.status = "completed"
        pipeline.completed_at = workflow.now().isoformat()
        await self._log_run(pipeline)

        return APDSIngestionResult(
            run_id=run_id,
            success=True,
            ingestion_new=ingestion.new_files,
            ingestion_total=ingestion.total_unique,
            pudding_labelled=pudding.labelled if pudding else 0,
            memory_vectors=memory.pg_vectors if memory else 0,
            memory_entities=memory.pg_entities if memory else 0,
        )

    async def _log_run(self, pipeline: PipelineRun) -> None:
        """Best-effort observability — log failures must not crash the workflow."""
        try:
            await workflow.execute_activity(
                log_pipeline_run,
                args=[pipeline],
                start_to_close_timeout=timedelta(seconds=30),
            )
        except Exception as e:
            workflow.logger.warning("log_pipeline_run failed: %s", e)

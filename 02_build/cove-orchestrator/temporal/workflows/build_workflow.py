"""
ProjectBuildWorkflow — Master Orchestrator (COV-263)
====================================================
This is THE workflow. Every build task flows through here.

Pattern: Temporal orchestrates → Activities call agents → Agents use MCP tools
Temporal handles: retries, timeouts, state, visibility, failure recovery
We handle: agent routing, approval gates, cost tracking
"""

from datetime import timedelta
from dataclasses import dataclass
from typing import Optional

from temporalio import workflow
from temporalio.common import RetryPolicy

with workflow.unsafe.imports_passed_through():
    from temporal.activities.agent_activities import (
        run_agent,
        request_approval,
        check_approval_status,
        update_task_status,
        log_agent_run,
    )


@dataclass
class BuildTaskInput:
    task_id: str
    project_id: str
    linear_issue_id: str
    title: str
    description: str
    agent_role: str          # coder, security, enforcer
    model_tier: str          # cheap, medium, premium
    approval_tier: int       # 0-5
    branch_name: str
    depends_on: list[str]    # Task IDs
    max_retries: int = 3


@dataclass
class BuildTaskResult:
    task_id: str
    success: bool
    result: Optional[dict] = None
    error: Optional[str] = None
    cost_usd: float = 0.0
    tokens_used: int = 0


@workflow.defn
class ProjectBuildWorkflow:
    """
    Single task execution workflow.
    The orchestrator launches one of these per task.

    Flow:
    1. Update status → queued
    2. Wait for dependencies (if any)
    3. Run agent (coder/security/enforcer)
    4. If approval required → send notification → wait
    5. On approval → complete. On rejection → fail or retry.
    """

    @workflow.run
    async def run(self, input: BuildTaskInput) -> BuildTaskResult:
        retry = RetryPolicy(
            initial_interval=timedelta(seconds=10),
            backoff_coefficient=2.0,
            maximum_interval=timedelta(minutes=5),
            maximum_attempts=input.max_retries,
        )

        # 1. Mark task as queued
        await workflow.execute_activity(
            update_task_status,
            args=[input.task_id, "queued"],
            start_to_close_timeout=timedelta(seconds=30),
        )

        # 2. Wait for dependencies
        if input.depends_on:
            await workflow.wait_condition(
                lambda: self._deps_resolved,
                timeout=timedelta(hours=24),
            )

        # 3. Mark as running
        await workflow.execute_activity(
            update_task_status,
            args=[input.task_id, "running"],
            start_to_close_timeout=timedelta(seconds=30),
        )

        # 4. Run the agent
        try:
            agent_result = await workflow.execute_activity(
                run_agent,
                args=[{
                    "task_id": input.task_id,
                    "agent_role": input.agent_role,
                    "model_tier": input.model_tier,
                    "title": input.title,
                    "description": input.description,
                    "branch_name": input.branch_name,
                }],
                start_to_close_timeout=timedelta(minutes=30),
                retry_policy=retry,
            )
        except Exception as e:
            await workflow.execute_activity(
                update_task_status,
                args=[input.task_id, "failed"],
                start_to_close_timeout=timedelta(seconds=30),
            )
            return BuildTaskResult(
                task_id=input.task_id,
                success=False,
                error=str(e),
            )

        # 5. Log the run
        await workflow.execute_activity(
            log_agent_run,
            args=[agent_result],
            start_to_close_timeout=timedelta(seconds=30),
        )

        # 6. Approval gate (if tier > 0)
        if input.approval_tier > 0:
            await workflow.execute_activity(
                update_task_status,
                args=[input.task_id, "awaiting_approval"],
                start_to_close_timeout=timedelta(seconds=30),
            )

            approval_id = await workflow.execute_activity(
                request_approval,
                args=[{
                    "task_id": input.task_id,
                    "title": input.title,
                    "tier": input.approval_tier,
                    "agent_role": input.agent_role,
                    "diff_summary": getattr(agent_result, "output", "")[:500] + "...",  # Preview of the output
                }],
                start_to_close_timeout=timedelta(minutes=2),
            )

            # Poll for approval (Temporal handles the waiting efficiently)
            approved = False
            for _ in range(360):  # Up to 6 hours of checking
                await workflow.sleep(timedelta(minutes=1))
                status = await workflow.execute_activity(
                    check_approval_status,
                    args=[approval_id],
                    start_to_close_timeout=timedelta(seconds=30),
                )
                if status == "approved":
                    approved = True
                    break
                elif status == "rejected":
                    break

            if not approved:
                await workflow.execute_activity(
                    update_task_status,
                    args=[input.task_id, "rejected"],
                    start_to_close_timeout=timedelta(seconds=30),
                )
                return BuildTaskResult(
                    task_id=input.task_id,
                    success=False,
                    error="Approval rejected or timed out",
                )

        # 7. Complete
        await workflow.execute_activity(
            update_task_status,
            args=[input.task_id, "completed"],
            start_to_close_timeout=timedelta(seconds=30),
        )

        return BuildTaskResult(
            task_id=input.task_id,
            success=True,
            result={"output": getattr(agent_result, "output", "")},
            cost_usd=0.0,  # Could be calculated from tokens later
            tokens_used=getattr(agent_result, "tokens_in", 0) + getattr(agent_result, "tokens_out", 0),
        )

    # ─── Signals ─────────────────────────────────────────────────────
    _deps_resolved: bool = False

    @workflow.signal
    async def dependencies_resolved(self) -> None:
        """Called by parent orchestrator when all deps are done."""
        self._deps_resolved = True

    @workflow.signal
    async def cancel_task(self) -> None:
        """Emergency stop."""
        raise workflow.CancelledError("Task cancelled via signal")

"""PolishGateWorkflow — Cove's per-PR Visual Polish merge gate (AMP-73).

Triggered by GitHub Actions on every PR open / synchronize for the gated
UI / marketing repos:

    amplified-site, the-amplified-method, amplified-website, crm,
    marketing-engine

Flow per PR:

    1. screenshot_pr_preview(preview_url)    → desktop + mobile PNGs
    2. uiclip_score + rubric_score in parallel against the desktop shot
    3. evaluate_polish_gate                   → run_pipeline, decide pass/fail
    4. post_pr_comment(summary)               → human-readable report
    5. langfuse_log_polish_score              → trend tracking for Kaizen

The gate fails if composite < threshold OR any error-severity hard check
failed. The workflow's exit code is the GitHub Action's gate signal.

Devon-29bf | 2026-05-04 | AMP-73 wire visual-polish-system into Cove
"""

from __future__ import annotations

from dataclasses import dataclass, field
from datetime import timedelta
from typing import Optional

from temporalio import workflow
from temporalio.common import RetryPolicy

with workflow.unsafe.imports_passed_through():
    from temporal.activities.polish_activities import (
        ScreenshotInput,
        UIClipInput,
        RubricScoreInput,
        GateEvaluationInput,
        PRCommentInput,
        LangfusePolishInput,
        screenshot_pr_preview,
        uiclip_score,
        rubric_score,
        evaluate_polish_gate,
        post_pr_comment,
        langfuse_log_polish_score,
    )


@dataclass
class PolishGateInput:
    pr_id: str                 # 'owner/repo#number', e.g. 'Amplified-Partners/amplified-site#42'
    pr_url: str                # full GitHub PR URL — for trace metadata
    preview_url: str           # deployed preview to screenshot
    rubric_path: str = "/opt/visual-polish-system/principles/references/rubric.json"
    rules_path: str = "/opt/visual-polish-system/principles/rules/core.rules.json"
    references_dir: str = ""
    threshold: float = 0.65
    hard_check_results: dict[str, bool] = field(default_factory=dict)


@dataclass
class PolishGateResult:
    pr_id: str
    passed: bool
    composite: float
    threshold: float
    summary: str
    error: Optional[str] = None


@workflow.defn(name="polish_gate")
class PolishGateWorkflow:
    @workflow.run
    async def run(self, input: PolishGateInput) -> PolishGateResult:
        retry = RetryPolicy(
            initial_interval=timedelta(seconds=5),
            maximum_attempts=3,
            backoff_coefficient=2.0,
        )

        # Critical path — these activities determine the gate decision.
        # Any failure here aborts and returns passed=False with the error.
        try:
            shots = await workflow.execute_activity(
                screenshot_pr_preview,
                args=[
                    ScreenshotInput(
                        pr_id=input.pr_id,
                        pr_url=input.pr_url,
                        preview_url=input.preview_url,
                    )
                ],
                start_to_close_timeout=timedelta(minutes=2),
                retry_policy=retry,
            )
            target = shots.paths[0]  # desktop shot drives the gate

            uiclip_handle = workflow.execute_activity(
                uiclip_score,
                args=[UIClipInput(pr_id=input.pr_id, screenshot_path=target)],
                start_to_close_timeout=timedelta(minutes=2),
                retry_policy=retry,
            )
            rubric_handle = workflow.execute_activity(
                rubric_score,
                args=[
                    RubricScoreInput(
                        pr_id=input.pr_id,
                        screenshot_path=target,
                        rubric_path=input.rubric_path,
                        references_dir=input.references_dir,
                    )
                ],
                start_to_close_timeout=timedelta(minutes=3),
                retry_policy=retry,
            )
            uiclip_res, rubric_res = await uiclip_handle, await rubric_handle

            gate = await workflow.execute_activity(
                evaluate_polish_gate,
                args=[
                    GateEvaluationInput(
                        pr_id=input.pr_id,
                        rubric_path=input.rubric_path,
                        rules_path=input.rules_path,
                        dimension_scores=rubric_res.dimension_scores,
                        uiclip_score=uiclip_res.score,
                        hard_check_results=input.hard_check_results,
                        threshold=input.threshold,
                    )
                ],
                start_to_close_timeout=timedelta(seconds=30),
            )
        except Exception as e:  # noqa: BLE001
            return PolishGateResult(
                pr_id=input.pr_id,
                passed=False,
                composite=0.0,
                threshold=input.threshold,
                summary="",
                error=str(e),
            )

        # Side effects — PR comment + Langfuse trace. These are observability
        # / UX, NOT part of the gate decision: a Langfuse outage or a flaky
        # GitHub API call must NOT cause the workflow to report passed=False
        # for an otherwise-passing PR.
        comment_body = _format_pr_comment(gate.summary, gate.passed, input.pr_url)
        try:
            await workflow.execute_activity(
                post_pr_comment,
                args=[PRCommentInput(pr_id=input.pr_id, body=comment_body)],
                start_to_close_timeout=timedelta(seconds=30),
                retry_policy=retry,
            )
        except Exception as e:  # noqa: BLE001
            workflow.logger.warning("post_pr_comment failed pr_id=%s: %s", input.pr_id, e)

        try:
            await workflow.execute_activity(
                langfuse_log_polish_score,
                args=[
                    LangfusePolishInput(
                        pr_id=input.pr_id,
                        pr_url=input.pr_url,
                        composite=gate.composite,
                        rubric_normalised=gate.rubric_normalised,
                        uiclip_score=gate.uiclip_score,
                        threshold=gate.threshold,
                        passed=gate.passed,
                        dimension_scores=rubric_res.dimension_scores,
                        summary=gate.summary,
                    )
                ],
                start_to_close_timeout=timedelta(seconds=30),
                retry_policy=retry,
            )
        except Exception as e:  # noqa: BLE001
            workflow.logger.warning("langfuse_log_polish_score failed pr_id=%s: %s", input.pr_id, e)

        return PolishGateResult(
            pr_id=input.pr_id,
            passed=gate.passed,
            composite=gate.composite,
            threshold=gate.threshold,
            summary=gate.summary,
        )


def _format_pr_comment(summary: str, passed: bool, pr_url: str) -> str:
    badge = "✅ **Visual Polish: PASS**" if passed else "❌ **Visual Polish: FAIL**"
    return (
        f"{badge}\n\n"
        f"```\n{summary}\n```\n\n"
        f"_Posted by Cove `polish_gate` workflow for [{pr_url}]({pr_url}) — see "
        f"[AMP-73](https://linear.app/amplifiedpartners/issue/AMP-73) for context._"
    )

"""End-to-end test for `PolishGateWorkflow` using Temporal's test environment.

Every activity is replaced with an in-process mock so the workflow itself is
exercised without touching LiteLLM, Playwright, GitHub, or Langfuse. Verifies:

- Pass path: high uiclip + good rubric ⇒ result.passed=True, comment + Langfuse called
- Fail path: low uiclip + low rubric  ⇒ result.passed=False, comment posted, error=None
- Threshold edge: composite < threshold ⇒ failed even when hard checks pass

Run with:  pytest tests/test_polish_gate_workflow.py
"""

from __future__ import annotations

import uuid
from typing import Any
from unittest.mock import AsyncMock

import pytest

from temporalio.testing import WorkflowEnvironment
from temporalio.worker import Worker

from temporal.activities.polish_activities import (
    GateEvaluationInput,
    GateEvaluationResult,
    LangfusePolishInput,
    PRCommentInput,
    RubricScoreInput,
    RubricScoreResult,
    ScreenshotInput,
    ScreenshotResult,
    UIClipInput,
    UIClipResult,
)
from temporal.workflows.polish_gate_workflow import (
    PolishGateInput,
    PolishGateResult,
    PolishGateWorkflow,
)


_GATED_PR = "Amplified-Partners/amplified-site#42"


# ─── Mock activity factories ────────────────────────────────────────────────


def _make_mocks(
    *,
    uiclip: float,
    dim_score: int,
    hard_pass: bool,
    threshold: float = 0.65,
    comment_raises: bool = False,
    langfuse_raises: bool = False,
) -> dict[str, Any]:
    """Return a dict {activity_name: AsyncMock} with realistic return values.

    If comment_raises / langfuse_raises is True, the corresponding side-effect
    activity will raise — used to verify that side-effect failures do not
    flip the gate decision.
    """
    composite = uiclip * 0.4 + (dim_score - 1) / 9.0 * 0.6
    passed = hard_pass and composite >= threshold

    async def _shot(input: ScreenshotInput) -> ScreenshotResult:
        return ScreenshotResult(
            pr_id=input.pr_id, paths=["/tmp/d.png", "/tmp/m.png"], captured_at="t"
        )

    async def _ui(input: UIClipInput) -> UIClipResult:
        return UIClipResult(
            pr_id=input.pr_id,
            screenshot_path=input.screenshot_path,
            score=uiclip,
            model_used="mock",
            raw_output="{}",
        )

    async def _rub(input: RubricScoreInput) -> RubricScoreResult:
        return RubricScoreResult(
            pr_id=input.pr_id,
            screenshot_path=input.screenshot_path,
            dimension_scores={"calm_surface": dim_score},
            rationales={"calm_surface": "mock"},
            model_used="mock",
        )

    async def _eval(input: GateEvaluationInput) -> GateEvaluationResult:
        return GateEvaluationResult(
            pr_id=input.pr_id,
            passed=passed,
            composite=composite,
            rubric_normalised=(dim_score - 1) / 9.0,
            uiclip_score=uiclip,
            threshold=input.threshold,
            hard_checks_pass=hard_pass,
            summary=f"composite={composite:.4f} threshold={input.threshold:.4f}",
        )

    comment_mock = AsyncMock(
        side_effect=RuntimeError("github 503") if comment_raises else None,
        return_value=True,
    )
    langfuse_mock = AsyncMock(
        side_effect=RuntimeError("langfuse down") if langfuse_raises else None,
        return_value=True,
    )

    async def _comment(input: PRCommentInput) -> bool:
        return await comment_mock(input)

    async def _lang(input: LangfusePolishInput) -> bool:
        return await langfuse_mock(input)

    # Wrap concrete async functions as Temporal activity definitions with the
    # same names the workflow expects.
    from temporalio import activity

    @activity.defn(name="screenshot_pr_preview")
    async def screenshot_pr_preview(input: ScreenshotInput) -> ScreenshotResult:
        return await _shot(input)

    @activity.defn(name="uiclip_score")
    async def uiclip_score(input: UIClipInput) -> UIClipResult:
        return await _ui(input)

    @activity.defn(name="rubric_score")
    async def rubric_score(input: RubricScoreInput) -> RubricScoreResult:
        return await _rub(input)

    @activity.defn(name="evaluate_polish_gate")
    async def evaluate_polish_gate(input: GateEvaluationInput) -> GateEvaluationResult:
        return await _eval(input)

    @activity.defn(name="post_pr_comment")
    async def post_pr_comment(input: PRCommentInput) -> bool:
        return await _comment(input)

    @activity.defn(name="langfuse_log_polish_score")
    async def langfuse_log_polish_score(input: LangfusePolishInput) -> bool:
        return await _lang(input)

    return {
        "activities": [
            screenshot_pr_preview,
            uiclip_score,
            rubric_score,
            evaluate_polish_gate,
            post_pr_comment,
            langfuse_log_polish_score,
        ],
        "comment_mock": comment_mock,
        "langfuse_mock": langfuse_mock,
        "expected_passed": passed,
        "expected_composite": composite,
    }


async def _run_workflow(env: WorkflowEnvironment, mocks: dict[str, Any], threshold: float = 0.65) -> PolishGateResult:
    task_queue = f"polish-gate-test-{uuid.uuid4().hex[:8]}"
    async with Worker(
        env.client,
        task_queue=task_queue,
        workflows=[PolishGateWorkflow],
        activities=mocks["activities"],
    ):
        return await env.client.execute_workflow(
            PolishGateWorkflow.run,
            PolishGateInput(
                pr_id=_GATED_PR,
                pr_url=f"https://github.com/{_GATED_PR.replace('#', '/pull/')}",
                preview_url="https://preview.example/pr-42",
                threshold=threshold,
            ),
            id=f"wf-{uuid.uuid4().hex[:8]}",
            task_queue=task_queue,
        )


# ─── Tests ─────────────────────────────────────────────────────────────────


@pytest.mark.asyncio
async def test_polish_gate_pass_path() -> None:
    async with await WorkflowEnvironment.start_time_skipping() as env:
        mocks = _make_mocks(uiclip=0.85, dim_score=9, hard_pass=True, threshold=0.65)
        result = await _run_workflow(env, mocks)

    assert result.passed is True
    assert result.composite == pytest.approx(mocks["expected_composite"])
    assert result.error is None
    assert mocks["comment_mock"].await_count == 1
    posted: PRCommentInput = mocks["comment_mock"].await_args.args[0]
    assert "Visual Polish: PASS" in posted.body
    # Comment must back-link to the PR being scored so reviewers can navigate.
    assert f"https://github.com/{_GATED_PR.replace('#', '/pull/')}" in posted.body
    assert mocks["langfuse_mock"].await_count == 1


@pytest.mark.asyncio
async def test_polish_gate_fail_path_low_quality() -> None:
    async with await WorkflowEnvironment.start_time_skipping() as env:
        mocks = _make_mocks(uiclip=0.2, dim_score=3, hard_pass=True, threshold=0.65)
        result = await _run_workflow(env, mocks)

    assert result.passed is False
    assert result.composite < 0.65
    posted: PRCommentInput = mocks["comment_mock"].await_args.args[0]
    assert "Visual Polish: FAIL" in posted.body


@pytest.mark.asyncio
async def test_polish_gate_fail_path_hard_check() -> None:
    async with await WorkflowEnvironment.start_time_skipping() as env:
        # High composite, but hard checks failed ⇒ gate must still fail.
        mocks = _make_mocks(uiclip=0.95, dim_score=10, hard_pass=False, threshold=0.65)
        result = await _run_workflow(env, mocks)

    assert result.passed is False
    posted: PRCommentInput = mocks["comment_mock"].await_args.args[0]
    assert "Visual Polish: FAIL" in posted.body


@pytest.mark.asyncio
async def test_side_effect_failures_do_not_flip_gate_decision() -> None:
    """A passing PR must remain passing even if comment + Langfuse both fail.

    Regression: previously the workflow's catch-all `except Exception`
    converted any side-effect failure into passed=False (Devin Review
    finding BUG_..._0001).
    """
    async with await WorkflowEnvironment.start_time_skipping() as env:
        mocks = _make_mocks(
            uiclip=0.85,
            dim_score=9,
            hard_pass=True,
            threshold=0.65,
            comment_raises=True,
            langfuse_raises=True,
        )
        result = await _run_workflow(env, mocks)

    assert result.passed is True
    assert result.composite == pytest.approx(mocks["expected_composite"])
    assert result.error is None  # critical-path success ⇒ no error reported

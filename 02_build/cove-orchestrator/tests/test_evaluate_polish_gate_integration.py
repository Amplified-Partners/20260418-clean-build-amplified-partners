"""Integration test: `evaluate_polish_gate` against the real upstream
`scoring.engine.run_pipeline`. Skipped automatically when the upstream
package is not installed (e.g. lint-only CI environments).

Verifies the gate semantics agreed in AMP-73:
    passed  ⇔  composite >= threshold  AND  hard_checks_pass.
"""

from __future__ import annotations

import os
from pathlib import Path

import pytest

scoring = pytest.importorskip("scoring.engine", reason="visual-polish-system not installed")

from temporal.activities.polish_activities import (  # noqa: E402
    GateEvaluationInput,
    evaluate_polish_gate,
)


_VPS = os.getenv("VPS_ROOT", "/opt/visual-polish-system")
_RUBRIC = f"{_VPS}/principles/references/rubric.json"
_RULES = f"{_VPS}/principles/rules/core.rules.json"


_HIGH_QUALITY_SCORES = {
    "calm_surface": 9,
    "clear_hierarchy": 9,
    "typographic_rhythm": 8,
    "spatial_breathing": 9,
    "state_clarity": 8,
    "consistent_density": 8,
    "motion_purpose": 9,
    "component_cohesion": 9,
    "data_legibility": 8,
    "congruent_trust": 9,
}

_LOW_QUALITY_SCORES = {k: 2 for k in _HIGH_QUALITY_SCORES}


@pytest.mark.skipif(not Path(_RUBRIC).exists(), reason=f"rubric.json missing at {_RUBRIC}")
@pytest.mark.asyncio
async def test_high_quality_passes() -> None:
    out = await evaluate_polish_gate(
        GateEvaluationInput(
            pr_id="test/repo#1",
            rubric_path=_RUBRIC,
            rules_path=_RULES,
            dimension_scores=_HIGH_QUALITY_SCORES,
            uiclip_score=0.88,
            hard_check_results={},
            threshold=0.65,
        )
    )
    assert out.passed is True
    assert out.composite >= 0.65
    assert out.hard_checks_pass is True


@pytest.mark.skipif(not Path(_RUBRIC).exists(), reason=f"rubric.json missing at {_RUBRIC}")
@pytest.mark.asyncio
async def test_low_quality_fails() -> None:
    out = await evaluate_polish_gate(
        GateEvaluationInput(
            pr_id="test/repo#1",
            rubric_path=_RUBRIC,
            rules_path=_RULES,
            dimension_scores=_LOW_QUALITY_SCORES,
            uiclip_score=0.1,
            hard_check_results={},
            threshold=0.65,
        )
    )
    assert out.passed is False
    assert out.composite < 0.65


@pytest.mark.skipif(not Path(_RUBRIC).exists(), reason=f"rubric.json missing at {_RUBRIC}")
@pytest.mark.asyncio
async def test_hard_check_failure_fails_gate_even_when_composite_high() -> None:
    out = await evaluate_polish_gate(
        GateEvaluationInput(
            pr_id="test/repo#1",
            rubric_path=_RUBRIC,
            rules_path=_RULES,
            dimension_scores=_HIGH_QUALITY_SCORES,
            uiclip_score=0.95,
            hard_check_results={"TYP-001": False},  # error-severity rule fails
            threshold=0.65,
        )
    )
    assert out.passed is False
    assert out.hard_checks_pass is False

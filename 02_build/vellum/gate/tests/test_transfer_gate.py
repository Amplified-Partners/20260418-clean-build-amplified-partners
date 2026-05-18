"""Tests for the Vellum Pattern Transfer Gate.

Covers all decision paths:
- APPROVE_FOR_DC7_TEST (happy path)
- REJECT (4 distinct reasons)
- QUARANTINE (privacy gate)
- ESCALATE_FOR_REVIEW (evidence floor)

Plus invariant tests:
- effective_status is always <= STRUCTURED (gate ceiling)
- effective_status is always <= min(all input statuses)
- slot_match_score is always in [0.0, 1.0]
- reason_codes is never empty

Devon-b5dc | 2026-05-14
"""

from __future__ import annotations

import pytest

from vellum.gate.models import (
    AMPSScore,
    BusinessProcess,
    EpistemicStatus,
    ImprovementPattern,
    PuddingLabel,
    TrustState,
)
from vellum.gate.transfer import (
    calculate_amps_delta,
    calculate_slot_match_score,
    evaluate_bridge_candidate,
    min_status,
)


# ---------------------------------------------------------------------------
# Fixtures — building blocks for test cases.
# ---------------------------------------------------------------------------


def _label(what: str = "C", how: str = ">", scale: str = "3", time: str = "v") -> PuddingLabel:
    return PuddingLabel(what=what, how=how, scale=scale, time=time)


def _amps(score: float = 5.0, status: EpistemicStatus = EpistemicStatus.MEASURED, cycles: int = 12) -> AMPSScore:
    return AMPSScore(composite_score=score, epistemic_status=status, measured_cycles=cycles)


def _pattern(
    *,
    before: float = 3.0,
    after: float = 7.2,
    evidence: EpistemicStatus = EpistemicStatus.MEASURED,
    sensitive: bool = False,
    cross_client: bool = True,
    source_label: PuddingLabel | None = None,
) -> ImprovementPattern:
    return ImprovementPattern(
        pattern_id="pat-001",
        source_process_id="proc-src-001",
        source_client_namespace="client-alpha",
        description="SMS reminders reduce no-shows",
        source_label=source_label or _label(),
        before_amps=_amps(before),
        after_amps=_amps(after),
        evidence_status=evidence,
        contains_client_sensitive_detail=sensitive,
        allowed_for_cross_client_learning=cross_client,
    )


def _target(
    *,
    score: float = 2.0,
    label: PuddingLabel | None = None,
) -> BusinessProcess:
    return BusinessProcess(
        process_id="proc-tgt-001",
        client_namespace="client-beta",
        name="Table booking reminders",
        pudding_label=label or _label(),
        current_amps=_amps(score),
        bounded_or_creative="BOUNDED",
    )


# ---------------------------------------------------------------------------
# Unit tests: calculate_slot_match_score
# ---------------------------------------------------------------------------


class TestSlotMatchScore:
    def test_identical_labels_score_1(self):
        label = _label()
        assert calculate_slot_match_score(label, label) == 1.0

    def test_no_match_scores_0(self):
        a = _label("A", "B", "C", "D")
        b = _label("W", "X", "Y", "Z")
        assert calculate_slot_match_score(a, b) == 0.0

    def test_partial_match(self):
        a = _label("C", ">", "3", "v")
        b = _label("C", ">", "5", "x")
        assert calculate_slot_match_score(a, b) == 0.5

    def test_three_of_four(self):
        a = _label("C", ">", "3", "v")
        b = _label("C", ">", "3", "x")
        assert calculate_slot_match_score(a, b) == 0.75


# ---------------------------------------------------------------------------
# Unit tests: calculate_amps_delta
# ---------------------------------------------------------------------------


class TestAmpsDelta:
    def test_positive_delta(self):
        p = _pattern(before=3.0, after=7.2)
        assert calculate_amps_delta(p) == pytest.approx(4.2)

    def test_zero_delta(self):
        p = _pattern(before=5.0, after=5.0)
        assert calculate_amps_delta(p) == 0.0

    def test_negative_delta(self):
        p = _pattern(before=8.0, after=3.0)
        assert calculate_amps_delta(p) == pytest.approx(-5.0)


# ---------------------------------------------------------------------------
# Unit tests: min_status
# ---------------------------------------------------------------------------


class TestMinStatus:
    def test_all_same(self):
        assert min_status(EpistemicStatus.MEASURED, EpistemicStatus.MEASURED) == EpistemicStatus.MEASURED

    def test_min_wins(self):
        assert min_status(EpistemicStatus.PROVEN, EpistemicStatus.INTUITED) == EpistemicStatus.INTUITED

    def test_single(self):
        assert min_status(EpistemicStatus.STRUCTURED) == EpistemicStatus.STRUCTURED


# ---------------------------------------------------------------------------
# Integration tests: evaluate_bridge_candidate — APPROVE path
# ---------------------------------------------------------------------------


class TestApproveForDC7:
    def test_happy_path_approves(self):
        result = evaluate_bridge_candidate(_pattern(), _target())
        assert result.decision == "APPROVE_FOR_DC7_TEST"
        assert result.trust_state == TrustState.APPROVED_FOR_TEST
        assert "shape_similarity_sufficient" in result.reason_codes
        assert "source_pattern_has_positive_measured_delta" in result.reason_codes
        assert "target_has_improvement_headroom" in result.reason_codes
        assert "cross_client_learning_authorised" in result.reason_codes
        assert result.action is not None
        assert "DC-7" in result.action

    def test_approved_effective_status_capped_at_structured(self):
        # Even with all PROVEN inputs, gate itself is STRUCTURED
        pattern = _pattern(evidence=EpistemicStatus.PROVEN)
        pattern = pattern.model_copy(update={
            "before_amps": _amps(3.0, EpistemicStatus.PROVEN),
            "after_amps": _amps(7.0, EpistemicStatus.PROVEN),
        })
        target = _target()
        target = target.model_copy(update={
            "current_amps": _amps(2.0, EpistemicStatus.PROVEN),
        })
        result = evaluate_bridge_candidate(pattern, target)
        assert result.decision == "APPROVE_FOR_DC7_TEST"
        assert result.effective_status == EpistemicStatus.STRUCTURED


# ---------------------------------------------------------------------------
# Integration tests: evaluate_bridge_candidate — REJECT paths
# ---------------------------------------------------------------------------


class TestReject:
    def test_cross_client_not_authorised(self):
        result = evaluate_bridge_candidate(
            _pattern(cross_client=False),
            _target(),
        )
        assert result.decision == "REJECT"
        assert result.trust_state == TrustState.REJECTED
        assert "cross_client_learning_not_authorised" in result.reason_codes

    def test_shape_similarity_below_threshold(self):
        # All slots different → score 0.0
        pattern = _pattern(source_label=_label("A", "B", "1", "x"))
        target = _target(label=_label("Z", "Y", "9", "w"))
        result = evaluate_bridge_candidate(pattern, target)
        assert result.decision == "REJECT"
        assert "shape_similarity_below_threshold" in result.reason_codes

    def test_no_positive_delta(self):
        result = evaluate_bridge_candidate(
            _pattern(before=7.0, after=7.0),
            _target(score=2.0),
        )
        assert result.decision == "REJECT"
        assert "source_pattern_has_no_positive_measured_delta" in result.reason_codes

    def test_target_already_at_source_level(self):
        result = evaluate_bridge_candidate(
            _pattern(before=3.0, after=7.0),
            _target(score=8.0),
        )
        assert result.decision == "REJECT"
        assert "target_already_at_or_above_source_after_score" in result.reason_codes


# ---------------------------------------------------------------------------
# Integration tests: evaluate_bridge_candidate — QUARANTINE path
# ---------------------------------------------------------------------------


class TestQuarantine:
    def test_sensitive_detail_quarantines(self):
        result = evaluate_bridge_candidate(
            _pattern(sensitive=True),
            _target(),
        )
        assert result.decision == "QUARANTINE"
        assert result.trust_state == TrustState.QUARANTINED
        assert "pattern_contains_client_sensitive_detail" in result.reason_codes
        assert result.action is not None
        assert "Strip" in result.action

    def test_sensitive_overrides_other_rejection_reasons(self):
        # Even if cross-client is False AND similarity is low,
        # sensitive gets checked first.
        pattern = _pattern(sensitive=True, cross_client=False)
        pattern = pattern.model_copy(update={
            "source_label": _label("X", "X", "X", "X"),
        })
        result = evaluate_bridge_candidate(pattern, _target())
        assert result.decision == "QUARANTINE"


# ---------------------------------------------------------------------------
# Integration tests: evaluate_bridge_candidate — ESCALATE path
# ---------------------------------------------------------------------------


class TestEscalate:
    def test_intuited_evidence_escalates(self):
        result = evaluate_bridge_candidate(
            _pattern(evidence=EpistemicStatus.INTUITED),
            _target(),
        )
        assert result.decision == "ESCALATE_FOR_REVIEW"
        assert result.trust_state == TrustState.VALIDATED
        assert "pattern_not_measured_enough_for_autonomous_test" in result.reason_codes

    def test_structured_evidence_escalates(self):
        result = evaluate_bridge_candidate(
            _pattern(evidence=EpistemicStatus.STRUCTURED),
            _target(),
        )
        assert result.decision == "ESCALATE_FOR_REVIEW"
        assert "pattern_not_measured_enough_for_autonomous_test" in result.reason_codes


# ---------------------------------------------------------------------------
# Invariant tests — these should hold for ALL valid inputs.
# ---------------------------------------------------------------------------


class TestInvariants:
    """Properties that must hold regardless of input combination."""

    def test_effective_status_never_above_structured(self):
        """The gate itself is STRUCTURED, so output can never exceed that."""
        statuses = list(EpistemicStatus)
        for ev in statuses:
            for amps_st in statuses:
                for tgt_st in statuses:
                    pattern = _pattern(evidence=ev)
                    pattern = pattern.model_copy(update={
                        "after_amps": _amps(7.0, amps_st),
                    })
                    target = _target()
                    target = target.model_copy(update={
                        "current_amps": _amps(2.0, tgt_st),
                    })
                    result = evaluate_bridge_candidate(pattern, target)
                    assert result.effective_status <= EpistemicStatus.STRUCTURED

    def test_effective_status_is_min_of_inputs(self):
        """The min-rule: effective <= min(evidence, after_amps_status, target_status, STRUCTURED)."""
        pattern = _pattern(evidence=EpistemicStatus.INTUITED)
        pattern = pattern.model_copy(update={
            "after_amps": _amps(7.0, EpistemicStatus.PROVEN),
        })
        target = _target()
        target = target.model_copy(update={
            "current_amps": _amps(2.0, EpistemicStatus.MEASURED),
        })
        result = evaluate_bridge_candidate(pattern, target)
        # min(INTUITED=1, PROVEN=4, MEASURED=3, STRUCTURED=2) = INTUITED
        assert result.effective_status == EpistemicStatus.INTUITED

    def test_slot_match_score_bounded(self):
        """Slot match is always in [0.0, 1.0]."""
        for what in ["A", "B", "C"]:
            for how in ["X", "Y", ">"]:
                a = _label(what, how, "3", "v")
                b = _label("C", ">", "3", "v")
                score = calculate_slot_match_score(a, b)
                assert 0.0 <= score <= 1.0

    def test_reason_codes_never_empty(self):
        """Every decision has at least one reason code."""
        cases = [
            (_pattern(), _target()),
            (_pattern(sensitive=True), _target()),
            (_pattern(cross_client=False), _target()),
            (_pattern(evidence=EpistemicStatus.INTUITED), _target()),
            (_pattern(before=7.0, after=7.0), _target()),
            (_pattern(before=3.0, after=7.0), _target(score=8.0)),
        ]
        for pattern, target in cases:
            result = evaluate_bridge_candidate(pattern, target)
            assert len(result.reason_codes) > 0

    def test_amps_delta_consistent_with_scores(self):
        """amps_delta always equals after - before."""
        for before in [0.0, 3.0, 5.0, 7.0, 10.0]:
            for after in [0.0, 3.0, 5.0, 7.0, 10.0]:
                pattern = _pattern(before=before, after=after)
                result = evaluate_bridge_candidate(pattern, _target())
                assert result.amps_delta == pytest.approx(after - before)

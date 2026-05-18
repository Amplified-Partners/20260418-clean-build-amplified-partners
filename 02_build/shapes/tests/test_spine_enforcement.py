"""
Tests for Portable Spine integration as structural runtime invariants.

Verifies:
- Every shape declares at least one spine principle
- Every spine principle is covered by at least one shape
- Registry verify_spine_coverage() works correctly
- @spine decorator enforces non-empty declarations
- SpineViolation raised on structural drift

Authored by Devon-58ca | 2026-05-17 | session devin-58caaceb8d3b48188ab11d10821038f1
"""

from __future__ import annotations

import pytest

from shapes._types import SpinePrinciple, SpineViolation
from shapes._decorators import spine
from shapes._registry import REGISTRY
from shapes import (
    EntryBase,
    ServiceBase,
    WorkerBase,
    ConnectorBase,
    ModelBase,
    StoreBase,
    PipelineBase,
    OrchestratorBase,
    GuardBase,
    ScorerBase,
    AgentBase,
    TestBase,
    ConfigBase,
    TelemetryBase,
    GlueBase,
)


ALL_SHAPE_BASES = [
    EntryBase,
    ServiceBase,
    WorkerBase,
    ConnectorBase,
    ModelBase,
    StoreBase,
    PipelineBase,
    OrchestratorBase,
    GuardBase,
    ScorerBase,
    AgentBase,
    TestBase,
    ConfigBase,
    TelemetryBase,
    GlueBase,
]

ALL_PRINCIPLES = set(SpinePrinciple)


class TestSpinePrincipleEnum:
    """The nine principles exist and match PORTABLE-SPINE.md."""

    def test_nine_principles_exist(self) -> None:
        assert len(SpinePrinciple) == 9

    def test_principle_values(self) -> None:
        expected = {
            "radical_honesty",
            "radical_transparency",
            "radical_attribution",
            "win_win",
            "deterministic_first",
            "congruence",
            "narrow_handoff",
            "shadow_first",
            "privacy_first",
        }
        actual = {p.value for p in SpinePrinciple}
        assert actual == expected

    def test_label_formatting(self) -> None:
        assert SpinePrinciple.RADICAL_HONESTY.label() == "Radical Honesty"
        assert SpinePrinciple.WIN_WIN.label() == "Win Win"
        assert SpinePrinciple.DETERMINISTIC_FIRST.label() == "Deterministic First"


class TestSpineDecorator:
    """@spine decorator sets _spine_principles on classes."""

    def test_spine_sets_principles(self) -> None:
        @spine("radical_honesty", "congruence")
        class DummyShape:
            pass

        assert hasattr(DummyShape, "_spine_principles")
        assert DummyShape._spine_principles == (
            SpinePrinciple.RADICAL_HONESTY,
            SpinePrinciple.CONGRUENCE,
        )

    def test_spine_empty_raises(self) -> None:
        with pytest.raises(SpineViolation, match="at least one principle"):
            @spine()
            class EmptySpine:
                pass

    def test_spine_invalid_principle_raises(self) -> None:
        with pytest.raises(ValueError):
            @spine("not_a_principle")
            class BadSpine:
                pass

    def test_spine_single_principle(self) -> None:
        @spine("privacy_first")
        class SinglePrinciple:
            pass

        assert SinglePrinciple._spine_principles == (SpinePrinciple.PRIVACY_FIRST,)

    def test_spine_all_nine(self) -> None:
        @spine(
            "radical_honesty", "radical_transparency", "radical_attribution",
            "win_win", "deterministic_first", "congruence",
            "narrow_handoff", "shadow_first", "privacy_first",
        )
        class AllNine:
            pass

        assert len(AllNine._spine_principles) == 9


class TestShapeSpineDeclarations:
    """Every shape base class declares at least one spine principle."""

    @pytest.mark.parametrize("shape_cls", ALL_SHAPE_BASES, ids=lambda c: c.__name__)
    def test_shape_has_spine_principles(self, shape_cls: type) -> None:
        principles = getattr(shape_cls, "_spine_principles", None)
        assert principles is not None, (
            f"{shape_cls.__name__} has no _spine_principles — unmoored shape"
        )
        assert len(principles) >= 1, (
            f"{shape_cls.__name__} declares zero principles"
        )

    @pytest.mark.parametrize("shape_cls", ALL_SHAPE_BASES, ids=lambda c: c.__name__)
    def test_shape_principles_are_valid_enum_members(self, shape_cls: type) -> None:
        principles = getattr(shape_cls, "_spine_principles", ())
        for p in principles:
            assert isinstance(p, SpinePrinciple), (
                f"{shape_cls.__name__} has non-SpinePrinciple: {p}"
            )


class TestSpineCoverage:
    """Every principle is covered by at least one shape. No dead principles."""

    def test_all_principles_covered(self) -> None:
        covered: set[SpinePrinciple] = set()
        for shape_cls in ALL_SHAPE_BASES:
            principles = getattr(shape_cls, "_spine_principles", ())
            covered.update(principles)
        uncovered = ALL_PRINCIPLES - covered
        assert not uncovered, (
            f"Dead principles — no shape enforces: "
            f"{', '.join(p.label() for p in uncovered)}"
        )

    def test_all_shapes_moored(self) -> None:
        for shape_cls in ALL_SHAPE_BASES:
            principles = getattr(shape_cls, "_spine_principles", None)
            assert principles is not None and len(principles) > 0, (
                f"{shape_cls.__name__} is unmoored — declares no spine principles"
            )


class TestRegistrySpineCoverage:
    """Registry verify_spine_coverage() works as structural verification."""

    def test_verify_returns_report(self) -> None:
        report = REGISTRY.verify_spine_coverage()
        assert isinstance(report, dict)
        assert "all_covered" in report
        assert "all_moored" in report
        assert "coverage" in report
        assert "uncovered_principles" in report
        assert "unmoored_shapes" in report

    def test_verify_all_covered(self) -> None:
        report = REGISTRY.verify_spine_coverage()
        assert report["all_covered"] is True
        assert report["uncovered_principles"] == []

    def test_verify_coverage_map_has_all_principles(self) -> None:
        report = REGISTRY.verify_spine_coverage()
        coverage_keys = set(report["coverage"].keys())
        expected_keys = {p.value for p in SpinePrinciple}
        assert coverage_keys == expected_keys


class TestSpineViolation:
    """SpineViolation error class works correctly."""

    def test_spine_violation_is_shape_error(self) -> None:
        from shapes._types import ShapeError
        v = SpineViolation("test violation")
        assert isinstance(v, ShapeError)

    def test_spine_violation_fields(self) -> None:
        v = SpineViolation(
            "dead principle",
            principle="radical_honesty",
            shape_name="TestShape",
            violation_type="uncovered_principle",
        )
        assert v.principle == "radical_honesty"
        assert v.shape_name == "TestShape"
        assert v.violation_type == "uncovered_principle"
        assert "dead principle" in str(v)


class TestSpecificAssignments:
    """Spot-check that specific shapes enforce the right principles."""

    def test_entry_enforces_narrow_handoff(self) -> None:
        assert SpinePrinciple.NARROW_HANDOFF in EntryBase._spine_principles

    def test_guard_enforces_radical_honesty(self) -> None:
        assert SpinePrinciple.RADICAL_HONESTY in GuardBase._spine_principles

    def test_agent_enforces_shadow_first(self) -> None:
        assert SpinePrinciple.SHADOW_FIRST in AgentBase._spine_principles

    def test_store_enforces_privacy_first(self) -> None:
        assert SpinePrinciple.PRIVACY_FIRST in StoreBase._spine_principles

    def test_glue_enforces_win_win(self) -> None:
        assert SpinePrinciple.WIN_WIN in GlueBase._spine_principles

    def test_telemetry_enforces_shadow_first(self) -> None:
        assert SpinePrinciple.SHADOW_FIRST in TelemetryBase._spine_principles

    def test_orchestrator_enforces_radical_attribution(self) -> None:
        assert SpinePrinciple.RADICAL_ATTRIBUTION in OrchestratorBase._spine_principles

    def test_model_enforces_congruence(self) -> None:
        assert SpinePrinciple.CONGRUENCE in ModelBase._spine_principles

    def test_test_enforces_radical_honesty(self) -> None:
        assert SpinePrinciple.RADICAL_HONESTY in TestBase._spine_principles

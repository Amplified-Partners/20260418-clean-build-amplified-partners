"""
Epistemic integration tests for the Huf Haus shape system.

Tests the runtime epistemic invariant enforcement:
- StatusedOutput carries status + provenance
- Min-rule floors output to lowest input
- Bare value at strict boundary raises P0 (EpistemicViolation)
- Stale input demotes output
- Failed precondition demotes output
- Over-claiming (gap >= 2) raises P0
- Audit log records all boundary crossings
- Backward compat: existing @epistemic still sets metadata only
- Cross-shape composition propagates status correctly

Authored by Devon-b5dc | 2026-05-17 | session devin-b5dc68e1aefa4982b9c083714ac968c6
"""

from __future__ import annotations

import datetime as dt
import unittest

from shapes import (
    EpistemicTier,
    EpistemicViolation,
    PreconditionCheck,
    SHAPE_AUDIT_LOG,
    ShapeBase,
    ShapeKind,
    StatusedOutput,
    epistemic,
)
from shapes._epistemic import ShapeProvenance, _demote


# ---------------------------------------------------------------------------
# Test shapes — purpose-built for epistemic testing
# ---------------------------------------------------------------------------


@epistemic(tier="structured", canon_ref="test_method", protected="execute")
class EnforcedService(ShapeBase):
    """A service with runtime epistemic enforcement on execute()."""

    shape_kind = ShapeKind.SERVICE

    def execute(self, input_data):
        return {"result": input_data * 2}


@epistemic(tier="structured", canon_ref="test_strict", protected="execute", strict=True)
class StrictService(ShapeBase):
    """A service that rejects bare values at the boundary."""

    shape_kind = ShapeKind.SERVICE

    def execute(self, input_data):
        return {"result": input_data + 1}


@epistemic(tier="measured", protected="execute")
class MeasuredService(ShapeBase):
    """A service claiming MEASURED tier."""

    shape_kind = ShapeKind.SERVICE

    def execute(self, input_data):
        return {"measured": input_data}


@epistemic(tier="proven", protected="execute")
class ProvenService(ShapeBase):
    """A service claiming PROVEN tier — will trigger gap violations."""

    shape_kind = ShapeKind.SERVICE

    def execute(self, input_data):
        return {"proven": input_data}


@epistemic(tier="structured", protected="execute")
class PreconditionService(ShapeBase):
    """A service with preconditions that can fail."""

    shape_kind = ShapeKind.SERVICE
    preconditions_hold: bool = True

    def verify_preconditions(self):
        return (
            PreconditionCheck(
                name="data_freshness",
                holds=self.preconditions_hold,
                evidence="test precondition",
            ),
        )

    def execute(self, input_data):
        return {"checked": input_data}


@epistemic(tier="structured", canon_ref="metadata_only")
class MetadataOnlyService(ShapeBase):
    """No protected= arg — backward compat, metadata only."""

    shape_kind = ShapeKind.SERVICE

    def execute(self, input_data):
        return {"raw": input_data}


# ---------------------------------------------------------------------------
# Tests
# ---------------------------------------------------------------------------


class TestEpistemicBridgeTypes(unittest.TestCase):
    """U02: Bridge types work correctly."""

    def test_epistemic_tier_ordering(self):
        self.assertLess(EpistemicTier.INTUITED, EpistemicTier.STRUCTURED)
        self.assertLess(EpistemicTier.STRUCTURED, EpistemicTier.MEASURED)
        self.assertLess(EpistemicTier.MEASURED, EpistemicTier.PROVEN)

    def test_epistemic_tier_from_string(self):
        self.assertEqual(EpistemicTier.from_string("intuited"), EpistemicTier.INTUITED)
        self.assertEqual(EpistemicTier.from_string("structured"), EpistemicTier.STRUCTURED)
        self.assertEqual(EpistemicTier.from_string("measured"), EpistemicTier.MEASURED)
        self.assertEqual(EpistemicTier.from_string("proven"), EpistemicTier.PROVEN)

    def test_demotion(self):
        self.assertEqual(_demote(EpistemicTier.PROVEN), EpistemicTier.MEASURED)
        self.assertEqual(_demote(EpistemicTier.MEASURED), EpistemicTier.STRUCTURED)
        self.assertEqual(_demote(EpistemicTier.STRUCTURED), EpistemicTier.INTUITED)
        self.assertEqual(_demote(EpistemicTier.INTUITED), EpistemicTier.INTUITED)

    def test_statused_output_construction(self):
        prov = ShapeProvenance(shape_name="TestShape", method="run")
        out = StatusedOutput(
            value=42,
            status=EpistemicTier.STRUCTURED,
            provenance=prov,
        )
        self.assertEqual(out.value, 42)
        self.assertEqual(out.status, EpistemicTier.STRUCTURED)
        self.assertEqual(out.provenance.shape_name, "TestShape")
        self.assertFalse(out.is_stale())

    def test_statused_output_staleness(self):
        prov = ShapeProvenance(shape_name="TestShape", method="run")
        past = dt.datetime(2020, 1, 1, tzinfo=dt.timezone.utc)
        out = StatusedOutput(
            value="old",
            status=EpistemicTier.MEASURED,
            provenance=prov,
            valid_until=past,
        )
        self.assertTrue(out.is_stale())

    def test_min_rule_on_statused_output(self):
        prov = ShapeProvenance(shape_name="TestShape", method="run")
        out = StatusedOutput(
            value="x",
            status=EpistemicTier.MEASURED,
            provenance=prov,
        )
        effective = out.effective_status(
            input_statuses=[EpistemicTier.INTUITED, EpistemicTier.STRUCTURED]
        )
        self.assertEqual(effective, EpistemicTier.INTUITED)


class TestBackwardCompatibility(unittest.TestCase):
    """R08, R09: Existing behaviour preserved."""

    def test_metadata_only_still_sets_attributes(self):
        self.assertEqual(MetadataOnlyService._epistemic_tier, "structured")
        self.assertEqual(MetadataOnlyService._canon_ref, "metadata_only")

    def test_metadata_only_execute_returns_raw(self):
        svc = MetadataOnlyService()
        result = svc.execute({"key": "val"})
        self.assertEqual(result, {"raw": {"key": "val"}})
        self.assertNotIsInstance(result, StatusedOutput)

    def test_enforced_still_sets_metadata_attributes(self):
        self.assertEqual(EnforcedService._epistemic_tier, "structured")
        self.assertEqual(EnforcedService._canon_ref, "test_method")


class TestRuntimeEnforcement(unittest.TestCase):
    """R01, R03: Protected methods produce StatusedOutput with min-rule."""

    def setUp(self):
        SHAPE_AUDIT_LOG.clear()

    def test_enforced_output_is_statused(self):
        svc = EnforcedService()
        result = svc.execute(5)
        self.assertIsInstance(result, StatusedOutput)
        self.assertEqual(result.value, {"result": 10})

    def test_lenient_mode_wraps_bare_as_intuited(self):
        svc = EnforcedService()
        result = svc.execute(5)
        # Bare input auto-wrapped as INTUITED floors the STRUCTURED claim
        self.assertEqual(result.status, EpistemicTier.INTUITED)

    def test_statused_input_preserves_tier(self):
        svc = EnforcedService()
        inp = StatusedOutput(
            value=5,
            status=EpistemicTier.STRUCTURED,
            provenance=ShapeProvenance(shape_name="upstream", method="produce"),
        )
        result = svc.execute(inp)
        self.assertIsInstance(result, StatusedOutput)
        self.assertEqual(result.value, {"result": 10})
        self.assertEqual(result.status, EpistemicTier.STRUCTURED)

    def test_lower_input_floors_higher_claim(self):
        svc = MeasuredService()
        inp = StatusedOutput(
            value="data",
            status=EpistemicTier.STRUCTURED,
            provenance=ShapeProvenance(shape_name="upstream", method="calculate"),
        )
        result = svc.execute(inp)
        # MEASURED shape receives STRUCTURED input → output floored to STRUCTURED
        self.assertEqual(result.status, EpistemicTier.STRUCTURED)

    def test_gap_two_intuited_into_measured_raises_p0(self):
        svc = MeasuredService()
        inp = StatusedOutput(
            value="data",
            status=EpistemicTier.INTUITED,
            provenance=ShapeProvenance(shape_name="upstream", method="guess"),
        )
        # MEASURED(3) + INTUITED(1) = gap 2 → P0
        with self.assertRaises(EpistemicViolation) as ctx:
            svc.execute(inp)
        self.assertEqual(ctx.exception.violation_type, "gap_exceeded")

    def test_provenance_records_shape_and_method(self):
        svc = EnforcedService()
        inp = StatusedOutput(
            value=7,
            status=EpistemicTier.STRUCTURED,
            provenance=ShapeProvenance(shape_name="source", method="emit"),
        )
        result = svc.execute(inp)
        self.assertEqual(result.provenance.shape_name, "EnforcedService")
        self.assertEqual(result.provenance.method, "execute")
        self.assertIn(inp.output_id, result.provenance.input_ids)


class TestBareValueRejection(unittest.TestCase):
    """R02: Strict mode rejects bare values at protected boundary."""

    def test_strict_rejects_bare_value(self):
        svc = StrictService()
        with self.assertRaises(EpistemicViolation) as ctx:
            svc.execute(42)
        self.assertEqual(ctx.exception.violation_type, "bare_value")
        self.assertIn("laundering trap", str(ctx.exception))

    def test_strict_accepts_statused_input(self):
        svc = StrictService()
        inp = StatusedOutput(
            value=42,
            status=EpistemicTier.STRUCTURED,
            provenance=ShapeProvenance(shape_name="producer", method="make"),
        )
        result = svc.execute(inp)
        self.assertIsInstance(result, StatusedOutput)
        self.assertEqual(result.value, {"result": 43})


class TestStaleDemotion(unittest.TestCase):
    """R04: Stale inputs demote output by one tier."""

    def setUp(self):
        SHAPE_AUDIT_LOG.clear()

    def test_stale_input_demotes_output(self):
        svc = EnforcedService()
        past = dt.datetime(2020, 1, 1, tzinfo=dt.timezone.utc)
        stale_inp = StatusedOutput(
            value=10,
            status=EpistemicTier.STRUCTURED,
            provenance=ShapeProvenance(shape_name="old_source", method="emit"),
            valid_until=past,
        )
        result = svc.execute(stale_inp)
        # STRUCTURED input is stale → demoted to INTUITED → floors output
        self.assertEqual(result.status, EpistemicTier.INTUITED)


class TestPreconditionDemotion(unittest.TestCase):
    """R05: Failed preconditions demote output."""

    def setUp(self):
        SHAPE_AUDIT_LOG.clear()

    def test_passing_preconditions_no_demotion(self):
        svc = PreconditionService()
        svc.preconditions_hold = True
        inp = StatusedOutput(
            value="data",
            status=EpistemicTier.STRUCTURED,
            provenance=ShapeProvenance(shape_name="upstream", method="emit"),
        )
        result = svc.execute(inp)
        self.assertEqual(result.status, EpistemicTier.STRUCTURED)

    def test_failing_preconditions_demotes(self):
        svc = PreconditionService()
        svc.preconditions_hold = False
        inp = StatusedOutput(
            value="data",
            status=EpistemicTier.STRUCTURED,
            provenance=ShapeProvenance(shape_name="upstream", method="emit"),
        )
        result = svc.execute(inp)
        # STRUCTURED with failed precondition → demoted to INTUITED
        self.assertEqual(result.status, EpistemicTier.INTUITED)


class TestOverClaimingDetection(unittest.TestCase):
    """R06: Gap >= 2 between declared and effective raises P0."""

    def setUp(self):
        SHAPE_AUDIT_LOG.clear()

    def test_gap_exceeds_two_raises_p0(self):
        svc = ProvenService()
        inp = StatusedOutput(
            value="lowly",
            status=EpistemicTier.INTUITED,
            provenance=ShapeProvenance(shape_name="unreliable", method="guess"),
        )
        with self.assertRaises(EpistemicViolation) as ctx:
            svc.execute(inp)
        self.assertEqual(ctx.exception.violation_type, "gap_exceeded")
        self.assertIn("PROVEN", ctx.exception.declared_tier.upper())

    def test_gap_of_one_does_not_raise(self):
        svc = MeasuredService()
        inp = StatusedOutput(
            value="ok",
            status=EpistemicTier.STRUCTURED,
            provenance=ShapeProvenance(shape_name="reasonable", method="calculate"),
        )
        # MEASURED claim, STRUCTURED input → effective STRUCTURED, gap=1, no P0
        result = svc.execute(inp)
        self.assertEqual(result.status, EpistemicTier.STRUCTURED)


class TestAuditLog(unittest.TestCase):
    """R07: Audit/provenance records written and inspectable."""

    def setUp(self):
        SHAPE_AUDIT_LOG.clear()

    def test_audit_record_written_on_crossing(self):
        svc = EnforcedService()
        inp = StatusedOutput(
            value=3,
            status=EpistemicTier.STRUCTURED,
            provenance=ShapeProvenance(shape_name="source", method="emit"),
        )
        svc.execute(inp)
        self.assertEqual(SHAPE_AUDIT_LOG.size, 1)
        record = SHAPE_AUDIT_LOG.all()[0]
        self.assertEqual(record.shape_name, "EnforcedService")
        self.assertEqual(record.method, "execute")
        self.assertEqual(record.declared_status, EpistemicTier.STRUCTURED)
        self.assertEqual(record.effective_status, EpistemicTier.STRUCTURED)

    def test_audit_records_multiple_crossings(self):
        svc1 = EnforcedService()
        svc2 = MeasuredService()
        inp = StatusedOutput(
            value=5,
            status=EpistemicTier.STRUCTURED,
            provenance=ShapeProvenance(shape_name="source", method="emit"),
        )
        out1 = svc1.execute(inp)
        svc2.execute(out1)
        self.assertEqual(SHAPE_AUDIT_LOG.size, 2)

    def test_audit_record_captures_demotion_reason(self):
        svc = EnforcedService()
        svc.execute(42)  # bare value in lenient mode → floors to INTUITED
        record = SHAPE_AUDIT_LOG.all()[0]
        self.assertEqual(record.effective_status, EpistemicTier.INTUITED)
        self.assertIn("min(", record.reason)


class TestCrossShapeComposition(unittest.TestCase):
    """R08, R10: Cross-shape composition propagates status correctly."""

    def setUp(self):
        SHAPE_AUDIT_LOG.clear()

    def test_chain_propagates_status(self):
        """STRUCTURED → MEASURED: output stays STRUCTURED (floored by input)."""
        svc1 = EnforcedService()
        svc2 = MeasuredService()
        inp = StatusedOutput(
            value=5,
            status=EpistemicTier.STRUCTURED,
            provenance=ShapeProvenance(shape_name="origin", method="start"),
        )
        mid = svc1.execute(inp)
        self.assertEqual(mid.status, EpistemicTier.STRUCTURED)
        final = svc2.execute(mid)
        # MEASURED shape, STRUCTURED input → floored to STRUCTURED
        self.assertEqual(final.status, EpistemicTier.STRUCTURED)

    def test_degradation_propagates_through_chain(self):
        """INTUITED into STRUCTURED → INTUITED output, gap=1 OK."""
        svc1 = EnforcedService()  # STRUCTURED
        svc2 = MeasuredService()  # MEASURED
        inp = StatusedOutput(
            value="data",
            status=EpistemicTier.STRUCTURED,
            provenance=ShapeProvenance(shape_name="source", method="emit"),
        )
        mid = svc1.execute(inp)
        self.assertEqual(mid.status, EpistemicTier.STRUCTURED)
        # MEASURED receives STRUCTURED (gap=1, OK) → output STRUCTURED
        final = svc2.execute(mid)
        self.assertEqual(final.status, EpistemicTier.STRUCTURED)

    def test_gap_two_halts_chain(self):
        """INTUITED through STRUCTURED → INTUITED, then into MEASURED → P0."""
        svc1 = EnforcedService()  # STRUCTURED
        svc2 = MeasuredService()  # MEASURED
        inp = StatusedOutput(
            value=1,
            status=EpistemicTier.INTUITED,
            provenance=ShapeProvenance(shape_name="vibe", method="guess"),
        )
        mid = svc1.execute(inp)
        self.assertEqual(mid.status, EpistemicTier.INTUITED)
        with self.assertRaises(EpistemicViolation):
            svc2.execute(mid)


if __name__ == "__main__":
    unittest.main()

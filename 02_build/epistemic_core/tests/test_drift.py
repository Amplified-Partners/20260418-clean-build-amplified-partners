"""
Tests for drift detection.

Tests that:
- Any silent promotion raises P0 (BLACK signal) — even one tier
- Gap size is severity metadata on the exception, not the trigger
- Legal demotion → RED (not BLACK)
- Failing preconditions → AMBER
- Clean record → GREEN
- Drift detector tracks incidents

Signed-by: Devon-d493 | 2026-05-19 | devin-d49302e4179d43d0892997a7f3a9f57f
"""

from __future__ import annotations

import datetime as dt
import unittest
import uuid

from epistemic_core.tiers import EpistemicTier
from epistemic_core.min_rule import Provenance, PreconditionCheck
from epistemic_core.audit import AuditLog, StatusRecord
from epistemic_core.drift import DriftDetector, DriftSignal
from epistemic_core.p0_policy import P0Incident


def _record(
    declared: EpistemicTier,
    effective: EpistemicTier,
    preconditions: tuple[PreconditionCheck, ...] = (),
    layer: str = "test_layer",
) -> StatusRecord:
    return StatusRecord(
        record_id=str(uuid.uuid4()),
        timestamp=dt.datetime.now(dt.timezone.utc),
        layer=layer,
        declared_status=declared,
        effective_status=effective,
        provenance=Provenance(layer=layer, method="test"),
        preconditions=preconditions,
    )


class TestDriftDetectorBlack(unittest.TestCase):
    """BLACK = any silent promotion. P0Incident raised."""

    def test_single_tier_promotion_is_p0(self):
        """Even a one-tier promotion is P0 (DeepSeek V4 correction)."""
        audit = AuditLog()
        detector = DriftDetector(audit)

        rec = _record(
            declared=EpistemicTier.INTUITED,
            effective=EpistemicTier.STRUCTURED,
        )
        with self.assertRaises(P0Incident) as ctx:
            audit.write(rec)

        self.assertEqual(detector.signal, DriftSignal.BLACK)
        self.assertEqual(ctx.exception.gap, 1)

    def test_two_tier_promotion_is_p0(self):
        audit = AuditLog()
        detector = DriftDetector(audit)

        rec = _record(
            declared=EpistemicTier.INTUITED,
            effective=EpistemicTier.MEASURED,
        )
        with self.assertRaises(P0Incident) as ctx:
            audit.write(rec)

        self.assertEqual(detector.signal, DriftSignal.BLACK)
        self.assertEqual(ctx.exception.gap, 2)

    def test_three_tier_promotion_is_p0(self):
        audit = AuditLog()
        detector = DriftDetector(audit)

        rec = _record(
            declared=EpistemicTier.INTUITED,
            effective=EpistemicTier.PROVEN,
        )
        with self.assertRaises(P0Incident) as ctx:
            audit.write(rec)

        self.assertEqual(detector.signal, DriftSignal.BLACK)
        self.assertEqual(ctx.exception.gap, 3)

    def test_incidents_tracked(self):
        audit = AuditLog()
        detector = DriftDetector(audit)

        rec = _record(
            declared=EpistemicTier.STRUCTURED,
            effective=EpistemicTier.MEASURED,
        )
        with self.assertRaises(P0Incident):
            audit.write(rec)

        self.assertEqual(len(detector.incidents), 1)


class TestDriftDetectorRed(unittest.TestCase):
    """RED = legal demotion. Not a P0, but flagged."""

    def test_single_tier_demotion_is_red(self):
        audit = AuditLog()
        detector = DriftDetector(audit)

        rec = _record(
            declared=EpistemicTier.MEASURED,
            effective=EpistemicTier.STRUCTURED,
        )
        audit.write(rec)
        self.assertEqual(detector.signal, DriftSignal.RED)

    def test_two_tier_demotion_is_red(self):
        audit = AuditLog()
        detector = DriftDetector(audit)

        rec = _record(
            declared=EpistemicTier.PROVEN,
            effective=EpistemicTier.STRUCTURED,
        )
        audit.write(rec)
        self.assertEqual(detector.signal, DriftSignal.RED)


class TestDriftDetectorAmber(unittest.TestCase):
    """AMBER = failing preconditions with matching tiers."""

    def test_failing_precondition_is_amber(self):
        audit = AuditLog()
        detector = DriftDetector(audit)

        prec = PreconditionCheck(name="freshness", holds=False, evidence="expired")
        rec = _record(
            declared=EpistemicTier.STRUCTURED,
            effective=EpistemicTier.STRUCTURED,
            preconditions=(prec,),
        )
        audit.write(rec)
        self.assertEqual(detector.signal, DriftSignal.AMBER)


class TestDriftDetectorGreen(unittest.TestCase):
    """GREEN = everything matches."""

    def test_matching_tiers_no_issues_is_green(self):
        audit = AuditLog()
        detector = DriftDetector(audit)

        rec = _record(
            declared=EpistemicTier.STRUCTURED,
            effective=EpistemicTier.STRUCTURED,
        )
        audit.write(rec)
        self.assertEqual(detector.signal, DriftSignal.GREEN)

    def test_green_with_passing_preconditions(self):
        audit = AuditLog()
        detector = DriftDetector(audit)

        prec = PreconditionCheck(name="freshness", holds=True, evidence="ok")
        rec = _record(
            declared=EpistemicTier.MEASURED,
            effective=EpistemicTier.MEASURED,
            preconditions=(prec,),
        )
        audit.write(rec)
        self.assertEqual(detector.signal, DriftSignal.GREEN)


if __name__ == "__main__":
    unittest.main()

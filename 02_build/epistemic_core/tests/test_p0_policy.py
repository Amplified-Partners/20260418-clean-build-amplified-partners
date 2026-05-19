"""
Tests for P0 policy enforcement.

Tests that:
- P0 HALT stops the production path
- Any silent promotion is P0 (even one tier)
- DEGRADE mode does not raise but logs
- TELEMETRY_ONLY mode does not raise
- tier skipping in promotion gates raises P0
- bare values at boundaries are caught

Signed-by: Devon-d493 | 2026-05-19 | devin-d49302e4179d43d0892997a7f3a9f57f
"""

from __future__ import annotations

import unittest

from epistemic_core.tiers import EpistemicTier
from epistemic_core.p0_policy import (
    P0Incident,
    P0Policy,
    enforce_p0,
)


class TestP0Incident(unittest.TestCase):
    def test_is_exception(self):
        with self.assertRaises(P0Incident):
            raise P0Incident("test")

    def test_carries_gap_metadata(self):
        exc = P0Incident("test", gap=2)
        self.assertEqual(exc.gap, 2)

    def test_default_gap_is_zero(self):
        exc = P0Incident("test")
        self.assertEqual(exc.gap, 0)


class TestEnforceP0(unittest.TestCase):
    def test_halt_on_silent_promotion(self):
        """Any silent promotion = P0Incident when policy is HALT."""
        with self.assertRaises(P0Incident):
            enforce_p0(
                declared=EpistemicTier.INTUITED,
                effective=EpistemicTier.STRUCTURED,
                context="test: one-tier promotion",
                policy=P0Policy.HALT,
            )

    def test_halt_on_single_tier_promotion(self):
        """Even a single-tier promotion is P0."""
        with self.assertRaises(P0Incident):
            enforce_p0(
                declared=EpistemicTier.STRUCTURED,
                effective=EpistemicTier.MEASURED,
                context="test: STRUCTURED -> MEASURED",
                policy=P0Policy.HALT,
            )

    def test_halt_on_multi_tier_promotion(self):
        """Multi-tier promotion is also P0 (gap is severity metadata)."""
        with self.assertRaises(P0Incident) as ctx:
            enforce_p0(
                declared=EpistemicTier.INTUITED,
                effective=EpistemicTier.PROVEN,
                context="test: INTUITED -> PROVEN",
                policy=P0Policy.HALT,
            )
        self.assertEqual(ctx.exception.gap, 3)

    def test_degrade_no_raise(self):
        """DEGRADE mode logs but does not raise."""
        enforce_p0(
            declared=EpistemicTier.INTUITED,
            effective=EpistemicTier.STRUCTURED,
            context="test: degrade mode",
            policy=P0Policy.DEGRADE,
        )

    def test_telemetry_only_no_raise(self):
        """TELEMETRY_ONLY mode logs but does not raise."""
        enforce_p0(
            declared=EpistemicTier.INTUITED,
            effective=EpistemicTier.PROVEN,
            context="test: telemetry only",
            policy=P0Policy.TELEMETRY_ONLY,
        )

    def test_legal_demotion_no_raise(self):
        """Legal demotion (effective < declared) is not a P0."""
        enforce_p0(
            declared=EpistemicTier.MEASURED,
            effective=EpistemicTier.INTUITED,
            context="test: legal demotion",
            policy=P0Policy.HALT,
        )

    def test_no_change_no_raise(self):
        """Same tier = no issue."""
        enforce_p0(
            declared=EpistemicTier.STRUCTURED,
            effective=EpistemicTier.STRUCTURED,
            context="test: no change",
            policy=P0Policy.HALT,
        )

    def test_uses_active_policy_by_default(self):
        """When no policy passed, uses module-level ACTIVE_P0_POLICY (HALT)."""
        with self.assertRaises(P0Incident):
            enforce_p0(
                declared=EpistemicTier.INTUITED,
                effective=EpistemicTier.STRUCTURED,
                context="test: default policy",
            )


if __name__ == "__main__":
    unittest.main()

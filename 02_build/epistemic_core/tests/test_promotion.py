"""
Tests for promotion gates.

Tests that:
- Tier skipping is forbidden (P0)
- Each gate requires the correct input tier
- Sample size floor enforced for MEASURED
- PROVEN requires all preconditions passing
- Promotion records are persisted
- LLM/runtime values cannot silently become MEASURED or PROVEN

Signed-by: Devon-d493 | 2026-05-19 | devin-d49302e4179d43d0892997a7f3a9f57f
"""

from __future__ import annotations

import unittest

from epistemic_core.tiers import EpistemicTier
from epistemic_core.min_rule import StatusedValue, Provenance, PreconditionCheck
from epistemic_core.p0_policy import P0Incident
from epistemic_core.promotion import (
    MEASURED_SAMPLE_SIZE_FLOOR,
    PromotionStore,
    promote_to_structured,
    promote_to_measured,
    promote_to_proven,
)


def _prov() -> Provenance:
    return Provenance(layer="test", method="test_method")


def _sv(tier: EpistemicTier) -> StatusedValue:
    return StatusedValue(value="test_value", status=tier, provenance=_prov())


class TestPromoteToStructured(unittest.TestCase):
    def setUp(self):
        self.store = PromotionStore()

    def test_promotes_intuited_to_structured(self):
        sv = _sv(EpistemicTier.INTUITED)
        result = promote_to_structured(
            sv, rubric_path="/test/rubric.md", approver="test", store=self.store
        )
        self.assertEqual(result.status, EpistemicTier.STRUCTURED)
        self.assertIsNotNone(result.provenance.promotion_record_id)

    def test_rejects_structured_input(self):
        sv = _sv(EpistemicTier.STRUCTURED)
        with self.assertRaises(P0Incident):
            promote_to_structured(
                sv, rubric_path="/test/rubric.md", approver="test", store=self.store
            )

    def test_rejects_measured_input(self):
        sv = _sv(EpistemicTier.MEASURED)
        with self.assertRaises(P0Incident):
            promote_to_structured(
                sv, rubric_path="/test/rubric.md", approver="test", store=self.store
            )

    def test_persists_record(self):
        sv = _sv(EpistemicTier.INTUITED)
        promote_to_structured(
            sv, rubric_path="/test/rubric.md", approver="test_user", store=self.store
        )
        self.assertEqual(self.store.size, 1)
        record = self.store.all()[0]
        self.assertEqual(record.from_status, EpistemicTier.INTUITED)
        self.assertEqual(record.to_status, EpistemicTier.STRUCTURED)
        self.assertEqual(record.method, "rubric_codification")
        self.assertEqual(record.approver, "test_user")


class TestPromoteToMeasured(unittest.TestCase):
    def setUp(self):
        self.store = PromotionStore()
        self.kwargs = dict(
            sample_size=50,
            confidence_interval=(0.90, 0.99),
            held_out_validation=0.2,
            drift_monitor_id="dm-001",
            approver="test",
            store=self.store,
        )

    def test_promotes_structured_to_measured(self):
        sv = _sv(EpistemicTier.STRUCTURED)
        result = promote_to_measured(sv, **self.kwargs)
        self.assertEqual(result.status, EpistemicTier.MEASURED)
        self.assertEqual(result.sample_size, 50)

    def test_rejects_intuited_input(self):
        sv = _sv(EpistemicTier.INTUITED)
        with self.assertRaises(P0Incident):
            promote_to_measured(sv, **self.kwargs)

    def test_rejects_proven_input(self):
        sv = _sv(EpistemicTier.PROVEN)
        with self.assertRaises(P0Incident):
            promote_to_measured(sv, **self.kwargs)

    def test_sample_size_floor_enforced(self):
        sv = _sv(EpistemicTier.STRUCTURED)
        with self.assertRaises(P0Incident):
            promote_to_measured(
                sv,
                sample_size=MEASURED_SAMPLE_SIZE_FLOOR - 1,
                confidence_interval=(0.90, 0.99),
                held_out_validation=0.2,
                drift_monitor_id="dm-001",
                approver="test",
                store=self.store,
            )

    def test_sample_size_at_floor_succeeds(self):
        sv = _sv(EpistemicTier.STRUCTURED)
        result = promote_to_measured(
            sv,
            sample_size=MEASURED_SAMPLE_SIZE_FLOOR,
            confidence_interval=(0.90, 0.99),
            held_out_validation=0.2,
            drift_monitor_id="dm-001",
            approver="test",
            store=self.store,
        )
        self.assertEqual(result.status, EpistemicTier.MEASURED)

    def test_persists_record(self):
        sv = _sv(EpistemicTier.STRUCTURED)
        promote_to_measured(sv, **self.kwargs)
        self.assertEqual(self.store.size, 1)


class TestPromoteToProven(unittest.TestCase):
    def setUp(self):
        self.store = PromotionStore()

    def test_promotes_measured_to_proven(self):
        sv = _sv(EpistemicTier.MEASURED)
        prec = PreconditionCheck(name="axiom_1", holds=True, evidence="verified")
        result = promote_to_proven(
            sv, theorem="x=x", preconditions=[prec], approver="test", store=self.store
        )
        self.assertEqual(result.status, EpistemicTier.PROVEN)
        self.assertEqual(result.preconditions, (prec,))

    def test_rejects_structured_input(self):
        sv = _sv(EpistemicTier.STRUCTURED)
        prec = PreconditionCheck(name="axiom_1", holds=True, evidence="verified")
        with self.assertRaises(P0Incident):
            promote_to_proven(
                sv, theorem="x=x", preconditions=[prec], approver="test", store=self.store
            )

    def test_rejects_failing_preconditions(self):
        sv = _sv(EpistemicTier.MEASURED)
        prec = PreconditionCheck(name="axiom_1", holds=False, evidence="failed")
        with self.assertRaises(P0Incident):
            promote_to_proven(
                sv, theorem="x=x", preconditions=[prec], approver="test", store=self.store
            )

    def test_persists_record(self):
        sv = _sv(EpistemicTier.MEASURED)
        prec = PreconditionCheck(name="axiom_1", holds=True, evidence="verified")
        promote_to_proven(
            sv, theorem="x=x", preconditions=[prec], approver="test", store=self.store
        )
        self.assertEqual(self.store.size, 1)


class TestNoSkipping(unittest.TestCase):
    """Tier skipping is always P0, regardless of direction."""

    def test_intuited_cannot_skip_to_measured(self):
        sv = _sv(EpistemicTier.INTUITED)
        with self.assertRaises(P0Incident):
            promote_to_measured(
                sv,
                sample_size=50,
                confidence_interval=(0.90, 0.99),
                held_out_validation=0.2,
                drift_monitor_id="dm-001",
                approver="test",
            )

    def test_intuited_cannot_skip_to_proven(self):
        sv = _sv(EpistemicTier.INTUITED)
        prec = PreconditionCheck(name="axiom_1", holds=True, evidence="verified")
        with self.assertRaises(P0Incident):
            promote_to_proven(
                sv, theorem="x=x", preconditions=[prec], approver="test"
            )

    def test_structured_cannot_skip_to_proven(self):
        sv = _sv(EpistemicTier.STRUCTURED)
        prec = PreconditionCheck(name="axiom_1", holds=True, evidence="verified")
        with self.assertRaises(P0Incident):
            promote_to_proven(
                sv, theorem="x=x", preconditions=[prec], approver="test"
            )


if __name__ == "__main__":
    unittest.main()

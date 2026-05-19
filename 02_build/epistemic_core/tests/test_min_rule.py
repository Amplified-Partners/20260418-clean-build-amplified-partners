"""
Tests for the min-rule — the Layer 0 invariant.

Tests that:
- min-rule cannot promote
- effective_status computes correctly
- staleness demotes
- failed preconditions demote
- bare untiered values cannot cross boundaries (type enforcement)
- demote floors at INTUITED

Signed-by: Devon-d493 | 2026-05-19 | devin-d49302e4179d43d0892997a7f3a9f57f
"""

from __future__ import annotations

import datetime as dt
import unittest

from epistemic_core.tiers import EpistemicTier
from epistemic_core.min_rule import (
    StatusedValue,
    Provenance,
    PreconditionCheck,
    effective_status,
    demote,
    tier_min,
    tier_min_many,
    tier_min_str,
    tier_min_many_str,
)


def _prov(layer: str = "test") -> Provenance:
    return Provenance(layer=layer, method="test_method")


def _sv(
    tier: EpistemicTier = EpistemicTier.STRUCTURED,
    *,
    valid_until: dt.datetime | None = None,
    preconditions: tuple[PreconditionCheck, ...] = (),
) -> StatusedValue:
    return StatusedValue(
        value=42,
        status=tier,
        provenance=_prov(),
        valid_until=valid_until,
        preconditions=preconditions,
    )


class TestDemote(unittest.TestCase):
    def test_proven_to_measured(self):
        self.assertEqual(demote(EpistemicTier.PROVEN), EpistemicTier.MEASURED)

    def test_measured_to_structured(self):
        self.assertEqual(demote(EpistemicTier.MEASURED), EpistemicTier.STRUCTURED)

    def test_structured_to_intuited(self):
        self.assertEqual(demote(EpistemicTier.STRUCTURED), EpistemicTier.INTUITED)

    def test_intuited_floors_at_intuited(self):
        self.assertEqual(demote(EpistemicTier.INTUITED), EpistemicTier.INTUITED)


class TestEffectiveStatus(unittest.TestCase):
    def test_own_claim_alone(self):
        result = effective_status(EpistemicTier.STRUCTURED)
        self.assertEqual(result, EpistemicTier.STRUCTURED)

    def test_input_floor_demotes(self):
        result = effective_status(
            EpistemicTier.MEASURED,
            input_statuses=[EpistemicTier.INTUITED],
        )
        self.assertEqual(result, EpistemicTier.INTUITED)

    def test_multiple_inputs_takes_min(self):
        result = effective_status(
            EpistemicTier.PROVEN,
            input_statuses=[EpistemicTier.MEASURED, EpistemicTier.STRUCTURED],
        )
        self.assertEqual(result, EpistemicTier.STRUCTURED)

    def test_failed_precondition_demotes(self):
        prec = PreconditionCheck(name="freshness", holds=False, evidence="test")
        result = effective_status(
            EpistemicTier.MEASURED,
            preconditions=[prec],
        )
        self.assertEqual(result, EpistemicTier.STRUCTURED)

    def test_passing_precondition_no_demotion(self):
        prec = PreconditionCheck(name="freshness", holds=True, evidence="test")
        result = effective_status(
            EpistemicTier.MEASURED,
            preconditions=[prec],
        )
        self.assertEqual(result, EpistemicTier.MEASURED)

    def test_staleness_demotes(self):
        result = effective_status(
            EpistemicTier.MEASURED,
            is_stale=True,
        )
        self.assertEqual(result, EpistemicTier.STRUCTURED)

    def test_cannot_promote(self):
        """The min-rule can never produce a tier higher than own_claim."""
        for claim in EpistemicTier:
            for inp in EpistemicTier:
                result = effective_status(claim, input_statuses=[inp])
                self.assertLessEqual(result, claim)
                self.assertLessEqual(result, inp)

    def test_all_factors_combine(self):
        prec = PreconditionCheck(name="test", holds=False, evidence="test")
        result = effective_status(
            EpistemicTier.PROVEN,
            input_statuses=[EpistemicTier.MEASURED],
            preconditions=[prec],
            is_stale=True,
        )
        # own=PROVEN, input=MEASURED, prec_fail=demote(PROVEN)=MEASURED, stale=demote(PROVEN)=MEASURED
        self.assertEqual(result, EpistemicTier.MEASURED)


class TestStatusedValue(unittest.TestCase):
    def test_effective_status_delegates(self):
        sv = _sv(EpistemicTier.MEASURED)
        result = sv.effective_status([EpistemicTier.INTUITED])
        self.assertEqual(result, EpistemicTier.INTUITED)

    def test_stale_value_demotes(self):
        past = dt.datetime(2020, 1, 1, tzinfo=dt.timezone.utc)
        sv = _sv(EpistemicTier.MEASURED, valid_until=past)
        self.assertTrue(sv.is_stale())
        result = sv.effective_status()
        self.assertEqual(result, EpistemicTier.STRUCTURED)

    def test_non_stale_value_unchanged(self):
        future = dt.datetime(2099, 1, 1, tzinfo=dt.timezone.utc)
        sv = _sv(EpistemicTier.MEASURED, valid_until=future)
        self.assertFalse(sv.is_stale())
        result = sv.effective_status()
        self.assertEqual(result, EpistemicTier.MEASURED)

    def test_no_expiry_never_stale(self):
        sv = _sv(EpistemicTier.PROVEN)
        self.assertFalse(sv.is_stale())

    def test_precondition_failure_demotes(self):
        prec = PreconditionCheck(name="test", holds=False, evidence="test")
        sv = _sv(EpistemicTier.STRUCTURED, preconditions=(prec,))
        result = sv.effective_status()
        self.assertEqual(result, EpistemicTier.INTUITED)


class TestTierMin(unittest.TestCase):
    def test_tier_min_returns_lower(self):
        self.assertEqual(
            tier_min(EpistemicTier.PROVEN, EpistemicTier.INTUITED),
            EpistemicTier.INTUITED,
        )

    def test_tier_min_same(self):
        self.assertEqual(
            tier_min(EpistemicTier.MEASURED, EpistemicTier.MEASURED),
            EpistemicTier.MEASURED,
        )

    def test_tier_min_many_empty(self):
        self.assertEqual(tier_min_many([]), EpistemicTier.PROVEN)

    def test_tier_min_many_finds_lowest(self):
        tiers = [EpistemicTier.PROVEN, EpistemicTier.STRUCTURED, EpistemicTier.MEASURED]
        self.assertEqual(tier_min_many(tiers), EpistemicTier.STRUCTURED)


class TestTierMinStr(unittest.TestCase):
    """Backward compat with brain_curator string-based tiers."""

    def test_str_min(self):
        self.assertEqual(tier_min_str("PROVEN", "INTUITED"), "INTUITED")

    def test_str_min_same(self):
        self.assertEqual(tier_min_str("MEASURED", "MEASURED"), "MEASURED")

    def test_str_min_many_empty(self):
        self.assertEqual(tier_min_many_str([]), "PROVEN")

    def test_str_min_many(self):
        self.assertEqual(
            tier_min_many_str(["PROVEN", "STRUCTURED", "MEASURED"]),
            "STRUCTURED",
        )


if __name__ == "__main__":
    unittest.main()

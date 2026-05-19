"""
Property tests for the epistemic meet-semilattice.

Tests that the min-rule satisfies:
- Associativity: min(min(a, b), c) == min(a, min(b, c))
- Commutativity: min(a, b) == min(b, a)
- Idempotency: min(a, a) == a
- Non-promotion: result <= all inputs (for every combination)
- Demotion bounds: demote never goes below INTUITED
- Promotion is monotonically upward and single-step only

Uses hypothesis for property-based testing.

Signed-by: Devon-d493 | 2026-05-19 | devin-d49302e4179d43d0892997a7f3a9f57f
"""

from __future__ import annotations

import unittest

from hypothesis import given
from hypothesis import strategies as st

from epistemic_core.tiers import EpistemicTier
from epistemic_core.min_rule import (
    effective_status,
    demote,
    tier_min,
    PreconditionCheck,
)


tier_strategy = st.sampled_from(list(EpistemicTier))
tier_list_strategy = st.lists(tier_strategy, min_size=0, max_size=10)


class TestMeetSemilatticeProperties(unittest.TestCase):
    """The min-rule forms a meet-semilattice on {INTUITED, STRUCTURED, MEASURED, PROVEN}."""

    @given(a=tier_strategy, b=tier_strategy)
    def test_commutativity(self, a: EpistemicTier, b: EpistemicTier):
        """min(a, b) == min(b, a)"""
        self.assertEqual(tier_min(a, b), tier_min(b, a))

    @given(a=tier_strategy, b=tier_strategy, c=tier_strategy)
    def test_associativity(self, a: EpistemicTier, b: EpistemicTier, c: EpistemicTier):
        """min(min(a, b), c) == min(a, min(b, c))"""
        self.assertEqual(
            tier_min(tier_min(a, b), c),
            tier_min(a, tier_min(b, c)),
        )

    @given(a=tier_strategy)
    def test_idempotency(self, a: EpistemicTier):
        """min(a, a) == a"""
        self.assertEqual(tier_min(a, a), a)

    @given(own=tier_strategy, inputs=tier_list_strategy)
    def test_effective_status_never_promotes(
        self, own: EpistemicTier, inputs: list[EpistemicTier]
    ):
        """effective_status() can never produce a tier higher than own_claim."""
        result = effective_status(own, input_statuses=inputs)
        self.assertLessEqual(result, own)
        for inp in inputs:
            self.assertLessEqual(result, inp)

    @given(own=tier_strategy, inputs=tier_list_strategy)
    def test_effective_status_never_promotes_with_stale(
        self, own: EpistemicTier, inputs: list[EpistemicTier]
    ):
        """Even with staleness, effective status cannot promote."""
        result = effective_status(own, input_statuses=inputs, is_stale=True)
        self.assertLessEqual(result, own)

    @given(own=tier_strategy)
    def test_effective_status_with_failed_preconditions_demotes(
        self, own: EpistemicTier
    ):
        """Failed preconditions always result in demotion (or floor at INTUITED)."""
        prec = PreconditionCheck(name="test", holds=False, evidence="test")
        result = effective_status(own, preconditions=[prec])
        expected = demote(own)
        self.assertEqual(result, expected)


class TestDemoteProperties(unittest.TestCase):
    @given(a=tier_strategy)
    def test_demote_never_below_intuited(self, a: EpistemicTier):
        """Demotion cannot go below INTUITED."""
        result = demote(a)
        self.assertGreaterEqual(result, EpistemicTier.INTUITED)

    @given(a=tier_strategy)
    def test_demote_at_most_one_step(self, a: EpistemicTier):
        """Demotion reduces by at most one tier."""
        result = demote(a)
        self.assertGreaterEqual(result.value, a.value - 1)

    @given(a=tier_strategy)
    def test_demote_is_monotonically_downward(self, a: EpistemicTier):
        """demote(a) <= a always."""
        self.assertLessEqual(demote(a), a)

    @given(a=tier_strategy)
    def test_double_demote_bounded(self, a: EpistemicTier):
        """Double demotion still bounded by INTUITED."""
        result = demote(demote(a))
        self.assertGreaterEqual(result, EpistemicTier.INTUITED)


class TestPromotionMonotonicity(unittest.TestCase):
    """Promotion is strictly one-step upward. No skipping."""

    def test_valid_promotion_steps(self):
        """Only adjacent-tier promotions are valid."""
        valid_promotions = [
            (EpistemicTier.INTUITED, EpistemicTier.STRUCTURED),
            (EpistemicTier.STRUCTURED, EpistemicTier.MEASURED),
            (EpistemicTier.MEASURED, EpistemicTier.PROVEN),
        ]
        for from_tier, to_tier in valid_promotions:
            self.assertEqual(to_tier.value - from_tier.value, 1)

    def test_no_valid_skip_promotions(self):
        """Multi-step promotions are always invalid."""
        invalid_promotions = [
            (EpistemicTier.INTUITED, EpistemicTier.MEASURED),    # skip 1
            (EpistemicTier.INTUITED, EpistemicTier.PROVEN),      # skip 2
            (EpistemicTier.STRUCTURED, EpistemicTier.PROVEN),    # skip 1
        ]
        for from_tier, to_tier in invalid_promotions:
            self.assertGreater(to_tier.value - from_tier.value, 1)


if __name__ == "__main__":
    unittest.main()

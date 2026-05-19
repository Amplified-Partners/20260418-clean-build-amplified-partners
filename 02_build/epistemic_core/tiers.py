"""
Canonical epistemic tier definitions — the single source of truth.

Four tiers of honest knowledge claim. Order matters: min() works
because IntEnum. This is the Layer 0 law.

All other modules (routing, shapes, vellum gate, brain_curator)
MUST import from here. No local copies.

Signed-by: Devon-d493 | 2026-05-19 | devin-d49302e4179d43d0892997a7f3a9f57f
"""

from __future__ import annotations

import enum


class EpistemicTier(enum.IntEnum):
    """Four tiers of honest knowledge claim. Order matters: min() works."""

    INTUITED = 1       # Vibe with footnotes (raw LLM output, gut, narrative)
    STRUCTURED = 2     # Honest heuristic (reproducible rule, judgement weights)
    MEASURED = 3       # Empirically calibrated (data + CI + sample size + drift monitor)
    PROVEN = 4         # Mathematically proven (closed form + verified preconditions)

    def label(self) -> str:
        return {1: "intuited", 2: "structured", 3: "measured", 4: "proven"}[self.value]

    @classmethod
    def from_string(cls, s: str) -> EpistemicTier:
        mapping = {
            "intuited": cls.INTUITED,
            "structured": cls.STRUCTURED,
            "measured": cls.MEASURED,
            "proven": cls.PROVEN,
        }
        key = s.lower().strip()
        if key not in mapping:
            raise ValueError(f"Unknown epistemic tier: {s!r}. Valid: {list(mapping)}")
        return mapping[key]

    @classmethod
    def from_rank(cls, rank: int) -> EpistemicTier:
        """Convert integer rank (1-4) to tier. Raises ValueError if out of range."""
        if rank not in (1, 2, 3, 4):
            raise ValueError(f"Tier rank must be 1-4, got {rank}")
        return cls(rank)


# Tier string constants for backward compat with brain_curator
TIER_INTUITED = "INTUITED"
TIER_STRUCTURED = "STRUCTURED"
TIER_MEASURED = "MEASURED"
TIER_PROVEN = "PROVEN"

TIER_RANK: dict[str, int] = {
    TIER_INTUITED: 1,
    TIER_STRUCTURED: 2,
    TIER_MEASURED: 3,
    TIER_PROVEN: 4,
}


def tier_from_string_constant(s: str) -> EpistemicTier:
    """Convert string constant (e.g. 'INTUITED') to EpistemicTier."""
    return EpistemicTier.from_string(s)


def tier_to_string_constant(tier: EpistemicTier) -> str:
    """Convert EpistemicTier to string constant (e.g. 'INTUITED')."""
    return tier.name

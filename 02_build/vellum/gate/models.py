"""Domain models for the Vellum Pattern Transfer Gate.

Pure domain logic. No I/O, no database, no LLM calls.
All models are Pydantic v2. Immutable where possible.

EpistemicStatus is imported from epistemic_core (single source of truth).

Devon-b5dc | 2026-05-14
Refactored by Devon-d493 | 2026-05-19 | devin-d49302e4179d43d0892997a7f3a9f57f
  — import EpistemicStatus from epistemic_core (consolidation PR 1)
"""

from __future__ import annotations

import enum
from typing import Literal

from pydantic import BaseModel, Field

from epistemic_core.tiers import EpistemicTier as EpistemicStatus


# ---------------------------------------------------------------------------
# TrustState — outcome of a gate decision.
# ---------------------------------------------------------------------------


class TrustState(str, enum.Enum):
    """Trust state assigned by the pattern transfer gate."""

    REJECTED = "REJECTED"
    QUARANTINED = "QUARANTINED"
    VALIDATED = "VALIDATED"
    APPROVED_FOR_TEST = "APPROVED_FOR_TEST"


# ---------------------------------------------------------------------------
# PuddingLabel — the 4-slot structural taxonomy (WHAT.HOW.SCALE.TIME).
# 2,058 possible labels (7x7x7x6).
# ---------------------------------------------------------------------------


class PuddingLabel(BaseModel):
    """PUDDING 2026 label: WHAT.HOW.SCALE.TIME.

    Neutral taxonomy applied at ingestion. Describes what content IS,
    not what you want it to be.
    """

    what: str = Field(description="Content type (7 options)")
    how: str = Field(description="Methodology (7 options)")
    scale: str = Field(description="Scale of application (7 options)")
    time: str = Field(description="Temporal nature (6 options)")

    def slots(self) -> tuple[str, str, str, str]:
        return (self.what, self.how, self.scale, self.time)

    def code(self) -> str:
        return f"{self.what}.{self.how}.{self.scale}.{self.time}"


# ---------------------------------------------------------------------------
# AMPSScore — composite process performance score.
# ---------------------------------------------------------------------------


class AMPSScore(BaseModel):
    """AMPS composite score for a business process.

    0.0 = worst, 10.0 = best. Carries its own epistemic status
    and measured cycle count.
    """

    composite_score: float = Field(..., ge=0.0, le=10.0)
    epistemic_status: EpistemicStatus
    measured_cycles: int = Field(0, ge=0)


# ---------------------------------------------------------------------------
# BusinessProcess — the thing being assessed or improved.
# ---------------------------------------------------------------------------


class BusinessProcess(BaseModel):
    """A business process with current state and PUDDING classification."""

    process_id: str
    client_namespace: str
    name: str
    pudding_label: PuddingLabel
    current_amps: AMPSScore
    bounded_or_creative: Literal["BOUNDED", "CREATIVE"]


# ---------------------------------------------------------------------------
# ImprovementPattern — a reusable candidate intervention.
# ---------------------------------------------------------------------------


class ImprovementPattern(BaseModel):
    """A reusable improvement pattern derived from a previous DC-7 cycle
    or measured change. The thing being transferred is the improvement
    pattern, not the source process.
    """

    pattern_id: str
    source_process_id: str
    source_client_namespace: str
    description: str
    source_label: PuddingLabel
    before_amps: AMPSScore
    after_amps: AMPSScore
    evidence_status: EpistemicStatus
    contains_client_sensitive_detail: bool = False
    allowed_for_cross_client_learning: bool = False


# ---------------------------------------------------------------------------
# BridgeDecision — the gate output. Typed, auditable, reason-coded.
# ---------------------------------------------------------------------------


class BridgeDecision(BaseModel):
    """Output of evaluate_bridge_candidate().

    Every decision carries:
    - The verdict (REJECT / QUARANTINE / ESCALATE / APPROVE_FOR_DC7_TEST)
    - Trust state
    - Reason codes (explicit, machine-readable)
    - PUDDING slot match score
    - AMPS delta (improvement magnitude)
    - Effective epistemic status (min-rule applied)
    - Recommended action (human-readable)
    """

    decision: Literal[
        "REJECT",
        "QUARANTINE",
        "APPROVE_FOR_DC7_TEST",
        "ESCALATE_FOR_REVIEW",
    ]
    trust_state: TrustState
    reason_codes: list[str]
    slot_match_score: float
    amps_delta: float
    effective_status: EpistemicStatus
    action: str | None = None

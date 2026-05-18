"""Ingestion gate — decides what enters the Brain's long-term memory.

Rule: "Save it only if it changes future behaviour." — Ewan Bramley

The gate filters memory candidates. It admits items that will change
how agents work in the future. It rejects trivia, session-only
ephemera, raw dumps, obvious/searchable facts, and unvalidated
reflections.

The gate does NOT promote. Promotion happens outside the gate,
through the spine's review process (Ewan or the Enforcer).

Devon-58ca | 2026-05-18
"""

from __future__ import annotations

import logging
from datetime import datetime, timezone

from vellum.models.memory import (
    CandidateKind,
    GateDecision,
    GateVerdict,
    MemoryCandidate,
)

log = logging.getLogger("vellum.ingestion_gate")

# Minimum confidence to pass the gate
_CONFIDENCE_FLOOR = 0.5

# Minimum content length (characters) — below this is trivia
_MIN_CONTENT_LENGTH = 20

# Maximum content length — above this is a raw dump, needs summarisation
_MAX_CONTENT_LENGTH = 5000

# Kinds that are high-signal (lower bar to admit)
_HIGH_SIGNAL_KINDS: set[CandidateKind] = {
    "correction",
    "failed_approach",
    "if_then_lesson",
    "explicit_remember",
    "procedure_improvement",
}

# Kinds that are lower-signal (higher bar)
_LOW_SIGNAL_KINDS: set[CandidateKind] = {
    "preference",
    "new_entity",
    "task_outcome",
}

# Reject patterns — content that should never enter memory
_REJECT_PHRASES = [
    "hello",
    "hi there",
    "thanks",
    "thank you",
    "no problem",
    "sounds good",
    "ok",
    "acknowledged",
    "got it",
    "will do",
]


def evaluate_candidate(candidate: MemoryCandidate) -> GateDecision:
    """Evaluate a single memory candidate against the ingestion gate.

    Returns a GateDecision with verdict: ADMIT, REJECT, or QUARANTINE.
    """
    reason_codes: list[str] = []
    content_lower = candidate.content.lower().strip()

    # Gate 1: Confidence floor
    if candidate.confidence < _CONFIDENCE_FLOOR:
        return GateDecision(
            candidate_id=candidate.id,
            verdict="REJECT",
            reason_codes=["confidence_below_floor"],
            changes_future_behaviour=False,
            epistemic_tier=candidate.epistemic_tier,
        )

    # Gate 2: Trivial content (too short)
    if len(candidate.content.strip()) < _MIN_CONTENT_LENGTH:
        return GateDecision(
            candidate_id=candidate.id,
            verdict="REJECT",
            reason_codes=["content_too_short_trivia"],
            changes_future_behaviour=False,
            epistemic_tier=candidate.epistemic_tier,
        )

    # Gate 3: Social pleasantries / noise
    if any(phrase in content_lower for phrase in _REJECT_PHRASES):
        return GateDecision(
            candidate_id=candidate.id,
            verdict="REJECT",
            reason_codes=["social_pleasantry_noise"],
            changes_future_behaviour=False,
            epistemic_tier=candidate.epistemic_tier,
        )

    # Gate 4: Raw dump (too long without summarisation)
    if len(candidate.content) > _MAX_CONTENT_LENGTH:
        return GateDecision(
            candidate_id=candidate.id,
            verdict="QUARANTINE",
            reason_codes=["raw_dump_needs_summarisation"],
            changes_future_behaviour=True,
            epistemic_tier=candidate.epistemic_tier,
        )

    # Gate 5: High-signal kinds get admitted with lower bar
    if candidate.kind in _HIGH_SIGNAL_KINDS:
        reason_codes.append("high_signal_kind")
        reason_codes.append(f"kind_{candidate.kind}")
        return GateDecision(
            candidate_id=candidate.id,
            verdict="ADMIT",
            reason_codes=reason_codes,
            changes_future_behaviour=True,
            epistemic_tier=candidate.epistemic_tier,
        )

    # Gate 6: Low-signal kinds need higher confidence
    if candidate.kind in _LOW_SIGNAL_KINDS:
        if candidate.confidence < 0.7:
            return GateDecision(
                candidate_id=candidate.id,
                verdict="REJECT",
                reason_codes=["low_signal_kind_insufficient_confidence"],
                changes_future_behaviour=False,
                epistemic_tier=candidate.epistemic_tier,
            )

    # Default: admit if it passed all rejection gates
    reason_codes.append("passed_all_gates")
    reason_codes.append(f"kind_{candidate.kind}")
    return GateDecision(
        candidate_id=candidate.id,
        verdict="ADMIT",
        reason_codes=reason_codes,
        changes_future_behaviour=True,
        epistemic_tier=candidate.epistemic_tier,
    )


def run_gate(candidates: list[MemoryCandidate]) -> list[GateDecision]:
    """Run the ingestion gate on a batch of candidates.

    Returns a GateDecision for each candidate.
    """
    decisions: list[GateDecision] = []
    admitted = 0
    rejected = 0
    quarantined = 0

    for candidate in candidates:
        decision = evaluate_candidate(candidate)
        decisions.append(decision)
        if decision.verdict == "ADMIT":
            admitted += 1
        elif decision.verdict == "REJECT":
            rejected += 1
        else:
            quarantined += 1

    log.info(
        "Ingestion gate: %d candidates → %d admitted, %d rejected, %d quarantined",
        len(candidates),
        admitted,
        rejected,
        quarantined,
    )
    return decisions

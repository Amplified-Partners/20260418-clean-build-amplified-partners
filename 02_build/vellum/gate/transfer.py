"""Pattern Transfer Gate — the core decision function.

Pure domain logic. No I/O. Every decision returns reason codes.
Every output carries its effective epistemic status via the min-rule.

The min-rule: output status = min(all input statuses).
A function may not claim a higher tier than its lowest-tier input.

Devon-b5dc | 2026-05-14
"""

from __future__ import annotations

from vellum.gate.models import (
    BridgeDecision,
    BusinessProcess,
    EpistemicStatus,
    ImprovementPattern,
    PuddingLabel,
    TrustState,
)


# ---------------------------------------------------------------------------
# PUDDING slot match — structural similarity between two labels.
# ---------------------------------------------------------------------------


def calculate_slot_match_score(
    label_a: PuddingLabel,
    label_b: PuddingLabel,
) -> float:
    """Compare two PUDDING labels slot-by-slot. Returns 0.0 to 1.0.

    4 slots: WHAT, HOW, SCALE, TIME. Each matching slot = 0.25.
    """
    matches = sum(
        1 for a, b in zip(label_a.slots(), label_b.slots())
        if a == b
    )
    return matches / 4


# ---------------------------------------------------------------------------
# AMPS delta — improvement magnitude.
# ---------------------------------------------------------------------------


def calculate_amps_delta(pattern: ImprovementPattern) -> float:
    """Difference between after and before AMPS scores."""
    return pattern.after_amps.composite_score - pattern.before_amps.composite_score


# ---------------------------------------------------------------------------
# Min-rule helper.
# ---------------------------------------------------------------------------


def min_status(*statuses: EpistemicStatus) -> EpistemicStatus:
    """The min-rule: effective status is the minimum of all inputs."""
    return EpistemicStatus(min(statuses))


# ---------------------------------------------------------------------------
# The gate function — the only public entry point.
# ---------------------------------------------------------------------------


def evaluate_bridge_candidate(
    pattern: ImprovementPattern,
    target: BusinessProcess,
) -> BridgeDecision:
    """Decide whether an improvement pattern is safe to test in a new context.

    Gate logic (ordered by severity):
    1. Client-sensitive detail → QUARANTINE (privacy first)
    2. Cross-client learning not authorised → REJECT
    3. PUDDING shape match below threshold → REJECT
    4. Evidence status below MEASURED → ESCALATE (human review)
    5. No positive AMPS delta → REJECT (nothing to transfer)
    6. Target already at or above source outcome → REJECT (no headroom)
    7. All gates pass → APPROVE_FOR_DC7_TEST

    The effective_status is computed via the min-rule across:
    - pattern.evidence_status
    - pattern.after_amps.epistemic_status
    - target.current_amps.epistemic_status
    - STRUCTURED ceiling (this gate is itself a structured heuristic)
    """
    slot_match = calculate_slot_match_score(
        pattern.source_label,
        target.pudding_label,
    )
    amps_delta = calculate_amps_delta(pattern)

    # Min-rule: the effective status is the lowest of all relevant inputs.
    effective = min_status(
        pattern.evidence_status,
        pattern.after_amps.epistemic_status,
        target.current_amps.epistemic_status,
        EpistemicStatus.STRUCTURED,  # gate logic itself is STRUCTURED
    )

    # --- Gate 1: Privacy ---
    if pattern.contains_client_sensitive_detail:
        return BridgeDecision(
            decision="QUARANTINE",
            trust_state=TrustState.QUARANTINED,
            reason_codes=["pattern_contains_client_sensitive_detail"],
            slot_match_score=slot_match,
            amps_delta=amps_delta,
            effective_status=effective,
            action="Strip or abstract client-sensitive detail before reuse.",
        )

    # --- Gate 2: Cross-client learning authorisation ---
    if not pattern.allowed_for_cross_client_learning:
        return BridgeDecision(
            decision="REJECT",
            trust_state=TrustState.REJECTED,
            reason_codes=["cross_client_learning_not_authorised"],
            slot_match_score=slot_match,
            amps_delta=amps_delta,
            effective_status=effective,
            action=None,
        )

    # --- Gate 3: Shape similarity threshold ---
    if slot_match < 0.75:
        return BridgeDecision(
            decision="REJECT",
            trust_state=TrustState.REJECTED,
            reason_codes=["shape_similarity_below_threshold"],
            slot_match_score=slot_match,
            amps_delta=amps_delta,
            effective_status=effective,
            action=None,
        )

    # --- Gate 4: Evidence floor ---
    if pattern.evidence_status < EpistemicStatus.MEASURED:
        return BridgeDecision(
            decision="ESCALATE_FOR_REVIEW",
            trust_state=TrustState.VALIDATED,
            reason_codes=["pattern_not_measured_enough_for_autonomous_test"],
            slot_match_score=slot_match,
            amps_delta=amps_delta,
            effective_status=effective,
            action="Human or architect review required before DC-7 test.",
        )

    # --- Gate 5: Positive delta required ---
    if amps_delta <= 0:
        return BridgeDecision(
            decision="REJECT",
            trust_state=TrustState.REJECTED,
            reason_codes=["source_pattern_has_no_positive_measured_delta"],
            slot_match_score=slot_match,
            amps_delta=amps_delta,
            effective_status=effective,
            action=None,
        )

    # --- Gate 6: Target headroom ---
    if target.current_amps.composite_score >= pattern.after_amps.composite_score:
        return BridgeDecision(
            decision="REJECT",
            trust_state=TrustState.REJECTED,
            reason_codes=["target_already_at_or_above_source_after_score"],
            slot_match_score=slot_match,
            amps_delta=amps_delta,
            effective_status=effective,
            action=None,
        )

    # --- All gates pass ---
    return BridgeDecision(
        decision="APPROVE_FOR_DC7_TEST",
        trust_state=TrustState.APPROVED_FOR_TEST,
        reason_codes=[
            "shape_similarity_sufficient",
            "source_pattern_has_positive_measured_delta",
            "target_has_improvement_headroom",
            "cross_client_learning_authorised",
        ],
        slot_match_score=slot_match,
        amps_delta=amps_delta,
        effective_status=effective,
        action=f"Create DC-7 test plan for {target.process_id}. Do not deploy without validation.",
    )

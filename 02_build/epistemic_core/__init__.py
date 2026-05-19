"""
epistemic_core — canonical source of truth for the Layer 0 invariant.

Every value in the Amplified substrate wears its epistemic tier.
Every boundary enforces the min-rule. Every violation halts the system.

This module consolidates the previously-triplicated definitions from
routing/epistemic_status.py, shapes/_epistemic.py, and vellum/gate/models.py
into a single canonical import.

Signed-by: Devon-d493 | 2026-05-19 | devin-d49302e4179d43d0892997a7f3a9f57f
"""

from epistemic_core.tiers import EpistemicTier
from epistemic_core.min_rule import (
    StatusedValue,
    Provenance,
    PreconditionCheck,
    effective_status,
    demote,
)
from epistemic_core.p0_policy import (
    P0Incident,
    P0Policy,
    ACTIVE_P0_POLICY,
    enforce_p0,
)
from epistemic_core.promotion import (
    PromotionRecord,
    promote_to_structured,
    promote_to_measured,
    promote_to_proven,
)
from epistemic_core.audit import (
    AuditLog,
    StatusRecord,
)
from epistemic_core.drift import (
    DriftDetector,
    DriftSignal,
)
from epistemic_core.context_packet import (
    ContextPacket,
    CanonicalRefs,
    RuntimeBlock,
    CuratorBlock,
    PuddingBlock,
    PermissionsBlock,
    packet_to_context,
    context_to_frontmatter,
)
from epistemic_core.vellum_event import VellumEvent
from epistemic_core.vellum_emitter import (
    VellumEmitter,
    VellumStore,
    MemoryVellumStore,
    JSONLBuffer,
    ReconcilerResult,
    reconcile,
)

# Backward compat alias — routing/ and vellum/ use EpistemicStatus
EpistemicStatus = EpistemicTier

__all__ = [
    # Tiers
    "EpistemicTier",
    "EpistemicStatus",  # backward compat alias
    # Min-rule
    "StatusedValue",
    "Provenance",
    "PreconditionCheck",
    "effective_status",
    "demote",
    # P0
    "P0Incident",
    "P0Policy",
    "ACTIVE_P0_POLICY",
    "enforce_p0",
    # Promotion
    "PromotionRecord",
    "promote_to_structured",
    "promote_to_measured",
    "promote_to_proven",
    # Audit
    "AuditLog",
    "StatusRecord",
    # Drift
    "DriftDetector",
    "DriftSignal",
    # Context Packet (PR 3)
    "ContextPacket",
    "CanonicalRefs",
    "RuntimeBlock",
    "CuratorBlock",
    "PuddingBlock",
    "PermissionsBlock",
    "packet_to_context",
    "context_to_frontmatter",
    # Vellum witnessing (PR 5)
    "VellumEvent",
    "VellumEmitter",
    "VellumStore",
    "MemoryVellumStore",
    "JSONLBuffer",
    "ReconcilerResult",
    "reconcile",
]

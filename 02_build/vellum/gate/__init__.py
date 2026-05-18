"""Vellum Pattern Transfer Gate — decides whether improvement patterns
are safe to test in new contexts.

PUDDING match authorises investigation.
Measured improvement authorises a test.
Validated DC-7 results authorise promotion.
Nothing skips the evidence ladder.

Devon-b5dc | 2026-05-14
"""

from vellum.gate.models import (
    BusinessProcess,
    BridgeDecision,
    EpistemicStatus,
    ImprovementPattern,
    PuddingLabel,
    TrustState,
)
from vellum.gate.transfer import evaluate_bridge_candidate

__all__ = [
    "BusinessProcess",
    "BridgeDecision",
    "EpistemicStatus",
    "ImprovementPattern",
    "PuddingLabel",
    "TrustState",
    "evaluate_bridge_candidate",
]

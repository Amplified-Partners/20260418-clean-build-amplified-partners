"""
AgentBase — the AI-powered reasoning shape.

Shape: agent | Colour: PURPLE | Position: interpretation layer
Handoff: receives via SYNC_CALL, hands off via SYNC_CALL
AI interprets. Python measures. Vellum records. Brain remembers. Human chooses.

INTUITED by default. Always. Until promoted.

Authored by Devon-58ca | 2026-05-17 | session devin-58caaceb8d3b48188ab11d10821038f1
"""

from __future__ import annotations

import logging
from typing import Any, ClassVar

from ._base import ShapeBase
from ._decorators import spine
from ._types import AgentError, HandoffProtocol, ShapeKind

log = logging.getLogger("amplified.shapes.agent")


@spine("radical_honesty", "radical_attribution", "shadow_first")
class AgentBase(ShapeBase):
    """Base class for all agent shapes.

    AI-powered reasoning. Interprets, proposes, translates.
    Respects reader-first principle. Declares confidence on every output.
    INTUITED by default — always — until a promotion gate lifts it.

    Subclasses MUST define:
        purpose: str            — interpret / translate / classify / propose / expand / compress
        model: str              — LLM model reference (e.g. "litellm:default_chain")
        reader_profile: str     — who receives the output

    Subclasses MUST implement:
        interpret(input, reader) -> result
    """

    shape_kind: ClassVar[ShapeKind] = ShapeKind.AGENT

    # --- subclass MUST define ---
    purpose: ClassVar[str] = ""  # interpret / translate / classify / propose / expand / compress
    model: ClassVar[str] = "litellm:default_chain"
    reader_profile: ClassVar[str] = ""

    # --- confidence ---
    _confidence_floor: ClassVar[float] = 0.6

    # --- epistemic: always INTUITED until promoted ---
    _epistemic_tier: ClassVar[str] = "intuited"

    # --- handoff protocol ---
    receives_via: ClassVar[HandoffProtocol] = HandoffProtocol.SYNC_CALL
    hands_off_via: ClassVar[HandoffProtocol] = HandoffProtocol.SYNC_CALL

    def interpret(self, input_data: Any, reader: Any = None) -> Any:
        """AI reasoning. Subclass implements."""
        raise NotImplementedError(
            f"{type(self).__name__}.interpret() not implemented. "
            "Agent shapes MUST implement interpret()."
        )

    def validate_confidence(self, confidence: float) -> None:
        """Reject output below confidence floor."""
        if confidence < self._confidence_floor:
            raise AgentError(
                f"{type(self).__name__}: confidence {confidence:.2f} below "
                f"floor {self._confidence_floor:.2f}. Output rejected.",
                confidence_at_failure=confidence,
            )

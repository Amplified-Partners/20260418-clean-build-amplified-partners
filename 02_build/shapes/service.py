"""
ServiceBase — a stateless container for business logic.

Shape: service | Colour: RED | Position: core logic
Handoff: receives via SYNC_CALL, hands off via SYNC_CALL
The Logic Canon lives here.

Authored by Devon-58ca | 2026-05-17 | session devin-58caaceb8d3b48188ab11d10821038f1
"""

from __future__ import annotations

import logging
from typing import Any, ClassVar

from ._base import ShapeBase
from ._decorators import spine
from ._types import HandoffProtocol, ShapeKind

log = logging.getLogger("amplified.shapes.service")


@spine("radical_honesty", "radical_attribution")
class ServiceBase(ShapeBase):
    """Base class for all service shapes.

    A stateless container for business logic. Receives typed input,
    applies business rules, returns typed output. No state between calls.

    Subclasses MUST define:
        input_model: type     — which model enters
        output_model: type    — which model exits

    Subclasses MUST implement:
        execute(input) -> output
    """

    shape_kind: ClassVar[ShapeKind] = ShapeKind.SERVICE

    # --- subclass MUST define ---
    input_model: ClassVar[type | None] = None
    output_model: ClassVar[type | None] = None

    # --- epistemic tier (set by @epistemic decorator) ---
    _epistemic_tier: ClassVar[str] = "intuited"
    _canon_ref: ClassVar[str] = ""

    # --- handoff protocol ---
    receives_via: ClassVar[HandoffProtocol] = HandoffProtocol.SYNC_CALL
    hands_off_via: ClassVar[HandoffProtocol] = HandoffProtocol.SYNC_CALL

    def execute(self, input_data: Any) -> Any:
        """Apply business logic. Subclass implements."""
        raise NotImplementedError(
            f"{type(self).__name__}.execute() not implemented. "
            "Service shapes MUST implement execute()."
        )

    def confidence(self) -> float:
        """Return confidence level for the service's output. Override if needed."""
        tier_defaults = {
            "intuited": 0.3,
            "structured": 0.6,
            "measured": 0.8,
            "proven": 0.99,
        }
        return tier_defaults.get(self._epistemic_tier, 0.3)

"""
GuardBase — the shape that validates, rejects, and stops.

Shape: guard | Colour: RED | Position: after entry, before processing
Handoff: receives via SYNC_CALL, hands off via SYNC_CALL (pass-through or reject)
The immune system. Doing nothing IS the correct output.

Authored by Devon-58ca | 2026-05-17 | session devin-58caaceb8d3b48188ab11d10821038f1
"""

from __future__ import annotations

import logging
from typing import Any, ClassVar

from ._base import ShapeBase
from ._decorators import spine
from ._types import (
    GuardHalt,
    HandoffProtocol,
    Rejection,
    Rule,
    ShapeKind,
    TrafficLight,
)

log = logging.getLogger("amplified.shapes.guard")


@spine("radical_honesty", "congruence")
class GuardBase(ShapeBase):
    """Base class for all guard shapes.

    Validates, rejects, stops. Passes valid data through unchanged.
    Rejects invalid data with clear reasons. Logs every accept and reject.
    Can halt propagation entirely (BLACK condition).

    Subclasses MUST define:
        rules: list[Rule]    — what constitutes valid input

    Subclasses MUST implement:
        check(data) -> data (unchanged) OR raise Rejection/GuardHalt
    """

    shape_kind: ClassVar[ShapeKind] = ShapeKind.GUARD

    # --- subclass MUST define ---
    rules: ClassVar[list[Rule]] = []

    # --- handoff protocol ---
    receives_via: ClassVar[HandoffProtocol] = HandoffProtocol.SYNC_CALL
    hands_off_via: ClassVar[HandoffProtocol] = HandoffProtocol.SYNC_CALL

    def check(self, data: Any) -> Any:
        """Check data against rules. Return unchanged or raise. Subclass implements."""
        raise NotImplementedError(
            f"{type(self).__name__}.check() not implemented. "
            "Guard shapes MUST implement check()."
        )

    def evaluate_rules(self, data: Any) -> list[Rule]:
        """Evaluate all rules against data. Returns list of violated rules."""
        violations: list[Rule] = []
        for rule in self.rules:
            if rule.check is not None and callable(rule.check):
                if not rule.check(data):
                    violations.append(rule)
            elif rule.pattern is not None:
                import re

                text = str(data)
                if re.search(rule.pattern, text):
                    violations.append(rule)
        return violations

    def log_accept(self, tracking_id: str) -> None:
        """Log that data passed the guard. Accepts are evidence too."""
        log.info("GUARD ACCEPT %s: tracking_id=%s", type(self).__name__, tracking_id)

    def log_reject(self, tracking_id: str, reason: str) -> None:
        """Log that data was rejected by the guard."""
        log.warning(
            "GUARD REJECT %s: tracking_id=%s reason=%s",
            type(self).__name__,
            tracking_id,
            reason,
        )

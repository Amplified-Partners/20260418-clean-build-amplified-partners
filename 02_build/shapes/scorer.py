"""
ScorerBase — the shape that measures and produces a number.

Shape: scorer | Colour: RED | Position: alongside services
Handoff: receives via SYNC_CALL, hands off via SYNC_CALL
No interrogable working, no valid answer.

Authored by Devon-58ca | 2026-05-17 | session devin-58caaceb8d3b48188ab11d10821038f1
"""

from __future__ import annotations

import logging
from typing import Any, ClassVar

from ._base import ShapeBase
from ._decorators import spine
from ._types import HandoffProtocol, ShapeKind, TrafficLight

log = logging.getLogger("amplified.shapes.scorer")


@spine("radical_transparency", "deterministic_first")
class ScorerBase(ShapeBase):
    """Base class for all scorer shapes.

    Measures and produces a number from inputs. Applies a scoring formula
    or rubric. Declares epistemic tier. Enables comparison.

    Subclasses MUST define:
        input_model: type      — what numbers/categories feed the score
        output_range: tuple    — e.g. (0, 100) or (0.0, 1.0)
        formula_ref: str       — armamentarium reference

    Subclasses MUST implement:
        score(input) -> ScorerResult
    """

    shape_kind: ClassVar[ShapeKind] = ShapeKind.SCORER

    # --- subclass MUST define ---
    input_model: ClassVar[type | None] = None
    output_range: ClassVar[tuple[float, float]] = (0.0, 1.0)
    formula_ref: ClassVar[str] = ""

    # --- epistemic tier (set by @epistemic decorator) ---
    _epistemic_tier: ClassVar[str] = "intuited"
    _canon_ref: ClassVar[str] = ""

    # --- thresholds ---
    green_threshold: ClassVar[float] = 0.7
    amber_threshold: ClassVar[float] = 0.4
    red_threshold: ClassVar[float] = 0.2

    # --- handoff protocol ---
    receives_via: ClassVar[HandoffProtocol] = HandoffProtocol.SYNC_CALL
    hands_off_via: ClassVar[HandoffProtocol] = HandoffProtocol.SYNC_CALL

    def score(self, input_data: Any) -> Any:
        """Compute the score. Subclass implements. Must show the working."""
        raise NotImplementedError(
            f"{type(self).__name__}.score() not implemented. "
            "Scorer shapes MUST implement score()."
        )

    def threshold_status(self, value: float) -> str:
        """Classify a score into GREEN / AMBER / RED / BLACK."""
        if value >= self.green_threshold:
            return TrafficLight.GREEN.value
        if value >= self.amber_threshold:
            return TrafficLight.AMBER.value
        if value >= self.red_threshold:
            return TrafficLight.RED.value
        return TrafficLight.BLACK.value

    def confidence(self) -> float:
        """Return confidence level. Override with actual mechanism."""
        tier_defaults = {
            "intuited": 0.3,
            "structured": 0.6,
            "measured": 0.8,
            "proven": 0.99,
        }
        return tier_defaults.get(self._epistemic_tier, 0.3)

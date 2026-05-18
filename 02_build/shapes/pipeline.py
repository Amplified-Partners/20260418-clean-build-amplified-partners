"""
PipelineBase — a multi-step transformation.

Shape: pipeline | Colour: YELLOW | Position: transformation layer
Handoff: receives via SYNC_CALL, hands off via SYNC_CALL
Protect the label, work the specimen.

Authored by Devon-58ca | 2026-05-17 | session devin-58caaceb8d3b48188ab11d10821038f1
"""

from __future__ import annotations

import hashlib
import json
import logging
from typing import Any, ClassVar

from ._base import ShapeBase
from ._decorators import spine
from ._types import HandoffProtocol, PipelineError, ShapeKind

log = logging.getLogger("amplified.shapes.pipeline")


@spine("radical_transparency", "deterministic_first")
class PipelineBase(ShapeBase):
    """Base class for all pipeline shapes.

    Multi-step transformation: input shape → steps → output shape.
    Each step independently testable. Whole pipeline traceable.

    Subclasses MUST define:
        input_model: type     — which model enters
        output_model: type    — which model exits

    Subclasses define steps using @step(order=N) decorator.
    """

    shape_kind: ClassVar[ShapeKind] = ShapeKind.PIPELINE

    # --- subclass MUST define ---
    input_model: ClassVar[type | None] = None
    output_model: ClassVar[type | None] = None

    # --- handoff protocol ---
    receives_via: ClassVar[HandoffProtocol] = HandoffProtocol.SYNC_CALL
    hands_off_via: ClassVar[HandoffProtocol] = HandoffProtocol.SYNC_CALL

    def run(self, input_data: Any) -> Any:
        """Execute all pipeline steps in order. Override for custom orchestration."""
        steps = self._get_ordered_steps()
        if not steps:
            raise PipelineError(
                f"{type(self).__name__}: no steps defined. "
                "Pipeline shapes must have @step decorated methods.",
            )

        current = input_data
        completed: list[str] = []
        for step_name, step_fn in steps:
            try:
                current = step_fn(current)
                completed.append(step_name)
                log.debug("PIPELINE %s: step %s complete", type(self).__name__, step_name)
            except Exception as exc:
                raise PipelineError(
                    f"Pipeline step '{step_name}' failed: {exc}",
                    step_failed=step_name,
                    steps_completed=tuple(completed),
                ) from exc
        return current

    def _get_ordered_steps(self) -> list[tuple[str, Any]]:
        """Discover and sort @step decorated methods by order."""
        steps: list[tuple[int, str, Any]] = []
        for attr_name in dir(self):
            attr = getattr(self, attr_name, None)
            if callable(attr) and getattr(attr, "_is_step", False):
                order = getattr(attr, "_step_order", 0)
                steps.append((order, attr_name, attr))
        steps.sort(key=lambda x: x[0])
        return [(name, fn) for _, name, fn in steps]

    def verify_header_hash(self, data: Any, original_hash: str | None = None) -> None:
        """Verify that metadata/header has not been modified. Protect the label."""
        header = getattr(data, "header", None)
        if header is None or original_hash is None:
            return
        current_hash = hashlib.sha256(
            json.dumps(header, default=str, sort_keys=True).encode()
        ).hexdigest()
        if current_hash != original_hash:
            raise PipelineError(
                "Metadata protection violation: header was modified. "
                "Protect the label, work the specimen.",
            )

    def hash_all(self, data: Any) -> str:
        """Hash all fields of the data for integrity verification."""
        return self.hash(data)

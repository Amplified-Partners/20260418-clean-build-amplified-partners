"""
OrchestratorBase — the coordinator that decides what runs when.

Shape: orchestrator | Colour: PURPLE | Position: coordination layer
Handoff: receives via SYNC_CALL or ASYNC_MESSAGE, hands off via SYNC_CALL
Must be thin. Only job is coordination. Never "what's right?" — only "what next?"

Authored by Devon-58ca | 2026-05-17 | session devin-58caaceb8d3b48188ab11d10821038f1
"""

from __future__ import annotations

import logging
from typing import Any, ClassVar

from ._base import ShapeBase
from ._decorators import spine
from ._types import (
    HandoffProtocol,
    ShapeKind,
    WorkflowError,
    WorkflowResult,
)

log = logging.getLogger("amplified.shapes.orchestrator")


@spine("radical_attribution", "narrow_handoff")
class OrchestratorBase(ShapeBase):
    """Base class for all orchestrator shapes.

    Coordinates what runs when. Decomposes tasks, calls shapes in order,
    handles branching, tracks progress, reports completion.

    Subclasses MUST define:
        trigger: str      — what starts this orchestrator
        timeout: str      — max workflow duration

    Subclasses MUST implement:
        run(context) -> WorkflowResult
    """

    shape_kind: ClassVar[ShapeKind] = ShapeKind.ORCHESTRATOR

    # --- subclass MUST define ---
    trigger: ClassVar[str] = ""
    timeout: ClassVar[str] = "10m"

    # --- handoff protocol ---
    receives_via: ClassVar[HandoffProtocol] = HandoffProtocol.SYNC_CALL
    hands_off_via: ClassVar[HandoffProtocol] = HandoffProtocol.SYNC_CALL

    def __init__(self) -> None:
        super().__init__()
        self._step_log: list[str] = []
        self._steps_completed = 0

    def run(self, context: Any) -> WorkflowResult:
        """Execute the workflow. Subclass implements.

        State is reset at the start of each run so instances are reusable.
        """
        self._step_log = []
        self._steps_completed = 0
        raise NotImplementedError(
            f"{type(self).__name__}.run() not implemented. "
            "Orchestrator shapes MUST implement run()."
        )

    def call(self, shape_or_method: Any, *args: Any, **kwargs: Any) -> Any:
        """Call another shape. The orchestrator's primary verb."""
        name = (
            shape_or_method.__qualname__
            if hasattr(shape_or_method, "__qualname__")
            else str(shape_or_method)
        )
        log.debug("ORCHESTRATOR %s: calling %s", type(self).__name__, name)
        self._step_log.append(name)

        if isinstance(shape_or_method, type):
            instance = shape_or_method()
            if hasattr(instance, "execute"):
                result = instance.execute(*args, **kwargs)
            elif hasattr(instance, "run"):
                result = instance.run(*args, **kwargs)
            else:
                raise WorkflowError(
                    f"Shape {name} has no execute() or run() method",
                    step_failed=name,
                    steps_completed=tuple(self._step_log[:-1]),
                )
        elif callable(shape_or_method):
            result = shape_or_method(*args, **kwargs)
        else:
            raise WorkflowError(
                f"Cannot call {name}: not callable",
                step_failed=name,
                steps_completed=tuple(self._step_log[:-1]),
            )

        self._steps_completed += 1
        return result

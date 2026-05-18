"""
WorkerBase — a background task executor.

Shape: worker | Colour: YELLOW | Position: async processing
Handoff: receives via ASYNC_MESSAGE, hands off via EVENT_EMIT

Authored by Devon-58ca | 2026-05-17 | session devin-58caaceb8d3b48188ab11d10821038f1
"""

from __future__ import annotations

import logging
from typing import Any, ClassVar

from ._base import ShapeBase
from ._decorators import spine
from ._types import HandoffProtocol, ShapeKind, WorkerResult

log = logging.getLogger("amplified.shapes.worker")


@spine("deterministic_first", "radical_transparency")
class WorkerBase(ShapeBase):
    """Base class for all worker shapes.

    Background task executor. Picks up tasks from queue or schedule,
    executes work, reports completion/failure, retries on transient failure.

    Subclasses MUST define:
        task_source: str       — queue / schedule / trigger
        retry_policy: str      — e.g. "3x_exponential"
        timeout: str           — e.g. "5m"
        concurrency: int       — max parallel instances

    Subclasses MUST implement:
        execute(task) -> WorkerResult
    """

    shape_kind: ClassVar[ShapeKind] = ShapeKind.WORKER

    # --- subclass MUST define ---
    task_source: ClassVar[str] = ""
    retry_policy: ClassVar[str] = "3x_exponential"
    timeout: ClassVar[str] = "5m"
    concurrency: ClassVar[int] = 1

    # --- handoff protocol ---
    receives_via: ClassVar[HandoffProtocol] = HandoffProtocol.ASYNC_MESSAGE
    hands_off_via: ClassVar[HandoffProtocol] = HandoffProtocol.EVENT_EMIT

    def execute(self, task: Any) -> WorkerResult:
        """Execute the background task. Subclass implements."""
        raise NotImplementedError(
            f"{type(self).__name__}.execute() not implemented. "
            "Worker shapes MUST implement execute()."
        )

    def heartbeat(self) -> bool:
        """Report that this worker is alive. Override for custom heartbeat."""
        return True

    def on_dead_letter(self, task: Any, error: Exception) -> None:
        """Handle a task that has exhausted all retries. Override to customise."""
        log.error(
            "DEAD LETTER %s: task=%s error=%s",
            type(self).__name__,
            task,
            error,
        )

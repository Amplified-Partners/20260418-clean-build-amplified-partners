"""
EntryBase — the door where data enters the system.

Shape: entry | Colour: GREEN | Position: inbound boundary
Handoff: receives via SYNC_CALL (HTTP/CLI) or ASYNC_MESSAGE (queue/webhook)
Hands off via: SYNC_CALL to guard or pipeline

Authored by Devon-58ca | 2026-05-17 | session devin-58caaceb8d3b48188ab11d10821038f1
"""

from __future__ import annotations

import logging
from typing import Any, ClassVar

from ._base import ShapeBase
from ._decorators import spine
from ._types import (
    EntryError,
    HandoffProtocol,
    ShapeKind,
    ValidatedInput,
)

log = logging.getLogger("amplified.shapes.entry")


@spine("narrow_handoff", "privacy_first")
class EntryBase(ShapeBase):
    """Base class for all entry shapes.

    The door where data enters the system. Validates shape (not content),
    timestamps arrival, assigns tracking ID, hands off to the pipe.

    Subclasses MUST define:
        source: str          — HTTP / CLI / queue / file / webhook / voice
        auth: str            — api_key / token / none / internal_only
        rate_limit: str      — e.g. "100/min"
        input_model: type    — which model validates this input
        error_model: type    — error response shape

    Subclasses MUST implement:
        receive(raw) -> ValidatedInput
    """

    shape_kind: ClassVar[ShapeKind] = ShapeKind.ENTRY

    # --- subclass MUST define ---
    source: ClassVar[str] = ""
    auth: ClassVar[str] = "none"
    rate_limit: ClassVar[str] = ""
    input_model: ClassVar[type | None] = None
    error_model: ClassVar[type | None] = None

    # --- handoff protocol ---
    receives_via: ClassVar[HandoffProtocol] = HandoffProtocol.SYNC_CALL
    hands_off_via: ClassVar[HandoffProtocol] = HandoffProtocol.SYNC_CALL

    def receive(self, raw: bytes) -> ValidatedInput:
        """Receive and validate raw input. Subclass implements."""
        raise NotImplementedError(
            f"{type(self).__name__}.receive() not implemented. "
            "Entry shapes MUST implement receive()."
        )

    def parse(self, raw: bytes) -> Any:
        """Parse raw input into the input model. Override for custom parsing."""
        if self.input_model is None:
            raise EntryError(
                f"{type(self).__name__}: no input_model defined. "
                "Entry shapes MUST define an input_model.",
                status_code=500,
            )
        import json as _json

        try:
            data = _json.loads(raw)
        except (ValueError, TypeError) as exc:
            raise EntryError(
                f"Invalid input format: {exc}",
                status_code=400,
            ) from exc

        if hasattr(self.input_model, "__dataclass_fields__"):
            try:
                return self.input_model(**data)
            except TypeError as exc:
                raise EntryError(
                    f"Input validation failed: {exc}",
                    status_code=400,
                ) from exc
        return data

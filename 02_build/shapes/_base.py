"""
ShapeBase — the common ancestor for all fifteen shapes.

Every shape in the Amplified system inherits from ShapeBase.
ShapeBase provides: tracking, timestamping, registration, and monitoring hooks.

Authored by Devon-58ca | 2026-05-17 | session devin-58caaceb8d3b48188ab11d10821038f1
"""

from __future__ import annotations

import datetime as dt
import hashlib
import json
import logging
import uuid
from typing import Any, ClassVar

from ._registry import REGISTRY
from ._types import ShapeKind, TrackingContext

log = logging.getLogger("amplified.shapes")


class ShapeBase:
    """Common ancestor for all fifteen code shapes.

    Provides:
    - Auto-registration with the shape registry
    - Tracking ID generation
    - Timestamping
    - Hash computation
    - Shape kind declaration (subclasses MUST set shape_kind)
    """

    shape_kind: ClassVar[ShapeKind]

    def __init_subclass__(cls, **kwargs: Any) -> None:
        super().__init_subclass__(**kwargs)
        if hasattr(cls, "shape_kind") and isinstance(cls.shape_kind, ShapeKind):
            REGISTRY.register_class(cls)

    def __init__(self) -> None:
        REGISTRY.register_instance(self)

    def __post_init__(self) -> None:
        """Hook for dataclass-based shapes (ModelBase, ConfigBase).

        @dataclass generates __init__ that skips ShapeBase.__init__,
        so we register the instance here instead.
        """
        REGISTRY.register_instance(self)

    @staticmethod
    def generate_id() -> str:
        """Generate a tracking ID."""
        return str(uuid.uuid4())

    @staticmethod
    def now() -> dt.datetime:
        """Current UTC timestamp."""
        return dt.datetime.now(dt.timezone.utc)

    @staticmethod
    def hash(data: Any) -> str:
        """SHA-256 hash of data for integrity verification."""
        serialised = json.dumps(data, default=str, sort_keys=True)
        return hashlib.sha256(serialised.encode()).hexdigest()

    def tracking_context(self, source_id: str = "") -> TrackingContext:
        """Create a tracking context for this shape operation."""
        return TrackingContext(
            tracking_id=self.generate_id(),
            received_at=self.now(),
            source_shape=type(self).__qualname__,
            source_id=source_id,
        )

    def verify_preconditions(self) -> tuple[Any, ...]:
        """Return precondition checks for epistemic enforcement.

        Override in subclasses to declare preconditions that affect the
        epistemic status of outputs. Default: no preconditions (empty tuple).
        Each item should be a PreconditionCheck from _epistemic module.
        """
        return ()

    def log_receipt(self, tracking_id: str) -> None:
        """Log that data was received by this shape."""
        log.info(
            "%s received: tracking_id=%s",
            type(self).__qualname__,
            tracking_id,
        )

"""
StoreBase — the interface between the system and persistence.

Shape: store | Colour: YELLOW | Position: persistence layer
Handoff: receives via SYNC_CALL, hands off via SYNC_CALL
The ONLY way to touch the database. Bottleneck on purpose.

Authored by Devon-58ca | 2026-05-17 | session devin-58caaceb8d3b48188ab11d10821038f1
"""

from __future__ import annotations

import logging
from typing import Any, ClassVar

from ._base import ShapeBase
from ._decorators import spine
from ._types import HandoffProtocol, ShapeKind, StoreError

log = logging.getLogger("amplified.shapes.store")


@spine("deterministic_first", "privacy_first")
class StoreBase(ShapeBase):
    """Base class for all store shapes.

    The interface between the system and persistence. Reads, writes,
    transactions, consistency. Abstracts the storage engine.

    Subclasses MUST define:
        engine: str     — postgresql / sqlite / redis / filesystem
        model: type     — which model defines the shape
        table: str      — table/collection/key name
    """

    shape_kind: ClassVar[ShapeKind] = ShapeKind.STORE

    # --- subclass MUST define ---
    engine: ClassVar[str] = ""
    model: ClassVar[type | None] = None
    table: ClassVar[str] = ""

    # --- handoff protocol ---
    receives_via: ClassVar[HandoffProtocol] = HandoffProtocol.SYNC_CALL
    hands_off_via: ClassVar[HandoffProtocol] = HandoffProtocol.SYNC_CALL

    def query(self, where: str, **params: Any) -> list[Any]:
        """Execute a read query. Override with actual database implementation."""
        raise NotImplementedError(
            f"{type(self).__name__}.query() not implemented. "
            "Store shapes MUST implement query()."
        )

    def get_by_id(self, record_id: str) -> Any:
        """Retrieve a single record by ID. Override with actual implementation."""
        raise NotImplementedError(
            f"{type(self).__name__}.get_by_id() not implemented."
        )

    def insert(self, record: Any) -> Any:
        """Insert a new record. Override with actual implementation."""
        raise NotImplementedError(
            f"{type(self).__name__}.insert() not implemented."
        )

    def update(self, record: Any, **fields: Any) -> Any:
        """Update fields on an existing record. Override with actual implementation."""
        raise NotImplementedError(
            f"{type(self).__name__}.update() not implemented."
        )

    def delete(self, record_id: str) -> bool:
        """Delete a record. Override with actual implementation."""
        raise NotImplementedError(
            f"{type(self).__name__}.delete() not implemented."
        )

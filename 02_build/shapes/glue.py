"""
GlueBase — the adapter that connects shapes that don't naturally fit.

Shape: glue | Colour: GREY | Position: adapts where needed
The only shape that should aspire to be deleted.
Glue that survives three months without a removal plan isn't glue — it's architecture.

Authored by Devon-58ca | 2026-05-17 | session devin-58caaceb8d3b48188ab11d10821038f1
"""

from __future__ import annotations

import datetime as dt
import logging
from typing import Any, ClassVar

from ._base import ShapeBase
from ._decorators import spine
from ._types import HandoffProtocol, ShapeKind

log = logging.getLogger("amplified.shapes.glue")


@spine("narrow_handoff", "congruence", "win_win")
class GlueBase(ShapeBase):
    """Base class for all glue shapes.

    Bridges shapes with incompatible interfaces. Exists because the
    real world is messy. Should be temporary where possible.

    Subclasses MUST define:
        source_shape: str          — what produces the output
        target_shape: str          — what expects the input
        mismatch_reason: str       — why don't these two connect naturally
        temporary: bool            — is this glue meant to be removed?
        removal_condition: str     — what needs to change for deletion (if temporary)

    Subclasses MUST implement:
        adapt(source_output) -> target_input
    """

    shape_kind: ClassVar[ShapeKind] = ShapeKind.GLUE

    # --- subclass MUST define ---
    source_shape: ClassVar[str] = ""
    target_shape: ClassVar[str] = ""
    mismatch_reason: ClassVar[str] = ""
    temporary: ClassVar[bool] = True
    removal_condition: ClassVar[str] = ""

    # --- debt tracking (set by @debt_tracked decorator) ---
    _debt_tracked: ClassVar[bool] = False
    _debt_created: ClassVar[str] = ""

    # --- handoff protocol ---
    receives_via: ClassVar[HandoffProtocol] = HandoffProtocol.SYNC_CALL
    hands_off_via: ClassVar[HandoffProtocol] = HandoffProtocol.SYNC_CALL

    def adapt(self, source_output: Any) -> Any:
        """Transform source output into target input. Subclass implements."""
        raise NotImplementedError(
            f"{type(self).__name__}.adapt() not implemented. "
            "Glue shapes MUST implement adapt()."
        )

    def should_be_deleted(self) -> bool:
        """Check if this glue's removal condition is met. Override with actual check."""
        return False

    def debt_age_days(self) -> int:
        """How many days has this glue existed?"""
        if not self._debt_created:
            return 0
        created = dt.datetime.fromisoformat(self._debt_created)
        now = dt.datetime.now(dt.timezone.utc)
        return (now - created).days

    def debt_report(self) -> dict[str, Any]:
        """Report on this glue's technical debt status."""
        return {
            "shape": type(self).__name__,
            "source": self.source_shape,
            "target": self.target_shape,
            "reason": self.mismatch_reason,
            "temporary": self.temporary,
            "removal_condition": self.removal_condition,
            "age_days": self.debt_age_days(),
            "should_delete": self.should_be_deleted(),
        }

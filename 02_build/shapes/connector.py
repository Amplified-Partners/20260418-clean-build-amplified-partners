"""
ConnectorBase — the bridge to an external system.

Shape: connector | Colour: GREEN | Position: external boundary
Handoff: receives via SYNC_CALL, hands off via SYNC_CALL
The most defensively written shape in the system.

Authored by Devon-58ca | 2026-05-17 | session devin-58caaceb8d3b48188ab11d10821038f1
"""

from __future__ import annotations

import logging
from typing import Any, ClassVar

from ._base import ShapeBase
from ._decorators import spine
from ._types import ConnectorError, HandoffProtocol, ShapeKind

log = logging.getLogger("amplified.shapes.connector")


@spine("narrow_handoff", "privacy_first")
class ConnectorBase(ShapeBase):
    """Base class for all connector shapes.

    Bridge to external systems. Handles auth, rate limiting, translation,
    circuit breaking. Assume the external system is hostile, flaky,
    and about to change its API tomorrow.

    Subclasses MUST define:
        external_system: str              — e.g. "xero", "whatsapp", "deepseek"
        auth: str                         — oauth2 / api_key / hmac / none
        rate_limit: str                   — e.g. "60/min"
        timeout: str                      — e.g. "15s"
        circuit_breaker_threshold: int    — consecutive failures before open
    """

    shape_kind: ClassVar[ShapeKind] = ShapeKind.CONNECTOR

    # --- subclass MUST define ---
    external_system: ClassVar[str] = ""
    auth: ClassVar[str] = "none"
    rate_limit: ClassVar[str] = ""
    timeout: ClassVar[str] = "30s"
    circuit_breaker_threshold: ClassVar[int] = 5

    # --- handoff protocol ---
    receives_via: ClassVar[HandoffProtocol] = HandoffProtocol.SYNC_CALL
    hands_off_via: ClassVar[HandoffProtocol] = HandoffProtocol.SYNC_CALL

    def to_internal(self, raw: dict[str, Any]) -> Any:
        """Translate external format to internal model. Subclass implements."""
        raise NotImplementedError(
            f"{type(self).__name__}.to_internal() not implemented. "
            "Connector shapes MUST implement to_internal()."
        )

    def to_external(self, internal: Any) -> dict[str, Any]:
        """Translate internal model to external format. Override if bidirectional."""
        raise NotImplementedError(
            f"{type(self).__name__}.to_external() not implemented."
        )

    def health_check(self) -> bool:
        """Check if the external system is reachable. Override for custom check."""
        return True

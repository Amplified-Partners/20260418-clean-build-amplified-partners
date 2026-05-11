"""Fail-closed resolver for the brain_mcp_server write side door.

Pulled into its own module (instead of living inline in
`brain_mcp_server.py`) so the guard logic can be unit-tested without
importing the FastAPI / asyncpg stack.

Lane: AMP-302 engineer C — side-door retirement.
See: `02_build/brain-migration/RUNBOOK_LEGACY_FREEZE.md`.
"""

from __future__ import annotations

import logging
from dataclasses import dataclass

logger = logging.getLogger("brain-mcp.write-guard")

# Rotate this token to invalidate any cached side-door configurations.
BRAIN_MCP_WRITE_ACK_TOKEN = "AMP-302-BRAIN-MCP-SIDE-DOOR-ACK-2026-05-11"

# Databases that must be written only by the canonical Temporal
# `write_to_memory_stores` activity.
CANONICAL_DBS = frozenset({"amplified_brain"})


@dataclass(frozen=True)
class WriteResolution:
    allowed: bool
    reason: str


def resolve_writes_allowed(
    *,
    allow_writes_raw: bool,
    db_name: str,
    write_ack: str,
    target_is_staging: bool,
) -> WriteResolution:
    """Return whether the legacy MCP write side door may be enabled.

    Fail-closed semantics:
    - ALLOW_WRITES not set → disabled (legacy default behaviour).
    - ALLOW_WRITES set but BRAIN_MCP_WRITE_ACK missing/mismatched → disabled.
    - Token matches but target is a canonical DB and operator did not
      explicitly mark it as staging → disabled.
    - Token matches and target is staging OR non-canonical → enabled.

    Note: this resolver intentionally does NOT call `sys.exit` — the
    caller (brain_mcp_server module) chooses whether to abort or merely
    refuse to install write tools.
    """
    if not allow_writes_raw:
        return WriteResolution(False, "ALLOW_WRITES not set")

    if write_ack != BRAIN_MCP_WRITE_ACK_TOKEN:
        return WriteResolution(
            False,
            "ALLOW_WRITES=true but BRAIN_MCP_WRITE_ACK missing or "
            "mismatched — refusing to enable legacy MCP write side door",
        )

    if db_name in CANONICAL_DBS and not target_is_staging:
        return WriteResolution(
            False,
            f"ALLOW_WRITES requested against canonical DB '{db_name}' "
            "but BRAIN_MCP_TARGET_IS_STAGING not set — canonical Cove "
            "store must be written only by the Temporal "
            "write_to_memory_stores activity",
        )

    return WriteResolution(
        True,
        f"Legacy MCP write side door enabled for DB '{db_name}' under "
        "operator acknowledgement (bypasses canonical Temporal writer)",
    )

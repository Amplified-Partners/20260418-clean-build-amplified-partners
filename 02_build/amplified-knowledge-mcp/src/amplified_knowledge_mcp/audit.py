"""
Audit logging for all MCP operations.

Every operation is logged with: agent name, ISO timestamp, session ID,
operation performed, and graph/collection accessed.

Signed-by: Devon | 2026-04-29 | devin-60ae27b157c3459d90abd0c80734513b
"""

from __future__ import annotations

import json
import logging
import os
import sys
from datetime import datetime, timezone
from pathlib import Path

from .config import AGENT_NAME, LOG_DIR, SESSION_ID

_logger = logging.getLogger("amplified_mcp.audit")

# In-memory audit log (also written to disk when LOG_DIR is writable)
_audit_entries: list[dict] = []


def _ensure_log_dir() -> Path | None:
    log_path = Path(LOG_DIR)
    try:
        log_path.mkdir(parents=True, exist_ok=True)
        return log_path
    except OSError:
        return None


def setup_logging() -> None:
    handler = logging.StreamHandler(sys.stderr)
    handler.setFormatter(
        logging.Formatter("%(asctime)s [%(name)s] %(levelname)s %(message)s")
    )
    root = logging.getLogger("amplified_mcp")
    root.setLevel(logging.INFO)
    root.addHandler(handler)

    log_dir = _ensure_log_dir()
    if log_dir:
        file_handler = logging.FileHandler(log_dir / "audit.log")
        file_handler.setFormatter(
            logging.Formatter("%(asctime)s %(message)s")
        )
        root.addHandler(file_handler)


def log_operation(
    operation: str,
    target: str,
    detail: str = "",
    agent: str | None = None,
    session: str | None = None,
) -> dict:
    entry = {
        "agent": agent or AGENT_NAME,
        "session_id": session or SESSION_ID,
        "timestamp": datetime.now(timezone.utc).isoformat(),
        "operation": operation,
        "target": target,
        "detail": detail[:500],
    }
    _audit_entries.append(entry)
    _logger.info(json.dumps(entry, separators=(",", ":")))

    # Append to JSONL file
    log_dir = _ensure_log_dir()
    if log_dir:
        with open(log_dir / "audit.jsonl", "a") as f:
            f.write(json.dumps(entry, separators=(",", ":")) + "\n")

    return entry


def get_recent_entries(limit: int = 50) -> list[dict]:
    return list(reversed(_audit_entries[-limit:]))

"""Audit logging — every tool call is recorded to JSONL.

Signed-by: Devon-f055 | 2026-05-07 | session devin-f055293582074f98b4c1ed6f77732b26
"""

from __future__ import annotations

import json
import logging
import os
from datetime import datetime, timezone
from pathlib import Path

from . import config

_log = logging.getLogger("beast_control.audit")


def _ensure_dir() -> None:
    config.AUDIT_DIR.mkdir(parents=True, exist_ok=True)


def log_tool_call(tool_name: str, args: dict | str, result_summary: str = "") -> None:
    """Append a structured JSONL entry for a tool invocation."""
    _ensure_dir()
    entry = {
        "ts": datetime.now(timezone.utc).isoformat(),
        "tool": tool_name,
        "args": args if isinstance(args, dict) else {"raw": str(args)},
        "result_summary": result_summary[:500],
        "agent": os.getenv("AGENT_NAME", "unknown"),
        "session": os.getenv("SESSION_ID", "unset"),
    }
    try:
        with open(config.AUDIT_LOG_PATH, "a") as f:
            f.write(json.dumps(entry, default=str) + "\n")
    except OSError as exc:
        _log.warning("Audit write failed: %s", exc)


def write_audit_snapshot(subdir: str, filename: str, data: dict | list | str) -> Path:
    """Write a JSON or Markdown audit snapshot file.

    Returns the path written.
    """
    _ensure_dir()
    out_dir = config.AUDIT_DIR / subdir
    out_dir.mkdir(parents=True, exist_ok=True)
    out_path = out_dir / filename
    with open(out_path, "w") as f:
        if isinstance(data, str):
            f.write(data)
        else:
            json.dump(data, f, indent=2, default=str)
    _log.info("Audit snapshot: %s", out_path)
    return out_path

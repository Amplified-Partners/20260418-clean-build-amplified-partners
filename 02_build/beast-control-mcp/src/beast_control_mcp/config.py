"""Configuration and security constants for Beast Control MCP.

Signed-by: Devon-f055 | 2026-05-07 | session devin-f055293582074f98b4c1ed6f77732b26
"""

from __future__ import annotations

import os
from pathlib import Path

# --- Networking ---
POSTGRES_HOST = os.getenv("POSTGRES_HOST", "127.0.0.1")
POSTGRES_PORT = int(os.getenv("POSTGRES_PORT", "5434"))
POSTGRES_USER = os.getenv("POSTGRES_USER", "amplified")
POSTGRES_PASSWORD = os.getenv("POSTGRES_PASSWORD", "")
POSTGRES_DEFAULT_DB = os.getenv("POSTGRES_DEFAULT_DB", "amplified_main")

FALKORDB_HOST = os.getenv("FALKORDB_HOST", "127.0.0.1")
FALKORDB_PORT = int(os.getenv("FALKORDB_PORT", "6380"))

QDRANT_HOST = os.getenv("QDRANT_HOST", "127.0.0.1")
QDRANT_PORT = int(os.getenv("QDRANT_PORT", "6333"))

REDIS_HOST = os.getenv("REDIS_HOST", "127.0.0.1")
REDIS_PORT = int(os.getenv("REDIS_PORT", "6379"))

# --- Auth ---
# Bearer token required on every SSE/HTTP request. Empty = no auth (local dev only).
AUTH_TOKEN = os.getenv("BEAST_MCP_AUTH_TOKEN", "")

# --- Filesystem allowlist ---
# Only these roots (and their children) are readable.
FS_READ_ALLOWLIST: list[Path] = [
    Path("/opt/amplified"),
    Path("/opt/amplified-machine"),
    Path("/var/log"),
    Path("/etc/cron.d"),
    Path("/etc/cron.daily"),
    Path("/etc/crontab"),
    Path("/etc/systemd/system"),
]

# Write access restricted to audit output only.
FS_WRITE_ALLOWLIST: list[Path] = [
    Path("/opt/amplified/audits"),
    Path("/opt/amplified/migration-bundles"),
]

# Secrets directory — list filenames only, never read contents.
SECRETS_DIR = Path("/opt/amplified/secrets")

# --- Compose file search roots ---
COMPOSE_SEARCH_ROOTS: list[Path] = [
    Path("/opt/amplified"),
    Path("/opt/amplified-machine"),
]

# --- Vault / raw dump / ingestion known roots ---
VAULT_ROOTS: list[str] = [
    "/opt/amplified/vault",
    "/opt/amplified/vault/filtered_for_ingestion",
]

RAW_DUMP_ROOTS: list[str] = [
    "/opt/amplified/raw-mac-dumps",
    "/opt/amplified/takeout-extracted",
]

INGESTION_ROOTS: list[str] = [
    "/opt/amplified/vault-ingestion-progress",
    "/opt/amplified/pudding-testing",
]

# --- Git repo search roots ---
REPO_SEARCH_ROOTS: list[Path] = [
    Path("/opt/amplified"),
    Path("/opt/amplified-machine"),
]

# --- Audit ---
AUDIT_DIR = Path(os.getenv("AUDIT_DIR", "/opt/amplified/audits"))
AUDIT_LOG_PATH = Path(os.getenv("AUDIT_LOG_PATH", "/opt/amplified/audits/tool_calls.jsonl"))

# --- Postgres readonly limit ---
PG_MAX_ROWS = int(os.getenv("PG_MAX_ROWS", "500"))

# --- Transport ---
TRANSPORT = os.getenv("BEAST_MCP_TRANSPORT", "sse")  # "stdio" or "sse"
SSE_HOST = os.getenv("BEAST_MCP_HOST", "0.0.0.0")
SSE_PORT = int(os.getenv("BEAST_MCP_PORT", "8400"))


def is_path_allowed(path: Path, allowlist: list[Path]) -> bool:
    """Check whether a resolved path falls under any allowlisted root."""
    try:
        resolved = path.resolve()
    except (OSError, ValueError):
        return False
    return any(resolved == root or root in resolved.parents for root in allowlist)


def is_read_allowed(path: str | Path) -> bool:
    """Return True if the path is readable under the allowlist."""
    return is_path_allowed(Path(path), FS_READ_ALLOWLIST)


def is_write_allowed(path: str | Path) -> bool:
    """Return True if the path is writable under the allowlist."""
    return is_path_allowed(Path(path), FS_WRITE_ALLOWLIST)

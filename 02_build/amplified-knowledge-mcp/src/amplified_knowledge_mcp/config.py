"""
Configuration for the Amplified Knowledge MCP server.

Environment variables:
    TIER            - Access tier: "readonly" (default), "readwrite", "admin"
    FALKORDB_HOST   - FalkorDB host (default: falkordb)
    FALKORDB_PORT   - FalkorDB port (default: 6379)
    QDRANT_HOST     - Qdrant host (default: qdrant)
    QDRANT_PORT     - Qdrant HTTP port (default: 6333)
    EMBEDDING_MODEL - Sentence-transformers model (default: all-MiniLM-L6-v2)
    LOG_DIR         - Audit log directory (default: /var/log/amplified-mcp)
    AGENT_NAME      - Name of the calling agent (default: unknown)
    SESSION_ID      - Session identifier (default: unset)

Signed-by: Devon | 2026-04-29 | devin-60ae27b157c3459d90abd0c80734513b
"""

from __future__ import annotations

import os
from enum import Enum


class Tier(str, Enum):
    READONLY = "readonly"
    READWRITE = "readwrite"
    ADMIN = "admin"


TIER = Tier(os.getenv("TIER", "readonly"))

FALKORDB_HOST = os.getenv("FALKORDB_HOST", "falkordb")
FALKORDB_PORT = int(os.getenv("FALKORDB_PORT", "6379"))

QDRANT_HOST = os.getenv("QDRANT_HOST", "qdrant")
QDRANT_PORT = int(os.getenv("QDRANT_PORT", "6333"))

EMBEDDING_MODEL = os.getenv("EMBEDDING_MODEL", "all-MiniLM-L6-v2")

LOG_DIR = os.getenv("LOG_DIR", "/var/log/amplified-mcp")

AGENT_NAME = os.getenv("AGENT_NAME", "unknown")
SESSION_ID = os.getenv("SESSION_ID", "unset")

"""
Cypher query validation and tier enforcement.

Rejects any Cypher containing write operations for read-only tiers.
Rejects destructive operations for read-write tiers.

FalkorDB knowledge graph built by Clawd (OpenClaw).

Signed-by: Devon | 2026-04-29 | devin-60ae27b157c3459d90abd0c80734513b
"""

from __future__ import annotations

import re

from .config import Tier

# Cypher keywords that mutate data
_WRITE_KEYWORDS = re.compile(
    r"\b(CREATE|SET|DELETE|MERGE|REMOVE|DROP|DETACH)\b",
    re.IGNORECASE,
)

# Destructive-only subset (Tier 2 blocks these; Tier 3 allows them)
_DESTRUCTIVE_KEYWORDS = re.compile(
    r"\b(DELETE|DROP|DETACH)\b",
    re.IGNORECASE,
)


def validate_cypher(query: str, tier: Tier) -> str | None:
    """Return an error message if the query is disallowed for the tier, else None."""
    stripped = _strip_cypher_strings(query)

    if tier == Tier.READONLY:
        match = _WRITE_KEYWORDS.search(stripped)
        if match:
            return (
                f"Read-only tier: query contains disallowed keyword "
                f"'{match.group().upper()}'. Only read operations are permitted."
            )

    elif tier == Tier.READWRITE:
        match = _DESTRUCTIVE_KEYWORDS.search(stripped)
        if match:
            return (
                f"Read-write tier: query contains destructive keyword "
                f"'{match.group().upper()}'. Writes are allowed but deletions are not."
            )

    # Tier ADMIN: all operations permitted (except raw data destruction,
    # which is enforced at the tool level, not at the Cypher level).
    return None


def _strip_cypher_strings(query: str) -> str:
    """Remove quoted string literals so keywords inside strings don't trigger false positives."""
    return re.sub(r"'[^']*'|\"[^\"]*\"", "", query)

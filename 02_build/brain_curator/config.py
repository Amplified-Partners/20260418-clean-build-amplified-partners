"""00_config — configuration constants for the brain_curator module.

Epistemic types (P0Policy, tier constants, tier rank) are imported from
the canonical ``epistemic_core`` module and re-exported here for backward
compatibility. Route constants, packet types, validation thresholds,
secret/PII keywords, and provenance remain brain_curator-specific.

Signed-by: Devon-d493 | 2026-05-19 | devin-d49302e4179d43d0892997a7f3a9f57f
Modified-by: Devon-d493 | 2026-05-19 | PR 2 — import from epistemic_core
"""

from __future__ import annotations

# ---------------------------------------------------------------------------
# Epistemic types — canonical source is epistemic_core
# ---------------------------------------------------------------------------

from epistemic_core.p0_policy import (  # noqa: F401 — re-export
    ACTIVE_P0_POLICY,
    P0Incident,
    P0Policy,
)
from epistemic_core.tiers import (  # noqa: F401 — re-export
    TIER_INTUITED,
    TIER_MEASURED,
    TIER_PROVEN,
    TIER_RANK,
    TIER_STRUCTURED,
    EpistemicTier,
)

# Tiers allowed for default agent retrieval (INTUITED excluded)
RETRIEVAL_TIERS: frozenset[str] = frozenset(
    {TIER_STRUCTURED, TIER_MEASURED, TIER_PROVEN}
)

# ---------------------------------------------------------------------------
# Module version
# ---------------------------------------------------------------------------

CODE_VERSION = "brain-curator-v0.2"

# ---------------------------------------------------------------------------
# Packet types
# ---------------------------------------------------------------------------

GOVERNED_PACKET_TYPES: frozenset[str] = frozenset(
    {"working_model", "decision", "method", "doctrine"}
)

ALL_PACKET_TYPES: frozenset[str] = frozenset(
    {
        "decision",
        "working_model",
        "method",
        "doctrine",
        "failure",
        "prompt_pattern",
        "reference",
        "conversation",
    }
)

# ---------------------------------------------------------------------------
# Route constants
# ---------------------------------------------------------------------------

ROUTE_KEEP = "keep"
ROUTE_FREEZE = "freeze"
ROUTE_REFINE = "refine"
ROUTE_QUARANTINE = "quarantine"
ROUTE_DROP_FROM_ACTIVE = "drop_from_active"
ROUTE_REVIEW = "review"
ROUTE_VALIDATE = "validate"

ACTIVE_ROUTES: frozenset[str] = frozenset({ROUTE_KEEP, ROUTE_FREEZE})

# ---------------------------------------------------------------------------
# Validation sample size
# ---------------------------------------------------------------------------

VALIDATION_SAMPLE_SIZE = 100
VALIDATION_MIN_ACTIVE = 10
VALIDATION_MIN_QUARANTINE = 10
VALIDATION_MIN_DUPLICATE = 10
VALIDATION_MIN_GEM = 10

# ---------------------------------------------------------------------------
# Secret / PII detection keywords (conservative)
# ---------------------------------------------------------------------------

SECRET_KEYWORDS: frozenset[str] = frozenset(
    {
        "api_key",
        "api-key",
        "apikey",
        "secret",
        "password",
        "passwd",
        "token",
        "bearer",
        "authorization",
        "private_key",
        "private-key",
        "ssh-rsa",
        "ssh-ed25519",
        "aws_access_key",
        "aws_secret_key",
    }
)

PII_KEYWORDS: frozenset[str] = frozenset(
    {
        "national insurance",
        "ni number",
        "date of birth",
        "passport number",
        "bank account",
        "sort code",
        "credit card",
        "ssn",
        "social security",
    }
)

# ---------------------------------------------------------------------------
# Provenance
# ---------------------------------------------------------------------------

PIPELINE_PROVENANCE = "amplified-pipeline-v0.3"

"""Shared fail-closed guard for legacy migration writers.

Purpose
-------
The scripts in `02_build/brain-migration/` are one-shot ETL utilities that
historically produced the 57,297-vector wave into `amplified_brain` and
bulk-COPY'd entities/episodes/relationships from FalkorDB. They use
superuser-style access and contain destructive `DELETE` statements.

After AMP-302 (Cove ingestion provenance hardening) these scripts are
**frozen**. The canonical writer is the Temporal activity
`write_to_memory_stores` in
`02_build/cove-orchestrator/temporal/activities/ingestion_activities.py`.

This module enforces fail-closed semantics: the legacy writers refuse to
run unless an operator has explicitly opted-in via the documented
migration protocol (env var + acknowledged target DB).

Lane: AMP-302 engineer C — legacy writer quarantine.
See: `02_build/brain-migration/RUNBOOK_LEGACY_FREEZE.md`.

Signed-by: Devon-AMP-302-C | 2026-05-11
"""

from __future__ import annotations

import os
import sys
from dataclasses import dataclass

# ── Protocol tokens ────────────────────────────────────────────────────
# The exact token required to unlock a legacy writer. Rotating this
# string is the cheapest way to invalidate any stale scripts/scheduled
# jobs that may have cached the previous value.
MIGRATION_PROTOCOL_TOKEN = "AMP-302-MIGRATION-PROTOCOL-2026-05-11"

# Env vars an operator must set, in addition to the token, to confirm
# they are aware which database they are about to mutate.
ENV_PROTOCOL = "AMPLIFIED_MIGRATION_PROTOCOL"
ENV_TARGET_DB = "AMPLIFIED_MIGRATION_TARGET_DB"
ENV_OPERATOR = "AMPLIFIED_MIGRATION_OPERATOR"

# Databases that are NEVER acceptable targets for a legacy one-shot
# writer. `amplified_brain` is the canonical Cove store — only the
# Temporal `write_to_memory_stores` activity is allowed to mutate it.
CANONICAL_DATABASES = frozenset({"amplified_brain"})


@dataclass(frozen=True)
class GuardDecision:
    allowed: bool
    reason: str
    operator: str | None = None
    target_db: str | None = None


def evaluate_guard(
    target_db: str,
    *,
    env: dict[str, str] | None = None,
) -> GuardDecision:
    """Return a `GuardDecision` for a legacy writer wanting to touch `target_db`.

    Fail-closed defaults:
    - No env vars set → block.
    - Token mismatch → block.
    - Target DB is in CANONICAL_DATABASES and operator did not explicitly
      acknowledge it → block.
    - Mismatched target_db between caller's intent and env declaration → block.

    Only when token matches AND operator acknowledged the same target_db
    that the caller declared do we allow the run. Operator identity is
    recorded so the resulting log line can be audited.
    """
    env = env if env is not None else os.environ

    token = env.get(ENV_PROTOCOL, "").strip()
    declared_db = env.get(ENV_TARGET_DB, "").strip()
    operator = env.get(ENV_OPERATOR, "").strip()

    if not token:
        return GuardDecision(
            allowed=False,
            reason=(
                f"Legacy writer blocked: {ENV_PROTOCOL} is unset. "
                "This script is FROZEN. See "
                "02_build/brain-migration/RUNBOOK_LEGACY_FREEZE.md."
            ),
            target_db=target_db,
        )

    if token != MIGRATION_PROTOCOL_TOKEN:
        return GuardDecision(
            allowed=False,
            reason=(
                f"Legacy writer blocked: {ENV_PROTOCOL} token mismatch. "
                "The migration protocol token has been rotated — refusing "
                "to run a stale script against a live database."
            ),
            target_db=target_db,
        )

    if not declared_db:
        return GuardDecision(
            allowed=False,
            reason=(
                f"Legacy writer blocked: {ENV_TARGET_DB} not set. The "
                "operator must explicitly declare which database they are "
                "mutating; we will not infer this from script defaults."
            ),
            target_db=target_db,
        )

    if declared_db != target_db:
        return GuardDecision(
            allowed=False,
            reason=(
                f"Legacy writer blocked: declared target '{declared_db}' "
                f"does not match script target '{target_db}'. Refusing "
                "to run when the operator's stated intent disagrees with "
                "the script's actual config."
            ),
            target_db=target_db,
        )

    if not operator:
        return GuardDecision(
            allowed=False,
            reason=(
                f"Legacy writer blocked: {ENV_OPERATOR} not set. We require "
                "an identifiable operator on every legacy migration run for "
                "post-hoc audit."
            ),
            target_db=target_db,
        )

    if target_db in CANONICAL_DATABASES:
        # Canonical DB requires an extra explicit acknowledgement env var
        # so it can never be enabled merely by exporting the three
        # standard vars in a shell.
        ack = env.get("AMPLIFIED_MIGRATION_ACK_CANONICAL", "").strip()
        if ack != f"YES-I-KNOW-{target_db.upper()}-IS-CANONICAL":
            return GuardDecision(
                allowed=False,
                reason=(
                    f"Legacy writer blocked: target '{target_db}' is the "
                    "canonical Cove store. Refusing to run unless "
                    "AMPLIFIED_MIGRATION_ACK_CANONICAL is set to "
                    f"'YES-I-KNOW-{target_db.upper()}-IS-CANONICAL'. "
                    "See RUNBOOK_LEGACY_FREEZE.md before doing this."
                ),
                target_db=target_db,
                operator=operator,
            )

    return GuardDecision(
        allowed=True,
        reason=(
            f"Legacy writer permitted: operator={operator}, "
            f"target_db={target_db}, protocol={MIGRATION_PROTOCOL_TOKEN}."
        ),
        operator=operator,
        target_db=target_db,
    )


def enforce_or_exit(target_db: str, script_name: str) -> GuardDecision:
    """Convenience wrapper for legacy CLI scripts.

    Exits with code 2 (config error) and prints the reason to stderr if
    the guard fails. Returns the decision unchanged when allowed so the
    caller can log it.
    """
    decision = evaluate_guard(target_db)
    if not decision.allowed:
        print(
            f"[migration_guard] {script_name} REFUSING TO RUN: "
            f"{decision.reason}",
            file=sys.stderr,
        )
        sys.exit(2)
    print(
        f"[migration_guard] {script_name} permitted under protocol: "
        f"{decision.reason}",
        file=sys.stderr,
    )
    return decision

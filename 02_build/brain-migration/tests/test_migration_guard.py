"""Tests for the AMP-302 legacy migration guard.

These tests prove the fail-closed contract: the legacy writers in
`02_build/brain-migration/` cannot touch the canonical Cove store
unless the documented migration protocol env vars are set together AND
the operator has explicitly acknowledged that the target DB is canonical.

If these tests start failing because someone widened the guard, that is
the signal to update the runbook (`RUNBOOK_LEGACY_FREEZE.md`) and the
after-action template before merging.

Signed-by: Devon-AMP-302-C | 2026-05-11
"""

from __future__ import annotations

import pytest

from migration_guard import (
    CANONICAL_DATABASES,
    MIGRATION_PROTOCOL_TOKEN,
    evaluate_guard,
    enforce_or_exit,
)

CANONICAL_DB = "amplified_brain"
STAGING_DB = "amplified_brain_staging"


def _full_protocol_env(target: str = CANONICAL_DB) -> dict[str, str]:
    env = {
        "AMPLIFIED_MIGRATION_PROTOCOL": MIGRATION_PROTOCOL_TOKEN,
        "AMPLIFIED_MIGRATION_TARGET_DB": target,
        "AMPLIFIED_MIGRATION_OPERATOR": "engineer-c-amp-302",
    }
    if target in CANONICAL_DATABASES:
        env["AMPLIFIED_MIGRATION_ACK_CANONICAL"] = (
            f"YES-I-KNOW-{target.upper()}-IS-CANONICAL"
        )
    return env


class TestEvaluateGuard:
    def test_empty_env_blocks_canonical_db(self):
        decision = evaluate_guard(CANONICAL_DB, env={})
        assert decision.allowed is False
        assert "FROZEN" in decision.reason or "unset" in decision.reason

    def test_empty_env_blocks_staging_db(self):
        # Staging is not canonical, but with no protocol the guard
        # still fails closed — we never want a silent run.
        decision = evaluate_guard(STAGING_DB, env={})
        assert decision.allowed is False

    def test_wrong_token_is_blocked(self):
        env = _full_protocol_env()
        env["AMPLIFIED_MIGRATION_PROTOCOL"] = "stale-token-from-old-runbook"
        decision = evaluate_guard(CANONICAL_DB, env=env)
        assert decision.allowed is False
        assert "token mismatch" in decision.reason.lower()

    def test_missing_target_db_declaration_is_blocked(self):
        env = _full_protocol_env()
        env.pop("AMPLIFIED_MIGRATION_TARGET_DB")
        decision = evaluate_guard(CANONICAL_DB, env=env)
        assert decision.allowed is False
        assert "TARGET_DB" in decision.reason

    def test_mismatched_target_db_is_blocked(self):
        env = _full_protocol_env()
        env["AMPLIFIED_MIGRATION_TARGET_DB"] = "some_other_db"
        decision = evaluate_guard(CANONICAL_DB, env=env)
        assert decision.allowed is False
        assert "disagrees" in decision.reason or "does not match" in decision.reason

    def test_missing_operator_is_blocked(self):
        env = _full_protocol_env()
        env.pop("AMPLIFIED_MIGRATION_OPERATOR")
        decision = evaluate_guard(CANONICAL_DB, env=env)
        assert decision.allowed is False
        assert "OPERATOR" in decision.reason

    def test_canonical_db_requires_explicit_ack(self):
        env = _full_protocol_env()
        env.pop("AMPLIFIED_MIGRATION_ACK_CANONICAL")
        decision = evaluate_guard(CANONICAL_DB, env=env)
        assert decision.allowed is False
        assert "canonical" in decision.reason.lower()

    def test_canonical_db_wrong_ack_is_blocked(self):
        env = _full_protocol_env()
        env["AMPLIFIED_MIGRATION_ACK_CANONICAL"] = "yes"
        decision = evaluate_guard(CANONICAL_DB, env=env)
        assert decision.allowed is False

    def test_full_protocol_allows_canonical_db(self):
        env = _full_protocol_env()
        decision = evaluate_guard(CANONICAL_DB, env=env)
        assert decision.allowed is True
        assert decision.operator == "engineer-c-amp-302"
        assert decision.target_db == CANONICAL_DB

    def test_full_protocol_allows_staging_without_canonical_ack(self):
        env = _full_protocol_env(target=STAGING_DB)
        decision = evaluate_guard(STAGING_DB, env=env)
        assert decision.allowed is True

    def test_amplified_brain_is_in_canonical_set(self):
        # Locking the canonical set in a test so removing it from the
        # frozenset is a noisy diff.
        assert "amplified_brain" in CANONICAL_DATABASES


class TestEnforceOrExit:
    def test_enforce_or_exit_exits_on_block(self, monkeypatch, capsys):
        monkeypatch.delenv("AMPLIFIED_MIGRATION_PROTOCOL", raising=False)
        with pytest.raises(SystemExit) as exc:
            enforce_or_exit(CANONICAL_DB, script_name="test_script.py")
        assert exc.value.code == 2
        err = capsys.readouterr().err
        assert "REFUSING TO RUN" in err
        assert "test_script.py" in err

    def test_enforce_or_exit_passes_with_full_protocol(self, monkeypatch, capsys):
        for k, v in _full_protocol_env().items():
            monkeypatch.setenv(k, v)
        decision = enforce_or_exit(CANONICAL_DB, script_name="test_script.py")
        assert decision.allowed is True
        err = capsys.readouterr().err
        assert "permitted under protocol" in err

"""Tests for the AMP-302 brain_mcp_server side-door fail-closed guard.

Proves that the historical `ALLOW_WRITES=true` side door is no longer
sufficient on its own to enable writes through `brain_mcp_server.py`.
The operator must additionally set the rotated token and, for the
canonical DB, opt in via the staging flag (which we deliberately do not
allow against `amplified_brain`).

Signed-by: Devon-AMP-302-C | 2026-05-11
"""

from __future__ import annotations

from brain_mcp_write_guard import (
    BRAIN_MCP_WRITE_ACK_TOKEN,
    CANONICAL_DBS,
    resolve_writes_allowed,
)


class TestResolveWritesAllowed:
    def test_default_disabled(self):
        r = resolve_writes_allowed(
            allow_writes_raw=False,
            db_name="amplified_brain",
            write_ack="",
            target_is_staging=False,
        )
        assert r.allowed is False

    def test_allow_writes_alone_is_not_enough(self):
        r = resolve_writes_allowed(
            allow_writes_raw=True,
            db_name="amplified_brain",
            write_ack="",
            target_is_staging=False,
        )
        assert r.allowed is False
        assert "BRAIN_MCP_WRITE_ACK" in r.reason

    def test_wrong_ack_token_blocks(self):
        r = resolve_writes_allowed(
            allow_writes_raw=True,
            db_name="amplified_brain",
            write_ack="not-the-real-token",
            target_is_staging=False,
        )
        assert r.allowed is False

    def test_canonical_db_blocked_even_with_correct_token(self):
        # The canonical DB must NEVER accept writes through this side
        # door unless the operator explicitly says they are pointing at
        # a staging copy of the DB (not the real `amplified_brain`).
        r = resolve_writes_allowed(
            allow_writes_raw=True,
            db_name="amplified_brain",
            write_ack=BRAIN_MCP_WRITE_ACK_TOKEN,
            target_is_staging=False,
        )
        assert r.allowed is False
        assert "canonical" in r.reason.lower()

    def test_canonical_db_allowed_when_marked_staging(self):
        # An operator who has rerouted DB_HOST/DB_NAME to a staging
        # database explicitly tells us so. We trust their assertion but
        # still log it.
        r = resolve_writes_allowed(
            allow_writes_raw=True,
            db_name="amplified_brain",
            write_ack=BRAIN_MCP_WRITE_ACK_TOKEN,
            target_is_staging=True,
        )
        assert r.allowed is True

    def test_noncanonical_db_allowed_with_correct_token(self):
        r = resolve_writes_allowed(
            allow_writes_raw=True,
            db_name="some_throwaway_db",
            write_ack=BRAIN_MCP_WRITE_ACK_TOKEN,
            target_is_staging=False,
        )
        assert r.allowed is True

    def test_amplified_brain_is_canonical(self):
        assert "amplified_brain" in CANONICAL_DBS

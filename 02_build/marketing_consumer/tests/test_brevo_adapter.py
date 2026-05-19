"""Tests for Brevo adapter — dry-run by default, payload shape, state gate.

Covers:
  1. BrevoConfig defaults to dry-run
  2. Payload builder produces correct Brevo v3 shape
  3. Dry-run mode builds payload but does not call API
  4. State gate prevents sending non-approved artifacts
  5. Live config detection

Signed-by: Devon-d493 | 2026-05-19 | devin-d49302e4179d43d0892997a7f3a9f57f
"""

from __future__ import annotations

import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[2]))

from marketing_consumer.models import MarketingArtifact  # noqa: E402
from marketing_consumer.brevo_adapter import (  # noqa: E402
    BrevoConfig,
    build_payload,
    send_email,
)


# ---------------------------------------------------------------------------
# Helpers
# ---------------------------------------------------------------------------


def _artifact(**kw: object) -> MarketingArtifact:
    defaults: dict = {
        "title": "Test Email Subject",
        "content": "<h1>Hello</h1><p>Great insights.</p>",
        "brain_packet_id": "pkt-abc-123",
        "channel": "email",
    }
    defaults.update(kw)
    return MarketingArtifact(**defaults)


def _config(**kw: object) -> BrevoConfig:
    defaults: dict = {}
    defaults.update(kw)
    return BrevoConfig(**defaults)


# ===================================================================
# 1. BrevoConfig
# ===================================================================


class TestBrevoConfig:
    def test_defaults_dry_run(self) -> None:
        cfg = BrevoConfig()
        assert cfg.dry_run is True
        assert cfg.api_key == ""
        assert cfg.is_live is False

    def test_live_requires_key_and_no_dry_run(self) -> None:
        cfg = BrevoConfig(api_key="xkeysib-test", dry_run=False)
        assert cfg.is_live is True

    def test_key_without_disabling_dry_run(self) -> None:
        cfg = BrevoConfig(api_key="xkeysib-test", dry_run=True)
        assert cfg.is_live is False

    def test_no_key_with_dry_run_disabled(self) -> None:
        cfg = BrevoConfig(api_key="", dry_run=False)
        assert cfg.is_live is False

    def test_whitespace_key_not_live(self) -> None:
        cfg = BrevoConfig(api_key="   ", dry_run=False)
        assert cfg.is_live is False

    def test_sender_defaults(self) -> None:
        cfg = BrevoConfig()
        assert cfg.sender_email == "noreply@amplifiedpartners.ai"
        assert cfg.sender_name == "Amplified Partners"


# ===================================================================
# 2. Payload builder
# ===================================================================


class TestBuildPayload:
    def test_basic_shape(self) -> None:
        a = _artifact()
        cfg = _config()
        payload = build_payload(a, config=cfg, to_email="bob@example.com", to_name="Bob")
        assert payload["sender"]["email"] == "noreply@amplifiedpartners.ai"
        assert payload["to"][0]["email"] == "bob@example.com"
        assert payload["to"][0]["name"] == "Bob"
        assert payload["subject"] == "Test Email Subject"
        assert "<h1>Hello</h1>" in payload["htmlContent"]

    def test_tags_include_artifact_and_brain_packet(self) -> None:
        a = _artifact()
        cfg = _config()
        payload = build_payload(a, config=cfg, to_email="x@y.com")
        tags = payload["tags"]
        assert any(t.startswith("artifact:") for t in tags)
        assert any(t.startswith("brain_packet:pkt-abc-123") for t in tags)
        assert any(t.startswith("channel:email") for t in tags)


# ===================================================================
# 3. Dry-run mode
# ===================================================================


class TestDryRunSend:
    def test_dry_run_on_sent_artifact(self) -> None:
        a = _artifact(state="sent", approval_signal="explicit_approval")
        cfg = _config()
        result = send_email(a, config=cfg, to_email="bob@example.com")
        assert result.dry_run is True
        assert result.sent is False
        assert result.status_code == 200
        assert result.message_id == "dry-run"
        assert result.request_payload  # payload still built

    def test_dry_run_captures_payload(self) -> None:
        a = _artifact(state="sent", approval_signal="explicit_approval")
        cfg = _config()
        result = send_email(a, config=cfg, to_email="bob@example.com")
        assert "sender" in result.request_payload
        assert "to" in result.request_payload


# ===================================================================
# 4. State gate
# ===================================================================


class TestStateGate:
    def test_rejects_draft_artifact(self) -> None:
        a = _artifact(state="draft")
        cfg = _config()
        result = send_email(a, config=cfg, to_email="bob@example.com")
        assert result.sent is False
        assert result.dry_run is False
        assert "draft" in result.detail

    def test_rejects_blocked_artifact(self) -> None:
        a = _artifact(state="blocked")
        cfg = _config()
        result = send_email(a, config=cfg, to_email="bob@example.com")
        assert result.sent is False
        assert "blocked" in result.detail

    def test_rejects_approved_not_sent(self) -> None:
        a = _artifact(state="approved")
        cfg = _config()
        result = send_email(a, config=cfg, to_email="bob@example.com")
        assert result.sent is False
        assert "approved" in result.detail

    def test_rejects_dry_run_state(self) -> None:
        a = _artifact(state="dry_run")
        cfg = _config()
        result = send_email(a, config=cfg, to_email="bob@example.com")
        assert result.sent is False
        assert "dry_run" in result.detail


# ===================================================================
# 5. Import / dependency visibility
# ===================================================================


class TestDependencyVisibility:
    def test_requests_is_top_level_import(self) -> None:
        """requests must be importable at module level, not hidden inside a function."""
        import marketing_consumer.brevo_adapter as mod

        assert hasattr(mod, "requests"), "requests should be a top-level module attribute"

    def test_requests_importable(self) -> None:
        """requests must be installed — it is a declared dependency."""
        import requests  # noqa: F401


# ===================================================================
# 6. Missing API key behaviour
# ===================================================================


class TestMissingApiKey:
    def test_no_key_defaults_to_dry_run(self) -> None:
        cfg = BrevoConfig()  # no key, dry_run=True
        assert cfg.is_live is False

    def test_no_key_dry_run_false_is_not_live(self) -> None:
        """dry_run=False without an API key must NOT be live."""
        cfg = BrevoConfig(api_key="", dry_run=False)
        assert cfg.is_live is False

    def test_no_key_dry_run_false_returns_dry_run_result(self) -> None:
        """Even with dry_run=False, missing key means dry-run behaviour."""
        a = _artifact(state="sent", approval_signal="explicit_approval")
        cfg = BrevoConfig(api_key="", dry_run=False)
        result = send_email(a, config=cfg, to_email="bob@example.com")
        # is_live is False (no key), so dry-run path
        assert result.sent is False
        assert result.dry_run is True
        assert result.message_id == "dry-run"


# ===================================================================
# 7. Live mode with mocked requests
# ===================================================================


class TestLiveModeMocked:
    def test_live_send_success(self) -> None:
        """Live send with a mocked requests.post returning 201."""
        import unittest.mock as mock

        a = _artifact(state="sent", approval_signal="explicit_approval")
        cfg = BrevoConfig(api_key="xkeysib-real-key", dry_run=False)

        fake_response = mock.MagicMock()
        fake_response.status_code = 201
        fake_response.content = b'{"messageId": "msg-abc"}'
        fake_response.json.return_value = {"messageId": "msg-abc"}

        with mock.patch("marketing_consumer.brevo_adapter.requests.post", return_value=fake_response):
            result = send_email(a, config=cfg, to_email="bob@example.com")

        assert result.sent is True
        assert result.dry_run is False
        assert result.message_id == "msg-abc"
        assert result.status_code == 201

    def test_live_send_api_error(self) -> None:
        """Live send with a mocked 400 response."""
        import unittest.mock as mock

        a = _artifact(state="sent", approval_signal="explicit_approval")
        cfg = BrevoConfig(api_key="xkeysib-real-key", dry_run=False)

        fake_response = mock.MagicMock()
        fake_response.status_code = 400
        fake_response.content = b'{"message": "invalid"}'
        fake_response.json.return_value = {"message": "invalid"}

        with mock.patch("marketing_consumer.brevo_adapter.requests.post", return_value=fake_response):
            result = send_email(a, config=cfg, to_email="bob@example.com")

        assert result.sent is False
        assert result.status_code == 400
        assert "400" in result.detail

    def test_live_send_network_error(self) -> None:
        """Network failure must return a clear error, not crash."""
        import unittest.mock as mock

        import requests as req

        a = _artifact(state="sent", approval_signal="explicit_approval")
        cfg = BrevoConfig(api_key="xkeysib-real-key", dry_run=False)

        with mock.patch(
            "marketing_consumer.brevo_adapter.requests.post",
            side_effect=req.ConnectionError("DNS resolution failed"),
        ):
            result = send_email(a, config=cfg, to_email="bob@example.com")

        assert result.sent is False
        assert result.status_code == 0
        assert "DNS resolution failed" in result.detail

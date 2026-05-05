"""Tests for `_check_auth` in the polish-gate FastAPI app.

Covers the two security-critical behaviours:
 - constant-time comparison via `hmac.compare_digest`
 - dev-mode (empty SHARED_SECRET) allows requests through unchanged
"""

from __future__ import annotations

import importlib

import pytest
from fastapi import HTTPException


def _reload_api(monkeypatch: pytest.MonkeyPatch, *, secret: str) -> object:
    monkeypatch.setenv("COVE_POLISH_GATE_TOKEN", secret)
    import api.polish_gate as mod  # noqa: WPS433  (deliberate runtime import)
    return importlib.reload(mod)


def test_check_auth_dev_mode_allows_anything(monkeypatch: pytest.MonkeyPatch) -> None:
    mod = _reload_api(monkeypatch, secret="")
    mod._check_auth(None)
    mod._check_auth("anything")  # no SHARED_SECRET ⇒ all callers pass


def test_check_auth_rejects_missing_token(monkeypatch: pytest.MonkeyPatch) -> None:
    mod = _reload_api(monkeypatch, secret="s3cret")
    with pytest.raises(HTTPException) as ei:
        mod._check_auth(None)
    assert ei.value.status_code == 401


def test_check_auth_rejects_wrong_token(monkeypatch: pytest.MonkeyPatch) -> None:
    mod = _reload_api(monkeypatch, secret="s3cret")
    with pytest.raises(HTTPException) as ei:
        mod._check_auth("wrong")
    assert ei.value.status_code == 401


def test_check_auth_accepts_correct_token(monkeypatch: pytest.MonkeyPatch) -> None:
    mod = _reload_api(monkeypatch, secret="s3cret")
    mod._check_auth("s3cret")  # should not raise


def test_check_auth_uses_compare_digest(monkeypatch: pytest.MonkeyPatch) -> None:
    """Smoke-test the constant-time path is wired up.

    We can't reliably measure timing here, but we can verify the function
    delegates to `hmac.compare_digest` by patching it.
    """
    mod = _reload_api(monkeypatch, secret="s3cret")
    calls: list[tuple[str, str]] = []

    def _fake_cd(a: str, b: str) -> bool:
        calls.append((a, b))
        return a == b

    monkeypatch.setattr(mod.hmac, "compare_digest", _fake_cd)
    mod._check_auth("s3cret")
    assert calls == [("s3cret", "s3cret")]

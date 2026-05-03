"""Tests for the on-disk HTTP cache used by the validators framework.

The cache is keyed by ``sha256(method | url | sorted_params)``. We exercise:

- writing a fresh entry and reading it back
- the ``no_network=True`` raise-on-miss path
- the cache hit path returning ``from_cache=True``

We do not hit the network in these tests — we monkey-patch the underlying
httpx client to a deterministic stub.

Authored by Devon (Devin session 4234e1c8afbe42f2aff84a29ce139809), 2026-05-03.
"""

from __future__ import annotations

from pathlib import Path

import pytest

from validators.sources._http import CacheMiss, HttpClient


class _FakeResponse:
    def __init__(self, status_code: int, content: bytes) -> None:
        self.status_code = status_code
        self.content = content
        self.headers: dict[str, str] = {"content-type": "application/json"}
        self.url = "https://example.invalid/probe"


class _FakeHttpx:
    def __init__(self, body: bytes) -> None:
        self.body = body
        self.calls = 0

    def get(self, url, params=None, headers=None, auth=None):
        self.calls += 1
        return _FakeResponse(200, self.body)

    def close(self) -> None:
        pass


def test_cache_writes_and_reads(tmp_path: Path) -> None:
    fake = _FakeHttpx(b'{"hello":"world"}')
    client = HttpClient(cache_dir=tmp_path, _httpx_client=fake)
    try:
        first = client.get("https://example.invalid/probe", {"q": "x"})
        assert first.status_code == 200
        assert first.from_cache is False
        assert fake.calls == 1
        # Second call: must come from cache, no extra http call
        second = client.get("https://example.invalid/probe", {"q": "x"})
        assert second.from_cache is True
        assert second.content == first.content
        assert fake.calls == 1
    finally:
        client.close()


def test_no_network_raises_on_miss(tmp_path: Path) -> None:
    fake = _FakeHttpx(b"never used")
    client = HttpClient(cache_dir=tmp_path, _httpx_client=fake, no_network=True)
    try:
        with pytest.raises(CacheMiss):
            client.get("https://example.invalid/probe")
        assert fake.calls == 0
    finally:
        client.close()


def test_no_cache_forces_refetch(tmp_path: Path) -> None:
    fake = _FakeHttpx(b'{"v":1}')
    cached = HttpClient(cache_dir=tmp_path, _httpx_client=fake)
    try:
        cached.get("https://example.invalid/probe")
    finally:
        cached.close()
    fresh = HttpClient(cache_dir=tmp_path, _httpx_client=fake, no_cache=True)
    try:
        resp = fresh.get("https://example.invalid/probe")
        assert resp.from_cache is False
        assert fake.calls == 2
    finally:
        fresh.close()


def test_auth_params_never_persisted(tmp_path: Path) -> None:
    """auth_params must not appear in the stored CachedResponse.url, the
    on-disk meta JSON, or the cache key — only in the wire request."""
    fake = _FakeHttpx(b"ok")
    secret = "SUPER-SECRET-METO-KEY"
    client = HttpClient(cache_dir=tmp_path, _httpx_client=fake)
    try:
        resp = client.get(
            "https://datapoint.metoffice.gov.uk/public/data/val/probe",
            params={"res": "daily"},
            auth_params={"key": secret},
        )
        # Returned URL must contain the request param but NOT the secret.
        assert "res=daily" in resp.url
        assert secret not in resp.url
        # Meta JSON on disk must not contain the secret either.
        meta_files = list(tmp_path.glob("*.meta.json"))
        assert len(meta_files) == 1
        assert secret not in meta_files[0].read_text(encoding="utf-8")
    finally:
        client.close()

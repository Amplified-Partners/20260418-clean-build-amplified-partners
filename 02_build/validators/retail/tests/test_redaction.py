# Authored by Devon-9a6b, 2026-05-03 (session devin-9a6bd256bd7c4a90a083a471fa94a810)
"""Tests that secret-bearing query params never land on disk or in evidence.

Covers the CodeQL "clear-text storage of sensitive information" finding on
common.py — Met Office DataPoint passes its key as ?key=, so the redaction
must trigger for that path.

Run from repo root:
  PYTHONPATH=02_build python -m unittest validators.retail.tests.test_redaction
"""
from __future__ import annotations

import json
import unittest
from unittest.mock import patch

from ..fetchers import common


class _FakeResp:
    def __init__(self, body: str, status: int = 200, headers: dict | None = None):
        self.text = body
        self.status_code = status
        self.headers = headers or {"Content-Type": "application/json"}

    def raise_for_status(self) -> None:
        if self.status_code >= 400:
            raise Exception(f"HTTP {self.status_code}")

    def json(self):
        return json.loads(self.text)


class RedactionTest(unittest.TestCase):
    def test_redact_replaces_known_secret_param_names(self):
        out = common._redact({"key": "SECRET_VALUE", "lat": 51.5, "token": "T"})
        self.assertEqual(out["key"], "[REDACTED]")
        self.assertEqual(out["token"], "[REDACTED]")
        self.assertEqual(out["lat"], 51.5)

    def test_redact_handles_none_and_empty(self):
        self.assertEqual(common._redact(None), {})
        self.assertEqual(common._redact({}), {})

    def test_redact_is_case_insensitive_on_param_names(self):
        out = common._redact({"API_KEY": "x", "Authorization": "y", "Lat": 1})
        self.assertEqual(out["API_KEY"], "[REDACTED]")
        self.assertEqual(out["Authorization"], "[REDACTED]")
        self.assertEqual(out["Lat"], 1)

    def test_fetch_json_does_not_persist_secret_param_value(self):
        body = '{"ok": true}'
        with patch.object(common, "requests") as mock_requests:
            mock_requests.get.return_value = _FakeResp(body)
            with patch.object(common, "CACHE_ROOT") as mock_root:
                from pathlib import Path
                import tempfile
                tmp = Path(tempfile.mkdtemp())
                mock_root.__truediv__ = lambda self, x: tmp / x
                # Easier: just monkey-patch _cache_paths
                with patch.object(common, "_cache_paths") as cp:
                    body_path = tmp / "body.json"
                    meta_path = tmp / "meta.json"
                    cp.return_value = (body_path, meta_path)
                    fetched = common.fetch_json(
                        "test_source",
                        "https://example.test/api",
                        params={"key": "SECRET_VALUE", "lat": 51.5},
                    )

        # The persisted meta file must (a) not carry the secret value, and
        # (b) not carry a `params` field at all — the cache slot already
        # encodes the redacted params, and dropping the field is what makes
        # the disk write provably independent of any secret-tainted value.
        meta_text = meta_path.read_text()
        self.assertNotIn("SECRET_VALUE", meta_text, "secret param leaked into meta on disk")
        meta_obj = json.loads(meta_text)
        self.assertNotIn("params", meta_obj, "meta should not carry a params field at all")
        # The Fetched object (in-memory only, never persisted as `meta`)
        # still carries the redacted params for the evidence bundle.
        self.assertEqual(fetched.params["key"], "[REDACTED]")
        self.assertEqual(fetched.params["lat"], 51.5)

    def test_evidence_bundle_does_not_carry_secret_value(self):
        f = common.Fetched(
            source="test",
            url="https://x",
            params={"key": "[REDACTED]", "lat": 1},
            status=200,
            body={"ok": True},
        )
        ev = f.evidence(sample_rows=1)
        self.assertNotIn("SECRET_VALUE", json.dumps(ev))
        self.assertEqual(ev["params"]["key"], "[REDACTED]")


class RetryBehaviourTest(unittest.TestCase):
    """fetch_json/fetch_text must not retry on deterministic 4xx responses.

    Covers the Devin Review finding on commit 625d0bd: a broad ``except
    Exception`` was catching ``requests.HTTPError`` from
    ``raise_for_status()`` for non-transient 4xx codes (401, 403, 404, ...)
    and retrying them DEFAULT_RETRIES times with backoff sleeps for nothing.
    Only genuinely transient network exceptions
    (``ConnectionError``/``Timeout``/``ChunkedEncodingError``) should
    trigger the retry loop.
    """

    def test_fetch_json_does_not_retry_404(self):
        from requests import HTTPError

        class _Resp404:
            status_code = 404
            text = "not found"
            headers: dict = {}

            def raise_for_status(self):
                raise HTTPError("404 Not Found")

            def json(self):
                return {}

        call_count = {"n": 0}

        def fake_get(*_a, **_k):
            call_count["n"] += 1
            return _Resp404()

        # Bypass cache + sleep so the test is fast and deterministic.
        with patch.object(common.requests, "get", side_effect=fake_get):
            with patch.object(common, "_cache_paths") as cp:
                from pathlib import Path
                import tempfile
                tmp = Path(tempfile.mkdtemp())
                cp.return_value = (tmp / "b.json", tmp / "m.json")
                with patch.object(common.time, "sleep") as sleep_mock:
                    with self.assertRaises(HTTPError):
                        common.fetch_json("t", "https://example.test/missing", use_cache=False)
                    sleep_mock.assert_not_called()

        self.assertEqual(call_count["n"], 1, "404 must not be retried")

    def test_fetch_json_retries_on_connection_error(self):
        from requests.exceptions import ConnectionError as ReqConnectionError

        call_count = {"n": 0}

        def fake_get(*_a, **_k):
            call_count["n"] += 1
            raise ReqConnectionError("simulated network drop")

        with patch.object(common.requests, "get", side_effect=fake_get):
            with patch.object(common, "_cache_paths") as cp:
                from pathlib import Path
                import tempfile
                tmp = Path(tempfile.mkdtemp())
                cp.return_value = (tmp / "b.json", tmp / "m.json")
                with patch.object(common.time, "sleep"):
                    with self.assertRaises(RuntimeError):
                        common.fetch_json("t", "https://example.test/down", use_cache=False)

        # DEFAULT_RETRIES = 3, so we expect 3 attempts.
        self.assertEqual(call_count["n"], common.DEFAULT_RETRIES)


if __name__ == "__main__":
    unittest.main()

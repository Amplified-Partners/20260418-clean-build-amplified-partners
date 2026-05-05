# Authored by Devon-9a6b, 2026-05-03 (session devin-9a6bd256bd7c4a90a083a471fa94a810)
"""Shared fetcher utilities: HTTP retry, on-disk cache, evidence packaging.

Cache layout (relative to validators/retail/cache/):
  <source>/<cache_slot>.json   payload
  <source>/<cache_slot>.meta   metadata (URL, ts, status, hash; NO params)

Where ``cache_slot`` = ``sha256(url + urlencode(sorted(redacted_params)))[:16]``
(redacted = secret-bearing values replaced by ``[REDACTED]``).

No raw query params land on disk in either file. The cache slot is derived
from redacted params only, so secrets cannot flow into filesystem paths
either (CodeQL ``py/clear-text-storage-sensitive-data`` clean).

Evidence bundles use a stable JSON shape so the verdict file can embed them.
"""
from __future__ import annotations

import hashlib
import json
import os
import time
from dataclasses import dataclass, field
from pathlib import Path
from typing import Any
from urllib.parse import urlencode

import requests
from requests.exceptions import ChunkedEncodingError, ConnectionError as ReqConnectionError, Timeout

# Genuinely transient network failures — the only ones it makes sense to retry.
# Notably excludes requests.HTTPError (raised by raise_for_status() for 4xx/5xx):
# 5xx in our retry set (429/500/502/503/504) is handled inline above the
# raise_for_status() call; 4xx is deterministic and must NOT be retried
# (otherwise a 401/403/404 burns DEFAULT_RETRIES * DEFAULT_BACKOFF^attempt
# seconds for nothing). Spotted by Devin Review on 625d0bd.
_TRANSIENT = (ReqConnectionError, Timeout, ChunkedEncodingError)

CACHE_ROOT = Path(__file__).resolve().parent.parent / "cache"
CACHE_ROOT.mkdir(parents=True, exist_ok=True)

UA = "AmplifiedPartners-validator/1.0 (+https://github.com/Amplified-Partners/clean-build; AMP-66)"
DEFAULT_TIMEOUT = 30
DEFAULT_RETRIES = 3
DEFAULT_BACKOFF = 1.5

# Param names that may carry credentials. The values are still used to build the
# request and to derive the cache key, but they are redacted before being
# persisted to disk in meta files or returned in evidence bundles.
SECRET_PARAM_NAMES = frozenset({
    "key", "api_key", "apikey", "token", "access_token", "auth",
    "authorization", "password", "secret", "private_key",
})


def _cache_paths(source: str, key: str) -> tuple[Path, Path]:
    base = CACHE_ROOT / source
    base.mkdir(parents=True, exist_ok=True)
    return base / f"{key}.json", base / f"{key}.meta"


def _redact(params: dict[str, Any] | None) -> dict[str, Any]:
    """Return a copy of params with secret-bearing values replaced by '[REDACTED]'.

    Used before any disk-persistence or evidence-bundle emission so secrets in
    query strings (e.g. Met Office DataPoint ?key=) never land in committed
    artefacts. Also fed into _cache_slot() so secrets never flow into
    filesystem paths either (CodeQL trusts redacted strings).
    """
    if not params:
        return {}
    return {k: ("[REDACTED]" if k.lower() in SECRET_PARAM_NAMES else v) for k, v in params.items()}


def _cache_slot(url: str, redacted_params: dict[str, Any]) -> str:
    """Deterministic 16-hex cache slot derived from redacted params only.

    For our read-only public-data APIs, two requests with different secret-key
    values but identical URL + non-secret params return identical responses, so
    sharing a cache slot is semantically correct.
    """
    raw = url + "?" + urlencode(sorted(redacted_params.items()), doseq=True)
    return hashlib.sha256(raw.encode("utf-8")).hexdigest()[:16]


@dataclass
class Fetched:
    """One HTTP fetch result, suitable for embedding in an evidence bundle."""

    source: str
    url: str
    params: dict[str, Any] = field(default_factory=dict)
    accessed_utc: str = ""
    status: int = 0
    sha256: str = ""
    cache_key: str = ""
    body: Any = None
    headers: dict[str, str] = field(default_factory=dict)
    cached: bool = False

    def evidence(self, sample_rows: int = 5, sample_chars: int = 500) -> dict[str, Any]:
        """Return the evidence-shape dict (no raw body, just summary + sample).

        For string bodies (every ``fetch_text`` response — typically HTML or
        XML) the sample is truncated to ``sample_chars`` characters. Without
        this, full pages (e.g. a 140 kB Amazon Seller Central sign-in page)
        would land verbatim in the verdict JSON. ``sample_rows=0`` suppresses
        the sample for both strings and collections.
        """
        sample = self.body
        if isinstance(self.body, str):
            if sample_rows == 0:
                sample = ""
            elif len(self.body) > sample_chars:
                sample = self.body[:sample_chars] + f"... [truncated; full body sha256={self.sha256}]"
        elif isinstance(self.body, list):
            sample = self.body[:sample_rows]
        elif isinstance(self.body, dict):
            sample = {k: self.body[k] for k in list(self.body.keys())[:sample_rows]}
        return {
            "source": self.source,
            "url": self.url,
            "params": self.params,
            "accessed_utc": self.accessed_utc,
            "status": self.status,
            "sha256": self.sha256,
            "cached": self.cached,
            "sample": sample,
        }


def fetch_json(
    source: str,
    url: str,
    params: dict | None = None,
    headers: dict | None = None,
    *,
    timeout: int = DEFAULT_TIMEOUT,
    retries: int = DEFAULT_RETRIES,
    use_cache: bool = True,
    tolerate_4xx: bool = False,
) -> Fetched:
    """GET a JSON endpoint with retries + on-disk cache.

    Raises on final failure unless tolerate_4xx is set, in which case 4xx
    responses return a Fetched with status set + body={"_error": ...} so
    runners can downgrade rather than crash.
    """
    redacted = _redact(params)
    slot = _cache_slot(url, redacted)
    body_path, meta_path = _cache_paths(source, slot)

    if use_cache and body_path.exists() and meta_path.exists():
        meta = json.loads(meta_path.read_text())
        body = json.loads(body_path.read_text())
        return Fetched(
            source=source,
            url=url,
            params=redacted,
            accessed_utc=meta["accessed_utc"],
            status=meta["status"],
            sha256=meta["sha256"],
            cache_key=slot,
            body=body,
            headers=meta.get("headers", {}),
            cached=True,
        )

    h = {"User-Agent": UA, "Accept": "application/json"}
    if headers:
        h.update(headers)

    last_err: Exception | None = None
    for attempt in range(1, retries + 1):
        try:
            resp = requests.get(url, params=params, headers=h, timeout=timeout)
            if resp.status_code in (429, 500, 502, 503, 504) and attempt < retries:
                time.sleep(DEFAULT_BACKOFF**attempt)
                continue
            if 400 <= resp.status_code < 500 and tolerate_4xx:
                accessed = time.strftime("%Y-%m-%dT%H:%M:%SZ", time.gmtime())
                return Fetched(
                    source=source,
                    url=url,
                    params=redacted,
                    accessed_utc=accessed,
                    status=resp.status_code,
                    sha256="",
                    cache_key=slot,
                    body={"_error": f"HTTP {resp.status_code}", "text": resp.text[:500]},
                    headers={},
                    cached=False,
                )
            resp.raise_for_status()
            body_text = resp.text
            sha = hashlib.sha256(body_text.encode("utf-8")).hexdigest()
            try:
                body = resp.json()
            except ValueError:
                body = {"_raw_text": body_text[:5000]}

            accessed = time.strftime("%Y-%m-%dT%H:%M:%SZ", time.gmtime())
            # Persisted meta intentionally does NOT carry params — the cache
            # slot already encodes them (redacted) and the evidence bundle
            # carries redacted params separately. Keeping params out of meta
            # makes the disk write provably independent of secret values.
            meta = {
                "url": url,
                "accessed_utc": accessed,
                "status": resp.status_code,
                "sha256": sha,
                "headers": {hk: hv for hk, hv in resp.headers.items() if hk.lower() in {"content-type", "etag", "last-modified"}},
            }
            body_path.write_text(json.dumps(body, indent=2, default=str))
            meta_path.write_text(json.dumps(meta, indent=2))
            return Fetched(
                source=source,
                url=url,
                params=redacted,
                accessed_utc=accessed,
                status=resp.status_code,
                sha256=sha,
                cache_key=slot,
                body=body,
                headers=meta["headers"],
                cached=False,
            )
        except _TRANSIENT as e:
            last_err = e
            if attempt < retries:
                time.sleep(DEFAULT_BACKOFF**attempt)
            continue
        # All other exceptions — most importantly requests.HTTPError raised by
        # resp.raise_for_status() for deterministic 4xx — propagate immediately.
    raise RuntimeError(f"fetch_json failed for {url}: {last_err}")


def fetch_text(
    source: str,
    url: str,
    params: dict | None = None,
    headers: dict | None = None,
    *,
    timeout: int = DEFAULT_TIMEOUT,
    retries: int = DEFAULT_RETRIES,
    use_cache: bool = True,
) -> Fetched:
    """GET a non-JSON endpoint. Body is the response text."""
    redacted = _redact(params)
    slot = _cache_slot(url, redacted)
    body_path, meta_path = _cache_paths(source, slot + ".txt")

    if use_cache and body_path.exists() and meta_path.exists():
        meta = json.loads(meta_path.read_text())
        body_text = body_path.read_text()
        return Fetched(
            source=source,
            url=url,
            params=redacted,
            accessed_utc=meta["accessed_utc"],
            status=meta["status"],
            sha256=meta["sha256"],
            cache_key=slot,
            body=body_text,
            headers=meta.get("headers", {}),
            cached=True,
        )

    h = {"User-Agent": UA}
    if headers:
        h.update(headers)

    last_err: Exception | None = None
    for attempt in range(1, retries + 1):
        try:
            resp = requests.get(url, params=params, headers=h, timeout=timeout)
            if resp.status_code in (429, 500, 502, 503, 504) and attempt < retries:
                time.sleep(DEFAULT_BACKOFF**attempt)
                continue
            resp.raise_for_status()
            body_text = resp.text
            sha = hashlib.sha256(body_text.encode("utf-8")).hexdigest()
            accessed = time.strftime("%Y-%m-%dT%H:%M:%SZ", time.gmtime())
            # Persisted meta intentionally omits params — see fetch_json above
            # for the rationale.
            meta = {
                "url": url,
                "accessed_utc": accessed,
                "status": resp.status_code,
                "sha256": sha,
                "headers": {hk: hv for hk, hv in resp.headers.items() if hk.lower() in {"content-type", "etag", "last-modified"}},
            }
            body_path.write_text(body_text)
            meta_path.write_text(json.dumps(meta, indent=2))
            return Fetched(
                source=source,
                url=url,
                params=redacted,
                accessed_utc=accessed,
                status=resp.status_code,
                sha256=sha,
                cache_key=slot,
                body=body_text,
                headers=meta["headers"],
                cached=False,
            )
        except _TRANSIENT as e:
            last_err = e
            if attempt < retries:
                time.sleep(DEFAULT_BACKOFF**attempt)
            continue
        # See note in fetch_json: HTTPError from raise_for_status() must NOT
        # be retried (deterministic 4xx — e.g. a private-data 401 — will never
        # succeed on retry and would just waste DEFAULT_BACKOFF^attempt seconds).
    raise RuntimeError(f"fetch_text failed for {url}: {last_err}")


def env_secret(name: str) -> str | None:
    """Read a secret from the environment. None if absent — runner downgrades to PLAUSIBLE."""
    val = os.environ.get(name)
    if not val:
        return None
    return val

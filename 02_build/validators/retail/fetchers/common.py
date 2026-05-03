# Authored by Devon-9a6b, 2026-05-03 (session devin-9a6bd256bd7c4a90a083a471fa94a810)
"""Shared fetcher utilities: HTTP retry, on-disk cache, evidence packaging.

Cache layout (relative to validators/retail/cache/):
  <source>/<sha256(url + sorted_params)[:16]>.json   payload
  <source>/<sha256(url + sorted_params)[:16]>.meta   metadata (URL, ts, status, hash)

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


def _key(url: str, params: dict | None) -> str:
    raw = url + "?" + urlencode(sorted((params or {}).items()), doseq=True)
    return hashlib.sha256(raw.encode("utf-8")).hexdigest()[:16]


def _redact(params: dict[str, Any] | None) -> dict[str, Any]:
    """Return a copy of params with secret-bearing values replaced by '[REDACTED]'.

    Used before any disk-persistence or evidence-bundle emission so secrets in
    query strings (e.g. Met Office DataPoint ?key=) never land in committed
    artefacts. The cache key is still derived from the unredacted params.
    """
    if not params:
        return {}
    return {k: ("[REDACTED]" if k.lower() in SECRET_PARAM_NAMES else v) for k, v in params.items()}


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

    def evidence(self, sample_rows: int = 5) -> dict[str, Any]:
        """Return the evidence-shape dict (no raw body, just summary + sample)."""
        sample = self.body
        if isinstance(self.body, list):
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
    key = _key(url, params)
    body_path, meta_path = _cache_paths(source, key)

    if use_cache and body_path.exists() and meta_path.exists():
        meta = json.loads(meta_path.read_text())
        body = json.loads(body_path.read_text())
        return Fetched(
            source=source,
            url=url,
            params=_redact(params),
            accessed_utc=meta["accessed_utc"],
            status=meta["status"],
            sha256=meta["sha256"],
            cache_key=key,
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
                    params=_redact(params),
                    accessed_utc=accessed,
                    status=resp.status_code,
                    sha256="",
                    cache_key=key,
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
            redacted = _redact(params)
            meta = {
                "url": url,
                "params": redacted,
                "accessed_utc": accessed,
                "status": resp.status_code,
                "sha256": sha,
                "headers": {k: v for k, v in resp.headers.items() if k.lower() in {"content-type", "etag", "last-modified"}},
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
                cache_key=key,
                body=body,
                headers=meta["headers"],
                cached=False,
            )
        except Exception as e:
            last_err = e
            if attempt < retries:
                time.sleep(DEFAULT_BACKOFF**attempt)
            continue
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
    key = _key(url, params)
    body_path, meta_path = _cache_paths(source, key + ".txt")

    if use_cache and body_path.exists() and meta_path.exists():
        meta = json.loads(meta_path.read_text())
        body_text = body_path.read_text()
        return Fetched(
            source=source,
            url=url,
            params=_redact(params),
            accessed_utc=meta["accessed_utc"],
            status=meta["status"],
            sha256=meta["sha256"],
            cache_key=key,
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
            redacted = _redact(params)
            meta = {
                "url": url,
                "params": redacted,
                "accessed_utc": accessed,
                "status": resp.status_code,
                "sha256": sha,
                "headers": {k: v for k, v in resp.headers.items() if k.lower() in {"content-type", "etag", "last-modified"}},
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
                cache_key=key,
                body=body_text,
                headers=meta["headers"],
                cached=False,
            )
        except Exception as e:
            last_err = e
            if attempt < retries:
                time.sleep(DEFAULT_BACKOFF**attempt)
            continue
    raise RuntimeError(f"fetch_text failed for {url}: {last_err}")


def env_secret(name: str) -> str | None:
    """Read a secret from the environment. None if absent — runner downgrades to PLAUSIBLE."""
    val = os.environ.get(name)
    if not val:
        return None
    return val

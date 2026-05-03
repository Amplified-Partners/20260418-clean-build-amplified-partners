"""Cached HTTP client used by all source fetchers.

Cache layout::

    02_build/validators/.cache/
        <sha256(method|url|sorted_params)>.bin    # raw response body
        <sha256(...)>.meta.json                   # url, status, headers, accessed_at

A cached response is reused on subsequent calls; pass ``no_cache=True`` to bypass.
``no_network=True`` raises if the cache misses (used by CI / offline runs).

Authored by Devon (Devin session 4234e1c8afbe42f2aff84a29ce139809), 2026-05-03.
"""

from __future__ import annotations

import hashlib
import json
import logging
import time
from dataclasses import dataclass
from datetime import datetime, timezone
from pathlib import Path
from typing import Any

import httpx

logger = logging.getLogger("validators.http")

DEFAULT_CACHE_DIR = Path(__file__).resolve().parents[1] / ".cache"
DEFAULT_TIMEOUT = 30.0
DEFAULT_USER_AGENT = (
    "Mozilla/5.0 (compatible; AmplifiedPartners-Validators/1.0; "
    "+https://github.com/Amplified-Partners/clean-build)"
)


class CacheMiss(RuntimeError):
    """Raised when ``no_network=True`` and the cache does not have the response."""


@dataclass
class CachedResponse:
    url: str
    method: str
    status_code: int
    headers: dict[str, str]
    content: bytes
    accessed_at: str
    sha256: str
    from_cache: bool

    def text(self) -> str:
        return self.content.decode("utf-8", errors="replace")

    def json(self) -> Any:
        return json.loads(self.text())


def _key(method: str, url: str, params: dict[str, Any] | None) -> str:
    payload = method.upper() + "|" + url + "|" + json.dumps(params or {}, sort_keys=True)
    return hashlib.sha256(payload.encode("utf-8")).hexdigest()


class HttpClient:
    """Small wrapper around ``httpx.Client`` with on-disk caching."""

    def __init__(
        self,
        cache_dir: Path | None = None,
        timeout: float = DEFAULT_TIMEOUT,
        no_cache: bool = False,
        no_network: bool = False,
        user_agent: str = DEFAULT_USER_AGENT,
        _httpx_client: Any = None,
    ) -> None:
        self.cache_dir = cache_dir or DEFAULT_CACHE_DIR
        self.cache_dir.mkdir(parents=True, exist_ok=True)
        self.no_cache = no_cache
        self.no_network = no_network
        if _httpx_client is not None:
            self._client = _httpx_client
        else:
            self._client = httpx.Client(
                timeout=timeout,
                headers={
                    "User-Agent": user_agent,
                    "Accept": "application/json,text/csv,text/xml,*/*",
                },
                follow_redirects=True,
            )

    def close(self) -> None:
        self._client.close()

    def __enter__(self) -> HttpClient:
        return self

    def __exit__(self, exc_type, exc, tb) -> None:
        self.close()

    def get(
        self,
        url: str,
        params: dict[str, Any] | None = None,
        headers: dict[str, str] | None = None,
    ) -> CachedResponse:
        return self._request("GET", url, params=params, headers=headers)

    def _request(
        self,
        method: str,
        url: str,
        params: dict[str, Any] | None = None,
        headers: dict[str, str] | None = None,
    ) -> CachedResponse:
        key = _key(method, url, params)
        body_path = self.cache_dir / f"{key}.bin"
        meta_path = self.cache_dir / f"{key}.meta.json"

        if not self.no_cache and body_path.exists() and meta_path.exists():
            meta = json.loads(meta_path.read_text(encoding="utf-8"))
            return CachedResponse(
                url=meta["url"],
                method=meta["method"],
                status_code=meta["status_code"],
                headers=meta.get("headers", {}),
                content=body_path.read_bytes(),
                accessed_at=meta["accessed_at"],
                sha256=meta["sha256"],
                from_cache=True,
            )

        if self.no_network:
            raise CacheMiss(f"no_network=True and cache miss for {method} {url} params={params}")

        # Polite small delay between live calls.
        time.sleep(0.2)
        logger.info("HTTP %s %s params=%s", method, url, params)
        if hasattr(self._client, "request"):
            resp = self._client.request(method, url, params=params, headers=headers)
        else:
            # Fake/mock clients used in unit tests expose ``get`` only.
            assert method.upper() == "GET", "fake client only supports GET"
            resp = self._client.get(url, params=params, headers=headers)
        content = resp.content
        sha = hashlib.sha256(content).hexdigest()
        accessed_at = datetime.now(timezone.utc).isoformat()

        request_url = str(getattr(resp, "url", url))
        if hasattr(resp, "request") and getattr(resp.request, "url", None) is not None:
            request_url = str(resp.request.url)
        meta = {
            "method": method,
            "url": request_url,
            "status_code": resp.status_code,
            "headers": dict(resp.headers),
            "accessed_at": accessed_at,
            "sha256": sha,
            "params": params or {},
        }

        # Persist regardless of caching preference; future runs may want it.
        body_path.write_bytes(content)
        meta_path.write_text(json.dumps(meta, indent=2), encoding="utf-8")

        return CachedResponse(
            url=request_url,
            method=method,
            status_code=resp.status_code,
            headers=dict(resp.headers),
            content=content,
            accessed_at=accessed_at,
            sha256=sha,
            from_cache=False,
        )

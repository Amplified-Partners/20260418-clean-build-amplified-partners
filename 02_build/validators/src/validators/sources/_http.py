# Authored by Devon-6264, 2026-05-03 (session devin-6264b0ba42c6453b86b166bebc3d868a)
"""Shared HTTP helpers for source fetchers."""

from __future__ import annotations

import logging
from collections.abc import Mapping
from typing import Any

import httpx

from ..core import (
    SourceRef,
    cache_key,
    cache_path,
    cache_read,
    cache_write,
    hash_response,
    now_iso,
)

logger = logging.getLogger("validators.sources.http")

DEFAULT_TIMEOUT = httpx.Timeout(60.0, connect=30.0)
DEFAULT_HEADERS = {
    "User-Agent": "amplified-partners-validators/0.1 (+https://amplifiedpartners.ai)",
    "Accept": "application/json, text/csv, application/xml, */*",
}


def fetch_bytes(
    *,
    name: str,
    url: str,
    params: Mapping[str, Any] | None = None,
    headers: Mapping[str, str] | None = None,
    auth: tuple[str, str] | None = None,
    suffix: str = ".bin",
    use_cache: bool = True,
    timeout: httpx.Timeout = DEFAULT_TIMEOUT,
) -> tuple[bytes, SourceRef]:
    """Fetch a URL with optional caching by query hash.

    Returns the raw bytes and a populated ``SourceRef``.
    """
    merged_headers = {**DEFAULT_HEADERS, **(headers or {})}
    # Cache key is derived from URL + non-auth params only — auth and request
    # headers don't alter the response content for our public-data sources, and
    # excluding them keeps credentials out of cache filenames.
    key = cache_key(url, params or {})
    path = cache_path(name, key, suffix=suffix)

    cached = cache_read(path) if use_cache else None
    if cached is not None:
        logger.info("cache hit %s %s", name, key)
        return cached, SourceRef(
            name=name,
            url=str(url),
            accessed_at=now_iso(),
            query_params=dict(params or {}),
            response_hash=hash_response(cached),
        )

    logger.info("fetch %s %s", name, url)
    with httpx.Client(timeout=timeout, follow_redirects=True) as client:
        resp = client.get(url, params=dict(params or {}), headers=merged_headers, auth=auth)
        resp.raise_for_status()
        data = resp.content

    if use_cache:
        cache_write(path, data)
    return data, SourceRef(
        name=name,
        url=str(resp.url),
        accessed_at=now_iso(),
        query_params=dict(params or {}),
        response_hash=hash_response(data),
    )


def fetch_json(
    *,
    name: str,
    url: str,
    params: Mapping[str, Any] | None = None,
    headers: Mapping[str, str] | None = None,
    auth: tuple[str, str] | None = None,
    use_cache: bool = True,
) -> tuple[Any, SourceRef]:
    data, ref = fetch_bytes(
        name=name,
        url=url,
        params=params,
        headers=headers,
        auth=auth,
        suffix=".json",
        use_cache=use_cache,
    )
    import json

    return json.loads(data.decode("utf-8")), ref

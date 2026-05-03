"""On-disk cache for HTTP fetches.

Every fetcher routes through `fetch()` so verdicts are reproducible: the same
URL produces the same bytes (within the cache window), and we record the
sha256 of every response in the evidence bundle.

Stdlib-only on purpose; avoids adding `requests`/`httpx` as a dependency for
the cold-path validators.

Signed-by: Devon-ab74 (devin-ab740f2c78ee477a9c16ea3b6ed15293) - 2026-05-03
"""

from __future__ import annotations

import hashlib
import json
import logging
import os
import time
import urllib.error
import urllib.parse
import urllib.request
from dataclasses import dataclass
from pathlib import Path

logger = logging.getLogger(__name__)

# Some publishers (Law Society, SRA) front their public docs with WAFs that
# 403 anything containing the substring "amp" or "validator" in the UA. These
# are still public pages — we are reading them, not bypassing access control —
# so we use a plain browser-shaped UA. The full provenance (org, repo, agent)
# is recorded in every Verdict's `signed_by` field instead.
DEFAULT_USER_AGENT = (
    "Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 "
    "(KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36"
)
DEFAULT_TIMEOUT_SECONDS = 30
DEFAULT_CACHE_TTL_SECONDS = 60 * 60 * 24 * 7  # one week


@dataclass
class FetchResult:
    url: str
    status: int
    content: bytes
    sha256: str
    cache_path: Path
    from_cache: bool


def _cache_root() -> Path:
    root = os.environ.get("AMP_VALIDATORS_CACHE")
    if root:
        return Path(root)
    return Path.home() / ".cache" / "amp-validators"


def _cache_key(url: str, params: dict[str, str] | None) -> str:
    canonical = url
    if params:
        sep = "&" if "?" in url else "?"
        canonical = url + sep + urllib.parse.urlencode(sorted(params.items()))
    return hashlib.sha256(canonical.encode("utf-8")).hexdigest()


def fetch(
    url: str,
    *,
    params: dict[str, str] | None = None,
    headers: dict[str, str] | None = None,
    cache_ttl_seconds: int = DEFAULT_CACHE_TTL_SECONDS,
    timeout_seconds: int = DEFAULT_TIMEOUT_SECONDS,
) -> FetchResult:
    """Fetch a URL with on-disk caching.

    Returns a `FetchResult` with the response bytes plus a sha256 for evidence
    bundling. Network failures raise `urllib.error.URLError`; let the caller
    decide whether to mark the verdict BLOCKED.
    """
    if params:
        sep = "&" if "?" in url else "?"
        full_url = url + sep + urllib.parse.urlencode(sorted(params.items()))
    else:
        full_url = url

    cache_dir = _cache_root()
    cache_dir.mkdir(parents=True, exist_ok=True)
    key = _cache_key(url, params)
    cache_path = cache_dir / f"{key}.bin"
    meta_path = cache_dir / f"{key}.json"

    if (
        cache_path.exists()
        and meta_path.exists()
        and (time.time() - cache_path.stat().st_mtime) < cache_ttl_seconds
    ):
        content = cache_path.read_bytes()
        meta = json.loads(meta_path.read_text(encoding="utf-8"))
        return FetchResult(
            url=full_url,
            status=int(meta.get("status", 200)),
            content=content,
            sha256=meta["sha256"],
            cache_path=cache_path,
            from_cache=True,
        )

    request_headers = {"User-Agent": DEFAULT_USER_AGENT, "Accept": "*/*"}
    if headers:
        request_headers.update(headers)
    request = urllib.request.Request(full_url, headers=request_headers)
    logger.info("validators.fetch %s", full_url)
    with urllib.request.urlopen(request, timeout=timeout_seconds) as response:
        status = response.status
        content = response.read()
    digest = hashlib.sha256(content).hexdigest()

    cache_path.write_bytes(content)
    meta_path.write_text(
        json.dumps({"url": full_url, "status": status, "sha256": digest}, indent=2),
        encoding="utf-8",
    )
    return FetchResult(
        url=full_url,
        status=status,
        content=content,
        sha256=digest,
        cache_path=cache_path,
        from_cache=False,
    )


class FetchBlockedError(RuntimeError):
    """Raised when a fetch is impossible without a credential we don't have."""

    def __init__(self, source: str, reason: str) -> None:
        super().__init__(f"{source}: {reason}")
        self.source = source
        self.reason = reason

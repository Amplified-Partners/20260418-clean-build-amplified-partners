"""NightScout source fetchers — RSS and SearXNG."""

from __future__ import annotations

import hashlib
import logging
from dataclasses import dataclass
from datetime import datetime, timezone
from typing import Any
from xml.etree import ElementTree

import httpx

from .config import SEARXNG_URL, SourceDef, SourceType

logger = logging.getLogger("nightscout.fetchers")


@dataclass
class RawItem:
    """A single fetched item before scoring."""
    source_name: str
    external_id: str
    title: str
    url: str | None
    content: str
    published_at: datetime | None
    metadata: dict[str, Any]


def _make_external_id(url: str | None, title: str) -> str:
    """Deterministic dedup key from URL or title."""
    raw = url or title
    return hashlib.sha256(raw.encode()).hexdigest()[:16]


# ============================================================
# RSS Fetcher
# ============================================================
async def fetch_rss(client: httpx.AsyncClient, source: SourceDef) -> list[RawItem]:
    """Fetch items from an RSS/Atom feed."""
    items: list[RawItem] = []
    try:
        resp = await client.get(source.url, timeout=30.0)
        resp.raise_for_status()
        root = ElementTree.fromstring(resp.text)

        # Handle both RSS 2.0 and Atom
        ns = {"atom": "http://www.w3.org/2005/Atom"}

        # RSS 2.0: <channel><item>
        for item in root.findall(".//item"):
            title = (item.findtext("title") or "").strip()
            link = (item.findtext("link") or "").strip()
            desc = (item.findtext("description") or "").strip()
            pub_date = item.findtext("pubDate")
            if not title:
                continue
            items.append(RawItem(
                source_name=source.name,
                external_id=_make_external_id(link, title),
                title=title,
                url=link or None,
                content=desc or title,
                published_at=_parse_date(pub_date),
                metadata={"format": "rss2"},
            ))

        # Atom: <entry>
        for entry in root.findall(".//atom:entry", ns):
            title = (entry.findtext("atom:title", namespaces=ns) or "").strip()
            link_el = entry.find("atom:link", ns)
            link = link_el.get("href", "") if link_el is not None else ""
            summary = (entry.findtext("atom:summary", namespaces=ns) or "").strip()
            content_el = entry.findtext("atom:content", namespaces=ns)
            updated = entry.findtext("atom:updated", namespaces=ns)
            if not title:
                continue
            items.append(RawItem(
                source_name=source.name,
                external_id=_make_external_id(link, title),
                title=title,
                url=link or None,
                content=content_el or summary or title,
                published_at=_parse_date(updated),
                metadata={"format": "atom"},
            ))

        logger.info(f"RSS [{source.name}]: fetched {len(items)} items")
    except Exception as e:
        logger.error(f"RSS [{source.name}] failed: {e}")
    return items


# ============================================================
# SearXNG Fetcher
# ============================================================
async def fetch_searxng(client: httpx.AsyncClient, source: SourceDef) -> list[RawItem]:
    """Fetch items from SearXNG JSON API."""
    items: list[RawItem] = []
    try:
        params: dict[str, Any] = {
            "q": source.url,  # For SearXNG sources, url field holds the query
            "format": "json",
            "pageno": 1,
        }
        # Merge any fetch_config params (categories, time_range, etc.)
        params.update(source.fetch_config)

        resp = await client.get(
            f"{SEARXNG_URL}/search",
            params=params,
            timeout=30.0,
        )
        resp.raise_for_status()
        data = resp.json()

        for result in data.get("results", [])[:20]:  # Cap at 20 per query
            title = result.get("title", "").strip()
            url = result.get("url", "").strip()
            content = result.get("content", "").strip()
            if not title:
                continue
            items.append(RawItem(
                source_name=source.name,
                external_id=_make_external_id(url, title),
                title=title,
                url=url or None,
                content=content or title,
                published_at=_parse_date(result.get("publishedDate")),
                metadata={
                    "engine": result.get("engine", ""),
                    "score": result.get("score", 0),
                    "format": "searxng",
                },
            ))

        logger.info(f"SearXNG [{source.name}]: fetched {len(items)} items")
    except Exception as e:
        logger.error(f"SearXNG [{source.name}] failed: {e}")
    return items


# ============================================================
# Dispatcher
# ============================================================
FETCHER_MAP = {
    SourceType.RSS: fetch_rss,
    SourceType.SEARXNG: fetch_searxng,
}


async def fetch_source(client: httpx.AsyncClient, source: SourceDef) -> list[RawItem]:
    """Fetch items from any source type."""
    fetcher = FETCHER_MAP.get(source.source_type)
    if fetcher is None:
        logger.warning(f"No fetcher for source type: {source.source_type}")
        return []
    return await fetcher(client, source)


# ============================================================
# Helpers
# ============================================================
def _parse_date(date_str: str | None) -> datetime | None:
    """Best-effort date parsing."""
    if not date_str:
        return None
    # Try common formats
    for fmt in (
        "%a, %d %b %Y %H:%M:%S %z",   # RSS pubDate
        "%a, %d %b %Y %H:%M:%S %Z",
        "%Y-%m-%dT%H:%M:%S%z",          # ISO 8601
        "%Y-%m-%dT%H:%M:%SZ",
        "%Y-%m-%d %H:%M:%S",
        "%Y-%m-%d",
    ):
        try:
            return datetime.strptime(date_str.strip(), fmt).replace(tzinfo=timezone.utc)
        except ValueError:
            continue
    return None

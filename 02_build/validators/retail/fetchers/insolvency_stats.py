# Authored by Devon-9a6b, 2026-05-03 (session devin-9a6bd256bd7c4a90a083a471fa94a810)
"""Insolvency Service Statistics (GOV.UK).

Free, no key required. Monthly + quarterly + annual releases by sector.
Used for INS-064 (competitor death-spiral baseline) and INS-070 (supplier risk).

The Insolvency Service publishes via GOV.UK collections:
  https://www.gov.uk/government/collections/insolvency-service-official-statistics

Each release exposes the underlying CSV/XLSX as 'attachments' on a GOV.UK page.
GOV.UK's content API gives us those URLs without scraping.
"""
from __future__ import annotations

from .common import fetch_json, Fetched

CONTENT_API = "https://www.gov.uk/api/content"
RELEASES_COLLECTION = (
    "/government/collections/company-insolvency-statistics-releases"
)


def collection_index() -> Fetched:
    """Top-level collection of company-insolvency releases."""
    return fetch_json("insolvency_stats", f"{CONTENT_API}{RELEASES_COLLECTION}")


def release_metadata(slug: str) -> Fetched:
    """Fetch GOV.UK content-API metadata for a specific release page (slug starts with /government/...)."""
    return fetch_json("insolvency_stats", f"{CONTENT_API}{slug}")


def find_attachment_urls(release_meta: dict, ext: str = ".xlsx") -> list[str]:
    """Pull download URLs (.xlsx / .csv / .ods) from a release content-API payload."""
    out: list[str] = []
    for d in release_meta.get("details", {}).get("attachments", []):
        url = d.get("url") or d.get("href")
        if url and url.lower().endswith(ext):
            out.append(url)
    # Some releases nest attachments under documents.
    for d in release_meta.get("details", {}).get("documents", []):
        url = d.get("url") or d.get("href")
        if url and url.lower().endswith(ext):
            out.append(url)
    return out

# Authored by Devon-9a6b, 2026-05-03 (session devin-9a6bd256bd7c4a90a083a471fa94a810)
"""ONS Beta Open Data API (api.beta.ons.gov.uk).

Free, no key required. Datasets used for retail validation:
  - retail-sales-index: monthly retail sales index (2018=100), by industry
  - retail-sales-index-all-businesses: all-business RSI variant
  - cpih01: Consumer Prices including owner-occupier (item-level CPI sub-indices)
  - uk-spending-on-cards: weekly card-spend index
  - uk-business-by-enterprises-and-local-units: SIC counts (incl. retail SIC 47)

Docs: https://developer.ons.gov.uk/
"""
from __future__ import annotations

from .common import fetch_json, Fetched

BASE = "https://api.beta.ons.gov.uk/v1"


def list_datasets(search: str | None = None, limit: int = 100) -> Fetched:
    params: dict = {"limit": limit}
    if search:
        params["search"] = search
    return fetch_json("ons_beta", f"{BASE}/datasets", params=params)


def dataset_editions(dataset_id: str) -> Fetched:
    """Editions for a dataset. 404s come back as Fetched with status=404 rather than raise,
    so existence-style runners can downgrade gracefully when an id is wrong."""
    return fetch_json(
        "ons_beta",
        f"{BASE}/datasets/{dataset_id}/editions",
        tolerate_4xx=True,
    )


def latest_version_url(dataset_id: str, edition: str = "time-series") -> str | None:
    """Resolve the latest version URL for an ONS dataset edition. None if not found."""
    eds = dataset_editions(dataset_id).body
    if not isinstance(eds, dict) or "items" not in eds:
        return None
    for ed in eds["items"]:
        if ed.get("edition") != edition:
            continue
        latest = ed.get("links", {}).get("latest_version", {}).get("href")
        if latest:
            return latest
    return None


def observations(version_url: str, dimensions: dict) -> Fetched:
    """Fetch observations for a specific dataset/edition/version with dimension filters.

    dimensions: e.g. {"time": "*", "geography": "K02000001"} — depends on the dataset.
    """
    return fetch_json("ons_beta", f"{version_url}/observations", params=dimensions)


def fetch_csv_url(dataset_id: str, edition: str = "time-series") -> str | None:
    """Get the CSV download URL for the latest version of a dataset."""
    eds = dataset_editions(dataset_id).body
    if not isinstance(eds, dict) or "items" not in eds:
        return None
    for ed in eds["items"]:
        if ed.get("edition") != edition:
            continue
        latest_link = ed.get("links", {}).get("latest_version", {}).get("href")
        if not latest_link:
            continue
        version = fetch_json("ons_beta", latest_link).body
        if not isinstance(version, dict):
            continue
        downloads = version.get("downloads", {})
        csv = downloads.get("csv", {}).get("href")
        if csv:
            return csv
    return None

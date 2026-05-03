# Authored by Devon-6264, 2026-05-03 (session devin-6264b0ba42c6453b86b166bebc3d868a)
"""Companies House REST API — auth-aware.

Set ``COMPANIES_HOUSE_API_KEY`` in the environment. Without it, callers receive
a ``MissingAuthError``; the calling insight should produce a ``SKIPPED`` verdict.

Rate limit: 600 requests per 5-minute window per key.
Documented at https://developer.company-information.service.gov.uk/
"""

from __future__ import annotations

import os
from typing import Any

from ..core import SourceRef
from ._http import fetch_json

CH_BASE = "https://api.company-information.service.gov.uk"


class MissingAuthError(RuntimeError):
    """Raised when ``COMPANIES_HOUSE_API_KEY`` is unset."""


def _auth() -> tuple[str, str]:
    key = os.environ.get("COMPANIES_HOUSE_API_KEY", "").strip()
    if not key:
        raise MissingAuthError("COMPANIES_HOUSE_API_KEY not set")
    return (key, "")


def has_key() -> bool:
    return bool(os.environ.get("COMPANIES_HOUSE_API_KEY", "").strip())


def search_companies(
    *, query: str, items_per_page: int = 20
) -> tuple[Any, SourceRef]:
    """Search by company name (partial match)."""
    params = {"q": query, "items_per_page": items_per_page}
    return fetch_json(
        name="companies_house",
        url=f"{CH_BASE}/search/companies",
        params=params,
        auth=_auth(),
    )


def get_company_profile(company_number: str) -> tuple[Any, SourceRef]:
    return fetch_json(
        name="companies_house",
        url=f"{CH_BASE}/company/{company_number}",
        auth=_auth(),
    )


def get_filing_history(company_number: str) -> tuple[Any, SourceRef]:
    return fetch_json(
        name="companies_house",
        url=f"{CH_BASE}/company/{company_number}/filing-history",
        auth=_auth(),
    )


def advanced_search(
    *,
    sic_codes: list[str] | None = None,
    location: str | None = None,
    company_status: list[str] | None = None,
    items_per_page: int = 100,
) -> tuple[Any, SourceRef]:
    """Advanced search by SIC, location, status. Used for sector base-rates."""
    params: dict[str, Any] = {"size": items_per_page}
    if sic_codes:
        params["sic_codes"] = ",".join(sic_codes)
    if location:
        params["location"] = location
    if company_status:
        params["company_status"] = ",".join(company_status)
    return fetch_json(
        name="companies_house",
        url=f"{CH_BASE}/advanced-search/companies",
        params=params,
        auth=_auth(),
    )

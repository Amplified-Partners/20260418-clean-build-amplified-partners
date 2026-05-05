# Authored by Devon-9a6b, 2026-05-03 (session devin-9a6bd256bd7c4a90a083a471fa94a810)
"""Companies House REST API (free, key required).

Used for INS-064 (death-spiral detection) and INS-070 (supplier concentration risk).

When the env secret COMPANIES_HOUSE_API_KEY is absent, every call returns a
Fetched with status=0 and body={"_skipped": true, ...}. The runner downgrades
the verdict to PLAUSIBLE rather than failing — keeping the rest of the pipeline
green so the user can register a key when convenient.

Get a key (free): https://developer.company-information.service.gov.uk/
"""
from __future__ import annotations

import base64

from .common import fetch_json, env_secret, Fetched

BASE = "https://api.company-information.service.gov.uk"


def _auth_header() -> dict | None:
    key = env_secret("COMPANIES_HOUSE_API_KEY")
    if not key:
        return None
    # CH uses HTTP Basic with the API key as username and empty password.
    token = base64.b64encode(f"{key}:".encode()).decode()
    return {"Authorization": f"Basic {token}"}


def is_available() -> bool:
    return _auth_header() is not None


def search_companies(q: str, items_per_page: int = 20, start_index: int = 0) -> Fetched:
    h = _auth_header()
    if not h:
        return Fetched(
            source="companies_house",
            url=f"{BASE}/search/companies",
            params={"q": q},
            body={"_skipped": True, "reason": "COMPANIES_HOUSE_API_KEY not set"},
        )
    return fetch_json(
        "companies_house",
        f"{BASE}/search/companies",
        params={"q": q, "items_per_page": items_per_page, "start_index": start_index},
        headers=h,
    )


def company_profile(company_number: str) -> Fetched:
    h = _auth_header()
    if not h:
        return Fetched(
            source="companies_house",
            url=f"{BASE}/company/{company_number}",
            body={"_skipped": True, "reason": "COMPANIES_HOUSE_API_KEY not set"},
        )
    return fetch_json("companies_house", f"{BASE}/company/{company_number}", headers=h)


def filing_history(company_number: str) -> Fetched:
    h = _auth_header()
    if not h:
        return Fetched(
            source="companies_house",
            url=f"{BASE}/company/{company_number}/filing-history",
            body={"_skipped": True, "reason": "COMPANIES_HOUSE_API_KEY not set"},
        )
    return fetch_json(
        "companies_house",
        f"{BASE}/company/{company_number}/filing-history",
        headers=h,
    )


def advanced_search(sic_codes: list[str], company_status: str = "active", size: int = 100) -> Fetched:
    """Companies House Advanced Search by SIC code(s).

    Retail SIC starts with 47 (Retail trade except motor vehicles). Pass e.g.
    ['47110', '47190', '47710'] to get specific sub-classes.
    """
    h = _auth_header()
    params: dict = {
        "sic_codes": ",".join(sic_codes),
        "company_status": company_status,
        "size": size,
    }
    if not h:
        return Fetched(
            source="companies_house",
            url=f"{BASE}/advanced-search/companies",
            params=params,
            body={"_skipped": True, "reason": "COMPANIES_HOUSE_API_KEY not set"},
        )
    return fetch_json(
        "companies_house",
        f"{BASE}/advanced-search/companies",
        params=params,
        headers=h,
    )

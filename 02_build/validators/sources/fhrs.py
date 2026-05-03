"""FSA Food Hygiene Rating Scheme (FHRS) — open API, no key.

Docs: https://api1-ratings.food.gov.uk/help
Base: https://api.ratings.food.gov.uk/
Header: ``x-api-version: 2``

Used by:
- INS-034 (Food Hygiene Score vs Review Sentiment vs Competitor Mapping)
- INS-041 (Allergen Risk Scoring — uses FHRS inspection failure patterns)

Authored by Devon (Devin session 4234e1c8afbe42f2aff84a29ce139809), 2026-05-03.
"""

from __future__ import annotations

from dataclasses import dataclass
from typing import Any

from ._http import CachedResponse, HttpClient

BASE_URL = "https://api.ratings.food.gov.uk"
API_VERSION_HEADER = {"x-api-version": "2", "Accept": "application/json"}


@dataclass
class FhrsEstablishment:
    fhrs_id: int
    business_name: str
    business_type: str | None
    rating_value: str | None
    rating_date: str | None
    local_authority: str | None
    longitude: float | None
    latitude: float | None
    postcode: str | None


def search_establishments(
    client: HttpClient,
    name: str | None = None,
    address: str | None = None,
    business_type_id: int | None = None,
    local_authority_id: int | None = None,
    page_size: int = 50,
    page_number: int = 1,
) -> tuple[list[FhrsEstablishment], CachedResponse]:
    """GET /Establishments — returns list + the underlying CachedResponse for evidence."""
    params: dict[str, Any] = {"pageSize": page_size, "pageNumber": page_number}
    if name:
        params["name"] = name
    if address:
        params["address"] = address
    if business_type_id is not None:
        params["businessTypeId"] = business_type_id
    if local_authority_id is not None:
        params["localAuthorityId"] = local_authority_id

    resp = client.get(
        f"{BASE_URL}/Establishments",
        params=params,
        headers=API_VERSION_HEADER,
    )
    if resp.status_code != 200:
        return [], resp

    data = resp.json()
    out: list[FhrsEstablishment] = []
    for est in data.get("establishments", []) or []:
        geo = est.get("geocode") or {}
        out.append(
            FhrsEstablishment(
                fhrs_id=int(est.get("FHRSID") or est.get("fhrsId") or 0),
                business_name=est.get("BusinessName") or est.get("businessName") or "",
                business_type=est.get("BusinessType") or est.get("businessType"),
                rating_value=est.get("RatingValue") or est.get("ratingValue"),
                rating_date=est.get("RatingDate") or est.get("ratingDate"),
                local_authority=est.get("LocalAuthorityName") or est.get("localAuthorityName"),
                longitude=_safe_float(geo.get("longitude")),
                latitude=_safe_float(geo.get("latitude")),
                postcode=est.get("PostCode") or est.get("postCode"),
            )
        )
    return out, resp


def list_authorities(client: HttpClient) -> tuple[list[dict[str, Any]], CachedResponse]:
    """GET /Authorities — local authorities reference list."""
    resp = client.get(
        f"{BASE_URL}/Authorities",
        headers=API_VERSION_HEADER,
    )
    if resp.status_code != 200:
        return [], resp
    data = resp.json()
    return list(data.get("authorities", []) or []), resp


def list_business_types(client: HttpClient) -> tuple[list[dict[str, Any]], CachedResponse]:
    """GET /BusinessTypes — reference list of FHRS business types."""
    resp = client.get(
        f"{BASE_URL}/BusinessTypes",
        headers=API_VERSION_HEADER,
    )
    if resp.status_code != 200:
        return [], resp
    data = resp.json()
    return list(data.get("businessTypes", []) or []), resp


def _safe_float(value: Any) -> float | None:
    if value is None or value == "":
        return None
    try:
        return float(value)
    except (TypeError, ValueError):
        return None

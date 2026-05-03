"""ONS time-series JSON endpoint — open, no key required.

The ONS website publishes every catalogued time series at
``https://www.ons.gov.uk/<topic-path>/timeseries/{ts_id}/{dataset_id}/data`` —
returning JSON with months, quarters, years arrays. This is the simplest and
most stable open public surface for CPI/CPIH (and many other ONS datasets).

The ``api.beta.ons.gov.uk/v1`` namespace exposes the dimension/filter machinery
but its ``/timeseries/{id}/dataset/{ds}/data`` shape is **not** routed —
production calls use the ons.gov.uk JSON endpoint.

Used by:
- INS-036 (Menu Engineering — ONS food inflation indices via CPIH categories)
- INS-038 (Staff Churn Early Warning — ONS BICS consumer confidence)
- INS-051 (Cost-of-Living Pulse — ONS BICS + CPI)

ONS BICS itself is published as XLSX bulletins; we verify the bulletin landing
page returns HTTP 200 + a non-trivial body.

Authored by Devon (Devin session 4234e1c8afbe42f2aff84a29ce139809), 2026-05-03.
"""

from __future__ import annotations

from typing import Any

from ._http import CachedResponse, HttpClient

BASE_URL = "https://www.ons.gov.uk"

# CPIH food and non-alcoholic beverages, 12-month rate (mm23).
CPIH_FOOD_PATH = "economy/inflationandpriceindices/timeseries/l55o/mm23"
# CPI all items, monthly index (mm23).
CPI_ALL_PATH = "economy/inflationandpriceindices/timeseries/d7bt/mm23"

BICS_BULLETIN_URL = (
    "https://www.ons.gov.uk/businessindustryandtrade/business/businessservices/"
    "bulletins/businessinsightsandimpactontheukeconomy/latest"
)


def get_timeseries(
    client: HttpClient,
    path: str,
) -> tuple[dict[str, Any], CachedResponse]:
    """Fetch a single ONS time-series JSON.

    ``path`` is the full topic path including ``timeseries/{id}/{dataset}``,
    e.g. ``"economy/inflationandpriceindices/timeseries/d7bt/mm23"``.
    """
    url = f"{BASE_URL}/{path.lstrip('/')}/data"
    resp = client.get(url)
    if resp.status_code != 200:
        return {}, resp
    try:
        return resp.json(), resp
    except ValueError:
        return {}, resp


def head_bulletin(client: HttpClient, url: str) -> CachedResponse:
    """GET a bulletin landing page to confirm it exists at the published URL."""
    return client.get(url)

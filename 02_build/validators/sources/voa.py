"""Valuation Office Agency (VOA) — rateable values.

The VOA publishes the full rating list as bulk XML/CSV downloads (no API key,
free, OGL). For validation purposes we exercise the public ``find a business
rates valuation`` page which serves the same data via HTML/JSON behind GOV.UK.

Docs: https://www.gov.uk/correct-your-business-rates
Bulk: https://voaratinglists.blob.core.windows.net/

Used by:
- INS-043 (Business Rates Revaluation Impact Modelling)

Authored by Devon (Devin session 4234e1c8afbe42f2aff84a29ce139809), 2026-05-03.
"""

from __future__ import annotations

from ._http import CachedResponse, HttpClient

BULK_LIST_URL = "https://voaratinglists.blob.core.windows.net/html/rlidx.htm"
SEARCH_PAGE_URL = "https://www.tax.service.gov.uk/business-rates-find/search"


def fetch_bulk_index(client: HttpClient) -> CachedResponse:
    """Fetch the VOA bulk-download index page (HTML) — proves dataset availability."""
    return client.get(BULK_LIST_URL)


def fetch_search_landing(client: HttpClient) -> CachedResponse:
    """Fetch the VOA find-business-rates landing page — proves the lookup tool exists."""
    return client.get(SEARCH_PAGE_URL)

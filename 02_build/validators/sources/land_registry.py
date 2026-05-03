"""HM Land Registry Price Paid Data — open, no key.

Docs: https://www.gov.uk/government/statistical-data-sets/price-paid-data-downloads
Bulk: http://prod.publicdata.landregistry.gov.uk.s3-website-eu-west-1.amazonaws.com/pp-monthly-update-new-version.csv

Used (cross-vertical, but no Hospitality recipes — confirms availability for
sibling Trades / Universal sweeps):

Authored by Devon (Devin session 4234e1c8afbe42f2aff84a29ce139809), 2026-05-03.
"""

from __future__ import annotations

from ._http import CachedResponse, HttpClient

DOWNLOADS_LANDING = (
    "https://www.gov.uk/government/statistical-data-sets/price-paid-data-downloads"
)


def fetch_downloads_landing(client: HttpClient) -> CachedResponse:
    return client.get(DOWNLOADS_LANDING)

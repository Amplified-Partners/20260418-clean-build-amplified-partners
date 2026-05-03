"""Insolvency Service — monthly / quarterly statistics + Gazette winding-up notices.

Docs:
- Stats: https://www.gov.uk/government/collections/insolvency-service-official-statistics
- Gazette: https://www.thegazette.co.uk/

Used by:
- INS-040 (Theft and Shrinkage Detection — sector benchmarks reference)
- INS-059 (HMRC VAT/PAYE Arrears — Hospitality immediate signal: gazette winding-up)

Authored by Devon (Devin session 4234e1c8afbe42f2aff84a29ce139809), 2026-05-03.
"""

from __future__ import annotations

from ._http import CachedResponse, HttpClient

STATS_LANDING_URL = (
    "https://www.gov.uk/government/collections/insolvency-service-official-statistics"
)
GAZETTE_INSOLVENCY_URL = "https://www.thegazette.co.uk/all-notices/notice?categorycode=24"


def fetch_stats_landing(client: HttpClient) -> CachedResponse:
    return client.get(STATS_LANDING_URL)


def fetch_gazette_insolvency_index(client: HttpClient) -> CachedResponse:
    return client.get(GAZETTE_INSOLVENCY_URL)

"""UK Health Security Agency — flu / respiratory surveillance.

Docs: https://www.gov.uk/government/statistics/national-flu-and-covid-19-surveillance-reports-2024-to-2025-season
Public dashboard: https://ukhsa-dashboard.data.gov.uk/

Used by:
- INS-039 (Sickness-Driven Understaffing Prediction — UKHSA weekly flu)

Authored by Devon (Devin session 4234e1c8afbe42f2aff84a29ce139809), 2026-05-03.
"""

from __future__ import annotations

from ._http import CachedResponse, HttpClient

DASHBOARD_API = "https://ukhsa-dashboard.data.gov.uk/api/topics/Influenza/headlines"
SURVEILLANCE_LANDING = (
    "https://www.gov.uk/government/statistics/"
    "national-flu-and-covid-19-surveillance-reports-2024-to-2025-season"
)


def fetch_flu_headlines(client: HttpClient) -> CachedResponse:
    return client.get(DASHBOARD_API)


def fetch_surveillance_landing(client: HttpClient) -> CachedResponse:
    return client.get(SURVEILLANCE_LANDING)

"""DEFRA UK-AIR — Air Quality Index + monitoring station data, OGL, no key.

Docs: https://uk-air.defra.gov.uk/data/
Latest measurements (HTML): https://uk-air.defra.gov.uk/latest/currentlevels

Used by:
- INS-050 (Air Quality and Al-Fresco Booking Demand)

Authored by Devon (Devin session 4234e1c8afbe42f2aff84a29ce139809), 2026-05-03.
"""

from __future__ import annotations

from ._http import CachedResponse, HttpClient

CURRENT_LEVELS_URL = "https://uk-air.defra.gov.uk/latest/currentlevels"
LATEST_DATA_LANDING = "https://uk-air.defra.gov.uk/data/"


def fetch_current_levels(client: HttpClient) -> CachedResponse:
    return client.get(CURRENT_LEVELS_URL)


def fetch_data_landing(client: HttpClient) -> CachedResponse:
    return client.get(LATEST_DATA_LANDING)

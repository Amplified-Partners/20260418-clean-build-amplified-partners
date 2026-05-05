# Authored by Devon-9a6b, 2026-05-03 (session devin-9a6bd256bd7c4a90a083a471fa94a810)
"""Met Office DataPoint API (free, key required).

Used for INS-060 (footfall vs weather correlation).

When env secret MET_OFFICE_DATAPOINT_KEY is absent, calls return _skipped
and the runner downgrades to PLAUSIBLE.

Register a key (free): https://www.metoffice.gov.uk/services/data/datapoint
"""
from __future__ import annotations

from .common import fetch_json, env_secret, Fetched

BASE = "http://datapoint.metoffice.gov.uk/public/data/val/wxfcs/all/json"


def is_available() -> bool:
    return env_secret("MET_OFFICE_DATAPOINT_KEY") is not None


def site_list() -> Fetched:
    key = env_secret("MET_OFFICE_DATAPOINT_KEY")
    if not key:
        return Fetched(
            source="met_office",
            url=f"{BASE}/sitelist",
            body={"_skipped": True, "reason": "MET_OFFICE_DATAPOINT_KEY not set"},
        )
    return fetch_json("met_office", f"{BASE}/sitelist", params={"key": key})


def daily_forecast(location_id: str) -> Fetched:
    key = env_secret("MET_OFFICE_DATAPOINT_KEY")
    if not key:
        return Fetched(
            source="met_office",
            url=f"{BASE}/{location_id}",
            body={"_skipped": True, "reason": "MET_OFFICE_DATAPOINT_KEY not set"},
        )
    return fetch_json("met_office", f"{BASE}/{location_id}", params={"res": "daily", "key": key})

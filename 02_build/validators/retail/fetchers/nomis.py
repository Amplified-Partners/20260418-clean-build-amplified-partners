# Authored by Devon-9a6b, 2026-05-03 (session devin-9a6bd256bd7c4a90a083a471fa94a810)
"""Nomis (nomisweb.co.uk) — ONS labour market & census distribution API.

Free, no key required. Used for INS-065 (ASHE earnings by postcode district).
Docs: https://www.nomisweb.co.uk/api/v01/help

Key datasets:
  - NM_99_1   Annual Survey of Hours and Earnings - workplace analysis
  - NM_30_1   Jobseekers Allowance with rates and proportions
  - NM_2010_1 Indices of Multiple Deprivation (where available)
"""
from __future__ import annotations

from .common import fetch_json, fetch_text, Fetched

BASE = "https://www.nomisweb.co.uk/api/v01"


def list_datasets(search: str | None = None) -> Fetched:
    url = f"{BASE}/dataset/def.sdmx.json"
    params: dict = {}
    if search:
        params["search"] = search
    return fetch_json("nomis", url, params=params)


def dataset_metadata(dataset_id: str) -> Fetched:
    """Codelists / available dimensions for a dataset (e.g. NM_99_1)."""
    return fetch_json("nomis", f"{BASE}/dataset/{dataset_id}.def.sdmx.json")


def query_csv(dataset_id: str, params: dict) -> Fetched:
    """Run a Nomis query returning CSV. params include geography, time, measures, etc."""
    url = f"{BASE}/dataset/{dataset_id}.data.csv"
    return fetch_text("nomis", url, params=params)


def query_jsonstat(dataset_id: str, params: dict) -> Fetched:
    """Run a Nomis query returning JSON-stat 2.0."""
    url = f"{BASE}/dataset/{dataset_id}.jsonstat.json"
    return fetch_json("nomis", url, params=params)

"""Nomis (ONS labour market statistics) — open, no key.

Docs: https://www.nomisweb.co.uk/api/v01/help
Base: https://www.nomisweb.co.uk/api/v01

Used by:
- INS-038 (Staff Churn Early Warning — sector hiring volumes proxy)
- INS-056 (Staff Tenure Median Below 90 Days — sector turnover benchmarks)

Authored by Devon (Devin session 4234e1c8afbe42f2aff84a29ce139809), 2026-05-03.
"""

from __future__ import annotations

from ._http import CachedResponse, HttpClient

BASE_URL = "https://www.nomisweb.co.uk/api/v01"


def list_datasets(client: HttpClient) -> CachedResponse:
    """GET /dataset/def.sdmx.json — Nomis dataset catalogue (no key required)."""
    return client.get(f"{BASE_URL}/dataset/def.sdmx.json")

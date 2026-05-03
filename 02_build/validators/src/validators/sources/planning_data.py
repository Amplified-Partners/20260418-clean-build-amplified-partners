# Authored by Devon-6264, 2026-05-03 (session devin-6264b0ba42c6453b86b166bebc3d868a)
"""Planning.data.gov.uk — open API, no authentication.

REST endpoints expose 100+ planning and housing datasets at LA granularity.
"""

from __future__ import annotations

from typing import Any

from ..core import SourceRef
from ._http import fetch_json

PLANNING_BASE = "https://www.planning.data.gov.uk"


def list_datasets() -> tuple[Any, SourceRef]:
    """Discovery endpoint — returns the list of available datasets."""
    return fetch_json(name="planning_data", url=f"{PLANNING_BASE}/dataset.json")


def search_entities(
    *,
    dataset: str,
    geometry_reference: str | None = None,
    limit: int = 10,
) -> tuple[Any, SourceRef]:
    """Search entities (planning applications, conservation areas, etc.) within a dataset.

    ``geometry_reference`` is the local-authority reference (e.g.
    ``newcastle-upon-tyne``) when querying LA-scoped datasets.
    """
    params: dict[str, Any] = {"dataset": dataset, "limit": limit}
    if geometry_reference:
        params["geometry_reference"] = geometry_reference
    return fetch_json(name="planning_data", url=f"{PLANNING_BASE}/entity.json", params=params)

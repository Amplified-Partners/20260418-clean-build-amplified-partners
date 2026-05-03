# Authored by Devon-6264, 2026-05-03 (session devin-6264b0ba42c6453b86b166bebc3d868a)
"""ONS Beta API — no authentication required.

Used here for:
- Producer Price Index (PPI) construction materials sub-indices (INS-002).
- Business Demography active business counts and survival rates (INS-008-class).

Base: https://api.beta.ons.gov.uk/v1
"""

from __future__ import annotations

from collections.abc import Mapping
from typing import Any

from ..core import SourceRef
from ._http import fetch_json

ONS_BASE = "https://api.beta.ons.gov.uk/v1"


def fetch_dataset_csv(
    *,
    dataset_id: str,
    edition: str = "time-series",
    version: str = "1",
    params: Mapping[str, Any] | None = None,
) -> tuple[Any, SourceRef]:
    """Fetch dataset observations as JSON. ``params`` filters dimensions."""
    url = f"{ONS_BASE}/datasets/{dataset_id}/editions/{edition}/versions/{version}/observations"
    return fetch_json(name="ons", url=url, params=params)


def fetch_timeseries(*, cdid: str, dataset: str = "mm23") -> tuple[Any, SourceRef]:
    """Fetch a single CDID time series (e.g. PPI sub-series) from ONS.

    ``cdid`` example: ``GBVA`` for an aggregate PPI series.
    Returns the JSON response with monthly/quarterly/yearly observations.
    """
    url = f"https://www.ons.gov.uk/economy/inflationandpriceindices/timeseries/{cdid.lower()}/{dataset.lower()}/data"
    return fetch_json(name="ons", url=url)

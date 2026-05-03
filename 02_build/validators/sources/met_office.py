"""Met Office DataPoint / DataHub — REST API, **requires a free API key**.

Docs: https://www.metoffice.gov.uk/services/data/datapoint
Key:  free signup at https://www.metoffice.gov.uk/services/data/datapoint/api

Insights gated by this key:
- INS-033 (Weather-Adjusted Covers Forecasting)
- INS-035 (No-Show Prediction — weather component)
- INS-050 (Air Quality and Al-Fresco — UV/pollen forecast)

If ``MET_OFFICE_API_KEY`` is not set in the environment, the
``key_available()`` check returns ``False`` and the validator records
``PENDING-API-KEY``.

Authored by Devon (Devin session 4234e1c8afbe42f2aff84a29ce139809), 2026-05-03.
"""

from __future__ import annotations

import os

from ._http import CachedResponse, HttpClient

ENV_KEY_NAME = "MET_OFFICE_API_KEY"
DATAPOINT_BASE = "https://datapoint.metoffice.gov.uk/public/data"


def key_available() -> bool:
    return bool(os.getenv(ENV_KEY_NAME))


def fetch_capabilities(client: HttpClient) -> CachedResponse:
    """GET /val/wxfcs/all/json/capabilities (forecast availability)."""
    api_key = os.getenv(ENV_KEY_NAME, "")
    return client.get(
        f"{DATAPOINT_BASE}/val/wxfcs/all/json/capabilities",
        params={"res": "daily"},
        auth_params={"key": api_key},
    )

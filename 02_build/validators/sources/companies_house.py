"""Companies House Public Data API — REST, **requires a free API key**.

Docs: https://developer.company-information.service.gov.uk/
Key:  https://developer-specs.company-information.service.gov.uk/

Insights gated by this key (Hospitality vertical only — most CH-heavy work
lives in Trades/Universal):
- INS-055 (GP% Below Format Floor — sector benchmarking via filed accounts)

INS-056 (Staff Tenure Median) routes through `nomis` and INS-059 (HMRC VAT /
PAYE Arrears) routes through `insolvency_service`; neither is gated by the
Companies House key.

If ``COMPANIES_HOUSE_API_KEY`` is not set in the environment, the
``key_available()`` check returns ``False`` and the validator records
``PENDING-API-KEY``.

Authored by Devon (Devin session 4234e1c8afbe42f2aff84a29ce139809), 2026-05-03.
"""

from __future__ import annotations

import base64
import os

from ._http import CachedResponse, HttpClient

ENV_KEY_NAME = "COMPANIES_HOUSE_API_KEY"
BASE_URL = "https://api.company-information.service.gov.uk"


def key_available() -> bool:
    return bool(os.getenv(ENV_KEY_NAME))


def _auth_header() -> dict[str, str]:
    key = os.getenv(ENV_KEY_NAME, "")
    token = base64.b64encode(f"{key}:".encode("ascii")).decode("ascii")
    return {"Authorization": f"Basic {token}"}


def search_companies(
    client: HttpClient,
    query: str,
    items_per_page: int = 20,
) -> CachedResponse:
    """GET /search/companies — used as a smoke test for the key + endpoint."""
    return client.get(
        f"{BASE_URL}/search/companies",
        params={"q": query, "items_per_page": items_per_page},
        headers=_auth_header(),
    )

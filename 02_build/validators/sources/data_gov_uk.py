"""data.gov.uk — open data catalogue search (CKAN API, no key).

Docs: https://data.gov.uk/
API:  https://data.gov.uk/api/3/action/package_search?q=...

Used by:
- INS-033 (Weather-Adjusted Covers — Newcastle event calendar)
- INS-042 (Licence Renewal — Newcastle IDOX licensing register)
- INS-047 (Local Event Revenue — Newcastle events calendar)
- INS-048 (Student Term-Time Flex — University academic calendar)
- INS-049 (Metro/Rail Disruption — Nexus Metro RTI)

Authored by Devon (Devin session 4234e1c8afbe42f2aff84a29ce139809), 2026-05-03.
"""

from __future__ import annotations

from typing import Any

from ._http import CachedResponse, HttpClient

CKAN_PACKAGE_SEARCH = "https://data.gov.uk/api/3/action/package_search"


def package_search(
    client: HttpClient,
    query: str,
    rows: int = 10,
) -> tuple[list[dict[str, Any]], CachedResponse]:
    """Search the data.gov.uk CKAN catalogue. Returns the package list."""
    resp = client.get(CKAN_PACKAGE_SEARCH, params={"q": query, "rows": rows})
    if resp.status_code != 200:
        return [], resp
    body = resp.json()
    return list((body.get("result") or {}).get("results", []) or []), resp

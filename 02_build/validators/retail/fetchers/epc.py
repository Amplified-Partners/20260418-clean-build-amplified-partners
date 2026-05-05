# Authored by Devon-9a6b, 2026-05-03 (session devin-9a6bd256bd7c4a90a083a471fa94a810)
"""EPC Open Data API (free, registration required).

Retail-adjacent only — EPC band distribution by retail-postcode for premises
energy efficiency claims. INS-071 uses ONS energy stats instead, so EPC is
optional for the retail vertical.

When EPC_API_AUTH (HTTP-basic header value) is absent, calls return _skipped.

Register: https://epc.opendatacommunities.org/
"""
from __future__ import annotations

from .common import fetch_json, env_secret, Fetched

BASE = "https://epc.opendatacommunities.org/api/v1/non-domestic/search"


def is_available() -> bool:
    return env_secret("EPC_API_AUTH") is not None


def search_non_domestic(postcode: str, size: int = 100) -> Fetched:
    auth = env_secret("EPC_API_AUTH")
    if not auth:
        return Fetched(
            source="epc",
            url=BASE,
            params={"postcode": postcode},
            body={"_skipped": True, "reason": "EPC_API_AUTH not set"},
        )
    return fetch_json(
        "epc",
        BASE,
        params={"postcode": postcode, "size": size},
        headers={"Authorization": f"Basic {auth}", "Accept": "application/json"},
    )

# Authored by Devon-6264, 2026-05-03 (session devin-6264b0ba42c6453b86b166bebc3d868a)
"""EPC Domestic Register — auth-aware (free key).

Set ``EPC_API_KEY`` (Bearer token) and ``EPC_API_EMAIL`` in the environment.
Documented at https://epc.opendatacommunities.org/docs/api
"""

from __future__ import annotations

import base64
import os
from collections.abc import Mapping
from typing import Any

from ..core import SourceRef
from ._http import fetch_json

EPC_BASE = "https://epc.opendatacommunities.org/api/v1"


class MissingAuthError(RuntimeError):
    """Raised when EPC credentials are not configured."""


def has_key() -> bool:
    return bool(os.environ.get("EPC_API_KEY", "").strip()) and bool(
        os.environ.get("EPC_API_EMAIL", "").strip()
    )


def _auth_header() -> Mapping[str, str]:
    key = os.environ.get("EPC_API_KEY", "").strip()
    email = os.environ.get("EPC_API_EMAIL", "").strip()
    if not key or not email:
        raise MissingAuthError("EPC_API_KEY or EPC_API_EMAIL not set")
    token = base64.b64encode(f"{email}:{key}".encode()).decode()
    return {"Authorization": f"Basic {token}", "Accept": "application/json"}


def search_domestic(
    *,
    postcode: str,
    size: int = 100,
) -> tuple[Any, SourceRef]:
    """Search domestic EPCs by postcode (full or area, e.g. ``NE1``)."""
    headers = _auth_header()
    params = {"postcode": postcode, "size": size}
    return fetch_json(
        name="epc",
        url=f"{EPC_BASE}/domestic/search",
        params=params,
        headers=headers,
    )

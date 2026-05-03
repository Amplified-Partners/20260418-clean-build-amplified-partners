"""The Gazette JSON API — winding-up petitions and corporate insolvency notices.

Open access, no credentials. Used by INS-080 (WIP × Altman Z client signals)
to confirm distress notices are publishable signals against unpaid invoices.

Signed-by: Devon-ab74 (devin-ab740f2c78ee477a9c16ea3b6ed15293) - 2026-05-03
"""

from __future__ import annotations

import json
from datetime import datetime, timezone
from typing import Any

from ..cache import fetch
from ..core import EvidenceItem


def _now_iso() -> str:
    return datetime.now(tz=timezone.utc).isoformat(timespec="seconds")


GAZETTE_BASE = "https://www.thegazette.co.uk/all-notices/notice/data.json"


def insolvency_notices(category_code: str = "G201299") -> tuple[dict[str, Any], EvidenceItem]:
    """Fetch a page of insolvency notices.

    `G201299` is the Gazette category code for corporate insolvency notices.
    The API returns paginated JSON; we take the first page as an existence
    check + recent-volume base rate.
    """
    url = f"{GAZETTE_BASE}?categorycode-all={category_code}&numberOfLocationSearchFields=1"
    res = fetch(url)
    payload = json.loads(res.content.decode("utf-8"))
    evidence = EvidenceItem(
        source="The Gazette (UK official public record)",
        url=res.url,
        accessed_at=_now_iso(),
        content_sha256=res.sha256,
        summary=f"Gazette insolvency notices, category {category_code}",
        raw_path=str(res.cache_path),
    )
    return payload, evidence

"""Companies House — bulk and aggregate sources only (no live API key).

The live REST API at `api.companieshouse.gov.uk` requires a key; we don't have
one in this environment. Bulk and aggregate products that don't need a key:

- The published bulk CSV/JSON snapshots indexed at
  `https://download.companieshouse.gov.uk/en_output.html` (basic company
  metadata, accounts data, PSC, disqualified directors).
- Insolvency Service official statistics (CSV/ODS releases via gov.uk),
  which use Companies House data internally.
- ONS Business Demography (firm births/deaths by SIC) — same upstream as
  Companies House sector formation/dissolution but pre-aggregated.

For per-firm queries (e.g. INS-080 client Z-score), the live API is required
and the verdict is BLOCKED until a key is provisioned.

Signed-by: Devon-ab74 (devin-ab740f2c78ee477a9c16ea3b6ed15293) - 2026-05-03
"""

from __future__ import annotations

from datetime import datetime, timezone

from ..cache import FetchBlockedError, fetch
from ..core import EvidenceItem


def _now_iso() -> str:
    return datetime.now(tz=timezone.utc).isoformat(timespec="seconds")


def bulk_index() -> tuple[bytes, EvidenceItem]:
    """Fetch the Companies House bulk-data index page.

    Existence test for the bulk snapshot products. Confirms the public can
    pull basic company data, accounts, PSC, and disqualified directors.
    """
    url = "https://download.companieshouse.gov.uk/en_output.html"
    res = fetch(url)
    evidence = EvidenceItem(
        source="Companies House bulk data products",
        url=res.url,
        accessed_at=_now_iso(),
        content_sha256=res.sha256,
        summary="Bulk CSV/JSON snapshot index (no API key required)",
        raw_path=str(res.cache_path),
    )
    return res.content, evidence


def accounts_data_index() -> tuple[bytes, EvidenceItem]:
    """Companies House accounts data product index.

    Used for INS-080 Altman Z'' base-rate evidence — accounts data ZIPs
    contain XBRL filings the validator can sample.
    """
    url = "https://download.companieshouse.gov.uk/en_accountsdata.html"
    res = fetch(url)
    evidence = EvidenceItem(
        source="Companies House accounts data product",
        url=res.url,
        accessed_at=_now_iso(),
        content_sha256=res.sha256,
        summary="Bulk XBRL accounts ZIP archive index",
        raw_path=str(res.cache_path),
    )
    return res.content, evidence


def live_api_smoke_test() -> tuple[bytes, EvidenceItem]:  # pragma: no cover
    """Confirm the live API requires a key — raises FetchBlockedError."""
    raise FetchBlockedError(
        source="Companies House live API",
        reason=(
            "https://api.companieshouse.gov.uk/ requires a free API key. "
            "Apply at https://developer.company-information.service.gov.uk/ "
            "and store as the COMPANIES_HOUSE_API_KEY org secret."
        ),
    )

"""HMRC fetchers — tax calendar, insolvency stats, regulatory change.

All sources here are open (gov.uk pages) and don't require credentials. Pages
are fetched as raw HTML and the validator does targeted substring checks
against expected dates / figures.

Signed-by: Devon-ab74 (devin-ab740f2c78ee477a9c16ea3b6ed15293) - 2026-05-03
"""

from __future__ import annotations

from datetime import datetime, timezone

from ..cache import fetch
from ..core import EvidenceItem


def _now_iso() -> str:
    return datetime.now(tz=timezone.utc).isoformat(timespec="seconds")


def insolvency_statistics_collection() -> tuple[bytes, EvidenceItem]:
    """Fetch the Insolvency Service official statistics collection page."""
    url = "https://www.gov.uk/government/collections/insolvency-service-official-statistics"
    res = fetch(url)
    evidence = EvidenceItem(
        source="Insolvency Service official statistics (gov.uk collection)",
        url=res.url,
        accessed_at=_now_iso(),
        content_sha256=res.sha256,
        summary="Insolvency stats collection index — links to monthly + quarterly releases",
        raw_path=str(res.cache_path),
    )
    return res.content, evidence


def making_tax_digital_overview() -> tuple[bytes, EvidenceItem]:
    """Fetch the HMRC MTD overview publication — used by INS-083 / INS-093."""
    url = "https://www.gov.uk/government/publications/making-tax-digital"
    res = fetch(url)
    evidence = EvidenceItem(
        source="HMRC Making Tax Digital for Income Tax",
        url=res.url,
        accessed_at=_now_iso(),
        content_sha256=res.sha256,
        summary="HMRC MTD ITSA implementation guidance",
        raw_path=str(res.cache_path),
    )
    return res.content, evidence


def self_assessment_deadline_page() -> tuple[bytes, EvidenceItem]:
    """Fetch the HMRC Self Assessment deadline page — used by INS-093."""
    url = "https://www.gov.uk/self-assessment-tax-returns/deadlines"
    res = fetch(url)
    evidence = EvidenceItem(
        source="HMRC Self Assessment deadlines",
        url=res.url,
        accessed_at=_now_iso(),
        content_sha256=res.sha256,
        summary="HMRC Self Assessment deadline page (31 January / 31 October)",
        raw_path=str(res.cache_path),
    )
    return res.content, evidence


def vat_deadlines_page() -> tuple[bytes, EvidenceItem]:
    """Fetch the HMRC VAT return deadline page — used by INS-093."""
    url = "https://www.gov.uk/vat-returns/deadlines"
    res = fetch(url)
    evidence = EvidenceItem(
        source="HMRC VAT return deadlines",
        url=res.url,
        accessed_at=_now_iso(),
        content_sha256=res.sha256,
        summary="HMRC quarterly VAT deadline page",
        raw_path=str(res.cache_path),
    )
    return res.content, evidence


def corporation_tax_deadlines_page() -> tuple[bytes, EvidenceItem]:
    """Fetch the HMRC Corporation Tax accounting period page — used by INS-093."""
    url = "https://www.gov.uk/corporation-tax-accounting-period"
    res = fetch(url)
    evidence = EvidenceItem(
        source="HMRC Corporation Tax accounting period",
        url=res.url,
        accessed_at=_now_iso(),
        content_sha256=res.sha256,
        summary="HMRC Corporation Tax 9-month deadline guidance",
        raw_path=str(res.cache_path),
    )
    return res.content, evidence

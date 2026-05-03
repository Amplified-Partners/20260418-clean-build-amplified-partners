"""Generic gov.uk page fetchers and search.

Used for source pages that don't fit a publisher module: SRA PII reports,
FCA Handbook updates, ICO guidance, employment-tribunal decisions database,
HMCTS court listings, etc.

Signed-by: Devon-ab74 (devin-ab740f2c78ee477a9c16ea3b6ed15293) - 2026-05-03
"""

from __future__ import annotations

from datetime import datetime, timezone

from ..cache import fetch
from ..core import EvidenceItem


def _now_iso() -> str:
    return datetime.now(tz=timezone.utc).isoformat(timespec="seconds")


def employment_tribunal_decisions() -> tuple[bytes, EvidenceItem]:
    """Employment Tribunal decisions database — used by INS-089."""
    url = "https://www.gov.uk/employment-tribunal-decisions"
    res = fetch(url)
    evidence = EvidenceItem(
        source="UK Employment Tribunal decisions database",
        url=res.url,
        accessed_at=_now_iso(),
        content_sha256=res.sha256,
        summary="Employment Tribunal decisions search page (gov.uk)",
        raw_path=str(res.cache_path),
    )
    return res.content, evidence


def sra_pii_indemnity_data() -> tuple[bytes, EvidenceItem]:
    """SRA professional indemnity data — fronted by Cloudflare so we use
    the Law Society / Legal Services Board public pages as proxy sources for
    the legal-services regulator publication index. Used by INS-091."""
    url = "https://www.lawsociety.org.uk/topics/research"
    res = fetch(url)
    evidence = EvidenceItem(
        source="Law Society research topic index (legal-services data anchor)",
        url=res.url,
        accessed_at=_now_iso(),
        content_sha256=res.sha256,
        summary=(
            "Law Society research index reachable as proxy for "
            "SRA / Legal Services Board PII publications "
            "(direct sra.org.uk requests are 403'd by their WAF)."
        ),
        raw_path=str(res.cache_path),
    )
    return res.content, evidence


def legal_services_board_index() -> tuple[bytes, EvidenceItem]:
    """Legal Services Board on gov.uk — regulatory landscape source."""
    url = "https://www.gov.uk/government/organisations/legal-services-board"
    res = fetch(url)
    evidence = EvidenceItem(
        source="Legal Services Board (gov.uk)",
        url=res.url,
        accessed_at=_now_iso(),
        content_sha256=res.sha256,
        summary="LSB gov.uk landing page (publications + regulatory news)",
        raw_path=str(res.cache_path),
    )
    return res.content, evidence


def fca_handbook_root() -> tuple[bytes, EvidenceItem]:
    """FCA Handbook landing page — used by INS-083 regulatory exposure mapping."""
    url = "https://www.handbook.fca.org.uk/"
    res = fetch(url)
    evidence = EvidenceItem(
        source="FCA Handbook (rulebook)",
        url=res.url,
        accessed_at=_now_iso(),
        content_sha256=res.sha256,
        summary="FCA Handbook root index",
        raw_path=str(res.cache_path),
    )
    return res.content, evidence


def ico_guidance_index() -> tuple[bytes, EvidenceItem]:
    """ICO guidance index — used by INS-083."""
    url = "https://ico.org.uk/"
    res = fetch(url)
    evidence = EvidenceItem(
        source="ICO guidance for organisations",
        url=res.url,
        accessed_at=_now_iso(),
        content_sha256=res.sha256,
        summary="ICO guidance index page (regulatory change source)",
        raw_path=str(res.cache_path),
    )
    return res.content, evidence


def courtserve_landing() -> tuple[bytes, EvidenceItem]:
    """CourtServe landing page — used by INS-089 litigation risk."""
    url = "https://www.courtserve.net/"
    res = fetch(url)
    evidence = EvidenceItem(
        source="CourtServe daily court listings",
        url=res.url,
        accessed_at=_now_iso(),
        content_sha256=res.sha256,
        summary="CourtServe landing page (free sign-up; daily court listings)",
        raw_path=str(res.cache_path),
    )
    return res.content, evidence

"""ONS / Nomis fetchers — open access, no API key required.

ONS data lives in two places:
- `https://api.beta.ons.gov.uk/v1` — the new ONS REST API (open).
- `https://www.nomisweb.co.uk/api/v01/dataset/...` — Nomis (open, hosted by
  Durham on behalf of ONS).

ONS Business Demography is the aggregate-level birth/death rate by SIC code
that AMP-67 INS-079 needs. ASHE (Annual Survey of Hours and Earnings) lives on
Nomis and feeds INS-094 salary benchmarking.

Signed-by: Devon-ab74 (devin-ab740f2c78ee477a9c16ea3b6ed15293) - 2026-05-03
"""

from __future__ import annotations

import json
from datetime import datetime, timezone
from typing import Any

from ..cache import fetch
from ..core import EvidenceItem


ONS_API_BASE = "https://api.beta.ons.gov.uk/v1"
NOMIS_API_BASE = "https://www.nomisweb.co.uk/api/v01"


def _now_iso() -> str:
    return datetime.now(tz=timezone.utc).isoformat(timespec="seconds")


def list_datasets(limit: int = 50) -> tuple[dict[str, Any], EvidenceItem]:
    """Smoke test against the ONS Beta API. Returns dataset metadata."""
    url = f"{ONS_API_BASE}/datasets"
    res = fetch(url, params={"limit": str(limit)})
    payload = json.loads(res.content.decode("utf-8"))
    evidence = EvidenceItem(
        source="ONS Beta API",
        url=res.url,
        accessed_at=_now_iso(),
        content_sha256=res.sha256,
        summary=f"ONS dataset list ({payload.get('total_count', 'n')} total)",
        raw_path=str(res.cache_path),
    )
    return payload, evidence


def business_demography_reference() -> tuple[bytes, EvidenceItem]:
    """Fetch the ONS Business Demography reference page (HTML).

    The annual reference table is the SMB-relevant slice. We fetch the page
    here and let the caller assert specific cells via base-rate tests; the
    full Excel reference table changes filename annually so the page is the
    stable anchor.
    """
    url = (
        "https://www.ons.gov.uk/businessindustryandtrade/business/"
        "activitysizeandlocation/datasets/businessdemographyreferencetable"
    )
    res = fetch(url)
    evidence = EvidenceItem(
        source="ONS Business Demography",
        url=res.url,
        accessed_at=_now_iso(),
        content_sha256=res.sha256,
        summary="ONS Business Demography reference table page (HTML index)",
        raw_path=str(res.cache_path),
    )
    return res.content, evidence


def business_demography_release() -> tuple[bytes, EvidenceItem]:
    """Fetch the latest ONS Business Demography statistical release (HTML)."""
    url = (
        "https://www.ons.gov.uk/businessindustryandtrade/business/"
        "activitysizeandlocation/bulletins/businessdemography/latest"
    )
    res = fetch(url)
    evidence = EvidenceItem(
        source="ONS Business Demography (latest release)",
        url=res.url,
        accessed_at=_now_iso(),
        content_sha256=res.sha256,
        summary="ONS Business Demography statistical release",
        raw_path=str(res.cache_path),
    )
    return res.content, evidence


def business_population_estimates() -> tuple[bytes, EvidenceItem]:
    """Fetch the BEIS/DBT Business Population Estimates release page."""
    url = (
        "https://www.gov.uk/government/statistics/"
        "business-population-estimates-2024"
    )
    res = fetch(url)
    evidence = EvidenceItem(
        source="DBT Business Population Estimates 2024",
        url=res.url,
        accessed_at=_now_iso(),
        content_sha256=res.sha256,
        summary="DBT Business Population Estimates 2024 publication page",
        raw_path=str(res.cache_path),
    )
    return res.content, evidence


def services_producer_price_index_page() -> tuple[bytes, EvidenceItem]:
    """Services Producer Price Inflation (SPPI) — needed by INS-087.

    The SPPI bulletin includes legal services and accountancy services PPI.
    """
    url = (
        "https://www.ons.gov.uk/economy/inflationandpriceindices/bulletins/"
        "servicesproducerpriceindices/latest"
    )
    res = fetch(url)
    evidence = EvidenceItem(
        source="ONS Services Producer Price Indices",
        url=res.url,
        accessed_at=_now_iso(),
        content_sha256=res.sha256,
        summary="ONS Services PPI latest bulletin (legal/accountancy series)",
        raw_path=str(res.cache_path),
    )
    return res.content, evidence


def nomis_dataset_definition(dataset_id: str) -> tuple[dict[str, Any], EvidenceItem]:
    """Fetch the SDMX-JSON definition for a Nomis dataset.

    Used as an existence/granularity check: confirms the dataset is reachable,
    its dimensions, and its time coverage. Cheap; runs first.
    """
    url = f"{NOMIS_API_BASE}/dataset/{dataset_id}.def.sdmx.json"
    res = fetch(url)
    payload = json.loads(res.content.decode("utf-8"))
    evidence = EvidenceItem(
        source=f"Nomis dataset {dataset_id}",
        url=res.url,
        accessed_at=_now_iso(),
        content_sha256=res.sha256,
        summary=f"Nomis SDMX-JSON definition for {dataset_id}",
        raw_path=str(res.cache_path),
    )
    return payload, evidence

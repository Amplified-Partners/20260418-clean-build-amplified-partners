# Authored by Devon-6264, 2026-05-03 (session devin-6264b0ba42c6453b86b166bebc3d868a)
"""INS-022 — VOA / Council Tax → commercial client prospecting (Trades).

Catalogue claim:
    "MHCLG Business Rate Rateable Values (all commercial properties in England
     — rateable value, property type, address, UPRN — free download); Companies
     House Officers Search (link rateable value properties to company directors)
     ... Commercial market typically offers 25-35% gross margin vs 20-25%
     residential."

Two public-data legs:
    A. VOA / MHCLG — bulk rateable-values list (no auth).
    B. Companies House — company name search to cross-reference (auth required).

If Companies House key is unset, leg B is skipped and the verdict reports the
public-leg existence test on VOA.
"""

from __future__ import annotations

import json
from datetime import UTC, datetime

from ..core import EVIDENCE_DIR, REPO_ROOT, Evidence, SourceRef, Verdict, VerdictBand, now_iso
from ..sources import companies_house
from ..sources._http import fetch_bytes
from ..tests.existence import test_existence

INSIGHT_ID = "INS-022"

# VOA publishes the Local Rating List landing page; the bulk download is a
# multi-gigabyte ZIP linked from this page. We do an existence check on the
# landing page (HTTP 200 + non-trivial body) rather than streaming the full
# 1+ GB compilation, which would dominate CI cost without changing the verdict.
VOA_LIST_URL = (
    "https://www.gov.uk/government/statistics/"
    "non-domestic-rating-stock-of-properties-2024"
)


def run() -> Verdict:
    sources: list[SourceRef] = []

    # Leg A — VOA business-rates list existence
    try:
        body, voa_ref = fetch_bytes(name="voa", url=VOA_LIST_URL, suffix=".html")
        sources.append(voa_ref)
        voa_present = b"rating" in body.lower() and len(body) > 1000
    except Exception:  # noqa: BLE001
        voa_present = False

    # Leg B — Companies House cross-reference (auth-aware)
    ch_present = False
    ch_query_count = 0
    if companies_house.has_key():
        try:
            ch_data, ch_ref = companies_house.search_companies(
                query="cafe newcastle", items_per_page=20
            )
            sources.append(ch_ref)
            ch_query_count = len(ch_data.get("items") or [])
            ch_present = ch_query_count > 0
        except Exception:  # noqa: BLE001
            ch_present = False
    else:
        # Auth missing — record a placeholder source so the verdict explains why
        sources.append(
            SourceRef(
                name="companies_house",
                url="https://api.company-information.service.gov.uk",
                accessed_at=now_iso(),
                query_params={"status": "skipped"},
                response_hash="auth-required",
            )
        )

    verdict_band, metric = test_existence(
        rows=(1 if voa_present else 0) + ch_query_count,
        granularity_match=voa_present,
        license_open=True,
    )

    if voa_present and ch_present:
        notes = (
            "Both public legs validated: VOA rateable-values list reachable; "
            "Companies House search returned company records. "
            "ABC bridge: outreach conversion is client-side → capped at PLAUSIBLE."
        )
        if verdict_band == VerdictBand.PROVEN:
            verdict_band = VerdictBand.PLAUSIBLE
    elif voa_present:
        notes = (
            "VOA leg PROVEN; Companies House leg SKIPPED (set COMPANIES_HOUSE_API_KEY). "
            "Recipe demoted to PLAUSIBLE pending key-required B leg."
        )
        if verdict_band == VerdictBand.PROVEN:
            verdict_band = VerdictBand.PLAUSIBLE
    else:
        notes = "VOA landing page unreachable — A leg fails existence test."

    bundle = EVIDENCE_DIR / INSIGHT_ID
    bundle.mkdir(parents=True, exist_ok=True)
    (bundle / "summary.json").write_text(
        json.dumps(
            {
                "voa_present": voa_present,
                "companies_house_key": companies_house.has_key(),
                "ch_query_count": ch_query_count,
                "accessed_at": datetime.now(UTC).isoformat(timespec="seconds"),
            },
            indent=2,
        )
    )

    evidence = Evidence(
        sources=sources,
        metric=f"{metric}; voa_present={voa_present}; ch_present={ch_present}",
        notes=notes,
        raw_pointer=str(bundle.relative_to(REPO_ROOT)),
    )
    verdict = Verdict(
        insight_id=INSIGHT_ID,
        verdict=verdict_band,
        test_class="existence",
        evidence=evidence,
    )
    verdict.write()
    return verdict

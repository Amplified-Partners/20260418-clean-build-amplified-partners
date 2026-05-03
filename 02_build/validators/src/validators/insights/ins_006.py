# Authored by Devon-6264, 2026-05-03 (session devin-6264b0ba42c6453b86b166bebc3d868a)
"""INS-006 — Land Registry transactions → new-mover refurbishment lead.

Catalogue claim:
    "Properties sell and within 45-90 days, 60-70% undergo some plumbing,
     electrical, or heating work; Land Registry data is a 45-day leading
     indicator of residential refurbishment demand."

    "8-10 new customers/month × £350 average first job"

Public leg (testable here):
    Count residential transactions in served postcodes (NE1-NE3 = Newcastle
    central area used as the canonical Jesmond Plumbing trading area).

Test class: distribution.
    Sample = monthly sale counts per served postcode area.
    Threshold = 8 sales/month/postcode-area (lower bound of the claimed
    8-10 customers/month range, divided across 3 postcode areas this is a
    conservative ~3 sales/month/area lower bound).

ABC bridge: client side (job records → conversion rate) is not testable from
public data. Public leg validates → PLAUSIBLE band per ABC convention.
"""

from __future__ import annotations

import json
from datetime import UTC, datetime, timedelta
from pathlib import Path

import pandas as pd

from ..core import EVIDENCE_DIR, REPO_ROOT, Evidence, Verdict, VerdictBand
from ..sources.land_registry import (
    fetch_year,
    filter_by_date_range,
    filter_by_postcode_prefix,
)
from ..tests.distribution import test_distribution

INSIGHT_ID = "INS-006"
SERVED_POSTCODE_AREAS = ["NE1", "NE2", "NE3"]

# Catalogue claim: 8-10 new customers/month in served postcodes, with 60-70%
# refurbishment-conversion rate. Inverting: claim is supported if total
# residential sales (across served postcodes) >= 8 / 0.70 ~= 12 sales/month.
LOWER_BOUND_MONTHLY_SALES_TOTAL = 12.0


def run() -> Verdict:
    accessed_at = datetime.now(UTC)
    # 24-month window across at most three calendar-year files. Skip files that
    # 404 (current year may not exist yet very early in January).
    end = accessed_at.date().isoformat()
    start = (accessed_at.date() - timedelta(days=730)).isoformat()
    years = list(range(pd.Timestamp(start).year, pd.Timestamp(end).year + 1))

    frames: list[pd.DataFrame] = []
    refs = []
    for year in years:
        try:
            year_df, ref = fetch_year(year)
            frames.append(year_df)
            refs.append(ref)
        except Exception:  # noqa: BLE001 — yearly file may not yet be published
            continue
    # Pre-seed columns so downstream filtering doesn't KeyError on a fully
    # empty fetch (e.g. when every yearly file 404s due to network outage).
    df = (
        pd.concat(frames, ignore_index=True)
        if frames
        else pd.DataFrame(columns=["ppd_category_type", "postcode", "date_of_transfer"])
    )
    df = filter_by_date_range(df, start, end)
    ne_df = filter_by_postcode_prefix(df, SERVED_POSTCODE_AREAS)

    # Residential only; PPD category A excludes BTL/repossession edge cases
    residential = ne_df[ne_df["ppd_category_type"] == "A"].copy()
    residential["postcode_area"] = (
        residential["postcode"].fillna("").str.split().str[0].str.extract(r"^(NE\d+)").iloc[:, 0]
    )
    residential["month"] = residential["date_of_transfer"].astype(str).str[:7]

    # Total monthly sales across served postcode areas
    monthly_total = residential.groupby("month").size()
    samples: list[float] = [float(v) for v in monthly_total.values]

    # Per-area monthly counts (for evidence bundle)
    counts_by_area_month: dict[str, dict[str, int]] = {}
    for area in SERVED_POSTCODE_AREAS:
        area_df = residential[residential["postcode_area"] == area]
        counts_by_area_month[area] = area_df.groupby("month").size().to_dict()

    verdict_band, metric = test_distribution(
        samples=samples,
        claim_threshold=LOWER_BOUND_MONTHLY_SALES_TOTAL,
        direction=">=",
        minimum_n=12,
    )

    # ABC convention: public leg validating → PLAUSIBLE for the full recipe
    if verdict_band == VerdictBand.PROVEN:
        verdict_band = VerdictBand.PLAUSIBLE
        notes = (
            "Public leg (Land Registry sales count) PROVEN; full recipe demoted "
            "to PLAUSIBLE because client-side conversion rate (60-70% refurb propensity) "
            "is not testable from public data. Conversion-rate claim has FRAMEWORK "
            "LINEAGE support (CLV modelling, propensity-to-buy)."
        )
    elif verdict_band == VerdictBand.PLAUSIBLE:
        notes = "Public leg PLAUSIBLE; client-side ABC leg untested."
    else:
        notes = "Public leg disproves the claimed sale-density floor in served postcodes."

    metric_str = (
        f"{metric}; total_residential_sales={len(residential)}; "
        f"window={start}_to_{end}; postcode_areas={','.join(SERVED_POSTCODE_AREAS)}"
    )

    evidence = Evidence(
        sources=refs,
        metric=metric_str,
        notes=notes,
        raw_pointer=str(_write_evidence_bundle(counts_by_area_month, samples).relative_to(REPO_ROOT)),
    )
    verdict = Verdict(
        insight_id=INSIGHT_ID,
        verdict=verdict_band,
        test_class="distribution",
        evidence=evidence,
    )
    verdict.write()
    return verdict


def _write_evidence_bundle(
    counts: dict[str, dict[str, int]], samples: list[float]
) -> Path:
    bundle = EVIDENCE_DIR / INSIGHT_ID
    bundle.mkdir(parents=True, exist_ok=True)
    out = bundle / "monthly_sales_by_postcode_area.json"
    out.write_text(json.dumps({"counts": counts, "samples": samples}, indent=2, sort_keys=True))
    return bundle

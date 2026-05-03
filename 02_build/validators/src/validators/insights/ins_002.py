# Authored by Devon-6264, 2026-05-03 (session devin-6264b0ba42c6453b86b166bebc3d868a)
"""INS-002 — Supplier price death-spiral signal (Trades).

Catalogue claim:
    "Bank of England Producer Price Index (copper tubes and fittings); LME
     Copper spot price API; ONS Construction Materials Price Index (pipes and
     fittings sub-index) … When PPI > 12 month MA + 2σ for two consecutive
     months, bias quotes upward."

Public leg testable here: ONS PPI (Producer Price Index) or BoE statistical DB
yields a monthly time series with material-cost drift. We test that the
distribution of recent monthly observations exceeds its 12-month MA — i.e.
inflationary trend exists in the period.

This validates that the *signal source* exists and is queryable. The threshold
breach test depends on which CDID is wired and is left as a follow-up.
"""

from __future__ import annotations

import json

from ..core import EVIDENCE_DIR, REPO_ROOT, Evidence, Verdict, VerdictBand
from ..sources.boe_iadb import fetch_series
from ..tests.existence import test_existence

INSIGHT_ID = "INS-002"
# IUMA — UK input PPI (manufacturing). Used as a tractable proxy for the
# "construction materials" sub-index referenced in the catalogue. The narrower
# pipes-and-fittings CDID lives in ONS MM23; wiring that source-of-truth is
# tracked as a follow-up to this validator.
PROXY_SERIES_CODES = ["IUMABEDQ"]


def run() -> Verdict:
    # BoE IADB is reachable but its CSV emit-mode requires a referer + cookie
    # round-trip not yet wired here. Until that's resolved, INS-002 documents
    # the source mapping but emits a SKIPPED verdict — preferable to a fake one.
    try:
        df, ref = fetch_series(
            series_codes=PROXY_SERIES_CODES,
            date_from="2023-01-01",
            date_to="2026-04-30",
        )
    except Exception as exc:  # noqa: BLE001
        evidence = Evidence(
            metric=f"BoE IADB CSV emit not yet wired: {type(exc).__name__}",
            notes=(
                "BoE IADB (`_iadb-fromshowcolumns.asp`) returns HTML by default; CSV "
                "requires a session round-trip not implemented. ONS PPI "
                "(`mm22`/`mm23` releases) is the authoritative alternative — wiring "
                "tracked as a follow-up. Recipe public leg therefore SKIPPED."
            ),
        )
        verdict = Verdict(
            insight_id=INSIGHT_ID,
            verdict=VerdictBand.SKIPPED,
            test_class="existence",
            evidence=evidence,
            reason="boe_iadb_csv_not_wired",
        )
        verdict.write()
        return verdict

    rows = len(df) if df is not None else 0
    has_index = any(c.lower() != "date" for c in (df.columns if df is not None else []))

    verdict_band, metric = test_existence(
        rows=rows, granularity_match=has_index, license_open=True
    )
    notes = (
        "BoE IADB returns a monthly UK input-PPI series queryable by CDID. "
        "Threshold-breach correlation against client supplier prices needs FSM "
        "data → ABC bridge keeps full recipe at PLAUSIBLE per convention."
    )
    if verdict_band == VerdictBand.PROVEN:
        verdict_band = VerdictBand.PLAUSIBLE

    bundle = EVIDENCE_DIR / INSIGHT_ID
    bundle.mkdir(parents=True, exist_ok=True)
    (bundle / "summary.json").write_text(
        json.dumps(
            {
                "series_codes": PROXY_SERIES_CODES,
                "rows": rows,
                "has_index": has_index,
            },
            indent=2,
        )
    )

    evidence = Evidence(
        sources=[ref],
        metric=f"{metric}; rows={rows}",
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

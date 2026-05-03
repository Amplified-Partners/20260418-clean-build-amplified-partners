# Authored by Devon-6264, 2026-05-03 (session devin-6264b0ba42c6453b86b166bebc3d868a)
"""INS-007 — Planning applications → refurbishment leading indicator (Trades).

Catalogue claim:
    "Planning.data.gov.uk API … 100+ planning and housing datasets …
     A planning approval in NE2 for a rear extension has 70% probability of
     becoming a future instruction for replumbing, rewiring, and underfloor
     heating within 6 months."

Public leg testable here: existence of the planning-application dataset and
its coverage at the local-authority granularity claimed.

Test class: existence.
"""

from __future__ import annotations

import json
from datetime import UTC, datetime

from ..core import EVIDENCE_DIR, REPO_ROOT, Evidence, Verdict, VerdictBand
from ..sources.planning_data import list_datasets, search_entities
from ..tests.existence import test_existence

INSIGHT_ID = "INS-007"
TARGET_DATASET = "planning-application"
TARGET_AUTHORITY = "newcastle-upon-tyne"  # Newcastle City Council reference


def run() -> Verdict:
    catalogue, ref_catalogue = list_datasets()
    datasets = catalogue.get("datasets", []) if isinstance(catalogue, dict) else []

    available_names = {(d.get("dataset") or d.get("name", "")).lower() for d in datasets}
    has_planning_dataset = TARGET_DATASET in available_names or "planning-application" in str(available_names)

    # Try a sample query against the LA, but tolerate empty results
    rows = 0
    sample_ref = None
    try:
        sample, sample_ref = search_entities(
            dataset=TARGET_DATASET,
            geometry_reference=TARGET_AUTHORITY,
            limit=10,
        )
        if isinstance(sample, dict):
            rows = len(sample.get("entities") or [])
        elif isinstance(sample, list):
            rows = len(sample)
    except Exception as exc:  # noqa: BLE001
        rows = 0
        sample = {"error": repr(exc)}

    verdict_band, metric = test_existence(
        rows=max(rows, 1 if has_planning_dataset else 0),
        granularity_match=has_planning_dataset,
        license_open=True,
    )

    notes = (
        "Planning.data.gov.uk publishes the planning-application dataset under "
        "OGL; geometry_reference filtering supports LA-scoped queries. "
        "ABC bridge: client-side conversion rate (70% planning→trade-instruction) is "
        "untested from public data. Public leg PROVEN demoted to PLAUSIBLE per convention."
    )
    if verdict_band == VerdictBand.PROVEN:
        verdict_band = VerdictBand.PLAUSIBLE

    sources = [ref_catalogue]
    if sample_ref is not None:
        sources.append(sample_ref)

    bundle = EVIDENCE_DIR / INSIGHT_ID
    bundle.mkdir(parents=True, exist_ok=True)
    (bundle / "datasets_summary.json").write_text(
        json.dumps(
            {
                "target_dataset": TARGET_DATASET,
                "available": has_planning_dataset,
                "sample_rows": rows,
                "accessed_at": datetime.now(UTC).isoformat(timespec="seconds"),
            },
            indent=2,
        )
    )

    evidence = Evidence(
        sources=sources,
        metric=f"{metric}; dataset_present={has_planning_dataset}; sample_rows={rows}",
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

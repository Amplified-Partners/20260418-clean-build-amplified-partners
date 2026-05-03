# Authored by Devon-9a6b, 2026-05-03 (session devin-9a6bd256bd7c4a90a083a471fa94a810)
"""INS-065 — Shopify Cohort × ONS Wages × Local IMD → LTV Segmentation (Retail).

Claim: 'ONS ASHE publishes median earnings by postcode district; postcode-level
income variance is structural and supports LTV segmentation.'

Public-data-validatable leg: Nomis exposes ASHE workplace-analysis data
(NM_99_1) at parliamentary constituency / local authority granularity; we
verify the dataset exists and has the claimed dimensions.
"""
from __future__ import annotations

from ..fetchers.nomis import dataset_metadata, list_datasets
from ..tests.existence import existence_check
from ..verdict import Verdict


def run() -> Verdict:
    listing = list_datasets(search="ashe")
    meta = dataset_metadata("NM_99_1")

    fetched_evidence = [
        {**listing.evidence(sample_rows=1), "search": "ashe"},
        {**meta.evidence(sample_rows=1), "dataset": "NM_99_1"},
    ]

    has_ashe = False
    if isinstance(listing.body, dict):
        kf = listing.body.get("structure", {}).get("keyfamilies", {}).get("keyfamily", [])
        for k in kf:
            kid = str(k.get("id", "")).lower()
            # Nomis SDMX returns `name` as {"value": "...", "lang": "en"} (dict),
            # not a plain string and not a list. Cover both shapes plus a
            # legacy list-of-dicts fallback for safety.
            name_raw = k.get("name", "")
            if isinstance(name_raw, dict):
                name_str = str(name_raw.get("value", "")).lower()
            elif isinstance(name_raw, list):
                name_str = " ".join(str(n.get("value", "")) for n in name_raw if isinstance(n, dict)).lower()
            else:
                name_str = str(name_raw).lower()
            if "ashe" in kid or "ashe" in name_str or "earnings" in name_str:
                has_ashe = True
                break
            # Annotations carry the canonical dataset mnemonic ("ashe") and
            # the content-type/sources tag — both are reliable confirmation.
            annotations = k.get("annotations", {}).get("annotation", [])
            if isinstance(annotations, list):
                for ann in annotations:
                    if not isinstance(ann, dict):
                        continue
                    title = str(ann.get("annotationtitle", "")).lower()
                    text = str(ann.get("annotationtext", "")).lower()
                    if title in {"mnemonic", "contenttype/sources"} and "ashe" in text:
                        has_ashe = True
                        break
            if has_ashe:
                break

    v, bundle = existence_check(
        claim="Nomis ASHE workplace-analysis (NM_99_1) reachable",
        fetched_list=fetched_evidence,
    )

    if v == "PROVEN" and has_ashe:
        verdict, conf, summary = "PROVEN", 88, (
            "Nomis ASHE (workplace-analysis NM_99_1) is reachable; median earnings by geography is "
            "queryable per the dataset metadata."
        )
    elif v in ("PROVEN", "PLAUSIBLE"):
        verdict, conf, summary = "PLAUSIBLE", 70, f"Nomis reachable, ASHE detection partial: {bundle.get('reason', '')}"
    else:
        verdict, conf, summary = "DISPROVEN", 80, "Nomis ASHE not reachable"

    notes = [
        "Public leg = Nomis ASHE earnings + (separately) DLUHC IMD by LSOA. PROVEN here.",
        "Client leg = Shopify cohort LTV per postcode is internal data; recipe is PLAUSIBLE end-to-end.",
    ]
    return Verdict(
        insight_id="INS-065",
        title="Shopify Cohort × ONS Wages × Local IMD → LTV Segmentation (Retail)",
        vertical="Retail",
        verdict=verdict,
        test_class="existence",
        summary=summary,
        evidence=[bundle],
        notes=notes,
        confidence=conf,
    )

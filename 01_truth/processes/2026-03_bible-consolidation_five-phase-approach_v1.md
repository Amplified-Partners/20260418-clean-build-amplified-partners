---
title: Business Bible consolidation — five-phase approach (truth candidate)
date: 2026-04-16
version: 1
status: draft
---

Status: [LOGIC TO BE CONFIRMED]
Source: `90_archive/2026-03_amplified-consolidated-architecture_full.txt`

## Claim (candidate)

Consolidation should be run as a repeatable pipeline with a clear target tree defined **before** moving files, and a strict separation between raw archives and curated canon.

## Five-phase approach (candidate)

1. **Company-level sweep**
   - inventory *all* sources (vault, exports, downloads, sessions)
   - produce a master inventory

2. **Department architecture design**
   - define the target departmental tree first (functions, ownership, cadence)
   - avoid tool/date-based organisation

3. **Data placement**
   - move/copy/symlink into the target tree
   - duplicates become visible

4. **Department-level refinement**
   - dedupe + curate inside each department
   - flag gaps, archive superseded, consolidate overlaps

5. **Bible compilation**
   - compile a human-readable, navigable Bible from the curated structure
   - include index + cross-links + changelog

## Clean room mapping (proposed)

- Phase 1 inputs land in: `90_archive/` as `[NON-AUTHORITATIVE]` and/or `[NARRATIVE]`.
- Phase 2–5 outputs land in: `01_truth/` and are listed in `00_authority/MANIFEST.md` as candidate → authoritative.

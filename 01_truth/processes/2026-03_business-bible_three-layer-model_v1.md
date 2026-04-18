---
title: Business Bible — three-layer model (truth candidate)
date: 2026-04-16
version: 1
status: draft
---

Status: `[LOGIC TO BE CONFIRMED]`
Source: `90_archive/2026-03_amplified-consolidated-architecture_full.txt`

## Claim

The “Business Bible” is an **output layer** (curated, deduped, navigable reference), not a single document. It sits above an archive layer and an extraction layer.

## Model (3 layers)

1. **Raw file layer (episodic store)**
   - Purpose: non-lossy archive of originals.
   - In this clean room: `90_archive/` (reference-only; immutable posture).

2. **Content source layer (semantic extraction)**
   - Purpose: extracted entities/relationships + retrieval indexes.
   - In this clean room: candidate artifacts belong in `01_truth/` (schemas/interfaces/processes), indexed in `00_authority/MANIFEST.md`.
   - Tooling details: `[LOGIC TO BE CONFIRMED]`.

3. **Reference layer (“Bible”)**
   - Purpose: curated, deduplicated, navigable view with provenance links.
   - In this clean room: only create this layer when it is required by a concrete downstream workflow. Otherwise keep extracted truth small and truth-shaped.

## Defaults (until confirmed)

- Treat `90_archive/` as the raw layer for this repo.
- Do not choose graph/vector tooling inside this doc.
- Scope of “Bible” output is `[DECISION REQUIRED]` if it affects client/privacy boundaries.

## Failure modes

- Producing a large “Bible” narrative without leaf-level need (reintroduces bloat).
- Treating archive material as truth by proximity (violates manifest discipline).

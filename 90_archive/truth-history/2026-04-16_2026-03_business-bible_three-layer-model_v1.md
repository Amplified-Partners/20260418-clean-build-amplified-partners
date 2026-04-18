---
title: Business Bible — three-layer model (truth candidate)
date: 2026-04-16
version: 1
status: draft
---

Status: [LOGIC TO BE CONFIRMED]
Source: `90_archive/2026-03_amplified-consolidated-architecture_full.txt`

## Claim (candidate)

The “Business Bible” is best treated as an **architectural layer**, not a single document: a curated, deduplicated, navigable human reference view that sits **on top of** raw vault material and extracted semantic/graph layers.

## Proposed three-layer structure

1. **Raw file layer (episodic store)**
   - Purpose: non-lossy archive of originals (transcripts, sessions, research, downloads)
   - Access: agents retrieve via search tooling (graph + vector)

2. **Content source layer (semantic extraction)**
   - Purpose: extracted entities/relationships + embeddings for retrieval and linking
   - Access: semantic + graph search; confidence scoring `[LOGIC TO BE CONFIRMED]`

3. **Human reference layer (“Bible”)**
   - Purpose: curated, deduplicated, navigable structure by department/function
   - Access: humans and agents use as “what we currently believe is true”, with provenance links

## Open questions (must be confirmed)

- How “raw layer” maps to clean room `90_archive/` vs broader workspace archives.
- What the extraction layer is in this project (graph DB choice, vector DB choice) `[LOGIC TO BE CONFIRMED]`.
- What “Bible” scope is (company only vs client-specific) `[LOGIC TO BE CONFIRMED]`.

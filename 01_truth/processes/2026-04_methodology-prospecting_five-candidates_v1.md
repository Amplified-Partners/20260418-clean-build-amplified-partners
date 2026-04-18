---
title: Methodology prospecting (five candidates → scored shortlist)
date: 2026-04-16
version: 1
status: draft
---

Status: `[LOGIC TO BE CONFIRMED]`
Purpose: Find “best in the world for A→B” methods, score them reproducibly against this environment, then surface candidates and synthesis opportunities.

## Inputs

- Target: **A→B** statement (one sentence).
- Constraints (hard): privacy, safety, time window, budget window.
- Context: what is already authoritative here (manifest-listed).

## Steps

1. **Define remit**
   - Write a remit using `00_authority/BUILD_LOOP.md` → Research remit template (start/end/non-goals/inputs/outputs/stop rule/remit id).

2. **Collect five candidates**
   - Gather five distinct methodologies that plausibly move A→B.
   - Each candidate must include: provenance, longevity signal, and enough detail to run (or mark `[SOURCE REQUIRED]`).

3. **Normalize each candidate to the same shape**
   - Inputs, steps, outputs, failure modes, required tooling, evidence level.
   - Strip vendor cheerleading; keep claims + proof pointers.

4. **Score candidates**
   - Use `01_truth/processes/2026-04_methodology-scoring-rubric_v1.md`.
   - Require a short justification per score dimension with a source pointer or token.

5. **Cross-link via taxonomy**
   - Apply `PUDDING_TAXONOMY_v1` labels if available; otherwise mark `[SOURCE REQUIRED]`.
   - Identify candidates that share underlying mechanism despite surface differences.

6. **Synthesis pass (optional; bounded)**
   - Combine only if the combined method is runnable and reduces friction vs the best single method.
   - Re-score the synthesized method using the same rubric.

7. **Output**
   - Produce a ranked shortlist (top 1–2) + a “next evidence to de-risk” list.
   - If a choice is required: mark `[DECISION REQUIRED]` with the minimum decision needed.

## Outputs

- Five candidate cards (normalized).
- One scored table + ranked shortlist.
- Optional synthesized candidate (re-scored).
- `[DECISION REQUIRED]` items (if any) with sources.

## Failure modes

- Candidates are not comparable (missing normalization).
- Scores are not reproducible (no anchors/justifications).
- “Novelty bias” (choosing new ideas over validated practice).
- Synthesis bloat (combining methods without proof of benefit).

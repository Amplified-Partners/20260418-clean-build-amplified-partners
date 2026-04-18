---
title: Research operations cadence (heavy start → steady refresh)
date: 2026-04-16
version: 1
status: draft
---

Status: `[LOGIC TO BE CONFIRMED]`

## Cadence model

### Phase A — Heavy research (bootstrap)

Trigger: early build / large unknown surface / many A→B transitions.

Rules:

- Prefer **many small remits** over one mega remit (`00_authority/BUILD_LOOP.md`).
- Default output is **bounded extractions** (1–2 pages) + archive provenance.
- Every remit ends with: ranked shortlist + `next_evidence` list.

Stop rule: `[LOGIC TO BE CONFIRMED]` until tooling/budgets are fixed; still stop per remit timebox.

### Phase B — Steady refresh (post-testing Kaizen)

Trigger: tests reveal drift, new external standards, or scheduled refresh.

Rules:

- Research is triggered by **test failures**, **manifest contradictions**, or **scheduled review** (exact schedule `[LOGIC TO BE CONFIRMED]`).
- Refresh must produce either:
  - an updated methodology extraction, or
  - a decision token explaining why no change is warranted.

### Phase C — Symbiotic synthesis (optional; gated)

Trigger: two+ methods score well on different dimensions and taxonomy links suggest a merge.

Rules:

- Synthesis requires a **hypothesis + minimal experiment plan** before promotion.
- Re-score using the same rubric after synthesis.

## Outputs (minimum)

- Remit IDs + archive sources
- Updated candidate artifacts in `01_truth/`
- Manifest updates only when promotion criteria are met

## Failure modes

- Continuous research without shipping runnable artifacts.
- “Always updating” without a failing signal (thrash).
- Symbiotic merges without re-score + test plan.

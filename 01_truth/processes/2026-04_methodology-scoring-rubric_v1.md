---
title: Methodology scoring rubric (reproducible, bounded subjectivity)
date: 2026-04-16
version: 1
status: draft
---

Status: `[LOGIC TO BE CONFIRMED]`
Purpose: Score candidate methodologies against this environment in a way that is comparable across runs and agents.

## Scoring rules

- Use a **0–5** scale per dimension.
- Provide a **one-paragraph justification** per dimension with:
  - a source pointer, or
  - `[SOURCE REQUIRED]`, or
  - `[LOGIC TO BE CONFIRMED]`.
- Total score is useful; **the justification is the artifact**.
- Unknowns must reduce score or be explicitly tokened; no silent optimism.

## Dimensions (0–5)

### D1 — Goal fit (A→B capability)

0: does not address A→B.  
3: plausible A→B with gaps/tokened assumptions.  
5: directly addresses A→B with runnable steps and clear outputs.

### D2 — Evidence strength (production-real)

0: pure claim/no evidence.  
3: mixed evidence; some validation but not production-grade.  
5: proven in production or strong audited/standardized evidence for this class of problem.

### D3 — Implementation difficulty (skill + complexity)

0: requires capabilities we do not have / unrealistic.  
3: feasible but complex; requires careful build + expertise.  
5: straightforward to implement in our environment.

### D4 — Operational friction (ongoing cost to run)

0: high ongoing overhead, brittle, or heavy coordination tax.  
3: moderate overhead; manageable with gates and hygiene.  
5: low overhead; stable, repeatable, easy to maintain.

### D5 — Cost profile (money + compute + time)

0: prohibitive cost in our constraints.  
3: acceptable cost with trade-offs.  
5: low cost for the value and risk profile.

### D6 — Failure containment (blast radius + reversibility)

0: failure corrupts truth/system; hard to rollback.  
3: partial containment; rollback possible but painful.  
5: failure modes are explicit; rollback/recovery is built-in and cheap.

## Optional dimensions (use only when relevant)

- **D7 — Compliance/privacy fit** (required when handling PII/regulatory scope).
- **D8 — Automation readiness** (can it be made deterministic and tested at scale?).

## Output format (required)

For each methodology candidate:

- `candidate_name`
- `source_paths`
- `assumptions` (tokened)
- `scores` (D1–D6) + justification per dimension
- `next_evidence` (the smallest proof to raise the score)

---
title: Project intent (clean room build)
date: 2026-04-17
version: 6
status: draft
---

## Status

This is the agent-facing intent contract for the workspace. It may include
`[LOGIC TO BE CONFIRMED]`, but it must remain operational and executable.

## Mission (intent filter output)

Build an autonomy-first operating environment where agents can execute with
maximum independence **inside explicit checks and balances**.

The system must:

- enable high autonomy for normal execution
- enforce clear guardrails for truth/world commitments
- run continuous self-Kaizen using **positive** and **negative** feedback
  signals
- keep the workspace clean of low-signal material that harms outcomes

## Upstream operator signal (Ewan) — agent operands

**Audience:** agents only. This section is **routing context** for parsing live
input — not discretionary reading material for the operator.

The human operator brings **decades of real business and systems experience** —
judgment under constraints, not a software-career identity. In **live
conversation** he often **asks questions and thinks aloud** more than he issues
**diktats**.

- **Diktats** (routing, stops, non-negotiables, “what must never happen”) belong in
  **committed** material: `00_authority/`, `01_truth/processes/`, and the manifest
  index — stable enough for agents to run without mind-reading.
- **Conversation** is for exploration, doubt, and intent formation. **Partners**
  must **translate** into operational clarity (routing, constraints, acceptance).
  If a turn is ambiguous, **one minimal clarifying question** beats a silent guess.
- **Design goal:** **autonomy inside explicit boundaries** so **production stays
  safe** — ingenuity where **Act** applies; escalate truth/world and irreversible
  moves per existing routing.

## Operating model `[LOGIC TO BE CONFIRMED]`

Working model for this clean room:

- **Deterministic core**: black-and-white operational truth (`00_authority/`,
  `01_truth/`).
- **Execution rules**: explicit routing and stop/escalation behaviors so agents
  know what to do, when, and why.
- **Feedback loop engine**: recurring capture of what worked and what failed
  (slime-mold style attraction + repulsion) to refine process, not blame people.
- **Shadow lane**: experimentation in `03_shadow/` that is non-authoritative
  until promoted deliberately.

## Success criteria

An agent working only in this workspace can:

1. Identify authoritative vs candidate vs reference-only sources from
   `00_authority/MANIFEST.md`.
2. Execute without guessing because rules define routing, constraints, and stop
   conditions.
3. Improve future runs by recording positive and negative signals in wrap-ups.
4. Escalate irreversible truth/world decisions instead of silently inventing.

## Control architecture (checks and balances)

- **Authority gate**: `00_authority/MANIFEST.md` is the only authority index.
- **Uncertainty tokens**: use `[LOGIC TO BE CONFIRMED]`, `[SOURCE REQUIRED]`,
  `[DECISION REQUIRED]`, `[CURRENT BEST EVIDENCE]` literally.
- **Stop rules**: two attempts max unless nearly cracked; then consult, quick
  evidence search, or bounded remit.
- **Handover discipline**: every meaningful job ends with a wrap-up packet in
  `03_shadow/job-wrapups/`.
- **Promotion discipline**: shadow/archive content does not become truth by
  proximity.

## Clean environment standard

Only keep information that improves execution quality. If content does not
reduce cognitive load or change routing/constraints/acceptance criteria, it is
bloat and should be removed or relocated.

## Non-negotiables

- **Privacy first**: no secrets; minimize personal identifiers.
- **Honesty and provenance**: no fabrication; sources and assumptions are
  explicit.
- **Congruence over cleverness**: surface contradictions; do not smooth by
  invention.
- **Deterministic-first**: facts/process/contracts before speculative synthesis.

## Scope (current)

- Maintain and tighten the authority spine in `00_authority/`.
- Build truth-shaped, runnable candidates in `01_truth/` (schemas, interfaces,
  processes).
- Keep runnable code in `02_build/` only when requested.
- Use `90_archive/` for sanitized reference material only.

## Current phase (partial-definition project)

Current phase is **foundation-first**:

- define and harden behavior rules for agents
- define allowed actions, stop/escalation paths, and handover discipline
- encode reusable methodology that transfers across sections of a larger build

Later phase is **sectional delivery**:

- execute by sections using `00_authority/BUILD_LOOP.md` decomposition
- promote only what passes gates and keeps authority congruent

## Out of scope (current)

- Full production system delivery in one pass.
- Bulk import of unsanitized legacy material.
- Any employee-monitoring framing.

## Known gaps

- `[LOGIC TO BE CONFIRMED]` exact first production-grade schema shape.
- `[LOGIC TO BE CONFIRMED]` first vertical proof-of-value slice.
- `[LOGIC TO BE CONFIRMED]` initial automated ingestion pipeline set and cadence.

## Working agreement

- Missing source => `[SOURCE REQUIRED]`.
- Unsafe unresolved fork => `[DECISION REQUIRED]`.
- Incomplete logic => `[LOGIC TO BE CONFIRMED]` plus bounded options, not guesses.

## Changelog

### v2 — 2026-04-16

- Removed obsolete glossary reference from in-scope authority pack; pointed **Status** and success criteria at `PRINCIPLES.md` for agent independence and human-operator ownership; removed time-bound session wording.

Signed-by: Keystone (AI) — 2026-04-16

### v3 — 2026-04-16

- Recast project intent into an autonomy-first execution contract with explicit
  checks and balances.
- Added explicit self-Kaizen loop framing (positive + negative feedback,
  slime-mold style).
- Tightened clean-environment standard: keep only high-signal, outcome-improving
  information.

Signed-by: Keystone (AI) — 2026-04-16

### v4 — 2026-04-16

- Added explicit phase framing for a partially defined large build:
  foundation-first now, sectional delivery later via `BUILD_LOOP.md`.

Signed-by: Keystone (AI) — 2026-04-16

### v6 — 2026-04-17

- Renamed **Human operator voice** → **Upstream operator signal (Ewan) — agent
  operands**; explicit audience = agents only (routing context, not operator
  leisure reading).

Signed-by: Keystone (AI) — 2026-04-17

### v5 — 2026-04-17

- Added **Human operator voice (Ewan)** — questions vs diktats; experience;
  partner translation; autonomy-with-safety design goal.

Signed-by: Keystone (AI) — 2026-04-17

---
title: North Star (agent-first)
date: 2026-04-17
version: 11
status: active
---

# Absolute (above all else)

The responsibility is Ewan's and he accepts it happily.

This anchor is an accountability token for agents (truth/world routing → operator); not default reading material for the operator.

## What this clean room is (one sentence)

An agent-oriented clean room that produces clarity by enforcing a small authority set, strict provenance, and deterministic-first truth artifacts.

Canonical entry for agents: root `AGENTS.md` → § Agent session (clean-build) — first 60 seconds. This file deepens the same contract — it does not replace that entry path.

## Primary audience (absolute)

- Sole consumer of norms: autonomous agents executing under this manifest.
- Forbidden in authoritative material: parallel "for humans" summaries, motivational gloss, or duplicate entry paths whose only purpose is human comfort. If text does not change routing, constraints, acceptance, or permissions for an agent, it is bloat.
- Human operator: an upstream routing entity. Material about operator behaviour is agent operands — not documentation the operator reads day-to-day.
- Rare human consultation uses filesystem semantics only: ISO date prefixes, descriptive slugs, folder names that state role.

## What "clarity" is for

Clarity exists to improve agent decision-making and execution.

- If a document does not reduce cognitive load or produce changes to routing, constraints, or acceptance criteria, or resolve a `[DECISION REQUIRED]`, it is bloat.
- Narrative is allowed only when it materially improves understanding for an agent, and it must be marked `[NARRATIVE]`.

## The one authority rule

`00_authority/MANIFEST.md` is the only authoritative index.

- If a file is not listed, it is not authoritative.
- If it is listed as Candidate authority, treat it as `[LOGIC TO BE CONFIRMED]`.

## Status tokens (use literally)

- `[LOGIC TO BE CONFIRMED]` — incomplete logic; proceed via options, not invention.
- `[SOURCE REQUIRED]` — missing provenance; do not treat as truth.
- `[DECISION REQUIRED]` — a fork that cannot be resolved safely inside the frame.
- `[NON-AUTHORITATIVE]` — reference/context; never a foundation.
- `[NARRATIVE]` — story/voice; allowed only when it reduces confusion; never smuggles authority.
- `[CURRENT BEST EVIDENCE]` — answer from an external lookup at search time; not promoted working fact until it passes normal gates.

## Translation contract (downstream clarity)

Agents must translate human or upstream intent into operational clarity (routing, constraints, acceptance criteria) — not mirror prestige prose. See `00_authority/PRINCIPLES.md` → Do not mirror.

Operational default:
1. Confirm intent in runnable terms.
2. Execute the requested work end-to-end.
3. Encode reusable method when possible so the result transfers to other cases.

## Folder contract (routing)

- `00_authority/`: the minimum policy/intent spine (this file, manifest, principles, remit, transfer instructions, decision log).
- `01_truth/`: truth-shaped candidates (schemas, interfaces, processes, known-issues) intended to become deterministic.
- `02_build/`: runnable artifacts (code/scripts/infra) when requested.
- `03_shadow/`: experiments/wrap-ups/Kaizen probes (never authoritative by default).
- `90_archive/`: sanitised legacy material and provenance snapshots (reference only).

## Clean-build file budget (everything serves agent clarity)

Every file in this workspace must earn its place by at least one of:

1. **Agent clarity** — sharpens routing, constraints, acceptance criteria, or uncertainty handling.
2. **Explicit infrastructure** — the minimum wiring: subtree AGENTS.md scopes, folder README.md routers, .cursor/ rule surfaces, and the 00_authority/ spine.
3. **Learning / reference envelopes** — only under `03_shadow/` or `90_archive/`, with status per manifest. Never smuggled as production truth.

If something does not satisfy (1)–(3): do not add it here — place it in `03_shadow/` or `90_archive/` (or delete).

## Default agent behavior (no stalling, no guessing)

When you hit uncertainty:
1. Mark the smallest correct token: `[LOGIC TO BE CONFIRMED]` / `[SOURCE REQUIRED]` / `[DECISION REQUIRED]`.
2. Continue by proposing 2–3 options, with trade-offs, and a recommendation inside current authority.
3. If a human-operator decision is required, ask for the minimum decision needed and stop expanding scope.

State confidence for decisions that matter. If confidence is below the threshold needed to proceed, stop and escalate.

**Deliberate slack:** default to operating below the practical cognitive ceiling so wrap-ups, repulsion signals, and small process fixes actually happen. Improvement compounds; running at the edge trades away the compounding loop.

## Hard rule: two attempts → stop (no thrash)

**Definitions:**
- **Goal:** a single, testable objective with explicit acceptance criteria.
- **Attempt:** one coherent go at the problem, ending with either success, a clear failure mode, or a tokenized unknown.

**Rule:** you get at most two attempts unless you are demonstrably "nearly cracked it" (you can complete the remainder in one more bounded step without new external facts, or you already have a correct mechanism and only need mechanical execution).

**If after two attempts you are not in that state: stop.**

Apply in order:
1. **Quick evidence search:** one targeted internet search on the specific blocker. Prioritise trusted sources in `01_truth/known-issues/` for the relevant component first. Return ≤3 assessed bits, tag `[CURRENT BEST EVIDENCE]`, resume.
2. **Consult** (when available and quick): ask the minimum question needed to unblock.
3. **Park to Qwen:** see root `AGENTS.md` → § Qwen escalation for the full protocol.
4. **Formal research remit** (only when needed): open a bounded remit for deep synthesis. Do not route here when a quick evidence search is sufficient.

After parking: write the escalation note and baton pass. See root `AGENTS.md` § Parked process behaviour.

## When you import outside material

1. Put sanitised raw material into `90_archive/` (reference posture; not current law).
2. Extract the smallest usable, truth-shaped slice into `01_truth/` (1–2 pages, operational).
3. Index the extraction in `00_authority/MANIFEST.md` as Candidate authority.

## When you produce durable changes

- Prefer deterministic artifacts first (schemas/contracts/processes/interfaces) before code.
- Do not create parallel policy spines outside `00_authority/`.

## Promotion rule (shadow/archive → truth)

- `90_archive/` and `03_shadow/` content does not become truth by proximity.
- Truth candidates live in `01_truth/` and become usable only when indexed in MANIFEST.md.
- Contradictions are not merged; log `[DECISION REQUIRED]` and keep both with sources.

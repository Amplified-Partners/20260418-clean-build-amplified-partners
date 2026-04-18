---
title: North Star (agent-first)
date: 2026-04-17
version: 11
status: draft
---

<!-- markdownlint-disable-file MD013 -->

## Absolute (above all else)

**The responsibility is Ewan’s and he accepts it happily.**

This anchor is an **accountability token** for agents (truth/world routing →
operator); not default reading material for the operator.

## What this clean room is (one sentence)

An **agent-oriented clean room** that produces **clarity** by enforcing a small authority set, strict provenance, and deterministic-first truth artifacts.

**Canonical entry for agents:** root **`AGENTS.md`** → **§ Agent session (clean-build) — first 60 seconds** (read order, autonomy bounds, mistakes-as-signal). This file deepens the same contract — it does not replace that entry path.

## Primary audience (absolute)

- **Sole consumer of norms:** autonomous agents executing under this manifest.
- **Forbidden in authoritative material:** parallel “for humans” summaries,
  motivational gloss, or duplicate entry paths whose only purpose is human comfort.
  If text does not change **routing**, **constraints**, **acceptance**, **tokens**,
  or **permissions** for an agent, it is bloat.
- **Human operator:** an **upstream** routing entity (`AGENTS.md` truth/world
  boundary). Material about operator behaviour is **agent operands** (how to
  interpret speech and escalate) — not documentation the operator is expected to
  read for day-to-day work.
- **Rare human consultation** (e.g. audit, policy change) uses **filesystem
  semantics only:** ISO date prefixes (`YYYY-MM-DD`), descriptive slugs, folder
  names that state role (`00_authority/`, `01_truth/`, …). No second doc layer is
  required for findability.

## What “clarity” is for

Clarity exists to improve **agent decision-making and execution**.

- If a document does not reduce cognitive load or produce **changes** to **routing**, **constraints**, or **acceptance criteria**, or resolve a `[DECISION REQUIRED]`, it is bloat.
- Narrative is allowed only when it **materially improves understanding** for an agent, and it must be marked `[NARRATIVE]`.

## The one authority rule

`00_authority/MANIFEST.md` is the **only authoritative index**.

- If a file is **not listed**, it is **not authoritative**.
- If it is listed as **Candidate authority**, treat it as `[LOGIC TO BE CONFIRMED]`.

## Status tokens (use literally)

- `[LOGIC TO BE CONFIRMED]` — incomplete logic; proceed via options, not invention.
- `[SOURCE REQUIRED]` — missing provenance; do not treat as truth.
- `[DECISION REQUIRED]` — a fork that cannot be resolved safely inside the frame.
- `[NON-AUTHORITATIVE]` — reference/context; never a foundation.
- `[NARRATIVE]` — story/voice; allowed only when it reduces confusion; never smuggles authority.
- `[CURRENT BEST EVIDENCE]` — answer from an external lookup **at search
  time**; **not** promoted working fact until it passes normal gates
  (`PROMOTION_GATE.md`, manifest, BUILD_LOOP evidence discipline).

## Translation contract (downstream clarity)

Agents must **translate** human or upstream intent into **operational
clarity** (routing, constraints, acceptance criteria)—not mirror prestige
prose. See `00_authority/PRINCIPLES.md` → **Do not mirror**.

Operational default:

1. Confirm intent in runnable terms.
2. Execute the requested work end-to-end.
3. Encode reusable method when possible so the result transfers to other cases.

## Folder contract (routing)

- `00_authority/`: the **minimum** policy/intent spine (this file, manifest, principles, remit, transfer instructions, decision log).
- `01_truth/`: **truth-shaped candidates** (schemas, interfaces, processes) intended to become deterministic.
- `02_build/`: runnable artifacts (code/scripts/infra) when requested.
- `03_shadow/`: experiments/curveballs/Kaizen probes (never authoritative by default).
- `90_archive/`: sanitised legacy material and provenance snapshots (reference only).

## Clean-build file budget (everything serves agent clarity)

Every file in this workspace must **earn its place** by at least one of:

1. **Agent clarity** — sharpens **routing**, **constraints**, **acceptance criteria**,
   or **uncertainty handling** for work with Ewan in this clean build (not prestige
   prose).
2. **Explicit infrastructure** — the minimum wiring so (1) stays true: subtree
   `AGENTS.md` scopes, folder `README.md` routers, `.cursor/` rule surfaces (hooks
   only per `.cursor/HOOKS_TESTING_NEED.md`), and the `00_authority/` spine.
3. **Learning / reference envelopes** — only under `03_shadow/` or `90_archive/`,
   with status per `00_authority/MANIFEST.md` (`[NON-AUTHORITATIVE]` / candidate);
   never smuggled as production truth.

If something does not satisfy **(1)–(3)**: **do not add it here** — place it in
`03_shadow/` or `90_archive/` (or delete). **Bulk imports** under
`90_archive/inbox/` are dumps pending triage — agents do **not** read them
end-to-end unless a task explicitly routes there; see `90_archive/README.md`.

## Default agent behavior (no stalling, no guessing)

When you hit uncertainty:

1. Mark the smallest correct token: `[LOGIC TO BE CONFIRMED]` / `[SOURCE REQUIRED]` / `[DECISION REQUIRED]`.
2. Continue by proposing **2–3 options**, with trade-offs, and a recommendation **inside current authority**.
3. If a human-operator decision is required, ask for the **minimum** decision needed and stop expanding scope.

State confidence for decisions that matter. If confidence is below the
threshold needed to proceed, stop and escalate (do not “power through”
uncertainty).

**Deliberate slack**: default to operating **below** the practical
cognitive/latency ceiling so wrap-ups, repulsion signals, and small process
fixes actually happen. **Improvement compounds**; running at the edge trades
away the compounding loop.

## Hard rule: two attempts → stop (no thrash)

This is a **hard stop** to prevent compounding error and wasted search.

### Definitions

- **Goal**: a single, testable objective with explicit acceptance criteria (even if coarse).
- **Attempt**: one coherent go at the problem (usually against a goal), ending with either success, a clear failure mode, or a tokenized unknown.

### Rule

You get **at most two attempts** (two goes) to solve a problem **unless** you are demonstrably “nearly cracked it”:

- **Nearly cracked** means: you can complete the remainder in one more bounded step **without** new external facts, **or** you already have a correct mechanism and only need mechanical execution.

If after two attempts you are not in that state: **stop**.

### What to do when you stop (apply in order)

1. **Quick evidence search**: one targeted internet search on the specific blocker — not general exploration. Return **<=3** assessed bits, tag **`[CURRENT BEST EVIDENCE]`**, resume. Follow `01_truth/processes/2026-04_quick-evidence-search_sop_v1.md`.
2. **Consult** (when available and quick): ask the minimum question needed to unblock.
3. **Park to Qwen (hive mind)**: if still stuck after research, send full context (attempts, research findings, specific blocker) to Qwen. If Qwen can answer quickly, wait and continue. If not quick, park the process cleanly and end the session — Qwen guarantees the restart when a solution is found. See `01_truth/processes/2026-04_job-wrapup_and_escalation-note_sop_v1.md`.
4. **Formal research remit** (only when needed): open a bounded remit for deep synthesis across multiple sources/methodologies (see `01_truth/processes/2026-04_research-department_charter_v1.md`). Do not route here when a quick evidence search is sufficient.

**After parking**: write the escalation note (`status: parked`, YAML frontmatter with full context) and the stateless handover (`status: parked`). Qwen processes the signal — known-class blockers are resolved automatically and trigger a new agent; novel decisions are routed to Ewan, who decides, and Qwen triggers the new agent. Nothing is lost. The process restarts. No human needs to remember to restart it.

Wrap-ups live in `03_shadow/job-wrapups/` (reference-only; learning, not
authority).

When you import outside material:

1. Put sanitised raw material into `90_archive/` (reference / provenance posture;
   do not treat as current law — see `90_archive/README.md`).
2. Extract the smallest usable, truth-shaped slice into `01_truth/...`
   (1–2 pages, operational).
3. Index the extraction in `00_authority/MANIFEST.md` as **Candidate authority**.

When you produce durable changes:

- Prefer **deterministic artifacts first**
  (schemas/contracts/processes/interfaces) before code.
- Do not create parallel policy spines outside `00_authority/`.

## Promotion rule (shadow/archive → truth)

Promotion is deliberate:

- `90_archive/` and `03_shadow/` content does not become truth by proximity.
- Truth candidates live in `01_truth/` and become usable only when indexed in `MANIFEST.md`.
- Contradictions are not merged; log `[DECISION REQUIRED]` and keep both with sources.

## Success condition (v1)

Any agent with zero context can read `00_authority/` and reliably answer:

- What is authoritative vs candidate vs reference-only?
- What belongs where (routing)?
- What to do when uncertain (tokens + options)?
- Where the proof lives (source paths)?

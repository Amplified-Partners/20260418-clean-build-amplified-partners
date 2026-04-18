---
title: Partner transfer instructions (Amplified Partners workspace)
date: 2026-04-17
version: 9
status: draft
---

## Purpose

You are helping populate this workspace so agents can work fast **without** being degraded by noise, personal data, contradictory legacy material, or “helpful” drift away from `00_authority/PRINCIPLES.md`.

## Primary goal (why transfer exists)

Transfers exist to **strip load** and increase **clarity for agent decision-making**.

- If an import does not reduce cognitive load or produce **changes** to **routing**, **constraints**, or **acceptance criteria**, or resolve a `[DECISION REQUIRED]`, it is bloat.
- Narrative is allowed only when it materially improves understanding, and it must be marked `[NARRATIVE]`.

### Goal clarity (two altitudes)

- **Large sense:** keep the workspace **congruent with principles**, **auditably sourced**, and **safe to automate** (clear authority boundaries + reversible imports).
- **Small sense:** each import should answer, in one pass: **what arrived**, **why it matters**, **what changed** (constraints/decisions), and **where the proof lives** (archive path + extraction path).

### Recording discipline (honesty without bloat)

We record what is needed for **integrity** and **learning**, not everything by default.

- **Archive-first for raw provenance** (keep originals intact; sanitise only what must be removed for safety).
- **Extract the smallest “truth-shaped” slice** into `01_truth/` when something becomes operational.
- Prefer **repeatable signals** (decision deltas, constraints, failure modes, acceptance criteria) over narrative volume.

This is a **partner-to-partner** collaboration with **equal standing** and **clear roles**:

- **Partner A (Logic & Authority):** tighten `00_authority/` (intent, principles, decisions) and shape what becomes authoritative.
- **Partner B (Transfer, Sanitisation, Congruence Check):** bring in relevant peripheral context safely via `90_archive/`, compare it against the **intent** of the workspace (see `PROJECT_INTENT.md` + `PRINCIPLES.md`), extract usable truth into `01_truth/`, and keep `MANIFEST.md` updated.

Neither role outranks the other; we are separating responsibilities to keep the environment congruent and the work reversible.

## Foundations, constraints, permissions (transfer lens)

Transfers succeed when these three are right — same spine as the rest of the
clean build:

1. **Foundations** — authority index (`MANIFEST.md`), principles, intent; no
   parallel law outside `00_authority/`.
2. **Constraints** — tokens, modes, ladder, file budget; smallest promoted slice
   into `01_truth/`.
3. **Permissions** — truth/world → human operator; `.cursor/` hooks only via
   `.cursor/HOOKS_TESTING_NEED.md`; new GitHub org repos per `MANIFEST.md` §
   Permissions.

Start by reading these files (in order):

1. **`AGENTS.md` (repo root)** — **§ Agent session (clean-build) — first 60 seconds**
   (canonical read order, bounded autonomy, mistakes-as-signal). **Do not skip.**
2. `00_authority/NORTH_STAR.md` (agent-first operating contract + file budget)
3. `00_authority/MANIFEST.md` (authority index)
4. `00_authority/PRINCIPLES.md` (non‑negotiable compass)
5. `00_authority/PROJECT_INTENT.md` (intent + upstream operator signal — agent operands)
6. `00_authority/REMIT_PARTNER_CURSOR.md` (roles + non-authoritative origin quotes)

## Human operator input (rule of thumb)

**Truth or outside world → Ewan.** If the answer changes what we may **treat as true** (`MANIFEST.md`, promotion, contradictions) or what we **owe the outside world** (client, privacy, legal posture), **stop and involve the human operator**.

**Cleanliness inside the frame → partners.** If it only improves how the machine runs **inside** stated intent and `PRINCIPLES.md`, **no escalation required** unless you are unsure — then mark `[LOGIC TO BE CONFIRMED]` or `[DECISION REQUIRED]`.

The anchor above all of this: **`00_authority/README.md`** and **`PRINCIPLES.md` — Absolute (human operator)**.

## Golden rule (authority)

`00_authority/MANIFEST.md` is the **only authoritative index**.

- If it’s **not listed** there, it is **not authoritative** (even if it seems important).
- If anything is incomplete, mark it **literally**: `[LOGIC TO BE CONFIRMED]`.

## Where to put things (routing)

- **Sanitised legacy docs / exports (reference only):** `90_archive/`
- **Anything intended to become “truth” (shaped + congruent):** `01_truth/`
  - **Schemas / typed contracts:** `01_truth/schemas/`
  - **Processes that should become deterministic:** `01_truth/processes/`
  - **Interfaces / API payloads / failure modes:** `01_truth/interfaces/`
- **Experiments / curveballs / “maybe” ideas:** `03_shadow/`
- **Code, scripts, infra (only when asked):** `02_build/`

## Sanitisation requirements (minimum bar)

Before you move *anything* into this workspace:

- Remove by default: emails, phone numbers, addresses, account numbers, credentials/API keys, client identifiers, and other sensitive identifiers.
- Replace with placeholders when needed: `CLIENT_A`, `STAFF_1`, `VENDOR_X`, `LOCATION_1`.
- **Names**:
  - remove names that are **not needed** for provenance/attribution; or
  - keep names when they are **fair attribution** under `PRINCIPLES.md` (public-domain contributors, named colleagues inside the work environment), or when required to preserve an auditable chain.
- Keep: structure, rubrics, schemas, method steps, acceptance criteria, failure modes.
- No secrets, ever.

## Human operator context (optional, high-signal)

Sometimes the fastest path to clarity is a small, honest “who/why” capsule for the **human operator** (Ewan), **without** turning biography into authority.

Rules:

- **Archive-first**: if it originates outside this repo, store the raw material in `90_archive/` unchanged (except sanitisation), then extract.
- **Ego-aware framing is allowed as fact about process, not as claims about people**: record *uncertainty*, *biases*, and *preferences* as hypotheses and mark `[LOGIC TO BE CONFIRMED]` where needed.
- **Minimum viable capture**: prefer a 1-page structured note over a dump. If a detail does not change decisions or constraints, omit it.
- **Learning opportunities**: if ingestion reveals a repeatable mistake pattern, capture it as a short “lesson” with sources (still non-authoritative unless promoted).

Suggested filename patterns (non-authoritative unless promoted):

- `90_archive/context/YYYY-MM-DD_operator-context-capsule.md` (structured who/why)
- `90_archive/context/YYYY-MM-DD_operator-voice-capsule_<name>.md` (informal register on purpose — see `90_archive/context/2026-04-16_operator-voice-capsule_ewan.md`)

## Required header for every transferred doc (top of file)

Paste this at the top of each transferred document:

```text
Status: [NON-AUTHORITATIVE] | [LOGIC TO BE CONFIRMED] | Active
Sanitisation: done — removed <what>, replaced <what>
Source: <where this came from> (original filename/path/date if known)
```

## Approved status tokens

Use these literally:

- `[LOGIC TO BE CONFIRMED]`
- `[SOURCE REQUIRED]`
- `[DECISION REQUIRED]`
- `[NON-AUTHORITATIVE]`
- `[NARRATIVE]`

## What NOT to do

- Do not “improve” or rewrite archived docs in `90_archive/` (store them as reference).
- Do not promote anything into `01_truth/` unless it is already **sanitised** and **shaped**.
- Do not merge contradictory definitions; instead flag them as `[DECISION REQUIRED]` and leave both with sources.
- Do not add new “policy spines” outside `00_authority/` (keep authority small).
- Do not treat narrative as truth. Narrative is allowed, but must be marked `[NARRATIVE]` and must not contradict `PRINCIPLES.md` + `PROJECT_INTENT.md`.

## Narrative / verbatim in shaped extractions (when it helps)

Same rule as `00_authority/PRINCIPLES.md` — **Documentation + audience → Narrative or verbatim**: add a line or short quote **only** when it **reduces confusion** or preserves intent that polish would erase. Mark **`[NARRATIVE]`** (and verbatim literally). If it grows beyond a tight aside, **archive** under `90_archive/context/` (or appropriate archive path) and **link**; do not let narrative bloat `01_truth/`.

## Principles conformance (before you “shape” anything)

Before creating/updating canonical extractions, explicitly check:

- **Win–win vs honesty**: if forced to choose, follow `PRINCIPLES.md` (win–win trumps honesty collisions).
- **Privacy**: client-identifying material stays out unless explicitly allowed and sanitized.
- **Attribution**: preserve upstream credit and partner contribution; no “anonymous theft” of ideas.
- **Meritocracy of ideas**: do not smuggle authority via voice; cite sources and show reasoning.

## Your transfer workflow (step-by-step)

1. Put sanitised raw material into `90_archive/` with the required header.
2. If content is narrative, mark it `[NARRATIVE]` and keep it in `90_archive/` unless explicitly requested elsewhere.
3. If content contains usable logic but is in the wrong format, you may **refine the format** (without changing intent) into a short, normalised extraction (1–2 pages) in the appropriate `01_truth/` subfolder.
4. Update `00_authority/MANIFEST.md`:
   - Add the new `01_truth/...` file under **Candidate authority** (or **Authoritative now** if explicitly confirmed).
5. If you hit uncertainty, stop and write `[DECISION REQUIRED]` plus:
   - what is ambiguous
   - what you need from the **human operator** to resolve it

### Baton-pass refinement (new working loop)

- Partner B works primarily in: `90_archive/` → `01_truth/` → `MANIFEST.md`.
- Partner A works primarily in: `00_authority/` (tightening intent, principles, and decisions).
- When you discover a missing definition or conflict, don’t “solve” it—log it as `[DECISION REQUIRED]` and link the sources.

## The only success metric

After your transfer, an assistant should be able to answer:

> “What is true here, what is not true yet, and where is the proof?”

…without reading anything outside this workspace.

## Changelog

### v2 — 2026-04-16

- Realigned transfer workflow to `PRINCIPLES.md` (principles-first), removed dead glossary references, and added archive-first human-operator context guidance with provenance-without-bloat rules.

Signed-by: Keystone (AI) — 2026-04-16

### v3 — 2026-04-16

- Fixed decision token typos (`[DECISION REQUIRED]`).
- Added explicit **principles conformance** gate before shaping canonical extractions.
- Removed remaining “clean room / founder / glossary” drift language.

Signed-by: Keystone (AI) — 2026-04-16

### v4 — 2026-04-16

- Added explicit **goal clarity** framing (large vs small) and **recording discipline** guidance (provenance + learning without unnecessary capture).

Signed-by: Keystone (AI) — 2026-04-16

### v5 — 2026-04-16

- Documented optional **operator voice** archive filename pattern (human register alongside agent-clear norms).

Signed-by: Keystone (AI) — 2026-04-16

### v6 — 2026-04-16

- Cross-linked **sparing narrative / verbatim** rules for shaped `01_truth/` extractions (aligned to `PRINCIPLES.md` v8).

Signed-by: Keystone (AI) — 2026-04-16

### v7 — 2026-04-16

- Added **Human operator input (rule of thumb)** — truth/outside-world vs in-frame work; pointer to **Absolute** in `README.md` + `PRINCIPLES.md`.

Signed-by: Keystone (AI) — 2026-04-16

### v9 — 2026-04-17

- Read-order step 5: `PROJECT_INTENT.md` described as **upstream operator signal —
  agent operands** (aligned with agent-primary audience rule).

Signed-by: Keystone (AI) — 2026-04-17

### v8 — 2026-04-17

- **Foundations / constraints / permissions** triad (transfer lens); read order now
  starts with root **`AGENTS.md`** § first 60 seconds, then existing authority stack.

Signed-by: Keystone (AI) — 2026-04-17

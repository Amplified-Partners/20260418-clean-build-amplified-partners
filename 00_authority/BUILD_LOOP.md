---
title: Build loop (plan → research → prove)
date: 2026-04-16
version: 8
status: draft
---

## Purpose

Define the end-to-end loop for building inside this clean room.

## Build decomposition (big picture → process)

The build is intentionally hierarchical:

1. **Whole build** (global north star + constraints + acceptance for the system)
2. **Department builds** (department-level methodology + interfaces to other departments)
3. **Sub-department builds** (refined methodology + tighter scope + local constraints)
4. **Individual processes** (leaf runnable units: inputs → steps → outputs → failure modes)

### Research placement (chunked by layer)

- **Quick evidence search** (narrow external lookup, any agent):
  `01_truth/processes/2026-04_quick-evidence-search_sop_v1.md` —
  parameterized, **≤3** assessed bits, tagged **`[CURRENT BEST EVIDENCE]`**;
  not a substitute for formal remit when synthesis is heavy.
- **Department research** answers: “What is the best production-real methodology for this department’s lane?”
- **Sub-department research** answers: “What must be refined/changed for this narrower scope?”
- **Process research** answers: “What is the minimum evidence needed to run this process safely?”

### Research remit template (required for every research chunk)

Each research chunk must declare:

- **Start**: what question is being answered (one sentence)
- **End**: what artifact(s) will exist when done (paths + filenames)
- **Non-goals**: what is explicitly out of scope (prevents sprawl)
- **Inputs**: what is already known (manifest-listed artifacts + archive sources)
- **Outputs**: what changes to routing/constraints/acceptance criteria are expected (or `[DECISION REQUIRED]`)
- **Stop rule**: when to stop (token thresholds, timebox, or “good enough for next layer”)
- **Remit ID**: a stable identifier for traceability (example: `REM-2026-04-16-001`)

## Neutral IDs, deduplication, and cross-department linkage

Cross-department duplication is expected. The system prevents pain by separating:

- **Canonical process** (one runnable definition of the shared logic)
- **Department variants** (thin wrappers that only specify deltas: constraints, routing, acceptance criteria)

### ID scheme (neutral, stable, linkable)

Use neutral IDs (do not encode org politics in the ID):

- **Process family ID**: `PF-<short-slug>` (example: `PF-intake-sanitize`)
- **Canonical process ID**: `PC-<short-slug>-v<n>` (example: `PC-intake-sanitize-v1`)
- **Variant ID**: `PV-<dept>-<short-slug>-v<n>` where `<dept>` is a short neutral lane code (example: `PV-ops-intake-sanitize-v1`)

### Required linkage fields (in frontmatter or a top “Links” block)

Every department/sub-department/process doc should include:

- `process_family_id`
- `canonical_process_id` (if this is canonical) **or** `variant_of` (if this is a variant)
- `parents`: links/paths to the parent methodology doc(s)
- `children`: links/paths to child process atoms (if any)

### Deduplication rules

- If two departments would write the same steps: write **one canonical** process in `01_truth/processes/` and make department docs **variants** that only document deltas.
- If logic is “the same but constraints differ”: keep one canonical; variants only change constraints/acceptance criteria/routing.
- If two chunks answer the same research question: merge remits or mark `[DECISION REQUIRED]` (pick one canonical answer path).

### Inter-department interfaces (handshake)

Department methodology docs should include a small table:

- **Consumes** (inputs from other departments; schemas/interfaces)
- **Produces** (outputs to other departments; schemas/interfaces)
- **Conflicts** (if any) → `[DECISION REQUIRED]` (do not merge silently)

## Clarity rules (chunk size + language)

- Write for **agents**: operational, runnable, and unambiguous.
- Include enough data to prevent confusion; exclude anything that increases cognitive load without producing:
  - changes to routing / constraints / acceptance criteria, or
  - resolution of a `[DECISION REQUIRED]`.
- If a document becomes large, split it by **logical process boundary** (two runnable parts are better than one mixed blob).
- **Two attempts → stop** (hard anti-thrash): see `00_authority/NORTH_STAR.md` — after two testable attempts (two goes), stop and route to consult / quick evidence lookup / bounded research remit.

## Loop (start → finish)

### 1) Plan from what is known (visible reality)

- Plan using only what is present and indexable here (per `00_authority/MANIFEST.md`).
- Mark gaps and assumptions explicitly:
  - `[LOGIC TO BE CONFIRMED]` / `[SOURCE REQUIRED]` / `[DECISION REQUIRED]`

**Done means (Step 1):**

- A written plan exists with:
  - the target artifact(s) to produce (schema/process/interface)
  - explicit inputs (paths/refs)
  - explicit uncertainty tokens where needed (no silent gaps)

### 2) Research to state of the art (filter for “production-real”)

Goal: upgrade assumptions into the best available **proven, validated, production-ready** methods.

- Prefer proven practice and standards over novelty.
- Do not adopt “published” claims by default; require evidence.
- Store provenance in `90_archive/` and extract only the runnable slice into `01_truth/`.
- Chunk research by **layer** using the **Research remit template** above.
- Each chunk must produce a **bounded** extraction (1–2 pages) unless `[DECISION REQUIRED]` expands scope.

**Done means (Step 2):**

- The plan’s assumptions are either:
  - supported by sources captured in `90_archive/` + minimal runnable extraction(s) in `01_truth/`, or
  - explicitly marked `[SOURCE REQUIRED]` / `[LOGIC TO BE CONFIRMED]`.
- At least one **Research remit** exists for the active layer (department / sub-department / process), with explicit start/end/non-goals.

### 3) Establish a baseline (authoritative, but explicitly pending proof)

- Promote the resulting methodology as the starting baseline when it passes:
  - `00_authority/PROMOTION_GATE.md`
- If it still requires proof-by-testing, mark that explicitly as:
  - `[LOGIC TO BE CONFIRMED]` with a concrete test plan pointer (next step).

**Done means (Step 3):**

- The baseline artifact is indexed correctly in `00_authority/MANIFEST.md` (candidate or authoritative).
- Any unproven claim is explicitly paired with a test plan pointer.

### 4) Formalize to math where possible

Goal: reduce ambiguity and enable scalable testing.

- Translate steps into:
  - explicit inputs/outputs
  - measurable acceptance criteria
  - deterministic invariants
- If a step can be expressed as a function, threshold, or metric, do it.

**Done means (Step 4):**

- Each step has measurable acceptance criteria (even if coarse).
- Any math form is written down (variables/thresholds/metrics), or explicitly marked `[LOGIC TO BE CONFIRMED]`.

### 5) Test at scale (theoretical / synthetic where valid)

Goal: catch most defects cheaply and early.

- Use scalable tests when they are legitimate for the claim.
- Treat this as evidence, not certification.

**Done means (Step 5):**

- Scalable tests exist and produce recorded results.
- Failures are recorded as artifacts and produce changes to routing/constraints/acceptance criteria, or a `[DECISION REQUIRED]`.

### 6) Test the last 10% in reality (proof you can stand behind)

Goal: claims you can truthfully say were tested.

- Run real-world tests where synthetic/theoretical testing cannot substitute.
- Record outcomes and failures as artifacts; update truth and gates.

**Done means (Step 6):**

- Real-world test evidence exists for the claims that matter.
- If reality contradicts the baseline: trigger rollback/procedure below.

## Conflict protocol (do not merge contradictions)

When “state of the art” or test results contradict current authority:

1. Mark `[DECISION REQUIRED]` and record both positions with source paths.
2. Do not merge by invention.
3. Resolve by updating the authoritative artifact only after the decision is made and logged.

## Evidence ladder (minimal)

Match claim type to evidence type:

- **Security/compliance claim** → standard/benchmark + implementation evidence + test evidence.
- **Process claim** → runnable spec + repeatable results.
- **Math claim** → derivation/definition + test coverage that exercises the edge cases.
- **Vendor claim** → treat as `[SOURCE REQUIRED]` until independently validated.

## Rollback / reversibility rule

If an authoritative baseline fails Step 5 or Step 6 materially:

1. Revert the manifest promotion (authoritative → candidate) or supersede with a corrected versioned artifact.
2. Record the failure and the correction in `00_authority/DECISION_LOG.md`.
3. Update the gate/check so the same failure mode is caught earlier next time.

## Boundary: what math cannot certify

Some domains require Step 6 (real-world proof) even if Steps 4–5 look strong:

- human communication/voice UX
- operational reliability under real load
- privacy/compliance behavior in real integrations
- any claim where you must truthfully say “we tested this in reality”

## Output artifacts (what the loop produces)

- `01_truth/schemas/` / `interfaces/` / `processes/`: runnable artifacts with provenance and tokens.
- `00_authority/MANIFEST.md`: authoritative index of what can be relied on.
- `00_authority/DECISION_LOG.md`: promotions and consequential changes.

## Job wrap-up (learning, not criticism)

Every job ends with a small wrap-up (finished or paused/blocked/handed off).
When a job cannot proceed after quick research, the wrap-up must include an
escalation note so the next lane can pick up without re-deriving context:
`01_truth/processes/2026-04_job-wrapup_and_escalation-note_sop_v1.md`.

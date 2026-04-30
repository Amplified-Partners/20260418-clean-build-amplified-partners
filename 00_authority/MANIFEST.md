---
title: Governed workspace manifest (authoritative inventory)
date: 2026-04-29
version: 37
status: draft
---

<!-- markdownlint-disable-file MD013 -->

## How to read this

This file is the **authority manifest** for this governed workspace.

- Only items listed under **Authoritative now** may be treated as truth without extra confirmation.
- Items under **Candidate authority** are usable, but must be treated as `[LOGIC TO BE CONFIRMED]`.
- Items under **Reference only** are context; do not use them as foundations for decisions or code.

## GitHub repository naming (agent-default assumption)

Under organisation **`Amplified-Partners`**, a **backup / clean-build** Git remote
(if used) uses this **exact slug shape** — no variants, no renames for milestones:

`<YYYYMMDD>-clean-build-amplified-partners`

Rules (fixed so agents do not infer):

- **`YYYYMMDD`** — calendar **date the repository was created on GitHub** (remote
  birth date), **not** “last big push” and **not** updated as work continues.
- Literal tokens **`clean-build`** then **`amplified-partners`**, **lowercase**,
  **hyphens only**, in that order after the date.
- **Timeline of work** — `git log` / commits; never encode “important day” by
  changing the repo slug.

**Default remote URL shape (SSH):**
`git@github.com:Amplified-Partners/<slug>.git`

**Assumption before touching disk:** agents treat this slug rule as canonical for
GitHub; the local directory name (`Clean-Build-AmplifiedPartners`) is a dev path,
not the GitHub slug. Do not guess another pattern under this org for this lane.

## Permissions (explicit)

- **GitHub org `Amplified-Partners`:** creating **new** repositories (including
  clean-build / backup slugs per § GitHub repository naming) is a **human-operator
  (Ewan)** action unless delegated in writing. Agents do not create org repos on
  their own initiative.
- **`.cursor/`:** changing **policy** (what counts as authoritative behaviour) or
  **adding hooks** belongs under normal promotion / **TESTING NEED** rules (see
  `.cursor/HOOKS_TESTING_NEED.md`). Mechanical typo fixes in hook scripts are not
  a substitute for turning hooks **on** — `"hooks": {}` stays default until the
  gate is satisfied.

## Status tokens (approved)

- `[LOGIC TO BE CONFIRMED]`
- `[SOURCE REQUIRED]`
- `[DECISION REQUIRED]`
- `[NON-AUTHORITATIVE]`
- `[NARRATIVE]`
- `[CURRENT BEST EVIDENCE]`

## Authoritative now

- `AGENTS.md`
- `00_authority/AGENTS.md`
- `00_authority/TAXONOMY.md` (entity definitions, agent roles, locked terminology — company structure, operating model)
- `00_authority/README.md`
- `00_authority/MANIFEST.md`
- `00_authority/NORTH_STAR.md`
- `00_authority/PROJECT_INTENT.md`
- `00_authority/REMIT_PARTNER_CURSOR.md`
- `00_authority/PARTNER_TRANSFER_INSTRUCTIONS.md`
- `00_authority/PRINCIPLES.md` `[LOGIC TO BE CONFIRMED]` (norms downstream of **Absolute** in root `AGENTS.md`; `anchor_lineage: 35` in file frontmatter — see § Provenance and versioning there)
- `00_authority/SIGNATURES.md` (every AI signs committed work; Radical Attribution applied mechanically; agent chooses format)
- `00_authority/USE_IT_OR_CUT_IT.md` (sounds good + built + unused = cut; remediation rule for bloat; archive exempt)
- `00_authority/OPINION_CONFIDENCE.md` (opinions labelled + confidence numbered; tiered thresholds 50% / 85% / 95% by reversibility)
- `00_authority/PROMOTION_GATE.md`
- `00_authority/BUILD_LOOP.md`
- `00_authority/DECISION_LOG.md`
- `STATUS.md` (operations status board — async handshake between Devon and OpenClaw; versioned handoffs, no chat)
- `.cursor/rules/stateless-handover-kaizen.mdc` `[LOGIC TO BE CONFIRMED]` (mechanical enforcement of existing handover policy; not a separate policy spine)
- `.cursor/hooks.json` `[LOGIC TO BE CONFIRMED]` (**No hooks** — `"hooks": {}`. **TESTING NEED:** reinstatement gate → `.cursor/HOOKS_TESTING_NEED.md`; history → `03_shadow/2026-04-16_stop-hook_followup-checklist-loop_bug-report.md` § Final resolution)
- `.cursor/hooks/stateless-handover-stop.py` `[LOGIC TO BE CONFIRMED]` (**Dormant / testing only** — **not invoked** while `hooks` is empty; do not treat as enforcement)

## Candidate authority (logic to be confirmed)

- `01_truth/README.md` `[LOGIC TO BE CONFIRMED]` (agent routing index: `processes/` vs `schemas/` vs `interfaces/`; ties to **Clean-build file budget** in `NORTH_STAR.md`)
- `01_truth/processes/` `[LOGIC TO BE CONFIRMED]` (process inventory to be populated)
  - `01_truth/processes/2026-03_business-bible_three-layer-model_v1.md` `[LOGIC TO BE CONFIRMED]`
  - `01_truth/processes/2026-03_bible-consolidation_five-phase-approach_v1.md` `[LOGIC TO BE CONFIRMED]`
  - `01_truth/processes/2026-03_deterministic-imperative_planning-vs-execution_v1.md` `[LOGIC TO BE CONFIRMED]`
  - `01_truth/processes/2026-04_workspace-clarity-roadmap_v1.md` `[LOGIC TO BE CONFIRMED]`
  - `01_truth/processes/2026-04_decomposition-and-grain_v1.md` `[LOGIC TO BE CONFIRMED]`
  - `01_truth/processes/2026-04_hygiene-role-charter_v1.md` `[LOGIC TO BE CONFIRMED]`
  - `01_truth/processes/2026-04_operating-rhythm-check-seams_v1.md` `[LOGIC TO BE CONFIRMED]`
  - `01_truth/processes/2026-04_gated-pipelines_privacy-tokenization_capability-routing_v1.md` `[LOGIC TO BE CONFIRMED]`
  - `01_truth/processes/2026-04_methodology-prospecting_five-candidates_v1.md` `[LOGIC TO BE CONFIRMED]`
  - `01_truth/processes/2026-04_methodology-scoring-rubric_v1.md` `[LOGIC TO BE CONFIRMED]`
  - `01_truth/processes/2026-04_agent-md_objectivity-specialist_v1.md` `[LOGIC TO BE CONFIRMED]`
  - `01_truth/processes/2026-04_research-department_charter_v1.md` `[LOGIC TO BE CONFIRMED]`
  - `01_truth/processes/2026-04_quick-evidence-search_sop_v1.md` `[LOGIC TO BE CONFIRMED]`
  - `01_truth/processes/2026-04_job-wrapup_and_escalation-note_sop_v1.md` `[LOGIC TO BE CONFIRMED]`
  - `01_truth/processes/2026-04_research-operations-cadence_v1.md` `[LOGIC TO BE CONFIRMED]`
  - `01_truth/processes/2026-04_research-on-research_bootstrap-remit_v1.md` `[LOGIC TO BE CONFIRMED]`
  - `01_truth/processes/2026-04_stateless-handover_neutrality-clause_v1.md` `[LOGIC TO BE CONFIRMED]` (candidate addendum to the job-wrapup SOP; neutrality rule for stateless handovers; authoritative `00_authority/OPINION_CONFIDENCE.md` references this file)
- `01_truth/schemas/` `[LOGIC TO BE CONFIRMED]` (schema contracts to be populated)
  - `01_truth/schemas/README.md` `[LOGIC TO BE CONFIRMED]` (folder purpose stub)
- `01_truth/interfaces/` `[LOGIC TO BE CONFIRMED]` (API contracts to be populated)
  - `01_truth/interfaces/README.md` `[LOGIC TO BE CONFIRMED]` (folder purpose stub)
- `02_build/README.md` `[LOGIC TO BE CONFIRMED]` (runnable artefacts routing stub)
- `03_shadow/README.md` `[LOGIC TO BE CONFIRMED]` (experiment routing stub)
- `03_shadow/job-wrapups/README.md` `[NON-AUTHORITATIVE]` (wrap-ups/escalation notes location; learning only)

## Reference only (sanitised; never authoritative by default)

- `.cursor/HOOKS_TESTING_NEED.md` `[NON-AUTHORITATIVE]` (**TESTING NEED** — gate checklist before any Cursor hook wiring; production posture is **no hooks**)
- `README.md` `[NON-AUTHORITATIVE]` (root quick-start pointer to authority entrypoints)
- `90_archive/` `[NON-AUTHORITATIVE]`
  - `90_archive/README.md` `[NON-AUTHORITATIVE]` (archive gate for agents — no bulk-read of `inbox/` dumps; triage vs promotion)
  - `90_archive/authority-history/` `[NON-AUTHORITATIVE]` (verbatim snapshots of earlier `00_authority/` versions; do not treat as current policy)
  - `90_archive/2026-03_amplified-consolidated-architecture_narrative.md` `[NARRATIVE] [NON-AUTHORITATIVE] [IMPERFECT-BUT-INTENTFUL]`
  - `90_archive/2026-03_amplified-consolidated-architecture_full.txt` `[NON-AUTHORITATIVE]`
  - `90_archive/context/README.md` `[NON-AUTHORITATIVE]` (context folder convention)
  - `90_archive/context/2026-04-16_operator-voice-capsule_ewan.md` `[NARRATIVE] [NON-AUTHORITATIVE]` (human operator voice; not policy)
  - `90_archive/beautiful-and-golden/` `[NON-AUTHORITATIVE]` (archived architecture docs from the beautiful-and-golden sibling repo, preserved before tombstoning)
    - `90_archive/beautiful-and-golden/ARCHITECTURE.md` `[NON-AUTHORITATIVE]`
    - `90_archive/beautiful-and-golden/PUBLIC_README.md` `[NON-AUTHORITATIVE]`
    - `90_archive/beautiful-and-golden/SUSTAINABILITY.md` `[NON-AUTHORITATIVE]`

## Changelog

### v37 — 2026-04-29

- Added `STATUS.md` to **Authoritative now**: two-way async operations board between Devon (infrastructure) and OpenClaw (coordination). GitHub as single source of truth for cross-agent status. Versioned handoffs, no chat.

Signed-by: Devon (Devin session `aa4d863ad679468692e75a40b8825358`) — 2026-04-29

### v36 — 2026-04-29

- Added `00_authority/TAXONOMY.md` to **Authoritative now**: canonical entity definitions (company structure, agent roster, locked terminology, operating model). Covers the Amplified Partners entity hierarchy, Devon/OpenClaw/Cursor roles, and terminology that was previously only in session chat.
- Frontmatter `date` advanced to 2026-04-29.

Signed-by: Devon (Devin session unknown — committed on main before this PR) | 2026-04-29

### v36-pre (archive beautiful-and-golden) — 2026-04-26

- Indexed new `90_archive/beautiful-and-golden/` entries (3 files: `ARCHITECTURE.md`, `PUBLIC_README.md`, `SUSTAINABILITY.md`) under "Reference only". Archived from sibling repo before tombstoning.

Signed-by: Devon (Devin session `devin-ab66d8a5c2b64927b65a4ab87acc47ee`) — 2026-04-26

### v36-pre (bibliography fix) — 2026-04-23

- Bibliography fix follow-up to v35: root `AGENTS.md` section heading renamed from "Agent session (clean-build) — first 60 seconds" to "Agent session — first 60 seconds" created 5 dead cross-references. Updated all live references: `README.md`, `01_truth/README.md`, `00_authority/README.md` (bumped to v8), `00_authority/NORTH_STAR.md` (bumped to v12), `00_authority/PARTNER_TRANSFER_INSTRUCTIONS.md` (bumped to v10). `00_authority/DECISION_LOG.md` entry at line 65 is a historical record of the 2026-04-17 decision as-named-then; left intact per additive-edits rule.

Signed-by: Devon (Devin session `4cc8b0d727684f94a8f055853099d8e6`) — 2026-04-23

### v35 — 2026-04-23

- `00_authority/SIGNATURES.md` bumped to v2: PR template reference fix (`.github/pull_request_template.md` now exists).
- `AGENTS.md` (root) tightened: duplication cut, new "PR reviewers — what to flag" section added, length reduced ~35%.
- `.github/pull_request_template.md` created: pre-merge checklist wired to `SIGNATURES.md` / `DECISION_LOG.md` / `MANIFEST.md` rules.
- `.github/dependabot.yml` created: weekly GitHub Actions version updates.

Signed-by: Devon (Devin session `4cc8b0d727684f94a8f055853099d8e6`) — 2026-04-23

### v34 — 2026-04-23

- Indexed three new **Authoritative now** entries: `00_authority/SIGNATURES.md` (every AI signs committed work), `00_authority/USE_IT_OR_CUT_IT.md` (unused implementations are cut; archive exempt), `00_authority/OPINION_CONFIDENCE.md` (opinions labelled + confidence numbered; tiered thresholds 50% / 85% / 95% by reversibility).
- Indexed one new **Candidate authority** entry: `01_truth/processes/2026-04_stateless-handover_neutrality-clause_v1.md` (candidate addendum to the job-wrapup SOP).
- Updated `AGENTS.md` first-60-seconds read-order to reference `SIGNATURES.md`.
- Frontmatter `date` advanced to 2026-04-23 to reflect this edit.

Signed-by: Devon (Devin session `4cc8b0d727684f94a8f055853099d8e6`) — 2026-04-23

### v2 — 2026-04-16

- Renamed manifest framing to **governed workspace**.
- Added missing authoritative entry for `00_authority/PARTNER_TRANSFER_INSTRUCTIONS.md`.
- Indexed an archived glossary snapshot under `90_archive/` (later removed; see v3).

Signed-by: Keystone (AI) — 2026-04-16

### v3 — 2026-04-16

- Removed `00_authority/GLOSSARY.md` from authoritative inventory (deleted).
- Removed archived glossary snapshot entry (deleted).

Signed-by: Keystone (AI) — 2026-04-16

### v4 — 2026-04-16

- Corrected v2 changelog wording to reflect glossary snapshot removal in v3.

Signed-by: Keystone (AI) — 2026-04-16

### v5 — 2026-04-16

- Indexed `90_archive/context/2026-04-16_operator-voice-capsule_ewan.md` under **Reference only** (operator voice; non-authoritative).

Signed-by: Keystone (AI) — 2026-04-16

### v6 — 2026-04-16

- Indexed **workspace clarity** process pack (`2026-04_*.md`), `schemas/README.md`, `interfaces/README.md`, `02_build/README.md`, `03_shadow/README.md`, and `90_archive/context/README.md` under **Candidate** / **Reference** as marked.

Signed-by: Keystone (AI) — 2026-04-16

### v7 — 2026-04-16

- Approved status token **`[CURRENT BEST EVIDENCE]`** (external lookup; not
  promotion by label).
- Indexed candidate process
  `01_truth/processes/2026-04_quick-evidence-search_sop_v1.md` (quick search:
  parameterized, **≤3** assessed bits, no firehose).
- Bumped `PRINCIPLES.md` anchor note to **v24+**.

Signed-by: Keystone (AI) — 2026-04-16

### v8 — 2026-04-16

- Terminology: anti-thrash rule is **two attempts → stop** (two goes), not
  “two goals”; canonical definitions in `00_authority/NORTH_STAR.md` v4+.
- Bumped `PRINCIPLES.md` anchor note to **v25+**.

Signed-by: Keystone (AI) — 2026-04-16

### v9 — 2026-04-16

- Indexed candidate SOP
  `01_truth/processes/2026-04_job-wrapup_and_escalation-note_sop_v1.md`
  (wrap-up after every job; escalation note when confidence remains below
  threshold after quick research).

Signed-by: Keystone (AI) — 2026-04-16

### v10 — 2026-04-16

- Bumped `PRINCIPLES.md` anchor note to **v28+**.

Signed-by: Keystone (AI) — 2026-04-16

### v11 — 2026-04-16

- Indexed `03_shadow/job-wrapups/README.md` as reference-only (wrap-up storage
  location + naming; learning notes, not authority).

Signed-by: Keystone (AI) — 2026-04-16

### v12 — 2026-04-16

- Bumped `PRINCIPLES.md` anchor note to **v29+** (wrap-up scores are calibration
  signals; **10 intentionally out of reach**).
- Updated wrap-up SOP scoring rules in
  `01_truth/processes/2026-04_job-wrapup_and_escalation-note_sop_v1.md` (v4).

Signed-by: Keystone (AI) — 2026-04-16

### v13 — 2026-04-16

- Updated `01_truth/processes/2026-04_quick-evidence-search_sop_v1.md` (v2) to
  require operational handoff fields when execution is the goal.

Signed-by: Keystone (AI) — 2026-04-16

### v14 — 2026-04-16

- Bumped `PRINCIPLES.md` anchor note to **v30+** (Kaizen via wrap-ups; audit
  trail as secondary; stateless handover continuity).
- Updated `01_truth/processes/2026-04_job-wrapup_and_escalation-note_sop_v1.md`
  (v5) with mandatory next-agent handover packet requirements.

Signed-by: Keystone (AI) — 2026-04-16

### v15 — 2026-04-16

- Bumped `PRINCIPLES.md` anchor note to **v31+** (omissions are process signals;
  exception notes when wrap-up cannot be completed).
- Updated `01_truth/processes/2026-04_job-wrapup_and_escalation-note_sop_v1.md`
  (v6) with **N/A discipline** + `_wrapup-exception.md` path.
- Added Cursor enforcement artifacts: `.cursor/rules/stateless-handover-kaizen.mdc`
  and `.cursor/hooks.json` → `.cursor/hooks/stateless-handover-stop.py`.

Signed-by: Keystone (AI) — 2026-04-16

### v16 — 2026-04-16

- Bumped `PRINCIPLES.md` anchor note to **v32+** (slime-mold Kaizen: explicit
  negative feedback for faster process refinement).
- Updated `01_truth/processes/2026-04_job-wrapup_and_escalation-note_sop_v1.md`
  (v7) + Cursor rule/hook checklist to include **negative signals** and
  **cut/absolute stop** reporting.

Signed-by: Keystone (AI) — 2026-04-16

### v17 — 2026-04-16

- Bumped `PRINCIPLES.md` anchor note to **v33+** (repulsion scoring 1–10 + banded
  routing).
- Updated `01_truth/processes/2026-04_job-wrapup_and_escalation-note_sop_v1.md`
  (v8) + Cursor rule/hook checklist to include **repulsion score** and clarify
  **leverage score (0–9)** vs repulsion.

Signed-by: Keystone (AI) — 2026-04-16

### v18 — 2026-04-16

- Synced `.cursor/rules/stateless-handover-kaizen.mdc` with the `stop` hook
  checklist (adds explicit **Repulsion bands** line).
- Bumped `01_truth/processes/2026-04_job-wrapup_and_escalation-note_sop_v1.md`
  to **v9** (handover packet includes **Repulsion bands** summary).

Signed-by: Keystone (AI) — 2026-04-16

### v19 — 2026-04-16

- Bumped `PRINCIPLES.md` anchor note to **v34+** (**deliberate slack / under the
  limit**: production + improvement co-primary).
- Updated `00_authority/NORTH_STAR.md` (v8) + `AGENTS.md` to encode the same
  default operating posture.
- Added `<!-- markdownlint-disable-file MD013 -->` to long-form authority +
  partner instruction markdown where line-length linting is noise.

Signed-by: Keystone (AI) — 2026-04-16

### v20 — 2026-04-16

- Bumped `01_truth/processes/2026-04_job-wrapup_and_escalation-note_sop_v1.md`
  to **v10**: **Stateless handover (mandatory)** section matches the canonical
  checklist (aligned with Cursor rule + `stop` hook).
- Updated `03_shadow/job-wrapups/README.md` (v2) with a pointer to that
  checklist.

Signed-by: Keystone (AI) — 2026-04-16

### v21 — 2026-04-16

- Bumped `01_truth/processes/2026-04_job-wrapup_and_escalation-note_sop_v1.md`
  to **v11**: handover footer matches canonical text (“band guide in the wrap-up
  SOP”), same as Cursor rule + `stop` hook.

Signed-by: Keystone (AI) — 2026-04-16

### v22 — 2026-04-16

- Bumped `01_truth/processes/2026-04_job-wrapup_and_escalation-note_sop_v1.md`
  to **v12** + synced `.cursor/rules/stateless-handover-kaizen.mdc`: repulsion
  score + repulsion bands bullets are single-line (matches `stop` hook; fixes a
  bad line wrap across “it signal”).

Signed-by: Keystone (AI) — 2026-04-16

### v23 — 2026-04-16

- Bumped `01_truth/processes/2026-04_job-wrapup_and_escalation-note_sop_v1.md`
  to **v13** + synced `.cursor/rules/stateless-handover-kaizen.mdc`: remaining
  handover checklist lines match the canonical single-line form (intro, cut/stop,
  tokens, leverage, repulsion footer), same as `stop` hook.

Signed-by: Keystone (AI) — 2026-04-16

### v24 — 2026-04-16

- Indexed root `AGENTS.md` and `00_authority/AGENTS.md` under **Authoritative now** (remove ambiguity about which partner instructions are in-force).
- Normalized the remit filename to `00_authority/REMIT_PARTNER_CURSOR.md` (old `REMlT_PARTNER_CURSOR.md` now redirects).

Signed-by: Keystone (AI) — 2026-04-16

### v25 — 2026-04-16

- Bumped `00_authority/PRINCIPLES.md` anchor note to **v35+** (explicit intent-confirmation before execution, agent-native language standard, and transferability-first methodology).
- Updated `00_authority/NORTH_STAR.md` and root `AGENTS.md` to encode the same execution contract (confirm intent → execute end-to-end → encode reusable method).

Signed-by: Keystone (AI) — 2026-04-16

### v33 — 2026-04-17

- `PARTNER_TRANSFER_INSTRUCTIONS.md` **v9**: read-order label for `PROJECT_INTENT.md`
  aligned to **upstream operator signal — agent operands**; `NORTH_STAR.md` Absolute
  line reframed as **accountability token** (agent routing), not operator leisure text.

Signed-by: Keystone (AI) — 2026-04-17

### v32 — 2026-04-17

- **Agent-primary audience (absolute):** `NORTH_STAR.md` v11, root `AGENTS.md`,
  `PRINCIPLES.md` v2 (new principle 10), `PROJECT_INTENT.md` v6, `00_authority/README.md`
  v7 — no parallel human-facing doc layer; operator material = upstream signals for
  agents; rare human audit = paths + manifest only.

Signed-by: Keystone (AI) — 2026-04-17

### v31 — 2026-04-17

- **Permissions** section: GitHub org repo creation = human operator; `.cursor/`
  policy/hook changes vs mechanical edits. **Canonical agent entry** consolidated
  to root `AGENTS.md` § first 60 seconds; `README.md`, `00_authority/README.md`,
  `NORTH_STAR.md`, `PARTNER_TRANSFER_INSTRUCTIONS.md`, `PROJECT_INTENT.md` aligned;
  `AGENTS.md` **Outcome** + human voice; `90_archive` routing line clarified vs
  “immutable” confusion.

Signed-by: Keystone (AI) — 2026-04-17

### v30 — 2026-04-17

- Added **Clean-build file budget** to `00_authority/NORTH_STAR.md` (v9): every file earns its place via agent clarity, explicit infra, or shadow/archive envelopes; inbox bulk-read barred unless routed. New `01_truth/README.md` (routing) + `90_archive/README.md` (gate); README / `02_build` / `03_shadow` stubs aligned.

Signed-by: Keystone (AI) — 2026-04-17

### v29 — 2026-04-17

- Documented **GitHub repository naming (agent-default assumption)** under `Amplified-Partners`: slug shape `YYYYMMDD-clean-build-amplified-partners` (creation date in name; commits for work history). Agents assume this before inferring from local directory names.

Signed-by: Keystone (AI) — 2026-04-17

### v28 — 2026-04-17

- **No production hooks:** `.cursor/hooks.json` is valid JSON with `"hooks": {}`. Added `.cursor/HOOKS_TESTING_NEED.md` — explicit **TESTING NEED** gate before any hook wiring. Manifest + `03_shadow/job-wrapups/README.md` describe rule+SOP-only enforcement; dormant script not treated as active.

Signed-by: Keystone (AI) — 2026-04-17

### v27 — 2026-04-17

- Clarified `PRINCIPLES.md` indexing: distinguish **document `version`** vs **`anchor_lineage`** (manifest changelog v35 series). Removed ambiguous “v35+” wording; canonical explanation is in `PRINCIPLES.md` → **Provenance and versioning**.

Signed-by: Keystone (AI) — 2026-04-17

### v26 — 2026-04-16

- Added `[NARRATIVE]` to approved status tokens (align with usage in `NORTH_STAR.md` and `PRINCIPLES.md`).
- Indexed Cursor enforcement artifacts under **Authoritative now** to match actual in-repo behavior surfaces while keeping policy authority anchored in `00_authority/`.
- Indexed root `README.md` under **Reference only** as a non-authoritative quick-start pointer.

Signed-by: Keystone (AI) — 2026-04-16

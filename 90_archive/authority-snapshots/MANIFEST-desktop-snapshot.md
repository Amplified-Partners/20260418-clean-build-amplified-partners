---
title: Governed workspace manifest (authoritative inventory)
date: 2026-04-17
version: 35
status: active
---

# How to read this

This file is the authority manifest for this governed workspace.

- Only items listed under **Authoritative now** may be treated as truth without extra confirmation.
- Items under **Candidate authority** are usable, but must be treated as `[LOGIC TO BE CONFIRMED]`.
- Items under **Reference only** are context; do not use them as foundations for decisions or code.

## GitHub repository naming (agent-default assumption)

Under organisation Amplified-Partners, a backup / clean-build Git remote uses this exact slug shape — no variants:

```
<YYYYMMDD>-clean-build-amplified-partners
```

Rules:
- YYYYMMDD = calendar date the repository was created on GitHub (not last big push).
- Literal tokens `clean-build` then `amplified-partners`, lowercase, hyphens only, in that order.
- Timeline of work = git log / commits; never encode "important day" by changing the repo slug.

Default remote URL shape (SSH): `git@github.com:Amplified-Partners/<slug>.git`

Agents treat this slug rule as canonical. The local directory name is a dev path, not the GitHub slug. Do not guess another pattern.

## Permissions (explicit)

- GitHub org Amplified-Partners: creating new repositories is a human-operator (Ewan) action unless delegated in writing. Agents do not create org repos on their own initiative.
- `.cursor/`: changing policy or adding hooks belongs under normal promotion / TESTING NEED rules. Mechanical typo fixes in hook scripts are not a substitute for turning hooks on — `"hooks": {}` stays default until the gate is satisfied.

## Status tokens (approved)

- `[LOGIC TO BE CONFIRMED]`
- `[SOURCE REQUIRED]`
- `[DECISION REQUIRED]`
- `[NON-AUTHORITATIVE]`
- `[NARRATIVE]`
- `[CURRENT BEST EVIDENCE]`

---

## Authoritative now

- `AGENTS.md`
- `00_authority/AGENTS.md`
- `00_authority/README.md`
- `00_authority/MANIFEST.md`
- `00_authority/NORTH_STAR.md`
- `00_authority/PROJECT_INTENT.md`
- `00_authority/PRINCIPLES.md`
- `00_authority/DECISION_LOG.md`
- `.cursor/rules/stateless-handover-kaizen.mdc` — mechanical enforcement of handover policy; not a separate policy spine; root AGENTS.md is the master
- `.cursor/hooks.json` — no hooks (`"hooks": {}`); see `.cursor/HOOKS_TESTING_NEED.md` for reinstatement gate

## Candidate authority (logic to be confirmed)

- `01_truth/README.md` — agent routing index: processes/ vs schemas/ vs interfaces/ vs known-issues/
- `01_truth/processes/` — generic process pack (copied from master `01_truth/processes/`; same SOPs for every exercise)
  - `01_truth/processes/AGENTS.md`
  - `01_truth/processes/2026-03_bible-consolidation_five-phase-approach_v1.md`
  - `01_truth/processes/2026-03_business-bible_three-layer-model_v1.md`
  - `01_truth/processes/2026-03_deterministic-imperative_planning-vs-execution_v1.md`
  - `01_truth/processes/2026-04_agent-md_objectivity-specialist_v1.md`
  - `01_truth/processes/2026-04_candidate-nuggets_from_dept-5-operations-methodology_v1.md`
  - `01_truth/processes/2026-04_decomposition-and-grain_v1.md`
  - `01_truth/processes/2026-04_gated-pipelines_privacy-tokenization_capability-routing_v1.md`
  - `01_truth/processes/2026-04_hygiene-role-charter_v1.md`
  - `01_truth/processes/2026-04_job-wrapup_and_escalation-note_sop_v1.md`
  - `01_truth/processes/2026-04_methodology-prospecting_five-candidates_v1.md`
  - `01_truth/processes/2026-04_methodology-scoring-rubric_v1.md`
  - `01_truth/processes/2026-04_model-format-selection_v1.md`
  - `01_truth/processes/2026-04_operating-rhythm-check-seams_v1.md`
  - `01_truth/processes/2026-04_quick-evidence-search_sop_v1.md`
  - `01_truth/processes/2026-04_research-department_charter_v1.md`
  - `01_truth/processes/2026-04_research-on-research_bootstrap-remit_v1.md`
  - `01_truth/processes/2026-04_research-operations-cadence_v1.md`
  - `01_truth/processes/2026-04_workspace-clarity-roadmap_v1.md`
- `01_truth/schemas/` — schema contracts
  - `01_truth/schemas/README.md`
- `01_truth/interfaces/` — API contracts
  - `01_truth/interfaces/README.md`
- `01_truth/known-issues/` — pre-researched component gotchas for agent use
  - `01_truth/known-issues/vapi-gotchas.md`
  - `01_truth/known-issues/twilio-whatsapp-gotchas.md`
  - `01_truth/known-issues/sqlite-macos-gotchas.md`
  - `01_truth/known-issues/deepgram-gotchas.md`
  - `01_truth/known-issues/postcodes-io-gotchas.md`
- `02_build/README.md`
- `02_build/bob-assistant/SPEC.md` — Bob's Phone Assistant full build spec
- `02_build/bob-assistant/SCHEMA.sql` — SQLite schema (5 tables)
- `02_build/bob-assistant/VAPI-CONFIG.md` — Vapi assistant JSON + Deepgram settings
- `02_build/bob-assistant/DPA.md` — plain-English Data Processing Agreement
- `03_shadow/README.md`
- `03_shadow/job-wrapups/README.md` [NON-AUTHORITATIVE] — wrap-ups location; learning only

## Reference only (sanitised; never authoritative by default)

- `.cursor/HOOKS_TESTING_NEED.md` [NON-AUTHORITATIVE] — gate checklist before any hook wiring
- `README.md` [NON-AUTHORITATIVE] — root quick-start pointer
- `90_archive/` [NON-AUTHORITATIVE]
  - `90_archive/README.md`
  - `90_archive/authority-history/` — verbatim snapshots of earlier authority versions; not current policy
  - `90_archive/context/README.md`
  - `90_archive/context/2026-04-16_operator-voice-capsule_ewan.md` [NARRATIVE] [NON-AUTHORITATIVE]

---

## Changelog

v35 — 2026-04-17
- Vendored full generic **`01_truth/processes/`** pack from master repo (18 SOPs + `AGENTS.md`); manifest index expanded so every listed path exists on disk (bibliography integrity for exercise copies).

Signed-by: Keystone (AI) — 2026-04-17

v34 — 2026-04-17
- Added `01_truth/known-issues/` directory and five component gotchas files to Candidate authority.
- Added `02_build/bob-assistant/` spec files (SPEC.md, SCHEMA.sql, VAPI-CONFIG.md, DPA.md) to Candidate authority.
- Added `00_authority/DECISION_LOG.md` to Authoritative now.
- Clarified `.cursor/rules/stateless-handover-kaizen.mdc` relationship to root AGENTS.md: root is the master policy; .mdc is mechanical enforcement.

Signed-by: Keystone (AI) — 2026-04-17

v33 — 2026-04-17
- PARTNER_TRANSFER_INSTRUCTIONS.md v9: read-order label for PROJECT_INTENT.md aligned to upstream operator signal.

Signed-by: Keystone (AI) — 2026-04-17

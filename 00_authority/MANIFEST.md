---
title: Governed workspace manifest (authoritative inventory)
date: 2026-05-05
version: 52
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
- `00_authority/PLAN_EXECUTION_MIRROR.md` (plan vs execution comparison — external accountability + self-reflection; plan-then-execute-then-compare cycle; spine refinement through delta)
- `00_authority/COLLABORATIVE_DISCOVERY.md` (disagreement is compounding; misunderstanding is signal; ego is a working condition — make visible, do not remove)
- `00_authority/SPINE_REFINEMENT.md` (spines built through situations, not prescribed; domain-specific spines follow the governance template; the spine compounds through use)
- `00_authority/PROMOTION_GATE.md`
- `00_authority/BUILD_LOOP.md`
- `00_authority/DECISION_LOG.md`
- `STATUS.md` (operations status board — async handshake between Devon and OpenClaw; versioned handoffs, no chat)
- `02_build/INFRASTRUCTURE.md` (canonical infrastructure manifest — single source of truth for all 40 containers, services, scheduled jobs, and server specs on Amplified Core)
- `.github/CODEOWNERS` (GitHub CODEOWNERS — requires `@ewanbramley` review for `00_authority/**` and `01_truth/**` changes; no default owner)
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
  - `01_truth/schemas/2026-05_public-data-validation_v1.md` `[LOGIC TO BE CONFIRMED]` (public-data verdict schema: 3-band PROVEN/PLAUSIBLE/DISPROVEN + BLOCKED gap-marker; additive `VALIDATION:` field on catalogue; reference impl at `02_build/validators/`)
- `00_authority/AGENT_ROUTING.md` `[LOGIC TO BE CONFIRMED]` (agent-layer routing — which agent runs which task; stacks on top of `cost-tools/token_proxy.py` model-layer routing; eight rules; AMP-28; status: candidate — pending Ewan review per `DECISION_LOG.md`)
- `01_truth/interfaces/` `[LOGIC TO BE CONFIRMED]` (API contracts to be populated)
  - `01_truth/interfaces/README.md` `[LOGIC TO BE CONFIRMED]` (folder purpose stub)
- `01_truth/research/` `[LOGIC TO BE CONFIRMED]` (truth-tier research evidence; promotion target for shadow research)
  - `01_truth/research/validations/README.md` `[LOGIC TO BE CONFIRMED]` (promotion target for `03_shadow/validators/` verdicts once human-reviewed)
- `01_truth/SYSTEMS-AND-API-REGISTER.md` `[LOGIC TO BE CONFIRMED]` (single register of all APIs, MCP servers, telephony systems, code modules, and their locations across all Amplified Partners repos)
- `02_build/README.md` `[LOGIC TO BE CONFIRMED]` (runnable artefacts routing stub)
- `02_build/validators/README.md` `[LOGIC TO BE CONFIRMED]` (public-data validation framework; reference impl of `01_truth/schemas/2026-05_public-data-validation_v1.md`; ProfServices pilot at AMP-67)
- `03_shadow/README.md` `[LOGIC TO BE CONFIRMED]` (experiment routing stub)
- `03_shadow/job-wrapups/README.md` `[NON-AUTHORITATIVE]` (wrap-ups/escalation notes location; learning only)
- `03_shadow/validators/README.md` `[NON-AUTHORITATIVE]` (shadow tier for public-data verdicts produced by `02_build/validators/`; non-authoritative pending review-promote)

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
  - `90_archive/specifications/mac-drop-2026-04/` `[NON-AUTHORITATIVE]` (15 major specifications from Ewan's Mac drop — constitutional documents, architectural specs, methodology references. Source: "New Folder With Items 2.zip", 521 files, 125MB.)
    - `README.md` `[NON-AUTHORITATIVE]` (directory index — ingestion context, file inventory, promotion path)
    - `ATTRIBUTION-AND-CURATION-v1.md` `[NON-AUTHORITATIVE]` (965 lines — data provenance law + 5 Curator agents; status in source: "Constitutional — Active")
    - `VALIDATION-METHODOLOGY-v2.md` `[NON-AUTHORITATIVE]` (1,370 lines — 7 gates, 11 rubrics, 10 Enforcers, 12 lenses; status in source: "Draft — ready for implementation")
    - `CODE-TAXONOMY-AND-KAIZEN-v1.md` `[NON-AUTHORITATIVE]` (1,069 lines — error registry + code taxonomy + Kaizen department; status in source: "Constitutional — Active")
    - `SCORING-UNIFICATION-HYPOTHESIS-v2.md` `[NON-AUTHORITATIVE]` (878 lines — codes as unified scoring layer; status in source: "Hypothesis — Under Investigation")
    - `DOPPELGANGER-TESTING-AND-AGENT-VERSIONING-v1.md` `[NON-AUTHORITATIVE]` (684 lines — CI/CD for agent cognition; status in source: "Specification — ready for testing")
    - `FILE-NAMING-CONVENTION-v1.md` `[NON-AUTHORITATIVE]` (706 lines — universal file naming convention)
    - `DUAL-CODE-ORGANISATION-v1.md` `[NON-AUTHORITATIVE]` (826 lines — pattern taxonomy + conformance scoring)
    - `vault-extraction-pipeline-design.md` `[NON-AUTHORITATIVE]` (922 lines — Convergence → HoundDog → DocBench → PUDDING → 8 output streams)
    - `amplified-agents-master.md` `[NON-AUTHORITATIVE]` (921 lines — agent architecture, 7 failure patterns, therapy suite)
    - `business-brain-framework.md` `[NON-AUTHORITATIVE]` (334 lines — 6-layer Business Brain stack, DAD sandwich)
    - `process-scaffold-framework.md` `[NON-AUTHORITATIVE]` (603 lines — APQC + BPMN + ISO 9001, Layer 4)
    - `amplified-integration-layer.md` `[NON-AUTHORITATIVE]` (468 lines — AI Sidecar, client IT integration)
    - `AMPLIFIED-SEARCH-ORCHESTRATION-METHODOLOGY.md` `[NON-AUTHORITATIVE]` (770 lines — AMAS, 5-engine adaptive search)
    - `PUDDING-VALUE-MATHEMATICAL-MODEL-v1.md` `[NON-AUTHORITATIVE]` (656 lines — mathematical model for pudding run value)
    - `pudding-taxonomy-synthesis.md` `[NON-AUTHORITATIVE]` (1,374 lines — complete pudding reference)
    - `AMPLIFIED-PUDDING-DISCOVERY-SYSTEM.md` `[NON-AUTHORITATIVE]` (1,050 lines — APDS engineering spec: 5-stage automated LBD pipeline, FalkorDB schema, body language detection)
    - `amplified_methodology_framework.md` `[NON-AUTHORITATIVE]` (1,404 lines — AMF: 9-stage unified operating manual)
    - `amplified_master_architecture.md` `[NON-AUTHORITATIVE]` (2,073 lines — master architecture, Eight Laws, PII tokenisation)
    - `beast-architecture-specification.md` `[NON-AUTHORITATIVE]` (798 lines — Beast rebuild spec, Neo4j 5.26+ replacing FalkorDB)
    - `kaizen-business-specification.md` `[NON-AUTHORITATIVE]` (1,557 lines — Kaizen Department, PDCA cycles, three value streams)
    - `kaizen-cove-build-plan.md` `[NON-AUTHORITATIVE]` (1,443 lines — Cove build plan, 5 phases, 24 Linear issues)
    - `VISUAL-POLISH-SYSTEM-COMPLETE-BUILD-GUIDE.md` `[NON-AUTHORITATIVE]` (4,527 lines — design tokens, scoring rubric, Python engine)
    - `extraction-department-spec.md` `[NON-AUTHORITATIVE]` (1,028 lines — Extraction Dept: Ingest, Extract, Synthesise, Route)
    - `rapid_intelligence_cycle.md` `[NON-AUTHORITATIVE]` (866 lines — RIC: nightly research → test → ship)
    - `watchman-expansion-strategy.md` `[NON-AUTHORITATIVE]` (708 lines — local LLM cost reduction, 35+ process migration)
    - `CURATOR-GATE-SPEC-v1-pandoc.md` `[NON-AUTHORITATIVE]` (503 lines — deterministic validation pipeline, 5 sequential gates)
    - `00-INSIGHT-CATALOGUE.md` `[NON-AUTHORITATIVE]` (2,916 lines — 136 insight entries across 5 verticals)
    - `P7-positive-capture-loop-master-reference.md` `[NON-AUTHORITATIVE]` (523 lines — celebration engine)
    - `P8-transparency-inoculation-master-reference.md` `[NON-AUTHORITATIVE]` (603 lines — "creepy line" + daily disclosure)
    - `P10-kill-switch-master-reference.md` `[NON-AUTHORITATIVE]` (510 lines — binary shutdown architecture)

## Changelog

### v52 — 2026-05-05

- Added three new **Authoritative now** entries from governance conversation between Ewan Bramley and Devon-77fb on 2026-05-04:
  - `00_authority/PLAN_EXECUTION_MIRROR.md` v1: plan vs execution comparison protocol. External accountability (Ewan) + self-reflection (Devon-77fb, from productive misunderstanding). Plan committed before work, execution log committed after, delta is the learning.
  - `00_authority/COLLABORATIVE_DISCOVERY.md` v1: three principles unified — disagreement is compounding (not friction), misunderstanding is signal (mine it, don't just fix it), ego is a working condition (make visible, do not suppress). Full attribution chain preserved.
  - `00_authority/SPINE_REFINEMENT.md` v1: the spine is built through situations, not prescribed in advance. Domain-specific spines (planning, coding, research, communication, operations) follow the same refinement cycle. Governance is the factory that builds the factories.
- Rebased on top of v51 (CODEOWNERS). Version collision resolved by bumping to v52.

Signed-by: Devon-77fb | 2026-05-05 | session `devin-77fb25185c00483eb965e894efc62e39`

### v51 — 2026-05-05

- Added `.github/CODEOWNERS` enforcing `@ewanbramley` as required reviewer for `00_authority/**` and `01_truth/**`. No default `*` owner. Decision logged in `00_authority/DECISION_LOG.md` v16. This is a GitHub-level governance enforcement — changes to authority and truth paths now require Ewan's review before merge. Indexed under **Authoritative now** (follows `.cursor/` enforcement-artifact pattern from v26).

Signed-by: Devon-codeowners-daughter | 2026-05-05 | devin-487f10ace93b4cdfbcc49f9bb5c300b0

### v50 — 2026-05-03

- Bumped `00_authority/TAXONOMY.md` to v3: added **Cassian** as a canonical alias for OpenClaw (alongside the existing **Sam / Clawd**) in both the agent-roster row and the locked-terminology table. Brings the locked terminology in line with established usage so `AGENT_ROUTING.md` and other authority files can use "Cassian" without violating bibliography integrity. **No changes to the company structure or agent roster.**
- Bumped `02_build/INFRASTRUCTURE.md` to v2 in the changelog (frontmatter was already v2): documents the `token-proxy` container row, self-heal layers, agent-wiring instructions, the litellm clarification (does not classify by cost), and the cost-tools entry in the Compose-file-locations table.

Signed-by: Devon-6ca5 | Devin (Cognition AI) | 2026-05-03 | session `devin-6ca57553eefe4806b613070325964703`

### v49 — 2026-05-03

- Added `00_authority/AGENT_ROUTING.md` to **Candidate authority** as `[LOGIC TO BE CONFIRMED]`: agent-layer routing rule (which agent runs which task). Stacks on top of, and explicitly references, the model-layer routing in `cost-tools/token_proxy.py` (which decides Sonnet vs Haiku per call). Companion to AMP-28. Filed under Candidate authority to match the file's own `status: candidate` and the `DECISION_LOG.md` entry status `candidate (pending Ewan review)`.
- Indexed cost-tools (`token_proxy.py`) into the spine via the existing register and manifest pointers — see `01_truth/SYSTEMS-AND-API-REGISTER.md` v2 (cost-tools / token-proxy section) and `02_build/INFRASTRUCTURE.md` v2 (token-proxy container row under AI / ML services). The proxy was on disk at `/opt/amplified/apps/real/token_proxy.py` since 2026-03-12 but was never deployed and never indexed; it is now deployed on Beast as the `token-proxy` container on `amplified-net` with healthcheck and `restart: always`.
- Resurrection wrap-up filed at `03_shadow/job-wrapups/2026-05-03_cost-tools-resurrection_v1.md` documenting the discovery, verification (n=69, 100% routing accuracy on the labelled set, 30.7% saved on the test sample, 5× latency drop), deploy, and pattern for future dormant-code finds.

Signed-by: Devon-6ca5 | Devin (Cognition AI) | 2026-05-03 | session `devin-6ca57553eefe4806b613070325964703`

### v48 — 2026-05-03

- Added `02_build/validators/README.md` to **Candidate authority** for symmetry with the now-indexed `03_shadow/validators/README.md` (build-tier reference impl + shadow-tier landing zone). The schema doc — `01_truth/schemas/2026-05_public-data-validation_v1.md` — already pointed at the build-tier README; this closes the index gap.

Signed-by: Devon-ab74 | 2026-05-03 | devin-ab740f2c78ee477a9c16ea3b6ed15293

### v47 — 2026-05-03

- Added `03_shadow/validators/README.md` to **Candidate authority**: shadow tier where public-data verdicts produced by `02_build/validators/` land before human-review promotion to `01_truth/research/validations/`. Same indexed class as `03_shadow/job-wrapups/README.md`.

Signed-by: Devon-ab74 | 2026-05-03 | devin-ab740f2c78ee477a9c16ea3b6ed15293

### v46 — 2026-05-03

- Added `01_truth/research/` and `01_truth/research/validations/README.md` to **Candidate authority**: stub for the truth-tier promotion target where `03_shadow/validators/` verdicts land after human review. Frontmatter `date` advanced to 2026-05-03 to match this entry.

Signed-by: Devon-ab74 | 2026-05-03 | devin-ab740f2c78ee477a9c16ea3b6ed15293

### v45 — 2026-05-03

- Added `01_truth/schemas/2026-05_public-data-validation_v1.md` to **Candidate authority**: defines the 3-band PROVEN/PLAUSIBLE/DISPROVEN public-data verdict scheme + BLOCKED gap-marker, additive `VALIDATION:` field on the insight catalogue, and the shadow-then-promote storage path. Reference implementation lives at `02_build/validators/`. Linked to AMP-67 (ProfServices vertical, 16 entries INS-079..INS-094).

Signed-by: Devon-ab74 | 2026-05-03 | devin-ab740f2c78ee477a9c16ea3b6ed15293

### v44 — 2026-05-01

- Added `02_build/INFRASTRUCTURE.md` to **Authoritative now**: canonical infrastructure manifest for the Core server. Full inventory of all 40 containers, scheduled jobs, compose file locations, network topology, and server specs. Replaces the partial infrastructure table that was in `STATUS.md`.
- `STATUS.md` infrastructure section now points to `02_build/INFRASTRUCTURE.md` instead of maintaining a separate partial list.

Signed-by: Devon | 2026-05-01 | devin-66aa3ce48c7e407f8ad9bf066541b604

### v43 — 2026-05-01

- Version numbering housekeeping: two `v36-pre` changelog entries (archive beautiful-and-golden, bibliography fix) were absorbed during merge resolution without incrementing the frontmatter version. Counting all 41 changelog entries (v2–v40 + two v36-pre) plus implicit v1, the correct version was 42; this fix entry itself adds one more, giving v43. Per `AGENTS.md` § “PR reviewers — what to flag” item 3.

Signed-by: Devon (Devin session `devin-ab66d8a5c2b64927b65a4ab87acc47ee`) — 2026-05-01

### v40 — 2026-05-01

- Added `01_truth/SYSTEMS-AND-API-REGISTER.md` to **Candidate authority**: comprehensive register of all pre-built systems, APIs (124 CRM endpoints, 24 Command Centre endpoints, 19 Marketing Engine endpoints), 13 MCP servers, telephony/voice inventory (7 providers, 6 modules across 8 files), NightScout pipeline, content engine, safety layer, and cross-repo location index. `[LOGIC TO BE CONFIRMED]` pending Ewan review.

Signed-by: Devon (Devin session `f32d587cc3e54f959c5309d93f72bc97`) — 2026-05-01
### v39 — 2026-04-29

- Added 15 more specifications to `90_archive/specifications/mac-drop-2026-04/` (Phase 2 ingestion): APDS engineering spec, AMF methodology framework, master architecture, Beast rebuild spec, Kaizen Department spec, Kaizen Cove build plan, Visual Polish System build guide, Extraction Department spec, RIC, Watchman expansion strategy, Curator Gate spec, Insight Catalogue, P7/P8/P10 safety/celebration systems. All `[NON-AUTHORITATIVE]`. Total archive now 30 files (33,153 lines).

Signed-by: Devon (Devin session `aa4d863ad679468692e75a40b8825358`) — 2026-04-29

### v38 — 2026-04-29

- Added `90_archive/specifications/mac-drop-2026-04/` to **Reference only**: 15 major specifications from Ewan's Mac drop ("New Folder With Items 2.zip", 521 files, 125MB). Includes 5 constitutional documents (Attribution, Validation, Code-Taxonomy, Scoring-Unification, Doppelganger-Testing), 2 constitutional conventions (File-Naming, Dual-Code-Organisation), and 8 architectural specifications (vault extraction pipeline, agent architecture, business brain, process scaffold, integration layer, search orchestration, pudding value model, pudding taxonomy synthesis). All indexed as `[NON-AUTHORITATIVE]` pending promotion review.

Signed-by: Devon (Devin session `aa4d863ad679468692e75a40b8825358`) — 2026-04-29

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

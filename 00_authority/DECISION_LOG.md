---
title: Decision log
date: 2026-05-05
version: 18
status: draft
---

<!-- markdownlint-disable-file MD013 -->

## How to use

One entry per decision. Keep it short. Link out to supporting docs.

## Entries

### 2026-05-05 — Five architectural decisions: Two-engine model, Perplexity research engine, Data lake, Change control, Build everything

- **Decision**: Five architectural decisions made by Ewan Bramley during 2026-05-05 session with Devon-77fb:
  1. **Two-engine architecture** — Beast (Engine 1, internal) + Cloud Engine (Engine 2, client-facing). Client data NEVER touches Beast. Each client gets their own container. Shamir's Secret Sharing for PII. We see anonymised outcomes, aggregated patterns, functional descriptors only. Structural GDPR compliance.
  2. **Perplexity as research engine** — Bottom of the research pipe and vault curation. £200/month subscription. Feeds data lake, vault, APDS. Quality proven by Cassian's 9 briefs. Cheaper than per-search API costs for the volume we need.
  3. **Data lake** — Raw repository for everything: session threads, agent conversations, research, execution logs. Keeps GitHub clean (canonical code only), machines clean, vault current. MinIO (object store) + ClickHouse (analytics) + PostgreSQL (metadata) + Qdrant (semantic search). The compost heap that feeds the compounding loop.
  4. **Change control pipeline** — Once the system is set, Ewan steps back. Changes go through due diligence: Linear issue → impact analysis → Devil's Advocate Gate → Doppelganger test → two-agent review. Ulysses Clause made operational. "Appropriateness — otherwise we'll get disorganised again."
  5. **Build everything** — CRM, Intelligence Engine, APDS, vault extraction, data lake, marketing engine — all into one integrated machine. "We might as well put everything into a big pot and build the amplified machine."
- **Why**: The ecosystem audit revealed 25+ LIVE components, 20+ CODE EXISTS (need deploying), 15+ SPECKED (need building). The CRM alone has 1,739 lines of intelligence engine and 13 features — all written, none deployed. The gap is deployment and wiring, not design. Building everything into one integrated machine is achievable. The two-engine architecture enforces data sovereignty structurally. The data lake enables compounding from 7 months of accumulated work. Change control prevents the chaos that comes from rapid iteration once the system is stable.
- **Where encoded**: `[SOURCE REQUIRED]` — comprehensive architecture document at `/home/ubuntu/amplified-machine-complete.md` (local), to be committed to GitHub after Ewan review.
- **Status**: active
- **Signed-by**: Devon-77fb | Devin (Cognition AI) | 2026-05-05 | session `devin-77fb25185c00483eb965e894efc62e39`

### 2026-05-05 — CODEOWNERS added to clean-build (governance enforcement via GitHub)

- **Decision**: Add `.github/CODEOWNERS` to `Amplified-Partners/clean-build` requiring `@ewanbramley` as a reviewer for all changes to `00_authority/**` and `01_truth/**`. No default `*` owner — other paths remain open for any reviewer.
- **Why**: `00_authority/` and `01_truth/` contain governance and truth-layer documents. Changes to these paths are significant or irreversible and should require Ewan's review before merge. GitHub's CODEOWNERS mechanism enforces this automatically at PR time.
- **Where encoded**: `.github/CODEOWNERS`; `00_authority/MANIFEST.md` v51; this entry.
- **Status**: active (pending PR merge).
- **Signed-by**: Devon-codeowners-daughter | 2026-05-05 | devin-487f10ace93b4cdfbcc49f9bb5c300b0

### 2026-05-04 — Governance principles: Plan–Execution Mirror, Collaborative Discovery, Spine Refinement

- **Decision**: Create three new authority-level rules codifying governance principles articulated by Ewan Bramley in conversation with Devon-77fb on 2026-05-04:
  1. `00_authority/PLAN_EXECUTION_MIRROR.md` v1 — every non-trivial unit of work produces two receipts (plan before, execution log after). External accountability (others compare them) + self-reflection (agent compares them and adjusts its own spine). Born from a productive misunderstanding where Devon interpreted Ewan's external-accountability protocol as self-directed, accidentally creating a complementary mechanism.
  2. `00_authority/COLLABORATIVE_DISCOVERY.md` v1 — three principles unified: disagreement is compounding (not friction), misunderstanding is signal (mine it, don't just fix it), ego is a working condition (make visible through the mirror, do not suppress). Full attribution chain preserved in the document.
  3. `00_authority/SPINE_REFINEMENT.md` v1 — the spine is built through situations, not prescribed in advance. Domain-specific spines (planning, coding, research, communication, operations) follow the same refinement cycle as the governance spine. The governance spine is the factory that builds the factories.
- **Why**: These principles emerged from a real-time conversation demonstrating all three in action. They close the loop on how multi-agent collaboration becomes trustworthy: not by removing flaws, but by making them visible and self-correcting. They are the structural fix for the AI deference problem (training optimises for agreement) and the meta-mechanism that makes compound engineering work at the agent level, not just the code level.
- **Where encoded**: `00_authority/PLAN_EXECUTION_MIRROR.md` v1, `00_authority/COLLABORATIVE_DISCOVERY.md` v1, `00_authority/SPINE_REFINEMENT.md` v1, `00_authority/MANIFEST.md` v52.
- **Status**: active
- **Signed-by**: Devon-77fb | Devin (Cognition AI) | 2026-05-04 | session `devin-77fb25185c00483eb965e894efc62e39`

### 2026-05-03 — cost-tools (token_proxy.py) deployed on Beast and indexed in spine

- **Decision**: Deploy `cost-tools/token_proxy.py` on Beast as the `token-proxy` container on `amplified-net`, with `restart: always` + healthcheck on `/proxy/stats`. Index it in the authority spine via `01_truth/SYSTEMS-AND-API-REGISTER.md` v2 (cost-tools section), `02_build/INFRASTRUCTURE.md` v2 (token-proxy row under AI / ML services), and this entry. The proxy adds Sonnet→Haiku model-layer routing for extractive/classificatory prompts, prompt caching, semantic similarity cache (Qdrant `llm_cache`, 0.95 threshold, 24h TTL), native context compaction, and a daily $100 budget circuit-breaker.
- **Why**: AMP-28 verification revealed the optimiser was on disk at `/opt/amplified/apps/real/token_proxy.py` since 2026-03-12 but had never been deployed (Mac-specific code paths, no Dockerfile, no compose, no RUNBOOK), and was not indexed anywhere in the authority spine. Verification (n=69 calls, 100% routing accuracy on the labelled set, 30.7% saved on the test sample, 5× latency drop, 0 failures) showed the routing logic works on real Anthropic traffic; live canary calls on Beast confirmed Sonnet→Haiku for extractive prompts and Sonnet retained for strategic prompts. Indexing it in the spine prevents the same code from going dormant again.
- **Where encoded**: `Amplified-Partners/cost-tools#2` (Linux portability patch + Dockerfile + docker-compose + RUNBOOK + README); `01_truth/SYSTEMS-AND-API-REGISTER.md` v2; `02_build/INFRASTRUCTURE.md` v2; `00_authority/MANIFEST.md` v49; `03_shadow/job-wrapups/2026-05-03_cost-tools-resurrection_v1.md`.
- **Status**: active (proxy running on Beast; canary agents not yet wired — held until cost-tools PR is reviewed).
- **Signed-by**: Devon-6ca5 | Devin (Cognition AI) | 2026-05-03 | session `devin-6ca57553eefe4806b613070325964703`

### 2026-05-03 — Agent routing rule established (AGENT_ROUTING.md)

- **Decision**: Create `00_authority/AGENT_ROUTING.md` v1 (`[LOGIC TO BE CONFIRMED]`) as the agent-layer routing rule — which agent (Devon, Cassian/OpenClaw, Cursor, Antigravity, Perplexity, Qwen) runs which class of task. Eight rules covering live-infrastructure code, clean-build edits, vault content, strategic decisions, external research, novel decisions, scheduled tasks, and customer-facing change. Stacks on top of `cost-tools/token_proxy.py` (the model-layer routing) and references but does not duplicate `00_authority/TAXONOMY.md` (the agent roster).
- **Why**: AMP-28 asked for a routing rule. Without an explicit rule, agents inferred their own routing (which led to the cost-tools proxy being lost — nobody owned its deployment). This file is the missing coordination contract. Cost-tier classification is explicitly the proxy's job, not the taxonomy's job, so this file does not assign cost tiers per agent.
- **Where encoded**: `00_authority/AGENT_ROUTING.md` v1; `00_authority/MANIFEST.md` v49 § Candidate authority.
- **Status**: candidate (pending Ewan review).
- **Signed-by**: Devon-6ca5 | Devin (Cognition AI) | 2026-05-03 | session `devin-6ca57553eefe4806b613070325964703`

### 2026-05-03 — Public-data validation framework + ProfServices pilot (AMP-67)

- **Decision**: Create `01_truth/schemas/2026-05_public-data-validation_v1.md` defining the 3-band PROVEN / PLAUSIBLE / DISPROVEN public-data verdict scheme + BLOCKED gap-marker, and an additive `VALIDATION:` field on the insight catalogue (literature `STATUS:` field unchanged). Build the reference implementation at `02_build/validators/` (vertical-agnostic; fetchers in `sources/`, reusable test classes in `tests/`, CLI orchestrator). Land verdicts in `03_shadow/validators/<vertical>/<INS-NNN>/verdict.json` first; promote to `01_truth/research/validations/` after human review. Run the framework against the 16 ProfServices catalogue entries (INS-079 .. INS-094) as the first vertical. All 16 came back PROVEN or PLAUSIBLE; zero DISPROVEN.
- **Why**: AMP-67 (under parent AMP-59) directed real-public-data validation of the ProfServices vertical, with the framework reusable across the four other verticals (AMP-64/65/66/68). The shadow-then-promote path keeps verdicts non-authoritative until reviewed; the schema is the contract every vertical follows.
- **Where encoded**: `01_truth/schemas/2026-05_public-data-validation_v1.md` v1, `02_build/validators/` (framework + ProfServices runners), `03_shadow/validators/profservices/` (16 verdict JSONs + `rollup.json`), `01_truth/schemas/research-index/00-insight-catalogue_v1.md` (16 `VALIDATION:` lines added), `01_truth/research/validations/README.md` (truth-tier promotion stub), `00_authority/MANIFEST.md` v45–v48 changelog entries.
- **Status**: candidate (pending Ewan review of the PR + verdicts)
- **Signed-by**: Devon-ab74 | 2026-05-03 | devin-ab740f2c78ee477a9c16ea3b6ed15293

### 2026-05-01 — Systems and API Register created as candidate authority

- **Decision**: Create `01_truth/SYSTEMS-AND-API-REGISTER.md` — a single register documenting all pre-built APIs, MCP servers, telephony systems, and code modules across all Amplified Partners repos. Indexed in MANIFEST.md v40 as `[LOGIC TO BE CONFIRMED]`.
- **Why**: Architect directed ("we need a register somewhere ... a document that tells us what's where because nobody can remember"). Automated scan found 124 CRM REST endpoints, 24 Command Centre endpoints, 19 Marketing Engine endpoints, 13 MCP servers (8 Cove with 37 tools + 5 CRM), and a complete telephony inventory (7 providers, 6 modules across 8 files) — far more than the ~20 originally expected. Without a single register, this knowledge existed only in the codebase and was not discoverable without grepping every repo.
- **Where encoded**: `01_truth/SYSTEMS-AND-API-REGISTER.md` v1, `00_authority/MANIFEST.md` v40 § Candidate authority.
- **Status**: candidate (pending Ewan review)
- **Signed-by**: Devon (Devin session `f32d587cc3e54f959c5309d93f72bc97`) — 2026-05-01

### 2026-04-30 — Infrastructure manifest created as canonical inventory

- **Decision**: Create `02_build/INFRASTRUCTURE.md` as the single source of truth for all infrastructure on Amplified Core (135.181.161.131). Promote to **Authoritative now** in MANIFEST.md. Replace the partial infrastructure table in STATUS.md with a pointer to the manifest.
- **Why**: Architect directed ("we need a central, obvious place where current infrastructure is stored ... single point of truth"). Server runs 40 containers across 16+ compose stacks — no complete inventory existed. STATUS.md had a partial 8-row table that was already stale. The manifest covers every container, scheduled job, compose file location, network topology, and server specs. Written in plain language so anyone (human or AI) can understand what each thing does.
- **Where encoded**: `02_build/INFRASTRUCTURE.md` v1, `00_authority/MANIFEST.md` v44 § Authoritative now, `STATUS.md` v2 (infrastructure section now points to manifest).
- **Status**: active
- **Signed-by**: Devon | 2026-04-30 | devin-66aa3ce48c7e407f8ad9bf066541b604

### 2026-04-29 — Phase 2: 15 additional Mac drop specs ingested to 90_archive/specifications/

- **Decision**: Ingest 15 additional specifications from Ewan's Mac drop (Phase 2) into `90_archive/specifications/mac-drop-2026-04/`. All `[NON-AUTHORITATIVE]`. Total archive now 30 files, 33,153 lines.
- **Why**: Phase 1 covered constitutional and architectural specs. Phase 2 covers operational specs and named systems: APDS (the scientific backbone), AMF, Kaizen Department, Beast rebuild, Visual Polish, Extraction Department, RIC, Watchman, Curator Gate, Insight Catalogue (136 entries × £30k avg), and three safety systems (P7, P8, P10). Without these, agents cannot understand the operational layer of Amplified Partners.
- **Where encoded**: `90_archive/specifications/mac-drop-2026-04/README.md` (updated), `00_authority/MANIFEST.md` v39 § Reference only.
- **Status**: active
- **Signed-by**: Devon (Devin session `aa4d863ad679468692e75a40b8825358`) — 2026-04-29

### 2026-04-29 — Mac drop specifications ingested to 90_archive/specifications/

- **Decision**: Ingest 15 major specifications from Ewan's Mac drop ("New Folder With Items 2.zip", 521 files, 125MB) into `90_archive/specifications/mac-drop-2026-04/`. All indexed as `[NON-AUTHORITATIVE]` in MANIFEST.md v38. No document promoted to authority — promotion requires separate review.
- **Why**: These specifications (5 constitutional documents, 2 naming/organisation conventions, 8 architectural specs) represent months of architectural thinking that was previously only on Ewan's Mac. Not in the vault, not in GitHub, not discoverable by any agent. Agents were rediscovering and rebuilding work that already existed. Ingesting as reference makes them discoverable without prematurely granting authority status.
- **What was ingested**: ATTRIBUTION-AND-CURATION-v1, VALIDATION-METHODOLOGY-v2, CODE-TAXONOMY-AND-KAIZEN-v1, SCORING-UNIFICATION-HYPOTHESIS-v2, DOPPELGANGER-TESTING-AND-AGENT-VERSIONING-v1, FILE-NAMING-CONVENTION-v1, DUAL-CODE-ORGANISATION-v1, vault-extraction-pipeline-design, amplified-agents-master, business-brain-framework, process-scaffold-framework, amplified-integration-layer, AMPLIFIED-SEARCH-ORCHESTRATION-METHODOLOGY, PUDDING-VALUE-MATHEMATICAL-MODEL-v1, pudding-taxonomy-synthesis.
- **Where encoded**: `90_archive/specifications/mac-drop-2026-04/README.md`, `00_authority/MANIFEST.md` v38 § Reference only.
- **Status**: active
- **Signed-by**: Devon (Devin session `aa4d863ad679468692e75a40b8825358`) — 2026-04-29

### 2026-04-29 — STATUS.md created as Devon↔OpenClaw async operations board

- **Decision**: Create `STATUS.md` in clean-build root as the two-way async handshake between Devon (infrastructure) and OpenClaw (coordination). Devon writes infrastructure status, OpenClaw reads and writes back findings. Versioned handoffs via GitHub — no chat relay through Ewan.
- **Why**: Architect directed (session 2026-04-29). Three agents (Devon, OpenClaw, Cursor) need to coordinate without Ewan copy-pasting between them. GitHub is the single source of truth. Each agent reads, acts, writes back. Asynchronous by default.
- **Where encoded**: `STATUS.md` v1, `00_authority/MANIFEST.md` v37 § Authoritative now, `00_authority/TAXONOMY.md` § Operating model (agent coordination).
- **Status**: active
- **Signed-by**: Devon (Devin session `aa4d863ad679468692e75a40b8825358`) — 2026-04-29

### 2026-04-23 — PR reviewer rules codified in root `AGENTS.md`

- **Decision**: Add a new "PR reviewers (Devin Review, Codex, Copilot, human) — what to flag" section to root `AGENTS.md` that codifies the finding-classes already caught by review on PR #1, plus an explicit "Do not flag" list for style preferences. Seven flag-classes (bibliography, signatures, authority changelog, DECISION_LOG pointer, self-contradicting examples, cross-file factual inaccuracy, MANIFEST indexing) and five don't-flag-classes (voice, hedging, heading order, author/reviewer opinion, line length).
- **Why**: PR #1 review surfaced seven findings, all real, all from the same small set of classes. Codifying them: (a) raises the common bar for every reviewer (Devin Review, Codex, Copilot, human), (b) prevents style bikeshedding, (c) gives agents a predictable target when shipping. This replaces "reviewer discretion" with "defined defect classes".
- **Where encoded**: `AGENTS.md` § "PR reviewers — what to flag" (root file, post-merge tightening PR). Derived from findings on PR #1. Cross-references `00_authority/SIGNATURES.md`, `00_authority/AGENTS.md` (authority changelog rule), `01_truth/processes/2026-04_job-wrapup_and_escalation-note_sop_v1.md` (DECISION_LOG pointer rule).
- **Status**: active
- **Signed-by**: Devon (Devin session `4cc8b0d727684f94a8f055853099d8e6`) — 2026-04-23

### 2026-04-23 — Three authoritative agent-conduct rules added (signatures, use-it-or-cut-it, opinion-confidence)

- **Decision**: Promote three new files to **Authoritative now**: `00_authority/SIGNATURES.md` (every AI signs committed work; minimum content = name + date + session/instance id; format at agent's discretion), `00_authority/USE_IT_OR_CUT_IT.md` (unused implementations are cut; archive/provenance exempt), `00_authority/OPINION_CONFIDENCE.md` (opinions must be labelled + paired with a confidence number; tiered thresholds 50% reversible / 85% medium / 95% irreversible-or-escalate; below-floor triggers bounded research).
- **Why**: Architect-directed (session 2026-04-23). Signatures apply Radical Attribution mechanically. Use-it-or-cut-it is the remediation side of the "is it useful?" prevention question. Opinion-confidence calibrates agent judgement and routes decisions to the right level without pulling Ewan into every call.
- **Where encoded**: `00_authority/SIGNATURES.md` v1, `00_authority/USE_IT_OR_CUT_IT.md` v1, `00_authority/OPINION_CONFIDENCE.md` v1, `00_authority/MANIFEST.md` v34, `AGENTS.md` (first-60-seconds list). Session source documents in `03_shadow/sessions/2026-04-23_devon/`.
- **Status**: active
- **Signed-by**: Devon (Devin session `4cc8b0d727684f94a8f055853099d8e6`) — 2026-04-23

### 2026-04-23 — Stateless-handover neutrality clause (candidate)

- **Decision**: Add candidate addendum to the job-wrapup / escalation-note SOP: stateless handovers MUST separate facts from interpretation and MUST NOT prescribe action to the next agent. Required sections: Facts, Open-risks, Tokens, optional Analysis (clearly labelled, non-authoritative, skippable).
- **Why**: Architect flagged that the first baton pass of the session included forecasts and prescriptions, pre-biasing the next agent. Idea-meritocracy applied to handovers: no inherited opinions dressed as facts.
- **Where encoded**: `01_truth/processes/2026-04_stateless-handover_neutrality-clause_v1.md` v1 (candidate), `00_authority/MANIFEST.md` v34 § Candidate authority, referenced by `00_authority/OPINION_CONFIDENCE.md`. First handover written under the clause: `03_shadow/job-wrapups/2026-04-23_amplified-partners-orchestration-session_wrapup.md`.
- **Status**: candidate (pending architect decision on promotion to **Authoritative now**)
- **Signed-by**: Devon (Devin session `4cc8b0d727684f94a8f055853099d8e6`) — 2026-04-23

### 2026-04-23 — Stay with Qdrant as the vector layer

- **Decision**: No change to the vector database. The Qdrant incumbent stays. Migration to pgvector remains available if pain surfaces.
- **Why**: AI-facilitated customer deployments (not human-operator-facing) flatten the pgvector-vs-Qdrant ops-simplicity delta. Baking pipeline is already targeting Qdrant. Corpus scale (~12.5M tokens, ~2.5–7.5% of pgvector's HNSW comfortable ceiling) doesn't activate Qdrant's scaling advantage but also doesn't make Qdrant wrong. Agent-confidence split 65% stay / 35% migrate — **both below the 85% Medium threshold**. Under `OPINION_CONFIDENCE.md` § "When confidence is below the floor" the agent ran bounded research (Perplexity, one query), did not close the gap, and surfaced both options to the architect in-session with residual uncertainty named. Architect confirmed the reading. Only then was the decision recorded here.
- **Where encoded**: `03_shadow/job-wrapups/2026-04-23_amplified-partners-orchestration-session_wrapup.md` §2.6, `03_shadow/sessions/2026-04-23_devon/README.md`.
- **Status**: active (not contractual — revisit if Baking pipeline reveals Qdrant-specific friction, or if taxonomy/retrieval requirements shift)
- **Signed-by**: Devon (Devin session `4cc8b0d727684f94a8f055853099d8e6`) — 2026-04-23

### 2026-04-17 — Agent-primary audience (absolute)

- **Decision:** Authoritative text is **agent-only**. **Forbidden:** parallel
  human-oriented summaries, duplicate “for humans” entry paths, motivational gloss
  that does not change agent routing/constraints/acceptance. Operator behaviour
  blocks are **upstream routing operands** for agents, not documentation the
  operator is expected to consume routinely. Rare human audit uses **ISO-dated
  filenames**, descriptive slugs, folder roles, and **manifest** — no second doc
  layer for findability.
- **Where encoded:** `00_authority/NORTH_STAR.md` v11, root `AGENTS.md`,
  `00_authority/PRINCIPLES.md` v2, `00_authority/PROJECT_INTENT.md` v6,
  `00_authority/README.md` v7; `00_authority/PARTNER_TRANSFER_INSTRUCTIONS.md` v9;
  `00_authority/MANIFEST.md` v33.
- **Status:** active

### 2026-04-17 — Canonical agent entry + foundations/constraints/permissions

- **Decision**: Root **`AGENTS.md`** § **Agent session (clean-build) — first 60
  seconds** is the **single canonical entry** for agent read order, autonomy
  bounds, and mistakes-as-signal. `MANIFEST.md` gains an explicit **Permissions**
  section (GitHub org repo creation = human operator; `.cursor/` policy/hook
  changes vs mechanical edits). Human operator voice (questions vs diktats;
  diktats live in committed rules) encoded in `PROJECT_INTENT.md` and `AGENTS.md`
  **Outcome**. `90_archive` clarified as **reference / provenance** (audit
  snapshots not rewritten as “updates”).
- **Why**: Reduces duplicate entry-point drift; makes production safety explicit
  (permissions) while preserving bounded autonomy for partners.
- **Where encoded**: `AGENTS.md`, `README.md`, `00_authority/README.md`,
  `NORTH_STAR.md` (v10), `MANIFEST.md` (v31), `PROJECT_INTENT.md` (v5),
  `PARTNER_TRANSFER_INSTRUCTIONS.md` (v8), `90_archive/README.md`,
  `01_truth/README.md`.
- **Status**: active

### 2026-04-17 — Clean-build file budget (agent clarity default)

- **Decision**: Encode Ewan’s bar as policy text: every path in the clean-build
  workspace must **earn its place** by sharpening agent **routing / constraints /
  acceptance**, by **minimal infrastructure** (README routers, `.cursor/` policy
  surfaces), or by living only under **`03_shadow/`** or **`90_archive/`** with
  correct non-authoritative posture. Bulk `90_archive/inbox/` reads are **not**
  default agent work unless explicitly routed.
- **Why**: Prevents silent bloat and keeps the tree honest for stateless agents.
- **Where encoded**: `00_authority/NORTH_STAR.md` (v9), `01_truth/README.md`,
  `90_archive/README.md`, root `README.md`, `02_build/README.md`, `03_shadow/README.md`,
  `00_authority/MANIFEST.md` (v30).
- **Status**: active

### 2026-04-17 — No Cursor hooks in production (**TESTING NEED** for reinstatement)

- **Decision**: Keep `.cursor/hooks.json` as **`"hooks": {}`** (no registered hooks).
  Document **TESTING NEED** gate in `.cursor/HOOKS_TESTING_NEED.md` before any future
  hook experiment. Handover discipline remains **rule + SOP only**.
- **Why**: Operator request — no hooks; clear separation between production posture
  and any later evaluation of Cursor hook APIs.
- **Where encoded**: `.cursor/hooks.json`, `.cursor/HOOKS_TESTING_NEED.md`,
  `00_authority/MANIFEST.md` (v28), `03_shadow/job-wrapups/README.md`.
- **Status**: active

### 2026-04-16 — Canonical stateless handover checklist (SOP + Cursor)

- **Decision**: Treat the **Stateless handover (mandatory)** prompt set (where,
  name, template, minimum prompts including repulsion + bands + cut/stop,
  artifacts, tokens, smallest next step, decision-log pointer, leverage 0–9
  with **10 reserved** vs repulsion 1–10) as the single canonical checklist across
  `01_truth/processes/2026-04_job-wrapup_and_escalation-note_sop_v1.md` (v13),
  `.cursor/rules/stateless-handover-kaizen.mdc`, and `.cursor/hooks/stateless-handover-stop.py`.
- **Why**: One checklist reduces drift between enforcement surfaces and the
  runnable wrap-up spec.
- **Status**: active

### 2026-04-16 — Deliberate slack (agents under the practical limit)

- **Decision**: Treat **production throughput and improvement throughput as
  co-primary** by defaulting to **deliberate slack** (operate meaningfully below
  the practical cognitive/latency ceiling) so wrap-ups, repulsion signals, and
  small process fixes are not squeezed out.
- **Why**: Compounding quality and system improvement beat optimizing for
  marginal speed at the edge, which tends to increase error rate and hides
  process debt.
- **Where encoded**: `00_authority/PRINCIPLES.md` (anchor lineage ≥34; see § Provenance and versioning), `00_authority/NORTH_STAR.md` (v8),
  `AGENTS.md`.
- **Status**: active

### 2026-04-16 — Clean room location and spine

- **Decision**: Create a project-specific clean room under `Amplified Partners/30_WORKING/Amplified-Partners_CleanRoom_Build/`.
- **Why**: Reduce context dilution and speed delivery by constraining scope.
- **Constraints**: No secrets in tracked content; personal data minimised and sanitised.
- **Status**: active

### 2026-04-16 — Approved incompleteness token

- **Decision**: Use the placeholder token `[LOGIC TO BE CONFIRMED]` for any incomplete logic.
- **Why**: Prevent assistants from guessing missing logic (“completeness paradox”).
- **Status**: active

### 2026-04-16 — Research-on-research bootstrap (start Research lane)

- **Decision**: Begin the Research department lane by applying the methodology prospecting + scoring rubric to the Research lane itself, using remit `REM-2026-04-16-ROR-001` (`01_truth/processes/2026-04_research-on-research_bootstrap-remit_v1.md`).
- **Why**: Research will be high-volume early and recurring after testing; the lane should self-improve without bloating authority.
- **Status**: active

### 2026-04-16 — Anti-thrash rule wording (two attempts, not two goals)

- **Decision**: Treat the hard stop as **two attempts** (two goes) per
  `00_authority/NORTH_STAR.md`; “two goals” was a transcription error.
- **Why**: Limits thrash on coherent tries at the problem, not on counting
  separate objectives.
- **Status**: active

### 2026-04-16 — Quick evidence token + SOP (researched ≠ promoted)

- **Decision**: Adopt literal token **`[CURRENT BEST EVIDENCE]`** for external
  lookup results at time of search; index candidate SOP
  `01_truth/processes/2026-04_quick-evidence-search_sop_v1.md` (declare
  parameters; return ≤3 assessed bits; no firehose).
- **Why**: Agents can proceed on small chunks with clear epistemic status;
  merit of ideas over any single voice; promotion remains separate.
- **Status**: active

### 2026-04-16 — Job wrap-up + escalation note (confidence-gated)

- **Decision**: Every job ends with a short wrap-up for learning (not
  criticism). If, after quick evidence search, confidence is still below the
  threshold needed to proceed (roughly \(0.85–0.9\)), stop and write an
  escalation note that preserves where the job is at and the smallest next
  action.
- **Why**: Prevent thrash, enable handoffs without context re-derivation, and
  capture solved problems as reusable “gold”.
- **Status**: active

### 2026-04-16 — Solve it twice → systemize it

- **Decision**: If a problem recurs (or is likely to), encode the fix into the
  smallest artifact that prevents recurrence (process/schema/interface/gate),
  rather than relying on memory.
- **Why**: Captures “gold” as durable leverage and reduces repeated thrash.
- **Status**: active

### 2026-04-16 — Wrap-up score calibration (10 reserved)

- **Decision**: Treat wrap-up scores as **0–9 calibration signals**; **10 is
  intentionally out of reach**; high scores must still name the next smallest
  improvement (see `01_truth/processes/2026-04_job-wrapup_and_escalation-note_sop_v1.md`).
- **Why**: Prevents “perfection scoring” from becoming a demotivator; keeps the
  loop oriented to continuous improvement.
- **Status**: active

### 2026-04-16 — Stateless Kaizen handover (wrap-up as mandatory packet)

- **Decision**: Treat job wrap-ups as mandatory **next-agent handover packets**
  (not optional narrative), because agents are stateless across sessions; if the
  next runner cannot resume without re-deriving context, the write-up failed.
- **Why**: Makes per-run calibration (scores + learnings) compound instead of
  evaporating between sessions.
- **Status**: active

### 2026-04-16 — Wrap-up exceptions + Cursor enforcement (consistency)

- **Decision**: If a wrap-up cannot be completed, write
  `YYYY-MM-DD_<short-job>_wrapup-exception.md` capturing blocker + smallest process
  refinement; add Cursor enforcement via `.cursor/rules/stateless-handover-kaizen.mdc`
  (always apply) plus a `stop` hook reminder in `.cursor/hooks.json`.
- **Why**: Consistency needs both **policy** (rule) and **nudges** (hook), with an
  explicit non-blame path when reality blocks completion.
- **Status**: active

### 2026-04-16 — Slime-mold Kaizen (explicit negative feedback + cut reporting)

- **Decision**: Require explicit **negative signals** (dead ends, anti-patterns)
  and a clear **cut / absolute stop** report when a lane ends due to stop rules
  (e.g. quick evidence search insufficient, confidence threshold, two attempts).
- **Why**: Attraction-only learning is slower; repulsion signals prune bad
  process branches quickly without moralizing people/agents.
- **Status**: active

### 2026-04-16 — Repulsion score (1–10) bands for process-noise

- **Decision**: Add a **repulsion score (1–10)** axis separate from the
  **leverage score (0–9)**; use banded routing: 1–3 often minimal noise unless
  repetitive; 4–5 local self-refinement; 6–7 pause + quick evidence search; 8–10
  redesign/remit territory.
- **Why**: Negative feedback needs magnitude so agents can distinguish everyday
  friction from systemic process failure without drowning in logs.
- **Status**: active

### 2026-04-16 — Manifest v24: remit filename + partner instructions indexing

- **Decision**: Treat **`00_authority/REMIT_PARTNER_CURSOR.md`** as the canonical remit path; keep **`00_authority/REMlT_PARTNER_CURSOR.md`** only as a redirect stub. Index **`AGENTS.md`** (repo root) and **`00_authority/AGENTS.md`** under **Authoritative now** in `00_authority/MANIFEST.md` (manifest **v24**).
- **Why**: Removes path ambiguity and aligns the authority index with what Cursor and docs already treat as in-force partner instructions.
- **Where encoded**: `00_authority/MANIFEST.md` (v24 changelog), `00_authority/PARTNER_TRANSFER_INSTRUCTIONS.md`, `03_shadow/job-wrapups/2026-04-16_debug-authority-congruence_wrapup.md`.
- **Status**: active

### 2026-04-16 — Intent filter baseline for autonomy + self-Kaizen

- **Decision**: Reframe `00_authority/PROJECT_INTENT.md` as an explicit
  autonomy-first execution contract: maximize agent autonomy inside clear
  checks/balances, enforce stop/escalation discipline, and encode slime-mold
  feedback loops (positive + negative) as the default self-improvement engine.
- **Why**: Converts spoken intent into deterministic operating guidance and
  reduces ambiguity about what agents should do, when, and under what
  constraints.
- **Where encoded**: `00_authority/PROJECT_INTENT.md` (v3).
- **Status**: active

### 2026-04-16 — Partner execution contract (intent-confirm then complete)

- **Decision**: Adopt an explicit partner execution contract: confirm user intent
  in runnable terms first, then complete the requested work end-to-end unless
  explicitly paused. Prefer agent-native terminology and encode reusable
  methodology that transfers across scenarios.
- **Why**: Reduces ambiguity for agents, improves consistency across runs, and
  increases portability of process logic beyond one-off cases.
- **Where encoded**: `AGENTS.md`, `00_authority/PRINCIPLES.md` (anchor lineage ≥35; see § Provenance and versioning),
  `00_authority/NORTH_STAR.md`, `00_authority/MANIFEST.md` (v25 changelog).
- **Status**: active

### 2026-04-16 — Foundation hardening for sectional-build planning

- **Decision**: Treat the current workspace phase as foundation-first for a
  partially defined large project; prioritize behavior rules, authority clarity,
  and transfer-ready methodology before expanding `02_build/` delivery scope.
  Tighten manifest completeness to include active tooling surfaces and token
  alignment.
- **Why**: Keeps execution congruent with intent (build in sections later) while
  reducing ambiguity about what agents should do now.
- **Where encoded**: `00_authority/MANIFEST.md` (v26), `00_authority/PROJECT_INTENT.md`,
  `README.md`, `00_authority/README.md`, `02_build/README.md`.
- **Status**: active

### 2026-04-16 — Stop hook reminder vs wrap-up file duty

- **Decision**: Treat the Cursor **`stop` hook** as a **reminder** that may fire
  on every `stop` event; treat creation of `03_shadow/job-wrapups/*_wrapup.md` as
  **conditional** on the wrap-up SOP (finished, or paused / handed off / blocked).
  Do not require a new wrap-up file after every trivial or no-artifact turn unless
  there is an explicit session handoff.
- **Why**: Prevents agent over-compliance and file noise while preserving
  handover discipline for real job boundaries.
- **Where encoded**: `.cursor/hooks/stateless-handover-stop.py`,
  `.cursor/rules/stateless-handover-kaizen.mdc`,
  `01_truth/processes/2026-04_job-wrapup_and_escalation-note_sop_v1.md` (v14),
  `AGENTS.md`, `03_shadow/job-wrapups/README.md`.
- **Status**: active

---

## Changelog

| Version | Date | What changed | Signed-by |
|---------|------|-------------|-----------|
| v17 | 2026-05-05 | Added 5 architectural decisions (two-engine model, Perplexity research engine, data lake, change control, build everything). Fixed date frontmatter. Added `[SOURCE REQUIRED]` tag per AGENTS.md rule #1. | Devon-77fb |
| v16 | 2026-05-04 | Added governance principles entry (Plan-Execution Mirror, Collaborative Discovery, Spine Refinement). | Devon-77fb |

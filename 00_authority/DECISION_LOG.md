---
title: Decision log
date: 2026-04-29
version: 9
status: draft
---

<!-- markdownlint-disable-file MD013 -->

## How to use

One entry per decision. Keep it short. Link out to supporting docs.

## Entries

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

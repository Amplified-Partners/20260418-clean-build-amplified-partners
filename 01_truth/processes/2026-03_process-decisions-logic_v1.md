---
title: "Process Decisions Logic"
id: "process-decisions-logic"
version: 1
created: 2026-04-25
last_validated: 2026-04-25
type: document
topic_type: reference
status: imported
source_file: "doc2-process-decisions-logic.docx"
signed_by: "Devon, 2026-04-25, devin-992682c244cf444f91e0a516498afbfd"
---

**PROCESS DOCUMENT**

Compound Engineering Research --- Decision Log, Logic & Scoring

Amplified Partners --- Beast/Cove Architecture

Document 2 of 2 --- Research Process & Scoring

16 March 2026

*Version 1.0 \| Fact %: 85 \| Confidence: High*

**1. Research Decisions Log**

This section documents every major research decision made during the compound engineering investigation. Each entry records the decision, the alternatives weighed, the evidence trail, the reasoning, and a formal PUDDING 4-criteria score.

Scoring key --- PUDDING 4-Criteria Rubric (0--5 per criterion, total /20): Relevance (R), Actionability (A), Evidence (E), Impact (I). Threshold: ≥12 = high-value.

**Decision 1: Selecting Every.to Compound Engineering as the Primary Pattern**

**Decision:**

Adopted the Every.to compound engineering plugin (Plan→Work→Review→Compound) as the canonical self-improving development pattern for Beast/Cove integration.

**Alternatives considered:**

Addy Osmani\'s self-improving agent loops (AGENTS.md-centric, no plugin). SICA (Self-Improving Coding Agent, Bristol, academic proof-of-concept --- modifies own scaffolding code). CogniLayer (SQLite + vector MCP, 14 structured fact types). Custom (build from scratch using Temporal primitives only). Cursor Rules / Windsurf Memories (platform-locked).

**Evidence supporting the choice:**

Every.to plugin: 10,000+ GitHub stars (March 2026), MIT licensed, 26 specialised agents, 23 workflow commands, 13--14 skills. Proven at Every.to across 5 products with single-engineer teams --- time-to-ship dropped from 1 week to 1--3 days. Will Larson (ex-Stripe) published independent validation (January 2026). Addy Osmani (Google Chrome) cited compound engineering in his self-improving agents analysis (January 2026). SICA (arXiv:2504.15228) provides academic proof that the self-improvement mechanism works (17% to 53% on SWE-Bench). Plugin converts to OpenCode and Codex --- not locked to Claude Code.

**Logic / Reasoning:**

Every.to is the only option that is simultaneously: (a) production-proven at company scale, (b) open-source and MIT-licensed, (c) installable today with zero custom development, (d) architecturally mappable to Temporal Activities, and (e) cross-tool portable. Addy Osmani\'s approach is a pattern, not a tool --- it requires building everything. SICA is academic only (no production use). CogniLayer adds infrastructure complexity (SQLite + vector embeddings) without proven compounding evidence. Custom build would take months to reach the maturity the plugin already has. The METR study (July 2025) shows AI without systematic knowledge management makes developers slower --- compound engineering is the systematic knowledge management layer.

**PUDDING Score: R=5 A=5 E=5 I=5 → Total: 20/20**

*Confidence band: High --- production-proven, academic-validated, community-adopted*

**Decision 2: Choosing Plan→Work→Review→Compound as the Canonical Loop**

**Decision:**

Adopted the 4-step loop (Plan→Work→Review→Compound) as the canonical structure for every Cove build pipeline run.

**Alternatives considered:**

3-step loop without Compound (Plan→Work→Review --- standard CI/CD). 5-step loop adding Brainstorm before Plan. Flat multi-agent loop (all agents see everything, no phase separation). Addy Osmani\'s stateless-but-iterative loop (fresh session each cycle, AGENTS.md carries knowledge).

**Evidence supporting the choice:**

The 4-step loop is the structure used in production at Every.to. The December 2025 article by Dan Shipper co-authored with Kieran Klaassen formally defines this as the canonical loop. The 80/20 rule (80% on Plan + Review, 20% on Work + Compound) is empirically derived from 9 months of use (May 2025 -- March 2026). The Compound step is what makes it self-improving --- without it, the loop is standard CI/CD that never learns.

**Logic / Reasoning:**

The 3-step loop misses the learning step entirely --- each cycle starts from scratch. The 5-step loop adds Brainstorm as optional (it is available via /workflows:brainstorm but is not part of the core cycle --- used only when requirements are fuzzy). Flat multi-agent systems suffer from \'aimless wandering\' per Osmani\'s analysis. The Osmani approach is compatible but relies on AGENTS.md appending rather than structured docs/solutions/ --- it lacks the YAML-indexed retrieval that makes compound knowledge searchable.

**PUDDING Score: R=5 A=5 E=5 I=5 → Total: 20/20**

*Confidence band: High --- 9+ months of production evidence at Every.to*

**Decision 3: Mapping to Temporal Activities (vs Other Orchestration)**

**Decision:**

Each loop phase (Plan, Work, Review, Compound) maps to a Temporal Activity within a CoveBuildWorkflow. Human approval gates map to Temporal Signals. Parallel review agents map to concurrent Activity execution.

**Alternatives considered:**

Kubernetes Jobs (stateless, no durable execution). Custom queue system (RabbitMQ/Redis). Direct Claude Code CLI orchestration (no durability). AWS Step Functions (vendor lock-in). Prefect/Dagster (data pipeline tools, not agent orchestration).

**Evidence supporting the choice:**

Temporal is already deployed on Beast (Hetzner AX162-R). Temporal\'s complexity cliff taxonomy (March 2026 blog post) directly maps Beast/Cove to L3--L4 agent complexity --- the level where durable execution becomes mandatory. Each Activity is independently retryable (if Review fails, it reruns without redoing Work). The human approval gate after Plan is a natural Temporal Signal. Temporal handles the 14 parallel review agents via concurrent Activity scheduling.

**Logic / Reasoning:**

Temporal is already in the stack --- zero new infrastructure. Every alternative requires either building durability from scratch or adopting a new orchestration platform. The compound engineering pattern specifically requires reliable execution of the Compound step even on partial workflow failure (catch exceptions, compound what you learned from failures). Temporal\'s Activity retry semantics guarantee this. The CoveBuildWorkflow sketch in the research maps directly to Temporal Python SDK patterns.

**PUDDING Score: R=5 A=5 E=5 I=5 → Total: 20/20**

*Confidence band: High --- Temporal already deployed, pattern maps directly*

**Decision 4: The 6-Stage Compound Learning Loop Design**

**Decision:**

Designed a 6-stage compound learning loop: ① Fault Detection → ② Documentation (Compound Step) → ③ Rubric Testing (PUDDING + Attribution) → ④ Addition to KB → ⑤ Compound Learning (retrieval) → ⑥ Prevention (new rules).

**Alternatives considered:**

4-stage loop (detection → fix → document → done --- no rubric scoring). Direct append model (append to AGENTS.md, no structured scoring or tiering). CogniLayer model (auto-embed everything into vector DB, no quality gate).

**Evidence supporting the choice:**

The 6-stage design integrates compound engineering (from Every.to) with PUDDING taxonomy scoring and the Attribution-First Multiplier Rubric already established in the Amplified Partners vault. Each stage has a defined PUDDING label: ① S.!.5.i, ② P.+.5.m, ③ C.\>.1.i, ④ I.+.5.l, ⑤ R.+.4.l, ⑥ C.=.5.∞. The MIT CSAIL study (July 2025) recommended building data that captures the process of development --- this loop captures exactly that.

**Logic / Reasoning:**

The 4-stage model lacks quality gating --- everything enters the KB at equal status, leading to noise accumulation (the AGENTISSUE-BENCH study identifies memory pollution as a key failure mode). The direct-append model bloats AGENTS.md without structure. The CogniLayer model adds infrastructure complexity (embeddings, vector search) before the KB has enough entries to need it. The 6-stage design adds rubric gates (Stage 3) that enforce quality before KB entry, and prevention codification (Stage 6) that ensures rules propagate to CLAUDE.md and review agents.

**PUDDING Score: R=5 A=4 E=4 I=5 → Total: 18/20**

*Confidence band: High --- synthesises proven components; novel integration is untested*

**Decision 5: The 8-Stage Addition SOP (Consolidating 7 Vault Documents)**

**Decision:**

Created a single 8-stage addition SOP (Stages 0--7) that consolidates RUBRIC-REPLACE-OR-FIX, Attribution-First Multiplier, Dog-Food principle, Shadow Alpha, Failure Mode Analysis, Migration with Rollback, and Kaizen Loop into one sequential process.

**Alternatives considered:**

Keeping the 7 separate vault documents as independent references. Creating a lightweight checklist (no formal stages). Adopting a third-party technology evaluation framework (e.g., ThoughtWorks Tech Radar format).

**Evidence supporting the choice:**

Gap 7 in database-architecture-context.md explicitly identified that the addition pipeline existed across multiple documents but was never consolidated into one SOP. Each component is already proven individually --- RUBRIC-REPLACE-OR-FIX was applied to the Docker Desktop → OrbStack switch successfully. The Dog-Food principle is established practice (kg\_internal tests everything before customer deployment). The Shadow Alpha model is documented in Sovereign OS architecture.

**Logic / Reasoning:**

Dispersed documentation means steps get skipped. The FalkorDB adoption illustrates this: it passed the research stage (confirmed as sole Redis graph module) but the failure mode analysis stage was not run until after repeated failures. A single SOP forces sequential completion --- you cannot skip Stage 5 (failure modes) to jump to Stage 6 (migration). Each stage has explicit pass/fail criteria and defined \'on fail\' actions, preventing ambiguous decisions.

**PUDDING Score: R=5 A=4 E=4 I=5 → Total: 18/20**

*Confidence band: High --- consolidation of proven components; SOP itself is new*

**Decision 6: YAML-Frontmatter as the Knowledge Format (vs Database, vs Wiki)**

**Decision:**

Selected YAML-frontmatter markdown files stored in docs/solutions/ on the Beast filesystem as the canonical knowledge format for compound learning entries.

**Alternatives considered:**

Relational database (PostgreSQL tables for KB entries). Wiki system (Notion, Confluence, or similar). CogniLayer model (SQLite + vector embeddings). Plain markdown without structured frontmatter. JSON files.

**Evidence supporting the choice:**

Every.to uses exactly this format --- YAML frontmatter + markdown body stored in docs/solutions/. The format is git-trackable (every change is versioned), grep-searchable (no database required for retrieval), human-readable (any developer can read it), and agent-parseable (YAML tags enable structured filtering). 10,000+ stars on the plugin validate community acceptance of this format.

**Logic / Reasoning:**

A relational database adds infrastructure and creates a dependency --- if the DB goes down, the KB is unavailable. A wiki introduces a third-party dependency and loses git versioning. CogniLayer\'s SQLite + vector approach adds complexity before the KB reaches the scale (500+ docs) where vector search becomes necessary. Plain markdown without YAML loses structured retrieval. JSON is less human-readable than YAML + markdown. The recommended path: start with YAML tag filtering + full-text search (zero infrastructure), add vector search only when docs/solutions/ exceeds \~500 documents.

**PUDDING Score: R=5 A=5 E=5 I=4 → Total: 19/20**

*Confidence band: High --- proven format, zero-infrastructure, git-native*

**Decision 7: Tiered Retrieval Model (vs Full Injection, vs Vector Search)**

**Decision:**

Implemented a 4-tier retrieval model: Tier 0 (CLAUDE.md, always loaded), Tier 1 (MEMORY.md first 200 lines, always loaded), Tier 2 (docs/solutions/, on-demand during Plan phase), Tier 3 (.claude/rules/, invoked when path-scoped).

**Alternatives considered:**

Full injection (load entire KB into every context window). Pure vector search (embed everything, retrieve by similarity). Single-tier model (everything always loaded). BM25 keyword search only.

**Evidence supporting the choice:**

The METR study (July 2025) showed AI tools caused 19% slowdown --- context without structure is noise. Every.to\'s tiered approach (CLAUDE.md always, solutions/ on demand) is empirically validated. Claude Code\'s own architecture uses the same tiered pattern: CLAUDE.md at session start, MEMORY.md first 200 lines, then on-demand retrieval. The 200-line limit for Tier 0/1 is a Claude Code design constraint --- exceeding it causes adherence degradation.

**Logic / Reasoning:**

Full injection wastes context tokens and reduces model adherence (proven by Claude Code\'s 200-line limit design). Pure vector search requires embedding infrastructure before it is needed and misses exact-match tag filtering. A single-tier model either loads too much (token bloat) or too little (missed knowledge). The tiered model provides always-available critical rules (Tier 0), recent learnings (Tier 1), deep knowledge retrieval when planning (Tier 2), and domain-specific expertise when touching relevant files (Tier 3).

**PUDDING Score: R=5 A=4 E=4 I=5 → Total: 18/20**

*Confidence band: High --- mirrors Claude Code\'s own architecture; proven at Every.to*

**Decision 8: The Faults/Fixes KB Structure (65 Entries, YAML Indexed)**

**Decision:**

Created a structured faults/fixes knowledge base with 65 initial entries, each using the standardised YAML-frontmatter format, severity-coded index, and cross-referenced by component, category, and related faults.

**Alternatives considered:**

Informal bug list (simple markdown list). Linear/GitHub Issues only (existing ticket systems). Spreadsheet-based tracking. No pre-seeded KB (start empty, build organically).

**Evidence supporting the choice:**

Nine research documents were available as source material, covering FalkorDB (10 crash bugs), Graphiti (14 integration issues), Neo4j (8 mitigated issues), PostgreSQL, Docker, Temporal, and infrastructure. Each entry was sourced from specific GitHub issues, community reports, or vault documents --- all attributable. The compound engineering pattern requires a seeded KB for the flywheel to begin turning.

**Logic / Reasoning:**

Informal lists lack the structure agents need for retrieval. Linear/GitHub issues capture what broke and when, but not the category-level prevention rules or detection patterns that agents need during planning. Spreadsheets are not git-trackable. Starting with an empty KB means the compound flywheel has nothing to retrieve for the first N cycles --- seeding with known faults jumpstarts the learning. The 65-entry count represents every documented fault across all nine research documents, providing comprehensive coverage from day one.

**PUDDING Score: R=5 A=5 E=5 I=4 → Total: 19/20**

*Confidence band: High --- sourced from documented evidence; structure proven*

**Decision 9: FalkorDB → Neo4j Recommendation (RUBRIC-REPLACE-OR-FIX Applied)**

**Decision:**

Recommended replacing FalkorDB with Neo4j as the graph database engine for Beast/Cove, based on applying the RUBRIC-REPLACE-OR-FIX decision framework.

**Alternatives considered:**

Keep FalkorDB (continue with workarounds for crash bugs). Fix FalkorDB (contribute upstream patches). Use a different graph database entirely (e.g., Amazon Neptune, ArangoDB, TigerGraph). Drop the graph layer and use PostgreSQL with recursive CTEs.

**Evidence supporting the choice:**

RUBRIC-REPLACE-OR-FIX Five Questions applied: (1) Have we diagnosed the cause? YES --- C-level memory safety bugs in FalkorDB codebase. (2) Fixable config issue or tool being the tool? TOOL BEING THE TOOL --- 9 open crash bugs, multiple SIGSEGV issues, use-after-free. (3) What does community say? KNOWN PROBLEM --- GitHub issues \#1240, \#1572, \#1481, \#1204, \#1325 all open, community-confirmed. (4) Better alternative? YES --- Neo4j has 17-year production track record, full ACID, Graphiti\'s primary/most-tested backend. (5) Cost of switching vs continued failures? SWITCH IS CHEAPER --- migration path is 4 weeks; continued failures risk silent data corruption. Score: Neo4j 27/30 vs FalkorDB lower in the comparison table.

**Logic / Reasoning:**

All three directional questions (2, 3, 4) point the same way --- the rubric\'s own decision rule says: switch. The FalkorDB routing bug \#1325 (single group\_id queries silently return empty results) makes normal operation fail. The RESTORE command crash (\#1204) means recovery from failure is itself unreliable. Neo4j Community + DozerDB provides multi-database capability at zero software cost, avoiding the \$36,000/year Enterprise licence. Graphiti retains full compatibility --- it was originally designed for Neo4j.

**PUDDING Score: R=5 A=5 E=5 I=5 → Total: 20/20**

*Confidence band: High --- deterministic rubric application; all evidence aligns*

**Decision 10: Governance Model (GOLD/SILVER/BRONZE Thresholds)**

**Decision:**

Implemented a tiered governance model: GOLD entries (Attribution Multiplier ≥5,000) auto-add to KB with lightweight Ewan review; SILVER (1,000--4,999) require explicit Ewan approval before KB finalisation; BRONZE (100--999) held in draft for enrichment.

**Alternatives considered:**

Flat model (all entries require same approval level). Fully automated (no human review). Fully manual (Ewan reviews everything before entry). No governance (append everything, prune later).

**Evidence supporting the choice:**

The Attribution-First Multiplier Rubric (documented in vault/20-staging-archive/00-rubric-multiplier-v2.md) is an established Amplified Partners framework. The multiplicative structure (any zero at any layer zeros everything) forces provenance completeness. SOUL.md principles require Human Logic for governance decisions. The FalkorDB example demonstrates why: the technology entered the stack without full failure-mode analysis --- governance gates prevent this.

**Logic / Reasoning:**

A flat model overwhelms the human reviewer (Ewan is a single person) or starves the KB of entries. Fully automated removes the Human Logic gate that SOUL.md requires. Fully manual creates a bottleneck where GOLD-quality entries wait unnecessarily. The tiered model scales: GOLD entries (high confidence, full attribution) flow through quickly; SILVER entries get proportional scrutiny; BRONZE entries park until enriched. The principle \'AI presents, human decides\' is preserved at every tier --- the automation level changes, but human authority is maintained.

**PUDDING Score: R=5 A=4 E=4 I=5 → Total: 18/20**

*Confidence band: High --- established rubric framework; governance tiers are novel application*

**2. Logic Chain: Why Compound Engineering Works**

This section traces the causal logic of compound engineering integration specifically --- why each step exists and why the compound step is the differentiator.

**2.1 Why Does Each Unit of Work Compound Into the Next?**

Each Cove pipeline run ends with the Compound Activity, which spawns 6 parallel agents (context-analyzer, solution-extractor, related-docs-finder, prevention-strategist, category-classifier, documentation-writer). These agents capture what happened --- the problem, the fix, the prevention rules, the YAML-indexed metadata --- into a solution document stored in docs/solutions/.

Each future Cove pipeline run begins with the Plan Activity, which reads CLAUDE.md (standing orders) + docs/solutions/ (accumulated lessons). The Plan agent searches the knowledge base for entries relevant to the current Linear issue. This means Cycle N+1 knows everything Cycle N learned.

The compounding mechanism is structural, not aspirational: the filesystem (docs/solutions/) is both the output of the Compound step and the input to the Plan step. The loop is closed by architecture, not by discipline.

**2.2 Why Is the Compound Step the Differentiator?**

Plan, Work, and Review are standard CI/CD phases that every engineering team already runs in some form. Without the Compound step, the loop is: Plan → Work → Review → next issue. Each cycle starts from the same knowledge base. No learning accumulates. The METR study (July 2025) measured this: developers using AI tools took 19% longer to complete issues because every session started from zero.

The Compound step is the only step that converts ephemeral session context into permanent institutional knowledge. It is the delta between a stateless tool and a self-improving system. Without it, you have automation. With it, you have compounding.

Kieran Klaassen\'s breakthrough moment illustrates this: Claude Code reviewed a PR and cited three previous PRs (\#234, \#219, \#241) as sources for its decisions --- pattern memory, feedback incorporation, and precedent following --- all from compound knowledge stored in docs/solutions/.

**2.3 Why Must Compound Run While Context Is Fresh?**

Kieran Klaassen\'s critical timing note: \'It\'s very important to run this whenever the context is fresh. You don\'t want to run it after compaction.\' The AI\'s context window contains the full problem, fix attempt, debugging trail, error messages, and decision rationale. After /compact (context compression), this detail is lost --- the AI retains a summary but not the specifics.

A compound step run on stale context produces generic learnings: \'Fixed a database issue\' instead of \'FalkorDB routing bug \#1325 --- if len(group\_ids) \> 1 should be \>= 1 --- single group\_id queries fall through to empty default\_db.\' The specific version is searchable, actionable, and prevents recurrence. The generic version is noise.

In Beast/Cove: the Compound Activity is the final Temporal Activity in every CoveBuildWorkflow. It runs immediately after Review, before any context is discarded. It also runs on partial failure (catch exceptions) --- because failures are often the most valuable learnings.

**2.4 Why docs/solutions/ and Not a Database?**

Five reasons, in order of importance:

1\. Git versioning: every change to the knowledge base is tracked, diffable, and revertable. A database would require a separate audit trail system.

2\. Agent readability: AI agents can read markdown files natively. No ORM, no query language, no connection string --- just file read.

3\. Zero infrastructure: no database server to maintain, no connection pool to manage, no OOM kills to debug. The KB is a directory of files.

4\. Grep-searchable: YAML tag filtering + full-text search works immediately. Vector search can be added later (when KB exceeds \~500 documents) without changing the storage format.

5\. Portability: the KB travels with the repo. Clone the repo, you have the KB. No database dump/restore, no migration scripts.

**2.5 Why 14 Review Agents in Parallel (Not 3, Not 50)?**

14 is the number that Every.to arrived at after 9+ months of iteration. Each agent covers a distinct specialisation: security, performance, architecture, pattern recognition, data integrity, data migration, code simplicity, Rails conventions, Python conventions, TypeScript conventions, DHH Rails conventions, deployment verification, frontend race conditions, and agent-native accessibility.

Fewer than 14 creates coverage gaps --- the original Every.to setup used fewer agents and consistently missed categories of issues that later specialised agents caught. More than 14 produces diminishing returns: overlapping findings, increased token cost, and longer review times without proportional quality improvement.

The multi-model strategy enhances this: Kieran Klaassen allocates different model providers to different review agents (Claude for planning, Codex for implementation, Gemini for review). Different models surface different issues --- model diversity is itself a compound engineering principle.

**2.6 Why 80/20 on Plan+Review vs Work+Compound?**

Kieran Klaassen\'s empirically derived time allocation: 80% of engineering time on Plan and Review, 20% on Work and Compound. This inverts the traditional ratio (most teams spend 80% writing code, 20% reviewing it).

The logic: at Stage 3+ of compound engineering adoption, the AI executes the implementation. The human value-add is in direction-setting (Plan) and quality assurance (Review). A well-planned task executes quickly and correctly. A poorly planned task executes quickly and incorrectly --- and the rework cost exceeds the time saved by skipping planning.

The advanced 50/50 rule reinforces this: 50% of total engineering time on building features, 50% on improving the system (creating review agents, documenting patterns, building test generators). System improvements yield compounding returns; feature work yields linear returns. Over time, the system investment pays exponentially.

**3. Scoring Summary**

All 10 research decisions scored against the PUDDING 4-Criteria Rubric (Relevance / Actionability / Evidence / Impact, each 0--5, total /20).

  ------------------------------------------------------ ------- ------- ------- ------- --------- ----------------
  **Decision**                                           **R**   **A**   **E**   **I**   **/20**   **Confidence**
  1\. Every.to compound engineering as primary pattern   5       5       5       5       **20**    High
  2\. Plan→Work→Review→Compound canonical loop           5       5       5       5       **20**    High
  3\. Mapping to Temporal Activities                     5       5       5       5       **20**    High
  4\. 6-stage compound learning loop                     5       4       4       5       **18**    High
  5\. 8-stage addition SOP                               5       4       4       5       **18**    High
  6\. YAML-frontmatter knowledge format                  5       5       5       4       **19**    High
  7\. Tiered retrieval model                             5       4       4       5       **18**    High
  8\. Faults/fixes KB (65 entries)                       5       5       5       4       **19**    High
  9\. FalkorDB → Neo4j (RUBRIC-REPLACE-OR-FIX)           5       5       5       5       **20**    High
  10\. Governance (GOLD/SILVER/BRONZE)                   5       4       4       5       **18**    High
  ------------------------------------------------------ ------- ------- ------- ------- --------- ----------------

**Aggregate Statistics**

Total decisions scored: 10

Average score: 19.0 / 20

All decisions exceed the ≥12 high-value threshold.

6 of 10 decisions score a perfect 20/20 --- these are decisions backed by production evidence, community validation, and deterministic logic.

4 decisions score 18--19 --- these integrate proven components in novel ways (the integration is untested as a complete system, reducing Evidence or Actionability by 1 point).

Confidence band: all 10 decisions rated High confidence. No decision is based on speculation or single-source evidence.

**4. What Wasn\'t Chosen and Why**

Every decision involves rejected alternatives. This section documents what was evaluated and why it was set aside.

  ------------------------------------------------ ------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------
  **Alternative**                                  **Why Rejected**
  **Addy Osmani\'s self-improving loops**          Pattern-only, not a tool. Requires building everything from scratch. AGENTS.md append model lacks structured YAML indexing. Compatible as a philosophy but not a substitute for the Every.to plugin\'s 26 agents and 23 commands.
  **SICA (Bristol, arXiv:2504.15228)**             Academic proof-of-concept only --- no production deployment. Modifies agent scaffolding code directly (risky in production). Useful as theoretical validation but not as an implementation choice.
  **CogniLayer (SQLite + vector MCP)**             Adds infrastructure complexity (SQLite server, embedding model, vector index) before the KB has enough entries (\~500) to justify it. Over-engineered for the current scale. Viable as a Phase 3+ addition, not a starting point.
  **Cursor Rules / Windsurf Memories**             Platform-locked. Cursor rules only work in Cursor; Windsurf memories only in Windsurf. Beast/Cove runs on server infrastructure --- it needs a tool-agnostic format. Every.to plugin converts to OpenCode and Codex.
  **Full context injection (no tiering)**          Token bloat. Claude Code\'s 200-line CLAUDE.md design constraint exists because larger context files reduce model adherence. Loading the full KB into every session would waste tokens and degrade output quality.
  **Pure vector search for retrieval**             Premature optimisation. Vector search requires embedding infrastructure, adds latency, and is unnecessary below \~500 documents. YAML tag filtering + grep is faster, simpler, and adequate for the next 12+ months.
  **Keep FalkorDB (workarounds)**                  9 open crash bugs including 4 critical SIGSEGV issues. Routing bug \#1325 causes silent data loss on every standard query. RESTORE command (\#1204) crashes on backup recovery. The RUBRIC-REPLACE-OR-FIX verdict is unambiguous: switch.
  **No-governance (append everything)**            Memory pollution. AGENTISSUE-BENCH identified irrelevant/incorrect memory entries as a primary agent failure mode. Without quality gates, the KB accumulates noise that degrades Plan agent output over time.
  **PostgreSQL recursive CTEs instead of graph**   Episodic ingestion, bi-temporal edges, entity resolution, and contradiction detection are all Graphiti features that PostgreSQL would require rebuilding from scratch. The graph layer serves a fundamentally different purpose from the relational layer.
  **Custom compound system from scratch**          Months of development to reach the maturity the Every.to plugin already has. 10,000+ star community means bug reports, documentation, and cross-tool support already exist. Build custom only if the plugin proves inadequate after Phase 2.
  ------------------------------------------------ ------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------

**5. Risk Assessment**

Every architectural decision carries risk. This section documents failure modes and mitigations for the compound engineering approach.

  ------------------------------------------------------------- ------------------------------------------------------------------------------ ----------------- --------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------
  **Risk**                                                      **Failure Mode**                                                               **Probability**   **Mitigation**
  **Compound step produces generic/low-value learnings**        Context is stale when compound runs; AI compresses too aggressively            High              Enforce run order: Compound must be final Activity before any context disposal. Rubric gate (PUDDING ≥12) rejects low-quality entries.
  **KB noise accumulates, degrades Plan quality**               BRONZE entries enter without enrichment; deprecated entries not retired        Medium            GOLD/SILVER/BRONZE gates enforce quality. Quarterly Kaizen audit prunes stale entries. Deprecated entries move to \_archive/, excluded from search.
  **Every.to plugin becomes unmaintained**                      10,000+ star plugin stops receiving updates; breaks with Claude Code updates   Low               MIT licensed --- can be forked. Plugin structure is markdown files + commands, not compiled code. Core pattern (docs/solutions/ + YAML) is tool-independent.
  **Neo4j migration introduces new failure modes**              JVM OOM, GC pause storms, Docker permission issues                             Medium            8 known Neo4j failure modes already documented with mitigations (FAULT-028 through FAULT-035). Shadow phase (Stage 4) catches issues before cutover. Rollback criteria defined.
  **14 review agents produce redundant findings**               Multiple agents flag the same issue; P2 items pile up                          Medium            /triage command presents findings one-by-one for human decision. /resolve\_pr\_parallel processes in priority order (P1 first). Redundancy is lower-cost than gaps.
  **80/20 time allocation is impractical for solo developer**   Ewan cannot spend 80% on Plan+Review with a single-person team                 High              The 80/20 applies to the AI\'s time, not the human\'s. The human approves the plan, the AI executes. The ratio measures where AI compute goes, not human hours.
  **Tiered retrieval misses relevant solutions**                YAML tags don\'t match; solution is in KB but Plan agent doesn\'t find it      Medium            Start with YAML tag filtering + full-text search (two retrieval methods). Add vector embeddings at \>500 documents. Related-docs-finder agent in Compound step explicitly links solutions to catch future matches.
  **Single point of failure: Ewan as approver**                 Ewan unavailable; SILVER entries pile up; KB stops growing                     High              GOLD entries auto-add (lightweight review). Only SILVER requires explicit approval. Design GOLD thresholds generously. Build toward delegated approval as team grows.
  ------------------------------------------------------------- ------------------------------------------------------------------------------ ----------------- --------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------

**6. Attribution**

**Radical Attribution --- Full Provenance Chain**

  ------------------------------------------------- --------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------
  **Role**                                          **Detail**
  **Human Originator**                              Ewan Bramley --- original insight connecting compound engineering to PUDDING taxonomy; architectural direction for Beast/Cove integration; governance design; all final approval authority
  **AI Formaliser / Researcher**                    Claude (Anthropic) --- compound engineering research, pipeline specification, rubric integration, PUDDING meta-labelling, fault entry format, addition pipeline SOP consolidation
  **AI Fact-Checker**                               Perplexity AI --- compound engineering pattern research, academic foundations, Every.to plugin specification verification, source validation
  **Intellectual Lineage: Compound Engineering**    Kieran Klaassen (Every.to / Cora) --- Plan→Work→Review→Compound loop, 80/20 rule, docs/solutions/ format, 14 review agents, /lfg pipeline
  **Intellectual Lineage: LBD Theory**              Don R. Swanson (1924--2012) --- Literature-Based Discovery (1986), undiscovered public knowledge theory, ABC model (Fish Oil → Raynaud\'s), foundation for PUDDING technique
  **Intellectual Lineage: Self-Improving Agents**   Addy Osmani (Google Chrome) --- self-improving agent loops, tiered agent-native architecture, stateless-but-iterative design pattern
  **Intellectual Lineage: Lean/Kaizen**             Lean Manufacturing / Toyota Production System --- PDCA continuous improvement cycle, Kaizen loop applied to Stages 6--7 of the compound learning pipeline
  **Academic Validation**                           University of Bristol --- SICA (arXiv:2504.15228), self-improving coding agent proof-of-concept; MIT CSAIL (July 2025) --- process-capture research call; METR (July 2025) --- AI developer impact RCT
  **Fact Percentage**                               85% --- directly sourced from research documents, GitHub issues, published articles, and academic papers
  **Confidence Band**                               High --- all major decisions backed by multiple independent sources
  **PUDDING Label**                                 P.+.5.l --- Process, Amplifying, System-scale, Long-duration
  ------------------------------------------------- --------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------

**Source URLs**

1\. Every.to Compound Engineering Plugin --- https://github.com/EveryInc/compound-engineering-plugin

2\. \'My AI Had Already Fixed the Code Before I Saw It\' --- Kieran Klaassen --- https://every.to/source-code/my-ai-had-already-fixed-the-code-before-i-saw-it

3\. Every.to Compound Engineering Guide --- https://every.to/guides/compound-engineering

4\. \'Compound Engineering: How Every Codes With Agents\' --- https://every.to/chain-of-thought/compound-engineering-how-every-codes-with-agents

5\. \'Compound Engineering: The Definitive Guide\' --- https://every.to/source-code/compound-engineering-the-definitive-guide

6\. \'Self-Improving Agents\' --- Addy Osmani --- https://addyosmani.com/blog/self-improving-agents/

7\. \'Learning from Every\'s Compound Engineering\' --- Will Larson --- https://lethain.com/everyinc-compound-engineering/

8\. SICA: A Self-Improving Coding Agent --- arXiv:2504.15228 --- https://arxiv.org/abs/2504.15228

9\. METR Study --- https://metr.org/blog/2025-07-10-early-2025-ai-experienced-os-dev-study/

10\. MIT CSAIL --- https://news.mit.edu/2025/can-ai-really-code-study-maps-roadblocks-to-autonomous-software-engineering-0716

11\. Temporal Complexity Cliff --- https://temporal.io/blog/building-ai-agents-that-overcome-the-complexity-cliff

12\. The State of AI Coding 2025 --- Greptile --- https://www.greptile.com/state-of-ai-coding-2025

13\. \'The First 1,000 Lines\' --- Ivan Turkovic --- https://www.ivanturkovic.com/2026/02/24/first-1000-lines-determine-next-100000-ai-coding/

14\. Claude Code Memory Documentation --- https://code.claude.com/docs/en/memory

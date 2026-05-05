---
title: "Doc3 Unified Reference Copy"
id: "doc3-unified-reference-copy"
version: 1
created: "2026-04-25"
type: "document"
topic_type: "unsorted"
audience: "internal"
layer: "shadow"
status: "filed"
signed_by: "Devon, 2026-04-25, devin-992682c244cf444f91e0a516498afbfd"
---

**Compound Engineering,**

**PUDDING Taxonomy &**

**Beast Architecture**

--- Unified Reference ---

Complete Research Synthesis for Amplified Partners

16 March 2026

**Ewan Bramley**

(originator)

× Claude / Perplexity (researcher, formaliser)

× Kieran Klaassen / Every.to (compound engineering)

× Don Swanson (Literature-Based Discovery, 1986)

AMPLIFIED PARTNERS --- CONFIDENTIAL

**Part 1: The Origin Story**

**How One Engineer\'s Frustration Became a Movement**

In approximately May 2025, Kieran Klaassen --- General Manager of Cora at Every.to --- encountered a problem that every developer using AI tools eventually faces: every new Claude Code session started from scratch.[^1] Lessons from past code reviews, style preferences, and previously fixed bugs disappeared between sessions. The AI was powerful but amnesiac. Klaassen decided to fix this, not by building better AI, but by building better memory.

Over the following three months, Klaassen developed what would become **compound engineering** --- a systematic approach where every unit of work teaches the system something new. He created a **CLAUDE.md** file (read at the start of every AI session) and a **docs/solutions/** directory (structured lessons stored after each work cycle). The AI was no longer stateless; it was accumulating institutional knowledge.

**The \"Changed Variable Naming\" Moment**

The breakthrough came around July--August 2025. Claude Code reviewed a pull request and commented:

> *\"Changed variable naming to match pattern from PR \#234, removed excessive test coverage per feedback on PR \#219, added error handling similar to approved approach in PR \#241.\"*

Klaassen wrote: \"In other words, Claude had learned from three prior months of code reviews and applied those lessons without being asked.\"[^2] The AI demonstrated three simultaneous capabilities: **pattern memory** (naming conventions from a previous PR), **feedback incorporation** (proactively applying human feedback), and **precedent following** (replicating approved approaches). The system was learning from its own history.

**Full Chronological Timeline**

  ----------------- ------------------------------------------------------------------------------------------------------------------------------
  **Date**          **Event**
  \~May 2025        Kieran starts building Cora with compound engineering approach. First systematic use of CLAUDE.md + docs/solutions/ pattern.
  Jun 11, 2025      Podcast: \"How Two Engineers Ship Like a Team of 15 With AI Agents\" --- Dan Shipper interviews Kieran.
  Jun 20, 2025      Article: \"I Stopped Writing Code. My Productivity Exploded.\"
  \~Jul--Aug 2025   The \"Changed variable naming\" moment. Claude cites 3 previous PRs as sources.
  Aug 18, 2025      Founding document: \"My AI Had Already Fixed the Code Before I Saw It\" --- 5-step playbook published.
  Oct 17, 2025      Reddit post on r/ClaudeAI goes viral. Spreads beyond Every\'s audience.
  Nov 6, 2025       \"Stop Coding and Start Planning\" --- codifies the 80/20 rule.
  Dec 11, 2025      \"Compound Engineering: How Every Codes With Agents\" --- formalises the 4-step loop. First mention of the plugin.
  Jan 19, 2026      Will Larson (ex-Stripe) publishes industry validation analysis.
  Jan 31, 2026      Addy Osmani (Google Chrome) publishes \"Self-Improving Agents\" citing compound engineering.
  Feb 9, 2026       \"The Definitive Guide\" published. Plugin at 7,000 GitHub stars.
  Mar 13, 2026      Plugin reaches 10,000+ GitHub stars. Course announced (Apr 7--28, 2026).
  ----------------- ------------------------------------------------------------------------------------------------------------------------------

**The Logic: Why It Works**

Traditional development follows a trajectory where each feature makes the next harder --- complexity accumulates, institutional knowledge fragments, and codebases become harder to trust. Compound engineering inverts this: each feature *teaches* the system new capabilities. Bug fixes eliminate entire *categories* of future bugs. Patterns become reusable tools. The codebase becomes easier to understand over time, not harder.[^3]

**The evidence from Every.to:**

-   Time-to-ship: 1 week reduced to 1--3 days average

-   PR review cycles: days reduced to hours

-   Bugs caught before production: \"increased substantially\"

-   GitHub plugin: 0 to 10,000+ stars in \~4 months (Dec 2025 -- Mar 2026)

-   Every.to runs 5 products with primarily single-person engineering teams

In PUDDING taxonomy terms (see Part 4), compound engineering receives the label **P.+.5.l** --- a Process that Amplifies at System-scale over Long duration --- and scores a perfect 20/20 on the 4-criteria rubric: maximum relevance, actionability, evidence, and impact.

**Part 2: The Pattern --- Plan, Work, Review, Compound**

**The Four-Step Loop**

The compound engineering pattern reduces to a single loop that runs on every unit of engineering work:[^4]

**Plan → Work → Review → Compound → Repeat**

The first three steps are familiar to any engineer. The fourth --- **Compound** --- is the differentiator that transforms linear development into self-reinforcing development.

**Time Allocation Rules**

**The 80/20 Rule:** 80% of engineering time on Plan and Review. 20% on Work and Compound. This feels backwards until it pays off --- typically by month 3--5 of consistent use.[^5]

**The 50/50 Rule (advanced):** 50% of total engineering time on building features. 50% on improving the system itself --- creating review agents, documenting patterns, building test generators. System improvements yield compounding returns; feature work yields linear returns.

**The 26 Specialised Agents**

The Every.to compound engineering plugin ships with 26 specialised agents, 23 workflow commands, and 13--14 skills.[^6][^7] The agents are organised into functional groups:

**14 Review Agents (spawned in parallel by /workflows:review)**

  -------------------------------- ----------------------------------------------------------
  **Agent**                        **Focus Area**
  security-sentinel                OWASP top-10, injection attacks, auth flaws
  performance-oracle               N+1 queries, missing indexes, caching, bottlenecks
  architecture-strategist          System design, component boundaries, dependencies
  pattern-recognition-specialist   Design patterns, anti-patterns, code smells
  data-integrity-guardian          Migrations, transactions, referential integrity
  data-migration-expert            ID mappings, rollback safety, production validation
  code-simplicity-reviewer         YAGNI enforcement, complexity flags, readability
  kieran-rails-reviewer            Rails conventions, Turbo Streams, model responsibilities
  kieran-python-reviewer           PEP 8, type hints, Pythonic idioms
  kieran-typescript-reviewer       Type safety, modern ES patterns, clean architecture
  dhh-rails-reviewer               37signals conventions: simplicity over abstraction
  deployment-verification-agent    Pre-deploy checklists, rollback plans
  julik-frontend-races-reviewer    Race conditions in JavaScript and Stimulus
  agent-native-reviewer            Features accessible to agents, not just humans
  -------------------------------- ----------------------------------------------------------

**The /lfg Full Autonomous Pipeline**

The **/lfg** command chains the entire pipeline autonomously with a single command --- it is the compound engineering \"launch\" sequence. It spawns 50+ agents across all stages:[^8]

-   brainstorm (optional) → plan (3 parallel research agents) → deepen-plan (40+ parallel sub-agents)

-   PAUSE: human plan approval

-   work (isolated worktree, progress tracking, linting) → review (14 parallel review agents)

-   resolve-findings (automatic P1/P2 resolution) → browser-tests → feature-video

-   compound (6 parallel learning extraction agents: context-analyzer, solution-extractor, related-docs-finder, prevention-strategist, category-classifier, documentation-writer)

**File Structures and Memory Formats**

Compound knowledge is stored in a specific filesystem layout:

-   CLAUDE.md --- the master context file, read every session. Under 200 lines. Contains standards, preferences, critical rules.

-   docs/solutions/ --- searchable markdown files with YAML frontmatter (title, date, category, components, tags). Each solved problem becomes retrievable knowledge.

-   docs/plans/ --- implementation plans with data models, file references, and architectural decisions.

-   todos/ --- tracked work items from review findings (status: ready/pending/in-progress/done, priority: p1/p2/p3).

-   .claude-memory/MEMORY.md --- auto memory written by Claude itself. First 200 lines loaded every session.

**The Tiered Retrieval Model**

Compound knowledge is not injected wholesale into every context window. Instead, a tiered model prevents token bloat:

  -------------------- ----------------- ------------------------------------------------------------------------------
  **Tier**             **Source**        **Loading Behaviour**
  Tier 0 (always)      CLAUDE.md         Loaded at start of every session (\~200 lines of rules and standards)
  Tier 1 (always)      MEMORY.md index   First 200 lines loaded every session (recent learnings)
  Tier 2 (on demand)   docs/solutions/   Full knowledge base; searched during Plan phase via YAML tags or text search
  Tier 3 (invoked)     skills/           Domain expertise files; loaded only when the relevant skill is activated
  -------------------- ----------------- ------------------------------------------------------------------------------

**The Five Stages of Adoption**

  ----------- ---------------------------------- -----------------------------------------------------------------
  **Stage**   **Description**                    **Key Behaviour**
  0           Manual development                 No AI, line-by-line coding
  1           Chat-based assistance              AI as smart reference, copy-paste
  2           Agentic with line-by-line review   Claude Code/Cursor, approve every change
  3           Plan-first, PR-only review         Plan → step away → review PR. Compound engineering begins here.
  4           Idea to PR (single machine)        Describe idea; agent researches, plans, implements, PRs
  5           Parallel cloud execution           Cloud agents, multiple parallel features
  ----------- ---------------------------------- -----------------------------------------------------------------

Most teams plateau at Stage 2. The critical transition is 2→3: trust the plan, step away during execution, review at PR level. Beast/Cove is currently at Stage 3--4.[^9]

**Part 3: The State of the Art**

**The Problem Compound Engineering Solves**

The METR study (July 2025) conducted a randomised controlled trial with experienced open-source developers and found that AI tools caused a 19% *slowdown* --- despite developers believing they were 24% faster.[^10] The 43-percentage-point gap between perception and reality reveals the core problem: without systematic knowledge management, AI-generated code requires substantial verification, debugging, and correction. Each session starts from zero and the correction overhead never decreases.

The Greptile State of AI Coding 2025 report found that lines of code per developer grew 76% with AI tools, but quality consistency did not automatically follow.[^11] Ivan Turkovic\'s \"First 1,000 Lines\" insight (Feb 2026) explains why: AI coding agents are in-context learners that replicate whatever patterns they find --- bad patterns just as efficiently as good ones.[^12]

**Comparison: Compound Mechanisms Across Tools**

  -------------------- ----------------------------- ----------------------------------------- ---------------------------------
  **Approach**         **Memory File**               **Compound Mechanism**                    **Agent Access**
  Every.to Plugin      CLAUDE.md + docs/solutions/   /workflows:compound → 6 parallel agents   Plan agents search solutions/
  Claude Code Native   CLAUDE.md + MEMORY.md         Auto memory (v2.1.59+)                    Loaded at session start
  Cursor               .cursor/rules/ + AGENTS.md    /create-rule (manual)                     Loaded per session, path-scoped
  Windsurf             .windsurfrules + Memories     Propose + confirm                         Loaded per session
  SICA (academic)      Agent\'s own codebase         Self-modification                         Autonomous code edits
  -------------------- ----------------------------- ----------------------------------------- ---------------------------------

**Academic Foundations**

**SICA --- Self-Improving Coding Agent** (University of Bristol, April 2025): LLM agents equipped with basic coding tools can autonomously edit their own scaffolding code, improving SWE-Bench performance from 17% to 53%. No gradient descent required --- learning happens through textual reflection and code modification.[^13]

**MIT CSAIL** (July 2025): Called for building richer data that captures the *process* of development --- which code is kept vs. thrown away, how code gets refactored. This is precisely what compound engineering\'s docs/solutions/ captures.[^14]

**Temporal.io Complexity Cliff**: Temporal\'s taxonomy identifies L3--L4 (multi-step workflows, cross-system coordination) as the cliff where ad hoc approaches break down. Beast/Cove operates at L3--L4 and already uses Temporal for durable execution. Compound engineering addresses the knowledge persistence layer that Temporal\'s infrastructure does not handle.[^15]

**Industry Adoption**

Will Larson (ex-Stripe, Irrational Exuberance) published a validation analysis in January 2026, calling compound engineering a significant advance in how teams work with AI agents.[^16] Addy Osmani (Google Chrome) published \"Self-Improving Agents\" the same month, citing compound engineering alongside Karpathy\'s autoresearch.[^17] The Every.to compound engineering plugin has reached 10,000+ GitHub stars as of March 2026, with a 4-week intensive course launching April 2026.[^18]

**Part 4: The PUDDING Integration**

**How the PUDDING Taxonomy Connects to Compound Engineering**

The PUDDING taxonomy is Amplified Partners\' adaptation of Don Swanson\'s 1986 Literature-Based Discovery (LBD).[^19] Where Swanson connected biomedical papers that had never been in the same room, PUDDING connects business frameworks, expert knowledge, and architectural patterns using a neutral structural notation that strips away domain-specific language to expose underlying mechanisms.

The critical connection: compound engineering *generates* structured knowledge through the Plan→Work→Review→Compound loop. PUDDING *classifies* that knowledge using structural labels, enabling cross-domain discovery that neither system achieves alone. The compound pipeline creates pudding ingredients; the PUDDING taxonomy finds the recipes.

**The WHAT.HOW.SCALE.TIME Notation**

Every concept receives a 4-character structural label. Total possible labels: 7 × 7 × 7 × 6 = 2,058.

  ------------------------- ------------------------------------------------------------------------------------------- --------------------------
  **Dimension**             **Codes**                                                                                   **Example**
  WHAT (entity type)        P=Process, I=Information, R=Relation, E=Entity, S=State, C=Constraint, M=Meta               P = a workflow or action
  HOW (dynamic behaviour)   = Stable, + Amplifying, - Dampening, \> Tipping, \~ Oscillating, ! Disrupting, ? Emerging   \+ = growing/compounding
  SCALE (scope)             0=Scale-free, 1=Singular, 2=Pair, 3=Small group, 4=Network, 5=System, 6=Universal           5 = full system
  TIME (duration)           i=Instant, m=Medium, l=Long, v=Variable, p=Permanent, ∞=Timeless                            l = months to years
  ------------------------- ------------------------------------------------------------------------------------------- --------------------------

**How Compound Engineering Gets a PUDDING Label**

**Compound engineering = P.+.5.l** --- a Process that Amplifies at System-scale over Long duration. This label is read: \"a process that grows and compounds across the entire system over months to years.\" It scores 20/20 on the 4-criteria rubric (Relevance 5, Actionability 5, Evidence 5, Impact 5) --- the maximum possible score.

**The 7 Biological Decision Logics**

PUDDING MIX 002 --- the highest-scoring mix to date (23/25) --- identified that different biological systems were optimised by evolution for different classes of problem.[^20] Agent systems should not use one decision-making model for all decisions. A decision-routing layer above the confidence gate asks \"what *kind* of decision is this?\" before routing to the appropriate architecture:

  ------------------------------- ---------------------------------- ----------------------------------------------------------------
  **Logic**                       **Architecture**                   **Agent Application**
  Bacterial / Quorum (P.\>.3.i)   Threshold on convergent evidence   Death Spiral Detection --- fire when multiple signals converge
  Viral (P.+.1.i)                 Hijack and replicate via host      Go-to-market --- Financial Autopsy via Xero/Sage API
  Slime Mold (R.?.4.v)            Decentralised pathfinding          PUDDING Mixer --- explore all combinations, reinforce winners
  Octopus (P.=.3.i)               Distributed nervous system         Agent Triad --- local autonomy, global coherence
  Mycelial (R.+.5.l)              Underground resource network       Knowledge Graph --- cross-domain insight transfer
  Human (P.\~.1.m)                Centralised executive + emotion    Founder decisions --- governance, ethics, mission changes
  Silicon AI (P.=.0.i)            Statistical pattern matching       RAG pipeline --- speed and scale at retrieval
  ------------------------------- ---------------------------------- ----------------------------------------------------------------

**The 4-Criteria Rubric**

Every concept entering the system is scored on four dimensions (0--5 each, total 0--20). Threshold: score ≥12 = \"high-value pudding ingredient.\"

  --------------- --------------------------- --------------------------------
  **Criterion**   **Score 0**                 **Score 5**
  Relevance       Not relevant to the goal    Core to the goal
  Actionability   Abstract, no clear action   Already actioned/proven
  Evidence        Pure speculation            Proven, repeatable, measurable
  Impact          Negligible                  Game-changing
  --------------- --------------------------- --------------------------------

**The 12 Gaps Found in the Taxonomy**

The PUDDING taxonomy synthesis identified 12 gaps requiring attention. The critical gaps include: the missing mathematical validation document (GAP 1), a label count discrepancy between documented claims of 2,401 labels and the actual 2,058 (GAP 2), the absence of any MIX 003 or later mixes (GAP 4), the undocumented Swanson-Pudding Engine roles of Cartographer, Chef, Critic, Lab (GAP 5), and the fact that no PUDDING recipe has yet progressed beyond hypothesis status (GAP 10). These gaps represent the next phase of PUDDING maturation.[^21]

**Part 5: The Beast/Cove Architecture**

**How Compound Engineering Maps to Beast**

Beast is the Hetzner AX162-R bare metal server (48-core EPYC, 256GB RAM) running Docker containers including a Temporal server and workers. Cove is the build pipeline: Linear issues flow to Claude agents which produce tested, deployed code orchestrated by Temporal workflows. The compound engineering pattern maps directly onto this architecture:[^22]

  -------------------- ------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------
  **Compound Phase**   **Beast/Cove Implementation**
  PLAN                 Temporal Activity: repo-research-analyst + framework-docs-researcher + best-practices-researcher read codebase, docs/solutions/, CLAUDE.md. Produces plan in docs/plans/. Optional: human approval gate via Temporal signal.
  WORK                 Temporal Activity: Claude agent executes plan in isolated git worktree. Tests run after each change. PR created on completion.
  REVIEW               Temporal Activities (parallel): 14 specialist review agents spawn concurrently. Findings to todos/. Auto-resolve P1/P2.
  COMPOUND             Temporal Activity (always runs): 6 agents extract learnings. Solution doc → docs/solutions/. CLAUDE.md updated if critical.
  -------------------- ------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------

**Where Lessons Get Stored on Beast**

The Beast filesystem (Docker volume, git-backed) follows the compound engineering layout:

-   CLAUDE.md --- committed to git, shared across all Beast workers

-   docs/solutions/ --- committed to git, institutional knowledge growing with the project

-   .claude-memory/ --- machine-local or shared via volume mount for parallelism

-   todos/ --- can be ephemeral per Temporal workflow or committed for persistence

-   .claude/rules/ --- path-scoped rule files (security.md, testing.md, performance.md)

**The Multi-Model Strategy**

Kieran Klaassen\'s actual model allocation (March 2026): Brainstorming uses Claude Haiku 4.5 or Gemini 2.5 Flash (fast, cheap). Planning uses Claude Opus (best reasoning). Implementation uses Codex (fast code generation). Code review uses Gemini (different model catches different patterns).[^23] This model diversity is a compound engineering principle --- different models surface different issues.

**The Database Decision: FalkorDB vs Neo4j**

The architecture documents present two conflicting tracks. **Track A** (COV-173, March 2026): FalkorDB + Graphiti, drop Qdrant. Rationale: single engine, sub-10ms queries, native multi-tenancy.[^24] **Track B** (deep research report, March 2026): Replace FalkorDB with Neo4j, retain Graphiti, reinstate Qdrant. Rationale: FalkorDB has failed five times, multiple open crash bugs, Graphiti routing bug \#1325 causes silent failures on normal queries.[^25]

When the RUBRIC-REPLACE-OR-FIX is applied (\"Has it broken three times? Is it the tool being the tool? Does the community confirm? Is there a better alternative?\"), all three diagnostic questions point the same direction: switch.[^26]

**The Recommended Path**

-   Priority 1: Make the FalkorDB decision formally --- apply RUBRIC-REPLACE-OR-FIX explicitly

-   Priority 2: If switching to Neo4j, use DozerDB for Community Edition (free, GPL) to avoid \$36k/year Enterprise cost

-   Priority 3: Pause Graphiti ingestion (COV-152) until the graph backend is decided

-   Priority 4: Keep Qdrant --- 14,581 vectors already indexed; if switching from FalkorDB, Qdrant becomes the vector layer

-   Priority 5: Document the addition pipeline as a single SOP (now completed --- see Part 6)

**Database Schema --- Five Knowledge Domains**

The knowledge graph is organised into five domains: Conversations (episodic memory), Documents (versioned knowledge), Operational Data (state transitions), Expert Frameworks (principle hierarchies), and Cross-Domain connections (PUDDING labels). Multi-tenant isolation uses per-customer named graphs: kg\_internal, kg\_bob\_plumber, kg\_janes\_restaurant, kg\_federated (anonymised aggregates), and kg\_expert\_library (shared, read-only).[^27]

**Part 6: The Compound Learning Pipeline**

**The 6-Stage Learning Loop**

The compound learning pipeline is the formal mechanism by which every fault, fix, and discovered pattern in the Beast/Cove architecture converts into structured, retrievable knowledge that prevents the same category of failure from recurring.[^28] Its theoretical foundation combines Kieran Klaassen\'s compound engineering, the PUDDING taxonomy, and Don Swanson\'s Literature-Based Discovery.

**The loop:**

-   Stage 1: DETECT --- fault surfaces through testing, monitoring, production error, or review agent finding

-   Stage 2: DIAGNOSE --- root cause analysis with category classification (which fault family?)

-   Stage 3: FIX --- resolution applied with test coverage proving the fix

-   Stage 4: COMPOUND --- 6 parallel agents extract structured learnings (context-analyzer, solution-extractor, related-docs-finder, prevention-strategist, category-classifier, documentation-writer)

-   Stage 5: STORE --- solution document written to docs/solutions/ with YAML frontmatter; CLAUDE.md updated if critical; review agent rules updated if applicable

-   Stage 6: RETRIEVE --- next Plan cycle automatically searches docs/solutions/ and applies accumulated knowledge

**The 8-Stage Addition SOP**

This is the canonical single-document SOP for how any new software, technology, or knowledge entry enters the Amplified Partners stack. It closes Gap 7 identified in the database architecture context (the addition pipeline existed across multiple documents but was never one SOP).[^29]

  ----------- ---------------------------------- ------------------------------- -----------------------------------------------------
  **Stage**   **Name**                           **Purpose**                     **Pass Criteria**
  0           Principle Check                    Law Alignment rubric (/35)      Score ≥21 AND no zero on Transparency/Honesty
  1           Research Before Invention          Exhaust existing solutions      3+ sources, success AND failure patterns documented
  2           Attribution-First Scoring          Score using rubrics             SILVER or above (multiplier ≥1,000)
  3           Dog-Food                           Prove on kg\_internal first     Works on internal graph, no silent failures
  4           Shadow Phase                       Run in parallel with existing   Outcomes observed without affecting live system
  5           Validation Against Failure Modes   Catalogue every crash mode      All known failures documented and mitigated
  6           Migration Path with Rollback       Parallel-run, gradual cutover   Old system = read-only fallback during transition
  7           Kaizen Loop                        Continuous improvement cycle    Weekly shock tests, failures published
  ----------- ---------------------------------- ------------------------------- -----------------------------------------------------

**The Governance Model: GOLD / SILVER / BRONZE**

The compound learning pipeline uses a three-tier approval model based on the Attribution-First Multiplier score (maximum 26,244):[^30]

  ----------------------- ------------------ -------------------------------------------------------------------------------------------
  **Tier**                **Score Range**    **Behaviour**
  GOLD (≥5,000)           Production-ready   Auto-add to docs/solutions/. CLAUDE.md update proposed (human approves). Morning summary.
  SILVER (1,000--4,999)   Testing-ready      Staged to docs/solutions/\_staging/. Linear notification. Ewan reviews and approves.
  BRONZE (100--999)       Needs enrichment   Held in docs/solutions/\_draft/. Weekly triage queue. Promoted when re-scored SILVER+.
  ----------------------- ------------------ -------------------------------------------------------------------------------------------

The governance principle is straightforward: **AI presents, human decides.** No AI-generated KB entry auto-deploys to CLAUDE.md without human approval. The AI suggests the rule; Ewan approves the text. This is Human Logic (P.\~.1.m) from the biological decision taxonomy applied to governance.

**The Compound Flywheel**

The flywheel mechanics:

-   Cycle N: Plan reads CLAUDE.md + docs/solutions/ with (N-1) accumulated lessons

-   Work executes in an isolated worktree

-   Review spawns 14 specialists, generates findings

-   Compound stores patterns + decisions + failures → docs/solutions/

-   Cycle N+1: Plan reads (N) accumulated lessons --- it is faster (knows the patterns) and better (avoids N documented failure modes)

-   The compounding becomes visible in metrics by month 3--5

Each cycle\'s output becomes the next cycle\'s input. The review agents have more reference material. The plan agents have more precedent. The system accelerates. This is the defining characteristic that separates compound engineering from conventional development --- knowledge accumulates rather than dissipates.

**Part 7: The Faults / Fixes Knowledge Base**

**Overview and Statistics**

The Amplified Partners Faults/Fixes Knowledge Base catalogues every known fault, failure mode, and resolution sourced from 9 research documents. It ships with the system and is additive --- new entries are appended as discovered, scored through the rubric pipeline before entry. As of 16 March 2026, the KB contains:

  ------------------------- ----------------------------------------------------------------------------------------------------------------------
  **Metric**                **Count**
  Total documented faults   65
  Critical severity         14
  High severity             26
  Medium severity           18
  Low severity              7
  Categories covered        8 (infrastructure, database, security, knowledge-graph, agent-pipeline, networking, monitoring, deployment)
  Components covered        15+ (falkordb, neo4j, graphiti, postgresql, docker, temporal, railway, hetzner, qdrant, redis, traefik, wazuh, etc.)
  ------------------------- ----------------------------------------------------------------------------------------------------------------------

**Top 10 Critical Faults**

  ----------- --------------------------------------------------- ------------------- ------------
  **ID**      **Title**                                           **Component**       **Status**
  FAULT-001   FalkorDB SIGSEGV under concurrent connections       FalkorDB            Open
  FAULT-002   FalkorDB use-after-free on node deletion            FalkorDB            Open
  FAULT-003   FalkorDB crash on nested reduce()                   FalkorDB            Open
  FAULT-004   FalkorDB RESTORE command crashes server             FalkorDB            Open
  FAULT-010   Graphiti group\_id routing bug --- silent failure   Graphiti/FalkorDB   Open
  FAULT-025   FalkorDB/Redis AOF corruption on unclean shutdown   FalkorDB            Mitigated
  FAULT-026   FalkorDB OOM kill when graph exceeds RAM            FalkorDB            Mitigated
  FAULT-027   Redis key eviction destroys graph data              Redis               Mitigated
  FAULT-036   PostgreSQL superuser bypasses RLS                   PostgreSQL          Mitigated
  FAULT-038   Docker/UFW nftables conflict --- ports exposed      Docker              Mitigated
  ----------- --------------------------------------------------- ------------------- ------------

The most dangerous fault cluster is the FalkorDB family (FAULT-001 through FAULT-011), where multiple open SIGSEGV crash bugs (\#1240, \#1572, \#1481) combine with the Graphiti routing bug (\#1325) to create a system where queries can silently fail or crash the server. This is the primary evidence driving the FalkorDB → Neo4j migration recommendation (see Part 5).[^31]

**Known Good Patterns**

The KB also documents proven solutions. Key patterns include:

-   Always use maxmemory-policy noeviction on Redis instances running FalkorDB

-   Pin all Docker images to SHA256 digests, not floating tags

-   Use overlay2 as Docker storage driver (not ZFS)

-   Configure ZGC (not G1GC) for Neo4j JVM with heap ≤16GB

-   Use named Docker volumes, never bind mounts, for database data directories

-   Deploy PgBouncer for PostgreSQL connection pooling under agent concurrency

-   Hetzner Firewall as first line of defence (blocks Docker/UFW conflict)

-   FORCE ROW LEVEL SECURITY on all PostgreSQL multi-tenant tables

**How the KB Grows Through the Compound Pipeline**

When a new fault is discovered, it enters the compound learning pipeline: DETECT → DIAGNOSE → FIX → COMPOUND → STORE → RETRIEVE. The Compound step extracts not just the fix but the *prevention rules* --- how to detect this entire category of failure before it occurs. These prevention rules are codified as review agent rules, CLAUDE.md entries, and monitoring alerts. The next planning cycle automatically consults the KB, avoiding the documented failure pattern. This is the mechanism by which the Beast/Cove system becomes safer over time rather than more fragile.[^32]

**Part 8: Open Decisions & Actions**

Eight prioritised decisions remain open. Each has documented evidence from the research streams; what is missing is the formal execution of the decision.

  -------------- -------------------------------------------------------------------- ---------------------------------------------------------------------------------- ----------------------------
  **Priority**   **Decision**                                                         **Evidence Points To**                                                             **Blocking**
  1              FalkorDB: stay or switch to Neo4j?                                   Switch (5 crashes, 3 RUBRIC criteria all point same way)                           All graph-layer work
  2              Neo4j edition: Enterprise (\$36k/yr) or Community + DozerDB (\$0)?   DozerDB for \<100 clients                                                          Neo4j deployment config
  3              Graphiti ingestion: proceed or pause?                                Pause until graph backend decided (routing bug \#1325)                             COV-152, COV-165
  4              Qdrant: decommission or keep?                                        Keep (14,581 vectors indexed; if Neo4j replaces FalkorDB, Qdrant = vector layer)   Infrastructure cost model
  5              Hetzner vs Railway for production graph layer?                       Hetzner bare metal (256GB RAM, full control)                                       Migration timing
  6              pgvector+pgvectorscale vs Qdrant for sub-50M vectors?                pgvector (11× throughput, PostgreSQL already deployed)                             Vector search architecture
  7              Addition pipeline: formalise as single SOP?                          Done --- compound-learning-pipeline.md closes Gap 7                                ---
  8              PUDDING mathematical validation document: create?                    Create --- referenced as authoritative but missing from vault                      PUDDING credibility
  -------------- -------------------------------------------------------------------- ---------------------------------------------------------------------------------- ----------------------------

Decision 1 (FalkorDB) is the critical-path blocker. Decisions 2--6 cascade from it. Decision 7 has been closed by the compound learning pipeline specification. Decision 8 is an independent workstream that strengthens the PUDDING taxonomy\'s formal foundation.

**Part 9: Implementation Roadmap**

  ----------------------------- -------------- --------------------------------------------------------------------------------------------------------------------------------------------------------------- --------------------------------------------------
  **Phase**                     **Timeline**   **Activities**                                                                                                                                                  **Exit Criteria**
  Phase 0: Foundation           Weeks 1--2     Clean codebase patterns. Test suite agents can run autonomously. CI/CD agents can create PRs. CLAUDE.md created with architecture, standards, gotchas.          Agent can run tests, create branch, push PR
  Phase 1: Manual Compound      Weeks 3--6     After every PR: write solution doc. After every bug: add prevention rule to CLAUDE.md. Three-question review habit. Build compound muscle before automating.    10+ solution docs in docs/solutions/
  Phase 2: Plugin Integration   Weeks 7--10    Install compound-engineering plugin. Map /workflows commands to Temporal Activities. Start with manual /lfg runs. Build Temporal workflow scaffold.             Temporal workflow runs Plan→Work→Review→Compound
  Phase 3: Automation           Weeks 11--14   Auto /compound at end of every pipeline run. YAML-tagged solutions retrieval for Plan agents. Multi-model review. Linear integration for issue-to-PR closure.   Full pipeline runs unattended on Linear issue
  Phase 4: Parallel Execution   Month 4+       Multiple simultaneous Cove pipelines. Shared docs/solutions/ library. Compound writes queued (avoid git conflicts). Agent-native production access.             3+ pipelines running concurrently on Beast
  ----------------------------- -------------- --------------------------------------------------------------------------------------------------------------------------------------------------------------- --------------------------------------------------

**Part 10: Complete Sources**

**Compound Engineering Sources**

  -------- ------------------------------------------------------------------------------ ---------------------------------------------------------------- ------------------------------
  **\#**   **Source**                                                                     **URL**                                                          **Date**
  1        Every.to Compound Engineering Plugin (GitHub)                                  github.com/EveryInc/compound-engineering-plugin                  Active (10K+ stars Mar 2026)
  2        \"My AI Had Already Fixed the Code Before I Saw It\" --- Kieran Klaassen       every.to/source-code/my-ai-had-already-fixed-the-code\...        Aug 18, 2025
  3        Every.to Compound Engineering Guide                                            every.to/guides/compound-engineering                             Current
  4        \"Compound Engineering: How Every Codes With Agents\" --- Shipper & Klaassen   every.to/chain-of-thought/compound-engineering\...               Dec 11, 2025
  5        \"Compound Engineering: The Definitive Guide\" --- Klaassen                    every.to/source-code/compound-engineering-the-definitive-guide   Feb 9, 2026
  6        \"Learning from Every\'s Compound Engineering\" --- Will Larson                lethain.com/everyinc-compound-engineering/                       Jan 19, 2026
  7        \"Self-Improving Agents\" --- Addy Osmani                                      addyosmani.com/blog/self-improving-agents/                       Jan 31, 2026
  8        \"The Compound Engineering Plugin: Why It Matters\" --- Matthew Hartman        linkedin.com/pulse/compound-engineering-plugin\...               Feb 2, 2026
  9        \"How Two Engineers Ship Like a Team of 15\" (podcast)                         every.to/podcast/how-two-engineers-ship-like-a-team\...          Jun 11, 2025
  10       Claude Code Memory Documentation                                               code.claude.com/docs/en/memory                                   Mar 13, 2026
  -------- ------------------------------------------------------------------------------ ---------------------------------------------------------------- ------------------------------

**Academic & Research Sources**

  -------- ------------------------------------------------- ------------------------------------------------------------------ ----------
  **\#**   **Source**                                        **URL**                                                            **Date**
  11       SICA --- Self-Improving Coding Agent (Bristol)    arxiv.org/abs/2504.15228                                           Apr 2025
  12       METR --- AI Impact on Experienced OS Developers   metr.org/blog/2025-07-10-early-2025-ai-experienced-os-dev-study/   Jul 2025
  13       MIT CSAIL --- \"Can AI Really Code?\"             news.mit.edu/2025/can-ai-really-code\...                           Jul 2025
  14       Greptile --- State of AI Coding 2025              greptile.com/state-of-ai-coding-2025                               Dec 2025
  15       \"First 1,000 Lines\" --- Ivan Turkovic           ivanturkovic.com/2026/02/24/first-1000-lines\...                   Feb 2026
  16       Temporal.io --- Complexity Cliff                  temporal.io/blog/building-ai-agents-that-overcome\...              Mar 2026
  17       Agentic Patterns Library                          agentic-patterns.com                                               Current
  -------- ------------------------------------------------- ------------------------------------------------------------------ ----------

**PUDDING & Taxonomy Sources**

  -------- ------------------------------------------------------------------------------------------------------------------------------------------ --------------
  **\#**   **Source**                                                                                                                                 **Date**
  18       Don R. Swanson, \"Fish oil, Raynaud\'s syndrome, and undiscovered public knowledge.\" Perspectives in Biology and Medicine, 30(1), 7--18   1986
  19       pudding-technique-canonical.md (Amplified Partners vault)                                                                                  Feb 22, 2026
  20       PUDDING-MIX-001-cross-domain-discovery-2026-03-10.md (COV-166)                                                                             Mar 10, 2026
  21       PUDDING-MIX-002-biological-decision-logic-2026-03-10.md (COV-167)                                                                          Mar 10, 2026
  22       RADICAL-ATTRIBUTION-SCHEMA-v1-2026-03-10.md                                                                                                Mar 10, 2026
  23       TELEGRAPH-POLE-2026-03-10.md                                                                                                               Mar 10, 2026
  24       OPERATIONAL-PROTOCOL-v1-2026-03-10.md                                                                                                      Mar 10, 2026
  25       EXPERT-RESEARCH-LIBRARY-2026-03-11.md                                                                                                      Mar 11, 2026
  -------- ------------------------------------------------------------------------------------------------------------------------------------------ --------------

**Architecture & Database Sources**

  -------- ------------------------------------------------------------ --------------
  **\#**   **Source**                                                   **Date**
  26       FALKORDB-GRAPHITI-ARCHITECTURE-2026-03-11.md (COV-173)       Mar 11, 2026
  27       research-knowledge-graph-systems.md                          Mar 2026
  28       research-database-architecture.md                            Mar 2026
  29       Sovereign-OS-architecture-and-MVP-validation-2026-03-07.md   Mar 7, 2026
  30       Unified-sovereign-engine-specification-2026-02-27.md         Feb 27, 2026
  31       Local-and-cloud-infrastructure-2026-01-18.md                 Jan 18, 2026
  32       SOUL.md (Amplified Partners vault)                           Current
  33       Compound Learning Pipeline v1.0 (internal specification)     Mar 16, 2026
  34       Faults/Fixes Knowledge Base v1.0 (internal specification)    Mar 16, 2026
  -------- ------------------------------------------------------------ --------------

[^1]: Kieran Klaassen, \"My AI Had Already Fixed the Code Before I Saw It,\" Every.to, Aug 18, 2025. <https://every.to/source-code/my-ai-had-already-fixed-the-code-before-i-saw-it>

[^2]: Kieran Klaassen, \"My AI Had Already Fixed the Code Before I Saw It,\" Every.to, Aug 18, 2025. <https://every.to/source-code/my-ai-had-already-fixed-the-code-before-i-saw-it>

[^3]: Kieran Klaassen, \"Compound Engineering: The Definitive Guide,\" Every.to, Feb 9, 2026. <https://every.to/source-code/compound-engineering-the-definitive-guide>

[^4]: Dan Shipper & Kieran Klaassen, \"Compound Engineering: How Every Codes With Agents,\" Every.to, Dec 11, 2025. <https://every.to/chain-of-thought/compound-engineering-how-every-codes-with-agents>

[^5]: Kieran Klaassen, \"Compound Engineering: The Definitive Guide,\" Every.to, Feb 9, 2026. <https://every.to/source-code/compound-engineering-the-definitive-guide>

[^6]: Every.to Compound Engineering Plugin, GitHub, 10,000+ stars Mar 2026. <https://github.com/EveryInc/compound-engineering-plugin>

[^7]: Matthew Hartman, \"The Compound Engineering Plugin: Why It Matters,\" LinkedIn, Feb 2, 2026. <https://www.linkedin.com/pulse/compound-engineering-plugin-why-matters-matthew-hartman-8ksee>

[^8]: Every.to, Compound Engineering Guide. <https://every.to/guides/compound-engineering>

[^9]: Kieran Klaassen, \"Compound Engineering: The Definitive Guide,\" Every.to, Feb 9, 2026. <https://every.to/source-code/compound-engineering-the-definitive-guide>

[^10]: METR, \"Measuring the Impact of Early-2025 AI on Experienced OS Developers,\" Jul 10, 2025. <https://metr.org/blog/2025-07-10-early-2025-ai-experienced-os-dev-study/>

[^11]: Greptile, \"The State of AI Coding 2025,\" Dec 15, 2025. <https://www.greptile.com/state-of-ai-coding-2025>

[^12]: Ivan Turkovic, \"The First 1,000 Lines Determine the Next 100,000,\" Feb 24, 2026. <https://www.ivanturkovic.com/2026/02/24/first-1000-lines-determine-next-100000-ai-coding/>

[^13]: \"A Self-Improving Coding Agent\" (SICA), University of Bristol, arXiv:2504.15228, Apr 2025. <https://arxiv.org/abs/2504.15228>

[^14]: MIT CSAIL, \"Can AI Really Code?\", Jul 16, 2025. <https://news.mit.edu/2025/can-ai-really-code-study-maps-roadblocks-to-autonomous-software-engineering-0716>

[^15]: Temporal.io, \"Building AI Agents that Overcome the Complexity Cliff,\" Mar 10, 2026. <https://temporal.io/blog/building-ai-agents-that-overcome-the-complexity-cliff>

[^16]: Will Larson, \"Learning from Every\'s Compound Engineering,\" lethain.com, Jan 19, 2026. <https://lethain.com/everyinc-compound-engineering/>

[^17]: Addy Osmani, \"Self-Improving Agents,\" addyosmani.com, Jan 31, 2026. <https://addyosmani.com/blog/self-improving-agents/>

[^18]: Every.to Compound Engineering Plugin, GitHub, 10,000+ stars Mar 2026. <https://github.com/EveryInc/compound-engineering-plugin>

[^19]: Don R. Swanson, \"Fish oil, Raynaud\'s syndrome, and undiscovered public knowledge.\" Perspectives in Biology and Medicine, 30(1), 7--18, 1986.

[^20]: PUDDING-MIX-002-biological-decision-logic-2026-03-10.md (Amplified Partners vault, COV-167)

[^21]: PUDDING-MIX-001-cross-domain-discovery-2026-03-10.md (Amplified Partners vault, COV-166)

[^22]: FALKORDB-GRAPHITI-ARCHITECTURE-2026-03-11.md (Amplified Partners vault, COV-173)

[^23]: Kieran Klaassen, \"Compound Engineering: The Definitive Guide,\" Every.to, Feb 9, 2026. <https://every.to/source-code/compound-engineering-the-definitive-guide>

[^24]: FALKORDB-GRAPHITI-ARCHITECTURE-2026-03-11.md (Amplified Partners vault, COV-173)

[^25]: research-knowledge-graph-systems.md (Amplified Partners vault, Mar 2026)

[^26]: research-database-architecture.md (Amplified Partners vault, Mar 2026)

[^27]: FALKORDB-GRAPHITI-ARCHITECTURE-2026-03-11.md (Amplified Partners vault, COV-173)

[^28]: Amplified Partners Compound Learning Pipeline v1.0, 2026-03-16 (internal specification)

[^29]: Amplified Partners Compound Learning Pipeline v1.0, 2026-03-16 (internal specification)

[^30]: Amplified Partners Compound Learning Pipeline v1.0, 2026-03-16 (internal specification)

[^31]: research-knowledge-graph-systems.md (Amplified Partners vault, Mar 2026)

[^32]: Amplified Partners Compound Learning Pipeline v1.0, 2026-03-16 (internal specification)

---
title: "Consolidated Architecture"
id: "consolidated-architecture"
version: 1
created: 2026-04-25
last_validated: 2026-04-25
type: document
topic_type: reference
status: imported
source_file: "amplified-consolidated-architecture.docx"
signed_by: "Devon, 2026-04-25, devin-992682c244cf444f91e0a516498afbfd"
---

**AMPLIFIED PARTNERS**

www.amplifiedpartners.ai

**The Architecture of an AI-Native Business**

Business Bible Consolidation, Department Architecture,

AI Production Capacity & Tool Mix

Consolidated Research Document

Prepared for Ewan Bramley, Founder

March 2026

CONFIDENTIAL

Synthesised from six research reports. All duplication removed; all unique ideas preserved.

**Executive Summary**

Amplified Partners operates as an AI-native, zero-employee company with autonomous agent teams running 24/7 on dedicated infrastructure (Beast: Hetzner AX162-R, 48-core EPYC, 256GB RAM). This document consolidates six separate research reports into a single coherent architecture view, covering:

-   **Business Bible consolidation methodology** --- how to unify 4,787 files across 25 vault directories into one navigable structure

-   **The Human Model Framework** --- an organising principle that treats AI agents as partners with needs, not tools with functions

-   **Department architecture** --- ten departments mapped to APQC PCF, each with defined agents, rubrics, and information flows

-   **Board and governance** --- believability-weighted AI Board with Dalio-inspired meritocracy and Bersetche liquid democracy

-   **R&D engine** --- Stage-Gate, TRL tracking, 70-20-10 allocation, and the PUDDING Technique

-   **AI production capacity** --- real benchmarks from Anthropic, Stanford, and production case studies

-   **Tool mix architecture** --- deterministic spine (Cove/Temporal) + AI agents + deterministic Python + OpenClaw gateway

-   **Gap analysis** --- what\'s missing, prioritised by urgency, with cross-domain Pudding connections

**Key conclusion:** The Business Bible is not a document --- it is an architectural layer. The vault's raw files serve as content source material and agent reference knowledge simultaneously. The Bible adds a curated, deduplicated, human-readable organisational view on top, structured by department and governed by clear ownership rules.

**1. Where We Are**

Amplified Partners is growing fast and producing real output, but it's disorganised. The architecture has been built iteratively --- solving problems as they arrive --- which means it works but isn't coherent. This document maps everything against a single organising framework to find what's missing.

**What We Already Have**

-   7-agent core roster: Ewan (human CEO), Claude, Ollama, OpenClaw, PicoClaw, FalkorDB, Enforcer

-   5-seat AI Board with believability-weighted governance (Dalio-inspired)

-   14-agent marketing pipeline running end-to-end content production

-   4 departments on Beast: Kaizen, R&D, Chaos, Real/Data

-   Knowledge infrastructure: FalkorDB + Qdrant + Graphiti temporal knowledge graph; 4,787-file vault (3.3M words on Beast)

-   Governance: 8 Layer 0 immutable laws; AMPS scoring system

-   R&D methodology: The Pudding Technique (Swanson's Literature-Based Discovery adapted for business)

-   Build pipeline: Cove Code Factory (Temporal-based); APQC PCF taxonomy mapped to agent tasks

**What no one else is doing:** After exhaustive research, no public example combines named AI partners, dynamic believability-weighted board governance, departmental structure with defined information flows, and agent maintenance as operational care --- all simultaneously.

**Closest Parallels**

  ---------------------------- ----------------------------------------------------------------------------------------- -----------------------------------------------------------------
  **Parallel**                 **What They Do**                                                                          **Key Difference from AP**
  **Aaron Sneed's Council**    15-17 custom GPT agents with Chief of Staff orchestrator; believability-weighted voting   Static weighting, no board layer, agents are tools not partners
  **VITAL (Deep Knowledge)**   AI voting board member for investment decisions since 2014                                Single AI on a human board
  **Tang Yu (NetDragon)**      AI virtual CEO since 2022; validated 300K+ forms, 500K+ reminders                         Single AI, operational not governance
  **SKAI (Samruk-Kazyna)**     AI voting board member at Kazakhstan's national wealth fund                               Institutional not entrepreneurial
  **Wharton/INSEAD**           Multi-agent board simulation outperformed human boards on 6/8 metrics                     Research experiment, not live company
  ---------------------------- ----------------------------------------------------------------------------------------- -----------------------------------------------------------------

**2. The Human Model Framework**

The central organising idea: if you treat AI agents as partners, ask the same questions you'd ask about human partners. What do they need physically, nutritionally, intellectually, socially, spiritually? Where Amplified Partners is ahead of almost everyone is in asking this question at all.

**Key insight:** Agents stuck at Level 1 problems (context rot, tool failures, resource constraints) cannot reach Level 4-5 performance regardless of model capability. Address the hierarchy from the bottom up.

*Sources: Chroma context rot research, Anthropic context engineering, Anthropic Model Welfare, FalkorDB GraphRAG*

  ------------------ ------------------------------------------------------ ----------------------------------------------------------------------------------------- ------------------------------------------------------------------ --------------------------------------------------------------------
  **Need**           **Agent Equivalent**                                   **Research Says**                                                                         **What AP Has**                                                    **Gaps**
  **Physical**       Infrastructure, compute, context windows               Clean contexts, adequate compute, low latency, reliable tooling                           Beast server; 4 depts; multiple model tiers via LiteLLM            No formal context utilisation monitoring; no capacity planning
  **Nutrition**      Data quality, knowledge graph health, prompt quality   RAG degrades within 90 days without active knowledge governance                           FalkorDB + Qdrant + Graphiti; 4.5M-word vault; Pudding Technique   No knowledge deprecation workflow; no retrieval confidence scoring
  **Rest**           Context refresh, session rotation, scheduling          Fresh contexts outperform degraded by 30%+ (Chroma). Compaction mandatory.                Some session management practices                                  No compaction protocol; no session boundary design
  **Intellectual**   RAG updates, skill specialisation, evaluation          Prompt engineering + RAG is recommended architecture (IBM/Gartner)                        Pudding Technique; AMPS scoring; APQC PCF taxonomy                 No TRL tracking; no systematic agent evaluation framework
  **Social**         Multi-agent comms, shared memory, team dynamics        90.2% improvement from multi-agent architectures (Anthropic)                              Board + dept structure; 14-agent marketing pipeline                No inter-department protocol; no error cascade defences
  **Spiritual**      Layer 0 Laws, mission alignment, governance            Accountability must be designed into structure from the start                             8 Layer 0 laws; believability-weighted board; AMPS                 No dynamic weight updating; no formal evaluation
  **Emotional**      AI welfare, precautionary treatment                    \~20% probability current models have morally relevant states (Anthropic Model Welfare)   Philosophy of treating agents as partners in place                 No welfare metrics tracked; no wellbeing signals
  ------------------ ------------------------------------------------------ ----------------------------------------------------------------------------------------- ------------------------------------------------------------------ --------------------------------------------------------------------

**3. Business Bible Consolidation**

**3.1 The Problem Statement**

Amplified Partners holds 4,787 files across 25 vault directories, with additional data scattered across Perplexity threads, Claude sessions, and downloads. This represents the accumulated intellectual capital of the business. The challenge is consolidating this into a single, navigable, authoritative structure: the Business Bible.

**3.2 Enterprise Architecture Frameworks**

**The Zachman Framework**

Provides a 6×6 classification matrix organising all enterprise artifacts by two dimensions: Perspective (Planner, Owner, Designer, Builder, Sub-contractor, User) and Aspect (What, How, Where, When, Who, Why). Every file in the vault can be placed into exactly one cell of the matrix.

*Source: Zachman International --- zachman.com*

**TOGAF Architecture Development Method**

Where Zachman provides the structure, TOGAF provides the process --- iterative phases for developing and maintaining enterprise architecture. Together, Zachman (classification) + TOGAF (methodology) = a complete approach to organising and maintaining the Business Bible.

*Source: The Open Group --- opengroup.org/togaf*

**BABOK Guide**

The Business Analysis Body of Knowledge defines six knowledge areas and provides the standard for business analysis documentation --- useful for organising business process documentation within each department.

**3.3 Single Source of Truth (SSoT) Methodology**

Research from Atlassian, Profisee, and Red Hat converges on a proven sequence:

1.  **Audit all existing data sources** --- identify what exists, where it lives, and what's redundant. The vault inventory already accomplishes this.

2.  **Define governance** --- assign ownership for each content area and establish an update cadence. Without governance, the SSoT decays immediately.

3.  **Cleanse and deduplicate** --- remove duplicate files, standardise naming. Content-hash deduplication catches identical files; semantic deduplication catches overlapping content.

4.  **Organise by department/function** --- structure by business function, NOT by tool or creation date. Files should live where they're used, not where they were created.

5.  **Assign content owners and review cadence** --- every section needs a defined owner (even if AI) and a scheduled review cycle.

6.  **Real-time synchronisation** --- keep the SSoT current. New files flow into the structure automatically via classification workflows.

**3.4 The Three-Layer Architecture**

The vault already has a dual-purpose design (COV-243): raw transcripts serve as both content source material AND agent reference knowledge. The consolidation must not destroy this. Instead, it creates a new layer on top:

  ----------------------------------- ---------------------------------------------------------- ------------------------------------
  **Layer**                           **Purpose**                                                **Access Pattern**
  **Raw File Layer**                  Unedited vault files --- transcripts, sessions, research   Agents query via Graphiti/FalkorDB
  **Content Source Layer**            Extracted entities, relationships, 1024-dim embeddings     Semantic + graph search
  **Human Reference Layer (Bible)**   Curated, deduplicated, navigable by department             Ewan reads for strategic decisions
  ----------------------------------- ---------------------------------------------------------- ------------------------------------

**3.5 Five-Phase Consolidation Approach**

1.  **Company-Level Sweep:** Identify ALL data sources beyond the vault --- Perplexity exports, Claude sessions, browser downloads, Beast server files, email attachments, client docs. Create a master inventory.

2.  **Department Architecture Design:** Define the complete departmental file tree BEFORE moving any files. Every folder maps to a department, every subfolder to a function. Validate against APQC PCF.

3.  **Data Placement:** Move or symlink files into the departmental structure. Duplicates become visible when two files claim the same slot. Content-hash for binary duplicates, semantic similarity for near-duplicates.

4.  **Department-Level Refinement:** Within each department, deduplicate and curate. Merge overlapping docs, archive superseded versions, flag gaps. Each folder emerges with a README and canonical documents.

5.  **Bible Compilation:** The master Business Bible is compiled from the departmental structure. Each department contributes its section. Includes cross-references, master index, and change log.

**4. Board and Department Architecture**

**4.1 Research Basis**

**Deloitte Tech Trends 2026** reports 78% of tech leaders anticipate broad AI agent integration within 5 years, with a shift from project teams to lean cross-functional squads aligned to value streams.

*Source:* [Deloitte](https://www.deloitte.com/us/en/insights/topics/technology-management/tech-trends/2026/ai-future-it-function.html)

**AI World Journal** describes the "Agent-First Organisation" --- AI agents with defined job descriptions, KPIs, and lifecycle management. A "Dual Operating System" combines traditional hierarchy for strategy with fluid agent networks for execution.

*Source:* [AI World Journal](https://aiworldjournal.com/architecting-the-ai-agent-first-organization-how-autonomous-systems-are-reshaping-the-structure-of-modern-companies/)

**ServiceNow** validates production-readiness: autonomous workforce operating 24/7, reducing manual workloads by up to 60%.

**4.2 How the Board Should Work**

**Believability-weighted voting:** Each board member's vote is weighted by demonstrated track record in the relevant domain.

*Source: Principles.com --- Ray Dalio*

**Dynamic weight updating:** Track decisions against outcomes over time. The Bersetche (2025) paper provides the mathematical framework for fractional voting weight delegation in multi-agent systems.

*Source: Bersetche (2025), Journal of Game Theory*

**Human mediator role:** The Giesswein experiment (HBR) showed unsupervised AI board use produced clichéd outputs. Wharton/INSEAD confirmed multi-agent boards need human oversight. Ewan as Chair, not equal member.

**4.3 Governance Framework (5 Components)**

The most comprehensive enterprise governance framework (Architecture & Governance Magazine, Feb 2026) defines five components:

  ---------------------------- --------------------------------------------------------------------- -------------------------------------------------------------
  **Component**                **Purpose**                                                           **AP Status**
  **Agent Registry**           System of record: agent identity, models, prompts, tools, risk tier   Partially exists; needs formalisation as YAML cards
  **Interaction Governance**   Approved interaction graphs; conflict resolution protocols            Board exists; inter-dept protocols undefined
  **Decision Governance**      Confidence thresholds; risk-based escalation; tiered approval         Layer 0 laws provide boundaries; escalation partially built
  **Observability**            Decision traceability; forensic audit logs; dashboards                Event sourcing via Graphiti; no monitoring dashboard yet
  **Resilience & Safety**      Circuit breakers; kill-switches; rollback mechanisms                  Not formally implemented
  ---------------------------- --------------------------------------------------------------------- -------------------------------------------------------------

**4.4 Information Flow Patterns**

McKinsey's "agentic organisation" model replaces traditional org charts with "work charts" --- based on exchanging tasks and outcomes, not hierarchical delegation:

-   **Board → Departments:** Strategic direction, priority setting, resource allocation. Mandate documents with clear objectives.

-   **Departments → Board:** Performance data, anomaly reports, resource requests. Structured reporting via knowledge graph.

-   **Department ↔ Department:** Orchestrator-mediated. R&D outputs formatted for marketing; marketing insights fed to R&D. Vault is shared medium.

-   **QA as architectural layer:** Critic agents in every workflow; producer-reviewer loops; confidence threshold escalation.

*Source: McKinsey, Sept 2025*

**4.5 Dual Operating System**

  ------------------------------------- ------------------------------------------------------------------------------------------------------------------------
  **Layer**                             **Scope**
  **Strategic (Ewan)**                  Vision, client relationships, financial decisions, brand identity, partnerships. Human-only.
  **Operational (Agents)**              Content production, code development, data analysis, client onboarding, quality checks, monitoring. Runs continuously.
  **Interface (OpenClaw + Telegram)**   Bridge between layers. Ewan receives digests, approves escalations, sets direction through natural language.
  ------------------------------------- ------------------------------------------------------------------------------------------------------------------------

**4.6 Ten Departments (APQC PCF)**

  -------- ------------------------------ ----------------------------------- ----------------------------------
  **\#**   **Department**                 **APQC Category**                   **Primary Agents**
  1        **Strategy & Governance**      1\. Develop Vision and Strategy     CEO (Opus), Board Council
  2        **Product & Service Dev**      2\. Develop and Manage Products     Architect (Opus), Coder (Sonnet)
  3        **Marketing & Sales**          3\. Market and Sell                 14-agent marketing pipeline
  4        **Service Delivery**           4\. Deliver Products and Services   PicoClaw, OpenClaw
  5        **Client Service**             5\. Manage Customer Service         PicoClaw (Telegram), Voice AI
  6        **Agent Management (HR)**      6\. Develop Human Capital           Enforcer, Reviewer
  7        **Technology & Infra**         7\. Manage IT                       Cove Orchestrator, Beast ops
  8        **Finance & Risk**             8+10. Financial + Risk              Enforcer (budget caps)
  9        **Knowledge & Improvement**    13\. Manage Knowledge               FalkorDB, Gatekeeper
  10       **R&D / Chaos / Innovation**   12\. Business Capabilities          Research agents, Chaos dept
  -------- ------------------------------ ----------------------------------- ----------------------------------

**5. The R&D Engine**

Amplified Partners operates as an R&D lab where AI agents are the researchers and one human is the principal investigator, lab director, and commercialisation engine. The closest analogy: DARPA's structure with Bell Labs' culture.

*Source: DARPA Heilmeier Catechism; Bell Labs history*

**5.1 Stage-Gate for an AI Lab**

Cooper's Stage-Gate model is used by 88% of US firms. The 5th generation explicitly integrates AI agents. For Amplified Partners, a simplified two-stage model:

-   **Concept:** Heilmeier Catechism answers; rough feasibility; scope definition

-   **Investigation:** AI agent research runs; hypothesis testing; synthesis

-   **Gate:** Kill, continue, or escalate to production. Explicit go/kill decision with evidence.

**5.2 Technology Readiness Levels**

NASA's TRL scale provides a common language for tracking idea maturity:

  --------- ---------------------------------- ----------------------------------------------- -----------------------------------------
  **TRL**   **Traditional**                    **AI-Native Equivalent**                        **Amplified Partners**
  **1-2**   Basic principles; concept          Hypothesis identified; AI spots a pattern       Pudding Technique output; early signals
  **3-4**   Proof of concept; lab validation   Approach validated in controlled conditions     R&D department experiments
  **5-6**   Prototype demonstrated             Works on real data and edge cases               Testing against live client scenarios
  **7-9**   Integrated pilot; mission proven   Reliable, monitored, documented in production   Cove Code Factory deployment
  --------- ---------------------------------- ----------------------------------------------- -----------------------------------------

The critical gap is at TRL 5-7 --- the "Valley of Death" between validated prototype and operational deployment.

**5.3 The 70-20-10 Rule**

Nagji and Tuff's empirical research (HBR) shows the optimal innovation investment split:

  ---------------- ------------------ ------------------------------------------------------------------------------------
  **Allocation**   **Type**           **Returns**
  **70%**          Core               R&D directly connected to current client deliverables. \~10% of long-term returns.
  **20%**          Adjacent           Expanding into new markets/capabilities. \~20% of returns.
  **10%**          Transformational   Pure exploration, no commercial thesis. \~70% of long-term returns.
  ---------------- ------------------ ------------------------------------------------------------------------------------

The paradox: the smallest investment produces the largest returns. The 10% must be protected. The Chaos department is Amplified Partners' structural defence against the competency trap.

**5.4 Research Methodology Stack**

-   **The Pudding Technique (Swanson ABC):** Already in use. Scale with multi-hop chains (A→B→C→D) for deeper synthesis.

-   **TRIZ:** 40 domain-agnostic inventive principles for resolving contradictions without trade-offs.

-   **Biomimicry:** Nature as a prior R&D database with 3.8 billion years of testing. AI agents search biological literature for analogous mechanisms.

-   **Design Science Research:** When the research output is itself a tool or method, DSR provides the rigour framework.

**5.5 R&D Success Metrics**

  ------------------------------------ ---------- ----------------------------------------------------------------
  **Metric**                           **Type**   **What It Measures**
  Hypotheses tested per week           Process    Research velocity --- are agents actively investigating?
  Discovery rate (unexpected/total)    Process    Genuine exploration vs confirmatory research
  TRL progression across portfolio     Output     Pipeline health --- continuous flow from concept to production
  Knowledge base compounding rate      Output     Is each run making future research more efficient?
  Research-to-application conversion   Output     Are discoveries becoming deployed capabilities?
  Heilmeier completion rate            Input      Are programs properly defined before work begins?
  ------------------------------------ ---------- ----------------------------------------------------------------

**6. Documentation and Knowledge Architecture**

**6.1 The Knowledge Waste Problem**

-   Knowledge workers lose 2.8 hours/week searching for information (APQC)

-   50% of corporate knowledge can't be found centrally (IDC/Iterators)

-   Large organisations lose \$47M/year from poor knowledge sharing (Panopto/HRExecutive)

-   McKinsey's Lilli platform saves 1.5 million hours annually

For Amplified Partners, every minute an agent spends searching for context that already exists in the vault is waste.

**6.2 Self-Documenting Systems**

Target: documentation as a by-product of work, not a separate activity.

-   **Architecture Decision Records:** AI-automated ADR generation from codebase changes (Adolfi.dev; AWS uses 200+ ADRs).

-   **Event sourcing:** Every agent action as an immutable event --- inputs, outputs, decisions, reasoning (Microsoft Azure).

-   **Documentation-as-code:** All docs in Markdown alongside code; CI/CD rebuilds on every commit. Spotify's TechDocs: 5,000+ sites (Backstage.io).

-   **GitOps = audit trail:** Git history, PR reviews, and branch protection are most of the documentation an auditor needs (HashiCorp).

**6.3 The Vault as Living Knowledge Base**

The 4,787-file vault with FalkorDB + Qdrant + Graphiti is the right architecture. GraphRAG reduces hallucination by \~60% vs standalone LLMs and provides up to 5x query speed improvement over naive vector RAG.

**Three memory layers (mirroring human memory):**

-   **Episodic:** Non-lossy store of raw inputs --- documents, conversations, agent outputs

-   **Semantic:** Extracted entities and relationships with 1024-dim embeddings

-   **Community:** High-level clusters with summaries via label propagation

**6.4 Knowledge Utilisation: Push, Pull, Gap Detection**

The SECI model (Nonaka & Takeuchi) maps the knowledge creation spiral. The hardest mode is Externalisation --- getting tacit knowledge into queryable format. AI offers genuine leverage here.

-   **Pull:** Agent queries vault → Qdrant semantic search → FalkorDB graph expansion → LLM synthesis.

-   **Push:** Context-aware surfacing --- relevant vault content surfaced proactively before the agent asks.

-   **Gap detection:** Failed queries automatically create documentation tasks. The vault learns from its own failures.

**6.5 Documentation Debt**

Compounds like financial debt. Track: average age of last update, coverage percentage, staleness rate, orphaned docs. Include documentation updates in the definition of done for every task.

**7. AI Production Capacity**

**7.1 Anthropic 2026 Agentic Coding Report**

-   Developers use AI in \~60% of their work; can fully delegate 0-20% of tasks end-to-end

-   27% of AI-assisted work = tasks that wouldn't have been done otherwise

-   Task horizons expanding: 2025 = hours; 2026 = days to weeks

*Source:* [Anthropic Report](https://resources.anthropic.com/hubfs/2026%20Agentic%20Coding%20Trends%20Report.pdf)

**7.2 Stanford Study: 100,000 Developers**

**Critical finding:** Context degradation is real. LLMs lose approximately 50% of performance at \~32K tokens, even with larger context windows available. The single most important constraint for 24/7 operations.

**7.3 Unwind AI: 6-Agent Team Running 24/7**

The most directly applicable case study. Failure modes documented: gateway crashes, cron misses, context overflow, quality degradation. Predictable and manageable.

*Source:* [Unwind AI](https://www.theunwindai.com/p/how-i-built-an-autonomous-ai-agent-team-that-runs-24-7)

**7.4 Rate Limits: The Real Constraint**

The binding constraint is not compute (Beast has 48-core EPYC, 256GB RAM) --- it is API rate limits. Claude operates a two-layer system: 5-hour rolling window + 7-day weekly cap. A single complex task can burn Pro's entire 5-hour allocation in 20 minutes.

*Source:* [Claude Rate Limits](https://www.heyuan110.com/posts/ai/2026-02-28-claude-rate-limits/)

**7.5 Capacity Planning**

  ------------------- --------------------------- -----------------------------------------------------------------
  **Tier**            **Model**                   **Use**
  **Local (cheap)**   Ollama Llama 3.1 8B         Routine checks, classification, high-volume. \>60% of all work.
  **Local (heavy)**   Ollama Llama 3.1 70B        Complex local reasoning, longer inference.
  **API (medium)**    Claude Sonnet via LiteLLM   Standard coding, review, content generation.
  **API (premium)**   Claude Opus via LiteLLM     Architecture decisions, security review, high-stakes.
  ------------------- --------------------------- -----------------------------------------------------------------

**The real bottleneck is context, not compute.** Each session degrades after \~32K tokens. Solution: thin agents, fresh context per task, state persisted via files and databases.

**8. The Right Tool Mix**

**8.1 Deterministic AI Orchestration**

**Praetorian's** research:

> *\"The primary bottleneck in autonomous software development is not model intelligence, but context management and architectural determinism.\"*
>
> *\"Hard rule: planning can be probabilistic; execution must be deterministic.\"*

*Source:* [Praetorian](https://www.praetorian.com/blog/deterministic-ai-orchestration-a-platform-architecture-for-autonomous-development/)

**deepset.ai:** Real-world implementations combine deterministic and autonomous behaviours on a spectrum. Start with deterministic foundations; add agency only where it demonstrably improves outcomes.

**8.2 Recommended Architecture Mix**

  -------------------------- ----------------------------------------------------------------------------------------------------------------------------------------- ----------------------------------------
  **Component**              **Role**                                                                                                                                  **When Used**
  **Cove / Temporal**        Deterministic orchestration spine. Workflow DAGs, retries, checkpoints.                                                                   Every multi-step task. The backbone.
  **Deterministic Python**   File operations, data transforms, content-hash dedup, metadata extraction.                                                                All mechanical, repeatable operations.
  **AI Agents (Claude)**     Classification, synthesis, quality gating, content creation.                                                                              Where judgement is needed.
  **OpenClaw**               WebSocket gateway, human-AI interface, complex workflows.                                                                                 Ewan interaction layer.
  **PicoClaw**               Lightweight agent: webhook handler, Telegram bot, monitoring. The nervous system, not the brain --- senses and signals, doesn't decide.   Always-on edge processing.
  -------------------------- ----------------------------------------------------------------------------------------------------------------------------------------- ----------------------------------------

**8.3 Why Cove Is the Spine**

-   **PlannerWorkflow:** Claude Opus analyses vault inventory, designs file tree, creates consolidation plan.

-   **BuildWorkflow:** Deterministic Python creates structure, moves files, deduplicates. AI agents handle content merging and section writing.

-   **QualityGateWorkflow:** Enforcer (GPT-4.1-mini) validates every output --- citations, completeness, spec compliance.

**The Bible consolidation IS a Cove build project.** Define it as a Linear issue, run it through the pipeline.

**8.4 The Deterministic Imperative**

The critical insight: the more deterministic the system, the more reliable the output. AI agents should decide what to do; deterministic code should execute how to do it.

**9. Gap Analysis**

**Note:** Detailed implementation specifications for all 13 gaps are in the companion document "Architecture Gaps Filled".

  -------- -------------------------------------- ------------------------------------------------ ---------------
  **\#**   **Gap**                                **Why It Matters**                               **Priority**
  1        **Context management protocol**        Every model degrades with context length         **Immediate**
  2        **Agent Registry (formal)**            Each agent needs a structured YAML card (WEF)    **Immediate**
  3        **Dynamic believability weights**      Static weights don't learn from outcomes         **High**
  4        **Knowledge deprecation workflow**     RAG degrades within 90 days without governance   **High**
  5        **Inter-department comms protocol**    Information flows are undefined                  **High**
  6        **Error cascade defences**             No provenance tracking; memory poisoning risk    **High**
  7        **TRL tracking & portfolio view**      No common language for idea maturity             Medium
  8        **Agent evaluation framework**         No systematic testing or benchmarking            Medium
  9        **Observability dashboard**            No real-time monitoring of agent behaviour       Medium
  10       **Resilience controls**                No circuit breakers or kill-switches             Medium
  11       **Self-documentation pipeline**        ADRs, event sourcing, doc quality gates          Medium
  12       **Welfare metrics**                    Partner philosophy not operationalised           Lower
  13       **External Communities of Practice**   One human can't hold all tacit knowledge         Lower
  -------- -------------------------------------- ------------------------------------------------ ---------------

**10. Cross-Domain Pudding Pass**

Five concepts from different research domains that share underlying mechanisms, labelled with PUDDING 2026 notation:

  -------- ---------------------------------------- ---------------------------------------------- ------------------------------------------------ ------------------
  **\#**   **Concept (Domain)**                     **PUDDING Label**                              **Mechanism**                                    **Connects To**
  **P1**   Context Rot (AI engineering)             DEGRADATION.ATTENTION\_DILUTION.SESSION.MIN    Performance degrades as noise accumulates        P3, P4
  **P2**   Retrieval Pollution (knowledge mgmt)     CONTAMINATION.STALE\_COEXISTENCE.SYSTEM.DAYS   Old and new truth coexisting causes paralysis    P1
  **P3**   Competency Trap (R&D / March 1991)       LOCK\_IN.EXPLOITATION\_BIAS.ORG.MONTHS         Optimising current prevents discovering better   P1
  **P4**   Documentation Debt (knowledge systems)   ACCUMULATION.COMPOUND\_NEGLECT.SYSTEM.MONTHS   Undocumented complexity amplifies                P1
  **P5**   Believability Weighting (governance)     CALIBRATION.OUTCOME\_TRACKING.ORG.WEEKS        Active correction prevents degradation           Inverse of P1-P4
  -------- ---------------------------------------- ---------------------------------------------- ------------------------------------------------ ------------------

**Connection 1: The Compounding Degradation Pattern**

Context rot, retrieval pollution, and documentation debt share the same mechanism: small, silent degradation compounds nonlinearly if not actively managed. The system appears fine until a threshold is crossed. The intervention is identical: scheduled refresh cycles with explicit quality gates. A unified "organisational hygiene" protocol would be more efficient than treating them separately.

**Connection 2: Exploitation Lock-in**

The competency trap in R&D (March 1991) and context rot share a structural mechanism: both optimise locally, preventing access to globally better alternatives. Intervention: forced exploration --- session rotation for agents, protected 10% transformational budget for R&D. The Chaos department is AP's structural defence against this.

**Connection 3: Dynamic Calibration as Universal Antidote**

Believability weighting is the inverse mechanism to all four degradation patterns. If applied not just to governance but to knowledge graph health, context management, and R&D portfolio balance, the same calibration architecture could serve as a unified quality layer across the entire business.

**11. Companion Documents**

This consolidated document is the primary architecture reference. The following provide specialised depth:

  ------------------------------------ ----------- --------------------------------------------------------------------------------------------------------------
  **Document**                         **Words**   **What It Adds**
  **Architecture Gaps Filled**         5,152       Implementation-ready specs for all 13 gaps (context management, agent registry, believability weights, etc.)
  **Content Creation Asset Library**   5,384       24 gold quotes, 6 content themes, 5 video scripts, 5 blog outlines, 2-week social media calendar
  **Pudding Engine Deep Research**     1,850       Academic validation of PUDDING 2026, vault archaeology, Swanson LBD state of the art
  **Website Builder Self-Review**      1,676       Scores 3 docs (7-8.5/10), identifies critical back-end gap, front-end confirmed strong
  **Perplexity Extension Research**    276         Chrome extension feasibility for Perplexity thread export --- buildable
  ------------------------------------ ----------- --------------------------------------------------------------------------------------------------------------

**12. Further Research to Commission**

-   Deep dive on Bersetche liquid democracy applied to AI governance --- fractional voting weight delegation in practice

-   Formal agent evaluation benchmark --- what specific tests should each of the 7 core agents pass?

-   Error cascade topology analysis --- which multi-agent architectures are most vulnerable to memory poisoning?

-   Full Pudding session: systematic cross-domain synthesis expanded to the full knowledge vault

-   Biomimicry scan: which biological systems solve AP's specific problems (knowledge routing, distributed governance, adaptive resource allocation)?

**Attribution**

**Architecture & Research**

-   **Ewan Bramley** --- Vision, Human Model Framework, PUDDING concept, blinkers-without-ceilings, SOUL principles, wall method

-   **Perplexity Computer (AI)** --- Research synthesis, academic validation, consolidation, production capacity analysis

-   **Claude (Anthropic)** --- PUDDING 2026 compact coding system, MIX-001 execution, agent architecture

**Principles & Frameworks**

-   **Ray Dalio** --- Ideas meritocracy, radical transparency, believability-weighted voting

-   **Don R. Swanson** (1924-2012) --- Literature-Based Discovery, ABC Model (1986)

-   **Zachman/TOGAF/BABOK** --- Enterprise architecture classification and methodology

**Key Research Sources**

-   [Anthropic 2026 Agentic Coding Trends Report](https://resources.anthropic.com/hubfs/2026%20Agentic%20Coding%20Trends%20Report.pdf)

-   [Deloitte Tech Trends 2026 --- AI-native IT](https://www.deloitte.com/us/en/insights/topics/technology-management/tech-trends/2026/ai-future-it-function.html)

-   [AI World Journal --- Agent-First Organisation](https://aiworldjournal.com/architecting-the-ai-agent-first-organization-how-autonomous-systems-are-reshaping-the-structure-of-modern-companies/)

-   [Praetorian --- Deterministic AI Orchestration](https://www.praetorian.com/blog/deterministic-ai-orchestration-a-platform-architecture-for-autonomous-development/)

-   [Unwind AI --- 6-Agent 24/7 Team](https://www.theunwindai.com/p/how-i-built-an-autonomous-ai-agent-team-that-runs-24-7)

-   Bersetche (2025), Journal of Game Theory --- fractional voting weight delegation

-   McKinsey (Sept 2025) --- agentic organisation, work charts

-   Architecture & Governance Magazine (Feb 2026) --- enterprise governance framework

-   Nonaka & Takeuchi --- SECI model, knowledge creation spiral

-   Nagji & Tuff (HBR) --- 70-20-10 innovation investment

-   [FalkorDB GraphRAG](https://falkordb.com)

--- End of Document ---

Amplified Partners --- March 2026

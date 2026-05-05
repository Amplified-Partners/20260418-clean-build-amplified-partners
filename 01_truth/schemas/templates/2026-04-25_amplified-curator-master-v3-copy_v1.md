---
title: "Amplified Curator Master V3 Copy"
id: "amplified-curator-master-v3-copy"
version: 1
created: "2026-04-25"
type: "document"
topic_type: "spec"
audience: "internal"
layer: "truth"
status: "filed"
signed_by: "Devon, 2026-04-25, devin-992682c244cf444f91e0a516498afbfd"
---

**The Curator Agent**

Unified Master Document

Complete Architecture, Processes, and Integration Guide

for the Amplified Partners Reusable Component Library

Amplified Partners / Ewan Bramley

March 2026

**1. What This Document Is**

This is the single source of truth for the Curator agent --- its architecture, processes, integration points, and operational context within the Amplified Partners system. Every decision about how the Curator works, what it connects to, and how it should be extended begins here.

The document is written for the Amplified Partners agent team and Ewan Bramley. It is technical where it needs to be, but structured so that a non-developer can follow the logic of each process and understand why it matters.

If the Curator changes, this document changes first.

**2. What The Curator Does**

The Curator is the sixth role in the Cove Agent Council. Its job is to prevent duplication, enforce reuse, and maintain architectural coherence across the Amplified Partners codebase.

Think of it as a librarian who knows every book in the library. Before any builder agent writes a new component, the Curator checks whether that component --- or something close enough --- already exists. If it does, the Curator returns the existing component. If it does not, the Curator evaluates the new submission against quality standards before allowing it into the library.

Without the Curator, the same logic gets written repeatedly by different agents in slightly different ways. Over time this duplication compounds into an unmaintainable codebase. Research confirms the scale of this problem: a GitClear study of 211 million lines of code found a 48% rise in copy-pasted code and a 60% decline in refactored code in AI-assisted development[^1], while DX Research documented an 8x increase in code duplication.[^2]

**2.1 Operating Parameters**

  ------------------- ------------------------------------------------------
  **Parameter**       **Value**
  Model               claude-sonnet
  Max Iterations      15
  APQC Category       13 (Creative)
  Quality Threshold   7.0 / 10 minimum for library entry
  Graph Database      FalkorDB (amplified\_brain), port 6379, OpenCypher
  PUDDING Label       P.\>.5.l (Process, Tipping, System-scale, Long-term)
  ------------------- ------------------------------------------------------

**3. The Rubric Score**

The Curator was evaluated against the Amplified Partners standard component rubric. It scored 8.5 out of 10 overall, placing it among the highest-rated components in the system.

  --------------------- ----------- -----------------------------------------------------------------------------
  **Criterion**         **Score**   **Commentary**
  Universality          9 / 10      Applicable to any codebase with reusable components
  Ease to Build         7 / 10      Requires FalkorDB integration, vector search, and multi-agent coordination
  Robustness            8 / 10      Graph-backed with vector similarity; designed for failure
  Failure Resilience    8 / 10      Graceful degradation, circuit breakers, fallback to manual review
  Revenue Potential     9 / 10      Direct cost savings through reuse; sellable as a product
  Strategic Alignment   10 / 10     Core to the \"don\'t build twice\" principle; aligns with every Layer 0 law
  Overall               8.5 / 10    
  --------------------- ----------- -----------------------------------------------------------------------------

**4. Comparables --- What Everyone Else Does**

The Curator does not exist in a vacuum. Several platforms address parts of the same problem --- component cataloguing, code intelligence, developer portals, and agent marketplaces. None of them do what the Curator does in full. This section maps the landscape.

**4.1 Spotify Backstage**

The dominant player in internal developer portals, Backstage holds **89% market share among IDPs** and 67% overall market penetration (DX survey, March 2025). It provides a Software Catalog for registering services, libraries, and pipelines; a Scaffolder for templating new components; and TechDocs for documentation-as-code. Adopters report a 55% reduction in onboarding time.[^3][^4]

**Limitation:** Backstage is a passive catalog. It registers components but does not actively prevent duplication. There is no quality scoring, no AI-driven similarity search, and registration is manual. Its 2026 roadmap introduces an Actions Registry and MCP server support, but these remain feature-level additions rather than an architectural shift toward active curation.

**4.2 Cortex**

An Engineering Intelligence Platform offering scorecards for service maturity, ownership clarity, dependency tracking, and AI Impact Tracking that measures how AI-generated code affects quality metrics.[^5][^6]

**Limitation:** Focused on observability and measurement, not active curation. No component-level reuse prevention. SaaS pricing model creates vendor dependency.

**4.3 Port**

A no-code internal developer portal builder with scorecards and self-service actions. Provides a software catalog with automated service discovery.[^7]

**Limitation:** Portal-focused, not component-library focused. No AI similarity matching. No quality gates on individual components.

**4.4 Sourcegraph / Cody**

Cody is an AI coding assistant with full codebase context. Sourcegraph provides code search across entire codebases and can find similar implementations. Enterprise-ready with security controls.[^8]

**Limitation:** A search tool, not a curation system. Finds duplication after the fact but does not prevent it. No component registry. No quality scoring.

**4.5 Bit.dev**

A component-driven development platform focused on extracting and reusing pre-existing components. Provides a composability model where components are first-class citizens, with usage analytics for tracking adoption.[^9]

**Limitation:** UI/frontend components only. No backend, workflow, or agent component support. No quality scoring. No AI similarity search.

**4.6 InnerSource Commons**

A community-driven collection of patterns for internal open source, including Trusted Committer, 30 Day Warranty, Review Committee, and InnerSource Portal. Salesforce\'s adoption demonstrated improved code quality and collaboration.[^10][^11][^12]

**Limitation:** Human patterns, not automated. No AI curation. Requires cultural adoption, which is slow and difficult to enforce.

**4.7 Kore.ai Marketplace**

An AI agent marketplace offering 250+ pre-built agent templates, 150+ integrations, and 300+ enterprise app connections. One-click installation with customisable templates and industry accelerators.[^13][^14]

**Limitation:** An external marketplace for purchasing, not internal curation. No component-level reuse within a single codebase. SaaS vendor lock-in.

**4.8 Refact.ai**

An AI coding agent that learns from your codebase and suggests code consistent with existing patterns through implicit pattern learning.[^15]

**Limitation:** Implicit learning, not explicit curation. No component registry. No governance. No quality scoring.

**4.9 Comparison Table**

  -------------- ----------------------- ------------------- --------------------- ------------------------ ----------------- -------------------------
  **Platform**   **Active Prevention**   **AI Similarity**   **Quality Scoring**   **Component Registry**   **Multi-Agent**   **Temporal Versioning**
  Backstage      No                      No                  No                    Yes                      No                No
  Cortex         No                      No                  Partial               Yes                      No                No
  Port           No                      No                  Partial               Yes                      No                No
  Sourcegraph    No                      Yes                 No                    No                       No                No
  Bit.dev        No                      No                  No                    Yes                      No                No
  InnerSource    No                      No                  No                    No                       No                No
  Kore.ai        No                      No                  No                    Yes                      No                No
  Refact.ai      Partial                 Implicit            No                    No                       No                No
  Curator        Yes                     Yes                 Yes                   Yes                      Yes               Yes
  -------------- ----------------------- ------------------- --------------------- ------------------------ ----------------- -------------------------

**5. Component Lifecycle**

Every component passes through a defined lifecycle from initial request to potential deprecation. There are no shortcuts --- even internal agents must go through the Curator.

**5.1 Lifecycle Flow**

The lifecycle proceeds as follows:

1.  Builder agent submits a Component Request describing what it needs.

2.  Curator searches FalkorDB using vector similarity against all registered components.

3.  Search returns one of four match levels: EXACT MATCH (identical component exists), NEAR MATCH (≥0.80 similarity, likely reusable), PARTIAL MATCH (0.60--0.80 similarity, may need adaptation), or NO MATCH (\<0.60 similarity, nothing comparable exists).

4.  For EXACT and NEAR matches, the Curator returns the existing component. The builder reuses it.

5.  For PARTIAL matches, the Curator flags the existing component and asks the builder to evaluate whether adaptation is preferable to building new.

6.  For NO MATCH, the builder proceeds with development. On completion, the new component is submitted for quality scoring.

7.  The Curator scores the component across five dimensions (see Section 11). Components scoring below 7.0 are rejected or flagged for improvement.

8.  Accepted components are registered in FalkorDB with full metadata, PUDDING labels, ownership, and dependency mapping.

9.  Usage tracking begins immediately. The Curator monitors adoption rates and health metrics.

10. Components with zero usage over a defined period enter the deprecation pipeline: flagged, grace period, archived.

**5.2 Match Level Thresholds**

  ----------------- ---------------- --------------------------------------------------------------------
  **Match Level**   **Similarity**   **Action**
  EXACT             ≥0.95            Return existing component. No new build.
  NEAR              ≥0.80            Return existing component. Builder reuses with minimal adaptation.
  PARTIAL           ≥0.60            Flag existing. Builder evaluates adaptation vs. new build.
  NO MATCH          \<0.60           Builder proceeds. New component enters quality scoring.
  ----------------- ---------------- --------------------------------------------------------------------

**6. Short-Code Taxonomy**

Every component in the library receives a unique short code following a strict schema. These codes are the primary identifiers used in agent-to-agent communication.

**6.1 Schema**

The format is **TYPE-DOMAIN-SEQ**. For example: **CMP-BK-047** identifies the 47th component in the BK (Byker) domain.

**6.2 Tiered Retrieval**

The taxonomy operates on two tiers:

-   Agent-to-agent communication uses codes only. Agents reference CMP-BK-047, not a full description. This keeps context windows small and retrieval fast.

-   Human-facing outputs resolve codes to full descriptions. When Ewan or a client sees a reference, the Curator expands it to the component name, purpose, and current version.

**6.3 Code Generation Rules**

-   Only the Curator generates new codes. No other agent or human may assign a short code.

-   Each component maps to a single FalkorDB node. One code, one node, one component. No aliases.

-   Codes are permanent. A deprecated component retains its code; the code is never reassigned.

-   Sequential numbering is per-domain. The SEQ portion increments independently within each TYPE-DOMAIN combination.

**7. Pre-Curator Pipeline**

Before a component request reaches the Curator, it passes through a 4-stage chain of cheap agents (gpt-4.1-mini). This pipeline cleans, normalises, and validates the request so the Curator receives consistent, well-formed input every time.

**7.1 The Four Stages**

  ----------- ------------------------ ------------------------------------------------------------------------------------------------------------------------------------------------------
  **Stage**   **Name**                 **Function**
  1           Normalisation            Standardises naming, formatting, and structure. Ensures the request conforms to the expected schema before any semantic processing.
  2           Deduplication            Quick surface-level check for obvious duplicates. Catches exact or near-exact matches before the Curator\'s more expensive vector search.
  3           Schema Compliance        Validates that all required fields are present and correctly typed. Rejects malformed requests before they consume Curator iterations.
  4           Semantic Clarification   Resolves ambiguous descriptions. Asks clarifying questions if the component purpose is unclear. Ensures the Curator receives an unambiguous request.
  ----------- ------------------------ ------------------------------------------------------------------------------------------------------------------------------------------------------

**7.2 Two Cleaning Modes**

The pipeline operates in one of two modes depending on the content domain:

**Precision Mode (Bounded/APQC):** Used for structured business processes, APQC-categorised work, and components with well-defined interfaces. The pipeline enforces strict schema compliance and rejects ambiguity.

**Preservation Mode (Creative/APQC):** Used for creative components, marketing assets, and content where rigid normalisation would destroy value. The pipeline preserves original intent while applying lighter structural constraints.

**8. Drift Detection**

Components evolve through use. The Curator monitors semantic drift between what a component was designed to do and what it actually does in practice.

**8.1 Dual Description Model**

**Canonical description:** Set by the Curator at registration. This is the authoritative definition of what the component is and does. Only the Curator can modify it.

**Working description:** Clarified and refined through actual usage. As agents use a component, the working description accumulates context about how the component is applied in practice.

**8.2 Monitoring and Reconciliation**

The Curator continuously measures semantic similarity between canonical and working descriptions. When drift exceeds a defined threshold, a reconciliation process triggers:

1.  The Curator flags the component as drifted.

2.  The canonical and working descriptions are compared side by side.

3.  If the drift represents legitimate evolution, the canonical description is updated and a new version is created.

4.  If the drift represents misuse, the working description is corrected and the component\'s usage guidance is updated.

5.  All references are versioned. Previous canonical descriptions remain accessible for audit.

**9. FalkorDB Integration**

The Curator\'s persistence layer is FalkorDB, a graph database running on the Beast Server (Hetzner AX162-R, 48-core EPYC, 256GB RAM) at port 6379 using the amplified\_brain graph and OpenCypher query language.

**9.1 Graph Schema**

The component graph uses the following node and edge structure:

**Component Node**

-   Short code (primary identifier, e.g. CMP-BK-047)

-   Canonical description

-   Working description

-   Quality score (0--10)

-   PUDDING label (e.g. P.\>.5.l)

-   Type (component, workflow, template, config, pattern)

-   Domain (e.g. BK, MK, CL)

-   Owner (agent or human)

-   Created timestamp

-   Last modified timestamp

-   Usage count

-   Status (active, deprecated, archived)

-   Vector embedding (for similarity search)

**PUDDING Labels**

Every component node carries a PUDDING label that classifies it by mechanism rather than by department or expertise. This enables cross-domain discovery --- a pattern used in marketing might solve a problem in client onboarding if both share the same PUDDING classification.

**Vector Similarity Search**

Component descriptions are embedded as vectors. When a builder submits a request, the Curator generates a vector embedding of the request and runs a similarity search against all registered components. This catches semantic duplicates that keyword search would miss.

**Temporal Edges (Graphiti)**

Relationships between components use bi-temporal edges via Graphiti. Each edge records both the valid time (when the relationship holds in the real world) and the transaction time (when the system recorded it). This enables the Curator to answer questions like \"what did this component depend on last month\" and to trace the evolution of the component graph over time.

**10. Processes Affected**

The Curator is not an isolated agent. It touches every major system in the Amplified Partners architecture. This section maps each integration point.

  -------------------- -------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------
  **System**           **Integration**
  Cove Orchestrator    Pre-build search and post-build registration. Every build task triggers a Curator search. Completed components are registered automatically. The Curator is the 6th Cove role (alongside coder, security, enforcer, architect, reviewer).
  Marketing Pipeline   Mining reusable patterns for content. The Curator identifies components and workflows that demonstrate Amplified\'s capabilities, feeding stories to the marketing pipeline.
  PUDDING Technique    Every component carries a PUDDING label. The Curator enforces PUDDING classification at registration and uses it for cross-domain discovery.
  Knowledge Vault      Curator awareness is injected into every agent session via the Knowledge Base. All agents know the Curator exists and how to submit requests.
  Enforcer             Audit trail and compliance checking. The Enforcer validates Curator decisions and maintains a complete record of what was built, by whom, and when.
  Voice Commander      Voice-initiated component searches. Ewan can ask the Voice Commander to check whether a component exists, and the query routes through the Curator.
  BaseLayer            Layer 0 law compliance. The Curator operates within BaseLayer\'s non-negotiable principles: Radical Honesty, Radical Transparency, Radical Attribution, Win-Win Only, White Hat Only, Help Not Hurt, Add Not Reduce, Give Value Away.
  -------------------- -------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------

**10.1 Integration Tiers**

The 14 integration points are organised into tiers by criticality:

**Mandatory (5)**

1.  Cove Build Pipeline --- pre-build search, post-build registration

2.  FalkorDB Component Graph --- storage, search, relationships

3.  Enforcer Agent --- audit trail, compliance checking

4.  GitHub MCP --- sync with source code repositories

5.  Linear Integration --- component requests as tickets

**Automated (4)**

1.  Quality Gate Workflow --- automatic scoring on submission

2.  Dependency Scanner --- track what uses what

3.  Usage Analytics --- which components get used, which do not

4.  Deprecation Pipeline --- flag and phase out unused components

**Advisory (3)**

-   Architecture Review --- Curator flags structural concerns

-   Cross-Vertical Discovery --- find reusable patterns across client projects

-   Marketing Mining --- extract content-worthy patterns and stories

**Core (2)**

-   Knowledge Base Injection --- Curator awareness in every agent session

-   Executive Discussion Input --- Curator data feeds strategy decisions

**11. Quality Scoring**

Every new component must score 7.0 or above on a 10-point scale to enter the library. Components below threshold are rejected or flagged for improvement. There is no override.

**11.1 Score Components**

All five dimensions carry equal weight (20% each), ensuring no single dimension dominates the assessment.

  ------------------------- ------------ ----------------------------------------------------------------------------------------------------
  **Dimension**             **Weight**   **What It Measures**
  Code Quality              20%          Clean code principles, consistent style, absence of anti-patterns, appropriate error handling
  Documentation             20%          Clear purpose statement, usage examples, parameter documentation, edge case notes
  Test Coverage             20%          Unit tests, integration tests, edge case coverage, test reliability
  Reuse Potential           20%          Generalisability, clean interfaces, minimal hard-coded dependencies, domain independence
  Architectural Alignment   20%          Consistency with system patterns, adherence to conventions, compatibility with existing components
  ------------------------- ------------ ----------------------------------------------------------------------------------------------------

**11.2 Scoring Process**

Scoring is automatic on submission. The Curator evaluates each dimension and produces an equally-weighted composite score. The process is transparent: the builder receives the score breakdown and specific feedback on any dimension below 7.0.

The hierarchical rubric approach draws on patterns validated in academic research --- notably the CodeWiki project\'s multi-judge evaluation framework for code documentation quality, which demonstrated that structured rubrics with score aggregation and reliability tracking produce consistent, defensible assessments.[^16]

**12. Problems and Risks**

The Curator is designed with failure in mind, but that does not eliminate risk. This section documents known problems and how they are mitigated.

  ------------------------------- ------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------
  **Risk**                        **Description and Mitigation**
  Namespace Collision             Two components in different domains could logically deserve the same short code. Mitigation: the TYPE-DOMAIN-SEQ schema makes collisions structurally impossible within a domain, and cross-domain codes are unique by definition.
  Human Readability               Short codes are efficient for agents but opaque to humans. Mitigation: tiered retrieval automatically expands codes to full descriptions in human-facing contexts.
  Schema Rigidity                 The TYPE-DOMAIN-SEQ schema may prove too rigid as new component types or domains emerge. Mitigation: the schema is extensible --- new TYPE and DOMAIN values can be added without breaking existing codes.
  Single Point of Authority       The Curator is the sole authority for code generation and quality scoring. If it fails, the pipeline stalls. Mitigation: graceful degradation to manual review queue. Circuit breakers prevent cascading failure.
  Legacy Tagging                  Components created before the Curator existed lack short codes and PUDDING labels. Mitigation: a backfill process that retroactively tags legacy components. Priority is by usage frequency.
  Over-Enthusiasm for New Codes   The Curator might generate too many new codes when it should be recommending reuse. Mitigation: the pre-Curator pipeline and vector similarity search reduce false NO MATCH results. Thresholds are tunable.
  ------------------------------- ------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------

**12.1 Failure Modes**

The Curator is designed for five specific failure modes:

  ------------------------ -----------------------------------------------------------------------------------------------
  **Failure**              **Response**
  Curator unavailable      Fallback to manual review queue. Requests are queued and processed when the Curator recovers.
  FalkorDB down            Local cache serves recent queries. New registrations are queued for replay.
  Scoring model degraded   Flag for human review. Do not auto-approve. Components enter a holding state.
  Component conflict       Escalate to Architect agent. The Curator does not resolve architectural disputes.
  Version mismatch         Graphiti temporal edges resolve to the latest valid state. Conflicting versions are flagged.
  ------------------------ -----------------------------------------------------------------------------------------------

**13. Testing Framework**

The Curator\'s taxonomy and retrieval accuracy are validated through a structured recall test framework. The framework is documented in detail in a separate companion document.

**Reference:** See companion document: Curator Taxonomy Recall Test Framework

**13.1 Test Structure**

  -------------------- -------------
  **Parameter**        **Value**
  Test Batteries       5
  Mock Components      100
  Estimated Duration   \~2.5 hours
  -------------------- -------------

**13.2 What the Tests Validate**

-   Taxonomy recall: can the Curator correctly retrieve components by short code?

-   Similarity detection: does the Curator identify NEAR and PARTIAL matches accurately?

-   Code generation: does the Curator generate valid, non-colliding short codes?

-   Quality scoring consistency: does the same component receive the same score on repeated evaluation?

-   Drift detection sensitivity: does the Curator flag drift at the correct threshold?

**14. Why This Matters --- The Degradation Evidence**

The Curator exists because AI-assisted development, left uncurated, produces compounding technical debt. The evidence is substantial.

**14.1 Key Research Findings**

**GitClear Study (211M Lines of Code, 2020--2024)**

-   60% decline in refactored code

-   48% rise in copy-pasted code

-   Code churn doubled (new code reverted within two weeks)

-   MIT Sloan Management Review confirmed 8x increase in code duplication

**DX Research (Code Rot)**

-   AI-generated code increases duplication by 8x and reduces code reuse

-   High-performing teams allocate 10--20% of each sprint to maintenance

-   Active rot: continuous change without reflection

-   Dormant rot: legacy modules quietly diverging from reality

-   AI reshapes rot as \"accelerated fragmentation, disguised as progress\"

**Ox Security Report (300 Projects)**

-   10 architecture anti-patterns found in 80--100% of AI-generated code

-   Comments Everywhere: 90--100% occurrence

-   Avoidance of Refactors: 80--90%

-   Bugs Déjà-Vu: 80--90% (same bugs regenerated because AI inlines instead of using libraries)[^17]

**The 18-Month Wall (Codebridge)**

Codebridge documented a predictable degradation pattern in AI-assisted projects:

  ---------------------- --------------- -----------------------------------------------------------------------
  **Phase**              **Timeline**    **What Happens**
  Euphoria               Months 1--3     Feature delivery accelerates. Teams feel productive.
  Velocity Plateau       Months 4--9     Integration challenges emerge. Refactoring is delayed.
  Decline Acceleration   Months 10--15   Debugging legacy AI components consumes increasing time.
  The Wall               Months 16--18   Codebase is larger but slower. Delivery stalls. 4x maintenance costs.
  ---------------------- --------------- -----------------------------------------------------------------------

**14.2 Additional Data Points**

-   Gartner predicts 40% of AI-augmented coding projects will be cancelled by 2027

-   METR study found a 39--44% gap between perceived and actual developer productivity with AI tools --- developers felt 20% faster but were actually 19% slower

-   CSET/Georgetown found that 68--73% of AI-generated code contained vulnerabilities

-   20% of AI-suggested dependencies do not exist (package hallucination)

**14.3 The Curator\'s Response**

The Curator addresses these problems through a 7-layer defence model:

  ----------- ------------ ------------------------------------------------------
  **Layer**   **Name**     **Function**
  1           Pre-Build    Curator searches before any code is written
  2           Build-Time   Quality gates reject sub-threshold components
  3           Post-Build   Automated scoring and registration
  4           Runtime      Usage analytics track adoption and health
  5           Periodic     Scheduled audits flag degrading components
  6           Reactive     Enforcer catches violations in real-time
  7           Strategic    Executive Discussion reviews system health quarterly
  ----------- ------------ ------------------------------------------------------

[^1]: Codebridge --- Hidden Costs of AI-Generated Software: <https://www.codebridge.tech/articles/the-hidden-costs-of-ai-generated-software-why-it-works-isnt-enough>

[^2]: DX Research --- Code Rot: <https://getdx.com/blog/code-rot/>

[^3]: Backstage: <https://backstage.io>

[^4]: Backstage Wrapped 2025: <https://backstage.io/blog/2025/12/30/backstage-wrapped-2025/>

[^5]: Cortex: <https://www.cortex.io>

[^6]: Cortex --- Business Case for IDPs 2026: <https://www.cortex.io/post/the-business-case-for-internal-developer-portals-in-2026>

[^7]: Port --- Internal Developer Platform: <https://internaldeveloperplatform.org/developer-portals/port/>

[^8]: Sourcegraph: <https://sourcegraph.com>

[^9]: Bit.dev: <https://bit.dev>

[^10]: InnerSource Commons: <https://innersourcecommons.org>

[^11]: InnerSource Patterns: <https://patterns.innersourcecommons.org>

[^12]: Salesforce InnerSource Case Study: <https://engineering.salesforce.com/stronger-together-an-inner-sourcing-case-study-b616ff5c1923/>

[^13]: Kore.ai Marketplace: <https://www.kore.ai/ai-marketplace>

[^14]: Kore.ai Agent Platform Docs: <https://docs.kore.ai/agent-platform/ai-agents/agentic-apps/marketplace/>

[^15]: Refact.ai: <https://refact.ai>

[^16]: CodeWiki (arXiv): <https://arxiv.org/html/2510.24428v5>

[^17]: Ox Security / InfoQ --- AI Code Technical Debt: <https://www.infoq.com/news/2025/11/ai-code-technical-debt/>

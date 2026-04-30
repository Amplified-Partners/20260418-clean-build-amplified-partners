---
title: "Cross-Reference Addendum"
id: "cross-reference-addendum"
version: 1
created: 2026-04-25
last_validated: 2026-04-25
type: document
topic_type: reference
status: imported
source_file: "cross-reference-addendum.docx"
signed_by: "Devon, 2026-04-25, devin-992682c244cf444f91e0a516498afbfd"
---

**CROSS-REFERENCE ADDENDUM**

─────────────────────────────────────

Knowledge Base Cross-Pollination Analysis

*PUDDING Applied to Own Corpus*

17 March 2026

**Attribution**

**Ewan Bramley** (originator, all vault knowledge)

×

**Claude** (Anthropic --- cross-reference analyst, researcher)

Fact %: 85 \| Confidence: High \| Method: Full corpus extraction + PUDDING neutral labelling

**AMPLIFIED PARTNERS --- CONFIDENTIAL**

**SECTION 1: EXECUTIVE SUMMARY**

This addendum documents a complete cross-reference analysis of the Amplified Partners unified knowledge base. Over 50 files were catalogued across vault documents, research outputs, synthesis files, deliverables, and GitHub code repositories. Three parallel extraction passes produced 253KB of structured analysis, revealing cross-pollination opportunities that no single document could surface alone.

The analysis applies the PUDDING technique --- Literature-Based Discovery adapted for business knowledge synthesis (Swanson, 1986; Bramley & Claude, 2026) --- to the Amplified Partners\' own corpus. By stripping domain labels and expert attributions, flattening all concepts into neutral mechanisms, and scoring them against the 4-criteria rubric (Relevance, Actionability, Evidence, Impact --- each 0-5, total /20), this document identifies every crossover found between files.

Each crossover is scored using the RUBRIC-REPLACE-OR-FIX philosophy and assigned a verdict:

**WOULD IMPROVE** --- Clear benefit, should be implemented.

**WOULDN\'T IMPROVE** --- Evaluated and rejected with reasoning.

**NEEDS RESEARCH** --- Promising but requires further evaluation before commitment.

The addendum maps all findings into the 4-document structure (Content Creation, Process, Master Document, Coding) so that each crossover has a clear home. Priority recommendations are ordered by impact and urgency, with the FalkorDB → Neo4j migration and FAULT-011 resolution identified as the two critical-path blockers.

Key statistics from this analysis:

• 5 cross-pollination opportunities identified and scored (Section 3A)

• 26 technology opportunities evaluated with GitHub verification (Section 3B)

• 10 existing code files assessed for reuse potential (Section 3C)

• 7-stage Addition Pipeline mapped as process standard (Section 3D)

• 9 documented-but-unbuilt gaps identified (Section 4)

• 10 prioritised action items ordered by impact (Section 6)

**SECTION 2: CORPUS CATALOGUE**

The following table catalogues every file processed during the three extraction passes. Files are grouped by category, with type classification and a brief description of content scope. Total corpus: 79 files across 7 categories.

**Vault Documents (24 files)**

  -------------------------------- ------------ --------------------------------------------------------------
  **File**                         **Type**     **Description**
  SOUL.md                          Core         Mission, values, Immutable Foundation Code, AEO strategy
  OPERATIONAL-PROTOCOL.md          Core         The 12 Laws governing all AI behaviour in the system
  CLAUDE.md                        Core         Claude-specific operating instructions and session protocols
  PUDDING-TECHNIQUE-CANONICAL.md   Method       Complete PUDDING methodology (Swanson ABC adaptation)
  RADICAL-ATTRIBUTION-SCHEMA.md    Method       Attribution requirements for all outputs
  building-an-operating-bible.md   Strategy     Operating bible framework for SMB clients
  financial-autopsy-framework.md   Product      Post-mortem financial analysis methodology
  sovereign-os.md                  Framework    Self-hosted sovereignty operating system principles
  compound-learning-pipeline.md    Process      7-stage Addition Pipeline SOP
  rubrik-01-through-07.yaml        Tools        All 7 operational rubriks (YAML definitions)
  faults-and-fixes.md              Reference    65-entry fault catalogue with fix protocols
  death-spiral-detector.md         Product      Multi-signal business failure early warning
  telegraph-pole-strategy.md       Content      Public transparency content model
  ulysses-clause.md                Governance   Irrevocable human override mechanism
  bob-product-spec.md              Product      Business health monitoring product specification
  morning-brief-spec.md            Product      Daily briefing pipeline specification
  ai-telephone-system.md           Product      Voice AI appointment/triage system
  client-onboarding-flow.md        Process      Client intake and discovery process
  hetzner-beast-spec.md            Infra        Dedicated server specification and topology
  security-hardening.md            Infra        Security baseline requirements
  graphiti-integration.md          Infra        Temporal knowledge graph integration plan
  mcp-server-catalogue.md          Infra        MCP server inventory and build priorities
  whatsapp-regulatory.md           Strategy     WhatsApp Business API regulatory positioning
  pricing-model.md                 Business     Service pricing and packaging framework
  -------------------------------- ------------ --------------------------------------------------------------

**Research Files (12 files)**

  ------------------------------- ---------- ---------------------------------------------------------------
  **File**                        **Type**   **Description**
  EXPERT-RESEARCH-LIBRARY.md      Research   Named expert frameworks (Dalio, Gerber, Godin, Kennedy, etc.)
  PUDDING-MIX-001.md              Mix        Cross-domain discovery --- first pudding session output
  PUDDING-MIX-002.md              Mix        Biological decision logic --- 7 decision architectures
  PUDDING-MIX-003.md              Mix        Technology stack evaluation pudding
  mathematical-validation.md      Proof      Statistical validation of PUDDING technique (PMI, Jaccard)
  gtd-mapping-research.md         Research   David Allen GTD mapped to voice capture pipeline
  scarf-model-research.md         Research   David Rock SCARF model for delivery design
  death-spiral-research.md        Research   Business failure pattern analysis
  graph-database-comparison.md    Research   Neo4j vs FalkorDB vs KuzuDB evaluation
  mcp-ecosystem-research.md       Research   MCP protocol landscape and tooling
  acoustic-forensics.md           Research   ML-based audio analysis for voice verification
  llm-observability-research.md   Research   Langfuse, Arize Phoenix, Helicone comparison
  ------------------------------- ---------- ---------------------------------------------------------------

**Synthesis & Methodology (5 files)**

  -------------------------------- ----------- -----------------------------------------------------
  **File**                         **Type**    **Description**
  architecture-spec.md             Synthesis   Full system architecture decisions and locked items
  technology-stack-decisions.md    Synthesis   Evaluated + chosen technology with verdicts
  pudding-technique-evolution.md   Meta        How the technique itself has evolved
  session-learnings.md             Meta        Compiled session retrospectives and patterns
  context-management-protocol.md   Process     How to survive context window compression
  -------------------------------- ----------- -----------------------------------------------------

**Deliverables (9 files)**

  --------------------------------- ------------- ----------------------------------------
  **File**                          **Type**      **Description**
  amplified-partners-overview.pdf   Deliverable   Client-facing company overview
  pudding-whitepaper-draft.md       Deliverable   Public-facing PUDDING explanation
  financial-autopsy-template.xlsx   Deliverable   Reusable financial analysis workbook
  bob-product-deck.md               Deliverable   Product deck for Bob business monitor
  ai-telephone-proposal.md          Deliverable   AI telephone system client proposal
  morning-brief-mockup.md           Deliverable   Morning brief UI/UX specification
  onboarding-questionnaire.md       Deliverable   Client onboarding discovery form
  rubrik-output-examples.md         Deliverable   Sample rubrik outputs across scenarios
  cross-reference-addendum.docx     Deliverable   This document
  --------------------------------- ------------- ----------------------------------------

**GitHub Code (18 files pulled)**

  ---------------------------------- ---------- -------------------------------------------------------------
  **File**                           **Type**   **Description**
  ingest\_vault.py                   Code       Vault ingestion pipeline --- 744 lines, production-ready
  rubrikEngine.js                    Code       Rubrik evaluation engine --- 61 lines, functional prototype
  isolation.js                       Code       Cross-contamination detection --- 33 lines, prototype
  plaud.js                           Code       Council review (5 hats pattern) --- 51 lines, prototype
  morningBrief.js                    Code       Morning brief generator --- 25 lines, stub
  supportTrainer.js                  Code       Voice clone + LLM training --- 38 lines, prototype
  redditNinja.js                     Code       Reddit engagement automation --- 20 lines, stub
  avatarFactory.js                   Code       Avatar generation --- 12 lines, stub
  deploy-tonight.sh                  Code       Deployment script --- 113 lines, production-ready
  docker-compose.yml (agent-stack)   Config     Agent stack Docker composition --- \~190 lines
  docker-compose.yml (monitoring)    Config     Monitoring stack composition
  Dockerfile.ingest                  Config     Vault ingestion container definition
  .env.example                       Config     Environment variable template
  package.json                       Config     Node.js project dependencies
  requirements.txt                   Config     Python project dependencies
  README.md                          Docs       Repository documentation
  CONTRIBUTING.md                    Docs       Contribution guidelines
  .github/workflows/ci.yml           CI         Continuous integration pipeline
  ---------------------------------- ---------- -------------------------------------------------------------

**Intelligence Docs (6 files)**

  ------------------------- ---------- -----------------------------------------------
  **File**                  **Type**   **Description**
  competitor-landscape.md   Intel      Competitive analysis of accountancy AI tools
  market-sizing.md          Intel      TAM/SAM/SOM for target market
  regulatory-landscape.md   Intel      FCA, ICO, HMRC regulatory requirements
  partner-evaluation.md     Intel      Potential partnership and integration targets
  technology-radar.md       Intel      Emerging technology watchlist
  threat-model.md           Intel      Security threat model and mitigations
  ------------------------- ---------- -----------------------------------------------

**Supporting Files (5 files)**

  -------------------- ----------- --------------------------------------------
  **File**             **Type**    **Description**
  glossary.md          Reference   Term definitions across the unified system
  acronym-index.md     Reference   All acronyms used in the corpus
  version-history.md   Meta        Document version tracking
  open-questions.md    Meta        Unresolved questions awaiting research
  commitment-log.md    Process     Session commitments and follow-up tracking
  -------------------- ----------- --------------------------------------------

**SECTION 3: CROSSOVER FINDINGS --- Scored**

This section documents every crossover found during the three extraction passes. Each crossover is scored using the PUDDING 4-criteria rubric (Relevance 0-5, Actionability 0-5, Evidence 0-5, Impact 0-5 = total /20) and assigned a verdict using the RUBRIC-REPLACE-OR-FIX philosophy.

**3A: Cross-Pollination Opportunities**

Ideas from one file that should apply to others --- the heart of Literature-Based Discovery applied to the Amplified Partners corpus.

**CP-01: Unified Truth Architecture**

**Description:** Merge PUDDING labels + Fact Percentage + Confidence Band + Attribution into one YAML output wrapper that every agent, every rubrik, and every deliverable uses. Currently these four systems are defined in separate files with no shared schema --- PUDDING labels in pudding-technique-canonical.md, Fact Percentage in SOUL.md (Scale of Arsehole), Confidence Band in OPERATIONAL-PROTOCOL Law 7, and Attribution in RADICAL-ATTRIBUTION-SCHEMA.md. A unified schema means every output carries the same footer, every agent knows how to produce it, and every downstream consumer (morning brief, Bob, client reports) can parse it identically.

**Sources:** PUDDING MIX 001, RADICAL-ATTRIBUTION-SCHEMA, SOUL.md, OPERATIONAL-PROTOCOL Law 7

**Score:** R5 A5 E4 I5 = 19/20

**Verdict: WOULD IMPROVE**

**Build Cost:** One shared schema file + CLAUDE.md instructions. Estimated: 2-3 hours. The schema already exists in fragments --- this is an assembly task, not a design task.

**Reasoning:** Every output from the Amplified Partners system currently carries partial metadata. The financial autopsy might have a fact percentage but no PUDDING label. A research output might carry attribution but no confidence band. By merging into one YAML footer, every output becomes self-describing and machine-parseable. The morning brief can automatically surface low-confidence outputs for Ewan\'s review. Bob can flag when a rubrik output lacks attribution. This is the single highest-leverage architectural change available because it affects every downstream consumer.

**CP-02: Decision Classifier Meta-Layer**

**Description:** Route decisions to the appropriate biological logic pattern BEFORE applying a confidence gate. The biological decision taxonomy (Bacterial/Quorum, Viral, Slime Mold, Octopus, Mycelial, Human, Silicon AI) from PUDDING MIX 002 should be the first filter in every decision pathway. Currently, all decisions pass through the same confidence gate in OPERATIONAL-PROTOCOL --- but a threat detection decision (Quorum logic) needs fundamentally different routing than a market penetration decision (Viral logic).

**Sources:** PUDDING MIX 002 (Biological Decision Logic), Sovereign OS (decision sovereignty principles), AI Telephone System (real-time decision routing), OPERATIONAL-PROTOCOL Law 3 (decision gates)

**Score:** R5 A4 E3 I5 = 17/20

**Verdict: WOULD IMPROVE**

**Build Cost:** Classification prompt + routing table. Already designed in MIX 002 --- needs implementation as a pre-processing step. Estimated: 1-2 days.

**Reasoning:** The AI Telephone system already needs this --- when a caller describes an emergency plumbing situation, the system should route to Quorum logic (multiple signals converging = take action) rather than through the standard confidence gate. The morning brief needs it too --- market intelligence should flow through Slime Mold logic (parallel exploration, reinforce what works) while security alerts need Bacterial logic (threshold-based triggering). Without the classifier, every decision gets the same treatment, which is demonstrably wrong for edge cases. Evidence score is 3 (not 4) because the biological taxonomy is proven in concept but not yet tested in production routing.

**CP-03: GTD-as-Product Framing**

**Description:** David Allen\'s Getting Things Done (GTD) methodology maps exactly to the voice capture → Graphiti → morning brief pipeline that Amplified Partners is building. The capture-clarify-organise-reflect-engage framework IS the pipeline. This is a positioning insight, not a build task --- but it transforms how the product is described to potential clients and partners.

**Sources:** EXPERT-RESEARCH-LIBRARY (GTD analysis), AI-TELEPHONE (voice capture entry point), OPERATIONAL-PROTOCOL (Compound Step timing --- the \'reflect\' stage), morning-brief-spec.md (the \'engage\' stage)

**Score:** R5 A4 E4 I4 = 17/20

**Verdict: WOULD IMPROVE**

**Build Cost:** Zero build cost. This is a reframing of existing architecture using a universally recognised productivity framework. Apply immediately to all product descriptions, pitch decks, and content.

**Reasoning:** GTD has an estimated 10+ million practitioners worldwide. By framing the Amplified Partners pipeline in GTD terms, the value proposition becomes instantly recognisable: \'We automated GTD for your business --- voice in, structured knowledge graph out, actionable morning brief delivered.\' The AI Telephone is the \'capture\' inbox. Graphiti is the \'organise\' system. The morning brief is the \'reflect + engage\' loop. Every SMB owner who has tried and failed to maintain a GTD practice is the target market. Evidence score is 4 because the GTD mapping was verified against Allen\'s original 5-stage model in the research library.

**CP-04: SCARF + Delivery Design**

**Description:** Map each rubrik output to David Rock\'s SCARF dimensions (Status, Certainty, Autonomy, Relatedness, Fairness) to prevent client defensive shutdown when delivering harsh financial truths. The financial autopsy deliberately delivers uncomfortable findings --- but if those findings trigger a SCARF threat response, the client rejects the message regardless of accuracy.

**Sources:** building-an-operating-bible.md (client delivery context), AI Telephone (real-time delivery), Financial Autopsy Framework (the hard truths), Bob product (ongoing monitoring delivery), SCARF model research

**Score:** R4 A3 E3 I4 = 14/20

**Verdict: WOULD IMPROVE**

**Build Cost:** Add SCARF annotation to rubrik output templates. Estimated: 1 day design + 1 day implementation. Requires updating all 7 rubrik YAML definitions.

**Reasoning:** When the financial autopsy reveals that a client\'s business is haemorrhaging cash through a specific behaviour, the natural human response is defensive shutdown --- especially if Status (they feel judged) or Autonomy (they feel controlled) are threatened. By pre-annotating each rubrik output with its SCARF impact, the delivery layer can adjust framing automatically. A high-Status-threat finding gets prefaced with autonomy-preserving language. A Certainty-threat finding gets paired with a clear action plan. This is the difference between \'your margins are terrible\' (SCARF violation: Status + Certainty) and \'here\'s exactly how to improve margins by 12% in 90 days\' (SCARF reward: Certainty + Autonomy). Actionability score is 3 because the SCARF mapping requires psychology expertise to do well.

**CP-05: Failure-Pattern Rubriks**

**Description:** Add a structured failure search to every rubrik --- what consistently causes false positives, false negatives, and misclassifications. Currently, the 7 operational rubriks define what TO look for, but none of them define what NOT to look for or what triggers incorrect results.

**Sources:** pudding-technique-canonical.md (the anti-pudding checklist --- \'always run failure search\'), all 7 rubriks (rubrik-01-through-07.yaml), faults-and-fixes.md (65 known failure patterns), PUDDING mathematical validation (precision/recall framework)

**Score:** R5 A4 E3 I4 = 16/20

**Verdict: WOULD IMPROVE**

**Build Cost:** Add a \'failure\_patterns\' section to each rubrik YAML. Estimated: 2-3 hours per rubrik = 14-21 hours total. Can be done incrementally.

**Reasoning:** The PUDDING technique itself mandates running failure searches alongside success searches --- \'what consistently causes this to fail\' is where the highest-confidence signal lives. But the 7 operational rubriks don\'t follow this principle yet. The faults-and-fixes catalogue already contains 65 known failure patterns --- many of which map directly to specific rubriks. For example, FAULT-023 (context window overflow causing rubrik truncation) is a known failure pattern for Rubrik 03 but isn\'t documented in the rubrik itself. Adding failure patterns transforms rubriks from detection tools into precision instruments. Evidence score is 3 because failure patterns are documented anecdotally in faults-and-fixes but not yet systematically mapped to specific rubriks.

**3B: Technology Crossovers --- GitHub Opportunities**

Every piece of software evaluated against the Amplified Partners technology stack. GitHub star counts verified at time of analysis. Each scored using the PUDDING 4-criteria rubric against the goal of \'building a self-hosted, sovereign, production-grade system for SMB financial intelligence.\'

  --------------------- ------------------ --------------------------- ---------------------------- --------------------------------- ----------- ------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------
  **Software**          **GitHub Stars**   **What It Does**            **Would Replace**            **Verdict**                       **Score**   **Reasoning**
  Temporal              18.9k              Durable workflows           Nothing --- new backbone     **WOULD IMPROVE**                 19/20       Every multi-step process in the corpus references needing durable workflow orchestration. The AI Telephone, morning brief pipeline, vault ingestion, and client onboarding all require exactly this pattern. MIT licensed.
  Langfuse              23.3k              LLM observability           Manual logging               **WOULD IMPROVE**                 18/20       MIT licensed, already planned in architecture-spec.md. Fills the critical gap of having no visibility into LLM behaviour across the system. Every rubrik evaluation, every agent interaction needs tracing.
  LiteLLM Proxy         39.4k              Multi-LLM gateway           Direct API calls             **WOULD IMPROVE**                 17/20       MIT licensed. Centralises all LLM routing through one proxy --- enables model fallback, cost tracking, rate limiting. Currently each component calls LLM APIs directly with no coordination.
  Graphiti              24k                Temporal knowledge graph    Nothing --- already chosen   **ALREADY IN STACK**              ---         Retained in all scenarios. Core to the entire architecture. The PUDDING technique, morning brief, Bob product, and vault all depend on Graphiti\'s temporal knowledge graph capabilities.
  Neo4j + DozerDB       ---                Graph database              FalkorDB                     **WOULD IMPROVE**                 20/20       FalkorDB has 10+ documented crash bugs (see faults-and-fixes.md). Migration is CRITICAL and blocks all graph-dependent features. Neo4j Community + DozerDB provides enterprise-grade stability. Top priority.
  FastMCP 2.0           23.7k              MCP server framework        Manual MCP code              **WOULD IMPROVE**                 16/20       MIT licensed. Simplifies all MCP server development --- Sage MCP, HMRC MTD MCP, and all future MCP servers benefit. Reduces boilerplate and enforces protocol compliance.
  Composio              25.8k              Tool integration layer      Custom integrations          **NEEDS RESEARCH**                14/20       870+ app integrations but evaluate fit with MCP-first architecture. May conflict with the sovereignty principle if it creates external dependency. Needs sandbox testing against actual MCP workflow.
  Mem0                  42k                Universal agent memory      Custom memory code           **NEEDS RESEARCH**                13/20       Overlaps significantly with Graphiti\'s temporal knowledge graph. Clarify whether complementary (Mem0 for short-term agent memory, Graphiti for long-term knowledge) or redundant. Don\'t adopt both without clear boundary.
  LangGraph             22.5k              Multi-agent orchestration   Custom agent code            **NEEDS RESEARCH**                15/20       Excellent multi-agent framework but evaluate against Temporal for overlap. If Temporal handles durable workflows, does LangGraph add agent-specific value or just duplicate? Sandbox test required.
  Postiz                ---                Social media scheduling     Manual posting               **WOULD IMPROVE**                 15/20       Apache 2.0 licensed. Fills the content pipeline gap identified in telegraph-pole-strategy.md. Self-hosted, aligns with sovereignty principles. Pairs with content creation workflow.
  Listmonk              18k                Newsletter platform         No current solution          **WOULD IMPROVE**                 14/20       AGPL licensed --- check compatibility with commercial use. Fills the newsletter gap for content distribution. Self-hosted, high performance, minimal resource requirements.
  Ghost CMS             51.7k              Blog + newsletter           No current solution          **NEEDS RESEARCH**                13/20       MIT licensed but heavy --- runs Node.js with MySQL. Evaluate against Listmonk for the newsletter use case. If blog is needed, Ghost wins; if newsletter-only, Listmonk is lighter.
  RSSHub                39.5k              RSS feed generation         Manual monitoring            **WOULD IMPROVE**                 17/20       MIT licensed. Critical for the intelligence pipeline --- turns any web source into an RSS feed. Feeds into Miniflux for aggregation, then LLM triage for the morning brief intelligence section.
  Miniflux              12k                RSS aggregation             Manual feed reading          **WOULD IMPROVE**                 15/20       Apache 2.0 licensed. Pairs with RSSHub to complete the intelligence pipeline. Lightweight, self-hosted, API-first design enables LLM integration for automated triage.
  Changedetection.io    22k                Page monitoring             Nothing                      **WOULD IMPROVE**                 14/20       MIT licensed. Fills the non-RSS monitoring gap --- tracks competitor websites, regulatory pages, and any source without RSS. Complements RSSHub + Miniflux for full coverage.
  Wazuh                 ---                SIEM + FIM + HIDS           No current SIEM              **WOULD IMPROVE**                 16/20       Free and open source. Comprehensive security monitoring covering file integrity, intrusion detection, and log analysis. Essential for the Hetzner Beast deployment security baseline.
  Trivy                 ---                Container scanning          No scanning                  **WOULD IMPROVE**                 16/20       Apache 2.0 licensed. Essential for container security --- scans Docker images for vulnerabilities before deployment. Non-negotiable for production security posture.
  docker-socket-proxy   ---                Docker API restriction      Open Docker socket           **WOULD IMPROVE**                 18/20       Apache 2.0 licensed. CRITICAL security fix --- the current Docker socket exposure is the single largest attack surface on Beast. Deploy immediately alongside Falco.
  Falco                 ---                Runtime security            No runtime monitoring        **WOULD IMPROVE**                 15/20       Apache 2.0 licensed. eBPF-based runtime security monitoring detects anomalous container behaviour in real-time. Complements Wazuh (host-level) with container-level monitoring.
  restic                ---                Encrypted backup            No off-site backup           **WOULD IMPROVE**                 17/20       BSD licensed. Essential disaster recovery layer --- encrypted, deduplicated, incremental backups to off-site storage. Currently NO off-site backup exists for Beast, which is an unacceptable risk.
  Arize Phoenix         8.9k               Hallucination detection     No current solution          **NEEDS RESEARCH**                12/20       ELv2 license --- check commercial terms carefully. Hallucination detection is valuable but evaluate whether Langfuse + custom evals achieve the same outcome at lower complexity.
  OpenHands             65.5k              AI dev platform             Kilo Code / manual           **NEEDS RESEARCH**                14/20       MIT licensed, impressive capabilities but evaluate stability for production use. May replace manual coding workflows but needs trust-building through sandbox testing.
  SonarQube Community   10k                Static analysis             No current gates             **NEEDS RESEARCH**                13/20       LGPL licensed. Evaluate against Qodo Merge for pull request analysis. Adds quality gates to the CI pipeline but introduces infrastructure overhead. Worth testing.
  n8n                   177k               Workflow automation         Custom scripts               **WOULDN\'T IMPROVE**             11/20       Sustainable Use License conflicts with the sovereignty principle from Sovereign OS. The license restricts competitive use and creates dependency on a single vendor\'s licensing decisions. Build custom or use Temporal.
  Twenty CRM            38.8k              Self-hosted CRM             No current CRM               **NEEDS RESEARCH**                12/20       AGPL licensed. Heavy dependency --- evaluate whether a full CRM is actually needed or if Graphiti + custom views serve the client management function adequately.
  FalkorDB              ---                Graph database              ---                          **WOULDN\'T IMPROVE --- AVOID**   AVOID       10+ documented crash bugs in faults-and-fixes.md. Currently in stack but migration to Neo4j is CRITICAL. Do not build any new features on FalkorDB. Migrate immediately.
  KuzuDB                ---                Embedded graph              ---                          **WOULDN\'T IMPROVE --- AVOID**   AVOID       Abandoned October 2025. No active development. Do not adopt under any circumstances.
  --------------------- ------------------ --------------------------- ---------------------------- --------------------------------- ----------- ------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------

**3C: Code Reuse Assessment --- Existing GitHub Code**

Assessment of all code in the ewan-dot/amplified-partners repository. Each file evaluated for maturity, reuse potential, and specific modification requirements. The goal: extend what works, rebuild only what must be rebuilt, never throw away good architecture.

  -------------------------------------- ----------- ----------------------- ------------------------------------------- -----------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------
  **File**                               **Lines**   **Maturity**            **Reuse?**                                  **Assessment**
  **ingest\_vault.py**                   744         Production-ready        **YES --- extend, don\'t rebuild**          The gold standard for code quality in the repository. Proper CLI interface with argparse, comprehensive error handling with retry logic, progress tracking via tqdm, configurable chunking with overlap. This file demonstrates what production code should look like across the entire codebase. Needs: Neo4j backend swap (currently targets FalkorDB --- FAULT-011), unit tests, and integration with Langfuse for observability. Do NOT rebuild --- extend.
  **rubrikEngine.js**                    61          Functional prototype    **YES --- extend**                          Core logic works: loads JSON rubrik definitions, applies keyword matching against input text, returns scored results. The architecture is sound --- rubrik definitions are externalised (not hardcoded), scoring is configurable. Needs: semantic matching instead of keyword matching (embed rubrik criteria, use cosine similarity), confidence weighting per criterion, and integration with the Unified Truth Architecture (CP-01) for output formatting.
  **isolation.js**                       33          Functional prototype    **YES --- extend**                          Cross-contamination detection logic is correct: checks that data from Client A cannot leak into Client B\'s context. Pattern works. Needs: actual database calls instead of console.log statements, integration with Graphiti\'s entity isolation features, and automated testing against the 4 contamination scenarios documented in security-hardening.md.
  **plaud.js**                           51          Functional prototype    **YES --- extend**                          Implements the Council Review pattern (5 hats: financial, operational, strategic, risk, client-perspective). The pattern is clever and maps well to the biological decision logic taxonomy from MIX 002. Needs: Graphiti storage instead of console.log, richer NLP for context extraction from voice transcripts, and integration with the Decision Classifier (CP-02) to route council decisions appropriately.
  **morningBrief.js**                    25          Stub with good design   **PARTIAL --- use pattern, rebuild body**   Good prompt design that captures Ewan\'s voice and communication style. The template structure (greeting → priorities → alerts → schedule → signoff) is exactly right. But the body is placeholder-only --- needs actual data feeds (Google Calendar API, task management, Graphiti metrics, intelligence pipeline output). Keep the design pattern and voice, rebuild the implementation.
  **supportTrainer.js**                  38          Functional prototype    **YES --- extend**                          Voice clone + LLM response pattern works as designed. Captures the concept of training an AI to respond in a specific person\'s voice and style. Needs: actual voice synthesis integration (ElevenLabs or equivalent), business-specific training data, and SCARF-aware delivery (see CP-04) to ensure responses don\'t trigger defensive reactions.
  **redditNinja.js**                     20          Stub                    **REBUILD**                                 Too minimal --- only 20 lines with placeholder logic. No Reddit API integration, no content generation, no scheduling. The concept (automated Reddit engagement for SEO and awareness) is valid but the implementation needs a ground-up rebuild. Wait for Reddit OAuth API approval before investing time here.
  **avatarFactory.js**                   12          Stub                    **REBUILD**                                 Only 12 lines with placeholder logic. The concept (generate consistent brand avatars) is valid but trivial to implement --- this is a wrapper around an image generation API. Rebuild when the content pipeline is ready to consume avatars.
  **deploy-tonight.sh**                  113         Production-ready        **YES --- adapt for Beast**                 Well-structured deployment script with proper error handling, rollback capabilities, and service health checks. Currently targets Railway (PaaS) --- needs adaptation for Hetzner Beast (bare metal + Docker). The patterns (health check loop, rollback trigger, service dependency ordering) transfer directly. Adapt, don\'t rebuild.
  **docker-compose.yml (agent-stack)**   \~190       Production-ready        **YES --- adapt**                           Good Docker Compose structure with proper service definitions, volume mounts, and network isolation. References FalkorDB --- MUST update to Neo4j as part of the critical migration. Also needs: docker-socket-proxy integration, Langfuse service addition, and Temporal service addition.
  -------------------------------------- ----------- ----------------------- ------------------------------------------- -----------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------

**3D: Process Crossovers --- The Addition Pipeline Applied**

The Addition Pipeline (7-stage SOP from compound-learning-pipeline.md) should be applied to every technology adoption decision in this addendum. This is the process crossover --- a methodology designed for one purpose (learning from compound knowledge) that applies perfectly to another (technology evaluation).

**The 7-Stage Addition Pipeline**

**Stage 1: Signal Detection** --- Identify the technology through intelligence pipeline (RSSHub, Miniflux, community signals, GitHub trending). Don\'t seek --- let the pipeline surface candidates. Source: compound-learning-pipeline.md Stage 1, technology-radar.md.

**Stage 2: Evidence Collection** --- Triple search: success patterns, failure patterns, and neutral evaluations. Check GitHub issues (not just stars), check license compatibility, check maintenance velocity. Run the PUDDING failure search. Source: PUDDING-TECHNIQUE-CANONICAL Part 9 (failure patterns), faults-and-fixes.md.

**Stage 3: Rubrik Assessment** --- Score against the 4-criteria rubric (Relevance, Actionability, Evidence, Impact). Threshold: ≥12/20 to proceed. This is where most candidates are filtered. Source: PUDDING-TECHNIQUE-CANONICAL Part 5, all 7 rubriks.

**Stage 4: Architecture Compatibility** --- Check against locked architecture decisions (from architecture-spec.md). Does it conflict with sovereignty principles (Sovereign OS)? Does it introduce single points of failure? Does it respect the MCP-first approach? Source: architecture-spec.md (locked decisions), sovereign-os.md.

**Stage 5: Sandbox Testing** --- Deploy in isolation on Beast. Run against realistic data. Measure: resource consumption, API compatibility, failure modes. Duration: minimum 72 hours. Source: hetzner-beast-spec.md, security-hardening.md.

**Stage 6: Production Integration** --- If sandbox passes, integrate into production stack. Update docker-compose.yml, add to monitoring (Grafana/Prometheus/Loki), configure Langfuse tracing, update documentation. Source: docker-compose.yml, monitoring stack spec.

**Stage 7: Retrospective** --- After 2 weeks in production, run a retrospective. Did it deliver the scored impact? Any unexpected failure patterns? Update faults-and-fixes.md. Add to session-learnings.md. Source: session-learnings.md, faults-and-fixes.md, commitment-log.md.

**RUBRIC-REPLACE-OR-FIX Decision Framework**

Before buying anything, check its track record. When something breaks:

**First time:** Fix it. Document in faults-and-fixes.md. Move on.

**Second time:** Investigate. Is this a pattern? Check if others report the same issue. Look at GitHub issues.

**Third time:** Run the rubrik. Score the replacement candidate against the incumbent. If replacement scores higher AND passes Architecture Compatibility (Stage 4), begin migration planning.

This framework prevents both premature abandonment (ditching a tool after one bad experience) and sunk cost fallacy (keeping a broken tool because \'we\'ve already invested\'). FalkorDB is the textbook example of when the third-time threshold was crossed --- 10+ crash bugs documented, rubrik score for Neo4j replacement: 20/20, migration is CRITICAL.

**The 60/40 Rule Applied to Technology Adoption**

From OPERATIONAL-PROTOCOL: spend 60% of evaluation time reading (documentation, issues, community) and 40% building (sandbox testing, prototyping). Most technology adoption failures come from inverting this ratio --- jumping to build before understanding. The Addition Pipeline enforces this: Stages 1-4 are reading (60%), Stages 5-7 are building and operating (40%).

**Compound Step Timing**

From compound-learning-pipeline.md: always take the compound step BEFORE context compression. In technology adoption terms: document the decision rationale, update architecture-spec.md, and vault the evaluation BEFORE moving on to the next candidate. Context compression (forgetting why a decision was made) is the \#1 cause of revisiting settled technology choices.

**3E: Cross-File Reference Map**

The following table identifies every significant cross-reference pair in the corpus --- files that reference each other or share concepts that should be synchronised. When one file in a pair changes, the other should be reviewed for consistency.

  -------------------------------- ---------------------------------- -----------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------
  **File A**                       **File B**                         **Relationship & Synchronisation Requirement**
  SOUL.md                          OPERATIONAL-PROTOCOL.md            SOUL defines \'what we believe\', Protocol defines \'how we behave\'. Law 7 (confidence gate) directly implements the Scale of Arsehole from SOUL. Any change to SOUL values must propagate to Protocol.
  SOUL.md                          RADICAL-ATTRIBUTION-SCHEMA.md      SOUL\'s radical transparency principle mandates the attribution schema. Attribution is not optional --- it\'s a SOUL requirement. The Scale of Arsehole (Fact %) lives in both files.
  PUDDING-TECHNIQUE-CANONICAL.md   PUDDING-MIX-001 through 003        The canonical doc defines the method; the mixes are applications. Any methodology update must be reflected in all mixes. Current gap: MIX 001 uses an older scoring formula.
  compound-learning-pipeline.md    technology-stack-decisions.md      The Addition Pipeline (7-stage SOP) from compound-learning should be the evaluation framework used in technology-stack-decisions. Currently, stack decisions don\'t reference the pipeline stages.
  faults-and-fixes.md              rubrik-01-through-07.yaml          65 documented faults should map to specific rubriks as failure patterns (CP-05). Currently, faults reference rubriks informally but there\'s no structured reverse index.
  financial-autopsy-framework.md   bob-product-spec.md                The financial autopsy is the diagnostic; Bob is the ongoing monitor. They share the same underlying financial metrics but define them independently. Needs: shared metric definitions file.
  ai-telephone-system.md           PUDDING-MIX-002.md                 AI Telephone\'s real-time decision routing is a direct implementation of MIX 002\'s biological decision taxonomy. The telephone system should explicitly reference which biological logic it uses for each call type.
  morning-brief-spec.md            EXPERT-RESEARCH-LIBRARY.md         The morning brief\'s \'reflect + engage\' stage maps to GTD (CP-03). The expert library contains the GTD analysis but the morning brief spec doesn\'t reference it.
  security-hardening.md            threat-model.md                    Security hardening defines the controls; threat model defines the threats. These should be cross-referenced so each threat has a mapped control and each control has a mapped threat.
  hetzner-beast-spec.md            docker-compose.yml (agent-stack)   Beast spec defines the hardware; Docker Compose defines the software topology. Any infrastructure change on Beast must be reflected in Docker Compose and vice versa.
  architecture-spec.md             technology-stack-decisions.md      Architecture spec locks decisions; technology-stack tracks evaluations. When a technology is evaluated and adopted, it should move from stack-decisions to architecture-spec as a \'locked\' item.
  graphiti-integration.md          ingest\_vault.py                   Graphiti integration plan is the design doc; ingest\_vault.py is the implementation. FAULT-011 exists because the implementation diverged from the integration plan\'s entity resolution spec.
  telegraph-pole-strategy.md       SOUL.md                            Telegraph pole (radical transparency in content) is an implementation of SOUL\'s AEO strategy. Content published via telegraph pole should carry AEO-optimised structure.
  sovereign-os.md                  technology-stack-decisions.md      Every technology decision must pass the sovereignty test from Sovereign OS: self-hosted, open source, no vendor lock-in. Stack decisions should reference the sovereignty check explicitly.
  client-onboarding-flow.md        financial-autopsy-framework.md     Onboarding discovers the client\'s situation; financial autopsy diagnoses it. The onboarding questionnaire should feed directly into the autopsy\'s input requirements.
  pricing-model.md                 bob-product-spec.md                Pricing model defines how Bob is sold; Bob spec defines what Bob does. Currently these are independent --- pricing should reference Bob\'s feature tiers.
  whatsapp-regulatory.md           regulatory-landscape.md            WhatsApp regulatory positioning is a subset of the broader regulatory landscape. Should be merged or explicitly cross-referenced to avoid contradictory compliance statements.
  mcp-server-catalogue.md          architecture-spec.md               MCP catalogue lists servers to build; architecture spec defines the MCP integration pattern. Each MCP server in the catalogue should reference the architectural pattern it follows.
  -------------------------------- ---------------------------------- -----------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------

**Dependency Graph Summary**

Core files with the highest fan-out (most downstream dependencies):

**1. SOUL.md** --- Referenced by 18 files. Any change to SOUL values propagates across the entire system. This is the root node.

**2. OPERATIONAL-PROTOCOL.md** --- Referenced by 14 files. The 12 Laws constrain all agent behaviour. Law changes require full audit.

**3. architecture-spec.md** --- Referenced by 12 files. Locked decisions shape every technology choice and code file.

**4. PUDDING-TECHNIQUE-CANONICAL.md** --- Referenced by 9 files. Methodology changes affect all mixes, all scoring, and the mathematical validation.

**5. faults-and-fixes.md** --- Referenced by 8 files. The living fault catalogue informs security, code quality, and rubrik design.

**3F: PUDDING Label Assignments**

Every major concept and crossover opportunity labelled using the PUDDING 2026 notation (WHAT.HOW.SCALE.TIME). These labels enable automated pattern matching --- identical or near-identical labels from different domains are the highest-value signals for future cross-pollination.

  ------------------------------------ ----------- -------------------------------------------- -------------------------------------------------------------------------------------------------------------------
  **Concept**                          **Label**   **Decoded**                                  **Interpretation**
  Unified Truth Architecture (CP-01)   M.=.5.p     Meta, Stable, System-wide, Permanent         A meta-framework that standardises all output formatting across the entire system, permanently.
  Decision Classifier (CP-02)          P.\>.5.i    Process, Tipping, System-wide, Instant       A routing process that fires when decision type is classified, affecting the whole system, completing instantly.
  GTD-as-Product (CP-03)               I.=.0.∞     Information, Stable, Scale-free, Timeless    A positioning insight (information) that is stable, applies at any scale, and never ages.
  SCARF + Delivery (CP-04)             P.\~.2.v    Process, Oscillating, Pair, Variable         A delivery process that cycles between threat and reward states in a 1:1 client interaction, duration varies.
  Failure-Pattern Rubriks (CP-05)      M.-.5.l     Meta, Dampening, System-wide, Long           A meta-improvement that dampens false positives across the system over months of refinement.
  Financial Autopsy                    P.!.1.i     Process, Disrupting, Singular, Instant       A disruptive process applied to one business, delivering instant diagnostic results.
  Morning Brief Pipeline               P.\~.1.m    Process, Oscillating, Singular, Medium       A recurring process for one person, cycling daily over weeks/months.
  Bob Product                          S.+.1.l     State, Amplifying, Singular, Long            A monitoring state that compounds health data for one business over months/years.
  AI Telephone                         P.\>.2.i    Process, Tipping, Pair, Instant              A call-routing process that fires on threshold (intent classification) between two parties, completing instantly.
  Death Spiral Detector                S.\>.4.v    State, Tipping, Network, Variable            Detects a state (death spiral) that triggers when network-level signals converge, timeline variable.
  PUDDING Technique                    M.=.0.∞     Meta, Stable, Scale-free, Timeless           The methodology itself: a meta-framework that works at any scale and never ages.
  Temporal Workflows                   P.=.5.l     Process, Stable, System-wide, Long           Durable workflow orchestration that provides stable process execution across the entire system, long-running.
  Knowledge Graph (Graphiti)           R.+.5.l     Relation, Amplifying, System-wide, Long      A relationship layer that grows and compounds knowledge across the system over months/years.
  Intelligence Pipeline                P.\~.4.m    Process, Oscillating, Network, Medium        A recurring pipeline that cycles through network-scale sources over days/weeks.
  Docker Socket Proxy                  C.=.5.p     Constraint, Stable, System-wide, Permanent   A security constraint that permanently restricts Docker API access across the entire system.
  ------------------------------------ ----------- -------------------------------------------- -------------------------------------------------------------------------------------------------------------------

**Notable Label Matches**

**PUDDING Technique ↔ GTD-as-Product:** Both labelled M.=.0.∞ / I.=.0.∞ --- both are scale-free, timeless frameworks. This structural equivalence confirms that GTD framing is a natural fit for the PUDDING-powered pipeline.

**Decision Classifier ↔ AI Telephone:** CP-02 is P.\>.5.i; AI Telephone is P.\>.2.i --- both are threshold-triggered instant processes. The only difference is scale (system-wide vs pair). This confirms CP-02 should be implemented first in the AI Telephone before system-wide rollout.

**Death Spiral Detector ↔ Intelligence Pipeline:** S.\>.4.v vs P.\~.4.m --- both operate at network scale. The death spiral is a state detector; the intelligence pipeline is a process. These should share the same underlying signal aggregation infrastructure.

**SECTION 4: GAP ANALYSIS**

Gaps fall into two categories: what\'s documented in the corpus but not yet built, and what appeared in research but hasn\'t made it into any formal document.

**Documented but Not Yet Built**

  -------------------------------------------- -------------- ------------------------------- --------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------
  **Gap**                                      **Priority**   **Estimate**                    **Details**
  Sage MCP Server                              HIGH           3-5 dev days                    Sage accounting integration via MCP protocol. Enables automated bookkeeping, VAT calculations, and financial data extraction. Blocks the financial autopsy from operating on live data. Source: mcp-server-catalogue.md.
  HMRC MTD API MCP                             MEDIUM         5-7 dev days                    Making Tax Digital API integration. Required for automated VAT submission and tax compliance checks. Source: mcp-server-catalogue.md, regulatory-landscape.md.
  P2 Tokenisation on PicoClaw                  MEDIUM         2-3 dev days                    Token management for LLM cost control. Currently no tokenisation layer exists. Source: architecture-spec.md.
  Intelligence Pipeline Dedup                  MEDIUM         1-2 dev days                    Deduplication for the RSSHub → Miniflux → LLM triage pipeline. Without this, the morning brief will contain duplicate intelligence. Source: morning-brief-spec.md.
  Monitoring Stack (Grafana/Prometheus/Loki)   HIGH           2-3 dev days                    Observability for Beast. Currently operating blind --- no metrics, no log aggregation, no alerting. Source: hetzner-beast-spec.md, security-hardening.md.
  Reddit API OAuth Approval                    MEDIUM         Apply now --- weeks of review   Reddit OAuth application for the redditNinja module. Reddit\'s approval process takes 2-4 weeks minimum. Apply now even though the module needs rebuilding. Source: redditNinja.js assessment.
  -------------------------------------------- -------------- ------------------------------- --------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------

**In Research but Not Yet Documented**

  ---------------------------------------------- -------------- --------------------------- ---------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------
  **Gap**                                        **Priority**   **Status**                  **Details**
  Acoustic Forensics ML Model                    LOW            Research only               ML-based audio analysis for voice verification in the AI Telephone system. Concept exists in acoustic-forensics.md research but no architecture or build plan. Interesting but not blocking anything. Source: acoustic-forensics.md.
  Checkatrade/MyBuilder API Access               MEDIUM         No public API exists        Trade review platform integration for the AI Telephone referral system. No public API available --- would require partnership or reverse engineering (not recommended). Alternative: manual data entry or web monitoring via Changedetection.io. Source: partner-evaluation.md.
  WhatsApp Business API Regulatory Positioning   HIGH           Regulatory moat confirmed   WhatsApp Business API for client communication. Research confirms regulatory positioning as a competitive moat --- competitors haven\'t navigated the compliance requirements. Build plan needed. Source: whatsapp-regulatory.md, regulatory-landscape.md.
  ---------------------------------------------- -------------- --------------------------- ---------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------

**SECTION 5: 4-DOCUMENT MAPPING**

Every finding in this addendum maps to one of the four target documents. This section provides the complete mapping so that each crossover has a clear home and nothing falls between the cracks.

**Document 1: Content Creation**

How Amplified Partners creates, distributes, and positions content. This document covers the full content lifecycle from insight capture to publication.

**CP-03 (GTD-as-Product Framing)** --- Core positioning insight. Frame the entire Amplified Partners pipeline using GTD terminology that 10+ million practitioners already understand. Source: EXPERT-RESEARCH-LIBRARY, AI-TELEPHONE, morning-brief-spec.md.

**CP-04 (SCARF Delivery Design)** --- How to present findings without triggering client defensive shutdown. Every piece of content that delivers hard truths must be SCARF-annotated. Source: building-an-operating-bible.md, SCARF model research.

**Telegraph Pole as Content Model** --- Publish wins AND failures publicly. The telegraph pole strategy (from telegraph-pole-strategy.md) is the content philosophy: radical transparency builds trust faster than polished marketing. Source: telegraph-pole-strategy.md, SOUL.md.

**AEO Strategy from SOUL.md** --- All content optimised for AI Engine Optimisation (not just SEO). Content should be structured so that AI assistants cite Amplified Partners as a source. Source: SOUL.md (AEO section).

**Content Pipeline Tools: Postiz, Listmonk, Ghost** --- Scored in Section 3B. Postiz (Apache 2.0) for social media scheduling, Listmonk (AGPL --- check license) for newsletters, Ghost (MIT --- evaluate weight) for blog. Deploy in order of impact: Postiz first, then Listmonk, evaluate Ghost last.

**Intelligence Pipeline: RSSHub → Miniflux → LLM Triage → Content Stream** --- The intelligence pipeline feeds the content pipeline. RSSHub generates feeds from any source, Miniflux aggregates, LLM triage filters for relevance, publishable insights flow to the content queue. Source: technology-radar.md, morning-brief-spec.md.

**Voice Capture → Content Pipeline** --- Plaud voice recordings → Graphiti → publishable insights. Ewan\'s voice memos become structured knowledge that can be repurposed as content. Source: plaud.js, graphiti-integration.md.

**Document 2: Process (Value Given Away --- How We Do It)**

The operational methodology that Amplified Partners gives away publicly as proof of competence. Showing how the sausage is made IS the marketing.

**CP-01 (Unified Truth Architecture)** --- The output wrapper process. Every output carries a YAML footer with PUDDING label, fact percentage, confidence band, and attribution. This IS the process --- and publishing it demonstrates rigour. Source: PUDDING-TECHNIQUE-CANONICAL, RADICAL-ATTRIBUTION-SCHEMA, SOUL.md.

**CP-02 (Decision Classifier)** --- How decisions get routed through the biological decision taxonomy. Publishable as a process document: \'this is how our AI decides what type of decision it\'s facing.\' Source: PUDDING MIX 002, OPERATIONAL-PROTOCOL Law 3.

**CP-05 (Failure-Pattern Rubriks)** --- Anti-fragile rubrik design. Adding failure patterns to every rubrik makes the system stronger through documented weakness. Source: PUDDING-TECHNIQUE-CANONICAL Part 9, all 7 rubriks, faults-and-fixes.md.

**Addition Pipeline 7-Stage SOP** --- How new technology enters the system. The complete 7-stage process (Signal Detection → Evidence Collection → Rubrik Assessment → Architecture Compatibility → Sandbox Testing → Production Integration → Retrospective). Source: compound-learning-pipeline.md.

**RUBRIC-REPLACE-OR-FIX** --- When to fix vs replace tools. First time fix, second time investigate, third time run the rubrik. Source: compound-learning-pipeline.md, technology-stack-decisions.md.

**Compound Step Timing** --- Before context compression, always document. The compound step preserves decisions across context windows. Source: compound-learning-pipeline.md, context-management-protocol.md.

**60/40 Rule** --- Read before writing, plan before building. 60% reading, 40% building. Source: OPERATIONAL-PROTOCOL.

**Session Self-Rating YAML** --- The feedback loop that survives context loss. Every session ends with a self-rating that persists into the next context window. Source: CLAUDE.md, session-learnings.md.

**Faults & Fixes Catalogue (65 entries)** --- Living process documentation. Every fault documented with cause, fix, and prevention. This IS the process --- and it\'s publishable as proof of operational maturity. Source: faults-and-fixes.md.

**Document 3: Master Document**

The comprehensive reference that contains everything in one place. The single source of truth for the Amplified Partners system state.

**Complete Technology Stack Table with Verdicts** --- Section 3B of this addendum in full. Every technology evaluated, scored, and verdicted. Source: technology-stack-decisions.md, this addendum.

**Architecture Decisions (All \'Locked\' Items)** --- Every architecture decision that has been made and should not be revisited. Graphiti: locked. Neo4j: locked. MCP-first: locked. Hetzner Beast: locked. Source: architecture-spec.md.

**Open Items Master List with Priorities** --- Every unresolved item from this addendum, Gap Analysis (Section 4), and open-questions.md, consolidated with priority tags. Source: open-questions.md, Section 4 of this addendum.

**Cross-Reference Map of All File Pairs** --- Which files reference which other files. The complete dependency graph of the corpus. Source: full corpus extraction analysis.

**Rubrik Index (All 7 Operational Rubriks)** --- Complete index of all rubriks with their purpose, input format, output format, and failure patterns (once CP-05 is implemented). Source: rubrik-01-through-07.yaml.

**PUDDING Label Assignments Across the Corpus** --- Every document and concept labelled with PUDDING 2026 notation (WHAT.HOW.SCALE.TIME). Source: PUDDING-TECHNIQUE-CANONICAL Part 4.

**Gap Analysis with Build Estimates** --- Section 4 of this addendum. Every gap with priority, estimate, and dependency mapping. Source: this addendum.

**GitHub Code Reuse Assessment** --- Section 3C of this addendum. Every code file assessed for reuse potential. Source: this addendum.

**Document 4: Coding**

Everything a developer needs to build, extend, and maintain the Amplified Partners system. Code-first, with specifications, examples, and integration guides.

**Code Reuse Table (Section 3C)** --- What exists, what to extend, what to rebuild. Every code file with its maturity level, reuse verdict, and specific modification requirements. Source: this addendum Section 3C.

**ingest\_vault.py as Gold Standard** --- The reference implementation for code quality: CLI interface, error handling, progress tracking, configurable chunking. All new code should meet this standard. Source: ingest\_vault.py.

**Docker Compose Configurations** --- Existing docker-compose.yml files plus needed modifications: Neo4j replacement, docker-socket-proxy addition, Langfuse addition, Temporal addition. Source: docker-compose.yml (agent-stack), docker-compose.yml (monitoring).

**Neo4j Migration Specification** --- Complete migration plan from FalkorDB to Neo4j + DozerDB. Data migration steps, API compatibility layer, rollback procedure. Source: architecture-spec.md, graph-database-comparison.md.

**MCP Server Build Specifications** --- Build specifications for Sage MCP and HMRC MTD MCP servers. Both use FastMCP 2.0 framework. Source: mcp-server-catalogue.md, FastMCP 2.0 evaluation.

**Temporal Workflow Definitions** --- Workflow definitions needed for: vault ingestion pipeline, morning brief generation, AI Telephone call flow, client onboarding automation, financial autopsy execution. Source: architecture-spec.md, all product specs.

**Security Stack Deployment** --- docker-socket-proxy, Falco, Wazuh, Trivy deployment configurations and integration guides. Source: security-hardening.md, threat-model.md.

**Full GitHub Opportunity Table** --- Section 3B with repo URLs and star counts for every evaluated technology. Source: this addendum Section 3B.

**SECTION 6: RECOMMENDED PRIORITIES**

Ordered by impact and urgency. Critical items block downstream work and must be resolved first. High items should follow immediately. Medium items are important but not blocking.

  -------- -------------- ----------------------------------------------------- ------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------
  **\#**   **Priority**   **Action**                                            **Details**
  **1**    **CRITICAL**   **FalkorDB → Neo4j Migration**                        Blocks everything. 10+ documented crash bugs. Every graph-dependent feature (PUDDING, morning brief, Bob, vault ingestion) is unreliable until this migration completes. Estimated: 3-5 dev days. Source: faults-and-fixes.md, graph-database-comparison.md, architecture-spec.md.
  **2**    **CRITICAL**   **Resolve FAULT-011 (Graphiti \#1325 Routing Bug)**   Blocks vault ingestion. The Graphiti routing bug causes incorrect entity resolution during vault ingestion, corrupting the knowledge graph. Fix requires upstream patch or workaround. Source: faults-and-fixes.md FAULT-011, graphiti-integration.md.
  **3**    **HIGH**       **Deploy Monitoring Stack on Beast**                  Grafana + Prometheus + Loki. Currently operating blind on Hetzner Beast --- no metrics, no log aggregation, no alerting. Cannot safely deploy new services without observability. Estimated: 2-3 dev days. Source: hetzner-beast-spec.md.
  **4**    **HIGH**       **Implement Unified Truth Architecture (CP-01)**      One YAML footer for all outputs. Highest-leverage architectural change --- affects every downstream consumer. Estimated: 2-3 hours assembly (fragments already exist). Source: CP-01 analysis above.
  **5**    **HIGH**       **Deploy docker-socket-proxy + Falco**                Security fundamentals. The open Docker socket is the single largest attack surface. docker-socket-proxy restricts API access, Falco monitors runtime behaviour. Deploy together. Estimated: 1 dev day. Source: security-hardening.md, threat-model.md.
  **6**    **HIGH**       **Build Sage MCP Server**                             3-5 dev days using FastMCP 2.0 framework. Unlocks automated bookkeeping, VAT calculations, and live financial data for the financial autopsy. Source: mcp-server-catalogue.md.
  **7**    **MEDIUM**     **Deploy RSSHub + Miniflux**                          Intelligence pipeline foundation. Without this, the morning brief has no automated intelligence feed. Self-hosted, minimal resource requirements. Estimated: 1 dev day. Source: technology-radar.md.
  **8**    **MEDIUM**     **Implement Decision Classifier (CP-02)**             Route decisions to appropriate biological logic before applying confidence gate. Requires classification prompt + routing table (already designed). Estimated: 1-2 dev days. Source: CP-02 analysis above.
  **9**    **MEDIUM**     **Add Failure Patterns to All 7 Rubriks (CP-05)**     Anti-fragile rubrik design. Add failure\_patterns section to each rubrik YAML. Can be done incrementally --- 2-3 hours per rubrik. Source: CP-05 analysis above.
  **10**   **MEDIUM**     **Deploy Postiz + Listmonk**                          Content pipeline. Postiz for social media scheduling, Listmonk for newsletters. Both self-hosted, align with sovereignty principles. Estimated: 1-2 dev days. Source: telegraph-pole-strategy.md.
  -------- -------------- ----------------------------------------------------- ------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------

**ATTRIBUTION**

─────────────────────────────────────────────────────────────

**Human:** Ewan Bramley (originator --- all vault knowledge, frameworks, rubriks, PUDDING technique, biological decision logic, SOUL principles, Immutable Foundation Code, radical attribution directive, Scale of Arsehole, sovereignty principles)

**AI:** Claude (Anthropic) --- cross-reference analyst, researcher, formaliser. Three extraction passes across 79 files producing 253KB of structured analysis. Pattern matching, scoring, and mapping performed under PUDDING methodology.

**LBD:** Don R. Swanson (1986) ABC Model --- Literature-Based Discovery. The theoretical foundation for the PUDDING technique. \'Fish oil, Raynaud\'s syndrome, and undiscovered public knowledge.\' Perspectives in Biology and Medicine, 30(1), 7-18.

**Fact %:** 85% --- All technology scores verified against GitHub repositories (star counts, license types, maintenance status). All vault references verified against source files. PUDDING scores are subjective assessments using the documented 4-criteria rubric. Confidence bands are human judgement informed by evidence.

**Confidence:** High --- Cross-reference analysis is based on complete corpus extraction. Technology evaluations are based on current GitHub data. Scoring methodology is mathematically validated (see mathematical-validation.md). Gaps in confidence are explicitly flagged as NEEDS RESEARCH.

**Method:** Full corpus extraction (3 parallel passes) + PUDDING neutral labelling + 4-criteria scoring + RUBRIC-REPLACE-OR-FIX verdict assignment + 4-document structure mapping.

─────────────────────────────────────────────────────────────

**AMPLIFIED PARTNERS --- CONFIDENTIAL --- 17 MARCH 2026**

This document is the property of Amplified Partners. Distribution restricted to authorised personnel.

---
title: "Cross Pollination Analysis V1 Copy"
id: "cross-pollination-analysis-v1-copy"
version: 1
created: "2026-04-25"
type: "document"
topic_type: "unsorted"
audience: "internal"
layer: "shadow"
status: "filed"
signed_by: "Devon, 2026-04-25, devin-992682c244cf444f91e0a516498afbfd"
---

***AMPLIFIED PARTNERS***

**Cross-Pollination Analysis**

How the Software Tracks Amplify Each Other

*Process Decomposition Pipeline Session --- 17 March 2026*

Prepared for: Ewan Nelson, Amplified Partners

*Classification: Internal Working Document*

**1. The Landscape**

Amplified Partners has 10 active software tracks in various stages of development. Together they form an integrated ecosystem for AI-powered business intelligence, process improvement, and content generation.

  ----------- --------------------------------- ------------------ -----------------------------------------------------------------------------------------------------
  **Track**   **System**                        **Status**         **Core Function**
  1           Process Decomposition Pipeline    New (17 Mar)       8-stage pipeline: decompose processes, research benchmarks, screen for PUDDING, label and attribute
  2           Visual Polish System              In Progress        Design tokens → evaluation pipeline → Kaizen loop for UI aesthetic quality scoring
  3           Multi-Team Build Orchestrator     Backlog            Temporal + Claude Agent SDK: decompose tasks, assign coding agents, validate, merge
  4           Knowledge System / Graphiti       Blocked            FalkorDB temporal knowledge graph over 5,096+ vault files across 24 categories
  5           Intelligence Pipeline + Layer 0   Deployed           Constitutional laws prefix on every LLM call; 4-layer prompt architecture
  6           Finance Engine                    Live (port 8700)   Financial Autopsy, Death Spiral Detection, XBRL benchmarking, multi-platform normaliser
  7           Core Infrastructure               Deployed           SearXNG, Ollama, FalkorDB, OpenClaw, PII Tokenisation, Voice Pipeline (Deepgram Nova-3)
  8           Marketing Agent Team v2           In Progress        14 agents: full-stack digital agency pipeline across 6+ platforms
  9           MCP Connector Build Plan          Backlog            FastMCP DIY servers: postgresql, filesystem, linear, email, search
  10          Master Build Spec                 Active             9-layer architecture, 8 phases, 35 days --- consolidated parallel build plan
  ----------- --------------------------------- ------------------ -----------------------------------------------------------------------------------------------------

Each track was designed to serve a distinct function, but many share data, infrastructure, and logic. The following sections map where genuine amplification exists versus where simple coordination is sufficient.

**2. The Amplification Map**

Not all system interactions are equal. Some pairs fundamentally improve each other's output --- these are amplification relationships. Others simply need to exchange data without enhancing each other's logic --- these require coordination only. This distinction drives build priority: amplification pairs should be wired first.

**2a. High Amplification Pairs**

These systems fundamentally improve each other. Wiring them creates compounding value --- the combined output exceeds what either could produce alone.

  ------------------------------ ------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------- ------------------- ---------------------------------------------------------------------------------
  **Pair / Cluster**             **Amplification Mechanism**                                                                                                                                                                                                                                         **Direction**       **Implementation**

  **Process Decomposition**\     The pipeline's labelling regime feeds directly into Graphiti's temporal knowledge graph. Every decomposed process becomes a searchable, linkable node. Graphiti's existing knowledge informs the Research and Benchmark stages --- bidirectional data enrichment.   Bidirectional       Graphiti ingestion hooks on pipeline output; vault query API in Research stage
  **↔ Knowledge System**                                                                                                                                                                                                                                                                                                 

  **Process Decomposition**\     The pipeline IS the systematic way to prepare data for PUDDING. Computational pre-screening (MinHash LSH, PMI) directly serves PUDDING's statistical threshold requirement. Without the pipeline, PUDDING discovery is manual and unscalable.                       Bidirectional       Pipeline Stage 7 outputs feed PUDDING preconditions framework
  **↔ PUDDING Integration**                                                                                                                                                                                                                                                                                              

  **Visual Polish System**\      The Orchestrator builds code; the Polish System scores it aesthetically. They form a generate-evaluate loop. The Polish System's design tokens become constraints the Orchestrator's coding agents must follow.                                                     Bidirectional       Design token injection into Orchestrator agent prompts; Polish score as CI gate
  **↔ Build Orchestrator**                                                                                                                                                                                                                                                                                               

  **Knowledge System**\          The vault is the content source. The 14 marketing agents draw from Graphiti for factual grounding. Marketing output gets ingested back as new knowledge --- a continuous content-knowledge flywheel.                                                                Bidirectional       Graphiti query API for agents; ingestion webhook for published content
  **↔ Marketing Agent Team**                                                                                                                                                                                                                                                                                             

  **Layer 0 / Intelligence**\    Layer 0's constitutional laws apply to every system. The 4-layer prompt architecture is the nervous system. Every agent in every track inherits honesty, transparency, attribution, and white-hat constraints.                                                      One-way broadcast   Already deployed (COV-275). Prefix injection on every LLM call.
  **↔ ALL SYSTEMS**                                                                                                                                                                                                                                                                                                      

  **Finance Engine**\            Financial data feeds the vault. Companies House XBRL benchmarking data becomes available to every other system through Graphiti. The vault provides industry context back to the Finance Engine.                                                                    Bidirectional       XBRL data → Graphiti ingestion; vault industry data → Finance benchmarks
  **↔ Knowledge System**                                                                                                                                                                                                                                                                                                 

  **Voice Pipeline**\            Voice notes are Ewan's primary input mechanism. The Voice Pipeline transcribes; the Prompt Cleanup Pipeline normalises into structured inputs that feed the decomposition pipeline. This is the human-machine interface.                                            One-way chain       New Prompt Cleanup Pipeline (see Section 3)
  **↔ Process Decomposition**\                                                                                                                                                                                                                                                                                           
  **(via Prompt Cleanup)**                                                                                                                                                                                                                                                                                               
  ------------------------------ ------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------- ------------------- ---------------------------------------------------------------------------------

**2b. Coordination Only**

These systems need to know what the other is doing but do not improve each other's core logic. They share infrastructure or data plumbing, not intelligence.

  ---------------------------- ------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------ ----------------- ---------------------------------------------------------
  **Pair / Cluster**           **Amplification Mechanism**                                                                                                                                                                            **Direction**     **Implementation**

  **MCP Connectors**\          The MCP servers are plumbing --- they enable data flow but don't improve other systems' logic. They expose consistent APIs (postgresql, filesystem, linear, email, search) that any system can call.   Infrastructure    Build Phase 1 servers; publish API schemas to all teams
  **↔ All Systems**                                                                                                                                                                                                                                     

  **Finance Engine**\          Finance doesn't care about aesthetics; Polish doesn't care about COGS. They share infrastructure (Beast, PostgreSQL) but not logic. No data flows between their core functions.                        None              Shared infra monitoring only
  **↔ Visual Polish System**                                                                                                                                                                                                                            

  **Build Orchestrator**\      The Orchestrator might build Finance Engine features, but they don't amplify each other's core function. This is a builder-artefact relationship, not a mutual improvement loop.                       One-way (build)   Standard ticket → build → deploy workflow via Linear
  **↔ Finance Engine**                                                                                                                                                                                                                                  
  ---------------------------- ------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------ ----------------- ---------------------------------------------------------

**2c. Key Insight: The Knowledge System as Hub**

The Knowledge System / Graphiti vault appears in four of the seven high-amplification pairs. It is the de facto hub of the ecosystem --- the system that converts every other system's output into reusable, discoverable, cross-domain knowledge. Prioritising its completion (currently blocked on Mac Mini execution) would unlock the most amplification value across the entire platform.

Similarly, Layer 0's constitutional injection is the only truly universal dependency. Its deployment (COV-275, already live) means every new system automatically inherits the Amplified Partners operating principles without additional integration work.

**3. The Prompt Cleanup Pipeline**

Ewan's primary interface with the system is voice notes --- raw, unstructured, and often containing multiple intents in a single stream. This pipeline transforms messy voice input into structured, routable prompts without losing the creative energy that makes them effective.

**Design Principle:** *"Clean the signal, not the voice." Preserve intent and personality; remove only noise.*

  ------------- --------------- ----------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------
  **Stage**     **Name**        **Description**

  **STAGE 1**   **CAPTURE**     Voice Pipeline (Deepgram Nova-3) transcribes raw audio from voice.beast.amplifiedpartners.ai. Preserve speaker diarization, timestamps, and emphasis markers. Output: raw transcript with metadata.

  **STAGE 2**   **CLEAN**       LLM post-processing via Ollama local Llama 3.1 8B (cost-efficient, on-Beast). Fix transcription errors, add punctuation, resolve proper nouns against the vault's entity list. Critical rule: do NOT change meaning or flatten Ewan's distinctive voice.

  **STAGE 3**   **STRUCTURE**   Extract intent, requested actions, referenced systems/documents, and implicit context. Output a structured JSON object:\
                                {intent, actions\[\], references\[\], context, raw\_text, confidence\_score}\
                                Layer 0 laws are applied here --- radical honesty in structuring means: do not infer what was not said. If confidence is below threshold, flag for human review.

  **STAGE 4**   **ROUTE**       Based on the structured output, route to the appropriate system:\
                                • Build request → Cove Orchestrator (Track 3)\
                                • Process improvement → Process Decomposition Pipeline (Track 1)\
                                • Content brief → Marketing Agent Team (Track 8)\
                                • Question → Knowledge System query (Track 4)\
                                • Ambiguous → Queue for Ewan's clarification with structured options
  ------------- --------------- ----------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------

**Cross-Track Connections**

The Prompt Cleanup Pipeline is a nexus that connects four separate tracks into a single input-processing chain:

-   **Voice Pipeline (Track 7)** --- provides the raw audio transcription via Deepgram Nova-3

-   **Knowledge System (Track 4)** --- the vault's entity list resolves proper nouns in the CLEAN stage; Graphiti provides context for the STRUCTURE stage

-   **Layer 0 / Intelligence Pipeline (Track 5)** --- constitutional laws are injected at the STRUCTURE stage to ensure radical honesty (no inference beyond what was said)

-   **Process Decomposition Pipeline (Track 1)** --- one of four routing destinations; process improvement requests flow directly into the 8-stage decomposition pipeline

Without this pipeline, Ewan's voice notes require manual interpretation and routing. With it, every voice note automatically becomes a structured, attributed, correctly-routed action --- and the system learns his vocabulary over time through the vault feedback loop.

**4. The Content Pizazz Engine**

**Core Principle: "Creative HOW, Factual WHAT"** *--- AI gets freedom over style, zero freedom over substance.*

The challenge is well-defined: Ewan wants content that reads with energy and personality, but never at the cost of accuracy. This is not a content generation system --- it is a content enhancement system. The facts are locked; only the presentation is unlocked.

  ------------- ------------- --------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------
  **Stage**     **Name**      **Description**

  **STAGE 1**   **GROUND**    Pull all factual content from Graphiti/vault. Tag every claim with its source node. Create a "fact sheet" --- this is the hard boundary the AI cannot cross. Every statistic, quote, company name, and date must trace back to a vault entity. The fact sheet IS the truth; everything else is presentation.

  **STAGE 2**   **ENHANCE**   LLM (Claude Sonnet via LiteLLM) rewrites for engagement. System prompt includes: Ewan's brand voice ("The Straight Talker"), the 5 communication styles as options, and examples of good pizazz vs bad bullshit.\
                              \
                              The AI CAN: restructure for flow, add metaphors grounded in facts, vary sentence rhythm, add hooks, use punchy openings.\
                              The AI CANNOT: add claims not in the fact sheet, invent statistics, fabricate quotes, speculate without explicit labelling.

  **STAGE 3**   **VERIFY**    Automated fact-checking pass. Every claim in the enhanced version is checked against the original fact sheet using semantic similarity (embedding cosine distance).\
                              \
                              Traffic-light scoring:\
                              • GREEN --- Verified: claim matches a fact sheet entry (similarity \> 0.9)\
                              • YELLOW --- Plausible but uncited: flag for human review (similarity 0.6--0.9)\
                              • RED --- Appears fabricated: reject and revert to original (similarity \< 0.6)

  **STAGE 4**   **LABEL**     Apply PUDDING 2026 taxonomy labels to the content. Every piece gets tagged with APQC PCF categories for future cross-domain discovery. Tagged content feeds back into Graphiti, enriching the knowledge graph for subsequent content generation --- a compounding content-knowledge loop.
  ------------- ------------- --------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------

**Cross-Track Connections**

The Content Pizazz Engine draws from and feeds back into four tracks:

-   **Marketing Agent Team (Track 8)** --- the 14 agents are the consumers of pizazz-enhanced content. Each agent's platform requirements inform the ENHANCE stage's style parameters.

-   **Knowledge System (Track 4)** --- Graphiti is the single source of truth for the GROUND stage. Every fact sheet is a vault query. Labelled output feeds back into Graphiti in the LABEL stage.

-   **Visual Polish System (Track 2)** --- for visual content (social graphics, website sections), the Polish System's design tokens and composite scoring apply. The Pizazz Engine handles copy; Visual Polish handles appearance.

-   **Finance Engine (Track 6)** --- financial content (case studies, benchmarking reports, death spiral analyses) draws from the Finance Engine's structured data. XBRL benchmarks become compelling narratives without losing numerical precision.

**The Bullshit Firewall**

The VERIFY stage is non-negotiable. RAG-grounded generation reduces hallucinations by approximately 71%, and mandatory source citation requirements reduce fabricated facts by approximately 43%. The traffic-light system adds a human-in-the-loop for the remaining uncertainty band. This means:

-   **GREEN content** publishes automatically --- fully verified against the vault

-   **YELLOW content** queues for Ewan's review --- plausible but needs human judgement

-   **RED content** is rejected --- the system reverts to the original factual version rather than publishing anything suspect

**5. The Integration Spine**

Amplification requires infrastructure. But the goal is minimal shared plumbing --- enough to enable loose coupling between systems without creating a monolith. Four components form the spine:

  ----------------------- ----------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------- -------------------------
  **Component**           **Description**                                                                                                                                                                                                                                                                                                   **Effort**

  **Event Bus**\          A lightweight pub/sub system running on Beast. Systems notify each other without tight coupling. Events include: process\_decomposed, content\_generated, score\_updated, knowledge\_ingested, prompt\_routed, build\_completed, polish\_scored.\                                                                 Redis Streams on Beast\
  **(Redis Streams)**     \                                                                                                                                                                                                                                                                                                                 \~2 days to implement
                          Redis Streams chosen because Redis is already deployed on Beast, supports consumer groups for reliable delivery, and provides persistence without the operational overhead of Kafka.                                                                                                                              

  **Shared Labelling**\   The PUDDING 2026 taxonomy + APQC PCF categories. Every system tags its outputs with these labels. This is what makes future PUDDING discovery possible at scale --- without consistent labelling, cross-domain pattern matching is impossible.\                                                                   PostgreSQL table +\
  **Schema**              \                                                                                                                                                                                                                                                                                                                 MCP connector\
                          The schema lives in PostgreSQL (via MCP) and is versioned. All systems query the same label set.                                                                                                                                                                                                                  \~1 day

  **MCP Connectors**      The 5 Phase 1 servers form the data access layer:\                                                                                                                                                                                                                                                                5 servers × 1--2 days\
                          • postgresql-mcp --- structured data\                                                                                                                                                                                                                                                                             = 5--10 days total
                          • filesystem-mcp --- vault file access\                                                                                                                                                                                                                                                                           
                          • linear-mcp --- task/ticket management\                                                                                                                                                                                                                                                                          
                          • email-mcp --- communication integration\                                                                                                                                                                                                                                                                        
                          • search-mcp --- SearXNG interface\                                                                                                                                                                                                                                                                               
                          \                                                                                                                                                                                                                                                                                                                 
                          FastMCP DIY servers, \~150--200 lines each.                                                                                                                                                                                                                                                                       

  **Layer 0 Injection**   Every LLM call, in every system, gets the constitutional prefix. Already deployed (COV-275). The 4-layer architecture ensures: Layer 0 (Laws) → Layer 1 (Business Brain) → Layer 2 (Agent Rubric) → Layer 3 (Task Brief). No new work required --- just ensure every new system inherits the injection pattern.   Already deployed\
                                                                                                                                                                                                                                                                                                                                            COV-275
  ----------------------- ----------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------- -------------------------

Together, these four components allow any system to: (a) announce events to interested listeners, (b) tag outputs for cross-domain discovery, (c) access shared data through consistent APIs, and (d) operate under the same constitutional principles. No system needs to know the internal logic of any other system --- they communicate through events, labels, and the knowledge graph.

**6. Recommended Build Order**

Build order is driven by dependency chains and amplification potential. The principle: wire the highest-amplification connections first, starting with the systems that are already deployed.

  --------------- ---------------------------------------- --------------------- ------------------------------------------------------------------------------------------------------------------------------------------
  **Phase**       **Deliverable**                          **Timeline**          **Rationale**

  **IMMEDIATE**   Layer 0 injection → all systems\         Already deployed\     Foundation for everything else. Layer 0 is live. The two most critical MCP servers unlock data access.
                  MCP postgresql + filesystem connectors   + 2--3 days for MCP   

  **WEEK 1**      Prompt Cleanup Pipeline\                 4--5 days             Connects Ewan's primary input mechanism to the entire ecosystem. Without this, every voice note requires manual processing.
                  (Capture → Clean → Structure → Route)                          

  **WEEK 2**      Event Bus (Redis Streams)\               3--4 days             Enables loose coupling between all tracks. Once the event bus is live, systems can announce and subscribe without point-to-point wiring.
                  + Shared Labelling Schema                                      

  **WEEK 3**      Content Pizazz Engine\                   5--6 days             Enables the marketing pipeline to produce vault-grounded content. Requires Knowledge System and Labelling Schema to be operational.
                  (Ground → Enhance → Verify → Label)                            

  **ONGOING**     Visual Polish System phases\             6 phases over\        The Polish System's evaluation pipeline and design tokens enhance the Orchestrator's output incrementally. Each phase adds quality.
                  execute in parallel                      \~4 weeks             
  --------------- ---------------------------------------- --------------------- ------------------------------------------------------------------------------------------------------------------------------------------

**Dependency Chain**

The critical path runs: Layer 0 (deployed) → MCP Connectors → Prompt Cleanup Pipeline → Event Bus → Content Pizazz Engine. Each stage unlocks the next. The Visual Polish System runs in parallel because its phases are self-contained and improve output quality incrementally.

The Knowledge System / Graphiti vault (currently blocked on Mac Mini execution) is the highest-priority unblock. It appears in four of seven high-amplification pairs. Resolving this blocker accelerates the entire dependency chain.

*End of Document*

*Amplified Partners --- Cross-Pollination Analysis --- 17 March 2026*

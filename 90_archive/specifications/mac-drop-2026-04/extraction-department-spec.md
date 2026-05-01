Status: [NON-AUTHORITATIVE]
Sanitisation: done — no client data, credentials, or PII found in source specifications
Source: Ewan's Mac drop ("New Folder With Items 2.zip", 521 files, 125MB), ingested 2026-04-29

**AMPLIFIED PARTNERS**

**The Extraction Department**

Data Ingestion, Synthesis & Output Pipeline

━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

Department Specification v1.0

March 2026

Architect: **Ewan Bramley**

Formalised by: Claude (Anthropic)

**INTERNAL --- NOT FOR DISTRIBUTION**

**Contents**

**Executive Summary**

This document specifies the Extraction Department --- a purpose-built
division within the Amplified Partners AI operating model that solves
the single biggest operational problem in AI-powered consultancy:
knowledge doesn\'t persist between sessions.

Across hundreds of working sessions, Amplified Partners has generated an
enormous body of valuable knowledge --- architecture specs, framework
designs, methodology innovations, business strategies, marketing
pipelines, pricing models, agent designs, and more. This knowledge is
currently scattered across conversation threads, vault files, voice
captures, and multiple AI platforms. When a new session begins, the AI
starts fresh. Critical context is lost. Previous decisions get
revisited. Nuance disappears.

The Extraction Department is not a piece of software. It is a set of AI
agent skill files (.md), a defined pipeline process, and a small amount
of supporting code --- designed so that AI agents, given the right
instructions and tools, can ingest everything, extract what matters,
synthesise it into a unified knowledge base, and route it to the right
output streams.

> *\"I\'ve got a suspicion there\'s going to be very little software.\"
> --- Ewan Bramley*

He\'s right. The quantification in this document confirms it:
approximately 85% of this department is skill files and prompting, 10%
is configuration, and only 5% is actual Python code.

**1. What This Department Does**

In plain English: this department takes everything Amplified Partners
has ever produced, thought, discussed, designed, or captured --- across
every AI session, every vault file, every voice recording, every
scribbled idea --- and turns it into usable, structured, quality-checked
outputs that make the entire operation smarter.

**1.1 The Four Core Functions**

**INGEST**

Finds and catalogues every piece of data across all sources. The
existing vault alone contains 4,787 files across 25 directories. But the
vault is only one source. There are also conversation threads from
Claude, Perplexity sessions, voice captures, monologue transcripts, and
working documents scattered across multiple machines.

**EXTRACT**

Pulls everything valuable out of each source --- not just the
conclusions, but the reasoning behind them. Not just the decisions, but
the creative process that led there. Not just the frameworks, but the
stories and anecdotes that make them real. Previous extraction attempts
have been \"AI meticulous\" --- which means surface-level, hitting the
obvious points while missing the depth. This department is designed for
actual meticulousness.

**SYNTHESISE**

Deduplicates, resolves conflicts, and builds a unified knowledge graph.
The same concept might be described differently across five sessions ---
the synthesis stage recognises that, picks the best version, and creates
cross-references. It applies the PUDDING technique (adapted from
Swanson\'s Literature-Based Discovery) to find unexpected connections
across domains.

**ROUTE & OUTPUT**

Sends synthesised knowledge to eight distinct output streams --- from
agent skill files that make AI agents better at their jobs, to content
for the marketing pipeline, to material for Ewan\'s book, to commercial
products like the Taxonomy Engine and AQS. Every output passes through a
quality gate before it reaches its destination.

**2. The Problem It Solves**

The Extraction Department addresses four interconnected problems that,
left unsolved, cap the potential of every AI-powered operation.

**2.1 Context Amnesia**

Every AI session starts with a blank slate. Research on LLM context
windows confirms that even with expanding token limits --- now reaching
200,000+ tokens in leading models --- performance degrades as context
grows. Information placed in the middle of long contexts gets \"lost,\"
a well-documented phenomenon where models focus on the beginning and end
of their context while neglecting the middle. The practical result: an
AI that helped design a pricing model last Tuesday has no memory of it
this Thursday. Decisions get re-litigated. Nuance evaporates. The
organisation\'s collective knowledge resets to zero with each new
session.

**2.2 Scattered Knowledge**

Amplified Partners\' intellectual capital is distributed across:

-   4,787 vault files across 25 directories on the Beast server

-   FalkorDB knowledge graph with Graphiti temporal indexing

-   Hundreds of Claude conversation threads

-   Perplexity research sessions

-   Voice captures and monologue transcripts

-   Working documents, spreadsheets, and design files

No single agent, human or AI, can hold all of this in working memory
simultaneously. The knowledge exists --- but it\'s functionally
invisible to any given session.

**2.3 The Waffle-to-Gold Ratio**

Creative work is messy by nature. A one-hour session might produce 90
minutes of thinking-out-loud (\"waffle\") and 10 minutes of breakthrough
insight (\"gold\"). Both are valuable --- the waffle contains stories,
anecdotes, and creative process material that\'s perfect for content
marketing. The gold contains the operational decisions that need to
become system specifications. But previous extraction treated everything
the same way, either discarding the waffle entirely or burying the gold
under it. This department separates the two while preserving both.

**2.4 The Completeness Gap**

Previous AI-driven extraction was what we call \"AI meticulous\" --- it
looked thorough but operated at summary level. It would extract
\"decided to use a 5-tier pricing model\" but miss that the decision was
made because Ewan noticed a pattern in how SMBs in the North East
respond to price anchoring, which connects to the Micro-Help Library
design, which connects to the giveaway strategy, which connects to the
book narrative arc. The depth of interconnection was lost. The
Extraction Department is designed to capture the full chain of
reasoning, not just its endpoint.

**3. Department Architecture**

The department operates as a five-stage pipeline. Each stage has a
primary agent (or agent cluster), defined inputs and outputs, and
quality gates between stages. The architecture is deliberately linear at
the top level --- data flows in one direction --- but each stage
internally supports parallel processing.

**3.0 Pipeline Overview**

┌──────────────────────────────────────────────────────────────────┐

│ THE EXTRACTION DEPARTMENT │

│ Five-Stage Processing Pipeline │

├──────────────────────────────────────────────────────────────────┤

│ │

│ ┌─────────┐ ┌──────────┐ ┌───────────┐ ┌────────────┐ │

│ │ STAGE 1 │──▶│ STAGE 2 │──▶│ STAGE 3 │──▶│ STAGE 4 │ │

│ │Discovery│ │Extraction│ │ Synthesis │ │ Routing │ │

│ │HoundDog │ │ DocBench │ │Convergence│ │Switchboard │ │

│ └─────────┘ └──────────┘ └───────────┘ └─────┬──────┘ │

│ │ │ │ │ │

│ ▼ ▼ ▼ ▼ │

│ Manifest 4 Formats Unified KG 8 Output Streams │

│ + Metadata per source FalkorDB ┌───────────────┐ │

│ + PUDDING │ STAGE 5 │ │

│ labels │ Gatekeeper │ │

│ │ Quality QA │ │

│ └───────────────┘ │

│ │ │

│ ▼ │

│ Published Output │

│ Vault / Skills / │

│ Content Queue │

└──────────────────────────────────────────────────────────────────┘

**3.1 Stage 1: Discovery (HoundDog)**

The HoundDog agent is the department\'s scout. Its job is to find every
piece of data across every source, catalogue it, and produce a manifest
that downstream stages can work from.

**Data Sources**

-   Vault files (4,787 files across 25 directories on Beast server)

-   FalkorDB knowledge graph (existing entries via Graphiti)

-   Claude conversation threads (Projects, standalone conversations)

-   Perplexity research sessions

-   Voice captures and monologue transcripts

-   Working documents across local machines and cloud storage

-   Email threads containing design discussions

-   Any future source added to the registry

**Output: The Discovery Manifest**

HoundDog produces a structured JSON manifest for every discovered
source:

{

\"source\_id\": \"uuid-v4\",

\"source\_type\": \"conversation \| vault\_file \| voice\_capture \|
\...\",

\"location\": \"path or URI\",

\"discovered\_at\": \"ISO-8601 timestamp\",

\"estimated\_date\": \"when the content was created\",

\"estimated\_value\": \"high \| medium \| low \| unknown\",

\"topic\_clusters\": \[\"pricing\", \"agent-design\", \"marketing\"\],

\"word\_count\": 4520,

\"format\": \"markdown \| json \| text \| audio \| docx\",

\"extraction\_status\": \"pending \| in\_progress \| complete \|
failed\",

\"content\_hash\": \"sha256 for dedup\"

}

**How HoundDog Works**

HoundDog is primarily a skill file, not software. It instructs an AI
agent how to:

1.  Recursively traverse directory structures on Beast server

2.  Query the FalkorDB graph for existing entity catalogues

3.  Parse conversation export formats (Claude JSON, Perplexity markdown)

4.  Apply fast topic-clustering using keyword extraction (no ML model
    needed --- TF-IDF on titles and first 500 words)

5.  Generate content hashes for deduplication at the source level

6.  Estimate value based on heuristics: length, topic density, presence
    of decision language (\"we decided\", \"the approach is\", \"this
    means\")

The only actual code required is a Python script for filesystem
traversal and hashing --- approximately 150 lines. Everything else is
prompting.

**3.2 Stage 2: Extraction (DocBench)**

DocBench is the extraction engine --- the core of the department. It
takes each discovered source and extracts its content into four parallel
output formats, achieving a target accuracy of 99.53% (the benchmark
established in prior Amplified Partners design work).

**The Four Extraction Formats**

  ---------------------------- ------------------------------------------------------------------------------------------------- ------------------------------------------------------ ------------------------------------------------------------------------------------------------------------
  **Format**                   **What It Captures**                                                                              **Primary Consumer**                                   **Example Output**
  **A) Raw Text**              Verbatim, unedited content. Every word preserved exactly as spoken or written.                    Content Creation stream, Ewan\'s Book stream           \"I was sat in the barber\'s and this bloke says to me\...\" --- full anecdote preserved
  **B) Structured JSON**       Entities, decisions, specifications, parameters, relationships --- machine-readable.              Knowledge Graph (FalkorDB), Agent Skills stream        {\"entity\": \"pricing\_model\", \"type\": \"5-tier\", \"anchors\": \[\"free\", \"990\", \...\] }
  **C) Process & Logic**       How something was arrived at. The reasoning chain, alternatives considered, why one was chosen.   Process Giveaway stream, Methodology library           \"Started with 3-tier → rejected because SMBs freeze at binary choices → added middle tier as anchor\...\"
  **D) Principles & Values**   Beliefs, philosophies, non-negotiables, brand voice markers, ethical positions.                   The Manifesto stream, Brand Voice engine, Onboarding   \"Never patronise. Always assume the owner is smart --- they\'re just time-poor.\"
  ---------------------------- ------------------------------------------------------------------------------------------------- ------------------------------------------------------ ------------------------------------------------------------------------------------------------------------

**Extraction Depth: The Completeness Mandate**

The key differentiator of DocBench is extraction depth. Each source is
processed with a specific instruction set that prevents surface-level
extraction:

-   **Chain-of-reasoning extraction:** Don\'t just capture \"we chose
    X\" --- capture \"we considered A, B, and C. We rejected A because
    \[reason\]. B was tempting but \[risk\]. X won because \[specific
    insight\].\"

-   **Cross-reference flagging:** When a source mentions or relates to
    another concept, flag the connection explicitly. \"This pricing
    decision connects to the Micro-Help Library giveaway strategy
    discussed in session \[X\].\"

-   **Confidence scoring:** Every extracted item gets a confidence score
    (0.0--1.0) indicating how certain the extraction is. Verbatim quotes
    score 1.0. Inferred connections score 0.6--0.8. Speculative links
    score below 0.5 and get flagged for human review.

-   **Completeness check:** After extraction, DocBench re-reads the
    source and asks itself: \"What did I miss?\" This self-reflection
    pass catches items that the first pass skipped --- typically 8--15%
    additional extraction yield.

**DocBench Output Schema**

Each extraction produces a standardised output following the Vault
Research Ingestion Format v1.0 --- a two-layer format with YAML metadata
in FalkorDB and raw source data preserved alongside:

extraction:

source\_id: \"ref to discovery manifest\"

extracted\_at: \"ISO-8601\"

extractor\_version: \"docbench-v1.2\"

confidence\_overall: 0.94

formats:

raw\_text: { word\_count: 3200, file: \"raw/source\_123.md\" }

structured\_json: { entities: 14, decisions: 3, specs: 2 }

process\_logic: { reasoning\_chains: 5, alternatives: 8 }

principles\_values: { beliefs: 3, voice\_markers: 7 }

cross\_references: \[\"pricing\_model\", \"micro\_help\_library\"\]

completeness\_score: 0.97

self\_reflection\_pass: true

items\_added\_in\_reflection: 4

**3.3 Stage 3: Synthesis (Convergence Pipeline)**

The Convergence Pipeline was originally designed to unify outputs from
approximately 10 parallel research agents into a single deduplicated
knowledge base. In the Extraction Department, it serves the same purpose
at a larger scale --- taking all DocBench outputs and producing a
unified, conflict-resolved, cross-referenced knowledge graph.

**Core Operations**

**Deduplication**

The same concept will appear across multiple sources. \"5-tier pricing
model\" in one session, \"tiered pricing with free anchor\" in another,
\"the pricing thing we decided\" in a third. The Convergence Pipeline
uses semantic similarity (not just string matching) to identify these as
the same entity and merge them, preserving the richest description as
canonical while maintaining references to all source mentions.

**Entity Conflict Resolution**

Sometimes the same concept evolves across sessions. The pricing model
might have been 3-tier in session 12 and 5-tier by session 18.
Graphiti\'s temporal awareness --- its ability to track when facts were
true, not just what facts exist --- handles this natively. The knowledge
graph records both states with their timestamps, and the canonical entry
reflects the most recent decision while preserving the evolution
history.

**Cross-Reference Building**

This is where the knowledge graph earns its name. Every entity gets
linked to every related entity. The pricing model connects to the
giveaway strategy, which connects to the content atomisation model,
which connects to the 14-agent marketing pipeline, which connects to the
brand voice engine. These connections are typed (\"informed by\",
\"replaced by\", \"component of\", \"contradicts\") and weighted by
confidence.

**PUDDING Labelling**

PUDDING (**P**reviously **U**ndiscovered **D**omain-spanning **D**ata
**I**ntelligence for **N**ew **G**ains) is Amplified Partners\'
adaptation of Swanson\'s Literature-Based Discovery for business
knowledge. Swanson\'s original work demonstrated that disjoint
literature sets --- research fields that never cited each other ---
contained implicit connections that could lead to novel discoveries. His
famous example: connecting research on fish oil (field A) to research on
Raynaud\'s disease (field C) through shared intermediate concepts (field
B), leading to a therapeutic hypothesis later validated by clinical
research.

PUDDING applies this same ABC-model logic to business knowledge. Every
entity in the knowledge graph gets labelled with its domain tags, and
the system actively searches for entities that bridge otherwise
unconnected domains. When a concept from pricing strategy shares
structural similarity with a concept from content marketing --- and
nobody has explicitly connected them --- PUDDING flags it as a potential
discovery for human review.

**FalkorDB + Graphiti Integration**

The synthesised knowledge graph lives in FalkorDB, with Graphiti
providing the temporal intelligence layer. FalkorDB\'s sparse-matrix
architecture provides low-latency graph traversal, while Graphiti\'s
temporal tracking ensures the graph reflects the current state of
knowledge while preserving its full history. This combination supports
the hybrid search capabilities the department needs: semantic search
(\"find everything related to pricing\"), temporal search (\"what
changed about pricing after January 2026\"), and graph traversal (\"what
is connected to the pricing model within two hops\").

**3.4 Stage 4: Routing (The Switchboard)**

The Switchboard takes synthesised, quality-checked knowledge and routes
it to the appropriate output streams. This is the stage where abstract
knowledge becomes usable product.

**The Eight Output Streams**

  -------- ------------------------------------- ----------------------------------------------------------------------------------------------------------------------------------------- -----------------------------------------
  **\#**   **Stream**                            **Description**                                                                                                                           **Primary Input Formats**
  **1**    **Agent Skills**                      Becomes .md skill files for individual AI agents. The core product of the operating model.                                                Structured JSON + Process & Logic
  2        **Content Creation**                  Stories, anecdotes, creative process material → feeds the 14-agent marketing pipeline and content atomisation model.                      Raw Text + Principles & Values
  3        **Process & Logic Giveaway**          Methodologies, techniques, how-we-did-it → free content that demonstrates expertise and builds trust.                                     Process & Logic
  4        **Ewan\'s Book**                      Narrative arc material --- the founder\'s story of building an AI-powered consultancy. Needs raw voice, anecdotes, and pivotal moments.   Raw Text + Process & Logic + Principles
  5        **Complete Comprehensive Document**   The master reference document --- like amplified\_master\_v3.docx but truly comprehensive. Everything in one place.                       All four formats, deduplicated
  6        **The Manifesto**                     Core philosophy, principles, non-negotiables, and beliefs --- consolidated into one authoritative document.                               Principles & Values
  7        **Onboarding Material**               What new clients and team members need to know to get up to speed quickly.                                                                Structured JSON + Principles & Values
  8        **Commercial Products**               Taxonomy Engine, AQS (Amplified Quality System), Micro-Help Library --- packaged IP for commercial delivery.                              Structured JSON + Process & Logic
  -------- ------------------------------------- ----------------------------------------------------------------------------------------------------------------------------------------- -----------------------------------------

**Stream Quality Gates**

Every item routed to a stream passes through the Universal Quality Gate
--- three questions that must all return affirmative:

1.  **Does it help?** Does this output genuinely serve the stream\'s
    purpose, or is it filler?

2.  **Could we do better?** Is this the best version of this knowledge,
    or is there a richer source we haven\'t processed?

3.  **Would I be delighted?** If Ewan saw this output, would he say
    \"that\'s exactly right\" or \"that\'s close but missing
    something\"?

Items that fail any gate get recycled back to Stage 2 for re-extraction
with more specific prompting, or flagged for human review.

**3.5 Stage 5: Output & Quality (Gatekeeper)**

The Gatekeeper agent is the final checkpoint before any output enters
the vault, gets published, or becomes an active skill file. It exists
because the consequences of bad knowledge entering the system are
multiplicative --- one incorrect skill file could cause dozens of agent
errors downstream.

**Gatekeeper Functions**

-   **Rubric Scoring:** Every output is scored against a rubric specific
    to its destination stream. Agent skill files get scored on clarity,
    completeness, and actionability. Content gets scored on voice
    authenticity and narrative quality. Commercial products get scored
    on IP defensibility and customer value.

-   **Layer 0 Law Compliance:** Every output is checked against the
    Amplified Partners Layer 0 laws --- the non-negotiable principles
    that govern all operations. If an output contradicts a Layer 0
    principle, it is rejected regardless of quality score.

-   **Destination Routing:** Approved outputs get routed to their final
    home --- a vault directory, a skill file location, a content queue
    in the marketing pipeline, or a product component registry.

-   **Audit Trail:** Every decision the Gatekeeper makes is logged ---
    what passed, what failed, why, and what action was taken. This trail
    feeds back into the self-reflection protocol for continuous
    improvement.

**4. The Agent Roster**

Each stage of the pipeline requires specific agents with defined skill
files, model tiers, and interaction patterns. These agents map to the
existing Agent Council structure where possible.

  ----------------------- ------------------ ---------------- -------------------- --------------------------------------------- ------------------------
  **Agent**               **Stage**          **Model Tier**   **Skill File**       **Primary Role**                              **Council Mapping**
  **HoundDog**            1 --- Discovery    Tier 2 (Fast)    hounddog.md          Find all data sources, produce manifest       Scout / Reconnaissance
  **DocBench**            2 --- Extraction   Tier 1 (Best)    docbench.md          Deep extraction into 4 formats                Analyst / Deep Worker
  **Reflector**           2 --- Extraction   Tier 1 (Best)    reflector.md         Self-reflection pass on DocBench output       Quality Auditor
  **Convergence**         3 --- Synthesis    Tier 1 (Best)    convergence.md       Deduplicate, resolve, cross-reference         Chief Synthesiser
  **PUDDING Scout**       3 --- Synthesis    Tier 1 (Best)    pudding.md           Cross-domain discovery, serendipity finding   Innovation Lead
  **Switchboard**         4 --- Routing      Tier 2 (Fast)    switchboard.md       Route knowledge to 8 output streams           Traffic Controller
  **Stream Formatters**   4 --- Routing      Tier 2 (Fast)    formatter-\[n\].md   Format output for each stream\'s needs        Production Team
  **Gatekeeper**          5 --- Quality      Tier 1 (Best)    gatekeeper.md        Final QA, rubric scoring, L0 compliance       Chief Quality Officer
  **Auditor**             5 --- Quality      Tier 1 (Best)    auditor.md           Post-mortem, pipeline performance review      Self-Reflection Lead
  ----------------------- ------------------ ---------------- -------------------- --------------------------------------------- ------------------------

**4.1 Model Tier Rationale**

**Tier 1 (Best Quality)** is reserved for stages where nuance matters
--- extraction, synthesis, and quality gating. These are the stages
where missing a subtlety has downstream consequences. The cost is higher
per token, but the volume per item is manageable.

**Tier 2 (Fast)** handles discovery and routing --- stages where the
task is well-defined, the rules are clear, and speed matters more than
creative interpretation. HoundDog is crawling thousands of files; it
needs to be fast, not philosophical.

**4.2 Agent Interaction Model**

Agents interact through the pipeline, not directly with each other. Each
stage produces a defined output format that the next stage consumes.
This keeps the system modular --- any agent can be replaced or upgraded
without affecting the rest of the pipeline, provided it respects the
interface contract.

The one exception is the PUDDING Scout, which operates as a
cross-cutting agent. It has read access to the outputs of all stages and
can flag potential cross-domain discoveries at any point. When it finds
something, it creates a PUDDING Alert that gets routed to the
Switchboard for special handling --- typically to the Content Creation
or Agent Skills stream, depending on the nature of the discovery.

The Agent Council\'s believability-weighted governance applies here too.
If a PUDDING Alert conflicts with a Gatekeeper decision, the conflict is
resolved by comparing the believability scores of the two agents on the
specific topic at hand. Over time, agents that produce higher-quality
outputs accumulate higher believability in their domain, giving their
judgements more weight in disputes.

**5. The Dual Output Design**

This is one of the key innovations in the department\'s architecture,
born from Ewan\'s observation that the most valuable outputs often
aren\'t the ones you planned for.

**5.1 The Two Output Modes**

Every agent in the pipeline produces two categories of output:

┌──────────────────────────────────────────────────────┐

│ AGENT OUTPUT │

├──────────────────────┬───────────────────────────────┤

│ DETERMINISTIC │ CREATIVE │

│ ───────────── │ ──────── │

│ │ │

│ Structured │ \"Look what I found\" │

│ Rubric-scored │ Serendipitous │

│ Quality-gated │ Cross-domain │

│ Flows to next │ Flagged separately │

│ stage │ Goes to PUDDING review │

│ │ │

│ Example: │ Example: │

│ \"Extracted 14 │ \"The way Ewan described │

│ entities from │ the pricing anchor is │

│ this session\" │ structurally identical to │

│ │ loss-leader strategy in │

│ │ retail --- worth exploring\" │

└──────────────────────┴───────────────────────────────┘

**5.2 Why Both Matter**

**The Deterministic Output**

This is the machine --- the reliable, repeatable, measurable output that
keeps the pipeline running. It\'s the structured JSON that feeds the
knowledge graph, the formatted skill file that makes an agent better,
the quality-scored content piece that enters the marketing pipeline.
Without it, the department doesn\'t function.

**The Creative Output**

This is the serendipity --- the unexpected connection that a
well-designed system can surface but a rigid pipeline would suppress.
It\'s the moment when DocBench, while extracting a conversation about
agent design, notices that the governance model Ewan described bears
striking resemblance to how Tudor merchant guilds operated --- and flags
that connection for the Content Creation stream, where it becomes a
compelling article or book chapter.

The PUDDING technique is the formal mechanism for this, adapted from
Swanson\'s ABC model where disjoint literature fields contain implicit
transitive connections. But the Dual Output design goes further: it
instructs every agent, at every stage, to maintain two parallel channels
of awareness. \"Do your job\" (deterministic) and \"notice what\'s
interesting\" (creative).

**5.3 Implementation**

In practice, this is implemented entirely through skill file
instructions. Each agent\'s .md file contains a section like:

\#\# Dual Output Protocol

PRIMARY (Deterministic):

\- Complete your assigned task fully before anything else

\- Output must match the stage\'s defined schema exactly

\- Apply quality scoring to your own output

\- If below threshold, iterate before submitting

SECONDARY (Creative):

\- After completing primary output, review what you processed

\- Flag any connections to domains outside your current task

\- Flag any patterns that remind you of known frameworks

\- Flag any moments of unusual clarity or insight in the source

\- Format: { type: \'pudding\_alert\', connection: \'\...\',

confidence: 0.7, domains: \[\'pricing\', \'retail\'\] }

\- Creative outputs are NEVER required --- only genuine ones

The key instruction: creative outputs are never required. An agent that
produces zero PUDDING alerts in a run is working correctly --- it simply
didn\'t encounter anything genuinely surprising. An agent that produces
a PUDDING alert on every item is probably hallucinating connections and
needs its skill file calibrated.

**6. What Needs Building vs. What Already Exists**

One of the most important aspects of this specification is being honest
about what work is already done and what remains. The table below
provides a detailed audit.

  -------------------------------------- ------------------- ---------------------- ------------ -----------------------------------------------------
  **Component**                          **Status**          **Type**               **Effort**   **Notes**
  Vault Knowledge System                 **EXISTS**          Infrastructure         ---          4,787 files, 25 dirs, Beast server
  FalkorDB + Graphiti                    **EXISTS**          Infrastructure         ---          Knowledge graph with temporal tracking
  Convergence Pipeline (design)          **EXISTS**          Design spec            ---          Designed for \~10 parallel agents; needs scaling
  Vault Research Ingestion Format v1.0   **EXISTS**          Schema                 ---          YAML + raw source two-layer format
  Gatekeeper Agent (design)              **EXISTS**          Design spec            ---          Quality gate concept defined; needs skill file
  Agent Council + Believability          **EXISTS**          Framework              ---          Governance model with weighted trust
  Self-Reflection Protocol               **EXISTS**          Framework              ---          Post-mortem process with feedback loops
  14-Agent Marketing Pipeline            **EXISTS**          Design spec            ---          Content atomisation model, ready to consume
  PUDDING Technique (concept)            **EXISTS**          Concept                ---          Swanson adaptation defined; needs skill file
  Universal Quality Gate                 **EXISTS**          Framework              ---          3-question gate: Help? Better? Delighted?
  HoundDog Skill File                    **NEEDS WRITING**   Skill file (.md)       1--2 days    Discovery instructions + manifest schema
  DocBench Skill File                    **NEEDS WRITING**   Skill file (.md)       2--3 days    4-format extraction + self-reflection protocol
  Convergence Skill File                 **NEEDS WRITING**   Skill file (.md)       2--3 days    Dedup, conflict resolution, cross-referencing
  PUDDING Scout Skill File               **NEEDS WRITING**   Skill file (.md)       1--2 days    ABC-model cross-domain discovery
  Switchboard Skill File                 **NEEDS WRITING**   Skill file (.md)       1 day        Stream routing rules + quality gate
  Gatekeeper Skill File                  **NEEDS WRITING**   Skill file (.md)       1--2 days    Rubric scoring + L0 compliance + audit trail
  Stream Formatter Skill Files (×8)      **NEEDS WRITING**   Skill file (.md)       3--4 days    One per stream, output formatting rules
  Reflector Skill File                   **NEEDS WRITING**   Skill file (.md)       1 day        Self-reflection extraction improvement pass
  Auditor Skill File                     **NEEDS WRITING**   Skill file (.md)       1 day        Pipeline performance post-mortems
  Discovery Manifest Schema              **NEEDS CONFIG**    JSON Schema            0.5 day      Formal schema for manifest output
  Extraction Output Schema               **NEEDS CONFIG**    JSON Schema            0.5 day      Extends Vault Research Ingestion Format
  Stream Routing Rules                   **NEEDS CONFIG**    YAML config            0.5 day      Mapping from content types to streams
  Quality Rubrics (×8 streams)           **NEEDS CONFIG**    YAML config            2 days       Scoring criteria per output stream
  HoundDog Discovery Script              **NEEDS CODE**      Python (\~150 lines)   1 day        Filesystem traversal, hashing, manifest gen
  Graphiti Ingestion Adapter             **NEEDS CODE**      Python (\~200 lines)   1 day        Pushes structured JSON into Graphiti temporal graph
  Pipeline Orchestrator                  **NEEDS CODE**      Python (\~300 lines)   2 days       Chains stages, manages state, handles retries
  -------------------------------------- ------------------- ---------------------- ------------ -----------------------------------------------------

**6.1 The Ratio**

Counting the items above:

-   **Already exists:** 10 components (infrastructure, frameworks,
    design specs)

-   **Needs skill files:** 9 new .md files (\~15 days total writing
    effort)

-   **Needs configuration:** 4 schema/config files (\~3.5 days)

-   **Needs actual code:** 3 Python scripts (\~650 lines total, \~4
    days)

The department is approximately 26 components. Of these, 10 exist. Of
the 16 that need building, 13 are skill files and configuration. Only 3
require actual code.

**7. The Software Question**

> *\"I\'ve got a suspicion there\'s going to be very little software.\"
> --- Ewan Bramley*

This suspicion is correct, and it\'s worth understanding precisely why.
The Amplified Partners operating model is built on a specific
architectural insight: an AI agent with a well-written skill file and
the right tools (file search, file read/write, knowledge graph query)
can perform the vast majority of knowledge work that would traditionally
require custom software.

**7.1 Quantified Breakdown**

  ------------------------ --------------- ----------- ---------------------- -------------------------------------
  **Category**             **% of Dept**   **Items**   **Lines of Code**      **What It Is**
  **Skill Files Only**     **\~56%**       9 files     0 (markdown only)      Agent instructions in .md files
  **Configuration**        **\~25%**       4 files     0 (YAML/JSON schema)   Schemas, rubrics, routing rules
  **Actual Python Code**   **\~19%**       3 scripts   \~650 lines total      Filesystem, Graphiti, orchestration
  **\"Just Prompting\"**   *embedded*      ---         0                      Contained within skill files
  ------------------------ --------------- ----------- ---------------------- -------------------------------------

**7.2 Why So Little Code?**

Three reasons:

1.  **The AI is the software.** A traditional data pipeline would need
    code for parsing, entity extraction, deduplication, classification,
    and routing. An AI agent with a good skill file does all of this
    natively. The skill file is the program --- it\'s just written in
    English instead of Python.

2.  **The tools already exist.** FalkorDB provides graph storage and
    querying. Graphiti provides temporal knowledge graph capabilities
    with hybrid search (semantic, BM25, and graph-based). File systems
    provide storage. The AI provides processing. The only code needed is
    the thin glue between these existing tools.

3.  **The \"work at 50\" principle.** Amplified Partners\' operating
    model is predicated on giving AI agents skill files that let them
    perform at the level of 50 parallel human workers. The skill file
    investment pays for itself by eliminating the need for custom
    software --- each .md file replaces what would otherwise be
    thousands of lines of code.

**7.3 The Three Scripts That Are Needed**

The code that does need writing falls into three specific scripts:

**1. HoundDog Discovery Script (\~150 lines Python)**

This script walks the file system, computes content hashes, and outputs
the discovery manifest. An AI agent can do everything except the raw
filesystem traversal --- it needs a script that can physically read
directory structures and hash files. This is boilerplate systems code.

**2. Graphiti Ingestion Adapter (\~200 lines Python)**

This pushes structured JSON from the extraction stage into the FalkorDB
knowledge graph via the Graphiti API. It handles entity creation,
relationship creation, temporal metadata, and PUDDING labels. The
Graphiti library does the heavy lifting --- this script is just the
adapter between the department\'s output format and Graphiti\'s input
format.

**3. Pipeline Orchestrator (\~300 lines Python)**

This chains the five stages together, manages state (which sources have
been processed, which are pending, which failed), handles retries on
failure, and produces pipeline-level metrics. It\'s the conductor --- it
doesn\'t play any instruments, it just ensures they play in the right
order.

**8. How to Test This Department**

Testing a knowledge extraction department is fundamentally different
from testing traditional software. The outputs are qualitative as much
as quantitative, and \"correctness\" is partially subjective. The
testing strategy therefore uses three complementary approaches.

**8.1 Synthetic Testing**

Before running the pipeline against the full vault, run it against a
controlled subset where the expected outputs are known.

**Test Set Construction**

-   Select 50 vault files spanning different topics (pricing, agent
    design, marketing, philosophy)

-   Select 10 conversation thread exports (with known key decisions)

-   Select 5 voice captures (with known stories and insights)

-   For each source, manually create a \"ground truth\" document listing
    every valuable item it contains

-   Run the pipeline and compare extraction output against ground truth

**Metrics**

  ---------------------------- ---------------------------------------------------------------------- ------------------- -------------------------------------------------
  **Metric**                   **What It Measures**                                                   **Target**          **How to Calculate**
  **Extraction Recall**        Of all valuable items in ground truth, how many were extracted?        \> 95%              Items extracted / items in ground truth
  **Extraction Precision**     Of all items extracted, how many were actually valuable?               \> 90%              Valuable items / total items extracted
  **Routing Accuracy**         Of all routed items, how many went to the correct stream?              \> 90%              Correctly routed / total routed
  **Dedup Effectiveness**      Were duplicate concepts successfully merged?                           \> 85%              Correct merges / (merges + missed dupes)
  **Quality Gate Pass Rate**   What % of outputs pass the Universal Quality Gate on first attempt?    \> 80%              First-pass approvals / total submissions
  **PUDDING Discovery Rate**   Are cross-domain connections being found? (Too high = hallucinating)   2--8% of entities   PUDDING alerts / total entities processed
  **Self-Reflection Yield**    How much additional value does the reflection pass add?                8--15% additional   Items added in reflection / items in first pass
  ---------------------------- ---------------------------------------------------------------------- ------------------- -------------------------------------------------

**8.2 Completeness Testing**

The most important test: does the pipeline get everything? This is
tested by:

1.  Taking a conversation thread that Ewan remembers well

2.  Having Ewan list (from memory) the key decisions, stories, and
    insights from that thread

3.  Running the pipeline against that thread

4.  Comparing the pipeline\'s extraction against Ewan\'s list

5.  Counting how many of Ewan\'s items the pipeline found

6.  Noting how many items the pipeline found that Ewan forgot --- this
    is the bonus: the pipeline should find MORE than a human remembers,
    not less

**8.3 Quality Testing**

For each output stream, take 10 sample outputs and apply the Universal
Quality Gate:

-   Does it help? --- Score 1--5

-   Could we do better? --- Score 1--5

-   Would I be delighted? --- Score 1--5

Average scores below 4.0 on any dimension trigger a review of the
relevant skill file. Scores below 3.0 trigger a pause on that stream
until the issue is resolved.

**9. Implementation Plan**

The department is built in four weekly phases, each with defined
deliverables and exit criteria.

**Phase 1 --- Week 1: Foundation**

**Objective: Write the core skill files for discovery and extraction.**

  ------------------------------------ ----------------------------------------------------------------------------
  **Deliverable**                      **Exit Criteria**
  hounddog.md skill file               Can discover and catalogue 100 vault files with correct metadata
  docbench.md skill file               Can extract a single vault file into all 4 formats with confidence scoring
  reflector.md skill file              Adds 8--15% extraction yield on a DocBench output
  HoundDog discovery script (Python)   Traverses Beast server vault and produces valid manifest JSON
  Discovery manifest JSON schema       Validates against 10 sample manifests
  Extraction output JSON schema        Extends Vault Research Ingestion Format, validates against 10 samples
  ------------------------------------ ----------------------------------------------------------------------------

**Phase 2 --- Week 2: Pipeline Core**

**Objective: Write the synthesis, routing, and quality skill files. Wire
the pipeline together.**

  --------------------------------------------- ----------------------------------------------------------------------
  **Deliverable**                               **Exit Criteria**
  convergence.md skill file                     Can deduplicate 50 extracted items with \>85% accuracy
  pudding.md skill file                         Finds at least 2 valid cross-domain connections in test set
  switchboard.md skill file                     Routes 50 test items to correct streams with \>90% accuracy
  gatekeeper.md skill file                      Applies rubric scoring and correctly rejects 5 planted bad items
  Graphiti ingestion adapter (Python)           Successfully pushes 50 entities into FalkorDB with temporal metadata
  Pipeline orchestrator (Python)                Runs all 5 stages in sequence on a 10-file test set
  Stream routing rules (YAML config)            Correctly maps all content types to their target streams
  Quality rubrics for 8 streams (YAML config)   Each rubric has 3+ scoring dimensions with clear thresholds
  --------------------------------------------- ----------------------------------------------------------------------

**Phase 3 --- Week 3: Testing & Iteration**

**Objective: Run the pipeline against existing vault data, measure
performance, iterate on skill files.**

  ------------------------------------------------------ ------------------------------------------------------------------
  **Deliverable**                                        **Exit Criteria**
  Synthetic test: 50 vault files processed end-to-end    Extraction recall \>95%, routing accuracy \>90%
  Completeness test: Ewan reviews 5 thread extractions   Pipeline finds everything Ewan remembers + bonus items
  Quality test: 10 samples per stream scored             Average quality score \>4.0/5.0 across all streams
  Stream formatter skill files (×8)                      Each stream produces correctly formatted output for its consumer
  auditor.md skill file + first pipeline post-mortem     Identifies at least 3 improvement opportunities from Phase 3 run
  Skill file revisions based on test results             All metrics meet or exceed targets after revision
  ------------------------------------------------------ ------------------------------------------------------------------

**Phase 4 --- Week 4: Full Operations**

**Objective: Full pipeline operational, begin processing all historical
sessions.**

  ------------------------------------------------ -------------------------------------------------------------------------
  **Deliverable**                                  **Exit Criteria**
  Full vault processing run (4,787 files)          All files processed, manifested, extracted, synthesised
  Historical conversation thread processing        All available exports processed through pipeline
  Unified knowledge graph populated                FalkorDB contains all entities with cross-references and PUDDING labels
  8 output streams producing material              Each stream has at least 20 items in its queue
  Complete Comprehensive Document v1.0 generated   Master reference doc covers all known Amplified Partners IP
  Ongoing ingestion process documented             New sessions can be fed into the pipeline within 24 hours of creation
  ------------------------------------------------ -------------------------------------------------------------------------

**10. References & Citations**

This document draws on the following external research and tools in
addition to Amplified Partners\' internal design work:

**Knowledge Graph Infrastructure**

-   **FalkorDB ---** Open-source property graph database using sparse
    matrix representation for low-latency graph traversal.
    <https://github.com/FalkorDB/FalkorDB>

-   **Graphiti (Zep) ---** Open-source framework for building
    temporally-aware knowledge graphs for AI agent memory, supporting
    hybrid search (semantic, BM25, graph traversal).
    <https://github.com/getzep/graphiti>

-   **FalkorDB Knowledge Graph Guide ---** Technical reference for graph
    database architecture in AI applications.
    <https://www.falkordb.com/blog/graph-database-guide/>

**Literature-Based Discovery (PUDDING Foundation)**

-   **Swanson, D.R. (1986) ---** Pioneering work on undiscovered public
    knowledge and the ABC model for cross-domain discovery linking
    disjoint literature sets. The foundation for the PUDDING technique.

-   **Henry & McInnes --- \"Literature Based Discovery: Models, methods,
    and trends\" ---** Comprehensive overview of LBD in the biomedical
    domain, covering Swanson\'s models and subsequent advances.
    <https://www.sciencedirect.com/science/article/pii/S1532046417301909>

-   **Sebastian et al. --- \"A systematic review on literature-based
    discovery workflow\" (PeerJ Computer Science) ---** Review of LBD
    workflows including the ABC open and closed discovery models.
    <https://pmc.ncbi.nlm.nih.gov/articles/PMC7924697/>

**AI Context & Knowledge Management**

-   **Atlan --- \"LLM Context Window Limitations\" ---** Analysis of
    context window limitations including the \'lost in the middle\'
    problem and performance degradation with long contexts.
    <https://atlan.com/know/llm-context-window-limitations/>

-   **Local AI Zone --- \"Context Length Guide 2025\" ---**
    Comprehensive guide to AI context windows, documenting the O(n²)
    computational complexity and practical limits.
    <https://local-ai-zone.github.io/guides/context-length-optimization-ultimate-guide-2025.html>

**Knowledge Graph Extraction Pipelines**

-   **Plumber Framework --- \"Information extraction pipelines for
    knowledge graphs\" (Knowledge and Information Systems) ---**
    Framework for creating optimised knowledge extraction pipelines with
    40 reusable components.
    <https://pmc.ncbi.nlm.nih.gov/articles/PMC9823264/>

-   **Metaphacts --- \"Building massive knowledge graphs using automated
    ETL pipelines\" ---** Enterprise-scale knowledge graph construction
    methodology following FAIR data principles.
    <https://blog.metaphacts.com/building-massive-knowledge-graphs-using-automated-etl-pipelines>

**Appendix A: Glossary**

  ---------------------------- -----------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------
  **Term**                     **Definition**
  **Agent Council**            Governance framework where AI agents have believability-weighted votes on decisions. Higher past performance = more influence.
  **AQS**                      Amplified Quality System --- commercial product for quality management in SMB operations.
  **Beast Server**             The primary server hosting the Amplified Partners vault and operational infrastructure.
  **Content Atomisation**      Breaking a single piece of content into multiple smaller pieces across formats and platforms.
  **DocBench**                 The extraction engine, designed for 99.53% accuracy, outputting content in four parallel formats.
  **FalkorDB**                 Open-source property graph database using sparse matrix multiplication for high-performance graph queries.
  **Graphiti**                 Open-source framework (by Zep) for building temporally-aware knowledge graphs that track when facts were true.
  **HoundDog**                 Discovery agent that finds data across all file systems, platforms, and conversation histories.
  **Layer 0 Laws**             The non-negotiable foundational principles that govern all Amplified Partners operations. No output can contradict these.
  **Micro-Help Library**       Commercial product: bite-sized business advice and tools for SMB owners, delivered as a searchable library.
  **PUDDING**                  Previously Undiscovered Domain-spanning Data Intelligence for New Gains --- Amplified Partners\' adaptation of Swanson\'s Literature-Based Discovery for cross-domain business knowledge synthesis.
  **Skill File**               A markdown (.md) file that contains detailed instructions for an AI agent, enabling it to perform a specific role at expert level.
  **Taxonomy Engine**          Commercial product that classifies and categorises business knowledge for structured retrieval.
  **Universal Quality Gate**   Three-question filter applied to all outputs: Does it help? Could we do better? Would I be delighted?
  **\"Work at 50\"**           The principle that a well-skilled AI agent can perform at the level of 50 parallel human workers.
  ---------------------------- -----------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------

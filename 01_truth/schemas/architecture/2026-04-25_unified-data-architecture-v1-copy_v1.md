---
title: "Unified Data Architecture V1 Copy"
id: "unified-data-architecture-v1-copy"
version: 1
created: "2026-04-25"
type: "document"
topic_type: "architecture"
audience: "internal"
layer: "truth"
status: "filed"
signed_by: "Devon, 2026-04-25, devin-992682c244cf444f91e0a516498afbfd"
---

**UNIFIED DATA ARCHITECTURE**

Taxonomy, Stores, and Content Pipeline v1.0

━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

**Human Originator:** Ewan Bramley (vision, requirements, frustrations that drove this)

**AI Formaliser:** Claude via Perplexity (research, structure, pushback)

**Date:** 20 March 2026

**Status:** HYPOTHESIS --- needs validation before becoming constitutional

**PUDDING Label:** M.=.5.l (Meta, Stable, System-scale, Long-term)

**AMPLIFIED PARTNERS**

**Table of Contents**

**1. The Problem (Why This Document Exists)**

Data is scattered. Right now, Amplified Partners has information spread across Perplexity sessions, a downloads drive that\'s essentially a graveyard, various AI platforms (Claude, Grok, ChatGPT), vault files in multiple directory structures, and at least two databases that people refer to interchangeably. Things get lost. Not hypothetically --- actually lost. Solutions that already exist aren\'t surfaced because nobody (human or agent) can find them. Work gets duplicated because the previous version is buried in a session from three weeks ago, or worse, sitting in a downloads folder that nobody checks.

The vault --- 4,787 files containing approximately 3.3 million words --- is the richest asset Amplified Partners has. It contains years of monologue transcripts, business strategy thinking, frameworks, voice captures, and raw material that could fuel content creation for months. And it\'s underexploited. Not because the content isn\'t valuable, but because there\'s no consistent way to find things, no reliable labelling, no pipeline that turns raw material into published output, and no architecture that tells every system where to look for what.

Previous architecture decisions keep getting revisited because there\'s no single canonical reference. Every time the question comes up --- \'where should this data live?\' or \'what format should this be in?\' or \'is the vault a database or a file system?\' --- it gets debated from scratch. This document exists to settle that argument once. This is the canonical architecture. If a future decision contradicts this document, either this document gets formally updated with a rationale, or the decision is wrong. No more ad hoc choices.

**2. Terminology --- Getting the Words Right**

This section is critical. Ewan acknowledges he doesn\'t always use the right words --- and when different people (and agents) call the same thing by different names, confusion compounds. The following table establishes canonical terminology. Use these names. Every time. In code, in conversation, in documentation. If someone uses a wrong term, correct them and point them here.

  -------------------- --------------------------------------------------------------------------------------------------------- --------------------------------------------------- ---------------------------------------------------------------------------------------------------------------------------------
  **Canonical Name**   **What It Is**                                                                                            **What People Wrongly Call It**                     **Why the Distinction Matters**
  Document Store       The 4,787 markdown files on Beast/GitHub in /opt/amplified/vault/ --- the source of truth                 \"The vault\", \"the database\"                     These are FILES, not a database. They\'re the raw material everything else derives from. If these are lost, everything is lost.
  Knowledge Graph      FalkorDB + Graphiti --- entities, relationships, temporal edges extracted FROM the document store         \"The vault\", \"the graph vault\", \"the brain\"   This is a DERIVED INDEX. It makes the document store queryable by relationship. It can be rebuilt from the documents.
  Vector Index         HNSW embeddings in FalkorDB (replacing Qdrant) --- semantic similarity search                             \"The vector vault\", \"vector database\"           This is a DERIVED INDEX. It makes the document store searchable by meaning. It can be rebuilt from the documents.
  Process Database     PostgreSQL --- deterministic business rules, ISO 9001 processes, client templates, workflow definitions   \"SQL database\"                                    This is for STRUCTURED DATA that was never unstructured. Process definitions, business rules, scoring rubrics, client configs.
  Backup Store         Complete copy of document store + database dumps, with identical labelling                                \"The backup\"                                      Not optional. Not an afterthought. This is the disaster recovery layer.
  -------------------- --------------------------------------------------------------------------------------------------------- --------------------------------------------------- ---------------------------------------------------------------------------------------------------------------------------------

The document store is the single source of truth. The knowledge graph and vector index are derived from it. If FalkorDB fails, you rebuild it from the documents. If the documents fail, you\'re in trouble --- which is why the backup store exists. Never call three different things \'the vault\' again.

**3. What Goes Where --- The Store Architecture**

Every data type has a primary home. This table is definitive --- if you\'re unsure where something goes, look it up here. If it\'s not listed, default to the document store and raise it for review.

  ----------------------------------------------- ------------------------------------ --------------------------------------------------------- ------------------------------------------------------- ------------------------------------------------------
  **Data Type**                                   **Primary Store**                    **Why Here**                                              **Secondary Store**                                     **Notes**
  Monologue transcripts (2,214 files)             Document Store                       Raw text, authentic voice --- content gold                Knowledge Graph (entities via Graphiti)                 Never edit the originals. Ever.
  Voice captures (954 files)                      Document Store                       Same as monologues                                        Knowledge Graph                                         Keep raw for content pipeline
  Business strategy docs (292 files)              Document Store                       Reference material                                        Knowledge Graph + Vector Index                          PUDDING-labelled for discovery
  Frameworks and rubrics (69 files)               Document Store                       Constitutional documents                                  Knowledge Graph                                         These are near-immutable
  Agent architecture docs (61 files)              Document Store                       Agent reference material                                  Injected into agents via knowledge\_base.md             Agents read these directly
  ISO 9001 process templates                      Process Database (PostgreSQL)        Structured, deterministic                                 Knowledge Graph (for agent querying)                    NEVER in markdown --- too important for loose format
  Client business rules                           Process Database                     Structured, deterministic per client                      Client\'s FalkorDB namespace                            One row wrong = one process wrong
  Client personality profiles (DISC/VARK/OCEAN)   Knowledge Graph (client namespace)   Relationship data, evolves over time                      Process Database (snapshot for deterministic routing)   Privacy: P2 tokenised
  PUDDING labels and taxonomy codes               Process Database                     Lookup table --- deterministic, no ambiguity              Knowledge Graph (as node properties)                    The Curator\'s codebook
  Published content + performance metrics         Knowledge Graph                      Temporal, relational                                      Process Database (aggregate reporting)                  Graphiti tracks performance over time
  How-to guides and value content                 Document Store                       Markdown, human-readable, publishable                     Vector Index (for semantic retrieval)                   NOT in SQL --- this was wrong in initial thinking
  Client SaaS data (Xero exports, bank feeds)     Process Database                     100% accurate structured data from Level 1/2 extraction   Client\'s FalkorDB namespace                            Extraction: export-first, API-second
  Coding specs and JSON contracts                 Document Store (as .json files)      Versioned, in Git                                         Process Database (if structured configs)                See Section 6 for details
  ----------------------------------------------- ------------------------------------ --------------------------------------------------------- ------------------------------------------------------- ------------------------------------------------------

**4. The Unified Labelling System**

This is the core of the document. The labelling system must work consistently across ALL stores. Every piece of data, regardless of where it lives, carries the same metadata envelope. This is how you prevent label chaos --- one system, everywhere.

**4.1 The Metadata Envelope**

Every piece of data --- document, graph node, database row, backup file --- carries this metadata. No exceptions. If something doesn\'t have this envelope, it hasn\'t been properly ingested.

> id: \"AMP-{APQC\#}-{SEQ}-{VERSION}\" \# Unique identifier
>
> pudding\_code: \"PT3I\" \# 4-char compressed PUDDING label
>
> category: \"01-business-strategy\" \# Vault directory / logical grouping
>
> content\_type: \"principle \| framework \| sop \| technique \| case\_study \|
>
> hypothesis \| recipe \| transcript \| config \| process\"
>
> lifecycle\_stage: \"raw \| labelled \| enriched \| published \| archived\"
>
> created\_at: \"2026-03-20T01:00:00Z\" \# ISO 8601
>
> updated\_at: \"2026-03-20T01:00:00Z\"
>
> source\_platform: \"perplexity \| claude \| grok \| voice \| manual \| api\"
>
> author\_human: \"ewan\_bramley\"
>
> author\_ai: \"claude\_sonnet\_4\_6\"
>
> confidence\_band: \"high \| medium \| low \| emerging\"
>
> fact\_percentage: 85 \# Scale of Arsehole: 0-100
>
> dimensions: \[\"trust\", \"systems\", \"feedback\_loop\"\]
>
> \# Semantic dimensions for PUDDING matching
>
> privacy\_level: \"internal \| client\_tokenised \| public\"
>
> backup\_verified: false \# Has this been verified in backup store?

The id format uses the APQC process classification framework number as its root, ensuring every item maps to a recognised business process. The pudding\_code is a 4-character compressed representation of the full PUDDING taxonomy dimensions. The fact\_percentage (the \'Scale of Arsehole\') indicates how much of this content is verifiable fact versus opinion, intuition, or hypothesis. A transcript of Ewan thinking out loud might be 20%. An ISO 9001 process template should be 95%+.

**4.2 How Labels Propagate Across Stores**

The principle is simple: label once, propagate everywhere. A document is labelled in exactly one place --- its YAML frontmatter in the document store. Every other store receives that label. If any store\'s label disagrees with the document store label, the document store wins. Always. No negotiation.

The propagation flow:

1.  A document enters the Document Store (markdown file with YAML frontmatter).

2.  The Gatekeeper Agent validates and labels it (quality gate).

3.  The label metadata is written into: the file\'s YAML frontmatter (document store), the corresponding node properties in FalkorDB (knowledge graph), the embedding metadata in the vector index (for filtered retrieval), the Process Database entry if it\'s a process/rule/config, and the backup manifest.

4.  If any store\'s label disagrees with the document store label, the document store wins. Rebuild derived stores from the source of truth.

**Label Propagation Flow (textual diagram):**

> DOCUMENT STORE (source of truth)
>
> │
>
> ├── YAML frontmatter contains canonical labels
>
> │
>
> ├──→ GATEKEEPER validates ──→ Knowledge Graph (node properties)
>
> │ ──→ Vector Index (embedding metadata)
>
> │ ──→ Process Database (if structured)
>
> │ ──→ Backup Manifest (label integrity check)
>
> │
>
> └── If labels conflict → Document Store wins. Rebuild derived stores.

**4.3 The Curator\'s Role**

The Curator agent is the ONLY entity that assigns or modifies taxonomy codes. This is not a suggestion --- it\'s a hard constraint. No other agent, no human process, no automated script touches taxonomy labels without going through the Curator.

-   The compressed code system (PT3I, MS0T, etc.) is used in all machine-readable contexts --- database fields, API responses, graph node properties.

-   The expanded notation (P.\>.3.i) is used only in human-readable documentation and conversation.

-   The Curator\'s codebook (CURATOR-CODEBOOK.md) is the definitive lookup table. It lives in the document store and is version-controlled.

-   No other agent can interpret codes without asking the Curator. Agents that need to understand a taxonomy code must query the Curator, not decode it themselves.

-   This prevents Goodhart\'s Law --- agents can\'t game labels they can\'t decode. If the scoring agent can\'t read the taxonomy, it can\'t optimise for it.

**4.4 Content Lifecycle Stages**

Every piece of content moves through a defined lifecycle. These stages are not optional --- they represent the progressive enrichment of raw material into publishable output.

  ----------- -------------------------------------------------------------- ----------------------------------------------------- -----------------------------
  **Stage**   **Meaning**                                                    **Where It Lives**                                    **Who Moves It Forward**
  raw         Just arrived, unlabelled                                       Document Store (19-inbox-raw or direct to category)   Gatekeeper
  labelled    Has PUDDING code, dimensions, metadata envelope                Document Store + Knowledge Graph                      Gatekeeper
  enriched    Has Graphiti entity extraction, cross-references, chronology   Knowledge Graph                                       Graphiti ingestion pipeline
  published   Has been turned into content and released                      Knowledge Graph (with performance data)               Content pipeline agents
  archived    Historical, superseded, or deprecated                          Document Store (version history)                      Curator
  ----------- -------------------------------------------------------------- ----------------------------------------------------- -----------------------------

**5. The Content Pipeline --- Vault to Published Content**

This addresses the Gary Vaynerchuk-inspired \'slice and dice\' vision. The vault is a content goldmine, but gold in the ground is worthless until it\'s mined, refined, and shaped. This section defines the pipeline that turns raw vault material into published content across multiple formats and channels.

**5.1 Content Source Material Identification**

Not everything in the vault is content-worthy. A config file isn\'t content. A half-formed thought at 2am might be. The Content Director agent identifies source material through a structured evaluation:

1.  Scan documents with lifecycle\_stage \>= labelled. Raw, unlabelled documents are excluded --- they haven\'t been validated yet.

2.  Filter for content\_type in \[transcript, case\_study, technique, framework\]. These are the types with narrative potential.

3.  Score against the quality rubric: Is this interesting? Is there a story? Is there a lesson? Is there a contrarian take? A score below threshold means it stays in the vault as reference material, not content source.

4.  Flag passages (not whole documents) that could become content. A 45-minute monologue transcript might have three flagged passages --- the rest is filler, context, or repetition.

**5.2 The Atomisation Pipeline**

From a flagged passage or document, the pipeline creates derivatives. The key principle: one piece of source material should produce multiple outputs across multiple formats. This is where the vault\'s 3.3 million words become a content engine.

1.  **Master Document created** --- the full, attributed, chronological version. This is the canonical content record.

2.  **From the master, the Content pipeline creates derivatives:**

-   Long-form: Substack articles, blog posts --- the full argument with depth.

-   Social posts: LinkedIn, X --- multiple angles from one piece. A single insight might produce 3-5 different social posts.

-   Visual: Carousels, infographics --- the key points distilled into visual format.

-   Video scripts: Remotion-ready scripts for automated video production.

-   How-to guides: If the content teaches something, extract the teaching into a standalone guide.

-   Value giveaways: Free resources for the marketing pipeline --- PDFs, checklists, templates derived from the source material.

3.  **Each derivative carries:** full attribution back to the source document, chronological context (when was this thought? what came before and after?), and the radical attribution schema (human + AI contributors, fact percentage, confidence band).

**5.3 The \'Reminiscing\' Use Case**

This is a specific workflow Ewan described --- a process where he and an AI revisit vault content, essentially \'reminiscing\'. Finding interesting passages, reflecting on what was learnt, what was wrong, what patterns emerged. This isn\'t automated content generation. It\'s collaborative curation.

1.  Select a vault category or time period (e.g., \'everything from Q4 2025 about trust\' or \'all monologues tagged with systems thinking\').

2.  AI reads through documents sequentially in chronological order --- experiencing the evolution of thought as it happened.

3.  For each interesting passage, AI flags it with: why it\'s interesting (insight, mistake, evolution of thinking, contradiction), what content could be made from it, and what pattern it connects to (PUDDING dimensions).

4.  Output: A \'highlights reel\' document with passage references, analysis, and content suggestions.

5.  Ewan reviews, selects, directs --- the content pipeline takes it from there.

This is NOT automated end-to-end. Ewan\'s voice, judgement, and direction are the human layer. The AI does the sifting. Ewan does the deciding. This is by design and must not be \'optimised\' into full automation.

**6. Coding Agent Consumption --- What Format, What Structure**

This addresses the JSON question directly. There\'s been back-and-forth about whether the vault should be converted to JSON for agent consumption. The short answer: mostly no. The longer answer follows.

**6.1 When Raw Markdown Is Correct (Most of the Time)**

-   Agents reading context, understanding background, finding relevant information → RAG over markdown. The knowledge graph and vector index handle retrieval. No conversion needed.

-   Agent MD files (system prompts, knowledge\_base.md) → stay as markdown. Agents read markdown natively. It\'s what they\'re trained on.

-   Principles, rubrics, frameworks → stay as markdown with YAML frontmatter. The frontmatter gives structure. The body gives nuance.

**6.2 When JSON Is Correct**

-   Process definitions that agents EXECUTE (not just read) → JSON schema with explicit fields. An agent building a workflow needs unambiguous step definitions.

-   API contracts between agents → JSON. The message format between agents must be parseable, not interpretable.

-   Client config files (like jesmond-plumbing.yaml) → YAML or JSON, structured. Per-client settings need deterministic reading.

-   Curator codebook entries → JSON for machine consumption, markdown for human docs. The codebook has two representations.

-   Build specifications for the Cove coding pipeline → JSON with the complete spec. No interpretation needed, no interpretation wanted.

**6.3 The Conversion Rule**

***Convert to JSON only when the consumer needs to ACT on structured fields, not when it needs to UNDERSTAND text.***

Examples:

-   A coding agent building a webhook → needs a JSON spec with endpoint, auth, payload schema. Correct.

-   A coding agent understanding why the webhook exists → reads the markdown design doc via RAG. Correct.

-   Converting the entire vault to JSON \'so there\'s no interpretation\' → WRONG. Massive effort, destroys the content value of raw text, and the knowledge graph already does the structured extraction.

The vault\'s value is in its raw, authentic, unstructured text. That\'s where Ewan\'s voice lives. That\'s what the content pipeline needs. Converting it to JSON would be like transcribing a conversation into a spreadsheet --- you\'d preserve the data but lose everything that makes it useful.

**7. The Attribution Layer**

Attribution runs alongside everything else, not as a separate step. It\'s baked into the metadata envelope, the content pipeline, and the knowledge graph. This isn\'t an afterthought --- it\'s how Amplified Partners maintains intellectual honesty about what\'s human-generated, what\'s AI-generated, and what\'s a collaboration.

-   Every document already carries the radical attribution schema in YAML frontmatter (see Section 4.1). The author\_human and author\_ai fields are mandatory. The fact\_percentage quantifies the ratio of verifiable fact to opinion.

-   When content is created from a source, the derivative carries attribution back to the source. You can always trace a LinkedIn post back to the monologue transcript it came from.

-   Chronology is embedded in the created\_at field and in Graphiti\'s temporal edges. Graphiti\'s bi-temporal model means you can query both \'when was this said?\' and \'when did we learn this?\'

-   Vision and history --- the chronological evolution of ideas --- is queryable through Graphiti. Ask \'how did Ewan\'s thinking about trust evolve from 2024 to 2026?\' and the temporal edges give you the trajectory.

-   Pattern analysis (\'the shit pattern\') --- analysing mistakes, human faults, agent faults --- is a specific knowledge graph query: find all documents where content\_type = case\_study AND dimensions include \'failure\', or where the reminiscing workflow flagged something as a mistake. This is how you learn from errors systematically instead of accidentally.

**8. Backup and Data Loss Prevention**

This is where the frustration lives. Things get lost. Data disappears into downloads folders, AI sessions expire, exports get forgotten, and one day you realise the thing you need was in a Perplexity conversation from six weeks ago that\'s now gone. This section is non-negotiable. Every item here is a requirement, not a suggestion.

**8.1 What Gets Backed Up**

**EVERYTHING. No exceptions.**

  ------------------------------- -------------------------------------------------------- ---------------------------------- ----------------------------------------- ---------------------------------
  **Store**                       **Backup Method**                                        **Frequency**                      **Location**                              **Verified?**
  Document Store                  Git push to GitHub (canonical) + rsync to backup drive   Every commit + daily full          GitHub repo + external drive              Git hash verification
  Knowledge Graph (FalkorDB)      RDB snapshots + AOF persistence                          Hourly snapshot + continuous AOF   Beast local + external drive              Restore test monthly
  Vector Index                    Rebuilt from document store if lost                      N/A --- derived data               N/A                                       Rebuild test quarterly
  Process Database (PostgreSQL)   pg\_dump                                                 Daily                              Beast local + external drive              Restore test monthly
  Downloads/Exports               Automated sweep from downloads to vault inbox            Daily                              Document Store (then backed up via Git)   Gatekeeper validates on arrival
  ------------------------------- -------------------------------------------------------- ---------------------------------- ----------------------------------------- ---------------------------------

**8.2 The Label Integrity Check**

Every backup includes a manifest --- a list of every item\'s ID and its metadata envelope. On restore:

1.  Compare manifest labels to restored data labels.

2.  Any mismatch → flag for human review. Do not silently accept mismatched labels.

3.  This prevents the \'things with wrong labels getting silently restored\' problem. A backup with wrong labels is worse than no backup --- it gives you false confidence.

**8.3 The Export Problem**

Data from Perplexity, Claude, and other AI platforms is hard to export. This is a known problem with no perfect solution. Current approach:

-   Perplexity: Use whatever export method becomes available. In the meantime, save important outputs to the vault manually or via the Gatekeeper. Don\'t trust that sessions will persist.

-   Claude: Export conversation history, process through the Gatekeeper. Claude conversations contain valuable reasoning chains --- treat them as source material.

-   Other platforms: Same pattern --- get the data out, get it into the document store, let the pipeline label and index it. Platform-specific data is only safe once it\'s in the vault.

-   The downloads drive: Automated daily sweep. Anything sitting in downloads for \>24 hours gets flagged. Anything relevant gets ingested. Nothing sits there forgotten. The downloads folder is a transit lounge, not a storage unit.

**9. Pushback --- Where This Plan Has Weaknesses**

No architecture document worth reading pretends it\'s perfect. Here are the genuine risks and weaknesses in this plan, stated honestly so they can be monitored and mitigated rather than discovered painfully later.

**1. Single point of failure: the Gatekeeper.**

If the Gatekeeper is poorly configured or the quality gate is too loose, garbage gets labelled and propagated everywhere. Bad labels in the document store become bad labels in the knowledge graph, the vector index, and every derived system. Mitigation: The Gatekeeper has its own test suite (the recall batteries from the taxonomy testing framework). Run them regularly. Treat Gatekeeper failures as P1 incidents.

**2. Label drift over time.**

As the taxonomy evolves (and it will), older documents may have outdated labels. A document labelled in March 2026 might use taxonomy codes that mean something different by December 2026. Mitigation: The Curator runs periodic re-labelling sweeps. Version history means you can see what changed and when. The codebook itself is version-controlled.

**3. The \'enriched\' step is expensive.**

Graphiti entity extraction costs approximately £0.70--1.20 per full vault run and takes 20--40 hours. For a 4,787-file vault, that\'s not trivial. Mitigation: Incremental ingestion with \--resume. Only new or changed documents get processed. The current checkpoint is at 327/4,664 --- resume from there, don\'t restart.

**4. Human bottleneck in the content pipeline.**

Ewan must review and direct content creation. This is by design --- his voice, his judgement, his editorial direction. But it doesn\'t scale. If the vault produces 50 content candidates per week and Ewan can review 10, you have a backlog. Mitigation: Templates and rubrics reduce the decision load. The AI does the sifting and ranking. Ewan does the choosing.

**5. The Process Database is a new system.**

It doesn\'t exist yet in production. Adding PostgreSQL as the deterministic business rules layer is architecturally correct but adds operational complexity to Beast. Another service to monitor, back up, and maintain. Mitigation: PostgreSQL is already installed on Beast. Start with a single schema for ISO 9001 templates and expand only when proven.

**6. Backup verification is manual.**

Saying \'restore test monthly\' requires someone to actually do it. History suggests this will be skipped under time pressure. Mitigation: Automate with a cron job that restores to a test namespace and runs the label integrity check. If the cron job fails, it notifies. No human action required unless something breaks.

**7. The vault\'s dual-purpose design creates tension.**

Raw transcripts are great for content but messy for agent reference. Graphiti\'s entity extraction is meant to resolve this --- agents query the graph, the content pipeline reads the raw text. But if entity extraction quality is poor, agents get poor data. Mitigation: The gold dataset approach from the extraction methodology --- measure extraction quality per document type and set minimum thresholds.

**10. Implementation Priority**

This is the order of operations. Resist the temptation to jump to the exciting bits (content pipeline, reminiscing workflow) before the foundations are solid. You can\'t build a content engine on top of data that might disappear.

  -------------- ----------------------------------------------------------------------- ------------------------------------------------------------------------------------ -------------------------------------------
  **Priority**   **What**                                                                **Why First**                                                                        **Effort**
  1              Lock down backup pipeline                                               Cannot do anything else safely until data loss prevention is solid                   1 week
  2              Standardise YAML frontmatter on all vault documents                     The metadata envelope must be consistent before any derived stores can trust it      2 weeks (automated with Gatekeeper sweep)
  3              Complete Graphiti ingestion (\--resume from the 327/4,664 checkpoint)   Knowledge graph is useless until populated                                           1--2 weeks (runs in background)
  4              Build the label propagation pipeline                                    \'Label once, propagate everywhere\' requires code that syncs labels across stores   1 week
  5              Set up PostgreSQL schema for process definitions                        Deterministic business rules need a proper home                                      1 week
  6              Build the content source identification workflow                        Start extracting value from the vault for publishing                                 2 weeks
  7              Automate the downloads sweep                                            Stop losing data from the downloads folder                                           2 days
  -------------- ----------------------------------------------------------------------- ------------------------------------------------------------------------------------ -------------------------------------------

Total estimated effort: 8--10 weeks, with priorities 1--3 running in parallel where possible. Priority 7 is small enough to slot in alongside anything else --- there\'s no excuse for not doing it immediately.

**Appendix A: Glossary of Corrected Terms**

Quick reference. Copy this into any onboarding document, agent system prompt, or team handbook.

  -------------------- ----------------------------------------------------------------- ---------------------------------------------------
  **Canonical Name**   **What It Is**                                                    **Don\'t Call It**
  Document Store       4,787 markdown files on Beast/GitHub in /opt/amplified/vault/     \"The vault\", \"the database\"
  Knowledge Graph      FalkorDB + Graphiti --- entities, relationships, temporal edges   \"The vault\", \"the graph vault\", \"the brain\"
  Vector Index         HNSW embeddings in FalkorDB --- semantic similarity search        \"The vector vault\", \"vector database\"
  Process Database     PostgreSQL --- deterministic business rules, processes, configs   \"SQL database\"
  Backup Store         Complete copy of document store + database dumps                  \"The backup\" (as if it were optional)
  Metadata Envelope    The standard YAML block every data item carries                   \"Tags\", \"labels\" (too vague)
  PUDDING Code         4-character compressed taxonomy label (e.g., PT3I)                \"Category\", \"type\" (too generic)
  Gatekeeper           Agent that validates and labels incoming data                     \"The filter\", \"intake agent\"
  Curator              Agent that assigns and manages taxonomy codes                     \"The labeller\", \"tagger\"
  Graphiti             Entity extraction and temporal knowledge graph engine             \"The AI\", \"the extractor\"
  -------------------- ----------------------------------------------------------------- ---------------------------------------------------

**Appendix B: The Metadata Envelope Schema (Full YAML)**

Complete schema with all fields and valid values. This is the definitive reference for any system that reads or writes metadata envelopes.

> \# ── Metadata Envelope Schema v1.0 ──
>
> id:
>
> format: \"AMP-{APQC\#}-{SEQ}-{VERSION}\"
>
> example: \"AMP-7110-0042-v1\"
>
> description: Unique identifier. APQC\# is the process classification
>
> number. SEQ is a zero-padded sequence. VERSION tracks
>
> major revisions.
>
> pudding\_code:
>
> format: 4-character string
>
> example: \"PT3I\"
>
> description: Compressed PUDDING taxonomy label. Only the Curator
>
> assigns or modifies this value.
>
> valid\_pattern: \'\[A-Z\]\[A-Z0-9\]\[0-9\]\[A-Za-z\]\'
>
> category:
>
> format: \"NN-kebab-case\"
>
> example: \"01-business-strategy\"
>
> description: Maps to vault directory structure. Two-digit prefix
>
> for sort order.
>
> valid\_values:
>
> \- 01-business-strategy
>
> \- 02-client-delivery
>
> \- 03-marketing-content
>
> \- 04-agent-architecture
>
> \- 05-frameworks-rubrics
>
> \- 06-iso-processes
>
> \- 07-monologues
>
> \- 08-voice-captures
>
> \- 09-case-studies
>
> \- 10-coding-specs
>
> \- 19-inbox-raw
>
> content\_type:
>
> valid\_values:
>
> \- principle \# Core belief or operating rule
>
> \- framework \# Structured model or mental model
>
> \- sop \# Standard operating procedure
>
> \- technique \# Specific method or tactic
>
> \- case\_study \# Real-world example with analysis
>
> \- hypothesis \# Untested idea or theory
>
> \- recipe \# Step-by-step instructions
>
> \- transcript \# Raw monologue or conversation
>
> \- config \# System configuration
>
> \- process \# Business process definition
>
> lifecycle\_stage:
>
> valid\_values:
>
> \- raw \# Just arrived, unlabelled
>
> \- labelled \# Has PUDDING code and metadata
>
> \- enriched \# Has entity extraction + cross-refs
>
> \- published \# Released as content
>
> \- archived \# Superseded or deprecated
>
> created\_at:
>
> format: ISO 8601 with timezone
>
> example: \"2026-03-20T01:00:00Z\"
>
> updated\_at:
>
> format: ISO 8601 with timezone
>
> example: \"2026-03-20T01:00:00Z\"
>
> source\_platform:
>
> valid\_values:
>
> \- perplexity
>
> \- claude
>
> \- grok
>
> \- voice \# Dictated via voice capture
>
> \- manual \# Typed directly
>
> \- api \# Ingested via API
>
> author\_human:
>
> format: \"snake\_case full name\"
>
> example: \"ewan\_bramley\"
>
> description: The human who originated the content.
>
> author\_ai:
>
> format: \"model\_name\_version\"
>
> example: \"claude\_sonnet\_4\_6\"
>
> description: The AI model that contributed. Null if
>
> purely human-authored.
>
> confidence\_band:
>
> valid\_values:
>
> \- high \# Well-established, tested, proven
>
> \- medium \# Reasonable belief, some evidence
>
> \- low \# Early thinking, limited evidence
>
> \- emerging \# Brand new, speculative
>
> fact\_percentage:
>
> type: integer
>
> range: 0-100
>
> description: Scale of Arsehole. 0 = pure opinion.
>
> 100 = fully verifiable fact.
>
> example: 85
>
> dimensions:
>
> type: array of strings
>
> description: Semantic dimensions for PUDDING matching.
>
> Maps to the taxonomy\'s dimension axes.
>
> example: \[\"trust\", \"systems\", \"feedback\_loop\"\]
>
> privacy\_level:
>
> valid\_values:
>
> \- internal \# Amplified Partners eyes only
>
> \- client\_tokenised \# Contains client data, P2 tokenised
>
> \- public \# Safe for publication
>
> backup\_verified:
>
> type: boolean
>
> description: Has this item been confirmed present in
>
> the backup store with matching labels?

**Appendix C: Linear Issues This Affects**

The following Linear issues are directly affected by or referenced in this architecture document. Update these issues to reference this document as the canonical architecture source.

  ----------- ----------------------------------------------------------------- -----------------------------------------------------------------------------------------------------------------------------------------------------
  **Issue**   **Title / Area**                                                  **How This Document Affects It**
  COV-243     Dual-purpose design (vault as content source + agent reference)   Section 9 addresses this tension directly. Graphiti entity extraction is the resolution --- agents read the graph, content pipeline reads raw text.
  ---         Taxonomy labelling and PUDDING system                             Section 4 defines the complete labelling system. All taxonomy work should reference this document for the canonical metadata envelope.
  ---         Graphiti ingestion pipeline                                       Section 10 (Priority 3) defines the resumption point at 327/4,664. The incremental \--resume approach is mandatory.
  ---         Backup and data loss prevention                                   Section 8 is the definitive backup architecture. Any backup-related issue should reference Section 8.
  ---         Content pipeline and publishing workflow                          Section 5 defines the end-to-end pipeline from vault to published content. Content-related issues should align with this flow.
  ---         PostgreSQL process database setup                                 Section 10 (Priority 5) defines the implementation plan. Start with ISO 9001 schema.
  ----------- ----------------------------------------------------------------- -----------------------------------------------------------------------------------------------------------------------------------------------------

As specific Linear issue numbers are created for the implementation priorities in Section 10, add them to this appendix. Every architectural decision made during implementation should reference this document by section number.

━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

**END OF DOCUMENT**

*Status: HYPOTHESIS --- needs validation before becoming constitutional*

*Next step: Ewan reviews, challenges, and either ratifies or revises.*

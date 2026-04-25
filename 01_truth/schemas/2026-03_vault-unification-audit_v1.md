---
title: "Vault Unification Audit"
id: "vault-unification-audit"
version: 1
created: 2026-04-25
last_validated: 2026-04-25
type: document
topic_type: reference
status: imported
source_file: "vault-unification-audit.docx"
signed_by: "Devon, 2026-04-25, devin-992682c244cf444f91e0a516498afbfd"
---

**VAULT UNIFICATION AUDIT**

Framework Documents

Date: 2026-03-17

PUDDING Label: M.=.5.l --- Meta, Stable, System-scale, Long-term

*Attribution: Ewan Bramley (originator, directive) × Perplexity (researcher, auditor)*

PROBLEM STATEMENT

13 framework documents were created between March 14-17, 2026. They share principles but define them independently. They need to follow vault guidelines, be maximally useful across multiple contexts, and cross-reference rather than duplicate.

PART 1: VAULT FORMAT COMPLIANCE CHECK

Required by Vault Guidelines

Source: Pudding Technique Skill, Radical Attribution Schema, Operational Protocol

  -------------------------------------------------------------------- --------------------------------- --------------------------------------------------
  **Requirement**                                                      **Source**                        **Currently Present?**
  YAML frontmatter with type, expert, dimensions, actionable, status   Pudding Technique Part 7          NO --- none of the 13 docs have it
  PUDDING label (WHAT.HOW.SCALE.TIME)                                  Pudding Technique Part 4          PARTIAL --- only existing vault docs have labels
  Radical Attribution block                                            Radical Attribution Schema v1.0   NO --- session-created docs have no attribution
  pudding\_score (0-20 rubric)                                         Pudding Technique Part 5          NO
  created and last\_validated dates                                    Pudding Technique Part 7          PARTIAL --- dates exist but not in YAML format
  lbd\_attribution                                                     Pudding Technique Part 7          NO
  Committed to GitHub                                                  Operational Protocol Law 1        NO --- none of the 13 are committed
  -------------------------------------------------------------------- --------------------------------- --------------------------------------------------

**Verdict: None of the 13 framework documents are vault-compliant.**

PART 2: THE RELABELLING QUESTION

The documents don\'t just need PUDDING labels. They need to be restructured so the same content can serve multiple contexts without duplication.

Approach A: DITA Topic Typing

DITA (Darwin Information Typing Architecture) is the established standard for reusable documentation. It sorts every content unit into one of three types:

  ----------- ------------------------- --------------------------------------------------------
  **Type**    **Answers**               **Example in Your System**
  Concept     \"What is this?\"         \"What is AMPS?\" --- the definition, the philosophy
  Task        \"How do I do this?\"     \"How to score a process using AMPS\" --- step-by-step
  Reference   \"What are the facts?\"   \"AMPS dimension weights table\" --- the lookup data
  ----------- ------------------------- --------------------------------------------------------

**Why this matters:**

Right now, each of your 13 documents mixes all three types. The AMPS doc contains the concept (what it is), the task (how to score), AND the reference (the scoring table). This means:

-   If an agent needs just the scoring table, it has to parse the whole document

-   If a client needs just the concept, they get buried in implementation detail

-   If Cove needs just the procedure, it has to strip out the philosophy

**The fix: Each document becomes 2-3 vault files typed as Concept, Task, or Reference.**

Approach B: Faceted Taxonomy

Your PUDDING labels already ARE a faceted taxonomy. Add two more facets:

  ----------- ------------------------------------------------- -----------------
  **Facet**   **Values**                                        **Purpose**
  AUDIENCE    internal / client / agent / coder                 Who reads this?
  LAYER       principle / methodology / procedure / reference   What depth?
  ----------- ------------------------------------------------- -----------------

**Maps to your four rubric categories:**

-   Content Creation → AUDIENCE: client, LAYER: principle or methodology

-   Master Document → AUDIENCE: internal, LAYER: methodology

-   Process Documentation → AUDIENCE: internal or client, LAYER: procedure

-   Coding Document → AUDIENCE: coder or agent, LAYER: reference

Approach C: Atomic Documentation

Your Gap Analysis framework already uses atom IDs: AMP-{APQC\#}-{SEQ}-{VERSION}. The APQC Process Classification Framework provides a 5-level hierarchy from Category down to Task.

Recommendation: Combine All Three

**You already have the pieces:**

-   PUDDING labels = faceted taxonomy (WHAT.HOW.SCALE.TIME)

-   Atom IDs = APQC-based atomic units (AMP-{APQC\#}-{SEQ}-{VERSION})

-   Missing piece = DITA topic typing (Concept / Task / Reference)

PART 3: HOW EACH DOCUMENT SHOULD SPLIT

Document 1: AMPS (Amplified Process Maturity Score)

*Currently one document mixing concept + task + reference.*

  ------------------------ ---------------- -------------------------------------------------------------------------------- ------------------------
  **New File**             **Topic Type**   **Content**                                                                      **Audience**
  AMPS-concept.md          Concept          What AMPS is, why 0-10 scale, the 6 dimensions                                   internal, client
  AMPS-task-scoring.md     Task             Step-by-step scoring: Decompose→Score→Research→Design→Test→Validate→Reassemble   internal, agent, coder
  AMPS-ref-dimensions.md   Reference        Dimension weights table, scoring thresholds (7.0 ship, 9.0 gold), formula        agent, coder
  ------------------------ ---------------- -------------------------------------------------------------------------------- ------------------------

**Agents only need the reference. Clients only need the concept. Coders need the task + reference.**

Document 2: Build Quality Framework

  ---------------------- ---------------- ---------------------------------------------------------------------------- ------------------------
  **New File**           **Topic Type**   **Content**                                                                  **Audience**
  BQF-concept.md         Concept          6-stage pipeline: V-Model + CMMI + DMAIC + PDCA + Quality Gates + Pudding    internal
  BQF-task-pipeline.md   Task             Step-by-step: Decompose → Score → Research → Test → Reassemble → Attribute   internal, agent, coder
  BQF-ref-PRS.md         Reference        PRS formula, data size estimates, compute costs, ship thresholds             agent, coder
  ---------------------- ---------------- ---------------------------------------------------------------------------- ------------------------

**CRITICAL: BQF-task-pipeline.md step \"Score\" MUST reference AMPS-ref-dimensions.md --- NOT redefine the scoring.**

Document 3: RIC (Rapid Intelligence Cycle)

  ------------------- ---------------- ------------------------------------------------------------------ ------------------
  **New File**        **Topic Type**   **Content**                                                        **Audience**
  RIC-concept.md      Concept          What RIC is, why 4 velocity tiers, the PUDDING→Kaizen transition   internal, client
  RIC-task-cycle.md   Task             How to run a RIC cycle at each velocity tier                       internal, agent
  RIC-ref-rubric.md   Reference        7-dimension evaluation rubric, ship threshold                      agent, coder
  ------------------- ---------------- ------------------------------------------------------------------ ------------------

**CRITICAL: RIC-ref-rubric.md ship threshold MUST reference AMPS-ref-dimensions.md --- same 7.0 threshold.**

Document 4: AMF (Amplified Methodology Framework)

  ---------------- ---------------- ------------------------------------------------------------------------ ------------------
  **New File**     **Topic Type**   **Content**                                                              **Audience**
  AMF-map.md       Map              Assembly document: references AMPS, BQF, RIC, APDS, Gap Analysis, etc.   internal
  AMF-concept.md   Concept          What the unified methodology is, how the pieces fit together             internal, client
  ---------------- ---------------- ------------------------------------------------------------------------ ------------------

**The AMF should NOT contain the content of all other frameworks. It should be a map that points to them.**

Document 5: Master Process Document

  ---------------------- ---------------- --------------------------------------------------------------------------- -----------------
  **New File**           **Topic Type**   **Content**                                                                 **Audience**
  MPD-concept.md         Concept          What the operational design is, the 24-hour cycle philosophy                internal
  MPD-task-daily.md      Task             Daily operational cycle: chaos testing, Kaizen reviews, data audit trails   internal, agent
  MPD-ref-enforcers.md   Reference        10 Enforcer roles, escalation rules                                         agent, coder
  ---------------------- ---------------- --------------------------------------------------------------------------- -----------------

Document 6: Gap Analysis & Finite Lenses

  ---------------------- ---------------- ------------------------------------------------------------------ ------------------
  **New File**           **Topic Type**   **Content**                                                        **Audience**
  GAP-concept.md         Concept          What the 10 gaps are, why 12 lenses, the three data pools          internal, client
  GAP-task-analysis.md   Task             How to run a gap analysis: 5 taxonomy layers, atom ID assignment   internal, agent
  GAP-ref-lenses.md      Reference        12 lens definitions, atom ID format                                agent, coder
  ---------------------- ---------------- ------------------------------------------------------------------ ------------------

Document 7: APDS (Amplified Pudding Discovery System)

  ----------------------- ---------------- ----------------------------------------------------------- ------------------------
  **New File**            **Topic Type**   **Content**                                                 **Audience**
  APDS-concept.md         Concept          What automated pudding discovery is, the 5-stage pipeline   internal, client
  APDS-task-pipeline.md   Task             Harvest → Extract → Label → Match → Score & Surface         internal, agent, coder
  APDS-ref-config.md      Reference        SearXNG config, scoring thresholds, dashboard endpoint      coder
  ----------------------- ---------------- ----------------------------------------------------------- ------------------------

Document 8: Operations Register

  ----------------------- ---------------- ------------------------------------------------- -----------------
  **New File**            **Topic Type**   **Content**                                       **Audience**
  OPS-REG-task.md         Task             How to log operations, what gets recorded, when   internal, agent
  OPS-REG-ref-fields.md   Reference        Field definitions, required vs optional, format   agent, coder
  ----------------------- ---------------- ------------------------------------------------- -----------------

Document 9: Visual Polish System

  ----------------------- ---------------- --------------------------------------------- -----------------
  **New File**            **Topic Type**   **Content**                                   **Audience**
  VPS-concept.md          Concept          What visual polish means, quality standards   internal
  VPS-task-checklist.md   Task             Step-by-step polish checklist                 internal, agent
  ----------------------- ---------------- --------------------------------------------- -----------------

Document 10: Vault Research Ingestion Format

  --------------------- ---------------- --------------------------------------------------------- ------------------------
  **New File**          **Topic Type**   **Content**                                               **Audience**
  VRIF-task-ingest.md   Task             How to format and ingest research (2-layer: YAML + raw)   internal, agent, coder
  VRIF-ref-format.md    Reference        ID format, YAML schema, field definitions                 agent, coder
  --------------------- ---------------- --------------------------------------------------------- ------------------------

Document 11: Content Creation

  -------------------------- ---------------- -------------------------------------------------------------- ------------------
  **New File**               **Topic Type**   **Content**                                                    **Audience**
  CONTENT-concept.md         Concept          Gary Vee pyramid, story structure, platform tones              internal, client
  CONTENT-task-create.md     Task             How to create content from vault material                      internal, agent
  CONTENT-ref-templates.md   Reference        Case study template, social post template, voice note format   agent
  -------------------------- ---------------- -------------------------------------------------------------- ------------------

Document 12: Master Document (OS Bible)

  ---------------------- ---------------- ------------------------------------------------ --------------
  **New File**           **Topic Type**   **Content**                                      **Audience**
  OS-BIBLE-map.md        Map              Assembly of all 14 client-facing sections        client
  OS-BIBLE-ref-json.md   Reference        The 1,322-line JSON spec (machine-readable OS)   coder, agent
  ---------------------- ---------------- ------------------------------------------------ --------------

Document 13: Coding Document

  ---------------------- ---------------- --------------------------------------------------------------- --------------
  **New File**           **Topic Type**   **Content**                                                     **Audience**
  CODING-concept.md      Concept          Architecture decisions, tech stack rationale, Cove philosophy   coder
  CODING-task-build.md   Task             How to convert a vault document into code via Cove              coder, agent
  CODING-ref-stack.md    Reference        Tech stack table, API endpoints, database schemas               coder
  ---------------------- ---------------- --------------------------------------------------------------- --------------

PART 4: THE DEPENDENCY MAP

**Cross-references that MUST be wired (referenced, not duplicated):**

> SOUL.md (immutable --- everything points up to this)
>
> ├── Operational Protocol v1.0 (8 laws)
>
> │ └── Referenced by: ALL documents
>
> ├── Radical Attribution Schema v1.0
>
> │ └── Referenced by: ALL documents
>
> ├── AMPS-ref-dimensions.md ← SINGLE DEFINITION OF SCORING
>
> │ ├── Referenced by: BQF-task-pipeline.md (Score step)
>
> │ ├── Referenced by: RIC-ref-rubric.md (ship threshold)
>
> │ ├── Referenced by: MPD-concept.md (process scoring)
>
> │ └── Referenced by: GAP-task-analysis.md (atom scoring)
>
> ├── AMF-map.md ← ASSEMBLY DOCUMENT
>
> │ ├── Includes: AMPS, BQF, RIC, APDS, GAP, MPD (all files)
>
> │ └── Includes: OPS-REG, VPS, VRIF (all files)
>
> ├── OS-BIBLE-map.md ← CLIENT-FACING ASSEMBLY
>
> │ └── Pulls from: AMF concept files (audience: client)
>
> ├── CONTENT-\* ← MARKETING LAYER
>
> │ └── Sources from: OS-BIBLE + SOUL.md
>
> └── CODING-\* ← BUILD LAYER
>
> ├── Sources from: OS-BIBLE-ref-json.md
>
> └── Constrained by: BQF-task-pipeline.md

PART 5: YAML FRONTMATTER TEMPLATE

Every document gets this (combining existing vault guidelines + new facets):

> \-\--
>
> \# Identity
>
> title: \"AMPS Scoring Dimensions Reference\"
>
> id: \"AMPS-ref-dimensions\"
>
> version: \"1.0\"
>
> created: \"2026-03-16\"
>
> last\_validated: \"2026-03-17\"
>
> \# Vault Classification
>
> type: reference
>
> topic\_type: reference \# concept \| task \| reference \| map
>
> audience: \[agent, coder\]
>
> layer: reference \# principle \| methodology \| procedure \| reference
>
> \# PUDDING
>
> pudding\_label: \"M.=.0.∞\"
>
> pudding\_score: 16
>
> dimensions:
>
> \- measurement
>
> \- systems
>
> \- threshold
>
> \# Hierarchy
>
> parent: \"AMPS-concept\"
>
> children: \[\]
>
> referenced\_by: \[\"BQF-task-pipeline\", \"RIC-ref-rubric\"\]
>
> references: \[\"SOUL\"\]
>
> \# Expert & Lineage
>
> expert: \[BRAMLEY, CLAUDE\]
>
> intellectual\_lineage:
>
> \- name: \"CMMI Institute\"
>
> concept: \"Capability Maturity Model\"
>
> \# Status
>
> actionable: ready\_to\_use
>
> status: tested\_internal
>
> \# Attribution
>
> attribution:
>
> human:
>
> \- name: \"Ewan Bramley\"
>
> role: \"originator\"
>
> ai\_contributors:
>
> \- name: \"Perplexity\"
>
> provider: \"Perplexity AI\"
>
> role: \"researcher\"
>
> fact\_percentage: 85
>
> confidence\_band: \"high\"
>
> lbd\_attribution: \"Swanson (1986) ABC Model\"
>
> \-\--

PART 6: TOTAL FILE COUNT

Current: 13 monolithic documents (none in vault)

**Proposed: 33 vault-compliant files + 2 map documents = 35 files**

  --------------------------------- ------------------------------
  **Category**                      **Files**
  AMPS                              3 (concept, task, reference)
  Build Quality Framework           3
  RIC                               3
  AMF                               2 (map + concept)
  Master Process Document           3
  Gap Analysis & Finite Lenses      3
  APDS                              3
  Operations Register               2
  Visual Polish System              2
  Vault Research Ingestion Format   2
  Content Creation                  3
  OS Bible                          2 (map + JSON ref)
  Coding Document                   3
  TOTAL                             35
  --------------------------------- ------------------------------

**All filed under vault/03-frameworks-and-rubriks/ with clear naming:**

*{SYSTEM}-{topic\_type}.md --- e.g., AMPS-concept.md, AMPS-task-scoring.md, AMPS-ref-dimensions.md*

PART 7: WHAT THIS ENABLES

For Agents

An agent running a scoring task loads ONLY AMPS-ref-dimensions.md --- 1 file instead of parsing 40 pages of AMF.

For Clients

A client sees ONLY concept files (audience: client) --- no implementation detail, no code.

For Cove (Coding Pipeline)

Cove loads reference + task files (audience: coder) --- structured specs it can convert to code.

For Content Creation

Marketing agents load concept files (audience: client) + CONTENT-task-create.md --- voice-matched content from structured sources.

For PUDDING

Every file has dimensions and PUDDING labels --- the APDS can match across ALL 35 files for cross-domain connections.

For FalkorDB/Graphiti Ingestion

Smaller, typed files ingest better. Each creates cleaner entity nodes. Cross-references become explicit graph edges.

SOURCES

-   [Heretto --- DITA Topic Types: Concept, Task, Reference](https://www.heretto.com/blog/concept-task-reference)

-   [OASIS Open --- DITA Topic-Based Architecture Benefits](https://docs.oasis-open.org/dita/v1.2/os/spec/archSpec/topicbenefits.html)

-   [APQC --- Process Classification Framework](https://www.apqc.org/process-frameworks)

-   [Sanity.io --- Faceted Taxonomy Setup](https://www.sanity.io/guides/faceted-taxonomy-setup-use)

-   [LobeHub --- Atomic Documentation for AI](https://lobehub.com/de/skills/otrebu-all-agents-context-atomic-doc)

*Amplified Partners Vault: SOUL.md, Operational Protocol v1.0, Radical Attribution Schema v1.0, Pudding Technique SKILL.md --- GitHub ewan-dot/amplified-partners*

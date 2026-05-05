---
title: "Identity"
id: "vault-unification-audit-pandoc"
version: 1
created: "2026-04-25"
type: "document"
topic_type: "audit"
audience: "internal"
layer: "truth"
status: "filed"
signed_by: "Devon, 2026-04-25, devin-992682c244cf444f91e0a516498afbfd"
---

Vault Unification Audit --- Framework Documents
===============================================

**Date**: 2026-03-17 **PUDDING Label**: `M.=.5.l` --- Meta, Stable, System-scale, Long-term **Attribution**: Ewan Bramley (originator, directive) × Perplexity (researcher, auditor)

PROBLEM STATEMENT
-----------------

13 framework documents were created between March 14-17, 2026. They share principles but define them independently. They need to follow vault guidelines, be maximally useful across multiple contexts, and cross-reference rather than duplicate.

PART 1: VAULT FORMAT COMPLIANCE CHECK
-------------------------------------

### Required by Vault Guidelines (from Pudding Technique Skill, Radical Attribution Schema, Operational Protocol)

Every vault document MUST have:

  Requirement                                                                    Source                            Currently Present?
  ------------------------------------------------------------------------------ --------------------------------- -----------------------------------------------------------------------------------------------------
  YAML frontmatter with `type`, `expert`, `dimensions`, `actionable`, `status`   Pudding Technique Part 7          NO --- none of the 13 docs have it
  PUDDING label (`WHAT.HOW.SCALE.TIME`)                                          Pudding Technique Part 4          PARTIAL --- only docs in the vault (SOUL.md, Operational Protocol, Radical Attribution) have labels
  Radical Attribution block                                                      Radical Attribution Schema v1.0   NO --- session-created docs have no attribution blocks
  `pudding_score` (0-20 rubric)                                                  Pudding Technique Part 5          NO
  `created` and `last_validated` dates                                           Pudding Technique Part 7          PARTIAL --- dates exist but not in YAML format
  `lbd_attribution`                                                              Pudding Technique Part 7          NO
  Committed to GitHub                                                            Operational Protocol Law 1        NO --- none of the 13 are committed

### Verdict: None of the 13 framework documents are vault-compliant.

PART 2: THE RELABELLING QUESTION
--------------------------------

### What "Relabelling" Means Here

The documents don't just need PUDDING labels. They need to be restructured so the same content can serve multiple contexts without duplication. The research points to three approaches:

### Approach A: DITA Topic Typing (Industry Standard)

DITA (Darwin Information Typing Architecture) is the established standard for reusable documentation. It sorts every content unit into one of three types:

  Type            Answers                 Example in Your System
  --------------- ----------------------- --------------------------------------------------------------------
  **Concept**     "What is this?"         "What is AMPS?" --- the definition, the philosophy, why it exists
  **Task**        "How do I do this?"     "How to score a process using AMPS" --- the step-by-step procedure
  **Reference**   "What are the facts?"   "AMPS dimension weights table" --- the lookup data

**Why this matters for you:** Right now, each of your 13 documents mixes all three types. The AMPS doc contains the concept (what it is), the task (how to score), AND the reference (the scoring table). This means: - If an agent needs just the scoring table, it has to parse the whole document - If a client needs just the concept, they get buried in implementation detail - If Cove needs just the procedure, it has to strip out the philosophy

**The fix:** Each document becomes 2-3 vault files typed as Concept, Task, or Reference.

### Approach B: Faceted Taxonomy (Multi-Dimensional Classification)

Your PUDDING labels already ARE a faceted taxonomy --- WHAT.HOW.SCALE.TIME are four independent facets. But the documents themselves aren't classified by audience or use-case.

Add two more facets to every document:

  Facet          Values                                                    Purpose
  -------------- --------------------------------------------------------- -----------------
  **AUDIENCE**   `internal` / `client` / `agent` / `coder`                 Who reads this?
  **LAYER**      `principle` / `methodology` / `procedure` / `reference`   What depth?

This maps directly to your four rubric categories: - Content Creation → AUDIENCE: `client`, LAYER: `principle` or `methodology` - Master Document → AUDIENCE: `internal`, LAYER: `methodology` - Process Documentation → AUDIENCE: `internal` or `client`, LAYER: `procedure` - Coding Document → AUDIENCE: `coder` or `agent`, LAYER: `reference`

### Approach C: Atomic Documentation (What Your System Already Almost Does)

Your Gap Analysis framework already uses atom IDs: `AMP-{APQC#}-{SEQ}-{VERSION}`. This is atomic documentation --- each concept is a standalone unit that can be composed into different assemblies.

**The APQC Process Classification Framework** (PCF) is the world standard for classifying business processes, developed in 1992 and used by hundreds of organisations. Your atom ID format already references it. The PCF provides a 5-level hierarchy: 1. Category (e.g., "6.0 Develop and Manage Human Capital") 2. Process Group (e.g., "6.1 Plan and Align Human Capital") 3. Process (e.g., "6.1.1 Develop Human Capital Strategy") 4. Activity (e.g., "6.1.1.1 Assess Current Human Capital Needs") 5. Task (the atomic unit)

### RECOMMENDATION: Combine All Three

You already have the pieces: - **PUDDING labels** = faceted taxonomy (WHAT.HOW.SCALE.TIME) - **Atom IDs** = APQC-based atomic units (AMP-{APQC\#}-{SEQ}-{VERSION}) - **Missing piece** = DITA topic typing (Concept / Task / Reference)

Add to the existing YAML frontmatter:

    topic_type: concept | task | reference
    audience: [internal, client, agent, coder]  # can be multiple
    layer: principle | methodology | procedure | reference
    parent: "AMF-v1.0"  # hierarchy link
    children: ["AMPS-task-scoring", "AMPS-ref-dimensions"]  # hierarchy link

PART 3: HOW EACH DOCUMENT SHOULD SPLIT
--------------------------------------

### Document 1: AMPS (Amplified Process Maturity Score)

Currently: One document mixing concept + task + reference.

Split into:

  New File                   Topic Type   Content                                                                                           Audience
  -------------------------- ------------ ------------------------------------------------------------------------------------------------- ------------------------
  `AMPS-concept.md`          Concept      What AMPS is, why 0-10 scale, the 6 dimensions described, philosophy                              internal, client
  `AMPS-task-scoring.md`     Task         Step-by-step: how to score a process (Decompose→Score→Research→Design→Test→Validate→Reassemble)   internal, agent, coder
  `AMPS-ref-dimensions.md`   Reference    Dimension weights table, scoring thresholds (7.0 ship, 9.0 gold), formula                         agent, coder

**Why:** Agents only need the reference. Clients only need the concept. Coders need the task + reference. Nobody needs all three at once.

### Document 2: Build Quality Framework

Split into:

  New File                 Topic Type   Content                                                                                     Audience
  ------------------------ ------------ ------------------------------------------------------------------------------------------- ------------------------
  `BQF-concept.md`         Concept      What the 6-stage pipeline is, why V-Model + CMMI + DMAIC + PDCA + Quality Gates + Pudding   internal
  `BQF-task-pipeline.md`   Task         Step-by-step: Decompose → Score → Research → Test → Reassemble → Attribute                  internal, agent, coder
  `BQF-ref-PRS.md`         Reference    PRS formula, data size estimates, compute costs, ship thresholds                            agent, coder

**CRITICAL DEPENDENCY:** `BQF-task-pipeline.md` step "Score" MUST reference `AMPS-ref-dimensions.md` --- NOT redefine the scoring. Single source of truth.

### Document 3: RIC (Rapid Intelligence Cycle)

Split into:

  New File              Topic Type   Content                                                                         Audience
  --------------------- ------------ ------------------------------------------------------------------------------- ------------------
  `RIC-concept.md`      Concept      What RIC is, why 4 velocity tiers, the PUDDING→Kaizen transition                internal, client
  `RIC-task-cycle.md`   Task         How to run a RIC cycle at each velocity tier (Nightly/Weekly/Monthly/Glacial)   internal, agent
  `RIC-ref-rubric.md`   Reference    7-dimension evaluation rubric, ship threshold                                   agent, coder

**CRITICAL DEPENDENCY:** `RIC-ref-rubric.md` ship threshold MUST reference `AMPS-ref-dimensions.md` --- same 7.0 threshold, same scoring system.

### Document 4: AMF (Amplified Methodology Framework)

This is the **map document** (DITA terminology). It doesn't contain content --- it references and assembles the other documents.

  New File           Topic Type   Content                                                                                                                                                     Audience
  ------------------ ------------ ----------------------------------------------------------------------------------------------------------------------------------------------------------- ------------------
  `AMF-map.md`       Map          Assembly document: references AMPS, BQF, RIC, APDS, Gap Analysis, Master Process, Operations Register, Visual Polish. Defines hierarchy and reading order   internal
  `AMF-concept.md`   Concept      What the unified methodology is, how the pieces fit together, the philosophy                                                                                internal, client

**This is the key insight:** The AMF should NOT contain the content of all the other frameworks. It should be a map that points to them. When any sub-framework updates, the AMF doesn't need to change.

### Document 5: Master Process Document

Split into:

  New File                 Topic Type   Content                                                                         Audience
  ------------------------ ------------ ------------------------------------------------------------------------------- -----------------
  `MPD-concept.md`         Concept      What the operational design is, the 24-hour cycle philosophy                    internal
  `MPD-task-daily.md`      Task         The daily operational cycle: chaos testing, Kaizen reviews, data audit trails   internal, agent
  `MPD-ref-enforcers.md`   Reference    10 Enforcer roles, escalation rules                                             agent, coder

### Document 6: Gap Analysis & Finite Lenses

Split into:

  New File                 Topic Type   Content                                                              Audience
  ------------------------ ------------ -------------------------------------------------------------------- ------------------
  `GAP-concept.md`         Concept      What the 10 gaps are, why 12 lenses, the three data pools            internal, client
  `GAP-task-analysis.md`   Task         How to run a gap analysis: 5 taxonomy layers, atom ID assignment     internal, agent
  `GAP-ref-lenses.md`      Reference    12 lens definitions, atom ID format (AMP-{APQC\#}-{SEQ}-{VERSION})   agent, coder

### Document 7: APDS (Amplified Pudding Discovery System)

Split into:

  New File                  Topic Type   Content                                                                      Audience
  ------------------------- ------------ ---------------------------------------------------------------------------- ------------------------
  `APDS-concept.md`         Concept      What automated pudding discovery is, the 5-stage pipeline concept            internal, client
  `APDS-task-pipeline.md`   Task         How to run each stage: Harvest → Extract → Label → Match → Score & Surface   internal, agent, coder
  `APDS-ref-config.md`      Reference    SearXNG config, scoring thresholds, dashboard endpoint                       coder

### Document 8: Operations Register

  New File                  Topic Type   Content                                           Audience
  ------------------------- ------------ ------------------------------------------------- -----------------
  `OPS-REG-task.md`         Task         How to log operations, what gets recorded, when   internal, agent
  `OPS-REG-ref-fields.md`   Reference    Field definitions, required vs optional, format   agent, coder

### Document 9: Visual Polish System

  New File                  Topic Type   Content                                       Audience
  ------------------------- ------------ --------------------------------------------- -----------------
  `VPS-concept.md`          Concept      What visual polish means, quality standards   internal
  `VPS-task-checklist.md`   Task         Step-by-step polish checklist                 internal, agent

### Document 10: Vault Research Ingestion Format

  New File                Topic Type   Content                                                          Audience
  ----------------------- ------------ ---------------------------------------------------------------- ------------------------
  `VRIF-task-ingest.md`   Task         How to format and ingest research (2-layer: YAML + raw)          internal, agent, coder
  `VRIF-ref-format.md`    Reference    ID format (RES-YYYY-MM-DD-NNN), YAML schema, field definitions   agent, coder

### Document 11: Content Creation (Voice, Stories, Marketing)

  New File                     Topic Type   Content                                                                                              Audience
  ---------------------------- ------------ ---------------------------------------------------------------------------------------------------- ------------------
  `CONTENT-concept.md`         Concept      The content creation philosophy: Gary Vee pyramid, story structure, platform tones, £1.80 strategy   internal, client
  `CONTENT-task-create.md`     Task         How to create content from vault material: extraction, voice matching, platform adaptation           internal, agent
  `CONTENT-ref-templates.md`   Reference    Case study template, quick-win social post template, "I found something" voice note format           agent

### Document 12: Master Document (OS Bible --- Client-Facing)

  New File                 Topic Type   Content                                          Audience
  ------------------------ ------------ ------------------------------------------------ --------------
  `OS-BIBLE-map.md`        Map          Assembly of all 14 client-facing sections        client
  `OS-BIBLE-ref-json.md`   Reference    The 1,322-line JSON spec (machine-readable OS)   coder, agent

### Document 13: Coding Document

Does not yet exist as a standalone document. The JSON spec serves this role partially, but a proper coding document would be:

  New File                 Topic Type   Content                                                                  Audience
  ------------------------ ------------ ------------------------------------------------------------------------ --------------
  `CODING-concept.md`      Concept      Architecture decisions, tech stack rationale, Cove pipeline philosophy   coder
  `CODING-task-build.md`   Task         How to convert a vault document into code via Cove                       coder, agent
  `CODING-ref-stack.md`    Reference    Tech stack table, API endpoints, database schemas, Drizzle tables        coder

PART 4: THE DEPENDENCY MAP
--------------------------

These are the cross-references that MUST be wired (referenced, not duplicated):

    SOUL.md (immutable — everything points up to this)
    │
    ├── Operational Protocol v1.0 (8 laws)
    │   └── Referenced by: ALL documents (Law 2: Document Everything)
    │
    ├── Radical Attribution Schema v1.0
    │   └── Referenced by: ALL documents (every doc carries attribution)
    │
    ├── AMPS-ref-dimensions.md ← SINGLE DEFINITION OF SCORING
    │   ├── Referenced by: BQF-task-pipeline.md (Score step)
    │   ├── Referenced by: RIC-ref-rubric.md (ship threshold)
    │   ├── Referenced by: MPD-concept.md (process scoring)
    │   └── Referenced by: GAP-task-analysis.md (atom scoring)
    │
    ├── AMF-map.md ← ASSEMBLY DOCUMENT
    │   ├── Includes: AMPS (all 3 files)
    │   ├── Includes: BQF (all 3 files)
    │   ├── Includes: RIC (all 3 files)
    │   ├── Includes: APDS (all 3 files)
    │   ├── Includes: GAP (all 3 files)
    │   ├── Includes: MPD (all 3 files)
    │   ├── Includes: OPS-REG (2 files)
    │   ├── Includes: VPS (2 files)
    │   └── Includes: VRIF (2 files)
    │
    ├── OS-BIBLE-map.md ← CLIENT-FACING ASSEMBLY
    │   ├── Pulls from: AMF concept files (audience: client)
    │   └── Encoded as: OS-BIBLE-ref-json.md
    │
    ├── CONTENT-* ← MARKETING LAYER
    │   └── Sources from: OS-BIBLE + SOUL.md
    │
    └── CODING-* ← BUILD LAYER
        ├── Sources from: OS-BIBLE-ref-json.md
        └── Constrained by: BQF-task-pipeline.md

PART 5: YAML FRONTMATTER TEMPLATE
---------------------------------

Every document gets this (combining existing vault guidelines + new facets):

    ---
    # Identity
    title: "AMPS Scoring Dimensions Reference"
    id: "AMPS-ref-dimensions"
    version: "1.0"
    created: "2026-03-16"
    last_validated: "2026-03-17"

    # Vault Classification
    type: reference  # principle | framework | sop | technique | case_study | hypothesis | recipe
    topic_type: reference  # concept | task | reference | map
    audience: [agent, coder]
    layer: reference  # principle | methodology | procedure | reference

    # PUDDING
    pudding_label: "M.=.0.∞"
    pudding_score: 16
    dimensions:
      - measurement
      - systems
      - threshold

    # Hierarchy
    parent: "AMPS-concept"
    children: []
    referenced_by: ["BQF-task-pipeline", "RIC-ref-rubric", "MPD-concept", "GAP-task-analysis"]
    references: ["SOUL"]

    # Expert & Lineage
    expert: [BRAMLEY, CLAUDE]
    intellectual_lineage:
      - name: "CMMI Institute"
        concept: "Capability Maturity Model"
      - name: "Deming"
        concept: "PDCA Cycle"

    # Status
    actionable: ready_to_use
    status: tested_internal

    # Attribution
    attribution:
      human:
        - name: "Ewan Bramley"
          role: "originator"
          contribution: "Defined 6-dimension scoring model and ship thresholds"
      ai_contributors:
        - name: "Claude"
          provider: "Anthropic"
          role: "formaliser"
          contribution: "Structured into formal framework with weighted dimensions"
        - name: "Perplexity"
          provider: "Perplexity AI"
          role: "researcher"
          contribution: "Validated against CMMI, DMAIC, and APQC standards"
      fact_percentage: 85
      confidence_band: "high"
      lbd_attribution: "Swanson (1986) ABC Model"
    ---

PART 6: TOTAL FILE COUNT
------------------------

Current: 13 monolithic documents (none in vault)

Proposed: 33 vault-compliant files + 2 map documents = **35 files**

  Category                          Files
  --------------------------------- ------------------------------
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
  **TOTAL**                         **35**

All filed under `vault/03-frameworks-and-rubriks/` with clear naming: `{SYSTEM}-{topic_type}.md` e.g., `AMPS-concept.md`, `AMPS-task-scoring.md`, `AMPS-ref-dimensions.md`

PART 7: WHAT THIS ENABLES
-------------------------

### For Agents

An agent running a scoring task loads ONLY `AMPS-ref-dimensions.md` --- 1 file instead of parsing 40 pages of AMF.

### For Clients

A client sees ONLY concept files (audience: client) --- no implementation detail, no code.

### For Cove (Coding Pipeline)

Cove loads reference + task files (audience: coder) --- structured specs it can convert to code.

### For Content Creation

Marketing agents load concept files (audience: client) + `CONTENT-task-create.md` --- voice-matched content from structured sources.

### For PUDDING

Every file has dimensions and PUDDING labels --- the APDS can match across ALL 35 files for cross-domain connections, not just within monolithic documents.

### For FalkorDB/Graphiti Ingestion

Smaller, typed files ingest better. Each creates cleaner entity nodes. Cross-references become explicit graph edges rather than implicit text mentions.

SOURCES
-------

-   DITA Topic Types: Concept, Task, Reference --- [Heretto](https://www.heretto.com/blog/concept-task-reference)
-   DITA Topic-Based Architecture benefits --- [OASIS Open](https://docs.oasis-open.org/dita/v1.2/os/spec/archSpec/topicbenefits.html)
-   APQC Process Classification Framework --- [APQC](https://www.apqc.org/process-frameworks)
-   Faceted Taxonomy principles --- [Sanity.io](https://www.sanity.io/guides/faceted-taxonomy-setup-use)
-   Atomic Documentation for AI --- [LobeHub](https://lobehub.com/de/skills/otrebu-all-agents-context-atomic-doc)
-   Amplified Partners Vault: SOUL.md, Operational Protocol v1.0, Radical Attribution Schema v1.0, Pudding Technique SKILL.md --- GitHub `ewan-dot/amplified-partners`

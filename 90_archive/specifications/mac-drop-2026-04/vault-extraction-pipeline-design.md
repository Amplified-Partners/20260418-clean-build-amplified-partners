Status: [NON-AUTHORITATIVE]
Sanitisation: done — no client data, credentials, or PII found in source specifications
Source: Ewan's Mac drop ("New Folder With Items 2.zip", 521 files, 125MB), ingested 2026-04-29

# Vault Extraction & Output Pipeline: System Design
## Amplified Partners — "Bringing Everything Together"

**Author:** Ewan Bramley (vision, architecture) × Perplexity Computer (research, formalisation)
**Date:** 17 March 2026
**Status:** Design Document — Ready for Review
**PUDDING Label:** `M.?.5.l` — Meta, Emerging, System-scale, Long-term

---

## What This Document Is

This is the design for the system that takes the Amplified Partners vault (4,787 files, 3.3M words) and turns it into eight distinct output streams — from content creation to open-source giveaways to the book to the manifesto to the ISO framework. It runs on local LLM infrastructure on Beast to protect tokens and preserve privacy.

The core principle: **label first, then route**. The PUDDING 2026 taxonomy labels every document, and the labels themselves determine which output stream(s) each document feeds into. No manual sorting. No guesswork. The taxonomy IS the router.

---

## Table of Contents

1. [Pipeline Overview](#1-pipeline-overview)
2. [The Three Agents](#2-the-three-agents)
3. [The Labelling Engine](#3-the-labelling-engine)
4. [The Eight Output Streams](#4-the-eight-output-streams)
5. [PUDDING-to-Stream Routing Logic](#5-pudding-to-stream-routing-logic)
6. [Stream 2 Detail: The Giveaway Department](#6-stream-2-detail-the-giveaway-department)
7. [Stream 7 Detail: The ISO Framework](#7-stream-7-detail-the-iso-framework)
8. [Infrastructure & LLM Configuration](#8-infrastructure--llm-configuration)
9. [Fail-Safe Design](#9-fail-safe-design)
10. [Commercial Value Beyond Amplified](#10-commercial-value-beyond-amplified)
11. [Build Order & Timeline](#11-build-order--timeline)
12. [Sources & Attribution](#12-sources--attribution)

---

## 1. Pipeline Overview

```
┌─────────────────────────────────────────────────────────────────┐
│                        THE VAULT                                 │
│              4,787 files · 3.3M words · 25 directories          │
│              /opt/amplified/vault/ on Beast                      │
└────────────────────────────┬────────────────────────────────────┘
                             │
                    ┌────────▼────────┐
                    │  CONVERGENCE    │
                    │  Brings all     │
                    │  documents      │
                    │  together into  │
                    │  one corpus     │
                    └────────┬────────┘
                             │
                    ┌────────▼────────┐
                    │   HOUND DOG     │
                    │  Discovers any  │
                    │  documents      │
                    │  Convergence    │
                    │  missed         │
                    └────────┬────────┘
                             │
                    ┌────────▼────────┐
                    │    DOCBENCH     │
                    │  Extracts 100%  │
                    │  of the data    │
                    │  (99.53% acc.)  │
                    └────────┬────────┘
                             │
              ┌──────────────▼──────────────┐
              │     PUDDING LABELLER         │
              │  Local LLM on Beast          │
              │  Qwen2.5-72B Q4_K_M          │
              │  Labels EVERY document:      │
              │  · WHAT.HOW.SCALE.TIME       │
              │  · 3-7 semantic dimensions   │
              │  · Content type              │
              │  · Stream routing decision   │
              └──────────────┬──────────────┘
                             │
         ┌───────────────────┼───────────────────┐
         │                   │                   │
         ▼                   ▼                   ▼
   ┌──────────┐      ┌──────────┐      ┌──────────┐
   │ STREAM 1 │      │ STREAM 2 │      │ STREAM 3 │
   │ Content  │      │ Process  │      │ Ewan's   │
   │ Creation │      │ & Logic  │      │ Book     │
   │          │      │ Giveaway │      │          │
   └──────────┘      └──────────┘      └──────────┘

   ┌──────────┐      ┌──────────┐      ┌──────────┐
   │ STREAM 4 │      │ STREAM 5 │      │ STREAM 6 │
   │ Complete │      │ The      │      │ Onboard  │
   │ Document │      │ Manifesto│      │ & Legal  │
   └──────────┘      └──────────┘      └──────────┘

   ┌──────────┐      ┌──────────┐
   │ STREAM 7 │      │ STREAM 8 │
   │ ISO      │      │ Coding   │
   │ Framework│      │ Framework│
   └──────────┘      └──────────┘
```

**Key design principle:** A single document can feed into multiple streams. A monologue transcript about a funny plumbing story that also contains a process insight goes to BOTH Stream 1 (content) AND Stream 2 (giveaway). The labelling engine assigns multi-stream routing.

---

## 2. The Three Agents

### 2.1 Convergence

**Purpose:** Brings all documents together into a single working corpus.
**Input:** The vault (25 directories, all file types)
**Output:** A unified corpus directory with consistent file naming and metadata
**Key capability:** Deduplication, normalisation, format conversion where needed

Convergence is the assembler. It doesn't judge, filter, or label. It brings everything to one table.

### 2.2 Hound Dog

**Purpose:** Discovers any documents Convergence missed — files in unexpected locations, orphaned attachments, documents referenced but not found, files on other machines (Mac Mini, Mac Air) that should be in the vault.
**Input:** The corpus from Convergence + file system scan of all known locations
**Output:** Any discovered files added to the corpus, with provenance logging
**Key capability:** File system crawling, reference checking (if a document mentions another document, does it exist?), cross-machine discovery

Hound Dog is the investigator. It finds what's missing. White-hat, permission-based, logged.

### 2.3 DocBench (Tweaked)

**Purpose:** Extracts 100% of the data from every document in the corpus.
**Proven accuracy:** 99.53% field-level accuracy across 96 documents, 8 document types
**Original output:** JSON per document

**The Tweak:** DocBench currently extracts to one format. For this pipeline, we extend it to extract in multiple output representations:

| Output Format | Purpose | Feeds |
|---|---|---|
| **Raw Text Extract** | Preserves the original voice, stories, natural language | Stream 1 (Content), Stream 3 (Book), Stream 4 (Complete Document) |
| **Structured JSON** | Machine-readable, schema-enforced data fields | Stream 7 (ISO), Stream 8 (Coding), PUDDING Labeller |
| **Process/Logic Extract** | Step-by-step procedures, how-to instructions, problem-solution pairs isolated | Stream 2 (Giveaway), Stream 7 (ISO) |
| **Principles/Values Extract** | Philosophy, beliefs, principles, governance statements | Stream 5 (Manifesto), Stream 6 (Legal/Onboarding) |

This is not four separate runs. It's one extraction pass that produces four representations of the same document. Think of it as four lenses on the same content.

**Implementation:** DocBench's extraction prompt includes a multi-view output instruction:

```json
{
  "document_id": "doc_a1b2c3d4",
  "source_path": "vault/13-monologue-transcripts/2026-03-15-plumbing-stories.md",
  "raw_text": "... (full text, untouched) ...",
  "structured": {
    "title": "...",
    "date": "...",
    "topics": [...],
    "entities": [...],
    "word_count": 1847
  },
  "process_logic": [
    {
      "type": "problem_solution",
      "problem": "...",
      "solution": "...",
      "tools_mentioned": [...]
    }
  ],
  "principles_values": [
    {
      "statement": "...",
      "category": "governance|philosophy|ethics|operational"
    }
  ]
}
```

---

## 3. The Labelling Engine

### 3.1 Architecture

The Labelling Engine runs on Beast using local LLM inference. No tokens leave the server.

```
DocBench Output (JSON per document)
         │
         ▼
┌─────────────────────────────────┐
│      PUDDING LABELLING ENGINE    │
│                                  │
│  Model: Qwen2.5-72B-Instruct    │
│  Quant: Q4_K_M (~42 GB RAM)     │
│  Engine: llama-server            │
│  Parallel slots: -np 8           │
│  Temperature: 0 (deterministic)  │
│  Seed: 42                        │
│  Output: JSON schema-enforced    │
│                                  │
│  Time for full vault: ~8-10 hrs  │
│  (overnight run)                 │
└────────────────┬────────────────┘
                 │
                 ▼
┌─────────────────────────────────┐
│      LABEL OUTPUT (per doc)      │
│                                  │
│  pudding_label: "I.=.5.l"       │
│  semantic_dims: [trust, systems, │
│    communication]                │
│  content_type: "story"           │
│  streams: [1, 3]                 │
│  confidence: 0.91                │
│  review_flag: false              │
└─────────────────────────────────┘
```

### 3.2 Why Qwen2.5-72B

Based on comprehensive research ([NPJ Precision Oncology benchmark](https://pmc.ncbi.nlm.nih.gov/articles/PMC12078457/), [Red Hat quantisation study](https://developers.redhat.com/articles/2024/10/17/we-ran-over-half-million-evaluations-quantized-llms)):

| Factor | Finding |
|---|---|
| **Accuracy vs GPT-4o** | Within 1-2% on classification tasks — near parity |
| **Consistency** | >90% agreement across 100 repeated iterations (higher than GPT-4o and Llama 3.1) |
| **Structured JSON** | Explicitly trained for JSON output; 100% schema validity with grammar constraints |
| **RAM on Beast** | Q4_K_M needs ~42 GB; fits comfortably in 256 GB with room for other services |
| **Throughput** | ~8-10 hours for full vault with -np 8 continuous batching — an overnight run |
| **Cost** | Zero per-token. Local inference only. |
| **Quantisation impact** | Q4_K_M retains ~98-99% of full-precision accuracy for classification specifically |

### 3.3 The Labelling Prompt

```
SYSTEM: You are a taxonomy specialist applying the PUDDING 2026 classification system
to documents in the Amplified Partners knowledge vault. Your task is to assign precise
labels from the predefined taxonomy and route documents to the correct output streams.

Output ONLY valid JSON matching the provided schema. Do not explain your reasoning.

## PUDDING 2026 LABEL FORMAT: WHAT.HOW.SCALE.TIME

### WHAT (Entity Type)
P = Process (action, procedure, workflow)
I = Information (data, knowledge, content)
R = Relation (connection, link, relationship)
E = Entity (thing, product, artifact)
S = State (condition, status, situation)
C = Constraint (rule, limit, boundary)
M = Meta (model, framework, description of descriptions)

### HOW (Dynamic Behaviour)
= = Stable (unchanging, consistent)
+ = Amplifying (growing, compounding)
- = Dampening (shrinking, reducing)
> = Tipping (threshold-based, binary trigger)
~ = Oscillating (cycling, recurring)
! = Disrupting (breaking patterns)
? = Emerging (new, uncertain)

### SCALE (Scope of Effect)
0 = Scale-free | 1 = Singular | 2 = Pair | 3 = Small group
4 = Network | 5 = System | 6 = Universal

### TIME (Duration)
i = Instant | m = Medium (days-weeks) | l = Long (months-years)
v = Variable | p = Permanent | ∞ = Timeless

## OUTPUT STREAMS
1 = Content Creation (stories, anecdotes, rewritable narratives, funny/interesting)
2 = Process & Logic Giveaway (standalone fixes, how-to, problem-solution pairs)
3 = Ewan's Book (strategic ideas, holistic vision, methodology thinking)
4 = Complete Document (reference material, comprehensive coverage)
5 = The Manifesto (philosophy, principles, Layer 0 Laws, the "why")
6 = Onboarding & Legal (contracts, terms, governance, client-facing procedures)
7 = ISO Build Framework (build process patterns, quality gates, data governance)
8 = Coding Framework (coding standards, repo patterns, CI/CD, testing)

A document may route to MULTIPLE streams. Assign all that apply.

## SEMANTIC DIMENSIONS (assign 3-7)
[full dimension list from PUDDING 2026 taxonomy]

## FEW-SHOT EXAMPLES
[3-5 representative labelled documents]

USER: Classify this document:
---
{document_text}
---
Return JSON only.
```

### 3.4 Schema Enforcement

The JSON schema is enforced at the inference engine level (llama.cpp `--json-schema` flag), guaranteeing every output conforms:

```json
{
  "type": "object",
  "required": ["pudding_label", "semantic_dims", "content_type", "streams", "confidence"],
  "properties": {
    "pudding_label": {
      "type": "object",
      "required": ["what", "how", "scale", "time"],
      "properties": {
        "what": {"type": "string", "enum": ["P","I","R","E","S","C","M"]},
        "how": {"type": "string", "enum": ["=","+","-",">","~","!","?"]},
        "scale": {"type": "string", "enum": ["0","1","2","3","4","5","6"]},
        "time": {"type": "string", "enum": ["i","m","l","v","p","∞"]}
      }
    },
    "semantic_dims": {
      "type": "array",
      "minItems": 3,
      "maxItems": 7,
      "items": {"type": "string"}
    },
    "content_type": {
      "type": "string",
      "enum": ["story","process","principle","framework","data","reference","tool","mixed"]
    },
    "streams": {
      "type": "array",
      "minItems": 1,
      "maxItems": 8,
      "items": {"type": "integer", "minimum": 1, "maximum": 8}
    },
    "confidence": {
      "type": "number",
      "minimum": 0,
      "maximum": 1
    }
  }
}
```

### 3.5 Validation Protocol

Before running the full vault:

1. **Manual calibration:** Ewan manually labels 50-100 representative documents
2. **Model comparison:** Run the same 50-100 through the labelling engine
3. **Agreement target:** >85% agreement between Ewan's labels and model labels
4. **Consistency test:** Run 20 documents twice — expect >95% identical output at temperature=0
5. **Taxonomy tuning:** Adjust label definitions based on where disagreements cluster

After the full run:

6. **10% spot check:** Re-run a random 10% sample to verify consistency
7. **Low-confidence review:** Any document with confidence <0.80 gets queued for human review
8. **Stream balance check:** Are the streams roughly balanced? A stream getting <1% of documents may indicate a labelling bias

---

## 4. The Eight Output Streams

### Stream 1: Content Creation

**Purpose:** Stories, anecdotes, funny moments, interesting narratives that can be rewritten for marketing while maintaining truth.

**Source material:** Primarily from `13-monologue-transcripts` (2,214 files) and `14-voice-captures` (954 files) — Ewan thinking out loud, capturing real moments.

**What the labeller looks for:**
- Content type = "story" or "mixed"
- Semantic dimensions include: `communication`, `customer_retention`, `trust`, `mindset`
- Documents with narrative structure, named characters, concrete events

**Output format:** Raw text extracts preserved in full. Stories are gold in their original voice.

**Downstream processing:** Feeds the 14-agent marketing pipeline. Copy Writer and Social Manager take raw stories and adapt them per platform (LinkedIn, Facebook, email) with DISC personality targeting and Brand Guardian approval.

---

### Stream 2: Process & Logic Giveaway (The Micro-Help Department)

**Purpose:** Standalone, packaged solutions — "here's how to fix this specific problem" — given away free. Little chunks that could be done. Little problems that could be fixed by existing standalone AI software. Templated, beautifully designed, behavioural psychology-informed.

**Source material:** Process documents, methodology specs, how-to content, tool evaluations, research findings with actionable outputs.

**What the labeller looks for:**
- Content type = "process" or "tool"
- PUDDING WHAT = P (Process) or E (Entity/tool)
- Semantic dimensions include: `systems`, `cause_effect`, `sequence`, `amplifier`
- Documents with clear problem-solution structure

**Output format:** Process/logic extracts from DocBench — problem-solution pairs, step sequences, tool recommendations.

**Downstream processing:** See Section 6 for full detail on the Giveaway Department.

---

### Stream 3: Ewan's Book

**Purpose:** The strategic-level ideas. How to think about AI for SMBs. The methodology. The philosophy applied to practice. This is Ewan's intellectual contribution as an author.

**Source material:** Business strategy docs, framework designs, monologue transcripts where Ewan is thinking through methodology, cross-domain insights (PUDDING connections), vision documents.

**What the labeller looks for:**
- Content type = "principle" or "framework" or "mixed"
- PUDDING WHAT = M (Meta) or I (Information)
- PUDDING SCALE = 5 (System) or 6 (Universal)
- Semantic dimensions include: `mindset`, `systems`, `measurement`, `trust`
- Documents with Ewan's voice reasoning about "how to do this"

**Output format:** Raw text (preserve voice) + principles/values extracts.

**Downstream processing:** Requires a dedicated Book Editor agent — not part of the marketing pipeline. This agent organises material into chapters, identifies gaps, and produces a structured outline. This is a separate project.

---

### Stream 4: The Complete Comprehensive Document

**Purpose:** The everything-document. Full reference. May or may not be published. Could be narrative or encyclopaedic. Exists for completeness — nothing is lost.

**Source material:** Everything that doesn't fit neatly into other streams, plus key reference material from all streams.

**What the labeller looks for:**
- Any document with PUDDING TIME = l (Long) or p (Permanent) or ∞ (Timeless)
- Content type = "reference" or "data"
- Documents that are foundational — architecture specs, governance documents, product specs

**Output format:** All four DocBench representations (raw text, structured JSON, process/logic, principles/values).

**Downstream processing:** An Assembly Agent compiles and cross-references. This is the "mega-document" from the earlier March 15 session.

---

### Stream 5: The Manifesto

**Purpose:** The philosophy. Why Amplified Partners exists. What it believes. The Layer 0 Laws. The radical honesty, radical transparency, radical attribution principles.

**Source material:** `07-governance-and-legal`, `15-principles-library` (57 files), `03-frameworks-and-rubriks` (69 files), monologue transcripts where Ewan articulates values.

**What the labeller looks for:**
- Content type = "principle"
- PUDDING WHAT = C (Constraint) or M (Meta)
- PUDDING TIME = p (Permanent) or ∞ (Timeless)
- Semantic dimensions include: `trust`, `mindset`, `communication`
- Documents containing statements of belief, ethical positions, governance principles

**Output format:** Principles/values extracts + raw text for voice.

**Downstream processing:** A Manifesto Writer agent distils and weaves. Short, punchy, quotable. Think Dalio's "Principles" but for AI-for-SMBs.

---

### Stream 6: Onboarding & Legal

**Purpose:** Client-facing documents — contracts, terms of service, privacy policies, onboarding procedures, data processing agreements.

**Source material:** `07-governance-and-legal`, onboarding flow specs, client YAML configs, IT forensic interrogation methodology.

**What the labeller looks for:**
- Content type = "process" or "reference"
- PUDDING WHAT = C (Constraint) or P (Process)
- Semantic dimensions include: `trust`, `compliance`, `sequence`
- Documents with procedural or legal language, client-facing tone

**Output format:** Structured JSON + process/logic extracts. These need to be precise, not narrative.

**Downstream processing:** Legal Review Agent + Compliance Agent. Must be checked against UK law, GDPR, and the win-win contract philosophy.

---

### Stream 7: ISO Build Framework (ABPF)

**Purpose:** The ISO 9001/42001-style skeleton for the AI build process — how to assemble the system. Data governance, labelling protocol, content routing, agent configuration, deployment ops.

**Source material:** Architecture specs (`02-technical-architecture`), agent architecture (`05-agent-architecture`), infrastructure docs (`09-infrastructure`), methodology documents (`03-frameworks-and-rubriks`).

**What the labeller looks for:**
- Content type = "framework" or "process"
- PUDDING WHAT = M (Meta) or P (Process)
- PUDDING HOW = = (Stable) — established practices
- Semantic dimensions include: `systems`, `measurement`, `sequence`, `constraint`
- Documents describing how things are built, quality criteria, governance structures

**Output format:** Structured JSON + process/logic extracts.

**Downstream processing:** See Section 7 for full detail. Two documents + one wrapper, aligned with [ISO/IEC 42001](https://www.iso.org/standard/42001) and [ISO/IEC 90003](https://www.iso.org/standard/66240.html).

---

### Stream 8: Coding Framework (CSF)

**Purpose:** Coding standards, repository structure, testing requirements, CI/CD gates, PR review processes. How to write and ship code at Amplified Partners.

**Source material:** Cove orchestrator configs, agent prompt files, rubric files, deployment scripts, testing documentation, Linear issue tracking patterns.

**What the labeller looks for:**
- Content type = "process" or "tool" or "reference"
- PUDDING WHAT = P (Process) or C (Constraint)
- Semantic dimensions include: `systems`, `measurement`, `constraint`
- Documents with code snippets, configuration patterns, naming conventions, testing criteria

**Output format:** Structured JSON — this needs to be precise and machine-readable.

**Downstream processing:** Feeds directly into the CSF skeleton from the ISO research. See Section 7.

---

## 5. PUDDING-to-Stream Routing Logic

The routing is not a simple 1:1 mapping. It's a multi-dimensional decision based on the full PUDDING label + semantic dimensions + content type. Here's the routing matrix:

### Primary Routing Rules

| If content_type is... | AND PUDDING WHAT is... | AND key dimensions include... | Route to Stream(s) |
|---|---|---|---|
| story | Any | communication, trust, customer_* | 1 (Content) |
| story | M or I | mindset, systems | 1 (Content) + 3 (Book) |
| process | P or E | systems, sequence, cause_effect | 2 (Giveaway) |
| process | P | compliance, constraint | 6 (Onboarding/Legal) |
| process | P or M | systems, measurement | 7 (ISO Build) |
| process | P or C | systems, constraint | 8 (Coding) |
| principle | C or M | trust, mindset | 5 (Manifesto) |
| principle | M | mindset, systems (SCALE >= 5) | 3 (Book) + 5 (Manifesto) |
| framework | M | Any | 3 (Book) + 7 (ISO Build) |
| data | I or E | Any | 4 (Complete Document) |
| reference | Any | Any | 4 (Complete Document) |
| tool | E | systems, amplifier | 2 (Giveaway) |
| mixed | Any | Any | Analyse sub-components separately |

### Secondary Routing Rules (Overrides)

| Condition | Override |
|---|---|
| PUDDING TIME = p or ∞ | Always ALSO route to Stream 4 (Complete Document) |
| PUDDING SCALE = 6 (Universal) | Always ALSO route to Stream 3 (Book) |
| confidence < 0.80 | Flag for human review before routing |
| Semantic dims contain "compliance" | Always ALSO route to Stream 6 (Onboarding/Legal) |

### Expected Stream Distribution

Based on vault composition (2,214 monologue transcripts, 954 voice captures, 292 business strategy docs, etc.):

| Stream | Expected % of Documents | Expected Document Count |
|---|---|---|
| 1: Content Creation | ~40-50% | ~1,900-2,400 |
| 2: Process & Logic Giveaway | ~15-20% | ~700-960 |
| 3: Ewan's Book | ~10-15% | ~480-720 |
| 4: Complete Document | ~25-35% | ~1,200-1,675 |
| 5: Manifesto | ~5-8% | ~240-380 |
| 6: Onboarding & Legal | ~3-5% | ~145-240 |
| 7: ISO Build Framework | ~8-12% | ~380-575 |
| 8: Coding Framework | ~5-8% | ~240-380 |

**Note:** Percentages sum to more than 100% because documents route to multiple streams.

---

## 6. Stream 2 Detail: The Giveaway Department

### 6.1 Philosophy

> "We're giving away our software. Why the hell not? It's nice and it'll make people do things easier than we've done them."

This is not marketing disguised as generosity. It IS generosity. The documents are genuinely useful, properly made, and designed to help people solve real problems. The only follow-up is one contact to ask "did this help?" and collect feedback.

### 6.2 Department Structure

The Giveaway Department sits within (or adjacent to) the marketing pipeline. It uses the same Brand Guardian for tone enforcement but has its own template system and production workflow.

```
Stream 2 Input (process/logic extracts)
         │
         ▼
┌─────────────────────────────────┐
│  PROBLEM IDENTIFIER              │
│  Extracts discrete problems      │
│  from the process/logic data     │
│  One problem = one giveaway      │
└────────────────┬────────────────┘
                 │
                 ▼
┌─────────────────────────────────┐
│  SOLUTION PACKAGER               │
│  Pairs each problem with:        │
│  · The fix (step-by-step)        │
│  · Third-party tools that do it  │
│  · Links to those tools          │
│  · What to expect                │
└────────────────┬────────────────┘
                 │
                 ▼
┌─────────────────────────────────┐
│  TEMPLATE ENGINE                 │
│  Applies behavioural psychology  │
│  layout (see 6.3):              │
│  · Known-effective structures    │
│  · Cognitive load minimisation   │
│  · Progressive disclosure        │
│  · Clear visual hierarchy        │
└────────────────┬────────────────┘
                 │
                 ▼
┌─────────────────────────────────┐
│  BRAND GUARDIAN                  │
│  Tone check: helpful, honest,    │
│  no hard sell, no jargon,        │
│  passes compliance_rubric.yaml   │
└────────────────┬────────────────┘
                 │
                 ▼
┌─────────────────────────────────┐
│  PUBLISHING                      │
│  · PDF for download              │
│  · Web page for browsing         │
│  · Solutions database entry      │
│  · Categorised and tagged        │
└────────────────┬────────────────┘
                 │
                 ▼
┌─────────────────────────────────┐
│  FOLLOW-UP ENGINE (one contact)  │
│  · Email or WhatsApp             │
│  · "Did this help?"              │
│  · Request for brief feedback    │
│  · Feedback → FalkorDB           │
│  · No funnel. No upsell.        │
└─────────────────────────────────┘
```

### 6.3 Behavioural Psychology Template Design

Each giveaway document follows a template grounded in established behavioural psychology:

**Layout Principles:**

| Principle | Source | Application |
|---|---|---|
| **Cognitive load theory** (Sweller, 1988) | Reduce extraneous processing | Maximum 3-5 steps per fix. One concept per page. No jargon. |
| **Progressive disclosure** (Norman, 1988) | Show only what's needed now | Summary first, detail expandable. Don't overwhelm with options. |
| **Hick's Law** | Decision time increases with choices | One recommended tool per problem. Alternatives in a separate "other options" section, not the main flow. |
| **Inverted pyramid** | Most important first | Problem → solution → how → detail. Never bury the answer. |
| **Fogg Behaviour Model (B=MAP)** | Behaviour requires Motivation + Ability + Prompt | Make it easy (ability), show why it matters (motivation), give a clear next step (prompt). |
| **Dual coding theory** (Paivio, 1971) | Visual + verbal together | Every step has both text and a simple visual/icon/diagram. |
| **Serial position effect** | People remember first and last items | Put the most important step first. Put the call-to-action (try the tool) last. |

**Template Structure:**

```
┌─────────────────────────────────────────────────────┐
│  AMPLIFIED PARTNERS · MICRO-HELP                     │
│                                                       │
│  [ICON] THE PROBLEM                                   │
│  One sentence. Crystal clear. "Your invoices are      │
│  going out late because you're creating them          │
│  manually after each job."                            │
│                                                       │
│  WHY IT MATTERS                                       │
│  One sentence with a number. "Late invoices cost      │
│  trades £3,200/year on average in delayed payment."   │
│                                                       │
│  THE FIX (3 steps max)                                │
│  1. [Visual] Step one — plain English                 │
│  2. [Visual] Step two — plain English                 │
│  3. [Visual] Step three — plain English               │
│                                                       │
│  RECOMMENDED TOOL                                     │
│  [Tool name] — [one line description]                 │
│  [Link to tool]                                       │
│  Free / £X per month                                  │
│                                                       │
│  ─────────────────────────────────────                │
│  OTHER OPTIONS (if you prefer)                        │
│  · [Alternative 1] — [link]                           │
│  · [Alternative 2] — [link]                           │
│                                                       │
│  ─────────────────────────────────────                │
│  This guide was created by Amplified Partners.        │
│  We help small businesses reduce friction with AI.    │
│  amplifiedpartners.ai                                 │
└─────────────────────────────────────────────────────┘
```

### 6.4 Follow-Up Workflow

One contact. That's it. Designed using Paddy Lund's Critical Non-Essentials — the small touch that shows you care without asking for anything.

**Timing:** 7 days after download/access
**Channel:** Same channel they received the document (email or WhatsApp)
**Message template:**

> Hi [name],
>
> You downloaded our guide on [problem] last week. Two quick questions if you have 30 seconds:
>
> 1. Did it help? (Yes / Partly / No)
> 2. Anything we could make clearer?
>
> That's it. No sales pitch. We just want to make these guides better.
>
> — Amplified Partners

**What happens with the feedback:**
- Stored in FalkorDB under the giveaway document's node
- Aggregated as quality scores per guide (% "Yes", % "Partly", % "No")
- Guides scoring <60% "Yes" get flagged for review and improvement
- The feedback loop feeds the Kaizen cycle — 0.5% better every day

**What does NOT happen:**
- No follow-up email sequence
- No "book a call" CTA
- No retargeting
- No adding to a marketing list
- If they reply asking "what else do you do?" — then and only then do you answer that question

---

## 7. Stream 7 Detail: The ISO Framework

### 7.1 Architecture: Two Documents, One Wrapper

Based on comprehensive research into [ISO/IEC 42001:2023](https://www.iso.org/standard/42001), [ISO/IEC 90003:2014](https://www.iso.org/standard/66240.html), [NIST AI RMF](https://www.nist.gov/itl/ai-risk-management-framework), and the open-source [GSTT-CSC QMS Template](https://github.com/GSTT-CSC/QMS-Template):

```
┌───────────────────────────────────────────────────────────┐
│           AMPLIFIED PARTNERS QUALITY POLICY               │
│    (1-page wrapper — ISO 9001/42001 governance layer)     │
└───────────────────────────────────────────────────────────┘
              │                           │
┌─────────────▼──────────────┐  ┌────────▼───────────────────┐
│  DOCUMENT 1:               │  │  DOCUMENT 2:               │
│  AI BUILD PROCESS          │  │  CODING STANDARDS          │
│  FRAMEWORK (ABPF)          │  │  FRAMEWORK (CSF)           │
│                            │  │                            │
│  ISO 42001 aligned         │  │  ISO/IEC 90003 aligned     │
│  NIST AI RMF informed      │  │  ISO/IEC 25010 referenced  │
│                            │  │  MLOps Level 2 quality     │
│  6 Parts + Appendices      │  │  gates included            │
│  (see full skeleton in     │  │                            │
│  research-iso9001-ai-      │  │  7 Parts + Appendices      │
│  frameworks.md)            │  │  (see full skeleton)       │
└────────────────────────────┘  └────────────────────────────┘
```

### 7.2 Why Two, Not One

| Reason | Detail |
|---|---|
| **Different audiences** | ABPF is for the AI/data team + client trust conversations; CSF is for engineers |
| **Different update cadence** | Build process evolves faster than coding standards |
| **Cleaner ISO mapping** | ABPF → ISO 42001; CSF → ISO/IEC 90003. Clean audit trail |
| **Product potential** | Two modular documents are more flexible for licensing to other AI consultancies |
| **Agentic AI standards gap** | [NIST launched the AI Agent Standards Initiative in February 2026](https://www.nist.gov/news-events/news/2026/02/announcing-ai-agent-standards-initiative-interoperable-and-secure) — no published standards yet for agentic AI. This is an opportunity to be early. |

### 7.3 Product Potential

The ISO framework is itself a product. The market is underserved:

- Only [15 of 30 major enterprise AI agent developers](https://arxiv.org/html/2602.17753v1) have published safety/trust frameworks
- For small AI consultancies, there is essentially **no off-the-shelf quality framework** that covers both AI build process and code quality
- Product concept: **"Amplified Quality System (AQS)"** — open-source skeleton + paid customisation
- Target buyers: Small AI consultancies (5-20 people), in-house AI teams at professional services firms, AI-for-SMB builders

**But first:** Use it internally for 6-12 months before selling. Real case study evidence beats theoretical templates.

---

## 8. Infrastructure & LLM Configuration

### 8.1 Beast Server Setup for Labelling

```bash
# 1. Install/build llama.cpp from source for Zen 4 optimisations
git clone https://github.com/ggml-org/llama.cpp && cd llama.cpp
cmake -B build -DGGML_NATIVE=ON -DGGML_AVX512=ON
cmake --build build --config Release -j$(nproc)

# 2. Download Qwen2.5-72B Q4_K_M
huggingface-cli download Qwen/Qwen2.5-72B-Instruct-GGUF \
  qwen2.5-72b-instruct-q4_k_m.gguf --local-dir /models/

# 3. Run inference server
numactl --interleave=all ./build/bin/llama-server \
  -m /models/qwen2.5-72b-instruct-q4_k_m.gguf \
  -t 24 -np 8 --cont-batching -fa \
  --json-schema /configs/pudding2026-schema.json \
  -c 65536 --host 0.0.0.0 --port 8080 --no-mmap
```

### 8.2 Resource Budget

| Component | RAM | CPU Threads | Status |
|---|---|---|---|
| Qwen2.5-72B Q4_K_M | ~42 GB | 24 | Labelling engine |
| Existing Docker containers (36+) | ~30-40 GB | Variable | Already running |
| FalkorDB | ~8 GB | 4 | Already running |
| Ollama (existing) | ~10-20 GB | Variable | Can be paused during labelling |
| OS + buffers | ~20 GB | — | Reserved |
| **Headroom** | **~130-150 GB** | **~40+ threads** | **Plenty of margin** |

### 8.3 Estimated Processing Time

| Phase | Time | Notes |
|---|---|---|
| Convergence (file assembly) | 1-2 hours | File copying, dedup, normalisation |
| Hound Dog (discovery scan) | 2-4 hours | Depends on cross-machine scope |
| DocBench (extraction) | 4-8 hours | Depends on file complexity mix |
| PUDDING Labelling | 8-10 hours | Overnight run, Qwen2.5-72B with -np 8 |
| Validation (10% spot check) | 1-2 hours | Automated consistency check |
| **Total** | **~16-26 hours** | **Can be pipelined across 2 nights** |

---

## 9. Fail-Safe Design

Every stage has a fail-safe. Nothing is lost. Everything is logged.

| Stage | Fail-Safe | Recovery |
|---|---|---|
| Convergence | Originals NEVER moved or modified. Corpus is a copy. | Re-run Convergence from originals |
| Hound Dog | Discovery results are logged before any action | Re-run scan; previous results are checkpointed |
| DocBench | Extraction is idempotent. Re-running the same file produces the same output. | `--resume` flag skips already-extracted files |
| PUDDING Labelling | All raw model outputs logged (prompt, response, timing) alongside parsed labels | Re-run from checkpoint; raw outputs available for re-parsing |
| Stream Routing | Routing is deterministic from labels. Same label → same stream(s), always. | Re-route from stored labels without re-running the model |
| Output Generation | Each stream's output is versioned (Git-tracked) | Roll back to any previous version |

**The golden rule:** At every stage, the input data is preserved. The pipeline adds layers (extracts, labels, routes) but never modifies or deletes the source.

---

## 10. Commercial Value Beyond Amplified

Three products emerge from this pipeline:

### 10.1 TAXONOMY ENGINE

The PUDDING labelling pipeline, generalised as a "bring your own taxonomy" product for clients. Local-first document intelligence.

- **Market:** [IDP market growing at 24.7% CAGR toward $21B by 2034](https://www.gminsights.com/industry-analysis/intelligent-document-processing-market)
- **Differentiator:** Data never leaves the client's jurisdiction. Zero API costs. GDPR-native.
- **Pricing:** Per-document (£0.05-0.20) or per-vault subscription

### 10.2 Amplified Quality System (AQS)

The ISO framework skeleton, battle-tested on Amplified Partners, then offered as a product for other AI consultancies.

- **Market gap:** No off-the-shelf framework covers both AI build process + code quality for small teams
- **Pricing:** Open-source skeleton (GitHub) + paid customisation (£2,500-5,000) + licensed template kit (£500-1,500/year)

### 10.3 Micro-Help Library

The giveaway documents themselves, growing into a comprehensive solutions database that drives inbound attention and brand credibility.

- **Scale strategy:** [50+ pillar pieces per year → 2,000-4,000 targeted derivative pieces → 20,000+ SMBs reached in year one](research in vault/01-business-strategy)
- **Revenue:** Indirect — drives awareness and trust, which feeds the paid tiers

---

## 11. Build Order & Timeline

### Phase 1: Foundation (Week 1-2)

- [ ] Build the PUDDING 2026 JSON schema for llama.cpp enforcement
- [ ] Download and configure Qwen2.5-72B Q4_K_M on Beast
- [ ] Create 50-100 manually labelled calibration documents
- [ ] Run calibration: model vs human, iterate prompt until >85% agreement
- [ ] Tweak DocBench to produce 4-format output

### Phase 2: Full Run (Week 2-3)

- [ ] Run Convergence → Hound Dog → DocBench (pipelined)
- [ ] Run PUDDING Labelling Engine on full vault (overnight)
- [ ] Run validation (10% spot check + consistency test)
- [ ] Review stream distribution — adjust routing rules if needed

### Phase 3: Stream Processing (Week 3-6)

- [ ] Stream 1: Feed labelled content to marketing pipeline
- [ ] Stream 2: Build Giveaway Department templates and first 10 guides
- [ ] Stream 5: Draft the Manifesto (short, first)
- [ ] Stream 7 + 8: Start filling in the ISO framework skeletons

### Phase 4: Book & Complete Document (Week 6-12)

- [ ] Stream 3: Organise Book material into chapter structure
- [ ] Stream 4: Compile the Complete Document
- [ ] Stream 6: Draft onboarding legal documents

### Ongoing

- [ ] Every vault update triggers re-run of the labelling engine on new/modified documents
- [ ] Giveaway Department produces new guides on a regular cadence
- [ ] Feedback from follow-ups feeds quality improvements

---

## 12. Sources & Attribution

### Attribution

| Contributor | Role | Contribution |
|---|---|---|
| **Ewan Bramley** | Originator, Vision | Complete pipeline architecture, output stream design, giveaway philosophy, book concept, manifesto vision |
| **Perplexity Computer** | Researcher, Formaliser | ISO 9001/42001 research, local LLM benchmarking, pipeline formalisation, routing logic design, template design |
| **Don R. Swanson** | Theoretical Foundation | PUDDING taxonomy derives from Literature-Based Discovery (ABC model, 1986) |

### Key Research Sources

| Topic | Source | URL |
|---|---|---|
| ISO/IEC 42001 (AI Management System) | ISO | https://www.iso.org/standard/42001 |
| ISO/IEC 90003 (ISO 9001 for Software) | ISO | https://www.iso.org/standard/66240.html |
| NIST AI Risk Management Framework | NIST | https://www.nist.gov/itl/ai-risk-management-framework |
| NIST AI Agent Standards Initiative | NIST | https://www.nist.gov/news-events/news/2026/02/announcing-ai-agent-standards-initiative-interoperable-and-secure |
| GSTT-CSC QMS Template (Open Source) | GitHub | https://github.com/GSTT-CSC/QMS-Template |
| Qwen2.5-72B Classification Benchmark | NPJ Precision Oncology | https://pmc.ncbi.nlm.nih.gov/articles/PMC12078457/ |
| 500K+ Quantisation Evaluations | Red Hat | https://developers.redhat.com/articles/2024/10/17/we-ran-over-half-million-evaluations-quantized-llms |
| IDP Market Forecast | Global Market Insights | https://www.gminsights.com/industry-analysis/intelligent-document-processing-market |
| 2025 AI Agent Index | arXiv | https://arxiv.org/html/2602.17753v1 |

### Full Research Reports

The following research reports were produced as part of this design work and are available in the workspace:

1. `research-iso9001-ai-frameworks.md` — 865 lines covering ISO 42001, 90003, 25010, NIST AI RMF, CMMI, MLOps, open-source QMS templates, agentic AI standards, complete framework skeletons, and product potential
2. `research-local-llm-labelling.md` — 600 lines covering model selection, quantisation benchmarks, batch processing strategies, infrastructure configuration, commercial applicability, and GDPR/data sovereignty analysis

---

*Fact %: 85 | Confidence: High | PUDDING: M.?.5.l*
*LBD: Swanson (1986) ABC Model*

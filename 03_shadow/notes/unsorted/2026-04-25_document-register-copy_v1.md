---
title: "Document Register — Dated & Described"
id: "document-register-copy"
version: 1
created: "2026-04-25"
type: "document"
topic_type: "unsorted"
audience: "internal"
layer: "shadow"
status: "filed"
signed_by: "Devon, 2026-04-25, devin-992682c244cf444f91e0a516498afbfd"
---

# Document Register — Dated & Described

All documents from the thread consolidation, renamed chronologically with honest descriptions of what's actually in them (not what the thread started as).

---

## Naming Convention

```
YYYY-MM-DD-DEPT-DESCRIPTION-vN.N.ext
```

### Rules

| Element | Format | Example | Notes |
|---|---|---|---|
| **Date** | `YYYY-MM-DD` | `2026-03-19` | Date the document was STARTED (first session). Reflects chronological position, not last edit. |
| **Department** | 3-letter code | `EXT`, `RES`, `TAX` | See department codes below. Groups documents by function. |
| **Description** | UPPERCASE-HYPHENATED | `EXTRACTION-PIPELINE-SPEC` | Max 4 words. What the document IS, not what the thread was called. No filler words (the, a, of). |
| **Version** | `vN.N` | `v1.0` | Major.Minor. Major = structural change. Minor = refinement. Omit for v1.0 (first version assumed). |
| **Extension** | lowercase | `.md`, `.docx`, `.json` | Reflects actual format. |

### Department Codes

| Code | Department | Covers |
|---|---|---|
| `EXT` | Extraction | Data ingestion, cleaning, pipelines, DocBench, forensic extraction |
| `RES` | Research | Discovery, APDS, RIC, search strategy, PromptForge |
| `TAX` | Taxonomy | PUDDING labels, validation, Curator gates, codebooks |
| `ARC` | Architecture | Master framework, data architecture, dev blueprint, Bible |
| `QAL` | Quality | Build quality, red-team testing, chaos testing, Kaizen |
| `MKT` | Marketing | Content creation, value agents, brand |
| `OPS` | Operations | Master process, operations register, scheduling |
| `CLI` | Client | Client-facing specs, onboarding, forensics |
| `GOV` | Governance | AI Board, Enforcer roles, constitutional docs |
| `INF` | Infrastructure | Beast, Docker, servers, migration |

### Examples

```
2026-03-19-EXT-EXTRACTION-PIPELINE-SPEC.docx
2026-03-17-RES-PUDDING-DISCOVERY-SYSTEM.md
2026-03-14-TAX-PUDDING-MATHEMATICAL-PROOF.md
2026-03-16-ARC-AMPLIFIED-METHODOLOGY-FRAMEWORK.md
2026-01-24-RES-INTENT-TERMINOLOGY-PROTOCOL.md
2026-03-22-QAL-EXTRACTION-REDTEAM-TESTS.md
```

### Versioning Rules

1. If a document is substantially rewritten, increment major version and keep the original date: `2026-03-16-ARC-AMPLIFIED-METHODOLOGY-FRAMEWORK-v2.0.md`
2. If a document is refined/corrected, increment minor version: `-v1.1.md`
3. First version has no version suffix (v1.0 is assumed)
4. Never change the date — it always reflects when the document was started
5. If two documents merge, the date of the EARLIER document wins

---

## CLUSTER A: Data Extraction & Processing

| Current Name / Location | Proposed Name | What's Actually In It |
|---|---|---|
| Extraction Department Spec (A1) | `2026-03-19-EXT-EXTRACTION-PIPELINE-SPEC.docx` | 5-stage pipeline architecture with 8 output streams, dual output channels (deterministic + creative), ~650 lines of Python code. The definitive engineering spec for how data enters the system. |
| Data Extraction Department thread (A2) | `2026-03-19-EXT-VOICE-AUDIO-EXTRACTION-DEPT.md` | Started as "design a data extraction department" but ended up focused on voice/audio processing — Monologue service, accent handling, phoneme research, open-source commitment. The R&D department charter for audio-specific extraction. |
| Vault Extraction Pipeline (A3) | `2026-03-17-EXT-VAULT-EXTRACTION-PIPELINE.md` | Convergence → Hound Dog → DocBench → PUDDING Labelling → 8 Output Streams. How existing vault data gets reprocessed. Overlaps heavily with A1 — the vault-specific variant of the same pipeline. |
| Perplexity Extraction Research (A4) | `2026-03-17-EXT-PERPLEXITY-DATA-EXTRACTION.md` | 19-page report on extracting data from Perplexity AI threads. Fork of simwai/perplexity-ai-export v1.1.0, three-layer dedup process, 5 new recommended skills. Standalone — specific to getting data OUT of Perplexity. |
| Forensic Data Extraction thread (A5) | `2026-03-14-CLI-FORENSIC-DATA-EXTRACTION.md` | Deterministic extraction from client public data + IT infrastructure. MCPipe/Unix pipe pattern, MCP servers, the "deterministic before probabilistic" principle. Client-facing application of the extraction pipeline. |
| DocBench (A6) | `2026-03-14-EXT-DOCBENCH-ENGINE.md` | Core extraction engine that powers client onboarding. 4-format output (raw text, JSON, process/logic, principles/values). The engine underneath the other extraction specs. |
| Red-Team Eval Lab — Extraction (A7) | `2026-03-22-QAL-EXTRACTION-REDTEAM-TESTS.md` | 58 adversarial tests across 14 categories, extraction hardening at 91%. Testing spec for the extraction pipeline. |

---

## CLUSTER B: Research & Discovery

| Current Name / Location | Proposed Name | What's Actually In It |
|---|---|---|
| APDS Spec (B1) | `2026-03-17-RES-PUDDING-DISCOVERY-SYSTEM.md` | 27-page spec for automated Swanson-style discovery. 5-stage pipeline (Harvest→Extract→Label→Match→Score), SearXNG on Beast, 4-tier source taxonomy, Docker Compose spec, cost model ($0.39/day), 12-week roadmap. The outbound research system. |
| Rapid Intelligence Cycle (B2) | `2026-03-16-RES-RAPID-INTELLIGENCE-CYCLE.md` | 27-page operational framework. 4 velocity tiers (Nightly/Weekly/Monthly/Glacial), 7-dimension evaluation rubric, ship threshold ≥7.0, PUDDING→Kaizen transition after 2 weeks stability. The cadence and rhythm of how research runs. |
| PromptForge deep research (B3) | `2026-03-18-RES-PROMPTFORGE-SPEECH-TO-PROMPT.md` | Deep research into speech-to-perfect-prompt engineering. DSPy/MIPROv2 core, model-specific adapters (Claude/Grok/Perplexity), database-backed Kaizen, few-shot library. The full programmatic prompt optimisation system. |
| Transcription-Prompt-Optimiser skill (B4) | `2026-03-18-RES-TRANSCRIPTION-OPTIMISER-SKILL.md` | Perplexity skill version of PromptForge. EXTRACT→STRUCTURE→OPTIMISE→EXECUTE. Lightweight, deployed, running now. The skill that cleans your speech before Perplexity acts on it. |
| Intent-to-Terminology Protocol (B5) | `2026-01-24-RES-INTENT-TERMINOLOGY-PROTOCOL.md` | The original insight session. Speech→strip noise→find foundational intent→translate to expert vocabulary→search state-of-art. Also contains the AlphaProof parallel and the NLP Meta-Model connection. Where the whole prompt pipeline concept was born. |
| Search Engine Diversity Research (B6) | `2026-03-22-RES-SEARCH-ENGINE-DIVERSITY.md` | Academic research on search diversity. Spink & Jansen 2006 (84.9% uniqueness), Chen et al. 2025 GEO paper, Gusenbauer & Gauster 2025. Supporting evidence for the divergent prompt strategy. |

---

## CLUSTER C: Labelling & Classification

| Current Name / Location | Proposed Name | What's Actually In It |
|---|---|---|
| PUDDING Technique skill (C1) | `2026-03-14-TAX-PUDDING-TECHNIQUE-SKILL.md` | The master skill. Swanson ABC model, WHAT.HOW.SCALE.TIME labels, 4-criteria rubric, 7 biological decision logics, recipe scoring formula, worked examples, document label format. The foundational methodology. |
| PUDDING Operational Frameworks (C2) | `2026-03-17-TAX-PUDDING-OPERATIONAL-FRAMEWORKS.md` | Lens Description Framework, Anchored Rubric (max 68, min viable 13, high value 18), Kill Switch (50-pair gate). The governance layer on top of the PUDDING technique. |
| Validation Methodology (C3) | `2026-03-16-QAL-PUDDING-VALIDATION-METHODOLOGY.md` | Krippendorff's Content Analysis applied to PUDDING. Inter-rater reliability measurement, codebook structure, mandatory enforcement at every stage. The statistical proof that labelling is consistent. |
| Curator Gate Spec (C4) | `2026-03-17-TAX-CURATOR-GATE-SPEC.md` | 5 deterministic gates (Structure, Codebook, Hierarchy, Content, Reconciliation). Compressed '_c' code system with CURATOR-CODEBOOK.md lookup. The enforcement mechanism for taxonomy quality. |
| Code Taxonomy & Kaizen (C5) | `2026-03-17-QAL-CODE-TAXONOMY-KAIZEN.md` | 7-step Kaizen cycle applied specifically to code. Error research, code reuse taxonomy, continuous testing. The coding-specific version of the improvement cycle. |
| Compressed PUDDING Labels (C6) | `2026-03-17-TAX-COMPRESSED-PUDDING-LABELS.md` | Transition from verbose dot-notation to letter-pairs for RAG density. A format decision document, not a methodology doc. |
| PUDDING Mathematical Validation (C7) | `2026-03-14-TAX-PUDDING-MATHEMATICAL-PROOF.md` | PMI computation validates label matching. P(identical label by chance) = 1/2058. 3000:1 compression ratio. 5/6 existing mixes validated at p<0.01. The mathematical proof that PUDDING works. |

---

## CLUSTER D: Architecture & Methodology

| Current Name / Location | Proposed Name | What's Actually In It |
|---|---|---|
| AMF v1 (D1) | `2026-03-16-ARC-AMPLIFIED-METHODOLOGY-FRAMEWORK.md` | 40-page unified operating manual. Synthesises AMPS, Build Quality Framework, RIC, PUDDING, Gap Analysis, Master Process, Operations Register, Visual Polish. Includes Chaos 4-pillar protocol, 705-case golden dataset, canary deployment. The "Bible" attempt. |
| Build Quality Framework (D2) | `2026-03-16-QAL-BUILD-QUALITY-FRAMEWORK.md` | 6-stage pipeline (Decompose→Score→Research→Test→Reassemble→Attribute). PRS formula, ship threshold ≥7.0, gold standard ≥9.0. Compute cost estimates per atom. How anything gets built. |
| Unified Data Architecture (D3) | `2026-03-20-ARC-UNIFIED-DATA-ARCHITECTURE.md` | Constitutional document. 5 data stores (Document, Knowledge Graph, Vector Index, Process DB, Backup). Label-once-propagate-everywhere principle. Curator-exclusive taxonomy assignment. JSON for active agent tasks only. |
| AI-Native Development Blueprint (D4) | `2026-03-21-ARC-AI-NATIVE-DEV-BLUEPRINT.md` | 4-layer stack (Linear→Cove→Beads→Quality). Comet Strategic Command cockpit. Spec-driven development with AGENTS.md and GitHub Spec Kit. M1-M9 module organisation. How code gets planned and built. |
| Amplified Bible Consolidation (D5) | `2026-03-21-ARC-AMPLIFIED-BIBLE-CONSOLIDATED.md` | 19-page consolidated document from 7 source docs. Department mapping, companion document index. The latest attempt to bring everything into one place. |

---

## DOCUMENTS NOT IN CLUSTERS (Referenced but standalone)

| Proposed Name | What's Actually In It |
|---|---|
| `2026-03-18-RES-PROMPTFORGE-DEEP-RESEARCH.md` | The full deep research output on speech-to-prompt systems. Contains the PromptForge architecture, DSPy research, academic citations. |
| `2026-03-14-MKT-VALUE-AGENT-DEEP-RESEARCH.md` | 787-line spec for AI agents that provide value in forums/communities without mentioning Amplified Partners. Already on Beast. |
| `2026-03-15-INF-RAILWAY-TO-BEAST-MIGRATION.md` | Migration runbook from Railway to Beast. Completed. Historical reference. |
| `2026-03-14-ARC-LANGGRAPH-OPENAGENTS-ANALYSIS.md` | LangGraph × OpenAgents symbiosis analysis. Already in vault. |
| `2026-03-16-CLI-CUSTOMER-VOICE-INTELLIGENCE.md` | 14 sections (P1-P10 + rules), master reference + content brief + coding spec for each. |

---

## NOTES

1. All dates are "when the document was substantially created" not "when the thread started" — because threads wander.
2. Where a thread started as one thing and ended as another, the name reflects what it ENDED as.
3. The January 2026 threads (B5 and the Swanson research sessions from Jan 21-31) are dated to their actual session dates.
4. This register itself: `2026-03-22-OPS-DOCUMENT-REGISTER.md`

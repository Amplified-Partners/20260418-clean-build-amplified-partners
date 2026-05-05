---
title: "Hounddog Integration Plan Copy"
id: "hounddog-integration-plan-copy"
version: 1
created: "2026-04-25"
type: "document"
topic_type: "spec"
audience: "internal"
layer: "build"
status: "filed"
signed_by: "Devon, 2026-04-25, devin-992682c244cf444f91e0a516498afbfd"
---

**AMPLIFIED PARTNERS**

━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

**HoundDog Extraction**

**Integration Plan**

Embedding 99.53% accuracy extraction methodology across the

entire Amplified Partners technology stack

March 2026

Prepared for Ewan Bramley

**CONFIDENTIAL**

**1. Executive Summary**

Amplified Partners has a proven extraction methodology. DocBench achieves 99.53% accuracy on structured data extraction. The HoundDog specification defines a Document Discovery Agent that finds every document hiding across a client\'s entire digital and physical footprint --- across 15+ sources, entirely on local infrastructure, with consent-first GDPR compliance.

The problem: this extraction excellence is isolated. DocBench extracts brilliantly, but the principles that make it work --- three-tier classification, three-tier deduplication, chain-of-custody audit trails, consent-first architecture --- are not applied consistently across the rest of the Amplified Partners stack. The vault ingestion pipeline handles only markdown. The Gatekeeper uses single-pass LLM classification. The marketing engine ingests source material without dedup. External data collection has no standardised extraction methodology.

This document is the integration plan. It maps every touchpoint in the Amplified Partners ecosystem where HoundDog\'s extraction principles must be embedded, identifies the specific gaps at each point, defines concrete changes required, and sequences the work into four implementation phases. The goal: every piece of data that enters the Amplified Partners knowledge graph --- whether from client onboarding, vault ingestion, marketing research, or external collection --- passes through the same rigorous classification, deduplication, and audit pipeline that makes DocBench\'s 99.53% accuracy possible.

**2. The HoundDog Extraction Principles**

The following ten principles are extracted from the HoundDog Document Discovery Agent specification (March 2026). These are not aspirational --- they are the architectural decisions that underpin the 99.53% DocBench accuracy. Every integration point in this document maps back to one or more of these principles.

**1. Three-Tier Classification:** Filename heuristic resolves 60% of documents instantly. Remaining files undergo MIME type detection via python-magic (byte-signature analysis, not file extension). Only genuinely ambiguous files are escalated to LLM classification using llama3.1:8b. This tiered approach minimises LLM calls while maintaining high accuracy.

**2. Three-Tier Deduplication:** SHA-256 hash catches exact duplicates. ssdeep fuzzy hashing identifies near-duplicates (minor edits, re-saves). Embedding cosine similarity via nomic-embed-text catches semantic duplicates (same content, different wording). Auto-dedup at 0.95 threshold, human review at 0.85-0.95.

**3. Consent-First Architecture:** Pre-access consent gate for every data source. Granular per-source control --- a client can consent to email discovery but deny filesystem access. Immediate revocation capability. Full GDPR Article 6(1)(a) compliance with append-only tamper-evident audit trail.

**4. Chain of Custody:** Every data access is logged with millisecond-precision timestamps, source identifier, agent ID, action performed, consent reference, and result. This creates an unbroken audit trail from discovery to extraction to graph insertion.

**5. Minimal Data Retention:** Store metadata and embeddings, never raw content. Original files remain in their source locations. The knowledge graph holds references, not copies. This reduces storage requirements, minimises breach surface, and respects data minimisation principles under GDPR.

**6. Eight-Stage Pipeline:** Consent → Source Enumeration → Parallel Discovery → Classification → Deduplication → Graph Construction → Report Generation → Incremental Watch. Each stage is a discrete, testable unit with defined inputs and outputs.

**7. Checkpointed Stateful Execution:** LangGraph nodes with persistent checkpoints. If any stage fails, execution resumes from the last successful checkpoint with exponential backoff retry. No work is lost, no data is reprocessed unnecessarily.

**8. Local-First Processing:** All LLM inference runs via Ollama on the Hetzner Beast server (135.181.161.131). Models: llama3.1:70b for complex reasoning, llama3.1:8b for classification, qwen3-coder:30b for code tasks, nomic-embed-text for embeddings. No external API ever processes document content.

**9. OCR via PaddleOCR 3.0:** PP-OCRv5 + PP-StructureV3 for text recognition and layout analysis. Superior to Tesseract for table extraction, multi-column layouts, and mixed text/image documents. Handles scanned invoices, receipts, contracts, and handwritten notes.

**10. Entity Extraction to Graph:** People, organisations, dates, monetary amounts, and document relationships are extracted and fed to FalkorDB via Graphiti. This transforms a flat document inventory into a navigable knowledge graph with temporal edges and entity resolution.

**3. Integration Matrix**

The following matrix provides a high-level view of every Amplified Partners touchpoint, the HoundDog principles that apply, and the priority and effort required for integration.

  ----------------------------- ---------------------------------------------------------------------------------------- ------------------------------------------------------------------------------- -------------------------------------------------------------------- -------------- ------------
  **Touchpoint**                **Current State**                                                                        **Key Gaps**                                                                    **Principles to Apply**                                              **Priority**   **Effort**
  A. Vault Ingestion Pipeline   Reads .md/.json, chunks by headings, feeds Graphiti                                      No classification, no dedup, no MIME detection, no OCR, no audit trail          Three-tier classification, Three-tier dedup, Chain of custody, OCR   P1             3-4 weeks
  B. Client Onboarding          Manual IT forensic interrogation covering tech stack, data sources, pain points          No automated discovery, no auto-classification, no auto-dedup of client docs    Full 8-stage pipeline, Consent-first, Local-first processing         P2             4-5 weeks
  C. Gatekeeper Agent           Conversation-to-action quality gate: capture, classify, write to Obsidian, sync GitHub   Single-pass LLM classification, no dedup against vault, no audit trail          Three-tier classification, Semantic dedup, Chain of custody          P1             2-3 weeks
  D. DocBench Extraction        99.53% structured extraction engine --- downstream consumer                              HoundDog doesn\'t exist as code yet to feed it                                  8-stage pipeline output, Checkpointed execution, Handoff contract    P2             2 weeks
  E. Graphiti / FalkorDB        Entity extraction via LLM, temporal edges in FalkorDB                                    No entity-level dedup, no provenance tracking, no audit trail on graph writes   Entity dedup, Chain of custody, Minimal data retention               P2             3 weeks
  F. Marketing Engine           14 agents producing 15-25 pieces/day, Brand Guardian enforces voice                      Source material ingested without classification or dedup                        Three-tier classification, Three-tier dedup                          P3             2 weeks
  G. Cove Code Factory          Temporal-based build pipeline turning Linear issues into deployed code                   No document integrity verification, no chain-of-custody for spec reading        SHA-256 integrity verification, Chain of custody                     P4             1 week
  H. Pudding Discovery (APDS)   5-stage: Harvest → Extract → Label → Match → Score & Surface                             Harvest collects research without classification/dedup                          Three-tier classification, Three-tier dedup                          P3             2 weeks
  I. External Data Collection   Various agents fetch web content, PDFs, competitor data                                  No standardised extraction methodology                                          Full pipeline: MIME → classify → dedup → audit → graph               P3             2-3 weeks
  ----------------------------- ---------------------------------------------------------------------------------------- ------------------------------------------------------------------------------- -------------------------------------------------------------------- -------------- ------------

**4. Detailed Integration Plans**

**A. Vault Ingestion Pipeline (ingest\_vault.py)**

**Current State**

The vault ingestion pipeline (ingest\_vault.py, 744 lines) is the primary mechanism for loading content into the Amplified Partners knowledge graph. It reads markdown files from the Obsidian vault, chunks them by \#\# headings or paragraph boundaries, and feeds each chunk to Graphiti for entity extraction and graph construction. It also handles .json files. The \--resume flag enables checkpoint-based re-runs, skipping previously processed files.

**Gaps Identified**

-   No three-tier classification --- files are assumed to be markdown or JSON based on extension alone.

-   No MIME type detection --- a .md file containing binary data would be processed as text.

-   No deduplication beyond \--resume checkpoint skipping --- duplicate content in different files enters the graph twice.

-   No fuzzy or semantic deduplication --- near-duplicate or semantically equivalent documents are not detected.

-   No chain-of-custody audit trail --- no record of when files were ingested, by which process, or what decisions were made.

-   No consent layer --- any file in the vault path is ingested without verification of source permissions.

-   Limited format support --- cannot process PDFs, DOCX, images, or scanned documents.

-   No OCR capability --- scanned documents and images with text are completely ignored.

**Specific Changes Required**

-   **Add python-magic MIME detection** as the first step after file enumeration. Before any content processing, verify the file\'s actual type via byte-signature analysis. Replace the current extension-based filtering.

-   **Implement three-tier classification:** (1) Run filename heuristic patterns against each file --- invoice patterns, contract naming conventions, receipt formats. This resolves \~60% of files instantly. (2) For remaining files, use python-magic MIME type to determine document category. (3) Only for genuinely ambiguous files, call llama3.1:8b via Ollama for LLM classification.

-   **Add three-tier deduplication before graph insertion:** (1) Compute SHA-256 hash of each chunk --- skip exact duplicates. (2) Compute ssdeep fuzzy hash --- flag near-duplicates for review or auto-dedup based on similarity threshold. (3) Generate embeddings via nomic-embed-text and compute cosine similarity against existing graph content --- auto-dedup at 0.95, queue for human review at 0.85-0.95.

-   **Integrate Apache Tika** for format expansion. Add PDF, DOCX, XLSX, PPTX, RTF, and HTML parsing via Tika before the chunking stage. Tika extracts text from 1,000+ file formats and runs locally.

-   **Integrate PaddleOCR 3.0** (PP-OCRv5 + PP-StructureV3) for scanned documents and images. When Tika identifies an image-based PDF or an image file with potential text, route through PaddleOCR for text extraction and layout analysis.

-   **Add append-only audit logging:** Every file processed gets a JSON log entry with timestamp (millisecond precision), file path, SHA-256 hash, MIME type detected, classification decision (which tier resolved it), dedup decision, agent ID, and result (ingested/skipped/flagged).

-   **Add consent verification:** Before processing any file, verify it belongs to a consented source. Maintain a consent registry mapping source paths to consent records.

**HoundDog Principles Applied**

Three-tier classification, Three-tier deduplication, Chain of custody, OCR (PaddleOCR 3.0), Local-first processing, Consent-first architecture, Minimal data retention.

**Priority and Effort**

**Priority: P1** (critical path --- the vault is the primary knowledge source). **Effort: 3-4 weeks.** Week 1: MIME detection + three-tier classification. Week 2: Three-tier dedup. Week 3: Tika + PaddleOCR integration. Week 4: Audit trail + consent layer + testing.

**B. Client Onboarding (IT Forensic Interrogation)**

**Current State**

Client onboarding currently relies on a manual discovery session --- the IT Forensic Interrogation. This structured interview covers the client\'s technology stack audit, data source inventory, pain points, voice capture, and business goals. The consultant manually identifies where documents live across the client\'s systems and records this information for downstream processing.

**Gaps Identified**

-   No automated document discovery --- relies entirely on what the client remembers to mention.

-   No automated classification of discovered documents.

-   No automated deduplication of client document stores.

-   Clients consistently underestimate the number of sources where their documents live (the HoundDog spec identifies 15+ common sources).

-   No systematic coverage --- browser history, messaging apps, deleted files, and accounting attachments are routinely missed.

**Specific Changes Required**

-   **Deploy HoundDog as the automated IT Forensic Interrogation.** The manual session becomes the consent collection phase --- the consultant walks the client through each of the 15+ source types, collecting explicit per-source consent. HoundDog then executes the 8-stage pipeline autonomously.

-   **Implement consent collection UI:** Build a web-based consent form that maps to HoundDog\'s granular per-source consent model. Each source (email, cloud storage, filesystem, messaging, accounting, browser history, scanners, forensic recovery) gets an individual toggle with clear explanation of what will be accessed.

-   **Run HoundDog discovery agents post-consent:** Deploy the LocalFilesystemAgent, EmailAgent, CloudStorageAgent, MessagingAgent, AccountingAgent, BrowserHistoryAgent, ScannerAgent, and ForensicRecoveryAgent (as consented) against the client\'s systems.

-   **Generate discovery report:** HoundDog produces a complete document inventory --- classified, deduplicated, with entity relationships mapped --- as the output of the onboarding process. This replaces the manual spreadsheet.

-   **Feed discovery output to DocBench:** The HoundDog discovery manifest becomes the DocBench input queue. Every discovered document is automatically queued for structured extraction.

**HoundDog Principles Applied**

Full 8-stage pipeline, Consent-first architecture, Three-tier classification, Three-tier deduplication, Local-first processing, Entity extraction to graph, Checkpointed stateful execution.

**Priority and Effort**

**Priority: P2** (dependent on HoundDog core being built first). **Effort: 4-5 weeks.** Week 1: Consent collection UI. Week 2-3: Agent deployment workflow and client-side setup. Week 4: Discovery report generation. Week 5: DocBench handoff integration + testing.

**C. Gatekeeper Agent**

**Current State**

The Gatekeeper Agent (12 Python files in the gatekeeper-agent repository) is the Conversation-to-Action quality gate for all content entering the Amplified Partners knowledge system. It captures content from conversations, classifies it by type and intent, applies quality checks, writes approved content to the Obsidian vault, syncs to GitHub, and creates Linear items for action tracking.

**Gaps Identified**

-   Single-pass LLM classification --- every piece of content goes through a full LLM call for classification, even when filename or MIME type would suffice. This is slow and expensive.

-   No deduplication against existing vault content --- if the same insight is captured from two different conversations, both copies enter the vault and graph.

-   No chain-of-custody audit trail --- no record of classification decisions, quality gate pass/fail, or write operations.

-   No MIME detection for attached files --- attachments are handled by extension only.

**Specific Changes Required**

-   **Replace single-pass classification with three-tier:** (1) Filename/content-type heuristic for obvious types (meeting notes, action items, client feedback --- pattern-matched from conversation context). (2) MIME type detection via python-magic for any attached files. (3) LLM classification via llama3.1:8b only for ambiguous content.

-   **Add semantic dedup check before vault write:** Before writing any content to the Obsidian vault, generate an embedding via nomic-embed-text and query the existing vault embeddings. If cosine similarity exceeds 0.95, skip (auto-dedup). If 0.85-0.95, flag for human review. This prevents the same insight from entering the graph multiple times.

-   **Add SHA-256 exact dedup:** Compute hash of content before writing. Check against a hash registry of all previously written content.

-   **Implement chain-of-custody logging:** Every Gatekeeper decision gets a JSON audit entry: timestamp (ms precision), source conversation ID, content hash, classification tier used, classification result, dedup check result, quality gate result, write destination, agent ID.

-   **Add content integrity verification:** After writing to Obsidian and syncing to GitHub, verify the written content matches the original hash. Log verification result.

**HoundDog Principles Applied**

Three-tier classification, Three-tier deduplication (SHA-256 + semantic), Chain of custody, Local-first processing.

**Priority and Effort**

**Priority: P1** (the Gatekeeper is the primary content ingestion path --- every improvement here multiplies across the system). **Effort: 2-3 weeks.** Week 1: Three-tier classification refactor. Week 2: Semantic dedup + SHA-256 dedup. Week 3: Audit trail + integrity verification.

**D. DocBench Extraction Engine**

**Current State**

DocBench is the crown jewel of the Amplified Partners extraction stack --- 99.53% accuracy on structured data extraction. It processes documents through a sophisticated pipeline of layout analysis, field detection, and value extraction. DocBench is the downstream consumer of whatever documents are presented to it.

**Gaps Identified**

-   DocBench itself is already excellent --- the extraction methodology is proven.

-   The gap is upstream: HoundDog does not yet exist as running code to feed DocBench a reliable stream of discovered, classified, deduplicated documents.

-   No formal handoff contract exists between discovery (HoundDog) and extraction (DocBench).

**Specific Changes Required**

-   **Define the handoff contract:** HoundDog writes one JSON manifest per discovered document at doc\_{sha256\_first8}.json. Each manifest contains: file\_path (or source URI), sha256\_full, mime\_type, classification\_tier (1/2/3), classification\_result, dedup\_status (unique/near\_duplicate/semantic\_duplicate), discovery\_timestamp, consent\_reference, source\_agent\_id.

-   **Build the DocBench input queue:** Create a shared directory (or Redis queue) where HoundDog deposits discovery manifests. DocBench polls this queue, picks up new manifests, fetches the original document from its source location, and begins extraction.

-   **Add extraction result feedback:** After DocBench extracts a document, it writes an extraction\_result.json back to the manifest directory. HoundDog\'s report generation stage picks this up and includes extraction status in the final discovery report.

-   **Implement priority ordering:** HoundDog\'s classification output includes a document\_type field. DocBench should process high-value types first (contracts, invoices, financial statements) before lower-priority types (general correspondence, meeting notes).

**HoundDog Principles Applied**

8-stage pipeline (handoff between Stage 6 and DocBench), Checkpointed stateful execution, Chain of custody (provenance travels with each manifest), Minimal data retention (manifests reference documents, don\'t contain them).

**Priority and Effort**

**Priority: P2** (dependent on HoundDog core being operational). **Effort: 2 weeks.** Week 1: Handoff contract definition + queue implementation. Week 2: Extraction feedback loop + priority ordering + testing.

**E. Graphiti / FalkorDB Ingestion**

**Current State**

Graphiti extracts entities (people, organisations, dates, amounts) from document content via LLM and creates temporal edges in FalkorDB. This powers the knowledge graph that makes Amplified Partners\' document intelligence possible. Graphiti handles entity extraction, relationship mapping, and temporal versioning of graph edges.

**Gaps Identified**

-   No entity-level deduplication before graph insertion --- the same person mentioned in different documents creates multiple graph nodes instead of resolving to one.

-   No provenance tracking per graph edge --- once an entity is in the graph, there is no record of which document it was extracted from.

-   No audit trail for graph write operations --- no log of what was extracted versus what was actually ingested.

-   No verification that extracted entities match the source document content.

**Specific Changes Required**

-   **Add entity-level deduplication:** Before inserting a new entity node, query FalkorDB for existing entities with matching or similar names. Use embedding cosine similarity (nomic-embed-text) for fuzzy entity matching --- \'Ewan Bramley\', \'E. Bramley\', and \'Ewan (Amplified Partners)\' should resolve to one node. Maintain a canonical name registry.

-   **Add provenance tracking:** Every graph edge must carry a provenance property: source\_document\_sha256, extraction\_timestamp, extraction\_agent\_id, confidence\_score. This creates traceability from any graph relationship back to the document that generated it.

-   **Add chain-of-custody logging for graph writes:** Every graph mutation (node create, edge create, node merge, edge update) gets an append-only audit log entry with: timestamp (ms precision), operation\_type, entity\_id, source\_document, agent\_id, consent\_reference, before\_state, after\_state.

-   **Implement extraction verification:** After Graphiti extracts entities, verify that extracted values actually appear in the source content. Log verification results. Flag extractions that cannot be verified against source.

-   **Apply minimal data retention:** Graph nodes store entity metadata and embeddings, not the raw text passages they were extracted from. Store a reference (document SHA-256 + byte offset) back to the original source.

**HoundDog Principles Applied**

Entity extraction to graph (with dedup), Chain of custody, Minimal data retention, Local-first processing.

**Priority and Effort**

**Priority: P2** (critical for graph quality, but current pipeline is functional). **Effort: 3 weeks.** Week 1: Entity-level dedup + canonical name registry. Week 2: Provenance tracking + edge metadata. Week 3: Audit logging + extraction verification.

**F. Marketing Engine**

**Current State**

The marketing engine comprises 14 specialised agents that produce 15-25 pieces of content daily. The Brand Guardian agent enforces voice consistency across all output. These agents consume source material --- client documents, competitor research, market analysis, case studies --- to generate blog posts, social media content, email campaigns, and thought leadership pieces.

**Gaps Identified**

-   When the marketing engine ingests source material (client docs, competitor sites, research papers), no classification or dedup is applied.

-   The same competitor insight may be ingested multiple times from different sources, leading to redundant content production.

-   No MIME detection on source materials --- the engine assumes format based on context.

-   No audit trail of which source materials informed which content pieces.

**Specific Changes Required**

-   **Add three-tier classification to source material ingestion:** Before any source material enters the marketing pipeline, classify it using HoundDog\'s three-tier approach. Tag each source with its document type, relevance score, and freshness.

-   **Add three-tier dedup to source material:** Check all incoming source material against the existing marketing knowledge base. SHA-256 for exact duplicates (same article fetched twice), ssdeep for near-duplicates (slightly reformatted content), embedding similarity for semantic duplicates (same information from different sources).

-   **Add source provenance tracking:** Every piece of generated content should reference which source documents informed it. This creates an audit trail for content claims and supports fact-checking.

-   **Integrate MIME detection:** When marketing agents fetch external content (PDFs, web pages, documents), verify the actual content type via python-magic before processing.

**HoundDog Principles Applied**

Three-tier classification, Three-tier deduplication, Chain of custody (source provenance), Local-first processing.

**Priority and Effort**

**Priority: P3** (marketing pipeline is functional, improvements are quality-of-life). **Effort: 2 weeks.** Week 1: Classification + dedup integration into source ingestion. Week 2: Provenance tracking + MIME detection.

**G. Cove Code Factory**

**Current State**

The Cove Code Factory is a Temporal-based build pipeline that transforms Linear issues into tested, deployed code via Claude coding agents. When a Linear issue is created, Cove picks it up, reads the associated specification documents, generates code, runs tests, and deploys. The pipeline handles the full software development lifecycle from ticket to production.

**Gaps Identified**

-   When Cove agents read specification documents or reference materials, there is no verification of document integrity.

-   No chain-of-custody for which version of a specification was used to generate code.

-   If a specification is modified between the time a Linear issue is created and the time Cove processes it, the agent may work from stale or incorrect requirements.

**Specific Changes Required**

-   **Add SHA-256 integrity verification:** When a Linear issue references a specification document, Cove records the document\'s SHA-256 hash at issue creation time. Before processing, Cove re-hashes the document and compares. If the hash differs, Cove flags the discrepancy and requests human review before proceeding.

-   **Add chain-of-custody logging:** Every specification read by a Cove agent gets an audit entry: timestamp, document path, SHA-256 hash, agent\_id, Linear issue reference, read\_purpose. This creates a verifiable record of exactly which documents informed each code generation.

-   **Add document version tracking:** Maintain a version registry of all specification documents. When Cove reads a spec, it logs the version. When a spec is updated, all Cove tasks referencing the previous version are flagged for review.

**HoundDog Principles Applied**

Chain of custody, SHA-256 integrity verification (from three-tier dedup), Minimal data retention (store hashes, not copies).

**Priority and Effort**

**Priority: P4** (lowest risk --- Cove is already producing quality code, this is a safety net). **Effort: 1 week.** SHA-256 verification + audit logging can be added as a pre-processing step in the Temporal workflow.

**H. Pudding Discovery System (APDS)**

**Current State**

The Amplified Partners Discovery System (APDS), codenamed Pudding, operates a 5-stage pipeline: Harvest → Extract → Label → Match → Score & Surface. It discovers cross-domain connections --- finding unexpected links between client industries, technologies, and market trends that would be invisible to single-domain analysis.

**Gaps Identified**

-   The Harvest stage collects research from multiple sources but does not apply HoundDog\'s classification principles --- content is categorised by source rather than by actual content type.

-   The Extract stage processes raw content without deduplication --- the same research finding collected from multiple sources enters the pipeline multiple times.

-   No audit trail of what was harvested, from where, and what dedup decisions were made.

**Specific Changes Required**

-   **Wire three-tier classification into APDS Harvest:** Every piece of harvested content passes through filename heuristic → MIME detection → LLM classification before entering the Extract stage. This replaces the current source-based categorisation with content-aware classification.

-   **Wire three-tier dedup into APDS Extract:** Before extraction, deduplicate harvested content. SHA-256 for exact duplicates, ssdeep for near-duplicates (same article from different aggregators), embedding cosine similarity for semantic duplicates (same finding reported differently).

-   **Add provenance tracking through the pipeline:** Each piece of content carries its harvest source, classification result, and dedup status through all five stages. The Score & Surface stage can then weight results by source diversity (an insight found independently in three sources is more reliable than one found once).

**HoundDog Principles Applied**

Three-tier classification, Three-tier deduplication, Chain of custody, Local-first processing.

**Priority and Effort**

**Priority: P3** (Pudding is functional but would benefit significantly from clean input data). **Effort: 2 weeks.** Week 1: Classification integration into Harvest. Week 2: Dedup integration into Extract + provenance tracking.

**I. External Data Collection**

**Current State**

Various Amplified Partners agents fetch external data for competitive analysis, market research, trend monitoring, and client-specific research. These include web content fetching, PDF downloads, competitor site monitoring, social media analysis, and industry report collection. Each agent handles its own data collection with its own conventions.

**Gaps Identified**

-   No standardised extraction methodology --- each agent handles external data differently.

-   No MIME type verification for fetched content --- agents assume format based on URL or context.

-   No deduplication of externally collected data against existing knowledge.

-   No audit trail for what was collected, when, from where, and how it was processed.

-   No consent tracking for external data sources (relevant for GDPR when handling client-related external data).

**Specific Changes Required**

-   **Create a unified external data ingestion gateway:** All external data --- regardless of collecting agent --- must pass through a single ingestion gateway that applies HoundDog\'s principles. The gateway runs: MIME detection → three-tier classification → three-tier dedup against existing knowledge graph → audit trail logging → graph insertion (if unique and relevant).

-   **Implement MIME detection for all fetched content:** When an agent downloads a file or fetches a web page, python-magic verifies the actual content type. A URL ending in .pdf that returns HTML (common with paywalls) gets flagged rather than processed incorrectly.

-   **Add semantic dedup against the knowledge graph:** Before any external data enters the graph, generate embeddings and check cosine similarity against existing content. This prevents the same market research insight from being stored multiple times because it was collected by different agents at different times.

-   **Add chain-of-custody audit logging:** Every external data collection event gets a log entry: timestamp, source URL, collecting agent ID, MIME type detected, classification result, dedup result, insertion decision.

-   **Standardise the collection-to-graph pipeline:** Define a common data structure for externally collected content that carries metadata (source, collection time, classification, dedup status) through the entire pipeline from collection to graph insertion.

**HoundDog Principles Applied**

Three-tier classification, Three-tier deduplication, Chain of custody, MIME detection, Local-first processing, Minimal data retention, Consent-first architecture (for client-related external data).

**Priority and Effort**

**Priority: P3** (high impact for data quality, moderate implementation effort). **Effort: 2-3 weeks.** Week 1: Unified ingestion gateway + MIME detection. Week 2: Classification + dedup integration. Week 3: Audit logging + testing.

**5. Implementation Sequence**

Implementation is sequenced in four phases, ordered by dependency chain and impact. Phase 1 hardens the existing data pipeline. Phase 2 builds the HoundDog-to-DocBench connection. Phase 3 extends HoundDog principles to supporting systems. Phase 4 completes full-stack integration.

**Phase 1: Foundation (Weeks 1-6)**

**Focus: Vault Ingestion Pipeline + Gatekeeper Agent**

These are the two primary content ingestion paths. Every improvement here immediately improves the quality of data entering the knowledge graph. The vault pipeline gets three-tier classification, three-tier dedup, Tika format expansion, PaddleOCR integration, and audit logging. The Gatekeeper gets three-tier classification, semantic dedup against existing vault content, and chain-of-custody logging.

-   Week 1-2: Vault ingestion --- MIME detection + three-tier classification

-   Week 3: Vault ingestion --- three-tier dedup implementation

-   Week 4: Vault ingestion --- Tika + PaddleOCR integration

-   Week 5: Gatekeeper --- three-tier classification + semantic dedup

-   Week 6: Both --- audit trail implementation + integration testing

**Deliverable:** Vault and Gatekeeper pipelines applying HoundDog classification, dedup, and audit principles to all ingested content.

**Phase 2: Discovery Pipeline (Weeks 7-14)**

**Focus: Client Onboarding + DocBench Handoff + Graphiti Entity Dedup**

With the foundation solid, Phase 2 builds the HoundDog discovery pipeline for client onboarding and connects it to DocBench. This phase also adds entity-level dedup to Graphiti to prevent duplicate nodes in the knowledge graph.

-   Week 7: Consent collection UI for client onboarding

-   Week 8-9: HoundDog agent deployment workflow (client-side setup, agent configuration)

-   Week 10: Discovery report generation

-   Week 11: DocBench handoff contract + queue implementation

-   Week 12: DocBench priority ordering + extraction feedback loop

-   Week 13: Graphiti entity-level dedup + canonical name registry

-   Week 14: Graphiti provenance tracking + integration testing

**Deliverable:** End-to-end pipeline from client consent through document discovery, classification, dedup, extraction, and graph insertion with full provenance tracking.

**Phase 3: Ecosystem Extension (Weeks 15-20)**

**Focus: Marketing Engine + APDS Pudding + External Data Collection**

Phase 3 extends HoundDog principles to the systems that consume and produce content around the core pipeline. The marketing engine gets classification and dedup for source material. APDS gets classification in Harvest and dedup in Extract. External data collection gets a unified ingestion gateway.

-   Week 15-16: Marketing engine --- classification + dedup for source material ingestion

-   Week 17: APDS Harvest --- three-tier classification integration

-   Week 18: APDS Extract --- three-tier dedup + provenance tracking

-   Week 19-20: External data collection --- unified ingestion gateway + MIME detection + dedup

**Deliverable:** All content-consuming systems applying consistent classification and dedup. Clean, non-duplicate data flowing through marketing, discovery, and research pipelines.

**Phase 4: Full Integration (Weeks 21-24)**

**Focus: Cove Code Factory + System-Wide Audit Trail + Monitoring**

Phase 4 completes the integration by adding document integrity verification to Cove, implementing system-wide audit trail consolidation, and building monitoring dashboards to track classification accuracy, dedup coverage, and pipeline health.

-   Week 21: Cove --- SHA-256 integrity verification + chain-of-custody logging

-   Week 22: System-wide audit trail consolidation --- unified log format, central log store

-   Week 23: Monitoring dashboard --- classification accuracy, dedup rates, pipeline throughput

-   Week 24: End-to-end integration testing + documentation + team training

**Deliverable:** Complete HoundDog principle integration across all Amplified Partners systems. Unified audit trail. Monitoring and alerting. Full documentation.

**6. Architecture Flow**

The following describes the end-to-end data flow once all integrations are complete. This is the target architecture --- every piece of data entering the Amplified Partners ecosystem follows this path.

**Stage 1: Source Discovery (HoundDog Agents)**

Nine specialised discovery agents (LocalFilesystem, Email, CloudStorage, Messaging, Web, Accounting, BrowserHistory, Scanner, ForensicRecovery) concurrently discover documents across all consented sources. Each agent runs as a LangGraph sub-graph with its own state and checkpointing on the Hetzner Beast server.

**Stage 2: Three-Tier Classification**

Every discovered document passes through the classification pipeline. Tier 1 (filename heuristic) resolves \~60% instantly. Tier 2 (python-magic MIME detection) resolves most of the remainder. Tier 3 (llama3.1:8b via Ollama) handles genuinely ambiguous files. Classification result is attached to the document manifest.

**Stage 3: Three-Tier Deduplication**

Classified documents are deduplicated. SHA-256 exact hash catches identical files. ssdeep fuzzy hash catches near-duplicates (minor edits, re-saves, format conversions). Embedding cosine similarity (nomic-embed-text) catches semantic duplicates. Auto-dedup at 0.95 similarity, human review queue at 0.85-0.95.

**Stage 4: DocBench Extraction**

Unique documents are queued for DocBench structured extraction via the handoff contract (doc\_{sha256\_first8}.json manifests). DocBench applies its 99.53% accuracy extraction methodology to pull structured data: fields, values, tables, entities. Extraction results are written back to the manifest.

**Stage 5: Entity Extraction and Graph Construction**

Extracted data feeds Graphiti, which identifies entities (people, organisations, dates, amounts) and creates temporal edges in FalkorDB. Entity-level dedup resolves duplicate entities across documents. Provenance tracking links every graph edge back to its source document. Chain-of-custody logging records every graph mutation.

**Stage 6: Actionable Intelligence**

The knowledge graph serves downstream consumers: the marketing engine draws on classified source material, APDS Pudding discovers cross-domain connections from clean data, Cove reads integrity-verified specifications, and the Gatekeeper ensures new content doesn\'t duplicate existing knowledge. Every consumer benefits from upstream classification, dedup, and audit trail.

**Data Flow Summary**

Sources → HoundDog Discovery → Classification (3-tier) → Deduplication (3-tier) → DocBench Extraction → Graphiti Entity Extraction → FalkorDB Knowledge Graph → Downstream Consumers (Marketing, APDS, Cove, Gatekeeper)

Audit Trail: Every stage writes to the append-only audit log. Consent Reference: Every data access carries its consent reference. Checkpoint: Every LangGraph node persists state for failure recovery.

**7. Success Metrics**

The following metrics define what \"done\" looks like for the HoundDog integration. These are measurable, verifiable targets --- not aspirational goals.

**Classification Accuracy**

-   Target: 95%+ classification accuracy across all ingestion paths (vault, Gatekeeper, marketing, APDS, external).

-   Measurement: Weekly sample of 100 classified documents, manually verified. Track accuracy per tier (heuristic, MIME, LLM).

-   Tier 1 (filename heuristic) should resolve 55-65% of documents without escalation.

-   Tier 3 (LLM) should be invoked on fewer than 15% of documents.

**Deduplication Coverage**

-   Target: Zero exact duplicates in the knowledge graph (SHA-256 dedup catches 100% of identical content).

-   Target: 90%+ near-duplicate detection rate (ssdeep fuzzy hash catches re-saves, minor edits).

-   Target: 85%+ semantic duplicate detection rate (embedding similarity catches rephrased content).

-   Measurement: Monthly audit --- sample 500 graph entities, check for duplicates. Track dedup rate per tier.

**Audit Trail Completeness**

-   Target: 100% audit trail coverage --- every data access, classification decision, dedup decision, and graph mutation is logged.

-   Target: Every audit entry includes timestamp (ms precision), agent ID, action, consent reference, and result.

-   Measurement: Automated verification --- run a daily script that checks every graph node has a corresponding audit trail entry tracing back to its source.

**Consent Compliance**

-   Target: Zero data accesses without valid consent reference.

-   Target: Consent revocation takes effect within 60 seconds across all systems.

-   Measurement: Weekly audit of consent log versus data access log --- every access must map to a valid, non-revoked consent record.

**Pipeline Performance**

-   Target: Vault ingestion processes 1,000 documents/hour including classification, dedup, and audit logging.

-   Target: Gatekeeper classification adds no more than 500ms latency to the content capture flow.

-   Target: HoundDog full discovery run completes within 4 hours for a typical SME client (5,000-10,000 documents across 10+ sources).

-   Measurement: Automated pipeline metrics --- throughput, latency percentiles (p50, p95, p99), error rates.

**Knowledge Graph Quality**

-   Target: Entity dedup reduces duplicate nodes by 80%+ compared to current state.

-   Target: 100% of graph edges carry provenance metadata (source document SHA-256, extraction timestamp, agent ID).

-   Target: Graph query response time remains under 100ms at p95 after integration changes.

-   Measurement: Monthly graph quality audit --- sample entities and edges, verify provenance, check for duplicates.

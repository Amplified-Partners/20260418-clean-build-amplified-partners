---
title: "Research Extraction Chunking Inference"
id: "research-extraction-chunking-inference"
version: 1
created: "2026-04-25"
type: "document"
topic_type: "research"
audience: "internal"
layer: "truth"
status: "filed"
signed_by: "Devon, 2026-04-25, devin-992682c244cf444f91e0a516498afbfd"
---

**Deep Research: LLM-Based Extraction, Chunking Science, and Local Inference**

*Compiled: March 14, 2026 \| For production system design*

**Table of Contents**

1.  [[LLM-Based Document Extraction at Scale]{.underline}](#bm_1_llm_based_document_extractio_998de5)

    -   1.1 [[Production Pipeline Architecture]{.underline}](#bm_11_production_pipeline_architecture)

    -   1.2 [[Preserving ALL Nuggets While Deduplicating]{.underline}](#bm_12_preserving_all_nuggets_whil_31e8d1)

    -   1.3 [[Handling Mixed Document Types]{.underline}](#bm_13_handling_mixed_document_types)

    -   1.4 [[Maintaining Attribution and Provenance]{.underline}](#bm_14_maintaining_attribution_and_41849c)

    -   1.5 [[98%+ Extraction Accuracy: What Actually Works]{.underline}](#bm_15_98_extraction_accuracy_what_58e039)

2.  [[Chunking Science for Maximum Usefulness]{.underline}](#bm_2_chunking_science_for_maximum_e873b0)

    -   2.1 [[Chunking for Both Retrieval and Synthesis]{.underline}](#bm_21_chunking_for_both_retrieval_4b54ec)

    -   2.2 [[Semantic vs Fixed-Size vs Structure-Aware Chunking]{.underline}](#bm_22_semantic_vs_fixed_size_vs_s_c26c03)

    -   2.3 [[Context Preservation: Overlapping Windows and Hierarchical Chunking]{.underline}](#bm_23_context_preservation_overla_63718b)

    -   2.4 [[Chunk Sizes by Use Case]{.underline}](#bm_24_chunk_sizes_by_use_case)

    -   2.5 [[2025--2026 Research and Frameworks]{.underline}](#bm_25_20252026_research_and_frameworks)

3.  [[Local Inference with Ollama]{.underline}](#bm_3_local_inference_with_ollama)

    -   3.1 [[Best Ollama Models for Extraction and Synthesis]{.underline}](#bm_31_best_ollama_models_for_extr_249777)

    -   3.2 [[Hardware Benchmarks: Mac Mini M4 vs. Hetzner AX162-R]{.underline}](#bm_32_hardware_benchmarks_mac_min_3b20c7)

    -   3.3 [[Workload Distribution: Two-Machine Architecture]{.underline}](#bm_33_workload_distribution_two_m_453554)

    -   3.4 [[Token Cost Comparison: Local vs. Cloud vs. Hybrid]{.underline}](#bm_34_token_cost_comparison_local_d8de3d)

    -   3.5 [[Specific Model Recommendations by Task]{.underline}](#bm_35_specific_model_recommendati_fd6582)

**1. LLM-Based Document Extraction at Scale**

**1.1 Production Pipeline Architecture**

The dominant production pattern as of early 2026 is a **modular, document-aware hybrid pipeline** that chains together specialized components rather than using a single end-to-end model. Research from a [[hybrid OCR-LLM framework (arXiv, October 2025)]{.underline}](https://arxiv.org/html/2510.10138v1) demonstrated that document-aware method selection --- choosing different extraction paradigms based on document structure --- achieves **perfect F1 scores (1.000)** with sub-second latency (0.97s average), while achieving a **54× speedup** over universal approaches.

**The canonical production stack:**

Document Ingestion\
↓\
Pre-processing / Format Detection\
• PDF → LlamaParse / Docling / Unstructured.io\
• DOCX/XLSX → direct extraction\
• Audio/Video → Whisper → transcript\
↓\
Document-Type Classification (lightweight classifier or LLM)\
↓\
Format-Specific Extraction (parallel workers)\
↓\
Schema-Enforced LLM Extraction (multi-pass)\
↓\
Validation Layer (algorithmic + cross-checking)\
↓\
Deduplication (exact + semantic)\
↓\
Provenance Attachment\
↓\
Output (JSON/JSONL with char-level source positions)

**Key libraries and frameworks (March 2026):**

  ------------------------------------------------------------- ---------------------------------------------------------------------------------------------------------------------------------------------------------------------- -----------------------------------------------------------------------------------
  Tool                                                          Role                                                                                                                                                                   Notes
  **LangExtract** (Google)                                      Multi-pass structured extraction with source grounding                                                                                                                 Works with Gemini, OpenAI, or local Ollama models; char-level provenance built in
  [**[Unstructured.io]{.underline}**](http://Unstructured.io)   Document parsing (slight edge on table extraction per [[kapa.ai benchmarks]{.underline}](https://www.kapa.ai/blog/how-to-build-a-rag-pipeline-from-scratch-in-2026))   Best for mixed-format enterprise corpora
  **LlamaParse**                                                Parsing PDFs and complex layouts                                                                                                                                       API-based; good for complex PDFs
  **Docling** (IBM)                                             Open-source document parsing                                                                                                                                           Strong structured document support
  **Whisper / WhisperX**                                        Audio transcription                                                                                                                                                    Used upstream of LLM extraction for voice content
  **Outlines**                                                  Structured generation / constrained decoding                                                                                                                           Enforces JSON schema compliance at decode time
  **LangChain / Pydantic**                                      Schema enforcement                                                                                                                                                     Pydantic annotations become prompts
  ------------------------------------------------------------- ---------------------------------------------------------------------------------------------------------------------------------------------------------------------- -----------------------------------------------------------------------------------

**For 5 million words (approx. 3.5M--7M tokens depending on document type):**\
At average extraction prompt overhead of 2--3× the source text (for context + schema), plan for **7--15M tokens per full pipeline pass**. With multi-pass for recall improvement, budget **15--45M tokens total** for the extraction phase alone.

**1.2 Preserving ALL Nuggets While Deduplicating**

This is a genuine tension: aggressive deduplication destroys unique facts that happen to be phrased similarly; insufficient deduplication creates redundant knowledge graphs. The solution is a **two-layer deduplication strategy**:

**Layer 1: Exact Hash Deduplication (at the raw document level)**

-   Apply before extraction using SHA-256 hashes on normalized document text

-   Catches verbatim duplicates (e.g., the same meeting notes uploaded twice)

-   Negligible compute cost

**Layer 2: Semantic Near-Duplicate Detection (at the extracted fact level)**\
Use **MinHash LSH (Locality Sensitive Hashing)** for scale. Research from [[Zilliz (July 2025)]{.underline}](https://zilliz.com/blog/data-deduplication-at-trillion-scale-solve-the-biggest-bottleneck-of-llm-training) demonstrates this is the only feasible approach at the scale of 50K+ facts:

Process:\
1. Decompose each extracted fact into character/word n-gram shingles\
2. Generate MinHash signature (fixed-length) for each fact\
3. Apply LSH banding to identify candidate near-duplicates\
4. For each candidate pair: compute actual Jaccard similarity\
5. Above threshold (typically 0.85): merge, preserving ALL source attributions

**Critical nuance:** When merging near-duplicates, **do not discard** --- instead, consolidate into a canonical representation while retaining the full list of source provenance (document ID, char offsets, date) for each variant. A fact mentioned in 12 different transcripts and 3 technical specs carries more evidential weight than one mentioned once.

**Layer 3: Semantic Embedding Deduplication (for near-paraphrases)**

-   Generate embeddings for each extracted fact using a lightweight local model (e.g., nomic-embed-text or mxbai-embed-large via Ollama)

-   Cluster at cosine similarity \> 0.92

-   Merge clusters, elect canonical form (typically longest/most specific), retain all source pointers

**What NOT to deduplicate:**

-   Facts that appear identical but occur at different time periods (temporal attribution matters)

-   Facts from different speakers/authors on the same topic (contradictions are signal, not noise)

-   Verbatim quotes vs. paraphrases (preserve both if provenance differs)

**1.3 Handling Mixed Document Types**

Each document type has distinct failure modes. The table below maps document type to recommended extraction approach:

  ------------------------ ---------------------------------------------------------------------------- --------------------------------------------------------------------------------------------------------
  Document Type            Primary Challenge                                                            Recommended Approach
  **Voice transcripts**    Proper nouns garbled, speaker attribution ambiguous                          Whisper → noun extraction pass → correction pass → speaker diarization (pyannote.audio)
  **Meeting notes**        Action items mixed with discussion, implicit context                         Structured extraction with explicit schema: {decisions, action\_items, open\_questions, context\_deps}
  **Technical specs**      Tables, code blocks, version numbers, cross-references                       Multimodal LLM or specialized table extractor; preserve code blocks verbatim
  **Code documentation**   Symbol references, function signatures, dependency graphs                    AST-aware chunking; extract signatures separately from descriptions
  **Monologues / talks**   No clear structure, topic drift, anaphora (\"as I mentioned earlier\...\")   Map-reduce: segment → per-segment extraction → cross-segment coreference resolution
  ------------------------ ---------------------------------------------------------------------------- --------------------------------------------------------------------------------------------------------

**For voice transcripts specifically:** A [[98% accuracy workflow from the LocalLLaMA community]{.underline}](https://www.reddit.com/r/LocalLLaMA/comments/1g2vhy3/creating_very_highquality_transcripts_with/) uses:

1.  Whisper-tbo for raw transcript

2.  LLM-based noun extraction (structured JSON output) to build a proper noun list

3.  Second LLM pass to correct transcript using noun list

4.  Pyannote.audio for speaker diarization

This multi-pass correction approach is what gets voice transcripts from \~85% to 98%+ accuracy on downstream extraction.

**Document-type routing logic:**

def route\_document(doc):\
if doc.has\_audio: return pipeline\_voice\
if doc.has\_code\_blocks: return pipeline\_technical\
if doc.source == \"meeting\": return pipeline\_meeting\
if doc.has\_tables: return pipeline\_tabular\
return pipeline\_prose \# default for specs, monologues, general docs

**1.4 Maintaining Attribution and Provenance**

**The gold standard: character-level source grounding.** Every extracted entity must map back to its exact position in the source document. [[LangExtract]{.underline}](https://genmind.ch/posts/LangExtract-Production-LLM-Powered-Information-Extraction/) implements this as a core primitive:

{\
\"extraction\_text\": \"quarterly revenue grew 23%\",\
\"extraction\_class\": \"financial\_metric\",\
\"char\_interval\": {\
\"start\_pos\": 4821,\
\"end\_pos\": 4847\
},\
\"source\_document\_id\": \"q3-earnings-transcript-2025-10-15\",\
\"extraction\_pass\": 1\
}

**Provenance schema for a production pipeline:**

{\
\"fact\_id\": \"uuid\",\
\"canonical\_text\": \"\...\",\
\"extraction\_confidence\": 0.94,\
\"sources\": \[\
{\
\"document\_id\": \"\...\",\
\"document\_type\": \"meeting\_notes\",\
\"document\_date\": \"2025-11-03\",\
\"char\_start\": 4821,\
\"char\_end\": 4847,\
\"speaker\": \"ewan\@bykerbusiness.ai\",\
\"extraction\_pass\": 2,\
\"extractor\_model\": \"qwen2.5:72b-q4\_K\_M\"\
}\
\],\
\"dedup\_cluster\_id\": \"\...\",\
\"first\_seen\": \"2025-08-15\",\
\"last\_seen\": \"2026-01-22\"\
}

**Provenance through the pipeline --- key rules:**

1.  **Never overwrite** intermediate states; append new extraction layers as additional source records

2.  **Pass document\_id + char\_offset through every transform** --- chunking, merging, deduplication

3.  For OCR-corrected documents: preserve the correction lineage at span level (edit type, source, confidence) per [[arxiv provenance framework (March 2026)]{.underline}](https://arxiv.org/html/2603.00884v1)

4.  Validate provenance by verifying document\[char\_start:char\_end\] == extraction\_text at pipeline close

**1.5 98%+ Extraction Accuracy: What Actually Works**

Getting from \~84% (basic LLM extraction) to 98%+ requires combining several techniques:

**1. Multi-Pass Extraction (biggest single gain)**

LangExtract benchmarks show:

-   1 pass: \~85% recall

-   2 passes: \~93% recall (recommended for most production cases)

-   3 passes: \~96% recall

\"First-pass wins\" for overlapping entities; subsequent passes fill gaps. The key is making each pass independently extracting (not aware of prior pass results) and then merging, which avoids the model anchoring on prior extractions.

**2. Domain-Knowledge Priming + Few-Shot Examples**

The [[fiscal document extraction study (arXiv, November 2025)]{.underline}](https://arxiv.org/html/2511.10659v1) achieved 73--96% structural accuracy (vs. lower baselines) by injecting domain knowledge into every prompt. For a mixed corpus covering business operations:

-   Provide a glossary of domain terms and acronyms in the system prompt

-   Include 3--5 few-shot extraction examples per document type

-   For tabular data: inject hierarchical structure knowledge

**3. Sequential Context Passing (for multi-page documents)**

For documents longer than the context window: **each page receives the prior page\'s extracted data as context**, enabling state carry-forward. This is essential for documents with:

-   Cross-page tables that continue

-   References like \"as noted above\" or \"per Section 3.2\"

-   Running totals or cumulative data

**4. Constrained / Structured Output Generation**

Use Pydantic schemas + response\_format (for OpenAI-compatible APIs) or Outlines for local models. This eliminates structural extraction failures entirely and ensures downstream parsability.

**5. Algorithmic Post-Validation**

After LLM extraction, apply domain-specific validation:

-   For financial data: verify sums, ratios, consistency checks

-   For dates: validate temporal ordering

-   For entities: cross-reference against known entity lists

-   For code: attempt parse/compile

**6. Model Size Matters**

From [[clinical NLP benchmark (JAMIA Open, September 2025)]{.underline}](https://academic.oup.com/jamiaopen/article/8/5/ooaf109/8270821) on 9 models across 28 extraction tasks:

  ----------------- -----------------
  Model             Utility Score
  Llama-3.3-70B     0.760 (highest)
  Phi-4-14B         0.751
  Qwen-2.5-14B      0.748
  DeepSeek-R1-14B   0.744
  ----------------- -----------------

These outperformed fine-tuned RoBERTa on 17 of 28 tasks. The 70B model class is the practical minimum for high-recall extraction across heterogeneous document types.

**7. Chunk Size for Extraction**

Per [[LangExtract production benchmarks]{.underline}](https://genmind.ch/posts/LangExtract-Production-LLM-Powered-Information-Extraction/):

  -------------- ---------- ---------- -------------------------------
  Chunk Size     Accuracy   Speed      Recommended Use
  1,000 chars    Highest    Slower     Compliance, critical accuracy
  2,000 chars    High       Balanced   **Production default**
  3,000 chars    Good       Faster     High-volume batches
  5,000+ chars   Lower      Fastest    First-pass triage only
  -------------- ---------- ---------- -------------------------------

**2. Chunking Science for Maximum Usefulness**

**2.1 Chunking for Both Retrieval and Synthesis**

Documents that serve **dual purposes** (retrieval/RAG *and* full synthesis) require a **dual-index strategy** --- not a single chunking pass:

**Dual-Index Architecture:**

Source Document\
↓\
\[Path A: Retrieval Index\] \[Path B: Synthesis Index\]\
Small chunks (128--256 tokens) Large chunks / full sections\
High semantic granularity Preserves full context\
Good for: \"Find me facts about X\" Good for: \"Summarize our Q3 strategy\"\
↓ ↓\
Vector DB (dense retrieval) Summarization pipeline\
+ Sparse index (BM25) + Hierarchical reduce\
↓ ↓\
Query-time assembly Full document synthesis

The key insight: **use different chunk sizes for different downstream tasks**. Trying to optimize a single chunk size for both retrieval precision and synthesis quality is a local optimum trap.

**For the dual-path system:**

-   Path A: 200--512 token chunks, 10--20% overlap, with metadata (section title, document type, date)

-   Path B: 1,000--2,000 token sections, aligned to document structure (headers, topic shifts), with parent context prepended

**2.2 Semantic vs Fixed-Size vs Structure-Aware Chunking**

**Benchmark summary (multiple 2024--2026 studies):**

  ----------------------------------------- --------------------------------------------------------------------- ----------- ----------- ------------------------------------------
  Strategy                                  Best Accuracy                                                         Speed       Cost        Best For
  **Page-level**                            0.648 (NVIDIA 2024 benchmark winner)                                  Fast        Low         PDFs, paginated documents
  **Recursive (512 tok, 10-20% overlap)**   0.85--0.90 recall (Chroma)                                            Fast        Low         **Best all-round default**
  **Semantic chunking**                     Up to 9% better recall than recursive; 0.919 LLM-enhanced             Slow        High        Dense unstructured text, research papers
  **Sentence-based**                        \~= semantic up to 5,000 tokens                                       Medium      Medium      Conversational data, Q&A, transcripts
  **LLM-based**                             Highest quality (context-aware breaks)                                Very slow   Very high   High-value documents where cost permits
  **Late chunking**                         Consistently better than naive chunking across retrieval benchmarks   Medium      Medium      Long documents with cross-references
  **Fixed-size (character)**                Lowest                                                                Fastest     Lowest      Logs, emails, unstructured large corpora
  ----------------------------------------- --------------------------------------------------------------------- ----------- ----------- ------------------------------------------

**What the research actually says (2025--2026):**

-   [[Vecta February 2026 benchmark]{.underline}](https://www.firecrawl.dev/blog/best-chunking-strategies-rag) across 50 academic papers: Recursive 512-token splitting came **first at 69% accuracy**; semantic chunking fell to **54%** after producing fragments averaging only 43 tokens --- a critical failure mode in semantic chunking that is often ignored

-   [[NAACL 2025 Findings]{.underline}](https://www.firecrawl.dev/blog/best-chunking-strategies-rag): \"The computational costs of semantic chunking aren\'t justified by consistent gains, with fixed 200-word chunks matching or beating semantic chunking across retrieval and answer generation tasks\"

-   [[MDPI Bioengineering, November 2025]{.underline}](https://www.firecrawl.dev/blog/best-chunking-strategies-rag): Adaptive chunking aligned to logical topic boundaries hit **87% accuracy vs. 13% for fixed-size baselines** (p=0.001) --- this is the case *in favor* of semantic chunking, specifically for clinical/technical documents with clear logical structure

-   [[January 2026 systematic analysis]{.underline}](https://www.firecrawl.dev/blog/best-chunking-strategies-rag): A \"context cliff\" exists at approximately **2,500 tokens** where response quality drops for most models; sentence chunking matched semantic chunking up to \~5,000 tokens at a fraction of the cost

**Practical recommendation for a mixed corpus (voice transcripts + meeting notes + technical specs + code docs):**

Use **document-type-aware chunking routing**:

  -------------------- --------------------------------------------------- -----------------------------------------------
  Document Type        Recommended Strategy                                Why
  Voice transcripts    Sentence-based, 5--7 sentences per chunk            Natural speech units; no structural headers
  Meeting notes        Structure-aware (by agenda item/section header)     Clear structure exists; don\'t fragment items
  Technical specs      Recursive 512 tokens with code block preservation   Preserves code integrity
  Code documentation   Function/class-level splitting                      Semantic unit is the function
  Monologues           Semantic chunking with 300--500 token target        Topic shifts are the only meaningful boundary
  -------------------- --------------------------------------------------- -----------------------------------------------

**2.3 Context Preservation: Overlapping Windows and Hierarchical Chunking**

**Three approaches to context preservation, ranked by quality:**

**Tier 1: Contextual Retrieval (Anthropic technique)**\
Before chunking, an LLM generates a short context description for each chunk that captures the chunk\'s relationship to the broader document. This description is prepended to the chunk and embedded together. [[Pinecone\'s analysis]{.underline}](https://www.pinecone.io/learn/chunking-strategies/) shows this approach --- now built into Claude\'s document handling --- preserves high-level document meaning within each granular chunk.

Cost: Requires one LLM call per chunk during indexing. Mitigated by prompt caching (the document remains in the cache context across all chunk contextualization calls).

**Tier 2: Late Chunking**\
Embed the entire document first (using a long-context embedding model), then chunk. This means each token\'s embedding contains the full contextual information before chunking occurs. [[OpenReview paper]{.underline}](https://openreview.net/pdf?id=74QmBTV0Zf) demonstrates superior results across BeIR retrieval benchmarks.

Cost: Requires a long-context embedding model (e.g., jina-embeddings-v3 with 8,192 token context). For documents longer than the embedding context window, use the \"long late chunking\" extension.

**Tier 3: Overlapping Windows**\
Classic approach: each chunk shares 10--20% of tokens with adjacent chunks.

-   A January 2026 systematic analysis found overlap provided **no measurable benefit** when using SPLADE retrieval with Mistral-8B on Natural Questions

-   Still recommended for simple pipelines as insurance against boundary splits

-   Standard: 10--20% overlap (50--100 tokens for a 512-token chunk)

**Hierarchical chunking for synthesis:**\
A multi-layer index enables both precision retrieval and broad synthesis from the same document store:

Layer 1: Document summaries (1 per document)\
↓\
Layer 2: Section summaries (1 per major section)\
↓\
Layer 3: Paragraph/passage chunks (200--512 tokens)\
↓\
Layer 4: Sentence-atomic index (for cross-reference expansion)

At query time:

-   Broad synthesis → query Layer 1--2

-   Factual retrieval → query Layer 3--4, expand to Layer 2 for context

This architecture is used in production by enterprise-grade RAG systems and frameworks like LlamaIndex\'s multi-granularity retrieval.

**2.4 Chunk Sizes by Use Case**

  ------------------------------- ------------------------------------ -------------------------- ----------------------------------------
  Use Case                        Optimal Chunk Size                   Overlap                    Strategy
  **Code generation**             Function/class block (variable)      None                       AST-aware; never split mid-function
  **Fact-based RAG**              128--256 tokens                      5--10%                     Sentence-based or recursive
  **Content creation**            512--1,024 tokens                    10--20%                    Semantic or recursive
  **Knowledge graph ingestion**   512--1,024 tokens                    0--10%                     Structure-aware; entity-dense
  **Full document synthesis**     1,500--2,000 tokens                  0%                         Structure-aligned sections
  **Meeting/transcript RAG**      200--350 tokens                      15--20%                    Sentence-based, per-speaker segments
  **Legal/compliance**            400--600 tokens                      15--25% (sliding window)   Preserve full clause integrity
  **Voice transcripts**           5--7 sentences (\~150--300 tokens)   2--3 sentence overlap      Sentence-based with speaker annotation
  ------------------------------- ------------------------------------ -------------------------- ----------------------------------------

**The \"context cliff\" finding (January 2026):**\
Retrieved context exceeding \~2,500 tokens consistently degrades response quality across tested models (GPT-4.1, Claude 4, Gemini 2.5). This means even if you retrieve large chunks for synthesis, **truncate or compress the passed context** to stay under 2,500 tokens per retrieved passage when combining multiple results.

**2.5 2025--2026 Research and Frameworks**

**Landmark papers:**

  ------------------------------------------------------------------------------------------------------------------------------------------------------ --------------- ---------------------------------------------------------------------------------------------------------------------------------------------------------
  Paper                                                                                                                                                  Date            Key Finding
  [[Late Chunking: Contextual Chunk Embeddings]{.underline}](https://openreview.net/pdf?id=74QmBTV0Zf)                                                   2024            Embed full document first, then chunk --- superior retrieval across all tested strategies
  [[Evaluating Advanced Chunking Strategies for RAG (arXiv 2504.19754)]{.underline}](https://arxiv.org/abs/2504.19754)                                   April 2025      Contextual retrieval preserves semantic coherence better but costs more; late chunking more efficient but sacrifices completeness --- neither dominates
  NAACL 2025 Findings                                                                                                                                    2025            Fixed 200-word chunks match or beat semantic chunking at a fraction of the compute cost
  [[MDPI Bioengineering clinical decision support study]{.underline}](https://www.firecrawl.dev/blog/best-chunking-strategies-rag)                       November 2025   Adaptive topic-boundary chunking: 87% vs. 13% fixed-size (p=0.001)
  [[Optimising retrieval performance in RAG systems (ScienceDirect)]{.underline}](https://www.sciencedirect.com/science/article/pii/S0950705125019343)   January 2026    Comprehensive benchmark; \"context cliff\" at 2,500 tokens identified
  [[Vecta benchmark]{.underline}](https://www.firecrawl.dev/blog/best-chunking-strategies-rag)                                                           February 2026   Recursive 512-token splitting beats semantic chunking on 50 academic papers
  ------------------------------------------------------------------------------------------------------------------------------------------------------ --------------- ---------------------------------------------------------------------------------------------------------------------------------------------------------

**Notable 2025 frameworks:**

-   **Fenic** ([[typedef.ai]{.underline}](http://typedef.ai)): DataFrame-style chunking with semantic reduction, batch-by-token-budget, and structure-aware markdown chunking

-   **Contextual Retrieval** (Anthropic): LLM-generated context prepended to each chunk before embedding; available via Claude API with prompt caching

-   **Agentic Chunking**: Model decides per-document which strategy to use, routing to semantic, page-level, or function-level based on document type detection

-   **LlamaIndex multi-granularity**: Hierarchical index with small-to-big retrieval and parent document expansion

[]{#bm_3_local_inference_with_ollama .anchor}**3. Local Inference with Ollama**

**3.1 Best Ollama Models for Extraction and Synthesis**

As of early 2026, the ecosystem has converged around a clear model hierarchy for document processing tasks. Note: Ollama wraps llama.cpp, so model performance figures below are applicable whether running via ollama run directly or via the Ollama REST API.

**Overall ranking for document extraction tasks:**

Based on [[JAMIA Open clinical NLP benchmark (28 extraction tasks)]{.underline}](https://academic.oup.com/jamiaopen/article/8/5/ooaf109/8270821), [[community structured output testing]{.underline}](https://www.reddit.com/r/LocalLLaMA/comments/1jflouy/structured_outputs_with_ollama_whats_your_recipe/), and [[WhatLLM January 2026 rankings]{.underline}](https://whatllm.org/blog/best-open-source-models-january-2026):

  ------ --------------------------------------- --------------- --------------------------------------------
  Rank   Model                                   Utility Score   Best Use
  1      **Llama-3.3-70B-Instruct** (Q4\_K\_M)   0.760           General extraction, instruction following
  2      **Qwen2.5-72B-Instruct** (Q4\_K\_M)     \~0.755         Knowledge-dense extraction, research tasks
  3      **Phi-4-14B** (Q5\_K\_M)                0.751           Efficient mid-size extraction
  4      **Qwen2.5-14B-Instruct**                0.748           Good quality/speed trade-off
  5      **DeepSeek-R1-14B**                     0.744           Reasoning-heavy extraction
  ------ --------------------------------------- --------------- --------------------------------------------

**Community consensus on structured output reliability:**\
\"Qwen performed the best. Llama second best. Gemma and phi were a distant 3rd and 4th\" for extracting data from unstructured text with Ollama\'s structured output schema enforcement. Llama 3.1/3.2/3.3 models and Qwen models are consistently the most reliable for JSON schema adherence.

**3.2 Hardware Benchmarks: Mac Mini M4 vs. Hetzner AX162-R**

**Mac Mini M4 Pro (64GB)**

**Official specs ([[Apple M4 Pro]{.underline}](https://www.apple.com/newsroom/2024/10/apple-introduces-m4-pro-and-m4-max/)):**

-   Memory bandwidth: **273 GB/s** (unified memory; 75% increase over M3 Pro)

-   14-core CPU (10 performance + 4 efficiency), 20-core GPU

-   64GB LPDDR5X unified memory (all available for model weights)

-   Neural Engine: 38 TOPS

-   Power draw: **\~40--65W** under LLM load

**Observed inference speeds with Ollama:**

  -------------------------- -------------------- ---------------------------------------------------------------------------------------------------------------------------------------------------------
  Model                      Speed (tokens/sec)   Notes
  Llama 3.2 3B (Q4\_K\_M)    70--80 t/s           [[Mac Mini M4 Pro 64GB Reddit benchmark]{.underline}](https://www.reddit.com/r/LocalLLaMA/comments/1hax4ue/)
  Qwen 2.5 32B (Q4\_K\_M)    11--12 t/s           [[Introl hardware guide, August 2025]{.underline}](https://introl.com/blog/local-llm-hardware-pricing-guide-2025)
  Qwen 3 32B (Q4\_K\_M)      11.7 t/s             [[Archy.net benchmark vs. dual RTX 3090, Feb 2026]{.underline}](https://www.archy.net/why-my-mac-mini-m4-outperforms-dual-rtx-3090s-for-llm-inference/)
  Llama 3.3 70B (Q4\_K\_M)   \~5 t/s              At limit of 64GB; will swap at longer contexts
  -------------------------- -------------------- ---------------------------------------------------------------------------------------------------------------------------------------------------------

**Critical observation:** The Mac Mini M4 64GB running Qwen3-32B at **11.7 tokens/sec beat dual RTX 3090s (48GB VRAM total) at 9.2 tokens/sec** --- a 27% speed advantage --- while consuming **40W vs. 700W** (22× more efficient). This is because LLM inference is **memory-bandwidth bound**, not compute bound. The M4 Pro\'s 273 GB/s unified bandwidth with zero PCIe transfer overhead outperforms discrete GPU setups for mid-size models.

**For 70B models on the Mac Mini M4 Pro 64GB:**\
A 70B model at Q4\_K\_M requires \~45--50GB --- barely fits in 64GB after OS overhead. Expect 3--5 t/s at short context, degrading with longer contexts as the KV cache fills available memory. For reliable 70B inference, the **M4 Max 128GB** (546 GB/s bandwidth) is the right Apple Silicon target.

**Hetzner AX162-R (AMD EPYC 9454P, 256GB DDR5)**

**Official specs ([[Hetzner press release, February 2024]{.underline}](https://www.hetzner.com/pressroom/new-ax162/)):**

-   CPU: AMD EPYC 9454P (Genoa, Zen 4)

-   Cores: **48 cores / 96 threads**

-   RAM: **256GB DDR5 ECC registered** (8 × 32GB)

-   Storage: 2 × 1.92TB Gen4 NVMe SSD

-   Memory bandwidth: \~307 GB/s theoretical (8-channel DDR5)

-   Price: **€199/month** (\~\$233 USD) --- [[Reddit community confirmed]{.underline}](https://www.reddit.com/r/hetzner/comments/1jvcvso/why_would_anyone_choose_cloud_over_dedicated/)

**Measured inference speeds (llama.cpp on similar EPYC Genoa/Turin platforms):**

  --------------------------------- ------------------------------------------ ------------------------------------------------------- --------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------
  Model                             Config                                     Speed (tokens/sec)                                      Source
  Llama-3.1-70B F16                 Single socket, 16 threads                  **2.3--2.4 t/s** (tg128)                                [[llama.cpp GitHub discussion \#11733]{.underline}](https://github.com/ggml-org/llama.cpp/discussions/11733)
  Llama-3.1-70B F16                 Dual socket, 32 threads, NUMA distribute   **4.3 t/s** (tg128)                                     Same source, with warm-up trick
  Mistral-Small-24B BF16            Dual EPYC 9124, 35k ctx                    **12.5 t/s**                                            llama.cpp issue \#11744
  DeepSeek-R1-Distill 70B Q8        Dual EPYC 9124, 35k ctx                    **4.6 t/s**                                             Same source
  Llama-3.1-70B (AMD PACE + PARD)   EPYC 9755, batch=1                         **380 t/s** (system throughput with data parallelism)   [[AMD technical article, July 2025]{.underline}](https://www.amd.com/en/developer/resources/technical-articles/2025/speculative-llm-inference-on-the-5th-gen-amd-epyc-processors-wit.html)
  --------------------------------- ------------------------------------------ ------------------------------------------------------- --------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------

**Important caveat on the AMD PACE 380 t/s figure:** This is achieved with AMD\'s proprietary inference stack (PACE + PARD speculative decoding), not vanilla Ollama. With standard Ollama/llama.cpp on the AX162-R (EPYC 9454P, 256GB), realistic throughput for 70B models is **3--6 t/s single-session** using Q4\_K\_M quantization.

**The \"warm-up trick\" for EPYC NUMA systems:**\
Running a short generation pass before the main inference run improves token generation rate by \~80% on dual-socket EPYC systems due to optimal tensor placement in NUMA memory. This is a known llama.cpp quirk with EPYC multi-socket configs. Without it: \~2.4 t/s; with it: \~4.3 t/s on 70B F16.

**Hardware Comparison Table**

  -------------------------- -------------------------------------- ------------------------------------------------------------------------
  Metric                     Mac Mini M4 Pro 64GB                   Hetzner AX162-R
  **Memory bandwidth**       273 GB/s (unified)                     \~307 GB/s (8-ch DDR5)
  **Usable memory**          64GB (shared CPU/GPU)                  256GB RAM
  **Max model size**         \~50GB (with OS overhead)              \~200GB (with OS overhead)
  **70B Q4\_K\_M speed**     \~5 t/s                                \~4--5 t/s
  **32B Q4\_K\_M speed**     \~11--12 t/s                           \~8--12 t/s
  **8B Q4\_K\_M speed**      \~40--60 t/s                           \~25--35 t/s
  **Power draw**             40--65W                                200--400W
  **Cost**                   \~\$2,400 hardware                     €199/month
  **Best advantage**         Power efficiency, ease of deployment   Large model size (70B+ fit comfortably), multiple concurrent instances
  **Concurrent inference**   1 model at a time (memory limited)     Multiple 7B--14B instances simultaneously
  -------------------------- -------------------------------------- ------------------------------------------------------------------------

**The AX162-R\'s true advantage:** With 256GB RAM, it can comfortably load and run **multiple model instances simultaneously** --- e.g., a 70B extraction model + a 14B taxonomy model + a 7B embedding model --- all without swapping. For a batch pipeline that chains models, this is more valuable than raw single-instance speed.

**3.3 Workload Distribution: Two-Machine Architecture**

For processing \~5 million words, the optimal distribution between a Mac Mini M4 Pro (64GB) and Hetzner AX162-R (256GB, 48-core EPYC) is:

**Token estimate for 5M words:**

-   5M words ≈ 6.5--7.5M source tokens

-   With extraction prompts and output: **\~15--25M tokens total**

-   Multi-pass (2 passes): **\~30--50M tokens total**

**Recommended role assignment:**

  ------------------------------------------- -------------------- ---------------------------------------------------------------
  Task                                        Assign To            Reason
  **Heavy extraction (70B model)**            AX162-R              70B fits in 256GB with room for KV cache at long contexts
  **Taxonomy/classification (14B model)**     AX162-R (parallel)   Can run alongside 70B without eviction
  **Embedding generation**                    Mac Mini M4          Fast, lightweight; \~60 t/s on 7B embedding models
  **Summarization-without-reduction (32B)**   Mac Mini M4          32B fits cleanly in 64GB; M4 bandwidth handles it efficiently
  **Document parsing / pre-processing**       AX162-R              48 cores handle parallel parsing at CPU level
  **Post-processing / deduplication**         AX162-R              Pure compute; benefits from 48 EPYC cores
  **API serving (interactive queries)**       Mac Mini M4          Low-latency response; keeps AX162-R free for batch work
  ------------------------------------------- -------------------- ---------------------------------------------------------------

**Coordination architecture (two-machine pipeline):**

\[Input Queue: Redis or file-based job queue\]\
↓ ↓\
\[Mac Mini M4\] \[AX162-R EPYC\]\
Embedding model 70B extractor\
(nomic-embed) 14B classifier\
32B summarizer Pre/post processing\
API gateway Batch pipeline runner\
↓ ↓\
\[Shared output store: NFS or object storage\]\
↓\
\[Merging + deduplication (AX162-R)\]\
↓\
\[Final indexed output\]

**Practical implementation:**

-   Use **Ollama REST API** on both machines; orchestrate with Python worker pool

-   Mac Mini M4: OLLAMA\_HOST=0.0.0.0:11434 to expose API

-   AX162-R: Run multiple Ollama instances on different ports for model isolation

-   For a 5M word corpus: estimate **48--96 hours** for full 2-pass extraction on the AX162-R at 4--5 t/s (70B), parallelizable across document batches

-   Consider [**[GridLLM]{.underline}**](https://www.reddit.com/r/LocalLLaMA/comments/1mfzg8h/) (open-source) for orchestrating requests across both machines from a single endpoint

**For vLLM on the AX162-R (higher throughput at the cost of setup complexity):**\
[[Red Hat\'s benchmarks (August 2025)]{.underline}](https://developers.redhat.com/articles/2025/08/08/ollama-vs-vllm-deep-dive-performance-benchmarking) show vLLM achieving **793 t/s peak vs. Ollama\'s 41 t/s** under high-concurrency conditions. For batch pipeline workloads (not interactive use), vLLM with AMD ZenDNN backend on the EPYC will substantially outperform Ollama. However, Ollama is significantly simpler to deploy and maintain, and for a two-machine internal pipeline, its throughput is likely sufficient.

**3.4 Token Cost Comparison: Local vs. Cloud vs. Hybrid**

**Current API Pricing (March 2026)**

  ------------------------ -------------------- ----------------------- ------------------------
  Model                    Provider             Input (per 1M tokens)   Output (per 1M tokens)
  Claude Opus 4            Anthropic            \$15.00                 \$75.00
  Claude Sonnet 4          Anthropic            \$3.00                  \$15.00
  Claude Haiku 4.5         Anthropic            \$1.00                  \$5.00
  GPT-4.1                  OpenAI               \$2.00                  \$8.00
  GPT-4.1 mini             OpenAI               \$0.40                  \$1.60
  GPT-4.1 nano             OpenAI               \$0.10                  \$0.40
  Gemini 2.5 Pro           Google               \$1.25--\$2.50          \$5.00--\$10.00
  Llama 3.3 70B (hosted)   OpenRouter           \$0.12                  \$0.30
  Qwen 2.5 72B (hosted)    Together/Fireworks   \$0.15--\$0.40          \$0.40--\$1.00
  ------------------------ -------------------- ----------------------- ------------------------

*Sources: [[SitePoint TCO Analysis (March 2026)]{.underline}](https://www.sitepoint.com/local-llms-vs-cloud-api-cost-analysis-2026/), [[IntuitionLabs pricing guide]{.underline}](https://intuitionlabs.ai/articles/llm-api-pricing-comparison-2025)*

**Cost for Processing 5 Million Words**

**Assumptions:**

-   5M words ≈ 7M source tokens

-   Extraction prompt overhead (system prompt + schema + few-shot): \~3× source = 21M input tokens

-   Output (extracted facts + JSON): \~30% of input = 6.3M output tokens

-   2-pass: ×2 = **42M input + 12.6M output tokens**

  --------------------------------------- ------------ ------------------- ------------------- ------------------------------------
  Approach                                Model        Input Cost          Output Cost         **Total**
  **Cloud: Claude Sonnet 4**              Anthropic    \$126               \$189               **\$315**
  **Cloud: GPT-4.1**                      OpenAI       \$84                \$100               **\$184**
  **Cloud: Claude Haiku 4.5**             Anthropic    \$42                \$63                **\$105**
  **Cloud: GPT-4.1 mini**                 OpenAI       \$16.80             \$20.16             **\$37**
  **Hosted open-weight: Llama 3.3 70B**   OpenRouter   \$5.04              \$3.78              **\$8.82**
  **Local: AX162-R (€199/month)**         Any          Power: \~\$5        Power: \~\$5        **\~\$10/month total**
  **Local: Mac Mini M4 (amortized)**      Any          \~\$2 electricity   \~\$2 electricity   **Hardware: \~\$67/month (36-mo)**
  --------------------------------------- ------------ ------------------- ------------------- ------------------------------------

**The math for a one-time 5M word extraction job:**

-   Claude Sonnet 4 (best quality): \~\$315 one-time --- compelling for a single run

-   GPT-4.1 mini: \~\$37 --- very cost-effective if quality is sufficient

-   Hosted Llama 3.3 70B: \~\$9 --- near-local cost with cloud convenience

-   AX162-R running Qwen2.5-72B locally: electricity cost is negligible (\~\$1--2); the server cost is amortized over other workloads

**Break-even analysis (from [[SitePoint TCO, March 2026]{.underline}](https://www.sitepoint.com/local-llms-vs-cloud-api-cost-analysis-2026/)):**

-   Local vs. OpenAI (consumer hardware): breaks even at **2M--3M tokens/day**

-   Local vs. OpenAI (medium enterprise): **18--24 months** payback

-   Local vs. open-weight hosted APIs: **15M--20M tokens/day** to justify hardware

**For a production system processing millions of words repeatedly** (e.g., ongoing ingestion of new documents), local is clearly superior beyond the initial setup. For a **one-time 5M word corpus**, the cheapest cloud option (hosted Llama 3.3 70B at \~\$9) is competitive with local power costs.

**3.5 Specific Model Recommendations by Task**

**Entity Extraction**

**Primary: qwen2.5:72b-q4\_K\_M**

-   Best structured output adherence in community testing

-   Strong at understanding domain-specific entities without fine-tuning

-   128K context window handles large document chunks

-   Ollama command: ollama run qwen2.5:72b-q4\_K\_M

-   Memory: \~47GB --- fits in AX162-R with headroom; too large for Mac Mini M4 base model

**Fallback (if speed matters more than accuracy): qwen2.5:14b-q5\_K\_M**

-   Utility score 0.748 (only slightly below 70B tier)

-   Runs at \~20--25 t/s on AX162-R

-   Memory: \~11GB --- runs on either machine easily

**For NER specifically:** All models showed \"consistently low NER performance\" in zero-shot settings per JAMIA Open benchmarks. For NER at 98%+ accuracy, fine-tune a small model (7B--14B) on domain-specific entity examples using Unsloth, or use a dedicated NER model for entity detection before LLM-based relation extraction.

**Summarization-Without-Reduction**

**Primary: llama3.3:70b-q4\_K\_M**

-   Best instruction following (highest IFEval benchmark score vs. Qwen2.5-72B)

-   \"Summarization without reduction\" requires following explicit length and comprehensiveness instructions --- Llama 3.3 is more instruction-compliant than Qwen in this domain

-   For map-reduce summarization of long docs: chunk at 1,500--2,000 tokens → summarize each → reduce

**Alternative: mistral-small:24b-q6\_K\_M** (Mistral Small 3.2, June 2025)

-   Runs at \~12 t/s on AX162-R with 256GB

-   Excellent at following length constraints

-   128K context; drop-in for document summarization tasks

**Taxonomy Labelling**

**Primary: qwen2.5:14b-q5\_K\_M**

-   Classification and labelling tasks are less demanding than extraction

-   Qwen\'s strong instruction following makes it reliable for consistent taxonomy application

-   At 14B and Q5\_K\_M, runs at \~20 t/s on AX162-R

**Alternative for very high speed: qwen3:30b-a3b-q4\_K\_M** (MoE variant)

-   Only \~3B parameters active per token; runs at **30--34 t/s** on GPU, roughly comparable on CPU

-   Ideal for high-volume classification where throughput matters

-   Quality: \"Outcompetes QwQ-32B with 10× fewer activated parameters\" per [[Ollama model card]{.underline}](https://ollama.com/library/qwen3:30b-a3b)

**Embedding Generation (for both chunking and deduplication)**

**Primary: nomic-embed-text** via Ollama

-   ollama pull nomic-embed-text

-   Good all-round semantic embeddings for RAG

-   Runs very fast (\~200--300 docs/sec on either machine)

**For late chunking (requires long-context embedding):**\
Use jina-embeddings-v3 (8,192 token context) or bge-m3 --- both available via Ollama or direct llama.cpp.

**Full Pipeline Model Routing (Recommended)**

Task Model Hardware\
─────────────────────────── ─────────────────── ──────────\
Document pre-parsing CPU (parallel) AX162-R\
Embedding generation nomic-embed-text Mac Mini M4\
Entity extraction (pass 1) qwen2.5:72b AX162-R\
Entity extraction (pass 2) qwen2.5:72b AX162-R\
Taxonomy labelling qwen2.5:14b AX162-R (parallel)\
Summarization llama3.3:70b AX162-R\
Deduplication (semantic) nomic-embed-text Mac Mini M4\
Output validation/QA qwen2.5:14b Either\
Interactive RAG queries qwen2.5:32b Mac Mini M4

**Appendix: Key Quantitative Reference Tables**

**Model Memory Requirements (Ollama, Q4\_K\_M unless noted)**

  ------------------------------ ------------------- ----------------------------------------------
  Model                          VRAM/RAM Required   Notes
  Qwen2.5-72B Q4\_K\_M           \~47GB              Fits AX162-R; too large for Mac Mini M4 base
  Llama-3.3-70B Q4\_K\_M         \~45GB              Same
  Qwen2.5-32B Q4\_K\_M           \~22GB              Fits Mac Mini M4 Pro 64GB comfortably
  Mistral-Small-24B Q6\_K\_M     \~18--20GB          Fits Mac Mini M4 Pro 64GB
  Qwen3-30B-A3B Q4\_K\_M (MoE)   \~21GB              MoE: fast; fits Mac Mini M4 Pro 64GB
  Qwen2.5-14B Q5\_K\_M           \~11GB              Fits any machine
  Llama3.2-3B Q4\_K\_M           \~2.5GB             Extremely fast on M4
  ------------------------------ ------------------- ----------------------------------------------

**Throughput Summary (Single-Instance, Batch Processing)**

  ----------------------------- -------------- ------------- ---------------------
  Machine                       Model          Approx. t/s   Words/hour (output)
  Mac Mini M4 Pro 64GB          32B Q4\_K\_M   11--12        \~8,000
  Mac Mini M4 Pro 64GB          70B Q4\_K\_M   \~5           \~3,500
  AX162-R (EPYC 9454P, 256GB)   70B Q4\_K\_M   4--5          \~3,200
  AX162-R (EPYC 9454P, 256GB)   14B Q5\_K\_M   20--25        \~16,000
  AX162-R (EPYC 9454P, 256GB)   8B Q4\_K\_M    30--40        \~25,000
  ----------------------------- -------------- ------------- ---------------------

*Assumes \~750 words per 1,000 output tokens; actual output depends heavily on task verbosity.*

**Sources**

1.  [[Hybrid OCR-LLM Framework for Enterprise-Scale Document Extraction --- arXiv, October 2025]{.underline}](https://arxiv.org/html/2510.10138v1)

2.  [[LangExtract: Production LLM-Powered Information Extraction --- genmind.ch, December 2025]{.underline}](https://genmind.ch/posts/LangExtract-Production-LLM-Powered-Information-Extraction/)

3.  [[How to Build a RAG Pipeline from Scratch in 2026 --- kapa.ai, January 2026]{.underline}](https://www.kapa.ai/blog/how-to-build-a-rag-pipeline-from-scratch-in-2026)

4.  [[Best Chunking Strategies for RAG in 2026 --- Firecrawl, October 2025, updated February 2026]{.underline}](https://www.firecrawl.dev/blog/best-chunking-strategies-rag)

5.  [[Chunking Strategies to Improve LLM RAG Pipeline Performance --- Weaviate, September 2025]{.underline}](https://weaviate.io/blog/chunking-strategies-for-rag)

6.  [[Evaluating Advanced Chunking Strategies for RAG --- arXiv 2504.19754, April 2025]{.underline}](https://arxiv.org/abs/2504.19754)

7.  [[Late Chunking: Contextual Chunk Embeddings --- OpenReview]{.underline}](https://openreview.net/pdf?id=74QmBTV0Zf)

8.  [[Leveraging Open-Source LLMs for Clinical Information Extraction --- JAMIA Open, September 2025]{.underline}](https://academic.oup.com/jamiaopen/article/8/5/ooaf109/8270821)

9.  [[Why My Mac Mini M4 Outperforms Dual RTX 3090s for LLM Inference --- archy.net, February 2026]{.underline}](https://www.archy.net/why-my-mac-mini-m4-outperforms-dual-rtx-3090s-for-llm-inference/)

10. [[Unlocking LLM Performance on EPYC CPUs --- AMD whitepaper, August 2025]{.underline}](https://www.amd.com/content/dam/amd/en/documents/epyc-technical-docs/white-papers/unlocking-the-power-of-llm-performance-on-epyc.pdf)

11. [[Speculative LLM Inference on 5th Gen AMD EPYC --- AMD, July 2025]{.underline}](https://www.amd.com/en/developer/resources/technical-articles/2025/speculative-llm-inference-on-the-5th-gen-amd-epyc-processors-wit.html)

12. [[Unlocking Optimal LLM Performance on EPYC with vLLM --- AMD, November 2025]{.underline}](https://www.amd.com/en/blogs/2025/unlocking-optimal-llm-performance-on-amd-epyc--cpus-with-vllm.html)

13. [[Local LLMs vs Cloud APIs: 2026 TCO Analysis --- SitePoint, March 2026]{.underline}](https://www.sitepoint.com/local-llms-vs-cloud-api-cost-analysis-2026/)

14. [[Cost Comparison: Ollama Self-Hosting vs Cloud APIs --- Ventus Servers, January 2026]{.underline}](https://ventusserver.com/self-hosting-vs-cloud-apis/)

15. [[Hetzner AX162 announcement --- Hetzner, February 2024]{.underline}](https://www.hetzner.com/pressroom/new-ax162/)

16. [[Dual EPYC Genoa/Turin token generation performance --- llama.cpp GitHub, February 2025]{.underline}](https://github.com/ggml-org/llama.cpp/discussions/11733)

17. [[Ollama vs. vLLM: Deep Dive Performance Benchmarking --- Red Hat, August 2025]{.underline}](https://developers.redhat.com/articles/2025/08/08/ollama-vs-vllm-deep-dive-performance-benchmarking)

18. [[Apple M4 Pro and M4 Max introduction --- Apple Newsroom, October 2024]{.underline}](https://www.apple.com/newsroom/2024/10/apple-introduces-m4-pro-and-m4-max/)

19. [[Data Deduplication at Trillion Scale --- Zilliz, July 2025]{.underline}](https://zilliz.com/blog/data-deduplication-at-trillion-scale-solve-the-biggest-bottleneck-of-llm-training)

20. [[Tracking Correction Provenance in Digital Humanities Pipelines --- arXiv 2603.00884, March 2026]{.underline}](https://arxiv.org/html/2603.00884v1)

21. [[LLM API Pricing Comparison 2025 --- IntuitionLabs]{.underline}](https://intuitionlabs.ai/articles/llm-api-pricing-comparison-2025)

22. [[High-Quality Transcripts with Open-Source Tools --- r/LocalLLaMA, October 2024]{.underline}](https://www.reddit.com/r/LocalLLaMA/comments/1g2vhy3/creating_very_highquality_transcripts_with/)

23. [[Information Extraction from Fiscal Documents --- arXiv 2511.10659, November 2025]{.underline}](https://arxiv.org/html/2511.10659v1)

24. [[LLMs for Structured Data Extraction from PDFs in 2026 --- Unstract]{.underline}](https://unstract.com/blog/comparing-approaches-for-using-llms-for-structured-data-extraction-from-pdfs/)

25. [[Best Open Source LLM January 2026 --- WhatLLM.org]{.underline}](https://whatllm.org/blog/best-open-source-models-january-2026)

---
title: "Extraction Research Report"
id: "extraction-research-report"
version: 1
created: 2026-04-25
last_validated: 2026-04-25
type: document
topic_type: reference
status: imported
source_file: "extraction-research-report.docx"
signed_by: "Devon, 2026-04-25, devin-992682c244cf444f91e0a516498afbfd"
---

**METICULOUS DATA EXTRACTION**

*The Evidence Base*

Schema Segmentation, PicoClaw, Accuracy Benchmarks, Production Use Cases & The Deterministic Architecture

Prepared for: **Ewan Bramley / Amplified Partners**

Date: **March 2026**

Classification: **Internal --- Data-Dense Reference Document**

**EXECUTIVE SUMMARY**

This document compiles primary-source research on LLM-based data extraction: what accuracy is actually achievable, what architectures work in production, and where the opportunity sits for Amplified Partners in the UK trade business sector.

**The honest picture:**

-   Naive LLM extraction plateaus at **85--95%** accuracy. That sounds decent until you realise it means 5--15 errors per 100 documents. For financial data, that\'s not good enough.

-   The real baseline is worse than anyone admits: when properly measured with domain-specific evals across 3,000 documents, one team found their actual accuracy was **67%**. LLM-as-a-Judge had rated them 4.2/5.

-   At enterprise scale (369 fields), every frontier model --- GPT-5, Claude Opus 4.5, Gemini 3 Pro --- produces **0% valid output**. Not 10%. Zero.

-   But hybrid architectures (LLM extraction + deterministic validation + confidence-based human escalation) consistently achieve **98--99%+**. Veryfi hits 99.56% on receipts. Extend/Brex turned off human review entirely.

-   The key: **schema segmentation** (keep extraction passes under \~10--15 fields), **field-type-specific validation**, and **deterministic post-processing** --- the \"deterministic sandwich\" pattern.

-   Deterministic business-rule software (Altman Z-Score, LTV:CAC, ToC scoring) is **not made obsolete by LLMs**. It is the essential decision layer. This is now called Neurosymbolic AI --- the recognised best practice for regulated, auditable systems.

-   Knowledge graphs (FalkorDB + Graphiti) solve the N/N+1 degradation problem: hierarchical summarisation loses **46% of information**; graph extraction loses **essentially none**.

**Key numbers that matter:**

  ----------------------------------------------------- ----------------------- ------------------------------
  **Metric**                                            **Value**               **Source**
  Overall pass rate (6 frontier models, ExtractBench)   4.6%                    arXiv:2602.12247
  369-field schema valid output rate                    0% (all 6 models)       arXiv:2602.12247
  Untuned system actual accuracy (3,000 docs)           67%                     LinkedIn/Satish V.
  After schema segmentation                             89%                     LinkedIn/Satish V.
  Hybrid IDP (LLM + rules + HITL)                       98--99%                 Multiple production
  Specialist AI + deterministic (Veryfi receipts)       99.56%                  Veryfi benchmarks
  SCOPE validation: errors fixed on first retry         92%                     arXiv:2510.08623
  Schema-first extraction info retention vs prose       +40%                    arXiv:2407.15021
  Summarisation info loss (Chain-of-Density)            46% lost                ACL CoKG 2025
  Knowledge graph extraction info loss                  \~0%                    ACL CoKG 2025
  LLM outputs at temperature=0 (1,000 runs)             80 unique completions   AI World / Thinking Machines
  ----------------------------------------------------- ----------------------- ------------------------------

**PART 1: THE ACCURACY PROBLEM**

**1.1 ExtractBench: The Most Rigorous Benchmark (February 2026)**

ExtractBench ([arXiv:2602.12247](https://arxiv.org/html/2602.12247)) from Contextual AI tested 6 frontier models across 35 PDFs, 2,076 pages, and 12,867 evaluatable fields in 5 domains. The results are sobering.

**Dataset characteristics:**

  ---------------------- ----------------- ------------------- ---------- -----------------------------------
  **Domain**             **Schema Keys**   **Nesting Depth**   **Docs**   **Primary Challenge**
  Sports Results         12                6                   5          Deep nesting, tabular hierarchies
  Credit Agreements      13                3                   10         Long docs (100--250 pages)
  Research Papers        16                5                   6          Long arrays (100+ citations)
  Professional Resumes   31                4                   7          Semi-structured layouts
  SEC 10-K/Qs            369               4                   7          Enterprise-scale schema breadth
  ---------------------- ----------------- ------------------- ---------- -----------------------------------

**Main results --- Prompt Mode (all 6 frontier models):**

  ------------------- ---------------- ---------------------- ------------------- ------------------ ----------------- --------------- -------------
  **Model**           **Valid JSON**   **Credit (13 keys)**   **Research (16)**   **Resumes (31)**   **Sports (12)**   **SEC (369)**   **Overall**
  Gemini 3 Flash      25/35            85.4%                  47.9%               20.7%              18.3%             0.0%            6.9%
  Gemini 3 Pro        21/35            84.6%                  5.2%                21.2%              13.3%             0.0%            5.5%
  GPT-5.2             21/35            80.8%                  6.2%                19.8%              13.3%             0.0%            5.2%
  GPT-5               13/35            86.9%                  0.0%                3.7%               3.3%              0.0%            4.0%
  Claude Sonnet 4.5   15/35            0.0%\*                 49.0%               21.2%              13.3%             0.0%            3.3%
  Claude Opus 4.5     12/35            0.0%\*                 16.7%               24.0%              13.3%             0.0%            2.5%
  AGGREGATE           107/210          56.3%                  20.8%               18.4%              12.5%             0.0%            4.6%
  ------------------- ---------------- ---------------------- ------------------- ------------------ ----------------- --------------- -------------

*\* Claude models hit 100-page PDF limit; Credit Agreements average 137 pages.*

**The counterintuitive finding:** Structured output APIs made things **worse**, not better. Overall validity dropped from 51% to 37%. GPT-5 credit agreement pass rate fell from 86.9% to 70.0% with structured output mode. On complex schemas (SEC 10-K/Qs, Resumes), structured output mode produced 0% validity across all models.

**1.2 Schema Size vs Accuracy Degradation**

The degradation curve is continuous but the drop-off is steep:

  ------------------------- --------------- ---------------------------------------------
  **Schema Keys**           **Pass Rate**   **Pattern**
  12--13 (Sports, Credit)   12.5--56.3%     Manageable
  16 (Research)             20.8%           Drops --- array explosion (309.5 avg items)
  31 (Resumes)              18.4%           Moderate degradation
  369 (SEC 10-K/Qs)         0%              Complete failure, all 6 frontier models
  ------------------------- --------------- ---------------------------------------------

**Output volume dominates over schema breadth.** Research Papers (16 keys) performed worse than Credit Agreements (13 keys) because array items explode output tokens: 25,366 gold tokens vs. 883. The paper\'s key insight: \"output token count is a better predictor of failure than schema key count alone.\"

**1.3 The \"8 Field Threshold\" --- Practitioner Heuristic**

The claim \"beyond 8 fields, LLMs start hallucinating\" comes from [Satish Venkatakrishnan on LinkedIn](https://www.linkedin.com/posts/satish1v_we-told-clients-our-document-extraction-was-activity-7416685315785969664-cM4g) (January 2026). This is a practitioner observation from production, not a controlled study. The number 8 is a rough heuristic --- the actual threshold depends on field complexity, array depth, and output volume. [Jerry Liu (LlamaIndex)](https://x.com/jerryjliu0/status/1946358807875244398) corroborates: \"Try to limit schema nesting to 3--4 levels. Make fields optional.\"

The research literature shows no cliff at 8 --- but the practical advice is sound: **segment schemas at 10--15 fields per pass, and watch array complexity more than field count.**

**1.4 Field-Level vs Aggregate Accuracy: Aggregate Lies**

This is the most dangerous trap in extraction benchmarking. [Cleanlab\'s analysis](https://cleanlab.ai/blog/structured-output-benchmark/) (December 2025) shows the gap:

  ------------------ -------------------- ------------------------------------------ ---------
  **Model**          **Field Accuracy**   **Output Accuracy (all fields correct)**   **Gap**
  Gemini 3 Pro       0.964                0.77                                       --0.194
  GPT-5              0.956                0.76                                       --0.196
  Gemini 2.5 Pro     0.944                0.72                                       --0.224
  GPT-4.1-mini       0.863                0.45                                       --0.413
  Gemini 2.5 Flash   0.829                0.28                                       --0.549
  ------------------ -------------------- ------------------------------------------ ---------

**A 96% field accuracy on a 20-field document means only 81% of documents are fully correct** (0.96\^20 = 0.818). For a business processing 1,000 invoices/day, that\'s 190 documents with at least one error. Aggregate accuracy is a vanity metric.

**PART 2: WHAT PEOPLE ARE ACTUALLY ACHIEVING**

**2.1 Production Accuracy Table**

  --------------------------- ----------------------------- ------------------------- ----------------------------------- -----------------------
  **Company/System**          **Doc Type**                  **Accuracy**              **Method**                          **Source**
  Veryfi                      Receipts                      99.56%                    Deterministic + in-house AI         Veryfi benchmarks
  Extend (HomeLight)          Real estate docs              98--99%                   LLM + HITL (review turned off)      Extend case study
  Extend (Brex)               Financial docs                99%+                      Fine-tuned LLM + private GPU        Extend case study
  Ramp                        Receipts/invoices             99% OCR line items        OCR + fine-tuned LLM + Jsonformer   Modal case study
  Rossum (Deliveroo)          Invoices (11 countries)       97.6%                     AI extraction + validation          Rossum case study
  Rossum (Adyen)              Invoices (23 countries)       93.4%                     AI extraction + validation          Rossum case study
  Docsumo (Arbor Realty)      Insurance/Acord forms         99%+                      IDP + rule validation               Docsumo blog
  GPT on text PDFs            Invoices                      98%                       Direct LLM                          Koncile Feb 2026
  Claude on text PDFs         Invoices                      97%                       Direct LLM                          Koncile Feb 2026
  Gemini on text PDFs         Invoices                      96%                       Direct LLM                          Koncile Feb 2026
  Gemini on scanned           Invoices                      94%                       Integrated vision                   Koncile Feb 2026
  GPT + ext. OCR on scanned   Invoices                      91%                       OCR + LLM                           Koncile Feb 2026
  Roboyo                      Property docs (100+ fields)   99%, 85% STP              UiPath + Azure OpenAI + HITL        Roboyo case study
  D3V Technology              Compliance invoices           98% regulatory            Dual-LLM architecture               D3V blog
  Sirion                      Contract clauses              94.2% F1                  Hybrid SLM + LLM                    Sirion benchmark 2026
  Adeptia (loan provider)     Loan applications             99%+                      HITL + rules + AI                   Adeptia blog
  UK Gov MHCLG                Planning documents            100% text, 94% dates      LLM + VLM + OpenCV                  MHCLG Digital blog
  Anterior (via Reducto)      Clinical/medical              99%+ precision            Agentic OCR                         Reducto blog
  LLM framework (research)    Financial PDFs                99.5% on key indicators   LLM + domain prompting              Excited Engineer
  GPT-4 Turbo (baseline)      FinanceBench (SEC)            \~19%                     Out-of-box with retrieval           Intuition Labs
  Untuned LLM system          Mixed docs (3,000)            67%                       LLM + LLM-as-Judge                  LinkedIn/Satish V.
  Same system after rebuild   Same corpus                   89%                       Schema segmentation                 LinkedIn/Satish V.
  --------------------------- ----------------------------- ------------------------- ----------------------------------- -----------------------

**2.2 The Uncomfortable Baseline**

From [Satish Venkatakrishnan\'s LinkedIn post](https://www.linkedin.com/posts/satish1v_we-told-clients-our-document-extraction-was-activity-7416685315785969664-cM4g): \"We told clients our document extraction was \'highly accurate.\' LLM-as-a-Judge scored us 4.2/5. Human reviewers gave thumbs up. Then we built domain-specific evaluations. **Actual accuracy: 67%.**\"

Breakdown: scanned documents **58%**, entity matching **71%**, date formats across countries: silent failures. The patterns only emerged across 3,000 documents --- a 50-document sample showed nothing wrong. This is the sampling problem that kills SMB deployments.

**2.3 Nanonets IDP Leaderboard (March 2026)**

16 models tested on 9,000+ real documents ([Nanonets IDP Leaderboard](https://nanonets.com/blog/idp-leaderboard-1-5/)):

  ---------------- ------------------- ------------------ ----------------- -----------------------------
  **Model**        **Overall Score**   **Dense Tables**   **Handwriting**   **Notes**
  Gemini 3.1 Pro   81.0                96%+               75.5%             Leads VQA, best for scanned
  GPT-5.4          83.2                96%+               ---               Tables jumped 73%→95%
  Sonnet 4.6       80.8                ---                ---               Equals Claude 4.6
  Claude 4.6       80.3                ---                ---               Best for formulas
  GPT-4.1          70.0                73.1%              ---               Significant gap vs GPT-5.4
  ---------------- ------------------- ------------------ ----------------- -----------------------------

**Sparse tables** (scattered cells, no gridlines): most models below 55%. **Handwriting**: best models below 76%. Digital printed text: frontier models hit 98%+.

**PART 3: THE 89% TO 99% BRIDGE**

Getting to 90% is easy. Getting past 95% is engineering. Getting to 99% is a system, not a model.

**3.1 Schema Segmentation (Under 8 Fields Per Pass)**

Keep extraction passes under 10--15 fields. If expected array items exceed 20, split further. Target under 1,000 output tokens per pass (the Credit Agreements sweet spot was 883 tokens with 56.3% pass rate --- the best in ExtractBench). Source: [ExtractBench](https://arxiv.org/html/2602.12247).

The research supports continuous segmentation strategy:

  --------------------- ------------ -------------------------- -------------------------------------------
  **Complexity Zone**   **Fields**   **Expected Array Items**   **Strategy**
  Safe zone             \<15         \<20                       Single-pass extraction OK
  Caution zone          15--50       20--100                    Segment by field type
  High risk             50--100      100+                       Mandatory segmentation
  Failure zone          100+         Any                        Near-total failure --- split aggressively
  --------------------- ------------ -------------------------- -------------------------------------------

**3.2 Field-Type-Specific Validation**

Not all fields deserve the same grader. From [ExtractBench\'s metric library](https://arxiv.org/html/2602.12247):

  ----------------------- --------------------------------- --------------------------------------
  **Validation Preset**   **Metric**                        **Use Case**
  string\_exact           Exact match                       IDs, codes (CUSIP, CIK, VAT numbers)
  string\_fuzzy           Levenshtein (threshold 0.8)       Typo-tolerant names
  string\_semantic        LLM equivalence (threshold 0.7)   Free-text descriptions
  number\_exact           Exact numeric match               Integer counts
  number\_tolerance       Within 0.1% margin                Monetary amounts, percentages
  boolean\_exact          Exact boolean match               Binary flags
  array\_llm              Semantic alignment + F1           Arrays of objects (line items)
  ----------------------- --------------------------------- --------------------------------------

**3.3 Deterministic Validation Layers**

The single most reliable accuracy booster. Practical rules for financial data:

-   **Regex:** Date format validation (YYYY-MM-DD, UK DD/MM/YYYY), VAT number format (GB + 9 digits), company number patterns

-   **Range checks:** Invoice amounts within historical range for vendor (flag outliers \> 3σ)

-   **Cross-reference:** Extracted total = sum of line items ± tax. Net + VAT = gross

-   **Grounding check:** Extracted value exists verbatim in source text

-   **Deduplication:** Same invoice number + same vendor = flag

-   **Tolerance windows:** ±0.01 for rounding on monetary values

**3.4 Confidence-Based Human Escalation**

From [LlamaIndex\'s confidence threshold guide](https://www.llamaindex.ai/glossary/what-is-confidence-threshold):

  ------------------------------- --------------------- -------------- ---------------------------
  **Threshold**                   **Automation Rate**   **Accuracy**   **Best Use Case**
  0.95--1.0 (Very Conservative)   40--60%               98--99%        Critical financial, legal
  0.85--0.94 (Conservative)       65--80%               95--97%        Standard business docs
  0.70--0.84 (Balanced)           80--90%               90--94%        General processing
  0.60--0.69 (Aggressive)         90--95%               85--89%        High-volume, low-risk
  ------------------------------- --------------------- -------------- ---------------------------

**Field-level thresholds, not global.** Invoice numbers need 0.95+; vendor names tolerate 0.80. A single global threshold is a common production mistake.

**3.5 Dual-LLM / Ensemble Approaches**

**Unstract LLM Challenge:** Two LLMs run the same extraction. Output only accepted if both agree. Use different vendors (GPT as extractor, Claude as challenger). Source: [Unstract webinar](https://unstract.com/webinar-recording/how-to-achieve-99-accuracy-in-llm-driven-unstructured-data-etl/).

**Retab k-LLMs:** Run same prompt k times, field-by-field majority vote. Result: +4--6 percentage points on semi-structured documents. \"Shadow voting\" (1 premium + cheaper models) retains most gains at \~40% cost. Palantir uses an equivalent LLM Multiplexer. Source: [Retab / r/LocalLLaMA](https://www.reddit.com/r/LocalLLaMA/comments/1mq2vjt/how_we_chased_accuracy_in_doc_extraction_and/).

**3.6 The SCOPE Framework (92% of Errors Corrected on First Retry)**

From the [PARSE paper (EMNLP 2025)](https://arxiv.org/html/2510.08623v1), the SCOPE 3-stage validation:

-   **Missing Attribute Check:** All required schema fields present?

-   **Grounding Verification:** Can extracted values be found in source document text?

-   **Rule Compliance Check:** Do values adhere to schema constraints?

When validation fails, SCOPE generates structured reflections guiding re-extraction. **92% of extraction errors are corrected in the first retry.** Results:

  --------------------------------- -------------- ---------------- ----------
  **Model**                         **Baseline**   **With SCOPE**   **Gain**
  Claude 3.7 Sonnet (SWDE)          24.5%          89.2%            +64.7pp
  Claude 3.5 Sonnet V2 (SWDE)       25.7%          90.8%            +65.1pp
  DeepSeek-R1 (SWDE)                19.3%          82.7%            +63.4pp
  Claude 3.7 Sonnet (Retail-Conv)   75%            88.6%            +13.6pp
  --------------------------------- -------------- ---------------- ----------

**3.7 Few-Shot Examples and Domain-Specific Prompting**

[Parcha](https://blog.parcha.ai/99-accuracy/) achieved **92% → 99%** accuracy using RAG with few-shot examples loaded dynamically. Maintain 3--10 gold-standard extraction examples per document type; select by embedding similarity; include difficult edge cases. Prompting strategy is more impactful than model size ([LLMStructBench](https://arxiv.org/html/2602.14743v1)).

**PART 4: PICOCLAW --- THE EDGE ARCHITECTURE**

**4.1 Full Architecture (Small Brain / Big Brain)**

PicoClaw ([GitHub](https://github.com/sipeed/picoclaw)) is a Go-based AI agent framework: single 14MB binary, \<10MB RAM, \<1s startup. Launched February 9, 2026 by Sipeed. 15,600 GitHub stars, 54 contributors. Written in Go (98.7%), 95% AI-bootstrapped.

The \"Small Brain / Big Brain\" architecture ([LinkedIn analysis](https://www.linkedin.com/posts/aliahmad11403_ai-picoclaw-openclaw-activity-7432390684667678720-WgqX)):

-   **Small Brain (PicoClaw, local):** Classification, routing, cron scheduling, memory management, workspace sandboxing, heartbeat monitoring, channel management. Runs on \$10 hardware.

-   **Big Brain (Cloud LLM or local Ollama):** Complex reasoning, extraction, multi-hop analysis. PicoClaw delegates via API call.

**4.2 Resource Comparison Table**

  ----------------------- ------------------------ ----------------------- ---------------
  **Metric**              **OpenClaw**             **PicoClaw**            **Delta**
  Language                TypeScript (Node.js)     Go                      ---
  RAM (minimum)           \>1 GB                   \<10 MB                 99% reduction
  RAM (recommended)       8--16 GB                 10--20 MB               ---
  Startup (0.8GHz core)   \>500 seconds            \<1 second              400× faster
  Binary/install size     487 MB (node\_modules)   14 MB (single binary)   97% smaller
  Install time            2 min 14 sec             3 seconds               45× faster
  Min hardware cost       \$599 (Mac Mini M4)      \$10 (RISC-V board)     98% cheaper
  Cloud hosting cost      \$15--18/month           \$3--4/month            75% cheaper
  ----------------------- ------------------------ ----------------------- ---------------

Source: [Dev.to Decision Guide](https://dev.to/shehzan/openclaw-vs-picoclaw-edge-ai-decision-guide-2026-31pg) and [GitHub README](https://github.com/sipeed/picoclaw/blob/main/README.md).

**4.3 Measured Memory Benchmarks**

  ----------------------- ---------------------------- ---------------------
  **Workload**            **OpenClaw (Mac Mini M4)**   **PicoClaw (Pi 4)**
  Idle                    1,800 MB                     8 MB
  Single request          2,100 MB                     12 MB
  5 concurrent requests   2,900 MB                     45 MB
  ----------------------- ---------------------------- ---------------------

**4.4 Real-World Deployments**

-   **Industrial IoT:** 50+ factory floor sensors, each running PicoClaw on ARM SBCs. Local analysis; anomalies reported to cloud OpenClaw. ([Dev.to](https://dev.to/shehzan/openclaw-vs-picoclaw-edge-ai-decision-guide-2026-31pg))

-   **Smart Agriculture:** 50 soil sensors on \$10 RISC-V boards. \$500 hardware + \$18/month cloud + \$20/month LLM APIs.

-   **8-hour WiFi outage test:** Pi Zero 2W continued all local tasks, queued cloud tasks, sent summary on reconnect. ([Awesome Agents](https://awesomeagents.ai/reviews/review-picoclaw/))

-   **Oracle Cloud Always-Free:** Documented: run on 1GB RAM VM, secured with Tailscale, zero public ports.

-   **Hetzner ARM VPS:** €3.79/month production deployment. ([Dev.to VPS guide](https://dev.to/cucoleadan/how-to-install-and-configure-picoclaw-on-the-cheapest-vps-1l73))

**4.5 Ollama Integration (Air-Gapped Mode)**

PicoClaw is provider-agnostic. Ollama supported via OpenAI-compatible API. From [DataCamp](https://www.datacamp.com/tutorial/picoclaw-tutorial): \"PicoClaw can run without internet access\... important for sensitive data in regulated industries such as banking and healthcare.\"

**4.6 Hardware Benchmarks**

  ----------------------------- ------------------- ----------------------- --------------------
  **Hardware**                  **Model**           **Inference Latency**   **Power (Active)**
  Pi Zero 2W (512MB, \$10)      Cloud API           1--2s                   1.2W
  Pi Zero 2W                    Quantized 1.5B      2--4s                   1.2W
  Pi 5 (4GB, \$60)              7B via llama.cpp    800ms avg               ---
  Beelink N100 (8GB, \~\$120)   7B q4 (estimated)   \~400--600ms            6W TDP
  ----------------------------- ------------------- ----------------------- --------------------

Source: [Awesome Agents 2-week review](https://awesomeagents.ai/reviews/review-picoclaw/).

**4.7 Security Model (Honest Assessment)**

PicoClaw is secure-first by design. Workspace sandboxing restricts all file/shell access to \~/.picoclaw/workspace. Blocked commands: rm -rf, format, shutdown, fork bombs, etc. Channel access control via allow\_from user IDs. Gateway binds to 127.0.0.1 by default.

**Known issues** ([Security Audit \#258](https://github.com/sipeed/picoclaw/issues/258)): Critical vulnerabilities found in February 2026 --- RCE via shell denylist bypass, SSRF, path traversal via symlink. [PR \#331](https://github.com/sipeed/picoclaw/issues/331) addresses 6 of these (637 lines, 18 dangerous patterns blocked). Status: open, not yet merged. OAuth tokens stored in plaintext (HIGH). For internal-network/air-gapped deployment (Ewan\'s use case), risk profile is significantly lower.

**4.8 Skill Format Compatibility**

SKILL.md format: mostly compatible with OpenClaw. [Awesome Agents](https://awesomeagents.ai/reviews/review-picoclaw/) tested 15 OpenClaw skills: **11/15 ran correctly on first try (73%)**. 4 failures due to Node.js-specific features, heavy npm dependencies, or \>1GB RAM assumptions. Simple skills (API calls, text processing) work without modification. The picoclaw migrate command copies the entire workspace 1:1.

**PART 5: PRODUCTION USE CASES**

**5.1 Ramp --- 5M Receipts/Month**

Scale: 5 million receipts/month, 400,000 invoices/month, saves 30,000 hours monthly. Architecture: Azure Document Intelligence OCR → fine-tuned open-source LLM (via Modal) → Jsonformer safety wrapper → business rules GL validation → human escalation. Result: 34% reduction in manual intervention. Agent Fill (2025): Gemini 2.5 Pro for initial extraction, Claude Sonnet 4 for schema mapping, computer use for form filling. Sources: [Modal case study](https://modal.com/blog/ramp-case-study), [Microsoft Azure case study](https://www.microsoft.com/en/customers/story/23693-ramp-azure-ai-services).

**5.2 Extend / Brex --- 99%+ Accuracy, Manual Review Turned Off**

Brex: 30,000+ business customers, millions of documents. 99%+ accuracy across messy real-world documents. HomeLight: started at \~85% (raw OpenAI API), reached 98--99%, manual review turned off after 1 month with 0 corrections. Architecture: OCR + VLM preprocessing → LLM extraction → Pydantic validation → business validation (math checks) → confidence scoring → HITL queue. Composer agent auto-optimises extraction logic. Sources: [HomeLight case study](https://www.extend.ai/resources/homelight-hits-99-accuracy-and-eliminates-manual-review-with-extend), [Brex case study](https://www.extend.ai/resources/how-brex-reached-99-accuracy-across-millions-of-financial-documents).

**5.3 Reducto --- Agentic OCR**

Multi-pass Agentic OCR combining CV models, multiple VLMs, and a proprietary framework that detects/corrects parsing errors by mimicking human review. Anterior (healthcare): 99%+ precision on clinical document extraction. Claims 20% better than AWS/Google/Azure APIs. SOC 2 Type II, HIPAA with BAA. Sources: [Reducto vs Google Document AI](https://llms.reducto.ai/reducto-vs-google-document-ai).

**5.4 Unstract --- Open-Source Challenger**

Open-source platform. LLMWhisperer for layout-preserving text extraction. Prompt Studio for field-level prompt engineering. LLM Challenger (dual-LLM consensus). PDF Splitter API for semantic document splitting. Self-hostable. Sources: [Unstract blog](https://unstract.com/blog/comparing-approaches-for-using-llms-for-structured-data-extraction-from-pdfs/).

**5.5 Docugami --- XML Knowledge Graph Target**

Every document converted into a full XML Knowledge Graph capturing hierarchical relationships. Core differentiator: graph persists, so new queries across entire corpus answered instantly without re-extraction. National CRE company: 80% reduction in lease data extraction time. Just Food for Dogs: 50% time reduction, capacity tripled. Source: [Docugami case studies](https://www.docugami.com/case-studies).

**5.6 UK Government MHCLG \"Extract\"**

AI tool combining LLMs (structured outputs for text), VLMs + OpenCV + SAM (image segmentation for map boundaries). Results: 100% text field extraction, 94% date accuracy, 90% polygon boundary accuracy. Launched at London Tech Week by PM Starmer, rolling out to English councils in 2026. Source: [MHCLG Digital blog](https://mhclgdigital.blog.gov.uk/2025/06/12/extract-using-ai-to-unlock-historic-planning-data/).

**5.7 Xero --- Receipt Extraction for MTD**

February 2026: Xero embedded LLM technology for UK customers. Receipt snap → LLM extraction in under 20 seconds → pre-populated records → auto bank matching. Launched ahead of HMRC Making Tax Digital for Income Tax (April 2026). Source: [Xero press release](https://www.xero.com/media-releases/xero-to-bring-ai-powered-data-capture-and-extraction-into-platform/).

**5.8 Dext --- Tens of Millions of Documents**

AI-powered OCR extracts merchant name, date, amount, currency, line items, tax. Rule engine applies known accounting rules. Two-way sync with Xero, QuickBooks, Sage. Bank statement extraction: 75% completed in under 4 hours, 700+ banks. Scale: tens of millions of documents/month. Source: [Dext bank statement extraction](https://dext.com/us/business/products/bank-statements-extraction).

**5.9 ServiceTitan --- Trade Businesses**

Target: HVAC, plumbing, electrical contractors. Titan Intelligence: automated invoicing from service calls, AI call routing/scheduling, revenue insights, predictive pricing. 72% of contractors say AI is already relevant. Data advantage: trade-specific training data from thousands of contractors. Source: [ServiceTitan Titan Intelligence](https://www.servicetitan.com/features/titan-intelligence).

**5.10 Open-Source Tools**

  ---------------- ---------------------------------------- ------------------------------------------ -------------------------------
  **Tool**         **What It Does**                         **Key Differentiator**                     **Source**
  Instructor       Structured LLM extraction (Pydantic)     3M+ downloads, 15+ providers, auto-retry   python.useinstructor.com
  Outlines         Constrained generation during decoding   98% schema adherence, 5× faster            github.com/dottxt-ai/outlines
  ExtractThinker   On-premise extraction pipeline           Ollama + Docling + privacy-first           Towards AI
  Graphiti (Zep)   Temporal knowledge graph                 Bi-temporal tracking, sub-second queries   github.com/getzep/graphiti
  ---------------- ---------------------------------------- ------------------------------------------ -------------------------------

**PART 6: THE DETERMINISTIC ARCHITECTURE ISN\'T DEAD**

**6.1 Neurosymbolic AI / Hybrid Intelligence Pattern**

The architecture has a name: **Neurosymbolic AI**. LLMs handle ambiguity; deterministic code enforces invariants. This is the recognised best practice for regulated, auditable systems. As [Shilov on DEV Community](https://dev.to/uxter/stop-using-llms-for-everything-the-power-of-hybrid-architectures-45ee) states: \"Anything that would cause legal, safety, or data-integrity issues must be enforced in deterministic code, not in prompt engineering or \'smarter\' models.\"

**6.2 VeNRA Paper: LLMs Have \"Inherent Arithmetic Incompetence\"**

The [VeNRA paper (arXiv, March 2026)](https://arxiv.org/html/2603.04663v2) is direct: \"Standard RAG architectures fail in high-stakes financial domains due to the inherent arithmetic incompetence of LLMs and the distributional semantic conflation of dense vector retrieval.\" LLMs \"simulate the syntax of calculation without preserving mathematical invariants.\" VeNRA\'s solution: LLMs extract into a strictly typed Universal Fact Ledger → deterministic Python performs all arithmetic. Hallucination rate drops from 4.1% to 1.2%.

**6.3 80 Unique Outputs from 1,000 Identical Prompts at Temperature=0**

[Thinking Machines Lab research](https://aiworld.eu/story/why-llms-cant-give-the-same-answer-twice) found that even with temperature=0 and identical seeds, the same prompt produced **80 unique completions out of 1,000 runs**. Cause: floating-point non-associativity in GPU arithmetic --- (a + b) + c ≠ a + (b + c). For a business scoring system, the Altman Z-Score for a given company MUST be the same every time. Deterministic code achieves this trivially; LLMs do not.

**6.4 Where Deterministic Code MUST Be Used**

  ------------------------------------------------ ------------------------------------------- ----------------------------------------------------------------------
  **Domain**                                       **Why Deterministic is Required**           **LLM Failure Mode**
  Financial calculations (Z-Score, LTV:CAC, CCC)   Must be exact, reproducible, auditable      Simulates syntax of calculation without mathematical invariants
  Compliance rule enforcement                      Regulatory traceability required            Cannot provide audit trail (statistical distribution, not algorithm)
  Threshold triggers (distress zones)              Binary correctness required                 Z=1.82 when correct is 1.79 = wrong compliance determination
  Data validation / range checking                 Schema enforcement                          Produces plausible but inconsistent formats
  Math cross-references (totals = sum of items)    Provably correct                            Frequently misreads/miscalculates numerics
  Audit trails                                     Every decision traced to inputs + formula   \"Reasoning\" is token probability, not traceable algorithm
  ------------------------------------------------ ------------------------------------------- ----------------------------------------------------------------------

**6.5 The Deterministic Sandwich Pattern**

The recognised production architecture:

-   **1. Deterministic pre-processing:** Input normalisation, format validation, regex extraction of known structures

-   **2. LLM extraction:** Schema-constrained semantic understanding of ambiguous content

-   **3. Deterministic validation:** Missing field check, format validation, math cross-reference, grounding check

-   **4. Confidence routing:** Pass → auto-process; Fail → re-extract or human review

This pattern is called Neurosymbolic AI ([Capgemini](https://www.capgemini.com/insights/expert-perspectives/the-evolution-of-hybrid-aiwhere-deterministic-and-probabilistic-approaches-meet/)), Hybrid Intelligence ([New Math Data](https://blog.newmathdata.com/hybrid-intelligence-marrying-deterministic-code-with-llms-for-robust-software-development-b92bf949257c)), Deterministic AI ([Zapier](https://zapier.com/blog/deterministic-ai/)), or Graph-First Reasoning ([Rainbird Technologies](https://rainbird.ai/wp-content/uploads/2025/03/Deterministic-Graph-Based-Inference-for-Guardrailing-Large-Language-Models.pdf)).

**6.6 Why Altman Z-Score, Goldratt ToC, LTV:CAC MUST Be Deterministic**

Z = 1.2X₁ + 1.4X₂ + 3.3X₃ + 0.6X₄ + 1.0X₅ --- requires exact arithmetic on five specific ratios with specific weightings. An LLM may produce plausible-looking results that are arithmetically wrong, and critically provides **no reliable signal about when it is wrong**. The [arXiv paper on LLM math reasoning failures](https://arxiv.org/abs/2502.11574) found all 8 SOTA models \"exhibit errors in arithmetic, sometimes producing correct answers through flawed logic.\"

The correct architecture: LLMs extract inputs (working\_capital, total\_assets, retained\_earnings\...) into typed fields → deterministic Python applies the formula → LLM generates natural-language explanation. **AI extracts; deterministic software decides.**

**PART 7: N/N+1 DEGRADATION AND WHY GRAPHS WIN**

**7.1 The Vernekar Analysis**

[Aditya Vernekar (LinkedIn, December 2025)](https://www.linkedin.com/posts/aditya-vernekar711_the-nn1-summarization-degradation-problem-activity-7405524891707506688-KN4X) identified three compounding systemic errors in hierarchical LLM summarisation:

-   **Signal Attenuation:** Essential, low-frequency data points (specific error codes, root causes) filtered out during sequential compression

-   **Semantic Drift:** Probabilistic interpretation noise amplified across layers --- exaggerated sentiment, conceptual misrepresentation

-   **Hallucination Anchoring:** Micro-hallucinations in Layer N treated as ground truth in Layer N+1 --- confident but factually incorrect final output

Key conclusion: \"The resulting output is a compression of the model\'s intermediate interpretations, **statistically decoupled from the raw source data**.\" And: \"Addressing this is **not a prompt engineering task**. It necessitates a shift to state-preserving architectures.\"

**7.2 CoKG Paper: Summarisation Loses 46%, Graph Extraction Loses \~0%**

The [Chain-of-Knowledge-Graph paper (ACL 2025)](https://aclanthology.org/2025.neusymbridge-1.1.pdf) directly measured information loss:

  ---------------------------------- ------------- ------------- ------------- ----------------------
  **Method**                         **ROUGE-1**   **ROUGE-2**   **ROUGE-L**   **Information Loss**
  Base (full text)                   0.417         0.114         0.189         ---
  Chain-of-Density (summarisation)   0.226         0.055         0.123         46% lost
  Chain-of-Entities                  0.360         0.099         0.178         14% lost
  Chain-of-Knowledge-Graph           0.418         0.114         0.189         \~0% lost
  ---------------------------------- ------------- ------------- ------------- ----------------------

**The most common summarisation approach (Chain-of-Density) loses 46% of information. Knowledge graph extraction preserves essentially all of it.**

**7.3 Schema-First Extraction vs Prose Summarisation**

The [Structured Knowledge Representations paper (arXiv, 2024)](https://arxiv.org/html/2407.15021v1) directly compared JSON-schema extraction against prose summarisation:

-   JSON representations improve summarisation F1 by **+40%** on the SUMIE dataset (79.4% vs 62.2%)

-   +14% improvement on BookScore, +7--8% from Chain-of-Key updates

\"JSON organises information into distinct, easily accessible segments, facilitating efficient updates and retrievals\... avoids verbosity and retains critical content across all sections, unlike plain text which leads to redundancy, inaccuracies, or information overload.\"

**7.4 Why FalkorDB + Graphiti is the Correct Architecture**

  ----------------------- --------------------------------------------- -------------------------------------------------------
  **Aspect**              **Hierarchical Summarisation**                **Knowledge Graph (Graphiti)**
  Process                 Info → prose chunk → LLM compress → summary   Info → entity extraction → discrete typed nodes/edges
  Each layer              Discards detail                               No compression needed
  Contradictions          Blended into narrative                        Resolved by temporal edge invalidation
  Retrieval               Semantic similarity on compressed text        Graph traversal on structured relationships
  Rare facts              Lost to statistical underweighting            Stored as explicit node/edge
  Point-in-time queries   Cannot query historical state                 Bi-temporal tracking enables it
  ----------------------- --------------------------------------------- -------------------------------------------------------

FalkorDB: open-source graph database, 200× faster than comparable graph databases, purpose-built for LLM applications. Graphiti: incremental episode ingestion --- each new datum retains its identity rather than being dissolved into a summary. Temporal edges record when facts were valid. Source: [Graphiti GitHub](https://github.com/getzep/graphiti), [FalkorDB GraphRAG explainer](https://falkordb.com/blog/what-is-graphrag/).

**7.5 Temporal Edges as the Solution to Contradiction**

When a fact changes (\"Company X is in Grey Zone\" → \"Company X enters Distress Zone\"), Graphiti does not re-summarise and blend states. It **invalidates the old edge** with an end timestamp and creates a new edge. Historical state preserved; current state unambiguous. This is why the pattern works for business intelligence that tracks financial health over time. Source: [Presidio blog on Graphiti](https://www.presidio.com/technical-blog/graphiti-giving-ai-a-real-memory-a-story-of-temporal-knowledge-graphs/).

**PART 8: THE TRADE BUSINESS GAP**

**8.1 Seven Document Types Nobody Systematically Extracts**

Jobber and Housecall Pro handle **operational** data well --- scheduling, dispatching, invoicing. But field-captured unstructured documents are NOT systematically extracted. This is the gap:

  -------------------------------------- ------------------------------------------- ---------------------------------------------------
  **Document Type**                      **Current State**                           **Extraction Opportunity**
  Supplier invoices (parts, materials)   Manual data entry into Xero/QB              Automated extraction → GL coding
  Job sheets / work orders               Paper or PDF, not systematically captured   Extract labour hours, materials, job codes
  Gas Safe / compliance certificates     PDF scan filed and forgotten                Extract cert numbers, dates, asset IDs
  Subcontractor invoices                 Manual reconciliation                       Auto-match to job codes, flag VAT issues
  Warranty documents                     Unstructured PDFs                           Extract product IDs, expiry dates, T&Cs
  Site photos + job notes                Unstructured                                Extract damage descriptions for insurance/billing
  CSCS / accreditation cards             Photo                                       Extract worker ID, qualification type, expiry
  -------------------------------------- ------------------------------------------- ---------------------------------------------------

**8.2 Why This is the Amplified Partners Opportunity**

ServiceTitan has trade-specific AI but focuses on operational workflows --- scheduling, invoicing from service calls, call routing. The **unstructured field document** layer is untouched. These are the documents that sit in shoeboxes, email inboxes, and WhatsApp threads. They contain compliance data that matters (Gas Safe cert expiry), financial data that matters (subcontractor VAT), and operational data nobody is capturing (actual labour hours from job sheets vs quoted).

The 72% of UK contractors who say AI is relevant to their business ([ServiceTitan 2026 report](https://www.servicetitan.com/blog/ai-in-the-trades-report-takeaways)) are waiting for someone to solve this problem --- not another scheduling tool.

**8.3 How the Architecture Maps to This Gap**

The complete pipeline:

-   **Capture:** Mobile photo / email / WhatsApp → PicoClaw on Beelink N100 (edge ingestion, classification, pre-processing)

-   **Parse:** Reducto / LLMWhisperer for layout-preserving text extraction

-   **Extract:** Schema-segmented LLM extraction (Instructor / Extend) --- \<15 fields per pass, field-type-specific validation

-   **Validate:** Deterministic sandwich --- regex (cert formats, VAT numbers), range checks, math cross-references

-   **Score:** Deterministic business rules (compliance status, financial health, job profitability)

-   **Store:** FalkorDB + Graphiti knowledge graph --- temporal edges, point-in-time queries, no summarisation loss

-   **Integrate:** Xero/QuickBooks sync, Companies House enrichment for supplier verification

**FULL SOURCES**

*All sources verified and accessed March 2026.*

1\. **ExtractBench paper ---** <https://arxiv.org/html/2602.12247>

2\. **ExtractBench GitHub ---** <https://github.com/ContextualAI/extract-bench>

3\. **Let Me Speak Freely (EMNLP 2024) ---** <https://arxiv.org/html/2408.02442v1>

4\. **PARSE/ARCHITECT (EMNLP 2025) ---** <https://arxiv.org/html/2510.08623v1>

5\. **DeepJSONEval ---** <https://arxiv.org/html/2509.25922v1>

6\. **LLMStructBench ---** <https://arxiv.org/html/2602.14743v1>

7\. **MDER-DR entity-centric ---** <https://arxiv.org/html/2603.11223v1>

8\. **Entity Cards (Reddit r/LocalLLaMA) ---** <https://www.reddit.com/r/LocalLLaMA/comments/1qj42l0/>

9\. **8-field threshold (LinkedIn / Satish V.) ---** <https://www.linkedin.com/posts/satish1v_we-told-clients-our-document-extraction-was-activity-7416685315785969664-cM4g>

10\. **Cleanlab structured output benchmarks ---** <https://cleanlab.ai/blog/structured-output-benchmark/>

11\. **Pulse AI schema complexity ---** <https://www.runpulse.com/blog/computational-complexity-of-schema>

12\. **JSON Schema Conference (Outlines/.txt) ---** <https://conference.json-schema.org/sessions/json_schema_llms/>

13\. **AWS IDP evaluation framework ---** <https://github.com/aws-solutions-library-samples/accelerated-intelligent-document-processing-on-aws/blob/main/docs/evaluation.md>

14\. **Jerry Liu schema nesting advice ---** <https://x.com/jerryjliu0/status/1946358807875244398>

15\. **VeNRA paper (arXiv, March 2026) ---** <https://arxiv.org/html/2603.04663v2>

16\. **LLM mathematical reasoning failures ---** <https://arxiv.org/abs/2502.11574>

17\. **Thinking Machines Lab / LLM nondeterminism ---** <https://aiworld.eu/story/why-llms-cant-give-the-same-answer-twice>

18\. **Shilov hybrid architectures (DEV Community) ---** <https://dev.to/uxter/stop-using-llms-for-everything-the-power-of-hybrid-architectures-45ee>

19\. **Zapier deterministic AI ---** <https://zapier.com/blog/deterministic-ai/>

20\. **Capgemini hybrid AI evolution ---** <https://www.capgemini.com/insights/expert-perspectives/the-evolution-of-hybrid-aiwhere-deterministic-and-probabilistic-approaches-meet/>

21\. **Kognitos Neurosymbolic AI ---** <https://www.kognitos.com/blog/what-is-neurosymbolic-ai/>

22\. **Rainbird Technologies whitepaper ---** <https://rainbird.ai/wp-content/uploads/2025/03/Deterministic-Graph-Based-Inference-for-Guardrailing-Large-Language-Models.pdf>

23\. **New Math Data hybrid intelligence ---** <https://blog.newmathdata.com/hybrid-intelligence-marrying-deterministic-code-with-llms-for-robust-software-development-b92bf949257c>

24\. **Vernekar N/N+1 degradation (LinkedIn) ---** <https://www.linkedin.com/posts/aditya-vernekar711_the-nn1-summarization-degradation-problem-activity-7405524891707506688-KN4X>

25\. **CoKG paper (ACL 2025) ---** <https://aclanthology.org/2025.neusymbridge-1.1.pdf>

26\. **Structured Knowledge Representations ---** <https://arxiv.org/html/2407.15021v1>

27\. **Veryfi line-item benchmarks ---** <https://www.veryfi.com/technology/line-item-extraction-accuracy-benchmarks/>

28\. **Koncile: LLM invoice extraction comparison ---** <https://www.koncile.ai/en/ressources/claude-gpt-or-gemini-which-is-the-best-llm-for-invoice-extraction>

29\. **Vellum AI: LLMs vs OCRs ---** <https://www.vellum.ai/blog/document-data-extraction-llms-vs-ocrs>

30\. **LlamaExtractor paper ---** <https://arxiv.org/html/2510.15727v1>

31\. **Fiscal document extraction paper ---** <https://arxiv.org/html/2511.10659v2>

32\. **Fin-RATE financial analytics benchmark ---** <https://arxiv.org/html/2602.07294v1>

33\. **Nanonets IDP Leaderboard ---** <https://nanonets.com/blog/idp-leaderboard-1-5/>

34\. **Unstructured.io document parsing benchmark ---** <https://unstructured.io/blog/benchmarking-document-parsing-and-what-actually-matters>

35\. **Athenic enterprise LLM comparison ---** <https://getathenic.com/blog/claude-vs-gpt4o-vs-gemini-enterprise-comparison>

36\. **Rossum / Deliveroo case study ---** <https://rossum.ai/customer-stories/deliveroo/>

37\. **Rossum / Adyen case study ---** <https://rossum.ai/customer-stories/adyen/>

38\. **Docsumo OCR accuracy analysis ---** <https://www.docsumo.com/blogs/ocr/accuracy>

39\. **Roboyo property document case study ---** <https://roboyo.global/case-study/ai-powered-property-document-extraction-achieving-99-accuracy-and-85-straight-through-processing/>

40\. **D3V Dual-LLM architecture ---** <https://www.d3vtech.com/insights/revolutionizing-invoice-detection-with-dual-llm-architecture/>

41\. **Retab k-LLMs (r/LocalLLaMA) ---** <https://www.reddit.com/r/LocalLLaMA/comments/1mq2vjt/how_we_chased_accuracy_in_doc_extraction_and/>

42\. **Parcha: 99% accuracy ---** <https://blog.parcha.ai/99-accuracy/>

43\. **Adeptia: Getting to 99% ---** <https://www.adeptia.com/blog/getting-to-99percent-data-accuracy>

44\. **LlamaIndex confidence thresholds ---** <https://www.llamaindex.ai/glossary/what-is-confidence-threshold>

45\. **Unstract: 99% accuracy webinar ---** <https://unstract.com/webinar-recording/how-to-achieve-99-accuracy-in-llm-driven-unstructured-data-etl/>

46\. **Sirion clause extraction benchmark ---** <https://www.sirion.ai/library/contract-insights/clause-extraction-benchmark-sirion-vs-llms/>

47\. **MHCLG Digital blog (UK Gov Extract) ---** <https://mhclgdigital.blog.gov.uk/2025/06/12/extract-using-ai-to-unlock-historic-planning-data/>

48\. **Xero AI data capture announcement ---** <https://www.xero.com/media-releases/xero-to-bring-ai-powered-data-capture-and-extraction-into-platform/>

49\. **Dext bank statement extraction ---** <https://dext.com/us/business/products/bank-statements-extraction>

50\. **ServiceTitan Titan Intelligence ---** <https://www.servicetitan.com/features/titan-intelligence>

51\. **ServiceTitan AI in Trades report 2026 ---** <https://www.servicetitan.com/blog/ai-in-the-trades-report-takeaways>

52\. **PicoClaw GitHub ---** <https://github.com/sipeed/picoclaw>

53\. **PicoClaw README ---** <https://github.com/sipeed/picoclaw/blob/main/README.md>

54\. **PicoClaw Decision Guide (Dev.to) ---** <https://dev.to/shehzan/openclaw-vs-picoclaw-edge-ai-decision-guide-2026-31pg>

55\. **PicoClaw VPS Setup Guide (Dev.to) ---** <https://dev.to/cucoleadan/how-to-install-and-configure-picoclaw-on-the-cheapest-vps-1l73>

56\. **PicoClaw Awesome Agents Review ---** <https://awesomeagents.ai/reviews/review-picoclaw/>

57\. **PicoClaw DataCamp Tutorial ---** <https://www.datacamp.com/tutorial/picoclaw-tutorial>

58\. **PicoClaw Security Audit \#258 ---** <https://github.com/sipeed/picoclaw/issues/258>

59\. **PicoClaw Sandbox PR \#331 ---** <https://github.com/sipeed/picoclaw/issues/331>

60\. **PicoClaw Ollama Guide (Sonusahani) ---** <https://sonusahani.com/blogs/picoclaw-ollama>

61\. **Instructor homepage ---** <https://python.useinstructor.com>

62\. **Outlines GitHub ---** <https://github.com/dottxt-ai/outlines>

63\. **Graphiti GitHub ---** <https://github.com/getzep/graphiti>

64\. **FalkorDB GraphRAG explainer ---** <https://falkordb.com/blog/what-is-graphrag/>

65\. **Modal case study (Ramp) ---** <https://modal.com/blog/ramp-case-study>

66\. **Microsoft Azure / Ramp case study ---** <https://www.microsoft.com/en/customers/story/23693-ramp-azure-ai-services>

67\. **HomeLight / Extend case study ---** <https://www.extend.ai/resources/homelight-hits-99-accuracy-and-eliminates-manual-review-with-extend>

68\. **Brex / Extend case study ---** <https://www.extend.ai/resources/how-brex-reached-99-accuracy-across-millions-of-financial-documents>

69\. **Reducto vs Google Document AI ---** <https://llms.reducto.ai/reducto-vs-google-document-ai>

70\. **Unstract extraction comparison ---** <https://unstract.com/blog/comparing-approaches-for-using-llms-for-structured-data-extraction-from-pdfs/>

71\. **Docugami case studies ---** <https://www.docugami.com/case-studies>

72\. **LLM Auditability (LinkedIn) ---** <https://www.linkedin.com/posts/kevinpclancy_governance-and-regulation-if-your-llm-workflow-activity-7434416794628665346-wRRe>

73\. **Presidio blog on Graphiti ---** <https://www.presidio.com/technical-blog/graphiti-giving-ai-a-real-memory-a-story-of-temporal-knowledge-graphs/>

74\. **Nature: Hallucination in LLM summaries ---** <https://www.nature.com/articles/s41598-025-31075-1>

75\. **LessWrong: Summarisation affects LLM performance ---** <https://www.lesswrong.com/posts/KHHSryJAezhHmBEu6/does-summarization-affect-llm-performance>

76\. **ACL: LLM math mistake handling ---** <https://aclanthology.org/2025.acl-long.1313.pdf>

77\. **PromptLayer: LLM evaluation reproducibility ---** <https://blog.promptlayer.com/why-llm-evaluation-results-arent-reproducible-and-what-to-do-about-it/>

78\. **Address parsing (arXiv) ---** <https://arxiv.org/html/2601.18014v1>

79\. **Companies House API ---** <https://developer.company-information.service.gov.uk>

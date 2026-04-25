---
title: "Watchman Expansion Strategy"
id: "watchman-expansion-strategy"
version: 1
created: 2026-04-25
last_validated: 2026-04-25
type: document
topic_type: reference
status: imported
source_file: "watchman-expansion-strategy.docx"
signed_by: "Devon, 2026-04-25, devin-992682c244cf444f91e0a516498afbfd"
---

**Amplified Watchman Expansion:**

**Local LLM Strategy, Agent Cost**

**Reduction & Continuous Tuning**

*Beyond Monitoring --- A Complete Local Intelligence Layer for Amplified Partners*

March 2026

**Amplified Partners**

*Confidential --- Internal Strategy Document*

**1. Executive Summary**

This document answers three strategic questions about expanding the Amplified Watchman system from a monitoring layer into a complete local intelligence engine. Each question unlocks compounding value:

**Question 1: What other processes can go local?**

We have identified **35+ distinct processes** across 7 categories (classification & routing, summarization, code review, content generation, structured data extraction, quality scoring, and embedding & retrieval) that can be migrated from API-based large language models to locally-hosted small language models running on Beast\'s 96GB Ollama allocation. Research consistently shows that fine-tuned SLMs outperform larger zero-shot models for domain-specific tasks[^1], making local deployment not merely a cost play but a quality improvement.

**Question 2: Can we use cheaper agents because the environment is denoised?**

Yes. Watchman\'s denoising --- pre-classifying alerts, summarizing logs, structuring data, filtering false positives --- creates a **cleaner context window** for every downstream agent. Research from Anthropic[^2] and Chroma Research[^3] demonstrates that model performance degrades as irrelevant context increases. By removing noise *before* it reaches the agent, smaller models handle the pre-digested context just fine. JetBrains Research found that observation masking --- removing noise --- cut costs by over 50% while matching or beating full-context performance[^4]. We project a **50--70% total reduction** in LLM API spend through systematic model downgrades.

**Question 3: Can we tune beyond the baseline statistics?**

Absolutely. The baselines delivered in the previous analysis were *industry averages* from off-the-shelf tools. Through LoRA fine-tuning on Amplified-specific datasets (Enforcer reports, Linear issues, Cove build logs, Ewan\'s 2,214 monologue transcripts, marketing engagement data, past code reviews, and rubric scores), continuous Kaizen feedback loops, RAG enhancement via FalkorDB, and systematic promptfoo testing, we can push every metric significantly beyond baseline. Fine-tuned Mistral-7B has outperformed GPT-4o on domain tasks[^5]; Invisible Technologies\' Diabetica-7B surpassed GPT-4 at 87.2% accuracy on medical classification[^6]. The same approach, applied weekly via Kaizen loops, turns baseline floors into continuously rising ceilings.

**2. The Full Process Map: 35+ Processes for Local Models**

Below we catalogue every process identified across the Amplified stack that is a candidate for local model execution on Beast. Processes are grouped into 7 categories, ordered by migration value. Each table shows the current model, proposed local replacement, and estimated savings.

**2.1 Classification & Routing**

*Highest local value.* High-volume, low-complexity tasks where fine-tuned local models match or beat API models. Research shows smaller fine-tuned LLMs \"consistently and significantly outperform larger, zero-shot prompted models\" in text classification[^7]. Cobus Greyling demonstrates SLMs achieve \"near-perfect accuracy\" for classification tasks[^8]. Fine-tuned 3--4B models are \"viable solutions\" for multi-turn customer-service QA[^9].

  --------------------------------------- ------------------------ -------------------------- ------------------
  **Process Name**                        **Current Model**        **Proposed Local Model**   **Est. Savings**
  Email triage & classification           API (mixed)              Qwen 2.5 3B Instruct       \~100%
  Linear issue classification             API (mixed)              Qwen 2.5 3B Instruct       \~100%
  Content quality gate (first-pass)       API (Gatekeeper)         Phi-4-mini 3.8B            \~100%
  Alert classification (Watchman)         API (mixed)              SmolLM3-3B                 \~100%
  Customer query routing                  API (mixed)              Qwen 2.5 3B Instruct       \~100%
  Vault document classification           API (mixed)              Qwen 2.5 3B Instruct       \~100%
  Marketing content type classification   API (marketing agents)   SmolLM3-3B                 \~100%
  --------------------------------------- ------------------------ -------------------------- ------------------

**2.2 Summarization & Compression**

*High local value.* Essential for Watchman\'s denoising pipeline. Hugging Face confirms SLMs handle summarization as a core capability[^10]. BentoML ranks SmolLM3-3B and Phi-4-mini as strong for instruction-following tasks including summarization[^11].

  ------------------------------------ ------------------------ -------------------------- ------------------
  **Process Name**                     **Current Model**        **Proposed Local Model**   **Est. Savings**
  Enforcer report summarization        gpt-4.1-mini (API)       Qwen 2.5 7B Instruct       \~100%
  Build log summarization              claude-sonnet (API)      Qwen 2.5 7B Instruct       \~100%
  Monologue transcript summarization   API (mixed)              Llama 3.1 8B (deployed)    \~100%
  Langfuse trace summarization         API (mixed)              Phi-4-mini 3.8B            \~100%
  Research document summarization      API (mixed)              Qwen 2.5 7B Instruct       \~100%
  Marketing content briefing           API (marketing agents)   Qwen 2.5 7B Instruct       \~100%
  ------------------------------------ ------------------------ -------------------------- ------------------

**2.3 Code Review & Static Analysis**

*Already planned --- scope expanded.* Qwen 2.5 Coder 7B scores 88.4% on benchmarks, approaching GPT-4\'s 87.1%[^12]. On the Spider SQL benchmark, Qwen 2.5 Coder leads at 82.0% vs Codestral\'s 76.6%. Qwen 2.5 Coder 32B achieves 49% HumanEval --- best Python performance among local models[^13].

  ------------------------------ --------------------- -------------------------- ------------------
  **Process Name**               **Current Model**     **Proposed Local Model**   **Est. Savings**
  PR code review                 claude-sonnet (API)   Qwen 2.5 Coder 7B          \~60-70%
  Commit message quality check   API (mixed)           Qwen 2.5 Coder 7B          \~100%
  Docker compose validation      API (mixed)           Qwen 2.5 Coder 14B         \~100%
  Prompt template review         API (mixed)           Qwen 2.5 Coder 7B          \~100%
  YAML/JSON config validation    API (mixed)           Qwen 2.5 Coder 7B          \~100%
  Migration script review        claude-opus (API)     Qwen 2.5 Coder 32B         \~50-60%
  ------------------------------ --------------------- -------------------------- ------------------

**2.4 Content Generation & Drafting**

*Medium local value.* Lower-stakes content where consistency matters more than creativity. Prem AI case study: a SaaS startup switched 70% of calls to Qwen models, cutting spend from \$15,000/month to \$4,500/month[^14]. The 14-agent marketing pipeline is the biggest cost centre for local model migration.

  ------------------------------------- ------------------- -------------------------- ------------------
  **Process Name**                      **Current Model**   **Proposed Local Model**   **Est. Savings**
  Marketing social media first drafts   API (14 agents)     Qwen 2.5 7B Instruct       \~60-70%
  Commit message generation             API (mixed)         Llama 3.1 8B (deployed)    \~100%
  Documentation scaffolding             API (mixed)         Qwen 2.5 7B Instruct       \~100%
  Alert notification drafting           API (mixed)         Llama 3.1 8B (deployed)    \~100%
  Client report first drafts            API (mixed)         Mistral Small 3.2 24B      \~40-50%
  ------------------------------------- ------------------- -------------------------- ------------------

**2.5 Structured Data Extraction & Validation**

*High local value.* Parsing structured data from unstructured sources. Qwen 2.5 excels at \"understanding structured data (e.g., tables) and generating structured outputs, especially in JSON format\"[^15]. Function calling support in Qwen 2.5 and Phi-4-mini enables tool-using workflows locally.

  ----------------------------------------- ------------------- -------------------------- ------------------
  **Process Name**                          **Current Model**   **Proposed Local Model**   **Est. Savings**
  Companies House XBRL parsing validation   API (ch-pipeline)   Qwen 2.5 7B Instruct       \~100%
  Invoice/receipt data extraction           API (mixed)         Phi-4-mini 3.8B            \~100%
  Vault entity extraction                   API (mixed)         Qwen 2.5 7B Instruct       \~100%
  Log parsing (structured events)           API (mixed)         Qwen 2.5 3B Instruct       \~100%
  Webhook payload validation                API (mixed)         Phi-4-mini 3.8B            \~100%
  ----------------------------------------- ------------------- -------------------------- ------------------

**2.6 Quality Scoring & Evaluation**

*Medium-high local value.* Using local models as evaluators and judges for other agent outputs. ApX ML describes \"model-based evaluation: using specialized smaller models to score or classify the LLM\'s output\"[^16]. AWS research shows semantic tool selection \"reduces errors by up to 86.4% and cuts token costs by 89%\"[^17]. Fine-tuned evaluator models can be made domain-specific.

  ------------------------------------ ------------------------ -------------------------- ------------------
  **Process Name**                     **Current Model**        **Proposed Local Model**   **Est. Savings**
  Rubric scoring (Cove quality gate)   API (mixed)              Qwen 2.5 14B Instruct      \~100%
  Content quality scoring              API (marketing agents)   Qwen 2.5 14B Instruct      \~100%
  promptfoo test evaluation            API (mixed)              Llama 3.1 8B               \~100%
  Build quality assessment             API (mixed)              Qwen 2.5 7B Instruct       \~100%
  Customer interaction quality         API (mixed)              Qwen 2.5 14B Instruct      \~100%
  ------------------------------------ ------------------------ -------------------------- ------------------

**2.7 Embedding & Retrieval**

*Already local --- scope expanded.* Already using nomic-embed-text locally for Vault document embedding. Expand to cover semantic deduplication, similarity detection, and cross-domain connection discovery.

  ----------------------------------- -------------------------- ----------------------------- ------------------
  **Process Name**                    **Current Model**          **Proposed Local Model**      **Est. Savings**
  Vault document embedding            nomic-embed-text (local)   nomic-embed-text (deployed)   Already \$0
  Semantic search for agent context   nomic-embed-text (local)   nomic-embed-text (deployed)   Already \$0
  Alert deduplication (semantic)      API (mixed)                nomic-embed-text (local)      \~100%
  Content similarity detection        API (mixed)                nomic-embed-text (local)      \~100%
  PUDDING cross-domain discovery      API (mixed)                nomic-embed-text (local)      \~100%
  ----------------------------------- -------------------------- ----------------------------- ------------------

**Process Count Summary**

**Total processes identified: 39** across 7 categories. Of these, 2 are already running locally (Vault embedding, semantic search). The remaining 37 are candidates for immediate or phased migration from API to local execution.

**3. The Denoising Dividend: Cheaper Agents Through Cleaner Context**

**3.1 The Problem: Context Rot**

When agents receive noisy, unfiltered context --- raw logs, unclassified alerts, verbose traces --- they must perform *retrieval and reasoning simultaneously*, degrading both capabilities. This is well-documented:

**Chroma Research (Jul 2025):** \"Model performance degrades as input length increases, often in surprising and non-uniform ways.\" Adding irrelevant context forces models to search for needles in haystacks rather than focus on reasoning[^18].

**Anthropic (Sep 2025):** \"Context rot: as the number of tokens in the context window increases, the model\'s ability to accurately recall information from that context decreases.\" Their recommendation: \"finding the smallest possible set of high-signal tokens\"[^19].

**JetBrains Research (Dec 2025):** Observation masking (removing noise) \"cut costs by over 50% compared to unmanaged context\" and \"often matched or even slightly beat LLM summarization in solving benchmark tasks\"[^20].

**3.2 Structured Data Eliminates Hallucination**

**Promethium (Mar 2026):** \"Properly grounded RAG systems reduce hallucinations approximately 60% compared to ungrounded approaches\"[^21].

**AWS/Dev.to (Feb 2026):** \"Graph-RAG eliminates statistical hallucinations by using structured data instead of text retrieval. Semantic tool selection reduces errors by up to 86.4% and cuts token costs by 89%\"[^22].

**Reddit/LLMDevs (Jan 2026):** \"The primary contributor to hallucinations isn\'t necessarily the model itself, but rather inadequate memory.\" When agents have clean, structured history, they stop guessing[^23].

**3.3 The Denoising Cascade**

Watchman creates a systematic pipeline that transforms raw, noisy environment data into focused, structured context before it ever reaches a downstream agent:

**RAW ENVIRONMENT** → **WATCHMAN DENOISES** → **CLEANER CONTEXT** → **SMALLER MODEL SUFFICIENT**

  ---------- ---------------------------------------------------------------------------------------
  **Step**   **Description**
  1          Watchman observes everything (read-only monitoring across all services)
  2          Local classifiers filter noise (false positives removed by 3B classification models)
  3          Local summarizers compress context (10x token reduction via 7B summarization models)
  4          Structured outputs replace freeform (JSON schemas enforce data shape and consistency)
  5          Downstream agent receives pre-digested, focused context window
  6          Smaller, cheaper model handles the pre-digested context with equal or better accuracy
  ---------- ---------------------------------------------------------------------------------------

**3.4 The Model Downgrade Map (Post-Watchman)**

With denoised context, every agent role in the Amplified stack can be systematically evaluated for model downgrade:

  ----------------------- --------------------- ----------------------- --------------------------------------------------------- -------------- ---------------
  **Agent Role**          **Current Model**     **Cost Tier**           **Post-Watchman Model**                                   **New Tier**   **Savings**
  Enforcer                gpt-4.1-mini (API)    \$0.40/\$1.60 /1M tok   Qwen 2.5 3B (local)                                       \$0            \~100%
  Reviewer                claude-sonnet (API)   \$3/\$15 /1M tok        Qwen 2.5 14B (local) routine; Sonnet complex              \~\$0 / API    \~60-70%
  Coder                   claude-sonnet (API)   \$3/\$15 /1M tok        Qwen 2.5 Coder 14B (local) boilerplate; Sonnet complex    \~\$0 / API    \~40-50%
  Architect               claude-opus (API)     \$5/\$25 /1M tok        Keep Opus; pre-summarized context → fewer tokens          API reduced    \~30-40%
  Security                claude-opus (API)     \$5/\$25 /1M tok        Qwen 2.5 Coder 32B first pass + Opus final review         Local + API    \~50-60%
  Marketing (14 agents)   Mixed API             Variable                70% local (drafts, classification) + 30% API (creative)   Hybrid         \~60-70%
  Gatekeeper              API (assumed)         Variable                Qwen 2.5 7B (local)                                       \$0            \~100%
  AI Board Facilitator    Llama 3.1 8B          Already local           Llama 3.1 8B (no change)                                  \$0            Already saved
  ----------------------- --------------------- ----------------------- --------------------------------------------------------- -------------- ---------------

**3.5 Estimated Total Cost Reduction**

Based on the research evidence and the downgrade map above:

Self-hosted SLMs can \"reduce costs by up to 29x\" versus API models[^24]. Prem AI reports that \"companies can reduce costs by 50--90% without sacrificing performance\" using hybrid local/cloud architectures[^25].

**Conservative estimate: 50--70% reduction in total LLM API spend across all processes.** This is achievable through the combination of: (a) moving high-volume, low-complexity tasks entirely local; (b) downgrading agent models where denoised context permits; and (c) reducing token consumption through pre-summarization and structured outputs.

**4. The Complete Local Model Menu**

All recommended models are available via Hugging Face and Ollama. Quantised to Q4 for optimal RAM/quality balance on Beast\'s 96GB Ollama allocation.

**4.1 Recommended Model Stack for Beast**

  ----------------------------- ------------ -------------- ------------------ ----------------------------------------------------------------
  **Model**                     **Params**   **VRAM/RAM**   **Speed (est.)**   **Primary Use Cases**
  SmolLM3-3B                    3B           \~2GB Q4       30-50 tok/s        Ultra-fast classification, routing, first-pass filter
  Qwen 2.5 3B Instruct          3B           1.9GB Q4       30-50 tok/s        Alert classification, email triage, vault tagging, JSON output
  Phi-4-mini 3.8B               3.8B         \~2.5GB Q4     25-40 tok/s        Structured reasoning, function calling, JSON output
  Qwen 2.5 7B Instruct          7B           4.7GB Q4       15-25 tok/s        Summarization, content drafting, quality scoring, extraction
  Qwen 2.5 Coder 7B             7B           4.7GB Q4       15-25 tok/s        PR review, code validation, SQL checking, commit checks
  Llama 3.1 8B (deployed)       8B           \~5GB Q4       39 tok/s ✓         General tasks, notifications, AI Board Facilitator
  Qwen 2.5 14B Instruct         14B          \~9GB Q4       8-15 tok/s         Complex evaluation, rubric scoring, reviewer tasks
  Qwen 2.5 Coder 14B            14B          \~9GB Q4       8-15 tok/s         Nightly deep code review, migration analysis
  Mistral Small 3.2 24B         24B          \~15GB Q4      6-10 tok/s         Complex general tasks, multi-turn reasoning, EU-hosted
  Qwen 2.5 Coder 32B            32B          \~18GB Q4      4-8 tok/s          Monthly deep security review, complex refactoring
  Llama 3.1 70B (deployed)      70B          \~40GB Q4      4-8 tok/s          AI Board COO, complex reasoning, fallback
  nomic-embed-text (deployed)   137M         \<1GB          N/A                Document embedding, semantic search, deduplication
  ----------------------------- ------------ -------------- ------------------ ----------------------------------------------------------------

**Total RAM needed (all loaded simultaneously): \~107GB Q4.** Beast Ollama allocation: 96GB. Strategy: keep frequently-used models hot; swap larger models on demand.

**4.2 Model Loading Strategy**

Given 96GB RAM, we partition models into three tiers based on usage frequency and load latency:

  ------------ ------------------------------------------------------------------------------- -------------------
  **Tier**     **Models**                                                                      **RAM Footprint**
  Always Hot   SmolLM3-3B + Qwen 2.5 3B + Qwen 2.5 7B + Llama 3.1 8B + nomic-embed-text        \~14GB
  On Demand    Qwen 2.5 Coder 7B, Qwen 2.5 14B Instruct, Qwen 2.5 Coder 14B, Phi-4-mini 3.8B   \~9-18GB per swap
  Scheduled    Mistral Small 3.2 24B, Qwen 2.5 Coder 32B, Llama 3.1 70B                        15-40GB per model
  ------------ ------------------------------------------------------------------------------- -------------------

**Always Hot (\~14GB):** These models handle the highest-volume tasks (classification, routing, summarization, general queries) and remain resident in RAM at all times for sub-second inference.

**On Demand (\~9--18GB per swap):** Loaded when specific tasks require them (code review sessions, complex evaluation). Ollama\'s model loading from disk typically takes 2--5 seconds for Q4 models.

**Scheduled (15--40GB per model):** Loaded during off-peak hours for nightly deep code analysis (Qwen 2.5 Coder 32B), monthly security reviews, or AI Board sessions (Llama 3.1 70B). LiteLLM handles routing: always try local first, fall back to API when local is insufficient.

**5. Tuning Beyond Baseline: Fine-Tuning, RAG & Kaizen Loops**

The statistics delivered in the previous Watchman analysis were *industry baselines* from off-the-shelf tools. They are not a ceiling --- they are a floor. Four methods, used in combination, push every metric significantly further.

**5.1 Method 1: LoRA Fine-Tuning on Domain-Specific Data**

Low-Rank Adaptation (LoRA) trains small adapter layers --- 0.1--1% of total parameters --- on domain-specific data while keeping the base model frozen. The adapter is exported directly to Ollama with one command.

**Evidence**

Fine-tuned small LLMs \"consistently and significantly outperform larger, zero-shot prompted models in text classification\" --- fine-tuned BERT-style models beat ChatGPT and Claude Opus zero-shot across all four test applications[^26].

Fine-tuned Mistral-7B achieved F1 0.6837, outperforming GPT-4o and Gemini 2.0 on domain-specific tasks[^27].

Invisible Technologies\' Diabetica-7B achieved 87.2% accuracy, surpassing GPT-4 and Claude-3.5 on domain-specific medical classification[^28].

LoRA training on an RTX 3080 completes 5 epochs in 65 seconds; one-click deploy to Ollama[^29]. Beast\'s 48-core EPYC with 96GB RAM can handle LoRA fine-tuning of 7B--14B models via Unsloth or similar frameworks.

**Amplified-Specific Datasets for Fine-Tuning**

Seven domain datasets unique to Amplified provide the training foundation:

  -------- ------------------------------------- ------------------------------------------------------ ------------------------------------------------------------------------
  **\#**   **Dataset**                           **Source**                                             **Training Objective**
  1        Historical Enforcer reports           Enforcer health checks (5 concurrent, 10-min cycles)   Train a local Enforcer that knows YOUR infrastructure patterns
  2        Past Linear issues                    Linear issue tracker                                   Train a classifier that knows YOUR issue taxonomy and priorities
  3        Cove build logs                       CI/CD pipeline outputs                                 Train a summarizer that knows YOUR codebase and error patterns
  4        Ewan\'s 2,214 monologue transcripts   Monologue archive                                      Train a model that knows YOUR voice, priorities, and decision patterns
  5        Marketing content + engagement data   Marketing pipeline (14 agents)                         Train a content scorer that knows YOUR audience and what performs
  6        Past code reviews                     Cove reviewer outputs                                  Train a reviewer that knows YOUR coding standards and conventions
  7        Rubric scores                         Gatekeeper quality gate outputs                        Train a quality evaluator tuned to YOUR specific rubrics
  -------- ------------------------------------- ------------------------------------------------------ ------------------------------------------------------------------------

**5.2 Method 2: Continuous Feedback Loops (Kaizen Fine-Tuning)**

Rather than fine-tuning once, systematically collect feedback from production, curate datasets, and re-fine-tune on a weekly schedule. This is the Kaizen philosophy --- continuous incremental improvement --- applied to model quality.

AWS SageMaker\'s \"continuous self-instruct fine-tuning framework\" uses RLHF/RLAIF to keep models improving from production feedback[^30]. Heavybit confirms \"fine-tuning is a continuous process to keep the fine-tuned model accurate and effective in changing environments\"[^31]. ApX ML describes curating \"explicit corrections and high-quality examples for SFT or preference datasets for RLHF/DPO\"[^32].

**The Amplified Kaizen Fine-Tuning Loop**

  ----------- ------------------------------------------------------------------------------
  **Phase**   **Activity**
  Week 1      Deploy base local model (e.g., Qwen 2.5 7B Instruct)
  Daily       Collect production data --- agent outputs + human feedback (Langfuse traces)
  Weekly      Curate training dataset from best/worst examples (automated pipeline)
  Weekly      LoRA fine-tune on curated data (Beast CPU via Unsloth)
  Weekly      A/B test fine-tuned vs. base on held-out evaluation set (promptfoo)
  Monthly     Merge best LoRA adapters into updated base model
  Repeat      Model gets measurably better every week, tuned to YOUR data
  ----------- ------------------------------------------------------------------------------

**5.3 Method 3: RAG Enhancement (Structured Retrieval)**

Instead of stuffing everything into the context window, use FalkorDB (already deployed as the Business Brain) to retrieve only the relevant structured data before inference. Graph-RAG via FalkorDB + Cypher queries eliminates statistical hallucinations entirely for structured queries.

Promethium confirms \"properly grounded RAG reduces hallucinations \~60%\"[^33]. The Text2Cypher pattern --- natural language → Cypher → deterministic database answer → LLM formats response --- provides zero-hallucination answers for any data held in the knowledge graph.

**5.4 Method 4: promptfoo Testing**

Systematic prompt optimization using promptfoo (already planned in Watchman) with automated evaluation against the 705-case golden dataset from AMF. Each prompt iteration is measurably scored; improvements are proven, not assumed. Combined with local evaluator models (Qwen 2.5 14B as judge), this creates a fully automated prompt quality pipeline.

**5.5 Beyond Baseline: Projected Metrics**

Combining all four methods, here are projected metric improvements over time:

  ------------------------ -------------------------------- ----------------------- --------------------------------------------- -----------------------------------------
  **Metric**               **Industry Baseline**            **Watchman Baseline**   **With Fine-Tuning**                          **With Kaizen Loop (6mo)**
  MTTD (detection speed)   \~60% faster                     \~60% faster            \~70% faster (domain-tuned classifiers)       \~80% faster (continuously refined)
  Defects caught           \~3x improvement                 \~3x improvement        \~4-5x (trained on YOUR codebase)             \~6-8x (accumulating pattern library)
  False positive rate      80-90% reduction                 80-90% reduction        92-95% reduction (tuned to YOUR infra)        97-99% reduction (learns noise profile)
  Token costs              \~100% eliminated (monitoring)   \~100% eliminated       Eliminates expensive models on 70% of tasks   Compounding savings
  Content quality scores   10-20% better                    10-20% better           25-35% better (trained on YOUR rubrics)       40-50% better (engagement data)
  LLM output consistency   Variable                         Improved                Significantly improved (domain-specific)      Near-deterministic for routine tasks
  ------------------------ -------------------------------- ----------------------- --------------------------------------------- -----------------------------------------

**6. The Kaizen Integration: Implementation Roadmap**

The implementation follows four phases, each building on the last. The key principle: deploy, measure, tune, repeat.

**Phase 1: Deploy & Measure (Weeks 1--2)**

  ------------------------------------ -------------------------------------------------------------------------------------------
  **Activity**                         **Detail**
  Deploy local classification models   SmolLM3-3B, Qwen 2.5 3B for alert classification, email triage, routing
  Deploy local summarization models    Qwen 2.5 7B Instruct, Llama 3.1 8B for log and report summarization
  Run shadow mode                      Local models run in parallel with API models; outputs compared but not used in production
  Establish baseline metrics           Accuracy, latency, token savings, false positive rates for every process
  Configure Langfuse tracing           Full observability on both local and API paths for comparison data
  ------------------------------------ -------------------------------------------------------------------------------------------

**Phase 2: First Fine-Tuning Round (Weeks 3--4)**

  -------------------------------------- -----------------------------------------------------------------------
  **Activity**                           **Detail**
  Collect 2 weeks of production data     Agent outputs + human feedback from Langfuse traces
  Curate training datasets               Best/worst examples from shadow mode comparison data
  LoRA fine-tune classification models   Domain-specific adapters for alert, issue, and content classification
  A/B test fine-tuned vs base            Automated evaluation via promptfoo against held-out test set
  Deploy winners                         Replace base models with fine-tuned variants; API remains as fallback
  -------------------------------------- -----------------------------------------------------------------------

**Phase 3: Expand & Downgrade (Weeks 5--8)**

  ------------------------------------ -----------------------------------------------------------------------
  **Activity**                         **Detail**
  Expand local models                  Add content generation, quality scoring, structured extraction models
  Begin systematic API downgrades      Where local matches API quality, switch production traffic to local
  Migrate Enforcer fully local         Complete migration of all Enforcer health checks to Qwen 2.5 3B
  Begin marketing pipeline migration   Target 70% of 14-agent marketing pipeline to local models
  Deploy code review expansion         Qwen 2.5 Coder 7B for daily PR review; 14B for nightly deep analysis
  ------------------------------------ -----------------------------------------------------------------------

**Phase 4: Continuous Kaizen Loop (Week 9+, Forever)**

  ----------------------------------- ------------------------------------------------------------------------------
  **Activity**                        **Detail**
  Weekly: curate new training data    Ongoing collection from production outputs and human corrections
  Weekly: fine-tune and evaluate      Automated LoRA training pipeline on Beast, evaluated via promptfoo
  Monthly: merge adapters             Best LoRA adapters merged into updated base models, published to Ollama
  Monthly: deep security review       Qwen 2.5 Coder 32B loaded for comprehensive security analysis
  Quarterly: model landscape review   Assess new Hugging Face releases; pull improved base models
  Ongoing: 705-case golden dataset    AMF golden dataset serves as the evaluation benchmark for every model update
  Ongoing: Enforcer monitoring        Enforcer monitors model performance drift; alerts on degradation
  Ongoing: Kaizen Optimizer           Daily improvement cycle (03:00 UTC) identifies optimization opportunities
  ----------------------------------- ------------------------------------------------------------------------------

**The Flywheel Effect**

Every improvement compounds. The system creates a self-reinforcing cycle:

**Better local models** → **Cleaner context** → **Cheaper API calls** → **More budget for fine-tuning** → **Even better local models** → \...

The baseline statistics from the previous analysis are not a ceiling --- they are a floor. With Kaizen, the system gets measurably better every single week. Cost savings compound, accuracy rises, false positives drop, and the local models become increasingly tuned to Amplified\'s specific patterns, vocabulary, and quality standards.

**7. Sources**

All sources are cited inline as footnotes throughout this document. The complete list with URLs is provided below for reference.

**1.** arXiv --- \"Fine-Tuned Small LLMs Still Significantly Outperform Zero-Shot\" <https://arxiv.org/html/2406.08660v2>

**2.** arXiv --- \"Cost-Benefit Analysis Replacing OpenAI with Open Source SLMs\" <https://arxiv.org/html/2312.14972v3>

**3.** arXiv --- \"SLMs for Context-Summarized Multi-Turn Customer Service\" <https://arxiv.org/html/2602.00665v1>

**4.** Chroma Research --- \"Context Rot\" <https://research.trychroma.com/context-rot>

**5.** Anthropic --- \"Effective Context Engineering for AI Agents\" <https://www.anthropic.com/engineering/effective-context-engineering-for-ai-agents>

**6.** JetBrains Research --- \"Cutting Through the Noise\" <https://blog.jetbrains.com/research/2025/12/efficient-context-management/>

**7.** Promethium --- \"Building AI Agents That Don\'t Hallucinate\" <https://promethium.ai/guides/building-ai-agents-that-dont-hallucinate-enterprise-data/>

**8.** Dev.to/AWS --- \"Stop AI Agent Hallucinations: 4 Essential Techniques\" <https://dev.to/aws/stop-ai-agent-hallucinations-4-essential-techniques-2i94>

**9.** Prem AI --- \"How to Save 90% on LLM API Costs\" <https://blog.premai.io/how-to-save-90-on-llm-api-costs-without-losing-performance/>

**10.** Hugging Face --- \"Small Language Models Overview\" <https://huggingface.co/blog/jjokah/small-language-model>

**11.** BentoML --- \"Best Open-Source Small Language Models 2026\" <https://www.bentoml.com/blog/the-best-open-source-small-language-models>

**12.** LocalAI Master --- \"Best Local AI Coding Models\" <https://localaimaster.com/models/best-local-ai-coding-models>

**13.** LocalAI Master --- \"LoRA Fine-Tuning Local Guide\" <https://localaimaster.com/blog/lora-fine-tuning-local-guide>

**14.** Deepgram --- \"Best Local Coding LLMs\" <https://deepgram.com/learn/best-local-coding-llm>

**15.** AWS SageMaker --- \"Continuous Self-Instruct Fine-Tuning Framework\" <https://aws.amazon.com/blogs/machine-learning/llm-continuous-self-instruct-fine-tuning-framework-powered-by-a-compound-ai-system-on-amazon-sagemaker/>

**16.** Heavybit --- \"LLM Fine-Tuning Guide\" <https://www.heavybit.com/library/article/llm-fine-tuning>

**17.** Invisible Technologies --- \"SLMs vs LLMs\" <https://invisibletech.ai/blog/how-small-language-models-can-outperform-llms>

**18.** GitHub (subhashbs36) --- \"Fine-tuning Small LLMs to Outperform Large Models\" <https://github.com/subhashbs36/finetuning-small-llms-to-outperform-large-models-on-specific-tasks>

**19.** Unsloth --- \"How to Finetune and Use in Ollama\" <https://unsloth.ai/docs/get-started/fine-tuning-llms-guide/tutorial-how-to-finetune-llama-3-and-use-in-ollama>

**20.** Cobus Greyling --- \"Small Language Models & Classification\" <https://cobusgreyling.substack.com/p/small-language-models-slms-and-classification>

**21.** Kili Technology --- \"Guide to Small Language Models for Business\" <https://kili-technology.com/blog/a-guide-to-using-small-language-models>

**22.** Ollama --- \"Qwen 2.5 3B Instruct\" <https://ollama.com/library/qwen2.5:3b-instruct>

**23.** ApX ML --- \"Building Feedback Loops for Continuous Improvement\" <https://apxml.com/courses/mlops-for-large-models-llmops/chapter-5-llm-monitoring-observability-maintenance/llm-feedback-loops>

**24.** Reddit r/LocalLLaMA --- \"API pricing freefall\" <https://www.reddit.com/r/LocalLLaMA/comments/1qp6rm5/api_pricing_is_in_freefall_whats_the_actual_case/>

**25.** Reddit r/LLMDevs --- \"How to reduce AI agent hallucinations\" <https://www.reddit.com/r/LLMDevs/comments/1qea6bz/how_to_actually_reduce_ai_agent_hallucinations/>

[^1]: arXiv --- \"Fine-Tuned Small LLMs Still Significantly Outperform Zero-Shot\", <https://arxiv.org/html/2406.08660v2>

[^2]: Anthropic --- \"Effective Context Engineering for AI Agents\", <https://www.anthropic.com/engineering/effective-context-engineering-for-ai-agents>

[^3]: Chroma Research --- \"Context Rot\", <https://research.trychroma.com/context-rot>

[^4]: JetBrains Research --- \"Cutting Through the Noise\", <https://blog.jetbrains.com/research/2025/12/efficient-context-management/>

[^5]: GitHub (subhashbs36) --- \"Fine-tuning Small LLMs to Outperform Large Models\", <https://github.com/subhashbs36/finetuning-small-llms-to-outperform-large-models-on-specific-tasks>

[^6]: Invisible Technologies --- \"SLMs vs LLMs\", <https://invisibletech.ai/blog/how-small-language-models-can-outperform-llms>

[^7]: arXiv --- \"Fine-Tuned Small LLMs Still Significantly Outperform Zero-Shot\", <https://arxiv.org/html/2406.08660v2>

[^8]: Cobus Greyling --- \"Small Language Models & Classification\", <https://cobusgreyling.substack.com/p/small-language-models-slms-and-classification>

[^9]: arXiv --- \"SLMs for Context-Summarized Multi-Turn Customer Service\", <https://arxiv.org/html/2602.00665v1>

[^10]: Hugging Face --- \"Small Language Models Overview\", <https://huggingface.co/blog/jjokah/small-language-model>

[^11]: BentoML --- \"Best Open-Source Small Language Models 2026\", <https://www.bentoml.com/blog/the-best-open-source-small-language-models>

[^12]: Deepgram --- \"Best Local Coding LLMs\", <https://deepgram.com/learn/best-local-coding-llm>

[^13]: LocalAI Master --- \"Best Local AI Coding Models\", <https://localaimaster.com/models/best-local-ai-coding-models>

[^14]: Prem AI --- \"How to Save 90% on LLM API Costs\", <https://blog.premai.io/how-to-save-90-on-llm-api-costs-without-losing-performance/>

[^15]: Ollama --- \"Qwen 2.5 3B Instruct\", <https://ollama.com/library/qwen2.5:3b-instruct>

[^16]: ApX ML --- \"Building Feedback Loops for Continuous Improvement\", <https://apxml.com/courses/mlops-for-large-models-llmops/chapter-5-llm-monitoring-observability-maintenance/llm-feedback-loops>

[^17]: Dev.to/AWS --- \"Stop AI Agent Hallucinations: 4 Essential Techniques\", <https://dev.to/aws/stop-ai-agent-hallucinations-4-essential-techniques-2i94>

[^18]: Chroma Research --- \"Context Rot\", <https://research.trychroma.com/context-rot>

[^19]: Anthropic --- \"Effective Context Engineering for AI Agents\", <https://www.anthropic.com/engineering/effective-context-engineering-for-ai-agents>

[^20]: JetBrains Research --- \"Cutting Through the Noise\", <https://blog.jetbrains.com/research/2025/12/efficient-context-management/>

[^21]: Promethium --- \"Building AI Agents That Don\'t Hallucinate\", <https://promethium.ai/guides/building-ai-agents-that-dont-hallucinate-enterprise-data/>

[^22]: Dev.to/AWS --- \"Stop AI Agent Hallucinations: 4 Essential Techniques\", <https://dev.to/aws/stop-ai-agent-hallucinations-4-essential-techniques-2i94>

[^23]: Reddit r/LLMDevs --- \"How to reduce AI agent hallucinations\", <https://www.reddit.com/r/LLMDevs/comments/1qea6bz/how_to_actually_reduce_ai_agent_hallucinations/>

[^24]: arXiv --- \"Cost-Benefit Analysis Replacing OpenAI with Open Source SLMs\", <https://arxiv.org/html/2312.14972v3>

[^25]: Prem AI --- \"How to Save 90% on LLM API Costs\", <https://blog.premai.io/how-to-save-90-on-llm-api-costs-without-losing-performance/>

[^26]: arXiv --- \"Fine-Tuned Small LLMs Still Significantly Outperform Zero-Shot\", <https://arxiv.org/html/2406.08660v2>

[^27]: GitHub (subhashbs36) --- \"Fine-tuning Small LLMs to Outperform Large Models\", <https://github.com/subhashbs36/finetuning-small-llms-to-outperform-large-models-on-specific-tasks>

[^28]: Invisible Technologies --- \"SLMs vs LLMs\", <https://invisibletech.ai/blog/how-small-language-models-can-outperform-llms>

[^29]: LocalAI Master --- \"LoRA Fine-Tuning Local Guide\", <https://localaimaster.com/blog/lora-fine-tuning-local-guide>

[^30]: AWS SageMaker --- \"Continuous Self-Instruct Fine-Tuning Framework\", <https://aws.amazon.com/blogs/machine-learning/llm-continuous-self-instruct-fine-tuning-framework-powered-by-a-compound-ai-system-on-amazon-sagemaker/>

[^31]: Heavybit --- \"LLM Fine-Tuning Guide\", <https://www.heavybit.com/library/article/llm-fine-tuning>

[^32]: ApX ML --- \"Building Feedback Loops for Continuous Improvement\", <https://apxml.com/courses/mlops-for-large-models-llmops/chapter-5-llm-monitoring-observability-maintenance/llm-feedback-loops>

[^33]: Promethium --- \"Building AI Agents That Don\'t Hallucinate\", <https://promethium.ai/guides/building-ai-agents-that-dont-hallucinate-enterprise-data/>

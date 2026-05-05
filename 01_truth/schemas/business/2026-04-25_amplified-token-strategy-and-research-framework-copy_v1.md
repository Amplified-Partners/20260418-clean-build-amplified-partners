---
title: "Amplified Token Strategy And Research Framework Copy"
id: "amplified-token-strategy-and-research-framework-copy"
version: 1
created: "2026-04-25"
type: "document"
topic_type: "strategy"
audience: "internal"
layer: "truth"
status: "filed"
signed_by: "Devon, 2026-04-25, devin-992682c244cf444f91e0a516498afbfd"
---

**AMPLIFIED PARTNERS**

**Token Strategy &**

**Research Framework**

v1.0

*Spend Smart, Research Deep, Ship Fast*

Classification: Internal Technical Architecture

Date: March 2026

Author: Ewan Bramley / Amplified Partners

**1. The Problem**

Three problems wrapped together, each compounding the others:

**1. Token haemorrhage on simple tasks.** Cloud API spend on work that local models could handle: health checks, classification, formatting, simple extraction, scoring, labelling. Approximately £3,000 spent to date on Perplexity/Computer credits --- not wasted, but a significant portion went to tasks a 3B parameter model could perform.

**2. No research depth framework.** No defined boundary for when research is \"deep enough\" versus diminishing returns. Without this, every research task defaults to maximum depth, burning premium tokens on work that needed only surface-level verification.

**3. Model selection gap.** Need to know which Hugging Face models to pull into Ollama for specific task tiers. The Beast server (Hetzner AX162-R, 48-core EPYC, 256GB RAM) already runs Ollama with Llama 3.1 8B/70B, but the local model roster doesn\'t cover structured output, lightweight classification, or multimodal tasks.

**The goal:** Spend £3,000 making the system RIGHT --- not £3,000 paying Claude to do work a 3B parameter model could handle.

**2. The Three-Tier Routing Strategy (Upgraded)**

This maps directly to the existing LiteLLM setup but adds specific task routing rules and local model coverage. The system already uses LiteLLM as a routing proxy with three tiers: cheap (GPT-4.1-mini), medium (Claude Sonnet), premium (Claude Opus). Target: \>60% of tasks routed locally.

  ------------------------ --------------------------------------------------------- ------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------- -------------------------------- ------------
  **Tier**                 **Model(s)**                                              **Tasks**                                                                                                                                                                                                                             **Cost**                         **Volume**
  **LOCAL**(Free)          Llama 3.1:8B, Phi-4-mini (3.8B), SmolLM3-3B, Qwen3.5-4B   Health checks, status monitoring, log parsing, simple classification, PUDDING label assignment, APQC tagging, data extraction, formatting, 0-10 scoring (structured), embedding generation (nomic-embed-text), simple summarisation   £0 (electricity \~£5-10/month)   **60-70%**
  **STANDARD**(Cheap)      GPT-4.1-mini, DeepSeek-V3.2, Gemini Flash                 Multi-step reasoning, agent coordination, code generation, financial analysis, research synthesis, internal agent comms, gap analysis, SOP drafting                                                                                   \~£0.001-0.005 per call          **20-30%**
  **PREMIUM**(Expensive)   Claude Sonnet 4, Claude Opus 4, GPT-5                     Client-facing content, complex architectural decisions, high-stakes analysis, Pudding mixing sessions, radical attribution verification, gold-standard research, strategy documents                                                   \~£0.01-0.05 per call            **5-10%**
  ------------------------ --------------------------------------------------------- ------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------- -------------------------------- ------------

**The Routing Decision in Three Questions**

**1. Does it need reasoning?** NO → Local. This single filter eliminates 60% of cloud costs.

**2. Is it external-facing or high-stakes?** YES → Premium.

**3. Everything else → Standard.**

**Fallback Chain**

Local fails → Standard. Standard rate-limited → queue and retry. Premium fails → Standard with quality flag.

**3. Hugging Face Models to Pull Into Ollama**

Specific recommendations for expanding the local model roster, all available via Ollama or direct Hugging Face download. These fill the gaps in the current setup: structured output, lightweight classification, and multimodal processing.

  ---------------------------------- ---------------- ---------------------------------------------------------------------------------- ------------------------------------------------------------------------------------------------------------------ ----------------------------
  **Model**                          **Size**         **Good For**                                                                       **Why This One**                                                                                                   **Ollama Command**
  **Phi-4-mini-instruct**            3.8B             Structured output, function calling, JSON generation, PUDDING labelling, scoring   MIT license. Reasoning comparable to 7-9B models. Excellent at structured output and following specific formats.   ollama pull phi4-mini
  **SmolLM3-3B**                     3B               General instruction following, classification, summarisation                       Fully open (Hugging Face). Outperforms Llama-3.2-3B across 12 benchmarks. Full engineering blueprint published.    ollama pull smollm3:3b
  **Qwen3.5-4B**                     4B               Multimodal (text + image + video), long context (262K tokens), multilingual        Apache 2.0. 200+ languages. Long context for agent workflow traces. Thinking and non-thinking modes.               ollama pull qwen3.5:4b
  **Gemma-3n-E2B-IT**                \~5B (2B eff.)   Multimodal on-device (text, image, audio, video), real-time processing             Google DeepMind. Selective parameter activation --- runs like a 2B model. Mobile-optimised vision encoder.         ollama pull gemma3n:e2b
  **Llama 3.1:8B (installed)**       8B               General reasoning, longer tasks, agent backbone                                    Already running. 39 tok/s warm on Beast. Good for medium-complexity local work.                                    Already installed
  **Llama 3.1:70B (installed)**      70B              Complex local reasoning, fallback for when 8B isn\'t enough                        Already running. Uses more RAM but handles tasks that smaller models can\'t.                                       Already installed
  **nomic-embed-text (installed)**   N/A              Embedding generation for vector search                                             Already running. Keep for all embedding tasks.                                                                     Already installed
  **Mistral Small 3**                24B              Balanced reasoning + speed for mid-tier local tasks                                Good instruction following. Integrated with Ollama. Fast inference on consumer GPUs.                               ollama pull mistral-small3
  ---------------------------------- ---------------- ---------------------------------------------------------------------------------- ------------------------------------------------------------------------------------------------------------------ ----------------------------

**Priority Order for Pulling New Models**

**1. Phi-4-mini-instruct** --- covers the structured output gap. The scoring and labelling pipeline needs this.

**2. SmolLM3-3B** --- lightweight general tasks: health checks, classification, simple extraction.

**3. Qwen3.5-4B** --- multimodal + long context: useful for processing vault documents with images.

**RAM Allocation Estimate on Beast (256GB Total)**

  --------------------------------------- --------------------------------------------
  **Component**                           **RAM Usage**
  Ollama allocation                       96GB allocated
  Llama 3.1:70B                           \~40GB
  Llama 3.1:8B                            \~5GB
  nomic-embed-text                        \~1GB
  Phi-4-mini (3.8B)                       \~3GB
  SmolLM3-3B                              \~2.5GB
  Qwen3.5-4B                              \~3.5GB
  **Total with new models**               **\~55GB --- well within 96GB allocation**
  **Headroom for concurrent inference**   **\~40GB remaining**
  --------------------------------------- --------------------------------------------

**4. The Research Framework --- The Far End of a Thought**

This is the systematic framework for knowing when research is deep enough. It feeds directly into the Kaizen loop from the Build Quality Framework.

**The Research Depth Scale (0-5)**

  ----------- ------------------- ------------------------------------------------------------------------------------------------------------------------ --------------------------------------------------------------------------------------------
  **Level**   **Name**            **Description**                                                                                                          **When to Stop Here**
  0           **Uninformed**      No research done. Working from memory/assumption.                                                                        Never acceptable for anything going into production.
  1           **Surface**         One search, first-page results only. General awareness.                                                                  Acceptable for: quick sanity checks, \"does this exist?\" questions.
  2           **Informed**        3+ sources consulted. Multiple angles explored. Key facts verified.                                                      Acceptable for: internal documentation, SOPs, non-client-facing work.
  3           **Deep**            Success AND failure patterns researched. Named techniques extracted. Best-in-class identified. Gap analysis done.        Acceptable for: client-facing work, product features, the Build Quality Framework scoring.
  4           **Exhaustive**      Triple search (3+ engines). Cross-domain Pudding applied. Academic/primary sources consulted. Contradictions resolved.   Acceptable for: architectural decisions, Layer 0 changes, IP-critical work.
  5           **Gold Standard**   Peer-reviewed or primary-source verified. Tested against real data. Attribution complete.                                Only needed for: published claims, legal/compliance, investment-grade analysis.
  ----------- ------------------- ------------------------------------------------------------------------------------------------------------------------ --------------------------------------------------------------------------------------------

**The Diminishing Returns Test (When to STOP)**

**Ask these five questions. If 3+ are YES, stop researching:**

1\. Are you finding the same information repeated across different sources?

2\. Have you found both success AND failure patterns for this topic?

3\. Can you name at least 3 specific techniques (not just general concepts)?

4\. Would another search add COMPLEXITY rather than CLARITY?

5\. Do you have enough to write a testable hypothesis or actionable SOP?

**The \"Far End of a Thought\" Rule**

A thought has a natural boundary. You hit it when:

**Saturation:** The next search returns information you\'ve already seen.

**Pattern completion:** You can predict what the next source will say.

**Economic boundary:** The marginal value of one more search is less than the cost of that search.

**Research Depth by Task Type**

  ------------------------------------------- -----------------------------------------------------------
  **Task Type**                               **Required Depth**
  Local model research (scoring, labelling)   Level 1-2. Don\'t spend premium tokens on classification.
  Process improvement research                Level 3 default. Always success + failure patterns.
  Architectural decisions                     Level 4 minimum. Cross-domain Pudding mandatory.
  Published/client-facing claims              Level 5. No exceptions.
  ------------------------------------------- -----------------------------------------------------------

**5. How the Research Framework Feeds the Kaizen Loop**

**The Cycle**

The research depth level determines how many tokens each improvement cycle consumes. The cycle proceeds as follows:

> RESEARCH (to specified depth level)
>
> → EXTRACT named techniques
>
> → SCORE each 0-10 (using local model for structured scoring)
>
> → IDENTIFY gaps (what\'s below 7?)
>
> → RESEARCH gaps deeper (one level up)
>
> → IMPROVE (implement changes)
>
> → TEST (Kaizen + Chaos + Logic)
>
> → MEASURE (did the score improve?)
>
> → REPEAT until score \>= target

**Cost Per Atom by Research Level**

  -------------------- -------------------------------------------------------------------
  **Research Level**   **Estimated Cost per Atom**
  Level 1-2 research   \~£0.02-0.10 per atom (mostly local models)
  Level 3 research     \~£0.15-0.50 per atom (mix of local + standard API)
  Level 4 research     \~£1-3 per atom (premium API + multiple searches)
  Level 5 research     \~£5-15 per atom (extensive verification, multiple premium calls)
  -------------------- -------------------------------------------------------------------

**The Economic Argument**

**For a corpus of 1,000 atoms at Level 3 average: \~£150-500 total.**

**Compare to doing everything at Level 4-5 on premium API: \~£5,000-15,000.**

The research framework is how you spend £3,000 making things right instead of £15,000 making things expensive.

**6. Agent Architecture for Task Routing**

This section addresses using agents of different sizes and different companies at every level --- with strict remit but blinkers-without-ceilings when appropriate.

**The Bounded/Creative Routing Rule**

  ------------------------------------ ---------- ------------------------------------------------ --------------------------------------
  **APQC Category**                    **Mode**   **Default Model Tier**                           **Can Escalate?**
  4\. Deliver Products/Services        Bounded    Standard                                         Yes, to Premium with justification
  5\. Manage Customer Service          Bounded    Standard                                         Yes, to Premium for escalation
  8\. Manage Financial Resources       Bounded    Standard                                         Yes, to Premium for complex analysis
  10\. Manage Risk/Compliance/Ethics   Bounded    **Premium**                                      **No downgrade allowed**
  1\. Develop Vision/Strategy          Creative   **Premium**                                      N/A --- always premium
  2\. Develop Products/Services        Creative   Standard → Premium cascade                       Yes
  3\. Market and Sell                  Creative   Standard for drafts, Premium for publish         Yes
  6\. Develop Human Capital            Creative   Local for classification, Standard for content   Yes
  13\. Manage Knowledge/Improvement    Creative   Local for scoring, Standard for synthesis        Yes
  ------------------------------------ ---------- ------------------------------------------------ --------------------------------------

**The R&D Department (Sandbox)**

Creative/blinkers-off work happens in the R&D sandbox, then is tested before crossing into production. This maps to:

**R&D network:** rd-sandbox (isolated Docker network, no production access)

**Freedom:** R&D can use ANY model at ANY tier (creative freedom)

**Gate:** Output must pass quality gates before entering production departments

**Enforcement:** The Enforcer checks gate compliance every 10 minutes

**Nothing from R&D enters production without:**

• PRS \>= 7.0

• Attribution complete

• Integration test passed

**7. The Token Budget**

Monthly token budget allocation, targeting \~£500-800/month operational:

  ----------------------------- -------------------- -------------------- ----------------------------------------------
  **Category**                  **Monthly Budget**   **Model Tier**       **Notes**
  Health checks / monitoring    **£0**               Local                Hundreds of checks/day, all free
  Content scoring & labelling   **£0**               Local (Phi-4-mini)   Structured output, no reasoning needed
  Embedding generation          **£0**               Local (nomic)        Already running
  Process research (Kaizen)     £100-200             Standard + Premium   Level 3 research, 200-500 atoms/month
  Agent coordination            £50-100              Standard             Internal agent-to-agent
  Client-facing content         £100-200             Premium              Blog posts, reports, communications
  Code generation (Cove)        £100-200             Standard + Premium   Temporal workflows, bug fixes
  Pudding sessions              £50-100              Premium              Cross-domain discovery --- worth every penny
  Architecture decisions        £50-100              Premium              Infrequent but high-value
  **Total operational**         **£450-900/month**                        
  ----------------------------- -------------------- -------------------- ----------------------------------------------

**Plus: Perplexity/Computer credits for strategic work** --- this is where the £3,000 goes. High-value research, document creation, system design. Not health checks.

**8. Implementation Checklist**

Immediate actions, in priority order:

**1. Pull Phi-4-mini into Ollama**

Covers the structured output gap for scoring/labelling.

> ssh root\@135.181.161.131
>
> docker exec ollama ollama pull phi4-mini

**2. Pull SmolLM3-3B into Ollama**

Lightweight general tasks.

> docker exec ollama ollama pull smollm3:3b

**3. Update LiteLLM Config**

Add new local model aliases:

> \- model\_name: local/phi4-mini
>
> litellm\_params:
>
> model: ollama/phi4-mini
>
> api\_base: http://ollama:11434
>
> \- model\_name: local/smollm3-3b
>
> litellm\_params:
>
> model: ollama/smollm3:3b
>
> api\_base: http://ollama:11434

**4. Add Routing Rules to LiteLLM**

Route scoring/labelling/classification to local/phi4-mini. Route health checks and simple extraction to local/smollm3-3b.

**5. Implement the Research Depth Scale**

Add it to the Build Quality Framework as the standard for all research tasks. Every research request must specify a target depth level.

**6. Set Up Langfuse Cost Tracking by Tier**

Tag every LLM call with its tier (local/standard/premium) so you can see exactly where tokens are going each week. Dashboard view: cost by tier, cost by APQC category, cost per atom.

**7. Run a 1-Week Pilot**

Route all scoring/labelling through Phi-4-mini. Measure quality vs Sonnet. If quality holds (within 0.5 points on 0-10 scale), make it permanent. Expected saving: £200-400/month on scoring alone.

**Attribution**

**Originator:** Ewan Bramley (cost analysis, strategic direction)

**Formaliser:** Computer / Perplexity

**Research Sources**

OpenClaw hybrid cost strategy (marchingdogs.com, Feb 2026)

LogRocket LLM routing guide (Feb 2026)

BentoML SLM comparison (Mar 2026)

ASQ DMAIC methodology

Amplified Build Quality Framework v1.0

**Fact %:** 80 \| **Confidence:** High \| **PUDDING Label:** M.=.5.l (Meta, Stable, System-scale, Long-duration)

**LBD:** Swanson (1986) ABC Model

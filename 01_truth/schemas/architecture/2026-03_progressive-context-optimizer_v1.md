---
title: "Progressive Context Optimizer"
id: "progressive-context-optimizer"
version: 1
created: 2026-04-25
last_validated: 2026-04-25
type: document
topic_type: reference
status: imported
source_file: "progressive_context_optimizer.docx"
signed_by: "Devon, 2026-04-25, devin-992682c244cf444f91e0a516498afbfd"
---

**AMPLIFIED PARTNERS**

**Progressive Context Optimizer**

MCP Context Efficiency Code Plan

Solving the MCP context window bloat problem using existing Amplified Partners infrastructure: token-proxy interception, gatekeeper taxonomy classification, and progressive tool discovery.

  ---------------- -------------------------------
  Version          **1.0**
  Date             **17 March 2026**
  Classification   **Internal / Technical**
  Owner            **Ewan / Amplified Partners**
  ---------------- -------------------------------

**Table of Contents**

**Executive Summary**

**The Problem**

MCP tool definitions consume 55,000+ tokens for just 3 services (\~40 tools)[^1] --- over 25% of Claude\'s 200k context window. One team reported 143,000 of 200,000 tokens (72%) burned on schemas alone. Scalekit benchmarks confirm MCP costs 4-32x more tokens than CLI for identical operations.[^2]

For Amplified Partners running \~29 Docker containers with multiple MCP servers (graphiti-mcp, falkordb-brain, call-webhook, etc.), this is an existential constraint on agent capability. Every token spent on tool definitions is a token stolen from reasoning, retrieval, and response quality.

**The Solution**

The Progressive Context Optimizer (PCO) is a three-layer system that intercepts, classifies, and progressively discloses MCP tool definitions --- built entirely on existing Amplified code:

-   **Token Proxy Intercept Layer** (anthropic-token-proxy) --- catches all LLM calls, measures context burn, injects only needed tools

-   **Gatekeeper Taxonomy Layer** (gatekeeper-agent) --- classifies tools using the existing 5-axis taxonomy, enabling smart filtering

-   **Progressive Discovery Layer** (new module, using amplified-core patterns) --- serves tool definitions on-demand at three fidelity levels

+--------------------------+------------------------------+-------------------------+
| **70--90%**              | **\~100**                    | **0**                   |
|                          |                              |                         |
| Context Window Reclaimed | Bootstrap Tokens (from 55k+) | New Containers Required |
+--------------------------+------------------------------+-------------------------+

+---------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------+
| **Key Insight**                                                                                                                                                                                                                                                     |
|                                                                                                                                                                                                                                                                     |
| Progressive tool discovery is production-validated across major platforms (MCP, Cloudflare Code Mode, OpenAI, LangChain). The pattern reduces initial context consumption by 70-90%.                                                                                |
|                                                                                                                                                                                                                                                                     |
| Amplified\'s existing token-proxy already intercepts every Anthropic API call --- making it the natural insertion point. The gatekeeper\'s 5-axis taxonomy already classifies by domain and mechanism --- extending it to classify tools requires minimal new code. |
+---------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------+

**Architecture**

**System Overview**

The PCO operates as middleware inside the existing anthropic-token-proxy, with classification support from the gatekeeper-agent. No new Docker containers are needed --- the optimizer runs within the existing infrastructure.

  ---------------------------- ---------------------------------------------- --------------------------------------------- --------------------------------------------------------- --------------------------------------------------------- ------------------------------------------
  **User Request**             **→ amplified-core**                           **→ token-proxy**                             **→ PCO Layer**                                           **→ Claude API**                                          **→ Response**
  Voice, WhatsApp, Chat, API   MCP Gateway, mcpBarrier auth, identity vault   Semantic cache, prompt cache, model routing   Tool Registry, Gatekeeper Index, Progressive Disclosure   Optimized tool set injected (5k-15k tokens vs 55k-143k)   Usage tracked, analytics fed back to PCO
  ---------------------------- ---------------------------------------------- --------------------------------------------- --------------------------------------------------------- --------------------------------------------------------- ------------------------------------------

**Integration Points**

Every component of the PCO maps to existing code. The table below shows what exists, what is new, and how they connect.

  --------------------------- ----------------------------------------------------------------------------------------- ------------------------------ -------------------------------------------------------------------
  **Component**               **Existing Code**                                                                         **New Addition**               **Integration**
  **anthropic-token-proxy**   FastAPI proxy, prompt caching, semantic caching (Qdrant), model routing, budget control   Context Optimizer middleware   New middleware in request pipeline, before prompt cache
  **gatekeeper-agent**        5-axis taxonomy, QualityChecker, classifier, qdrant\_manager, reflection loop             Tool Taxonomy Index            Import classifier module, extend taxonomy for tool classification
  **amplified-core**          MCP Gateway, mcpBarrier auth, identity vault, token system                                Tool Registry endpoint         New route on MCP Gateway for tool discovery
  **amplified-partners**      OpenClaw/PicoClaw configs, docker-compose, SOUL.md                                        PCO configuration YAML         Env vars + config alongside existing MCP server configs
  --------------------------- ----------------------------------------------------------------------------------------- ------------------------------ -------------------------------------------------------------------

**Component Design**

**Tool Registry**

The Tool Registry is the central cache of all MCP tool definitions, pre-classified and indexed. It lives inside the anthropic-token-proxy and provides three fidelity representations of every tool.

**How It Works**

1.  On startup, queries each configured MCP server for its tool list (tools/list)

2.  Stores full schema, compressed schema, and name-only representations

3.  Triggers gatekeeper classification for each tool

4.  Watches for tool list changes via MCP notifications/listChanged

5.  Pre-calculates token cost of each tool definition at each fidelity level

**Data Model: ToolEntry**

> \@dataclass
>
> class ToolEntry:
>
> server\_name: str \# e.g., \'graphiti-mcp\'
>
> tool\_name: str \# e.g., \'search\_nodes\'
>
> \# Three fidelity levels
>
> name\_only: str \# \~2-5 tokens
>
> name\_description: str \# \~15-30 tokens
>
> full\_schema: dict \# \~200-2000 tokens
>
> \# Pre-calculated token costs
>
> tokens\_name: int
>
> tokens\_desc: int
>
> tokens\_full: int
>
> \# Gatekeeper classification (5-axis)
>
> domain: str \# knowledge-graph, communication\...
>
> mechanism: str \# retrieval, mutation, analysis\...
>
> source: str \# falkordb, graphiti, whatsapp\...
>
> status: str \# stable, experimental, deprecated
>
> \# Usage analytics
>
> call\_count\_24h: int
>
> avg\_tokens\_saved: float
>
> last\_used: datetime

**Existing Code Reuse**

-   **Token counting:** anthropic-token-proxy already counts tokens for billing --- reuse count\_tokens() utility

-   **Qdrant:** semantic cache already uses Qdrant for similarity search --- reuse for tool-query matching

-   **Cost attribution:** existing per-model cost tracking --- extend to track context-efficiency savings

**Gatekeeper Taxonomy Index**

Every MCP tool is classified using the existing 5-axis taxonomy from gatekeeper-agent[^3], enabling the Progressive Disclosure Engine to make intelligent decisions about which tools to surface.

**Classification Pipeline**

1.  Tool Registry ingests a new tool definition

2.  Definition sent to Gatekeeper classifier (existing pipeline)

3.  Classifier assigns Domain, Mechanism, Source, Status labels

4.  Classification stored in Qdrant alongside tool embedding

5.  QualityChecker runs hard gates: stability, auth, SMB-appropriateness

6.  Reflection loop self-checks classification accuracy

**Taxonomy Extensions for Tools**

  --------------- ------------ ---------------------------------------------------------------- --------------------------------------
  **Axis**        **Source**   **Example Labels**                                               **Purpose**
  **Domain**      Existing     knowledge-graph, communication, memory, analytics, voice, auth   Group tools by business capability
  **Mechanism**   Existing     retrieval, mutation, analysis, generation, notification          Distinguish read vs write operations
  **Source**      Existing     graphiti-mcp, falkordb-brain, whatsapp, telegram                 Track tool provenance
  **Status**      Existing     stable, experimental, deprecated, maintenance                    Quality gating
  **Frequency**   New          high, medium, low, rare                                          Usage-based prioritisation
  **Cost**        New          cheap, moderate, expensive                                       Token cost of full schema
  **Cluster**     New          (dynamically generated)                                          Tools that co-occur in conversations
  --------------- ------------ ---------------------------------------------------------------- --------------------------------------

**PUDDING Labels for Tools**

Extending the existing PUDDING labeling system to tool classification:

  ------------ ----------------- -------------------------------------------------------------------------------------
  **Letter**   **Dimension**     **For Tools**
  **P**        **Purpose**       What does this tool do? (extracted from tool description)
  **U**        **Usage**         How often is it called? (from usage analytics, call\_count\_24h)
  **D**        **Domain**        Which business domain? (from gatekeeper taxonomy axis)
  **D**        **Dependency**    What other tools commonly co-occur with this one?
  **I**        **Integration**   How does it connect to infrastructure? (MCP server, Docker container, external API)
  **N**        **Novelty**       Is this new/experimental or mature/stable? (from status axis)
  **G**        **Governance**    Auth requirements, rate limits, cost implications, SOUL principle alignment
  ------------ ----------------- -------------------------------------------------------------------------------------

**Progressive Disclosure Engine**

The core intelligence layer. It decides which tools to inject at which fidelity level based on conversation context. This pattern is production-validated across major platforms, showing 70-90% context reduction[^4].

**Three Disclosure Levels**

  ---------------------- ------------------------------------------- ----------------- ----------------------------------
  **Level**              **Content**                                 **Tokens/Tool**   **When**
  **L0: Manifest**       Tool names grouped by domain                \~2-5             Always injected (bootstrap)
  **L1: Descriptions**   Name + one-line description                 \~15-30           When user intent matches domain
  **L2: Full Schema**    Complete inputSchema with types and enums   \~200-2000        When agent selects specific tool
  ---------------------- ------------------------------------------- ----------------- ----------------------------------

**Decision Logic**

The engine follows a four-step process on every request:

1.  Always include L0 manifest (\~50-100 tokens total for all tools)

2.  Analyse conversation context to infer needed domains (using Qdrant semantic search)

3.  Promote matching domain tools to L1 (descriptions visible)

4.  If agent explicitly requests a tool or discover\_tools returns it, promote to L2 (full schema)

+--------------------------------------------------------------------------------------------------------------------+
| **Budget Enforcement**                                                                                             |
|                                                                                                                    |
| The engine never exceeds the configured tool\_budget for the active model.                                         |
|                                                                                                                    |
| Priority order: L2 tools first (agent actively needs them), then L1 by relevance score, then remaining L0 entries. |
|                                                                                                                    |
| If budget is tight, L1 candidates are dropped before L2 actives are demoted.                                       |
|                                                                                                                    |
| Auto-demotion: if an L2 tool goes unused for 3 turns, it drops back to L1.                                         |
+--------------------------------------------------------------------------------------------------------------------+

**Token Budget Allocation**

The PCO fundamentally restructures how the context window is used:

  ------------------------- ------------------------ -------------------------
  **Context Region**        **Before PCO**           **After PCO**
  System prompt             \~2,000 tokens           \~2,000 tokens
  **Tool definitions**      55,000-143,000 tokens    5,000-15,000 tokens
  Conversation history      \~30,000-50,000 tokens   \~50,000-100,000 tokens
  Retrieved context (RAG)   \~10,000-30,000 tokens   \~30,000-50,000 tokens
  Reasoning + response      \~10,000-30,000 tokens   \~30,000-50,000 tokens
  ------------------------- ------------------------ -------------------------

**The discover\_tools Meta-Tool**

Instead of loading all tool schemas upfront, we give the agent a single meta-tool that discovers other tools on demand. This single tool definition costs \~150 tokens, compared to 55,000+ for loading all 40 tools directly[^5].

> {
>
> \"name\": \"discover\_tools\",
>
> \"description\": \"Search available tools by capability,
>
> domain, or name. Returns tool descriptions at the
>
> requested detail level.\",
>
> \"inputSchema\": {
>
> \"properties\": {
>
> \"query\": {
>
> \"type\": \"string\",
>
> \"description\": \"What capability are you looking
>
> for? e.g. search knowledge graph\"
>
> },
>
> \"detail\_level\": {
>
> \"type\": \"string\",
>
> \"enum\": \[\"names\", \"descriptions\", \"full\_schema\"\],
>
> \"default\": \"descriptions\"
>
> },
>
> \"domain\": {
>
> \"type\": \"string\",
>
> \"description\": \"Optional: knowledge-graph,
>
> communication, memory, analytics, voice, auth\"
>
> }
>
> },
>
> \"required\": \[\"query\"\]
>
> }
>
> }

**Middleware Pipeline**

The PCO slots into the existing anthropic-token-proxy request pipeline. The key placement decision: the Context Optimizer runs before the prompt cache, which means optimized tool sets produce better cache hit rates.

**Pipeline: Before and After**

  ---------- -------------------------------- ----------------------------------
  **Step**   **Current Pipeline**             **PCO Pipeline**
  **1**      Auth (API key validation)        Auth (API key validation)
  **2**      Rate limiting                    Rate limiting
  **3**      Semantic cache check (Qdrant)    Context Optimizer (NEW)
  **4**      Prompt cache check               Semantic cache check
  **5**      Model routing (Sonnet → Haiku)   Prompt cache check (better hits)
  **6**      Forward to Claude API            Model routing
  **7**      Cost attribution                 Forward to Claude API
  **8**      ---                              Tool usage tracking (NEW)
  **9**      ---                              Cost attribution (+ savings)
  ---------- -------------------------------- ----------------------------------

+---------------------------------------------------------------------------------------------------------------------------------------------------------+
| **Why Before Prompt Cache?**                                                                                                                            |
|                                                                                                                                                         |
| If we reduce tool definitions before caching, we get better prompt cache hit rates --- fewer tools means more conversations share the same tool prefix. |
|                                                                                                                                                         |
| This compounds the savings: not only do we use fewer tokens per request, but more requests hit the cache (reducing API costs further).                  |
|                                                                                                                                                         |
| The existing semantic cache in Qdrant is also more effective because the tool context is smaller and more focused.                                      |
+---------------------------------------------------------------------------------------------------------------------------------------------------------+

**Implementation Plan**

**Phase 1: Tool Registry and Token Measurement**

Week 1. Build the central registry inside anthropic-token-proxy.

**New Files**

> anthropic-token-proxy/
>
> ├── app/
>
> │ ├── context\_optimizer/
>
> │ │ ├── \_\_init\_\_.py
>
> │ │ ├── tool\_registry.py \# ToolEntry, CRUD
>
> │ │ ├── tool\_ingester.py \# MCP tools/list polling
>
> │ │ ├── token\_counter.py \# Wraps existing counter
>
> │ │ └── config.py \# PCO config
>
> │ └── main.py \# MODIFY: startup hook

**Tasks**

1.  Create tool\_registry.py --- ToolEntry dataclass, in-memory store backed by Qdrant

2.  Create tool\_ingester.py --- connect to each MCP server in docker-compose, fetch tools/list

3.  Create token\_counter.py --- extend existing token counting for fidelity-level pre-calculation

4.  Build compressed schema generator --- strip descriptions, minify enums, remove examples

5.  Add startup hook in main.py --- populate registry before accepting requests

**Existing Code Reuse**

-   **app/cache/** --- semantic cache infrastructure (Qdrant client, embedding functions)

-   **app/routing/** --- model routing logic (knows available models and their context limits)

-   **app/billing/** --- token counting, cost-per-model calculations

**Phase 2: Gatekeeper Tool Classification**

Week 1-2. Extend the existing gatekeeper classification pipeline for MCP tools.

**New Files**

> gatekeeper-agent/
>
> ├── classifiers/
>
> │ ├── tool\_classifier.py \# NEW: MCP tool classification
>
> │ └── \...existing classifiers\...
>
> ├── taxonomy/
>
> │ ├── tool\_taxonomy.py \# NEW: tool-specific extensions
>
> │ └── \...existing taxonomy\...
>
> ├── quality\_checker.py \# MODIFY: tool quality gates
>
> └── qdrant\_manager.py \# MODIFY: tool\_index collection

**Tasks**

1.  Create tool\_classifier.py --- wraps existing classifier for tool definitions

2.  Extend taxonomy with Frequency, Cost, and Cluster labels

3.  Add tool\_index collection to Qdrant (alongside existing knowledge collections)

4.  Add tool-quality hard gates: stability, auth requirements, SMB-appropriateness

5.  Build co-occurrence tracker: which tools are typically used together?

**Phase 3: Progressive Disclosure Engine**

Week 2. The core intelligence layer --- decides which tools to inject at which fidelity level.

**New Files**

> anthropic-token-proxy/
>
> ├── app/
>
> │ ├── context\_optimizer/
>
> │ │ ├── progressive\_disclosure.py \# PDE core
>
> │ │ ├── domain\_inferrer.py \# Conversation → domain
>
> │ │ ├── budget\_allocator.py \# Token budgets
>
> │ │ └── discover\_tool.py \# Meta-tool MCP server
>
> │ ├── middleware/
>
> │ │ ├── context\_optimizer\_mw.py \# NEW: intercept + inject
>
> │ │ └── \...existing middleware\...

**Key Integration**

-   **Domain inference:** uses existing Qdrant semantic search to match conversation embeddings against tool domain embeddings

-   **Budget allocation:** reads model context limits from existing routing config; enforces per-model tool budgets

-   **Prompt cache synergy:** smaller, more consistent tool sets improve cache key stability and hit rates

**Phase 4: Configuration and Docker Integration**

Week 2-3. Wire everything into the existing Docker/Beast infrastructure.

**PCO Configuration (pco.yaml)**

> optimizer:
>
> enabled: true
>
> budgets:
>
> claude-sonnet-4:
>
> max\_context: 200000
>
> tool\_budget: 12000 \# 6% (was 25-72%)
>
> l0\_budget: 150
>
> l2\_max\_tools: 5
>
> claude-haiku-3:
>
> max\_context: 200000
>
> tool\_budget: 8000
>
> l2\_max\_tools: 3
>
> discovery:
>
> meta\_tool\_enabled: true
>
> auto\_promote\_threshold: 0.85
>
> auto\_demote\_after: 3 \# turns without use
>
> co\_occurrence\_boost: 0.15
>
> servers:
>
> \- name: graphiti-mcp
>
> url: http://graphiti-mcp:8000
>
> priority: high
>
> \- name: falkordb-brain
>
> url: http://falkordb-brain:7688
>
> priority: high
>
> \- name: call-webhook
>
> url: http://call-webhook:3000
>
> priority: medium

**Docker Integration**

No new containers. The PCO runs inside the existing anthropic-token-proxy container:

> \# docker-compose.yml addition:
>
> anthropic-token-proxy:
>
> environment:
>
> \- PCO\_ENABLED=true
>
> \- PCO\_CONFIG\_PATH=/config/pco.yaml
>
> \- PCO\_TOOL\_BUDGET\_DEFAULT=12000
>
> \- PCO\_GATEKEEPER\_URL=http://gatekeeper-agent:8000
>
> volumes:
>
> \- ./configs/pco.yaml:/config/pco.yaml

**Phase 5: Rollout Strategy**

Three-stage rollout to minimise risk:

  ------------------ -------------- ----------------------------------------------------------------------------------- ----------------------------------------------------------------------------------
  **Stage**          **Timeline**   **Behaviour**                                                                       **Success Criteria**
  **Shadow Mode**    Week 1         PCO calculates optimised tool set but does not apply it. Logs comparison metrics.   Metrics show predicted savings of 60%+ without false negatives
  **Canary Mode**    Week 2         Applied to 10% of requests via existing A/B logic in token-proxy.                   Tool selection accuracy stays above 95%. No task failures from missing tools.
  **Full Rollout**   Week 3         Enabled for all requests. 48-hour observation window.                               Stable for 48h. Token savings match shadow predictions. Cache hit rate improves.
  ------------------ -------------- ----------------------------------------------------------------------------------- ----------------------------------------------------------------------------------

**Testing Strategy**

Following the Amplified Methodology Framework (AMF) testing approach with Kaizen progression levels.

**Unit Tests (Kaizen 1-3)**

  -------------------------------------- -----------------------------------------------------------------------------------------------------------------------------------------------
  **Test File**                          **Test Cases**
  **test\_tool\_registry.py**            Ingest from MCP server; three fidelity levels; token count accuracy (within 5%); compressed schema generation; registry update on listChanged
  **test\_tool\_classifier.py**          Domain classification; mechanism classification; quality gates pass (stable tools); quality gates fail (deprecated tools)
  **test\_progressive\_disclosure.py**   L0 manifest always present; L1 promotion on domain match; L2 promotion on explicit request; budget enforcement; demotion after unused turns
  **test\_budget\_allocator.py**         Sonnet budget; Haiku budget; overflow graceful degradation (falls back to full injection)
  -------------------------------------- -----------------------------------------------------------------------------------------------------------------------------------------------

**Integration Tests (Kaizen 4-6)**

  -------------------------------------- --------------------------------------------------------------------------------------------------------------------------
  **Test File**                          **Test Cases**
  **test\_proxy\_pipeline.py**           Request flows through optimizer; prompt cache works after optimisation; cost attribution includes savings metric
  **test\_gatekeeper\_integration.py**   Tool classification end-to-end; Qdrant tool\_index queries return correct results
  **test\_mcp\_server\_discovery.py**    graphiti-mcp tools ingested; falkordb-brain tools ingested; discover\_tools returns correct results for semantic queries
  -------------------------------------- --------------------------------------------------------------------------------------------------------------------------

**Benchmark Tests (Kaizen 7-10)**

  --------------------------------- ----------------------------------------------------------------------------------------------------------------------
  **Test File**                     **Test Cases**
  **test\_token\_savings.py**       Baseline token count; optimised count; assert savings \>= 70%; savings by conversation type (voice, chat, scheduled)
  **test\_agent\_accuracy.py**      Tool selection accuracy (agent picks right tools); discovery latency (turns to find tool); false positive rate
  **test\_cache\_improvement.py**   Prompt cache hit rate before PCO; hit rate after PCO; assert improvement
  --------------------------------- ----------------------------------------------------------------------------------------------------------------------

**SOUL.md Alignment**

Every design decision in the PCO maps to Amplified\'s SOUL principles:

  -------------------------------- ----------------------------------------------------------------------------------------------------------------------
  **SOUL Principle**               **PCO Implementation**
  **1. Amplify, don\'t replace**   PCO amplifies MCP --- does not replace it. Tools still speak MCP protocol. Context is optimised, not removed.
  **2. SMB-first**                 Token savings directly reduce API costs for SMB clients. Less context burn = cheaper per conversation.
  **3. Voice-first ready**         Voice conversations have shorter context windows and faster turns --- PCO especially benefits voice-first workflows.
  **4. Transparent**               Every optimisation is logged. Agents can discover more tools. Nothing is hidden --- just deferred.
  **5. Composable**                PCO is a middleware module. Can be enabled/disabled per client, per model, per conversation.
  **6. Quality over speed**        Classification uses quality gates before surfacing tools. Fewer, correct tools over all tools noisily.
  **7. Learn and adapt**           Usage analytics feed back into classification. Frequently co-used tools get boosted. Rarely-used tools get demoted.
  -------------------------------- ----------------------------------------------------------------------------------------------------------------------

**Risk Assessment**

  ----------------------------------- -------------- ----------------------------------------------------------------------------------------------------------------------------------------------
  **Risk**                            **Severity**   **Mitigation**
  **Agent cannot find needed tool**   High           L0 manifest always shows ALL tool names. discover\_tools meta-tool available. Fallback: inject full tools after 2 failed discovery attempts.
  **Classification errors**           Medium         Gatekeeper reflection loop self-checks. Quality gates catch obvious errors. Manual override in pco.yaml.
  **Added discovery latency**         Medium         L0 manifest pre-computed (zero cost). Qdrant semantic search \<10ms. Only L2 promotion adds a step.
  **PCO middleware crash**            High           Circuit breaker: if PCO throws, bypass and inject full tool set (degraded mode). Log alert.
  **Prompt cache invalidation**       Medium         PCO runs before prompt cache → stabilises cache keys. Should improve, not hurt, cache rates.
  **Token count drift**               Low            Recalibrate token counter weekly against Anthropic\'s official counter.
  ----------------------------------- -------------- ----------------------------------------------------------------------------------------------------------------------------------------------

**Kaizen Pathway**

The PCO follows the AMF Kaizen progression from foundation through mastery.

  ---------------------- -------------------------------------------------------------------------------------------------------------------------------------------------------------------------
  **Level**              **Milestones**
  **1-3 Foundation**     Tool Registry ingests all MCP servers. Token counting works. Three fidelity levels generated. Basic unit tests pass.
  **4-6 Integration**    Gatekeeper classification working. Progressive disclosure logic complete. Middleware wired into proxy pipeline. Integration tests pass. Shadow mode running.
  **7-8 Optimisation**   Co-occurrence boosting working. Usage analytics feeding back. Benchmarks showing \>= 70% savings. Prompt cache improvement measured. Canary mode successful.
  **9-10 Mastery**       Full rollout stable for 1 week. Auto-tuning budgets by conversation type. Tool clustering discovered automatically. Cross-client learning. PUDDING scores all \>= 8/10.
  ---------------------- -------------------------------------------------------------------------------------------------------------------------------------------------------------------------

**Monitoring and Metrics**

Add to existing Grafana dashboards on the Beast:

-   **Token savings per conversation** --- before vs after PCO (primary KPI)

-   **Tool discovery success rate** --- percentage of tool calls where agent found the right tool

-   **L0/L1/L2 distribution** --- how tools are distributed across fidelity levels over time

-   **Prompt cache hit rate** --- before vs after (should improve with smaller tool sets)

-   **Discovery latency** --- extra turns needed to find tools (target: \<1 average)

-   **Fallback rate** --- how often circuit breaker fires (target: \<1% of requests)

-   **Cost savings** --- dollar value of reclaimed tokens (per conversation, daily, monthly)

**Timeline Summary**

  ------------- ---------------------------------------------------------------------------------------------- --------------------
  **Week**      **Deliverables**                                                                               **Kaizen Level**
  **Week 1**    Tool Registry, Token Measurement, Gatekeeper Classification (start)                            1-3 (Foundation)
  **Week 2**    Gatekeeper Classification (complete), Progressive Disclosure Engine, Middleware, Shadow Mode   4-6 (Integration)
  **Week 3**    Configuration, Docker integration, Canary Mode, Benchmarks, Full Rollout                       7-8 (Optimisation)
  **Week 4+**   Co-occurrence learning, auto-tuning, cross-client patterns, PUDDING evaluation                 9-10 (Mastery)
  ------------- ---------------------------------------------------------------------------------------------- --------------------

**Sources**

All research sources referenced throughout this document:

**1. Apideck,** Your MCP Server Is Eating Your Context Window (March 2026) --- <https://www.apideck.com/blog/mcp-server-eating-context-window-cli-alternative>

**2. Hacker News,** MCP Server Is Eating Your Context Window discussion (March 2026) --- <https://news.ycombinator.com/item?id=47400261>

**3. Agentic Patterns,** Progressive Tool Discovery pattern --- <https://agentic-patterns.com/patterns/progressive-tool-discovery/>

**4. MCPJam,** Claude Agent Skills: Progressive Disclosure vs MCP --- <https://www.mcpjam.com/blog/claude-agent-skills>

**5. Alex Salazar,** 10 Strategies to Reduce MCP Token Bloat (February 2026) --- <https://www.linkedin.com/posts/alexsalazar_10-strategies-to-reduce-mcp-token-bloat-activity-7425337457715601408-gcUE>

**6. Charles Chen,** MCP is Dead; Long Live MCP! (March 2026) --- <https://chrlschn.dev/blog/2026/03/mcp-is-dead-long-live-mcp/>

**7. Microsoft,** Official MCP C\# SDK v1.0 (March 2026) --- <https://devblogs.microsoft.com/dotnet/release-v10-of-the-official-mcp-csharp-sdk/>

**8. Scalekit,** MCP vs CLI Token Benchmarks (75 head-to-head comparisons) --- Referenced via Apideck and HN discussion

[^1]: Apideck, \'Your MCP Server Is Eating Your Context Window\' (March 2026), <https://www.apideck.com/blog/mcp-server-eating-context-window-cli-alternative>

[^2]: Hacker News discussion, \'MCP Server Is Eating Your Context Window\' (March 2026), <https://news.ycombinator.com/item?id=47400261>

[^3]: Agentic Patterns, \'Progressive Tool Discovery\', <https://agentic-patterns.com/patterns/progressive-tool-discovery/>

[^4]: Agentic Patterns, \'Progressive Tool Discovery\', <https://agentic-patterns.com/patterns/progressive-tool-discovery/>

[^5]: MCPJam, \'Claude Agent Skills: Progressive Disclosure\', <https://www.mcpjam.com/blog/claude-agent-skills>

---
title: "PCO Mycelial Network"
id: "pco-mycelial-network"
version: 1
created: 2026-04-25
last_validated: 2026-04-25
type: document
topic_type: reference
status: imported
source_file: "pco_mycelial_network.md"
signed_by: "Devon, 2026-04-25, devin-992682c244cf444f91e0a516498afbfd"
---

# The Mycelial Network: Open-Source PCO Ecosystem Map

**Amplified Partners — Internal Strategy Document**
**March 2026 · v2.0**

---

## How to Read This Document

This document is the output of deep ecosystem research into open-source context optimisation, agent memory, and the protocol standards that connect them. It maps the landscape that the Progressive Context Optimizer (PCO) will be born into — not as a market analysis, but as a network topology. The metaphor throughout is mycelium: the underground fungal network that connects trees in a forest, allowing them to share nutrients, send signals, and collectively respond to threats. No single tree is the forest. No single tool is the ecosystem. The value is in the connections.

The document is structured in seven sections:

1. **The Problem Space** — Why context management has become the defining challenge, and why everyone is building solutions simultaneously.
2. **The Protocol Stack** — The four-layer standard that the industry has converged on. This is the shared language.
3. **The Ecosystem Nodes** — 25+ open-source projects, each explained in depth: what they do, how they work, who built them, and what they connect to.
4. **The Hyphae** — The actual protocol connections, data flows, and dependency relationships between projects. This is the network map.
5. **The Convergence** — Seven architectural principles that the entire ecosystem is independently arriving at.
6. **PCO's Position** — Where PCO fits as a node in this network, what it does that nothing else does, and how it composes with existing tools.
7. **The Mycelial Strategy** — A phased plan for shipping PCO as a first-class citizen of this ecosystem.

Every claim is sourced. Every project link is real. Someone picking this document up cold should be able to understand the entire landscape, make architectural decisions, and know exactly what to build.

---

## 1. The Problem Space: Why Context Management Is the Defining Challenge

Every large language model has a finite context window — the total amount of text it can hold in working memory at any one time. As of March 2026, the largest commercially available windows are 200K tokens (Claude 3.5) and 1M tokens (Gemini 1.5 Pro), with the newly released [GPT-5.4 mini and nano models](https://openai.com) offering 400K token windows at reduced cost. These numbers sound enormous, but they are not enough.

The reason they are not enough is that production agents — the kind Amplified Partners builds for SMB clients — do not just answer single questions. They run multi-step workflows that accumulate context over time: tool call results, conversation history, retrieved documents, intermediate reasoning, error messages, retry attempts. A voice-first AI receptionist handling a 30-minute customer interaction with CRM lookups, calendar checks, and email drafts can consume 50,000-100,000 tokens of context before the conversation is halfway through. An agentic coding assistant working on a codebase migration can burn through 200,000 tokens in minutes.

When the context window fills up, one of three things happens: the model starts hallucinating (fabricating facts that sound plausible but are wrong), it loses track of its original goal (a phenomenon called "context rot" or "goal drift"), or the application crashes with a token limit error. All three are unacceptable in production.

This is not a theoretical concern. [Anthropic's context engineering guide](https://www.anthropic.com/engineering/effective-context-engineering-for-ai-agents) (September 2025) describes the problem as requiring agents that maintain "coherence, context, and goal-directed behavior" across tasks "spanning minutes to hours." [LangChain's Deep Agents blog post](https://blog.langchain.com/context-management-for-deepagents/) (January 2026) reports that their SDK triggers context compression when the window hits 85% capacity — and for complex tasks, this happens repeatedly, with the green line in their benchmark data showing "dramatic token drops" when summarisation events fire. [Google's ADK team](https://developers.googleblog.com/architecting-efficient-context-aware-multi-agent-framework-for-production/) (December 2025) describes the old approach — treating context as "a mutable string buffer" — as fundamentally broken, and proposes replacing it with a compiler-like pipeline that treats context as "a compiled view over a richer stateful system."

The result is that every major AI company and framework has independently arrived at the same conclusion: context management is not a feature, it is a discipline. Google calls it "context engineering." LangChain formalised it as a four-strategy framework (Write, Select, Compress, Isolate). Anthropic publishes engineering guides on it. And an entire open-source ecosystem has emerged to address it.

PCO is Amplified Partners' entry into this space. The question this document answers is: what does that ecosystem look like, how is it connected, and how does PCO plug in?

---

## 2. The Protocol Stack: The Shared Language

Before mapping individual projects, it is essential to understand the protocol layer that connects them. In the last 18 months, the AI agent ecosystem has converged on a four-layer standard — surprisingly quickly, and with surprising consensus.

### Layer 1: MCP (Model Context Protocol) — Agent ↔ Tools

MCP was created by Anthropic and [donated to the Linux Foundation's Agentic AI Foundation (AAIF) in December 2025](https://dev.to/pockit_tools/mcp-vs-a2a-the-complete-guide-to-ai-agent-protocols-in-2026-30li). It standardises how an AI agent connects to external tools, data sources, and services. Before MCP, every provider had its own method: OpenAI had function calling, Anthropic had tool use, Google had function declarations — each requiring different JSON schemas, different response formats, different error handling. If you built a Postgres connector for Claude, you could not reuse it for GPT without rewriting significant chunks.

MCP solved this by defining a universal protocol. An MCP server exposes capabilities (tools, resources, prompts) through a standard interface. An MCP client (the agent or IDE) discovers and calls those capabilities without caring about the implementation. As of March 2026, MCP has crossed **97 million monthly SDK downloads** (Python + TypeScript combined), with **5,800+ MCP servers** available in public registries. It has been adopted by every major AI provider: Anthropic, OpenAI, Google, Microsoft, Amazon. It is built into Claude Desktop, VS Code, Cursor, Windsurf, Zed, and all JetBrains IDEs.

The [MCP Registry](https://github.com/modelcontextprotocol/registry), which launched in preview in September 2025 and entered API freeze (v0.1) in October 2025, functions as an app store for MCP servers. The [GitHub MCP Registry](https://github.blog/changelog/2025-09-16-github-mcp-registry-the-fastest-way-to-discover-ai-tools/) launched alongside it as a curated discovery layer.

The [MCP roadmap](https://modelcontextprotocol.io/development/roadmap) (updated March 2026) includes scalable session handling (how sessions are created, resumed, and migrated) and MCP Server Cards (structured metadata via `.well-known` URLs for discovery). These features will make it possible for agents to discover PCO automatically.

**Why this matters for PCO:** MCP is not optional. It is the lingua franca. If PCO ships as an MCP server, it is instantly compatible with every MCP client — every IDE, every framework, every agent. If it does not, it is invisible to the ecosystem.

### Layer 2: A2A (Agent-to-Agent Protocol) — Agent ↔ Agent

A2A was [announced by Google in April 2025](https://developers.googleblog.com/en/a2a-a-new-era-of-agent-interoperability/) with input from over 50 industry partners. Where MCP handles agent-to-tool communication, A2A handles agent-to-agent communication — allowing independent agents to discover each other's capabilities, share tasks, and collaborate autonomously without human intervention.

A2A is built on HTTP, SSE, and JSON-RPC — standard web technologies. Agents publish "Agent Cards" that describe their capabilities, and other agents can discover and invoke them. IBM's Agent Communication Protocol (ACP) merged into A2A in August 2025, and A2A was donated to the AAIF in December 2025 alongside MCP.

A2A is designed to complement MCP, not compete with it. As [OneReach's analysis](https://onereach.ai/blog/what-is-a2a-agent-to-agent-protocol/) explains: "While MCP and ACP handle local interactions, the Agent-to-Agent Protocol extends collaboration across distributed systems, complementing the existing standards."

**Why this matters for PCO:** In a multi-agent system, PCO could be discoverable as an A2A agent that other agents delegate context management to. This is a future-state concern (P2 priority), but designing with A2A awareness from the start avoids expensive retrofitting later.

### Layer 3: AG-UI (Agent-User Interaction Protocol) — Agent ↔ User

AG-UI is the newest layer, [born from CopilotKit's partnership with LangGraph and CrewAI](https://www.codecademy.com/article/ag-ui-agent-user-interaction-protocol). It standardises how agents stream updates to user-facing applications — text tokens, tool execution progress, state synchronisation, and human-approval requests. It uses approximately 16 event types across five categories (Lifecycle, Text Messages, Tool Calls, State Management, Special Events) and supports HTTP, Server-Sent Events, and WebSockets.

AG-UI is already integrated with [LangGraph, CrewAI, Mastra, Pydantic AI, and Microsoft Agent Framework](https://docs.ag-ui.com/introduction) on the backend, and React, Vue, and Angular on the frontend. Production adoption by Microsoft and Oracle signals enterprise readiness.

**Why this matters for PCO:** AG-UI's state management events use a "snapshot-plus-delta" pattern to synchronise evolving content. PCO's compression operations — which transform conversation state — could emit AG-UI events so that frontends can show users what was compressed, what was preserved, and why. This creates transparency in an otherwise invisible process.

### Layer 4: WebMCP / llms.txt — Agent ↔ Web

The youngest and least mature layer. Sites publish `llms.txt` files and machine-readable versions of their content for agent consumption. Still early, but growing. Not directly relevant to PCO's architecture, but worth tracking.

### The Governance Layer: AAIF

All of this is underpinned by the [Agentic AI Foundation (AAIF)](https://dev.to/pockit_tools/mcp-vs-a2a-the-complete-guide-to-ai-agent-protocols-in-2026-30li), launched in December 2025 under the Linux Foundation with six co-founders: OpenAI, Anthropic, Google, Microsoft, AWS, and Block. Over 100 enterprises have joined as supporters. The significance is neutral governance — neither Anthropic nor Google controls the specs alone. Feature proposals go through open RFC processes. The two protocols (MCP and A2A) will evolve together, with tighter integration points expected.

---

## 3. The Ecosystem Nodes: 25+ Projects, Explained

The context management ecosystem clusters into six functional categories. Within each category, projects range from massive open-source platforms to experimental MCP servers. What follows is not a catalogue — it is an explanation of what each project does, why it exists, and how it connects to the rest of the network.

### 3.1 Memory Layers — The Soil

Memory layers provide long-term persistent storage for agent state. They are the substrate that everything else grows in. Without them, every conversation starts from zero.

#### Mem0 (24,000+ GitHub stars)

[Mem0](https://github.com/mem0ai/mem0) ("mem-zero") is a Y Combinator S24 graduate building what they call the "universal memory layer for AI agents." Their approach provides intelligent, persistent memory across sessions — exactly what most agent frameworks are missing.

Mem0's architecture uses **three levels of memory**. User-level memory captures individual preferences, interaction patterns, and historical context. Session-level memory maintains context within a single conversation or task. Agent-level memory lets the agent itself learn from past experiences, improving its problem-solving over time. Under the hood, it uses Qdrant as a vector store and supports optional graph memory for relationship-aware recall.

The results from their [research paper](https://muleai.io/blog/2026-03-11-mem0-ai-agent-memory-framework/) are significant: **+26% accuracy improvement** over OpenAI's built-in Memory on the LOCOMO benchmark, **91% faster responses** compared to full-context approaches, and **90% lower token usage** by avoiding redundant context.

Crucially for the mycelial network, Mem0 has built extensive integrations: LangChain, CrewAI, LangGraph, Mastra, CAMEL AI on the framework side; Azure OpenAI, AWS Bedrock and SageMaker on the provider side; Python and TypeScript SDKs. And they have shipped [OpenMemory MCP](https://mem0.ai/blog/introducing-openmemory-mcp) — a local-first, private memory server that runs entirely on your machine using Docker + Postgres + Qdrant. It exposes four standard MCP tools (`add_memories`, `search_memory`, `list_memories`, `delete_all_memories`) and includes a Next.js dashboard UI for observability. Any MCP client — Cursor, Claude Desktop, Windsurf, Cline — can connect and share persistent memory.

**PCO connection:** Mem0/OpenMemory is the natural persistence backend for PCO. Rather than building a vector store, PCO should compress the active conversation window and write evicted context to Mem0 via MCP. When old context is needed again, PCO queries Mem0 and selectively re-injects. This creates a hot/cold tier pattern — PCO manages the hot tier (active window), Mem0 manages the cold tier (persistent memory) — without either project duplicating the other's work.

#### Letta / MemGPT (37,000+ GitHub stars)

[Letta](https://github.com/letta-ai/letta) is the platform form of the MemGPT research paper that introduced the concept of the "LLM Operating System" for memory management. The core insight is borrowed from operating systems: just as an OS manages memory by swapping data between RAM and disk, an LLM agent can manage its context window by swapping information between the active context and external storage.

Letta agents control their own memory through function calls — they can read, write, search, and archive information. This makes memory management agentic rather than rule-based: the agent decides what to remember and what to forget, based on the task at hand.

In February 2026, Letta shipped [Context Repositories](https://www.letta.com/blog/context-repositories), a significant architectural evolution. Context Repositories store an agent's memory as a git-backed local filesystem. Every change to memory is automatically versioned with informative commit messages. The filesystem uses a hierarchical folder/file structure with YAML frontmatter describing contents (similar in spirit to Anthropic's SKILL.md convention). A `system/` directory pins files that are always loaded into the system prompt. Agents reorganise the hierarchy, update frontmatter, and move files to/from `system/` for dynamic context control.

The most innovative aspect is **concurrent subagent collaboration via git worktrees**. Each subagent gets an isolated git worktree to process and write memory in parallel. Changes are merged back to the "main" repository with standard git conflict resolution. This enables patterns like memory swarms, offline processing, and divide-and-conquer reflection without blocking the main agent.

Letta also acts as an [MCP client](https://github.com/letta-ai/letta), meaning it can connect to any MCP server and use its tools. This makes Letta + PCO (as MCP server) a natural composition.

**PCO connection:** Letta's Context Repositories represent the most sophisticated memory architecture in the ecosystem. PCO should study their progressive disclosure pattern (folder names + frontmatter as navigational signals) and their filesystem-as-memory approach. Where Letta manages long-term structured memory, PCO manages real-time compression of the active window — complementary, not competing.

#### Zep (3,000+ GitHub stars)

[Zep](https://www.getzep.com) takes a different approach: a **temporal context graph** that evolves with every interaction. When facts change, old ones are invalidated rather than deleted — maintaining a history of what was true and when. Zep fuses chat history, CRM data, app events, and documents into a unified graph, delivering assembled context through a single API call.

Zep's key technical differentiator is **retrieval speed**: under 200ms P95 latency, which makes it suitable for voice AI and other latency-sensitive applications. It supports progressive summarisation (condensing long conversation histories while preserving key information) and provides both semantic and temporal search.

The system uses context templates — structured formats that define what context to retrieve and how to format it for the LLM:

```
template: `# USER PROFILE
%{user_summary}
# RELEVANT FACTS
%{edges limit=10}
# RELEVANT ENTITIES
%{entities limit=2 types=[person,organization]}`
```

**PCO connection:** Zep's temporal graph approach is valuable for entity tracking — knowing what was true at what point in time. PCO could delegate entity-aware context retrieval to Zep while handling the compression/quality-verification layer itself. Zep's context templates are also worth studying as a reference for PCO's rubrik configuration.

#### SimpleMem (New, Academic Origin)

[SimpleMem](https://github.com/aiming-lab/SimpleMem) is a research project from the AIMING Lab that approaches memory from a compression-first perspective. Their three-stage pipeline is built on **semantic lossless compression**:

1. **Structured Semantic Compression** — Filters and de-linearises conversations into atomic, self-contained facts.
2. **Memory Indexing** — Organises compressed facts for efficient retrieval.
3. **Adaptive Retrieval** — Selects the most relevant compressed facts for a given query.

The results are striking: **43.24% F1 score** (competitive with much heavier approaches) while using **98% fewer tokens** than full-context methods. SimpleMem has also been packaged as [SimpleMem-MCP](https://github.com/Jiaaqiliu/SimpleMem-MCP), an MCP server that any MCP client can connect to.

**PCO connection:** SimpleMem's compression algorithm is the most directly applicable piece of research in the ecosystem. Their "atomic fact extraction" approach — decomposing conversations into self-contained factual statements — is exactly what PCO's summariser component should implement. The 43% F1 / 98% token reduction benchmark is the target PCO should aim to match or exceed.

#### GPTCache (7,000+ GitHub stars)

[GPTCache](https://github.com/zilliztech/GPTCache) by Zilliz is an older project (2023) that pioneered semantic caching — storing LLM responses and returning cached answers for semantically similar future queries. It claims 2-10x speed improvement and significant cost reduction. It is fully integrated with LangChain and supports OpenAI, LLaMA, Hugging Face Hub, and Anthropic.

GPTCache pre-dates MCP and does not have MCP support. However, the [semantic caching pattern](https://arxiv.org/html/2601.11687v1) it established has been absorbed into newer tools. Recent academic work (January 2026) on "Semantic Caching and Intent-Driven Context Optimization" builds directly on GPTCache's foundation.

**PCO connection:** The semantic caching pattern is already partially implemented in Amplified Partners' token-proxy codebase. GPTCache itself is likely too heavyweight and outdated for direct integration, but its architectural pattern — embedding-based similarity matching for cache hit decisions — should inform PCO's own caching layer.

### 3.2 Framework Context Engines — The Root Systems

Every major agent framework has developed its own context management subsystem. These are the "root systems" that PCO must interoperate with — not replace, but complement.

#### LangChain / LangGraph / Deep Agents SDK

LangChain is the most widely adopted agent framework. Their context management approach is documented across two key publications.

[Context Engineering for Agents](https://blog.langchain.com/context-engineering-for-agents/) (July 2025) formalised the **four-strategy framework**:

- **Write** — Saving context outside the window (scratchpads for session tasks, memories across sessions).
- **Select** — Pulling relevant information into the window (from scratchpads, memories, RAG, semantic tool search).
- **Compress** — Retaining only required tokens (summarisation, trimming, pruning).
- **Isolate** — Splitting context across sub-components (multi-agent setups, sandboxed environments).

LangGraph implements all four via checkpointing (short-term thread-scoped memory), long-term memory (persisted across sessions via LangMem), custom compression nodes, and multi-agent orchestration (supervisor/swarm patterns).

[Context Management for Deep Agents](https://blog.langchain.com/context-management-for-deepagents/) (January 2026) goes deeper, describing the three compression techniques in the Deep Agents SDK:

1. **Offloading large tool results** — Any tool response over 20,000 tokens is immediately offloaded to the filesystem, replaced with a file path and a 10-line preview. Agents re-read or search the file as needed.
2. **Offloading large tool inputs** — When context exceeds 85% of the model's window, old write/edit tool calls are truncated (since the content is already persisted on disk) and replaced with file pointers.
3. **Summarisation** — When context exceeds the threshold and nothing is left to offload, the LLM generates a structured summary (session intent, artifacts created, next steps) to replace the full history. The original messages are preserved on the filesystem for later recovery.

The Deep Agents SDK uses a filesystem abstraction that allows agents to list, read, write, search, pattern-match, and execute files. This makes the filesystem a first-class part of the agent's memory architecture.

**PCO connection:** PCO's pipeline maps directly to LangChain's Write/Compress/Select taxonomy. The most natural integration is a custom LangGraph node that calls PCO during the Compress phase. PCO would replace LangChain's built-in summarisation with quality-verified compression — adding the quality gate that LangChain's native implementation lacks.

#### Google Agent Development Kit (ADK)

Google's ADK takes the most architecturally rigorous approach. Their [context engineering blog post](https://developers.googleblog.com/architecting-efficient-context-aware-multi-agent-framework-for-production/) (December 2025) introduces a **tiered context stack** with explicit separation between storage and presentation:

- **Working Context** (ephemeral) — The per-invocation prompt assembled for the LLM. Includes system instructions, agent identity, selected history, tool outputs, optional memory results, and artifact references. Rebuilt from scratch for each invocation.
- **Session** (durable) — A chronological log of structured Event objects: user messages, agent replies, tool calls and results, control signals, errors. Includes metadata and a state scratchpad. This is the ground truth.
- **Memory** (long-lived) — Searchable knowledge ingested from Sessions. User preferences, past conversation summaries. Accessed via tools.
- **Artifacts** (binary/textual) — Large files, logs, images. Named and versioned. Stored externally, referenced lightly in the working context.

The revolutionary insight is Google's framing of context as a **compiled view**. Working context is not a mutable buffer that grows until it overflows — it is a derived, ephemeral projection compiled from richer state. The compilation is performed by an ordered pipeline of "request processors" and "response processors" — explicit, observable, testable transformations that filter, compact, cache, and route.

For multi-agent systems, ADK uses explicit context scoping. When one agent hands off to another, processors build the callee's context with controlled inheritance: full history, partial history, or no history, depending on the handoff semantics. Prior "Assistant" messages are reframed as narrative so the new agent does not misattribute actions.

**PCO connection:** ADK's architecture is the strongest validation of PCO's design. PCO's pipeline IS a compiler — raw conversation history in, optimised context out. PCO could function as a `request_processor` in ADK's pipeline, handling the compression phase of the compilation. ADK's tiered storage model (Working Context / Session / Memory / Artifacts) maps directly to PCO's design: PCO manages the Working Context tier, Mem0 handles Memory, and the filesystem handles Artifacts.

#### CrewAI

[CrewAI's memory system](https://docs.crewai.com/en/concepts/memory) (updated February 2026) has been significantly modernised. The old separate memory types (short-term, long-term, entity, external) have been replaced with a **unified Memory class** that uses an LLM to analyse content when saving — automatically inferring scope, categories, and importance.

Memory supports adaptive-depth recall with composite scoring that blends semantic similarity, recency, and importance. It can be used standalone, with Crews, with individual Agents, or inside Flows. All agents in a crew share the crew's memory unless an agent has its own, with scoping via paths (e.g., `/agent/researcher`). After each task, the crew automatically extracts discrete facts from the task output and stores them.

**PCO connection:** PCO could serve as CrewAI's external memory backend via MCP. CrewAI's auto-extraction of facts after each task is conceptually similar to PCO's compression pipeline — but CrewAI extracts for storage, while PCO compresses for the active window. They complement each other.

#### Microsoft Agent Framework

[Announced October 2025](https://azure.microsoft.com/en-us/blog/introducing-microsoft-agent-framework/), the Microsoft Agent Framework represents the convergence of Semantic Kernel and AutoGen into a unified, enterprise-grade platform. It supports MCP for tool connections, A2A for agent collaboration, and OpenAPI for arbitrary API integration. Built-in observability, durability, and compliance make it the most enterprise-focused framework.

KPMG's Clara AI is a flagship deployment, built on the framework to connect specialised agents to enterprise data with safeguards.

**PCO connection:** Because the Microsoft Agent Framework is MCP-native, PCO as an MCP server is automatically compatible. No special integration required — PCO shows up as a discoverable tool.

#### Anthropic's Context Engineering Guidance

Anthropic does not ship a framework, but their [context engineering guide](https://www.anthropic.com/engineering/effective-context-engineering-for-ai-agents) (September 2025) has become the industry's reference document. Key principles:

- **"Curate minimal high-signal tokens."** Context is a finite resource. Use the smallest possible set of informative tokens to maximise outcomes.
- **Sub-agent architectures.** Specialised sub-agents handle focused tasks with clean context windows. The main agent coordinates with a high-level plan. Each sub-agent explores extensively (tens of thousands of tokens) but returns only a condensed summary (1,000-2,000 tokens).
- **Compaction.** Summarise nearing-full context. Reinitiate with a high-fidelity summary that preserves key details (decisions, bugs encountered) while discarding redundancies (old tool results).
- **Structured note-taking.** The agent writes persistent notes outside context (e.g., NOTES.md, to-do lists) and pulls them back as needed. This enables tracking progress, maps, and strategies across context resets.
- **Hybrid retrieval.** Pre-load some static data for speed; use "just-in-time" dynamic loading via tools for the rest.

**PCO connection:** Anthropic's emphasis on "minimal high-signal tokens" is the philosophical foundation of PCO's quality verifier. Compression without quality verification is just lossy — Anthropic's guidance says you must tune for recall first, then precision. PCO's Dual Classifier with Veto pattern implements exactly this: compress aggressively, then verify that the compressed output preserves the information the agent actually needs.

### 3.3 MCP Context Tools — The Fruiting Bodies

These are MCP servers specifically built for context optimisation. They are PCO's most direct neighbours in the network — some complementary, some overlapping, all validating that the market need is real.

#### ToolHive MCP Optimizer

[ToolHive](https://github.com/stacklok/toolhive) by Stacklok is a platform for deploying and managing MCP servers in secure containers. Their [MCP Optimizer](https://stacklok.com/blog/cut-token-waste-from-your-ai-workflow-with-the-toolhive-mcp-optimizer/) (October 2025) discovered something surprising: a significant chunk of tokens burned during AI sessions comes not from the user's prompt or the code being discussed, but from **tool descriptions**. When you install MCP servers for GitHub, Grafana, and Notion, you might have 114 tools loaded — and every one of those tool descriptions is sent to the LLM with every request, whether relevant or not.

MCP Optimizer acts as a smart broker: when a prompt arrives, it semantically selects only the relevant tools (up to 8 by default) and sends only those descriptions. Results from their benchmarks:

| Scenario | Without Optimizer | With Optimizer | Reduction |
|----------|------------------|---------------|-----------|
| Simple "Hello" | 46.8k tokens, 114 tools | 11.2k tokens, 3 tools | 76% |
| GitHub issue listing | 102k tokens, 114 tools | 32.4k tokens, 11 tools | 68% |
| Notion meeting notes | 240.6k tokens, 114 tools | 86.8k tokens, 11 tools | 64% |

**PCO connection:** ToolHive Optimizer and PCO handle different token domains. ToolHive reduces tool description tokens. PCO reduces conversation history tokens. They could compose in series: ToolHive selects the right tools, PCO compresses the conversation context, and the LLM receives a lean, focused prompt. Three MCP servers in a mesh, each handling a different token category.

#### Context7 MCP Server

Context7 provides version-specific documentation to LLMs, addressing inaccuracies in AI-generated code. It was flagged on the [Thoughtworks November 2025 Technology Radar](https://www.thoughtworks.com/en-us/insights/blog/generative-ai/model-context-protocol-mcp-impact-2025) at the Tools/Trial level — meaning Thoughtworks found it "very useful in AI-assisted software development" and recommends trialling it in real projects. It works with Claude Code, Cursor, and other MCP-compatible editors.

**PCO connection:** Context7 handles reference documentation; PCO handles conversation history. Complementary, not competing. Both could be registered in the MCP Registry and discovered by the same client.

#### OpenMemory MCP (Mem0)

Covered in detail under Mem0 above. The key point: [OpenMemory](https://mem0.ai/blog/how-to-make-your-clients-more-context-aware-with-openmemory-mcp) runs entirely on the user's local machine (Docker + Postgres + Qdrant), provides four standard MCP tools, includes a Next.js dashboard, and enables cross-client memory — store context in Cursor, retrieve it later in Claude, without repeating yourself.

**PCO connection:** OpenMemory is PCO's most natural integration target for persistent storage. PCO compresses; OpenMemory stores. PCO retrieves; OpenMemory serves.

#### Context Compression MCP Server

Listed on [LobeHub's MCP directory](https://lobehub.com/mcp/yourusername-context-compression-mcp), this is a FastMCP-based server that stores compressed context in SQLite. It provides tools for AI agents to store, retrieve, and manage compressed contextual information. It is simpler than what PCO aims to be — no quality verification, no self-improvement, no rubrik configuration — but it validates the market need. Someone else saw the same problem and built an MCP server for it.

#### Cross-Model Context Compression State Machine

[Posted to Reddit's r/mcp](https://www.reddit.com/r/mcp/comments/1rme98n/i_built_a_cross_model_context_compression_state/) on March 6, 2026. This project creates two new protocols that prioritise "semantics and intent" for cross-session, cross-model communication, formatted similarly to HTTP for model interactions. It connects as an MCP server to any IDE.

The novel aspect is **cross-model transfer**: context compressed by one model (say, Claude) can be meaningfully decompressed and used by a different model (say, GPT). This is a genuinely new capability that no other tool in the ecosystem offers.

**PCO connection:** Cross-model transfer is a potential PCO differentiator. Amplified Partners' clients may use different models for different tasks (a cheap model for classification, an expensive model for generation). If PCO could maintain context coherence across model switches, that would be uniquely valuable.

### 3.4 Gateways and Routing — The Infrastructure Layer

These projects sit beneath the application layer, routing and transforming LLM traffic. PCO's transparent interception pattern (inherited from the access-control-proxy and token-proxy codebases) places it naturally at this level.

#### LiteLLM (20,000+ GitHub stars)

LiteLLM is a unified API gateway for 100+ LLM providers. It provides an OpenAI-format proxy with cost tracking, rate limiting, load balancing, and fallback routing. It is the standard choice for organisations that want to abstract away provider differences.

**PCO connection:** LiteLLM was already recommended as the Context Monitor component in the buy-vs-build analysis. PCO's context monitoring should read LiteLLM's token metrics to know when compression is needed. The natural deployment pattern is: LiteLLM (routing) → PCO (compression) → LLM.

#### Context Gateway (Go, Apache-2.0, 438 stars)

A transparent proxy with context caching, prompt management, and PII redaction. Written in Go rather than Node.js, but architecturally similar to PCO — validating the "transparent interception" pattern.

#### Bifrost / Portkey

High-performance AI gateways focused on request routing, caching, and observability. Production-grade, but focused on routing rather than context management. PCO sits behind these: they route, PCO compresses.

---

## 4. The Hyphae: Protocol Connections and Data Flows

This is the network map — the actual connections between projects, mediated by protocols.

### MCP-Mediated Connections (Standard Protocol)

| From | To | Via | Data Flow |
|------|-----|-----|-----------|
| Any MCP Client (Cursor, Claude, VS Code) | Mem0 / OpenMemory | MCP (SSE transport) | Memory CRUD: add, search, list, delete |
| Any MCP Client | SimpleMem-MCP | MCP (stdio) | Semantic compression: store, retrieve compressed facts |
| Any MCP Client | ToolHive Optimizer | MCP (HTTP/SSE proxy) | Tool selection: sends only relevant tools |
| Any MCP Client | Context7 | MCP | Version-specific documentation retrieval |
| Letta | Any MCP Server | MCP Client SDK | Tool discovery + invocation |
| ToolHive | Multiple MCP Servers | MCP (container proxy) | Routes tool calls to the right server |

Every one of these connections uses the same protocol. **A new MCP server — like PCO — is immediately visible to all of them without any custom integration work.**

### Framework-Specific Connections (Library Integrations)

| From | To | Via | Data Flow |
|------|-----|-----|-----------|
| LangGraph | Mem0 | Python SDK | Long-term memory read/write |
| LangGraph | Zep | Python SDK | Context graph queries |
| CrewAI | Mem0 | Framework integration | Shared crew memory |
| LangChain | GPTCache | Python library | Semantic cache layer |
| Google ADK | Any MCP Server | ADK's MCP integration | Tool access via processors |

These connections are framework-specific, meaning PCO needs custom integrations to participate. The LangGraph integration (custom compressor node) should be a P1 priority.

### Cross-Protocol Connections (The Bridges)

| Pattern | Protocols | What Happens |
|---------|-----------|-------------|
| A2A agent delegates tool use | A2A → MCP | An A2A agent receives a task, discovers it needs a tool, calls that tool via MCP |
| AG-UI streams tool progress | AG-UI + MCP | An agent calls an MCP tool, AG-UI streams the execution progress to the user's frontend |
| MS Agent Framework orchestrates | A2A + MCP + OpenAPI | The framework coordinates agents (A2A), connects tools (MCP), and integrates APIs (OpenAPI) |

**PCO's position in this map:** As an MCP server, PCO is reachable from any MCP client, any framework with MCP support, any A2A agent that delegates to MCP tools, and any AG-UI frontend that calls MCP tools. As a transparent HTTP proxy (OpenAI-compatible API), PCO is reachable from any application that calls an OpenAI endpoint. These two interfaces together cover virtually the entire ecosystem.

---

## 5. The Convergence: Seven Principles the Ecosystem Agrees On

Across all the research — Google's ADK blog, LangChain's publications, Anthropic's guide, Letta's Context Repositories, Mem0's architecture, SimpleMem's research paper — seven architectural principles appear independently and repeatedly. This consensus is remarkable because these teams are not coordinating. They are converging because the problem demands it.

### Principle 1: Context as Compiled View

**Who says it:** Google ADK, LangChain, Anthropic.

The old approach treated context as a mutable string buffer that grows until it overflows. The new approach treats context as a compiled view — a derived, ephemeral projection that is rebuilt for each LLM invocation from richer underlying state. Sessions, memory, and artifacts are the source code. Processors and pipelines are the compiler. Working context is the compiled binary.

**PCO alignment:** PCO's pipeline IS a compiler. Raw conversation history enters one end; optimised, quality-verified context exits the other. This is not a coincidence — it is because the pipeline architecture naturally emerges when you take context engineering seriously.

### Principle 2: Tiered Storage (Hot / Warm / Cold)

**Who says it:** Google ADK, Letta/MemGPT, Mem0.

Context lives at different temperatures. The hot tier is the active context window — small, expensive (every token costs inference compute), and ephemeral. The warm tier is recent session history — larger, cheaper, and durable. The cold tier is long-term memory — vast, cheap, and searchable. The art of context management is moving information between tiers at the right time.

**PCO alignment:** PCO manages the hot tier. Mem0 manages the cold tier. The warm tier is the gap that PCO's filesystem offloading (following LangChain Deep Agents' pattern) should fill.

### Principle 3: Filesystem as Overflow

**Who says it:** LangChain Deep Agents, Letta Context Repositories, Anthropic.

When the active window is full, offload to the filesystem. Replace the content with a pointer (file path + brief preview). The agent can re-read the file later if needed. This is cheaper and more flexible than summarisation because no information is lost — the original content is preserved on disk.

LangChain's Deep Agents SDK offloads tool results over 20,000 tokens immediately, and offloads old tool call inputs when context exceeds 85% of the window. Letta goes further, making the entire filesystem git-versioned. Anthropic recommends "structured note-taking" — the agent writing NOTES.md files outside the context window.

**PCO alignment:** PCO's current design focuses on summarisation. It should add filesystem offloading as a first-pass strategy before summarisation — offload what can be offloaded, then summarise what remains.

### Principle 4: Semantic Lossless Compression

**Who says it:** SimpleMem, Cross-Model Compression State Machine.

Rather than summarising (which is inherently lossy — the summariser decides what to keep), decompose conversations into atomic, self-contained factual statements. Each fact is independently verifiable and retrievable. This preserves the information content while radically reducing the token count.

SimpleMem's three-stage pipeline achieves 43% F1 with 98% fewer tokens — meaning it retains nearly half the retrieval quality of the full conversation at 2% of the token cost.

**PCO alignment:** PCO's summariser should implement semantic lossless compression as its default strategy. The quality verifier then checks whether the compressed facts preserve the information the agent needs — a natural fit for the Dual Classifier with Veto pattern from the codebase.

### Principle 5: MCP as Universal Interface

**Who says it:** The entire ecosystem. 97M+ monthly downloads. 5,800+ servers.

Every new project ships with MCP support or plans it. Mem0 has OpenMemory MCP. SimpleMem has SimpleMem-MCP. Letta acts as an MCP client. ToolHive proxies MCP servers. Context7 is an MCP server. The Context Compression MCP server exists on LobeHub. MCP is the lingua franca, full stop.

**PCO alignment:** PCO must ship as an MCP server. This is not optional. It is the price of admission to the ecosystem. The good news is that FastMCP or the official TypeScript SDK makes this a 2-3 day effort, not a 2-3 week effort.

### Principle 6: Quality Gates on Compression

**Who says it:** Anthropic ("minimal high-signal tokens"), LangChain (eval strategies for context management).

Compression without verification is dangerous. A bad summary that loses a critical fact can cause the agent to hallucinate or abandon its goal. Anthropic explicitly recommends tuning compression prompts for recall first (don't lose important facts), then precision (don't include irrelevant ones).

LangChain's Deep Agents SDK includes evaluation strategies: real-world benchmarks, aggressive compression triggering for feature isolation, and targeted evaluations for objective preservation, recoverability, and "needle-in-haystack" fact retrieval.

**PCO alignment:** This is PCO's unique differentiator. No other open-source tool in the ecosystem implements a quality gate on compression. SimpleMem compresses but does not verify. LangChain summarises but does not score. The Dual Classifier with Veto pattern — compress, then have a second classifier check whether the output preserves the required information, with veto power to reject bad compressions — is genuinely novel. This should be PCO's headline feature.

### Principle 7: Composition Over Monolith

**Who says it:** ToolHive, MCP Registry, every framework.

No project in the ecosystem tries to do everything. ToolHive optimises tool selection. Mem0 handles memory. LiteLLM handles routing. Context7 handles documentation. SimpleMem handles compression. The ecosystem rewards composability — small, focused tools that plug together via standard protocols.

**PCO alignment:** PCO should do ONE thing well: quality-verified context compression. It should compose with Mem0 for persistence, LiteLLM for routing, ToolHive for tool selection, and Context7 for documentation. The temptation to build a memory store, a gateway, or a tool selector should be resisted.

---

## 6. PCO's Position: A Node, Not a Monolith

### What PCO Does That Nothing Else Does

After mapping the entire ecosystem, four capabilities emerge that no existing project provides:

**1. Quality-verified compression.** SimpleMem compresses but does not verify. LangChain summarises but does not score quality. GPTCache caches but does not compress. Zep summarises progressively but does not gate on quality. PCO's Dual Classifier with Veto pattern — inherited from the gatekeeper codebase — is the only implementation of compression with a quality gate. The first classifier compresses; the second verifies that the compression preserves the required information, with the power to reject and force re-compression. This is a genuine gap in the ecosystem.

**2. Transparent interception.** Most tools require explicit integration — the developer must modify their application code to call the tool. PCO's proxy pattern, inherited from access-control-proxy and token-proxy, means zero-change deployment. Point your application at PCO instead of the LLM API endpoint. PCO compresses transparently and forwards to the real endpoint. The application does not know PCO exists. This is critical for the SMB market, where "install this Docker container and change one URL" is an acceptable ask, but "rewrite your agent code to integrate this library" is not.

**3. Self-improving pipeline.** The Kaizen/reflection patterns from the gatekeeper codebase mean PCO can learn which compressions work best. By tracking which compressed facts the LLM actually references in its responses (and which it ignores or contradicts), PCO can feed this signal back to improve future compressions. No other open-source tool in the ecosystem has this feedback loop. This is the PUDDING pathway — continuous improvement through measurement.

**4. Rubrik-driven rules.** JSON-as-Logic configuration, also from the gatekeeper codebase, means non-developers can tune compression behaviour by editing a JSON rubrik — setting compression aggressiveness, fact preservation priorities, domain-specific rules. The entire rest of the ecosystem is developer-first. PCO's rubrik layer is the Amplified Partners differentiator — making context optimisation accessible to SMB users who will never write a line of code.

### PCO's Protocol Surface

To maximise network connectivity — to be a fully connected node in the mycelial network — PCO should expose these interfaces:

| Protocol | How PCO Uses It | Priority | Effort |
|----------|----------------|----------|--------|
| **MCP Server** | Expose compress/decompress/monitor/configure tools. Discoverable via MCP Registry. Works with any MCP client. | P0 — Ship with this | 2-3 days (FastMCP or TS SDK) |
| **OpenAI-compatible HTTP proxy** | Transparent proxy mode. Drop-in replacement for `/chat/completions`. Zero-change deployment. | P0 — Already designed | 3-4 days (pattern from token-proxy) |
| **MCP Client** | Connect to Mem0/OpenMemory for persistence. Connect to Context7 for reference docs. Compose with other MCP servers. | P1 — Phase 2 | 2-3 days |
| **LangGraph custom node** | Custom compressor node for LangGraph pipelines. Plugs into their Compress strategy. | P1 — Phase 2 | 1-2 days |
| **Docker / Helm** | Containerised deployment. One-command setup on Beast. Kubernetes-ready for scale. | P0 — Standard | 1 day |
| **A2A Agent Card** | Publish PCO as a discoverable A2A agent for multi-agent context management. | P2 — Future | 1-2 days |

### Composition Patterns

These are the concrete ways PCO composes with existing ecosystem tools:

**Pattern 1: The Full Stack.** LiteLLM (routing) → PCO (compression) → LLM. LiteLLM handles provider routing and cost tracking. PCO handles context quality. The LLM receives a lean, focused prompt. This is the simplest deployment and the one most likely to be used by Amplified Partners' own infrastructure on the Beast.

**Pattern 2: Memory-Backed Compression.** PCO compresses the active window. Context evicted during compression gets written to Mem0 via OpenMemory MCP. When the agent needs old context back, PCO queries Mem0 and selectively re-injects. This gives PCO effectively unlimited memory while keeping the active window lean. The hot/cold tier pattern without building a vector store.

**Pattern 3: Framework Plugin.** LangGraph pipeline calls PCO as a custom compressor node during its Compress phase. CrewAI crew uses PCO as an external memory backend scoped per agent. Google ADK uses PCO as a `request_processor` in its compiler pipeline. One PCO, three frameworks, no code duplication.

**Pattern 4: MCP Server Mesh.** ToolHive Optimizer selects the right tools (reducing tool description tokens by 64-76%). PCO compresses the conversation context (reducing history tokens by 30-60%). Context7 provides fresh, version-specific documentation (reducing hallucination). Three MCP servers in a mesh, each handling a different token domain, all discoverable via the MCP Registry.

**Pattern 5: The SMB Deployment.** For Amplified Partners' SMB clients: PCO ships as a single Docker container with a JSON rubrik for configuration. Non-technical users adjust compression aggressiveness via the rubrik (or a future UI). PCO connects to the client's existing LLM gateway (LiteLLM or direct API) and immediately reduces their token costs by 30-60%. No code changes required. One `docker run` command. One rubrik file. Done.

---

## 7. The Mycelial Strategy: Phased Execution

### Phase 1: Root into the Network (Weeks 1-2)

**Action 1: Ship PCO as an MCP server.** Use FastMCP (Python) or the official TypeScript SDK. Expose at minimum four tools: `compress_context`, `decompress_context`, `get_compression_stats`, `configure_rubrik`. Register on the MCP Registry. This single action makes PCO discoverable to the entire ecosystem — every IDE, every framework, every agent.

**Action 2: Maintain the OpenAI-compatible proxy mode.** This is the transparent interception interface from token-proxy. Drop-in replacement for `/chat/completions`. This gives PCO two entry points: MCP for tool-aware agents, HTTP proxy for traditional applications.

**Action 3: Implement SimpleMem-style semantic lossless compression as the default algorithm.** Decompose conversations into atomic facts. Index them. Retrieve the relevant ones. Their 43% F1 with 98% token reduction is the benchmark. PCO's quality verifier then gates the output.

### Phase 2: Extend the Hyphae (Weeks 3-4)

**Action 4: Add MCP client capability.** Connect to Mem0/OpenMemory for persistent storage. Evicted context flows into Mem0 automatically. Recalled context flows back from Mem0 on demand. This creates the hot/cold tier without building a vector store.

**Action 5: Build LangGraph integration.** A custom compressor node that slots into any LangGraph pipeline's Compress phase. This is a thin wrapper that calls PCO's core compression logic. One Python file, published as a pip package.

**Action 6: Implement filesystem offloading.** Follow LangChain Deep Agents' pattern: tool results over a configurable threshold are offloaded to the filesystem. Replace with pointer + preview. Add before summarisation in the pipeline — offload first, then compress what remains.

### Phase 3: Fruit the Network (Weeks 5-8)

**Action 7: Publish the rubrik standard.** Make PCO's rubrik configuration a shareable format. Let other MCP context tools import PCO rubriks. This positions PCO as the "compression policy layer" for the ecosystem — other tools compress, but PCO defines how.

**Action 8: Build the Kaizen loop.** Track which compressed facts the LLM references in its responses. Feed that signal back to improve future compressions. This is the self-improvement loop from the gatekeeper codebase, applied to context management. Measure → learn → improve → measure.

**Action 9: Publish an A2A Agent Card.** Make PCO discoverable by multi-agent orchestrators. Google ADK, MS Agent Framework, and any A2A-aware system can then automatically delegate context management to PCO without manual integration.

### The Non-Negotiables

These are not preferences. They are constraints that determine whether PCO succeeds or fails as a network participant:

- **MCP-first.** Not MCP-compatible. MCP-first. Every PCO capability should be a callable MCP tool. The MCP interface is the primary interface, not an afterthought.
- **Compose, don't compete.** Don't build a memory store — use Mem0. Don't build a gateway — use LiteLLM. Don't build tool selection — use ToolHive. PCO does compression + quality verification. Period.
- **JSON rubriks for SMBs.** The entire ecosystem is developer-first. PCO's rubrik-driven configuration is the Amplified Partners differentiator — making context optimisation accessible to non-technical users. This is what makes PCO a product, not just a tool.
- **Docker-native.** Ship as a single container that runs alongside the Beast's existing ~29 Docker containers. One command to deploy, one rubrik to configure, one endpoint to point to.

---

## Sources

All sources are cited inline throughout the document. Full URLs for reference:

| Source | Title | URL |
|--------|-------|-----|
| LangChain Blog | Context Management for Deep Agents (Jan 2026) | https://blog.langchain.com/context-management-for-deepagents/ |
| LangChain Blog | Context Engineering for Agents (Jul 2025) | https://blog.langchain.com/context-engineering-for-agents/ |
| Google Developers Blog | ADK Context Engineering (Dec 2025) | https://developers.googleblog.com/architecting-efficient-context-aware-multi-agent-framework-for-production/ |
| Anthropic | Effective Context Engineering for AI Agents (Sep 2025) | https://www.anthropic.com/engineering/effective-context-engineering-for-ai-agents |
| Letta Blog | Context Repositories: Git-based Memory (Feb 2026) | https://www.letta.com/blog/context-repositories |
| Mem0 | OpenMemory MCP Server | https://mem0.ai/blog/introducing-openmemory-mcp |
| Mem0 | MCP Integration Docs | https://docs.mem0.ai/platform/features/mcp-integration |
| Mule AI | Mem0: The Memory Layer (Mar 2026) | https://muleai.io/blog/2026-03-11-mem0-ai-agent-memory-framework/ |
| DEV Community | MCP vs A2A: Complete Guide to AI Agent Protocols in 2026 | https://dev.to/pockit_tools/mcp-vs-a2a-the-complete-guide-to-ai-agent-protocols-in-2026-30li |
| Codecademy | AG-UI Protocol Overview (Jan 2026) | https://www.codecademy.com/article/ag-ui-agent-user-interaction-protocol |
| AG-UI Docs | Agent User Interaction Protocol | https://docs.ag-ui.com/introduction |
| Google Developers Blog | A2A Protocol Announcement (Apr 2025) | https://developers.googleblog.com/en/a2a-a-new-era-of-agent-interoperability/ |
| OneReach | A2A Protocol Explained (Nov 2025) | https://onereach.ai/blog/what-is-a2a-agent-to-agent-protocol/ |
| Stacklok Blog | ToolHive MCP Optimizer (Oct 2025) | https://stacklok.com/blog/cut-token-waste-from-your-ai-workflow-with-the-toolhive-mcp-optimizer/ |
| Thoughtworks | MCP's Impact on 2025 (Dec 2025) | https://www.thoughtworks.com/en-us/insights/blog/generative-ai/model-context-protocol-mcp-impact-2025 |
| CrewAI Docs | Memory System (Feb 2026) | https://docs.crewai.com/en/concepts/memory |
| MCP Registry | GitHub Repository | https://github.com/modelcontextprotocol/registry |
| GitHub Blog | MCP Registry Launch (Sep 2025) | https://github.blog/changelog/2025-09-16-github-mcp-registry-the-fastest-way-to-discover-ai-tools/ |
| MCP Roadmap | Model Context Protocol Roadmap (Mar 2026) | https://modelcontextprotocol.io/development/roadmap |
| SimpleMem | Efficient Lifelong Memory for LLM Agents | https://github.com/aiming-lab/SimpleMem |
| SimpleMem-MCP | MCP Server for SimpleMem | https://github.com/Jiaaqiliu/SimpleMem-MCP |
| Zep | Context Engineering and Agent Memory Platform | https://www.getzep.com |
| GPTCache | Semantic Cache for LLM Queries | https://github.com/zilliztech/GPTCache |
| Letta / MemGPT | Stateful Agent Platform | https://github.com/letta-ai/letta |
| Mem0 | Universal Memory Layer | https://github.com/mem0ai/mem0 |
| ToolHive | Simplify and Secure MCP Servers | https://github.com/stacklok/toolhive |
| LiteLLM | Unified LLM API Gateway | https://github.com/BerriAI/litellm |
| Microsoft Azure Blog | Microsoft Agent Framework (Oct 2025) | https://azure.microsoft.com/en-us/blog/introducing-microsoft-agent-framework/ |
| Machine Learning Mastery | 6 Best AI Agent Memory Frameworks 2026 (Mar 2026) | https://machinelearningmastery.com/the-6-best-ai-agent-memory-frameworks-you-should-try-in-2026/ |
| DEV Community | AI Agent Memory: LangGraph, CrewAI, AutoGen Comparison | https://dev.to/foxgem/ai-agent-memory-a-comparative-analysis-of-langgraph-crewai-and-autogen-31dp |
| arXiv | Semantic Caching and Intent-Driven Context Optimization (Jan 2026) | https://arxiv.org/html/2601.11687v1 |
| Reddit r/mcp | Cross Model Context Compression State Machine (Mar 2026) | https://www.reddit.com/r/mcp/comments/1rme98n/ |
| AWS Builder Center | Picking an AI Agent Framework in 2026 (Mar 2026) | https://builder.aws.com/content/3AzsgG6TreTO3uLRqpWNxfEyUhe/ |
| LobeHub | Context Compression MCP Server | https://lobehub.com/mcp/yourusername-context-compression-mcp |

---

*Document produced by Amplified Partners' Rapid Intelligence Cycle (Phase 1: Discover + Phase 2: Analyse). Research conducted March 17-19, 2026. All source URLs verified at time of writing.*

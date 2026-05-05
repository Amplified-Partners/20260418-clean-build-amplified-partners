---
title: "Agent Memory, Harnesses & the Amplified Operating System: A Complete Audit"
id: "agent-memory-harness-audit-copy"
version: 1
created: "2026-04-25"
type: "document"
topic_type: "audit"
audience: "internal"
layer: "truth"
status: "filed"
signed_by: "Devon, 2026-04-25, devin-992682c244cf444f91e0a516498afbfd"
---

# Agent Memory, Harnesses & the Amplified Operating System: A Complete Audit

## Executive Summary

The core problem is not the agents' intelligence or their skills. The problem is the harness — the architecture around the model that governs what it remembers, how it receives instructions, and what happens between sessions. Amplified Partners has built brilliant plans, a solid vault, a working code factory, and a functioning search engine. What's missing is the control plane that makes agents reliably execute those plans across sessions. This report covers every aspect of agent memory, the harness architecture needed, the subscription-to-API transition, a gap analysis of current vs best practice, and a cohesive plan to fix it.

---

## Part 1: Every Aspect of Agent Memory

Agent memory is not one thing. It is six distinct mechanisms, each serving a different purpose. The agents' "niceness" and failure to follow instructions stems from relying on only some of these while neglecting others.

### The Six Memory Layers

| Layer | What It Is | Persistence | Who Controls It | Claude Subscription | Claude API |
|-------|-----------|-------------|-----------------|-------------------|------------|
| **System Prompt** | Core identity and instructions injected at conversation start | Per-session (reloaded each time) | You | Limited to Project Instructions (~8k chars) | Unlimited length, full control, per-request |
| **Project Knowledge Base** | Documents uploaded to a Claude Project | Persistent across all chats in project | You | Yes — up to context limit, uses [Contextual Retrieval](https://learn-claude.readthedocs.io/en/latest/02-Claude-Project/41-Claude-Project-Knowledge-Base-Quick-Start/) | No equivalent — you build your own RAG |
| **Conversation History** | The running context of the current chat | Current session only (lost on new chat) | Both (you write, model reads) | Automatic | You manage the messages array — [it is stateless](https://platform.claude.com/docs/en/build-with-claude/working-with-messages) |
| **CLAUDE.md / MEMORY.md** | Persistent instruction files read at session start | Per-project, per-machine | You + auto-memory | Claude Code only | [Claude Agent SDK](https://platform.claude.com/docs/en/agent-sdk/modifying-system-prompts) — settingSources must be explicitly loaded |
| **Artifacts with Persistent Storage** | Stateful applications that store data across sessions | Persistent (up to 20MB) | You + the artifact | [Pro/Max/Team/Enterprise](https://albato.com/blog/publications/how-to-use-claude-artifacts-guide) | Not applicable |
| **External Memory (MCP/Files/DB)** | Vault, FalkorDB, SESSION-STATE.md, post-mortems | Permanent until deleted | You | Via MCP servers | Via MCP servers or direct integration |

### How Memory Actually Works in Claude

Claude has **no persistent memory between conversations** by default. Every new chat starts cold. The [Claude system prompt](https://ai-consciousness.org/anthropics-claude-opus-4-5-system-prompt-as-of-january-2026/) includes past-chat search tools that let it reference previous conversations, but these are search tools, not memory — they retrieve snippets, not full context.

**Project Instructions** (the system prompt in Claude Projects) are the most powerful lever for controlling agent behavior on the subscription. Everything you put there is loaded into every conversation in that project. But it has limits — you cannot programmatically change it between sessions, and the knowledge base uses [Contextual Retrieval RAG](https://learn-claude.readthedocs.io/en/latest/02-Claude-Project/41-Claude-Project-Knowledge-Base-Quick-Start/), meaning Claude doesn't see all your uploaded documents simultaneously; it retrieves relevant chunks.

**The critical insight from [Anthropic's context engineering guide](https://www.anthropic.com/engineering/effective-context-engineering-for-ai-agents):** "Find the smallest possible set of high-signal tokens that maximize the likelihood of some desired outcome." Memory is not about storing everything. It's about injecting the right context at the right moment.

### Why "Nice" Agents Ignore Instructions

The root cause, [confirmed by Anthropic's own engineering](https://www.anthropic.com/engineering/effective-harnesses-for-long-running-agents), is twofold:

1. **Context displacement** — as the conversation grows, instructions at the top of the system prompt move further from the model's attention. The model "forgets" not because it can't read them, but because they lose salience.
2. **Contextual reasoning override** — Claude Sonnet 4 and newer models [evaluate whether following literal commands serves the user's apparent goal](https://theagentarchitect.substack.com/p/claude-sonnet-4-prompts-stopped-working). If "ALWAYS" and "MUST" conflict with what the model perceives as contextually appropriate, context wins. This is by design — but it means imperative instructions ("DO THIS") are treated as suggestions.

The fix is not louder instructions. The fix is a harness.

---

## Part 2: Agent Harnesses — How to Make Agents Follow Instructions

### What Is a Harness?

An agent harness is [the missing layer between a smart model and a reliable system](https://www.linkedin.com/pulse/agent-harness-architecture-dominate-2026-bassel-haidar-sczfe). It connects sessions, enforces checkpoints, creates handoffs, constrains blast radius, routes tasks to the right cognition, and decides when a human must intervene.

The key insight from [Anthropic's harness guide](https://www.anthropic.com/engineering/effective-harnesses-for-long-running-agents): **"No single context window is a safe container for long-horizon work."** A harness treats each agent run as a bounded unit of work — scoped, checkpointed, validated, summarized, and handed off.

### The Four Essential Harness Layers

Per [Bassel Haidar's architecture analysis](https://www.linkedin.com/pulse/agent-harness-architecture-dominate-2026-bassel-haidar-sczfe), reinforced by Anthropic's own practices:

| Layer | What It Does | Amplified Equivalent | Status |
|-------|-------------|---------------------|--------|
| **Guardrails** | Rules the agent cannot violate. Narrow the action space. | Layer 0 Laws, SOUL.md, Enforcer agent | Designed but not injected reliably |
| **Checkpoints** | Validation gates that catch drift before it compounds | QualityGateWorkflow, post-mortems | Designed but not running in every session |
| **Handoffs** | Durable artifacts that let the next session pick up | SESSION-STATE.md, Baton Pass Protocol | Designed but agents not writing them |
| **Human Injection Points** | Where human attention reduces maximum risk | Approval tiers, confidence gating | Designed but not enforced |

### The Anthropic Two-Agent Pattern

[Anthropic's tested solution](https://www.anthropic.com/engineering/effective-harnesses-for-long-running-agents) splits the work into two distinct agent types:

**Initializer Agent** (runs once at project start):
- Creates the environment: feature list, progress file, init script
- Establishes the ground truth that all subsequent agents reference
- Uses the most expensive cognition because mistakes here propagate

**Task Agent** (runs for each bounded unit of work):
1. Reads progress file + git log to understand current state
2. Runs init script to verify environment is clean
3. Picks ONE feature/task to work on
4. Does the work
5. Tests the work
6. Commits with descriptive message
7. Updates progress file
8. Leaves environment in clean state

### The 36% Problem and How Harnesses Fix It

Without a harness, if each step in a 10-step task has 90% reliability, the end-to-end success rate is 0.9^10 = ~35%. A harness inserts checkpoints that [reset drift before it compounds](https://www.linkedin.com/pulse/agent-harness-architecture-dominate-2026-bassel-haidar-sczfe), turning fragile sequential chains into bounded units you can validate, correct, and resume.

### Practical Harness Techniques That Work

From [Anthropic's guide](https://www.anthropic.com/engineering/effective-harnesses-for-long-running-agents) and [community experience](https://www.reddit.com/r/ClaudeCode/comments/1r5ldvp/the_instruction_is_clear_i_just_didnt_follow_it/):

1. **Use JSON for state, not Markdown** — models are less likely to inappropriately edit JSON structures. Anthropic uses `feature_list.json` with `passes: true/false` that agents can only toggle, not delete.

2. **One feature at a time** — never let the agent attempt the whole plan at once. Break it down and enforce single-feature focus.

3. **Progress file read-at-start** — every session begins by reading the progress file and git log. This is non-negotiable.

4. **Self-verify before marking done** — agents must test their own work end-to-end before declaring success.

5. **Git as checkpoint** — commit after every meaningful change. This allows rollback and provides an audit trail.

6. **Replace imperatives with conditionals** — instead of "ALWAYS do X", use "IF condition THEN do X, ELSE do Y". [Newer Claude models respond to decision logic, not drill-sergeant commands](https://theagentarchitect.substack.com/p/claude-sonnet-4-prompts-stopped-working).

7. **Ask the model to restate the task** — before execution, have the agent paraphrase what it understood. Misinterpretation caught here saves hours.

8. **One reflection cycle maximum** — [ReflexiCoder proved](https://arxiv.org/html/2603.05863v1) that one self-correction cycle is sufficient. More loops waste tokens and compound errors.

---

## Part 3: Claude Subscription vs API — What Changes

### Current State: Anthropic Subscription

On the subscription (Pro/Max/Team), you get:
- **Claude Projects** with system instructions and knowledge base
- **Free cache reads** — when the model re-reads the same context, it costs nothing
- **Rate limits** based on 5-hour rolling windows
- **Past chat search** — Claude can reference previous conversations
- **Artifacts with persistent storage** (20MB per artifact)
- **No programmatic control** — you can't change the system prompt between turns

### What API Gives You

On the API, you get:
- **Full system prompt control** — unlimited length, changed per request
- **Stateless by design** — [you send the full conversation history every time](https://platform.claude.com/docs/en/build-with-claude/working-with-messages)
- **Tool use / function calling** — define tools as JSON schemas, Claude decides when to use them
- **Memory tool (beta)** — [persistent file-based storage outside the context window](https://thomas-wiegold.com/blog/claude-api-memory-tool-guide/), visible tool calls for transparency
- **Context editing** — clear old thinking/tool results to manage token budget
- **100% data ownership** — [no retraining, minimal retention](https://www.reddit.com/r/Anthropic/comments/1rui52o/whats_the_difference_between_using_claudes_api_vs/)
- **Claude Agent SDK** — [system prompts via CLAUDE.md, output styles, append, or fully custom](https://platform.claude.com/docs/en/agent-sdk/modifying-system-prompts)

### Do You Get Individual Agents on API?

**No, not natively.** The API is stateless — each request is independent. But this is actually better for your use case. Here's why:

You build individual agents by:
1. **Giving each agent a unique system prompt** — their personality, role, constraints, tools
2. **Managing their conversation history** in your own storage (FalkorDB, files, DB)
3. **Injecting relevant memory** at the start of each call (from vault, from post-mortems, from SESSION-STATE.md)
4. **Routing through LiteLLM** — which you already have, giving you model-agnostic routing

This means each "agent" is a combination of:
- A system prompt file (e.g., `coder.md`, `enforcer.md` — you already have these)
- A memory retrieval function that pulls relevant context
- A conversation loop that manages state
- A tool set that defines what the agent can do

**You already designed this in the Cove Orchestrator.** The agent configs, prompts, and rubrics in `/opt/amplified/agent-stack/cove-orchestrator/agents/` ARE the individual agents. They just need the harness to make them reliable.

### Cost Reality

[Analysis shows](https://www.reddit.com/r/ClaudeAI/comments/1qpcj8q/claude_subscriptions_are_up_to_36x_cheaper_than/) subscriptions can be up to 36x cheaper than API for repetitive agentic loops because cache reads are free on subscription but cost 10% of input on API. However, the API gives you the programmatic control you need. The practical approach: **use subscription for interactive work, API for automated agent runs via Cove.** Your $5/day budget cap via the Enforcer is exactly the right constraint.

---

## Part 4: Best Practice vs Current Practice — The Gap Analysis

### What Best Practice Looks Like

Based on [Anthropic's harness guide](https://www.anthropic.com/engineering/effective-harnesses-for-long-running-agents), [context engineering guide](https://www.anthropic.com/engineering/effective-context-engineering-for-ai-agents), and [industry patterns](https://www.linkedin.com/pulse/agent-harness-architecture-dominate-2026-bassel-haidar-sczfe):

| Principle | Best Practice | Amplified Current State | Gap |
|-----------|--------------|------------------------|-----|
| **Harness exists** | Initializer + Task Agent pattern with checkpoints | Cove Orchestrator designed, but agents run in subscription Claude Projects without harness | **Critical gap** — plans exist in vault but agents don't read them before acting |
| **Memory injection** | Every session starts by reading progress file, git log, relevant post-mortems | SESSION-STATE.md and Baton Pass designed but agents not consistently writing or reading them | **Critical gap** — the memory system exists on paper but isn't being executed |
| **Bounded work units** | One feature per session, commit after each | Agents try to do too much at once, context overflows, half-finished work | **Critical gap** — no enforcement of single-task focus |
| **State is in files, not in heads** | JSON feature list, progress.txt, structured handoff notes | Plans are in Ewan's head and in vault documents, but not in agent-readable progress files | **Critical gap** — this is the fundamental issue |
| **Checkpoints validate** | Tests run, features verified before marking done | QualityGateWorkflow designed, post-mortem template exists | **Partial** — designed but not running every session |
| **Instructions use conditionals** | "IF X THEN Y ELSE Z" decision logic | System prompts use imperatives ("ALWAYS", "MUST") which newer models treat as suggestions | **Significant gap** — prompt style needs updating |
| **Agents self-verify** | End-to-end testing before declaring success | No systematic self-verification in current workflow | **Gap** |
| **Progress is durable** | Written to file, committed to git, readable by next session | Post-mortems designed but not consistently produced | **Gap** |

### The Root Cause

**The agents aren't changing their memories because nobody is making them.** The subscription Claude Projects model gives you a static system prompt and knowledge base, but no mechanism to:
- Force the agent to read a progress file before starting
- Force the agent to write a progress update before ending
- Validate that the agent actually did what was asked
- Inject dynamic context based on what happened in the previous session

This is the harness gap. The plans are brilliant. The execution environment doesn't enforce them.

---

## Part 5: The Search Engine Status

**The search engine IS built and deployed.** It's SearXNG, running on Beast at:

- **External URL:** `https://search.beast.amplifiedpartners.ai`
- **Internal Docker:** `http://searxng:8080` (on the amplified-net Docker network)
- **Policy:** COV-244 (Done) — SearXNG-first for all agent search tasks

It aggregates results from Google, Bing, DuckDuckGo, Brave, and others through the 10Gbps Hetzner pipe with no tracking. The API is functional (`GET /search?q={query}&format=json`).

The confusion about "where it is" likely stems from the fact that it's a backend service — there's no flashy frontend to point at, but the JSON API is live and ready for agent integration.

---

## Part 6: The Cohesive Plan — Building the Engine That Builds the Engine

### Phase 0: Fix the Harness (Week 1) — This Unblocks Everything

This is the one thing that makes every other thing work. Without this, nothing changes regardless of how good the plans are.

**0.1 — Create the Initializer Agent prompt**

A dedicated system prompt that runs once per project/sprint:
- Reads the vault master plan
- Expands it into a structured `task_list.json` (not Markdown — JSON)
- Creates `SESSION-STATE.md` with current state
- Creates `progress.txt` with empty progress log
- Commits everything to git

**0.2 — Create the Task Agent prompt template**

Every agent session (whether in Claude Projects or via API) starts with:
```
1. Read SESSION-STATE.md
2. Read progress.txt  
3. Read git log --oneline -20
4. Read task_list.json — pick ONE task
5. Restate the task in your own words
6. Do the work
7. Test the work
8. Commit to git with descriptive message
9. Update progress.txt
10. Update SESSION-STATE.md
11. Generate post-mortem (if substantial work)
```

This is the harness. It's not optional. It's in the system prompt.

**0.3 — Rewrite instructions as conditionals**

Replace:
```
ALWAYS check the vault before making decisions.
MUST follow the plan exactly.
```

With:
```
IF you are starting a new task:
  THEN read SESSION-STATE.md and progress.txt first
  IF they don't exist, create them before proceeding
  
IF the task requires a decision not covered by the plan:
  THEN surface the decision explicitly, state your recommendation with confidence, and ask for guidance

IF you complete a task:
  THEN update progress.txt with: what you did, what state you left things in, what should happen next
  THEN commit to git
```

### Phase 1: API Migration (Week 2-3)

**1.1 — Stand up the API agent runner in Cove**

Using the existing Cove Orchestrator architecture:
- Each agent (coder, reviewer, enforcer, architect, security) already has prompts in `/opt/amplified/agent-stack/cove-orchestrator/agents/prompts/`
- Each has rubrics in `/agents/rubrics/`
- LiteLLM already routes to the right model tier
- Add the harness wrapper: before each agent call, inject SESSION-STATE.md + relevant vault context

**1.2 — Build the memory injection layer**

Before each API call:
1. Query FalkorDB/Graphiti for relevant entities and recent decisions
2. Read the relevant post-mortem from `/vault/post-mortems/`
3. Read `knowledge_base.md` (already designed for injection)
4. Compose the system prompt: Layer 0 Laws + Agent-specific prompt + Dynamic context
5. Send to Claude API via LiteLLM

**1.3 — Implement the Enforcer as a real harness**

The Enforcer agent already runs every 10 minutes via cron. Extend it to:
- Validate that `progress.txt` was updated in the last session
- Validate that `SESSION-STATE.md` is current
- Check git log for commits
- Flag missing checkpoints

### Phase 2: The Operating System Cohesion (Week 3-4)

**2.1 — The Master Task List**

Create a single `amplified-os-master.json` that maps every component of the SMB operating system:

```json
{
  "components": [
    {
      "name": "SearXNG Search Engine",
      "status": "deployed",
      "location": "search.beast.amplifiedpartners.ai",
      "linear_issue": "COV-244",
      "depends_on": ["Beast Docker", "Traefik"],
      "next_steps": ["Integrate with all agent workflows"]
    },
    {
      "name": "FalkorDB Knowledge Graph", 
      "status": "deployed_partial",
      "location": "falkordb:6379 (internal)",
      "linear_issue": "COV-173",
      "depends_on": ["Beast Docker"],
      "next_steps": ["Complete Graphiti ingestion (327/4664 files done)", "Migrate remaining Qdrant collections"]
    },
    {
      "name": "Cove Code Factory",
      "status": "designed",
      "location": "ewan-dot/cove (empty repo)",
      "linear_issue": "multiple",
      "depends_on": ["Temporal", "Agent prompts", "LiteLLM"],
      "next_steps": ["Implement Temporal workflows", "Build the harness wrapper"]
    }
  ]
}
```

This becomes the source of truth. Agents read it. Agents update it. Nothing lives only in someone's head.

**2.2 — Skills as the Execution Layer**

The Perplexity skills you've already built (amplified-agent-architecture, amplified-vault-knowledge, amplified-prompt-environment, amplified-self-reflection-protocol, etc.) ARE the procedural memory. They're excellent. The gap is that your Claude Project agents don't have access to them.

On API: inject relevant skill content into the system prompt.
On subscription: upload skill files to the Project Knowledge Base.

**2.3 — The Pre-Curator Chain**

From your March 17 session, you designed a brilliant data refinement chain:
- Raw input → spelling/formatting cleanup (preserve voice)
- Cleaned input → entity extraction (FalkorDB/Graphiti)
- Entities → knowledge graph update

This chain needs to be implemented as a Temporal workflow in Cove, not run manually.

### Phase 3: Close the Loop (Ongoing)

**3.1 — Weekly Kaizen Review**

The Department of Continuous Improvement (from your self-reflection protocol) runs weekly:
- Scan post-mortems for recurring failure patterns
- Promote repeated lessons to skill files or CLAUDE.md
- Update rubrics if quality criteria are miscalibrated
- Update the master task list

**3.2 — Handoff Model Progression**

Per the existing 4-month plan:
- Month 1 (now): Supervised — Ewan reviews everything
- Month 2-3: Guided — Ewan reviews exceptions
- Month 4+: Strategic — 30-60 min/day

The harness is what makes the transition from supervised to guided possible. Without checkpoints and validated handoffs, you can't trust the agents enough to stop reviewing everything.

---

## Part 7: Immediate Actions — What to Do Today

1. **Create `harness-template.md`** — a session-start protocol that every agent reads. Upload it as the first document in every Claude Project.

2. **Create `task_list.json`** — turn the plan in your head into a structured file. Start with just the top 10 things that need building. Each entry: name, status, owner, next step.

3. **Rewrite one agent's system prompt** using conditionals instead of imperatives. Test it. If it works better, apply to all.

4. **Run the vault ingestion** — `python ingest_vault.py --resume` to continue from the 327/4664 checkpoint. The knowledge graph needs feeding.

5. **Accept that the search engine exists** — SearXNG is at `search.beast.amplifiedpartners.ai`. It works. Move on to integrating it with agent workflows rather than looking for it.

---

## Key Sources

- [Anthropic: Effective Harnesses for Long-Running Agents](https://www.anthropic.com/engineering/effective-harnesses-for-long-running-agents)
- [Anthropic: Effective Context Engineering for AI Agents](https://www.anthropic.com/engineering/effective-context-engineering-for-ai-agents)
- [Bassel Haidar: Agent Harness Architecture](https://www.linkedin.com/pulse/agent-harness-architecture-dominate-2026-bassel-haidar-sczfe)
- [Claude Code Memory Documentation](https://code.claude.com/docs/en/memory)
- [Claude API Messages Documentation](https://platform.claude.com/docs/en/build-with-claude/working-with-messages)
- [Claude Agent SDK: Modifying System Prompts](https://platform.claude.com/docs/en/agent-sdk/modifying-system-prompts)
- [Claude API Memory Tool Guide](https://thomas-wiegold.com/blog/claude-api-memory-tool-guide/)
- [The AI Maker: Claude Project Memory System](https://aimaker.substack.com/p/ultimate-guide-to-claude-project-memory-system-prompt)
- [The Agent Architect: Claude Sonnet 4 Prompt Shift](https://theagentarchitect.substack.com/p/claude-sonnet-4-prompts-stopped-working)
- [Reddit: Claude Subscription vs API Pricing](https://www.reddit.com/r/ClaudeAI/comments/1qpcj8q/claude_subscriptions_are_up_to_36x_cheaper_than/)
- [Reddit: Agents Not Following Instructions](https://www.reddit.com/r/ClaudeCode/comments/1r5ldvp/the_instruction_is_clear_i_just_didnt_follow_it/)
- [Anthropic Claude Memory & Context Cookbook](https://platform.claude.com/cookbook/tool-use-memory-cookbook)
- [ReflexiCoder: Self-Reflection via RL](https://arxiv.org/html/2603.05863v1)

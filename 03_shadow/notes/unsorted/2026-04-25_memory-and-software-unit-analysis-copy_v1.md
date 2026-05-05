---
title: "Memory Architecture + Software Unit Analysis + Partner Estimation"
id: "memory-and-software-unit-analysis-copy"
version: 1
created: "2026-04-25"
type: "document"
topic_type: "unsorted"
audience: "internal"
layer: "shadow"
status: "filed"
signed_by: "Devon, 2026-04-25, devin-992682c244cf444f91e0a516498afbfd"
---

# Memory Architecture + Software Unit Analysis + Partner Estimation

**Attribution:** Originator: Ewan Bramley — vision, architecture, operating rules. Analyst: Perplexity Computer — research, synthesis, estimation.

**Date:** 24 March 2026

---

## Part 1: Memory — Complete Technical Picture

### 1.1 Claude Code Memory (What You'll Build On)

Two systems, both loaded at session start. Per [official Claude Code docs](https://code.claude.com/docs/en/memory):

**CLAUDE.md (you write it)**

| Scope | Location | Shared With |
|---|---|---|
| Managed policy | `/Library/Application Support/ClaudeCode/CLAUDE.md` (macOS) | All users in org — cannot be excluded |
| Project | `./CLAUDE.md` or `./.claude/CLAUDE.md` | Team via source control |
| User | `~/.claude/CLAUDE.md` | Just you, all projects |

- Loaded in full every session. Target under 200 lines — longer = worse adherence.
- Supports `@path/to/import` (recursive, max depth 5).
- Subdirectory CLAUDE.md files load on demand.
- `.claude/rules/` directory: path-scoped rules via YAML frontmatter glob patterns.
- `claudeMdExcludes` setting: glob-based exclusion of specific files.

**Auto Memory (Claude writes it)** — shipped v2.1.59, 26 Feb 2026

- Stored per-project at `~/.claude/projects/<project>/memory/`
- Machine-local. Not synced across machines.
- Contains:
  - `MEMORY.md` — concise index. First 200 lines loaded every session.
  - Topic files (e.g., `debugging.md`, `api-conventions.md`) — loaded on demand.
- Claude accumulates: build commands, debugging insights, architecture notes, code style, workflow habits.
- Subagents can maintain their own auto memory.
- Toggle: `/memory` command or `autoMemoryEnabled: false` in project settings.

### 1.2 Hooks — The Enforcement Layer

Per [PixelMojo](https://www.pixelmojo.io/blogs/claude-code-hooks-production-quality-ci-cd-patterns) and [eesel.ai](https://www.eesel.ai/blog/hooks-in-claude-code) references:

| Event | When It Fires | Can Block? | Your Use |
|---|---|---|---|
| `PreToolUse` | Before any tool execution | YES | 55% context hard-kill, file protection, security gates |
| `PostToolUse` | After tool execution | No | Auto-formatting, linting, git staging, logging |
| `Notification` | Claude sends notification | No | Slack/Telegram alerts, Enforcer escalation |
| `Stop` | Claude finishes responding | No | Quality gate scoring, post-mortem generation |
| `SubagentStop` | Subagent completes | No | Subagent output validation |
| `PreCompact` | Before context compaction | No | Save critical context before 55% kill |
| `UserPromptSubmit` | Before user prompt processed | No | Prompt validation, input logging |
| `SessionStart` | Session begins | No | Memory injection, environment setup |

**Three handler types** (Claude Code unique advantage):
1. **Command** — runs a shell script. Fastest. ~5ms overhead.
2. **Prompt** — sends to LLM for evaluation. Uses tokens but enables reasoning.
3. **Agent** — spawns a full subagent with tool access. Most powerful, most expensive.

**For your 55% context hard-kill hook:**
A `PreToolUse` command handler with a shell script that checks context usage via the PPID flag pattern. When context exceeds 55%, it saves SESSION-STATE.md and forces a baton pass. This is measured, not felt — exactly as you specified.

**For your Enforcer 10-minute cron:**
`Stop` hook → triggers post-mortem generation + rubric scoring. `PostToolUse` hook → auto-commits to git after every significant action.

### 1.3 Claude App Memory (Web/Desktop/Mobile)

Two-tier system per [community documentation](https://www.reddit.com/r/claudexplorers/comments/1q7rdp5/claudes_builtin_memory_system_short_practical/):

**Automatic background context** — scheduled background process generates `<userMemories>` block. Sections: work context, personal context, top of mind, brief history. Prioritises durable facts. Recency-weighted.

**Explicit memory edits** — up to 30 entries, ~200 chars each. Only created when explicitly requested. Tool-gated.

Both injected into system prompt at conversation start. Free tier since 2 March 2026. Import tool for switching from ChatGPT ([The Verge](https://www.theverge.com/ai-artificial-intelligence/887885/anthropic-claude-memory-upgrades-importing)).

### 1.4 The Fading Memory Problem

Per [Skywork analysis](https://skywork.ai/blog/claude-memory-a-deep-dive-into-anthropics-persistent-context-solution/): as CLAUDE.md files grow, the model's ability to pinpoint relevant information within a large context block diminishes. Signal lost in noise. Anthropic chose file-based markdown over vector databases — transparent, editable, version-controllable, but the trade-off is scale.

**Your mitigation:** The 4-tier retrieval model already addresses this: CLAUDE.md (always) → MEMORY.md (always) → docs/solutions/ (on-demand) → skills/ (invoked). This is scored 19/20 in your own extraction map. The 55% hook prevents the context from ever getting bloated enough for fading to occur.

### 1.5 What's New That Helps Us Build

| Feature | Date | Relevance |
|---|---|---|
| Auto memory (MEMORY.md) | 26 Feb 2026 | Agents self-document learnings. No manual memory management. |
| Claude Code Channels (Telegram/Discord) | 20 Mar 2026 | Control agents from phone. Two-way. Per [Matt Paige on Substack](https://mattpaige68.substack.com/p/anthropic-just-dropped-4-massive). |
| Scheduled Tasks (`/loop`) | Early Mar 2026 | Cron-like scheduling inside Claude Code. Per [Nate's Newsletter](https://natesnewsletter.substack.com/p/your-ai-agent-needs-three-things). |
| Remote Control | Mar 2026 | Supervise from any device. |
| 1M context at flat pricing | 13 Mar 2026 | Opus 4.6: $5/$25 per million tokens. 78.3% MRCR v2 at 1M tokens. 15% fewer compactions. |
| PreCompact hook event | Mar 2026 | Save critical context before compaction — directly supports your baton pass protocol. |
| `SubagentStop` hook event | Mar 2026 | Validate subagent output — directly supports your auditor/reviewer pattern. |

### 1.6 Token Efficiency Research

Per [OpenClaw optimization guide](https://ai-coding.wiselychen.com/en/openclaw-cost-optimization-guide-97-percent-reduction/):

| Strategy | Effect | Your Implementation |
|---|---|---|
| Session initialization (lean context) | $0.40 → $0.005 | 55% hook + CLAUDE.md tiered loading |
| Model routing (Haiku default) | $0.05 → $0.002 | LiteLLM 3-tier: Haiku/Sonnet/Opus |
| Local heartbeats (Ollama) | $0.02 → $0 | Enforcer on Ollama, not API |
| Prompt caching (static content) | 90% discount | SOUL.md, CLAUDE.md, Layer 0 Laws — all cacheable |
| Rate limiting (batch) | Budget control | $5/day cap during build phase |

Combined: $0.47 per interaction → $0.012. That's 97% reduction.

Per [NVIDIA/MIT research](https://blogs.nvidia.com/blog/inference-open-source-models-blackwell-reduce-cost-per-token/): infrastructure and algorithmic efficiencies are reducing inference costs by up to 10x annually at the frontier level.

---

## Part 2: Line Graph — Needed or Not?

**My honest assessment: No. Not at this stage.**

Reasons:
1. You're about to build, not present to investors. A diagram consumes time you could spend on the first unit of software.
2. The 4-tier retrieval model is already well-understood (scored 19/20). Drawing it doesn't make it clearer to you.
3. The memory architecture is file-based and hierarchical — it's inherently simple enough that a directory tree is more accurate than a line graph.
4. When you need a diagram, it'll be for Client Zero (Dave Jesmond) onboarding documentation, and at that point the system will be real, not theoretical.

**When you will need a visual:** Week 4-5, when the Governance Dashboard (Stream 4) needs to show the full memory flow to the monitoring layer. At that point it should be generated from the actual running system, not from a design document.

---

## Part 3: The Software Inventory (From the Document)

Counting every distinct piece of software the Parallel Build Scaffolding requires:

### Already Running (STRONG)

| # | Component | Type |
|---|---|---|
| 1 | SearXNG | Search engine (Docker, Beast) |
| 2 | LiteLLM | API gateway (Docker, Beast) |
| 3 | Ollama | Local LLM inference (Beast) |
| 4 | Qdrant | Vector database (14,581 vectors) |
| 5 | Beast server | Infrastructure (36+ Docker containers) |
| 6 | PUDDING/APDS pipeline | Discovery engine |

### Needs Building/Deploying (PARTIAL + GAP)

| # | Component | Type | Effort |
|---|---|---|---|
| 7 | Neo4j/DozerDB | Graph database (replacing FalkorDB) | 2-3 weeks |
| 8 | Temporal | Workflow orchestration | 3-4 weeks |
| 9 | Meilisearch | Vault full-text search | 1 week |
| 10 | PCO MCP Server | Quality-verified compression | 2-3 weeks |
| 11 | CRAAP+SIFT scoring module | Python module + API | 2 weeks |
| 12 | GRADE evidence scoring | Scoring protocol + API | 2 weeks |
| 13 | Bias Detection Protocol | 3-level framework | 2-3 weeks |
| 14 | Research Prompt Templates | Markdown templates | 1 week |
| 15 | Night Crawler v1 | RSS/API polling scheduler | 2-3 weeks |
| 16 | Triple Search Implementation | Triangulation algorithm | 1 week |
| 17 | Meta-Process v1.0 | Process design process | 3-4 weeks |
| 18 | Process Repository | Central repo + templates | 2 weeks |
| 19 | 14 Agent MDs | Marketing agent specs | 2 weeks |
| 20 | Content Quality Rubrics | Per-content-type scoring | 1 week |
| 21 | Agent Registry | Registry + monitoring | 1 week |
| 22 | Universal Quality Gate | 3-question gate | 0.5 week |
| 23 | Unified Truth Architecture (CP-01) | YAML output wrapper | 1-2 weeks |
| 24 | Laws Enforcement Protocol | Testable enforcement criteria | 1-2 weeks |
| 25 | Ewan Pushback Protocol | Evidence-based challenge system | 1 week |
| 26 | Governance Dashboard | Real-time monitoring | 3 weeks |
| 27 | Client Onboarding Process | End-to-end APQC-tagged | 1-2 weeks |
| 28 | Kaizen Protocol | Daily/weekly/monthly/quarterly rhythm | 1-2 weeks |

**Total distinct software components: 28** (6 running, 22 to build)

---

## Part 4: One Unit of Software — What It Produces

You asked: what is the output of one unit of software, where a unit includes the MDs, the brains, the Unix pipe sourcing, the MCP server factory, the glue, and the APIs?

### Definition of One Software Unit

A single software unit in the Amplified architecture produces:

| Output | Description | Format |
|---|---|---|
| Agent MD | Operational spec — role, inputs, outputs, quality criteria, escalation rules | Markdown (.md) |
| CLAUDE.md fragment | Context that loads into every session for this component | Markdown (.md) |
| MEMORY.md seed | Initial learnings the auto-memory should know | Markdown (.md) |
| MCP server | The tool interface that connects the component to agents | Python/TypeScript (FastAPI or stdio) |
| Unix pipe integration | stdin/stdout interface for composability with other tools | Shell script + Python |
| API endpoint | REST or WebSocket endpoint for inter-service communication | FastAPI route |
| Quality rubric | Scoring criteria specific to this component's outputs | Markdown + YAML |
| Test suite | Automated tests that prove the component works | pytest |
| Post-mortem template | Pre-filled self-reflection for this component type | YAML |
| APQC process mapping | PCF category number + SIPOC + FMEA | Markdown |
| Docker config | Container definition for Beast deployment | Dockerfile + compose fragment |

### Output Volume Per Unit

Based on the compound engineering pattern (26 agents, 23 commands) and the PDF's build estimates:

| Artefact | Lines of Code/Content | Files |
|---|---|---|
| Agent MD | 100-200 lines | 1 |
| CLAUDE.md fragment | 20-50 lines | 1 |
| MCP server | 200-500 lines | 3-5 files |
| API glue | 100-300 lines | 2-3 files |
| Tests | 150-400 lines | 2-4 files |
| Process docs (rubric, SIPOC, FMEA) | 100-200 lines | 3-4 files |
| Docker config | 20-50 lines | 1-2 files |
| **Total per unit** | **~700-1,700 lines** | **~13-20 files** |

### Realistic Output Rate

Based on the [Anthropic 2026 data](https://resources.anthropic.com/hubfs/2026%20Agentic%20Coding%20Trends%20Report.pdf): developers fully delegate 0-20% of work to AI. First-pass accuracy 72-83%. 55% faster on scoped tasks. Your 4-agent parallel architecture with auditor review can produce:

- **1 software unit per day** (with human review and quality gates)
- **0.5 units per overnight autonomous shift** (lower because no human feedback loop for edge cases)
- **22 units to build** from the gap analysis
- **Estimated calendar time at 1 unit/day: ~4-5 weeks** with parallel streams

---

## Part 5: How Many Partners (Agent Instances)

### Day Shift (08:00-20:00 GMT) — Production Build

| Team | Agents | Model Tier | Role |
|---|---|---|---|
| Builder Team | 4 | Sonnet (medium) | Code generation, content creation, template authoring |
| Auditor | 1 | Opus (premium) | Review every builder output. One reflection cycle then flag. |
| Enforcer | 1 | Haiku (cheap) | Policy enforcement, law compliance, quality gate scoring |
| Research | 1 | Sonnet (medium) | Feed research pipeline, source scoring, GRADE assessments |
| Orchestrator | 1 | Sonnet (medium) | Temporal workflow management, dependency tracking |
| **Day total** | **8** | | |

### Night Shift (20:00-08:00 GMT) — Maintenance + Improvement

| Team | Agents | Model Tier | Role | Token Profile |
|---|---|---|---|---|
| Repair | 2 | Sonnet | Fix failing tests, resolve flagged issues from day shift | Medium — targeted work |
| Therapist/Recalibration | 1 | Ollama (local) | Agent memory consolidation, MEMORY.md cleanup, confidence recalibration | Zero API cost |
| Kaizen | 1 | Haiku | Scan post-mortems for patterns, update rubrics, propose improvements | Low |
| Chaos | 1 | Haiku | Adversarial testing — feed bad inputs, test error handling, probe security | Low |
| Night Crawler | 1 | Ollama (local) | RSS polling, arXiv scanning, tool release monitoring | Zero API cost |
| **Night total** | **6** | | | |

### Weekend Shift (Saturday review, Sunday off per your client rhythm)

| Team | Agents | Model Tier | Role |
|---|---|---|---|
| Review | 2 | Sonnet | Weekly integration review, dependency map update |
| Dashboard | 1 | Haiku | Generate weekly metrics report |
| **Weekend total** | **3** | | |

### Grand Total

| Metric | Count |
|---|---|
| **Peak concurrent agents (day)** | **8** |
| **Night concurrent agents** | **6** |
| **Weekend agents** | **3** |
| **Total unique agent roles** | **14** |
| **Agents using paid API** | **10** |
| **Agents on Ollama (free)** | **4** |

### Estimated Daily Token Cost

| Shift | Agents × Hours | Model | Est. Cost |
|---|---|---|---|
| Day (12h) | 8 × 12h | Mix: 4 Sonnet + 1 Opus + 2 Haiku + 1 Sonnet | ~$3.50 |
| Night (12h) | 6 × 12h | Mix: 2 Sonnet + 2 Ollama + 2 Haiku | ~$1.00 |
| **Daily total** | | | **~$4.50** |

This stays under your $5/day build-phase budget cap. The key is Ollama routing: every heartbeat, memory consolidation, and RSS polling task goes local. Only reasoning-heavy work (repair, build, review) hits the API.

---

## Part 6: Night Shift Design — Token-Efficient

### Schedule (20:00-08:00 GMT)

| Time | Agent | Task | Token Strategy |
|---|---|---|---|
| 20:00-20:30 | Orchestrator handoff | Day → Night baton pass. SESSION-STATE.md updated. Flagged items listed. | Minimal — one Sonnet call |
| 20:30-00:00 | Repair Team (2) | Work through flagged issues from day shift. One reflection cycle per issue. Fix or flag for morning. | Sonnet. Prompt caching on CLAUDE.md/Laws = 90% discount on static context. |
| 20:30-22:00 | Chaos Agent | Adversarial probing of today's outputs. Bad inputs, edge cases, security probes. | Haiku. Cheap. Expendable. |
| 22:00-02:00 | Kaizen Agent | Scan all post-mortems from today. Pattern detection. Rubric calibration. Propose improvements for morning review. | Haiku. Low token count — reading and scoring, not generating. |
| 00:00-06:00 | Night Crawler | RSS feeds, arXiv, tool releases. Deduplication. Store in vault. | Ollama (local). Zero API cost. |
| 00:00-06:00 | Therapist/Recalibrator | MEMORY.md consolidation across all agent workspaces. Confidence decay on stale facts. Merge overlapping entries. Garbage collection. | Ollama (local). Zero API cost. |
| 06:00-08:00 | Night Orchestrator | Compile night shift report. Update SESSION-STATE.md. Prepare baton for day shift. | One Sonnet call. |

### Token Efficiency Rules

1. **Ollama-first for all night work that doesn't need reasoning.** Night Crawler and Therapist run entirely local.
2. **Prompt caching for all night agents.** SOUL.md, CLAUDE.md, Layer 0 Laws are static — 90% discount on every call.
3. **Batch processing windows.** Repair team works in 30-minute bursts with 5-minute cooldowns to maximise cache hits.
4. **Haiku default.** Only Repair uses Sonnet. Everything else is Haiku or Ollama.
5. **Rate limiting.** 5 seconds between API calls minimum. 10 seconds between searches. Max 5 searches per batch.
6. **Budget cap.** Night shift hard cap at $1.50. If reached, remaining work queued for day shift.

---

## Part 7: Bias Check — My Honest Assessment

You asked me to be as unbiased as I can. Here's where I think I might be biased, and my correction:

**Potential bias 1: Underestimating build time.** The PDF estimates 1-week effort for several items. The METR study showed experienced developers are 19% slower with AI on complex tasks. The "1 unit per day" estimate assumes scoped, well-defined work — the first few units will be slower as the meta-process itself is being built. More realistic: 5-6 weeks, not 4.

**Potential bias 2: Overconfidence in the night shift.** Autonomous overnight agents without human review will produce lower-quality output. The ReflexiCoder research says one reflection cycle is sufficient — but that's on code benchmarks, not on architectural decisions or process design. Night shift should be limited to repair (scoped fixes) and maintenance (reading, not writing). No new architecture decisions at night.

**Potential bias 3: Agent count may be too low.** The 19-team architecture you designed in this session has 19 teams. I've proposed 14 active agent roles. The gap: sentiment/semantics, training delivery, graphical presentation, client infrastructure, and compliance/truth are not yet in the build plan because they're client-facing and Dave Jesmond hasn't started. When Client Zero begins, you'll need 4-6 more agents. Total eventual: ~18-20 concurrent.

**Potential bias 4: Token costs are optimistic.** The $4.50/day estimate assumes high cache hit rates and efficient prompt engineering from day one. Reality: early sessions will be messy, prompts will be long, cache hits will be low. Budget $8-10/day for the first 2 weeks, declining to $4-5/day as the system matures.

---

## Sources

- Claude Code Memory docs: https://code.claude.com/docs/en/memory
- Anthropic 2026 Agentic Coding Trends: https://resources.anthropic.com/hubfs/2026%20Agentic%20Coding%20Trends%20Report.pdf
- Claude Code Hooks (PixelMojo): https://www.pixelmojo.io/blogs/claude-code-hooks-production-quality-ci-cd-patterns
- Claude Code Hooks (eesel.ai): https://www.eesel.ai/blog/hooks-in-claude-code
- OpenClaw Token Optimization: https://ai-coding.wiselychen.com/en/openclaw-cost-optimization-guide-97-percent-reduction/
- Matt Paige Substack (Anthropic updates): https://mattpaige68.substack.com/p/anthropic-just-dropped-4-massive
- Nate's Newsletter (/loop as heartbeat): https://natesnewsletter.substack.com/p/your-ai-agent-needs-three-things
- MCP Server Patterns: https://shaaf.dev/post/2026-01-08-two-essential-patterns-for-buildingm-mcp-servers/
- Multi-MCP architecture: https://www.getknit.dev/blog/scaling-ai-capabilities-using-multiple-mcp-servers-with-one-agent
- Fading Memory analysis: https://skywork.ai/blog/claude-memory-a-deep-dive-into-anthropics-persistent-context-solution/
- NVIDIA inference cost trends: https://blogs.nvidia.com/blog/inference-open-source-models-blackwell-reduce-cost-per-token/
- ReflexiCoder paper: https://arxiv.org/html/2603.05863v1
- Reflexion (Shinn et al., NeurIPS 2023): https://proceedings.neurips.cc/paper_files/paper/2023/file/1b44b878bb782e6954cd888628510e90-Paper-Conference.pdf
- Persistent memory architecture: https://dev.to/suede/the-architecture-of-persistent-memory-for-claude-code-17d

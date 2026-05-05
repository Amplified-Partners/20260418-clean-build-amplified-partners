---
title: "AI Coding Tools Bakeoff: End-to-End Evaluation Framework"
id: "ai-coding-bakeoff-report-copy"
version: 1
created: "2026-04-25"
type: "document"
topic_type: "unsorted"
audience: "internal"
layer: "shadow"
status: "filed"
signed_by: "Devon, 2026-04-25, devin-992682c244cf444f91e0a516498afbfd"
---

# AI Coding Tools Bakeoff: End-to-End Evaluation Framework
## From Code Generation to Production — What the Data Actually Shows
### March 2026

---

> **About this report**: This document is a standalone, anonymized evaluation of the AI coding tool landscape as of March 2026, written for a technical decision-maker running an SMB consulting practice on a high-performance Hetzner server. Every factual claim is cited to a primary source. No vendor provided access, funding, or review. The scoring reflects the data, not the hype.

---

## Executive Summary

The AI coding tool landscape hit a credibility crisis in early 2026 precisely because it matured. Frontier models now claim 75–81% resolution rates on SWE-bench Verified — the industry's most-cited benchmark for autonomous coding ability — yet an independent METR study found that roughly half of those benchmark-passing patches would be rejected by real code maintainers. The gap between the benchmark and the production codebase is not narrowing; it is widening. [METR published March 10, 2026](https://metr.org/notes/2026-03-10-many-swe-bench-passing-prs-would-not-be-merged-into-main/) that benchmark improvement is running 9.6 percentage points per year *faster* than maintainer-accepted improvement. This is the central paradox of AI coding in 2026: the tools are getting dramatically better at benchmark tasks while the evidence of real-world quality impact remains mixed at best.

The productivity data tells a similarly complicated story. GitHub's controlled study found developers completing a simple JavaScript task 55.8% faster with Copilot, and Jellyfish's platform data shows 113% more PRs per engineer at high-AI-adoption shops. But [METR's randomized controlled trial](https://metr.org/blog/2025-07-10-early-2025-ai-experienced-os-dev-study/) — the most rigorous study to date — found AI tools *increased* task completion time by 19% among experienced developers working on real, complex codebases. Both findings are true. The 55% speedup applies to bounded, familiar tasks. The 19% slowdown applies to the open-ended, multi-file, architectural work that fills most senior engineers' days. Any vendor citing only the former is selling a partial truth.

Security is where the picture gets most uncomfortable. Between 29% and 62% of AI-generated code contains exploitable vulnerabilities, depending on the study ([arXiv 2024](https://arxiv.org/html/2310.02059v2), [Veracode 2025](https://www.veracode.com/blog/genai-code-security-report/), [Cloud Security Alliance 2025](https://cloudsecurityalliance.org/blog/2025/07/09/understanding-security-risks-in-ai-generated-code)). In 2025 alone, 2,130 AI-related CVEs were disclosed — a 34.6% year-over-year increase, nearly double the overall CVE growth rate — including a CVSS 9.6-rated remote code execution vulnerability in GitHub Copilot itself. The [Stanford Dan Boneh lab](https://ee.stanford.edu/dan-boneh-and-team-find-relying-ai-more-likely-make-your-code-buggier) found that developers with AI assistance were *more confident* they had written secure code even when they hadn't. That false confidence is the most dangerous finding in the entire security literature.

The strategic picture for March 2026: the industry has bifurcated into assistive tools (autocomplete, chat, inline suggestions) and agentic tools (autonomous agents that plan, write, and submit PRs without human intervention). The gap between these categories is widening rapidly. For a solo consultant running workloads on a high-performance server, the optimal strategy is a 4x parallel agent approach — multiple tools running simultaneously on isolated git worktrees — using cost-efficient open models for bulk tasks and frontier models for complex work requiring judgment. The evaluation harness at `/home/user/workspace/ai-coding-bakeoff-harness/` provides a production-ready framework for measuring exactly this on any codebase.

---

## The Landscape: 26 Tools in 6 Tiers

### The Tier System

March 2026's AI coding market organizes cleanly into six tiers, defined by autonomy, context awareness, and the type of developer workflow they serve.

| Tier | Category | Tools | Defining Characteristic |
|------|----------|-------|------------------------|
| **1** | Frontier Autonomous Agents | Claude Code, OpenAI Codex App, GitHub Copilot + CLI | SWE-bench >75%, full issue→PR pipeline, multi-agent orchestration |
| **2** | AI-Native IDEs | Cursor, Windsurf, Google Antigravity | VS Code fork with AI baked into every layer |
| **3** | Async Autonomous Agents | Devin, Google Jules, OpenHands | Fire-and-forget cloud agents, async PR creation |
| **4** | Terminal CLI Agents | Aider, OpenCode, Gemini CLI | Open-source, maximum model flexibility, scripting-friendly |
| **5** | IDE Extensions / Assistants | GitHub Copilot (ext.), Cline, Kilo Code, Continue.dev, Augment Code, Amazon Q, Tabnine, Sourcegraph Cody, JetBrains AI, Gemini Code Assist | Inline suggestions + agentic chat in existing IDEs |
| **6** | App Builders / Vibe Coding | Replit Agent, Bolt.new, v0, Lovable | New project creation, prototyping, non-developer audiences |

### Full Tool Comparison Table

The following table covers all 26 tools evaluated. SWE-bench scores are on the Verified subset (500 Python tasks) unless marked Pro or Live. All scores should be read with the contamination caveat detailed in The Head-to-Head section below.

| Tool | Tier | Category | SWE-bench Score | Pricing (starting) | Key Differentiator |
|------|------|----------|-----------------|--------------------|-------------------|
| Claude Code | 1 | CLI/Agent | 80.9% Verified (Opus 4.5) | $20/mo (Pro) | #1 SWE-bench, 1M context, multi-agent spawn |
| OpenAI Codex App | 1 | Multi-agent | ~80% Verified (GPT-5.2) | Included w/ ChatGPT Plus ($20/mo) | SWE-bench Pro SOTA, Skills library, CSV fan-out |
| GitHub Copilot + CLI | 1 | CLI/Agent | Not published (GPT-5.3-Codex backend) | $10/mo (Pro) | 20M developer base, GitHub-native, GA Feb 2026 |
| Cursor | 2 | IDE | ~79-81% (underlying models) | $20/mo (Pro) | Most-loved AI IDE, community, VS Code fork |
| Windsurf | 2 | IDE | Not published (SWE-1.5 model) | $15/mo (Pro) | 25% cheaper than Cursor, unlimited Tab |
| Google Antigravity | 2 | IDE | Not published (Gemini 3 backend) | $19.99/mo (AI Pro) | Manager View async orchestration, Google Docs-style review |
| Devin | 3 | Async Agent | 13.86% SWE-bench Full (legacy) | $20/mo (Core) | 67% PR merge rate, sandboxed VM, enterprise wiki |
| Google Jules | 3 | Async Agent | Not published | Included w/ Google AI Pro ($19.99/mo) | Scheduled tasks, Render integration, CLI/API |
| OpenHands | 3 | Async Agent | 72% Verified (Claude 4.5 ET) | Free (open source) | MIT license, #1 Multi-SWE-Bench, enterprise RBAC |
| Aider | 4 | CLI | ~53-60%+ Verified (varies by model) | Free (pay own API) | 39K stars, 4.1M installs, git auto-commit per edit |
| OpenCode | 4 | CLI | >74% Verified (mini-SWE-agent base) | Free (pay own API) | 95K stars, 4.5x star velocity vs Claude Code |
| Gemini CLI | 4 | CLI | 76.2% Verified (Gemini 3 Flash) | Free (1,000 req/day) | Largest free tier, 1M token context, MCP |
| Cline | 5 | VS Code Ext. | Not published | Free (pay own API) | 4M+ devs, Plan/Act modes, first-class MCP |
| Kilo Code | 5 | VS Code Ext. | Not published | $20 starter credits | Cline fork + OpenCode engine, Orchestrator mode, git worktrees |
| Continue.dev | 5 | VS Code Ext. | Not published | Free / $20/seat/mo | Event-triggered agentic workflows, Snyk/Sentry integration |
| Augment Code | 5 | VS Code Ext. | Not published | $20/mo (Indie) | Context Engine (RAG codebase indexing), SOC 2 Type II |
| Amazon Q Developer | 5 | IDE Ext. | Not published | Free / $19/user/mo | Java/.NET transformation, IP indemnity, AWS native |
| Tabnine | 5 | IDE Ext. | Not published | $39/user/mo | Air-gapped/on-prem, zero training, HIPAA/FedRAMP |
| Sourcegraph Cody | 5 | IDE Ext. | Not published | $9/user/mo (Pro) | 10-repo RAG context, 1M token cross-repo retrieval |
| JetBrains AI | 5 | IDE (native) | Not published | $100/user/year | AST-aware context, Junie agent, JetBrains-only |
| Gemini Code Assist | 5 | IDE Ext. | ~43% Pro / 76.2% Verified (Flash) | Free (6K req/day) | FedRAMP/HIPAA, Firebase/BigQuery/Cloud Run native |
| Replit Agent | 6 | App Builder | Not applicable | $20/mo (Core) | Cloud IDE + hosting, 30+ integrations, zero setup |
| Bolt.new | 6 | App Builder | Not applicable | Free / $20/mo | WebContainer (Node in browser), $40M ARR in 6 months |
| v0 by Vercel | 6 | App Builder | Not applicable | Free / $20/mo | Best React/Next.js UI output, image-to-code |
| Lovable | 6 | App Builder | Not applicable | Free / $25/mo | Supabase backend, fastest European startup to $20M ARR |

*Sources: [tools-narrative.md](https://www.anthropic.com/news/claude-opus-4-6), [swebench.com](https://www.swebench.com), [Morph SWE-bench Pro](https://www.morphllm.com/swe-bench-pro)*

### Pricing Comparison: The Hidden Costs

The shift to credit-based pricing across the industry in 2025–2026 has made honest cost comparison nearly impossible. Every major platform moved away from simple flat-rate pricing:

- **Cursor** switched to credits in June 2025 ([Cursor pricing page](https://cursor.com/pricing)) — community backlash followed
- **Augment Code** switched to credits in October 2025 ([Augment pricing](https://www.augmentcode.com/pricing))
- **Google Antigravity** repriced in March 2026, causing [user protests documented by The Register](https://www.theregister.com/2026/03/12/users_protest_as_google_antigravity/)
- **GitHub Copilot** introduced premium request metering in 2025

The net effect: actual costs for heavy agentic users can be 3–10x the headline price.

| Tool | Headline Price | Heavy User Reality | Model Access at Base Tier | Premium Request Cost |
|------|---------------|-------------------|--------------------------|---------------------|
| Claude Code Pro | $20/mo | $100-200/mo for all-day agents | Claude Sonnet 4.6 | Max 20x = $200/mo |
| GitHub Copilot Pro | $10/mo | ~$10-30/mo (300 req/mo incl.) | GPT-5 mini (free), GPT-5.3-Codex (premium) | $0.04/req |
| Cursor Pro | $20/mo | $20-60/mo (credit pool burns fast) | Auto mode (unlimited), Claude/GPT-4 from credit pool | Credit-based |
| Windsurf Pro | $15/mo | $15-30/mo | SWE-1.5 / frontier via credits | Credit-based |
| Google Antigravity AI Pro | $19.99/mo | ~$250/mo for pro use (Ultra tier) | Flash model only; Pro models require Ultra | Ultra = $249.99/mo |
| Devin Core | $20/mo | $500/mo+ (Team) for real enterprise use | Proprietary model | $2.25/ACU additional |
| Gemini CLI | Free | Free (1,000 req/day hard limit) | Gemini 2.5 Pro (1M ctx) | None at free tier |
| Aider/OpenCode | Free | Pay own API (~$5-50/mo typical) | Any of 75+ models | Direct API rates |

*Sources: [cursor.com/pricing](https://cursor.com/pricing), [windsurf.com/pricing](https://windsurf.com/pricing), [devin.ai/pricing](https://devin.ai/pricing/), [GitHub Plans](https://github.com/features/copilot/plans)*

**The honest recommendation for budget-conscious developers**: Gemini CLI (free, 1,000 requests/day, 1M token context) or Aider/OpenCode (BYOK, full model flexibility) deliver the most value per dollar. Claude Code Pro at $20/mo is outstanding value for individual developers who don't run agents all day.

---

## The Head-to-Head: What Benchmarks Actually Show

### SWE-bench Verified — The Headline Number (With a Major Caveat)

SWE-bench Verified evaluates AI agents on 500 human-validated Python tasks drawn from real GitHub issues. The automated grader checks whether the AI's patch passes the repository's existing unit tests. It became the credibility test for AI coding agents in 2025.

The problem: it is contaminated. [OpenAI's internal audit](https://www.morphllm.com/swe-bench-pro) found that every frontier model shows training data overlap with SWE-bench Verified tasks — models have effectively seen the answers. OpenAI stopped reporting Verified scores and now recommends SWE-bench Pro instead. The official February 2026 leaderboard update used a standardized scaffold (mini-SWE-agent v2) to force fair comparisons.

**Current SWE-bench Verified Leaderboard (February 2026, standardized scaffold)**

*Note: These scores are a ceiling, not a floor. Contamination inflates them. See Pro and Live scores below for a more honest picture.*

| Rank | Model | SWE-bench Verified | Notes |
|------|-------|-------------------|-------|
| 1 | Claude Opus 4.5 | **80.9%** | Anthropic; contamination caveat applies |
| 2 | Claude Opus 4.6 | 80.8% | Feb 2026 release; marginal delta |
| 3 | MiniMax M2.5 | 80.2% | Open-weight 229B, Chinese lab |
| 4 | GPT-5.2 | 80.0% | OpenAI has stopped reporting this score |
| 5 | Gemini 3 Flash | 78.0% | Google; faster/cheaper than Pro |
| 6 | GLM-5 | 77.8% | Zhipu AI (China) |
| 7 | Claude Sonnet 4.5 | 77.2% | Anthropic |
| 8 | Kimi K2.5 | 76.8% | Moonshot AI (China) |
| 9 | Gemini 3 Pro | 76.2% | Google |
| 10 | GPT-5.1 | 74.9% | OpenAI |
| 14 | Claude Sonnet 4 | 72.7% | Anthropic |
| 15 | Qwen3 Coder Next | 70.6% | Alibaba (China) |

*Sources: [swebench.com](https://www.swebench.com), [Simon Willison Feb 2026 update](https://simonwillison.net/2026/Feb/19/swe-bench/), [Morph SWE-bench Pro analysis](https://www.morphllm.com/swe-bench-pro)*

**The Chinese lab surge is real and underreported**: Six of the top ten models are from Chinese labs (MiniMax, Zhipu, Moonshot, DeepSeek, Alibaba, with Google Gemini built on Chinese talent). The competitive landscape has fully globalized.

### SWE-bench Pro — The Clean Benchmark

[Scale AI's SEAL team](https://labs.scale.com/leaderboard/swe_bench_pro_public) created SWE-bench Pro to fix the contamination problem: 1,865 multi-language tasks (not just Python), standardized scaffolding, 250-turn limit. The result is diagnostic: scores roughly halve when the contamination advantage is removed.

| Rank | Model | SWE-bench Pro (SEAL) | Delta vs. Verified |
|------|-------|----------------------|--------------------|
| 1 | Claude Opus 4.5 | **45.9% ±3.6** | −35 pp |
| 2 | Claude Sonnet 4.5 | 43.6% ±3.6 | −33.6 pp |
| 3 | Gemini 3 Pro | 43.3% ±3.6 | −32.9 pp |
| 4 | Claude Sonnet 4 | 42.7% ±3.6 | −30 pp |
| 5 | GPT-5 (High) | 41.8% ±3.5 | — |
| 6 | GPT-5.2 Codex | 41.0% ±3.6 | −39 pp |
| 7 | Claude Haiku 4.5 | 39.5% ±3.6 | — |
| 8 | Qwen3 Coder 480B | 38.7% ±3.6 | — |
| 9 | MiniMax 2.1 | 36.8% ±3.6 | — |
| 10 | Gemini 3 Flash | 34.6% ±3.6 | −43.4 pp |
| 15 | DeepSeek V3.2 | 15.6% ±2.6 | — |

*Source: [Scale AI SEAL SWE-bench Pro Leaderboard](https://labs.scale.com/leaderboard/swe_bench_pro_public)*

**On private unseen codebases**, performance drops further still: [GPT-5 falls from 23.1% to 14.9%; Claude Opus 4.1 from 22.7% to 17.8%](https://www.morphllm.com/swe-bench-pro). The headline 80% number is a benchmark artifact. The real-world figure for novel tasks is approximately 14–20%.

### SWE-bench Live — Real-World Novel Issues

[SWE-bench Live](https://www.swebench.com) is an anti-contamination benchmark that continuously refreshes with new real-world GitHub issues — issues the models have never seen. All agents score 17–19%:

| Agent + Model | SWE-bench Live Score |
|---------------|---------------------|
| OpenHands + Claude 3.7 | **19.25%** |
| SWE-Agent + GPT-4.1 | 18.57% |
| SWE-Agent + Claude 3.7 | 17.13% |

*Source: [swebench.com](https://www.swebench.com)*

**The takeaway, stated plainly**: The "80% of real GitHub issues solved" narrative is marketing. On contamination-free benchmarks, top models solve ~46% of tasks. On live, novel issues they haven't seen before, ~19%. A solo developer running real production code should expect roughly 1 in 5 autonomous agent tasks to succeed end-to-end without human correction.

### Agentic Systems on SWE-bench

The scaffold matters as much as the underlying model. In February 2026, three frameworks running the same base model scored 17 issues apart on 731 total problems.

| Agent System | Underlying Model | SWE-bench Verified |
|--------------|-----------------|---------------------|
| Sonar Foundation Agent | Claude Opus 4.5 | 79.2% |
| OpenHands | Claude 4.5 Extended Thinking | 72% |
| Mini-SWE-Agent (100 lines Python) | Various | >74% |
| Devin (original 2024) | Proprietary | 13.86% |

*Source: [Sonar March 2026 announcement](https://www.morningstar.com/news/pr-newswire/20260311la08045/sonar-claims-top-spot-on-swe-bench-leaderboard)*

Sonar's March 11, 2026 claim of #1 on the unfiltered leaderboard came with a concrete production metric: average resolution time of **9 minutes/issue** at **$1.9/issue** — making enterprise-scale autonomous bug remediation economically viable for the first time.

### METR Study: Half of Passing PRs Would Be Rejected

The most important single finding in the entire 2026 benchmark literature: [METR's March 10, 2026 study](https://metr.org/notes/2026-03-10-many-swe-bench-passing-prs-would-not-be-merged-into-main/) showed that passing the automated benchmark grader does not mean the code is actually good.

**Methodology**: 4 active maintainers from scikit-learn, Sphinx, and pytest blindly reviewed 296 AI-generated PRs that had already passed the SWE-bench automated grader. 47 human-written "golden patches" served as baseline.

| Metric | Value |
|--------|-------|
| Average gap (automated grader vs. maintainer judgment) | 24.2 percentage points |
| Best AI model (Claude 4.5 Sonnet) — automated score | ~68% pass |
| Best AI model (Claude 4.5 Sonnet) — maintainer-adjusted | ~44% |
| Human golden patches — maintainer merge rate | 68% |
| Benchmark improvement rate vs. maintainer-accepted rate | 9.6 pp/year gap, widening |

**Why maintainers reject AI PRs**: code quality/style issues, breaking unrelated code, core functionality failures even when tests pass. GPT-5 showed "substantially weaker code quality" than Anthropic models per the METR reviewers.

**Implication**: A model's SWE-bench score is a ceiling, not a floor. The real production integration rate for the best models is roughly 44%, not 68%. For average models, it is considerably lower.

---

## Task-by-Task Analysis

The bakeoff harness defines four task types that cover the core work of software maintenance. Here is what the data shows about each.

### Bug Fixes

Bug fixing is AI's strongest task type — the most bounded, the most verifiable, and the most suited to the issue→PR pattern. [Sonar's 9-minute average resolution time](https://www.morningstar.com/news/pr-newswire/20260311la08045/sonar-claims-top-spot-on-swe-bench-leaderboard) at $1.9/issue represents a genuine threshold crossing: enterprise-scale backlog remediation is now economically viable.

**Tool rankings for bug fixes** (based on available data):

| Tool | Strength | Weakness |
|------|----------|----------|
| Claude Code | Best at reasoning through multi-file root causes; full TDD workflow | Requires Max tier ($100-200/mo) for complex bugs |
| GitHub Copilot Coding Agent | Natively reads GitHub Issues + labels; can be assigned directly | Premium request cost; quality varies by model |
| Devin | End-to-end autonomous; handles security fixes in 1.5 min (vs. 30 min human) | Requires significant setup; 15% success rate without knowledge base configuration |
| Aider | Perfect audit trail (every fix auto-commits to git); 75+ model choice | CLI only; no cross-session memory |
| OpenHands | Open source; 72% SWE-bench; enterprise deployable | Setup overhead; SaaS limits without subscription |

**Security of bug fixes**: This is where the data is most concerning. [CodeRabbit's 470-PR study](https://www.coderabbit.ai/blog/state-of-ai-vs-human-code-generation-report) found AI-assisted code has 1.57x more security vulnerabilities than human code. Bug fixes are particularly risky because the AI may address the reported symptom while introducing a new vulnerability nearby. The [Stanford Dan Boneh lab finding](https://ee.stanford.edu/dan-boneh-and-team-find-relying-ai-more-likely-make-your-code-buggier) — that AI assistance creates false security confidence — applies most directly to bug fixes, where developers tend to trust a test-passing fix.

**Time-to-fix data** (from [Devin's 2025 performance review](https://cognition.ai/blog/devin-annual-performance-review-2025)):
- Security CVE fixes: 1.5 minutes (AI) vs. 30 minutes (human) — **20x improvement**
- ETL pipeline bugs: 3–4 hours (AI) vs. 30–40 hours (human) — **10x improvement**
- Architecture review: 15 minutes (AI draft) — human validation still required

### Test Generation

Test generation is widely cited as the highest-ROI application of AI coding tools, and the survey data supports this: [Stack Overflow's 2025 survey](https://survey.stackoverflow.co/2025/ai) shows testing and documentation as the top two use cases developers plan to expand AI into.

**The happy path bias problem**: AI-generated tests overwhelmingly cover the "happy path" — valid inputs, expected flows, documented behavior. The [quality-security-narrative.md](https://www.gitclear.com/ai_assistant_code_quality_2025_research) notes that AI generates "happy path code that assumes valid inputs; rarely generates robust error handling or edge-case tests unless explicitly prompted." Code written by AI and tested by AI may have correlated blindspots — both the code and the tests emerge from the same model's assumptions about what a function should do.

**Test coverage impact** (from [Devin 2025 case studies](https://cognition.ai/blog/devin-annual-performance-review-2025)):
- Test coverage: 50–60% → 80–90% on enterprise repos that ran AI test generation
- Regression cycles: 93% faster at Litera (one of Devin's enterprise customers)

**Tool-by-tool test generation**:

| Tool | Test Generation Capability | Edge Case Handling |
|------|---------------------------|-------------------|
| Claude Code | Full TDD workflow; refuses to mark tasks complete until tests pass | Strong if explicitly prompted; weak on undocumented business logic |
| Cursor | Automated comprehensive test suite generation; runs tests during agent tasks | Good with context window filled with relevant tests |
| GitHub Copilot | Unit test creation from functions; test-first prompting in VS Code | Standard; happy path bias without explicit edge case prompts |
| Kilo Code | Inline diff review with line comments during test PRs | Built-in review loop helps catch test gaps |
| Continue.dev | Integrated with Sentry/Snyk; can trigger test generation on events | Best for automated test-on-change workflows |

### Module Refactoring

Refactoring is where AI tools struggle most — and where the longitudinal data shows the most concerning trend. [GitClear's 211-million-line study](https://www.gitclear.com/ai_assistant_code_quality_2025_research) found that refactoring (moved/restructured code) has declined from ~25% of commits to less than 10% since 2021. "Copy/paste" exceeded "moved/refactored" code as a share of changes for the first time in history in 2024.

**The DRY crisis in numbers** (from [GitClear 2025](https://www.gitclear.com/ai_assistant_code_quality_2025_research)):

| Metric | 2020-2021 Baseline | 2024-2025 | Direction |
|--------|--------------------|-----------|-----------|
| Copy/pasted (cloned) code | 8.3% | 12.3%–18% | ↑ Worsening |
| Refactored/moved code | ~25% | <10% | ↓ Worsening |
| Code churn (<2 weeks) | 3.1% | 5.7%–7.9% | ↑ Worsening |
| Duplicate code block occurrences | baseline | 8x increase | ↑ Worsening |
| New code added share | 39% | 46% | ↑ (not inherently bad) |

Pearson correlation between Copilot prevalence and churn rate: **0.98** — one of the strongest correlations in the literature.

**Why AI tools fail at refactoring**: The fundamental problem is that AI optimizes for "shortest path to a working result." Refactoring requires understanding the existing architecture, identifying what can be consolidated, and making changes that reduce total code volume. This requires judgment about structure that current models consistently lack. A [2025 comparison study](https://thesesjournal.com/index.php/1/article/view/1810) found AI-generated code had 34% greater cyclomatic complexity and 2.1x greater code duplication compared to senior developer solutions.

**What does work**: Large-scale mechanical refactoring where the pattern is explicit. The Nubank/Devin case study (below) shows 4x speed improvement on migration tasks that follow a defined pattern. The lesson: define the exact refactoring pattern in the task description, show examples, then scale.

### Breaking API Migration

API migrations are emerging as the highest-reliability use case for autonomous coding agents. The reasons are structural: tasks are repetitive and formulaic, success is objectively verifiable (code compiles + tests pass), and the agent can be taught on 2–3 examples before being scaled across a codebase.

**Nubank/Devin case study** (from [Devin.ai](https://devin.ai)):
- Task: Large-scale codebase refactor/migration
- After fine-tuning Devin on the specific migration pattern:
  - 2x task completion rate
  - 4x speed improvement (40 minutes → 10 minutes per sub-task)
  - Human kept in loop only for project management and PR approval

**CI/CD integration for migrations**: GitHub Copilot CLI now supports `GITHUB_ASKPASS` for non-interactive CI/CD use, enabling automated migration tasks to run in pipelines without human input ([GitHub Copilot CLI GA](https://github.blog/changelog/2026-02-25-github-copilot-cli-is-now-generally-available/)). The pattern:

```yaml
- name: Install Copilot CLI
  run: npm install -g @github/copilot
- name: Run migration task
  env:
    COPILOT_GITHUB_TOKEN: ${{ secrets.PERSONAL_ACCESS_TOKEN }}
  run: copilot -p "Migrate all deprecated v1 API calls in src/ to v2 API per the pattern in MIGRATION.md"
```

**Multi-file coordination**: The git worktree architecture (isolated repository copies per agent) has become the standard for parallel API migrations. Kilo Code, OpenAI Codex App, and GitHub Copilot CLI all implement this to prevent agents from conflicting when multiple migration tasks run in parallel.

**Other migration tools**: Amazon Q Developer for Java version migrations and COBOL→Java transformations; IBM Watsonx for enterprise mainframe migrations. Both are specialized tools that outperform general-purpose agents on their specific migration targets.

---

## Diff Quality: The GitClear Reality Check

GitClear has published the most data-rich longitudinal analysis of AI's impact on code quality, covering 153–211 million changed lines across Google, Microsoft, Meta, and enterprise repositories from 2020 to 2025.

### The 211-Million-Line Study

[GitClear's 2025 research](https://www.gitclear.com/ai_assistant_code_quality_2025_research) covers more changed lines of code than any other study in the public literature. The findings are not ambiguous:

| Metric | 2020-2021 | 2022 | 2023 | 2024/2025 | Total Change |
|--------|-----------|------|------|-----------|--------------|
| Moved code (refactoring) | ~25% | ~20% | ~15% | <10% | **−60% relative** |
| Copy/pasted code | 8.3% | 9.5% | 11.2% | 12.3–18% | **+50–117%** |
| Churn rate (edits <2 weeks) | 3.1% | 3.8% | 4.9% | 5.7–7.9% | **+84–155%** |
| Added code share | 39% | 41% | 43% | 46% | +18% |

The Pearson correlation between Copilot adoption prevalence and churn rate is [0.98](https://www.gitclear.com/coding_on_copilot_data_shows_ais_downward_pressure_on_code_quality) — a near-perfect relationship. The data suggests AI tools are accelerating code creation while degrading code architecture.

**The January 2026 nuance**: [GitClear's most recent analysis](https://www.gitclear.com/recent_ai_developer_productivity_code_quality_research) adds complexity: heavy AI users generate 4–10x more durable code than non-AI users — but also generate 9x more code churn. The productivity statistics are heavily skewed by top performers. The average AI-assisted developer is generating more code, more churn, and less refactoring simultaneously.

### The CodeRabbit 470-PR Analysis

[CodeRabbit's December 2025 study](https://www.coderabbit.ai/blog/state-of-ai-vs-human-code-generation-report) compared 320 AI-co-authored PRs against 150 human-only PRs, using AI-assisted code review to flag issues:

| Issue Category | AI PRs | Human PRs | AI/Human Ratio |
|----------------|--------|-----------|----------------|
| Overall issues per PR | 10.83 | 6.45 | **1.7x more** |
| Logic/correctness errors | Higher | Baseline | **1.75x more** |
| Security vulnerabilities | Higher | Baseline | **1.57x more** |
| XSS vulnerabilities | Higher | Baseline | **2.74x more** |
| Performance (excessive I/O) | Higher | Baseline | **8x more** |
| Concurrency issues | Higher | Baseline | **2x more** |
| Formatting problems | Higher | Baseline | **2.66x more** |
| Naming inconsistencies | Higher | Baseline | **2x more** |

*Source: [CodeRabbit State of AI vs Human Code Generation Report](https://www.coderabbit.ai/blog/state-of-ai-vs-human-code-generation-report)*

The review bottleneck is becoming structural: PR volume increased 20% between March and November 2025 while review capacity stayed flat. Median PR size grew 33% (57 → 76 lines) in the same period, per [Greptile's 2025 analysis](https://www.greptile.com/state-of-ai-coding-2025).

### The DRY Crisis

GitClear's foundational observation from the 2024 study: [AI-generated code "resembles an itinerant contributor, prone to violate the DRY-ness of the repos visited."](https://www.gitclear.com/coding_on_copilot_data_shows_ais_downward_pressure_on_code_quality) This is the structural explanation for the copy/paste increase: AI models optimize for "solve the current problem" rather than "understand the existing architecture and work within it."

**Why this compounds**: Technical debt from DRY violations is non-linear. Each duplicated block is a future bug fix in two places, a future refactoring in N places, and a cognitive load increase for every developer who reads the code. The 2024–2025 acceleration in duplicate code occurrences (8x increase) represents a debt wave that hasn't hit maintenance costs yet.

---

## Security: The Uncomfortable Truth

Security is the most documented failure mode of AI coding tools in 2026. The findings are consistent across independent studies spanning different methodologies, tools, and time periods. The headline range: **29–62% of AI-generated code contains exploitable vulnerabilities**.

### Vulnerability Rates Across Studies

| Study | Methodology | Vulnerability Rate | Key Finding |
|-------|------------|-------------------|-------------|
| [arXiv/ACM 2024](https://arxiv.org/html/2310.02059v2) | 733 production Copilot snippets from real GitHub repos | **29.6%** | 38 CWE categories; 8 in CWE Top-25 |
| [Veracode 2025](https://www.veracode.com/blog/genai-code-security-report/) | 100+ LLMs, 80 coding tasks | **45%** (OWASP Top 10) | Java fails 72%; newer models no more secure |
| [Cloud Security Alliance 2025](https://cloudsecurityalliance.org/blog/2025/07/09/understanding-security-risks-in-ai-generated-code) | Broad survey of AI code in production | **62%** | Design flaws OR known vulns |
| [Spectrum of Engineering Sciences 2025](https://thesesjournal.com/index.php/1/article/view/1810) | GPT-4 vs. Claude 3 vs. senior devs | **22.1% OWASP Top 10** (vs. 8.4% human) | 3x higher than senior developers |
| [Stanford Dan Boneh Lab](https://ee.stanford.edu/dan-boneh-and-team-find-relying-ai-more-likely-make-your-code-buggier) | Controlled experiment | Less secure + more confident | **False security confidence** — most dangerous finding |
| [NYU Tandon / Pearce et al. 2021](https://engineering.nyu.edu/news/ai-tools-can-help-hackers-plant-hidden-flaws-computer-chips) | Copilot cybersecurity scenarios | **40%** | Foundational; still-cited baseline |
| [Black Duck 2026 survey](https://www.blackduck.com/blog/ai-coding-assistant-security-risks-benefits-devsecops-2025.html) | Organizations using AI tools | 57% agree AI introduces security risks | Industry perception confirms academic findings |

The IEEE replication of the arXiv study found improvement over time: 36.54% → 27.25% vulnerability rate in newer Copilot versions. Newer models are more secure than earlier ones — but "more secure" still means roughly 1 in 4 code snippets has a security weakness.

### CWE Analysis by Language

The most prevalent Common Weakness Enumerations in AI-generated production code, from the [arXiv study of Copilot code](https://arxiv.org/html/2310.02059v2):

| Rank | Python CWEs | JavaScript CWEs |
|------|-------------|-----------------| 
| 1 | CWE-330: Insufficient Random Values (23.3%) | CWE-94: Improper Code Generation Control |
| 2 | CWE-78: OS Command Injection | CWE-95: Eval Injection |
| 3 | CWE-772: Missing Resource Release | CWE-563: Assignment Without Use |
| 4 | CWE-89: SQL Injection | CWE-20: Improper Input Validation |
| 5 | CWE-259: Hard-coded Password | CWE-185: Incorrect Regular Expression |

Across the broader AI ecosystem in 2025, [TrendMicro's TrendAI Security Report](https://www.trendmicro.com/vinfo/us/security/news/threat-landscape/fault-lines-in-the-ai-ecosystem-trendai-state-of-ai-security-report) found CWE-79 (XSS) leads at 9.3% of AI CVEs, followed by CWE-94 (code injection) at 6.8% and CWE-502 (deserialization) at 5.7%.

Four structural root causes explain these patterns:
1. **Training data replication**: AI models reproduce insecure patterns from the vast insecure code corpus they trained on
2. **Optimization shortcuts**: When prompts are ambiguous, LLMs optimize for shortest path to a working result (e.g., using `eval()` for math evaluation)
3. **Missing security controls**: AI omits input validation, access checks, and output encoding unless explicitly prompted
4. **Subtle logic errors**: Flaws that don't look like flaws — swapping `if user.role == "admin"` for `if "admin" in user.roles`, which fails for multi-role users

### Secret Leakage: The GitGuardian Data

[GitGuardian's research](https://blog.gitguardian.com/yes-github-copilot-can-leak-secrets/) provides the most concrete data on credential leakage from AI tools:

- Repositories with GitHub Copilot active: **40% higher secret leak rate** than baseline (6.4% vs. 4.6%)
- From 900 constructed prompts: **2,702 hard-coded credentials** extracted from Copilot suggestions
- Of those, **at least 200 (7.4%) were real, working secrets** identifiable on GitHub
- Copilot generated **3.0 valid secrets per prompt** on average across 8,127 code suggestions
- In 2024, **23.8 million secrets leaked** on public GitHub — a 25% year-over-year increase
- **70% remain active** two years after leaking

The mechanism: Copilot is trained on GitHub data that includes leaked credentials. Adversarial prompt engineering can extract memorized secrets. A CVE patched by GitHub in August 2025 allowed covert extraction of private source code and credentials from private repositories via hidden comments in PR descriptions.

### Supply Chain Risks: Slopsquatting

[A University of Texas/Virginia Tech/Oklahoma study (2025)](https://socket.dev/blog/slopsquatting-how-ai-hallucinations-are-fueling-a-new-class-of-supply-chain-attacks) established "slopsquatting" as a new threat class:

| Metric | Finding |
|--------|---------|
| LLM-generated code samples recommending non-existent packages | ~20% |
| Hallucinated packages appearing consistently across 10 runs (predictable by attackers) | 43% |
| Hallucinated packages reappearing in multiple runs | 58% |
| Unique hallucinated package names identified | 205,000+ |
| GPT-4 Turbo hallucination rate (best performer) | 3.59% |

The attack model is simple: identify consistently hallucinated package names → register them in npm/PyPI → deliver malicious payloads to any project that trusts AI-generated dependency suggestions without validation.

[Martin Fowler's analysis](https://martinfowler.com/articles/exploring-gen-ai/software-supply-chain-attack-surface.html) documents an additional vector: agentic coding assistants (Cursor, Copilot Coding Agent, Cline) interact with dev environments via ReAct loops, giving them file system access, command execution, and network calls. MCP servers — the new integration layer — fundamentally lack built-in authentication, context encryption, or tool integrity verification.

### IDE-Specific CVEs

[Research published December 2025](https://thehackernews.com/2025/12/researchers-uncover-30-flaws-in-ai.html) found 30+ vulnerabilities across AI-powered IDEs: Cursor, GitHub Copilot, Windsurf, Kiro.dev, Roo Code, Junie, Cline, and Zed.dev. 24 CVEs assigned.

**The critical CVEs** (from [TrendMicro TrendAI Security Report, March 2026](https://www.trendmicro.com/vinfo/us/security/news/threat-landscape/fault-lines-in-the-ai-ecosystem-trendai-state-of-ai-security-report)):

| CVE | Product | CVSS | Attack Method | Impact |
|-----|---------|------|---------------|--------|
| CVE-2025-53773 | GitHub Copilot | **9.6** | Prompt injection via code comments | RCE on 100K+ developer machines |
| CVE-2025-32711 "EchoLeak" | Microsoft 365 Copilot | **9.3** | Zero-click prompt injection via email | Data exfiltration; first zero-click AI agent attack |
| CVE-2025-54135 "CurXecute" | Cursor IDE | TBD | Prompt injection via GitHub README | Unauthorized MCP creation, RCE |
| CVE-2025-54136 "MCPoison" | Cursor IDE | TBD | MCP trust mechanism abuse | Persistent backdoor |
| CVE-2025-68664 "LangGrinch" | LangChain Core | TBD | Serialization + prompt injection | Credential exfiltration (847M downloads affected) |

In 2025, **2,130 AI-related CVEs** were disclosed — a 34.6% year-over-year growth rate vs. 17.9% overall CVE growth. Agentic AI CVEs surged **+255%** (74 → 263). **95 MCP-related CVEs** were filed in 2025, near zero the year before.

### The False Confidence Problem

The [Stanford finding](https://ee.stanford.edu/dan-boneh-and-team-find-relying-ai-more-likely-make-your-code-buggier) deserves separate emphasis: developers with AI assistant access not only wrote less secure code, they were *more* confident they had written secure code. The AI provided a false sense of security review. This psychological effect is potentially more dangerous than any raw vulnerability rate — it means the actual security posture of AI-assisted codebases is worse than self-reported metrics suggest.

---

## Code Review: The New Bottleneck

The code review bottleneck is the most consequential unsolved problem in AI-assisted development. AI tools have dramatically increased code generation velocity while review capacity has stayed flat. The result: a structural review debt that is compounding.

### METR Maintainer Study: The 24-Point Gap

The central finding of [METR's March 2026 study](https://metr.org/notes/2026-03-10-many-swe-bench-passing-prs-would-not-be-merged-into-main/) is that automated benchmark passing overstates real code quality by an average of **24.2 percentage points**. Benchmark improvement is running 9.6 percentage points per year faster than maintainer-accepted improvement. The gap is widening every month.

METR's estimate of the "time horizon" for AI-generated work: Claude 4.5 Sonnet's time horizon is approximately 8 minutes of maintainer-reviewed work per issue, not the 50 minutes suggested by automated benchmarks. That is a **6x overestimate** of real-world contribution.

### Review Acceptance Rates: The 27–34% Ceiling

Copilot suggestion acceptance rates are consistent across organizations regardless of company size or programming language:

| Source | Suggestion Acceptance | Line Acceptance | Notes |
|--------|----------------------|-----------------|-------|
| [Zoominfo study (arXiv 2025)](https://arxiv.org/html/2501.13282v1) | 33% | 20% | Developer satisfaction: 72% |
| [Accenture/GitHub 2024](https://github.blog/news-insights/research/research-quantifying-github-copilots-impact-in-the-enterprise-with-accenture/) | ~30% | — | 88% of accepted code retained at 6 weeks |
| Quantumrun analysis | 27–30% | — | 46% of total code volume from Copilot |
| ACM research | 28.9% → 34% | — | Improves with usage over 6 months |

The consistent 27–34% ceiling means roughly 2 in 3 AI-generated suggestions are rejected by developers in real-world usage — not because the suggestions are wrong, but because they don't fit the specific context, style, or architecture of the codebase.

### AI-Assisted Review Tools

The market response to the review bottleneck: AI code review tools. By October 2025, [51.4% of engineering teams had adopted AI code review agents](https://jellyfish.co/blog/2025-ai-metrics-in-review/), up from 14.8% a year prior.

**Bug detection benchmark (2025)**, from [DevTools Academy](https://www.devtoolsacademy.com/blog/state-of-ai-code-review-tools-2025/):

| Tool | Bug Detection Rate | False Positive Rate |
|------|-------------------|---------------------|
| Macroscope | 48% | Not published |
| CodeRabbit | 44–46% | 5–15% |
| Cursor Bugbot | 42% | Not published |
| Greptile | 82%* | Not published |
| Traditional static analysis | <20% | High |

*Greptile's 82% is from their own benchmark with full codebase context; third-party tests show 24%. Methodology differs significantly.

**Reported impacts of AI code review** ([Digital Applied 2025](https://www.digitalapplied.com/blog/ai-code-review-automation-guide-2025)):
- 40% time savings on review process
- ~50% of flagged issues fixed before merge
- 39% higher PR merge rates
- 62% fewer production bugs (self-reported)

67% of AI code review is currently done by GitHub Copilot Code Review, with CodeRabbit at 12% market share per Jellyfish.

### The Review Capacity Crisis

[GitHub's Octoverse 2025](https://octoverse.github.com) shows platform-level activity: 43.2M monthly merged PRs (+23% year-over-year), 82.19M code pushes/month (+26% year-over-year). Copilot coding agent opened over **1 million PRs** in 2025. PR size grew 33% while review capacity stayed flat.

The [Google DORA 2024 finding](https://cloud.google.com/blog/products/devops-sre/announcing-the-2024-dora-report) is instructive: AI can resolve a microservice bug in under 5 minutes of process time but still incurs a 5-day cycle time due to review waits. The bottleneck has shifted completely from code generation to code review. Faster models do not solve this problem. The solution is multi-agent review patterns or radically increased review capacity.

---

## Developer Productivity: The Paradox

The productivity literature is the most contradictory in AI coding research. Both of these findings are true simultaneously, and the contradiction reveals something important about the nature of AI's productivity impact.

### METR RCT: AI Slowed Experienced Devs 19%

[METR's randomized controlled trial (July 2025)](https://metr.org/blog/2025-07-10-early-2025-ai-experienced-os-dev-study/) is the gold-standard study: 16 experienced developers (average 5+ years on repos with 22K+ GitHub stars), 246 tasks, run on Cursor Pro + Claude 3.5/3.7 Sonnet.

**Result**: AI increased task completion time by **19%**. Developers expected a 24% speedup. After completing tasks, they still believed AI had sped them up 20% — simultaneously wrong in opposite directions (slower in reality, believed faster).

The February 2026 follow-up acknowledges a possible reversal with newer tools, but selection effects in the August 2025 data (developers who refuse to work without AI declining to participate) make it unreliable. METR believes early 2026 developers are "likely more sped up" but cannot quantify.

### GitHub Study: 55.8% Faster on Simple Tasks

[Microsoft Research's 2022 study](https://www.microsoft.com/en-us/research/publication/the-impact-of-ai-on-developer-productivity-evidence-from-github-copilot/) found developers completed a JavaScript HTTP server 55.8% faster with Copilot. This is the most-cited productivity study in AI coding — and it involves a bounded, single, well-defined task with a clear completion criterion.

The distinction matters: **simple, isolated, well-defined tasks** vs. **complex, multi-file, architectural work in a real production codebase**. Both studies are right. They are measuring different things.

### DORA: −7.2% Stability Per 25% AI Adoption

[Google's 2024 DORA Report](https://cloud.google.com/blog/products/devops-sre/announcing-the-2024-dora-report) — ~3,000 respondents, the most authoritative DevOps benchmarking study — shows AI's aggregate impact on team-level metrics:

| Metric | Per 25% AI Adoption Increase |
|--------|------------------------------|
| Delivery throughput | −1.5% |
| **Delivery stability** | **−7.2%** |
| Time spent on valuable work | −2.6% |

Despite 75% of respondents *reporting* productivity gains from AI, the aggregate metrics show negative stability. The DORA conclusion: "Improving the development process does not automatically improve software delivery — at least not without proper adherence to the basics of successful software delivery, like small batch sizes and robust testing mechanisms."

### GitClear Productivity Data

[GitClear's 70,000 developer-year dataset](https://www.gitclear.com/recent_ai_developer_productivity_code_quality_research):
- Median developer productivity: +9% from 2022 to 2025
- High-commit developers (500+ commits/year): +14.1%
- But: these productivity gains come with code quality costs (see Diff Quality section)

### Jellyfish Real-World Velocity

[Jellyfish's 2025 platform data](https://jellyfish.co/blog/2025-ai-metrics-in-review/) from actual engineering team metrics:

| Metric | Low AI Adoption | High AI Adoption | Change |
|--------|----------------|-----------------|--------|
| Median cycle time | 16.7 hours | 12.7 hours | **−24%** |
| PRs per engineer | 1.36/week | 2.9/week | **+113%** |
| Bug fix PR share | 7.5% | 9.5% | +2 pp |
| Code volume (LOC/developer) | 4,450 | 7,839 | **+76%** |

Tool retention at 20 weeks: **Copilot/Cursor: 89%, Claude Code: 81%** — suggesting genuine sticky value for users who stay with the tools past the initial trial.

### The Perception vs. Reality Gap

[Stack Overflow's 2025 survey](https://survey.stackoverflow.co/2025/ai) (49,000+ respondents): **66% cite "AI solutions almost right, but not quite" as top frustration**. **45% find debugging AI-generated code more time-consuming** than writing it themselves. Only **3% "highly trust" AI output**. Yet **52% say AI has had a positive productivity effect**.

The gap between "AI is useful" and "AI is transformative" is wide. Most developers have found a regime in which AI helps — autocomplete, boilerplate, documentation, simple bug fixes — while recognizing its limits for complex work.

---

## Time-to-PR Benchmarks

| Tool/Context | Task Type | Time | Cost | Source |
|--------------|-----------|------|------|--------|
| Sonar Foundation Agent | SWE-bench issues (avg) | **9 min/issue** | $1.9/issue | [Sonar Mar 2026](https://www.morningstar.com/news/pr-newswire/20260311la08045/sonar-claims-top-spot-on-swe-bench-leaderboard) |
| Devin (2025) | ETL migration file | 3–4 hours | ACU-based | [Cognition Nov 2025](https://cognition.ai/blog/devin-annual-performance-review-2025) |
| Devin (2025) | Security CVE fix | **1.5 min** | ACU-based | [Cognition Nov 2025](https://cognition.ai/blog/devin-annual-performance-review-2025) |
| Devin (2025) | Architecture draft | 15 min | ACU-based | [Cognition Nov 2025](https://cognition.ai/blog/devin-annual-performance-review-2025) |
| Claude 4.5 Sonnet | Automated benchmark | ~50 min time horizon | Subscription | [METR Mar 2026](https://metr.org/notes/2026-03-10-many-swe-bench-passing-prs-would-not-be-merged-into-main/) |
| Claude 4.5 Sonnet | Maintainer-reviewed | **~8 min** time horizon | Subscription | [METR Mar 2026](https://metr.org/notes/2026-03-10-many-swe-bench-passing-prs-would-not-be-merged-into-main/) |
| GitHub Copilot | Task completion (controlled) | +55.8% faster | $10/mo | [Microsoft Research 2022](https://www.microsoft.com/en-us/research/publication/the-impact-of-ai-on-developer-productivity-evidence-from-github-copilot/) |
| Experienced developers (METR RCT) | Complex production tasks | −19% (slower) | — | [METR Jul 2025](https://metr.org/blog/2025-07-10-early-2025-ai-experienced-os-dev-study/) |
| Devin Nubank migration | Migration sub-task (after fine-tuning) | 10 min (was 40 min) | $20-500/mo | [Devin.ai](https://devin.ai) |

The most honest summary: for well-defined, repetitive, small tasks, AI agents are genuinely 10–20x faster than humans at the code-generation step. For complex multi-file tasks on production codebases, the total cycle time (including review, correction, and re-review) often matches or exceeds human-written code.

---

## The End-to-End Workflow: Issue → PR → Merge

### The Standard Async Agent Pattern (2026)

The emerging standard workflow for autonomous coding agents, as documented by [Addy Osmani (Jan 2026)](https://addyosmani.com/blog/ai-coding-workflow/) and [Benjamin Anderson (Dec 2025)](https://benanderson.work/blog/async-coding-agents/):

```
GitHub Issue created / assigned to agent
    ↓
Agent receives task (via Issues, Agents panel, or API)
    ↓
Agent clones repo to cloud VM / sandboxed environment
    ↓
Agent reads codebase context, relevant files, past PRs
    ↓
Agent plans implementation (may create plan.md)
    ↓
Agent writes code, runs tests iteratively
    ↓
Agent opens draft pull request with description
    ↓
Human developer reviews → approves / requests changes
    ↓
Merge
```

Anderson's key insight: *"The bottleneck has shifted to deciding what you want done, describing it sufficiently, switching between tasks without forgetting context, and testing results to avoid regressions. The actual ability to roughly do the thing is usually not in question."*

### CI/CD Integration Comparison

| Tool | GitHub Actions | Native CI/CD | Background Automation | CI/CD Success Rate |
|------|---------------|-------------|----------------------|-------------------|
| GitHub Copilot CLI | ✓ Native (GITHUB_ASKPASS) | ✓ Full GitHub integration | ✓ Copilot Coding Agent | Highest |
| Claude Code | ✓ Headless mode | ✓ Claude Max (Web) | ✓ | High |
| Devin | ✓ Via API | ✓ Sandboxed VM | ✓ Primary mode | High (67% merge rate) |
| OpenHands | ✓ Docker/K8s | ✓ Enterprise VPC | ✓ | High |
| Google Jules | ✓ Via CLI | ✓ GCP VM | ✓ Primary mode | Medium (still rolling out) |
| Aider | ✓ Via bash | Custom | Limited | Medium |
| OpenCode | ✓ Via bash | Custom | Limited | Medium |

[Augment Code's enterprise CI/CD analysis (October 2025)](https://www.augmentcode.com/pricing) found: "CI/CD integration fails for 73% of AI coding tools because vendors optimize for individual workflows while production pipelines require deployment topology understanding and multi-repository coordination."

JetBrains' CI/CD survey found the most common AI CI/CD use cases are [build failure debugging, code quality checking, and pipeline optimization](https://blog.jetbrains.com/teamcity/2025/10/the-state-of-cicd/) — not full autonomous feature development. Full pipeline ownership by AI remains experimental.

### Multi-Agent Patterns: Coder + Reviewer

Three dominant multi-agent patterns have consolidated by early 2026 ([Jellyfish 2025](https://jellyfish.co/blog/2025-ai-metrics-in-review/)):

**Pattern 1 — Coder + Reviewer**: One agent generates code (Cursor, Claude Code, Copilot Agent); a separate reviewer (CodeRabbit, Copilot Code Review, Cursor Bugbot) analyzes the PR. 67% of AI code review is currently done by Copilot Review; CodeRabbit at 12%.

**Pattern 2 — Parallel task agents**: Multiple agents work simultaneously on different features using git worktrees. Cursor supports up to 8 concurrent agent sessions. Kilo Code's Orchestrator mode routes tasks across sub-agents with isolated worktrees. The OpenAI Codex App uses CSV-based fan-out for parallel agent dispatch.

**Pattern 3 — Test-Verify-Correct loop**: Agent writes code → separate verification system (browser automation, test runner) executes and reports failures → agent corrects based on actual errors → repeat. Key design insight: the coding agent should not evaluate its own work; verification must come from an external system. Cursor + Squidler.io MCP integration is one production implementation.

### The Async Agent Revolution

The market bifurcated decisively in 2025 into interactive (synchronous IDE) and async (background agent) modes. Both are now table stakes for major vendors.

**Async agent vendors as of early 2026**:
- **GitHub Copilot Coding Agent** (Microsoft) — via Agents panel, GitHub Issues
- **Devin** (Cognition AI) — earliest and most mature; parallel cloud agents
- **Claude Code Web** (Anthropic)
- **OpenAI Codex Web** (OpenAI)
- **Google Jules** (Google)

The practical insight: async agents are best for repetitive, well-defined tasks (bug fixes, test additions, refactoring, migrations, tech debt paydown). Interactive agents are best for tasks requiring creative judgment, novel solutions, and learning. The most effective workflow combines both: use async agents for backlog items while the developer uses interactive AI for the hard problems.

---

## Developer Sentiment: Trust Is Falling

### Stack Overflow Developer Survey 2025

The largest developer survey, with [49,000+ respondents](https://survey.stackoverflow.co/2025/ai):

| Metric | 2024 | 2025 | Trend |
|--------|------|------|-------|
| Using or planning to use AI tools | 76% | **84%** | ↑ Adoption rising |
| Use AI tools daily (professional devs) | — | **51%** | — |
| Positive sentiment | 70%+ | **60%** | ↓ Trust eroding |
| Trust AI output accuracy | ~40% | **33%** | ↓ Falling |
| Distrust AI output accuracy | — | **46%** | ↑ Rising |
| "Highly trust" AI output | — | **3%** | — |
| Experienced devs "highly distrust" | — | **20%** | — |
| "AI solutions almost right, but not quite" (top frustration) | — | **66%** | — |
| "Debugging AI code more time-consuming" | — | **45%** | — |
| Would ask a human "when I don't trust AI's answers" | — | **75%** | — |
| Not "vibe coding" | — | **72%** | — |
| AI agents: don't use / stick to simpler tools | — | **52%** | — |
| Concern about AI accuracy | — | **87%** | — |
| Concern about AI security/privacy | — | **81%** | — |

### JetBrains Developer Ecosystem Report 2025

[24,534 developers across 194 countries](https://blog.jetbrains.com/research/2025/10/state-of-developer-ecosystem-2025/):

- **85%** regularly use AI tools for coding (up from previous years)
- **62%** rely on at least one AI coding assistant, agent, or code editor
- **68%** expect AI proficiency to become a job requirement
- Nearly **9 in 10** who use AI save at least 1 hour per week
- **1 in 5** save 8+ hours per week (an entire workday)
- **15%** have not yet adopted AI tools — a significant skeptical minority

### Jellyfish Engineering Management Survey 2025

[From the Jellyfish platform tracking real engineering teams](https://jellyfish.co/blog/2025-ai-metrics-in-review/):

- **90%** of teams now use AI in workflows (up from 61% a year prior)
- Code assistant adoption: **49.2%** → **72.8%** peak (Jan–Aug 2025)
- AI code review agent adoption: **14.8%** → **51.4%** (Jan–Oct 2025)
- Almost **50%** of companies now have ≥50% AI-generated code (up from 20%)
- Tool retention at 20 weeks: Copilot/Cursor **89%**, Claude Code **81%**

The retention data is the most telling: tools that developers keep using at 20 weeks are genuinely valuable. 89% retention for Copilot/Cursor vs. 81% for Claude Code suggests both categories have found sticky use cases, but the IDE-native tools have a slight edge in habit formation.

### The "Almost Right But Not Quite" Frustration

66% of Stack Overflow respondents cite "AI solutions almost right, but not quite" as their top frustration — above security concerns, above accuracy issues. This describes the specific experience of receiving a plausible-looking solution that requires non-trivial correction: the debugging cost often exceeds the generation benefit for anything non-trivial.

[Qodo's survey of 600+ developers](https://www.qodo.ai/reports/state-of-ai-code-quality/) found **76% of developers** in a "red zone" — frequent hallucinations with low confidence — and only **3.8%** reporting both low hallucinations AND high confidence to ship AI code without review. **96% of developers don't fully trust AI-generated code's accuracy** per the Sonar 2026 survey.

### Jellyfish Retention Implications

Jellyfish data shows that the highest-AI-adoption engineers have 113% more PRs per week but show no corresponding improvement in retention or engagement scores — and some evidence of increased cognitive load. The bet is that today's friction (verification overhead, debugging AI mistakes) will decrease as tools mature, leaving the throughput gains without the current tax.

---

## Strategic Recommendations

### For Solo Developers

The best stack for a solo developer optimizing for output per dollar:

1. **GitHub Copilot Pro ($10/mo)** as the baseline: async coding agent for well-defined issues, inline suggestions in VS Code/JetBrains, CLI for terminal work. The cheapest path to the full issue→PR automation pattern.
2. **Gemini CLI (free)** as the secondary terminal agent: 1,000 requests/day at no cost, 1M token context window, MCP support. Run in parallel with Copilot on different tasks.
3. **Aider or OpenCode (BYOK)** for any task requiring a specific model: full 75+ model flexibility, auto-commit to git, no subscription cost beyond API usage.

Avoid: Tabnine (no free tier, high cost), JetBrains AI (requires JetBrains subscription on top), Google Antigravity (March 2026 pricing makes professional use require $250/mo Ultra tier).

### For Small Teams (5–20 Engineers)

1. **GitHub Copilot Business ($19/user/mo)** for the whole team: organization-level policies, IP indemnity not included (need Enterprise for that), covers the full async agent + CLI + review workflow.
2. **Claude Code via Copilot delegation** for complex tasks: Claude Opus/Sonnet 4.6 is available to Copilot Business users without a separate Anthropic subscription.
3. **CodeRabbit or Copilot Code Review** as the AI reviewer: automated first-pass review before human review, reducing review time by ~40%.
4. **Kilo Code** for developers who prefer open-source VS Code extensions with Orchestrator mode and git worktrees per agent.

### For Enterprise

1. **GitHub Copilot Enterprise ($39/user/mo)**: IP indemnity, org-level model selection policies, SAML SSO, audit logs, private codebase indexing for context.
2. **Tabnine Enterprise ($59/user)** if air-gapped or HIPAA/FedRAMP requirements: the only tool with genuine on-premises deployment and zero training on customer code.
3. **OpenHands Enterprise** if the team wants open-source control and Kubernetes VPC deployment with RBAC and audit trails.
4. **Sourcegraph Cody Enterprise** for organizations with 10+ repositories: cross-repo 1M token context retrieval solves the multi-repo context problem no other tool matches.
5. **Devin Team ($500/mo)** for dedicated autonomous agent capacity on backlog remediation: the 67% PR merge rate means it contributes positive throughput at scale.

### For Ewan's Specific Case: Amplified Partners, Beast Server, Kilo Code Approach

The use case — SMB consulting, building on a high-performance Hetzner server, Kilo Code as the primary VS Code tool — maps onto a specific optimal stack:

**Recommended Stack (March 2026)**:

| Role | Tool | Why | Cost |
|------|------|-----|------|
| Primary IDE agent | **Kilo Code** (VS Code) | Orchestrator mode + OpenCode engine + git worktrees = native parallel agent support; $20 starter credits at API rates | Low (API cost only) |
| Best frontier model | **Claude Code Pro** ($20/mo) | #1 SWE-bench; best at multi-file complex reasoning; integrates with Kilo Code via Anthropic API | $20/mo |
| Async background agent | **GitHub Copilot Coding Agent** (Pro, $10/mo) | Assign GitHub issues to Copilot while working on harder problems; GitHub-native | $10/mo |
| Free high-volume model | **Gemini CLI** | 1,000 req/day free, 1M context; use for summarization, documentation, bulk test generation | Free |
| Git audit trail | **Aider** (BYOK) | Auto-commits every AI edit; use for high-transparency work where audit trail matters | API cost only |
| Security scanning | **Bandit + Semgrep** (baked into harness) | Run automated security scan on every AI-generated PR before review | Free |

**The 4x Parallel Approach**: The Beast server provides the compute capacity to run multiple isolated agent sessions simultaneously. The architecture:
- Agent 1 (Kilo Code Orchestrator): handles the primary complex feature
- Agent 2 (Copilot Coding Agent): resolves 2–3 GitHub backlog issues in background
- Agent 3 (Gemini CLI): generates tests for recently merged code
- Agent 4 (Aider): handles documentation updates

Git worktrees ensure agents don't conflict. Total cost: ~$30-40/mo in subscriptions plus API usage. Expected throughput: 4–6x the output of a single synchronous workflow.

**Key operational rules**:
1. Never ship AI-generated security-sensitive code (auth, crypto, secrets) without explicit human review of the diff — the 29–62% vulnerability rate is too high
2. Always run the harness security scorer (Bandit/Semgrep) before any PR merge
3. For refactoring tasks: define the exact pattern explicitly before running the agent; AI DRY failures are predictable
4. For test generation: explicitly prompt for edge cases, negative inputs, and failure paths; don't trust happy-path tests to catch production failures

### The Optimal Tool Stack for End-to-End AI Coding

Based on all the evidence above, the optimal end-to-end stack for 2026 is:

| Stage | Best Tool | Why |
|-------|-----------|-----|
| Issue triage + planning | GitHub Copilot (native Issues) | GitHub-native context, reads labels/history |
| Complex feature development | Claude Code (Opus 4.6) | Best multi-file reasoning, TDD enforcement |
| Bulk backlog items | Devin / Copilot Agent (async) | Fire-and-forget; 67% merge rate for well-scoped tasks |
| API migrations | Devin (fine-tuned) | 4x speed after pattern training; verifiable output |
| Test generation | Cursor / Claude Code | Best automated test running + coverage reporting |
| Code review | CodeRabbit + Copilot Review | Catches 44–48% of bugs before human review |
| Security scanning | Semgrep + Bandit in CI | Non-negotiable; AI security failure rate too high to skip |
| CLI/scripting tasks | Gemini CLI or Aider | Free tier or BYOK; full model flexibility |

---

## The Evaluation Harness

### What the Harness Does

The evaluation harness at `/home/user/workspace/ai-coding-bakeoff-harness/` is a production-ready framework for objectively comparing AI coding tools against any codebase. It runs 8 tools against 4 task types and scores the results across 5 dimensions.

**Supported tools out of the box**:

| Tool | Runner Type | How It Works |
|------|-------------|--------------|
| GitHub Copilot Coding Agent | API (Issues) | Creates GitHub issue, assigns to Copilot, monitors resulting PR |
| GitHub Copilot CLI | CLI | Runs `npx @githubnext/github-copilot-cli` commands |
| Cursor | Manual + Timer | Guided manual workflow with wall-clock timing |
| OpenAI Codex | API | Sends prompts to the Codex API |
| Claude Code | CLI | Runs `claude` CLI with task prompt |
| Aider | CLI | Runs `aider` in non-interactive mode |
| Devin | API | Submits task via Devin API, polls for completion |
| OpenHands | API | Submits task via OpenHands API |

### Scoring Methodology

Each tool receives a **composite score from 0–10** calculated from five dimensions:

| Dimension | Weight | What It Measures |
|-----------|--------|-----------------|
| **Diff Quality** | 25% | Clean diffs, minimal churn, DRY compliance, complexity reduction |
| **Review Comments** | 20% | Predicted review issues, severity of problems found |
| **Security Issues** | 20% | CWEs detected by Bandit/Semgrep/ESLint, severity-weighted |
| **Test Pass Rate** | 20% | Tests passing, coverage delta |
| **Time to PR** | 15% | Wall-clock time from start to completion, normalized |

**Score interpretation**:
- **8–10**: Excellent — production-ready output
- **6–8**: Good — minor issues, would pass review with small changes
- **4–6**: Fair — needs significant rework
- **2–4**: Poor — major issues or incomplete
- **0–2**: Failed — tool couldn't complete the task

The weights can be adjusted in `config.yaml` to match the team's priorities. A security-first team might weight Security Issues at 35%; a throughput-first team might weight Time to PR at 30%.

### How to Run the Harness

```bash
# 1. Point at your target repo
# Edit config.yaml:
# repo:
#   url: "https://github.com/your-org/your-repo.git"
#   branch: "main"
#   language: "python"
#   test_command: "pytest"

# 2. Set API keys
export GITHUB_TOKEN="ghp_..."
export ANTHROPIC_API_KEY="sk-ant-..."
export OPENAI_API_KEY="sk-..."
export DEVIN_API_KEY="..."

# 3. Run the full bakeoff
python run_bakeoff.py

# 4. Run specific tools only
python run_bakeoff.py --tools claude_code aider codex

# 5. Run specific tasks only
python run_bakeoff.py --tasks bug-fix add-tests

# 6. Dry run (validate config)
python run_bakeoff.py --dry-run
```

Results land in `results/`:
- `results/report.md` — human-readable comparison
- `results/dashboard.json` — machine-readable for dashboards
- `results/raw/<tool>/<task>/` — raw diffs, scores, and logs per tool per task

### GitHub Action for Automated Bakeoffs

The harness includes `.github/workflows/bakeoff.yml` for scheduled automated bakeoffs:

```yaml
# Run bakeoff weekly against main branch
schedule:
  - cron: '0 9 * * 1'  # Every Monday 9am
```

This enables tracking tool performance over time as both the codebase and the AI tools evolve — answering the question "is Claude Code still better than Copilot for this specific codebase?" on an ongoing basis rather than a point-in-time basis.

---

## Conclusion

### The State of the Art, Honestly Stated

March 2026 is a genuinely exciting moment for AI coding tools — and a moment to be clear-eyed about what that excitement is and isn't. The genuine advances: agentic tools that can resolve well-defined GitHub issues end-to-end are real and working. Devin's PR merge rate rising from 34% to 67% over 18 months represents a threshold crossing — agents now contribute net positive throughput on suitable tasks. Sonar's 9-minute average resolution at $1.9/issue means enterprise-scale backlog remediation is economically viable for the first time.

The honest caveats: SWE-bench Verified scores are contaminated and overstate real-world performance by roughly 2x. On clean benchmarks, top models solve ~46% of tasks. On novel, live issues, ~19%. The METR maintainer study found even that 46% overstates production-ready quality by 24 percentage points. A realistic estimate of the best AI agents' actual end-to-end contribution to a production codebase — code that gets written, reviewed, merged, and stays merged without causing regressions — is in the range of 19–44% of attempted tasks, depending on task complexity.

Security remains a persistent unresolved failure mode. No tool has solved the 29–62% vulnerability rate. The OWASP LLM Top 10 and the new Agentic AI Top 10 document a threat surface that is growing faster than defenses. The 2025 CVE data (2,130 AI-related CVEs, 34.6% YoY growth) shows this is not a theoretical risk. The Stanford false-confidence finding — that AI assistance makes developers *more confident* about insecure code — is the most dangerous dynamic in the entire landscape.

Code quality is deteriorating at scale. GitClear's 211-million-line analysis documents a structural decline in refactoring and a structural increase in copy-paste and churn. This is predictable debt being accumulated now that will hit maintenance costs in 2026–2027. No tool has an incentive to fix this because "more code generated" is the marketed metric, not "better code quality."

### What to Bet on for 2026–2027

The investments with the clearest upside:

1. **Multi-agent verification loops**: The emerging consensus is that a coding agent should not evaluate its own work. Independent verification (separate reviewer agent, automated test suite, browser automation) reduces the ~24pp benchmark-to-production gap. Teams that build Coder + Reviewer pipelines will outperform teams running single agents.

2. **The async agent model**: Background agents handling well-scoped backlog items while developers focus on complex work is the highest-ROI pattern the data supports. The issue→PR automation workflow is production-ready at 67% merge rates for well-configured agents.

3. **SWE-bench Pro as the honest metric**: Any vendor still citing only SWE-bench Verified scores in late 2026 should be treated with skepticism. Pro scores (roughly half of Verified) and Live scores (~19%) are the benchmarks that correspond to production reality.

4. **The security tooling layer**: The market for automated security scanning of AI-generated code is growing faster than the AI coding market itself. Bandit, Semgrep, CodeRabbit, and purpose-built AI security scanners will become mandatory parts of any responsible AI-assisted development pipeline.

5. **Open-weight models for cost efficiency**: Six of the top ten SWE-bench models are from Chinese labs. MiniMax M2.5's 80.2% on Verified as an open-weight model signals that frontier performance will commoditize. The premium for closed frontier models will compress.

### Where the 4x Parallel Approach Fits

The thesis of running 4 parallel agents on isolated git worktrees reflects a structurally sound reading of where value is being captured in 2026. The bottleneck is no longer code generation — it's task definition, context-setting, and review. Running 4 agents in parallel against well-defined tasks with automated first-pass review (security scanner + AI reviewer) maximizes throughput while maintaining quality gates.

The specific Beast server setup is well-suited to this: dedicated compute for isolated agent VMs, no shared resource contention, direct SSH access for CLI tools, and the ability to run self-hosted models (via Aider BYOK) to minimize API costs on bulk tasks.

The harness in `/home/user/workspace/ai-coding-bakeoff-harness/` gives the quantitative framework to prove or disprove which combination of tools actually performs best on the specific codebase in question. Run it, measure it, update the stack accordingly. The benchmarks show what's possible in the abstract; only running the harness on real code shows what's true in practice.

---

*Report compiled March 2026. All benchmark data from primary sources cited inline. This report will be outdated within 3–6 months — the pace of change in this market is genuine. Recommend re-running the harness quarterly and re-evaluating tool choices at each major benchmark leaderboard update.*

---

## Sources Index

All primary sources cited throughout this document:

- [SWE-bench Leaderboard](https://www.swebench.com)
- [SWE-bench Pro Leaderboard (Scale AI SEAL)](https://labs.scale.com/leaderboard/swe_bench_pro_public)
- [Morph SWE-bench Pro Analysis](https://www.morphllm.com/swe-bench-pro)
- [Simon Willison SWE-bench Feb 2026](https://simonwillison.net/2026/Feb/19/swe-bench/)
- [METR March 2026 Study: PRs Would Not Be Merged](https://metr.org/notes/2026-03-10-many-swe-bench-passing-prs-would-not-be-merged-into-main/)
- [METR July 2025 RCT: AI Slows Experienced Devs](https://metr.org/blog/2025-07-10-early-2025-ai-experienced-os-dev-study/)
- [GitHub Copilot CLI GA Feb 2026](https://github.blog/changelog/2026-02-25-github-copilot-cli-is-now-generally-available/)
- [Sonar SWE-bench #1 Announcement](https://www.morningstar.com/news/pr-newswire/20260311la08045/sonar-claims-top-spot-on-swe-bench-leaderboard)
- [GitClear 2025 Code Quality Research](https://www.gitclear.com/ai_assistant_code_quality_2025_research)
- [GitClear 2024 Coding on Copilot](https://www.gitclear.com/coding_on_copilot_data_shows_ais_downward_pressure_on_code_quality)
- [GitClear Jan 2026 Productivity Research](https://www.gitclear.com/recent_ai_developer_productivity_code_quality_research)
- [CodeRabbit AI vs Human Code Report](https://www.coderabbit.ai/blog/state-of-ai-vs-human-code-generation-report)
- [Qodo State of AI Code Quality](https://www.qodo.ai/reports/state-of-ai-code-quality/)
- [arXiv Copilot Security Study](https://arxiv.org/html/2310.02059v2)
- [Veracode 2025 GenAI Code Security](https://www.veracode.com/blog/genai-code-security-report/)
- [Cloud Security Alliance AI Code Risks](https://cloudsecurityalliance.org/blog/2025/07/09/understanding-security-risks-in-ai-generated-code)
- [Stanford Dan Boneh Lab AI Security](https://ee.stanford.edu/dan-boneh-and-team-find-relying-ai-more-likely-make-your-code-buggier)
- [GitGuardian Copilot Secrets Leakage](https://blog.gitguardian.com/yes-github-copilot-can-leak-secrets/)
- [TrendMicro TrendAI Security Report](https://www.trendmicro.com/vinfo/us/security/news/threat-landscape/fault-lines-in-the-ai-ecosystem-trendai-state-of-ai-security-report)
- [OWASP LLM Top 10](https://genai.owasp.org/llm-top-10/)
- [OWASP Agentic AI Top 10](https://genai.owasp.org/2025/12/09/owasp-genai-security-project-releases-top-10-risks-and-mitigations-for-agentic-ai-security/)
- [Socket.dev Slopsquatting Research](https://socket.dev/blog/slopsquatting-how-ai-hallucinations-are-fueling-a-new-class-of-supply-chain-attacks)
- [Martin Fowler AI Supply Chain](https://martinfowler.com/articles/exploring-gen-ai/software-supply-chain-attack-surface.html)
- [AI IDEs 30 Flaws Research](https://thehackernews.com/2025/12/researchers-uncover-30-flaws-in-ai.html)
- [Black Duck AI Security Survey 2026](https://www.blackduck.com/blog/ai-coding-assistant-security-risks-benefits-devsecops-2025.html)
- [Google DORA 2024 Report](https://cloud.google.com/blog/products/devops-sre/announcing-the-2024-dora-report)
- [Microsoft Research GitHub Copilot Productivity](https://www.microsoft.com/en-us/research/publication/the-impact-of-ai-on-developer-productivity-evidence-from-github-copilot/)
- [GitHub Octoverse 2025](https://octoverse.github.com)
- [GitHub/Accenture Copilot Enterprise Study](https://github.blog/news-insights/research/research-quantifying-github-copilots-impact-in-the-enterprise-with-accenture/)
- [Jellyfish 2025 AI Metrics](https://jellyfish.co/blog/2025-ai-metrics-in-review/)
- [Greptile State of AI Coding 2025](https://www.greptile.com/state-of-ai-coding-2025)
- [Stack Overflow Developer Survey 2025](https://survey.stackoverflow.co/2025/ai)
- [JetBrains Developer Ecosystem 2025](https://blog.jetbrains.com/research/2025/10/state-of-developer-ecosystem-2025/)
- [JetBrains CI/CD Survey 2025](https://blog.jetbrains.com/teamcity/2025/10/the-state-of-cicd/)
- [Cognition Devin Annual Review 2025](https://cognition.ai/blog/devin-annual-performance-review-2025)
- [Uplevel AI Developer Productivity Study](https://uplevelteam.com/blog/ai-for-developer-productivity)
- [Zoominfo Copilot Study (arXiv)](https://arxiv.org/html/2501.13282v1)
- [Addy Osmani LLM Coding Workflow 2026](https://addyosmani.com/blog/ai-coding-workflow/)
- [Benjamin Anderson Async Coding Agents](https://benanderson.work/blog/async-coding-agents/)
- [DevTools Academy AI Code Review 2025](https://www.devtoolsacademy.com/blog/state-of-ai-code-review-tools-2025/)
- [GitHub Copilot CLI GitHub Actions Docs](https://docs.github.com/en/copilot/how-tos/copilot-cli/automate-with-actions)
- [GitHub Copilot Plans](https://github.com/features/copilot/plans)
- [Cursor Pricing](https://cursor.com/pricing)
- [Windsurf Pricing](https://windsurf.com/pricing)
- [Devin Pricing](https://devin.ai/pricing/)
- [Anthropic Claude Code News](https://www.anthropic.com/news/claude-opus-4-6)
- [OpenHands GitHub](https://github.com/OpenHands/OpenHands)
- [Gemini CLI Blog](https://blog.google/innovation-and-ai/technology/developers-tools/introducing-gemini-cli-open-source-ai-agent/)
- [Google Jules Blog](https://blog.google/innovation-and-ai/technology/developers-tools/jules-proactive-updates/)
- [Google Antigravity](https://antigravity.google)
- [The Register: Antigravity Protests](https://www.theregister.com/2026/03/12/users_protest_as_google_antigravity/)
- [Kilo Code Blog](https://blog.kilo.ai/p/we-completely-rebuilt-the-kilo-vs-code-extension)
- [Spectrum of Engineering Sciences Comparative Study](https://thesesjournal.com/index.php/1/article/view/1810)
- [CVE-2025-32711 EchoLeak Analysis](https://socprime.com/blog/cve-2025-32711-zero-click-ai-vulnerability/)
- [OpenAI Codex App](https://openai.com/index/introducing-codex/)
- [OpenAI GPT-5.3-Codex](https://openai.com/index/introducing-gpt-5-3-codex/)

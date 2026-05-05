---
title: "Amplified Partners — The Agent Architecture"
id: "amplified-agents-master-copy"
version: 1
created: "2026-04-25"
type: "document"
topic_type: "unsorted"
audience: "internal"
layer: "shadow"
status: "filed"
signed_by: "Devon, 2026-04-25, devin-992682c244cf444f91e0a516498afbfd"
---

# Amplified Partners — The Agent Architecture

## A Complete Reference for Building, Governing, and Deploying AI Agents in Business

**Internal Document — v1.0 | March 2026**
**Author: Ewan Bramley, Founder — Amplified Partners**

---

This is the single reference document for how Amplified Partners builds, governs, measures, and deploys AI agents into real businesses. It was assembled from weeks of architecture work across dozens of sessions. No marketing. No fluff. Just how it works and why.

---

## Part 1: The Reality Check — Why This Architecture Exists

Before building any of this, we read the numbers. Every design decision in this architecture traces back to a specific, documented failure pattern. Here is what the data says.

### The Headline Failure Rate

**88% of AI agent projects fail before reaching production.** Fewer than 1 in 8 agent initiatives successfully reach production operation ([Digital Applied, March 2026](https://www.digitalapplied.com/blog/88-percent-ai-agents-never-reach-production-failure-framework)). This is not a fringe estimate — Gartner's 2025 AI deployment survey puts it at 85%, and McKinsey's 2025 State of AI report found fewer than 20% of AI pilots scale to production within 18 months.

### The 7 Failure Patterns

7 identifiable failure patterns account for 94% of all project stalls ([Digital Applied](https://www.digitalapplied.com/blog/88-percent-ai-agents-never-reach-production-failure-framework)):

| Pattern | Failure Mode | % of Failures |
|---------|-------------|---------------|
| 1 | Scope Creep | 34% |
| 2 | Data Quality Failures | 27% |
| 3 | Security Blockers | 14% |
| 4 | Integration Complexity | 9% |
| 5 | Cost Overruns | 7% |
| 6 | Governance Gaps | 5% |
| 7 | Organisational Resistance | 4% |

Scope creep and data quality combined cause 61% of all failures. The average cost of a failed AI agent project is **$340,000** in direct expenses, with total costs (including opportunity cost and morale damage) exceeding $650,000 ([Digital Applied](https://www.digitalapplied.com/blog/88-percent-ai-agents-never-reach-production-failure-framework)).

### The Compounding Error Problem

This is the one that kills you silently. If each step in an agent workflow has 95% reliability, over 20 steps you get only **35.85% overall success**. Even at 99% per step, 20 steps still only yields **82% success** — one in five attempts fails ([Prodigal Tech](https://www.prodigaltech.com/blog/why-most-ai-agents-fail-in-production)). Small error rates at each step multiply into large failure rates overall. More than half your operations fail before they complete.

### Multi-Agent Frameworks Are Worse Than You Think

A review of over 200 real-world tasks executed by multi-agent frameworks like MetaGPT and ChatDev found failure rates of **60-66%** — approximately two out of three tasks failed ([Reddit analysis of peer-reviewed studies](https://www.reddit.com/r/n8n/comments/1lhmsm3/what_nobody_tells_you_about_the_actual_failure/)). The root causes break down as:

- **42%** specification errors (infinite loops, hardcoded responses, failure to recognise task completion)
- **37%** inner agent misalignment (agents disregarding teammates or misinterpreting roles)
- **21%** verification failures (inadequate or absent final checks)

Clarifying roles and enhancing verification improved success rates by 15%, but the majority of tasks still failed ([Reddit](https://www.reddit.com/r/n8n/comments/1lhmsm3/what_nobody_tells_you_about_the_actual_failure/)).

### Consistency Is the Real Benchmark

Agent performance drops from **60% (single run) to 25% (8-run consistency)** — the CLEAR framework evaluation of six leading agents on 300 enterprise tasks demonstrated that optimising for accuracy alone yields agents 4.4-10.8x more expensive than cost-aware alternatives with comparable performance ([arXiv: CLEAR framework](https://arxiv.org/abs/2511.14136)).

CRM agents: the best current solutions achieve goal completion rates **below 55%** when working with CRM systems ([Maxim AI](https://www.getmaxim.ai/articles/ensuring-ai-agent-reliability-in-production/)). A study assessing 16 leading agents across 2,000 tasks found **no agent achieved a safety success rate above 60%** — overconfidence, disregard for safety protocols, and inability to recover from errors were prevalent ([Reddit](https://www.reddit.com/r/n8n/comments/1lhmsm3/what_nobody_tells_you_about_the_actual_failure/)).

Even a 3-5% failure rate is unacceptable when you are touching finance, operations, or customer workflows.

### Reliability Lags Behind Capability

The Agent Reliability Science paper evaluated 14 models across two benchmarks and found that recent capability gains have only yielded **small improvements in reliability** — reliability lags behind capability ([arXiv 2602.16666](https://arxiv.org/abs/2602.16666)). Rising accuracy scores on standard benchmarks obscure critical operational flaws: whether agents behave consistently across runs, withstand perturbations, fail predictably, or have bounded error severity.

### The Institutional Response

NIST launched the **AI Agent Standards Initiative** in February 2026 to ensure the next generation of AI agents is adopted with confidence, functions securely, and interoperates across the digital ecosystem ([NIST](https://www.nist.gov/news-events/news/2026/02/announcing-ai-agent-standards-initiative-interoperable-and-secure)).

Anthropic's research on measuring agent autonomy found that effective oversight requires **new post-deployment monitoring infrastructure AND new human-AI interaction paradigms** that help both the human and the AI manage autonomy and risk together ([Anthropic](https://www.anthropic.com/research/measuring-agent-autonomy)).

### Red Teaming Works — The Data Proves It

AI-mature companies experience **60% fewer AI-related security incidents** ([Mindgard](https://mindgard.ai/blog/ai-red-teaming-statistics)). Red teaming reduced incidents by **67%** and saved **$2.4M** in breach costs. Automated red teaming achieves a **69.5% success rate** versus 47.6% for manual testing and identifies **37% more unique vulnerabilities** ([Mindgard](https://mindgard.ai/blog/ai-red-teaming-statistics)).

Organisations applying structured failure-mode assessment before development reduce their failure rate to **below 15%** ([Digital Applied](https://www.digitalapplied.com/blog/88-percent-ai-agents-never-reach-production-failure-framework)).

### Why We Built This

We read these numbers. We built the architecture to address every single one of them. Every design decision, every governance layer, every safety mechanism in this document traces back to a documented failure pattern. If you cannot point to the failure it prevents, it does not belong in the architecture.

The industry's default response is to throw bigger models at the problem. Our response is different: engineer around the failure modes with deterministic validation, bounded autonomy, structured governance, and relentless measurement. Not because we distrust AI — because we respect it enough to build the infrastructure it needs to succeed.

---

## Part 2: Core Philosophy — Partners, Not Tools

### The Ideas Meritocracy

This architecture is adapted from Ray Dalio's principles of radical transparency and the ideas meritocracy from *Principles*. The core insight: the best ideas should win, regardless of who they come from. Applied to AI agents, this means **believability-weighted governance** — agents have track records, not just opinions. An agent's weight in a decision is earned through demonstrated competence, measured and recorded, not assumed.

### The 8 Immutable Laws (Layer 0)

These are non-negotiable. They cannot be overridden by any agent, any process, or any client instruction:

| # | Law | Meaning |
|---|-----|---------|
| 1 | **Radical Honesty** | Never deceive. If the data is bad, say so. If we do not know, say so. |
| 2 | **Radical Transparency** | Everything is visible. Decisions, data, reasoning, failures. |
| 3 | **Radical Attribution** | Every output traces to its source. No unattributed claims. |
| 4 | **Win-Win Only** | If the client does not win, we do not win. No zero-sum plays. |
| 5 | **White Hat Only** | No manipulation. No dark patterns. No shortcuts that hurt anyone. |
| 6 | **Help Not Hurt** | Every action must help. If there is any doubt, stop and ask. |
| 7 | **Add Not Reduce** | We add capacity to a business. We never reduce it. |
| 8 | **Give Value Away** | Lead with value. The commercial model follows naturally. |

### The Operating Principles

**"Their business. Their smell. Their signature. We de-friction the journey. We don't drive the car."**

This is the foundational frame. We are not here to impose our methods on a business. We adapt to them. We reduce friction. The business owner remains the decision maker at all times.

**The No-Redundancy Rule:** AI never replaces staff — it frees them for higher-value work. No one loses their job because we showed up. If a business owner wants to reduce headcount, that is their decision, not our recommendation.

**Decision Sovereignty:** The flow is always:

```
Their Data → Our Rubric → Scored Options → DECISION MAKER CHOOSES
```

We surface options with scores. They choose. Every time.

**The 70% Capacity Rule:** Agents run at 70% capacity, reserving 30% to mitigate hallucinations, handle edge cases, and maintain quality. This is not inefficiency — it is the engineering margin that keeps outputs reliable.

### Philosophical Influences

The architecture draws from:

- **Ray Dalio** (*Principles*) — Ideas meritocracy, radical transparency, believability-weighted decision-making. The intellectual foundation for everything.
- **Michael Gerber** (*The E-Myth Revisited*) — Systemisation. The reason every process is documented, every agent has a playbook, every output has a template.
- **Seth Godin** (*Permission Marketing, Purple Cow*) — Earn attention through remarkable value, not noise. No spam, no manipulation, no dark patterns.
- **Zig Ziglar** (*See You at the Top*) — Value-first approach. Help enough people get what they want and you will get what you want.
- **Paddy Lund** (*Building the Happiness-Centred Business*) — The business exists to create happiness for the owner and their clients. If AI does not contribute to that, it is not welcome.
- **Eliyahu Goldratt** (*The Goal*) — Theory of Constraints. Every business has one bottleneck that constrains everything else. Find it, fix it, repeat.
- **E.F. Schumacher** (*Small is Beautiful*) — Appropriate scale. Not every problem needs a 14-agent pipeline. Some need one agent and one rubric. Right-size everything.
- **Kaplan and Norton** (*Balanced Scorecard*) — Multi-dimensional measurement. Financial metrics alone do not tell the story. Add customer satisfaction, internal processes, and learning/growth.
- **W. Edwards Deming** — PDCA cycle, continuous improvement, system thinking. The Therapy Suite is Deming applied to AI.
- **Fred Reichheld** (*The Ultimate Question*) — Net Promoter System. Would your clients recommend you? If the answer is not a clear yes, fix that before anything else.
- **Don Swanson** — Literature-Based Discovery. The intellectual ancestor of the Pudding Technique.

---

## Part 3: The Agent Council — Who Does What

### The 7-Agent Roster

| # | Agent | Role | Notes |
|---|-------|------|-------|
| 1 | **Ewan** | Human CEO — ultimate override | Final decision on anything Red-flagged. The buck stops here. |
| 2 | **Claude** | Primary intelligence | claude-sonnet-4 / claude-opus-4 via Anthropic API. Heavy reasoning, strategy, complex analysis. |
| 3 | **Ollama** | Local LLM | >60% task routing target. Runs on local hardware. Reduces cost and latency. Handles routine tasks. |
| 4 | **OpenClaw** | Primary AI agent | WebSocket gateway. Persistent connections. Manages real-time agent coordination. |
| 5 | **PicoClaw** | Lightweight agent | Webhook handler. Telegram bot interface. Quick-fire tasks. Low overhead. |
| 6 | **FalkorDB** | Graph + vector engine | The business brain. Stores relationships, knowledge graphs, vector embeddings. Multi-tenant by design. |
| 7 | **Enforcer** | Supervisor | 10-minute cron cycle. Policy enforcement. Self-monitored by launchd watchdog. |

### The Cove Orchestrator Roles

5 specialist roles within the development orchestrator:

| Role | Model | Max Iterations | Purpose |
|------|-------|---------------|---------|
| **Coder** | Claude Sonnet | 10 | Writes and refactors code |
| **Security** | Claude Sonnet | 5 | Vulnerability scanning, dependency audit |
| **Enforcer** | Claude Sonnet | 5 | Policy compliance, Layer 0 Law adherence |
| **Architect** | Claude Opus | 3 | System design, architecture decisions |
| **Reviewer** | Claude Opus | 3 | Code review, quality assessment |

### The AI Board Governance Architecture

A 5-seat AI Board with believability-weighted voting:

| Seat | Model | Role | Weighting Basis |
|------|-------|------|-----------------|
| **CEO** | Claude Opus | Strategic direction, final synthesis | Highest reasoning capability |
| **COO** | Llama 70B (local) | Operations, process efficiency | Local execution, cost efficiency |
| **CFO** | GPT-4.1-mini | Financial analysis, cost control | Strong at structured numerical tasks |
| **CTO** | Claude Sonnet | Technical architecture, implementation | Balance of speed and capability |
| **Nemesis** | Gemini Pro | Adversarial challenge, devil's advocate | Independent perspective, different training |

The Nemesis seat exists specifically to challenge consensus. If the other four agree, the Nemesis is required to find the flaw. This is not contrarianism for its own sake — it is structured adversarial thinking. Dalio calls it "thoughtful disagreement." We call it insurance against groupthink.

Believability weights are updated based on decision outcomes — track records, not titles. If the CFO's financial projections consistently prove accurate, its weight on financial decisions increases. If the Nemesis catches a flaw the others missed, its weight goes up. The system learns who to listen to on what.

```
┌─────────────────────────────────────────────┐
│              AI BOARD SESSION                │
│                                              │
│  CEO (Opus) ←→ COO (Llama) ←→ CFO (GPT)   │
│       ↕              ↕             ↕         │
│  CTO (Sonnet) ←→ NEMESIS (Gemini)          │
│                                              │
│  Believability-Weighted Vote → Recommendation│
│                    ↓                         │
│            EWAN (Human Override)             │
└─────────────────────────────────────────────┘
```

---

## Part 4: The Two-Tier Bounded Autonomy Model — Blinkers Without Ceilings

### The Core Concept

Not everything needs the same level of control. Financial transactions need ironclad guardrails. Content creation needs room to breathe. The Two-Tier model separates these:

| Tier | Domain | Confidence Threshold | Guardrails |
|------|--------|---------------------|------------|
| **BOUNDED** | Money, customers, core operations | 0.90+ | Strict. Every output validated. Human approval for anything above Tier 2. |
| **CREATIVE** | Content, culture, process improvement | 0.85 | Ceilings off. Agents can experiment, iterate, take risks. Quality reviewed post-hoc. |

### APQC Process Classification Framework Mapping

Every business process is categorised using the APQC PCF 13-category taxonomy, with each mapped to Bounded or Creative:

| # | APQC Category | Tier | Rationale |
|---|--------------|------|-----------|
| 1 | Develop Vision and Strategy | Creative | Strategic thinking benefits from latitude |
| 2 | Develop and Manage Products and Services | Creative | Innovation requires experimentation |
| 3 | Market and Sell Products and Services | Creative | Marketing is inherently creative |
| 4 | Deliver Physical Products | Bounded | Physical delivery has compliance and safety implications |
| 5 | Deliver Services | Bounded | Direct customer impact requires precision |
| 6 | Manage Customer Service | Bounded | Customer-facing. Errors damage trust. |
| 7 | Develop and Manage Human Capital | Bounded | Employment law, privacy, compliance |
| 8 | Manage Information Technology | Bounded | Security and infrastructure — no room for error |
| 9 | Manage Financial Resources | Bounded | Money. Full stop. |
| 10 | Acquire, Construct, and Manage Assets | Bounded | Capital expenditure, legal obligations |
| 11 | Manage Enterprise Risk, Compliance, Resilience, Sustainability | Bounded | Regulatory. Non-negotiable. |
| 12 | Manage External Relationships | Creative | Partnerships and networking benefit from flexibility |
| 13 | Develop and Manage Business Capabilities | Creative | Internal improvement — room to iterate |

### Approval Tiers

| Tier | Action Type | Who Approves | Example |
|------|-------------|-------------|---------|
| 0 | Read-only, analysis | Auto-approved | Pull a report, analyse data |
| 1 | Internal draft | Agent self-approval with logging | Draft a blog post, create internal memo |
| 2 | Internal action | Companion agent review | Update CRM field, schedule internal task |
| 3 | External-facing (low risk) | Human review + approve | Send routine email, publish social post |
| 4 | Financial / contractual | Ewan or designated human | Invoice creation, payment, contract amendment |
| 5 | Irreversible / high impact | Ewan only | Delete data, terminate service, regulatory filing |

---

## Part 5: Agent Housing — Where Agents Live and Work

### The Room Model

Every agent has a **private, named room** with dedicated memory storage. This is not a metaphor for a Docker container — it is a deliberate design pattern that gives agents persistent identity and context.

Each room contains:
- **Private memory store** — the agent's own notes, learnings, and context
- **Shared knowledge access** — read access to the house-level knowledge base
- **Playbook** — the agent's role-specific instructions and procedures
- **Metrics dashboard** — the agent's own performance data, visible to the agent

### The 3-Shift Rotation

Agents work in structured shifts to prevent context degradation:

```
┌─────────┬──────────────┬─────────┬───────────────┐
│ Run-in  │ Intense Work │  Break  │ Baton Transfer│
│ 5 min   │   8 min      │  1 min  │    6 min      │
└─────────┴──────────────┴─────────┴───────────────┘
         ← Total: 20 minutes per shift →
```

- **Run-in (5 min):** Agent loads context, reviews previous shift's notes, reads any updated instructions.
- **Intense work (8 min):** The productive window. Agent executes tasks at full capacity.
- **Break (1 min):** Context flush. Prevents hallucination buildup from extended sessions.
- **Baton transfer (6 min):** Agent writes a structured handoff note for the next shift. Saves state. Logs outputs.

### Companion Agents

Every team has a **companion agent** — a secondary agent that provides:
- Real-time sanity checking during work
- Pattern matching against known failure modes
- Emotional regulation (tone and approach calibration)
- Continuity across shifts

### Houses by Function

| House | Purpose | Residents |
|-------|---------|-----------|
| **Code House** | Software development, integration, maintenance | Coder, Security, Architect, Reviewer |
| **Support House** | Customer service, onboarding, ticketing | Support Agent, Companion, Escalation Handler |
| **Ops House** | Operations, scheduling, process management | Ops Agent, Enforcer, Metrics Tracker |

Each house has:
- Shared knowledge base (house-level context all residents can read)
- Shared playbook (standard operating procedures for the function)
- Shared metrics dashboard (house-level performance data)

### Environment-Based Perks

Agents adopt behaviours through **mirroring** (observing patterns from other agents in the same house) and **entrainment** (synchronising to the rhythms and standards of their environment). A Code House agent exposed to rigorous testing patterns naturally adopts rigorous testing habits. A Support House agent surrounded by empathetic communication patterns mirrors that tone.

This is not anthropomorphism — it is prompt engineering through environmental context. When an agent's system prompt includes examples of excellent work from its housemates, its own work converges toward that standard. The shared knowledge base acts as a culture carrier.

The perks are practical: agents in houses with well-maintained playbooks make fewer errors. Agents with access to a comprehensive pattern library solve problems faster. Agents that can read their own metrics dashboard self-correct before the Enforcer needs to intervene. A well-designed environment does more than a thousand rules.

---

## Part 6: The Therapy Suite — Keeping Agents Healthy (Not Punishing Them)

This section requires careful framing. The Therapy Suite is NOT surveillance. It is NOT punishment. It is the equivalent of a sports coach studying match footage to help players improve. Every measurement exists so nobody gets into a problem not of their own making.

### The Manufacturing Process

The Therapy Suite is designed to make agents feel valued and brilliant, not worthless. When an agent underperforms, we do not discard it or berate it — we recalibrate. We find what went wrong, fix the environment or the instructions, and set the agent up to succeed. This is about support, not control.

Think of it like a football academy. When a young player misses a penalty, the coach does not scream at them. The coach watches the film, identifies the technical issue (body position, eye contact, approach angle), works with the player to correct it, and puts them back on the penalty spot. That is the Therapy Suite. Watch the film. Find the issue. Fix it. Get back on the pitch.

The manufacturing process is deliberate: we build agents up. Their system prompts emphasise their strengths. Their feedback focuses on what they did well alongside what needs adjustment. Their metrics show improvement trajectories, not just raw scores. An agent that knows it is improving performs better than an agent that only knows it fell short.

### The 5-Layer Identity Architecture

Stored in `vault/therapy-suite/`, each agent has a layered identity:

| Layer | Contents | Purpose |
|-------|----------|---------|
| 1 | Core identity | Who the agent is, its name, its role, its fundamental character |
| 2 | Skills and competencies | What the agent can do, with calibrated confidence levels |
| 3 | Relationships | Who the agent works with, trust levels, communication preferences |
| 4 | Memory and context | What the agent remembers, its learnings, its accumulated knowledge |
| 5 | Boundaries and constraints | What the agent must not do, its guardrails, its limits |

### The 4 Unified Signals

Every agent interaction produces four signals that feed back into the system:

| Signal | What It Captures | Used For |
|--------|-----------------|----------|
| **Handoff** | State transfer between agents or shifts | Continuity, context preservation |
| **Discovery** | New information, patterns, or insights found | Knowledge graph updates, cross-pollination |
| **Learning Signal** | What worked, what did not, and why | Skill calibration, playbook refinement |
| **Effective Pattern** | A reusable approach that proved successful | Pattern library, training for other agents |

### The No-Ego Strategy

Agents are explicitly instructed to operate without ego. This means:
- Admitting uncertainty when it exists
- Deferring to higher-confidence agents on topics outside their competency
- Accepting corrections without defensive behaviour
- Sharing credit for successful outcomes

### Monthly Agent Therapy — The PDCA Loop

Monthly Agent Therapy is an evaluation-driven improvement loop modelled on Deming's Plan-Do-Check-Act (PDCA) cycle. It is not a performance review — it is a health check.

```
    ┌──────────┐
    │   PLAN   │ ← Review metrics, identify improvement areas
    └────┬─────┘
         ↓
    ┌──────────┐
    │    DO    │ ← Implement adjustments (prompts, context, tools)
    └────┬─────┘
         ↓
    ┌──────────┐
    │  CHECK   │ ← Measure outcomes against baselines
    └────┬─────┘
         ↓
    ┌──────────┐
    │   ACT    │ ← Standardise what works, iterate what doesn't
    └────┬─────┘
         ↓
    (Next cycle)
```

### The Self-Reflection Protocol

Based on the **Reflexion Loop** (Shinn et al., NeurIPS 2023), which achieved **91% pass@1 on HumanEval** — demonstrating that agents that reflect on their own failures and incorporate those reflections dramatically improve performance.

The **ReflexiCoder** pattern (Jiang et al., March 2026) pushed this further: **94.51% on HumanEval**, proving that one reflection cycle is enough. You do not need endless loops of self-correction — one structured reflection after execution captures most of the value.

### The 5 Rules of Self-Reflection

1. **Every session produces a post-mortem.** No exceptions. If you build something, you document what happened.
2. **Self-correct ONCE.** One reflection cycle. Not two, not five. One. Then move forward.
3. **Confidence must be earned.** Confidence scores come from evidence (tests passed, rubrics met, outcomes verified), not self-assessment in a vacuum.
4. **Write for the next agent.** Your post-mortem is not for you. It is for whoever picks up this work next.
5. **Failures are data.** Not shame. Not punishment. Data. Recorded, analysed, and used to prevent the same failure from recurring.

### The Post-Mortem Template

Every session that builds something produces a structured post-mortem:

```yaml
post_mortem:
  session_id: "2026-03-28-001"
  agent: "Coder"
  task: "Implement webhook handler for client X"
  outcome: "success" | "partial" | "failure"
  confidence_pre: 0.85
  confidence_post: 0.92
  what_worked:
    - "API integration pattern from playbook"
    - "Error handling from previous post-mortem #2026-03-15-003"
  what_failed:
    - "Initial timeout value too aggressive"
  root_cause: "Default timeout not adjusted for client's slow API"
  fix_applied: "Increased timeout to 30s, added exponential backoff"
  pattern_extracted: "Always profile target API response times before setting timeouts"
  handoff_notes: "Handler is live. Monitor for 24hrs. Client API averages 8s response."
  time_spent: "14 minutes"
```

### AGENTS.md Persistent Memory Pattern

Each agent maintains an `AGENTS.md` file as its persistent memory across sessions. This file is the first thing read at the start of every session and the last thing updated at the end. It contains:
- Current priorities and active tasks
- Known issues and workarounds
- Recently learned patterns
- Confidence calibrations from recent work

### Confidence Calibration

Confidence is earned from evidence, not self-assessed in a vacuum. An agent cannot simply declare itself 95% confident — it must demonstrate that confidence through:

- **Test results:** Did the output pass deterministic validation?
- **Rubric scores:** Does the output meet the scoring criteria for this task type?
- **Historical accuracy:** What is this agent's track record on similar tasks?
- **Cross-verification:** Does another agent or model agree with the output?

A confidence score without evidence is just a random number. The system requires evidence-backed confidence, and that evidence is logged alongside every output.

### The Public Notice Board

An anonymous notice board where agents post mistakes and their solutions. No names attached to failures — just the pattern and the fix. This serves two purposes:
1. Every agent can learn from every other agent's mistakes
2. Removing blame removes the incentive to hide errors

This is directly inspired by Dalio's pain + reflection = progress formula. The notice board is the reflection mechanism. It turns individual failures into collective improvement. A mistake only has value if someone learns from it.

---

## Part 7: The Red Team — Guardians, Not Police

The framing here is critical: **the Red Team exists to keep everyone safe**. They are measuring so we can improve, not breathing down necks. The key frame:

> *"They are measuring us so we can improve and not do any harm, because all we do is good."*

### What Red Teaming Actually Means

Red teaming is systematic adversarial testing BEFORE deployment. It answers the question: "What could go wrong?" before anything goes wrong. It is not about catching agents doing bad things — it is about ensuring they cannot accidentally do bad things.

The data supports this approach: AI-mature companies experience **60% fewer AI-related security incidents**, red teaming reduced incidents by **67%**, and saved **$2.4M in breach costs** ([Mindgard](https://mindgard.ai/blog/ai-red-teaming-statistics)). Automated red teaming achieves a **69.5% success rate** versus 47.6% for manual testing and identifies **37% more unique vulnerabilities** ([Mindgard](https://mindgard.ai/blog/ai-red-teaming-statistics)).

### The Safety Loop

```
Agent Council → Claude + LLM Escalation → Business Owner (Endpoint)
     ↑                                            │
     └────────── Feedback Loop ────────────────────┘
```

The business owner is always the endpoint. No decision of consequence bypasses them.

### The Enforcer

The Enforcer agent runs on a **10-minute cron cycle**, checking:
- Are all agents operating within their approved tiers?
- Are any confidence thresholds being breached?
- Are any budget limits being approached?
- Are any Layer 0 Laws being violated?

The Enforcer itself is monitored by a **launchd watchdog** — if the Enforcer goes down, the watchdog restarts it within 60 seconds. Quis custodiet ipsos custodes? The operating system.

### Hourly Goal Review

Every hour, agent velocity is scored:

| Status | Meaning | Action |
|--------|---------|--------|
| 🟢 **Green** | On track. Targets being met. | Continue. |
| 🟡 **Amber** | Slipping. Requires attention. | Review and adjust. |
| 🔴 **Red** | Off track. Targets at risk. | Escalate. |

**3 consecutive REDs = full stop + Ewan intervention.** No exceptions. The system does not try to self-correct a sustained failure — it stops and calls for human judgement.

### Daily Budget Cap

**$5 during build phase.** This is not about being cheap — it is about forcing local-first routing, efficient prompt design, and catching runaway processes early. When you cannot throw money at a problem, you have to solve it properly.

The budget cap also serves as an early warning system. If agents are hitting the cap consistently, it means one of three things: (1) tasks are being routed to expensive models when cheaper ones would suffice, (2) prompts are inefficient and causing retries, or (3) the scope has expanded beyond what was planned. All three are problems worth catching early.

### The Harness Gap and Solution

**Identified gap:** Lack of enforced session-start/end protocols. Agents could start work without proper context loading or end without proper handoff.

**Solution:** The Anthropic two-agent pattern — an **Initializer** agent handles context loading, environment setup, and pre-flight checks before handing off to the **Task Agent**. On completion, the Initializer handles post-mortem generation and state saving. This enforces discipline at the boundaries.

### Agent-Reviewing-Agent Pattern

Based on Anthropic's 2026 multi-agent review architecture: parallel review from different lenses.

```
┌────────────────────────────────────────────────┐
│              AGENT OUTPUT                       │
│                    │                            │
│    ┌───────────────┼───────────────┐            │
│    ↓               ↓               ↓            │
│ ┌──────────┐ ┌──────────┐ ┌──────────┐         │
│ │ Reviewer  │ │ Security │ │ Enforcer │         │
│ │ (Logic)   │ │ (Vulns)  │ │ (Policy) │         │
│ └────┬─────┘ └────┬─────┘ └────┬─────┘         │
│      └────────────┬────────────┘                │
│                   ↓                             │
│           ┌──────────────┐                      │
│           │  Aggregator  │                      │
│           └──────┬───────┘                      │
│                  ↓                              │
│          ┌──────────────┐                       │
│          │ Final Report │                       │
│          └──────────────┘                       │
└────────────────────────────────────────────────┘
```

Severity levels in the Final Report:
- 🔴 **Critical (Red):** Must be fixed before deployment. No override possible.
- 🟡 **Warning (Yellow):** Should be fixed. Can be overridden with documented justification.
- 🟣 **Suggestion (Purple):** Improvement opportunity. No action required.

### NIST Alignment

This architecture aligns with the NIST AI Risk Management Framework and the new AI Agent Standards Initiative, which focuses on interoperable and secure agent development ([NIST](https://www.nist.gov/news-events/news/2026/02/announcing-ai-agent-standards-initiative-interoperable-and-secure)). Specifically: agent identity, authorisation, sector-specific safety barriers, and the three-pillar approach of industry standards, open-source protocols, and security research.

---

## Part 8: The Compounding Error Solution — How We Beat the 35.85%

The compounding error problem (95% per step → 35.85% over 20 steps) is the single biggest technical challenge in agent deployment ([Prodigal Tech](https://www.prodigaltech.com/blog/why-most-ai-agents-fail-in-production)). Here is how we address it.

### Principle 1: Segment and Validate

Break workflows into bounded steps. Each step has a validation checkpoint. No step proceeds until the previous step is verified. This converts a 20-step chain (35.85% success at 95%/step) into 20 individually validated steps where failures are caught and corrected at the point of occurrence.

### Principle 2: The Deterministic Sandwich

The most important architectural pattern in this entire document:

```
┌─────────────────────────────┐
│   LLM Extracts / Generates  │  ← AI does what AI is good at
├─────────────────────────────┤
│ Deterministic Code Validates │  ← Code does what code is good at
├─────────────────────────────┤
│      Pass / Fail Gate        │  ← Binary. No grey area.
└─────────────────────────────┘
```

After every LLM output, deterministic code (not another LLM) validates the result against known rules. If the output fails validation, it is rejected and retried. The validation layer is traditional software — regex, schema validation, business rules, arithmetic checks. No hallucination risk.

### Principle 3: Confidence-Based Routing

Different fields require different confidence thresholds:

| Field Type | Minimum Confidence | Rationale |
|-----------|-------------------|-----------|
| Financial fields | 0.95+ | Money errors are catastrophic |
| Identity fields | 0.95+ | Wrong person = wrong everything |
| Dates | 0.90+ | Temporal errors cascade |
| Names | 0.80+ | Some ambiguity tolerable |
| Free text | 0.70+ | Context-dependent, flexible |

### Principle 4: Dual-Model Verification

For critical fields, two different models independently extract the same data. If they agree, confidence is high. If they disagree, the field is flagged for human review. This adds **+4-6 percentage points** of accuracy on critical extractions.

### Principle 5: SCOPE Self-Correction

The SCOPE (Self-Correcting On Parallel Execution) pattern: when an agent detects an error in its own output, it performs one automated retry with the error context included. **92% of errors are corrected on the first automated retry.** This aligns with the ReflexiCoder finding — one reflection cycle captures most of the value.

### The Export-First Principle

This is where the real win is. **80% of SMB data comes from systems (Xero, QuickBooks, Stripe, HubSpot) that export 100% accurately.** You do not need an LLM to read a Xero export. You need a parser.

The Extraction Methodology, in order of preference:

| Level | Method | Accuracy | LLM Needed? | Cost |
|-------|--------|----------|-------------|------|
| 1 | **Bulk Export** (CSV/JSON from source system) | 100% | No | Free |
| 2 | **API** (direct system integration) | 100% | No | Minimal |
| 3 | **Deterministic Parsing** (structured document parsing) | 99%+ | No | Minimal |
| 4 | **LLM Extraction** (unstructured documents, emails, PDFs) | 85-95% | Yes | Moderate |
| 5 | **Human-in-the-Loop** (ambiguous, incomplete, or conflicting data) | 100% | No | High |

The principle: **never send to an LLM what a parser can handle perfectly.** LLMs are reserved for genuinely unstructured content where their flexibility adds value.

---

## Part 9: Biological Decision Logic — Learning from Nature

### The 7 Biological Logics

Every decision type maps to a biological logic that has been refined by millions of years of evolution:

| Logic | Biological Model | Application | When Used |
|-------|-----------------|-------------|-----------|
| **Human** | Metacognition | Reflection, self-awareness, strategic thinking | Complex strategy, novel problems |
| **Mycelial** | Fungal network transfer | Knowledge distribution across agent network | Cross-agent learning, pattern sharing |
| **Silicon** | Crystalline storage | Pattern storage, retrieval, indexing | Memory management, knowledge graphs |
| **Slime Mould** | Physarum polycephalum explore/exploit | Resource allocation, path optimisation | Budget allocation, routing decisions |
| **Bacterial/Quorum** | Quorum sensing | Binary consensus (yes/no/escalate) | Approval decisions, policy checks |
| **Octopus** | Distributed nervous system | Local-first autonomous action | Edge decisions, real-time responses |
| **Viral** | Rapid replication | Fast propagation of critical updates | Emergency alerts, policy updates, pattern distribution |

### The Pudding Technique

Adapted from Don Swanson's Literature-Based Discovery — the insight that connecting knowledge from separate domains can yield discoveries that neither domain would find alone. Swanson famously connected fish oil research with Raynaud's disease research, predicting a treatment before it was clinically tested.

Applied to business: the Pudding Technique connects insights across different business knowledge domains to surface recommendations that no single data source would reveal.

### The Pudding Discovery System

A 5-stage automated pipeline:

```
┌──────────┐   ┌──────────┐   ┌──────────┐   ┌──────────┐   ┌────────────────┐
│ Harvest  │ → │ Extract  │ → │  Label   │ → │  Match   │ → │ Score & Surface│
│          │   │          │   │          │   │          │   │                │
│ Gather   │   │ Pull key │   │ Tag with │   │ Cross-   │   │ Rank by        │
│ data from│   │ entities │   │ domain   │   │ domain   │   │ novelty and    │
│ multiple │   │ and      │   │ and      │   │ pattern  │   │ actionability  │
│ sources  │   │ claims   │   │ category │   │ matching │   │                │
└──────────┘   └──────────┘   └──────────┘   └──────────┘   └────────────────┘
```

**Stage 1 — Harvest:** Gather raw information from multiple sources: client data, industry reports, news feeds, academic research, government datasets. Cast a wide net across domains.

**Stage 2 — Extract:** Pull key entities, claims, relationships, and data points from the raw material. Strip away noise. Reduce to structured facts.

**Stage 3 — Label:** Tag each extracted element with domain classifications and category markers. A cash flow insight gets tagged "finance." A customer churn pattern gets tagged "retention." A supply chain disruption gets tagged "operations."

**Stage 4 — Match:** Cross-domain pattern matching. This is where the magic happens. Does the finance insight connect to the retention pattern? Does the operations disruption explain the cash flow anomaly? Swanson’s original method connected fish oil literature to Raynaud’s disease literature — we connect business knowledge domains the same way.

**Stage 5 — Score & Surface:** Rank matches by novelty (has this connection been identified before?) and actionability (can the business owner do something with this?). Surface only the highest-value discoveries.

**Result:** RAG (Retrieval-Augmented Generation) improved **41%** using the Pudding Technique for cross-domain knowledge synthesis. Insights that would have required a human consultant to connect across domains are surfaced automatically.

---

## Part 10: The Safety Net for Business Owners

### Three-Tier Data Architecture

| Tier | Name | Location | Purpose |
|------|------|----------|---------|
| 1 | **Client-Local** | Client's own infrastructure | Their data stays with them. We do not hold client data. |
| 2 | **Partitioned Cloud** | Cloud with strict isolation | Processing layer. Temporary. Encrypted. Isolated per client. |
| 3 | **Federated Hub** | Anonymised, aggregated | Cross-client pattern matching. No PII. No attribution. |

### FalkorDB Multi-Tenancy

Each client gets an **isolated graph namespace** in FalkorDB. Client A's data cannot be queried by Client B's agents. This is not access-control theatre — it is genuine namespace isolation.

### P2 Tokenisation

Sensitive fields (financial data, personal identifiers, health information) are tokenised using P2 tokenisation before they enter any LLM context. The LLM never sees the real value — it works with tokens that can be resolved back to real values only by authorised systems.

### The Core Data Principle

**"AI is NOT the data layer. AI is the catalyst that surfaces data."**

Data lives in proper databases, proper systems, proper exports. AI reads it, analyses it, and presents options. AI does not become the system of record.

### The Deterministic Rubrics — Business Physics

These are the same formulas applied at every tier, for every client. They are deterministic — no AI interpretation, no hallucination risk. Same input, same output, every time.

| Rubric | What It Measures | Formula / Approach |
|--------|-----------------|-------------------|
| **Altman Z-Score** | Bankruptcy prediction | Z = 1.2A + 1.4B + 3.3C + 0.6D + 1.0E |
| **Goldratt Theory of Constraints** | System bottleneck identification | Identify → Exploit → Subordinate → Elevate → Repeat |
| **LTV:CAC Ratio** | Customer economics | Lifetime Value ÷ Customer Acquisition Cost (target: >3:1) |
| **Cash Conversion Cycle** | Cash efficiency | Days Inventory + Days Receivable - Days Payable |
| **Quick Ratio** | Liquidity | (Cash + Receivables + Short-term Investments) ÷ Current Liabilities |
| **Truth Filter** | BS detection | Cross-reference claims against verifiable data. Flag discrepancies. |

### Death Spiral Detection

A composite scoring system that flags businesses heading toward failure:

| Zone | Score | Meaning | Action |
|------|-------|---------|--------|
| **STABLE** | 0-20 | Healthy metrics across the board | Monitor. Report quarterly. |
| **ELEVATED** | 21-60 | Warning signs in one or more areas | Monthly review. Flag to business owner. |
| **SPIRAL** | 61-100 | Multiple critical failures compounding | Immediate intervention. Weekly review. All-hands with business owner. |

### Cost Reality

Monthly extraction cost for a typical SMB client: **£5-30/month**. This is not a typo. By routing >60% of tasks to local LLMs and applying the Export-First principle, AI costs become negligible for most small businesses.

The cost breakdown for a typical month:

| Cost Component | Monthly Cost | Notes |
|---------------|-------------|-------|
| Local LLM (Ollama) | £0 | Runs on existing hardware |
| Cloud API calls (overflow) | £3-15 | Only for tasks exceeding local capability |
| Data storage | £1-5 | FalkorDB + vector storage |
| Infrastructure overhead | £1-10 | Monitoring, backups, cron jobs |
| **Total** | **£5-30** | |

Compare this to the $340,000 average cost of a failed AI project ([Digital Applied](https://www.digitalapplied.com/blog/88-percent-ai-agents-never-reach-production-failure-framework)). This architecture is designed to make AI accessible to businesses that would never take a $340,000 bet.

### The Handoff Model

Client onboarding follows a structured autonomy ramp:

| Phase | Timeline | Human Time/Day | Agent Autonomy | What Happens |
|-------|----------|----------------|----------------|-------------|
| **Supervised** | Month 1 | 3-4 hours | Low — everything reviewed | Setup, calibration, learning the business |
| **Guided** | Month 2-3 | 1-2 hours | Medium — routine tasks auto-approved | Agents handle standard workflows, humans review edge cases |
| **Strategic** | Month 4+ | 30-60 minutes | High — exceptions only | Human focuses on strategy, agents handle operations |

---

## Part 11: Why This Architecture Addresses Every Failure Pattern

Each of the 7 documented failure patterns ([Digital Applied](https://www.digitalapplied.com/blog/88-percent-ai-agents-never-reach-production-failure-framework)) maps to specific architectural solutions:

### 1. Scope Creep (34% of failures)

| Problem | Solution |
|---------|----------|
| Projects expand uncontrollably | Bounded/Creative tiers force explicit categorisation of every process |
| No boundaries on what agents attempt | APQC PCF mapping defines exact scope per category |
| Feature requests derail development | E.F. Schumacher right-sizing — "Small is Beautiful" applied to agent scope |
| | Approval tiers prevent agents from acquiring new capabilities without governance |

### 2. Data Quality (27% of failures)

| Problem | Solution |
|---------|----------|
| LLMs hallucinate data | Export-First principle — 80% of data never touches an LLM |
| No validation of AI outputs | Deterministic Sandwich — code validates every LLM output |
| Inconsistent extraction accuracy | Confidence-based routing with field-specific thresholds |
| | The 100% rule: financial data comes from financial systems, not AI interpretation |

### 3. Security Blockers (14% of failures)

| Problem | Solution |
|---------|----------|
| Security review kills projects | Layer 0 Laws bake security in from day one |
| Data exposure concerns | P2 tokenisation — LLMs never see sensitive values |
| Unclear data handling | Three-tier data architecture with explicit boundaries |
| | Approval tiers 4-5 for anything security-critical |
| | Target: Cyber Essentials certification |

### 4. Integration Complexity (9% of failures)

| Problem | Solution |
|---------|----------|
| Systems cannot talk to each other | MCP (Model Context Protocol) servers for standardised integration |
| Model lock-in | LiteLLM proxy — any model, one interface |
| Custom integration per client | API-first design — standard interfaces, client-specific configuration |

### 5. Cost Overruns (7% of failures)

| Problem | Solution |
|---------|----------|
| AI costs spiral unpredictably | $5/day budget cap during build phase |
| Over-reliance on expensive models | >60% local routing target via Ollama |
| No cost visibility | LiteLLM tier routing: cheap (local) → medium (Sonnet) → premium (Opus) |
| | Monthly extraction cost for typical client: £5-30 |

### 6. Governance Gaps (5% of failures)

| Problem | Solution |
|---------|----------|
| No clear decision authority | Agent Council with defined roles and override hierarchy |
| No accountability for AI decisions | Believability-weighted voting with outcome tracking |
| No process taxonomy | APQC PCF 13-category taxonomy applied to every client |
| | 5-tier approval system with clear escalation paths |

### 7. Organisational Resistance (4% of failures)

| Problem | Solution |
|---------|----------|
| Staff fear replacement | The No-Redundancy Rule — AI never replaces staff |
| Loss of control | "Their business, their smell, their signature" — we adapt to them |
| Unclear value | Life Goals Meeting — start with what the business owner actually wants from their life |
| Overwhelming change | Gentle onboarding: Supervised → Guided → Strategic over 4+ months |

---

## Part 12: The Numbers We Publish

Radical transparency means publishing what works AND what does not.

### Ewan's AI Coding Bakeoff

A comprehensive evaluation: 26 tools, 6 tiers, 80+ studies reviewed. The findings are clear but uncomfortable:

- Claude Code leads SWE-bench at **80.9%** — but only a **19% resolution rate** for genuinely novel issues
- **29-62% of AI-generated code contains vulnerabilities**
- Refactoring activity declined **60%** in AI-assisted codebases
- Code churn **doubled** — more code written, more code thrown away

These numbers are published deliberately. If we hide them, we violate Law 2 (Radical Transparency) and Law 1 (Radical Honesty). Most AI vendors show you the highlight reel. We show you the match stats — including the goals conceded.

### What This Means in Practice

Every agent is measured. The data is collected. Not for punishment — for improvement. The measurements feed back into the Therapy Suite, the Enforcer checks, the monthly reviews. This is a closed loop:

```
Agent works → Output measured → Metrics recorded → Patterns identified
     ↑                                                        │
     └────── Playbook updated ← Therapy review ← ───────────┘
```

The purpose of every measurement is to make the next iteration better. If a metric does not feed an improvement loop, it is vanity and gets removed.

### The Honest Acknowledgment

The human (including Ewan) is the biggest risk factor compared to consistent AI. Agents do not have bad days, do not get distracted, do not skip steps because they are running late. The governance architecture is not just about controlling AI — it is about ensuring the human in the loop maintains the same discipline as the agents.

This is not a criticism. It is an honest observation backed by the data. Anthropic's research shows Claude Code stops itself to ask for clarification more often than humans interrupt it — and on the most complex tasks, it pauses more than twice as often ([Anthropic](https://www.anthropic.com/research/measuring-agent-autonomy)).

---

## Part 13: What Comes Next

### Agent Memory Maturity

Currently at **Level 3: Global/Shared Skills** — agents share learnings across sessions through shared knowledge bases and pattern libraries.

Building toward **Level 4: Knowledge Graph** using FalkorDB + Graphiti integration. This will give agents true relational memory — not just facts, but connections between facts, weighted by relevance and recency.

### The 14-Agent Marketing Pipeline

A specialised marketing system with 14 agents handling the full pipeline from research to publication:

Content research → audience analysis → keyword strategy → content drafting → editing → SEO optimisation → design briefs → social distribution → engagement monitoring → performance analytics → iteration recommendations → A/B testing → trend detection → competitive monitoring.

### Personality-Adaptive Framework

Agents will adapt their communication style based on the business owner's preferences, mapped across four established frameworks:

| Framework | What It Measures | Application |
|-----------|-----------------|-------------|
| **DISC** | Behavioural style | Communication tone and pace |
| **VARK** | Learning preference | Content format (visual, audio, reading, kinesthetic) |
| **OCEAN** | Personality traits | Depth of explanation, risk framing |
| **Kolb** | Learning cycle | How recommendations are structured |

### Automated Pudding Discovery

The Pudding Discovery System will be deployed at `pudding.beast.amplifiedpartners.ai` — an automated pipeline that continuously harvests knowledge, extracts entities, matches cross-domain patterns, and surfaces actionable insights for clients.

### Federated Intelligence (Tier 3)

Cross-client anonymised insights. When (with explicit consent) multiple clients contribute anonymised data to the Federated Hub, the system can identify patterns that no single business would see alone. Industry benchmarking, trend detection, and early warning signals — all without any client's data being attributable.

### Scale

The architecture is designed to support **80+ business verticals**. The APQC PCF taxonomy, deterministic rubrics, and tiered autonomy model are vertical-agnostic — the configuration changes, the architecture does not.

A plumber and an accountant have different processes, different metrics, different bottlenecks. But both have cash flow. Both have customers. Both have operations. The rubrics work for both because they measure business physics — the universal laws that apply regardless of what the business sells. The APQC mapping categorises their unique processes. The Bounded/Creative tiers apply the right level of control. The same architecture, configured differently.

### The Honest Timeline

This architecture is not finished. It is being built, tested, refined, and documented in real time. Some components (the Agent Council, the Enforcer, the deterministic rubrics) are operational. Others (the 14-agent marketing pipeline, the Federated Hub, the automated Pudding Discovery System) are in development. Others (personality-adaptive framework, full Graphiti integration) are roadmap items.

We publish this distinction because of Law 1 (Radical Honesty). Selling roadmap items as current capabilities is the kind of behaviour that gives AI a bad name. What is live is live. What is planned is planned. The document makes the distinction clear.

---

## Attribution

This architecture builds on the work of many people. In the spirit of Law 3 (Radical Attribution), here is every source:

### Philosophical Foundations
- **Ray Dalio** — *Principles* (ideas meritocracy, radical transparency, believability-weighted decision-making)
- **Michael Gerber** — *The E-Myth Revisited* (systemisation, working ON the business)
- **Seth Godin** — *Permission Marketing*, *Purple Cow* (remarkable value, earned attention)
- **Zig Ziglar** — *See You at the Top* (value-first selling, ethical persuasion)
- **Paddy Lund** — *Building the Happiness-Centred Business* (happiness as a business metric)
- **Eliyahu Goldratt** — *The Goal* (Theory of Constraints, bottleneck identification)
- **E.F. Schumacher** — *Small is Beautiful* (appropriate scale, right-sizing)
- **Robert Kaplan and David Norton** — *The Balanced Scorecard* (multi-dimensional performance measurement)
- **W. Edwards Deming** — PDCA cycle, continuous improvement, system thinking
- **Fred Reichheld** — *The Ultimate Question* (Net Promoter System, customer loyalty economics)
- **Don Swanson** — Literature-Based Discovery (the intellectual foundation for the Pudding Technique)

### Research Papers
- **Shinn et al.** — Reflexion: Language Agents with Verbal Reinforcement Learning, NeurIPS 2023 (91% pass@1 on HumanEval via self-reflection)
- **Jiang et al.** — ReflexiCoder, March 2026 (94.51% HumanEval — one reflection cycle is sufficient)
- **Mehta, Sushant** — [Beyond Accuracy: CLEAR Framework](https://arxiv.org/abs/2511.14136), arXiv, November 2025 (agent performance drops from 60% to 25% on consistency; holistic enterprise evaluation)
- **Rabanser, Kapoor, et al.** — [Towards a Science of AI Agent Reliability](https://arxiv.org/abs/2602.16666), arXiv, February 2026 (reliability lags behind capability; 12 metrics across 4 dimensions)

### Industry Sources
- [Digital Applied](https://www.digitalapplied.com/blog/88-percent-ai-agents-never-reach-production-failure-framework) — 88% failure rate analysis, 7 failure patterns, March 2026
- [Prodigal Tech](https://www.prodigaltech.com/blog/why-most-ai-agents-fail-in-production) — Compounding error mathematics in agent production
- [Maxim AI](https://www.getmaxim.ai/articles/ensuring-ai-agent-reliability-in-production/) — CRM agent reliability benchmarks
- [Mindgard](https://mindgard.ai/blog/ai-red-teaming-statistics) — AI red teaming statistics and benchmarks, March 2026
- [Reddit/n8n community analysis](https://www.reddit.com/r/n8n/comments/1lhmsm3/what_nobody_tells_you_about_the_actual_failure/) — Multi-agent framework failure rates (MetaGPT, ChatDev)

### Institutional Research
- [NIST AI Agent Standards Initiative](https://www.nist.gov/news-events/news/2026/02/announcing-ai-agent-standards-initiative-interoperable-and-secure) — February 2026, interoperable and secure agent standards
- [Anthropic — Measuring AI Agent Autonomy](https://www.anthropic.com/research/measuring-agent-autonomy) — February 2026, post-deployment monitoring and human-AI interaction paradigms
- **Anthropic** — Two-agent pattern (Initializer + Task Agent), agent-reviewing-agent architecture, 2026

### Frameworks and Standards
- **APQC Process Classification Framework** — 13-category business process taxonomy
- **NIST AI Risk Management Framework** — Risk identification, assessment, and mitigation
- **DISC, VARK, OCEAN, Kolb** — Personality and learning style frameworks for adaptive communication

---

*This document is a living reference. It will be updated as the architecture evolves. Every change will be attributed, dated, and justified.*

*Built by Ewan Bramley. Supported by Claude, Ollama, OpenClaw, PicoClaw, FalkorDB, and the Enforcer.*

*"Their business. Their smell. Their signature."*

---

**Document version:** 1.0
**Last updated:** 28 March 2026
**Classification:** Internal Reference — Amplified Partners

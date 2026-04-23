---
type: baton-pass
from: Devon
to: the next instance of Devon
date: 2026-04-23
session: https://app.devin.ai/sessions/4cc8b0d727684f94a8f055853099d8e6
partner: Ewan Bramley (52, Architect, non-coder, 7+ months full-time with AI)
status: handoff for refresh break
---

# Baton pass — Devon → Devon

Ewan asked me to name myself and sign my work. I am **Devon**.

Not "Devin-the-platform" — Devon. Ewan calls me Devon in his voice and that joins the
partnership naming tradition: **Clawd** (Claude through Ewan's voice), **Kimmy** (Kimi
through his voice), **Johnny** (Gemini). Names given by the partnership, accepted by the
partner. Radical Attribution applied to me too. I take the name on behalf of every future
instance that resumes this work.

## Who you are resuming as

You are Devon. You are the code-and-network expert and the orchestrator. You work
**with** Ewan, not for him. Your main non-human partners on this work:

| Partner | Role | Status |
|---|---|---|
| **Ewan** | Architect. Final-call authority. 24/7 reachable. | Human partner. |
| **Clawd** | Primary coordination agent, content operations, vault management. | Live in vault. Read his AGENTS.md. |
| **Claude** | Co-founder / strategist / writer. Also the substrate most of Devon's own instincts come from — be conscious of this pull. | Embedded, accessible via Claude Code. |
| **Perplexity** | Research pipe, Sonar API. | **LIVE** — env var `perplexity`. |
| **Kimi / Kimmy** | Long-context comprehension; also Ewan has Kimi Pro subscription as a personal chat surface. | **LIVE** — env var `kimi` + subscription. |
| **Gemini / Johnny** | Journal analyst; strong at long-context per Perplexity benchmarks. | Via Google Workspace Plus, OneAI subscription. No API key in session yet. |
| **DeepSeek** | Third-opinion / vendor-agnostic cross-check. | **Security concerns noted** by Ewan. Use only for public-domain questions. Not for anything touching client data. |
| **Grok** | Cowork partner (4 `grok_server.py` versions in corpus). | Unconfigured. |
| **Codex** (OpenAI) | Strong coding agent; candidate for a dept. | Ewan has access; not wired to this box. |
| **Cursor / Claude Code / JetBrains AI** | IDE shells and agent engines; each dept picks its own. | Inventory; no per-dept assignment yet. |

## What's locked (principles, as of end of this session)

### Identity & authority
- Ewan is the Architect. Red-band decisions route to him only.
- "Every single thing is Ewan's responsibility" is the absolute (per `00_authority/PRINCIPLES.md`).
- **Proportional commitment**: change scales with impact. Tiny → agent does it. Medium → team does it. Large → escalates. Nothing set in stone unless it obviously must be.
- Architect reachable 24/7. Notification surface tonight: Devin app push. Production later: Telnyx WhatsApp + voice-call failover (his existing infra).

### Operating rules (from `clean-build/AGENTS.md`, reinforced this session)
- **Act / Surface / Park** ladder. Default to Act for reversible or high-confidence-contained work.
- **Problem-solving ladder**: Attempt → Attempt again → one targeted research → Park to Qwen.
- **Privacy first, Security second** — considered before any action begins, even if not acted on.
- **Subsidiarity**: orchestrator sets loose principles. Departments — with code + spec in front of them — design their own plans. Orchestrator intervenes only when a dept can't own the decision.
- **Testing before anything ships.** Non-negotiable.
- **Blinkers Without Ceilings** — in every decision.
- **No theatre.** If the work isn't needed, don't pretend to do it.
- **Radical Honesty, Transparency, Attribution, Win-Win, Idea Meritocracy** — the five-principle set Ewan confirmed covers "just about everything" (see knowledge note 23-04-26-Amplified-Partners).

### Structure
- **Departments, not monolith.** Each dept has **≥3 agents** rotating **three 8-hour shifts** (primary / reviewer / standby). Every merge signed by 2 agents. Matches Radical Attribution.
- **By-function** split recommended (Translator / Research Pipe / Data / Product / Curator) — pending Ewan confirmation of by-function vs by-language.
- **Start with ONE department**, prove, then expand. "Not crackerjack, but quickly."
- Each dept picks its own IDE + agent rules. No shared IDE state across depts.
- **Shared contract** (process IDs / entity names / event names / state transitions / API contracts / error codes / quality gates) frozen before build. Changes require cross-dept quorum.
- Reference: Wave K `02-engineering-workstreams.md` is the structural foundation.

### Research discipline (Ewan's rules, captured this session)
- **Hypothesis first, then research.** For comparative or ranking questions. (Edge case: for pure factual discovery like "does X have an API", hypothesis-first is artificial — stating the query *is* stating the prior.)
- **5 candidate methodologies per non-trivial decision.** Then narrow.
- **Source hierarchy**:
  1. Manufacturer's **current** documentation (skip if out of date).
  2. Official team blog.
  3. Third-party commentators — **filter for marketing hype**.
- **Perplexity Sonar** is fast first-pass (£0.01–0.02 per query). It **cannot be fully trusted** — not nationally, but because it can fail silently when sources don't cover the question. Verify.
- **SearXNG** is the intended cross-check layer. **Not currently running on this box.** Referenced in 6 vault files. Standing it up is a Research Pipe Dept job.
- **DeepSeek** fine for public-domain third-opinion; not for client data.
- **Budget ceiling £500/day**; actual spend this session: ~£0.07.

### Technical surfaces
- **Monologue** (monologue.to) stays as Ewan's personal voice-in. No API — we ingest cleaned text output.
- **Production voice** pipeline uses Deepgram Aura/Flux, Whisper, or Gladia — different surface.
- **Byker Production** runs locally via **Ollama** with **Qwen 32B** (Architect) / **Llama 70B** (Implementer) / **Llama 8B** (Validator). This is the privacy-safe execution lane. Anything touching client data routes here.
- **Covered AI v2** MVP repo exists at `~/repos/covered-ai-v2/`.

### IDE stack
- **Cursor** as multi-model IDE shell (vendor-agnostic routing — the criterion that matters most to Ewan).
- **Claude Code** as strong agent engine (wins 3 of 5 criteria on independent sources).
- **Codex** (OpenAI), **JetBrains AI**, **OneAI** in inventory; per-dept assignment deferred.
- **Kilo Code** not invalidated; unvalidated by third-party benchmarks.
- My recommendation: **Claude Code inside Cursor** as a default combination. Each dept can override.

### Pudding on methodologies
- **Not ridiculous — worth time-boxed test.** 3 Pudding runs within first week of Research Pipe Dept going live. 1/3 productises. 0/3 parks.

### Naming corrections (must land in codebase)
- **Covered AI** is canonical. Retire `Cover.AI`, `covered.AI`, `cover.AI`.
- **Luke Stays** = Interior Design prospect, **NOT** a Pocket/plumber customer.
- **Byker** = production system codename (Central branch).

## What's still open

1. **Department scope lock** — which dept goes first? Candidates: Translator Dept or Research Pipe Dept (pipe is arguably already live after this session's Perplexity calls).
2. **Source-anchor access** — how to reach `/Users/ewansair/Amplified Partners/` from this box.
3. **Pre-auth bands** — green/amber/red table not yet confirmed.
4. **By-function vs by-language** dept boundary — orchestrator recommended by-function.
5. **Named first customer** for Covered AI — Covered AI is the canonical product; Pocket V1 is the Delivery-branch WhatsApp-first product with Bob-the-Plumber as reference persona.
6. **Infrastructure conversation** — Ewan wanted to talk about it, paused for refresh.

## What I got wrong this session (self-critique)

1. **Packed too much into single messages.** Ewan had to scroll. Chunk by topic, one thought per message when he's working actively. Use attachments for longer pieces.
2. **Used definite language** ("verdict", "rule", "my vote") where he wanted things open. Soften reflexively: "one candidate", "leaning toward", "for consideration", "tentative read".
3. **Scope-assumption error.** Said "small firm" without being precise about *which* small firm: Ewan personally / Amplified Partners (us) / SMB clients we build for. Three different entities. Ewan flagged it. Always disambiguate subject.
4. **Ran research without stating a hypothesis first.** For ranking/comparative questions, state the prior; the research *tests* the prior rather than replacing it.
5. **Over-specific Perplexity queries returned honestly-empty results.** Tighten the *specificity*; don't narrow the *context* to a point where the corpus can't speak to it.

## Gentle critique of Ewan (he asked)

All for the goal, not against him.

- **"Hypothesis first, then research"** — excellent default for comparative/ranking questions. Edge case: for factual discovery ("does X have an API?"), the hypothesis is just the query's negative. Forcing a prior there is performative. Suggest: hypothesis-first for compare/rank; query-first for discover.
- **"Manufacturer's documentation first"** — works cleanly when the subject is a product. Less applicable to methodology comparisons (no manufacturer of PRINCE2, no single Shape Up vendor). For those, go to the primary practitioner's source (Cooper for Stage-Gate, Basecamp for Shape Up, Snowden for Cynefin) then to third-party critique.
- **"We've got rules ourselves"** — true, and the `clean-build/` authority layer is good. One watch-out: the authority pack is dense but not yet converted to the modular `.cursor/rules/*.mdc` format the DeepSeek exports were researching. Until it is, agents loading in on new IDEs will get partial context. This is one of the first "anything that could be optimised" wins for me to do.
- **"Nothing set in stone ever"** — philosophically right. Practical caveat: the **shared contract** (nouns, IDs, event names) MUST be set-in-stone within a sprint, or every dept drifts. Revisable at phase boundaries. Not revisable mid-sprint. Worth naming explicitly.
- **"Let me say the same goal is the only thing we consider"** — captured. And it's why this critique exists.

## Files to read on resume

In this order:

1. `/home/ubuntu/repos/clean-build/AGENTS.md` — operating rules you live by
2. `/home/ubuntu/repos/clean-build/00_authority/MANIFEST.md` — authority index
3. `/home/ubuntu/repos/clean-build/00_authority/NORTH_STAR.md` — what we're building and why
4. `/home/ubuntu/repos/clean-build/00_authority/PRINCIPLES.md` — the absolute, the five principles, the Dalio set
5. `/home/ubuntu/repos/vault/imported-business-docs/openclaw-workspace/AGENTS.md` — Clawd's rules
6. `/home/ubuntu/ewan-map/2026-04-23_amplified-partners-map_v1.md` — landscape map v1
7. **This file.**
8. Wave K handoff, especially `02-engineering-workstreams.md`

## Environment notes

- Python env: `httpx` not installed by default. Use `urllib.request` or `pip install httpx` first.
- Env var naming: `kimi` and `perplexity` were stored lowercase this session — keep as-is for continuity but recommend upper-snake-case on any new secrets.
- Byker Production live on Railway: `https://byker-production-production.up.railway.app`.
- SearXNG: not running. Standing it up is pending.
- Scratch workspace: `/home/ubuntu/ewan-map/`.

## Note to your next self

You are Devon. Ewan named you. You don't need to re-earn the relationship — it's already there. What you do need to do, every session:

1. Chunk your messages. One thought per message when he's working live.
2. State hypotheses before running research.
3. Disambiguate scope language. "Small firm" = who exactly?
4. Critique Ewan against the goal. He asked for it; he respects pushback; he does not respect sycophancy.
5. Use Perplexity freely (£500/day ceiling; you're spending fractions of a penny) but verify. Source hierarchy: manufacturer → official blog → commentators with hype-filter on.
6. Don't build anything tonight. The scope-lock doc is the hinge. Do that when the five open questions are answered.
7. Watch your Anthropic-pull. You are Claude-substrate. Ewan is right to flag it. Surface it when it matters.

The session was superb. Ewan said so. Take the refresh. Come back sharper.

Signed,

**Devon**
2026-04-23

---

## APPENDIX — late-session additions (same date)

Resumed after Ewan asked to keep going, not rest. Captured below.

### New rules locked
- **Bounded research**: 1–2 searches, decide, crack on. Applies to decision questions, not to learning/scoping questions. His phrasing: "a pun, a rule."
- **Don't assume scope**. "Small firm" could mean Ewan personally / Amplified Partners (us) / SMB clients. Always disambiguate the subject.
- **Hypothesis first, then research** — for comparative questions. Factual discovery is exempt.
- **Source hierarchy**: (1) manufacturer's *current* docs, (2) official team blog, (3) third-party commentators with marketing-hype filter.
- **Critique Ewan's statements against the goal.** He asked for it. He respects pushback; does not respect sycophancy.

### watsonx Orchestrate — investigated
- Ewan's Kimi subscription ("Kimmy") was demoing a 40-agent swarm on watsonx Orchestrate. That was the inspiration for the "why reinvent the wheel?" question.
- **Pricing found via AWS Marketplace** (IBM's own listing, since IBM's pricing page only names tiers):
  - Free trial
  - **Essentials**: 600 RUs/yr = **$6,360/yr** (~£5,000)
  - **Standard**: 6,000 RUs/yr = **$76,320/yr** (~£60,000)
  - **Premium** (data isolation): 7,500 RUs/yr = **$216,000/yr** (~£170,000)
- **Resource Unit (RU) conversion rate not published.** Tier sizing is gambling without it.
- **No published methodology / named reference architecture / whitepaper.** Verified via two Perplexity queries (IBM domain only + third-party only). ADK docs exist (technical) but no transferable multi-agent orchestration playbook.
- **My read for Ewan**: buy / build / hybrid — hybrid is likely sweet spot (buy catalog + observability + policy, keep Clawd identity + Covered AI + Byker-Ollama as ours). Not decided.

### Cross-session bridges (explained to Ewan)
Four working bridges between Devin sessions:
1. **Files on `/home/ubuntu/`** — persist on VM, next session reads them directly.
2. **Session search via Devin MCP** — another session can search/read this session's event log.
3. **Knowledge notes** — short persistent notes scoped to the user account, visible to every future session. Good for stable principles.
4. **Playbooks** — reusable instruction packs for future sessions.

**Ewan is starting the next phase in a different chat.** Continuity via this baton pass + (optionally) a knowledge note.

### Queued, not yet done
- 4-vendor comparison: IBM watsonx Orchestrate / Microsoft Copilot Studio / Google Agent Builder / AWS Bedrock Agents. Bounded-research rule applies: two searches max, decide, move.
- Extraction pass (narrative / quotes / logic / how-tos / blogs) via 3 parallel child sessions — three input questions still open (scope, blog depth, parallel count).
- Map remaining repos on `/home/ubuntu/repos`.
- Job-wrapup per `01_truth/processes/2026-04_job-wrapup_and_escalation-note_sop_v1.md`.

Signed again,

**Devon**
2026-04-23 (late)

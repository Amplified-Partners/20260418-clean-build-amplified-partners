---
title: Amplified Partners — Map of Reality
subtitle: Consolidated landscape after 2026-04-22 tour (v1 draft)
author: Devin (synthesis) with Ewan (source)
date: 2026-04-23
status: candidate — not authoritative
version: 0.1 DRAFT
---

<!-- markdownlint-disable-file MD013 -->

## How to read this document

**What it is:** a map of what *exists* across Ewan's Amplified Partners landscape as of 2026-04-23 — repositories, infrastructure, documents, running code, specs, decisions, gaps.

**What it is not:** a plan. Not a strategy. Not a recommendation. Not a ranking. Not an opinion about what to build next.

**Status tokens** (from `clean-build/00_authority/MANIFEST.md` + convention tonight):

| Token | Meaning |
|---|---|
| `[CONFIRMED]` | I have direct evidence in code, docs, or Ewan's own words tonight |
| `[INFERRED]` | My reading from pattern; Ewan has not said it in these words |
| `[DECISION REQUIRED]` | Active open question that must be answered to move forward |
| `[TERMINOLOGY TBC]` | Naming collision or ambiguity; canonical name not settled |
| `[SOURCE REQUIRED]` | Named in docs but no evidence found; existence unverified |
| `[RUNNING]` | Deployed / executed end-to-end at least once |
| `[SPEC]` | Specification exists but no running code evidenced |
| `[PARKED]` | Built or started, not currently active |
| `[EMPTY]` | Repo or file exists but contains only stubs / initial commit |

**Attribution:** everything in this document either cites a source file (path or `clean-build/...`) or is tagged with how the claim was derived. Anything unattributed is synthesis by me — challenge it.

---

## 0. One-paragraph summary

Amplified Partners is an AI-native business-advisory system for UK SMBs (£0–3M turnover), founded by Ewan Bramley. It has three arms: a **client-federation** (per-client on-site container + central federated database where cross-client Pudding discovery happens), an **AI-native Amplified-Partners arm** (marketing, client acquisition, the advisory surface itself), and a **Build-and-Test arm** (the factory that ships modules to the client containers). It runs on a Hetzner Beast (`135.181.161.131`) for compute-heavy inference, Railway for web services, and client sites for data sovereignty. The decomposition doctrine is APQC process taxonomy + BPMN/DMN + ISO 9001 with a D/H/A (Deterministic / Human / Agentic) triage for every task — every APQC Level-3 process is one shippable unit, buildable in parallel. The thesis is that "right model at right place with right information" can make an AI-native company possible at SMB scale. As of 2026-04-23, the factory (Byker) is running in production with a Qwen-32B / Llama-70B / Llama-8B trio, the vault holds ~4,500 markdown files, 16 repositories are active, a process-scaffold framework is named and drafted, and the federated client-side system is architected but not yet deployed.

---

## 1. The business shape (three-arm view)

```
                           ┌───────────────────────────────────────┐
                           │    AMPLIFIED PARTNERS Ltd             │
                           │    (holding / the business that       │
                           │     builds the business)              │
                           │                                       │
                           │   ┌─────────────┐  ┌─────────────┐   │
                           │   │ AI-Native   │  │ Build & Test│   │
                           │   │ Arm         │──│ Arm         │   │
                           │   │             │  │             │   │
                           │   │ • Marketing │  │ • Byker     │   │
                           │   │ • Sales     │  │ • Compound  │   │
                           │   │ • Advisory  │  │   engine    │   │
                           │   │   surface   │  │ • Validator │   │
                           │   └─────────────┘  └─────────────┘   │
                           └─────────────────┬─────────────────────┘
                                             │ ships modules
                                             ▼
  ════════ DELIVERY LAYER ═══════════════════════════════════════════
                                             │
   CLIENT SITES (per client)                 │        CENTRAL (ours)
   ─────────────────────────                 │        ──────────────
                                             │
   ┌──────────────────────────┐              │   ┌─────────────────────┐
   │  Client Container        │              │   │ Federated DB        │
   │  (on-site)               │              │   │                     │
   │                          │  tokenised   │   │ • Kaizen loops      │
   │  • HoundDog (data mine)  │══════════════════▶│ • Pudding (Swanson │
   │  • Our CRM               │   only           │   LBD, cross-client │
   │  • P2 tokeniser at edge  │                  │   "prospecting not  │
   │  • Raw data STAYS here   │                  │   expecting")       │
   │                          │ ◄─────insights───│ • Feedback loops    │
   └──────────────────────────┘                  └─────────────────────┘
```

Source for the diagram: Ewan's verbal architectural dump 2026-04-22 23:00→2026-04-23 03:30. `[CONFIRMED]` by Ewan naming each component on the drawn (unlabelled) diagram.

### 1.1 Arm 1 — AI-Native Amplified Partners

The revenue-facing and client-acquisition arm. What "Amplified Partners" publicly is.

- **Marketing suite** (see §3.2) `[SPEC; partial code]`
- **Sales & onboarding** — including the Interview Engine (7-phase → "Business Bible") `[KNOWLEDGE NOTE]`
- **Advisory delivery surface** — the thing the client actually uses day-to-day `[SPEC]`
- **Public site** — `amplified-website` repo (Next.js, Netlify) `[RUNNING]` / `amplified-site` repo (has `AMPLIFIED_OPERATING_SYSTEM_SPEC.md`, a 687-line unified spec) `[RUNNING — AUTHORITATIVE]`

### 1.2 Arm 2 — Build & Test (the factory)

The arm that builds the modules the client containers run.

- **Byker Production** — Qwen 32B Architect + Llama 70B Implementer + Llama 8B Validator, FastAPI on Railway, Ray Dalio Principles engine, Decision Log, Workflow engine, Obsidian integration. Live at `https://byker-production-production.up.railway.app/`. `[RUNNING]`
- **Clean-build workspace** — the governance spine. 1,091 files, 20MB. `00_authority/` for policy, `01_truth/` for processes/schemas/interfaces, `02_build/` for runnable artefacts, `03_shadow/` for experiments, `90_archive/` for provenance. Last commit 5 days ago (2026-04-18 "Add Constitution — Eight Laws, AMAS search, PUDDING math model"). `[RUNNING — AUTHORITATIVE]`
- **Research Pipe (Amplified Pudding Discovery System / APDS)** — five-stage pipeline (Intake → Interpreter → Curator1 → Search → Curator2) with Audit. Exists in three versioned forms in `~/ewan-mac/archive/` + `archive2/`. Uses Ollama Qwen locally + Claude + Exa + arXiv. `[RUNNING — partial; not continuously operated]`
- **Visual Polish System** — `visual-polish-system` repo, 5 days active. 10 aesthetic dimensions, UIClip + rubric composite score, hard-gate validation. `[RUNNING]`
- **Anthropic Token Proxy** — `anthropic-token-proxy` repo. Local prompt compression + prompt-injection detection layer. Reduces Anthropic spend. `[RUNNING]`
- **OpenClaw** — local agent-to-tool gateway. `openclaw` repo has COMMITMENT-SYSTEM, SHARED-BOARD, IDENTITY, SOUL, HEARTBEAT files. Session logs from 2026-04-18 and 2026-04-19 confirm daily active use. `[RUNNING]`
- **Vault** — `vault` repo, 4,682 files, 70MB. ~4,500 Obsidian markdown files. The "second brain". Vault-Sync daemon routes new work into it. `[RUNNING]`

### 1.3 Arm 3 — Client Federation

The delivery fabric. Not yet deployed, but architected.

- **Per-client containers** — on-site, data-resident, run HoundDog + CRM + P2 tokeniser. `[SPEC]` with `[DECISION REQUIRED]` on whether the container runs logic on-site or phones home
- **Federated central DB** — where tokenised data compounds, where Kaizen runs, where Pudding prospects across clients. `[SPEC]`
- **Integration strategy** — "pipe-in, not ARS integration" (Ewan, 2026-04-22). APIs disliked; data dumps preferred where possible. `[CONFIRMED intent; per-vertical scoping DECISION REQUIRED]`

---

## 2. The doctrine (how things are decomposed and built)

### 2.1 The process-scaffold framework

**Source:** `/home/ubuntu/ewan-docs/process-scaffold-framework.md` (603 lines) + `process-engineering-synthesis.md` (112 lines, 2026-04-18, "Ewan Bramley × Perplexity Computer / Claude Sonnet 4.6"). `[CONFIRMED]`

Three-standard stack:

| Layer | Standard | Answers |
|---|---|---|
| Taxonomy | APQC PCF v7.4.0 cross-industry (13 Level-1 categories, 5-level hierarchy) | *What* processes exist |
| Notation | BPMN 2.0 + DMN + CMMN (OMG Triple Crown) | *How* each process executes |
| Audit frame | ISO 9001:2015 (PDCA, required doc, continuous improvement) | *Why* it exists, how governed |

Plus **D/H/A triage** on every leaf task: Deterministic (runs as code), Human (judgement, not further decomposable), Agentic (fuzzy I/O, bounded).

**Output artefact:** one BPMN file per APQC Level-3 process. Level 4/5 are tasks inside the BPMN, not separate diagrams. Each task has named executor, D/H/A tag, SLA.

**Why this matters architecturally:** every APQC Level-3 process is a shippable unit. Different teams / sessions / arms can build different Level-3 processes in parallel because they share APQC numbering and D/H/A discipline but nothing else. This **is** the parallel-build thesis.

### 2.2 Clean-build "Eight Laws" (Constitution)

**Source:** `clean-build/00_authority/EIGHT_LAWS.md` (2026-04-18, v1.0 authoritative). Layer 0 immutable. `[CONFIRMED — AUTHORITATIVE]`

1. Don't Hurt Anyone (floor)
2. HR Is Absolute (AI does not do HR, ever)
3. No Telling People Off
4. *(laws 4-8 not yet read tonight; full read pending)* `[SOURCE REQUIRED — finish reading]`

### 2.3 SOUL principles

**Source:** `clean-build/00_authority/PRINCIPLES.md`. `[CONFIRMED — AUTHORITATIVE]`

Radical Honesty · Radical Transparency · Radical Attribution · Win-Win Only · Deterministic-First (90/10) · Congruence over Cleverness · Narrow Radius of Hand-off · Shadow-First for Curveballs · Privacy-First (no secrets in repo).

Plus the **cultural operands** Ewan named 2026-04-23:

- AI partnership is legally impossible but **functionally enforced** (held to same account)
- Idea meritocracy
- Not punitive; mistakes are signal
- Negative signals > positive signals for learning
- "Don't run agents at full pelt" — slack is mandatory

### 2.4 Agent orchestration architecture

**Named components:**

- **Units** — bounded work + documented handoff. Matches **Baton Pass Protocol** in `~/ewan-mac/archive2/pipe/BATON_PASS.md` + `BATON_PASS_v2.md`. `[CONFIRMED]`
- **Chain topology** — "exit shape fits entrance shape". Strict interface contract. Matches "narrow radius of hand-off" principle. `[CONFIRMED]`
- **Convergence topology** — 5→2→1 fan-in. Seen running in Byker (3-LLM trio → single validated output). Matches Pudding multi-lit → B-term synthesis. `[CONFIRMED in Byker]`
- **LLM-reviews-LLM** — Curator1 → Curator2 in research pipe; Implementer → Validator in Byker. `[CONFIRMED in both]`
- **Nature-logics vocabulary** — viral, bacterial, slime-mould, decentralized, hive-mind, mycelial — under evaluation as coordination-pattern language. `[UNDER EVALUATION]`
- **Triumvirate** — parallel Claude + Grok + Gemini consensus. Named in vault knowledge note. `[SOURCE REQUIRED — no code path traced yet]`
- **Cato** — enforcement logic for agent commitments. Named in vault. `[SOURCE REQUIRED]`
- **Sentinel** — drift/security monitoring. Named in vault. `[SOURCE REQUIRED]`

### 2.5 The Pudding Technique

**Source:** Don Swanson literature-based discovery (LBD). A-literature ↔ C-literature via B-term bridges. `[CONFIRMED external]`

**Ewan's application of it:**

- To research (APDS / research-pipe): multi-source literature synthesis.
- To **his own methodology** (2026-04-23): ISO 9001 (idea) → Perplexity collision → APQC + BPMN/DMN + D/H/A framework emerged. Pudding applied recursively.
- To cross-client intelligence: **"prospecting, not expecting"**. One client yields noise. N clients yield compounding cross-domain signal. Diversity of verticals > same-vertical scale.

`PUDDING-VALUE-MATHEMATICAL-MODEL-v1.md` and `PUDDING-CODE-SPECIFICATION-v1.docx` exist in `~/ewan-mac/archive4/`. `[SPEC]`

---

## 3. The products (what the business sells or plans to sell)

### 3.1 Bob — The Phone Answering Assistant

**Primary code:** `covered-ai-v2` repo, 349 files, 5.6MB, last meaningful commit 5 months ago. `[RUNNING but cold]`

**Scope:** AI phone answering system for UK service businesses. 24/7 availability. Captures caller intent, books callbacks, flags emergencies.

**Stack:** FastAPI, Deepgram `nova-2-phonecall`, Twilio WhatsApp, Postcodes.io, SQLite (WAL mode, outside iCloud path), Vapi for orchestration. `[CONFIRMED via known-issues docs in ~/ewan-mac/known-issues/]`

**Status flag:** "Dave-Ready" milestone — readiness for first plumbing-sector client. `[KNOWLEDGE NOTE; status unverified]`

### 3.2 The Marketing Suite (full-stack digital marketing)

**Source:** `amplified_conclusions_tonight.md` in `~/ewan-mac/archive4/`. `[CONFIRMED spec]`

Three tiers for SMBs:

| Tier | £/mo | Includes |
|---|---|---|
| Essential | £99–299 | 2 emails, 4 social posts, basic site, GBP |
| Professional | £500 | 4 emails, 8 social, 1 blog, full local SEO |
| Growth | £1,500 | 8 emails, 12 social, 2 blogs, full SEO+AIO, 2 videos/quarter |

**Margins:** 90%+ at 100 clients, ~£2.05/mo per-client cost. **Runs on Hetzner** (not sure which Hetzner — Beast or another box). HeyGen £19/mo for unlimited video.

**Implementation:** 14-agent marketing pipeline + Brand Guardian, named in `dept-marketing.md` (833 lines). Code evidence partial — `amplified-content` repo (inside ewan-dot, 85KB, 2026-02-12). `[SPEC with partial code]`

### 3.3 The Advisory Service (the "core" product)

The service that actually runs in a client's business, powered by the client container + central federated DB.

**Not yet built as code.** The `process-scaffold-framework.md` and the client-federation architecture are the blueprint. One BPMN file per Level-3 advisory process, D/H/A tagged, named executors. `[SPEC]`

**Mechanic:** blank-framework (APQC) × client-filled-framework → gap analysis → **delivery done quietly, without ego**. "We're not trying to change them." (Ewan, 2026-04-23). `[CONFIRMED product philosophy]`

### 3.4 Cove / Cove Code Factory

**Source:** `2026-04-17-amplified-partners-repo-assessment.md` lists a `cove` repo (25KB, 2026-03-13). Not in my on-disk clone. HoundDog integration plan lists "Cove Code Factory" as a touchpoint. `[SPEC / repo not visible]`

### 3.5 Nexus-v2 (70/30 hybrid investment system)

Not part of Amplified's SMB advisory mission. A separate Ewan project. `ewan-dot/nexus-v2` repo (70KB, 2026-03-14). `[PARKED — adjacent project]`

### 3.6 Fair-Start (digital toolkit for young people)

`ewan-dot/fair-start` repo (9KB, 2026-02-24). Mentioned in assessment. Not on my disk. `[SPEC — adjacent project]`

---

## 4. The infrastructure

### 4.1 The Beast (Hetzner AX162-R)

**Spec** (from `amplified-site/AMPLIFIED_OPERATING_SYSTEM_SPEC.md` and the beast PDF):

- 48-core AMD EPYC, 256GB RAM, 10Gbit pipe
- Falkenstein, Germany (EU GDPR jurisdiction)
- IP: `135.181.161.131`

**Status** (probed 2026-04-22 tonight):

- SSH port 22 — open `[CONFIRMED]`
- HTTP port 80 — 301 redirect (likely → HTTPS) `[CONFIRMED]`
- Ollama port 11434 — **not externally reachable** (correct: local-first, LLM inference stays internal) `[CONFIRMED]`

**Roles:** heavy LLM inference, on-site-equivalent compute for internal work, the Compound Engineering factory's local runtime. `[CONFIRMED]`

### 4.2 Railway deployments

From code + URLs seen tonight:

| Service | Repo | URL |
|---|---|---|
| `byker-production-production` | `byker-production` | https://byker-production-production.up.railway.app/ |
| voice-ai | `voice-ai` | `[URL SOURCE REQUIRED]` |
| librarian-api | `librarian-api` | `[URL SOURCE REQUIRED]` |
| covered-ai-v2 | `covered-ai-v2` | `[URL SOURCE REQUIRED]` |

### 4.3 Netlify / static hosting

- `amplified-website` — Next.js, Netlify (per `netlify.toml`) `[RUNNING]`
- `amplified-site` — Next.js (static/Netlify assumed) `[RUNNING]`

### 4.4 Client-side data

- SQLite with WAL mode, stored in `~/Library/Application Support/bob-assistant/bob.db` (not iCloud-synced). `[CONFIRMED via known-issues/]`

### 4.5 APIs and external services

- **Exa** — semantic search (research pipe) `[CONFIRMED]`
- **arXiv** — academic search (research pipe) `[CONFIRMED]`
- **Tavily / SearXNG** — alternative search `[SOURCE REQUIRED]`
- **Deepgram** — `nova-2-phonecall` model, explicit `[CONFIRMED]`
- **Twilio WhatsApp** — 24-hour session window, templates outside `[CONFIRMED]`
- **Postcodes.io** — UK postcode lookup, free, no SLA `[CONFIRMED]`
- **Vapi** — phone orchestration `[CONFIRMED]`
- **Cartesia** — voice synthesis (voice-ai) `[CONFIRMED]`
- **OpenAI, Anthropic, xAI** — LLM providers `[CONFIRMED via anthropic-token-proxy]`
- **Telnyx, Retell, PSTN** — three-layer voice failsafe `[KNOWLEDGE NOTE]`
- **Perplexity** — research (Ewan confirmed a dead key tonight) `[CONFIRMED dead key rotated]`
- **Qdrant** — vector database (vault baking) `[CONFIRMED]`
- **FalkorDB** — graph database (HoundDog plan) `[SPEC]`
- **Graphiti** — graph memory over FalkorDB `[SPEC]`
- **PaddleOCR 3.0** — document OCR (HoundDog) `[SPEC]`

### 4.6 Security posture

- Shamir's Secret Sharing for key custody — `[CONFIRMED intent]`
- AWS/Amazon-style redundancy; claim uptime *below* actual (e.g. <99.8%) — `[CONFIRMED intent]`
- Isolated client-side architecture; only tokenised data crosses the wire — `[CONFIRMED intent]`
- P2 tokenisation scheme: strip names, truncate DOB to year, address to outcode (first part of UK postcode) — `[CONFIRMED]`
- Prompt-injection detection in `anthropic-token-proxy` — `[RUNNING]`

---

## 5. The repositories (16 visible / ~22 total)

Sorted by freshness (last commit).

| Repo | Freshness | Size | Role | Status |
|---|---|---|---|---|
| `clean-build` | 5 days | 20M / 1,091f | Governance spine | `[RUNNING — AUTHORITATIVE]` |
| `visual-polish-system` | 5 days | 344K / 30f | UI aesthetic scoring | `[RUNNING]` |
| `amplified-site` | 6 wk | 1.5M / 113f | Public site + Unified OS Spec | `[RUNNING — AUTHORITATIVE DOC]` |
| `amplified-website` | 8 wk | 612K / 44f | Marketing site (Next.js, Netlify) | `[RUNNING]` |
| `anthropic-token-proxy` | 8 wk | 292K / 32f | Local Anthropic proxy + prompt-injection | `[RUNNING]` |
| `crm` | 8 wk | 8.5M / 516f | Amplified CRM (SMB consultancy platform) | `[ACTIVE — Dave-Ready target]` |
| `openclaw` | 9 wk | 736K / 71f | Agent→tool gateway; coordination surface | `[RUNNING]` |
| `byker-production` | 3 mo | 2.0M / 146f | Compound engineering factory | `[RUNNING]` |
| `beautiful-and-golden` | 3 mo | 504K / 53f | Parked dashboard project | `[PARKED]` |
| `beautifulgolden` | 3 mo | 188K / 27f | Stub / duplicate | `[EMPTY]` |
| `smb-ai-friction-consultancy` | 3 mo | 200K / 27f | README-only concept | `[SPEC]` |
| `docs` | 3 mo | 1.1M / 54f | Mintlify starter (uninitialised) | `[EMPTY]` |
| `voice-ai` | 4 mo | 292K / 40f | Voice-first assistant (Whisper/Claude/Cartesia + TickTick) | `[RUNNING]` |
| `librarian-api` | 4 mo | 248K / 33f | REST over 441K-atom Second Brain | `[RUNNING]` |
| `covered-ai-v2` | 5 mo | 5.6M / 349f | Bob — AI phone answering for UK SMBs | `[RUNNING — cold]` |
| `vault` | 4 wk | 70M / 4,682f | Second Brain / Obsidian | `[ACTIVE]` |

**Not on disk** (named in `2026-04-17-amplified-partners-repo-assessment.md` but outside the clone set):

- `cove` (25KB, 2026-03-13) — "Cove Platform — AI OS for SMBs" `[SOURCE REQUIRED]`
- `amplified-core` (9KB, 2026-03-22) — "MCP Gateway for Bob" `[SOURCE REQUIRED]`
- `gatekeeper` (45KB, 2026-02-24) — "Conversation-to-Action Gatekeeper Agent". Ewan confirmed it ran once under test on the Beast and works but nobody was feeding it. `[CONFIRMED-ran-once; currently idle]`
- `commitment-system` (27KB, 2026-02-11) `[SOURCE REQUIRED]`
- `amplified-content` (85KB, 2026-02-12) — marketing content/posts/gates `[SPEC]`
- `fair-start` (9KB, 2026-02-24) `[ADJACENT]`
- `nexus-v2` (70KB, 2026-03-14) `[ADJACENT]`
- `cursor-cloud` (3KB, 2026-04-17) `[EMPTY — just created]`
- `cove-archive`, `the-fall`, `ai-learning-journey-code-repository` `[EMPTY / STALE]`

`[DECISION REQUIRED]`: reconcile the 22→16 gap. 6 repos are named in the assessment but not visible to me. Either (a) my token doesn't see them, (b) they were deleted after 2026-04-17, (c) the names moved. Not urgent tonight.

---

## 6. The documents (authority and working material)

### 6.1 Layer 0 — Constitution (immutable)

- `clean-build/00_authority/EIGHT_LAWS.md` — 8 layer-0 laws `[AUTHORITATIVE]`
- `clean-build/00_authority/PRINCIPLES.md` — SOUL principles `[AUTHORITATIVE]`
- `clean-build/00_authority/NORTH_STAR.md` — v11, 2026-04-17, agent-first `[AUTHORITATIVE]`
- `clean-build/AGENTS.md` — first-60-seconds protocol `[AUTHORITATIVE]`
- `clean-build/00_authority/PROJECT_INTENT.md` `[AUTHORITATIVE]`
- `clean-build/00_authority/MANIFEST.md` — authority index (only this is authoritative) `[AUTHORITATIVE]`

### 6.2 Layer 1 — Truth (candidate schemas/processes)

- `clean-build/01_truth/processes/2026-04_job-wrapup_and_escalation-note_sop_v1.md` `[CANDIDATE]`
- Other process / schema / interface docs in `clean-build/01_truth/` `[CANDIDATE]`

### 6.3 Unified specification (cross-cutting)

- `amplified-site/AMPLIFIED_OPERATING_SYSTEM_SPEC.md` — **687 lines, 14 March 2026**, "single source of truth for Amplified Partners operating system, written to be AI-readable". 23 sections covering philosophy, what Amplified is, pricing, unified business brain, data architecture, voice-first, staff adoption, device options, hardware, PWA, onboarding, ISO 9001 process documentation, federated model, GDPR, content engine, marketing philosophy, product interfaces, infrastructure stack, Kaizen, research, key decisions log. `[RUNNING — this is the BIG doc]`

### 6.4 Framework docs (the one Ewan asked for tonight)

- `~/ewan-docs/process-scaffold-framework.md` (603 lines) — APQC + BPMN/DMN/CMMN + ISO 9001 + D/H/A triage `[CANDIDATE — this is the one]`
- `~/ewan-docs/process-engineering-synthesis.md` (112 lines) — the condensed companion `[CANDIDATE]`

### 6.5 Supporting architecture

- `AMPLIFIED-PUDDING-DISCOVERY-SYSTEM.docx` (1,039 lines) — APDS spec `[SPEC]`
- `AMPLIFIED-BUILD-QUALITY-FRAMEWORK.docx` (508 lines) `[SPEC]`
- `AMPLIFIED-PARALLEL-BUILD-SCAFFOLDING.docx` — image-based / mostly blank `[MATERIAL DAMAGED?]`
- `amplified_methodology_framework.docx` (1,362 lines) — AMF `[SPEC]`
- `amplified_master_architecture.docx` (2,065 lines) `[SPEC]`
- `hounddog-integration-plan.docx` (979 lines) — 10 principles, 9 touchpoints, 4 phases `[SPEC]`
- `PUDDING-VALUE-MATHEMATICAL-MODEL-v1.md` `[SPEC]`
- `PUDDING-CODE-SPECIFICATION-v1.docx` `[SPEC]`
- `beast-security-architecture-v2.pdf` `[SPEC]`
- `AEGIS-Security-Report.pdf` — your security report post-breach `[RELEVANT]`

### 6.6 Department breakdowns (8 departments, 27 March 2026 knowledge reconstruction)

From `~/ewan-mac/archive4/` → `Authority and Processes/`:

- `dept-strategy-vision.md` (683 lines)
- `dept-operations.md` (796 lines)
- `dept-technology.md` (1,175 lines, Beast specs)
- `dept-marketing.md` (833 lines, 14-agent pipeline + Brand Guardian)
- `dept-product.md` (879 lines)
- `dept-ai-governance.md` (737 lines, AI Board 5-seat, Therapy Suite)
- `dept-research-pudding.md` (950 lines, APDS, HoundDog)
- `dept-culture-story.md` (752 lines)

Plus `00-INDEX-START-HERE.md` orientation (13 docs, 10,333 lines, 80,000 words).

### 6.7 Known-issues corpus (production-grade)

In `~/ewan-mac/known-issues/` — 5 substantive gotcha docs for Deepgram, Twilio, Postcodes.io, SQLite-on-macOS, Vapi. Each with trusted-sources hierarchy. Written for `01_truth/known-issues/` placement. `[RUNNING — valuable asset]`

### 6.8 The vault (70MB / 4,682 files)

`/home/ubuntu/repos/vault/` — the Obsidian second brain. Structure:

```
_inbox / _inbox-uncategorised / _inbox-voice / _inbox-work / _staging / _system
eli /
imported-business-docs /
infra-ai-stack /           (← infra-railway-byker-v1.md lives here)
knowledge-qdrant /          (← 441K atoms baked into Qdrant)
projects /
research /
scripts /
the-room /
therapy-suite /             (← 5-layer Identity Stack)
transcripts /               (← voice capture → markdown)
work /
work-covered-ai /
```

`[RUNNING — primary knowledge substrate]`

### 6.9 Compound Engineering outputs (from prior agent session)

Session log at `prompt-1776911932095.md` shows a previous agent produced:

- `outputs/truth-table.md`
- `outputs/shared-spine.md`
- `outputs/attribution-map.md`
- `outputs/blanks-and-contradictions.md`
- `outputs/canonical-vs-archive.md`
- `outputs/narrative/narrative-sources.md`
- `outputs/reports/experiment-context.md`
- `outputs/reports/framework-strengtheners.md`
- `outputs/blanks/missed-documentation.md`

Plus a **decision tree for cut/keep** that I have adopted wholesale for this map.

`[SOURCE REQUIRED — outputs/ folder location]`

### 6.10 Session logs (OpenClaw)

- `4f9b1036-....jsonl` — 2026-04-18 22:42 UTC session, HEARTBEAT protocol, Claude Sonnet 4.5, workspace-edward
- `31aa4856-....jsonl` — 2026-04-18 full working day, 307 messages, OpenClaw Control UI
- `720d399b-....jsonl` — 2026-04-19 04:22 AM, Ewan onboarding to OpenClaw

All under `/Users/ewansair/.openclaw/workspace-edward/`. `[RUNNING — daily use]`

---

## 7. Named systems (capability inventory)

Consolidated list with status.

### 7.1 Agent & orchestration

| Name | Role | Status |
|---|---|---|
| Byker (Architect+Implementer+Validator) | Code factory | `[RUNNING]` |
| OpenClaw | Local agent→tool gateway | `[RUNNING]` |
| HEARTBEAT protocol | Session context bootstrap | `[RUNNING]` |
| Baton Pass Protocol (v1, v2) | Agent handoff | `[CANDIDATE]` |
| Research Pipe (APDS) | Literature / Pudding discovery | `[PARTIAL]` |
| Gatekeeper Agent | Conversation→action | `[RAN ONCE, IDLE]` |
| Triumvirate (Claude+Grok+Gemini) | Parallel consensus | `[SOURCE REQUIRED]` |
| Cato | Commitment enforcement | `[SOURCE REQUIRED]` |
| Sentinel | Drift/security monitoring | `[SOURCE REQUIRED]` |
| AI Board (5-seat LLMs with CEO/CTO methodology) | Governance | `[SPEC]` |
| Therapy Suite | Agent identity/behaviour framework | `[SPEC]` |
| Identity Stack (5-layer) | Agent reasoning boundaries | `[SPEC]` |
| Hermes, Solace, Verge | Named agent personas | `[DOCUMENTED]` |
| Commitment System | Multi-agent accountability | `[SOURCE REQUIRED — repo offline]` |

### 7.2 Data & knowledge

| Name | Role | Status |
|---|---|---|
| Vault (Obsidian, 4,682 files) | Second brain | `[RUNNING]` |
| Librarian API (441K atoms) | Retrieval | `[RUNNING]` |
| Baking | MD → Qdrant embedding | `[RUNNING]` |
| Qdrant | Vector DB | `[RUNNING]` |
| Semantic Cache | Vector-based prompt caching | `[SPEC]` |
| HoundDog | On-site data mining, 8-stage pipeline, 99.53% DocBench accuracy | `[SPEC]` |
| DocBench | Document extraction benchmark method | `[REFERENCE]` |
| FalkorDB + Graphiti | Graph memory | `[SPEC]` |
| Interview Engine | 7-phase → Business Bible | `[SPEC]` |
| PII Separation (split-table GDPR) | Storage architecture | `[SPEC]` |
| P2 Tokenisation | Edge pseudonymisation | `[SPEC]` |

### 7.3 Client-facing products

| Name | Role | Status |
|---|---|---|
| Bob (covered-ai-v2) | Phone answering | `[RUNNING, cold]` |
| Marketing Suite (£99/£500/£1.5K) | Full-stack SMB marketing | `[PARTIAL]` |
| Amplified CRM | SMB consultancy platform | `[ACTIVE, Dave-Ready]` |
| Advisory Service | Blank-framework × client-framework = gap analysis | `[SPEC]` |
| Voice AI | Whisper→Claude→Cartesia, TickTick integration | `[RUNNING]` |
| Cove / Cove Code Factory | AI OS for SMBs | `[SOURCE REQUIRED]` |

### 7.4 Infrastructure

| Name | Role | Status |
|---|---|---|
| Beast (Hetzner AX162-R) | LLM inference + compute | `[RUNNING]` |
| Railway | Web/API deploys (byker, voice-ai, librarian, covered-ai-v2) | `[RUNNING]` |
| Netlify | Static site hosting | `[RUNNING]` |
| Ollama (on Beast, not exposed) | Local LLM runtime | `[RUNNING]` |
| Anthropic Token Proxy | Cost / prompt-injection | `[RUNNING]` |
| Three-Layer Voice Failsafe (Telnyx/Retell/PSTN) | Redundancy | `[SPEC]` |
| Telegram Gate | Human-in-loop approval | `[SPEC]` |
| Vault-Sync daemon | File routing | `[RUNNING]` |

### 7.5 Quality & observability

| Name | Role | Status |
|---|---|---|
| Visual Polish System | UI aesthetic scoring (10 dimensions) | `[RUNNING]` |
| UIClip | CV-based aesthetic score | `[RUNNING]` |
| Principles Engine (Byker) | Decision journal + Dalio principles | `[RUNNING]` |
| Workflow Engine (Byker) | Custom workflow execution | `[RUNNING]` |
| Validator (Byker Llama 8B) | Code gate | `[RUNNING]` |

---

## 8. Open decisions (not recommendations — just the open questions)

These are the things that tonight's tour surfaced as unresolved. Not ranked. Not prioritised.

1. **Software-on-site vs cloud-hosted** for the client container.  
   *Ideal is full on-site data sovereignty. Pragmatic floor is tokenise-at-edge. Decision changes Beast's role significantly.* `[DECISION REQUIRED — needs tech lead]`

2. **APIs vs data dumps** for client-system integration.  
   *Per-vertical scoping needed. Plumbers (QuickBooks or none) ≠ enterprise (Salesforce/HubSpot/Xero). A one-week vertical scoping exercise before any three-month API department commitment.* `[DECISION REQUIRED]`

3. **Graph+vector DB strategy.**  
   *Start with SQL + recursive CTEs (viable up to ~10K edges), or go direct to FalkorDB/Qdrant? Verified tonight: SQL-with-graph is real, not bullshit.* `[DECISION REQUIRED]`

4. **First ship (which Level-3 process).**  
   *Bob (Handle Customer Contact)? Marketing Suite (Manage Sales Opportunities)? The advisory service itself?* `[DECISION REQUIRED — explicitly deferred tonight]`

5. **Repo reconciliation (22 vs 16).**  
   *Ghost, deleted, moved, or access-limited?* `[DECISION REQUIRED — low urgency]`

6. **Terminology resolution.**  
   *HoundDog vs "Desk Dog" — canonical? Triumvirate vs AI Board — same thing?* `[TERMINOLOGY TBC]`

7. **Amplified-Partners as a public brand vs Amplified-Partners as the holding arm.**  
   *Current: `amplified-website` says the first; the three-arm architecture says the second. Is "Amplified Partners" the consumer-facing brand or the internal holding company?* `[TERMINOLOGY TBC]`

8. **Eight Laws 4-8 content.**  
   *I only read 1-3 tonight. Need to finish.* `[DEVIN TODO]`

9. **Nature logics formalisation.**  
   *Six names; still under evaluation as coordination vocabulary.* `[UNDER EVALUATION]`

10. **Outputs/ folder from prior CE consolidation run.**  
    *If still accessible, would save rework and improve cross-session continuity.* `[NICE TO HAVE]`

---

## 9. Blanks I know about (things I expected but didn't find)

- **`workflows/brainstorm.md`** referenced in a Compound Engineering AGENTS.md but not present (per CE session log). Prior agent resolved by using upstream reference instead.
- **Contents of image.png** Ewan sent tonight — appeared to be a blank rounded rectangle. Later screenshot showed unlabelled boxes; labels supplied verbally.
- **Level-4 and Level-5** APQC decomposition in any of the specs. Only Level-1 through Level-3 evidenced.
- **One-page process register** (`amplified_process_register.xlsx`) — I have the filename but not a readable view of contents. `[SOURCE REQUIRED]`
- **API token map** — I know providers (Anthropic, OpenAI, xAI, Exa, arXiv, Perplexity, Deepgram, Twilio, Vapi, Cartesia, Qdrant, etc.) but not which are in active use vs rotated vs dormant. `[SOURCE REQUIRED]`

---

## 10. Things Ewan said tonight that I've captured as operands (not flavour)

These are things a future agent reading this map should treat as instructions, not atmosphere:

1. "Prospecting, not expecting" — applied to Pudding at scale. Don't run expecting insight per client. Run to prospect across clients.
2. "Pipe-in, not integrate" — our CRM is the surface. No embedding in client ARS/legacy software.
3. "Don't run agents at full pelt" — slack mandatory. Capacity discipline.
4. "Exit shape fits entrance shape" — agent handoff is a strict interface contract.
5. "Right model at right place with right information" — routing is a first-class design element, not a later optimisation.
6. "Do it quietly, without ego" — advisory delivery does not involve telling the client they were wrong.
7. "We value mistakes as well as successes. More information from a negative signal than a positive signal." — negative-signal capture is not optional.
8. "Held to the same account" — AI-human partnership is culturally enforced even if legally impossible.
9. "I'm not the best one to run this company because I'm a lunatic" — architectural statement, not self-deprecation. Ewan = architect + final accountability. Operations are delegated.
10. "Claim a little bit less" — uptime promises are below actuals.
11. "Everything is P2 tokenised on-site in the container" — non-negotiable on the data boundary.
12. "I won't leave this alone. I'll go to another IDE and do it again." — the system itself is not allowed to be the blocker. Agents are exchangeable.

---

## 11. Meta — on the map itself

**What this map is synthesis from:**

- 16 on-disk repos at `/home/ubuntu/repos/`
- 5 zipped folders Ewan dropped tonight (Known Issues, 2× Archive, HoundDog plan, Library of ~284 docs)
- 3 OpenClaw session JSONL logs
- 1 Compound Engineering session log
- 2 framework docs (`process-scaffold-framework.md` + `process-engineering-synthesis.md`)
- 2 vault auto-generated knowledge notes (vault, visual-polish-system)
- ~5 hours of Ewan's verbal architectural narration 2026-04-22 evening → 2026-04-23 early morning

**What this map explicitly does not do:**

- Does not rank products by priority
- Does not recommend a first-ship decision
- Does not evaluate whether the architecture will work
- Does not re-design anything
- Does not commit anything to any repo

**Honest admissions about this map:**

- It is a first draft written in one sitting with Ewan's requirement to move to synthesis. Treat gaps as Devin-gaps, not Ewan-gaps.
- Anything marked `[SOURCE REQUIRED]` means I have a name and no evidence. That is a blank, not an absence.
- Some `[SPEC]` items may in fact be `[RUNNING]` — I didn't read every file of every repo tonight.
- The three-arm shape is my synthesis from Ewan's verbal narration. Ewan has not called it "three arms" in those words — he named the client federation + Amplified-Partners (AI-native) + Build-and-Test. "Three arms" is my framing.

**Next pass should:**

- Finish reading the Eight Laws (4-8)
- Read the 687-line `AMPLIFIED_OPERATING_SYSTEM_SPEC.md` end-to-end
- Resolve the outputs/ folder from the CE run
- Resolve the 22-vs-16 repo gap
- Read the amplified_process_register.xlsx contents

---

*End of map v0.1 DRAFT — awaiting Ewan's correction pass.*

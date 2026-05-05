---
title: "MASTER AUDIT: project-latest.md + Defriction Estimates + Financial Forecasts"
id: "master-audit-and-defriction-estimates-copy"
version: 1
created: "2026-04-25"
type: "document"
topic_type: "audit"
audience: "internal"
layer: "truth"
status: "filed"
signed_by: "Devon, 2026-04-25, devin-992682c244cf444f91e0a516498afbfd"
---

# MASTER AUDIT: project-latest.md + Defriction Estimates + Financial Forecasts
## For the Building AI — Flags Only, No Solutions
**Date**: 16 March 2026
**Author**: Perplexity Computer (commissioned by Ewan Bramley)
**Purpose**: Flag everything the building AI needs to know. Don't build anything. Just flag it.

---

## DOCUMENT 1: PROJECT-LATEST.MD AUDIT

### What It Is
`project-latest.md` is a 10,110-line (409KB) Claude Project file dated 17 January 2026. It contains 37 embedded documents from Ewan's early sessions — primarily voice-transcribed thinking sessions, business bible extraction prompts, Docker orchestration scripts, and early strategy docs.

### Structure Summary (37 Embedded Docs)

| # | Document | Lines | Content |
|---|----------|-------|---------|
| 1 | bible-extraction 3.md | 1-578 | Kilo Code prompt for business knowledge extraction (v3) |
| 2 | docker-aware-immediate 2.sh | 579-1214 | Docker orchestration bash script for 4-instance extraction |
| 3 | bible-extraction 2.md | 1215-1781 | Same extraction prompt (v2) — DUPLICATE |
| 4 | "I've got a strong feeling of déjà vu..." | 1782-2215 | Business Brain Box architecture discussion |
| 5 | bible-extraction-from-zip.md | 2216-2782 | Same extraction prompt (zip variant) — DUPLICATE |
| 6 | "I think you're missing a point..." (2) | 2783-2904 | Conversation fragment about data approach |
| 7 | THE BUSINESS BIBLE - SMB Operating System | 2905-3295 | Business bible content with principles, SOPs, frameworks |
| 8 | FOUNDER STORY / SMB Operating System | 3296-3689 | Founder narrative + mission statement |
| 9 | BUSINESS-VISION-covered-ai-full-v1.md | 3690-3890 | Full business vision (still using "Covered AI" name) |
| 10 | docker-aware-immediate.sh | 3891-4526 | Same Docker script (v1) — DUPLICATE |
| 11 | "How many kilo called..." | 4527-4957 | Discussion about Kilo Code instance management |
| 12 | "he will need to orchestrate 4..." | 4958-5169 | Kilo Code orchestration planning |
| 13 | verify-permissions.sh | 5170-5423 | Permission verification shell script |
| 14 | "I have a huge amount of data..." | 5424-6854 | Massive data extraction discussion + Qdrant/Neo4j architecture |
| 15 | "so github mcp.md" | 6855-6973 | GitHub MCP setup notes |
| 16 | "I think you're missing a point..." (1) | 6974-7095 | Earlier version of conversation fragment — DUPLICATE |
| 17 | bible-extraction.md | 7096-7662 | Original extraction prompt — DUPLICATE (4th copy) |
| 18 | "I think you're missing a point..." | 7663-7784 | Yet another copy — DUPLICATE |
| 19 | "I do the related and create a master reference..." | 7785-7881 | Master reference doc discussion |
| 20 | "Got you we're gonna do this..." | 7882-7964 | Session planning |
| 21 | SESSION-SUMMARY-17-jan-2025-v1.md | 7965-8046 | Session summary from 17 Jan |
| 22 | PRODUCT-year-1-consulting-automations-v1.md | 8047-8138 | Year 1 product plan for consulting automations |
| 23 | STRATEGY-fiddly-bit-data-collection-v1.md | 8139-8242 | Data collection strategy |
| 24-28 | DUPLICATES of docs 19-23 | 8243-8700 | Exact duplicates of the above 5 documents |
| 29 | BUSINESS-VISION-covered-ai-full-v1.md | 8701-8901 | DUPLICATE of doc 9 |
| 30 | RESEARCH-speech-act-theory-intent-mapping-v1.md | 8902-9004 | Speech act theory research for intent classification |
| 31 | OPERATING-PRINCIPLE-shoulders-of-giants-v1.md | 9005-9055 | Shoulders of giants principle document |
| 32 | CORE-PRINCIPLE-covered-ai-v1.md | 9056-9112 | Core principle statement |
| 33 | "Can you do it or at least packaged up..." | 9113-9325 | SOP packaging request |
| 34 | skill-sop-expert-writer-v1.md | 9326-9670 | Skill prompt for SOP writing |
| 35 | "so its all here_" | 9671-9687 | Short confirmation note |
| 36 | "where are the documents please_..." | 9688-9716 | Document location query |
| 37 | (Remaining content) | 9717-10110 | Final fragments and conversation tails |

---

### CRITICAL FINDING: Massive Redundancy

**At least 12 of 37 documents are duplicates.** The bible-extraction prompt appears 4 times. Several conversation snippets appear 2-3 times. Five documents (19-23) are duplicated verbatim as documents 24-28. The business vision doc appears twice.

**Flag for building AI:** ~40% of project-latest.md is duplicated content. The file is 409KB but probably only ~250KB of unique content.

---

### CRITICAL GAPS — What's Missing from project-latest.md

The following concepts exist in the March 2026 specs but are ABSENT or barely mentioned in project-latest.md:

| Topic | In project-latest.md? | Where it exists instead |
|-------|----------------------|------------------------|
| **Three-tier product architecture** (Phone/Full Stack/Federated) | NO (3 mentions) | PRODUCT-ARCHITECTURE-TIERS.md (March 10) |
| **7 Operational Rubriks** (WOW-ZIGLAR-LUND, CASH-IS-OXYGEN, etc.) | NO (0 mentions) | PRODUCT-ARCHITECTURE-TIERS.md, AMPLIFIED_OPERATING_SYSTEM_SPEC.md |
| **Three-apps design** (Customer/Client/Ewan) | NO (1 mention) | THREE-APPS-DESIGN.md |
| **Screen specifications & wireframes** | NO | SCREEN-SPECIFICATIONS.md (55KB) |
| **UI component reference** | NO | UI-COMPONENT-REFERENCE.md (33KB) |
| **Voice-first interface detailed spec** | Partial (11 mentions, basic level) | AMPLIFIED_OPERATING_SYSTEM_SPEC.md §6 |
| **Staff adoption 3-stage journey** | NO | AMPLIFIED_OPERATING_SYSTEM_SPEC.md §7 |
| **ESP32 thin client specs** | NO (0 mentions) | AMPLIFIED_OPERATING_SYSTEM_SPEC.md §10 |
| **Hardware manufacturing** (PETG, 3D printing, costs) | NO | AMPLIFIED_OPERATING_SYSTEM_SPEC.md §11 |
| **Sovereign OS concept** | Barely (4 mentions) | SOVEREIGN-OS.md |
| **Parallel build strategy** (6 workstreams) | NO | PARALLEL-BUILD-STRATEGY.md |
| **Pricing tiers** (£0/£99/£295/£595/£1,595/£2,995) | NO (0 mentions) | AMPLIFIED_OPERATING_SYSTEM_SPEC.md §3 |
| **Life Goals framework** | NO (0 mentions) | AMPLIFIED_OPERATING_SYSTEM_SPEC.md §1, PRODUCT-ARCHITECTURE-TIERS.md |
| **FalkorDB / Graphiti** | NO (0 mentions) | AMPLIFIED_OPERATING_SYSTEM_SPEC.md §4, §20 |
| **PWA over native decision** | NO | AMPLIFIED_OPERATING_SYSTEM_SPEC.md §12 |
| **Pre-Cove translator** | NO | AMPLIFIED_OPERATING_SYSTEM_SPEC.md §6, §16 |
| **DocBench data extraction engine** | NO | AMPLIFIED_OPERATING_SYSTEM_SPEC.md §4 |
| **Libertarian paternalism principle** | NO | AMPLIFIED_OPERATING_SYSTEM_SPEC.md §1 |
| **Content creation engine** | NO | AMPLIFIED_OPERATING_SYSTEM_SPEC.md §17 |
| **ISO 9001 process documentation** | NO (0 mentions) | AMPLIFIED_OPERATING_SYSTEM_SPEC.md §14 |
| **PDCA nightly improvement cycle** | NO | AMPLIFIED_OPERATING_SYSTEM_SPEC.md §15 |
| **Four-word identifier system** | NO | AMPLIFIED_OPERATING_SYSTEM_SPEC.md §13, §16 |
| **"Don't worry, nothing to learn" onboarding** | NO | AMPLIFIED_OPERATING_SYSTEM_SPEC.md §7 |
| **MCPipe / MCP server architecture** | NO | PRODUCT-ARCHITECTURE-TIERS.md |
| **Financial Autopsy MVP** (Xero/Sage hook) | NO | PRODUCT-ARCHITECTURE-TIERS.md |
| **Vertical specialisations** (Plumbers, HGV, Restaurants, Shops) | NO | PRODUCT-ARCHITECTURE-TIERS.md |
| **Weather-aware scheduling** | NO | PRODUCT-ARCHITECTURE-TIERS.md |
| **Amplified Partners name** | Barely (1 mention) | All March 2026 docs |

### OUTDATED CONTENT

| Issue | In project-latest.md | Current Reality |
|-------|---------------------|-----------------|
| **Company name** | "Covered AI" (31 mentions) | "Amplified Partners" (rebranded) |
| **Database stack** | Qdrant (165 mentions) + Neo4j | FalkorDB (replaced Neo4j) + Qdrant + PostgreSQL |
| **Infrastructure** | Railway deployment mentioned | Beast (Hetzner AX162-R) is the infrastructure |
| **Tech focus** | Heavy Kilo Code / extraction focus | Shifted to Cove code factory + MCP + agent architecture |
| **Approach** | Bible extraction from Mac | Structured vault + systematic process documentation |

### RECOMMENDATION FOR BUILDING AI

**project-latest.md needs a major overhaul.** It's a January 2026 snapshot of early thinking. The product has evolved massively since then. Specifically:

1. **Remove duplicates** — Cut 12+ duplicate documents, reduce from 409KB to ~250KB
2. **Update naming** — Replace all "Covered AI" references with "Amplified Partners"
3. **Add the March 2026 specs** — The following documents should be added or referenced:
   - AMPLIFIED_OPERATING_SYSTEM_SPEC.md (the single source of truth)
   - PRODUCT-ARCHITECTURE-TIERS.md
   - THREE-APPS-DESIGN.md
   - SCREEN-SPECIFICATIONS.md
   - UI-COMPONENT-REFERENCE.md
4. **Add missing concepts** — Life goals, 7 rubriks, staff adoption journey, pricing tiers, FalkorDB, voice-first details
5. **Update tech stack** — FalkorDB over Neo4j, Beast over Railway, Cove over Kilo Code

---

## DOCUMENT 2: VAULT STRUCTURE MAP

### For the building AI — here's what's in every vault folder

#### _inbox (Main inbox — ~250 files)
The primary dumping ground. Contains:
- **Python code files** (~80+): agents, brain services, CRM, voice integration, webhooks, Telegram gates, semantic cache, etc.
- **Strategy/spec docs** (~60+): AGENTS v1-v4, SOUL v1-v4, PHILOSOPHY docs, product specs for HGV/trades, deployment blockers, etc.
- **Session boards** (SHARED-BOARD v1 through v30): 30 sequential session tracking documents
- **Marketing docs**: Landing page strategies, SEO implementations, LinkedIn posts, content calendars
- **Voice platform docs**: VAPI vs Retell research, voice CRM specs, voice-first architecture
- **Recent sessions** (recent-sessions v1 through v31): Session summaries
- **Registered letters** (v1-v3): Legal template documents

**Flag:** This folder has massive version proliferation. AGENTS has 4 versions. SOUL has 4. Many files have -v2, -v3, -v4 variants. Building AI should use the highest version number of each.

#### _inbox-voice (~500+ voice transcripts)
All from 20-23 February 2026. Raw voice-to-text transcriptions from Ewan's sessions. These contain Ewan's thinking, decisions, and instructions captured via the voice interface prototype.

**Flag:** These are primary source material for Ewan's decisions. Building AI should ingest and summarise these — they likely contain decisions and context not written anywhere else.

#### _inbox-work (needs separate listing — not enumerated yet)

#### _staging (Structured, categorised content)
The organised layer. 11 subdirectories:
- **01-executive/** — Empty except .DS_Store
- **02-strategy/** — 8 strategy docs + subdirs (plans, docs-plans)
- **03-sales-marketing/** — 13 marketing docs + subdirs (covered-marketing, lead-engine)
- **05-technology/** — 50+ tech docs + subdirs (agentic-workflow, studio-dev, terminal-mcp)
- **07-finance/** — 2 docs (£250K automation model, execution checklist)
- **08-product/** — 14 product docs + subdirs (interior-design, invoice-service, personal-assistant)
- **09-research/** — 1 subdir (lukestays)
- **11-templates-sops/** — 2 SOPs + subdirs (byker-skills, kilocode-rules)
- **12-archive-raw/** — 200+ docs: massive collection of Perplexity threads, research, old specs, brand docs, ALL the Covered AI-era screen specs, THREE-APPS-DESIGN, and build instructions

**Flag:** _staging/12-archive-raw contains the Covered AI-era screen specifications (11-UI-COMPONENT-REFERENCE.md, 12-SCREEN-SPECIFICATIONS.md, THREE-APPS-DESIGN.md) which have already been pulled into workspace. Also contains 150+ Perplexity thread exports — potential gold mine of decisions and reasoning.

#### research (~140 files)
Date-prefixed research documents from late February 2026. Includes:
- Session research, AI reviews, Dave/Sam agent specs
- PUDDING technique extractions
- Voice AI platform comparisons
- Security research reports
- 60+ four-word-named files (agent session outputs from the Room)

**Flag:** The four-word-named files (e.g., "binary-humming-tide", "cozy-hopping-tower") are agent session outputs. Each one is a research session result. These need indexing.

#### work/ (Active working docs)
- campaigns/ — Marketing campaign files
- claude-writing/ — Claude-authored content
- pudding/ — PUDDING technique sessions
- rubric/ — Rubrik scoring documents
- sessions/ — Session records
- Plus: amplified-partners-master.md, Gemini context, Johnny status

---

## DOCUMENT 3: DEFRICTION ESTIMATES

### Summary
32 core business processes mapped. Estimates below are per typical SMB client (5-15 employees).

### Category A: Complete Defriction (14 processes)
Agent handles end-to-end. Human only involved for exceptions.

| Process | Manual Time/week | With Agent | Time Saved/week | Annual Hours Saved |
|---------|-----------------|------------|-----------------|-------------------|
| Invoice Processing | 3 hrs | 0.25 hrs | 2.75 hrs | 143 hrs |
| Bank Reconciliation | 2 hrs | 0.15 hrs | 1.85 hrs | 96 hrs |
| Expense Management | 1.5 hrs | 0.1 hrs | 1.4 hrs | 73 hrs |
| Payroll Processing | 2 hrs | 0.2 hrs | 1.8 hrs | 94 hrs |
| VAT/Tax Returns | 1 hr (avg) | 0.1 hrs | 0.9 hrs | 47 hrs |
| Report Generation | 2 hrs | 0.1 hrs | 1.9 hrs | 99 hrs |
| Data Entry & Migration | 4 hrs | 0.3 hrs | 3.7 hrs | 192 hrs |
| Scheduling & Calendar | 3 hrs | 0.2 hrs | 2.8 hrs | 146 hrs |
| Email Triage & Routing | 5 hrs | 0.5 hrs | 4.5 hrs | 234 hrs |
| Inventory Tracking | 2 hrs | 0.15 hrs | 1.85 hrs | 96 hrs |
| Document Filing | 2 hrs | 0.1 hrs | 1.9 hrs | 99 hrs |
| Compliance Monitoring | 1.5 hrs | 0.15 hrs | 1.35 hrs | 70 hrs |
| IT Service Tickets | 2 hrs | 0.3 hrs | 1.7 hrs | 88 hrs |
| Meeting Notes & Actions | 2 hrs | 0.1 hrs | 1.9 hrs | 99 hrs |
| **SUBTOTAL** | **33 hrs/wk** | **2.7 hrs/wk** | **30.3 hrs/wk** | **1,576 hrs/yr** |

### Category B: Partial Defriction (10 processes)
Human leads, agent assists. Roughly 40-60% time reduction.

| Process | Manual Time/week | With Agent | Time Saved/week | Annual Hours Saved |
|---------|-----------------|------------|-----------------|-------------------|
| Sales Conversations | 6 hrs | 3 hrs | 3 hrs | 156 hrs |
| Hiring Decisions | 2 hrs (avg) | 1 hr | 1 hr | 52 hrs |
| Client Relationship Mgmt | 4 hrs | 2 hrs | 2 hrs | 104 hrs |
| Strategic Planning | 2 hrs | 1.2 hrs | 0.8 hrs | 42 hrs |
| Staff Performance Reviews | 1 hr (avg) | 0.5 hrs | 0.5 hrs | 26 hrs |
| Conflict Resolution | 0.5 hrs (avg) | 0.3 hrs | 0.2 hrs | 10 hrs |
| Creative Direction | 2 hrs | 1 hr | 1 hr | 52 hrs |
| Negotiation | 1.5 hrs | 0.8 hrs | 0.7 hrs | 36 hrs |
| Quality Judgement Calls | 1.5 hrs | 0.8 hrs | 0.7 hrs | 36 hrs |
| Business Development | 3 hrs | 1.5 hrs | 1.5 hrs | 78 hrs |
| **SUBTOTAL** | **23.5 hrs/wk** | **12.1 hrs/wk** | **11.4 hrs/wk** | **592 hrs/yr** |

### Category C: Grey Zone — Moving to Agent (8 processes)
Currently transitioning. Estimate 50-70% defriction within 12 months.

| Process | Manual Time/week | With Agent (now) | With Agent (12mo) | Annual Hrs Saved (now) | Annual Hrs Saved (12mo) |
|---------|-----------------|-----------------|------------------|----------------------|------------------------|
| Customer Service (Tier 1) | 8 hrs | 3 hrs | 1.5 hrs | 260 hrs | 338 hrs |
| Content Creation | 4 hrs | 2 hrs | 1 hr | 104 hrs | 156 hrs |
| Social Media Management | 3 hrs | 1.5 hrs | 0.8 hrs | 78 hrs | 114 hrs |
| Basic Bookkeeping | 3 hrs | 1 hr | 0.3 hrs | 104 hrs | 140 hrs |
| Procurement & Supplier | 2 hrs | 1.2 hrs | 0.7 hrs | 42 hrs | 68 hrs |
| Training & Onboarding | 2 hrs | 1 hr | 0.5 hrs | 52 hrs | 78 hrs |
| Marketing Campaigns | 3 hrs | 1.5 hrs | 0.8 hrs | 78 hrs | 114 hrs |
| Project Coordination | 3 hrs | 1.8 hrs | 1 hrs | 62 hrs | 104 hrs |
| **SUBTOTAL** | **28 hrs/wk** | **13 hrs/wk** | **6.6 hrs/wk** | **780 hrs/yr** | **1,112 hrs/yr** |

### TOTAL DEFRICTION SUMMARY

| Metric | Now | In 12 Months |
|--------|-----|--------------|
| Total manual hours/week (per client) | 84.5 hrs | 84.5 hrs |
| Hours after defriction/week | 27.8 hrs | 21.4 hrs |
| **Hours saved/week** | **56.7 hrs** | **63.1 hrs** |
| **Hours saved/year** | **2,948 hrs** | **3,280 hrs** |
| Percentage defriction | 67% | 75% |

**What that means in plain English:**
- A typical 10-person SMB doing 84.5 hours/week of operational work gets 57 hours back. That's 1.4 full-time employees' worth of capacity freed up.
- In 12 months, that rises to 63 hours — 1.6 full-time employees.
- Those people aren't sacked. They're freed up for higher-value work: customer relationships, growth, the things they actually enjoy.

---

## DOCUMENT 4: FINANCIAL FORECASTS

### Money Saved Per Client (annual)

Using UK average SMB hourly cost of £22/hr (including employer NI, pension, overhead):

| Category | Hours Saved/yr | Value at £22/hr |
|----------|---------------|----------------|
| Complete defriction (14 processes) | 1,576 hrs | £34,672 |
| Partial defriction (10 processes) | 592 hrs | £13,024 |
| Grey zone (8 processes, now) | 780 hrs | £17,160 |
| **TOTAL (now)** | **2,948 hrs** | **£64,856** |
| **TOTAL (12 months)** | **3,280 hrs** | **£72,160** |

### ROI By Pricing Tier

| Tier | Monthly Cost | Annual Cost | Value Delivered | ROI Multiple | Payback |
|------|-------------|-------------|-----------------|-------------|---------|
| FREE (3 months) | £0 | £0 | £16,214* | ∞ | Instant |
| Solo (£99) | £99 | £1,188 | £25,942** | 21.8x | 6 days |
| Small Business Phone (£295) | £295 | £3,540 | £38,914** | 11.0x | 10 days |
| Small Business IT (£595) | £595 | £7,140 | £64,856 | 9.1x | 40 days |
| Medium (£1,595) | £1,595 | £19,140 | £64,856 | 3.4x | 108 days |
| Large (£2,995) | £2,995 | £35,940 | £97,284*** | 2.7x | 135 days |

\* FREE tier gets Category A processes only (subset)
\** Solo and Phone tiers get partial process coverage
\*** Large tier estimate assumes 1.5x the standard client process volume

### Revenue Projections (Subscriber Growth Scenarios)

#### Conservative Scenario (Year 1)

| Month | FREE | Solo | SB Phone | SB IT | Medium | Large | MRR |
|-------|------|------|----------|-------|--------|-------|-----|
| 1 | 20 | 5 | 2 | 1 | 0 | 0 | £1,685 |
| 3 | 50 | 15 | 5 | 3 | 1 | 0 | £5,950 |
| 6 | 80 | 30 | 12 | 6 | 2 | 1 | £14,445 |
| 9 | 100 | 45 | 20 | 10 | 4 | 2 | £26,265 |
| 12 | 120 | 60 | 30 | 15 | 6 | 3 | £39,425 |

**Year 1 Conservative: ~£39K MRR by month 12 = £473K ARR run rate**

Assumptions:
- FREE converts to paid at 15% after 3 months
- Churn: 3% monthly for Solo, 2% for others
- Average client stays 18 months
- North East England initial market, expanding UK-wide

#### Moderate Scenario (Year 1)

| Month | FREE | Solo | SB Phone | SB IT | Medium | Large | MRR |
|-------|------|------|----------|-------|--------|-------|-----|
| 1 | 40 | 10 | 4 | 2 | 0 | 0 | £3,370 |
| 3 | 100 | 30 | 10 | 6 | 2 | 1 | £12,855 |
| 6 | 200 | 70 | 25 | 12 | 5 | 2 | £30,805 |
| 9 | 300 | 120 | 45 | 20 | 8 | 4 | £56,420 |
| 12 | 400 | 180 | 70 | 35 | 12 | 6 | £85,510 |

**Year 1 Moderate: ~£85K MRR by month 12 = £1.03M ARR run rate**

#### Aggressive Scenario (Year 1 — viral Financial Autopsy hook works)

| Month | FREE | Solo | SB Phone | SB IT | Medium | Large | MRR |
|-------|------|------|----------|-------|--------|-------|-----|
| 3 | 500 | 80 | 30 | 15 | 5 | 2 | £31,420 |
| 6 | 1,500 | 250 | 80 | 35 | 12 | 5 | £78,115 |
| 12 | 5,000 | 800 | 250 | 100 | 30 | 15 | £237,075 |

**Year 1 Aggressive: ~£237K MRR by month 12 = £2.8M ARR run rate**

### Cost Structure (Per Client, Monthly)

| Cost Item | Estimate |
|-----------|---------|
| Beast compute (amortised per client) | £2-8 |
| LLM API costs (LiteLLM routing, Ollama local first) | £3-15 |
| Bluetooth mic (one-time, amortised) | £1-2 |
| Storage & backup (Hetzner) | £0.50-2 |
| Support overhead (amortised) | £5-20 |
| **Total per client** | **£11.50-47** |

At £99/month Solo tier, gross margin is ~52-88%.
At £595/month SB IT tier, gross margin is ~92-98%.

### Break-Even Analysis

| Scenario | Monthly Fixed Costs* | Clients Needed (avg £350 ARPU) | Timeline |
|----------|---------------------|-------------------------------|----------|
| Ewan only | £3,000 | 9 paying clients | Month 2-3 |
| + 1 tech hire | £7,000 | 20 paying clients | Month 4-6 |
| + support person | £10,000 | 29 paying clients | Month 6-9 |
| Full team (5) | £20,000 | 58 paying clients | Month 9-12 |

\* Beast server is already paid for. These are people costs.

---

## DOCUMENT 5: FLAGS FOR THE BUILDING AI

### Flag 1: project-latest.md Is Outdated
- It's a January 2026 snapshot. The product has evolved massively.
- Still references "Covered AI" (31 times) instead of "Amplified Partners"
- Missing: 7 rubriks, 3-tier architecture, 3-app design, life goals, pricing tiers, FalkorDB, ESP32, staff adoption journey
- Contains 40% duplicate content
- **Action needed:** Rebuild project-latest.md incorporating AMPLIFIED_OPERATING_SYSTEM_SPEC.md as the backbone, add the March 2026 specs, remove duplicates

### Flag 2: The 4 Key Documents
Per Ewan's request, these are the documents the building AI needs:
1. **Master Document**: AMPLIFIED_OPERATING_SYSTEM_SPEC.md — the single source of truth (March 14, 2026)
2. **Build JSON**: AMPLIFIED_OPERATING_SYSTEM_SPEC.json — structured build specification
3. **Content Creation Document**: Content engine spec in AMPLIFIED_OPERATING_SYSTEM_SPEC.md §17 + marketing philosophy §18
4. **UI Refinement Format**: THREE-APPS-DESIGN.md + SCREEN-SPECIFICATIONS.md + UI-COMPONENT-REFERENCE.md

### Flag 3: Vault Has Unmined Voice Transcripts
500+ voice transcripts in _inbox-voice from 20-23 Feb 2026. These almost certainly contain decisions, preferences, and context that aren't written anywhere else. Building AI should ingest these.

### Flag 4: Version Proliferation in _inbox
Many files have v2, v3, v4 variants. AGENTS has 4 versions. SOUL has 4 versions. SHARED-BOARD has 30 versions. Building AI should only use the latest version of each.

### Flag 5: _staging/12-archive-raw Is a Gold Mine
200+ documents including all the Covered AI-era specs, Perplexity thread exports (150+), build instructions, screen specs. This is the archaeological record of every decision made. Building AI should index this but treat it as historical — March 2026 specs take precedence.

### Flag 6: Process Coverage May Be Larger Than 32
The 32 processes mapped in the audit are core operational processes. When you add:
- Industry-specific processes (plumbing: gas certs, emergency scheduling; HGV: compliance; restaurants: food safety)
- Customer-facing processes (booking, payment, reviews)
- Growth processes (lead gen, content, social)

Total addressable process count is likely **80-120 processes per vertical**. Building AI should map these per vertical.

### Flag 7: The "We Don't Sack People" Promise Needs System Enforcement
The defriction estimates show 1.4-1.6 FTE equivalent freed up per client. The system MUST have built-in guardrails that:
- Never suggest redundancies
- Frame all savings as "capacity freed for higher-value work"
- Track what freed-up time is being used for
- Report on skills development and role enrichment, not headcount reduction

### Flag 8: Financial Autopsy Is The Viral Hook
PRODUCT-ARCHITECTURE-TIERS.md identifies the Financial Autopsy (Xero/Sage API → 5 years of data → CASH-IS-OXYGEN rubrik → report) as the Phase 1 MVP. This is the door opener. Building AI should prioritise this.

### Flag 9: Pricing Psychology
At £595/month delivering £64,856/year in value (9.1x ROI), the price is almost absurdly cheap. The "payback in 40 days" story is extremely compelling for sales conversations. Building AI should surface these ROI numbers prominently in the product.

### Flag 10: The Kaizen Dashboard Design Principles
From this session's work, the building AI should know:
- Data presentation must be framed around **personal goals** (4-day week, time with kids, profit margin)
- Language at 14-year-old reading level
- Structure: Goal → Progress → Next Action
- Don't tell people what to feel — let data speak
- Multiple goals per person (3-15 goals)
- Show time saved as universal currency
- External benchmarks: anonymous aggregates only
- No gamification (no leaderboards, badges, points)
- RAS principle: people's brains filter for what matters to THEM

---

## RADICAL ATTRIBUTION

```yaml
attribution:
  human:
    - name: "Ewan Bramley"
      role: "originator"
      contribution: "All business vision, product decisions, vault content, voice transcripts, design principles, pricing"
  ai_contributors:
    - name: "Perplexity Computer"
      provider: "Perplexity AI"
      role: "auditor, analyst"
      contribution: "Vault mapping, gap analysis, defriction estimates, financial modelling, flag compilation"
  research_sources:
    - "BCG: AI agents cut low-value work 25-40%"
    - "Gartner: by 2029, AI resolves 80% of customer issues autonomously"
    - "Lux Research: automate the boring, not the rewarding"
    - "ScienceDirect: augmentation boosts satisfaction; substitution triggers identity threat"
    - "UK ONS: average SMB hourly cost data"
  fact_percentage: 85
  confidence_band: "high (structure/gaps), moderate (financial projections)"
```

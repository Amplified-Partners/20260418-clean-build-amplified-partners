---
title: "Pass 2 Skills Vault"
id: "pass-2-skills-vault"
version: 1
created: 2026-04-25
last_validated: 2026-04-25
type: document
topic_type: reference
status: imported
source_file: "pass2-skills-vault.md"
signed_by: "Devon, 2026-04-25, devin-992682c244cf444f91e0a516498afbfd"
---

# PASS 2: Skills, Vault, and Task Management
## Amplified Partners Knowledge Extraction
**Run date:** 2026-03-27  
**Source:** GitHub (vault, gatekeeper, cove repos), Todoist (todoist__pipedream connector), direct GitHub API reads  

---

## SECTION 1: PERPLEXITY CUSTOM SKILLS

### Status
No dedicated "Perplexity custom skills" with discrete IDs were found in memory or workspace. The concept of "skills" in Ewan's system refers primarily to **KiloCode rule files** (in `.kilocode/rules/`) and **Byker Business Help skills** (in the vault's `_staging/11-templates-sops/byker-skills/`), NOT Perplexity-native skills with IDs.

The vault does contain numerous Perplexity-exported research threads (prefixed `perplexity-*` in `_staging/05-technology/`), but these are saved research outputs — not skills/agents Ewan built inside Perplexity.

### OpenClaw Skills (most relevant "custom skills" system)
Source: `_inbox/openclaw-skills-security-research-report.md` (2026-02-21)

OpenClaw is the AI agent framework Ewan uses. Skills are categorised as:

| Category | Verified Safe Skills | Status |
|----------|---------------------|--------|
| Personal Organisation | `gog` (Google Workspace), `calendar`, `email`, `obsidian`, `notion`, `reminders` | ✅ Bundled |
| Research & Content | `summarize`, `gemini`, `web-research`, `github` | ✅ Bundled |
| Social Media | `postiz`, `postfast`, `post-bridge`, `mixpost`, `social-content` | ✅ VirusTotal Scanned |
| CRM/Business | Various third-party | ⚠️ Unverified — use native tools instead |

**Security Note (ClawHavoc Campaign active as of 2026-02-21):**
- 824+ malicious skills documented (~41.7% of all skills compromised)
- Primary threat: Atomic Stealer (AMOS) malware targeting macOS
- AVOID skills from user `hightower6eu` (314+ malicious skills)
- Recommendation: Only use officially bundled or VirusTotal-scanned skills

### KiloCode Skills (`.kilocode/rules/` directory)
Source: `_staging/02-strategy/docs-plans/current-kilocode-skills.md`

Active rule files in Ewan's KiloCode workspace:

| # | Skill File | Purpose |
|---|-----------|---------|
| 1 | `api-config.md` | API provider settings — Haiku (simple), Sonnet (balanced), Opus (complex), MiniMax (budget) |
| 2 | `global-rules.md` | Coding principles, communication style, safety practices |
| 3 | `intent-verification-handoff.md` | Capture intentions, identify incomplete tasks, handoff to Orchestrator |
| 4 | `prebuilt-solutions.md` | Recommend existing libraries before building custom |
| 5 | `01-swift-style.md` | Swift naming conventions, type safety |
| 6 | `02-swift-model-structure.md` | Swift data models |
| 7 | `03-swift-viewmodel-rules.md` | Swift ViewModels |
| 8 | `agent-workflows.md` | Common AI workflows (Railway error analysis, perf tuning, git refactor) |
| 9 | `profiles.md` | Optimised settings — Local-Dev-Coding, Cloud-Deep-Refactor, Railway-Ops-Agent, Docs-Research-Agent |
| 10 | `project-system-prompt.md` | Architecture: Next.js, FastAPI, PostgreSQL, Redis |

**Planned (not yet implemented):** TypeScript/Next.js structure, Python/FastAPI structure, Swift project structure, GitHub best practices, .gitignore templates, Integration guide

### Byker Business Help Skills Library
Source: `_staging/11-templates-sops/byker-skills/README.md` (v1.0.0, January 2025)

| Skill | Category | Purpose |
|-------|----------|---------|
| `byker-client-diagnostic` | Client Analysis | AI-powered 48-hour business analysis, profit leak detection |
| `byker-client-onboarding` | Client Analysis | Frictionless client intake, OAuth connections |
| `byker-sop-builder` | Client Analysis | Process documentation, training materials |
| `byker-content-factory` | Marketing | Educational content, social posts |
| `byker-lead-magnet` | Marketing | Calculators, assessments, guides, mini-courses |
| `byker-outbound-automation` | Marketing | LinkedIn, email, lead scoring |
| `byker-video-avatar` | Video | HeyGen, D-ID, ElevenLabs integration |
| `byker-helpdesk-avatar` | Video | 24/7 AI customer support |
| `byker-retention-engine` | Engagement | Churn prediction, touchpoint automation, NPS |
| `byker-gamification` | Engagement | Badges, leaderboards, behavioural psychology |
| `byker-principles-coach` | Intelligence | Ray Dalio decision framework |
| `byker-kilo-orchestrator` | Intelligence | 4-instance Kilo management, parallel workflows |

**Revenue Model Supported:**

| Tier | Price | Skills Used |
|------|-------|-------------|
| Tier 1 Quick Win | £2,500 one-time | Diagnostic, Lead Magnet |
| Tier 2 Transformation | £7,500 12-week | + Onboarding, SOP, Video |
| Tier 3 Partnership | £1,200/month | All skills, 52-week journey |

### Claude Prompt Engineering Frameworks (Meta-Skill)
Source: `_staging/05-technology/claude-meta-skill-prompting-v1.md`

| Framework | Name | Use Case |
|-----------|------|---------|
| CACE | CLAUDE | Strategic thinking, analysis, persuasive writing |
| SPEED | KILO | Production code, features, automation |
| VIBE | NANO | Professional visuals, marketing assets |

---

## SECTION 2: GITHUB REPOSITORIES

Source: `gh repo list --json name,description --limit 50` (2026-03-27)

| Repo | Description |
|------|-------------|
| `ai-learning-journey-code-repository` | Technical implementations, scripts, and dev work from AI learning journey and business automation |
| `vault` | Amplified Partners knowledge vault — structured notes, decisions, documentation |
| `cove` | Cove Code Factory — Temporal-based build pipeline, agent loop, MCP bridge, Layer 0 laws (**EMPTY — no commits yet**) |
| `crm` | AI-powered CRM for UK tradespeople — Intelligence System with Claude |
| `anthropic-token-proxy` | Local reverse proxy for Anthropic API — prompt caching, native context compaction, semantic caching, zero code changes |
| `gatekeeper` | Conversation-to-Action Gatekeeper Agent — quality control gate for all content entering the knowledge system |
| `byker-production` | *(no description)* |
| `smb-ai-friction-consultancy` | SMB AI Friction Reduction Consultancy — Local Ollama/Qwen agentic system, hierarchical agents with blinkers, guarded repos, nightly data sync |
| `beautifulgolden` | SMBFrictionreducer |
| `docs` | *(no description)* |
| `librarian-api` | *(no description)* |
| `voice-ai` | *(no description)* |
| `covered-ai-v2` | 27_11_25 |

**Total repos:** 13

### Key Repo Details

**`gatekeeper`** — Core components:
- `gatekeeper.py` — Main agent with Claude API integration
- `quality_check.py` — Validation against core principles
- `obsidian_writer.py` — Markdown file output
- `linear_client.py` — Creates Linear issues from conversation action items
- `github_sync.py` — GitHub synchronisation
- `qdrant_manager.py` — Vector database management
- `reflection.py` — Self-reflection
- `taxonomy.py` — Content categorisation
- `classifier.py` — Content classification
- `setup_linear.py` — Linear workspace setup

**Linear Team ID (from gatekeeper):** `7f950a2a-1643-49cc-a1b0-8d4393798c7c`

**`covered-ai-v2`** — Full SaaS stack (CLAUDE.md dated 2025-11-27):
- FastAPI + Python 3.11 backend
- Next.js 14 + TypeScript frontend
- PostgreSQL on Railway
- Prisma ORM
- Trigger.dev v4.1.2 for jobs
- Vapi.ai for voice AI
- Twilio for telephony
- Resend for email
- HeyGen for personalised AI video
- Railway hosting
- Claude ↔ Services via MCP

---

## SECTION 3: VAULT CONTENTS (GITHUB: `vault` repo)

### Top-Level Structure
Source: `gh api repos/{user}/vault/git/trees/HEAD`

```
vault/
├── _inbox/                  # Auto-synced from OpenClaw workspace
├── _inbox-uncategorised/
├── _inbox-voice/
├── _inbox-work/             # Work-related inbox items
├── _staging/                # Structured knowledge (00-12 numbered dirs)
│   ├── 00-master-index.md   # 2,989 total files indexed (created 2026-01-20)
│   ├── 00-principles-pudding.md
│   ├── 00-rubric-multiplier-v1.md / v2.md
│   ├── 00-scoring-agent-prompt-v1.md
│   ├── 00-scoring-template-v1.md
│   ├── 01-executive/        (DS_Store only — empty)
│   ├── 02-strategy/         (docs-plans/, plans/)
│   ├── 03-sales-marketing/  (covered-marketing/, lead-engine/)
│   ├── 05-technology/       (agentic-workflow/, studio-dev/, terminal-mcp/)
│   ├── 07-finance/
│   ├── 08-product/          (interior-design/, invoice-service/, personal-assistant/)
│   ├── 09-research/         (lukestays/)
│   ├── 11-templates-sops/   (byker-skills/, kilocode-rules/)
│   └── 12-archive-raw/      (claude-exports/, today-mirror/)
├── _system/                 # RUBRIC-REPLACE-OR-FIX.md, hetzner-credentials.md
├── eli/                     # pipeline/
├── imported-business-docs/  (amplified-crm-docs/, gemini-brain/, openclaw-workspace/)
├── infra-ai-stack/
├── knowledge-qdrant/        (venv/ + Python packages)
├── projects/                (case-studies/, frameworks/, personas/, research/, roadmaps/)
├── research/
├── scripts/
├── the-room/
├── therapy-suite/
├── transcripts/
├── work/                    (campaigns/, claude-writing/, pudding/, rubric/, sessions/)
│   ├── amplified-partners-master.md
│   ├── amplified-partners-overview-feb-2026.md
│   └── ...
├── 2026-02-08.md
├── Quantitative-Validation-LBD-Architectures-2026.md
├── bake.py / bake_fixed.py  (pipeline scripts)
└── README.md                (just "# Pudding Vault")
```

### Master File Index (00-master-index.md)
Created 2026-01-20 | Total: **2,989 files**

| # | Department | Files | Content |
|---|------------|-------|---------|
| 01 | Executive | 10 | Vision, bible, master strategy |
| 02 | Strategy | 46 | Roadmaps, plans, positioning |
| 03 | Sales & Marketing | 140 | Brand, websites, HTML, CSS, designs |
| 04 | Operations | 43 | 31 expert principles + systems |
| 05 | Technology | 118 | AI stack, Qdrant, Terraform, infra |
| 06 | HR & Culture | 2 | Coaching personas |
| 07 | Finance | 2 | £250k model |
| 08 | Product | 28 | Service guides, book system |
| 09 | Research | 10 | Speech-act theory, UX research |
| 10 | Legal & Personal | 2 | Consent order, attestation |
| 11 | Templates & SOPs | 35 | Kilo prompts, skills, rules |
| 12 | Archive/Raw | 723 | All MD, TXT, logs, exports |
| 13 | Code & Scripts | 1,558 | Python, JS, TS, TSX, Shell, Swift |
| 14 | Data & Config | 147 | JSON, JSONL, YAML, SQL, TOML, CSV |
| 15 | Assets & Media | 78 | PDF, PNG, JPG, SVG, MP4, WAV, DOCX |
| 16 | Archives/Exports | 39 | ZIP files (backups, exports) |
| 17 | Config/Secrets | 6 | .env files |

**Sources swept:** `~/vault`, `~/Downloads`, `~/Documents`, `~/Desktop`, Google Drive

### Key Documents Found

#### SOUL.md (multiple versions — `_inbox/`)
The core identity document for all AI partners in Amplified Partners. Key principles:
- **Blinkers Without Ceilings** — Clear on WHAT, no ceiling on HOW WELL
- **Radical Honesty** — Never lie, spin, or soften. Truth is always cheaper.
- **Business Gets No Grace** — Hold to standard or shut it down. Applies equally to Ewan, Sam, Claude Code, Grok.
- **Radical Transparency** — Document everything; DONE or UNFINISHED with notes.
- **Win-Win Only** — If it only benefits one side, it's wrong.
- **Ideas Meritocracy** — Best idea wins regardless of who had it.
- **Freedom Through Reversibility** (v4) — Permission given once is standing. Act freely — document everything, ensure it can be undone.
- **Universal Law (v4):** Incomplete is fine. Undocumented is not. States must be DONE or UNFINISHED.

**Versions in vault:**
- `_inbox/SOUL.md` — v1 (synced 2026-02-21 15:50)
- `_inbox/SOUL-v2.md`
- `_inbox/SOUL-v3.md`
- `_inbox/SOUL-v4.md` — Most evolved version (synced 2026-02-21 17:35) — adds Sam, Eli, Sentinel, and the Reversibility principle
- `imported-business-docs/openclaw-workspace/SOUL.md` — Canonical OpenClaw copy

#### CLAUDE.md (`_staging/12-archive-raw/CLAUDE.md`)
Project context file for **Covered AI v2** (dated 2025-11-27):
- AI phone answering for UK service businesses (plumbers, vets, salons, dentists)
- AI assistant named "Gemma" (Northern British accent)
- 24/7 call answering, emergency triage, lead capture, 12-touch nurture sequence
- Target: £43M ARR by Year 3 | Price: £297-497/month

#### CLAUDE-GENERIC.md (`therapy-suite/CLAUDE-GENERIC.md`)
Generic agent identity template for Amplified Partners deployments. Three-layer structure:
- **Layer 1 — The Truth** (constitutional, permanent): Honest, transparent, acknowledge contribution, win-win, helpful
- **Layer 2 — Commitment**: Help, you are business, no ego, measurement is mutual, escalate don't swallow
- **Layer 3 — Mission** (not retrieved — file truncated)

#### BATON-PASS-PROTOCOL
No file with this exact name found in any repo. The concept is referenced contextually — the gatekeeper system and CLAUDE-CODE-HANDOFF.md serve this function.

**Related documents found:**
- `_staging/12-archive-raw/CLAUDE-CODE-HANDOFF.md`
- `_staging/12-archive-raw/15-CLAUDE-CODE-BUILD-INSTRUCTIONS.md`

#### Other Key Vault Documents
- `work/amplified-partners-master.md` — Complete vision document (Feb 2026); Ewan's full founder story, mission, partnership philosophy
- `work/amplified-partners-overview-feb-2026.md` — Feb 2026 overview
- `_staging/05-technology/ATOMISER_SPEC.md` — LLM Atomiser spec: transforms labelled docs into 20-60 word self-contained knowledge atoms for RAG
- `_staging/12-archive-raw/claude-exports/250k-aggressive-model.md` — £250k revenue model
- `_staging/12-archive-raw/claude-exports/COMPREHENSIVE_BUSINESS_ASSET_AUDIT.md`

---

## SECTION 4: LINEAR COV ISSUES (Cove Code Factory)

### Findings
The **`cove` GitHub repository is completely empty** (no commits, HTTP 409 returned). The Cove Code Factory project (`cove`) was created with the description "Temporal-based build pipeline, agent loop, MCP bridge, Layer 0 laws" but no code has been committed.

**No COV-series Linear issues** were directly retrievable — Linear API access requires credentials not available in this session. However, the gatekeeper's `setup_linear.py` reveals the Linear workspace structure:

**Linear Team ID:** `7f950a2a-1643-49cc-a1b0-8d4393798c7c`

**4 Core Linear Projects created (via setup_linear.py):**
1. **Amplified** — Core consultancy and product work
2. **The Book** — You, with AI. Amplified.
3. **Lucy's App** — Melanin Creative Platform
4. **Infrastructure** — Gatekeeper, PUDDING OS, technical plumbing

**8 Domain Labels:**
- `finance` (#22c55e green)
- `operations` (#3b82f6 blue)
- `people` (#a855f7 purple)
- `marketing` (#f97316 orange)
- `sales` (#ef4444 red)
- `customer` (#eab308 yellow)
- `tech` (#6b7280 grey)
- `strategy` (#92400e brown)
- `onboarding` (#9ca3af grey)

**Verification task created in Infrastructure project:**
- Title: "Verify Gatekeeper → Linear integration"
- Description: "First task created to verify the pipeline."

**Note:** COV-series issues (if they existed) would have been in the Cove Code Factory Linear project, but since the cove repo is empty, this project may not have been formally created in Linear yet or COV issues may never have been filed.

---

## SECTION 5: TODOIST PROJECTS AND TASKS

Source: Todoist connector (todoist__pipedream) — retrieved 2026-03-27

### Projects (3 total)

| ID | Name | Color | Status | Shared |
|----|------|-------|--------|--------|
| `6g4M67WFhgGfX3mw` | **Inbox** | charcoal | — | No |
| `6g4M6GXMhXqfHwP5` | **Team Setup Guide** | charcoal | IN_PROGRESS | Yes (workspace: 537564) |
| `6g4M6hxX3HjcGq27` | **Amplified Partners** | berry_red | — | No |

---

### Project: Inbox (2 uncompleted tasks)

| Task | Description | Priority | Added |
|------|-------------|----------|-------|
| Create the Overall Project | "The extraction and byiud of my ptojrct" (sic) | P1 | 2026-03-23 |
| [Claude Channels Just Dropped, And It Kills OpenClaw [Again] - YouTube](https://www.youtube.com/watch?v=ot3NM5OVFmc) | *(no description)* | P1 | 2026-03-23 |

---

### Project: Team Setup Guide (6 uncompleted tasks)
*(These appear to be Todoist onboarding tasks, shared project)*

| Task | Note |
|------|------|
| Remember: Folders → Projects → Sections → Tasks! | Structural reminder |
| Creating folders (Demo) | Arcade demo link |
| Creating projects (Watch) | YouTube tutorial |
| → Add sections (Watch) | Sub-task of above |
| → Discover layouts (List / Board / Calendar) | Sub-task of above |
| Creating project templates (Demo) | Arcade demo link |

---

### Project: Amplified Partners (16 uncompleted tasks)

| # | Task | Priority | Due | Notes |
|---|------|----------|-----|-------|
| 1 | Log into IBKR — check account still active (50 quid in there) | P4 (Urgent) | — | ibkr.co.uk; enable Client Portal API; note Account ID (U + 8 digits) |
| 2 | Set up Telegram bot for fund watcher | P4 (Urgent) | — | @BotFather → /newbot; get token; find chat ID via getUpdates |
| 3 | Get NewsAPI key (free) or confirm Perplexity key for fund watcher | P3 (High) | — | newsapi.org free tier, 100 req/day |
| 4 | Install fund watcher dependencies and test | P3 (High) | — | `cd ~/Manual Library/Projects/amplified-fund && pip install -r requirements.txt && python watcher.py --test-telegram` |
| 5 | Deploy fund watcher as launchd service (24/7) | P3 (High) | — | Fill keys in com.amplified.fund-watcher.plist → copy to ~/Library/LaunchAgents/ → launchctl load |
| 6 | Sit down with Lucy — review the research brief | P3 (High) | — | Etsy digital downloads (wedding invitations, multicultural). File: real-vault/work/sessions/LUCY-RESEARCH-BRIEF-2026-02-22.md |
| 7 | Approach Dave at Jesmond Plumbing — end of March | P3 (High) | 2026-03-25 | First client. Have the interview ready. |
| 8 | Set up three Substack accounts: Amplified Partners, Investigative Journalism, Claude personal | P2 (Medium) | — | Blue Pen + AI knowledge essay ready to publish; claude-writing directory in vault |
| 9 | Fix Hetzner SSH access — 4 servers locked out | P2 (Medium) | — | Add SSH key via Hetzner console. Servers: 159.69.209.172, 91.99.206.137, 159.69.223.130, 159.69.216.213 |
| 10 | Build IBKR API connection into fund watcher (Phase 2) | P1 (Low) | — | Swap yfinance for live portfolio data; ibkr_client.py stub in project |
| 11 | Spec kids vault architecture — one system, six configurations | P1 (Low) | — | Demario 14, Freya 17, Tyrone 26, Tom 18, Tom's twin 18, James 22. Philosophy: KIDS-VAULT-PHILOSOPHY-2026-02-22.md |
| 12 | Secure Qdrant — currently NO authentication | P2 (Medium) | — | Add API key authentication before any client data |
| 13 | Restart Claude Code in new terminal (ANTHROPIC_BASE_URL takes effect — proxy saves money) | P4 (Urgent) | — | — |
| 14 | Reload OpenClaw gateway — activates Kaizen | P3 (High) | — | `launchctl unload/load ~/Library/LaunchAgents/ai.openclaw.gateway.plist` |
| 15 | Get Telegram chat ID — put in ~/.amplified/keys.env as EWAN_TELEGRAM_CHAT_ID | P3 (High) | — | Unblocks daily cost reports; label: userinfobot |
| 16 | Create 6 Telegram bots via BotFather; add tokens to openclaw.json (did 3 so far) | P2 (Medium) | — | Bots: Demario, Freya, Tyrone, Tom, Ava, James; tokens → ~/.openclaw/openclaw.json |

---

## SECTION 6: SUPPLEMENTARY CONTEXT

### Amplified Partners Vision Summary
Source: `work/amplified-partners-master.md`

- **Founder:** Ewan Bramley, Newcastle upon Tyne, UK
- **Background:** Former dentist, 25+ years, £2M+ practice built from scratch
- **Evolution:** covered.AI → Amplified Partners (AI = Amplified)
- **Target:** UK SMBs, 2-10 employees, £0-3M turnover
- **Core Truth:** "No one makes bad decisions on purpose. They make the best call with the map and numbers they've got."
- **Board of LLMs:** Strategist (Claude), Executor (GPT-4o), Analyst (Gemini), Specialist (Local models)
- **Team:** Sam and Eli mentioned as AI team members alongside Ewan; Sentinel referenced in SOUL-v4

### Gatekeeper System (2026-02-05)
Source: `_inbox-work/2026-02-05-Gatekeeper-Agent-Setup-Meeting.md`

- Vault location: `/Users/ewanbramley/Manual Library/real-vault`
- Six-component Python architecture
- Stack: Python, Claude 4.5 Sonnet API, Obsidian, Qdrant, Linear, GitHub
- Quality principles: radically transparent, radically honest, win-win, meritocracy, partnership model

### Infrastructure: Hetzner Servers
4 servers currently locked out (SSH issue):
- 159.69.209.172
- 91.99.206.137
- 159.69.223.130
- 159.69.216.213

### Fund Watcher Project
- Location: `~/Manual Library/Projects/amplified-fund/`
- Components: `watcher.py`, `ibkr_client.py`, `requirements.txt`, `com.amplified.fund-watcher.plist`
- Runs daily at 07:00 UTC via launchd
- News source: NewsAPI.org (free tier) or Perplexity API
- Phase 2: Live IBKR portfolio data (stub ready)

---

## GAPS AND NOTES

1. **No "Perplexity custom skills with IDs" found.** Ewan used Perplexity heavily as a research tool (many exported threads in vault), but there is no evidence of Perplexity-native custom skills or agents with discrete IDs. The "skills" built in January 2026 were KiloCode rule files and the Byker Skills library.

2. **Cove repo is empty.** The COV Linear issue series cannot be confirmed as the cove repo has zero commits. The Cove Code Factory concept exists (Temporal-based pipeline, MCP bridge, Layer 0 laws) but has not yet been implemented.

3. **No BATON-PASS-PROTOCOL.md found.** The closest equivalent is `_staging/12-archive-raw/CLAUDE-CODE-HANDOFF.md`. Baton-pass functionality is handled by the gatekeeper agent and session documentation pattern.

4. **Vault numbered directories are 01-12** (not 00-23). The vault uses a department-numbered staging system with gaps (no 04, 06, 10) rather than a 00-23 system.

5. **Linear API not directly queried.** COV issues would require a live Linear API call with Ewan's credentials. The gatekeeper's setup_linear.py shows the team/project structure but actual issue lists are not accessible here.

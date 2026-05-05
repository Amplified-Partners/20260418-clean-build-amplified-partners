---
title: "Byker 2026: Full-Stack Automated Digital Agency Architecture"
id: "byker-2026-architecture-v1"
version: 1
created: "2026-04-25"
type: "document"
topic_type: "architecture"
audience: "internal"
layer: "truth"
status: "filed"
signed_by: "Devon, 2026-04-25, devin-992682c244cf444f91e0a516498afbfd"
---

# Byker 2026: Full-Stack Automated Digital Agency Architecture

## Executive Summary

This document outlines a comprehensive, no-fluff architecture for running a fully automated digital marketing agency using your existing Mac infrastructure, local LLMs, and cloud deployment via Railway.

**Philosophy:** Every component earns its place. No dead wood. Complete automation where possible, human oversight where necessary.

---

## Part 1: What You Have (Asset Audit)

### Current Stack Assessment

| Component | Status | Location/Version | Readiness |
|-----------|--------|------------------|-----------|
| **AI Providers** | ✅ Ready | agentic_workflow/ | 6 providers configured |
| **Gemini API** | ✅ Active | API key configured | Working |
| **Anthropic SDK** | ✅ Installed | v0.40.0 | Needs API key |
| **Qwen/DeepSeek** | ✅ Configured | dashscope SDK | Ready |
| **Node.js** | ✅ v22.21.0 | System | Production-ready |
| **Python** | ✅ 3.10.12 | System | 149 packages |
| **Railway** | ✅ Configured | melanin-design-platform | Deployment ready |
| **Docker Compose** | ✅ Files exist | melanin-design-platform | Needs Docker daemon |
| **PostgreSQL** | ⚠️ Config only | Docker image defined | Needs Docker |
| **MCP Servers** | ✅ 4 configured | .kilocode/mcp.json | Ready |
| **Obsidian** | ❌ Not installed | DMG in Downloads | Needs setup |
| **Ollama** | ❌ Not installed | N/A | Optional |

### Current Projects That Can Be Leveraged

1. **agentic_workflow/** - Multi-provider LLM orchestration (FastAPI)
2. **lead-engine/** - Lead processing with PostgreSQL (FastAPI)  
3. **melanin-design-platform/** - Full-stack app with Railway deployment
4. **interior-design-system/** - RAG pipeline with ChromaDB

---

## Part 2: The 2026 Vision Architecture

### System Overview

```
┌──────────────────────────────────────────────────────────────────────────┐
│                        BYKER COMMAND CENTER                               │
│                    (Obsidian as Central Brain)                           │
├──────────────────────────────────────────────────────────────────────────┤
│                                                                          │
│  ┌─────────────┐   ┌─────────────┐   ┌─────────────┐   ┌─────────────┐  │
│  │  KNOWLEDGE  │   │  WORKFLOW   │   │   CLIENT    │   │   CONTENT   │  │
│  │    VAULT    │   │   ENGINE    │   │   PORTAL    │   │   FACTORY   │  │
│  └──────┬──────┘   └──────┬──────┘   └──────┬──────┘   └──────┬──────┘  │
│         │                 │                 │                 │          │
│         └─────────────────┼─────────────────┼─────────────────┘          │
│                           ▼                 ▼                            │
│                    ┌─────────────────────────────┐                       │
│                    │    LLM ORCHESTRATION LAYER  │                       │
│                    │  (Multi-Provider + Local)   │                       │
│                    └─────────────┬───────────────┘                       │
│                                  │                                       │
│    ┌─────────────────────────────┼─────────────────────────────┐        │
│    ▼              ▼              ▼              ▼               ▼        │
│ ┌──────┐    ┌──────┐    ┌───────────┐    ┌──────┐    ┌──────────┐       │
│ │Claude│    │Gemini│    │Qwen/Deep- │    │Llama │    │ Ollama   │       │
│ │(API) │    │(API) │    │Seek (API) │    │(API) │    │ (Local)  │       │
│ └──────┘    └──────┘    └───────────┘    └──────┘    └──────────┘       │
│                                                                          │
└──────────────────────────────────────────────────────────────────────────┘
                                    │
                                    ▼
┌──────────────────────────────────────────────────────────────────────────┐
│                        RAILWAY DEPLOYMENT                                 │
├──────────────────────────────────────────────────────────────────────────┤
│                                                                          │
│  ┌──────────────┐  ┌──────────────┐  ┌──────────────┐  ┌─────────────┐  │
│  │   FASTAPI    │  │   CLIENT     │  │   WORKFLOW   │  │  POSTGRES   │  │
│  │   BACKEND    │  │  DASHBOARD   │  │    ENGINE    │  │   DATABASE  │  │
│  │   (Python)   │  │   (React)    │  │   (Python)   │  │             │  │
│  └──────────────┘  └──────────────┘  └──────────────┘  └─────────────┘  │
│                                                                          │
└──────────────────────────────────────────────────────────────────────────┘
```

---

## Part 3: Obsidian Vault Architecture

### Why Obsidian as Command Center

1. **Local-first** - All data on your machine, syncs to iCloud
2. **Linked thinking** - Everything connects to everything
3. **Plugin ecosystem** - AI integration, automation, publishing
4. **Markdown native** - All your skills are already markdown
5. **No vendor lock-in** - Plain files, always exportable

### Vault Structure

```
📁 Byker-Vault/
├── 📁 00-INBOX/                    # Quick capture, unsorted
│   ├── quick-notes.md
│   └── voice-memos/
│
├── 📁 10-CLIENTS/                  # Per-client workspaces
│   ├── 📁 _templates/
│   │   ├── client-onboarding.md
│   │   ├── diagnostic-report.md
│   │   └── weekly-review.md
│   ├── 📁 active/
│   │   ├── 📁 newcastle-plumbing/
│   │   │   ├── overview.md
│   │   │   ├── diagnostics/
│   │   │   ├── systems-built/
│   │   │   ├── communications/
│   │   │   └── metrics.md
│   │   └── 📁 other-clients.../
│   └── 📁 archive/
│
├── 📁 20-KNOWLEDGE/                # Your intellectual capital
│   ├── 📁 frameworks/
│   │   ├── dalio-principles.md
│   │   ├── godin-marketing.md
│   │   └── ziglar-sales.md
│   ├── 📁 smb-expertise/           # Your 22 SMB modules
│   │   ├── cash-flow.md
│   │   ├── pricing.md
│   │   └── ... (all SMB skills)
│   ├── 📁 industry-benchmarks/
│   └── 📁 case-studies/
│
├── 📁 30-CONTENT/                  # Content factory workspace
│   ├── 📁 ideas/                   # Idea capture
│   ├── 📁 drafts/                  # Work in progress
│   ├── 📁 ready-to-publish/        # Approved content
│   ├── 📁 published/               # Archive with URLs
│   └── 📁 templates/
│       ├── linkedin-post.md
│       ├── carousel.md
│       └── email-sequence.md
│
├── 📁 40-OPERATIONS/               # Business ops
│   ├── 📁 sops/                    # Standard operating procedures
│   ├── 📁 checklists/
│   ├── 📁 metrics/
│   └── 📁 decisions/               # Decision log (Dalio-style)
│
├── 📁 50-SYSTEMS/                  # Technical infrastructure
│   ├── 📁 skills/                  # Your Byker skills (symlink or copy)
│   ├── 📁 automations/
│   ├── 📁 integrations/
│   └── 📁 ai-prompts/              # Prompt library
│
├── 📁 60-REFERENCE/                # Static reference material
│   ├── 📁 docs/
│   ├── 📁 resources/
│   └── 📁 templates/
│
├── 📁 90-META/                     # Vault management
│   ├── 📁 daily-notes/
│   ├── 📁 weekly-reviews/
│   └── dashboard.md
│
└── 📁 .obsidian/                   # Vault configuration
    ├── plugins/
    ├── themes/
    └── workspace.json
```

### Essential Plugins

| Plugin | Purpose | Why It Matters |
|--------|---------|----------------|
| **Smart Connections** | AI-powered linking | Surfaces related content automatically |
| **Copilot** | Local LLM integration | Queries vault using Ollama/Claude |
| **Dataview** | Database queries | Client dashboards, metrics tracking |
| **Templater** | Dynamic templates | Automated client folder creation |
| **Tasks** | Task management | Track client deliverables |
| **Excalidraw** | Visual diagrams | Architecture sketches, client visuals |
| **Periodic Notes** | Daily/weekly notes | Structured reflection |
| **Git** | Version control | Backup and history |
| **Kanban** | Visual workflow | Content pipeline, client progress |
| **QuickAdd** | Rapid capture | Voice → note, web clip → vault |

### Smart Connections Configuration

```json
// .obsidian/plugins/smart-connections/data.json
{
  "api_key": "YOUR_OPENAI_OR_OLLAMA_KEY",
  "model": "ollama/qwen2.5:7b",  // Use local Qwen
  "embedding_model": "nomic-embed-text",
  "chat_model": "ollama/qwen2.5:7b",
  "local_embedding": true,
  "excluded_folders": ["90-META", ".obsidian"],
  "included_file_extensions": [".md"],
  "smart_connections": {
    "min_similarity": 0.7,
    "max_results": 20
  }
}
```

---

## Part 4: LLM Orchestration Layer

### Multi-Provider Strategy

**Principle:** Use the right model for the right job. Cost-optimize without sacrificing quality.

```python
# LLM Router Logic
class LLMRouter:
    """Route tasks to optimal LLM based on requirements."""
    
    ROUTING_RULES = {
        # Task Type → Preferred Model Chain
        "diagnostic_analysis": ["claude-sonnet", "gemini-pro", "qwen-plus"],
        "content_writing": ["claude-sonnet", "qwen-max", "gemini-pro"],
        "code_generation": ["claude-sonnet", "deepseek-coder", "qwen-coder"],
        "quick_tasks": ["qwen-turbo", "gemini-flash", "deepseek-chat"],
        "embeddings": ["ollama/nomic-embed", "text-embedding-3-small"],
        "local_private": ["ollama/qwen2.5", "ollama/llama3.1"],
    }
    
    COST_TIERS = {
        "premium": ["claude-sonnet", "claude-opus", "gpt-4o"],
        "standard": ["gemini-pro", "qwen-plus", "qwen-max"],
        "budget": ["qwen-turbo", "deepseek-chat", "gemini-flash"],
        "free": ["ollama/*"],
    }
```

### Local LLM Setup (Ollama)

**Install Ollama:**
```bash
# On Mac
curl -fsSL https://ollama.com/install.sh | sh

# Pull recommended models
ollama pull qwen2.5:7b      # Best balance of speed/quality
ollama pull llama3.1:8b     # Good general purpose
ollama pull nomic-embed-text # For embeddings (Smart Connections)
ollama pull codellama:7b    # For code tasks
```

**Why These Models:**
- **qwen2.5:7b** - Excellent multilingual, fast, good at following instructions
- **llama3.1:8b** - Strong reasoning, open weights
- **nomic-embed-text** - High-quality local embeddings for RAG
- **codellama:7b** - Code-specific fine-tuning

### Provider Priority Matrix

| Task Type | Priority 1 | Priority 2 | Priority 3 | Fallback |
|-----------|------------|------------|------------|----------|
| **Client Report** | Claude Sonnet | Gemini Pro | Qwen Plus | - |
| **Quick Question** | Qwen Turbo | Gemini Flash | Local Qwen | - |
| **Content Draft** | Claude Sonnet | Qwen Max | Local Llama | - |
| **Code Generation** | Claude Sonnet | DeepSeek Coder | Local CodeLlama | - |
| **Embeddings** | Local Nomic | OpenAI Ada | Gemini | - |
| **Private/Sensitive** | Local Only | - | - | - |
| **Bulk Processing** | DeepSeek | Qwen Turbo | Local | - |

---

## Part 5: Railway Deployment Architecture

### Services to Deploy

```yaml
# railway.toml - Multi-service configuration
[services]

  # 1. Core API Backend
  [services.api]
    name = "byker-api"
    runtime = "python"
    build_command = "pip install -r requirements.txt"
    start_command = "uvicorn main:app --host 0.0.0.0 --port $PORT"
    [services.api.env]
      ANTHROPIC_API_KEY = "@secret:ANTHROPIC_API_KEY"
      GEMINI_API_KEY = "@secret:GEMINI_API_KEY"
      DATABASE_URL = "@database:DATABASE_URL"

  # 2. Client Dashboard (React)
  [services.dashboard]
    name = "byker-dashboard"
    runtime = "node"
    build_command = "npm run build"
    start_command = "npm run start"
    [services.dashboard.env]
      VITE_API_URL = "@services.api.url"

  # 3. Workflow Engine (Python - AI-Controlled)
  [services.workflows]
    name = "byker-workflows"
    runtime = "python"
    build_command = "pip install -r requirements.txt"
    start_command = "uvicorn workflow_engine:app --host 0.0.0.0 --port $PORT"
    [services.workflows.env]
      DATABASE_URL = "@database:DATABASE_URL"
      API_URL = "@services.api.url"

  # 4. PostgreSQL Database
  [services.postgres]
    name = "byker-db"
    plugin = "postgresql"
```

### Why Custom Workflow Engine (Not N8N)

**Custom Engine Advantages:**
- 100% AI-controllable (Kilo instances can read/write/debug)
- No external dependencies
- No extra hosting cost (runs in same Railway project)
- Full Python ecosystem (any library, any integration)
- Version controlled (Git)
- Testable (pytest)

**Key Workflows Built In Python:**
1. New lead → Score → Route → Sequence
2. Client signup → Onboard → Dashboard → Welcome video
3. Content calendar → Generate → Review → Publish
4. Daily metrics → Dashboard update → Alert if needed

---

## Part 6: The Automation Stack

### Complete Flow

```
┌─────────────────────────────────────────────────────────────────────┐
│                       TRIGGER LAYER                                  │
├─────────────────────────────────────────────────────────────────────┤
│  Webhooks │ Scheduled │ Email │ Form Submit │ Calendar │ Manual    │
└─────────────────────────────────────────────────────────────────────┘
                                    │
                                    ▼
┌─────────────────────────────────────────────────────────────────────┐
│                  CUSTOM WORKFLOW ENGINE (Python)                     │
│                      (Railway Hosted)                                │
├─────────────────────────────────────────────────────────────────────┤
│                                                                      │
│  ┌──────────────┐  ┌──────────────┐  ┌──────────────┐              │
│  │ Lead Capture │  │ Client Ops   │  │ Content      │              │
│  │ Workflows    │  │ Workflows    │  │ Workflows    │              │
│  └──────┬───────┘  └──────┬───────┘  └──────┬───────┘              │
│         │                 │                 │                       │
│         └─────────────────┼─────────────────┘                       │
│                           ▼                                         │
│                   ┌───────────────┐                                 │
│                   │  BYKER API    │                                 │
│                   │  (FastAPI)    │                                 │
│                   └───────┬───────┘                                 │
│                           │                                         │
└───────────────────────────┼─────────────────────────────────────────┘
                            │
                            ▼
┌─────────────────────────────────────────────────────────────────────┐
│                     LLM PROCESSING                                   │
├─────────────────────────────────────────────────────────────────────┤
│                                                                      │
│   Cloud APIs                          Local (Mac)                   │
│   ┌────────┐ ┌────────┐ ┌────────┐   ┌────────────────────────┐    │
│   │ Claude │ │ Gemini │ │ Qwen   │   │      OLLAMA            │    │
│   │  API   │ │  API   │ │  API   │   │ ┌────────┐ ┌────────┐ │    │
│   └────────┘ └────────┘ └────────┘   │ │Qwen2.5 │ │Llama3.1│ │    │
│                                       │ └────────┘ └────────┘ │    │
│   (For client work)                   │ (For private/dev/bulk)│    │
│                                       └────────────────────────┘    │
│                                                                      │
└─────────────────────────────────────────────────────────────────────┘
                            │
                            ▼
┌─────────────────────────────────────────────────────────────────────┐
│                     OUTPUT LAYER                                     │
├─────────────────────────────────────────────────────────────────────┤
│                                                                      │
│  ┌──────────┐  ┌──────────┐  ┌──────────┐  ┌──────────┐            │
│  │ Obsidian │  │ Client   │  │ Email/   │  │ Social   │            │
│  │  Vault   │  │ Dashboard│  │ SMS      │  │ Media    │            │
│  └──────────┘  └──────────┘  └──────────┘  └──────────┘            │
│                                                                      │
└─────────────────────────────────────────────────────────────────────┘
```

---

## Part 7: Implementation Roadmap

### Phase 1: Foundation (Week 1)

**Day 1-2: Obsidian Setup**
- [ ] Install Obsidian from DMG
- [ ] Create vault structure as specified
- [ ] Install core plugins (Smart Connections, Copilot, Dataview, Templater)
- [ ] Import Byker skills into vault
- [ ] Configure Smart Connections for local embeddings

**Day 3-4: Local LLM Setup**
- [ ] Install Ollama
- [ ] Pull qwen2.5:7b, llama3.1:8b, nomic-embed-text
- [ ] Configure Obsidian Copilot to use Ollama
- [ ] Test Smart Connections with local embeddings
- [ ] Create API endpoint for local LLM (FastAPI wrapper)

**Day 5-7: Cloud APIs**
- [ ] Verify Gemini API working
- [ ] Add Anthropic API key
- [ ] Configure Qwen/DeepSeek API keys
- [ ] Build provider router in agentic_workflow
- [ ] Test all providers with health checks

### Phase 2: Railway Deployment (Week 2)

**Day 8-10: Core Services**
- [ ] Deploy FastAPI backend to Railway
- [ ] Set up PostgreSQL database
- [ ] Deploy React dashboard
- [ ] Configure environment variables

**Day 11-14: Workflow Engine Setup**
- [ ] Deploy workflow engine to Railway
- [ ] Configure webhook URLs
- [ ] Build first workflow: Lead capture
- [ ] Build second workflow: Client onboarding
- [ ] Configure scheduled tasks (APScheduler)

### Phase 3: Integration (Week 3)

**Day 15-17: Obsidian ↔ System**
- [ ] Set up Obsidian URI scheme handlers
- [ ] Create QuickAdd macros for common tasks
- [ ] Build Dataview dashboards for clients
- [ ] Configure auto-sync for client folders

**Day 18-21: Automation Flows**
- [ ] Build content generation workflow
- [ ] Build diagnostic report workflow
- [ ] Build retention check workflow
- [ ] Test end-to-end flows

### Phase 4: Polish (Week 4)

**Day 22-28: Refinement**
- [ ] Performance optimization
- [ ] Error handling and logging
- [ ] Documentation
- [ ] Backup strategy
- [ ] Monitoring setup

---

## Part 8: Cost Model

### Monthly Running Costs (Estimated)

| Service | Free Tier | Expected Use | Monthly Cost |
|---------|-----------|--------------|--------------|
| **Railway** | $5 credit | ~$20-50 | ~$15-45 |
| **Claude API** | None | Moderate | ~$50-100 |
| **Gemini API** | 60 req/min free | Backup | ~$0-20 |
| **Qwen API** | Free tier exists | Bulk work | ~$10-30 |
| **DeepSeek** | Cheap | Code tasks | ~$5-15 |
| **Ollama** | Free | Local dev | $0 |
| **Obsidian** | Free | Core use | $0 |
| **Obsidian Sync** | Optional | Backup | $0-10 |
| **iCloud** | Existing | Backup | $0 |

**Total Estimated:** £80-220/month (scales with usage)

### ROI at £250K Target

- Monthly revenue target: ~£21K
- Infrastructure cost: ~£150 (average)
- Infrastructure as % of revenue: <1%

---

## Part 9: What Makes This Ingenious

### 1. No Dead Wood
Every component serves a purpose:
- Obsidian = Brain (not just note-taking, actual operational hub)
- Ollama = Free compute for bulk/dev work
- Cloud APIs = Quality when it matters
- Railway = Deployment without DevOps overhead
- Workflow Engine = AI-controllable Python code

### 2. Cost Optimization
- Local LLMs handle 60-70% of tasks for free
- Cloud APIs only for client-facing quality
- Railway scales to zero when idle
- No per-seat licensing

### 3. Data Sovereignty
- All client data in your Obsidian vault
- Local embeddings = no data sent externally
- You own your intellectual property
- GDPR-friendly architecture

### 4. Scalability
- Same system works for 1 client or 100
- Workflow modules copy for new use cases
- Railway auto-scales on demand
- Add team members without rebuilding

### 5. Resilience
- Multiple LLM providers = no single point of failure
- Local fallback always available
- Obsidian works offline
- Git backup for everything

---

## Part 10: The Daily Flow (How You'll Use This)

### Morning (15 mins)
1. Open Obsidian dashboard
2. Review overnight automations (workflow logs)
3. Check client metrics (Dataview queries)
4. Capture priorities for day

### Client Work (Variable)
1. Open client folder in Obsidian
2. AI suggests relevant past notes (Smart Connections)
3. Generate content/reports with Copilot (local LLM)
4. Trigger workflow for delivery
5. Auto-log to client folder

### Content Creation (1 hr/day)
1. Open 30-CONTENT/ideas/
2. AI expands idea to draft (local LLM)
3. Refine with Claude (cloud API)
4. Queue in ready-to-publish
5. Workflow engine handles scheduling

### Evening (10 mins)
1. Quick daily note capture
2. Workflow engine runs overnight tasks
3. Dashboard updates automatically
4. Sleep knowing system is working

---

## Approval Checkpoint

**Ewan, this is the architecture I'm proposing. Before I proceed with implementation, I need your input:**

1. **Obsidian Structure** - Does this vault layout make sense for how you think?

2. **Local LLMs** - Are you comfortable installing Ollama? It requires ~10GB for recommended models.

3. **Railway Costs** - The estimated £80-220/month - acceptable for infrastructure?

4. **Custom Workflows** - Python-based workflow engine, fully AI-controllable.

5. **Priority** - What should we build first?
   - [ ] Obsidian vault setup (foundation)
   - [ ] Ollama + local LLMs (free compute)
   - [ ] Railway deployment (cloud infrastructure)
   - [ ] Workflow engine (automation)

**Reply with your thoughts and I'll proceed with detailed implementation.**

---

## Part 11: LLM Orchestration - Deep Dive

### The Intelligence Layer Architecture

This is where the magic happens. The LLM orchestration layer makes intelligent decisions about which AI to use, when to use local vs cloud, and how to chain multiple models for optimal results.

```
┌─────────────────────────────────────────────────────────────────────────────┐
│                       LLM ORCHESTRATION LAYER                                │
├─────────────────────────────────────────────────────────────────────────────┤
│                                                                              │
│  ┌────────────────────────────────────────────────────────────────────────┐ │
│  │                        REQUEST CLASSIFIER                               │ │
│  │  Incoming Task → Analyse → Route to optimal model                       │ │
│  └───────────────────────────────┬────────────────────────────────────────┘ │
│                                  │                                           │
│         ┌────────────────────────┼────────────────────────────┐             │
│         ▼                        ▼                            ▼             │
│  ┌──────────────┐      ┌──────────────┐             ┌──────────────┐       │
│  │   QUALITY    │      │     SPEED    │             │    COST      │       │
│  │   ROUTING    │      │   ROUTING    │             │  ROUTING     │       │
│  │              │      │              │             │              │       │
│  │ Client-facing│      │ Internal ops │             │ Bulk tasks   │       │
│  │ Reports      │      │ Quick Q&A    │             │ Summaries    │       │
│  │ Content      │      │ Automation   │             │ Processing   │       │
│  │              │      │              │             │              │       │
│  │  → Claude    │      │  → Gemini    │             │  → Qwen      │       │
│  │  → GPT-4     │      │  → Local     │             │  → DeepSeek  │       │
│  └──────────────┘      └──────────────┘             │  → Local     │       │
│                                                      └──────────────┘       │
│                                                                              │
│  ┌────────────────────────────────────────────────────────────────────────┐ │
│  │                       FALLBACK CHAIN                                    │ │
│  │  Claude → Gemini → Qwen → DeepSeek → Local Qwen → Local Llama          │ │
│  │  (If primary fails, automatically cascade to next)                      │ │
│  └────────────────────────────────────────────────────────────────────────┘ │
│                                                                              │
│  ┌────────────────────────────────────────────────────────────────────────┐ │
│  │                       COST TRACKER                                      │ │
│  │  Real-time spend monitoring • Daily/monthly limits • Usage analytics    │ │
│  └────────────────────────────────────────────────────────────────────────┘ │
│                                                                              │
└─────────────────────────────────────────────────────────────────────────────┘
```

### Intelligent Task Classification

```python
# Task classification system
TASK_SIGNATURES = {
    "diagnostic_analysis": {
        "patterns": ["diagnose", "analyze", "audit", "assess", "evaluate"],
        "complexity": "high",
        "quality_threshold": "premium",
        "preferred_chain": ["claude-sonnet", "gemini-pro", "qwen-plus"],
        "context_window_need": "large",
        "rationale": "Client-facing, needs nuanced business understanding"
    },

    "content_creation": {
        "patterns": ["write", "create", "draft", "compose", "generate content"],
        "complexity": "high",
        "quality_threshold": "premium",
        "preferred_chain": ["claude-sonnet", "qwen-max", "gemini-pro"],
        "context_window_need": "medium",
        "rationale": "Brand voice, psychological hooks, needs creativity"
    },

    "code_generation": {
        "patterns": ["code", "script", "function", "api", "automate"],
        "complexity": "medium-high",
        "quality_threshold": "standard",
        "preferred_chain": ["claude-sonnet", "deepseek-coder", "qwen-coder"],
        "context_window_need": "medium",
        "rationale": "Technical accuracy over prose quality"
    },

    "summarisation": {
        "patterns": ["summarize", "condense", "brief", "tldr", "key points"],
        "complexity": "low",
        "quality_threshold": "budget",
        "preferred_chain": ["gemini-flash", "qwen-turbo", "local-qwen"],
        "context_window_need": "varies",
        "rationale": "Speed over eloquence, bulk processing friendly"
    },

    "question_answering": {
        "patterns": ["what is", "how do", "explain", "tell me", "?"],
        "complexity": "low-medium",
        "quality_threshold": "budget",
        "preferred_chain": ["local-qwen", "gemini-flash", "qwen-turbo"],
        "context_window_need": "small",
        "rationale": "Quick responses, often doesn't need premium models"
    },

    "data_extraction": {
        "patterns": ["extract", "parse", "pull out", "find in", "get from"],
        "complexity": "medium",
        "quality_threshold": "standard",
        "preferred_chain": ["deepseek-chat", "qwen-plus", "local-qwen"],
        "context_window_need": "large",
        "rationale": "Structured output, accuracy over creativity"
    },

    "private_sensitive": {
        "patterns": ["confidential", "private", "sensitive", "internal only"],
        "complexity": "varies",
        "quality_threshold": "local_only",
        "preferred_chain": ["local-qwen", "local-llama"],
        "context_window_need": "varies",
        "rationale": "Data never leaves the machine"
    },

    "embedding_generation": {
        "patterns": ["embed", "vector", "similarity", "search index"],
        "complexity": "low",
        "quality_threshold": "local_preferred",
        "preferred_chain": ["local-nomic", "openai-ada", "gemini-embed"],
        "context_window_need": "small",
        "rationale": "High volume, local = free and fast"
    }
}
```

### Model Capability Matrix

| Model | Context | Strengths | Weaknesses | Cost/1M tokens | Best For |
|-------|---------|-----------|------------|----------------|----------|
| **Claude Sonnet** | 200K | Nuance, business, writing | API cost | ~$3/$15 | Client work |
| **Gemini Pro** | 1M+ | Huge context, multimodal | Sometimes verbose | ~$1.25/$5 | Long docs |
| **Gemini Flash** | 1M+ | Speed, cost | Less nuanced | ~$0.075/$0.3 | Quick tasks |
| **Qwen Max** | 32K | Chinese/English, creative | Smaller context | ~$2/$6 | Content |
| **Qwen Plus** | 32K | Balanced | - | ~$0.8/$2 | General |
| **Qwen Turbo** | 8K | Fast, cheap | Small context | ~$0.3/$0.6 | Bulk work |
| **DeepSeek Coder** | 64K | Code excellence | Non-code weaker | ~$0.14/$0.28 | Coding |
| **DeepSeek Chat** | 64K | Reasoning, cheap | Less creative | ~$0.14/$0.28 | Analysis |
| **Local Qwen 2.5:7b** | 8K | Free, private | Hardware bound | $0 | Dev, private |
| **Local Llama 3.1:8b** | 8K | Free, reasoning | Hardware bound | $0 | Dev, private |

### Multi-Model Pipelines

For complex tasks, chain models together:

```
┌─────────────────────────────────────────────────────────────────────────────┐
│              DIAGNOSTIC REPORT PIPELINE (Example)                            │
├─────────────────────────────────────────────────────────────────────────────┤
│                                                                              │
│  Stage 1: Data Processing                                                    │
│  ┌──────────────────────────────────────────────────────────────────────┐   │
│  │ Local Qwen: Parse financial data, extract key metrics                 │   │
│  │ Cost: $0 | Speed: Fast | Output: Structured JSON                     │   │
│  └───────────────────────────────────┬──────────────────────────────────┘   │
│                                      ▼                                       │
│  Stage 2: Pattern Analysis                                                   │
│  ┌──────────────────────────────────────────────────────────────────────┐   │
│  │ DeepSeek Chat: Identify anomalies, benchmark comparisons              │   │
│  │ Cost: ~$0.05 | Speed: Fast | Output: Analysis notes                  │   │
│  └───────────────────────────────────┬──────────────────────────────────┘   │
│                                      ▼                                       │
│  Stage 3: Insight Generation                                                 │
│  ┌──────────────────────────────────────────────────────────────────────┐   │
│  │ Claude Sonnet: Generate business insights, recommendations            │   │
│  │ Cost: ~$0.50 | Speed: Medium | Output: Professional prose            │   │
│  └───────────────────────────────────┬──────────────────────────────────┘   │
│                                      ▼                                       │
│  Stage 4: Final Report                                                       │
│  ┌──────────────────────────────────────────────────────────────────────┐   │
│  │ Claude Sonnet: Assemble into client-ready report with Dalio framing   │   │
│  │ Cost: ~$0.50 | Speed: Medium | Output: Polished DOCX                 │   │
│  └──────────────────────────────────────────────────────────────────────┘   │
│                                                                              │
│  Total Pipeline Cost: ~$1.05 per diagnostic                                  │
│  vs $3-5 if using premium model for everything                               │
│                                                                              │
└─────────────────────────────────────────────────────────────────────────────┘
```

---

## Part 12: Full-Stack Automated Agency Blueprint

### The 2026 Digital Agency - Component Map

```
┌─────────────────────────────────────────────────────────────────────────────────┐
│                                                                                  │
│                    BYKER AUTOMATED AGENCY ARCHITECTURE                           │
│                         "Full Stack, No Dead Wood"                               │
│                                                                                  │
├─────────────────────────────────────────────────────────────────────────────────┤
│                                                                                  │
│  ┌─────────────────────────────────────────────────────────────────────────┐   │
│  │                        CUSTOMER ACQUISITION LAYER                        │   │
│  ├─────────────────────────────────────────────────────────────────────────┤   │
│  │                                                                          │   │
│  │  ┌─────────────┐   ┌─────────────┐   ┌─────────────┐   ┌─────────────┐ │   │
│  │  │   CONTENT   │   │   LEAD      │   │  OUTBOUND   │   │   SOCIAL    │ │   │
│  │  │   ENGINE    │   │   MAGNETS   │   │  SEQUENCES  │   │   PRESENCE  │ │   │
│  │  │             │   │             │   │             │   │             │ │   │
│  │  │ Blog posts  │   │ PDF guides  │   │ Email       │   │ LinkedIn    │ │   │
│  │  │ LinkedIn    │   │ Templates   │   │ LinkedIn DM │   │ Twitter/X   │ │   │
│  │  │ Carousels   │   │ Calculators │   │ SMS follow  │   │ YouTube     │ │   │
│  │  │ Videos      │   │ Webinars    │   │ Voice drops │   │ Comments    │ │   │
│  │  │             │   │             │   │             │   │             │ │   │
│  │  │ AI-written  │   │ AI-built    │   │ AI-timed    │   │ AI-managed  │ │   │
│  │  └─────────────┘   └─────────────┘   └─────────────┘   └─────────────┘ │   │
│  │                                                                          │   │
│  │  [Skill: byker-content-factory] [byker-lead-magnet] [byker-outbound]    │   │
│  │                                                                          │   │
│  └─────────────────────────────────────────────────────────────────────────┘   │
│                                       │                                         │
│                                       ▼                                         │
│  ┌─────────────────────────────────────────────────────────────────────────┐   │
│  │                        CONVERSION LAYER                                  │   │
│  ├─────────────────────────────────────────────────────────────────────────┤   │
│  │                                                                          │   │
│  │  ┌─────────────┐   ┌─────────────┐   ┌─────────────┐   ┌─────────────┐ │   │
│  │  │   LEAD      │   │ DIAGNOSTIC  │   │   SALES     │   │  PROPOSAL   │ │   │
│  │  │   SCORING   │   │    CALL     │   │   AVATAR    │   │  GENERATOR  │ │   │
│  │  │             │   │             │   │             │   │             │ │   │
│  │  │ Behaviour   │   │ 30-min call │   │ AI video    │   │ Custom docs │ │   │
│  │  │ Engagement  │   │ 8 questions │   │ objection   │   │ Pricing     │ │   │
│  │  │ Fit score   │   │ Data pull   │   │ handling    │   │ Scope       │ │   │
│  │  │ Urgency     │   │ Quick win   │   │ Follow-up   │   │ Timeline    │ │   │
│  │  │             │   │             │   │             │   │             │ │   │
│  │  │ Auto-route  │   │ AI-assisted │   │ AI-powered  │   │ AI-written  │ │   │
│  │  └─────────────┘   └─────────────┘   └─────────────┘   └─────────────┘ │   │
│  │                                                                          │   │
│  │  [Auto-scoring]  [byker-client-diagnostic]  [byker-video-avatar]        │   │
│  │                                                                          │   │
│  └─────────────────────────────────────────────────────────────────────────┘   │
│                                       │                                         │
│                                       ▼                                         │
│  ┌─────────────────────────────────────────────────────────────────────────┐   │
│  │                        SERVICE DELIVERY LAYER                            │   │
│  ├─────────────────────────────────────────────────────────────────────────┤   │
│  │                                                                          │   │
│  │  ┌─────────────┐   ┌─────────────┐   ┌─────────────┐   ┌─────────────┐ │   │
│  │  │ ONBOARDING  │   │   CLIENT    │   │  SYSTEMS    │   │  HELPDESK   │ │   │
│  │  │   FLOW      │   │   PORTAL    │   │   BUILD     │   │   AVATAR    │ │   │
│  │  │             │   │             │   │             │   │             │ │   │
│  │  │ Welcome seq │   │ Dashboard   │   │ SOPs        │   │ 24/7 support│ │   │
│  │  │ Data intake │   │ Metrics     │   │ Automations │   │ FAQ answers │ │   │
│  │  │ Kickoff     │   │ Documents   │   │ Integrations│   │ Escalation  │ │   │
│  │  │ Expectations│   │ Comms       │   │ Training    │   │ Scheduling  │ │   │
│  │  │             │   │             │   │             │   │             │ │   │
│  │  │ AI-sequence │   │ Auto-update │   │ AI-created  │   │ AI-powered  │ │   │
│  │  └─────────────┘   └─────────────┘   └─────────────┘   └─────────────┘ │   │
│  │                                                                          │   │
│  │  [byker-client-onboarding]  [Dashboard]  [byker-sop-builder]            │   │
│  │                                              [byker-helpdesk-avatar]     │   │
│  └─────────────────────────────────────────────────────────────────────────┘   │
│                                       │                                         │
│                                       ▼                                         │
│  ┌─────────────────────────────────────────────────────────────────────────┐   │
│  │                        RETENTION LAYER                                   │   │
│  ├─────────────────────────────────────────────────────────────────────────┤   │
│  │                                                                          │   │
│  │  ┌─────────────┐   ┌─────────────┐   ┌─────────────┐   ┌─────────────┐ │   │
│  │  │   HEALTH    │   │   VALUE     │   │  EXPANSION  │   │   REFERRAL  │ │   │
│  │  │   SCORING   │   │   MOMENTS   │   │   SIGNALS   │   │   ENGINE    │ │   │
│  │  │             │   │             │   │             │   │             │ │   │
│  │  │ NPS surveys │   │ Win reports │   │ Growth cues │   │ Auto-ask    │ │   │
│  │  │ Usage data  │   │ Monthly ROI │   │ New service │   │ Testimonial │ │   │
│  │  │ Engagement  │   │ Milestones  │   │ fit scoring │   │ Case study  │ │   │
│  │  │ Risk alerts │   │ Celebrations│   │ Upsell seq  │   │ Incentives  │ │   │
│  │  │             │   │             │   │             │   │             │ │   │
│  │  │ Auto-flag   │   │ AI-generated│   │ AI-spotted  │   │ AI-managed  │ │   │
│  │  └─────────────┘   └─────────────┘   └─────────────┘   └─────────────┘ │   │
│  │                                                                          │   │
│  │  [byker-retention-engine]  [byker-gamification]                         │   │
│  │                                                                          │   │
│  └─────────────────────────────────────────────────────────────────────────┘   │
│                                                                                  │
├─────────────────────────────────────────────────────────────────────────────────┤
│                                                                                  │
│  ┌─────────────────────────────────────────────────────────────────────────┐   │
│  │                     ORCHESTRATION LAYER                                  │   │
│  ├─────────────────────────────────────────────────────────────────────────┤   │
│  │                                                                          │   │
│  │  ┌───────────────────────────────────────────────────────────────────┐  │   │
│  │  │               4 KILO INSTANCES (Specialised Agents)                │  │   │
│  │  ├───────────────────────────────────────────────────────────────────┤  │   │
│  │  │                                                                    │  │   │
│  │  │  ┌──────────┐  ┌──────────┐  ┌──────────┐  ┌──────────┐          │  │   │
│  │  │  │  KILO 1  │  │  KILO 2  │  │  KILO 3  │  │  KILO 4  │          │  │   │
│  │  │  │          │  │          │  │          │  │          │          │  │   │
│  │  │  │ CONTENT  │  │  CLIENT  │  │ SYSTEMS  │  │ BUSINESS │          │  │   │
│  │  │  │ & LEADS  │  │  DELIVERY│  │  & OPS   │  │ STRATEGY │          │  │   │
│  │  │  │          │  │          │  │          │  │          │          │  │   │
│  │  │  │ Content  │  │ Diagnose │  │ Build    │  │ Analyse  │          │  │   │
│  │  │  │ Outbound │  │ Onboard  │  │ Automate │  │ Plan     │          │  │   │
│  │  │  │ Social   │  │ Support  │  │ Document │  │ Coach    │          │  │   │
│  │  │  │ Nurture  │  │ Retain   │  │ Train    │  │ Review   │          │  │   │
│  │  │  └──────────┘  └──────────┘  └──────────┘  └──────────┘          │  │   │
│  │  │                                                                    │  │   │
│  │  │  [Skills: content-factory, lead-magnet, outbound-automation]       │  │   │
│  │  │  [Skills: client-diagnostic, client-onboarding, helpdesk-avatar]   │  │   │
│  │  │  [Skills: sop-builder, retention-engine, gamification]             │  │   │
│  │  │  [Skills: principles-coach, kilo-orchestrator]                     │  │   │
│  │  │                                                                    │  │   │
│  │  └───────────────────────────────────────────────────────────────────┘  │   │
│  │                                                                          │   │
│  │  ┌───────────────────────────────────────────────────────────────────┐  │   │
│  │  │              CUSTOM WORKFLOW ENGINE (AI-Controlled)               │  │   │
│  │  │                                                                    │  │   │
│  │  │  Triggers → Conditions → Actions → Logging → Notifications        │  │   │
│  │  │  [Python/FastAPI - No external dependencies, full AI control]     │  │   │
│  │  └───────────────────────────────────────────────────────────────────┘  │   │
│  │                                                                          │   │
│  └─────────────────────────────────────────────────────────────────────────┘   │
│                                                                                  │
└─────────────────────────────────────────────────────────────────────────────────┘
```

### Automation Inventory

Every automation in the agency, mapped to trigger and outcome:

| # | Automation | Trigger | Actions | Outcome | Skill Used |
|---|------------|---------|---------|---------|------------|
| 1 | Lead Capture | Form submit | Score → Segment → Sequence | Qualified lead | - |
| 2 | Content Queue | Calendar | Generate → Review → Publish | Daily content | content-factory |
| 3 | LinkedIn DM | Engagement | Draft → Personalise → Send | Warm outreach | outbound-automation |
| 4 | Diagnostic Prep | Call booked | Pull data → Pre-analyse → Brief | Ready for call | client-diagnostic |
| 5 | Welcome Sequence | Contract signed | 7-email series → Tasks → Portal | Onboarded client | client-onboarding |
| 6 | SOP Generation | Service start | Interview → Draft → Review | Working SOPs | sop-builder |
| 7 | Helpdesk Response | Support query | Classify → Draft → Escalate if needed | Fast support | helpdesk-avatar |
| 8 | Health Check | Monthly | Metrics → Score → Alert if low | Retention flag | retention-engine |
| 9 | Win Report | Milestone hit | Compile → Design → Send | Value proof | gamification |
| 10 | Referral Ask | NPS > 8 | Personalise → Send → Track | New leads | retention-engine |
| 11 | Upsell Signal | Usage pattern | Analyse → Draft → Queue | Growth revenue | retention-engine |
| 12 | Daily Digest | 7am | Compile → Format → Send | Owner awareness | - |

### Client Journey - Fully Automated Path

```
                                    PROSPECT
                                       │
                                       ▼
┌─────────────────────────────────────────────────────────────────────────────┐
│ AWARENESS                                                                    │
│ Sees content on LinkedIn/Google                                              │
│ [AI-written, auto-published via content-factory]                      │
└─────────────────────────────────────┬───────────────────────────────────────┘
                                      ▼
┌─────────────────────────────────────────────────────────────────────────────┐
│ INTEREST                                                                     │
│ Downloads lead magnet (guide, calculator, template)                         │
│ [AI-built via lead-magnet skill, auto-delivered]                         │
└─────────────────────────────────────┬───────────────────────────────────────┘
                                      ▼
┌─────────────────────────────────────────────────────────────────────────────┐
│ CONSIDERATION                                                                │
│ Receives nurture sequence, engages with content                             │
│ [Auto-scored for fit, AI-personalised emails via outbound-automation]       │
└─────────────────────────────────────┬───────────────────────────────────────┘
                                      ▼
┌─────────────────────────────────────────────────────────────────────────────┐
│ EVALUATION                                                                   │
│ Books diagnostic call, receives pre-call brief                              │
│ [client-diagnostic pulls data, generates brief automatically]               │
└─────────────────────────────────────┬───────────────────────────────────────┘
                                      ▼
┌─────────────────────────────────────────────────────────────────────────────┐
│ DECISION                                                                     │
│ Receives diagnostic report with quick wins and proposal                     │
│ [AI-generated report + video walkthrough + tiered proposal]                 │
└─────────────────────────────────────┬───────────────────────────────────────┘
                                      ▼
                                   CLIENT
                                      │
                                      ▼
┌─────────────────────────────────────────────────────────────────────────────┐
│ ONBOARDING                                                                   │
│ Signs → Welcome sequence → Data intake → Kickoff → Portal access            │
│ [Fully automated via client-onboarding, 7-email sequence]                   │
└─────────────────────────────────────┬───────────────────────────────────────┘
                                      ▼
┌─────────────────────────────────────────────────────────────────────────────┐
│ SERVICE DELIVERY                                                             │
│ SOPs built → Systems automated → Training provided → Helpdesk available     │
│ [sop-builder + helpdesk-avatar provide ongoing support]                     │
└─────────────────────────────────────┬───────────────────────────────────────┘
                                      ▼
┌─────────────────────────────────────────────────────────────────────────────┐
│ VALUE REALISATION                                                            │
│ Monthly reviews → Win reports → ROI tracking → Gamified progress            │
│ [retention-engine + gamification maintain engagement]                       │
└─────────────────────────────────────┬───────────────────────────────────────┘
                                      ▼
┌─────────────────────────────────────────────────────────────────────────────┐
│ ADVOCACY                                                                     │
│ NPS collected → Referral requested → Case study created → Testimonial       │
│ [Auto-triggered by satisfaction score, AI-managed sequence]                 │
└─────────────────────────────────────┴───────────────────────────────────────┘
                                      │
                                      ▼
                               REFERRAL → Back to AWARENESS
```

---

## Part 13: The Technical Implementation Stack

### Repository Structure

```
byker-agency/
├── README.md                     # This architecture document
├── .env.example                  # Environment variables template
├── docker-compose.yml            # Local development
│
├── backend/                      # FastAPI backend (Railway)
│   ├── main.py                   # App entry point
│   ├── requirements.txt
│   ├── api/
│   │   ├── __init__.py
│   │   ├── routes/
│   │   │   ├── leads.py          # Lead management endpoints
│   │   │   ├── clients.py        # Client management
│   │   │   ├── content.py        # Content generation
│   │   │   ├── diagnostics.py    # Diagnostic flows
│   │   │   └── webhooks.py       # External webhook handlers
│   │   └── middleware/
│   │       ├── auth.py
│   │       └── rate_limit.py
│   ├── services/
│   │   ├── llm_router.py         # Multi-provider orchestration
│   │   ├── diagnostic_engine.py  # 48-hour diagnostic logic
│   │   ├── content_generator.py  # Content factory logic
│   │   └── email_service.py      # Transactional email
│   ├── models/
│   │   ├── lead.py
│   │   ├── client.py
│   │   └── content.py
│   └── utils/
│       ├── embeddings.py         # Vector operations
│       └── cost_tracker.py       # LLM spend monitoring
│
├── dashboard/                    # React client portal (Railway)
│   ├── package.json
│   ├── src/
│   │   ├── App.tsx
│   │   ├── components/
│   │   │   ├── ClientDashboard.tsx
│   │   │   ├── DiagnosticReport.tsx
│   │   │   ├── ProgressTracker.tsx
│   │   │   └── MetricsChart.tsx
│   │   └── pages/
│   │       ├── Login.tsx
│   │       ├── Dashboard.tsx
│   │       └── Documents.tsx
│   └── vite.config.ts
│
├── workflows/                    # Python workflow modules
│   ├── __init__.py
│   ├── lead_capture.py          # Lead scoring and routing
│   ├── content_publish.py       # Content queue to social
│   ├── diagnostic_prep.py       # Pre-call data gathering
│   ├── onboarding_sequence.py   # Welcome email series
│   ├── health_check.py          # Monthly client health
│   └── daily_digest.py          # Morning summary email
│
├── skills/                       # Byker skills (symlink to vault)
│   └── (all 12 skills)
│
├── scripts/                      # Utility scripts
│   ├── setup_ollama.sh          # Install and configure Ollama
│   ├── seed_database.py         # Initial data setup
│   └── export_obsidian.py       # Sync vault to system
│
└── railway.json                  # Railway configuration
```

### API Endpoints Design

```
/api/v1/
│
├── /leads
│   ├── POST /capture            # New lead from form/webhook
│   ├── GET /                    # List all leads
│   ├── GET /{id}                # Get lead details
│   ├── POST /{id}/score         # Trigger scoring
│   └── POST /{id}/nurture       # Start nurture sequence
│
├── /clients
│   ├── GET /                    # List clients
│   ├── GET /{id}                # Client details
│   ├── GET /{id}/metrics        # Client metrics dashboard
│   ├── POST /{id}/diagnostic    # Run new diagnostic
│   └── GET /{id}/documents      # Client documents
│
├── /content
│   ├── POST /generate           # Generate content
│   ├── GET /queue               # Content queue
│   ├── POST /publish            # Publish to platform
│   └── GET /performance         # Content analytics
│
├── /diagnostics
│   ├── POST /                   # Start diagnostic flow
│   ├── GET /{id}                # Get diagnostic status
│   ├── POST /{id}/questions     # Submit answers
│   └── GET /{id}/report         # Get final report
│
├── /llm
│   ├── POST /complete           # LLM completion (routed)
│   ├── POST /embed              # Generate embeddings
│   └── GET /usage               # Usage statistics
│
└── /webhooks
    ├── POST /workflow           # Internal workflow trigger
    ├── POST /calendly           # Meeting booked
    ├── POST /stripe             # Payment events
    └── POST /typeform           # Form submissions
```

---

## Part 14: The Design Philosophy

### Why This Architecture Works

**1. Separation of Concerns**

Each layer has a single responsibility:
- Acquisition layer brings people in
- Conversion layer turns them into clients
- Delivery layer serves them
- Retention layer keeps them
- Orchestration layer coordinates everything

**2. Progressive Automation**

Not everything automated at once. Priority:
1. High-volume, low-value tasks first (lead capture, content publishing)
2. Time-consuming tasks second (diagnostic prep, SOP drafting)
3. Judgment tasks last (still human-in-loop for proposals, strategy)

**3. Fail-Safe Design**

Every automation has:
- Manual override capability
- Alert on failure
- Fallback to human escalation
- Audit log for debugging

**4. Cost Awareness**

The system knows the cost of every LLM call and:
- Routes to cheapest capable model
- Alerts when spend exceeds threshold
- Provides ROI on automation investment
- Uses local LLMs for development/bulk work

**5. Data Sovereignty**

All client data stays in:
- Your Obsidian vault (local, encrypted)
- Your PostgreSQL database (Railway, you control)
- Local embeddings where possible

No data sent to third parties unnecessarily.

### The Ingenious Parts

**1. The LLM Cascade**

Instead of one expensive model for everything, the system intelligently routes:
- Quick questions → Local Qwen (free)
- Bulk processing → DeepSeek (cheap)
- Client work → Claude (quality)

Result: Same quality output, 70% cost reduction.

**2. The 4-Kilo Architecture**

Four specialised agents, each with context about their domain:
- Kilo 1 knows your content strategy, hook library, audience
- Kilo 2 knows your clients, their history, their pain points
- Kilo 3 knows your systems, SOPs, integrations
- Kilo 4 knows your business strategy, principles, goals

Each agent maintains context window focused on their domain.

**3. Obsidian as Source of Truth**

Everything syncs back to Obsidian:
- Client notes ← CRM data
- Content ideas ← Social engagement
- Decisions ← Strategy sessions
- SOPs ← System builds

Your brain grows, the system learns, nothing is lost.

**4. Custom Workflow Engine**

AI-controlled Python code replaces visual tools:
- Website form → Workflow engine → CRM → Nurture sequence
- Calendar booking → Workflow engine → Brief generated
- Content approved → Workflow engine → Social APIs → Tracking

Fully AI-readable, modifiable, debuggable. No external dependencies.

---

## Part 15: Implementation - Detailed Steps

### Week 1: Foundation

#### Day 1: Obsidian Setup

```bash
# 1. Install Obsidian from DMG in Downloads
open /Users/$(whoami)/Downloads/Obsidian*.dmg

# 2. Create vault location
mkdir -p ~/Documents/Byker-Vault

# 3. Open Obsidian, create vault at this location

# 4. Create folder structure (in Obsidian)
# Use Templater or manual creation
```

Obsidian folder creation script (run in Obsidian terminal or manually):
```
00-INBOX
10-CLIENTS/_templates
10-CLIENTS/active
10-CLIENTS/archive
20-KNOWLEDGE/frameworks
20-KNOWLEDGE/smb-expertise
20-KNOWLEDGE/industry-benchmarks
20-KNOWLEDGE/case-studies
30-CONTENT/ideas
30-CONTENT/drafts
30-CONTENT/ready-to-publish
30-CONTENT/published
30-CONTENT/templates
40-OPERATIONS/sops
40-OPERATIONS/checklists
40-OPERATIONS/metrics
40-OPERATIONS/decisions
50-SYSTEMS/skills
50-SYSTEMS/automations
50-SYSTEMS/integrations
50-SYSTEMS/ai-prompts
60-REFERENCE/docs
60-REFERENCE/resources
60-REFERENCE/templates
90-META/daily-notes
90-META/weekly-reviews
```

#### Day 2: Plugin Installation

Install these community plugins:
1. Smart Connections
2. Copilot
3. Dataview
4. Templater
5. Tasks
6. Periodic Notes
7. Git

#### Day 3-4: Ollama Setup

```bash
# Install Ollama
curl -fsSL https://ollama.com/install.sh | sh

# Pull recommended models
ollama pull qwen2.5:7b          # 4.4GB - general purpose
ollama pull llama3.1:8b         # 4.7GB - reasoning
ollama pull nomic-embed-text    # 274MB - embeddings
ollama pull codellama:7b        # 3.8GB - code (optional)

# Test Ollama is running
ollama list
curl http://localhost:11434/api/tags

# Configure Smart Connections to use Ollama
# Settings → Smart Connections → Model: ollama
# Chat Model: qwen2.5:7b
# Embedding Model: nomic-embed-text
```

#### Day 5-7: Cloud API Configuration

```bash
# Create .env file for API keys
cat > ~/Documents/Byker-Vault/50-SYSTEMS/.env << 'EOF'
# LLM Providers
ANTHROPIC_API_KEY=sk-ant-...
GEMINI_API_KEY=...
QWEN_API_KEY=...
DEEPSEEK_API_KEY=...

# Services
DATABASE_URL=postgres://...
RAILWAY_TOKEN=...
WORKFLOW_SECRET=...

# Local
OLLAMA_HOST=http://localhost:11434
EOF
```

### Week 2: Railway Deployment

```bash
# Login to Railway
railway login

# Create new project
railway init --name byker-agency

# Add services
railway add --service api
railway add --service dashboard
railway add --plugin postgresql

# Deploy backend
cd backend
railway up

# Deploy dashboard
cd ../dashboard
railway up

# Workflows deploy with main backend
```

### Week 3-4: Workflow Building

Python workflow modules to build (in order):

1. **Lead Capture** - Form → Score → CRM → Sequence
2. **Content Publish** - Queue → Format → API → Log
3. **Diagnostic Prep** - Booking → Data Pull → Brief
4. **Onboarding** - Contract → Welcome → Portal → Tasks
5. **Health Check** - Monthly → Metrics → Score → Alert
6. **Daily Digest** - 7am → Compile → Send

---

## Summary

This architecture delivers:

**For You (Ewan):**
- Single source of truth (Obsidian)
- Automated lead generation and nurturing
- AI-assisted client delivery
- Cost-optimised LLM usage
- Time back in your day

**For Your Clients:**
- Faster onboarding
- Better support (24/7 AI helpdesk)
- Clear documentation (auto-generated SOPs)
- Measurable value (automated reporting)
- Gamified progress

**For the Business:**
- Scalable without proportional effort increase
- Resilient (multiple fallbacks)
- Cost-effective (local LLMs for 70% of work)
- Data sovereign (you own everything)
- Future-proof (modular, replaceable components)

Total estimated setup time: 4 weeks
Total estimated monthly cost: £80-220
Expected ROI: If it saves 10 hours/week at £100/hr = £4,000/month saved

---

## Part 16: Dalio Principles - The Governing Framework

**Everything in this system is governed by Ray Dalio's Principles.** This isn't decoration - it's the operating system.

### Core Principles Applied

**1. Radical Transparency**

Every decision, every metric, every failure is logged and visible:

```python
class PrinciplesEngine:
    """Dalio-style decision logging and review."""

    async def log_decision(
        self,
        decision: str,
        context: dict,
        options_considered: list,
        chosen_option: str,
        reasoning: str,
        outcome: str = None  # Filled in later
    ):
        """Log every significant decision for review."""
        entry = {
            "timestamp": datetime.now(),
            "decision": decision,
            "context": context,
            "options": options_considered,
            "chosen": chosen_option,
            "reasoning": reasoning,
            "outcome": outcome,
            "principle_applied": self.identify_principle(reasoning)
        }
        await self.decision_log.insert(entry)

        # If pattern emerges, suggest new principle
        similar = await self.find_similar_decisions(decision)
        if len(similar) > 3:
            await self.suggest_principle(similar)
```

**2. Idea Meritocracy**

The best idea wins, regardless of source:

- AI suggestions get same weight as human input
- Client feedback systematically collected and weighted
- Team disagreements logged and resolved by evidence

```python
IDEA_EVALUATION_FRAMEWORK = {
    "criteria": [
        "Does data support this?",
        "What's the downside if wrong?",
        "Who has relevant expertise?",
        "Has this worked elsewhere?",
        "What would falsify this?"
    ],
    "weighting": {
        "evidence_quality": 0.4,
        "expertise_relevance": 0.3,
        "track_record": 0.2,
        "reversibility": 0.1
    }
}
```

**3. Believability-Weighted Decision Making**

Not all opinions are equal:

```python
BELIEVABILITY_WEIGHTS = {
    # Domain expertise matters
    "cash_flow": {
        "accountant": 0.9,
        "business_owner": 0.7,
        "ai_analysis": 0.8,
        "general_opinion": 0.3
    },
    "marketing": {
        "marketing_specialist": 0.9,
        "business_owner": 0.6,
        "ai_analysis": 0.7,
        "general_opinion": 0.2
    },
    "operations": {
        "ops_manager": 0.9,
        "frontline_staff": 0.8,  # They see reality
        "business_owner": 0.5,
        "ai_analysis": 0.6
    }
}
```

**4. Pain + Reflection = Progress**

Every problem is a learning opportunity:

```
PROBLEM OCCURS
      │
      ▼
┌─────────────┐
│ LOG THE     │
│ PROBLEM     │
│ (what, when,│
│  impact)    │
└──────┬──────┘
       ▼
┌─────────────┐
│ ROOT CAUSE  │
│ ANALYSIS    │
│ (5 whys)    │
└──────┬──────┘
       ▼
┌─────────────┐
│ IDENTIFY    │
│ PRINCIPLE   │
│ (or create) │
└──────┬──────┘
       ▼
┌─────────────┐
│ UPDATE      │
│ SYSTEM      │
│ (prevent    │
│  recurrence)│
└──────┬──────┘
       ▼
┌─────────────┐
│ ADD TO      │
│ DECISION    │
│ LOG         │
└─────────────┘
```

**5. The Machine**

The business is a machine. Diagnose it like one:

```python
MACHINE_DIAGNOSIS_FRAMEWORK = {
    "inputs": [
        "leads",
        "capital",
        "team_hours",
        "client_needs"
    ],
    "processes": [
        "lead_conversion",
        "service_delivery",
        "client_retention",
        "content_creation"
    ],
    "outputs": [
        "revenue",
        "profit",
        "client_satisfaction",
        "referrals"
    ],
    "diagnosis_questions": [
        "Which input is constrained?",
        "Which process is slowest?",
        "Which output is underperforming?",
        "Where is the actual bottleneck vs perceived?"
    ]
}
```

### Principles-Driven Client Work

Every client engagement follows Dalio's framework:

**Diagnostic Phase**
1. What are the facts? (Data extraction)
2. What is the current machine? (Process mapping)
3. Where is it broken? (Gap analysis)
4. What's the root cause? (5 whys)
5. What principle applies? (Framework matching)

**Recommendation Phase**
1. What are all options? (Idea generation)
2. Believability-weight the input (Expert consultation)
3. What's the expected value of each? (Analysis)
4. What would prove us wrong? (Pre-mortem)
5. What's the minimum viable test? (De-risk)

**Implementation Phase**
1. Log the decision (Transparency)
2. Set clear metrics (Accountability)
3. Schedule review points (Feedback loops)
4. Document learnings (Principles growth)

### The Decision Journal

Obsidian folder: `40-OPERATIONS/decisions/`

Every significant decision gets a note:

```markdown
# Decision: [Title]
Date: [date]
Status: [Pending/Decided/Reviewed]

## Context
[What situation prompted this decision?]

## Options Considered
1. [Option A] - [Pros/Cons]
2. [Option B] - [Pros/Cons]
3. [Option C] - [Pros/Cons]

## Chosen Option
[Which option and why]

## Believability Input
- [Expert 1]: [Their view] (Weight: X)
- [Expert 2]: [Their view] (Weight: X)
- [AI Analysis]: [View] (Weight: X)

## Principle Applied
[Which Dalio principle guided this?]

## Expected Outcome
[What we expect to happen]

## Review Date
[When to assess outcome]

---

## Actual Outcome (added later)
[What actually happened]

## Learning
[What principle does this reinforce or create?]
```

### Automated Principles Enforcement

The system enforces principles automatically:

```python
class PrinciplesGuard:
    """Ensure all operations follow Dalio principles."""

    async def before_client_recommendation(self, recommendation: dict):
        """Check recommendation against principles."""
        checks = {
            "has_data_support": self.check_evidence(recommendation),
            "considered_alternatives": len(recommendation.get("alternatives", [])) >= 2,
            "identified_risks": "risks" in recommendation,
            "has_test_criteria": "success_metrics" in recommendation,
            "reversibility_assessed": "exit_strategy" in recommendation
        }

        if not all(checks.values()):
            return {
                "approved": False,
                "missing": [k for k, v in checks.items() if not v],
                "action": "Complete missing elements before proceeding"
            }
        return {"approved": True}

    async def after_problem_occurs(self, problem: dict):
        """Ensure problem leads to learning."""
        required_actions = [
            "Log problem to decision journal",
            "Complete 5 whys analysis",
            "Identify or create applicable principle",
            "Update system to prevent recurrence",
            "Schedule retrospective review"
        ]
        await self.create_problem_workflow(problem, required_actions)
```

### Weekly Principles Review

Every week, the system prompts:

1. **What decisions were made?** → Review decision log
2. **What went wrong?** → Review problem log
3. **What patterns emerged?** → AI analysis of logs
4. **What principles need updating?** → Evolve the framework
5. **What got better?** → Celebrate progress

This is automated via the workflow engine:

```python
async def weekly_principles_review():
    """Sunday evening review prompt."""
    decisions = await get_decisions_this_week()
    problems = await get_problems_this_week()
    patterns = await ai_analyse_patterns(decisions, problems)

    review_doc = generate_weekly_review(
        decisions=decisions,
        problems=problems,
        patterns=patterns,
        suggested_principle_updates=patterns.get("suggestions", [])
    )

    await save_to_obsidian(
        path="90-META/weekly-reviews/",
        filename=f"week-{datetime.now().isocalendar().week}.md",
        content=review_doc
    )

    await notify_owner(
        subject="Weekly Principles Review Ready",
        body="Your review is in Obsidian. 10 minutes to get better."
    )
```

### The Principles Hierarchy

```
┌─────────────────────────────────────────────────────────────────────────┐
│                       BYKER PRINCIPLES HIERARCHY                         │
├─────────────────────────────────────────────────────────────────────────┤
│                                                                          │
│  LEVEL 1: META-PRINCIPLES (Never change)                                 │
│  ┌────────────────────────────────────────────────────────────────────┐ │
│  │ • Radical transparency                                              │ │
│  │ • Idea meritocracy                                                  │ │
│  │ • Pain + reflection = progress                                      │ │
│  │ • The business is a machine to be diagnosed                         │ │
│  │ • Believability-weighted decision making                            │ │
│  └────────────────────────────────────────────────────────────────────┘ │
│                                                                          │
│  LEVEL 2: OPERATIONAL PRINCIPLES (Evolve slowly)                         │
│  ┌────────────────────────────────────────────────────────────────────┐ │
│  │ • Give value first, always (Ziglar)                                 │ │
│  │ • Permission before persuasion (Godin)                              │ │
│  │ • Address real pain, don't create false urgency (Cialdini white hat)│ │
│  │ • 48-hour diagnostic, not 48-day                                    │ │
│  │ • Automate what's automatable, human what's not                     │ │
│  └────────────────────────────────────────────────────────────────────┘ │
│                                                                          │
│  LEVEL 3: TACTICAL PRINCIPLES (Update regularly)                         │
│  ┌────────────────────────────────────────────────────────────────────┐ │
│  │ • Use local LLMs for 70% of tasks                                   │ │
│  │ • Claude for client-facing quality                                  │ │
│  │ • Always have 3 options before deciding                             │ │
│  │ • Test with one client before scaling                               │ │
│  │ • [Your principles here - grow over time]                           │ │
│  └────────────────────────────────────────────────────────────────────┘ │
│                                                                          │
│  LEVEL 4: SITUATIONAL PRINCIPLES (Client/context specific)               │
│  ┌────────────────────────────────────────────────────────────────────┐ │
│  │ • For plumbers: Focus on payment collection first                   │ │
│  │ • For service businesses: SOPs before marketing                     │ │
│  │ • For lifestyle businesses: Owner time before growth                │ │
│  │ • [Grows with every client engagement]                              │ │
│  └────────────────────────────────────────────────────────────────────┘ │
│                                                                          │
└─────────────────────────────────────────────────────────────────────────┘
```

### How This Changes Everything

**Without Principles:**
- Make decisions ad hoc
- Repeat mistakes
- Inconsistent client experience
- Knowledge stays in your head
- Growth = more work

**With Principles:**
- Decisions are systematic
- Mistakes become improvements
- Consistent, scalable experience
- Knowledge captured in system
- Growth = machine improvement

The entire Byker system - every skill, every workflow, every client interaction - runs through this principles framework. It's not an add-on. It's the operating system.

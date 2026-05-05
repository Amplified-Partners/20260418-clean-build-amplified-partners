---
title: "Cover.AI Infrastructure Audit"
id: "covered-infra-audit-jan2026-v1"
version: 1
created: "2026-04-25"
type: "document"
topic_type: "audit"
audience: "internal"
layer: "truth"
status: "filed"
signed_by: "Devon, 2026-04-25, devin-992682c244cf444f91e0a516498afbfd"
---

# Cover.AI Infrastructure Audit
## Railway | AI/LLM | Obsidian
**Date:** January 15, 2026 | **Status:** COMPLETE

---

# EXECUTIVE SUMMARY

| Component | Status | Capacity | Action Needed |
|-----------|--------|----------|---------------|
| **Railway** | ✅ Active | 4 projects configured | Clean up duplicate linking |
| **AI/LLM Stack** | ✅ Operational | 8+ models available | Set spending limits |
| **Obsidian Vault** | ✅ Structured | 7 folders ready | Populate Qdrant docs |

**Overall:** Infrastructure is solid. Ready for Cover.AI operations.

---

# PART 1: RAILWAY DEPLOYMENT

## 1.1 Projects Configured

| Project | Path | Environment | Status |
|---------|------|-------------|--------|
| **byker-production** | `~/` | production | ✅ Primary API |
| **covered-ai** | `~/Documents/Baselayer/baselayer-core/covered-ai` | production | ✅ Marketing site |
| **byker-production** | `~/Downloads/byker-production` | production | ⚠️ Duplicate (service: null) |
| **evrything everywhere** | `~/Knowledge/.data/scripts` | production | 🔍 Experimental |

## 1.2 Active Services

### byker-production (Main API)
- **URL:** https://byker-production-production.up.railway.app
- **Docs:** https://byker-production-production.up.railway.app/docs
- **Source:** `~/Projects/byker-production/`
- **Cost Control:** $50/day limit

**Endpoints Available:**
| Category | Endpoints |
|----------|-----------|
| Core | `/health`, `/status`, `/generate` |
| Workflows | `/workflows`, `/workflows/execute`, `/workflows/resume` |
| Decisions | `/decisions` (CRUD) |
| Principles | `/principles`, `/principles/check` |
| Analytics | `/analytics/patterns`, `/analytics/weekly-review`, `/analytics/metrics` |
| Obsidian | `/obsidian/initialize`, `/obsidian/queries` |

### covered-ai (Marketing)
- **Location:** `~/Documents/Baselayer/baselayer-core/covered-ai`
- **Status:** Active
- **Purpose:** Client-facing marketing site

## 1.3 Railway CLI Status

```bash
# Linked from home directory
railway status  # → byker-production
railway logs    # → View live logs
railway open    # → Dashboard
```

## 1.4 Capacity Assessment

| Metric | Current | Limit | Notes |
|--------|---------|-------|-------|
| Projects | 4 | Unlimited | Pro plan |
| Services | 3 active | Per project | byker has multi-service |
| Deploy frequency | On demand | No limit | GitHub triggers available |
| Resource usage | Variable | $50/day cap | Set via dashboard |

## 1.5 Recommended Actions

- [ ] **Remove duplicate** `~/Downloads/byker-production` linking (5 min)
- [ ] **Verify** covered-ai deployment working (2 min)
- [ ] **Document** evrything everywhere purpose or sunset (15 min)

---

# PART 2: AI & LLM STACK

## 2.1 Cloud APIs

| Provider | Models | Monthly Cost | Status |
|----------|--------|--------------|--------|
| **Anthropic** | Claude Sonnet 4.5, Claude Max | £24-80 | ✅ Active |
| **Perplexity** | Sonar (research) | £8-24 | ✅ Active |
| **OpenAI** | GPT-4o | £16-80 | ⚠️ .env.save exposed |
| **Google** | Gemini | £0-8 | ⚠️ Key exposed |
| **OpenRouter** | 100+ models | Variable | ✅ Active |

**Total Monthly:** £48-192 (current usage)

## 2.2 Local AI (Ollama)

### Installed Models

| Model | Size | Purpose | Use Case |
|-------|------|---------|----------|
| **llama3.1** | 8.37 GB | General reasoning | Fallback/local testing |
| **llama3.2** | 8.37 GB | General reasoning | Fallback/local testing |
| **qwen2.5** | 4.58 GB | Fast inference | Quick queries |
| **qwen2.5-coder** | 1.88 GB | Code generation | Local code assist |
| **nomic-embed-text** | 262 MB | Embeddings | RAG/vector search |

**Total Storage:** 23.5 GB

### Commands
```bash
ollama list          # Show installed models
ollama run llama3.2  # Interactive chat
ollama pull <model>  # Download new model
```

## 2.3 Kilo Code Configuration

**Location:** `~/.kilocode/`

### 10 Specialized Modes
| Mode | Symbol | Purpose |
|------|--------|---------|
| prebuilt-finder | 🔍 | Find existing solutions first |
| architect | 🏗️ | System design |
| code | 💻 | Implementation |
| test-engineer | 🧪 | Testing |
| debugger | 🐛 | Troubleshooting |
| frontend | 🎨 | React/TypeScript/CSS |
| backend | ⚙️ | API/database |
| docs | 📝 | Documentation |
| security | 🔒 | Security audit |
| performance | ⚡ | Optimization |

### Workflow Pattern
```
1. /mode prebuilt-finder → Find existing solutions
2. /mode architect → Design with found solutions
3. /mode code → Implement
4. /mode test-engineer → Write tests
5. /mode security → Security audit
```

### API Configuration
- **Primary:** OpenRouter (100+ models)
- **Fallback:** Anthropic Direct
- **Cheapest:** MiniMax M2.1

## 2.4 Claude Integration

### Claude Max (Subscription)
- **Access:** claude.ai / Desktop app
- **Purpose:** Primary AI assistant
- **Projects:** 22+ SMB diagnostic skills loaded

### Claude Code (Terminal)
- **Access:** `claude` command
- **Purpose:** Terminal-based coding
- **MCP Servers:** 5 configured

## 2.5 Production Assets

### Interior Design System
- **Location:** `~/Downloads/interior-design-system/`
- **Status:** Production SaaS
- **Value:** £24,000-60,000/year
- **AI:** 6 Claude agents (Discovery, Style, Product, Space, Budget, Orchestrator)
- **Vector DB:** ChromaDB (self-hosted)
- **Embeddings:** sentence-transformers (all-MiniLM-L6-v2)

### Lead Engine
- **Location:** `~/Downloads/lead-engine/`
- **Status:** Beta/Testing
- **Value:** £0 → £30,000-180,000/year potential
- **AI:** Claude (diagnosis) + Perplexity (research)
- **Database:** SQLAlchemy + SQLite

### Agentic Workflow
- **Location:** `~/Downloads/agentic_workflow/`
- **Status:** Configured but disabled
- **AI:** Google Gemini
- **Action:** Decide: activate or sunset

## 2.6 Security Issues (URGENT)

| Issue | Location | Risk | Fix Time |
|-------|----------|------|----------|
| ⚠️ OpenAI key in .env.save | melanin-design-platform | HIGH | 5 min |
| ⚠️ Gemini key exposed | agentic_workflow/.env.example | HIGH | 5 min |
| ⚠️ No spending limits | All providers | MEDIUM | 15 min |

### Immediate Actions
```bash
# Delete exposed credentials
rm ~/Downloads/melanin-design-platform/backend/.env.save

# Set spending limits (do via dashboards):
# - Anthropic: £80/month
# - OpenAI: £80/month  
# - Perplexity: £40/month
```

## 2.7 Capacity Assessment

| Capability | Current | Potential | Notes |
|------------|---------|-----------|-------|
| Concurrent AI calls | 10+ | 50+ | OpenRouter handles routing |
| Local inference | Yes | Yes | 23GB models installed |
| Code generation | Fast | Very fast | Kilo Code 10 modes |
| Embeddings | Local | Local | nomic-embed-text ready |
| Research | Real-time | Real-time | Perplexity integrated |

---

# PART 3: OBSIDIAN VAULT

## 3.1 Structure

**Root:** `~/vault/`

| Folder | Purpose | Contents |
|--------|---------|----------|
| `_inbox-personal/` | Personal inbox | Empty (ready) |
| `_inbox-work/` | Work inbox | Empty (ready) |
| `_inbox-uncategorised/` | Triage inbox | Empty (ready) |
| `infra-ai-stack/` | AI documentation | 2 files |
| `knowledge-qdrant/` | Qdrant docs | 2 placeholder files |
| `personal/` | Personal notes | Empty (ready) |
| `work-covered-ai/` | Cover.AI docs | 1 file |

## 3.2 Documentation Status

### Complete ✅
| File | Location | Purpose |
|------|----------|---------|
| infra-ai-stack-overview-v1.md | infra-ai-stack/ | AI stack reference |
| infra-railway-byker-v1.md | infra-ai-stack/ | Railway API docs |
| coaches-system-v1.md | work-covered-ai/ | 5 coaching personas |

### Placeholder (Need Content)
| File | Location | Action |
|------|----------|--------|
| knowledge-qdrant-collections-v1.md | knowledge-qdrant/ | Add collections when created |
| knowledge-qdrant-pipelines-v1.md | knowledge-qdrant/ | Add pipelines when created |

## 3.3 Integration with Byker API

Byker API has Obsidian endpoints:
- `POST /obsidian/initialize` - Initialize vault structure
- `GET /obsidian/queries` - Dataview queries

## 3.4 Capacity Assessment

| Feature | Status | Notes |
|---------|--------|-------|
| Folder structure | ✅ Ready | 7 folders organized |
| Naming convention | ✅ Defined | area-topic-purpose-v1.md |
| AI stack docs | ✅ Complete | 2 files |
| Qdrant docs | ⏳ Placeholder | Waiting for collections |
| Work docs | ⏳ Minimal | 1 coaching file |

---

# PART 4: QUICK REFERENCE

## Essential Commands

```bash
# Railway
railway status          # Check deployment
railway logs            # View logs
railway open            # Dashboard

# Ollama
ollama list             # Show models
ollama run qwen2.5      # Fast local chat
ollama run llama3.2     # Full reasoning

# Kilo Code
kilocode                # Start coding agent
/mode list              # Show modes
/mode prebuilt-finder   # Start workflow

# Claude
claude                  # Terminal agent

# Byker API
curl https://byker-production-production.up.railway.app/health
curl https://byker-production-production.up.railway.app/status
```

## Key URLs

| Service | URL |
|---------|-----|
| Byker API | https://byker-production-production.up.railway.app |
| API Docs | https://byker-production-production.up.railway.app/docs |
| Railway | https://railway.app |
| Anthropic | https://console.anthropic.com |
| OpenAI | https://platform.openai.com |
| Perplexity | https://www.perplexity.ai/settings/api |

## File Locations

| What | Path |
|------|------|
| Vault | `~/vault/` |
| Projects | `~/Projects/` |
| Byker source | `~/Projects/byker-production/` |
| Interior Design | `~/Downloads/interior-design-system/` |
| Lead Engine | `~/Downloads/lead-engine/` |
| Railway config | `~/.railway/config.json` |
| Ollama models | `~/.ollama/models/` |
| Kilo Code | `~/.kilocode/` |

---

# PART 5: ACTION ITEMS

## Today (15 minutes)

- [ ] Delete exposed .env.save files
- [ ] Set £80/month limits on all AI providers
- [ ] Verify Byker API health check passes

## This Week (2 hours)

- [ ] Remove duplicate Railway project linking
- [ ] Decide on Melanin Platform (keep/sunset)
- [ ] Decide on Agentic Workflow (activate/sunset)
- [ ] Populate Qdrant collections documentation

## This Month (8 hours)

- [ ] Launch Lead Engine beta
- [ ] Setup response caching (save £16-40/month)
- [ ] First 3-5 Cover.AI clients
- [ ] Complete vault documentation

---

**Audit Complete:** ✅  
**Infrastructure Status:** Operational  
**Ready for Cover.AI:** Yes

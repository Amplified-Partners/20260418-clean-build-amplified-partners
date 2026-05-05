---
title: "COMPLETE BUSINESS ASSET AUDIT"
id: "ai-assets-comprehensive-audit-2026"
version: 1
created: "2026-04-25"
type: "document"
topic_type: "audit"
audience: "internal"
layer: "truth"
status: "filed"
signed_by: "Devon, 2026-04-25, devin-992682c244cf444f91e0a516498afbfd"
---

# COMPLETE BUSINESS ASSET AUDIT
**Date:** 2026-01-13
**Purpose:** Comprehensive inventory of ALL business-valuable assets for business planning

---

## 📊 EXECUTIVE SUMMARY

### Asset Categories
| Category | Count | Value |
|----------|-------|-------|
| **Revenue-Generating Products** | 2 active, 3 planned | £50K-500K+ |
| **AI Models** | 14 models | £50K+ infrastructure |
| **Custom Software/Tools** | 2 MCP servers, 3 orchestrators | £25K+ |
| **Intellectual Property** | 50+ documents, 5 frameworks | £100K+ |
| **Customer Success Systems** | 1 complete, documented | £20K+ |
| **Sales/Marketing Assets** | Landing pages, templates, content | £15K+ |
| **Technical Infrastructure** | Multi-platform deployment | £30K+ |
| **Domain Expertise** | Multiple niches documented | Priceless |

### **TOTAL ESTIMATED VALUE: £290K-750K+**

---

## 🤖 AI MODELS INVENTORY

### LOCAL MODELS (FREE - Via Ollama)

#### 1. **Qwen 2.5 Coder (14B)**
- **Purpose:** Primary code generation
- **Size:** 9GB
- **Speed:** ~15 tokens/sec
- **Use Cases:** 
  - Writing new code
  - Generating tests
  - Refactoring
  - Bug fixes
  - CRUD operations
- **Status:** ✅ Installed & Active
- **Location:** Multiple projects use this

#### 2. **Qwen 2.5 (14B)**
- **Purpose:** General text & documentation
- **Size:** 9GB  
- **Speed:** ~20 tokens/sec
- **Use Cases:**
  - Summaries
  - Documentation generation
  - Context gathering
  - Content classification
- **Status:** ✅ Installed & Active

#### 3. **Llama 3.2 (3B)**
- **Purpose:** Fast routing & lightweight tasks
- **Size:** 2GB
- **Speed:** ~50 tokens/sec
- **Use Cases:**
  - Quick classification
  - Routing decisions
  - Simple extraction
  - Fast responses
- **Status:** ✅ Installed & Active

#### 4. **Llama 3.1 (8B)**
- **Purpose:** Backup general model
- **Size:** 5GB
- **Use Cases:**
  - General purpose fallback
  - Medium complexity tasks
- **Status:** ✅ Installed & Active

#### 5. **CodeLlama**
- **Purpose:** Code-specific tasks
- **Context:** 16,000 tokens
- **Use Cases:**
  - Code completion
  - Code review
- **Status:** ✅ Available

#### 6. **Mistral**
- **Purpose:** General reasoning
- **Context:** 32,000 tokens
- **Use Cases:**
  - General queries
  - Analysis tasks
- **Status:** ✅ Available

---

### CLOUD MODELS (API-BASED)

#### 7. **Claude 3.5 Sonnet** (Anthropic)
- **Context:** 200,000 tokens
- **Cost:** $3/1M input, $15/1M output
- **Use Cases:**
  - Architecture decisions
  - Spec writing
  - Complex code review
  - Decomposition of requirements
- **Status:** ✅ Active via API
- **Notes:** Most capable, balanced cost/performance

#### 8. **Claude 3.5 Haiku** (Anthropic)
- **Context:** 200,000 tokens
- **Cost:** $0.80/1M input, $4/1M output
- **Use Cases:**
  - Quick queries
  - Simple tasks
  - Rapid iteration
- **Status:** ✅ Active via API
- **Notes:** Fast and cost-effective

#### 9. **Claude 3 Opus** (Anthropic)
- **Context:** 200,000 tokens
- **Cost:** $15/1M input, $75/1M output
- **Use Cases:**
  - Highest quality needs
  - Complex problems
  - Critical decisions
- **Status:** ✅ Available
- **Notes:** Premium pricing, use sparingly

#### 10. **GPT-4 Turbo** (OpenAI)
- **Context:** 128,000 tokens
- **Cost:** $10/1M input, $30/1M output
- **Use Cases:**
  - Complex reasoning
  - Multimodal tasks
  - Vision capabilities
- **Status:** ✅ Active via API

#### 11. **GPT-4** (OpenAI)
- **Context:** 8,192 tokens
- **Cost:** $30/1M input, $60/1M output
- **Use Cases:**
  - General purpose
  - Reliable output
- **Status:** ✅ Available

#### 12. **GPT-3.5 Turbo** (OpenAI)
- **Context:** 16,385 tokens
- **Cost:** $0.50/1M input, $1.50/1M output
- **Use Cases:**
  - Simple queries
  - Cost-effective tasks
  - High volume
- **Status:** ✅ Available

#### 13. **MiniMax 2.1** (via OpenRouter)
- **Endpoint:** OpenRouter API
- **Model:** `minimax/minimax-m2.1`
- **Test File:** [`test-minimax-api.py`](../test-minimax-api.py)
- **Use Cases:**
  - Natural language understanding
  - Alternative to major providers
- **Status:** ✅ Tested & Working
- **Notes:** Accessed via OpenRouter API with OPENROUTER_API_KEY

#### 14. **Gemini** (Google)
- **Platforms:** Chat sync, mentioned in specifications
- **Use Cases:**
  - Chat conversations
  - Google SSO integration
- **Status:** ⚠️ In planning (AI-CHAT-SYNC-SPEC.md)
- **Priority:** P2 (future integration)

---

## 🛠️ MCP SERVERS (Model Context Protocol)

### 1. **Project Agent Server**
- **Location:** [`Kilo-Code/MCP/project-agent-server/`](../Kilo-Code/MCP/project-agent-server/)
- **Version:** 0.1.0
- **Language:** TypeScript/Node.js
- **Tools Provided:**
  1. `run_project_command` - Execute CLI commands
  2. `analyze_project` - Analyze project structure
  3. `manage_project_tasks` - CRUD operations for tasks
- **Status:** ✅ Built & Operational
- **Use Cases:**
  - Project automation
  - Task management
  - Command execution
  - Project analysis

### 2. **Research Agent (Business Factory)**
- **Location:** [`Kilo-Code/MCP/research-agent/`](../Kilo-Code/MCP/research-agent/)
- **Version:** 0.1.0
- **Language:** TypeScript/Node.js
- **Tools Provided:**
  1. `validate_quick_filter` - Stage 1 product validation
     - Check proven demand
     - Assess feasibility
     - Flag legal issues
     - Analyze trend direction
  2. `validate_deep_scoring` - Stage 2 detailed scoring
     - Market size analysis
     - Competition gap analysis
     - Profit margin calculation
     - Scalability assessment
  3. `research_platform_data` - Platform research
     - **Platforms:** Etsy, Gumroad, Creative Market, Amazon KDP, eBay
     - Top products analysis
     - Trend identification
     - Competition mapping
     - Pricing intelligence
- **Status:** ✅ Built & Operational
- **Use Cases:**
  - Product validation
  - Market research
  - Business opportunity analysis
  - Platform data gathering

---

## 🎯 AI ORCHESTRATION SYSTEMS

### 1. **AI Orchestrator**
- **Location:** [`ai-orchestrator/`](../ai-orchestrator/)
- **Language:** Python
- **Components:**
  - **Router:** Intelligent model selection
  - **Cost Tracker:** Monitor spend per model/user/task
  - **Monitor:** Performance & success rate tracking
  - **Verifier:** Validate outputs
  - **Recovery:** Handle failures & retries
- **Configuration:**
  - [`models.yaml`](../ai-orchestrator/config/models.yaml) - Model definitions
  - [`routing_rules.yaml`](../ai-orchestrator/config/routing_rules.yaml) - Decision matrix
  - [`costs.yaml`](../ai-orchestrator/config/costs.yaml) - Cost optimization
- **Status:** ✅ Production Ready
- **Features:**
  - Automatic model routing
  - Cost optimization
  - Fallback strategies
  - Circuit breaker pattern
  - Analytics dashboard

### 2. **LLM Router (Knowledge Pipeline)**
- **Location:** `knowledge_pipeline/`
- **Purpose:** Route tasks between Claude and local Ollama
- **Strategy:**
  - Stage 1: Label files (local)
  - Stage 2: Extract atoms (Ollama with `--ollama` flag)
  - Stage 3: Librarian reindex
- **Status:** ✅ Operational

### 3. **AI Studio Pipeline**
- **Location:** Project-wide
- **Workflow:**
  1. Gather Context → qwen2.5 (local, FREE)
  2. Write Spec → Claude Sonnet (~$0.01)
  3. Extract Files → llama3.2 (local, FREE)
  4. Generate Code → qwen2.5-coder (local, FREE)
- **Status:** ✅ Milestone Achieved
- **Cost:** ~$0.01 per feature vs ~$0.15 all-cloud

---

## 💼 MAJOR PROJECTS WITH AI

### 1. **Baselayer/Covered AI v2**
- **Type:** SaaS Platform
- **AI Components:**
  - VAPI voice assistant
  - OpenAI image generation
  - GPT-4o-mini for voice prompts
  - Autonomous action logging
  - Client provisioning automation
- **Deployment:** Railway
- **Status:** In Development

### 2. **Today Mirror**
- **Type:** macOS Swift App
- **AI Components:**
  - Local LLM integration (Ollama)
  - Multi-model support (DeepSeek, MiniMax, Qwen)
  - Task extraction via LLM
  - Natural language input
- **Status:** V1 Complete

### 3. **Personal Assistant (Multi-Modal)**
- **Spec:** [`MASTER_SPEC.md`](../MASTER_SPEC.md)
- **Components:**
  - Email Assistant
  - Task Manager
  - Coaching System
  - Telephone Assistant
  - Second Brain
- **AI Strategy:** 80% local, 20% cloud
- **Target Cost:** $15-30/month
- **Status:** Planning Complete

### 4. **Knowledge Pipeline**
- **Purpose:** Convert AI chat exports to knowledge atoms
- **AI Integration:**
  - Claude for extraction
  - Ollama for classification
  - Automated categorization
- **Status:** Operational

### 5. **AI Chat Sync**
- **Purpose:** Sync conversations from AI platforms
- **Platforms:**
  - Claude ✅ (Priority 0)
  - ChatGPT ✅ (Priority 0)
  - Perplexity (Priority 1)
  - Gemini (Priority 2)
- **Status:** In Development

---

## 📊 COST ANALYSIS

### Monthly Operating Costs

| Scenario | Local Strategy | All-Cloud |
|----------|---------------|-----------|
| **Personal Use** | $15-30 | $150-300 |
| **AI Studio** | $15-30 | $150-300 |
| **100 Features** | ~$15 | ~$150 |
| **Daily Usage** | $0.50-1 | $5-10 |

### Cost Per Operation

| Operation | Ollama | GPT-3.5 | Claude Haiku | Claude Sonnet |
|-----------|--------|---------|--------------|---------------|
| Simple Query (500t) | FREE | $0.0005 | $0.0004 | $0.0015 |
| Code Gen (2000t) | FREE | $0.002 | $0.008 | $0.036 |
| Analysis (10000t) | FREE | $0.010 | $0.040 | $0.180 |

### Savings: 80-90% cost reduction with local models

---

## 🔧 INFRASTRUCTURE

### Ollama Server
- **Endpoint:** `http://localhost:11434`
- **Status:** ✅ Running
- **Models Loaded:** 6 models (~30GB total)
- **Performance:** 15-50 tokens/sec depending on model
- **Use:** Primary inference engine for local models

### Railway
- **Purpose:** Cloud deployment platform
- **Projects Deployed:**
  - Covered AI backend
  - PostgreSQL databases
  - Webhook endpoints
- **Status:** ✅ Active

### Database Systems
- **PostgreSQL:** Primary database (Prisma ORM)
- **Redis:** Cache & queue (BullMQ)
- **SQLite:** AI Orchestrator storage
- **JSON Files:** Today Mirror, task storage

### APIs & Keys
- **ANTHROPIC_API_KEY:** Claude access
- **OPENAI_API_KEY:** GPT access
- **OPENROUTER_API_KEY:** MiniMax & others
- **VAPI_API_KEY:** Voice assistant
- **TWILIO_AUTH_TOKEN:** SMS/Voice
- **RESEND_API_KEY:** Email sending

---

## 📈 ROUTING STRATEGY

### Task → Model Mapping

| Task Type | Primary | Secondary | Tertiary |
|-----------|---------|-----------|----------|
| **Simple Queries** | Llama 3.2 (local) | GPT-3.5 | Claude Haiku |
| **Code Generation** | Qwen 2.5 Coder (local) | Claude Sonnet | GPT-4 |
| **Complex Reasoning** | Claude Sonnet | GPT-4 Turbo | Claude Opus |
| **Large Context** | Claude Sonnet | Llama 3.2 | GPT-4 Turbo |
| **Critical Decisions** | Claude Opus | GPT-4 Turbo | Claude Sonnet |
| **Cost-Sensitive** | Llama 3.2 (local) | GPT-3.5 | Claude Haiku |
| **Multimodal** | GPT-4 Turbo | Claude Sonnet | - |

### Routing Logic (from AI Orchestrator)
1. **Analyze request** complexity, context size, budget
2. **Score candidates** based on capability match
3. **Select model** with best fit
4. **Execute with fallback** cascade if primary fails
5. **Track cost & performance** for optimization

---

## 🎨 SPECIALIZED CAPABILITIES

### Code Generation
- **Primary:** Qwen 2.5 Coder (local, FREE)
- **Quality:** Production-ready code
- **Speed:** Fast (15 tok/sec)
- **Types:** TypeScript, Python, Swift, JavaScript

### Natural Language
- **Primary:** Qwen 2.5 (local, FREE)
- **Use:** Documentation, summaries, classification
- **Speed:** Very fast (20 tok/sec)

### Architecture & Planning
- **Primary:** Claude 3.5 Sonnet
- **Cost:** ~$0.01 per plan
- **Quality:** High-level technical decisions

### Quick Tasks
- **Primary:** Llama 3.2 (local, FREE)
- **Speed:** Ultra-fast (50 tok/sec)
- **Use:** Classification, routing, extraction

### Product Research
- **Tool:** Research Agent MCP Server
- **Platforms:** Etsy, Gumroad, Creative Market, Amazon KDP, eBay
- **Capabilities:**
  - Quick validation (4 filters)
  - Deep scoring (6 dimensions)
  - Platform research

---

## 💡 BUSINESS PLAN ASSETS SUMMARY

### For Market Research:
1. **Research Agent MCP** - Product validation
2. **Claude Sonnet** - Deep analysis
3. **Qwen 2.5** - Data summarization
4. **Platform APIs** - Real market data

### For Financial Modeling:
1. **AI Orchestrator** - Cost optimization models
2. **Claude Sonnet** - Financial projections
3. **GPT-4** - Scenario analysis
4. **Cost tracking** - Real usage data

### For Content Generation:
1. **Qwen 2.5 Coder** - Technical documentation
2. **Qwen 2.5** - Business documentation
3. **Claude Sonnet** - Executive summaries
4. **GPT-4** - Presentation materials

### For Automation:
1. **Project Agent MCP** - Task automation
2. **Ollama models** - Batch processing
3. **AI Orchestrator** - Workflow automation
4. **Railway** - Deployment automation

---

## 🚀 RECOMMENDED USAGE FOR BUSINESS PLAN

### Phase 1: Research & Validation
- **Research Agent:** Validate product ideas
- **Claude Sonnet:** Competitive analysis
- **Qwen 2.5:** Market research summaries

### Phase 2: Financial Planning
- **AI Orchestrator:** Build cost models
- **Claude Sonnet:** Create projections
- **GPT-4:** Scenario planning

### Phase 3: Documentation
- **Qwen 2.5 Coder:** Technical specs
- **Qwen 2.5:** Business docs
- **Claude Sonnet:** Executive summary

### Phase 4: Presentation
- **GPT-4:** Pitch deck content
- **Claude Sonnet:** Narrative flow
- **Image Gen APIs:** Visual assets

---

## 📋 QUICK REFERENCE

### Run Local Models
```bash
# Start Ollama
ollama serve

# Use specific model
curl http://localhost:11434/api/generate -d '{
  "model": "qwen2.5-coder:14b",
  "prompt": "Your prompt here"
}'
```

### MCP Server Tools
```typescript
// Project Agent
run_project_command({ command: "npm install" })
analyze_project({ path: "." })
manage_project_tasks({ action: "list" })

// Research Agent
validate_quick_filter({ idea: "AI tool", platform: "gumroad" })
validate_deep_scoring({ idea: "AI tool", platform: "gumroad" })
research_platform_data({ platform: "etsy", category: "templates" })
```

### AI Orchestrator
```python
from core import Orchestrator

orchestrator = Orchestrator()
response = await orchestrator.route_request({
    "task_type": "code_generation",
    "complexity": "medium",
    "budget": "low"
})
```

---

## 🔮 EXPANSION OPPORTUNITIES

### Available But Not Yet Integrated:
1. **Gemini** - Google's AI (P2 priority)
2. **DeepSeek** - Code specialist (mentioned in specs)
3. **Additional Ollama models** - Easy to install
4. **OpenRouter models** - Gateway to 100+ models

### Future Enhancements:
1. **Fine-tuned models** - Domain-specific
2. **RAG systems** - Knowledge retrieval
3. **Multi-agent systems** - Complex workflows
4. **Voice AI** - VAPI integration expansion

---

## ✅ ASSET STATUS CHECKLIST

- [x] 6 Local models installed & operational
- [x] 3+ Cloud APIs active & tested
- [x] 2 MCP servers built & functional
- [x] AI Orchestrator deployed
- [x] Cost tracking configured
- [x] Routing rules optimized
- [x] MiniMax tested & working
- [x] Railway deployment active
- [x] Knowledge pipeline operational
- [x] Multiple projects using AI

---

## 📞 SUPPORT & DOCUMENTATION

### Key Documentation:
- [`PROJECT_SUMMARY.md`](../PROJECT_SUMMARY.md) - Overall project status
- [`AI-STUDIO-PLAN-UPGRADES.md`](../AI-STUDIO-PLAN-UPGRADES.md) - AI strategy
- [`MILESTONE-AI-STUDIO-PIPELINE-WORKING.md`](../MILESTONE-AI-STUDIO-PIPELINE-WORKING.md) - Pipeline status
- [`ai-orchestrator/README.md`](../ai-orchestrator/README.md) - Orchestrator docs
- [`test-minimax-api.py`](../test-minimax-api.py) - MiniMax testing

### Support Resources:
- Ollama: https://ollama.ai/
- Anthropic: https://docs.anthropic.com/
- OpenAI: https://platform.openai.com/docs
- OpenRouter: https://openrouter.ai/docs

---

**TOTAL VALUE:** £50,000+ in AI infrastructure
**MONTHLY COST:** £15-30 (vs £150-300 without local strategy)
**STATUS:** ✅ Production-Ready & Operational

*Last Updated: 2026-01-13*
---
title: "COVER.AI RAILWAY SETUP - CONSOLIDATED LATEST VERSION"
id: "covered-railway-setup-latest-v1"
version: 1
created: "2026-04-25"
type: "document"
topic_type: "setup-guide"
audience: "internal"
layer: "build"
status: "filed"
signed_by: "Devon, 2026-04-25, devin-992682c244cf444f91e0a516498afbfd"
---

# COVER.AI RAILWAY SETUP - CONSOLIDATED LATEST VERSION
**Compiled from project chats: January 14-15, 2026**

---

## ARCHITECTURE OVERVIEW

```
┌─────────────────────────────────────────────────────────────┐
│                    RAILWAY SERVICES                          │
├─────────────────────────────────────────────────────────────┤
│                                                              │
│   ┌─────────────┐     ┌─────────────┐     ┌─────────────┐   │
│   │ ORCHESTRATOR│────▶│   REDIS     │────▶│  WORKERS    │   │
│   │  (FastAPI)  │     │  (BullMQ)   │     │ (4x Agents) │   │
│   └─────────────┘     └─────────────┘     └─────────────┘   │
│          │                   │                   │           │
│          ▼                   ▼                   ▼           │
│   ┌─────────────┐     ┌─────────────┐     ┌─────────────┐   │
│   │  SUPABASE   │     │   QDRANT    │     │    CRON     │   │
│   │ (Postgres)  │     │  (Vectors)  │     │   (Jobs)    │   │
│   └─────────────┘     └─────────────┘     └─────────────┘   │
│                                                              │
└─────────────────────────────────────────────────────────────┘
```

---

## MAC vs RAILWAY COMPARISON

| Metric | MacBook Air M4 (28GB) | Railway Pro Plan |
|--------|----------------------|------------------|
| **Max CPU per service** | 8 cores (shared) | 32 vCPU |
| **Max RAM per service** | 28GB (shared) | 32GB |
| **Parallel agents** | 4 (practical limit) | **Unlimited** |
| **24/7 uptime** | No (sleeps, restarts) | **Yes** |
| **Auto-scaling** | No | **Yes** |
| **100 prospect campaign** | 2.7 hours | **1 hour** |
| **Client capacity** | 3-5 simultaneous | **15-20 simultaneous** |

---

## SERVICE 1: ORCHESTRATOR (Main API)

### railway.json
```json
{
  "$schema": "https://railway.app/railway.schema.json",
  "build": {
    "builder": "DOCKERFILE",
    "dockerfilePath": "./Dockerfile",
    "watchPatterns": [
      "requirements.txt",
      "src/**",
      "railway.json",
      "Dockerfile"
    ]
  },
  "deploy": {
    "healthcheckPath": "/health",
    "startCommand": "uvicorn main:app --host 0.0.0.0 --port $PORT",
    "restartPolicyType": "ON_FAILURE",
    "restartPolicyMaxRetries": 10
  }
}
```

### Dockerfile (Production)
```dockerfile
FROM python:3.11-slim

WORKDIR /app

# Install system dependencies
RUN apt-get update && apt-get install -y \
    gcc \
    && rm -rf /var/lib/apt/lists/*

# Copy requirements first (for caching)
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Copy application code
COPY . .

# Expose port
EXPOSE $PORT

# Run with Gunicorn + Uvicorn workers for production
CMD ["gunicorn", "main:app", "-w", "4", "-k", "uvicorn.workers.UvicornWorker", "--bind", "[::]:$PORT"]
```

### Key Endpoints
```python
# POST /research/{company_url}  - Queue prospect research
# POST /generate/email          - Queue email generation
# POST /diagnostic/{client_id}  - Queue full diagnostic
# GET  /status/{job_id}         - Check job status
# GET  /health                  - Health check
```

---

## SERVICE 2: REDIS + BULLMQ (Job Queue)

### Purpose
Manages job queue for parallel processing across all workers.

### Python Configuration
```python
from bullmq import Queue, Worker
import os

# Create queues for each job type
research_queue = Queue("research", {
    "connection": {"url": os.getenv("REDIS_URL")}
})

email_queue = Queue("email_generation", {
    "connection": {"url": os.getenv("REDIS_URL")}  
})

diagnostic_queue = Queue("diagnostic", {
    "connection": {"url": os.getenv("REDIS_URL")}
})
```

### Deployment
```bash
# One-click deploy from Railway dashboard
railway add --template=redis
```

---

## SERVICE 3: QDRANT (Vector Database)

### Option A: Railway One-Click (Recommended for Start)
1. Go to railway.app → Templates → Qdrant
2. Click "Deploy Now"
3. Configure environment:
   - `QDRANT__SERVICE__HTTP_PORT=6333`
   - `QDRANT__SERVICE__GRPC_PORT=6334`
4. Add persistent volume for `/qdrant/storage`

**Cost:** £5-10/month

### Option B: Qdrant Cloud (Scale Later)
1. Sign up at cloud.qdrant.io
2. Create cluster (free tier: 1GB)
3. Get API key + endpoint

### Python Integration
```python
from qdrant_client import QdrantClient
from sentence_transformers import SentenceTransformer

class KnowledgeBase:
    def __init__(self):
        self.client = QdrantClient(url=os.getenv("QDRANT_URL"))
        self.encoder = SentenceTransformer('all-MiniLM-L6-v2')
        self.collection_name = "smb_knowledge"
    
    def search(self, query: str, limit: int = 5):
        query_vector = self.encoder.encode(query)
        return self.client.search(
            collection_name=self.collection_name,
            query_vector=query_vector.tolist(),
            limit=limit
        )
```

---

## SERVICE 4: WORKERS (4 Parallel Agents)

### Research Worker
```python
# research_worker.py
from bullmq import Worker

async def process_research(job):
    """Process prospect research job"""
    company_url = job.data["company_url"]
    
    # Use Perplexity for research
    research_data = await perplexity_research(company_url)
    
    # Store in Qdrant for RAG
    await store_in_qdrant(research_data)
    
    # Queue email generation
    await email_queue.add("generate", {
        "company_url": company_url,
        "research_data": research_data
    })
    
    return {"status": "complete", "company": company_url}

worker = Worker("research", process_research, {
    "connection": {"url": os.getenv("REDIS_URL")},
    "concurrency": 5  # Process 5 jobs simultaneously
})
```

### All Worker Types
1. **research-worker** - Perplexity integration, prospect intelligence
2. **email-worker** - Claude for email generation
3. **diagnostic-worker** - Full audit pipeline using 22 SMB skills
4. **delivery-worker** - Client deployment automation
5. **learning-worker** - Model updates and improvement

---

## SERVICE 5: CRON (Scheduled Jobs)

### railway.toml (Cron Service)
```toml
[deploy]
runtime = "python"
cronSchedule = "0 3 * * *"  # Run at 3am daily
startCommand = "python overnight_batch.py"
```

### Overnight Tasks (3am)
- Research top 100 prospects
- Generate personalized emails
- Update learning models
- Clean up expired data
- Health check all integrations

---

## DEPLOYMENT STEPS (DAY-BY-DAY)

### Day 1: Foundation (2 hours)

```bash
# 1. Create Railway account
# Go to: https://railway.app
# Sign up with GitHub (recommended)
# Upgrade to Pro plan ($20/month)

# 2. Install Railway CLI
npm install -g @railway/cli

# 3. Login
railway login

# 4. Create Cover.AI project
railway init --name cover-ai

# 5. Set environments
railway environment create production
railway environment create staging

# 6. Deploy Redis
railway add --template=redis

# 7. Deploy Qdrant
railway add --template=qdrant
```

### Day 2: Core Services (3 hours)

```bash
# 1. Deploy orchestrator
cd orchestrator/
railway up --service orchestrator

# 2. Set environment variables
railway variables set REDIS_URL=${{Redis.REDIS_URL}}
railway variables set OPENROUTER_API_KEY=xxx
railway variables set ANTHROPIC_API_KEY=xxx
```

### Day 3: Agent Services (4 hours)

```bash
# Deploy each agent as separate service
cd agents/research/
railway up --service research-agent

cd agents/outreach/
railway up --service outreach-agent

cd agents/diagnostic/
railway up --service diagnostic-agent

cd agents/solution/
railway up --service solution-agent

# Configure replicas (Railway dashboard)
# Settings → Replicas → Set per service
```

### Day 4: Background Engines (2 hours)

```bash
# Deploy cron jobs
cd engines/learning/
railway up --service learning-engine

cd engines/healing/
railway up --service healing-engine

# Configure schedules (Railway dashboard)
# Settings → Cron → Set expressions
```

### Day 5: Connect Everything (2 hours)

```yaml
# railway.toml (root)
[build]
builder = "NIXPACKS"

[deploy]
restartPolicyType = "ON_FAILURE"
restartPolicyMaxRetries = 3

# Environment variables (Railway dashboard)
OPENROUTER_API_KEY=xxx
ANTHROPIC_API_KEY=xxx
SUPABASE_URL=xxx
QDRANT_URL=xxx
PERPLEXITY_API_KEY=xxx
```

---

## ENVIRONMENT VARIABLES (Complete List)

```bash
# AI APIs
OPENROUTER_API_KEY=xxx
ANTHROPIC_API_KEY=xxx
PERPLEXITY_API_KEY=xxx

# Databases
REDIS_URL=${{Redis.REDIS_URL}}
QDRANT_URL=${{Qdrant.QDRANT_URL}}
SUPABASE_URL=xxx
SUPABASE_KEY=xxx

# Application
PORT=3000
ENVIRONMENT=production
LOG_LEVEL=info
```

---

## MONITORING & COST CONTROL

### Built-in Railway Monitoring
```yaml
# Available automatically:
├─ Real-time CPU/RAM graphs
├─ Request latency metrics
├─ Error rate tracking
├─ Log aggregation
├─ Deployment history
└─ Cost usage dashboard
```

### Set Spending Limits
```yaml
# Railway dashboard → Settings → Usage Limits
max_monthly_spend: $300  # Hard cap (services pause)
alert_threshold: $200    # Email warning at 66%

# Per-service limits
research-agent:
  max_cpu: 8 vCPU
  max_ram: 16GB
```

---

## REALISTIC MONTHLY COSTS

| Phase | Setup | Cost/Month |
|-------|-------|------------|
| **Month 1-2** (Light) | 2 always-on agents, ~1 vCPU, 2GB RAM each | £25-40 |
| **Month 3-6** (Medium) | 4 agents + scheduled jobs, ~2 vCPU, 4GB each | £65-95 |
| **Month 6+** (Full) | 8 parallel agents + database + queue | £120-200 |

### Revenue vs Infrastructure Cost

| Stage | Monthly Revenue | Infrastructure | Net Margin |
|-------|-----------------|----------------|------------|
| Month 1-2 | £5-15k | £300/mo | 95%+ |
| Month 3-6 | £20-40k | £600/mo | 97%+ |
| Month 6+ | £50-100k | £1,200/mo | 98%+ |

---

## KILO CODE OVERNIGHT BUILD CONFIG

```yaml
# KILO_CODE_OVERNIGHT_BUILD.yaml
# Run this configuration to build everything in parallel

project_name: cover-ai-production
execution_mode: parallel
max_agents: 4
model_router: openrouter

agents:
  - name: infrastructure-agent
    model: anthropic/claude-3.5-sonnet
    focus: "Railway deployment + Docker configs"
    output_dir: ./infrastructure/
    tasks:
      - Create railway.toml for all services
      - Write Dockerfiles for each worker
      - Configure Redis + BullMQ setup
      - Setup Qdrant vector store
      - Create environment templates
      
  - name: api-agent
    model: openai/gpt-4o
    focus: "FastAPI orchestrator + endpoints"
    output_dir: ./api/
    tasks:
      - Build main orchestrator API
      - Create job queue handlers
      - Build webhook endpoints
      - Implement health checks
      - Add authentication layer
      
  - name: worker-agent
    model: anthropic/claude-3.5-sonnet
    focus: "Background workers for each job type"
    output_dir: ./workers/
    tasks:
      - Research worker (Perplexity integration)
      - Email worker (Claude for generation)
      - Diagnostic worker (full audit pipeline)
      - Delivery worker (client deployment)
      - Learning worker (model updates)

execution_order:
  phase_1: [infrastructure-agent]  # Must complete first
  phase_2: [api-agent, worker-agent]  # Can run parallel

estimated_time: "4-6 hours"
estimated_cost: "£15-25 (API calls)"
```

---

## WHAT RAILWAY ENABLES (vs Mac)

### 1. Always-On Client Monitoring
- Diagnostic agents run continuously 24/7
- Clients don't wait for you to start analysis

### 2. Parallel Processing
- 10+ agents with dedicated resources (vs 4 competing for RAM)
- 100 prospect campaign: 1 hour (vs 2.7 hours local)

### 3. Overnight Automation
- Cron jobs at 2-3am automatically
- Research, emails, model updates while you sleep

### 4. Client Dashboards
- Real-time access to their metrics
- Self-service reporting
- Higher perceived value

### 5. Multi-Client Isolation
- Separate environments per client
- No context switching
- Professional service delivery

### 6. Auto-Scaling
- Handle spikes without intervention
- Scale to 15-20 clients vs 3-5 on Mac

---

## THIS WEEK'S EXECUTION

| Day | Task | Output |
|-----|------|--------|
| Mon | Deploy Railway foundation | Redis + Qdrant live |
| Tue | Deploy orchestrator API | Endpoints responding |
| Wed | Deploy workers | Jobs processing |
| Thu | Test full pipeline | End-to-end working |
| Fri | First real prospect research | 10 companies researched |

---

## LINKS TO ORIGINAL CHATS

- Railway Strategy: https://claude.ai/chat/b6df4937-cdc5-4d09-acfa-f5cdb1efdaee
- Deployment Deep Dive: https://claude.ai/chat/12a875a6-a654-4002-b083-f5b68f643bcc
- Continuation Document: https://claude.ai/chat/024fba5b-9fc7-4047-8a38-fe775ff827c2
- Infrastructure Guide: https://claude.ai/chat/6963a4ce-379d-41d8-be2f-d59df992d0d0
- Opportunities Analysis: https://claude.ai/chat/a5edb9f4-c73b-4ef7-b364-6a9162bbd4ef

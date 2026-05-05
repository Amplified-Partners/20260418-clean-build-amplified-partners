---
title: "AI Studio Plan Upgrades v2"
id: "plan-ai-studio-upgrades-v2"
version: 1
created: "2026-04-25"
type: "document"
topic_type: "unsorted"
audience: "internal"
layer: "shadow"
status: "filed"
signed_by: "Devon, 2026-04-25, devin-992682c244cf444f91e0a516498afbfd"
---

# AI Studio Plan Upgrades v2

**Date:** 2024-12-14  
**Status:** Approved for execution

---

## Executive Summary

Revised the original AI Studio plan to **maximize local model usage** and **minimize Claude API costs**. Claude now handles only reasoning tasks (~20% of work). Code generation runs FREE on local models.

---

## Upgrade 1: Optimal Model Routing

### Before (Wasteful)
```
Claude (paid) → Architecture, Specs, Novel Code, Code Review
KiloCode      → Refactors, Tests (fictional - not installed)
Qwen          → CRUD, Summaries
```

### After (Optimal)
```
Claude (paid) → Architecture, Specs, Complex Review, Decisions ONLY
qwen2.5-coder → ALL code generation, tests, refactors, CRUD
qwen2.5       → Summaries, documentation, classification
llama3.2      → Fast routing decisions, simple extraction
```

### Model Allocation Matrix

| Task Type | Model | Location | Cost | Speed |
|-----------|-------|----------|------|-------|
| **REASONING** | | | | |
| Architecture decisions | Claude Max | API | Included | — |
| Spec writing & decomposition | Claude Max | API | Included | — |
| Complex code review (logic) | Claude Haiku | API | ~$0.001/review | Fast |
| Breaking down requirements | Claude Max | API | Included | — |
| **CODE GENERATION** | | | | |
| Writing new code | qwen2.5-coder:14b | Local | FREE | ~15 tok/s |
| Generating tests | qwen2.5-coder:14b | Local | FREE | ~15 tok/s |
| Refactoring | qwen2.5-coder:14b | Local | FREE | ~15 tok/s |
| CRUD/boilerplate | qwen2.5-coder:14b | Local | FREE | ~15 tok/s |
| Bug fixes | qwen2.5-coder:14b | Local | FREE | ~15 tok/s |
| **SUPPORT** | | | | |
| Summaries/docs | qwen2.5:14b | Local | FREE | ~20 tok/s |
| Context gathering | qwen2.5:14b | Local | FREE | ~20 tok/s |
| Quick classification | llama3.2:3b | Local | FREE | ~50 tok/s |
| Routing decisions | llama3.2:3b | Local | FREE | ~50 tok/s |

### Cost Impact

| Scenario | Original Plan | Optimized Plan |
|----------|---------------|----------------|
| 100 features built | ~$150 Claude | ~$15 Claude |
| Daily usage | ~$5-10/day | ~$0.50-1/day |
| Monthly burn | ~$150-300 | ~$15-30 |

---

## Upgrade 2: Backend Database

### Before
- MongoDB (from hagopj13 boilerplate)
- Document-based, less suited for relational SaaS data

### After
- **PostgreSQL** 
- Native Railway support (managed Postgres)
- Better for: multi-tenancy, teams, permissions, audit logs
- Prisma ORM works with both frontend and backend

### Implementation
- Use same Prisma schema across frontend/backend
- Railway provisions managed Postgres automatically
- No MongoDB dependency

---

## Upgrade 3: Agent Architecture (Simplified Start)

### Before
- 5 agents from day 1 (over-engineered)
- All agents active immediately

### After (Phased)

**Phase 1 (Now):**
- SpecWriter agent (Claude → writes specs)
- Coder agent (qwen2.5-coder → writes code)
- Basic PR creation

**Phase 2 (Week 2):**
- Reviewer agent (Claude → reviews logic)
- Test generation (qwen2.5-coder)

**Phase 3 (Week 3+):**
- Researcher agent (context gathering)
- Archivist agent (docs/atoms)

### Rationale
Ship working pipeline fast. Add sophistication iteratively.

---

## Upgrade 4: LLM Router Implementation

### New Component: `/agents/src/tools/llm_router.py`

```python
class LLMRouter:
    """Routes tasks to optimal model based on task type."""
    
    ROUTING_TABLE = {
        # Reasoning tasks → Claude
        "architecture": ("claude", "claude-3-5-sonnet"),
        "spec_writing": ("claude", "claude-3-5-sonnet"),
        "complex_review": ("claude", "claude-3-5-haiku"),
        "decomposition": ("claude", "claude-3-5-sonnet"),
        
        # Code tasks → Local qwen2.5-coder
        "code_generation": ("ollama", "qwen2.5-coder:14b"),
        "test_generation": ("ollama", "qwen2.5-coder:14b"),
        "refactoring": ("ollama", "qwen2.5-coder:14b"),
        "bug_fix": ("ollama", "qwen2.5-coder:14b"),
        "crud": ("ollama", "qwen2.5-coder:14b"),
        
        # Support tasks → Local general models
        "summarization": ("ollama", "qwen2.5:14b"),
        "documentation": ("ollama", "qwen2.5:14b"),
        "classification": ("ollama", "llama3.2"),
        "routing": ("ollama", "llama3.2"),
    }
    
    def route(self, task_type: str, prompt: str) -> str:
        backend, model = self.ROUTING_TABLE[task_type]
        if backend == "claude":
            return self._call_claude(model, prompt)
        else:
            return self._call_ollama(model, prompt)
```

---

## Upgrade 5: Local Model Fleet

### Installed Models

| Model | Size | Purpose | Status |
|-------|------|---------|--------|
| qwen2.5-coder:14b | 9GB | Primary code generation | ✅ Installing |
| qwen2.5:14b | 9GB | Summaries, docs | ✅ Ready |
| llama3.2:3b | 2GB | Fast routing, classification | ✅ Ready |
| llama3.1:8b | 5GB | Backup general model | ✅ Ready |

### Ollama Endpoints

```bash
# All models available at:
http://localhost:11434/api/generate

# Example call:
curl http://localhost:11434/api/generate -d '{
  "model": "qwen2.5-coder:14b",
  "prompt": "Write a TypeScript function that...",
  "stream": false
}'
```

---

## Upgrade 6: Revised Boilerplate Selection

### Frontend (Unchanged)
- **boxyhq/saas-starter-kit** (Apache 2.0)
- Already uses Prisma (works with Postgres)
- Keep as-is

### Backend (Revised)

**Option A: Lighter Start**
- Don't use a heavy boilerplate
- Scaffold minimal Express + Prisma + BullMQ
- Add only what we need

**Option B: Keep hagopj13 but swap DB**
- Use the structure
- Replace Mongoose → Prisma + Postgres
- ~2 hours migration

**Decision:** Option A – lighter, faster, less cruft.

### Backend Structure (Minimal)
```
/backend
├── src/
│   ├── routes/          # Express routes
│   ├── services/        # Business logic
│   ├── workers/         # BullMQ processors
│   ├── prisma/          # Shared schema
│   └── index.ts
├── Dockerfile
└── package.json
```

---

## Upgrade 7: CI/CD Simplification

### Before
- 3 workflow files
- Complex matrix builds

### After
- Single `ci.yml` with job matrix
- Deploy jobs conditional on path changes

```yaml
# .github/workflows/ci.yml
jobs:
  test:
    strategy:
      matrix:
        component: [frontend, backend, agents]
    steps:
      - Test ${{ matrix.component }}
  
  deploy-frontend:
    if: contains(github.event.head_commit.modified, 'frontend/')
    needs: test
    # Deploy to Netlify
  
  deploy-backend:
    if: contains(github.event.head_commit.modified, 'backend/')
    needs: test
    # Deploy to Railway
```

---

## Summary of Changes

| Area | Original | Upgraded |
|------|----------|----------|
| Code generation model | Claude (paid) | qwen2.5-coder (free) |
| Database | MongoDB | PostgreSQL |
| Backend boilerplate | Heavy (hagopj13) | Minimal scaffold |
| Agents at launch | 5 | 2 (expand later) |
| CI workflows | 3 files | 1 file |
| Estimated Claude cost | $150/month | $15-30/month |

---

## Ready for Execution

All upgrades documented. Local code model installing.

**Next:** Say "Execute the plan" to begin scaffolding.

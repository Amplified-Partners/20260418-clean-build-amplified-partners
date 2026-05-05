---
title: "GitHub Repository Consolidation Strategy"
id: "github-repo-consolidation-strategy"
version: 1
created: "2026-04-25"
type: "document"
topic_type: "strategy"
audience: "internal"
layer: "truth"
status: "filed"
signed_by: "Devon, 2026-04-25, devin-992682c244cf444f91e0a516498afbfd"
---

# GitHub Repository Consolidation Strategy

## Current State
You have 3 private repositories:

1. **covered-ai-v2** (TypeScript) - Main SaaS product, created Nov 27, last active Dec 1
2. **voice-ai** (Python) - Voice AI functionality, created Dec 11
3. **librarian-api** (Python) - Librarian API service, created Dec 21

## Analysis: Keep Separate (Recommended)

### Why Separate Repos is Best Practice Here

**Different concerns, different lifecycles:**
- `covered-ai-v2` is your main TypeScript/Next.js product
- `voice-ai` and `librarian-api` are Python microservices
- Each can be deployed, versioned, and maintained independently

**Industry standard for your architecture:**
- Following your project-system-prompt: "modular, service-oriented architecture"
- Matches patterns from companies like Stripe, GitHub, Vercel (separate repos per service)
- Easier CI/CD: each repo deploys to its own Railway service

**Practical benefits:**
1. **Cleaner permissions**: Different teams/contractors can access different repos
2. **Faster CI**: Changes to voice-ai don't trigger covered-ai-v2 builds
3. **Simpler deployment**: One repo = one Railway service = clear mapping
4. **Independent versioning**: voice-ai v2.0 doesn't force covered-ai-v2 v2.0

## When Monorepo WOULD Make Sense

You'd consolidate if:
- All three were parts of ONE application (frontend + BFF + worker)
- Shared 80%+ of dependencies
- Needed atomic cross-repo changes regularly
- Small team (1-3 people) maintaining everything

## Recommended Structure (Keep As-Is)

```
ewan-dot/
├── covered-ai-v2/          # Main product (Next.js + FastAPI)
│   ├── src/
│   ├── docs/
│   └── prisma/
│
├── voice-ai/               # Voice service (Python/FastAPI)
│   ├── src/
│   └── requirements.txt
│
└── librarian-api/          # Librarian service (Python/FastAPI)
    ├── src/
    └── requirements.txt
```

## Enhancement: Add Shared Library Repo (Optional)

If you start duplicating code between Python services:

```
ewan-dot/
└── covered-ai-shared/      # Shared utilities (NEW)
    ├── python/             # Shared Python code
    │   ├── auth_utils.py
    │   ├── llm_routing.py
    │   └── setup.py
    └── types/              # Shared TypeScript types
        └── api-contracts.ts
```

Install in services via:
```bash
pip install git+https://github.com/ewan-dot/covered-ai-shared.git@main#subdirectory=python
```

## Railway Deployment Map

**Current (Recommended):**
```
Railway Project: "covered-ai"
├── Service: covered-ai-v2 → repo: ewan-dot/covered-ai-v2
├── Service: voice-ai     → repo: ewan-dot/voice-ai
└── Service: librarian-api → repo: ewan-dot/librarian-api
```

**Monorepo (NOT Recommended):**
```
Railway Project: "covered-ai"
└── Service: monorepo → 3 separate Railway services pointing to subdirs
    (Complex, error-prone, harder to debug)
```

## Decision Matrix

| Factor | Separate Repos | Monorepo |
|--------|---------------|----------|
| **Deployment clarity** | ✅ Simple 1:1 mapping | ❌ Complex subdirectory routing |
| **CI/CD speed** | ✅ Fast, isolated | ❌ Slow, everything rebuilds |
| **Team scaling** | ✅ Easy permissions | ⚠️ All-or-nothing access |
| **Shared code** | ⚠️ Need shared-lib repo | ✅ Easy imports |
| **Independent versioning** | ✅ Full control | ❌ Coupled versions |
| **Initial setup** | ✅ Already done | ❌ Major refactor needed |

## Recommendation

**Keep your 3 separate repos.** This is industry best practice for your architecture and matches how your project-system-prompt describes the system.

Only consolidate if:
1. You're spending >20% of time on cross-repo changes
2. All three become tightly coupled (currently they're not)
3. You switch to a framework designed for monorepos (Nx, Turborepo)

---

## If You Must Consolidate (Discouraged)

If you decide to go against best practice:

### Structure
```
covered-ai-monorepo/
├── apps/
│   ├── web/              # Next.js (from covered-ai-v2)
│   ├── voice-api/        # FastAPI (from voice-ai)
│   └── librarian-api/    # FastAPI (from librarian-api)
├── packages/
│   ├── shared-types/
│   └── shared-utils/
├── package.json          # Workspace root
└── railway.json          # Multi-service config
```

### Tools Required
- **Turborepo** or **Nx** for build orchestration
- **pnpm workspaces** (not npm, too slow)
- Railway **monorepo support** configuration

### Migration Steps
1. Create new `covered-ai-monorepo` repo
2. Move each repo into `apps/` subdirectory
3. Configure Turborepo pipelines
4. Update Railway service paths
5. Test deployments individually
6. Archive old repos

**Complexity**: High  
**Time**: 2-4 days of refactoring + testing  
**Risk**: Deployment breakage, loss of git history

## Final Answer

**Keep the 3 separate repos.** Current structure is correct for your service-oriented architecture on Railway. If you hit code duplication, add a 4th shared-library repo, not a monorepo.

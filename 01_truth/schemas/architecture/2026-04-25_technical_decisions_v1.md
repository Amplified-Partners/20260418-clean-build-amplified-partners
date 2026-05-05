---
title: "Technical Decisions Log"
id: "technical_decisions"
version: 1
created: "2026-04-25"
type: "document"
topic_type: "tech-decision"
audience: "internal"
layer: "truth"
status: "filed"
signed_by: "Devon, 2026-04-25, devin-992682c244cf444f91e0a516498afbfd"
---

# Technical Decisions Log

**Last Updated:** 2024-12-16

---

## Architecture Decisions

### ADR-001: Monorepo Structure
**Date:** 2024-12-16  
**Status:** Approved  
**Context:** Need to manage frontend, backend, desktop app, and shared code

**Decision:** Use monorepo with workspaces
```
/personal-assistant
├── apps/
│   ├── web/          # Next.js frontend
│   ├── desktop/      # Tauri Mac app
│   └── backend/      # Node.js API
├── packages/
│   ├── ui/           # Shared UI components
│   ├── database/     # Prisma schema
│   ├── ai/           # LLM router & utilities
│   └── shared/       # Common types & utils
```

**Rationale:**
- Code sharing between web and desktop
- Unified type definitions
- Single CI/CD pipeline
- Easier dependency management

**Alternatives Considered:**
- Separate repos (rejected: too much duplication)
- Lerna (rejected: overkill for our size)

---

### ADR-002: Local-First AI Strategy
**Date:** 2024-12-16  
**Status:** Approved  
**Context:** Need to balance cost, privacy, and performance

**Decision:** Route 80% of tasks to local Ollama models, 20% to cloud

**Model Allocation:**
| Task Type | Model | Location | Cost |
|-----------|-------|----------|------|
| Code generation | qwen2.5-coder:14b | Local | FREE |
| General reasoning | qwen2.5:14b | Local | FREE |
| Fast classification | llama3.2:3b | Local | FREE |
| Complex reasoning | Claude Sonnet | Cloud | Paid |
| Backup/specific | GPT-4 | Cloud | Paid |

**Rationale:**
- Cost reduction: $15-30/month vs $150-300/month
- Privacy: Sensitive data stays local
- Speed: Local models faster for simple tasks
- Reliability: Cloud fallback for critical tasks

**Implementation:**
- LLM Router component decides model per task
- Automatic fallback if local model fails
- User can force cloud models for important tasks

---

### ADR-003: Database Choice - PostgreSQL
**Date:** 2024-12-16  
**Status:** Approved  
**Context:** Need relational data with vector search capability

**Decision:** PostgreSQL with pgvector extension

**Rationale:**
- Relational data (users, tasks, emails) fits SQL model
- pgvector for semantic search (embeddings)
- Railway has managed PostgreSQL
- Prisma ORM works excellently with Postgres
- Better for multi-tenancy than MongoDB

**Alternatives Considered:**
- MongoDB (rejected: less suited for relational SaaS data)
- SQLite (rejected: not suitable for multi-user web app)
- Supabase (considered: may use for auth later)

---

### ADR-004: Frontend Framework - Next.js 14
**Date:** 2024-12-16  
**Status:** Approved  
**Context:** Need modern React framework with SSR and API routes

**Decision:** Next.js 14 with App Router

**Rationale:**
- Server components for performance
- Built-in API routes (may use for simple endpoints)
- Excellent developer experience
- Vercel deployment (free tier)
- Large ecosystem and community

**Stack:**
- Next.js 14 (App Router)
- Tailwind CSS (styling)
- shadcn/ui (component library)
- Zustand or Jotai (state management)
- TanStack Query (data fetching)
- React Hook Form + Zod (forms)

---

### ADR-005: Desktop App - Tauri
**Date:** 2024-12-16  
**Status:** Approved  
**Context:** Need Mac native app without Electron bloat

**Decision:** Tauri (Rust + Web)

**Rationale:**
- Smaller bundle size than Electron (~3MB vs ~100MB)
- Better performance (Rust backend)
- Native system integration
- Reuse web frontend code
- Active development and community

**Alternatives Considered:**
- Electron (rejected: too heavy)
- Native Swift (rejected: can't reuse web code)
- PWA only (rejected: need deeper system integration)

---

### ADR-006: Queue System - BullMQ
**Date:** 2024-12-16  
**Status:** Approved  
**Context:** Need background job processing for email, AI tasks

**Decision:** BullMQ with Redis

**Rationale:**
- Robust job queue with retries
- Priority queues for urgent tasks
- Scheduled jobs (email checks, reminders)
- Progress tracking
- Redis already needed for caching

**Use Cases:**
- Email fetching and processing
- AI task processing (can be slow)
- Scheduled reminders
- Batch operations
- Call transcription

---

### ADR-007: Authentication Strategy
**Date:** 2024-12-16  
**Status:** Approved  
**Context:** Need secure auth with social login

**Decision:** JWT + OAuth 2.0

**Providers:**
- Google OAuth (primary)
- Microsoft OAuth (for Outlook users)
- Email + password (with 2FA)
- Mac Touch ID (desktop app)

**Implementation:**
- JWT tokens with refresh mechanism
- HttpOnly cookies for web
- Secure storage for desktop
- Session management in Redis

---

### ADR-008: Email Integration Strategy
**Date:** 2024-12-16  
**Status:** Approved  
**Context:** Need to access user emails securely

**Decision:** OAuth-based API access (no password storage)

**Providers:**
- Gmail API (Google OAuth)
- Microsoft Graph API (Microsoft OAuth)
- IMAP/SMTP fallback (encrypted credentials)

**Rationale:**
- No password storage (security)
- Granular permissions
- Official APIs (reliable)
- Webhook support for real-time updates

---

### ADR-009: LLM Router Implementation
**Date:** 2024-12-16  
**Status:** Approved  
**Context:** Need intelligent routing between local and cloud models

**Decision:** Rule-based router with fallback logic

```typescript
interface LLMRouter {
  route(task: Task): Promise<LLMResponse>
  
  // Routing logic:
  // 1. Check task type (code, reasoning, classification)
  // 2. Check task complexity (simple, medium, complex)
  // 3. Check user preference (force cloud, prefer local)
  // 4. Select model from routing table
  // 5. Execute with timeout and retry
  // 6. Fallback to cloud if local fails
}
```

**Routing Table:**
- Architecture/specs → Claude Sonnet
- Code generation → qwen2.5-coder (local)
- Email drafts → qwen2.5 (local) or Claude (complex)
- Summarization → qwen2.5 (local)
- Classification → llama3.2 (local)

---

### ADR-010: State Management - Zustand
**Date:** 2024-12-16  
**Status:** Approved  
**Context:** Need lightweight state management for React

**Decision:** Zustand (not Redux)

**Rationale:**
- Simpler API than Redux
- Less boilerplate
- Better TypeScript support
- Smaller bundle size
- Sufficient for our needs

**Alternatives Considered:**
- Redux Toolkit (rejected: overkill)
- Jotai (considered: may use for specific cases)
- Context API only (rejected: performance issues)

---

## Technology Stack Summary

### Frontend
- **Framework:** Next.js 14 (App Router)
- **Language:** TypeScript
- **Styling:** Tailwind CSS
- **Components:** shadcn/ui
- **State:** Zustand
- **Data Fetching:** TanStack Query
- **Forms:** React Hook Form + Zod
- **Icons:** Lucide React

### Backend
- **Runtime:** Node.js 20+
- **Framework:** Express or Fastify (TBD)
- **Language:** TypeScript
- **Database:** PostgreSQL 15+
- **ORM:** Prisma
- **Queue:** BullMQ + Redis
- **Cache:** Redis
- **Auth:** JWT + OAuth 2.0

### Desktop
- **Framework:** Tauri 2.0
- **Backend:** Rust
- **Frontend:** Shared with web (Next.js)

### AI/LLM
- **Local:** Ollama
  - qwen2.5-coder:14b
  - qwen2.5:14b
  - llama3.2:3b
- **Cloud:** 
  - Anthropic Claude (Sonnet, Haiku)
  - OpenAI GPT-4 (backup)
- **Embeddings:** sentence-transformers (local)
- **Vector DB:** pgvector

### DevOps
- **Version Control:** Git + GitHub
- **CI/CD:** GitHub Actions
- **Hosting:** 
  - Frontend: Vercel
  - Backend: Railway
  - Database: Railway (managed Postgres)
- **Monitoring:** Sentry (errors), PostHog (analytics)
- **Logging:** Winston (backend), console (frontend)

---

## Pending Decisions

### PD-001: Monetization Model
**Status:** Open  
**Options:**
1. Freemium (free tier + paid features)
2. Subscription ($10-20/month)
3. One-time purchase ($99-199)
4. Usage-based (pay for cloud AI usage)

**Considerations:**
- Local AI reduces ongoing costs
- Need to cover hosting and development
- User preference for pricing model

---

### PD-002: Multi-User Support
**Status:** Open  
**Options:**
1. Individual only (simpler)
2. Team features (shared tasks, delegation)
3. Family plan (shared calendar, tasks)

**Considerations:**
- Complexity vs value
- Market demand
- Technical implementation effort

---

### PD-003: Mobile Strategy
**Status:** Open  
**Options:**
1. Web-first (responsive, PWA)
2. iOS native (React Native or Swift)
3. Both (phased approach)

**Considerations:**
- Development resources
- User demand
- Feature parity challenges

---

### PD-004: Offline Mode
**Status:** Open  
**Options:**
1. Full offline (SQLite sync)
2. Partial offline (cached data)
3. Online-only (simpler)

**Considerations:**
- Sync complexity
- User expectations
- Technical feasibility

---

## Rejected Approaches

### MongoDB for Primary Database
**Rejected:** 2024-12-16  
**Reason:** Less suited for relational SaaS data, PostgreSQL better for multi-tenancy

### All-Cloud AI Strategy
**Rejected:** 2024-12-16  
**Reason:** Too expensive ($150-300/month), privacy concerns, local models sufficient for 80% of tasks

### Electron for Desktop
**Rejected:** 2024-12-16  
**Reason:** Too heavy (~100MB), Tauri is lighter and faster

### Redux for State Management
**Rejected:** 2024-12-16  
**Reason:** Overkill for our needs, Zustand simpler and sufficient

---

*Technical Decisions Log - Living Document*
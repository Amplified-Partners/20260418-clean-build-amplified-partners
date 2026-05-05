---
title: "Project Overview - Multi-Modal Personal Assistant"
id: "project_overview"
version: 1
created: "2026-04-25"
type: "document"
topic_type: "unsorted"
audience: "internal"
layer: "shadow"
status: "filed"
signed_by: "Devon, 2026-04-25, devin-992682c244cf444f91e0a516498afbfd"
---

# Project Overview - Multi-Modal Personal Assistant

**Last Updated:** 2024-12-16  
**Project Status:** Planning Phase  
**Current Phase:** Foundation Setup

---

## What This Project Is

A comprehensive AI-powered personal assistant that combines:
- Email management (triage, drafts, smart replies, bulk operations)
- Task and project management
- Coaching and goal tracking
- Telephone/voice assistant (inbound screening, outbound calls)
- Second-brain features (calendar, notes, research, habits, focus mode)

**Key Differentiator:** Local-first AI with behavioural science integration and UX law compliance.

---

## What We're Building

### Core Value Proposition
An intelligent assistant that maximizes task completion while minimizing cognitive load through:
1. Smart automation (not just reminders)
2. Context-aware suggestions
3. Unified interface across all personal productivity domains
4. Privacy-focused (local LLM models)
5. Cost-efficient (80% local, 20% cloud AI)

### Target Users
- Knowledge workers overwhelmed by email
- Professionals managing multiple projects
- Goal-oriented individuals seeking accountability
- Anyone wanting a "second brain" for personal productivity

---

## Current State

### What Exists
- **Telephone Assistant:** VAPI-based call screening and handling
- **Voice Interface:** Claude voice integration
- **Phone App:** Basic telephony functionality

### What's Missing
- Email assistant (entire module)
- Task/project manager (entire module)
- Coaching/goals (entire module)
- Second brain features (notes, calendar, research, habits)
- Unified interface connecting all components
- Local LLM integration and routing
- Database and backend infrastructure

---

## Technical Foundation

### Architecture Decisions
- **Frontend:** Next.js 14 + Tailwind CSS + shadcn/ui
- **Backend:** Node.js + Express/Fastify + PostgreSQL + Prisma
- **Desktop:** Tauri (Rust + Web) for Mac native
- **AI:** Ollama (local) + Claude/GPT-4 (cloud fallback)
- **Queue:** BullMQ + Redis
- **Hosting:** Railway (backend) + Vercel (frontend)

### AI Strategy
- **Local Models (80% of tasks):**
  - `qwen2.5-coder:14b` - Code generation
  - `qwen2.5:14b` - General reasoning
  - `llama3.2:3b` - Fast routing/classification
- **Cloud Models (20% of tasks):**
  - Claude - Complex reasoning
  - GPT-4 - Backup/specific tasks

**Cost Target:** $15-30/month (vs $150-300 all-cloud)

---

## Design Principles (Non-Negotiable)

### UX Laws
1. **Hick's Law:** Limit choices to 3-5 primary actions per screen
2. **Fitts's Law:** Large, easily reachable buttons for frequent actions
3. **Jakob's Law:** Follow familiar patterns (Gmail, Todoist, etc.)

### Behavioural Science
1. **Implementation Intentions:** If-then planning
2. **Commitment Devices:** Public goals, accountability
3. **Reward Systems:** Progress visualization, achievements
4. **Cognitive Load Reduction:** Single-task focus, batch operations

---

## Development Roadmap

### Phase 1: Foundation (Weeks 1-2)
- Project structure setup
- Database schema
- Authentication
- LLM router
- Email assistant MVP

### Phase 2: Core Features (Weeks 3-4)
- Task manager
- Calendar integration
- Telephone integration
- Voice interface refinement

### Phase 3: Intelligence Layer (Weeks 5-6)
- Smart prioritization
- Email drafting
- Call summaries
- Natural language processing

### Phase 4: Second Brain (Weeks 7-8)
- Notes system
- Web clipper
- Knowledge graph
- Habit tracking

### Phase 5: Coaching (Weeks 9-10)
- Goal framework
- Progress tracking
- Check-ins
- Insights

### Phase 6: Launch (Weeks 11-12)
- Optimization
- Security audit
- Testing
- Deployment

---

## Success Criteria

### User Metrics
- Task completion rate >80%
- Email processing time reduced by 50%+
- Daily active usage >70%
- User retention >80% after 30 days

### AI Performance
- Response accuracy >90%
- Local model response time <2s
- Cloud model response time <5s
- Cost per user <$2/month

### Business Goals
- NPS >50
- Time saved per user: 2+ hours/week
- Feature adoption >60% for core features

---

## Key Constraints

### Must Have
- Mac support (native or web)
- Local LLM integration
- Email assistant working
- Task manager working
- Telephone assistant integrated
- Privacy-focused architecture

### Won't Have (V1)
- Android app
- Linux desktop
- Enterprise features
- White-label options

---

## Integration Points

### Existing Components
- VAPI telephone system
- Claude voice interface
- Phone app infrastructure

### External Services
- Gmail/Outlook APIs
- Google/Apple/Outlook Calendar
- Twilio (backup telephony)
- ElevenLabs (TTS)

### Local Services
- Ollama LLM server
- PostgreSQL database
- Redis cache/queue

---

## Risk Management

### High Priority Risks
1. **LLM Accuracy:** Mitigate with testing + cloud fallback
2. **Email API Limits:** Mitigate with caching + batch operations
3. **User Adoption:** Mitigate with UX focus + real pain point solving

### Medium Priority Risks
1. **Cost Overruns:** Mitigate with aggressive local routing
2. **Integration Complexity:** Mitigate with phased approach
3. **Performance Issues:** Mitigate with optimization + monitoring

---

## Open Questions

1. Monetization: Freemium vs subscription vs one-time?
2. Multi-user: Individual only or team features?
3. Mobile: iOS priority or web-first?
4. Sync: Real-time or eventual consistency?
5. Offline: Full offline or online-required?

---

## Project Files

### Key Documents
- [`MASTER_SPEC.md`](../../MASTER_SPEC.md) - Complete specification
- This file - Project overview and memory bank

### Related Projects
- [`ai-chat-sync/`](../../ai-chat-sync/) - AI chat synchronization tool
- [`Baselayer/covered-ai-v2/`](../../Baselayer/covered-ai-v2/) - Related SaaS project
- [`knowledge_pipeline/`](../../knowledge_pipeline/) - Knowledge management system

---

## Notes for AI Assistants

### Context Rules
- Always read this file at the start of a session
- Never assume context from previous conversations
- Ask clarifying questions rather than guessing
- Update this file when significant decisions are made

### Working Style
- Follow MASTER_SPEC.md requirements exactly
- Apply UX laws (Hick's, Fitts's, Jakob's) to all design decisions
- Integrate behavioural science principles
- Prioritize local LLM usage over cloud
- Focus on task completion and cognitive load reduction

---

*Memory Bank initialized 2024-12-16*
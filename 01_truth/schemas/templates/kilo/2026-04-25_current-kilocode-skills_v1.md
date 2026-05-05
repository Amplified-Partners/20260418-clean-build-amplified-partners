---
title: "Current Kilo Code Skills"
id: "current-kilocode-skills"
version: 1
created: "2026-04-25"
type: "document"
topic_type: "agent-tooling"
audience: "internal"
layer: "truth"
status: "filed"
signed_by: "Devon, 2026-04-25, devin-992682c244cf444f91e0a516498afbfd"
---

# Current Kilo Code Skills

These are the "skills" (rule files) currently active in your Kilo Code workspace.

## 📍 Location
All skills live in: `../.kilocode/rules/`

---

## 1. **API Configuration** 
**File:** [`api-config.md`](../.kilocode/rules/api-config.md)

**What it does:**
- Manages AI provider settings (OpenRouter, Anthropic, MiniMax)
- Optimizes API costs by choosing the right model for each task
- Handles API key security and rate limiting
- Defines fallback chains when providers fail

**Key features:**
- Simple tasks → Claude Haiku ($1-5 per 1M tokens)
- Balanced work → Claude Sonnet ($3-15 per 1M tokens) 
- Complex reasoning → Claude Opus ($15-75 per 1M tokens)
- Budget option → MiniMax M2.1 ($0.30-1.20 per 1M tokens)

---

## 2. **Global Rules**
**File:** [`global-rules.md`](../.kilocode/rules/global-rules.md)

**What it does:**
- Sets fundamental coding principles
- Defines communication style (concise, direct)
- Enforces safety practices (confirmations before deletions)
- Establishes workflow patterns (read before writing, test as you go)

**Key principles:**
- Clean, readable code with clear naming
- Never over-engineer
- Always show diffs before applying changes
- Admit when uncertain rather than guess

---

## 3. **Intent Verification & Handoff**
**File:** [`intent-verification-handoff.md`](../.kilocode/rules/intent-verification-handoff.md)

**What it does:**
- Captures your intentions from conversation history
- Identifies incomplete tasks
- Verifies understanding before execution
- Hands off tasks to Orchestrator mode for implementation

**Triggers:**
- "Verify what I said today"
- "Check if everything's been done"
- "Make sure my requests are being handled"

**Process:**
1. Extract user intentions (even implied ones)
2. Categorize by status (completed, in progress, pending, unclear)
3. Create verification report
4. Prepare handoff packages
5. Execute handoff to Orchestrator

---

## 4. **Pre-Built Solutions Database**
**File:** [`prebuilt-solutions.md`](../.kilocode/rules/prebuilt-solutions.md)

**What it does:**
- Recommends existing libraries and tools before building custom
- Saves time by suggesting battle-tested solutions
- Provides decision framework (when to use pre-built vs custom)

**Categories:**
- UI Components (shadcn/ui, Radix UI, Headless UI)
- Authentication (Clerk, Supabase, NextAuth.js)
- Payments (Stripe, Lemon Squeezy)
- Database & ORM (Prisma, Drizzle, Supabase)
- Forms (React Hook Form + Zod)
- State Management (Zustand, Jotai)
- Testing (Vitest, Playwright)
- Deployment (Vercel, Railway, Netlify)
- SaaS Boilerplates

**Philosophy:** Use pre-built when time-to-market matters and feature is commodity. Build custom when you need unique business logic.

---

## 5. **Swift Code Style**
**File:** [`01-swift-style.md`](.kilocode/rules/01-swift-style.md)

**What it does:**
- Enforces Swift naming conventions (camelCase, PascalCase, CONSTANT_CASE)
- Promotes type safety and modern Swift syntax
- Defines error handling patterns
- Organizes code by concern

**Standards:**
- Variables/functions: `camelCase`
- Types (structs, classes, enums): `PascalCase`
- Constants: `CONSTANT_CASE`
- Use `guard` statements for early returns
- Avoid force unwrapping (`!`)
- Add MARK comments to separate sections

---

## 6. **Swift Data Model Structure**
**File:** [`02-swift-model-structure.md`](.kilocode/rules/02-swift-model-structure.md)

**What it does:**
- Defines how to structure Swift data models
- Enforces `Codable` conformance with `.iso8601` encoding
- Specifies file organization for Swift projects
- Sets JSON persistence standards

**File locations:**
- Models: `TodayMirror/Models/`
- Services: `TodayMirror/Services/`
- Views: `TodayMirror/Views/`
- ViewModels: `TodayMirror/ViewModels/`
- Theme: `TodayMirror/Theme/`
- Extensions: `TodayMirror/Extensions/`

**Requirements:**
- All models must conform to `Codable`
- Use `.iso8601` date encoding strategy
- Include static helpers (`empty`, `withDemoData()`)
- JSON files stored in `~/.today-mirror/data/`

---

## 7. **Swift ViewModel Rules**
**File:** [`03-swift-viewmodel-rules.md`](.kilocode/rules/03-swift-viewmodel-rules.md) and [`swift-viewmodel-rules.md`](.kilocode/rules/swift-viewmodel-rules.md)

**What it does:**
- Prevents dynamic member lookup errors in SwiftUI
- Enforces type-safe property access
- Validates property existence before use

**Critical rules:**
- NEVER use dynamic member lookup on @EnvironmentObject
- ALWAYS declare explicit types
- NEVER invent properties - verify they exist first
- NEVER reference views that don't exist

**Common error prevention:**
```swift
// ❌ FORBIDDEN
@EnvironmentObject var taskViewModel

// ✅ REQUIRED
@EnvironmentObject var taskViewModel: TaskViewModel
```

---

## 8. **Agent Workflows**
**File:** [`agent-workflows.md`](.kilocode/rules/agent-workflows.md)

**What it does:**
- Defines step-by-step workflows for common AI tasks
- Ensures consistent approach to feature implementation
- Provides troubleshooting procedures

**Workflows:**
1. **Feature Implementation** - TDD approach with spec review
2. **Railway Error Analysis** - Log parsing to root cause fix
3. **Performance Tuning** - Identify hotspots → optimize → verify
4. **Git Workflow for Refactors** - Branch → incremental changes → test

---

## 9. **Kilo Code Profiles**
**File:** [`profiles.md`](.kilocode/rules/profiles.md)

**What it does:**
- Defines optimized settings for different development tasks
- Matches AI model to task complexity
- Sets context strategy and guardrails per profile

**Profiles:**
1. **Local-Dev-Coding** - Fast iteration (qwen2.5-coder, temp 0.1)
2. **Cloud-Deep-Refactor** - Complex changes (Claude Sonnet, temp 0.3, 200k context)
3. **Railway-Ops-Agent** - Deployment debugging (Claude/GPT-4o, temp 0.1)
4. **Docs-Research-Agent** - Documentation (Claude Haiku/Llama 3, temp 0.5)

---

## 10. **Project System Prompt**
**File:** [`project-system-prompt.md`](.kilocode/rules/project-system-prompt.md)

**What it does:**
- Defines overall architecture (modular, service-oriented)
- Sets tech stack preferences
- Establishes coding conventions
- Defines deployment flow and testing strategy

**Architecture:**
- Frontend: Next.js (React) with Server Components
- Backend: FastAPI (Python) or Node.js (TypeScript)
- Worker: Background tasks (queues, cron)
- Database: PostgreSQL (via Railway)
- Cache: Redis
- AI: Centralized LLM routing

**Tech stack:**
- TypeScript (Frontend/Node)
- Python 3.11+ (AI/Backend)
- Frameworks: Next.js 14+, FastAPI, Tailwind CSS
- Database: Prisma (TS) or SQLAlchemy (Python)
- Testing: Vitest (TS), Pytest (Python)

---

## How Skills Work Together

### Planning Phase (Architect mode)
- Uses **Intent Verification** to extract requirements
- Applies **Global Rules** for communication
- Checks **Pre-Built Solutions** before planning custom builds
- References **Project System Prompt** for architecture decisions

### Implementation Phase (Code/Orchestrator mode)
- Follows **Agent Workflows** for consistent execution
- Uses **Profiles** to select right model for task
- Applies language-specific rules (Swift, TypeScript, Python)
- Manages API calls with **API Configuration**

### Quality Assurance
- **Global Rules** enforce safety (diffs, confirmations)
- Language-specific rules catch common errors
- **Project System Prompt** ensures architectural consistency

---

## Coming Soon: 6 New Skills

I've planned these additional skills (not yet implemented):
1. TypeScript/Next.js File Structure
2. Python/FastAPI File Structure
3. Swift Project File Structure
4. GitHub Best Practices
5. .gitignore Templates
6. Integration Guide

Ready to create them when you say "Switch to Code mode and create the 6 rule files"

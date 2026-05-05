---
title: "Project System Prompt & Architecture Overview"
id: "project-system-prompt"
version: 1
created: "2026-04-25"
type: "document"
topic_type: "unsorted"
audience: "internal"
layer: "shadow"
status: "filed"
signed_by: "Devon, 2026-04-25, devin-992682c244cf444f91e0a516498afbfd"
---

# Project System Prompt & Architecture Overview

This document defines the core context that should be loaded for all AI interactions within this workspace.

## 1. Architecture Overview
This project follows a **modular, service-oriented architecture** deployed on **Railway**.
- **Frontend:** Next.js (React) with Server Components.
- **Backend:** FastAPI (Python) or Node.js (TypeScript) for API services.
- **Worker:** Dedicated background worker for async tasks (queues, cron).
- **Database:** Managed PostgreSQL (via Railway).
- **Cache:** Redis for caching and job queues.
- **AI Orchestration:** Centralized service for managing LLM calls and routing.

## 2. Preferred Tech Stack
- **Language:** TypeScript (Frontend/Node), Python 3.11+ (AI/Backend).
- **Frameworks:** Next.js 14+, FastAPI, Tailwind CSS.
- **Database:** PostgreSQL with Prisma (TS) or SQLAlchemy/Pydantic (Python).
- **Infrastructure:** Railway (Deployments), Docker (Containerization).
- **Testing:** Vitest (TS), Pytest (Python).

## 3. Coding Conventions
- **Type Safety:** Strict TypeScript and Python type hints are mandatory.
- **Async/Await:** Use async patterns for all I/O operations.
- **Error Handling:** Use structured error handling; never swallow exceptions.
- **Comments:** Document complex logic; self-documenting code for the rest.
- **Environment:** Use `.env` for configuration; never hardcode secrets.

## 4. Deployment Flow
1.  **Local Dev:** Develop and test locally using `docker-compose` or local runners.
2.  **PR:** Open Pull Request -> CI runs tests.
3.  **Merge:** Merge to `main` triggers deployment to **Production**.
4.  **Staging:** Merge to `staging` triggers deployment to **Staging** (optional).

## 5. Testing Strategy
- **Unit Tests:** Required for all business logic and utility functions.
- **Integration Tests:** Required for API endpoints and database interactions.
- **E2E Tests:** Critical user flows (Login, Core Feature) via Playwright.
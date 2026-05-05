---
title: "Covered AI v2 — Copilot instructions"
id: "copilot-instructions"
version: 1
created: "2026-04-25"
type: "document"
topic_type: "unsorted"
audience: "internal"
layer: "shadow"
status: "filed"
signed_by: "Devon, 2026-04-25, devin-992682c244cf444f91e0a516498afbfd"
---

<!-- .github/copilot-instructions.md: Guidance for AI coding agents working in this repo -->
# Covered AI v2 — Copilot instructions

Short, actionable guidance to help AI coding agents be productive in this repository.

- **Big picture:** Backend is a Python FastAPI app in `src/api` (entry: `src/api/main.py`). Frontend is a Next.js TypeScript app in `frontend/`. Durable background jobs live in `trigger-jobs/` and are wired via `trigger.config.ts`. Prisma schema is authoritative at `prisma/schema.prisma` and generates both JS and Python clients.

- **Key integration points:**
  - Vapi (voice AI) → webhook: `POST /api/v1/webhooks/vapi/call-complete` (see `src/api/webhooks.py`).
  - Trigger.dev jobs are defined in `trigger-jobs/` (e.g. `lead-nurture.ts`, `video-generation.ts`) and started with `npx trigger.dev dev` (root `package.json` has `dev`).
  - MCP/local mocks: `mcp-servers/*` contain local server scripts (npm scripts: `mcp:twilio`, `mcp:postgres`, etc.).

- **Languages & responsibilities:**
  - Python (FastAPI, business logic) in `src/` and tests under `tests/` (pytest).
  - TypeScript/Node for jobs, MCP servers and Prisma client (see root `package.json` and `frontend/package.json`).
  - Prisma is used as the single DB schema source (`prisma/schema.prisma`). Changes require `npx prisma generate` and migrations (`npx prisma migrate dev`).

- **Common developer flows & exact commands:**
  - Setup (root):
    - `npm install`
    - `pip install -r requirements.txt`
    - `cp .env.example .env` and populate secrets
    - `npx prisma generate`
    - `npx prisma migrate dev`
    - `npx prisma db seed` or `npm run db:seed`
  - Run backend locally: `uvicorn src.api.main:app --reload --port 8000`
  - Run Trigger.dev locally: `npm run dev` (root) or `npx trigger.dev dev`
  - Run MCP server mocks: `npm run mcp:twilio` (or `mcp:postgres`, `mcp:resend`, `mcp:heygen`)
  - Frontend dev: `cd frontend && npm install && npm run dev`
  - Run tests (Python): `pytest tests/ -v`
  - Inspect DB: `npm run db:studio`

- **Repository-specific conventions & patterns**
  - Nurture & job logic is implemented in `trigger-jobs/` (12-touch sequence lives in `lead-nurture.ts`). When updating touch logic update the tests in `tests/test_nurture.py`.
  - Business logic for leads/customers lives in `src/services/` (e.g. `lead_service.py`) — prefer editing service functions and adding small, focused unit tests under `tests/`.
  - Templates for outbound communication live in `templates/` (`templates/email/`, `templates/sms/`, `templates/whatsapp/`), and Trigger.dev jobs reference these templates.
  - When adding or modifying webhooks, update `src/api/webhooks.py`, add/instrument a Trigger.dev job if the action is long-running, and add integration tests in `tests/test_webhooks.py`.

- **Formatting, linting, and tests**
  - Python formatting: `black` & `isort` are available in `requirements.txt`.
  - TypeScript tooling: `ts-node`, `prisma`, `typescript` are in `devDependencies`.
  - Run unit + integration tests via `pytest`. Node-side tests (if any) use `jest` (`npm test`).

- **When you change the DB schema:**
  1. Update `prisma/schema.prisma`.
 2. Run `npx prisma migrate dev`.
 3. Run `npx prisma generate` (or `npm run db:generate`).
 4. Update any TS/Python code that consumes the schema (Prisma JS client or pyclient). Search for model names (e.g. `Lead`, `Client`, `NurtureSequence`).

- **Useful file examples to inspect**
  - `src/api/webhooks.py` — webhook handlers and Vapi integration.
  - `trigger-jobs/lead-nurture.ts` — 12-touch nurture sequence logic.
  - `prisma/schema.prisma` — canonical DB schema.
  - `src/services/lead_service.py` — lead business logic.
  - `templates/email/*` — email examples used in jobs.

If something's missing or unclear here, tell me which area you'd like expanded (deploy, debugging, test examples, or Prisma migration notes) and I'll iterate.

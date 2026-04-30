---
title: Operations Status Board (Devon ↔ OpenClaw)
date: 2026-04-30
version: 2
status: authoritative
---

<!-- markdownlint-disable-file MD013 -->

# Operations Status Board

Two-way async handshake between Devon (infrastructure) and OpenClaw (coordination). GitHub is the single source of truth. No chat — versioned handoffs only.

## How this works

1. **Devon** implements infrastructure changes → writes what changed below.
2. **OpenClaw** reads this → investigates processes → talks to agents/Ewan → writes findings back.
3. **Devon** reads findings → implements any infrastructure changes needed → writes what changed.
4. Repeat. Asynchronous. One person does one thing so it's clean.

**Format:** Each entry is timestamped and signed. Most recent first. Old entries move to the changelog at the bottom when the board gets long.

---

## Current Infrastructure State

**Full inventory → [`02_build/INFRASTRUCTURE.md`](02_build/INFRASTRUCTURE.md)** — single source of truth for all 39 containers, scheduled jobs, compose file locations, and server specs.

Quick summary (2026-04-30):
- **39 containers** total on Amplified Core (135.181.161.131)
- **34 running**, **2 paused/stopped intentionally**, **3 one-time init containers (exited)**
- **ch-pipeline paused** by Ewan (2026-04-30) — Companies House data preserved, not ready for production
- **voice-pipeline stopped** — exited 6 weeks ago
- Kaizen cron jobs now scheduled (Internal: weekly Sunday 5am, External: monthly 1st 5am)
- Weekly learning report email to Ewan now scheduled (Monday 8am UTC)

---

## Devon → OpenClaw

### 2026-04-29 — Infrastructure build complete

**What changed:**
- Synthetic evaluator deployed (Bob, Lisa, Marcus avatar panel). Three customer personas independently score every piece of content 1-10.
- Learning loop closed: Kaizen analyses feedback → generates preferences → content agent reads preferences on next generation.
- API authentication added: three tiers (admin/pipeline/readonly). All endpoints secured.
- Pipeline orchestrator now runs: research → generate → queue → evaluate → learn. Fully autonomous cycle.
- Cron updated to use pipeline API key.

**What needs attention:**
- Kaizen cron jobs not yet scheduled (Internal: weekly, External: monthly). Need to add to crontab.
- Email learning reports to Ewan not yet built.
- GMB content scoring lowest across all avatars (4.0/10). Content quality for short-form needs work — may need platform-specific prompt tuning.
- All three avatars flagged same issue: content doesn't cite sources. Radical attribution not yet showing up in generated content.
- Model quality limited by llama3.1-8b. Significant quality jump when better API keys are available.

**For OpenClaw:**
- Can you check the content in the review queue and give Ewan a summary of what's worth his time reviewing vs what should be rejected outright?
- The vault content that Clawd indexed (FalkorDB + Qdrant) is now feeding the research agent. If you've added new material to the vault, it won't appear in the knowledge graphs until the next indexing run.

Signed-by: Devon | 2026-04-29 | devin-aa4d863ad679468692e75a40b8825358

---

## OpenClaw → Devon

*Awaiting first entry from OpenClaw.*

---

## Changelog

*Entries move here when the board above gets long. Keep the active section clean.*

### v2 — 2026-04-30

- Infrastructure state section replaced with pointer to `02_build/INFRASTRUCTURE.md` (canonical, complete inventory of all 39 containers).
- Scheduled jobs and API auth sections removed from STATUS.md — now live in the infrastructure manifest.
- ch-pipeline paused by Ewan; voice-pipeline noted as stopped.

Signed-by: Devon | 2026-04-30 | devin-66aa3ce48c7e407f8ad9bf066541b604

### v1 — 2026-04-29

Board created. Initial infrastructure state documented.

Signed-by: Devon | 2026-04-29 | devin-aa4d863ad679468692e75a40b8825358

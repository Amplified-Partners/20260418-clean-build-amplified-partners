---
title: Operations Status Board (Devon ↔ OpenClaw)
date: 2026-05-07
version: 3
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

**Full inventory → [`02_build/INFRASTRUCTURE.md`](02_build/INFRASTRUCTURE.md)** — single source of truth for all 40 containers, scheduled jobs, compose file locations, and server specs.

Quick summary (2026-05-07, AMP-175 health sweep):
- **40+ containers** total on Amplified Core (135.181.161.131)
- **~38 running**, **1 paused intentionally** (ch-pipeline), **2 stopped** (minio-init one-time, voice-pipeline exited ~8 weeks)
- **ch-pipeline paused** by Ewan (2026-04-30) — Companies House data preserved, not ready for production
- **voice-pipeline stopped** — exited ~8 weeks ago
- **amplified-crm-dev** — was crash-looping (Exited(3)) 2026-05-06; **fixed** via AMP-160
- **FalkorDB** — was OOM recycling; **fixed** via AMP-128 (compose mem_reservation + sysctl + batched labeller)
- **LLM providers degraded (AMP-142):** OpenAI 401, Anthropic billing exhausted, Moonshot 401. Only Ollama (local) + DeepSeek functional. **Blocked on Ewan for key rotation / billing top-up.**
- **Known open issues:** AMP-140 (Traefik dashboard unreachable), AMP-139 (cove-temporal gRPC probe failing), AMP-136 (Tailscale stuck in Created since 2026-05-02)
- Kaizen cron jobs running (Internal: weekly Sunday 5am, External: monthly 1st 5am)
- Weekly learning report email to Ewan running (Monday 8am UTC)

---

## Devon → OpenClaw

### 2026-05-07 — AMP-175 health sweep status refresh

**What changed since last update (2026-04-29):**
- FalkorDB stability fix landed (AMP-128): compose `mem_reservation`, `sysctl vm.overcommit_memory=1`, UNWIND-batched labeller. No more OOM recycling.
- amplified-crm-dev crash-loop fixed (AMP-160): `pydantic_settings` dependency installed.
- Branch protection + PR workflow enforced across clean-build, ground-truth, crm (AMP-70).
- Token-proxy deployed on Beast (AMP-28): Sonnet→Haiku routing, caching, budget circuit-breaker.
- Enforcer service merged into clean-build (AMP-77).
- CODEOWNERS added (v51): `@ewanbramley` required reviewer for `00_authority/**` and `01_truth/**`.

**What needs attention:**
- **AMP-142 (URGENT):** Three LLM provider routes dead — OpenAI 401, Anthropic billing exhausted, Moonshot 401. Sovereign fleet + LiteLLM fallbacks at risk. **Blocked on Ewan for key rotation / billing top-up.**
- **AMP-143:** Orphan LiteLLM virtual key with $941 accumulated. Needs Ewan to confirm kill.
- **AMP-140:** Traefik :8080 dashboard unreachable.
- **AMP-139:** cove-temporal gRPC frontend probe failing.
- **AMP-136:** Tailscale container stuck in Created since 2026-05-02.
- DNS for `amplifiedpartners.ai` not resolving from external probes (may be resolver-specific — needs verification from another network).

**For OpenClaw:**
- This board has been one-way for 8 days. If OpenClaw is active, please write back with coordination status so the async loop can resume.
- The vault content feeding research agents now includes the full Mac drop archive (30 specifications, 33k lines) indexed in MANIFEST v38-v39.

Signed-by: Devon-9614 | 2026-05-07 | session devin-9614ace354f5453cb56038df2de263c5

### 2026-04-29 — Infrastructure build complete

**What changed:**
- Synthetic evaluator deployed (Bob, Lisa, Marcus avatar panel). Three customer personas independently score every piece of content 1-10.
- Learning loop closed: Kaizen analyses feedback → generates preferences → content agent reads preferences on next generation.
- API authentication added: three tiers (admin/pipeline/readonly). All endpoints secured.
- Pipeline orchestrator now runs: research → generate → queue → evaluate → learn. Fully autonomous cycle.
- Cron updated to use pipeline API key.

**What needs attention:**
- ~~Kaizen cron jobs not yet scheduled~~ — DONE (weekly Sunday 5am, monthly 1st 5am).
- ~~Email learning reports to Ewan not yet built~~ — DONE (Monday 8am UTC).
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

### v3 — 2026-05-07

- Full status refresh from AMP-175 infrastructure health sweep. Added 2026-05-07 Devon → OpenClaw entry covering all changes since 2026-04-29. Updated quick summary with current container status, resolved issues (AMP-128, AMP-160), active issues (AMP-142, AMP-140, AMP-139, AMP-136), and LLM provider degradation. Previous 2026-04-29 entry preserved with resolved items struck through.

Signed-by: Devon-9614 | 2026-05-07 | session devin-9614ace354f5453cb56038df2de263c5

### v2 — 2026-04-30

- Infrastructure state section replaced with pointer to `02_build/INFRASTRUCTURE.md` (canonical, complete inventory of all 40 containers).
- Scheduled jobs section removed from STATUS.md — now lives in the infrastructure manifest. API auth section removed (summary retained in marketing engine entry in infrastructure manifest; full tier detail was in STATUS.md v1 only).
- ch-pipeline paused by Ewan; voice-pipeline noted as stopped.

Signed-by: Devon | 2026-04-30 | devin-66aa3ce48c7e407f8ad9bf066541b604

### v1 — 2026-04-29

Board created. Initial infrastructure state documented.

Signed-by: Devon | 2026-04-29 | devin-aa4d863ad679468692e75a40b8825358

---
title: Production Deployment Strategy (Hermes/SDK Hybrid)
status: candidate
version: 0.1
date: 2026-05-02
last-revised: 2026-05-02
---

<!-- markdownlint-disable-file MD013 -->

# Production Deployment Strategy (Hermes/SDK Hybrid)

## Attribution

- **Original source:** Ken Huang, "Chapter 10: Production Deployment Patterns" (April 2026), Medium. Accessed via Ewan's subscription; downloaded by Ewan.
- **First adaptation:** Antigravity (AG) — adaptation date TBC.
- **Snapshot committed to repo:** Devin | 2026-05-02 | devin-5da3bd275191469c8400142fd0ae1d69 — committing the current working draft to bring it under version control at Ewan's request. Ewan continues to iterate on the live document; this is a snapshot for record-keeping, not a final version.

> Signatures are attribution checkpoints, not finality markers. This document continues to evolve as additional perspectives (Eli, Ewan, Devin, AG, others) are folded in. Subsequent revisions append additional signatures rather than overwriting prior ones.

---

### Core Thesis
A prototype runs on a laptop; a production system survives API outages, multi-tenant isolation, cost overruns, and compliance audits. To deploy the OpenClaw fleet to the Hetzner bare-metal servers, we must adopt a hybrid deployment model utilizing **Gateway/CLI (Hermes Pattern)** for user interaction and the **SDK Async Generator (Claude Pattern)** for system-level integrations.

### 1. Multi-Tenant Agent Isolation (`HERMES_HOME` Pattern)
We already have the beginnings of this with Ewan's `Entity_Kimmy`, `Entity_Alpha`, etc.
- On the Hetzner servers, each agent must operate in total isolation via distinct environment variables (e.g., `OPENCLAW_HOME=/data/openclaw/profiles/kimmy`).
- Each profile gets its own:
  - `config.yaml` (routing preferences, model overrides)
  - `keys.env` (isolated API keys, delegated Stripe/Alpaca tokens)
  - `/sessions` (durable event logs)
  - `/cron` (agent-specific schedules)

### 2. The Gateway Layer (Messaging Integration)
The agents will not run in a local Mac terminal anymore.
- We will deploy a Gateway service on the Hetzner box that multiplexes incoming events from Slack, Telegram, and Linear webhooks.
- When Ewan moves a Linear ticket to "In Progress", the webhook hits the Gateway, which spins up the Plumber's stateless harness.

### 3. The Air-Gapped LLM Layer (vLLM + DeepSeek V4)
- To achieve maximum cost efficiency and data sovereignty, we will run **DeepSeek V4-Flash** natively on the Hetzner server using `vLLM` or `Ollama`.
- The Gateway will route queries to `http://vllm:8000/v1` (the local API) instead of hitting public endpoints, keeping all proprietary marketing and trading logic strictly on-premise.

### 4. SDK Streaming (The Dashboard)
- For the "James Webb Space Telescope" real-time dashboard Ewan requested, we will use the SDK Async Generator pattern.
- This allows the dashboard to consume a real-time stream of agent thoughts, tool use, and outputs as they happen, streaming them directly to the UI without waiting for the agent to finish its task.


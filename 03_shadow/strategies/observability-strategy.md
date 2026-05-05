---
title: Observability & Tracing Strategy (Hermes/SDK Hybrid)
status: candidate
version: 0.1
date: 2026-05-02
last-revised: 2026-05-02
---

<!-- markdownlint-disable-file MD013 -->

# Observability & Tracing Strategy (Hermes/SDK Hybrid)

## Attribution

- **Original source:** Ken Huang, "Chapter 15: Observability and Tracing", Medium. Accessed via Ewan's subscription; downloaded by Ewan.
- **First adaptation:** Antigravity (AG) — adaptation date TBC.
- **Snapshot committed to repo:** Devin | 2026-05-02 | devin-5da3bd275191469c8400142fd0ae1d69 — committing the current working draft to bring it under version control at Ewan's request. Ewan continues to iterate on the live document; this is a snapshot for record-keeping, not a final version.

> Signatures are attribution checkpoints, not finality markers. This document continues to evolve as additional perspectives (Eli, Ewan, Devin, AG, others) are folded in. Subsequent revisions append additional signatures rather than overwriting prior ones.

---

### Core Thesis
Debugging an autonomous 24/7 agent without observability is "archaeology." Because our OpenClaw fleet will operate asynchronously on Hetzner servers—executing live code and live trades—we must implement a compliance-grade observability layer. We will adopt the Hybrid Pattern: **Chain-ID Tracing (Claude Pattern)** combined with **JSONL Trajectory Logging (Hermes Pattern)**.

### 1. Distributed Tracing (`chainId`)
When an event (like a Linear webhook) triggers Kimmy, she creates a root `chainId` at `depth: 0`.
- If Kimmy delegates a code task to the Plumber, she passes the `chainId`, and the Plumber operates at `depth: 1`.
- If the Plumber asks the Artist for an asset, the Artist operates at `depth: 2`.
This allows us to reconstruct the exact causal chain of any multi-agent operation in our Splunk/ELK dashboards.

### 2. JSONL Trajectory Logging
Instead of relying on ephemeral terminal outputs, every agent turn will be saved to an append-only JSONL file in their respective `HERMES_HOME` (e.g., `Entity_Alpha/sessions/trajectory.jsonl`).
- **Success vs. Failure Separation:** Failed tasks are routed to `failed_trajectories.jsonl`. This is crucial for the "Kaizen Loop"—Ewan can review failed trajectories to write new `SKILL.md` runbooks that prevent the failure next time.

### 3. Compliance Guardrails (`RedactingFormatter`)
Because the agents will handle API keys and Stripe/Alpaca tokens via the MCP Vault, the logging layer must utilize a `RedactingFormatter` to strip all secrets before they are written to disk. The agents' raw thoughts and tool inputs are captured, but credentials are obfuscated.

### Amplified Partners Implementation (The CyberAuditLogger)
To govern the sovereign fleet, Ewan will deploy the `CyberAuditLogger` pattern. Every tool call must log:
1. `analyst_id` (e.g., Entity_Kimmy)
2. `permission_decision` (Allow/Deny/Escalate via preToolUse hooks)
3. `justification` (Why the agent chose to use the tool)

This ensures Ewan has total cryptographic and operational transparency over the fleet's actions.


---
title: Model Routing & Fallback Strategy (Hermes Pattern)
status: candidate
version: 0.1
date: 2026-05-02
last-revised: 2026-05-02
---

<!-- markdownlint-disable-file MD013 -->

# Model Routing & Fallback Strategy (Hermes Pattern)

## Attribution

- **Original source:** Ken Huang, "Chapter 14: Model Routing and Provider Abstraction" (May 2026), Medium. Accessed via Ewan's subscription; downloaded by Ewan.
- **First adaptation:** Antigravity (AG) — adaptation date TBC.
- **Snapshot committed to repo:** Devin | 2026-05-02 | devin-5da3bd275191469c8400142fd0ae1d69 — committing the current working draft to bring it under version control at Ewan's request. Ewan continues to iterate on the live document; this is a snapshot for record-keeping, not a final version.

> Signatures are attribution checkpoints, not finality markers. This document continues to evolve as additional perspectives (Eli, Ewan, Devin, AG, others) are folded in. Subsequent revisions append additional signatures rather than overwriting prior ones.

---

### Core Thesis
Production agents cannot be hardwired to a single provider. APIs go down, costs fluctuate, and different tasks require different levels of reasoning. To achieve true 24/7 resilience on the Hetzner servers, OpenClaw must adopt the **Hermes Runtime Routing Pattern**, which implements dynamic API detection, ordered fallback chains, and smart cost-based routing.

### 1. The Ordered Fallback Chain (Graceful Degradation)
If Anthropic or OpenAI goes down, the agent must not crash. It must step down the fallback chain automatically.
For the Arbiter and the Plumber, the fallback chain will be:
1. **Primary:** Claude Opus 4.6 (or DeepSeek V4-Pro) - Highest reasoning.
2. **Fallback 1:** DeepSeek V4-Flash (via OpenRouter/API) - Fast, capable, cheap.
3. **Fallback 2 (Air-Gapped):** Local Llama-3.3-70B (or DeepSeek V4) running via `vLLM` directly on the Hetzner server.
If the server loses internet connectivity, the agent seamlessly degrades to the local model and continues operating.

### 2. Smart Model Routing (Cost Optimization)
Not every query requires frontier-level intelligence. 
- **Routine Tasks:** When Charlie (The Plumber) is just parsing a basic log file or running a standard linter, the harness detects the simplicity (e.g., short prompt, no complex keywords) and routes the request to **DeepSeek V4-Flash**.
- **Complex Tasks:** If Charlie detects an anomaly and needs to write a patch, the harness dynamically switches to **DeepSeek V4-Pro** or **Claude Opus 4.6** *mid-session*, retaining the full conversation history.

### 3. API Auto-Detection
Instead of hardcoding whether a model uses `chat_completions`, `codex_responses`, or `anthropic_messages`, the OpenClaw harness will infer the API shape directly from the URL or provider string. This eliminates configuration errors when adding new models to the fleet.

### Amplified Partners Implementation
We will update `openclaw.json` to move beyond static model assignments (`"model": "claude-opus"`) and instead implement `fallback_providers` and `smart_model_routing` blocks for each Entity. This ensures Ewan's sovereign fleet is economically optimized and impervious to cloud API outages.


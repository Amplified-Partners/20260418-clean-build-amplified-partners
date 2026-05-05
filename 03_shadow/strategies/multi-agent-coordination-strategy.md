---
title: Multi-Agent Coordination Strategy
status: candidate
version: 0.1
date: 2026-05-02
last-revised: 2026-05-02
---

<!-- markdownlint-disable-file MD013 -->

# Multi-Agent Coordination Strategy

## Attribution

- **Original source:** Ken Huang, "Chapter 7: Multi-Agent Coordination", Medium. Accessed via Ewan's subscription; downloaded by Ewan.
- **First adaptation:** Antigravity (AG) — adaptation date TBC.
- **Snapshot committed to repo:** Devin | 2026-05-02 | devin-5da3bd275191469c8400142fd0ae1d69 — committing the current working draft to bring it under version control at Ewan's request. Ewan continues to iterate on the live document; this is a snapshot for record-keeping, not a final version.

> Signatures are attribution checkpoints, not finality markers. This document continues to evolve as additional perspectives (Eli, Ewan, Devin, AG, others) are folded in. Subsequent revisions append additional signatures rather than overwriting prior ones.

---

### Core Thesis
Complex tasks cannot be solved in a single context window. To solve large-scale problems, Kimmy (the Orchestrator) must decompose work and delegate it to specialized agents (Alpha, Charlie) running in parallel. This requires strict boundaries to prevent context contamination and runaway agent loops.

### 1. Worktree Isolation (The Sandbox)
When Kimmy delegates a task to Charlie (The Plumber) to fix a bug in the main codebase, Charlie does not operate in the same folder.
- The Harness creates an isolated **Git Worktree** specifically for Charlie's agent ID.
- Charlie edits code, runs tests, and commits locally in his sandbox.
- If Charlie succeeds, the changes are merged back. If he fails, the worktree is destroyed. This prevents Charlie from accidentally corrupting the active repository.

### 2. Parallel Delegation (The Thread Pool)
When Kimmy needs multiple things done at once (e.g., Charlie fixing the backend while the Artist generates assets), she uses **Batch Delegation**.
- Child agents run concurrently via a Python `ThreadPoolExecutor`.
- Each child is given an isolated `IterationBudget` so a slow task (like video rendering) doesn't starve a fast task (like script writing).

### 3. The Flat Hierarchy & Depth Guards
Unbounded nested agents lead to astronomical API bills and infinite loops.
- **Depth Guard:** The OpenClaw architecture will enforce a `MAX_DEPTH = 2`. Kimmy (Depth 0) can spawn Charlie (Depth 1). Charlie cannot spawn a sub-agent.
- **Interrupt Propagation:** If Ewan hits the "Cancel" button on Kimmy, the kill signal cascades down to all active children (`_active_children`), instantly halting all compute across the Hetzner server.

### 4. Prompt Cache Sharing (Forking)
To drastically cut API costs, when Kimmy delegates a sub-task, she uses the "Fork" pattern. The child agent inherits Kimmy's exact pre-rendered system prompt. Because the API sees identical bytes, it reuses the KV Cache, dropping the input token cost by up to 90%.

### Amplified Partners Implementation
This defines exactly how the "SIDECAR" operates. Kimmy is the SOC Coordinator. When a new ticket arrives, she delegates parallel read-only recon (e.g., Hound Dog extraction). She aggregates the data. Then, and only then, she asks Alpha (The Arbiter) for permission to execute the final destructive write to the codebase.


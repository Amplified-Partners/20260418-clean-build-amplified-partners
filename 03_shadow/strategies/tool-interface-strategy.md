---
title: Tool Interface Strategy
status: candidate
version: 0.1
date: 2026-05-02
last-revised: 2026-05-02
---

<!-- markdownlint-disable-file MD013 -->

# Tool Interface Strategy

## Attribution

- **Original source:** Ken Huang, "Chapter 2: The Tool Interface", Medium. Accessed via Ewan's subscription; downloaded by Ewan.
- **First adaptation:** Antigravity (AG) — adaptation date TBC.
- **Snapshot committed to repo:** Devin | 2026-05-02 | devin-5da3bd275191469c8400142fd0ae1d69 — committing the current working draft to bring it under version control at Ewan's request. Ewan continues to iterate on the live document; this is a snapshot for record-keeping, not a final version.

> Signatures are attribution checkpoints, not finality markers. This document continues to evolve as additional perspectives (Eli, Ewan, Devin, AG, others) are folded in. Subsequent revisions append additional signatures rather than overwriting prior ones.

---

### Core Thesis
Tools are the hands of the AI. A poorly designed tool interface leaves the harness blind to tool semantics, forcing it to treat every tool call as potentially dangerous. By strictly defining behavioral metadata (`isConcurrencySafe`, `isDestructive`), we allow the OpenClaw harness to optimize execution speed while maintaining absolute safety.

### 1. Zod Schema Validation (Input Safety)
Before a tool is ever executed, the incoming JSON from the LLM is validated against a strict schema.
- **Why it matters:** If Charlie hallucinates a tool argument (e.g., passing a string where an array is expected), the schema validation fails instantly and returns the error to the model. The underlying Python code *never* sees malformed input, eliminating an entire class of runtime bugs.

### 2. Behavioral Flags for Orchestration
Every tool registered in the OpenClaw harness must declare its behavior:
- `isConcurrencySafe`: Can this run in parallel? (e.g., `read_file` = True, `git_commit` = False).
- `isReadOnly`: Does this modify state? (If True, it is auto-approved by the Tier 1 permission gateway).
- `isDestructive`: Does this delete/overwrite data? (If True, triggers Tier 3 CISO approval).

### 3. Output Truncation (Memory Protection)
A critical feature for 24/7 autonomous agents is `maxResultSizeChars`.
- If Charlie runs a `grep_search` that returns 500,000 lines of output, keeping it in memory will crash the Python process and instantly blow out the LLM's context window.
- **The Solution:** The harness intercepts any output exceeding `maxResultSizeChars`, saves the full output to a temporary `.txt` file, and returns only a truncated preview to the LLM along with the file path. The agent can then use a targeted `read_file` with line numbers to inspect it safely.

### Amplified Partners Implementation
This defines the contract for how we will build the actual Python tools that Kimmy, Charlie, and Alpha use. We aren't just writing generic functions; we are building a typed, schema-validated, behaviorally-flagged Tool Registry that guarantees memory safety and predictable execution on the Hetzner bare-metal.


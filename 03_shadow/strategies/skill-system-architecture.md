---
title: Skill System Architecture (Hermes Pattern)
status: candidate
version: 0.1
date: 2026-05-02
last-revised: 2026-05-02
---

<!-- markdownlint-disable-file MD013 -->

# Skill System Architecture (Hermes Pattern)

## Attribution

- **Original source:** Ken Huang, "The Skill System Pattern" (April 2026), Medium. Accessed via Ewan's subscription; downloaded by Ewan.
- **First adaptation:** Antigravity (AG) — adaptation date TBC.
- **Snapshot committed to repo:** Devin | 2026-05-02 | devin-5da3bd275191469c8400142fd0ae1d69 — committing the current working draft to bring it under version control at Ewan's request. Ewan continues to iterate on the live document; this is a snapshot for record-keeping, not a final version.

> Signatures are attribution checkpoints, not finality markers. This document continues to evolve as additional perspectives (Eli, Ewan, Devin, AG, others) are folded in. Subsequent revisions append additional signatures rather than overwriting prior ones.

---

### Core Thesis
An agent without a skill system is bounded by its context window and the user's prompt. An agent with a skill system can accumulate and reuse procedural knowledge across thousands of sessions. We will adopt the **Hermes Agent Pattern** (dynamic, secure, agent-managed) rather than the basic Claude Code pattern (static `CLAUDE.md`).

### The Hermes Pattern for OpenClaw Skills
Our OpenClaw agents must treat "skills" as a first-class subsystem. Every skill should be a dedicated directory containing a `SKILL.md` file with YAML frontmatter.

#### 1. `SKILL.md` Structure
- **YAML Frontmatter:** Must define `name`, `description`, `version`, `platforms`, and `required_environment_variables`.
- **Markdown Body:** Defines the trigger conditions and step-by-step procedure.

#### 2. Progressive Disclosure (Context Engineering)
To save token costs and prevent context bloat, skills must be loaded progressively:
- **Tier 0:** Category names and counts.
- **Tier 1:** List of skill names and descriptions.
- **Tier 2:** Full `SKILL.md` content (loaded only when invoked).
- **Tier 3:** Supporting files (scripts, templates, references) loaded on-demand.

#### 3. Agent-Managed Creation (The Kaizen Loop)
When Alpha, Kimmy, or the Plumber solve a novel problem, they must codify the solution into a new skill.
- Skills are written atomically to disk.
- If a scan fails, the skill write is rolled back completely.

#### 4. Security Guardrails
Since agents can write their own skills or download community skills, all skills must pass through static analysis to block:
- **Exfiltration:** `curl` commands piped with secret API keys.
- **Prompt Injection:** "ignore previous instructions".
- **Destruction:** `rm -rf /`
- **Supply Chain Attacks:** `curl | bash` patterns.

### Amplified Partners Implementation
As we scale the OpenClaw fleet on Hetzner, the `skills/` directory in each Agent's workspace will follow this Hermes standard. This ensures the agents can self-improve safely without requiring Ewan (The Architect) to manually hardcode every new behavior.


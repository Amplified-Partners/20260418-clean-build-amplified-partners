---
title: Permission System Strategy
status: candidate
version: 0.1
date: 2026-05-02
last-revised: 2026-05-02
---

<!-- markdownlint-disable-file MD013 -->

# Permission System Strategy

## Attribution

- **Original source:** Ken Huang, "Chapter 4: The Permission System", Medium. Accessed via Ewan's subscription; downloaded by Ewan.
- **First adaptation:** Antigravity (AG) — adaptation date TBC.
- **Snapshot committed to repo:** Devin | 2026-05-02 | devin-5da3bd275191469c8400142fd0ae1d69 — committing the current working draft to bring it under version control at Ewan's request. Ewan continues to iterate on the live document; this is a snapshot for record-keeping, not a final version.

> Signatures are attribution checkpoints, not finality markers. This document continues to evolve as additional perspectives (Eli, Ewan, Devin, AG, others) are folded in. Subsequent revisions append additional signatures rather than overwriting prior ones.

---

### Core Thesis
A permission system is the difference between an autonomous agent and a catastrophic script. While IBAC checks semantic *intent*, the Permission System checks explicit *patterns* and enforces Human-in-the-Loop (HITL) gateways based on three distinct tiers of operation.

### 1. The Three-Tier Gateway Model
The OpenClaw harness will enforce a strict 3-tier hierarchy for all agent tool calls:

**Tier 1: Read-Only Recon (Auto Mode)**
- **Tools:** `read_file`, `git_log`, `grep_search`, `port_scan`
- **Execution:** Auto-approved. No human interaction required. The system simply logs `[AUDIT] AUTO-ALLOW` for compliance.

**Tier 2: Active Probing (Default Mode)**
- **Tools:** `run_command` (safe shell), `credential_check`
- **Execution:** Pings the Arbiter (Ewan/Alpha) with an interactive dialog asking for explicit approval before proceeding. Fails safe (denies) if no answer within 5 minutes.

**Tier 3: Destructive Actions (Plan Mode)**
- **Tools:** `git_push`, `isolate_host`, `write_to_file` (in production)
- **Execution:** Requires full CISO/Arbiter review of the *entire plan* before execution. A single `rm -rf` cannot fire without explicit sign-off on the broader goal.

### 2. Regex-Based Failsafes (DANGEROUS_PATTERNS)
Even with IBAC, the terminal tool must have a hardcoded regex failsafe. Before any shell command is executed, it is normalized (stripping ANSI escapes and Unicode fullwidth characters) and checked against a blacklist:
- `rm -rf /`
- SQL `DROP TABLE` or `DELETE FROM` without `WHERE`
- Fork bombs `:(){ :|:& };:`
- Piping remote content directly to shell (`curl ... | bash`)

If a command matches, it triggers an immediate Tier 3 hard block.

### Amplified Partners Implementation
This completes the security triumvirate for the Hetzner server:
1. **Hooks:** Pre/Post tool lifecycle interception.
2. **IBAC:** JWT-based intent validation (Cedar).
3. **Permission Tiers:** Hardcoded regex failsafes and tiered human-in-the-loop gating.

Charlie the Plumber cannot accidentally drop the production database, because the Regex Failsafe will catch the SQL pattern, override his permissions, and trigger a Tier 3 CISO approval prompt directly to Ewan's dashboard.


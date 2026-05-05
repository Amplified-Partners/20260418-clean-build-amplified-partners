---
title: 03_shadow/strategies/ — index and policy
status: candidate
version: 0.1
date: 2026-05-02
last-revised: 2026-05-02
---

<!-- markdownlint-disable-file MD013 -->

# `03_shadow/strategies/`

Status: **candidate** (non-authoritative). Per `03_shadow/README.md`, nothing in this folder is production truth until explicitly promoted via `00_authority/MANIFEST.md` and the normal review path.

## Why this folder exists

These files were drafted by Ewan locally — synthesised from Ken Huang's *Agentic AI* Medium articles, with first-pass adaptations by Antigravity (AG). On 2026-05-02 Ewan asked that they be brought into version control rather than continuing to live as local working drafts. Ewan named the gap explicitly: *"It should have gone through GitHub, but it's not. It's not completely agreed yet, although we are using it, which I know is wrong."* This folder closes that gap by giving the working drafts a permanent home with full attribution chain, while keeping their non-authoritative status visible.

This is the record of the gap, per Ewan's instruction: *"Put it in the GitHub. It's record. It's asynchronous, but it needs to be important because that's how we track things."*

## Index of current candidate strategies

| File | Topic | Source chapter |
|------|-------|----------------|
| `tool-interface-strategy.md` | Zod schema validation, behavioral flags (`isConcurrencySafe` / `isReadOnly` / `isDestructive`), output truncation | Ken Huang, "Chapter 2: The Tool Interface" |
| `skill-system-architecture.md` | Hermes Pattern, `SKILL.md` structure, progressive disclosure tiers, agent-managed skill creation, security guardrails | Ken Huang, "The Skill System Pattern" (April 2026) |
| `production-deployment-strategy.md` | `HERMES_HOME` per-agent isolation, Gateway service, vLLM air-gapped LLM, SDK streaming dashboard | Ken Huang, "Chapter 10: Production Deployment Patterns" (April 2026) |
| `permission-system-strategy.md` | Three-tier gateway, regex `DANGEROUS_PATTERNS` failsafe | Ken Huang, "Chapter 4: The Permission System" |
| `observability-strategy.md` | `chainId` distributed tracing, JSONL trajectory logging, `RedactingFormatter`, `CyberAuditLogger` pattern | Ken Huang, "Chapter 15: Observability and Tracing" |
| `multi-agent-coordination-strategy.md` | Worktree isolation, `MAX_DEPTH = 2`, interrupt propagation, prompt-cache forking | Ken Huang, "Chapter 7: Multi-Agent Coordination" |
| `model-routing-strategy.md` | Ordered fallback chain, smart routing by task complexity, API auto-detection | Ken Huang, "Chapter 14: Model Routing and Provider Abstraction" (May 2026) |

## The signature model used here (and worth using more widely)

Each file in this folder carries an `## Attribution` block near the top with the chain:

1. **Original source** — Ken Huang chapter, Medium, with Ewan's note on access.
2. **First adaptation** — Antigravity (AG).
3. **Snapshot committed to repo** — Devin, with date and session ID.
4. **Subsequent revisions** — appended below the line as additional signatures rather than overwriting prior ones.

> Signatures are attribution checkpoints, not finality markers. A document never has "an end" — it just accumulates more attribution as more contributors touch it.

This pattern is consistent with `00_authority/SIGNATURES.md` (every artefact signed) and Law 7 (radical attribution). It extends the model from "one signature per artefact" to "one signature per contribution to an artefact". Worth lifting to a `01_truth/processes/` SOP if it proves out.

## Naming substitutions applied at commit time

- `multi-agent-coordination-strategy.md` — `Ghost Sidecar` → `SIDECAR` (1 instance). Per Ewan's name-lock decision (2026-05-02): *"The sidecar is called the sidecar and that's it."* Original earlier-version naming superseded by the canonical product name. Recorded here rather than silently substituted.

## Promotion path

These files are not authoritative and do not become so by sitting here. Promotion requires:

1. Review by Eli (architecture / framing) and AG (operations / arbiter).
2. Resolution of internal inconsistencies (some are flagged in this commit's PR description — e.g., `HERMES_HOME` vs `OPENCLAW_HOME` in `production-deployment-strategy.md`, source attribution precision, aspirational-vs-implemented framing).
3. Decision recorded in `00_authority/DECISION_LOG.md` with version bump.
4. File moved to `02_build/` (build artefact) or `01_truth/` (process / interface) as appropriate, and indexed in `00_authority/MANIFEST.md`.

Until then: read these as working drafts, not as decisions.

## Cross-references

- Sovereign Fleet runtime (currently spec'd at v1, lives on the unmerged [`clean-build` PR #27](https://github.com/Amplified-Partners/clean-build/pull/27) branch — `02_build/sovereign-fleet/` does not yet exist on `main` `[SOURCE REQUIRED]`) — these strategies effectively spec a v2 of that runtime.
- Beast / Hetzner infrastructure: `02_build/INFRASTRUCTURE.md` (authoritative).
- Sovereign Fleet PR currently held pending L5 + IBAC: [`Amplified-Partners/clean-build` #27](https://github.com/Amplified-Partners/clean-build/pull/27).
- Authority index: `00_authority/MANIFEST.md`.

Signed-by: Devin | 2026-05-02 | devin-5da3bd275191469c8400142fd0ae1d69

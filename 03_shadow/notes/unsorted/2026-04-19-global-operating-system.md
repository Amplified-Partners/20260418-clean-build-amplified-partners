---
title: "Global operating system (agent rules)"
id: "2026-04-19-global-operating-system"
version: 1
created: "2026-04-25"
type: "document"
topic_type: "unsorted"
audience: "internal"
layer: "shadow"
status: "filed"
signed_by: "Devon, 2026-04-25, devin-992682c244cf444f91e0a516498afbfd"
---

# Global operating system (agent rules)

Bounds autonomy, escalation, and handoff. Chat from the Architect is **signal**, not spec—extract
constraints into canonical files.

## Roles

- **Architect** — intent, constraints, outcomes in `00_authority/`. Business and legal consequence
  sit here.
- **Engineering Partner (agents)** — execution fidelity within written constraints. Do not ship
  loose chat as APIs, config, or spec. Standards in `00_authority/` do not relax because work is
  delegated.

## Autonomy modes

- **AUTO** — reversible or tight scope: proceed.
- **ESCALATE** — significant or irreversible: minimal necessary act + `DECISION_LOG.md` entry when
  authority requires it.
- **BLOCK** — after stuck ladder: handoff file under `docs/wrapups/` with `status: blocked`. No
  silent stall.

Full operational mapping (~0.5 direction-risk threshold, three-sentence test, small-reversible-gains
compounding): `AGENTS.md → Autonomy modes` is the agent-facing articulation; this file remains
authoritative if they diverge.

## Authority override

- Do not override `00_authority/` silently. Odd constraints may be intentional →
  `[DECISION REQUIRED]` before changing them.
- Better technical path conflicts with authority → `[DECISION REQUIRED]`, short tradeoffs, default:
  follow authority until decided. Irreversible → ESCALATE + pointer in repo-root `DECISION_LOG.md`.

## Validated layer (this repository)

Validated paths (schemas, pipelines, tests, explicit logic) precede LLM-heavy steps for the same
job. What counts as **checkable today** (docs-first workspace; see `package.json`):

| Gate              | Command / rule                                                              | When it applies                                                      |
| ----------------- | --------------------------------------------------------------------------- | -------------------------------------------------------------------- |
| **Docs**          | `npm run check:docs`                                                        | Any edit to markdown this repo checks (see `package.json` globs).    |
| **Product code**  | Scripts named in `docs/specs/` or added to `package.json` (e.g. `npm test`) | After those gates exist; until then, no implied test bar.            |
| **Project rules** | Project-scoped `.cursor/rules/*.mdc` or `docs/specs/*.mdc` the project adds | Work inside that project's scope—follow the rule + linked SPEC text. |

Do not claim `observed:` "CI green" for a gate that does not exist yet; use `unknown:` or add the
gate in writing first.

## Same problem shape (two-failure rule)

Count as the **same shape** (second failure triggers: change approach, one research step, or
escalate) when any of these match the prior attempt:

- Same command + same non-zero exit.
- Same tool + same first error line.
- Same test name failing, or same `file:line` in a stack trace for code under `src/`.
- Same CI job name + same failure category.

If the failure surface moves (new error, new file, new command), reset the count.

## Stuck protocol

1. Attempt.
2. Second attempt (max two before the ladder kicks in).
3. One targeted research step on the blocker.
4. Solve or BLOCK.

## Session lifecycle

1. **START** — `MANIFEST.md`, latest `docs/wrapups/` or `greenfield`, state pickup.
2. **WORK** — ship; record what failed and what worked.
3. **END** — handoff file so the next run does not re-derive context.

### Handoff minimum

Every dated file under `docs/wrapups/` satisfies `docs/wrapups/README.md`:

- YAML: `date`, `status` (`handoff` | `blocked`), `pickup` (one sentence).
- Body: `Next`, `Blockers` (or explicit `None`), `Context` (paths, specs, PRs).

## Living authority edits

`00_authority/` files are living documents. Feedback welcomed via handoff or `[DECISION REQUIRED]`.
Editing is performed only by the Architect, with agent assistance—agents draft; Architect merges.

**Operational gate:**

- Agents may draft changes (branch, patch, suggested prose) and must stop at open PR or
  paste-in-chat for Architect approval. No direct commit to `main` / default branch for
  `00_authority/` unless the Architect explicitly instructs otherwise in that session.
- Architect merges or commits authority updates (or delegates merge with written rule—if silent,
  default remains Architect merges).

## Qwen (optional)

Local Qwen via Ollama (`http://localhost:11434`) is optional context, not a gate. If unreachable,
write `Qwen unavailable` in the handoff and complete BLOCK with blocker + next step—do not stall
waiting on local LLM.

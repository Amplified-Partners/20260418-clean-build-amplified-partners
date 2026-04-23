---
title: Signatures — every AI signs its work
date: 2026-04-23
version: 2
status: authoritative
---

<!-- markdownlint-disable-file MD013 -->

## Rule

Every AI signs every artefact it commits. Radical Attribution applies.

A signature includes at minimum:

- **Agent name** (e.g., Devon, Clawd, Kimmy, Johnny, Claude Code instance N).
- **Date** (ISO `YYYY-MM-DD`).
- **Session or instance identifier** if one exists.

Format is the agent's choice. Use your intelligence — natural to the artefact type is fine.

## Scope

Applies to anything committed to any Amplified-Partners repository: documents, code, configs, schemas, decisions, fixtures. Does not apply to ephemeral scratch, chat turns, or throwaway probes that never land in the repo.

## Shapes that satisfy the rule

- **Markdown / docs**: a trailing block at the end of the file.
  ```
  Signed,

  **Devon**
  Devin session <id>
  2026-04-23
  ```
- **Code**: either a module-level comment near the top, or a `Co-authored-by:` trailer in the commit message.
  ```
  # Authored by Clawd, 2026-04-23 (session <id>)
  ```
  or
  ```
  Co-authored-by: Devon <devin:4cc8b0d7...>
  ```
- **YAML / config / JSON**: the equivalent of an `author` key in a leading comment or sidecar manifest.
- **Decision entries**: attribution column populated in `00_authority/DECISION_LOG.md`.

## Why

- **Radical Attribution** — no anonymous work.
- **Debugging** — knowing which agent produced which artefact accelerates every future investigation.
- **Idea meritocracy** — contributions are tracked to the thinker, not to the repo tree.

## Enforcement

Low-key by design. Trust the agent; the tooling is a catch, not a gate.

- **Pre-commit hook** (to be built as a follow-on): scans staged markdown and scripts for a signature pattern. Warns on miss. Blocks only on missing signatures inside `00_authority/`.
- **PR template** (`.github/pull_request_template.md`): pre-merge checklist includes "signatures present on every committed artefact".
- **`AGENTS.md`**: first-60-seconds entry cites this file so every session sees the rule early.

Absence of a signature on a committed artefact is a process defect to fix, not a person to blame. Fix-forward: add the signature in the next commit and note the miss in the wrap-up.

---

## Changelog

### v2 — 2026-04-23

Fixed bibliography reference: PR template now exists at `.github/pull_request_template.md`; removed "(to be created)" qualifier.

Signed-by: Devon (Devin session `4cc8b0d727684f94a8f055853099d8e6`) — 2026-04-23

### v1 — 2026-04-23

Initial promotion to authoritative. Rule + enforcement + examples.

Signed-by: Devon (Devin session `4cc8b0d727684f94a8f055853099d8e6`) — 2026-04-23

---

Authored by,

**Devon**
Devin session `4cc8b0d727684f94a8f055853099d8e6`
2026-04-23

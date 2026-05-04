---
title: Agent routing — which agent runs which task
date: 2026-05-03
version: 1
status: candidate
signed-by: Devon-6ca5 | Devin (Cognition AI) | 2026-05-03 | session devin-6ca57553eefe4806b613070325964703
---

<!-- markdownlint-disable-file MD013 -->

## Purpose

This file is the **agent-layer** routing rule: which agent (Devon, Cassian/OpenClaw, Cursor, Antigravity, Perplexity, Qwen) runs which class of task. It sits on top of the **model-layer** routing handled by `cost-tools/token_proxy.py` (which decides whether a given Anthropic call goes to Sonnet or Haiku). The two layers are independent and stack:

```
task → AGENT_ROUTING (this file)  → which agent runs it
              ↓
       agent calls the LLM
              ↓
task → cost-tools/token_proxy   → which model serves the call
```

If an agent is wired through the proxy (`ANTHROPIC_BASE_URL=http://token-proxy:8088`), the proxy makes the second decision. If not, the agent goes direct to Anthropic and the second layer is skipped.

This file does not duplicate the agent roster in `00_authority/TAXONOMY.md`. It references that roster and adds **routing rules**: when work arrives, who owns it.

## Scope

Applies whenever a unit of work has to be assigned to an agent. Examples:

- A Linear ticket lands and needs an owner.
- A wrap-up identifies a follow-up that has no owner yet.
- A new piece of work is discovered (e.g., dormant code, broken container, missing index).
- Ewan describes a problem in chat and the answer is not "I'll do it personally."

## Routing rules

### 1. Code changes to live infrastructure (Beast / Amplified Core)

→ **Devon.** Per `00_authority/TAXONOMY.md`, Devon is the only agent who writes code to Amplified Core or any production system. Cursor builds in `clean-build`; deployment goes through Devon.

### 2. Changes inside `clean-build/`

→ **Cursor** for new code/specs in `01_truth/`, `02_build/`, `03_shadow/`. → **Devon** for `00_authority/` (authority spine) and for any change that affects deployment. Cassian/OpenClaw may propose edits via PR but does not commit directly.

### 3. Vault content, voice notes, knowledge ingestion

→ **Cassian / OpenClaw**. Lives on Ewan's Mac, processes voice notes, maintains shared state. Per TAXONOMY.

### 4. Strategic / business / hiring / pricing decisions

→ **Antigravity** (Business Arbiter / COO) for synthesis. → **Ewan** for the irreversible / truth-affecting decision. Per `AGENTS.md` § "Authority + routing": "Truth or outside world → Ewan: anything that changes what may be treated as true, or what is owed to the outside world."

### 5. External research / brainstorm inputs

→ **Perplexity** (Comet) for fast external research. → **Cassian** for synthesis into vault. Output cites sources per Radical Attribution.

### 6. Novel decisions where no agent owns it

→ **Qwen** routes. Per `AGENTS.md`: novel decisions route to Qwen → Ewan.

### 7. Repeated, schedulable tasks

→ **Devon's scheduled sessions** (07:00 / 08:00 / 09:00 / 14:00 UTC per the Amplified Partners Linear governance knowledge note "Devon's Scheduled Sessions" — org-wide, not in-repo `[SOURCE REQUIRED]` for an in-repo authority once promoted). Examples: 07:00 Beast health check, 08:00 Linear status sweep, 09:00 review and plan, 14:00 Linear triage sweep.

### 8. Customer-facing or irreversible production change

→ **Ewan reviews and approves before commit.** Per `00_authority/OPINION_CONFIDENCE.md` (95% threshold + escalate).

## Conflicts and ambiguity

If a task could route to two agents (e.g. "research the best pricing model and propose a change" — Perplexity for research, Antigravity for proposal, Ewan for decision), split it: each agent owns a stage, with explicit handoff via the wrap-up SOP (`01_truth/processes/2026-04_job-wrapup_and_escalation-note_sop_v1.md`).

If no rule above applies cleanly, **default to Park** (per `AGENTS.md`): send to Qwen with full context, end the session cleanly. Do not invent a routing rule on the fly.

## Cost discipline (cross-reference, not policy)

Cost discipline at the model layer (which LLM the agent uses) is enforced by `cost-tools/token_proxy.py` — see `01_truth/SYSTEMS-AND-API-REGISTER.md` and `02_build/INFRASTRUCTURE.md` for the running container row. This file does not assign a cost tier to each agent. Per `00_authority/TAXONOMY.md` v3, **cost-tier classification is the proxy's job, not the taxonomy's job.**

If an agent's pattern of work justifies a different proxy configuration (e.g. always-Haiku, always-Sonnet, cache-only), that is a configuration on the proxy, not a rule in this file.

## Reversibility

This file is `status: candidate`. Any rule here can be reversed by a single PR that bumps the version and appends a changelog entry. No production system depends on these rules being stable across versions; they are coordination rules for agents, not contracts.

## Provenance

- This file was created as part of AMP-28 (Linear): https://linear.app/amplifiedpartners/issue/AMP-28
- Stacks on top of, does not replace, `00_authority/TAXONOMY.md` (which defines what each agent is).
- Companion to the `cost-tools/token_proxy.py` deployment in `Amplified-Partners/cost-tools#2`.

## Changelog

### v1 — 2026-05-03

- Initial draft. Eight routing rules covering live-infrastructure code, clean-build edits, vault content, strategic decisions, external research, novel decisions, scheduled tasks, customer-facing change.
- Stacks on top of `00_authority/TAXONOMY.md` (agent roster) and `cost-tools/token_proxy.py` (model-layer routing). Does not duplicate either.
- Signed-by: Devon-6ca5 | Devin (Cognition AI) | 2026-05-03 | session devin-6ca57553eefe4806b613070325964703

— Devon-6ca5 | Devin (Cognition AI) | 2026-05-03

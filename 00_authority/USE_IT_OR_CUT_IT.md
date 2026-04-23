---
title: Use-It-Or-Cut-It — unused ideas are cut
date: 2026-04-23
version: 1
status: authoritative
---

<!-- markdownlint-disable-file MD013 -->

## Rule

**If an idea sounds good, gets implemented, and never gets used, it's cut.**

## Scope

Applies to anything committed to an Amplified-Partners repository: features, scripts, agents, principles, processes, infrastructure, tooling. Applies to ideas no matter who proposed them — Ewan, any AI agent, any partner.

## Why

Two failure modes the rule prevents:

1. **Bloat.** Unused implementations clutter the surface, confuse new agents, and drag maintenance cost without returning value.
2. **Sunk-cost preservation.** Once something exists, it's psychologically harder to remove than it was to add. The rule cancels that bias by making unused = cut by default.

Pairs with the prevention principle: *"Is it useful?"* asked before building. Use-It-Or-Cut-It is the remediation when prevention missed.

## Application

1. **Cadence**: reviewed at session wrap-up and at scheduled repo audits (monthly is a candidate cadence; not mandated).
2. **Evidence of use**: imports, invocations, references in commits/logs within the review window. Mere presence in the repo is not use.
3. **Grace period**: new additions have a one-cycle grace before the rule bites. After that, use-or-cut applies.
4. **Cut means remove**: file deleted, references purged, change logged. Not "archived for later" — archival is itself implementation-not-used.
5. **Exception: reference/provenance**. Items under `90_archive/` and audit trails (superseded baton passes, prior decisions, historical snapshots) are **not** subject to this rule. They exist for provenance, not for use.

## Counter-test before cutting

Two **gates**. Both must be cleared before the cut — they shape *how* to cut, not *whether*.

1. **Tried?** If not — run one test first. Do not cut blind.
2. **Load-bearing?** If yes — migrate dependents first.

Sequence by risk:

- **Tried + not load-bearing** → cut now. Safest, clearest case.
- **Tried + load-bearing** → migrate dependents, then cut.
- **Not tried + not load-bearing** → test; if still unused, cut.
- **Not tried + load-bearing** → migrate dependents, test, then cut. Hardest case. If the gate-clearing cost exceeds the bloat cost, log and defer to the next cycle.

## Interaction with other rules

- **SIGNATURES.md**: the cutter signs the removal, like any other commit.
- **OPINION_CONFIDENCE.md**: cut decisions below the reversibility threshold are reversible by restoring from git history; cuts that delete external state (customer data, third-party accounts) are irreversible and subject to the 95% / escalate rule.
- **Stateless-handover neutrality clause**: when proposing a cut in a handover, state the evidence of non-use and leave the decision to the next agent or to Ewan. Do not cut on behalf of the reader.

## Example applications

- A workflow defined six months ago, never invoked → cut.
- A principle written once, never cited in a decision → cut.
- An integration built speculatively for a customer pattern that never materialised → cut.
- An archive snapshot in `90_archive/` that is by definition non-authoritative → **not** cut (exception 5).

---

Authored by,

**Devon**
Devin session `4cc8b0d727684f94a8f055853099d8e6`
2026-04-23

---
title: Compound Engineering after-action — ingestion task template
date: 2026-05-11
version: 1
status: candidate-authority
lane: AMP-302 engineer C
signed_by: Devon-AMP-302-C
linear: AMP-302
---

<!-- markdownlint-disable-file MD013 -->

## Why this template exists

Cove ingestion is being hardened into a controlled production facility.
Every ingestion task — feature, fix, rerun, schema change, even
"investigated something and decided not to change it" — should leave
behind a short after-action note so that:

- the next agent does not have to re-derive what was tried,
- the guard surface grows over time instead of decaying,
- the Compound Engineering loop (Plan → Work → Review → Compound) has
  a real artefact at the Compound step.

Drop the filled-in note into `03_shadow/` with the filename pattern
`YYYY-MM-DD_ingestion-<short-slug>_after-action.md`.

Keep it short — a tight one-pager is more useful than a long essay no
one reads. If a section does not apply, write **N/A** rather than
deleting it; the structure itself is the contract.

---

## After-action — `<short title>`

**Lane / engineer**: `<AMP-### engineer ID>`
**Date (UTC)**: `<YYYY-MM-DD>`
**Linear**: `<ticket>`
**Branch / PR**: `<branch>` / `<PR URL>`
**Signed-by**: `<agent-id>`

### 1. What changed

One paragraph. The diff in plain English — what code/docs/config moved.
Link to the PR for the precise file list; do not paste it here.

### 2. What problem was this trying to solve

Why was this task picked up? What was the user-visible or
operator-visible failure mode, drift, or risk that motivated the work?
If the answer is "preemptive hardening," say so explicitly.

### 3. What we tried that did not work

The honest part. Approaches considered and rejected, dead ends hit,
assumptions that turned out to be wrong. **Required even on
green-path tasks** — "tried nothing else, the obvious approach worked"
is itself a useful signal for future agents.

### 4. Tests added or changed

- `<test file>` — what it asserts and which guard/contract it locks.
- Any tests deleted or weakened, and why.

If no tests were added, justify it. (Acceptable reasons: docs-only
change, deletion of dead code, change inside an already-tested
contract.)

### 5. What guard prevents recurrence

The single most important section.

- Concrete guard (test, lint, fail-closed env var, schema constraint,
  CODEOWNERS rule, runbook gate) that would have caught the original
  drift had it existed.
- Where the guard lives and how it fires (CI? import time? runtime?).
- What the failure message looks like when the guard catches a
  regression — so a future agent sees the right pointer and does not
  weaken the guard to "make the test pass".

If the answer is "no guard added," explain why a guard would be
disproportionate. Default expectation is one new guard per ingestion
task.

### 6. What future agents should read first

Ordered list of 2–5 file paths. The smallest reading list that lets
the next agent pick up where this one stopped without re-discovering
context.

Example:
1. `02_build/brain-migration/RUNBOOK_LEGACY_FREEZE.md`
2. `02_build/cove-orchestrator/temporal/activities/ingestion_activities.py`
3. This after-action.

### 7. Open follow-ups (not done here, on purpose)

Bullet list. For each, who owns it (or "unassigned") and the trigger
that should pick it up. Distinguishing "deferred" from "missed" is the
whole point.

### 8. Compounding note

One sentence: how does this task make the next ingestion task cheaper
or safer? If it does not, that is itself worth recording — three of
those in a row is a process smell worth raising with Ewan.

---

## Worked example (delete when copying)

> **After-action — Legacy writer quarantine (AMP-302 engineer C)**
>
> **1. What changed**: Added `migration_guard.py` and
> `brain_mcp_write_guard.py`; wired both into `migrate_qdrant.py`,
> `migrate_falkordb.py`, and `brain_mcp_server.py`; created
> `RUNBOOK_LEGACY_FREEZE.md` and this template; added 22 tests under
> `02_build/brain-migration/tests/`.
>
> **2. Problem**: Three writers could mutate `amplified_brain` with
> no acknowledgement that they were bypassing the canonical Temporal
> activity. The 57,297 duplicate-vector wave is attributed to this
> exact failure mode.
>
> **3. What did not work**: Tried inlining the side-door resolver in
> `brain_mcp_server.py`; could not unit-test it without the FastAPI
> stack. Extracted it to `brain_mcp_write_guard.py` as a pure
> function, which became testable. Also tried importing `redis` at
> module top in `migrate_falkordb.py` — but the guard then ran
> *after* the redis import, so a missing-dep error masked the
> refusal. Moved `import redis` into `main()` so the guard runs first.
>
> **4. Tests**: `tests/test_migration_guard.py` (env-var combinatorics,
> canonical-ack required); `tests/test_brain_mcp_write_guard.py`
> (resolver matrix); `tests/test_legacy_writers_blocked.py`
> (subprocess proof that the entrypoints exit 2 without protocol).
>
> **5. Guard**: `enforce_or_exit(DB_NAME, script_name=...)` runs as
> the first statement of `main()` in both legacy ETL scripts and
> fails closed unless four env vars + a canonical-DB ack are
> present. CI runs the test suite; a regression that weakens the
> guard fails `test_legacy_writers_blocked.py`.
>
> **6. Read order**:
> 1. `02_build/brain-migration/RUNBOOK_LEGACY_FREEZE.md`
> 2. `02_build/brain-migration/migration_guard.py`
> 3. `02_build/cove-orchestrator/temporal/activities/ingestion_activities.py`
>    (the canonical writer)
>
> **7. Follow-ups**:
> - Move `migrate_qdrant.py` / `migrate_falkordb.py` to `90_archive/`
>   once canonical DB stable for one quarter (unassigned; trigger: no
>   ingestion incident through 2026-Q3).
> - Audit `/opt/amplified/.../memory_writer.py` against canonical
>   invariants and either reabsorb or shut down (Ewan / engineer D).
> - Remove `brain_mcp_server.py` write endpoints once Temporal
>   covers all callers (engineer A; trigger: zero
>   `BRAIN_MCP_WRITE_ACK` invocations for 30 days).
>
> **8. Compounding note**: Future ingestion writers must thread
> through `migration_guard` — the cost of adding a new safe writer
> is now one decision-log entry and one `enforce_or_exit` call;
> the cost of adding an unsafe writer is a failing test and a PR
> rejection. The asymmetry compounds.

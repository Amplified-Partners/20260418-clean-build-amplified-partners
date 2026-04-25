---
description: The standard operating process for all work — chat, research, plan, execute, document, review. No shortcuts.
---

# The Amplified Way — How We Work

Every piece of work follows this process. No exceptions. No shortcuts.

## 1. Chat
- Discuss the idea, understand the goal
- Ask questions, clarify scope
- Agree on what "done" looks like

## 2. Research
- Deep research into the problem space
- Stand on the shoulders of giants — find who's solved this before
- Read official docs, reference implementations, best practices
- Compare approaches honestly (at least 2-3 options)
- This takes seconds now and saves hours later

## 3. Plan
- Write an `implementation_plan.md` with:
  - Background and context
  - Proposed changes (grouped by component)
  - Verification plan
- Get approval before writing a single line of code
- If feedback comes, update the plan and re-review

## 4. Execute
- Build it properly — the right way, not the quick way
- Work at 70% capacity — no rushing, no panic
- Follow the plan. If the plan needs changing, go back to step 3

## 5. Document
- Update `task.md` as you go (checkboxes: `[ ]` → `[/]` → `[x]`)
- Write a `walkthrough.md` when done:
  - What was built
  - What was tested
  - Validation results
  - Screenshots/recordings where relevant
- Leave it clean for the next person — the baton pass is everything

## 6. Review
- Rate the work honestly (1-10)
- Note where we could have done better
- This helps the next person (including future us)

## When Things Go Wrong

The diagnosis IS the work. The fix is the easy part.

1. **STOP** — don't immediately try to fix, change, or rewrite
2. **Research the possible causes** — what could cause this exact symptom?
3. **Make a short list** — write down the 3-5 most likely causes
4. **Check each one systematically** — quick look, eliminate or confirm
5. **Fix once** — now you know what the problem actually is

**Never**: try a fix, fail, try a different fix, fail, try another architecture.
**Always**: find the problem first, THEN fix it.

If three different solutions all fail the same way, the problem isn't the solution — it's something they all share. Stop and ask: what do all my attempts have in common?

## The Rules

- **No shortcuts** unless there's a genuinely good reason (and document why)
- **Clean up after yourself** — no loose ends, no half-finished code
- **70% capacity** — sustainable pace, no burning out
- **Document everything** — if it's not written down, it didn't happen
- **Baton pass** — anyone picking this up next should understand what was done and why
- **Every single time** — this process is non-negotiable

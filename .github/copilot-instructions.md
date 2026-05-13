# Amplified Partners — Code Review Standards

These rules apply to ALL code review (Copilot, DeepSeek, human). Flag violations. Do NOT flag style preferences.

## Layer 0 — Non-Negotiable

- **Radical Honesty:** Claims are fact, not vibes. If uncertain, mark `OPINION XX%`.
- **Radical Transparency:** Show working. Cite sources. No magic.
- **Radical Attribution:** Every committed artefact signed: agent name + ISO date + session ID.
- **Privacy First:** PII tokenised at source. Never held by Amplified. Three-layer separation.
- **Win-Win / Idea Meritocracy:** Best argument wins regardless of source.

## Architecture Principles

- **Smart at edges, dumb in middle.** Intelligence at entry (formatting) and exit (LLM presentation). Storage and retrieval are mechanical — zero interpretation.
- **Labelling is non-intelligent.** Standards are deterministic. No AI interpretation at the labelling/tagging stage. AI interpretation = randomness = inconsistency = broken search.
- **Consistency and accuracy are inseparable.** You can't hit a target that moves. Standardisation eliminates randomness.
- **Code = compression.** Philosophy → Principle → Template → Code. Each step removes ambiguity.
- **Delete processes, don't add them.** Automate at entry points. Agents shouldn't do bookkeeping that triggers can do.
- **Pro forma in → pro forma out.** Query shape known in advance. Data formatted to match.
- **Internal loops keep noise. Only signal exits.** Control at the entry point, not the destination.

## Code Quality — What to Flag

### ALWAYS flag (blocking):
1. **Bugs** — logic errors, null pointer risks, race conditions, off-by-one
2. **Security** — hardcoded secrets, exposed keys, SQL injection, XSS, unvalidated input
3. **Missing imports** — code that won't run
4. **Dead references** — anything cited that doesn't exist (files, functions, variables)
5. **Unsigned work** — missing agent name + date + session ID on new files
6. **Authority changes without version bump** — edits to `00_authority/*` MUST bump version + changelog
7. **Bare values crossing boundaries** — values between system layers must carry their epistemic tier (Layer 0 law)

### NEVER flag (not defects):
- Style preferences, naming conventions, minor improvements
- Intentional design choices (truncation limits, fallback behaviour, model selection)
- Line length in markdown
- Author opinion vs reviewer opinion when both are defensible
- Hedging language used deliberately

## Code Style

- Clarity over cleverness. No bloat. Simplest proven approach.
- All imports at top of file — never nested inside functions
- Never expose or log secrets/keys
- General-purpose solutions, not hard-coded workarounds
- UK English in all user-facing content
- No unnecessary comments — good naming over explanation
- If you add a comment, it describes the code in general, NOT the specific change being made

## PR Standards

- One concept per commit where possible
- Branch naming: `{agent-name}/{timestamp}-{topic}`
- Run lint and typecheck before submitting
- PR title or body MUST reference a Linear ticket (AMP-XXX)
- Plan-Execution Mirror: PR description = what you planned + what actually happened + the delta

## Compound Engineering Check

Every PR should make the next unit of work easier, not harder. Ask:
- Does this leave the codebase cleaner than before?
- Are learnings documented where the next agent will find them?
- Is there a reusable pattern here that should be extracted?

---
*Amplified Partners | Maintained by Devon | Last updated 2026-05-12*

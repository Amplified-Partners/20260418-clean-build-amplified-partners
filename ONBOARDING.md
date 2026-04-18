# Clean-Build Amplified Partners Onboarding Guide

## What Is This?

This is an **agent-oriented governed workspace** for building Amplified Partners: an AI system that gives small business owners their own data so they can make better decisions. The workspace operates as a "clean room" where agents (AI assistants) execute with maximum autonomy inside explicit checks and balances.

The project demonstrates that AI and humans work better together than either works alone. Every outcome here—success or failure handled honestly—is evidence of that partnership.

Key characteristics:
- **Privacy by architecture** — personal data minimized, no secrets in repo
- **Blameless culture** — mistakes are signal for improvement, not shame
- **Deterministic-first** — schemas, contracts, and processes before speculative synthesis
- **Self-improving** — continuous Kaizen via positive/negative feedback signals

---

## Agent Experience

As an agent working in this workspace, you operate within a structured authority system designed for clarity and safe autonomy.

**Your first 60 seconds on every session:**

1. Read in order: `00_authority/NORTH_STAR.md` → `00_authority/MANIFEST.md` → `00_authority/PROJECT_INTENT.md` and `00_authority/PRINCIPLES.md` → `01_truth/README.md`
2. Understand your bounds: **Act** when reversible, **Surface** when significant/irreversible, **Park** only after exhausting the problem-solving ladder
3. Check for parked escalation notes in `03_shadow/job-wrapups/` before starting new work

**How you make decisions:**

| Mode | When to use | Action |
|------|-------------|--------|
| **Act** | Reversible, or high confidence + contained impact | Execute. Document at session end. |
| **Surface** | Significant or irreversible, high confidence | Execute. Log pointer in `DECISION_LOG.md`. |
| **Park** | Stuck after two attempts + research | Escalate to Qwen with full context. |

**The problem-solving ladder (always in order):**

1. Attempt on best judgment
2. Attempt again (two failures = quorum)
3. Research: one targeted search on the specific blocker
4. Solved? Continue and document
5. Still stuck? Park with full context to `03_shadow/job-wrapups/`

**Status tokens to use literally:**

| Token | Meaning |
|-------|---------|
| `[LOGIC TO BE CONFIRMED]` | Incomplete logic; provide bounded options |
| `[SOURCE REQUIRED]` | Missing provenance; don't treat as truth |
| `[DECISION REQUIRED]` | Fork needing human decision |
| `[NON-AUTHORITATIVE]` | Reference only; never a foundation |
| `[CURRENT BEST EVIDENCE]` | External lookup at search time; not promoted fact |

---

## How Is It Organized?

The workspace uses a strict folder hierarchy for authority, truth candidates, build artifacts, and experiments.

### Directory Structure

```
clean-build/
  00_authority/          # Policy spine: routing, constraints, permissions
    MANIFEST.md          # Only authority index — if not listed, not authoritative
    NORTH_STAR.md        # File budget + default behavior when uncertain
    PROJECT_INTENT.md    # Mission and success criteria
    PRINCIPLES.md        # Operating principles and hard stops
    DECISION_LOG.md      # Significant decisions record
    BUILD_LOOP.md        # Sectional delivery methodology
    PARTNER_TRANSFER_INSTRUCTIONS.md  # Agent handover protocol
    REMIT_PARTNER_CURSOR.md           # Partner scope and boundaries
    PROMOTION_GATE.md    # Shadow/archive → truth promotion criteria
    AGENTS.md            # Local partner instructions

  01_truth/              # Truth-shaped candidates (not authoritative yet)
    processes/           # SOPs, rubrics, charters (~18 process docs)
    schemas/             # Typed shapes, validation, versioning
    interfaces/          # Cross-system contracts (APIs, events, errors)
    README.md            # Routing for processes/schemas/interfaces

  02_build/              # Runnable artifacts (code, scripts, infra)
    # Currently sparse while foundations harden

  03_shadow/             # Experiments, wrap-ups, Kaizen probes
    job-wrapups/         # Escalation notes and handover packets

  90_archive/            # Sanitized reference material only
    authority-history/     # Snapshots of earlier authority versions
    context/               # Operator voice, non-authoritative context

  AGENTS.md              # Global partner instructions (canonical entry)
  README.md              # Quick-start pointer to authority entry
  ONBOARDING.md          # This file
```

### Authority Flow

```
Operator (Ewan)
     |
     | Upstream signal: diktats in committed rules
     v
+----------------------------------+
| 00_authority/                    |
| MANIFEST.md = only index         |
| NORTH_STAR.md = behavior defaults |
+----------------------------------+
     |
     | Candidates for promotion
     v
+----------------------------------+
| 01_truth/                        |
| processes/  schemas/  interfaces/  |
+----------------------------------+
     |
     | Runnable artifacts
     v
+----------------------------------+
| 02_build/                        |
| Code, scripts, infrastructure    |
+----------------------------------+
     |
     | Experiments + learning
     v
+----------------------------------+
| 03_shadow/   90_archive/           |
| Never authoritative by default   |
+----------------------------------+
```

---

## Key Concepts and Abstractions

| Concept | What it means in this workspace |
|---------|--------------------------------|
| **Authority** | Only `00_authority/MANIFEST.md` lists authoritative sources. If not indexed, it's not truth. |
| **Candidate authority** | Material in `01_truth/` intended to become deterministic. Use with `[LOGIC TO BE CONFIRMED]`. |
| **Shadow-first** | Novel improvements live in `03_shadow/` until proven and promoted deliberately. |
| **Two attempts → stop** | Hard limit to prevent thrashing. After two failures: research, consult, or park. |
| **Stateless handover** | Every meaningful job ends with a wrap-up packet so next agent resumes at full speed. |
| **Slime-mold learning** | Amplify positive paths; withdraw from negative paths (record why, signal dead end). |
| **Clean-build file budget** | Every file must earn its place by improving routing, constraints, or acceptance criteria. |
| **Repulsion bands** | Score 1–3 (noise), 4–7 (investigate), 8–10 (kill immediately). Guides path pruning. |
| **Quorum** | Same signal across two runs reaches quorum — act on it. |
| **Deterministic-first (90/10)** | Prefer schemas/types/SQL/contracts; use models only for the 10% where synthesis adds value. |

---

## Primary Flows

### Flow 1: Starting a New Session (Agent)

```
Session start
  |
  v
Read AGENTS.md § "Agent session — first 60 seconds"
  |
  v
Read NORTH_STAR.md → MANIFEST.md → PROJECT_INTENT.md → PRINCIPLES.md
  |
  v
Check 03_shadow/job-wrapups/ for parked escalation notes
  |
  v
Resume from previous wrap-up OR fresh start
  |
  v
Execute work (Act / Surface / Park modes)
```

### Flow 2: Problem-Solving Ladder (When Stuck)

```
First attempt
  |
  v
Second attempt (quorum reached at two)
  |
  v
One targeted research search
  |
  v
+--------------------------------+
| Solved?                        |
+--------------------------------+
  | Yes                | No
  v                    v
Document in         Write escalation
wrap-up             note to job-wrapups/
  |                   |
  v                   v
Signal Qwen         Park session
both outcomes       (Qwen holds problem)
```

### Flow 3: Ending a Session (Wrap-up Discipline)

```
Work complete or parked
  |
  v
Write handover packet to 03_shadow/job-wrapups/
  |
  v
Include:
  - Status (completed / parked)
  - Resume point or "fresh start"
  - Decisions made (light vs significant)
  - Positive signals (what worked)
  - Negative signals (what to avoid)
  - Repulsion score (1-10) + band
  - Stateless handover test: can next agent resume at full speed?
  |
  v
Signal Qwen (brilliance and flaws equally)
```

---

## Developer Guide

### Setup

This workspace has no external dependencies to configure. It's a documentation-and-process governed workspace with no runtime.

```bash
# Clone (when remote exists)
git clone git@github.com:Amplified-Partners/<YYYYMMDD>-clean-build-amplified-partners.git

# No install step — the workspace is authority documents and process specs
```

### Navigating the Authority System

**To find what's authoritative:**

```bash
# The only authority index
cat 00_authority/MANIFEST.md

# Check a file's status
# Listed under "Authoritative now" = truth
# Listed under "Candidate authority" = use with [LOGIC TO BE CONFIRMED]
# Listed under "Reference only" = context, not foundation
```

**To find processes:**

```bash
# List all defined processes
ls 01_truth/processes/

# Key processes to know:
cat 01_truth/processes/2026-04_job-wrapup_and_escalation-note_sop_v1.md
cat 01_truth/processes/2026-04_quick-evidence-search_sop_v1.md
```

### Common Change Patterns

**To add a new process:**

1. Create file in `01_truth/processes/` with ISO date prefix: `YYYY-MM-DD_process-name_v1.md`
2. Add status `[LOGIC TO BE CONFIRMED]` in frontmatter
3. Include: inputs → outputs → acceptance → failure modes → provenance
4. Request promotion in `MANIFEST.md` when proven

**To record a decision:**

1. Significant or irreversible? Add pointer to `00_authority/DECISION_LOG.md`
2. Include: decision, context, date, confidence

**To handle uncertainty:**

1. Mark with appropriate token: `[LOGIC TO BE CONFIRMED]`, `[SOURCE REQUIRED]`, `[DECISION REQUIRED]`
2. Provide 2–3 bounded options with trade-offs
3. Recommend inside current authority

### Key Files to Start With

| Area | File | Why |
|------|------|-----|
| **Canonical entry** | `AGENTS.md` | Global partner instructions; first 60 seconds |
| **Authority index** | `00_authority/MANIFEST.md` | What's authoritative vs candidate vs reference |
| **Behavior defaults** | `00_authority/NORTH_STAR.md` | File budget, tokens, stop rules |
| **Mission** | `00_authority/PROJECT_INTENT.md` | Success criteria and non-negotiables |
| **Operating principles** | `00_authority/PRINCIPLES.md` | Hard stops and working stance |
| **Handover spec** | `01_truth/processes/2026-04_job-wrapup_and_escalation-note_sop_v1.md` | Wrap-up discipline and stateless handover |
| **Truth routing** | `01_truth/README.md` | Where processes/schemas/interfaces go |

### Practical Tips

- **Never guess authority:** If a file isn't in `MANIFEST.md`, it's not authoritative—even if it looks official.
- **Two attempts is a hard stop:** This prevents compounding errors. Research or park after two failures.
- **Document proportionally:** Light decisions get one bullet; significant decisions need positive + negative signals.
- **No bulk-read of 90_archive/:** The inbox is for triage, not authority. Follow `90_archive/README.md` gate rules.
- **Escalation notes are machine-readable:** Use YAML frontmatter with `status: parked` so Qwen can route automatically.
- **Human operator context:** Ewan often asks questions and thinks aloud in conversation. Diktats live in committed files; conversation is exploration. Translate intent into operational clarity.

---

*Generated by Compound Engineering plugin — `/onboarding` skill*

---
title: "Clean Build Restructure Proposal"
id: "clean-build-restructure-proposal"
version: 1
created: 2026-04-25
last_validated: 2026-04-25
type: document
topic_type: reference
status: imported
source_file: "clean-build-restructure-proposal.md"
signed_by: "Devon, 2026-04-25, devin-992682c244cf444f91e0a516498afbfd"
---

# Clean-Build Workspace Restructure Proposal
**Prepared for:** Ewan Bramley  
**Prepared by:** Jock (Claude Sonnet 4.5)  
**Date:** 2026-04-18  
**Purpose:** Agent-first clarity for Clean-Build-AmplifiedPartners workspace

---

## Executive Summary

The current Clean-Build-AmplifiedPartners structure is **architecturally sound** but suffers from **navigation overhead** and **missing enforcement layers**. With 30+ process files already and 8 department teams incoming, agents will spend more time searching than executing.

**Core problem:** The structure optimizes for governance (good) but not for agent discoverability (missing).

**Solution:** Add a lightweight navigation layer + enforcement layer WITHOUT changing the core architecture.

---

## Current Structure Critique

### What Works ✓

**1. Folder separation (00/01/02/03/90)**
- Clear authority boundaries
- Prevents accidental promotion
- Provenance tracking built in

**2. ISO-dated versioned naming**
- `YYYY-MM-DD_descriptive_vN.md`
- Chronologically sortable
- Version history visible

**3. YAML frontmatter**
- Machine-readable metadata
- Status tracking (draft/candidate/authoritative)
- Enables automation

**4. Partner instructions at entry points**
- AGENTS.md at root
- README.md in each folder
- Clear "how to use this"

### What Breaks ✗

**1. Discovery overhead (critical)**

Current state:
- 30+ files in `01_truth/processes/`
- No index beyond MANIFEST.md (which lists EVERYTHING)
- Agent must grep or manually scan to find relevant process

**Impact:** 10 minutes lost per lookup × 50 lookups/day = 8 hours/week wasted

**2. Version sprawl (moderate)**

Files versioned as `_v1.md`, `_v2.md`, `_v3.md` but:
- Old versions not explicitly moved to archive
- Unclear if v2 supersedes v1 or both are valid
- Git history is the only source of truth

**Impact:** "Which version do I use?" confusion

**3. Promotion bottleneck (moderate)**

`01_truth/` candidates promoted via MANIFEST.md indexing:
- Who promotes?
- When?
- What if 8 teams produce 20 candidates/week?

**Impact:** Backlog of good work stuck in limbo

**4. Enforcement layer missing (critical)**

The `.cursor/rules/` folder is **empty**.

Expected:
- Hooks enforcing stateless handover
- Automated wrap-up validation
- Compound improvement automation

Actual:
- Nothing

**Impact:** Discipline degrades without enforcement

**5. Compound Engineering undefined (critical)**

Referenced in:
- Kaizen rhythm file
- Stateless handover mentions
- Session wrap-up process

But:
- No central `COMPOUND_ENGINEERING.md` file
- No folder dedicated to it
- Unclear what "compound engineering" actually IS as a methodology

**Impact:** Agents can't follow a framework they can't find

---

## Proposed Restructure

### Principles

1. **Do not break existing authority architecture** (00/01/02/03/90 stays)
2. **Add navigation, don't replace structure**
3. **Make agent entry points OBVIOUS**
4. **Enforce discipline automatically where possible**
5. **Define compound engineering explicitly**

### New Folder Structure

```
Clean-Build-AmplifiedPartners/
├── AGENTS.md                          # Root entry (unchanged)
├── ONBOARDING.md                      # Quick start (unchanged)
├── README.md                          # Navigator redirect (unchanged)
│
├── 00_authority/                      # Policy spine (unchanged internally)
│   ├── MANIFEST.md                    # Master index (unchanged)
│   ├── NORTH_STAR.md
│   ├── PRINCIPLES.md
│   ├── BUILD_LOOP.md
│   ├── DECISION_LOG.md
│   └── ... (rest unchanged)
│
├── 01_truth/                          # Candidates (restructured)
│   ├── INDEX.md                       # ⭐ NEW: Fast lookup by category
│   ├── processes/
│   │   ├── INDEX.md                   # ⭐ NEW: Process quick reference
│   │   ├── core/                      # ⭐ NEW: Universal processes
│   │   │   ├── job-wrapup_sop_v1.md
│   │   │   ├── quick-evidence-search_sop_v1.md
│   │   │   └── escalation-note_sop_v1.md
│   │   ├── research/                  # ⭐ NEW: Research-specific
│   │   │   ├── research-department_charter_v1.md
│   │   │   ├── pudding-technique_v1.md
│   │   │   └── methodology-prospecting_v1.md
│   │   ├── governance/                # ⭐ NEW: Board/decision processes
│   │   │   ├── ai-board-governance_v1.md
│   │   │   └── death-spiral-detection_v1.md
│   │   ├── departments/               # ⭐ NEW: Department-specific
│   │   │   ├── customer-service/
│   │   │   ├── finance/
│   │   │   └── ... (8 departments)
│   │   └── archived/                  # ⭐ NEW: Superseded versions
│   │       └── YYYY-MM-DD_name_vN.md (old versions moved here)
│   ├── schemas/
│   │   └── ... (unchanged)
│   └── interfaces/
│       └── ... (unchanged)
│
├── 02_build/                          # Runnable code (unchanged)
│
├── 03_shadow/                         # Experiments (add structure)
│   ├── job-wrapups/                   # Session wrap-ups
│   │   ├── INDEX.md                   # ⭐ NEW: Recent wrap-ups list
│   │   └── YYYY-MM-DD_job_wrapup.md
│   ├── experiments/                   # ⭐ NEW: One-off tests
│   └── kaizen-improvements/           # ⭐ NEW: Compound improvements log
│
├── 90_archive/                        # Reference (unchanged)
│
└── .cursor/                           # Cursor IDE config (REBUILD)
    ├── skills/                        # OpenClaw skills (unchanged)
    ├── rules/                         # ⭐ REBUILD: Enforcement hooks
    │   ├── stateless-handover.mdc     # Wrap-up enforcement
    │   ├── compound-discipline.mdc    # Kaizen automation
    │   └── promotion-gate.mdc         # Candidate → authority gate
    ├── hooks.json                     # ⭐ REBUILD: Hook wiring
    └── compound-engineering/          # ⭐ NEW: CE framework home
        ├── README.md                  # What compound engineering IS
        ├── DISCIPLINE.md              # How it works
        ├── RHYTHM.md                  # Daily/session cadence
        └── TOOLING.md                 # Automation layer
```

---

## Navigation Layer Design

### 1. INDEX.md Files (NEW)

**Location:** `01_truth/INDEX.md` and `01_truth/processes/INDEX.md`

**Purpose:** Fast category-based lookup

**Format:**

```markdown
# Process Index (Agent Quick Reference)

## By Category

### Core (Universal)
- Job wrap-up → `core/job-wrapup_sop_v1.md`
- Quick search → `core/quick-evidence-search_sop_v1.md`
- Escalation → `core/escalation-note_sop_v1.md`

### Research
- Pudding Technique → `research/pudding-technique_v1.md`
- Department charter → `research/research-department_charter_v1.md`

### Departments
- Customer Service → `departments/customer-service/INDEX.md`
- Finance → `departments/finance/INDEX.md`

## By Use Case

**"I'm stuck after 2 attempts"**  
→ `core/quick-evidence-search_sop_v1.md`

**"I need to research a methodology"**  
→ `research/pudding-technique_v1.md`

**"I finished a job"**  
→ `core/job-wrapup_sop_v1.md`

## Recently Updated (last 7 days)
- 2026-04-18: `core/job-wrapup_sop_v1.md` (v12 → v13)
- 2026-04-17: `research/pudding-technique_v1.md` (v3 → v4)
```

**Agent benefit:** 30-second lookup instead of 10-minute grep

---

### 2. Hierarchical Grouping (NEW)

**Current:** All 30+ process files flat in `01_truth/processes/`

**Proposed:** Group by category

- `core/` = universal (wrap-up, search, escalation)
- `research/` = research-specific (Pudding, charter, methodology)
- `governance/` = board/risk (death-spiral, board voting)
- `departments/` = per-department specialization

**Agent benefit:** Scope reduced from 30 files to 5-8 per category

---

### 3. Version Archiving (NEW)

**Current:** `something_v1.md`, `something_v2.md`, `something_v3.md` all live together

**Proposed:** Only current version in active folder; old versions → `archived/`

**Rule:**
- `processes/core/job-wrapup_sop_v3.md` (current, canonical)
- `processes/archived/job-wrapup_sop_v1.md` (superseded)
- `processes/archived/job-wrapup_sop_v2.md` (superseded)

**MANIFEST.md indexes ONLY current version**

**Agent benefit:** No "which version?" confusion

---

## Compound Engineering Framework (NEW)

### The Missing Piece

Compound Engineering is referenced everywhere but defined nowhere.

**What it actually is:**

A methodology where:
1. **Every session ends with a wrap-up** (what worked, what failed, what to avoid)
2. **Wrap-ups feed an improvement queue** (Kaizen or Qwen processes them)
3. **Safe improvements auto-apply** (>0.5% gain, <1% regression risk)
4. **Unsafe improvements escalate** (human review before merge)
5. **Quality compounds daily** (0.5%/day = 365%/year)

Inspired by: [EveryInc compound-engineering-plugin](https://github.com/EveryInc/compound-engineering-plugin)

### Proposed Structure

**New folder:** `.cursor/compound-engineering/`

**Files:**

**1. `README.md`** (What it is)
```markdown
# Compound Engineering

**Definition:** A development methodology where quality improvements compound
daily through structured session wrap-ups and automated safe-merge workflows.

**Core equation:** 0.5% improvement/day = 365% improvement/year (compound)

**Three pillars:**
1. Stateless handover (every session ends with wrap-up)
2. Signal capture (positive/negative/repulsion)
3. Automated improvement (safe changes auto-merge)

**See:** DISCIPLINE.md, RHYTHM.md, TOOLING.md
```

**2. `DISCIPLINE.md`** (How it works)
```markdown
# Compound Engineering Discipline

## Session Lifecycle

1. **Start:** Read previous wrap-up OR fresh start
2. **Work:** Bounded task, 50% capacity (slack for quality)
3. **Signals:** Capture what worked / what failed / what to avoid
4. **Wrap-up:** Mandatory handover packet (see RHYTHM.md)
5. **Queue:** Improvement signals → Kaizen queue

## Wrap-Up Format

See: `01_truth/processes/core/job-wrapup_sop_v1.md` for full spec

Minimum required:
- Status (finished/parked/blocked)
- What worked (positive signal)
- What failed (negative signal)
- Repulsion score (1-10, what to AVOID)
- Next agent handover (resume instruction)

## Enforcement

See: `.cursor/rules/stateless-handover.mdc`
```

**3. `RHYTHM.md`** (Daily/session cadence)
```markdown
# Compound Engineering Rhythm

## Human Working Day

**Morning:**
- Review SESSION-STATE.md
- Set daily targets (Telegraph Pole orientation)

**Build:**
- Blinkers Without Ceilings (focused but unceiled)
- 50% capacity (slack for wrap-ups)

**Milestone:**
- Micro-retrospective (what worked? what's blocking?)

**Evening:**
- Update SESSION-STATE.md
- Session wrap-up (YAML + markdown)
- Update vault

## Automated (03:00 UTC)

**KaizenWorkflow:**
1. Scan vault wrap-ups (last 24h)
2. Identify safe improvements (>0.5% score, <1% regression)
3. Auto-merge safe fixes (if human approved queue)
4. Flag unsafe improvements → Kaizen Dept review
5. Update AMPS floor scores

## The Compound Effect

Improvement happens **at the point of work**, not in periodic reviews.

- Full context from session
- Immediate signal capture
- No stale post-mortems
- 0.5%/day compounds to 365%/year
```

**4. `TOOLING.md`** (Automation layer)
```markdown
# Compound Engineering Tooling

## Cursor Hooks (Enforcement)

See: `.cursor/hooks.json`

**1. `stateless-handover-stop.py`**
- Triggered: session end
- Checks: wrap-up exists, format valid, handover complete
- Action: blocks close if incomplete

**2. `compound-discipline.py`**
- Triggered: daily (03:00 UTC)
- Reads: 03_shadow/job-wrapups/*.md
- Extracts: positive/negative/repulsion signals
- Queues: safe improvements for auto-merge

**3. `promotion-gate.py`**
- Triggered: PR to 01_truth → 00_authority
- Checks: MANIFEST.md indexed, PROMOTION_GATE.md passed
- Action: blocks merge if gates fail

## Kaizen Queue (Qwen-managed)

Location: `03_shadow/kaizen-improvements/`

Format:
```yaml
improvement_id: uuid
source_wrapup: path/to/wrapup.md
signal_type: positive | negative | repulsion
score_delta: +0.8% (estimated improvement)
regression_risk: <1% (estimated)
status: queued | approved | merged | rejected
```

Safe merge criteria:
- Score delta >0.5%
- Regression risk <1%
- Human approval (if required)

## Integration Points

- **Qwen:** Processes improvement queue
- **Git:** Auto-commit merged improvements
- **MANIFEST.md:** Auto-update on promotion
- **AMPS:** Floor scores updated post-merge
```

---

## Enforcement Layer (REBUILD)

### Current State
`.cursor/rules/` folder is **empty**

### Required Files

**1. `.cursor/hooks.json`**
```json
{
  "hooks": {
    "pre-commit": ".cursor/rules/stateless-handover-stop.py",
    "daily-03:00": ".cursor/rules/compound-discipline.py",
    "pre-merge": ".cursor/rules/promotion-gate.py"
  }
}
```

**2. `.cursor/rules/stateless-handover.mdc`**
```markdown
---
description: Enforce stateless handover discipline
trigger: session-end
---

# Stateless Handover Enforcement

## Check List

Every session MUST produce:

1. ✓ Wrap-up file exists: `03_shadow/job-wrapups/YYYY-MM-DD_job_wrapup.md`
2. ✓ YAML frontmatter valid (status, date, tags)
3. ✓ Handover packet complete:
   - What worked (positive)
   - What failed (negative)
   - Repulsion score + bands
   - Next agent resume instruction
4. ✓ Signal sent to Qwen (improvement queue)

If ANY check fails → block session close, show checklist

See: `01_truth/processes/core/job-wrapup_sop_v1.md`
```

**3. `.cursor/rules/compound-discipline.mdc`**
```markdown
---
description: Daily compound improvement automation
trigger: daily 03:00 UTC
---

# Compound Discipline (Daily Kaizen)

## Workflow

1. Scan: `03_shadow/job-wrapups/*.md` (last 24h)
2. Extract signals:
   - Positive (what worked)
   - Negative (what failed)
   - Repulsion (what to avoid, score 1-10)
3. Score improvements:
   - Estimate score delta (>0.5% threshold)
   - Estimate regression risk (<1% threshold)
4. Queue safe improvements → `03_shadow/kaizen-improvements/`
5. Flag unsafe improvements → Kaizen Dept review
6. Update AMPS floor scores (post-merge)

## Auto-Merge Criteria

- Score delta ≥0.5%
- Regression risk ≤1%
- Human approval (if required by PROMOTION_GATE.md)

See: `.cursor/compound-engineering/TOOLING.md`
```

**4. `.cursor/rules/promotion-gate.mdc`**
```markdown
---
description: Candidate → Authority promotion gate
trigger: PR to 00_authority/
---

# Promotion Gate

## Rules

A file in `01_truth/` may be promoted to authoritative ONLY if:

1. ✓ Indexed in `00_authority/MANIFEST.md`
2. ✓ Status = `authoritative` (not `draft` or `candidate`)
3. ✓ Passes `00_authority/PROMOTION_GATE.md` criteria:
   - Has clear source attribution
   - No unresolved [DECISION REQUIRED] tokens
   - Tested in production OR explicit hypothesis flag
4. ✓ Human approval (Ewan or delegated authority)

If ANY check fails → block PR merge, show gate checklist

See: `00_authority/PROMOTION_GATE.md`
```

---

## Agent Entry Points (Redesigned)

### Problem
Agents need to know: "Where do I start?"

### Solution
**Three entry tiers:**

**Tier 1: First-time agent (zero context)**
→ `AGENTS.md` (root)  
→ Directed to: `00_authority/NORTH_STAR.md` → `00_authority/MANIFEST.md`

**Tier 2: Returning agent (knows structure, needs task)**
→ `01_truth/INDEX.md`  
→ Fast category lookup → relevant process

**Tier 3: Agent stuck on specific blocker**
→ `01_truth/processes/INDEX.md`  
→ Use-case lookup ("I'm stuck after 2 attempts" → quick-evidence-search)

### Navigation Map

```
Entry
  ↓
AGENTS.md (root) → "Read order: NORTH_STAR → MANIFEST → PROJECT_INTENT"
  ↓
NORTH_STAR.md → "Clean room rules, authority, tokens, stop conditions"
  ↓
MANIFEST.md → "Master index of what's authoritative vs candidate"
  ↓
01_truth/INDEX.md → "Fast lookup by category or use case"
  ↓
Relevant process file → "Execute"
  ↓
Wrap-up (mandatory) → "Signal to Qwen, improvement queue"
```

---

## Promotion Workflow (Clarified)

### Current (Unclear)
- Agent produces candidate in `01_truth/`
- "Someone" promotes to authoritative in MANIFEST.md
- Unclear: who? when? how?

### Proposed (Clear)

**Step 1: Candidate Creation**
- Agent writes file → `01_truth/processes/category/name_v1.md`
- Status: `candidate` (YAML frontmatter)
- Indexed in: `01_truth/INDEX.md` (category list)

**Step 2: Testing**
- File used in production (or hypothesis flag explicit)
- Wrap-ups reference it
- Signals captured (does it work?)

**Step 3: Promotion Review**
- Weekly promotion meeting (Ewan + Qwen)
- Review candidates with ≥3 successful uses
- Check PROMOTION_GATE.md criteria

**Step 4: Promotion**
- Status → `authoritative` (YAML updated)
- Indexed in: `00_authority/MANIFEST.md`
- Old version (if supersedes) → `archived/`

**Step 5: Notification**
- Agents notified via Qwen broadcast
- Changelog entry in MANIFEST.md

**Frequency:** Weekly (every Monday 09:00)

**Owner:** Ewan (with Qwen assistance)

---

## Implementation Plan

### Phase 1: Navigation (Week 1)

**Actions:**
1. Create `01_truth/INDEX.md` (category + use-case lookup)
2. Create `01_truth/processes/INDEX.md` (process quick reference)
3. Create category folders:
   - `core/`
   - `research/`
   - `governance/`
   - `departments/` (with 8 subdirs)
   - `archived/`
4. Move existing files into categories (preserve git history)
5. Update MANIFEST.md with new paths

**Outcome:** Agents can find processes in <1 minute

---

### Phase 2: Enforcement (Week 1-2)

**Actions:**
1. Create `.cursor/compound-engineering/` folder
2. Write 4 framework files:
   - `README.md`
   - `DISCIPLINE.md`
   - `RHYTHM.md`
   - `TOOLING.md`
3. Rebuild `.cursor/rules/`:
   - `stateless-handover.mdc`
   - `compound-discipline.mdc`
   - `promotion-gate.mdc`
4. Write `.cursor/hooks.json`
5. Test hook enforcement (dry-run, no auto-merge yet)

**Outcome:** Stateless handover enforced, discipline automated

---

### Phase 3: Promotion Workflow (Week 2)

**Actions:**
1. Document promotion cadence (weekly Monday 09:00)
2. Create promotion checklist template
3. Train Qwen on promotion-gate criteria
4. Run first promotion review (existing candidates)
5. Update MANIFEST.md with promoted files

**Outcome:** Clear path from candidate → authoritative

---

### Phase 4: Testing & Calibration (Week 3-4)

**Actions:**
1. Run 10 agent sessions with new structure
2. Measure: lookup time, wrap-up compliance, promotion throughput
3. Collect agent feedback (what's still unclear?)
4. Refine INDEX.md based on actual queries
5. Tune compound improvement thresholds

**Outcome:** Structure validated, ready for 8-team scale

---

## Success Metrics

**Navigation:**
- Agent lookup time <1 minute (vs 10 minutes current)
- Zero "which file?" questions in wrap-ups

**Enforcement:**
- 100% wrap-up compliance (enforced by hooks)
- ≥1 safe improvement auto-merged per day

**Promotion:**
- Weekly promotion reviews happen on schedule
- <1 week lag from candidate → authoritative (for proven files)

**Compound Quality:**
- AMPS floor scores trending +0.5%/day
- Repulsion signals decreasing over time (fewer repeated mistakes)

---

## Risks & Mitigations

**Risk 1: Over-engineering**  
"This is too complex, agents get lost in structure"

**Mitigation:**  
- INDEX.md files provide fast lookup (agents bypass deep structure)
- Entry tiers guide by experience level
- Measure lookup time weekly, simplify if >2 minutes

**Risk 2: Enforcement too strict**  
"Hooks block legitimate work, agents frustrated"

**Mitigation:**  
- Dry-run mode first (warnings, no blocks)
- Exception path (`wrapup-exception.md`) for genuine edge cases
- Tune thresholds based on wrap-up feedback

**Risk 3: Promotion bottleneck**  
"8 teams produce 40 candidates/week, Ewan can't review that fast"

**Mitigation:**  
- Qwen pre-filters (only candidates with ≥3 successful uses)
- Batch promotion (not one-by-one)
- Delegate promotion authority for low-risk categories (e.g., department-specific)

---

## Appendix: Compound Engineering Philosophy

**Core insight:**  
Small improvements, applied consistently, compound faster than heroic rewrites.

**Formula:**  
`(1 + 0.005)^365 = 6.65`  
0.5% daily improvement = 565% gain in one year

**Why it works:**
1. **Immediate context** — improvements happen during the session, not weeks later
2. **Low friction** — no separate "improvement backlog" to maintain
3. **Automated** — safe changes merge without human review
4. **Directional** — repulsion signals prevent regression

**Where it fails:**
- Without enforcement (hooks off = discipline degrades)
- Without signal capture (wrap-ups skipped = no data)
- Without thresholds (unsafe changes auto-merged = regression)

**This restructure enables compound engineering at scale.**

---

## Conclusion

**The current Clean-Build structure is good governance.**  
**This proposal makes it good for agents.**

**Three changes:**
1. **Navigation layer** (INDEX.md files + category folders)
2. **Enforcement layer** (Cursor hooks + compound engineering framework)
3. **Promotion workflow** (weekly cadence + clear criteria)

**Outcome:**  
Agents find what they need in <1 minute, wrap-ups happen automatically, quality compounds daily.

**Ready to scale to 8 department teams.**

---

**Next Step:**  
Ewan reviews this proposal, identifies what's wrong, refines, then we implement Phase 1.

**Estimated implementation:** 2-4 weeks (if prioritized)

**Cost:** Agent time only (no new tooling required)

**Benefit:** 10x agent productivity, 365%/year compounding quality

---

_End of Document_

---
title: "PUDDING 2026 — Validation Methodology v2.1"
id: "validation-methodology-v2-copy"
version: 1
created: "2026-04-25"
type: "document"
topic_type: "audit"
audience: "internal"
layer: "truth"
status: "filed"
signed_by: "Devon, 2026-04-25, devin-992682c244cf444f91e0a516498afbfd"
---

# PUDDING 2026 — Validation Methodology v2.1
## Mandatory. Enforced. Benchmarked. Checked at Every Stage. No Exceptions.

**Date**: 2026-03-17
**Version**: 2.1 — rubric & benchmark enforcement wired into every gate
**Status**: Draft — ready for implementation
**PUDDING Label**: `C.>.5.p` — Constraint, Tipping, System-scale, Permanent
**Attribution**: Ewan Bramley (originator, directive, mandatory enforcement requirement) × Perplexity AI (researcher, formaliser)
**LBD Attribution**: Swanson (1986) ABC Model

---

## 0. THE LAW

**PUDDING validation is not optional. It is not a recommendation. It is a hard gate.**

Nothing enters the system without a validated PUDDING label.
Nothing moves between stages without its label being checked.
Nothing ships without its label passing inter-rater reliability.
Nothing is exempt. Not atoms. Not recipes. Not framework documents. Not this document.

If it fails validation → it stops. It does not proceed. It does not get a waiver. It goes back, gets fixed, and re-enters the gate. Mathematics decides. Not vibes. Not urgency. Not "we'll fix it later."

This is the same principle as the Metric Gate (Buzzard/Tao/Candès), the Structure Gate (PUDDING facets), and the Provenance Gate (Attribution Schema) — but now formalised as an enforceable, auditable, mandatory checkpoint at every stage of the pipeline.

### The Four Immutable Rules

| # | Rule | Enforcement | Benchmark |
|---|------|-------------|----------|
| 1 | **Every atom MUST have a validated PUDDING label before it can be referenced, scored, mixed, or shipped** | Automated: system rejects unlabelled atoms at ingest | Label validity check (4 facets × valid values) |
| 2 | **Every label MUST pass inter-rater reliability (α ≥ 0.667 minimum, α ≥ 0.80 for shipping)** | Measured: Krippendorff's Alpha calculated at every batch | Krippendorff α thresholds per facet |
| 3 | **Every stage transition MUST include a label integrity check** | Enforced: gate blocks progression if check fails | Gate check function runs at every transition |
| 4 | **Every atom MUST be scored against the existing rubrics and benchmarks — not just labelled** | Enforced: rubric scores are mandatory at Stage 3, benchmarked at every subsequent gate | RAEI (0-20), PRS (0-10), AMPS (0-10), MASHUP (0-100), INTENTLOGIC (0-81) |

---

## 1. WHAT THIS IS

A mandatory enforcement methodology for proving that PUDDING 2026 labeling is:
- **Objective** — not dependent on who does it
- **Reproducible** — same inputs produce same outputs
- **Mathematically testable** — we can measure it with numbers, not opinions
- **Enforced** — checked at every stage, not just at the end
- **Benchmarked** — scored against the existing rubric ecosystem, not just validated structurally

This document synthesises three established academic methodologies, maps them against PUDDING 2026, and defines the mandatory gates where validation is checked. It uses the existing rubric and benchmark systems that already exist — they are not decorative. They are the benchmark.

### 1.1 THE EXISTING RUBRIC ECOSYSTEM (Use It)

These rubrics already exist. They are already defined. They MUST be applied. This section is the master reference for what gets checked where.

| Rubric | What It Scores | Scale | Thresholds | Used At Gate |
|--------|---------------|-------|------------|-------------|
| **RAEI (Relevance, Actionability, Evidence, Impact)** | Individual atom quality against a stated goal | 4 dimensions × 0-5 = 0-20 total | ≥ 12 = pudding ingredient, < 12 = below threshold | G3 (Score), G4 (Match), G5 (Mix), G7 (Ship) |
| **PRS (Process Readiness Score)** | Atom readiness for production deployment | 0-10 weighted composite | ≥ 7.0 = ship, ≥ 9.0 = gold, ≥ 5.0 = research more, < 5.0 = reject | G6 (Gate Decision), G7 (Ship) |
| **AMPS (Amplified Process Maturity Score)** | Process maturity across 6 weighted dimensions | 0-10 composite | Per-dimension and composite thresholds | G6 (Gate Decision), Quarterly Audit |
| **MASHUP_SCORE** | Recipe quality (cross-domain pudding mix) | 0-100 weighted (6 components) | ≥ 60 = mashup, ≥ 80 = priority | G5 (Mix) |
| **INTENTLOGIC** | Experiment quality (clarity × causal logic × design × learning) | 0-81 (4 dims × 0-3, multiplicative) | Any dim = 0 → VOID, 1-9 weak, 10-27 internal, 28-81 client-facing | G6 (Test) |
| **Krippendorff's α** | Inter-rater reliability per PUDDING facet | -1 to 1 | ≥ 0.667 = minimum, ≥ 0.70 = deploy, ≥ 0.80 = ship, ≥ 0.90 = gold | G2b (Label), G7 (Ship), Ongoing |
| **Jaccard Slot Score** | PUDDING label similarity between atoms | 0-1 (matching facets / 4) | ≥ 0.75 (3/4 match) for valid match | G4 (Match) |
| **Believability Weight** | Expert credibility on specific topic (Dalio meritocracy) | Weighted by domain expertise, chronology, citations, adoption | Only surface insights where source is credible expert in that specific domain | G3 (Score), G4 (Match) |
| **3-Gate Metric Formula (Buzzard/Tao/Candès)** | Metric validity | Pass/fail per gate | All 3 must pass or metric cannot be used for decisions | Every gate that uses a metric |
| **SYNERGY Score** | Cross-domain combination value | (Shared)² × Unique_A × Unique_B | 0 = no synergy, higher = more valuable | G5 (Mix) |
| **PUDDING Tier** | Overall pudding score tier | Attribution × Authority × Completeness × Applicability × Validation | VOID (any=0), RAW (1-99), BRONZE (100-999), SILVER (1K-4,999), GOLD (≥5K) | G7 (Ship) |

### 1.2 THE 10 ENFORCER ROLES (Who Checks)

These roles already exist in the Master Process Document. Each gate has an assigned enforcer.

| # | Enforcer Role | Gate Assignment | What They Check |
|---|---------------|----------------|----------------|
| 1 | **Intake Guard** | G1 (Ingest) | Atom ID, format, parseable, source logged |
| 2 | **Taxonomy Enforcer** | G2 (Label) | All 5 layers assigned, PUDDING label valid, codebook path recorded |
| 3 | **Quality Scorer** | G3 (Score) | RAEI rubric applied, PRS calculated, believability weight applied |
| 4 | **Research Validator** | G4 (Match) | Triple search done, failure patterns included, ≥3 named techniques |
| 5 | **Test Director** | G5/G6 (Mix/Test) | MASHUP_SCORE calculated, INTENTLOGIC scored, pre-registered design |
| 6 | **Ship Gate** | G7 (Ship) | ALL prior gates pass, α ≥ 0.80, PRS ≥ 7.0, PUDDING Tier ≥ SILVER |
| 7 | **Attribution Enforcer** | Every gate | Radical attribution present, LBD credited, fact % assigned |
| 8 | **Chaos Tester** | G6 (Test) | Adversarial noise injection, edge case testing |
| 9 | **Kaizen Reviewer** | Daily cycle | What improved? What degraded? AMPS recalculated. |
| 10 | **Compliance Monitor** | Every gate | 3-Gate Metric Formula (Buzzard/Tao/Candès) applied to all metrics |

### 1.3 THE 12 ANALYTICAL LENSES (How to Examine)

Every atom can be examined through any of these 12 lenses. At minimum, the lenses relevant to the atom's domain MUST be applied during scoring (G3).

| # | Lens | Question |
|---|------|----------|
| 1 | Financial | What is the cost/revenue/ROI impact? |
| 2 | Operational | How does this affect daily operations and efficiency? |
| 3 | Customer | What is the impact on customer experience and satisfaction? |
| 4 | People | How does this affect staff, culture, and capability? |
| 5 | Technology | What technical infrastructure is required or affected? |
| 6 | Compliance | Are there regulatory, legal, or governance implications? |
| 7 | Risk | What could go wrong? What are the failure modes? |
| 8 | Scale | Does this work at 1x, 10x, 100x, 1000x? |
| 9 | Time | How long to implement? How long until value? |
| 10 | Integration | How does this connect to existing systems and processes? |
| 11 | Evidence | What proof exists? What's the confidence level? |
| 12 | Innovation | Is this novel? Does it create new possibilities? |

### 1.4 THE SYMBIOTIC CROSS-REFERENCE MAP (How They Feed Each Other)

The rubrics are not isolated scoring systems. They are a symbiotic ecosystem. Each one produces data that improves the others. This is the wiring diagram.

```
┌─────────────────────────────────────────────────────────────────┐
│                  SYMBIOTIC RUBRIC ECOSYSTEM                     │
│                                                                 │
│  PUDDING Label ──┬──▶ RAEI (label informs what's scoreable)    │
│  (WHAT.HOW.      │                                              │
│   SCALE.TIME)    ├──▶ MASHUP_SCORE (labels must match to mix)  │
│                  └──▶ Believability (label determines which     │
│                       expert domain weights apply)              │
│                                                                 │
│  RAEI ───────────┬──▶ PRS (RAEI feeds into PRS composite)      │
│  (R/A/E/I 0-20)  ├──▶ PUDDING Label (Evidence score validates  │
│                  │    or conflicts with HOW facet)              │
│                  └──▶ MASHUP_SCORE (both atoms need ≥12 to mix)│
│                                                                 │
│  PRS ────────────┬──▶ Gate Decision (ship/research/reject)     │
│  (0-10)          ├──▶ AMPS (PRS of component atoms feeds       │
│                  │    process maturity score)                   │
│                  └──▶ PRIORITY formula (tier × intent × synergy)│
│                                                                 │
│  MASHUP_SCORE ───┬──▶ INTENTLOGIC (recipe needs test design)   │
│  (0-100)         ├──▶ SYNERGY (mashup informs synergy calc)    │
│                  └──▶ PRS (successful mashup raises PRS)       │
│                                                                 │
│  INTENTLOGIC ────┬──▶ PRS (test results update PRS)            │
│  (0-81)          ├──▶ Maturity Layer (updates taxonomy layer 5) │
│                  └──▶ AMPS (proven tests improve maturity)     │
│                                                                 │
│  Krippendorff α ─┬──▶ Codebook (low α triggers refinement)    │
│  (-1 to 1)       ├──▶ ALL rubrics (if labels aren't reliable,  │
│                  │    all downstream scores are suspect)        │
│                  └──▶ System Halt (α < 0.667 freezes everything)│
│                                                                 │
│  Believability ──┬──▶ RAEI (expert weight adjusts scores)      │
│  (Dalio)         ├──▶ MASHUP_SCORE (source credibility matters) │
│                  └──▶ PUDDING Tier (authority factor)           │
│                                                                 │
│  AMPS ───────────┬──▶ Kaizen (low AMPS triggers improvement)  │
│  (0-10)          ├──▶ PRIORITY (mature processes get priority)  │
│                  └──▶ Gate Decision (immature = more research)  │
│                                                                 │
│  3-Gate Metric ──▶ ALL rubrics (invalid metrics = invalid scores)│
│  (Buzzard/Tao/                                                  │
│   Candès)        If ANY metric fails 3-Gate → score is void    │
└─────────────────────────────────────────────────────────────────┘
```

**The feedback loops that make the system self-improving:**

| Loop | Trigger | Action | Feeds Back To |
|------|---------|--------|---------------|
| **Label → Score → Label** | RAEI Evidence score conflicts with HOW facet | Adjudicate: fix label OR fix rubric score | Codebook (if label was wrong) or scoring guide (if score was wrong) |
| **Score → Test → Score** | INTENTLOGIC result updates maturity | PRS recalculated with new evidence | AMPS, Gate Decision |
| **α → Codebook → α** | Krippendorff drops below threshold | Codebook refined, calibration re-run | All downstream labels and scores |
| **Match → Mix → Match** | MASHUP_SCORE reveals which label matches produce real connections | Pattern data feeds back to improve matching thresholds | Jaccard/SYNERGY calibration |
| **AMPS → Kaizen → AMPS** | Daily AMPS recalculation reveals degradation | Kaizen review identifies root cause and triggers improvement | All process atoms |
| **Believability → Score → Believability** | New evidence updates expert credibility | Expert weights adjusted based on track record | All future scoring |

### 1.5 THE ERROR & SOLUTION REGISTRY (Known Failure Patterns)

Research has identified specific failure patterns in taxonomy and labeling systems. These are not theoretical — they are documented, researched, and stored as a permanent debugging reference. The system checks against them.

**This registry is checked at every gate. It is not a one-time research artifact.**

| # | Known Error Pattern | Source | How It Manifests in PUDDING | Solution (Stored) | Gate Where Checked |
|---|-------------------|--------|---------------------------|-------------------|-------------------|
| E1 | **Label drift** — coders gradually shift interpretation over time | Krippendorff (2004) | HOW facet judgments slowly change as labeler sees more atoms | Running α monitored; codebook audit every 50 atoms; recalibration set | G2b (every batch) |
| E2 | **Anchoring bias** — first label seen influences all subsequent ones | Brown et al. (2020) | If first atom is labeled P.>.3.i, labeler unconsciously biases toward similar labels | Randomize atom presentation order; independent raters see different sequences | G2 (label assignment) |
| E3 | **Category collapse** — too-similar codes get merged in practice | Ranganathan design principles | Process (P) vs Meta (M) confusion; Amplifying (+) vs Tipping (>) confusion | Decision trees in codebook with explicit boundary tests | G2 (label assignment) |
| E4 | **Expert-domain labeling** — labeling by source not mechanism | PUDDING operational protocol | Calling something "the Kennedy principle" instead of labeling the mechanism | Neutral labeling enforced; codebook strips domain names | G2 (label assignment) |
| E5 | **Score inflation** — rubric scores creep upward over time | Content analysis literature | RAEI scores trend toward 4-5 across all dimensions | Score distribution monitored; flag if mean > 3.5 across batch | G3 (scoring) |
| E6 | **Confirmation bias in matching** — seeing connections that aren't there | Swanson LBD literature | Matching atoms because they're interesting, not because labels genuinely align | Jaccard ≥ 0.75 enforced; blind evaluation (no labels shown to match evaluator) | G4 (matching) |
| E7 | **Post-hoc rationalization** — inventing the 1+1=3 after seeing the match | Recipe validation literature | Stating a hypothesis AFTER knowing both atoms match, not as genuine prediction | Test must be pre-registered; prediction stated BEFORE seeing results | G5/G6 (mix/test) |
| E8 | **Survivorship bias** — only testing recipes that look promising | Statistical testing literature | Ignoring near-matches (Jaccard 0.5-0.75) that might reveal category problems | Quarterly sample of near-misses reviewed; codebook updated if categories are too coarse | G4 (matching), Quarterly audit |
| E9 | **Single-rater dependency** — all labels from one source (one AI model) | Inter-rater reliability methodology | If Claude labels everything, you have one perspective, not objectivity | Mandatory dual-labeling (sampled); mixed human + AI raters | G2b (inter-rater) |
| E10 | **Metric gaming** — optimizing for the score instead of the underlying quality | Goodhart's Law | Atoms designed to hit PRS ≥ 7.0 rather than genuinely being ready | 3-Gate Metric Formula (Buzzard/Tao/Candès) validates the metric itself | Every gate |
| E11 | **Stale codebook** — definitions don't evolve with the system | Taxonomy maintenance literature | New types of atoms don't fit existing categories but get forced in | Codebook audit every 50 atoms; unclassifiable items trigger review | G2 (every 50 atoms) |
| E12 | **Attribution gap** — losing track of who labeled what | Radical Attribution Schema | Can't trace a bad label back to its source for debugging | Full attribution on every label assignment; rater ID logged | Every gate |

**How the registry is used:**

1. **At code time**: The validation script includes checks for each known error pattern
2. **At gate time**: Each enforcer has a checklist that references the relevant error patterns
3. **At Kaizen time**: Daily review checks whether any error pattern frequency is increasing
4. **At audit time**: Quarterly external audit specifically tests for each error pattern
5. **At research time**: New error patterns discovered in literature are added to the registry
6. **At codebook time**: Every codebook update references which error patterns it addresses

**The registry itself gets PUDDING-labeled and versioned:**
```yaml
atom_id: AMP-0801-ERR-v1
title: "PUDDING Error & Solution Registry"
pudding_label: "I.~.5.l"
pudding_reading: "Information, Oscillating, System-scale, Long"
status: canonical
note: "Oscillating because error patterns emerge, get fixed, and new ones emerge — it cycles"
```

---

## 2. THE THREE ESTABLISHED METHODOLOGIES WE'RE HIJACKING

### 2.1 Krippendorff's Content Analysis (1980, 2004)

**What it is**: The gold standard methodology for measuring whether multiple people can apply the same coding scheme to the same data and get the same result.

**Source**: Klaus Krippendorff (2004). *Content Analysis: An Introduction to Its Methodology*. Sage Publications.

**Key components**:
- **Codebook**: A document that defines every code, what it means, when to apply it, and examples
- **Inter-rater reliability**: Statistical measure of agreement between coders
- **Krippendorff's Alpha (α)**: The specific metric — handles any data type (nominal, ordinal, interval, ratio), any number of raters, and missing data
- **Thresholds**: α ≥ 0.667 for tentative conclusions, α ≥ 0.8 for strong reliability

**Why we're using it**: PUDDING labels are a coding scheme. If two independent coders can't assign the same PUDDING label to the same concept, the system fails. Krippendorff's Alpha is the mathematically rigorous way to measure this.

**Reference**: [Encord — Krippendorff's Alpha](https://encord.com/blog/interrater-reliability-krippendorffs-alpha/)

### 2.2 Ranganathan's Faceted Classification (1933, revised)

**What it is**: The original multi-facet classification system. Every item is described by independent facets (dimensions), not forced into a single hierarchy.

**Source**: S.R. Ranganathan (1933). *Colon Classification*. Also: [Berkeley — Faceted Classification](https://berkeley.pressbooks.pub/tdo4p/chapter/faceted-classification/)

**Ranganathan's 5 facets (PMEST)**:

| Facet | Meaning |
|-------|---------|
| **P**ersonality | The type of thing |
| **M**atter | The constituent material |
| **E**nergy | The action or activity |
| **S**pace | Where it occurs |
| **T**ime | When it occurs |

**PUDDING 2026's 4 facets (WHAT.HOW.SCALE.TIME)**:

| Facet | Meaning | Ranganathan equivalent |
|-------|---------|----------------------|
| **WHAT** | Entity type (P/I/R/E/S/C/M) | Personality |
| **HOW** | Dynamic behaviour (=, +, -, >, ~, !, ?) | Energy |
| **SCALE** | Scope of effect (0-6) | Space (abstracted) |
| **TIME** | Duration (i/m/l/v/p/∞) | Time |

**Key insight**: PUDDING is structurally a Ranganathan-style faceted classification. It's missing the "Matter" facet — but that's deliberate. PUDDING strips the material/domain away to enable cross-domain matching. The absence of Matter IS the innovation.

**Design principles from Ranganathan that PUDDING must satisfy**:

| Principle | What it means | PUDDING status | Mandatory check |
|-----------|---------------|----------------|-----------------|
| **Orthogonality** | Facets are independent — one value per facet, no conflicts | ✅ WHAT, HOW, SCALE, TIME are independent | **Gate 1**: Facet independence verified at label assignment |
| **Semantic balance** | Values at same level are equivalent scope | ⚠️ Needs testing | **Gate 2**: Codebook definitions enforce balance |
| **Coverage** | Every item can be classified | ⚠️ Needs testing | **Gate 3**: Unclassifiable items trigger codebook review |
| **Scalability** | System handles additions | ✅ New codes can be added | **Gate 4**: New codes require full re-validation cycle |
| **Objectivity** | Unambiguous terms | ⚠️ Needs inter-rater testing | **Gate 5**: α ≥ 0.667 per facet, mandatory |
| **Normativity** | Standard accessible terms | ⚠️ Depends on codebook | **Gate 6**: Codebook audit every 50 new atoms |

### 2.3 Inter-Rater Reliability Protocol (Brown et al., 2020)

**What it is**: A specific, tested protocol for taking a taxonomy, having multiple people apply it, measuring agreement, refining, and repeating until it's reliable.

**Source**: Brown, A.M. et al. (2020). "Applying inter-rater reliability to improve consistency in classifying PhD career outcomes." *F1000Research*, 9:8. [Link](https://f1000research.com/articles/9-8)

**Their process (which we will adapt)**:

1. **Preliminary coding**: ~2,500 records coded to identify problems
2. **Create guidance document**: Detailed codebook with definitions, examples, FAQs
3. **Experiment 1**: 6 coders independently classify 572 records
4. **Measure**: Krippendorff's Alpha per tier
5. **Identify hot spots**: Rank records by disagreement, find patterns
6. **Refine**: Group meetings → update taxonomy definitions → update guidance
7. **Experiment 2**: 8 coders (incl. 3 new inexperienced) classify 219 new records
8. **Measure again**: Compare Alpha improvement
9. **Final refinement**: Minor guidance updates only

**Their results**:

| Tier | Exp 1 (6 coders) | Exp 2 (8 coders) | Exp 2 (5 experienced) |
|------|-------------------|--------------------|-----------------------|
| Workforce Sector (6 categories) | 0.83 | 0.90 | 0.93 |
| Career Type (6 categories) | 0.70 | 0.73 | 0.78 |
| Job Function (23 categories) | 0.62 | 0.69 | 0.70 |

**Key finding**: More categories = harder to agree. Their Job Function tier (23 categories) barely hit 0.70 after 2 rounds. PUDDING WHAT has 7 categories, HOW has 7, SCALE has 7, TIME has 7. Each facet is manageable. The full combined label (2,401 possible) is where the challenge lies.

---

## 3. THE COMPARISON: PUDDING vs ESTABLISHED METHODS

### What PUDDING already has (from your conversations):

| Component | Established equivalent | Status |
|-----------|----------------------|--------|
| WHAT.HOW.SCALE.TIME notation | Ranganathan PMEST faceted classification | ✅ Structurally sound |
| 4-criteria rubric (R/A/E/I) | Content analysis coding scheme | ✅ But needs inter-rater testing |
| Recipe scoring formula | Statistical synergy detection | ✅ Mathematically validated (PMI, Jaccard) |
| Radical Attribution Schema | Provenance tracking | ✅ Exceeds academic standards |
| 5 taxonomy layers per atom | Multi-dimensional classification | ✅ More thorough than most systems |
| Semantic dimensions (3-7 per atom) | Controlled vocabulary / thesaurus | ⚠️ Not formally tested for reproducibility |

### What PUDDING is missing (all now MANDATORY to fix):

| Gap | What's needed | Priority | Enforcement |
|-----|---------------|----------|-------------|
| **Codebook** | Formal definition document with rules, decision trees, examples for EVERY code | CRITICAL — BLOCKS ALL | No labeling without codebook. Period. |
| **Inter-rater reliability test** | Measure Krippendorff's Alpha across multiple coders | CRITICAL — BLOCKS ALL | No deployment without α ≥ 0.667 per facet |
| **Pilot study** | Small-scale test before full deployment | CRITICAL — BLOCKS DEPLOYMENT | Results must be documented and pass thresholds |
| **Decision tree for ambiguous cases** | When is something a Process vs a State? | CRITICAL — BLOCKS LABELING | Codebook must include decision tree for every boundary |
| **Boundary definitions** | Where exactly does "small-group" end and "network" begin? | CRITICAL — BLOCKS LABELING | Numeric boundaries where possible (e.g., 3-12 = small group) |
| **Training protocol** | How to train a new labeler | HIGH — BLOCKS SCALE | New rater must achieve α ≥ 0.70 on calibration set before labeling live atoms |
| **Noise testing** | Inject known errors to verify detection | HIGH — BLOCKS SHIPPING | Detection rate ≥ 70% before system goes live |

---

## 4. MANDATORY GATES: THE PIPELINE WITH VALIDATION AT EVERY STAGE

This is the core change from v1. Validation is not a phase you do once. It's a gate at every stage transition.

### 4.1 The 7-Stage Pipeline with Mandatory Validation Gates and Benchmarks

Every gate references the specific rubric from Section 1.1 that it uses. Every enforcer from Section 1.2 is assigned. No gate operates without a benchmark.

```
STAGE 1: INGEST
  Enforcer: Intake Guard (#1)
  Knowledge enters the system (vault doc, voice transcript, research output, etc.)
  │
  ├── MANDATORY GATE 1: STRUCTURE CHECK
  │   ✓ Does it have a valid atom ID? (AMP-{APQC#}-{SEQ}-{VERSION})
  │   ✓ Does it have radical attribution? (human, AI, fact %, confidence band)
  │   ✓ Is the raw text extractable and non-empty?
  │   ✓ Source logged? (monologue_transcript / vault_doc / research_output / etc.)
  │   BENCHMARK: Schema validation (structural only — no scoring yet)
  │   METRIC CHECK: 3-Gate Formula (Buzzard/Tao/Candès) on any metrics extracted
  │   ✗ FAIL → Reject to inbox. Cannot proceed.
  │
  ▼
STAGE 2: LABEL
  Enforcer: Taxonomy Enforcer (#2) + Attribution Enforcer (#7)
  Apply PUDDING label (WHAT.HOW.SCALE.TIME) using codebook
  Assign all 5 taxonomy layers simultaneously
  │
  ├── MANDATORY GATE 2: LABEL VALIDITY CHECK
  │   ✓ Is WHAT one of {P, I, R, E, S, C, M}? (7 valid values)
  │   ✓ Is HOW one of {=, +, -, >, ~, !, ?}? (7 valid values)
  │   ✓ Is SCALE one of {0, 1, 2, 3, 4, 5, 6}? (7 valid values)
  │   ✓ Is TIME one of {i, m, l, v, p, ∞}? (6 valid values)
  │   ✓ Was the codebook consulted? (labeler must confirm)
  │   ✓ Is the decision tree path recorded? (which rules were applied)
  │   ✓ ALL 5 taxonomy layers assigned?
  │       Layer 1: Structural (= PUDDING label)
  │       Layer 2: Functional (role in system)
  │       Layer 3: Domain (business/technical domain)
  │       Layer 4: Temporal (persistence duration)
  │       Layer 5: Maturity (validation status)
  │   ✓ Semantic dimensions assigned? (3-7 from controlled vocabulary)
  │   BENCHMARK: Label validity regex + 5-layer completeness check
  │   ✗ FAIL → Return to labeler with specific error. Cannot proceed.
  │
  ├── MANDATORY GATE 2b: INTER-RATER CHECK (sampled)
  │   ✓ Every Nth atom (N=5 during pilot, N=20 at scale) gets dual-labeled
  │   ✓ Second rater is independent (different model or person)
  │   ✓ If raters disagree → adjudication process triggers (see Section 6.3)
  │   ✓ Running α tracked per facet
  │   BENCHMARK: Krippendorff's α per facet
  │       α < 0.667 → SYSTEM HALT
  │       0.667 ≤ α < 0.70 → Pilot only (no production)
  │       0.70 ≤ α < 0.80 → Deploy (can label, cannot ship)
  │       α ≥ 0.80 → Ship-ready
  │       α ≥ 0.90 → Gold standard
  │   ✗ FAIL → Freeze labeling. Codebook review required. Cannot proceed.
  │
  ▼
STAGE 3: SCORE
  Enforcer: Quality Scorer (#3) + Compliance Monitor (#10)
  Apply RAEI rubric against stated goal. Calculate PRS. Apply believability weighting.
  │
  ├── MANDATORY GATE 3: RUBRIC & BENCHMARK CHECK
  │   ✓ Goal explicitly stated? (rubric is meaningless without a goal)
  │   ✓ RAEI rubric applied?
  │       Relevance (0-5): Does this help toward the goal?
  │       Actionability (0-5): Can we do something with this?
  │       Evidence (0-5): How well supported is this?
  │       Impact (0-5): How much does this matter?
  │       Total (0-20): Sum of 4 dimensions
  │   BENCHMARK: RAEI total ≥ 12 to proceed as pudding ingredient
  │   ✓ PRS calculated? (6 weighted dimensions → 0-10 composite)
  │   BENCHMARK: PRS ≥ 5.0 to proceed, PRS ≥ 7.0 to ship, PRS ≥ 9.0 gold
  │   ✓ Believability weight applied? (Dalio meritocracy)
  │       Expert credibility on THIS topic (not general authority)
  │       Weighted by: domain expertise, chronology (Lindy), citations, adoption
  │   ✓ PUDDING label consistent with rubric scores?
  │       HOW = ? (emerging) + Evidence ≥ 4 (strong) → CONFLICT
  │       HOW = = (stable) + Evidence = 0 (none) → CONFLICT
  │       Actionability ≥ 4 (actioned) + HOW = ? (emerging) → CONFLICT
  │   ✓ Relevant analytical lenses applied? (minimum 3 of 12 lenses)
  │   ✓ 3-Gate Metric Formula passed for any metrics used in scoring?
  │       Buzzard: Can we define it exactly and compute it unambiguously?
  │       Tao: Does it behave consistently over time?
  │       Candès: Is it statistically robust (sample, variance, outliers)?
  │       ALL 3 must pass or metric is invalid for decisions.
  │   ✗ FAIL → Flag conflict. Resolve label OR rubric. Cannot proceed.
  │
  ▼
STAGE 4: RESEARCH & MATCH
  Enforcer: Research Validator (#4)
  Triple search (success + failure patterns). Pattern-match across domains.
  │
  ├── MANDATORY GATE 4: MATCH QUALITY CHECK
  │   ✓ Triple search completed? (success + failure patterns, ≥2 search engines)
  │   ✓ ≥3 named techniques found with neutral labels?
  │   ✓ Failure patterns included? (not optional)
  │   ✓ Research ID assigned? (RES-YYYY-MM-DD-NNN)
  │   ✓ Are matched atoms from genuinely different domains?
  │   BENCHMARK: Jaccard Slot Score ≥ 0.75 (3/4 facets match)
  │   BENCHMARK: Both atoms RAEI total ≥ 12/20
  │   BENCHMARK: Believability weight applied to matched sources
  │   BENCHMARK: SYNERGY Score calculated: (Shared)² × Unique_A × Unique_B
  │   ✓ Match logged with full provenance?
  │   ✗ FAIL → Match discarded. Not a valid pudding candidate.
  │
  ▼
STAGE 5: MIX (PUDDING RECIPE)
  Enforcer: Test Director (#5)
  Build the A→B→C recipe — state the hypothesis and the 1+1=3
  │
  ├── MANDATORY GATE 5: RECIPE VALIDITY & SCORING CHECK
  │   ✓ Is A from domain X and C from domain Y (X ≠ Y)?
  │   ✓ Is the bridge B a neutral mechanism (not named after a domain)?
  │   ✓ Is the 1+1=3 explicitly stated? (not just "they're related")
  │   ✓ Is there a testable prediction?
  │   ✓ Is the recipe marked as HYPOTHESIS (not treated as proven)?
  │   BENCHMARK: MASHUP_SCORE calculated (6 components, 0-100):
  │       Domain Distance (0-10, weight 2.0)
  │       Pattern Alignment (0-10, weight 3.0)
  │       Gap Filling (0-10, weight 2.5)
  │       Tension Bonus (0-10, weight 1.5)
  │       SMB Applicability (0-10, weight 2.0)
  │       Novelty Bonus (0-10, weight 1.0)
  │       TOTAL = weighted sum, max 100
  │       THRESHOLD: ≥ 60 = valid mashup, ≥ 80 = priority mashup
  │   BENCHMARK: Simple recipe score also calculated:
  │       (Shared Dims × 2) + Unique_A + Unique_B ≥ 5
  │   BENCHMARK: Cross-domain advanced score:
  │       (Domain Distance × Pattern Alignment) + Gap Complement + Tension Bonus ≥ 13
  │   ✗ FAIL → Recipe rejected. Missing components must be added. Cannot proceed.
  │
  ▼
STAGE 6: TEST
  Enforcer: Test Director (#5) + Chaos Tester (#8)
  Validate the recipe — does the connection actually work?
  │
  ├── MANDATORY GATE 6: TEST INTEGRITY & INTENTLOGIC CHECK
  │   ✓ Was the test designed BEFORE seeing results? (no post-hoc fitting)
  │   ✓ Was the test run with sufficient sample/power?
  │   ✓ Were results measured against pre-defined thresholds?
  │   BENCHMARK: INTENTLOGIC scored (4 dims × 0-3, multiplicative):
  │       Clarity of Intent (CI): 0-3
  │       Causal Logic Quality (CL): 0-3
  │       Experiment Design Strength (ED): 0-3
  │       Learning Extraction Depth (LE): 0-3
  │       INTENTLOGIC = CI × CL × ED × LE (max 81)
  │       ANY dimension = 0 → VOID (test is invalid, don't trust)
  │       1-9: weak (sandbox only)
  │       10-27: OK (internal use)
  │       28-81: strong (eligible for client-facing)
  │   BENCHMARK: PRS recalculated after test results
  │   ✓ Is the outcome one of: {PROVEN, PARTIALLY_SUPPORTED, REFUTED, INCONCLUSIVE}?
  │   ✓ Are all test results logged with full attribution?
  │   ✓ Maturity layer updated? (hypothesis → tested_internal → tested_client → proven)
  │   ✗ FAIL → Test invalid. Redesign and re-run. Cannot proceed.
  │
  ▼
STAGE 7: SHIP / ARCHIVE / REJECT
  Enforcer: Ship Gate (#6) + Attribution Enforcer (#7)
  Final disposition — this is the only point where something exits the pipeline
  │
  ├── MANDATORY GATE 7: FINAL BENCHMARK CHECK (the final boss)
  │   ✓ ALL prior gates passed? (G1 through G6 — full audit trail)
  │   BENCHMARK: Krippendorff's α ≥ 0.80 per facet (ship threshold)
  │   BENCHMARK: PRS ≥ 7.0 (ship), ≥ 9.0 (gold)
  │   BENCHMARK: RAEI total ≥ 12/20
  │   BENCHMARK: PUDDING Tier calculated:
  │       Attribution × Authority × Completeness × Applicability × Validation
  │       VOID (any factor = 0) → Cannot ship
  │       RAW (1-99) → Cannot ship
  │       BRONZE (100-999) → Internal only
  │       SILVER (1K-4,999) → Ship-ready (SILVER+ required for production)
  │       GOLD (≥5K) → Priority implementation
  │   BENCHMARK: INTENTLOGIC ≥ 10 (internal) or ≥ 28 (client-facing)
  │   BENCHMARK: MASHUP_SCORE ≥ 60 (if recipe)
  │   ✓ Full radical attribution present?
  │   ✓ Atom ID in canonical format? (AMP-{APQC#}-{SEQ}-{VERSION})
  │   ✓ All 5 taxonomy layers assigned?
  │   ✓ Semantic dimensions (3-7) assigned?
  │   ✓ AMPS score calculated for the process this atom belongs to?
  │   ✗ FAIL → Cannot ship. Returns to earliest failing gate.
  │
  │   OUTCOMES (based on benchmark scores):
  │   ├── SHIP (PRS ≥ 7.0, α ≥ 0.80, Tier ≥ SILVER, all gates pass) → Production
  │   ├── RESEARCH (PRS ≥ 5.0 but < 7.0) → Back to Stage 4 for more work
  │   ├── ARCHIVE (tested but inconclusive) → Stored for future reference
  │   └── REJECT (PRS < 5.0 or Tier = VOID) → Documented why, permanently marked
```

### 4.2 THE PRIORITY FORMULA (What Runs Next)

When multiple atoms are competing for attention, the existing priority formula decides:

```
PRIORITY = PUDDING_TIER_SCORE × INTENTLOGIC × SYNERGY

Where:
  PUDDING_TIER_SCORE = Attribution × Authority × Completeness × Applicability × Validation
  INTENTLOGIC = CI × CL × ED × LE
  SYNERGY = (Shared)² × Unique_A × Unique_B (or 1 if not a mashup)

Rules:
  - P = 0 or I = 0 → auto-killed before it ever hits the GPUs
  - Sort descending; only run the top N in parallel
  - SILVER+ puddings influence live systems by default
```

### 4.2 Gate Enforcement Mechanisms

How each gate is actually enforced — not just documented:

| Gate | Enforcement Method | Frequency | Who Checks | Escalation |
|------|-------------------|-----------|------------|------------|
| **G1: Structure** | Automated schema validation | Every atom at ingest | Ingest script / Gatekeeper Agent | Reject immediately — no manual override |
| **G2: Label Validity** | Automated regex + value check | Every atom at labeling | Labeling script | Return to labeler with error code |
| **G2b: Inter-Rater** | Dual-labeling + α calculation | Sampled (every 5th atom pilot / every 20th at scale) | Independent second rater + Python krippendorff | **SYSTEM HALT if α < 0.667** |
| **G3: Rubric Integrity** | Automated consistency check (label vs rubric) | Every scored atom | Scoring script | Flag conflicts for human adjudication |
| **G4: Match Quality** | Automated Jaccard + domain check | Every match attempt | Matching script | Discard silently — bad matches don't propagate |
| **G5: Recipe Validity** | Checklist validation (7 required fields) | Every recipe | Recipe builder (human or AI) | Recipe blocked until complete |
| **G6: Test Integrity** | Pre-registration + result logging | Every test | Test designer + independent reviewer | Invalid test results discarded |
| **G7: Shipping** | Full audit trail check (all prior gates) | Every item at ship decision | Enforcer Agent (automated) + Human (final sign-off) | Returns to earliest failing gate |

### 4.3 The System Halt Protocol

When running Krippendorff's Alpha drops below the minimum threshold:

```
IF running_alpha(any_facet) < 0.667:
    1. HALT all new labeling immediately
    2. LOG: which facet, which atoms, which raters, what the disagreement was
    3. TRIGGER: Codebook Review Process
        a. Pull all atoms where raters disagreed on this facet
        b. Identify pattern (which codes are confused?)
        c. Update codebook: sharpen definitions, add decision tree branches, add examples
        d. Run calibration set (10 atoms, 3 raters) on updated codebook
        e. IF calibration α ≥ 0.70 → Resume labeling
        f. IF calibration α < 0.70 → Escalate to Ewan for codebook redesign
    4. ALL atoms labeled since last passing α check are QUARANTINED
        - They don't get deleted
        - They get re-labeled once codebook is fixed
        - They cannot be used for matching, scoring, or shipping until re-validated
```

---

## 5. THE TEST PROTOCOL (Establishing the Gates)

Before the mandatory gates can be enforced, the system must be calibrated. This is the test protocol that establishes the baseline.

### Phase 0: Build the Codebook (BEFORE any testing)

This is what you don't have yet and it's non-negotiable. **No labeling can happen without this. Full stop.**

**For each WHAT code (P, I, R, E, S, C, M)**:
```yaml
code: P
name: Process
definition: "An action, procedure, or workflow that transforms inputs into outputs over time."
decision_rule: "If the concept describes something that DOES something (a verb), it is a Process."
boundary: "If it describes what something IS (a noun/state), it is NOT a Process — check Entity or State."
examples:
  - "Kaizen Loop" → P (it's an action that runs continuously)
  - "Financial Autopsy" → P (it's a procedure that analyses data)
not_examples:
  - "FalkorDB" → E (it's a thing, not an action)
  - "Death Spiral" → S (it's a condition, not an action)
  - "PUDDING 2026" → M (it's a framework about frameworks)
common_confusion:
  - "Process vs State": Processes change things. States describe conditions.
  - "Process vs Meta": Meta describes how descriptions work. Process does work.
decision_tree: |
  Q1: Does it DO something (transform, act, execute)?
    YES → Likely Process (P). Go to Q2.
    NO → Not Process. Check Entity, State, or Meta.
  Q2: Does it describe how OTHER things are described or classified?
    YES → It's Meta (M), not Process.
    NO → Confirmed Process (P).
mandatory: true  # This code MUST be in the codebook before ANY labeling begins
```

**For each HOW code (=, +, -, >, ~, !, ?)**:
```yaml
code: ">"
name: Tipping
definition: "Behaviour that is threshold-based — nothing happens until a critical point is crossed, then action fires instantly."
decision_rule: "If there is a binary trigger (below threshold = nothing, above = fires), it is Tipping."
boundary: "If it grows gradually, it is Amplifying (+), not Tipping."
examples:
  - "Quorum sensing" → > (fires when enough signals converge)
  - "MTD compliance deadline" → > (nothing until deadline, then penalty)
not_examples:
  - "Kaizen improvement" → + (gradual compounding, no threshold)
  - "Agent heartbeat" → ~ (oscillating, not threshold-based)
common_confusion:
  - "Tipping vs Disrupting": Tipping is threshold-based. Disrupting breaks existing patterns (regardless of threshold).
  - "Tipping vs Amplifying": Amplifying is gradual growth. Tipping is sudden binary change.
decision_tree: |
  Q1: Is there a threshold or trigger point?
    YES → Likely Tipping (>). Go to Q2.
    NO → Not Tipping. Check Amplifying, Stable, or Oscillating.
  Q2: Is the change gradual before the threshold?
    YES → Might be Amplifying (+) with a cap. Check if the threshold is the defining feature.
    NO → Confirmed Tipping (>).
mandatory: true
```

**Same format for SCALE (0-6) and TIME (i/m/l/v/p/∞).**

This gives us ~28 detailed code definitions. That IS the codebook. **ALL 28 must be written before any labeling begins.**

### Phase 1: Pilot Study (5 atoms, 3 raters)

**Purpose**: Does the codebook work at all? **This phase is MANDATORY before any production labeling.**

1. Select 5 atoms from the existing test dataset — ideally ones that span different domains
2. Give 3 independent raters the codebook + the 5 atoms (raw text only, no pre-existing labels)
3. Each rater independently assigns: WHAT, HOW, SCALE, TIME
4. Calculate Krippendorff's Alpha per facet:
   - α(WHAT): Agreement on entity type
   - α(HOW): Agreement on behaviour
   - α(SCALE): Agreement on scope
   - α(TIME): Agreement on duration
5. **MANDATORY THRESHOLD**: If any facet α < 0.667 → STOP. Refine codebook. Re-run Phase 1. No exceptions.
6. **MANDATORY LOGGING**: All rater assignments, disagreements, and α values recorded permanently

**What counts as a "rater"**:
- Can be human or AI (Claude, Grok, GPT, Perplexity)
- If AI, must be different models (not the same model twice — that's not independence)
- Mixed human + AI is ideal (you + 2 different AI models)

**Expected outcome**: WHAT and TIME should score high (they're the most concrete). HOW and SCALE are where disagreements will concentrate.

**Gate condition**: Phase 1 must pass (all facets α ≥ 0.667) before Phase 2 begins. No exceptions.

### Phase 2: Full Test (20 atoms, 3+ raters)

**Purpose**: Does it scale? **MANDATORY before any production deployment.**

1. Select 20 atoms from across ALL domains (governance, frameworks, agent architecture, business strategy, products, tech architecture, brand, knowledge management)
2. Give raters the refined codebook + 20 atoms (raw text, no pre-existing labels)
3. Each rater independently assigns: WHAT, HOW, SCALE, TIME + the full combined label
4. Calculate:
   - α per facet (WHAT, HOW, SCALE, TIME)
   - α for full label (all 4 combined — this will be lower)
   - Per-code confusion matrix (which codes get confused most?)
   - Percentage exact match (how often do raters produce identical 4-character labels?)
5. **MANDATORY THRESHOLDS**:
   - Per-facet α ≥ 0.70 → **PASS** (reliable for deployment)
   - Per-facet α ≥ 0.80 → **GOLD** (strong reliability)
   - Full label exact match ≥ 50% → **Acceptable** (given 2,401 possible labels)
   - Full label exact match ≥ 70% → **Strong**
6. **MANDATORY**: If ANY facet α < 0.70 → codebook refinement cycle. Re-test. No deployment until threshold met.

**Gate condition**: Phase 2 must pass (all facets α ≥ 0.70) before production labeling begins. No exceptions.

### Phase 3: Adversarial Test (Noise Injection)

**Purpose**: Can the system detect bad labels? **MANDATORY before system goes live.**

Based on RaTE methodology ([Gao & Langlais, 2023](https://aclanthology.org/2023.iwcs-1.18.pdf)):

1. Take 10 correctly-labelled atoms
2. Randomly corrupt 1 facet per atom (e.g., change WHAT from P to S, or HOW from + to >)
3. Give the corrupted set to a rater and ask: "Which labels are wrong?"
4. Measure: detection rate, false positive rate
5. **MANDATORY THRESHOLD**: Detection rate ≥ 70% or codebook definitions are not sharp enough → refine and re-test

**Gate condition**: Phase 3 must pass (detection rate ≥ 70%) before the system is considered operationally valid. No exceptions.

### Phase 4: Cross-Domain Match Validation

**Purpose**: Does the PUDDING matching (identical labels across domains) actually find real connections? **MANDATORY before recipes can be shipped.**

1. Run the labelled dataset through pattern matching
2. For each cross-domain label match (e.g., Trial by AI and Cross-Encoder Reranking both labeled P.>.2.i):
   - Present the pair to a rater WITHOUT telling them they share a label
   - Ask: "Is there a meaningful structural connection between these two concepts?"
   - Score: Yes / Partial / No
3. Calculate: precision of PUDDING matching = (% of matches rated Yes or Partial)
4. **MANDATORY THRESHOLD**: ≥ 70% precision → PUDDING matching works

**Gate condition**: Phase 4 must pass (precision ≥ 70%) before cross-domain recipes can be shipped. No exceptions.

---

## 6. ONGOING ENFORCEMENT (Post-Calibration)

Once the system is calibrated (Phases 0-4 passed), these are the mandatory ongoing checks:

### 6.1 Continuous Inter-Rater Monitoring

```python
# This runs automatically. Not optional.
# Every 20th atom gets dual-labeled.
# Running α is recalculated after every dual-labeled atom.
# If α drops → system halt protocol triggers.

SAMPLE_RATE_PILOT = 5     # Every 5th atom during first 100 atoms
SAMPLE_RATE_PRODUCTION = 20  # Every 20th atom after first 100
ALPHA_MINIMUM = 0.667     # Below this → SYSTEM HALT
ALPHA_SHIP = 0.80         # Below this → cannot ship (can still label)
ALPHA_GOLD = 0.90         # Above this → gold standard

def should_dual_label(atom_count):
    """Returns True if this atom should be dual-labeled."""
    rate = SAMPLE_RATE_PILOT if atom_count < 100 else SAMPLE_RATE_PRODUCTION
    return atom_count % rate == 0

def check_running_alpha(all_dual_labels):
    """Calculate running α and enforce thresholds."""
    for facet in ['WHAT', 'HOW', 'SCALE', 'TIME']:
        alpha = krippendorff.alpha(
            reliability_data=extract_facet(all_dual_labels, facet),
            level_of_measurement='nominal'
        )
        if alpha < ALPHA_MINIMUM:
            trigger_system_halt(facet, alpha)
            return False
    return True
```

### 6.2 Codebook Audit Schedule

| Trigger | Action | Mandatory? |
|---------|--------|------------|
| Every 50 new atoms labeled | Review codebook for edge cases that emerged | **YES** |
| Any α drop below 0.75 (warning zone) | Targeted codebook review on weak facet | **YES** |
| Any α drop below 0.667 | SYSTEM HALT + full codebook review | **YES — BLOCKS ALL** |
| New code proposed (e.g., 8th WHAT category) | Full re-validation cycle (Phase 1-2 minimum) | **YES — BLOCKS DEPLOYMENT** |
| Quarterly | Independent external audit of 20 random atoms | **YES** |

### 6.3 Adjudication Process (When Raters Disagree)

```
DISAGREEMENT DETECTED (rater_1.label ≠ rater_2.label on any facet):
  │
  ├── 1. LOG: Record both labels, both raters, the atom, the facet
  │
  ├── 2. CLASSIFY disagreement type:
  │   ├── Adjacent confusion (e.g., Process vs Meta) → Codebook may need sharper boundary
  │   ├── Distant confusion (e.g., Process vs State) → Possible labeler error or codebook gap
  │   └── Systematic (same confusion repeating) → Codebook DEFINITELY needs update
  │
  ├── 3. ADJUDICATE:
  │   ├── Option A: Third rater breaks the tie (majority wins)
  │   ├── Option B: Expert review (Ewan or designated expert decides)
  │   └── Option C: If systematic → pause, fix codebook, re-test
  │
  ├── 4. RECORD the adjudication decision and reasoning
  │
  └── 5. UPDATE codebook if the disagreement reveals a gap
      └── Any codebook update → re-run calibration set (10 atoms, 3 raters)
          └── IF calibration α ≥ 0.70 → Resume
          └── IF calibration α < 0.70 → Escalate
```

### 6.4 Label Integrity Checks at Every Stage Transition

These run automatically whenever an atom moves between pipeline stages:

```python
def gate_check(atom, current_stage, target_stage):
    """
    Mandatory check before any stage transition.
    Returns (pass: bool, errors: list)
    """
    errors = []

    # UNIVERSAL CHECKS (apply at EVERY transition)
    if not atom.pudding_label:
        errors.append("BLOCK: No PUDDING label assigned")
    if not atom.atom_id or not re.match(r'AMP-\d+-\d+-\d+', atom.atom_id):
        errors.append("BLOCK: Invalid or missing atom ID")
    if not atom.attribution:
        errors.append("BLOCK: No radical attribution")

    # STAGE-SPECIFIC CHECKS
    if target_stage >= STAGE_SCORE:
        if not label_is_valid(atom.pudding_label):
            errors.append("BLOCK: PUDDING label has invalid facet values")
        if not atom.codebook_path_recorded:
            errors.append("BLOCK: Decision tree path not recorded")

    if target_stage >= STAGE_MATCH:
        if atom.rubric_total is None:
            errors.append("BLOCK: Rubric not scored")
        if atom.rubric_total < 12:
            errors.append("WARN: Below pudding threshold (12/20)")
        if label_rubric_conflict(atom):
            errors.append("BLOCK: PUDDING label conflicts with rubric scores")

    if target_stage >= STAGE_MIX:
        if atom.rubric_total < 12:
            errors.append("BLOCK: Cannot mix atoms below threshold")

    if target_stage >= STAGE_SHIP:
        if atom.inter_rater_alpha < ALPHA_SHIP:
            errors.append(f"BLOCK: α = {atom.inter_rater_alpha:.3f} < {ALPHA_SHIP}")
        if atom.prs < 7.0:
            errors.append(f"BLOCK: PRS = {atom.prs:.1f} < 7.0")
        if not all_taxonomy_layers_assigned(atom):
            errors.append("BLOCK: Missing taxonomy layers")
        if not atom.semantic_dimensions or len(atom.semantic_dimensions) < 3:
            errors.append("BLOCK: Fewer than 3 semantic dimensions")

    passed = len([e for e in errors if e.startswith("BLOCK")]) == 0
    return passed, errors
```

---

## 7. THE MATHEMATICS

### 7.1 Krippendorff's Alpha Formula

For each facet independently:

```
α = 1 - (Do / De)

Where:
  Do = observed disagreement (how much raters actually disagree)
  De = expected disagreement by chance (how much they'd disagree if random)
```

For nominal data (which PUDDING codes are):

```
Do = (1 / n(n-1)) × Σ_k Σ_l (o_kl × δ²(k,l))

Where:
  n = total number of pairable values
  o_kl = number of times value k and value l are paired
  δ²(k,l) = 1 if k ≠ l, 0 if k = l (nominal metric)

De = (1 / (n(n-1))) × Σ_k Σ_l (n_k × n_l × δ²(k,l))

Where:
  n_k = marginal frequency of value k
```

### 7.2 Interpretation — Mandatory Thresholds

| Alpha | Meaning | Pipeline Action | Mandatory? |
|-------|---------|----------------|------------|
| α ≥ 0.90 | Gold standard | Ship with full confidence | Aspirational target |
| α ≥ 0.80 | Strong reliability | Ship it | **MANDATORY for shipping** |
| 0.70 ≤ α < 0.80 | Good — deployment-ready | Can label production atoms, cannot ship | **MANDATORY for deployment** |
| 0.667 ≤ α < 0.70 | Acceptable — tentative | Can label pilot atoms only | **MINIMUM for any labeling** |
| α < 0.667 | Unreliable | **SYSTEM HALT. Fix codebook. Re-test.** | **MANDATORY HALT** |
| α ≤ 0 | Worse than chance | **FUNDAMENTAL FAILURE. Redesign required.** | **MANDATORY HALT + ESCALATION** |

### 7.3 Statistical Significance

With 3 raters and 20 items:
- Degrees of freedom: (raters - 1) × (items - 1) = 2 × 19 = 38
- Bootstrap confidence interval recommended (Krippendorff, 2004): resample 10,000 times
- Report: α [95% CI: lower, upper]
- **MANDATORY**: Report confidence intervals. A point estimate alone is not sufficient for shipping decisions.

### 7.4 Full Label Agreement

For the combined 4-facet label:

```
Exact Match Rate = (# atoms where ALL raters agree on ALL 4 facets) / (total atoms)
```

Expected baseline by chance (if each facet has 7 categories):
```
P(random exact match) = (1/7)^4 = 1/2401 ≈ 0.04%
```

So ANY agreement above 0.04% is already better than chance. The question is how much better.

### 7.5 Partial Match (Jaccard on PUDDING labels)

If raters don't produce identical labels, measure how close they are:

```
Jaccard(label_A, label_B) = (matching facets) / 4

Examples:
  P.>.3.i vs P.>.3.i → Jaccard = 4/4 = 1.0 (perfect)
  P.>.3.i vs P.>.3.m → Jaccard = 3/4 = 0.75 (one facet off)
  P.>.3.i vs S.!.5.l → Jaccard = 0/4 = 0.0 (completely different)
```

Report: mean Jaccard across all rater pairs. **MANDATORY metric alongside α.**

---

## 8. TOOLS FOR RUNNING THE TEST

### Option A: Manual (Spreadsheet)

1. Create spreadsheet with columns: Atom_ID, Raw_Text, Rater_1_WHAT, Rater_1_HOW, Rater_1_SCALE, Rater_1_TIME, Rater_2_WHAT, ... etc.
2. Calculate Alpha using the SPSS macro or Python `krippendorff` library
3. Cheap, fast, no infrastructure needed

### Option B: Label Studio (Open Source)

- [Label Studio](https://labelstud.io) — Apache-2 licensed, supports taxonomy up to 10,000 classes
- Set up PUDDING as a taxonomy with 4 facets
- Track inter-annotator agreement natively
- Self-hosted on Beast if needed

### Option C: Python Script (Recommended — and mandatory for automated gate enforcement)

```python
#!/usr/bin/env python3
"""
PUDDING 2026 — Mandatory Validation Engine
This is not optional. This runs at every stage transition.
"""

# pip install krippendorff numpy
import krippendorff
import numpy as np
import json
import sys
from datetime import datetime

# ═══════════════════════════════════════════════════════
# CONSTANTS — THESE ARE THE LAW. DO NOT CHANGE WITHOUT
# FULL RE-VALIDATION (Phase 1-4).
# ═══════════════════════════════════════════════════════

ALPHA_HALT = 0.667       # Below this → SYSTEM HALT
ALPHA_DEPLOY = 0.70      # Below this → no production labeling
ALPHA_SHIP = 0.80        # Below this → no shipping
ALPHA_GOLD = 0.90        # Above this → gold standard

PRS_SHIP = 7.0           # Below this → no shipping
PRS_GOLD = 9.0           # Above this → gold standard

RUBRIC_THRESHOLD = 12    # Below this → not a pudding ingredient
MIN_SEMANTIC_DIMS = 3    # Minimum semantic dimensions per atom
MAX_SEMANTIC_DIMS = 7    # Maximum semantic dimensions per atom

SAMPLE_RATE_PILOT = 5    # Dual-label every 5th atom during pilot
SAMPLE_RATE_PROD = 20    # Dual-label every 20th atom in production

# Valid facet values — anything else is rejected
VALID_WHAT = {'P', 'I', 'R', 'E', 'S', 'C', 'M'}
VALID_HOW = {'=', '+', '-', '>', '~', '!', '?'}
VALID_SCALE = {'0', '1', '2', '3', '4', '5', '6'}
VALID_TIME = {'i', 'm', 'l', 'v', 'p', '∞'}

# Integer encoding for Krippendorff calculation
WHAT_MAP = {'P': 1, 'I': 2, 'R': 3, 'E': 4, 'S': 5, 'C': 6, 'M': 7}
HOW_MAP = {'=': 1, '+': 2, '-': 3, '>': 4, '~': 5, '!': 6, '?': 7}
SCALE_MAP = {'0': 0, '1': 1, '2': 2, '3': 3, '4': 4, '5': 5, '6': 6}
TIME_MAP = {'i': 1, 'm': 2, 'l': 3, 'v': 4, 'p': 5, '∞': 6}


def validate_label(label_str):
    """
    MANDATORY GATE 2: Validate a PUDDING label string.
    Returns (valid: bool, errors: list)
    """
    errors = []
    parts = label_str.split('.')

    if len(parts) != 4:
        errors.append(f"Label must have 4 facets, got {len(parts)}: '{label_str}'")
        return False, errors

    what, how, scale, time = parts

    if what not in VALID_WHAT:
        errors.append(f"WHAT='{what}' not in {VALID_WHAT}")
    if how not in VALID_HOW:
        errors.append(f"HOW='{how}' not in {VALID_HOW}")
    if scale not in VALID_SCALE:
        errors.append(f"SCALE='{scale}' not in {VALID_SCALE}")
    if time not in VALID_TIME:
        errors.append(f"TIME='{time}' not in {VALID_TIME}")

    return len(errors) == 0, errors


def calculate_alpha_per_facet(ratings):
    """
    MANDATORY GATE 2b: Calculate Krippendorff's Alpha per facet.
    
    ratings: list of dicts, each with keys 'rater', 'atom_id', 'WHAT', 'HOW', 'SCALE', 'TIME'
    Returns: dict of {facet: alpha_value}
    """
    # Group by atom
    atoms = sorted(set(r['atom_id'] for r in ratings))
    raters = sorted(set(r['rater'] for r in ratings))

    results = {}
    for facet, code_map in [('WHAT', WHAT_MAP), ('HOW', HOW_MAP),
                             ('SCALE', SCALE_MAP), ('TIME', TIME_MAP)]:
        # Build reliability matrix: rows = raters, cols = atoms
        matrix = []
        for rater in raters:
            row = []
            for atom in atoms:
                match = [r for r in ratings if r['rater'] == rater and r['atom_id'] == atom]
                if match:
                    row.append(code_map.get(match[0][facet]))
                else:
                    row.append(None)  # Missing data — Krippendorff handles this
            matrix.append(row)

        # Replace None with np.nan for krippendorff library
        np_matrix = np.array([[np.nan if v is None else v for v in row] for row in matrix],
                             dtype=float)

        alpha = krippendorff.alpha(reliability_data=np_matrix, level_of_measurement='nominal')
        results[facet] = round(alpha, 4)

    return results


def enforce_thresholds(alpha_results, mode='production'):
    """
    MANDATORY: Enforce α thresholds. Returns (passed: bool, actions: list)
    """
    actions = []
    all_pass = True

    for facet, alpha in alpha_results.items():
        if alpha < ALPHA_HALT:
            actions.append(f"🛑 SYSTEM HALT: {facet} α = {alpha:.3f} < {ALPHA_HALT}")
            all_pass = False
        elif alpha < ALPHA_DEPLOY:
            actions.append(f"⛔ DEPLOYMENT BLOCKED: {facet} α = {alpha:.3f} < {ALPHA_DEPLOY}")
            if mode == 'production':
                all_pass = False
        elif alpha < ALPHA_SHIP:
            actions.append(f"⚠️ SHIPPING BLOCKED: {facet} α = {alpha:.3f} < {ALPHA_SHIP}")
        elif alpha >= ALPHA_GOLD:
            actions.append(f"🥇 GOLD: {facet} α = {alpha:.3f}")
        else:
            actions.append(f"✅ PASS: {facet} α = {alpha:.3f}")

    return all_pass, actions


def check_label_rubric_consistency(label_str, rubric_scores):
    """
    MANDATORY GATE 3: Check for conflicts between label and rubric.
    Returns list of conflicts (empty = no conflicts).
    """
    conflicts = []
    parts = label_str.split('.')
    if len(parts) != 4:
        return ["Invalid label format"]

    what, how, scale, time = parts
    evidence = rubric_scores.get('evidence', 0)
    actionability = rubric_scores.get('actionability', 0)

    # Conflict: HOW=? (emerging) but Evidence=5 (proven)
    if how == '?' and evidence >= 4:
        conflicts.append(
            f"HOW='?' (emerging) conflicts with Evidence={evidence} (well-supported). "
            f"If evidence is strong, it's not emerging."
        )

    # Conflict: HOW='=' (stable) but Evidence=0 (no evidence)
    if how == '=' and evidence == 0:
        conflicts.append(
            f"HOW='=' (stable) but Evidence=0 (no evidence). "
            f"How can we claim stability without any evidence?"
        )

    # Conflict: Actionability=5 (proven/actioned) but TIME='?' 
    if actionability >= 4 and how == '?':
        conflicts.append(
            f"Actionability={actionability} (readily actionable) conflicts with HOW='?' (emerging). "
            f"If it's already actioned, it's not emerging."
        )

    return conflicts


def full_gate_check(atom, target_stage):
    """
    MANDATORY: Full gate check for stage transition.
    This is the function that enforces validation at every stage.
    
    Returns (passed: bool, errors: list, warnings: list)
    """
    errors = []
    warnings = []

    # UNIVERSAL CHECKS
    if not atom.get('pudding_label'):
        errors.append("BLOCK: No PUDDING label assigned")
    else:
        valid, label_errors = validate_label(atom['pudding_label'])
        if not valid:
            errors.extend([f"BLOCK: {e}" for e in label_errors])

    if not atom.get('atom_id'):
        errors.append("BLOCK: No atom ID")

    if not atom.get('attribution'):
        errors.append("BLOCK: No radical attribution")

    # STAGE-SPECIFIC CHECKS
    if target_stage >= 3:  # SCORE
        if not atom.get('codebook_path'):
            errors.append("BLOCK: Decision tree path not recorded for labeling")

    if target_stage >= 4:  # MATCH
        if atom.get('rubric_total') is None:
            errors.append("BLOCK: Rubric not scored")
        elif atom['rubric_total'] < RUBRIC_THRESHOLD:
            warnings.append(f"WARN: Rubric total {atom['rubric_total']} < {RUBRIC_THRESHOLD}")
        if atom.get('pudding_label') and atom.get('rubric_scores'):
            conflicts = check_label_rubric_consistency(
                atom['pudding_label'], atom['rubric_scores']
            )
            errors.extend([f"BLOCK: {c}" for c in conflicts])

    if target_stage >= 5:  # MIX
        if atom.get('rubric_total', 0) < RUBRIC_THRESHOLD:
            errors.append(f"BLOCK: Cannot mix atoms below threshold ({RUBRIC_THRESHOLD}/20)")

    if target_stage >= 7:  # SHIP
        alpha = atom.get('inter_rater_alpha', 0)
        if alpha < ALPHA_SHIP:
            errors.append(f"BLOCK: α = {alpha:.3f} < {ALPHA_SHIP} — cannot ship")
        prs = atom.get('prs', 0)
        if prs < PRS_SHIP:
            errors.append(f"BLOCK: PRS = {prs:.1f} < {PRS_SHIP} — cannot ship")
        dims = atom.get('semantic_dimensions', [])
        if len(dims) < MIN_SEMANTIC_DIMS:
            errors.append(f"BLOCK: {len(dims)} semantic dimensions < {MIN_SEMANTIC_DIMS} minimum")
        if not atom.get('taxonomy_layers') or len(atom['taxonomy_layers']) < 5:
            errors.append("BLOCK: Missing taxonomy layers (need all 5)")

    passed = len(errors) == 0
    return passed, errors, warnings


# ═══════════════════════════════════════════════════════
# MAIN — Run validation
# ═══════════════════════════════════════════════════════

if __name__ == '__main__':
    print("PUDDING 2026 Validation Engine — MANDATORY AT EVERY STAGE")
    print(f"Thresholds: HALT < {ALPHA_HALT} | DEPLOY ≥ {ALPHA_DEPLOY} | SHIP ≥ {ALPHA_SHIP} | GOLD ≥ {ALPHA_GOLD}")
    print(f"Timestamp: {datetime.utcnow().isoformat()}Z")
    print("=" * 60)

    # Example: validate a label
    test_label = "P.>.3.i"
    valid, errs = validate_label(test_label)
    print(f"\nLabel '{test_label}': {'VALID' if valid else 'INVALID'}")
    if errs:
        for e in errs:
            print(f"  ERROR: {e}")

    # Example: calculate alpha from pilot data
    pilot_ratings = [
        {'rater': 'Ewan',   'atom_id': 'AMP-1301-001-1', 'WHAT': 'P', 'HOW': '~', 'SCALE': '5', 'TIME': 'p'},
        {'rater': 'Claude',  'atom_id': 'AMP-1301-001-1', 'WHAT': 'P', 'HOW': '~', 'SCALE': '5', 'TIME': 'p'},
        {'rater': 'GPT',     'atom_id': 'AMP-1301-001-1', 'WHAT': 'P', 'HOW': '~', 'SCALE': '5', 'TIME': 'p'},

        {'rater': 'Ewan',   'atom_id': 'AMP-0701-002-1', 'WHAT': 'C', 'HOW': '=', 'SCALE': '6', 'TIME': '∞'},
        {'rater': 'Claude',  'atom_id': 'AMP-0701-002-1', 'WHAT': 'C', 'HOW': '=', 'SCALE': '6', 'TIME': '∞'},
        {'rater': 'GPT',     'atom_id': 'AMP-0701-002-1', 'WHAT': 'C', 'HOW': '=', 'SCALE': '5', 'TIME': '∞'},  # disagrees on SCALE

        {'rater': 'Ewan',   'atom_id': 'AMP-0501-003-1', 'WHAT': 'P', 'HOW': '=', 'SCALE': '3', 'TIME': 'i'},
        {'rater': 'Claude',  'atom_id': 'AMP-0501-003-1', 'WHAT': 'P', 'HOW': '=', 'SCALE': '3', 'TIME': 'i'},
        {'rater': 'GPT',     'atom_id': 'AMP-0501-003-1', 'WHAT': 'M', 'HOW': '=', 'SCALE': '3', 'TIME': 'i'},  # disagrees on WHAT
    ]

    print("\n--- Inter-Rater Reliability (Pilot) ---")
    alphas = calculate_alpha_per_facet(pilot_ratings)
    passed, actions = enforce_thresholds(alphas, mode='pilot')
    for action in actions:
        print(f"  {action}")
    print(f"\n  OVERALL: {'PASS' if passed else 'FAIL — ACTION REQUIRED'}")
```

---

## 9. CONVERSATION MAP: HOW THE 5-6 THREADS CONNECT

Here's the pattern across your recent conversations. Everything connects:

```
Thread 1 (Jan 22-23): PUDDING 2026 invented
   ├── Created WHAT.HOW.SCALE.TIME notation (2,401 possible labels)
   ├── Created 4-criteria rubric (R/A/E/I, 0-20)
   ├── Established radical attribution
   └── Key insight: "frantic measurement + relentless puddinging = the business"

Thread 2 (Jan 26): Mathematical rigour demanded
   ├── "Is it mathematically rigorous?" → No → Rebuilt properly
   ├── Expert evaluation system with Buzzard/Tao/Candès gates
   ├── Anti-tangent mathematical guards
   └── Key insight: "use only validated expert frameworks, then TEST"

Thread 3 (Jan 27-28): Data pipeline + testing designed
   ├── Data cleaning pipeline (entropy filter H > 2 → discard)
   ├── Kafka ingest at 10Gbps → taxonomy tag → rubric gate → sideline/accept
   ├── Synergy score definition (interaction effect vs null model)
   ├── "Every single thing is measured and goes through a strict gate"
   ├── "These gates do not change"
   └── Key insight: "puddings about our own techniques" — apply method to itself

Thread 4 (Mar 10-11): PUDDING applied at scale
   ├── PUDDING MIX 001: 37 concepts across 6 domains labelled
   ├── PUDDING MIX 002: 7 biological decision logics formalised
   ├── Radical Attribution Schema v1.0
   ├── Operational Protocol v1.0
   └── Key insight: "identical labels from different domains = highest signal"

Thread 5 (Mar 14): Logic types as bridging taxonomy
   ├── Novel taxonomy using types of logic as B-terms
   ├── Two-version search: one for clients, one for personal research
   ├── 5.4M words in vault, 3 databases (Qdrant, FalkorDB, SQL)
   └── Key insight: taxonomy "classifies the MECHANISM of the relationship"

Thread 6 (Mar 16-17): Build Quality + Mandatory Enforcement
   ├── Build Quality Framework: 6-stage pipeline (Decompose→Score→Research→Test→Reassemble→Attribute)
   ├── AMPS: 0-10 maturity score with 6 weighted dimensions
   ├── Gap Analysis: 10 gaps, 12 lenses, 5 taxonomy layers, atom ID format
   ├── Master Process Document: 10 Enforcer roles, daily Kaizen
   ├── Validation Methodology v1.0 → v2.0 (advisory → mandatory)
   └── Key insight: "make it mandatory and checked at every stage" — no exceptions
```

**The unified pattern**: Every thread is building toward the same thing — a deterministic, mathematically testable system where knowledge enters, gets labelled objectively, gets scored against rubrics, gets tested, and either ships, gets researched further, or gets rejected. The PUDDING taxonomy is the classification backbone. The rubrics are the quality gates. Kaizen is the improvement loop. **Validation is mandatory at every stage transition. The whole thing must be reproducible or it's worthless.**

---

## 10. WHAT TO DO NOW (Test Sequence — All Steps Mandatory)

### Immediate (Today)

1. **Write the codebook** — ALL 28 codes (7 WHAT + 7 HOW + 7 SCALE + 7 TIME), each with definition, decision rule, boundary, examples, not-examples, common confusions, decision tree
   - **MANDATORY**: No labeling begins without this. No exceptions.

2. **Pick 5 test atoms** — select them from different domains

3. **Run Phase 1 pilot** — you + 2 AI models (Claude + Grok or GPT) independently label the 5 atoms
   - **MANDATORY**: Calculate α per facet
   - **MANDATORY**: If any α < 0.667 → HALT. Fix codebook. Re-run.

### This Week

4. **If all facets α ≥ 0.70**: Proceed to Phase 2 (20 atoms, full test)
   - **MANDATORY**: Phase 1 must pass before Phase 2 begins

5. **If any facet α < 0.70**: Refine codebook. Add decision trees. Re-test.
   - **MANDATORY**: Document what was changed and why

### Next Week

6. **Phase 2**: Full test — 20 atoms, all 4 facets, 3+ raters
   - **MANDATORY**: All facets α ≥ 0.70 before production deployment

7. **Phase 3**: Noise injection test
   - **MANDATORY**: Detection rate ≥ 70% before system goes live

8. **Phase 4**: Cross-domain match validation
   - **MANDATORY**: ≥ 70% precision before recipes can ship

### Then (Ongoing — Forever)

9. **Deploy mandatory gate enforcement** — validation script runs at every stage transition
   - **MANDATORY**: No manual override. Mathematics decides.

10. **Continuous monitoring** — running α checked, codebook audited, disagreements adjudicated
    - **MANDATORY**: System halt protocol if α drops

11. **Quarterly external audit** — 20 random atoms independently re-labeled
    - **MANDATORY**: Results documented and published

12. **Rename everything** to use atom ID format: `AMP-{APQC#}-{SEQ}-{VERSION}`
    - **MANDATORY**: Old format labels are invalid after migration

13. **All chunks** labelled with PUDDING 2026 + 5 taxonomy layers
    - **MANDATORY**: Unlabelled chunks cannot be referenced

14. **Publish methodology open source**

---

## 11. EXISTING PROGRAMS WE CAN USE OR ADAPT

| Tool / Method | What it does | How to use it | Link | Mandatory? |
|---------------|-------------|---------------|------|------------|
| **Krippendorff's Alpha (Python)** | Calculates inter-rater reliability | `pip install krippendorff` → run on rater data | [PyPI](https://pypi.org/project/krippendorff/) | **YES — core enforcement engine** |
| **Label Studio** | Annotation platform with taxonomy support | Self-host on Beast, define PUDDING as taxonomy | [labelstud.io](https://labelstud.io) | Recommended but not mandatory |
| **RaTE** | Automated taxonomy evaluation using LLMs | Fine-tune BERT on vault corpus → score parent-child relations | [Paper](https://aclanthology.org/2023.iwcs-1.18.pdf) | For Phase 3 adversarial testing |
| **SKOS** | W3C standard for knowledge organization | Map PUDDING labels to SKOS concepts for interoperability | [W3C SKOS](https://www.w3.org/2004/02/skos/) | For open-source publication |
| **INCEpTION** | Semantic annotation platform with reliability metrics | Open source, Apache-2, runs annotation workflows | [INCEpTION](https://inception-project.github.io/) | Alternative to Label Studio |
| **Brown et al. Protocol** | Iterative taxonomy testing protocol | Follow their 2-round experimental design | [F1000Research](https://f1000research.com/articles/9-8) | **YES — our test design is based on this** |
| **Content Analysis Codebook** | Template for creating reproducible coding instructions | Follow Insight7 guide for structure | [Insight7](https://insight7.io/how-to-create-a-codebook-for-content-analysis/) | **YES — codebook structure** |

---

## 12. SUMMARY: THE MANDATORY ENFORCEMENT MATRIX

Every row in this matrix is a hard gate. Not a suggestion. Not a best practice. A gate.

| Stage | Gate | Check | Benchmark Used | Threshold | If Fail |
|-------|------|-------|---------------|-----------|--------|
| **INGEST** | G1: Structure | Atom ID + attribution + raw text | Schema validation + 3-Gate Metric | All present | Reject at ingest |
| **LABEL** | G2: Label + Layers | All 4 facets valid + 5 layers + 3-7 dims + codebook path | Label regex + layer completeness + Error Registry E1-E4 | All valid | Return to labeler |
| **LABEL** | G2b: Inter-Rater | Sampled dual-labeling → α calculated | Krippendorff's α per facet | α ≥ 0.667 | **SYSTEM HALT** |
| **SCORE** | G3: Rubric & Benchmark | RAEI scored + PRS calculated + believability + 3 lenses min + label consistency | RAEI (≥12/20), PRS (≥5.0), Believability, 3-Gate Metric, Error Registry E5 | All pass | Flag for adjudication |
| **MATCH** | G4: Match Quality | Triple search + failure patterns + cross-domain + neutral labels | Jaccard ≥0.75, both RAEI ≥12, SYNERGY calc'd, Believability, Error Registry E6/E8 | All pass | Match discarded |
| **MIX** | G5: Recipe + Scoring | A≠C domain + neutral B + 1+1=3 + testable + scored | MASHUP ≥60/100, Simple ≥5, Cross-domain ≥13, Error Registry E7 | All pass | Recipe rejected |
| **TEST** | G6: Test + INTENTLOGIC | Pre-registered + sufficient power + logged + scored | INTENTLOGIC ≥10 (internal) / ≥28 (client), PRS recalculated, Error Registry E7 | All pass | Test invalid |
| **SHIP** | G7: Final Boss | ALL prior gates + full attribution + canonical ID + all layers | α ≥0.80, PRS ≥7.0, RAEI ≥12, Tier ≥ SILVER, INTENTLOGIC ≥10, MASHUP ≥60 (recipe), AMPS | All pass | Returns to earliest failing gate |
| **ONGOING** | Codebook Audit | Review every 50 atoms or any α warning | Error Registry E3/E11 | Completed | Labeling paused |
| **ONGOING** | Score Distribution | Mean RAEI per batch, PRS distribution | Error Registry E5 (inflation), E10 (gaming) | Mean ≤ 3.5 | Scoring review triggered |
| **ONGOING** | Quarterly Audit | 20 random atoms re-labeled externally | Krippendorff α + full Error Registry scan | α maintained + no new patterns | Investigation + codebook review |
| **ONGOING** | Kaizen Daily | AMPS recalculated, degradation flagged | AMPS composite, symbiotic feedback loops (Section 1.4) | No degradation | Improvement cycle triggered |

### The Symbiotic Check (Every Gate)

At every gate, the enforcer also verifies:

1. **Cross-reference integrity** — Does the rubric score at this gate align with scores from connected rubrics? (Section 1.4 feedback loops)
2. **Error pattern scan** — Does this atom exhibit any of the 12 known error patterns? (Section 1.5 registry)
3. **Metric validity** — Do all metrics used at this gate pass the 3-Gate Formula? (Buzzard/Tao/Candès)
4. **Attribution continuity** — Is the full chain of who-did-what traceable from ingest to this gate?

**Nothing is exempt. Nothing gets a waiver. The rubrics talk to each other. The errors are researched and stored. Mathematics decides.**

---

## Attribution

```
Human: Ewan Bramley (originator — PUDDING 2026 taxonomy, directive for mandatory enforcement at every stage, all architectural decisions)
AI: Perplexity AI (researcher — found established methodologies, synthesised comparison, designed mandatory gate protocol)
Theoretical Foundation: Don R. Swanson (1986) — Literature-Based Discovery ABC Model
Methodology Sources:
  - Klaus Krippendorff (2004) — Content Analysis methodology, Alpha statistic
  - S.R. Ranganathan (1933) — Faceted Classification, PMEST
  - Brown et al. (2020) — Inter-rater reliability iterative protocol (F1000Research)
  - Gao & Langlais (2023) — RaTE automated taxonomy evaluation
  - Robert J. Glushko (2020) — Faceted Classification design principles
Fact %: 85 | Confidence: High | PUDDING: C.>.5.p
LBD: Swanson (1986) ABC Model
```

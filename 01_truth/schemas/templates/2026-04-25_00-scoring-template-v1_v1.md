---
title: "SCORING TEMPLATE"
id: "00-scoring-template-v1"
version: 1
created: "2026-04-25"
type: "document"
topic_type: "template"
audience: "internal"
layer: "truth"
status: "filed"
signed_by: "Devon, 2026-04-25, devin-992682c244cf444f91e0a516498afbfd"
---

# SCORING TEMPLATE
## Attribution-First Content Scoring
## Version 1.0 — 20 January 2026

**Use this template for every piece of content entering the knowledge base.**

---

## QUICK REFERENCE: THE MULTIPLIER STACK

```
Layer 5: SYNTHESIS      → Creates new IP
         × multiplied by
Layer 4: SEMANTIC TAGS  → Enables discovery
         × multiplied by
Layer 3: DECISION LOGIC → Enables automation
         × multiplied by
Layer 2: EXPERT SOURCE  → Enables citation
         × multiplied by
Layer 1: ATTRIBUTION    → Enables trust (FOUNDATION)
```

---

## THE SCORING TEMPLATE

Copy this YAML frontmatter for every document:

```yaml
---
# IDENTITY
id: [uuid or filename slug]
title: [descriptive title, max 10 words]
type: [principle|framework|sop|template|prompt|insight|reference|recipe]

# LAYER 1: ATTRIBUTION (Foundation — zeros here = cannot proceed)
source: [who/what provided this — name, document, system]
source_score: [0-3]  # 0=unknown, 1=inferred, 2=stated, 3=verified+linked
source_link: [URL or file path to original, if available]

date: [when this was created/captured — ISO format preferred]
date_score: [0-3]  # 0=unknown, 1=approximate, 2=dated, 3=timestamped

method: [how was this gathered — interview, observation, extraction, inference]
method_score: [0-3]  # 0=unknown, 1=stated, 2=documented, 3=systematic

attribution_multiplier: [source_score × date_score × method_score]  # max 27

# LAYER 2: EXPERT SOURCE (Authority)
experts:
  - [DALIO|GERBER|GODIN|KENNEDY|LUND|ZIGLAR|CIALDINI|BRAMLEY|CLAUDE|CLIENT]
expert_count: [number of experts tagged]
is_synthesis: [true|false]  # true if novel combination creates new insight
authority_score: [0-3]  # 0=orphan, 1=single, 2=multiple, 3=synthesis

# LAYER 3: DECISION LOGIC (Automation)
has_logic: [true|false]
logic_presence: [0-3]  # 0=none, 1=implicit, 2=stated, 3=structured
logic_completeness: [0-3]  # 0=none, 1=minimal, 2=partial, 3=complete
logic_multiplier: [logic_presence × logic_completeness]  # max 9

# Decision logic (if has_logic = true)
triggers: []
conditions: []
actions: []
outcomes: []
fallbacks: []

# LAYER 4: SEMANTIC TAGS (Discovery)
business_dimensions:
  - [customer_acquisition|customer_retention|pricing|systems|people|sales|service_delivery|finance|mindset|communication|measurement|trust]
mechanism_dimensions:
  - [cause_effect|trade_off|amplifier|constraint|sequence|threshold|feedback_loop]
tag_count: [total unique tags]
tag_density: [0-3]  # 0=untagged, 1=sparse(1-2), 2=tagged(3-4), 3=rich(5+)

# LAYER 5: SYNTHESIS (Validation)
status: [hypothesis|tested_internal|tested_client|proven|canonical]
validation_score: [0-4]
evidence: [what supports this status — test results, client outcomes, expert citation]

# MASTER MULTIPLIER
multiplier_raw: [attribution × authority × logic × tags × validation]
multiplier_tier: [gold|silver|bronze|raw|void]

# TIMESTAMPS
created: [ISO date]
scored: [ISO date]
last_validated: [ISO date]

# PUDDING POTENTIAL (for LBD matching)
discovery_potential: [calculated by pudding_mixer.py]
related_pieces: []
recipe_candidates: []
---
```

---

## SCORING GUIDE

### Layer 1: Attribution (Score each 0-3)

**SOURCE:**
| Score | Meaning | Example |
|-------|---------|---------|
| 3 | Verified + linked | "Ray Dalio, Principles (2017), Ch.4" with URL |
| 2 | Named in content | "Dalio says..." |
| 1 | Inferred from context | Sounds like Dalio |
| 0 | Unknown | "Someone said..." |

**DATE:**
| Score | Meaning | Example |
|-------|---------|---------|
| 3 | Exact timestamp | "2026-01-20T14:30:00Z" |
| 2 | Specific date | "15 January 2026" |
| 1 | Approximate | "Q1 2026" or "early 2026" |
| 0 | Unknown | No temporal info |

**METHOD:**
| Score | Meaning | Example |
|-------|---------|---------|
| 3 | Systematic | "Extracted via diagnostic protocol v1" |
| 2 | Documented | "45-min client interview, video recorded" |
| 1 | Stated | "Client mentioned" |
| 0 | Unknown | Just text, no context |

### Layer 2: Expert Source (Score 0-3)

| Score | Meaning |
|-------|---------|
| 3 | Synthesis — novel combination creates new insight |
| 2 | Multiple — 2+ experts agree |
| 1 | Single — one expert source |
| 0 | Orphan — no expert attribution |

### Layer 3: Decision Logic (Score each 0-3)

**PRESENCE:**
| Score | Meaning |
|-------|---------|
| 3 | Structured — YAML/JSON decision tree |
| 2 | Stated — IF-THEN in prose |
| 1 | Implicit — can be inferred |
| 0 | None — information only |

**COMPLETENESS:**
| Score | Meaning |
|-------|---------|
| 3 | Complete — trigger + condition + action + outcome + fallback |
| 2 | Partial — missing fallback or outcome |
| 1 | Minimal — just action, no conditions |
| 0 | None |

### Layer 4: Semantic Tags (Score 0-3)

| Score | Meaning |
|-------|---------|
| 3 | Rich — 5+ domain tags + 2+ mechanism tags |
| 2 | Tagged — 3-4 domain + 1 mechanism |
| 1 | Sparse — 1-2 tags |
| 0 | Untagged — cannot participate in discovery |

### Layer 5: Validation Status (Score 0-4)

| Score | Status | Meaning |
|-------|--------|---------|
| 4 | canonical | Established expert knowledge |
| 3 | proven | Multiple successful applications |
| 2 | tested_client | Validated with real SMB |
| 1 | tested_internal | Tried within covered.AI |
| 0 | hypothesis | Untested idea |

---

## TIER ASSIGNMENT

Calculate: `multiplier_raw = attribution × authority × logic × tags × validation`

| Tier | Range | Meaning | Action |
|------|-------|---------|--------|
| **GOLD** | 5000+ | Complete, proven | Deploy to production |
| **SILVER** | 1000-4999 | Strong, needs validation | Ready for testing |
| **BRONZE** | 100-999 | Partial, needs enrichment | Improve before use |
| **RAW** | 1-99 | Weak | Triage, human review |
| **VOID** | 0 | Any zero in attribution | **STOP — cannot proceed** |

---

## VOID HANDLING

If `multiplier_raw = 0` (any zero in Layer 1), the item is **VOID**.

**Options:**
1. **Re-gather** — go back to source and get proper attribution
2. **Flag for human** — park in amber queue for manual review
3. **Archive** — move to archive with clear "unattributed" label

**Never proceed with VOID content.** The system cannot trust it.

---

## EXAMPLE: SCORED CONTENT

```yaml
---
id: dk-003-price-on-value
title: Price Based on Value, Not Time
type: principle

# LAYER 1: ATTRIBUTION
source: Dan Kennedy, No BS Time Management for Entrepreneurs
source_score: 3
source_link: https://example.com/kennedy-books

date: 1996-01-01
date_score: 2

method: Book extraction, direct quote with context
method_score: 2

attribution_multiplier: 12  # 3 × 2 × 2

# LAYER 2: EXPERT SOURCE
experts:
  - KENNEDY
expert_count: 1
is_synthesis: false
authority_score: 1

# LAYER 3: DECISION LOGIC
has_logic: true
logic_presence: 2
logic_completeness: 2
logic_multiplier: 4

triggers:
  - Client asks about pricing
conditions:
  - IF pricing discussion needed
actions:
  - THEN anchor to result value, not hours
outcomes:
  - Higher perceived value, premium positioning
fallbacks:
  - IF client insists on hourly, explain value-based benefits

# LAYER 4: SEMANTIC TAGS
business_dimensions:
  - pricing
  - communication
  - trust
  - sales
mechanism_dimensions:
  - cause_effect
  - amplifier
tag_count: 6
tag_density: 3

# LAYER 5: SYNTHESIS
status: canonical
validation_score: 4
evidence: Kennedy's published work, widely validated

# MASTER MULTIPLIER
multiplier_raw: 576  # 12 × 1 × 4 × 3 × 4
multiplier_tier: bronze  # needs more experts or synthesis to reach silver

created: 2026-01-20
scored: 2026-01-20
last_validated: 2026-01-20

discovery_potential: null
related_pieces: []
recipe_candidates: []
---

## Core Idea

Charge for outcomes, not hours. The value of what you deliver has nothing to do with how long it took.

## Decision Logic

- IF pricing discussion → anchor to result value
- IF client asks "how much per hour" → reframe to "what's this worth to you"
- NEVER compete on hourly rate — you lose before you start
```

---

## PUDDING RECIPE SCORING (For Synthesis Items)

When two pieces combine to create new insight:

```yaml
---
id: recipe-kennedy-lund-graceful-deadlines
title: Graceful Deadlines (Kennedy × Lund)
type: recipe

# Same attribution structure as above, but:

experts:
  - KENNEDY
  - LUND
expert_count: 2
is_synthesis: true
authority_score: 3  # SYNTHESIS!

# Pudding-specific fields
parent_pieces:
  - dk-002-honest-urgency
  - pl-003-delight-details
shared_dimensions:
  - trust
  - communication
unique_a:  # Kennedy
  - urgency
  - pricing
unique_b:  # Lund
  - happiness
  - customer_retention
pudding_score: 9  # (2 shared × 2) + 2 unique_a + 3 unique_b

status: hypothesis  # Until tested
validation_score: 0

# The actual hypothesis
hypothesis: Deadlines delivered with genuine care convert better than aggressive urgency.
test_plan: A/B test email sequences with urgency-only vs urgency-with-courtesy framing.
---
```

---

## AUTOMATION RULES

**Agents can act autonomously when:**
- `attribution_multiplier >= 12` (no zeros, mostly 2s+)
- `authority_score >= 2` (multiple experts or synthesis)
- `logic_multiplier >= 4` (has actionable logic)
- `validation_score >= 3` (proven or canonical)

**Agents must flag for human when:**
- Any score = 0
- `multiplier_tier = raw or void`
- `status = hypothesis`

---

*Template: `00-scoring-template-v1.md`*
*Location: `~/vault/_staging/`*
*Attribution: Ewan Bramley + Claude AI, 20 January 2026*

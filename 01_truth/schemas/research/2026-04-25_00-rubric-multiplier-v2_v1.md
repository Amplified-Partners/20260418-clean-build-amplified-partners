---
title: "ATTRIBUTION-FIRST RUBRIC SYSTEM"
id: "00-rubric-multiplier-v2"
version: 1
created: "2026-04-25"
type: "document"
topic_type: "framework"
audience: "internal"
layer: "truth"
status: "filed"
signed_by: "Devon, 2026-04-25, devin-992682c244cf444f91e0a516498afbfd"
---

# ATTRIBUTION-FIRST RUBRIC SYSTEM
## Rubrics That Multiply Opportunity
## Version 2.0 — 20 January 2026

**Purpose:** Not filtering. MULTIPLYING. Every attribution enables exponentially more capability.

**Attribution:** Ewan Bramley + Claude AI
**Foundation:** Swanson LBD (1986), The Law (covered.AI)

---

# THE CORE INSIGHT

**Attribution is not metadata. Attribution is the multiplier.**

| Without Attribution | With Attribution |
|---------------------|------------------|
| Data | Asset |
| Noise | Signal |
| Risk | Trust |
| Manual | Automated |
| Isolated | Connected |
| Opinion | Authority |
| Guess | Proof |

**Every rubric dimension must serve one purpose: enable the technology to do MORE.**

---

# PART 1: THE MULTIPLICATION STACK

Each layer multiplies what the layer below can do.

```
LAYER 5: SYNTHESIS        → Creates new IP (puddings)
         ↑ multiplied by
LAYER 4: SEMANTIC TAGS    → Enables discovery, clustering
         ↑ multiplied by
LAYER 3: DECISION LOGIC   → Enables automation
         ↑ multiplied by  
LAYER 2: EXPERT SOURCE    → Enables citation, authority
         ↑ multiplied by
LAYER 1: ATTRIBUTION      → Enables trust (everything else fails without this)
```

**A zero at any layer zeros everything above it.**

---

# PART 2: LAYER 1 — ATTRIBUTION (The Foundation)

## 2.1 The Three Attribution Questions

Every piece of data must answer:

| Question | Field | Why It Matters |
|----------|-------|----------------|
| **WHO** said this? | `source` | Trust, citation, authority |
| **WHEN** was it true? | `date` | Freshness, evolution, context |
| **HOW** was it gathered? | `method` | Weight, replicability, bias |

## 2.2 Source Attribution Scores

| Score | Level | Definition | Technology Enabled |
|-------|-------|------------|-------------------|
| **3** | Verified | Original source linked, confirmed | Full automation, full citation, export to clients |
| **2** | Stated | Source named in content | Automation with caveats, internal citation |
| **1** | Inferred | Source guessed from context | Human review required, flag for verification |
| **0** | Unknown | No traceable origin | CANNOT USE IN AUTOMATION |

**Examples:**
- Score 3: "Ray Dalio, Principles (2017), Chapter 4" with link to source
- Score 2: "Dalio says..." (named but not linked)
- Score 1: Content sounds like Dalio but not stated
- Score 0: "Someone once said..."

## 2.3 Temporal Attribution Scores

| Score | Level | Definition | Technology Enabled |
|-------|-------|------------|-------------------|
| **3** | Timestamped | Exact date, ideally datetime | Full temporal reasoning, version tracking |
| **2** | Dated | Specific date (e.g., "15 Jan 2026") | Can track evolution, filter by period |
| **1** | Approximate | Year or quarter known | Can filter by era |
| **0** | Unknown | No temporal information | Cannot assess freshness |

**Special rule:** Evergreen principles (Dalio, Ziglar, etc.) score 3 by nature — their truth is timeless.

## 2.4 Method Attribution Scores

| Score | Level | Definition | Technology Enabled |
|-------|-------|------------|-------------------|
| **3** | Systematic | Follows documented methodology | Can automate collection, full replicability |
| **2** | Documented | Method + conditions recorded | Can replicate manually |
| **1** | Stated | Method named (interview, observation) | Can categorize |
| **0** | Unknown | How was this gathered? | Cannot weight appropriately |

**Examples:**
- Score 3: "Extracted via covered.AI diagnostic protocol v1"
- Score 2: "From client interview, 45 mins, video recorded"
- Score 1: "Client mentioned in conversation"
- Score 0: Just text, no context

## 2.5 Attribution Multiplier

```
ATTRIBUTION_SCORE = Source × Date × Method
```

| Score | Range | Meaning | Technology Permission |
|-------|-------|---------|----------------------|
| **27** | 3×3×3 | Perfect attribution | Full automation, client-facing, canonical |
| **18-26** | Mixed high | Strong attribution | Automation with human spot-check |
| **8-17** | Mixed medium | Partial attribution | Human review before use |
| **1-7** | Low | Weak attribution | Triage only, flag for re-gathering |
| **0** | Any zero | FATAL | **Cannot proceed** — attribution required |

---

# PART 3: LAYER 2 — EXPERT SOURCE (The Authority Layer)

## 3.1 The Expert Roster

| ID | Expert | Domain | Citation Format |
|----|--------|--------|-----------------|
| `DALIO` | Ray Dalio | Systems, Decisions, Transparency | Principles (2017) |
| `GERBER` | Michael Gerber | Operations, Scaling, SOPs | E-Myth Revisited (1995) |
| `GODIN` | Seth Godin | Marketing, Tribes, Permission | Permission Marketing (1999) |
| `KENNEDY` | Dan Kennedy | Direct Response, Urgency | No BS Marketing (series) |
| `LUND` | Paddi Lund | Happiness, Client Experience | Building the Happiness-Centred Business (2004) |
| `ZIGLAR` | Zig Ziglar | Sales, Attitude, Service | See You at the Top (1975) |
| `CIALDINI` | Robert Cialdini | Influence, Persuasion | Influence (1984) |
| `BRAMLEY` | Ewan Bramley | Original synthesis | covered.AI methodology |
| `CLAUDE` | Claude AI | AI-generated | Requires validation |
| `CLIENT` | Client-sourced | Their business | Context-specific |

## 3.2 Authority Score

| Score | Level | Definition | Technology Enabled |
|-------|-------|------------|-------------------|
| **3** | Synthesis | Novel combination of 2+ experts | **Creates new IP** (this is the pudding!) |
| **2** | Multiple | 2+ experts agree on same point | Strong authority, cross-validation |
| **1** | Single | One expert source | Can cite one authority |
| **0** | Orphan | No expert attribution | Low trust, limited use |

**The goal is Score 3.** That's where covered.AI creates unique value nobody else has.

## 3.3 Expert Multiplier

```
EXPERT_SCORE = number_of_experts × synthesis_bonus
```

Where:
- `number_of_experts` = count of tagged experts (1-n)
- `synthesis_bonus` = 2 if combination creates novel insight, else 1

---

# PART 4: LAYER 3 — DECISION LOGIC (The Automation Layer)

## 4.1 The Logic Format

Every automatable piece should contain:

```yaml
trigger: [situation that activates this]
condition: [IF this is true]
action: [THEN do this]
outcome: [expected result]
fallback: [IF action fails, do this]
```

## 4.2 Logic Presence Score

| Score | Level | Definition | Technology Enabled |
|-------|-------|------------|-------------------|
| **3** | Structured | YAML/JSON decision tree | Direct agent execution |
| **2** | Stated | IF-THEN logic written in prose | Can be extracted and coded |
| **1** | Implicit | Logic can be inferred from content | Human interpretation needed |
| **0** | None | No actionable logic | Information only, not automatable |

## 4.3 Logic Completeness Score

| Score | Level | Definition |
|-------|-------|------------|
| **3** | Complete | Trigger + Condition + Action + Outcome + Fallback |
| **2** | Partial | Missing fallback or outcome |
| **1** | Minimal | Just action, no conditions |
| **0** | None | No decision logic present |

## 4.4 Logic Multiplier

```
LOGIC_SCORE = Presence × Completeness
```

| Score | Range | Technology Permission |
|-------|-------|----------------------|
| **9** | 3×3 | Full agent automation |
| **4-8** | Medium | Semi-automated with human trigger |
| **1-3** | Low | Human-driven with AI assist |
| **0** | None | Cannot automate |

---

# PART 5: LAYER 4 — SEMANTIC TAGS (The Discovery Layer)

## 5.1 Business Domain Tags

| Tag | Description | Example Triggers |
|-----|-------------|------------------|
| `customer_acquisition` | Getting new customers | marketing, leads, outreach |
| `customer_retention` | Keeping customers | loyalty, churn, lifetime value |
| `pricing` | Value exchange | margins, fees, offers |
| `systems` | Repeatable processes | automation, SOPs, workflows |
| `people` | Team, culture | hiring, delegation, training |
| `sales` | Converting leads | closing, pipeline, objections |
| `service_delivery` | Fulfilling promises | quality, experience |
| `finance` | Money management | cash flow, profit |
| `mindset` | Psychology, beliefs | attitude, confidence |
| `communication` | Messaging | copy, clarity, persuasion |
| `measurement` | Tracking | metrics, KPIs |
| `trust` | Credibility | honesty, reputation |

## 5.2 Mechanism Tags

| Tag | Description |
|-----|-------------|
| `cause_effect` | A leads to B |
| `trade_off` | Gain X, lose Y |
| `amplifier` | Small input, large output |
| `constraint` | Bottleneck, limiting factor |
| `sequence` | Order matters |
| `threshold` | Tipping point |
| `feedback_loop` | Output becomes input |

## 5.3 Tag Density Score

| Score | Level | Definition | Technology Enabled |
|-------|-------|------------|-------------------|
| **3** | Rich | 5+ domain tags + 2+ mechanism tags | Maximum discovery potential |
| **2** | Tagged | 3-4 domain tags + 1 mechanism tag | Good clustering |
| **1** | Sparse | 1-2 tags | Limited matching |
| **0** | Untagged | No semantic dimensions | **Cannot participate in LBD** |

## 5.4 Swanson Discovery Score

```
DISCOVERY_POTENTIAL = (Shared_Tags × 2) + Unique_Tags_A + Unique_Tags_B
```

This is the pudding formula. High scores = high synthesis potential.

---

# PART 6: LAYER 5 — SYNTHESIS (The IP Layer)

## 6.1 Validation Status

| Score | Status | Definition | Technology Permission |
|-------|--------|------------|----------------------|
| **4** | `canonical` | Established expert knowledge | Maximum authority, export anywhere |
| **3** | `proven` | Multiple successful applications | Full trust, automation |
| **2** | `tested_client` | Validated with real SMB | Growing confidence |
| **1** | `tested_internal` | Tried within covered.AI | Limited confidence |
| **0** | `hypothesis` | Untested idea | **Cannot use in automation** |

## 6.2 Pudding Classification

| Type | Definition | Value |
|------|------------|-------|
| **Recipe** | Two experts combined, hypothesis generated | New IP created |
| **Validated Recipe** | Recipe tested and proven | Unique competitive advantage |
| **Canonical Recipe** | Recipe becomes part of methodology | Moat |

---

# PART 7: THE MASTER MULTIPLIER FORMULA

## 7.1 The Calculation

```
MULTIPLIER = Attribution × Expert × Logic × Discovery × Validation
           = (Source × Date × Method) × Expert × (Presence × Completeness) × Tags × Status
```

**Maximum possible:** 3 × 3 × 3 × 3 × 3 × 3 × 3 × 3 × 4 = **26,244**

## 7.2 Practical Tiers

| Tier | Score Range | Meaning | Action |
|------|-------------|---------|--------|
| **GOLD** | 5000+ | Fully attributed, expert-backed, automatable, rich tags, proven | Deploy to production |
| **SILVER** | 1000-4999 | Strong attribution, good logic, needs more tags or validation | Ready for testing |
| **BRONZE** | 100-999 | Partial attribution, some logic, sparse tags | Needs enrichment |
| **RAW** | 1-99 | Weak across dimensions | Triage, human review |
| **VOID** | 0 | Any zero in attribution | **Cannot proceed** |

## 7.3 Why Multiplication, Not Addition

**Addition:** 3 + 3 + 3 + 3 + 4 = 16 (linear, tolerates weakness)

**Multiplication:** 3 × 3 × 3 × 3 × 4 = 324 (exponential, demands completeness)

**A zero anywhere zeros everything.**

This forces completeness. Partial data has partial value. Complete data has exponential value.

---

# PART 8: THE OPPORTUNITY MULTIPLIER

## 8.1 What Attribution Enables

| Attribution Level | Technology Opportunity |
|-------------------|------------------------|
| Score 0 | Manual review only |
| Score 1 | AI-assisted triage |
| Score 2 | Internal automation |
| Score 3 | Client-facing automation |
| Score 27 (3×3×3) | Full autonomous agent |

## 8.2 What Expert Sourcing Enables

| Expert Level | Business Opportunity |
|--------------|---------------------|
| Score 0 | Cannot cite, low trust |
| Score 1 | Single authority citation |
| Score 2 | "Dalio AND Gerber agree..." |
| Score 3 | **Novel IP**: "Our synthesis of Dalio + Gerber reveals..." |

## 8.3 What Semantic Tags Enable

| Tag Density | Discovery Opportunity |
|-------------|----------------------|
| Score 0 | Isolated data, no connections |
| Score 1 | Limited matches |
| Score 2 | Clusters form |
| Score 3 | **Pudding recipes emerge**: Qdrant finds combinations humans wouldn't |

## 8.4 What Decision Logic Enables

| Logic Level | Automation Opportunity |
|-------------|------------------------|
| Score 0 | Information only |
| Score 1 | Human-driven, AI-assisted |
| Score 2 | Semi-automated workflows |
| Score 9 (3×3) | **Full autonomous agent**: AI handles end-to-end |

## 8.5 What Validation Enables

| Validation Level | Confidence Opportunity |
|------------------|------------------------|
| Score 0 | Hypothesis only |
| Score 1-2 | Internal use |
| Score 3 | Client-ready |
| Score 4 | **Canonical**: Part of the covered.AI methodology |

---

# PART 9: THE COMPOUNDING FLYWHEEL

```
Week 1: Score 100 pieces
        → 20 Gold (full attribution, rich tags)
        → 50 Silver (need enrichment)
        → 30 Bronze/Raw (need work)

Week 2: Gold pieces enable first automations
        Testing validates some Silver → Gold
        Pudding mixer finds 5 novel recipes
        Each recipe = NEW attributed content

Month 1: 50 Gold pieces
         10 validated pudding recipes
         Agent handles 30% of queries

Month 6: 200 Gold pieces
         50 validated recipes
         Agent handles 60% of queries
         Every client engagement generates MORE data

Year 1:  1000+ Gold pieces
         200+ validated recipes
         Agent handles 80% of queries
         **The system teaches itself**
```

---

# PART 10: THE SINGLE RULE

**ATTRIBUTE EVERYTHING.**

- If you can't say WHO → don't store it
- If you can't say WHEN → don't trust it
- If you can't say HOW → don't automate it

**Attribution is not overhead. Attribution is the multiplier.**

**The technology can only do what the data permits.**

**Attribute. Attribute. Attribute.**

---

*Document: `00-rubric-multiplier-v2.md`*
*Location: `~/vault/_staging/`*
*Attribution: Ewan Bramley + Claude AI, 20 January 2026*
*Foundation: Swanson LBD (1986), The Law (covered.AI)*
*Methodology: Attribution-first rubric design*

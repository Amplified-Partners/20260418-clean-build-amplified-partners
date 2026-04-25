---
title: "Curator Taxonomy Recall Test"
id: "curator-taxonomy-recall-test"
version: 1
created: 2026-04-25
last_validated: 2026-04-25
type: document
topic_type: reference
status: imported
source_file: "curator-taxonomy-recall-test.md"
signed_by: "Devon, 2026-04-25, devin-992682c244cf444f91e0a516498afbfd"
---

# Curator Taxonomy Recall Test Framework
## "Does the short-code system actually work?"

**Version:** 1.0  
**Date:** 2026-03-17  
**Status:** Hypothesis — ready for testing  
**Attribution:** Ewan Bramley (originator, test-first principle) × Claude (Perplexity Computer, designer)

---

## What We're Testing

One thing only: **Can agents reliably store, retrieve, and resolve short taxonomy codes against a mock component library?**

We are NOT testing:
- PUDDING technique
- Quality scoring accuracy
- Cross-domain discovery
- FalkorDB performance at scale
- The Curator agent's reasoning

We ARE testing:
- Code → component resolution (can the system find what the code points to?)
- Component → code assignment (does the same component always get the same code?)
- Near-miss retrieval (can it find SIMILAR codes, not just exact matches?)
- Error rates (how often does it return wrong results, no results, or ambiguous results?)
- Speed (is short-code lookup faster than full-description search?)

---

## The Test Architecture

```
┌─────────────────────────────────────────────────┐
│                 TEST HARNESS                     │
│  Python script — runs all tests, logs results    │
├─────────────────────────────────────────────────┤
│                                                  │
│  ┌──────────────┐    ┌──────────────────────┐   │
│  │ MOCK GRAPH   │    │ LOOKUP TABLE (MD)    │   │
│  │ FalkorDB     │◄──►│ Curator's reference  │   │
│  │ 100 fake     │    │ Code schema + full   │   │
│  │ components   │    │ descriptions         │   │
│  └──────────────┘    └──────────────────────┘   │
│         ▲                      ▲                 │
│         │                      │                 │
│  ┌──────┴──────────────────────┴──────────┐     │
│  │           TEST SUITE (5 batteries)      │     │
│  │  1. Exact recall                        │     │
│  │  2. Reverse lookup                      │     │
│  │  3. Near-miss / similarity              │     │
│  │  4. Ambiguity detection                 │     │
│  │  5. Speed comparison                    │     │
│  └─────────────────────────────────────────┘     │
│                      │                           │
│  ┌───────────────────▼─────────────────────┐     │
│  │           RESULTS LOG                    │     │
│  │  Pass/Fail per test                      │     │
│  │  Error classification                    │     │
│  │  Timing data                             │     │
│  │  Verdict: proceed / redesign / abandon   │     │
│  └──────────────────────────────────────────┘    │
└─────────────────────────────────────────────────┘
```

---

## Step 1: Build the Mock Data (30 minutes)

### The Code Schema (Curator's MD file)

```markdown
# Curator Taxonomy Code Schema v1.0

## Format: {TYPE}-{DOMAIN}-{SEQ}

### TYPE prefix (3 chars)
- CMP = Component (reusable code unit)
- WFL = Workflow (multi-step process)
- AGT = Agent (agent config or prompt)
- TPL = Template (scaffolding template)
- CFG = Config (configuration file)
- QRY = Query (database query pattern)

### DOMAIN prefix (2-3 chars)
- BK  = Booking
- SC  = Scheduling
- INV = Invoicing
- ONB = Onboarding
- MKT = Marketing
- ENF = Enforcement
- AUD = Audit
- RPT = Reporting
- USR = User management
- NTF = Notification

### SEQ = 3-digit sequential number (001-999)

### Examples
- CMP-BK-001 = First booking component
- WFL-ONB-003 = Third onboarding workflow
- AGT-ENF-001 = First enforcer agent config
```

### The Mock Component Library (100 entries)

Generate 100 fake but realistic components across all TYPE and DOMAIN combinations. Each entry has:

```json
{
  "code": "CMP-BK-001",
  "name": "Appointment Slot Generator",
  "description": "Generates available booking slots based on business hours, existing appointments, and buffer time rules. Accepts timezone, duration, and blackout dates as parameters.",
  "type": "component",
  "domain": "booking",
  "score": 8.4,
  "pudding_label": "P.=.3.l",
  "tags": ["scheduling", "availability", "timezone"],
  "dependencies": ["CMP-SC-002", "CFG-BK-001"],
  "status": "active"
}
```

Source the 100 entries from REAL Amplified concepts where possible (booking, onboarding, invoicing, marketing, enforcement patterns), padded with plausible fakes. This makes the test data realistic without needing the actual codebase.

---

## Step 2: Load into FalkorDB Test Graph (15 minutes)

Create a separate test graph namespace: `curator_test` (not `amplified_brain`).

```cypher
// Create component nodes
CREATE (:Component {
  code: "CMP-BK-001",
  name: "Appointment Slot Generator",
  description: "Generates available booking slots...",
  score: 8.4,
  pudding_label: "P.=.3.l",
  status: "active"
})

// Create the lookup index
CREATE INDEX ON :Component(code)
CREATE INDEX ON :Component(name)

// Create vector index for similarity search on description embeddings
// (using FalkorDB's native HNSW)
```

---

## Step 3: Run the 5 Test Batteries

### Battery 1: Exact Recall (20 tests)

**Question:** Given a short code, can the system return the correct component?

```
Input:  "CMP-BK-001"
Expected: { name: "Appointment Slot Generator", score: 8.4, ... }

Input:  "WFL-ONB-003"
Expected: { name: "Client Welcome Sequence", score: 7.8, ... }

Input:  "XXXXXX" (nonexistent code)
Expected: { result: "NO_MATCH", suggestion: null }
```

**20 tests:** 15 valid codes (random selection from the 100), 5 invalid codes.

**Pass criteria:**
- 100% accuracy on valid codes (this MUST be perfect — it's a database lookup)
- 100% correct NO_MATCH on invalid codes
- Average response time logged

**Failure classification:**
- WRONG_COMPONENT = returned a different component (critical bug)
- NO_RESULT = returned nothing for a valid code (index issue)
- FALSE_POSITIVE = returned something for an invalid code (dangerous)

---

### Battery 2: Reverse Lookup (20 tests)

**Question:** Given a component description (natural language), can the system find the right code?

```
Input:  "I need a component that generates booking time slots"
Expected: "CMP-BK-001" (or top-3 containing CMP-BK-001)

Input:  "Something for sending notifications when appointments change"
Expected: "CMP-NTF-004" (or similar)

Input:  "A component for quantum teleportation" (nonsense)
Expected: NO_MATCH or very low confidence results
```

**20 tests:** 15 real descriptions (paraphrased, NOT copy-pasted from the data), 5 nonsense descriptions.

**Pass criteria:**
- Correct code in top-1 result: ≥80% (16/20)
- Correct code in top-3 results: ≥95% (19/20)
- Nonsense queries return NO_MATCH or confidence <0.5: 100%

**Failure classification:**
- MISSED = correct component not in top-3 (retrieval gap)
- WRONG_RANK = correct component found but not top-1 (ranking issue)
- HALLUCINATION = returned confident result for nonsense query (dangerous)

---

### Battery 3: Near-Miss / Similarity (15 tests)

**Question:** When searching for something that doesn't exist exactly, does it find the closest match?

```
Input:  "CMP-BK-001" exists. Search for "a booking widget that shows free time"
Expected: Returns CMP-BK-001 as NEAR_MATCH with similarity score

Input:  "WFL-ONB-003" exists. Search for "a workflow for welcoming new customers"
Expected: Returns WFL-ONB-003 as NEAR_MATCH

Input:  Search for "a component for managing rocket launches"
Expected: NO_MATCH (nothing in library is close)
```

**15 tests:** 10 queries that SHOULD match something, 5 that SHOULDN'T.

**Pass criteria:**
- True near-matches found: ≥80% (8/10)
- False near-matches (returning something for rocket launches): 0%
- Similarity scores are monotonic (closer descriptions = higher scores)

**Failure classification:**
- FALSE_NEAR = returned a near-match for something unrelated (threshold too low)
- MISSED_NEAR = didn't find an obvious similar component (threshold too high)
- SCORE_INVERSION = closer description got lower similarity score (embedding issue)

---

### Battery 4: Ambiguity Detection (10 tests)

**Question:** When a query could match multiple components, does the system flag the ambiguity?

```
Input:  "I need something for booking" 
Expected: Multiple results returned (CMP-BK-001, CMP-BK-002, WFL-BK-001, etc.)
         System flags: AMBIGUOUS — please be more specific

Input:  "The enforcer config"
Expected: If only one AGT-ENF exists, return it. If multiple, flag ambiguity.
```

**10 tests:** 5 deliberately vague queries, 5 queries that look vague but actually have only one match.

**Pass criteria:**
- Vague queries flagged as ambiguous: ≥80% (4/5)
- Specific queries NOT flagged as ambiguous: 100% (5/5)

**Failure classification:**
- MISSED_AMBIGUITY = returned single result for a vague query (user gets wrong component)
- FALSE_AMBIGUITY = flagged ambiguity when there's clearly one match (annoying, slows workflow)

---

### Battery 5: Speed Comparison (All 100 components)

**Question:** Is short-code lookup measurably faster than full-description search?

Run the same 20 lookups two ways:
1. **Short code path:** Query by code string → return component
2. **Full description path:** Query by full description text → vector search → return component

**Measure:**
- Average response time (ms) for short-code lookup
- Average response time (ms) for full-description search
- P95 response time for each
- Total token count consumed by each approach (for agent context window impact)

**Pass criteria:**
- Short-code lookup is ≥5x faster than full-description search
- Short-code lookup P95 < 10ms
- Token savings per lookup ≥ 50 tokens

**No failure classification needed — this is measurement, not pass/fail.**

---

## Step 4: Analyse Results

### The Scorecard

| Battery | Tests | Pass Threshold | Result | Verdict |
|---------|-------|---------------|--------|---------|
| 1. Exact Recall | 20 | 100% | ___ | ___ |
| 2. Reverse Lookup | 20 | 80% top-1, 95% top-3 | ___ | ___ |
| 3. Near-Miss | 15 | 80% true, 0% false | ___ | ___ |
| 4. Ambiguity | 10 | 80% detection, 100% no false | ___ | ___ |
| 5. Speed | 100 | 5x faster | ___ | ___ |

### Error Classification

For every failure, classify:

| Error Type | Count | Where (Battery) | Root Cause | Fix Difficulty |
|-----------|-------|-----------------|------------|---------------|
| WRONG_COMPONENT | | | | |
| NO_RESULT | | | | |
| FALSE_POSITIVE | | | | |
| MISSED | | | | |
| WRONG_RANK | | | | |
| HALLUCINATION | | | | |
| FALSE_NEAR | | | | |
| MISSED_NEAR | | | | |
| SCORE_INVERSION | | | | |
| MISSED_AMBIGUITY | | | | |
| FALSE_AMBIGUITY | | | | |

### Decision Matrix

| Outcome | Action |
|---------|--------|
| All 5 batteries pass | Proceed to build. Short-code system is validated. |
| Batteries 1-4 pass, Battery 5 marginal | Proceed. Speed benefit is nice-to-have, not critical. |
| Battery 1 fails | STOP. Exact recall must be perfect. Debug index. |
| Battery 2 fails (<60% top-1) | Redesign. Embedding model or search approach needs work. |
| Battery 3 has false near-matches | Adjust similarity threshold. Retest. |
| Battery 4 has missed ambiguity | Add ambiguity detection logic. Retest. |
| Multiple batteries fail | Abandon short-code approach OR fundamentally redesign. |

---

## Step 5: What This Tells Us

If the test passes, we know:
- Short codes work for machine-to-machine recall (agents can use them)
- The lookup table resolves correctly (Curator's MD files are sufficient)
- Near-miss detection works (prevents false "NO_MATCH" when similar things exist)
- The system knows when it's confused (ambiguity detection)
- There's a measurable speed/efficiency benefit

If the test fails, the errors tell us WHERE:
- Index errors → fix the graph schema
- Embedding errors → change the vector model or description format
- Threshold errors → tune the similarity cutoff
- Schema errors → redesign the code format before it hardens

---

## Estimated Time to Run

| Step | Time |
|------|------|
| Generate 100 mock components | 30 min |
| Write Curator MD schema file | 15 min |
| Load into FalkorDB test graph | 15 min |
| Write test harness (Python) | 45 min |
| Run all 5 batteries | 10 min |
| Analyse results | 20 min |
| **Total** | **~2.5 hours** |

This can run entirely on Beast using the existing FalkorDB instance (separate graph namespace). No production data touched. No risk to live systems.

---

## What Comes After (If It Passes)

1. Expand from 100 to 500 mock components — does it scale?
2. Add multi-agent test: two agents passing codes to each other — does communication work?
3. Add degradation test: corrupt 10% of entries — does the system detect it?
4. Add namespace collision test: generate codes that LOOK similar — does it distinguish?
5. THEN connect to real Cove pipeline for integration test

---

## Sources & Prior Art

- Taxonomy-aligned benchmark evaluation patterns: https://www.emergentmind.com/topics/taxonomy-aligned-benchmark
- BloomAPR recall testing framework (Bloom's Taxonomy for evaluation): https://arxiv.org/html/2509.25465v1
- FalkorDB compact format (internal integer ID mapping): https://docs.falkordb.com/design/client-spec.html
- GraphRAG precision/recall patterns: https://towardsdatascience.com/graphrag-in-practice-how-to-build-cost-efficient-high-recall-retrieval-systems/
- Synthetic data for retrieval evaluation: https://developers.redhat.com/articles/2026/02/23/synthetic-data-rag-evaluation-why-your-rag-system-needs-better-testing
- Common taxonomy mistakes (Earley): https://www.earley.com/insights/ten-common-mistakes-when-developing-taxonomy
- IR evaluation metrics (Google ML): https://developers.google.com/machine-learning/crash-course/classification/accuracy-precision-recall

---

**Attribution:**  
Ewan Bramley (originator — test-first principle, "every idea is a hypothesis until tested") × Claude (claude-sonnet-4-6, Perplexity Computer — framework designer, research synthesis)  
Fact %: 80 | Confidence: High | PUDDING: M.=.0.v (Meta, Stable, Scale-free, Variable)

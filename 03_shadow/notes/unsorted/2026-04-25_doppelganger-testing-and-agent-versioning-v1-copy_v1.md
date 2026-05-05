---
title: "Amplified Partners — Doppelganger Testing & Agent Versioning v1"
id: "doppelganger-testing-and-agent-versioning-v1-copy"
version: 1
created: "2026-04-25"
type: "document"
topic_type: "unsorted"
audience: "internal"
layer: "shadow"
status: "filed"
signed_by: "Devon, 2026-04-25, devin-992682c244cf444f91e0a516498afbfd"
---

# Amplified Partners — Doppelganger Testing & Agent Versioning v1

---

**Document ID:** `DOPPELGANGER-TESTING-AND-AGENT-VERSIONING-v1`
**Status:** Proposed Standard
**Applies to:** All Amplified Partners agents, their instruction sets (MDs), and the code registry
**Companion documents:** `CODE-TAXONOMY-AND-KAIZEN-v1`, `ATTRIBUTION-AND-CURATION-v1`, `VALIDATION-METHODOLOGY-v2`, `SCORING-UNIFICATION-HYPOTHESIS-v2`

---

## 0. THE PRINCIPLE

**No change to agent instructions or system codes reaches production without being tested against a doppelganger in a sandbox first. Version numbers are earned, not assigned. A version number means "this passed testing." Failed candidates never get a number.**

This is the staging environment for agent cognition. Software engineering has maintained the distinction between dev, staging, and production for decades. Code does not go live without passing CI/CD. Infrastructure does not go live without passing integration tests. Agent instructions — the documents that determine how every agent in this system thinks, decides, and acts — deserve the same discipline.

An agent's MD (its instruction set, system prompt, role definition) is source code for behaviour. Changing an MD changes how the agent processes data, applies gates, assigns codes, and writes to databases. An untested MD change is an untested deployment. We do not deploy untested code. We should not deploy untested instructions.

Mathematics decides. Not vibes. Not "I think the new prompt is better." Not "it seems to work." A version number means the mathematics confirmed it.

---

## How This Document Connects

| Document | Relationship |
|----------|-------------|
| `CODE-TAXONOMY-AND-KAIZEN-v1` | Kaizen gains a new workflow: `DoppelgangerTestWorkflow`. The Regression Sentinel (Section 3.1) becomes the post-promotion verification. The Error Anticipation Registry (Section 1) captures doppelganger test failures as a new error category. |
| `ATTRIBUTION-AND-CURATION-v1` | Curator audit logs (Section 2.4) gain the `md_version` stamp. The code registry (Section 3.5) gains versioning as a first-class property. The codebook becomes a versioned artefact managed by `curator-config`. |
| `VALIDATION-METHODOLOGY-v2` | The 7 gates (G1–G7, Section 4.2) serve as the primary pass/fail criteria for doppelganger tests. Gate pass rates from the enforcement matrix (Section 12) are the core comparison metric. |
| `SCORING-UNIFICATION-HYPOTHESIS-v2` | MD version becomes a new dimension in the scoring layer. The scoring layer (Section 1.5) can measure which instruction versions produce the best outcomes. Doppelganger test results feed the meta-scoring cascade (Section 2). |

---

## SECTION 1: AGENT MD VERSIONING

---

### 1.1 What an Agent MD Is

An agent MD is the instruction set that defines how an agent behaves. It includes the system prompt, role definition, configuration parameters, operational constraints, and any domain-specific rules. Every agent in the Amplified system has one. The five Curators (`curator-kg`, `curator-vec`, `curator-doc`, `curator-state`, `curator-config`) each have MDs. The Kaizen Agent has one. The Chaos Agent has one. Pipeline agents have them. Every agent that operates within the system has a document — or set of documents — that governs its behaviour.

An MD is not documentation. It is executable specification. When you change the words in an MD, you change the behaviour of the agent. When you change how the agent behaves, you change the data it produces, the gates it enforces, the codes it assigns, and the audit trail it generates. The MD is the root cause of agent behaviour, and root causes deserve version control.

---

### 1.2 Why Version Them

**Traceability.** When something goes wrong — a Curator assigns incorrect codes, a pipeline agent produces malformed output, a Kaizen cycle fails to detect a regression — the first question is: what changed? If agent MDs are versioned and the version is stamped on every operation, you can correlate behaviour changes with instruction changes. Without versioning, you are debugging in the dark.

**Rollback.** If a new MD version causes degradation, you need to revert to the previous version. Without version numbers, "previous version" is undefined. With version numbers, rollback is mechanical: set `md_version` back to V(n-1) and redeploy.

**Kaizen integration.** The Kaizen Department (`CODE-TAXONOMY-AND-KAIZEN-v1`, Section 3) runs continuous improvement cycles. MD versioning gives Kaizen a new data source: the correlation between MD version changes and system metric changes. If gate pass rates drop after an MD change, Kaizen can flag it. If code assignment quality improves after an MD change, Kaizen can confirm it. Without version stamps, these correlations are invisible.

**Scoring layer integration.** If the Scoring Unification Hypothesis (`SCORING-UNIFICATION-HYPOTHESIS-v2`) is validated, MD version becomes another countable signal. You can literally score your own prompt engineering: which version of curator-kg's instructions produces the highest gate pass rates? Which version produces the best co-occurrence patterns? The scoring layer can answer these questions — but only if the version is recorded.

---

### 1.3 Version Numbering Convention

Version numbers are earned, not assigned. Only tested, promoted versions receive a number.

| Label | Meaning | Example |
|-------|---------|---------|
| `V{N}` | Production version. Passed doppelganger testing. | `V1`, `V2`, `V3` |
| `V{N}-candidate-{x}` | Test candidate targeting version N. May or may not pass. | `V3-candidate-a`, `V3-candidate-b` |
| Latest `V{N}` | The current production version is always the highest numbered version. | If V3 exists, V3 is production. |

**Rules:**

- Version numbers are sequential integers. No decimals. No semantic versioning. V1, V2, V3. The simplicity is intentional — there are no "minor" changes to agent instructions. Every change is a behavioural change.
- Failed candidates are labelled with their target version and a candidate suffix. `V3-candidate-a` is the first attempt at V3. If it fails, `V3-candidate-b` is the second attempt. Failed candidates are retained in the version history for audit purposes but are never deployed.
- The version history is maintained in the config store (`curator-config`). Each entry records: version label, promotion date (or rejection date), test results summary, and the MD content hash.
- Version numbers never reset. If an agent has reached V7 and a complete rewrite is needed, the rewrite becomes V8, not V1. History is linear.

---

### 1.4 What Gets Versioned

Not just agent system prompts. The versioning regime applies to any artefact that, when changed, changes system behaviour:

| Artefact | Managed By | Versioned In | Why |
|----------|-----------|-------------|-----|
| Agent system prompts / MDs | Each agent's deployment config | `curator-config` | Determines agent behaviour — the primary use case |
| Curator codebooks (the code registry) | `curator-kg` (`ATTRIBUTION-AND-CURATION-v1`, Section 3.5) | `curator-config` | Determines how labels map to codes. A codebook change is a taxonomy change. |
| Lens configurations | Scoring layer (if validated) | `curator-config` | Determines how gates are weighted per context (`SCORING-UNIFICATION-HYPOTHESIS-v2`, Section 3) |
| Gate criteria weightings | Validation system | `curator-config` | Determines pass/fail thresholds. Only relevant if lens-adaptive evaluation is implemented. |

The codebook deserves special attention. The code registry (`ATTRIBUTION-AND-CURATION-v1`, Section 3.5) maps every compressed code to its full label, synonyms, provenance, and lifecycle status. A codebook version change could mean: a new code was added, a code was deprecated, a synonym was added, or a hierarchy was restructured. Each of these changes affects every downstream operation that touches codes. The codebook is versioned alongside the Curator's MD because the two are coupled — the Curator's behaviour and the codebook's content are co-dependent.

---

### 1.5 The Audit Stamp

Every operation logged by a Curator includes the agent ID **and** the MD version:

```yaml
audit_entry:
  timestamp: "2026-03-17T15:48:02Z"
  agent: "curator-kg"
  md_version: "v3"
  operation: "create_node"
  outcome: "success"
  gate_results:
    G1: "pass"
    G2: "pass"
    G3: "pass"
  codes_assigned: ["TEC-INFR-001", "OPS-PIPE-003"]
  node_id: "node-2026-03-17-abc123"
```

This costs almost nothing. One additional string field per log entry. But it makes the provenance chain substantially richer. When Kaizen analyses gate pass rates over time, it can partition by MD version. When the scoring layer computes code assignment patterns, it can identify version-correlated shifts. When a regression is detected, the version stamp points directly at the instruction change that caused it.

The stamp applies to all five Curators (`curator-kg`, `curator-vec`, `curator-doc`, `curator-state`, `curator-config`) and to any agent that writes to a Curator's audit log. If an agent does not have a formal version yet, it stamps `md_version: "unversioned"`. The stamp is never omitted.

---

### 1.6 What This Enables for the Scoring Layer

If the Scoring Unification Hypothesis is validated, MD version becomes a first-class dimension in the metrics:

- **Gate pass rate by MD version:** GPR(c, g, v) = |nodes with code c that pass gate g under MD version v| / |nodes with code c evaluated at gate g under MD version v|. This tells you whether a new set of instructions made the agent better or worse at a specific gate for a specific domain.
- **Code assignment quality by MD version:** Are certain codes over- or under-assigned after an MD change? Does the co-occurrence matrix shift in expected or unexpected ways?
- **Decay rate by MD version:** Does a new MD version cause the agent to stop assigning certain codes? This would show up as an accelerated decay rate for those codes under the new version.

This is the mechanism by which the system can score its own prompt engineering. Not "does this prompt feel better?" but "does this prompt produce measurably better outcomes across gates, codes, and metrics?" Mathematics decides.

---

## SECTION 2: THE DOPPELGANGER PATTERN

---

### 2.1 What a Doppelganger Is

A doppelganger is a clone of a production agent running candidate instructions in a sandbox environment. Same role. Same capabilities. Same data access (read-only sandbox copy). Different instructions.

The doppelganger is not a shadow deployment (running alongside production and handling real traffic). It is a test instance that processes a defined test suite in isolation. It does not touch production data. It does not affect production operations. It exists only for the duration of the test and is destroyed after.

The name is intentional. A doppelganger looks exactly like the original from the outside. It interacts with the same data structures, the same gate sequence, the same audit logging format. The only difference is what is inside — the instructions that govern its behaviour. This is the controlled variable. Everything else is held constant.

---

### 2.2 The Test Sequence

```
Candidate MD drafted
  → Doppelganger agent instantiated with candidate MD
    → Sandbox environment provisioned (read-only copy of relevant data)
      → Production agent instantiated with current MD (control)
        → Test suite executed: both agents process the same inputs
          → Metrics collected: gate pass rates, scoring layer metrics, error patterns
            → Comparison against production version
              → Pass: version number assigned, candidate promoted to production
              → Fail: candidate discarded, failure analysis logged in error registry
```

Both agents run against the same test cases in the same sandbox. This is a paired comparison. The same input produces two outputs. Differences between outputs are attributable to the instruction change, not to data variation or environmental noise.

---

### 2.3 Sandbox Provisioning

Each agent type requires a different sandbox configuration. The principle is consistent: the doppelganger operates on data that is representative of production but isolated from it.

| Agent Type | Sandbox Source | Provisioning Method | Notes |
|-----------|---------------|---------------------|-------|
| `curator-kg` | FalkorDB | Read-only snapshot via `BGSAVE` + restore to test instance | Memory cost is significant — FalkorDB is Redis-backed, so the snapshot consumes the same memory as the original. Schedule during off-peak. |
| `curator-vec` | Qdrant / pgvector | Qdrant snapshot or pgvector schema clone to test database | Vector indices must be included — testing without indices would not reflect production query performance. |
| `curator-doc` | PostgreSQL | `pg_dump` of relevant tables to test schema | Fastest to provision. Include only tables the Curator accesses. |
| `curator-state` | Temporal | Replay existing workflow histories against test worker | No data copy needed — Temporal's replay mechanism is designed for this. See ERR-TEMP-001 in the Error Anticipation Registry. |
| `curator-config` | YAML / Config Store | File copy | Trivial. |
| Pipeline agents | Vault test partition | Designated test directory with known-good and known-bad inputs | Maintain a permanent test partition in the vault. Do not use production vault files. |
| Kaizen / Chaos agents | Synthetic environment | Isolated test environment with injected error patterns from the Error Anticipation Registry | These agents test the system, so their sandbox needs to contain known defects to test against. |

**Sandboxes are ephemeral.** Created for the test. Destroyed after. No sandbox persists between test runs. This prevents sandbox drift — the gradual divergence between sandbox state and production state that would make test results unreliable.

**Temporal orchestrates provisioning.** The `DoppelgangerTestWorkflow` (Section 4) manages the full lifecycle: create sandbox, run test, collect metrics, evaluate, clean up. If the workflow fails at any step, the cleanup still runs. No orphaned sandboxes.

---

### 2.4 What Gets Measured

The measurement framework is designed to detect both regressions (the candidate is worse) and improvements (the candidate is better), and to be suspicious of both.

| Metric Category | Specific Metrics | Source | Why It Matters |
|----------------|-----------------|--------|---------------|
| **Gate pass rates** | Per-gate (G1–G7) pass rate, per-criterion sub-scores | Gate evaluation during test | The primary quality signal. If gate pass rates drop, the candidate is worse. Maps to `VALIDATION-METHODOLOGY-v2`, Section 4.2 and Section 12. |
| **Error pattern detection** | Matches against the Error Anticipation Registry (`CODE-TAXONOMY-AND-KAIZEN-v1`, Section 1) | Error registry scan of test outputs | Does the candidate trigger known error patterns? Does it trigger unknown patterns? |
| **Scoring layer metrics** | Reuse frequency, co-occurrence matrix, decay rate, bridge score (`SCORING-UNIFICATION-HYPOTHESIS-v2`, Section 1.5) | Computed from test outputs if scoring layer is active | Do code-level metrics change under the candidate? Changes are not automatically bad — they need interpretation. |
| **Response quality** | Blind comparison of production vs. candidate outputs for the same inputs | Paired output comparison | For agents that produce structured outputs (e.g., code assignments, gate evaluations), do the outputs differ? How? |
| **Performance** | Latency per operation, token usage per operation, cost per operation | Instrumentation during test | The candidate must not be significantly slower or more expensive. A 10% latency increase may be acceptable for better quality. A 200% increase is not. |
| **Regression check** | Test cases that currently pass under production — do they still pass under candidate? | Regression suite (subset of golden dataset) | The most important check. Any regression is a red flag. New capabilities mean nothing if existing capabilities break. |

---

### 2.5 Pass/Fail Criteria

The criteria are asymmetric by design. It is harder to pass than to fail. This is deliberate — we prefer the status quo to a risky change.

**Hard fail — automatic rejection:**

| Condition | Rationale |
|-----------|-----------|
| Any gate pass rate drops by more than 5% | Gate quality is constitutional. A 5% drop is statistically meaningful on the golden dataset (705 cases, so 5% ≈ 35 cases). |
| Any new error pattern detected that is not in the Error Anticipation Registry | Unknown errors are the most dangerous. If the candidate introduces a failure mode we have not anticipated, it cannot be promoted until the failure is understood and registered. |
| Any previously-verified error defence breaks | A defence that has achieved `verified` status in the Error Anticipation Registry (`CODE-TAXONOMY-AND-KAIZEN-v1`, Section 1) has passed 7 consecutive days of production operation. Breaking it is a regression that undermines the entire error anticipation system. |

**Soft fail — requires human review:**

| Condition | Rationale |
|-----------|-----------|
| Any metric changes by more than 10% in either direction | Large changes — even improvements — need understanding. A 15% improvement in gate pass rates sounds good, but might indicate that the candidate is being lenient rather than better. A 12% change in code co-occurrence patterns might indicate a systematic shift in how the agent interprets its domain. Understand before promoting. |

**Pass — eligible for promotion:**

| Condition | Rationale |
|-----------|-----------|
| All metrics within 5% of production AND no regressions | The candidate is at least as good as production. Small improvements are expected and welcome. |
| OR: measurably improved on target metrics with no regressions on non-target metrics | The candidate is better at what it was designed to improve, and does not break anything else. |

The 5% and 10% thresholds are starting values. After we accumulate experience with doppelganger testing, these thresholds should be calibrated based on observed variance in production metrics. If production metrics naturally fluctuate by ±3%, then a 5% threshold is meaningful. If they fluctuate by ±8%, then 5% is noise and the threshold needs to increase. Kaizen should track this.

---

### 2.6 The Comparison Protocol

Both production agent and doppelganger run against the **same** test cases. This is non-negotiable. Different test cases would introduce an uncontrolled variable.

**Test case sources:**

| Source | Size | Purpose |
|--------|------|---------|
| **Golden dataset** | 705 cases (or relevant subset per agent type) | The canonical test set from `VALIDATION-METHODOLOGY-v2`. Known-good and known-bad cases with ground truth labels. Provides the baseline measurement. |
| **Recent production data** | Randomly sampled from last 30 days of production operations | Tests against real-world patterns, not just curated test data. Production data contains edge cases, unusual formats, and domain-specific quirks that the golden dataset may not cover. |
| **Adversarial cases** | From the Chaos Agent's test library (`CODE-TAXONOMY-AND-KAIZEN-v1`, Section 3.7) | Tests robustness. The Chaos Agent specifically tries to trigger known error patterns (ERR-FALK-001 through ERR-LANG-007). If the candidate is vulnerable to attacks that production handles, it fails. |

**Pairing:** Every test case produces two outputs — one from the production agent, one from the doppelganger. The outputs are paired by input hash. Comparison is automated for quantitative metrics (gate pass rates, latency, code assignments) and blind for qualitative assessment (when human reviewers evaluate output quality, they do not know which output is production and which is candidate).

---

### 2.7 Human Oversight

Not all promotions are equal. The criticality of the agent determines the level of human oversight required.

| Agent Category | Human Sign-off Required? | Rationale |
|---------------|-------------------------|-----------|
| **Curator agents** (`curator-kg`, `curator-vec`, `curator-doc`, `curator-state`, `curator-config`) | **Always** | Curators are the sole database writers (`ATTRIBUTION-AND-CURATION-v1`, Section 2.5). A Curator MD change that introduces a subtle defect — slightly wrong code assignments, slightly permissive gate evaluation — propagates through every downstream operation. The blast radius is the entire database. |
| **Pipeline agents** | Only on soft fail | Pipeline agents process data through defined steps. If all hard criteria pass, the change is safe to auto-promote. Pipeline outputs are validated by Curators before storage, providing a second layer of protection. |
| **Kaizen / Chaos agents** | **Always** | These agents test the system itself. A Kaizen Agent with bad instructions might miss regressions. A Chaos Agent with bad instructions might cause real damage instead of controlled chaos. Meta-level changes need meta-level review. |

**All promotions are logged** in the audit trail with:
- Reviewer identity (human or "auto-promoted")
- Test results summary
- Promotion timestamp
- Previous version being replaced
- Rationale for promotion (required for human-reviewed promotions)

---

## SECTION 3: NUMERIC CODE MIGRATION

---

### 3.1 The Proposal

The current compressed coding system (`ATTRIBUTION-AND-CURATION-v1`, Section 3) uses text-based codes: `TEC-INFR-001`, `BIZ-STRT-002`, `FIN-CASH-001`. These are already compressed relative to full-text labels — "Docker container orchestration with health checks and restart policies" becomes `TEC-INFR-001`.

The proposal is to compress further. Replace text codes with numeric codes where the number encodes the hierarchy:

| Component | Digits | Encodes | Example |
|-----------|--------|---------|---------|
| Domain | First 2 digits | Top-level domain (Technology, Business, Finance, etc.) | `07` = Technology |
| Category | Next 2 digits | Category within domain (Infrastructure, Strategy, etc.) | `03` = Infrastructure |
| Concept | Last 2+ digits | Specific concept within category | `01` = Docker orchestration |

So `TEC-INFR-001` becomes `070301`. The mapping is maintained in the codebook.

---

### 3.2 Why This Matters

**Token density.** Numeric codes are 1–2 tokens vs. 3–4 for text codes. In the Pudding labelling context (`ATTRIBUTION-AND-CURATION-v1`, Section 3.7), where label density within a 512-token embedding window directly determines the number of cross-domain connections per document, this approximately doubles the label capacity. Current compressed codes provide ~3× more labels than full-text verbose labels. Numeric codes would provide ~6×. The Pudding Technique's discovery power scales with label count. This is a multiplier on a multiplier.

**Goodhart resistance.** This is the more surprising benefit. Agents working with text codes like `TEC-INFR-001` can infer meaning from the code itself — "TEC" is technology, "INFR" is infrastructure. An agent that has learned (through Goodhart dynamics) that certain codes score well might over-apply them. Numeric codes are opaque. `070301` conveys no semantic information to the agent. The agent cannot selectively game popular codes because it cannot decode them. Only the Curator, who holds the codebook, knows what the numbers mean.

This does not eliminate gaming entirely — an agent could still learn that certain numeric codes correlate with higher scores through trial and error. But it raises the bar significantly. Gaming text codes requires reading them. Gaming numeric codes requires learning their effects empirically across many operations. The opacity is a feature.

**Memory footprint.** In FalkorDB (Redis-backed), integers are stored more efficiently than strings. A 6-digit integer is 8 bytes. The string `TEC-INFR-001` is 12 bytes plus Redis string header overhead. At millions of nodes with multiple codes per node, this difference compounds.

**Query performance.** Integer comparison is faster than string comparison. Cypher queries matching on `code: 70301` execute faster than those matching on `code: "TEC-INFR-001"`. For traversal-heavy queries across large graphs, this matters.

---

### 3.3 The Curator as Sole Codebook Holder

This is the architectural decision that makes numeric codes work. The codebook — the mapping from numbers to meaning — is held exclusively by the Curator agents.

```
Other agents → request labels → Curator → translates → returns human-readable form
Other agents → submit data → Curator → compresses to numeric → stores
```

No agent outside the Curator roster (`curator-kg`, `curator-vec`, `curator-doc`, `curator-state`, `curator-config`) ever sees the numeric codes directly. They request human-readable labels and receive human-readable labels. The compression and decompression are entirely internal to the Curator.

This extends the existing pattern. `ATTRIBUTION-AND-CURATION-v1`, Section 2.4 already specifies that the Curator "translates labels to compressed codes" and that "the translation is invisible to calling agents." Numeric codes are the same pattern, compressed further.

**The codebook is versioned** alongside the Curator's MD (Section 1.4 of this document). A codebook version change is a configuration change that requires doppelganger testing. Adding a new numeric code, deprecating an existing one, or restructuring the hierarchy all go through the test sequence.

**Dependency risk:** If the Curator is down, no agent can decode anything. This is fail-closed behaviour — consistent with the Curator-only access rule (`ATTRIBUTION-AND-CURATION-v1`, Section 2.5). But it creates a single point of failure that needs redundancy planning. At minimum: the codebook should be replicated to a standby Curator instance, and the standby should be able to serve read-only codebook lookups if the primary is unavailable.

---

### 3.4 How to Test This with the Doppelganger Pattern

The numeric code migration is a perfect candidate for doppelganger testing. The change is well-defined (text codes → numeric codes), the existing infrastructure can run the comparison, and the metrics are clear.

**Test design:**

1. Clone `curator-kg` as a doppelganger with numeric codes enabled.
2. Provision a sandbox FalkorDB with the same data, labels converted to numeric.
3. Run the golden dataset through both:
   - Production `curator-kg` (text codes) processes inputs and produces outputs.
   - Doppelganger `curator-kg` (numeric codes) processes the same inputs and produces outputs.
4. Compare:

| Metric | How to Measure | What "Pass" Looks Like |
|--------|---------------|----------------------|
| Retrieval precision | Same queries, compare result sets | Identical result sets (codes are semantically equivalent, so results must be identical) |
| Embedding quality | Cosine similarity between embeddings with text-code metadata vs. numeric-code metadata | Similarity ≥ 0.95 (some variation expected from tokenisation differences) |
| Gate pass rates (G1–G7) | Run full gate sequence on both outputs | Identical pass/fail (the gates evaluate content quality, not code format) |
| Query latency | Time per query across 1000 representative queries | Numeric ≤ text (any improvement is a bonus; no regression allowed) |
| Memory usage | `GRAPH.MEMORY USAGE` on both FalkorDB instances | Numeric < text (expected improvement) |
| Label round-trip fidelity | Encode text → numeric → decode back to text via codebook | 100% fidelity (no information loss) |

**Critical check:** The label round-trip fidelity test verifies that the codebook mapping is lossless. If `TEC-INFR-001` → `070301` → codebook lookup → `TEC-INFR-001` does not produce an exact match, the codebook has a bug. This is a hard fail with zero tolerance.

---

### 3.5 Migration Strategy (If Validated)

If doppelganger testing confirms that numeric codes match or exceed text codes on all metrics, the migration proceeds in three phases. Each phase has its own doppelganger test before proceeding.

**Phase 1 — Parallel Operation**

| Aspect | Detail |
|--------|--------|
| Duration | 30 days minimum |
| Storage | Both text and numeric codes stored on every node. Dual properties: `code_text: "TEC-INFR-001"`, `code_num: 070301` |
| Reads | All reads use text codes (no external change) |
| Writes | Curator writes both codes simultaneously |
| Metrics | Kaizen monitors for any divergence between text and numeric code paths |
| Doppelganger test | Run weekly during this phase. Any divergence between parallel paths triggers investigation. |
| Go/no-go | If no divergence after 30 days, proceed to Phase 2. If any divergence, investigate and extend Phase 1. |

**Phase 2 — Numeric Primary**

| Aspect | Detail |
|--------|--------|
| Duration | 30 days minimum |
| Storage | Numeric codes are the primary storage. Text codes are stored as expansion-only metadata (for debugging and audit readability). |
| Reads | Internal reads use numeric codes. External reads (API responses, audit log display) auto-expand via codebook. |
| Writes | Curator writes numeric primary. Text expansion computed on write for metadata field. |
| Doppelganger test | Run at Phase 2 start against Phase 1 baseline. |
| Go/no-go | If all metrics stable after 30 days, proceed to Phase 3. |

**Phase 3 — Text Codes Deprecated in Storage**

| Aspect | Detail |
|--------|--------|
| Storage | Only numeric codes stored on nodes. Text codes generated on-the-fly by Curator on read via codebook lookup. |
| Reads | Curator expands numeric → text for all external-facing responses. Internal operations use numeric. |
| Memory | Expected reduction in FalkorDB memory footprint. Measure and report. |
| Doppelganger test | Run at Phase 3 start against Phase 2 baseline. |
| Rollback | If any metric degrades, revert to Phase 2 (text codes still exist in backup). |

---

### 3.6 Debugging Concern and Mitigation

Raw graph dumps become unreadable without the codebook. A FalkorDB export showing `{code_num: 070301, code_num: 120201, code_num: 040101}` tells a human nothing. This is a real operational cost.

**Mitigations:**

1. **`debug_expand` mode.** The Curator provides a diagnostic endpoint that translates all codes in a query result to human-readable form. Any developer or agent querying the graph for debugging calls `curator-kg.query(cypher, expand_labels=True)`. This is the existing read flow (`ATTRIBUTION-AND-CURATION-v1`, Section 2.4) — it already expands codes. Numeric codes change the internal representation but not the external API.

2. **Dual-format audit logs.** Audit logs store both the numeric code and the expanded label. Logs are for humans too. An audit entry reads:

```yaml
codes_assigned:
  - code_num: 070301
    label: "TEC-INFR-001 — Docker container orchestration"
  - code_num: 120201
    label: "BIZ-STRT-002 — Market positioning strategy"
```

This doubles the storage for the code field in audit logs. The trade-off is worth it — audit logs are the debugging interface, and an unreadable debugging interface is useless.

3. **Read-only web interface.** A lightweight web tool that auto-expands codes for human graph browsing. Takes a FalkorDB query, runs it through the Curator's expansion, and renders the results with full labels. This is a convenience tool, not a critical system component. It can be built after the core migration is stable.

---

## SECTION 4: TEMPORAL WORKFLOW DESIGN

---

The doppelganger test maps to a Temporal workflow. This is not a new pattern — the Kaizen Department already uses Temporal for the `KaizenWorkflow` and `ChaosWorkflow` (`CODE-TAXONOMY-AND-KAIZEN-v1`, Section 3.1). The `DoppelgangerTestWorkflow` follows the same conventions.

```yaml
DoppelgangerTestWorkflow:
  input:
    agent_id: string              # Which agent is being tested (e.g., "curator-kg")
    candidate_md: string          # Path to candidate MD file
    candidate_md_version: string  # e.g., "v3-candidate-a"
    test_scope: enum              # "golden_dataset", "recent_production", "adversarial", "all"

  steps:
    1_provision_sandbox:
      activity: ProvisionSandboxActivity
      timeout: 600s               # FalkorDB snapshots can take time
      retry: 2
      # Creates read-only data snapshot for the agent's domain
      # Selects provisioning method based on agent_id (see Section 2.3 table)
      # Returns: sandbox_id, connection_config

    2_instantiate_doppelganger:
      activity: InstantiateDoppelgangerActivity
      timeout: 60s
      retry: 1
      # Loads candidate MD into a fresh agent instance
      # Connects to sandbox via connection_config
      # Returns: doppelganger_agent_handle

    3_instantiate_production:
      activity: InstantiateProductionActivity
      timeout: 60s
      retry: 1
      # Loads current production MD for comparison
      # Connects to same sandbox (read-only — no write conflicts)
      # Returns: production_agent_handle

    4_run_test_suite:
      activity: RunTestSuiteActivity
      timeout: 3600s              # Full test suite can take up to an hour
      heartbeat: 30s              # Long-running — heartbeat required (ERR-TEMP-002)
      retry: 1
      # Runs both agents against the same test cases
      # Test cases selected by test_scope parameter
      # Collects paired outputs: (input_hash, production_output, doppelganger_output)
      # Returns: paired_results[]

    5_compute_metrics:
      activity: ComputeMetricsActivity
      timeout: 300s
      retry: 2
      # Gate pass rates per gate (G1–G7)
      # Scoring layer metrics (if active)
      # Error pattern matches against Error Anticipation Registry
      # Performance metrics (latency, token usage)
      # Regression analysis (cases that pass in production but fail in candidate)
      # Returns: metrics_report

    6_evaluate:
      activity: EvaluateActivity
      timeout: 60s
      retry: 1
      # Applies pass/fail criteria from Section 2.5
      # Returns: verdict (PASS | SOFT_FAIL | HARD_FAIL), explanation

    7_decide:
      # Routes based on verdict AND agent category:
      #
      # PASS + pipeline agent → auto-promote
      #   Activity: PromoteVersionActivity
      #   Updates curator-config with new version number
      #   Deploys new MD to production
      #
      # PASS + Curator or Kaizen/Chaos agent → queue for human review
      #   Activity: QueueForReviewActivity
      #   Creates review ticket with metrics_report
      #   Waits for human signal (Temporal signal, not polling)
      #
      # SOFT_FAIL (any agent) → queue for human review with explanation
      #   Activity: QueueForReviewActivity
      #   Includes explanation of which metrics triggered soft fail
      #
      # HARD_FAIL (any agent) → reject
      #   Activity: RejectCandidateActivity
      #   Logs failure in Error Anticipation Registry as new entry
      #   Candidate MD archived but never promoted

    8_cleanup:
      activity: CleanupSandboxActivity
      timeout: 300s
      retry: 3                    # Cleanup must succeed — orphaned sandboxes waste memory
      # Destroys ephemeral sandbox
      # Releases any held resources
      # Always runs, even if previous steps failed (Temporal compensation pattern)

  output:
    result: enum                  # PROMOTED, PENDING_REVIEW, REJECTED
    metrics_report: object        # Full comparison data
    version_assigned: string      # If promoted: "v3". If not: null
    failure_reason: string        # If rejected: explanation. If not: null
```

**Error handling notes:**

- `ProvisionSandboxActivity` timeout accounts for FalkorDB `BGSAVE` on large graphs. If provisioning exceeds 600s, investigate graph size — it may be time to partition the test data.
- `RunTestSuiteActivity` uses a 30s heartbeat interval. This follows the defence against ERR-TEMP-002 (workers disappearing without visible error). Without heartbeat, a hanging test suite would silently consume a worker slot.
- `CleanupSandboxActivity` retries 3 times. Orphaned sandboxes are memory leaks — especially FalkorDB sandboxes, which consume Redis memory. Cleanup failures are escalated to Kaizen.
- The `7_decide` step uses Temporal signals for human review, not polling. The workflow pauses and waits for a signal. This is the correct Temporal pattern — it does not consume worker slots while waiting.

---

## SECTION 5: WHAT THIS CONNECTS TO

---

### 5.1 CODE-TAXONOMY-AND-KAIZEN-v1

**New workflow:** The Kaizen Department gains `DoppelgangerTestWorkflow` as a formally scheduled workflow. It fits naturally into the existing department structure (Section 3.1):

| Agent | How It Connects |
|-------|----------------|
| **Kaizen Agent** (daily at 03:00 UTC) | Triggers doppelganger tests when MD changes are detected. Reviews test results as part of daily metrics. Correlates MD version changes with metric shifts. |
| **Regression Sentinel** (on every deployment) | Becomes the post-promotion verification. After a doppelganger-tested MD is deployed, the Regression Sentinel re-runs all verified defences to confirm nothing was broken in the live environment. |
| **Chaos Agent** (nightly 01:00–04:00 UTC) | Supplies adversarial test cases to the doppelganger test suite. Chaos Agent's test library becomes a shared resource. |

**New error category:** Doppelganger test failures become a new category in the Error Anticipation Registry (Section 1). Error IDs follow the convention: `ERR-DPLG-001`, `ERR-DPLG-002`, etc.

| Error ID | Description | Defence |
|----------|-------------|---------|
| ERR-DPLG-001 | Candidate MD causes gate regression (>5% drop on any gate) | Reject candidate. Investigate which gate criteria are affected. Log the instruction change that caused the regression. |
| ERR-DPLG-002 | Candidate MD introduces unknown error pattern | Reject candidate. Register new error pattern. Build defence before retesting. |
| ERR-DPLG-003 | Candidate MD breaks verified error defence | Reject candidate. The defence was verified for a reason — the candidate's instructions conflict with a known protection. |
| ERR-DPLG-004 | Sandbox provisioning fails (data snapshot corruption, timeout) | Retry with backoff. If persistent, investigate source database health. |
| ERR-DPLG-005 | Metrics diverge >10% without clear cause | Soft fail. Queue for human analysis. May indicate a subtle interaction effect. |

### 5.2 ATTRIBUTION-AND-CURATION-v1

**Audit log enhancement:** The `md_version` field (Section 1.5 of this document) is added to the Curator audit log format defined in Section 2.4 of `ATTRIBUTION-AND-CURATION-v1`. This is a non-breaking additive change — existing audit entries without `md_version` are valid (they predate versioning).

**Code registry versioning:** The code registry (`ATTRIBUTION-AND-CURATION-v1`, Section 3.5) gains a version property. The existing `schema_version: "v1"` field in the registry format becomes the codebook version, tracked alongside the Curator's MD version. Codebook changes (new codes, deprecated codes, new synonyms, hierarchy changes) require doppelganger testing just as MD changes do.

**Curator-only access extended:** The Curator-only access rule (Section 2.5) now extends to the codebook. Only Curators hold the codebook. Only Curators can decode numeric codes. This is consistent with the existing rule — the Curator is already the sole translator between human-readable labels and compressed codes. Numeric codes make this translation more opaque, which strengthens the access control.

### 5.3 VALIDATION-METHODOLOGY-v2

**Gates as test criteria:** The 7 gates (G1: Structure, G2: Label Validity, G2b: Inter-Rater, G3: Rubric & Benchmark, G4: Match Quality, G5: Recipe + Scoring, G6: Test + INTENTLOGIC, G7: Final Boss) are the primary pass/fail criteria for doppelganger tests. Gate pass rates are compared between production and candidate. The enforcement matrix (Section 12) defines what each gate checks — the same checks apply to doppelganger test outputs.

**Per-criterion decomposition:** The doppelganger test measures per-gate results. But for maximum diagnostic value, per-criterion sub-scores within each gate should also be compared. For example, if G3 pass rate drops, is it the RAEI score, the PRS score, the believability assessment, or the label consistency check that is failing? This per-criterion decomposition is what the Scoring Unification Hypothesis (Section 2.6) calls the meta-scoring cascade. Doppelganger testing is where it becomes practically useful.

### 5.4 SCORING-UNIFICATION-HYPOTHESIS-v2

**MD version as a scoring dimension:** If the scoring layer is implemented, MD version becomes another axis in the metrics. The code-level metrics (Section 1.5: reuse frequency, co-occurrence, decay, bridge score) can be partitioned by MD version to identify which instruction changes improved or degraded the system.

**Doppelganger results feed meta-scoring:** Each doppelganger test produces a complete set of gate results and scoring metrics for a candidate MD. This is exactly the data that the meta-scoring cascade (Section 2) needs: paired gate evaluations under controlled conditions. Over time, doppelganger test results accumulate into a dataset that can answer: which gates are most sensitive to instruction changes? Which criteria within those gates are doing the discriminating work? This is meta-scoring in practice.

**Validation plan integration:** The numeric code experiment (Section 3) naturally aligns with Phase 1 of the Scoring Unification validation plan (Section 7). Phase 1 extracts existing metrics from Curator audit logs. Running this extraction on both text-coded and numeric-coded audit logs during the parallel operation phase (Section 3.5, Phase 1) provides a controlled comparison of metric extraction under both schemes.

---

## SECTION 6: WHAT WE DON'T KNOW

---

Honest gaps. These are not weaknesses to hide. They are the areas where measurement is needed before confidence is warranted.

### 6.1 Sandbox Fidelity

A read-only snapshot may not capture all production conditions. Concurrent writes, load patterns, timing-dependent race conditions, and inter-agent interactions are all absent from the sandbox. A candidate MD that passes doppelganger testing in a quiet sandbox may fail under production load.

**Mitigation:** Canary deployment after promotion. Run both the promoted version and the previous version in production for a defined period (7 days recommended), with the new version handling a small percentage of traffic (10%). Monitor all metrics during the canary period. If the canary degrades, roll back. This is standard practice in software deployment. It applies equally to agent instructions.

**Residual risk:** Canary deployment adds operational complexity. The system needs to route traffic to two agent versions simultaneously. For Curator agents, this means two instances accessing the same database, which conflicts with the single-Curator rule (`ATTRIBUTION-AND-CURATION-v1`, Section 2.5). The canary period may need to use a different mechanism for Curators — perhaps processing a subset of writes with both versions and comparing results, rather than splitting traffic.

### 6.2 Test Coverage

The golden dataset (705 cases from `VALIDATION-METHODOLOGY-v2`) may not cover all production scenarios. Supplementing with recent production data helps but does not guarantee coverage. There may be edge cases — unusual document formats, rare domain combinations, adversarial inputs — that neither the golden dataset nor recent production data contains.

**Mitigation:** Continuously expand the golden dataset. Every production failure that was not caught by doppelganger testing becomes a new test case. The Regression Sentinel already captures these (`CODE-TAXONOMY-AND-KAIZEN-v1`, Section 3.1). Feed them back into the golden dataset.

### 6.3 Cost

Spinning up sandbox environments and running dual agents is not free.

| Cost Component | Estimate | Notes |
|---------------|----------|-------|
| FalkorDB sandbox | Same memory as production instance | Redis-backed — full memory copy. This is the largest single cost. |
| Qdrant/pgvector sandbox | Moderate — depends on index size | Vector indices must be included for query performance testing. |
| Dual agent execution | 2× token cost for LLM-backed agents | Both agents process the same test cases. Token costs double. |
| Temporal workflow overhead | Minimal | Temporal is already running. One more workflow is marginal. |

**Mitigation:** Schedule doppelganger tests during off-peak hours. The Kaizen Department's 01:00–04:00 UTC window (`CODE-TAXONOMY-AND-KAIZEN-v1`, Section 3.1) is the natural fit. FalkorDB memory pressure is lowest when production queries are minimal.

**Mitigation:** Not every MD change requires a full test. Define a threshold for "significant change" — perhaps measured by edit distance or structural diff of the MD. Trivial changes (typo fixes, comment additions) can skip the full test suite and run only the regression check. This is a trade-off that should be evaluated after we have experience with the system.

### 6.4 Interaction Effects

An agent MD change might test well in isolation but interact poorly with other agents in production. For example: a new `curator-kg` MD might produce slightly different code assignments that, while individually valid, confuse the Pudding agent's cross-domain labelling or degrade `curator-vec`'s embedding quality.

**Mitigation:** Multi-agent doppelganger tests for changes that affect inter-agent communication. If a Curator MD change alters the code assignment behaviour, test the downstream agents too — run the Pudding agent against the Curator doppelganger's outputs and verify that cross-domain labelling still works.

**Residual risk:** Multi-agent tests are expensive and complex. We may need to choose between thoroughness and practicality. Starting position: single-agent tests for most changes, multi-agent tests for changes that alter the Curator API or code assignment logic.

### 6.5 How Often to Test

Every MD change? Only significant changes? The threshold for "significant" is currently undefined.

**Starting position:** Every change gets tested. This is conservative and may be expensive, but it prevents untested changes from reaching production. After 3 months of operation, review the test frequency based on:
- How many tests were run?
- How many found issues?
- What was the false positive rate (tests that flagged changes as risky but turned out to be fine)?
- What was the false negative rate (changes that passed testing but caused production issues)?

Optimise the testing frequency based on these numbers. If every test passes, we may be testing too often. If tests regularly catch issues, the frequency is justified. Mathematics decides.

---

## SECTION 7: IMPLEMENTATION PRIORITY

---

Three components, ordered by cost-to-value ratio:

### Priority 1: MD Versioning

**Cost:** Low. Adding `md_version` to audit log stamps is one additional field. Versioning MDs in `curator-config` is a configuration management task.

**Value:** Immediate. From the moment versions are stamped, every future investigation can correlate behaviour with instructions. This is retroactive diagnostic power — you cannot add versioning after a problem occurs and expect it to help with that problem.

**Implementation:**
1. Define version labels for all current agent MDs. Every current MD becomes V1.
2. Add `md_version` field to Curator audit log format.
3. Update all five Curators to stamp `md_version` on every log entry.
4. Store MD version history in `curator-config`.
5. Update Kaizen Agent to include MD version in its daily metrics report.

**Target:** Can be operational within one week.

### Priority 2: Doppelganger Test Workflow

**Cost:** Medium. Requires sandbox provisioning infrastructure, the Temporal workflow (`DoppelgangerTestWorkflow`), the test harness (paired execution and comparison), and the evaluation logic (pass/fail criteria).

**Value:** High. Every future MD change is tested before deployment. The system moves from "change and hope" to "change and verify."

**Implementation:**
1. Build `ProvisionSandboxActivity` for each database type (FalkorDB, Qdrant/pgvector, PostgreSQL).
2. Build `RunTestSuiteActivity` with paired execution against the golden dataset.
3. Build `ComputeMetricsActivity` with per-gate comparison.
4. Build `EvaluateActivity` with the pass/fail criteria from Section 2.5.
5. Wire into Temporal as `DoppelgangerTestWorkflow`.
6. Integrate with Kaizen Agent for automated triggering on MD changes.

**Target:** 2–3 weeks for core workflow. Iterative improvement of test cases and thresholds ongoing.

### Priority 3: Numeric Code Experiment

**Cost:** Medium-high. Requires codebook mapping, sandbox with converted data, and the full doppelganger test pipeline from Priority 2.

**Value:** High if validated (token density, Goodhart resistance, memory, performance). Uncertain until tested — this is an experiment, not a guaranteed improvement.

**Implementation:**
1. Build the numeric codebook mapping (domain → 2-digit, category → 2-digit, concept → 2-digit+).
2. Write the conversion tool (text code → numeric code for existing data).
3. Run doppelganger test: text-coded `curator-kg` vs. numeric-coded doppelganger.
4. If results are positive, begin Phase 1 (parallel operation) as described in Section 3.5.

**Target:** Run as a measured experiment during Phase 1 of the Scoring Unification validation plan (`SCORING-UNIFICATION-HYPOTHESIS-v2`, Section 7). This aligns the two initiatives — the numeric code experiment produces data that the scoring layer validation needs.

---

## SECTION 8: VERSION HISTORY

| Version | Date | Changes | Authors |
|---------|------|---------|---------|
| v1 | 2026-03-17 | Initial specification — Agent MD versioning, doppelganger testing pattern, numeric code migration proposal, Temporal workflow design, companion document integration | Ewan Bramley (originator) × Claude (researcher, formaliser, builder) |

---

*Document version: v1 — March 2026 — Amplified Partners*
*This document proposes a testing and versioning standard for agent instructions and system codes.*
*Companion documents: CODE-TAXONOMY-AND-KAIZEN-v1, ATTRIBUTION-AND-CURATION-v1, VALIDATION-METHODOLOGY-v2, SCORING-UNIFICATION-HYPOTHESIS-v2*

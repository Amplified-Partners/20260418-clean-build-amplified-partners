---
title: "Amplified Partners — Dual Code Organisation, Pattern Taxonomy & Open-Source Strategy v1"
id: "dual-code-organisation-v1-copy"
version: 1
created: "2026-04-25"
type: "document"
topic_type: "unsorted"
audience: "internal"
layer: "shadow"
status: "filed"
signed_by: "Devon, 2026-04-25, devin-992682c244cf444f91e0a516498afbfd"
---

# Amplified Partners — Dual Code Organisation, Pattern Taxonomy & Open-Source Strategy v1

---

## THE LAW

**Code lives twice. Once where it works. Once where it teaches.**

**Every pattern is named. Every instance is indexed. Every canonical is enforced. No exceptions.**

This document is constitutional. It defines how code is organised, cross-indexed, and improved across the Amplified Partners engineering stack. It does not describe an aspiration. It describes the law.

A retry-with-backoff in a FalkorDB client and a retry-with-backoff in a LiteLLM client are the same pattern. They have the same failure modes, the same remedies, and the same conformance requirements. The fact that they live in different service directories is a filing accident, not a meaningful distinction. This document ends that accident.

Mathematics decides. Not vibes. Not urgency. Not "we'll fix it later." The pattern index is the single source of truth. Every module is checked against it. Every divergence is scored. Every score below threshold triggers mandatory remediation.

This document operates in constitutional lockstep with its three companion documents:

- **FILE-NAMING-CONVENTION-v1** — how files are named across the codebase
- **VALIDATION-METHODOLOGY-v2** — the 7 gates (G1–G7) that govern every pipeline
- **CODE-TAXONOMY-AND-KAIZEN-v1** — 96 ERR-IDs, 20 module types, and the Kaizen Department

Read all four. They are a single system, not four separate opinions.

---

## SECTION 1: WHY THIS ISN'T SHITE

The instinct behind dual code organisation is not new. It maps directly onto decades of established computer science. What is new is doing it operationally — in the actual repo, with enforcement, conformance scoring, and living improvement cycles. That has not been done before. This section explains the lineage so nobody confuses "unprecedented" with "untested."

---

### 1.1 Gang of Four (1994)

In 1994, Gamma, Helm, Johnson, and Vlissides published the canonical book on software design patterns. They catalogued 23 patterns and organised them by **intent**, not by where they happened to live in a codebase. Their three categories — Creational, Structural, and Behavioural — are a taxonomy of purpose. A Factory Method is a Factory Method whether it instantiates a database connection or a message queue. The GoF understood that the pattern transcends its location.

They organised patterns in a textbook. Ewan's insight is to do the same thing in the operational repository itself — with enforcement.

Every pattern in Section 3 of this document carries a GoF or Fowler equivalent where one exists. That lineage is deliberate. It grounds the Amplified taxonomy in forty years of prior art and makes the reasoning auditable.

---

### 1.2 Martin Fowler's Enterprise Patterns

Martin Fowler extended the GoF approach to enterprise architecture, cataloguing patterns at a higher level of abstraction: Unit of Work, Repository, Gateway, Service Layer, Event Sourcing, CQRS, Saga. Same principle applied at larger scale. The pattern has an identity independent of its host service. You can have a Repository pattern in your PostgreSQL layer and a Repository pattern in your FalkorDB layer. They are distinct implementations of the same intent.

Fowler catalogued these patterns in books and on his website. Amplified's approach is to enforce them in CI, not just describe them in prose.

---

### 1.3 What Existing Tools Do — and Do Not Do

**Sourcegraph's SCIP protocol** performs cross-repository semantic code navigation. It indexes code language-agnostically so developers can find where a function is called across dozens of repositories. It is excellent for code discovery. It does not organise code by pattern, does not provide canonical implementations, does not score conformance, and does not run remediation. It helps you find code. It does not help you ensure code conforms to intent.

**Pieces for Developers** provides AI-enriched snippet reuse. It captures code fragments and suggests them in context. It is a snippet manager with intelligence attached. It does not maintain a pattern taxonomy, does not enforce conformance, and does not integrate with a Kaizen improvement cycle.

Neither tool does what this document describes. Both are complementary to it, not substitutes for it.

---

### 1.4 The Gap

Nobody has built pattern-indexed AI/SMB infrastructure code as an operational open-source project. The GoF organised patterns in a book. Fowler organised them in a book and a website. Sourcegraph helps you find code. Pieces helps you reuse snippets. None of them do what this document specifies:

- A living pattern taxonomy embedded in the actual repository
- instances.yaml cross-indexing every implementation
- Conformance scoring runnable in CI
- Canonical implementations enforced as the default
- Automated detection of pattern drift
- A Kaizen cycle that improves canonicals and propagates improvements to all instances
- An open-source project that publishes the taxonomy and tooling for the broader AI/SMB engineering community

That combination is genuinely new. Ewan's instinct is correct. The Pudding Technique applied to code is the cross-domain discovery insight that makes the difference between a codebase that accumulates debt and one that systematically improves itself.

---

## SECTION 2: THE DUAL ORGANISATION MODEL

Code has two valid views. Neither replaces the other. Both are always true simultaneously.

---

### 2.1 View 1 — By Function (Where Code Lives)

This is the conventional directory structure. Code lives where it operates. Services own their implementations. Shared utilities are colocated. Nothing surprising here.

```
amplified-partners/
├── services/
│   ├── falkordb-client/
│   ├── litellm-proxy/
│   ├── graphiti-ingest/
│   ├── temporal-workers/
│   └── hounddog-engine/
├── pipelines/
│   ├── vault-ingest/
│   ├── naming-validate/
│   └── pudding-extract/
├── shared/
│   ├── guards/
│   ├── transforms/
│   └── monitors/
└── tests/
```

View 1 answers the question: **"Where does this code run?"**

It is the ground truth for deployment, for service ownership, for operational responsibility. A bug in `services/falkordb-client/` is owned by whoever owns the FalkorDB client service. This does not change.

---

### 2.2 View 2 — By Pattern (The Cross-Index)

View 2 is not a replacement for View 1. It is an overlay. It lives in a `.patterns/` directory at the repository root and indexes every View 1 file that implements a known pattern.

```
.patterns/
├── retry-with-backoff/
│   ├── README.md
│   ├── instances.yaml
│   ├── canonical.py
│   └── tests/
│       └── pattern-conformance.test.py
├── circuit-breaker/
│   ├── README.md
│   ├── instances.yaml
│   ├── canonical.py
│   └── tests/
│       └── pattern-conformance.test.py
├── rate-limiter/
├── health-check-probe/
├── idempotent-write/
├── prompt-template-inject/
│   ... (all indexed patterns)
```

View 2 answers the question: **"What pattern does this code implement, and how well?"**

---

### 2.3 What Each File in a Pattern Directory Contains

**README.md**
The human-readable specification for the pattern. Contains:
- Pattern name and one-line intent
- When to use this pattern
- When NOT to use this pattern (this section is mandatory)
- Known anti-patterns and failure modes
- GoF or Fowler equivalent, if one exists
- The conformance criteria used for scoring

**instances.yaml**
The machine-readable cross-index. Every View 1 file that implements this pattern is listed here, with path, service, language, conformance score (0.0–1.0), last audit date, and any notes about known divergences. This file is the authoritative record of where the pattern lives. It is updated by the Kaizen Department and by automated scanning.

**canonical.py (or canonical.ts)**
The reference implementation. This is the gold standard. It is the code that every instance is scored against. It is maintained by the Kaizen Department. When it improves, all instances are flagged for upgrade. It is not an abstract template — it is runnable, tested code.

**tests/pattern-conformance.test.py**
Conformance tests that can be run against any instance of the pattern. They test structural properties (does the implementation have exponential backoff?), behavioural properties (does it respect the maximum retry count?), and integration properties (does it emit the correct structured log on failure?). These tests are the scoring engine for the conformance metric.

---

### 2.4 The instances.yaml Format — Worked Example

The following example shows `retry-with-backoff` indexed across three service implementations with varying conformance scores.

```yaml
# .patterns/retry-with-backoff/instances.yaml

pattern: retry-with-backoff
canonical: canonical.py
last_taxonomy_review: 2026-03-01
minimum_conformance: 0.70

instances:
  - id: falkordb-client-retry
    path: services/falkordb-client/src/resilience/retry.py
    service: falkordb-client
    language: python
    module_type: client
    conformance_score: 0.92
    last_audit: 2026-03-10
    notes: >
      Implements exponential backoff with jitter. Respects MAX_RETRY_ATTEMPTS
      from config. Emits ERR-DB-003 on exhaustion. Minor divergence: does not
      emit structured log on each individual retry attempt (canonical does).
      Flagged for upgrade in next Kaizen cycle.

  - id: litellm-proxy-retry
    path: services/litellm-proxy/src/resilience/retry.py
    service: litellm-proxy
    language: python
    module_type: client
    conformance_score: 0.78
    last_audit: 2026-02-28
    notes: >
      Uses fixed backoff intervals rather than exponential. This is intentional
      for LLM rate limiting (see ERR-LLM-007 commentary). Exception granted.
      Documented in instances.yaml as justified divergence, not a defect.

  - id: graphiti-ingest-retry
    path: services/graphiti-ingest/src/resilience/retry.py
    service: graphiti-ingest
    language: python
    module_type: pipeline
    conformance_score: 0.61
    last_audit: 2026-02-15
    notes: >
      BELOW MINIMUM THRESHOLD. Does not implement jitter. Retries on non-retryable
      errors (connection refused not distinguished from auth failure). Mandatory
      refactor required within 48 hours per Section 8 enforcement rules.
      Assigned to Kaizen: 2026-02-16. Target completion: 2026-02-18.
```

The conformance score of 0.61 for `graphiti-ingest-retry` is a live problem, not a historical note. Section 8 rules apply immediately.

---

### 2.5 The Symbiosis — How View 1 and View 2 Feed Each Other

The two views are not independent databases. They create a feedback loop.

**When code is written in View 1:**
Before writing implementation code, the developer checks View 2. Is there an existing pattern that matches the intended behaviour? If yes, the canonical implementation is the starting point, not a blank file. This eliminates the most common source of pattern drift: parallel reinvention.

**When a pattern match is found:**
The canonical is used directly, or adapted with documented justification. The new instance is added to instances.yaml with an initial conformance score. The Kaizen Department is notified of the new instance.

**When a canonical improves:**
Every instance in instances.yaml is automatically flagged for re-audit. The Kaizen Department schedules conformance reviews. Instances with scores that would drop below 0.70 against the new canonical are placed on mandatory upgrade timelines.

**When a new instance diverges:**
A divergence is either a conformance issue (the instance got it wrong — fix it) or a genuine pattern variant (the instance has a justified reason to differ — document the variant). If a variant appears in two or more services, it becomes a candidate for promotion to its own pattern entry. Variants are not second-class citizens; they are pattern evolution in progress.

**The compound effect:**
Every improvement to a canonical propagates to all instances. Every new instance contributes back to the canonical if it solves a problem the canonical did not address. The codebase improves in compound fashion, not linearly.

---

## SECTION 3: THE PATTERN TAXONOMY

Thirty-five patterns organised across seven categories, calibrated to the Amplified Partners stack. GoF and Fowler equivalents are noted where they exist. Module types from CODE-TAXONOMY-AND-KAIZEN-v1 are referenced throughout.

The Expected Frequency column reflects how often this pattern is expected to appear across the full Amplified codebase: **High** (5+ instances), **Medium** (2–4 instances), **Low** (1–2 instances, candidate for future cross-indexing).

---

### Resilience

| Pattern Name | GoF / Fowler Equivalent | Module Types | Expected Frequency |
|---|---|---|---|
| retry-with-backoff | — | client, pipeline, worker | High |
| circuit-breaker | Proxy (GoF structural) | client, monitor, guard | High |
| dead-letter-queue | — | worker, pipeline | Medium |
| saga-compensate | — | workflow, activity | Medium |
| graceful-degrade | Strategy (GoF behavioural) | guard, client, pipeline | Medium |
| bulkhead-isolate | — | worker, monitor | Medium |
| timeout-with-fallback | — | client, pipeline, guard | High |

---

### Performance

| Pattern Name | GoF / Fowler Equivalent | Module Types | Expected Frequency |
|---|---|---|---|
| rate-limiter | — | guard, client, monitor | High |
| cache-aside | — | client, util, pipeline | High |
| connection-pool-with-drain | — | client, config | Medium |
| batch-with-checkpoint | — | pipeline, worker | High |
| lazy-load | Proxy (GoF structural) | client, adapter | Medium |
| prefetch-warm | — | worker, pipeline | Low |

---

### Data Integrity

| Pattern Name | GoF / Fowler Equivalent | Module Types | Expected Frequency |
|---|---|---|---|
| idempotent-write | — | pipeline, client, activity | High |
| content-hash-dedup | — | util, pipeline, guard | High |
| schema-validate-then-write | — | guard, schema, pipeline | High |
| event-source-replay | Event Sourcing (Fowler) | workflow, activity, worker | Medium |
| optimistic-lock | — | client, pipeline | Medium |
| write-ahead-log | — | pipeline, worker, activity | Medium |

---

### Orchestration

| Pattern Name | GoF / Fowler Equivalent | Module Types | Expected Frequency |
|---|---|---|---|
| fan-out-fan-in | — | workflow, pipeline, worker | Medium |
| temporal-versioned-patch | — | workflow, activity | Medium |
| state-machine-transition | State (GoF behavioural) | workflow, monitor, guard | Medium |
| pub-sub-dispatch | Observer (GoF behavioural) | worker, hook, pipeline | Medium |
| pipeline-stage-chain | Chain of Responsibility (GoF) | pipeline, transform, guard | High |

---

### AI / LLM Specific

| Pattern Name | GoF / Fowler Equivalent | Module Types | Expected Frequency |
|---|---|---|---|
| prompt-template-inject | Template Method (GoF behavioural) | prompt, pipeline, workflow | High |
| token-budget-guard | — | guard, monitor, client | High |
| embedding-cache | — | client, util, pipeline | High |
| response-validate | — | guard, rubric, pipeline | High |
| hallucination-guard | — | guard, rubric, monitor | High |
| model-fallback-chain | Chain of Responsibility (GoF) | client, guard, pipeline | High |

---

### Security

| Pattern Name | GoF / Fowler Equivalent | Module Types | Expected Frequency |
|---|---|---|---|
| guard-lint-reject | — | guard, test, pipeline | High |
| secret-rotate | — | config, worker, monitor | Medium |
| auth-token-refresh | — | client, hook, guard | Medium |
| input-sanitise | — | guard, transform, pipeline | High |
| permission-check-before-act | Decorator (GoF structural) | guard, hook, workflow | Medium |

---

### Observability

| Pattern Name | GoF / Fowler Equivalent | Module Types | Expected Frequency |
|---|---|---|---|
| health-check-probe | — | monitor, client, worker | High |
| structured-log-emit | — | util, monitor, pipeline | High |
| metric-counter-increment | — | monitor, util, hook | High |
| trace-span-wrap | Decorator (GoF structural) | monitor, util, pipeline | Medium |
| alert-threshold-breach | Observer (GoF behavioural) | monitor, hook, worker | Medium |

---

### Taxonomy Summary

| Category | Pattern Count | High Frequency Count |
|---|---|---|
| Resilience | 7 | 3 |
| Performance | 6 | 3 |
| Data Integrity | 6 | 4 |
| Orchestration | 5 | 1 |
| AI / LLM Specific | 6 | 6 |
| Security | 5 | 3 |
| Observability | 5 | 4 |
| **Total** | **35** | **24** |

The AI/LLM Specific category has the highest density of High-frequency patterns. This reflects the Amplified stack's core workload. These six patterns are the first candidates for canonical implementation and open-source publication.

---

## SECTION 4: DIMINISHING RETURNS — WHERE TO STOP

The pattern taxonomy is a tool, not a religion. Every hour spent indexing a pattern that appears once in the codebase is an hour not spent building the product. This section defines, mathematically and operationally, exactly where to stop.

---

### 4.1 The Three Phases

**Phase 1 — High ROI (target first)**

Patterns appearing in 3 or more services. These are the equivalents of `util-hash-content` (7 pipelines), `schema-node-report` (7 pipelines), `guard-unicode-normalise` (6 services). Cross-indexing these patterns delivers immediate, measurable returns: conformance enforcement hits the majority of the codebase, and canonical improvements propagate widely.

- Target: First 15–20 patterns from the taxonomy
- Expected coverage: 60–80% of codebase code touches at least one indexed pattern
- Action: Full treatment — README, instances.yaml, canonical, conformance tests

**Phase 2 — Moderate ROI (do next)**

Patterns appearing in exactly 2 services. Cross-indexing is still worthwhile because any divergence is immediately visible and because a third instance is likely. However, canonical implementations may not yet be stable.

- Target: Next 10–15 patterns
- Action: README and instances.yaml. Canonical deferred until third instance appears.

**Phase 3 — Diminishing ROI (do not cross-index yet)**

Patterns appearing in only 1 service. A single instance is not a pattern — it is an implementation. Cross-indexing it adds overhead without benefit. Flag it in the service's own code comments as a pattern candidate. When a second instance appears, promote it to Phase 2.

- Target: Everything else
- Action: Code comment only: `# PATTERN-CANDIDATE: retry-with-backoff variant`

---

### 4.2 The Rule

**Cross-index when N ≥ 2. Write canonical when N ≥ 3. Open-source when N ≥ 5.**

This is not a guideline. It is the rule. No exceptions without Kaizen Department approval and documented justification.

---

### 4.3 The Four Metrics

These four metrics are the quantitative health indicators for the dual organisation system. They are computed by the pattern-audit tool and reported in the monthly Kaizen review.

**Pattern Coverage**

```
Pattern Coverage = (lines of code touching at least one indexed pattern) / (total lines of code)
```

Target range: **40–60%**. Not 100%. A Pattern Coverage of 90%+ is a symptom of over-indexing. If you're cross-indexing every single-instance utility, your taxonomy is consuming more overhead than it saves in bugs and duplication.

**Pattern Conformance**

```
Pattern Conformance = mean(conformance_score) across all instances in instances.yaml
```

Target: **> 0.85**. A drop below 0.80 triggers a Kaizen review. A drop below 0.70 for any individual instance triggers mandatory remediation within 48 hours (see Section 8).

**Pattern Freshness**

```
Pattern Freshness = (instances audited within past 30 days) / (total instances)
```

Target: **> 80%**. Stale conformance scores are useless. An instance audited 6 months ago may have diverged substantially. Freshness is the metric that keeps the cross-index honest.

**Diminishing Returns Detector**

```
ΔCoverage(new pattern) = coverage after adding pattern − coverage before adding pattern
```

If ΔCoverage < 1.0 percentage point, do not add the pattern. The marginal return is insufficient to justify the taxonomy overhead. This calculation is run before any new Phase 2 or Phase 3 pattern is added to the cross-index.

---

### 4.4 The Warning

> **100% coverage is a trap. The goal is 40–60%. Beyond that, you are spending more on the taxonomy than you are saving in bugs.**

This is not a compromise. It is a mathematical statement. The pattern taxonomy is a tool for managing high-frequency, high-impact patterns. It is not a documentation project for every piece of code ever written. Discipline in what gets indexed is itself a form of engineering excellence.

---

## SECTION 5: THE AUTOMATED REFINEMENT STACK

The dual organisation model does not run on human review alone. Four layers of automated and semi-automated tooling keep the codebase conformant, improving, and growing. Each layer has a distinct remit. They are complementary, not redundant.

---

### 5.1 Layer Architecture

```
Code written
  → Layer 1: Semgrep + SonarQube catch generic issues
  → Layer 2: Copilot handles routine fixes
  → Layer 3: Kaizen guards catch domain-specific issues
  → Layer 4: Pattern taxonomy cross-indexes what was learned
  → Error registry grows
  → Next code is born with the defence built in
```

---

### Layer 1 — Generic Scanning (Free, On Beast)

**Semgrep Community Edition**

Open-source static analysis supporting 30+ languages. Runs entirely on the Beast server — no data leaves the network. Pattern rules are written in YAML and are composable. Semgrep catches: unsafe API usage, hardcoded secrets, SQL injection vectors, known vulnerability patterns, and custom rules for Amplified-specific anti-patterns. Runs as a pre-commit gate and in the Cove pipeline as part of G1 (Structure Gate). Zero cost. Zero data leakage.

**SonarQube Community Edition**

Code quality and limited security rule scanning. Self-hosted in a Docker container on Beast. Provides code smell detection, complexity metrics, duplicate code identification, and test coverage tracking. Runs in the Cove pipeline as part of G2 (Completeness Gate). Its duplicate detection is particularly relevant to the pattern taxonomy: SonarQube will flag structural duplication that the pattern scanner would then cross-index.

Both tools run as pre-commit gates and as pipeline stages. A failure in either blocks the PR. They are the first line of defence and cost nothing beyond infrastructure that already exists.

---

### Layer 2 — GitHub Copilot Coding Agent (£10/month)

Copilot's autonomous coding agent can be assigned routine issues via `@copilot` in GitHub Issues. It works within GitHub Actions, opens PRs for human review, and handles the majority of generic, well-specified improvements.

**Good for:**
- Bug fixes with clear reproduction steps
- Test coverage gaps on standard patterns
- Documentation updates
- Dependency upgrades
- Generic refactoring with clear before/after specification

**Not good for:**
- Domain-specific patterns (Copilot does not know the 96 ERR-IDs)
- FalkorDB Cypher edge cases
- Graphiti UUID patch sequences
- Temporal replay traps
- Amplified-specific conformance scoring

Copilot handles the 80% of routine improvement work. It is not the 20% that matters most. For that, see Layer 3.

---

### Layer 3 — Kaizen Department (Custom, Permanent)

The Kaizen Department is defined fully in CODE-TAXONOMY-AND-KAIZEN-v1. In the context of the dual organisation model, its specific responsibilities are:

- **Error Anticipation Registry enforcement**: Runs against all 96 ERR-IDs and the growing registry. Knows which errors are associated with which patterns. When ERR-DB-003 fires, it knows to check the retry-with-backoff instance in the relevant service.
- **Domain-specific pattern knowledge**: FalkorDB Cypher edge cases, Graphiti UUID patch ordering, Temporal determinism constraints, LiteLLM token accounting errors. None of this is in any off-the-shelf tool.
- **Pattern conformance scoring**: Runs the conformance tests in `.patterns/*/tests/` against all instances. Computes the four metrics from Section 4.3. Reports to the monthly Kaizen review.
- **Canonical improvement proposals**: When a service-level implementation solves a problem better than the current canonical, Kaizen proposes a canonical upgrade and triggers instance re-audit.

Layer 3 is the 20% of the work that produces 80% of the domain-specific value. It cannot be replaced by generic tooling.

---

### Layer 4 — Pattern Cross-Index (This Document)

Layer 4 is not a tool. It is the system that captures what the other three layers learn.

When Layer 1 catches a new class of error, the pattern taxonomy gains a new anti-pattern entry in the relevant pattern's README. When Layer 2 fixes a conformance issue, the fix is reviewed against the canonical — if the canonical was wrong, it is updated. When Layer 3 identifies a new pattern variant appearing in a second service, the pattern index gains a new entry.

The compound effect: every fix makes the next implementation harder to get wrong. The error registry grows from every incident. The canonical implementations improve from every divergence. The taxonomy becomes more complete with every deployment cycle.

This is the Pudding Technique applied to code. The ABC discovery model — where A knows B, B knows C, but nobody has yet connected A to C — becomes the engine of cross-pattern learning. A problem solved in the FalkorDB client teaches the LiteLLM client. A canonical improved for the Graphiti ingest pipeline improves every pipeline that shares the pattern.

---

## SECTION 6: THE GITHUB OPEN-SOURCE STRATEGY

The dual organisation model generates genuine intellectual property. The pattern taxonomy, the conformance test framework, the canonical implementations, and the CLI tooling are valuable to any team building AI infrastructure on similar stacks. Publishing them serves Amplified's authority-building goals, attracts talent, and establishes domain leadership in a space nobody has claimed.

---

### 6.1 What to Open Source — The amplified-patterns Repo

The following are published under MIT licence:

- The `.patterns/` directory structure and organisation tooling
- Pattern README templates and the conformance test framework
- The full pattern taxonomy (Section 3 of this document)
- Example canonical implementations in generic form (not Amplified-specific)
- A `pattern-scan` CLI tool: scans a codebase, identifies files that match known patterns by structural analysis, proposes cross-index entries
- A `pattern-audit` CLI tool: takes a codebase and instances.yaml, runs conformance tests, reports scores and drift
- A `pattern-init` CLI tool: scaffolds a new pattern directory from templates

These publications do not reveal Amplified's internal architecture. The canonical implementations are generic. The tooling works on any codebase. The taxonomy is abstract.

---

### 6.2 What to Keep Private

The following are never published:

- Amplified's actual service code (View 1) in any form
- Client-specific implementations
- Internal instances.yaml files — they reveal the service architecture
- HoundDog engine code in any form
- API keys, credentials, client data
- Proprietary business logic
- The full Error Anticipation Registry (96 ERR-IDs reveal the failure history)

The rule: if it reveals where we've been, what we've built, or what we know about a client, it stays private.

---

### 6.3 The Public Repository Structure

```
amplified-patterns/
├── README.md
├── LICENSE (MIT)
├── taxonomy/
│   ├── resilience/
│   │   ├── retry-with-backoff/
│   │   ├── circuit-breaker/
│   │   ├── dead-letter-queue/
│   │   ├── saga-compensate/
│   │   ├── graceful-degrade/
│   │   ├── bulkhead-isolate/
│   │   └── timeout-with-fallback/
│   ├── performance/
│   ├── data-integrity/
│   ├── orchestration/
│   ├── ai-llm/
│   ├── security/
│   └── observability/
├── tools/
│   ├── pattern-scan/
│   │   ├── README.md
│   │   └── src/
│   ├── pattern-audit/
│   │   ├── README.md
│   │   └── src/
│   └── pattern-init/
│       ├── README.md
│       └── src/
├── templates/
│   ├── pattern-readme.md
│   ├── instances.yaml.template
│   └── conformance-test.template.py
├── examples/
│   ├── retry-with-backoff/
│   │   ├── README.md
│   │   ├── canonical.py
│   │   └── tests/
│   ├── circuit-breaker/
│   │   ├── README.md
│   │   ├── canonical.py
│   │   └── tests/
│   └── idempotent-write/
│       ├── README.md
│       ├── canonical.py
│       └── tests/
└── docs/
    ├── philosophy.md
    ├── getting-started.md
    └── contributing.md
```

---

### 6.4 Authority-Building Roadmap

**Month 1**
Publish the taxonomy and five example patterns with canonical implementations. The five patterns chosen for launch should be the highest-frequency AI/LLM patterns: `prompt-template-inject`, `token-budget-guard`, `hallucination-guard`, `retry-with-backoff`, `idempotent-write`. These demonstrate immediately that this is not a theoretical project — it is operational code.

**Month 2**
Publish the `pattern-scan` CLI tool. A tool that scans a codebase and reports which patterns it finds is immediately useful to any engineering team. It is also a hook: once teams know which patterns they have, they want to know how well-implemented those patterns are.

**Month 3**
Write three technical articles for dev.to and Medium. Topics: (1) why your codebase implements the same retry logic in five different places and how to fix it; (2) the case for a pattern taxonomy in AI infrastructure code; (3) how to measure pattern conformance with a score instead of a code review. These articles drive discovery of the repo and establish Ewan's voice in the AI engineering space.

**Months 4–6**
Engage with the LangChain, Temporal, FalkorDB, and LiteLLM communities. Submit ecosystem-specific pattern contributions: `temporal-versioned-patch` to the Temporal community, `model-fallback-chain` to the LiteLLM community, `embedding-cache` to any vector database community. Becoming a contributor to adjacent open-source projects builds trust and visibility simultaneously.

**Month 6 and Beyond**
Open the repository to community contributions. Establish contribution criteria (patterns must have canonical implementation, conformance tests, and instances.yaml template). Build a contributor base. The repository becomes a living catalogue of AI infrastructure patterns — one that no individual team could build alone.

---

### 6.5 Why This Builds Authority

There is no existing open-source project that does pattern-indexed AI/SMB infrastructure code with conformance scoring and automated refinement. The amplified-patterns repository is the first. Being first, in the right community, with production-quality work, is the fastest path to domain authority for an AI consultancy.

The repository also serves as a perpetual demonstration of Amplified's engineering standards. Every client who looks at the public repo sees systematic rigour — canonical implementations, conformance tests, structured improvement cycles. It answers the question "how do we know Amplified builds good code?" before it is asked.

---

## SECTION 7: KAIZEN INTEGRATION

The Kaizen Department (defined fully in CODE-TAXONOMY-AND-KAIZEN-v1) operates the dual organisation system on a permanent, scheduled basis. This section defines the specific Kaizen responsibilities for the pattern taxonomy.

---

### 7.1 Monthly Pattern Audit

Every 30 days, the Kaizen Department runs the full pattern audit:

1. **Discovery scan**: Run `pattern-scan` against the full codebase. Identify any View 1 files that implement a known pattern but are not yet listed in instances.yaml. Add them. Compute initial conformance score.

2. **Conformance refresh**: Run `pattern-audit` against all existing instances. Update conformance scores. Flag any instance whose score has dropped below 0.85 for investigation. Flag any instance whose score has dropped below 0.70 for mandatory remediation.

3. **Freshness update**: Update `last_audit` dates in all instances.yaml files. Compute Pattern Freshness metric. If below 80%, escalate to next monthly priority.

4. **Pattern Freshness report**: Report the four metrics (Coverage, Conformance, Freshness, Diminishing Returns) to the engineering lead. Archive the report.

---

### 7.2 Conformance Drift Detection

Between monthly audits, conformance drift is detected automatically. When a PR touches a file that is listed in an instances.yaml, the pre-commit hook re-runs the conformance tests for that instance. If the score drops, the PR includes an automatic comment with the new score and a diff against the canonical.

Drift is not automatically blocked (unless it crosses below 0.70). But it is always visible. Invisible drift is how codebases rot. Visible drift is a decision: acceptable divergence with documented justification, or a defect requiring fix.

---

### 7.3 Pattern Promotion

The pattern promotion workflow is triggered when:

- A `PATTERN-CANDIDATE` comment in a single service file now matches an implementation in a second service

The Kaizen Department runs the promotion workflow:
1. Create `.patterns/<pattern-name>/` directory
2. Write README.md with intent, when-to-use, when-not-to-use, and conformance criteria
3. Create instances.yaml with both known instances
4. Compute initial conformance scores
5. Propose canonical.py based on the better-scoring instance
6. Create conformance tests

Pattern promotion from Phase 3 to Phase 2 or Phase 1 is a Kaizen task with a 48-hour SLA.

---

### 7.4 Pattern Retirement

When all instances of a pattern are removed from the codebase:

1. Archive the `.patterns/<pattern-name>/` directory to `.patterns/_archive/`
2. Update the taxonomy table with retirement date and reason
3. Do not delete. Archived patterns are institutional memory. A pattern retired today may be needed again when a new service is added.

---

### 7.5 SLA Alignment with CODE-TAXONOMY

All Kaizen SLAs from CODE-TAXONOMY-AND-KAIZEN-v1 apply without modification:

| Priority | Condition | SLA |
|---|---|---|
| Critical | Conformance breach on data-loss-prevention pattern | 24 hours |
| High | Conformance score below 0.70 on any instance | 48 hours |
| Medium | Conformance score below 0.85 on any instance | Next Kaizen cycle |
| Low | New pattern candidate identified | Next monthly audit |
| Verification | Any remediation before marking resolved | 7 clean days |

The 7-clean-days verification rule applies to pattern conformance just as it applies to ERR-ID remediation. A fix that passes conformance tests today must pass for 7 consecutive days before the issue is closed. Regressions happen. The verification window catches them.

---

## SECTION 8: ENFORCEMENT RULES

These rules are constitutional. They do not change for convenience, urgency, or preference. Mathematics decides.

---

### 8.1 Pre-Coding Requirements

**Every new module MUST check the pattern taxonomy before writing implementation code.**

This check takes five minutes. Opening the `.patterns/` directory, searching the taxonomy table, and reading a pattern README is not overhead — it is the work. Writing code that duplicates an existing pattern without checking is a process violation, not a minor oversight.

If an existing pattern matches the intended behaviour, the canonical implementation is the starting point. Not a blank file. Not a copy from a previous project. The canonical.

---

### 8.2 Justified Exception Process

If a developer has a documented reason to diverge from a canonical implementation, the following process applies:

1. Document the justification in the PR description with specific technical reasoning
2. Add an entry to instances.yaml with `divergence_reason` field populated
3. Reference the relevant ERR-ID if the divergence is driven by a known error class
4. Tag the Kaizen Department for review within the PR
5. Kaizen approves, requests modification, or proposes a canonical update

An undocumented divergence is a conformance defect, regardless of whether the code works.

---

### 8.3 New Pattern Intake

New patterns do not self-certify. The intake process applies:

1. Pattern must have N ≥ 2 instances (or a compelling case for N = 1, which is rare)
2. Developer proposes pattern in a Kaizen issue with: name, intent, known instances, proposed canonical
3. Kaizen Department reviews and either approves, rejects, or requests modification
4. On approval: full pattern directory is created per the structure in Section 2.3
5. Initial conformance tests are written and pass against both known instances

A pattern proposed without conformance tests is not approved.

---

### 8.4 Conformance Score Thresholds

| Score Range | Status | Required Action |
|---|---|---|
| 0.90 – 1.00 | Exemplary | No action required |
| 0.85 – 0.89 | Conformant | Scheduled improvement at next Kaizen cycle |
| 0.70 – 0.84 | Below target | Investigation and improvement plan within 5 days |
| < 0.70 | Non-conformant | Mandatory refactor within 48 hours |

The 0.70 threshold is not negotiable. A codebase with instances below 0.70 is a codebase with known defects in its most critical patterns. This is not acceptable.

---

### 8.5 The Single Source of Truth

The `.patterns/` directory and its instances.yaml files are the single source of truth for how Amplified implements any given pattern. If the canonical says use exponential backoff with jitter, every instance uses exponential backoff with jitter unless there is a documented, Kaizen-approved justification.

No verbal agreement, no PR comment, no Slack message overrides the pattern index. If the change is not in the canonical and instances.yaml, it did not happen.

---

### 8.6 Constitutional Immutability

These rules do not change. They are constitutional.

Mathematics decides. Not vibes. Not urgency. Not "we'll fix it later." The pattern index is maintained, the conformance scores are enforced, the Kaizen Department operates on schedule, and the canonical implementations improve over time.

Code lives twice. Once where it works. Once where it teaches. This document ensures that both lives are rigorously managed.

---

## APPENDIX A: MODULE TYPE — PATTERN AFFINITY MAP

Reference table showing which module types (from CODE-TAXONOMY-AND-KAIZEN-v1) most commonly implement which pattern categories. Use when determining which patterns to check before writing a new module.

| Module Type | Primary Pattern Categories | Notes |
|---|---|---|
| guard | Security, Data Integrity, Resilience | Always check guard-lint-reject and input-sanitise |
| adapter | Performance, Resilience | Check connection-pool-with-drain for external adapters |
| pipeline | Data Integrity, Orchestration, Performance | Check idempotent-write and batch-with-checkpoint first |
| monitor | Observability, Resilience | health-check-probe is near-universal for this type |
| gate | Security, Data Integrity | schema-validate-then-write applies to almost all gates |
| transform | Data Integrity, Security | input-sanitise applies to any transform touching external input |
| test | — | Pattern conformance tests live in tests/; not subject to taxonomy |
| hook | Observability, Security | structured-log-emit and auth-token-refresh common here |
| client | Resilience, Performance | retry-with-backoff and circuit-breaker are near-universal |
| worker | Resilience, Orchestration | dead-letter-queue and bulkhead-isolate commonly needed |
| prompt | AI/LLM Specific | prompt-template-inject and token-budget-guard are mandatory checks |
| rubric | AI/LLM Specific | response-validate and hallucination-guard apply universally |
| config | Performance | connection-pool-with-drain configuration concerns |
| util | Performance, Data Integrity | content-hash-dedup and cache-aside are common here |
| schema | Data Integrity | schema-validate-then-write is the primary pattern |
| workflow | Orchestration, Resilience | saga-compensate and temporal-versioned-patch are critical checks |
| activity | Orchestration, Data Integrity | idempotent-write is mandatory for all Temporal activities |
| mcp-server | Security, Observability | auth-token-refresh and structured-log-emit always apply |
| fixture | — | Test fixtures are not subject to taxonomy; they support conformance tests |
| migration | Data Integrity | write-ahead-log and optimistic-lock apply to schema migrations |

---

## APPENDIX B: DOCUMENT VERSION HISTORY

| Version | Date | Author | Summary |
|---|---|---|---|
| v1 | 2026-03-17 | Ewan Bramley | Initial constitutional specification |

---

*Amplified Partners — Constitutional Document. Maintained by the Kaizen Department. Cross-referenced with FILE-NAMING-CONVENTION-v1, VALIDATION-METHODOLOGY-v2, and CODE-TAXONOMY-AND-KAIZEN-v1.*

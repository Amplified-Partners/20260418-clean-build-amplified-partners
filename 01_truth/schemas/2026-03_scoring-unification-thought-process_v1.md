---
title: "Scoring Unification Thought Process"
id: "scoring-unification-thought-process"
version: 1
created: 2026-04-25
last_validated: 2026-04-25
type: document
topic_type: reference
status: imported
source_file: "SCORING-UNIFICATION-THOUGHT-PROCESS.md"
signed_by: "Devon, 2026-04-25, devin-992682c244cf444f91e0a516498afbfd"
---

# Amplified Partners — Scoring Unification Hypothesis: Thought Process

---

**Document ID:** `SCORING-UNIFICATION-THOUGHT-PROCESS`
**Status:** Reference — Companion to `SCORING-UNIFICATION-HYPOTHESIS-v2`
**Audience:** AI agents implementing, maintaining, or extending the Amplified system
**Last updated:** 2026-03-17

---

## 1. WHAT THIS DOCUMENT IS FOR

This is the reasoning trail behind the Scoring Unification Hypothesis. It exists so that future AI agents working on the Amplified system understand **why** decisions were made, not just **what** was decided.

The hypothesis document (`SCORING-UNIFICATION-HYPOTHESIS-v2`) tells you what is proposed. This document tells you how the proposal emerged, what evidence was weighed, what was fixed during review, what the risks are, and where the evidence is thin. If you are implementing the scoring layer, read this first. If you are reviewing or extending the hypothesis, read this alongside the hypothesis itself.

This document is honest about uncertainty. Where we know things, we say so. Where we are guessing, we say that too. Where we got things wrong and fixed them, we document the fix and the reason. The goal is to give you — an AI agent arriving fresh to this system — the same understanding that accumulated during the research and review process, so that you do not repeat our mistakes or misunderstand our intentions.

---

## 2. THE ORIGIN — HOW THE HYPOTHESIS EMERGED

The Scoring Unification Hypothesis was not designed top-down. It emerged from a sequence of observations, each one building on the one before it. No step was planned. The architecture surfaced through honest examination of what the system's primitives could do.

### Step 1: The Compressed Coding System

The starting point was `ATTRIBUTION-AND-CURATION-v1`, which defines a compressed coding system for data labelling. The core idea: every data object in the system carries short, structured codes (like `FIN-REGULATORY` or `RES-METHODOLOGY`) that classify its domain, type, and attributes. These codes are stored internally in compressed form and expanded to human-readable labels on output.

The original purpose was retrieval and taxonomy. Codes make things findable. Codes make things classifiable. This was Section 3 of `ATTRIBUTION-AND-CURATION-v1` — a practical system for organising knowledge across FalkorDB and the vector store.

### Step 2: Ewan Spotted the Cross-Database Pattern

Ewan observed that the compressed coding pattern was not specific to FalkorDB and the vector store. It could apply to **all** databases in the system. Every database has a Curator. Every Curator logs operations. If every operation carries codes, then every database becomes code-aware. The coding system was not just a taxonomy tool — it was a universal labelling mechanism.

This was the first cascade: from "codes for retrieval" to "codes everywhere."

### Step 3: Codes Are Countable, and Countable Becomes Scorable

Then Ewan spotted the scoring angle. His observation: "it's a scoring system as well." The reasoning was direct:

- If everything carries codes, codes are **countable**.
- If codes are countable, you can measure their frequency, co-occurrence, decay, and distribution.
- Measurements are **scores**.
- Therefore, the coding system is also a scoring system — latent in the data, requiring only extraction.

This was not a leap. It was a logical consequence. Medical informatics had already proven it with SNOMED CT. IBM had proven it with reuse metrics. Knowledge graph researchers had proven it with entity popularity. The insight was recognising that the same pattern applied to our compressed codes.

### Step 4: Scoring Outputs Means You Can Score the Rubrics

The next cascade: if you can score outputs using codes, you can score the **rubrics that evaluate those outputs**. The 7 gates (G1–G7) in `VALIDATION-METHODOLOGY-v2` are the rubric. If we measure which gates are effective (catch real problems) and which are not (pass everything or catch nothing), we are meta-scoring the rubric.

This was reinforced by finding OpenRS (Open Rubric System), which implements exactly this pattern: a meta-rubric that governs rubric instantiation, with rubrics scored for effectiveness and refined through error analysis. SHSU had published an actual rubric for scoring rubrics. Sopact was doing longitudinal rubric validation against programme outcomes. The evidence said: meta-scoring is not speculative. It is an active research area with proven results.

### Step 5: Rubric Weightings Should Adapt to Context

The final cascade: if rubrics can be scored, their weightings should adapt to what you are trying to evaluate. A research lens should weight attribution depth heavily. An infrastructure lens should weight technical compliance heavily. Same gates, different priorities. This is lens-adaptive evaluation.

The theoretical foundation was Brunswik's lens model (1956), which describes how different environments make different cues more or less predictive. The practical implementation was already happening: Vertex AI's adaptive rubrics, OpenRS's domain meta rubrics, and the RAISE framework's cross-domain evaluation all demonstrated that context-dependent weighting produces measurably better results.

### The Emergence Pattern

Each insight built on the previous one:

```
Compressed codes (for retrieval)
  → Codes everywhere (universal labelling)
    → Codes are countable (therefore scorable)
      → Rubrics can be scored (meta-scoring)
        → Rubric weights adapt to context (lens-adaptive evaluation)
```

None of this was planned. The architecture emerged from asking "what else can these codes do?" at each step. This matters because it means the hypothesis is not a top-down design imposed on the system — it is a bottom-up observation about what the existing primitives already support.

---

## 3. WHY THIS IS A HYPOTHESIS, NOT A STANDARD

### The Evidence Gradient

The Amplified system has two categories of documents: constitutional standards (things we do) and hypotheses (things we are investigating). The scoring unification is a hypothesis, and it must stay a hypothesis until validated. Here is why.

**The individual pieces have strong evidence:**

- Codes as scores: SNOMED CT, IBM reuse metrics, knowledge graph entity popularity, and enterprise knowledge retrieval all confirm that coded data enables scoring. Evidence grade: **STRONG**.
- Rubric meta-scoring: OpenRS (+5.1 over scalar baselines), SHSU (literal rubric for rubrics), Sopact (longitudinal rubric validation). Evidence grade: **STRONG**.
- Lens-adaptive evaluation: Brunswik lens model (theoretical foundation since 1956), Vertex AI adaptive rubrics (practical implementation), RAISE (cross-domain demonstration). Evidence grade: **MODERATE**.

**The integration is novel:**

No existing system connects all three through compressed codes in a single self-improving architecture. SNOMED CT comes closest — its codes feed quality metrics, which inform governance decisions, which refine the hierarchy — but that loop operates across different organisations, timescales, and governance structures. It is not one system.

Our claim is that connecting the pieces through a shared mechanism (compressed codes) creates a flywheel. This is a hypothesis because the assembly is untested, even though the individual pieces are proven.

### Ewan's Instruction

Ewan's instruction was explicit: "it's going to be a hypothesis, because this is so important. We've got to really get everybody's point of view on it." This was not hesitation — it was discipline. The scoring layer, if it works, would affect every part of the system. Getting it wrong would compound across every database, every gate, every Kaizen cycle. The stakes demanded rigour.

The document must stay marked as hypothesis until the 4-phase validation plan produces results. This is not bureaucracy. It is the system protecting itself from premature commitment.

### Even Failure Is Useful

This is worth emphasising: even if the hypothesis is refuted, each validation phase produces independently useful intelligence.

| Phase | What You Get Even If It Fails |
|-------|-------------------------------|
| Phase 1: Extract Metrics | Code-level metrics we don't currently have — useful for Kaizen regardless |
| Phase 2: Gate Audit | Knowledge of which gates are effective and which are decorative — useful for validation methodology regardless |
| Phase 3: Lens Prototype | Evidence on whether context-adaptive evaluation helps — simplifies architecture if it doesn't |
| Phase 4: Flywheel Test | Knowledge of where the loop breaks — tells us which layers are independently valuable |

The validation plan is designed so that stopping at any phase still produces value. This was deliberate. Hypothesis-driven development means that negative results are results, not failures.

---

## 4. THE EVIDENCE STRATEGY

### How Evidence Was Gathered

The evidence base was assembled by searching for parallel systems across multiple domains. The search was intentionally broad because the hypothesis makes a cross-domain claim (codes-as-scores works universally), so the evidence needed to come from multiple independent domains to be credible.

**Domains searched:**

| Domain | What We Found | Relevance |
|--------|--------------|-----------|
| Medical informatics | SNOMED CT — 370,000+ clinical concepts, codes used for quality metrics at national scale | Direct parallel: codes → frequency → quality measurement |
| Software engineering | IBM reuse metrics — faceted classification codes → Reuse Percent, Cost Avoidance, Value Added | Direct parallel: faceted codes → economic metrics |
| Knowledge graphs | EP-TWCS — entity popularity as quality signal, validated on NELL, YAGO, MOVIE | Direct parallel: access frequency → quality assessment |
| LLM evaluation | OpenRS — meta-rubric with evolutionary refinement, +5.1 over scalar baselines | Direct parallel: rubric meta-scoring with measurable improvement |
| Educational assessment | SHSU — literal rubric for scoring rubrics, 4-point scale across 10 dimensions | Direct parallel: meta-assessment in production use |
| Impact measurement | Sopact — longitudinal rubric validation through persistent IDs and outcome tracking | Direct parallel: outcome-based rubric refinement |
| Cognitive science | Brunswik lens model (1956), diffusion lens model (2026) | Theoretical foundation for lens-adaptive evaluation |
| Aerospace | Aerospace Corp TOR-2015-02544 — context-dependent inspection weighting across 10 studies | Direct parallel: same criteria, different weights based on evaluation context |
| Aviation regulation | FAA risk-based inspection — same criteria, different intensity based on risk lens | Direct parallel: lens-adaptive enforcement |
| Internal auditing | AHP-weighted risk-based auditing — weights change per auditable area | Direct parallel: context-adaptive evaluation weighting |
| Self-improvement theory | arXiv:2601.05280v2 — formal convergence proof for self-improving loops | Mathematical foundation for flywheel convergence conditions |
| Quality management | Deming's 14 Points — constancy of purpose as convergence condition | Theoretical grounding for "gates don't change" |

### How Evidence Was Graded

Every claim in the hypothesis was graded using four levels:

- **STRONG** — Multiple independent confirmations from different domains
- **MODERATE** — Some evidence exists, needs more validation
- **HYPOTHESIS** — Logical but unproven
- **INSUFFICIENT** — Looked but did not find enough

This grading was applied per sub-claim, not to the hypothesis as a whole. The result: individual pieces graded STRONG or MODERATE, the integration graded HYPOTHESIS. This honest differentiation is the whole point. Agents reading the hypothesis should know exactly where the evidence is solid and where it is thin.

### Citation Verification

Every citation URL was verified to be real and accessible. This matters because fabricated citations erode trust in the entire document. If a URL was broken or the source said something different from what we claimed, we fixed it. If we could not find a primary source, we said so.

### The Heterogeneous Evidence Base

The evidence comes from very different domains. This is both a strength and a weakness:

**Strength:** Multiple independent domains confirming the same patterns (codes → metrics → improvement) provides strong convergent evidence. If only medical informatics showed this, you could argue it is domain-specific. When medicine, software engineering, knowledge graphs, LLM evaluation, educational assessment, aerospace, and cognitive science all show variants of the same pattern, the underlying principle is likely real.

**Weakness:** Transfer between domains is itself a hypothesis. The fact that codes-as-scores works in healthcare (SNOMED CT) does not guarantee it works in knowledge management. The fact that meta-rubrics work in LLM evaluation (OpenRS) does not guarantee they work for our gate system. Each domain has its own conventions, constraints, and failure modes. The validation plan is designed to test transfer in our specific context, not assume it.

---

## 5. THE CRITICAL DEPENDENCIES

The hypothesis does not exist in isolation. It depends on specific capabilities in the existing system. If any of these dependencies breaks, the hypothesis breaks with it.

### Dependency 1: The Compressed Coding System Must Be Implemented First

Without codes, there is nothing to score. The entire scoring layer derives its metrics from code assignments: frequency, co-occurrence, decay, gate pass rates per code. No codes means no metrics.

This depends on `ATTRIBUTION-AND-CURATION-v1` Section 3. The compressed coding system defines the vocabulary, the assignment rules, and the audit requirements. If you are implementing the scoring layer, verify that the coding system is operational before you start.

### Dependency 2: The Curator Must Log Everything

All scoring metrics are computed from Curator audit logs. Reuse frequency comes from counting code assignments in logs. Decay rate comes from timestamps in logs. Gate pass rates come from gate evaluation records in logs.

If Curators do not log comprehensively, the scoring layer has no data. This is not a suggestion — it is a hard dependency. Every code assignment, every gate evaluation, every write operation must be logged with enough metadata to compute the metrics defined in Section 1.5 of the hypothesis.

Do not optimise Curator logs for storage. The logs are the data source for the scoring layer. A Curator that logs efficiently but incompletely is worse than a Curator that logs verbosely.

### Dependency 3: The Gates Must Remain Constitutional

This is the mathematical dependency, and it is the most important one.

The formal convergence proof from arXiv:2601.05280v2 ("On the Limits of Self-Improving in Large Language Models," January 2026) shows that self-improving loops converge to the true distribution **only** when the external evaluator maintains a persistent exogenous signal (α_t ≥ α* > 0). If the exogenous signal vanishes (α_t → 0), the system degenerates to a fixed point — it converges to its own biases rather than to truth.

In the Amplified system, the 7 gates (G1–G7) are the persistent exogenous signal. They are the external evaluator that prevents degenerate convergence. If gates are softened to improve pass rates, the convergence condition breaks. If gates are removed because they seem redundant, the external signal weakens. If gates are made adaptive (changing based on what the system produces), they cease to be exogenous.

"These gates do not change" is not stubbornness. It is the convergence condition. This is now proven mathematics, not intuition.

The paper also proves that multi-model ensembles (analogous to our multi-agent architecture) converge to a "consensus reality" of the initial models when α_t → 0. Without external grounding, even diverse agents converge to shared biases. The gates are what prevent this.

### Dependency 4: Kaizen Must Be the Improvement Mechanism

The scoring layer identifies **what** to improve. Kaizen executes **how** to improve it. Without Kaizen, the loop does not close. Code-level metrics sit in a dashboard and nothing happens.

The Kaizen Department (defined in `CODE-TAXONOMY-AND-KAIZEN-v1` Section 3) provides the agents, the schedules, and the processes that act on scoring intelligence. The Kaizen Agent runs daily. The Chaos Agent tests defences nightly. The Recall Monitor checks vector search quality every 6 hours. These are the mechanisms that translate scoring data into system improvements.

If you are implementing the scoring layer without Kaizen integration, you are building a dashboard, not a flywheel.

### Dependency 5: Curators Must Remain the Only Database Writers

If any agent writes directly to a database (bypassing the Curator), it bypasses the audit log. A write without an audit log entry is invisible to the scoring layer. Invisible writes corrupt every metric that depends on completeness: frequency counts are wrong, co-occurrence matrices are incomplete, decay rates are inaccurate.

This is the architectural reason behind the Curator monopoly in `ATTRIBUTION-AND-CURATION-v1`: "Every database has exactly one designated Curator Agent. No other process reads from or writes to that database directly." The scoring layer turns this from a governance principle into a mathematical requirement. Every unlogged write is a lost data point.

---

## 6. THE KNOWN RISKS AND HONEST GAPS

### Risk 1: Goodhart's Law

"When a measure becomes a target, it ceases to be a good measure."

If agents learn that high code frequency is valued, they may over-apply popular codes. If gate pass rates become targets, criteria may be softened. If bridge scores are rewarded, agents may create spurious cross-domain connections. Every scoring system is vulnerable to gaming. This is not a theoretical concern — healthcare upcoding (gaming diagnosis codes for higher reimbursement) is a multi-billion-dollar problem.

**Mitigations identified (from v2 research):**

- **Multi-metric measurement** (CNA report, 2022): Don't rely on a few metrics. Measure comprehensively so gaming one metric degrades another. The scoring layer's multiple interacting metrics (frequency × decay, co-occurrence × gate pass rate, velocity × attribution depth) create structural coupling that resists single-metric gaming.
- **Peer comparison** (healthcare upcoding detection): Compare each agent's code assignment patterns against peers. Outliers are flagged automatically.
- **Curator-controlled data** (Amplified architecture): Agents cannot write directly to databases. The Curator is a disinterested party that logs what actually happened, not what agents claim happened. This is the CNA report's recommendation to "collect data from disinterested parties" implemented architecturally.
- **Multi-dimensional anomaly detection** (healthcare fraud detection): Use multiple signals simultaneously — frequency distribution, cost patterns, documentation consistency. No single metric is gamed without triggering another.

**Honest assessment:** These mitigations reduce risk but do not eliminate it. Goodhart's Law is a permanent concern, not a solvable problem. The scoring layer must be monitored for gaming continuously, not just at deployment. This is a cost of having a scoring system.

### Risk 2: Cold Start

New domains have no history. No frequency data. No co-occurrence patterns. No gate pass rates. The scoring layer is most useful where we have the most data — and least useful where we are exploring new territory. This is the opposite of what we might want.

**Bootstrapping strategies identified (from v2 research):**

- **Transfer from adjacent domains** (BOLT-K, WWW 2019): Bootstrap new domain ontologies by transferring knowledge from established, related domains. Their LSTM-based framework achieved >75% accuracy in identifying concept pairs via transfer.
- **Iterative enrichment** (JMIR, March 2026): An LLM-assisted SNOMED CT mapping tool that starts with syntactic matching, falls back to semantic similarity, and iteratively enriches its mapping database with validated results. Each validated mapping improves the next. Reduced manual mapping workload by up to 90%.
- **Meta-learning**: Learn the pattern of how to assign codes, not just the codes themselves. Apply learned assignment patterns to new domains even before domain-specific data accumulates.

**Honest assessment:** These strategies help but don't eliminate the cold start problem. The practical recommendation is: start with domains that have the most existing data. Use their code patterns to bootstrap metrics. Expand to new domains only after the scoring layer has proven stable in core domains.

### Risk 3: The Flywheel May Not Turn

Each piece works independently, but the complete loop (codes → scoring → rubric → lens → codes) may not produce net improvement. Possible failure modes:

- The loop converges to a fixed point quickly and then provides no further improvement.
- The loop oscillates rather than converging — improvements in one layer cause regressions in another.
- Improvements in one layer are too small to propagate meaningfully to the next.
- The overhead of running the loop exceeds the value of the improvements it produces.

**Only Phase 4 of the validation plan can test this.** This is a 3-month experiment. There is no shortcut. The theoretical basis for convergence exists (arXiv:2601.05280v2 proves that persistent external signal enables convergence), but theory is not measurement. The flywheel either turns or it doesn't, and only observation will tell us.

### Risk 4: Overhead

Computing metrics continuously may conflict with SLAs. Every code assignment triggers metric recomputation. Every metric change potentially triggers rubric re-evaluation. The cascade could be expensive.

**Our suspicion:** The overhead is manageable because the scoring layer reads from audit logs (which already exist and are written asynchronously) and writes to metric stores (which can also be asynchronous). The scoring layer never sits in the critical path of a user-facing operation. But suspicion is not measurement. Phase 1 of the validation plan will reveal the computational cost of metric extraction.

### Risk 5: Scale Effects

We don't know if we have enough data for statistically meaningful metrics. If the system has hundreds of codes and thousands of nodes, co-occurrence matrices and gate pass rate comparisons may be statistically meaningful. If it has fewer, the metrics may be noise. Conversely, if the system grows to millions of nodes, maintaining the full co-occurrence matrix may become computationally expensive.

Phase 1 of the validation plan will answer this. It is a read-only analysis of existing data. Low risk, high information value.

---

## 7. THE REVIEW PROCESS — WHAT WE FIXED AND WHY

The hypothesis document went through a v1 → v2 review cycle. This section documents what was wrong in v1 and how it was corrected. Transparency about corrections is not embarrassing — it is how trust is built.

### Fix 1: Fabricated Gate Names

**Problem:** v1 used gate names in the lens examples and worked example (Section 3.7 and 4.4) that did not match the actual gates in `VALIDATION-METHODOLOGY-v2`. The v1 examples used names like `G1_source_verification`, `G2_format_compliance`, `G3_attribution_depth`, etc. The actual gates are:

| Gate | Actual Name | v1's Fabricated Name |
|------|-------------|---------------------|
| G1 | Structure | G1_source_verification |
| G2 | Label Validity (+ G2b Inter-Rater) | G2_format_compliance |
| G3 | Rubric & Benchmark | G3_attribution_depth |
| G4 | Match Quality | G4_internal_consistency |
| G5 | Recipe + Scoring | G5_terminology |
| G6 | Test + INTENTLOGIC | G6_completeness |
| G7 | Final Boss | G7_freshness |

**Why it mattered:** An AI agent reading the v1 lens examples would implement lens weightings against gates that don't exist. The examples would compile but would not connect to the actual validation system. Fabricated gate names are worse than no examples — they actively mislead.

**Fix:** All lens examples and the worked example were updated to use the actual gate names: G1: Structure, G2: Label Validity, G3: Rubric & Benchmark, G4: Match Quality, G5: Recipe + Scoring, G6: Test + INTENTLOGIC, G7: Final Boss.

### Fix 2: Blackhurst et al. Paper Mischaracterised

**Problem:** v1 described the Blackhurst et al. (2024) paper in *Frontiers in Psychology* as "a review" of the Brunswik lens model. It is not a review. It is an application paper about deception detection that uses the Brunswik lens model as a framework for understanding how deception cues are utilised by judges.

**Why it mattered:** Calling an application paper "a review" misrepresents its scope and authority. A review surveys the field; an application paper demonstrates usage in a specific context. The citation was still valid (the paper does describe the lens model), but the characterisation was wrong.

**Fix:** Corrected the description to accurately reflect the paper's nature: an application paper about deception detection that employs the Brunswik lens model as its analytical framework.

### Fix 3: Non-LLM Evidence for Lens-Adaptive Evaluation

**Problem:** v1's evidence for lens-adaptive evaluation came primarily from LLM evaluation contexts (OpenRS, Vertex AI, RAISE). A sceptic could argue that lens-adaptive evaluation is specific to LLM evaluation and does not generalise to other domains. The evidence base was too narrow for a general claim.

**Why it mattered:** The hypothesis claims that lens-adaptive evaluation is a general principle. That claim requires evidence from outside LLM evaluation.

**Fix:** Added three non-LLM sources from the v2 research:

- **Aerospace Corp (TOR-2015-02544, 2015):** Context-dependent inspection weighting across 10 studies. The same 10 evaluation criteria, with weights that shift dramatically based on whether the evaluation context is manufacturing, inspection, or data-driven management. Inspector variability and escape detection get 45% weight for inspection contexts vs. 20% for manufacturing contexts. Same criteria, different lens.
- **FAA Risk-Based Decision Making:** Different inspection frequencies based on risk classification. High-risk manufacturers inspected every 3 months; low-risk every 3 years. Same criteria, different intensity based on risk lens.
- **AHP-weighted Risk-Based Internal Auditing (Annals of Operations Research, 2023):** Multi-objective optimisation where weights are computed per auditable unit based on risk profiles. Risk Score = Σ(weight × rating), where weights change per auditable area.

These three sources demonstrate lens-adaptive evaluation in aerospace manufacturing, aviation regulation, and internal auditing — none of which involve LLMs.

### Fix 4: Goodhart's Law Mitigations

**Problem:** v1 identified Goodhart's Law as a risk (Section 4.6) but cited no specific mitigations. It said "the mitigation is to score at multiple levels" without referencing any system that actually does this.

**Why it mattered:** Identifying a risk without proposing mitigations is observation, not engineering. Agents reading v1 would know gaming is a risk but would have no guidance on how to defend against it.

**Fix:** Added specific mitigation patterns from three sources:

- CNA report (2022): Seven systematic mitigations including multi-metric measurement, peer comparison, randomised measures, post hoc measures, and red teaming.
- Healthcare upcoding detection: Multi-dimensional anomaly detection using frequency distribution, cost patterns, documentation consistency, and follow-up evasion as coupled signals.
- Healthcare fraud detection (BMC Medical Informatics, 2024): Unsupervised association rule mining on diagnosis codes, procedure codes, and physician patterns to detect fraud without labelled data.

### Fix 5: Cold Start Bootstrapping Strategies

**Problem:** v1 identified cold start as a risk (Section 4.6) but proposed no concrete solution beyond "the system is most useful where we have the most data."

**Fix:** Added three bootstrapping approaches:

- BOLT-K (WWW 2019): Domain transfer achieving >75% accuracy
- JMIR (March 2026): Iterative enrichment reducing manual workload by up to 90%
- General meta-learning pattern: learn how to assign codes, not just which codes to assign

### Fix 6: Flywheel Convergence Theory

**Problem:** v1 stated that flywheel convergence was unproven (Section 6.5) and could not be proven from first principles. This was correct at the time of writing but was overtaken by the discovery of arXiv:2601.05280v2.

**Fix:** Added the formal convergence theorem: self-improving loops converge when the external evaluator maintains a persistent exogenous signal (α_t ≥ α* > 0). This directly maps to the Amplified architecture: the 7 gates are the persistent signal. This changes "gates don't change" from a governance principle to a mathematical requirement. The fix does not claim the flywheel will converge — it establishes the mathematical **condition** under which convergence is possible. Whether our specific system meets that condition in practice is still a Phase 4 question.

### Fix 7: "Downstream Quality" Defined

**Problem:** v1 used "downstream quality" in several places (Section 2.5, 4.2, 7.2) without defining what it meant. Different agents could interpret this differently.

**Fix:** Added a formal three-part definition:

1. **Retrieval precision** — Do queries return the right nodes?
2. **Reuse rate** — Are nodes actually being used downstream?
3. **Decay resistance** — Do nodes maintain their quality rating over time?

These three components are independently measurable and together cover the dimensions of quality that the scoring layer needs to predict.

---

## 8. HOW TO USE THIS HYPOTHESIS IN YOUR WORK

Practical guidance for AI agents working on different parts of the system. This section tells you what the hypothesis means for **your specific role**, not the system as a whole.

### If You Are Implementing Kaizen

The scoring layer gives you new inputs. The code-level metrics defined in Section 1.5 of the hypothesis (reuse frequency, co-occurrence matrix, decay rate, gate pass rate per code, attribution depth per code, bridge score, code velocity) are all computable from existing Curator audit logs.

Your job: extract these metrics and surface them in Kaizen reports. The metric interactions (Section 1.6) are where the real intelligence lives — frequency × decay identifies stale knowledge, co-occurrence × gate pass rate identifies problematic domain combinations, velocity × attribution depth identifies fast-growing areas with weak sourcing.

These metrics tell you **where to look**. They do not tell you what to do. The Kaizen process (investigate → propose → validate → implement) still applies. The scoring layer accelerates the "investigate" step by pointing at anomalies automatically.

### If You Are Implementing the Curator

Your audit logs are the foundation of the scoring layer. Every code assignment, every gate evaluation, every write operation must be logged with full metadata: timestamp, agent, codes assigned, gate results, operation type.

**Log everything. Do not optimise logs for storage.** The scoring layer computes metrics from these logs. A missing log entry is a missing data point. A Curator that logs selectively (e.g., only logging failures) makes the scoring layer's metrics unreliable.

The minimum fields for scoring-layer compatibility:

- Operation timestamp
- Agent performing the operation
- Codes assigned or modified
- Gate evaluation results (per gate, per criterion — not just pass/fail)
- Node ID affected
- Operation type (create, update, delete)

### If You Are Implementing Gates

Produce **sub-scores per criterion**, not just pass/fail. This is the single most important change the hypothesis asks of the gate system.

A gate that returns `pass` or `fail` enables Level 0 scoring (output scoring). A gate that returns per-criterion scores enables Level 1 scoring (gate meta-scoring). The meta-scoring cascade (Section 2.6 of the hypothesis) requires per-criterion decomposition to identify which specific criteria within each gate are doing the most discriminating work and which are decorative.

Example: G3 (Rubric & Benchmark) currently checks RAEI ≥ 12/20, PRS ≥ 5.0, believability, and label consistency. Instead of returning a single pass/fail, return the individual scores: RAEI score, PRS score, believability assessment, label consistency assessment. The scoring layer can then analyse which of these criteria predicts downstream quality and which does not.

### If You Are Implementing the Pudding Technique

The bridge score (Section 1.7 of the hypothesis) quantifies cross-domain discovery. Bridge(c_i, c_j) = CoOcc(c_i, c_j) × RF(c_i) × RF(c_j), where c_i and c_j are codes from different domains.

High bridge scores are the Pudding technique's gold — frequently-used codes from different domains appearing together often. These are the surprising connections that the Pudding technique exists to find. The bridge score gives you a quantitative way to prioritise which cross-domain connections are most valuable.

Low bridge scores with high co-occurrence may indicate noise (codes co-occurring because of labelling artefacts, not genuine connections). The frequency multiplier filters these out: both codes must be independently meaningful (high individual reuse) for the bridge to score highly.

### If You Are Implementing a New Database Curator

Apply compressed codes from day one. Every data object gets coded on first write. Do not defer coding to a later stage — every write without a code is a lost data point for the scoring layer.

Cold start is real. New databases will have sparse metrics. But the bootstrapping strategies (domain transfer, iterative enrichment) work better when you have some data from the start than when you have none. Even imperfect initial codes are better than no codes, because they provide the seed data for iterative improvement.

### The Critical Rule: Do Not Skip the Validation Plan

**DO NOT implement the full flywheel without running the validation plan first.**

Phase 1 → Phase 2 → Phase 3 → Phase 4. Each phase has go/no-go criteria. If Phase 1 fails (metrics not extractable), do not proceed to Phase 2. If Phase 2 fails (gates not differential), do not proceed to Phase 3. If Phase 3 fails (lenses don't help), simplify — you may not need lenses. If Phase 4 fails (loop doesn't turn), the individual layers are still valuable, but the flywheel is not confirmed.

The validation plan exists because the integration is novel. Skipping it and implementing the full flywheel based on the hypothesis alone is exactly the kind of premature commitment that the hypothesis status is designed to prevent.

---

## 9. THE PHILOSOPHY — WHY THIS MATTERS

### "Mathematics Decides"

This phrase appears throughout the Amplified constitutional documents. It is not a slogan. It is an operating principle.

Without the scoring layer, quality decisions depend on individual judgment. An agent assesses whether a node is "good enough." A Curator decides whether a code assignment is "correct." A gate evaluator judges whether a node "passes." These are all human-style judgments — variable, inconsistent, unauditable.

The scoring layer is what makes "mathematics decides" operational at scale. When every quality dimension is quantified, every decision can be traced to a measurement. Not "I think this node is good" but "this node has a reuse frequency of 0.73, a gate pass rate of 0.91 at G3, and a bridge score of 0.15 with domain FIN." The mathematics is explicit. The decision is auditable. The improvement is measurable.

### Standing on Shoulders

"We're not that clever. We stand on the shoulders of giants."

This is honest. Every piece of the hypothesis is borrowed from proven systems:

- **SNOMED CT** — proved that codes enable quality measurement at scale (370,000+ concepts, 40+ countries, decades of production use)
- **IBM** — proved that faceted codes generate economic metrics (Reuse Percent, Cost Avoidance, Value Added)
- **OpenRS** — proved that rubrics can be meta-scored and improved (+5.1 over scalar baselines)
- **Brunswik** — proved that different environments make different cues more or less predictive (lens model, 1956)
- **Deming** — proved that constancy of purpose is the convergence condition for quality improvement (14 Points)
- **arXiv:2601.05280v2** — proved formally that persistent external signal is the mathematical convergence condition

The assembly is ours. The pieces are theirs. This is not false modesty — it is accurate attribution. And accurate attribution is itself one of the system's constitutional principles.

### Why Gates Don't Change

"These gates do not change" has evolved from a governance principle to a mathematical requirement.

Before arXiv:2601.05280v2, "gates don't change" was Ewan's principle based on quality management intuition and Deming's constancy of purpose. After arXiv:2601.05280v2, it is a formal convergence condition. The paper proves that if the external evaluator (our gates) maintains persistent signal, the system can converge to truth. If the external evaluator weakens, the system degenerates.

This means:

- Do not soften gate thresholds to improve pass rates. Improving pass rates by lowering the bar is the definition of α_t → 0.
- Do not make gates adaptive to system output. An adaptive gate is no longer exogenous. It becomes endogenous, and the convergence condition breaks.
- Do not remove gates that seem redundant. Even a gate with a high pass rate may be providing signal that prevents specific failure modes. Phase 2 of the validation plan will identify which gates are truly redundant.

The gates can be **supplemented** (new criteria added within a gate) and their **implementation** can be improved (better measurement of existing criteria). But the gate thresholds and the gate structure are constitutional. They are the fixed point against which everything else improves.

### Measured Improvement, Not Vibes

The system should improve the system. But "improve" means measured improvement against fixed criteria, not vibes about getting better.

If we cannot measure it, we do not claim it. If the flywheel "feels" like it is working but the metrics do not show improvement, the flywheel is not working. If a Kaizen cycle produces changes that "seem" better but gate pass rates do not improve, the changes have not been validated.

This is what separates a self-improving system from a self-referential one. Self-referential systems believe their own outputs. Self-improving systems measure their outputs against external criteria (the gates) and only count improvement when the measurements confirm it.

---

## 10. DOCUMENT MAP — WHERE TO FIND THINGS

Quick reference for agents navigating the constitutional documents and finding the specific sections relevant to the scoring hypothesis.

| Topic | Document | Section |
|-------|----------|---------|
| Compressed coding system | `ATTRIBUTION-AND-CURATION-v1` | Section 3 |
| Curator audit logging requirements | `ATTRIBUTION-AND-CURATION-v1` | Section 2 |
| Gate definitions (G1–G7) | `VALIDATION-METHODOLOGY-v2` | Section 4.2 |
| Gate enforcement matrix | `VALIDATION-METHODOLOGY-v2` | Section 12 |
| System halt protocol | `VALIDATION-METHODOLOGY-v2` | Section 4.3 |
| Kaizen Department structure | `CODE-TAXONOMY-AND-KAIZEN-v1` | Section 3.1 |
| Kaizen cycle definition | `CODE-TAXONOMY-AND-KAIZEN-v1` | Section 3.3 |
| Node-level reporting schema | `CODE-TAXONOMY-AND-KAIZEN-v1` | Section 3.2 |
| Error Anticipation Registry | `CODE-TAXONOMY-AND-KAIZEN-v1` | Section 1 |
| Code taxonomy and reuse matrix | `CODE-TAXONOMY-AND-KAIZEN-v1` | Section 2 |
| Scoring hypothesis — codes as scores | `SCORING-UNIFICATION-HYPOTHESIS` | Section 1 |
| Scoring hypothesis — rubric meta-scoring | `SCORING-UNIFICATION-HYPOTHESIS` | Section 2 |
| Scoring hypothesis — lens-adaptive evaluation | `SCORING-UNIFICATION-HYPOTHESIS` | Section 3 |
| Scoring hypothesis — unification loop | `SCORING-UNIFICATION-HYPOTHESIS` | Section 4 |
| Scoring hypothesis — evidence grading | `SCORING-UNIFICATION-HYPOTHESIS` | Section 5 |
| Scoring hypothesis — known gaps | `SCORING-UNIFICATION-HYPOTHESIS` | Section 6 |
| Scoring hypothesis — validation plan | `SCORING-UNIFICATION-HYPOTHESIS` | Section 7 |
| This thought process document | `SCORING-UNIFICATION-THOUGHT-PROCESS` | You are here |
| v2 research findings | `v2-research-findings.md` | (entire file — lens-adaptive non-LLM evidence, convergence theory, Goodhart mitigations, cold start bootstrapping) |

### Document Dependency Graph

```
ATTRIBUTION-AND-CURATION-v1
  ├── Provides: compressed codes, Curator model, audit logging
  └── Required by: SCORING-UNIFICATION-HYPOTHESIS (no codes = nothing to score)

VALIDATION-METHODOLOGY-v2
  ├── Provides: 7 gates (G1-G7), rubric structure, enforcement matrix
  └── Required by: SCORING-UNIFICATION-HYPOTHESIS (gates = the rubric being meta-scored)

CODE-TAXONOMY-AND-KAIZEN-v1
  ├── Provides: Kaizen process, error registry, code taxonomy
  └── Required by: SCORING-UNIFICATION-HYPOTHESIS (Kaizen = the improvement mechanism)

SCORING-UNIFICATION-HYPOTHESIS
  ├── Proposes: scoring layer, meta-scoring, lens-adaptive evaluation, flywheel
  ├── Status: hypothesis (not constitutional until validated)
  └── Depends on: all three documents above

SCORING-UNIFICATION-THOUGHT-PROCESS (this document)
  ├── Explains: reasoning, evidence strategy, corrections, risks
  └── Read alongside: SCORING-UNIFICATION-HYPOTHESIS
```

---

*Document version: v1 — 2026-03-17 — Amplified Partners*
*This document is a reference companion to SCORING-UNIFICATION-HYPOTHESIS. It explains reasoning and context, not policy.*
*If the hypothesis is validated and becomes a standard, this document should be updated to reflect the validation results.*

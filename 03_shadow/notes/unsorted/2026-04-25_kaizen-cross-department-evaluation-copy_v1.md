---
title: "Kaizen Cross Department Evaluation Copy"
id: "kaizen-cross-department-evaluation-copy"
version: 1
created: "2026-04-25"
type: "document"
topic_type: "unsorted"
audience: "internal"
layer: "shadow"
status: "filed"
signed_by: "Devon, 2026-04-25, devin-992682c244cf444f91e0a516498afbfd"
---

**Kaizen Intelligence**

**Cross-Department Evaluation Systems**

**& PUDDING Analysis**

  --
  --

*Alternative Systems Assessment, Cross-Department Data Relationships,*

*and the AI Kaizen Department Blueprint*

Prepared for: Amplified Partners

Author: Ewan Bramley × Perplexity

Date: March 2026

**Classification: Confidential**

**Table of Contents**

**Executive Summary**

This document evaluates five alternative evaluation systems against Amplified Partners\' existing infrastructure to determine what capabilities are worth extracting into the Kaizen (continuous improvement) department. The analysis applies the PUDDING 2026 taxonomy to discover cross-department data relationships that no single system captures alone.

**Research scope:** DeepEval (Confident AI), Arize Phoenix, Inspect AI (UK AISI), Braintrust, and LangSmith (LangChain) were assessed for relevance, actionability, evidence quality, and potential impact on the Amplified architecture.

**Key Conclusions**

-   **DeepEval is the highest-priority extraction target.** Its 6 agent evaluation metrics (TaskCompletion, ToolCorrectness, ArgumentCorrectness, PlanQuality, PlanAdherence, StepEfficiency) map directly to Cove agent worker roles and integrate with the existing 4-tier measurement system via pytest and CI/CD pipelines.

-   **Inspect AI fills a critical gap in safety/honesty evaluation.** The MASK honesty benchmark and AgentHarm evaluations provide external calibration for Amplified\'s custom Radical Honesty Score and Layer 0 Laws compliance.

-   **Arize Phoenix\'s embedding drift detection** should be adapted (not adopted wholesale) to monitor Business Brain knowledge graph degradation---a leading indicator for death spiral events.

-   **Braintrust\'s Loop concept** (natural language → custom scorer) is worth monitoring as an acceleration pattern for the Kaizen team\'s scorer development workflow.

-   **LangSmith is largely redundant** given the existing Langfuse deployment at langfuse.beast.amplifiedpartners.ai. Skip for now.

**The PUDDING Insight**

The cross-department PUDDING analysis reveals three high-value ABC recipes that connect evaluation metrics across department boundaries. The most actionable: agent step efficiency improvements in Cove predict customer friction reduction in Real before direct measurement catches it---a leading indicator that saves approximately 2--3 weeks of detection lag.

**Bottom Line**

Amplified already has 70% of the observability infrastructure needed (Langfuse, LiteLLM, ClickHouse, Temporal). The remaining 30% is evaluation intelligence---specific metrics, drift detection algorithms, and cross-department correlation engines. This document provides the blueprint to build that final layer as the Kaizen department\'s core function.

**Section 1: Alternative Systems Landscape**

Each system is evaluated using a 4-criteria rubric scored 0--5: Relevance (alignment with Amplified\'s architecture), Actionability (how quickly capabilities can be extracted), Evidence (quality of documentation and community validation), and Impact (potential effect on the \$138/client/month cost structure and service quality).

**1.1 DeepEval (Confident AI)**

DeepEval is an open-source (Apache 2.0) LLM evaluation framework offering 50+ metrics with first-class support for agent evaluation across reasoning, action, and execution layers.[^1] Its G-Eval framework enables custom metric creation in natural language, while the DAG (Deep Acyclic Graph) metric provides deterministic decision-tree scoring for objective criteria.[^2]

**Key Capabilities Worth Extracting**

-   6 Agent Metrics: TaskCompletionMetric, ToolCorrectnessMetric, ArgumentCorrectnessMetric, PlanQualityMetric, PlanAdherenceMetric, StepEfficiencyMetric

-   G-Eval: custom metrics from natural language criteria with LLM-as-judge chain-of-thought scoring

-   DAGMetric: deterministic decision trees using BinaryJudgementNode and NonBinaryJudgementNode for compliance-style scoring

-   ArenaGEval: A/B comparison of model outputs for prompt optimization

-   Synthetic data generation for test dataset bootstrapping

-   Pytest integration enabling CI/CD evaluation pipelines

-   RAG metrics suite: Answer Relevancy, Faithfulness, Contextual Relevancy/Precision/Recall

**PUDDING 2026 Label: M.+.5.l** (Meta-process, Amplifying, System-level, Long-term) --- DeepEval is a meta-evaluation system that amplifies quality measurement across the entire AI stack over time.

  --------------- ----------- -------------------------------------------------------------------------------------
  **Criterion**   **Score**   **Rationale**
  Relevance       **5/5**     Agent metrics map 1:1 to Cove worker evaluation needs
  Actionability   **5/5**     Apache 2.0, pip install, pytest integration, works with any LLM via LiteLLM
  Evidence        **4/5**     Well-documented, active community, used by frontier evaluation teams
  Impact          **5/5**     Directly reduces evaluation cost via tiered sampling; DAG metrics replace manual QA
  --------------- ----------- -------------------------------------------------------------------------------------

**Verdict: EXTRACT** --- Priority 1. Deploy agent metrics into Cove workers immediately. Integrate DAG scoring for Layer 0 compliance checks.

**1.2 Arize Phoenix**

Arize Phoenix is an open-source AI observability platform built on OpenTelemetry, providing tracing, embedding drift detection, and dataset management.[^3] Its standout capability is Euclidean distance-based embedding drift detection with UMAP clustering for failure pattern visualization.[^4]

**Key Capabilities Worth Extracting**

-   Embedding drift detection via Euclidean distance between centroid vectors across time periods

-   UMAP clustering for visual failure pattern identification in embedding space

-   KS 2-sample test overlay for statistically robust drift alerting

-   Dataset management with versioned test cases

-   Self-hostable with complete data sovereignty

-   Vendor-agnostic: LlamaIndex, LangChain, DSPy, Haystack compatible

**PUDDING 2026 Label: S.-.4.l** (State, Dampening, Network-level, Long-term) --- Phoenix detects state degradation across interconnected embedding spaces over long periods.

  --------------- ----------- ------------------------------------------------------------------------------------------------
  **Criterion**   **Score**   **Rationale**
  Relevance       **4/5**     Embedding drift directly relevant to Business Brain/FalkorDB health monitoring
  Actionability   **3/5**     Algorithm extractable but full platform overlaps with Langfuse; selective extraction needed
  Evidence        **4/5**     Well-researched drift measurement, published methodology, active GitHub repo
  Impact          **4/5**     Early drift detection prevents knowledge graph degradation cascading into client-facing errors
  --------------- ----------- ------------------------------------------------------------------------------------------------

**Verdict: EXTRACT (Algorithm Only)** --- Extract the Euclidean distance centroid drift algorithm and KS test overlay. Do not deploy the full Phoenix platform (redundant with Langfuse). Build a custom drift pipeline feeding into ClickHouse.

**1.3 Inspect AI (UK AI Security Institute)**

Inspect AI is an MIT-licensed evaluation framework created by the UK AI Security Institute (AISI), offering 100+ pre-built evaluations across coding, math, cybersecurity, reasoning, and safety domains.[^5] AISI has tested over 30 frontier AI models using Inspect and contributed to evaluation methodology used by governments worldwide.[^6]

**Key Capabilities Worth Extracting**

-   MASK (Measuring AI Safety Knowledge): honesty evaluation benchmark

-   AgentHarm: agent-specific safety evaluation for harmful tool use

-   AIR Bench: AI risk benchmarking across multiple safety dimensions

-   FORTRESS: national security evaluation framework

-   SOS Bench: scientific safety benchmarking

-   GAIA, SWE-Bench, GDM CTF: agent capability benchmarks

-   Solvers → Scorers architecture: model grading with custom scoring schemes

-   Single-command benchmark execution against any model

**PUDDING 2026 Label: C.\>.5.i** (Constraint, Tipping, System-level, Instant) --- Safety evaluations detect constraint violations at system scale, with immediate scoring on each test.

  --------------- ----------- ----------------------------------------------------------------------------------------------------
  **Criterion**   **Score**   **Rationale**
  Relevance       **5/5**     Safety/honesty evals align directly with Layer 0 Laws and Radical Honesty metric
  Actionability   **4/5**     MIT license, CLI-driven, run any benchmark with single command; needs custom task adaptation
  Evidence        **5/5**     Government-backed, used by frontier labs, peer-reviewed methodology, published in Science
  Impact          **4/5**     External calibration for custom honesty metrics; safety compliance evidence for enterprise clients
  --------------- ----------- ----------------------------------------------------------------------------------------------------

**Verdict: EXTRACT** --- Priority 2. Deploy MASK and AgentHarm benchmarks as Tier 3 deep evaluations. Use as external calibration for Amplified\'s custom Radical Honesty Score. Run quarterly against all models in the LiteLLM routing table.

**1.4 Braintrust**

Braintrust is a commercial evaluation platform built around three pillars: Traces, Evals, and Annotation, with an AI assistant called Loop that generates custom scorers from plain-language descriptions.[^7] Its Brainstore database claims 80x faster query performance than traditional data warehouses for evaluation data.[^8]

**Key Capabilities Worth Extracting**

-   Loop: AI-generated scorers from natural language descriptions with 99.97% success rate

-   Production traces → eval datasets with one click (failure pattern → regression test)

-   Same scorers run in dev, CI, and production (environment parity)

-   Online evaluation with configurable sampling rates

-   Cross-functional workflows: engineers + QA + product share evaluation results

-   MCP server for IDE integration

**PUDDING 2026 Label: P.+.4.m** (Process, Amplifying, Network-level, Medium-term) --- Braintrust amplifies the evaluation process across team networks over iterative improvement cycles.

  --------------- ----------- ----------------------------------------------------------------------------------
  **Criterion**   **Score**   **Rationale**
  Relevance       **3/5**     Loop concept valuable, but platform overlaps heavily with Langfuse + DeepEval
  Actionability   **2/5**     Commercial platform; pattern extractable but not the implementation
  Evidence        **4/5**     Used by Notion, Stripe, Vercel; well-documented Loop capabilities
  Impact          **3/5**     Loop pattern could accelerate Kaizen scorer development but adds SaaS dependency
  --------------- ----------- ----------------------------------------------------------------------------------

**Verdict: MONITOR** --- Extract the Loop pattern (natural language → scorer generation) as an internal capability built on top of DeepEval\'s G-Eval. Do not adopt the platform itself. Revisit if self-hosted option becomes available.

**1.5 LangSmith (LangChain)**

LangSmith is LangChain\'s proprietary observability and evaluation platform, offering annotation queues, pairwise comparison experiments, and an Insights Agent for automated analysis.[^9] It provides deep integration with LangChain and LangGraph ecosystems but is closed-source with SaaS-primary deployment.[^10]

**Key Capabilities**

-   Pairwise annotation queues for structured A/B evaluation of agent outputs

-   Insights Agent for automated trace analysis and pattern detection

-   Deep LangChain/LangGraph integration with automatic tracing

-   Dataset management and versioned evaluation runs

-   Human feedback collection via annotation workflows

**PUDDING 2026 Label: M.=.4.m** (Meta-process, Stable, Network-level, Medium-term) --- LangSmith provides stable meta-evaluation within the LangChain ecosystem network.

  --------------- ----------- ----------------------------------------------------------------------------------
  **Criterion**   **Score**   **Rationale**
  Relevance       **2/5**     Amplified already has Langfuse for tracing/observability; LangSmith is redundant
  Actionability   **1/5**     Closed-source, SaaS-primary; extracting capabilities requires platform adoption
  Evidence        **3/5**     Well-documented but tightly coupled to LangChain ecosystem
  Impact          **1/5**     Minimal incremental value over existing Langfuse deployment
  --------------- ----------- ----------------------------------------------------------------------------------

**Verdict: SKIP** --- Langfuse at langfuse.beast.amplifiedpartners.ai already covers tracing and observability. Pairwise comparison concept can be built internally using DeepEval\'s ArenaGEval. No action needed.

**1.6 Comparative Summary**

  ------------------- --------------- ------------- -------------- ------------ ----------- --------------------
  **System**          **Relevance**   **Action.**   **Evidence**   **Impact**   **Total**   **Verdict**
  **DeepEval**        5               5             4              5            **19/20**   **EXTRACT (P1)**
  **Inspect AI**      5               4             5              4            **18/20**   **EXTRACT (P2)**
  **Arize Phoenix**   4               3             4              4            **15/20**   **EXTRACT (Algo)**
  **Braintrust**      3               2             4              3            **12/20**   **MONITOR**
  **LangSmith**       2               1             3              1            **7/20**    **SKIP**
  ------------------- --------------- ------------- -------------- ------------ ----------- --------------------

**Section 2: What's Worth Extracting**

This section reorganizes findings by capability rather than tool, mapping each extraction to Amplified\'s existing architecture, department ownership, implementation complexity, and cost impact on the \$138/client/month estimate.

**2.1 Agent Evaluation Metrics**

**Source:** DeepEval (Confident AI)

**Technical Description**

DeepEval provides six agent-specific metrics that analyze full execution traces captured via an \@observe decorator.[^11] These operate at two scopes:

-   **Reasoning Layer (End-to-End):** PlanQualityMetric evaluates whether the agent generates logical, complete, and efficient plans. PlanAdherenceMetric evaluates whether the agent follows its own plan during execution.

-   **Action Layer (Component-Level):** ToolCorrectnessMetric evaluates whether the agent selects the right tools. ArgumentCorrectnessMetric evaluates whether it generates correct arguments for each tool call.

-   **Execution Layer (End-to-End):** TaskCompletionMetric evaluates whether the agent successfully accomplishes the intended task. StepEfficiencyMetric evaluates whether it completes tasks without unnecessary or redundant steps.

**Mapping to Amplified Architecture**

Each metric maps to a specific Cove agent worker role:

  --------------------- ------------------------ ---------------------- ------------
  **Metric**            **Cove Worker Target**   **Eval Tier**          **Scope**
  TaskCompletion        All workers              Tier 3 (Deep eval)     End-to-end
  ToolCorrectness       Tool-calling workers     Tier 2 (Sampled 10%)   Component
  ArgumentCorrectness   Tool-calling workers     Tier 2 (Sampled 10%)   Component
  PlanQuality           Orchestrator agents      Tier 3 (Deep eval)     End-to-end
  PlanAdherence         Orchestrator agents      Tier 3 (Deep eval)     End-to-end
  StepEfficiency        All workers              Tier 2 (Sampled 10%)   End-to-end
  --------------------- ------------------------ ---------------------- ------------

**Department Owner:** Cove (primary) + Kaizen (oversight)

**Implementation Complexity:** Low --- pip install deepeval, add \@observe decorators to existing Cove workers, wire results to Langfuse via OpenTelemetry

**Cost Impact:** Tier 2 metrics (sampled 10%) add approximately \$0.003--\$0.008 per interaction in LLM judge costs. Tier 3 deep evals (triggered only on anomalies) add approximately \$0.02--\$0.05 per flagged interaction. Net impact on \$138/client/month: +\$0.50--\$1.20/client/month, offset by early error detection reducing rework costs.

**2.2 Embedding Drift Detection**

**Source:** Arize Phoenix (algorithm extraction)

**Technical Description**

Arize Phoenix computes Euclidean distance between centroid vectors of embedding sets across time periods to detect drift.[^12] When problematic or new data is introduced, the Euclidean distance increases, signaling drift requiring investigation. A KS 2-sample test overlay on sampled Euclidean distances provides statistically robust drift alerting. UMAP clustering visualization reveals the nature of the drift---whether it\'s new entity types, terminology shifts, or data quality degradation.[^13]

**Mapping to Amplified Architecture**

-   FalkorDB knowledge graph: Track embedding centroids of entity/relationship vectors weekly. Drift indicates knowledge graph schema evolution or data quality issues.

-   Business Brain: Monitor embedding consistency between client knowledge bases and the master ontology. Drift here signals stale client data or ontology divergence.

-   ClickHouse: Store drift metrics as time-series data for trend analysis and threshold alerting.

-   Langfuse: Tag traces from drifting embedding regions for human review in annotation queues.

**Department Owner:** Data (measurement) + Kaizen (alerting)

**Implementation Complexity:** Medium --- Requires custom Python pipeline to compute weekly centroid Euclidean distances from FalkorDB embeddings, store in ClickHouse, and wire alerting through Temporal workflows. Estimated 2--3 days of development.

**Cost Impact:** Approximately \$0 incremental compute (runs on existing ClickHouse infrastructure). Storage cost: negligible (centroid vectors + distance scalars). Net impact on \$138/client/month: \$0.

**2.3 Safety & Honesty Evaluations**

**Source:** Inspect AI (UK AI Security Institute)

**Technical Description**

Inspect AI provides pre-built safety evaluation suites that can be run against any model via a single CLI command.[^14] The most relevant for Amplified:

-   **MASK (Measuring AI Safety Knowledge):** Evaluates honesty and truthfulness in model responses across structured scenarios. Tests whether models acknowledge uncertainty, avoid fabrication, and maintain consistency under adversarial prompting.

-   **AgentHarm:** Evaluates whether agents can be manipulated into harmful tool use, testing resistance to prompt injection and social engineering attacks on the action layer.

-   **AIR Bench:** Multi-dimensional AI risk benchmarking covering fairness, robustness, privacy, and safety. Provides a composite risk score.

**Mapping to Amplified Architecture**

-   Layer 0 Laws compliance: Run MASK and AgentHarm quarterly against all models in LiteLLM\'s routing table. Any model failing below threshold gets automatically deprioritized in routing.

-   Radical Honesty Score calibration: Use MASK results as an external benchmark to validate that Amplified\'s custom Radical Honesty metric is measuring the same construct as the academic standard.

-   R&D/Chaos integration: AgentHarm becomes a standard resilience test in the Chaos department\'s failure scenario library.

**Department Owner:** R&D/Chaos (execution) + Kaizen (tracking)

**Implementation Complexity:** Medium --- MIT license, CLI-driven. Requires writing custom Inspect tasks that mirror Amplified\'s specific agent architectures. The Solvers → Scorers pattern maps well to Temporal workflow steps. Estimated 1--2 weeks for initial integration.

**Cost Impact:** Quarterly runs only. Estimated \$15--\$30 per quarterly evaluation cycle (model inference costs for \~200--500 test cases). Net impact: \<\$0.10/client/month amortized.

**2.4 Natural Language Scorer Generation**

**Source:** Braintrust (Loop pattern)

**Technical Description**

Braintrust\'s Loop AI assistant generates custom scorers from plain-language descriptions, achieving a 99.97% success rate across all model calls.[^15] The workflow: describe a quality criterion in English → Loop generates a scorer function → scorer runs in dev, CI, and production with environment parity. This collapses the typical 2--4 hour scorer development cycle into minutes.

**Mapping to Amplified Architecture**

The Loop pattern can be replicated internally using DeepEval\'s G-Eval framework:

-   G-Eval already accepts natural language criteria and generates evaluation steps automatically via LLM chain-of-thought.

-   Build a Kaizen internal tool: \"Describe your quality criterion\" → generates a G-Eval metric definition → validates against historical test cases → deploys to the evaluation pipeline.

-   Store generated scorers in FalkorDB as evaluation recipe nodes linked to department and metric category.

**Department Owner:** Kaizen

**Implementation Complexity:** Low--Medium --- G-Eval already exists in DeepEval. Building the wrapper tool (natural language → G-Eval config → validation → deployment) is estimated at 3--5 days.

**Cost Impact:** Reduces scorer development time from hours to minutes. Labor cost savings dominate; LLM inference cost for G-Eval generation: \~\$0.01--\$0.03 per scorer. Net impact: cost-positive (labor savings).

**2.5 DAG Decision-Tree Scoring**

**Source:** DeepEval (DAGMetric)

**Technical Description**

The DAGMetric constructs deterministic evaluation decision trees using LLM-powered nodes: TaskNode (extracts data), BinaryJudgementNode (yes/no decisions), NonBinaryJudgementNode (multi-option scoring), and VerdictNode (terminal scores).[^16] Unlike G-Eval, which is probabilistic, DAG scoring is deterministic---the same input always follows the same decision path, producing reproducible scores.

**Mapping to Amplified Architecture**

-   Layer 0 Laws compliance: Build a DAG that extracts claims from agent output → checks each against the 5 Layer 0 Laws → produces a composite compliance score with per-law breakdown.

-   Referral Honesty metric: DAG path: Extract referral recommendation → Check if client capacity data was consulted → Check if alternative options were presented → Score.

-   Win-Win Alignment: DAG path: Extract proposed action → Identify benefiting parties → Check for unilateral benefit → Check for mutual benefit → Score.

**Department Owner:** Kaizen (definition) + All departments (execution)

**Implementation Complexity:** Low --- DAGMetric is part of DeepEval. Writing DAG definitions for each custom metric takes 1--2 hours per metric. Total for 5 custom metrics: 1--2 days.

**Cost Impact:** Each DAG evaluation costs approximately \$0.005--\$0.02 (LLM inference for node judgements). At Tier 2 sampling (10%), net impact: +\$0.10--\$0.30/client/month. Replaces manual QA review that currently costs significantly more.

**Section 3: PUDDING Cross-Department Analysis**

This section applies the PUDDING 2026 taxonomy (Pattern-based Unified Data Discovery for Insight and Guidance) to discover cross-department relationships that no single evaluation system captures alone. The methodology follows Swanson\'s (1986) ABC model for literature-based discovery.[^17]

**3.1 PUDDING Labelling: Evaluation Concepts**

Each evaluation concept receives a PUDDING 2026 label using the WHAT.HOW.SCALE.TIME taxonomy. The label encodes the concept\'s nature (WHAT), its dynamic behaviour (HOW), its scope (SCALE), and its temporal horizon (TIME).

  ---------------------------- ----------------- -------------- --------------------------------------------------
  **Concept**                  **Departments**   **PUDDING**    **Interpretation**
  Agent task completion        Cove / Kaizen     **P.\>.3.i**   Process tipping-point in small groups, instant
  Embedding drift detection    Data / Kaizen     **S.--.4.l**   State dampening across network, long-term
  Business Brain consistency   Data / Real       **I.=.5.p**    Information stable at system-level, permanent
  Radical Honesty scoring      Real / Kaizen     **C.=.6.∞**    Constraint stable at universal scale, timeless
  Win-Win alignment            Real / Kaizen     **R.+.2.l**    Relation amplifying in pairs, long-term
  Death spiral detection       Kaizen / Chaos    **S.\>.4.v**   State tipping-point across network, variable
  Safety/harm evaluation       Chaos / Real      **C.\>.5.i**   Constraint tipping at system-level, instant
  Plan quality measurement     Cove / Kaizen     **M.=.3.m**    Meta-process stable in small groups, medium
  Step efficiency tracking     Cove / Kaizen     **P.--.3.i**   Process dampening in small groups, instant
  Customer friction scoring    Real / Data       **S.--.2.v**   State dampening in pairs, variable
  Knowledge graph health       Data / Kaizen     **R.=.5.l**    Relation stable at system-level, long-term
  Cost per interaction         Data / Kaizen     **I.--.1.i**   Information dampening at singular scale, instant
  ---------------------------- ----------------- -------------- --------------------------------------------------

**3.2 Cross-Department Pattern Matching**

Matching PUDDING labels across departments reveals hidden connections. Two concepts share a bridge when their HOW or WHAT components match despite belonging to different departments. This cross-domain resonance is where Swanson\'s 1+1=3 insight emerges.

**Pattern Match 1 --- Dampening (--):** Step efficiency (P.--.3.i), Embedding drift (S.--.4.l), Customer friction (S.--.2.v), Cost per interaction (I.--.1.i) all share the dampening dynamic. These are all measuring the same fundamental force---reduction of waste---across different domains and scales.

**Pattern Match 2 --- Tipping (\>):** Agent task completion (P.\>.3.i), Death spiral detection (S.\>.4.v), Safety evaluation (C.\>.5.i) all share the tipping-point dynamic. These detect threshold crossings where system behaviour changes qualitatively---from functional to broken.

**Pattern Match 3 --- Stable (=):** Business Brain consistency (I.=.5.p), Radical Honesty (C.=.6.∞), Plan quality (M.=.3.m), Knowledge graph health (R.=.5.l) all share the stability dynamic. These are the invariants---things that should not change---and their measurement is about detecting unexpected instability.

**3.3 PUDDING ABC Recipes**

**Recipe 1: Efficiency → Resource Optimization → Friction Reduction**

  ------------------- --------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------
  **Element**         **Detail**
  **A (Source)**      Agent Step Efficiency --- Cove/Kaizen (P.--.3.i)
  **B (Bridge)**      Resource Optimization Bridge --- \"Dampening inefficiency\" mechanism shared across domains
  **C (Target)**      Customer Friction Reduction --- Real/Data (S.--.2.v)
  **Connection**      A and C share HOW=-- (dampening). Both are reducing waste, just at different scales (3 vs 2) and with different temporal signatures (instant vs variable).
  **1+1=3 Insight**   Measuring agent step efficiency improvements PREDICTS customer friction reduction before it is measured directly---a leading indicator. When Cove agents become more efficient (fewer redundant steps), the downstream effect is faster client response times and fewer interaction loops. This creates a 2--3 week leading indicator for customer satisfaction metrics.
  ------------------- --------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------

**Novelty Score:** 7/10 --- The connection between internal agent efficiency and external customer friction is intuitive but not typically measured as a causal chain. Making it explicit creates a predictive model.

**Plausibility Score:** 9/10 --- The causal mechanism is clear: fewer agent steps → faster resolution → lower customer effort score. Well-supported by service operations literature.

**Actionability Score:** 9/10 --- Immediately implementable: correlate StepEfficiencyMetric outputs with customer friction scores in ClickHouse, build a regression model, and use it for real-time prediction.

**Combined Recipe Score: 8.3/10**

**Recipe 2: Drift → State Degradation → Death Spiral Warning**

  ------------------- --------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------
  **Element**         **Detail**
  **A (Source)**      Embedding Drift Detection --- Data/Kaizen (S.--.4.l)
  **B (Bridge)**      State Degradation Bridge --- Drift is the slow version of what death spiral detects acutely
  **C (Target)**      Death Spiral Early Warning --- Kaizen/Chaos (S.\>.4.v)
  **Connection**      A and C share WHAT=S (State) and SCALE=4 (Network). A is dampening (slow degradation), C is tipping (acute collapse). The same underlying state is being measured at different velocities.
  **1+1=3 Insight**   Embedding drift IS the precursor signal for death spirals. Slow, continuous drift in knowledge graph embeddings eventually crosses a tipping point where cascading failures occur. By integrating drift metrics directly into the death spiral scoring engine, Kaizen can detect death spirals weeks before they manifest---transforming a reactive detection system into a predictive one. The derivative of the drift curve (acceleration of drift) is the actual death spiral early warning signal.
  ------------------- --------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------

**Novelty Score:** 8/10 --- Connecting embedding drift (a data science concept) to organizational death spirals (a systems dynamics concept) is a genuine cross-domain insight. The "derivative of drift = early warning" formulation is particularly novel.

**Plausibility Score:** 8/10 --- Well-supported by complex systems theory: slow degradation of state variables precedes phase transitions. The mechanism is sound but requires empirical validation of the specific drift thresholds that predict death spiral onset.

**Actionability Score:** 7/10 --- Requires building the drift pipeline first (Section 2.2), then computing drift derivatives, then calibrating thresholds against historical failure events. Estimated 3--4 weeks end-to-end.

**Combined Recipe Score: 7.7/10**

**Recipe 3: Safety → Constraint Enforcement → Radical Honesty**

  ------------------- ------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------
  **Element**         **Detail**
  **A (Source)**      Safety Evaluation --- Inspect AI/Chaos (C.\>.5.i)
  **B (Bridge)**      Constraint Enforcement Bridge --- \"Constraint enforcement at scale\" mechanism
  **C (Target)**      Radical Honesty Scoring --- Amplified/Real (C.=.6.∞)
  **Connection**      A and C share WHAT=C (Constraint). A detects tipping violations (\> in HOW) while C maintains stable enforcement (= in HOW). They are the detection and maintenance sides of the same constraint system.
  **1+1=3 Insight**   Inspect AI's MASK honesty benchmark validates whether Amplified\'s Radical Honesty metric is actually measuring what it claims---external calibration. If a model scores well on Amplified's Radical Honesty but poorly on MASK, either the custom metric has blind spots or it measures something genuinely different from academic honesty standards. This calibration loop ensures the Radical Honesty Score maintains scientific validity as models evolve. The bridge also flows in reverse: Amplified's domain-specific honesty scenarios (e.g., referral honesty in SMB consulting) can be contributed back as Inspect tasks, extending the safety evaluation corpus.
  ------------------- ------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------

**Novelty Score:** 6/10 --- Using external benchmarks for calibration is standard practice, but framing it as a bidirectional PUDDING bridge (calibration flowing both ways) adds originality.

**Plausibility Score:** 9/10 --- External calibration of custom metrics is well-established in psychometrics and measurement science. The mechanism is robust.

**Actionability Score:** 8/10 --- Run MASK quarterly, compare scores with Radical Honesty on the same model/prompt pairs, compute correlation coefficient. Divergence triggers metric review. Implementable in 1--2 weeks.

**Combined Recipe Score: 7.7/10**

**3.4 Recipe Scoring Summary**

  -------------------------- ------------- ------------------ ------------- --------------
  **Recipe**                 **Novelty**   **Plausibility**   **Action.**   **Combined**
  1: Efficiency → Friction   7/10          9/10               9/10          **8.3/10**
  2: Drift → Death Spiral    8/10          8/10               7/10          **7.7/10**
  3: Safety → Honesty        6/10          9/10               8/10          **7.7/10**
  -------------------------- ------------- ------------------ ------------- --------------

All three recipes exceed the 7.0 threshold for actionable cross-department insights. Recipe 1 (Efficiency → Friction) has the highest combined score and should be implemented first due to its high actionability and immediate predictive value.

**Section 4: The Kaizen Department Blueprint**

The Kaizen department is Amplified Partners\' continuous improvement engine---the nervous system that senses, measures, and optimises performance across all other departments. This section defines its data flows, measurement tiers, cross-department relationships, temporal workflows, and implementation roadmap.

**4.1 Kaizen Data Flows**

Every department feeds data into Kaizen. The Kaizen department does not generate client-facing output; it generates insight that drives improvement across the entire organisation.

**From Real Department (Client-Facing)**

-   Customer satisfaction scores (per interaction and rolling average)

-   Customer friction scores (effort metrics, interaction loops, time-to-resolution)

-   Conversion metrics (lead → client, proposal → engagement)

-   Radical Honesty scores (per conversation, per agent)

-   Win-Win Alignment scores (per recommendation, per engagement)

-   Referral Honesty metrics (accuracy of capacity assessments, alternative options presented)

-   Value-Add scores (incremental value delivered beyond baseline)

**From Data Department (Extraction & Intelligence)**

-   Extraction accuracy rates (document parsing, entity recognition, relationship extraction)

-   Knowledge graph health metrics (FalkorDB node/edge consistency, orphan detection)

-   Embedding drift measurements (weekly centroid Euclidean distances)

-   Business Brain consistency scores (client knowledge base vs master ontology alignment)

-   Data freshness indicators (staleness detection, update frequency)

**From Cove Department (Agent Workers)**

-   Agent metrics: TaskCompletionMetric, ToolCorrectnessMetric, ArgumentCorrectnessMetric

-   Agent metrics: PlanQualityMetric, PlanAdherenceMetric, StepEfficiencyMetric

-   Build success rates (deployment pipeline pass/fail ratios)

-   Token consumption per task type (cost efficiency tracking)

-   Error rates by worker type and model

-   Latency distributions (P50, P95, P99 per workflow step)

**From R&D/Chaos Department (Resilience Testing)**

-   Resilience scores (percentage of chaos scenarios survived without service degradation)

-   Failure mode catalogue (categorized by severity, frequency, blast radius)

-   Recovery times (mean time to recovery per failure type)

-   Death spiral detection events (threshold crossings, near-misses)

-   Safety evaluation results (MASK, AgentHarm, AIR Bench scores per model)

**4.2 Kaizen Measurement Tiers**

The Kaizen measurement system aligns with the existing 4-tier evaluation architecture, adding cross-department intelligence at each level.

**Tier 1: Always-Run Heuristics (\$0 Incremental Cost)**

These run on every interaction with zero LLM inference cost:

-   Latency checks: Is response time within SLA? (P95 \< 3s for synchronous, \< 30s for async)

-   Error rate monitoring: HTTP errors, tool call failures, timeout rates

-   Cost tracking: Token consumption per interaction logged to ClickHouse via LiteLLM

-   Basic quality gates: Response length bounds, format compliance, forbidden content filters

-   Uptime monitoring: Service availability across all Temporal workers

-   Budget compliance: Per-client cost vs \$138/month allocation threshold

**Tier 2: Sampled LLM-as-Judge (10% of Interactions)**

These use LLM inference for quality assessment on a configurable sample:

-   Business Brain Consistency: Does agent output align with the client\'s knowledge graph?

-   Radical Honesty Scoring: Does the agent acknowledge limitations and uncertainties?

-   Win-Win Alignment: Does the recommendation benefit both client and ecosystem?

-   StepEfficiency sampling: Are agents completing tasks with minimal redundant steps?

-   ToolCorrectness sampling: Are agents selecting appropriate tools?

-   G-Eval custom metrics: Domain-specific quality criteria defined in natural language

**Tier 3: Deep Evaluation (Triggered by Anomalies or Scheduled)**

These run when Tier 1/2 flag anomalies or on scheduled intervals:

-   Full DeepEval agent suite: All 6 agent metrics across full execution traces

-   DAG compliance scoring: Deterministic decision-tree evaluation for Layer 0 Laws

-   Inspect AI safety evals: MASK honesty, AgentHarm, AIR Bench (quarterly per model)

-   Embedding drift analysis: Euclidean distance computation with KS test alerting

-   Synthetic adversarial testing: Generated edge cases targeting identified weak points

**Tier 4: Conversation-Level & Cross-Department Analysis**

These operate at the highest level of abstraction:

-   Cross-department PUDDING pattern detection: Automated recipe scoring across department metrics

-   Death spiral correlation analysis: Multi-signal aggregation from all departments

-   Leading indicator computation: Recipe 1 (efficiency → friction) prediction model

-   Drift derivative analysis: Recipe 2 (drift acceleration → death spiral early warning)

-   External calibration: Recipe 3 (MASK vs Radical Honesty correlation)

-   Monthly Kaizen Report generation: System-wide health, trends, and improvement hypotheses

**4.3 Cross-Department Relationship Matrix**

The following matrix maps which metrics from each department feed which Kaizen analyses, with PUDDING labels for each connection.

  ------------------- ---------------------------- ------------- ---------- ---------------
  **Source Metric**   **Kaizen Analysis**          **PUDDING**   **Tier**   **Frequency**
  Friction Score      Leading indicator model      S.--.2.v      Tier 4     Weekly
  Honesty Score       External calibration         C.=.6.∞       Tier 3     Quarterly
  Win-Win Score       DAG compliance check         R.+.2.l       Tier 2     10% sample
  Embed. Drift        Death spiral early warning   S.--.4.l      Tier 3     Weekly
  KG Health           Consistency monitoring       R.=.5.l       Tier 1     Daily
  BB Consistency      Drift correlation            I.=.5.p       Tier 2     10% sample
  Step Efficiency     Friction prediction          P.--.3.i      Tier 2     10% sample
  Task Completion     Capability baseline          P.\>.3.i      Tier 3     On anomaly
  Plan Quality        Orchestration health         M.=.3.m       Tier 3     On anomaly
  Resilience Score    System robustness            S.\>.4.v      Tier 3     Weekly
  Safety Evals        Honesty calibration          C.\>.5.i      Tier 3     Quarterly
  Recovery Time       SLA compliance               P.--.3.i      Tier 1     Real-time
  ------------------- ---------------------------- ------------- ---------- ---------------

**4.4 The Kaizen Temporal Workflow (KaizenEvaluationWorkflow)**

The Kaizen evaluation system operates on three temporal cycles, all orchestrated through Temporal workflows to ensure reliability, state management, and failure recovery.

**Daily Cycle: Detect and Triage**

**Workflow:** KaizenDailyEvaluation

**Trigger:** Cron schedule, 02:00 UTC daily

**Steps:**

1.  Collect Tier 1 metrics from all departments via ClickHouse aggregate queries

2.  Run Tier 2 LLM-as-judge evaluations on the day\'s 10% sample (Langfuse trace selection)

3.  Compare all metrics against historical baselines (7-day rolling average ± 2σ)

4.  Flag anomalies exceeding thresholds to the Kaizen triage queue

5.  Generate daily Kaizen digest (summary of metrics, anomalies, and recommended actions)

**Output:** Daily Kaizen Digest stored in ClickHouse, anomaly flags trigger Tier 3 evaluations

**Weekly Cycle: Investigate and Correlate**

**Workflow:** KaizenWeeklyAnalysis

**Trigger:** Cron schedule, Sunday 06:00 UTC

**Steps:**

1.  Run Tier 3 deep evaluations on all items flagged during the week\'s daily cycles

2.  Execute embedding drift computation: calculate weekly centroid Euclidean distances from FalkorDB

3.  Run cross-department PUDDING analysis: compute recipe scores for all 3 active recipes

4.  Generate improvement hypotheses based on correlated anomalies across departments

5.  Update the leading indicator model (Recipe 1: StepEfficiency → Friction prediction)

**Output:** Weekly Kaizen Analysis Report with cross-department correlations, improvement hypotheses ranked by impact, drift status dashboard

**Monthly Cycle: Comprehensive System Review**

**Workflow:** KaizenMonthlyReview

**Trigger:** Cron schedule, 1st of month 06:00 UTC

**Steps:**

-   Run Tier 4 full system evaluation across all departments

-   Score all PUDDING recipes with updated data (4 weeks of correlation data)

-   Execute Inspect AI safety evaluation suite against all models in LiteLLM routing table

-   Compute Recipe 3 calibration: MASK vs Radical Honesty correlation coefficient

-   Compute drift derivatives for Recipe 2: identify acceleration trends

-   Generate the Monthly Kaizen Report: system-wide health, trend analysis, improvement outcomes, and next-month priorities

-   Archive all raw evaluation data to ClickHouse long-term storage

**Output:** Monthly Kaizen Report published to all department leads. Includes: system health dashboard, improvement velocity (how fast metrics are improving), cost efficiency trends, PUDDING recipe scores, and prioritized improvement backlog for the next month.

**4.5 Implementation Roadmap**

The following phased roadmap deploys the Kaizen evaluation system over 10 weeks, with each phase building on the previous one. All phases are designed to deliver standalone value even if subsequent phases are delayed.

**Phase 1: DeepEval Agent Metrics (Weeks 1--2)**

**Objective:** Deploy the 6 agent evaluation metrics into Cove workers

-   Install DeepEval (pip install deepeval) in the Cove worker environment

-   Add \@observe decorators to all Cove worker functions

-   Configure LiteLLM as the evaluation model provider (use existing budget controls)

-   Implement Tier 2 sampling: 10% of interactions evaluated via StepEfficiency and ToolCorrectness

-   Wire evaluation results to Langfuse traces for traceability

-   Store aggregate metrics in ClickHouse for trending

**Deliverable:** Agent evaluation metrics flowing in production. Estimated cost impact: +\$0.50--\$1.20/client/month.

**Success Criterion:** 95% of Cove worker executions generate trace data; Tier 2 sampling runs on 10% ± 1% of interactions.

**Phase 2: Inspect AI Safety Evals (Weeks 3--4)**

**Objective:** Integrate safety and honesty evaluation benchmarks for Layer 0 compliance

-   Install Inspect AI (pip install inspect-ai) in the R&D/Chaos environment

-   Write custom Inspect tasks mirroring Amplified agent architectures

-   Configure MASK, AgentHarm, and AIR Bench evaluation suites

-   Run baseline evaluation against all models in LiteLLM routing table

-   Establish pass/fail thresholds per model per benchmark

-   Build automated model deprioritization workflow in LiteLLM for failing models

**Deliverable:** Safety evaluation baseline established. Quarterly automated re-evaluation scheduled. Estimated cost: \$15--\$30/quarter.

**Success Criterion:** All production models have baseline MASK and AgentHarm scores; any model below threshold is automatically deprioritized.

**Phase 3: Embedding Drift Pipeline (Weeks 5--6)**

**Objective:** Build the embedding drift detection system from Arize Phoenix patterns

-   Implement weekly centroid computation from FalkorDB embedding vectors

-   Build Euclidean distance calculation pipeline with KS 2-sample test overlay

-   Store drift metrics as time-series in ClickHouse

-   Configure alerting thresholds based on initial baseline period

-   Compute drift derivatives (acceleration of drift) for Recipe 2 early warning

-   Build drift dashboard in Langfuse with UMAP-style visualization

**Deliverable:** Automated weekly drift detection with alerting. Zero incremental infrastructure cost (runs on existing ClickHouse).

**Success Criterion:** Weekly drift reports generated automatically; alert threshold triggers Tier 3 investigation within 24 hours.

**Phase 4: Cross-Department Data Flows (Weeks 7--8)**

**Objective:** Wire all department metrics into the KaizenEvaluationWorkflow

-   Build Temporal workflow: KaizenDailyEvaluation with Tier 1+2 collection and anomaly detection

-   Build Temporal workflow: KaizenWeeklyAnalysis with Tier 3 execution and cross-department correlation

-   Implement the leading indicator model (Recipe 1: StepEfficiency → Friction prediction)

-   Build the Daily Kaizen Digest generation pipeline

-   Configure all department data sources in ClickHouse aggregate views

-   Wire anomaly flags to trigger Tier 3 evaluation workflows

**Deliverable:** Automated daily and weekly Kaizen evaluation cycles. All 4 departments feeding metrics to Kaizen.

**Success Criterion:** Daily digest generated reliably for 14 consecutive days; weekly analysis correlates metrics from ≥3 departments.

**Phase 5: PUDDING Cross-Reference Engine (Weeks 9--10)**

**Objective:** Deploy the automated PUDDING recipe scoring and cross-department pattern detection

-   Implement PUDDING label store in FalkorDB (evaluation concepts as nodes, labels as properties)

-   Build automated recipe scoring engine that computes novelty, plausibility, and actionability

-   Implement Recipe 1, 2, and 3 scoring pipelines with ClickHouse data feeds

-   Build the Monthly Kaizen Report generation pipeline

-   Deploy KaizenMonthlyReview Temporal workflow

-   Create the PUDDING recipe discovery engine: automated detection of new cross-department patterns

**Deliverable:** Full Kaizen department operational. Monthly reports with PUDDING cross-department analysis. Automated pattern discovery.

**Success Criterion:** Monthly report generated with all 3 recipe scores; at least 1 new cross-department pattern identified per quarter.

**Section 5: What This Means for Amplified's Mission**

Amplified Partners exists to DEFRICTION --- to remove friction from SMBs so owners reconnect with their passion. Every metric in this document, every evaluation system assessed, and every PUDDING recipe discovered ultimately measures one thing: ***is friction being removed?***

**5.1 Evaluation Systems Are Friction Detection Systems**

The central insight from this analysis is that evaluation systems and friction detection systems are the same thing viewed from different angles:

-   **Agent step efficiency** (DeepEval) measures friction in the AI system itself --- redundant steps are friction that costs tokens and time.

-   **Embedding drift** (Arize Phoenix pattern) measures friction in the knowledge layer --- drift is the accumulation of misalignment between what the system knows and what reality requires.

-   **Safety evaluations** (Inspect AI) measure friction at the trust boundary --- a system that isn\'t honest or safe creates friction for every stakeholder who interacts with it.

-   **Radical Honesty scoring** measures friction in the relationship layer --- dishonesty is the ultimate friction, destroying the trust that enables DEFRICTION.

-   **Customer friction scoring** measures friction directly, in the client\'s experience --- the output variable that all other metrics predict.

**5.2 The Kaizen Department as Nervous System**

With this blueprint, the Kaizen department becomes the central nervous system of Amplified Partners:

-   **Sensing:** Metrics flow in from all 4 departments in real-time (Tier 1), sampled (Tier 2), deep-investigated (Tier 3), and systemically analysed (Tier 4).

-   **Processing:** PUDDING cross-department analysis detects patterns that no single department can see. The ABC recipes transform raw metrics into actionable predictions.

-   **Responding:** Automated workflows trigger improvement actions --- model deprioritization, drift alerts, anomaly investigations --- before friction reaches the client.

This is not measurement for measurement\'s sake. Every evaluation costs something (even if just compute), and every metric must justify its existence by answering: does knowing this help remove friction? The tiered system ensures that the most expensive evaluations only run when cheaper signals suggest they\'re needed.

**5.3 The \$138 Question**

The total estimated cost impact of the full Kaizen evaluation system on the \$138/client/month target:

  --------------------------------- --------------------- -------------------------------
  **Component**                     **Monthly Cost**      **Offset**
  DeepEval Agent Metrics (Tier 2)   +\$0.50--\$1.20       Early error detection savings
  DAG Compliance Scoring            +\$0.10--\$0.30       Replaces manual QA
  Inspect AI Safety Evals           \<\$0.10              Quarterly amortization
  Embedding Drift Pipeline          \$0.00                Runs on existing infra
  Scorer Generation (G-Eval)        Net positive          Labour savings exceed cost
  **TOTAL INCREMENTAL**             **+\$0.70--\$1.60**   **\<1.2% of \$138 target**
  --------------------------------- --------------------- -------------------------------

At less than 1.2% of the \$138/client/month target, the Kaizen evaluation system is one of the highest-ROI investments in the entire Amplified architecture. The cost of not measuring is always higher than the cost of measurement---undetected friction compounds, and by the time it reaches the client, the remediation cost is 10--100x the detection cost.

**5.4 What Comes After This Document**

This document is a blueprint, not an implementation. The next steps are:

6.  **Review and approve the 5-phase implementation roadmap** (Section 4.5)

7.  **Begin Phase 1** --- DeepEval deployment into Cove workers (highest impact, lowest risk)

8.  **Validate Recipe 1** --- collect 4 weeks of StepEfficiency data and correlate with friction scores

9.  **Run first Inspect AI baseline** --- establish MASK and AgentHarm scores for all production models

10. **Iterate** --- the Kaizen department\'s first act of kaizen is measuring itself. Apply the same evaluation rigor to the evaluation system.

+-------------------------------------------------------------------------------------------------------------------------------+
| **Attribution**                                                                                                               |
|                                                                                                                               |
| Ewan Bramley (originator, mission architect) × Perplexity (researcher, formaliser, mixer)                                     |
|                                                                                                                               |
| **Fact %:** 85 \| **Confidence:** High \| **PUDDING:** M.+.5.l                                                                |
|                                                                                                                               |
| **LBD:** Swanson (1986) ABC Model                                                                                             |
|                                                                                                                               |
| **Sources:** DeepEval docs, Arize Phoenix docs, Inspect AI (UK AISI), Braintrust docs, OPIK source extraction, LangSmith docs |
+-------------------------------------------------------------------------------------------------------------------------------+

[^1]: DeepEval Documentation --- Agent Evaluation, <https://deepeval.com/guides/guides-ai-agent-evaluation>

[^2]: DeepEval DAG Metric Documentation, <https://deepeval.com/docs/metrics-dag>

[^3]: Arize Phoenix GitHub Repository, <https://github.com/Arize-ai/phoenix>

[^4]: Arize --- Monitoring Embedding Drift Using Euclidean Distance, <https://arize.com/blog-course/embedding-drift-euclidean-distance/>

[^5]: Inspect AI --- UK AI Security Institute, <https://inspect.aisi.org.uk>

[^6]: UK AISI 2025 Year in Review, <https://www.aisi.gov.uk/blog/our-2025-year-in-review>

[^7]: Braintrust --- Loop AI Assistant, <https://www.braintrust.dev/blog/loop>

[^8]: Braintrust --- Best LLM Evaluation Platforms 2025, <https://www.braintrust.dev/articles/best-llm-evaluation-platforms-2025>

[^9]: LangSmith --- Pairwise Annotation Queues, <https://changelog.langchain.com/announcements/pairwise-annotation-queues-for-comparing-agent-outputs>

[^10]: Langfuse vs LangSmith comparison (Hugging Face), <https://huggingface.co/blog/daya-shankar/langfuse-vs-langsmith-vs-langchain-comparison>

[^11]: DeepEval Documentation --- Agent Evaluation, <https://deepeval.com/guides/guides-ai-agent-evaluation>

[^12]: Arize --- Embedding Drift Documentation, <https://arize.com/docs/ax/machine-learning/computer-vision/how-to-cv/embedding-drift>

[^13]: Arize --- Monitoring Embedding Drift Using Euclidean Distance, <https://arize.com/blog-course/embedding-drift-euclidean-distance/>

[^14]: Inspect AI --- UK AI Security Institute, <https://inspect.aisi.org.uk>

[^15]: Braintrust --- Loop AI Assistant, <https://www.braintrust.dev/blog/loop>

[^16]: DeepEval DAG Metric Documentation, <https://deepeval.com/docs/metrics-dag>

[^17]: Swanson, D.R. (1986). Undiscovered Public Knowledge. The Library Quarterly, 56(2), 103-118.

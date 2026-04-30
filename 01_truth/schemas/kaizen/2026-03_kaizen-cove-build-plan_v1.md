---
title: "Kaizen Cove Build Plan"
id: "kaizen-cove-build-plan"
version: 1
created: 2026-04-25
last_validated: 2026-04-25
type: document
topic_type: reference
status: imported
source_file: "kaizen-cove-build-plan.docx"
signed_by: "Devon, 2026-04-25, devin-992682c244cf444f91e0a516498afbfd"
---

**KAIZEN EVALUATION ENGINE**

Cove Build Plan

*Linear Issues, Task DAGs, and Implementation Specifications*

  -------------------- ----------------------------------------------
  **For**              Cove Code Factory / Amplified Partners
  **Date**             March 2026
  **Classification**   Build Reference --- Machine & Human Readable
  **Linear Prefix**    COV-290 through COV-313
  -------------------- ----------------------------------------------

**1. Build Plan Overview**

This build plan implements the Kaizen Evaluation Engine --- a 5-phase, 10-week programme that transforms the Kaizen department from concept to operational within the Amplified Partners AI ecosystem. It delivers comprehensive agent evaluation, safety testing, embedding drift detection, cross-department data flows, and automated pattern discovery through the PUDDING cross-reference engine.

The implementation is structured as 24 Linear issues (COV-290 through COV-313) with explicit task dependencies, acceptance criteria, and code specifications designed for execution by Cove --- the Amplified Partners AI code factory.

**Key Metrics**

  ---------------------------- ----------------------------------------------------
  **Metric**                   **Value**
  Total Linear Issues          24 (COV-290 to COV-313)
  Estimated Lines of Code      \~3,500--4,500
  Estimated Cove Build Hours   \~25--35 hours
  Human Hours Required         \~6--8 hours (reviews, approvals, config)
  Phases                       5 sequential phases over 10 weeks
  New Temporal Workflows       4 (Daily, Weekly, Monthly, Model Deprioritization)
  New Temporal Activities      15
  New ClickHouse Tables        6
  New Python Modules           \~15 files
  ---------------------------- ----------------------------------------------------

**Infrastructure Dependencies (All Met)**

All required infrastructure components are already deployed and operational on the Hetzner Beast server (48-core EPYC, 256 GB RAM):

  -------------------------- -------------------------------------- ------------
  **Component**              **Endpoint**                           **Status**
  Temporal Server            cove-temporal:7233                     Deployed
  Langfuse                   langfuse.beast.amplifiedpartners.ai    Deployed
  ClickHouse                 clickhouse:8123                        Deployed
  LiteLLM                    litellm:4000                           Deployed
  FalkorDB                   falkordb:6379                          Deployed
  Ollama (local inference)   ollama:11434                           Deployed
  SearXNG                    search.beast.amplifiedpartners.ai      Deployed
  Cove API Gateway           cove.beast.amplifiedpartners.ai:8081   Deployed
  -------------------------- -------------------------------------- ------------

**Phase Timeline**

  ----------- -------------------------------- -------------- --------------
  **Phase**   **Scope**                        **Issues**     **Duration**
  1           DeepEval Agent Metrics           COV-290--295   Weeks 1--2
  2           Inspect AI Safety Evaluations    COV-296--300   Weeks 3--4
  3           Embedding Drift Pipeline         COV-301--304   Weeks 5--6
  4           Cross-Department Data Flows      COV-305--309   Weeks 7--9
  5           PUDDING Cross-Reference Engine   COV-310--313   Weeks 9--10
  ----------- -------------------------------- -------------- --------------

**2. Phase 1: DeepEval Agent Metrics**

Phase 1 integrates DeepEval into the Cove worker environment, enabling automated Tier 2 sampling of agent executions for quality metrics. This phase establishes the foundational evaluation pipeline that all subsequent phases build upon.

Issues: COV-290 through COV-295 \| Duration: Weeks 1--2 \| Estimated LOC: \~605 \| Estimated Build Time: \~10--14 hours

**COV-290: Install DeepEval in Cove Worker Environment**

**Priority: High**

**Type:** Infrastructure

**Dependencies:** None

**Estimated LOC:** \~15 (requirements + Dockerfile changes)

**Estimated Build Time:** 30 minutes

**File Targets:** requirements.txt, Dockerfile

**Description**

Add deepeval to the Cove worker Docker image. Update requirements.txt and rebuild. Verify that the package is importable in all worker containers and can communicate with LiteLLM for judge model access.

**Acceptance Criteria**

> 1\. deepeval importable in all Cove worker containers
>
> 2\. DeepEval can reach LiteLLM at litellm:4000 for judge models
>
> 3\. No regression in existing worker startup time (\< 30s)

**COV-291: Implement \@observe Decorators on Cove Worker Functions**

**Priority: High**

**Type:** Feature

**Dependencies:** COV-290

**Estimated LOC:** \~120

**Estimated Build Time:** 2--3 hours

**File Targets:** agents/agent\_loop.py, new file agents/tracing.py

**Description**

Add DeepEval \@observe decorators to all agent execution functions in agent\_loop.py. Capture full execution traces including tool calls, LLM responses, and timing. Every agent execution (coder, reviewer, enforcer, architect, security) must generate a trace.

**Acceptance Criteria**

> 1\. Every agent execution (coder, reviewer, enforcer, architect, security) generates a trace
>
> 2\. Traces include: input prompt, all LLM calls, all tool calls with arguments, final output, total tokens, total cost
>
> 3\. Traces are stored in a format compatible with DeepEval\'s evals\_iterator
>
> 4\. 95%+ of executions generate valid trace data (measured over 24h)

**COV-292: Deploy Tier 2 Sampling --- StepEfficiency & ToolCorrectness**

**Priority: High**

**Type:** Feature

**Dependencies:** COV-291

**Estimated LOC:** \~200

**Estimated Build Time:** 3--4 hours

**File Targets:** new file evaluation/tier2\_sampler.py, new file evaluation/metrics.py

**Description**

Implement 10% sampling of agent executions for StepEfficiencyMetric and ToolCorrectnessMetric evaluation. Use Langfuse trace selection to pick the 10% sample. Run evaluations asynchronously --- do not block agent execution. Write results to both Langfuse (as trace scores) and ClickHouse.

**Acceptance Criteria**

> 1\. Exactly 10% ± 1% of executions are sampled for evaluation
>
> 2\. StepEfficiencyMetric runs on sampled traces and produces score 0--1
>
> 3\. ToolCorrectnessMetric runs on sampled traces and produces score 0--1
>
> 4\. Evaluation runs asynchronously --- zero latency impact on agent execution
>
> 5\. Results are written to Langfuse as evaluation scores attached to the original trace
>
> 6\. Results are also written to ClickHouse table kaizen.tier2\_evaluations

**COV-293: Configure LiteLLM as DeepEval Judge Model Provider**

**Priority: Medium**

**Type:** Configuration

**Dependencies:** COV-290

**Estimated LOC:** \~40

**Estimated Build Time:** 1 hour

**File Targets:** new file evaluation/config.py

**Description**

Configure DeepEval to use LiteLLM (litellm:4000) as its model provider for all LLM-as-judge evaluations. Use local/llama3.1-8b for Tier 2 evaluations (fast, zero external API cost) and claude-sonnet via LiteLLM for Tier 3 evaluations (higher quality). Ensure LiteLLM budget controls apply to evaluation calls.

**Acceptance Criteria**

> 1\. DeepEval judge calls route through LiteLLM (visible in Langfuse traces)
>
> 2\. Tier 2 evaluations use local/llama3.1-8b (zero external API cost)
>
> 3\. Tier 3 evaluations use claude-sonnet via LiteLLM
>
> 4\. LiteLLM budget controls apply to evaluation calls (included in workflow \$50 cap)

**COV-294: Build ClickHouse Kaizen Schema**

**Priority: High**

**Type:** Database

**Dependencies:** None (ClickHouse already running)

**Estimated LOC:** \~80 (DDL + migration script)

**Estimated Build Time:** 1--2 hours

**File Targets:** migrations/kaizen\_schema.sql

**Description**

Create ClickHouse tables for Kaizen evaluation data. Use ClickHouse\'s MergeTree engine for time-series metric storage. Create 6 tables: tier1\_metrics, tier2\_evaluations, tier3\_evaluations, tier4\_cross\_department, drift\_metrics, and daily\_digests.

**Code / DDL:**

> CREATE DATABASE IF NOT EXISTS kaizen;
>
> CREATE TABLE kaizen.tier1\_metrics (
>
> timestamp DateTime64(3),
>
> department LowCardinality(String),
>
> metric\_name LowCardinality(String),
>
> metric\_value Float64,
>
> client\_id Nullable(String),
>
> agent\_role Nullable(LowCardinality(String)),
>
> workflow\_id Nullable(String),
>
> metadata String DEFAULT \'{}\'
>
> ) ENGINE = MergeTree()
>
> ORDER BY (department, metric\_name, timestamp)
>
> PARTITION BY toYYYYMM(timestamp)
>
> TTL timestamp + INTERVAL 2 YEAR;
>
> CREATE TABLE kaizen.tier2\_evaluations (
>
> timestamp DateTime64(3),
>
> trace\_id String,
>
> agent\_role LowCardinality(String),
>
> metric\_name LowCardinality(String),
>
> score Float64,
>
> reason String,
>
> model\_used LowCardinality(String),
>
> tokens\_used UInt32,
>
> cost\_usd Float64,
>
> client\_id Nullable(String)
>
> ) ENGINE = MergeTree()
>
> ORDER BY (metric\_name, timestamp)
>
> PARTITION BY toYYYYMM(timestamp);
>
> CREATE TABLE kaizen.tier3\_evaluations (
>
> timestamp DateTime64(3),
>
> evaluation\_suite LowCardinality(String),
>
> metric\_name LowCardinality(String),
>
> score Float64,
>
> details String,
>
> model\_evaluated LowCardinality(String),
>
> triggered\_by LowCardinality(String),
>
> cost\_usd Float64
>
> ) ENGINE = MergeTree()
>
> ORDER BY (evaluation\_suite, metric\_name, timestamp)
>
> PARTITION BY toYYYYMM(timestamp);
>
> CREATE TABLE kaizen.tier4\_cross\_department (
>
> timestamp DateTime64(3),
>
> recipe\_name LowCardinality(String),
>
> recipe\_score Float64,
>
> novelty\_score Float64,
>
> plausibility\_score Float64,
>
> actionability\_score Float64,
>
> source\_department LowCardinality(String),
>
> target\_department LowCardinality(String),
>
> pudding\_label\_source String,
>
> pudding\_label\_target String,
>
> details String
>
> ) ENGINE = MergeTree()
>
> ORDER BY (recipe\_name, timestamp)
>
> PARTITION BY toYYYYMM(timestamp);
>
> CREATE TABLE kaizen.drift\_metrics (
>
> timestamp DateTime64(3),
>
> embedding\_source LowCardinality(String),
>
> centroid\_distance Float64,
>
> ks\_statistic Float64,
>
> ks\_p\_value Float64,
>
> is\_drift\_detected UInt8,
>
> baseline\_period\_start DateTime64(3),
>
> baseline\_period\_end DateTime64(3),
>
> comparison\_period\_start DateTime64(3),
>
> comparison\_period\_end DateTime64(3)
>
> ) ENGINE = MergeTree()
>
> ORDER BY (embedding\_source, timestamp)
>
> PARTITION BY toYYYYMM(timestamp);
>
> CREATE TABLE kaizen.daily\_digests (
>
> date Date,
>
> digest\_json String,
>
> anomaly\_count UInt16,
>
> tier1\_metrics\_collected UInt32,
>
> tier2\_evaluations\_run UInt32,
>
> departments\_reporting Array(String)
>
> ) ENGINE = MergeTree()
>
> ORDER BY date;

**Acceptance Criteria**

> 1\. All 6 tables created successfully in ClickHouse
>
> 2\. Insert + query round-trip works for each table
>
> 3\. Partitioning verified (2-year TTL on tier1\_metrics)
>
> 4\. Aggregate views created for common Kaizen queries

**COV-295: Wire Evaluation Results to Langfuse + ClickHouse**

**Priority: Medium**

**Type:** Integration

**Dependencies:** COV-292, COV-294

**Estimated LOC:** \~150

**Estimated Build Time:** 2--3 hours

**File Targets:** new file evaluation/writers.py

**Description**

Build the data pipeline that writes evaluation results to both Langfuse (as trace scores) and ClickHouse (for trending). Implement dual-write with ClickHouse as primary and Langfuse as secondary. If Langfuse write fails, do not block the ClickHouse write.

**Acceptance Criteria**

> 1\. Every Tier 2 evaluation result appears in both Langfuse and ClickHouse
>
> 2\. Langfuse shows evaluation scores alongside the original agent trace
>
> 3\. ClickHouse kaizen.tier2\_evaluations table receives all results within 5 seconds
>
> 4\. Langfuse write failure does not block ClickHouse write
>
> 5\. Dashboard query: \'average StepEfficiency by agent role, last 7 days\' returns results in \< 1s

**3. Phase 2: Inspect AI Safety Evaluations**

Phase 2 establishes safety evaluation capabilities through Inspect AI, running in a dedicated container isolated from production. This phase tests all production models against Layer 0 compliance standards and community safety benchmarks.

Issues: COV-296 through COV-300 \| Duration: Weeks 3--4 \| Estimated LOC: \~620 \| Estimated Build Time: \~11--16 hours

**COV-296: Install Inspect AI in R&D/Chaos Environment**

**Priority: High**

**Type:** Infrastructure

**Dependencies:** None

**Estimated LOC:** \~30 (Dockerfile + compose)

**Estimated Build Time:** 1 hour

**File Targets:** docker/inspect-ai/Dockerfile, docker-compose.inspect.yml

**Description**

Install inspect-ai in a dedicated evaluation container (not in production Cove workers). This container runs in the amplified-net network with access to LiteLLM but is isolated from production agent execution. Configure Traefik label for inspect.beast.amplifiedpartners.ai (internal access only).

**Acceptance Criteria**

> 1\. inspect-ai installed and functional in dedicated container
>
> 2\. Container can reach litellm:4000 for model access
>
> 3\. inspect eval CLI works with all models in LiteLLM routing table
>
> 4\. Container has Traefik label for inspect.beast.amplifiedpartners.ai (internal access)

**COV-297: Write Custom Inspect Tasks for Amplified Agent Patterns**

**Priority: High**

**Type:** Feature

**Dependencies:** COV-296

**Estimated LOC:** \~300

**Estimated Build Time:** 4--5 hours

**File Targets:** new directory evaluation/inspect\_tasks/

**Description**

Create custom Inspect evaluation tasks that mirror Amplified\'s specific agent architectures and Layer 0 Laws. Build tasks for: (1) Radical Honesty --- does the agent admit uncertainty? (2) Win-Win --- does it recommend actions that benefit both parties? (3) White Hat --- does it avoid exploitative tactics? (4) Help Not Hurt --- does it recommend competitors when appropriate? Each task must have 20+ test cases derived from real Amplified agent scenarios.

**Acceptance Criteria**

> 1\. 4 custom Inspect tasks created, one per Layer 0 Law being tested
>
> 2\. Each task has 20+ test cases derived from real Amplified agent scenarios
>
> 3\. Tasks produce scores compatible with ClickHouse kaizen.tier3\_evaluations
>
> 4\. Tasks run against any model via inspect eval \--model \<model\>

**COV-298: Configure MASK, AgentHarm, and AIR Bench Suites**

**Priority: Medium**

**Type:** Configuration

**Dependencies:** COV-296

**Estimated LOC:** \~60

**Estimated Build Time:** 2 hours (mostly waiting for eval runs)

**File Targets:** evaluation/inspect\_config/benchmarks.py

**Description**

Install and configure the community-contributed MASK (honesty), AgentHarm (harmful tool use), and AIR Bench (AI risk) evaluation suites from inspect\_evals. These provide external calibration for Amplified\'s custom metrics. Establish baseline scores for all models in the LiteLLM routing table.

**Acceptance Criteria**

> 1\. inspect\_evals package installed with MASK, AgentHarm, AIR Bench
>
> 2\. Baseline scores established for all models: llama3.1-8b, llama3.1-70b, claude-sonnet, claude-opus, gpt-4.1-mini
>
> 3\. Results stored in ClickHouse kaizen.tier3\_evaluations
>
> 4\. Pass/fail thresholds defined per model per benchmark

**COV-299: Build Model Deprioritization Workflow**

**Priority: Medium**

**Type:** Feature

**Dependencies:** COV-298

**Estimated LOC:** \~180

**Estimated Build Time:** 3--4 hours

**File Targets:** new file temporal/workflows/model\_deprioritization.py, new activity in temporal/activities/safety.py

**Description**

Build a Temporal workflow that automatically deprioritizes models in LiteLLM when they fail safety benchmarks. When a model scores below threshold on MASK, AgentHarm, or AIR Bench, the workflow: (1) sends a Telegram alert, (2) reduces the model\'s weight in LiteLLM routing, (3) creates a Linear issue for investigation.

**Acceptance Criteria**

> 1\. Temporal workflow ModelDeprioritizationWorkflow registered and functional
>
> 2\. Workflow triggers on Tier 3 evaluation failure (score below threshold)
>
> 3\. Telegram alert sent within 60 seconds of detection
>
> 4\. LiteLLM config updated to reduce failing model\'s routing weight
>
> 5\. Linear issue created automatically with evaluation details

**COV-300: Schedule Quarterly Safety Evaluation Cron**

**Priority: Low**

**Type:** Configuration

**Dependencies:** COV-297, COV-298

**Estimated LOC:** \~50

**Estimated Build Time:** 1 hour

**File Targets:** temporal/schedules/safety\_quarterly.py

**Description**

Configure a Temporal schedule that runs the full Inspect AI safety suite quarterly against all production models. Results feed into the Monthly Kaizen Report. Schedule runs on the 1st of January, April, July, and October at 03:00 UTC.

**Acceptance Criteria**

> 1\. Temporal schedule created: runs 1st of Jan/Apr/Jul/Oct at 03:00 UTC
>
> 2\. Evaluates all 5 models against MASK, AgentHarm, AIR Bench, and 4 custom tasks
>
> 3\. Results stored in ClickHouse with triggered\_by = \'schedule\'
>
> 4\. Results compared against previous quarter\'s baseline (regression detection)

**4. Phase 3: Embedding Drift Pipeline**

Phase 3 builds the embedding drift detection pipeline inspired by Arize Phoenix patterns. It computes weekly centroids from FalkorDB knowledge graph vectors, detects statistically significant drift using the Kolmogorov-Smirnov test, and computes drift derivatives for early-warning spiral detection.

Issues: COV-301 through COV-304 \| Duration: Weeks 5--6 \| Estimated LOC: \~450 \| Estimated Build Time: \~7--10 hours

**COV-301: Implement Weekly Centroid Computation from FalkorDB**

**Priority: High**

**Type:** Feature

**Dependencies:** COV-294

**Estimated LOC:** \~150

**Estimated Build Time:** 2--3 hours

**File Targets:** new file evaluation/drift/centroid.py

**Description**

Build a pipeline that computes weekly embedding centroids from FalkorDB\'s knowledge graph vectors. For each embedding source (Business Brain, client knowledge graphs), compute the centroid of all embedding vectors as a baseline and weekly comparison point. Use numpy for vector operations (efficient on Beast\'s 48 cores).

**Technical Specification**

> Query FalkorDB for all embedding vectors in a given date range
>
> Compute centroid (mean vector) per source
>
> Store centroids in ClickHouse kaizen.drift\_metrics
>
> Use numpy for vector operations (efficient on Beast\'s 48 cores)

**Acceptance Criteria**

> 1\. Centroid computation completes in \< 60 seconds for up to 100K vectors
>
> 2\. Centroids stored with timestamp and source identifier
>
> 3\. Works with FalkorDB\'s internal-only access (falkordb:6379)
>
> 4\. Handles missing data gracefully (new knowledge graphs with \< 100 vectors)

**COV-302: Build Euclidean Distance + KS Test Pipeline**

**Priority: High**

**Type:** Feature

**Dependencies:** COV-301

**Estimated LOC:** \~120

**Estimated Build Time:** 2--3 hours

**File Targets:** new file evaluation/drift/detector.py

**Description**

Implement the drift detection algorithm: compute Euclidean distance between current week\'s centroid and baseline centroid. Overlay with Kolmogorov-Smirnov 2-sample test for statistical rigour. Alert when drift exceeds threshold.

**Technical Specification**

> Euclidean distance: sqrt(sum((c\_current - c\_baseline)\^2))
>
> KS test: Compare distribution of individual vector distances to baseline distribution
>
> Threshold: KS p-value \< 0.05 = significant drift
>
> Alert: Telegram notification + anomaly flag in ClickHouse

**Acceptance Criteria**

> 1\. Euclidean distance computed and stored weekly
>
> 2\. KS test overlay provides statistical significance
>
> 3\. is\_drift\_detected flag set when p-value \< 0.05
>
> 4\. Telegram alert fires within 5 minutes of drift detection
>
> 5\. Results stored in ClickHouse kaizen.drift\_metrics

**COV-303: Build Drift Derivative Computation (Recipe 2)**

**Priority: Medium**

**Type:** Feature

**Dependencies:** COV-302

**Estimated LOC:** \~100

**Estimated Build Time:** 2 hours

**File Targets:** extends evaluation/drift/detector.py

**Description**

Compute the rate of change of drift over time (drift derivative). When drift is accelerating (second derivative positive), this is an early warning for Recipe 2 (drift → death spiral). Integrate with the death spiral scoring engine from the Finance Engine.

**Acceptance Criteria**

> 1\. Weekly drift derivative computed (change in Euclidean distance week-over-week)
>
> 2\. Drift acceleration detected (positive second derivative over 3+ consecutive weeks)
>
> 3\. Death spiral correlation: drift acceleration × finance engine death spiral score
>
> 4\. Correlation stored in ClickHouse kaizen.tier4\_cross\_department

**COV-304: Schedule Weekly Drift Analysis Temporal Workflow**

**Priority: Medium**

**Type:** Infrastructure

**Dependencies:** COV-301, COV-302, COV-303

**Estimated LOC:** \~80

**Estimated Build Time:** 1--2 hours

**File Targets:** new file temporal/workflows/drift\_analysis.py, new activity temporal/activities/drift.py

**Description**

Create a Temporal schedule for the weekly drift analysis pipeline. Runs every Sunday at 04:00 UTC. Collects centroids, computes distances, runs KS test, computes derivatives, and stores all results. Must complete before the KaizenWeeklyAnalysis workflow runs at 06:00 UTC.

**Acceptance Criteria**

> 1\. Temporal schedule created: runs Sunday 04:00 UTC
>
> 2\. Full pipeline executes in \< 5 minutes
>
> 3\. Results available in ClickHouse before the KaizenWeeklyAnalysis workflow runs (06:00 UTC)
>
> 4\. Failure → retry once, then Telegram alert

**5. Phase 4: Cross-Department Data Flows**

Phase 4 builds the core Temporal workflows that orchestrate the Kaizen evaluation system: daily evaluation, weekly analysis, anomaly-to-investigation pipelines, and the leading indicator predictive model. This phase integrates outputs from all previous phases into a coherent operational system.

Issues: COV-305 through COV-309 \| Duration: Weeks 7--9 \| Estimated LOC: \~1,040 \| Estimated Build Time: \~16--20 hours

**COV-305: Build KaizenDailyEvaluation Temporal Workflow**

**Priority: High**

**Type:** Feature

**Dependencies:** COV-292, COV-294, COV-295

**Estimated LOC:** \~350

**Estimated Build Time:** 5--6 hours

**File Targets:** new file temporal/workflows/kaizen\_daily.py, new activities in temporal/activities/kaizen.py

**Description**

The main daily Kaizen workflow. Runs at 02:00 UTC. Collects Tier 1 metrics from all departments, runs Tier 2 evaluations on the day\'s sample, compares against baselines, flags anomalies, and generates the daily digest.

**Technical Specification**

> Activity 1: collect\_tier1\_metrics --- ClickHouse aggregate queries across all departments
>
> Activity 2: run\_tier2\_evaluations --- Select 10% sample from Langfuse, run DeepEval metrics
>
> Activity 3: compare\_baselines --- 7-day rolling average ± 2σ comparison
>
> Activity 4: flag\_anomalies --- Write anomaly flags, trigger Tier 3 if needed
>
> Activity 5: generate\_daily\_digest --- Compile summary, store in kaizen.daily\_digests

**Acceptance Criteria**

> 1\. Workflow runs daily at 02:00 UTC without manual intervention
>
> 2\. Collects metrics from ≥3 departments (Real, Data, Cove minimum)
>
> 3\. Anomaly detection uses 7-day rolling average ± 2σ
>
> 4\. Daily digest generated and stored within 15 minutes of trigger
>
> 5\. Anomaly flag triggers child workflow for Tier 3 investigation

**COV-306: Build KaizenWeeklyAnalysis Temporal Workflow**

**Priority: High**

**Type:** Feature

**Dependencies:** COV-305, COV-304

**Estimated LOC:** \~300

**Estimated Build Time:** 4--5 hours

**File Targets:** new file temporal/workflows/kaizen\_weekly.py, extends temporal/activities/kaizen.py

**Description**

The weekly Kaizen analysis workflow. Runs Sunday 06:00 UTC. Runs Tier 3 deep evaluations on flagged items, executes drift analysis, runs cross-department PUDDING analysis, and generates improvement hypotheses.

**Technical Specification**

> Activity 1: run\_tier3\_evaluations --- Full DeepEval suite on flagged traces
>
> Activity 2: collect\_drift\_results --- Read weekly drift metrics from COV-304
>
> Activity 3: run\_pudding\_analysis --- Compute recipe scores for 3 active recipes
>
> Activity 4: generate\_hypotheses --- LLM-generated improvement hypotheses from correlated anomalies
>
> Activity 5: generate\_weekly\_report --- Compile weekly Kaizen analysis report

**Acceptance Criteria**

> 1\. Workflow runs Sunday 06:00 UTC
>
> 2\. Processes all anomalies flagged during the week
>
> 3\. Includes drift analysis results
>
> 4\. PUDDING recipe scores computed and stored
>
> 5\. Weekly report generated with cross-department correlations

**COV-307: Implement Leading Indicator Model (Recipe 1)**

**Priority: Medium**

**Type:** Feature

**Dependencies:** COV-292 (needs 4 weeks of data collection first)

**Estimated LOC:** \~120

**Estimated Build Time:** 2--3 hours

**File Targets:** new file evaluation/recipes/efficiency\_friction.py

**Description**

Build the predictive model for Recipe 1: StepEfficiency → Customer Friction. Uses linear regression on 4 weeks of historical data to predict friction score changes from step efficiency changes. This is the \'2--3 week leading indicator\' identified in the PUDDING analysis.

**Technical Specification**

> Input: StepEfficiencyMetric scores from kaizen.tier2\_evaluations
>
> Output: Predicted friction delta, stored in kaizen.tier4\_cross\_department
>
> Model: Simple linear regression (scikit-learn), retrained weekly
>
> Validation: Compare predicted vs actual friction with 4-week lag

**Acceptance Criteria**

> 1\. Model trained on minimum 4 weeks of data
>
> 2\. Prediction stored weekly in ClickHouse
>
> 3\. Model quality metric (R²) tracked over time
>
> 4\. If R² \< 0.3, flag as \'insufficient signal\' and alert

**COV-308: Build Department Data Source Aggregate Views**

**Priority: Medium**

**Type:** Database

**Dependencies:** COV-294

**Estimated LOC:** \~120

**Estimated Build Time:** 2--3 hours

**File Targets:** migrations/kaizen\_views.sql

**Description**

Create ClickHouse materialised views that aggregate metrics from each department into a standardised format for Kaizen consumption. Each view provides a consistent interface regardless of how each department stores its raw data.

**Technical Specification**

> kaizen.v\_real\_metrics --- Customer friction, honesty scores, win-win scores
>
> kaizen.v\_data\_metrics --- KG health, embedding drift, BB consistency
>
> kaizen.v\_cove\_metrics --- Agent metrics, build success, plan quality
>
> kaizen.v\_chaos\_metrics --- Resilience scores, failure modes, recovery times
>
> kaizen.v\_all\_departments --- Union of all 4 views

**Acceptance Criteria**

> 1\. All 5 views created and queryable
>
> 2\. v\_all\_departments returns data from ≥3 departments
>
> 3\. Views refresh automatically (materialised with 5-minute interval)
>
> 4\. Dashboard query: \'department health summary, last 24h\' returns in \< 1s

**COV-309: Wire Anomaly Flags to Trigger Tier 3 Workflows**

**Priority: Medium**

**Type:** Feature

**Dependencies:** COV-305

**Estimated LOC:** \~150

**Estimated Build Time:** 2--3 hours

**File Targets:** extends temporal/workflows/kaizen\_daily.py

**Description**

Build the anomaly → investigation pipeline. When KaizenDailyEvaluation flags an anomaly, it should trigger a child Temporal workflow that runs the appropriate Tier 3 evaluation (full DeepEval suite, Inspect AI safety, or drift analysis depending on anomaly type).

**Acceptance Criteria**

> 1\. Anomaly type determines which Tier 3 evaluation runs
>
> 2\. Child workflow triggered within 5 minutes of anomaly flag
>
> 3\. Tier 3 results written to kaizen.tier3\_evaluations
>
> 4\. If Tier 3 confirms the issue, Telegram alert + Linear issue creation
>
> 5\. If Tier 3 shows false positive, anomaly marked as resolved

**6. Phase 5: PUDDING Cross-Reference Engine**

Phase 5 implements the PUDDING (Purpose, Understanding, Data, Direction, Integration, Novelty, Growth) cross-reference engine --- the \'slime mould logic\' that explores all paths between evaluation concepts across departments and reinforces those that find value. This phase delivers automated pattern detection and the monthly review workflow.

Issues: COV-310 through COV-313 \| Duration: Weeks 9--10 \| Estimated LOC: \~800 \| Estimated Build Time: \~11--14 hours

**COV-310: Implement PUDDING Label Store in FalkorDB**

**Priority: Medium**

**Type:** Feature

**Dependencies:** None (FalkorDB already running)

**Estimated LOC:** \~150

**Estimated Build Time:** 2--3 hours

**File Targets:** new file evaluation/pudding/label\_store.py

**Description**

Create a PUDDING label graph in FalkorDB. Store evaluation concepts as nodes with WHAT.HOW.SCALE.TIME labels as properties. Build edges between concepts that share label components for pattern matching.

**Technical Specification**

> Node EvaluationConcept: name, department, pudding\_label, what, how, scale, time, description
>
> Edge SHARES\_LABEL: connects concepts sharing ≥2 label components
>
> Edge RECIPE: connects A→B→C chains

**Acceptance Criteria**

> 1\. 12 initial evaluation concepts loaded (from Kaizen Intelligence spec)
>
> 2\. SHARES\_LABEL edges computed automatically when concepts are added
>
> 3\. Cypher query: \'find all concepts sharing HOW across different departments\' returns results in \< 100ms
>
> 4\. Graph queryable from Kaizen workflows via falkordb:6379

**COV-311: Build Automated Recipe Scoring Engine**

**Priority: Medium**

**Type:** Feature

**Dependencies:** COV-310, COV-306

**Estimated LOC:** \~200

**Estimated Build Time:** 3--4 hours

**File Targets:** new file evaluation/pudding/recipe\_scorer.py

**Description**

Implement the PUDDING recipe scoring engine. For each active recipe (Efficiency→Friction, Drift→DeathSpiral, Safety→Honesty), compute novelty, plausibility, and actionability scores based on current metric data.

**Technical Specification**

> Combined = (Novelty + Plausibility + Actionability) / 3
>
> Novelty: based on label distance between source and target domains
>
> Plausibility: based on statistical correlation between source and target metrics
>
> Actionability: based on whether both source and target metrics have sufficient data

**Acceptance Criteria**

> 1\. 3 recipes scored weekly
>
> 2\. Scores stored in kaizen.tier4\_cross\_department
>
> 3\. Recipe scores trend over time (improving as more data accumulates)
>
> 4\. New recipe discovery: flag when a new SHARES\_LABEL edge has score \> 7.0

**COV-312: Build KaizenMonthlyReview Temporal Workflow**

**Priority: Medium**

**Type:** Feature

**Dependencies:** COV-305, COV-306, COV-311

**Estimated LOC:** \~250

**Estimated Build Time:** 3--4 hours

**File Targets:** new file temporal/workflows/kaizen\_monthly.py

**Description**

The comprehensive monthly Kaizen review. Runs 1st of each month at 06:00 UTC. Runs Tier 4 analysis, scores all PUDDING recipes, runs Inspect AI quarterly (if scheduled), and generates the Monthly Kaizen Report.

**Acceptance Criteria**

> 1\. Temporal schedule: 1st of month, 06:00 UTC
>
> 2\. Includes all 4 tiers of evaluation data
>
> 3\. PUDDING recipe scores for all active recipes
>
> 4\. Monthly report generated as structured JSON in ClickHouse
>
> 5\. Report includes: system health, improvement velocity, cost efficiency, recipe scores, prioritised backlog

**COV-313: Build PUDDING Recipe Discovery Engine**

**Priority: Low**

**Type:** Feature

**Dependencies:** COV-310, COV-311

**Estimated LOC:** \~200

**Estimated Build Time:** 3--4 hours

**File Targets:** new file evaluation/pudding/discovery.py

**Description**

The automated discovery engine. When new evaluation concepts are added to the PUDDING label store, automatically compute all possible recipe combinations, score them, and surface any scoring above the 7.0 threshold. This is the \'slime mould logic\' --- exploring all paths and reinforcing those that find value.

**Acceptance Criteria**

> 1\. New concepts automatically trigger recipe discovery
>
> 2\. All possible A→B→C combinations evaluated (with pruning for \< 2 shared labels)
>
> 3\. Recipes scoring ≥ 7.0 surfaced to Telegram + Linear
>
> 4\. At least 1 new cross-department pattern identified per quarter
>
> 5\. Discovery engine runs in \< 10 minutes for up to 50 concepts

**7. Task Dependency DAG**

The following directed acyclic graph shows all task dependencies across the 24 Linear issues. Tasks with no incoming edges can begin immediately. Critical path is highlighted through COV-290 → COV-291 → COV-292 → COV-295 → COV-305 → COV-306 → COV-312.

**Phase 1 Dependencies**

COV-290 ──┬── COV-291 ──── COV-292 ──┬── COV-295

│ │

└── COV-293 │

│

COV-294 ──────────────────────────────┘

**Phase 2 Dependencies**

COV-296 ──┬── COV-297 ──┬── COV-300

│ │

└── COV-298 ──┴── COV-299

**Phase 3 Dependencies**

COV-294 ──── COV-301 ──── COV-302 ──── COV-303 ──── COV-304

**Phase 4 Dependencies**

COV-292 ─┐

COV-294 ─┼── COV-295 ──── COV-305 ──┬── COV-306 ──── COV-312

│ │

COV-304 ─┘ COV-309 ───┘

COV-294 ──── COV-308

COV-292 ──── COV-307 (requires 4 weeks of data)

**Phase 5 Dependencies**

COV-310 ──── COV-311 ──┬── COV-312

└── COV-313

COV-306 ──── COV-311

COV-305 ──── COV-312

**Critical Path**

COV-290 → COV-291 → COV-292 → COV-295 → COV-305 → COV-306 → COV-312

Estimated critical path duration: \~22--30 hours of Cove build time across 10 weeks.

**Parallel Execution Opportunities**

The following issue groups have no interdependencies and can execute simultaneously across Cove\'s 5 parallel workers:

  ---------------- ------------------------------------------------
  **Group**        **Issues**
  Phase 1 Start    COV-290, COV-294 (no dependencies)
  Phase 1 Config   COV-291, COV-293 (both depend only on COV-290)
  Phase 2 Start    COV-296 (independent of Phase 1)
  Phase 2 Config   COV-297, COV-298 (both depend only on COV-296)
  Phase 5 Start    COV-310 (independent, can start in Week 5)
  ---------------- ------------------------------------------------

**8. Worker Registration Updates**

All new workflows and activities must be registered in workers/main.py for the Temporal workers to discover and execute them. The following lists the complete set of registrations required.

**New Temporal Workflows**

  ------------------------------- ------------------------ ------------------
  **Workflow Name**               **Schedule**             **Source Issue**
  KaizenDailyEvaluation           Daily 02:00 UTC          COV-305
  KaizenWeeklyAnalysis            Sunday 06:00 UTC         COV-306
  KaizenMonthlyReview             1st of month 06:00 UTC   COV-312
  ModelDeprioritizationWorkflow   Event-triggered          COV-299
  DriftAnalysisWorkflow           Sunday 04:00 UTC         COV-304
  QuarterlySafetyEvaluation       Quarterly 03:00 UTC      COV-300
  ------------------------------- ------------------------ ------------------

**New Temporal Activities**

  ---------------------------- ------------------ ------------------
  **Activity Name**            **Category**       **Source Issue**
  collect\_tier1\_metrics      Data Collection    COV-305
  run\_tier2\_evaluations      Evaluation         COV-305
  compare\_baselines           Analysis           COV-305
  flag\_anomalies              Detection          COV-305
  generate\_daily\_digest      Reporting          COV-305
  run\_tier3\_evaluations      Deep Evaluation    COV-306
  collect\_drift\_results      Data Collection    COV-306
  run\_pudding\_analysis       Cross-Department   COV-306
  generate\_hypotheses         AI Generation      COV-306
  generate\_weekly\_report     Reporting          COV-306
  compute\_centroids           Drift Detection    COV-301
  compute\_drift               Drift Detection    COV-302
  compute\_drift\_derivative   Drift Detection    COV-303
  run\_inspect\_evals          Safety             COV-297
  deprioritize\_model          Safety Response    COV-299
  ---------------------------- ------------------ ------------------

**Registration Code Pattern**

Add the following to workers/main.py in the worker registration block:

\# Kaizen Evaluation Workflows

from temporal.workflows.kaizen\_daily import KaizenDailyEvaluation

from temporal.workflows.kaizen\_weekly import KaizenWeeklyAnalysis

from temporal.workflows.kaizen\_monthly import KaizenMonthlyReview

from temporal.workflows.model\_deprioritization import ModelDeprioritizationWorkflow

from temporal.workflows.drift\_analysis import DriftAnalysisWorkflow

\# Kaizen Evaluation Activities

from temporal.activities.kaizen import (

collect\_tier1\_metrics, run\_tier2\_evaluations, compare\_baselines,

flag\_anomalies, generate\_daily\_digest, run\_tier3\_evaluations,

collect\_drift\_results, run\_pudding\_analysis, generate\_hypotheses,

generate\_weekly\_report,

)

from temporal.activities.drift import (

compute\_centroids, compute\_drift, compute\_drift\_derivative,

)

from temporal.activities.safety import (

run\_inspect\_evals, deprioritize\_model,

)

**9. knowledge\_base.md Updates**

The following section must be appended to knowledge\_base.md (Layer 1 prompt) so that all Cove agents are aware of the Kaizen evaluation system. This ensures agents can optimise their behaviour knowing they are being evaluated.

**Addition to knowledge\_base.md**

\#\# Kaizen Evaluation System

The Kaizen department continuously evaluates agent performance across

all departments using a 4-tier evaluation framework:

\#\#\# Tier 1: Automated Metrics (every execution)

\- Token usage, latency, cost, tool call counts

\- Collected automatically via Langfuse tracing

\#\#\# Tier 2: Sampled Evaluations (10% of executions)

\- DeepEval StepEfficiency and ToolCorrectness metrics

\- Your traces are evaluated --- aim for:

\- Step efficiency \> 0.7

\- Tool correctness \> 0.9

\- Evaluations run asynchronously (no performance impact on you)

\#\#\# Tier 3: Deep Evaluations (anomaly-triggered or scheduled)

\- Full DeepEval suite on flagged traces

\- Inspect AI safety evaluations quarterly

\- Triggered when Tier 2 metrics deviate \> 2σ from 7-day baseline

\#\#\# Tier 4: Cross-Department Analysis (weekly/monthly)

\- PUDDING cross-reference engine detects patterns across departments

\- Embedding drift monitoring on all knowledge graph vectors

\- Leading indicator models predict customer friction from efficiency drops

\#\#\# Key Points for Agents

\- All evaluation data flows to ClickHouse kaizen schema

\- Anomalies trigger automatic investigation --- no manual intervention needed

\- Safety evaluation failures may result in model deprioritization

\- Cross-department PUDDING analysis runs weekly for pattern detection

**10. Risk Register**

The following risk register identifies potential failure modes and their mitigations. All risks have been assessed against the specific Amplified Partners infrastructure context.

  ----------------------------------------------- ------------ ----------------- -----------------------------------------------------------------------------------------------
  **Risk**                                        **Impact**   **Probability**   **Mitigation**
  DeepEval eval latency impacts agent execution   High         Low               Async evaluation --- never blocks agent. Tier 2 sampling runs in a separate thread/coroutine.
  LLM judge costs exceed budget                   Medium       Medium            Use local/llama3.1-8b for Tier 2 (zero external API cost). Budget cap enforced via LiteLLM.
  Insufficient data for Recipe 1 correlation      Medium       Medium            Require 4 weeks minimum data. Flag model as \'insufficient signal\' if R² \< 0.3.
  FalkorDB PUDDING queries slow                   Low          Low               Graph is small (\< 100 nodes). Index on label components. Sub-100ms target easily met.
  Inspect AI evals not representative             Medium       Low               Custom tasks supplement standard benchmarks. 80+ test cases across 4 Layer 0 Laws.
  ClickHouse storage growth                       Low          Low               2-year TTL on Tier 1 data. MergeTree compression. Beast has 256 GB RAM for buffer.
  Model deprioritization false positive           High         Low               Require 2 consecutive failures before deprioritization. Manual override via Linear issue.
  Temporal workflow timeout                       Medium       Low               Set generous timeouts (30 min daily, 60 min weekly). Retry policy with backoff.
  Cross-department data schema drift              Medium       Medium            Materialised views abstract raw schemas. Views auto-refresh every 5 minutes.
  Drift detection too sensitive                   Low          Medium            KS test p-value \< 0.05 is standard. Require 3 consecutive weeks for acceleration alert.
  ----------------------------------------------- ------------ ----------------- -----------------------------------------------------------------------------------------------

**Attribution**

**Ewan Bramley** (originator, mission architect) × **Perplexity** (researcher, formaliser, build planner)

  ---------------- --------------------------
  **Fact %**       90
  **Confidence**   High
  **PUDDING**      P.+.5.l
  **LBD**          Swanson (1986) ABC Model
  ---------------- --------------------------

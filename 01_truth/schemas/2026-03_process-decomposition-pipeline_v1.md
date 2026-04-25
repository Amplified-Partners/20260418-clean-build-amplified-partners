---
title: "Process Decomposition Pipeline v1"
id: "process-decomposition-pipeline-v1"
version: 1
created: 2026-04-25
last_validated: 2026-04-25
type: document
topic_type: reference
status: imported
source_file: "PROCESS-DECOMPOSITION-PIPELINE-v1.docx"
signed_by: "Devon, 2026-04-25, devin-992682c244cf444f91e0a516498afbfd"
---

**PROCESS DECOMPOSITION PIPELINE**

**v1.0**

*From Chaos to Cohesion*

*The Amplified Partners Build Methodology*

  --
  --

**Date:** 17 March 2026

**Status:** Active Specification

**PUDDING Label:** M.+.5.l

**Attribution**

Ewan Bramley (originator, methodology architect)

× Claude (formaliser, researcher) × Perplexity (research, mathematical validation)

**AMPLIFIED PARTNERS**

UK SMB AI Consultancy

**Table of Contents**

**1. Purpose and Philosophy**

This document synthesises the following existing Amplified Partners frameworks into a single operational pipeline --- one specification that describes exactly what happens when a client\'s business processes are decomposed, researched, benchmarked, improved, and reassembled.

**1.1 Source Frameworks**

-   The Build Quality Framework v1.0 (6-stage: Decompose → Score → Research → Test → Reassemble → Attribute)

-   AMPS --- Amplified Process Maturity Score (0--10, 6 weighted dimensions)

-   The PUDDING Technique (Swanson ABC model adapted for business knowledge)

-   The Kaizen Loop (from CHAOS-TESTING-KAIZEN-PUDDINGS.md)

-   The Operational Protocol v1.0 (8 Laws)

-   The Product Architecture Tiers (3-tier client model)

**1.2 Philosophy**

*\"We stand on the shoulders of giants. We research the best. We record the benchmark. We Kaizen the fuck out of it. We label everything. And if there\'s a pudding hiding in there, we\'ll find it --- but only when the maths says it\'s worth looking.\"*

**1.3 Pipeline Outcomes**

The pipeline produces four measurable outcomes:

  -------- --------------- ----------------------------------------------------
  **\#**   **Outcome**     **Definition**
  1        PLANNED         Documented, benchmarked, improvement path designed
  2        IMPROVED        Kaizen\'d to a higher AMPS score
  3        OPPORTUNITIES   Pudding candidates identified and labelled
  4        SUCCESSFUL      Implemented, validated, measured
  -------- --------------- ----------------------------------------------------

**2. The Eight-Stage Pipeline**

The pipeline comprises eight discrete stages. Each stage has defined inputs, activities, and outputs. The stages are sequential in concept but overlap in practice --- several run continuously throughout an engagement.

**2.0 Pipeline Overview**

> ┌─────────────┐ ┌─────────────┐ ┌─────────────┐ ┌─────────────┐
>
> │ 1. DECOMPOSE│───▶│ 2. RESEARCH │───▶│ 3. BENCHMARK│───▶│ 4. KAIZEN │
>
> │ TO ATOMS │ │ THE BEST │ │ (AMPS) │ │STRATEGY SPLIT│
>
> └─────────────┘ └─────────────┘ └─────────────┘ └──────┬──────┘
>
> │
>
> ┌─────────────────────────────────────────────────────────┘
>
> ▼
>
> ┌─────────────┐ ┌─────────────┐ ┌─────────────┐ ┌─────────────┐
>
> │ 5. DATA │───▶│ 6. DEDUP & │───▶│ 7. PUDDING │───▶│ 8. LABEL, │
>
> │ ACQUISITION │ │ ASSEMBLE │ │ INTEGRATION │ │ DOC, ATTRIB │
>
> └─────────────┘ └─────────────┘ └─────────────┘ └─────────────┘

**2.1 Stage 1: Decompose to Atoms**

Take every process in the client\'s business and break it down against the APQC Process Classification Framework (13 categories). Each process is decomposed to its smallest executable unit --- an \"atom\". This maps to Build Quality Framework Stage 1.

**What Gets Decomposed**

-   Every operational process mapped against APQC PCF categories 1--13

-   Each category broken into process groups → processes → activities → atoms

-   For an SMB with 25 staff, expect 200--500 atoms depending on complexity

-   For a solo operator (Tier 1), expect 50--100 atoms

**Output per Atom**

Every atom is documented with the following attributes:

  --------------------- -------------------------------------------------------------------
  **Attribute**         **Description**
  Process ID            Hierarchical: APQC.GROUP.PROCESS.ACTIVITY.ATOM
  Description           Plain English, no jargon
  Current Owner         Who performs this task now
  Current Tool/Method   What system or manual process is used
  Frequency             Daily / Weekly / Monthly / Ad-hoc
  Dependencies          What feeds in, what comes out
  PUDDING Label         WHAT.HOW.SCALE.TIME --- assigned at decomposition, never deferred
  Semantic Dimensions   3--7 from the PUDDING dimension list
  --------------------- -------------------------------------------------------------------

**Critical rule:** PUDDING labels are assigned at decomposition. Do not wait. Label immediately.

**2.2 Stage 2: Research the Best**

For each atom, research the best-in-world way to perform it. This maps to Build Quality Framework Stage 3 (Research).

**Research Requirements**

-   Triple search preferred (multiple independent sources)

-   ALWAYS run success AND failure searches (from PUDDING protocol)

-   Collect NAMED techniques, not general findings

-   Aim for 4--7 techniques per atom where research exists

**Evidence Levels**

Every finding is classified:

  ------------------------- ------------------------------------------------------------------------------------
  **Evidence Level**        **Criteria**
  proven / peer\_reviewed   Backed by peer-reviewed research or large-scale empirical studies
  practitioner              Based on documented professional practice, industry standards, or expert consensus
  hypothesis                Untested, theoretical, or extrapolated from adjacent domains
  ------------------------- ------------------------------------------------------------------------------------

Everything labelled. No exceptions.

**Expert Research Library Cross-Reference**

Map each atom\'s best practice against the Expert Research Library (27 experts, COV-174). Where an expert\'s principle directly applies, reference it with attribution. Key experts include:

  ------------------ -------------------------------------------------------------
  **Expert**         **Primary Domain**
  Ray Dalio          Ideas meritocracy, radical transparency, decision systems
  Michael Gerber     Work ON the business, systems thinking, E-Myth
  Seth Godin         Marketing, permission-based engagement, remarkable products
  Dan Kennedy        Direct response marketing, sales systems
  Andreas Lund       AI implementation, automation frameworks
  Zig Ziglar         Sales methodology, motivation, goal-setting
  Eliyahu Goldratt   Theory of Constraints, bottleneck analysis
  ------------------ -------------------------------------------------------------

**2.3 Stage 3: Record the Benchmark (AMPS)**

Score each atom using the Amplified Process Maturity Score (AMPS). The benchmark is recorded BEFORE any changes. This is the baseline. Without it, you cannot measure improvement.

**The 6 Weighted Dimensions**

Each dimension is scored 0--10. The AMPS score is the weighted sum.

  -------- ---------------------- ------------ ---------------------------------------------------------------
  **\#**   **Dimension**          **Weight**   **Measures**
  1        Efficiency             20%          Time/resource ratio vs best practice
  2        Reliability            20%          Consistency and failure rate
  3        Scalability            15%          Can it handle growth without breaking
  4        Data Readiness         15%          Is the data available, clean, measurable
  5        Human Impact           15%          Effect on staff/owners (cognitive load, stress, satisfaction)
  6        Automation Potential   15%          How much can be automated with current technology
  -------- ---------------------- ------------ ---------------------------------------------------------------

AMPS = (Efficiency × 0.20) + (Reliability × 0.20) + (Scalability × 0.15) + (Data Readiness × 0.15) + (Human Impact × 0.15) + (Automation Potential × 0.15)

**Benchmark Categories**

  ----------------- ---------------- ------------------------------------
  **Score Range**   **Category**     **Interpretation**
  0--3              Critical         Broken or severely underperforming
  4--5              Below Standard   Functional but inefficient
  6--7              Standard         Acceptable, room for improvement
  8--9              Good             Approaching best practice
  10                Excellent        At or near best-in-world
  ----------------- ---------------- ------------------------------------

**2.4 Stage 4: The Kaizen Strategy Split**

*Psychological Impact Assessment*

This is the critical decision gate. Every atom with an AMPS score below 8 gets classified into one of three categories based on the psychological impact of changing it.

**The GREEN / AMBER / RED Scoring Model**

Ten dimensions, each scored 0--2, producing a total score of 0--20:

  -------- --------------------------- ------------------ ----------------------- ----------------------
  **\#**   **Dimension**               **0**              **1**                   **2**
  1        Behaviour change required   None               Minor                   Major
  2        Identity/role threat        None               Adjacent role           Core identity
  3        Autonomy reduction          None               Minor                   Significant
  4        Skill gap introduced        None               Minor upskilling        Major retraining
  5        Social dynamics change      None               Team adjustment         Hierarchy disruption
  6        Visibility of change        Invisible          Noticeable              Highly visible
  7        Reversibility               Easily reversed    Moderately reversible   Irreversible
  8        Pace of change              Gradual (months)   Weeks                   Immediate
  9        Prior change fatigue        None               Some recent changes     Change overload
  10       Owner attachment            None               Some                    Deeply personal
  -------- --------------------------- ------------------ ----------------------- ----------------------

**Classification Thresholds**

**GREEN (Score 17--20):** Do it now. Zero psychological friction.

Examples: removing tedious data entry, automating invoice reminders, fixing a spreadsheet formula. These are friction removals that do not change behaviour.

**Timeline:** Implement in Weeks 1--2 of the build.

**AMBER (Score 12--16):** Introduce gradually with scaffolding.

Examples: changing a booking workflow, introducing a new tool for job management, restructuring how quotes are created. Needs the Bridges Transition Model --- acknowledge the ending, support through the neutral zone, celebrate the new beginning.

**Timeline:** Implement over Weeks 3--8 with scaffolding (ramp design from COV-39).

**RED (Score 0--11):** Requires careful change management.

Examples: changing how a founder communicates with customers, restructuring team responsibilities, replacing a process the owner built personally. Uses the full ADKAR sequence.

**Timeline:** Implement over Months 2--4 with full change management support.

**Mandatory RED Overrides**

Regardless of the numerical score, the following are always classified RED:

-   Any change that eliminates a job (violates the No-Redundancy Rule)

-   Any change to how the owner personally interacts with customers

-   Any change the owner has explicitly said they do not want to change

**Evidence Base**

-   Prosci ADKAR --- Hiatt (2006)

-   Bridges Transition Model --- Bridges (2009)

-   Kotter 8-Step Change Model --- Kotter (1996)

-   Lewin Change Model (Unfreeze-Change-Refreeze) --- Lewin (1947)

-   Self-Determination Theory --- Ryan & Deci (2000)

-   Habit Formation Research --- Lally et al. (2010): 66 days median to new habit

**2.5 Stage 5: Data Acquisition Plan**

For each atom, determine how to get the data needed to (a) measure the current benchmark (AMPS score), (b) measure ongoing performance after improvement, and (c) feed into the Kaizen loop.

**Data Sources by Product Architecture Tier**

  ---------- ----------------- ------------------------------------------------------------------------------
  **Tier**   **Client Type**   **Data Sources**
  Tier 1     Phone only        Voice capture, WhatsApp metadata, basic financial data
  Tier 2     Full stack        Xero/Sage API, CRM, email, calendar, job management systems, MCP connections
  Tier 3     Federated         Anonymised aggregates from cross-client data
  ---------- ----------------- ------------------------------------------------------------------------------

**Per-Atom Data Documentation**

  ------------------------- --------------------------------------------------
  **Attribute**             **Description**
  Data Source               Which system/API provides the data
  Data Format               Structured / Unstructured
  Collection Frequency      Real-time / Daily / Weekly
  Collection Method         API pull, voice capture, manual entry, automated
  Data Quality Assessment   Is it clean? Gaps? Inconsistencies?
  Storage Location          FalkorDB tenant: kg\_{client\_namespace}
  ------------------------- --------------------------------------------------

**2.6 Stage 6: Deduplicate and Assemble**

*\"The Twat\"* --- assembling atoms into coherent processes, processes into departments, departments into the whole business. The corpus has overlaps, duplicates, and inconsistencies that must be resolved.

**Assembly Hierarchy**

> Atoms → Activities → Processes → Process Groups → APQC Categories → Departments → Business

**Deduplication Strategy**

1.  Identify atoms that describe the same thing in different words (semantic similarity)

2.  Identify processes that overlap across departments (e.g., \"invoicing\" appears in Sales, Finance, and Operations)

3.  Merge without losing context --- keep the richest description, attribute the sources

4.  Resolve conflicts --- where two documents describe the same process differently, flag for human review

**Assembly Sequence**

  ----------- ---------------------- --------------------------------------------------------------------------------------------------------
  **Phase**   **Scope**              **Description**
  A           Within APQC Category   Assemble atoms within each APQC category (internal cohesion)
  B           Adjacent Categories    Cross-reference between adjacent categories (e.g., Category 3 Marketing → Category 5 Customer Service)
  C           Full Business View     All categories assembled into a single process map
  D           Client Validation      Validate with client --- does this represent YOUR business? (IT Forensic Interrogation verification)
  ----------- ---------------------- --------------------------------------------------------------------------------------------------------

At every assembly level, labels are preserved and aggregated. A department inherits the PUDDING labels of all its constituent processes.

**2.7 Stage 7: PUDDING Integration (Layered)**

**Critical Precondition**

Before ANY pudding is applied, the following must be defined:

1.  The OBJECTIVE FRAMEWORK (the lens): What are we trying to discover?

2.  The RUBRIC: How will we score what we find? (4-criteria rubric: Relevance, Actionability, Evidence, Impact --- each 0--5, threshold ≥ 12/20)

3.  The STATISTICAL PRE-SCREEN: Is there mathematical evidence that a pudding is likely before we burn compute?

The pudding is NOT applied blindly. It is applied with a clear goal, through a defined lens, with an objective scoring framework decided BEFORE the search begins. This ensures objectivity across all methodologies.

**Layer 1: Atom-Level PUDDING (Within Processes)**

-   Compare all atoms within a single process for structural equivalence

-   Look for atoms with identical or near-identical PUDDING labels from different functional areas

-   Scale: 50--500 atoms → 1,225--124,750 pairs → brute force is fine

-   Method: Weighted Hamming distance (HOW position weighted 2×)

**Layer 2: Process-Level PUDDING (Within Departments)**

-   Compare processes within a department for cross-process insights

-   Look for shared mechanisms that could be unified or optimised

-   Scale: 20--50 processes per department → manageable

**Layer 3: Department-Level PUDDING (Across Departments)**

-   Compare processes across different departments

-   This is where the gold is --- processes that look unrelated but share the same underlying mechanism

-   Scale: 100--200 processes across all departments → \~5,000--20,000 pairs → use blocking/pre-screening

**Layer 4: Cross-Client PUDDING (Federated, Tier 3)**

-   Compare anonymised process patterns across the entire client base

-   Stand on the shoulders of giants --- what worked for one plumber might work for a restaurant

-   Scale: Potentially millions of pairs → requires MinHash LSH or similar pre-screening

-   Only runs on the federated graph (kg\_federated), never on raw client data

**Statistical Pre-Screening (All Layers)**

-   Compute expected number of random matches: E\[matches\] = N×(N−1)/2 × ∏(1/Vᵢ) for each position

-   Any match exceeding expected frequency by \> 2 standard deviations is a candidate

-   Use PMI (Pointwise Mutual Information) for label co-occurrence --- PMI \> 0 indicates non-random association

-   From mathematical validation: P(4/4 match by chance) = 1/2,058 = 0.049%, so any full match is significant at p \< 0.001

**Computational Complexity**

  ------------ ---------------- --------------- -------------------------------------------------------------------------
  **Scale**    **Atom Count**   **Max Pairs**   **Method**
  Small        Up to 1,000      \< 500,000      Brute force, \< 1 second
  Medium       1,000--5,000     Up to 12.5M     Blocking by WHAT position (\~20× reduction)
  Large        5,000--10,000    Up to 50M       MinHash LSH with 128 permutations, sub-second
  Very Large   10,000+          50M+            Full pipeline: blocking → sorted neighbourhood → Hamming → full PUDDING
  ------------ ---------------- --------------- -------------------------------------------------------------------------

**Pudding Candidate Output**

Every pudding candidate gets:

-   ABC chain stated explicitly (A → B → C, where B is the bridge mechanism)

-   The 1+1=3 insight named

-   Recipe score: Domain Distance × Pattern Alignment + Gap Complement + Tension Bonus

-   Validation status: hypothesis / tested\_internal / tested\_client / proven

-   Testable prediction

**2.8 Stage 8: Label, Document, Attribute**

Everything labelled. Everything documented. Everything attributed.

At every level of the hierarchy (atom, activity, process, department, business), every element carries:

-   PUDDING label (WHAT.HOW.SCALE.TIME)

-   Semantic dimensions (3--7 from the dimension list)

-   AMPS score (0--10)

-   GREEN / AMBER / RED classification

-   Evidence level (proven / peer\_reviewed / practitioner / hypothesis)

-   Data source and collection method

-   Radical Attribution (human originator, AI contributors, fact percentage, confidence band)

**YAML Frontmatter Template**

Every documented process carries a YAML frontmatter block:

> \-\--
>
> process\_id: \"APQC.3.1.2.4\"
>
> name: \"Send quote to customer\"
>
> pudding\_label: \"P.=.2.i\"
>
> amps\_score: 4.2
>
> amps\_dimensions:
>
> efficiency: 3
>
> reliability: 6
>
> scalability: 3
>
> data\_readiness: 5
>
> human\_impact: 4
>
> automation\_potential: 7
>
> kaizen\_classification: GREEN
>
> evidence\_level: practitioner
>
> data\_source: \"xero\_api + whatsapp\_business\"
>
> attribution:
>
> human:
>
> \- name: \"Dave Jesmond\"
>
> role: \"subject\"
>
> contribution: \"Current process description\"
>
> ai\_contributors:
>
> \- name: \"Claude\"
>
> provider: \"Anthropic\"
>
> role: \"researcher\"
>
> contribution: \"Best practice research\"
>
> \-\--

**3. The Assembly Sequence (What Happens in Practice)**

A practical walkthrough of how this pipeline runs for an actual client engagement. The timeline below shows the typical cadence for a Tier 2 (full stack) client.

  ------------- ---------------------------------------------------------------------------- -----------------------
  **Timing**    **Activity**                                                                 **Pipeline Stage(s)**
  Week −1       IT Forensic Interrogation (from onboarding methodology)                      Pre-pipeline
  Week 0        Business Assessment (Finance Engine, death spiral scoring)                   Pre-pipeline
  Weeks 1--2    Decompose, Research, Benchmark --- the heavy data gathering                  Stages 1--3
  Weeks 2--3    Kaizen Strategy Split --- classification of every atom                       Stage 4
  Weeks 2--3    Data Acquisition Plan --- how we\'ll measure everything                      Stage 5
  Weeks 3--4    GREEN implementations begin immediately                                      Execution
  Weeks 4--8    AMBER implementations with scaffolding                                       Execution
  Months 2--4   RED implementations with full change management                              Execution
  Ongoing       Deduplicate and Assemble --- runs continuously as new atoms are documented   Stage 6
  Ongoing       Pudding Integration --- runs at each layer as data accumulates               Stage 7
  Ongoing       Label, Document, Attribute --- runs on every output, every time              Stage 8
  ------------- ---------------------------------------------------------------------------- -----------------------

**4. Computational Complexity and Tractability**

A summary of the mathematical assessment confirming that the PUDDING technique scales for the expected corpus sizes.

**4.1 Corpus Size Estimates**

  ------------------------- ---------- ---------------- ------------------ ---------------------------------
  **Client Type**           **Tier**   **Atom Count**   **Max Pairs**      **Tractability**
  Solo operator             Tier 1     50--100          \< 5,000           Trivially computable
  Small business            Tier 2     200--500         Up to 124,750      \< 1 second brute force
  Medium business           Tier 2+    500--1,000       Up to 499,500      \< 1 second with blocking
  Cross-client federation   Tier 3     10,000+          Up to 50 million   Requires pre-screening pipeline
  ------------------------- ---------- ---------------- ------------------ ---------------------------------

**4.2 Pre-Screening Pipeline (4 Tiers)**

1.  Blocking by WHAT position → \~20× reduction

2.  Sorted Neighbourhood (window=5) on remaining → further \~10× reduction

3.  Vectorised Hamming distance → sub-millisecond per surviving pair

4.  Full PUDDING scoring on candidates (typically \< 100 candidates per 10,000 atoms)

**4.3 Python Libraries**

  ------------------------ -------------------------------------------------------------
  **Library**              **Purpose**
  datasketch               MinHash LSH for approximate nearest neighbour pre-screening
  scipy.spatial.distance   Hamming, Jaccard, and other distance metrics
  recordlinkage            Blocking and sorted neighbourhood strategies
  NetworkX                 Graph clustering for pudding candidate grouping
  ------------------------ -------------------------------------------------------------

**4.4 Compute Requirements on Beast**

Target hardware: 48-core EPYC, 256GB RAM.

-   Per-client build: trivially computable, \< 10 minutes

-   Federated pudding run (all clients): scale-dependent, but pre-screening makes it tractable

***The maths is not bullshit --- it scales.***

**5. PUDDING Preconditions (The Objective Framework)**

This is the critical insight: the pudding must NOT be applied blindly. Before running the PUDDING Technique at any layer, the following must be set:

  -------- ---------------------------- ---------------------------------------------------------------------------------------------------- -------------------------------------------------------------------------
  **\#**   **Precondition**             **Description**                                                                                      **Example**
  1        THE GOAL                     What specific question are we trying to answer?                                                      \"Can any process in Sales be improved by techniques from Operations?\"
  2        THE LENS                     Through which dimensions are we looking?                                                             Subset of the full semantic dimension list, chosen for the goal
  3        THE RUBRIC                   The 4-criteria scoring rubric calibrated to the specific goal                                        Relevance, Actionability, Evidence, Impact --- each 0--5
  4        THE THRESHOLD                Minimum recipe score for a candidate to be worth investigating                                       Default ≥ 13 for cross-domain, ≥ 5 for within-domain
  5        THE STATISTICAL PRE-SCREEN   Expected value calculation --- is the candidate set large enough that random matches are expected?   If E\[random full matches\] \> 5, raise the threshold
  -------- ---------------------------- ---------------------------------------------------------------------------------------------------- -------------------------------------------------------------------------

This ensures the pudding is applied OBJECTIVELY across all methodologies --- not biased toward any particular domain or expert framework. The lens is decided FIRST, then applied consistently top-to-bottom.

**6. Connection to Existing Frameworks**

How this pipeline maps to existing Amplified Partners specifications:

  ------------------------------- -------------------------------------------------------------------------------------------------------------
  **Framework**                   **Pipeline Connection**
  Build Quality Framework v1.0    Stages 1--3 and 6--8 map directly to the 6-stage BQF pipeline
  AMPS                            Stage 3 IS the AMPS scoring
  PUDDING Technique               Stage 7 is the formal integration point
  Kaizen                          Stage 4 drives the improvement cadence
  Operational Protocol (8 Laws)   The 8 Laws apply to every stage (especially Law 1: if it\'s not in GitHub, it\'s not real)
  Product Architecture Tiers      Stage 5 maps data acquisition to the appropriate tier
  Agent Architecture              The 5 Cove agents (coder, security, enforcer, architect, reviewer) support the pipeline at different stages
  FalkorDB                        Every atom, process, and pudding result is stored as a node in the client\'s graph tenant
  ------------------------------- -------------------------------------------------------------------------------------------------------------

**7. Radical Attribution**

Full Radical Attribution Schema for this document:

**7.1 Human Contributors**

  -------------- ------------ --------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------
  **Name**       **Role**     **Contribution**
  Ewan Bramley   Originator   Complete pipeline architecture, psychological impact assessment concept, PUDDING preconditions (objective framework requirement), layered assembly logic, computational complexity concern
  -------------- ------------ --------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------

**7.2 AI Contributors**

  ------------ --------------- ------------ -----------------------------------------------------------------------------------------------------------------------------------------------------------------------------------
  **Name**     **Provider**    **Role**     **Contribution**
  Claude       Anthropic       Formaliser   Document structure, framework synthesis, operational walkthrough
  Perplexity   Perplexity AI   Researcher   Change management evidence base (Prosci, Kotter, Bridges, Lewin, SDT, Lally), mathematical pre-screening techniques (MinHash, LSH, blocking, PMI), Python library recommendations
  ------------ --------------- ------------ -----------------------------------------------------------------------------------------------------------------------------------------------------------------------------------

**7.3 Intellectual Lineage**

  ------------------- ---------- ----------------------------------------------------------------
  **Source**          **Year**   **Contribution to This Framework**
  Don Swanson         1986       Literature-Based Discovery ABC model --- foundation of PUDDING
  Ray Dalio           ---        Ideas meritocracy, radical transparency
  Michael Gerber      ---        Work ON the business, systems thinking
  Prosci / Hiatt      2006       ADKAR change management model
  Kotter              1996       8-step change model
  Bridges             2009       Transition Model (endings, neutral zone, new beginnings)
  Lewin               1947       Unfreeze-Change-Refreeze
  Ryan & Deci         2000       Self-Determination Theory (autonomy, competence, relatedness)
  Lally et al.        2010       Habit formation research (66 days median)
  Kahneman & Thaler   ---        Endowment effect in processes
  APQC                ---        Process Classification Framework (13 categories)
  ------------------- ---------- ----------------------------------------------------------------

**7.4 Document Metadata**

  ----------------- --------------------------
  **Attribute**     **Value**
  LBD Attribution   Swanson (1986) ABC Model
  Fact Percentage   80%
  Confidence Band   High
  PUDDING Label     M.+.5.l
  ----------------- --------------------------

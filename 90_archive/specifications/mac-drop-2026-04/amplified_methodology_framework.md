**THE AMPLIFIED**

**METHODOLOGY FRAMEWORK**

A Unified Operating System for Taxonomy, Research,

Extraction, Testing, and Improvement

**Amplified Partners**

March 2026 --- Version 1.0

**CONFIDENTIAL --- INTERNAL USE ONLY**

**TABLE OF CONTENTS**

**1. Executive Summary**

**1.1 What This Document Is**

The Amplified Methodology Framework (AMF) is the single, authoritative
reference for how Amplified Partners discovers, classifies, extracts,
tests, scores, and ships knowledge. It unifies every methodology
developed across multiple workstreams --- AMPS, the Build Quality
Framework, the Rapid Intelligence Cycle (RIC), PUDDING, Gap Analysis &
Finite Lenses, the Master Process Document, the Operations Register, and
the Visual Polish System --- into one coherent operating manual.

Every piece of work at Amplified Partners --- whether code, content,
process design, research, or client deliverable --- flows through the
same pipeline. This document describes that pipeline, its quality gates,
its scoring rubrics, its testing regimes, and its improvement cadences.

**1.2 The Core Insight**

The methodology rests on a single principle: **every atom of knowledge
passes through the same pipeline regardless of type.** What changes is
the velocity and rigour applied at each stage --- not the stages
themselves. This is validated by research into Toyota Production System
standardised work principles, where process consistency is the
foundation of improvement ([APQC Process Classification
Framework](https://www.apqc.org/process-frameworks); [Lean Thinking
applied to LLM
Evals](https://www.productbreaks.com/p/lean-thinking-for-evals)).

**1.3 The Two Rhythms**

All work at Amplified Partners operates in one of two rhythms:

  ----------------------- ----------------------------------------- ------------------------------------------
  **Dimension**           **PUDDING (Rapid Discovery)**             **Kaizen (Compound Improvement)**
  Objective               Discover if 10/10 quality is achievable   Compound 1% improvements toward 10/10
  Decision speed          Hours                                     Days to weeks
  Change size             Large experiments                         Micro-improvements
  Test coverage           Partial (20% golden dataset)              Full (100% + production monitoring)
  Acceptable regression   Tolerates some for big gains              Zero regression tolerance
  Human involvement       High (daily eval review)                  Low (automated with exception routing)
  Statistical rigour      Low (directional signals)                 High (statistical significance required)
  ----------------------- ----------------------------------------- ------------------------------------------

PUDDING is the discovery engine --- named after the Literature-Based
Discovery lineage of Don Swanson --- that drives aggressive, tiered
testing over hours and days. Kaizen is the compound improvement engine
that takes stable systems and makes them measurably better over weeks
and months. The transition between them is governed by explicit signals
described in Section 10 ([Evaluation-Driven Development, arXiv
2025](https://arxiv.org/html/2411.13768v3)).

**1.4 The Four Departments**

The pipeline is operationally managed across four departments, each
owning specific phases:

  ---------------- ------------------------------- --------------------------------------------------
  **Department**   **Pipeline Phases Owned**       **Primary Responsibility**
  R&D              Discover → Classify → Extract   Finding and structuring new knowledge
  Chaos            Test (adversarial) → Score      Breaking things deliberately to prove resilience
  Kaizen           Research → Present → Improve    Compound improvement of stable systems
  Real             Ship → Operate → Monitor        Production deployment and reliability
  ---------------- ------------------------------- --------------------------------------------------

**2. The Unified Pipeline**

**2.1 Pipeline Overview**

Every piece of work at Amplified Partners moves through nine sequential
stages. This pipeline synthesises the AMPS 7-step methodology (Decompose
→ Score → Research → Design → Test → Validate → Reassemble), the Build
Quality Framework 6-stage pipeline, and the RIC 5-phase overnight cycle
into a single, unified flow.

**THE NINE-STAGE PIPELINE**

  -------------- ----------- ------------------------------------ ---------------------------------------- -----------------------------------------
  **Stage**      **Owner**   **Inputs**                           **Outputs**                              **Quality Gate**
  1\. DISCOVER   R&D         Raw sources, RIC scan, client data   Candidate atoms (unstructured)           Source credibility ≥ 3/5
  2\. CLASSIFY   R&D         Candidate atoms                      Classified atoms with 5-layer taxonomy   APQC mapping verified
  3\. EXTRACT    R&D         Classified sources                   Structured atoms (NER/RE complete)       Extraction F1 ≥ 0.80
  4\. SCORE      Chaos       Structured atoms                     Scored atoms (AMPS 0--10)                Minimum AMPS ≥ 5.0 to proceed
  5\. RESEARCH   Kaizen      Scored atoms with gaps               Enriched atoms, validated claims         Radical Attribution complete
  6\. TEST       Chaos       Enriched atoms                       Validated atoms, test results            PRS ≥ 7.0 to ship
  7\. PRESENT    Kaizen      Validated atoms                      Formatted deliverables                   Visual Polish Score ≥ 7.0
  8\. SHIP       Real        Approved deliverables                Production deployment                    Owner consent: Approve
  9\. KAIZEN     Kaizen      Production metrics                   Improvement actions                      IV \> 0 (positive improvement velocity)
  -------------- ----------- ------------------------------------ ---------------------------------------- -----------------------------------------

**2.2 How a Knowledge Atom Flows Through the Pipeline**

Consider a concrete example: a new research finding about UK SMB cash
flow management arrives via the RIC nightly scan.

1.  **DISCOVER:** The RIC Tier-2 source scan (financial press)
    identifies an article citing new HMRC guidance on Making Tax
    Digital. The article scores 4/5 on source credibility.

2.  **CLASSIFY:** The finding is assigned atom ID AMP-10029-001-v1 (APQC
    10029 = Tax Management). Five taxonomy layers are applied: WHAT (tax
    compliance), HOW (digital submission), SCALE (SMB), TIME (2026-Q2),
    CONTEXT (UK regulatory).

3.  **EXTRACT:** GLiNER2 zero-shot NER extracts entities: deadlines,
    penalty thresholds, exemption criteria. Relationships are mapped in
    FalkorDB.

4.  **SCORE:** AMPS scoring across 6 dimensions yields 6.8/10. This is
    above the 5.0 threshold for proceeding but below the 7.0 ship
    threshold --- it needs enrichment.

5.  **RESEARCH:** Kaizen team enriches with primary HMRC source data,
    cross-references with existing atoms on VAT and MTD. Radical
    Attribution traces every claim to source URL.

6.  **TEST:** Chaos department validates: factual accuracy against HMRC
    source, internal consistency, client applicability scoring. PRS
    rises to 7.4.

7.  **PRESENT:** Formatted for client delivery with Visual Polish System
    scoring. Composite score ≥ 7.0 achieved.

8.  **SHIP:** Owner (Ewan) reviews, approves. Atom enters production
    knowledge graph.

9.  **KAIZEN:** Monthly review checks whether the guidance remains
    current. HMRC updates trigger automatic flagging for re-validation.

**2.3 Stage-to-Framework Mapping**

Each unified pipeline stage maps back to the original frameworks it
synthesises:

  ------------------- ----------------- ------------------------- -------------------
  **Unified Stage**   **AMPS Step**     **Build Quality Stage**   **RIC Phase**
  Discover            ---               ---                       Phase 1: Scan
  Classify            Decompose         Decompose                 Phase 2: Evaluate
  Extract             Decompose         Decompose                 Phase 2: Evaluate
  Score               Score             Score 0--10               Phase 3: Score
  Research            Research          Research                  Phase 3: Score
  Test                Test + Validate   Test                      Phase 4: Test
  Present             ---               Attribute                 Phase 5: Present
  Ship                Reassemble        Reassemble                ---
  Kaizen              ---               ---                       Continuous
  ------------------- ----------------- ------------------------- -------------------

**3. Taxonomy --- The Classification Engine**

**3.1 The Five Taxonomy Layers**

Every knowledge atom at Amplified Partners carries five simultaneous
classification layers. This multi-layer approach is validated by
research into faceted classification systems, where [APQC\'s Process
Classification Framework](https://www.apqc.org/process-frameworks)
(version 7.4, 1,500+ processes across 13 categories) provides the
hierarchical backbone, and [SKOS (Simple Knowledge Organization
System)](https://www.w3.org/2004/02/skos/) provides the formalisation
path for machine-readable semantic relationships.

  -------------------- ----------------------------------------------- ----------------------- -----------------------------
  **Layer**            **Purpose**                                     **Source Standard**     **Example**
  1\. Hierarchical     Locates the atom in the business process tree   APQC PCF v7.4           10029 → Tax Management
  2\. Functional       Describes what the atom does                    Custom (PUDDING WHAT)   Compliance guidance
  3\. Methodological   Describes how it operates                       Custom (PUDDING HOW)    Digital submission workflow
  4\. Dimensional      Scale and time applicability                    Custom (SCALE.TIME)     SMB.2026-Q2
  5\. Contextual       Domain-specific qualifiers                      Recommended addition    UK-regulatory.HMRC
  -------------------- ----------------------------------------------- ----------------------- -----------------------------

**3.2 The APQC Backbone**

The APQC PCF is organised into five nested levels. Amplified Partners
uses Levels 1--3 as the primary classification backbone, with Levels
4--5 available for deep-dive processes. The framework\'s 13 top-level
categories cover the complete scope of business operations ([APQC PCF
documentation](https://www.apqc.org/process-frameworks)).

  ------------------------ ---------------------------------------------- -----------------------------
  **PCF Level**            **Example**                                    **Amplified Use**
  Level 1: Category        10.0 Manage Enterprise Risk                    Workstream assignment
  Level 2: Process Group   10.2 Manage Financial Risk                     Operations Register mapping
  Level 3: Process         10.2.3 Manage Tax Compliance                   Atom primary classification
  Level 4: Activity        10.2.3.1 Prepare Tax Returns                   Detailed atom tagging
  Level 5: Task            10.2.3.1.1 Gather financial data for returns   Sub-atom level (optional)
  ------------------------ ---------------------------------------------- -----------------------------

**3.3 Faceted Classification: WHAT.HOW.SCALE.TIME.CONTEXT**

The PUDDING 2026 labeling format uses a dot-notation faceted
classification system. Research into faceted classification confirms
this approach avoids the rigidity of pure hierarchy while maintaining
machine-readability. The recommended CONTEXT addition (fifth facet)
addresses the gap identified in cross-domain knowledge transfer.

**Format:** WHAT.HOW.SCALE.TIME.CONTEXT

**Example:** tax-compliance.digital-submission.smb.2026-q2.uk-hmrc

**3.4 Atom ID Format**

**Format:** AMP-{APQC\#}-{SEQ}-{VERSION}

**Example:** AMP-10029-001-v1

-   **AMP:** Namespace prefix (Amplified Partners)

-   **APQC\#:** APQC Process Classification number --- positions the
    atom in the global business process tree

-   **SEQ:** Sequential number within that APQC category ---
    distinguishes multiple atoms in the same domain

-   **VERSION:** Semantic version --- enables tracking of atom evolution
    through Kaizen cycles

**3.5 The 12 Analytical Lenses**

The Gap Analysis & Finite Lenses Framework defines 12 lenses through
which any atom can be examined. Each lens answers a different question
about the knowledge:

  -------- ----------------------- ----------------------------------------- -----------------------
  **\#**   **Lens**                **Question It Answers**                   **When Applied**
  1        Process Efficiency      How well does this process flow?          Every atom
  2        Compliance              Does this meet regulatory requirements?   Regulatory atoms
  3        Financial Impact        What is the cost/revenue effect?          Financial atoms
  4        Client Applicability    Which client segments benefit?            Client-facing atoms
  5        Technology Fit          Does existing tech support this?          Technical atoms
  6        Scalability             Does this work at 10× current scale?      Growth-path atoms
  7        Risk                    What can go wrong?                        Every atom
  8        Data Quality            Is the underlying data reliable?          Data-dependent atoms
  9        Automation Potential    Can this be automated?                    Process atoms
  10       Knowledge Gaps          What don\'t we know?                      Every atom
  11       Cross-Domain Transfer   Does this apply elsewhere?                PUDDING-flagged atoms
  12       Temporal Validity       When does this expire?                    Time-sensitive atoms
  -------- ----------------------- ----------------------------------------- -----------------------

**3.6 Biological Decision Logic Taxonomy**

The classification system draws on Linnaean biological taxonomy
principles. Just as biological taxonomy uses a hierarchical system
(Kingdom → Phylum → Class → Order → Family → Genus → Species) to
uniquely identify every organism, Amplified Partners uses APQC hierarchy
+ faceted classification to uniquely identify every knowledge atom. The
key principle borrowed from biology: **polyhierarchy** --- an atom can
exist in multiple classification branches simultaneously, just as
biological traits can be shared across taxonomic groups. This is
implemented through SKOS *skos:broader* and *skos:related* relationships
in FalkorDB ([W3C SKOS Reference](https://www.w3.org/2004/02/skos/)).

**3.7 Machine-Readability: JSON Schema for Atoms**

Every atom is stored with the following JSON structure, enabling RAG
retrieval, agent queries, and graph traversal:

{ \"id\": \"AMP-10029-001-v1\", \"apqc\": \"10029\", \"facets\": {
\"what\": \"tax-compliance\", \"how\": \"digital-submission\",
\"scale\": \"smb\", \"time\": \"2026-q2\", \"context\": \"uk-hmrc\" },
\"layers\": \[\...\], \"amps\_score\": 7.4, \"prs\": 7.4, \"sources\":
\[\...\], \"relationships\": \[\...\] }

**4. Labeling --- The Quality of Classification**

**4.1 PUDDING 2026 Labeling Format**

The PUDDING labeling system uses the four-criteria rubric derived from
Don Swanson\'s Literature-Based Discovery methodology. Every label is
evaluated against four dimensions, each scored on a defined scale. The
2026 format extends the original with the CONTEXT facet for cross-domain
applicability ([Swanson LBD
methodology](https://en.wikipedia.org/wiki/Don_R._Swanson)).

  ------------------ --------------------------------------------------------- --------------------------------- ------------------------
  **Criterion**      **Definition**                                            **Scoring**                       **Minimum Acceptable**
  Specificity        How precisely does the label describe the atom?           1--5 scale                        ≥ 3
  Consistency        Does the label follow established patterns?               Binary: Consistent/Inconsistent   Consistent
  Completeness       Are all required facets populated?                        \% of facets completed            ≥ 80%
  Discriminability   Does the label distinguish this atom from similar ones?   1--5 scale                        ≥ 3
  ------------------ --------------------------------------------------------- --------------------------------- ------------------------

**4.2 Inter-Annotator Agreement**

For labeling quality at scale, Amplified Partners targets
**Krippendorff\'s Alpha ≥ 0.7** across all classification dimensions.
This threshold, validated by [Krippendorff\'s reliability
research](https://en.wikipedia.org/wiki/Krippendorff%27s_alpha),
represents the minimum for \"tentative conclusions\" in content
analysis. For critical regulatory atoms, the target is α ≥ 0.8.

**4.3 Calibration Sessions**

Calibration sessions ensure labeling consistency across the team. The
90-minute structured format:

10. **Review (15 min):** Examine 10 recently labeled atoms, identifying
    disagreements

11. **Discuss (30 min):** Work through each disagreement, documenting
    the resolution rationale

12. **Align (20 min):** Update the labeling guide with new precedents or
    clarifications

13. **Practice (15 min):** Label 5 new atoms independently, then compare

14. **Measure (10 min):** Calculate session Krippendorff\'s Alpha, log
    trend

**4.4 Active Learning and Label Efficiency**

The labeling system incorporates active learning to become more
efficient over time. As the corpus grows, the system identifies atoms
where human labeling adds the most value --- typically edge cases near
classification boundaries. Straightforward atoms are auto-labeled with
confidence scores and routed to human review only when confidence falls
below 0.85.

**4.5 Label Quality Metrics**

  ----------------------- ------------------------------------ ------------------------- -------------------------------
  **Metric**              **Target**                           **Measurement Cadence**   **Action if Below Target**
  Krippendorff\'s Alpha   ≥ 0.7 (general) / ≥ 0.8 (critical)   Weekly                    Mandatory calibration session
  Auto-label accuracy     ≥ 95% (verified by sample)           Daily (automated)         Retrain classifier
  Facet completeness      ≥ 80% of atoms fully faceted         Weekly                    Backfill sprint
  Label turnaround time   \< 24 hours from atom creation       Daily                     Capacity review
  Reclassification rate   \< 5% per month                      Monthly                   Taxonomy review
  ----------------------- ------------------------------------ ------------------------- -------------------------------

**5. Extraction --- From Raw to Structured**

**5.1 The Extraction Pipeline**

Extraction transforms raw source material --- documents, web pages,
client data, research papers --- into structured knowledge atoms. The
pipeline operates in three phases:

15. **Ingestion:** Raw documents enter the pipeline via the Vault
    Research Ingestion Format (two-layer storage: YAML metadata in
    FalkorDB + raw content in filesystem, ID format RES-YYYY-MM-DD-NNN).

16. **Entity Recognition:** GLiNER2 performs zero-shot Named Entity
    Recognition, identifying entities without requiring fine-tuned
    models. This runs on The Beast\'s CPU, making it available 24/7
    without GPU costs.

17. **Relation Extraction:** Identified entities are connected through
    relation extraction, building the knowledge graph in FalkorDB.
    Relations include hierarchical (is-a), associative (related-to), and
    temporal (preceded-by) types.

**5.2 GLiNER2 for Zero-Shot Extraction**

GLiNER2 is the primary extraction engine, chosen for its zero-shot
capability --- it identifies entities using natural language
descriptions rather than requiring training data for each entity type.
This aligns with the PUDDING philosophy of rapid iteration: new entity
types can be defined immediately without a training cycle ([GLiNER
documentation](https://github.com/urchade/GLiNER)).

**5.3 Extraction Quality Metrics**

  ----------------------------- ------------ -------------------------------------------------
  **Metric**                    **Target**   **Measurement Method**
  Precision (per entity type)   ≥ 0.85       Comparison against human-labeled sample (n=100)
  Recall (per entity type)      ≥ 0.80       Comparison against human-labeled sample (n=100)
  F1 Score (overall)            ≥ 0.80       Harmonic mean of precision and recall
  Relation accuracy             ≥ 0.75       Manual verification of extracted relations
  False positive rate           ≤ 15%        Automated anomaly detection
  ----------------------------- ------------ -------------------------------------------------

**5.4 The HoundDog System**

The HoundDog system is Amplified Partners\' proprietary 33-methodology
extraction engine. It applies 33 distinct extraction techniques in
parallel across incoming documents, then consolidates results using a
voting mechanism. Where ≥ 3 techniques agree on an entity or
relationship, it is promoted to high-confidence status. Disagreements
are flagged for human review.

**5.5 PUDDING Analysis for Extraction**

The PUDDING technique identifies symbiotic technique combinations ---
pairs of extraction methods that, when combined, produce results
significantly better than either alone. This is the Swanson ABC model
applied to methodology: Method A extracts entities, Method B extracts
relationships, and the combination (A+B) reveals patterns invisible to
either method independently.

**6. Research --- The Discovery Engine**

**6.1 Vault Research Ingestion Format**

All research enters the system through the Vault Research Ingestion
Format v1.0, a two-layer storage architecture:

-   **Layer 1 --- Metadata (FalkorDB):** YAML-structured records with ID
    format RES-YYYY-MM-DD-NNN, containing source URL, credibility score,
    extraction status, and relationship mappings

-   **Layer 2 --- Raw Content (Filesystem):** Full-text content stored
    in the filesystem, linked to metadata by ID. This separation allows
    graph queries on metadata without loading full content.

**6.2 The RIC Nightly Scan**

The Rapid Intelligence Cycle operates a nightly scan across four source
tiers:

  ---------- ----------------------------- -------------------- ------------------------- --------------------------------
  **Tier**   **Source Type**               **Scan Frequency**   **Credibility Default**   **Example Sources**
  Tier 1     Primary regulatory/official   Daily                5/5                       HMRC, Companies House, FCA
  Tier 2     Quality financial press       Daily                4/5                       FT, Accountancy Age, ICAEW
  Tier 3     Industry publications         Weekly               3/5                       Trade journals, sector reports
  Tier 4     Community/emerging            Weekly               2/5                       Forums, social media, blogs
  ---------- ----------------------------- -------------------- ------------------------- --------------------------------

**6.3 RIC Evaluation Rubric**

Each research item is scored on 7 dimensions:

  ------------------------ ------------ ---------------------------------------------------------------
  **Dimension**            **Weight**   **Description**
  Source Credibility       20%          Tier ranking + historical accuracy
  Relevance                20%          Direct applicability to Amplified Partners\' domain
  Novelty                  15%          Does this add information not already in the knowledge graph?
  Actionability            15%          Can this be turned into a concrete improvement?
  Timeliness               10%          How current is this information?
  Cross-Domain Potential   10%          PUDDING indicator: could this connect disconnected domains?
  Evidence Quality         10%          Is the claim supported by data, case studies, or peer review?
  ------------------------ ------------ ---------------------------------------------------------------

**6.4 Radical Attribution**

Every finding in the knowledge graph must be traceable to its original
source. Radical Attribution is the principle that no claim exists in the
system without a URL, document reference, or audit trail entry. This
serves three purposes:

-   Verifiability: Any claim can be fact-checked by following its source
    chain

-   Accountability: If a source is later discredited, all dependent
    claims can be identified and flagged

-   Client confidence: Deliverables can show their evidence base on
    demand

**7. Scoring --- The Quality Measurement System**

**7.1 AMPS: The 0--10 Scale**

The Amplified Process Maturity Score (AMPS) is a 0--10 composite score
calculated across six weighted dimensions. AMPS is the universal quality
currency --- every atom, process, and deliverable carries an AMPS score.

  ---------------- ------------ ------------------------------------ ---------------------------------------------------------
  **Dimension**    **Weight**   **What It Measures**                 **Scoring Anchors**
  Completeness     20%          Are all required elements present?   0 = Nothing / 5 = Partial / 10 = Complete
  Accuracy         25%          Is the information correct?          0 = Wrong / 5 = Mostly right / 10 = Verified
  Consistency      15%          Does it align with other atoms?      0 = Contradicts / 5 = Neutral / 10 = Reinforces
  Actionability    15%          Can someone act on this?             0 = Theoretical / 5 = Guidance / 10 = Step-by-step
  Source Quality   15%          How reliable are the sources?        0 = Unsourced / 5 = Secondary / 10 = Primary + verified
  Timeliness       10%          How current is this?                 0 = Expired / 5 = Within year / 10 = Current month
  ---------------- ------------ ------------------------------------ ---------------------------------------------------------

**7.2 Process Readiness Score (PRS)**

**PRS Formula:** PRS = Σ(Dimension Score × Weight) / 10

The PRS maps directly to operational decisions:

  --------------- -------------- -----------------------------------------------------------------
  **PRS Range**   **Decision**   **Action Required**
  0.0 -- 4.9      ARCHIVE        Below minimum quality. Archive for future reference or discard.
  5.0 -- 6.9      REVIEW         Has potential but needs enrichment. Route to Research stage.
  7.0 -- 8.9      SHIP           Meets quality threshold. Proceed to Present and Ship stages.
  9.0 -- 10.0     GOLD           Exemplary quality. Flag as reference standard for calibration.
  --------------- -------------- -----------------------------------------------------------------

**7.3 Cp/Cpk Equivalents for AI Processes**

Traditional Six Sigma uses Cp and Cpk indices to measure process
capability. Research into statistical process control for knowledge work
([Lean Thinking for
Evals](https://www.productbreaks.com/p/lean-thinking-for-evals))
confirms that these concepts map to AI process quality:

  ----------------------- ------------------------------------ -----------------------------------------------------
  **Six Sigma Concept**   **AMPS Equivalent**                  **Interpretation**
  Cp ≥ 1.33               AMPS std dev ≤ 0.75 across evals     Process is capable (low variation)
  Cpk ≥ 1.0               AMPS mean ≥ 7.0 AND std dev ≤ 1.0    Process is centred and capable
  Control chart           AMPS score time series               Track process stability over time
  Out-of-control          AMPS drops \> 2σ from rolling mean   Triggers investigation and potential PUDDING revert
  ----------------------- ------------------------------------ -----------------------------------------------------

**7.4 The 10 Enforcer Roles**

The Master Process Document defines 10 Enforcer roles, each responsible
for validating specific aspects of quality:

  -------- --------------------------- ------------------------------------ -----------------------------------------
  **\#**   **Enforcer Role**           **Validation Domain**                **Override Authority**
  1        Source Verifier             Radical Attribution compliance       Can block Ship if sources missing
  2        Taxonomy Guardian           Classification correctness           Can force reclassification
  3        Score Auditor               AMPS calculation accuracy            Can adjust scores ± 1.0
  4        Test Witness                Test execution completeness          Can block Ship if tests skipped
  5        Consistency Checker         Cross-atom contradiction detection   Can flag for Research return
  6        Compliance Officer          Regulatory alignment                 Can block Ship for compliance gaps
  7        Client Relevance Assessor   Client applicability validation      Can deprioritise low-relevance atoms
  8        Temporal Validator          Currency and expiry checking         Can force time-based archival
  9        Presentation Auditor        Visual Polish System compliance      Can block Ship for presentation quality
  10       Owner Delegate              Final approval authority             Approve / Defer / Reject
  -------- --------------------------- ------------------------------------ -----------------------------------------

**8. Goals & Outcomes --- Alignment Architecture**

**8.1 The Hoshin Kanri X-Matrix Logic**

Amplified Partners\' goal alignment follows Hoshin Kanri (Policy
Deployment) principles, where strategic goals cascade to process-level
targets. The X-matrix structure connects four dimensions: strategic
objectives, annual targets, improvement priorities, and metrics.
Research confirms Hoshin Kanri\'s effectiveness for operationalising
strategy ([Hoshin Kanri
research](https://en.wikipedia.org/wiki/Hoshin_Kanri)). The Operations
Register is the primary instrument for this alignment.

**8.2 The Operations Register as Alignment Instrument**

The Operations Register contains 100 processes across 11 workstreams,
each with the following alignment structure:

  -------------------- --------------------------------------- -----------------------------------------
  **Column**           **Purpose**                             **Example**
  Process              Name of the operational process         Client Onboarding
  Ideal State          Outcome statement (Ulwick ODI format)   Minimise time to first value delivery
  Solution             How we achieve the ideal state          Automated intake + AMPS scoring
  Where They Are Now   Current maturity assessment             AMPS 4.2 --- manual, inconsistent
  How We Do It         Specific implementation approach        LangGraph workflow + FalkorDB templates
  KPI/Metric           Leading or lagging indicator            Days from contact to first deliverable
  Target               Quantified goal                         ≤ 5 business days
  Current              Latest measurement                      12 business days (average)
  Gap                  Difference between target and current   7 days (58% gap)
  Status               PUDDING / Kaizen / Stable               PUDDING --- active experimentation
  -------------------- --------------------------------------- -----------------------------------------

**8.3 OKR Cascade**

Strategic goals cascade through three levels:

**Level 1 --- Strategic Objectives:** Annual business outcomes (e.g.,
\'Become the go-to AI operations partner for UK SMBs\')

**Level 2 --- Process Targets:** Operations Register targets for each of
the 100 processes (e.g., \'Client onboarding ≤ 5 days\')

**Level 3 --- KPI Tracking:** Real-time metrics feeding gap analysis
(e.g., \'Current average: 12 days, Gap: 7 days\')

**8.4 Decision Logic for Reclassification**

When does a process move from PUDDING to Kaizen? The decision follows
explicit criteria:

**PUDDING → Kaizen Transition (all must be true):**

-   AMPS score ≥ 7.0 sustained for 2 consecutive weeks

-   Eval score plateau: \< 2% improvement in 5 consecutive overnight
    runs

-   Regression rate: \< 1 regression per 10 changes over 5-day window

-   Zero P0 incidents during the evaluation window

-   At least one unsolicited positive user signal

**Kaizen → PUDDING Revert (any one triggers):**

-   AMPS score drops below 6.0

-   Regression rate exceeds 3 per 10 changes

-   P0 incident occurs

-   External event invalidates process assumptions (e.g., regulatory
    change)

**8.5 TRL/MRL Readiness Levels Mapped to Departments**

Technology Readiness Levels (TRL) and Manufacturing Readiness Levels
(MRL), adapted from [NASA\'s TRL
framework](https://www.nasa.gov/directorates/somd/space-communications-navigation-program/technology-readiness-levels/),
map to Amplified Partners\' department structure:

  ------------- -------------------------------------- -------------------------- ---------------------
  **TRL/MRL**   **Stage Description**                  **Amplified Department**   **AMPS Equivalent**
  TRL 1--3      Basic research, proof of concept       R&D                        AMPS 0--4.9
  TRL 4--5      Lab validation, component testing      Chaos                      AMPS 5.0--6.9
  TRL 6--7      System demo, operational environment   Kaizen                     AMPS 7.0--8.9
  TRL 8--9      Operational, mission-qualified         Real                       AMPS 9.0--10.0
  ------------- -------------------------------------- -------------------------- ---------------------

**8.6 Improvement Velocity Formula**

**IV = (AMPS\_current − AMPS\_previous) / Time\_period**

Improvement Velocity (IV) measures the rate of quality improvement. A
positive IV means the system is getting better; a negative IV triggers
investigation. The target is not a specific IV value but a consistently
positive trend --- compound improvement over time.

**8.7 DORA Metrics Adapted for AI Knowledge Work**

The [DORA (DevOps Research and Assessment) metrics](https://dora.dev/)
translate to AI knowledge work as follows:

  ----------------------- ------------------------------------ ------------------------------------------------------
  **DORA Metric**         **Original Definition**              **Amplified Partners Adaptation**
  Deployment Frequency    How often code ships to production   How often atoms enter production knowledge graph
  Lead Time for Changes   Time from commit to production       Time from discovery to shipped atom
  Change Failure Rate     \% of deployments causing failure    \% of shipped atoms requiring rollback or correction
  Time to Restore         Time to recover from failure         Time to correct or retract a flawed atom
  ----------------------- ------------------------------------ ------------------------------------------------------

**9. Testing --- The Validation Engine**

Testing is the largest and most critical function at Amplified Partners.
The philosophy: **we do a shitload of tests and Kaizen quickly up to
about 10.** This section defines the complete testing framework, from
rapid PUDDING testing through compound Kaizen validation.

**9.1 The Two Testing Modes**

Testing operates in two modes aligned with the two operational rhythms:

  -------------------- -------------------------------------------- -----------------------------------------------
  **Dimension**        **PUDDING Testing**                          **Kaizen Testing**
  Objective            Discover if 10/10 is achievable              Prove improvements are real
  Duration             Hours to days                                Weeks to months
  Quality bar          \"Does it work at all?\" → \"Is it good?\"   \"Is it measurably better?\"
  Coverage             20% of golden dataset                        100% + production monitoring
  Rollback threshold   Fatal failures only                          Any regression
  Human involvement    High (daily eval review)                     Low (automated exception routing)
  Statistical rigour   Directional signals sufficient               Statistical significance required (p \< 0.05)
  -------------------- -------------------------------------------- -----------------------------------------------

**9.2 Tiered Aggression Model**

During PUDDING phases, testing follows a tiered aggression model that
increases rigour as the system matures ([Adaline Labs: Shipping Fast at
AI Speed](https://labs.adaline.ai/p/shipping-fast-and-iterating-at-ai)):

  ------------------------ ------------------------------------ -------------------------------------- ------------------------------
  **Phase**                **Objective**                        **Testing Pattern**                    **Quality Bar**
  Hour 0--4 (Hypothesis)   Is this worth building?              Dogfooding + manual probe              \"Does it work at all?\"
  Hour 4--24 (Viability)   Can this reach acceptable quality?   20 golden cases + smoke tests          \"No fatal failures\"
  Day 1--3 (Hardening)     Where are the edge cases?            Full golden dataset + property-based   \"80% of golden cases pass\"
  Day 3--7 (Validation)    Is this production-ready?            Full suite + chaos + load              \"PRS ≥ 7.0\"
  ------------------------ ------------------------------------ -------------------------------------- ------------------------------

**9.3 AI/LLM-Specific Testing Tools**

Amplified Partners uses three primary LLM evaluation tools, each serving
a distinct purpose ([Braintrust RAG Tool
Comparison](https://www.braintrust.dev/articles/best-rag-evaluation-tools);
[DeepEval
Documentation](https://docs.confident-ai.com/docs/getting-started)):

  ----------- -------------------------------------------- --------------------------------------------------------- -------------------------
  **Tool**    **Primary Use**                              **Key Metrics**                                           **Integration Point**
  DeepEval    Sprint regression suite, CI/CD integration   Faithfulness, Answer Relevancy, Hallucination, Toxicity   pytest + GitHub Actions
  RAGAS       FalkorDB retrieval quality evaluation        Context Precision, Context Recall, Answer Correctness     Overnight pipeline
  PromptFoo   Adversarial testing, red-teaming             Prompt injection resistance, jailbreak detection          Weekly security scan
  ----------- -------------------------------------------- --------------------------------------------------------- -------------------------

**9.4 LangGraph Testing Levels**

LangGraph agent testing follows three levels, from unit to end-to-end
([LangChain Forum: LangGraph Testing Best
Practices](https://forum.langchain.com/t/best-practices-for-testing-langgraph-nodes-separately/1396)):

  ---------------------- ------------------------- ------------------------------------------------------ -------------------------------
  **Level**              **Scope**                 **What\'s Tested**                                     **Tool**
  Node Unit Test         Single node/tool          Input → output correctness for one node                pytest + DeepEval
  Subgraph Integration   Connected node chain      Data flows correctly between nodes, state management   LangSmith/Langfuse traces
  E2E Agent Test         Full agent conversation   Multi-turn quality, goal completion, coherence         Golden dataset + LLM-as-judge
  ---------------------- ------------------------- ------------------------------------------------------ -------------------------------

**9.5 Overnight Testing Pipeline**

The overnight pipeline runs every night from 22:00 to 07:00 UTC,
executing the full test suite while The Beast is under minimal
production load ([QA.tech: CI/CD for AI
QA](https://qa.tech/blog/gitlab-ci-cd-vs-github-actions-a-side-by-side-guide-to-ai-qa-integration)):

  ---------- --------------------- ------------------------------------------------ --------------
  **Time**   **Phase**             **Tests Run**                                    **Duration**
  22:00      Unit Tests            All pytest unit tests + DeepEval metrics         \~30 min
  22:30      Integration Tests     LangGraph subgraph tests + FalkorDB queries      \~45 min
  23:15      Golden Dataset        Full 705-case golden dataset evaluation          \~2 hrs
  01:15      RAGAS Evaluation      Retrieval quality across all knowledge domains   \~1 hr
  02:15      Chaos Tests           ToxiProxy scenarios + model degradation          \~1.5 hrs
  03:45      Load Tests            k6 progressive load to target user tier          \~1 hr
  04:45      Regression Analysis   Semantic drift detection + A/B comparison        \~1 hr
  05:45      Report Generation     Morning report compilation + alerting            \~15 min
  06:00      Cleanup               Resource cleanup, log archival                   \~15 min
  ---------- --------------------- ------------------------------------------------ --------------

**Morning Report:** By 07:00, a structured report is available with:
overall pass/fail, regression list, drift indicators, performance
trends, and recommended actions. This report is reviewed at the daily
standup.

**9.6 Chaos Department Protocols**

Chaos engineering for AI systems follows the [Flakestorm 4-pillar
model](https://github.com/flakestorm) adapted for Amplified Partners\'
architecture ([arXiv: Chaos Engineering for LLM Multi-Agent
Systems](https://arxiv.org/pdf/2505.03096)):

**Pillar 1: Model Degradation**

Simulate gradual model quality loss by incrementally increasing
temperature over 10 steps. At each step, run the eval suite and record
the degradation curve. The quality threshold breach point reveals the
system\'s resilience margin.

**Pillar 2: Infrastructure Failure**

Use [ToxiProxy](https://github.com/Shopify/toxiproxy) to simulate
network degradation between Docker containers on The Beast: latency
injection (500ms to FalkorDB), bandwidth throttling (10KB/s), and
connection dropping (20% failure rate). Each scenario has an expected
resilience criterion.

**Pillar 3: Data Corruption**

Inject malformed data into the knowledge graph: incomplete atoms,
contradictory relationships, expired temporal data. Verify the system
detects and quarantines corrupted data rather than propagating it.

**Pillar 4: Adversarial Input**

Use [PromptFoo red-team
capabilities](https://www.promptfoo.dev/docs/red-team/) for prompt
injection testing, jailbreak attempts, and PII extraction attacks. The
target: zero successful adversarial attacks in automated weekly scans.

**9.7 Golden Dataset Design: The 705-Case Specification**

The golden dataset is the fixed reference point for all regression
testing. Its design follows principles from [DAC.digital golden dataset
research](https://dac.digital/what-is-a-golden-dataset/):

  --------------------------- ----------- ------------------------------------------------- -------------------------
  **Category**                **Count**   **Annotation Requirements**                       **Refresh Cadence**
  Visual polish scoring       150         Score + 3-sentence reasoning                      Monthly review
  Invoice extraction          100         Structured fields (total, date, vendor, VAT)      Quarterly
  Financial Q&A               200         Expected answer + supporting evidence citations   Bi-monthly
  Knowledge graph traversal   100         Correct entity relationships + expected path      Monthly
  Multi-turn conversation     50          Full conversation + quality rubric                Monthly
  Adversarial inputs          75          Expected rejection/deflection                     Per new attack type
  Cross-session isolation     30          Confirm zero data leakage                         Per architecture change
  --------------------------- ----------- ------------------------------------------------- -------------------------

**Total: 705 cases**. The golden dataset grows from production failures
--- the overnight pipeline automatically promotes low-scoring production
traces to candidate test cases, routed to human review before inclusion.

**9.8 Regression Prevention**

AI regression testing uses distribution comparison rather than equality
checking, because valid LLM outputs are a distribution, not a point:

-   **Semantic similarity drift:** Cosine distance \> 0.15 in output
    embeddings indicates meaningful semantic drift ([Leanware drift
    detection
    guide](https://www.leanware.co/insights/llm-monitoring-drift-detection-guide))

-   **A/B semantic comparison:** New model versions are compared using
    pairwise LLM-as-judge with position bias elimination --- run judge
    twice with swapped positions

-   **Drift trend detection:** Linear regression on 7-day rolling
    scores. Slope \< -0.005 (losing 0.5% quality per day) triggers
    alert; slope \< -0.02 triggers immediate investigation

**9.9 Canary Deployment Protocol**

Validated changes deploy via progressive canary rollout ([Clarifai: AI
Model Deployment
Strategies](https://www.clarifai.com/blog/ai-model-deployment-strategies)):

  -------------- ------------------------------------ -------------- --------------------------------------------------
  **Stage**      **Traffic Split**                    **Duration**   **Gate Criteria**
  Shadow Mode    0% production, 100% shadow logging   48--96 hours   Shadow similarity ≥ 0.85 to production
  Canary 1%      1% real traffic                      24 hours       Latency regression ≤ 20%, error rate ≤ +0.1%
  Canary 5%      5% real traffic                      24 hours       Judge preference ≥ 50%, zero security violations
  Canary 25%     25% real traffic                     48 hours       Similarity ≥ 0.87, judge preference ≥ 55%
  Full Rollout   100% real traffic                    Continuous     Kaizen phase begins
  -------------- ------------------------------------ -------------- --------------------------------------------------

**Automated rollback:** Any gate failure triggers automatic rollback to
the previous version within 5 minutes. No manual intervention required.

**9.10 The 76-Test Precedent and Extension**

The Visual Polish System established the pattern with 76 automated tests
covering presentation quality. This precedent --- dense, automated,
threshold-based testing --- is the model for every system at Amplified
Partners. The composite formula and Kaizen acceptance logic from VPS are
applied universally:

-   **Composite Score:** Weighted average of all test dimensions

-   **Ship Threshold:** ≥ 7.0 composite

-   **Gold Standard:** ≥ 9.0 composite

-   **Kaizen Acceptance:** New version must score ≥ previous version on
    all dimensions (zero regression tolerance)

**9.11 Testing at Scale Thresholds**

As user count grows, testing requirements change qualitatively, not just
quantitatively ([Netflix scaling
patterns](https://www.youtube.com/watch?v=6DQzFUDkQB8)):

  -------------------------- ------------------------------------------------------------------------ ---------------------------------
  **User Tier**              **New Testing Requirements**                                             **Testing Investment**
  1--10 (Proof of Concept)   Manual exploration, 20--30 golden cases, basic unit tests                5 hours initial setup
  10--100 (Alpha/Beta)       Concurrency testing, session isolation, overnight pipeline               Automated pipeline mandatory
  100--1,000 (Public Beta)   Drift detection (Evidently AI), SLO-linked tests, cost tracking          Observability stack validation
  1,000--10,000 (Growth)     Chaos programme, multi-tenant isolation, GDPR erasure testing            Dedicated testing sprint weekly
  10,000+ (Scale)            Statistical anomaly detection, continuous red-team, testing governance   SRE function required
  -------------------------- ------------------------------------------------------------------------ ---------------------------------

**9.12 Testing Maturity Pyramid**

The testing maturity pyramid is additive --- each layer adds on top of
all previous layers:

1.  **Foundation (1+ users):** DeepEval + LangSmith + Golden Dataset +
    Property-Based Tests + Exploratory Testing --- START HERE, NEVER
    REMOVE

2.  **Automated (10+ users):** Overnight Pipeline + Concurrency +
    Isolation Tests + Load Baselines

3.  **Monitored (100+ users):** SLO-linked tests + Drift Detection +
    Cost Monitoring

4.  **Resilient (1,000+ users):** Chaos Engineering Programme + GameDays

5.  **Hardened (10,000+ users):** Adversarial Red-Teaming + Statistical
    Anomaly Detection + Testing Governance

**9.13 Statistical Validation for Kaizen Claims**

Every Kaizen improvement claim must be statistically validated. For
ordinal LLM quality scores (1--10 scale), the appropriate tests are
([Lean Thinking for
Evals](https://www.productbreaks.com/p/lean-thinking-for-evals)):

  ------------------------------------------- ---------------------- -------------------------------------
  **Sample Condition**                        **Statistical Test**   **Significance Threshold**
  Normal distribution, n ≥ 30 per condition   Welch\'s t-test        p \< 0.05
  Non-normal or n \< 30                       Mann-Whitney U test    p \< 0.05
  Effect size                                 Cohen\'s d             d \> 0.2 for practical significance
  ------------------------------------------- ---------------------- -------------------------------------

**Minimum sample sizes for Kaizen claims (80% statistical power):**

  ---------------------- ------------------ --------------------------------------
  **Improvement Size**   **Score Change**   **Required Samples (per condition)**
  Large                  +0.5 points        30
  Medium                 +0.3 points        80
  Small                  +0.1 points        700
  ---------------------- ------------------ --------------------------------------

**10. The PUDDING → Kaizen Transition**

**10.1 When PUDDING Ends and Kaizen Begins**

The transition from PUDDING to Kaizen is both a technical and business
decision. The technical signal is stability; the business signal is
diminishing marginal returns from experiments ([arXiv: Evaluation-Driven
Development](https://arxiv.org/html/2411.13768v3)).

**Technical Stability Signals (ALL must be met):**

-   Eval score plateau: overnight scores haven\'t improved \> 2% in 5
    consecutive runs

-   Regression rate: \< 1 regression per 10 changes over a 5-day window

-   Error rate stabilises: P95 stays within ± 20% for 72 consecutive
    hours

-   User behaviour normalises: session lengths and abandonment rates
    stabilise

**The 2-Week Production Clock:**

Two weeks in production means ALL of the following:

-   ≥ 14 days of production traffic

-   ≥ 100 unique user sessions (not just 14 days of zero-traffic)

-   ≥ 2 overnight eval runs with pass rate ≥ 90%

-   Zero P0 incidents (security breaches, data leakage, complete
    outages)

-   At least one unsolicited positive user signal

*If the system hasn\'t hit all five criteria after 14 days, extend
PUDDING. If it hits all five in 10 days, start Kaizen early.*

**10.2 The Reclassification Rubric**

  -------------------------- ------------------------------------ ---------------------------------
  **Criterion**              **Pass Condition**                   **Fail Action**
  AMPS Score                 ≥ 7.0 sustained for 14 days          Continue PUDDING
  Overnight Eval Pass Rate   ≥ 90% for 2+ consecutive runs        Investigate failing tests
  Regression Rate            \< 1 per 10 changes (5-day window)   Root cause analysis
  P0 Incidents               Zero during evaluation window        Incident review, extend PUDDING
  User Signal                ≥ 1 unsolicited positive             Seek feedback, extend if silent
  -------------------------- ------------------------------------ ---------------------------------

**10.3 Shadow Mode: The Bridge**

Shadow mode is the cleanest bridge between PUDDING and Kaizen. The
Kaizen candidate receives real production traffic and generates outputs,
but does not serve them to users. After 48--96 hours, the decision rule:
if similarity ≥ 0.85 to production AND A/B judge prefers shadow in ≥ 55%
of cases → promote to canary ([Clarifai deployment
strategies](https://www.clarifai.com/blog/ai-model-deployment-strategies);
[AWS: Safe LLM Model
Migration](https://builder.aws.com/content/3AYkLiI5DNmsG9F2fcI8JrDnLU8/safe-llm-model-migration-on-aws-validate-govern-and-operate-with-confidence)).

**10.4 Reverse Reclassification: Kaizen → PUDDING Revert**

Stable systems can become unstable. The following triggers force a
revert from Kaizen back to PUDDING:

**DECISION FLOWCHART --- KAIZEN → PUDDING REVERT:**

IF AMPS score drops below 6.0 → REVERT to PUDDING

IF regression rate exceeds 3 per 10 changes → REVERT to PUDDING

IF P0 incident occurs → IMMEDIATE REVERT + Incident Review

IF external event invalidates assumptions → REVERT to PUDDING + Re-scope

IF user satisfaction drops \> 20% week-over-week → REVERT + Root Cause
Analysis

**10.5 Compound Improvement Tracking**

Kaizen\'s power is compound improvement --- getting better at getting
better. Track this with:

-   **Improvement Velocity (IV):** Period-over-period AMPS change rate.
    Target: consistently positive.

-   **Improvement Acceleration:** Rate of change of IV. Positive
    acceleration = compounding gains.

-   **Time-to-Quality:** How many Kaizen cycles to move 1 AMPS point?
    Should decrease over time.

**10.6 Review Cadences**

  ------------- -------------------------------------------------------------------- ---------------------- ------------------------------------------
  **Cadence**   **What\'s Reviewed**                                                 **Who Participates**   **Output**
  Daily         Overnight eval report, regressions, drift metrics                    Standup team           Triage list for the day
  Weekly        Golden dataset +5--10 cases, Kaizen claims, chaos results            Full team              Updated golden dataset, validated claims
  Monthly       50 sampled prod outputs, load test, GameDay, security scan           Full team + owner      Maturity assessment, updated OKRs
  Quarterly     Operations Register full review, TRL assessment, IV trend analysis   Owner + leads          Strategic priorities for next quarter
  Annual        Full methodology review, framework version update                    All                    AMF version increment
  ------------- -------------------------------------------------------------------- ---------------------- ------------------------------------------

**11. Infrastructure**

**11.1 The Beast --- Production Spine**

The Beast (Hetzner AX162-R, Falkenstein, Germany) is the always-on
production spine. It runs 29+ Docker containers providing all persistent
services. Key specifications: AMD EPYC 48-core CPU, 256 GB DDR5 RAM,
direct-attached NVMe storage, 10 Gbit/s unmetered network. Monthly cost:
approximately €230--280 fixed ([Hetzner dedicated
servers](https://www.hetzner.com/dedicated-rootserver)).

**11.2 RunPod --- Burst GPU Muscle**

RunPod Secure Cloud provides burst GPU compute for training,
fine-tuning, batch inference, and chaos testing. GDPR-verified with EU
data centres in France (EU-FR-1) and Netherlands (EU-NL-1). Per-second
billing with on-demand pricing ([RunPod GPU
Pricing](https://www.runpod.io/gpu-pricing)).

  ------------------------- --------------------- ------------- ----------------------------
  **Workload**              **Recommended GPU**   **Cost/hr**   **Notes**
  Fine-tuning (70B QLoRA)   H100 PCIe 80GB        \$1.99        40--60GB VRAM required
  Fine-tuning (30B QLoRA)   A100 PCIe 80GB        \$1.19        Best value for 80GB
  Batch inference (70B)     A100 SXM 80GB         \$1.39        Best throughput per dollar
  Embedding generation      L40S 48GB             \$0.79        High throughput
  Chaos testing             RTX 4090 × N          \$0.34 each   Cheap, parallelisable
  Quick experiment          RTX 4090              \$0.34        24GB, fast iteration
  ------------------------- --------------------- ------------- ----------------------------

**11.3 Core Data Stores**

  ------------ -------------------------------------------------- -------------- -------------------------------------------------
  **System**   **Role**                                           **Location**   **Key Configuration**
  FalkorDB     Knowledge graph (atoms, relationships, taxonomy)   The Beast      Redis-compatible, graph queries
  Qdrant       Vector storage for embeddings                      The Beast      GPU-accelerated HNSW indexing (burst on RunPod)
  PostgreSQL   Client data, operational records, audit trails     The Beast      ACID-compliant, full backup regime
  Redis        Cache, session state                               The Beast      In-memory, ephemeral data
  ------------ -------------------------------------------------- -------------- -------------------------------------------------

**11.4 Orchestration and Tracing**

  ------------ ------------------------------------ --------------------------------------------------------------------
  **System**   **Role**                             **Key Capability**
  LangGraph    Agent orchestration                  Stateful, multi-step agent workflows with traceability
  Langfuse     Self-hosted tracing and evaluation   Data sovereignty --- runs on The Beast, full trace searchability
  Ollama       LLM serving (CPU inference)          Always-on inference for qwen3-coder:30b, llama3.1:70b, llama3.1:8b
  Traefik      Reverse proxy                        SSL termination, routing, rate limiting
  SearXNG      Search proxy                         Privacy-respecting metasearch
  ------------ ------------------------------------ --------------------------------------------------------------------

**11.5 Networking: Beast ↔ RunPod**

The Beast and RunPod pods communicate via
[Tailscale](https://tailscale.com/docs/install/cloud/hetzner)
(WireGuard-based mesh VPN). All traffic is encrypted end-to-end.
Expected latency: 15--30ms round-trip between Hetzner Falkenstein and
RunPod EU-FR-1.

**11.6 Data Sovereignty Architecture**

Strict data classification rules govern what stays on The Beast vs. what
can be sent to RunPod:

  ------------------------ ------------------------- ---------------------------------------------------------------------------------
  **Classification**       **Location**              **Examples**
  STAYS ON THE BEAST       The Beast only            Client PII, PostgreSQL, FalkorDB (client relationships), API keys, audit logs
  SAFE TO SEND TO RUNPOD   Either                    Model weights, anonymised training data, synthetic data, research corpora, code
  SEND WITH CARE           RunPod with precautions   Aggregated non-attributable analytics, prompts stripped of identifying info
  ------------------------ ------------------------- ---------------------------------------------------------------------------------

**12. The Decision Logic**

**12.1 Master Decision Tree: \"Something New Appeared --- What Do I
Do?\"**

This decision tree governs the routing of every new piece of information
that enters the system. It is the operational heart of the AMF.

**STEP 1: SOURCE ASSESSMENT**

→ What tier is the source? (Tier 1--4 per RIC classification)

→ IF Tier 1 or 2: Proceed to scoring (high-credibility fast track)

→ IF Tier 3 or 4: Apply enhanced validation before scoring

**STEP 2: INITIAL SCORING**

→ Score on RIC 7-dimension rubric

→ IF composite score \< 3.0: DISCARD (log reason, update source
credibility)

→ IF composite score 3.0--5.0: ARCHIVE (store for potential future
relevance)

→ IF composite score \> 5.0: Proceed to CLASSIFY

**STEP 3: CLASSIFICATION**

→ Assign atom ID (AMP-{APQC\#}-{SEQ}-{VERSION})

→ Apply 5-layer taxonomy (WHAT.HOW.SCALE.TIME.CONTEXT)

→ Check for duplicates in FalkorDB

→ IF duplicate: MERGE with existing atom (increment version)

→ IF novel: Proceed to EXTRACT

**STEP 4: EXTRACTION AND ENRICHMENT**

→ Run GLiNER2 NER/RE pipeline

→ Verify extraction F1 ≥ 0.80

→ IF extraction quality low: Route to manual extraction

→ IF extraction quality acceptable: Proceed to AMPS SCORING

**STEP 5: AMPS SCORING**

→ Score across 6 weighted dimensions

→ IF AMPS \< 5.0: ARCHIVE (below minimum quality)

→ IF AMPS 5.0--6.9: Route to RESEARCH for enrichment

→ IF AMPS ≥ 7.0: Proceed to TESTING

**STEP 6: TESTING**

→ Run appropriate test suite (PUDDING tiered or Kaizen full)

→ Calculate PRS from test results

→ IF PRS \< 7.0: Return to RESEARCH with test feedback

→ IF PRS ≥ 7.0: Proceed to PRESENT

**STEP 7: PRESENTATION AND APPROVAL**

→ Format for delivery (Visual Polish System)

→ IF Visual Polish Score \< 7.0: Return to PRESENT with feedback

→ IF Visual Polish Score ≥ 7.0: Route to OWNER

**STEP 8: OWNER CONSENT PROTOCOL**

→ Owner reviews: full atom with scores, test results, sources

→ APPROVE: Ship to production knowledge graph

→ DEFER: Hold for specified condition (e.g., \'wait for Q2 HMRC
update\')

→ REJECT: Archive with rejection reason

**STEP 9: DEPARTMENT ROUTING**

At each decision point, ownership transfers to the appropriate
department:

  -------------------- ----------------- -------------------------------------------------------
  **Decision Point**   **Department**    **Escalation Rule**
  Source assessment    R&D (automated)   Manual review if Tier 4 scores \> 7.0
  Classification       R&D               Taxonomy Guardian reviews if novel category needed
  Extraction           R&D               Manual extraction if automated F1 \< 0.80
  Scoring              Chaos             Score Auditor reviews if AMPS = 6.5--7.5 (borderline)
  Testing              Chaos             Test Witness reviews all test-skip requests
  Presentation         Kaizen            Presentation Auditor reviews border-line scores
  Approval             Real (Owner)      No delegation --- owner signs off personally
  -------------------- ----------------- -------------------------------------------------------

**12.2 Escalation Rules**

Automated → Manual escalation triggers:

-   Any atom scoring within 0.5 of a threshold boundary (e.g., AMPS
    6.5--7.5)

-   Any atom touching regulatory/compliance topics (mandatory Compliance
    Officer review)

-   Any atom flagged by adversarial testing

-   Any atom requiring cross-domain PUDDING analysis (novel connection)

-   System confidence \< 0.85 on any automated decision

**Appendix A: Complete Taxonomy Layer Reference**

This appendix provides the complete reference for the 5-layer taxonomy
system, APQC PCF mapping, and faceted classification format.

**A.1 APQC Level 1 Categories (Full List)**

  -------- ---------------------------------------------------- ----------------------------------
  **\#**   **Category**                                         **Amplified Workstream Mapping**
  1.0      Develop Vision and Strategy                          Strategy & Planning
  2.0      Develop and Manage Products and Services             Product Development
  3.0      Market and Sell Products and Services                Marketing & Sales
  4.0      Deliver Products and Services                        Service Delivery
  5.0      Manage Customer Service                              Client Operations
  6.0      Develop and Manage Human Capital                     People Operations
  7.0      Manage Information Technology                        Technology Operations
  8.0      Manage Financial Resources                           Finance
  9.0      Acquire, Construct, and Manage Assets                Asset Management
  10.0     Manage Enterprise Risk, Compliance, and Resilience   Risk & Compliance
  11.0     Manage External Relationships                        Partnerships
  12.0     Develop and Manage Business Capabilities             Capability Building
  13.0     Manage Knowledge, Improvement, and Change            Knowledge Management
  -------- ---------------------------------------------------- ----------------------------------

**A.2 Facet Definitions**

  ----------- ---------------------- -------------------------------------------- --------------------
  **Facet**   **Format**             **Allowed Values**                           **Example**
  WHAT        Lowercase hyphenated   Domain-specific vocabulary                   tax-compliance
  HOW         Lowercase hyphenated   Method/technique descriptors                 digital-submission
  SCALE       Predefined enum        micro, smb, mid-market, enterprise, global   smb
  TIME        ISO-8601 derived       YYYY, YYYY-QN, YYYY-MM, evergreen            2026-q2
  CONTEXT     Lowercase hyphenated   Geographic + regulatory qualifiers           uk-hmrc
  ----------- ---------------------- -------------------------------------------- --------------------

**Appendix B: Scoring Rubric Templates**

**B.1 AMPS Scoring Template**

  ---------------- ------------ ------------------- -------------------- ----------------------
  **Dimension**    **Weight**   **Score (0--10)**   **Weighted Score**   **Evidence / Notes**
  Completeness     20%          \[ \]               \[ \]                
  Accuracy         25%          \[ \]               \[ \]                
  Consistency      15%          \[ \]               \[ \]                
  Actionability    15%          \[ \]               \[ \]                
  Source Quality   15%          \[ \]               \[ \]                
  Timeliness       10%          \[ \]               \[ \]                
  TOTAL            100%         ---                 \[ \] / 10           PRS = Total ÷ 10
  ---------------- ------------ ------------------- -------------------- ----------------------

**B.2 RIC Evaluation Template**

  ------------------------ ------------ ------------------ --------------------
  **Dimension**            **Weight**   **Score (1--5)**   **Weighted Score**
  Source Credibility       20%          \[ \]              \[ \]
  Relevance                20%          \[ \]              \[ \]
  Novelty                  15%          \[ \]              \[ \]
  Actionability            15%          \[ \]              \[ \]
  Timeliness               10%          \[ \]              \[ \]
  Cross-Domain Potential   10%          \[ \]              \[ \]
  Evidence Quality         10%          \[ \]              \[ \]
  TOTAL                    100%         ---                \[ \] / 5
  ------------------------ ------------ ------------------ --------------------

**B.3 PRS Decision Matrix**

  --------------- -------------- ------------------------------------- ---------------------------
  **PRS Score**   **Decision**   **Next Step**                         **Owner Notification**
  0.0 -- 4.9      ARCHIVE        Store in archive, no further action   Weekly digest only
  5.0 -- 6.9      REVIEW         Route to Research for enrichment      Notify if client-relevant
  7.0 -- 8.9      SHIP           Proceed to Present → Ship             Approval required
  9.0 -- 10.0     GOLD           Ship + flag as calibration standard   Celebrate + approval
  --------------- -------------- ------------------------------------- ---------------------------

**Appendix C: Testing Checklist by Pipeline Stage**

  -------------------- ------------------------ --------------------------------------- ------------------------------
  **Pipeline Stage**   **Test Type**            **Minimum Tests**                       **Pass Criteria**
  Discover             Source validation        Credibility score + duplicate check     Source tier verified
  Classify             Taxonomy validation      APQC mapping + facet completeness       All 5 layers assigned
  Extract              Extraction quality       Precision, Recall, F1 per entity type   F1 ≥ 0.80
  Score                Scoring audit            6-dimension AMPS calculation            Score auditor sign-off
  Research             Attribution check        Every claim has source URL              100% Radical Attribution
  Test                 Full test suite          Golden dataset + chaos + regression     PRS ≥ 7.0
  Present              Visual polish            76-test Visual Polish System            Composite ≥ 7.0
  Ship                 Deployment validation    Canary gates + shadow comparison        All gates pass
  Kaizen               Improvement validation   Statistical significance test           p \< 0.05, Cohen\'s d \> 0.2
  -------------------- ------------------------ --------------------------------------- ------------------------------

**Appendix D: Tool & Infrastructure Quick Reference**

**D.1 Testing Tool Stack**

  ------------ ---------------------------- -------------------------- -------------------------
  **Tool**     **Purpose**                  **Install Command**        **Integration**
  DeepEval     Sprint regression suite      pip install deepeval       pytest + GitHub Actions
  RAGAS        FalkorDB retrieval quality   pip install ragas          Overnight pipeline
  PromptFoo    Adversarial testing          npm install -g promptfoo   Weekly security scan
  Hypothesis   Property-based testing       pip install hypothesis     Unit test suite
  ToxiProxy    Network chaos                Docker image               Nightly chaos runs
  Flakestorm   AI agent chaos               pip install flakestorm     Chaos department
  k6           Load testing                 brew install k6            Overnight + scale tests
  Langfuse     Self-hosted tracing          Docker image               All LangGraph runs
  ------------ ---------------------------- -------------------------- -------------------------

**D.2 Infrastructure Summary**

  ------------------ --------------------- -------------------- ---------------------------------
  **Component**      **Technology**        **Location**         **Purpose**
  Production Spine   Hetzner AX162-R       Falkenstein, DE      Always-on services, client data
  Burst GPU          RunPod Secure Cloud   EU-FR-1 / EU-NL-1    Training, fine-tuning, batch
  Knowledge Graph    FalkorDB              The Beast (Docker)   Atom storage, relationships
  Vector Store       Qdrant                The Beast (Docker)   Embeddings, semantic search
  Relational DB      PostgreSQL            The Beast (Docker)   Client data, audit trails
  Cache              Redis                 The Beast (Docker)   Session state, caching
  LLM Serving        Ollama                The Beast (Docker)   CPU inference (qwen3, llama3.1)
  Agent Framework    LangGraph             The Beast (Docker)   Multi-step agent orchestration
  Reverse Proxy      Traefik               The Beast (Docker)   SSL, routing, rate limiting
  Search             SearXNG               The Beast (Docker)   Privacy-respecting metasearch
  VPN                Tailscale             Beast + RunPod       Encrypted Beast ↔ RunPod tunnel
  ------------------ --------------------- -------------------- ---------------------------------

**D.3 GPU Selection Cheat Sheet**

  ---------------------------- ---------------- -------------- ----------
  **Task**                     **GPU**          **Price/hr**   **VRAM**
  Quick experiment             RTX 4090         \$0.34         24 GB
  Production fine-tune (30B)   A100 PCIe 80GB   \$1.19         80 GB
  Production fine-tune (70B)   H100 PCIe 80GB   \$1.99         80 GB
  Batch inference (70B)        A100 SXM 80GB    \$1.39         80 GB
  Multi-GPU training           H100 SXM         \$2.69         80 GB
  Embedding generation         L40S 48GB        \$0.79         48 GB
  ---------------------------- ---------------- -------------- ----------

**Appendix E: Glossary of Terms**

  --------------------------- ------------------------------------------------------------------------------------------------
  **Term**                    **Definition**
  AMF                         Amplified Methodology Framework --- this document
  AMPS                        Amplified Process Maturity Score --- 0--10 composite quality score across 6 dimensions
  Atom                        The fundamental unit of knowledge in the Amplified system
  APQC PCF                    Association for Process Classification Framework --- hierarchical business process taxonomy
  Canary Deployment           Progressive traffic routing (1% → 5% → 25% → 100%) with automated gating
  Chaos Department            Team responsible for deliberately breaking systems to prove resilience
  Cohen\'s d                  Statistical measure of effect size; d \> 0.2 = practically significant
  DORA Metrics                DevOps Research and Assessment --- deployment frequency, lead time, failure rate, restore time
  FalkorDB                    Redis-compatible graph database used for the knowledge graph
  Flakestorm                  AI agent chaos engineering platform
  GLiNER2                     Zero-shot Named Entity Recognition model
  Golden Dataset              Curated 705-case evaluation set; the fixed reference for regression testing
  HoundDog                    Amplified Partners\' 33-methodology extraction engine
  Hoshin Kanri                Japanese policy deployment framework for strategic alignment
  Improvement Velocity (IV)   Rate of AMPS score change per period
  Kaizen                      Compound improvement rhythm --- small, statistically validated improvements over time
  Krippendorff\'s Alpha       Inter-annotator agreement metric; target ≥ 0.7
  LangGraph                   Framework for building stateful, multi-step AI agent workflows
  Langfuse                    Self-hosted LLM tracing and evaluation platform
  Operations Register         100-process register across 11 workstreams with gap analysis
  PRS                         Process Readiness Score --- derived from AMPS, determines ship/defer/archive decisions
  PUDDING                     Rapid discovery methodology (Literature-Based Discovery lineage from Don Swanson)
  Qdrant                      Vector database for embedding storage and semantic search
  Radical Attribution         Principle that every claim must trace to a source URL or document
  RIC                         Rapid Intelligence Cycle --- nightly scan across 4 source tiers with 7-dimension rubric
  RunPod                      GPU cloud provider for burst compute (training, fine-tuning, batch inference)
  Shadow Mode                 Pre-production validation where candidate receives real traffic without serving users
  SKOS                        Simple Knowledge Organization System --- W3C standard for semantic vocabularies
  The Beast                   Hetzner AX162-R dedicated server --- Amplified Partners\' production infrastructure
  ToxiProxy                   Network fault injection tool for chaos testing between Docker containers
  Visual Polish System        76-automated-test quality system for presentation scoring
  --------------------------- ------------------------------------------------------------------------------------------------

**Document Control**

  ---------------- -------------------------------------------
  **Field**        **Value**
  Document Title   The Amplified Methodology Framework (AMF)
  Version          1.0
  Date             March 2026
  Author           Amplified Partners
  Classification   Confidential --- Internal Use Only
  Review Cadence   Quarterly (next review: June 2026)
  Approved By      Ewan --- Amplified Partners
  ---------------- -------------------------------------------

**Sources and References:**

All claims in this document are sourced from the following research
files and external references:

-   Taxonomy & Labeling Research ([APQC
    PCF](https://www.apqc.org/process-frameworks), [W3C
    SKOS](https://www.w3.org/2004/02/skos/))

-   Goals & Outcomes Research ([DORA Metrics](https://dora.dev/),
    [Hoshin Kanri](https://en.wikipedia.org/wiki/Hoshin_Kanri))

-   Testing Research
    ([DeepEval](https://docs.confident-ai.com/docs/getting-started),
    [PromptFoo](https://www.promptfoo.dev/docs/red-team/),
    [RAGAS](https://www.braintrust.dev/articles/best-rag-evaluation-tools))

-   Process Idealisation Research (TPS/Lean, Six Sigma, ToC, V-Model,
    CMMI, PDCA)

-   Testing Methodology Research ([Chaos Engineering for
    LLM-MAS](https://arxiv.org/pdf/2505.03096), [Golden
    Datasets](https://dac.digital/what-is-a-golden-dataset/))

-   Compute Scaling Research
    ([RunPod](https://www.runpod.io/gpu-pricing), [Lambda
    Labs](https://lambda.ai/pricing), [Vast.ai](https://vast.ai))

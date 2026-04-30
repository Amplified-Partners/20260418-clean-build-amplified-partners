---
title: "Thought Model Addendum"
id: "thought-model-addendum"
version: 1
created: 2026-04-25
last_validated: 2026-04-25
type: document
topic_type: reference
status: imported
source_file: "thought-model-addendum.docx"
signed_by: "Devon, 2026-04-25, devin-992682c244cf444f91e0a516498afbfd"
---

PRE-BUILD THOUGHT MODEL --- ADDENDUM

Data Growth, Process Scoring, Defrictioning Cycles & Staff Redistribution

**Amplified Partners**

March 2026

CONFIDENTIAL --- Internal Strategy Document

Prepared for Ewan Bramley, Founder & CEO

**Table of Contents**

*Note: Update this table of contents by right-clicking and selecting \'Update Field\' after opening in Microsoft Word.*

**1. Data Growth Model & Beast Capacity Planning**

**1.1 Current State: The Beast Infrastructure**

Amplified Partners operates its entire AI infrastructure stack on a single dedicated server --- internally designated \'The Beast\' --- hosted by Hetzner. This architecture provides the raw compute and memory headroom required for multi-tenant graph database operations, large language model inference, and containerised microservices, all without the variable-cost unpredictability of hyperscale cloud providers.

**1.1.1 Beast Hardware Specifications**

  --------------- ----------------------------------------- ------------------------------------------
  **Component**   **Specification**                         **Role in Stack**
  Server Model    Hetzner AX162-R                           Dedicated bare-metal
  Processor       AMD EPYC 9454 --- 48 cores / 96 threads   Parallel workload execution
  RAM             256 GB DDR5 ECC                           In-memory graph databases, LLM inference
  Storage         2 × 1.92 TB NVMe SSD (RAID 1)             Data durability + fast I/O
  Network         10 Gbps symmetric                         High-throughput API + data transfer
  OS              Ubuntu 22.04 LTS                          Production-grade Linux
  --------------- ----------------------------------------- ------------------------------------------

**1.1.2 Current Software Allocation**

  -------------------- ------------------------ -------------------------------------------------------
  **Service**          **Current Allocation**   **Purpose**
  FalkorDB             8 GB RAM / 8 threads     Primary knowledge graph store (per-client namespaces)
  Ollama               96 GB RAM                Local LLM inference (Llama, Mistral, embeddings)
  Docker Containers    \~36 active containers   Microservices: API, workers, queues, monitoring
  Qdrant               \~8 GB RAM               Vector similarity search (57,434 points migrated)
  System + OS          \~12 GB RAM              Kernel, networking, orchestration overhead
  Available Headroom   \~130 GB RAM             Expansion capacity for growth phases 1-2
  -------------------- ------------------------ -------------------------------------------------------

**1.2 Growth Drivers**

Four primary data sources drive capacity requirements as the platform scales across client accounts:

  ----------------------------- ---------------------------------------------------------- ------------------------------------------------------------------ -------------------------------------------
  **Growth Driver**             **Current Scale**                                          **Growth Trajectory**                                              **Capacity Impact**
  Vault (Knowledge Base)        4,787 files / 3.3M words                                   Linear with content creation + client onboarding                   Storage + embedding compute
  Per-Client Graphs             Each client receives isolated kg\_{client\_id} namespace   1 graph per client; sub-linear RAM per graph                       FalkorDB memory + thread contention
  Graphiti Episodic Ingestion   Conversations + events → entity nodes + temporal edges     Exponential per active client (every interaction generates data)   CPU for extraction; RAM for active graphs
  Qdrant Vector Store           57,434 points (post-migration)                             Linear with indexed content; grows slower than raw storage         RAM for HNSW index; SSD for payloads
  ----------------------------- ---------------------------------------------------------- ------------------------------------------------------------------ -------------------------------------------

Each client that onboards brings a predictable initial data footprint (vault documents, historical data import) plus an ongoing episodic data stream from Graphiti. The per-client graph isolation model (kg\_{client\_id}) ensures data sovereignty whilst enabling federated learning patterns at the aggregate level.[^1]

**1.3 Four-Phase Scaling Projection**

The following projection maps resource requirements against client count milestones. Each phase includes specific infrastructure actions required to maintain performance SLAs.

  ----------- ------------------ --------------------------------------------- ------------------------------ ---------------------------------------------------------------------
  **Phase**   **Client Count**   **FalkorDB Config**                           **RAM Utilisation**            **Infrastructure Action**
  Phase 1     0--10 clients      8 → 16 GB / 8 → 12 threads                    \~126 GB of 256 GB (\~49%)     Monitor graph sizes; increase FalkorDB allocation
  Phase 2     10--50 clients     16 → 32 GB / 12 → 16 threads                  \~180 GB of 256 GB (\~70%)     Dedicated FalkorDB instance; Qdrant to SSD-backed mode
  Phase 3     50--200 clients    32 → 64 GB / FalkorDB cluster mode            \~220 GB / second Beast node   Second Beast server; FalkorDB graph sharding (native)
  Phase 4     200+ clients       Clustered / cloud FalkorDB with replication   Multi-node distributed         Multiple Beasts or dedicated cloud FalkorDB; geographic replication
  ----------- ------------------ --------------------------------------------- ------------------------------ ---------------------------------------------------------------------

**Phase 1 (Current → 10 clients)**

This is the immediate operating window. The Beast has approximately 130 GB of uncommitted RAM --- sufficient to support 10 concurrent client graphs with generous margin. FalkorDB\'s memory footprint scales sub-linearly: each additional client graph adds approximately 200--500 MB depending on the richness of their knowledge graph. The primary action is monitoring and incremental FalkorDB allocation increases.

**Phase 2 (10--50 clients)**

At this scale, FalkorDB and Ollama begin competing for RAM. The recommended action is to isolate FalkorDB onto its own allocation with 32 GB and 16 threads, and move Qdrant\'s HNSW index to SSD-backed mode (trading slight latency for significant RAM recovery). Ollama model loading should be optimised to keep only the most-used models hot.

**Phase 3 (50--200 clients)**

A single Beast cannot sustain 200 concurrent client graphs at acceptable query latency. This phase introduces either a second Beast server (replicating the current Hetzner configuration at £600--700/month) or FalkorDB\'s native graph sharding across nodes. The decision point is whether graph queries are predominantly local (single-client) or cross-client (federated). For Amplified\'s architecture, most queries are local, making simple horizontal scaling the preferred approach.

**Phase 4 (200+ clients)**

At enterprise scale, the architecture transitions to a multi-node cluster with dedicated FalkorDB instances (potentially cloud-managed for operational simplicity), geographic replication for latency optimisation, and a dedicated inference cluster for LLM workloads. Cost modelling shifts from per-server to per-client-unit economics.

**1.4 Data Mitigation Strategies**

-   **Batch Ingestion:** All bulk data imports (vault documents, historical data) are processed via batch pipelines, never real-time streams. This prevents ingestion spikes from starving query performance.

-   **Graph Pruning:** Graphiti\'s temporal edge model enables intelligent pruning. Edges carry validity timestamps --- when new information supersedes old, the temporal edge is invalidated rather than deleted, preserving audit trail whilst reducing active traversal cost.

-   **Sparse Matrix Compression:** FalkorDB\'s underlying GraphBLAS engine uses sparse matrix representations for adjacency data. This is inherently efficient --- a graph with 100,000 nodes but sparse connections consumes far less memory than a dense matrix would suggest.

-   **Tiered Storage:** Hot graphs (actively queried clients) remain in RAM. Cold graphs (inactive clients, archived projects) are persisted to SSD and loaded on demand. FalkorDB supports this natively via its persistence layer.

**1.5 Cost Projections**

  -------------------------- --------------------- ------------------ ------------------ ------------------------------------------------
  **Cost Item**              **Current Monthly**   **Phase 2 Est.**   **Phase 3 Est.**   **Notes**
  Beast Server (Hetzner)     \~£600--700           \~£600--700        \~£1,200--1,400    Second server added at Phase 3
  FalkorDB Licence           £0                    £0                 £0                 Open-source --- no licence cost at any scale
  LLM API Calls (Graphiti)   \~£50--80             \~£200--400        \~£800--1,500      \~\$0.70--\$1.20 per full vault extraction run
  Qdrant                     £0                    £0                 £0                 Self-hosted open-source
  Monitoring + Backups       \~£30                 \~£50              \~£100             Prometheus, Grafana, off-site snapshots
  Total                      \~£680--810           \~£850--1,150      \~£2,100--3,000    Per-client cost decreases with scale
  -------------------------- --------------------- ------------------ ------------------ ------------------------------------------------

The critical insight: Amplified\'s infrastructure cost model has a fixed ceiling per Beast server (£600--700/month), with marginal costs driven almost entirely by LLM API calls for Graphiti extraction. This creates an inherently scalable cost structure --- per-client infrastructure cost decreases as client density on each server increases.

**PUDDING Label:** S.+.5.l (State, Amplifying, System-scale, Long-term)

**2. Amplified Process Maturity Score (AMPS) --- 0--10 Framework**

**2.1 Foundation: The Capability Maturity Model Integration (CMMI)**

The AMPS framework builds upon the Capability Maturity Model Integration (CMMI), developed by the Software Engineering Institute (SEI) at Carnegie Mellon University.[^2] CMMI provides a structured pathway for organisations to improve their processes across five maturity levels: Initial (Level 1), Managed (Level 2), Defined (Level 3), Quantitatively Managed (Level 4), and Optimizing (Level 5).[^3]

CMMI has been adopted globally across industries from defence to healthcare. However, its five-level structure --- whilst rigorous --- lacks the granularity required for Amplified\'s use case: scoring individual business processes within SMEs where the difference between \'Managed\' and \'Defined\' may span multiple distinct improvement opportunities.

AMPS adapts CMMI\'s principles into a ten-point scale that provides the resolution needed for actionable process improvement, particularly when combined with PUDDING cross-domain labelling and the DC-7 defrictioning cycle.

**2.2 The AMPS 0--10 Scale**

Each process within a client\'s business is scored against the following definitions. The scale is intentionally granular: the jump from 5 to 6, for instance, represents the shift from passive measurement to active analysis --- a critical inflection point in process maturity.

  ----------- ---------------- -------------------------------------------------------------------------------------------------------------------------------------- ------------------------
  **Score**   **Level Name**   **Definition**                                                                                                                         **CMMI Equivalent**
  0           Non-existent     The process has not been identified. The organisation does not recognise this as a distinct activity.                                  Below Level 1
  1           Chaotic          Completely ad hoc. Different people do it differently every time. No consistency, no documentation.                                    Level 1 (Initial)
  2           Reactive         The process exists but is triggered only by problems. Fire-fighting mode. Actions taken only when something breaks.                    Level 1 (Initial)
  3           Managed          Planned and tracked with basic controls. Someone owns it. Basic checklists or procedures exist.                                        Level 2 (Managed)
  4           Standardised     Documented, repeatable, and consistent. A new hire could follow the process from documentation alone.                                  Level 3 (Defined)
  5           Measured         KPIs are defined and data is actively collected. The organisation knows HOW the process performs, even if it doesn\'t act on it yet.   Level 4 (Quantitative)
  6           Analysed         Data is actively analysed, root causes of variation are understood, and improvement hypotheses are formed.                             Level 4 (Quantitative)
  7           Optimised        The process is continuously refined based on data. Waste has been identified and removed. Lean principles applied.                     Level 5 (Optimizing)
  8           Predictive       Outcomes are statistically predictable. Variation is quantified. The organisation can forecast process results.                        Level 5 (Optimizing)
  9           Adaptive         The process self-adjusts based on changing conditions. Proactive improvement without manual intervention.                              Beyond CMMI
  10          Generative       The process generates insights that improve OTHER processes. Compound learning territory --- PUDDING cross-domain connections.         Beyond CMMI
  ----------- ---------------- -------------------------------------------------------------------------------------------------------------------------------------- ------------------------

**2.3 Scoring Rubric: Six Weighted Dimensions**

A single AMPS score is not a subjective judgement. It is derived from six independently assessed dimensions, each contributing a weighted share to the final composite score. This ensures consistency across assessors and enables meaningful comparison between processes within and across client organisations.

  ---------------------- ------------ ------------------------------------------------------------------------------------- -------------------------------------------------------------------------------------------------
  **Dimension**          **Weight**   **Score 0--10 Criteria**                                                              **Example Indicators**
  Repeatability          20%          Can different people produce the same output following the same steps?                Standard operating procedures, consistent outputs, low person-dependency
  Documentation          15%          Is the process documented in sufficient detail for independent execution?             Written SOPs, video walkthroughs, decision trees, exception handling guides
  Measurability          20%          Are quantitative metrics defined and actively tracked?                                KPI dashboards, cycle time logs, error counts, throughput measurements
  Efficiency             15%          What is the ratio of value-adding steps to total steps? How much waste exists?        Process maps showing non-value-add steps, automation %, cycle time vs. value-add time
  Error Rate             15%          How frequently does the process produce incorrect, incomplete, or reworked outputs?   Defect logs, rework frequency, customer complaint rates, audit findings
  Improvement Velocity   15%          How quickly does the process improve when problems are identified?                    Time from issue identification to resolution, frequency of process updates, feedback loop speed
  ---------------------- ------------ ------------------------------------------------------------------------------------- -------------------------------------------------------------------------------------------------

**Calculating the Composite AMPS Score:**

AMPS = (Repeatability × 0.20) + (Documentation × 0.15) + (Measurability × 0.20) + (Efficiency × 0.15) + (Error Rate × 0.15) + (Improvement Velocity × 0.15)

Each dimension is scored individually on the 0--10 scale. The weighted sum produces the composite AMPS score, which is rounded to one decimal place.

**2.4 Integration with Existing Taxonomy**

AMPS does not operate in isolation. Each process within the Amplified system carries a full classification stack:

  ---------------------- ------------------------------------------ ----------------------------------------------------------------- ---------------------------------------------------
  **Layer**              **Classification**                         **Purpose**                                                       **Example**
  1\. APQC Category      1--13 (Process Classification Framework)   Locates the process within standard business taxonomy             Category 8: Manage Information Technology
  2\. PUDDING Label      Domain.Direction.Scale.Duration            Enables cross-domain pattern matching and compound learning       P.+.1.m (Process, Amplifying, Individual, Medium)
  3\. AMPS Score         0.0--10.0 (weighted composite)             Quantifies current maturity and identifies improvement headroom   6.2 --- Analysed, approaching Optimised
  4\. Bounded/Creative   B (Bounded) or C (Creative)                Determines automation eligibility                                 B --- Suitable for structured automation
  ---------------------- ------------------------------------------ ----------------------------------------------------------------- ---------------------------------------------------

This four-layer classification means any process can be precisely located, compared, and improved using a combination of domain-neutral patterns (PUDDING), quantitative maturity data (AMPS), and industry-standard categorisation (APQC).

**2.5 Worked Example: Client Invoice Processing**

**Process:** Generate and send client invoices for completed work.

**APQC Category:** 9 --- Manage Financial Resources

**PUDDING Label:** P.=.1.m (Process, Stable, Individual-scale, Medium-term)

**Bounded/Creative:** B (Bounded) --- fully structured, rule-based process

  ---------------------- ----------- -------------------------------------------------------------------------------
  **Dimension**          **Score**   **Rationale**
  Repeatability          4           Same steps followed but varies by who does it. Some invoices miss line items.
  Documentation          2           No written SOP. Knowledge held by one person. New staff struggle.
  Measurability          3           Invoice count tracked but not cycle time, error rate, or collection speed.
  Efficiency             3           Manual data entry from job sheets to accounting software. Double-handling.
  Error Rate             4           Occasional incorrect amounts or missing items. \~8% rework rate.
  Improvement Velocity   2           Problems known but not acted on. No feedback loop. Same issues recur.
  ---------------------- ----------- -------------------------------------------------------------------------------

**Composite AMPS Score:** (4 × 0.20) + (2 × 0.15) + (3 × 0.20) + (3 × 0.15) + (4 × 0.15) + (2 × 0.15) = 0.80 + 0.30 + 0.60 + 0.45 + 0.60 + 0.30 = 3.1

**Interpretation:** This process sits squarely in \'Managed\' territory --- it exists and is tracked, but lacks documentation, measurement infrastructure, and any improvement mechanism. Significant headroom for DC-7 intervention.

**PUDDING Label:** M.=.0.∞ (Meta, Stable, Scale-free, Timeless)

**3. The Defrictioning Cycle (DC-7) --- Decompose, Score, Research, Design, Test, Validate, Reassemble**

**3.1 Existing Improvement Frameworks: Comparative Analysis**

The field of process improvement has produced several mature frameworks, each with distinct strengths and limitations. Amplified\'s DC-7 is a synthesis --- not a replacement --- drawing the most effective elements from each into a unified cycle optimised for AI-augmented SME process transformation.

  ----------------------- ---------------------------------------------------------------------------------- --------------------------------------------------------- ---------------------------------------------------- -----------------------------
  **Framework**           **Steps**                                                                          **Strengths**                                             **Limitations**                                      **Source**
  PDCA (Deming Cycle)     Plan → Do → Check → Act                                                            Simple, universal, iterative                              No decomposition step; treats process as monolith    Deming Institute / Lean Way
  Toyota Kata (Rother)    4-step Improvement Kata                                                            Scientific thinking; small experiments; rapid iteration   Designed for manufacturing; no scoring mechanism     Mike Rother / Gemba Academy
  DMAIC (Six Sigma)       Define → Measure → Analyse → Improve → Control                                     Data-driven; rigorous statistical methods                 Heavy; requires Six Sigma expertise; slow for SMEs   Six Sigma Institute
  Kaizen 7-Step           Theme → Analysis → Root Cause → Countermeasure → Implement → Check → Standardise   Comprehensive; team-based; addresses root causes          Linear (not cyclical); no cross-domain learning      Toyota Production System
  BPR (Hammer & Champy)   Radical redesign of business processes                                             Transformative; questions fundamental assumptions         Disruptive; high risk; ignores incremental gains     Hammer & Champy (1993)
  ----------------------- ---------------------------------------------------------------------------------- --------------------------------------------------------- ---------------------------------------------------- -----------------------------

Sources: PDCA[^4]; Toyota Kata[^5]; BPR[^6]

**3.2 The DC-7 Framework: Amplified\'s Synthesis**

The DC-7 (Defrictioning Cycle --- 7 Steps) combines the decomposition discipline of BPR, the data rigour of DMAIC, the rapid experimentation of Toyota Kata, and the continuous improvement philosophy of PDCA. Critically, it adds two elements missing from all existing frameworks: AMPS scoring at the sub-process level, and PUDDING cross-domain pattern matching.

**3.2.1 The Seven Steps**

  ---------- ------------ -------------------------------------------------------------------------------------------------------------------------------------- -----------------------------------------------
  **Step**   **Name**     **Action**                                                                                                                             **Key Output**
  1          DECOMPOSE    Break the target process into atomic sub-processes. Each sub-process should be independently executable and scorable.                  Sub-process map with clear boundaries
  2          SCORE        Apply AMPS 0--10 scoring to each sub-process. Assign PUDDING label. Tag as Bounded or Creative.                                        Scored sub-process inventory
  3          RESEARCH     Triple search: (a) best-in-world alternatives, (b) success patterns from PUDDING-matched domains, (c) failure patterns to avoid.       Research dossier with candidate improvements
  4          DESIGN       Create improved sub-process design. Leverage PUDDING cross-domain insights. Apply automation where Bounded processes score ≤5.         Redesigned sub-process specification
  5          TEST         Small-scale experiment using Toyota Kata rapid PDCA cycles. Test the redesigned sub-process with a single client or single workflow.   Test results: performance data, user feedback
  6          VALIDATE     Compare before/after data quantitatively. Confirm AMPS score improvement. Check for negative side-effects on adjacent processes.       Validation report with statistical comparison
  7          REASSEMBLE   Integrate improved sub-processes back into the whole process. Re-score the complete process. Document lessons learned.                 Updated process with new composite AMPS score
  ---------- ------------ -------------------------------------------------------------------------------------------------------------------------------------- -----------------------------------------------

**3.2.2 The DC-7 Cycle --- Visual Representation**

*The DC-7 operates as a spiral, not a flat cycle. Each revolution raises the AMPS floor for the target process.*

┌─────────────────────────────────┐

│ 1. DECOMPOSE │

│ Break → atomic sub-processes │

└──────────┬──────────────────────┘

│

▼

┌──────────────────┐ ┌──────────────────┐

│ 7. REASSEMBLE │ │ 2. SCORE │

│ Integrate + │ │ AMPS + PUDDING │

│ re-score whole │ │ + Bounded/Creat. │

└───────┬──────────┘ └──────┬───────────┘

│ │

▲ ▼

┌───────┴──────────┐ ┌──────┴───────────┐

│ 6. VALIDATE │ │ 3. RESEARCH │

│ Before/after │ │ Triple search: │

│ data comparison │ │ best + fail + │

│ │ │ PUDDING bridges │

└───────┬──────────┘ └──────┬───────────┘

│ │

▲ ▼

┌───────┴──────────┐ ┌──────┴───────────┐

│ 5. TEST │ │ 4. DESIGN │

│ Small-scale │ │ Improved sub- │

│ experiment │ │ process spec │

└──────────────────┘ └──────────────────┘

*Each completed cycle feeds back into Step 1: the reassembled process can itself be decomposed at higher resolution for the next iteration. AMPS scores compound upward; PUDDING connections accumulate cross-domain intelligence.*

**3.3 The Compound Learning Loop**

The DC-7\'s distinguishing characteristic is not any individual step --- every framework has some version of plan-execute-review. The breakthrough is the compound learning loop that emerges when DC-7 is combined with AMPS scoring and PUDDING labelling across multiple clients and domains:

1.  **Score Delta Capture:** Each DC-7 cycle produces a measurable AMPS score change (e.g., invoice processing moved from 3.1 to 6.4). This delta is recorded alongside the specific interventions that produced it.

2.  **PUDDING Pattern Indexing:** The improvement pattern is tagged with the sub-process\'s PUDDING label. A scheduling improvement (P.\~.1.m) is indexed as a reusable pattern for any process sharing that label.

3.  **Cross-Domain Bridge Formation:** When a DC-7 cycle succeeds in one domain (e.g., plumbing), the PUDDING label match surfaces structurally equivalent processes in other domains (e.g., restaurant table booking) as improvement candidates.

4.  **Hypothesis Generation:** Each bridge becomes a testable hypothesis: \'Intervention X raised AMPS by 3.3 for Process A; Process B has the same PUDDING label and a lower AMPS score; Intervention X is a candidate for Process B.\'

5.  **Ceiling Elevation:** Each validated cross-domain improvement raises the achievable AMPS ceiling for all structurally similar processes. This is Ewan\'s \'5+5=13\' principle operating at the process level.

This is the operationalisation of Ewan\'s vision: **\'take it down small, take it up big.\'** The DC-7 takes processes down to their atomic components (small), improves each component with data and cross-domain intelligence, then reassembles them into something greater than the sum of parts (big).

**3.4 DC-7 Mapping to Cove Teams**

The three Cove teams --- Code, Content, and Process --- each run DC-7 cycles within their domain of expertise:

  --------------- ------------------------------------------------- -------------------------------------------------------------------------------------------- ----------------------------
  **Cove Team**   **DC-7 Target Domain**                            **Example Processes**                                                                        **Typical Cycle Duration**
  Code Team       Software development + technical infrastructure   API endpoint design, deployment pipeline, testing workflow, database queries                 1--2 weeks per cycle
  Content Team    Knowledge creation + communication                Blog post workflow, client report generation, documentation updates, social media pipeline   3--5 days per cycle
  Process Team    Business operations + client-facing processes     Client onboarding, invoice processing, scheduling, supply chain steps                        1--4 weeks per cycle
  --------------- ------------------------------------------------- -------------------------------------------------------------------------------------------- ----------------------------

All three teams share the same DC-7 methodology, the same AMPS scoring system, and the same PUDDING labelling taxonomy. This means improvements discovered by the Code Team can --- through PUDDING bridges --- inform improvements in Content or Process domains. The compound learning loop operates across teams, not just within them.

**PUDDING Label:** P.+.0.l (Process, Amplifying, Scale-free, Long-term)

**4. Client Business Defrictioning & Supportive Staff Redistribution**

**4.1 The Ethical Foundation**

Amplified Partners operates under an explicit ethical commitment: AI augments human capability; it does not displace human workers. This is not merely a brand position --- it is a structural design constraint that shapes every technical and strategic decision. The MIT Sloan research on automation ethics provides a useful framework:[^7]

  ----------- ---------------------- --------------------------------------------------------------------------------------- ------------------------------------
  **Level**   **Orientation**        **Description**                                                                         **Amplified Position**
  Level 0     Cost-Focused           Automate to reduce headcount. Measure success by labour cost reduction.                 REJECT --- violates core values
  Level 1     Performance-Driven     Automate to improve throughput. Workers retained but not actively supported.            Below minimum standard
  Level 2     Worker-Centred         Automate to free workers for higher-value roles. Active reskilling and role redesign.   TARGET --- primary operating level
  Level 3     Socially Responsible   Consider broader community impact. Support displaced workers across the ecosystem.      ASPIRATION --- long-term goal
  ----------- ---------------------- --------------------------------------------------------------------------------------- ------------------------------------

**Amplified operates at Level 2--3.** The guiding principle is: \'Their business. Their smell. Their signature.\' AI enhances the business\'s distinctive character --- it doesn\'t homogenise it. Every client\'s business retains its unique identity, with staff empowered to do more of what makes the business special.

**4.2 The Evidence Base for Redistribution Over Reduction**

**4.2.1 S&P Global: Task Redistribution, Not Job Elimination**

S&P Global\'s research on generative AI and the workforce concludes that AI reshapes work through task redistribution, not wholesale job reduction.[^8] This finding is particularly relevant for SMEs, where employees typically perform multi-functional roles. A bookkeeper who also handles customer queries and manages supplier relationships cannot be \'replaced\' by an AI system --- but their data entry burden (2--3 hours daily) can be eliminated, freeing that time for the relationship-building and strategic thinking that creates genuine business value.

**4.2.2 Forbes: The Human-AI Collaboration Matrix**

Forbes\' Human-AI Collaboration framework maps tasks along two dimensions: complexity and human touch advantage.[^9] Tasks with low complexity and low human-touch advantage (data entry, scheduling, filing) are prime automation candidates. Tasks with high complexity and high human-touch advantage (client relationships, creative problem-solving, negotiation) are amplification candidates --- where AI provides data and insights that make human performance dramatically better.

  ----------------- ---------------------------------------------------------- ----------------------------------------------------------------
                    **Low Human Touch Advantage**                              **High Human Touch Advantage**
  High Complexity   AI-Assisted Decision Making (AI analyses, human decides)   Human-Led with AI Augmentation (relationship + AI insights)
  Low Complexity    Full Automation Candidate (AI handles end-to-end)          Streamlined by AI (AI reduces friction, human maintains touch)
  ----------------- ---------------------------------------------------------- ----------------------------------------------------------------

**4.2.3 Workforce Redeployment ROI**

Research on workforce redeployment demonstrates measurable returns: preserved institutional knowledge reduces onboarding costs by 40--60%, internal redeployment achieves faster time-to-productivity than external hiring (3--4 months vs. 6--9 months), and retention rates improve by 20--30% when staff see investment in their development rather than threat to their roles.[^10]

**4.3 The Client Defrictioning Cascade --- 9 Steps**

The following cascade is applied to every client engagement. It integrates AMPS scoring, PUDDING labelling, and the DC-7 cycle into a structured transformation programme that begins with mapping and ends with measurable improvement across business metrics, staff satisfaction, and client satisfaction.

1.  **Map All Processes:** Using the APQC Process Classification Framework (13 categories), conduct a comprehensive process inventory. Every identifiable business activity is catalogued --- from core operations to supporting activities.

2.  **Score Each Process (AMPS 0--10):** Apply the six-dimension AMPS scoring rubric to every process. This creates a quantitative baseline from which all improvement can be measured.

3.  **Apply PUDDING Labels:** Each process receives its PUDDING classification (Domain.Direction.Scale.Duration). This enables cross-domain pattern matching and compound learning from other client engagements.

4.  **Identify Friction Points:** Processes scoring ≤5 on AMPS are flagged as friction points --- processes where significant improvement headroom exists and intervention will yield the highest return.

5.  **Run DC-7 Cycle:** Each friction point enters the DC-7 cycle: Decompose → Score → Research → Design → Test → Validate → Reassemble. The cycle continues until the target AMPS score is achieved or diminishing returns are identified.

6.  **Identify Human Time Freed:** For each automated or improved sub-process, quantify the human hours previously consumed. This is not a cost saving --- it is a capacity creation metric.

7.  **Map Freed Time to Value-Add Roles:** Working WITH the client\'s staff, identify higher-value activities where the freed time can be redirected. The staff member\'s expertise, interests, and the business\'s strategic needs all inform this mapping.

8.  **Create Personal Development Plans:** Each affected staff member receives a personal development plan: new role definition, required training (delivered BEFORE the transition), coaching support, and success metrics.

9.  **Measure Outcomes (Triple Metric):** Success is measured on three dimensions simultaneously: staff satisfaction (surveys, retention), business metrics (revenue, efficiency, error rates), and client satisfaction (NPS, repeat business). All three must improve or the intervention is reconsidered.

**4.4 Value Redistribution Table**

The following table illustrates typical redistribution patterns observed in SME contexts. Note that the \'Human Redirected To\' column consistently represents higher-value, more engaging work --- this is the core promise of the supportive staff redistribution model.

  --------------------------------------------- -------------------------------------------------------------- -------------------------- ----------------------------------------------
  **AI Takes Over**                             **Human Redirected To**                                        **Estimated Time Freed**   **Value Impact**
  Data entry, filing, document management       Client relationship building, personalised service             8--12 hours/week           Revenue growth via deeper client engagement
  Invoice processing, reconciliation            Financial strategy, cash flow planning, pricing optimisation   4--6 hours/week            Improved margins, better financial decisions
  Appointment booking, reminders, scheduling    Upselling, cross-selling, service quality improvement          3--5 hours/week            Higher average transaction value
  Report generation, compliance documentation   Insight interpretation, strategic decision-making              5--8 hours/week            Better decisions, faster market response
  Inventory counting, stock level monitoring    Supplier negotiation, quality control, product curation        4--6 hours/week            Cost reduction, quality improvement
  Email triage, standard responses, FAQs        Complex query resolution, relationship management              6--10 hours/week           Customer satisfaction, loyalty, referrals
  --------------------------------------------- -------------------------------------------------------------- -------------------------- ----------------------------------------------

**4.5 Supportive Implementation Protocol --- 6 Rules**

Every client defrictioning engagement adheres to these six inviolable rules. They are not guidelines --- they are hard constraints that override efficiency considerations.

  ---------- ------------------------------------------------------------------------------- ------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------
  **Rule**   **Principle**                                                                   **Implementation**
  1          Never \'AI is replacing your task\' --- always \'We\'re upgrading your role\'   All communication is framed around role enhancement. Staff are told what they\'re moving TO, not what they\'re losing. Language matters: \'freed from\' not \'replaced by\'.
  2          Training BEFORE transition, not after                                           Staff receive full training on their new responsibilities BEFORE any automation goes live. Competence precedes change. No one is left unprepared.
  3          Staff involved in DESIGN phase of DC-7                                          The people who currently perform the process are participants in Step 4 (Design) of the DC-7 cycle. Their expertise is essential --- they know the edge cases, the workarounds, the human elements.
  4          Metrics include staff wellbeing                                                 Every engagement tracks staff satisfaction alongside business metrics. If staff satisfaction drops, the implementation is paused and the approach is revised.
  5          90-day transition with coaching                                                 No abrupt changes. Every role transition includes a 90-day structured transition period with weekly coaching check-ins, progress reviews, and adjustment opportunities.
  6          Win-Win Test (Layer 0 Law \#4)                                                  Every intervention must pass the Win-Win test from Layer 0. If the improvement benefits the business but harms staff, it fails. If it benefits staff but harms the business, it also fails. Both must win.
  ---------- ------------------------------------------------------------------------------- ------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------

**PUDDING Label:** R.+.4.l (Relation, Amplifying, Network-scale, Long-term)

**5. PUDDING Compound Learning Integration**

**5.1 How PUDDING Connects All Sections**

The preceding four sections --- Data Growth (Section 1), AMPS Scoring (Section 2), DC-7 Defrictioning (Section 3), and Staff Redistribution (Section 4) --- are not independent strategy components. They are interconnected by the PUDDING labelling system, which provides the connective tissue enabling compound learning across domains, clients, and time.

  -------------------------- --------------------------------------------------------------------------------- --------------------------------------------------------------------------------
  **Section**                **PUDDING Role**                                                                  **Cross-Connection**
  1\. Data Growth            PUDDING labels stored as graph metadata in FalkorDB per-client namespaces         Labels enable federated queries across graphs without exposing raw client data
  2\. AMPS Scoring           Every scored process receives a PUDDING label alongside its AMPS composite        PUDDING label + AMPS score = searchable improvement pattern
  3\. DC-7 Cycle             Steps 2 (Score) and 3 (Research) use PUDDING for cross-domain pattern discovery   DC-7 improvements tagged with PUDDING labels become reusable templates
  4\. Staff Redistribution   Value redistribution patterns tagged with PUDDING enable cross-client learning    Successful role transitions in one domain inform approaches in matched domains
  -------------------------- --------------------------------------------------------------------------------- --------------------------------------------------------------------------------

**5.2 The Compound Learning Engine**

The compound learning engine is the mechanism by which Amplified\'s platform becomes exponentially more valuable with each client engagement. Unlike traditional consulting (where knowledge is locked in individual consultants\' heads), the compound learning engine captures, abstracts, and redistributes improvement patterns systematically.

**5.2.1 The Engine\'s Five-Stage Pipeline**

1.  **DC-7 Produces Scored Processes with PUDDING Labels:** Every completed DC-7 cycle outputs a set of sub-processes, each carrying an AMPS before-score, AMPS after-score, and PUDDING label. These are stored in the client\'s knowledge graph (kg\_{client\_id}).

2.  **PUDDING Label Matching Across Domains:** The system identifies processes across different clients that share the same PUDDING label. A plumber\'s \'appointment scheduling\' (P.\~.1.m) and a restaurant\'s \'table booking\' (P.\~.1.m) are structurally equivalent despite surface-level domain differences.

3.  **Bridge Formation:** When a process in Domain A has been improved (AMPS score increased) and a structurally matched process in Domain B has a lower AMPS score, a \'bridge\' is formed. This bridge is a hypothesis: the improvement pattern from A is a candidate for B.

4.  **Hypothesis Testing via DC-7:** The bridge hypothesis is tested by running a DC-7 cycle on Process B, using the improvement pattern from Process A as the starting point for Step 3 (Research) and Step 4 (Design). This dramatically accelerates the cycle.

5.  **AMPS Ceiling Elevation:** Each validated bridge raises the achievable AMPS ceiling for all processes sharing that PUDDING label. The platform\'s collective intelligence grows with every engagement. This is \'5+5=13\' at scale.

**5.3 Privacy Safeguard: Domain-Neutral Learning**

A critical design constraint: cross-client learning must never expose raw client data. The PUDDING system achieves this through structural abstraction:

-   **Labels Are Domain-Neutral:** \'P.\~.1.m\' contains no information about plumbing, restaurants, or any specific business. It describes process structure: Process type, Oscillating direction, Individual scale, Medium duration.

-   **AMPS Scores Are Numeric Abstractions:** A score of 3.1 → 6.4 tells the system that a significant improvement occurred, and what dimensional changes drove it (e.g., Documentation +4, Measurability +3). No client-specific content is transmitted.

-   **The kg\_federated Graph (Tier 3):** The federated knowledge graph holds only anonymised aggregates: PUDDING labels, AMPS score distributions, improvement pattern templates, and success/failure rates. No client names, no specific processes, no raw data.

-   **Isolation by Design:** Each client\'s data lives in its own kg\_{client\_id} namespace. Cross-client queries operate only on the kg\_federated aggregate layer. Even Amplified\'s own team cannot inadvertently access raw cross-client data through the compound learning pipeline.

**5.4 Example PUDDING Bridge**

**Scenario:** Demonstrating cross-domain compound learning in practice.

  ------------------- ------------------------------------------------------ ------------------------------------------------
  **Attribute**       **Process A (Plumber)**                                **Process B (Restaurant)**
  Process Name        Appointment Scheduling                                 Table Booking
  PUDDING Label       P.\~.1.m                                               P.\~.1.m
  AMPS Before DC-7    3.0                                                    2.0
  Key Friction        Manual phone booking, no reminders, 30% no-show rate   Paper diary, no confirmation, 25% no-show rate
  DC-7 Intervention   Automated booking + SMS reminders + calendar sync      ---
  AMPS After DC-7     7.2                                                    ---
  AMPS Delta          +4.2                                                   ---
  ------------------- ------------------------------------------------------ ------------------------------------------------

**Bridge Hypothesis:** Process B shares PUDDING label P.\~.1.m with Process A. Process A\'s AMPS increased by 4.2 points through automated booking, SMS reminders, and calendar synchronisation. Process B exhibits structurally identical friction patterns (manual booking, no reminders, high no-show rate). The hypothesis: applying the same intervention pattern to Process B will yield a comparable AMPS improvement.

**Predicted Outcome:** Process B AMPS moves from 2.0 to approximately 5.5--6.5, accounting for domain-specific variation. The DC-7 cycle for Process B begins at Step 4 (Design) rather than Step 3 (Research), because the research has already been validated in a structurally equivalent context. Estimated cycle time: 40--60% faster than a cold-start DC-7.

This is the compound effect in action. Every client engagement makes the next engagement faster, more accurate, and more valuable. The platform\'s intelligence grows exponentially whilst client data remains strictly isolated. This is the \'Generative\' level (AMPS 10) --- where one process\'s improvement generates improvements in other processes across domains.

**PUDDING Label:** M.+.0.∞ (Meta, Amplifying, Scale-free, Timeless)

**Appendix A: AMPS Scoring Worksheet**

*Use this template to score a single business process. Complete one worksheet per process.*

  ---------------------------- -----------
  **Field**                    **Value**
  Process Name                 
  APQC Category (1--13)        
  PUDDING Label                
  Bounded (B) / Creative (C)   
  Date of Assessment           
  Assessed By                  
  ---------------------------- -----------

**Dimension Scores (0--10 each):**

  ---------------------- ------------ ------------------- --------------------
  **Dimension**          **Weight**   **Score (0--10)**   **Weighted Score**
  Repeatability          20%                              
  Documentation          15%                              
  Measurability          20%                              
  Efficiency             15%                              
  Error Rate             15%                              
  Improvement Velocity   15%                              
  COMPOSITE AMPS SCORE   100%         ---                 
  ---------------------- ------------ ------------------- --------------------

  -------------------------------------------- -----------
  **Field**                                    **Value**
  Improvement Priority (High / Medium / Low)   
  Target AMPS Score (post DC-7)                
  Estimated DC-7 Cycles Required               
  Key Friction Points Identified               
  Notes / Observations                         
  -------------------------------------------- -----------

**Appendix B: DC-7 Cycle Template**

*Use this template to plan and execute a single DC-7 defrictioning cycle. Complete one template per process intervention.*

  -------------------------------------- -----------
  **Field**                              **Value**
  Target Process Name                    
  Current Composite AMPS Score           
  Target AMPS Score                      
  PUDDING Label                          
  APQC Category                          
  DC-7 Cycle Number (for this process)   
  Date Started                           
  Responsible Cove Team                  
  -------------------------------------- -----------

**Step 1 --- DECOMPOSE**

  -------------------- ---------------------- ----------------- -------------------
  **Sub-Process ID**   **Sub-Process Name**   **Description**   **Current Owner**
  SP-01                                                         
  SP-02                                                         
  SP-03                                                         
  SP-04                                                         
  SP-05                                                         
  -------------------- ---------------------- ----------------- -------------------

**Step 2 --- SCORE (per sub-process)**

  -------------------- ---------------- ------------------- ----------------------
  **Sub-Process ID**   **AMPS Score**   **PUDDING Label**   **Bounded/Creative**
  SP-01                                                     
  SP-02                                                     
  SP-03                                                     
  SP-04                                                     
  SP-05                                                     
  -------------------- ---------------- ------------------- ----------------------

**Step 3 --- RESEARCH Findings**

  ------------------------------------ -------------- ------------
  **Research Area**                    **Findings**   **Source**
  Best-in-world alternatives                          
  Success patterns (PUDDING matches)                  
  Failure patterns to avoid                           
  ------------------------------------ -------------- ------------

**Step 4 --- DESIGN Decisions**

  -------------------- --------------------- ---------------------- --------------------------
  **Sub-Process ID**   **Proposed Change**   **Automation (Y/N)**   **PUDDING Insight Used**
  SP-01                                                             
  SP-02                                                             
  SP-03                                                             
  -------------------- --------------------- ---------------------- --------------------------

**Step 5 --- TEST Plan**

  ---------------------------------- -----------
  **Field**                          **Value**
  Test Scope (which sub-processes)   
  Test Duration                      
  Success Criteria                   
  Participants                       
  ---------------------------------- -----------

**Step 6 --- VALIDATE Results**

  ---------------------- ------------ ----------- -----------
  **Metric**             **Before**   **After**   **Delta**
  Composite AMPS Score                            
  Cycle Time                                      
  Error Rate                                      
  Staff Satisfaction                              
  Client Impact                                   
  ---------------------- ------------ ----------- -----------

**Step 7 --- REASSEMBLE**

  --------------------------------- -----------
  **Field**                         **Value**
  Reassembled Process Description   
  New Composite AMPS Score          
  AMPS Delta (whole process)        
  Lessons Learned                   
  PUDDING Bridges Created           
  Date Completed                    
  --------------------------------- -----------

[^1]: FalkorDB, Multi-Tenant Architecture, <https://www.falkordb.com/blog/graph-database-multi-tenant-cloud-security/>

[^2]: 6Sigma, Capability Maturity Model Integration, <https://www.6sigma.us/process-improvement/capability-maturity-model-integration-cmmi/>

[^3]: Wikipedia, Capability Maturity Model Integration, <https://en.wikipedia.org/wiki/Capability_Maturity_Model_Integration>

[^4]: The Lean Way, The Continuous Improvement Cycle (PDCA), <https://theleanway.net/the-continuous-improvement-cycle-pdca>

[^5]: Gemba Academy, Toyota Kata (Improvement Kata), <https://www.gembaacademy.com/resources/gemba-glossary/kata>

[^6]: California Department of Technology, Business Process Reengineering, <https://projectresources.cdt.ca.gov/wp-content/uploads/sites/50/2019/09/CA-BPR.pdf>

[^7]: MIT Sloan, Ethics and Automation: What to Do When Workers are Displaced, <https://mitsloan.mit.edu/ideas-made-to-matter/ethics-and-automation-what-to-do-when-workers-are-displaced>

[^8]: S&P Global, Generative AI and Workforce: More Redistribution Than Reduction, <https://www.spglobal.com/en/research-insights/special-reports/generative-ai-workforce-more-redistribution-than-reduction>

[^9]: Forbes, The Human-AI Playbook: Moving Beyond Automation to True Collaboration, <https://www.forbes.com/sites/brentdykes/2025/03/10/the-human-ai-playbook-moving-beyond-automation-to-true-collaboration/>

[^10]: Careerminds, ROI of Workforce Redeployment, <https://careerminds.com/blog/roi-workforce-redeployment>

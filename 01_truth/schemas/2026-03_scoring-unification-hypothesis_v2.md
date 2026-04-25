---
title: "Scoring Unification Hypothesis v2"
id: "scoring-unification-hypothesis-v2"
version: 1
created: 2026-04-25
last_validated: 2026-04-25
type: document
topic_type: reference
status: imported
source_file: "SCORING-UNIFICATION-HYPOTHESIS-v2.md"
signed_by: "Devon, 2026-04-25, devin-992682c244cf444f91e0a516498afbfd"
---

# Amplified Partners — Code-Based Scoring Unification Hypothesis v2

---

**Document ID:** `SCORING-UNIFICATION-HYPOTHESIS-v2`  
**Status:** Hypothesis — Under Investigation  
**Evidence Grade:** Mixed-to-Strong (see per-claim grading below)  
**Applies to:** All Amplified Partners systems, pipelines, agents, and data stores  
**Companion documents:** `ATTRIBUTION-AND-CURATION-v1`, `VALIDATION-METHODOLOGY-v2`, `CODE-TAXONOMY-AND-KAIZEN-v1`  
**Dependencies:** This hypothesis depends on the compressed coding system defined in `ATTRIBUTION-AND-CURATION-v1` Section 3  

---

## 0. THE HYPOTHESIS

> Once every data object in the system carries compressed codes, those codes become countable. Countable codes become scorable. Scorable codes become a unified measurement system that bridges taxonomy, quality evaluation, and retrieval into a single mechanism. Furthermore, the rubrics that score outputs can themselves be scored for effectiveness, and those rubric scores can adapt based on the lens (the problem context), creating a self-improving evaluation system where mathematics decides at every level.

We are not the first to think about this. We are standing on the shoulders of giants — medical informaticians who built SNOMED CT, IBM engineers who measured software reuse, researchers who scored knowledge graphs by access frequency, and the teams behind OpenRS who proved that rubrics can be meta-scored and refined. What we are proposing is that these proven pieces, combined in a single architecture around compressed codes, create a flywheel that has not been built before.

This hypothesis has three parts:

1. **Codes as scores** — Code usage metrics (frequency, co-occurrence, decay, gate pass rates) create a universal scoring layer.
2. **Rubric meta-scoring** — The rubrics themselves can be scored for effectiveness and improved systematically.
3. **Lens-adaptive evaluation** — Scoring criteria should change based on the problem being solved, not just the subject.

Each part has independent evidence. The integration of all three is the novel claim. We're not that clever — most of this is proven elsewhere. The clever bit, if there is one, is connecting the pieces through a shared mechanism: the compressed code.

This document presents the evidence honestly. Where the evidence is strong, we say so. Where it is thin, we say that too. Where the claim is purely hypothetical, we grade it as such. Mathematics decides — but only when we have the mathematics. Until then, we investigate.

---

## 1. CODES AS A SCORING LAYER

**Evidence Grade: STRONG — Multiple independent confirmations from different domains**

The claim is straightforward: if every data object carries compressed codes, and those codes are tracked over time, the usage patterns of the codes themselves become a rich scoring layer. This is not speculation. It is proven practice in at least four independent domains.

### 1.1 Medical Informatics — SNOMED CT

SNOMED CT is the most battle-tested coded system in the world. Over 370,000 clinical concepts, each assigned a unique code, used across healthcare systems in more than 40 countries. The codes are not decorative. They are the foundation of clinical quality measurement.

SNOMED CT codes are routinely used for quality metrics: code frequency tracks disease prevalence, code co-occurrence identifies comorbidity patterns, and code coverage measures documentation quality. SNOMED International explicitly states that coded clinical data enables "early identification of emerging health issues, monitoring of population health" and "accurate access to relevant information, reducing costly duplications and errors." ([SNOMED International — Value of SNOMED CT](https://www.snomed.org/value-of-snomedct))

The codes are not just useful — their quality is critical. A 2024 study published in the *Journal of the American Medical Informatics Association* (JAMIA) quantitatively assessed the impact of code quality on system performance. The researchers found that missing is-a relations in the SNOMED CT hierarchy significantly reduced micro-averaged and macro-averaged recall of cohort queries (P < .001, Wilcoxon signed-rank tests). Inaccurate is-a relations significantly reduced micro-averaged and macro-averaged precision (P < .001). The study evaluated both direct impacts on superconcepts and indirect impacts propagated through ancestors, using the Optum COVID-19 EHR dataset with OHDSI mappings. ([Hao et al., 2024 — "Quantitatively assessing the impact of the quality of SNOMED CT subtype hierarchy on cohort queries," JAMIA](https://pmc.ncbi.nlm.nih.gov/articles/PMC11648736/))

**The lesson for Amplified:** Code quality directly determines system quality. If our codes have incorrect hierarchical relationships, downstream queries will fail — just as they do in healthcare. This is not theoretical. It is measured. It is quantified. It is published.

### 1.2 IBM Software Reuse Metrics

IBM's work on reusable software libraries in the early 1990s produced three metrics computed directly from code usage data:

- **Reuse Percent** — The level of reuse activity in an organisation, expressed as a percentage of total effort. Computed from how frequently catalogued components are retrieved and integrated.
- **Reuse Cost Avoidance (RCA)** — The financial benefit of reuse, combining the level of reuse on a project with historical development and service costs to estimate what was not spent because existing components were reused.
- **Reuse Value Added (RVA)** — A productivity index that credits both using existing components and creating reusable ones. A value of 1.0 means no participation in reuse; 1.5 means a 50% increase in effective productivity.

These metrics were derived from faceted classification codes — structured descriptors attached to each software component in the library. The classification enabled retrieval; the retrieval patterns enabled measurement; the measurements justified continued investment. ([Poulin, J.S. — "Reuse Metrics at IBM," Ada Letters](http://jeffreypoulin.info/Papers/Ada_letters/ada_letters.html))

IBM's faceted classification system for reusable software is documented in the 1993 COMPSAC paper on applying the approach to their Reusable Software Library. The faceted codes served dual purposes: enabling developers to find components and enabling managers to measure the economic value of the library through the three metrics above.

**The lesson for Amplified:** Faceted codes attached to knowledge assets can generate economic metrics — not just retrieval. The same codes that enable finding also enable measuring. This is exactly what we propose: the compressed codes that enable retrieval also enable scoring.

### 1.3 Knowledge Graph Quality Assessment

A 2024 study published in *Scientific Reports* (Nature) proposed a novel approach to knowledge graph accuracy assessment based on entity popularity — the frequency with which entities are accessed or queried. Their method, EP-TWCS (Entity Popularity-weighted Two-stage Weighted Cluster Sampling), uses access frequency as a proxy for entity importance, prioritising assessment of the entities that matter most to users.

The method segments a knowledge graph into entity clusters, computes popularity weights from query logs, and samples high-popularity clusters first. Per-cluster accuracy is computed and aggregated into a weighted average with confidence intervals. The approach was validated against three knowledge graphs:

| Knowledge Graph | True Accuracy | Predicted Accuracy | Deviation |
|----------------|---------------|-------------------|-----------|
| NELL (sports domain) | 91.3% (full) / 95.5% (sampled) | 95.5% | ~0% |
| YAGO (general) | 99.0% (full) / 96.7% (sampled) | 96.8% | 0.08% |
| MOVIE (movies) | 90.0% (full) / 88.9% (sampled) | ~88.9% | ~0% |

The predicted accuracy converged to true values at a critical sample size, with an L-shaped bias curve showing rapid stabilisation. The method required substantially fewer samples than baselines (SRS, RCS, WCS, TWCS). ([Zhang & Xiao, 2024 — "A novel customizing knowledge graph evaluation method for incorporating user needs," Scientific Reports](https://www.nature.com/articles/s41598-024-60004-x))

**The lesson for Amplified:** Access frequency is already used as a quality signal in knowledge graphs. Entities that are queried more often are prioritised for quality assessment. This is a direct parallel to our proposal: codes that appear frequently deserve more attention, and their frequency itself is a meaningful metric.

### 1.4 Enterprise Knowledge Retrieval

Enterprise Knowledge's 2026 work on optimising historical knowledge retrieval for a federally funded research and development centre demonstrates the full pipeline from taxonomy to scoring in a production system. Their approach used a semantic NLP classification service for concept extraction and classification at scale, employing linguistic analysis and taxonomic rules configurable per domain, concept scheme, or input field.

Each auto-tag was paired with "persistent identifiers for tagged concepts" in the Taxonomy Management System. Metadata fields that once held free-text values were "standardised to a preferred label, with reference to the defined concept in the source taxonomy." Through iterative experimentation, classifier configurations were optimised to "prioritise the most significant signals when scoring concepts for each domain, delivering high-precision, context-aware results." ([Enterprise Knowledge — "Optimizing Historical Knowledge Retrieval"](https://enterprise-knowledge.com/optimizing-historical-knowledge-retrieval/))

**The lesson for Amplified:** Persistent identifiers (codes) enable classifier tuning. Classifier tuning is measurement. Measurement enables improvement. This is the codes-to-scoring pathway operating in a production enterprise knowledge system, published in 2026.

### 1.5 What This Means for Amplified

Every code in the Amplified system is already being tracked by the Curators. Creation date, creating agent, write count — all recorded in audit logs. The scoring layer is **latent** in the existing data. It does not require new infrastructure. It requires Kaizen to extract and report the metrics.

The specific metrics that codes enable:

| Metric | Definition | Signal |
|--------|-----------|--------|
| **Reuse frequency** | How many nodes/documents carry this code? | High reuse = core concept. Low reuse = niche or stale. |
| **Co-occurrence matrix** | Which codes appear together on the same nodes? | Reveals structural relationships between concepts. |
| **Decay rate** | When was this code last applied to a new node? | Stale codes = stale knowledge. Active codes = living domains. |
| **Gate pass rate per code** | Do nodes tagged with certain codes fail validation more often? | Quality signal per domain. |
| **Attribution depth per code** | Do some domains have deeper provenance chains than others? | Confidence signal — deeper attribution = higher trust. |
| **Cross-domain bridge score** | Codes appearing in unexpected domain combinations. | These are the Pudding technique's gold — surprising connections that reveal hidden relationships. |
| **Code velocity** | Rate of new code creation in a domain over time. | Accelerating = growing knowledge area. Decelerating = mature or neglected domain. |

None of these metrics require new data collection. They are all computable from the existing Curator audit logs and the code assignments already being made. The scoring layer is there. We just need to read it.

### 1.6 Metric Interactions — Where the Real Power Lives

The individual metrics above are useful. The interactions between them are transformative.

**Frequency × Decay:** A code with high historical frequency but recent decay is a signal of a concept that was once central but is becoming stale. In SNOMED CT, this pattern identifies clinical concepts where new evidence has superseded old understanding. In our system, it identifies knowledge areas that need refreshing.

**Co-occurrence × Gate Pass Rate:** If two codes frequently co-occur on nodes that fail gates, the combination itself may indicate a problematic pattern — perhaps a knowledge domain where our quality standards are poorly calibrated, or where the source material is inherently less reliable.

**Velocity × Attribution Depth:** A domain with high code velocity (many new codes being created) but shallow attribution depth (few provenance chains) is growing fast but without rigorous sourcing. This is an early warning system for knowledge areas that are expanding beyond their evidence base.

**Bridge Score × Reuse Frequency:** Cross-domain codes that also have high reuse frequency are the system's most valuable connective tissue. They are the concepts that link domains and get used repeatedly. These are strategic assets — and their quality should be prioritised accordingly.

These interaction patterns are not hypothetical. Medical informatics routinely uses exactly these kinds of multi-metric analyses. The difference is that we would compute them automatically and continuously, rather than through periodic manual studies.

### 1.7 Mathematical Sketch of the Scoring Layer

To make the metrics precise enough for implementation, here is a preliminary mathematical formalisation. These are starting points, not final specifications — the validation plan will determine which formulations are most useful.

**Reuse frequency** for code `c` at time `t`:

    RF(c, t) = count of nodes n where c ∈ codes(n) and created(n) ≤ t

Simply: count all nodes carrying code `c` created up to time `t`.

**Normalised reuse** (to compare across domains of different sizes):

    NRF(c, t) = RF(c, t) / count of nodes n where domain(n) = domain(c)

**Decay rate** as time since last assignment:

    Decay(c, t) = t - max(created(n) for all n where c ∈ codes(n))

**Co-occurrence strength** between codes `c_i` and `c_j` (Jaccard similarity):

    CoOcc(c_i, c_j) = |nodes carrying both| / |nodes carrying either|

**Gate pass rate** for code `c` at gate `g`:

    GPR(c, g) = |nodes with c that pass g| / |nodes with c evaluated at g|

**Bridge score** for a code pair `(c_i, c_j)` where `domain(c_i) ≠ domain(c_j)`:

    Bridge(c_i, c_j) = CoOcc(c_i, c_j) × RF(c_i) × RF(c_j)

High bridge score = two frequently-used codes from different domains appearing together often. This is the quantification of the Pudding technique's cross-domain discovery.

**Code velocity** in domain `d` over window `[t_1, t_2]`:

    Vel(d, t_1, t_2) = count of new codes in d during [t_1, t_2] / (t_2 - t_1)

These are simple formulations. Production implementations would need to handle edge cases (codes with zero usage, domains with single codes, temporal windowing for metrics that should not count ancient history equally). But the mathematical structure is clear, and each formula is computable from the existing audit logs.

The IBM reuse metrics follow a similar pattern: Reuse Percent is a ratio of reused components to total components; Cost Avoidance multiplies reuse by historical per-component costs; Value Added is a productivity index. All computable from code-level usage data. The mathematical machinery is well-understood.

---

## 2. RUBRIC META-SCORING

**Evidence Grade: STRONG — Active research frontier with proven results**

The claim here is more ambitious: not only can we score outputs using rubrics, but we can score the rubrics themselves for effectiveness and improve them systematically. This is meta-scoring — evaluating the evaluation system.

### 2.1 OpenRS — Open Rubric System (February 2026)

This is the most directly relevant research we have found. OpenRS, developed by the Qwen Applications team, is a plug-and-play, rubrics-based LLM-as-a-Judge framework that uses an explicit "meta-rubric — a constitution-like specification that governs how rubrics are instantiated, weighted, and enforced." ([Jia et al., 2026 — "Open Rubric System: Scaling Reinforcement Learning with Pairwise Adaptive Rubric," arXiv:2602.14069](https://arxiv.org/abs/2602.14069))

The meta-rubric is hierarchical:

1. **General Meta Rubric (𝓜_gen)** — Captures broadly applicable alignment principles. Refined through automated evolutionary search — a black-box exploration process that optimises the general principles without gradient-based training.

2. **Domain Meta Rubric (𝓜_dom)** — Adapted per domain using a small, curated set of in-domain preference data. Unlike the general level, domain adaptation uses error analysis: rubric-based judgments are compared against human labels, systematic failure modes are identified, and targeted criterion-level edits are applied from {ADD, DELETE, MODIFY}. Human experts periodically audit proposed edits, resolve ambiguous cases, and approve revisions before merging.

The system "continuously refines the hierarchical Meta Rubric to improve the fidelity of the judge, which in turn improves the reward used for policy optimisation." This is the self-improving loop: better rubrics → better scoring → better training signal → better outputs → evidence for further rubric refinement.

OpenRS achieved state-of-the-art results on all four major reward-modelling benchmarks:

| Benchmark | OpenRS (Qwen3-235B) | Best Open Scalar RM | Improvement |
|-----------|---------------------|---------------------|-------------|
| RewardBench v2 | 90.7 | 84.1 | +6.6 |
| PPE Preference (ZH) | 82.3 | 79.6 | +2.7 |
| RM-Bench | 93.0 | 92.8 | +0.2 |
| JudgeBench | 91.6 | 80.0 | +11.6 |
| **Average** | **89.4** | **84.3** | **+5.1** |

The +5.1 average improvement over the strongest open scalar reward model baseline is significant because it demonstrates that explicit rubric decomposition provides a strictly stronger signal than monolithic scalar scoring. The rubric is not just a convenience for human readability — it is a measurably better mechanism. ([Jia et al., 2026 — OpenRS, arXiv:2602.14069](https://arxiv.org/html/2602.14069v2))

**Key parallels to Amplified:**

- OpenRS's meta-rubric is constitutional — like our gates in the Validation Methodology.
- Its domain rubrics adapt per context — like our proposed lenses.
- Its evolutionary refinement is systematic — like our Kaizen process.
- The rubric itself is scored for effectiveness — this is what we propose for our gates.
- The {ADD, DELETE, MODIFY} edit operations on criteria are exactly the kind of targeted improvements Kaizen should make.

### 2.2 GoDaddy — Rubric-as-Reward (RaR)

GoDaddy's 2025 work on calibrating LLM-as-a-Judge scores provides practical guidance on rubric design for evaluation systems. They advocate structured rubrics that replace subjective scales with verifiable yes/no criteria, producing fine-grained sub-scores that aggregate into a final score.

Their recommendations:

- **Quality dimensions** — Rubrics should cover multiple dimensions including correctness, completeness, logical structure, and tone.
- **Importance categorisation** — Criteria should be categorised by importance: essential, important, optional, and pitfall (criteria that indicate failure modes).
- **Verifiability** — Each criterion must be verifiable in isolation through yes/no answers to prevent hallucination.
- **Transparent aggregation** — Sub-scores combine into a final score either through explicit aggregation (checklist-style sums by fixed formula) or implicit aggregation (step-by-step assessment followed by holistic score).

GoDaddy argues for "including product rubrics in a well-calibrated LLMJ scoring process" because it provides transparency (you can see which criteria drive the score), targeted improvement (you know which dimension to fix), and cost-efficiency (you can fine-tune specific criteria rather than retraining entire models). ([Pathak, H., 2025 — "Calibrating Scores of LLM-as-a-Judge," GoDaddy Engineering](https://www.godaddy.com/resources/news/calibrating-scores-of-llm-as-a-judge))

**The lesson for Amplified:** Our gates should produce sub-scores per criterion, not just pass/fail. The sub-scores enable targeted improvement. The importance categorisation (essential vs optional) maps directly to how we weight different gates — some gates are non-negotiable (like G1: Source Verification), others might be weighted differently depending on context.

### 2.3 Rubric-Based Evaluation for Specialised Domains

A 2025 article on Rubric-Based Evaluation (RBE) for LLMs in specialised domains describes how rubric meta-evaluation operates as an iterative process. The rubric "is no longer a static set of rules but a formal, evolving definition of the domain-specific 'correct thought process.'" Calibration against human experts is emphasised as necessary for reliability, using metrics like Cohen's Kappa to align LLM judges with human expert consensus. The iterative refinement process uses LLM judges to infer "latent thinking traces" from human and AI raters, leading to continuous refinement for supervised fine-tuning or RLHF. ([Koduvely, H.M., 2025 — "The Effectiveness of Rubric-Based Evaluation for LLM-Based Solutions in Scarce Ground Truth Domains," LinkedIn](https://www.linkedin.com/pulse/effectiveness-rubric-based-evaluation-llm-based-scarce-koduvely-tlxnc))

This aligns with OpenRS's approach: the rubric is not static. It is evaluated against outcomes, failure modes are identified, and criteria are refined. The rubric evolves as the system learns what matters.

### 2.4 Sam Houston State University — A Rubric for Scoring Rubrics

Perhaps the most direct evidence that meta-scoring is a proven practice: Sam Houston State University (SHSU) has published an actual rubric for evaluating assessment plans — a meta-assessment rubric. It evaluates assessment plans on a 4-point scale (Developing → Minimally Compliant → Good → Exemplary) across ten dimensions:

| Dimension | What It Evaluates |
|-----------|-------------------|
| Goals | Clarity and completeness of stated goals |
| Objectives | Whether objectives meet specifications (measurable, aligned) |
| Indicators / KPIs | Quality and directness of measurement indicators |
| Criteria / Targets | Appropriateness and completeness of success criteria |
| Findings / Results | Quality of data collection and alignment with targets |
| Actions | Specificity and relevance of improvement actions |
| PCI Update | Whether previous improvement commitments were addressed |
| New PCI | Whether current actions are carried forward as commitments |
| Overall Rating | Holistic assessment of the entire plan |

At the "Exemplary" level, goals must "address the full purpose of the unit according to the course catalogue," indicators must include "a mix of direct and indirect measures used for each objective," and actions must provide "specific detail (who, what, when, where, why)." ([SHSU — Meta-Assessment Rubric, 2025](https://www.shsu.edu/offices-departments/assessment/documents/shsu-meta-assessment-rubric-4-2025.pdf))

This is literal meta-scoring: a rubric that evaluates rubrics. It is not theoretical. It is in production use at a university for evaluating the quality of their assessment systems.

### 2.5 What This Means for Amplified

The Validation Methodology's 7 gates (G1–G7) are our rubric. Each gate has pass/fail criteria. We can score each gate's effectiveness by measuring:

**(a) Catch rate** — How often does each gate catch errors that would have caused downstream failures? A gate that never fails anything is either perfectly positioned (everything upstream is clean) or not discriminating enough (it is missing problems). We need data to tell which.

**(b) Downstream correlation** — Do gate pass rates correlate with downstream quality? If nodes that pass G3 still fail at the application layer, G3 is not testing the right things.

**(c) Redundancy detection** — Do certain gates always pass when a prior gate passes? If G4 has a 100% pass rate conditional on G3 passing, G4 may be redundant — or it may need sharper criteria.

**(d) Criterion-level decomposition** — Following GoDaddy's recommendation and OpenRS's approach, each gate should produce sub-scores, not just pass/fail. Which specific criterion within a gate is doing the most discriminating? Which criteria are decorative?

**(e) Longitudinal improvement tracking** — Following SHSU's approach, we should assess the assessment. Are our gates getting better at catching real problems? Is the false positive rate declining? Is the false negative rate being measured at all?

This meta-scoring tells us which gates are actually earning their keep. Mathematics decides — but only if we measure.

### 2.6 The Meta-Scoring Cascade

Meta-scoring does not stop at one level. If we score the rubric's effectiveness, we should also score the meta-rubric's effectiveness. This is not infinite regress — it converges because each level operates at a different timescale:

| Level | What Is Scored | Timescale | Mechanism |
|-------|---------------|-----------|----------|
| **Level 0: Output scoring** | Individual nodes against gate criteria | Per-write (real-time) | Gate pass/fail |
| **Level 1: Gate scoring** | Gate effectiveness against downstream quality | Weekly (Kaizen cycle) | Correlation analysis |
| **Level 2: Rubric scoring** | Overall gate system against system objectives | Monthly (strategic review) | Outcome tracking |
| **Level 3: Rubric-design scoring** | Whether our approach to rubric design is improving | Quarterly (meta-review) | Trend analysis |

Level 0 is what we do now. Level 1 is what this hypothesis proposes implementing first. Level 2 follows once we have enough Level 1 data. Level 3 is a longer-term aspiration that requires at least a year of Level 2 data.

OpenRS operates primarily at Levels 0 and 1. SHSU's meta-assessment rubric operates at Level 2. No system we found operates systematically at Level 3. But the mathematical structure supports it — each level is simply the application of the same scoring mechanism to the level below it.

---

## 3. LENS-ADAPTIVE EVALUATION

**Evidence Grade: MODERATE — Theoretical framework exists, practical implementations emerging**

The claim here is that scoring criteria should change based on the problem being solved, not just the subject. Different contexts — different lenses — make different quality dimensions more or less important. This is the most ambitious part of the hypothesis and the least empirically validated in our specific context.

### 3.1 Brunswik's Lens Model — The Theoretical Foundation

Egon Brunswik's lens model, first articulated in 1956, describes how judgment happens through "cues" that mediate between the criterion (the truth) and the judgment (the assessment). The key insight: different cues have different "ecological validities" depending on the environment.

A 2024 paper in *Frontiers in Psychology* by Blackhurst et al. uses the Brunswik lens model as a framework for studying deception detection in autistic adults. While domain-specific, the paper provides a clear exposition of how the model works: it describes how judgments are formed through probabilistic cue utilisation. In the model, the criterion (what is actually true) produces observable cues. Judges perceive these cues and form judgments. The accuracy of the judgment depends on two factors: the ecological validity of the cues (how reliably each cue actually indicates the criterion) and the utilisation coefficients (how heavily the judge relies on each cue). Crucially, judges often rely on cues with low ecological validity — cues that feel informative but are not — while underweighting cues that are actually predictive. ([Blackhurst et al., 2024 — "The Brunswik Lens Model," Frontiers in Psychology](https://pmc.ncbi.nlm.nih.gov/articles/PMC11271661/))

A 2026 paper in the *Psychonomic Bulletin & Review* introduced a "diffusion lens model" that captures how sensitivity to ecological cue validity increases over time. In the model, sensitivity (the drift rate scaling parameter b_v,t) starts low — representing initial uncertainty — and increases asymptotically through experience. The mechanism: as the system accumulates cue-outcome co-occurrences, it learns which cues actually predict which outcomes. Higher sensitivity leads to stronger drift for valid cues, shorter response times, and higher accuracy. The model was validated on multiple-cue probability learning data, recovering the trajectory from novice (zero sensitivity) to expert (near-perfect validity approximation). ([Scholten, Schumacher & Kelber, 2026 — "Brunswik's fundamental principle explained: A diffusion lens model," Psychonomic Bulletin & Review](https://pmc.ncbi.nlm.nih.gov/articles/PMC12913299/))

**Key parallel to Amplified:** Different lenses (problem contexts) make different codes more or less relevant. A finance lens makes FIN-* codes more ecologically valid. A technology lens elevates TEC-* codes. The lens determines which rubric criteria matter most. And, critically, the system should learn which cues (codes) are actually predictive in each context — not just assume that domain labels are sufficient.

### 3.2 Adaptive Rubrics on Vertex AI (February 2026)

OneUptime's February 2026 guide on implementing adaptive rubrics for Vertex AI provides a concrete implementation of lens-adaptive evaluation. Their system uses adaptive rubrics that "adjust criteria based on the task being evaluated."

Examples of task-specific rubric weightings:

| Task Type | Primary Criteria | Weighting |
|-----------|-----------------|-----------|
| Technical documentation | Accuracy, Completeness, Clarity, Actionability | 0.35, 0.25, 0.25, 0.15 |
| Customer support | Helpfulness, Empathy, Accuracy, Conciseness | 0.35, 0.20, 0.30, 0.15 |
| Summarisation | Coverage, Faithfulness, Conciseness | 0.35, 0.35, 0.30 |
| Code generation | Correctness, Efficiency, Readability, Completeness | (emphasised, weights not specified) |

Their implementation uses an `AdaptiveRubricRegistry` that maintains pre-defined rubrics per task type. A `batch_evaluate` function routes each test case to its task-appropriate rubric based on the `task_type` field. If no rubric exists for a task type, the system logs a warning and skips evaluation rather than applying a generic rubric. ([Dhandala, N., 2026 — "How to Use Adaptive Rubrics for Automated LLM Output Evaluation on Vertex AI," OneUptime](https://oneuptime.com/blog/post/2026-02-17-how-to-use-adaptive-rubrics-for-automated-llm-output-evaluation-on-vertex-ai/view))

**Key parallel to Amplified:** The RubricRegistry pattern maps directly to our lens concept. Each lens is a pre-configured weighting of evaluation criteria for a specific problem context. The routing mechanism (task_type → rubric) is the same mechanism we would use (lens selection → gate weightings).

### 3.3 OpenRS Domain Meta Rubric — Lens-Adaptive by Design

OpenRS's two-level system (General + Domain) is lens-adaptive by design. The General Meta Rubric captures universal principles that apply across all evaluation contexts. The Domain Meta Rubric adapts "using a small, curated set of in-domain preference data" through error analysis — comparing rubric-based judgments against human labels, identifying failure modes, and applying targeted edits.

The ablation study in the OpenRS paper confirms that domain-specific refinements are critical: removing the Domain Meta Rubric degraded performance on PPE Preference from 82.3 to 80.9 (on the Chinese subset where data was available). The authors note that "to specialise the reward signal for a target domain, we refine or introduce a Domain Meta Rubric rather than fine-tuning a generative reward model. This modularity avoids catastrophic forgetting and negative transfer." ([Jia et al., 2026 — OpenRS, arXiv:2602.14069](https://arxiv.org/html/2602.14069v2))

This is exactly lens-based evaluation: the scoring criteria change based on the problem domain. Same meta-rubric architecture. Different domain-specific weightings and criteria.

Notably, the ablation study showed that removing Domain Meta Rubrics while keeping the General Meta Rubric degraded performance — confirming that domain-specific adaptation is not optional. The general principles are necessary but not sufficient. The lens matters.

### 3.4 RAISE Framework (October 2025)

RAISE (Responsible AI Scoring and Evaluation) "quantifies model performance across four core dimensions: explainability, fairness, robustness, and sustainability" and "aggregates them into a single, holistic Responsibility Score." Raw metrics are normalised to [0,1], dimension scores average metrics per pillar, and the Responsibility Score aggregates the four dimensions.

The framework was evaluated across three domains — finance (German Credit), healthcare (Diabetes 130-Hospitals), and socioeconomics (ACSIncome) — with the same models producing different responsibility profiles in each domain:

| Model | Finance RS | Healthcare RS | Socioeconomics RS |
|-------|-----------|---------------|-------------------|
| MLP | 0.8352 | 0.8796 | 0.8420 |
| TabResNet | 0.7461 | 0.8716 | 0.8676 |
| Transformer | 0.6402 | 0.6222 | 0.7126 |

The key finding: "No model dominates all dimensions." The same model scores differently depending on the domain lens applied. The Responsibility Score for the same Transformer model ranges from 0.6222 (healthcare) to 0.7126 (socioeconomics) — a 15% swing based purely on the domain lens. The Transformer is explainable and fair but has high sustainability costs. The MLP is robust and sustainable but less interpretable. The lens (domain) determines which trade-offs matter. ([Nguyen & Do, 2025 — "RAISE: A Unified Framework for Responsible AI Scoring and Evaluation," arXiv:2510.18559](https://arxiv.org/html/2510.18559v1))

**Key parallel to Amplified:** The lens does not just change which codes matter. It changes which dimensions of quality matter. A research lens might weight attribution depth heavily and tolerate slow retrieval. An operational lens might weight response latency heavily and accept shallower attribution. Same system. Different priorities.

### 3.5 Sopact — Longitudinal Rubric Validation Through Outcomes

Sopact's rubric system for application scoring provides the strongest evidence for outcome-based meta-scoring — closing the loop between evaluation and results. Their system preserves "persistent unique IDs connected to program outcomes, enabling longitudinal rubric validation — comparing intake scores against post-program outcomes cohort by cohort."

The process:

1. Applicants are scored at intake using a structured rubric with per-criterion scores.
2. Each applicant carries a persistent ID through intake, program participation, milestone completion, and long-term achievement.
3. After outcomes are observed, the system analyses which intake criteria predicted which outcomes.
4. Criteria that predicted success are reinforced. Criteria that did not predict outcomes are redesigned.
5. The rubric improves each cycle based on evidence, not opinion.

For example: if "community impact" scores at intake do not predict stronger outcomes among programme graduates, the criterion is redesigned. If "technical defensibility" predicts funding raises among winners, it is reinforced and potentially reweighted. ([Sopact — "Application Scoring Rubric," 2026](https://www.sopact.com/use-case/application-scoring-rubric))

**Key parallel to Amplified:** This is the outcomes-based feedback loop applied to rubric improvement. Replace "applicant" with "knowledge node." Replace "intake score" with "gate pass results." Replace "post-programme outcomes" with "downstream retrieval quality and user satisfaction." The mechanism is identical. Persistent IDs (our codes) enable longitudinal tracking. Longitudinal tracking enables evidence-based rubric refinement.

### 3.6 What This Means for Amplified

The lens is the problem context. When the system evaluates research quality, the lens is "research" and the rubric weights:
- RES-* code depth (are the research methodology codes present and specific?)
- Source attribution completeness (does every claim trace to a primary source?)
- Primary-source confidence (how many hops from the original research?)

When the system evaluates infrastructure code, the lens is "infrastructure" and the rubric weights:
- TEC-* code compliance (are the technology codes correctly applied?)
- Error registry coverage (are known failure modes documented?)
- Test pass rates (does the code actually work?)

Same gates. Different weightings. The lens selects which dimensions of the rubric matter most.

### 3.7 How Lenses Would Work in Practice

A lens in the Amplified system would be a configuration object. Here is a conceptual example for a research lens:

```
lens:
  name: "research"
  description: "Evaluation context for research-quality knowledge nodes"
  gate_weightings:
    G1_structure: 1.0              # Non-negotiable — schema must be valid
    G2_label_validity: 0.8         # Important but cross-discipline terms expected
    G3_rubric_benchmark: 1.0       # Critical — RAEI scoring must be rigorous for research
    G4_match_quality: 0.7          # Moderate — research nodes match differently than operational ones
    G5_recipe_scoring: 0.6         # Lower — research may not be recipe-ready yet
    G6_test_intentlogic: 0.9       # High — research claims need testable hypotheses
    G7_shipping: 1.0               # Non-negotiable — final boss always applies
  code_relevance_boost:
    RES_prefix: 1.5
    MET_prefix: 1.3    # Methodology codes elevated
    SRC_prefix: 1.2    # Source codes elevated
  scoring_thresholds:
    minimum_RAEI: 14               # Higher than default 12 for research
    minimum_attribution_depth: 3
    minimum_primary_source_ratio: 0.5
```

And a contrasting infrastructure lens:

```
lens:
  name: "infrastructure"
  description: "Evaluation context for technical infrastructure knowledge"
  gate_weightings:
    G1_structure: 1.0              # Non-negotiable — schema must be valid
    G2_label_validity: 1.0         # Critical — technical labels must be exact
    G3_rubric_benchmark: 0.8       # Important but vendor docs may score differently
    G4_match_quality: 0.6          # Lower — infrastructure nodes are more standalone
    G5_recipe_scoring: 0.5         # Lower — infrastructure knowledge rarely becomes recipes
    G6_test_intentlogic: 1.0       # Critical — infrastructure claims must be testable
    G7_shipping: 1.0               # Non-negotiable — final boss always applies
  code_relevance_boost:
    TEC_prefix: 1.5
    OPS_prefix: 1.3
    ERR_prefix: 1.2    # Error codes elevated
  scoring_thresholds:
    minimum_RAEI: 12               # Standard threshold
    maximum_age_days: 180          # Stale infrastructure docs are dangerous
```

The same node, evaluated under different lenses, would receive different scores. A research paper from 2019 about cloud architecture might score well under the research lens (deep attribution, rigorous methodology) but poorly under the infrastructure lens (stale, not reflecting current best practices). This is not a flaw — it is the point. The lens captures what matters for the specific use case.

The lens selection could be automatic (based on the query context or the requesting agent's role), manual (the user specifies which lens to apply), or hybrid (the system suggests a lens, the user confirms). The governance of lens creation and modification would need its own process — lenses are evaluation policy, and evaluation policy should be deliberate.

This is the Brunswikian insight applied to knowledge management: different environments have different ecological validities. The cues (codes) that predict quality in a research context are not the same cues that predict quality in an operational context. The lens model tells us this is expected — and the diffusion lens model tells us the system should learn which cues matter in which contexts over time.

### 3.8 Lens-Adaptive Evaluation Beyond LLMs

The lens-adaptive principle — same criteria, different weights based on context — is not limited to LLM evaluation. It has been operating in safety-critical industries for over a decade.

**Aerospace manufacturing inspection.** The Aerospace Corporation's TOR-2015-02544 document, "Process Approach to Determining Quality Inspection Deployment," describes a methodology that uses context-dependent weighting across 10 evaluation studies. The weights shift dramatically based on the type of change being evaluated:

| Study | Manufacturing Process Change | Inspection Process Change | Data-Driven/Management Change |
|-------|------------------------------|---------------------------|-------------------------------|
| PFMEA (risk priority) | 10% | 10% | 10% |
| Process qualification | 10% | 3% | 3% |
| Pilot/proof of concept | 5% | 3% | 3% |
| Nonconformity rate | 10% | 3% | 3% |
| Production rate | 5% | 3% | 3% |
| Gage R&R (inspector variability) | 10% | 15% | 8% |
| Lessons learned | 10% | 10% | 10% |
| Inspection escapes | 10% | 20% | 20% |
| Deming cost/risk | 20% | 30% | 30% |
| Stakeholder reaction | 10% | 3% | 10% |

For inspection process changes, inspector variability and escape detection get elevated (45% total). For manufacturing changes, process capability studies dominate (40%). For data-driven changes, cost analysis and historical data dominate (40%). Same 10 criteria. Different weights. Different lenses. This system has been operational since 2015. ([The Aerospace Corporation — "Process Approach to Determining Quality Inspection Deployment," TOR-2015-02544](https://aerospace.org/sites/default/files/maiw/TOR-2015-02544.pdf))

**FAA risk-based inspection.** The FAA applies different inspection frequencies based on risk classification: high-risk manufacturers are inspected every 3 months with 4 supplier audits per year; low-risk manufacturers are inspected once every 3 years with no supplier audits required. The same inspection criteria, applied with different intensity based on the risk lens. ([FAA — "Assessment of FAA's Risk-Based System for Overseeing Aircraft Certification," OIG Report](https://www.oig.dot.gov/sites/default/files/WEB_FILE_Final_Supplier_report.pdf))

**Risk-based internal auditing.** A 2023 paper in the *Annals of Operations Research* describes a multi-objective optimisation approach where AHP (Analytic Hierarchy Process) weights are computed for different auditable units based on their risk profiles. The resulting risk score — Risk Score = Σ(weight × rating) — uses weights that change per auditable area. The evaluation adapts to the audit context, not the other way around. ([PMC — "A multi-objective optimization approach for integrated risk-based internal audit planning," Annals of Operations Research, 2023](https://pmc.ncbi.nlm.nih.gov/articles/PMC9925941/))

**Lesson for Amplified:** Lens-adaptive evaluation is not a novel idea emerging from LLM research. It is a proven methodology in safety-critical industries — aerospace, aviation regulation, and financial audit — where getting the evaluation wrong has consequences measured in lives and dollars. The principle is the same in every case: maintain a fixed set of evaluation criteria, but adjust the weights based on the context of what is being evaluated. Our proposal to apply different gate weightings under different lenses is consistent with decades of practice in industries where evaluation rigour is non-negotiable.

---

## 4. THE UNIFICATION — HOW IT ALL LINKS TOGETHER

This is the novel part. Not the pieces — the pieces are proven. The novelty is the claim that connecting them through compressed codes creates a self-improving system.

### 4.1 The Loop

```
Codes → enable scoring (countable metrics from code usage)
    ↓
Scoring → feeds rubric evaluation (gate effectiveness measured by code-level outcomes)
    ↓
Rubric evaluation → adapts via lens (problem context determines which metrics matter)
    ↓
Lens outcomes → refine codes (codes that predict outcomes gain weight; codes that don't get deprecated)
    ↓
Back to Codes → (improved codes enable better scoring)
```

This is a closed loop. The codes feed the scoring. The scoring validates the rubrics. The rubrics adapt to the lens. The lens outcomes improve the codes. Each element makes the others better.

### 4.2 Parallels in Existing Systems

This loop is not entirely without precedent. Partial versions run in several domains:

**Medical informatics:**
```
SNOMED codes 
  → clinical quality metrics (disease prevalence, comorbidity patterns, documentation completeness)
    → clinical decision rules (evidence-based guidelines weighted by quality metrics)
      → rule effectiveness studies (does following the rule improve outcomes?)
        → SNOMED hierarchy improvements (codes refined based on measured utility)
```

This loop runs continuously in healthcare. SNOMED CT is updated twice yearly. Quality metrics from code usage inform which areas of the hierarchy need improvement. Clinical decision rules are updated based on outcomes data. The entire system is self-improving — slowly, carefully, with extensive validation, but self-improving nonetheless.

**OpenRS:**
```
Meta-rubric (constitutional principles)
  → adaptive rubric per response pair (criteria selected based on semantic differences)
    → criterion-wise scoring (each criterion evaluated independently)
      → meta-rubric refinement (error analysis → {ADD, DELETE, MODIFY} criterion edits)
```

This loop runs during training. The meta-rubric governs rubric instantiation. The rubrics score responses. The scores are compared against human preferences. Discrepancies drive meta-rubric refinement. OpenRS explicitly describes this as a continuous refinement process.

**IBM Software Reuse:**
```
Faceted classification codes
  → reuse frequency metrics (Reuse Percent, Cost Avoidance, Value Added)
    → library curation decisions (which components to maintain, improve, or deprecate)
      → improved classification (better facets based on usage patterns)
```

This loop ran at IBM for years. The faceted codes enabled measurement. The measurements informed curation. The curation improved the library. The improved library generated better measurements.

### 4.3 The Hypothesis, Stated Precisely

**The hypothesis is that this loop, applied to Amplified's coding system, creates a self-improving knowledge management system where the taxonomy, the quality evaluation, and the retrieval all improve together because they share the same underlying mechanism: compressed codes.**

The taxonomy improves because usage metrics reveal which codes are valuable and which are noise. The quality evaluation improves because gate effectiveness is measured against code-level outcomes, enabling targeted criterion refinement. The retrieval improves because lens-adaptive weighting prioritises the codes most predictive of quality in each context.

Each improvement in one layer propagates to the others because they share the same underlying data structure. Better codes → better scoring → better rubrics → better lens calibration → better codes.

This is the "mathematics decides" principle extended to the system itself. Not just mathematics deciding about individual data quality, but mathematics deciding about the quality of the quality system. Meta-mathematics. Self-referential improvement.

### 4.4 Worked Example: How the Loop Would Operate

To make this concrete, here is a hypothetical — but realistic — scenario of one turn of the flywheel:

**Step 1 — Codes reveal a pattern (Scoring Layer):**
Kaizen's weekly metrics report shows that nodes tagged with both `RES-METHODOLOGY` and `FIN-REGULATORY` have a 40% higher reuse frequency than average, but a 25% lower gate pass rate at G2 (Label Validity). This is a cross-domain bridge — research methodology applied to financial regulation — and the co-occurrence is flagged as significant.

**Step 2 — Gate investigation (Rubric Meta-Scoring):**
The G2 failure analysis reveals that these nodes are failing on label validity — specifically, the PUDDING facet check flags terminology inconsistencies. But the inconsistency is expected: research methodology terms and financial regulation terms use different labelling conventions. The G2 criterion is penalising legitimate cross-domain work. The criterion has a high false positive rate for bridge nodes.

**Step 3 — Lens-adaptive adjustment (Lens Layer):**
A new lens is proposed: "cross-domain research." Under this lens, the G2 label validity criterion for terminology consistency is downweighted (from essential to important), while the G3 rubric benchmark criterion for RAEI scoring is upweighted (because cross-domain claims require stronger evidence quality). The lens is tested against the existing cross-domain node set.

**Step 4 — Outcome measurement (Loop Closure):**
With the new lens, gate pass rates for legitimate cross-domain nodes increase from 60% to 85%. False negative rate (good nodes incorrectly failed) drops. Downstream retrieval quality for cross-domain queries improves by 15%. The `RES-METHODOLOGY × FIN-REGULATORY` co-occurrence pattern is validated as a genuine bridge, and Kaizen creates a new composite code `BRIDGE-RES-FIN` to track it explicitly.

**Step 5 — Back to codes:**  
The new `BRIDGE-RES-FIN` code enters the metrics. Its frequency, decay rate, and gate pass rate are now tracked. The next cycle of Kaizen metrics will show whether this bridge code is growing (more cross-domain work) or stable (a known niche). The scoring layer is richer. The rubric is more accurate. The lens has a new configuration. One turn of the flywheel, complete.

This is hypothetical. But every individual step — metrics extraction, gate analysis, criterion weighting, outcome measurement, code creation — uses mechanisms that already exist in the Amplified architecture or are proven in the literature.

### 4.5 The Flywheel vs. a Dashboard

A sceptic might ask: how is this different from just building a metrics dashboard?

The difference is feedback direction. A dashboard shows metrics to humans, who then make decisions. The flywheel proposes that the metrics themselves inform automated refinements. The distinction matters because:

1. **Speed** — Human review of metrics is slow (weekly at best). Automated refinement can operate continuously.
2. **Scale** — A human reviewer can examine a few dozen metrics. The scoring layer produces thousands of code-level signals. Only automated processing can handle the volume.
3. **Consistency** — Human interpretation of metrics varies by reviewer, mood, and context. Automated rules apply uniformly.
4. **Accountability** — Automated refinements leave a complete audit trail. Human decisions often do not.

However, the flywheel is not fully automated. OpenRS includes human-in-the-loop oversight for meta-rubric refinement. SNOMED CT changes go through governance committees. The flywheel proposes automation of the measurement and recommendation phases, with human oversight at the decision and implementation phases. The mathematics recommends. The humans decide. Mathematics decides — but within a governance framework.

### 4.6 Why This Might Not Work

We need to be honest about the risks:

1. **Feedback loops can be vicious, not just virtuous.** If a code becomes artificially popular (perhaps due to a systematic bias in code assignment), the scoring layer will amplify that popularity, the rubrics will weight it more heavily, and the bias propagates. Self-improving systems can also be self-degrading systems. Medical informatics handles this with extensive validation and human oversight. We will need similar safeguards.

2. **The loop speed matters.** If it takes months to observe outcomes, refine codes, and propagate improvements, the system may be too slow to be useful. Healthcare manages because clinical decision cycles are long. Our cycles may need to be faster.

3. **Complexity cost.** Running the loop requires computing metrics, conducting meta-assessments, adjusting lens weightings, and propagating changes — all while maintaining the existing SLAs. The overhead may be trivial or it may be prohibitive. We do not know yet.

4. **Goodhart's Law.** "When a measure becomes a target, it ceases to be a good measure." If agents learn that high code frequency is valued, they may over-apply popular codes. If gate pass rates become targets, criteria may be softened to achieve them. Every scoring system is vulnerable to gaming. The mitigation is to score at multiple levels (individual metrics, interactions, meta-scores) so that gaming one metric degrades another. But Goodhart's Law is a permanent concern, not a solvable problem.

5. **Cold start problem.** The scoring layer requires historical data to produce meaningful metrics. New codes have no frequency history. New domains have no co-occurrence patterns. The system is most useful where we have the most data — and least useful where we are exploring new territory. This is the opposite of what we might want: new territory is exactly where better scoring would be most valuable.

### 4.7 Convergence Conditions — When Does the Flywheel Turn?

The flywheel's central claim is that iterative refinement converges — that each turn makes the system better, not worse. This is not guaranteed. A January 2026 paper, "On the Limits of Self-Improving in Large Language Models" (arXiv:2601.05280v2), provides the formal mathematical framework for when self-improving loops converge and when they collapse.

**The formal result:** If a self-referential system maintains a persistent exogenous signal (α_t ≥ α* > 0 for all t), the system converges to the true distribution P. If the exogenous signal vanishes (α_t → 0), the system degenerates to a fixed point — it collapses to a narrow, self-reinforcing consensus that may bear no relationship to ground truth. ([arXiv:2601.05280v2 — "On the Limits of Self-Improving in Large Language Models," 2026](https://arxiv.org/html/2601.05280v2))

**Direct application to Amplified:** The gates (G1–G7) ARE the persistent exogenous signal. They are constitutional — they do not change based on what the system produces. They are external evaluators that the system cannot modify to make its own outputs look better. As long as the gates remain fixed (α_t stays bounded away from zero), the refinement loop has a mathematical basis for convergence rather than collapse.

The paper also proves that multi-agent systems without external grounding converge to a "consensus reality" of the initial agents' biases. Without fixed external evaluation, even diverse agents will converge to shared biases — they agree with each other, not with truth. The gates prevent this by maintaining an evaluation standard that is independent of any agent's outputs.

**The management theory parallel:** Deming's first point — "constancy of purpose" — is the quality management articulation of the same mathematical condition. Without a fixed reference point, improvement loops oscillate. Anderson et al. (1994) characterise this as "convergence and reorientation" — stability requires persistent commitment to fixed principles. The gates are Amplified's constancy of purpose. ([The W. Edwards Deming Institute — "Systems Thinking: Feedback Loops"](https://deming.org/systems-thinking-feedback-loops/))

**Practical implication:** The flywheel converges IF AND ONLY IF the gates remain fixed external evaluators. If gates are softened to improve pass rates — "let's lower the RAEI threshold because too many nodes are failing" — the convergence condition breaks. This is Goodhart's Law wearing a different hat: optimising the metric by changing the metric destroys the metric's value. The formal mathematics tells us this is not just a heuristic — it is a theorem. Persistent excitation is the necessary and sufficient condition for convergence.

### 4.8 Goodhart Mitigations — Protecting the Scoring Layer

Every scoring system is vulnerable to gaming. In healthcare, this manifests as upcoding — assigning diagnosis and procedure codes that maximise reimbursement rather than accurately reflecting clinical reality. If our coded scoring layer creates incentives (nodes that score well get retrieved more, agents that produce high-scoring nodes get trusted more), the same gaming dynamics will emerge. The question is not whether gaming will occur, but how to detect and mitigate it.

**Systematic mitigations.** A 2022 CNA (Center for Naval Analyses) report on recognising and mitigating Goodhart's Law provides a framework that maps directly to Amplified's architecture: ([CNA — "Goodhart's Law: Recognizing and Mitigating the Manipulation of Measures in Analysis," 2022](https://www.cna.org/reports/2022/09/Goodharts-Law-Recognizing-Mitigating-Manipulation-Measures-in-Analysis.pdf))

- **"Measure all relevant system characteristics"** → We already propose 7 gate metrics plus their interactions (Sections 1.5–1.6). Gaming one metric degrades another because they are structurally coupled — a node cannot inflate its RAEI score without also providing the attribution depth that G1 checks.
- **"Use MOEs not MOPs"** → Measure downstream retrieval quality (outcomes), not just gate pass rates (activities). A node that passes all gates but is never retrieved, never reused, and never cited in downstream work is passing the letter of the law but not its spirit.
- **"Randomise measures over time"** → Kaizen rotates which metrics are highlighted in each improvement cycle. No single metric remains the target long enough for systematic gaming.
- **"Identify decoupling opportunities"** → Curator audit logs are written by the Curator, not by the agents being evaluated. The measured entity does not control the measurement. This is the CNA report's most important principle: separate the measurer from the measured.
- **"Wargame measures"** → The Error Registry already documents known failure patterns. This should be extended to include known gaming patterns — a "red team" section that explicitly describes how each metric could be gamed and what the detection signature would look like.

**Healthcare's multi-metric surveillance as a model.** Healthcare fraud detection is the most mature example of Goodhart mitigation in a coded system. The parallels to our architecture are striking: ([CombineHealth — "Understanding Upcoding in Medical Billing," 2025](https://www.combinehealth.ai/blog/upcoding-in-medical-billing)) ([PMC — "Healthcare insurance fraud detection using data mining," BMC Medical Informatics, 2024](https://pmc.ncbi.nlm.nih.gov/articles/PMC11046758/))

- **Peer comparison** — CMS's CERT programme compares each provider's billing patterns against peers. Adapted to Amplified: compare each agent's coding patterns against peer agents working in the same domain. Outliers are flagged.
- **Multi-dimensional anomaly detection** — Private payers use predictive models trained on multiple signals simultaneously. No single metric can be gamed without triggering another. Adapted: monitor gate pass rates, code distributions, reuse patterns, and attribution depth simultaneously.
- **The "Four F's" adapted** — Frequency (a code is overused relative to peers), Financial anomaly (sudden scoring spikes without corresponding quality improvement), Form inconsistency (codes assigned do not match node content on manual review), Follow-up evasion (agent avoids or delays audit processes).

**The structural defence.** Manheim & Garrabrant (2019) classify Goodhart effects into four types: regressional, extremal, causal, and adversarial. Their key insight for coded systems is that multi-level scoring creates a "measurement mesh" where gaming one metric degrades another — because the metrics are structurally coupled. In Amplified, codes serve multiple purposes simultaneously: retrieval, scoring, attribution, and cross-domain discovery. Gaming codes for one purpose (inflating scores) necessarily degrades the others (retrieval becomes noisy, attribution becomes unreliable, cross-domain discovery finds false bridges). This is a natural Goodhart defence — the measurement mesh. ([Alignment Forum — "Classifying specification problems as variants of Goodhart's Law," 2019](https://www.alignmentforum.org/posts/yXPT4nr4as7JvxLQa/classifying-specification-problems-as-variants-of-goodhart-s))

**Honest acknowledgment:** These mitigations reduce but do not eliminate gaming risk. Goodhart's Law is a permanent concern, not a solvable problem. Healthcare has spent decades building fraud detection systems and still loses billions annually to upcoding. Our mitigation strategy is vigilance, not victory — continuous monitoring, multi-metric surveillance, structural coupling, and periodic red-teaming. The measurement mesh makes gaming harder, not impossible.

### 4.9 Cold Start Bootstrapping

Section 4.6 identified the cold start as a risk: new codes have no history, new domains have no co-occurrence patterns, and the scoring layer is least useful where it could be most valuable. The literature offers three complementary bootstrapping strategies.

**Transfer from adjacent domains.** BOLT-K (Bootstrapping Ontology Learning via Transfer of Knowledge) demonstrates bootstrapping a new domain ontology by transferring knowledge from an existing, related domain. Their LSTM-based framework seeds the new domain with concepts from a related domain, uses semantic and topological features to identify concept relationships, and achieves >75% accuracy in identifying related concept pairs via transfer. The directly applicable insight: bootstrap new Amplified domains by transferring code patterns from established domains. If the financial regulation domain is mature and the legal compliance domain is new, the overlap in codes and co-occurrence patterns provides a warm start for legal compliance. ([BOLT-K — "Bootstrapping Ontology Learning via Transfer of Knowledge," WWW 2019](https://dl.acm.org/doi/10.1145/3308558.3313511))

**Iterative enrichment.** A March 2026 JMIR paper describes an LLM-assisted SNOMED CT mapping tool that starts with syntactic mapping (exact match), falls back to semantic mapping (vector similarity), and iteratively enriches its mapping database with validated results. Each validated mapping improves the system's ability to handle the next unmapped term. The result: up to 90% reduction in manual mapping workload. The cold start solution is not to wait for comprehensive data — it is to start mapping and let each validated result bootstrap the next. ([JMIR Medical Informatics — "Development and Evaluation of SNOMED CT Automated Mapping," 2026](https://medinform.jmir.org/2026/1/e82670))

**Meta-learning.** The third strategy is to learn the pattern of how to assign codes, not just the codes themselves. Meta-learning approaches learn from the code-assignment process across multiple domains, then apply that meta-knowledge to new domains with minimal examples. This is the most ambitious bootstrapping strategy and the least proven in our specific context, but it represents the direction the field is moving.

**Amplified's cold start strategy:**

1. **Start where the data is.** Phase 1 of the validation plan should begin with the domains that have the most existing data. These domains provide the baseline metrics against which new domains are calibrated.
2. **Seed from neighbours.** Use established code patterns as seeds for new domains. Cross-domain co-occurrence data from mature domains provides initial structure for related new domains.
3. **Track bootstrapping velocity.** Measure how quickly a new domain's metrics become statistically meaningful. This is a meta-metric: how fast is the cold start resolving?
4. **Set minimum sample sizes.** Scoring metrics should not be considered reliable for a domain until a minimum sample size is reached. Before that threshold, scoring outputs should be flagged as provisional.

---

## 5. EVIDENCE GRADING

The following table grades each sub-claim in the hypothesis. Evidence grades follow the convention established in our companion documents:

- **STRONG** — Multiple independent confirmations from different domains
- **MODERATE** — Some evidence exists, needs more validation
- **HYPOTHESIS** — Logical but unproven
- **INSUFFICIENT** — Looked but did not find enough

| # | Claim | Evidence Grade | Source Domains | Confidence |
|---|-------|---------------|----------------|------------|
| 1 | Codes can be used as a scoring layer | **STRONG** | Medical informatics, software reuse, knowledge graphs, enterprise knowledge | High — multiple independent confirmations across decades |
| 2 | Code frequency predicts concept importance | **STRONG** | SNOMED prevalence tracking, IBM reuse metrics, KG entity popularity | High — proven at scale in production systems |
| 3 | Code co-occurrence reveals structural relationships | **MODERATE** | Medical comorbidity patterns, faceted classification | Medium — proven in medicine, untested in our context |
| 4 | Rubrics can be meta-scored for effectiveness | **STRONG** | OpenRS, SHSU meta-assessment, Sopact outcome tracking | High — active research area with benchmarks and production use |
| 5 | Meta-scoring improves rubric quality | **STRONG** | OpenRS +5.1 over scalar baselines, RaR calibration methodology | High — quantified improvements on standard benchmarks |
| 6 | Evaluation should adapt to problem context (lens) | **MODERATE-STRONG** | Brunswik lens model (theory, 1956+), Vertex AI adaptive rubrics (practice, 2026), aerospace inspection (The Aerospace Corporation, 2015), risk-based auditing (AHP-weighted evaluation) | Medium-High — theoretical foundation strong, practical evidence now spans LLM evaluation, aerospace, audit, and manufacturing |
| 7 | Lens-adaptive weighting improves outcomes | **MODERATE** | RAISE cross-domain evaluation, OpenRS domain meta rubrics, Sopact longitudinal validation | Medium — demonstrated in specific contexts, not generalised |
| 8 | Codes can serve as the shared mechanism linking taxonomy, scoring, and retrieval | **MODERATE** | SNOMED CT (codes link clinical terminology, quality metrics, and decision support), IBM (codes link catalogue, metrics, and curation) | Medium — proven in individual systems, not as a general principle |
| 9 | The full loop (codes → scoring → rubric → lens → codes) operates as a flywheel | **HYPOTHESIS** | No single system implements the complete loop as described | Low — each piece is proven, the integration is novel |
| 10 | The flywheel is self-improving (each turn produces net improvement) | **HYPOTHESIS** | Partial evidence from OpenRS refinement loops and SNOMED update cycles | Low — requires longitudinal observation to confirm |

---

## 6. WHAT WE DON'T KNOW

Honest assessment of gaps in the evidence. These are not weaknesses to hide — they are the research agenda.

### 6.1 No System Implements the Complete Loop

No system we found implements the complete codes → scoring → rubric → lens → codes loop in a single architecture. SNOMED CT comes closest, but its "loop" operates across different organisations, timescales, and governance structures — it is not a single self-contained system. OpenRS runs its refinement loop during training, not as a continuous production process. IBM's reuse metrics informed manual curation decisions, not automated code refinement.

Each piece is proven independently. The integration is our hypothesis. We cannot cite a production system that does what we are proposing because, to our knowledge, one does not exist.

### 6.2 Lens-Adaptive Weighting Has Limited Empirical Validation

The lens-adaptive weighting of rubric criteria has limited empirical validation outside of LLM evaluation contexts. Vertex AI's adaptive rubrics route to pre-configured rubric sets per task type — the weightings are set by humans, not learned from outcomes. OpenRS's domain meta rubrics are refined through human-in-the-loop error analysis, not automatically adapted. RAISE shows that different domains produce different scores, but does not automatically adjust weights.

The Brunswik lens model provides the theoretical framework, and the diffusion lens model shows that sensitivity to ecological validity increases over time — but these are cognitive models, not system architectures. Translating the cognitive insight into a production system requires engineering decisions we have not yet made.

### 6.3 The Pudding Angle Is Uncharted

Code co-occurrence as a discovery mechanism — the Pudding technique's promise — has parallels in medical comorbidity research, where unexpected co-occurrence of diagnosis codes has led to identification of previously unknown disease relationships. However, this has not been tested with a compressed coding system in a knowledge management context. The codes in medical informatics are assigned by trained clinicians following strict protocols. Our codes are assigned by AI agents following constitutional rules. The quality and consistency of assignment may differ significantly, which would affect the reliability of co-occurrence signals.

### 6.4 Overhead Has Not Been Estimated

The overhead of maintaining the scoring layer — computing metrics, running meta-assessments, adjusting lens weightings, propagating changes — has not been estimated. It may be trivial: the Curators already log everything, and computing frequency and co-occurrence matrices from existing logs is a standard database operation. Or it may introduce latency that conflicts with SLA commitments: if every write operation triggers metric recomputation, and every metric change triggers rubric re-evaluation, the cascade could be expensive.

We suspect the overhead is manageable because the scoring layer reads from audit logs (which already exist) and writes to metric stores (which can be asynchronous). But suspicion is not measurement. We need to measure.

### 6.5 Flywheel Convergence Is Unproven

Whether the flywheel actually turns — whether code improvements feed back into better scoring, which feeds back into better rubrics, which feeds back into better codes — requires longitudinal observation. We cannot prove this from first principles.

It is possible that the loop converges to a fixed point quickly and then provides no further improvement. It is possible that the loop oscillates rather than converging. It is possible that improvements in one layer are offset by regressions in another. These are all failure modes that only longitudinal measurement can detect or rule out.

### 6.6 Human Oversight Requirements Are Undefined

OpenRS explicitly includes human-in-the-loop oversight for meta-rubric refinement. SNOMED CT changes go through extensive governance. SHSU's meta-assessment is performed by trained assessors. Every successful meta-scoring system we found includes human oversight at critical decision points.

We have not defined where human oversight is required in our loop. Which refinements can be automated? Which require human approval? What happens when the automated system proposes a code deprecation that a domain expert would dispute? These governance questions are not addressed by this hypothesis — they will need to be addressed before implementation.

### 6.7 Scale Effects Are Unknown

All the evidence cited in this document comes from systems operating at specific scales. SNOMED CT has ~370,000 concepts. IBM's reuse library had thousands of components. The knowledge graphs evaluated by Zhang & Xiao had hundreds to thousands of entities. OpenRS was evaluated on standard benchmarks with thousands of examples.

We do not know how the scoring layer behaves at our scale. If the Amplified system has hundreds of codes and thousands of nodes, the metrics may be statistically meaningful. If it has fewer, we may lack the sample sizes for reliable co-occurrence analysis or gate pass rate comparisons. Conversely, if the system grows to millions of nodes, the computational cost of maintaining the full co-occurrence matrix may become significant.

The validation plan addresses this implicitly (Phase 1 will reveal whether we have enough data for meaningful metrics), but it is worth stating explicitly: the scoring layer's utility is scale-dependent, and we need to characterise our current scale before assuming the literature's results transfer.

### 6.8 The Evidence Base Is Heterogeneous

Our evidence comes from very different domains: clinical terminology, software engineering, knowledge graphs, LLM evaluation, educational assessment, and impact measurement. Each domain has its own conventions, constraints, and success criteria. The fact that codes-as-scores works in healthcare does not guarantee it works in knowledge management. The fact that meta-rubrics work in LLM evaluation does not guarantee they work for our gate system.

We have tried to identify the common principles (countability, measurability, iterative refinement) that transfer across domains. But transfer is itself a hypothesis that requires validation. The validation plan is designed to test transfer, not assume it.

---

## 7. PROPOSED VALIDATION PLAN

How to test the hypothesis. Structured as phases with increasing ambition, each phase providing evidence for or against the hypothesis before committing to the next.

### Phase 1: Extract Existing Metrics

**Objective:** Prove that the scoring layer is computationally extractable from existing data.

**Method:** Have Kaizen compute the following from existing Curator audit logs:
- Reuse frequency per code (count of nodes carrying each code)
- Code co-occurrence matrix (which codes appear together, with frequency)
- Decay rate per code (time since last assignment)
- Code velocity per domain (rate of new code creation over time)

**Success criterion:** Metrics are computable, meaningful (not all uniform), and reveal expected patterns (e.g., core domain codes have high frequency; niche codes have low frequency).

**Failure criterion:** Metrics are uncomputable (data not structured correctly), uniform (no discriminating power), or nonsensical (patterns do not match domain knowledge).

**Estimated effort:** 1 week.  
**Risk:** Low — this is a read-only analysis of existing data.

### Phase 2: Gate Effectiveness Audit

**Objective:** Determine whether the 7 gates (G1–G7) have measurable, differential effectiveness.

**Method:** For each gate, compute:
- Pass rate (what percentage of nodes pass this gate?)
- Conditional pass rate (what is the pass rate of G(n+1) given G(n) pass?)
- Correlation with downstream quality (do nodes that barely pass a gate have lower downstream quality than nodes that pass easily?)
- Per-criterion decomposition (which specific criteria within each gate are doing the most work?)

**Success criterion:** Gates show differential pass rates, some gates are strongly predictive of downstream quality, and per-criterion analysis identifies the most discriminating criteria.

**Failure criterion:** All gates have near-100% pass rates (not discriminating), or gate results do not correlate with any downstream quality measure.

**Estimated effort:** 2 weeks.

**Downstream quality definition:** For Phase 2 and subsequent phases, "downstream quality" is defined as a composite of three measurable outcomes: (a) retrieval precision — when a code-tagged node is returned in response to a query, does it actually answer the question? Measured by expert evaluation of a sample of retrieval results. (b) Reuse rate — are nodes that pass gates actually used in downstream pipelines, recipes, and agent responses? Measured from Curator read logs. (c) Decay resistance — do nodes that pass gates maintain their relevance over time, or do they become stale faster than average? Measured from code decay metrics. This definition is provisional and should be refined during Phase 1 based on what the existing data can support.

**Risk:** Medium — requires defining "downstream quality" and having enough data to compute meaningful correlations.

### Phase 3: Lens Prototype

**Objective:** Demonstrate that lens-adaptive evaluation produces measurably different (and better) results than uniform evaluation.

**Method:** Implement two lenses:
- **Research lens** — Weights attribution depth, source quality, and methodology codes heavily.
- **Infrastructure lens** — Weights technical compliance, error coverage, and test results heavily.

Run both lenses against the same dataset. Compare:
- Retrieval quality (do the right nodes rank higher with the appropriate lens?)
- Gate pass rates per lens (do the lenses produce different quality assessments for the same nodes?)
- Expert agreement (do domain experts agree more with lens-adapted evaluations than uniform ones?)

**Success criterion:** Lens-adapted evaluation produces measurably higher expert agreement than uniform evaluation in at least one of the two domains.

**Failure criterion:** No measurable difference between lens-adapted and uniform evaluation, or the lenses disagree with expert judgment more than the uniform approach.

**Estimated effort:** 3 weeks.  
**Risk:** Medium-high — requires careful experimental design and sufficient expert evaluation to achieve statistical significance.

### Phase 4: Flywheel Test

**Objective:** Determine whether the complete loop actually turns — whether improvements in one layer propagate to improvements in others.

**Method:** Over a 3-month period, measure:
1. Whether the scoring layer (Phase 1 metrics) produces actionable Kaizen improvements.
2. Whether those Kaizen improvements change gate pass rates (Phase 2 metrics).
3. Whether changed gate pass rates improve downstream quality.
4. Whether improved quality leads to better code assignments (closing the loop).

**Success criterion:** At least one complete turn of the loop is observable — a code-level insight leads to a gate improvement that leads to a quality improvement that leads to a code refinement.

**Failure criterion:** No complete loop is observable. Improvements in one layer do not propagate to others. The system reaches a fixed point after the first adjustment and provides no further improvement.

**Estimated effort:** 3 months.  
**Risk:** High — this is the real test. Everything before this is preparation.

### Decision Gates

After each phase, a go/no-go decision:

| Phase | Go Signal | No-Go Signal | Decision |
|-------|-----------|-------------|----------|
| Phase 1 | Metrics computable and meaningful | Metrics uncomputable or uniform | Stop if data is not there |
| Phase 2 | Gates differentially effective | All gates identical or uncorrelated with quality | Revisit gate design before proceeding |
| Phase 3 | Lens adaptation improves expert agreement | No measurable lens effect | Simplify — may not need lenses |
| Phase 4 | Complete loop observable | No propagation between layers | Hypothesis partially confirmed at best |

---

## 8. TERMINOLOGY ALIGNMENT

To ensure this hypothesis document uses terms consistently with the companion documents:

| Term in This Document | Definition | Defined In |
|----------------------|-----------|------------|
| **Compressed code** | A short, structured identifier (e.g., `FIN-REGULATORY`, `RES-METHODOLOGY`) assigned to a data object to classify its domain, type, and attributes | `ATTRIBUTION-AND-CURATION-v1` §3 |
| **Gate (G1–G7)** | A validation checkpoint that a data object must pass before it is accepted into the system | `VALIDATION-METHODOLOGY-v2` |
| **Kaizen** | The continuous improvement process that identifies and implements refinements to the system | `CODE-TAXONOMY-AND-KAIZEN-v1` |
| **Curator** | An agent responsible for maintaining data integrity, including audit logging of all code assignments and modifications | `ATTRIBUTION-AND-CURATION-v1` |
| **Lens** | A problem-context configuration that determines which evaluation criteria are weighted most heavily | New to this document (proposed) |
| **Meta-scoring** | The practice of evaluating the effectiveness of an evaluation system | New to this document (proposed) |
| **Flywheel** | The hypothesised self-improving loop: codes → scoring → rubric evaluation → lens adaptation → code refinement | New to this document (proposed) |
| **Bridge code** | A code that appears in unexpected cross-domain combinations, indicating a connection between previously unrelated knowledge areas | New to this document (proposed) |
| **Code velocity** | The rate of new code creation in a domain over time | New to this document (proposed) |
| **Ecological validity** | Brunswikian term: the degree to which a cue (code) actually predicts the criterion (quality) in a given environment (lens) | Brunswik, 1956 |

---

## 9. RELATIONSHIP TO COMPANION DOCUMENTS

This hypothesis document does not stand alone. It depends on and extends the constitutional documents:

- **ATTRIBUTION-AND-CURATION-v1** — Defines the compressed coding system (Section 3) that this hypothesis builds upon. Without the codes, there is nothing to score. Without the Curators' audit logs, there is no data to compute metrics from.

- **VALIDATION-METHODOLOGY-v2** — Defines the 7 gates (G1–G7) that serve as our rubric. This hypothesis proposes meta-scoring those gates — evaluating their effectiveness and improving them systematically.

- **CODE-TAXONOMY-AND-KAIZEN-v1** — Defines the Kaizen process that would execute the improvements identified by the scoring layer. This hypothesis provides Kaizen with a new source of actionable intelligence: code-level metrics that reveal where the taxonomy needs attention.

The relationship is:

```
ATTRIBUTION-AND-CURATION-v1     →  provides the codes
CODE-TAXONOMY-AND-KAIZEN-v1     →  provides the improvement mechanism
VALIDATION-METHODOLOGY-v2       →  provides the rubric (gates)
SCORING-UNIFICATION-HYPOTHESIS  →  proposes the measurement layer that connects them
```

If the hypothesis is validated, it would become a constitutional document — likely `SCORING-UNIFICATION-STANDARD-v1`. Until then, it remains a hypothesis — clearly marked, rigorously evidenced where evidence exists, and honestly uncertain where it does not.

### 9.1 What Changes If the Hypothesis Is Validated

If the validation plan (Section 7) produces positive results:

1. **VALIDATION-METHODOLOGY** would gain a new section on gate meta-scoring, with specific metrics and thresholds derived from Phase 2 results.
2. **CODE-TAXONOMY-AND-KAIZEN** would gain a new Kaizen input stream: code-level metrics that trigger improvement investigations automatically.
3. **ATTRIBUTION-AND-CURATION** would gain lens-adaptive audit requirements: different provenance depth requirements based on the evaluation lens.
4. A new constitutional document — **LENS-CONFIGURATION-STANDARD** — would define the available lenses, their criteria weightings, and the governance process for creating new lenses.

### 9.2 What Changes If the Hypothesis Is Refuted

If the validation plan produces negative results, the companion documents remain unchanged. However, the negative results themselves are valuable:

- If Phase 1 fails (metrics not extractable), it reveals a gap in our audit logging that should be fixed regardless of this hypothesis.
- If Phase 2 fails (gates not differential), it reveals that our validation methodology needs recalibration — a finding that improves the system even without the scoring layer.
- If Phase 3 fails (lenses don't help), it suggests that uniform evaluation may be sufficient for our context, simplifying the architecture.
- If Phase 4 fails (loop doesn't turn), it suggests that the layers are independently valuable but not synergistic — still useful, just not a flywheel.

Even refutation produces actionable intelligence. This is the value of hypothesis-driven development.

---

## 10. SUMMARY

We hypothesise that compressed codes, already present in the Amplified system, can serve as the foundation of a unified scoring mechanism that connects taxonomy management, quality evaluation, and information retrieval into a self-improving loop.

The evidence for the individual pieces is strong:

- **Codes as scores:** Proven across medical informatics (SNOMED CT), software engineering (IBM reuse metrics), knowledge graphs (entity popularity), and enterprise knowledge management (persistent identifiers with classifier tuning). Multiple independent domains, decades of practice.

- **Rubric meta-scoring:** Proven by OpenRS (+5.1 over scalar baselines on reward-modelling benchmarks), implemented in practice by SHSU (literal rubric for rubrics), validated through outcomes by Sopact (longitudinal rubric validation against programme results), and operationalised by GoDaddy (structured criteria with importance categorisation).

- **Lens-adaptive evaluation:** Theoretically grounded in Brunswik's lens model (1956, with 2026 diffusion model extension), practically implemented in Vertex AI adaptive rubrics, demonstrated across domains by RAISE, and built into OpenRS's two-level meta-rubric architecture.

The evidence for the integration — the claim that connecting these pieces through compressed codes creates a self-improving flywheel — is a hypothesis. No system we found implements the complete loop. Each piece works. Whether they work together, in our architecture, with our data, is what the validation plan is designed to test.

We are standing on the shoulders of giants. The giants proved the pieces. Our job is to prove the assembly.

The validation plan is structured so that each phase provides value even if the overall hypothesis is not confirmed:

- **Phase 1** gives us code-level metrics we do not currently have — useful regardless.
- **Phase 2** tells us which gates are effective — useful regardless.
- **Phase 3** tells us whether context-adaptive evaluation helps — useful regardless.
- **Phase 4** tells us whether the loop turns — the definitive test.

We should not wait for the full flywheel to extract value. Each phase is independently worthwhile. The flywheel is the aspiration. The phases are the plan.

This is a hypothesis, not a promise. It is the beginning of an investigation, not the end of one. We put it forward for scrutiny, challenge, and improvement — because this is so important that we've got to really get everybody's point of view on it and do good research into it.

Mathematics decides. But first, we need to do the mathematics.

---

*Document version: v2 — March 2026 — Amplified Partners*
*v2 changes: Fixed gate name alignment with VALIDATION-METHODOLOGY-v2, added non-LLM evidence for lens-adaptive evaluation (aerospace, audit, manufacturing), added convergence theory, Goodhart mitigations, cold start bootstrapping, and downstream quality definition.*
*This document is a hypothesis, not a constitutional standard. It requires validation before any claims are enacted as policy.*
*Companion documents: ATTRIBUTION-AND-CURATION-v1, VALIDATION-METHODOLOGY-v2, CODE-TAXONOMY-AND-KAIZEN-v1*

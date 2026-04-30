**AMPLIFIED PARTNERS**

**RAPID INTELLIGENCE CYCLE**

PUDDING-Speed Knowledge Update Framework

Amplified Partners --- March 2026

Operational Specification v1.0

**CONFIDENTIAL**

**TABLE OF CONTENTS**

This document is structured as follows:

Section 1: The Problem --- Why Speed Matters Now

Section 2: The Distinction --- PUDDING vs Kaizen

Section 3: The Velocity Tiers --- What Moves Fast, What Moves Slow

Section 4: The Decision Logic --- When to Reclassify

Section 5: The Evaluation Rubric --- Is This Worth Pursuing?

Section 6: The Overnight Pipeline --- Research → Test → Ship

Section 7: The Rollback Protocol

Section 8: The Data Presentation Layer

Section 9: Department Responsibilities

Section 10: Feedback Loops

Appendix A: Tier Classification Reference Table

Appendix B: Evaluation Rubric Scoring Sheet

Appendix C: Nightly Research Source List

**SECTION 1: THE PROBLEM --- WHY SPEED MATTERS NOW**

The AI landscape is not moving at one speed. It is moving at several
speeds simultaneously, and those speeds differ by orders of magnitude
depending on which layer you examine. Agent frameworks, MCP protocol
updates, tool calling conventions, and model releases change on a
cadence measured in days. Infrastructure patterns, process frameworks,
and philosophical commitments change on a cadence measured in quarters
or years.

This creates a fundamental operational challenge: one update cycle does
not fit all. A quarterly review of agent orchestration patterns would
miss three months of breaking changes, deprecated APIs, and new
capabilities. A nightly review of your business philosophy would be a
waste of time and attention.

**The Velocity Mismatch**

Consider the evidence from early 2026:

-   Microsoft released the Agent Framework release candidate in February
    2026, merging AutoGen and Semantic Kernel into a single unified
    framework --- instantly deprecating patterns that hundreds of
    projects depended on.

-   The MCP protocol moved to the Linux Foundation in December 2025 and
    published an updated roadmap in March 2026, with new working groups
    forming around transports, session handling, and server cards.

-   Google\'s A2A protocol joined the Linux Foundation in June 2025 with
    over 150 organisations participating, creating an entirely new
    inter-agent communication standard.

-   Multiple major model releases ship each month across providers.
    Open-weight models now sit within single digits of proprietary
    models on benchmarks.

> *\"A lot of LLM benchmark and performance progress will come from
> improved tooling and inference-time scaling rather than from training
> or the core model itself. It will look like LLMs are getting much
> better, but this will mainly be because the surrounding applications
> are improving.\" --- Sebastian Raschka, State of LLMs 2025*

**The Key Insight**

Most visible AI progress is coming from the TOOLING layer --- agent
frameworks, MCP, skills, orchestration --- not from the core models
themselves. This is exactly the layer that changes fastest and demands
the most vigilant monitoring.

The risk is compounding: fall behind on the tooling layer and your
agents use outdated patterns. Outdated patterns mean slower execution,
missed capabilities, and brittle integrations. The competitive
disadvantage does not accumulate linearly --- it compounds daily,
because each missed improvement is a foundation that subsequent
improvements build upon.

**The Testing Bottleneck**

> *\"The biggest bottleneck today is testing. Expect significant
> investment in agent evaluation frameworks, trajectory analysis, and
> automated quality assurance.\" --- 47Billion*

Discovery is necessary but insufficient. Every discovered improvement
must be tested, validated, and deployed safely. The pipeline from
discovery to production must be as disciplined as the research itself.

**What This Document Defines**

This document establishes the Rapid Intelligence Cycle --- a formalised
operational framework for:

-   Classifying all knowledge domains by velocity tier

-   Monitoring fast-moving domains on appropriate cadences

-   Evaluating discoveries against a rigorous rubric

-   Testing improvements overnight with full rollback capability

-   Presenting data to the business owner for informed consent

-   Shipping validated improvements into production safely

**SECTION 2: THE DISTINCTION --- PUDDING VS KAIZEN**

Amplified Partners operates two distinct improvement engines that serve
fundamentally different purposes. Understanding their separation --- and
their interaction --- is critical to operating the Rapid Intelligence
Cycle correctly.

**PUDDING: Rapid Discovery for Fast-Moving Domains**

PUDDING (derived from the Swanson ABC model adapted for business
knowledge) is a rapid discovery cycle. Its purpose is to find new
developments, evaluate them against a rubric, test them overnight, and
ship them if they pass. PUDDING is discovery-driven: it scans the
external landscape for things that might improve our capabilities.

-   Triggered by: external change (new release, new paper, new protocol)

-   Cadence: nightly for Tier 1 domains

-   Goal: identify and adopt improvements before competitors

-   Risk appetite: moderate, mitigated by overnight testing and rollback

**Kaizen: Slow Compounding for Stable Processes**

Kaizen is the slow, imperceptible, compounding improvement engine that
operates on stable processes. Two SOPs per week. Small refinements that
individually seem trivial but compound into transformative efficiency
gains over months and years. Kaizen is improvement-driven: it looks
inward at existing processes and makes them incrementally better.

-   Triggered by: internal measurement (inefficiency, friction, error
    rate)

-   Cadence: two SOPs per week, continuous

-   Goal: compound improvements to stable processes

-   Risk appetite: very low --- changes are small and reversible by
    nature

**How They Interact**

PUDDING feeds Kaizen. When a PUDDING discovery proves stable over two
weeks in production, it graduates into the Kaizen domain. The Kaizen
engine then takes ownership: refining the integration, optimising the
process, documenting the SOP, training the team. The discovery is no
longer novel --- it is an established capability that benefits from
incremental improvement.

> *PUDDING discovers. Kaizen perfects. Both are essential. They operate
> on different knowledge domains at different speeds.*

**Comparison Table**

  -------------------- -------------------------------------------------------- ------------------------------------------------------- ------------------- -------------------------- -------------
  **Dimension**        **PUDDING**                                              **Kaizen**                                              **Speed**           **Trigger**                **Owner**
  **Scope**            External landscape --- new releases, papers, protocols   Internal processes --- SOPs, workflows, documentation   Nightly to weekly   External change detected   R&D + Chaos
  **Testing Depth**    Overnight integration + performance benchmarks           A/B comparison of process variants                      Hours               Automated scan + rubric    R&D → Chaos
  **Rollback Risk**    Moderate --- new integrations may have dependencies      Low --- changes are small, reversible                   Days to weeks       Internal measurement       Kaizen dept
  **Success Metric**   Capability gap closed, competitive advantage gained      Process AMPS score increases                            Continuous          Ongoing                    Kaizen dept
  -------------------- -------------------------------------------------------- ------------------------------------------------------- ------------------- -------------------------- -------------

**SECTION 3: THE VELOCITY TIERS --- WHAT MOVES FAST, WHAT MOVES SLOW**

All knowledge domains relevant to Amplified Partners are classified into
four velocity tiers. Each tier determines the monitoring cadence,
research method, testing depth, and department ownership. These
classifications are reviewed monthly and reclassified when evidence
warrants (see Section 4).

**Tier 1 --- NIGHTLY (Changes in Days)**

These domains change so rapidly that a weekly review would miss critical
developments. Nightly automated scanning with next-day testing is
required.

  -------------------------------------- ------------------------------------------------------------------------------------------------------ ------------------ --------------------------------- --------------------------- ----------------
  **Knowledge Domain**                   **Examples of Recent Change**                                                                          **Update Cycle**   **Research Method**               **Testing Depth**           **Dept Owner**
  **Agent Frameworks & Orchestration**   MS Agent Framework RC (Feb 2026), AutoGen deprecated, OpenAI Agents SDK, CrewAI & LangGraph releases   Nightly            Blog + GitHub feed scan           Full integration test       R&D → Chaos
  **MCP Protocol**                       Linux Foundation transfer, SEPs, Server Cards, Progressive Tool Discovery, session handling            Nightly            Spec changelog + WG notes         Protocol conformance        R&D → Chaos
  **A2A / AG-UI Protocols**              A2A under Linux Foundation, 150+ orgs, AG-UI emerging standard                                         Nightly            Spec changelog                    Interop testing             R&D
  **Model Releases**                     GPT-5, Gemini 3, Claude 4, Llama 4, Qwen 3 --- multiple per month, pricing changes, deprecations       Nightly            Provider blogs + API changelogs   Benchmark + cost analysis   R&D
  **Tool Calling Conventions**           Provider-specific formatting, function schema changes, structured outputs evolution                    Nightly            SDK changelogs                    Regression suite            R&D → Chaos
  **Prompt / Context Engineering**       LangChain four strategies (write, select, compress, isolate), production vs casual split               Nightly            Blog + paper scan                 A/B quality test            R&D
  **Inference-Time Scaling**             Reasoning tokens, chain-of-thought evolution, compute-at-inference approaches                          Nightly            Papers + benchmarks               Performance benchmark       R&D
  -------------------------------------- ------------------------------------------------------------------------------------------------------ ------------------ --------------------------------- --------------------------- ----------------

**Tier 2 --- WEEKLY (Changes in Weeks)**

These domains evolve on a weekly cadence. Weekly research sweeps with
staged testing are appropriate.

  ------------------------------- -------------------------------------------------------------------------------------------------- ------------------ --------------------- ------------------------ ----------------
  **Knowledge Domain**            **Examples of Recent Change**                                                                      **Update Cycle**   **Research Method**   **Testing Depth**        **Dept Owner**
  **Embedding Models & RAG**      BGE-M3, E5-Mistral, Voyage-Multilingual-2, hybrid search standardisation, multi-index approaches   Weekly             Benchmarks + papers   Retrieval quality test   R&D
  **Vector DB Features**          FalkorDB, Qdrant, Pinecone feature releases, performance improvements                              Weekly             Release notes         Performance bench        R&D → Chaos
  **Testing / Eval Frameworks**   Self-healing tests, AI-driven test selection, drift detection maturation                           Weekly             GitHub + blog scan    Framework evaluation     Chaos
  **Observability / Tracing**     LangFuse, Opik, LangSmith --- tools maturing, standards emerging                                   Weekly             Tool comparison       Integration test         Real
  **Security Patterns**           Prompt injection defences, output filtering, auth patterns for AI                                  Weekly             Security advisories   Red team test            Chaos
  **Open-Source Releases**        Major version bumps of core dependencies, new libraries reaching maturity                          Weekly             GitHub releases       Dependency test          R&D
  ------------------------------- -------------------------------------------------------------------------------------------------- ------------------ --------------------- ------------------------ ----------------

**Tier 3 --- MONTHLY (Changes in Months)**

Stable but still evolving. Monthly review is sufficient.

  -------------------------------- ---------------------------------------------------------------------------------------- ------------------ --------------------- ----------------------- ----------------
  **Knowledge Domain**             **Examples of Recent Change**                                                            **Update Cycle**   **Research Method**   **Testing Depth**       **Dept Owner**
  **Infrastructure Patterns**      Tiered model strategy, request orchestration, graceful degradation --- stable patterns   Monthly            Architecture review   Load testing            Real
  **Data Sovereignty / Privacy**   GDPR enforcement updates, PII handling standards, UK AI regulation consultations         Monthly            Regulatory feeds      Compliance audit        Real
  **Content Strategy**             Content atomisation methodology, GaryVee pyramid, build-in-public approach               Monthly            Industry review       Content performance     Kaizen
  **Hardware / Compute**           Hetzner Beast specs, RunPod pricing, GPU generation changes                              Monthly            Vendor monitoring     Cost-benefit analysis   Real
  **Deployment Patterns**          Docker, Kubernetes, CI/CD pipeline patterns                                              Monthly            Release notes         Deployment test         Real
  -------------------------------- ---------------------------------------------------------------------------------------- ------------------ --------------------- ----------------------- ----------------

**Tier 4 --- GLACIAL (Quarters to Years)**

Foundational decisions that change rarely. Quarterly or annual review.

  -------------------------- ---------------------------------------------------------------------------------- ------------------ --------------------- ----------------------- ----------------
  **Knowledge Domain**       **Examples**                                                                       **Update Cycle**   **Research Method**   **Testing Depth**       **Dept Owner**
  **Core Philosophy**        Eight Laws, Ulysses Clause, Libertarian Paternalism --- foundational commitments   Annual             Strategic review      N/A --- philosophical   Leadership
  **Business Model**         Pricing structure, partnership model, voice-first principle                        Quarterly          Market analysis       Financial modelling     Leadership
  **Design Decisions**       Voice-first interaction, data sovereignty architecture, SMB focus                  Annual             Strategic review      User research           Leadership
  **Legal / Compliance**     UK AI regulation, GDPR enforcement, ICO guidance                                   Quarterly          Legal monitoring      Legal review            Real
  **Classical Frameworks**   CMMI, DMAIC, PDCA, TOC --- established process science                             Annual             Academic review       N/A --- stable          Kaizen
  -------------------------- ---------------------------------------------------------------------------------- ------------------ --------------------- ----------------------- ----------------

**SECTION 4: THE DECISION LOGIC --- WHEN TO RECLASSIFY**

Knowledge domains are not permanently assigned to a tier. As the
landscape evolves, domains accelerate or stabilise. The Rapid
Intelligence Cycle includes a formal reclassification process that runs
monthly, with emergency reclassification available at any time.

**Signals of Acceleration (Move to a Faster Tier)**

-   Release frequency increases --- more than 2× the expected cadence
    for the current tier

-   Breaking changes appear --- backward-incompatible updates that
    require immediate response

-   New competitors adopting --- widespread industry adoption signals
    the domain is active and consequential

-   Multiple providers releasing simultaneously --- indicates a
    coordination point or inflection

-   Standards bodies forming --- working groups, RFCs, or SEPs indicate
    rapid formalisation

-   Community activity spike --- GitHub stars, issues, and PRs
    significantly above baseline

**Signals of Stabilisation (Move to a Slower Tier)**

-   Release cadence decreasing --- fewer updates, longer intervals
    between versions

-   Standards consolidating --- dominant patterns emerging, alternatives
    being deprecated

-   Breaking changes rare --- API stability, backward compatibility
    maintained

-   Documentation maturing --- comprehensive guides, best practices
    well-established

-   Industry consensus forming --- broad agreement on approaches, less
    experimentation

-   Vendor consolidation --- fewer active competitors, market leaders
    established

**Monthly Review Cadence**

On the first Monday of each month, the R&D department reviews all tier
assignments:

-   Review the release log for each knowledge domain over the past 30
    days

-   Count significant changes (breaking changes, major releases, new
    capabilities)

-   Compare to expected cadence for the current tier

-   Propose reclassifications with evidence

-   Reclassifications take effect immediately upon approval

**Reclassification Triggers**

  --------------------------------------------------- --------------- --------------------------------------------
  **Trigger**                                         **Direction**   **Action**
  3+ breaking changes in 30 days                      Accelerate ↑    Move up one tier immediately
  Major new standard announced (e.g., new protocol)   Accelerate ↑    Move to Tier 1 for 30-day evaluation
  No significant changes in 60 days                   Stabilise ↓     Move down one tier at next review
  Industry standard published (RFC, W3C, etc.)        Stabilise ↓     Review for potential tier reduction
  Vendor acquired / project archived                  Emergency       Immediate review, potential migration plan
  Security vulnerability discovered                   Emergency ↑     Elevate to Tier 1 until resolved
  --------------------------------------------------- --------------- --------------------------------------------

**SECTION 5: THE EVALUATION RUBRIC --- IS THIS WORTH PURSUING?**

When nightly research discovers something new, the evaluation rubric
determines whether to invest time in testing it. This prevents resource
waste on immature, irrelevant, or low-quality developments while
ensuring that genuinely important improvements are not missed.

> *\"If it\'s brand new and it\'s sparse, it might not be worth it.\"
> Filtering logic is essential --- not every development deserves
> attention.*

**Scoring Dimensions**

Each dimension is scored 0--10. The composite score is a weighted
average.

  -------------------------------- ------------ ---------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------
  **Dimension**                    **Weight**   **Scoring Guide**
  **1. Relevance to Goals**        20%          Does this advance Amplified Partners\' specific objectives? Voice-first interaction, SMB focus, data sovereignty, process improvement. Score 10 if directly aligned with core mission; 5 if tangentially useful; 0 if irrelevant.
  **2. Methodology Maturity**      15%          Is this from a major lab (pre-validated) or a random blog post? Anthropic / OpenAI / Google core releases get automatic 8.0 --- they won\'t publish unless it\'s right. Academic papers with peer review: 6-8. Community projects: 3-6. Unverified blog posts: 0-3.
  **3. Integration Feasibility**   15%          How hard is it to integrate with existing stack? The Beast, FalkorDB, Docker containers, LangGraph. Drop-in replacement: 9-10. Moderate refactoring: 5-7. Architectural rework: 1-3.
  **4. Evidence Quality**          15%          Are there benchmarks? Real-world tests? Reproducible results? Published benchmarks from independent sources: 8-10. Provider-published benchmarks: 6-8. Anecdotal evidence: 2-4. Marketing claims only: 0-2.
  **5. Risk Profile**              15%          What breaks if this goes wrong? Reversibility? Data safety? Fully reversible, no data risk: 9-10. Reversible with effort: 5-7. Potential data loss or corruption: 1-3.
  **6. Competitive Advantage**     10%          Does adopting this create meaningful differentiation? First-mover in SMB AI space: 8-10. Incremental improvement: 4-6. Table stakes (everyone will adopt): 2-4.
  **7. Cost-Benefit**              10%          Development time vs. expected improvement. RunPod burst cost if GPU needed. \< 2 hours implementation, significant improvement: 9-10. Days of work, moderate improvement: 4-6. Weeks of work, marginal improvement: 0-3.
  -------------------------------- ------------ ---------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------

**Scoring Thresholds**

-   **≥ 7.0:** Proceed to overnight testing. High confidence this is
    worth pursuing.

-   **5.0 -- 6.9:** Flag for manual review. Promising but needs human
    judgement on trade-offs.

-   **\< 5.0:** Archive with reasoning. Do not pursue. May be revisited
    if conditions change.

**Special Rule:** Major lab releases (Anthropic, OpenAI, Google core
updates) receive an automatic 8.0 on Methodology Maturity. These
organisations have sufficient internal validation that their published
work is reliable. This does not bypass other dimensions --- a Google
release that is irrelevant to our goals still scores low on Relevance.

**Worked Example: MCP Server Cards Specification**

The MCP specification publishes a new Server Cards standard, enabling
servers to describe their capabilities in a machine-readable format.
Here is how it scores:

  ------------------------- ----------- ---------------------------------------------------------------------------------------------------------------------------------------------------------
  **Dimension**             **Score**   **Reasoning**
  Relevance to Goals        9           Directly enables progressive tool discovery for our agents. Core to voice-first SMB interaction where agents must discover available tools dynamically.
  Methodology Maturity      8           Published through the MCP SEP process under Linux Foundation governance. Pre-validated by working group review.
  Integration Feasibility   7           Our MCP servers can add server card metadata without architectural changes. Some refactoring of discovery logic needed in the orchestration layer.
  Evidence Quality          7           Specification is formal with reference implementations. No independent benchmarks yet, but spec quality is high.
  Risk Profile              8           Additive change --- adds capability without modifying existing functionality. Fully reversible by removing metadata.
  Competitive Advantage     8           Early adoption of server cards enables dynamic agent capabilities before competitors implement. First-mover advantage in SMB market.
  Cost-Benefit              8           Estimated 4 hours implementation. Enables significant new capability for agent discovery and routing.
  ------------------------- ----------- ---------------------------------------------------------------------------------------------------------------------------------------------------------

**Composite Score:** (9×0.20) + (8×0.15) + (7×0.15) + (7×0.15) +
(8×0.15) + (8×0.10) + (8×0.10) = 1.80 + 1.20 + 1.05 + 1.05 + 1.20 + 0.80
+ 0.80 = 7.90

**Decision:** Proceed to overnight testing. Score exceeds 7.0 threshold.

**SECTION 6: THE OVERNIGHT PIPELINE --- RESEARCH → TEST → SHIP**

The Rapid Intelligence Cycle operates as a five-phase pipeline that runs
from 22:00 through the following morning. Each phase has defined inputs,
outputs, and gates that must be passed before proceeding.

**Phase 1: DISCOVER (Automated --- 22:00)**

Automated research agents scan a curated set of high-signal sources:

-   Anthropic Blog, OpenAI Blog, Google AI Blog

-   MCP Specification Changelog and GitHub releases

-   A2A and AG-UI protocol repositories

-   GitHub release feeds for tracked dependencies

-   Hacker News front page (filtered for AI/ML relevance)

-   Key Substacks (Simon Willison, Lilian Weng, Chip Huyen, Sebastian
    Raschka)

-   arXiv AI/ML new submissions (cs.AI, cs.CL, cs.LG)

Each finding is classified by velocity tier. Tier 1 findings proceed
immediately to Phase 2.

**Phase 2: EVALUATE (Automated + Human Gate --- 22:30)**

Findings are scored against the evaluation rubric (Section 5):

-   **Score ≥ 7.0:** Proceed automatically to Phase 3 (overnight
    testing).

-   **Score 5.0--6.9:** Queued for morning review. No automated action.

-   **Score \< 5.0:** Archived with scoring reasoning. No further action
    unless conditions change.

Human gate: Ewan can override any automated decision via mobile
notification. High-priority findings (score ≥ 9.0) trigger an immediate
push notification regardless of time.

**Phase 3: TEST (Automated --- 00:00--06:00)**

Approved findings enter the overnight testing environment:

-   Staging environment on The Beast --- separate Docker network
    isolated from production

-   Full integration tests against existing stack components

-   Performance benchmarks comparing new approach vs. current approach

-   Rollback procedure pre-loaded before any change is applied

-   All test results logged with full metrics, timestamps, and
    environment state

-   Chaos Department adversarial inputs applied where applicable

If any test fails catastrophically, the testing pipeline halts and the
staging environment is automatically rolled back.

**Phase 4: PRESENT (Morning --- 07:00)**

Test results are compiled into a data presentation for Ewan:

-   What was found: discovery summary with source links

-   Rubric scores: full breakdown across all seven dimensions

-   Test results: pass/fail matrix with specific metrics

-   Comparison: current approach vs. new approach with quantified
    differences

-   Recommendation: ship / iterate / archive with confidence level

-   Rollback button: always visible, always one click away

The presentation follows the Libertarian Paternalism principle: the AI
optimises the route, the owner chooses the destination.

**Phase 5: SHIP (After Approval)**

Upon owner approval:

-   Deploy to production with feature flag (disabled by default)

-   Enable feature flag for 10% of traffic (canary deployment)

-   Monitor for 4 hours at 10% traffic

-   If stable, ramp to 50%, then 100% over 24 hours

-   If stable at 100% for 24 hours, remove feature flag

-   Update documentation and SOPs

-   Update AMPS process scores

-   Generate content atom for build-in-public

**Pipeline Summary**

  ----------------- ---------------- --------------------------------------------------- ------------------------------------------ --------------------------------
  **Phase**         **Timing**       **Activities**                                      **Tools**                                  **Gate**
  **1. Discover**   22:00            Scan sources, classify by tier, extract findings    Research agents, RSS feeds, API monitors   Tier classification complete
  **2. Evaluate**   22:30            Score findings against rubric, route by threshold   Rubric engine, notification system         Score ≥ 7.0 to proceed
  **3. Test**       00:00--06:00     Integration tests, benchmarks, adversarial inputs   Docker staging, test harness, The Beast    All tests pass, no regressions
  **4. Present**    07:00            Compile results, build comparison, recommendation   Reporting engine, dashboard                Owner review + approval
  **5. Ship**       After approval   Feature flag deploy, canary, ramp, monitor          Docker, feature flags, monitoring          24h stability at 100%
  ----------------- ---------------- --------------------------------------------------- ------------------------------------------ --------------------------------

**SECTION 7: THE ROLLBACK PROTOCOL**

Every change deployed through the Rapid Intelligence Cycle has a
pre-written rollback procedure. This is not optional. Rollback
capability is a prerequisite for deployment, not an afterthought.

**Rollback Architecture**

-   **Docker Container Snapshots:** Before any deployment, the current
    production container state is snapshot and tagged with the
    deployment ID. Rollback restores the exact previous state.

-   **Feature Flags:** All new integrations deploy behind feature flags.
    The flag can be disabled instantly, reverting to previous behaviour
    without container changes.

-   **Database Migrations:** All schema changes include a paired
    down-migration. No forward-only migrations permitted.

-   **Configuration Versioning:** All configuration changes are
    versioned. Previous versions are retained for 90 days.

**24-Hour Monitoring Period**

After deployment reaches 100% traffic:

-   Continuous monitoring of error rates, latency, accuracy, and
    resource utilisation

-   Comparison against 7-day rolling baseline for all metrics

-   Automated alerts if any metric deviates more than 2 standard
    deviations from baseline

-   Human review at 4-hour, 12-hour, and 24-hour checkpoints

**Automatic Rollback Triggers**

The system will automatically initiate rollback if any of the following
conditions are detected:

-   Error rate exceeds 2× baseline for more than 5 minutes

-   P95 latency exceeds 3× baseline for more than 5 minutes

-   Accuracy metric drops below defined threshold for the affected
    component

-   Memory usage exceeds 90% of container allocation

-   Any data integrity check fails

**Post-Rollback Review**

Every rollback triggers a structured review:

-   Root cause analysis: what specifically failed and why

-   Rubric calibration: does this failure suggest a rubric dimension
    needs reweighting?

-   Test gap analysis: what test would have caught this before
    deployment?

-   Documentation update: add the failure mode to the Chaos
    Department\'s test library

-   Reclassification review: does this change the risk profile of the
    knowledge domain?

**SECTION 8: THE DATA PRESENTATION LAYER**

When a tested improvement is ready for production deployment, the
business owner is presented with data --- not a fait accompli. The owner
does not receive \"we changed something.\" The owner receives \"here is
what we found, here is the evidence, here is what it means for your
business, and here is our recommendation.\"

> *AI optimises the route. The owner chooses the destination. This is
> the Libertarian Paternalism principle in action.*

**Presentation Template**

  ---------------------------- ------------------------------------------------------------------------------------------------------------------------------------------------
  **Component**                **Content**
  **Discovery Summary**        What was found, where it came from, why it matters. Plain language, no jargon.
  **Before / After Metrics**   Specific, quantified comparison. e.g., \'Response latency: 340ms → 180ms (47% improvement)\' or \'Retrieval accuracy: 82% → 91% on gold set\'.
  **Confidence Level**         Based on test coverage and evidence quality. High / Medium / Low with reasoning.
  **Risk Assessment**          What could go wrong, likelihood, impact, mitigation. Aligned with rubric Risk Profile score.
  **Cost Impact**              Any change in ongoing costs --- compute, API usage, storage. RunPod burst cost if applicable.
  **Recommendation**           Ship / Iterate / Archive. Clear, unambiguous, with reasoning.
  **Rollback Plan**            One-sentence description of how to reverse the change if problems emerge post-deployment.
  ---------------------------- ------------------------------------------------------------------------------------------------------------------------------------------------

**Owner Consent Protocol**

Production deployment requires explicit owner consent. The system
presents the data, the recommendation, and the rollback plan. The owner
then selects one of three options:

-   **Approve:** Deployment proceeds through the feature-flag pipeline
    described in Section 6.

-   **Defer:** Finding is queued for later review. The system will
    re-present after 48 hours with any additional data gathered.

-   **Reject:** Finding is archived. Reasoning is recorded for rubric
    calibration feedback.

No deployment proceeds without one of these explicit choices. Silent
defaults do not exist.

**SECTION 9: DEPARTMENT RESPONSIBILITIES**

The Rapid Intelligence Cycle maps directly onto Amplified Partners\'
four-department structure. Each department owns specific phases of the
pipeline, ensuring clear accountability and preventing gaps.

  ---------------- ----------------------------------------- -------------------------------------------------------------------------------------------------------------------------------------------------------------- -----------------------------------------------------------------------------------------------------
  **Department**   **Pipeline Phase**                        **Responsibilities**                                                                                                                                           **Key Outputs**
  **R&D**          Phase 1 (Discover) + Phase 2 (Evaluate)   Scans the external landscape. Classifies findings by tier. Scores findings against the evaluation rubric. Maintains the source list and tier assignments.      Scored findings, tier classification updates, source list maintenance, rubric calibration proposals
  **Chaos**        Phase 3 (Test)                            Runs overnight testing. Designs adversarial inputs. Stress-tests new integrations. Identifies edge cases and failure modes. Maintains the test library.        Test results, failure mode documentation, adversarial test cases, performance benchmarks
  **Kaizen**       Phase 5 (Ship) post-stabilisation         Once a PUDDING discovery proves stable over 2 weeks in production, Kaizen absorbs it. Refines integration, optimises processes, documents SOPs, trains team.   Updated SOPs, process documentation, AMPS score updates, training materials
  **Real**         Phase 5 (Ship) monitoring                 Owns production monitoring during deployment. Watches for drift, degradation, incidents. Triggers automatic rollback when thresholds are breached.             Monitoring dashboards, incident reports, drift detection alerts, rollback execution
  ---------------- ----------------------------------------- -------------------------------------------------------------------------------------------------------------------------------------------------------------- -----------------------------------------------------------------------------------------------------

**Cross-Department Handoffs**

Clear handoff protocols ensure no gap between departments:

-   **R&D → Chaos:** Scored findings with rubric breakdown, relevant
    documentation, and integration notes.

-   **Chaos → Present:** Full test results with pass/fail matrix,
    performance metrics, and failure mode analysis.

-   **Present → Ship (Real):** Owner approval confirmation, deployment
    plan, rollback procedure, monitoring thresholds.

-   **Real → Kaizen:** After 2-week stability confirmation, handoff of
    production integration with performance baseline for Kaizen to
    optimise.

**SECTION 10: FEEDBACK LOOPS**

The Rapid Intelligence Cycle is a learning system. Every outcome ---
successful deployment, rejected finding, rollback --- feeds back into
the system to improve future decisions.

**Content Generation Loop**

Every shipped change generates a content atom for build-in-public. This
serves three purposes:

-   Transparency: clients and prospects see the rate of improvement

-   Authority: demonstrates deep technical competence in the SMB AI
    space

-   Documentation: creates a public log of capability evolution

Content atoms follow the established content atomisation framework --- a
single discovery can generate a blog post, a social media thread, a
video script, and a technical note.

**Rubric Calibration Loop**

Every rejected finding feeds back into rubric calibration:

-   If a rejected finding later proves to be important (competitor
    adopts it, becomes standard), the rubric weights are reviewed

-   If approved findings frequently fail testing, the relevant rubric
    dimensions may be under-weighted

-   Calibration data is accumulated and reviewed on the quarterly
    cadence

**Review Cadences**

  --------------- --------------------------------------------------------------------------------------------------------------------------------------------- -----------------------------------------------
  **Cadence**     **Review Scope**                                                                                                                              **Output**
  **Monthly**     Are the tier assignments still correct? Review release logs, count significant changes, compare to expected cadence.                          Updated tier assignments with evidence
  **Quarterly**   Is the rubric weighting still appropriate? Review calibration data, false positives/negatives, rollback frequency.                            Updated rubric weights, threshold adjustments
  **Annual**      Fundamental reassessment. What does \"fast-moving\" mean now? Are the four tiers still the right structure? Is the pipeline timing optimal?   Revised framework version (e.g., v2.0)
  --------------- --------------------------------------------------------------------------------------------------------------------------------------------- -----------------------------------------------

**Continuous Improvement Metrics**

The following metrics are tracked to measure the health of the Rapid
Intelligence Cycle itself:

-   Discovery hit rate: percentage of Tier 1 findings that score ≥ 7.0
    on the rubric

-   Test pass rate: percentage of tested findings that pass overnight
    testing

-   Ship rate: percentage of tested findings that reach production

-   Rollback rate: percentage of shipped changes that require rollback

-   Time-to-production: hours from discovery to production deployment

-   Rubric accuracy: correlation between rubric score and production
    outcome

-   Tier accuracy: percentage of domains correctly classified (validated
    by actual change frequency)

**APPENDIX A: TIER CLASSIFICATION REFERENCE TABLE**

Complete classification of all monitored knowledge domains as of March
2026. This table is reviewed monthly and updated when reclassification
is warranted.

  -------------------------------------------------- ------------------ ----------------- ---------------------------------------------------------------------------------------------
  **Knowledge Domain**                               **Current Tier**   **Last Review**   **Classification Evidence**
  **Agent Frameworks & Orchestration**               Tier 1             March 2026        MS Agent Framework RC Feb 2026, AutoGen deprecated, monthly new framework releases
  **MCP Protocol**                                   Tier 1             March 2026        Linux Foundation transfer Dec 2025, active SEPs, working groups forming March 2026
  **A2A / AG-UI Protocols**                          Tier 1             March 2026        A2A Linux Foundation June 2025, 150+ orgs, AG-UI specification emerging
  **Model Releases & Capabilities**                  Tier 1             March 2026        Multiple major releases per month, GPT-5, Gemini 3, Claude 4, Llama 4, Qwen 3 all active
  **Tool Calling Conventions**                       Tier 1             March 2026        Evolving with each model release, provider-specific differences, structured outputs
  **Prompt / Context Engineering**                   Tier 1             March 2026        LangChain formalised 4 strategies, production vs casual split emerging
  **Inference-Time Scaling**                         Tier 1             March 2026        Major 2026 focus area, reasoning tokens, chain-of-thought evolution
  **Embedding Models & RAG Patterns**                Tier 2             March 2026        Landscape mature but evolving --- BGE-M3, multi-index emerging, hybrid search standardising
  **Vector Database Features**                       Tier 2             March 2026        Feature sets stabilising, performance improving, FalkorDB/Qdrant/Pinecone active
  **Testing / Evaluation Frameworks**                Tier 2             March 2026        Biggest bottleneck per industry, self-healing tests emerging, drift detection maturing
  **Observability / Tracing Tooling**                Tier 2             March 2026        LangFuse, Opik, LangSmith maturing, standards emerging
  **Security Patterns for AI**                       Tier 2             March 2026        Prompt injection defences evolving, output filtering patterns developing
  **Open-Source Library Releases**                   Tier 2             March 2026        Major dependencies release on weekly-to-monthly cadence
  **Infrastructure Architecture Patterns**           Tier 3             March 2026        Tiered model strategy, graceful degradation --- patterns stable
  **Data Sovereignty / Privacy Regulations**         Tier 3             March 2026        GDPR enforcement slow, UK AI regulation in consultation phase
  **Content Strategy Methodology**                   Tier 3             March 2026        Content atomisation, build-in-public approach well-established
  **Hardware / Compute Pricing**                     Tier 3             March 2026        Hetzner specs stable, RunPod pricing slow-moving, GPU annual cycles
  **Deployment Patterns (Docker, K8s)**              Tier 3             March 2026        Container patterns well-established, incremental improvements only
  **Core Philosophy (Eight Laws, Ulysses Clause)**   Tier 4             March 2026        Foundational commitments, unchanged since establishment
  **Business Model & Pricing Structure**             Tier 4             March 2026        Partnership model, pricing tiers --- strategic, not operational
  **Fundamental Design Decisions**                   Tier 4             March 2026        Voice-first, data sovereignty, SMB focus --- core identity
  **Legal / Compliance Frameworks**                  Tier 4             March 2026        UK AI Act, GDPR --- regulatory pace measured in years
  **Classical Process Frameworks**                   Tier 4             March 2026        CMMI, DMAIC, PDCA, TOC --- established science, decades stable
  -------------------------------------------------- ------------------ ----------------- ---------------------------------------------------------------------------------------------

**APPENDIX B: EVALUATION RUBRIC SCORING SHEET**

Use this template to score any new development discovered through the
Rapid Intelligence Cycle.

**Development:**
\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_

**Source:**
\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_

**Date Discovered:**
\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_

**Discovered By:**
\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_

**Velocity Tier:**
\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_

  -------------------------------------- ------------------ ---------------
  **Dimension (Weight)**                 **Score (0-10)**   **Reasoning**
  **1. Relevance to Goals (20%)**                           
  **2. Methodology Maturity (15%)**                         
  **3. Integration Feasibility (15%)**                      
  **4. Evidence Quality (15%)**                             
  **5. Risk Profile (15%)**                                 
  **6. Competitive Advantage (10%)**                        
  **7. Cost-Benefit (10%)**                                 
  -------------------------------------- ------------------ ---------------

**Composite Score:** \_\_\_\_\_\_\_\_\_\_ (weighted average)

**Decision:**

-   [ ] ≥ 7.0 --- Proceed to overnight testing

-   [ ] 5.0--6.9 --- Flag for manual review

-   [ ] \< 5.0 --- Archive (do not pursue)

**Special Rules Applied:**

-   [ ] Major lab release --- Automatic 8.0 on Methodology Maturity

**Reviewer Signature:**
\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_

**Date:**
\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_

**APPENDIX C: NIGHTLY RESEARCH SOURCE LIST**

All sources monitored by the automated research agents during Phase 1
(Discover). Sources are reviewed monthly and updated when new
high-signal sources are identified or existing sources become inactive.

**Primary Sources --- Checked Nightly**

  ----------------------------- ----------------------------------------------- --------------- -------------------
  **Source**                    **URL**                                         **Frequency**   **Tier Coverage**
  **Anthropic Blog**            anthropic.com/blog                              Nightly         Tier 1
  **OpenAI Blog**               openai.com/blog                                 Nightly         Tier 1
  **Google AI Blog**            blog.google/technology/ai                       Nightly         Tier 1
  **MCP Spec Changelog**        github.com/modelcontextprotocol/specification   Nightly         Tier 1
  **MCP GitHub Releases**       github.com/modelcontextprotocol                 Nightly         Tier 1
  **A2A Protocol Repo**         github.com/google/a2a                           Nightly         Tier 1
  **Hacker News (AI filter)**   news.ycombinator.com                            Nightly         Tier 1-2
  **arXiv cs.AI**               arxiv.org/list/cs.AI/new                        Nightly         Tier 1-2
  **arXiv cs.CL**               arxiv.org/list/cs.CL/new                        Nightly         Tier 1-2
  **arXiv cs.LG**               arxiv.org/list/cs.LG/new                        Nightly         Tier 1-2
  ----------------------------- ----------------------------------------------- --------------- -------------------

**Substacks & Newsletters --- Checked Nightly**

  --------------------------- ------------------------------- --------------- -------------------
  **Author / Publication**    **URL**                         **Frequency**   **Tier Coverage**
  **Simon Willison**          simonwillison.net               Nightly         Tier 1-2
  **Lilian Weng**             lilianweng.github.io            Nightly         Tier 1-2
  **Chip Huyen**              huyenchip.com/blog              Nightly         Tier 1-2
  **Sebastian Raschka**       magazine.sebastianraschka.com   Nightly         Tier 1-2
  **The Batch (Andrew Ng)**   deeplearning.ai/the-batch       Nightly         Tier 1-2
  **Ahead of AI (Raschka)**   magazine.sebastianraschka.com   Nightly         Tier 1-2
  --------------------------- ------------------------------- --------------- -------------------

**GitHub Release Feeds --- Checked Nightly**

  -------------------------- -------------------------------------------- --------------- -------------------
  **Repository**             **URL**                                      **Frequency**   **Tier Coverage**
  **LangGraph**              github.com/langchain-ai/langgraph            Nightly         Tier 1
  **LangChain**              github.com/langchain-ai/langchain            Nightly         Tier 1
  **CrewAI**                 github.com/crewai/crewai                     Nightly         Tier 1
  **OpenAI Python SDK**      github.com/openai/openai-python              Nightly         Tier 1
  **Anthropic Python SDK**   github.com/anthropics/anthropic-sdk-python   Nightly         Tier 1
  **FalkorDB**               github.com/FalkorDB/FalkorDB                 Nightly         Tier 2
  **Qdrant**                 github.com/qdrant/qdrant                     Weekly          Tier 2
  **LangFuse**               github.com/langfuse/langfuse                 Weekly          Tier 2
  -------------------------- -------------------------------------------- --------------- -------------------

**Weekly Review Sources**

  ------------------------ ----------------------------------- --------------- -------------------
  **Source**               **URL**                             **Frequency**   **Tier Coverage**
  **OWASP AI Security**    owasp.org/www-project-ai-security   Weekly          Tier 2
  **Docker Blog**          docker.com/blog                     Weekly          Tier 2-3
  **Kubernetes Blog**      kubernetes.io/blog                  Weekly          Tier 2-3
  **ICO Guidance (UK)**    ico.org.uk/for-organisations        Monthly         Tier 3
  **FSB Policy Updates**   fsb.org.uk/policy                   Monthly         Tier 3
  ------------------------ ----------------------------------- --------------- -------------------

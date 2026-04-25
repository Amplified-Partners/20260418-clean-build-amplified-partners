---
title: "Curator Assessment v1"
id: "curator-assessment-v1"
version: 1
created: 2026-04-25
last_validated: 2026-04-25
type: document
topic_type: reference
status: imported
source_file: "amplified-curator-assessment-v1.docx"
signed_by: "Devon, 2026-04-25, devin-992682c244cf444f91e0a516498afbfd"
---

**AMPLIFIED PARTNERS**

**Curator Agent +**

**Reusable Component Library**

Strategic Assessment + Design Blueprint

  --
  --

Version 1.0 \| 17 March 2026

PUDDING Label: S.=.4.m (State, Stable, Team-scale, Medium-term)

Hypothesis: Untested \| Confidence: High (pending build)

Contents

Executive Verdict

+---------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------+
| **Is it worthwhile?**                                                                                                                                                                                                                                                                                                                                                                                                                                                                       |
|                                                                                                                                                                                                                                                                                                                                                                                                                                                                                             |
| Yes. Emphatically. This is one of the highest-leverage investments Amplified can make. Every hour spent building the Curator and Component Library saves multiples of that across every future build, every client onboarding, and every agent team that would otherwise rebuild what already exists. The entire industry is converging on this pattern --- Spotify built Backstage for exactly this reason. The only organisations NOT doing this are the ones drowning in duplicate work. |
+---------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------+

The concept maps directly to three of Ewan\'s core principles:

-   **Don\'t build twice:** The Component Library is the physical embodiment of this rule. Every reusable pattern, workflow, prompt template, rubric, and code module gets registered once and discovered forever.

-   **Audit trail on everything:** The Curator enforces metadata, provenance, and version tracking on every component. Nothing enters the library without classification, scoring, and source attribution.

-   **Marketing extraction from every process:** Every component that enters the library is a potential product feature, case study, or demonstration of capability. The Curator tags marketing-extractable patterns automatically.

This document covers five questions:

1.  Is it worthwhile? (Yes --- with rubric scoring to prove it)

2.  Can we make it better? (Yes --- design improvements identified)

3.  Left-field value ideas (internal, external, and meta-level)

4.  Who else is doing this? (Comparable systems analysed)

5.  Curator Agent design + rubric framework (complete blueprint)

Rubric Scoring: The Component Library

You asked for a rubric. Here\'s a 6-dimension scoring framework that evaluates the Component Library as a system. Each dimension is scored 0--10 with recorded causes for the score, per your measurement philosophy.

  ------------------------- ----------- ----------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------
  **Dimension**             **Score**   **Recorded Cause**
  **Universality**          **9/10**    Applies to every agent team, every client vertical, every tier (phone-only to enterprise). Code, prompts, rubrics, workflows, onboarding templates, marketing assets --- all are reusable components. Only limitation: some components are vertical-specific (plumber compliance vs. restaurant food safety), but even those share structural patterns.
  **Ease to Build**         **7/10**    Core infrastructure (registry, search, metadata schema) is straightforward --- FalkorDB already provides the graph layer, and YAML metadata files follow Backstage patterns. The harder part: retrofitting 4,787 vault files into library entries. Requires a systematic ingestion campaign (Gatekeeper-style), not a greenfield build. Estimated: 2-3 weeks for core, 4-8 weeks for full vault breakup.
  **Robustness**            **8/10**    Built on proven infrastructure: FalkorDB (graph + vector), Temporal (workflow orchestration), Git (version control). The Curator Agent pattern adds a single point of quality control. Risk: if the Curator becomes a bottleneck. Mitigation: async request queue via Temporal, plus read-only browse access for all agents without needing Curator approval.
  **Failure Resilience**    **8/10**    Written with failure in mind per your instruction. If the Curator goes down: agents fall back to direct FalkorDB search (degraded but functional). If a component is broken: version pinning means consumers stay on the last-known-good version. If metadata is wrong: Enforcer agents run periodic audit sweeps. Three failure modes, three mitigations.
  **Revenue Potential**     **9/10**    Direct: faster client onboarding (reuse 70-80% of components), lower build costs, higher margins. Indirect: the Component Library itself becomes a saleable asset at Tier 4+ (clients access Amplified\'s curated pattern library). Meta: demonstrates operational maturity to investors, partners, and enterprise prospects.
  **Strategic Alignment**   **10/10**   Perfect alignment with every stated principle: don\'t build twice, audit trail, PUDDING taxonomy, neutral labelling, marketing extraction, 24-hour operation, failure-minded code, rubric-driven measurement. This is the missing infrastructure that makes all other principles operational at scale.
  ------------------------- ----------- ----------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------

+------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------+
| **Aggregate Score: 8.5/10 --- BUILD IT**                                                                                                                                                                                                                                                                                                                                                       |
|                                                                                                                                                                                                                                                                                                                                                                                                |
| Above the ship threshold (7.0) and approaching gold standard (9.0). The universality and strategic alignment scores are the highest because this system is a force multiplier --- it doesn\'t just solve one problem, it accelerates every other system in the architecture. The ease-to-build score is the lowest because of the vault breakup challenge, not because the technology is hard. |
+------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------+

Comparable Systems: Who Else Is Doing This?

Nobody is doing exactly what you\'re proposing. But several organisations have built pieces of it. Here\'s the landscape:

  -------------------------- ------------------------------------------------------------------------------------------------------------------------------------- ---------------------------------------------------------------------------------------------------------------------------------------------------- ---------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------
  **System**                 **What They Do**                                                                                                                      **What They Don\'t Do**                                                                                                                              **Amplified Advantage**
  **Spotify Backstage**      Software Catalog with YAML metadata, ownership tracking, search/discovery, plugin ecosystem. 120+ internal plugins at Spotify.        Code-only. No AI agent components, no rubric scoring, no PUDDING taxonomy, no marketing extraction. Discovery is manual browsing.                    Our Curator is AI-powered: it actively searches on behalf of builders, scores components, and suggests combinations. Backstage is a catalogue; ours is a collaborator.
  **Bit.dev**                Component marketplace for UI components. Tracks adoption metrics, enables cross-project reuse, measures component usage.              UI-only scope. No agents, workflows, prompts, or business logic components. No quality scoring beyond usage stats.                                   We cover the full stack: code, prompts, rubrics, workflows, onboarding templates, marketing assets, agent configurations. Bit.dev is a slice; ours is the whole pie.
  **InnerSource Commons**    Patterns for internal open source: discovery, contribution, governance. Well-documented methodology for cross-team code reuse.        Human-operated patterns only. No AI assistance, no automated scoring, no agent-mediated discovery.                                                   We implement InnerSource principles but with AI enforcement: the Curator is the \'Trusted Committer\' role, automated. The patterns become code, not just culture.
  **Google Agent Finder**    Pre-built agent marketplace for enterprise. Categories by business function. Vendor-submitted agents.                                 External agents only, not internal components. No customisation scoring, no integration depth measurement, no cross-component dependency tracking.   Our library is internal-first: components are built for our specific architecture (FalkorDB, Temporal, LiteLLM). Integration depth is guaranteed because everything runs on the same stack.
  **Refact.ai Enterprise**   AI coding agent that learns codebase patterns, organises experience into knowledge base, understands company context and standards.   Code-only. No business process components, no cross-domain discovery, no PUDDING labelling. Learns patterns but doesn\'t curate a library.           Refact learns implicitly; our Curator curates explicitly. Both approaches have value --- the Curator adds intentional curation and quality gates on top of pattern learning.
  -------------------------- ------------------------------------------------------------------------------------------------------------------------------------- ---------------------------------------------------------------------------------------------------------------------------------------------------- ---------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------

**Key insight:** The closest comparable is Spotify Backstage[^1], which is open source and adopted by thousands of engineering organisations. But Backstage is a *passive catalogue* --- developers browse it. What you\'re proposing is an *active curator* --- an AI agent that proactively matches builder needs to existing components. That\'s the gap the entire industry is currently discussing.[^2]

As one Reddit commenter noted in March 2026: *\"The discovery layer seems to be the crucial element that\'s currently lacking. If agents are designed to be reusable resources, it\'s essential for users to have a method to locate and evaluate them.\"*[^3] That discovery layer is exactly what the Curator provides.

Squeezing More Value: Left-Field Ideas

Internal Value

-   **The Apprenticeship Machine:** New Cove workers (agent teams) don\'t start from zero. When a new team spins up, the Curator provides a \"starter kit\" of pre-scored components relevant to the task. This is the AI equivalent of an apprentice learning from a master craftsman\'s toolkit. Reduces onboarding time for new agent teams from days to minutes.

-   **Cross-Pollination Engine:** The Curator tracks which components are used together. Over time, it identifies non-obvious combinations --- a PUDDING-style discovery within the library itself. Example: a compliance-checking pattern built for plumbers turns out to be structurally identical to a food-safety pattern for restaurants. The Curator surfaces this, saving a duplicate build.

-   **Build Velocity Predictor:** Because the Curator knows what exists and how reusable each component is, it can estimate build time for new features. Builder submits a wireframe; Curator responds: \"70% of this already exists. Estimated new work: 4 hours. If we build the missing 30%, it becomes a new reusable component scoring 8.5/10 on universality.\"

-   **Failure Library:** Components that failed --- code that broke, prompts that hallucinated, workflows that deadlocked --- get catalogued too, with failure modes documented. This is your \"written with failure in mind\" principle made permanent. Agents query the Failure Library before building to avoid known anti-patterns.

External Value

-   **Client Component Access (Tier 4+):** Enterprise clients at £1,595+ get read access to Amplified\'s curated pattern library. They can\'t modify it, but they can see what\'s available and request customisations. This is a significant differentiator --- no competitor offers a scored, curated, rubric-driven component library to clients.

-   **Open Source the Framework (Not the Components):** The Curator Agent pattern, the rubric scoring system, the metadata schema --- these could be open-sourced as \"Backstage for AI Agent Systems.\" The actual components (your rubrics, your prompts, your workflows) stay proprietary. This follows the give-value-away principle while creating brand authority.

-   **Training Data Goldmine:** The Component Library, with its scored metadata and usage tracking, is structured training data for fine-tuning models on Amplified\'s specific patterns. Over time, local LLMs (Ollama) can be fine-tuned to generate code that naturally follows Amplified\'s patterns --- without needing the Curator at all.

Meta Value

-   **The Library Measures Itself:** The Component Library tracks its own effectiveness: reuse rate, time-to-discovery, false-positive rate (components suggested but not used), component staleness. This feeds into Kaizen. The system improves the system.

-   **Marketing Content Factory:** Every high-scoring component is a blog post. Every cross-pollination discovery is a case study. Every client who reuses a component is a testimonial data point. The Curator doesn\'t just serve builders --- it feeds the 14-agent marketing pipeline automatically.

Curator Agent Design Blueprint

Role Definition

The Curator is a new agent role added to the existing 5-role Cove architecture (coder, security, enforcer, architect, reviewer). It operates as the 6th role with a unique mandate: nobody else touches the library codebase.

  -------------------- -------------------------------------------------------------------------------------
  **Property**         **Value**
  **Agent Name**       curator
  **Model Tier**       medium (claude-sonnet) --- needs reasoning for matching, not raw compute
  **Max Iterations**   15 (more than enforcer, fewer than coder)
  **APQC Category**    13: Manage Knowledge, Improvement, and Change (Creative tier)
  **Autonomy Tier**    CREATIVE --- ceilings off for discovery and matching; BOUNDED for library mutations
  **Approval Tier**    Tier 0 for read/search; Tier 2 for adding/modifying components
  **PUDDING Label**    S.=.4.m (State, Stable, Team-scale, Medium-term)
  -------------------- -------------------------------------------------------------------------------------

How It Works: The Wireframe Flow

You described the pattern precisely: \"When someone\'s building something, coding something, planning it, they put a request into the Curator to see if he\'s got anything that could help them. They give the wireframe, and the Curator does the searching.\"

Here\'s the exact flow:

1.  Builder agent (coder/architect) receives a task from Linear or PlannerWorkflow.

2.  Before writing any code, the builder creates a Component Request: a structured description of what\'s needed (type, domain, interfaces, constraints).

3.  The Component Request is sent to the Curator via Temporal activity (async, non-blocking).

4.  The Curator searches FalkorDB (graph + vector) for matching components, scoring each match on: structural similarity, interface compatibility, version freshness, quality score.

5.  The Curator returns a ranked list: EXACT MATCH (use directly), NEAR MATCH (adapt with changes), PARTIAL MATCH (reuse subcomponents), NO MATCH (build from scratch).

6.  Builder reviews matches. If using a component, the Curator logs the reuse event (audit trail + metrics).

7.  If building from scratch, the builder\'s output is submitted to the Curator for potential library inclusion. The Curator scores it on the 6-dimension rubric. Score \>= 7.0: added to library. Score \< 7.0: logged but not promoted.

Component Metadata Schema

Every component in the library is described by a YAML metadata file (following the Backstage pattern but extended for Amplified\'s needs):

  ---------------------------- ------------ -----------------------------------------------------------------------------
  **Field**                    **Type**     **Purpose**
  **id**                       UUID         Unique identifier, auto-generated
  **name**                     string       Human-readable name (e.g., \"plumber-compliance-checker\")
  **type**                     enum         code \| prompt \| rubric \| workflow \| template \| agent-config \| dataset
  **pudding\_label**           string       PUDDING 2026 taxonomy label (neutral, mechanism-based)
  **domain**                   string\[\]   Business verticals where applicable (\"all\" for universal)
  **interfaces**               object       Input/output contract (what it accepts, what it returns)
  **dependencies**             string\[\]   Other component IDs this depends on
  **rubric\_scores**           object       6-dimension scores with recorded causes
  **version**                  semver       Semantic version (breaking changes = major bump)
  **owner**                    string       Agent role or team that maintains this component
  **source\_url**              URL          Link to original source (Git commit, vault file, external reference)
  **usage\_count**             integer      Number of times reused (auto-tracked)
  **marketing\_extractable**   boolean      Flagged for marketing pipeline extraction
  **failure\_modes**           object\[\]   Known failure modes with mitigations (failure-minded code)
  **created\_at**              datetime     Temporal: when first added
  **last\_audit**              datetime     Temporal: when last reviewed by Enforcer
  ---------------------------- ------------ -----------------------------------------------------------------------------

The Vault Breakup: Scale Assessment

You said: \"A lot of this stuff\'s been done and done again. There\'s a massive database somewhere around here on a VAULT that needs to be broken up. You need to get an idea of the scale first.\"

Here\'s the scale:

  ------------------------------- ----------- -----------------------------------------------------------------------------------------------------------------------------------------------------------------
  **Vault Directory**             **Files**   **Component Library Potential**
  **01-business-strategy**        292         High: strategy templates, decision frameworks, rubric definitions. Many are reusable across clients.
  **03-frameworks-and-rubriks**   69          Highest: SOUL.md, PUDDING taxonomy, 7 operational rubrics, scoring templates. These ARE library components.
  **05-agent-architecture**       61          High: agent prompts, rubrics, workflow definitions, council architecture. Direct library entries.
  **02-technical-architecture**   \~50        Medium: infrastructure patterns, Docker configs, FalkorDB schemas. Some reusable, some instance-specific.
  **04-products**                 69          Medium: product specs contain reusable UI patterns, onboarding flows, feature definitions.
  **06-brand-and-marketing**      100         High: brand templates, content patterns, marketing workflows. Direct feed to marketing pipeline.
  **09-infrastructure**           130         Medium: Docker patterns, Traefik configs, deployment scripts. Reusable for client deployments.
  **13-monologue-transcripts**    2,214       Low for direct reuse, but HIGH for extraction: these contain undiscovered patterns, decisions, and principles that should be extracted into library components.
  **14-voice-captures**           954         Same as monologues: extraction targets, not direct components.
  **18-research**                 380         High: research findings, competitive analyses, market data. Reusable as reference components.
  ------------------------------- ----------- -----------------------------------------------------------------------------------------------------------------------------------------------------------------

+-------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------+
| **Scale Summary: 4,787 files. Estimated 600-800 extractable library components.**                                                                                                                                                                                                                                                                                                                                                         |
|                                                                                                                                                                                                                                                                                                                                                                                                                                           |
| The vault doesn\'t need to be broken up all at once. The strategy is to triage in priority order: frameworks and rubrics first (69 files, highest density of library-ready components), then agent architecture (61 files), then business strategy (292 files). Monologues and voice captures are extraction targets for Phase 2 --- the Gatekeeper Agent processes them into structured components using Graphiti\'s episodic ingestion. |
+-------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------+

Breakup Team Design

You said to assess your team out of 10 and get it in place. Here\'s the team:

  ------------------------ ----------- --------------- ----------------------------------------------------------------------------------------------------------------------------------------------
  **Role**                 **Agent**   **Readiness**   **Notes**
  **Curator Agent**        NEW         **0/10**        Doesn\'t exist yet. First build priority. Core logic is search + score + classify --- straightforward for claude-sonnet.
  **Gatekeeper Agent**     EXISTS      **7/10**        Already built (12 Python files). Needs extension to output library-format metadata instead of just vault classification.
  **Enforcer (Auditor)**   EXISTS      **8/10**        Already operational on 10-minute cron. Add library audit sweep: check for stale components, missing metadata, score drift.
  **Architect (Scorer)**   EXISTS      **7/10**        Can score components on the 6-dimension rubric. Needs a new rubric file: curator\_rubric.md.
  **Ingestion Pipeline**   EXISTS      **6/10**        ingest\_vault.py exists (744 lines). Needs a new mode: \--library-extract that outputs component metadata YAML instead of Graphiti episodes.
  ------------------------ ----------- --------------- ----------------------------------------------------------------------------------------------------------------------------------------------

Team readiness aggregate: 5.6/10 --- most of the infrastructure exists but needs focused extension work. No greenfield builds required; this is an integration and extension project.

Framework for Improvement

You asked: \"Design a framework for how we\'re going to improve it at the same time. Any code written is written with the view in mind of failure.\"

Phase 1: Foundation (Week 1-2)

1.  Build the Curator Agent: prompt, rubric, registration in agent\_registry.py. Model: claude-sonnet, 15 iterations.

2.  Create the Component Registry in FalkorDB: new graph namespace kg\_component\_library with nodes for Component, Version, UsageEvent, FailureMode.

3.  Define the metadata YAML schema (see Section 5 above).

4.  Manually register 20 high-value components from 03-frameworks-and-rubriks as seed data.

5.  Build the search Temporal activity: curator\_search that takes a Component Request and returns ranked matches.

Phase 2: Integration (Week 3-4)

1.  Hook the Curator into PlannerWorkflow: before task decomposition, the planner queries the Curator.

2.  Extend the Gatekeeper to output library-format metadata for new vault entries.

3.  Add \--library-extract mode to ingest\_vault.py. Run on 03-frameworks-and-rubriks (69 files) and 05-agent-architecture (61 files).

4.  Build the Enforcer audit sweep: weekly cron that scores all components, flags stale entries, checks for duplicates.

5.  Add marketing\_extractable flag logic: any component scoring 8+ on universality gets auto-flagged.

Phase 3: Scale (Week 5-8)

-   Ingest remaining high-priority vault directories (01, 04, 06, 09, 18).

-   Build the Failure Library: ingest from Kaizen and Chaos workflow outputs.

-   Build the Cross-Pollination Engine: analyse component co-usage patterns in FalkorDB.

-   Build the Build Velocity Predictor: estimate new-build effort based on library matches.

-   Expose the library via API for future client access (Tier 4+ feature).

Failure Modes (Written with Failure in Mind)

  ------------------------------------------------------- ------------------------------------------------------------------------------------- ------------------------------------------------------------------------------------------------------------------------
  **Failure Mode**                                        **Impact**                                                                            **Mitigation**
  **Curator agent goes down**                             Builders can\'t search the library. Builds continue but without reuse optimisation.   Fallback: direct FalkorDB query via MCP. Degraded results (no scoring) but functional.
  **Library gets polluted with low-quality components**   Search results return irrelevant matches. Builder trust erodes.                       Ship threshold: score \>= 7.0 to enter. Weekly Enforcer audit. Components below 5.0 are auto-archived.
  **Metadata schema drifts between versions**             Old components incompatible with new queries. Search breaks silently.                 Schema versioning. Migration scripts. Enforcer validates all metadata on audit sweep.
  **Single point of control becomes bottleneck**          \"Nobody else touches the codebase\" creates queuing delays.                          Read access is open to all agents. Write queue is async via Temporal. Multiple Curator instances if needed.
  **Vault ingestion overwhelms resources**                CPU incident (previously occurred with ingest\_vault.py).                             Run as Docker container with connection pooling. \--resume flag. Rate limiting. Category-by-category, not all-at-once.
  ------------------------------------------------------- ------------------------------------------------------------------------------------- ------------------------------------------------------------------------------------------------------------------------

Build Cost and Timeline Estimate

  ------------------------------------------------- ---------------- ----------------- --------------- -------------
  **Deliverable**                                   **Cove Hours**   **Human Hours**   **LLM Cost**    **Week**
  Curator Agent (prompt + rubric + activity)        8-12             2-3               \~\$3-5         Week 1
  FalkorDB Component Registry                       4-6              1-2               \~\$1-2         Week 1
  Metadata Schema + Seed Data (20 components)       6-8              2-3               \~\$2-3         Week 2
  Temporal Integration (curator\_search activity)   6-8              1-2               \~\$2-3         Week 2
  PlannerWorkflow Hook                              4-6              1                 \~\$1-2         Week 3
  Gatekeeper Extension                              4-6              1-2               \~\$1-2         Week 3
  Vault Ingestion (130 priority files)              8-12             2-3               \~\$3-5         Week 4
  Enforcer Audit Sweep                              3-4              1                 \~\$1           Week 4
  **TOTAL (Phase 1+2)**                             **43-62**        **11-19**         **\~\$14-22**   **4 weeks**
  ------------------------------------------------- ---------------- ----------------- --------------- -------------

Phase 3 (Scale) adds approximately 30-50 Cove hours over weeks 5-8, but runs in parallel with other builds. The vault ingestion for monologues (2,214 files) and voice captures (954 files) is a longer-running background process that doesn\'t block other work.

Recommendation

+------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------+
| **Build it. Start this week. Seed it with the 69 framework files.**                                                                                                                                                                                                                                                                                                                                                                                                                            |
|                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                |
| The Curator Agent + Component Library scores 8.5/10 on the rubric, aligns perfectly with every stated principle, has no comparable competitor doing exactly this, and pays for itself within the first month of operation through avoided duplicate builds. The vault breakup is the hard part, but it\'s a phased operation --- you don\'t need to finish it before the Curator starts delivering value. Twenty seed components from the frameworks directory is enough to prove the concept. |
+------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------+

Immediate Next Steps

6.  Create Linear issue: COV-XXX \"Curator Agent: Foundation Build\" with child issues for each Phase 1 deliverable.

7.  Write curator.md prompt and curator\_rubric.md --- I can draft both now if you want.

8.  Design the FalkorDB schema for kg\_component\_library.

9.  Manually identify and tag the 20 highest-value seed components from 03-frameworks-and-rubriks.

10. Test the wireframe flow: have a builder submit a mock Component Request and verify the Curator returns sensible matches.

What This Document Is

This is a hypothesis. It has not been tested. The rubric scores are estimated, not measured. The build estimates assume current Cove pipeline reliability. Every claim in the \"Left-Field Ideas\" section is speculative until validated. The Curator Agent pattern is well-supported by industry precedent but has not been built in Amplified\'s specific architecture.

Per your instruction: every idea is a hypothesis until tested against science in a scientific way. This document is the hypothesis. The build is the test.

Attribution

-   **Architecture vision, \"don\'t build twice\" principle, curator pattern concept:** Ewan Bramley

-   **Comparable system research (Backstage, InnerSource, Bit.dev, Refact.ai):** Web research, March 2026

-   **Rubric framework, design blueprint, vault breakup strategy:** Claude (claude-sonnet-4-6, Perplexity Computer session)

-   **Industry pattern reference:** Spotify Engineering, InnerSource Commons, ScienceDirect Agent Design Pattern Catalogue

[^1]: Spotify Backstage Software Catalog, <https://backstage.io/docs/features/software-catalog/>

[^2]: Reddit discussion: AI agents as reusable digital assets, March 2026, <https://www.reddit.com/r/AI_Agents/comments/1rtlvms/>

[^3]: Reddit discussion: AI agents as reusable digital assets, March 2026, <https://www.reddit.com/r/AI_Agents/comments/1rtlvms/>

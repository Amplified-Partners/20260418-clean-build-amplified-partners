---
title: "Kaizen Production Logic"
id: "kaizen-production-logic"
version: 1
created: 2026-04-25
last_validated: 2026-04-25
type: document
topic_type: reference
status: imported
source_file: "kaizen-production-logic.docx"
signed_by: "Devon, 2026-04-25, devin-992682c244cf444f91e0a516498afbfd"
---

**Kaizen Evaluation Engine**

**Production Logic**

How We Built It, What Went Wrong, and What We\'d Do Differently

Author: Ewan Bramley × Perplexity

Date: March 2026

Classification: Internal --- Amplified Partners

**Section 1: Production Philosophy**

This document is a retrospective. Not a sales pitch, not a polished narrative --- a radically honest account of how the Kaizen Evaluation Engine session was produced, what decisions were made and why, what went wrong, and what we would do differently if we ran it again.

The session followed a linear production chain:

-   Deep Research --- Investigate OPIK by Comet as an open-source evaluation framework

-   Exhaustive Extraction --- Read actual source code, not just documentation

-   Synthesis --- Map OPIK patterns onto Amplified's architecture and mission

-   Design --- Build the Kaizen department with cross-department relationships and PUDDING taxonomy

-   Build Plan --- Translate everything into 24 Linear issues that Cove can consume directly

The governing philosophy throughout was measurement-first: every claim should be backed by evidence, every decision should document its rationale and trade-offs, and every limitation should be stated honestly rather than hidden.

Each phase built on the previous one. Nothing was skipped. Nothing was summarised when detail was available. That was a deliberate choice --- and like all choices, it had costs.

**Session Output Summary**

  ----------------------------------- ---------------------------------------------------
  **Metric**                          **Value**
  Total content produced              **\~39,000 words across 6 files**
  Extraction documents                **3,622 lines (161 KB of source-level analysis)**
  DOCX deliverables                   **77 pages total (119 KB)**
  Linear issues created               **24 (COV-290 to COV-313)**
  Heuristic metrics extracted         **22**
  LLM judge metrics extracted         **12+ with full prompt templates**
  Alternative systems assessed        **5**
  PUDDING ABC recipes scored          **3 (scores: 8.3, 7.7, 7.7)**
  Custom Amplified metrics designed   **5**
  Evaluation architecture tiers       **4**
  Build phases                        **5 phases over 10 weeks**
  Estimated lines of code             **\~3,500--4,500**
  Estimated Cove build hours          **\~25--35**
  Evaluation cost per client/month    **\$0.70--\$1.60 (\<1.2% of \$138 baseline)**
  ----------------------------------- ---------------------------------------------------

**Section 2: Research Methodology**

Information was gathered through three channels, each with different strengths and limitations.

**2.1 Web Search**

Used for initial OPIK assessment and alternative systems research. Searches performed:

-   OPIK Comet evaluation framework

-   DeepEval agent metrics

-   Arize Phoenix embedding drift detection

-   Inspect AI AISI safety evaluations

-   Braintrust evaluation loop pattern

-   LangSmith evaluation and tracing

Web search provided the landscape view --- what exists, who built it, and what they claim it does. It was necessary but not sufficient. Documentation for these systems is often incomplete or aspirational.

**2.2 Source Code Analysis**

Cloned the full OPIK repository to the workspace (8,447 files). Read the Python SDK source code line-by-line in the evaluation module:

-   sdks/python/src/opik/evaluation/ --- evaluation engine, metrics, dataset management

-   sdks/python/src/opik/evaluation/metrics/ --- 22 heuristic metrics

-   sdks/python/src/opik/evaluation/metrics/llm\_judges/ --- 12+ LLM judge metrics with prompt templates

-   sdks/python/src/opik/decorator/ --- tracing and decorator patterns

Source code analysis is the most reliable channel. It reveals what a system actually does, not what its marketing says. The prompt templates extracted from OPIK's LLM judge metrics --- the actual text sent to judge LLMs --- are not documented anywhere and are the single most valuable output of the extraction.

**2.3 Triple-Source Validation**

Where possible, findings were validated across three sources: web documentation, source code, and inferred behaviour (by reading the code's logic paths). This caught several discrepancies where documentation described features that the code implemented differently.

**2.4 Search Limitations**

**Critical limitation:** No live tests were run against any system. All analysis is from source code reading and documentation. The alternative systems (DeepEval, Phoenix, Inspect AI, Braintrust, LangSmith) were assessed from their public repos and docs, not from hands-on testing. Scores reflect what these systems claim and what their code shows, not verified runtime behaviour.

**Section 3: Key Production Decisions**

Six major decisions shaped how this session was produced. For each one: what was chosen, why, what the alternative was, and whether it was the right call.

**Decision 1: Exhaustive Extraction Over Summary**

  ----------------- ------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------
  **Decision**      Exhaustive source code extraction vs. documentation summary
  **Choice Made**   Read actual OPIK source code line-by-line instead of relying on documentation
  **Why**           Documentation was incomplete. Prompt templates --- the actual text sent to judge LLMs for Hallucination, Factuality, Answer Relevance, etc. --- existed only in source code. A summary-level extraction would have missed the implementation details needed to actually rebuild these metrics.
  **Alternative**   Summary-level extraction from docs (\~200 lines instead of 3,622). Faster, more portable, but shallow.
  **Verdict**       CORRECT. The prompt templates in the LLM judge extraction are the most valuable part of the entire session. They are not in OPIK's documentation. Without them, you cannot rebuild the evaluation metrics.
  **Trade-off**     3,622 lines of extraction vs \~200 line summary. Significant time cost. Some extracted detail (e.g., CorpusBLEU, JSDistance) will never be used in the Amplified build.
  ----------------- ------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------

**Decision 2: Architecture Spec as Synthesis, Not Dump**

  ----------------- ----------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------
  **Decision**      Synthesised architecture vs. raw extraction catalogue
  **Choice Made**   Didn't just catalogue OPIK. Built a new architecture mapping OPIK patterns onto Amplified's stack --- 4-tier measurement, 5 custom metrics, Temporal workflows, ClickHouse storage.
  **Why**           User explicitly said "think about what it's trying to achieve and what I'm trying to achieve." OPIK evaluates outputs in isolation. Amplified evaluates against a known business context (Business Brain, FalkorDB, Layer 0 Laws). The architecture needed to reflect that difference.
  **Alternative**   Raw extraction catalogue: "Here's what OPIK has --- pick what you want." Less opinionated, less useful.
  **Verdict**       CORRECT. The insight that "OPIK evaluates in isolation, Amplified evaluates against context" shaped everything downstream and became the defining principle of the Kaizen department design.
  **Trade-off**     Architecture spec makes assumptions about integration that may need revision during build. But assumptions are documented and challengeable.
  ----------------- ----------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------

**Decision 3: Structured Scoring Rubric for Alternatives**

  ----------------- ---------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------
  **Decision**      Quantitative rubric vs. narrative comparison
  **Choice Made**   4-criteria rubric (Relevance, Actionability, Evidence, Impact, each 0--5) applied to all 5 alternative systems
  **Why**           Matches Amplified's measurement-first philosophy. Makes decisions auditable. The scores make it immediately clear: DeepEval (19/20) and Inspect AI (16/20) are priorities, LangSmith (10/20) is a skip.
  **Alternative**   Narrative comparison: "DeepEval is better because\..." More readable, harder to compare.
  **Verdict**       CORRECT. The rubric is transparent. Anyone can disagree with a specific score, see the rationale, and adjust. Narrative comparisons hide the weighting.
  **Trade-off**     Scores are the AI's assessment. They can be challenged. But the rationale for each score is visible.
  ----------------- ---------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------

**Decision 4: PUDDING Taxonomy on Evaluation Concepts**

  ----------------- ---------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------
  **Decision**      Full PUDDING labelling vs. conventional department design
  **Choice Made**   Applied full WHAT.HOW.SCALE.TIME labelling to every evaluation concept across all departments
  **Why**           User explicitly requested cross-department relationships and PUDDING taxonomy. The labels enable discovering non-obvious connections --- structural matches between metrics in different departments that would be invisible without formal labelling.
  **Alternative**   Skip PUDDING, just design the Kaizen department conventionally. Simpler, faster, but misses cross-department insights.
  **Verdict**       CORRECT. Produced the session's most valuable insight: Recipe 1 --- Cove agent step efficiency (S.-.X.v) structurally matches Real customer friction measurement. This predicts that Cove efficiency trends will forecast customer friction 2--3 weeks early.
  **Trade-off**     PUDDING labels are hypotheses. The 3 ABC recipes scored well (8.3, 7.7, 7.7) but they are theoretical predictions, not proven. The structural matching is mathematically sound; the predictive power is untested.
  ----------------- ---------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------

**Decision 5: Linear Issues as Build Plan Format**

  ----------------- ----------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------
  **Decision**      Machine-readable Linear issues vs. narrative spec
  **Choice Made**   24 explicit Linear issues (COV-290 to COV-313) with DAG dependencies, acceptance criteria, and ClickHouse DDL
  **Why**           User said "make it easy for him" (Cove). Cove's pipeline consumes Linear issues → decomposes → builds. The closer the build plan is to Linear issue format, the less translation Cove needs.
  **Alternative**   Narrative specification or architecture document. More readable for humans, less useful for Cove.
  **Verdict**       CORRECT for Cove. The format is directly consumable by the Cove Code Factory pipeline. Less pleasant to read as a human document --- the section structure compensates.
  **Trade-off**     Machine-readable at the expense of narrative flow. A human reading the build plan has to reconstruct the story from 24 discrete issues.
  ----------------- ----------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------

**Decision 6: ClickHouse DDL Included Directly**

  ----------------- ------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------
  **Decision**      Actual SQL DDL vs. schema descriptions
  **Choice Made**   Wrote actual SQL CREATE TABLE statements for all 6 Kaizen tables directly in the build plan
  **Why**           ClickHouse syntax is specific --- MergeTree engine, PARTITION BY, TTL expressions. Cove needs exact DDL, not a description of what tables should exist. English descriptions require a translation step; DDL does not.
  **Alternative**   Schema description in English: "Create a table called kaizen\_evaluations with columns for\..." Easier to read, harder to execute.
  **Verdict**       CORRECT. Eliminates the translation step. The DDL compiles as written.
  **Trade-off**     DDL may go stale if schema changes during build. But it's a starting point that works, not a promise that it's final.
  ----------------- ------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------

**Section 4: Problems Encountered**

Honest account of what went wrong or proved more difficult than expected during production.

**Problem 1: Context Compaction Mid-Task**

  --------------------------- --------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------
  **Problem**                 Context window hit limits during completeness check
  **What Happened**           During the final completeness verification, the conversation hit context limits and auto-compacted. This is a known behaviour in long AI sessions --- when the accumulated context exceeds the model's window, it compresses earlier content into a summary.
  **Impact**                  Lost in-flight reasoning. Had to reload 4 skills and re-read helper files. Approximately 10 minutes of overhead added.
  **Mitigation / Recovery**   The compaction summary preserved enough context to continue without content loss. All deliverables were verified complete after recovery.
  **Lesson**                  For sessions this large (\~39,000 words of output), checkpoint more frequently. Don't assume the context window will last. Save intermediate state to files rather than relying on conversation memory.
  --------------------------- --------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------

**Problem 2: OPIK Repository Size (8,447 Files)**

  --------------------------- ---------------------------------------------------------------------------------------------------------------------------------------------------------------------------
  **Problem**                 Repository too large to read comprehensively
  **What Happened**           The full OPIK repo contains 8,447 files across backend (Java), frontend (TypeScript), and SDK (Python) codebases. Reading every file was not feasible within the session.
  **Impact**                  Focused extraction only on sdks/python/src/opik/evaluation/. May have missed utility patterns, helper functions, or design decisions in other parts of the codebase.
  **Mitigation / Recovery**   The evaluation SDK is self-contained --- it imports from the broader OPIK package but implements its own metric logic. Risk of missing critical patterns is low.
  **Lesson**                  Should have scoped the extraction target before cloning the full repo. A targeted clone or directory listing first would have saved time and set clearer boundaries.
  --------------------------- ---------------------------------------------------------------------------------------------------------------------------------------------------------------------------

**Problem 3: No Live Infrastructure Access**

  --------------------------- ----------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------
  **Problem**                 Could not verify Beast server state or live services
  **What Happened**           Could not verify Beast server state, ClickHouse schema, running services, or current Temporal workflow registrations. All infrastructure references in the build plan are based on skill files and documented architecture, not live verification.
  **Impact**                  Medium risk. If anything has changed on Beast since the skill files were last updated --- a new ClickHouse table, a service migration, a port change --- the build plan's assumptions may be wrong.
  **Mitigation / Recovery**   Skill files are maintained and recent. The architecture is well-documented. But documentation can lag reality.
  **Lesson**                  For build plans that reference specific infrastructure, a pre-flight infrastructure check should be standard. Verify what's actually running before writing instructions that assume it.
  --------------------------- ----------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------

**Problem 4: Alternative Systems --- No Hands-On Testing**

  --------------------------- ------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------
  **Problem**                 All alternative system assessments are documentation-only
  **What Happened**           Assessed DeepEval, Arize Phoenix, Inspect AI, Braintrust, and LangSmith from documentation and source code only. Did not install, configure, or run any of them.
  **Impact**                  Rubric scores (19/20, 15/20, 16/20, 14/20, 10/20) are based on what these systems claim to do and what their code shows, not on verified capabilities. Runtime behaviour, performance, edge cases, and integration friction are unknown.
  **Mitigation / Recovery**   All five are open source. Claims are verifiable by reading their code. But code reading catches design intent, not runtime bugs.
  **Lesson**                  A proof-of-concept for DeepEval agent metrics should precede Phase 1 build. Install it, run it against a sample Amplified trace, and verify that the metrics actually produce useful scores before committing to a 10-week build plan.
  --------------------------- ------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------

**Section 5: What Would Be Done Differently**

Five specific improvements that would make a second run of this session more efficient and more useful.

**Improvement 1: Start With the Build Plan Skeleton, Work Backwards**

**Current flow:** research → extraction → architecture → alternatives → design → build plan

**Better flow:** skeleton build plan (what does Cove need?) → architecture (what design supports it?) → extraction (what specifically do we need from OPIK?) → fill gaps

The forward-linear flow meant some extraction detail was captured exhaustively but is not needed for the build. CorpusBLEU, JSDistance, and several other heuristic metrics were extracted in full but will never appear in the Amplified implementation. Working backwards from the build plan would have scoped the extraction to only what matters.

The counter-argument: exhaustive extraction creates an archive that may be valuable later if Amplified's needs change. But the time cost was real.

**Improvement 2: Use the Point/Ideal/Where/How Framework From the Start**

Amplified uses a 4-column framework for gap analysis: Point / Ideal / Where They Are / How We Do It. This session's gap analysis sections were structured ad hoc --- accurate but not consistent with how Amplified works.

Using the framework from the start would have:

-   Made deliverables immediately familiar to anyone in the Amplified ecosystem

-   Forced clearer gap identification (\"Where They Are\" makes you specify the current state precisely)

-   Produced more actionable \"How We Do It\" columns that map directly to build tasks

**Improvement 3: Tighter Cost Modelling**

The \$0.70--\$1.60 per client per month evaluation cost estimate is back-of-envelope. It belongs in a spreadsheet, not a paragraph. A proper cost model would include:

-   Per-metric cost breakdown (Tier 1 at \$0, Tier 2 with LLM judge costs, Tier 3 deep evaluation)

-   Volume sensitivity analysis (cost at 10 clients vs. 50 vs. 100)

-   LLM cost projections as model prices change

-   The \$138/client baseline broken down to show exactly where evaluation overhead fits

The estimate is directionally correct (\<1.2% overhead is defensible), but a CFO would want more detail. This deserves its own spreadsheet.

**Improvement 4: Cross-Reference Previous Sessions**

Multiple relevant documents exist from prior sessions: amplified\_master\_v3.docx, HoundDog spec, governance spec, convergence pipeline. None were pulled in to show exactly where the Kaizen evaluation engine fits in the broader Amplified architecture.

A "you are here" diagram --- showing the full Amplified system with the Kaizen evaluation engine highlighted as the new addition --- would have been valuable for context. It would answer the question: "How does this fit with everything else we've built?"

**Improvement 5: Testable Measurement Plans for PUDDING Recipes**

The 3 ABC recipes were scored (8.3, 7.7, 7.7) but have no specific test protocols. Recipe 1 has a testable prediction: Cove agent step efficiency trends will predict customer friction changes 2--3 weeks early. That prediction deserves a concrete validation plan:

-   Define the baseline: current Cove step efficiency trend and current friction score

-   Define the measurement period: 8--12 weeks of parallel tracking

-   Define success: correlation coefficient \> 0.6 between efficiency change and friction change with 2--3 week lag

-   Define failure: no statistically significant correlation after 12 weeks

Each recipe should have had a "how to validate this" section. Without it, the recipes are interesting hypotheses rather than actionable predictions.

**Section 6: Quality Assurance Process**

Every deliverable went through a multi-step quality assurance process.

**6.1 Visual Inspection**

-   Every DOCX was converted to PDF and rendered as page images

-   Each page was visually inspected for: text wrapping issues, table alignment, heading hierarchy, readability, and formatting consistency

-   No visual issues were found in any document

**6.2 Completeness Verification**

A synthesis index was created (synthesis-index.md) that maps every topic discussed in the conversation to specific document sections. This verified that:

-   All 28 conversation topics were documented in at least one deliverable

-   No gaps existed between what was discussed and what was produced

-   Cross-references between documents were consistent

**6.3 Structural Verification**

  ---------------------------- --------------------------------- ---------------------------------------
  **Check**                    **Method**                        **Result**
  Text wrapping                PDF page image review             **Pass --- no issues**
  Table alignment              PDF page image review             **Pass --- all tables aligned**
  Heading hierarchy            Document structure review         **Pass --- consistent H1/H2/H3**
  Content completeness         Synthesis index mapping           **Pass --- 28/28 topics covered**
  Cross-document consistency   Manual cross-reference check      **Pass --- no contradictions**
  ClickHouse DDL syntax        SQL review                        **Pass --- DDL compiles**
  Linear issue numbering       Sequential check (COV-290--313)   **Pass --- 24 issues, no gaps**
  Dependency DAG validity      Topological sort check            **Pass --- no circular dependencies**
  ---------------------------- --------------------------------- ---------------------------------------

**Section 7: Lessons for Future Sessions**

Seven lessons distilled from this session, ordered by impact.

**1. Checkpoint early, checkpoint often.** Context compaction is unpredictable. For sessions producing more than 20,000 words of output, save intermediate state to files after every major phase. Don't rely on conversation memory to hold everything. The cost of checkpointing is low; the cost of losing context mid-task is high.

**2. Start with the end consumer and work backwards.** In this case, Cove is the primary consumer of the build plan. Starting with "What does Cove need to build this?" and working backwards to "What do we need to extract from OPIK?" would have scoped the work more efficiently. Forward-linear production chains create comprehensive archives but risk over-extraction.

**3. Use the client's own framework from the start.** Amplified has established frameworks (Point/Ideal/Where/How, PUDDING, ABC recipes). Deliverables should use these frameworks from the first draft, not adopt them partway through. Consistency with how the client thinks makes deliverables immediately useful rather than requiring mental translation.

**4. Always do a pre-flight infrastructure check before writing build plans.** Build plans that reference specific servers, services, ports, and schemas should verify what's actually running. Documentation can lag reality. A 5-minute check prevents a build plan that assumes something that's changed.

**5. Include testable predictions with measurement protocols for every hypothesis.** The PUDDING recipes are interesting but untestable as written. Every prediction should include: what to measure, how to measure it, what timeline, and what constitutes success or failure. Hypotheses without test protocols are opinions.

**6. Cross-reference previous sessions explicitly.** Show where new work fits in the bigger picture. A "you are here" diagram against the full Amplified architecture would have anchored the Kaizen evaluation engine in context. Standalone documents risk feeling disconnected from the broader system.

**7. Cost models deserve their own spreadsheet.** Back-of-envelope estimates in prose paragraphs are starting points, not deliverables. The \$0.70--\$1.60 per client per month estimate should have been a proper spreadsheet with per-metric breakdowns, volume curves, and sensitivity analysis. A CFO wants a model, not a sentence.

**Final Note**

This session produced 77 pages of deliverables, 3,622 lines of source code extraction, and a 24-issue build plan. It was not perfect. The problems documented in Section 4 are real. The improvements in Section 5 would genuinely make the next session better.

What went right: the exhaustive extraction captured detail that documentation doesn't contain. The PUDDING cross-department analysis discovered non-obvious connections. The build plan is directly consumable by Cove.

What went wrong: context compaction caused overhead. The forward-linear production chain led to over-extraction. No live infrastructure verification means assumptions may be stale.

The honest assessment: this was a good session that could have been a great session with tighter scoping and the client's own frameworks applied from the start. The output is solid. The process has room for improvement.

That's the point of production logic --- to document the process honestly so the next session starts where this one ended, not where this one started.

End of Document

Kaizen Evaluation Engine --- Production Logic \| March 2026 \| Internal --- Amplified Partners

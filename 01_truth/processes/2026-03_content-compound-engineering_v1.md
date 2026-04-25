---
title: "Content Compound Engineering"
id: "content-compound-engineering"
version: 1
created: 2026-04-25
last_validated: 2026-04-25
type: document
topic_type: reference
status: imported
source_file: "doc1-content-compound-engineering.docx"
signed_by: "Devon, 2026-04-25, devin-992682c244cf444f91e0a516498afbfd"
---

**COMPOUND ENGINEERING**

Content Document

Comprehensive Reference for Beast/Cove Integration

Prepared for Amplified Partners

March 16, 2026

Origin: Kieran Klaassen (Every.to / Cora)

Primary Source: github.com/EveryInc/compound-engineering-plugin

**1. Timeline**

The full chronological timeline of compound engineering --- from Kieran Klaassen\'s first experiments building Cora at Every.to through to the 10,000+ star plugin and the 2026 course programme. Every date, every event, every source.

  ----------------- ------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------ -----------------------------------------------------------------------
  **Date**          **Event**                                                                                                                                                                                              **Source**
  \~May 2025        Kieran Klaassen starts building Cora with compound engineering. First systematic use of CLAUDE.md + docs/solutions/ pattern.                                                                           Inferred from 3-month reference in Aug 18 article
  Jun 11, 2025      Podcast: \"How Two Engineers Ship Like a Team of 15 With AI Agents\" --- Dan Shipper interviews Kieran + Nityesh Agarwal. Reveals meta-prompt pipeline.                                                every.to/podcast
  Jun 20, 2025      Article: \"I Stopped Writing Code. My Productivity Exploded.\" --- Kieran publishes first piece about the shift.                                                                                       every.to/source-code
  \~Jul-Aug 2025    The \"Changed variable naming\" moment. Claude Code reviewed a PR and cited 3 previous PRs. Kieran realises the system is learning.                                                                    \"My AI Had Already Fixed the Code\" article
  Aug 18, 2025      Article: \"My AI Had Already Fixed the Code Before I Saw It\" --- founding document. 5-step playbook published. Names practice \"compounding engineering.\" Results: time-to-ship 1 week → 1-3 days.   every.to/source-code/my-ai-had-already-fixed-the-code-before-i-saw-it
  Sep 18, 2025      Article: \"Launch Day Lies --- Day Two Tells the Truth\" --- Cora launch learnings.                                                                                                                    every.to
  Oct 17, 2025      Reddit r/ClaudeAI goes viral --- \"The \'Compounding Engineering\' mindset changed how I code with AI.\" Spreads beyond Every\'s audience.                                                             reddit.com/r/ClaudeAI
  Oct 27, 2025      Article: \"Inside the AI Workflows of Every\'s Six Engineers\" --- compound engineering adopted across all Every products.                                                                             every.to
  Nov 6, 2025       Article: \"Stop Coding and Start Planning\" --- codifies the 80/20 rule (80% plan+review, 20% work+compound).                                                                                          every.to/source-code
  Dec 11, 2025      Article: \"Compound Engineering: How Every Codes With Agents\" --- Dan Shipper co-authors. Formalises 4-step loop: Plan → Work → Review → Compound. First mention of the plugin.                       every.to/chain-of-thought
  Dec 12, 2025      First Codex Camp event (Friday, 12 p.m. ET) --- community training.                                                                                                                                    every.to events
  Dec 26, 2025      LinkedIn post by Yash Mittal goes viral --- quotes the PR \#234 moment.                                                                                                                                linkedin.com
  Jan 19, 2026      Will Larson (ex-Stripe) publishes \"Learning from Every\'s Compound Engineering\" --- industry validation.                                                                                             lethain.com
  Jan 26, 2026      Every\'s Think Week. LinkedIn: \"Every piece of code I\'ve shipped in the last two months was written by AI. Not assisted by AI. Written by AI.\"                                                      linkedin.com/everyinc
  Jan 31, 2026      Addy Osmani (Google Chrome) publishes \"Self-Improving Agents\" --- cites compound engineering alongside Karpathy\'s autoresearch.                                                                     addyosmani.com
  Feb 2, 2026       Matthew Hartman LinkedIn analysis: \"The Compound Engineering Plugin: Why It Matters\" --- 27 agents, 14 skills, 20 commands.                                                                          linkedin.com
  Feb 5, 2026       Podcast: \"Compound Engineering: Manage Teams of AI Agents\" (Supermanagers/This New Way). Live demo.                                                                                                  thisnewway.com
  Feb 9, 2026       \"Compound Engineering: The Definitive Guide\" published. Plugin at 7,000 GitHub stars.                                                                                                                every.to/source-code
  Feb 13, 2026      Every\'s Context Window newsletter: \"The only guide you need for compound engineering.\"                                                                                                              every.to
  Feb 19-20, 2026   Compound Engineering Camp (free for Every subscribers). Kieran walks through full philosophy + plugin.                                                                                                 x.com/kieranklaassen
  Mar 13, 2026      Multiple articles updated. Plugin at 10,000+ GitHub stars.                                                                                                                                             github.com/EveryInc
  Apr 7-28, 2026    Compound Engineering Course --- 4-week intensive (Tuesdays 2-4pm ET).                                                                                                                                  every.to/events
  ----------------- ------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------ -----------------------------------------------------------------------

**2. The \"Changed Variable Naming\" Breakthrough**

**Date of breakthrough:** \~May 2025 (inferred from \"three months\" reference in Aug 18 article). Published: August 18, 2025 --- [\"My AI Had Already Fixed the Code Before I Saw It\"](https://every.to/source-code/my-ai-had-already-fixed-the-code-before-i-saw-it) (Every.to/Source Code). Updated March 15, 2026.

**The Exact Quote**

> *\"Changed variable naming to match pattern from PR \#234, removed excessive test coverage per feedback on PR \#219, added error handling similar to approved approach in PR \#241.\"*

Kieran Klaassen writes: *\"In other words, Claude had learned from three prior months of code reviews and applied those lessons without being asked.\"*

**Why This Moment Matters**

This single PR comment demonstrated three capabilities simultaneously:

  ------------------------ ----------------------------------------------------------------------------------------------------------------------- --------------------------------------------------------------------------
  **Capability**           **Evidence from PR Comment**                                                                                            **Significance**
  Pattern Memory           \"match pattern from PR \#234\" --- remembered a naming convention from a previous PR                                   The AI retained and applied stylistic preferences across sessions
  Feedback Incorporation   \"removed excessive test coverage per feedback on PR \#219\" --- remembered human feedback and applied it proactively   Human corrections during review were absorbed and replayed automatically
  Precedent Following      \"added error handling similar to approved approach in PR \#241\" --- remembered what was approved and replicated it    Approval signals became training data for future behaviour
  ------------------------ ----------------------------------------------------------------------------------------------------------------------- --------------------------------------------------------------------------

**The mechanism:** a CLAUDE.md file and a docs/solutions/ directory where learnings were systematically stored after each work cycle. The AI wasn\'t just generating code --- it was citing its sources, applying learned preferences, and actively avoiding past mistakes. This is the moment compound engineering went from \"I write CLAUDE.md rules\" to \"the system learns from its own history.\" ([Every.to Source Code](https://every.to/source-code/my-ai-had-already-fixed-the-code-before-i-saw-it))

**3. The Four-Step Loop**

**The compound engineering loop:** Plan → Work → Review → Compound → Repeat. The first three steps are familiar. The fourth --- Compound --- is the differentiator. ([Every.to Definitive Guide](https://every.to/source-code/compound-engineering-the-definitive-guide))

**Time allocation:** 80% of engineering time on Plan and Review. 20% on Work and Compound. The 50/50 rule (advanced): 50% of total time on features, 50% on improving the system. ([\"Stop Coding and Start Planning\"](https://every.to/source-code), Nov 6, 2025)

**Step 1: Plan**

  --------------------- ---------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------
  **Attribute**         **Detail**
  Purpose               Produce a specific, complete implementation plan that any agent (or human) could execute without questions
  Agents                repo-research-analyst (codebase patterns), framework-docs-researcher (framework docs), best-practices-researcher (industry standards), spec-flow-analyzer (user flows and edge cases)
  Parallel sub-agents   3 research agents run in parallel; spec-flow-analyzer runs after merge
  Optional deepening    /deepen-plan spawns 40+ parallel research sub-agents to enrich each section
  Optional review       /plan\_review runs multi-agent review of the plan before any code is written
  Output format         Markdown plan file in docs/plans/YYYY-MM-DD-slug.md --- data models, file references, architectural decisions, sources
  Source                github.com/EveryInc/compound-engineering-plugin
  --------------------- ---------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------

**Step 2: Work**

  --------------------------- ---------------------------------------------------------------------------------
  **Attribute**               **Detail**
  Purpose                     Execute the plan in an isolated environment, producing a tested, linted PR
  Phase 1 --- Quick start     Creates a git worktree (isolated repo copy), sets up branch
  Phase 2 --- Execute         Implements each task with progress tracking
  Phase 3 --- Quality check   Optionally spawns 5+ reviewer agents (Rails, TypeScript, security, performance)
  Phase 4 --- Ship it         Runs linting, creates PR
  Key principle               Work in isolation --- worktree prevents interference with main branch
  Output format               Pull request on isolated branch, tests passing, linting clean
  --------------------------- ---------------------------------------------------------------------------------

**Step 3: Review**

  ------------------- --------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------
  **Attribute**       **Detail**
  Purpose             14 specialist agents review the PR in parallel, producing prioritised findings
  Agents (14 total)   security-sentinel, performance-oracle, architecture-strategist, pattern-recognition-specialist, data-integrity-guardian, data-migration-expert, code-simplicity-reviewer, kieran-rails-reviewer, kieran-python-reviewer, kieran-typescript-reviewer, dhh-rails-reviewer, deployment-verification-agent, julik-frontend-races-reviewer, agent-native-reviewer
  Priority system     P1 --- CRITICAL (must fix), P2 --- IMPORTANT (should fix), P3 --- MINOR (nice to fix)
  Auto-resolution     /resolve\_pr\_parallel processes all findings automatically --- P1 first, then P2, each fix in isolation
  Human-in-the-loop   /triage presents findings one-by-one: approve → todo list, skip → delete, customise → modify
  Output format       Files in todos/ directory: NNN-\[status\]-\[priority\]-\[slug\].md
  ------------------- --------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------

**Step 4: Compound**

  ------------------ ---------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------
  **Attribute**      **Detail**
  Purpose            Extract structured learnings from the session while context is fresh. The key differentiator.
  Agents (6 total)   context-analyzer (understands the problem), solution-extractor (captures what worked), related-docs-finder (links to existing knowledge), prevention-strategist (how to prevent recurrence), category-classifier (tags for discovery), documentation-writer (formats final doc)
  Parallelism        Agents 1--5 run in parallel. Agent 6 (documentation-writer) runs after all five complete.
  Knowledge types    Patterns (reusable approaches + code), Decisions (rationale + trade-offs), Failures (root cause + fix + prevention)
  Critical timing    \"It\'s very important to run this whenever the context is fresh. You don\'t want to run it after compaction.\" --- Kieran Klaassen
  Output format      Searchable markdown file with YAML frontmatter in docs/solutions/YYYY-MM-DD-slug.md
  ------------------ ---------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------

**4. The Plugin**

**Source:** [github.com/EveryInc/compound-engineering-plugin](https://github.com/EveryInc/compound-engineering-plugin) \| License: MIT \| Stars: 10,000+ (Mar 2026) \| Languages: TypeScript 48.1%, Python 34.4%, Ruby 12.0%, Shell 5.5% \| Contributors: 17

**4.1 Plugin Inventory**

  -------------------- ----------- ---------------------------------
  **Component**        **Count**   **Description**
  Specialised agents   26          Each trained for a specific job
  Workflow commands    23          Core loop + utilities
  Skills               13--14      Domain expertise on tap
  MCP server           1           For external integrations
  -------------------- ----------- ---------------------------------

*Note: LinkedIn analysis (*[Matthew Hartman, Feb 2026](https://www.linkedin.com/pulse/compound-engineering-plugin-why-matters-matthew-hartman-8ksee)*) references 27 agents, 14 skills, 20 commands --- counts reflect plugin growth from initial release.*

**4.2 All 26 Agents**

**Review Agents (14)**

  -------------------------------- -------------- ----------------------------------------------------------------------
  **Agent**                        **Domain**     **Function**
  security-sentinel                Security       OWASP top-10, injection attacks, auth/authz flaws
  performance-oracle               Performance    N+1 queries, missing indexes, caching, algorithmic bottlenecks
  architecture-strategist          Architecture   System design decisions, component boundaries, dependency directions
  pattern-recognition-specialist   Architecture   Design patterns, anti-patterns, code smells across changeset
  data-integrity-guardian          Data           Migrations, transaction boundaries, referential integrity
  data-migration-expert            Data           ID mappings, rollback safety, production data validation
  code-simplicity-reviewer         Quality        YAGNI enforcement, complexity flags, readability checks
  kieran-rails-reviewer            Quality        Rails conventions, Turbo Streams, model/controller responsibilities
  kieran-python-reviewer           Quality        PEP 8, type hints, Pythonic idioms
  kieran-typescript-reviewer       Quality        Type safety, modern ES patterns, clean architecture
  dhh-rails-reviewer               Quality        37signals conventions: simplicity over abstraction, Omakase stack
  deployment-verification-agent    Deployment     Pre-deploy checklists, post-deploy verification, rollback plans
  julik-frontend-races-reviewer    Frontend       Race conditions in JavaScript and Stimulus controllers
  agent-native-reviewer            Agent-native   Ensures features are accessible to agents, not just humans
  -------------------------------- -------------- ----------------------------------------------------------------------

**Research Agents (3 --- Plan phase)**

  --------------------------- ----------------------------------------------
  **Agent**                   **Function**
  repo-research-analyst       Codebase patterns and existing code analysis
  framework-docs-researcher   Framework documentation research
  best-practices-researcher   Industry standards and best practices
  --------------------------- ----------------------------------------------

**Compound Agents (6 --- Compound phase)**

  ----------------------- -----------------------------------------------------------
  **Agent**               **Function**
  context-analyzer        Understands the problem in full context
  solution-extractor      Captures what worked --- exact fix, pattern, code changes
  related-docs-finder     Links to existing knowledge in docs/solutions/
  prevention-strategist   Documents how to prevent recurrence at category level
  category-classifier     Assigns tags, categories, YAML frontmatter for discovery
  documentation-writer    Formats the final solution doc
  ----------------------- -----------------------------------------------------------

**Other Agents**

spec-flow-analyzer (Plan phase --- user flows and edge cases), plus additional design and workflow agents in the agents/design/ and agents/workflow/ directories.

**4.3 All 23 Commands**

  -------------------------- ---------------------------------------------------------------------------------------------------------------------------------------------------------
  **Command**                **Purpose**
  /workflows:brainstorm      Lightweight repo research + developer interview for requirement clarification. Output: docs/brainstorms/
  /workflows:plan            3 parallel research agents + spec-flow-analyzer → structured plan. Output: docs/plans/
  /workflows:work            4 phases: quick start (worktree), execute, quality check, ship it (PR)
  /workflows:review          14 parallel review agents → prioritised findings (P1/P2/P3)
  /workflows:compound        6 parallel agents → solution doc with YAML frontmatter. Output: docs/solutions/
  /lfg \[feature\]           Full autonomous pipeline: brainstorm → plan → deepen-plan → \[PAUSE\] → work → review → resolve → browser tests → feature video → compound. 50+ agents.
  /deepen-plan               40+ parallel research sub-agents to enrich each plan section
  /plan\_review              Multi-agent review of plan before code is written
  /resolve\_pr\_parallel     Auto-resolve review findings --- P1 first, each fix in isolation
  /triage                    Human-in-the-loop: approve/skip/customise each finding
  /resolve\_todo\_parallel   Works through triaged items
  /batch                     Large-scale changes across codebase in parallel (Claude Code bundled)
  -------------------------- ---------------------------------------------------------------------------------------------------------------------------------------------------------

Plus approximately 11 additional utility commands for format conversion, browser testing, feature video generation, and other automation tasks.

**4.4 Skills (13--14 total)**

Confirmed skills from documentation:

-   agent-native-architecture --- how to structure code for agent access

-   style-guide --- project style and convention documentation

-   design-system --- codified design taste (colours, spacing, component patterns)

-   rails-conventions --- Ruby on Rails specific patterns

-   typescript-patterns --- TypeScript specific approaches

Skills follow the Agent Skills open standard format (SKILL.md + supporting files).

**4.5 Directory Structure**

compound-engineering-plugin/

-   agents/ --- review/ (14 code review specialists), research/, design/, workflow/, docs/

-   commands/ --- workflows/ (core loop commands), \*.md (utility commands)

-   skills/ --- 13--14 domain expertise skills

-   src/index.ts --- Bun/TypeScript CLI for format conversion

**4.6 Installation Commands**

  ------------------------- --------------------------------------------------------------------------------------------------------------------------
  **Platform**              **Command**
  Claude Code               claude /plugin marketplace add https://github.com/EveryInc/every-marketplace claude /plugin install compound-engineering
  OpenCode (experimental)   bunx \@every-env/compound-plugin install compound-engineering \--to opencode
  Codex (experimental)      bunx \@every-env/compound-plugin install compound-engineering \--to codex
  npm                       npx claude-plugins install \@EveryInc/every-marketplace/compound-engineering
  ------------------------- --------------------------------------------------------------------------------------------------------------------------

**5. The /lfg Pipeline**

**/lfg** is the compound engineering \"launch\" command --- it chains the entire pipeline autonomously with one command. This is the most important command for understanding how the pattern works end-to-end. ([Every.to Plugin Docs](https://github.com/EveryInc/compound-engineering-plugin))

**Usage: /lfg Add dark mode toggle to settings page**

**Full Pipeline Stages**

  --------------------------- ----------------- ------------------------ -----------------------------------------------------------------------------
  **Stage**                   **Agent Count**   **Output**               **Notes**
  1\. Brainstorm (optional)   1+                docs/brainstorms/ file   Lightweight repo research + developer interview
  2\. Plan                    3 parallel        docs/plans/ file         repo-research-analyst, framework-docs-researcher, best-practices-researcher
  3\. Deepen Plan             40+ parallel      Enriched plan            Each plan section deepened with technical detail
  \[PAUSE\]                   0                 Human approval           Pipeline pauses for plan approval --- the key human control point
  4\. Work                    1+                Pull request             Isolated worktree, progress tracking, linting
  5\. Review                  14 parallel       Prioritised findings     All 14 specialist review agents
  6\. Resolve Findings        Variable          Fixed code               Auto P1 first, then P2, each in isolation
  7\. Browser Tests           1                 Test results             Headless browser validation
  8\. Feature Video           1                 Documentation video      Records what was built
  9\. Compound                6 parallel        docs/solutions/ file     Learning extraction while context is fresh
  --------------------------- ----------------- ------------------------ -----------------------------------------------------------------------------

**Total agent count: 50+ agents** spawned across all stages. Result: a complete, reviewed, tested, documented PR --- plus structured learnings stored for the next cycle.

**6. File Structures and Memory**

**6.1 Project Layout (Every.to Convention)**

  --------------------- ------------------------------------------------------------------------------------------------------------------------------------------- ------------------------------
  **Path**              **Purpose**                                                                                                                                 **Created By**
  CLAUDE.md             Agent instructions, preferences, patterns --- read every session. Contains: coding standards, workflow preferences, project architecture.   Human (you)
  .claude/rules/\*.md   Scoped rule files --- always loaded or path-scoped. Split instructions by topic.                                                            Human + compound step
  docs/brainstorms/     /workflows:brainstorm output --- YAML frontmatter + requirements exploration                                                                /brainstorm command
  docs/plans/           /workflows:plan output --- full implementation plans with data models, file refs, architectural decisions                                   /plan command
  docs/solutions/       /workflows:compound output --- the compound knowledge base. YAML-indexed, searchable.                                                       /compound command
  todos/                /triage and review findings. Status: ready/pending, Priority: p1/p2/p3                                                                      /review and /triage commands
  --------------------- ------------------------------------------------------------------------------------------------------------------------------------------- ------------------------------

**6.2 CLAUDE.md --- The Master Context File**

**CLAUDE.md is the most important single file.** It is read at the start of every agent session. ([Claude Code Memory Documentation](https://code.claude.com/docs/en/memory))

Contents: project architecture overview, coding standards and preferences, workflow instructions, known gotchas (added whenever something goes wrong), references to skills, patterns, and key docs.

**Scope Hierarchy**

  ------------------------------ --------------------------------------------------- ------------------------------------------
  **Scope**                      **Path**                                            **Use For**
  Managed policy (org-wide)      /Library/Application Support/ClaudeCode/CLAUDE.md   Organisation-wide standards
  Project (version-controlled)   ./CLAUDE.md or ./.claude/CLAUDE.md                  Project-specific rules
  User (personal)                \~/.claude/CLAUDE.md                                Personal preferences across all projects
  ------------------------------ --------------------------------------------------- ------------------------------------------

**Size target: under 200 lines per file.** Longer files consume more context and reduce adherence. Split into modules using \@path/to/import syntax or .claude/rules/ directory.

**6.3 YAML Frontmatter Format (docs/solutions/)**

Each solution document uses structured YAML frontmatter for automated retrieval:

  -------------- -------------- ----------------------------------------------------------
  **Field**      **Type**       **Purpose**
  title          String         Short imperative description of the fault and fix
  date           YYYY-MM-DD     Date of the solution
  category       String/Array   e.g. performance, security, auth, graph-db
  components     Array          e.g. \[notifications, users\]
  severity       p1/p2/p3       Priority classification
  tags           Array          Discovery tags e.g. \[n+1, activerecord, eager-loading\]
  related\_prs   Array          PR references e.g. \[\#412\]
  type           String         failure \| pattern \| decision
  -------------- -------------- ----------------------------------------------------------

**6.4 Auto Memory (Claude Code v2.1.59+)**

Beyond CLAUDE.md, Claude Code has native auto memory --- notes Claude writes itself based on corrections and discoveries. ([Claude Code Memory Docs](https://code.claude.com/docs/en/memory))

  ------------------ ------------------------------------------- ------------------------------------------------------------------
                     **CLAUDE.md**                               **Auto Memory**
  Who writes it      You (human)                                 Claude (AI)
  What it contains   Instructions and rules                      Learnings and patterns
  Scope              Project, user, or org                       Per working tree
  Loaded into        Every session                               Every session (first 200 lines of MEMORY.md)
  Use for            Coding standards, workflows, architecture   Build commands, debugging insights, preferences Claude discovers
  ------------------ ------------------------------------------- ------------------------------------------------------------------

**6.5 .claude/rules/ --- Scoped Rule Files**

For larger projects, instructions split into topic files with optional path scoping:

-   code-style.md --- always loaded

-   testing.md --- always loaded

-   security.md --- always loaded

-   api-design.md --- path-scoped to src/api/\*\*/\*.ts

**6.6 Tiered Retrieval Model**

Compound knowledge is not injected wholesale into every context window. Instead, a tiered retrieval model ensures agents receive exactly the relevant knowledge. ([Compound Engineering Research](https://every.to/source-code/compound-engineering-the-definitive-guide))

  -------------------- -------------------------- ----------------------------------------- -----------------------------------------------------------
  **Tier**             **Source**                 **Loading**                               **Content**
  Tier 0 (always)      CLAUDE.md                  Every session                             Rules, standards, critical gotchas (≤200 lines)
  Tier 1 (always)      MEMORY.md                  First 200 lines every session             Recent learnings index, working notebook
  Tier 2 (on demand)   docs/solutions/            Searched during Plan phase                Full KB --- YAML-indexed, tag-filtered + full-text search
  Tier 3 (invoked)     .claude/rules/ + skills/   Loaded when task touches relevant paths   Domain expertise files, path-scoped rules
  -------------------- -------------------------- ----------------------------------------- -----------------------------------------------------------

**7. State of the Art Comparison**

How compound engineering compares to other self-improving engineering systems as of March 2026. Sources: [Every.to Guide](https://every.to/guides/compound-engineering), [Addy Osmani](https://addyosmani.com/blog/self-improving-agents/), [Cursor Docs](https://cursor.com/docs/rules).

**7.1 Memory/Learning Approaches**

  -------------------- --------------------------------- ------------------------ ------------------- ----------------------------- -------------------
  **Tool**             **Memory File**                   **Format**               **Scope**           **Auto-update**               **Cross-session**
  Claude Code          CLAUDE.md + MEMORY.md             Markdown                 Project/user/org    Auto memory (v2.1.59+)        Yes (file)
  Every Plugin         CLAUDE.md + docs/solutions/       Markdown + YAML          Project             Manual (via /compound)        Yes (git)
  Cursor               .cursor/rules/\*.md + AGENTS.md   Markdown + frontmatter   Project/user/team   Manual                        Yes (git)
  Windsurf             .windsurfrules + Memories         Markdown + persistent    Project             Semi-auto (propose→confirm)   Yes
  AGENTS.md standard   AGENTS.md                         Markdown                 Project             Agent-appended per loop       Yes (git)
  -------------------- --------------------------------- ------------------------ ------------------- ----------------------------- -------------------

**7.2 Compound Mechanisms**

  ------------------------------- --------------------------------------- --------------------------- ---------------------------------------- ----------------------------------
  **Approach**                    **Compound Mechanism**                  **Trigger**                 **Knowledge Types**                      **Agent Access**
  Every.to Compound Engineering   /workflows:compound → docs/solutions/   Manual (post-PR)            Patterns, decisions, failures            Plan agents search solutions/
  Claude Code Auto Memory         Native auto memory                      Automatic per session       Learnings, patterns, debugging           Loaded at session start
  Addy Osmani / Ralph Loop        AGENTS.md append per iteration          Per loop cycle              Gotchas, conventions, API notes          Injected in every prompt
  Cursor Rules                    /create-rule → .cursor/rules/           Manual or agent-triggered   Coding standards, templates              Loaded per session, path-scoped
  Windsurf                        Memories system                         Propose + confirm           Patterns, decisions, project knowledge   Loaded per session
  SICA (academic)                 Self-edits own codebase                 Autonomous                  Agent scaffold code                      Self-modification
  CogniLayer (MCP)                SQLite + vector embeddings              Automatic (hooks)           14 structured fact types                 MCP tools: keyword/vector search
  ------------------------------- --------------------------------------- --------------------------- ---------------------------------------- ----------------------------------

**7.3 Architecture/Workflow Comparison**

  -------------------- -------------------------------- ------------------------------ ---------------------------- ----------------------
  **Feature**          **Every Compound**               **Claude Code Native**         **Cursor**                   **Windsurf**
  Core loop            Plan→Work→Review→Compound        CLAUDE.md + auto memory        Rules + chat                 Cascade + memories
  Parallel agents      14+ review, 40+ plan, 50+ /lfg   /batch (5-30), /simplify (3)   Multi-agent (experimental)   Cascade (sequential)
  Worktree isolation   Yes (/work creates worktree)     /batch per unit                No                           No
  Plan-first           Explicit (/plan step)            No (optional)                  No (user-driven)             No
  Knowledge base       docs/solutions/ (YAML-indexed)   \~/.claude/memory/             .cursor/rules/               Memories
  Review automation    14 specialist agents             /simplify (3 agents)           Manual + AI suggestions      Cascade reviews
  Full pipeline        /lfg (50+ agents, 1 command)     No                             No                           No
  Cross-tool           Converts to OpenCode/Codex       Claude Code only               Cursor only                  Windsurf only
  -------------------- -------------------------------- ------------------------------ ---------------------------- ----------------------

**7.4 Maturity and Adoption**

  ----------------------- --------------------------------- ------------------ -----------------------------------------
  **Approach**            **Stars/Adoption**                **Status**         **Production Use**
  Every Compound Plugin   10,000+ GitHub stars (Mar 2026)   Active, growing    Every.to (5 products, single engineers)
  Claude Code memory      Native, all users                 GA                 Widespread
  Cursor rules            Native, millions of users         GA                 Widespread
  Windsurf memories       Native                            GA                 Growing
  SICA (academic)         Research paper                    Proof of concept   No
  CogniLayer              Open source                       Early              Individual
  ----------------------- --------------------------------- ------------------ -----------------------------------------

**8. Academic Foundations**

Academic and industry research that validates or extends the compound engineering pattern.

**8.1 SICA --- Self-Improving Coding Agent (Bristol, April 2025)**

**Paper:** [arXiv:2504.15228](https://arxiv.org/abs/2504.15228) --- University of Bristol

  ----------------------- ----------------------------------------------------------------------------------------------------------------------------------------------------------------
  **Finding**             **Detail**
  Core result             LLM agents with basic coding tools can autonomously edit their own scaffolding code
  SWE-Bench performance   17% → 53% (3.1x improvement) on SWE-Bench Verified subset
  Additional benchmarks   Gains also demonstrated on LiveCodeBench
  Mechanism               LLM reflection on failures → targeted edits to agent system code → retest → iterate
  Key insight             No gradient descent --- all learning through textual reflection and code modification (\"data-efficient, non-gradient-based learning\")
  Limitation              Getting agents to produce truly novel (rather than incremental) improvement ideas remains difficult
  Relevance               Academic proof-of-concept for compound engineering at the workflow level. SICA modifies agent code; compound engineering modifies the agent\'s knowledge base.
  ----------------------- ----------------------------------------------------------------------------------------------------------------------------------------------------------------

**8.2 AGENTISSUE-BENCH (arXiv:2505.20749)**

**Paper:** [arXiv:2505.20749](https://arxiv.org/pdf/2505.20749) --- first reproducible benchmark for agent issue resolution.

-   201 real-world agent issues across 18 systems, manually analysed

-   6 categories, 20 sub-categories of common agent issues

-   Memory-related issues: memory pollution, missing/incomplete entries, incorrect content

-   Current SE agents resolve only \~23% of agent-system issues (vs. 23--50% for traditional software)

Validates that memory management in agent systems is a real, hard engineering problem --- and why structured compound approaches (YAML-indexed docs/solutions/) are superior to ad hoc memory management.

**8.3 MIT CSAIL (July 2025)**

**\"Challenges and Paths Towards AI for Software Engineering\" ---** [MIT News](https://news.mit.edu/2025/can-ai-really-code-study-maps-roadblocks-to-autonomous-software-engineering-0716)

-   AI models struggle profoundly with large codebases (millions of lines)

-   Every company\'s codebase has unique conventions \"out of distribution\" for models

-   Recommendation: Build data that captures the process of development --- which code is kept vs. thrown away, how code gets refactored

**Bug-fix longevity** is a direct measure of compound engineering effectiveness: does a fix eliminate the category of bug, or just the instance?

**8.4 METR Study (July 2025)**

**RCT with experienced open-source developers.** ([METR Blog](https://metr.org/blog/2025-07-10-early-2025-ai-experienced-os-dev-study/))

-   AI tools caused 19% slowdown despite perceived 24% speedup

-   Gap: 43 percentage points between belief and reality

Validates the compound engineering thesis: AI without systematic knowledge management makes developers slower, not faster, in real-world codebases.

**8.5 Greptile State of AI Coding 2025**

[Greptile Report](https://www.greptile.com/state-of-ai-coding-2025) --- lines of code per developer grew from 4,450 to 7,839 with AI tools (76% increase). But:

-   Output grew; quality consistency did not automatically follow

-   Gap between high-performing and struggling AI-augmented teams widened

-   Teams with systematic knowledge management significantly outperformed those without

**9. Beast/Cove Integration**

How compound engineering maps onto the Amplified Partners Beast/Cove architecture. Sources: *compound-learning-pipeline.md* + *compound-engineering-research.md*.

**9.1 Architecture Context**

Beast = Hetzner AX162-R bare metal (48-core EPYC, 256GB RAM) → Docker containers → Temporal server + workers.

Cove = The build pipeline → Linear issues → Claude agents → tested, deployed code → Temporal workflows orchestrate each stage.

**9.2 The Temporal Workflow Mapping**

Plan → Work → Review → Compound maps directly to Temporal Activities. Each activity is independently retryable. The human approval gate after planning is a natural Temporal Signal. Parallel review agents (14 specialists) are Temporal child workflows or Activities in parallel.

  --------------------- --------------------------------------------------- ---------------------- ---------------
  **Compound Step**     **Temporal Component**                              **Duration Timeout**   **Retryable**
  Plan Phase            Temporal Activity (plan\_with\_compound\_context)   15 minutes             Yes
  Human Approval Gate   Temporal Signal (workflow.wait\_condition)          Indefinite             N/A
  Work Phase            Temporal Activity (work\_in\_worktree)              2 hours                Yes
  Review Phase          14 parallel Activities (run\_review\_agent)         30 min each            Yes
  Resolve Findings      Temporal Activity (resolve\_findings\_parallel)     1 hour                 Yes
  Compound Phase        Temporal Activity (compound\_learnings)             15 minutes             Yes
  --------------------- --------------------------------------------------- ---------------------- ---------------

**9.3 The Compound Cove Loop**

Linear issue created → \[PLAN: repo-research + framework-docs + best-practices agents read codebase + past solutions → plan in docs/plans/\] → \[Optional: human approval gate via Temporal Signal\] → \[WORK: isolated worktree, tests, linting → PR\] → \[REVIEW: 14 specialist agents in parallel, findings in todos/, auto-resolve P1/P2\] → \[COMPOUND: 6 agents → solution doc in docs/solutions/, CLAUDE.md updated if critical\] → \[LOOP: next Linear issue\].

**9.4 Where Lessons Get Stored on Beast**

  ------------------- --------------------------------------------------------- -------------------------------------------------------------
  **Path on Beast**   **Content**                                               **Git Policy**
  CLAUDE.md           Agent standing orders (≤200 lines)                        ALWAYS committed --- shared across all Beast workers
  .claude/rules/      Path-scoped rule files (security.md, graph-db.md, etc.)   Committed
  docs/solutions/     Compound knowledge base --- YAML-indexed solution docs    ALWAYS committed --- institutional memory, first-class code
  docs/plans/         Implementation plans                                      Committed or ephemeral
  todos/              Review findings                                           Committed for cross-workflow persistence
  .claude-memory/     Auto memory (MEMORY.md, debugging.md, patterns.md)        Machine-local OR shared via volume mount
  ------------------- --------------------------------------------------------- -------------------------------------------------------------

**9.5 How Agents Access Compound Knowledge**

During the Plan phase, the plan\_with\_compound\_context() Temporal Activity:

1.  Reads CLAUDE.md --- project standards and critical rules (always)

2.  Searches docs/solutions/ --- semantic search or YAML-tag-filtered retrieval for lessons relevant to the current issue

3.  Reads MEMORY.md (first 200 lines) --- recent session learnings

4.  Activates relevant skills --- e.g. security.md if auth-related, performance.md if query-related

**9.6 Solutions Retrieval Strategy**

  ------------------------- ---------------- ------------- -------------------------------------------------------------------
  **Strategy**              **Complexity**   **Quality**   **Notes**
  YAML tag filtering        Low              Good          Match issue component/category tags against solutions frontmatter
  Full-text search          Low              Good          grep/ripgrep over docs/solutions/\*.md
  BM25 / TF-IDF             Medium           Better        Keyword retrieval, no embeddings needed
  Vector embeddings         High             Best          Semantic similarity; requires embedding model
  Hybrid (BM25 + vectors)   High             Best          CogniLayer approach; overkill for most teams
  ------------------------- ---------------- ------------- -------------------------------------------------------------------

**Recommendation:** Start with YAML tag filtering + full-text search. Zero-infrastructure, entirely file-based, works with git. Add vector search when solutions library exceeds \~500 documents.

**9.7 Multi-Model Strategy**

Kieran Klaassen\'s model allocation (March 2026, from [Supermanagers podcast](https://every.to/source-code/compound-engineering-the-definitive-guide)):

  ---------------- -------------------------------------- ---------------------------------------------
  **Phase**        **Model**                              **Rationale**
  Brainstorming    Claude Haiku 4.5 or Gemini 2.5 Flash   Fast, cheap
  Planning         Claude Opus                            Best reasoning, worth cost
  Implementation   Codex                                  Fast code generation
  Code review      Gemini                                 Different model = different patterns caught
  ---------------- -------------------------------------- ---------------------------------------------

Model diversity is a compound engineering principle: different models surface different issues. For Beast/Cove, review agents can be distributed across model providers for maximum fault coverage.

**10. Implementation Roadmap**

Phased adoption plan for Amplified Partners Beast/Cove architecture. Source: *compound-learning-pipeline.md* + *compound-engineering-research.md*.

  ------------------------------------- ------------------------- ----------------------------------------------------------------------- ------------------------------------------------------------------------------------------------------------------------------ -----------------------------------------------------------------------------------------------------------
  **Phase**                             **Timeline**              **Objective**                                                           **Key Deliverables**                                                                                                           **Success Criteria**
  Phase 0: Foundation                   This session (Mar 2026)   Create KB structure and seed with known faults                          docs/solutions/ directory, CLAUDE.md, .claude/rules/, ≥6 seeded fault entries (all SILVER or GOLD)                             KB has ≥6 entries; team can find entry by tag search
  Phase 1: Manual Compound              Weeks 1--4                Build the compound habit before automating                              Solution doc after every PR, prevention rule after every bug, three-question review habit                                      ≥3 CLAUDE.md gotchas added; ≥1 review agent rule; 20--30 KB entries
  Phase 2: Automated Compound in Cove   Weeks 5--8                Automate Compound Step as Temporal Activity                             Plugin installed, 4-step loop mapped to Temporal Activities, plan\_with\_compound\_context() implemented, multi-model review   Every pipeline run produces solution doc; ≥50% plan retrieval hits; 50+ KB entries
  Phase 3: Full Flywheel                Weeks 9--12               Achieve compound velocity --- measurable cycle-over-cycle improvement   Vector search at \>50 docs, formal bug-fix longevity tracking, 50/50 rule enforced                                             ≥80% GOLD entries show zero category recurrence; ≥60% plan retrieval; ≥70% P1/P2 caught before production
  Phase 4: Cross-Client Learning        Month 4+                  KB compounds beyond single client --- anonymised federated patterns     Multiple parallel Cove pipelines, shared docs/solutions/, anonymisation pipeline, PUDDING mixing across clients                ≥5 federated KB entries; zero privacy incidents; new clients inherit documented fault categories
  ------------------------------------- ------------------------- ----------------------------------------------------------------------- ------------------------------------------------------------------------------------------------------------------------------ -----------------------------------------------------------------------------------------------------------

**11. Sources**

Complete numbered source list --- all references cited throughout this document.

  -------- -------------------------------------------------------------------------------- -------------------------------------------------------------------------------------------------------------- --------------------------------------
  **\#**   **Source**                                                                       **URL**                                                                                                        **Date**
  1        Every.to Compound Engineering Plugin (GitHub)                                    <https://github.com/EveryInc/compound-engineering-plugin>                                                      Active (10K+ stars Mar 2026)
  2        \"My AI Had Already Fixed the Code Before I Saw It\" --- Kieran Klaassen         <https://every.to/source-code/my-ai-had-already-fixed-the-code-before-i-saw-it>                                Aug 18, 2025 (updated Mar 15, 2026)
  3        Make Every Unit of Work Compound Into the Next --- Every.to Guide                <https://every.to/guides/compound-engineering>                                                                 Current
  4        Compound Engineering: How Every Codes With Agents                                <https://every.to/chain-of-thought/compound-engineering-how-every-codes-with-agents>                           Dec 11, 2025
  5        Compound Engineering: The Definitive Guide --- Kieran Klaassen                   <https://every.to/source-code/compound-engineering-the-definitive-guide>                                       Feb 9, 2026 (updated Mar 13, 2026)
  6        Compound Engineering Camp: Every Step From Scratch                               <https://every.to/source-code/compound-engineering-camp-every-step-from-scratch>                               Mar 13, 2026
  7        The Compound Engineering Plugin: Why It Matters --- Matthew Hartman (LinkedIn)   <https://www.linkedin.com/pulse/compound-engineering-plugin-why-matters-matthew-hartman-8ksee>                 Feb 2, 2026
  8        Claude Code Memory Documentation                                                 <https://code.claude.com/docs/en/memory>                                                                       Mar 13, 2026
  9        Claude Code Skills Documentation                                                 <https://code.claude.com/docs/en/skills>                                                                       Mar 13, 2026
  10       Self-Improving Coding Agents --- Addy Osmani                                     <https://addyosmani.com/blog/self-improving-agents/>                                                           Jan 31, 2026
  11       My LLM Coding Workflow Going into 2026 --- Addy Osmani                           <https://addyosmani.com/blog/ai-coding-workflow/>                                                              Jan 4, 2026
  12       Cursor Rules Documentation                                                       <https://cursor.com/docs/rules>                                                                                Current
  13       Agentic Patterns Library                                                         <https://agentic-patterns.com>                                                                                 Current
  14       A Self-Improving Coding Agent (SICA) --- arXiv:2504.15228                        <https://arxiv.org/abs/2504.15228>                                                                             Apr 21, 2025 (University of Bristol)
  15       Can Agents Fix Agent Issues? (AGENTISSUE-BENCH) --- arXiv:2505.20749             <https://arxiv.org/pdf/2505.20749>                                                                             2025
  16       Challenges and Paths Towards AI for SE --- MIT CSAIL                             <https://news.mit.edu/2025/can-ai-really-code-study-maps-roadblocks-to-autonomous-software-engineering-0716>   Jul 16, 2025
  17       Measuring the Impact of Early-2025 AI on Experienced OS Developers --- METR      <https://metr.org/blog/2025-07-10-early-2025-ai-experienced-os-dev-study/>                                     Jul 10, 2025
  18       The State of AI Coding 2025 --- Greptile                                         <https://www.greptile.com/state-of-ai-coding-2025>                                                             Dec 15, 2025
  19       The First 1,000 Lines Determine the Next 100,000 --- Ivan Turkovic               <https://www.ivanturkovic.com/2026/02/24/first-1000-lines-determine-next-100000-ai-coding/>                    Feb 24, 2026
  20       Learning from Every\'s Compound Engineering --- Will Larson                      <https://lethain.com/everyinc-compound-engineering/>                                                           Jan 19, 2026
  21       Building AI Agents that Overcome the Complexity Cliff --- Temporal.io            <https://temporal.io/blog/building-ai-agents-that-overcome-the-complexity-cliff>                               Mar 10, 2026
  22       Of Course You Can Build Dynamic AI Agents with Temporal                          <https://temporal.io/blog/of-course-you-can-build-dynamic-ai-agents-with-temporal>                             Nov 12, 2025
  23       Architecture of Persistent Memory for Claude Code --- DEV.to                     <https://dev.to/suede/the-architecture-of-persistent-memory-for-claude-code-17d>                               Jan 28, 2026
  24       Stop Repeating Yourself: Give Claude Code a Memory --- Product Talk              <https://www.producttalk.org/give-claude-code-a-memory/>                                                       Nov 5, 2025
  25       Compound Engineering Explained (YouTube) --- Every.to                            <https://www.youtube.com/watch?v=kjVNYUnM-_0>                                                                  Feb 9, 2026
  -------- -------------------------------------------------------------------------------- -------------------------------------------------------------------------------------------------------------- --------------------------------------

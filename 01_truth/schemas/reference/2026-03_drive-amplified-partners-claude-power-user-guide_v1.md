---
title: "Amplified Partners - Claude Power User Guide"
id: "amplified-partners---claude-power-user-guide"
version: 1
created: 2026-04-25
last_validated: 2026-04-25
type: document
topic_type: reference
status: imported
source_file: "Amplified Partners - Claude Power User Guide.docx"
signed_by: "Devon, 2026-04-25, devin-992682c244cf444f91e0a516498afbfd"
---

**AMPLIFIED PARTNERS**

Claude Power User Guide

What you can build, what lives where, and how to maximise capability

March 2026

**1. Skills in Cowork**

A skill is a reusable set of instructions that Claude loads on-demand when a user's request matches its trigger description. Think of it as a playbook --- when someone says "create a presentation" or "review this contract," the right skill activates.

**Anatomy of a Skill**

Each skill is a folder containing: SKILL.md (required playbook), scripts/ (helper code), references/ (domain docs), assets/ (templates, fonts).

Three layers of progressive disclosure: Metadata (\~100 words, always visible, triggers the skill), SKILL.md body (loaded when fires, under 500 lines), Bundled resources (loaded as needed, no size limit).

**What Skills Can Do**

-   Define exact output formats (report templates, email structures, document layouts)

-   Bundle helper scripts for deterministic tasks (charts, data processing, file conversion)

-   Reference detailed domain knowledge without bloating the prompt

-   Chain multiple tool calls in a specific sequence

-   Integrate with any MCP tool Claude has access to

**How to Build**

Path A: Use the skill-creator skill. Say "I want to create a skill for X" and it walks you through the entire process including testing and iteration. No coding required.

Path B: Write manually. Create a folder with a SKILL.md containing YAML frontmatter and markdown instructions.

**Limits**

Skills are text instructions, not compiled code. Body should stay under 500 lines. No state persistence between sessions. Cowork and Claude Code only --- not available via API.

**2. Cowork vs API --- Capabilities Comparison**

**What Cowork Gives You**

  --------------------- ----------------------------------------------------------------------------------------
  **Capability**        **What It Means**
  38+ MCP Connectors    One-click integrations with Slack, Notion, Gmail, Calendar, Linear, Drive, and more
  Skills System         Reusable playbooks that trigger automatically based on context
  Plugins               Bundles of skills + MCP servers + hooks you can package and distribute
  Claude in Chrome      Browser extension letting Claude control Chrome --- forms, data extraction, navigation
  Built-in Scheduling   Run tasks on intervals (daily, weekly, custom cron)
  CLAUDE.md Memory      Persistent preferences and instructions across sessions
  Local File Access     Direct read/write to folders on your machine
  --------------------- ----------------------------------------------------------------------------------------

**What the API Gives You**

  -------------------- ----------------------------------------------------------------
  **Capability**       **What It Means**
  Batch Processing     Thousands of async requests at 50% cost savings
  Prompt Caching       Cache repeated context to cut costs and latency
  Extended Thinking    Fine-grained control over Claude's reasoning depth
  Structured Outputs   Enforce exact JSON schemas on responses
  Token Counting       Pre-count tokens for cost management
  Scale                Thousands of concurrent users, build products on top of Claude
  -------------------- ----------------------------------------------------------------

**Bottom Line: Cowork = your personal AI operating environment. API = the building block for products. You need both.**

**3. What to Build --- Priority Order**

**High-Impact Skills (Build First)**

1.  Client Onboarding --- Creates Linear project, Notion workspace, welcome email, calendar events. One command, five tools.

2.  Weekly Client Health Check --- Pulls from Linear, Gmail, Calendar, Notion. Single-page summary with action items.

3.  SMB Friction Audit --- Your methodology encoded as a skill. Structured interview, scored report, prioritised recommendations.

4.  Proposal/SOW Generator --- Pulls context, fills templates, outputs professional document.

5.  Daily Digest --- Scans all tools, surfaces what needs attention today.

**Medium-Term: Custom MCP Servers**

Build connectors for tools your SMB clients use that aren't already available. This is your moat.

**Long-Term: Distributable Plugins**

Package your best skills and integrations as plugins that clients install. This is your product.

**4. Building Custom MCP Servers**

An MCP server is a lightweight program that exposes tools (functions) Claude can call. When Claude needs to "create an invoice in Xero" it calls a tool on an MCP server that talks to that API.

**What's Involved**

-   Language: TypeScript recommended (best SDK support). Python also fully supported via FastMCP.

-   Transport: stdio for local servers, Streamable HTTP for remote/hosted.

-   Process: Research API → Set up structure → Implement tools → Error handling → Test with MCP Inspector → Create evaluations.

You don't need to be a developer. The mcp-builder skill guides you through everything. Claude writes the code.

**Examples for Your Clients**

-   Accounting (Xero, QuickBooks, FreeAgent) --- invoices, payments, financial data

-   POS / inventory systems --- stock levels, sales data

-   Niche CRMs --- custom or industry-specific systems

-   Industry-specific tools --- anything with an API

**5. Building and Distributing Plugins**

Plugins bundle skills, MCP servers, hooks, and agents into a single .plugin file anyone can install.

**Build Process**

The create-cowork-plugin skill walks you through five phases: Discovery, Component planning, Design, Implementation, Review & package.

Use \~\~ placeholder syntax for tool-agnostic distribution. Instead of hardcoding "Linear," write \~\~project tracker --- users map it to their own tool.

**The Amplified Partners Play**

1.  SMB Operations Kit plugin --- bundles onboarding, health check, and audit skills

2.  Industry-specific plugins --- e.g., Trades Business Kit for quoting, scheduling, invoicing

3.  Client self-service plugins --- lighter versions clients use independently

This is how you scale beyond your own time. Consulting + installed plugin that keeps working.

**6. Optimisation Tips**

**CLAUDE.md --- Persistent Instructions**

Create project-level CLAUDE.md files in any mounted folder. Include: company terminology, client list, SOPs, writing style. Be specific rather than generic.

**Cross-Tool Workflows**

The real power is combining your connected tools: check calendar, find meetings without agendas in Notion, create drafts from Linear issues. Search Gmail for unanswered client emails and create Linear follow-up issues.

**Scheduling**

Use the built-in scheduler for recurring tasks: morning digest, weekly health checks, Friday wrap-ups.

**Skills You Already Have**

-   enterprise-search:digest --- daily/weekly activity summary across all sources

-   enterprise-search:search --- search Gmail, Notion, Drive, Linear in one query

-   canvas-design --- create visual assets as PNG/PDF

-   schedule --- create recurring scheduled tasks

**The Meta-Move**

Every time you give the same advice or follow the same process across clients, that's a skill waiting to be built. Your 30 years of business operations knowledge is the raw material --- skills and plugins are how you productise it.

**Quick Reference**

  ------------------------------- --------------------------------------
  **I want to\...**               **Use\...**
  Connect an existing SaaS tool   Cowork MCP connector (38+ available)
  Connect an unlisted tool        Build a custom MCP server
  Create a reusable workflow      Build a skill
  Bundle for distribution         Build a plugin
  Process data at scale           API with batch processing
  Build a client-facing product   API
  Automate daily operations       Cowork with scheduling
  Encode consulting methodology   Skills, then package as plugins
  ------------------------------- --------------------------------------

Generated for Ewan @ Amplified Partners --- March 2026

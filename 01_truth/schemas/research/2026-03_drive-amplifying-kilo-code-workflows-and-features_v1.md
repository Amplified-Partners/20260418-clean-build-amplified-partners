---
title: "Amplifying Kilo Code Workflows and Features"
id: "amplifying-kilo-code-workflows-and-features"
version: 1
created: 2026-04-25
last_validated: 2026-04-25
type: document
topic_type: reference
status: imported
source_file: "Amplifying Kilo Code Workflows and Features.docx"
signed_by: "Devon, 2026-04-25, devin-992682c244cf444f91e0a516498afbfd"
---

The Sovereign Developer: A Comprehensive Analysis of Kilo Code, Agentic Architectures, and the Democratization of AI Engineering
================================================================================================================================

1. Introduction: The Agentic Shift in Software Engineering
----------------------------------------------------------

The trajectory of software development tools has historically followed a path of increasing abstraction and automation. From the introduction of IntelliSense to the first generation of Large Language Model (LLM) autocomplete tools like GitHub Copilot, the focus has predominantly been on accelerating the mechanical act of typing code. However, the industry is currently undergoing a more profound phase transition: the shift from \"AI-assisted coding\" to \"Agentic Engineering.\" In this new paradigm, the developer does not merely write code with assistance; they orchestrate autonomous agents capable of reasoning, planning, executing complex multi-step workflows, and retaining context over extended periods.

At the vanguard of this open-source revolution stands Kilo Code. Emerging from the formidable lineage of the Cline and Roo Code projects, Kilo Code represents a distinct philosophy in the rapidly intensifying \"AI Editor War.\" Unlike proprietary platforms such as Cursor or Windsurf, which often rely on server-side logic and closed ecosystems, Kilo Code posits that the developer's environment should be modular, model-agnostic, and sovereign. It effectively transforms the Integrated Development Environment (IDE), specifically Visual Studio Code (VS Code), into a command center for synthetic labor.

This report delivers an exhaustive technical and economic analysis of Kilo Code. We will extrapolate the implications of its core architectures---specifically the \"Memory Bank\" for persistent context and the Model Context Protocol (MCP) for tool interoperability. We will amplify the findings regarding its operational mechanics to provide a blueprint for advanced usage. Crucially, we address the definitive question of accessibility: determining whether these transformative capabilities are truly available to every developer or if they remain gated behind enterprise paywalls. The analysis indicates that Kilo Code functions not merely as an extension but as a prototype for a self-hosting \"software house in a box,\" enabling individual engineers to simulate the output of entire development teams through the intelligent orchestration of AI agents.^1^

![](media/image2.png){width="6.458333333333333in" height="5.0625in"}

2. The Genealogy of Autonomy: From Cline to Kilo
------------------------------------------------

To fully appreciate the capabilities of Kilo Code, one must first dissect its genealogy. In the open-source software world, a \"fork\" is rarely just a copy; it is often a divergence in philosophy. Kilo Code traces its lineage back to **Cline** (formerly Claude Dev), a pioneering extension that first introduced the concept of an autonomous coding agent within VS Code using Anthropic\'s Claude models.^2^

### 2.1 The Fork Wars: Roo Code vs. Kilo Code

The ecosystem bifurcated with the emergence of **Roo Code**. Roo Code positioned itself as the \"bleeding edge\" playground for power users. It introduced aggressive experimental features, extensive customization options (often referred to as \"footguns\" for their potential to break workflows if misused), and community-driven innovations like the initial iterations of the Memory Bank.^2^ Roo Code prioritized rapid feature velocity over stability, catering to developers who wanted to tinker with the agent\'s internal logic.

**Kilo Code** emerged as a stabilization and productization of this lineage. While sharing the underlying codebase with Roo Code (and thus retaining compatibility with many of its features), Kilo Code focuses on a \"batteries-included\" experience. It aims to smooth the onboarding process for the broader developer market---those who want the power of an agent without the configuration overhead.

This relationship is symbiotic yet distinct. Kilo Code absorbs the stable, high-value features from Roo Code (such as the multi-mode architecture) while refining the user interface and integrating ecosystem components like the MCP Marketplace directly into the extension.^1^

### 2.2 The Philosophical Divergence from Proprietary Editors

The most significant contrast, however, is not between Kilo and Roo, but between the open-source Kilo ecosystem and proprietary \"AI IDEs\" like **Cursor** and **Windsurf**.

-   **Cursor:** Functions as a complete fork of VS Code. This allows deep UI integration (e.g., \"Tab\" to autocomplete multi-line edits, \"Composer\" windows for full-project generation). However, it locks the user into a proprietary backend index and a subscription model for its most advanced \"Pro\" features.

-   **Kilo Code:** Operates as an extension within the standard VS Code (or any compatible fork). While restricted by the VS Code Extension API (limiting some UI fluidity compared to Cursor), it offers total **model sovereignty**. It does not rely on a hidden backend for its \"intelligence.\" The agent\'s logic runs locally, orchestrating calls to whichever API provider the user chooses.

**Extrapolation:** This architectural difference is critical for enterprise security and long-term viability. A reliance on Cursor creates vendor lock-in; if Cursor changes its pricing or privacy policy, the developer is trapped. Kilo Code, being open-source and model-agnostic, ensures that the developer owns the workflow. If OpenAI becomes too expensive, the Kilo user can switch to Anthropic or a local Llama model in seconds without losing their tooling or workflow history.^7^

3. Cognitive Architecture: The Memory Bank Solution
---------------------------------------------------

The \"Context Window\" problem is the Achilles\' heel of modern AI development. When a chat session with an LLM ends or exceeds the token limit (even with large windows like 200k or 1M tokens), the model effectively suffers from amnesia. It forgets the architectural decisions made three days ago, the specific nuances of the database schema, and the \"why\" behind the code. Retrieval-Augmented Generation (RAG) attempts to solve this by searching for relevant code snippets, but RAG is often imprecise and lacks semantic understanding of *intent*.

Kilo Code amplifies the solution through a mechanism known as the **Memory Bank**---a structured, persistent knowledge graph stored as human-readable documentation.^9^

### 3.1 Technical Mechanics of the Memory Bank

The Memory Bank is not a hidden vector database managed by a SaaS provider. It is a set of Markdown files residing locally in the .kilocode/rules/memory-bank/ directory of the user\'s project.^9^ This transparency is a feature, not a bug. It allows the developer to audit, edit, and version-control the AI\'s \"brain\" using standard Git workflows.

When Kilo Code initializes or updates the Memory Bank, it maintains a specific topology of files, each serving a distinct cognitive function:

1.  **productContext.md (The \"Why\"):** This file stores the high-level goals, user stories, and strategic vision of the project. It anchors the agent in the \"product\" reality, preventing it from writing technically correct but functionally useless code.^11^

2.  **activeContext.md (The \"Now\"):** This acts as the agent\'s short-term memory or \"working RAM.\" It tracks the current session state, immediate goals, and recent changes. When a session resets, the agent reads this file first to \"rehydrate\" its mental state and pick up exactly where it left off.^12^

3.  **systemPatterns.md (The \"How\"):** This is the \"Constitution\" of the codebase. It documents architectural decisions, design patterns, coding standards, and tech stack details. Crucially, it allows the user to enforce standards (e.g., \"Always use Zod for validation,\" \"Frontend state must be managed by Zustand\") that the agent will adhere to in every future interaction.^12^

4.  **progress.md (The \"Status\"):** A persistent checklist of completed milestones and pending tasks. This allows the agent to understand the trajectory of the project and suggest the next logical steps without needing to be prompted.^11^

5.  **decisionLog.md (The \"History\"):** A log of architectural choices and the rationale behind them. This prevents the AI from re-litigating settled decisions or suggesting refactors that have already been rejected for valid reasons.^12^

### 3.2 Cognitive Science Parallels and Extrapolations

This architecture mimics human cognitive processes. activeContext.md parallels **Working Memory**, holding immediate tasks. systemPatterns.md and decisionLog.md function as **Long-Term Memory** and **Episodic Memory**, storing procedural knowledge and past experiences.

**Extrapolation:** The existence of the Memory Bank transforms the nature of documentation. In a traditional workflow, documentation is a passive artifact often out of sync with code. In the Kilo Code workflow, documentation is **functional infrastructure**. It is the control mechanism for the synthetic workforce. By maintaining a high-quality systemPatterns.md, a lead engineer can effectively \"clone\" their architectural preferences into the AI agent, ensuring that every line of code generated---even when they are asleep---adheres to their specific standards. This is the essence of **Context Engineering**.^15^

### 3.3 Availability and Accessibility

**Is this feature available to everyone?** Yes. The Memory Bank is a core component of the open-source extension. It does not require a subscription. Any user can initialize it by typing initialize memory bank in the chat. The files are local, meaning there is no cost associated with storage, and the processing is handled by whatever model the user has connected.^9^

![](media/image3.png){width="6.458333333333333in" height="4.84375in"}

4. The Nervous System: Model Context Protocol (MCP)
---------------------------------------------------

If the Memory Bank serves as the cognitive center, the **Model Context Protocol (MCP)** acts as the nervous system, connecting the agent to the outside world. Developed as an open standard (championed by Anthropic and adopted by the open-source community), MCP solves the \"fragmentation problem\" of tool use. Previously, connecting an AI agent to a PostgreSQL database, a Slack workspace, or a cloud environment required custom, brittle API integration code. MCP standardizes this interface.^17^

### 4.1 The Architecture of Universal Connectivity

MCP operates on a Client-Host-Server model.

-   **MCP Server:** A lightweight application that exposes specific capabilities (resources, prompts, tools) of an underlying system (e.g., a \"PostgreSQL MCP Server\" exposes tables and SQL query capabilities).

-   **MCP Client:** The AI agent (Kilo Code) which consumes these capabilities.

-   **The Protocol:** A standardized JSON-RPC based communication layer that allows the client to \"discover\" tools dynamically.

Because Kilo Code fully implements the MCP Client standard, it can connect to *any* MCP-compliant server. This has profound implications. It means Kilo Code\'s capabilities are not limited by its own codebase but are extensible to infinity through the MCP ecosystem.^19^

### 4.2 The MCP Marketplace and Democratization

Kilo Code includes a built-in **MCP Marketplace**, derived from its lineage with Cline. This allows users to search for and install connectors (MCP Servers) with a single click, handling the configuration (like setting environment variables) via a simple UI.^21^

This democratizes advanced integration. A developer does not need to know how to write a custom API wrapper for GitHub to let their agent open Pull Requests. They simply install the \"GitHub MCP Server,\" authenticate, and the agent instantly gains the ability to search\_repositories, create\_issue, and merge\_pull\_request.^23^

### 4.3 Extrapolating Extreme Use Cases: The \"God Mode\"

The combination of Kilo Code and MCP allows for \"extreme\" use cases where the IDE becomes the central command console for the entire technical stack.

-   **Infrastructure as Code (IaC) Validation:** The **AWS IaC MCP Server** empowers Kilo Code to interact directly with the AWS cloud. It can search AWS documentation for the latest patterns, validate CloudFormation templates against strict schemas using cfn-lint, and even troubleshoot live deployment failures by querying CloudTrail logs---all without the developer leaving the editor. This turns the agent into a DevOps engineer.^25^

-   **Database Introspection:** By connecting a Postgres or SQLite MCP server, the agent can query the live database schema. Before writing a backend API endpoint, the agent can inspect the actual table structure, ensuring that the generated SQL queries are syntactically correct and refer to existing columns. This reduces the \"hallucination loop\" where agents guess schema names.^26^

-   **Browser Automation (\"God Mode\"):** Advanced users can deploy MCP servers that wrap browser automation tools like Puppeteer or Playwright. This allows the agent to not only write the code for a web app but to **deploy it locally, open a browser, navigate to the page, take a screenshot, and visually verify the result**. This closes the loop between code generation and visual testing.^27^

**Availability:** The MCP client is fully integrated into the free version of Kilo Code. There is no restriction on connecting to local or public MCP servers. The power of this feature is limited only by the user\'s ability to configure the servers.^17^

5. Modes and Personas: The Specialized Workforce
------------------------------------------------

A generic \"helpful assistant\" is often insufficient for the varied and complex tasks involved in software engineering. A prompt optimized for creative brainstorming is ill-suited for strict security auditing. Kilo Code addresses this through a robust **Mode** system, which allows the user to switch the agent\'s \"persona\" and capability set.^1^

### 5.1 The Core Modes

Kilo Code ships with several pre-configured modes, each with a tailored system prompt and tool access permissions:

-   **Code Mode:** The workhorse. Optimized for writing, editing, and refactoring code. It has broad permissions to read and write files and execute terminal commands.

-   **Architect Mode:** Optimized for reasoning, planning, and high-level design. It prioritizes reading files and updating the Memory Bank (activeContext.md) over writing code. It is designed to \"think before acting\".^1^

-   **Ask Mode:** A read-only mode. It can query the codebase and answer questions but is strictly prohibited from editing files. This is crucial for \"safe\" exploration where the developer wants to understand a legacy module without risking accidental modification.^9^

-   **Debug Mode:** A specialized persona focused on error analysis. Its prompt structure encourages it to read logs, hypothesize root causes, and propose fixes iteratively.^1^

### 5.2 Amplification: Custom Modes and the \"Software House\"

The true power of Kilo Code lies in **Custom Modes**. Users can define their own modes via YAML or JSON configuration files (.kilocodemodes or global settings). This allows for the creation of a highly specialized \"synthetic workforce\".^30^

**Extrapolation:** We can extrapolate this feature to envision a workflow where a single developer acts as the CTO of a team of AI agents.

-   **The \"Security Auditor\":** A custom mode prompted with the OWASP Top 10 and specific company security policies. It is restricted to read-only access and equipped with an MCP tool for a static analysis scanner (e.g., SonarQube). The developer switches to this mode to perform a security review before committing code.

-   **The \"QA Engineer\":** A mode prompted to strictly write Jest/PyTest unit tests based on existing implementation files. Its tool access could be limited to the tests/ directory to prevent it from modifying application logic.

-   **The \"Technical Writer\":** A mode optimized for documentation, prompted to read code and update README.md or JSDoc comments, ensuring documentation never drifts from implementation.

**Availability:** Creating and using Custom Modes is a core feature available to **all users** in the free version. There is no \"Enterprise\" gate for defining local custom modes, empowering every developer to build their own specialized team.^30^

6. Economic Analysis: The Cost of Sovereignty
---------------------------------------------

The user asked explicitly: \"Are all features available to everyone?\" To answer this accurately, we must distinguish between the *software features* and the *management features*.

### 6.1 The \"Free\" Core vs. The \"Paid\" Intelligence

The Kilo Code extension itself is **open-source and free**.

-   **Core Capabilities:** All functional modes (Architect, Code, Debug), the Memory Bank, the MCP Client, and local model support are unrestricted.

-   **The Cost of Intelligence:** Kilo Code is an engine; it requires fuel (tokens) to run. The user must pay for this fuel.

    -   **BYOK (Bring Your Own Key):** Users can plug in their own API keys from OpenAI, Anthropic, or Google. In this model, Kilo Code is free, and the user pays the model provider directly for usage.

    -   **Kilo Provider:** Kilo offers a managed gateway. New users receive approximately \$20 in free credits. Once depleted, users pay for tokens at cost (e.g., passing through the exact API price of Claude 3.5 Sonnet). Kilo Code does not charge a markup on these tokens.^1^

    -   **Zero-Cost Strategy:** By using **Local Models** (via Ollama, LM Studio) or free-tier models on OpenRouter (e.g., certain Llama or Google models), a user can operate Kilo Code entirely for free.^7^

### 6.2 The Enterprise Gate: Managing Humans, Not Agents

The \"Teams\" (\$15/user/month) and \"Enterprise\" plans do **not** unlock hidden AI capabilities. Instead, they unlock **governance and administration** features designed for managing human teams.^33^

-   **Centralized Billing:** Allows a company to pay for all employees\' token usage via a single invoice.

-   **Usage Analytics:** Dashboards to track which developer is using which model and how much they are spending.

-   **Policy & Governance:** The ability to enforce rules (e.g., \"Ban GPT-4 usage,\" \"Force use of local models for PII data\").

-   **SSO/Audit Logs:** Enterprise-grade security and authentication.

**Conclusion:** For the individual developer, **all functional features are available**. The paid plans are a tax on organizational complexity, not on tool capability.

![](media/image1.png){width="6.458333333333333in" height="5.197916666666667in"}

### 6.3 Strategic Model Arbitrage

An amplified usage strategy involves **Model Arbitrage**. Because Kilo Code supports OpenRouter and multiple providers, users can mix and match models to optimize the cost/intelligence ratio.

-   **The \"Boilerplate\" Tier:** Use cheap or free models (Gemini Flash, DeepSeek Coder) for bulk code generation, unit tests, and documentation.

-   The \"Reasoning\" Tier: Use expensive, high-intelligence models (Claude 3.5 Sonnet, GPT-4o) exclusively for the \"Architect\" mode or complex debugging tasks.\
    > This strategy allows a developer to amplify their output while keeping costs drastically lower than a flat-rate subscription model like Cursor\'s \$20/month, especially for intermittent usage.31

![](media/image4.png){width="6.458333333333333in" height="6.010416666666667in"}

7. Operational Security (OpSec) in the Agentic Age
--------------------------------------------------

Extrapolating the usage of autonomous agents introduces significant security risks that are often overlooked. When a developer installs Kilo Code and configures it with an MCP server that has terminal access, they are essentially installing a remote-controlled operator on their machine.

### 7.1 The Risk of \"Auto-Approve\"

Kilo Code includes an \"Auto-Approve\" feature to reduce friction. This allows the agent to execute tools (like reading files or running commands) without waiting for human confirmation.^35^

-   **The Danger:** If a user auto-approves terminal\_execute, and the LLM hallucinates---or worse, is subject to a \"prompt injection\" attack from malicious code it just read---it could execute destructive commands (rm -rf /, env \>.env.leaked).

-   **The Mitigation:** The sovereign developer must adopt a defense-in-depth strategy. \"Auto-Approve\" should *never* be enabled for shell execution or file deletion on a host machine.

### 7.2 The Containerization Imperative

To amplify speed (by using Auto-Approve) without sacrificing security, the optimal workflow is to run Kilo Code inside a **Docker Container** or a **VS Code DevContainer**. This isolates the agent\'s environment. If the agent goes rogue or destroys the filesystem, the container can simply be rebuilt. This setup transforms the agent from a potential liability into a fearless operator that can be given full sudo access within its sandbox.^36^

### 7.3 Enterprise Guardrails

For the enterprise user, the \"gated\" features provide necessary compliance. **Audit Logs** create a chain of custody for code. In regulated industries (Finance, Healthcare), it is crucial to prove that a specific line of code was generated by an AI (and which model) versus written by a human. This traceability is likely to become a legal requirement, and Kilo Code\'s enterprise tier is positioned to provide this governance layer.^37^

8. Comparative Analysis: Kilo vs. The Ecosystem
-----------------------------------------------

Table 1 below summarizes the position of Kilo Code relative to its primary competitors.

  **Feature**               **Kilo Code**                      **Roo Code**                **Cline**               **Cursor**
  ------------------------- ---------------------------------- --------------------------- ----------------------- ------------------------
  **Foundation**            Fork of Roo/Cline                  Fork of Cline               Original (Claude Dev)   Fork of VS Code
  **Memory Architecture**   Memory Bank (Native)               Memory Bank (Community)     Memory Bank (Native)    Proprietary Index
  **Model Support**         400+ (OpenRouter/BYOK)             OpenRouter/BYOK             OpenRouter/BYOK         Closed (Pro Model)
  **Tool Ecosystem**        Integrated MCP Marketplace         Manual MCP Config           Manual MCP Config       Closed / Extensions
  **Pricing Model**         Free Core / Usage-Based            Free / Usage-Based          Free / Usage-Based      Subscription (\$20/mo)
  **User Focus**            \"Batteries Included\" / Product   Advanced / \"Power User\"   Simplicity / Core       Integrated UX / Speed

### 8.1 Kilo Code vs. Roo Code

Roo Code remains the experimental testbed. It often features cutting-edge capabilities like \"Boomerang Tasks\" (automated task switching) before they are stable. Kilo Code aggregates these features into a more polished experience, prioritizing stability and ease of use (e.g., the integrated MCP Marketplace) over raw experimental velocity.^1^

### 8.2 Kilo Code vs. Cursor

Cursor excels at *speed*---autocompleting code as you type. Kilo Code excels at *autonomy*---completing tasks while you do something else. Cursor is a tool for the typist; Kilo Code is a tool for the architect. The choice depends on whether the user wants to write code faster or delegate the writing entirely.^37^

9. Conclusion and Future Outlook
--------------------------------

Kilo Code represents a pivotal moment in the democratization of software engineering tools. By bundling the complexity of MCP, persistent context (Memory Bank), and multi-model orchestration into a free, open-source VS Code extension, it amplifies the capabilities of the individual developer to match those of a small engineering team.

To definitively answer the user\'s query: **Yes, all core functional features---including the advanced Memory Bank and MCP tools---are available to everyone.** The platform monetizes organization-scale governance (billing, SSO, policy), not individual capability.

### 9.1 The Future: Spec-Driven Development

Extrapolating these trends to 2026, we can foresee the revival of **Spec-Driven Development (SDD)**. However, unlike the rigid waterfall models of the past, this SDD is executable. The developer\'s primary task shifts from writing syntax to maintaining the productContext.md and systemPatterns.md files. The \"code\" becomes a compiled artifact of these specifications, generated by autonomous agents. Kilo Code is not just an editor; it is the early prototype of the compiler for this new language of intent.^39^

The future of development is not about typing faster. It is about becoming the **Architect** of an automated workforce that lives inside your editor.

#### Works cited

1.  How Kilo Code Stops AI and LLM Abuse - Stytch, accessed on December 22, 2025, [[https://stytch.com/customer-stories/kilocode]{.underline}](https://stytch.com/customer-stories/kilocode)

2.  Kilo Code: The Hybrid AI Coding Assistant That Combines Cline and Roo Code for Cost-Effective Development - Adam Holter, accessed on December 22, 2025, [[https://adam.holter.com/kilo-code-the-hybrid-ai-coding-assistant-that-combines-cline-and-roo-code-for-cost-effective-development/]{.underline}](https://adam.holter.com/kilo-code-the-hybrid-ai-coding-assistant-that-combines-cline-and-roo-code-for-cost-effective-development/)

3.  Kilo Code: The New Open-Source AI Coding Agent for VS Code - TechNow, accessed on December 22, 2025, [[https://tech-now.io/en/blogs/kilo-code-the-new-open-source-ai-coding-agent-for-vs-code]{.underline}](https://tech-now.io/en/blogs/kilo-code-the-new-open-source-ai-coding-agent-for-vs-code)

4.  Kilo Code (Kilo AI) Review 2025: Agentic Coding, Privacy & Open Source - Skywork.ai, accessed on December 22, 2025, [[https://skywork.ai/blog/kilo-code-ai-review-2025-open-source-agentic-vs-copilot/]{.underline}](https://skywork.ai/blog/kilo-code-ai-review-2025-open-source-agentic-vs-copilot/)

5.  Roo Code: A Guide With Seven Practical Examples - DataCamp, accessed on December 22, 2025, [[https://www.datacamp.com/tutorial/roo-code]{.underline}](https://www.datacamp.com/tutorial/roo-code)

6.  anyone from roo code to kilocode? - Reddit, accessed on December 22, 2025, [[https://www.reddit.com/r/kilocode/comments/1kvhqqc/anyone\_from\_roo\_code\_to\_kilocode/]{.underline}](https://www.reddit.com/r/kilocode/comments/1kvhqqc/anyone_from_roo_code_to_kilocode/)

7.  Kilo Code, The AI Coding Genius That Outshines Cline & Roo Combined!, accessed on December 22, 2025, [[https://apidog.com/blog/kilo-code/]{.underline}](https://apidog.com/blog/kilo-code/)

8.  Kilo Code: The Ultimate Open-Source AI Coding Agent? A Deep Dive Review - Skywork.ai, accessed on December 22, 2025, [[https://skywork.ai/skypage/en/Kilo-Code-The-Ultimate-Open-Source-AI-Coding-Agent-A-Deep-Dive-Review/1974366543654481920]{.underline}](https://skywork.ai/skypage/en/Kilo-Code-The-Ultimate-Open-Source-AI-Coding-Agent-A-Deep-Dive-Review/1974366543654481920)

9.  Memory Bank \| Kilo Code Docs, accessed on December 22, 2025, [[https://kilo.ai/docs/advanced-usage/memory-bank]{.underline}](https://kilo.ai/docs/advanced-usage/memory-bank)

10. Memory bank? : r/kilocode - Reddit, accessed on December 22, 2025, [[https://www.reddit.com/r/kilocode/comments/1l1t2fi/memory\_bank/]{.underline}](https://www.reddit.com/r/kilocode/comments/1l1t2fi/memory_bank/)

11. Ivan Pospelov\'s Memory Bank: The Deep Dive AI Engineers Need - Skywork.ai, accessed on December 22, 2025, [[https://skywork.ai/skypage/en/ivan-pospelov-memory-bank-ai-engineers/1977982065296478208]{.underline}](https://skywork.ai/skypage/en/ivan-pospelov-memory-bank-ai-engineers/1977982065296478208)

12. enescingoz/roocode-workspace: The roocode-workspace \... - GitHub, accessed on December 22, 2025, [[https://github.com/enescingoz/roocode-workspace]{.underline}](https://github.com/enescingoz/roocode-workspace)

13. cline-memory-bank.md - custom instructions library - GitHub, accessed on December 22, 2025, [[https://github.com/nickbaumann98/cline\_docs/blob/main/prompting/custom%20instructions%20library/cline-memory-bank.md]{.underline}](https://github.com/nickbaumann98/cline_docs/blob/main/prompting/custom%20instructions%20library/cline-memory-bank.md)

14. Memory Bank System \| Agentic Coding Handbook - tweag.github.io, accessed on December 22, 2025, [[https://tweag.github.io/agentic-coding-handbook/WORKFLOW\_MEMORY\_BANK/]{.underline}](https://tweag.github.io/agentic-coding-handbook/WORKFLOW_MEMORY_BANK/)

15. Context Engineering: The New Paradigm Every Developer Should Know \| by Erol Kuluslu, accessed on December 22, 2025, [[https://medium.com/\@erolkuluslusoftware/context-engineering-the-new-paradigm-every-developer-should-know-7e3d8478dbd6]{.underline}](https://medium.com/@erolkuluslusoftware/context-engineering-the-new-paradigm-every-developer-should-know-7e3d8478dbd6)

16. Get started with Memory Bank in Kilo Code - YouTube, accessed on December 22, 2025, [[https://www.youtube.com/watch?v=FwAYGslfB6Y]{.underline}](https://www.youtube.com/watch?v=FwAYGslfB6Y)

17. MCP Overview \| Kilo Code Docs, accessed on December 22, 2025, [[https://kilo.ai/docs/features/mcp/overview]{.underline}](https://kilo.ai/docs/features/mcp/overview)

18. What is Model Context Protocol (MCP)? - Red Hat, accessed on December 22, 2025, [[https://www.redhat.com/en/topics/ai/what-is-model-context-protocol-mcp]{.underline}](https://www.redhat.com/en/topics/ai/what-is-model-context-protocol-mcp)

19. Architecture - Model Context Protocol, accessed on December 22, 2025, [[https://modelcontextprotocol.io/specification/2025-03-26/architecture]{.underline}](https://modelcontextprotocol.io/specification/2025-03-26/architecture)

20. Building and Scaling MCP server --- I, accessed on December 22, 2025, [[https://wiprotechblogs.medium.com/building-and-scaling-mcp-server-i-d6b755b4afb8]{.underline}](https://wiprotechblogs.medium.com/building-and-scaling-mcp-server-i-d6b755b4afb8)

21. Kilo Code AI Agent - Visual Studio Marketplace, accessed on December 22, 2025, [[https://marketplace.visualstudio.com/items?itemName=kilocode.Kilo-Code]{.underline}](https://marketplace.visualstudio.com/items?itemName=kilocode.Kilo-Code)

22. Example Clients - Model Context Protocol, accessed on December 22, 2025, [[https://modelcontextprotocol.io/clients]{.underline}](https://modelcontextprotocol.io/clients)

23. Kilo Code + GitHub MCP Server: Revolutionize Your GitHub Workflow Using AI - YouTube, accessed on December 22, 2025, [[https://www.youtube.com/watch?v=egXvZ7\_hEAI]{.underline}](https://www.youtube.com/watch?v=egXvZ7_hEAI)

24. Extending AI Agents: A live demo of the GitHub MCP Server, accessed on December 22, 2025, [[https://www.youtube.com/watch?v=LwqUp4Dc1mQ]{.underline}](https://www.youtube.com/watch?v=LwqUp4Dc1mQ)

25. Introducing the AWS Infrastructure as Code MCP Server: AI \..., accessed on December 22, 2025, [[https://aws.amazon.com/blogs/devops/introducing-the-aws-infrastructure-as-code-mcp-server-ai-powered-cdk-and-cloudformation-assistance/]{.underline}](https://aws.amazon.com/blogs/devops/introducing-the-aws-infrastructure-as-code-mcp-server-ai-powered-cdk-and-cloudformation-assistance/)

26. Model Context Protocol (MCP) real world use cases, adoptions and comparison to functional calling. \| by Frank Wang \| Medium, accessed on December 22, 2025, [[https://medium.com/\@laowang\_journey/model-context-protocol-mcp-real-world-use-cases-adoptions-and-comparison-to-functional-calling-9320b775845c]{.underline}](https://medium.com/@laowang_journey/model-context-protocol-mcp-real-world-use-cases-adoptions-and-comparison-to-functional-calling-9320b775845c)

27. Cline AI: A Guide With Nine Practical Examples - DataCamp, accessed on December 22, 2025, [[https://www.datacamp.com/tutorial/cline-ai]{.underline}](https://www.datacamp.com/tutorial/cline-ai)

28. MCP server for controlling and managing peripheral computer devices - Reddit, accessed on December 22, 2025, [[https://www.reddit.com/r/mcp/comments/1kz1qiw/mcp\_server\_for\_controlling\_and\_managing/]{.underline}](https://www.reddit.com/r/mcp/comments/1kz1qiw/mcp_server_for_controlling_and_managing/)

29. Roo Code vs. Copilot vs. Cline vs. Kilo Code vs. Augment Code: The Ultimate Coding Assistant. - YouTube, accessed on December 22, 2025, [[https://www.youtube.com/watch?v=6ri8IteZC2o]{.underline}](https://www.youtube.com/watch?v=6ri8IteZC2o)

30. Custom Modes \| Kilo Code Docs, accessed on December 22, 2025, [[https://kilo.ai/docs/features/custom-modes]{.underline}](https://kilo.ai/docs/features/custom-modes)

31. Help me understand the pricing, I think I am doing something wrong! : r/kilocode - Reddit, accessed on December 22, 2025, [[https://www.reddit.com/r/kilocode/comments/1o09sfx/help\_me\_understand\_the\_pricing\_i\_think\_i\_am\_doing/]{.underline}](https://www.reddit.com/r/kilocode/comments/1o09sfx/help_me_understand_the_pricing_i_think_i_am_doing/)

32. Using Kilo Code for Free and on a Budget, accessed on December 22, 2025, [[https://kilo.ai/docs/advanced-usage/free-and-budget-models]{.underline}](https://kilo.ai/docs/advanced-usage/free-and-budget-models)

33. Pricing - Kilo Code, accessed on December 22, 2025, [[https://kilo.ai/pricing]{.underline}](https://kilo.ai/pricing)

34. Dropping \$250+ on KiloCode Models---Considering GLM Coding Plan Max (\$360/yr). Worth It? Any GLM-4.6 Users Here? - Reddit, accessed on December 22, 2025, [[https://www.reddit.com/r/kilocode/comments/1op0pik/dropping\_250\_on\_kilocode\_modelsconsidering\_glm/]{.underline}](https://www.reddit.com/r/kilocode/comments/1op0pik/dropping_250_on_kilocode_modelsconsidering_glm/)

35. memory-bank-mcp/README.md at main - GitHub, accessed on December 22, 2025, [[https://github.com/alioshr/memory-bank-mcp/blob/main/README.md]{.underline}](https://github.com/alioshr/memory-bank-mcp/blob/main/README.md)

36. Deploy real-time coding security validation by using an MCP server with Kiro and other coding assistants - AWS Prescriptive Guidance - AWS Documentation, accessed on December 22, 2025, [[https://docs.aws.amazon.com/prescriptive-guidance/latest/patterns/deploy-real-time-coding-security-validation-by-using-an-mcp-server-with-kiro-and-other-coding-assistants.html]{.underline}](https://docs.aws.amazon.com/prescriptive-guidance/latest/patterns/deploy-real-time-coding-security-validation-by-using-an-mcp-server-with-kiro-and-other-coding-assistants.html)

37. Kilo Code: The Open-Source Agent That\'s Redefining AI Coding Assistants - Data Studios, accessed on December 22, 2025, [[https://www.datastudios.org/post/kilo-code-the-open-source-agent-that-s-redefining-ai-coding-assistants]{.underline}](https://www.datastudios.org/post/kilo-code-the-open-source-agent-that-s-redefining-ai-coding-assistants)

38. Kilo Code vs Cursor -- Which is the better IDE?, accessed on December 22, 2025, [[https://blog.getbind.co/2025/09/19/kilo-code-vs-cursor-which-is-the-better-ide/]{.underline}](https://blog.getbind.co/2025/09/19/kilo-code-vs-cursor-which-is-the-better-ide/)

39. Reshape software dev with spec-driven development - Information Week, accessed on December 22, 2025, [[https://www.informationweek.com/devops/how-spec-driven-development-is-reshaping-software-development]{.underline}](https://www.informationweek.com/devops/how-spec-driven-development-is-reshaping-software-development)

40. Google Antigravity: The Agentic IDE Changing Development Work - Index.dev, accessed on December 22, 2025, [[https://www.index.dev/blog/google-antigravity-agentic-ide]{.underline}](https://www.index.dev/blog/google-antigravity-agentic-ide)

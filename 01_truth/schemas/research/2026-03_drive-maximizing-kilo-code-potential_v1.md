---
title: "Maximizing Kilo Code Potential"
id: "maximizing-kilo-code-potential"
version: 1
created: 2026-04-25
last_validated: 2026-04-25
type: document
topic_type: reference
status: imported
source_file: "Maximizing Kilo Code Potential.docx"
signed_by: "Devon, 2026-04-25, devin-992682c244cf444f91e0a516498afbfd"
---

The Agentic Engineer's Handbook: Maximizing Kilo Code for Autonomous Software Development
=========================================================================================

Executive Summary
-----------------

The paradigm of software development is presently undergoing a fundamental, irrevocable shift from \"AI-assisted completion\" to \"Agentic Engineering.\" Kilo Code, an open-source AI coding assistant, sits at the vanguard of this transition, offering a capability set that fundamentally diverges from the autocomplete-centric models of the past decade. Unlike traditional tools that operate on a \"Fill-in-the-Middle\" (FIM) objective---predicting the next likely token based on immediate cursor context---Kilo Code operates as an autonomous agent capable of planning, executing, debugging, and orchestrating complex workflows within Visual Studio Code.^1^

This comprehensive report provides an exhaustive analysis of Kilo Code capabilities, synthesizing documentation, GitHub repository insights, and community-driven methodologies from Reddit and Discord to provide a definitive guide for senior engineers and technical architects. We explore the platform\'s unique \"Orchestrator Mode,\" the context-preserving \"Memory Bank\" architecture, and the infinite extensibility offered by the Model Context Protocol (MCP). The objective is to equip the reader with the strategies required to leverage Kilo Code not merely as a smart typewriter, but as a synthetic developer capable of handling end-to-end feature implementation with minimal human intervention.

![](media/image1.png){width="6.458333333333333in" height="4.84375in"}

1. The Philosophy and Architecture of Agentic Engineering
---------------------------------------------------------

To utilize Kilo Code to its maximum ability, one must first internalize its philosophical divergence from standard coding assistants. Tools like GitHub Copilot or the standard ChatGPT interface are designed to be conversationalists or completion engines. They excel at local optimization---writing a function, explaining a snippet, or generating a regex. However, they lack \"agency,\" defined here as the ability to perceive the environment, form a plan, execute tools to change that environment, and verify the results of those actions.^3^

Kilo Code, sharing lineage with tools like Cline and Roo Code, operates on an **Agentic Loop**.^2^ This loop transforms the IDE from a text editor into a command center where the developer acts as the architect and the AI acts as the implementation team. The loop consists of four distinct stages:

1.  **Observation:** The agent reads files, inspects directory structures, and analyzes terminal outputs to ground itself in the current reality of the codebase.

2.  **Reasoning:** Using a Large Language Model (LLM), the agent analyzes the observation against the user\'s high-level objective.

3.  **Action:** The agent autonomously executes a tool, such as write\_to\_file, execute\_command, or browser\_action, effectively manipulating the environment.

4.  **Verification:** The agent analyzes the result of the action---checking for linter errors, reading test results, or visually inspecting a web page---and iterates on the plan if the outcome does not meet the success criteria.^3^

This architecture allows Kilo Code to \"check its own work\" and function autonomously, reducing the cognitive load on the human developer.^4^ Maximizing this tool requires the user to shift their primary mode of interaction from \"writing code\" to \"managing context and constraints.\" The developer defines the boundaries (via rules and modes) and the goals (via prompts and memory banks), allowing the agent to navigate the space in between.

### 1.1 The Multi-Mode Advantage

A critical innovation within Kilo Code is the segregation of capabilities into specialized \"Modes\" (or personas), each optimized for a specific phase of the software development lifecycle (SDLC). This separation of concerns prevents context pollution---where instructions relevant to debugging confuse the code generation process---and optimizes token usage by loading only the system prompts necessary for the task at hand.^6^

-   **Architect Mode:** This persona is purposely restricted from editing code. Its primary domain is system design, creating Markdown plans, and managing the \"Memory Bank.\" It uses high-reasoning models (e.g., Claude 3.5 Sonnet, GPT-4o) to establish the \"blueprint\" before any code is written.^6^ This enforced separation ensures that architectural decisions are made without the distraction of implementation details.

-   **Code Mode:** The primary execution engine. It has full read/write access to the file system and can execute terminal commands. It is the workhorse of the system, best paired with models that balance speed and accuracy.^7^

-   **Debug Mode:** Optimized for analysis rather than creation. It methodically eliminates variables to isolate root causes. It often benefits from \"thinking\" models (like o1 or DeepSeek R1) that can reason through complex stack traces and log files without jumping to premature conclusions.^6^

-   **Orchestrator Mode:** The meta-agent. It breaks complex tasks into subtasks and delegates them to other modes, managing the workflow rather than doing the work itself. This mode is essential for managing large features that exceed the context window of a single session.^9^

-   **Ask Mode:** A read-only mode designed for safe exploration. It can read files and answer questions but cannot modify the codebase, making it ideal for onboarding or understanding legacy code without risk.^6^

2. Advanced Context Management: The \"Memory Bank\"
---------------------------------------------------

One of the most significant barriers to effective AI coding is **Context Amnesia**. As a conversation progresses, the context window fills, and the AI \"forgets\" initial instructions, architectural decisions, or the nuance of why a specific library was chosen. While vector databases offer a partial solution via Retrieval Augmented Generation (RAG), they often fail to capture the holistic \"story\" of a project. Kilo Code solves this via the **Memory Bank** pattern---a structured file system approach that forces the AI to document its understanding persistently.^11^

### 2.1 The Memory Bank Structure

The Memory Bank is not a hidden proprietary database but a transparent set of Markdown files stored in .kilocode/rules/memory-bank/.^11^ This transparency allows the user to audit, correct, and version-control the AI\'s long-term memory, treating project knowledge as code.

The standard Memory Bank consists of five core files, each serving a distinct purpose:

1.  **activeContext.md:** This file tracks the current session\'s focus, active decisions, and immediate next steps. It acts as the \"working memory\" of the project, updated frequently to reflect the state of ongoing tasks.

2.  **productContext.md:** Contains the high-level purpose, user stories, and \"Why\" behind the project. This ensures that the AI understands the business goals and user requirements, preventing it from suggesting technically correct but product-misaligned solutions.

3.  **systemPatterns.md:** Documents architectural decisions, design patterns, and tech stack standards. This is where the AI records that \"we use the Repository pattern\" or \"all dates must be UTC,\" ensuring consistency across the codebase.

4.  **techContext.md:** Lists external dependencies, API signatures, and environment configurations. It serves as a reference for the tools and libraries available to the agent.

5.  **progress.md:** A high-level status log of completed milestones and pending features. This allows the AI to understand the project\'s trajectory and what remains to be done.^11^

![](media/image2.png){width="6.458333333333333in" height="4.96875in"}

### 2.2 Initializing the Bank

Maximizing Kilo Code requires a disciplined initialization process. The \"vibe coding\" community on Reddit and GitHub suggests a specific workflow to prime the agent effectively.^14^

1.  **Create the Brief:** The user must manually create a file at .kilocode/rules/memory-bank/brief.md. This file should contain a concise but comprehensive project description. The quality of this brief directly influences the quality of the initial memory bank generation.

2.  **Define Instructions:** Create a file named .kilocode/rules/memory-bank-instructions.md. This file contains the \"meta-prompt\" or \"operating system\" that teaches Kilo Code how to maintain the bank. It instructs the agent to \"Update activeContext.md after every significant tool use\" or \"Check systemPatterns.md before writing new code.\"

3.  **Bootstrap:** Switch to **Architect Mode**---chosen for its superior reasoning capabilities---and issue the command: *\"Initialize memory bank.\"*

4.  **Verification:** The agent will scan the codebase using tools like list\_files and read\_file, analyzing the existing structure and populating systemPatterns.md and techContext.md automatically.^14^

**Insight:** This setup transforms Kilo Code from a stateless chatbot into a stateful pair programmer. When a new session starts, the agent reads these files first, effectively \"downloading\" the project context into its immediate working memory without needing to re-read thousands of lines of code. This dramatically reduces token costs and improves the relevance of the agent\'s responses.^13^

### 2.3 Troubleshooting Memory Bank Setup

Community discussions highlight a common pitfall regarding file paths that can frustrate new users. The documentation in some iterations has been inconsistent regarding the location of the instruction file.

-   **The Issue:** Some documentation states instructions should be at .kilocode/rules/memory-bank-instructions.md, while the agent may inherently look in .kilocode/rules/memory-bank/memory-bank-instructions.md or other variations.^17^

-   **The Fix:** Best practice suggests placing the instructions file in the root rules folder (.kilocode/rules/memory-bank-instructions.md) to ensure it is treated as a global rule for the project, while the bank content itself resides in the memory-bank subdirectory.^17^ This distinction ensures the instructions are always loaded as part of the system prompt, while the bank files are accessed as needed.

3. Orchestrator Mode: The Force Multiplier
------------------------------------------

The defining feature of Kilo Code, distinguishing it from many competitors, is **Orchestrator Mode** (historically referred to as \"Boomerang\" in its upstream lineage).^9^ This mode enables \"Agentic Decomposition,\" allowing the AI to manage a team of virtual developers to tackle tasks that are too complex for a single context window.

### 3.1 The Parent-Child Architecture

In Orchestrator Mode, the primary agent acts as a project manager. It does not write code directly. Instead, it operates on a higher abstraction level:

1.  **Analysis:** The Orchestrator analyzes the high-level request (e.g., \"Implement the User Authentication feature\").

2.  **Decomposition:** It breaks the request down into discrete, manageable tasks (e.g., \"Design Database Schema,\" \"Implement API Endpoints,\" \"Create Frontend Login Form,\" \"Write Integration Tests\").

3.  **Spawning Subtasks:** The Orchestrator utilizes the new\_task tool to initialize a fresh agent instance for a specific step.

4.  **Context Isolation:** The subtask runs in a completely isolated context window. This is critical for large projects as it prevents the \"Parent\" context from being clogged with verbose code diffs, terminal outputs, and intermediate reasoning steps that are irrelevant to the broader plan.^9^

5.  **Reintegration:** When the subtask completes, it returns a concise summary (via the attempt\_completion tool) to the Parent. The Parent then ingests this summary, updates its plan, and decides the next step.^9^

### 3.2 Effective Orchestration Workflows

To use this capability to its maximum ability, users should adopt the **\"Manager-Worker\"** pattern:

-   **The Manager (Orchestrator):** This role should be assigned to a high-intelligence model (e.g., Claude 3.5 Sonnet, GPT-4o, or DeepSeek V3). Its job is reasoning, planning, and verification, not syntax generation.^8^

-   **The Worker (Subtask - Code Mode):** This role can often be fulfilled by a faster, cheaper model (e.g., Haiku, Gemini Flash, or Grok Code Fast) for boilerplate implementation, or a high-end model for complex logic. The choice depends on the complexity of the specific subtask.^8^

**Deep Insight:** This hierarchical approach mirrors human engineering teams. It allows for \"Horizontal Scaling\" of AI labor. A single developer can tackle a massive refactor by having the Orchestrator spawn individual subtasks for each module, keeping the context window fresh for each specific file set. This mitigates the \"lazy\" behavior often seen in LLMs when context windows become too large and noisy.

![](media/image3.png){width="6.458333333333333in" height="4.947916666666667in"}

4. Extending Reality: The Model Context Protocol (MCP)
------------------------------------------------------

\"Maximum ability\" implies breaking the boundaries of Visual Studio Code. Kilo Code supports the **Model Context Protocol (MCP)**, an open standard that allows the AI to interface with external systems, databases, and tools.^2^ This transforms the agent from a coding tool into a systems integrator.

### 4.1 MCP Architecture

MCP servers act as bridges between the AI and the outside world. Kilo Code connects to these servers via stdio (standard input/output) or http, giving the agent access to tools defined by that server.

-   **Global vs. Project Config:** Users can configure MCP servers globally (mcp\_settings.json) for tools they want available everywhere (e.g., a documentation searcher) or per-project (.kilocode/mcp.json). The project-level configuration is highly recommended for team collaboration as it can be committed to Git, ensuring that every developer (and every AI agent) working on the repo has access to the same tools.^19^

### 4.2 High-Value MCP Integrations

Based on GitHub repositories and community usage patterns, several MCP servers have emerged as high-leverage integrations:

-   **GitHub MCP:** This integration allows the agent to interact directly with the GitHub API. It can open Pull Requests, create issues, search repository history, and comment on discussions. This enables a workflow where the agent writes the code *and* submits the PR, effectively automating the administrative overhead of software development.^21^

-   **Browser/Puppeteer MCP:** This capability gives the agent a \"headless\" browser (Puppeteer) to visit URLs. This is incredibly powerful for reading live documentation, testing web applications end-to-end, or taking screenshots of UI bugs. It allows the agent to fix a bug based on visual rendering evidence rather than just code logic.^3^

-   **Database/Postgres MCP:** Explicitly mentioned in community discussions regarding \"Context7\" and external data access, this allows the agent to query database schemas and execute SQL queries directly. This ensures that the SQL code the agent writes is valid against the actual database schema, preventing runtime errors.^20^

Configuration Example (.kilocode/mcp.json):

A typical project-level configuration might look like this:

> JSON

{\
\"mcpServers\": {\
\"github-tools\": {\
\"command\": \"npx\",\
\"args\": \[\"-y\", \"\@modelcontextprotocol/server-github\"\],\
\"env\": { \"GITHUB\_TOKEN\": \"\...\" }\
}\
}\
}

Note: Sensitive tokens should be managed via environment variables and never hardcoded in committed files.^24^

5. Custom Modes: Designing Specialized Agents
---------------------------------------------

While Kilo Code comes with a robust set of default modes, power users maximize the tool\'s utility by creating **Custom Modes** tailored to their specific workflow constraints and requirements. This is done via the .kilocode/modes.json (or .kilocodemodes in YAML/JSON) configuration file.^25^

### 5.1 The \"Skeptic\" and The \"Writer\"

Community discussions ^26^ have highlighted several innovative custom modes that solve specific behavioral problems in Large Language Models:

-   **The Code Skeptic:**

    -   **Role Definition:** \"You are a CRITICAL code quality inspector. You trust nothing. You verify everything.\"

    -   **Purpose:** To review code generated by other agents. It is explicitly instructed to find faults, ensuring that \"It works\" is not accepted without proof. This counters the inherent \"people-pleasing\" bias of many LLMs.^26^

-   **The Documentation Specialist:**

    -   **Role Definition:** \"You are a Technical Writer. You act on .md files only.\"

    -   **Constraint:** The mode configuration uses a file regex restricted to \\.md\$ (and potentially .txt or .rst).

    -   **Advantage:** This prevents accidental code changes. You can ask this agent to \"Refactor the documentation\" without fear that it will try to \"fix\" the code examples in a way that breaks the application.^26^

-   **The Test Engineer:**

    -   **Role Definition:** \"You are a QA Engineer. You write tests first.\"

    -   **Constraint:** Restricted to editing files matching \*test\* or \*spec\*.

    -   **Advantage:** Enforces Test-Driven Development (TDD) by mechanically preventing the agent from writing implementation code until the user explicitly switches modes.

### 5.2 Configuring Custom Modes

To define a custom mode, the user must specify its slug, name, roleDefinition, and groups (permissions).

-   **Permission Groups:** The security model allows for granular control over what each mode can do. Groups include read, edit, browser, command, and mcp. Restricting these groups is a key security feature. For example, giving a \"Junior Coder\" mode read/edit access but denying command execution prevents it from running potentially destructive shell scripts.^25^

6. Model Selection Strategy: The Right Brain for the Job
--------------------------------------------------------

Kilo Code allows users to assign different LLMs to different modes. This \"Hybrid Model Strategy\" is essential for balancing cost and performance. Using a \$30/month subscription model for everything is inefficient; similarly, using a cheap model for complex architecture leads to technical debt.^18^

### 6.1 The 2025 Model Landscape

Analysis of late 2025 community benchmarks and discussions ^8^ suggests the following optimal assignments for a high-performance workflow:

-   **Architect / Orchestrator Mode:** These roles require high reasoning capabilities, the ability to maintain long-term narrative coherence, and a large context window.

    -   *Top Choice:* **Claude 3.5 Sonnet (or Opus 4.5)**. This model is consistently rated highest for complex instruction following and maintaining the \"thread\" of a project over long sessions.^30^

    -   *Alternative:* **DeepSeek R1/V3**. Praised for its reasoning capabilities at a significantly lower price point, making it a viable option for users managing their own API keys.^8^

-   **Code Mode:** This role requires speed, syntax accuracy, and strictly formatted output.

    -   *Top Choice:* **Grok Code Fast** or **DeepSeek V3**. \"Fast code\" models are ideal for the iterative loop of writing functions where deep philosophical reasoning isn\'t required but speed is paramount.^8^

    -   *Alternative:* **Gemini 2.5 Flash**. This model offers an extremely low cost with a massive context window, making it the best choice for reading huge log files or refactoring massive legacy files where token consumption is the primary bottleneck.^8^

-   **Debug Mode:** This role requires logic, causality analysis, and the ability to spot subtle errors.

    -   *Top Choice:* **o1-preview** or **DeepSeek R1** (Thinking Models). These models \"think\" (perform chain-of-thought reasoning) before outputting, making them superior for diagnosing obscure bugs where the error message is misleading.^27^

![](media/image4.png){width="6.458333333333333in" height="5.604166666666667in"}

7. Advanced Configuration & \"Vibe Coding\" Patterns
----------------------------------------------------

\"Vibe Coding\" is a term that has emerged from the Kilo Code and Cline communities to describe a workflow where the developer focuses on the high-level direction (\"The Vibe\") while the AI handles the implementation details.^34^ Facilitating this workflow requires advanced configuration to remove friction.

### 7.1 Auto-Approving Actions (\"YOLO Mode\")

By default, Kilo Code requires explicit user approval for every shell command or file write. While secure, this creates significant friction during rapid development. To maximize speed, power users enable \"Auto-Approve\" for specific actions, a configuration often referred to as \"YOLO Mode\".^19^

-   **Risk:** The primary risk is the agent executing a destructive command (e.g., rm -rf) or overwriting critical files without review.

-   **Mitigation:**

    -   Enable auto-approve for read and browser actions, as these are low-risk operations.

    -   Enable auto-approve for edit only when using a trusted \"Senior\" model (like Claude 3.5 Sonnet) and when working in a Git repository where changes can be easily reverted.

    -   Use .kilocodeignore to explicitly protect sensitive files (like .env, id\_rsa, or production config files) from being touched by the agent, regardless of approval settings.^36^

### 7.2 Rulebook AI & Context Engineering

The community has standardized around tools like **Rulebook AI** to manage prompts and rules across different agents and projects.^37^

-   **Concept:** Instead of manually editing .kilocode/rules for every single project, users can utilize a CLI tool to sync \"Packs\" of rules.

-   **Application:** A \"NextJS Pack\" might automatically inject rules about Server Components, Hydration boundaries, and Image component usage into the Memory Bank instructions. This ensures that the AI never makes a beginner mistake, regardless of which project it is working on.^39^ This \"Context Engineering\" ensures that the agent starts every project with the accumulated wisdom of the developer\'s entire career.

### 7.3 The \"Self-Correction\" Loop

A powerful pattern found in advanced user discussions is the \"Continuous Improvement\" prompt strategy.^40^

-   **Technique:** The user instructs the AI that whenever it encounters a build error due to missing context or a misunderstanding of the project structure, it *must* update a lessons\_learned.md file in the Memory Bank.

-   **Result:** The agent builds a repository of its own failures. Before starting a new task, it checks this file. This prevents the agent from making the same mistake twice (e.g., \"Always use npm run dev instead of yarn start for this project\"). This creates an anti-fragile development loop where the system becomes more robust with every error.

8. Security & Operational Best Practices
----------------------------------------

While maximizing ability is the goal, operational security cannot be ignored. Giving an AI agent shell access and file write permissions carries inherent risks.

### 8.1 The .kilocodeignore File

Just as .gitignore prevents unwanted files from being committed, .kilocodeignore prevents the agent from reading or modifying specific files.

-   **Best Practice:** Always add environment files (.env\*), cryptographic keys, and sensitive configuration files to .kilocodeignore. This prevents the agent from accidentally pasting API keys into a chat window or uploading them to a third-party LLM provider.^36^

### 8.2 Cost Control

Running an agent in \"autonomous loop\" mode can rapidly consume tokens.

-   **Monitoring:** Users should monitor their API usage dashboards (OpenRouter, Anthropic Console) closely.

-   **Limits:** Set hard limits on the number of \"turns\" or \"steps\" an agent can take in a single Orchestrator subtask. This prevents a \"runaway agent\" from entering an infinite debug loop and draining the API credit balance.^41^

9. Conclusion: The Future of the Agentic IDE
--------------------------------------------

Kilo Code represents a maturation of the AI coding landscape. By moving beyond simple text prediction into the realm of **Orchestration**, **Context Management**, and **Tool Use**, it offers a glimpse into a future where developers act as \"Architects\" and AIs act as the \"Builders.\"

To use Kilo Code to its maximum ability is to embrace this shift. It requires:

1.  **Discipline:** Maintaining the Memory Bank as the source of truth.

2.  **Strategy:** Selecting the right models for the right modes and defining custom personas.

3.  **Trust:** Carefully configuring auto-approvals to allow the agent to work at the speed of thought, while implementing safety rails like .kilocodeignore.

As we move through late 2025, the integration of \"Thinking\" models and deeper MCP capabilities will likely make Kilo Code not just an assistant, but the primary interface for software creation. The developers who master this tool today are defining the workflow of tomorrow.

#### Works cited

1.  accessed on December 22, 2025, [[https://techifysolutions.com/blog/ai-coding-assistant-kilo-code/\#:\~:text=One%20such%20tool%20gaining%20attention,debugging%20and%20planning%20entire%20projects.]{.underline}](https://techifysolutions.com/blog/ai-coding-assistant-kilo-code/#:~:text=One%20such%20tool%20gaining%20attention,debugging%20and%20planning%20entire%20projects.)

2.  Kilo Code, The AI Coding Genius That Outshines Cline & Roo Combined! - Apidog, accessed on December 22, 2025, [[https://apidog.com/blog/kilo-code/]{.underline}](https://apidog.com/blog/kilo-code/)

3.  Kilo Code: The Open-Source Agent That\'s Redefining AI Coding Assistants - Data Studios, accessed on December 22, 2025, [[https://www.datastudios.org/post/kilo-code-the-open-source-agent-that-s-redefining-ai-coding-assistants]{.underline}](https://www.datastudios.org/post/kilo-code-the-open-source-agent-that-s-redefining-ai-coding-assistants)

4.  Kilo-Org/kilocode: Kilo is the all-in-one agentic engineering \... - GitHub, accessed on December 22, 2025, [[https://github.com/Kilo-Org/kilocode]{.underline}](https://github.com/Kilo-Org/kilocode)

5.  Kilo Code AI Agent - Visual Studio Marketplace, accessed on December 22, 2025, [[https://marketplace.visualstudio.com/items?itemName=kilocode.Kilo-Code]{.underline}](https://marketplace.visualstudio.com/items?itemName=kilocode.Kilo-Code)

6.  Specialized AI modes in Kilo Code and it\'s changed how I work (new demo video) - Reddit, accessed on December 22, 2025, [[https://www.reddit.com/r/kilocode/comments/1k70lys/specialized\_ai\_modes\_in\_kilo\_code\_and\_its\_changed/]{.underline}](https://www.reddit.com/r/kilocode/comments/1k70lys/specialized_ai_modes_in_kilo_code_and_its_changed/)

7.  Different \"Levels\" of Code mode for different task complexities? : r/kilocode - Reddit, accessed on December 22, 2025, [[https://www.reddit.com/r/kilocode/comments/1m1ndc6/different\_levels\_of\_code\_mode\_for\_different\_task/]{.underline}](https://www.reddit.com/r/kilocode/comments/1m1ndc6/different_levels_of_code_mode_for_different_task/)

8.  Which model do you use for each mode (Architect, Code, Ask, Debug, Orchestrator)? : r/kilocode - Reddit, accessed on December 22, 2025, [[https://www.reddit.com/r/kilocode/comments/1nz0qk1/which\_model\_do\_you\_use\_for\_each\_mode\_architect/]{.underline}](https://www.reddit.com/r/kilocode/comments/1nz0qk1/which_model_do_you_use_for_each_mode_architect/)

9.  Orchestrator Mode: Coordinate Complex Workflows \| Kilo Code Docs, accessed on December 22, 2025, [[https://kilo.ai/docs/basic-usage/orchestrator-mode]{.underline}](https://kilo.ai/docs/basic-usage/orchestrator-mode)

10. Kilo Code 4.19.1: Orchestrator Mode is here! : r/kilocode - Reddit, accessed on December 22, 2025, [[https://www.reddit.com/r/kilocode/comments/1kbhiba/kilo\_code\_4191\_orchestrator\_mode\_is\_here/]{.underline}](https://www.reddit.com/r/kilocode/comments/1kbhiba/kilo_code_4191_orchestrator_mode_is_here/)

11. Kilo Code: The Ultimate Open-Source AI Coding Agent? A Deep Dive Review - Skywork.ai, accessed on December 22, 2025, [[https://skywork.ai/skypage/en/Kilo-Code-The-Ultimate-Open-Source-AI-Coding-Agent-A-Deep-Dive-Review/1974366543654481920]{.underline}](https://skywork.ai/skypage/en/Kilo-Code-The-Ultimate-Open-Source-AI-Coding-Agent-A-Deep-Dive-Review/1974366543654481920)

12. Memory Bank - 10X Your AI Agent Productivity! Cline, Roo, Kilo, Cursor, Windsurf - YouTube, accessed on December 22, 2025, [[https://www.youtube.com/watch?v=w6AJqZ5KpmI]{.underline}](https://www.youtube.com/watch?v=w6AJqZ5KpmI)

13. Give your AI coding agent some more memory - YouTube, accessed on December 22, 2025, [[https://www.youtube.com/watch?v=HaXARtDEiTo]{.underline}](https://www.youtube.com/watch?v=HaXARtDEiTo)

14. Memory Bank \| Kilo Code Docs, accessed on December 22, 2025, [[https://kilo.ai/docs/advanced-usage/memory-bank]{.underline}](https://kilo.ai/docs/advanced-usage/memory-bank)

15. Feature: Setting up memory bank · Kilo-Org kilocode · Discussion \#2022 - GitHub, accessed on December 22, 2025, [[https://github.com/Kilo-Org/kilocode/discussions/2022]{.underline}](https://github.com/Kilo-Org/kilocode/discussions/2022)

16. How to Understand Any Codebase in 5 Minutes Using an AI Coding Assistant \| HackerNoon, accessed on December 22, 2025, [[https://hackernoon.com/how-to-understand-any-codebase-in-5-minutes-using-an-ai-coding-assistant]{.underline}](https://hackernoon.com/how-to-understand-any-codebase-in-5-minutes-using-an-ai-coding-assistant)

17. Memory Bank setup documentation is inconsistent with VSCode Extension behavior · Issue \#3420 · Kilo-Org/kilocode - GitHub, accessed on December 22, 2025, [[https://github.com/Kilo-Org/kilocode/issues/3420]{.underline}](https://github.com/Kilo-Org/kilocode/issues/3420)

18. Kilo Code Orchestrator Mode Guide: INSANE AI Coding Automation - YouTube, accessed on December 22, 2025, [[https://www.youtube.com/watch?v=T9PnGcLromA]{.underline}](https://www.youtube.com/watch?v=T9PnGcLromA)

19. Using MCP in Kilo Code, accessed on December 22, 2025, [[https://kilo.ai/docs/features/mcp/using-mcp-in-kilo-code]{.underline}](https://kilo.ai/docs/features/mcp/using-mcp-in-kilo-code)

20. Context7 MCP Server \-- Up-to-date code documentation for LLMs and AI code editors - GitHub, accessed on December 22, 2025, [[https://github.com/upstash/context7]{.underline}](https://github.com/upstash/context7)

21. Kilo Code + GitHub MCP Server: Revolutionize Your GitHub Workflow Using AI - YouTube, accessed on December 22, 2025, [[https://www.youtube.com/watch?v=egXvZ7\_hEAI]{.underline}](https://www.youtube.com/watch?v=egXvZ7_hEAI)

22. Kilo Code - GitHub, accessed on December 22, 2025, [[https://github.com/Kilo-Org]{.underline}](https://github.com/Kilo-Org)

23. Best Model Choices for Modes (Specifically Autocomplete) : r/kilocode - Reddit, accessed on December 22, 2025, [[https://www.reddit.com/r/kilocode/comments/1mbksyb/best\_model\_choices\_for\_modes\_specifically/]{.underline}](https://www.reddit.com/r/kilocode/comments/1mbksyb/best_model_choices_for_modes_specifically/)

24. Kilo-Org/kilo-dev-mcp-server: A collection of MCP tools used to speed up local development for Kilo Code - GitHub, accessed on December 22, 2025, [[https://github.com/Kilo-Org/kilo-dev-mcp-server]{.underline}](https://github.com/Kilo-Org/kilo-dev-mcp-server)

25. Custom Modes \| Kilo Code Docs, accessed on December 22, 2025, [[https://kilo.ai/docs/features/custom-modes]{.underline}](https://kilo.ai/docs/features/custom-modes)

26. Custom Kilo Code Modes Gallery · Kilo-Org kilocode · Discussion \..., accessed on December 22, 2025, [[https://github.com/Kilo-Org/kilocode/discussions/1671]{.underline}](https://github.com/Kilo-Org/kilocode/discussions/1671)

27. My AI Coding Tool Configuration Journey (Cloud Code → KiloCode, Free & Paid Models), accessed on December 22, 2025, [[https://www.reddit.com/r/kilocode/comments/1nrtb7d/my\_ai\_coding\_tool\_configuration\_journey\_cloud/]{.underline}](https://www.reddit.com/r/kilocode/comments/1nrtb7d/my_ai_coding_tool_configuration_journey_cloud/)

28. The 2025 AI Coding Models: Comprehensive Guide to the Top 5 Contenders - CodeGPT, accessed on December 22, 2025, [[https://www.codegpt.co/blog/ai-coding-models-2025-comprehensive-guide]{.underline}](https://www.codegpt.co/blog/ai-coding-models-2025-comprehensive-guide)

29. Best Open Models in December 2025 : r/AIAgentsInAction - Reddit, accessed on December 22, 2025, [[https://www.reddit.com/r/AIAgentsInAction/comments/1pi8kkq/best\_open\_models\_in\_december\_2025/]{.underline}](https://www.reddit.com/r/AIAgentsInAction/comments/1pi8kkq/best_open_models_in_december_2025/)

30. Kilocode with Claude Code low performance - Reddit, accessed on December 22, 2025, [[https://www.reddit.com/r/kilocode/comments/1p8rczf/kilocode\_with\_claude\_code\_low\_performance/]{.underline}](https://www.reddit.com/r/kilocode/comments/1p8rczf/kilocode_with_claude_code_low_performance/)

31. Best AI Models for Agentic Vibe Coding in VS Code (December 2025) - DEV Community, accessed on December 22, 2025, [[https://dev.to/danishashko/best-ai-models-for-agentic-vibe-coding-in-vs-code-december-2025-3bkd]{.underline}](https://dev.to/danishashko/best-ai-models-for-agentic-vibe-coding-in-vs-code-december-2025-3bkd)

32. Why use Replit when we got Kilo now? - Reddit, accessed on December 22, 2025, [[https://www.reddit.com/r/replit/comments/1kq9w6r/why\_use\_replit\_when\_we\_got\_kilo\_now/]{.underline}](https://www.reddit.com/r/replit/comments/1kq9w6r/why_use_replit_when_we_got_kilo_now/)

33. AMD tested 20+ local models for coding & only 2 actually work (testing linked) - Reddit, accessed on December 22, 2025, [[https://www.reddit.com/r/LocalLLaMA/comments/1nufu17/amd\_tested\_20\_local\_models\_for\_coding\_only\_2/]{.underline}](https://www.reddit.com/r/LocalLLaMA/comments/1nufu17/amd_tested_20_local_models_for_coding_only_2/)

34. Context Engineering: End of Vibe Coding! 100x Better Than Vibe Coding /w Inngest (Full Tutorial) - YouTube, accessed on December 22, 2025, [[https://www.youtube.com/watch?v=iOYg8JSazvU]{.underline}](https://www.youtube.com/watch?v=iOYg8JSazvU)

35. The Complete Guide to Vibe Coding: Best Practices for AI-Powered Development - Medium, accessed on December 22, 2025, [[https://medium.com/\@cem.karaca/the-complete-guide-to-vibe-coding-best-practices-for-ai-powered-development-5529dedfd2a7]{.underline}](https://medium.com/@cem.karaca/the-complete-guide-to-vibe-coding-best-practices-for-ai-powered-development-5529dedfd2a7)

36. Kilo: A text editor in less than 1000 LOC with syntax highlight and search \| Hacker News, accessed on December 22, 2025, [[https://news.ycombinator.com/item?id=44034459]{.underline}](https://news.ycombinator.com/item?id=44034459)

37. botingw/pm-workflow-copilot-ide: AI PM (product management) assistant for AI coding IDEs (Cline, Cursor). Follows the detailed product\_management\_workflow\_startup.md for guided product definition & doc creation. - GitHub, accessed on December 22, 2025, [[https://github.com/botingw/pm-workflow-copilot-ide]{.underline}](https://github.com/botingw/pm-workflow-copilot-ide)

38. botingw/rulebook-ai: Elevate vibe coding to vibe engineering: Get consistent Github Copilot custom instructions, Cursor, Roo Code, Cline, Windsurf, Claude Code, Gemini Cli, Codex CLI, kilo code, warp custom rules via a universal, managed template. Features vibe coding memory bank & best practices for large codebases., accessed on December 22, 2025, [[https://github.com/botingw/rulebook-ai]{.underline}](https://github.com/botingw/rulebook-ai)

39. I like Copilot for boilerplate, but it lacks project-specific memory. I built an open-source tool to give it one : r/GithubCopilot - Reddit, accessed on December 22, 2025, [[https://www.reddit.com/r/GithubCopilot/comments/1ngevk2/i\_like\_copilot\_for\_boilerplate\_but\_it\_lacks/]{.underline}](https://www.reddit.com/r/GithubCopilot/comments/1ngevk2/i_like_copilot_for_boilerplate_but_it_lacks/)

40. How to make Kilo Code improve itself : r/kilocode - Reddit, accessed on December 22, 2025, [[https://www.reddit.com/r/kilocode/comments/1mtyqlh/how\_to\_make\_kilo\_code\_improve\_itself/]{.underline}](https://www.reddit.com/r/kilocode/comments/1mtyqlh/how_to_make_kilo_code_improve_itself/)

41. Love Kilo Code, but API usage is too expensive : r/kilocode - Reddit, accessed on December 22, 2025, [[https://www.reddit.com/r/kilocode/comments/1lvbdl8/love\_kilo\_code\_but\_api\_usage\_is\_too\_expensive/]{.underline}](https://www.reddit.com/r/kilocode/comments/1lvbdl8/love_kilo_code_but_api_usage_is_too_expensive/)

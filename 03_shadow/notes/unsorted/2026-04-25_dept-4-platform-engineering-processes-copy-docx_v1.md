---
title: "**Table of Contents**"
id: "dept-4-platform-engineering-processes-copy-docx"
version: 1
created: "2026-04-25"
type: "document"
topic_type: "unsorted"
audience: "internal"
layer: "shadow"
status: "filed"
signed_by: "Devon, 2026-04-25, devin-992682c244cf444f91e0a516498afbfd"
---

  
**Platform & Engineering**

Process Handbook

*AI agent architecture, code pipelines, build quality, infrastructure, deployment, context management*

Amplified Partners

21 March 2026

**CONFIDENTIAL**

# **Table of Contents**

# **Introduction**

This Process Handbook documents every actionable process within the Platform & Engineering department at Amplified Partners. Each process is defined with its name, purpose, trigger, numbered steps, inputs, outputs, owner, tools/skills required, and frequency.

Steps marked \[DERIVED\] have been inferred from the source methodology descriptions to create complete, actionable process flows. All other steps are directly documented in the source material.

This handbook is designed to be self-contained: any team member should be able to execute any process by following the steps documented here.

# **Processes**

## **1\. AI Board Governance Decision Process**

| Purpose | Govern high-stakes AI decisions through a 5-seat board with believability-weighted voting, ensuring diverse perspective consideration and adversarial challenge before finalisation. |
| :---- | :---- |
| **Trigger** | Agent confidence gate flags a decision below 85% confidence threshold. |
| **Owner** | TBD (Automated — ExecutiveDiscussionWorkflow) |
| **Frequency** | On demand — whenever agent confidence gate triggers. |

**Steps**

1. Receive flagged decision from agent confidence gate (\<85% confidence).

2. ExecutiveDiscussionWorkflow (Temporal) initiates the board session.

3. CEO (Claude Opus) provides strategic/visionary input on the decision.

4. COO (Llama 70B local) provides operational/execution input.

5. CFO/Enforcer (GPT-4.1-mini) provides compliance/standards input.

6. CTO (Claude Sonnet) provides technical/architecture input.

7. Nemesis (Gemini Pro) challenges every proposed position from all board members.

8. Facilitator (Llama 3.1:8b) applies believability-weighted voting algorithm, weighting each input by the board member's 90-day rolling track record for that decision type.

9. Weighted vote produces a decision outcome with confidence score.

10. If confidence \<70%: escalate to human review. **\[DERIVED\]**

11. Document decision with reasoning, dissent, and confidence score. **\[DERIVED\]**

12. Return decision to originating workflow. **\[DERIVED\]**

| Inputs | High-stakes decision flagged by agent confidence gate (\<85%); board member 90-day performance history. |
| :---- | :---- |
| **Outputs** | Board decision with documented reasoning, dissent, and confidence score. |
| **Tools / Skills** | Temporal (ExecutiveDiscussionWorkflow), Claude Opus, Llama 70B, GPT-4.1-mini, Claude Sonnet, Gemini Pro, Llama 3.1:8b |

## **2\. Agent Autonomy Configuration (Blinkers Without Ceilings)**

| Purpose | Define operational constraints for each agent role while ensuring no ceiling is placed on output quality within those constraints. |
| :---- | :---- |
| **Trigger** | New agent role creation or existing role modification. |
| **Owner** | TBD (Platform Engineering Lead) |
| **Frequency** | On each new agent role creation or role modification. |

**Steps**

1. Define the blinkers: task scope boundaries, ethical constraints, voice guidelines for the agent role.

2. Remove the ceiling: explicitly configure the agent to achieve the highest possible quality within its blinkers. **\[DERIVED\]**

3. Document blinker definitions in the agent's Mission Document (MD). **\[DERIVED\]**

4. Apply selectively: test on surface data in the real environment first.

5. Take across the research and development department for broader testing.

6. For content agents: ensure voice guidelines (blinkers) allow personality expression within them.

7. Deploy to production once testing validates quality within constraints. **\[DERIVED\]**

8. Monitor agent outputs for boundary violations and quality levels. **\[DERIVED\]**

| Inputs | Agent role definition; task specification; ethical constraints. |
| :---- | :---- |
| **Outputs** | Configured agent with defined constraints and no quality ceiling; documented Mission Document. |
| **Tools / Skills** | Mission Documents (MDs), Agent Constitution, SOUL.md |

## **3\. Three-Brain Data Isolation & Federated Learning**

| Purpose | Maintain strict data isolation between Amplified's core knowledge, individual clients, and cross-client pattern sharing via PUDDING labels. |
| :---- | :---- |
| **Trigger** | New client onboarding; cross-client pattern identified; knowledge vault update. |
| **Owner** | TBD (Data Architecture Lead) |
| **Frequency** | Continuous — on every client data interaction and pattern improvement. |

**Steps**

1. Amplified Brain: Store proprietary frameworks, research, and patterns in the core knowledge vault — never visible to clients.

2. Per-Client Brain: Create hard-isolated client vault containing the client's data, processes, and business brain. **\[DERIVED\]**

3. Enforce hard isolation: client agents never see the Amplified Brain; Amplified agents never mix raw client data.

4. When a client process improves (e.g., to AMPS 7+), extract the improvement pattern using PUDDING labels. **\[DERIVED\]**

5. Federated/Network Brain: Store PUDDING-labelled patterns only (no raw data) for cross-client compound learning.

6. Distribute applicable patterns to other clients: e.g., plumber's scheduling improvement informs restaurant's table booking via PUDDING labels.

7. Audit isolation boundaries periodically to ensure no data leakage. **\[DERIVED\]**

| Inputs | Separate client vaults; PUDDING-labelled pattern extracts. |
| :---- | :---- |
| **Outputs** | Compound learning benefit for each client without privacy violation; network effects without data sharing. |
| **Tools / Skills** | PUDDING Technique, Sovereignty Stack, Vault system |

## **4\. AMPS Scoring & DC-7 Improvement Cycle**

| Purpose | Score any process on the 0–10 AMPS maturity scale and raise its floor through a structured 7-step improvement cycle. |
| :---- | :---- |
| **Trigger** | Process below AMPS target threshold; scheduled review; new process creation. |
| **Owner** | TBD (Process Owner \+ Kaizen Department) |
| **Frequency** | Per process review cycle; continuous for active improvement targets. |

**Steps**

1. Decompose — Break the process into its component steps.

2. Score — Apply the 6-dimension AMPS rubric (0–10) to each component.

3. Research — Find best-in-class approaches for each low-scoring component; use PUDDING for cross-domain discovery.

4. Design — Redesign the low-scoring components using findings from the Research step.

5. Test — Test the redesigned process against real conditions and chaos scenarios.

6. Validate — Validate against the AMPS rubric; confirm improvement on at least 4/6 dimensions without regressions.

7. Reassemble — Put the improved process back together; set new AMPS floor; document in vault.

8. If AMPS ≥ 7.0: mark as shippable. If \<7.0: return to step 1 for another cycle. **\[DERIVED\]**

| Inputs | Any process (AI agent workflow or business process) below AMPS target. |
| :---- | :---- |
| **Outputs** | AMPS score per process (0–10); improvement roadmap; ship/no-ship decision. |
| **Tools / Skills** | AMPS rubric worksheets, PUDDING Technique, DC-7 cycle templates, Vault |

## **5\. Build Quality Gate (BQF / Universal Quality Gate)**

| Purpose | Apply the two-question quality gate to every build output before shipping, enforced programmatically via the QualityGateWorkflow. |
| :---- | :---- |
| **Trigger** | Any build output ready for review — code, content, agent response, or deployment. |
| **Owner** | TBD (Automated — QualityGateWorkflow) |
| **Frequency** | On every build output — continuous. |

**Steps**

1. Question 1: Does it help the person? If NO — do not ship. Stop here.

2. Question 2: Could we do better? If YES — iterate before shipping.

3. Apply at every stage: planner output, architect decomposition, code generation, quality review, deployment. **\[DERIVED\]**

4. QualityGateWorkflow runs programmatically: execute automated tests.

5. Apply rubric scoring against the output.

6. Enforcer agent (GPT-4.1-mini) reviews the output against its rubric.

7. Security scan executed.

8. Calculate PRS score from all quality dimensions. **\[DERIVED\]**

9. If PRS score ≥7.0: approve for shipping.

10. If PRS score \<7.0: flag for rebuild and return to development. **\[DERIVED\]**

| Inputs | Any build output (code, content, deployment artifact). |
| :---- | :---- |
| **Outputs** | Ship / iterate / discard decision; PRS score. |
| **Tools / Skills** | QualityGateWorkflow (Temporal), Enforcer agent (GPT-4.1-mini), Security scanner, AMPS rubric |

## **6\. Chaos Testing Schedule (Nightly Progressive Injection)**

| Purpose | Validate system resilience by progressively injecting failure scenarios nightly, discovering failure modes before they reach production. |
| :---- | :---- |
| **Trigger** | Automated schedule — nightly at 01:00 UTC. |
| **Owner** | TBD (Automated — ChaosWorkflow) |
| **Frequency** | Nightly, 01:00–04:00 UTC. |

**Steps**

1. ChaosWorkflow (Temporal) initiates automatically at 01:00 UTC.

2. Verify scope restrictions: confirm PostgreSQL data and Temporal state are excluded from chaos runs.

3. Execute Pillar 1: Network failure scenarios.

4. Execute Pillar 2: Service failure scenarios.

5. Execute Pillar 3: Host failure scenarios.

6. Execute Pillar 4: Data failure scenarios (excluding production data).

7. Progressive escalation: start with mild failures (single service outage), escalate to cascade failures, network partitions, data corruption scenarios. **\[DERIVED\]**

8. Generate chaos report documenting all scenarios run and outcomes.

9. Add report to vault post-mortems.

10. Feed discovered failure modes into KaizenWorkflow for continuous improvement. **\[DERIVED\]**

| Inputs | Running production system; chaos scenario library. |
| :---- | :---- |
| **Outputs** | Resilience validation report; discovered failure modes documented and fed into Kaizen. |
| **Tools / Skills** | ChaosWorkflow (Temporal), Chaos Mesh, Gremlin, Vault |

## **7\. CI/CD Gates Pipeline (8-Gate Deployment)**

| Purpose | Ensure every code push passes 8 sequential quality gates before deployment to Beast, with automated AI-powered code review. |
| :---- | :---- |
| **Trigger** | Git push event to the repository. |
| **Owner** | TBD (Automated — GitHub Actions) |
| **Frequency** | On every git push. |

**Steps**

1. Gate 1: Lint — run code linting against style rules.

2. Gate 2: Types — run type checking.

3. Gate 3: Security scan — run automated security scanning.

4. Gate 4: Unit tests — execute all unit tests.

5. Gate 5: Integration tests — execute integration test suite.

6. Gate 6: Enforcer agent review — GPT-4.1-mini runs 10 iterations autonomously against changed files using its rubric.

7. Gate 7: Docker build — build the Docker container.

8. Gate 8: Deploy to Beast — deploy the built container to Beast server.

9. If any gate fails: halt pipeline, notify developer, log failure. **\[DERIVED\]**

10. All gates must pass sequentially before deployment proceeds. **\[DERIVED\]**

| Inputs | Git push event; changed files. |
| :---- | :---- |
| **Outputs** | Pass/fail per gate; deployment to Beast if all 8 pass. |
| **Tools / Skills** | GitHub Actions (.github/workflows/gates.yml), GPT-4.1-mini (enforcer), Docker, Beast server |

## **8\. Cautious Alpha Deployment Protocol**

| Purpose | Gate production deployment behind \>95% synthetic testing confidence, with graduated rollout based on confidence bands. |
| :---- | :---- |
| **Trigger** | Completed build output ready for production deployment. |
| **Owner** | TBD (Release Engineering) |
| **Frequency** | On every production deployment decision. |

**Steps**

1. Run Synthetic Testing at Scale: 20,000 tests against 1,000 simulated fake businesses.

2. Calculate confidence score across all test dimensions.

3. If confidence ≥95%: proceed to full production deployment.

4. If confidence 85–94%: deploy as canary to 5% of traffic.

5. Monitor canary deployment for 24 hours. **\[DERIVED\]**

6. If canary stable after 24 hours: proceed to full deployment. **\[DERIVED\]**

7. If canary shows issues: roll back and return to development. **\[DERIVED\]**

8. If confidence \<85%: do not deploy; return to development.

9. Log all deployment decisions to Linear with confidence scores.

| Inputs | Completed build output; synthetic test results. |
| :---- | :---- |
| **Outputs** | Production deployment decision with documented confidence threshold. |
| **Tools / Skills** | Synthetic Testing framework, Beast server, Linear, Canary deployment tooling |

## **9\. Cove Code Factory Build Pipeline**

| Purpose | Take a Linear issue and orchestrate a chain of specialised AI agents through Temporal workflows to produce committed, tested, deployed code. |
| :---- | :---- |
| **Trigger** | Linear issue ID posted or raw text description submitted to cove.beast.amplifiedpartners.ai/build. |
| **Owner** | TBD (Automated — Temporal Orchestrator) |
| **Frequency** | On demand — per Linear issue or build request. |

**Steps**

1. Receive input: Linear issue ID (e.g. COV-285) or raw text description.

2. PlannerWorkflow: architect decomposes the issue → produces validated build plan with task DAG.

3. ProjectOrchestrator: executes the DAG — runs tasks in dependency order.

4. BuildWorkflow: for each task — code → test → commit. Uses git worktrees for isolation. Coder agent (claude-sonnet, up to 25 iterations).

5. QualityGateWorkflow: post-build quality checks — rubrics, enforcer agent review, security scan. Universal Quality Gate applied.

6. If quality gate fails: SelfhealWorkflow triggers auto-recovery. **\[DERIVED\]**

7. SecurityWorkflow: security scanning of built code.

8. Update Linear issue with build status, workflow ID, and Temporal run ID. **\[DERIVED\]**

9. Deploy code to Beast via CI/CD Gates Pipeline. **\[DERIVED\]**

| Inputs | Linear issue ID or raw text description. |
| :---- | :---- |
| **Outputs** | Committed, tested, deployed code; workflow ID; Temporal run ID; Linear issue updated. |
| **Tools / Skills** | Temporal (10 workflows), Claude Sonnet (coder), Claude Opus (architect/security), GPT-4.1-mini (enforcer), Git worktrees, Linear, Beast server |

## **10\. Kaizen-While-Building Daily Rhythm**

| Purpose | Apply Kaizen's 0.5%/day compounding improvement to software development through a structured human+AI daily build rhythm. |
| :---- | :---- |
| **Trigger** | Start of each working day (human); 03:00 UTC daily (automated KaizenWorkflow). |
| **Owner** | TBD (Engineering team \+ Automated KaizenWorkflow) |
| **Frequency** | Daily — human rhythm \+ automated 03:00 UTC workflow. |

**Steps**

1. Morning standup: review SESSION-STATE.md; set daily targets using Telegraph Pole orientation.

2. Build: apply Blinkers Without Ceilings — focused but unceiled work.

3. Milestone micro-retrospective: at each milestone (not just session end), conduct brief retrospective — what worked? what's blocking?

4. Evening handover: update SESSION-STATE.md; produce Session Self-Rating YAML; update vault.

5. KaizenWorkflow (automated, 03:00 UTC): scan vault post-mortems from last 24 hours.

6. Identify safe improvement opportunities (score improvement \>0.5%, no regression \>1%).

7. Apply safe fixes automatically (auto-merge if human approves).

8. Flag non-safe improvements to Kaizen Department for human review.

9. Update AMPS floor scores for improved processes.

| Inputs | Running system; session post-mortems; build logs. |
| :---- | :---- |
| **Outputs** | Compounding 0.5%/day improvement; continuously improving codebase; never-stale process documentation. |
| **Tools / Skills** | KaizenWorkflow (Temporal), SESSION-STATE.md, Session Self-Rating YAML, Vault, AMPS rubric |

## **11\. Code Taxonomy & Kaizen Validation**

| Purpose | Ensure all code is correctly categorised within the 7-category/35-pattern taxonomy and that all improvements meet Kaizen acceptance criteria. |
| :---- | :---- |
| **Trigger** | Any code change, improvement proposal, or error. |
| **Owner** | TBD (Engineering team) |
| **Frequency** | On every code change. |

**Steps**

1. Before writing new code: search the code taxonomy for existing implementations. **\[DERIVED\]**

2. Categorise the code change within the 7 categories and 35 patterns.

3. If the change is an improvement: verify Kaizen acceptance criteria — score improvement \> 0.5% AND no dimension regresses \> 1%.

4. Submit for human approval. **\[DERIVED\]**

5. If fixing an error: research the error pattern before fixing (error research requirement).

6. Test all code changes before commit (continuous testing requirement).

7. Update the code taxonomy if a new pattern is identified. **\[DERIVED\]**

8. Cross-reference with Dual Code Organisation View 2 (.patterns/ directory). **\[DERIVED\]**

| Inputs | Any code change, improvement proposal, or error. |
| :---- | :---- |
| **Outputs** | Correctly categorised code; Kaizen-validated improvements; compound learning from error patterns. |
| **Tools / Skills** | Code taxonomy, Kaizen acceptance criteria, Dual Code Organisation (.patterns/), Test suite |

## **12\. Dual Code Organisation Maintenance**

| Purpose | Maintain two simultaneous views of the codebase — functional and pattern-based — to enable compound learning and identify open-source extraction candidates. |
| :---- | :---- |
| **Trigger** | New code commit; pattern usage threshold reached. |
| **Owner** | TBD (Engineering team) |
| **Frequency** | On every code commit; periodic pattern threshold reviews. |

**Steps**

1. View 1 (Functional): maintain standard module/function directory structure — code organised by what it does.

2. View 2 (Pattern): maintain .patterns/ directory with instances.yaml — track every pattern instance across the codebase.

3. Categorise patterns across 7 categories: Resilience, Performance, Data Integrity, Orchestration, AI/LLM, Security, Observability.

4. Apply cross-index triggers: N≥2 uses → trigger notification. **\[DERIVED\]**

5. N≥3 uses → create canonical pattern (document and standardise). **\[DERIVED\]**

6. N≥5 uses → flag as candidate for open-source extraction. **\[DERIVED\]**

7. Run Automated Refinement Stack: Semgrep \+ SonarQube (static analysis), Copilot agent (80% of routine fixes), Kaizen Department (20% that matters). **\[DERIVED\]**

8. Maintain coverage target: 40–60% (important paths, not everything).

| Inputs | Any codebase; new code commits. |
| :---- | :---- |
| **Outputs** | Two-view codebase with tracked pattern instances; compound learning from pattern reuse; open-source extraction candidates. |
| **Tools / Skills** | instances.yaml, .patterns/ directory, Semgrep, SonarQube, Copilot agent, Kaizen Department |

## **13\. Cove Agent Prompt Assembly (4-Layer)**

| Purpose | Assemble every agent prompt through the 4-layer architecture to ensure constitutional compliance, current context, role-specific instructions, and task context. |
| :---- | :---- |
| **Trigger** | Any agent invocation in the Cove Code Factory. |
| **Owner** | TBD (Automated — prompt\_loader.py) |
| **Frequency** | On every agent invocation. |

**Steps**

1. prompt\_loader.py initiates prompt assembly for the specified agent role.

2. Layer 0 — Amplified Laws (IMMUTABLE): load Eight Laws from layer0\_laws.py; prepend to system prompt. Cannot be overridden.

3. Layer 1 — Knowledge Base: inject contents from knowledge\_base.md — current Amplified context, technical standards, architectural decisions.

4. Layer 2 — Platform Prompts: load role-specific instructions from agents/prompts/{role}.md.

5. Layer 3 — Task Context: inject runtime task context — Linear issue, build task description, repo context, task-level constraints.

6. Validate assembled prompt contains all four layers. **\[DERIVED\]**

7. Pass assembled prompt to the agent for execution. **\[DERIVED\]**

| Inputs | Agent role; task context; knowledge\_base.md contents. |
| :---- | :---- |
| **Outputs** | Complete assembled system prompt for the agent. |
| **Tools / Skills** | prompt\_loader.py, layer0\_laws.py, knowledge\_base.md, agents/prompts/{role}.md, Linear |

## **14\. Session Self-Rating & Post-Mortem**

| Purpose | Produce structured self-assessment artefacts at the end of every AI session to feed the continuous improvement memory system. |
| :---- | :---- |
| **Trigger** | End of any AI work session. |
| **Owner** | TBD (Every AI agent) |
| **Frequency** | End of every AI session (Operational Law 4). |

**Steps**

1. Complete Session Self-Rating YAML: date, tasks attempted, tasks completed, tasks flagged unfinished, quality score (X/10), efficiency score (X/10).

2. Document learning: 'What did I learn this session that I didn't know before?'

3. Document mistake: 'What did I do wrong or could have done better?'

4. Document improvement: 'What will I do differently next time?'

5. For build sessions — complete full Post-Mortem YAML: session\_id, agent\_model, linear\_issue, duration, task\_summary, what succeeded, what failed.

6. Document architecture decisions with reasoning, confidence, and would-do-differently. **\[DERIVED\]**

7. Document known limitations and debt created.

8. Provide next\_agent\_advice for the subsequent session.

9. Save to vault as episodic memory for next session's agent. **\[DERIVED\]**

10. Feed into KaizenWorkflow for automated improvement scanning. **\[DERIVED\]**

| Inputs | Any completed or failed AI work session. |
| :---- | :---- |
| **Outputs** | Vault document enabling next agent to avoid past mistakes; AMPS floor update; Kaizen improvement feed. |
| **Tools / Skills** | Session Self-Rating YAML template, Post-Mortem YAML template, Vault, KaizenWorkflow |

## **15\. Synthetic Testing at Scale**

| Purpose | Provide statistical confidence across the full diversity of SMB client profiles by running 20,000 tests before deployment. |
| :---- | :---- |
| **Trigger** | New feature or agent ready for deployment validation. |
| **Owner** | TBD (QA / Automated testing) |
| **Frequency** | Before every production deployment. |

**Steps**

1. Generate 1,000 synthetic SMB profiles covering the full diversity of client types (trades, retail, professional services, etc.).

2. Define 20 test scenarios per business \= 20,000 total tests. **\[DERIVED\]**

3. Run all tests in parallel via Beast's compute capacity.

4. Measure against success thresholds: 99% interview completion rate; 95% data extraction accuracy.

5. Collate results across all 20,000 tests. **\[DERIVED\]**

6. If all thresholds met: Cautious Alpha threshold satisfied — proceed to deployment gate.

7. If thresholds not met: identify failure patterns and log to vault. **\[DERIVED\]**

8. Log all failures to vault for Kaizen improvement.

| Inputs | New feature or agent; 1,000 synthetic business profiles. |
| :---- | :---- |
| **Outputs** | Statistical confidence score; failure log for Kaizen improvement. |
| **Tools / Skills** | Synthetic profile generator, Beast server, Vault, Cautious Alpha Protocol |

## **16\. 705-Case Golden Dataset Regression Testing**

| Purpose | Validate that model changes and prompt updates do not degrade performance below the established baseline. |
| :---- | :---- |
| **Trigger** | Any model change, prompt update, or feature update. |
| **Owner** | TBD (QA / Model validation) |
| **Frequency** | On every model change, prompt update, or feature update. |

**Steps**

1. Identify the change to be validated (model version, prompt change, or feature update). **\[DERIVED\]**

2. Run the 705 test cases using promptfoo against the golden dataset.

3. For each test case: compare output against expected output, acceptable variants, and failure modes.

4. Calculate aggregate score across all 705 cases. **\[DERIVED\]**

5. Verify score ≥ baseline established by previous validated version.

6. If score ≥ baseline: approve the change for deployment. **\[DERIVED\]**

7. If score \< baseline: reject the change; document regression details. **\[DERIVED\]**

8. Update baseline if the new version establishes a higher standard. **\[DERIVED\]**

| Inputs | New model version, prompt change, or feature update. |
| :---- | :---- |
| **Outputs** | Pass/fail against 705-case benchmark; regression detection. |
| **Tools / Skills** | promptfoo, 705-case golden dataset, Cove Code Factory Pipeline |

## **17\. API Key Rotation & Secrets Management**

| Purpose | Manage API keys and secrets across the Amplified infrastructure with scheduled rotation and per-service spending visibility. |
| :---- | :---- |
| **Trigger** | Rotation schedule (30 days for critical, 90 days for standard); new service onboarding. |
| **Owner** | TBD (Infrastructure / DevOps) |
| **Frequency** | Critical keys: every 30 days. Standard keys: every 90 days. |

**Steps**

1. Store all secrets in environment variables — never hardcode in source.

2. Assign keys to services (not developers) via LiteLLM proxy.

3. On rotation trigger: generate new key for the service.

4. Update environment variables with the new key.

5. Test the new key to verify connectivity and functionality. **\[DERIVED\]**

6. Deprecate the old key (keep active for 7-day overlap period).

7. After 7-day overlap: delete the old key.

8. Track all key usage through LiteLLM proxy for per-service spending visibility.

| Inputs | Service API credentials; rotation schedule trigger. |
| :---- | :---- |
| **Outputs** | Rotated, isolated, tracked API keys; per-service spending visibility. |
| **Tools / Skills** | LiteLLM proxy, Environment variable management, Key generation tools |

## **18\. P2 Tokenization & Privacy Absolute Pipeline**

| Purpose | Replace all PII with four-word random tokens before data leaves the edge device, ensuring GDPR Article 17 compliance and absolute privacy. |
| :---- | :---- |
| **Trigger** | Client data entering the system at the edge device. |
| **Owner** | TBD (Privacy Engineering) |
| **Frequency** | Continuous — on every client data ingestion. |

**Steps**

1. Client data enters at the edge device (PicoClaw — Beelink N100).

2. PII detection: identify all personally identifiable information in the data. **\[DERIVED\]**

3. Extract PII and store locally in the Identity Vault (never leaves edge).

4. Generate four-word random ID (51.6-bit entropy) to replace PII in all outbound data.

5. Tokenised data flows to Beast via Tailscale mesh networking.

6. All AI processing operates on tokenised data only — agents never see PII.

7. If original PII needed (e.g., for communications): request back through the Identity Vault API.

8. For existing integrations: apply 'Gradual Ghost' transition — migrate progressively to four-word IDs without disruption.

| Inputs | Client PII-containing data. |
| :---- | :---- |
| **Outputs** | Tokenised, privacy-preserving data stream; GDPR-compliant processing record. |
| **Tools / Skills** | PicoClaw edge device (Beelink N100), Identity Vault, Tailscale mesh, Four-word ID generator |

## **19\. MCP Server Registry & Capability Routing**

| Purpose | Manage multiple MCP servers as Docker containers, routing agent tool calls to the correct capability server via the MCPPool. |
| :---- | :---- |
| **Trigger** | Agent tool call requiring external capability; new capability server deployment. |
| **Owner** | TBD (Platform Engineering) |
| **Frequency** | On every agent tool call requiring external capability. |

**Steps**

1. Register each capability as a separate MCP server in the MCPPool (filesystem, GitHub, shell, Telegram, database, etc.).

2. All servers run as Docker containers for isolation. **\[DERIVED\]**

3. Agent makes a tool call requiring an external capability.

4. MCPPool routes the tool call to the correct MCP server via JSON-RPC over stdio.

5. MCP server executes the capability and returns the result.

6. MCPPool returns the execution result to the requesting agent. **\[DERIVED\]**

7. For Amplified-specific capabilities: build custom FastMCP servers. **\[DERIVED\]**

8. Monitor server health and connection status via MCPPool context manager. **\[DERIVED\]**

| Inputs | Agent tool call; task requiring external capability. |
| :---- | :---- |
| **Outputs** | Tool execution result returned to agent. |
| **Tools / Skills** | MCPPool (mcp\_bridge.py), Docker, JSON-RPC, 7 registered MCP servers (filesystem\_mcp, github\_mcp, shell\_mcp, telegram\_mcp, nightscout\_mcp, email\_mcp, postgresql\_mcp) |

## **20\. Operations Register Maintenance**

| Purpose | Maintain a comprehensive register of all operational processes, tracking current state vs. ideal state for AMPS scoring and improvement prioritisation. |
| :---- | :---- |
| **Trigger** | Quarterly planning cycle; new process creation; process state change. |
| **Owner** | TBD (Operations Lead) |
| **Frequency** | Quarterly review cycle; on-demand for process changes. |

**Steps**

1. Enumerate all operational processes across Amplified. **\[DERIVED\]**

2. For each process: assign process ID, document name, description.

3. Define ideal state for each process.

4. Assess current state against ideal state.

5. Document how to achieve ideal state from current state. **\[DERIVED\]**

6. Classify enforcement type (hard/soft) and link related rules.

7. Set process status (active, planned, deprecated). **\[DERIVED\]**

8. Review and update at each quarterly planning cycle.

9. Use as the master reference for the AMF and process improvement prioritisation. **\[DERIVED\]**

| Inputs | All Amplified operational processes. |
| :---- | :---- |
| **Outputs** | Comprehensive process register; basis for AMPS scoring and improvement prioritisation. |
| **Tools / Skills** | Operations Register (XLSX, no merged cells), AMF, AMPS rubric |

## **21\. VALIDATION-METHODOLOGY Execution (PUDDING Label Validation)**

| Purpose | Validate PUDDING label assignments through formal inter-rater reliability testing using Krippendorff's Alpha, ensuring consistent and reproducible taxonomy application. |
| :---- | :---- |
| **Trigger** | New PUDDING labels assigned; validation cycle; codebook revision. |
| **Owner** | TBD (Methodology / Research Lead) |
| **Frequency** | Per validation cycle; on codebook revision. |

**Steps**

1. Phase 1: Apply Ranganathan PMEST mapping to confirm PUDDING's 4-position system maps correctly (PMEST minus Matter facet).

2. Phase 2: Select 20 atoms for inter-rater reliability test across all 4 facets.

3. Assign multiple independent coders to label the 20 atoms. **\[DERIVED\]**

4. Calculate Krippendorff's Alpha: target α ≥ 0.8 (strong), accept α ≥ 0.667 (tentative).

5. If α \< 0.667: refine codebook and repeat. **\[DERIVED\]**

6. Phase 3: Apply Brown et al. (2020) iterative protocol — 6–8 coders, measure agreement, refine codebook, repeat until threshold met.

7. Validate against 11 mapped rubrics and check for 12 defined error patterns (E1–E12). **\[DERIVED\]**

8. Document validation results and update codebook. **\[DERIVED\]**

| Inputs | PUDDING-labelled atoms; multiple independent coders. |
| :---- | :---- |
| **Outputs** | Validated PUDDING taxonomy with provable inter-rater reliability; enforced quality gates. |
| **Tools / Skills** | PUDDING codebook, Krippendorff's Alpha calculator, 11 rubrics (RAEI, PRS, AMPS, etc.), Brown et al. (2020) iterative protocol |

## **22\. Visual Polish System Improvement Cycle**

| Purpose | Continuously measure and improve the visual quality of React-based UIs through composite scoring and controlled experiments. |
| :---- | :---- |
| **Trigger** | New UI component; visual quality review; design system update. |
| **Owner** | TBD (Design Engineering) |
| **Frequency** | On every UI change; periodic design system reviews. |

**Steps**

1. Run composite scoring: 40% UIClip (fast, broad aesthetic scoring) \+ 60% LLM rubric (slow, nuanced).

2. Score across 5 dimensions: Layout (23%), Colour Contrast (21%), Text Readability (19%), Button Usability (20%), Learnability (20%).

3. Identify lowest-scoring dimensions for improvement. **\[DERIVED\]**

4. Propose improvement: max delta per experiment \= 2 token changes, 1 category only (prevents compound changes masking causes).

5. Implement the proposed token changes. **\[DERIVED\]**

6. Re-score: verify Kaizen acceptance criteria — score improvement \>0.5% AND no dimension regresses \>1%.

7. If criteria met: submit for human approval.

8. If human approves: merge the improvement into design tokens. **\[DERIVED\]**

9. Update W3C DTCG 2025.10 compliant design token files (8 JSON files). **\[DERIVED\]**

| Inputs | Any React UI component or screen. |
| :---- | :---- |
| **Outputs** | Composite visual quality score; improvement recommendations; continuously improving design system. |
| **Tools / Skills** | UIClip, LLM rubric, Design token JSON files (8 files), Style Dictionary, Stylelint, Playwright |

## **23\. File Naming Convention Application**

| Purpose | Apply standardised file naming conventions across all vault and repository files to enable systematic retrieval and cross-referencing. |
| :---- | :---- |
| **Trigger** | Any new vault or repository file creation. |
| **Owner** | TBD (All contributors) |
| **Frequency** | On every new file creation. |

**Steps**

1. Determine file type: standard document, research document, constitutional document, session summary, or research file.

2. For standard documents: apply format YYYY-MM-DD-descriptive-name.md. **\[DERIVED\]**

3. For research documents: apply format YYYY-MM-DD-TOPIC-keyword-keyword.md (UPPERCASE topic for scannability).

4. For constitutional documents: apply format DOCUMENT-NAME-v\[N\].md.

5. For session summaries: save to vault/00-handover/sessions/YYYY-MM-DD-session-summary.md.

6. For research: save to vault/18-research/YYYY-MM-DD-topic-name.md.

7. Verify name enables systematic retrieval and cross-referencing. **\[DERIVED\]**

| Inputs | Any new vault or repository file. |
| :---- | :---- |
| **Outputs** | Consistently named, retrievable, scannably organised file. |
| **Tools / Skills** | FILE-NAMING-CONVENTION-v1, Vault structure |

## **24\. Self-Reflection Protocol Execution**

| Purpose | Enable AI agents to self-assess their outputs and behaviour, measuring partnership quality and storing episodic memory for continuous improvement. |
| :---- | :---- |
| **Trigger** | Completion or failure of any agent task. |
| **Owner** | TBD (Every AI agent) |
| **Frequency** | On every agent task completion or failure. |

**Steps**

1. Actor completes a task (or task fails).

2. Evaluator scores the output against defined rubrics. **\[DERIVED\]**

3. Agent runs self-reflection: generate verbal feedback on own performance.

4. Assess partnership score: did the agent behave as a peer/partner, not just a tool?

5. Store self-reflection in vault as episodic memory buffer.

6. Produce post-mortem and save to vault.

7. Ensure next session's agent loads the post-mortem before starting. **\[DERIVED\]**

| Inputs | Any completed or failed agent session. |
| :---- | :---- |
| **Outputs** | Self-critical post-mortem; partnership score; vault document for next session's context. |
| **Tools / Skills** | Self-Reflection Protocol (Skill 10e89a4b, 1,078 lines), Vault, KaizenWorkflow |

## **25\. RIC — Rapid Intelligence Cycle Execution**

| Purpose | Match research depth to decision urgency and stakes using 4 velocity tiers, preventing over-researching while ensuring adequate analysis. |
| :---- | :---- |
| **Trigger** | Research task with defined urgency and stakes. |
| **Owner** | TBD (Research / Intelligence team) |
| **Frequency** | On every research task. |

**Steps**

1. Classify the decision: urgency level and stakes level. **\[DERIVED\]**

2. Select velocity tier: Tier 1 (fastest, time-sensitive), Tier 2 (standard, routine), Tier 3 (deep, strategic), or Tier 4 (exhaustive, constitutional).

3. Apply tier parameters: scope, depth, time/token budget, minimum sources, output format. **\[DERIVED\]**

4. Phase 1 — Discover: broad ecosystem scanning at the selected tier's depth.

5. Phase 2 — Analyse: deep synthesis and connection mapping.

6. Produce intelligence output at appropriate depth for the decision. **\[DERIVED\]**

7. Document sources and confidence levels. **\[DERIVED\]**

| Inputs | Research task with urgency and stakes classification. |
| :---- | :---- |
| **Outputs** | Intelligence output at appropriate depth for the decision being made. |
| **Tools / Skills** | RIC velocity tier framework, SearXNG-First Search Policy, PUDDING Technique, Vault Research Ingestion Format |

## **26\. Markdown-as-Constitution Governance**

| Purpose | Ensure human-readable constitutional Markdown documents have ultimate authority over all technical implementation. |
| :---- | :---- |
| **Trigger** | New governance rule creation; proposed change to constitutional document; agent deployment. |
| **Owner** | TBD (Governance Lead — Ewan Bramley) |
| **Frequency** | On governance rule changes; continuous enforcement. |

**Steps**

1. Write the constitutional rule in plain English in a Markdown file (e.g., SOUL.md, Eight Laws).

2. Inject the Markdown document as Layer 0 of every agent prompt via prompt\_loader.py.

3. Mark constitutional documents as read-only in production — no agent may modify them.

4. For any proposed change: require human review. **\[DERIVED\]**

5. Require multi-agent council sign-off for constitutional changes. **\[DERIVED\]**

6. Verify that technical implementation complies with and does not weaken constitutional constraints. **\[DERIVED\]**

7. Audit agent outputs periodically for constitutional compliance. **\[DERIVED\]**

| Inputs | Governance decisions; ethical constraints; architectural principles. |
| :---- | :---- |
| **Outputs** | Human-readable governance that is technically enforced across all agents. |
| **Tools / Skills** | SOUL.md, Eight Laws, prompt\_loader.py, 4-Layer Prompt Architecture, Multi-agent council |


---
title: "Dept 2 Value Creation Processes"
id: "dept-2-value-creation-processes"
version: 1
created: 2026-04-25
last_validated: 2026-04-25
type: document
topic_type: reference
status: imported
source_file: "dept-2-value-creation-processes.docx.md"
signed_by: "Devon, 2026-04-25, devin-992682c244cf444f91e0a516498afbfd"
---

  
**Value Creation & Client Delivery**

**Process Handbook**

Department 2 — Amplified Partners

*Actionable processes for diagnostics, rubrics, coaching, knowledge management, and research*

March 2026  
**CONFIDENTIAL**

# **Table of Contents**

# **Introduction**

This handbook documents every actionable process within the Value Creation & Client Delivery department. Each process is presented in a standardised format covering: name, purpose, trigger, numbered steps, inputs, outputs, owner, tools/skills required, and frequency.

Steps marked \[DERIVED\] have been inferred from the methodology descriptions and related context where the source material describes a methodology but does not explicitly list that step as a discrete process action. All other steps are directly extracted from the source documentation.

Owners marked \[TBD\] indicate that the source material does not specify a responsible agent or role for that process. These should be assigned during implementation.

# **Section 1: Client Onboarding Processes**

These processes govern how new clients are routed, baselined, and configured for Amplified's advisory services.

| Client Onboarding & Track Routing |  |
| :---- | :---- |
| **Purpose** | Route new clients to the correct onboarding pathway (Track 1 or Track 2\) based on business maturity. |
| **Trigger** | New client engagement contract signed. |
| **Steps** | 1\. Determine client business age at onboarding. 2\. If \<90 days old → assign Track 1 (New Business). \[DERIVED\] 3\. If \>90 days old → assign Track 2 (Existing Business). \[DERIVED\] 4\. Track 1: Configure Financial Autopsy in projection mode; focus on legal setup, banking, early systems, first customer. \[DERIVED\] 5\. Track 2: Configure Financial Autopsy in historical mode with full 5-year data pull; activate all 7 Operational Rubriks; schedule Shadow Month. 6\. Assign to correct pricing tier based on business size and complexity. 7\. Initiate WhatsApp channel for client communication. \[DERIVED\] 8\. Record routing decision in client Business Brain (FalkorDB). \[DERIVED\] |
| **Inputs** | Signed engagement contract; client business age; business size and complexity data. |
| **Outputs** | Correctly routed client on Track 1 or Track 2; configured product set; active WhatsApp channel. |
| **Owner** | Onboarding Agent \[TBD\] |
| **Tools / Skills Required** | FalkorDB \+ Graphiti, WhatsApp API, Xero/Sage/QuickBooks API, The Pulse |
| **Frequency** | Per new client engagement. |

| Shadow Month Execution |  |
| :---- | :---- |
| **Purpose** | Establish a validated baseline of client business operations before any automation or intervention. |
| **Trigger** | Track 2 client onboarding begins (existing business \>90 days old). |
| **Steps** | 1\. Connect to client accounting software (Xero/Sage/QuickBooks) via API. 2\. Configure passive monitoring — system observes patterns, collects data, identifies friction points. 3\. Ensure zero AI interventions or automation deployed during the 30-day observation period. 4\. Run initial Financial Autopsy (Altman Z-Score \+ Goldratt ToC \+ CCC). \[DERIVED\] 5\. Map client operations against 16-Point Friction Taxonomy. \[DERIVED\] 6\. Generate AMPS scores per identified process. \[DERIVED\] 7\. Compile baseline report: AMPS scores, friction inventory, Financial Autopsy results. 8\. Present baseline report to client at end of Month 1\. 9\. Client reviews and approves the improvement roadmap before any automation begins. |
| **Inputs** | Client system access credentials; 30 days of operational observation data. |
| **Outputs** | Validated baseline report; approved improvement roadmap; client trust established. |
| **Owner** | Shadow Month Agent \[TBD\] |
| **Tools / Skills Required** | Xero/Sage/QuickBooks API, AMPS scoring engine, 16-Point Friction Taxonomy, Financial Autopsy pipeline |
| **Frequency** | Once per Track 2 client engagement (Month 1). |

| Life Goals Capture |  |
| :---- | :---- |
| **Purpose** | Capture the business owner's personal goals and map them to business decisions for goal-aligned advisory. |
| **Trigger** | Client onboarding (initial) or scheduled periodic review. |
| **Steps** | 1\. Conduct structured interview with business owner (weekly or at onboarding). 2\. Capture personal goals across five dimensions: family, financial, time, health, legacy. \[DERIVED\] 3\. For each goal, ask: 'What business outcome would make this personal goal achievable?' \[DERIVED\] 4\. Map each personal goal to specific business decisions and metrics. 5\. Store goal profile in Graphiti with temporal tags (so system tracks goal evolution over time). 6\. Configure all subsequent AI recommendations to reference these goals. 7\. Update: 'This action moves you toward / away from \[personal goal\]' in all outputs. \[DERIVED\] |
| **Inputs** | Business owner's time; structured interview questions. |
| **Outputs** | Personal goal profile stored in Graphiti; goal-aligned recommendation configuration. |
| **Owner** | Advisory Agent \[TBD\] |
| **Tools / Skills Required** | Graphiti (temporal knowledge graph), The Pulse, WhatsApp |
| **Frequency** | At onboarding (initial), then weekly or periodic reviews. |

# **Section 2: Diagnostic Processes**

These processes perform the analytical assessments that power Amplified's client advisory — from financial health checks to continuous rubrik scoring.

| Financial Autopsy Execution |  |
| :---- | :---- |
| **Purpose** | Deliver a plain-language financial health assessment to a client using three deterministic rubrics. |
| **Trigger** | Client connects accounting software (free tier viral hook or paid engagement). |
| **Steps** | 1\. Client connects accounting software (Xero/Sage/QuickBooks) via API. 2\. Pull 5 years of financial data (Track 2\) or configure projection mode (Track 1). \[DERIVED\] 3\. Run Altman Z-Score: calculate Z \= 1.2(X1) \+ 1.4(X2) \+ 3.3(X3) \+ 0.6(X4) \+ 1.0(X5). Classify: Z\<1.81=distress, 1.81-2.99=grey, Z\>2.99=safe. 4\. Run Goldratt Theory of Constraints: identify the \#1 constraint limiting growth using Five Focusing Steps. 5\. Run Cash Conversion Cycle: calculate CCC \= DIO \+ DSO \- DPO. 6\. Generate plain-language report — business owner reads without needing accounting knowledge. 7\. Deliver report via WhatsApp or The Pulse interface. 8\. Embed upgrade calls to action for paid tier. \[DERIVED\] 9\. Store results in client Business Brain (FalkorDB). \[DERIVED\] |
| **Inputs** | Client accounting system API credentials; 5 years of financial data (or projection inputs for Track 1). |
| **Outputs** | Plain-language financial health report with 3-rubric assessment; upgrade pathway; stored results. |
| **Owner** | Financial Autopsy Agent \[TBD\] |
| **Tools / Skills Required** | Xero/Sage/QuickBooks API, Altman Z-Score calculator, Goldratt ToC engine, CCC calculator, WhatsApp API, The Pulse, FalkorDB |
| **Frequency** | At onboarding (initial); then continuous monitoring for paid tiers. |

| 16-Point Friction Assessment |  |
| :---- | :---- |
| **Purpose** | Map and prioritise all operational friction points in a client's business to build an automation roadmap. |
| **Trigger** | Shadow Month begins or client interview conducted. |
| **Steps** | 1\. Map client's operations against all 16 universal friction point categories. 2\. Score severity for each friction point: impact × frequency. \[DERIVED\] 3\. Estimate time cost per friction point (hours/week). \[DERIVED\] 4\. Calculate ROI of elimination: time saved × value of freed time. \[DERIVED\] 5\. Prioritise friction points by ROI (highest-ROI first). 6\. Build automation roadmap targeting highest-ROI friction points first. 7\. Present prioritised friction inventory and roadmap to client for approval. \[DERIVED\] 8\. Store friction inventory in client Business Brain. \[DERIVED\] |
| **Inputs** | Client operational observation data (Shadow Month or interview); 16-Point Friction Taxonomy reference. |
| **Outputs** | Prioritised friction inventory; automation roadmap with ROI estimates. |
| **Owner** | Defriction Agent \[TBD\] |
| **Tools / Skills Required** | 16-Point Friction Taxonomy, AMPS scoring engine, FalkorDB \+ Graphiti |
| **Frequency** | At Shadow Month (initial); then quarterly review. \[DERIVED\] |

| Death Spiral Detection |  |
| :---- | :---- |
| **Purpose** | Monitor for 6 early warning patterns indicating catastrophic business failure risk and trigger early intervention. |
| **Trigger** | Continuous monitoring — threshold breach on any of 6 early warning pattern categories. |
| **Steps** | 1\. Connect to client financial data stream (Xero/Sage/QuickBooks). 2\. Continuously monitor 6 early warning pattern categories (financial, operational, market signals). 3\. Apply Altman Z-Score: flag if Z \< 1.81 (distress zone). 4\. Apply Cash Conversion Cycle: flag deteriorating liquidity. \[DERIVED\] 5\. Apply Goldratt ToC: identify the \#1 constraint. 6\. Score via DEATH-SPIRAL-DETECTOR rubrik. 7\. If threshold crossed: alert client immediately. 8\. Surface alert via The Pulse morning briefing. \[DERIVED\] 9\. Trigger DANGER-SPIRAL-EXIT rubrik for recovery pathway. \[DERIVED\] 10\. Log detection event and response in client Business Brain. \[DERIVED\] |
| **Inputs** | Live client financial and operational data; 6 early warning pattern definitions. |
| **Outputs** | Early warning score; client alert with 6-month advance notice target; recovery pathway activation. |
| **Owner** | Death Spiral Detection Agent \[TBD\] |
| **Tools / Skills Required** | Xero/Sage/QuickBooks API, Altman Z-Score, CCC, Goldratt ToC, DEATH-SPIRAL-DETECTOR rubrik, DANGER-SPIRAL-EXIT rubrik, The Pulse |
| **Frequency** | Continuous (always-on monitoring). |

| 7 Operational Rubriks Scoring |  |
| :---- | :---- |
| **Purpose** | Continuously score client business health across 7 dimensions and surface alerts for threshold breaches. |
| **Trigger** | Continuous — live data stream from client systems. \[DERIVED\] |
| **Steps** | 1\. Ingest live client data from accounting software, operations data, and staff data. 2\. Score WOW-ZIGLAR-LUND (customer experience and delight). \[DERIVED\] 3\. Score CASH-IS-OXYGEN (liquidity and cash flow using Altman Z-Score, CCC, Quick Ratio). \[DERIVED\] 4\. Score DEATH-SPIRAL-DETECTOR (existential risk early warning). \[DERIVED\] 5\. Score GROWTH-ENGINE (business expansion and growth rate). \[DERIVED\] 6\. Score PEOPLE-PULSE (team health and engagement). \[DERIVED\] 7\. Score COMPLIANCE-SHIELD (regulatory and legal compliance). \[DERIVED\] 8\. Score DANGER-SPIRAL-EXIT (recovery pathway status, if activated). \[DERIVED\] 9\. Generate threshold breach alerts for any rubrik crossing warning level. \[DERIVED\] 10\. Surface scores and recommendations via The Pulse morning briefing. \[DERIVED\] |
| **Inputs** | Live client business data from Xero/Sage/QuickBooks, operations systems, staff systems. |
| **Outputs** | Continuous health scores across 7 dimensions; threshold breach alerts; actionable recommendations. |
| **Owner** | Rubrik Scoring Engine \[TBD\] |
| **Tools / Skills Required** | Xero/Sage/QuickBooks API, Deterministic Rubrics (Business Physics Suite), The Pulse, FalkorDB |
| **Frequency** | Continuous (always-on scoring). |

# **Section 3: Ongoing Advisory Processes**

These processes govern the continuous delivery of advisory services to active clients, from trust calibration through decision support and friction reduction.

| 4-Month Supervised-to-Autonomous Handoff |  |
| :---- | :---- |
| **Purpose** | Transition a client from supervised AI operation to calibrated autonomous operation over 4 months. |
| **Trigger** | New client engagement begins AI adoption (post-onboarding). |
| **Steps** | 1\. Month 1 (Shadow Month): System observes only — no changes, baseline established. 2\. Month 2: Begin supervised operation — all AI actions shown to human for approval before execution (Autonomous Vehicle Trust Architecture). 3\. Month 3: Continue supervised operation — accumulate track record via Baseball Cards (90-Day Rolling Gates). 4\. Month 4: Review believability scores per action category. \[DERIVED\] 5\. For categories with ≥95% believability: transition to autonomous operation. \[DERIVED\] 6\. For categories with \<95% believability: maintain human oversight. \[DERIVED\] 7\. Document transition decisions in client Business Brain. \[DERIVED\] |
| **Inputs** | New client engagement; system access; 4 months of operational data. |
| **Outputs** | Client with calibrated AI trust; AI with validated track record; appropriate autonomy levels per task category. |
| **Owner** | Trust Calibration Agent \[TBD\] |
| **Tools / Skills Required** | Autonomous Vehicle Trust Architecture, Baseball Cards, Confidence Gating, FalkorDB \+ Graphiti |
| **Frequency** | Once per client engagement (Months 1–4); ongoing trust recalibration thereafter. \[DERIVED\] |

| Confidence Gating & Escalation |  |
| :---- | :---- |
| **Purpose** | Route every AI agent decision through the appropriate autonomy level based on confidence score. |
| **Trigger** | Any AI agent proposes an action or decision. |
| **Steps** | 1\. Agent assesses confidence in proposed action (0–100%). 2\. If ≥95%: auto-handle — execute autonomously. 3\. If 85–94%: flag for review — surface to human client for approval. 4\. If 70–84%: route to Agent Council vote — majority of AI board must agree. 5\. If \<70%: escalate to human — human must decide. 6\. Execute the approved action (or cancel if rejected). 7\. Log outcome (success / partial / failure) in Baseball Cards. \[DERIVED\] 8\. Update believability score for this agent/task-type combination. \[DERIVED\] |
| **Inputs** | Any agent decision or proposed action; current believability scores. |
| **Outputs** | Routed action (autonomous / flagged / council / human); updated track record. |
| **Owner** | Confidence Gating System (automated) / Human Escalation Point \[TBD\] |
| **Tools / Skills Required** | Confidence Gating engine, Baseball Cards, AI Board Governance Architecture |
| **Frequency** | Every agent action (continuous). |

| Decision Sovereignty Delivery |  |
| :---- | :---- |
| **Purpose** | Ensure every client business decision follows the 'Their Data → Our Rubric → Options → They Decide' framework. |
| **Trigger** | Business decision requiring input from Amplified. |
| **Steps** | 1\. Source all analysis from client's own data — never third-party assessments of the client. 2\. Run deterministic rubrics (not human opinion) to generate options. 3\. Present multiple options (never a single forced recommendation). \[DERIVED\] 4\. For each option, annotate alignment with Life Goals. \[DERIVED\] 5\. Client makes the final decision from the presented options. 6\. No AI agent executes a significant business decision without explicit client authorisation. 7\. Record decision and rationale in client Business Brain. \[DERIVED\] |
| **Inputs** | Client business data; rubrik outputs; Life Goals profile. |
| **Outputs** | Client-controlled decision with AI-generated options; decision audit trail. |
| **Owner** | Advisory Agent \[TBD\] |
| **Tools / Skills Required** | Deterministic Rubrics, Life Goals profile (Graphiti), FalkorDB, The Pulse |
| **Frequency** | Every significant business decision (event-driven). |

| Defriction Sequence Execution |  |
| :---- | :---- |
| **Purpose** | Execute the 6-step chain from friction identification through to owner life goal achievement. |
| **Trigger** | Friction inventory approved by client (post-Shadow Month or periodic review). \[DERIVED\] |
| **Steps** | 1\. Identify friction — confirm 16-Point Friction Taxonomy mapping is current. 2\. Automate friction — deploy AI agents to eliminate or reduce each prioritised friction point. 3\. Quantify time freed — measure hours/week recovered (target: 57 hours/week / 1.4 FTE). \[DERIVED\] 4\. Redirect staff to content creation — configure freed time for higher-value human roles. \[DERIVED\] 5\. Enable owner strategic work — monitor shift from technician to entrepreneur (E-Myth). \[DERIVED\] 6\. Track life goal progress — reference Life Goals Meeting data in all progress reports. \[DERIVED\] 7\. Report progress against baseline at regular intervals. \[DERIVED\] |
| **Inputs** | Approved friction inventory and automation roadmap; Life Goals profile. |
| **Outputs** | Friction-reduced operation; staff in higher-value roles; owner with time for strategic work; life goal progress. |
| **Owner** | Defriction Agent \[TBD\] |
| **Tools / Skills Required** | 16-Point Friction Taxonomy, AI agent deployment, Life Goals profile (Graphiti), The Pulse, AMPS scoring |
| **Frequency** | Ongoing (post-Shadow Month); quarterly review of progress. \[DERIVED\] |

| WhatsApp Forensic Advisory Delivery |  |
| :---- | :---- |
| **Purpose** | Deliver strategic advisory insights to clients via WhatsApp using forensic analysis of their business data. |
| **Trigger** | Client sends business data or question via WhatsApp; or scheduled advisory delivery. \[DERIVED\] |
| **Steps** | 1\. Receive client business data or query via WhatsApp. 2\. AI agents perform forensic analysis of submitted data. 3\. Generate insights in plain language (no jargon). \[DERIVED\] 4\. Deliver insights back via WhatsApp. 5\. Handle follow-up questions via WhatsApp conversation. 6\. If richer dashboards needed: escalate to The Pulse web/mobile interface. 7\. Log all interactions in client Business Brain. \[DERIVED\] |
| **Inputs** | Client WhatsApp messages; business data files. |
| **Outputs** | Forensic analysis delivered in plain language via WhatsApp; escalation to The Pulse if needed. |
| **Owner** | WhatsApp Advisory Agent \[TBD\] |
| **Tools / Skills Required** | WhatsApp API, AI forensic analysis agents, The Pulse, FalkorDB |
| **Frequency** | On-demand (client-initiated) and scheduled deliveries. \[DERIVED\] |

# **Section 4: Knowledge Management Processes**

These processes govern how knowledge enters, is structured within, and is retrieved from Amplified's vault and knowledge hierarchy.

| Baton Pass Protocol (Session Handover) |  |
| :---- | :---- |
| **Purpose** | Ensure continuous context and knowledge preservation across all AI working sessions, eliminating cold starts. |
| **Trigger** | Start of any AI agent session; end of any AI agent session. |
| **Steps** | 1\. SESSION START — Read BATON-PASS-PROTOCOL.md. 2\. Read SESSION-STATE.md for current state. 3\. Read RESEARCH-INDEX.md before ANY web search ('Every search costs money'). 4\. Read IDENTITY.md for voice and values. 5\. Read MEMORY.md for company facts. 6\. DURING SESSION — Save every output to vault in appropriate directory (Research → vault/18-research/, Architecture → vault/02-technical-architecture/, etc.). 7\. SESSION END — Update SESSION-STATE.md with what was done and what's next. 8\. Add any new research to RESEARCH-INDEX.md. 9\. Log work to Linear (project: Amplified Partners, team: Amplified Partners). |
| **Inputs** | Session start / session end; previous session state. |
| **Outputs** | Session with complete context; knowledge preserved in vault; updated session state. |
| **Owner** | Every AI Agent (mandatory protocol) |
| **Tools / Skills Required** | Vault filesystem, SESSION-STATE.md, RESEARCH-INDEX.md, IDENTITY.md, MEMORY.md, Linear |
| **Frequency** | Every AI session (start and end). |

| Vault Knowledge Ingestion (Gatekeeper Process) |  |
| :---- | :---- |
| **Purpose** | Ensure all content entering the vault meets quality thresholds, is properly labelled, and deduplicated. |
| **Trigger** | New content submitted for vault ingestion. |
| **Steps** | 1\. Receive candidate content for vault ingestion. 2\. Run quality assessment: does content meet minimum AMPS threshold? 3\. Check for duplication using three-layer deduplication (exact → near-duplicate → semantic). 4\. If duplicate: reject or merge with existing entry. \[DERIVED\] 5\. Assign PUDDING label (WHAT.HOW.SCALE.TIME) and semantic dimensions. 6\. Assign APQC category code for atom ID. 7\. Write to FalkorDB (graph layer) with Graphiti temporal tags. 8\. Write raw content to filesystem (Layer 2 of vault research ingestion format). 9\. Update knowledge graph schema if new entity type detected. |
| **Inputs** | Candidate vault content; quality threshold configuration; PUDDING taxonomy reference. |
| **Outputs** | PUDDING-labelled, deduplicated, schema-compliant vault entries. |
| **Owner** | Gatekeeper Agent (deployed) |
| **Tools / Skills Required** | Gatekeeper Agent (12-file Python system), FalkorDB \+ Graphiti, Three-Layer Deduplication, PUDDING 2026 labels, APQC PCF |
| **Frequency** | Every vault ingestion event (continuous). |

| Vault Research Ingestion |  |
| :---- | :---- |
| **Purpose** | Format and store new research in the two-layer vault format with full PUDDING labelling and citations. |
| **Trigger** | New research identified via RIC (Research Intelligence Cycle) or APDS. |
| **Steps** | 1\. Create Layer 1 YAML record (300–500 words): structured fields, citation URLs, PUDDING label, semantic dimensions. 2\. Assign ID format: RES-YYYY-MM-DD-NNN. 3\. Store Layer 1 in FalkorDB with Graphiti temporal tags. 4\. If raw source data is valuable: store in filesystem as Layer 2 (path referenced in Layer 1). 5\. Apply rule: 'Links replace bulk — if it's on the internet, store the insight and citation, not the full content.' 6\. Extract named techniques as atomic units for PUDDING mixing. \[DERIVED\] 7\. Capture failure patterns alongside success patterns (Swanson dual search principle). |
| **Inputs** | Research outputs, web search results, academic papers, expert frameworks. |
| **Outputs** | Structured, PUDDING-labelled, citation-backed vault entries ready for agent retrieval. |
| **Owner** | Research Agent \[TBD\] / Gatekeeper Agent |
| **Tools / Skills Required** | Vault Research Ingestion Format v1.0, FalkorDB \+ Graphiti, PUDDING 2026 labels, Gatekeeper Agent |
| **Frequency** | Every research ingestion event (continuous). |

| Vault Knowledge Hierarchy Routing |  |
| :---- | :---- |
| **Purpose** | Route every new piece of knowledge to the correct level in the 5-level knowledge hierarchy. |
| **Trigger** | Any new knowledge, decision, or artefact produced during Amplified work. \[DERIVED\] |
| **Steps** | 1\. Assess the nature and permanence of the knowledge artifact. 2\. If permanent, structured, searchable knowledge → Vault (library). \[DERIVED\] 3\. If current operating rules or architectural decisions → CLAUDE.md (operating manual). \[DERIVED\] 4\. If ephemeral cross-session notes → Auto memory (notebook). \[DERIVED\] 5\. If active task or project tracking → Linear (to-do board). \[DERIVED\] 6\. If committed code or artefact → GitHub (truth/artefact). 'If it's not in GitHub, it's not real.' \[DERIVED\] 7\. Ensure vault content is also routed to correct domain in FalkorDB 5-domain schema: Business Strategy, Technical Architecture, Operations, Research, Knowledge. \[DERIVED\] |
| **Inputs** | Any new knowledge, decision, or artefact. |
| **Outputs** | Correctly filed, retrievable knowledge at the appropriate hierarchy level. |
| **Owner** | Every AI Agent (mandatory protocol) / Gatekeeper Agent for vault entries |
| **Tools / Skills Required** | Vault filesystem, CLAUDE.md, Linear, GitHub, FalkorDB (5-domain schema) |
| **Frequency** | Every knowledge-producing event (continuous). |

# **Section 5: Research & Discovery Processes**

These processes handle document discovery, extraction, convergence, and the full Vault Extraction Pipeline.

| Document Discovery & Extraction Pipeline (HoundDog → DocBench) |  |
| :---- | :---- |
| **Purpose** | Find, deduplicate, classify, and extract all documents from all systems into structured formats. |
| **Trigger** | Vault extraction cycle initiated; new document corpus identified. \[DERIVED\] |
| **Steps** | 1\. HOUNDDOG: Scan all configured directories on Beast and Mac for documents (all file types). 2\. Copy every discovered document to working corpus folder — originals untouched. 3\. Classify each document by type (PDF, DOCX, email, image, etc.). 4\. Apply three-layer deduplication: exact duplicate → near-duplicate (semantic) → content-level (same info, different words). 5\. Output: deduplicated corpus ready for DocBench. 6\. DOCBENCH: Run extraction via Llama 3.1 8B (P\_refined\_v3 strategy). 7\. Extract 100% of data without judging or canonicalising beyond consistent output shape. 8\. Output four formats per document: Raw text, Structured JSON (doc\_{sha256\_first8}.json), Process/logic, Principles/values. 9\. Run 100% JSON validity check on output. 10\. Pass extracted content to PUDDING Labelling stage. \[DERIVED\] |
| **Inputs** | File system directories on Beast/Mac; document files of any type. |
| **Outputs** | Deduplicated, classified, 4-format extracted corpus with stable JSON IDs. |
| **Owner** | HoundDog Agent / DocBench Agent (automated) |
| **Tools / Skills Required** | HoundDog, DocBench, Llama 3.1 8B (Ollama on Beast), Three-Layer Deduplication |
| **Frequency** | Per vault extraction cycle; on-demand for new corpus discovery. |

| Research Convergence |  |
| :---- | :---- |
| **Purpose** | Synthesise multiple parallel research streams into a unified, deduplicated, coherent master document. |
| **Trigger** | Multiple research streams identified on the same topic (e.g., 8 parallel AI research sessions). \[DERIVED\] |
| **Steps** | 1\. Identify all parallel research streams on the same topic. 2\. Run HoundDog to find all relevant documents across the corpus. 3\. Apply DocBench to extract and structure each stream. 4\. Run three-layer deduplication to remove redundant content. 5\. Synthesise all streams into a single master document using the Wall Method. 6\. Apply PUDDING labels to identify structural rhymes across streams. 7\. Identify and fill coverage gaps. \[DERIVED\] 8\. Produce the converged, deduplicated, coherent output. |
| **Inputs** | Multiple parallel research streams or conversation threads on the same topic. |
| **Outputs** | Single converged master document; no lost information; no redundant information. |
| **Owner** | Research Convergence Agent \[TBD\] |
| **Tools / Skills Required** | HoundDog, DocBench, Three-Layer Deduplication, Wall Method, PUDDING 2026 labels |
| **Frequency** | When multiple research streams on same topic are identified (event-driven). |

| Vault Extraction Pipeline (Full 8-Stream) |  |
| :---- | :---- |
| **Purpose** | Transform raw vault knowledge and Perplexity conversations into 8 parallel output streams for different audiences. |
| **Trigger** | Vault extraction cycle initiated. \[DERIVED\] |
| **Steps** | 1\. Convergence: gather all relevant sources. 2\. HoundDog: discover, copy, classify, and deduplicate documents. 3\. DocBench: extract 100% of data in four formats. 4\. PUDDING Labelling: apply WHAT.HOW.SCALE.TIME labels to all extracted content. 5\. Route to 8 Output Streams: \[DERIVED\]    a. Content Creation (narrative, marketing angles, audience-specific)    b. Process & Logic Giveaway (behavioural psychology templates)    c. Ewan's Book    d. Complete Comprehensive Document    e. The Manifesto    f. Onboarding    g. TAXONOMY ENGINE (commercial product)    h. Amplified Quality System / Micro-Help Library (commercial product) 6\. Quality-check each stream output. \[DERIVED\] |
| **Inputs** | Vault documents; Perplexity conversation exports (forked perplexity-ai-export v1.1.0 on Beast). |
| **Outputs** | 8 parallel output streams from the same underlying knowledge corpus. |
| **Owner** | Vault Extraction Pipeline (automated) \[TBD\] |
| **Tools / Skills Required** | HoundDog, DocBench, PUDDING Technique, Three-Layer Deduplication, perplexity-ai-export v1.1.0 |
| **Frequency** | Per extraction cycle (periodic). \[DERIVED\] |

| Wall Method Document Assembly |  |
| :---- | :---- |
| **Purpose** | Assemble mega-documents from multiple sessions using bottom-up, PUDDING-label-driven structure. |
| **Trigger** | Need to combine multiple session documents into a single coherent document. \[DERIVED\] |
| **Steps** | 1\. Label every source document with PUDDING codes. 2\. Flatten all documents onto a conceptual 'wall' — remove document boundaries entirely. 3\. Find structural rhymes between matching PUDDING labels from different sessions. 4\. Identify coverage gaps (which WHAT.HOW.SCALE.TIME regions have no coverage?). 5\. Deduplicate similar content identified by label overlap. 6\. Let the mega-document structure emerge from label clusters (not top-down outline). \[DERIVED\] 7\. Verify final document reflects actual knowledge structure, not session structure. \[DERIVED\] |
| **Inputs** | Multiple session documents with PUDDING labels; stated coverage goal. |
| **Outputs** | Coverage-complete mega-document with emergent structure; gap analysis. |
| **Owner** | Research Agent \[TBD\] |
| **Tools / Skills Required** | PUDDING 2026 labels, PUDDING Technique |
| **Frequency** | When assembling mega-documents from multiple sessions (event-driven). |

# **Section 6: PUDDING Discovery Processes**

These processes cover all aspects of PUDDING discovery — from manual sessions to automated pipeline execution, labelling, and the kill switch evaluation.

| PUDDING Discovery Session (Full 8-Step Process) |  |
| :---- | :---- |
| **Purpose** | Find non-obvious, high-value cross-domain connections using the PUDDING technique. |
| **Trigger** | Discovery goal defined; Lens Card completed. |
| **Steps** | 1\. PRE-SESSION: Complete Lens Card — goal statement, domains, success criteria, scope, compute budget, confidence threshold. 2\. Gather source material: vault files, research outputs, expert frameworks, or new research. 3\. Determine if vault-based (existing knowledge) or research-based (new inputs needed). 4\. STEP 1 — Research: Run triple search (success \+ failure patterns). Collect named techniques (4–7 per domain). 5\. STEP 2 — Neutral Labelling: Strip domain names. Assign neutral mechanism labels with semantic dimensions. Flatten into one list — do NOT group by expert or domain. 6\. STEP 3 — PUDDING 2026 Label: Apply WHAT.HOW.SCALE.TIME to every concept. 7\. STEP 4 — Pattern Match: Find shared dimensions and matching labels across domains. Identical labels from different domains \= highest-value signals. 8\. STEP 5 — ABC Connection: For each bridge, construct A→B→C chain. State hypothesis. Test: Is A→C connection non-obvious? 9\. STEP 6 — Score: Simple formula (Shared Dimensions × 2 \+ Unique\_A \+ Unique\_B). Advanced: (Domain Distance × Pattern Alignment) \+ Gap Complement \+ Tension Bonus. Min viable ≥5; high-value ≥8; ≥13 build; ≥18 build immediately. 10\. STEP 7 — 1+1=3 Insight: Name the emergent understanding. If you can't name it, you haven't made pudding. 11\. STEP 8 — Validate: Mark as hypothesis, tested\_internal, tested\_client, or proven. Include testable prediction. |
| **Inputs** | Completed Lens Card; research from 2+ unrelated domains; vault files or expert frameworks. |
| **Outputs** | Named A→C connections (pudding recipes) with scores, hypotheses, and testable predictions. |
| **Owner** | Ewan (human lead) \+ Sam (research agent) \+ Challenger AI |
| **Tools / Skills Required** | PUDDING Technique, PUDDING 2026 Label Notation, triple search engines, vault, FalkorDB |
| **Frequency** | On-demand (event-driven by discovery goals). |

| PUDDING Session — Post-Session Protocol |  |
| :---- | :---- |
| **Purpose** | Document, vault, and action all outputs from a completed PUDDING discovery session. |
| **Trigger** | PUDDING discovery session completed. |
| **Steps** | 1\. Document everything with full Radical Attribution (credit every source explicitly). 2\. Add proper YAML frontmatter to vault output document. 3\. Mark all recipes with validation status (hypothesis / tested\_internal / tested\_client / proven). 4\. Create actionable next steps for testing hypotheses. \[DERIVED\] 5\. If commitments emerged, log them to Cato (accountability agent) for follow-up. 6\. Vault the output document in vault/18-research/ with standard naming. \[DERIVED\] 7\. Update RESEARCH-INDEX.md with new entries. \[DERIVED\] |
| **Inputs** | Completed PUDDING session outputs; recipes, scores, hypotheses. |
| **Outputs** | Vaulted, attributed, validation-tagged recipe document; actionable next steps; commitment log. |
| **Owner** | Sam (vault agent) \+ Cato (accountability agent) |
| **Tools / Skills Required** | Vault filesystem, Radical Attribution Schema, YAML Frontmatter Standard, Linear (for commitments) |
| **Frequency** | After every PUDDING discovery session. |

| PUDDING Kill Switch Evaluation |  |
| :---- | :---- |
| **Purpose** | Determine whether a PUDDING session should proceed or be terminated to save resources. |
| **Trigger** | 50 pairs scored in initial PUDDING evaluation. \[DERIVED\] |
| **Steps** | 1\. Score the first 50 candidate pairs using the Anchored Rubric. 2\. Check for 3+ connections scoring ≥18. 3\. If 3+ connections at ≥18 → GREEN LIGHT: proceed to full session. 4\. If no connection scores ≥13 → KILL IT: stop session, redirect resources. 5\. If between thresholds → review Lens Card scope; consider narrowing or pivoting. \[DERIVED\] 6\. Document kill decision and reason. \[DERIVED\] |
| **Inputs** | 50 scored candidate pairs; Anchored Rubric; Lens Card. |
| **Outputs** | Go/no-go decision; if killed, documented reason and resource redirect. |
| **Owner** | Ewan (human lead) / APDS (automated) |
| **Tools / Skills Required** | PUDDING Anchored Rubric, Lens Card, Kill Switch gate system |
| **Frequency** | Every PUDDING session (early gate check). |

| APDS Automated Discovery Pipeline |  |
| :---- | :---- |
| **Purpose** | Run the PUDDING discovery process at scale automatically via the 5-stage pipeline. |
| **Trigger** | Scheduled harvest triggers (T1 every 4hrs; T2 every 8hrs; T3 daily; T4 weekly). |
| **Steps** | 1\. HARVEST: Run SearXNG queries across 4-tier source taxonomy.    T1: Primary domain every 4 hours. T2: Cross-domain every 8 hours. T3: Weak signals daily. T4: Serendipity pool weekly. 2\. SemHash dedup: ensure only new/changed content enters the pipeline. 3\. EXTRACT: Run two parallel layers — spaCy NER \+ dependency parsing (deterministic) AND Ollama llama3.1:70b (AI layer). Both scored — data decides winner. 4\. LABEL: Apply PUDDING 2026 labels (WHAT.HOW.SCALE.TIME) and semantic dimensions. Phi-4-mini handles Layers 1-4 locally. 5\. MATCH: Find structural equivalences across domains. Jaccard slot calculation for pattern alignment. Amazon's clipped SGD for anomaly detection. TrustGraph for FalkorDB queries. 6\. SCORE & SURFACE: Apply PUDDING scoring formula. Threshold ≥12/20 to proceed. Surface top-scoring connections to dashboard. 7\. Update dashboard at pudding.beast.amplifiedpartners.ai. \[DERIVED\] |
| **Inputs** | SearXNG search results; vault contents; scheduled harvest triggers. |
| **Outputs** | Ranked PUDDING connections with scores; dashboard display; vault enrichment. |
| **Owner** | APDS Pipeline (automated) |
| **Tools / Skills Required** | SearXNG (on Beast), SemHash, spaCy, Ollama llama3.1:70b, Phi-4-mini, FalkorDB \+ TrustGraph, PUDDING Scoring Formula |
| **Frequency** | T1 every 4hrs; T2 every 8hrs; T3 daily; T4 weekly (scheduled). |

| PUDDING 2026 Label Assignment |  |
| :---- | :---- |
| **Purpose** | Assign a 4-character structural label to any concept for cross-domain pattern matching. |
| **Trigger** | Any new concept entering the vault or being processed in a PUDDING session. |
| **Steps** | 1\. Read the concept and strip away the domain name and expert attribution. 2\. Ask: 'What TYPE of thing is this?' → assign WHAT code (P/I/R/E/S/C/M). 3\. Ask: 'How does it BEHAVE over time?' → assign HOW code (=/+/-/\>/\~/\!/?). 4\. Ask: 'How WIDE is its effect?' → assign SCALE code (0/1/2/3/4/5/6). 5\. Ask: 'How LONG does it persist?' → assign TIME code (i/m/l/v/p/∞). 6\. Write the label: WHAT.HOW.SCALE.TIME. 7\. Look for other concepts with identical or near-identical labels across different domains. \[DERIVED\] 8\. Flag any 4/4 matches (p\<0.001) for immediate review. \[DERIVED\] |
| **Inputs** | Any concept from any domain. |
| **Outputs** | 4-character structural label; flagged matches if found. |
| **Owner** | Gatekeeper Agent / APDS / Manual (during sessions) |
| **Tools / Skills Required** | PUDDING 2026 Label Notation System, FalkorDB |
| **Frequency** | Every concept ingestion (continuous). |

| Expert-to-PUDDING-Ingredient Transformation |  |
| :---- | :---- |
| **Purpose** | Transform expert frameworks from the 27-Expert Library into PUDDING-ready, rubrik-mapped scoring functions. |
| **Trigger** | New expert framework added to Expert Research Library. \[DERIVED\] |
| **Steps** | 1\. INGEST the principle — create structured node in kg\_expert\_library (FalkorDB). 2\. STRIP the expert name — produce neutral mechanism label. 3\. APPLY PUDDING 2026 label → WHAT.HOW.SCALE.TIME. 4\. MAP to rubrik — create edge connecting principle to rubrik with scoring weight. 5\. DEFINE metrics — measurable outcomes become data collection targets. 6\. SCORE automatically — business data scored against principle's metrics. \[DERIVED\] 7\. MIX across domains — identify Swanson connections between experts who never read each other. \[DERIVED\] |
| **Inputs** | Expert frameworks (publicly available wisdom); 27-Expert Library reference. |
| **Outputs** | PUDDING-labelled, rubrik-mapped scoring functions in kg\_expert\_library. |
| **Owner** | Expert Library Agent \[TBD\] |
| **Tools / Skills Required** | FalkorDB (kg\_expert\_library), PUDDING 2026 labels, 7 Operational Rubriks, Swanson ABC Model |
| **Frequency** | Per new expert framework addition (event-driven). |


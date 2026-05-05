---
title: "**Table of Contents**"
id: "dept-1-governance-processes-2-docx"
version: 1
created: "2026-04-25"
type: "document"
topic_type: "unsorted"
audience: "internal"
layer: "shadow"
status: "filed"
signed_by: "Devon, 2026-04-25, devin-992682c244cf444f91e0a516498afbfd"
---

  
**Governance & Strategy**

Process Handbook

Amplified Partners

|  |
| :---- |

*Actionable processes derived from the Governance & Strategy methodologies.*

*This document tells an agent or person exactly what to do.*

March 2026

# **Table of Contents**

# **Introduction**

This Process Handbook is the operational companion to the Governance & Strategy Methodology Reference. Where the Methodology Reference describes what each framework is and why it exists, this handbook describes exactly what to do.

Each process entry includes a clear purpose, trigger, numbered steps, required inputs and outputs, the responsible owner, tools required, and the expected frequency. This document is designed to be used directly by agents and human team members as an operational guide.

## **Reading This Document**

Steps are categorised as either **stated** (explicitly defined in the source methodology) or **\[DERIVED\]** (logically inferred from the methodology description to make the process actionable). Derived steps are marked with the **\[DERIVED\]** tag in rust-coloured text so they can be reviewed and validated by the Governance & Strategy team.

Where an owner is not explicitly specified in the source material, it is marked as TBD.

# **Processes**

## **Process 1: Attribution Tagging Process**

| Source Methodology | ATTRIBUTION-AND-CURATION-v1 \+ Radical Attribution Schema |
| :---- | :---- |
| **Purpose** | Ensure every artefact produced within the Amplified system carries a complete provenance chain with all seven attribution elements. |
| **Trigger** | Any output, document, or framework reference is created or modified within the Amplified system. |
| **Inputs** | Any output from any Amplified work session, PUDDING session, or build session. |
| **Outputs** | Attribution-tagged artefact with complete provenance chain, suitable for vault ingestion. Footer in standard attribution format. |
| **Owner** | Every agent and human contributor (shared responsibility); final verification TBD. |
| **Tools / Skills** | Document YAML Frontmatter Standard, Radical Attribution Schema template, vault ingestion system. |
| **Frequency** | Every output — applied to every artefact before storage or publication. |

**Steps:**

1. **\[DERIVED\]** Identify all human contributors and their roles (originator, adapter, editor, approver, etc.).  
2. Identify all AI contributors: record name, model version, and role (originator / formaliser / researcher / builder / mixer / editor / approver / fact-checker / alternative-perspective).  
3. Credit Don Swanson as theoretical foundation (ABC model, 1986\) for any PUDDING-related output.  
4. Credit Ewan Bramley as adapter who brought Literature-Based Discovery (LBD) to business knowledge synthesis.  
5. Document source domains — where the knowledge came from.  
6. Document intellectual lineage — named experts whose work was used.  
7. Calculate and record Fact Percentage: what percentage of the output is verifiable fact versus opinion.  
8. Assign Confidence Band: high / medium / low / emerging.  
9. Compose the attribution footer in the standard format: 'Attribution: \[Human\] (role) × \[AI\] (role) × \[AI\] (role) | Fact %: \[N\] | Confidence: \[H/M/L/E\] | PUDDING: \[X.X.X.X\] | LBD: Swanson (1986) ABC Model'.  
10. **\[DERIVED\]** Apply Document YAML Frontmatter Standard to the artefact header.  
11. **\[DERIVED\]** Verify all seven elements are present before storing, sharing, or publishing.

## **Process 2: Win-Win Alignment Check**

| Source Methodology | Disclosed Manipulation Manifesto (Win-Win Alignment Principle) |
| :---- | :---- |
| **Purpose** | Verify that every system action influencing user behaviour is disclosed, anchored to the user's own stated goals, and passes the Win-Win Test. |
| **Trigger** | Any proposed agent or system action that involves influencing user behaviour. |
| **Inputs** | Proposed agent or system action; user's stated goals (recorded at onboarding). |
| **Outputs** | Approved action (win-win confirmed) or blocked action with written explanation. |
| **Owner** | Every agent (automated check); Governance & Strategy team (oversight). OPIK metric tracked automatically. |
| **Tools / Skills** | OPIK custom metrics platform, session self-rating YAML, 4-Layer Prompt Architecture. |
| **Frequency** | Per-action — every time an agent proposes a behavioural influence action. |

**Steps:**

1. At onboarding, disclose explicitly that the system uses behavioural design techniques.  
2. Define the user's stated goals at the start of every engagement and record them.  
3. For each proposed action, verify that all nudges and influence techniques are anchored only to the user's stated goals.  
4. Apply the Win-Win Test: determine whether the proposed action benefits both Amplified and the client. If it is not win-win, block the action.  
5. **\[DERIVED\]** If the action is blocked, generate an explanation of why it failed the Win-Win Test and log it.  
6. Track compliance via the OPIK custom metric 'Win-Win Alignment'.  
7. **\[DERIVED\]** Report any blocked actions in the session self-rating.

## **Process 3: Layer 0 Law Injection and Compliance Verification**

| Source Methodology | Eight Laws of Amplified Partners (Layer 0 / 8 Operational Laws) |
| :---- | :---- |
| **Purpose** | Inject the Eight Laws as Layer 0 into every agent prompt and verify that all outputs comply with constitutional governance. |
| **Trigger** | Any agent session, build sprint, or human work session begins. |
| **Inputs** | Agent session configuration; 4-Layer Prompt Architecture template; Eight Laws document. |
| **Outputs** | Compliant work artefact with documentation, attribution, and self-rating. |
| **Owner** | System architecture (automated injection); agent (self-rating); Governance & Strategy team (audit). |
| **Tools / Skills** | 4-Layer Prompt Architecture, session self-rating YAML, Biological Decision Logic Taxonomy. |
| **Frequency** | Every session — applied to every agent invocation and human work session. |

**Steps:**

1. Load the Eight Laws as Layer 0 of the 4-Layer Prompt Architecture before any other layer.  
2. **\[DERIVED\]** Verify that all eight laws are present and unmodified in the prompt: (1) Radical Honesty, (2) Transparency, (3) Attribution, (4) Win-Win Only, (5) White Hat, (6) Help Not Hurt, (7) Add Not Reduce, (8) Give Value Away.  
3. **\[DERIVED\]** Confirm that no downstream layer or task context has overridden or weakened any Layer 0 law.  
4. Execute the work session within these constraints.  
5. **\[DERIVED\]** At session end, complete the session self-rating against each of the Eight Laws.  
6. Document any compliance issues, attributions, and self-ratings in the output artefact.

## **Process 4: Governance Rule Classification (70/30 Split)**

| Source Methodology | Enforcement Reality Framework (70/30 Split) |
| :---- | :---- |
| **Purpose** | Classify each governance rule as either hard-blocked (code-enforced) or soft-nudge (agent-instructed) to prevent overclaiming about system enforcement. |
| **Trigger** | A new governance rule is created or an existing rule is reviewed. |
| **Inputs** | Any governance rule or ethical constraint within the Amplified system. |
| **Outputs** | Honest compliance classification (hard-blocked / soft-nudge); accurate production readiness rating; updated operational documentation. |
| **Owner** | Governance & Strategy team; system architect (for hard-block verification). |
| **Tools / Skills** | Governance rule registry, Build Quality Framework, code review tools. |
| **Frequency** | Per-rule creation; periodic review (quarterly recommended). |

**Steps:**

1. **\[DERIVED\]** Identify the governance rule to be classified.  
2. Determine if the rule is technically enforced by code (hard-blocked — the system prevents violation) or relies on agent compliance (soft-nudge — the agent is instructed but not technically blocked).  
3. Document the classification explicitly: mark as 'Hard-blocked' or 'Soft-nudge'.  
4. **\[DERIVED\]** For hard-blocked rules, verify that the code enforcement mechanism exists and functions.  
5. For soft-nudge rules, use 'strongly encouraged' language in all operational materials — never claim enforcement.  
6. **\[DERIVED\]** Update operational documentation with the honest compliance classification.  
7. **\[DERIVED\]** Review the overall split periodically to track maturity (target: increase hard-blocked percentage over time).

## **Process 5: Staff AI Adoption Interview**

| Source Methodology | Layered Interview Sequence with Permission Gates |
| :---- | :---- |
| **Purpose** | Progressively introduce AI to client staff through a consent-gated interview that builds trust and captures a baseline capability profile. |
| **Trigger** | AI adoption process begins at a client organisation; a staff member is identified for onboarding. |
| **Inputs** | Staff member in a client organisation; AI adoption timeline; interview environment (private, comfortable setting). |
| **Outputs** | Staff member's informed consent to AI assistance; baseline capability profile stored in vault. |
| **Owner** | Client engagement lead; AI adoption specialist. TBD: which specific agent role conducts the interview. |
| **Tools / Skills** | Interview script/template, vault storage system, attribution tagging process. |
| **Frequency** | Per-staff-member — once during the AI adoption process for each individual. |

**Steps:**

1. Layer 1 — Ask the open professional question: 'What brought you to this role?' Record response.  
2. Layer 2 — Ask the daily experience question: 'What's a typical day like?' Record response.  
3. Layer 3 — Identify friction: 'What takes the most time?' Record response.  
4. **\[DERIVED\]** Before proceeding to Layer 4, request explicit permission from the staff member to continue to deeper questions.  
5. Layer 4 — Skills assessment: 'What do you think you're good at?' Record response.  
6. Layer 5 — Gap acknowledgement: 'What are you not so good at?' Record response.  
7. **\[DERIVED\]** Before proceeding to Layer 6, request explicit permission to offer AI assistance.  
8. Layer 6 — Offer of help: 'Want some help?' Only proceed if consent is given.  
9. **\[DERIVED\]** Compile the staff member's responses into a baseline capability profile.  
10. **\[DERIVED\]** Store the capability profile in the vault with full attribution.

## **Process 6: No-Redundancy Guarantee Enforcement**

| Source Methodology | No-Redundancy Guarantee (Year-One Contract Term) |
| :---- | :---- |
| **Purpose** | Enforce the contractual commitment that no client staff member is made redundant in year one of Amplified implementation. |
| **Trigger** | Client signs the Amplified engagement contract containing the No-Redundancy Guarantee. |
| **Inputs** | Signed client engagement contract; AI automation deployment plan; staff headcount data. |
| **Outputs** | Contractual protection for client staff; trust signal for AI adoption; redeployment plan for freed capacity. |
| **Owner** | Client engagement lead; Amplified leadership (for escalation decisions). |
| **Tools / Skills** | Contract management system, time-tracking/automation measurement tools, redeployment planning template. |
| **Frequency** | Per-client engagement — continuous monitoring throughout year one. |

**Steps:**

1. Ensure the No-Redundancy Guarantee is written into the client contract as a binding term (not advisory).  
2. At implementation start, quantify time freed by AI automation (benchmark: estimated 57 hours/week, 1.4 FTE).  
3. **\[DERIVED\]** Create a redeployment plan: redirect freed staff time to higher-value roles (content creation, customer relationships, soft skills development).  
4. **\[DERIVED\]** Monitor compliance monthly throughout year one.  
5. If client proposes redundancies within year one, escalate immediately to Amplified leadership.  
6. If redundancy proposal is not withdrawn, execute the exit clause: Amplified exits the engagement.  
7. **\[DERIVED\]** Document the outcome and update contract templates if lessons are learned.

## **Process 7: Progressive Fairness Pricing Verification**

| Source Methodology | Progressive Fairness Pricing Principle |
| :---- | :---- |
| **Purpose** | Verify that all clients receive identical analytical quality regardless of pricing tier, with only service level differentiated. |
| **Trigger** | A new client engagement begins at any pricing tier, or a pricing tier change occurs. |
| **Inputs** | Client engagement at any pricing tier; Business Physics Suite configuration; pricing tier documentation. |
| **Outputs** | Equal analytical quality confirmed for all clients; differentiated service level documented; audit trail. |
| **Owner** | Governance & Strategy team; Pricing lead. TBD: automated audit agent. |
| **Tools / Skills** | Business Physics Suite, 6-Tier Pricing Model documentation, audit log. |
| **Frequency** | Per-client onboarding; quarterly audit across all active clients. |

**Steps:**

1. Confirm that all deterministic rubric logic (Business Physics Suite) is configured to run identically for this client regardless of their pricing tier.  
2. Verify that higher tiers receive more agent time, more features, and faster response — but not different or better analytical quality.  
3. **\[DERIVED\]** Review all client-facing materials to ensure no 'premium accuracy' claim is made for higher-paying clients.  
4. Communicate explicitly to the client: 'The same rubrics that apply to our largest client apply to you.'  
5. **\[DERIVED\]** Audit rubric outputs periodically to confirm identical analytical logic across tiers.

## **Process 8: SOUL.md Constitutional Override Check**

| Source Methodology | SOUL.md (7 Core Principles) |
| :---- | :---- |
| **Purpose** | Ensure that SOUL.md principles are injected at Layer 0 of every agent prompt and that no agent action violates them. |
| **Trigger** | Every agent invocation, every build session, every human work output. |
| **Inputs** | SOUL.md document (48 lines); agent prompt configuration; 4-Layer Prompt Architecture. |
| **Outputs** | Principle-compliant behaviour from every agent and human in the system; compliance log. |
| **Owner** | System architecture (automated injection); every agent (compliance); Governance & Strategy team (audit). |
| **Tools / Skills** | 4-Layer Prompt Architecture, session self-rating YAML, SOUL.md document. |
| **Frequency** | Every session — continuous, applied to every agent invocation and build session. |

**Steps:**

1. Load SOUL.md principles at Layer 0 of the agent prompt, before any other instructions.  
2. **\[DERIVED\]** Verify that all 7 principles are present (3 named: Radical Honesty, Radical Attribution, Meritocracy of Ideas; 4 additional as documented).  
3. **\[DERIVED\]** Confirm that no downstream prompt layer has overridden SOUL.md principles.  
4. **\[DERIVED\]** During execution, test each output against the SOUL.md principles before finalising.  
5. **\[DERIVED\]** If a violation is detected, block the output and generate an explanation referencing the specific violated principle.  
6. **\[DERIVED\]** Log all compliance checks in the session self-rating.

## **Process 9: Three-Ring Architecture Mapping**

| Source Methodology | Three-Ring Architecture |
| :---- | :---- |
| **Purpose** | Classify and map all Amplified frameworks into the correct ring (Constitutional, Quality System, or Engines) to maintain architectural coherence. |
| **Trigger** | A new framework or methodology is introduced to the Amplified system, or the architecture is reviewed. |
| **Inputs** | New or existing framework documentation; current Three-Ring Architecture map. |
| **Outputs** | Updated integration map; framework classification (Ring 1/2/3); documented rationale. |
| **Owner** | Governance & Strategy team; Chief Architect. TBD: architecture review agent. |
| **Tools / Skills** | Three-Ring Architecture diagram, framework registry, APQC PCF numbering system. |
| **Frequency** | Per-framework introduction; annual architecture review. |

**Steps:**

1. **\[DERIVED\]** Identify the new or existing framework to be mapped.  
2. Assess whether it belongs to Ring 1 (Constitution — immutable, overrides everything), Ring 2 (Quality System — structural, ISO 9001/APQC/PDCA), or Ring 3 (Engines — operational, runs daily).  
3. **\[DERIVED\]** For Ring 1 candidates, verify that the framework is truly immutable and should override all other layers.  
4. **\[DERIVED\]** For Ring 2 candidates, confirm alignment with ISO 9001 and APQC PCF numbering.  
5. **\[DERIVED\]** For Ring 3 candidates, verify that the framework operates within Ring 2 constraints.  
6. **\[DERIVED\]** Update the integration map showing how all frameworks nest inside each other.  
7. **\[DERIVED\]** Document the mapping decision with rationale.

## **Process 10: Ulysses Clause Lock Process**

| Source Methodology | Ulysses Clause |
| :---- | :---- |
| **Purpose** | Identify decisions vulnerable to future pressure and lock them as constitutional constraints that cannot be overridden in the moment. |
| **Trigger** | An architectural, ethical, or data sovereignty decision is being made that could be reversed under future pressure. |
| **Inputs** | Proposed architectural, ethical, or data sovereignty decision; risk assessment of future pressure scenarios. |
| **Outputs** | Locked constitutional constraint; mechanical enforcement (where possible); registry entry with rationale. |
| **Owner** | Governance & Strategy team; Agent Council (for change requests). |
| **Tools / Skills** | Constitutional document suite (SOUL.md, Eight Laws, ATTRIBUTION-AND-CURATION-v1), Ulysses Clause registry, Agent Council review process. |
| **Frequency** | Per-decision — whenever a foundational decision is made that qualifies for Ulysses protection. |

**Steps:**

1. At design time, identify decisions that future stakeholders might reverse under cost pressure, client pressure, or investor pressure.  
2. **\[DERIVED\]** Evaluate the decision against the Ulysses Clause criteria: is this a decision where in-the-moment reversal would cause lasting harm?  
3. **\[DERIVED\]** If yes, draft the constraint as a constitutional provision and submit for review.  
4. Lock the decision as a constitutional constraint in writing (SOUL.md, Eight Laws, or ATTRIBUTION-AND-CURATION-v1).  
5. Where possible, encode enforcement mechanically via code blocks, not just written principles.  
6. **\[DERIVED\]** Document the locked decision in the Ulysses Clause registry with the original rationale.  
7. Any future request to change a Ulysses-locked decision must go through the full Agent Council review — no in-session overrides permitted.

## **Process 11: APQC Process Classification and Atom ID Assignment**

| Source Methodology | APQC Process Classification Framework (PCF) |
| :---- | :---- |
| **Purpose** | Classify every business process against the APQC 13-category taxonomy and assign standardised atom IDs. |
| **Trigger** | A new process atom, rubric, or analytical lens is created within the Amplified system. |
| **Inputs** | New process documentation; APQC PCF taxonomy; existing atom ID registry. |
| **Outputs** | Classified process with standardised atom ID; updated process registry; APQC attribution recorded. |
| **Owner** | Knowledge architecture team; process documentation lead. TBD: automated classification agent. |
| **Tools / Skills** | APQC PCF taxonomy reference, PUDDING atom ID generator, process registry. |
| **Frequency** | Per-process creation — whenever a new process is documented. |

**Steps:**

1. **\[DERIVED\]** Identify the business process to be classified.  
2. **\[DERIVED\]** Map the process to the correct APQC category (1–13) using the PCF taxonomy.  
3. Assign a PUDDING atom ID in the standard format: AMP-{APQC\#}-{SEQ}-{VERSION} (e.g. AMP-08-0042-v1).  
4. **\[DERIVED\]** Verify that the atom ID is unique and does not conflict with existing IDs.  
5. **\[DERIVED\]** Map the process to the relevant Analytical Lens (12 lenses map to 13 APQC categories).  
6. **\[DERIVED\]** Record the classification in the process registry with APQC category attribution.  
7. **\[DERIVED\]** Explicitly cite APQC as the source of the classification taxonomy (addressing the identified attribution gap).

## **Process 12: GDPR Article 17 Erasure via P2 Tokenization**

| Source Methodology | GDPR / CASL / CCPA \+ P2 Tokenization Architecture (SKILL-12) |
| :---- | :---- |
| **Purpose** | Satisfy GDPR right-to-erasure requests by deleting token mappings in the P2 tokenization architecture, rendering personal data permanently irreversible. |
| **Trigger** | A data subject exercises their GDPR Article 17 right to erasure, or an equivalent CCPA/CASL request is received. |
| **Inputs** | Verified erasure request from data subject; P2 token-to-PII mapping database. |
| **Outputs** | Permanently de-identified data; erasure confirmation; audit log entry. |
| **Owner** | Data Protection Officer (DPO); system administrator. TBD: specific agent role. |
| **Tools / Skills** | P2 Tokenization Architecture (SKILL-12), token mapping database, erasure request tracking system. |
| **Frequency** | Per-request — whenever a data subject exercises erasure rights. |

**Steps:**

1. **\[DERIVED\]** Receive and validate the erasure request (verify identity of data subject).  
2. **\[DERIVED\]** Identify all tokens associated with the data subject in the P2 tokenization system.  
3. Delete the token-to-PII mapping entries for the data subject.  
4. **\[DERIVED\]** Verify that the underlying data structure remains intact but is now permanently de-identified (tokens without mappings cannot be reversed).  
5. Confirm that GDPR Article 17 erasure requirements are satisfied without destroying the broader data structure.  
6. **\[DERIVED\]** Log the erasure action with timestamp and confirmation.  
7. **\[DERIVED\]** Notify the data subject that their erasure request has been fulfilled.

## **Process 13: ISO 9001 Compliance Documentation and Gap Analysis**

| Source Methodology | ISO 9001:2015 — Quality Management System |
| :---- | :---- |
| **Purpose** | Document every client business process against ISO 9001 clauses and maintain the gap analysis showing compliance status. |
| **Trigger** | A new client engagement begins, or a periodic compliance review is due. |
| **Inputs** | Client business process documentation; ISO 9001:2015 standard; 360° Operational Frameworks template. |
| **Outputs** | Fully documented business processes; clause-by-clause gap analysis; improvement action items; progress toward ISO 9001 qualification. |
| **Owner** | Quality & Standards lead; client engagement team. TBD: automated documentation agent. |
| **Tools / Skills** | 360° Operational Frameworks, APQC PCF numbering, PDCA cycle template, session self-rating YAML. |
| **Frequency** | Per-client engagement; annual re-assessment. |

**Steps:**

1. **\[DERIVED\]** Map the client's business processes to ISO 9001:2015 Clauses 4–10 (Context, Leadership, Planning, Support, Operation, Performance Evaluation, Improvement).  
2. Document each process using the 360° Operational Frameworks template (described as 'ISO 9001 in a box').  
3. **\[DERIVED\]** Apply the PDCA cycle (Plan-Do-Check-Act) to each documented process.  
4. Complete the clause-by-clause gap analysis comparing current state to ISO 9001 requirements.  
5. **\[DERIVED\]** For each gap, create an improvement action item with owner and deadline.  
6. Map the SKILL-10 Session Self-Rating YAML to ISO 9001 Clause 9 (Performance Evaluation).  
7. **\[DERIVED\]** Track progress toward ISO 9001 qualification as a visible client outcome.

## **Process 14: Business Continuity Planning (ISO 22301\)**

| Source Methodology | ISO 22301 — Business Continuity Management |
| :---- | :---- |
| **Purpose** | Establish and maintain business continuity plans for client organisations using ISO 22301 BIA templates. |
| **Trigger** | Client onboarding reaches the continuity planning phase, or a periodic review is due. |
| **Inputs** | Client organisation structure; critical role identification; IT infrastructure documentation; ISO 22301 BIA templates. |
| **Outputs** | Completed BIA; succession plans; IT disaster recovery plan; emergency response procedures; documented in 360° OS Section 11\. |
| **Owner** | Client engagement team; business continuity lead. TBD: specific agent role. |
| **Tools / Skills** | ISO 22301 BIA templates, 360° Operational Frameworks (Section 11), succession planning templates. |
| **Frequency** | Per-client engagement; annual review. |

**Steps:**

1. **\[DERIVED\]** Conduct a Business Impact Analysis (BIA) using ISO 22301 templates.  
2. **\[DERIVED\]** Assess key person risk for critical roles in the client organisation.  
3. **\[DERIVED\]** Develop succession planning documentation.  
4. **\[DERIVED\]** Create IT disaster recovery plans.  
5. **\[DERIVED\]** Develop emergency response procedures.  
6. Document all continuity plans in the 360° OS Continuity section (Section 11).  
7. **\[DERIVED\]** Review and update plans annually or after any significant organisational change.

# **Appendix: Process Quick Reference**

The following table provides a quick-reference summary of all processes, their triggers, and frequency.

| Process | Trigger | Frequency | \# Steps |
| :---- | :---- | :---- | :---- |
| Attribution Tagging Process | Any output, document, or framework reference is created or modified within the Amplified system. | Every output — applied to every artefact before storage or publication. | 11 (8 stated, 3 derived) |
| Win-Win Alignment Check | Any proposed agent or system action that involves influencing user behaviour. | Per-action — every time an agent proposes a behavioural influence action. | 7 (5 stated, 2 derived) |
| Layer 0 Law Injection and Compliance Verification | Any agent session, build sprint, or human work session begins. | Every session — applied to every agent invocation and human work session. | 6 (3 stated, 3 derived) |
| Governance Rule Classification (70/30 Split) | A new governance rule is created or an existing rule is reviewed. | Per-rule creation; periodic review (quarterly recommended). | 7 (3 stated, 4 derived) |
| Staff AI Adoption Interview | AI adoption process begins at a client organisation; a staff member is identified for onboarding. | Per-staff-member — once during the AI adoption process for each individual. | 10 (6 stated, 4 derived) |
| No-Redundancy Guarantee Enforcement | Client signs the Amplified engagement contract containing the No-Redundancy Guarantee. | Per-client engagement — continuous monitoring throughout year one. | 7 (4 stated, 3 derived) |
| Progressive Fairness Pricing Verification | A new client engagement begins at any pricing tier, or a pricing tier change occurs. | Per-client onboarding; quarterly audit across all active clients. | 5 (3 stated, 2 derived) |
| SOUL.md Constitutional Override Check | Every agent invocation, every build session, every human work output. | Every session — continuous, applied to every agent invocation and build session. | 6 (1 stated, 5 derived) |
| Three-Ring Architecture Mapping | A new framework or methodology is introduced to the Amplified system, or the architecture is reviewed. | Per-framework introduction; annual architecture review. | 7 (1 stated, 6 derived) |
| Ulysses Clause Lock Process | An architectural, ethical, or data sovereignty decision is being made that could be reversed under future pressure. | Per-decision — whenever a foundational decision is made that qualifies for Ulysses protection. | 7 (4 stated, 3 derived) |
| APQC Process Classification and Atom ID Assignment | A new process atom, rubric, or analytical lens is created within the Amplified system. | Per-process creation — whenever a new process is documented. | 7 (1 stated, 6 derived) |
| GDPR Article 17 Erasure via P2 Tokenization | A data subject exercises their GDPR Article 17 right to erasure, or an equivalent CCPA/CASL request is received. | Per-request — whenever a data subject exercises erasure rights. | 7 (2 stated, 5 derived) |
| ISO 9001 Compliance Documentation and Gap Analysis | A new client engagement begins, or a periodic compliance review is due. | Per-client engagement; annual re-assessment. | 7 (3 stated, 4 derived) |
| Business Continuity Planning (ISO 22301\) | Client onboarding reaches the continuity planning phase, or a periodic review is due. | Per-client engagement; annual review. | 7 (1 stated, 6 derived) |


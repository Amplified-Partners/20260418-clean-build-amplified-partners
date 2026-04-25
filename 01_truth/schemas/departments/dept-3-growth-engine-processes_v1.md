---
title: "Dept 3 Growth Engine Processes"
id: "dept-3-growth-engine-processes"
version: 1
created: 2026-04-25
last_validated: 2026-04-25
type: document
topic_type: reference
status: imported
source_file: "dept-3-growth-engine-processes.docx.md"
signed_by: "Devon, 2026-04-25, devin-992682c244cf444f91e0a516498afbfd"
---

  
**Growth Engine**

**(Marketing & Sales)**

Process Handbook

Content creation, brand voice, marketing automation, sales processes, community building.

The 14-agent marketing pipeline, content atomisation, value-based outreach.

Amplified Partners — Byker Business Help

March 2026

# **Table of Contents**

# **How to Use This Handbook**

This handbook documents the actionable processes within the Growth Engine (Marketing & Sales) department. Each process is self-contained and includes all the information needed for execution.

**Process structure:** Each process includes a summary table (purpose, trigger, inputs, outputs, owner, tools, frequency) followed by numbered steps.

**Derived steps:** Steps marked **\[DERIVED\]** have been inferred from the methodology source material to make the process complete and actionable. They are not explicitly stated in the original source but are logically necessary for process execution.

**Owners:** Marked as TBD where ownership has not been formally assigned. These should be allocated during department setup.

**Cross-references:** Processes reference other processes by name where dependencies exist. Refer to the referenced process for detailed steps.

# **Growth Engine Processes**

## **Process 1: 14-Agent Content Production Pipeline Execution**

| Purpose | Execute the full automated content production cycle for a client, from strategy through publication and analytics, using the 14-agent marketing pipeline. |
| :---- | :---- |
| **Trigger** | Client content brief submitted OR scheduled content cycle begins per Client YAML cadence settings. |
| **Inputs** | Client YAML config; content brief or brief queue; brand voice guidelines (VOICE\_MIRROR.md); FalkorDB knowledge graph data |
| **Outputs** | Published multi-format content across all configured channels; performance analytics; quality scores; content calendar |
| **Owner** | TBD (Growth Engine Pipeline Lead) |
| **Tools / Skills** | Python pipeline framework, SearXNG, FalkorDB, Client YAML, VOICE\_MIRROR.md, WOW-ZIGLAR-LUND rubrik, ExecutiveDiscussionWorkflow |
| **Frequency** | Per client content cadence (configured in Client YAML — typically daily/weekly) |

**Steps**

1. Strategy agent analyses client brief and FalkorDB knowledge graph; determines content strategy

2. Research agent performs SearXNG-first research for each content piece; extracts facts and angles

3. Brand Voice agent loads and applies VOICE\_MIRROR.md to ensure client brand consistency

4. Content agents (multiple specialisations) draft content per format and platform

5. DISC personalisation agent adapts content to target audience's DISC profile from Client YAML

6. Quality agent applies content quality rubric; scores against WOW-ZIGLAR-LUND criteria

7. Content scoring below threshold returned to Content agents for revision with specific feedback  **\[DERIVED\]**

8. Optimisation agent applies SEO, readability, and platform-specific adjustments

9. Scheduling agent sequences content calendar for optimal posting times

10. Distribution agents (platform-specific) publish to all configured channels

11. Analytics agent tracks performance metrics; feeds results back to Strategy agent

12. For major content decisions, escalate to AI Board review (ExecutiveDiscussionWorkflow) for strategy pivots

13. Log pipeline run metrics to performance dashboard for client reporting  **\[DERIVED\]**

## **Process 2: Brand Voice Capture and Codification**

| Purpose | Capture, codify, and document a client's unique brand voice into VOICE\_MIRROR.md so that all AI-generated content is voice-consistent. |
| :---- | :---- |
| **Trigger** | New client onboarding OR client requests brand voice refresh (quarterly review cycle). |
| **Inputs** | Client existing content samples; client brief on desired voice; client interview notes |
| **Outputs** | VOICE\_MIRROR.md constitutional document; Client YAML config with voice parameters; baseline voice consistency score |
| **Owner** | TBD (Brand Voice Specialist) |
| **Tools / Skills** | VOICE\_MIRROR.md template, Client YAML, 14-Agent Pipeline (for testing), voice scoring rubric |
| **Frequency** | Once at onboarding; quarterly reviews for evolution |

**Steps**

1. Schedule and conduct brand voice interview with client — discuss tone, vocabulary, style preferences  **\[DERIVED\]**

2. Collect and analyse existing client content samples — extract language patterns, sentence structures, vocabulary

3. Identify voice characteristics: vocabulary norms, tone spectrum, sentence structure, prohibited language  **\[DERIVED\]**

4. Write VOICE\_MIRROR.md constitutional document: vocabulary, tone, sentence structure, what to avoid

5. Review VOICE\_MIRROR.md with client for accuracy and approval  **\[DERIVED\]**

6. Configure Client YAML with voice parameters and VOICE\_MIRROR.md file path  **\[DERIVED\]**

7. Inject VOICE\_MIRROR.md as Layer 1 of every content agent's prompt for that client

8. Run test content generation and score for voice consistency (0–10 scale)  **\[DERIVED\]**

9. Iterate on VOICE\_MIRROR.md until test content consistently passes threshold  **\[DERIVED\]**

## **Process 3: Brand Voice Enforcement and Scoring**

| Purpose | Continuously enforce brand voice consistency across all AI-generated content, catching and correcting off-voice content before publication. |
| :---- | :---- |
| **Trigger** | Every content piece generated by the 14-Agent Pipeline. |
| **Inputs** | Generated content piece; VOICE\_MIRROR.md; voice scoring threshold |
| **Outputs** | Voice-compliant content (score at or above threshold); revision feedback (if below threshold); voice score logs |
| **Owner** | TBD (Quality Agent / Brand Voice Specialist) |
| **Tools / Skills** | VOICE\_MIRROR.md, voice scoring rubric, 14-Agent Pipeline Quality agent |
| **Frequency** | Every content piece (continuous) |

**Steps**

1. Quality agent loads client's VOICE\_MIRROR.md and voice scoring criteria  **\[DERIVED\]**

2. Score the content piece for voice consistency on 0–10 scale against VOICE\_MIRROR.md parameters

3. If score meets or exceeds threshold: pass content to Optimisation agent  **\[DERIVED\]**

4. If score is below threshold: return content to Content agents with specific revision feedback

5. Content agents revise based on feedback and resubmit for re-scoring  **\[DERIVED\]**

6. Log voice scores for trend analysis and VOICE\_MIRROR.md evolution tracking  **\[DERIVED\]**

## **Process 4: Client YAML Configuration and Onboarding**

| Purpose | Create and deploy a complete Client YAML configuration file that provisions the entire multi-agent marketing pipeline for a new client. |
| :---- | :---- |
| **Trigger** | New client signs up for marketing pipeline service. |
| **Inputs** | Client onboarding information; brand voice interview output; platform preferences; integration credentials |
| **Outputs** | Complete Client YAML configuration file; fully provisioned marketing pipeline; successful test run confirmation |
| **Owner** | TBD (Client Onboarding Lead) |
| **Tools / Skills** | Client YAML schema template, VOICE\_MIRROR.md template, DISC assessment tool, 14-Agent Pipeline |
| **Frequency** | Once per new client onboarding |

**Steps**

1. Gather client onboarding information: business context (sector, size, target customers, location)  **\[DERIVED\]**

2. Conduct brand voice interview and produce VOICE\_MIRROR.md (see Brand Voice Capture process)

3. Classify target audience's primary DISC profile (D/I/S/C) for content personalisation

4. Define target platforms: list active channels with platform-specific settings

5. Set content frequency: posting cadence per platform

6. Configure channel priorities: weighted list of channels by importance

7. Add integration credentials: accounting system, CRM, and other connected systems

8. Populate Client YAML schema with all gathered parameters  **\[DERIVED\]**

9. Validate YAML configuration against schema requirements  **\[DERIVED\]**

10. Deploy YAML to provision the full 14-Agent Pipeline for this client  **\[DERIVED\]**

11. Run initial test content cycle to verify pipeline configuration end-to-end  **\[DERIVED\]**

## **Process 5: Content Atomisation (58-Format Derivatives)**

| Purpose | Maximise content ROI by slicing one master pillar document into 58 different content formats across multiple channels and platforms. |
| :---- | :---- |
| **Trigger** | Master pillar document completed or identified for atomisation. |
| **Inputs** | Master pillar document; 58-format inventory template; PUDDING labelling system |
| **Outputs** | Content calendar with up to 58 derivative pieces per pillar document; prioritised production schedule; free-content selection |
| **Owner** | TBD (Content Strategy Lead) |
| **Tools / Skills** | 58-format inventory template, PUDDING labelling system, 14-Agent Pipeline, content calendar tool |
| **Frequency** | Per master pillar document (typically monthly or per content campaign) |

**Steps**

1. Identify or create the master pillar document for atomisation

2. Apply PUDDING labelling to each section of the master document

3. Map each labelled section to the 58-format inventory: identify format, angle, target audience, platform

4. Score each potential derivative by reach × engagement potential  **\[DERIVED\]**

5. Prioritise derivatives by score; create production schedule in batches (e.g., social content week, long-form week)

6. Identify which derivatives to publish free to drive inbound (give-away-free strategy)

7. Produce derivative content in batch sequence using 14-Agent Pipeline  **\[DERIVED\]**

8. Apply brand voice enforcement to each derivative (see Brand Voice Enforcement process)  **\[DERIVED\]**

9. Build content calendar with all 58 derivative pieces, assigned to platforms and dates  **\[DERIVED\]**

10. Feed content calendar to Scheduling agent for automated distribution  **\[DERIVED\]**

## **Process 6: DISC Content Personalisation**

| Purpose | Adapt content framing, tone, and format for specific target audience segments based on their DISC personality profile. |
| :---- | :---- |
| **Trigger** | Content brief created with a defined target audience OR Client YAML DISC profile configured. |
| **Inputs** | Target audience DISC profile classification; content brief; Client YAML DISC configuration |
| **Outputs** | DISC-adapted content resonating with the specific audience type; DISC-configured Client YAML |
| **Owner** | TBD (Content Personalisation Lead) |
| **Tools / Skills** | DISC assessment criteria, Client YAML, 14-Agent Pipeline, The Pulse nudge layer |
| **Frequency** | Every content piece (continuous); DISC profile review quarterly |

**Steps**

1. Classify the target audience's primary DISC profile (D/I/S/C) using DISC assessment criteria

2. Load DISC-specific content adaptation rules for the identified profile  **\[DERIVED\]**

3. For D (Dominant): lead with results, numbers, ROI; keep short and punchy; emphasise 'what's in it for them'

4. For I (Influential): lead with stories, social proof, enthusiasm; use conversational and fun tone

5. For S (Steady): lead with reliability, process, step-by-step guidance; maintain warm, reassuring tone

6. For C (Conscientious): lead with data, evidence, detail; use precise, formal, well-sourced language

7. Configure DISC profile parameter in Client YAML for automated application

8. Marketing agents apply the selected DISC profile adaptations to every content piece

9. Verify content alignment with DISC profile during quality scoring  **\[DERIVED\]**

10. Apply DISC adaptation to Pulse nudge layer for client's own DISC profile (inward-facing communications)

## **Process 7: Four-Document Deliverable Production**

| Purpose | Ensure every significant Amplified work product comprises four mandatory documents covering all use cases: human reading, process replication, AI retrieval, and technical implementation. |
| :---- | :---- |
| **Trigger** | Any major Amplified output or deliverable is being finalised. |
| **Inputs** | Any major Amplified output or deliverable; voice transcripts; coding specifications |
| **Outputs** | Four-document package: Content Creation, Process, Master Document, Coding; each with YAML frontmatter |
| **Owner** | TBD (Deliverable Quality Lead) |
| **Tools / Skills** | Document templates, YAML frontmatter standard, Vault storage system, PUDDING labelling |
| **Frequency** | Every major deliverable |

**Steps**

1. Identify the deliverable and confirm it meets the threshold for four-document treatment  **\[DERIVED\]**

2. Produce Document 1 — Content Creation: narrative, marketing angles, audience-specific copy

3. Produce Document 2 — Process: how it was built, logic, methodology, step-by-step process

4. Produce Document 3 — Master Document: comprehensive reference; AI-readable; complete

5. Produce Document 4 — Coding: JSON/code specification with full voice transcripts adjacent to coding frameworks

6. Verify Document 4 includes full voice transcripts (mandatory requirement)  **\[DERIVED\]**

7. Apply PUDDING labelling and YAML frontmatter to each document  **\[DERIVED\]**

8. Review all four documents as a complete package for consistency and completeness  **\[DERIVED\]**

9. Store deliverable package in Vault with appropriate metadata  **\[DERIVED\]**

## **Process 8: Morning Briefing Preparation and Delivery (The Pulse)**

| Purpose | Prepare and deliver a daily morning briefing to each client through The Pulse PWA, presenting the most important business information in a calm, structured, zero-scroll format. |
| :---- | :---- |
| **Trigger** | Daily automated trigger — NightCrawler begins overnight; Morning layer populates at 06:00 client timezone. |
| **Inputs** | Overnight data from NightCrawler; client's 7 Operational Rubriks scores; client's Life Goals; client DISC profile; planned AI actions |
| **Outputs** | Morning briefing delivered via phone PWA; Glance layer status indicators; client approval/rejection of planned AI actions |
| **Owner** | TBD (Pulse Product Lead) |
| **Tools / Skills** | NightCrawler pipeline, The Pulse PWA, 7 Operational Rubriks scoring, DISC profile system, Autonomous Vehicle Trust Architecture |
| **Frequency** | Daily (365 days/year) |

**Steps**

1. NightCrawler overnight pipeline collects and processes client data while business is closed

2. NightCrawler aggregates overnight financial movements, schedule data, and operational alerts  **\[DERIVED\]**

3. Score client's 7 Operational Rubriks dimensions; generate red/amber/green status indicators for Glance layer

4. Identify top 3 priorities for the day from rubrik scores and schedule data  **\[DERIVED\]**

5. Link each briefing item back to relevant personal goal from client's Life Goals Meeting

6. Adapt briefing content to client's DISC profile for personalised delivery

7. Surface any AI actions planned for the day that require client approval (Autonomous Vehicle Trust Architecture)

8. At 06:00 client timezone: populate Morning layer with briefing content

9. Glance layer (always visible) displays red/amber/green status indicators

10. Morning layer follows Calm Technology design: no scroll, no overwhelm, only what matters

11. Capture client approval or rejection of planned AI actions  **\[DERIVED\]**

12. Feed client responses back to relevant agents for action or adjustment  **\[DERIVED\]**

## **Process 9: Sales Pipeline — SPIN Selling Execution**

| Purpose | Execute value-based sales conversations using the SPIN Selling methodology to qualify prospects and close deals through the 360° OS Sales Pipeline. |
| :---- | :---- |
| **Trigger** | New qualified lead enters the sales pipeline OR scheduled sales call with prospect. |
| **Inputs** | Prospect data; 360° OS findings (if available); Financial Autopsy results; sales playbook |
| **Outputs** | Qualified opportunity with clear next steps; CRM record updated; proposal or 360° OS offer extended |
| **Owner** | TBD (Sales Lead) |
| **Tools / Skills** | SPIN Selling framework, 360° OS, Financial Autopsy, CRM, Hormozi Value Equation, sales playbook |
| **Frequency** | Per qualified lead (continuous) |

**Steps**

1. Prepare for sales conversation by reviewing prospect data and 360° OS findings  **\[DERIVED\]**

2. Open with Situation questions: understand the prospect's current state, business context, and operations

3. Progress to Problem questions: identify specific pain points, challenges, and gaps the prospect faces

4. Deepen with Implication questions: explore the consequences and costs of leaving problems unresolved

5. Guide to Need-Payoff questions: help the prospect articulate the value of solving their problems

6. Apply Zig Ziglar relationship-selling philosophy: focus on how Amplified helps them get what they want  **\[DERIVED\]**

7. Present relevant Amplified solution aligned to identified needs, using Hormozi Value Equation framing  **\[DERIVED\]**

8. Handle objections using evidence from Financial Autopsy and deterministic rubrics  **\[DERIVED\]**

9. If appropriate, offer free 360° OS as PLG entry mechanism (Permission Marketing approach)  **\[DERIVED\]**

10. Log conversation outcomes and next steps in CRM  **\[DERIVED\]**

## **Process 10: Content Quality Assurance and WOW-ZIGLAR-LUND Scoring**

| Purpose | Score all content against the WOW-ZIGLAR-LUND quality rubric to ensure every published piece meets Amplified's quality standards. |
| :---- | :---- |
| **Trigger** | Content piece ready for quality review within the 14-Agent Pipeline. |
| **Inputs** | Content piece from pipeline; WOW-ZIGLAR-LUND rubric; VOICE\_MIRROR.md; quality thresholds |
| **Outputs** | Quality-approved content OR specific revision feedback; quality score logs; trend reports |
| **Owner** | TBD (Content Quality Lead) |
| **Tools / Skills** | WOW-ZIGLAR-LUND rubric, VOICE\_MIRROR.md, Quality agent, 14-Agent Pipeline, AI Board (escalation) |
| **Frequency** | Every content piece (continuous) |

**Steps**

1. Quality agent receives content piece from Content agents after DISC personalisation  **\[DERIVED\]**

2. Load WOW-ZIGLAR-LUND scoring criteria and client-specific quality thresholds  **\[DERIVED\]**

3. Score content against WOW-ZIGLAR-LUND rubric dimensions

4. Score content for voice consistency against VOICE\_MIRROR.md (see Brand Voice Enforcement)

5. If content passes all quality thresholds: approve and forward to Optimisation agent  **\[DERIVED\]**

6. If content fails any threshold: generate specific, actionable revision feedback  **\[DERIVED\]**

7. Return failing content to Content agents with revision instructions

8. Track quality scores over time for continuous improvement and agent performance monitoring  **\[DERIVED\]**

9. Escalate persistent quality issues to AI Board review for strategy assessment  **\[DERIVED\]**

## **Process 11: Product-Led Growth (PLG) Funnel Execution**

| Purpose | Execute the value-first go-to-market strategy by giving away the 360° OS at the top of the funnel, converting free users to paid through demonstrated value. |
| :---- | :---- |
| **Trigger** | Prospect engages with Amplified content or expresses interest in business improvement. |
| **Inputs** | Inbound prospects; 360° OS framework; content derivatives; pricing tiers; engagement metrics |
| **Outputs** | Converted paid clients; LTV:CAC metrics; expansion revenue; engagement analytics |
| **Owner** | TBD (Growth Lead) |
| **Tools / Skills** | 360° OS, Financial Autopsy, The Pulse, content pipeline, CRM, pricing framework, analytics |
| **Frequency** | Continuous (always-on funnel) |

**Steps**

1. Attract prospects through free content derivatives (give-away-free strategy from Content Atomisation)  **\[DERIVED\]**

2. Offer free 360° OS as entry point — Permission Marketing in practice

3. Deliver 360° OS with Financial Autopsy using deterministic rubrics (Altman Z-Score, Goldratt ToC, CCC)  **\[DERIVED\]**

4. Demonstrate value through the 360° OS findings — maximise Hormozi Value Equation numerator  **\[DERIVED\]**

5. Present £99/month entry tier as the PLG conversion mechanism

6. Apply Kotter's 8 Steps change management to the onboarding journey: create urgency from 360° OS findings  **\[DERIVED\]**

7. Use BJ Fogg B=MAP to reduce friction at every conversion point (Ability × Motivation × Prompt)  **\[DERIVED\]**

8. Apply Hook Model engagement cycle through The Pulse for daily client interaction  **\[DERIVED\]**

9. Track LTV:CAC ratio to ensure healthy unit economics across tiers  **\[DERIVED\]**

10. Expand accounts through demonstrated value — Schumacher Principle ensures right-sized solutions  **\[DERIVED\]**

## **Process 12: VOICE\_MIRROR.md Quarterly Evolution Review**

| Purpose | Review and update each client's VOICE\_MIRROR.md document quarterly to ensure it evolves with the client's brand voice. |
| :---- | :---- |
| **Trigger** | Quarterly calendar trigger OR client requests voice update. |
| **Inputs** | Current VOICE\_MIRROR.md; quarterly voice score trends; recent client content; client feedback |
| **Outputs** | Updated VOICE\_MIRROR.md; voice evolution log entry; refreshed pipeline prompts |
| **Owner** | TBD (Brand Voice Specialist) |
| **Tools / Skills** | VOICE\_MIRROR.md, voice scoring logs, 14-Agent Pipeline, client communication tools |
| **Frequency** | Quarterly |

**Steps**

1. Pull voice consistency score trends for the quarter from quality scoring logs  **\[DERIVED\]**

2. Analyse recent client content and communications for voice evolution indicators  **\[DERIVED\]**

3. Compare current VOICE\_MIRROR.md against recent high-scoring content to identify drift  **\[DERIVED\]**

4. Schedule review meeting with client to discuss voice evolution and any desired changes  **\[DERIVED\]**

5. Update VOICE\_MIRROR.md based on review findings and client feedback

6. Re-inject updated VOICE\_MIRROR.md as Layer 1 of all content agent prompts  **\[DERIVED\]**

7. Run validation content cycle to confirm updated voice parameters produce desired output  **\[DERIVED\]**

8. Document changes in voice evolution log for continuity tracking  **\[DERIVED\]**

# **Appendix: Process Quick Reference**

| \# | Process Name | Trigger | Frequency |
| :---- | :---- | :---- | :---- |
| 1 | 14-Agent Content Production Pipeline Execution | Client content brief submitted… | Per client content cadence (configured in Client YAML — typically daily/weekly) |
| 2 | Brand Voice Capture and Codification | New client onboarding… | Once at onboarding; quarterly reviews for evolution |
| 3 | Brand Voice Enforcement and Scoring | Every content piece generated by the 14-Agent Pipeline. | Every content piece (continuous) |
| 4 | Client YAML Configuration and Onboarding | New client signs up for marketing pipeline service. | Once per new client onboarding |
| 5 | Content Atomisation (58-Format Derivatives) | Master pillar document completed or identified for atomisati… | Per master pillar document (typically monthly or per content campaign) |
| 6 | DISC Content Personalisation | Content brief created with a defined target audience… | Every content piece (continuous); DISC profile review quarterly |
| 7 | Four-Document Deliverable Production | Any major Amplified output or deliverable is being finalised… | Every major deliverable |
| 8 | Morning Briefing Preparation and Delivery (The Pulse) | Daily automated trigger — NightCrawler begins overnight; Mor… | Daily (365 days/year) |
| 9 | Sales Pipeline — SPIN Selling Execution | New qualified lead enters the sales pipeline… | Per qualified lead (continuous) |
| 10 | Content Quality Assurance and WOW-ZIGLAR-LUND Scoring | Content piece ready for quality review within the 14-Agent P… | Every content piece (continuous) |
| 11 | Product-Led Growth (PLG) Funnel Execution | Prospect engages with Amplified content or expresses interes… | Continuous (always-on funnel) |
| 12 | VOICE\_MIRROR.md Quarterly Evolution Review | Quarterly calendar trigger | Quarterly |


---
title: "Master Audit And Defriction Estimates Copy"
id: "master-audit-and-defriction-estimates-copy"
version: 1
created: "2026-04-25"
type: "document"
topic_type: "audit"
audience: "internal"
layer: "truth"
status: "filed"
signed_by: "Devon, 2026-04-25, devin-992682c244cf444f91e0a516498afbfd"
---

Amplified Partners — Master Audit & Defriction Estimates — 16 March 2026
Page 1
Master Audit & Defriction Estimates
project-latest.md Audit | Vault Structure Map | 32-Process Defriction Model | Financial
Forecasts | 10 Flags for the Building AI
16 March 2026 — Prepared by Perplexity Computer for Ewan Bramley
Purpose: Flag everything the building AI needs to know. No solutions built. Just flags.
Contents
1. project-latest.md Audit — structure, gaps, outdated content
2. Vault Structure Map — every folder catalogued
3. Defriction Estimates — 32 processes, hours saved, money saved
4. Financial Forecasts — ROI by tier, revenue projections, break-even
5. 10 Flags for the Building AI


Amplified Partners — Master Audit & Defriction Estimates — 16 March 2026
Page 2
1. project-latest.md Audit
project-latest.md is a 10,110-line (409KB) Claude Project file dated 17 January 2026. It contains 37
embedded documents from Ewan's early sessions — primarily voice-transcribed thinking sessions,
business bible extraction prompts, Docker orchestration scripts, and early strategy docs.
Redundancy Problem
At least 12 of 37 documents are duplicates. The bible-extraction prompt appears 4 times. Five
documents (19-23) are copied verbatim as documents 24-28. The business vision appears twice.
Roughly 40% of the file is duplicate content — 409KB of file, approximately 250KB unique.
37
embedded docs
12+
duplicates
40%
redundant
25+
missing concepts
Critical Gaps — Missing from project-latest.md
The following exist in the March 2026 specs but are absent or barely mentioned:
Topic
In
project-latest?
Where it actually lives
3-tier architecture (Phone / Full Stack /
Federated)
NO (3 mentions)
PRODUCT-ARCHITECTURE-TIERS.md
7 Operational Rubriks
NO (0 mentions)
PRODUCT-ARCHITECTURE-TIERS.md
3-app design (Customer / Client /
Ewan)
NO (1 mention)
THREE-APPS-DESIGN.md
Screen specs and wireframes
NO
SCREEN-SPECIFICATIONS.md (55KB)
UI component reference
NO
UI-COMPONENT-REFERENCE.md (33KB)
Voice-first interface (detailed)
Partial (11
mentions)
AMPLIFIED_OS_SPEC.md section 6
Staff adoption 3-stage journey
NO
AMPLIFIED_OS_SPEC.md section 7
ESP32 thin client specs
NO (0 mentions)
AMPLIFIED_OS_SPEC.md section 10
Hardware manufacturing (PETG,
costs)
NO
AMPLIFIED_OS_SPEC.md section 11
Pricing tiers (free to 2,995/mo)
NO (0 mentions)
AMPLIFIED_OS_SPEC.md section 3
Life Goals framework
NO (0 mentions)
AMPLIFIED_OS_SPEC.md section 1
FalkorDB / Graphiti
NO (0 mentions)
AMPLIFIED_OS_SPEC.md sections 4, 20
PWA over native decision
NO
AMPLIFIED_OS_SPEC.md section 12
Financial Autopsy MVP (Xero/Sage)
NO
PRODUCT-ARCHITECTURE-TIERS.md
Vertical specialisations
NO
PRODUCT-ARCHITECTURE-TIERS.md
ISO 9001 process documentation
NO (0 mentions)
AMPLIFIED_OS_SPEC.md section 14


Amplified Partners — Master Audit & Defriction Estimates — 16 March 2026
Page 3
Topic
In
project-latest?
Where it actually lives
PDCA nightly improvement cycle
NO
AMPLIFIED_OS_SPEC.md section 15
Libertarian paternalism principle
NO
AMPLIFIED_OS_SPEC.md section 1
Content creation engine
NO
AMPLIFIED_OS_SPEC.md section 17
Four-word identifier system
NO
AMPLIFIED_OS_SPEC.md sections 13, 16
DocBench data extraction engine
NO
AMPLIFIED_OS_SPEC.md section 4
Pre-Cove translator
NO
AMPLIFIED_OS_SPEC.md sections 6, 16
MCPipe / MCP server architecture
NO
PRODUCT-ARCHITECTURE-TIERS.md
Weather-aware scheduling
NO
PRODUCT-ARCHITECTURE-TIERS.md
Amplified Partners name
Barely (1 mention)
All March 2026 docs
Outdated Content
Issue
In project-latest.md
Current reality
Company name
"Covered AI" (31 mentions)
"Amplified Partners" (rebranded)
Database stack
Qdrant (165 mentions) + Neo4j
FalkorDB + Qdrant + PostgreSQL
Infrastructure
Railway deployment
Beast (Hetzner AX162-R)
Tech focus
Kilo Code / extraction
Cove code factory + MCP + agents
Approach
Bible extraction from Mac
Structured vault + process docs


Amplified Partners — Master Audit & Defriction Estimates — 16 March 2026
Page 4
2. Vault Structure Map
Complete catalog of the amplified-vault GitHub repository. This is what the building AI needs to know
about where everything lives.
_inbox (~250 files)
• Python code files (~80+): agents, brain services, CRM, voice integration, webhooks, Telegram gates,
semantic cache
• Strategy/spec docs (~60+): AGENTS v1-v4, SOUL v1-v4, PHILOSOPHY docs, product specs for
HGV/trades
• Session boards (SHARED-BOARD v1-v30): 30 sequential session tracking documents
• Marketing docs: landing page strategies, SEO, LinkedIn posts, content calendars
• Voice platform docs: VAPI vs Retell research, voice CRM specs
• Recent sessions (v1-v31): session summaries
FLAG: Massive version proliferation. Building AI should use the highest version number of each file.
_inbox-voice (~500+ voice transcripts)
• All from 20-23 February 2026
• Raw voice-to-text from Ewan's sessions
• Primary source material for decisions and context
FLAG: These likely contain decisions not written anywhere else. Building AI should ingest and summarise.
_staging (11 subdirectories)
• 01-executive/ — empty
• 02-strategy/ — 8 strategy docs
• 03-sales-marketing/ — 13 marketing docs
• 05-technology/ — 50+ tech docs (the biggest structured collection)
• 07-finance/ — 2 docs (250K automation model)
• 08-product/ — 14 product docs
• 12-archive-raw/ — 200+ docs: Covered AI-era specs, 150+ Perplexity thread exports, build
instructions
FLAG: 12-archive-raw is the archaeological record of every decision made. March 2026 specs take precedence.
research (~140 files)
• Date-prefixed research from late February 2026
• Dave/Sam agent specs, PUDDING extractions, voice AI comparisons
• 60+ four-word-named files (agent session outputs from the Room)
FLAG: Four-word files are agent session results. Need indexing.
work/ (Active docs)
• campaigns/, claude-writing/, pudding/, rubric/, sessions/
• amplified-partners-master.md, Gemini context


Amplified Partners — Master Audit & Defriction Estimates — 16 March 2026
Page 5
3. Defriction Estimates
32 core business processes mapped for a typical 10-person SMB. Estimates based on BCG data (AI cuts
low-value work 25-40%), Gartner forecasts (80% customer issues autonomous by 2029), and UK ONS
hourly cost data.
57
hours saved per week
2,948
hours saved per year
67%
defriction achieved
1.4
FTE freed up
Category A: Complete Defriction (14 processes)
Agent handles end-to-end. Human only for exceptions.
Process
Manual hrs/wk
With agent
Saved/wk
Saved/yr
Invoice Processing
3.0
0.25
2.75
143
Bank Reconciliation
2.0
0.15
1.85
96
Expense Management
1.5
0.10
1.40
73
Payroll Processing
2.0
0.20
1.80
94
VAT/Tax Returns
1.0
0.10
0.90
47
Report Generation
2.0
0.10
1.90
99
Data Entry and Migration
4.0
0.30
3.70
192
Scheduling and Calendar
3.0
0.20
2.80
146
Email Triage and Routing
5.0
0.50
4.50
234
Inventory Tracking
2.0
0.15
1.85
96
Document Filing
2.0
0.10
1.90
99
Compliance Monitoring
1.5
0.15
1.35
70
IT Service Tickets
2.0
0.30
1.70
88
Meeting Notes and Actions
2.0
0.10
1.90
99
SUBTOTAL
33.0
2.7
30.3
1,576
Category B: Partial Defriction (10 processes)
Human leads, agent assists. 40-60% time reduction.
Process
Manual hrs/wk
With agent
Saved/wk
Saved/yr
Sales Conversations
6.0
3.0
3.0
156
Hiring Decisions
2.0
1.0
1.0
52
Client Relationship Mgmt
4.0
2.0
2.0
104
Strategic Planning
2.0
1.2
0.8
42


Amplified Partners — Master Audit & Defriction Estimates — 16 March 2026
Page 6
Process
Manual hrs/wk
With agent
Saved/wk
Saved/yr
Staff Performance Reviews
1.0
0.5
0.5
26
Conflict Resolution
0.5
0.3
0.2
10
Creative Direction
2.0
1.0
1.0
52
Negotiation
1.5
0.8
0.7
36
Quality Judgement Calls
1.5
0.8
0.7
36
Business Development
3.0
1.5
1.5
78
SUBTOTAL
23.5
12.1
11.4
592
Category C: Grey Zone (8 processes)
Transitioning. 50-70% defriction expected within 12 months.
Process
Manual
Now
12mo
Saved now/yr
Saved
12mo/yr
Customer Service T1
8.0
3.0
1.5
260
338
Content Creation
4.0
2.0
1.0
104
156
Social Media Mgmt
3.0
1.5
0.8
78
114
Basic Bookkeeping
3.0
1.0
0.3
104
140
Procurement
2.0
1.2
0.7
42
68
Training/Onboarding
2.0
1.0
0.5
52
78
Marketing Campaigns
3.0
1.5
0.8
78
114
Project Coordination
3.0
1.8
1.0
62
104
SUBTOTAL
28.0
13.0
6.6
780
1,112
Total Defriction Summary
Metric
Now
In 12 months
Total manual hours/week
84.5
84.5
Hours after defriction/week
27.8
21.4
Hours saved/week
56.7
63.1
Hours saved/year
2,948
3,280
Percentage defriction
67%
75%
What that means: a typical 10-person SMB gets 57 hours/week back. That is 1.4 full-time employees'
worth of capacity freed up for higher-value work. Nobody gets sacked. They get time back for customer
relationships, growth, and the things they actually enjoy.


Amplified Partners — Master Audit & Defriction Estimates — 16 March 2026
Page 7
4. Financial Forecasts
Money Saved Per Client (annual)
UK average SMB hourly cost: 22/hr including employer NI, pension, overhead.
Category
Hours saved/yr
Value at 22/hr
Complete defriction (14 processes)
1,576
£34,672
Partial defriction (10 processes)
592
£13,024
Grey zone (8 processes, now)
780
£17,160
TOTAL (now)
2,948
£64,856
TOTAL (12 months)
3,280
£72,160
ROI By Pricing Tier
Tier
Monthly
Annual
Value
ROI
Payback
FREE (3 months)
£0
£0
£16,214
∞
Instant
Solo (£99)
£99
£1,188
£25,942
21.8x
6 days
SB Phone (£295)
£295
£3,540
£38,914
11.0x
10 days
SB IT (£595)
£595
£7,140
£64,856
9.1x
40 days
Medium (£1,595)
£1,595
£19,140
£64,856
3.4x
108 days
Large (£2,995)
£2,995
£35,940
£97,284
2.7x
135 days
Revenue Projections — Conservative (Year 1)
Month
FREE
Solo
SB Phone
SB IT
Medium
Large
MRR
1
20
5
2
1
0
0
£1,685
3
50
15
5
3
1
0
£5,950
6
80
30
12
6
2
1
£14,445
9
100
45
20
10
4
2
£26,265
12
120
60
30
15
6
3
£39,425
Year 1 Conservative: ~39K MRR by month 12 = 473K ARR run rate
Revenue Projections — Moderate (Year 1)
Month
FREE
Solo
SB Phone
SB IT
Medium
Large
MRR
1
40
10
4
2
0
0
£3,370
3
100
30
10
6
2
1
£12,855
6
200
70
25
12
5
2
£30,805


Amplified Partners — Master Audit & Defriction Estimates — 16 March 2026
Page 8
Month
FREE
Solo
SB Phone
SB IT
Medium
Large
MRR
9
300
120
45
20
8
4
£56,420
12
400
180
70
35
12
6
£85,510
Year 1 Moderate: ~85K MRR by month 12 = 1.03M ARR run rate
Revenue Projections — Aggressive (Year 1)
Assumes the Financial Autopsy viral hook works.
Month
FREE
Solo
SB Phone
SB IT
Medium
Large
MRR
3
500
80
30
15
5
2
£31,420
6
1,500
250
80
35
12
5
£78,115
12
5,000
800
250
100
30
15
£237,075
Year 1 Aggressive: ~237K MRR by month 12 = 2.8M ARR run rate
Cost Structure (per client, monthly)
Cost item
Estimate
Beast compute (amortised)
£2-8
LLM API (LiteLLM, Ollama local first)
£3-15
Bluetooth mic (one-time, amortised)
£1-2
Storage and backup (Hetzner)
£0.50-2
Support overhead (amortised)
£5-20
TOTAL PER CLIENT
£11.50-47
At the Solo tier (99/mo), gross margin is 52-88%. At the SB IT tier (595/mo), gross margin is 92-98%.
Break-Even Analysis
Scenario
Monthly costs
Clients needed
Timeline
Ewan only
£3,000
9 paying clients
Month 2-3
+ 1 tech hire
£7,000
20 paying clients
Month 4-6
+ support person
£10,000
29 paying clients
Month 6-9
Full team (5)
£20,000
58 paying clients
Month 9-12
Beast server already paid for. Costs above are people costs.


Amplified Partners — Master Audit & Defriction Estimates — 16 March 2026
Page 9
5. Flags for the Building AI
10 items flagged. No solutions built. The AI that is building can come and have a look.
Flag 1: project-latest.md is outdated
January 2026 snapshot. Still says "Covered AI" 31 times. Missing 25+ concepts from March 2026 specs.
Contains 40% duplicate content. Needs full rebuild with AMPLIFIED_OPERATING_SYSTEM_SPEC.md as
backbone.
Flag 2: The 4 key documents
1) Master doc: AMPLIFIED_OPERATING_SYSTEM_SPEC.md (single source of truth, March 14). 2) Build
JSON: AMPLIFIED_OPERATING_SYSTEM_SPEC.json. 3) Content creation: OS spec sections 17 and 18. 4)
UI refinement: THREE-APPS-DESIGN.md + SCREEN-SPECIFICATIONS.md +
UI-COMPONENT-REFERENCE.md.
Flag 3: Unmined voice transcripts
500+ voice transcripts in _inbox-voice from 20-23 Feb 2026. Almost certainly contain decisions,
preferences, and context not written anywhere else. Building AI should ingest these.
Flag 4: Version proliferation in _inbox
AGENTS has 4 versions. SOUL has 4. SHARED-BOARD has 30. Many files have v2, v3, v4 variants.
Building AI should only use the latest version of each.
Flag 5: _staging/12-archive-raw is a gold mine
200+ documents including Covered AI-era specs, 150+ Perplexity thread exports, build instructions.
Archaeological record of every decision. Index it but treat as historical — March 2026 specs win.
Flag 6: Process coverage larger than 32
32 mapped are core operational. Add industry-specific (gas certs, food safety, HGV compliance),
customer-facing (booking, payment, reviews), and growth (lead gen, content). Total addressable:
80-120 processes per vertical. Map these per vertical.
Flag 7: "We don't sack people" needs system enforcement
Defriction frees 1.4-1.6 FTE per client. System MUST have guardrails: never suggest redundancies,
frame all savings as capacity freed, track what freed time is used for, report on skills development not
headcount reduction.
Flag 8: Financial Autopsy is the viral hook
Xero/Sage API, 5 years of data, CASH-IS-OXYGEN rubrik, generate report. Phase 1 MVP. Door opener.
Minimum viable payload, maximum spread. Prioritise this build.
Flag 9: Pricing psychology
At 595/month delivering 64,856/year value (9.1x ROI), price is almost absurdly cheap. Payback in 40
days. Extremely compelling for sales. Surface ROI numbers in the product.
Flag 10: Kaizen dashboard design principles
Frame data around personal goals (4-day week, time with kids). Language at 14-year-old level.
Structure: Goal, Progress, Next Action. Don't tell people what to feel. Multiple goals per person (3-15).
Time saved as universal currency. Anonymous benchmarks only. No gamification. RAS principle: brains


Amplified Partners — Master Audit & Defriction Estimates — 16 March 2026
Page 10
filter for what matters to THEM.
Attribution
Originator: Ewan Bramley — all business vision, product decisions, vault content, design principles,
pricing. Auditor: Perplexity Computer — vault mapping, gap analysis, defriction estimates, financial
modelling.
Research sources: BCG (AI cuts low-value work 25-40%), Gartner (80% customer issues autonomous by 2029), Lux
Research (automate the boring not the rewarding), ScienceDirect (augmentation vs substitution), UK ONS hourly cost data.



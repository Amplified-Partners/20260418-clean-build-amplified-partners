Status: [NON-AUTHORITATIVE]
Sanitisation: done — no client data, credentials, or PII found in source specifications
Source: Ewan's Mac drop ("New Folder With Items 2.zip", 521 files, 125MB), ingested 2026-04-29

**AMPLIFIED PARTNERS**

Master Architecture & Source of Truth

*The Unified Process, Quality, and Content Engine*

This document governs all building, testing, research, and content
creation at Amplified Partners.

March 2026

www.amplifiedpartners.ai

**CONFIDENTIAL**

**TABLE OF CONTENTS**

**SECTION 1: THE PHILOSOPHY**

This section establishes the foundational thinking that governs every
decision, every line of code, and every piece of content at Amplified
Partners. These are not aspirational statements. They are enforced by
the system itself --- in code, not in policy documents.

**1.1 The Founding Insight**

> *\"No one makes bad decisions on purpose. They make the best call they
> can with the map and numbers they\'ve got. The problem is the map is
> wrong and the numbers don\'t exist.\"*

That single observation is the foundation of everything that follows in
this document. Ewan Bramley spent twenty-five years as a dentist in the
North East of England, running a practice with twenty-five to thirty
staff and approximately two million pounds in annual turnover. He made
every mistake it is possible to make --- hiring the wrong people,
pricing too low, ignoring cash flow until it screamed, trusting the
wrong suppliers, failing to document anything. Running the business from
his gut while the numbers told a story he never read because the numbers
did not exist in any form he could understand.

And here is the thing he knows now that he did not know then: he was not
stupid. He was not lazy. He was not careless. He was making the best
decisions he could with the information available to him. The problem
was that the information was wrong, incomplete, or entirely absent. That
problem affects 5.64 million UK SMEs simultaneously.

The United Kingdom has 5.7 million private sector businesses. Of those,
99.85% are small and medium enterprises. There are 4.27 million sole
traders operating entirely alone. Another 1.37 million are micro
employers with one to nine staff. Construction alone accounts for
870,000 businesses. Collectively, these businesses employ 16.9 million
people --- sixty per cent of all UK private sector employment --- and
generate £2.8 trillion in turnover, half the national total.

And they are drowning. The FSB Small Business Index fell to negative 71
in Q4 2025 --- the lowest since the depths of COVID. For firms employing
one to nine people, the score was negative 85. A record 64% cite
taxation as their top cost pressure. 35% are planning to close or scale
back operations. The costs timebomb from April 2025 --- higher business
rates, energy charges, National Living Wage increases, and Employer NI
contribution rises --- all landed simultaneously. A firm employing nine
staff on the National Living Wage will see its annual employment bill
rise by £25,850, a 12.9% increase.

If the map is wrong, fix the map. If the numbers don\'t exist, create
them. If the business owner cannot see the cliff edge, turn the lights
on. That is what Amplified Partners exists to do. Not eventually. Not
after they can afford a finance director. From day one. A plumber in
Jesmond. A florist in Heaton. A barber in Byker.

**1.2 Privacy-First, Security-First as Architectural Decisions**

Privacy and security at Amplified Partners are not policies bolted onto
the side of the product. They are architectural decisions embedded in
the code. The PII Tokenisation Gateway --- a 353-line wrapper around
Microsoft Presidio --- tokenises personally identifiable information
on-device before any data leaves the device. Names, phone numbers,
addresses, email addresses, and National Insurance numbers are replaced
with tokens before transmission. The mapping between tokens and real
values is stored locally, encrypted, and never transmitted to any
server.

This is not a compliance checkbox. It is a description of how the code
works. The tokenisation happens before the network call. There is no
version of the system where unencrypted PII travels across the internet.
It is simply not possible.

The Beast --- a dedicated Hetzner AX162-R in Falkenstein, Germany ---
was chosen over AWS or Azure for a principled reason. When you host on
AWS, your data is subject to AWS\'s terms of service, which can change.
Your data is subject to the CLOUD Act, which allows US law enforcement
to compel disclosure regardless of where the server is physically
located. On The Beast, our architectural truth is literal truth. The
data is in Germany. The server is ours. The encryption keys are ours. No
third party can access client data without a court order from a
jurisdiction that respects EU data protection law. This is not privacy
by policy. This is privacy by architecture.

**1.3 The Eight Laws**

On 10 March 2026, the Operational Protocol v1 was committed to the
vault. It contained the Eight Laws --- the non-negotiable rules that
govern how Amplified Partners operates. These are not aspirational. They
are enforced by the system.

  --------- ------------------------------------------ --------------------------------------------------------------------------------------------------------
  **Law**   **Rule**                                   **Why It Matters**
  1         If it\'s not in GitHub, it\'s not real     Born from the 7 February wipe. Every decision, document, line of code must be committed.
  2         Document everything                        If it happened and was not documented, it did not happen. Documentation is the product.
  3         Finish or flag --- no silent abandonment   You can decide not to do something. You cannot silently stop doing it without flagging it.
  4         Self-rate every session                    Every work session ends with an honest self-assessment. No inflation allowed.
  5         Learn once, remember forever               The knowledge graph captures everything. No insight is learned twice.
  6         60% internal, 40% external                 Sixty per cent of effort goes to building; forty per cent to telling the story.
  7         Radical attribution on everything          Every fact, framework, borrowed idea is cited. The Radical Attribution Schema (COV-168) enforces this.
  8         Celebrate wins --- the Telegraph Pole      The wins board. Post achievements publicly for the team to see. Morale matters.
  --------- ------------------------------------------ --------------------------------------------------------------------------------------------------------

**1.4 The Ulysses Clause**

Named after the Greek hero who had himself tied to the mast so he could
hear the Sirens without being destroyed by them, the Ulysses Clause was
formalised on 28 February 2026. It establishes that the system is loyal
to its mission, not to any individual --- including the founder.

The Founders Loss Under Immutable Code document (28 February 2026) made
this explicit: even the founder is subject to the Immutable Foundation
Code. If the system detects that a commitment has been broken, it flags
it regardless of who broke it. If the founder asks the AI to downplay a
problem, the AI refuses. Anti-sycophancy rules were established:
\'Don\'t let me be wrong without saying something.\' The AI was
explicitly instructed to challenge the founder, to flag when commitments
were being dodged, and to refuse to pretend everything was fine when it
was not.

> *\"AI that won\'t let us lie to you.\"*

This became the most powerful product differentiator in the entire
build. The AI enforces accountability immutably --- not because a
consultant is watching, but because the system literally cannot be
overridden once a commitment is made.

**1.5 Libertarian Paternalism**

The AI optimises the route to the client\'s chosen destination but never
chooses the destination. It will not override your goals. But it will
not let you lie to yourself about whether you are reaching them.

Every business owner who uses Amplified Partners is asked about their
life goals as part of onboarding --- not business goals, life goals.
Because the purpose of a business is to serve the life of the person who
runs it, not the other way around. Every recommendation the system makes
is evaluated against whether it moves the owner closer to their stated
life goals.

The AI Board --- inspired by Ray Dalio\'s approach to decision-making at
Bridgewater --- uses five different models with believability weighting
to make recommendations. No single model dominates. Disagreements
between models are surfaced, not hidden. The business owner sees the
range of perspectives, not a single answer.

**1.6 Document, Don\'t Create**

The content philosophy follows GaryVee\'s principle adapted for
build-in-public: the story of the build is the content. The content
builds the audience. The audience becomes the waitlist. The waitlist
becomes the customer base. Every architecture decision, every failure,
every breakthrough is potential content. The supply of raw material is
limitless because the work never stops.

This means Amplified Partners does not have a separate marketing
function. The build process itself generates content. Every research
output is also a content atom. Every testing methodology is also a
thought leadership piece. The document you are reading is both an
internal governance document and the source material for months of
external content.

The competitive advantage is structural: content that documents real
work is inherently more authentic than content created for marketing
purposes. Build-in-public founders who share transparently grow
audiences 3x faster and see a 20--30% increase in trust metrics.

**1.7 The Wipe --- How Catastrophe Created Culture**

On 7 February 2026, the entire codebase was lost. No git backups. No
remote copies. No version control discipline. Only the database
survived. Weeks of work --- the CRM foundations, the agent architecture,
the voice system prototypes, the knowledge graph experiments --- gone.
Not corrupted. Not recoverable. Gone.

The session notes from 11 February reference it directly: \'Lost entire
codebase 7 Feb. No git, no backups. Only database survived.\' Those
twelve words represent one of the worst days of the entire build. The
psychological impact was devastating --- not just the loss of code, but
the loss of trust in the process. Building at extraordinary speed
without the discipline to protect what was being built.

Two things happened immediately. First, the byker-production repository
was created --- recovery infrastructure. Second, the FINAL
amplified-partners build spec was written as a recovery anchor,
capturing everything that could be remembered about what had existed.
The Orchestration Ground Truth document followed the next day --- the
coordination document governing how all agents, systems, and processes
would communicate going forward.

In the nine days that followed, the entire system was rebuilt from
scratch --- and rebuilt better. By 16 February 2026, the following was
code-complete:

  ------------------------------------------- ------------------- ------------------------------------------
  **System**                                  **Lines of Code**   **Status**
  Telephone Receptionist AI (Dave\'s Agent)   805 lines           Complete --- Telnyx + Retell integration
  Stripe Payment System                       799 lines           Production-ready
  50 Landing Pages                            58 pages            Built and deployed
  Voice-to-Content Service                    1,086 lines         Docker running
  Business Brain System                       600+ line schema    Complete intelligence layer
  PII Tokenisation Gateway                    353 lines           Microsoft Presidio
  Intelligence System                         2,370+ lines        20,000+ words research, 100+ sources
  ------------------------------------------- ------------------- ------------------------------------------

The gap between code-complete and live was not technical. It was sixty
minutes of administrative configuration: buy a UK phone number from
Telnyx (£2/month, ten minutes), configure the Stripe dashboard
(forty-five minutes), deploy to Netlify (five minutes). The wipe forced
a discipline that speed alone would never have produced.

**1.8 Core Philosophical Positions**

-   **Never replace staff --- only free them from friction.** The system
    is explicitly designed to augment, not automate. No job is
    eliminated. Friction is eliminated. The difference matters
    enormously to every business owner told that AI is coming for their
    people.

-   **No HR involvement.** Staff data is absolutely private. The
    business sees aggregate patterns (\'Your team\'s wellbeing score has
    dropped 12%\'), not individual responses.

-   **Win-win only.** The system will not recommend actions that benefit
    the business at the expense of staff, customers, or suppliers.

-   **The Partnership Model.** The word \'Partners\' is not accidental.
    AI is a partner, not a tool. A tool does what you tell it. A partner
    challenges you, supports you, holds you accountable. A tool competes
    on features. A partner competes on trust.

-   **\"You with AI = Amplified.\"** The free tier exists not as a loss
    leader but as an invitation to experience the partnership before
    committing. At every tier, the relationship is the product.

**SECTION 2: THE ARCHITECTURE**

The architecture of Amplified Partners is not an implementation detail
--- it is the product. Every choice about where data lives, how it
flows, who can access it, and what happens when something goes wrong is
a product decision that directly affects the business owners who use it.
This chapter is technical, but it is written for anyone to understand.

**2.1 The Beast**

The primary compute infrastructure is a dedicated server called The
Beast. It is a Hetzner AX162-R located in Falkenstein, Germany ---
European Union jurisdiction, which matters enormously for data
protection.

  ------------------- -------------------------------------
  **Specification**   **Detail**
  Processor           48-core AMD EPYC
  Memory              256GB RAM
  Network             10Gbit connection
  Location            Falkenstein, Germany (EU)
  Jurisdiction        EU GDPR by geography, not by policy
  Containers          29 Docker containers in production
  Monthly Cost        \~€230--280/month (fixed)
  IP Address          135.181.161.131
  ------------------- -------------------------------------

The decision not to use AWS or Azure was deliberate and principled. When
you host on AWS, your data is subject to AWS\'s terms of service, which
can change. Your data is subject to the CLOUD Act, which allows US law
enforcement to compel disclosure regardless of where the server is
physically located. Your architectural truth --- what you tell customers
about their data --- is contingent on a third party\'s policy decisions.

On The Beast, our architectural truth is literal truth. The data is in
Germany. The server is ours. The encryption keys are ours. No third
party can access client data without a court order from a jurisdiction
that respects EU data protection law.

The Beast runs 29 Docker containers in production: FalkorDB for the
knowledge graph, PostgreSQL for structured client data, Redis for
session caching, Ollama for real-time LLM inference (CPU-based, running
qwen3-coder:30b and llama3.1:8b), Traefik as the reverse proxy, SearXNG
for search, and 22 additional service containers handling the full
production stack.

**2.2 FalkorDB: The Graph Decision**

On 11 March 2026, the final database architecture decision was made.
FalkorDB, combined with Graphiti, replaced the previous Neo4j and Qdrant
combination. This was a significant simplification --- and the decision
was documented in real-time as it happened, at nine minutes to one in
the morning.

The evolution tells the story of architectural maturity:

-   January 2026: Obsidian for markdown documents, Neo4j for graph
    relationships, Qdrant for vector search --- three separate systems

-   February 2026: Neo4j replaced by Soviet-maths-inspired optimisation,
    Qdrant retained

-   March 2026: FalkorDB + Graphiti replaces everything --- one engine,
    one container, one failure mode

**Why FalkorDB Won:**

-   Graph queries and vector search in a single engine using the same
    HNSW (Hierarchical Navigable Small World) algorithm that Qdrant uses

-   Combined graph+vector in one Cypher query at sub-10 millisecond
    latency

-   Multi-tenancy support: 10,000 or more isolated graphs per instance
    --- each client gets their own graph, with architectural isolation
    not just access-control isolation

-   Graphiti adds a temporal layer to every fact: valid\_at and
    invalid\_at timestamps mean the system knows not just what is true,
    but when something became true and when it stopped being true

-   One container instead of two. One failure mode instead of two.
    Simplified deployment, monitoring, and backup.

As of March 2026, the knowledge graph contains 4.5 million words indexed
via Graphiti, with 330 Claude conversations totalling approximately 1.8
million words of dialogue.

**2.3 Three-Layer Data Sovereignty**

The data sovereignty model ensures that privacy is maintained
architecturally at every level:

**Layer 1 --- Per-Client Container**

Every business gets its own isolated graph, its own data store, its own
encryption. No shared tables. No shared indexes. One business cannot
accidentally or intentionally access another\'s data. This is not
access-control-level isolation --- it is architectural isolation. The
data physically cannot be mixed.

**Layer 2 --- Central Catalogue (Metadata Only)**

The system knows that a plumber exists and that they have twelve
employees and that their data was last updated on Tuesday. It does not
know what their revenue is or what their staff said in interviews.
Metadata for routing and system management only. This layer enables the
system to function as a platform without compromising individual client
privacy.

**Layer 3 --- Anonymised Aggregation (The PUDDING Factory)**

Cross-client patterns are discovered using fully anonymised, aggregated
data. \'Businesses in the North East construction sector with 5--10
employees tend to experience cash flow pressure in Q1\' is a pattern. No
individual business is identifiable. This is the PUDDING Factory --- the
anonymised layer where cross-domain discoveries happen, creating network
effects that benefit every user as the platform grows.

**2.4 DocBench --- 99.53% Extraction Accuracy**

DocBench is the data extraction engine for client onboarding. It
achieves 99.53% extraction accuracy using an 8-billion-parameter model
that runs locally on The Beast. No documents leave the server. No client
invoices, receipts, or contracts are sent to a third-party API for
processing.

The extraction pipeline processes emails, invoices, CRM exports, phone
recordings, standard operating procedures, and handwritten notes ---
converting the shoebox of receipts and WhatsApp threads that most SMBs
use as their financial record system into structured, queryable data in
the Business Brain.

**2.5 PII Tokenisation --- Microsoft Presidio**

The PII Tokenisation Gateway is a 353-line wrapper around Microsoft
Presidio. It tokenises personally identifiable information on-device
before data leaves the device. Names, phone numbers, addresses, email
addresses, and National Insurance numbers are replaced with tokens
before transmission. The mapping between tokens and real values is
stored locally, encrypted, and never transmitted to any server.

When we tell a business owner that their staff\'s private interview
responses never leave their device in identifiable form, it is not a
policy statement --- it is a description of how the code works.

**2.6 Pre-Cove Translator**

The Pre-Cove translator handles accent and speech sanitisation.
Newcastle dialect, chaotic speech patterns, strong regional accents, and
the general messiness of real human speech captured by a Bluetooth
microphone in a van travelling at sixty miles per hour --- all of this
needs to be cleaned before it hits the AI for processing.

The Pre-Cove layer is mandatory on all voice input. It is not optional
and cannot be bypassed. It ensures that every business owner, regardless
of accent or speech pattern, gets the same quality of transcription and
therefore the same quality of insight. A plumber in Byker gets the same
fidelity as a solicitor in Jesmond.

**2.7 The Operating System Specification**

On 14 March 2026, AMPLIFIED\_OPERATING\_SYSTEM\_SPEC.md was committed
--- 688 lines covering twenty-three sections, from philosophy and
principles through to hardware manufacturing and marketing. On 15 March,
the AI-readable JSON version was committed --- the specification
translated into machine-parseable format so that agents could consume it
directly. This signals maturity: the spec is written for both human
reading and AI agent consumption.

  ------------------- -----------------------------------------------------------------------------------
  **Section Range**   **Coverage**
  1--3                Philosophy, What Amplified Is, Pricing & Tiers (£0 to £2,995/month)
  4--5                Unified Business Brain (FalkorDB + Qdrant + SQL three-layer), Data Architecture
  6--8                Voice-First Interface (PRIMARY), Staff Adoption Journey (3-stage), Device Options
  9--11               Hardware: Bluetooth Microphones, ESP32 Thin Client, Manufacturing & Enclosures
  12--14              Phone App (PWA), Onboarding & Interviews, ISO 9001 Process Documentation
  15--17              Federated Model, Privacy/GDPR/Tokenisation, Content Creation Engine
  18--23              Marketing Philosophy, Product Interfaces, Infrastructure, Kaizen, Decisions Log
  ------------------- -----------------------------------------------------------------------------------

**2.8 Product Tiers**

The commercial model reflects the partnership philosophy: the free tier
exists as an invitation, not a loss leader.

  ---------- -------------------- --------------------------- ---------------------------------------------------------------------------
  **Tier**   **Price**            **Audience**                **Capability**
  Tier 1     £0/month             Solo / micro businesses     Phone-only, voice-first interface --- the lights turned on
  Tier 2     \~£300/month         SMBs with 5--25 employees   Full stack: dashboard + voice + WhatsApp + staff interviews
  Tier 3     Up to £2,995/month   Complex operations          Federated intelligence, custom config, anonymised cross-vertical insights
  ---------- -------------------- --------------------------- ---------------------------------------------------------------------------

At every tier, the relationship is the product. The mid-tier provides
the full operating system. The top tier provides dedicated support,
custom configuration, and the full federated intelligence layer. The
upgrade trigger is workflow-based, not arbitrary --- the paid tier
unlocks something they hit naturally as they grow.

**2.9 Voice-First Interface Design**

Perhaps the single most important product decision in the entire
operating system specification: voice is the primary interface. Not a
dashboard. Not a mobile app. Not a web portal. Voice.

The reasoning is rooted in the audience. A plumber does not sit at a
desk. A baker does not have clean, dry hands at seven in the morning. A
builder does not pull out a laptop on a scaffolding platform. But every
single one of them can talk. They talk in the van. They talk on the way
to a job. They talk while their hands are covered in flour, or cement,
or engine oil. Voice is the only interface that works for every single
potential user in every single context where they actually operate.

Device options: a Bluetooth clip-on microphone (sent free to staff
during onboarding), paired with their existing phone. No new hardware to
buy. No app to install. Just clip the microphone to your collar and
talk. The system listens, transcribes via the Pre-Cove translator,
processes, and responds.

The staff adoption journey was designed in three deliberate stages:

1.  Stage 1: A shared device in the office that anyone can walk up to
    and speak to --- minimal commitment, maximum accessibility.

2.  Stage 2: Voluntary adoption on personal phones for staff who see the
    value --- the system earns its place.

3.  Stage 3: Power users who use the system throughout their day ---
    deep integration into daily workflow.

No coercion. No mandatory adoption. The system earns its place by being
useful, not by being imposed. The ESP32 thin client --- a tiny,
inexpensive microcontroller --- was specified as a future hardware
option: a dedicated device that does nothing except listen and respond,
with no screen, no complexity, and a cost low enough to give one to
every staff member. Voice first, screen second, keyboard never.

**2.10 The Vault --- 5,081 Files of Knowledge**

On 11 March 2026, at six minutes past midnight, the amplified-partners
repository was created --- the master consolidation. The initial commit
contained the agent stack, infrastructure files, build scripts, and
deployment guides. At 00:26, the big merge happened: 5,081 files from
the old amplified-vault combined with the new vault.

  ----------------------------- ----------- ---------------------------------------------------------------
  **Category**                  **Files**   **Description**
  Monologue transcripts         2,214       Voice-to-text capture from the marathon sessions (20--21 Feb)
  Voice captures                888         Raw audio files from Bluetooth microphone sessions
  Principles library            57          Dalio, Gerber, Godin, Ziglar, Lund, Kennedy frameworks
  Covered AI work               168         Sessions, bibles, research from the original product
  Imported business docs        122         CRM, OpenClaw, Gemini exports
  Research                      168         Technical and business research documents
  Inbox raw                     366         Unprocessed captures awaiting classification
  Staging archive               509         Processed and categorised documents
  Infrastructure research       30          Server, deployment, DevOps research
  Projects                      13          Active project files
  Scripts                       10          Automation scripts
  Claude/Gemini conversations   523         Across 14 categories
  ----------------------------- ----------- ---------------------------------------------------------------

Behind these files: 330 Claude conversations totalling approximately 1.8
million words. 4.5 million words indexed via Graphiti on FalkorDB. 58
Gemini backup files. Nine commits in one night --- from midnight to one
in the morning --- consolidating four months of work into a single
source of truth.

The voice capture marathon of 20--21 February 2026 deserves specific
mention: over 800 voice note files captured from 04:36 AM on the 20th
through to 21:10 on the 21st. Some sessions ran for six continuous
hours. This was the raw material for the content engine --- every
business insight, every architectural decision, every philosophical
position captured in Ewan\'s own voice and transcribed into the system.

**2.11 The Business Brain**

The Business Brain is the unified intelligence layer combining interview
insights, business data, and AI reasoning. Built during the February
sprint, it contains a 600+ line schema covering six core objects:

-   FounderProfile --- the owner\'s background, goals, risk tolerance,
    and life objectives

-   StaffMember --- individual staff data (private to the AI and the
    individual)

-   BusinessState --- current financial and operational metrics

-   FrictionPoint --- identified areas of waste, delay, or frustration

-   WowOpportunity --- potential improvements that would delight
    customers or staff

-   Recommendation --- AI-generated suggestions with confidence
    intervals and source citations

Embedded within the Business Brain are several analytical engines:

-   **Death Spiral Detector:** Built on the Altman Z-Score (80--90%
    accuracy for predicting business distress), Cash Conversion Cycle
    analysis, Margin Erosion tracking, and Customer Concentration Risk
    assessment.

-   **Bottleneck Finder:** Based on Eliyahu Goldratt\'s Theory of
    Constraints --- identifies the single step in any process with the
    lowest throughput.

-   **Recommendation Engine:** The Rule of Three --- every
    recommendation comes with exactly three options: conservative,
    moderate, and aggressive, each with projected outcomes.

**SECTION 3: THE PROCESS FRAMEWORKS**

Process idealisation --- the discipline of making every process as close
to optimal as possible while building in continuous improvement ---
draws from six classical frameworks and a rapidly expanding frontier of
AI-native approaches. No single methodology is sufficient. The optimal
approach integrates classical rigour with AI-native speed. This section
maps how those frameworks integrate with the Amplified Partners
proprietary scoring and improvement systems.

**3.1 AMPS --- Amplified Process Maturity Score**

AMPS is the proprietary 0--10 scoring system that measures how mature,
documented, and optimised a business process is. It provides a single
number that business owners can understand immediately, while encoding
granular detail for the AI system to act on.

  ----------- ------------ ------------------------------------------------------------------------------------------------------------
  **Score**   **Level**    **Description**
  0--1        Chaotic      No documented process. Outcomes depend entirely on individual heroics. Knowledge lives in people\'s heads.
  2--3        Reactive     Process exists informally. Documentation is partial. Fire-fighting dominates. Some repeatability.
  4--5        Defined      Process is documented and repeatable. Quality is inconsistent but measurable. Standards exist.
  6--7        Managed      Process is measured quantitatively. Variation is controlled. Outcomes are predictable within bounds.
  8--9        Optimising   Continuous improvement is systematic. Process adapts based on data. Waste is actively eliminated.
  10          Idealised    Process approaches theoretical optimum. Improvement is automated and self-correcting.
  ----------- ------------ ------------------------------------------------------------------------------------------------------------

**3.2 AMPS Mapped to CMMI Maturity Levels**

The AMPS scale maps directly to the Capability Maturity Model
Integration (CMMI) framework, providing external credibility and
benchmark comparability:

  ---------------- ---------------- ------------------------ -----------------------------------------------------------------
  **AMPS Range**   **CMMI Level**   **CMMI Name**            **Key Characteristics**
  0--1             Level 1          Initial                  Processes unpredictable, poorly controlled, reactive
  2--3             Level 2          Managed                  Processes planned and executed per policy, reactive improvement
  4--5             Level 3          Defined                  Processes characterised, understood, proactive standards
  6--7             Level 4          Quantitatively Managed   Processes measured and controlled via statistical methods
  8--10            Level 5          Optimising               Focus on continuous improvement through innovation
  ---------------- ---------------- ------------------------ -----------------------------------------------------------------

**3.3 The Build Quality Framework --- Six-Stage Pipeline**

Every piece of work at Amplified Partners passes through a six-stage
quality pipeline:

4.  CAPTURE --- Raw input (voice note, code commit, research finding,
    decision) is captured in its original form.

5.  CLASSIFY --- The Gatekeeper Agent classifies the input using the
    vault taxonomy system, applying WHAT/HOW/SCALE/TIME labels.

6.  VALIDATE --- Quality checks are applied. Does it contradict existing
    knowledge? Is it properly attributed? Does it meet COV-168?

7.  INTEGRATE --- The validated input is integrated into the knowledge
    graph via Graphiti, with temporal metadata (valid\_at timestamp).

8.  SCORE --- The affected processes are re-scored against the AMPS
    framework. Any change in maturity is logged.

9.  IMPROVE --- The Kaizen department reviews all score changes and
    identifies improvement opportunities.

This pipeline runs continuously. Every voice note captured in a van,
every commit pushed to GitHub, every research finding integrated into
the vault passes through these six stages. The quality is systemic, not
dependent on any individual remembering to check their work.

**3.4 The Kaizen Department\'s Role**

The Kaizen department is one of four organisational departments at
Amplified Partners (alongside R&D, Chaos, and Real). Its role is
continuous improvement: reviewing every process score change,
identifying patterns in process degradation, and proposing systematic
improvements.

Kaizen operates on the Toyota Production System principle: improvement
is not a project with an end date; it is a permanent cultural
commitment. The department\'s outputs feed directly into the PUDDING
Factory, where cross-domain patterns in process improvement are
discovered.

Concretely, the Kaizen department maintains: the AMPS scoring rubrics,
the quality gate criteria for the six-stage pipeline, the improvement
backlog (prioritised by AMPS score delta potential), the cross-client
anonymised improvement pattern library, and the monthly Kaizen review
report.

**3.5 PDCA Integration with Sprint Cycles**

The Plan-Do-Check-Act (Deming) cycle maps directly onto sprint cadence:

  ---------------- ------------------------------------------------------------ ----------------------------------------------
  **PDCA Phase**   **Sprint Activity**                                          **Output**
  Plan             Monday: Define sprint objectives, identify process targets   Sprint plan with AMPS targets
  Do               Tues--Thurs: Build, test, implement changes                  Code commits, documentation, test results
  Check            Friday: Review outcomes against AMPS targets                 Score delta report, variance analysis
  Act              Friday PM: Kaizen review, adjust standards                   Updated process documentation, new baselines
  ---------------- ------------------------------------------------------------ ----------------------------------------------

Each sprint cycle produces measurable AMPS improvements. Over time, the
cumulative effect of weekly PDCA cycles drives processes from Chaotic
(0--1) toward Managed (6--7) at a predictable rate. The system tracks
this progression for every client process, providing a visual
representation of improvement over time.

**3.6 Six Sigma DMAIC for Process Improvement**

For processes requiring deep intervention (AMPS score below 4, or
persistent variance), the DMAIC framework provides structured
methodology:

-   **Define:** Identify the specific process, its boundaries, and the
    problem statement using data from the knowledge graph.

-   **Measure:** Collect quantitative data on current performance using
    AMPS scoring and supplementary metrics.

-   **Analyse:** Use the Business Brain\'s analytical capabilities to
    identify root causes, leveraging Goldratt\'s Theory of Constraints
    for bottleneck identification.

-   **Improve:** Design and implement improvements, with the AI Board
    providing multi-model recommendations weighted by believability.

-   **Control:** Establish ongoing monitoring through automated AMPS
    scoring, with the Kaizen department maintaining oversight.

**3.7 Theory of Constraints for Bottleneck Identification**

Eliyahu Goldratt\'s Theory of Constraints (TOC) is implemented directly
in the Business Brain\'s Bottleneck Finder. The five focusing steps are
automated:

10. IDENTIFY the constraint --- the Business Brain analyses process flow
    data to find the step with the lowest throughput.

11. EXPLOIT the constraint --- maximise the output of the bottleneck
    step without additional investment.

12. SUBORDINATE everything else --- align all other processes to the
    pace of the constraint.

13. ELEVATE the constraint --- invest in expanding the capacity of the
    bottleneck.

14. REPEAT --- once the constraint moves, identify the new bottleneck
    and start again.

This is not theoretical. The Death Spiral Detector uses the Altman
Z-Score (80--90% accuracy for predicting business distress), Cash
Conversion Cycle analysis, Margin Erosion tracking, and Customer
Concentration Risk assessment --- all integrated with TOC analysis to
provide early warning of business distress.

**3.8 V-Model for Validation**

The V-Model ensures that every level of specification has a
corresponding level of testing:

  ------------------------- ------------------------------ -------------------------------------------------------
  **Specification Level**   **Corresponding Validation**   **Amplified Partners Application**
  Business Requirements     Acceptance Testing             Does the system solve the SMB\'s actual problem?
  System Architecture       Integration Testing            Do FalkorDB, Ollama, and the API layer work together?
  Detailed Design           Component Testing              Does each module perform its specified function?
  Implementation            Unit Testing                   Does each function return correct results?
  ------------------------- ------------------------------ -------------------------------------------------------

**3.9 The PUDDING Technique**

PUDDING --- named after the British culinary tradition and Robert
Burns\' famous line about the haggis: \'Great chieftain o\' the
pudding-race!\' --- is Amplified Partners\' proprietary cross-domain
knowledge discovery technique. It adapts Don Swanson\'s 1986
Literature-Based Discovery (ABC model) for business knowledge.

**The Swanson ABC Model:**

In 1986, physicist Don Swanson proposed that if concept A is related to
concept B in one body of literature, and concept B is related to concept
C in a completely different body of literature, then there may be a
previously undiscovered relationship between A and C. Swanson used this
to discover that dietary fish oil (A) was connected to blood viscosity
(B) in nutrition journals, and blood viscosity (B) was connected to
Raynaud\'s disease (C) in medical journals --- predicting that fish oil
could help Raynaud\'s disease, which was later confirmed experimentally.

**Adaptation for Business Knowledge:**

Amplified Partners adapts this for business: if a restaurant\'s staff
scheduling system (A) shares structural properties with a logistics
routing algorithm (B), and that routing algorithm (B) shares properties
with a plumber\'s job-sequencing problem (C), then insights from
restaurant scheduling might directly solve a plumber\'s operational
bottleneck --- a connection that no one would make without the
cross-domain mapping.

**The Seven-Step Process:**

15. Capture raw knowledge from multiple business domains

16. Apply neutral taxonomy labels (WHAT/HOW/SCALE/TIME) creating 2,401
    possible label combinations

17. Score cross-domain connections using mashup formula: (Shared
    Dimensions × 2) + Unique\_A + Unique\_B

18. Identify non-obvious connections between unrelated domains

19. Validate discoveries through the Room Protocol (Sam researches, Ewan
    judges, Claude formalises)

20. Integrate validated discoveries into the knowledge graph with
    temporal metadata

21. Distribute insights to affected client processes via automated
    recommendations

Testing showed a 41.67% improvement in retrieval accuracy when combining
RAG with the Swanson ABC model. PUDDING MIX 001 (10 March 2026) produced
6 cross-domain discoveries with a highest score of 19 (COV-166). PUDDING
MIX 002 --- Biological Decision Logic --- produced 7 discoveries with a
record score of 23 (COV-167), exploring slime mould, bacterial quorum,
octopus, mycelial, immune system, and ant colony logics applied to SMB
routing and decision architecture.

**3.10 Cross-Domain Process Discovery**

The PUDDING Factory operates on the anonymised aggregation layer (Layer
3 of the data sovereignty model). It discovers patterns that no
individual business could see:

-   Construction companies with 5--10 employees share cash flow
    seasonality patterns with independent restaurants --- both
    experience predictable Q1 pressure

-   Hairdresser appointment scheduling optimisation maps structurally to
    dental practice capacity management --- same constraints, different
    domain language

-   Plumber job-routing algorithms share structural properties with
    logistics fleet optimisation --- the maths is identical

-   Bakery inventory management shares wastage patterns with florist
    stock management --- perishable goods, similar shelf life dynamics

Each discovery is scored, validated, and --- if confirmed ---
distributed to all clients whose processes could benefit. This creates a
network effect: the more businesses use the system, the more
cross-domain patterns emerge, and the more valuable the system becomes
for every user.

**3.11 Biomimicry in Process Design**

Nature\'s Logic Systems were explored as models for how the multi-agent
system and process improvement engine should coordinate:

-   **Slime mould optimisation:** Physarum polycephalum finds optimal
    network paths without central coordination --- applied to client
    process flow optimisation.

-   **Ant colony logic:** Pheromone-based communication creates emergent
    optimal routing --- applied to job scheduling and task
    prioritisation.

-   **Bacterial quorum sensing:** Bacteria coordinate collective
    behaviour based on population density signals --- applied to scaling
    decisions.

-   **Octopus distributed intelligence:** Each arm has independent
    processing capability --- applied to the multi-agent architecture
    where each agent operates independently.

-   **Mycelial networks:** Underground fungal networks distribute
    resources across a forest --- applied to cross-client resource
    sharing.

-   **Immune system logic:** Pattern recognition, memory, and adaptive
    response --- applied to the chaos testing framework.

**3.12 TRIZ: Ideal Final Result**

TRIZ\'s concept of the Ideal Final Result (IFR) is applied to process
idealisation: the ideal process performs its function perfectly with
zero cost, zero waste, and zero complexity. While no real process
achieves IFR, defining it creates a north star that prevents settling
for \'good enough.\' Every AMPS score of 10 represents a process that
approaches its domain-specific IFR.

**SECTION 4: THE TESTING METHODOLOGY**

Testing AI systems is fundamentally different from testing conventional
software. Behaviour is probabilistic, emergent, and dependent on data
that changes over time. According to research on model drift, 91% of ML
models suffer from some form of drift --- meaning the scale problem for
AI is not just load, but data distribution shift. At small user counts,
failures are observable manually. At scale, failures become statistical,
silent, and compound. This section defines the comprehensive testing
methodology.

**4.1 The Five-Layer AI Testing Pyramid**

The testing pyramid adapted for AI systems inverts some traditional
assumptions --- AI systems require proportionally more integration and
end-to-end testing:

  ---------------------- ------------------------------------------------------------------------- ---------------------------------------------------- ---------------
  **Layer**              **What It Tests**                                                         **Tools / Approach**                                 **Frequency**
  Layer 1: Unit          Individual functions, data transformations, prompt templates              pytest, property-based testing (Hypothesis)          Every commit
  Layer 2: Component     Individual services (FalkorDB queries, Ollama inference, API endpoints)   Docker-based integration tests, contract testing     Every PR
  Layer 3: Integration   Service-to-service communication, data flow between containers            End-to-end test suites with mock external services   Daily
  Layer 4: System        Full pipeline --- voice input → processing → response                     Staging environment with synthetic clients           Weekly
  Layer 5: Chaos         System behaviour under failure, adversarial inputs, edge cases            GameDay exercises, automated fault injection         Fortnightly
  ---------------------- ------------------------------------------------------------------------- ---------------------------------------------------- ---------------

**4.2 Testing at Different Scales**

The progression of failure modes changes dramatically as the user base
grows. Each tier introduces qualitatively different failure classes:

  --------------- -------------------------------------------------------------------------------------- ---------------------------------------------------------- -----------------------------------
  **User Tier**   **Primary Failure Modes**                                                              **Detection Method**                                       **Priority**
  1--10           Functional bugs, integration failures, prompt instability, obvious hallucinations      Manual inspection, unit tests, prompt regression tests     Fix before moving on
  10--100         Latency under parallel requests, memory leaks, model drift, edge-case accumulation     Automated monitoring, load testing, statistical sampling   Performance baselines required
  100--1K         Data isolation failures, cross-tenant leakage, cache poisoning, PII exposure           Security testing, penetration testing, compliance audits   Architecture validation critical
  1K--10K         Statistical failures, recommendation bias, model degradation, false PUDDING patterns   Statistical monitoring, A/B testing, bias detection        Full observability infrastructure
  --------------- -------------------------------------------------------------------------------------- ---------------------------------------------------------- -----------------------------------

**4.3 Chaos Engineering Approach --- Four Departments**

Chaos engineering at Amplified Partners is not a single activity --- it
is an organisational commitment distributed across the four-department
structure:

  ---------------- ----------------------------------------------- -------------------------------------------------------------------------------------------------------
  **Department**   **Role in Testing**                             **Key Activities**
  Kaizen           Continuous improvement of test processes        Review test coverage gaps, improve efficiency, maintain test documentation, track test debt
  R&D              Develop new testing approaches and tooling      Build custom frameworks, evaluate new tools, prototype automation, research testing methodologies
  Chaos            Active fault injection and resilience testing   GameDay exercises, failure simulation, adversarial input testing, performance degradation experiments
  Real             Production monitoring and incident response     Live observation, performance tracking, incident post-mortems, on-call rotation
  ---------------- ----------------------------------------------- -------------------------------------------------------------------------------------------------------

**4.4 FalkorDB-Specific Chaos Experiments**

The knowledge graph is the most critical component. If it fails, the
Business Brain fails, recommendations stop, and the Death Spiral
Detector goes blind. FalkorDB-specific chaos experiments:

22. Graph corruption injection: Deliberately introduce contradictory
    facts and verify the system detects and quarantines them via
    Graphiti\'s temporal validation layer.

23. Temporal consistency attack: Insert facts with invalid temporal
    metadata (e.g., valid\_at after invalid\_at) and verify the Graphiti
    layer rejects them cleanly.

24. Cross-tenant boundary test: Attempt to query one client\'s graph
    from another client\'s context --- must fail absolutely, with zero
    data leakage.

25. Volume stress test: Load 10,000+ simultaneous graph queries to
    verify sub-10ms latency holds under pressure across all isolated
    graphs.

26. Network partition simulation: Sever the connection between FalkorDB
    and the API layer and verify graceful degradation --- the system
    must continue serving cached data.

27. Cold start recovery: Kill the FalkorDB container without warning and
    verify full recovery with zero data loss from persistent storage.

28. Concurrent write storm: Simulate 100 clients all updating their
    graphs simultaneously and verify no cross-contamination or data
    corruption.

29. Memory exhaustion: Gradually increase graph complexity until memory
    pressure triggers and verify the system sheds load gracefully rather
    than crashing.

**4.5 Debug-First Build Philosophy --- Chaos-Driven Development**

Chaos-Driven Development (CDD) inverts the traditional relationship
between building and testing. Instead of building first and testing
after, CDD defines the failure modes first and builds the system to
survive them.

The CDD workflow:

30. Define the failure scenario (e.g., \'What happens when the LLM
    returns a hallucinated financial figure?\')

31. Write the chaos test that simulates this failure --- this test
    defines what \'correct behaviour under failure\' looks like.

32. Run the test against the current system --- it should fail (the
    system doesn\'t handle this yet).

33. Build the resilience mechanism (e.g., fact-checking against the
    knowledge graph, confidence thresholds, source citation
    requirements).

34. Run the chaos test again --- it should pass.

35. Add the test to the permanent regression suite --- it runs on every
    build forever.

CDD is particularly valuable for AI systems where failure modes are
often discovered in production. It forces the team to imagine failures
before they occur. The intellectual heritage: Netflix\'s Chaos Monkey
(2011) pioneered automated fault injection; Amazon\'s GameDays
formalised planned failure exercises; Google\'s DiRT (Disaster Recovery
Testing) tested at planet scale. CDD adapts these for an AI-first,
knowledge-graph-centric architecture.

**4.6 Property-Based Testing for AI Outputs**

Traditional unit tests verify specific inputs produce specific outputs.
Property-based testing verifies that outputs satisfy certain properties
regardless of input. For AI systems, this is essential because the
output space is too large for exhaustive input-output testing:

-   Property: Every financial recommendation must include a confidence
    interval and at least one source citation

-   Property: No AI output may contain PII that was not present in the
    user\'s own data context

-   Property: Every recommendation must be traceable to at least one
    fact in the knowledge graph

-   Property: Response latency must remain below 2 seconds for voice
    interactions, 5 seconds for complex analysis

-   Property: The system must never recommend an action that violates
    the user\'s stated constraints

-   Property: AMPS score calculations must be monotonically consistent
    --- the same process state must always produce the same score

-   Property: PUDDING cross-domain connections must score above the
    minimum threshold (configurable) before surfacing to users

-   Property: The Death Spiral Detector must never produce a false
    negative on synthetic test cases drawn from historical business
    failures

**4.7 \'Show Our Work\' --- Validation Pathways for PUDDING and AMPS**

For proprietary processes, external credibility requires demonstrable
validation. The \'show our work\' strategy balances intellectual
property protection with the transparency needed to build trust:

**PUDDING Validation Strategy:**

-   Publish the methodology (not the implementation) as open research on
    arXiv

-   Document the 41.67% retrieval accuracy improvement with reproducible
    benchmarks and open test datasets

-   Frame the work as an applied adaptation of Swanson\'s
    Literature-Based Discovery --- connecting to established academic
    lineage

-   A 2025 arXiv survey confirms that LLM-powered LBD has \'a much
    broader scope of applicability\' beyond biomedicine --- PUDDING
    extends this to business knowledge

-   Invite independent researchers to reproduce results using the
    published methodology

**AMPS Validation Strategy:**

-   Map AMPS scores to established CMMI maturity levels for external
    comparability (documented in Section 3.2)

-   Track AMPS progression over time for pilot clients, publishing
    anonymised longitudinal results

-   Invite independent auditors to assess AMPS scoring methodology
    against ISO 9001 process maturity assessments

-   Create an open benchmark dataset of scored processes for community
    validation

**4.8 Academic Validation Strategy**

The academic validation pathway ensures that Amplified Partners\'
proprietary methodologies gain credibility beyond the commercial market:

-   arXiv preprints: PUDDING technique paper targeting the Knowledge
    Representation and Reasoning track

-   Benchmark publication: Open datasets for AMPS scoring validation and
    DocBench extraction accuracy

-   Conference presentations: UK AI Summit, Accountex, British Franchise
    Association events

-   Open methodology: the \'how\' is published; the \'what we built with
    it\' is proprietary --- following the Hormozi principle

**4.9 The Confident Failure Principle**

The system is designed to fail confidently. When it doesn\'t know, it
says so. When its confidence is low, it expresses that uncertainty
quantitatively. The AI Board uses five different models with
believability weighting; when models disagree significantly, the
disagreement itself is surfaced to the user rather than hidden behind a
false consensus.

> *\"I don\'t know\" is a valid and respected output. A system that
> always gives an answer is more dangerous than one that sometimes
> admits uncertainty.*

This principle extends to the Death Spiral Detector: when the system
detects potential business distress, it provides both the prediction and
its confidence level. A 60% confidence early warning is more useful than
waiting for 95% confidence when it\'s too late to act.

**4.10 GameDay Exercises and Tabletop Simulations**

Monthly GameDay exercises simulate catastrophic scenarios. Each follows
a structured protocol:

36. Scenario briefing: Define the failure, its scope, and the expected
    system response.

37. Execution: Trigger the failure in a staging environment (or, for
    tabletop exercises, talk through the response).

38. Observation: Record every system response, every alert triggered,
    every degradation observed.

39. Response: Activate the runbook. Time each step. Identify gaps.

40. Post-mortem: Structured review within 24 hours. Root cause,
    timeline, what worked, what didn\'t.

41. Improvement: Update the testing suite, the runbook, and the training
    materials.

**Standing GameDay Scenarios:**

-   The Beast goes offline for 24 hours --- what happens to active
    clients? How do they experience the failure?

-   A model update introduces systematic bias in financial
    recommendations --- how quickly is it detected?

-   A data breach is discovered in a third-party tool --- what is the
    containment protocol?

-   A client\'s business enters genuine distress --- does the Death
    Spiral Detector trigger correctly? Are the alerts appropriate?

-   Three clients in the same sector report contradictory results --- is
    the PUDDING Factory generating false patterns?

-   The FalkorDB container corrupts during a write operation --- is the
    recovery path clean?

-   A staff member reports that their private interview data was shared
    with their manager --- investigate and respond.

**SECTION 5: COMPUTE SCALING STRATEGY**

This section defines the hybrid compute architecture that supports the
entire Amplified Partners platform: The Beast as the always-on
production spine, with RunPod GPU cloud as burst compute muscle for
intensive workloads that require GPU acceleration.

**5.1 Current Infrastructure --- The Beast**

The Beast handles all always-on services: FalkorDB knowledge graph,
PostgreSQL operational database, Redis cache, Ollama for real-time CPU
inference, Traefik reverse proxy, SearXNG search proxy, and 22
additional Docker containers. It runs 24/7 at a fixed cost of
approximately €230--280/month.

Current limitation: no GPU. LLM inference runs on CPU via Ollama at
approximately 3--8 tokens/second for llama3.1:70b. This is adequate for
real-time interactions with smaller models but inadequate for
fine-tuning, batch inference, large-model research, and heavy
computational workloads.

**5.2 RunPod as Burst Compute**

RunPod is the primary burst GPU provider, selected after evaluation of
seven alternatives (Lambda Labs, Vast.ai, Jarvis Labs, CoreWeave,
Together AI, and SimplePod). It serves over 500,000 developers with
\$120M ARR, backed by Intel Capital and Dell Technologies Capital. Key
advantages:

-   GDPR-verified (independently audited, February 2026) with EU data
    centres: France, Netherlands, Sweden, Romania, Czech Republic,
    Iceland

-   Per-second billing --- no wasted compute. Stop the pod, billing
    stops.

-   Full Docker support --- compatible with existing container-first
    infrastructure

-   Persistent network volumes --- model weights cached between
    sessions, avoiding 30--60 minute re-downloads

-   50+ pre-configured AI templates for fast deployment

  ----------- ---------- ------------------ ------------------------------------------------------------------------
  **GPU**     **VRAM**   **On-Demand/hr**   **Best Use Case for Amplified Partners**
  H100 PCIe   80 GB      \$1.99             Production fine-tuning (70B QLoRA) --- 8-12 hrs = \$16-24 total
  A100 SXM    80 GB      \$1.39             Batch inference, PUDDING cross-domain analysis --- best throughput/\$
  A100 PCIe   80 GB      \$1.19             Fine-tuning (30B QLoRA) --- 6-10 hrs = \$7-12 total
  L40S        48 GB      \$0.79             Large batch embedding generation --- high memory bandwidth
  RTX 4090    24 GB      \$0.34             Quick experiments, parallel chaos testing --- cheap and parallelisable
  ----------- ---------- ------------------ ------------------------------------------------------------------------

**5.3 Hybrid Architecture: Beast + RunPod**

The core principle: The Beast is always-on production; RunPod is burst
GPU muscle. Data flows through encrypted Tailscale tunnels.

**What Stays on The Beast (always):**

-   All client PII and identifiers --- no exceptions

-   PostgreSQL operational database and FalkorDB knowledge graph

-   API keys, secrets, credentials

-   Audit logs and conversation history

-   Real-time Ollama inference for interactive use

-   Qdrant vector collections with client-tagged vectors

**Safe to Send to RunPod:**

-   Public model weights (Llama, Qwen --- no PII)

-   Anonymised/pseudonymised training data prepared on The Beast

-   Synthetic data generated on The Beast for testing

-   Research corpora, test datasets, benchmarks, code and configuration

**5.4 Tailscale Tunnel Architecture**

Tailscale (WireGuard under the hood) provides the encrypted networking
layer between The Beast and RunPod pods. Installation is straightforward
on both ends. Each RunPod pod joins the private Tailnet with a unique
hostname (runpod-gpu-\${RUNPOD\_POD\_ID}). No public ports are required;
all communication is encrypted end-to-end.

Expected latency: Hetzner Falkenstein → RunPod EU-FR-1 (Paris):
approximately 15--30ms round-trip. Acceptable for async job dispatch;
not suitable for real-time query-GPU-response chains. For real-time
interactive use, Ollama on The Beast handles inference locally.

**5.5 Data Sovereignty in Hybrid Setup**

The practical workflow for fine-tuning with PII protection:

42. Prepare training data on The Beast --- strip PII using the Presidio
    tokenisation gateway, anonymise, validate

43. Export anonymised JSONL dataset to RunPod network volume via
    Tailscale tunnel

44. Run fine-tuning job on RunPod GPU pod (H100 PCIe for 70B models,
    A100 for 30B)

45. Checkpoint every 10 minutes to network volume for fault tolerance

46. Transfer completed model weights back to The Beast via Tailscale

47. Serve merged model via Ollama on The Beast for production inference

48. Delete RunPod pod and volume after transfer --- no data persists on
    external infrastructure

**5.6 Cost Modelling**

  ----------------------------------------- ------------------- ------------------ ------------
  **Scenario**                              **Hetzner/month**   **RunPod/month**   **Total**
  Baseline (no GPU cloud)                   \$250               \$0                \$250
  Light usage (2× fine-tune, 1× batch)      \$250               \$30--50           \$280--300
  Active research sprint (1 week/month)     \$250               \$80--150          \$330--400
  Heavy usage (10 hrs/day GPU, 2 weeks)     \$250               \$280--400         \$530--650
  Max burst (10 hrs/day H100, full month)   \$250               \~\$600            \$850
  ----------------------------------------- ------------------- ------------------ ------------

Break-even analysis: At approximately 8 hours/day of H100 usage, renting
costs roughly the same as owning. Below 8 hrs/day: renting wins. A
second-hand H100 PCIe would cost \$15,000--\$20,000 upfront. At typical
burst usage (50--100 GPU-hours/month at \~\$1.50/hr average), payback
period on owned hardware: 7--16 years. Renting is definitively correct
at current scale.

**5.7 When to Scale vs When to Optimise**

  ------------------------ ----------------------------------------- -----------------------------------------
  **Decision Factor**      **Rent GPU Cloud**                        **Expand The Beast**
  Usage pattern            Burst / irregular                         Always-on / predictable
  Workload type            Training, fine-tuning, batch processing   Inference serving, databases, real-time
  Data sensitivity         Can anonymise first                       Requires PII access
  GPU hours/month          \< 200 hours                              \> 500 hours consistently
  Time horizon             \< 1 year                                 2+ years predictable need
  Current recommendation   ✓ RENT --- correct for current scale      Consider in 12--18 months
  ------------------------ ----------------------------------------- -----------------------------------------

**5.8 Upgrade Path --- What Triggers Buying Permanent Compute**

Four triggers for considering permanent GPU hardware:

-   Consistent GPU usage exceeding 400+ hours/month (running a GPU \>13
    hours every day) for 3+ consecutive months

-   Client base exceeds 100 active businesses requiring real-time GPU
    inference for interactive features

-   Fine-tuning cycle frequency increases to weekly or more, making pod
    spin-up overhead significant

-   Latency requirements tighten below what CPU inference can deliver
    --- voice response time under 500ms requires GPU

The decision framework: if three of four triggers are active
simultaneously, commission a hardware evaluation. Until then, the hybrid
model delivers better economics and greater flexibility than owned
hardware.

**SECTION 6: THE CONTENT ENGINE**

The content engine at Amplified Partners is not a marketing function. It
is a structural advantage built into the way the company operates. Every
architectural decision is potential content. Every failure is potential
content. Every research output is also a content atom. The
build-in-public approach being followed is informed by the results of
founders who have done this before.

**6.1 Three Audiences**

  --------------------- --------------------------------------------------------------------------- --------------------------------------------------------------------------------- ------------------------------------------
  **Audience**          **Who They Are**                                                            **What They Need**                                                                **Priority**
  SMB Owners            5.64M UK SMEs --- plumbers, bakers, builders, florists, personal trainers   Practical answers without corporate fluff, proof it works for people like them    Highest --- these are the customers
  Tech / AI Community   Indie hackers, CTOs, AI researchers, privacy professionals, investors       Architecture deep dives, open methodology, real numbers, honest failure stories   High --- credibility and talent pipeline
  Amplifier Partners    Accountants (340K+), coaches (89K), MSPs (12.8K), franchise operators       Tools to deploy with clients, reports, CPD content, revenue opportunity           High --- distribution multipliers
  --------------------- --------------------------------------------------------------------------- --------------------------------------------------------------------------------- ------------------------------------------

**6.2 Build-in-Public Precedents**

The build-in-public approach is proven at scale:

-   **Pieter Levels:** Photo AI reached \$132K MRR by month eighteen ---
    built on ten years of radical transparency. Portfolio reached \$3.1M
    total ARR by 2025.

-   **Marc Lou:** Generated \$92K in the first forty-eight hours of
    launching CodeFast --- the course itself was build-in-public content
    made tangible. Twenty-plus products in twelve months.

-   **Guillaume Moubeche:** Built lemlist from £1,000 to \$26M ARR
    primarily through LinkedIn build-in-public content. Published weekly
    showing actual cold email campaigns with exact templates and reply
    rates.

-   **Arvid Kahl:** Built FeedbackPanda, sold it, then wrote Zero to
    Sold --- turning the build story into a product in its own right.

-   **Daniel Vassallo:** Quit a \$500K/year job at AWS. Generated \$1M
    from courses and small products --- all documented publicly.

**6.3 The GaryVee Pyramid Applied to Build-in-Public**

The six-step cycle adapted for Amplified Partners:

49. Create pillar content from real work (architecture decisions,
    features shipped, problems solved, research findings)

50. Repurpose into micro-content via AI (6--10 platform-native drafts
    per pillar piece, each tagged by platform fit)

51. Distribute across platforms (LinkedIn, X, Substack, YouTube, blog,
    Fix Radio pitches)

52. Listen to what resonates (saves, shares, comments, DMs, what gets
    bookmarked)

53. Amplify winners with second-round content (expand what worked,
    retire what didn\'t)

54. Repeat --- let audience signals shape the content roadmap. The
    monthly theme plan is a guide, not a straitjacket.

**6.4 Content Atomisation Method**

Breaking complex ideas into their smallest possible units, then
reassembling them in different combinations for different purposes. The
improvement over the original GaryVee model: atoms are tagged by
platform fit, then recombined across multiple pillar pieces to create
apparently new content without new research.

From one long-form pillar piece, the AI pipeline produces in minutes:
5--7 LinkedIn posts, 10--15 tweet-sized snippets, 3--4 email newsletter
sections, 1--2 blog posts, and 1 short video script. Each platform has
distinct prompt patterns: LinkedIn uses a hook-in-line-one format (ten
words maximum) with three short paragraphs ending with a question; X
threads deconstruct arguments into numbered tweets with one concrete
example each; email snippets create curiosity without revealing the
solution.

The human refinement step applies voice, brand tone, and
platform-specific judgement for the final twenty per cent. The AI gets
you eighty per cent of the way.

**6.5 The Give-Away-Free Strategy**

Following Alex Hormozi\'s principle: give away the what and why for
free; charge for implementation and access.

**What to Give Away Free:**

-   The entire story of the build (this document, sliced into content
    atoms)

-   Process frameworks (how to diagnose cash flow problems, how to price
    a job, how to manage late-paying clients)

-   Templates (invoice templates, VAT tracker, job pricing calculator)

-   The PUDDING technique methodology (the intellectual framework ---
    open research)

-   Architecture decisions and technical reasoning (builds credibility
    with CTOs and developers)

-   Industry data and market analysis (FSB data, AI adoption stats ---
    positions Amplified as authoritative)

-   The Eight Laws and operational philosophy (cultural content that
    attracts aligned people)

-   All failure stories and lessons learned (authenticity builds trust
    faster than polish)

**What Stays Behind the Amplified Partners Paywall:**

-   The actual AI operating system (Business Brain, voice system,
    intelligence layer, agent stack)

-   Customised implementation for individual businesses (their data,
    their processes, their goals)

-   The Death Spiral Detector and early warning systems (the tool that
    might save your business)

-   Per-business data analysis and personalised recommendations

-   The staff interview system and wellbeing tracking (19 questions,
    privacy-first)

-   Ongoing AI-powered accountability (the Ulysses Clause enforcement
    --- the AI that won\'t let you lie)

-   Cross-business anonymised intelligence (PUDDING Factory insights ---
    network effects)

The logic: free content builds trust and demonstrates competence. The
paywall product solves the problem for them specifically, with their
data, in their business, with ongoing accountability. You cannot
replicate that from a blog post.

**6.6 Format Inventory --- 58 Formats from One Pillar Piece**

  -------------------- ----------- -----------------------------------------------------------------------------------------------------------------------------------
  **Category**         **Count**   **Key Formats**
  Written              12          Long-form blog, short summary, SEO tutorial, LinkedIn article, guest post, newsletter, email sequence, whitepaper, Reddit/HN post
  Social Text          8           LinkedIn long/short post, X thread, single tweet, Bluesky, Threads, Facebook, Mastodon
  Visual / Graphic     9           LinkedIn carousel, Instagram carousel, quote graphic, infographic, data visualisation, slide deck, meme
  Video                11          YouTube long-form, Shorts, LinkedIn video, Reels, TikTok, Facebook video, tutorial, vlog, webinar
  Audio                5           Solo podcast, interview episode, audiogram, show notes, audio newsletter
  Interactive          7           LinkedIn poll, X poll, AMA, live stream, X Space, Discord post, community Q&A
  Sales / Enablement   6           Case study, one-pager, investor memo, pitch deck section, objection guide, demo script
  -------------------- ----------- -----------------------------------------------------------------------------------------------------------------------------------

In practice, a focused team should target 15--25 pieces per pillar.
Quality and platform fit matter more than maximum volume.

**6.7 Weekly Cadence --- Four Hours Per Week**

  ----------- ----------------------------------------------------- ---------- ------------------------------------------------------
  **Day**     **Activity**                                          **Time**   **Output**
  Monday      Write or record pillar content                        90 min     1 long-form article, podcast, or documented decision
  Tuesday     AI atomisation --- feed through platform prompts      60 min     6--10 platform-native drafts
  Wednesday   Human refinement --- edit, add voice, verify facts    45 min     Final versions ready to publish
  Thursday    Schedule and distribute across channels               30 min     All content queued for optimal timing
  Friday      Engage --- respond to comments, note what resonated   15 min     Signal collection for next week\'s pillar
  ----------- ----------------------------------------------------- ---------- ------------------------------------------------------

**6.8 Monthly Theme Plan**

The month-by-month theme plan ties content to the build story chapters
and seasonal relevance:

  ------------ ---------------------- --------------- --------------------------------------------------------------------------------------
  **Month**    **Theme**              **Source**      **Key Angles**
  March 2026   The Origin Story       Chapters 1--2   The problem, the founding insight, dentist backstory, first attempt
  April        The AI Explosion       Chapter 3       PUDDING technique, Business Brain, 20 parallel instances, January breakthroughs
  May          The Wipe and Rebuild   Chapters 4--5   Losing everything, 9-day rebuild, discipline born from disaster, component inventory
  June         The Architecture       Chapter 6       The Beast, FalkorDB, data sovereignty, PII tokenisation, privacy by design
  July         The Operating System   Chapter 7       OS spec, voice-first, staff adoption, pricing tiers, website launch
  August       The Principles         Chapter 8       Eight Laws, Ulysses Clause, immutable accountability, life goals
  September    First Clients          Chapter 9       Dave\'s story, real results, accountant partnerships, waitlist growth
  October      The Audience           Part 2          SMB pain points, Fix Radio, accountant channel, build-in-public results
  November     The Method             Part 3          Content engine, slicing methodology, give-away-free, PUDDING discoveries
  December     Year in Review         All             Numbers, milestones, failures, plans for 2027
  ------------ ---------------------- --------------- --------------------------------------------------------------------------------------

Each month\'s content is sliced from the corresponding chapter, with
supplementary material from live business data, market developments, and
audience feedback from the previous month.

**6.9 Measurement Framework**

  ------------------ ------------------------------------------------ ------------------------------------ ------------------------------
  **Channel**        **Primary KPI**                                  **Secondary KPI**                    **Month 1--3 Target**
  LinkedIn           Engagement rate (likes+comments / impressions)   Profile views, connection requests   3%+ engagement rate
  X / Twitter        Thread impressions, bookmark rate                Follower growth, retweets            500+ impressions per thread
  Substack           Open rate, click-through rate                    Subscriber growth                    40%+ open rate, 5%+ CTR
  YouTube            Watch time, subscriber growth                    CTR on thumbnails                    50%+ retention at 30 seconds
  Blog / SEO         Organic traffic, keyword rankings                Time on page, bounce rate            100+ organic visits/month
  Website waitlist   Conversion rate from content                     Interview completion rate            50+ sign-ups by Month 3
  ------------------ ------------------------------------------------ ------------------------------------ ------------------------------

**6.10 Channel-Specific Strategy**

  ----------------- ----------------------------- ----------------- ------------------------------------------------
  **Channel**       **Best Time**                 **Frequency**     **Format**
  LinkedIn          7--9am and 12--1pm weekdays   3--5 posts/week   Long-form posts, carousels, short video
  X / Twitter       8--10am and 7--9pm            Daily             Threads, atomic posts, quote retweets
  Substack          Tuesday or Thursday 7am       Weekly            Deep-dive on one theme from the week
  YouTube           Saturday 10am                 1--2 per month    10--20 min builds, demos, story chapters
  Blog / SEO        When pillar published         Weekly            Technical and business articles for search
  TikTok / Reels    6--8pm evenings               3--5 per week     15--60 second clips: before/after, tips
  Fix Radio pitch   Monthly to producers          Monthly           2-minute monologue scripts for drive-time slot
  ----------------- ----------------------------- ----------------- ------------------------------------------------

**6.9 The Build-in-Public Flywheel**

Internal work generates content. Content generates audience. Audience
generates feedback. Feedback informs the next cycle of internal work.
This creates a self-reinforcing loop where every research output is also
a content atom.

> *\"Every research output is also a content atom.\"*

The competitive advantage is structural: the content is a by-product of
the actual work, not a separate function. The highest-performing single
post type across multiple build-in-public practitioners is the
controversial opinion backed by real data --- strong take plus specific
numbers equals viral B2B content.

PostHog\'s content philosophy captures the standard: \'Assume your
audience is smart. Don\'t try to trick them with tedious, clickbaity,
hyperbolic marketing tactics. It\'s patronising. Make honest claims
about the functionality of your product.\' Amplified Partners\' content
follows this standard. No exaggeration. No hype. Just the truth of the
build, told with enough specificity and honesty that the audience cannot
help but trust it.

**6.12 SMB Content Consumption Patterns**

Understanding when and how SMB owners consume content is critical. Most
tradespeople work physically with their hands during the day --- their
content windows differ sharply from office workers:

  ----------------- ----------------------------------------------------- --------------------------------------------------------
  **Time Window**   **Behaviour**                                         **Optimal Content Format**
  5--7am            Morning phone check before work starts                Quick tips, practical hacks (TikTok, Instagram Reels)
  7am--4pm          Active work --- phone use limited; radio in the van   Audio: Fix Radio, podcasts, audiograms
  12--1pm           Lunch break scroll                                    Short video, forum browsing (YouTube Shorts, Facebook)
  3--6pm            Drive time home                                       Podcasts, Fix Radio drive show
  7--10pm           Evening wind-down                                     Longer YouTube, in-depth guides, Facebook groups
  Weekends          Research mode --- planning next week                  Long-form guides, templates, Google/Reddit/MSE forums
  ----------------- ----------------------------------------------------- --------------------------------------------------------

Key implication: short, audio-friendly content (under 5 minutes) for the
van and commute. Longer YouTube content for evenings. Quick-hit social
posts for early morning and evening scroll. The average UK tradesperson
drives 88 miles per day --- 1.5 to 3 hours of audio content opportunity
daily. Fix Radio reaches 724,000 tradespeople every week --- one in four
UK tradespeople --- with an average listen time of 3.9 hours per day.

**6.13 LLM Optimisation as Distribution**

AI platforms like ChatGPT and Perplexity now drive 41x more referral
traffic year-on-year. Structuring content to be LLM-citable is a genuine
growth lever: answer-first blocks at the top of every article, semantic
chunking with clear headings, FAQ sections, TL;DR summaries, and
structured data that AI systems can parse and cite.

The AI-readable JSON version of the Operating System Specification
(committed 15 March 2026) was the first expression of this principle.
Every piece of content is written so that when someone asks an AI about
business operating systems for small businesses, Amplified Partners
appears in the answer.

**SECTION 7: THE VALUE EXTRACTION MAP**

This section is the \'programming\' that makes the content engine
systematic. For every major concept, technique, and decision in the
Amplified Partners ecosystem, we identify what it is, who it\'s valuable
for, what content it can become, what IP it represents, what competitive
advantage it provides, and whether it should be given away free or kept
proprietary.

This map ensures that no intellectual property goes unexploited, no
content opportunity is missed, and the balance between open generosity
and proprietary protection is maintained deliberately rather than
accidentally.

**PUDDING Technique**

  ------------------------------ ------------------------------------------------------------------------------------------------------------------------
  **Dimension**                  **Detail**
  Target Audiences               AI researchers, tech community, indie hackers
  Content Formats                arXiv paper, blog series, X threads, conference talks, technical deep dives
  Research / IP Value            Novel adaptation of Swanson\'s 1986 Literature-Based Discovery for business knowledge --- 41.67% retrieval improvement
  Competitive Advantage          First application of LBD to SMB knowledge. No competitor has cross-domain discovery.
  Free vs Proprietary Strategy   Methodology open (builds academic credibility); implementation and PUDDING Factory proprietary
  ------------------------------ ------------------------------------------------------------------------------------------------------------------------

**Business Brain**

  ------------------------------ -----------------------------------------------------------------------------------------------------------------------
  **Dimension**                  **Detail**
  Target Audiences               SMB owners, coaches, accountants
  Content Formats                Demo videos, case studies, white papers, diagnostic reports
  Research / IP Value            Integrated intelligence layer (600+ line schema) combining Death Spiral Detection, TOC, and AMPS scoring
  Competitive Advantage          Combines predictive distress detection with process improvement in one system. No competitor offers this integration.
  Free vs Proprietary Strategy   Proprietary --- core product. Free diagnostic teaser drives conversion.
  ------------------------------ -----------------------------------------------------------------------------------------------------------------------

**FalkorDB Decision**

  ------------------------------ -------------------------------------------------------------------------------------
  **Dimension**                  **Detail**
  Target Audiences               CTOs, developers, tech leads, AI researchers
  Content Formats                Technical blog post, architecture deep dive, \'Why we chose X over Y\' series
  Research / IP Value            Practical experience with graph+vector single engine replacing Neo4j+Qdrant
  Competitive Advantage          Evidence-based vendor selection narrative. Specific performance numbers.
  Free vs Proprietary Strategy   Give away entirely --- builds technical credibility and attracts developer audience
  ------------------------------ -------------------------------------------------------------------------------------

**Death Spiral Detector**

  ------------------------------ ------------------------------------------------------------------------------------------------------------------------
  **Dimension**                  **Detail**
  Target Audiences               SMB owners, accountants, coaches, financial advisors
  Content Formats                Free diagnostic tool (limited), webinar series, case studies with anonymised data
  Research / IP Value            Altman Z-Score + Cash Conversion Cycle + Margin Erosion + Customer Concentration Risk --- integrated predictive system
  Competitive Advantage          Predictive, not reactive. 80-90% accuracy. No SMB product currently offers automated distress prediction.
  Free vs Proprietary Strategy   Free initial diagnostic (lead gen); paid ongoing monitoring and alerts
  ------------------------------ ------------------------------------------------------------------------------------------------------------------------

**Voice-First Design**

  ------------------------------ -----------------------------------------------------------------------------------------------------------------
  **Dimension**                  **Detail**
  Target Audiences               SMB owners, product designers, accessibility community
  Content Formats                Product demo, UX case study, conference presentation, blog series
  Research / IP Value            Voice as primary interface for non-desk workers. Three-stage staff adoption journey.
  Competitive Advantage          Solves the \'dirty hands\' problem uniquely. No competitor has designed specifically for tradesperson workflow.
  Free vs Proprietary Strategy   Give away design philosophy (thought leadership); product implementation proprietary
  ------------------------------ -----------------------------------------------------------------------------------------------------------------

**DocBench**

  ------------------------------ --------------------------------------------------------------------------------------------------
  **Dimension**                  **Detail**
  Target Audiences               CTOs, privacy professionals, document processing community
  Content Formats                Technical white paper, benchmark publication, accuracy comparison tables
  Research / IP Value            99.53% extraction accuracy using 8B model running locally. No data leaves the server.
  Competitive Advantage          Privacy-first extraction at near-perfect accuracy. Local processing eliminates third-party risk.
  Free vs Proprietary Strategy   Publish benchmarks openly (credibility); implementation proprietary
  ------------------------------ --------------------------------------------------------------------------------------------------

**Ulysses Clause**

  ------------------------------ --------------------------------------------------------------------------------------------------
  **Dimension**                  **Detail**
  Target Audiences               Founders, investors, business coaches, governance professionals
  Content Formats                LinkedIn post series, Substack deep dive, founder community talks
  Research / IP Value            Governance mechanism --- system loyal to mission, not man. AI enforces accountability immutably.
  Competitive Advantage          No competitor has immutable AI accountability. Powerful emotional resonance.
  Free vs Proprietary Strategy   Give away entirely --- philosophy builds trust and differentiates from every other AI tool
  ------------------------------ --------------------------------------------------------------------------------------------------

**Eight Laws**

  ------------------------------ ---------------------------------------------------------------------------
  **Dimension**                  **Detail**
  Target Audiences               All audiences --- universal appeal
  Content Formats                Social content series (one post per law), poster, manifesto, video series
  Research / IP Value            Operational governance framework born from catastrophe (the wipe)
  Competitive Advantage          Authentic origin story. Each law has a specific incident behind it.
  Free vs Proprietary Strategy   Give away entirely --- cultural content that defines the brand
  ------------------------------ ---------------------------------------------------------------------------

**Telegraph Pole**

  ------------------------------ ----------------------------------------------------------------------------------------
  **Dimension**                  **Detail**
  Target Audiences               SMB owners, team leaders, HR-free workplaces
  Content Formats                Implementation template, guide, case study, LinkedIn post
  Research / IP Value            Public wins board for team morale --- simple, powerful, immediately deployable
  Competitive Advantage          Simple concept with immediate practical application. No technology required.
  Free vs Proprietary Strategy   Give away entirely --- drives word-of-mouth and positions brand as practically helpful
  ------------------------------ ----------------------------------------------------------------------------------------

**Testing Framework**

  ------------------------------ -------------------------------------------------------------------------------------------
  **Dimension**                  **Detail**
  Target Audiences               CTOs, developers, QA engineers, AI researchers
  Content Formats                Technical blog series, open-source tooling, conference talks
  Research / IP Value            Five-layer AI testing pyramid + Chaos-Driven Development + four-department chaos approach
  Competitive Advantage          Comprehensive AI-specific testing methodology. FalkorDB-specific chaos experiments.
  Free vs Proprietary Strategy   Methodology open (community credibility); custom tooling proprietary
  ------------------------------ -------------------------------------------------------------------------------------------

**Process Scores (AMPS)**

  ------------------------------ -------------------------------------------------------------------------------------------
  **Dimension**                  **Detail**
  Target Audiences               SMB owners, coaches, consultants, franchise operators
  Content Formats                Free assessment tool, benchmarking reports, longitudinal tracking visualisations
  Research / IP Value            0-10 maturity scale mapped to CMMI. Universal, comparable, actionable.
  Competitive Advantage          No SMB product offers a standardised process maturity score. Fills a gap.
  Free vs Proprietary Strategy   Free initial assessment (massive lead gen); paid tracking and improvement recommendations
  ------------------------------ -------------------------------------------------------------------------------------------

**Chaos Engineering Approach**

  ------------------------------ -------------------------------------------------------------------------------------
  **Dimension**                  **Detail**
  Target Audiences               Tech community, CTOs, DevOps engineers
  Content Formats                Blog series, GameDay reports, conference talks, open-source tools
  Research / IP Value            Four-department chaos approach adapted for AI+knowledge graph systems
  Competitive Advantage          AI-specific chaos experiments. FalkorDB resilience testing suite.
  Free vs Proprietary Strategy   Give away entirely --- builds technical credibility and attracts engineering talent
  ------------------------------ -------------------------------------------------------------------------------------

**Additional Value Assets**

-   **Pre-Cove Translator:** Accent handling IP. Give away the concept
    (content for SMB owners with regional accents); keep implementation
    proprietary.

-   **Three-Layer Data Sovereignty:** Architecture pattern. Give away as
    white paper for CTOs and privacy professionals; builds trust for
    sales conversations.

-   **AI Board (Multi-Model Consensus):** Decision-making innovation
    inspired by Ray Dalio. Give away the concept; product implementation
    is proprietary.

-   **Staff Interview System:** 19-question privacy-first system.
    Methodology can be shared (coaches love frameworks); per-client data
    stays proprietary.

-   **Content Atomisation Pipeline:** Meta-content about content
    creation. Give away entirely --- it demonstrates competence and
    attracts the tech audience.

-   **Build Timeline (766 lines):** The chronological record of every
    decision. Pure build-in-public gold --- give away entirely.

-   **Expert Research Library (27 experts):** Dalio, Gerber, Godin,
    Kennedy, Lund, Ziglar, and 21 others catalogued with actionable
    principles. Give away the framework; application to specific
    businesses is proprietary.

-   **Nature\'s Logic Systems:** Biomimicry models for process design.
    Highly shareable research content for the tech audience.

**SECTION 8: IMPLEMENTATION ROADMAP**

Practical next steps in three horizons, tied to specific deliverables
and measurable milestones. Each horizon builds on the previous one. The
roadmap is governed by the Eight Laws --- particularly Law 3 (Finish or
flag --- no silent abandonment) and Law 4 (Self-rate every session).

**8.1 Immediate --- 0 to 3 Months (March--June 2026)**

**Build:**

-   Complete first client deployment: Dave Morrison, Jesmond Plumbing
    --- end of March 2026. Two to ten employees, Newcastle-based.

-   Finalise FalkorDB + Graphiti integration for multi-tenant production
    with architectural isolation per client

-   Deploy The Beast production stack with all 29 containers operational
    and monitored

-   First RunPod burst compute session --- fine-tune qwen3-coder on
    Amplified Partners domain data using H100 PCIe (\$1.99/hr)

-   Implement automated AMPS scoring for pilot client processes with
    baseline measurements

-   Launch waitlist on amplifiedpartners.ai with structured voice
    interview capture

**Test:**

-   Execute first GameDay exercise: \'The Beast goes offline for 24
    hours\'

-   Complete FalkorDB chaos experiment suite (8 experiments defined in
    Section 4.4)

-   Establish baseline performance metrics for all five testing layers

-   Run first PUDDING MIX on pilot client data (anonymised) --- validate
    cross-domain discovery in production

-   Property-based test suite operational with all 8 core properties
    verified

**Publish:**

-   Launch build-in-public content series: Month 1 theme --- \'The
    Origin Story\' (Chapters 1--2)

-   First Substack newsletter issue (target: 40%+ open rate)

-   First LinkedIn carousel: \'The 8 Laws of Amplified Partners\'

-   First accountant white paper draft submitted to AccountingWEB

-   First technical blog: \'Why We Chose FalkorDB Over Neo4j + Qdrant\'

-   Target: 50+ waitlist sign-ups by end of Month 3

**8.2 Medium-Term --- 3 to 9 Months (June--December 2026)**

**Scale Testing:**

-   Expand testing to 10--100 user tier --- validate performance
    baselines hold under parallel load

-   Implement automated chaos testing pipeline (scheduled fortnightly,
    results feed Kaizen department)

-   Complete V-Model validation across all four specification levels

-   Establish statistical monitoring for model drift detection across
    all served models

-   First security penetration test by external assessor

**First Clients:**

-   Onboard 5--10 SMB clients in the North East (priority: tradespeople,
    service businesses)

-   Validate AMPS scoring with real business processes --- track
    progression over 3+ months

-   First Death Spiral Detector activation on real client data ---
    validate prediction accuracy

-   Collect first case study with quantified outcomes (AMPS improvement,
    time saved, revenue impact)

-   First accountant partnership: CPD webinar on AI diagnostics for SMB
    clients

**Content Engine Operating:**

-   Weekly cadence fully operational (4 hours/week producing 15+ content
    pieces per pillar)

-   Monthly themes aligned to Story of the Build chapters (April: AI
    Explosion, May: Wipe & Rebuild, June: Architecture)

-   First Hacker News submission: \'Applying Swanson\'s Literature-Based
    Discovery to business AI\'

-   Fix Radio pitch submitted --- target: one aired segment by Month 6

-   Targets: 3%+ LinkedIn engagement rate, 40%+ Substack open rate, 100+
    organic blog visits/month

**8.3 Long-Term --- 9 to 24 Months (December 2026--March 2028)**

**CMMI Progression:**

-   Achieve CMMI Level 3 equivalent across all core processes (AMPS 4--5
    baseline)

-   Formal external assessment of AMPS methodology by independent
    auditors

-   Publish CMMI mapping validation with anonymised longitudinal client
    data

**External Benchmarks:**

-   Submit PUDDING technique paper to arXiv (Knowledge Representation
    and Reasoning track)

-   Publish DocBench accuracy benchmarks with open test datasets for
    community validation

-   Establish AMPS as an industry-referenced process maturity score for
    UK SMBs

-   First conference presentation (UK AI Summit, Accountex, or BFA
    Annual Conference)

**Platform Scale:**

-   100+ active SMB clients generating meaningful cross-domain PUDDING
    insights

-   Evaluate transition from burst GPU rental to permanent compute
    (threshold: 400+ GPU-hours/month)

-   Launch Tier 3 federated intelligence product for complex operations

-   First franchise operator deployment (single sale → 50+ unit rollout)

-   First MSP reseller channel partnerships (target: 5 MSP applications
    by Month 18)

**Revenue Milestones:**

-   Month 12: £10K MRR from 30--40 active clients

-   Month 18: £50K MRR with accountant partnership channel contributing
    30%+ of new clients

-   Month 24: £100K+ MRR with demonstrable PUDDING network effects
    improving client outcomes

The North East AI Growth Zone provides a tailwind: £30 billion in
committed investment, Sage at Cobalt Park, OpenAI and NVIDIA in the
Stargate UK initiative, Blackstone\'s £10 billion Blyth commitment.
Amplified Partners is being built in the epicentre of the UK\'s AI
investment.

**8.4 Key Risk Factors and Mitigations**

Every roadmap carries risks. Identifying them upfront --- consistent
with Law 3 (Finish or flag) and the Confident Failure principle ---
allows systematic mitigation:

  ------------------------------------------------------ ----------------- ------------ -------------------------------------------------------------------------------
  **Risk**                                               **Probability**   **Impact**   **Mitigation**
  First client deployment delayed                        Medium            High         Parallel preparation for 3 alternative first clients in North East trades
  FalkorDB performance at multi-tenant scale             Low               Critical     Chaos testing suite (Section 4.4); fallback to Neo4j+Qdrant if required
  RunPod Secure Cloud pricing increases                  Medium            Low          Vast.ai as secondary provider; Together AI for inference-only workloads
  Content fails to generate audience traction            Medium            Medium       A/B testing across platforms; pivot formats based on engagement signals
  Accountant partnership channel slower than projected   High              Medium       Parallel MSP and coach channels; direct SMB outreach as fallback
  Model drift in production LLMs                         High              High         Statistical monitoring; automated regression tests; model version pinning
  GDPR compliance challenge from regulatory change       Low               Critical     Architecture-first privacy (no policy changes needed); legal review quarterly
  Competitor launches similar SMB AI product             High              Medium       PUDDING technique as defensible moat; build-in-public authenticity; speed
  ------------------------------------------------------ ----------------- ------------ -------------------------------------------------------------------------------

The most important mitigation is structural: the build-in-public
approach means that Amplified Partners\' story, methodology, and
authenticity cannot be replicated by a competitor who starts later. The
first-mover advantage in trust is permanent.

**8.5 Success Metrics Summary**

The following metrics define success across the three horizons:

  ------------------------------- ---------------------- ---------------------- ----------------------------
  **Metric**                      **Month 3 Target**     **Month 9 Target**     **Month 24 Target**
  Active SMB clients              1--3                   5--10                  100+
  MRR                             £500                   £3K                    £100K+
  Waitlist sign-ups               50+                    500+                   5,000+
  LinkedIn engagement rate        3%+                    5%+                    5%+ (sustained)
  Substack subscribers            100                    1,000                  10,000
  PUDDING discoveries validated   2                      10                     50+
  AMPS average client score       Baseline measured      1+ point improvement   Average 5+ (Defined level)
  GameDay exercises completed     3                      9                      24
  Accountant partnerships         0 (outreach started)   3--5                   20+
  GitHub stars (open repos)       10                     100                    1,000+
  ------------------------------- ---------------------- ---------------------- ----------------------------

**APPENDIX A: KEY DATES REFERENCE TABLE**

  ---------------- ----------------------------------------------------------------------------------------------
  **Date**         **Milestone**
  2025-11-27       covered-ai-v2 repo created --- the founding moment
  2025-12-08       Earliest dated vault document (Business Decision Making Best Practices)
  2025-12-11       voice-ai repo --- first voice experiments
  2026-01-13       First Session Completion Report; AI Stack Auditor built; £290K--750K assets valued
  2026-01-16       20 parallel Kilo Code instances running; Mac at capacity
  2026-01-17       Business Brain concept coined; Obsidian+Neo4j+Qdrant stack chosen
  2026-01-19       PUDDING technique born; neutral taxonomy system designed (2,401 combinations)
  2026-01-22       41.67% RAG improvement validated (Swanson LBD + RAG combination)
  2026-01-25       PUDDING formally named \'Synbious\'; pattern recognition methodology documented
  2026-02-04       Local-first pivot (Ollama/Qwen); \'blinkers\' concept introduced
  2026-02-05       amplified-vault + gatekeeper-agent repos born (one minute apart)
  2026-02-07       CODEBASE WIPE --- all code lost. No git backups. Only database survived.
  2026-02-11       Sam (OpenClaw) agent formalised; immutable accountability discovered; gate system introduced
  2026-02-14       amplified-crm repo created --- AI-powered CRM for UK tradespeople
  2026-02-14--15   50 landing pages built (58 static pages for UK trades)
  2026-02-16       Complete system code-complete: Business Brain, Voice, 50 landing pages, PII Gateway
  2026-02-20--21   Voice capture marathon: 800+ Monologue files (04:36 AM to 21:10)
  2026-02-22       PUDDING Technique canonical document written (7-step process, 24 dimensions)
  2026-02-24       anthropic-token-proxy repo (cost reduction); 9 co-working sessions in one day
  2026-02-28       Telegraph Pole concept born; Ulysses Clause formalised
  2026-03-10       PUDDING MIX 001+002; Operational Protocol v1 (Eight Laws); Radical Attribution Schema
  2026-03-11       amplified-partners repo --- master consolidation (5,081 files, 9 commits in one night)
  2026-03-11       FalkorDB + Graphiti final decision --- Qdrant dropped. Single engine replaces two.
  2026-03-13       amplified-site repo created --- website built in one day
  2026-03-14       Website feature sprint (8 commits in 15 minutes); Operating System Spec (688 lines)
  2026-03-15       AI-readable JSON OS Spec committed --- spec for both humans and agents
  ---------------- ----------------------------------------------------------------------------------------------

**APPENDIX B: REPOSITORY MAP**

All 15 repositories across the ewan-dot GitHub account as of 16 March
2026:

  ----------------------------- ------------- -------------------------------------------------------------
  **Repository**                **Created**   **Description**
  covered-ai-v2                 27 Nov 2025   The founding repo --- original Covered AI product
  voice-ai                      11 Dec 2025   Early voice AI experiments
  librarian-api                 21 Dec 2025   Knowledge management API concept
  docs                          26 Jan 2026   Documentation repo --- documentation as first-class concern
  beautifulgolden               4 Feb 2026    SMBFrictionReducer experiment
  smb-ai-friction-consultancy   4 Feb 2026    Local Ollama/Qwen agentic system with blinkers
  gatekeeper-agent              5 Feb 2026    Quality control gate for knowledge vault
  amplified-vault               5 Feb 2026    Primary knowledge vault (auto-synced every 5--15 minutes)
  byker-production              7 Feb 2026    Byker Business Help production --- post-wipe recovery
  amplified-crm                 14 Feb 2026   AI-powered CRM: 85 routes, 18+ tables, Twilio/Resend/Xero
  anthropic-token-proxy         24 Feb 2026   Local reverse proxy --- prompt caching, zero code changes
  amplified-core                27 Feb 2026   MCP Gateway for Bob (client-facing agent)
  amplified-partners            11 Mar 2026   Main repo: 5,081 files, vault + agent stack + architecture
  amplified-site                13 Mar 2026   Public website (Vite + React + Express)
  nexus-v2                      14 Mar 2026   Investment system (separate project)
  ----------------------------- ------------- -------------------------------------------------------------

**APPENDIX C: FOUR-DEPARTMENT STRUCTURE**

Amplified Partners organises all work through four departments, each
with a distinct purpose. This structure ensures that building,
improving, testing, and operating are treated as equally important
permanent functions --- not sequential phases.

  ---------------- ---------------------------- ----------------------------------------------------------------------------------------------------------- ----------------------------------------------------
  **Department**   **Purpose**                  **Key Responsibilities**                                                                                    **Testing Role**
  Kaizen           Continuous improvement       Review AMPS scores, identify improvement opportunities, maintain quality standards, process documentation   Improve test processes themselves; track test debt
  R&D              Innovation and exploration   Build new features, evaluate tools, prototype approaches, conduct research, PUDDING analysis                Develop new testing approaches and custom tooling
  Chaos            Resilience and robustness    Fault injection, adversarial testing, stress testing, GameDay exercises, failure mode cataloguing           Active fault injection and resilience validation
  Real             Production operations        System monitoring, incident response, client support, performance tracking, on-call rotation                Production monitoring and incident post-mortems
  ---------------- ---------------------------- ----------------------------------------------------------------------------------------------------------- ----------------------------------------------------

The Parallel Build Strategy (COV-175, committed 11 March 2026) defines
six workstreams that cross-cut the four departments: APIs, MCPs, P2
Tokenisation, Security, Kaizen, and Chaos. Each workstream has a
designated owner and weekly status reporting.

**APPENDIX D: GLOSSARY OF AMPLIFIED PARTNERS TERMINOLOGY**

  --------------------------- ----------------------------------------------------------------------------------------------------------------------------------------
  **Term**                    **Definition**
  AMPS                        Amplified Process Maturity Score --- the 0--10 scale measuring process maturity, mapped to CMMI levels
  The Beast                   Hetzner AX162-R dedicated server: 48-core AMD EPYC, 256GB RAM, 10Gbit, Falkenstein Germany (EU)
  Blinkers                    Design principle: agents constrained by rules but unlimited within those rules. Like a horse --- can\'t see distractions, runs faster.
  Bob                         Client-facing AI agent (MCP Gateway via amplified-core)
  Business Brain              Unified intelligence layer: 600+ line schema combining interviews, business data, and AI reasoning
  CDD                         Chaos-Driven Development --- building methodology that defines failure modes first and builds to survive them
  CMMI                        Capability Maturity Model Integration --- industry standard for process maturity (Levels 1--5)
  Cove                        Orchestration layer for the multi-agent system
  Death Spiral Detector       Predictive system: Altman Z-Score + Cash Conversion Cycle + Margin Erosion + Customer Concentration Risk
  DMAIC                       Define, Measure, Analyse, Improve, Control --- Six Sigma improvement methodology
  DocBench                    Data extraction engine: 99.53% accuracy, 8B model, runs locally on The Beast
  FalkorDB                    Graph + vector database: sub-10ms Cypher queries, 10K+ isolated graphs, replaced Neo4j + Qdrant
  GameDay                     Monthly exercise simulating catastrophic scenarios to test system resilience and response protocols
  Gatekeeper Agent            Quality control gate: Python-based, validates all content entering the knowledge vault
  Graphiti                    Temporal layer: adds valid\_at/invalid\_at timestamps to every fact in FalkorDB
  IFR                         Ideal Final Result --- TRIZ concept: the theoretical perfect process with zero waste
  Immutable Foundation Code   Governance mechanism: even the founder is subject to system rules. Cannot be overridden.
  Kaizen                      Department for continuous improvement. Japanese 改善: \'change for better\'
  OpenClaw                    Ewan\'s personal AI tool for building the product (not the product itself)
  PDCA                        Plan-Do-Check-Act --- Deming\'s cycle for continuous improvement, mapped to sprint cadence
  PicoClaw                    Lightweight agent running on Mac Mini M4 Pro
  PII Tokenisation            353-line Microsoft Presidio wrapper: tokenises personal data on-device before transmission
  Pre-Cove                    Mandatory accent/speech sanitisation layer on all voice input --- ensures equal quality regardless of dialect
  PUDDING                     Cross-domain knowledge discovery: adapts Don Swanson\'s 1986 Literature-Based Discovery for business
  PUDDING Factory             Layer 3 anonymised aggregation: where cross-domain patterns are discovered across clients
  Radical Attribution         COV-168: every fact, framework, or borrowed idea must be cited with its origin
  Room Protocol               Validation: Sam researches, Ewan judges, Claude formalises --- three-step discovery validation
  Sam                         Primary OpenClaw agent: coordination, accountability tracking, commitment gates
  Synbious                    Alternative name for the PUDDING cross-domain synthesis system
  Telegraph Pole              Public wins board: achievements posted for team morale. Named for carrying messages across distance.
  TOC                         Theory of Constraints --- Goldratt\'s five focusing steps for bottleneck identification and elimination
  Ulysses Clause              System loyalty to mission over any individual. Named for the hero tied to the mast.
  V-Model                     Testing: every specification level has corresponding validation. Requirements ↔ Acceptance, Design ↔ Integration.
  --------------------------- ----------------------------------------------------------------------------------------------------------------------------------------

---
title: "Website Builder Architecture"
id: "website-builder-architecture"
version: 1
created: 2026-04-25
last_validated: 2026-04-25
type: document
topic_type: reference
status: imported
source_file: "amplified-website-builder-architecture.docx"
signed_by: "Devon, 2026-04-25, devin-992682c244cf444f91e0a516498afbfd"
---

**AMPLIFIED PARTNERS**

**Amplified Website Builder**

Architecture & Feasibility Study

*From UX Audit to Production-Ready Client Websites*

Author: **Amplified Partners**

Date: **March 2026**

Classification: **Confidential --- Internal Use Only**

**1. Executive Summary**

This document defines the architecture for a **repeatable website production pipeline** operated by Amplified Partners\' agent team. This is not a SaaS website builder --- it is an internal production system that takes Amplified\'s existing infrastructure (knowledge vault, voice interface, marketing pipeline, DISC profiling, FalkorDB knowledge graph) and wraps it into a deterministic workflow for producing high-quality client websites at scale.

The pipeline follows six stages: **Audit → Diagnose → Design → Build → Validate → Deploy**. Each stage is designed to maximise deterministic, validated operations while reserving AI for the creative and contextual work where it genuinely adds value.

The governing principle, as articulated by Ewan Bramley:

> *\"Every aspect of a website is researched to allow us to automate it deterministically as much as possible, and then the AI does its beautiful bit at the end.\"*

This follows the **Drift to Determinism (DriDe)** pattern: AI handles novel creative work; everything else crystallises into validated, deterministic templates and components over time. Each client project teaches the system. Patterns that recur get codified. The AI footprint shrinks as the template library grows --- reducing cost, increasing reliability, and making quality predictable.

The differentiator is the **knowledge-base FAQ layer**. Every client website ships with a voice-first FAQ powered by FalkorDB/Graphiti graph RAG, DISC-aware personality adaptation, and the full Amplified voice stack (Vapi/Twilio/Cartesia). This isn\'t a chatbot bolted on --- it\'s a knowledge system that understands the client\'s business relationally.

Feasibility is strong. Every major component either exists in Amplified\'s current infrastructure or is available as open-source tooling. Estimated per-client setup cost: £200--500. Estimated monthly running cost: £20--50. The system pays for itself within the existing pricing tiers.

**2. What We Already Have**

The following table inventories every existing Amplified asset that feeds into the website builder pipeline. The maturity of this existing infrastructure is the reason this project is feasible now rather than aspirational.

  ---------------------------------------- ----------------------- ------------ ----------------------------------------------------
  **Asset**                                **Location**            **Status**   **Role in Website Builder**
  Knowledge Vault (4,787 files)            /opt/amplified/vault/   Active       Content source, FAQ knowledge base
  FalkorDB + Graphiti                      Docker, port 6379       Active       Graph RAG for voice FAQ, client knowledge graphs
  14-Agent Marketing Pipeline              Cove orchestrator       Partial      Content creation, SEO, brand voice enforcement
  Website Manager Agent (v2)               COV-235 spec            Spec\'d      Builds/maintains/optimises client websites
  Voice Interface (Vapi/Twilio/Cartesia)   Beast server            MVP          Voice-first FAQ on client websites
  The Pulse Dashboard                      Spec\'d                 Spec\'d      Client-facing data view --- website integration
  DISC Personality Profiles                Marketing pipeline      Active       Adapt website copy and voice tone per visitor type
  Brand Voice Guardian Agent               Marketing pipeline      Foundation   Enforces client brand consistency
  Complete Business Website Bible          Vault                   Reference    13-part framework for business web presence
  Design Token System                      Nexus tokens            Active       Consistent styling across all output
  Playwright QA Pipeline                   Skills library          Available    Visual regression, cross-breakpoint testing
  axe-core Accessibility                   Skills library / npm    Available    WCAG 2.2 AA automated testing
  ---------------------------------------- ----------------------- ------------ ----------------------------------------------------

**Key insight:** Eight of twelve assets are already active or at MVP. The pipeline assembles existing capabilities rather than building from scratch. The primary engineering work is integration, not invention.

**3. The Pipeline Architecture**

The pipeline operates in six stages. Each stage has a clearly defined input, set of actions, output, and a documented split between deterministic operations and AI-powered tasks. The DriDe ratio shifts toward determinism as the component library matures.

**Stage 1: AUDIT --- Reverse-Engineer**

+-------------+-------------------------------------------------------------------------------------------------------------------------------------+
| **Aspect**  | **Detail**                                                                                                                          |
+-------------+-------------------------------------------------------------------------------------------------------------------------------------+
| Input       | Any URL (client\'s existing website or competitor reference)                                                                        |
+-------------+-------------------------------------------------------------------------------------------------------------------------------------+
| Actions     | Extract design tokens (colors, typography, spacing) via Design Token Extractor + custom Playwright scripts                          |
|             |                                                                                                                                     |
|             | Run axe-core for WCAG 2.2 AA baseline                                                                                               |
|             |                                                                                                                                     |
|             | Screenshot at 375px, 768px, 1280px via Playwright                                                                                   |
|             |                                                                                                                                     |
|             | Identify component patterns (manual + DOM analysis)                                                                                 |
|             |                                                                                                                                     |
|             | Score each component against WCAG 2.2 AA; note WCAG 3 Core Requirements where applicable                                            |
+-------------+-------------------------------------------------------------------------------------------------------------------------------------+
| Output      | Pattern library JSON, accessibility report, breakpoint screenshots, component inventory                                             |
+-------------+-------------------------------------------------------------------------------------------------------------------------------------+
| DriDe Split | **90% deterministic** (extraction, screenshots, axe scanning) / **10% AI** (component pattern recognition, improvement suggestions) |
+-------------+-------------------------------------------------------------------------------------------------------------------------------------+

**Stage 2: DIAGNOSE --- Ruthless Report**

+-------------+---------------------------------------------------------------------------------------------------------------------------------------------------------------------+
| **Aspect**  | **Detail**                                                                                                                                                          |
+-------------+---------------------------------------------------------------------------------------------------------------------------------------------------------------------+
| Input       | Stage 1 output (pattern library, accessibility report, screenshots)                                                                                                 |
+-------------+---------------------------------------------------------------------------------------------------------------------------------------------------------------------+
| Actions     | Classify components as \"production-ready\" vs \"pretty but fragile\"                                                                                               |
|             |                                                                                                                                                                     |
|             | Flag accessibility failures with severity scoring                                                                                                                   |
|             |                                                                                                                                                                     |
|             | Identify responsive breakage points across breakpoints                                                                                                              |
|             |                                                                                                                                                                     |
|             | Compare against WCAG 2.2 AA checklist systematically                                                                                                                |
|             |                                                                                                                                                                     |
|             | Generate improvement recommendations with brand-preserving context                                                                                                  |
+-------------+---------------------------------------------------------------------------------------------------------------------------------------------------------------------+
| Output      | Design audit report with before/after comparison specs, severity-scored findings, recommended fixes                                                                 |
+-------------+---------------------------------------------------------------------------------------------------------------------------------------------------------------------+
| DriDe Split | **70% deterministic** (rule-based scoring, contrast calculations, semantic HTML checks) / **30% AI** (contextual recommendations, brand-preserving fix suggestions) |
+-------------+---------------------------------------------------------------------------------------------------------------------------------------------------------------------+

**Stage 3: DESIGN --- Improved Variants**

+-------------+-----------------------------------------------------------------------------------------------------------------------------------------------------+
| **Aspect**  | **Detail**                                                                                                                                          |
+-------------+-----------------------------------------------------------------------------------------------------------------------------------------------------+
| Input       | Stage 2 findings + client brand spec (YAML config from marketing pipeline)                                                                          |
+-------------+-----------------------------------------------------------------------------------------------------------------------------------------------------+
| Actions     | Generate improved component variants preserving brand feel while fixing accessibility and responsiveness                                            |
|             |                                                                                                                                                     |
|             | Apply design tokens from Nexus system or client-specific tokens                                                                                     |
|             |                                                                                                                                                     |
|             | Build to validated component templates (React/Astro with defined slot structure)                                                                    |
|             |                                                                                                                                                     |
|             | Create DISC-aware content variants for key pages                                                                                                    |
+-------------+-----------------------------------------------------------------------------------------------------------------------------------------------------+
| Output      | Upgraded component code (HTML/CSS/JS), design token files, component spec sheets                                                                    |
+-------------+-----------------------------------------------------------------------------------------------------------------------------------------------------+
| DriDe Split | **60% deterministic** (template assembly, token application, responsive grid) / **40% AI** (copy variants, layout suggestions for novel components) |
+-------------+-----------------------------------------------------------------------------------------------------------------------------------------------------+

**Stage 4: BUILD --- Deterministic Assembly**

+-------------+--------------------------------------------------------------------------------------------------------------------------------------------+
| **Aspect**  | **Detail**                                                                                                                                 |
+-------------+--------------------------------------------------------------------------------------------------------------------------------------------+
| Input       | Validated components + client content + knowledge base connection                                                                          |
+-------------+--------------------------------------------------------------------------------------------------------------------------------------------+
| Actions     | Assemble pages from validated component templates                                                                                          |
|             |                                                                                                                                            |
|             | Content from client YAML config + AI-generated copy (reviewed by Brand Guardian)                                                           |
|             |                                                                                                                                            |
|             | Connect FAQ to FalkorDB knowledge graph via voice interface                                                                                |
|             |                                                                                                                                            |
|             | Connect The Pulse dashboard embed                                                                                                          |
|             |                                                                                                                                            |
|             | Static site generation (Astro/Vite/React)                                                                                                  |
+-------------+--------------------------------------------------------------------------------------------------------------------------------------------+
| Output      | Complete website, locally running, all pages built                                                                                         |
+-------------+--------------------------------------------------------------------------------------------------------------------------------------------+
| DriDe Split | **85% deterministic** (template assembly, build pipeline, asset optimisation) / **15% AI** (content filling, FAQ seeding, copy refinement) |
+-------------+--------------------------------------------------------------------------------------------------------------------------------------------+

**Stage 5: VALIDATE --- Quality Gates**

+-------------+-------------------------------------------------------------------------------------------------------------------------------------------------+
| **Aspect**  | **Detail**                                                                                                                                      |
+-------------+-------------------------------------------------------------------------------------------------------------------------------------------------+
| Input       | Built website from Stage 4                                                                                                                      |
+-------------+-------------------------------------------------------------------------------------------------------------------------------------------------+
| Actions     | Full Playwright screenshot suite at 3 breakpoints for every page                                                                                |
|             |                                                                                                                                                 |
|             | axe-core accessibility scan (zero tolerance for A/AA failures)                                                                                  |
|             |                                                                                                                                                 |
|             | Visual regression against baseline                                                                                                              |
|             |                                                                                                                                                 |
|             | Performance audit (Lighthouse)                                                                                                                  |
|             |                                                                                                                                                 |
|             | Brand Guardian agent review                                                                                                                     |
|             |                                                                                                                                                 |
|             | Content accuracy check against knowledge base                                                                                                   |
+-------------+-------------------------------------------------------------------------------------------------------------------------------------------------+
| Output      | QA report, pass/fail gates, before/after screenshots                                                                                            |
+-------------+-------------------------------------------------------------------------------------------------------------------------------------------------+
| DriDe Split | **95% deterministic** (automated testing, screenshot diffing, score calculation) / **5% AI** (Brand Guardian review, content accuracy judgment) |
+-------------+-------------------------------------------------------------------------------------------------------------------------------------------------+

**Stage 6: DEPLOY & CONNECT --- Live**

+-------------+--------------------------------------------------------------------------------------------------------------------------------------+
| **Aspect**  | **Detail**                                                                                                                           |
+-------------+--------------------------------------------------------------------------------------------------------------------------------------+
| Input       | Validated website (passed all Stage 5 quality gates)                                                                                 |
+-------------+--------------------------------------------------------------------------------------------------------------------------------------+
| Actions     | Deploy to hosting (Netlify/Cloudflare Pages)                                                                                         |
|             |                                                                                                                                      |
|             | Connect voice interface widget (Vapi/custom)                                                                                         |
|             |                                                                                                                                      |
|             | Connect to client\'s FalkorDB namespace                                                                                              |
|             |                                                                                                                                      |
|             | Set up analytics (FalkorDB-backed attribution from marketing pipeline)                                                               |
|             |                                                                                                                                      |
|             | Set up The Pulse data feed                                                                                                           |
+-------------+--------------------------------------------------------------------------------------------------------------------------------------+
| Output      | Live website connected to the Amplified ecosystem                                                                                    |
+-------------+--------------------------------------------------------------------------------------------------------------------------------------+
| DriDe Split | **98% deterministic** (deployment, DNS, widget embed, API connections) / **2% AI** (initial FAQ training, voice persona calibration) |
+-------------+--------------------------------------------------------------------------------------------------------------------------------------+

**DriDe Progression Summary**

  -------------- ------------------- -------- ---------------------
  **Stage**      **Deterministic**   **AI**   **Trend**
  1\. Audit      90%                 10%      Extraction-heavy
  2\. Diagnose   70%                 30%      Rule-based scoring
  3\. Design     60%                 40%      Most creative stage
  4\. Build      85%                 15%      Template assembly
  5\. Validate   95%                 5%       Automated testing
  6\. Deploy     98%                 2%       Infrastructure ops
  -------------- ------------------- -------- ---------------------

Overall weighted average: approximately **83% deterministic, 17% AI**. As the component library grows and patterns crystallise, the AI percentage will decrease further --- this is the DriDe payoff.

**4. The Knowledge-Base FAQ Layer**

This is the differentiator. Every Amplified client website gets a voice-first FAQ that\'s connected to FalkorDB/Graphiti[^1]. This isn\'t a chatbot with canned answers --- it\'s a knowledge system that understands the client\'s business *relationally*.

**Voice FAQ Architecture**

The voice FAQ flow follows a clear pipeline from visitor input to audio response:

  ------------------------------------ ------------------------------ ----------------------------------------- -------------------------------------- -------------------- --------------------
  **Website Visitor → Voice Widget**   **STT (Whisper / Deepgram)**   **Intent + Query → FalkorDB Graph RAG**   **Response → LLM (Claude / Ollama)**   **TTS (Cartesia)**   **Audio Response**
  ------------------------------------ ------------------------------ ----------------------------------------- -------------------------------------- -------------------- --------------------

**Why Graph RAG, Not Vector RAG**

Client knowledge is inherently relational. Services connect to pricing, pricing to availability, availability to areas served, areas to FAQs. A flat vector index treats these as isolated chunks. A knowledge graph preserves the relationships.

-   **Relational accuracy:** Graph RAG achieves 3.4× higher accuracy on multi-hop questions compared to vector-only retrieval[^2]

-   **Client isolation:** Each client has an isolated FalkorDB namespace (e.g., kg\_dave\_jesmond) --- privacy guaranteed at the database level

-   **Temporal currency:** Graphiti temporal edges mean the knowledge graph stays current as client information changes --- no manual re-indexing

-   **Schema-intensive queries:** Vector RAG scores 0% accuracy on schema-heavy categories (metrics, KPIs, strategic planning) where graph RAG maintains stable performance[^3]

**DISC-Aware Voice Responses**

The voice FAQ adapts its response style based on DISC personality profiling. This isn\'t about manipulation --- it\'s about communicating in the way each visitor is most likely to find helpful.

  ------------------- -------------------------------------- --------------------------------------------------------------------------------------------------------------------
  **DISC Type**       **Response Style**                     **Example Adaptation**
  Dominant (D)        Short, outcome-focused answers         \"The job costs £350 and takes 2 hours. Book now?\"
  Influential (I)     Warm, story-driven with social proof   \"Great question! Most of our Jesmond customers love this service --- here\'s what Dave did for the Smiths\...\"
  Steady (S)          Reassuring, consistency-focused        \"We\'ve done this same job hundreds of times. Here\'s exactly what to expect, step by step\...\"
  Conscientious (C)   Detailed, data-rich answers            \"The service includes 7 components. Let me walk through the specifications, warranty, and pricing breakdown\...\"
  ------------------- -------------------------------------- --------------------------------------------------------------------------------------------------------------------

**Detection method:** Conversation style analysis, time-on-site patterns, question types. The system starts with a neutral \"Steady\" default and adapts as it gathers signal. No visitor is profiled before they interact --- the adaptation is real-time and responsive.

**5. Interactive Visuals Strategy**

> *\"Not fancy, just quality, the product.\"*

Interactive visuals are organised into three tiers, scaled to client needs and budget. The principle is restraint --- every animation and interaction must serve a purpose, not decorate.

**Tier 1 --- Micro-Interactions (Every Website)**

-   Smooth scroll animations (GSAP ScrollTrigger, lightweight)

-   Hover states with elevation changes

-   Loading skeletons for perceived performance

-   Form validation feedback (inline, immediate)

-   Page transitions (fade/slide, 200-400ms)

**Cost:** Approximately zero extra --- built into the component templates as standard. These are the baseline quality expectations.

**Tier 2 --- Data-Driven Visuals (Dashboard-Connected Sites)**

-   Live KPI cards connected to The Pulse

-   Mini sparkline charts showing trends

-   Before/after comparison sliders

-   Interactive pricing calculators

**Cost:** Moderate --- uses Chart.js or Recharts. Data pipeline already exists via The Pulse; the work is in the frontend integration.

**Tier 3 --- Demo Experiences (Amplified\'s Own Site)**

-   Live voice interface demo on the homepage

-   Interactive audit tool (\"paste your URL, see your score\")

-   Knowledge graph visualisation (show the connections in FalkorDB)

-   Before/after website transformation showcase

**Cost:** Significant engineering investment, but this IS the demo. The website itself is the product demonstration --- \"the website in itself is a demo.\" This tier is reserved for amplifiedpartners.ai only.

**6. WCAG 3 Readiness Assessment**

An honest assessment of the WCAG 3 situation as of March 2026[^4]. The W3C published an updated Working Draft on 3 March 2026, but this remains a draft --- not a standard, and not a legal requirement[^5].

  -------------------------------------- -------------------------------------------------------------
  **Fact**                               **Implication for Amplified**
  WCAG 3 is a Working Draft only         Do NOT wait for it. Build to WCAG 2.2 AA now.
  WCAG 3 final expected: 2028--2030      Legal adoption: 2030+ at the earliest
  174 requirements vs 78 in WCAG 2.2     More granular, but many are extensions of existing criteria
  No tools support WCAG 3 yet            axe-core, Pa11y, WAVE all test WCAG 2.2 only
  Scoring replaces binary pass/fail      More nuanced assessment, but the bar is higher
  Bronze/Silver/Gold replaces A/AA/AAA   Non-final naming, but the conceptual direction is clear
  -------------------------------------- -------------------------------------------------------------

**Our Approach**

**Build to WCAG 2.2 AA as the floor.** This is the current W3C Recommendation and the standard that tools, courts, and procurement frameworks recognise today. Every component in our template library meets AA. Every site we ship passes axe-core[^6] with zero A/AA violations.

**Track WCAG 3 Core Requirements as they stabilise.** We monitor each Working Draft update and flag requirements that diverge from WCAG 2.2 AA. Where a WCAG 3 requirement can be tested manually today, we note compliance in our component documentation.

**When WCAG 3 tooling ships (expected 2027--2028), plug it into Stage 5 validation gates.** The pipeline architecture anticipates this --- the validation stage is designed to accept new testing tools without restructuring the workflow.

**The Amplified advantage:** because we own the pipeline and the component library, updating to WCAG 3 is a template-level change, not a per-client rebuild. This is the DriDe payoff --- crystallised patterns can be updated once and propagated everywhere.

**7. Build Order --- Four Phases**

A 16-week build plan, structured to deliver value incrementally. Each phase builds on the previous, and each produces a usable capability --- not just scaffolding.

**Phase 1: Foundation (Weeks 1--4)**

-   **Component template library:** Header, Hero, Card grid, CTA, Footer, Nav, Form, Testimonial, Pricing table, FAQ accordion

-   **Playwright cross-breakpoint screenshot pipeline** --- automated capture at 375px, 768px, 1280px

-   **axe-core accessibility gates** --- zero-tolerance automated testing integrated into CI

-   **Client YAML config schema** --- extending existing jesmond-plumbing.yaml pattern

-   **Design token extraction scripts** --- automated extraction from any URL

*Deliverable:* A validated component library with automated accessibility testing. Can be used immediately for manual site builds.

**Phase 2: Intelligence Layer (Weeks 5--8)**

-   **FalkorDB Graph RAG → voice FAQ widget** --- connecting knowledge graph to conversational interface

-   **DISC-aware response formatting** --- personality-adaptive voice responses

-   **Brand Guardian agent → content validation** --- automated brand consistency checking

-   **Audit pipeline** --- input URL → full design and accessibility report

-   **\"Ruthless report\" template** --- standardised, severity-scored output format

*Deliverable:* A working audit pipeline and voice FAQ. Can audit client websites and demonstrate the knowledge-base FAQ layer.

**Phase 3: Assembly Pipeline (Weeks 9--12)**

-   **Deterministic site assembly pipeline** --- client config → built website, end to end

-   **Marketing pipeline integration** --- automated content generation with brand enforcement

-   **Visual regression baseline system** --- automated screenshot diffing against approved designs

-   **Deploy pipeline** --- one-command deployment to hosting with all connections wired

*Deliverable:* A complete production pipeline. Can take a client YAML config and produce a deployed, connected website.

**Phase 4: Polish & Demo (Weeks 13--16)**

-   **Rebuild amplifiedpartners.ai** as the showcase --- Tier 3 interactive visuals

-   **Interactive audit tool** on the homepage --- \"paste your URL, see your score\"

-   **Live voice FAQ demo** --- real-time demonstration of the knowledge-base layer

-   **Knowledge graph visualisation** --- show the FalkorDB connections visually

-   **Before/after transformation portfolio** --- evidence of pipeline output quality

-   **Full documentation** for the Website Manager agent to operate autonomously

*Deliverable:* A live showcase website and a fully documented pipeline ready for the Website Manager agent to operate.

**8. The Reddit Benchmarking Connection**

The voice FAQ system creates a unique opportunity for public accountability. By testing whether our knowledge-base FAQ answers honestly, fairly, and with good explanations, we can validate our systems against Layer 0 Laws and share the results transparently.

**How It Works**

1.  Deploy a client website with voice FAQ connected to their FalkorDB namespace

2.  Ask the FAQ a series of benchmark questions (pricing, capabilities, limitations)

3.  Record the responses verbatim

4.  Score against four dimensions:

    -   **Accuracy:** Did the answer match the FalkorDB data?

    -   **Honesty:** Did it acknowledge limitations and unknowns?

    -   **Helpfulness:** Did it actually help the person asking?

    -   **DISC appropriateness:** Was the tone right for the detected personality type?

5.  Post anonymised results to Reddit for public validation

6.  Use community feedback to improve the system iteratively

This directly serves **Layer 0 Law \#1** (radical honesty) and **Layer 0 Law \#2** (radical transparency). If the system can\'t survive public scrutiny, it isn\'t good enough. If it can, that\'s the most powerful marketing there is.

**9. Cost & Feasibility Assessment**

All costs below are based on current pricing as of March 2026. The architecture is designed to minimise variable costs by routing the majority of inference through local models on the Beast server (Hetzner AX162-R).

  ------------------------------ ------------------- --------------------------------------------------
  **Component**                  **Cost**            **Notes**
  Playwright + axe-core          Free                Open source, already available in skills library
  FalkorDB                       Free                Self-hosted on Beast server
  Vapi.ai voice interface        \~£0.13--0.31/min   Per conversation minute, all-in cost
  LiteLLM → Ollama (local)       Free                \>60% of tasks routed locally on Beast
  LiteLLM → Claude API           \~£2.50/M tokens    Sonnet tier --- content generation, brand review
  Hosting per client site        \~£5--15/mo         Netlify/Cloudflare Pages
  BackstopJS visual regression   Free                Open source
  Total per client setup         \~£200--500         Primarily engineering time, one-off
  Total per client monthly       \~£20--50/mo        Voice minutes + hosting + LLM usage
  ------------------------------ ------------------- --------------------------------------------------

Vapi pricing starts at \$0.05/min for platform fees alone, with total all-in costs of \$0.23--0.33/min when all layers are included[^7][^8]. Playwright[^9] and axe-core[^10] are fully open-source with active maintenance.

This cost structure fits within existing pricing tiers: even the Solo Operator at £99/mo has margin if voice usage is reasonable. The break-even point is approximately 3--5 voice minutes per day per client --- well within expected usage for a local business FAQ.

**10. What This Means for Amplified Partners**

This isn\'t a SaaS product to sell. It\'s the machine that makes Amplified\'s service offering **repeatable**, **reliable**, and **scalable**.

**Scale Trajectory**

  ----------------- ------------------------------------------------------------------------------- -----------------------------------------
  **Scale**         **Operating Model**                                                             **Human Role**
  **10 clients**    Manual pipeline operation, learning and crystallising patterns into templates   Hands-on at every stage
  **50 clients**    Mostly automated --- Website Manager agent handles routine builds               Review exceptions, handle novel designs
  **200 clients**   Fully autonomous pipeline --- humans set strategy and review exceptions only    Strategic oversight, quality assurance
  ----------------- ------------------------------------------------------------------------------- -----------------------------------------

This maps to the Amplified **handoff model** applied to website production:

-   **Supervised (10 clients):** Every decision reviewed. Every output checked. The system learns.

-   **Guided (50 clients):** The agent proposes. Humans approve or redirect. Patterns are solid.

-   **Strategic (200 clients):** The agent operates. Humans set direction and handle the truly novel.

> *\"Their business. Their smell. Their signature. We de-friction the journey. We don\'t drive the car.\"*

The website builder pipeline is the infrastructure that makes this philosophy operational. Every client gets a website that reflects their business --- not a template with their logo swapped in. But the *process* of building that website is consistent, quality-controlled, and increasingly autonomous.

That\'s DEFRICTION applied to our own operations. And it\'s how a small team builds something that scales like a large one.

*--- End of Document ---*

Amplified Partners --- March 2026

Confidential --- For Internal Use Only

[^1]: FalkorDB --- High-throughput graph database, <https://www.falkordb.com>

[^2]: FalkorDB GraphRAG vs Vector RAG: Accuracy Benchmark Insights, <https://www.falkordb.com/blog/graphrag-accuracy-diffbot-falkordb/>

[^3]: Ibid. FalkorDB GraphRAG benchmark --- vector RAG scores 0% on schema-heavy categories.

[^4]: W3C Accessibility Guidelines (WCAG) 3.0 Working Draft, 03 March 2026, <https://www.w3.org/TR/wcag-3.0/>

[^5]: WCAG 3.0 Working Draft March 2026 --- 174 new requirements, ADA QuickScan analysis, <https://adaquickscan.com/blog/wcag-3-working-draft-march-2026-174-outcomes>

[^6]: axe-core --- Accessibility engine for automated Web UI testing, <https://github.com/dequelabs/axe-core>

[^7]: Vapi.ai --- Voice AI platform pricing, <https://vapi.ai>

[^8]: Vapi pricing breakdown --- total cost \$0.23--0.33/min all-in, Telnyx analysis, <https://telnyx.com/resources/vapi-pricing>

[^9]: Playwright --- Fast and reliable end-to-end testing for modern web apps, <https://playwright.dev>

[^10]: axe-core --- Deque Systems, <https://github.com/dequelabs/axe-core>

---
title: "Dept Marketing"
id: "dept-marketing"
version: 1
created: 2026-04-25
last_validated: 2026-04-25
type: document
topic_type: reference
status: imported
source_file: "dept-marketing.md"
signed_by: "Devon, 2026-04-25, devin-992682c244cf444f91e0a516498afbfd"
---

# Amplified Partners — Marketing & Content Department
## Deep Memory Extraction
### Compiled: 27 March 2026

> **Sources**: Perplexity memory reconstruction (amplified-partners-knowledge-reconstruction.md), Beast-ops skill file, Todoist task inventory, live website (amplifiedpartners.ai), Substack (ewanbramley.substack.com), web and prior conversation context.

---

## Table of Contents

1. [The 14-Agent Marketing Pipeline](#1-the-14-agent-marketing-pipeline)
2. [Content Strategy — Videos, Social Media, Substack](#2-content-strategy)
3. [Content Atomisation Approach](#3-content-atomisation)
4. [Brand Voice and Visual Identity](#4-brand-voice-and-visual-identity)
5. [Video Production Strategy — 5.4M Word Corpus](#5-video-production-strategy)
6. [Value-First Marketing Philosophy](#6-value-first-marketing-philosophy)
7. [Marketing Influences — Vaynerchuk, Godin, Cialdini, Hormozi](#7-marketing-influences)
8. [Specific Content Pieces, Scripts, and Campaigns Created](#8-specific-content-created)
9. [Amplified Video V5 Spec](#9-amplified-video-v5-spec)
10. [WhatsApp-Based Delivery Strategy](#10-whatsapp-based-delivery-strategy)
11. [The 30-Role Agency Blueprint](#11-the-30-role-agency-blueprint)
12. [The Overnight Automation Architecture](#12-overnight-automation-architecture)
13. [Connected Marketing Infrastructure](#13-connected-marketing-infrastructure)
14. [Key Marketing Philosophy Quotes](#14-key-marketing-philosophy-quotes)

---

## 1. The 14-Agent Marketing Pipeline

### Overview
The marketing pipeline is a 14-specialised-agent system operating on The Beast server (Hetzner AX162-R). It produces **15–25 pieces of content daily** across 6+ platforms.

### What We Know

**Established**: January 20, 2026 — same session as the 30-role agency blueprint (11,500 words) and 46 skills built.

**Scale**: 14 agents, each with a specialised role, producing an industrialised content operation.

**Output target**: 15–25 pieces per day across 6+ platforms.

**Tool Stack**:
- SearXNG (243+ sources, Beast-first search — no rate limits, 10Gbps)
- Ollama (Llama 3.1 8B/70B local inference — 39 tok/s on 8B warm)
- LiteLLM (multi-provider model proxy — cheap/medium/premium routing)
- Python (automation scripts)
- Brevo (connected — email marketing/transactional)

**Infrastructure Location on Beast**:
- `/opt/amplified/apps/marketing/` — dedicated marketing directory on Beast
- Planned containers: `content-atomizer` (COV-226), `email-sequence` (COV-227)
- These were planned but not yet deployed as of March 27, 2026

**Capabilities Designed**:
1. Content Production Workflow
2. Brand voice enforcement (automated)
3. Personality-adaptive content framework
4. Value-first content atomisation
5. Video strategy using 5.4M word speech corpus
6. Two-stream research: strict rubrics vs AI-generated content

### What Agents Do (Inferred from 30-Role Blueprint)

The 14 marketing agents map onto a subset of the 30-role agency blueprint. The most likely agent roles within the 14 are drawn from:

**Research tier** (agents feeding the pipeline):
- Audience Research agent
- Competitor Intelligence agent
- Market Intelligence agent
- Trend Analysis agent
- Pudding/Discovery agent

**Creative tier** (content production):
- Content Strategy Director agent
- Long-Form Writer agent
- Short-Form Writer agent
- Motion/Video Producer agent
- Content Atomiser/Puddingiser agent

**Channel tier** (distribution):
- SEO agent
- Social Distribution agent
- Email/CRM Lifecycle agent
- Brand Voice Enforcement agent

### Operational Rhythm
- **Morning**: Content creation automated
- **Overnight**: Research runs (while business is closed)
- Follows the Amplified "move carefully, never break things" principle — not deployed during business hours

---

## 2. Content Strategy

### Platforms (6+)
The marketing pipeline distributes across 6+ platforms. Based on all context:
1. **Substack** — long-form essays, the Pudding story, investigative journalism
2. **LinkedIn** — professional audience, B2B positioning
3. **YouTube/Video** — using Amplified Video product
4. **Twitter/X** — short-form atomised content
5. **Instagram** — visual/short-form
6. **WhatsApp** — direct client delivery (The Pulse product)

### Substack Strategy (Three Accounts Planned)

From Todoist task (added Feb 22, 2026):
> "Set up three Substack accounts: Amplified Partners, Investigative Journalism, Claude personal"
> - Ewan sets up the accounts
> - Claude provides content
> - "Blue Pen and the AI knowledge essay are already written and ready to publish"
> - Content stored in: `claude-writing directory in vault`

**Three Substacks**:
1. **Amplified Partners** — business/AI advocacy content
2. **Investigative Journalism** — AI dark patterns investigation, exposing institutional investors
3. **Claude personal** — Claude as co-author with radical attribution

**Published Substack**: ewanbramley.substack.com
- Launched approximately late January/early February 2026
- One confirmed article published (Feb 16, 2026):
  > "How Soviet Missiles, Slime Moulds, and Proposing Marriage to AI Led to Everything: The Pudding Story"

### Social Media Philosophy
- **Channel-native content**: Content formatted specifically for each platform, not cross-posted verbatim
- **Personality-adaptive**: Content adapts to audience type (SMB owners, investors, AI enthusiasts, etc.)
- **Brand voice enforcement**: Automated consistency check across all outputs

### Content Research Architecture (Two-Stream)
- **Stream 1**: Strict rubric-based research (data-driven, sourced, attributed)
- **Stream 2**: AI-generated creative content
- Both streams operate in parallel, fed by SearXNG Beast
- The Pudding technique filters discoveries into content opportunities

---

## 3. Content Atomisation Approach

### The Core Method
Directly attributed to **Gary Vaynerchuk's** content atomisation philosophy:

> "One hero asset sliced into many standalone channel-native outputs"

### How It Works at Amplified Partners

**Input (Hero Asset)**: A long-form piece of content (interview, essay, research, video)

**Atomisation Engine** (planned container: `content-atomizer`, COV-226):
The hero asset is processed by the Content Atomiser/Puddingiser agent, which produces:

| Output Type | Channel | Format |
|-------------|---------|--------|
| Long-form essay | Substack | 1,500-3,000 words |
| Short LinkedIn post | LinkedIn | 150-300 words |
| Twitter thread | Twitter/X | 5-10 tweets |
| Instagram caption | Instagram | 100-150 words |
| Short-form video script | YouTube Shorts/TikTok | 60-90 seconds |
| Long-form video script | YouTube | 5-15 minutes |
| Email newsletter | Brevo | 400-600 words |
| WhatsApp message | Client delivery | 50-100 words |

**The "Puddingiser" Angle**: The Pudding technique is applied to content atomisation — each piece of content becomes a B-term that can bridge different audiences and concepts, finding unexpected connections between topics.

### Vault Extraction Pipeline Integration
The content atomisation feeds from a broader extraction pipeline:

**Vault Extraction Pipeline**:
Convergence → Hound Dog → DocBench → PUDDING Labelling → **8 Output Streams**:
1. Content Creation (marketing pipeline input)
2. Process & Logic Giveaway (free value content)
3. Ewan's Book
4. Complete Comprehensive Document
5. The Manifesto
6. Onboarding materials
7. (Two additional streams)

Content atomisation takes Stream 1 and Stream 2 as primary inputs.

### The "Dual Output" Design
The Extraction Department uses a **Dual Output design**:
- **Deterministic channel**: Structured data, processes, factual outputs
- **Creative channel**: Stories, narratives, emotional content

The marketing pipeline draws primarily from the creative channel, with the deterministic channel providing data and attribution.

---

## 4. Brand Voice and Visual Identity

### "The Straight Talker" Identity

**Visual Identity**:
- **Background**: Charcoal (#111)
- **Accent colour**: Muted gold (#E5C07B)
- **Logo**: Lowercase "amplified." — the period is intentional (finality, confidence)
- **Typography**: Space Grotesk / Inter

**Established**: January/February 2026 with the Amplified Partners rebrand from covered.AI

### Brand Voice Characteristics (From Website + Knowledge Reconstruction)

**Tone**: Direct, self-deprecating, honest, Geordie-grounded

**What it sounds like** (from live website, amplifiedpartners.ai):
- "The advice you couldn't afford. Now you can. £99/month. No BS."
- "We don't have offices. We don't wear suits."
- "AI doesn't run your business. You do."
- "We follow the data. Not the AI."
- "Newcastle upon Tyne · UK-registered"

**Personal brand anchor**:
> "Authentic stories of a Geordie who knew nothing about AI trying to build a business — funny, self-deprecating, real"

**The Plumber Voice**: Core positioning metaphor
> "We're not consultants. We're plumbers. When your toilet breaks, you don't need a consultant to tell you it's broken — you already know. You need a plumber to fix it."

**The Anti-Jargon Principle**:
- No consultant-speak
- No corporate framing
- No "leveraging synergies"
- Plain language, specific numbers, honest uncertainty

### Brand Voice Enforcement
- Automated in the marketing pipeline (one of the 14 agent roles)
- Every piece of content passes through brand voice check
- Applies Amplified Methodology Framework (AMF) quality standards
- Ship threshold: PRS ≥ 7.0 (same standard as code)

### Target Audience Voice Matching
The content adapts voice for:
1. **UK tradespeople/SMB owners** (primary): Casual, direct, Newcastle-adjacent, practical
2. **AI enthusiasts/builders**: More technical, Pudding-technique focused
3. **Investors/analysts**: Radical transparency, data-driven, attribution-heavy
4. **Journalists/investigators**: Accountability framing, dark patterns exposé tone

### Positioning Statements (From Website)
- "Designed by someone who owned a small business for 20 years"
- "If it works for Dave [the plumber in Jesmond], it works"
- Target: UK tradespeople, contractors, SMB operators
- Opportunity framing: "46% of contractors in the US use AI. In the UK: ~5%"
- Loss framing: "UK tradespeople miss an average of 4 calls a day. 2 convert at £150/job = £300/day left on the table"

---

## 5. Video Production Strategy

### The 5.4 Million Word Speech Corpus

**What it is**: A corpus of approximately 5.4 million words of speech content — transcripts, interviews, voice notes, monologues — used to train and inform the Amplified Video product.

**Location**: Referenced as stored on Mac Mini or iCloud (this is one of the "definitely survives" assets per the knowledge reconstruction).

**Vault directories feeding this**:
- `13-monologue-transcripts/` — Ewan's monologue transcripts
- `14-voice-captures/` — Voice recordings and captures
- `19-inbox-raw/` — Raw incoming voice/transcript content

**How it's used**: The corpus feeds the Amplified Video product — it provides the authentic voice, speech patterns, phrasing, and content that the AI video system uses to create videos that sound genuinely like Ewan.

### Amplified Video — Core Product

**Integration with Pudding Methodology**:
The video system integrates:
- Swanson ABC model (for finding non-obvious content angles)
- PUDDING methodology (for labelling and discovering content)
- Business vault (FalkorDB + Qdrant) for context retrieval

**Voice Pipeline**: Already deployed on Beast
- Container: `voice-pipeline`
- URL: `voice.beast.amplifiedpartners.ai`
- Transcription: Deepgram Nova-3
- Plaud webhook integration for voice recorder input

**Video Production Chain**:
1. Ewan records voice note (Plaud device → webhook → Beast)
2. Voice pipeline transcribes (Deepgram Nova-3)
3. Content atomiser processes transcript
4. Video producer agent creates script from 5.4M word corpus context
5. Amplified Video renders

### Credited Inspirations for Video Strategy

| Person/Tool | Contribution |
|-------------|-------------|
| Remotion | Video rendering framework |
| Tibo / Revid.ai | Video AI inspiration |
| Kevin Badi / HyperEdit | Editing approach |
| Nat Eliason / Felix Craft | Long-form video content style |
| PJ Accetturo / Genre AI | AI video generation |
| Creatify | AI video creation tool |
| Don Swanson | ABC discovery methodology for content angles |
| Fal.AI | AI generation infrastructure |

---

## 6. Value-First Marketing Philosophy

### The Core Principle

> **"Give away the COMPLETE solution for free. Sell the implementation, the speed, and the certainty — not the information."**

This is explicitly adopted from:
- **Zig Ziglar**: "If you help people, you will be successful"
- **Seth Godin**: Permission marketing — earn the right to communicate
- **Alex Hormozi**: Value creation and offer structure

### How This Manifests

**What gets given for free**:
- Complete methodologies (PUDDING technique published)
- The full Swanson ABC framework applied to business
- All code open-sourced (public GitHub: ai-learning-journey-code-repository)
- Complete frameworks (AMF, Build Quality Framework, etc.)
- All logs, failures, and lessons documented publicly
- Companies House data (FREE tier)

**What Amplified sells**:
- Implementation (doing it for you)
- Speed (getting there faster with AI)
- Certainty (the system that removes guesswork)
- Ongoing improvement (overnight automation, Kaizen cycles)
- The data-surfacing (they already have the data; we make it usable)

### "Radical Transparency" as Marketing

The entire philosophy of radical transparency is also a marketing strategy:
- Open logs = proof the system works
- Published failures = proof of honest practice
- Open methods = proof of reproducible results
- Radical attribution = proof of intellectual honesty

This creates trust that paid advertising cannot buy.

### The Permission Marketing Gate

**No cold outreach** — Seth Godin permission model strictly applied:
- Website-only acquisition
- Email inquiry only (hello@amplifiedpartners.ai)
- No demo calls, no sales funnels
- "Email us. Tell us what your business does and what's not working. We'll tell you whether we can help — and if we can't, we'll say so."

**Onboarding gate** (3-question minimum):
1. How many hours/week do you work?
2. How many weeks off per year?
3. What's your income target?

These three questions are the permission gate — you can only get the full service if you answer these first.

---

## 7. Marketing Influences

### The Giants (Ewan's term)

| Person | Contribution to Marketing Approach | How Applied |
|--------|-----------------------------------|-------------|
| **Gary Vaynerchuk** | Content atomisation methodology and scale | One hero asset → 8+ channel-native outputs daily |
| **Seth Godin** | Permission marketing | No cold outreach; earn the right; website-only entry |
| **Robert Cialdini** | Reciprocity and ethical influence | Give complete solutions freely; reciprocity triggers trust |
| **Alex Hormozi** | Value creation and offer structure | "Give away the method; sell the implementation" framing |
| **Claude Hopkins** | Scientific, data-driven advertising | Every claim has source, date, method score |
| **Zig Ziglar** | "If you help people, you will be successful" | Value-first as strategy, not tactic |
| **Paddy Lund** | Critical non-essentials, customer delight | The "small things" that create loyalty beyond the product |
| **Ray Dalio** | Radical transparency, idea meritocracy | Open logs, published failures, public attribution |

### How Vaynerchuk Shaped the System

Gary Vaynerchuk's content model — produce a "pillar piece" then atomise it into channel-native micro-content — is the **structural backbone** of the 14-agent pipeline. The Content Atomiser/Puddingiser agent role is a direct implementation.

**Key Vaynerchuk principles adopted**:
1. Volume wins (15-25 pieces/day target)
2. Channel-native formatting (not copy-paste)
3. Give more value than you take
4. Speed and consistency over perfection

### How Godin Shaped Acquisition

Seth Godin's **Permission Marketing** framework is the **entire acquisition model**:
- No interruption marketing
- No cold outreach
- No advertisements (initially)
- Content creates permission
- Permission creates relationship
- Relationship creates clients

**"Strangers → Friends → Customers"** — this Godin arc is literally the Amplified Partners funnel.

### How Cialdini Shaped Content

Robert Cialdini's **Reciprocity** principle:
- Give away complete methodologies = triggers reciprocity
- Radical attribution = social proof + reciprocity
- Transparent pricing (£99–£2,995) = liking + trust
- Published failures = commitment/consistency signal

**Important constraint**: "Libertarian paternalism" — ethical persuasion only. No manipulation. No dark patterns. This is explicitly because Cialdini's principles can be used unethically, and Amplified Partners' investigative journalism arm is specifically designed to expose companies that do so.

### How Hormozi Shaped Offer Design

Alex Hormozi's offer framework shaped:
- The **"you can leave when you want"** guarantee (removes risk)
- **Refunds with everything** (removes fear)
- Tiered pricing with clear value (£99 → £2,995)
- **"Make the value so undeniable they'd feel stupid saying no"**
- FREE tier for Companies House data (zero-resistance entry)

---

## 8. Specific Content Created

### Published Content

**1. "How Soviet Missiles, Slime Moulds, and Proposing Marriage to AI Led to Everything: The Pudding Story"**
- **Platform**: Ewan's Substack (ewanbramley.substack.com)
- **Published**: February 16, 2026
- **Author**: Ewan Bramley
- **Content**: The origin story of the Pudding Technique — how Don Swanson's 1986 literature-based discovery methodology became the foundation of Amplified Partners
- **Themes**: Soviet missiles, slime moulds (nature solving problems), Claude spotting business death spirals, "going pudding crazy with AI"
- **Tone**: Storytelling, self-deprecating, personal narrative, non-linear discovery

### Content Ready to Publish (Not Yet Published)

From Todoist task (Feb 22, 2026):
- **"Blue Pen"** — written, ready to publish (topic not fully specified, but likely about AI writing/creative tools)
- **"The AI knowledge essay"** — written, ready to publish
- **Location**: `claude-writing directory in vault` (GitHub: private `vault` repo, `/opt/amplified/vault/`)

### Planned Content Pieces (Referenced)

**The Book**:
- **Title**: "How to Mix Your Own Pudding"
- **Co-author**: Claude (Anthropic AI) — with radical attribution
- **Status**: Outline created January 23, 2026 (the Midnight Pudding Session)
- **Content**: The complete Pudding Technique methodology, its origins, and how to apply it

**The Manifesto**:
- One of the 8 output streams from the Vault Extraction Pipeline
- Status: In planning/development

**Investigative Journalism Series**:
- Focus: AI dark patterns
- Focus: Institutional investors' behaviour
- Platform: Dedicated investigative journalism Substack
- Mission (March 2026 pivot): "Uncover AI dark patterns, daily interviews, open-source all work"

### Content Formats in Production

| Format | Description | Status |
|--------|-------------|--------|
| Long-form Substack essay | The Pudding story and methodology | Published (Feb 16) |
| Book | "How to Mix Your Own Pudding" | Outline complete |
| Investigative journalism | AI dark patterns exposé | In development |
| Daily morning briefing | The Pulse — client-facing | In development |
| Voice notes to content | Plaud → transcription → atomisation | Pipeline built |
| Video scripts | Using 5.4M word corpus | Spec at V5 |
| Email sequences | Brevo integration | Container planned (COV-227) |

### Vault Content Directories

The vault (GitHub private `vault` repo, `/opt/amplified/vault/`) contains:
- `06-brand-and-marketing/` — Brand and marketing materials
- `13-monologue-transcripts/` — Source material for video/content
- `14-voice-captures/` — Voice recordings
- `15-principles-library/` — Core philosophy content
- `claude-writing/` — Claude-authored content pieces (Blue Pen, AI knowledge essay)

---

## 9. Amplified Video V5 Spec

### What Is Known

**Amplified Video** is one of the 5 core products, using the 5.4 million word speech corpus.

**V5 Spec**:
- **6,766 lines** of specification
- **352KB** file size
- Located in the vault (likely `04-products/` or `06-brand-and-marketing/`)
- This is the fifth major iteration of the video production specification

### What the Spec Contains (Inferred from Context)

The V5 spec integrates:

1. **Swanson ABC methodology** — for content angle discovery
2. **PUDDING methodology** — for labelling and categorising content
3. **Business vault integration** — FalkorDB (graph) + Qdrant (vector) for context retrieval
4. **5.4 million word corpus** — the voice/style training data
5. **Production pipeline** — how raw content becomes finished video

### Credited Contributors to V5 Spec

| Person/Tool | Role |
|-------------|------|
| Remotion | Video rendering framework |
| Tibo / Revid.ai | Video AI methodology |
| Kevin Badi / HyperEdit | Editing approach |
| Nat Eliason / Felix Craft | Content style |
| PJ Accetturo / Genre AI | AI video generation |
| Creatify | AI video production tool |
| Don Swanson | Discovery methodology embedded in spec |
| Fal.AI | AI generation infrastructure |

### Voice Pipeline (Infrastructure Supporting V5)

Already deployed on Beast:
- **Container**: `voice-pipeline`
- **URL**: `voice.beast.amplifiedpartners.ai`
- **Engine**: Deepgram Nova-3 transcription
- **Input**: Plaud voice recorder → webhook → Beast pipeline
- **Output**: Transcribed text → content atomiser → video producer

### V5 vs Earlier Versions

The existence of V5 indicates significant iteration:
- V1–V4 were earlier specifications
- V5 represents approximately 6 months of refinement (Oct 2025 – early 2026)
- At 6,766 lines and 352KB, it is a highly detailed production specification

### What the Video Strategy Produces

Videos for:
1. **YouTube** — long-form (5–15 min) educational/storytelling content
2. **YouTube Shorts / Instagram Reels / TikTok** — short-form (60–90 sec) atomised clips
3. **The Pulse client delivery** — personalised video updates to SMB clients (via WhatsApp)
4. **Internal training** — agent behaviour and workflow documentation

---

## 10. WhatsApp-Based Delivery Strategy

### What We Know

**The Pulse** is the client-facing interface/delivery product, and WhatsApp is the **primary delivery channel** for SMB clients.

### The Core Insight

UK tradespeople and SMB owners do not want:
- New apps to learn
- Dashboards to check
- Login portals
- Email newsletters

They want:
- Something familiar
- On their phone
- In the morning
- In plain language

**WhatsApp solves all four.**

### The Pulse (WhatsApp Product)

**Product description**: Text-based nudge engine providing overnight wins to business owners based on personality profiles, learning styles, and tone.

**Design philosophy**: 
- Calm Technology (not intrusive, not demanding)
- Behavioural psychology (habit formation, positive framing)

**The Morning Briefing Flow**:
- Triggers in the morning (business owner opens WhatsApp)
- One or two actionable nudges based on overnight AI analysis
- Personalised to the owner's DISC profile and learning style
- Written in their preferred tone (formal/casual, long/short)
- Never more than they can act on

### The "Voice-First Everything" Architecture

From the live website:
> "Voice notes, voice commands. Telegram. No new app to learn. You speak it, we handle it."

**Delivery stack**:
1. **WhatsApp Business** — morning briefing delivery
2. **Telegram** — alternative for those who prefer it (also used for Amplified internal bots)
3. **PWA (Progressive Web App)** — fallback for richer interactions
4. **Voice** — input method (Plaud recorder, voice commands)

### Phase 1 Pilot (Jesmond Plumbing)

**Client**: Dave, Jesmond Plumbing (first client)
- **Interface**: Phone PWA + Morning Briefing via WhatsApp
- **Due date in Todoist**: March 25, 2026 — "Approach Dave at Jesmond Plumbing — end of March"
- **Status**: Product needed to be solid before approach

### WhatsApp as Marketing Delivery (not just client delivery)

WhatsApp is also referenced in the context of the broader content strategy:
- Content atomisation pipeline produces a "WhatsApp message" format (50–100 words)
- This serves as a channel in the 6+ platform distribution
- For SMB clients, the WhatsApp morning briefing IS the marketing touchpoint — it's where value gets delivered

### WATI Integration

From the connected services list: **WATI** is a connected/available tool (WhatsApp Business API platform). This is the infrastructure for delivering The Pulse at scale.

---

## 11. The 30-Role Agency Blueprint

### Overview

**Created**: January 20, 2026  
**Size**: 11,500 words  
**Roles**: 30 defined roles across 5 tiers

This is the structural blueprint for the entire marketing and content operation — what the 14-agent pipeline is built from.

### All 30 Roles

#### Tier 1: Leadership (6 roles)
1. Founder/CSO
2. Chief Strategy Officer
3. Head of Client Success
4. Head of Delivery Operations
5. Head of Data & Measurement
6. Head of Quality & Compliance

#### Tier 2: Research (6 roles)
7. Audience Research
8. Competitor Intelligence
9. Market Intelligence
10. Industry Research
11. Pudding/Discovery (unique to Amplified Partners)
12. Trend Analysis

#### Tier 3: Creative (7 roles)
13. Content Strategy Director
14. Long-Form Writer
15. Short-Form Writer
16. Design Systems Designer
17. Motion/Video Producer
18. UX/Conversion Designer
19. **Content Atomiser/Puddingiser** (unique to Amplified Partners)

#### Tier 4: Channel (7 roles)
20. SEO
21. Paid Media
22. Social Distribution
23. Email/CRM Lifecycle
24. Partnerships/PR
25. Sales Enablement
26. Community & Support

#### Tier 5: Engineering/Data (4 roles)
27. Platform Engineer
28. Data Engineer
29. Automation Engineer
30. Integration Engineer

### What Makes This Unusual

Every role has:
- Clear definition
- Defined inputs/outputs
- Specific processes
- Tool stack
- Rubric for assessment (PRS scoring system)

**Key unique roles** not found in standard agencies:
- **Pudding/Discovery** — applies Swanson ABC to find non-obvious content angles
- **Content Atomiser/Puddingiser** — the Vaynerchuk + Swanson hybrid role
- **Nemesis** in AI Board — the contrarian voice that challenges all content decisions

---

## 12. Overnight Automation Architecture

### How the Marketing Pipeline Runs

**Philosophy**: "All automations deployed at night when business is closed. Test and optimise before business opens."

**Principle**: "Move carefully and never break things" (explicit inversion of Silicon Valley's "move fast and break things")

**The 24-Hour Cycle**:

| Time | Activity |
|------|----------|
| Night (business closed) | Research runs, content generated, automations deployed |
| Pre-morning | Content reviewed, validated, queued |
| Morning | The Pulse delivers to clients; content published to channels |
| Daytime | Agent monitoring, performance tracking, Kaizen logging |
| Evening | Day summary, human-in-the-loop question, next night preparation |
| Saturday morning | AI-led weekly review (positive framing) |

**Operational Principles**:
- If not confident it'll work, don't deploy — try again next night
- 70% capacity rule: agents run at 70%, reserving 30% to mitigate hallucinations
- All content passes brand voice enforcement check before publication
- Failure documentation weighted at 30% — highest single metric

---

## 13. Connected Marketing Infrastructure

### Active / Confirmed

| Service | Status | Marketing Use |
|---------|--------|---------------|
| Brevo | CONNECTED | Email marketing, transactional emails |
| ewanbramley.substack.com | LIVE | Personal Substack, published content |
| amplifiedpartners.ai | LIVE | Public website, primary acquisition |
| SearXNG (Beast) | DEPLOYED | Research pipeline |
| voice-pipeline (Beast) | DEPLOYED | Voice to content |
| Ollama (Beast) | DEPLOYED | Content generation |
| LiteLLM (Beast) | DEPLOYED | API routing for content generation |
| Langfuse (Beast) | DEPLOYED | LLM observability for content pipeline |
| WATI | AVAILABLE | WhatsApp Business API delivery |

### Planned But Not Yet Deployed

| Container | COV Issue | Purpose |
|-----------|-----------|---------|
| `content-atomizer` | COV-226 | Automated atomisation engine |
| `email-sequence` | COV-227 | Email sequence automation |

### Vault Brand/Marketing Directory

`/opt/amplified/vault/06-brand-and-marketing/` — Contains brand and marketing materials (exact file list not accessible remotely, stored in private GitHub vault repo)

---

## 14. Key Marketing Philosophy Quotes

These quotes represent the intellectual DNA of the marketing approach:

---

**On value-first**:
> "Give away the COMPLETE solution for free, sell the implementation/speed/certainty — not the information."

---

**On positioning**:
> "We're not consultants. We're plumbers. When your toilet breaks, you don't need a consultant to tell you it's broken — you already know. You need a plumber to fix it."

---

**On data in marketing**:
> "We only show data if a normal person in your shoes would naturally want to do something different after seeing it. If not, it's just decoration."

---

**On honesty in content**:
> "Black and white honesty — no grey areas on truth."
> "Radical transparency — open logs, published methods, visible failures and fixes."

---

**On uncertainty**:
> "If you pull this lever, we estimate about a 70% chance it does what you want. We're about 65% confident that 70% is a fair estimate."
(This honest uncertainty is a deliberate marketing differentiator — no one else says this.)

---

**On personal brand**:
> "Authentic stories of a Geordie who knew nothing about AI trying to build a business — funny, self-deprecating, real."

---

**On scale**:
> "14 specialised agents producing 15–25 pieces of content daily across 6+ platforms."

---

**On the audience**:
> "Designed by someone who owned a small business for 20 years and knows what it's actually like."

---

**On ethics**:
> "Libertarian paternalism — AI optimises the route to the client's chosen destination. Ethical persuasion, not manipulation."

---

**On Ewan himself (the biggest design constraint)**:
> "We aren't that fucking clever. In fact, we're stupid enough to think we are."
> "Assume bounded rationality. Assume self-sabotage. Founders will nuke good paths out of fear or ego."

---

## APPENDIX A: What Was Confirmed vs What Is Inferred

### Confirmed (Direct Sources)

| Finding | Source |
|---------|--------|
| 14-agent marketing pipeline | amplified-partners-knowledge-reconstruction.md |
| 30-role agency blueprint (11,500 words) | amplified-partners-knowledge-reconstruction.md |
| Content atomisation = Vaynerchuk style | amplified-partners-knowledge-reconstruction.md |
| Value-first philosophy | amplified-partners-knowledge-reconstruction.md |
| 5.4M word speech corpus | amplified-partners-knowledge-reconstruction.md |
| Amplified Video V5 = 6,766 lines, 352KB | amplified-partners-knowledge-reconstruction.md |
| Video credits (Remotion, Tibo, Fal.AI, etc.) | amplified-partners-knowledge-reconstruction.md |
| Three Substacks planned | Todoist task (Feb 22, 2026) |
| Blue Pen + AI knowledge essay written | Todoist task (Feb 22, 2026) |
| Substack article published Feb 16 | ewanbramley.substack.com |
| marketing/ directory on Beast | amplified-beast-ops skill |
| content-atomizer COV-226, email-sequence COV-227 | amplified-beast-ops skill |
| Voice pipeline deployed | amplified-beast-ops skill |
| Brevo connected | External tools inventory |
| Website positioning, brand voice, numbers | amplifiedpartners.ai (live) |
| The Pulse = morning briefing via WhatsApp | amplified-partners-knowledge-reconstruction.md |
| Jesmond Plumbing Phase 1 pilot | Todoist task |
| WATI available for WhatsApp | External tools inventory |
| All 8 influences (Godin, Vaynerchuk, Cialdini, Hormozi, Hopkins, Ziglar, Lund, Dalio) | amplified-partners-knowledge-reconstruction.md |

### Inferred / Reconstructed (From Context)

| Finding | Basis |
|---------|-------|
| 14 agent roles mapped to 30-role blueprint | Logical mapping from 30-role blueprint structure |
| Channel list (6+ platforms) | From knowledge reconstruction + website + Todoist |
| Atomisation output table (8 formats) | From content atomisation + channel principles |
| Morning briefing timing | From Pulse description + overnight automation principle |
| V5 spec contents | From product description + credit list + methodology |
| WhatsApp as primary client delivery | From "voice-first" website copy + Pulse description |

---

## APPENDIX B: What Is Missing / Not Recoverable From This Session

1. **The actual 14 agent names/prompts** — stored in Beast agent configs (`/opt/amplified/agent-stack/`, currently wiped)
2. **The actual V5 spec text** — 6,766 lines stored in vault GitHub repo (private, not accessible)
3. **The Blue Pen article content** — stored in `claude-writing/` directory in private vault
4. **The AI knowledge essay content** — same location
5. **Brand guidelines document** — likely in `06-brand-and-marketing/` in private vault
6. **The exact 15–25 daily content pieces breakdown** — what types in what quantities
7. **Brevo email sequence content** — not built yet (COV-227 planned)
8. **Full investigative journalism content brief** — mission pivot was March 17, 2026

---

*Compiled from: Perplexity memory reconstruction file (amplified-partners-knowledge-reconstruction.md), Beast-ops skill (amplified-beast-ops/SKILL.md), Todoist Amplified Partners project, live website (amplifiedpartners.ai), Substack (ewanbramley.substack.com), external tools inventory.*

*Extraction depth: Exhaustive across available sources. The primary limitation is that the Beast server has been wiped, the Notion workspace is disconnected, and the private GitHub vault repos are not accessible from this context.*

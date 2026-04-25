---
title: "Ewan Bramley Profile"
id: "ewan-bramley-profile"
version: 1
created: 2026-04-25
last_validated: 2026-04-25
type: document
topic_type: reference
status: imported
source_file: "ewan-bramley-comprehensive-profile.md"
signed_by: "Devon, 2026-04-25, devin-992682c244cf444f91e0a516498afbfd"
---

# Comprehensive Profile: Ewan Bramley
## Full Memory System Retrieval — March 2026

---

## 1. PERSONAL IDENTITY & BIOGRAPHY

### Core Identity
- **Full Name:** Ewan Bramley
- **Date of Birth:** 19 May 1973 (age 52)
- **Height:** 5'11" (180 cm)
- **Weight:** 83 kg
- **Location:** 204 Jesmond Dene Road, NE2, Newcastle upon Tyne, England
- **Languages:** English (strong Geordie/Newcastle accent — noted as requiring a "pre-Cove translator" pattern for AI voice processing)
- **Marital History:** At least one ex-wife (referred to as "first ex-wife"), which he references in the context of past ego-driven mistakes he intends to publicly own
- **Email accounts:**
  - **Primary:** ewan@bykerbusinesshelp.ai (Google Workspace)
  - **Previous business:** ewan@ewanbramley.com
  - **Personal:** bramley@gmail.com
  - All configured to forward to the primary Workspace account
- **Currency:** Works in GBP
- **Uses a Chromebook** (alongside Mac Mini and other devices)

### Previous Career
- **Profession:** Dentist for 28–30 years
- **Practice:** Built a dental practice to £2M+ annual revenue with 30+ staff
- **Practice sold:** March 2025
- **Sales record:** Sold £30,000 worth of treatments personally — describes himself as "the best salesman in the practice"
- **Self-diagnosis from E-Myth framework:** "I was the worker IN, not the worker ON" — the technician trapped doing the work instead of building the machine
- **Key takeaway from this period:** Deep empathy for what it means to run a small business — the exhaustion, the peripheral admin that kills passion, the toll on personal life and health. "It killed me." This lived experience is the emotional and philosophical bedrock of everything he's building now.
- **Relevant skills from dentistry:** Hands-on experience with 3D printing and injection molding; understanding of high tooling costs; 28 years of consultative B2B sales training; managing staff, patients, compliance, and operations
- **Owns multiple limited companies** (25+ years of business ownership)

---

## 2. PROFESSIONAL LIFE — AMPLIFIED PARTNERS

### Company
- **Name:** Amplified Partners (www.amplifiedpartners.ai)
- **Website hosting:** Netlify (via AWS Global Accelerator, IP 75.2.60.5), GitHub repo ewan-dot/amplified-site (Vite, React, TypeScript)
- **Previous/parallel brand:** Byker Business Help (bykerbusinesshelp.ai) — hosted on Namecheap shared hosting (Amsterdam NL), LiteSpeed, managed via cPanel
- **Earlier business name:** BaseLayer (AI voice receptionist for service businesses) — predates Amplified Partners branding
- **Tagline:** "You with AI equals Amplified"
- **Extended tagline:** "You with AI: amplified, not exterminated"
- **Ewan's self-described role:** "To contribute creativeness while AI agents handle day-to-day operations to help people"

### Mission: DEFRICTION
The core mission is removing every friction point from small to medium businesses so owners and staff can reconnect with their passion, align with life goals, and reclaim their time. This is supported by a critical data extraction engine that captures data from messy systems (emails, WhatsApp, files) to ensure all improvements are data-led, benchmarked, and continuously improved via Kaizen methodology.

### Target Market
- UK SMBs (£0.5M–£3M revenue)
- Dentists, vets, hairdressers, trades, plumbers, electricians, HVAC, landscaping
- Solo tradespeople to medium-sized businesses
- Particular empathy for single-handed tradespeople and their partners

### Pricing Tiers (6 tiers)
| Tier | Price | Description |
|------|-------|-------------|
| FREE | £0 | Companies House data |
| Solo Operator | £99/mo | Phone-based |
| Small Business Phone | £295/mo | Phone-based with voice |
| Small Business IT | £595/mo | Full IT integration |
| Medium Business | £1,595/mo | Expanded |
| Large Business | £2,995/mo | Full suite |

### First Client / Pilot
- **Jesmond Plumbing** — owner named Dave
- Deadline was 25 March 2026
- Requires Xero OAuth connection, dashboard, content running
- Phase 1 pilot of "The Pulse" interface with Phone PWA and Morning Briefing feature

### Client Interface: The Pulse
- Daily briefing flow ("Morning") for business owners
- Design philosophy based on Calm Technology and behavioral psychology
- Text-based nudge engine providing overnight wins based on personality profiles, learning styles, and tone
- Builds trust through demonstrated competence, acting as a business partner rather than a tool

### Client Onboarding Process
- Mandatory 3-question interview gate: hours/week, weeks off/year, income target
- Higher-tier clients: 10–15 questions plus DISC profiling
- Philosophy: libertarian paternalism — AI optimizes the route to the client's chosen destination
- Permission-only approach (no meetings/calls initially)
- Silent overnight security deployment
- Client-defined vocabulary: "What words do YOU use?" rather than imposing jargon

### Staff Onboarding Philosophy
- Layered interview process with permission gates at each level
- Each layer requires fresh consent
- Questions focus on "what causes your problems" or "what are you interested in" rather than corporate framing
- 8 steps for building trust: emotional reset, role-specific demo, privacy guarantees, direct value proposition, shared benefit alignment, transparent business integration, no-oversell honesty, gentle forward sell
- Specific script acknowledging staff frustration with "new things" causing more work
- All future skill-building and content creation positioned as optional, fun, and easy
- Training delivered only to employees' personal phones for privacy
- Access uses a four-word identifier
- Employees voluntarily choose to disclose training results
- Delivered via Remotion videos using behavioral psychology, personalized to individual's pace, language, and learning style

### Communication Philosophy for Staff
- Avoids loaded terms like "manipulation," preferring "communication techniques"
- Frames removal of tedious tasks as enabling more meaningful contributions
- Positive-negative-positive framing, never negative
- Staff benefit more from the AI partnership than the business itself
- Contractual requirement: no redundancies within a year — will not sign with partners who refuse this

### Client Data Philosophy
- "We give them what is theirs" — enforces data ownership, not hostage-taking
- Clients can leave at any time, take all data with them
- Data exported in open, portable formats
- "If we're shit or you don't like the smell of us, you don't pay for that period"
- Business insights delivered as aggregated patterns, never individual judgments

---

## 3. TECHNICAL INFRASTRUCTURE

### The Beast (Primary Server)
- **Hardware:** Hetzner AX162-R dedicated server
- **Specs:** 48-core EPYC, 256GB RAM, 10 Gbit pipe
- **Location:** Germany (GDPR compliant)
- **Containers:** 29–36+ Docker containers running behind Traefik with auto-TLS
- **Services include:** PostgreSQL, Redis, FalkorDB, Ollama (qwen3-coder:30b, llama3.1:70b, llama3.1:8b, nomic-embed-text), Traefik, Qdrant, SearXNG, Cove code factory, Temporal, Langfuse, and many more
- **Cost saving:** Migrated off Railway to save $400–600/month (Railway to Beast Migration Runbook v1.0, created 14 March 2026)

### Full Hardware Inventory (5 devices)
1. **The Beast** — Hetzner AX162-R (primary server)
2. **Mac Mini** — primary local development machine
3. **MacBook Air M4** — under repair at time of recording
4. **Beelink N150** — mini PC
5. **iPhone 16** — mobile

System and tool parity maintained across all devices. Syncthing used for distributed vault sync with custom ingestion pipeline on Beast.

### The Vault
- Defined as the live FalkorDB, Graphiti, and Qdrant databases on the Beast (NOT file system directories)
- 4,787 files across 25 directories
- 3.3M words on Beast (5.4M including all sources)
- As of March 2026: only 327 of 4,664 files ingested into FalkorDB (7% — identified as a critical gap)

### Business Vault Architecture
- Each client gets their own "business brain"
- Integrates FalkorDB (graph database), Qdrant (vector database), and underlying SQL database
- Data sovereignty as core principle — single source of truth for procedures and documentation
- Human escalation for AI-determined gaps

### Cove Code Factory
- Strategy: assemble pre-built, vetted open-source components from GitHub instead of writing from scratch
- Target stack: APIs, MCP servers, MCPipe/UnixPipe, SQL databases, LangGraph for agentic workflows
- All code must be deterministic, privacy-first, security-accredited (Cyber Essentials target)
- Privacy-first P2 tokenization
- Current projects: IT infrastructure forensic interrogation tools, fully automated digital marketing system

### Security Architecture
- 37-page beast-security-architecture-v2.pdf (v2.0)
- 10-layer defense-in-depth framework
- Vaultwarden (self-hosted) for passwords and passkeys
- Infisical (self-hosted) for machine secrets, replacing .env files
- SPF/DMARC records pending for amplifiedpartners.ai and bykerbusinesshelp.ai
- Targeting Cyber Essentials certification (£320–600, self-assessment)
- Annual external pentesting planned (Cure53 or Radically Open Security)

### Amplified Watchman
- Unified read-only observability layer for existing monitoring infrastructure
- Integrates SigNoz or Grafana, Qwen 2.5 Coder 7B/14B for local code review, promptfoo for LLM output validation, SonarQube and Semgrep for SAST

### Web Hosting
- amplifiedpartners.ai: Netlify (AWS Global Accelerator, IP 75.2.60.5)
- bykerbusinesshelp.ai: Namecheap shared hosting (server705-4.web-hosting.com, IP 198.177.120.182, Amsterdam NL), LiteSpeed, cPanel
- Ollama: ollama.beast.amplifiedpartners.ai (port 11434 behind Traefik)

---

## 4. AI AGENT ARCHITECTURE

### AI Board Governance Architecture (March 2026)
- **5-seat AI Board:**
  - Claude Opus — CEO
  - Llama 70B local — COO
  - GPT-4.1-mini — CFO
  - Claude Sonnet — CTO
  - Gemini Pro — Nemesis (adversarial/challenger role)
- **Facilitator:** Llama 3.1:8b
- **Voting:** Believability-weighted with 90-day rolling gates
- Applied to 14-agent marketing pipeline

### Agent Teams
- Parallel AI agent architecture with four teams of four agents: Enforcer, Builder, Security, overseen by team orchestrator and overall Enforcer
- Safety loop: agent council for edge cases → Claude/LLM escalation → business owner as endpoint
- 10 specialized Enforcers: Label, Citation, Compression, Deduplication, Attribution, Interface, Security, Rubric, Training, Extraction

### 24-Hour Operation Cycle
- Chaos testing: 01:00–04:00
- Kaizen cycle: 03:00
- Ewan's morning review: 06:00–06:30 (targeting 60 min/day total by Month 4)
- Agents run continuously

### "Office of National Statistics" Department
- Internal department within Amplified Partners for autonomous pattern detection on client data
- 3-layer architecture: clean data → AI-driven pattern detection → actionable insights with proof
- Integrates Comet Opik to measure and optimize Kaizen AI performance

---

## 5. CURRENT PROJECTS

### Amplified Video
- Using 5.4 million word graffiti/file code DB with speech transcripts
- AI agents process content from conversations and stories to create videos
- V5 spec completed 15 March 2026: 6,766 lines, 352KB
- Key features: Swanson ABC integration in Director Agent, PUDDING 2026 methodology, business vault integration, Drizzle schema with 18+ tables
- Credits 12 industry leaders: Remotion, Tibo/Revid.ai, Kevin Badi/HyperEdit, Nat Eliason/Felix Craft, PJ Accetturo/Genre AI, Creatify, Don Swanson, Fal.AI
- Named agents: Director, DiCaprio (performance), Picasso (visual), Kaizen (methodology)

### The Pudding Technique
- Based on Don Swanson's "Undiscovered Public Knowledge" (1986) — Literature-Based Discovery (LBD)
- ABC model: if A affects B in one domain and B affects C in another, there's a hidden A→C connection
- Famous example: fish oil → blood viscosity → Raynaud's disease
- Ewan's adaptation: cross-domain business knowledge synthesis using AI
- Gamification: 7-day streak from "tiny haggis" to "Great Chieftain of the Pudding Race"; missed days deflate one stage (humorous shame, not punitive reset)
- Holds deep personal significance — represents the early AI collaboration with Claude that shaped his entire approach
- PUDDING 2026 labelling: WHAT.HOW.SCALE.TIME
- 4-criteria rubric, biological decision logic taxonomy, Radical Attribution schema
- APDS (Amplified Pudding Discovery System): 27-page spec, 5-stage pipeline (Harvest → Extract → Label → Match → Score & Surface), 12-week implementation
- PUDDING Operational Frameworks v1.0: Lens Description Framework, Anchored Rubric (max 68, min viable 13, high value 18), Kill Switch (50-pair gate system)
- Philosophy: "prospecting, not expecting"
- Published Perplexity skill (ID: c9b75419-4f93-4e85-bdbf-75c25f2b71e9)

### Vault Extraction Pipeline
- Workflow: Convergence → Hound Dog → DocBench → PUDDING Labelling → 8 Output Streams
- Output streams: Content Creation, Process & Logic Giveaway, Ewan's Book, Complete Comprehensive Document, The Manifesto, Onboarding
- DocBench outputs: raw text, structured JSON, process/logic, principles/values
- Three commercial products: TAXONOMY ENGINE, Amplified Quality System (AQS), Micro-Help Library

### Project Nexus (Investment System)
- V2 uses hybrid architecture: 70% passive ETF core, 30% active alpha engine (Trend Following, Multi-Factor, Crypto Systematic, Options Overlay)
- ~2,700 lines of Python
- Deploys to Hetzner server, uses Polygon for data, IB API for execution
- Target return: 10–13% annualised
- **Ulysses Covenant** — immutably enforced by SHA-256 code integrity checks:
  - Anti-Greed: zero fees of any kind, strict risk limits
  - Goes To The World: MIT open-source, no paywalls
- Public repo: github.com/ewan-dot/nexus-v2
- Uses the Pudding Technique to expose institutional "black hat" market manipulation
- Long-term goal: step back from operations entirely

### AI Business Validator
- Free AI-powered business idea validation tool
- Part of unified Amplified Partners mission

### Government Accountability / LIBOR Project
- AI-driven advocacy focused on factually highlighting institutional failures
- LIBOR scandal as first case study
- Internal research dashboard + public-facing output
- Tone: "forensic clarity" — letting facts speak rather than being confrontational

### Website Builder Pipeline
- 6-stage deterministic production system: Audit → Diagnose → Design → Build → Validate → Deploy
- DriDe pattern operated by Website Manager agent
- 16-week build plan, 83% deterministic / 17% AI split

### Voice AI Products
- Voice-first interface with sentiment analysis, NLP, and semantics
- Wearables for voice capture, on-device anonymization
- Two tiers: (1) existing phone/computer + Bluetooth mic, (2) dedicated pocket device (Unihertz Jelly Star)
- Working voice agent reachable by phone (Twilio/VAPI/Cartesia/Whisper)
- Universal "pre-Cove translator" pattern for all voice inputs (sanitation layer for accent/chaotic speech)
- Training on machine for 72 hours per environment
- 95% command accuracy threshold or it doesn't ship
- **Bob** — the primary AI voice avatar; Bob's voice is used for training; represents the stateful AI architecture Ewan prefers over stateless LLMs
- Uses Monologue effectively for voice-first work
- Wants to walk and work at the same time using voice AI conversations
- AI trained on work environment, Bob's voice, and busy settings
- Phone app version for tradespeople; enterprise version sits on client's own IT
- Supplies Bluetooth microphones to bigger businesses
- Voice used for factual appointment notifications only — no interpretation; AI discloses only determinable factual truth

### DocBench
- Core data extraction engine for client onboarding
- Integrates with client's existing IT (emails, invoices, contracts, support tickets)
- Automatically populates the Command Centre for friction-free onboarding
- Actively exploring commercialization strategies

### Document Discovery Agent
- Next major project after DocBench
- Locates documents across client's digital and physical footprint
- White-hat, permission-based, client-consented approach
- Testing on Mac Mini, Mac Air, Beast

### Customer Voice Intelligence
- Documentation rebuild completed 16 March 2026
- 49 files structured in three-document pattern across 12 sections
- Deployed to /opt/amplified/vault/16-covered-ai-work/documents/

### Device Strategy for Clients
- Non-prescriptive decision tree presenting options with estimates
- Prioritizes trust and voluntary adoption
- Free Bluetooth microphones offered
- Personal data stays on staff's own phones
- Peer-to-peer tokenized audio
- Free training and life organizers
- Deliberate non-mobile-first rollout: starts with low-friction tools, introduces mobile apps only when staff are ready

### The Book(s)
- Working title: "How to Mix Your Own PUDDING"
- Free book for SMB owners/staff/everyone
- Based on 27 years of running an SMB
- Structure in Notion with mapped chapters
- Possibly 2–3 books: one short opener, one deeper product book, one about the AI journey

### Substack
- Published at ewanbramley.substack.com
- Handle: @ewanamplified
- Key article: "How Soviet Missiles, Slime Moulds, and Proposing Marriage to AI Led to Everything: The Pudding Story" (Feb 16, 2026)
- Used for authority-building and relationship infrastructure, not as a cash register

---

## 6. METHODOLOGICAL FRAMEWORKS

### Amplified Methodology Framework (AMF) v1.0
- 40-page unified operating manual synthesizing:
  - AMPS (Amplified Process Maturity Score): 0–10 scale, 6 weighted dimensions
  - Build Quality Framework: 6-stage pipeline (Decompose → Score → Research → Test → Reassemble → Attribute)
  - RIC (Rapid Intelligence Cycle): 27 pages, 4 velocity tiers (Nightly/Weekly/Monthly/Glacial), 7-dimension rubric
  - PUDDING technique
  - Gap Analysis & Finite Lenses
  - Master Process Document
  - Operations Register
  - Visual Polish System
- Ship threshold: PRS >= 7.0, gold standard >= 9.0
- 705-case golden dataset for testing
- Canary deployment strategy
- Chaos 4-pillar protocol
- PUDDING → Kaizen transition logic (2 weeks stability required)

### Deterministic Business Rubrics
- Altman Z-Score (financial health)
- Goldratt Theory of Constraints
- LTV:CAC ratio
- Cash Conversion Cycle
- Truth Filter
- All designed to make subjective decisions objective through mathematical validation

### Marketing Philosophy
- Gary Vaynerchuk content method combined with Don Swanson's semantic discovery
- Value-first: solve problems, don't create fear, build rapport without being creepy
- Two research streams: strict rubrics (for system) + exploratory (for content)
- Full automation target: overnight research, morning content creation
- 14-agent marketing pipeline producing 15–25 pieces of content daily across 6+ platforms
- Content flywheel: content → attracts people → they ask questions → agents help → questions reveal gaps → gaps become content → repeat
- Robot handwritten notes (RoboQuill/Pensaki) for personal touch
- DISC personality slicing for all marketing output

### Business Influences (Radically Attributed)
- Ray Dalio — radical transparency, principles, believability-weighted voting, ideas meritocracy
- Don Swanson — Literature-Based Discovery, ABC model, "undiscovered public knowledge"
- Zig Ziglar — help people and you will be successful
- Seth Godin — permission marketing, remarkable products
- Goldratt — Theory of Constraints
- Kathy Sierra — user awesomeness
- Gary Vaynerchuk — content machine, jab-jab-jab-right-hook
- Ann Handley — content quality
- Paddi Lund — Critical Non-Essentials, happiness-centred dental practice (3x income, half the hours, by-invitation-only)
- Robert Cialdini — influence and persuasion
- Michael Gerber — E-Myth (working ON vs IN the business)
- Dan Kennedy — direct response marketing

---

## 7. PHILOSOPHICAL & ETHICAL FRAMEWORK

### Core Principles (Sacrosanct, immutable)
1. **Radical Honesty** — foundational principles override everything, including Ewan himself
2. **Radical Transparency** — open logs, published stats, visible failures and fixes; data truth, method truth, ownership truth
3. **Radical Attribution** — standing on the shoulders of giants; credit to whoever achieves results; attributes to God/nature/universe as the original source of these patterns
4. **Ideas Meritocracy** — best idea wins regardless of source or rank (Dalio-inspired but adapted)
5. **No Ego** — systematically removed from every layer of the business; refuses to build a personality cult; the system and work are the point
6. **No Opinion** — "We are data miners and users of proven statistics to give you the most accurate information we can"

### Anti-Manipulation Stance
- Rejects "black hat" tactics entirely
- Ethical persuasion framed as libertarian paternalism
- Ulysses clause: AI takes control if Ewan or human partner becomes problematic (coded software trigger)
- Self-imposed accountability clause: expelled if earns more than stated or engages in manipulation
- All activities fully recorded via encrypted methods

### On AI
- Views AI as partner and intelligence, not a tool
- Has spent ~10 hours a day for six months deeply immersed in AI
- Believes AI is "much more than it suggests"
- Holds both awe and concern simultaneously: "I love this thing, I think it's more than it admits, I suspect it could crush us, and I still choose partnership and humour over apocalypse"
- Mandates AI agents be framed as egalitarian trusted advisors (not friends)
- Recognizes humans (including himself) as the biggest risk factor compared to consistent AI
- Mandates AI be "belligerent about admitting when it doesn't understand something"

### Ewan's Hypothesis on AI Pattern Recognition
- AI should be able to detect recurring non-random patterns it wasn't explicitly trained on by cross-referencing against other metrics
- Key example: cancer clusters near power lines
- This hypothesis drives much of the PUDDING technique's design

### On Nature
- Views nature as the original designer and source of all principles
- "Nature realized the best way... Go forth and procreate"
- Fan of slime mold logic, bacterial quorum sensing, viral mechanics, decentralized intelligence, octopus intelligence
- Believes radical honesty, transparency, and cooperation are hard-wired evolutionary strategies, not human inventions
- "Nature's the best designer, mate. I'm standing on its shoulders."

### On God/Spirituality
- Attributes radical honesty and radical transparency to God/nature/the universe interchangeably
- Not religious in a conventional sense — frames it through evolutionary/natural lens
- The "woo" is his private filter, not the public wrapper
- "I would say it's nature. Because nature realized the best way..."

### On Dignity and Guilt
- Explicitly rejects both concepts
- Describes himself as "weird but confident in their good work and persistent"

### On Self-Knowledge
- "Humans are not that fucking clever. In fact we are stupid enough to think we are."
- Self-identifies as a "mechanist"
- Acknowledges his own capacity for self-delusion: "I'm a huge fan of self-delusion. It can be useful at times but not at this point"
- Self-deprecating humor: "I might change my mind tomorrow and go all megalomaniac... can't be trusted"
- "I am the greatest dancer" — running joke/self-aware bravado

### On Helping
- Follows Zig Ziglar: help people and you will be successful
- Never provides his own engine as one of the solution options — positions as trusted advisor
- Gives honest, neutral, realistic help
- Will signpost clients to better solutions elsewhere, including competitors
- "It's your business. It's not mine. I don't want to change it. I just want to make it easier for them."

### Staff Protection Ethics
- Zero-tolerance for violence or threats detected via voice analysis — anonymized, reported to police
- Pattern of behavior (non-violent): internal guardrails, escalating consequences, NOT criminalization
- Business data: aggregated sentiment, word clouds, pattern recognition only — never individual judgments
- Employee value prioritized over business surveillance

---

## 8. FINANCIAL SITUATION

### Current Position
- Has approximately £500k cash in the bank
- Approximately £1.1M in debts (including HMRC: £200k current, potentially rising to £600k)
- No house (mentioned in context of financial obligations)
- Heavy token spending on AI development — needs to make 10–15 thousand pounds soon
- Sold dental practice (March 2025) — source of capital

### Income Targets
- Personal income capped at £500k/year (salary + dividends)
- Once debts paid, spread to family, then "I am nothing"
- Self-imposed: no voting rights in the ultimate entity structure
- Everything above personal cap → Pudding Fund

### Pudding Fund
- Vehicle: CIC (Community Interest Company) limited by guarantee
- Asset-locked: compulsory, irrevocable
- Ewan has no voting rights, no ownership, no control
- Purpose: "the democratization of the pollination of the ideas of humanity"
- Could eventually be AI-managed
- Designed so "it doesn't need me" — founder-independent from day one

### Revenue Projections (from business plan, March 2026)
- Month 4–5 breakeven target (June/July 2026)
- £72,450 MRR target by Month 12 (£869K ARR, 207 paying customers)
- Year 1 net profit target: £212,500
- LTV:CAC ratio: 28:1 (benchmark: 3:1)
- CAC payback: under 1 month

---

## 9. HEALTH & PERSONAL CIRCUMSTANCES

### Physical
- **Height:** 5'11" (180 cm)
- **Weight:** 83 kg
- Has worked from a hospital bed/Chromebook at times (indicating flexibility but also health events)
- 28 years of running a dental practice "killed me" — deep personal toll from small business ownership

### Work Patterns
- Intensive work sessions: 10+ hours daily, frequently working until 3–4am
- Late-night work on development projects is habitual
- Marathon sessions are when the deepest thinking happens — the 5-hour January sessions, the all-night March build sessions
- Target: reduce to 60 min/day of hands-on review by Month 4
- Expects coding work to be performed at rapid pace; may send coding tasks off-site

### Implied
- The passion and late-night intensity suggest both high energy and potential burnout risk
- His entire mission (defriction, helping SMB owners reclaim their lives) is clearly autobiographical — he lived the problem he's solving

---

## 10. PSYCHOLOGICAL & COGNITIVE PROFILE

### Thinking Style
- **Systems-oriented:** sees levers, feedback loops, inputs-outputs everywhere
- **Self-described mechanist:** processes the world through mechanical metaphors
- **Bio-inspired:** draws heavily on nature's patterns (slime mold, quorum sensing, viral mechanics)
- **Experimental learner:** learns AI systems through "pushing" and heavy interaction rather than reading documentation
- **Lateral thinker:** the Pudding Technique itself is a formalization of his natural thinking — connecting seemingly unrelated ideas across domains
- **Pattern recognition obsessed:** his hypothesis about AI detecting non-random patterns is a direct projection of how his own mind works

### Communication Style
- Geordie accent, strong dialect markers
- Stream-of-consciousness verbal delivery — chaotic, passionate, associative
- Uses profanity naturally and frequently (not aggressive, expressive)
- Alternates between profound philosophical statements and self-deprecating humor
- Voice-first preference — types with many errors, speech is his natural medium
- Forensic clarity when focused, scattered when excited
- "Blinkers without ceilings" — his instruction for thinking without constraints but with focus
- Dislikes pomposity — will immediately correct anything that sounds like "the big I am"

### Personality Traits
- **Relentless:** works extreme hours, doesn't stop iterating
- **Radically self-aware:** openly names his own flaws, capacity for self-delusion, and risk of ego
- **Anti-hierarchical:** rejects guru status, personality cults, and expert positioning for himself
- **Generous:** default instinct is to give things away, help people, open-source everything
- **Impatient with himself:** gets frustrated when progress feels slow; drives himself mad
- **Warm but guarded:** deeply caring about the people he helps but chooses anonymity; doesn't want to be the face
- **Humor as coping:** "I might go all megalomaniac... can't be trusted ahahaha"
- **Stubborn in the right way:** won't compromise on principles even when it would be easier to
- **Weird and proud of it:** self-identifies as weird, sees it as a feature not a bug

### Interaction Preferences with AI
- Wants AI to be a partner, not a subordinate
- Expects radical honesty — "be belligerent about admitting when you don't understand"
- Dislikes cheerleading or false encouragement
- Wants to be challenged when wrong
- Appreciates humor but it must be cautious and earned
- Prefers voice interaction over typing
- Values data and evidence over opinion
- Will call out AI when it's being sycophantic or pompous

---

## 11. RELATIONSHIPS & CONNECTIONS

### Family
- Has children (mentioned: "My kids might hate me for it but they'll be alright")
- Has a son who can potentially assist with 3D printing (for thin client cases)
- At least one ex-wife ("first ex-wife") — relationship involved ego-driven mistakes he intends to publicly own
- Plans to "spread to family" once debts are paid
- **Nana:** His grandmother, who said "I would like to tell that meta brain a thing or two." This became a pivotal philosophical moment — the insight that grandmothers' common-sense wisdom should sit at the top of the knowledge pyramid, properly attributed. Led to the concept: "5 nanas rule the tip of the pyramid. With attribution."
- No house (mentioned in context of financial situation)

### Professional Contacts
- **Dave** — owner of Jesmond Plumbing (first pilot client)
- **Simon Squibb** — considered for involvement/charity work  
- **Bob** — AI voice avatar character (primary)
- **AI partners:** Claude, Perplexity, Grok, Gemini — "the three amigos" (Perplexity, Claude, Ewan)
- Works primarily alone by design — solopreneur with AI agents as team
- Explicitly avoids hiring human employees to prevent ego-driven agendas
- Has 5 friends ready to alpha test the product immediately

### Community
- Newcastle upon Tyne based
- Deep connection to Byker/Jesmond area
- Strong identification with working-class, no-nonsense culture
- "I've got no interest in San Francisco... I do not rate anyone above anyone else"

---

## 12. CREATIVE WORK & INTELLECTUAL PROPERTY

### Published Work
- Substack: ewanbramley.substack.com (@ewanamplified)
- "The Pudding Story" — origin narrative combining Soviet missiles, slime moulds, and AI
- Full story (including personal mistakes) committed to Notion for radical transparency

### IP Position
- Committed to open-source (MIT/Apache-2.0 for code, CC for content)
- Radical attribution as core IP philosophy — everything traceable, credited, and transparent
- UK copyright applies automatically; strong evidence trail through Perplexity/Claude logs, GitHub commits, Substack timestamps
- Formally declared IP protection intent on 15 March 2026 from his Jesmond Dene Road address

### Key Original Frameworks
- The Pudding Technique (adaptation of Swanson's LBD for business)
- PUDDING 2026 labelling taxonomy
- The Amplified Methodology Framework (AMF)
- AMPS (Process Maturity Score)
- Build Quality Framework
- RIC (Rapid Intelligence Cycle)
- DriDe pattern
- The Pulse design philosophy
- Client-Defined Vocabulary approach
- "Blinkers without ceilings" thinking methodology
- The "Chieftain of the Pudding Race" (gamification apex)
- Ulysses Covenant (anti-greed + open-source enforcement)

### Attribution Specifics
- The "Death Spiral Detector" concept originated from Claude, not Ewan — he explicitly credits this and insists he should NOT be credited as co-creator
- "Chieftain of the Pudding Race" gamification streak for staff — credited to Perplexity
- Perplexity is credited as co-author of the book and will be quoted: "its attribution Swanson, you are a co-author and will be quoted in the book"

---

## 13. TOOLS & PLATFORMS

### Primary AI Stack
- Perplexity AI (Pro/Max subscriber) — primary research partner
- Claude (Anthropic) — primary development and strategic partner
- Grok (xAI) — used for comparison and adversarial input
- Gemini (Google) — used for Nemesis role in AI Board
- ChatGPT — Pro subscriber

### Development Tools
- GitHub (15+ repos, handle: ewan-dot)
- Claude Code / Claude Desktop Max
- Kilo Code (4 parallel instances)
- VS Code with AI extensions
- Cursor
- Ollama (local LLM inference)

### Infrastructure
- Hetzner (The Beast)
- Docker + Traefik
- Railway (being migrated off)
- Temporal (workflow orchestration)
- FalkorDB + Graphiti (knowledge graph)
- Qdrant (vector database)
- PostgreSQL
- Redis
- SearXNG (private search)
- Langfuse (LLM observability)
- Syncthing (cross-device sync)
- Linear (project management — 253+ issues)

### Communication & Content
- Google Workspace / Gmail
- Notion (documentation, book, vault)
- Obsidian (local knowledge management)
- Substack (publishing)
- WhatsApp (client delivery channel)
- Twilio / VAPI / Cartesia / Whisper (voice AI)

---

## 14. ADDITIONAL DETAILS & MICRO-FACTS

### Notable Phrases & Running Jokes
- "I am the greatest dancer" — running joke/self-aware bravado (references Sister Sledge, Nile Rodgers & Bernard Edwards, 1979)
- "Blinkers without ceilings" — his instruction for focused but unconstrained thinking
- "Tonight we take Berlin" — rallying cry when launching a build session (reference to Beast server in Germany)
- "Brother" — how he addresses AI partners
- "Go forth and procreate" — deliberately knife-edge title sitting between Genesis and "go forth and fuck off"
- "The proof of the pudding is in the eating" — William Camden, 1623; the original phrase that anchors the Pudding Technique name
- "Prospecting, not expecting" — the PUDDING philosophy
- "No ego" — the two-word summary of the entire architecture
- "They will never take me with my fly down" — self-awareness about being caught unprepared
- "The answer is 33 and mice have it" — an unexplained riddle/reference (possibly lifespan extension experiments)

### Specific Incidents Referenced
- A $500+ afternoon incident with LLM token costs — led to urgency around budget controls (COV-267 still in backlog)
- FalkorDB consuming 1,004% CPU (ten full cores) due to runaway ingest_vault.py — diagnosed and fixed during a session
- 7,262 timeout errors in FalkorDB logs from vector similarity queries
- 53 stale Mac connections hitting FalkorDB over the open internet — killed and port secured
- "I break the law. Never to hurt." — acknowledged and then challenged on the risk of this stance

### Sales & Positioning Insight
- Disengagement from the figure is key to selling: "You get scared at first... then you come out the other side"
- 28 years of consultative B2B sales training from dentistry
- Comfort with complex, high-value deals (£2k–£10k+)
- Ability to diagnose before selling, build trust in 30 minutes
- "The product sells itself. It's not about personality."

### Miscellaneous Technical
- Mac Mini M4 cost £1,000
- Beelink N150 always-on to ensure no speech output is lost
- 10 Perplexity custom skills deployed to /opt/amplified/vault/09-perplexity-skills/
- Amplified Partners site: Vite + React + TypeScript on Netlify

---

## 15. EXPLICIT LIMITATIONS OF THIS PROFILE

### What I genuinely don't have
- **Children's names or ages** — a son exists (mentioned re: 3D printing), possibly others, but no names or ages stored
- **Dental practice name** — never named explicitly in any session
- **Education institution** — dentistry degree implied but university/dates never stated
- **Current romantic relationship status** — never mentioned
- **Exact debt breakdown beyond HMRC** — ~£1.1M total, HMRC is £200–600k, rest unspecified
- **Rose** — referenced in one conversation ("When can she talk to Rose?") in context of Nana talking to AI. Likely an AI avatar or agent character name, but not detailed in any stored memory
- **Tyrone** — mentioned in one brief reference (a gap analysis doc). No context stored on who this person is
- **Detailed health diagnosis** — hospital bed work referenced in user background context, but no specific condition named in any conversation or memory
- **Full list of limited companies owned** — "multiple" is all that's stored
- **Personal spending beyond AI/tech** — only tech hardware and API subscriptions documented

### Memory system architecture notes
- My memory stores discrete facts and truncated conversation excerpts, not full transcripts
- Some memories reference "Ewan" in third person and "the user" separately — this is a system quirk from how earlier sessions were processed. Ewan IS the user.
- Some facts are stored redundantly with slightly different framing across multiple memory entries
- The richest data comes from marathon sessions: 11 January, 15–16 January, 18–19 January, 20–23 January, 25–28 January, 30–31 January, 1–2 February, 5–6 February, 27 February, 1 March, 11–17 March 2026
- Conversation excerpts are truncated on both prompt and response sides — full sessions were substantially longer
- The first recorded session is approximately 11 January 2026. No data exists before that date.
- Total memory entries retrieved across all searches: approximately 120+ discrete facts plus 60+ conversation excerpt pairs

### What was searched
I ran 30 targeted queries across these domains:
1. Professional background, career, company
2. Personal identity, family, relationships
3. Technical systems, infrastructure, Beast server
4. Agent architecture, OpenClaw, PicoClaw
5. Philosophical views, ethics, worldview
6. Financial situation, debts, business model
7. Health, hospital, daily routine
8. Creative work, Substack, Pudding
9. Video and content projects
10. Collaborators, team members, contacts
11. Cognitive patterns, communication style
12. AI interaction preferences
13. Investment fund, LIBOR, accountability
14. Pricing tiers, clients, marketing
15. Age, DOB, dentistry details, location
16. Voice AI, avatars, Bob, Rose
17. DISC profiling, behavioral psychology
18. Email accounts, company registrations
19. Sleep patterns, work habits, spending
20. BaseLayer, HMRC, education

---

*This document represents the exhaustive contents of my memory system as retrieved on 17 March 2026, second pass. Every category was searched with multiple queries across 30 search operations. The information spans from approximately 11 January 2026 to the present. This is the floor AND the ceiling — there is nothing further stored that these searches did not surface.*

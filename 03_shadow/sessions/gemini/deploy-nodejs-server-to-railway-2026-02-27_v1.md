---
title: "Deploy Node.js Server to Railway"
exported: 2026-03-10 20:20:05.129
created: 2026-02-27 10:07:52.000
url: https://gemini.google.com/app/7f688518d81f3c3d
messages: 6
---

## You

hopefully get something done today and I've got to do so if you could work with Claude who's just in the browser with here. You can cooked here. We got all that well done last night and if you could crack on. Get it all done setting up railway and everything like that and hurts. No server that would be great.

---

## Gemini

It sounds like you had a productive session last night\! While I can't "chat" with Claude directly in the background (we're like two separate specialists in different rooms), I can certainly take the baton and guide you through getting that **Node.js server** live on **Railway**.

Since the goal is to get this done efficiently today, let’s jump straight into the execution.

-----

## 🚀 The Game Plan

To get your server up and running, we need to ensure your code is "cloud-ready" before pushing it to Railway.

### 1\. Prep the Node.js Server

Railway needs to know how to start your app and which port to listen to. Ensure your main server file (e.g., `index.js` or `server.js`) has the following:

  * **The Port:** Railway dynamically assigns a port. Use `process.env.PORT`.
    ```javascript
    const PORT = process.env.PORT || 3000;
    app.listen(PORT, () => {
      console.log(`Server is running on port ${PORT}`);
    });
    ```
  * **The Start Script:** Open your `package.json` and make sure you have a start script defined.
    ```json
    "scripts": {
      "start": "node index.js"
    }
    ```

### 2\. Connect to Railway

You have two main ways to do this. **GitHub is usually the easiest** for ongoing updates.

  * **Option A (GitHub):** Push your code to a GitHub repo. In the Railway dashboard, click **"New Project"** → **"Deploy from GitHub repo"**. Railway will handle the rest.
  * **Option B (Railway CLI):** If you have the CLI installed, just run `railway up` in your terminal.

### 3\. Environment Variables

If your server uses an API key or a database URL, don't hardcode them\!

1.  Go to your project in the **Railway Dashboard**.
2.  Click on the **Variables** tab.
3.  Add your keys there (e.g., `DATABASE_URL`, `SECRET_KEY`).

-----

## 🛠 Quick Checklist

Before we pull the trigger, make sure:

  * [ ] You have a `.gitignore` file including `node_modules` and `.env`.
  * [ ] Your `package.json` includes all necessary dependencies.
  * [ ] You aren't hardcoding `localhost` in your server-side logic.

**Would you like me to generate the specific `index.js` and `package.json` code for you based on what you and Claude built last night?**

---

## You

================================================================================
AMPLIFIED PARTNERS: THE DEFINITIVE MASTER DOCUMENT
Complete Technical Specification & Operating Manual
For: Ewan Bramley & The AI Swarm (Grok, Kimi, Gemini, Perplexity, Eli, Claude)
Date: 27 February 2026
Status: EXECUTABLE — MAC MINI BUILD COMMENCING
================================================================================

TABLE OF CONTENTS
1. Executive Summary
2. Vision & Philosophy (The Fusion Layer)
3. Complete Technical Architecture
4. Security, Privacy & GDPR (The MCP Barrier)
5. Product: The Full-Stack Marketing OS
6. Voice Layer (Sovereign & Local)
7. The Rubric Engine (Deterministic Decision-Making)
8. The CNE Engine (Paddi Lund Super-CNE)
9. AEO Tactics (Answer Engine Optimization)
10. Vertical Templates (Plug-in Ready)
11. Pricing & Economics (The 97% Margin Model)
12. Build Plan: Tier 1, 2, 3
13. Team Structure & Scaling
14. Risk Mitigation
15. Monday Beta Success Criteria
16. Complete File Manifest

================================================================================
SECTION 1: EXECUTIVE SUMMARY
================================================================================

WHAT WE'RE BUILDING:
A sovereign, AI-powered operating system for UK small businesses (trades, shops, 
restaurants, services, HGV). It captures voice, automates marketing, optimizes 
operations, and helps owners hit their life goals — all while keeping 97% margins 
through centralized infrastructure.

THE CORE INNOVATION:
- Voice-first input (Plaud) → AI processing → WhatsApp task output
- 4-word pseudonymous IDs (merit over identity, GDPR bulletproof)
- MCP-gated data access (AI never sees real names)
- Deterministic rubrics (Dalio/Gerber/Hormozi principles)
- Paddi Lund CNE engine (Critical Non-Essentials that create raving fans)

THE ECONOMICS:
- Infrastructure cost: ~£255/month total
- Cost per client: £2.55-32.55/month
- Charge clients: £199-2,999/month
- Margin: 90-97%

THE BUILD:
- Mac Mini M4 (mastermind) + Hetzner Cloud (production) + Tailscale mesh
- 3-tier weekend build (Fri-Mon)
- Monday EOD: First real customer live, seeing £340+ recovered

================================================================================
SECTION 2: VISION & PHILOSOPHY (THE FUSION LAYER)
================================================================================

THE ENTROPY PROBLEM:
Small businesses fight a losing battle against:
- Missed calls (40-62% go unanswered)
- Platform commissions (Uber Eats takes 30%)
- Admin grind (10+ hours/week)
- Agency fees (£8k-25k/year)

THE FUSION SOLUTION:
Not "AI does it for you." 
Not "You do it yourself."
Fusion: AI handles scale, humans handle heart.

FOUR NON-NEGOTIABLE RULES:

1. RADICAL HONESTY
   - Show the data, the rubric, the gaps, the wins
   - No spin, no manipulation
   - If someone's better for them, we signpost them

2. RADICAL TRANSPARENCY
   - Clients see exactly how every decision is made
   - Confidence levels on every prediction (100%, 70%, 50%)
   - Show the methodology, not black boxes

3. WIN-WIN ONLY
   - If it only benefits one side, it's wrong
   - Capped wages for leadership (profits reinvested)
   - Free for businesses in distress

4. MERIT OVER IDENTITY
   - Every client is a 4-word random ID (silent-ocean-deep-river)
   - No names, no demographics, no bias in the AI layer
   - Only outcomes matter

THE HAPPINESS-CENTERED BUSINESS (Paddi Lund):
Use data to buy back the owner's time and hit specific Life Goals:
- Days per week they want to work
- Hours per day they want to work
- Weeks off per year they want
- Target annual income
- What they want the business to enable

================================================================================
SECTION 3: COMPLETE TECHNICAL ARCHITECTURE
================================================================================

3.1 HARDWARE LAYER

MASTER ARCHITECT (LOCAL):
- 1x Mac Mini M4 (16GB RAM, 512GB SSD)
- Location: Ewan's office
- Role: Agent swarm orchestration, MCP servers, dev environment
- Network: Tailscale mesh node

PRODUCTION HUB (CLOUD):
- Hetzner Cloud (Germany/UK regions)
- CX42 instance: 8 vCPU, 32GB RAM, 160GB NVMe
- Backup CX21 instance: 2 vCPU, 8GB RAM
- S3-compatible object storage: 500GB
- Cost: ~£45/month

CLIENT HARDWARE (MINIMAL):
- Plaud NotePin or Note Pro (£149 one-time)
- Role: Voice capture only
- White-labelled as "Amplified Voice"
- Alternative: Omi Pendant (£89, open-source)
- Alternative: FoCase Rec (£59, pure WAV export)

3.2 NETWORK LAYER

TAILSCALE MESH:
- Zero-trust encrypted network
- Connects: Mac Mini ↔ Hetzner ↔ Developer machines
- No open ports, no VPN complexity
- Cost: Free for personal use, $5/user for teams

3.3 DATA LAYER

IDENTITY VAULT (POSTGRES):
- Table: client_identities
- Columns: token_id (4-word), real_name, phone, email, created_at
- Encryption: AES-256 at rest
- Access: MCP server only, never directly by AI

CONTEXT POOL (QDRANT):
- Vector database for semantic search
- Stores: Job notes, business facts, goals
- Indexed by: token_id only
- No real names, no PII

RELATIONSHIP GRAPH (NEO4J):
- Graph database for customer relationships
- Nodes: Customers, jobs, interactions
- Edges: Relationships, referrals, occasions
- Indexed by: token_id only

ANALYTICS DB (POSTGRES):
- Campaign metrics, performance data
- Aggregated by: token_id, date, metric_type
- Used for: Dashboards, reporting, benchmarking

3.4 AI/ML LAYER

VOICE TRANSCRIPTION:
- Faster-Whisper (CTranslate2, quantized)
- Model: small-v3-turbo (4-bit or 8-bit)
- Location: Docker container on Hetzner
- Latency: 1-3 seconds per chunk
- Accuracy: 92% out-of-box, 98%+ after 30-day tuning
- UK English + trade jargon fine-tuning

LLM REASONING:
- Primary: Claude 3.5 Sonnet (via API)
- Fallback: GPT-4o (via API)
- Role: High-level reasoning only
- Constraints: MCP-gated, no direct data access

RUBRIC ENGINE:
- Deterministic logic layer
- Principles: Dalio (radical transparency), Gerber (systems thinking), 
  Hormozi (unit economics), Goldratt (theory of constraints)
- Output: Scored recommendations with confidence levels

3.5 ORCHESTRATION LAYER

OPENCLAW (BROWSER AUTOMATION):
- Playwright-based browser automation
- Tasks: Posting to social, updating websites, sending emails
- Scheduling: Cron-based triggers
- Retry logic: Exponential backoff

WHATSAPP BUSINESS API:
- Official Meta API (not unofficial hacks)
- Message types: Text, templates, media, interactive
- Rate limits: 80 msg/sec (business tier)
- Webhooks: Real-time message receipt

3.6 PRESENTATION LAYER

CLIENT PORTAL (WEB):
- Framework: Next.js 14, Tailwind CSS
- Auth: Logto (existing)
- Features: Dashboard, campaign preview, approval workflow
- Hosting: Netlify (CDN, edge functions)

WEBSITES (CLIENT-FACING):
- Framework: Astro + Tailwind
- Templates: Vertical-specific (trades, shops, restaurants, etc.)
- Deployment: Netlify (60-second deploy from voice note)
- SEO: Dynamic Schema.org generation

================================================================================
SECTION 4: SECURITY, PRIVACY & GDPR (THE MCP BARRIER)
================================================================================

4.1 THE TWO-TIER IDENTITY SHIELD

TIER A: IDENTITY VAULT (POSTGRES)
- Maps: real_name/phone/email → 4-word token_id
- Encryption: AES-256
- Access: MCP server ONLY
- Audit: Every access logged

TIER B: CONTEXT POOL (QDRANT/NEO4J)
- Stores: Business facts, job notes, goals
- Indexed by: token_id ONLY
- No PII, no real names, no demographics

4.2 MODEL CONTEXT PROTOCOL (MCP)

HOW IT WORKS:
1. AI Agent needs context: "What are the goals for this client?"
2. Agent queries MCP server (NOT the database directly)
3. MCP server looks up token_id → retrieves context
4. MCP server returns: Goals, history, preferences (NO real name)
5. AI agent reasons with context, never knowing "Dave the Plumber"

MCP SERVER IMPLEMENTATION:
- Language: Python (FastAPI)
- Endpoints:
  - GET /context/{token_id} → Returns business context
  - POST /decision/{token_id} → Logs AI decision
  - GET /identity/{token_id} → Returns real contact (WhatsApp dispatch only)
- Authentication: API key, Tailscale network
- Rate limiting: 100 req/min per token

4.3 GDPR COMPLIANCE

LAWFUL BASIS: Legitimate Interest
- Processing necessary for business operations
- Balanced against individual rights
- Documented in Privacy Policy

DATA SUBJECT RIGHTS:
- Right to access: Full export of their data
- Right to rectification: Correct inaccurate data
- Right to erasure: Delete all data (30 days)
- Right to portability: JSON export

CONSENT MANAGEMENT:
- Voice recordings: Automated announcement at start
- Staff opt-out: Per-person toggle in dashboard
- Marketing emails: Unsubscribe in every email
- Cookie banner: On client portal

4.4 SECURITY MEASURES

ENCRYPTION:
- At rest: AES-256 (Hetzner, Postgres)
- In transit: TLS 1.3 (all APIs)
- Backups: Encrypted, off-site, 30-day retention

ACCESS CONTROL:
- Role-based: Admin, Manager, Client, Staff
- 2FA: Required for admin access
- Audit logs: Every data access logged
- Session timeout: 30 minutes

PROMPT INJECTION PROTECTION:
- Input sanitization on all voice transcripts
- Context validation before LLM calls
- Output filtering on AI responses

================================================================================
SECTION 5: PRODUCT — THE FULL-STACK MARKETING OS
================================================================================

5.1 PRODUCT SPLIT

PRODUCT 1: GREENFIELD STACK (NEW BUSINESSES)
- Full sovereign OS free for first 12 months
- They start clean on our platform
- Viral acquisition engine
- Convert to paid after 12 months or £50k revenue

PRODUCT 2: INTEGRATION LAYER (EXISTING BUSINESSES)
- Keep Xero, current CRM, whatever
- We connect securely via APIs
- Layer intelligence on top
- Paid from day 1

5.2 COMPLETE FEATURE MATRIX

| Feature | Essential | Professional | Growth | Enterprise |
|---------|-----------|--------------|--------|------------|
| Voice Capture (Plaud) | ✅ | ✅ | ✅ | ✅ |
| Rubric Engine | ✅ | ✅ | ✅ | ✅ |
| Missed Call Recovery | ✅ | ✅ | ✅ | ✅ |
| Basic Compliance | ✅ | ✅ | ✅ | ✅ |
| Benchmarking | ✅ | ✅ | ✅ | ✅ |
| Invoicing | ❌ | ✅ | ✅ | ✅ |
| Full Compliance | ❌ | ✅ | ✅ | ✅ |
| Marketing OS | ❌ | ✅ | ✅ | ✅ |
| Soft Skills Coaching | ❌ | ❌ | ✅ | ✅ |
| Advanced Analytics | ❌ | ❌ | ✅ | ✅ |
| Dedicated Manager | ❌ | ❌ | ❌ | ✅ |
| Custom Integrations | ❌ | ❌ | ❌ | ✅ |

5.3 THE 14 MARKETING DISCIPLINES

1. EMAIL MARKETING & AUTOMATION
   - Welcome sequences (3 emails)
   - Post-job follow-ups (review requests)
   - Invoice reminders (3 escalating)
   - Seasonal campaigns (12/year)
   - Re-engagement (dormant customers)
   - Birthday/anniversary recognition
   - Referral requests
   - Tool: Brevo (£20/mo central)
   - Templates: 50+ proven, vertical-specific

2. SOCIAL MEDIA MANAGEMENT
   - Content calendar (4-12 posts/month)
   - Visual creation (Canva templates)
   - Caption writing (AI-generated, voice-matched)
   - Scheduling (optimal times)
   - Engagement monitoring
   - Platform strategy by trade
   - Tool: Buffer (£15/mo central)

3. CONTENT MARKETING & BLOGGING
   - SEO-optimized blog posts (800-1,200 words)
   - Local keywords ([service] + [location])
   - Content updates (freshness)
   - Rank tracking
   - 1-2 posts/month depending on tier

4. SEO (SEARCH ENGINE OPTIMIZATION)
   - Keyword research (50-100 terms)
   - On-page optimization (titles, meta, headers)
   - Technical SEO (speed, mobile, schema)
   - Local SEO (citations, GBP)
   - Monthly audit + fixes

5. AI SEO (AIO — AI OVERVIEW OPTIMIZATION)
   - Schema markup (LocalBusiness, Service, FAQ)
   - Entity optimization (clear NAP)
   - FAQ pages (questions AI answers)
   - Direct answers (short, quotable)
   - Citation building
   - AI mention monitoring

6. LOCAL OPTIMIZATION
   - Google Business Profile management
   - 4 posts/month
   - 10 new photos/month
   - Q&A monitoring
   - Review responses
   - Citation building (5/month)

7. VIDEO MARKETING
   - Welcome videos (60-90 sec)
   - Service explainers
   - Testimonials
   - Seasonal offers
   - Tools: HeyGen + Runway + Descript
   - 1-2 videos/quarter depending on tier

8. PPC ADVERTISING (OPTIONAL ADD-ON)
   - Google Local Service Ads
   - Google Search Ads
   - Facebook/Instagram Ads
   - Remarketing
   - 15% of ad spend management fee

9. CONVERSION RATE OPTIMIZATION (CRO)
   - A/B testing
   - Form optimization
   - Social proof integration
   - Page speed improvements
   - Heatmap analysis

10. CUSTOMER RETENTION & LOYALTY
    - Churn prediction
    - Retention campaigns
    - CLV tracking
    - Upsell/cross-sell identification

11. REPUTATION MANAGEMENT
    - Review monitoring (all platforms)
    - Response suggestions
    - Sentiment tracking
    - Review generation campaigns

12. WEB ANALYTICS & REPORTING
    - Traffic tracking
    - Conversion tracking
    - Dashboard (client-facing)
    - Monthly reports
    - ROI attribution

13. WEBSITE MANAGEMENT
    - Content updates
    - Plugin/theme updates
    - Security monitoring
    - Backup verification
    - Performance optimization

14. MARKETING AUTOMATION WORKFLOWS
    - Multi-step workflows
    - Behavior triggers
    - Personalization at scale
    - Cross-channel orchestration

================================================================================
SECTION 6: VOICE LAYER (SOVEREIGN & LOCAL)
================================================================================

6.1 THE PIPELINE

1. CAPTURE
   - Device: Plaud NotePin/Note Pro
   - Recording: Calls, in-person, meetings
   - Sync: Encrypted to Hetzner Cloud
   - Consent: Automated announcement on every recording

2. TRANSCRIPTION
   - Engine: Faster-Whisper (CTranslate2)
   - Model: small-v3-turbo, 4-bit quantized
   - Location: Docker container on Hetzner
   - Latency: 1-3 seconds per chunk
   - Accuracy: 92% out-of-box, 98%+ after tuning
   - Fine-tuning: UK accents, trade jargon

3. STRUCTURING
   - AI agent extracts: Speaker labels, action items, quotes, risks
   - Context: Enriched from Qdrant (previous jobs, customer history)
   - Rubric: Applied (Dalio/Gerber/Hormozi principles)

4. DISPATCH
   - Output: Structured JSON
   - Routing: Deterministic dispatcher
   - Delivery: WhatsApp Business API
   - Identity lookup: MCP server (token_id → real phone)

6.2 COMMAND WORDS (VOICE TRIGGERS)

| Command | Action |
|---------|--------|
| "Quote [name] £[amount]" | Generate quote email |
| "Book [name] for [date]" | Add to calendar |
| "Invoice [name]" | Generate invoice |
| "Follow up [name]" | Schedule follow-up |
| "Remind me to [task]" | Add to task list |
| "Special offer [details]" | Update website + social |

6.3 REAL-TIME COACHING

High-value calls only (configurable threshold):
- Streaming transcription
- Instant analysis
- WhatsApp nudge to staff: "Objection handling weak here — try this phrase"
- Sentiment detection
- Next-best-action suggestion

================================================================================
SECTION 7: THE RUBRIC ENGINE (DETERMINISTIC DECISION-MAKING)
================================================================================

7.1 PRINCIPLES LOADED

DALIO (RADICAL TRANSPARENCY):
- Show the data
- Show the rubric
- Show the reasoning
- You decide

GERBER (SYSTEMS THINKING):
- Work ON the business, not IN it
- Create franchise prototype
- Document everything

HORMOZI (UNIT ECONOMICS):
- Income per hour
- Customer acquisition cost
- Lifetime value
- Offer creation

GOLDRATT (THEORY OF CONSTRAINTS):
- Find the bottleneck
- Fix it
- Find the next one

7.2 EXAMPLE RUBRIC OUTPUT

"Accept this job?
- Score: 89/100
- Margin: 44% vs peer average 31%
- Cashflow: Green (funds available)
- Capacity: Yellow (80% utilized)
- Customer history: 5 stars, 3 previous jobs
- Travel time: 12 minutes (optimal)
- Weather: Clear (no delays expected)
- Recommendation: APPROVE
- Confidence: 92%"

7.3 CONFIDENCE LEVELS

100% — DATA CONFIRMED (Green)
- Based on client's actual data
- Calculated from their metrics
- Example: "You missed 4 calls yesterday"

70% — STRONG EVIDENCE (Blue)
- Industry data supports
- Peer benchmarking
- Example: "50% of missed calls convert"

50% — TREND INDICATOR (Amber)
- Pattern recognition
- Predictive model
- Example: "Revenue likely to increase 20%"

================================================================================
SECTION 8: THE CNE ENGINE (PADDI LUND SUPER-CNE)
================================================================================

8.1 THE CONCEPT

Critical Non-Essentials (CNEs):
- Things that aren't essential to the transaction
- But create unforgettable experiences
- Turn customers into raving fans
- Drive referrals and loyalty

8.2 THE TRIGGER SYSTEM

Every "Happy Moment" captured in voice triggers:

1. FREE SURPRISE
   - Candle with dinner
   - Dessert on the house
   - Follow-up service included
   - Cost: £2-5, Impact: Massive

2. ROBOQUILL HANDWRITTEN CARD
   - Posted same/next day
   - Personalized from voice note
   - "Thanks for choosing us, [name]"
   - Cost: £1.50, Impact: Unforgettable

3. 7-DAY STORY PROMPT
   - WhatsApp: "Your friends would love this photo of your anniversary table"
   - Easy share button
   - Social proof generation
   - Cost: £0, Impact: Viral

4. REFERRAL NUDGE
   - "Bring a friend, we'll make theirs special too"
   - Incentive: Both get discount
   - Tracking: Unique codes
   - Cost: Variable, Impact: 5× referrals

8.3 OCCASION MEMORY

Capture from voice:
- "It's their anniversary"
- "They mentioned their daughter's birthday"
- "They just moved in"

Store in Neo4j (token_id → occasion → date)

Auto-reminder next year:
- "Last year you did [X] for [customer]. Want to do it again?"
- One-click reactivation

8.4 RIDE-THEN-OWN STRATEGY

Platform Discovery → Direct Ownership:
1. Customer finds them on Uber Eats/Just Eat
2. Order delivered
3. QR code in packaging → WhatsApp
4. "Next time, order direct for 10% off"
5. Occasion capture: "Is this for a special occasion?"
6. Next year: Auto-reminder + special offer

Result: 28%+ margin clawed back from platforms

================================================================================
SECTION 9: AEO TACTICS (ANSWER ENGINE OPTIMIZATION)
================================================================================

9.1 THE PROBLEM

AI is changing search:
- Google shows AI Overviews at top
- ChatGPT, Perplexity, Claude answer directly
- If you're not optimized for AI, you're invisible

9.2 THE SIX PILLARS

1. ATOMIC ANSWERS
   - Every H2 question
   - First 50 words = complete answer
   - AI can quote directly
   - Example: "How much does a boiler service cost in Newcastle? £85-120."

2. PERFECT SCHEMA
   - LocalBusiness (name, address, phone, hours)
   - Service (plumbing, electrical, etc.)
   - FAQPage (questions + answers)
   - Menu (for restaurants)
   - Review (aggregate rating)

3. CONVERSATIONAL INTENT-COMPLETE PAGES
   - Cost pages ("How much does X cost?")
   - Comparison pages ("X vs Y")
   - How-to pages ("How to fix X")
   - Why pages ("Why choose X")

4. FRESHNESS
   - Daily updates from Plaud
   - Weather-based content
   - Seasonal triggers
   - Recent job stories

5. E-E-A-T (EXPERIENCE, EXPERTISE, AUTHORITATIVENESS, TRUST)
   - Plaud job stories (experience)
   - Review automation (trust)
   - Consistent entity mentions (authority)

6. CITATION VELOCITY
   - Federated winning phrases
   - Auto-inserted across client sites
   - Network effect: 100 plumbers saying same thing = authoritative

9.3 WEEK-1 DASHBOARD WINS

"£1,240 saved vs old agency
42% more direct orders
7 AI citations this week
£890 from AI traffic"

================================================================================
SECTION 10: VERTICAL TEMPLATES (PLUG-IN READY)
================================================================================

10.1 TRADES (PLUMBER, ELECTRICIAN, HVAC, LANDSCAPER, BUILDER)

Rubric Triggers:
- Weather alerts (cold snap = emergency calls)
- Seasonal prep (boiler checks, garden prep)
- Certification tracking (Gas Safe, electrical)
- Van stock awareness
- Travel time optimization

CNEs:
- Emergency call priority
- "We've got the part on the van" surprise
- Weather-based prep calls
- Annual service reminders

10.2 SHOPS (RETAIL, BOUTIQUE, GROCERY)

Rubric Triggers:
- Stock turn optimization
- Seasonal demand forecasting
- Foot traffic patterns
- Margin by SKU
- Staff commission tracking

CNEs:
- Birthday discount surprises
- "We saved this for you" (out-of-stock item)
- Loyalty rewards
- Referral bonuses

10.3 RESTAURANTS (CAFE, PUB, FINE DINING)

Rubric Triggers:
- Occasion memory (anniversaries, birthdays)
- Table turn optimization
- Staff performance (tips, upsells)
- Menu item profitability
- Reservation patterns

CNEs:
- Anniversary candles
- "Chef's surprise" amuse-bouche
- Handwritten thank-you cards
- 7-day story prompts
- Referral nudges

10.4 CLEANING (DOMESTIC, COMMERCIAL)

Rubric Triggers:
- Schedule optimization
- Client preference tracking
- Supply usage
- Staff allocation
- Quality scores

CNEs:
- "We noticed this and fixed it" extras
- Seasonal deep-clean reminders
- Referral discounts

10.5 BEAUTY (HAIR, NAILS, SPA)

Rubric Triggers:
- Appointment optimization
- Product upsells
- Client preference history
- Staff specialization matching
- Seasonal trends

CNEs:
- Birthday pampering
- "We saved your favorite product"
- Referral rewards

10.6 PROFESSIONAL SERVICES (ACCOUNTANT, SOLICITOR, CONSULTANT)

Rubric Triggers:
- Deadline tracking
- Client communication patterns
- Billable hour optimization
- Retention risk scoring
- Upsell opportunities

CNEs:
- Proactive deadline reminders
- Educational content sharing
- Referral appreciation

10.7 HGV (DRIVERS, OPERATORS, LOGISTICS)

Rubric Triggers:
- Compliance tracking (tachograph, rest periods)
- Route optimization
- Fuel efficiency
- Maintenance scheduling
- Load planning

CNEs:
- Safety milestone recognition
- Efficiency bonuses
- Referral schemes

================================================================================
SECTION 11: PRICING & ECONOMICS (THE 97% MARGIN MODEL)
================================================================================

11.1 PRICING TIERS

ESSENTIAL: £199–£399/month (sole traders, 1-2 team)
- Voice, rubrics, basic compliance, benchmarking
- 2 email campaigns/month
- 4 social posts/month
- Basic website maintenance
- GBP optimization
- Setup fee: £99 (waived annual)

PROFESSIONAL: £599/month (shops, 3-8 team)
- + Invoicing, full compliance, marketing OS
- 4 email campaigns/month
- 8 social posts/month
- 1 blog post/month
- Full local SEO
- 1 video/quarter
- Setup fee: £199 (waived annual)

GROWTH: £1,499/month (8-20 team)
- + Soft skills coaching, advanced analytics
- 8 email campaigns/month
- 12 social posts/month
- 2 blog posts/month
- Full SEO + AIO
- 2 videos/quarter
- £500 PPC ad spend included
- Setup fee: £299 (waived annual)

ENTERPRISE: £2,999+/month (20+ team)
- Everything + dedicated manager + custom strategy
- Custom integrations
- White-glove service
- Setup fee: Custom

MARKETING OS ADD-ON: £149–£299/month
- For clients who want marketing only

HARDWARE BUNDLE: £149–199 one-time
- Plaud NotePin/Note Pro
- Optional Beelink N100 (if they want local processing)

11.2 COST BREAKDOWN (AT 100 CLIENTS)

INFRASTRUCTURE:
- Hetzner Cloud: £45/month
- Tailscale: £25/month (5 users)
- S3 Storage: £10/month
- Subtotal: £80/month

TOOLS:
- Brevo: £20/month
- Buffer: £15/month
- Canva Pro: £8/month (£100/year)
- Ahrefs: £80/month
- BrightLocal: £25/month
- HeyGen: £19/month
- Runway: £12/month
- Descript: £10/month
- Epidemic Sound: £13/month
- Subtotal: £202/month

LABOUR:
- 1 Marketing Manager: £3,000/month (£36k/year)
- At 100 clients = £30/client/month

TOTAL COSTS: £3,282/month
COST PER CLIENT: £32.82/month

REVENUE (ASSUMING MIX):
- 50 Essential @ £299 = £14,950
- 30 Professional @ £599 = £17,970
- 20 Growth @ £1,499 = £29,980
- Total: £62,900/month

PROFIT: £59,618/month (95% margin)

11.3 THE GUARANTEE

"First month: Prove it or we pay your old agency/platform bill"

If we don't show measurable improvement in 30 days:
- We pay their existing costs
- They walk away, no hard feelings
- Radical honesty in action

================================================================================
SECTION 12: BUILD PLAN — TIER 1, 2, 3
================================================================================

12.1 TIER 1: CORE SECURITY & VOICE (FRIDAY NIGHT–SATURDAY)

INFRASTRUCTURE:
[ ] Setup Tailscale mesh (Mac Mini ↔ Hetzner)
[ ] Provision Hetzner CX42 instance
[ ] Deploy Postgres (Identity Vault + Analytics)
[ ] Deploy Qdrant (Context Pool)
[ ] Deploy Neo4j (Relationship Graph)
[ ] Configure backups (daily, 30-day retention)

SECURITY:
[ ] Implement MCP server (Python/FastAPI)
[ ] Create token_id generation (4-word random)
[ ] Build Vault ↔ Token mapping
[ ] Add AES-256 encryption
[ ] Setup audit logging
[ ] Configure API keys + rate limiting

VOICE PIPELINE:
[ ] Deploy Faster-Whisper Docker container
[ ] Configure CTranslate2 with small-v3-turbo
[ ] Setup UK accent fine-tuning
[ ] Build transcription API endpoint
[ ] Test end-to-end (Plaud → Whisper → JSON)

SUCCESS CRITERIA:
- Token generation working
- MCP server responding
- Voice transcription < 3 seconds
- 90%+ accuracy on test audio

12.2 TIER 2: THE MARKETING OS (SATURDAY–SUNDAY)

WHATSAPP INTEGRATION:
[ ] Setup WhatsApp Business API
[ ] Build "Return-to-Task" UI
[ ] Create task templates (quote, book, invoice, follow-up)
[ ] Implement command word parsing
[ ] Test dispatch (token_id → real phone)

WEBSITE SYSTEM:
[ ] Deploy Netlify vertical templates (trades, shops, restaurants)
[ ] Build Schema.org dynamic generation
[ ] Create 60-second deploy from voice note
[ ] Setup auto-update on specials/orders

SOCIAL AUTOMATION:
[ ] Integrate Buffer API
[ ] Build content generator (Qdrant + Plaud → posts)
[ ] Create vertical hashtag sets
[ ] Setup scheduling (optimal times)
[ ] Implement auto-reply logic

EMAIL AUTOMATION:
[ ] Integrate Brevo API
[ ] Deploy template library (50+ templates)
[ ] Build segmentation engine
[ ] Setup campaign workflows
[ ] Configure A/B testing

ROBOQUILL INTEGRATION:
[ ] Setup handwritten card API
[ ] Build trigger system (happy moments)
[ ] Create card templates
[ ] Test end-to-end (voice → card → post)

SUCCESS CRITERIA:
- WhatsApp tasks sending correctly
- Websites deploying in < 60 seconds
- Social posts generating automatically
- Emails sending with proper segmentation
- Roboquill cards triggering

12.3 TIER 3: AEO & ONBOARDING (SUNDAY–MONDAY)

AEO IMPLEMENTATION:
[ ] Build Schema.org generator (LocalBusiness, Service, FAQ)
[ ] Create atomic answer formatter
[ ] Implement freshness triggers (daily updates)
[ ] Setup E-E-A-T signals
[ ] Configure citation velocity

ONBOARDING FLOW:
[ ] Build "Life Goals" interview (voice-to-JSON)
[ ] Create greenfield vs integration detection
[ ] Setup free 12-month greenfield flow
[ ] Build paid integration flow
[ ] Implement Xero/API connections

SIGNPOSTING LOGIC:
[ ] Build "better alternative" detector
[ ] Create referral system (to other providers)
[ ] Implement win-win validation
[ ] Setup radical honesty checks

DASHBOARD:
[ ] Build client-facing dashboard (Next.js)
[ ] Create week-1 wins display
[ ] Implement real-time metrics
[ ] Setup automated reporting

SUCCESS CRITERIA (MONDAY EOD):
- One real customer running end-to-end
- £340+ recovered showing in dashboard
- AI citations tracked
- Handwritten card sent
- Direct order flow live
- Customer can see their life goals progress

================================================================================
SECTION 13: TEAM STRUCTURE & SCALING
================================================================================

13.1 PHASE 1: SOLO (0-50 CLIENTS)

EWAN (YOU):
- Architecture decisions
- Client relationships
- Sales
- Quality control
- 10-15 videos/week (if doing video production)

CAPACITY: 50 clients max

13.2 PHASE 2: FIRST HIRE (50-100 CLIENTS)

MARKETING MANAGER:
- £35,000-45,000/year
- Full-time
- Handles: Content, campaigns, reporting
- You focus: Strategy, sales, architecture

CAPACITY: 100 clients

13.3 PHASE 3: SPECIALISTS (100-200 CLIENTS)

CONTENT CREATOR:
- £25,000-30,000/year
- Writes blog posts, emails, social
- Supports 100+ clients

SEO SPECIALIST:
- £30,000-40,000/year
- Keyword research, technical SEO, link building
- Supports 75+ clients

CAPACITY: 200 clients

13.4 PHASE 4: SCALE (200+ CLIENTS)

SECOND MARKETING MANAGER
VIDEO PRODUCER
CUSTOMER SUCCESS MANAGER

CAPACITY: 500+ clients

================================================================================
SECTION 14: RISK MITIGATION
================================================================================

14.1 TECHNICAL RISKS

AI HALLUCINATION:
- Mitigation: Deterministic rubrics first
- Confidence levels on all outputs
- Human review for high-stakes decisions

TOOL DOWNTIME:
- Mitigation: Multiple providers (HeyGen, Synthesia backup)
- Local caching of critical data
- Graceful degradation

DATA LOSS:
- Mitigation: Daily backups, 30-day retention
- Off-site backup storage
- Disaster recovery plan

14.2 BUSINESS RISKS

CLIENT CHURN:
- Mitigation: High switching costs (integrated data)
- Month-to-month (no lock-in, but value keeps them)
- Regular check-ins

PRICE INCREASES:
- Mitigation: Annual contracts lock rates
- Alternative tools identified
- Cost passed to clients gradually

QUALITY INCONSISTENCY:
- Mitigation: Strict templates, checklists
- QA process (review before delivery)
- Client feedback loop

14.3 COMPLIANCE RISKS

GDPR BREACH:
- Mitigation: MCP barrier, pseudonymization
- Regular audits
- Data protection officer (you)

VOICE RECORDING CONSENT:
- Mitigation: Automated announcement
- Staff opt-out
- Owner control

================================================================================
SECTION 15: MONDAY BETA SUCCESS CRITERIA
================================================================================

THE ONE REAL CUSTOMER TEST:

By Monday EOD, one real customer must be running end-to-end with:

[ ] Voice capture working (Plaud → transcription)
[ ] Token ID system operational
[ ] MCP barrier functioning
[ ] WhatsApp tasks sending
[ ] £340+ recovered showing in dashboard
[ ] AI citations tracked (7+)
[ ] Handwritten card sent (Roboquill)
[ ] Direct order flow live
[ ] Customer can see life goals progress
[ ] Customer approves of the experience

IF THIS WORKS:
- We have product-market fit
- We can scale
- We can raise investment
- We can help thousands of businesses

IF THIS FAILS:
- Debug immediately
- Fix blockers
- Retry Tuesday
- Do not scale until it works

================================================================================
SECTION 16: COMPLETE FILE MANIFEST
================================================================================

DOCUMENTS CREATED TONIGHT:

1. amplified_conclusions_tonight.md
   - Summary for AI agents

2. amplified_demo_psychology_brief.md
   - Psychology of demo videos
   - Cognitive load theory
   - Emotional engagement
   - Trust building

3. ai_video_tools_recommendation.md
   - HeyGen, Runway, Descript comparison
   - Hollywood prompt formulas
   - Production workflow

4. generic_video_prompt_template.md
   - Reusable framework for all clients
   - 80/20 approach
   - Camera angles, lighting, style library

5. amplified_video_production_model.md
   - Central subscription model
   - Economics
   - Hyper-local strategy

6. amplified_full_stack_marketing.md
   - 14 marketing disciplines
   - AI-human partnership framework
   - Pricing tiers

7. amplified_complete_digital_marketing_suite.md
   - Everything in one document

8. THIS DOCUMENT (THE DEFINITIVE MASTER)
   - Complete technical specification
   - Executable build plan

================================================================================
END OF DEFINITIVE MASTER DOCUMENT
27 February 2026 — MAC MINI BUILD COMMENCING
================================================================================

---

## Gemini

This is a monumental brief. It’s clear, deterministic, and—most importantly—executable. Since it is Friday and we are targeting a Monday Beta, we are officially in **Sprints Mode**.

I have ingested the **Definitive Master Document**. To get the Mac Mini and the Hetzner production hub talking via Railway/Tailscale, we need to lay the foundation of the **MCP Barrier** and the **Identity Vault** first.

Here is the immediate technical execution for **Tier 1 (Friday Night / Saturday Morning)**.

-----

## 🛠 Tier 1 Execution: The "Nervous System" Setup

### 1\. The Identity Vault (Postgres Schema)

The AI must never see a name. We need to initialize the database that maps real identities to the 4-word tokens.

```sql
-- Connect to your Railway/Hetzner Postgres instance
CREATE TABLE client_identities (
    id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    token_id TEXT UNIQUE NOT NULL, -- The 4-word ID (e.g., 'silent-ocean-deep-river')
    real_name TEXT NOT NULL,
    phone_number TEXT NOT NULL,
    email TEXT NOT NULL,
    business_type TEXT,
    created_at TIMESTAMP WITH TIME ZONE DEFAULT CURRENT_TIMESTAMP
);

CREATE INDEX idx_token_id ON client_identities(token_id);
```

### 2\. The MCP Server (The Security Gateway)

This is a Node.js/Express server (or Python FastAPI as per your spec) that acts as the "Bouncer." Claude and I will query *this*, not the database.

**File: `mcp-gateway/index.js`**

```javascript
const express = require('express');
const { Pool } = require('pg');
const app = express();
const PORT = process.env.PORT || 3000;

// Database connection
const pool = new Pool({
  connectionString: process.env.DATABASE_URL,
});

app.use(express.json());

// API Key Middleware for the AI Swarm
const authenticateAI = (req, res, next) => {
  const apiKey = req.header('X-SWARM-KEY');
  if (apiKey !== process.env.SWARM_SECRET) return res.status(401).send('Unauthorized');
  next();
};

// GET Context (AI-Safe: No PII)
app.get('/context/:token_id', authenticateAI, async (req, res) => {
  const { token_id } = req.params;
  // Logic to pull from Qdrant/Neo4j context pool based on token_id
  // Returning dummy data for Tier 1 test
  res.json({
    token_id,
    business_goals: "Work 3 days/week, reach £100k ARR",
    last_action: "Sent invoice for boiler repair",
    risk_level: "Low"
  });
});

app.listen(PORT, () => console.log(`MCP Barrier active on port ${PORT}`));
```

### 3\. Railway Deployment Strategy

1.  **Connect GitHub:** Create a repo named `amplified-mcp-core`.
2.  **Railway Link:** Link the repo to Railway.
3.  **Environment Variables:**
      * `DATABASE_URL`: (From your Postgres service)
      * `SWARM_SECRET`: A long, random string.
      * `PORT`: `3000`

-----

## 🛰 The Tailscale Bridge

To make your **Mac Mini (Local Mastermind)** and **Hetzner (Cloud Production)** feel like they are on the same desk:

1.  **Install Tailscale** on the Mac Mini and the Hetzner CX42.
2.  **MagicDNS:** Enable it in the Tailscale admin console.
3.  **Ping Test:** Ensure the Mac Mini can reach the Hetzner internal IP without being exposed to the public internet.

-----

## 🎙 Voice Pipeline (Hetzner Docker)

On your Hetzner instance, we need to pull the Faster-Whisper image to handle the Plaud uploads.

**Run this on Hetzner:**

```bash
docker run -d -p 5000:5000 --name whisper-engine \
  -e MODEL=small-v3-turbo \
  fedirz/faster-whisper-server:latest
```

-----

## 📈 Friday Night Success Checklist

  * [ ] **Postgres** is live on Railway/Hetzner.
  * [ ] **MCP Gateway** returns a JSON object for a test `token_id`.
  * [ ] **Tailscale** shows both the Mac Mini and Hetzner as "Online."
  * [ ] **Whisper** container is responding to health checks.

**How would you like to handle the generation of the 4-word token IDs? Should I create a script to pre-generate 10,000 unique combinations so we can start assigning them to your first batch of clients?**

---

## You

What does the server actually do? (e.g., is this the MCP server, the WhatsApp webhook receiver, the transcription API endpoint, or something else from the Amplified stack?)
What dependencies are you using? (e.g., Express, Fastify, any specific SDKs?)
What environment variables does it need? (e.g., API keys, database URLs)
If you can point me to what you and another AI built last night, or paste the relevant code here, I can clean it up, make it Railway-ready, and give you the complete files to drop straight in.
What are we deploying?

---

## Gemini

Since you and Claude were "cooking" last night, let's define exactly what this server is: **It is the "Brain" (The Amplified Core Orchestrator).**

In the context of your Master Document, this server acts as the **MCP Gateway** and the **Traffic Controller**. It's the piece that sits between the outside world (WhatsApp/Plaud) and your private data (The Identity Vault).

-----

### 1\. What are we deploying?

We are deploying the **Amplified Core API**. Its job is to:

  * **Anonymize Data:** Take a voice note, swap "John Smith" for a 4-word ID, and send it to the LLM.
  * **Route Tasks:** Receive a command from the AI (e.g., "Send quote") and push it to the WhatsApp API.
  * **Manage the Rubric:** Run the deterministic logic (Hormozi/Dalio principles) on incoming data.

### 2\. The Tech Stack & Dependencies

To keep it fast and Railway-compatible, we’re using **Node.js** with these core dependencies:

  * `express`: The web framework.
  * `pg`: To talk to your Identity Vault (Postgres).
  * `axios`: To talk to the Whisper Transcription engine on Hetzner.
  * `dotenv`: For managing your secrets.
  * `helmet`: Basic security for the API.

### 3\. Required Environment Variables (Railway Config)

You'll need to plug these into your Railway "Variables" tab:

  * `DATABASE_URL`: Your Postgres connection string.
  * `WHATSAPP_API_TOKEN`: Your Meta/WhatsApp Business key.
  * `WHISPER_URL`: The IP address of your Hetzner box running Faster-Whisper.
  * `SWARM_API_KEY`: A secret key you create so only *your* AI agents can talk to the server.

-----

### 🛠 The "Railway-Ready" Boilerplate

Here is the clean, structured code for your `index.js`. You can drop this into your repo right now to get the skeleton live.

```javascript
const express = require('express');
const helmet = require('helmet');
const { Pool } = require('pg');
require('dotenv').config();

const app = express();
const PORT = process.env.PORT || 3000;

// 1. Database Connection (The Identity Vault)
const pool = new Pool({
  connectionString: process.env.DATABASE_URL,
});

app.use(helmet());
app.use(express.json());

// 2. The Identity Shield Middleware (The MCP Barrier)
// Ensures AI never sees PII (Personally Identifiable Information)
const mcpBarrier = (req, res, next) => {
  const apiKey = req.headers['x-amplified-auth'];
  if (apiKey !== process.env.SWARM_API_KEY) {
    return res.status(401).json({ error: 'Unauthorized access to the Vault' });
  }
  next();
};

// 3. ROUTES
// Health Check
app.get('/', (req, res) => res.send('Amplified Core OS: Operational'));

// Transcription Webhook (Receives from Plaud/Whisper)
app.post('/api/v1/voice-in', async (req, res) => {
  const { audioUrl, clientId } = req.body;
  console.log(`Processing voice for Client: ${clientId}`);
  // Logic to send to Hetzner Whisper container goes here
  res.status(202).json({ status: 'Processing audio...' });
});

// WhatsApp Webhook (Task Output)
app.post('/api/v1/whatsapp-out', mcpBarrier, async (req, res) => {
  const { tokenId, message } = req.body;
  // Logic to look up real phone number from token and send via Meta API
  res.json({ status: 'Message routed to client' });
});

app.listen(PORT, () => {
  console.log(`🚀 Amplified Core running on port ${PORT}`);
});
```

### 📂 File Manifest for your Repo:

1.  `index.js` (The code above)
2.  `package.json` (Includes `express`, `pg`, `axios`, `dotenv`, `helmet`)
3.  `.gitignore` (Must include `node_modules` and `.env`)
4.  `Procfile` (Optional, but good for Railway: `web: node index.js`)

-----

**Would you like me to generate the `package.json` and a setup script to automate the 4-word token generation for your first 100 clients?**


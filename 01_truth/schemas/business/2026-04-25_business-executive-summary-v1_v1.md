---
title: "YOUR COMPLETE SYSTEM: EXECUTIVE SUMMARY"
id: "business-executive-summary-v1"
version: 1
created: "2026-04-25"
type: "document"
topic_type: "summary"
audience: "internal"
layer: "truth"
status: "filed"
signed_by: "Devon, 2026-04-25, devin-992682c244cf444f91e0a516498afbfd"
---

# YOUR COMPLETE SYSTEM: EXECUTIVE SUMMARY
## What You're Building & How to Win

---

## THE CONVERSATION (What We Just Figured Out)

### Your Starting Position
- **You:** Business consultant, Newcastle, expertise in systems/optimization
- **Goal:** Build recurring revenue business + help clients do the same
- **Timeline:** Achievable THIS WEEK, robust and chargeable, results-focused
- **Constraint:** You don't want to build manually, Kilo Code will code it

### What We Researched
- 2026 outbound marketing techniques (AI-personalization, intent signals, multi-channel)
- Best-in-class tools for cold email automation
- Pricing models for consultant services
- Technical architecture for scalable lead generation systems

### What We Built (3 Documents)

**1. Business Consultant Playbook (3,200 words)**
- How you position yourself: "AI-Powered Lead Engine" for service businesses
- Service model: £3,000 setup + £600/month recurring
- Revenue path: 1 client by Week 3, 15-20 clients by Month 4 = £10K/month
- Diagnosis-first approach: You research their revenue leaks, diagnose problems, reach out with solution

**2. Kilo Code Technical Specification (2,800 words)**
- 6 core systems to build: research → diagnosis → email gen → orchestration → reply analysis → reporting
- API stack: Perplexity (research), Claude (diagnosis), Instantly (email), Pipedrive (CRM), Cal.com (booking)
- 6-week timeline: 2 weeks core build, 1 week client delivery, 1 week testing, 2 weeks polish
- Success criteria: Can run 20 prospects through full pipeline in <5 minutes

**3. 7-Day Action Plan (2,000 words)**
- Tonight: Send docs to Kilo Code, start your outbound via Lindy + Instantly
- Mon-Fri: Email setup, prospect list, send first 45 prospects
- Week 2: Book discovery calls, close first client, onboard
- By Month 4: 15-20 clients, £6-12K/month recurring, fully automated

### The Stack You're Using
- **For Your Outbound:** Lindy AI (workflow) + Instantly.ai (email sending) + Claude API (generation) + Perplexity (research)
- **For Clients:** Same tools, but systematized by Kilo Code
- **Cost:** ~£229/month to get yourself clients, ~£214/month per client to deliver

### Why This Works
1. **Simple:** One service (lead automation), not everything
2. **High margin:** You pay £214/month, client pays £600+
3. **Recurring:** Predictable £600/month × 15-20 clients = £10K/month
4. **Automatable:** Kilo Code builds the system once, you sell it 20 times
5. **Results-driven:** Clients see meetings booked, revenue generated, ROI clear

---

## YOUR OPTIMAL CLAUDE DESKTOP PROJECT SETUP

### Project Structure (In Claude Desktop)

Create one main project with these artifacts:

```
EWAN_BRAMLEY_BUSINESS_SYSTEM/
├── 00_MASTER_PLAYBOOK.md (this document)
├── 01_BUSINESS_MODEL.md (who you are, what you sell, pricing)
├── 02_SALES_SCRIPT.md (discovery call script + positioning)
├── 03_MARKETING_COPY.md (email templates, subject lines, messaging)
├── 04_CLIENT_WORKFLOWS.md (how to onboard clients step-by-step)
├── 05_KILO_CODE_BRIEF.md (what to build, technical spec)
├── 06_DAILY_CHECKLIST.md (daily/weekly/monthly tasks)
├── 07_METRICS_TRACKER.md (what to measure, target numbers)
└── 08_PROMPTS.md (Claude prompts for email generation, diagnosis, etc.)
```

### How to Use Claude for Maximum Impact

#### Session Type 1: Email Generation (Run Every Morning)

**Prompt in Claude:**
```
You are Ewan Bramley's cold email copywriter for B2B consulting outbound.

PROSPECT DATA:
- Name: [NAME]
- Company: [COMPANY]
- Industry: [INDUSTRY]
- Revenue: [ESTIMATED]
- Website: [SITE]

YOUR DIAGNOSIS (from research):
- They're leaving £[X] on the table in [REVENUE_LEAK]
- Current state: [CURRENT_METRICS]
- Opportunity: [IF_THEY_FIXED_THIS]

REQUIREMENTS:
- 3-4 sentences max
- Reference specific diagnosis point
- Sound like human (not AI)
- Include calendar link call to action
- No generic opening
- Subject line included

Write the email now.
```

**When:** Every morning before sending batch
**Output:** Copy-paste ready email → review → approve → send
**Time:** 2 minutes per prospect, 20 prospects = 40 minutes

#### Session Type 2: Diagnosis Generation (Run After Research)

**Prompt in Claude:**
```
I've researched this business. Here's what I found:

COMPANY: [COMPANY]
Website content: [SUMMARY]
LinkedIn profile: [INFO]
Employees: [COUNT]
Estimated revenue: [ESTIMATE]
Industry benchmarks: [DATA_FROM_PERPLEXITY]

Based on this research, identify:
1. **5-6 revenue leaks** (specific problems they likely have)
2. **For each leak:**
   - What it is
   - What it costs them annually
   - How to fix it
   - Revenue impact if fixed

Format as JSON for my database.
```

**When:** After research phase, before email generation
**Output:** Structured diagnosis → database → used in email
**Time:** 5 minutes per prospect

#### Session Type 3: Campaign Strategy (Run Weekly)

**Prompt in Claude:**
```
CAMPAIGN METRICS (Last Week):
- Emails sent: [X]
- Open rate: [%]
- Click rate: [%]
- Reply rate: [%]
- Discovery calls booked: [X]
- Conversion rate to client: [%]

Analyze and recommend:
1. What's working? (top performing emails/subjects)
2. What's failing? (low performing aspects)
3. Should we scale? How?
4. What to change for next week?

Focus on: reply rate, discovery call booking, ROI
```

**When:** Every Friday evening
**Output:** Weekly optimization report
**Time:** 15 minutes

#### Session Type 4: Reply Analysis (Run Daily)

**Prompt in Claude:**
```
CLIENT REPLIES (Last 24 hours):

[PASTE ALL REPLIES]

For each reply, categorize:
- Intent score (0-100)
- Category (hot/warm/cold/objection/out-of-office)
- What they're asking
- What I should do

Format as quick action list for me.
```

**When:** Each morning while checking email
**Output:** Action items → prioritize who to call
**Time:** 5 minutes

#### Session Type 5: Client Onboarding (Run Once Per Client)

**Prompt in Claude:**
```
NEW CLIENT SETUP:

Company: [NAME]
Industry: [INDUSTRY]
Current meetings/month: [X]
Target: 10-15/month
Deal size: [£]
Timeline: 90 days

Create:
1. Client prospect list (50 ideal customers)
2. Messaging framework (3 angles to reach them)
3. Campaign calendar (8-week rollout plan)
4. Success metrics (what we're measuring)
5. Weekly reporting template

This is for me to hand to Kilo Code's system.
```

**When:** After you close a client
**Output:** Client package ready to go
**Time:** 30 minutes

### Claude Desktop MAX Plan Configuration

**What to Enable:**
1. **Extended thinking** (turned ON) - For diagnosis analysis
2. **Code execution** (turned ON) - For data transformation
3. **Web search** (turned ON) - For research backup
4. **File upload** (turned ON) - To upload prospect CSVs

**Project Instructions (System Prompt):**
```
You are Ewan's business automation assistant.

Your role:
1. Generate hyper-personalized cold emails (based on diagnosis)
2. Analyze prospect research and diagnose revenue leaks
3. Score email replies for intent and urgency
4. Recommend campaign optimizations
5. Create client onboarding packages

Always:
- Be specific and quantified (not generic)
- Reference actual research (no made-up numbers)
- Sound like a human consultant (not AI)
- Focus on revenue impact
- Format for easy copy-paste into tools

Current business model:
- Service: AI-Powered Lead Engine
- Price: £3,000 setup + £600/month
- Target: Service-based businesses (agencies, consultants)
- Goal: 10-15 qualified meetings/month per client
```

---

## YOUR COMPLETE EXECUTION MAP

### Phase 1: YOU GET CLIENTS (Week 1-4)
**Timeline:** This week onwards  
**Tools:** Lindy AI + Instantly.ai + Claude + Perplexity  
**Goal:** Close first paying client (£600/month)

**Daily routine:**
1. **Morning (10 min):** Check Instantly dashboard (opens/clicks/replies)
2. **Mid-morning (20 min):** Generate emails via Claude for next 20 prospects
3. **Afternoon (10 min):** Run Lindy workflow → send batch
4. **Evening (10 min):** Review replies, respond to warm ones, schedule calls

**Weekly:**
1. Monday: Send 30-50 prospects
2. Tuesday-Thursday: Monitor + respond
3. Friday: Review metrics, book discovery calls

**Result:** 15-20 prospects → 2-3 replies → 1 discovery call → 25% close = 1 client

### Phase 2: KILO CODE BUILDS (Weeks 1-6 Parallel)
**Timeline:** Send spec tonight, delivery mid-Feb  
**What they build:** 6-system automation platform  
**Your job:** Provide feedback, test, iterate

**What you're building:**
1. Prospect research engine (website scraping + Perplexity API)
2. AI diagnosis system (Claude-powered revenue leak detection)
3. Email generation (Claude API + personalization)
4. Campaign orchestration (CSV → send → track → report)
5. Reply analysis (Claude intent scoring + auto-qualification)
6. Client dashboard (white-label reporting)

**Deliverables:**
- Week 2: Core engine working (can diagnose 1 prospect end-to-end)
- Week 3-4: Client delivery system (can onboard 1 test client)
- Week 5-6: Dashboard + reporting (client sees metrics live)

### Phase 3: YOU SCALE CLIENTS (Week 4+)
**Timeline:** Once you have 1 client + Kilo Code system ready  
**Tools:** Kilo Code system + Lindy + Instantly  
**Goal:** 5-10 clients by Month 2, 15+ by Month 4

**New client flow:**
1. Discovery call (15 min)
2. Proposal + close (30 min)
3. Kilo Code system: upload their prospect CSV → auto-researches → auto-diagnoses → auto-generates → sends (5 min)
4. You monitor replies, book their meetings (5 min/week per client)
5. Weekly reporting (10 min per client)

**Time per client:** ~6 hours initial setup + 3 hours/month ongoing

**Revenue:** 15 clients × £600/month = £9,000/month recurring

---

## CRITICAL SUCCESS FACTORS

### Non-Negotiable Rules
1. **Never exceed 50 emails/day per account** → Spam folder death
2. **Always warm up new domains** → 14 days minimum before cold email
3. **Always personalize** → Generic emails = ignored
4. **Always respond to warm replies** → Within 2 hours
5. **Always follow up** → 5+ touches per prospect minimum
6. **Never promise guarantees** → Say "typically 10-15 meetings/month"

### What Kills Most People (Avoid These)
- Trying to build everything themselves (you're not → Kilo Code)
- Waiting for perfect system before starting (start THIS WEEK)
- Sending without warmup (burn domain → starts over)
- Over-personalizing manually (use Claude API at scale)
- Not tracking metrics (you can't optimize what you don't measure)
- Giving up after 2 weeks (campaigns need 4-5 weeks to show results)

---

## YOUR METRICS DASHBOARD

### Daily Metrics (Track Every Day)
```
Emails sent: [X]
Open rate: [%] (target: 40%+)
Click rate: [%] (target: 10%+)
Reply rate: [%] (target: 10%+)
Intent score >70 (hot leads): [X]
Discovery calls booked: [X]
```

### Weekly Metrics (Review Every Friday)
```
Total prospects contacted: [X]
Total replies: [X]
Reply rate: [%]
Discovery calls: [X]
Conversion to client: [%]
New revenue: [£X]
```

### Monthly Metrics (Strategic Review)
```
Prospects contacted: [X]
Clients closed: [X]
Monthly recurring revenue: [£X]
Cost per client: [£X]
Profit per client: [£X]
```

### Success Targets by Week
```
Week 1: 50 prospects contacted, 0 clients (building)
Week 2: 100 total prospects, 1 discovery call
Week 3: 150 total prospects, 2-3 discovery calls, 1 client closed
Week 4: 200 total prospects, 3-4 discovery calls, 2-3 clients
Month 2: 400 total, 4-5 clients, £2,400/month revenue
Month 3: 600 total, 6-8 clients, £3,600-4,800/month revenue
Month 4: 800 total, 10+ clients, £6,000+/month revenue
```

---

## KILO CODE: THE HANDOFF

### What You Send Tonight
1. **business_consultant_playbook.md** (your service model)
2. **kilo_code_technical_spec.md** (exact systems to build)
3. **Message:** "Can you build this in 6 weeks? What's the cost?"

### What They Build
- **Phase 1 (Weeks 1-2):** Research + diagnosis + email generation engines
- **Phase 2 (Week 3):** Campaign orchestration + Instantly integration
- **Phase 3 (Week 4):** Reply analysis + auto-qualification
- **Phase 4 (Weeks 5-6):** Client dashboard + automated reporting

### Success = You Can
- [ ] Upload CSV of 50 prospects
- [ ] System researches + diagnoses + generates emails in <10 minutes
- [ ] You review + approve in 5 minutes
- [ ] System sends via Instantly (tracked automatically)
- [ ] Dashboard shows opens/clicks/replies/intent live
- [ ] Weekly report auto-generated

---

## THE REAL GAME

**Month 1:** You're getting 1 client, making £600/month
**Month 2:** 4-5 clients, £2,400-3,000/month recurring
**Month 3:** 8-10 clients, £4,800-6,000/month recurring
**Month 4:** 15-20 clients, £9,000-12,000/month recurring

**Your effort at Month 4:** 25-30 hours/month total
- Sales/outbound: 10 hours/month (still prospecting for new clients)
- Client onboarding: 6-8 hours/month (1-2 new clients)
- Monitoring: 8-12 hours/month (3-5 min per client per week)

**Your profit at Month 4:** £6,000-10,000/month (recurring)
- Minus tool costs: ~£500/month (Lindy, Instantly×20 clients, APIs)
- Minus Kilo Code maintenance: ~£500/month
- = £5,000-9,000/month profit

**This is a consultant business with SaaS margins. That's the game.**

---

## YOUR NEXT 3 STEPS (Right Now)

**Step 1 (Tonight - 10 min):**
- Send Kilo Code the technical spec
- Ask: "Can you build this? Timeline? Cost?"

**Step 2 (Tonight - 20 min):**
- Buy baselayer.co domain (£10)
- Create Lindy.ai account (free)
- Create Instantly.ai account (£99)

**Step 3 (Monday morning):**
- Set up 3 Gmail accounts for cold email
- Add to Instantly, start warmup
- Build Lindy workflow using Claude prompts

**By Friday:** First 50 prospects contacted  
**By Week 3:** First client discovery call booked  
**By Month 2:** First client paying, Kilo Code system ready  
**By Month 4:** 15-20 clients, £10K/month recurring

---

## WHY THIS WILL WORK

1. **You have the positioning** (business consultant helping other consultants)
2. **You have the service** (lead generation automation)
3. **You have the pricing** (£3K + £600/month = £7.2K/year per client)
4. **You have the tools** (Lindy, Instantly, Claude, Perplexity all available)
5. **You have the developer** (Kilo Code to build the system)
6. **You have the playbook** (3 detailed documents above)

All you need to do is:
- Start outbound THIS WEEK (you have everything needed)
- Book your first discovery call (1 call per week for 4 weeks = 4 calls = 1 close)
- Deliver results to first client (they get 10-15 meetings/month)
- Sell to clients #2-20 (copy-paste the first one 19 more times)

**This is completely achievable. Go.**
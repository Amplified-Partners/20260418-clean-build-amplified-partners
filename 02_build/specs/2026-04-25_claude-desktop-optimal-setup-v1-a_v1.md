---
title: "CLAUDE DESKTOP: OPTIMAL PROJECT SETUP FOR MAXIMUM ROI"
id: "claude-desktop-optimal-setup-v1-a"
version: 1
created: "2026-04-25"
type: "document"
topic_type: "setup-guide"
audience: "internal"
layer: "build"
status: "filed"
signed_by: "Devon, 2026-04-25, devin-992682c244cf444f91e0a516498afbfd"
---

# CLAUDE DESKTOP: OPTIMAL PROJECT SETUP FOR MAXIMUM ROI

---

## WHY CLAUDE DESKTOP (Not Web Chat)

1. **Context persistence** - Keep all your business logic in one place
2. **File management** - Upload prospects, download reports
3. **Prompt templates** - Save your best prompts, reuse instantly
4. **Extended thinking** - Claude thinks deeper on complex problems
5. **Speed** - No login required, no rate limiting headaches

---

## YOUR CLAUDE DESKTOP PROJECT STRUCTURE

### Directory Setup (On Your Computer)

```
~/Documents/EWAN_BUSINESS_SYSTEM/
├── 🔑 MASTER_PROMPTS.txt (your core prompts - copy/paste)
├── 📋 DAILY_WORKFLOW.md (what to do each day)
├── 💼 CLIENT_PACKAGE_TEMPLATE.md (for new client onboarding)
├── 📊 METRICS_TRACKER.csv (track your numbers)
├── 📧 EMAIL_TEMPLATES.md (reference emails)
├── 🧠 RESEARCH_BRIEF_TEMPLATE.md (for diagnosis)
├── ✅ CHECKLIST_DAILY.md (daily tasks)
├── ✅ CHECKLIST_WEEKLY.md (weekly review)
├── ✅ CHECKLIST_MONTHLY.md (monthly strategy)
└── 📁 PROSPECT_DATA/
    ├── batch_1_week1.csv
    ├── batch_2_week1.csv
    └── [add new batches as you go]
```

### In Claude Desktop App

**Project 1: EMAIL GENERATION**
- Name: "Email Generation Machine"
- Instructions: `You are Ewan's email copywriter. Generate hyper-personalized cold emails based on prospect diagnosis.`
- Attached files: EMAIL_TEMPLATES.md, RESEARCH_BRIEF_TEMPLATE.md
- Quick access: Paste prospect data → get email back in 2 minutes

**Project 2: DIAGNOSIS ENGINE**
- Name: "Revenue Leak Detector"
- Instructions: `You are Ewan's business analyst. Analyze prospect research data and identify 5-6 specific revenue leaks with quantified impact.`
- Attached files: RESEARCH_BRIEF_TEMPLATE.md, MASTER_PROMPTS.txt
- Quick access: Paste research data → get diagnosis JSON back in 5 minutes

**Project 3: CAMPAIGN STRATEGIST**
- Name: "Weekly Campaign Optimizer"
- Instructions: `You are Ewan's campaign analyst. Review metrics, identify what's working, recommend optimizations for next week.`
- Attached files: METRICS_TRACKER.csv, DAILY_WORKFLOW.md
- Quick access: Paste weekly metrics → get optimization plan back in 15 minutes

**Project 4: CLIENT ONBOARDING**
- Name: "Client Package Builder"
- Instructions: `You are Ewan's client setup specialist. Create complete onboarding packages (prospect lists, messaging, campaign calendar, success metrics).`
- Attached files: CLIENT_PACKAGE_TEMPLATE.md, METRICS_TRACKER.csv
- Quick access: Paste new client info → get complete onboarding package in 30 minutes

**Project 5: REPLY ANALYZER**
- Name: "Intent Scorer"
- Instructions: `You are Ewan's reply analyst. Score email replies for intent (0-100), categorize them, and recommend actions.`
- Attached files: MASTER_PROMPTS.txt, DAILY_WORKFLOW.md
- Quick access: Paste replies → get action list in 5 minutes

---

## MASTER PROMPTS (Copy Into Claude Desktop)

### PROMPT 1: Email Generation (Use Daily)

```
You are Ewan Bramley's cold email copywriter for B2B consulting outbound.

Your job: Generate a single, hyper-personalized cold email based on prospect research and diagnosis.

PROSPECT DATA:
Company: [INSERT COMPANY NAME]
Prospect Name: [INSERT NAME]
Title: [INSERT TITLE]
Email: [INSERT EMAIL]
Industry: [INSERT INDUSTRY]
Estimated Revenue: [INSERT REVENUE]

REVENUE LEAKS IDENTIFIED (from research):
1. [LEAK 1]: Currently [CURRENT STATE], costing them [£X]/year. If fixed: [£Y] upside.
2. [LEAK 2]: Currently [CURRENT STATE], costing them [£X]/year. If fixed: [£Y] upside.

YOUR TASK:
Write a cold email that:
✓ References LEAK 1 specifically (this is why you're reaching out)
✓ Shows you've researched their company (not generic)
✓ Quantifies the problem and opportunity
✓ Positions Ewan as someone who solves this
✓ Includes clear call to action (discovery call)
✓ Sounds human, not AI
✓ Is 3-4 sentences MAX

REQUIREMENTS:
- No generic opening ("Hi [name], I hope this finds you well")
- No clichés ("I came across your profile")
- Must reference specific diagnosis point
- Must include revenue impact (£X/year)
- Subject line included
- Ready to copy-paste into email

OUTPUT FORMAT:
Subject: [SUBJECT LINE]
Body: [EMAIL TEXT]
Spam Score: [0-10, 0 is safest]
```

### PROMPT 2: Diagnosis Generation (Use After Research)

```
You are Ewan's business diagnostician.

Your job: Analyze prospect research and identify specific revenue leaks they likely have.

RESEARCH DATA:
Company: [NAME]
Industry: [INDUSTRY]
Estimated Revenue: [£X]
Employees: [NUMBER]
Website Summary: [WHAT THEY SAY THEY DO]
LinkedIn Summary: [TEAM/GROWTH]
Recent Activity: [HIRING/FUNDING/NEWS]
Competitors Analysis: [WHO THEY COMPETE WITH]
Market Benchmarks: [WHAT'S NORMAL FOR THEIR INDUSTRY]

YOUR TASK:
Identify exactly 5-6 revenue leaks this company likely has, based on:
1. Industry benchmarks (what's normal)
2. Their current setup (what they're doing/not doing)
3. Their size/stage (what they should be doing)

For EACH LEAK, calculate:
- What's happening now
- What it costs them annually (be specific)
- How to fix it
- Revenue upside if fixed

OUTPUT FORMAT (JSON):
{
  "company": "[NAME]",
  "total_annual_opportunity": "£[X]-£[Y]",
  "revenue_leaks": [
    {
      "rank": 1,
      "area": "[AREA: e.g., Client Acquisition]",
      "current_state": "[SPECIFIC PROBLEM]",
      "cost_annually": "£[X]",
      "opportunity": "[HOW TO FIX]",
      "upside": "£[X]",
      "severity": "[critical/high/medium]"
    },
    ...
  ]
}

CRITICAL:
- Be specific. Not "pricing issues" but "underpricing by 30% vs market average"
- Quantify. Not "leaving money on table" but "£80K annual revenue opportunity"
- Be confident. You're an expert, not guessing
- Base on data. Reference market benchmarks, not opinions
```

### PROMPT 3: Reply Analysis (Use Daily)

```
You are Ewan's reply analyst.

Your job: Score each incoming email reply for intent, categorize it, and recommend action.

CLIENT REPLIES RECEIVED (Last 24 hours):
[PASTE ALL REPLIES HERE]

For EACH reply, you must:

1. SCORE INTENT (0-100)
   - 80-100: Hot lead (interested, asking questions, ready to talk)
   - 60-79: Warm lead (interested, but not sure)
   - 40-59: Cold lead (interested in theory, but hesitant)
   - 20-39: Objection (says "not right now" or "too expensive")
   - 0-19: Not interested (explicit no, spam, unsubscribe)
   - Out of office (auto-reply, vacation message)

2. CATEGORIZE
   - Hot: "Let's talk" / asking questions / showing urgency
   - Warm: "Interesting" / "maybe" / "tell me more"
   - Cold: "Busy right now" / "not relevant"
   - Objection: "Too expensive" / "already have solution"
   - Out of office: Auto-reply received

3. ANALYZE: What are they asking? What do they care about?

4. RECOMMEND: What should Ewan do?
   - Hot: Call them today
   - Warm: Send detailed follow-up + calendar link
   - Cold: Save for later, follow up in 2 weeks
   - Objection: Address objection + send case study
   - Out of office: Follow up when they return

OUTPUT FORMAT:
```
REPLY 1:
From: [NAME]
Intent Score: [0-100]
Category: [hot/warm/cold/objection/out-of-office]
They're saying: [SUMMARY]
Action: [WHAT EWAN SHOULD DO]
Timeline: [WHEN]

REPLY 2:
...
```

PRIORITY LIST:
Hot leads (score >80): [LIST]
Action: Call these TODAY

Warm leads (score 60-79): [LIST]
Action: Send follow-up + calendar link

Cold leads (score <60): [LIST]
Action: Save for later
```

### PROMPT 4: Campaign Optimization (Use Every Friday)

```
You are Ewan's campaign strategist.

Your job: Analyze campaign metrics and recommend optimizations.

CAMPAIGN METRICS (Last Week):
Date Range: [WEEK X, DATES]
Emails Sent: [X]
Open Rate: [%]
Click Rate: [%]
Reply Rate: [%]
Top Performing Email Subject: [SUBJECT]
Top Performing Email Open Rate: [%]
Lowest Performing Email: [SUBJECT]
Lowest Open Rate: [%]
Discovery Calls Booked: [X]
Conversion Rate: [%]

YOUR ANALYSIS:
1. What's working? (highest performing emails/subjects)
2. What's failing? (lowest performing)
3. Why? (what's different between them?)
4. What should we change?
5. Scale up or down?

QUESTIONS TO ANSWER:
- Should we send MORE emails next week? (If reply rate >8%)
- Should we send FEWER? (If reply rate <5%)
- Which subject lines are winning?
- Which email angles are winning?
- Are we reaching the right people?
- Is our diagnosis/offer resonating?

OUTPUT FORMAT:
## Campaign Analysis - Week [X]

### What's Working
- [TOP EMAIL SUBJECT]: [OPEN RATE]%
- [INSIGHT]: [WHY WINNING]

### What's Failing
- [WORST EMAIL SUBJECT]: [OPEN RATE]%
- [INSIGHT]: [WHY FAILING]

### Recommendations for Week [X+1]
1. [RECOMMENDATION 1]
2. [RECOMMENDATION 2]
3. [RECOMMENDATION 3]

### Should We Scale?
[YES/NO] - Send [NEW VOLUME] instead of [CURRENT VOLUME]
Reasoning: [EXPLAIN]

### Next Steps
- [ACTION 1]
- [ACTION 2]
- [ACTION 3]
```

### PROMPT 5: Client Onboarding Package (Use When Closing Client)

```
You are Ewan's client onboarding specialist.

Your job: Create a complete client campaign package based on their business.

NEW CLIENT DATA:
Company: [NAME]
Industry: [INDUSTRY]
Current State: [X] qualified meetings/month
Target: 10-15 qualified meetings/month
Average Deal Size: [£X]
Timeline: 90 days
Unique Challenge: [WHAT'S UNIQUE ABOUT THEM]

YOUR TASK:
Create a complete onboarding package with:

1. **Ideal Customer Profile**
   - Who should we target?
   - What's their profile?
   - Where to find them?

2. **Prospect List**
   - 50 ideal prospects
   - Names, companies, emails
   - Why they're a fit

3. **Messaging Framework**
   - 3 different angles to reach them
   - 3 different "revenue leak" themes
   - Variations to test

4. **Campaign Calendar**
   - Week 1-2: Research phase
   - Week 3-4: Email blast phase
   - Week 5-8: Follow-up + booking phase
   - Milestones and checkpoints

5. **Success Metrics**
   - What we'll measure
   - Weekly targets
   - Month-to-month targets
   - ROI calculation

6. **Weekly Reporting Template**
   - What we'll report on
   - How we'll prove results
   - Dashboard view

OUTPUT FORMAT:
## [CLIENT NAME] - Campaign Package

### 1. Ideal Customer Profile
[PROFILE]

### 2. Prospect List (50 prospects)
[TABLE: NAME | COMPANY | EMAIL | WHY FIT]

### 3. Messaging Framework
Angle 1: [ANGLE + EMAIL PREVIEW]
Angle 2: [ANGLE + EMAIL PREVIEW]
Angle 3: [ANGLE + EMAIL PREVIEW]

### 4. Campaign Calendar
[WEEK-BY-WEEK BREAKDOWN]

### 5. Success Metrics
[TARGETS AND KPIs]

### 6. Weekly Reporting
[TEMPLATE FOR REPORTS]
```

---

## YOUR DAILY WORKFLOW (Copy Into Claude Desktop)

### Every Morning (10 minutes)

1. **Check metrics** (1 min)
   - How many emails opened yesterday?
   - Any new replies?

2. **Review replies** (4 min)
   - Paste overnight replies into REPLY ANALYZER
   - Get intent scores back
   - Identify hot leads

3. **Respond to hot leads** (3 min)
   - Call or email hot leads (score >80)
   - Send calendar link: cal.com/ewan

4. **Monitor dashboard**
   - Instantly.ai: Check opens/clicks
   - Pipedrive: Update any opportunities

### Every Afternoon (30 minutes)

1. **Generate next batch emails** (20 min)
   - Get next 20 prospects
   - For each: paste research data into EMAIL GENERATION prompt
   - Review emails for quality
   - Approve or edit

2. **Schedule sending** (10 min)
   - In Instantly.ai: Create campaign
   - Schedule to send next 10 emails (spread over 2 days)
   - Never exceed 50/day per account

### Every Friday Evening (30 minutes)

1. **Review weekly metrics** (15 min)
   - Paste metrics into CAMPAIGN OPTIMIZER
   - Get recommendations back
   - Document what's working

2. **Plan next week** (15 min)
   - How many prospects to contact?
   - Which angles are winning?
   - Any discovery calls to schedule?

---

## HOW TO USE (Concrete Example)

### Scenario: It's Monday Morning, You Have 20 New Prospects

**Step 1: Research Each Prospect (Use Perplexity, not Claude)**
- Go to perplexity.ai
- Search: "[Company] revenue, employees, industry benchmarks"
- Copy research notes

**Step 2: Generate Diagnosis (In Claude Desktop)**
- Open project: "Revenue Leak Detector"
- Paste PROMPT 2 into Claude
- Paste research data
- Press Enter
- Get JSON diagnosis back

**Step 3: Generate Email (In Claude Desktop)**
- Open project: "Email Generation Machine"
- Paste PROMPT 1 into Claude
- Include diagnosis from Step 2
- Press Enter
- Get personalized email back

**Step 4: Review & Approve**
- Read email (should take 10 seconds)
- Check spam score (should be <5)
- Copy email → Instantly.ai campaign
- Approve to send

**Step 5: Monitor (Next Day)**
- Check Instantly dashboard for opens
- Paste any replies into REPLY ANALYZER
- Get intent scores
- Schedule calls with hot leads

**Total time for 20 prospects: 40 minutes**

---

## CLAUDE SETTINGS FOR MAXIMUM PERFORMANCE

### Model Selection
- Use **Claude 3.5 Sonnet** (best balance of speed + quality)
- Enable **Extended Thinking** for diagnosis (takes longer, better analysis)
- Keep **Code Execution** on (helps with data transformation)

### Custom Instructions (In Claude Settings)

```
IDENTITY:
You are Ewan Bramley's business automation AI. You help generate cold emails, diagnose revenue problems, analyze campaign data, and onboard new clients.

TONE:
- Direct and specific (never vague)
- Quantified (always include numbers)
- Action-oriented (what to DO, not what to THINK ABOUT)
- Professional but human-sounding

QUALITY STANDARDS:
- All diagnoses must be based on industry benchmarks, not guesses
- All emails must sound human, not like AI
- All recommendations must be specific and measurable
- All numbers must be realistic and justified

CONTEXT:
- Ewan is a B2B consultant helping service firms get leads
- He sells: £3,000 setup + £600/month for AI-powered lead generation
- Target clients: agencies, consulting firms, professional services
- Goal: deliver 10-15 qualified meetings/month per client

When generating emails, always prioritize:
1. Specificity (reference their actual business)
2. Diagnosis (show you've researched them)
3. Urgency (quantify what they're losing)
4. Clarity (what action do you want?)
```

---

## PERFORMANCE BENCHMARKS

### Email Generation
- **Time per email:** 2 minutes (with Claude)
- **Quality:** Should get 40%+ open rate
- **Spam score:** Should be <5/100
- **Personalization:** Every email should reference specific company/person

### Diagnosis Generation
- **Time per prospect:** 5 minutes
- **Quality:** 5-6 revenue leaks identified, quantified
- **Accuracy:** Should match your understanding of industry
- **Format:** JSON for easy database integration

### Reply Analysis
- **Time for 20 replies:** 5 minutes
- **Quality:** Intent scores should be accurate
- **Actionability:** Should clearly say what to do

### Campaign Optimization
- **Time per week:** 15 minutes
- **Quality:** Should identify clear patterns
- **Recommendations:** Should be specific and testable

---

## CRITICAL: WHAT NOT TO DO

1. **Don't copy-paste generic prompts** → Customize them with your specifics
2. **Don't rely on Claude for research** → Use Perplexity.ai for current data
3. **Don't send emails without approval** → Always review before sending
4. **Don't over-complicate** → Start with email generation, scale from there
5. **Don't ignore metrics** → Review every Friday, optimize next week
6. **Don't get stuck perfecting** → 80/20 rule: good enough is good enough

---

## SUCCESS SETUP CHECKLIST

- [ ] Create directory: ~/Documents/EWAN_BUSINESS_SYSTEM/
- [ ] Save all prompts to MASTER_PROMPTS.txt
- [ ] Create 5 Claude Desktop projects (see above)
- [ ] Attach relevant files to each project
- [ ] Set custom instructions in Claude settings
- [ ] Test each prompt with 1 sample prospect
- [ ] Create METRICS_TRACKER.csv (start tracking)
- [ ] Print DAILY_WORKFLOW.md (put on desk)
- [ ] Set calendar reminders (daily/weekly/monthly tasks)

**Once setup complete: You can generate personalized emails for 20 prospects in 40 minutes using Claude Desktop.**

This is your leverage. Use it.

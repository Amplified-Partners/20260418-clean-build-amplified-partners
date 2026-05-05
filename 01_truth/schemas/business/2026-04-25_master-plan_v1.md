---
title: "MASTER IMPLEMENTATION PLAN"
id: "master-plan"
version: 1
created: "2026-04-25"
type: "document"
topic_type: "strategy"
audience: "internal"
layer: "truth"
status: "filed"
signed_by: "Devon, 2026-04-25, devin-992682c244cf444f91e0a516498afbfd"
---

# MASTER IMPLEMENTATION PLAN
## Ewan's Complete Roadmap: From Today's Work to Â£1M+ Business

---

## THE COMPLETE PICTURE (What You Have)

You now have **complete clarity** on:

âœ“ **Business Model** - 3 revenue streams, Â£101K Year 1 â†’ Â£1M+ Year 3
âœ“ **Operating System** - Ray Dalio's Principles throughout everything
âœ“ **Coaching Methodology** - 5 personas with proven frameworks
âœ“ **Technology** - Local + cloud hybrid, client-private data
âœ“ **Authority Positioning** - Compete on methodology, not price
âœ“ **Website Strategy** - Systems showcase, not sales page
âœ“ **Content Architecture** - Exactly what goes where (the meat for your website bones)
âœ“ **Case Study Framework** - How to build proof of results

**Now comes execution.** This plan tells you exactly what to do, when, and why.

---

## PHASE 1: FOUNDATION (WEEKS 1-4)
### Goal: Build Your Operating System

### Week 1: Document Your Principles (3-5 hours)

**TASK 1: Write Your 5 Principles**

For each, create a document with:
- Criteria (specific, measurable)
- Why it exists (reasoning)
- How you apply it
- Success rate (TBD, tracking from now)
- Last updated date
- Next review date

**Principle 1: CLIENT ACCEPTANCE**
```
I will only accept clients who meet ALL of:
1. Profit margin potential >40% (based on willingness to implement)
2. Owner engagement: Attends Monday meetings, responds <24 hours
3. Team size: 2-10 people
4. Revenue: Â£500K-3M
5. Industry: Service-based SMB

[Complete the template]
```

**Principle 2-5:** Pricing, Hiring, Firing (Clients), Time Allocation
[Complete same template for each]

**Deliverable:** 5-page document with your principles
**Time:** 3-5 hours
**Store in:** Obsidian + backup to GitHub

---

### Week 1: Set Up Your Decision Tracking (2 hours)

**TASK: Create a template for tracking decisions**

Every decision you make gets logged:
```
DATE: [date]
DECISION: [what you decided]
PRINCIPLE USED: [which principle?]
CRITERIA CHECK: [did you meet criteria? how many/how many?]
OUTCOME: [what did you choose? why?]
TRACKED FOR: [when will you review this?]
RESULT: [did it work? check back in 3 months]
LEARNING: [what did you learn?]
```

**Deliverable:** Decision tracking template in Obsidian
**Time:** 2 hours
**Storage:** Obsidian vault

---

### Week 2: Build Your Dashboard (Data Layer)

**TASK: Extract Your Key Metrics**

Pull from your actual business:
- Monthly revenue: Â£[real]
- Monthly profit: Â£[real]
- Profit margin: [real]%
- Number of clients: [real]
- Conversion rate: [real]%
- Team hours per week: [real]
- Response time average: [real]
- Team satisfaction (ask them): [real]

**Deliverable:** CSV with your current metrics
**Time:** 4 hours (collecting + analyzing)
**Storage:** Qdrant (prepare for cloud) + local backup

**Why this matters:**
This is your PROOF. Real numbers. Real metrics.
Your website will show this live.
Every month, you'll update it.

---

### Week 2-3: Deploy Your AI Assistant

**TASK: Set up personal AI orchestration**

Goal: You have 1 "Ewan's Assistant" that:
1. Knows your principles
2. Tracks your decisions
3. Alerts you to principle violations
4. Suggests updates to principles based on outcomes

**Setup:**
1. Create Qdrant instance (local or cloud small instance)
2. Load your principles into vector DB
3. Build simple LangGraph flow:
   - Ewan asks: "Should I take Client X?"
   - System retrieves Client Acceptance Principle
   - System evaluates Client X against criteria
   - System returns: "Check criteria... 5/5 met"

**Deliverable:** Working AI assistant (basic version)
**Time:** 8-10 hours
**Tools:** LangGraph, Qdrant, Claude API via OpenRouter

---

### Week 3-4: Land Your First Tier 1 Client

**TASK: Find 1 real client to do Tier 1 with**

Your first client is your proof of concept.
This is NOT a test. This is REAL.

**Who to reach out to:**
- Dental practice in Newcastle (you know this industry)
- Service SMB owner you know personally
- Someone who trusts you enough to be transparent

**The pitch:**
"I'm building a principles-based business transformation system.
You're perfect for testing it.
Here's what I'll do:

Week 1-4: Tier 1 Extraction (Â£2,500)
- Pull your financial data
- Show you profit by client
- Document your principles
- Build your dashboard

I want to prove this works before scaling.
Will you be my first real case study?
Permission to publish results (anonymized for now)?

[Book a call to discuss]"

**Deliverable:** 1 signed Tier 1 engagement
**Time:** 5-10 hours (outreach, calls, closing)

**Why this matters:**
You need REAL data, not theory.
You need PROOF that the system works.
First case study = everything else gets easier.

---

## PHASE 2: SYSTEMS (WEEKS 5-8)
### Goal: Build Coaching Infrastructure + Prove Methodology

### Week 5-6: Build Your First 3 Coaching Personas

**TASK: Implement Business Coach, Sales Coach, HR Coach**

Each coach:
1. References your principles + client's principles
2. Has specific framework (Kennedy, Ziglar, Scott)
3. Returns actionable guidance
4. Tracks outcomes

**BUSINESS COACH (Dan Kennedy Framework)**
- Input: Client situation
- Process: Check profit principle, time allocation, principles
- Output: Specific recommendation with principle reference
- Example: "You're at 38 hours delivery. Adding Client X makes 42. Violates your allocation."

[Build in LangGraph]

**SALES COACH (SPIN Framework)**
- Input: Sales situation
- Process: Situation â†’ Problem â†’ Implication â†’ Need-Payoff
- Output: Structured sales guidance
- Example: "Prospect pushing for discount. Your conversion is 68%. Don't discount."

[Build in LangGraph]

**HR COACH (Radical Candor - Kim Scott)**
- Input: Team situation
- Process: Check team principles, suggest radical truth conversation
- Output: Script for difficult conversation + follow-up plan
- Example: "Sarah missed deadline. Care personally + challenge directly."

[Build in LangGraph]

**Deliverable:** 3 working coaches in cloud (LangGraph)
**Time:** 30-40 hours (design + build + test)

---

### Week 6: Document Your Methodology

**TASK: Write "How We Make Decisions" (Blog Post)**

This becomes your first blog post.

Structure:
1. The problem (most businesses wing it)
2. Our solution (principles-based)
3. The framework (Dalio: Radical Truth + Transparency + Believability)
4. How we apply it (your 5 principles)
5. The result (systematic improvement)

**Deliverable:** 1,500-2,000 word blog post
**Time:** 5 hours
**Publish:** Week 8 (when website ready)

---

### Week 7: Complete Your First Tier 1

**TASK: Deliver extraction + principles to Client 1**

Deliverable to them:
1. 30-page analysis (profit by client, team metrics, opportunities)
2. Dashboard (live, showing their data)
3. 1-hour call (here's what we found)
4. Their first 5-8 principles (documented)

**Deliverable:** Complete Tier 1 engagement
**Time:** Full week (concentrated effort)

**Why this matters:**
This is your PROOF.
This is your TESTIMONIAL.
This is your FIRST CASE STUDY.

Get permission to publish (anonymized).

---

### Week 8: Close Tier 2 (Or Tier 3)

**TASK: Offer next level of service**

After Tier 1, offer:
- Tier 2: "Let me implement these principles with you over 12 weeks" (Â£7,500)
- Tier 3: "Let me support you ongoing" (Â£1,200/month)

**Ideal:** They choose Tier 3 (recurring revenue)
**Fallback:** They choose Tier 2 (proof of transformation)

**Deliverable:** Signed engagement (Tier 2 or Tier 3)
**Time:** 3-4 hours

---

## PHASE 3: WEBSITE (WEEKS 9-12)
### Goal: Build Website (The Bones + Meat)

### Week 9: Build Homepage + Services

**TASK: Build website skeleton**

Using your website architecture document:

**Homepage:**
- Hero section (your positioning statement)
- Your principles (published, tracked)
- Live dashboard (your metrics)
- How it works (3-minute explainer)
- CTA sections

**Services Page:**
- Tier 1: Extraction (Â£2,500)
- Tier 2: Transformation (Â£7,500)
- Tier 3: Ongoing (Â£1,200/month)
- AI Coaching add-on (+Â£300-500/month)

**Deliverable:** Homepage + Services page (functional)
**Time:** 20-30 hours (design + copy + build)
**Platform:** Next.js / Webflow / [your choice]

---

### Week 10: Blog + Your Principles

**TASK: Set up blog infrastructure**

Publish:
1. "How We Make Decisions" (your principles)
2. Your 5 principles (individually documented)
3. Your monthly transparency report (January)

**Deliverable:** Blog live with 3+ posts
**Time:** 15-20 hours

---

### Week 11: First Case Study

**TASK: Write + publish your first case study**

Using Client 1 (from Week 7):

Format:
- Situation (their pain)
- Transformation (what you built)
- Principles (their 5-8 principles)
- Results (before/after metrics)
- Quote (from client)

**Deliverable:** 1 published case study
**Time:** 10-15 hours
**Permission:** Get written approval from client

---

### Week 12: About + Demo Pages

**TASK: Finish website**

About page:
- Your philosophy
- Your journey
- Your tech stack
- Your team

Demo page:
- How coaches reference principles
- Data privacy
- ROI calculator

**Deliverable:** Complete website
**Time:** 20-30 hours

---

## PHASE 4: PROOF (MONTH 4+)
### Goal: Build Authority + Land More Clients

### Month 4: Monthly Rhythm

**Week 1: Transparency Report**
- Publish monthly report (what worked, what didn't)
- Update live dashboard
- Blog post: "Learnings from [month]"

**Week 2: Case Study**
- Publish 1 new case study (from completed engagement)
- Get permission + testimonial
- Feature on website + LinkedIn

**Week 3: Content**
- Blog post on principles (updated one)
- Blog post on methodology
- LinkedIn post (3-5x per week)

**Week 4: Sales**
- Tier 1 outreach (15-20 prospects)
- Calls booked (target: 10+ qualified)
- Tier 1 clients closed (target: 3-4)

### Result by End of Month 4:
- 5-6 Tier 1 clients completed
- 2-3 converting to Tier 3
- 3+ case studies published
- 8+ blog posts
- Authority established (local level)

---

## YEAR 1 TARGETS (What Success Looks Like)

### REVENUE
- Month 1-3: Â£2-5K (Tier 1s landing)
- Month 4-6: Â£8-12K (Tier 1s + Tier 3 recurring starting)
- Month 7-9: Â£15-20K (3-4 Tier 3, multiple Tier 1s)
- Month 10-12: Â£25-30K (5-6 Tier 3 recurring, Tier 2 starting)
- **Total Year 1 revenue: ~Â£70-100K**

### PROFIT
- After costs (cloud, tools, contractors): ~Â£45-70K
- **Target: Â£101K (from today's model)**
- If you hit targets: Â£99-120K

### CASE STUDIES
- Published: 8-10 named, verified, detailed
- Anonymized: 5-10 additional (for pattern evidence)
- Total proof: 13-20 case studies showing methodology works

### AUTHORITY
- LinkedIn: 2,000+ followers
- Website: 1,000+ visitors/month
- Blog: 20+ posts (showing your thinking)
- Inbound leads: 30-40% of pipeline from website
- Cold outreach conversion: 5-10% (Tier 1 calls â†’ clients)

### PRINCIPLES
- Personal: 5 documented (Jan) â†’ 8-10 by Dec (added based on experience)
- Per client: 5-8 principles per Tier 3 client
- Total principles across business: 100+ (5 personal + 8 clients Ã— 12)

### TEAM
- Still solo (or 1 part-time contractor if needed)
- AI coaches handling support
- You focused on: Sales, Strategy, Client Relationships

### FOUNDATION FOR YEAR 2
- 5+ Tier 3 clients (recurring: Â£6-7K/month)
- 3-4 Tier 2 engagements running
- Ready to launch AI coaching add-on
- Ready to recruit white-label partners

---

## CRITICAL SUCCESS FACTORS

### 1. PUBLISH YOUR PRINCIPLES
Don't keep them private.
Show the world how you think.
This IS your authority.

### 2. TRACK EVERYTHING
Every decision â†’ outcome â†’ learning
This data = your competitive advantage

### 3. REAL CLIENTS, REAL PROOF
First case study is everything.
Get Client 1 right.
Then build from there.

### 4. TRANSPARENCY
Monthly reports â†’ published
Your metrics â†’ live dashboard
Your learnings â†’ blog posts
You practice what you preach

### 5. STAY FOCUSED
Year 1: Land Tier 1 + convert to Tier 3
Don't get distracted by white-label or AI coaching add-on
Perfect the core first

### 6. REPEAT WHAT WORKS
One case study â†’ system for case studies
One principle â†’ systematic principle building
One client â†’ repeatable methodology

---

## MONTH-BY-MONTH EXECUTION CHECKLIST

```
MONTH 1 (Weeks 1-4): FOUNDATION
âœ“ Week 1: Document 5 principles
âœ“ Week 1: Set up decision tracking
âœ“ Week 2-3: Build personal AI assistant
âœ“ Week 2-3: Deploy on cloud (LangGraph + Qdrant)
âœ“ Week 3-4: Land Client 1 (Tier 1)

MONTH 2 (Weeks 5-8): SYSTEMS
âœ“ Week 5-6: Build 3 coaching personas
âœ“ Week 6: Write methodology blog post
âœ“ Week 7: Complete Tier 1 with Client 1
âœ“ Week 8: Close Tier 3 (ongoing engagement)

MONTH 3 (Weeks 9-12): WEBSITE
âœ“ Week 9: Build homepage + services pages
âœ“ Week 10: Blog infrastructure + 3 posts published
âœ“ Week 11: First case study published
âœ“ Week 12: About + demo pages live

MONTH 4+: PROOF + SCALE
âœ“ Week 1: Monthly transparency report (blog)
âœ“ Week 2: 1 new case study published
âœ“ Week 3: Content creation (principles, methodology)
âœ“ Week 4: Sales outreach (Tier 1 pipeline building)
âœ“ Repeat monthly

BY END OF MONTH 4:
âœ“ 3-4 Tier 1 clients completed
âœ“ 2-3 Tier 3 clients ongoing
âœ“ 3+ case studies published
âœ“ 8+ blog posts
âœ“ Authority building (local)

BY END OF MONTH 6:
âœ“ 5-6 Tier 3 clients (Â£6-7K/month recurring)
âœ“ 1-2 Tier 2 engagements
âœ“ 5+ case studies published
âœ“ Ready for Year 2 expansion

BY END OF MONTH 12:
âœ“ 5-6 Tier 3 clients (Â£6-7K/month recurring)
âœ“ 2-3 Tier 2 engagements
âœ“ 20+ Tier 1 clients delivered
âœ“ 8-10 case studies published
âœ“ Authority established (Newcastle + North)
âœ“ Foundation for white-label + AI coaching add-on
```

---

## WHAT TO DO RIGHT NOW (Today)

**TASK 1: Document Your 5 Principles (Do Today)**
Use the template from this plan.
Write down exactly how you make major decisions.
Store in Obsidian.

**TASK 2: Identify Client 1 (Do This Week)**
Who can you approach about Tier 1?
Someone who trusts you.
Someone in Newcastle / North England.
Someone with 2-10 staff, Â£500K-3M revenue.

Call them. Pitch Tier 1. Explain you're building proof of concept.
Target: 1 signed engagement by end of Week 4.

**TASK 3: Set Up Your Dashboard (Do This Week)**
Pull your actual business metrics right now.
Revenue, profit, conversion rate, team hours, response time.
Save as CSV.
This is your starting point.

**TASK 4: Decide on Website Platform (Do This Week)**
Next.js? Webflow? WordPress?
What's fastest to get working?
Don't over-engineer this.
Get homepage + services + principles live by Week 12.

**TASK 5: Email Me Your First Principle (Do This Week)**
Write your Client Acceptance Principle.
Send it to [me].
Let's validate it before you publish.

---

## THE FINAL VISION

**End of This Month:**
- Principles documented
- Client 1 signed
- Dashboard live
- Personal AI assistant working

**End of Month 3:**
- Website live
- Case study published
- Authority starting
- Tier 3 client signed

**End of Year 1:**
- Â£101K+ profit
- 20+ Tier 1 clients completed
- 5-6 Tier 3 clients recurring
- 8-10 case studies published
- Authority established
- Ready for Â£1M Year 2

**End of Year 2:**
- Â£431K+ profit
- White-label platform deployed
- AI coaching add-on live
- 30+ case studies published
- Global authority (not just Newcastle)
- Approaching Â£1M

**End of Year 3:**
- Â£1M+ profit
- Acquired by larger firm OR
- Building Â£10M+ SaaS company OR
- Running ultra-profitable services business

---

## ONE FINAL THING

You've got everything now.
- Strategy: âœ“
- Methodology: âœ“
- Technology: âœ“
- Website plan: âœ“
- Execution roadmap: âœ“

What matters now is EXECUTION.

Not perfect execution. Just execution.

Start today:
1. Document your first principle (1 hour)
2. Find your first client (call someone today)
3. Pull your dashboard metrics (2 hours)

That's it. That's week 1.

Build from there.

The system will improve as you use it.
The principles will evolve as you test them.
The website will get better each month.

But you have to START.

Start today. ðŸš€

---

## Contact / Questions

As you go through this plan:
- Questions about strategy? â†’ Back to Phase docs
- Questions about tactics? â†’ Back to content architecture
- Questions about principles? â†’ Back to Dalio integration doc
- Questions about website? â†’ Back to website architecture

Everything you need is already documented.

Now go execute.

The world doesn't need another generic consulting agency.
It needs a principles-based transformation platform.
You're building exactly that.

Let's go. ðŸ’ª

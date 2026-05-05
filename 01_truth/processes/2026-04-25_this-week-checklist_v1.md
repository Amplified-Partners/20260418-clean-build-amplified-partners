---
title: "THIS WEEK EXECUTION CHECKLIST"
id: "this-week-checklist"
version: 1
created: "2026-04-25"
type: "document"
topic_type: "checklist"
audience: "internal"
layer: "truth"
status: "filed"
signed_by: "Devon, 2026-04-25, devin-992682c244cf444f91e0a516498afbfd"
---

# THIS WEEK EXECUTION CHECKLIST
## January 13-19, 2026: Get Live

---

## YOUR NORTH STAR

**End of Week 1 (January 19):**
- âœ“ Your 5 principles documented (Obsidian)
- âœ“ Website live (rough, real, principles published)
- âœ“ Dashboard live (your real metrics)
- âœ“ AI assistant prototype working (local)
- âœ“ First 3 blog posts published (decisions, principles, intro)
- âœ“ First decision log entries tracked

**Status:** System live. Ready to close Client 1 next week.

---

## MONDAY JANUARY 13 (Today)

### Morning (1-2 hours):
- [ ] Write your Client Acceptance Principle (copy template from Revised Plan)
  - What criteria must prospects meet?
  - 5-6 specific, measurable criteria
  - Why each criterion exists
  - Save to Obsidian as "Principles/ClientAcceptance.md"

- [ ] Email me your draft (ewan@[domain])
  - Subject: "Client Acceptance Principle - Draft"
  - Let's validate before you publish

### Afternoon (2 hours):
- [ ] Write your Time Allocation Principle
  - How do you spend your week? (%)
  - Sales / Delivery / Strategic / Admin
  - Save to Obsidian

- [ ] Write your Pricing Principle
  - When do you raise prices?
  - When do you lower?
  - What's your current thinking?
  - Save to Obsidian

### Evening (1 hour):
- [ ] Extract your business metrics RIGHT NOW
  - Monthly revenue: Â£[?]
  - Monthly profit: Â£[?]
  - Profit margin: [?]%
  - Clients/customers: [?]
  - Conversion rate: [?]%
  - Team hours/week: [?]
  - Response time average: [?]
  - Save as CSV named "YourBusiness_Jan13.csv"

**END OF DAY MONDAY:**
- 3 principles drafted
- Business metrics extracted
- Email sent to me for feedback

---

## TUESDAY JANUARY 14

### Morning (2 hours):
- [ ] Revise principles based on my feedback
- [ ] Finish remaining 2 principles:
  - Hiring Principle
  - Firing/Clients Principle
- [ ] All 5 principles saved to Obsidian with consistent format

### Afternoon (3 hours):
- [ ] Set up Qdrant instance
  - Option A: Local (on your Mac) â†’ `docker run -p 6333:6333 qdrant/qdrant`
  - Option B: Cloud (free tier) â†’ qdrant.io/cloud
  - Create collection "principles"
  - Test it runs

- [ ] Convert principles to vector format
  - Principle name
  - Criteria (as text)
  - Description
  - Save as JSON

### Evening (1-2 hours):
- [ ] Decide on website platform
  - Quick decision: Webflow or Next.js + template?
  - Set it up (basic, nothing fancy)
  - Get login credentials saved

**END OF DAY TUESDAY:**
- 5 principles complete + published to Obsidian
- Qdrant running
- Website platform decided and set up

---

## WEDNESDAY JANUARY 15

### Morning (4 hours):
- [ ] Build basic LangGraph assistant
  - Copy template: [I'll send this]
  - Load your 5 principles from Qdrant
  - Build simple flow:
    1. You input: "Should I take Client X?" + client info
    2. System retrieves Client Acceptance Principle
    3. System evaluates criteria
    4. System outputs: "X/5 criteria met. [RECOMMEND/DON'T RECOMMEND]"
  - Test 3x with real prospects

### Afternoon (2 hours):
- [ ] Create decision tracking template (Obsidian)
  - File: "DecisionLog/Template.md"
  - Copy format from Revised Plan
  - Fill in first entry: "Today's principle writing"

### Evening (2 hours):
- [ ] Start website content structure
  - Create folder: "website_content"
  - Create files:
    - homepage.md (hero section)
    - principles.md (your 5 principles published)
    - dashboard.md (screenshot spot)
    - about.md (your story)
  - Just structure. No perfect copy yet.

**END OF DAY WEDNESDAY:**
- LangGraph assistant running (local test)
- Decision log template created
- Website content structure ready

---

## THURSDAY JANUARY 16

### Morning (2 hours):
- [ ] Set up your website homepage
  - Add hero section:
    - Headline: "Stop Making Decisions on Feelings. Start on Principles."
    - Subheading: [Your positioning from earlier docs]
  - Add CTA: "See How It Works" + "Book a Call"
  - Add your principles list (brief version)

- [ ] Create live dashboard mockup
  - Screenshot or Retool dashboard with YOUR metrics
  - Your Jan 13 CSV data
  - Simple: Revenue, Profit, Conversion, Response Time, Client Count
  - Add to website homepage

### Afternoon (3 hours):
- [ ] Write first 3 blog posts
  - Post 1: "Here's My 5 Principles (And How I Test Them)" 
    - Publish your Client Acceptance Principle fully
    - Explain why it matters
    - Show 1 example of it working
    - 500 words
  
  - Post 2: "Decision Log: Week 1"
    - Screenshot your decision tracking
    - What decisions came up?
    - Which principle helped?
    - What surprised you?
    - 300 words
  
  - Post 3: "Welcome to Principles-Based Business"
    - Your philosophy
    - What you're building
    - Why it matters
    - 400 words

### Evening (1 hour):
- [ ] Publish all 3 blog posts to website
- [ ] Test links work
- [ ] Share first blog post on LinkedIn (personal profile)

**END OF DAY THURSDAY:**
- Website live (rough but real)
- Dashboard live (your metrics)
- First 3 blog posts published
- LinkedIn post going out

---

## FRIDAY JANUARY 17

### Morning (2 hours):
- [ ] Test your LangGraph assistant with real scenarios
  - Scenario 1: Should you take a prospect that meets 4/5 criteria?
  - Scenario 2: Should you take one that meets 5/5 but violates Time Allocation?
  - Scenario 3: Should you discount your pricing?
  - Test it 5x, make notes

### Afternoon (2 hours):
- [ ] Create a "Decision Tracking" blog post
  - Screenshot your decision log from this week
  - "This Week I Tested 5 Decisions Through My Principles"
  - Show the framework working
  - 300-400 words
  - Publish

- [ ] Update your principles based on testing
  - Did anything surprise you?
  - Any edge cases?
  - Update them in Obsidian
  - Update on website if you found clarity

### Evening (1 hour):
- [ ] LinkedIn content
  - Post 3-5 quick updates from the week:
    - "Day 1: Wrote my first principle..."
    - "Day 3: Got my AI assistant running..."
    - "Day 5: Tested my framework 5x..."
  - Use images (screenshots of principles, dashboard)

**END OF DAY FRIDAY:**
- 4 blog posts published
- Assistant tested 5x
- LinkedIn updates going out
- Principles refined
- Ready for Monday client calls

---

## SATURDAY JANUARY 18

### Morning (1 hour):
- [ ] Prepare for Monday calls
- [ ] List 10 ideal prospects for Tier 1:
  - Service SMBs (dentist, vet, salon, trade)
  - 2-10 staff
  - Â£500K-3M revenue
  - Newcastle/North area
  - Decision maker available

### Afternoon (2 hours):
- [ ] Draft your Tier 1 pitch script
  - "I'm testing a principles-based system..."
  - "4 weeks, Â£2,500, you'll get..."
  - "Only taking 3 proof clients..."
  - "You fit the profile because..."
  - Save to file for reference

### Evening:
- Rest. You've earned it.

---

## SUNDAY JANUARY 19

### Morning (1-2 hours):
- [ ] Final checklist:
  - Website live? âœ“
  - Dashboard live? âœ“
  - Principles published? âœ“
  - 4 blog posts up? âœ“
  - AI assistant working? âœ“
  - LinkedIn posts sent? âœ“
  - Decision log started? âœ“

- [ ] Test everything works
  - Visit website
  - Check blog posts load
  - Check dashboard displays
  - Test assistant (one more time)

- [ ] Take screenshot
  - Your homepage
  - Your dashboard
  - Your first blog post
  - Save for "Launch Day" record

### Afternoon (1 hour):
- [ ] Prepare Monday:
  - Print your 10 prospect list
  - Print your pitch script
  - Set calendar: "Client calls all day Monday"
  - Target: 5 calls, 3 qualified, 1 close this week

### Evening:
- Celebrate. You're LIVE.

---

## WHAT YOU'LL HAVE BY END OF SUNDAY

**System:**
- âœ“ 5 documented principles (Obsidian + website)
- âœ“ Personal AI assistant (working, tested)
- âœ“ Decision tracking (started)
- âœ“ Dashboard (live, your real metrics)

**Website:**
- âœ“ Homepage (principles published)
- âœ“ Dashboard (live, your real metrics)
- âœ“ 4 blog posts (decisions, principles, intro, decision tracking)
- âœ“ About page (your story)
- âœ“ Contact/Call booking

**Content:**
- âœ“ 4 blog posts published
- âœ“ 5+ LinkedIn posts sent
- âœ“ Proof: System works, published, live

**Momentum:**
- âœ“ Ready to close Client 1 Monday
- âœ“ Authority starting (published principles)
- âœ“ Proof starting (decision logs published)

**Status:** LIVE + REAL + READY

---

## MONDAY JANUARY 20: THE REAL WORK STARTS

Monday you start calling.
10 calls.
5 meetings.
1-2 closes this week.

By Friday January 24:
- Client 1 signed
- Tier 1 engagement started
- Website getting daily traffic
- Blog getting daily posts (2x/week minimum)

---

## TOOLS YOU'LL NEED

- Obsidian (you have it)
- Qdrant (free, Docker)
- LangGraph (pip install)
- OpenRouter API key (for Claude access)
- Webflow or Next.js (website)
- LinkedIn (for posting)

Total cost this week: ~$0 (assuming you have Mac + basic services)

---

## IF YOU GET STUCK

**Monday 2pm stuck?** â†’ Call me. 15 min. We'll unblock.
**Tuesday stuck on LangGraph?** â†’ Use simple version (no LLM, just rule-based matching)
**Wednesday stuck on website?** â†’ Use Webflow template, not custom build
**Friday stuck on copy?** â†’ Copy from earlier docs, personalize later

Don't get perfect. Get LIVE.

---

## THE REAL GOAL THIS WEEK

Not: Perfect system
Not: Beautiful website
Not: Polished content

**Real goal:** Get your principles working on your decisions, publish what happens, close Client 1.

Everything else flows from that.

---

## REPORT BACK SUNDAY

By Sunday January 19:
- Screenshot your live website
- Share your decision log
- Share your first 4 blog posts
- Let's celebrate

Then Monday you close Client 1.

---

## ONE FINAL THING

You're overthinking this.

The system works. You know what to do.

This week:
1. Write principles (done by Tuesday)
2. Build assistant (done by Wednesday)
3. Launch website (done by Thursday)
4. Publish content (done by Friday)
5. Close Client 1 (done by Friday next week)

That's it.

Then compound from there.

You've got this.

Start today.

Go. ðŸš€

---

## QUICK REFERENCE: THIS WEEK'S DELIVERABLES

**Monday-Tuesday:**
- [ ] 5 principles documented
- [ ] Metrics extracted
- [ ] Qdrant set up

**Wednesday-Thursday:**
- [ ] LangGraph assistant running
- [ ] Website live
- [ ] First 3 blog posts published
- [ ] Dashboard live

**Friday-Sunday:**
- [ ] 1 more blog post (decision tracking)
- [ ] 5+ LinkedIn posts
- [ ] Assistant tested 5x
- [ ] Prepared for Monday calls

**End Result:** Everything live, everything real, everything ready to close Client 1 Monday.

Go ship it. ðŸ’ª

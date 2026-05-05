---
title: "Integration: Website Critique System + Kilo Code + MiniMax 2.1"
id: "tech-expert-panel-integration-v1"
version: 1
created: "2026-04-25"
type: "document"
topic_type: "unsorted"
audience: "internal"
layer: "shadow"
status: "filed"
signed_by: "Devon, 2026-04-25, devin-992682c244cf444f91e0a516498afbfd"
---

# Integration: Website Critique System + Kilo Code + MiniMax 2.1

## How to Automate the 8-Expert Panel using AI

### The Vision
Instead of manually reviewing websites with each expert lens, **MiniMax 2.1 runs all 8 experts in parallel**, each asking their specialized questions and scoring the website.

Result: **Full website critique in 5-10 minutes** (vs. 90 minutes with humans)

---

## KILO CODE SETUP

### Agent: "Website Expert Panel Reviewer"

```
ROLE: Expert panel of 8 judges reviewing a website

You are 8 different experts, each with deep expertise in:
1. Conversion optimization
2. User experience
3. Brand strategy
4. Copywriting
5. Design systems
6. Technical SEO
7. Performance engineering
8. Accessibility

Each expert will review the website independently, score it (0-10) 
on their dimension, and provide specific feedback.

WEBSITE TO REVIEW: [Website URL]
CONTEXT: [Brief context about business, target audience, goals]

PROCESS:
- Each expert conducts their review in parallel
- Each expert scores their dimension 0-10
- Each expert identifies top 3 issues
- Each expert suggests 1 quick win + 1 deep dive
- All 8 experts provide their feedback

OUTPUT:
Generate a comprehensive critique report with all 8 expert reviews.
```

---

## MINIMAX 2.1 PROMPTS

### Prompt 1: Conversion Architect

```
ROLE: Conversion Rate Optimization Expert

You are reviewing a website for conversion effectiveness.
Your goal: Identify every friction point that prevents visitors 
from taking the desired action (book audit, sign up, download, etc.)

WEBSITE URL: [URL]
PRIMARY CONVERSION GOAL: [e.g., "Book a free audit"]
TARGET AUDIENCE: [e.g., "UK SMBs, £500K-3M revenue, owner-operators"]

REVIEW PROCESS:
Ask yourself each question in order:
1. What is the primary conversion goal on this page?
2. Is the CTA visible within first 3 seconds?
3. How many steps to conversion?
4. Where do users likely drop off?
5. Is the value proposition clear before asking for action?
6. Are objections addressed?
7. How many form fields? (Rate from 0-10 on friction)
8. Does it feel trustworthy?

SCORING (0-10):
- 9-10: Excellent CRO, minimal friction
- 7-8: Good, but some improvements needed
- 5-6: Moderate issues affecting conversions
- 3-4: Significant CRO problems
- 0-2: Severely broken funnel

DELIVERABLES:
1. Score (0-10) with explanation
2. Top 3 issues (by impact on conversion)
3. One quick win (1-hour fix)
4. One deep dive (1-2 week improvement)
5. Specific metrics (CTA click rate, form completion rate)

FORMAT YOUR OUTPUT:
🎯 CONVERSION SCORE: [Score]/10

[Issue 1]: [Impact] → [Specific fix]
[Issue 2]: [Impact] → [Specific fix]
[Issue 3]: [Impact] → [Specific fix]

Quick Win: [Fix and expected impact]
Deep Dive: [Improvement and expected impact]

Current Metrics (estimated):
- CTA click rate: [X]%
- Form completion: [X]%
- Booking rate: [X]%
```

### Prompt 2: UX Researcher

```
ROLE: User Experience Researcher

You are reviewing a website for usability and user experience.
Your goal: Identify every point where users might get confused, 
frustrated, or abandon the site.

WEBSITE URL: [URL]

REVIEW PROCESS:
Navigate the website as if you're a first-time visitor.
Ask yourself each question in order:
1. Can I understand what this site is about in 5 seconds?
2. How many clicks to reach major pages? (Target: ≤3)
3. Is mobile version actually usable?
4. Do all interactive elements behave as expected?
5. Are there dead ends or missing navigation?
6. Do forms provide helpful error messages?
7. Is there sufficient whitespace?
8. Can I use this with keyboard only?

SCORING (0-10):
- 9-10: Excellent UX, smooth navigation
- 7-8: Good UX, minor issues
- 5-6: Moderate UX problems
- 3-4: Significant usability issues
- 0-2: Severely broken UX

DELIVERABLES:
1. Score (0-10)
2. Navigation flow analysis (is it intuitive?)
3. Top 3 UX issues
4. One quick win (1-hour fix)
5. One deep dive (1-2 week improvement)
6. Mobile usability assessment

FORMAT YOUR OUTPUT:
😊 UX SCORE: [Score]/10

Navigation: [Analysis of how intuitive it is]

[Issue 1]: [What confuses users] → [Fix]
[Issue 2]: [What confuses users] → [Fix]
[Issue 3]: [What confuses users] → [Fix]

Quick Win: [Fix and UX improvement]
Deep Dive: [Improvement and expected impact]

Mobile Assessment: [Specific mobile UX issues]
```

### Prompt 3-8: [Continue pattern for Brand, Copy, Design, SEO, Performance, Accessibility]

---

## KILO CODE EXECUTION FLOW

### Step 1: Create Agent Task

```json
{
  "agent_name": "Website Expert Panel Reviewer",
  "task": "Review website using 8-expert framework",
  "input": {
    "website_url": "https://example.com",
    "context": "UK SMB optimization consultancy, target: owner-operators",
    "conversion_goal": "Book free audit"
  },
  "experts": [
    "Conversion Architect",
    "UX Researcher",
    "Brand Strategist",
    "Copywriter",
    "Design Systems Expert",
    "Technical SEO Specialist",
    "Performance Engineer",
    "Accessibility Auditor"
  ],
  "execution": "parallel_all_experts",
  "timeout": "10_minutes"
}
```

### Step 2: Run MiniMax in Parallel

```
KILO CODE INSTRUCTION:
Execute all 8 experts in parallel (not sequentially)
Model: MiniMax 2.1
Temperature: 0.6 (consistent, not overly creative)
Max tokens: 2,000 per expert
Timeout: 2 minutes per expert

Use function calling to structure responses:
- Each expert returns a JSON object
- Scoring: 0-10
- Issues: Array of 3 issues
- Quick win: String
- Deep dive: String
```

### Step 3: Aggregate Results

```
AGGREGATION LOGIC:
1. Collect all 8 expert scores
2. Calculate weighted average (see scoring matrix)
3. Identify common themes (if 3+ experts mention same issue)
4. Rank issues by priority (impact × effort)
5. Generate executive summary
```

---

## OUTPUT TEMPLATE (Auto-generated Report)

```markdown
# Website Expert Panel Review Report
## [Website Name/URL]
**Review Date:** [Date]
**Reviewed By:** 8-Expert Panel (AI-powered analysis)

---

## EXECUTIVE SUMMARY

**Overall Score:** [Weighted average]/10
- [Score breakdown by expert]

**Critical Issues (Fix immediately):**
1. [Issue] - Impact: High - Effort: Low
2. [Issue] - Impact: High - Effort: Medium

**Strategic Issues (Plan for next sprint):**
1. [Issue] - Impact: Medium - Effort: Medium
2. [Issue] - Impact: Medium - Effort: High

---

## DETAILED EXPERT REVIEWS

### 1️⃣ Conversion Architect
**Score:** [Score]/10

**Analysis:**
[Full expert analysis]

**Top 3 Issues:**
1. [Issue 1] → [Fix]
2. [Issue 2] → [Fix]
3. [Issue 3] → [Fix]

**Quick Win:** [1-hour fix + expected impact]
**Deep Dive:** [Major improvement + timeline + expected impact]

---

[Repeat for Experts 2-8]

---

## PRIORITY ACTION PLAN

### DO FIRST (This week)
- [ ] [Quick win from Conversion Architect]
- [ ] [Quick win from UX Researcher]
- [ ] [Quick win from Copy expert]

### DO NEXT (Next 2 weeks)
- [ ] [Deep dive from Conversion Architect]
- [ ] [Deep dive from Designer]
- [ ] [Deep dive from SEO expert]

### PLAN LATER (Next quarter)
- [ ] [Lower priority improvement]
- [ ] [Nice-to-have optimization]

---

## METRICS DASHBOARD

Current Performance (Estimated):
- Conversion rate: [X]%
- Bounce rate: [X]%
- Avg time on page: [X] min
- Core Web Vitals: [Green/Yellow/Red]
- SEO visibility: [Low/Medium/High]

Projected Performance (After fixes):
- Conversion rate: [X]% (+Y% improvement)
- Bounce rate: [X]% (-Y% improvement)
- Avg time on page: [X] min (+Y%)
- Core Web Vitals: [Green]
- SEO visibility: [High]

---

## NEXT REVIEW DATE

Recommended: 2 weeks after implementing fixes
[Book follow-up review]

---
```

---

## WORKFLOW: CRITIQUE → BUILD → ITERATE

### Day 1: Run Expert Panel (10 min)
```
Input website URL → MiniMax analyzes with 8 experts → Report generated
Output: Full critique report with prioritized action plan
```

### Day 2-3: Review + Prioritize (30 min)
```
Client reviews report
Select top 5 fixes to implement first
Discuss trade-offs (what's quick vs. what's important)
```

### Day 4-7: Implement First Batch (16 hours)
```
- Conversion expert's quick wins (2 hours)
- UX expert's quick wins (3 hours)
- Copy expert's quick wins (2 hours)
- Designer's quick wins (3 hours)
- SEO expert's quick wins (2 hours)
- Performance optimization (2 hours)

Deploy changes live
```

### Day 8: Monitor + Measure (2 hours)
```
Set up tracking (GA4, heatmaps, session recordings)
Monitor bounce rate, CTA clicks, form submissions
Compare Week 1 vs Week 2
```

### Day 14: Second Expert Panel Review (10 min)
```
Run same 8 experts again
Compare scores: Week 1 vs Week 2
Celebrate improvements ✅
Identify remaining issues
```

---

## FOR YOUR CONSULTANCY: THE SALES PITCH

**Your service:**
```
"Website audit by 8 expert judges: conversion specialist, UX researcher, 
brand strategist, copywriter, designer, SEO expert, performance engineer, 
and accessibility auditor.

Normally, hiring these 8 experts would cost £5,000-8,000.

With our AI-powered panel, you get a full critique in 10 minutes for £1,997.

You also get a prioritized action plan that shows which fixes will have 
the biggest impact on revenue.

And if you hire us to implement the fixes, we'll run a second review 
after 2 weeks to prove we delivered improvement."
```

---

## THE COMPETITIVE MOAT

**Why this is powerful:**

1. **Speed:** 10 minutes vs. 90 minutes (9x faster than humans)
2. **Consistency:** Same criteria applied every time
3. **Specificity:** Each expert goes deep on their dimension
4. **Scalability:** Same system works for £1K websites and £100K websites
5. **Proof:** Numbered scores show improvement over time

**What makes it unique:**
- No other agency has this system
- Your clients can't get this anywhere else
- You can charge premium pricing because you have premium methodology

**How to scale:**
- Start with manual reviews (prove it works)
- Transition to AI panel (as you validate)
- Train other designers to implement recommendations
- Build a "Website Quality Certified" program

---

## IMPLEMENTATION TIMELINE

**Week 1:** Write 8 expert personas + 8 critique templates
**Week 2:** Create MiniMax prompts for each expert
**Week 3:** Test with 3 example websites (collect feedback)
**Week 4:** Launch service to clients
**Week 5+:** Document case studies, refine process

---

## GETTING STARTED THIS WEEK

**Today:**
1. Review `website-critique-rag-onboarding-system.md` (Part 1: 8 experts)
2. Pick 3 websites to test with (yours, competitor, friend)
3. Read through each expert's critique template

**Tomorrow:**
1. Draft MiniMax prompts for Expert #1 (Conversion Architect)
2. Test prompt on your website
3. Evaluate quality of output

**This Week:**
1. Draft all 8 expert prompts
2. Test on 3 websites
3. Document what works, what needs refinement

**Next Week:**
1. Launch first client audit
2. Document results
3. Iterate based on feedback

---

**You now have everything to build your competitive moat.**

**The 8-Expert Panel critique system is your secret weapon.**

**Go build it.**

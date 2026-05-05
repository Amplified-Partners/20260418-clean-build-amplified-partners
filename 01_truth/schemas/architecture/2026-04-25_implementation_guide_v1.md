---
title: "covered.AI Implementation Guide"
id: "implementation_guide"
version: 1
created: "2026-04-25"
type: "document"
topic_type: "implementation-plan"
audience: "internal"
layer: "truth"
status: "filed"
signed_by: "Devon, 2026-04-25, devin-992682c244cf444f91e0a516498afbfd"
---

# covered.AI Implementation Guide

## Quick-Start Reference

This guide provides a step-by-step execution plan for launching the covered.AI marketing system. All documentation exists in `Baselayer/covered-ai-v2/`. Use this file as your implementation checklist.

---

## Pre-Launch Checklist

### Week 0: Foundation Setup

| Task | Location | Status |
|------|----------|--------|
| [ ] Confirm logo concept selection | `brand-identity-system.md` (lines 141-153) | ☐ |
| [ ] Generate final logo files (SVG, PNG, ICO) | Designer or AI tool | ☐ |
| [ ] Set up domain and hosting | covered.ai | ☐ |
| [ ] Create email account (ewan@covered.ai) | Google Workspace | ☐ |
| [ ] Set up Calendly (free tier) | calendly.com | ☐ |
| [ ] Create HubSpot account (free tier) | hubspot.com | ☐ |

---

## Phase 1: Brand Assets (Days 1-3)

### 1.1 Logo Implementation

**Reference:** [`brand-identity-system.md`](Baselayer/covered-ai-v2/brand-identity-system.md) - Part 2 (lines 156-295)

**Deliverables needed:**
- [ ] Primary logo (full color) - 1024px wide minimum
- [ ] White version (for dark backgrounds)
- [ ] Icon-only version (favicon, social)
- [ ] Favicon (32x32px ICO)
- [ ] Business card design (85mm x 55mm)

**Design Specifications:**
```
Primary Colors:
- Navy Blue: #0A2540
- Bright Teal: #00D9C0
- Charcoal Gray: #2D3748
- Light Gray: #F7FAFC

Fonts:
- Headings: Satoshi Bold
- Body: Inter Regular
- Data: JetBrains Mono
```

**Design Tools (no coding required):**
- Canva (canva.com) - Recommended for non-designers
- Figma (figma.com) - If you want more control
- Look for "logo maker" templates matching these colors

### 1.2 Email Signature

**Reference:** [`brand-identity-system.md`](Baselayer/covered-ai-v2/brand-identity-system.md) - Part 7 (lines 736-758)

**Copy this template to Gmail/Outlook:**

```
Ewan Bramley
Founder, covered.AI

ewan@covered.ai
covered.ai
Byker, Newcastle upon Tyne, UK

"We tighten your processes. You keep running your business."
```

**Instructions:**
1. Gmail → Settings → See all settings → Signature
2. Paste the above with logo image link
3. Set as default for new emails

---

## Phase 2: Website Setup (Days 4-10)

### 2.1 Build Homepage

**Reference:** [`MARKETING_SYSTEM.md`](Baselayer/covered-ai-v2/MARKETING_SYSTEM.md) - Phase 2 (lines 386-567)

**Required Pages:**
1. Homepage (/)
2. How It Works (/how-it-works)
3. Case Studies (/case-studies)
4. About Ewan (/about-ewan)
5. Free Audit Landing Page (/free-audit)

**Platform Options (no coding required):**

| Platform | Cost | Difficulty | Best For |
|----------|------|------------|----------|
| Carrd | £19/year | Easy | Simple landing pages |
| Webflow | Free/$19/mo | Medium | Custom design |
| Framer | Free/$12/mo | Medium | Design-forward |
| WordPress | Free/$5/mo | Hard | Full CMS |

**Recommendation:** Carrd for first launch (simple, fast, covers all needs)

### 2.2 Homepage Copy

**Hero Section:**
```
Headline: We automate the busywork. You keep running your business.

Subheadline: covered.AI works in the background to tighten your processes—
automating invoices, chasing late payments, and capturing more leads.
No disruption to how you work. No retraining your team. Just results.

CTA Button: Get Free Process Audit
Secondary: See How This Works

Social Proof: Helping 150+ UK SMBs collect £8K+ more per month
```

**Problem Section:**
```
Headline: Most Consultants Want to "Transform" Your Business.
You Just Need It to Work Better.

You're not broken. Your business is working—you're just spending too much
time on things that don't make money. The late payments. The admin.
The lead follow-ups that fall through the cracks.

Three Pain Points:
1. 60+ hours/week doing everything yourself
2. £8K-15K stuck in late payments every month
3. Marketing feels like throwing money at a wall
```

**How It Works Section:**
```
Headline: Four Steps. Six Weeks. Zero Disruption.

Step 1: We Audit What You're Already Doing (Week 1)
Step 2: We Automate the Busywork (Weeks 2-4)
Step 3: We Run in the Background (Weeks 5-8)
Step 4: You Get Results (Week 9+)

Closing: Typical setup: 4-6 weeks. Disruption: Zero.
```

---

## Phase 3: LinkedIn Setup (Days 11-14)

### 3.1 Personal Profile Optimization

**Reference:** [`linkedin-strategy.md`](Baselayer/covered-ai-v2/linkedin-strategy.md) - Section 1 (lines 9-208)

**Headline (89 characters):**
```
Founder, covered.AI | Helping UK SMBs Get Their Time Back (Without Disruption)
```

**About Section Copy (copy and paste):**

```
I spent 30 years running a dental practice in Byker, Newcastle.

Started with just me. Ended with 30 staff and millions in revenue.
Made every mistake along the way—late payments, admin overwhelm,
working 60+ hours, wondering where the time went.

Here's what I learned: You don't need transformation. You need optimization.

Most consultants want to "transform" your business. Replace your systems.
Retrain your staff. Disrupt your operations.

I don't do that.

I tighten what's already working. Automate the busywork. Chase late
payments. Document your processes. Run in the background.

What I do now:

Help UK SMBs (£500K-£3M revenue, 3-15 staff) get:
- 10-20 hours/week back
- £8K-15K more collected monthly
- 30% more leads captured
- Zero disruption to how they work

Typical client:
- Owner working 50+ hours/week
- Frustrated with late payments or inconsistent leads
- Wants results without changing everything
- Running a service business (dental, salon, vet, trades, consulting)

My promise: Honest assessment. No hype. If you're not a fit, I'll tell you.

If you're working too many hours and wondering where the money goes,
let's talk.

Book a free process audit:
[Calendly Link]

---
Ewan Bramley
Founder, covered.AI
Byker, Newcastle, UK
```

### 3.2 Company Page Setup

**Reference:** [`linkedin-strategy.md`](Baselayer/covered-ai-v2/linkedin-strategy.md) - Section 2 (lines 210-336)

**Company Page Details:**
```
Name: covered.AI
Tagline: Low-friction optimization for UK SMBs
URL: linkedin.com/company/covered-ai
Industry: Business Consulting
Company Size: 1-10 employees
Founded: 2025

Specialties:
- Process Automation
- Cash Flow Optimization
- Late Payment Recovery
- Lead Generation
- Business Documentation
- SMB Consulting

About Section: Copy from personal profile, adapt to company voice
CTA Button: Book Free Process Audit → https://covered.ai/free-audit
```

### 3.3 Banner Images

**Personal Profile Banner:** 1584 x 396px
**Company Page Banner:** 1128 x 150px

**Design brief for designer or Canva:**
```
Background: Navy Blue (#0A2540)
Text: White
Logo: covered.AI logo (white version)
Tagline: "Low-Friction Optimization for UK SMBs"
Values: "10-20 hours saved | £8K-15K more collected"
```

---

## Phase 4: Email System (Days 15-21)

### 4.1 HubSpot Setup

**Reference:** [`email-sequences.md`](Baselayer/covered-ai-v2/email-sequences.md) - Section "HubSpot Workflow Setup" (lines 1119-1160)

**Required Integrations:**
1. Connect HubSpot to Calendly
2. Set up email deliverability (SPF, DKIM)
3. Create contact property: `pain_point`, `industry`, `revenue`

### 4.2 Email Sequence Setup

**Create these 7 emails in HubSpot:**

| Day | Email Name | Purpose |
|-----|------------|---------|
| 0 | Welcome | Introduce Ewan, set expectations |
| 3 | Problem ID | Highlight late payment issue |
| 5 | Case Study | Show specific results (Mark dental) |
| 7 | Lead Magnet | Offer free audit |
| 10 | Objection Handling | Address concerns |
| 14 | Scarcity | "2 spots left" (if no booking) |
| 21 | Final Follow-up | Last touch (if no booking) |

**Copy for each email:** See [`email-sequences.md`](Baselayer/covered-ai-v2/email-sequences.md)

### 4.3 Automation Rules

**Sequence 1: New Subscriber**
```
Trigger: Form submission
→ Send Welcome Email
→ Wait 3 days
→ Send Problem ID Email
→ Wait 2 days
→ Send Case Study Email
→ Wait 2 days
→ Send Lead Magnet Email
→ Wait 3 days
→ Send Objection Handling Email
```

**Conditional Logic:**
- Clicked Calendly → Move to "Post-Click Sequence"
- Replied "LATE" → Send invoice automation guide
- Replied "INVOICE" → Send setup guide
- Didn't open → Resend with new subject line

---

## Phase 5: Content Calendar (Ongoing)

### 5.1 LinkedIn Posting Schedule

**Reference:** [`linkedin-strategy.md`](Baselayer/covered-ai-v2/linkedin-strategy.md) - Section 3 (lines 338-652)

**Posting Cadence:** 3 posts per week
- Monday: Case Study or Problem/Solution
- Wednesday: Case Study or Myth-Busting
- Friday: Quick Tip or Behind-the-Scenes

**Week 1-2 Posts:**

| Week | Monday | Wednesday | Friday |
|------|--------|-----------|--------|
| 1 | Case Study: Sarah Salon | Problem/Solution: Transform vs Tighten | Quick Tip: Invoice Timing |
| 2 | Case Study: Mark Dental | Myth-Busting: New Software | Quick Tip: Lead Follow-Up |

**All 30 post templates:** See [`linkedin-strategy.md`](Baselayer/covered-ai-v2/linkedin-strategy.md) (lines 606-652)

### 5.2 Blog Publishing Schedule

**Reference:** [`MARKETING_SYSTEM.md`](Baselayer/covered-ai-v2/MARKETING_SYSTEM.md) - Phase 5 (lines 1888-2013)

**Post 1-8 Outlines:**
1. "How to Stop Losing Leads"
2. "How to Collect £8K More Per Month"
3. "Why Your Marketing Feels Like Guesswork"
4. "Stop Chasing Invoices"
5. "The £15K Leak"
6. "Cash Flow Problems Are Visibility Problems"
7. "How to Get 10 Hours Back"
8. "The Admin Automation Checklist"

**AI Prompt for MiniMax 2.1:** See [`MARKETING_SYSTEM.md`](Baselayer/covered-ai-v2/MARKETING_SYSTEM.md) (lines 1940-1969)

**Publishing Schedule:**
- Tuesday 10 AM GMT: Blog post
- Thursday 3 PM GMT: Blog post
- Repurpose to LinkedIn, email, social

---

## Phase 6: Sales Process (Ongoing)

### 6.1 Discovery Call Script

**Reference:** [`MARKETING_SYSTEM.md`](Baselayer/covered-ai-v2/MARKETING_SYSTEM.md) - Phase 6 (lines 2017-2073)

**30-Minute Call Structure:**

| Time | Section | Script |
|------|---------|--------|
| 0:00-0:02 | Intro | "Hi [Name], I'm Ewan from covered.AI. Spent 30 years running dental practices in Newcastle. Goal: show you where you're losing money. No pitch, no pressure. Sound good?" |
| 0:02-0:04 | Rapport | "Tell me about your business. How long have you been running it? What does a typical week look like?" |
| 0:04-0:14 | Pain Discovery | Ask key questions (see below) |
| 0:14-0:22 | Situation Audit | "Walk me through how you handle [invoices/leads/admin]" |
| 0:22-0:28 | Present Solution | Share relevant case study |
| 0:28-0:30 | Next Steps | "I can put together a proposal. Want me to do that?" |

**Key Questions:**
1. "What's the biggest challenge you're facing right now?"
2. "How many hours per week on admin vs. revenue work?"
3. "Where are you losing money—late payments, leads going cold, admin?"
4. "If you could get 20 hours back per week, what would you do with it?"
5. "Have you tried fixing this before? What happened?"

### 6.2 Proposal Template

**Reference:** [`MARKETING_SYSTEM.md`](Baselayer/covered-ai-v2/MARKETING_SYSTEM.md) - Phase 6 (lines 2075-2143)

**Three Tiers:**

| Tier | Price | Timeline | Processes | Expected Results |
|------|-------|----------|-----------|------------------|
| Basic | £2,997 | 4 weeks | 1 core process | £8K+ collected, 5-10 hours saved |
| Standard | £3,997 | 6 weeks | 2-3 core processes | £12K+ collected, 10-20 hours saved |
| Premium | £4,997 | 8 weeks | 3-5 core processes | £15K+ collected, 20+ hours saved |

**Recommendation:** Default to Standard (£3,997)

### 6.3 Objection Handling

**Reference:** [`MARKETING_SYSTEM.md`](Baselayer/covered-ai-v2/MARKETING_SYSTEM.md) - Phase 6 (lines 2145-2164)

| Objection | Response |
|-----------|----------|
| "Sounds too good to be true" | "We work in background 4-6 weeks. You don't change anything. Results show up in numbers." |
| "No budget right now" | "If we find £8K/month in leaks, that's £96K/year. Our engagement is £3-5K. Investment, not expense." |
| "Worried about disruption" | "We don't retrain your team. We don't force new software. We just automate the busywork." |
| "Need to think about it" | "Sleep on it. But think about: hours last week on things that don't make money? Money in unpaid invoices?" |
| "What if it doesn't work?" | "6 weeks of work. No measurable results = no pay second 50%. Risk is ours, not yours." |

---

## Daily/Weekly Execution Schedule

### Weekly Time Investment: 7-8 Hours

| Day | Activity | Time |
|-----|----------|------|
| Monday | LinkedIn Post #1 + Analytics Review | 1.5 hours |
| Tuesday | Blog Post + Email Send | 1.5 hours |
| Wednesday | LinkedIn Post #2 + Engagement | 1 hour |
| Thursday | Discovery Calls | 1-2 hours |
| Friday | LinkedIn Post #3 + Next Week Planning | 1 hour |
| Sunday | Content Batching | 1 hour |

### Daily Tasks (30 minutes):

**Morning (15 min):**
- Process emails
- Send 10 LinkedIn DMs

**Mid-Day (10 min):**
- Engage on LinkedIn (comment on 5 posts)
- Respond to comments on own posts

**Evening (5 min):**
- Review metrics
- Plan next day

---

## Revenue Projections

### Conservative Estimate (7-8 hrs/week)

| Month | Audits Booked | Clients | Revenue |
|-------|---------------|---------|---------|
| 1 | 0 | 0 | £0 |
| 2 | 10 | 1 | £3-5K |
| 3 | 20 | 2-3 | £6-10K |
| 4 | 30 | 3-4 | £9-15K |
| 5 | 40 | 4-5 | £12-20K |
| 6 | 50 | 5-7 | £15-25K |
| 12 | 100 | 15-20 | £45-75K |

**Year 1 Target:** £45-75K revenue
**Average Client Value:** £3-5K

---

## Tracking & Analytics

### Key Metrics to Monitor Weekly

| Metric | Target | Tool |
|--------|--------|------|
| Website visitors | 500+/month | Google Analytics |
| Email subscribers | 50+/month | HubSpot |
| LinkedIn impressions | 2,000+/month | LinkedIn Analytics |
| Discovery calls booked | 5-10/month | Calendly |
| Audit completion rate | 90%+ | Manual tracking |
| Audit → Client conversion | 30% | Manual tracking |

### Monthly Review Checklist

- [ ] Review website analytics
- [ ] Check email open/click rates
- [ ] Analyze LinkedIn post performance
- [ ] Review discovery call outcomes
- [ ] Update case studies with new results
- [ ] Adjust content calendar based on engagement

---

## Quick Reference: Key Files

| File | Purpose |
|------|---------|
| [`MARKETING_SYSTEM.md`](Baselayer/covered-ai-v2/MARKETING_SYSTEM.md) | Complete marketing strategy (read this first) |
| [`brand-identity-system.md`](Baselayer/covered-ai-v2/brand-identity-system.md) | Logo, colors, typography, voice |
| [`email-sequences.md`](Baselayer/covered-ai-v2/email-sequences.md) | All email copy and HTML templates |
| [`linkedin-strategy.md`](Baselayer/covered-ai-v2/linkedin-strategy.md) | Profile optimization, 30 posts, outreach |

---

## Launch Checklist

### Before Going Live

- [ ] Logo files created and uploaded
- [ ] Website pages live (homepage, how-it-works, case-studies, about, free-audit)
- [ ] Email signature updated
- [ ] LinkedIn personal profile optimized
- [ ] LinkedIn company page created
- [ ] Calendly connected to website
- [ ] HubSpot connected to website forms
- [ ] Welcome email sequence active
- [ ] First 2 weeks of LinkedIn posts scheduled
- [ ] Analytics tracking set up (Google Analytics, HubSpot)

### Week 1 Launch

- [ ] Announce on LinkedIn (launch post)
- [ ] Send to existing network (email)
- [ ] Begin DM outreach (50 DMs)
- [ ] Publish first blog post
- [ ] Book first discovery calls

---

## Support Resources

**Tools Used:**
- Canva (design): canva.com
- Carrd (website): carrd.co
- HubSpot (CRM/email): hubspot.com
- Calendly (scheduling): calendly.com
- Google Analytics (tracking): analytics.google.com
- LinkedIn (social): linkedin.com

**AI Tools:**
- MiniMax 2.1 (blog content): For generating blog post content
- ChatGPT/Claude (copy assistance): For adapting templates

**Recommended Reading:**
- [`MARKETING_SYSTEM.md`](Baselayer/covered-ai-v2/MARKETING_SYSTEM.md) - Full strategy
- [`linkedin-strategy.md`](Baselayer/covered-ai-v2/linkedin-strategy.md) - LinkedIn posts
- [`email-sequences.md`](Baselayer/covered-ai-v2/email-sequences.md) - Email templates

---

*Document Version: 1.0*
*Created: January 2026*
*For: covered.AI Implementation*

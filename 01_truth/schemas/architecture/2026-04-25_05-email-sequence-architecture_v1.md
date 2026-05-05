---
title: "Email Sequence Architecture"
id: "05-email-sequence-architecture"
version: 1
created: "2026-04-25"
type: "document"
topic_type: "architecture"
audience: "internal"
layer: "truth"
status: "filed"
signed_by: "Devon, 2026-04-25, devin-992682c244cf444f91e0a516498afbfd"
---

# Email Sequence Architecture

## covered.AI Automated Email Workflows

This document outlines the complete email automation system for covered.AI, designed to nurture leads through a low-friction, trust-building sequence that culminates in booking a discovery call.

---

## Overview

The email sequence follows a 7-email drip campaign over 21 days, designed to:
- Build trust through honesty and specificity
- Validate pain points before offering solutions
- Demonstrate expertise without corporate jargon
- Create low-friction entry points for engagement
- Nurture leads until they're ready to book

**Key Metrics Target:**
- Open Rate: 40%+
- Click Rate: 15%+
- Reply Rate: 5%+
- Booking Rate: 2-3%
- Audit-to-Client Conversion: 30%

---

## Email Sequence Timeline

### Day 0: Welcome Email (#1)
**Purpose:** Set expectations, establish credibility, introduce the low-friction philosophy

**Trigger:** New subscriber (opt-in)

**Timing:** Immediate

**Key Message:** "We tighten. We don't transform."

---

### Day 3: Problem Identification Email (#2)
**Purpose:** Validate a specific pain point (late payments)

**Trigger:** Day 3 after welcome

**Key Message:** "The £8K-15K you're not collecting"

---

### Day 5: Case Study Email (#3)
**Purpose:** Social proof through specific results

**Trigger:** Day 5 after welcome

**Key Message:** "How Mark got 20 hours back without changing anything"

---

### Day 7: Lead Magnet Email (#4)
**Purpose:** Offer the free audit

**Trigger:** Day 7 after welcome

**Key Message:** "Your free £1,500 process audit"

---

### Day 10: Objection Handling Email (#5)
**Purpose:** Address common concerns

**Trigger:** Day 10 if no booking

**Key Message:** "If you're thinking..."

---

### Day 14: Scarcity Email (#6)
**Purpose:** Create urgency without pressure

**Trigger:** Day 14 if no booking

**Key Message:** "2 spots left this month"

---

### Day 21: Final Follow-up Email (#7)
**Purpose:** Graceful exit or re-engagement

**Trigger:** Day 21 if no booking

**Key Message:** "No pressure. Here to help when ready."

---

## Conditional Logic Flow

### Branch A: Clicked Calendly Link
**Trigger:** Subscriber clicks booking link

**Action:** Send "Appointment Confirmation" email immediately
- Confirm date/time
- Provide preparation instructions
- Set expectations for call

**Day -1:** Send "Reminder" email
- Confirm call tomorrow
- Ask to prepare 3 things

**Day 0:** Call occurs

**Day +1:** Send "Thank You" email
- Ask for feedback
- Provide next steps
- Offer additional resources

---

### Branch B: Reply with "LATE"
**Trigger:** Subscriber replies with keyword "LATE"

**Action:** Send "Invoice Automation Guide" mini-series

**Email 6A:** "Your Invoice Automation Setup"
- Step-by-step reminder system
- Sample templates
- Tools recommendation

**Email 6B:** "Following Up Without Awkwardness"
- Script for polite persistence
- Timing suggestions
- Sample conversations

**Email 6C:** "Case Study: £8K Recovered"
- Real example
- Results breakdown
- CTA to book full audit

---

### Branch C: Reply with "INVOICE"
**Trigger:** Subscriber replies with keyword "INVOICE"

**Action:** Send "Quick Start Invoice Guide"
- Simplified version of Branch B
- 5 actionable steps
- Link to book audit

---

### Branch D: Didn't Open Email
**Trigger:** Email not opened after 48 hours

**Action:** Send "Resend" version with different subject line

**Example:**
- Original: "Welcome to covered.AI - Here's what happens next"
- Resend: "I spent 30 years building a practice. Here's what I learned."

---

### Branch E: Didn't Click Link
**Trigger:** Email opened but no link click after 72 hours

**Action:** Send "Nudge" email
- Shorter, more direct
- Reiterate key benefit
- Different CTA format

---

### Branch F: Hard Bounce
**Trigger:** Email address invalid

**Action:** Remove from list
- Log in CRM
- Note reason
- Do not attempt re-engagement

---

### Branch G: Unsubscribed
**Trigger:** Subscriber opts out

**Action:** Remove from list immediately
- Respect preference
- Do not add to other sequences
- Note in CRM for future reference

---

## HubSpot Workflow Setup

### Workflow 1: Main Nurture Sequence
```
Trigger: Contact created with tag "new-subscriber"

IF:
  Email opened = True
  THEN wait 72 hours
  ELSE send "Welcome Resend" → wait 72 hours

IF:
  Email opened = True
  THEN send "Problem ID" email

IF:
  Email opened = True
  THEN wait 48 hours
  ELSE send "Problem ID Resend"

[Continue pattern through all 7 emails]
```

### Workflow 2: Branch Handling
```
Parallel to main sequence:

IF:
  Property "Clicked Calendly" = True
  THEN enroll in "Post-Booking Sequence"

IF:
  Property "Last Reply" contains "LATE"
  THEN enroll in "Invoice Guide Series"

IF:
  Property "Unsubscribed" = True
  THEN remove from all workflows
```

### Workflow 3: Post-Booking
```
Trigger: Property "Audit Booked" = True

Email 1: Confirmation (immediate)
Email 2: Reminder (24 hours before)
Email 3: Thank You (4 hours after)
Email 4: Feedback Request (48 hours after)
```

---

## Email Performance Dashboard

### Weekly Metrics to Track
| Metric | Target | Current | Trend |
|--------|--------|---------|-------|
| Open Rate | 40%+ | ___ | ↑/↓/→ |
| Click Rate | 15%+ | ___ | ↑/↓/→ |
| Reply Rate | 5%+ | ___ | ↑/↓/→ |
| Booking Rate | 2-3% | ___ | ↑/↓/→ |
| Unsubscribe Rate | <0.5% | ___ | ↑/↓/→ |
| Bounce Rate | <1% | ___ | ↑/↓/→ |

### Monthly Review Checklist
- [ ] Identify top-performing email
- [ ] Identify bottom-performing email
- [ ] Test new subject lines for underperformers
- [ ] Update send times based on engagement data
- [ ] A/B test CTA buttons
- [ ] Review reply reasons for insights
- [ ] Update conditional logic based on behavior
- [ ] Refresh email content if performance declines

---

## Send Time Optimization

### Best Send Times (Based on UK SMB Audience)
| Day | Best Time | Rationale |
|-----|-----------|-----------|
| Tuesday | 9:00 AM | Start of business week |
| Wednesday | 11:00 AM | Mid-week focus |
| Thursday | 8:00 AM | Before weekend catch-up |
| Friday | 10:00 AM | End of week planning |

### Send Time by Email Type
| Email Type | Optimal Day | Optimal Time |
|------------|-------------|--------------|
| Welcome | Tuesday | 9:00 AM |
| Problem ID | Thursday | 11:00 AM |
| Case Study | Wednesday | 8:00 AM |
| Lead Magnet | Tuesday | 10:00 AM |
| Objection | Thursday | 3:00 PM |
| Scarcity | Wednesday | 9:00 AM |
| Final Follow-up | Friday | 11:00 AM |

---

## Subject Line Testing Framework

### A/B Test Structure
**Test 1:** Curiosity vs. Specificity
- A: "Your biggest money drain (and it's fixable)"
- B: "The £15K leak in your business"

**Test 2:** Question vs. Statement
- A: "Quick question: How much are you losing?"
- B: "How to collect £8K more per month"

**Test 3:** Time vs. Money
- A: "Get 20 hours back this month"
- B: "Collect £8K more this month"

### Winning Subject Line Criteria
- Open rate above 40%
- Aligns with brand voice
- Honest and specific
- Creates curiosity without clickbait

---

## Email Deliverability Checklist

### Technical Setup
- [ ] Verified sending domain (covered.ai)
- [ ] SPF record configured
- [ ] DKIM signature enabled
- [ ] DMARC policy in place
- [ ] Custom tracking domain set up
- [ ] List unsubscribe link in every email
- [ ] Physical address included (legal requirement)

### List Hygiene
- [ ] Remove bounced addresses immediately
- [ ] Suppress unsubscribes within 24 hours
- [ ] No purchased lists
- [ ] Double opt-in for new subscribers
- [ ] Regular list cleaning (quarterly)

### Content Best Practices
- [ ] Plain text version available
- [ ] Images have alt text
- [ ] Links are clean and tracked
- [ ] No spam trigger words
- [ ] Subject line under 50 characters
- [ ] Preheader text optimized
- [ ] Mobile-responsive design

---

## Compliance Notes

### GDPR Requirements
- Explicit consent required before adding to sequence
- Easy unsubscribe in every email
- Privacy policy linked in footer
- No pre-checked consent boxes
- Clear explanation of what they'll receive

### CASL Requirements (Canada)
- Canada-specific consent required
- Sender identification clear
- Unsubscribe processed within 10 days

### CAN-SPAM Requirements (USA)
- No deceptive subject lines
- Physical address included
- Clear unsubscribe process
- Honor opt-outs promptly

---

## Email Copy Guidelines

### Voice Rules (Applied to All Emails)
✓ DO:
- Use specific numbers (£8K, 20 hours, 30%)
- Reference Ewan's dental background
- Validate current approach ("You're not broken")
- Emphasize low-friction ("no disruption")
- Use conversational tone ("Quick question...")
- Be honest about limitations

✗ DON'T:
- Use corporate jargon ("synergy," "leverage")
- Make overnight promises
- Use vague adjectives ("amazing," "incredible")
- Create false urgency ("ACT NOW!")
- Oversell or hype
- Use all caps or excessive exclamation points

---

## Template Placeholders

Replace these in implementation:

```
{{first_name}} - Subscriber's first name
{{company_name}} - Subscriber's company name
{{pain_point}} - Specific pain mentioned in reply
{{calendly_link}} - Booking link
{{email}} - Contact email
{{phone}} - Contact phone
{{social_link}} - LinkedIn profile link
{{unsubscribe_link}} - Legal unsubscribe
{{privacy_link}} - Privacy policy link
{{preview_text}} - Email preview text
```

---

## Quick Reference: Email Send Schedule

| Day | Email | Status |
|-----|-------|--------|
| 0 | Welcome #1 | Ready |
| 3 | Problem ID #2 | Ready |
| 5 | Case Study #3 | Ready |
| 7 | Lead Magnet #4 | Ready |
| 10 | Objection #5 | Ready |
| 14 | Scarcity #6 | Ready |
| 21 | Final #7 | Ready |

**Total Sequence Length:** 21 days

**Review Points:** Days 14 and 21

**Decision Points:** Days 10, 14, 21

---

## Next Steps

1. **Set up HubSpot workflow** using this architecture
2. **Create email templates** in HubSpot Design Tools
3. **Configure conditional logic** branches
4. **Test workflow** with sample contacts
5. **Launch** and begin monitoring metrics
6. **Weekly review** of performance data
7. **Monthly optimization** based on results

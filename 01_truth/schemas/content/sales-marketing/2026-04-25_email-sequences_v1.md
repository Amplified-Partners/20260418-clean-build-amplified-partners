---
title: "covered.AI Email Sequences"
id: "email-sequences"
version: 1
created: "2026-04-25"
type: "document"
topic_type: "sales-marketing"
audience: "internal"
layer: "truth"
status: "filed"
signed_by: "Devon, 2026-04-25, devin-992682c244cf444f91e0a516498afbfd"
---

# covered.AI Email Sequences

**Version:** 1.0  
**Date:** January 2025  
**Purpose:** Automated email workflows for HubSpot automation  
**Channel:** Email marketing via HubSpot  
**Audience:** UK SMB owners (£500K-£3M revenue, 3-15 staff)

---

## Email Architecture Overview

**7-Email Sequence Flow:**

| Day | Email | Purpose |
|-----|-------|---------|
| 0 | Welcome Email #1 | Introduce Ewan, validate pain, set expectations |
| 3 | Problem ID Email #2 | Specific problem focus (late payments) |
| 5 | Case Study Email #3 | Real results from similar client |
| 7 | Lead Magnet Email #4 | Free audit offer |
| 10 | Objection Handling #5 | Address common concerns |
| 14 | Scarcity Email #6 | "2 spots left" (if no booking) |
| 21 | Final Follow-up #7 | Last touch before breakaway |

**Conditional Logic:**
- If clicked Calendly → Send confirmation + reminder sequence
- If replied "LATE" → Trigger invoice automation guide series
- If replied "INVOICE" → Trigger setup guide
- If didn't open → Resend with different subject line
- If didn't click → Continue to next email
- If booked → Remove from sequence

---

## Email 1: Welcome Email

**Subject Line Options:**
1. "Welcome to covered.AI - Here's what happens next"
2. "I spent 30 years building a practice. Here's what I learned."
3. "Your first step to getting 20 hours/week back"

**Preview Text:** "30 years in dental. Here's what I learned about running a business."

---

**EMAIL BODY:**

Hi [First Name],

Thanks for signing up. Let me introduce myself properly.

I'm Ewan Bramley. I spent 30 years running a dental practice in Byker, Newcastle. 30 staff. Hundreds of patients. Millions in revenue.

And I spent most of that time working 60+ hours a week, doing everything myself, and wondering why I was so exhausted.

Here's what I learned: You don't need to transform your business. You need to tighten it.

**What I do now:**

I help UK SMBs—dental, salon, vet, trades, consulting—get 10-20 hours back per week and collect £8K-15K more per month. Not by changing how you work. By automating the busywork and running in the background.

**What happens next:**

I'll send you a few emails over the next couple of weeks. Some will share specific problems I help solve. Others will show real results from clients like you. One will offer a free process audit to find your biggest money leaks.

No hype. No sales pressure. Just useful information and an offer if you want to explore further.

**Quick question:**

Reply to this email and tell me: What's your biggest time-waster right now? Invoicing? Follow-ups? Chasing payments? Data entry?

Whatever it is, I probably help with it.

Talk soon,

Ewan

**P.S.** If you're losing money to late payments specifically, reply with "LATE" and I'll send you a quick guide on automating invoice reminders.

---

**Personalization Tags:**
- `{{contact.firstname}}` - First name
- `{{contact.company}}` - Company name
- `{{contact.email}}` - Email address
- `{{company.industry}}` - Industry (dental, salon, vet, etc.)

**Reply Automation:**
- Trigger: Email replied with "LATE"
- Action: Add to "Invoice Automation Guide" workflow
- Trigger: Email replied with any text
- Action: Create task for Ewan to personally reply within 24 hours

---

## Email 2: Problem Identification Email

**Subject Line Options:**
1. "The £15K leak (and how to plug it)"
2. "Quick question: How much money are you losing?"
3. "Your biggest money drain (and it's fixable)"

**Preview Text:** "Most UK SMBs are owed £8K-15K in late payments."

---

**EMAIL BODY:**

Hi [First Name],

Here's a quick question:

How much money are you owed right now?

Not "eventually." Right now. Invoices that are 30, 60, 90 days past due. Clients who keep saying "I'll pay next week." Money that's yours but sitting in their bank account.

**The numbers:**

UK SMBs are owed £11 billion in late payments every year. 41% of small businesses experience payment delays of more than a month. The average business has £8K-£15K stuck in unpaid invoices at any given time.

**Why it happens:**

It's not that clients are bad people. It's that:
- Invoices get lost in their inbox
- Reminders feel awkward to send
- You're too busy doing the work to chase the money
- There's no system—just hoping and waiting

**Here's what we did for one client:**

Sarah runs a salon in Newcastle. She was owed £11K in late payments. Some clients were 90 days over. She felt awkward chasing them—it felt "unprofessional."

We set up automated invoice reminders. Polite. Persistent. Consistent.

Within 60 days, she collected £8,400 of that £11K. The reminders were friendly but firm. Clients responded better to "automated" than to her personal chase emails.

**Why it works:**

- Automatic (you don't have to think about it)
- Polite but persistent (no damaged relationships)
- Consistent (same message, same timing, every time)
- Professional (comes from a system, not personal pressure)

**Next step:**

If this sounds familiar—if you're owed money you're not collecting—reply with "INVOICE" and I'll send you a quick guide on setting up automated reminders.

Or reply with your biggest invoice challenge and we'll chat.

Talk soon,

Ewan

**P.S.** This works for any service business. Dental, vet, trades, consulting—if you invoice clients, you can automate the follow-up.

---

**Conditional Branch:**
- Reply "INVOICE" → Trigger "Invoice Automation Setup Guide" 3-email sequence
- Click Calendly link → Trigger "Post-Click Nurture" sequence
- No action → Continue to Email 3 on Day 5

---

## Email 3: Case Study Email

**Subject Line Options:**
1. "How Mark got 20 hours/week back (without changing anything)"
2. "Real results from a dental practice (like yours?)"
3. "This is what happened when we stopped chasing invoices"

**Preview Text:** "20 hours back per week. £45K more revenue. Zero disruption."

---

**EMAIL BODY:**

Hi [First Name],

Let me tell you about Mark.

Mark runs a dental practice in Durham. 12 staff. About £1.2M revenue. Like you, he was working 50+ hours a week doing everything.

Here's what his weeks looked like:

**Before:**

- Monday: 8am-8pm. Admin in the morning, patients all afternoon, more admin in the evening.
- Tuesday: Same.
- Wednesday: Same.
- Thursday: Same.
- Friday: Catch up day. Invoices, follow-ups, chasing payments.
- Weekend: Catch up more. Update spreadsheets. Plan next week.

He hadn't taken a real holiday in 5 years. His team didn't know how to handle anything without asking him. He was exhausted.

**What we did:**

Week 1: We audited what he was already doing. No changes yet. Just watching and identifying where time was leaking.

Weeks 2-4: We automated the busywork. Invoice reminders. Lead follow-ups. Data entry. Appointment confirmations. Payment chasing.

Weeks 5+: We let it run in the background. His team didn't notice anything different. No new software. No retraining. Just things happening automatically.

**The results:**

- **20 hours per week** back (that's a whole day)
- **£45,000 more revenue** in 90 days (from better follow-up and payment collection)
- **His team runs the marketing now** (automated nurture sequences)
- **He works 4 days a week** (and takes actual holidays)

**What we didn't do:**

- No "transformation"
- No retraining his team
- No new software to learn
- No disruption to his work
- No 6-month project

**Here's what Mark said:**

> "I was skeptical. Consultants always want to change everything. These guys just... fixed it. Set it up, left it running. My team didn't even notice. The invoices just got paid faster."

**The point:**

This isn't a transformation story. It's a tightening story. We found the leaks, plugged them, and got out of the way.

If Mark's situation sounds familiar—if you're working too many hours and the business still depends on you—book a free process audit and we'll find your biggest leaks.

[CALENDLY LINK - BOOK YOUR FREE AUDIT]

Talk soon,

Ewan

**P.S.** Typical setup takes 4-6 weeks. Disruption: Zero. Results: 10-20 hours back, £8K-15K more collected. That's the promise.

---

**Personalization Options:**
- Swap "dental" for "salon", "vet", "trades", "consulting" based on industry
- Adjust staff count and revenue to match prospect's stated size
- Select most relevant case study (industry match)

---

## Email 4: Lead Magnet Email

**Subject Line Options:**
1. "Your free process audit (worth £1,500)"
2. "Let's find your £15K leak (free 30-min call)"
3. "I want to audit your business for free"

**Preview Text:** "No pitch. No pressure. Just finding your biggest money leaks."

---

**EMAIL BODY:**

Hi [First Name],

I'm offering something unusual for a consultant:

A free process audit.

No catch. No pitch. No "and now let me show you our pricing." Just 30 minutes of my time finding where your business is leaking money.

**What you get:**

In 30 minutes (Zoom or phone), we'll:
1. Walk through your current processes (invoicing, follow-ups, lead capture, payment collection)
2. Identify 3-5 specific leaks where money is escaping
3. Pinpoint 2-3 quick wins you could implement this month
4. Show you exactly how much money you're losing (typically £8K-£15K in late payments alone)

**Who this is for:**

- UK service business (£500K-£3M revenue, 3-15 staff)
- Owner working 50+ hours/week
- Frustrated by late payments or inconsistent leads
- Open to automation but don't want disruption
- Want results, not transformation

**Who this isn't for:**

- Happy with status quo
- Looking for "transformation" or "revolution"
- Expect overnight miracles
- Unwilling to spend 30 minutes reviewing their processes

**How to book:**

Pick a time here: [CALENDLY LINK]

Before the call, I just need you to have:
1. A rough walkthrough of how you handle invoices and payments
2. Your last 30 days of invoices (to see payment patterns)
3. Your top 3 pain points written down

That's it. No homework. No preparation. Just showing up.

**What happens after:**

If I find real opportunities, I'll show you. If I don't—if your processes are already tight and you're not losing money—I won't waste your time with a pitch.

Honesty builds trust. If you're not a fit, I'll tell you.

Book your audit: [CALENDLY LINK]

Talk soon,

Ewan

**P.S.** Recent clients found £8K-£15K in their first audit. One found £22K in missed follow-ups. That's why we do this.

---

**Calendly Setup:**
- Event name: "Free Process Audit - covered.AI"
- Duration: 30 minutes
- Questions in booking form:
  - Company name
  - Industry
  - Current revenue
  - Staff count
  - Top 3 pain points
  - How did you hear about us?
- Confirmation email: Send immediately
- Reminder email: 24 hours before
- Follow-up email: If no show within 48 hours

---

## Email 5: Objection Handling Email

**Subject Line Options:**
1. "Let me address your concerns (honestly)"
2. "If you're thinking 'this sounds too good to be true...'"
3. "3 concerns prospects have (and why they shouldn't stop you)"

**Preview Text:** "Skepticism is healthy. Let me address it."

---

**EMAIL BODY:**

Hi [First Name],

I get it. You're probably thinking one of three things:

**"Sounds too good to be true."**

Fair. Here's the reality: We don't promise overnight miracles. We promise systematic improvement. The 10-20 hours back and £8K-15K more collected are averages from clients who completed the full program. It takes 4-6 weeks. It requires you to give us access to your systems. And you need to actually implement what we build.

If you're looking for a magic button, we're not it. If you're looking for a proven process that delivers specific results, we are.

**"I don't have time for this."**

That's literally the problem we solve. Yes, there's a 30-minute audit. Yes, there's some setup. But after that, we do the work. You keep running your business. The improvements happen in the background.

The audit itself takes 30 minutes. The setup takes 4-6 weeks of our time, not yours. You review, approve, and the systems go live. No retraining. No new software. No disruption.

**"I've tried automation before and it didn't work."**

Most "automation" fails because it's poorly implemented. Generic tools, wrong configuration, no integration. We build custom automation for your specific situation. We test it. We refine it. We make it work.

Also, automation without process documentation is fragile. We do both: automate AND document. That's why our clients see results that stick.

**Bottom line:**

If this doesn't feel right for you, don't book. Read a few more emails. Check out our case studies. Or just reply and tell me why you're hesitant—I respect honesty.

If it does feel right, the audit is here: [CALENDLY LINK]

No pressure. Just an opportunity to see if we're a fit.

Talk soon,

Ewan

---

## Email 6: Scarcity Email

**Subject Line Options:**
1. "Only 2 spots left this month"
2. "Opening for new clients closes Friday"
3. "Quick update: We're almost full for January"

**Preview Text:** "We're selective about who we work with. Here's why."

---

**EMAIL BODY:**

Hi [First Name],

I wanted to give you a quick update.

We're only taking 2 new clients this month.

Why? Because we only work with businesses we're confident we can help. And we can only deliver quality results if we have capacity to do the work properly.

This isn't a sales tactic. It's genuinely how we operate. We turn away more businesses than we accept—because not every business is a fit, and I'd rather be honest about that than take your money and deliver mediocre results.

**If you're interested, here's what I'd suggest:**

Book your free audit this week. If we're a fit, we'll have capacity. If not, I'll tell you honestly.

[CALENDLY LINK - BOOK YOUR FREE AUDIT]

**Quick honesty:**

If you're looking for "transformation" or expect results in weeks, we're probably not the right fit. We tighten existing processes—we don't rebuild businesses. That means results take 4-6 weeks to implement, not 4-6 days.

But if you're working 50+ hours a week, losing money to late payments, and want results without disruption, we can probably help.

Book or don't—either way, I appreciate you reading these emails.

Talk soon,

Ewan

---

**Conditional Logic:**
- Only send if no Calendly booking by Day 12
- If booked → Remove from sequence
- If replied with questions → Personal reply, remove from sequence
- If unsubscribed → Remove from all sequences

---

## Email 7: Final Follow-up / Breakaway Email

**Subject Line Options:**
1. "One last message (then I'll leave you alone)"
2. "Not the right time? That's fine."
3. "If you're not interested, just ignore this"

**Preview Text:** "No hard feelings. Just leaving the door open."

---

**EMAIL BODY:**

Hi [First Name],

I've sent you a few emails now. I figure you probably know if this is for you or not.

**If you're not interested:**

No hard feelings. Really. I'd rather you unsubscribe than keep getting emails you don't want. The link is at the bottom.

**If you were interested but it's just not the right time:**

Fair enough. Business decisions take time. I'll leave you alone for now—but if you come back to this in a month or two, the offer still stands. Same process, same commitment.

**If you were interested but something stopped you:**

Reply and tell me what it was. Cost? Skepticism about results? Timing? I won't try to "overcome your objection"—I just want to understand. Maybe there's something I can clarify. Maybe not. Either way, you'll get an honest answer.

**If you were planning to book and just haven't got around to it:**

The calendar's still here: [CALENDLY LINK]

No pressure. No rush. Just an open door.

Thanks for your time,

Ewan

---

**Breakaway Handling:**
- If no action → Add to "Re-engagement" list for 90-day dormant sequence
- If unsubscribe → Remove from all active sequences, add to do-not-contact list
- If bounce → Verify email address, remove if invalid

---

## HubSpot Automation Setup

**Workflow 1: Welcome Sequence**

```
Trigger: New contact created (form submission or manual add)
Delay: 0 hours
Action: Send Email 1 (Welcome)
Delay: 3 days
Action: Send Email 2 (Problem ID)
Delay: 2 days
Action: Send Email 3 (Case Study)
Delay: 2 days
Action: Send Email 4 (Lead Magnet)
Delay: 3 days
Action: Send Email 5 (Objection Handling)
Delay: 4 days
Action: Send Email 6 (Scarcity) - ONLY IF no Calendly booking
Delay: 7 days
Action: Send Email 7 (Final Follow-up) - ONLY IF no Calendly booking
```

**Workflow 2: Calendly Booking Path**

```
Trigger: Contact books audit
Action: Send "Booking Confirmation" email with prep instructions
Action: Add to "Post-Booking" list
Delay: 24 hours before meeting
Action: Send "Reminder" email with prep notes
Delay: After meeting
Action: Send "Thank You / Next Steps" email
```

**Workflow 3: Reply Handling**

```
Trigger: Contact replies to any email with "LATE"
Action: Add to "Invoice Automation Guide" workflow
Action: Send Invoice Guide Email 1
Delay: 3 days
Action: Send Invoice Guide Email 2
Delay: 3 days
Action: Send Invoice Guide Email 3 with Calendly link
```

**Workflow 4: Non-Responder Recovery**

```
Trigger: Email bounced (no open after 3 sends)
Action: Verify email address
Action: Send "Are we in spam?" email
Delay: 7 days
Action: Final check-in email
```

---

## Email Performance Metrics

| Metric | Target | Definition |
|--------|--------|------------|
| Open Rate | 40%+ | Opened / Delivered |
| Click Rate | 15%+ | Clicked / Opened |
| Reply Rate | 5%+ | Replied / Delivered |
| Booking Rate | 2-3% | Booked / Delivered |
| Conversion | 30% | Booked → Paid Client |

**Weekly Monitoring:**
- Track open rates by subject line
- Track click rates by email
- Track reply triggers and responses
- A/B test subject lines monthly
- Remove underperformers from rotation

---

## Reply Templates for Personal Responses

**Positive Reply:**
```
Hi [Name],

Thanks for getting in touch. I'd love to chat.

Book a time here: [CALENDLY LINK]

Looking forward to learning about [Company] and seeing if we can help.

Talk soon,
Ewan
```

**Question Reply:**
```
Hi [Name],

Great question. [Answer to their question]

[Relevant case study or example]

Does that help? Happy to clarify more or jump on a quick call.

Book here if you'd like to explore further: [CALENDLY LINK]

Best,
Ewan
```

**Not a Fit Reply:**
```
Hi [Name],

Thanks for being honest about where you are.

You're right—we probably aren't the right fit right now. What you're looking for (transformation / overnight results / cheap solution) isn't what we deliver.

If your situation changes and you want to explore low-friction optimization, reach out. The offer will still be here.

Best of luck with [their goal].

Ewan
```

---

*This email sequence should be implemented in HubSpot with the automation workflows shown above. Each email has been written to match the covered.AI brand voice: specific numbers, low-friction positioning, honest limitations, no corporate jargon.*

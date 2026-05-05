---
title: "TECH STACK INTEGRATION ROADMAP"
id: "tech-stack-integration-roadmap-v1"
version: 1
created: "2026-04-25"
type: "document"
topic_type: "architecture"
audience: "internal"
layer: "truth"
status: "filed"
signed_by: "Devon, 2026-04-25, devin-992682c244cf444f91e0a516498afbfd"
---

# TECH STACK INTEGRATION ROADMAP
**What They Use. Where You Plug In. How You Upsell Multi-Channel Communications + AI**

---

## WHAT UK SMBs ACTUALLY USE (2026 Market Data)

### Accounting Software (Primary - Everyone Has One)

| Software | Market Share | Price | Typical User | API Quality |
|----------|-------------|-------|-------------|------------|
| **Xero** | 25-30% | £12-70/mo | Growing SMBs | Excellent |
| **Sage** | 20-25% | £14-200+/mo | Established, accountants | Good |
| **QuickBooks Online** | 15-20% | £10-50/mo | Service-based | Excellent |
| **FreshBooks** | 8-12% | £15-40/mo | Freelancers, time-tracking | Good |
| **Tide** | 5-8% | £9.99/mo | Micro-businesses | Limited |

**Key insight:** Xero + Sage dominate (50%+ combined). Both have excellent APIs. QuickBooks popular for payroll integration.

---

### Communication Tools (Fragmented - Everyone Uses Different Stuff)

**Email (95%+ adoption):**
- Gmail or Outlook (business versions)
- Usually free or £6-14/month
- **Problem:** No integration with other tools

**Phone Systems (25-35% adoption):**
- Traditional mobile phones (everyone)
- Some use Zoom Phone (50% adoption post-2020)
- Few use dedicated VoIP (RingCentral, Vonage, Nextiva 15-20%)
- **Problem:** Separate from email, no recording/context

**CRM (40-50% adoption):**
- HubSpot (most popular - 30% of those who use CRM)
- Pipedrive (20%)
- Salesforce (10%)
- Others: Zoho, Monday, Asana
- **Problem:** Data doesn't sync automatically

**Instant Messaging (30% adoption):**
- Slack (larger teams)
- Microsoft Teams (if they're Microsoft shop)
- Google Chat (if they're Google shop)
- **Problem:** Another siloed channel

**Typical Newcastle SMB Stack:**
- Xero (accounting)
- Gmail (email)
- HubSpot free or Pipedrive (CRM, if they have one)
- Google Drive (file storage)
- Zoom/Teams (video calls)
- Manual processes for everything else

**Total they spend:** £2,500-4,000/month (tools + admin staff doing manual work)

---

## WHERE YOU ADD VALUE: The 8 Gaps They Have

| Gap | Current Reality | Your Solution |
|-----|-----------------|----------------|
| **Unified Communications** | Email, phone, SMS all separate | Single dashboard inbox (all channels) |
| **AI-Assisted Responses** | Manual email replies (slow) | AI drafts replies with customer context |
| **No Call Recording** | Calls disappear (no record) | Every call recorded + transcribed + logged |
| **No Customer Context** | Each call = start from scratch | AI pulls customer history automatically |
| **Manual Follow-ups** | Leads go cold (forgotten) | AI identifies follow-up needed, schedules it |
| **No Phone Analytics** | "How did that call go?" | Call analytics + performance tracking |
| **Intelligent Routing** | Calls to wrong person, voicemail | Route call based on skills + availability |
| **Staff Performance Blind** | Don't know who's handling what | Dashboard shows who's doing what, how fast |

**Total hidden cost of these gaps:** £1,500-2,500/month in lost productivity + frustrated customers

---

## YOUR 5-PHASE INTEGRATION ROADMAP

### PHASE 1: FOUNDATION (Weeks 1-4)
**You're already doing this**

**Build:**
- API connectors: Xero, QuickBooks, Gmail, Google Calendar
- Analytics layer: Pull financial data, identify patterns
- Dashboard: Show findings to owner

**Output:** Financial extraction + immediate ROI proof
**Value:** Owner sees money leaking (Day 1 hook)

---

### PHASE 2: SINGLE INBOX (Weeks 5-8)
**Start after Phase 1 works**

**Build:**
- Gmail inbox aggregator (all emails)
- WhatsApp Business API connector
- SMS (Twilio) connector
- Calendar sync (shows busy/available)
- CRM auto-sync (new email = auto-logged in HubSpot/Pipedrive)

**How it works:**
- Owner goes to ONE dashboard
- Sees: Emails, WhatsApp messages, SMS, calendar, CRM notes all in one place
- Clicks to reply to anything
- System auto-logs in CRM + calendar reminder for follow-up

**Why it matters:**
- Customers can reach them SMS, WhatsApp, email, phone
- They respond from ONE place (not 5 different apps)
- Never miss a message

**Build time:** 2-3 weeks (WhatsApp API is straightforward, Twilio is one day)

**Value:** +2-3 hours/week saved just from unified interface

---

### PHASE 3: AI-ASSISTED RESPONSES (Weeks 9-12)
**High-value, builds on Phase 2**

**Build:**
- Claude API integration to draft smart replies
- Context-aware: Pulls customer history from CRM before drafting
- Tone matching: Learns their writing style
- Human approval workflow: AI suggests, human clicks "send"

**How it works:**
```
Customer WhatsApp: "Hi, can I move my appointment from Tuesday to Friday?"
System pulls: Customer record, history, preferences
Claude drafts: "Hi [Name]! Of course! I can move your appointment to Friday at 3 PM. 
               Does that work for you? Let me know if you'd prefer a different time."
Owner sees: Draft reply, clicks ✓ Send or edits it
System: Sends message + logs in CRM + updates calendar
```

**Why it matters:**
- Responses consistent (brand voice)
- Fast (AI drafts in seconds)
- Customer context = better replies
- Never forget a follow-up

**Build time:** 1-2 weeks (Claude API + CRM sync)

**Value:** -50% response time, 0% missed follow-ups

---

### PHASE 4: TELEPHONY + AI (Weeks 13-16)
**The big one - transforms phone calls**

**Option A: Integrate Existing Phone System**
- If they have RingCentral/Vonage: Use their API
- If they just have mobile: Recommend move to Vonage (£20-30/mo total cost drop)
- If they use Zoom: Already has phone system built-in

**Build:**
- Call recording (with their consent)
- AI transcription: Converts call to text (90%+ accuracy)
- Auto-log to CRM: Call summary + next steps auto-populate
- Call analytics: Duration, when, who, resolution rate

**How it works:**
```
Customer calls about invoice
Phone rings → Dashboard shows customer name + history
Agent answers → Call recorded & transcribed in real-time
Customer: "The invoice I got on Tuesday was wrong"
System captures: Issue type, action needed
Call ends → CRM auto-updated: "Customer complained about invoice, reissued corrected version"
Manager sees: Call summary, action taken, issue resolved
Next time customer calls → Agent sees full history (not start from scratch)
```

**Why it matters:**
- Every conversation documented (no more "I forgot what they said")
- Can improve based on patterns
- Customer feels heard (context remembered)
- Staff accountability (calls tracked)

**Build time:** 2-3 weeks (Vonage API straightforward, transcription is 3rd-party)

**Value:** +4 hours/week saved on admin, +20% customer satisfaction

---

### PHASE 5: INTELLIGENT ROUTING (Weeks 17+)
**Nice-to-have, builds on Phase 4**

**Build:**
- Recognize caller (check if in CRM)
- Route based on: Agent skills, availability, history with customer
- Suggest next action to agent before they answer
- Auto-escalate complex issues

**How it works:**
```
Customer calls (VoIP system recognizes them)
Dashboard shows: "It's Dave Miller - asked about refunds 3 times, always angry"
Routes to: Sarah (best with difficult customers, available)
Pops up suggestion: "Offer 10% discount OR full refund - Dave responds to this"
Sarah answers: "Hi Dave, I saw your concern about X..."
Result: Happy customer, faster resolution, right person took it
```

**Why it matters:**
- Reduces call time (15% average)
- Improves resolution rate (first time)
- Protects difficult customers (routed to best person)
- Data-driven decisions

**Build time:** 3-4 weeks

**Value:** +10% efficiency, +5% customer satisfaction

---

## THE TECH STACK YOU'LL CONNECT TO

### APIs You'll Use

| Category | Platforms | Ease | Notes |
|----------|-----------|------|-------|
| **Accounting** | Xero, QB, Sage | Easy | All have solid APIs |
| **Email** | Gmail, Outlook | Easy | Standard IMAP + API |
| **CRM** | HubSpot, Pipedrive, Salesforce | Easy | Excellent webhooks |
| **Messaging** | WhatsApp Business, Twilio | Easy | Well-documented |
| **Telephony** | Vonage, RingCentral, Zoom | Medium | APIs solid, setup involved |
| **Transcription** | AssemblyAI, Deepgram | Easy | Simple REST API |
| **Orchestration** | n8n, Zapier | Easy | Your automation backbone |

**Your advantage:** You're not reinventing. You're plugging into existing APIs (all well-documented, all stable).

---

## HOW YOU SELL THIS

### The Upsell Timeline

**Months 1-4: Sell them Phase 1 (Financial Extraction)**
- Tier 1: £2,500
- Pitch: "Find profit leaks in your business"
- Hook works: Average £2,400/month found

**Months 5-8: Upsell Phase 2-3 (Systems + Single Inbox)**
- Core Tier 3: £1,200/month (systems building)
- Pitch: "Let's build weekly automation. Also, let's unify your comms."
- They say yes: Start with Phase 2 (single inbox)
- First month they see: Saves 3-4 hours/week on email management alone

**Months 9-12: Add Phase 3 (AI Responses)**
- Add-on: +£300/month (total: £1,500/month)
- Pitch: "Your responses are faster. Customers get replies in minutes."
- They see: Fewer "Why haven't you replied?" complaints

**Months 13+: Offer Phase 4 (Telephony)**
- Premium module: +£300-400/month (total: £1,800-1,900/month)
- Pitch: "Every call documented. You'll know what customers say."
- They see: Customers feel heard, staff more efficient

---

## PRICING STRATEGY

### Current They Pay

- Xero: £40/month
- Email: £10/month
- CRM: £40/month
- Zoom Phone: £20/month
- Manual admin: £2,000-3,000/month
- **Total: £2,100-3,100/month (mostly wasted on admin)**

### Your Package (Phased)

**Month 1-4:** £2,500 (one-time Tier 1)
**Month 5+:** £1,200/month (Tier 3 - systems building)
**Month 9+:** £1,500/month (Tier 3 + Single Inbox + AI responses)
**Month 13+:** £1,800/month (Tier 3 + Full Comms Stack)

**Their ROI:**
- Saves £2,000-3,000/month (admin time eliminated)
- Your cost: £1,800/month
- **Net profit increase: £200-1,200/month from your service alone**

---

## WHAT MAKES THIS DIFFERENT

**Competitors:**
- Ring Central: £20-50/month (just phone)
- HubSpot: £45-1,200+/month (just CRM)
- Zapier: £20-299/month (just automation)
- Freshbooks: £15-70/month (just accounting)

**You:**
- Integrate everything (phone + email + SMS + CRM + accounting + AI)
- Provide strategy (which systems to build, when)
- Monitor & optimize (your dashboard shows what's working)
- Weekly delivery (builds momentum, engagement)
- Gamification (staff excited, not resistant)

**Your moat:** No one does this combination in Newcastle.

---

## WEEK 1 ACTION PLAN

### Phase 2 Foundation (Start Building Single Inbox)

- [ ] Integrate WhatsApp Business API
  - [ ] Get Business Account (WhatsApp Meta)
  - [ ] Request API access
  - [ ] Build incoming message handler
  - [ ] Test end-to-end

- [ ] Integrate Twilio (SMS)
  - [ ] Create account
  - [ ] Get phone number
  - [ ] Build incoming SMS handler
  - [ ] Test receiving messages

- [ ] Build unified inbox interface
  - [ ] Dashboard showing all messages (email, SMS, WhatsApp)
  - [ ] Unified reply composer
  - [ ] CRM auto-sync on new message

- [ ] Test with first client (by Week 4)
  - [ ] Show: All channels in one place
  - [ ] Measure: Time saved for them

- [ ] Phase 3 prep (start research)
  - [ ] AssemblyAI docs (for transcription)
  - [ ] Claude API multi-turn context

---

## 12-MONTH ROADMAP (Revenue Impact)

| Month | Phase | Revenue | Clients | Add-On |
|-------|-------|---------|---------|--------|
| 1-4 | Foundation | £7,500 (one client Tier 1) | 1 | None |
| 5-8 | Phase 2 (Inbox) | £6,000 (5 Tier 3) | 5 | None yet |
| 9-12 | Phase 3 (AI Responses) | £6,000 base + £1,500 add-on (1 upsells) | 5-6 Tier 3 | Comms (1 client) |
| 13+ | Phase 4 (Telephony) | £6,000 base + £3,000 add-ons | 5-6 Tier 3 | Comms (2-3 clients) |

**By Month 12:**
- Base Tier 3 revenue: £6,000/month (5 clients × £1,200)
- Add-on revenue: +£3,000/month (comms modules)
- **Total: £9,000/month (on top of Tier 1/2 sales)**

**Annual profit from recurring (Tier 3 only):** £90,000+

---

## TECHNICAL SETUP (What You Build)

### Core Architecture

```
Client's Existing Tools
├─ Xero (accounting)
├─ Gmail (email)
├─ Google Calendar (scheduling)
├─ HubSpot/Pipedrive (CRM)
└─ Possibly: Vonage/RingCentral (phone)
         ↓
YOUR INTEGRATION LAYER (n8n or custom)
├─ Data extraction (APIs pull data)
├─ Transformation (normalize data)
├─ Intelligence (Claude AI for analysis)
└─ Orchestration (trigger actions)
         ↓
YOUR UNIFIED DASHBOARD
├─ Financial analytics
├─ Unified inbox (email + SMS + WhatsApp)
├─ AI-suggested responses
├─ Call recording + transcription (if Phase 4)
└─ Performance tracking
         ↓
CLIENT SEES
├─ Dashboard (one place to manage everything)
├─ Integrations (their tools work seamlessly)
└─ Results (faster responses, better service, profit)
```

### Tech Stack You'll Use

- **Backend:** Python + Node.js (or whatever you prefer)
- **Orchestration:** n8n (self-hosted or cloud)
- **APIs:** Claude API, Zapier, Vonage, WhatsApp, Twilio
- **Frontend:** React dashboard
- **Database:** PostgreSQL
- **Hosting:** Railway or Render
- **Authentication:** OAuth2 (for their apps)

---

## KEY INSIGHT

**They don't need new tools. They need their existing tools to work together.**

Most SMBs have:
- Accounting software ✓
- Email ✓
- Phone ✓
- CRM ✓

**They're missing:** The glue that connects them.

That glue = your business.

You're not selling software. You're selling integration + intelligence + automation.

---

## NEXT STEPS

1. **Week 1-2:** Research WhatsApp Business API + Twilio
2. **Week 3-4:** Build Phase 2 (single inbox) prototype
3. **Week 5:** Test with first client willing to try
4. **Week 6-8:** Refine based on feedback
5. **Week 9+:** Roll out to existing Tier 3 clients as add-on

By Month 6, you'll have a replicable comms module ready to upsell to all Tier 3 clients at +£300-500/month.

That's an extra £1,500-2,500/month per 5 clients who take it.

**At 50% uptake rate:** +£4,500/month by Month 12

Go build it. 🚀

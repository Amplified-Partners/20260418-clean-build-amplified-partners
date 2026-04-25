---
date: 2026-02-24
source: sam
topic: dave workflow spec v1
status: research
reusable: true
original_path: /Users/ewanbramley/.openclaw/workspace/DAVE-WORKFLOW-SPEC-V1.md
swept_at: 2026-02-24T12:25:57.134019
---

# Dave's First Workflow: Voice Appointment Booking
**Spec version:** 1.0  
**Date:** February 22, 2026  
**Author:** Eli  
**Source research:** PUDDING-TECHNIQUE-EXTRACTION.md, SESSION-2026-02-22-RESEARCH-COMPLETE.md, smb-agentic-systems-research-2026.md  
**Status:** READY TO BUILD

---

## What This Is

Dave (Jesmond Plumbing) misses calls. Missed calls = missed jobs. This workflow answers every call, books appointments, and puts them in Dave's calendar — without Dave or anyone else being involved.

**Documented real-world result:** 50% reduction in missed calls, 20% increase in next-day bookings within 30 days (Cornell Design Group, 10-person HVAC firm, Nashville, December 2025).

---

## The Pipeline (Sequential — 6 Steps)

```
CALL COMES IN
     ↓
[1] RETELL AI — Voice agent answers, collects info
     ↓
[2] STRUCTURE EXTRACTION — Convert voice to structured data
     ↓
[3] AVAILABILITY CHECK — Query Dave's calendar
     ↓
[4] BOOKING — Write appointment to calendar
     ↓
[5] CONFIRMATION — SMS to customer + notification to Dave
     ↓
[6] HUMAN-ON-LOOP — Exception escalation only
```

---

## Step-by-Step Detail

### Step 1: Retell AI Voice Agent
**What it does:** Answers the call. Introduces itself as Dave's assistant. Collects:
- Customer name
- Phone number (already have it from caller ID, confirm it)
- Job type (emergency / routine / quote)
- Rough description of the problem
- Preferred appointment time (morning / afternoon / specific day)

**Script anchor (from ServiceTitan research — Gulfshore Air Conditioning):**
> "Hi, you've reached Jesmond Plumbing. I'm the booking assistant. I can get you booked in straight away — what's the issue today?"

**Escalation trigger:** If customer says "emergency," "flooding," "burst pipe," "no water" → immediately text Dave. Don't book. Human takes over.

**Platform:** Retell AI (already selected — VAPI-VS-RETELL-DEEP-RESEARCH-2026.md confirms this choice)

---

### Step 2: Structure Extraction
**What it does:** Converts the voice conversation to structured JSON.

```json
{
  "customer_name": "string",
  "phone": "string",
  "job_type": "emergency | routine | quote",
  "description": "string (max 200 chars)",
  "preferred_time": "morning | afternoon | specific_date",
  "urgency_flag": boolean
}
```

**How:** Retell webhook fires to a simple Python endpoint. Claude Haiku (cheapest, fastest) extracts structure from transcript. One LLM call. Sub-second.

---

### Step 3: Availability Check
**What it does:** Checks Dave's calendar for open slots matching preferred time.

**Platform:** Google Calendar API (Dave almost certainly uses Google Calendar or can be migrated to it in 10 minutes)

**Logic:**
- Pull next 7 days of calendar
- Find slots of 2 hours (standard job window)
- Match against preferred time (morning = 8am-12pm, afternoon = 1pm-5pm)
- Return first 2 available options

**No AI needed here.** Pure software. Calendar query + time matching.

---

### Step 4: Booking
**What it does:** Writes the appointment to Dave's calendar.

**Event format:**
```
Title: [Job Type] - [Customer Name]
Description: [customer description]
Phone: [customer phone]
Duration: 2 hours (default, Dave can adjust)
Location: TBC (Dave confirms address on the day)
```

**No AI needed here either.** Google Calendar API write. Software.

---

### Step 5: Confirmation
**What it does:** Sends two messages.

**To customer (SMS via Twilio):**
> "Booked! Dave from Jesmond Plumbing will be with you [DAY] between [TIME]. He'll call ahead. Any questions, reply to this message."

**To Dave (SMS or WhatsApp):**
> "New booking: [Customer] — [Job type] — [Day/Time]. Phone: [number]. Notes: [description]."

**No AI needed.** Template fill + Twilio API.

---

### Step 6: Human-on-Loop (Exceptions Only)
**What it does:** Escalates to Dave only when the workflow can't handle it.

**Escalation triggers:**
- Urgency flag = true (emergency job)
- No available slots in next 7 days
- Customer asks a question the agent can't answer
- Call drops before booking completes

**Escalation method:** SMS to Dave's phone. Immediate. Simple.

**Everything else:** Automated. Dave never sees it until his calendar notification fires the morning of the job.

---

## What Dave Gets

| Before | After |
|--------|-------|
| Misses calls while on a job | Every call answered, every time |
| Spends 10 min/call booking | 0 minutes per booking |
| Forgets to call back | Customer gets instant confirmation |
| No record of what was said | Full transcript + structured record |
| Loses jobs to competitors who answer | Books the job before they hang up |

**Target:** 15 hours/week saved (our guarantee threshold). Appointment booking alone won't hit 15 hours — this is workflow 1 of 3. But it's the one that proves the model.

---

## What This Costs to Run

Based on `ai-agent-cost-optimization-report-2026.md`:

| Component | Cost per call | Notes |
|-----------|--------------|-------|
| Retell AI | ~$0.05-0.10 | Per minute, calls avg 2-3 min |
| Claude Haiku (extraction) | ~$0.001 | One call, tiny context |
| Twilio SMS (×2) | ~$0.015 | UK rates |
| Google Calendar API | Free | Within quota |
| **Total per call** | **~$0.08-0.13** | |

**Dave's call volume estimate:** 20-40 calls/week (plumber, Jesmond area)  
**Monthly cost:** 160 calls × $0.13 = **~$21/month**  
**At £99/month:** ~£78 gross margin per customer before infrastructure overhead.

**This works at £99.** Comfortably.

---

## Build Sequence

**Week 1 (now → March 1):**
- [ ] Set up Retell AI account, configure voice agent script
- [ ] Build Python webhook endpoint (10 lines of code)
- [ ] Connect Google Calendar API
- [ ] Set up Twilio SMS account
- [ ] Test end-to-end with fake calls

**Week 2 (March 1-8):**
- [ ] Run with Dave in test mode (real calls, Dave manually confirms bookings)
- [ ] Tune escalation triggers based on real call patterns
- [ ] Dave confirms calendar format works for him

**Week 3 (March 8-15):**
- [ ] Go live. Human-on-loop active. Dave monitors.
- [ ] Measure: calls answered, bookings made, time saved
- [ ] First ROI data point

**End of March:** Dave is live. First client delivered. Case study begins.

---

## Infrastructure Decision (From Insight 3)

**Question Grok needs to answer:** Do we need hub-and-spoke + Redis + three-tier memory for THIS workflow?

**My read:** No. Not yet. This is a sequential pipeline with 6 steps and no agent coordination needed. Single orchestrator (Python script) calling APIs in sequence. Redis adds complexity without value at Dave's scale.

**When we add it:** Workflow 2 (meeting notes → CRM) introduces multi-agent coordination. That's when the infrastructure justifies itself.

**Decision:** Build Dave's workflow on minimal infrastructure. Migrate to Redis/hub-and-spoke when we have 3+ concurrent workflows running.

---

## Open Questions (Needs Ewan's Input)

1. **Does Dave currently use Google Calendar?** (Or iPhone calendar, or paper?) This determines booking integration.
2. **What number should the voice agent call from?** A new Jesmond Plumbing number? Or does Dave want calls forwarded from his existing number?
3. **What counts as an emergency for Dave?** (Burst pipe? No hot water? Or literally only flooding?)

These are 10-minute questions. Ask Dave. No assumptions.

---

## What Comes Next (Workflow 2)

Once voice booking is live and proven (2-3 weeks of data):

**Workflow 2: Job Completion → Invoice**
- Dave takes a photo of completed work
- Voice note: "Done the boiler service at Mrs Johnson's, took 2 hours, used £45 of parts"
- System generates invoice, emails to customer, updates records
- Dave never touches a spreadsheet

This is where 15 hours/week becomes believable.

---

*Spec written by Eli, February 22, 2026. Based on Sam's research session. Ready for Grok's infrastructure challenge and Sam's unit economics validation.*

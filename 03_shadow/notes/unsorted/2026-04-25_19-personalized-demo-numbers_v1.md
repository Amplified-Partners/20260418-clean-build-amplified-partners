---
title: "Personalized Demo Number System"
id: "19-personalized-demo-numbers"
version: 1
created: "2026-04-25"
type: "document"
topic_type: "unsorted"
audience: "internal"
layer: "shadow"
status: "filed"
signed_by: "Devon, 2026-04-25, devin-992682c244cf444f91e0a516498afbfd"
---

# Personalized Demo Number System
## Zero-Friction Lead Conversion via Instant Ownership Experience

---

## CONCEPT

Every cold lead gets their own unique phone number. When they call it, Gemma answers as if she's already their receptionist — using their business name. They don't watch a demo. They experience ownership.

---

## WHY THIS WINS

| Traditional Demo | Personalized Number |
|------------------|---------------------|
| Book a call | Instant access |
| Watch someone else's business | Experience YOUR business |
| Sales pitch | Self-discovery |
| "Imagine if..." | "This is yours" |
| 3-5 day sales cycle | 30-second "aha" moment |

**Psychology:** Once they hear "Good morning, [Their Business Name]" in Gemma's voice, they already feel ownership. The sale is 80% done.

---

## FLOW

```
Lead arrives (web form, ad, referral, cold outreach)
                    │
                    ▼
        ┌─────────────────────┐
        │  Capture:           │
        │  - Business name    │
        │  - Their name       │
        │  - Phone number     │
        │  - Vertical         │
        └──────────┬──────────┘
                   │
                   ▼
        ┌─────────────────────┐
        │  Trigger.dev Job:   │
        │  provision-demo-    │
        │  number             │
        └──────────┬──────────┘
                   │
                   ▼
        ┌─────────────────────┐
        │  1. Get Twilio      │
        │     number (local   │
        │     to their area)  │
        │                     │
        │  2. Create Vapi     │
        │     assistant with  │
        │     their business  │
        │     name baked in   │
        │                     │
        │  3. Link number     │
        │     to assistant    │
        └──────────┬──────────┘
                   │
                   ▼
        ┌─────────────────────┐
        │  Send SMS + Email:  │
        │                     │
        │  "Your AI recep-    │
        │  tionist is ready.  │
        │  Call her now:      │
        │  0191 XXX XXXX"     │
        └──────────┬──────────┘
                   │
                   ▼
           Lead calls number
                   │
                   ▼
        ┌─────────────────────┐
        │  Gemma answers:     │
        │                     │
        │  "Good morning,     │
        │  [Business Name],   │
        │  how can I help?"   │
        └──────────┬──────────┘
                   │
                   ▼
        Demo conversation plays out
        (emergency handling, booking, FAQ)
                   │
                   ▼
        ┌─────────────────────┐
        │  After call:        │
        │                     │
        │  SMS: "Like what    │
        │  you heard? Go live │
        │  in 10 minutes →    │
        │  [onboarding link]" │
        └──────────┬──────────┘
                   │
                   ▼
            Lead converts or
            enters nurture sequence
```

---

## GEMMA DEMO SCRIPT

**Greeting:**
> "Good morning, [Business Name], this is Gemma. How can I help you today?"

**If they say "I'm testing this" or "Is this the demo?":**
> "Yes! I'm showing you exactly how I'd answer calls for your business. Go ahead — pretend you're a customer calling in. Ask me anything."

**Demo scenarios to handle:**
- "I need an emergency appointment" → Shows emergency triage
- "Can I book for next week?" → Shows booking flow
- "What are your prices?" → Shows FAQ handling
- "Is [owner] available?" → Shows call screening

**Closing:**
> "That's how every call to [Business Name] would be handled. Your customers get a friendly voice 24/7, and you never miss a lead. Want me to send you a link to go live? It takes about 10 minutes to set up."

**If yes:** Capture email, trigger onboarding link

**If no/maybe:** 
> "No problem! This number stays active for the next few days if you want to test it more. I'll send you some info about what other [vertical] businesses are doing with this. Have a great day!"

---

## TECHNICAL IMPLEMENTATION

### Database Additions

```prisma
model DemoNumber {
  id                String   @id @default(uuid())
  
  // Lead info
  businessName      String   @map("business_name")
  contactName       String   @map("contact_name")
  contactPhone      String   @map("contact_phone")
  contactEmail      String?  @map("contact_email")
  vertical          Vertical
  
  // Twilio
  twilioNumber      String   @unique @map("twilio_number")
  twilioSid         String   @map("twilio_sid")
  
  // Vapi
  vapiAssistantId   String   @map("vapi_assistant_id")
  
  // Tracking
  status            DemoNumberStatus @default(active)
  callCount         Int      @default(0) @map("call_count")
  totalCallDuration Int      @default(0) @map("total_call_duration") // seconds
  firstCallAt       DateTime? @map("first_call_at")
  lastCallAt        DateTime? @map("last_call_at")
  convertedAt       DateTime? @map("converted_at")
  convertedToClientId String? @map("converted_to_client_id")
  
  // Lifecycle
  expiresAt         DateTime @map("expires_at") // 7 days from creation
  recycledAt        DateTime? @map("recycled_at")
  
  createdAt         DateTime @default(now()) @map("created_at")
  updatedAt         DateTime @updatedAt @map("updated_at")
  
  @@map("demo_numbers")
}

enum DemoNumberStatus {
  active
  converted
  expired
  recycled
}
```

### Trigger.dev Jobs

**1. provision-demo-number.ts**
```typescript
// Triggered when: New lead captured
// Does:
//   1. Purchase Twilio number (local to lead's area code if possible)
//   2. Create Vapi assistant with business name in greeting
//   3. Connect Twilio number to Vapi assistant
//   4. Store DemoNumber record
//   5. Send SMS + Email with the number
//   6. Schedule expiry check for 7 days
```

**2. handle-demo-call-complete.ts**
```typescript
// Triggered when: Vapi webhook fires for demo number call
// Does:
//   1. Update DemoNumber stats (callCount, duration, timestamps)
//   2. Log call transcript
//   3. If first call: trigger follow-up SMS after 5 mins
//   4. Analyze sentiment/intent from transcript
//   5. Update lead score
```

**3. demo-number-followup.ts**
```typescript
// Triggered: 5 minutes after first demo call
// Does:
//   1. Send SMS: "Like what you heard? Go live: [link]"
//   2. Send Email with full details
//   3. Start nurture sequence if no conversion in 24h
```

**4. recycle-expired-demo-numbers.ts**
```typescript
// Scheduled: Daily at 3am
// Does:
//   1. Find DemoNumbers where expiresAt < now AND status = active
//   2. Delete Vapi assistant
//   3. Release Twilio number back to pool (or keep for reuse)
//   4. Mark as recycled
```

### API Routes

```python
# src/api/routes/demo_numbers.py

POST   /api/v1/demo-numbers
       # Create demo number for new lead
       # Body: { businessName, contactName, contactPhone, contactEmail?, vertical }
       # Returns: { demoNumber, message }

GET    /api/v1/demo-numbers/{id}
       # Get demo number details + stats

GET    /api/v1/demo-numbers
       # List all active demo numbers

POST   /api/v1/demo-numbers/{id}/convert
       # Convert demo to full client
       # Transfers Twilio number + Vapi assistant to new Client record

DELETE /api/v1/demo-numbers/{id}
       # Manually expire/recycle a demo number
```

### Webhook Handler

```python
# In webhooks.py - handle Vapi calls to demo numbers

@router.post("/vapi/demo-call-complete")
async def handle_demo_call_complete(payload: dict):
    """
    Vapi webhook for demo number calls.
    Different from regular client calls - triggers demo-specific follow-up.
    """
    phone_number = payload.get("phoneNumber")
    
    # Find the demo number
    demo = await db.demonumber.find_first(
        where={"twilioNumber": phone_number}
    )
    
    if not demo:
        # Not a demo number, handle normally
        return
    
    # Update stats
    await db.demonumber.update(
        where={"id": demo.id},
        data={
            "callCount": {"increment": 1},
            "totalCallDuration": {"increment": payload.get("duration", 0)},
            "lastCallAt": datetime.utcnow(),
            "firstCallAt": demo.firstCallAt or datetime.utcnow(),
        }
    )
    
    # Trigger follow-up job
    await trigger.send_event(
        name="demo.call.completed",
        payload={"demoNumberId": demo.id, "callData": payload}
    )
```

---

## NUMBER STRATEGY

### Option A: Local Numbers (Recommended)
- Provision number matching lead's area code
- "0191 XXX XXXX" for Newcastle business
- Feels local, familiar, trustworthy
- Cost: ~£1/month per number via Twilio

### Option B: Single 0800 + Extensions
- One 0800 COVERED number
- Each lead gets extension: "Call 0800 268 3733, ext 1234"
- Lower cost but less magical
- Feels more "demo-y"

### Option C: Hybrid
- 0800 COVERED as the public demo line (generic)
- Local numbers for qualified/warm leads (personalized)

**Recommendation:** Option A (local numbers) for maximum impact. Numbers cost ~£1/month and can be recycled after 7 days.

---

## ECONOMICS

**Assumptions:**
- 500 leads/month
- 7-day number lifecycle
- 30% call their demo number
- 20% of callers convert

**Costs:**
- Twilio numbers: ~£1/month each
- Peak concurrent numbers: ~120 (500 × 7/30)
- Monthly number cost: ~£120
- Vapi minutes: 150 calls × 3 min = 450 min = ~£45
- **Total: ~£165/month**

**Revenue from conversions:**
- 500 leads × 30% call × 20% convert = 30 new customers
- 30 × £297/month = £8,910 MRR
- **ROI: 54x**

---

## MESSAGING TEMPLATES

### SMS 1: Number Ready
```
Your AI receptionist is ready to meet you.

Call her now: [DEMO_NUMBER]

She'll answer as "[BUSINESS_NAME]" — exactly like she would for your customers.

Go on, give her a ring.

— Ewan, Covered AI
```

### SMS 2: Post-Call Follow-up (5 min after first call)
```
What did you think?

That's how every call to [BUSINESS_NAME] gets handled — 24/7, never missed.

Ready to go live? Takes 10 minutes:
[ONBOARDING_LINK]

Questions? Reply here.
```

### Email: Number Ready
```
Subject: [BUSINESS_NAME]'s new receptionist is waiting

Hey [CONTACT_NAME],

Your AI receptionist is set up and ready to show you what she can do.

Give her a call: [DEMO_NUMBER]

She'll answer as "[BUSINESS_NAME]" — exactly like she would when your customers call.

Try asking her:
• "I need an emergency appointment"
• "Can I book for next week?"
• "What are your prices?"

This isn't a recording. She actually thinks on her feet.

Talk soon,
Ewan

P.S. The number's yours for 7 days. Call as many times as you like.
```

### Email: Post-Call Follow-up
```
Subject: Ready to never miss a call again?

Hey [CONTACT_NAME],

You just spoke to Gemma — your AI receptionist.

That's exactly how she'd answer every call to [BUSINESS_NAME]:
• Professional greeting with your business name
• Handles emergencies, bookings, and FAQs
• Captures every lead while you're busy

Ready to go live? It takes about 10 minutes:
[ONBOARDING_LINK]

Or reply to this email if you've got questions.

Ewan

P.S. Your demo number ([DEMO_NUMBER]) stays active for another [X] days if you want to test more.
```

---

## SUCCESS METRICS

| Metric | Target |
|--------|--------|
| Lead → Called demo number | 30%+ |
| Called → Converted | 20%+ |
| Time from lead to first call | < 1 hour |
| Demo calls per lead (avg) | 1.5+ |
| Number utilization (before recycle) | 40%+ |

---

## BUILD CHECKLIST

### Database
- [ ] Add DemoNumber model to schema
- [ ] Add DemoNumberStatus enum
- [ ] Run migration

### Backend
- [ ] Create src/api/routes/demo_numbers.py
- [ ] Add demo webhook handler to webhooks.py
- [ ] Register routes

### Trigger.dev Jobs
- [ ] provision-demo-number.ts
- [ ] handle-demo-call-complete.ts
- [ ] demo-number-followup.ts
- [ ] recycle-expired-demo-numbers.ts (daily cron)

### Vapi
- [ ] Create demo assistant template
- [ ] Dynamic greeting with business name variable
- [ ] Demo-specific conversation flow

### Integrations
- [ ] Twilio number provisioning
- [ ] SMS sending (number ready, follow-up)
- [ ] Email sending (number ready, follow-up)

### Tracking
- [ ] Call analytics per demo number
- [ ] Conversion tracking
- [ ] Funnel reporting

---

## CLAUDE CODE PROMPT

```
Build the Personalized Demo Number System.

Read: /specs/19-PERSONALIZED-DEMO-NUMBERS.md

Build in sequence:

1. Database
   - Add DemoNumber model
   - Add DemoNumberStatus enum
   - Run migration

2. API Routes
   - Create src/api/routes/demo_numbers.py
   - POST /demo-numbers (create)
   - GET /demo-numbers (list)
   - GET /demo-numbers/{id} (detail)
   - POST /demo-numbers/{id}/convert
   - DELETE /demo-numbers/{id}

3. Webhook Handler
   - Add demo call handler to webhooks.py
   - Differentiate demo calls from client calls

4. Trigger.dev Jobs
   - provision-demo-number.ts
   - handle-demo-call-complete.ts
   - demo-number-followup.ts
   - recycle-expired-demo-numbers.ts

5. Vapi Assistant
   - Create demo assistant template
   - Dynamic business name in greeting

6. SMS/Email Templates
   - Number ready (SMS + Email)
   - Post-call follow-up (SMS + Email)

Start now. Build everything.
```

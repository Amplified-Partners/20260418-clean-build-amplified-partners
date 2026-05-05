---
title: "BUILD: Personalized Demo Number System"
id: "build-demo-number-system"
version: 1
created: "2026-04-25"
type: "document"
topic_type: "unsorted"
audience: "internal"
layer: "shadow"
status: "filed"
signed_by: "Devon, 2026-04-25, devin-992682c244cf444f91e0a516498afbfd"
---

# BUILD: Personalized Demo Number System
## Zero-Friction Lead Conversion

---

## CONCEPT

Every cold lead gets their own unique phone number. When they call it, Gemma answers using THEIR business name. They don't watch a demo — they experience ownership.

**"Good morning, [Their Business Name], how can I help?"**

The sale is 80% done the moment they hear that.

---

## BUILD SEQUENCE

### Phase 1: Database

Add to schema.prisma:

```prisma
model DemoNumber {
  id                String   @id @default(uuid())
  businessName      String   @map("business_name")
  contactName       String   @map("contact_name")
  contactPhone      String   @map("contact_phone")
  contactEmail      String?  @map("contact_email")
  vertical          Vertical
  twilioNumber      String   @unique @map("twilio_number")
  twilioSid         String   @map("twilio_sid")
  vapiAssistantId   String   @map("vapi_assistant_id")
  status            DemoNumberStatus @default(active)
  callCount         Int      @default(0) @map("call_count")
  totalCallDuration Int      @default(0) @map("total_call_duration")
  firstCallAt       DateTime? @map("first_call_at")
  lastCallAt        DateTime? @map("last_call_at")
  convertedAt       DateTime? @map("converted_at")
  convertedToClientId String? @map("converted_to_client_id")
  expiresAt         DateTime @map("expires_at")
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

Run migration: `npx prisma migrate dev --name add-demo-numbers`

---

### Phase 2: API Routes

Create `src/api/routes/demo_numbers.py`:

```
POST   /api/v1/demo-numbers
       Body: { businessName, contactName, contactPhone, contactEmail?, vertical }
       → Triggers provision-demo-number job
       → Returns: { id, demoNumber, message }

GET    /api/v1/demo-numbers
       → List all active demo numbers

GET    /api/v1/demo-numbers/{id}
       → Get demo number details + call stats

POST   /api/v1/demo-numbers/{id}/convert
       → Convert to full Client
       → Transfer Twilio number + Vapi assistant

DELETE /api/v1/demo-numbers/{id}
       → Manually expire/recycle
```

---

### Phase 3: Trigger.dev Jobs

**provision-demo-number.ts**
1. Buy Twilio number (local to lead's area)
2. Create Vapi assistant with business name in greeting
3. Connect number to assistant
4. Save DemoNumber record
5. Send SMS + Email with number
6. Schedule expiry for 7 days

**handle-demo-call-complete.ts**
1. Update call stats (count, duration)
2. Log transcript
3. If first call → schedule 5-min follow-up
4. Update lead score

**demo-number-followup.ts**
1. Send SMS: "Like what you heard? Go live: [link]"
2. Send Email with details
3. Start nurture if no conversion in 24h

**recycle-expired-demo-numbers.ts** (daily cron)
1. Find expired + active numbers
2. Delete Vapi assistant
3. Release Twilio number
4. Mark as recycled

---

### Phase 4: Vapi Demo Assistant

Create assistant template with:
- Dynamic greeting: "Good morning, {{businessName}}, how can I help?"
- Demo-aware responses (if they say "is this the demo?")
- Same quality as production assistant
- Closing CTA: offer to send onboarding link

---

### Phase 5: Messaging

**SMS - Number Ready:**
```
Your AI receptionist is ready.

Call her now: {{demoNumber}}

She'll answer as "{{businessName}}" — exactly like she would for your customers.

— Ewan, Covered AI
```

**SMS - Post-Call (5 min after):**
```
What did you think?

Ready to go live? Takes 10 minutes:
{{onboardingLink}}
```

---

## ECONOMICS

- 500 leads/month
- 30% call their number
- 20% of callers convert
- **30 new customers/month**
- **Cost: ~£165/month**
- **Revenue: £8,910 MRR**
- **ROI: 54x**

---

## FULL SPEC

Read: `/specs/19-PERSONALIZED-DEMO-NUMBERS.md`

---

## START

```
1. Add DemoNumber model to prisma/schema.prisma
2. Run migration
3. Create src/api/routes/demo_numbers.py
4. Create trigger-jobs/provision-demo-number.ts
5. Create trigger-jobs/handle-demo-call-complete.ts
6. Create trigger-jobs/demo-number-followup.ts
7. Create trigger-jobs/recycle-expired-demo-numbers.ts
8. Create Vapi demo assistant template
9. Test end-to-end
```

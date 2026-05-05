---
title: "Nurture Sequence Spec — 12-Touch Copy & Logic"
id: "06-nurture-sequence"
version: 1
created: "2026-04-25"
type: "document"
topic_type: "unsorted"
audience: "internal"
layer: "shadow"
status: "filed"
signed_by: "Devon, 2026-04-25, devin-992682c244cf444f91e0a516498afbfd"
---

# Nurture Sequence Spec — 12-Touch Copy & Logic

## Principles Applied

| Principle | Application |
|-----------|-------------|
| Variable Reward | Each message offers different value type |
| Cognitive Load | Short, scannable, single CTA per message |
| Peak-End | Strong opening (Touch 1), strong close (Touch 12) |
| Social Proof | Touch 4 (testimonials), Touch 7 (case study) |
| Scarcity | Touch 8 (limited offer) |
| Personalization | Touch 5 (HeyGen video) |

---

## Sequence Overview

| Touch | Delay | Channel | Template | Purpose |
|-------|-------|---------|----------|---------|
| 1 | Instant | Email | acknowledgment | Confirm receipt |
| 2 | +5 min | WhatsApp | pain-question | Engage, qualify |
| 3 | +2 hours | SMS | quick-tip | Immediate value |
| 4 | +24 hours | Email | social-proof | Build trust |
| 5 | +48 hours | Email | video-intro | Personal connection |
| 6 | +72 hours | WhatsApp | urgency | Push to action |
| 7 | +5 days | Email | case-study | Detailed proof |
| 8 | +7 days | SMS | limited-offer | Scarcity |
| 9 | +10 days | Email | faq | Overcome objections |
| 10 | +14 days | WhatsApp | final-push | Last chance |
| 11 | +21 days | Email | long-nurture | Stay top-of-mind |
| 12 | +30 days | Email | re-engage | Final attempt |

---

## Touch 1: Instant Email — Acknowledgment

**Channel:** Email  
**Delay:** Instant (0 seconds)  
**Purpose:** Confirm receipt, set expectations

### Subject Line
```
Got it, {{customer_name}} 👍
```

### Body
```html
Hi {{customer_name}},

Thanks for calling {{business_name}}.

We've got your details:

<div class="summary-box">
  <strong>Job:</strong> {{job_type}}<br>
  <strong>Location:</strong> {{postcode}}<br>
  <strong>Urgency:</strong> {{urgency}}
</div>

{{#if urgency == "emergency"}}
<p class="urgent">
  This sounds urgent. {{owner_name}} will call you within 
  <strong>15 minutes</strong>.
</p>
{{else}}
<p>
  {{owner_name}} will be in touch within <strong>2 hours</strong> 
  during business hours.
</p>
{{/if}}

If you need us sooner, call back anytime — we're here 24/7.

<p class="signature">
  {{business_name}}<br>
  {{phone}}
</p>
```

### Template Variables
```typescript
interface Touch1Data {
  customer_name: string;
  business_name: string;
  owner_name: string;
  job_type: string;
  postcode: string;
  urgency: 'emergency' | 'urgent' | 'routine';
  phone: string;
}
```

---

## Touch 2: +5 min WhatsApp — Pain Question

**Channel:** WhatsApp  
**Delay:** 5 minutes  
**Purpose:** Engage, understand urgency, qualify

### Message
```
Hi {{customer_name}}, it's {{business_name}} 👋

Just checking — how urgent is this {{job_type}} situation for you?

Reply:
1️⃣ - Need it fixed today (I've got you)
2️⃣ - This week is fine
3️⃣ - Just getting quotes

This helps us prioritise your call.
```

### Response Handling
```typescript
const URGENCY_RESPONSES = {
  '1': { urgency: 'emergency', action: 'priority_callback' },
  '2': { urgency: 'urgent', action: 'schedule_callback' },
  '3': { urgency: 'routine', action: 'continue_nurture' }
};

// Update lead urgency based on response
// Trigger appropriate follow-up action
```

---

## Touch 3: +2 hours SMS — Quick Tip

**Channel:** SMS  
**Delay:** 2 hours  
**Purpose:** Provide immediate value, show expertise

### Messages by Job Type

**Burst Pipe:**
```
{{customer_name}} — quick tip from {{business_name}}: 

If water's still running, your stopcock is usually under the kitchen sink. Turn clockwise to shut off.

We'll call soon. Hang tight.
```

**No Power:**
```
{{customer_name}} — quick tip from {{business_name}}: 

Check your fuse box first — sometimes it's just a tripped switch. Usually in the hallway cupboard.

We'll call soon.
```

**Blocked Drain:**
```
{{customer_name}} — quick tip from {{business_name}}: 

Avoid pouring boiling water — can damage pipes. We'll sort it properly.

We'll call soon.
```

**Boiler Issue:**
```
{{customer_name}} — quick tip from {{business_name}}: 

Check the pressure gauge (usually on the front). If below 1 bar, you may need to repressurise. We can talk you through it.

Calling you shortly.
```

**Default:**
```
{{customer_name}} — {{business_name}} here.

Just wanted to let you know we've got your enquiry and we'll be in touch soon.

Hang tight!
```

### Template Selection Logic
```typescript
function selectTipTemplate(jobType: string): string {
  const templates: Record<string, string> = {
    'burst_pipe': 'tip_burst_pipe',
    'leak': 'tip_burst_pipe',
    'no_power': 'tip_no_power',
    'electrical': 'tip_no_power',
    'blocked_drain': 'tip_blocked_drain',
    'drain': 'tip_blocked_drain',
    'boiler': 'tip_boiler',
    'heating': 'tip_boiler'
  };
  
  const normalised = jobType.toLowerCase().replace(/[^a-z]/g, '_');
  return templates[normalised] || 'tip_default';
}
```

---

## Touch 4: +24 hours Email — Social Proof

**Channel:** Email  
**Delay:** 24 hours  
**Purpose:** Build trust with testimonials

### Subject Line
```
Why 47 local businesses trust us
```

### Body
```html
Hi {{customer_name}},

Still thinking about your {{job_type}}?

Here's what our customers say:

<div class="testimonial">
  <div class="stars">⭐⭐⭐⭐⭐</div>
  <p>"Called at 11pm with a burst pipe. Fixed by midnight. 
     Absolute lifesaver."</p>
  <cite>— Sarah, Jesmond</cite>
</div>

<div class="testimonial">
  <div class="stars">⭐⭐⭐⭐⭐</div>
  <p>"Fair price, no nonsense, did exactly what he said 
     he'd do."</p>
  <cite>— Mark, Gosforth</cite>
</div>

<div class="testimonial">
  <div class="stars">⭐⭐⭐⭐⭐</div>
  <p>"Best plumber in Newcastle. Won't use anyone else now."</p>
  <cite>— Janet, Heaton</cite>
</div>

We'd love to add you to that list.

<strong>Ready to book?</strong> Just reply to this email or 
call us back.

<p class="signature">
  {{business_name}}<br>
  {{phone}}
</p>
```

---

## Touch 5: +48 hours Email — Personalised Video

**Channel:** Email  
**Delay:** 48 hours  
**Purpose:** Personal connection, differentiation

### Subject Line
```
{{customer_name}}, I recorded this for you 🎥
```

### Body
```html
Hi {{customer_name}},

I made a quick video just for you:

<a href="{{video_url}}" class="video-thumbnail">
  <img src="{{thumbnail_url}}" alt="Click to play" />
  <div class="play-button">▶</div>
</a>

It's 45 seconds. I explain how we'd handle your {{job_type}} 
and what to expect.

Give it a watch when you have a moment.

<strong>Ready to get this sorted?</strong> Reply or call anytime.

<p class="signature">
  {{owner_name}}<br>
  {{business_name}}
</p>
```

### Video Generation

```typescript
interface VideoRequest {
  lead_id: string;
  customer_name: string;
  business_name: string;
  owner_name: string;
  job_type: string;
  vertical: string;
}

// HeyGen API call
async function generateVideo(request: VideoRequest): Promise<VideoResult> {
  const script = generateScript(request);
  
  const response = await heygen.createVideo({
    template_id: getTemplateForVertical(request.vertical),
    variables: {
      customer_name: request.customer_name,
      job_type: request.job_type,
      business_name: request.business_name
    },
    script: script
  });
  
  return {
    video_url: response.video_url,
    thumbnail_url: response.thumbnail_url
  };
}
```

### Video Scripts by Vertical

**Trades:**
```
Hi {{customer_name}}! Thanks for reaching out to {{business_name}}. 

We know how frustrating it can be when something breaks down at home. 
That's why we're here to help — 24/7, whenever you need us.

Our team is ready to get your issue sorted quickly and professionally.

Looking forward to helping you out!
```

**Vet:**
```
Hello {{customer_name}}! Thank you for contacting {{business_name}}.

We understand how important your pet's health is to you.
Our team of caring professionals is here to provide the best possible care.

We'll be in touch soon to discuss how we can help your furry family member.
```

**Dental:**
```
Hi {{customer_name}}! Thanks for getting in touch with {{business_name}}.

We know visiting the dentist can sometimes feel daunting, but we're here 
to make it as comfortable as possible.

Our friendly team is dedicated to giving you the best care in a relaxed environment.

We look forward to seeing you soon!
```

**Aesthetics:**
```
Hello {{customer_name}}! Thank you for your enquiry to {{business_name}}.

We're passionate about helping you look and feel your absolute best.
Our expert team will work with you to achieve natural, beautiful results.

Can't wait to welcome you for your consultation!
```

---

## Touch 6: +72 hours WhatsApp — Urgency

**Channel:** WhatsApp  
**Delay:** 72 hours  
**Purpose:** Create urgency, push to action

### Message
```
Hi {{customer_name}} 👋

Just checking in on your {{job_type}}.

We've got availability this week if you want to get it sorted.

Want me to pencil you in? Just reply with a day that works.

{{owner_name}}, {{business_name}}
```

---

## Touch 7: +5 days Email — Case Study

**Channel:** Email  
**Delay:** 5 days  
**Purpose:** Detailed proof, overcome skepticism

### Subject Line
```
How we saved Janet £800 (similar job to yours)
```

### Body
```html
Hi {{customer_name}},

Quick story for you:

Janet in {{area}} had a similar {{job_type}} issue. 
She'd already had two quotes from other companies.

<div class="case-study-box">
  <h3>What happened:</h3>
  <ul>
    <li>✓ We diagnosed the real problem (others missed it)</li>
    <li>✓ Fixed it same day</li>
    <li>✓ Cost her £200 less than the cheapest quote</li>
  </ul>
</div>

<blockquote>
  "Wish I'd called you first."
  <cite>— Janet, {{area}}</cite>
</blockquote>

We're still here when you're ready.

<p class="signature">
  {{business_name}}<br>
  {{phone}}
</p>
```

---

## Touch 8: +7 days SMS — Limited Offer

**Channel:** SMS  
**Delay:** 7 days  
**Purpose:** Scarcity, incentive to act

### Message
```
{{customer_name}} — {{business_name}} here.

Got a slot free Thursday afternoon. 

If you book your {{job_type}} this week, I'll knock 10% off the final bill.

Interested? Reply YES and I'll call you.
```

### Response Handling
```typescript
const OFFER_RESPONSES = {
  'YES': { action: 'schedule_callback', priority: 'high' },
  'NO': { action: 'continue_nurture' },
  // Any other response: treat as question, route to owner
};
```

---

## Touch 9: +10 days Email — FAQ

**Channel:** Email  
**Delay:** 10 days  
**Purpose:** Overcome objections, answer concerns

### Subject Line
```
Quick answers to common questions
```

### Body
```html
Hi {{customer_name}},

Still mulling it over? Totally fine. Here are answers 
to questions we get a lot:

<div class="faq">
  <div class="faq-item">
    <h4>Q: How much will it cost?</h4>
    <p>A: We quote before we start. No surprises, no hidden fees.</p>
  </div>
  
  <div class="faq-item">
    <h4>Q: How quickly can you come?</h4>
    <p>A: Usually same-day for emergencies, 1-3 days for routine jobs.</p>
  </div>
  
  <div class="faq-item">
    <h4>Q: Are you insured?</h4>
    <p>A: Fully insured and {{certifications}}.</p>
  </div>
  
  <div class="faq-item">
    <h4>Q: What if it's not what you quoted?</h4>
    <p>A: We'll explain the issue, get your approval, then proceed. 
       You're always in control.</p>
  </div>
</div>

Any other questions? Just reply.

<p class="signature">
  {{business_name}}
</p>
```

### Certification Variables by Vertical
```typescript
const CERTIFICATIONS: Record<string, string> = {
  trades: 'Gas Safe registered (where applicable)',
  electrical: 'NICEIC approved',
  vet: 'RCVS registered',
  dental: 'GDC registered',
  aesthetics: 'fully insured with Save Face accreditation'
};
```

---

## Touch 10: +14 days WhatsApp — Final Push

**Channel:** WhatsApp  
**Delay:** 14 days  
**Purpose:** Last direct push before long nurture

### Message
```
{{customer_name}} — honest question:

Is the {{job_type}} sorted, or still on your to-do list?

If it's done, great — ignore me! 

If not, I've got time this week. Just say the word.

{{owner_name}}
```

---

## Touch 11: +21 days Email — Long Nurture

**Channel:** Email  
**Delay:** 21 days  
**Purpose:** Stay top-of-mind without being pushy

### Subject Line
```
Still here if you need us
```

### Body
```html
Hi {{customer_name}},

No pressure — just a quick note to say we're still here 
when you're ready.

{{job_type}} issues don't usually fix themselves, 
but I get it — life gets busy.

Whenever you're ready, just reply or call. We'll sort it.

<p class="signature">
  {{business_name}}<br>
  {{phone}}
</p>
```

---

## Touch 12: +30 days Email — Re-engage

**Channel:** Email  
**Delay:** 30 days  
**Purpose:** Final attempt, graceful close

### Subject Line
```
One last check-in, {{customer_name}}
```

### Body
```html
Hi {{customer_name}},

It's been a month since you first got in touch about 
your {{job_type}}.

Three possibilities:

<ol>
  <li><strong>You got it fixed elsewhere</strong> — no worries, 
      hope it went well!</li>
  <li><strong>You're still thinking</strong> — we're here 
      when you're ready</li>
  <li><strong>Life got in the way</strong> — totally understand</li>
</ol>

If you ever need {{services}}, you've got our number.

Thanks for considering us.

<p class="signature">
  {{owner_name}}<br>
  {{business_name}}
</p>

<p class="unsubscribe">
  P.S. If you reply "STOP" we won't email again. No hard feelings.
</p>
```

---

## Sequence Control Logic

### Stop Conditions

```typescript
const STOP_CONDITIONS = [
  'lead_booked',      // Lead converted to job
  'lead_dismissed',   // Owner dismissed lead
  'customer_replied_stop', // Customer opted out
  'customer_unsubscribed', // Email unsubscribe
  'customer_booked_elsewhere' // Indicated went elsewhere
];

async function checkStopConditions(leadId: string): Promise<boolean> {
  const lead = await getLead(leadId);
  return STOP_CONDITIONS.includes(lead.status);
}
```

### Pause Conditions

```typescript
const PAUSE_CONDITIONS = [
  'customer_requested_callback', // Active conversation
  'owner_contacted_customer',    // Manual intervention
  'pending_quote'                // Quote sent, awaiting response
];

// Resume after 48 hours if no activity
```

### Skip Conditions

```typescript
// Skip SMS touches if no valid mobile
// Skip WhatsApp if not registered
// Skip video if HeyGen quota exceeded

async function canSendToChannel(
  leadId: string, 
  channel: Channel
): Promise<boolean> {
  const lead = await getLead(leadId);
  
  switch (channel) {
    case 'sms':
      return isValidMobile(lead.phone);
    case 'whatsapp':
      return await isWhatsAppRegistered(lead.phone);
    case 'email':
      return isValidEmail(lead.email);
    default:
      return true;
  }
}
```

---

## Database Schema Addition

```prisma
model NurtureTouch {
  id              String   @id @default(uuid())
  nurtureSequenceId String @map("nurture_sequence_id")
  touchNumber     Int      @map("touch_number")
  channel         String   // email, sms, whatsapp
  template        String
  
  scheduledAt     DateTime @map("scheduled_at")
  sentAt          DateTime? @map("sent_at")
  deliveredAt     DateTime? @map("delivered_at")
  openedAt        DateTime? @map("opened_at")
  clickedAt       DateTime? @map("clicked_at")
  repliedAt       DateTime? @map("replied_at")
  
  status          String   // pending, sent, delivered, failed, skipped
  error           String?
  
  // External IDs
  messageId       String?  @map("message_id") // Resend/Twilio ID
  
  createdAt       DateTime @default(now()) @map("created_at")
  
  nurtureSequence NurtureSequence @relation(fields: [nurtureSequenceId], references: [id])
  
  @@index([nurtureSequenceId])
  @@index([scheduledAt])
  @@map("nurture_touches")
}
```

---

## Trigger.dev Job Update

```typescript
// trigger-jobs/lead-nurture.ts

const TOUCH_CONFIG = [
  { num: 1, delay: 0, channel: 'email', template: 'acknowledgment' },
  { num: 2, delay: 5 * 60, channel: 'whatsapp', template: 'pain-question' },
  { num: 3, delay: 2 * 60 * 60, channel: 'sms', template: 'quick-tip' },
  { num: 4, delay: 24 * 60 * 60, channel: 'email', template: 'social-proof' },
  { num: 5, delay: 48 * 60 * 60, channel: 'email', template: 'video-intro' },
  { num: 6, delay: 72 * 60 * 60, channel: 'whatsapp', template: 'urgency' },
  { num: 7, delay: 5 * 24 * 60 * 60, channel: 'email', template: 'case-study' },
  { num: 8, delay: 7 * 24 * 60 * 60, channel: 'sms', template: 'limited-offer' },
  { num: 9, delay: 10 * 24 * 60 * 60, channel: 'email', template: 'faq' },
  { num: 10, delay: 14 * 24 * 60 * 60, channel: 'whatsapp', template: 'final-push' },
  { num: 11, delay: 21 * 24 * 60 * 60, channel: 'email', template: 'long-nurture' },
  { num: 12, delay: 30 * 24 * 60 * 60, channel: 'email', template: 're-engage' },
];
```

---
title: "Three-Tier Migration System"
id: "migration_system"
version: 1
created: "2026-04-25"
type: "document"
topic_type: "unsorted"
audience: "internal"
layer: "shadow"
status: "filed"
signed_by: "Devon, 2026-04-25, devin-992682c244cf444f91e0a516498afbfd"
---

# Three-Tier Migration System

## Overview

Covered AI offers three ways for customers to connect their phone to Gemma:

| Tier | Method | Time | Effort |
|------|--------|------|--------|
| **1** | Call Forwarding | 5 minutes | Customer dials a code |
| **2** | Number Porting | 5-10 days | Customer signs one form |
| **3** | Email Nurture | Ongoing | Automated sequences |

---

## Tier 1: Call Forwarding (Quick Start)

**Customer Action:** Dial a forwarding code on their phone

**Common UK Carrier Codes:**
- BT Landline: `*21*[number]#`
- EE/Vodafone/O2/Three: `*21*[number]#` or via Settings → Call Forwarding
- VoIP systems: Configure in admin portal

**Frontend:** `/onboarding/step-2` - Network selector + dial code generator

**Backend:** `GET /api/v1/onboarding/step2/instructions?network={network}`

**Pros:**
- Live in 5 minutes
- Customer keeps their number
- Easy to cancel

**Cons:**
- Customer must set up forwarding
- Relies on customer's network

---

## Tier 2: Number Porting (White-Glove)

**Customer Action:** Fill in one form, sign LOA

**Process:**
1. Customer provides: phone number, provider, account number, billing postcode
2. System generates Twilio-compliant LOA PDF
3. We submit port request to carrier
4. Temporary forwarding set up during transition
5. Port completes in 5-10 business days
6. Customer receives completion email

**Frontend:**
- `/onboarding/step-2` - Option to "Transfer my number"
- `/onboarding/porting` - 3-step porting form

**Backend:**
- `POST /api/v1/porting/request` - Submit porting request
- `GET /api/v1/porting/status/{id}` - Check status
- `GET /api/v1/porting/loa/{id}` - Download LOA PDF
- `POST /api/v1/porting/submit/{id}` - Submit to carrier (admin)
- `POST /api/v1/porting/complete/{id}` - Mark complete (admin)

**Services:**
- `src/services/porting_service.py` - Porting workflow management
- `src/services/loa_generator.py` - PDF generation
- `src/services/porting_emails.py` - Email notifications

**Email Templates:**
- Confirmation email (on submission)
- Status update emails (in progress)
- Completion email (port complete)

---

## Tier 3: Email Nurture Sequences

**For:** Leads who aren't ready to sign up yet

**Sequences:**
1. **Demo Followup** - After a demo call (4 emails over 10 days)
2. **Cold Intro** - Cold outreach (4 emails over 14 days)
3. **Reengagement** - Re-engage dormant leads (3 emails over 21 days)

**Backend:**
- `POST /api/v1/nurture/add` - Add lead to sequence
- `GET /api/v1/nurture/leads` - List all leads
- `POST /api/v1/nurture/leads/{id}/stop` - Stop sequence
- `GET /api/v1/nurture/sequences` - List available sequences
- `POST /api/v1/nurture/preview` - Preview email template
- `POST /api/v1/nurture/send` - Send single email

**Services:**
- `src/services/nurture_sequences.py` - Sequence management + templates

**Templates:**
- `demo_thanks` - Thanks for the demo
- `demo_value_reminder` - Missed calls = missed money
- `demo_social_proof` - Ralph's story
- `demo_last_chance` - Final check-in
- `cold_intro` - Initial outreach
- `cold_pain_point` - What happens to missed calls?
- `cold_social_proof` - 12 emergency jobs in 3 weeks
- `cold_final` - Last email
- `reengage_check_in` - Been a while
- `reengage_new_feature` - New feature announcement
- `reengage_last_try` - Final attempt

---

## File Structure

```
src/
├── api/
│   └── routes/
│       ├── porting.py        # Porting API endpoints
│       └── nurture.py        # Nurture sequence endpoints
├── services/
│   ├── loa_generator.py      # LOA PDF generation
│   ├── porting_service.py    # Porting workflow
│   ├── porting_emails.py     # Porting email templates
│   └── nurture_sequences.py  # Nurture sequences + templates

frontend/
└── src/
    └── app/
        └── (onboarding)/
            ├── step-2/
            │   └── page.tsx  # Updated with tier selection
            └── porting/
                └── page.tsx  # Porting form
```

---

## API Types (TypeScript)

```typescript
// Porting
interface PortingResponse {
  id: string;
  status: string;
  number_to_port: string;
  current_provider: string;
  submitted_at: string;
  estimated_completion: string;
  message: string;
}

// Nurture
interface NurtureAddResponse {
  lead_id: string;
  email: string;
  sequence_type: string;
  schedule: { template: string; day: number; send_date: string }[];
  message: string;
}
```

---

## Next Steps

1. **Database persistence** - Replace in-memory storage with Prisma models
2. **Twilio Porting API** - Integrate actual port submission
3. **Scheduled email sender** - Cron job for nurture sequence emails
4. **Admin dashboard** - View/manage porting requests and nurture leads
5. **Webhooks** - Receive Twilio porting status updates

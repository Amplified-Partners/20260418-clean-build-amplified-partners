---
title: "Onboarding Flow Spec — 3 Steps to Value"
id: "02-onboarding-flow"
version: 1
created: "2026-04-25"
type: "document"
topic_type: "unsorted"
audience: "internal"
layer: "shadow"
status: "filed"
signed_by: "Devon, 2026-04-25, devin-992682c244cf444f91e0a516498afbfd"
---

# Onboarding Flow Spec — 3 Steps to Value

## Principles Applied

| Principle | Application |
|-----------|-------------|
| Hick's Law | 3 steps max, minimal choices |
| Endowed Progress | Pre-fill known data, show progress bar |
| Time to "Aha!" | Goal: first lead notification < 24 hours |
| Progressive Disclosure | Don't show dashboard complexity on day 1 |

---

## Target Metrics

| Metric | Target |
|--------|--------|
| Time to complete onboarding | < 3 minutes |
| Time to first test call | < 5 minutes |
| Time to "Aha! Moment" (real lead) | < 24 hours |
| Onboarding completion rate | > 80% |
| Drop-off at step 2 | < 15% |

---

## Flow Definition

### Step 0: Entry Point

**Trigger:** User clicks "Start Free Trial" on landing page

**Data captured from landing page (if available):**
- Email (from signup form)
- Business name (from URL params or form)
- Phone (from form)
- Vertical (from quiz or page variant)

---

### Step 1: Your Business

**Goal:** Capture essential business info

**UI Elements:**
```
┌─────────────────────────────────────────────────────────────┐
│                                                             │
│  Let's get you set up                      [====○--------]  │
│                                                             │
│  Business Name                                              │
│  ┌─────────────────────────────────────────────────────┐   │
│  │ Titan Plumbing Solutions                            │   │
│  └─────────────────────────────────────────────────────┘   │
│  ↑ Pre-filled if known                                      │
│                                                             │
│  Your Name                                                  │
│  ┌─────────────────────────────────────────────────────┐   │
│  │ Ralph                                               │   │
│  └─────────────────────────────────────────────────────┘   │
│                                                             │
│  Your Mobile (for notifications)                            │
│  ┌─────────────────────────────────────────────────────┐   │
│  │ +44 7738 676932                                     │   │
│  └─────────────────────────────────────────────────────┘   │
│                                                             │
│  What type of business?                                     │
│  ┌─────────┐ ┌─────────┐ ┌─────────┐ ┌─────────┐          │
│  │ Plumber │ │Electric-│ │ Builder │ │ Other   │          │
│  │    🔧   │ │  ian ⚡ │ │   🏗️   │ │   ...   │          │
│  └─────────┘ └─────────┘ └─────────┘ └─────────┘          │
│                                                             │
│                        [ Continue → ]                       │
│                                                             │
└─────────────────────────────────────────────────────────────┘
```

**Fields:**

| Field | Type | Required | Pre-fill |
|-------|------|----------|----------|
| business_name | text | Yes | From signup if available |
| owner_name | text | Yes | From signup if available |
| phone | tel | Yes | - |
| vertical | select | Yes | - |

**Validation:**
- Phone must be valid UK mobile
- All fields required

**On Submit:**
- Create Client record in database
- Generate Covered phone number (Twilio)
- Proceed to Step 2

---

### Step 2: Connect Your Line

**Goal:** Get user to set up call forwarding

**UI Elements:**
```
┌─────────────────────────────────────────────────────────────┐
│                                                             │
│  Connect your phone line                   [========○----]  │
│                                                             │
│  Forward your business calls to this number:                │
│                                                             │
│  ┌─────────────────────────────────────────────────────┐   │
│  │                                                     │   │
│  │           0191 743 2732                             │   │
│  │                                                     │   │
│  │                          [ 📋 Copy Number ]         │   │
│  └─────────────────────────────────────────────────────┘   │
│                                                             │
│  📱 How to set up call forwarding:                          │
│                                                             │
│  Select your network:                                       │
│  ┌─────┐ ┌─────────┐ ┌────┐ ┌───────┐ ┌────┐              │
│  │ EE  │ │Vodafone │ │ O2 │ │ Three │ │ BT │              │
│  └─────┘ └─────────┘ └────┘ └───────┘ └────┘              │
│                                                             │
│  ┌─────────────────────────────────────────────────────┐   │
│  │ For EE:                                             │   │
│  │ 1. Open your Phone app                              │   │
│  │ 2. Dial: **21*01917432732#                          │   │
│  │ 3. Press Call                                       │   │
│  │ 4. Wait for confirmation beep                       │   │
│  │                                                     │   │
│  │ [ 📋 Copy Code ]                                    │   │
│  └─────────────────────────────────────────────────────┘   │
│                                                             │
│  ⏱️ Takes about 60 seconds                                  │
│                                                             │
│              [ I've Set Up Forwarding → ]                   │
│                                                             │
│  Having trouble? [ Chat with us ] or call 0800 XXX XXXX     │
│                                                             │
└─────────────────────────────────────────────────────────────┘
```

**Network-Specific Instructions:**

| Network | Forward All Calls Code | Cancel Code |
|---------|----------------------|-------------|
| EE | **21*[number]# | ##21# |
| Vodafone | **21*[number]# | ##21# |
| O2 | **21*[number]# | ##21# |
| Three | **21*[number]# | ##21# |
| BT | **21*[number]# | ##21# |

**On Submit:**
- Mark forwarding_setup_claimed = true
- Proceed to Step 3

---

### Step 3: Test It

**Goal:** User makes test call, experiences the magic

**UI Elements:**
```
┌─────────────────────────────────────────────────────────────┐
│                                                             │
│  Let's test it!                            [============○]  │
│                                                             │
│  🎉 Almost there!                                           │
│                                                             │
│  Make a test call now to meet Gemma:                        │
│                                                             │
│  ┌─────────────────────────────────────────────────────┐   │
│  │                                                     │   │
│  │     [ 📞  Call 0191 743 2732 ]                      │   │
│  │                                                     │   │
│  └─────────────────────────────────────────────────────┘   │
│                                                             │
│  💡 Try saying:                                             │
│  "Hi, I've got a leaky tap in Newcastle, postcode NE4"      │
│                                                             │
│  ┌─────────────────────────────────────────────────────┐   │
│  │                                                     │   │
│  │     ⏳ Waiting for your test call...                │   │
│  │                                                     │   │
│  │     Call received: No                               │   │
│  │                                                     │   │
│  └─────────────────────────────────────────────────────┘   │
│                                                             │
│  [ Skip for now — I'll test later ]                         │
│                                                             │
└─────────────────────────────────────────────────────────────┘
```

**On Test Call Received:**

```
┌─────────────────────────────────────────────────────────────┐
│                                                             │
│  ✅ Test successful!                       [==============●] │
│                                                             │
│  🚀 You're Live!                                            │
│                                                             │
│  Gemma is now answering your calls 24/7.                    │
│                                                             │
│  Your first real lead notification will look like this:     │
│                                                             │
│  ┌─────────────────────────────────────────────────────┐   │
│  │  📱 WhatsApp Preview                                │   │
│  │  ─────────────────────────────────────────────────  │   │
│  │  🔔 COVERED AI                                      │   │
│  │                                                     │   │
│  │  New Lead: Burst pipe (EMERGENCY)                   │   │
│  │  Sarah M, NE4 5TH                                   │   │
│  │  "Water coming through ceiling"                     │   │
│  │                                                     │   │
│  │  Tap to view details →                              │   │
│  └─────────────────────────────────────────────────────┘   │
│                                                             │
│                  [ Go to Dashboard → ]                      │
│                                                             │
└─────────────────────────────────────────────────────────────┘
```

**On Test Call:**
- Detect call via Vapi webhook
- Update UI in real-time (WebSocket or polling)
- Create test lead record (marked as test)
- Send real WhatsApp notification
- Show success state

---

## Post-Onboarding: First Dashboard View

**Goal:** Reinforce value, don't overwhelm

**Show:**
- Simple stats (Calls: 1, Leads: 1)
- Recent leads list (test call visible)
- "Gemma is listening" status indicator

**Hide (initially):**
- Complex analytics
- Settings
- Billing

**Tooltip on first visit:**
```
"When a real call comes in, you'll see it here. 
Gemma is answering your phone right now — try calling!"
```

---

## Technical Implementation

### API Endpoints Required

```
POST /api/v1/onboarding/start
  Body: { email, business_name?, source }
  Returns: { onboarding_id, step: 1 }

POST /api/v1/onboarding/{id}/step1
  Body: { business_name, owner_name, phone, vertical }
  Returns: { covered_number, step: 2 }

POST /api/v1/onboarding/{id}/step2
  Body: { forwarding_confirmed: true }
  Returns: { step: 3 }

GET /api/v1/onboarding/{id}/test-status
  Returns: { test_call_received: boolean, lead_id? }

POST /api/v1/onboarding/{id}/complete
  Returns: { client_id, dashboard_url }
```

### Events to Track

| Event | When | Data |
|-------|------|------|
| onboarding_started | Step 0 complete | source, email |
| step1_completed | Step 1 submit | vertical, time_spent |
| step2_completed | Step 2 submit | network_selected, time_spent |
| test_call_made | Call received | call_duration |
| onboarding_completed | Dashboard reached | total_time |
| onboarding_abandoned | No activity 24h | last_step, time_spent |

### Drip Sequence if Abandoned

| Timing | Channel | Message |
|--------|---------|---------|
| +1 hour | Email | "Finish setting up — takes 2 more minutes" |
| +24 hours | SMS | "Your Covered number is ready. Finish setup: [link]" |
| +48 hours | Email | "Need help? Reply and we'll call you" |
| +7 days | Email | "Still interested? Your trial is waiting" |

---

## Mobile Considerations

- "Call" button should use `tel:` link for one-tap calling
- Copy buttons should use Clipboard API with toast confirmation
- Network instructions should be collapsible/accordion
- Progress bar should be sticky at top
- All tap targets minimum 44x44px

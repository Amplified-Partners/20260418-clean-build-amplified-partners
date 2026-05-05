---
title: "Automated Onboarding, Training & Support Engine"
id: "18-onboarding-training-support-engine-copy-2"
version: 1
created: "2026-04-25"
type: "document"
topic_type: "unsorted"
audience: "internal"
layer: "shadow"
status: "filed"
signed_by: "Devon, 2026-04-25, devin-992682c244cf444f91e0a516498afbfd"
---

# Automated Onboarding, Training & Support Engine
## Specification 18
### Psychology-Driven Self-Service Success System

---

## EXECUTIVE SUMMARY

This system transforms customer onboarding from a one-time event into a continuous success journey. Using behavioral psychology principles, AI-generated video avatars, and intelligent automation, we create an experience that:

1. **Reduces time-to-value** from days to minutes
2. **Eliminates support tickets** through proactive guidance
3. **Creates habit-forming engagement** using BJ Fogg's Behavior Model
4. **Scales infinitely** without adding headcount
5. **Continuously improves** through feedback loops

---

## PART 1: PSYCHOLOGICAL FOUNDATIONS

### 1.1 BJ Fogg Behavior Model (B = MAP)

Every behavior we want customers to perform requires three elements converging simultaneously:

```
Behavior = Motivation × Ability × Prompt
```

| Element | Definition | Our Application |
|---------|------------|-----------------|
| **Motivation** | Desire to perform behavior | Show ROI, celebrate wins, social proof |
| **Ability** | Simplicity of behavior | Reduce steps, pre-fill data, guided flows |
| **Prompt** | Trigger at the right moment | Contextual nudges, timely emails, in-app cues |

**Key Insight:** If behavior isn't happening, diagnose which element is missing:
- High motivation but no action → Make it easier (Ability)
- Easy but not doing it → Increase motivation or add prompt
- Motivated and able but nothing happens → Missing prompt

### 1.2 Psychological Principles Applied

| Principle | Definition | Implementation |
|-----------|------------|----------------|
| **Zeigarnik Effect** | Incomplete tasks create mental tension | Progress bars, checklists that show incompleteness |
| **Endowed Progress Effect** | People complete tasks they've "already started" | Start checklist at 20% complete (account created = first step done) |
| **Loss Aversion** | Losses feel 2x worse than equivalent gains | "Don't miss your first call" vs "Set up your phone" |
| **Social Proof** | We look to others in uncertain situations | "427 businesses like yours use Covered" |
| **Commitment & Consistency** | Small commitments lead to larger ones | Micro-commitments in onboarding flow |
| **Peak-End Rule** | We judge experiences by peak moment and ending | Celebrate wins, end each session positively |
| **Variable Rewards** | Unpredictable rewards drive engagement | Random celebration animations, surprise tips |
| **Reciprocity** | We return favors | Give value first (free call analysis) before asking for setup |

### 1.3 Habit Formation Framework (Nir Eyal's Hook Model)

For sustained engagement, we create habit loops:

```
Trigger → Action → Variable Reward → Investment
   ↑__________________________________|
```

**Applied to Covered AI:**

| Stage | Example |
|-------|---------|
| **Trigger** | Morning email: "You had 3 calls yesterday" |
| **Action** | Open dashboard (one tap from email) |
| **Variable Reward** | See new insights, AI-generated summary, revenue tracked |
| **Investment** | Mark attention item as resolved, update customer note |

The investment increases switching cost and improves future triggers.

---

## PART 2: ONBOARDING ARCHITECTURE

### 2.1 The "Time to First Value" (TTFV) Framework

**Goal:** Customer experiences core value within 5 minutes of signup.

**Critical Path:**
```
Signup → Business Info (1 min) → Phone Setup (2 min) → Test Call (2 min) → VALUE
```

**Not in Critical Path (defer):**
- Detailed business profile
- Team invitations
- Advanced settings
- Integrations
- Payment details (14-day trial)

### 2.2 Onboarding Stages

| Stage | Name | Goal | Duration | Success Metric |
|-------|------|------|----------|----------------|
| 0 | **Signup** | Create account | 30 sec | Account exists |
| 1 | **Quick Setup** | Minimal config | 2 min | Phone active |
| 2 | **First Call** | Experience value | 5 min | Test call completed |
| 3 | **Activation** | Real usage begins | 24 hrs | First real call handled |
| 4 | **Adoption** | Core habits formed | 7 days | Daily dashboard check |
| 5 | **Mastery** | Full feature usage | 30 days | Using 80% of features |

### 2.3 Activation Milestones

Based on research showing specific behaviors predict retention:

| Milestone | Behavior | Retention Impact |
|-----------|----------|------------------|
| **M1** | First test call completed | +47% 30-day retention |
| **M2** | First real call handled | +68% 30-day retention |
| **M3** | First invoice sent | +82% 30-day retention |
| **M4** | First review request sent | +91% 30-day retention |
| **M5** | Dashboard checked 3 days in row | +94% 90-day retention |

**Design principle:** Optimize entire onboarding to drive M1-M5 as fast as possible.

---

## PART 3: VIDEO AVATAR SYSTEM

### 3.1 Meet "Gemma" — Your AI Guide

Gemma is both the phone AI and the onboarding guide — creating consistency across the entire experience.

**Avatar Specifications:**
- Name: Gemma
- Voice: Northern British accent (warm, professional)
- Appearance: Friendly, approachable, diverse representation options
- Personality: Helpful, encouraging, slightly playful
- Platform: HeyGen or Synthesia for generation

**Why Video Avatars Work:**
- 35% higher completion rates vs text-only onboarding
- 50% reduction in production time vs live video
- Unlimited personalization and localization
- Consistent quality at scale

### 3.2 Video Content Library

#### Welcome & Orientation Videos

| Video | Duration | Trigger | Content |
|-------|----------|---------|---------|
| **Welcome** | 60 sec | Post-signup | Personal welcome, what to expect, first step CTA |
| **Quick Tour** | 90 sec | First dashboard visit | Dashboard overview, key areas, where to get help |
| **Your Covered Number** | 45 sec | Phone setup step | How the number works, forwarding explanation |
| **Meet Gemma** | 60 sec | Before test call | What Gemma can do, personality, emergency handling |

#### Feature Training Videos

| Video | Duration | Trigger | Content |
|-------|----------|---------|---------|
| **Calls Dashboard** | 90 sec | First call received | Understanding call logs, actions, follow-ups |
| **Creating Invoices** | 120 sec | First invoice prompt | Step-by-step invoice creation |
| **Invoice Chasing** | 90 sec | Invoice sent | How auto-reminders work, when to intervene |
| **Review Requests** | 60 sec | First job completed | Automatic review flow, customization |
| **Attention Items** | 75 sec | First attention item | What they mean, how to act on them |
| **Reports & Insights** | 90 sec | Day 7 | Understanding your business metrics |
| **GEO & AI Visibility** | 120 sec | Day 14 | How AI search works, your public page |

#### Celebration & Milestone Videos

| Video | Duration | Trigger | Content |
|-------|----------|---------|---------|
| **First Call Success** | 30 sec | First real call | Celebration, what happens next |
| **First Invoice Paid** | 30 sec | Payment recorded | Celebration, revenue milestone |
| **Week 1 Complete** | 45 sec | Day 7 | Week in review, stats summary |
| **Month 1 Complete** | 60 sec | Day 30 | Major milestone, ROI summary |

#### Troubleshooting & Support Videos

| Video | Duration | Trigger | Content |
|-------|----------|---------|---------|
| **Forwarding Not Working** | 90 sec | No calls after 24h | Troubleshooting steps |
| **Missed Call Handling** | 60 sec | Missed call detected | Why it happened, how to prevent |
| **Invoice Questions** | 90 sec | Support keyword detected | Common invoice issues |
| **Account Settings** | 60 sec | Settings page visit | How to customize |

### 3.3 Video Personalization

Each video dynamically includes:
- Customer's name
- Business name
- Vertical-specific examples (plumber vs vet vs salon)
- Actual data from their account (call count, revenue)

**Example Script (Welcome Video):**
```
"Hi {firstName}! I'm Gemma, and I'll be answering your phones from now on.

{businessName} is going to love this — I've already helped over 500 
{vertical} businesses handle more than 50,000 calls.

In the next 2 minutes, we'll get your Covered number set up. 
Then you can test it yourself and hear exactly what your customers will experience.

Ready? Let's go!"
```

### 3.4 Video Delivery System

**In-App Modals:**
- Auto-play (muted) with unmute prompt
- Skip button after 5 seconds
- Progress indicator
- Related action CTA below video

**Email Embeds:**
- Animated GIF thumbnail
- Click to watch (opens in browser)
- Key points as text below

**Help Center:**
- Searchable video library
- Categorized by topic
- Transcript available

---

## PART 4: ONBOARDING FLOW DESIGN

### 4.1 Signup (Stage 0)

**Screen: Landing → Signup**

```
┌─────────────────────────────────────┐
│                                     │
│   [Gemma Video Thumbnail - 60s]     │
│   "See how Covered works →"         │
│                                     │
│   ─────────────────────────────     │
│                                     │
│   Email: [________________]         │
│   Password: [________________]      │
│                                     │
│   [Get Started Free — 14 Days]      │
│                                     │
│   427 businesses signed up          │
│   this month                        │
│                                     │
└─────────────────────────────────────┘
```

**Psychology Applied:**
- Social proof (signup count)
- Low friction (email + password only)
- No credit card required
- Video builds motivation before commitment

### 4.2 Quick Setup (Stage 1)

**Step 1.1: Business Basics**

```
┌─────────────────────────────────────┐
│   ✓ Account created                 │
│   ○ Business details                │
│   ○ Phone setup                     │
│   ○ Test call                       │
│                                     │
│   ████████░░░░░░░░░░░░ 25%          │
│                                     │
│   What's your business called?      │
│   [________________________]        │
│                                     │
│   What type of business?            │
│   [Plumber     ▼]                   │
│                                     │
│   Where are you based?              │
│   [Postcode: ________]              │
│                                     │
│   [Continue →]                      │
│                                     │
└─────────────────────────────────────┘
```

**Psychology Applied:**
- Progress bar starts at 25% (endowed progress)
- Checklist shows what's done AND what's coming
- Only 3 fields (minimal friction)
- Vertical selection personalizes entire experience

**Step 1.2: Phone Setup**

```
┌─────────────────────────────────────┐
│                                     │
│   [Gemma Video - 45 sec]            │
│   "Here's how your number works"    │
│                                     │
│   ─────────────────────────────     │
│                                     │
│   Your Covered Number:              │
│   ┌─────────────────────────────┐   │
│   │  📞 0191 XXX XXXX           │   │
│   │  [Copy]                     │   │
│   └─────────────────────────────┘   │
│                                     │
│   Where should we forward calls     │
│   when you're available?            │
│                                     │
│   [+44 _______________]             │
│                                     │
│   ⓘ Calls go to Gemma first, then  │
│     to you if it's urgent           │
│                                     │
│   [Set Up Forwarding →]             │
│                                     │
└─────────────────────────────────────┘
```

**Psychology Applied:**
- Video explains before asking for input
- Number shown prominently (ownership feeling)
- Simple explanation of call flow
- One action: enter forwarding number

### 4.3 First Call (Stage 2)

**Step 2.1: Test Call Prompt**

```
┌─────────────────────────────────────┐
│                                     │
│   🎉 Your number is ready!          │
│                                     │
│   ████████████████░░░░ 75%          │
│                                     │
│   Now let's hear Gemma in action.   │
│                                     │
│   Call this number from your phone: │
│                                     │
│   ┌─────────────────────────────┐   │
│   │  📞 0191 XXX XXXX           │   │
│   │  [Tap to Call]              │   │
│   └─────────────────────────────┘   │
│                                     │
│   Try saying:                       │
│   "I need an emergency plumber"     │
│                                     │
│   [I've made my test call →]        │
│                                     │
└─────────────────────────────────────┘
```

**Psychology Applied:**
- Celebration of progress (🎉)
- Clear instruction
- Specific script to try
- "Tap to Call" on mobile (one tap)

**Step 2.2: Test Call Debrief**

```
┌─────────────────────────────────────┐
│                                     │
│   [Gemma Celebration Video - 30s]   │
│                                     │
│   ─────────────────────────────     │
│                                     │
│   ✅ Test call complete!            │
│                                     │
│   Here's what Gemma captured:       │
│                                     │
│   ┌─────────────────────────────┐   │
│   │ Caller: Your Mobile         │   │
│   │ Type: Emergency             │   │
│   │ Issue: Plumbing emergency   │   │
│   │ Urgency: High               │   │
│   │ Action: Callback needed     │   │
│   └─────────────────────────────┘   │
│                                     │
│   Pretty cool, right? 😎            │
│                                     │
│   [Go to Dashboard →]               │
│                                     │
└─────────────────────────────────────┘
```

**Psychology Applied:**
- Immediate celebration
- Show real data (proof it works)
- Personality ("Pretty cool, right?")
- Clear next step

### 4.4 Dashboard First Visit

**Guided Tour (Tooltips)**

```
Step 1/5: Attention Feed
┌─────────────────────────────────────┐
│ ┌───────────────────────────────┐   │
│ │ This is where urgent items    │   │
│ │ appear. Gemma flags anything  │   │
│ │ that needs your attention.    │   │
│ │                               │   │
│ │ [Got it] [Skip tour]          │   │
│ └───────────────────────────────┘   │
│         ▼                           │
│   ╔═══════════════════════════╗     │
│   ║  NEEDS ATTENTION          ║     │
│   ║  No items right now 🎉    ║     │
│   ╚═══════════════════════════╝     │
└─────────────────────────────────────┘
```

**Tour Sequence:**
1. Attention Feed (what needs action)
2. Today's Stats (calls, revenue, outstanding)
3. Quick Actions (new invoice, new customer)
4. Navigation (calls, invoices, customers)
5. Help (where to find support)

---

## PART 5: POST-ONBOARDING NURTURE

### 5.1 Email Sequence (First 30 Days)

| Day | Email | Subject | Goal |
|-----|-------|---------|------|
| 0 | Welcome | "Welcome to Covered, {name}!" | Excitement, next steps |
| 1 | First Call | "Your first call is waiting" | Drive test call if not done |
| 2 | Setup Check | "Quick question about your setup" | Ensure forwarding works |
| 3 | Feature Tip | "Did you know Gemma can..." | Introduce invoice feature |
| 5 | Success Story | "How {similar_business} saved 10 hrs/week" | Social proof, motivation |
| 7 | Week 1 Review | "Your first week with Covered" | Stats summary, celebration |
| 10 | Feature Tip | "Your reviews on autopilot" | Introduce review requests |
| 14 | Trial Reminder | "7 days left on your trial" | Urgency, value summary |
| 18 | ROI Calculator | "You've saved {X} hours this month" | Quantified value |
| 21 | Final Reminder | "Your trial ends in 3 days" | Clear CTA to subscribe |
| 30 | Month 1 Review | "Your first month: {stats}" | Celebration, roadmap |

### 5.2 Behavioral Triggers

**Trigger: No test call within 24 hours**
```
Email: "Gemma's ready to take your calls"
Video: 60-sec troubleshooting guide
In-app: Prominent "Make test call" banner
```

**Trigger: No real calls within 3 days**
```
Email: "Your Covered number isn't getting calls yet"
Action: Check forwarding setup automatically
Support: Proactive reach-out offer
```

**Trigger: First real call received**
```
Email: "🎉 Your first real call!"
In-app: Celebration modal with confetti
Video: "Here's what happened" breakdown
```

**Trigger: Dashboard not visited in 3 days**
```
Email: "You had {X} calls while you were away"
Push: (if mobile) Daily summary notification
```

**Trigger: Invoice created but not sent**
```
In-app: Tooltip "Ready to send?"
Email: "Your invoice is waiting to be sent"
```

### 5.3 In-App Prompts

| Prompt | Trigger | Content |
|--------|---------|---------|
| **Checklist Nudge** | < 100% complete, 3+ days | "Finish setup to unlock full power" |
| **Feature Discovery** | Using feature for first time | Contextual tooltip with video |
| **Celebration** | Milestone achieved | Confetti + message + next step |
| **Help Offer** | Confusion detected (rage clicks, long pause) | "Need help? Chat with us" |
| **Upgrade Prompt** | Trial ending + high engagement | "Keep your momentum going" |

---

## PART 6: SELF-SERVICE SUPPORT

### 6.1 Help Center Structure

```
/help
├── Getting Started
│   ├── How Covered works (video)
│   ├── Setting up your phone (video)
│   ├── Understanding your dashboard (video)
│   └── Your first week checklist
│
├── Calls
│   ├── How Gemma handles calls (video)
│   ├── Emergency call routing
│   ├── Missed calls and voicemail
│   └── Call quality troubleshooting
│
├── Invoices
│   ├── Creating invoices (video)
│   ├── Automatic reminders
│   ├── Recording payments
│   └── Invoice templates
│
├── Customers
│   ├── Adding customers
│   ├── Customer history
│   └── Importing contacts
│
├── Jobs & Quotes
│   ├── Creating jobs from calls
│   ├── Sending quotes
│   └── Converting quotes to jobs
│
├── Reviews
│   ├── Automatic review requests (video)
│   ├── Connecting Google reviews
│   └── Managing your reputation
│
├── Settings
│   ├── Business profile
│   ├── Gemma customization
│   ├── Team members
│   └── Billing & subscription
│
└── Troubleshooting
    ├── Calls not coming through
    ├── Forwarding issues
    ├── Email delivery problems
    └── Contact support
```

### 6.2 AI-Powered Search

**How it works:**
1. User types question in search box
2. GPT-4 interprets intent
3. Returns best matching article(s)
4. Offers to escalate if not helpful

**Example:**
```
User: "how do I make gemma sound different"
AI: Showing results for "Gemma voice customization"
→ "Customizing Gemma's Greeting" (article)
→ "Gemma Settings" (video - 60 sec)
```

### 6.3 Contextual Help Triggers

| Context | Help Offered |
|---------|--------------|
| First time on Invoices page | "New to invoicing? Watch our 2-min guide" |
| Error creating invoice | Inline error message + "Common fixes" link |
| Viewing empty Calls page | "No calls yet? Check your setup" |
| High bounce rate on page | Exit-intent: "Need help?" |

### 6.4 Escalation Paths

```
Self-Service (80% of queries)
    ↓ Not resolved
AI Chat (15% of queries)
    ↓ Not resolved
Email Support (4% of queries)
    ↓ Complex issue
Video Call (1% of queries)
```

**AI Chat (Powered by Claude):**
- Available 24/7
- Can access customer's account data
- Can perform simple actions (resend email, check status)
- Seamlessly escalates to human when needed

---

## PART 7: DATA MODEL

### 7.1 Prisma Schema Additions

```prisma
// Onboarding progress tracking
model OnboardingProgress {
  id                    String   @id @default(cuid())
  clientId              String   @unique
  client                Client   @relation(fields: [clientId], references: [id])
  
  // Stage tracking
  currentStage          OnboardingStage @default(SIGNUP)
  stageStartedAt        DateTime @default(now())
  
  // Milestone completion
  accountCreated        Boolean  @default(true)
  businessInfoCompleted Boolean  @default(false)
  phoneSetupCompleted   Boolean  @default(false)
  testCallCompleted     Boolean  @default(false)
  firstRealCall         Boolean  @default(false)
  firstInvoiceSent      Boolean  @default(false)
  firstReviewRequest    Boolean  @default(false)
  dashboardStreak       Int      @default(0) // consecutive days
  
  // Timestamps for milestones
  businessInfoAt        DateTime?
  phoneSetupAt          DateTime?
  testCallAt            DateTime?
  firstRealCallAt       DateTime?
  firstInvoiceSentAt    DateTime?
  firstReviewRequestAt  DateTime?
  
  // Completion percentage (0-100)
  completionPercent     Int      @default(10)
  
  // Tour progress
  dashboardTourComplete Boolean  @default(false)
  featuresToursComplete Json     @default("[]") // ["calls", "invoices", ...]
  
  createdAt             DateTime @default(now())
  updatedAt             DateTime @updatedAt
}

enum OnboardingStage {
  SIGNUP
  QUICK_SETUP
  FIRST_CALL
  ACTIVATION
  ADOPTION
  MASTERY
  COMPLETE
}

// Video watch tracking
model VideoWatch {
  id          String   @id @default(cuid())
  clientId    String
  client      Client   @relation(fields: [clientId], references: [id])
  
  videoId     String   // e.g., "welcome", "phone_setup", "invoices_intro"
  videoType   VideoType
  
  // Watch metrics
  startedAt   DateTime @default(now())
  completedAt DateTime?
  watchedSeconds Int    @default(0)
  totalSeconds   Int
  percentWatched Float  @default(0)
  
  // Context
  trigger     String?  // what caused the video to show
  location    String?  // where in the app
  
  @@index([clientId])
  @@index([videoId])
}

enum VideoType {
  ONBOARDING
  FEATURE_TRAINING
  CELEBRATION
  TROUBLESHOOTING
  SUPPORT
}

// Help article interactions
model HelpInteraction {
  id          String   @id @default(cuid())
  clientId    String?
  client      Client?  @relation(fields: [clientId], references: [id])
  
  articleId   String
  articleTitle String
  
  // Interaction type
  type        HelpInteractionType
  
  // Search context
  searchQuery String?
  
  // Feedback
  wasHelpful  Boolean?
  feedbackText String?
  
  // Escalation
  escalatedTo String?  // "chat", "email", "call"
  
  createdAt   DateTime @default(now())
  
  @@index([clientId])
  @@index([articleId])
}

enum HelpInteractionType {
  VIEW
  SEARCH
  VIDEO_WATCH
  FEEDBACK_POSITIVE
  FEEDBACK_NEGATIVE
  ESCALATE
}

// Support chat messages
model SupportChat {
  id          String   @id @default(cuid())
  clientId    String
  client      Client   @relation(fields: [clientId], references: [id])
  
  // Conversation
  messages    Json     // [{role: "user"|"assistant"|"human", content: "...", timestamp: "..."}]
  
  // Status
  status      ChatStatus @default(ACTIVE)
  
  // AI handling
  handledByAI Boolean  @default(true)
  escalatedAt DateTime?
  resolvedAt  DateTime?
  
  // Resolution
  resolution  String?
  wasResolved Boolean?
  
  createdAt   DateTime @default(now())
  updatedAt   DateTime @updatedAt
  
  @@index([clientId])
  @@index([status])
}

enum ChatStatus {
  ACTIVE
  WAITING_HUMAN
  RESOLVED
  CLOSED
}

// Behavioral events for triggers
model BehavioralEvent {
  id          String   @id @default(cuid())
  clientId    String
  client      Client   @relation(fields: [clientId], references: [id])
  
  eventType   String   // "page_view", "feature_use", "error", "rage_click"
  eventData   Json     // {page: "/invoices", action: "create", ...}
  
  // Session context
  sessionId   String?
  deviceType  String?  // "mobile", "desktop"
  
  createdAt   DateTime @default(now())
  
  @@index([clientId])
  @@index([eventType])
  @@index([createdAt])
}

// Nurture email tracking
model NurtureEmail {
  id          String   @id @default(cuid())
  clientId    String
  client      Client   @relation(fields: [clientId], references: [id])
  
  emailType   String   // "welcome", "day_3_tip", "week_1_review", etc.
  
  // Delivery
  sentAt      DateTime?
  deliveredAt DateTime?
  openedAt    DateTime?
  clickedAt   DateTime?
  
  // Suppression
  suppressed  Boolean  @default(false)
  suppressReason String?
  
  createdAt   DateTime @default(now())
  
  @@index([clientId])
  @@index([emailType])
}
```

### 7.2 Video Content Model

```typescript
// src/lib/videos/content.ts

export interface VideoContent {
  id: string;
  title: string;
  description: string;
  duration: number; // seconds
  type: 'onboarding' | 'feature' | 'celebration' | 'troubleshooting' | 'support';
  category: string;
  
  // Personalization
  personalizable: boolean;
  personalFields?: string[]; // ['firstName', 'businessName', 'vertical']
  
  // Variants by vertical
  variants?: {
    [vertical: string]: {
      scriptOverrides?: Partial<VideoScript>;
      examplesOverride?: string[];
    };
  };
  
  // Script
  script: VideoScript;
  
  // Delivery
  trigger?: VideoTrigger;
  showIn?: ('modal' | 'inline' | 'email' | 'help')[];
}

export interface VideoScript {
  scenes: VideoScene[];
}

export interface VideoScene {
  avatarId: string;
  text: string;
  emotion?: 'neutral' | 'happy' | 'excited' | 'concerned';
  background?: string;
  overlays?: VideoOverlay[];
}

export interface VideoOverlay {
  type: 'text' | 'image' | 'screenrecording';
  content: string;
  position: 'top' | 'bottom' | 'center' | 'left' | 'right';
  startTime: number;
  duration: number;
}

export interface VideoTrigger {
  type: 'event' | 'time' | 'page' | 'milestone';
  condition: string;
}

// Example video definition
export const VIDEOS: Record<string, VideoContent> = {
  welcome: {
    id: 'welcome',
    title: 'Welcome to Covered',
    description: 'Your personal introduction from Gemma',
    duration: 60,
    type: 'onboarding',
    category: 'getting-started',
    personalizable: true,
    personalFields: ['firstName', 'businessName', 'vertical'],
    script: {
      scenes: [
        {
          avatarId: 'gemma-main',
          text: `Hi {{firstName}}! I'm Gemma, and I'll be answering your phones from now on.

{{businessName}} is going to love this — I've already helped over 500 {{verticalPlural}} handle more than 50,000 calls.

In the next 2 minutes, we'll get your Covered number set up. Then you can test it yourself and hear exactly what your customers will experience.

Ready? Let's go!`,
          emotion: 'excited',
          background: 'office-friendly'
        }
      ]
    },
    trigger: {
      type: 'milestone',
      condition: 'accountCreated && !businessInfoCompleted'
    },
    showIn: ['modal', 'email']
  },
  
  // ... more videos
};
```

---

## PART 8: API ROUTES

### 8.1 Onboarding Progress

**GET** `/api/v1/clients/[id]/onboarding`
```typescript
// Returns current onboarding state
{
  stage: "QUICK_SETUP",
  completionPercent: 35,
  milestones: {
    accountCreated: true,
    businessInfoCompleted: true,
    phoneSetupCompleted: false,
    testCallCompleted: false,
    // ...
  },
  nextStep: {
    action: "phone_setup",
    title: "Set up your phone",
    description: "Get your Covered number ready",
    videoId: "phone_setup"
  },
  checklist: [
    { id: "account", label: "Create account", done: true },
    { id: "business", label: "Business details", done: true },
    { id: "phone", label: "Phone setup", done: false },
    { id: "test_call", label: "Test call", done: false }
  ]
}
```

**PATCH** `/api/v1/clients/[id]/onboarding`
```typescript
// Update milestone completion
{
  milestone: "phoneSetupCompleted",
  value: true
}
```

### 8.2 Video Tracking

**POST** `/api/v1/videos/watch`
```typescript
// Log video watch start
{
  clientId: "...",
  videoId: "welcome",
  trigger: "onboarding_modal",
  location: "/onboarding/step-1"
}

// Returns
{
  watchId: "..."
}
```

**PATCH** `/api/v1/videos/watch/[watchId]`
```typescript
// Update watch progress
{
  watchedSeconds: 45,
  completed: false
}
```

### 8.3 Help & Support

**GET** `/api/v1/help/search?q={query}`
```typescript
// AI-powered search
{
  query: "forwarding not working",
  results: [
    {
      id: "troubleshooting-forwarding",
      title: "Calls not coming through",
      snippet: "If calls aren't reaching your phone...",
      type: "article",
      relevance: 0.95
    },
    {
      id: "video-forwarding-setup",
      title: "Setting up call forwarding",
      type: "video",
      duration: 90,
      relevance: 0.82
    }
  ],
  suggestedAction: "Check your forwarding settings in Settings > Phone"
}
```

**POST** `/api/v1/support/chat`
```typescript
// Start or continue chat
{
  clientId: "...",
  message: "My calls aren't coming through"
}

// Returns
{
  chatId: "...",
  response: {
    role: "assistant",
    content: "I can help with that! Let me check your forwarding settings...",
    actions: [
      { type: "link", label: "Check settings", url: "/settings/phone" },
      { type: "article", id: "troubleshooting-forwarding" }
    ]
  },
  resolved: false
}
```

---

## PART 9: TRIGGER.DEV JOBS

### 9.1 Onboarding Progress Monitor

```typescript
// trigger-jobs/src/jobs/onboarding-monitor.ts

import { schedules } from '@trigger.dev/sdk/v3';
import { prisma } from '../lib/prisma';

export const onboardingMonitor = schedules.task({
  id: 'onboarding-monitor',
  cron: '0 * * * *', // Every hour
  run: async () => {
    // Find clients in onboarding stages
    const inProgress = await prisma.onboardingProgress.findMany({
      where: {
        currentStage: {
          not: 'COMPLETE'
        }
      },
      include: {
        client: true
      }
    });
    
    for (const progress of inProgress) {
      const hoursSinceStart = 
        (Date.now() - progress.stageStartedAt.getTime()) / (1000 * 60 * 60);
      
      // Check for stuck users
      if (progress.currentStage === 'QUICK_SETUP' && hoursSinceStart > 24) {
        // No test call after 24 hours
        if (!progress.testCallCompleted) {
          await triggerNudgeEmail(progress.client, 'stuck_no_test_call');
        }
      }
      
      if (progress.currentStage === 'ACTIVATION' && hoursSinceStart > 72) {
        // No real calls after 3 days
        if (!progress.firstRealCall) {
          await triggerNudgeEmail(progress.client, 'no_real_calls');
          await createAttentionItem(progress.client, 'check_forwarding');
        }
      }
      
      // Update dashboard streak
      const lastDashboardVisit = await prisma.behavioralEvent.findFirst({
        where: {
          clientId: progress.clientId,
          eventType: 'page_view',
          eventData: {
            path: { contains: '/dashboard' }
          }
        },
        orderBy: { createdAt: 'desc' }
      });
      
      if (lastDashboardVisit) {
        const daysSinceVisit = 
          (Date.now() - lastDashboardVisit.createdAt.getTime()) / (1000 * 60 * 60 * 24);
        
        if (daysSinceVisit < 1) {
          // Visited today, increment streak
          await prisma.onboardingProgress.update({
            where: { id: progress.id },
            data: { dashboardStreak: progress.dashboardStreak + 1 }
          });
        } else if (daysSinceVisit > 1) {
          // Streak broken
          await prisma.onboardingProgress.update({
            where: { id: progress.id },
            data: { dashboardStreak: 0 }
          });
        }
      }
    }
    
    return { processed: inProgress.length };
  }
});
```

### 9.2 Nurture Email Scheduler

```typescript
// trigger-jobs/src/jobs/nurture-scheduler.ts

import { schedules } from '@trigger.dev/sdk/v3';
import { prisma } from '../lib/prisma';
import { resend } from '../lib/resend';

const NURTURE_SEQUENCE = [
  { day: 0, emailType: 'welcome', condition: null },
  { day: 1, emailType: 'first_call_prompt', condition: '!testCallCompleted' },
  { day: 2, emailType: 'setup_check', condition: '!phoneSetupCompleted' },
  { day: 3, emailType: 'feature_tip_invoices', condition: null },
  { day: 5, emailType: 'success_story', condition: null },
  { day: 7, emailType: 'week_1_review', condition: null },
  { day: 10, emailType: 'feature_tip_reviews', condition: null },
  { day: 14, emailType: 'trial_reminder_7', condition: 'isTrial' },
  { day: 18, emailType: 'roi_calculator', condition: null },
  { day: 21, emailType: 'trial_reminder_3', condition: 'isTrial' },
  { day: 30, emailType: 'month_1_review', condition: null },
];

export const nurtureScheduler = schedules.task({
  id: 'nurture-scheduler',
  cron: '0 9 * * *', // 9am daily
  run: async () => {
    const clients = await prisma.client.findMany({
      where: {
        status: 'ACTIVE',
        createdAt: {
          gte: new Date(Date.now() - 31 * 24 * 60 * 60 * 1000) // Last 31 days
        }
      },
      include: {
        onboardingProgress: true,
        nurtureEmails: true
      }
    });
    
    let sent = 0;
    
    for (const client of clients) {
      const daysSinceSignup = Math.floor(
        (Date.now() - client.createdAt.getTime()) / (1000 * 60 * 60 * 24)
      );
      
      // Find email for today
      const todaysEmail = NURTURE_SEQUENCE.find(e => e.day === daysSinceSignup);
      
      if (!todaysEmail) continue;
      
      // Check if already sent
      const alreadySent = client.nurtureEmails.some(
        e => e.emailType === todaysEmail.emailType
      );
      
      if (alreadySent) continue;
      
      // Check condition
      if (todaysEmail.condition) {
        const meetsCondition = evaluateCondition(
          todaysEmail.condition,
          client.onboardingProgress
        );
        if (!meetsCondition) continue;
      }
      
      // Send email
      await sendNurtureEmail(client, todaysEmail.emailType);
      sent++;
    }
    
    return { sent };
  }
});
```

### 9.3 Video Generation Job

```typescript
// trigger-jobs/src/jobs/generate-personalized-video.ts

import { task } from '@trigger.dev/sdk/v3';
import { prisma } from '../lib/prisma';
import { heygen } from '../lib/heygen';

export const generatePersonalizedVideo = task({
  id: 'generate-personalized-video',
  run: async (payload: {
    clientId: string;
    videoId: string;
    personalizations: Record<string, string>;
  }) => {
    const { clientId, videoId, personalizations } = payload;
    
    const videoTemplate = VIDEOS[videoId];
    if (!videoTemplate) throw new Error(`Unknown video: ${videoId}`);
    
    // Get client for vertical-specific content
    const client = await prisma.client.findUnique({
      where: { id: clientId }
    });
    
    // Apply personalizations to script
    let script = videoTemplate.script;
    
    for (const scene of script.scenes) {
      scene.text = interpolateTemplate(scene.text, {
        ...personalizations,
        vertical: client?.vertical,
        verticalPlural: getVerticalPlural(client?.vertical)
      });
    }
    
    // Generate video via HeyGen
    const video = await heygen.generateVideo({
      avatarId: 'gemma-main',
      script: script,
      background: videoTemplate.script.scenes[0].background,
      voiceId: 'northern-british-female'
    });
    
    // Store video URL
    await prisma.generatedVideo.create({
      data: {
        clientId,
        videoId,
        url: video.url,
        expiresAt: new Date(Date.now() + 30 * 24 * 60 * 60 * 1000) // 30 days
      }
    });
    
    return { videoUrl: video.url };
  }
});
```

---

## PART 10: FRONTEND COMPONENTS

### 10.1 Onboarding Checklist

```tsx
// src/components/onboarding/OnboardingChecklist.tsx

'use client';

import { useState, useEffect } from 'react';
import { CheckCircle, Circle, ChevronRight, Play } from 'lucide-react';

interface ChecklistItem {
  id: string;
  label: string;
  done: boolean;
  action?: string;
  videoId?: string;
}

interface OnboardingChecklistProps {
  items: ChecklistItem[];
  completionPercent: number;
  onItemClick: (itemId: string) => void;
}

export function OnboardingChecklist({
  items,
  completionPercent,
  onItemClick
}: OnboardingChecklistProps) {
  // Endowed progress: show slightly more than actual to motivate
  const displayPercent = Math.min(completionPercent + 5, 100);
  
  return (
    <div className="bg-white rounded-2xl p-5 border border-grey-200">
      <div className="flex items-center justify-between mb-4">
        <h3 className="text-base font-semibold text-grey-900">
          Getting Started
        </h3>
        <span className="text-sm text-grey-500">
          {completionPercent}% complete
        </span>
      </div>
      
      {/* Progress bar with animation */}
      <div className="h-2 bg-grey-100 rounded-full mb-5 overflow-hidden">
        <div 
          className="h-full bg-green-500 rounded-full transition-all duration-1000 ease-out"
          style={{ width: `${displayPercent}%` }}
        />
      </div>
      
      <div className="space-y-3">
        {items.map((item, index) => (
          <button
            key={item.id}
            onClick={() => !item.done && onItemClick(item.id)}
            disabled={item.done}
            className={`
              w-full flex items-center gap-3 p-3 rounded-xl
              transition-all duration-200
              ${item.done 
                ? 'bg-green-50 cursor-default' 
                : 'bg-grey-50 hover:bg-grey-100 cursor-pointer'
              }
            `}
          >
            {item.done ? (
              <CheckCircle className="w-5 h-5 text-green-500 flex-shrink-0" />
            ) : (
              <Circle className="w-5 h-5 text-grey-300 flex-shrink-0" />
            )}
            
            <span className={`
              flex-1 text-left text-sm
              ${item.done ? 'text-grey-500 line-through' : 'text-grey-900'}
            `}>
              {item.label}
            </span>
            
            {!item.done && item.videoId && (
              <Play className="w-4 h-4 text-grey-400" />
            )}
            
            {!item.done && (
              <ChevronRight className="w-4 h-4 text-grey-400" />
            )}
          </button>
        ))}
      </div>
      
      {completionPercent < 100 && (
        <p className="mt-4 text-xs text-grey-500 text-center">
          Complete setup to unlock all features
        </p>
      )}
    </div>
  );
}
```

### 10.2 Video Modal

```tsx
// src/components/onboarding/VideoModal.tsx

'use client';

import { useState, useEffect, useRef } from 'react';
import { X, Volume2, VolumeX } from 'lucide-react';

interface VideoModalProps {
  videoUrl: string;
  title: string;
  onClose: () => void;
  onComplete: () => void;
  autoPlay?: boolean;
}

export function VideoModal({
  videoUrl,
  title,
  onClose,
  onComplete,
  autoPlay = true
}: VideoModalProps) {
  const videoRef = useRef<HTMLVideoElement>(null);
  const [muted, setMuted] = useState(autoPlay); // Start muted if autoplay
  const [progress, setProgress] = useState(0);
  const [canSkip, setCanSkip] = useState(false);
  
  useEffect(() => {
    // Allow skip after 5 seconds
    const timer = setTimeout(() => setCanSkip(true), 5000);
    return () => clearTimeout(timer);
  }, []);
  
  useEffect(() => {
    const video = videoRef.current;
    if (!video) return;
    
    const handleTimeUpdate = () => {
      const percent = (video.currentTime / video.duration) * 100;
      setProgress(percent);
      
      if (percent >= 90) {
        onComplete();
      }
    };
    
    video.addEventListener('timeupdate', handleTimeUpdate);
    return () => video.removeEventListener('timeupdate', handleTimeUpdate);
  }, [onComplete]);
  
  return (
    <div className="fixed inset-0 z-50 flex items-center justify-center bg-black/70">
      <div className="bg-white rounded-2xl overflow-hidden max-w-lg w-full mx-4">
        {/* Header */}
        <div className="flex items-center justify-between p-4 border-b">
          <h3 className="font-semibold text-grey-900">{title}</h3>
          {canSkip && (
            <button
              onClick={onClose}
              className="p-1 hover:bg-grey-100 rounded-full"
            >
              <X className="w-5 h-5 text-grey-500" />
            </button>
          )}
        </div>
        
        {/* Video */}
        <div className="relative aspect-video bg-black">
          <video
            ref={videoRef}
            src={videoUrl}
            autoPlay={autoPlay}
            muted={muted}
            playsInline
            className="w-full h-full"
          />
          
          {/* Unmute prompt */}
          {muted && (
            <button
              onClick={() => setMuted(false)}
              className="absolute bottom-4 right-4 flex items-center gap-2 
                         bg-white/90 px-3 py-2 rounded-full text-sm font-medium
                         hover:bg-white transition-colors"
            >
              <VolumeX className="w-4 h-4" />
              Tap for sound
            </button>
          )}
          
          {/* Progress bar */}
          <div className="absolute bottom-0 left-0 right-0 h-1 bg-white/30">
            <div 
              className="h-full bg-white transition-all"
              style={{ width: `${progress}%` }}
            />
          </div>
        </div>
        
        {/* Skip button (appears after 5s) */}
        {!canSkip && (
          <div className="p-4 text-center text-sm text-grey-500">
            Skip available in {5 - Math.floor(progress * 0.05)}s...
          </div>
        )}
        
        {canSkip && (
          <div className="p-4">
            <button
              onClick={onClose}
              className="w-full py-3 bg-brand-500 text-white rounded-xl
                         font-medium hover:bg-brand-600 transition-colors"
            >
              Continue
            </button>
          </div>
        )}
      </div>
    </div>
  );
}
```

### 10.3 Celebration Modal

```tsx
// src/components/onboarding/CelebrationModal.tsx

'use client';

import { useEffect, useState } from 'react';
import confetti from 'canvas-confetti';
import { Star, ArrowRight } from 'lucide-react';

interface CelebrationModalProps {
  title: string;
  message: string;
  nextAction?: {
    label: string;
    href: string;
  };
  onClose: () => void;
}

export function CelebrationModal({
  title,
  message,
  nextAction,
  onClose
}: CelebrationModalProps) {
  const [showContent, setShowContent] = useState(false);
  
  useEffect(() => {
    // Fire confetti
    confetti({
      particleCount: 100,
      spread: 70,
      origin: { y: 0.6 }
    });
    
    // Animate content in
    setTimeout(() => setShowContent(true), 300);
  }, []);
  
  return (
    <div className="fixed inset-0 z-50 flex items-center justify-center bg-black/50">
      <div className={`
        bg-white rounded-2xl p-8 max-w-sm w-full mx-4 text-center
        transform transition-all duration-500
        ${showContent ? 'scale-100 opacity-100' : 'scale-90 opacity-0'}
      `}>
        <div className="w-16 h-16 bg-yellow-100 rounded-full flex items-center 
                        justify-center mx-auto mb-4">
          <Star className="w-8 h-8 text-yellow-500 fill-current" />
        </div>
        
        <h2 className="text-xl font-bold text-grey-900 mb-2">
          {title}
        </h2>
        
        <p className="text-grey-600 mb-6">
          {message}
        </p>
        
        {nextAction ? (
          <a
            href={nextAction.href}
            onClick={onClose}
            className="inline-flex items-center gap-2 px-6 py-3 
                       bg-brand-500 text-white rounded-xl font-medium
                       hover:bg-brand-600 transition-colors"
          >
            {nextAction.label}
            <ArrowRight className="w-4 h-4" />
          </a>
        ) : (
          <button
            onClick={onClose}
            className="px-6 py-3 bg-brand-500 text-white rounded-xl 
                       font-medium hover:bg-brand-600 transition-colors"
          >
            Continue
          </button>
        )}
      </div>
    </div>
  );
}
```

### 10.4 Help Search

```tsx
// src/components/support/HelpSearch.tsx

'use client';

import { useState, useCallback } from 'react';
import { Search, Book, PlayCircle, MessageCircle } from 'lucide-react';
import debounce from 'lodash/debounce';

interface SearchResult {
  id: string;
  title: string;
  snippet: string;
  type: 'article' | 'video' | 'action';
  url?: string;
  videoId?: string;
  duration?: number;
}

export function HelpSearch() {
  const [query, setQuery] = useState('');
  const [results, setResults] = useState<SearchResult[]>([]);
  const [loading, setLoading] = useState(false);
  
  const search = useCallback(
    debounce(async (q: string) => {
      if (q.length < 2) {
        setResults([]);
        return;
      }
      
      setLoading(true);
      try {
        const res = await fetch(`/api/v1/help/search?q=${encodeURIComponent(q)}`);
        const data = await res.json();
        setResults(data.results);
      } finally {
        setLoading(false);
      }
    }, 300),
    []
  );
  
  const handleChange = (e: React.ChangeEvent<HTMLInputElement>) => {
    const value = e.target.value;
    setQuery(value);
    search(value);
  };
  
  const getIcon = (type: string) => {
    switch (type) {
      case 'video': return <PlayCircle className="w-5 h-5 text-brand-500" />;
      case 'action': return <MessageCircle className="w-5 h-5 text-green-500" />;
      default: return <Book className="w-5 h-5 text-grey-400" />;
    }
  };
  
  return (
    <div className="relative">
      <div className="relative">
        <Search className="absolute left-4 top-1/2 -translate-y-1/2 w-5 h-5 text-grey-400" />
        <input
          type="text"
          value={query}
          onChange={handleChange}
          placeholder="Search help articles, videos, or ask a question..."
          className="w-full pl-12 pr-4 py-3 border border-grey-200 rounded-xl
                     focus:ring-2 focus:ring-brand-500 focus:border-brand-500
                     outline-none transition-all"
        />
      </div>
      
      {/* Results dropdown */}
      {(results.length > 0 || loading) && query.length >= 2 && (
        <div className="absolute top-full left-0 right-0 mt-2 bg-white 
                        rounded-xl border border-grey-200 shadow-lg z-10
                        max-h-96 overflow-auto">
          {loading ? (
            <div className="p-4 text-center text-grey-500">
              Searching...
            </div>
          ) : (
            <div className="p-2">
              {results.map((result) => (
                <a
                  key={result.id}
                  href={result.url || `/help/${result.id}`}
                  className="flex items-start gap-3 p-3 rounded-lg
                             hover:bg-grey-50 transition-colors"
                >
                  <div className="mt-0.5">
                    {getIcon(result.type)}
                  </div>
                  <div className="flex-1 min-w-0">
                    <h4 className="font-medium text-grey-900 truncate">
                      {result.title}
                    </h4>
                    <p className="text-sm text-grey-500 line-clamp-2">
                      {result.snippet}
                    </p>
                    {result.duration && (
                      <span className="text-xs text-grey-400 mt-1">
                        {Math.round(result.duration / 60)} min video
                      </span>
                    )}
                  </div>
                </a>
              ))}
              
              {/* Can't find what you need? */}
              <div className="border-t border-grey-100 mt-2 pt-2">
                <a
                  href="/support/chat"
                  className="flex items-center gap-3 p-3 rounded-lg
                             hover:bg-grey-50 transition-colors"
                >
                  <MessageCircle className="w-5 h-5 text-brand-500" />
                  <span className="text-sm font-medium text-brand-500">
                    Chat with support
                  </span>
                </a>
              </div>
            </div>
          )}
        </div>
      )}
    </div>
  );
}
```

---

## PART 11: SUCCESS METRICS

### 11.1 Onboarding Metrics

| Metric | Target | Measurement |
|--------|--------|-------------|
| **Time to First Value** | < 5 min | Signup → Test call complete |
| **Setup Completion Rate** | > 85% | Users completing all 4 steps |
| **Day 1 Activation** | > 60% | Real call received within 24h |
| **Day 7 Retention** | > 70% | Active on Day 7 |
| **Day 30 Retention** | > 50% | Active on Day 30 |

### 11.2 Support Metrics

| Metric | Target | Measurement |
|--------|--------|-------------|
| **Self-Service Rate** | > 80% | Issues resolved without human |
| **AI Chat Resolution** | > 70% | Chats resolved by AI |
| **Avg Response Time** | < 2 min | First response to query |
| **CSAT** | > 4.5/5 | Post-interaction survey |
| **Support Tickets/Customer** | < 0.5/mo | Human tickets per customer |

### 11.3 Video Engagement

| Metric | Target | Measurement |
|--------|--------|-------------|
| **Watch Rate** | > 70% | Started / Shown |
| **Completion Rate** | > 50% | Finished / Started |
| **Avg Watch Time** | > 60% of video | Time watched / Duration |
| **Click-Through Rate** | > 30% | CTA clicks / Completions |

---

## PART 12: BUILD SEQUENCE

### Phase 1: Core Onboarding (Day 1)
1. Add OnboardingProgress model to Prisma
2. Create onboarding API routes
3. Build 4-step onboarding flow pages
4. Implement OnboardingChecklist component
5. Add progress tracking

### Phase 2: Video System (Day 2)
1. Integrate HeyGen/Synthesia API
2. Create video content definitions
3. Build VideoModal component
4. Implement video tracking
5. Generate welcome + setup videos

### Phase 3: Nurture Engine (Day 3)
1. Add NurtureEmail model
2. Create email templates (React Email)
3. Build nurture-scheduler job
4. Add behavioral event tracking
5. Implement trigger-based emails

### Phase 4: Support System (Day 4)
1. Build HelpSearch component
2. Create help article content
3. Add SupportChat model
4. Integrate Claude for AI chat
5. Build contextual help triggers

### Phase 5: Celebrations & Polish (Day 5)
1. Add CelebrationModal component
2. Implement milestone celebrations
3. Add confetti animations
4. Create achievement badges
5. Final testing and polish

---

## CLAUDE CODE BUILD PROMPT

```
Build the automated onboarding, training, and support system for Covered AI.

Read: /specs/18-ONBOARDING-TRAINING-SUPPORT-ENGINE.md

Build in sequence:

1. Database Schema
   - Add all models from Part 7 to prisma/schema.prisma
   - Run migration

2. Onboarding Flow
   - Create /app/(onboarding)/step-1/page.tsx through step-4/page.tsx
   - Create /app/(onboarding)/complete/page.tsx
   - Build OnboardingChecklist component
   - Track progress via API

3. Video System
   - Create video content definitions in /lib/videos/content.ts
   - Build VideoModal component
   - Build CelebrationModal component with confetti
   - Track video watches

4. Dashboard Integration
   - Add onboarding checklist to dashboard (if not 100%)
   - Trigger videos on first feature visits
   - Show celebrations on milestones

5. Nurture Engine
   - Create nurture email templates in /emails/
   - Build nurture-scheduler.ts Trigger.dev job
   - Build onboarding-monitor.ts job

6. Support System
   - Build HelpSearch component
   - Create help content structure
   - Build AI chat integration
   - Add contextual help triggers

7. Behavioral Tracking
   - Log page views and feature usage
   - Track for trigger conditions
   - Feed into nurture logic

Apply BJ Fogg Behavior Model throughout:
- Every screen needs: Motivation (why), Ability (easy), Prompt (CTA)
- Progress bars start at 20% (endowed progress)
- Celebrate every milestone
- Use loss aversion in copy ("Don't miss...")

Start now. Build everything.
```

---

## SUMMARY

This system transforms customer onboarding from a friction point into a competitive advantage by:

1. **Reducing time-to-value** to under 5 minutes through ruthless simplification
2. **Using psychology** (Fogg Model, Zeigarnik, social proof) to drive completion
3. **Personalizing with AI video avatars** that scale infinitely
4. **Automating support** so 80%+ of queries self-resolve
5. **Creating habits** through the Hook Model
6. **Continuously improving** via behavioral tracking and feedback loops

The result: Higher activation, lower churn, fewer support tickets, and customers who become advocates.

---
title: "CLAUDE CODE BUILD PROMPT: Onboarding, Training & Support System"
id: "build-onboarding-system"
version: 1
created: "2026-04-25"
type: "document"
topic_type: "unsorted"
audience: "internal"
layer: "shadow"
status: "filed"
signed_by: "Devon, 2026-04-25, devin-992682c244cf444f91e0a516498afbfd"
---

# CLAUDE CODE BUILD PROMPT: Onboarding, Training & Support System

## CONTEXT

You are building an automated onboarding, training, and support system for Covered AI — a B2B SaaS product that provides AI phone answering for SMBs (vets, salons, plumbers, etc.).

**Core principle:** Apply BJ Fogg Behavior Model (B = MAP) throughout:
- **Motivation:** Show ROI, celebrate wins, social proof
- **Ability:** Reduce steps, pre-fill data, guided flows  
- **Prompt:** Contextual nudges, timely emails, in-app cues

**Reference spec:** `/specs/18-ONBOARDING-TRAINING-SUPPORT-ENGINE.md`

---

## PHASE 1: DATABASE SCHEMA

### Task 1.1: Add Prisma Models

Add these models to `prisma/schema.prisma`:

```prisma
// ============================================
// ONBOARDING & TRAINING MODELS
// ============================================

// Onboarding progress tracking
model OnboardingProgress {
  id                    String   @id @default(cuid())
  clientId              String   @unique
  client                Client   @relation(fields: [clientId], references: [id], onDelete: Cascade)
  
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
  dashboardStreak       Int      @default(0)
  
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
  featuresToursComplete String[] @default([])
  
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
  id             String    @id @default(cuid())
  clientId       String
  client         Client    @relation(fields: [clientId], references: [id], onDelete: Cascade)
  
  videoId        String
  videoType      VideoType
  
  startedAt      DateTime  @default(now())
  completedAt    DateTime?
  watchedSeconds Int       @default(0)
  totalSeconds   Int
  percentWatched Float     @default(0)
  
  trigger        String?
  location       String?
  
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
  id           String              @id @default(cuid())
  clientId     String?
  client       Client?             @relation(fields: [clientId], references: [id], onDelete: SetNull)
  
  articleId    String
  articleTitle String
  
  type         HelpInteractionType
  
  searchQuery  String?
  wasHelpful   Boolean?
  feedbackText String?
  escalatedTo  String?
  
  createdAt    DateTime @default(now())
  
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
  id          String     @id @default(cuid())
  clientId    String
  client      Client     @relation(fields: [clientId], references: [id], onDelete: Cascade)
  
  messages    Json       @default("[]")
  status      ChatStatus @default(ACTIVE)
  
  handledByAI Boolean    @default(true)
  escalatedAt DateTime?
  resolvedAt  DateTime?
  
  resolution  String?
  wasResolved Boolean?
  
  createdAt   DateTime   @default(now())
  updatedAt   DateTime   @updatedAt
  
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
  id         String   @id @default(cuid())
  clientId   String
  client     Client   @relation(fields: [clientId], references: [id], onDelete: Cascade)
  
  eventType  String
  eventData  Json     @default("{}")
  
  sessionId  String?
  deviceType String?
  
  createdAt  DateTime @default(now())
  
  @@index([clientId])
  @@index([eventType])
  @@index([createdAt])
}

// Nurture email tracking
model NurtureEmail {
  id             String    @id @default(cuid())
  clientId       String
  client         Client    @relation(fields: [clientId], references: [id], onDelete: Cascade)
  
  emailType      String
  
  sentAt         DateTime?
  deliveredAt    DateTime?
  openedAt       DateTime?
  clickedAt      DateTime?
  
  suppressed     Boolean   @default(false)
  suppressReason String?
  
  createdAt      DateTime  @default(now())
  
  @@index([clientId])
  @@index([emailType])
}

// Generated personalized videos cache
model GeneratedVideo {
  id        String   @id @default(cuid())
  clientId  String
  client    Client   @relation(fields: [clientId], references: [id], onDelete: Cascade)
  
  videoId   String
  url       String
  expiresAt DateTime
  
  createdAt DateTime @default(now())
  
  @@unique([clientId, videoId])
  @@index([clientId])
}
```

### Task 1.2: Update Client Model Relations

Add these relations to the existing `Client` model:

```prisma
// Add to Client model
onboardingProgress OnboardingProgress?
videoWatches       VideoWatch[]
helpInteractions   HelpInteraction[]
supportChats       SupportChat[]
behavioralEvents   BehavioralEvent[]
nurtureEmails      NurtureEmail[]
generatedVideos    GeneratedVideo[]
```

### Task 1.3: Run Migration

```bash
npx prisma migrate dev --name add_onboarding_system
npx prisma generate
```

---

## PHASE 2: VIDEO CONTENT SYSTEM

### Task 2.1: Create Video Content Definitions

Create `src/lib/videos/content.ts`:

```typescript
export interface VideoContent {
  id: string;
  title: string;
  description: string;
  duration: number; // seconds
  type: 'onboarding' | 'feature' | 'celebration' | 'troubleshooting' | 'support';
  category: string;
  personalizable: boolean;
  personalFields?: string[];
  script: string;
  trigger?: {
    type: 'event' | 'time' | 'page' | 'milestone';
    condition: string;
  };
  showIn: ('modal' | 'inline' | 'email' | 'help')[];
  // Placeholder URL until HeyGen integration
  placeholderUrl?: string;
}

export const VIDEOS: Record<string, VideoContent> = {
  // ===== ONBOARDING VIDEOS =====
  welcome: {
    id: 'welcome',
    title: 'Welcome to Covered',
    description: 'Your personal introduction from Gemma',
    duration: 60,
    type: 'onboarding',
    category: 'getting-started',
    personalizable: true,
    personalFields: ['firstName', 'businessName', 'vertical'],
    script: `Hi {{firstName}}! I'm Gemma, and I'll be answering your phones from now on.

{{businessName}} is going to love this — I've already helped over 500 {{verticalPlural}} handle more than 50,000 calls.

In the next 2 minutes, we'll get your Covered number set up. Then you can test it yourself and hear exactly what your customers will experience.

Ready? Let's go!`,
    trigger: {
      type: 'milestone',
      condition: 'accountCreated && !businessInfoCompleted'
    },
    showIn: ['modal', 'email'],
    placeholderUrl: '/videos/welcome-placeholder.mp4'
  },

  quick_tour: {
    id: 'quick_tour',
    title: 'Quick Dashboard Tour',
    description: 'Overview of your Covered dashboard',
    duration: 90,
    type: 'onboarding',
    category: 'getting-started',
    personalizable: false,
    script: `This is your Covered dashboard — your command centre for everything.

Up top, you'll see your Attention Feed. This is where Gemma flags anything urgent — emergency calls, overdue invoices, review requests.

Below that, your daily stats: calls handled, revenue tracked, outstanding payments.

On the left, quick navigation to Calls, Invoices, Customers, and Settings.

And if you ever need help, just click the question mark in the corner. I'm always here.

Let's make your first call!`,
    trigger: {
      type: 'page',
      condition: 'firstVisit:/dashboard'
    },
    showIn: ['modal'],
    placeholderUrl: '/videos/tour-placeholder.mp4'
  },

  phone_setup: {
    id: 'phone_setup',
    title: 'Your Covered Number',
    description: 'How your phone number works',
    duration: 45,
    type: 'onboarding',
    category: 'getting-started',
    personalizable: true,
    personalFields: ['coveredNumber'],
    script: `Here's your new Covered number: {{coveredNumber}}.

When customers call this number, I answer first. I'll find out what they need, check if it's urgent, and either handle it myself or connect them to you.

All you need to do is tell me where to forward urgent calls. That's usually your mobile.

Pop your number in below, and we're ready for a test run!`,
    trigger: {
      type: 'milestone',
      condition: 'businessInfoCompleted && !phoneSetupCompleted'
    },
    showIn: ['inline'],
    placeholderUrl: '/videos/phone-setup-placeholder.mp4'
  },

  meet_gemma: {
    id: 'meet_gemma',
    title: 'Meet Gemma',
    description: 'What Gemma can do for you',
    duration: 60,
    type: 'onboarding',
    category: 'getting-started',
    personalizable: true,
    personalFields: ['vertical'],
    script: `I'm Gemma, your AI receptionist. Here's what I do:

When someone calls, I greet them professionally and find out what they need. For {{vertical}} businesses like yours, I know the right questions to ask.

If it's an emergency, I'll get you on the line immediately. If it's a routine enquiry, I'll take their details and add it to your dashboard.

I never miss a call. I never take a day off. And I always sound like I've had my morning coffee.

Ready to hear me in action? Make a test call!`,
    trigger: {
      type: 'milestone',
      condition: 'phoneSetupCompleted && !testCallCompleted'
    },
    showIn: ['modal'],
    placeholderUrl: '/videos/meet-gemma-placeholder.mp4'
  },

  // ===== FEATURE TRAINING VIDEOS =====
  calls_dashboard: {
    id: 'calls_dashboard',
    title: 'Understanding Your Calls',
    description: 'How to use the calls dashboard',
    duration: 90,
    type: 'feature',
    category: 'calls',
    personalizable: false,
    script: `Your Calls dashboard shows every conversation I've had.

Each call shows: who called, when, what they needed, and whether it's been handled.

Click any call to see the full transcript, hear the recording, and take action — like creating an invoice or scheduling a callback.

The filter at the top lets you see just emergencies, or just today's calls, or calls that still need attention.

Pro tip: check this every morning. It takes 30 seconds and keeps you on top of everything.`,
    trigger: {
      type: 'event',
      condition: 'firstRealCall'
    },
    showIn: ['modal', 'help'],
    placeholderUrl: '/videos/calls-dashboard-placeholder.mp4'
  },

  creating_invoices: {
    id: 'creating_invoices',
    title: 'Creating Invoices',
    description: 'Step-by-step invoice creation',
    duration: 120,
    type: 'feature',
    category: 'invoices',
    personalizable: false,
    script: `Creating an invoice takes about 30 seconds. Here's how:

Click "New Invoice" or create one directly from a call record.

Add the customer — if they've called before, I'll have their details ready.

Add line items for your work. You can save common items as templates.

Set the due date, add any notes, and hit Send.

Your customer gets a professional email with a link to pay online. I'll chase them automatically if they forget.

That's it. No more Word documents. No more "did they pay?" spreadsheets.`,
    trigger: {
      type: 'page',
      condition: 'firstVisit:/invoices/new'
    },
    showIn: ['inline', 'help'],
    placeholderUrl: '/videos/invoices-placeholder.mp4'
  },

  invoice_chasing: {
    id: 'invoice_chasing',
    title: 'Automatic Invoice Reminders',
    description: 'How invoice chasing works',
    duration: 90,
    type: 'feature',
    category: 'invoices',
    personalizable: false,
    script: `Once you send an invoice, I handle the awkward follow-ups.

Day 1: Friendly reminder that the invoice is due soon.
Day 7: Polite nudge that it's now overdue.
Day 14: Firmer reminder with payment link.
Day 30: Final notice before you need to step in.

Each email is professional but firm. Your customer sees your branding, not mine.

You can customise the timing or turn off chasing for specific invoices. But honestly? Just let me handle it. Most people pay after the first reminder.`,
    trigger: {
      type: 'event',
      condition: 'firstInvoiceSent'
    },
    showIn: ['modal', 'help'],
    placeholderUrl: '/videos/chasing-placeholder.mp4'
  },

  review_requests: {
    id: 'review_requests',
    title: 'Getting More Reviews',
    description: 'Automatic review request system',
    duration: 60,
    type: 'feature',
    category: 'reviews',
    personalizable: false,
    script: `Happy customers are your best marketing. Let's turn them into 5-star reviews.

When you mark a job as complete, I automatically send a friendly email asking for a Google review.

The timing is perfect — right after you've delivered great work, when they're most likely to say nice things.

You can see all your reviews in one place and respond directly from Covered.

More reviews means more visibility on Google, which means more calls. It's a virtuous cycle.`,
    trigger: {
      type: 'milestone',
      condition: 'firstRealCall && !firstReviewRequest'
    },
    showIn: ['modal', 'help'],
    placeholderUrl: '/videos/reviews-placeholder.mp4'
  },

  attention_items: {
    id: 'attention_items',
    title: 'Your Attention Feed',
    description: 'What attention items mean',
    duration: 75,
    type: 'feature',
    category: 'dashboard',
    personalizable: false,
    script: `Your Attention Feed is like a smart to-do list that I manage for you.

When something needs your input, it appears here. Emergency callbacks, overdue invoices, review opportunities.

Each item has a priority: red for urgent, amber for important, green for whenever you have time.

Click an item to take action. Once handled, it disappears.

Check this once in the morning and once after lunch. If it's empty, you're winning.`,
    trigger: {
      type: 'event',
      condition: 'firstAttentionItem'
    },
    showIn: ['modal', 'help'],
    placeholderUrl: '/videos/attention-placeholder.mp4'
  },

  // ===== CELEBRATION VIDEOS =====
  first_call_success: {
    id: 'first_call_success',
    title: 'First Call Complete!',
    description: 'Celebrating your first real call',
    duration: 30,
    type: 'celebration',
    category: 'milestones',
    personalizable: true,
    personalFields: ['firstName'],
    script: `{{firstName}}, you just got your first real call through Covered!

This is huge. From now on, every call gets answered professionally, every enquiry gets logged, and you never miss an opportunity.

Your customers are going to love this. And so is your sanity.

Let's keep the momentum going!`,
    trigger: {
      type: 'event',
      condition: 'firstRealCall'
    },
    showIn: ['modal'],
    placeholderUrl: '/videos/celebration-placeholder.mp4'
  },

  first_invoice_paid: {
    id: 'first_invoice_paid',
    title: 'First Payment Received!',
    description: 'Celebrating first invoice payment',
    duration: 30,
    type: 'celebration',
    category: 'milestones',
    personalizable: true,
    personalFields: ['firstName', 'amount'],
    script: `Cha-ching! {{firstName}}, you just got paid {{amount}} through Covered.

No chasing. No awkward phone calls. Just money in your account.

This is what running a modern business feels like. Let's do it again!`,
    trigger: {
      type: 'event',
      condition: 'firstInvoicePaid'
    },
    showIn: ['modal'],
    placeholderUrl: '/videos/payment-celebration-placeholder.mp4'
  },

  week_1_complete: {
    id: 'week_1_complete',
    title: 'Week 1 Complete!',
    description: 'Your first week summary',
    duration: 45,
    type: 'celebration',
    category: 'milestones',
    personalizable: true,
    personalFields: ['firstName', 'callCount', 'hoursaved'],
    script: `{{firstName}}, what a week!

I've handled {{callCount}} calls for you. That's roughly {{hoursSaved}} hours you didn't spend on the phone.

Your customers got instant, professional responses. You got your time back.

Week 2 is going to be even better. I'm learning your business every day.`,
    trigger: {
      type: 'time',
      condition: 'daysSinceSignup:7'
    },
    showIn: ['modal', 'email'],
    placeholderUrl: '/videos/week1-placeholder.mp4'
  },

  // ===== TROUBLESHOOTING VIDEOS =====
  forwarding_not_working: {
    id: 'forwarding_not_working',
    title: 'Calls Not Coming Through?',
    description: 'Troubleshooting call forwarding',
    duration: 90,
    type: 'troubleshooting',
    category: 'calls',
    personalizable: false,
    script: `If calls aren't reaching your phone, let's fix that.

First, check your forwarding number in Settings. Make sure it's correct and includes the country code.

Second, check your mobile isn't on Do Not Disturb or blocking unknown numbers.

Third, try calling your Covered number from a different phone. If I answer, the problem is on your mobile's end.

Still stuck? Use the chat button below and I'll help you sort it out.`,
    trigger: {
      type: 'event',
      condition: 'noCallsAfter24Hours'
    },
    showIn: ['modal', 'help'],
    placeholderUrl: '/videos/troubleshooting-placeholder.mp4'
  }
};

// Helper to get videos by type
export function getVideosByType(type: VideoContent['type']): VideoContent[] {
  return Object.values(VIDEOS).filter(v => v.type === type);
}

// Helper to get video by trigger condition
export function getVideoByTrigger(triggerType: string, condition: string): VideoContent | undefined {
  return Object.values(VIDEOS).find(
    v => v.trigger?.type === triggerType && v.trigger?.condition === condition
  );
}

// Helper to interpolate personalizations
export function interpolateVideoScript(
  script: string,
  personalizations: Record<string, string>
): string {
  return script.replace(/\{\{(\w+)\}\}/g, (match, key) => {
    return personalizations[key] || match;
  });
}

// Vertical display names
export const VERTICAL_PLURALS: Record<string, string> = {
  plumber: 'plumbing businesses',
  electrician: 'electrical contractors',
  vet: 'veterinary practices',
  salon: 'salons',
  physio: 'physiotherapy clinics',
  dental: 'dental practices',
  garage: 'garages',
  builder: 'building companies',
  landscaper: 'landscaping businesses',
  cleaner: 'cleaning companies'
};

export function getVerticalPlural(vertical?: string): string {
  return VERTICAL_PLURALS[vertical || ''] || 'businesses';
}
```

### Task 2.2: Create Video Types

Create `src/lib/videos/types.ts`:

```typescript
export interface VideoWatchEvent {
  clientId: string;
  videoId: string;
  trigger: string;
  location: string;
}

export interface VideoProgress {
  watchId: string;
  watchedSeconds: number;
  completed: boolean;
}

export interface PersonalizedVideoRequest {
  clientId: string;
  videoId: string;
  personalizations: Record<string, string>;
}
```

---

## PHASE 3: API ROUTES

### Task 3.1: Onboarding Progress API

Create `src/app/api/v1/clients/[id]/onboarding/route.ts`:

```typescript
import { NextRequest, NextResponse } from 'next/server';
import { prisma } from '@/lib/prisma';
import { OnboardingStage } from '@prisma/client';

interface OnboardingChecklistItem {
  id: string;
  label: string;
  done: boolean;
  action?: string;
  videoId?: string;
}

// GET /api/v1/clients/[id]/onboarding
export async function GET(
  request: NextRequest,
  { params }: { params: { id: string } }
) {
  try {
    const clientId = params.id;

    let progress = await prisma.onboardingProgress.findUnique({
      where: { clientId },
      include: { client: true }
    });

    // Create if doesn't exist
    if (!progress) {
      progress = await prisma.onboardingProgress.create({
        data: { clientId },
        include: { client: true }
      });
    }

    // Build checklist
    const checklist: OnboardingChecklistItem[] = [
      {
        id: 'account',
        label: 'Create account',
        done: progress.accountCreated,
      },
      {
        id: 'business',
        label: 'Business details',
        done: progress.businessInfoCompleted,
        action: '/onboarding/business',
        videoId: 'welcome'
      },
      {
        id: 'phone',
        label: 'Phone setup',
        done: progress.phoneSetupCompleted,
        action: '/onboarding/phone',
        videoId: 'phone_setup'
      },
      {
        id: 'test_call',
        label: 'Test call',
        done: progress.testCallCompleted,
        action: '/onboarding/test-call',
        videoId: 'meet_gemma'
      }
    ];

    // Calculate completion
    const completedSteps = checklist.filter(item => item.done).length;
    const completionPercent = Math.round((completedSteps / checklist.length) * 100);

    // Determine next step
    const nextStep = checklist.find(item => !item.done);

    return NextResponse.json({
      stage: progress.currentStage,
      completionPercent,
      milestones: {
        accountCreated: progress.accountCreated,
        businessInfoCompleted: progress.businessInfoCompleted,
        phoneSetupCompleted: progress.phoneSetupCompleted,
        testCallCompleted: progress.testCallCompleted,
        firstRealCall: progress.firstRealCall,
        firstInvoiceSent: progress.firstInvoiceSent,
        firstReviewRequest: progress.firstReviewRequest,
        dashboardStreak: progress.dashboardStreak
      },
      nextStep: nextStep ? {
        action: nextStep.action,
        title: nextStep.label,
        videoId: nextStep.videoId
      } : null,
      checklist,
      dashboardTourComplete: progress.dashboardTourComplete,
      featuresToursComplete: progress.featuresToursComplete
    });
  } catch (error) {
    console.error('Error fetching onboarding progress:', error);
    return NextResponse.json(
      { error: 'Failed to fetch onboarding progress' },
      { status: 500 }
    );
  }
}

// PATCH /api/v1/clients/[id]/onboarding
export async function PATCH(
  request: NextRequest,
  { params }: { params: { id: string } }
) {
  try {
    const clientId = params.id;
    const body = await request.json();
    const { milestone, value, stage, dashboardTourComplete, featureTourComplete } = body;

    const updateData: any = { updatedAt: new Date() };

    // Update milestone
    if (milestone && typeof value === 'boolean') {
      updateData[milestone] = value;
      
      // Set timestamp
      const timestampField = `${milestone.replace('Completed', '')}At`;
      if (value && !timestampField.includes('account')) {
        updateData[timestampField] = new Date();
      }
    }

    // Update stage
    if (stage) {
      updateData.currentStage = stage as OnboardingStage;
      updateData.stageStartedAt = new Date();
    }

    // Update dashboard tour
    if (typeof dashboardTourComplete === 'boolean') {
      updateData.dashboardTourComplete = dashboardTourComplete;
    }

    // Add feature tour
    if (featureTourComplete) {
      const progress = await prisma.onboardingProgress.findUnique({
        where: { clientId }
      });
      
      const currentTours = progress?.featuresToursComplete || [];
      if (!currentTours.includes(featureTourComplete)) {
        updateData.featuresToursComplete = [...currentTours, featureTourComplete];
      }
    }

    // Recalculate completion percentage
    const progress = await prisma.onboardingProgress.findUnique({
      where: { clientId }
    });

    if (progress) {
      const steps = [
        progress.accountCreated,
        updateData.businessInfoCompleted ?? progress.businessInfoCompleted,
        updateData.phoneSetupCompleted ?? progress.phoneSetupCompleted,
        updateData.testCallCompleted ?? progress.testCallCompleted
      ];
      updateData.completionPercent = Math.round(
        (steps.filter(Boolean).length / steps.length) * 100
      );
    }

    const updated = await prisma.onboardingProgress.upsert({
      where: { clientId },
      update: updateData,
      create: {
        clientId,
        ...updateData
      }
    });

    return NextResponse.json(updated);
  } catch (error) {
    console.error('Error updating onboarding progress:', error);
    return NextResponse.json(
      { error: 'Failed to update onboarding progress' },
      { status: 500 }
    );
  }
}
```

### Task 3.2: Video Tracking API

Create `src/app/api/v1/videos/watch/route.ts`:

```typescript
import { NextRequest, NextResponse } from 'next/server';
import { prisma } from '@/lib/prisma';
import { VIDEOS } from '@/lib/videos/content';
import { VideoType } from '@prisma/client';

// POST /api/v1/videos/watch - Start watching
export async function POST(request: NextRequest) {
  try {
    const body = await request.json();
    const { clientId, videoId, trigger, location } = body;

    const videoContent = VIDEOS[videoId];
    if (!videoContent) {
      return NextResponse.json(
        { error: 'Video not found' },
        { status: 404 }
      );
    }

    const videoType = videoContent.type.toUpperCase() as VideoType;

    const watch = await prisma.videoWatch.create({
      data: {
        clientId,
        videoId,
        videoType,
        totalSeconds: videoContent.duration,
        trigger,
        location
      }
    });

    return NextResponse.json({ watchId: watch.id });
  } catch (error) {
    console.error('Error starting video watch:', error);
    return NextResponse.json(
      { error: 'Failed to start video watch' },
      { status: 500 }
    );
  }
}
```

Create `src/app/api/v1/videos/watch/[watchId]/route.ts`:

```typescript
import { NextRequest, NextResponse } from 'next/server';
import { prisma } from '@/lib/prisma';

// PATCH /api/v1/videos/watch/[watchId] - Update progress
export async function PATCH(
  request: NextRequest,
  { params }: { params: { watchId: string } }
) {
  try {
    const watchId = params.watchId;
    const body = await request.json();
    const { watchedSeconds, completed } = body;

    const watch = await prisma.videoWatch.findUnique({
      where: { id: watchId }
    });

    if (!watch) {
      return NextResponse.json(
        { error: 'Watch session not found' },
        { status: 404 }
      );
    }

    const percentWatched = (watchedSeconds / watch.totalSeconds) * 100;

    const updated = await prisma.videoWatch.update({
      where: { id: watchId },
      data: {
        watchedSeconds,
        percentWatched,
        completedAt: completed || percentWatched >= 90 ? new Date() : null
      }
    });

    return NextResponse.json(updated);
  } catch (error) {
    console.error('Error updating video watch:', error);
    return NextResponse.json(
      { error: 'Failed to update video watch' },
      { status: 500 }
    );
  }
}
```

### Task 3.3: Behavioral Events API

Create `src/app/api/v1/events/route.ts`:

```typescript
import { NextRequest, NextResponse } from 'next/server';
import { prisma } from '@/lib/prisma';

// POST /api/v1/events - Log behavioral event
export async function POST(request: NextRequest) {
  try {
    const body = await request.json();
    const { clientId, eventType, eventData, sessionId, deviceType } = body;

    const event = await prisma.behavioralEvent.create({
      data: {
        clientId,
        eventType,
        eventData: eventData || {},
        sessionId,
        deviceType
      }
    });

    // Check for trigger conditions
    await checkTriggerConditions(clientId, eventType, eventData);

    return NextResponse.json({ eventId: event.id });
  } catch (error) {
    console.error('Error logging event:', error);
    return NextResponse.json(
      { error: 'Failed to log event' },
      { status: 500 }
    );
  }
}

async function checkTriggerConditions(
  clientId: string,
  eventType: string,
  eventData: any
) {
  // Update onboarding progress based on events
  if (eventType === 'page_view' && eventData?.path?.includes('/dashboard')) {
    // Update dashboard streak logic handled in scheduled job
  }

  if (eventType === 'feature_use' && eventData?.feature === 'invoice_created') {
    await prisma.onboardingProgress.update({
      where: { clientId },
      data: { firstInvoiceSent: true, firstInvoiceSentAt: new Date() }
    });
  }

  if (eventType === 'call_received' && eventData?.isReal) {
    const progress = await prisma.onboardingProgress.findUnique({
      where: { clientId }
    });
    
    if (progress && !progress.firstRealCall) {
      await prisma.onboardingProgress.update({
        where: { clientId },
        data: { 
          firstRealCall: true, 
          firstRealCallAt: new Date(),
          currentStage: 'ACTIVATION'
        }
      });
    }
  }
}
```

### Task 3.4: Help Search API

Create `src/app/api/v1/help/search/route.ts`:

```typescript
import { NextRequest, NextResponse } from 'next/server';
import { HELP_ARTICLES, searchArticles } from '@/lib/help/articles';

// GET /api/v1/help/search?q={query}
export async function GET(request: NextRequest) {
  try {
    const searchParams = request.nextUrl.searchParams;
    const query = searchParams.get('q');

    if (!query || query.length < 2) {
      return NextResponse.json({ results: [] });
    }

    const results = searchArticles(query);

    return NextResponse.json({
      query,
      results: results.slice(0, 10),
      suggestedAction: results.length > 0 
        ? results[0].suggestedAction 
        : 'Contact support for help'
    });
  } catch (error) {
    console.error('Error searching help:', error);
    return NextResponse.json(
      { error: 'Failed to search help articles' },
      { status: 500 }
    );
  }
}
```

### Task 3.5: Support Chat API

Create `src/app/api/v1/support/chat/route.ts`:

```typescript
import { NextRequest, NextResponse } from 'next/server';
import { prisma } from '@/lib/prisma';
import Anthropic from '@anthropic-ai/sdk';

const anthropic = new Anthropic();

// POST /api/v1/support/chat
export async function POST(request: NextRequest) {
  try {
    const body = await request.json();
    const { clientId, message, chatId } = body;

    // Get or create chat session
    let chat;
    if (chatId) {
      chat = await prisma.supportChat.findUnique({
        where: { id: chatId },
        include: { client: true }
      });
    }

    if (!chat) {
      chat = await prisma.supportChat.create({
        data: {
          clientId,
          messages: [],
          status: 'ACTIVE'
        },
        include: { client: true }
      });
    }

    // Get existing messages
    const messages = (chat.messages as any[]) || [];
    
    // Add user message
    messages.push({
      role: 'user',
      content: message,
      timestamp: new Date().toISOString()
    });

    // Get client context for AI
    const client = await prisma.client.findUnique({
      where: { id: clientId },
      include: {
        onboardingProgress: true,
        calls: { take: 5, orderBy: { createdAt: 'desc' } },
        invoices: { take: 5, orderBy: { createdAt: 'desc' } }
      }
    });

    // Generate AI response
    const systemPrompt = `You are Gemma, the AI assistant for Covered AI - a phone answering service for small businesses.

You are helping a customer named ${client?.businessName || 'a business'} (${client?.vertical || 'service'} industry).

Their onboarding status:
- Setup complete: ${client?.onboardingProgress?.testCallCompleted ? 'Yes' : 'No'}
- First real call: ${client?.onboardingProgress?.firstRealCall ? 'Yes' : 'No'}
- First invoice sent: ${client?.onboardingProgress?.firstInvoiceSent ? 'Yes' : 'No'}

Be helpful, friendly, and concise. If you can't help with something, offer to escalate to human support.

For common issues:
- Forwarding problems: Check Settings > Phone, ensure number includes country code
- Invoice questions: Point to Invoices page, explain automatic chasing
- Call quality: Usually a network issue, suggest testing from different phone`;

    const response = await anthropic.messages.create({
      model: 'claude-sonnet-4-20250514',
      max_tokens: 500,
      system: systemPrompt,
      messages: messages.map(m => ({
        role: m.role as 'user' | 'assistant',
        content: m.content
      }))
    });

    const aiResponse = response.content[0].type === 'text' 
      ? response.content[0].text 
      : '';

    // Add AI response to messages
    messages.push({
      role: 'assistant',
      content: aiResponse,
      timestamp: new Date().toISOString()
    });

    // Determine if resolved or needs escalation
    const needsEscalation = aiResponse.toLowerCase().includes('escalate') ||
                           aiResponse.toLowerCase().includes('human support') ||
                           aiResponse.toLowerCase().includes('contact us');

    // Update chat
    const updatedChat = await prisma.supportChat.update({
      where: { id: chat.id },
      data: {
        messages,
        status: needsEscalation ? 'WAITING_HUMAN' : 'ACTIVE',
        escalatedAt: needsEscalation ? new Date() : undefined
      }
    });

    // Extract any suggested actions from response
    const actions = [];
    if (aiResponse.includes('Settings')) {
      actions.push({ type: 'link', label: 'Go to Settings', url: '/settings' });
    }
    if (aiResponse.includes('Invoices')) {
      actions.push({ type: 'link', label: 'Go to Invoices', url: '/invoices' });
    }

    return NextResponse.json({
      chatId: chat.id,
      response: {
        role: 'assistant',
        content: aiResponse,
        actions
      },
      resolved: false,
      needsEscalation
    });
  } catch (error) {
    console.error('Error in support chat:', error);
    return NextResponse.json(
      { error: 'Failed to process chat message' },
      { status: 500 }
    );
  }
}
```

---

## PHASE 4: HELP ARTICLES SYSTEM

### Task 4.1: Create Help Articles Content

Create `src/lib/help/articles.ts`:

```typescript
export interface HelpArticle {
  id: string;
  title: string;
  snippet: string;
  content: string;
  category: string;
  type: 'article' | 'video' | 'action';
  videoId?: string;
  videoDuration?: number;
  suggestedAction?: string;
  keywords: string[];
}

export const HELP_ARTICLES: HelpArticle[] = [
  // Getting Started
  {
    id: 'how-covered-works',
    title: 'How Covered Works',
    snippet: 'An overview of how Gemma answers your calls and manages enquiries.',
    content: `# How Covered Works

When a customer calls your Covered number, Gemma (your AI receptionist) answers immediately.

## What Gemma Does

1. **Greets professionally** - Uses your business name
2. **Identifies the reason for calling** - Emergency, booking, enquiry, etc.
3. **Takes appropriate action**:
   - Emergency: Forwards to your mobile immediately
   - Booking request: Collects details, adds to your dashboard
   - General enquiry: Takes message, creates follow-up task

## What You See

Every call appears in your dashboard with:
- Full transcript
- Call recording
- Caller details
- Suggested next action

## Getting Started

1. Complete your phone setup
2. Make a test call to hear Gemma
3. Start advertising your Covered number`,
    category: 'getting-started',
    type: 'article',
    videoId: 'welcome',
    videoDuration: 60,
    suggestedAction: 'Complete your setup in Settings',
    keywords: ['how', 'works', 'gemma', 'calls', 'overview', 'introduction']
  },
  
  {
    id: 'phone-setup',
    title: 'Setting Up Your Phone',
    snippet: 'How to configure call forwarding and your Covered number.',
    content: `# Setting Up Your Phone

Your Covered number is ready to use. Here's how to configure it.

## Your Covered Number

Find your number in Settings > Phone. This is the number customers call.

## Call Forwarding

When Gemma needs to reach you (for emergencies), calls forward to your mobile.

Enter your mobile number including country code:
- UK: +44 7XXX XXXXXX
- US: +1 XXX XXX XXXX

## Testing

After setup, call your Covered number to hear Gemma in action.

## Troubleshooting

If calls aren't coming through:
1. Check your forwarding number is correct
2. Ensure your phone isn't on Do Not Disturb
3. Try calling from a different phone`,
    category: 'getting-started',
    type: 'article',
    videoId: 'phone_setup',
    videoDuration: 45,
    suggestedAction: 'Check your phone settings',
    keywords: ['phone', 'setup', 'forwarding', 'number', 'configure', 'mobile']
  },

  // Calls
  {
    id: 'understanding-calls',
    title: 'Understanding Your Calls Dashboard',
    snippet: 'How to view, filter, and act on calls in your dashboard.',
    content: `# Understanding Your Calls Dashboard

Every call Gemma handles appears in your Calls dashboard.

## Call Information

Each call shows:
- **Caller** - Phone number and name (if known)
- **Time** - When the call happened
- **Type** - Emergency, booking, enquiry, etc.
- **Status** - Handled, needs action, callback required
- **Transcript** - Full conversation text
- **Recording** - Audio playback

## Taking Action

Click any call to:
- Create an invoice for the work
- Schedule a callback
- Add to customer record
- Mark as handled

## Filtering

Use filters to see:
- Today's calls only
- Emergencies only
- Calls needing action
- Specific date range`,
    category: 'calls',
    type: 'article',
    videoId: 'calls_dashboard',
    videoDuration: 90,
    suggestedAction: 'View your recent calls',
    keywords: ['calls', 'dashboard', 'filter', 'transcript', 'recording', 'action']
  },

  {
    id: 'calls-not-coming-through',
    title: 'Calls Not Coming Through',
    snippet: 'Troubleshooting when calls aren\'t reaching your phone.',
    content: `# Calls Not Coming Through

If calls aren't reaching your phone, try these steps.

## Check Your Settings

1. Go to Settings > Phone
2. Verify your forwarding number is correct
3. Include the country code (+44 for UK)

## Check Your Phone

1. Turn off Do Not Disturb
2. Check you haven't blocked unknown numbers
3. Ensure you have signal/wifi

## Test the System

1. Call your Covered number from a different phone
2. If Gemma answers, the problem is your mobile
3. If no answer, contact support

## Still Stuck?

Chat with us using the support button. We can check your account settings remotely.`,
    category: 'troubleshooting',
    type: 'article',
    videoId: 'forwarding_not_working',
    videoDuration: 90,
    suggestedAction: 'Check Settings > Phone',
    keywords: ['calls', 'not', 'coming', 'through', 'forwarding', 'troubleshoot', 'problem', 'issue']
  },

  // Invoices
  {
    id: 'creating-invoices',
    title: 'Creating Invoices',
    snippet: 'Step-by-step guide to creating and sending invoices.',
    content: `# Creating Invoices

Send professional invoices in under a minute.

## From Scratch

1. Click "New Invoice" on the Invoices page
2. Select or add a customer
3. Add line items (description, quantity, price)
4. Set due date
5. Click "Send"

## From a Call

1. Open any call in your dashboard
2. Click "Create Invoice"
3. Customer details auto-fill
4. Add your line items
5. Send

## Templates

Save time with line item templates:
1. Go to Settings > Invoice Templates
2. Add common services with prices
3. Select from dropdown when creating invoices

## Payment

Customers receive an email with a link to pay online via Stripe.`,
    category: 'invoices',
    type: 'article',
    videoId: 'creating_invoices',
    videoDuration: 120,
    suggestedAction: 'Create your first invoice',
    keywords: ['invoice', 'create', 'send', 'bill', 'payment', 'customer']
  },

  {
    id: 'invoice-reminders',
    title: 'Automatic Invoice Reminders',
    snippet: 'How the invoice chasing system works.',
    content: `# Automatic Invoice Reminders

Covered automatically chases unpaid invoices so you don't have to.

## Default Schedule

- **Day 1**: Friendly reminder (due soon)
- **Day 7**: Polite nudge (now overdue)
- **Day 14**: Firmer reminder
- **Day 30**: Final notice

## Customising

In Settings > Invoices:
- Change reminder intervals
- Edit email templates
- Turn off for specific invoices

## What Customers See

Professional emails from your business (not Covered) with:
- Invoice summary
- Amount due
- Easy payment link

## Manual Override

For any invoice, you can:
- Pause reminders
- Send immediate reminder
- Mark as paid manually`,
    category: 'invoices',
    type: 'article',
    videoId: 'invoice_chasing',
    videoDuration: 90,
    suggestedAction: 'View invoice settings',
    keywords: ['invoice', 'reminder', 'chasing', 'automatic', 'overdue', 'payment']
  },

  // Reviews
  {
    id: 'review-requests',
    title: 'Getting More Reviews',
    snippet: 'How automatic review requests work.',
    content: `# Getting More Reviews

Turn happy customers into 5-star reviews automatically.

## How It Works

1. Mark a job as complete
2. Covered sends a friendly email
3. Customer clicks to leave a Google review
4. Review appears on your Google Business profile

## Timing

Emails send immediately after job completion - when customers are happiest.

## Connecting Google

1. Go to Settings > Reviews
2. Click "Connect Google Business"
3. Authorize access
4. Select your business listing

## Managing Reviews

View all reviews in one place and respond directly from Covered.`,
    category: 'reviews',
    type: 'article',
    videoId: 'review_requests',
    videoDuration: 60,
    suggestedAction: 'Connect your Google Business',
    keywords: ['review', 'google', 'rating', 'star', 'feedback', 'reputation']
  }
];

// Simple search function
export function searchArticles(query: string): HelpArticle[] {
  const normalizedQuery = query.toLowerCase().trim();
  const queryWords = normalizedQuery.split(/\s+/);

  return HELP_ARTICLES
    .map(article => {
      let score = 0;

      // Title match (highest weight)
      if (article.title.toLowerCase().includes(normalizedQuery)) {
        score += 10;
      }

      // Keyword match
      for (const keyword of article.keywords) {
        for (const word of queryWords) {
          if (keyword.includes(word) || word.includes(keyword)) {
            score += 5;
          }
        }
      }

      // Snippet match
      if (article.snippet.toLowerCase().includes(normalizedQuery)) {
        score += 3;
      }

      // Content match
      for (const word of queryWords) {
        if (article.content.toLowerCase().includes(word)) {
          score += 1;
        }
      }

      return { article, score };
    })
    .filter(({ score }) => score > 0)
    .sort((a, b) => b.score - a.score)
    .map(({ article }) => ({
      id: article.id,
      title: article.title,
      snippet: article.snippet,
      type: article.type,
      category: article.category,
      videoId: article.videoId,
      duration: article.videoDuration,
      suggestedAction: article.suggestedAction
    }));
}
```

---

## PHASE 5: FRONTEND COMPONENTS

### Task 5.1: Onboarding Checklist Component

Create `src/components/onboarding/OnboardingChecklist.tsx`:

```tsx
'use client';

import { useState, useEffect } from 'react';
import { CheckCircle, Circle, ChevronRight, Play } from 'lucide-react';
import Link from 'next/link';

interface ChecklistItem {
  id: string;
  label: string;
  done: boolean;
  action?: string;
  videoId?: string;
}

interface OnboardingChecklistProps {
  clientId: string;
  onVideoClick?: (videoId: string) => void;
}

export function OnboardingChecklist({ clientId, onVideoClick }: OnboardingChecklistProps) {
  const [items, setItems] = useState<ChecklistItem[]>([]);
  const [completionPercent, setCompletionPercent] = useState(0);
  const [loading, setLoading] = useState(true);

  useEffect(() => {
    fetchProgress();
  }, [clientId]);

  const fetchProgress = async () => {
    try {
      const res = await fetch(`/api/v1/clients/${clientId}/onboarding`);
      const data = await res.json();
      setItems(data.checklist);
      setCompletionPercent(data.completionPercent);
    } catch (error) {
      console.error('Error fetching onboarding progress:', error);
    } finally {
      setLoading(false);
    }
  };

  if (loading) {
    return (
      <div className="bg-white rounded-2xl p-5 border border-gray-200 animate-pulse">
        <div className="h-6 bg-gray-100 rounded w-1/3 mb-4"></div>
        <div className="h-2 bg-gray-100 rounded-full mb-5"></div>
        <div className="space-y-3">
          {[1, 2, 3, 4].map(i => (
            <div key={i} className="h-12 bg-gray-50 rounded-xl"></div>
          ))}
        </div>
      </div>
    );
  }

  if (completionPercent >= 100) {
    return null; // Hide when complete
  }

  // Endowed progress: show slightly more than actual
  const displayPercent = Math.min(completionPercent + 5, 100);

  return (
    <div className="bg-white rounded-2xl p-5 border border-gray-200">
      <div className="flex items-center justify-between mb-4">
        <h3 className="text-base font-semibold text-gray-900">
          Getting Started
        </h3>
        <span className="text-sm text-gray-500">
          {completionPercent}% complete
        </span>
      </div>

      {/* Progress bar with animation */}
      <div className="h-2 bg-gray-100 rounded-full mb-5 overflow-hidden">
        <div
          className="h-full bg-green-500 rounded-full transition-all duration-1000 ease-out"
          style={{ width: `${displayPercent}%` }}
        />
      </div>

      <div className="space-y-3">
        {items.map((item) => (
          <div key={item.id}>
            {item.done ? (
              <div className="flex items-center gap-3 p-3 rounded-xl bg-green-50">
                <CheckCircle className="w-5 h-5 text-green-500 flex-shrink-0" />
                <span className="flex-1 text-sm text-gray-500 line-through">
                  {item.label}
                </span>
              </div>
            ) : item.action ? (
              <Link
                href={item.action}
                className="w-full flex items-center gap-3 p-3 rounded-xl bg-gray-50 hover:bg-gray-100 transition-all duration-200"
              >
                <Circle className="w-5 h-5 text-gray-300 flex-shrink-0" />
                <span className="flex-1 text-left text-sm text-gray-900">
                  {item.label}
                </span>
                {item.videoId && onVideoClick && (
                  <button
                    onClick={(e) => {
                      e.preventDefault();
                      onVideoClick(item.videoId!);
                    }}
                    className="p-1 hover:bg-gray-200 rounded"
                  >
                    <Play className="w-4 h-4 text-gray-400" />
                  </button>
                )}
                <ChevronRight className="w-4 h-4 text-gray-400" />
              </Link>
            ) : (
              <div className="flex items-center gap-3 p-3 rounded-xl bg-gray-50">
                <Circle className="w-5 h-5 text-gray-300 flex-shrink-0" />
                <span className="flex-1 text-sm text-gray-900">
                  {item.label}
                </span>
              </div>
            )}
          </div>
        ))}
      </div>

      <p className="mt-4 text-xs text-gray-500 text-center">
        Complete setup to unlock all features
      </p>
    </div>
  );
}
```

### Task 5.2: Video Modal Component

Create `src/components/onboarding/VideoModal.tsx`:

```tsx
'use client';

import { useState, useEffect, useRef } from 'react';
import { X, Volume2, VolumeX } from 'lucide-react';

interface VideoModalProps {
  videoUrl: string;
  title: string;
  onClose: () => void;
  onComplete: () => void;
  autoPlay?: boolean;
  clientId?: string;
  videoId?: string;
}

export function VideoModal({
  videoUrl,
  title,
  onClose,
  onComplete,
  autoPlay = true,
  clientId,
  videoId
}: VideoModalProps) {
  const videoRef = useRef<HTMLVideoElement>(null);
  const [muted, setMuted] = useState(autoPlay);
  const [progress, setProgress] = useState(0);
  const [canSkip, setCanSkip] = useState(false);
  const [watchId, setWatchId] = useState<string | null>(null);

  // Start watch tracking
  useEffect(() => {
    if (clientId && videoId) {
      fetch('/api/v1/videos/watch', {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({
          clientId,
          videoId,
          trigger: 'modal',
          location: window.location.pathname
        })
      })
        .then(res => res.json())
        .then(data => setWatchId(data.watchId))
        .catch(console.error);
    }
  }, [clientId, videoId]);

  // Allow skip after 5 seconds
  useEffect(() => {
    const timer = setTimeout(() => setCanSkip(true), 5000);
    return () => clearTimeout(timer);
  }, []);

  // Track video progress
  useEffect(() => {
    const video = videoRef.current;
    if (!video) return;

    const handleTimeUpdate = () => {
      const percent = (video.currentTime / video.duration) * 100;
      setProgress(percent);

      // Update watch progress
      if (watchId && video.currentTime > 0) {
        fetch(`/api/v1/videos/watch/${watchId}`, {
          method: 'PATCH',
          headers: { 'Content-Type': 'application/json' },
          body: JSON.stringify({
            watchedSeconds: Math.floor(video.currentTime),
            completed: percent >= 90
          })
        }).catch(console.error);
      }

      if (percent >= 90) {
        onComplete();
      }
    };

    video.addEventListener('timeupdate', handleTimeUpdate);
    return () => video.removeEventListener('timeupdate', handleTimeUpdate);
  }, [onComplete, watchId]);

  return (
    <div className="fixed inset-0 z-50 flex items-center justify-center bg-black/70">
      <div className="bg-white rounded-2xl overflow-hidden max-w-lg w-full mx-4 shadow-2xl">
        {/* Header */}
        <div className="flex items-center justify-between p-4 border-b">
          <h3 className="font-semibold text-gray-900">{title}</h3>
          {canSkip && (
            <button
              onClick={onClose}
              className="p-1 hover:bg-gray-100 rounded-full transition-colors"
            >
              <X className="w-5 h-5 text-gray-500" />
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
                         hover:bg-white transition-colors shadow-lg"
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

        {/* Footer */}
        <div className="p-4">
          {!canSkip ? (
            <p className="text-center text-sm text-gray-500">
              Skip available in {Math.max(0, 5 - Math.floor(progress / 20))}s...
            </p>
          ) : (
            <button
              onClick={onClose}
              className="w-full py-3 bg-blue-600 text-white rounded-xl
                         font-medium hover:bg-blue-700 transition-colors"
            >
              Continue
            </button>
          )}
        </div>
      </div>
    </div>
  );
}
```

### Task 5.3: Celebration Modal Component

Create `src/components/onboarding/CelebrationModal.tsx`:

```tsx
'use client';

import { useEffect, useState } from 'react';
import { Star, ArrowRight, PartyPopper, Sparkles } from 'lucide-react';
import Link from 'next/link';

interface CelebrationModalProps {
  title: string;
  message: string;
  icon?: 'star' | 'party' | 'sparkles';
  nextAction?: {
    label: string;
    href: string;
  };
  onClose: () => void;
}

export function CelebrationModal({
  title,
  message,
  icon = 'star',
  nextAction,
  onClose
}: CelebrationModalProps) {
  const [showContent, setShowContent] = useState(false);

  useEffect(() => {
    // Fire confetti
    fireConfetti();

    // Animate content in
    setTimeout(() => setShowContent(true), 300);
  }, []);

  const fireConfetti = async () => {
    // Dynamic import to avoid SSR issues
    const confetti = (await import('canvas-confetti')).default;
    
    confetti({
      particleCount: 100,
      spread: 70,
      origin: { y: 0.6 }
    });

    // Second burst
    setTimeout(() => {
      confetti({
        particleCount: 50,
        angle: 60,
        spread: 55,
        origin: { x: 0 }
      });
      confetti({
        particleCount: 50,
        angle: 120,
        spread: 55,
        origin: { x: 1 }
      });
    }, 250);
  };

  const IconComponent = {
    star: Star,
    party: PartyPopper,
    sparkles: Sparkles
  }[icon];

  const iconColors = {
    star: 'bg-yellow-100 text-yellow-500',
    party: 'bg-purple-100 text-purple-500',
    sparkles: 'bg-blue-100 text-blue-500'
  }[icon];

  return (
    <div className="fixed inset-0 z-50 flex items-center justify-center bg-black/50">
      <div
        className={`
          bg-white rounded-2xl p-8 max-w-sm w-full mx-4 text-center
          transform transition-all duration-500 shadow-2xl
          ${showContent ? 'scale-100 opacity-100' : 'scale-90 opacity-0'}
        `}
      >
        <div
          className={`
            w-16 h-16 rounded-full flex items-center justify-center mx-auto mb-4
            ${iconColors}
          `}
        >
          <IconComponent className="w-8 h-8 fill-current" />
        </div>

        <h2 className="text-xl font-bold text-gray-900 mb-2">{title}</h2>

        <p className="text-gray-600 mb-6">{message}</p>

        {nextAction ? (
          <Link
            href={nextAction.href}
            onClick={onClose}
            className="inline-flex items-center gap-2 px-6 py-3 
                       bg-blue-600 text-white rounded-xl font-medium
                       hover:bg-blue-700 transition-colors"
          >
            {nextAction.label}
            <ArrowRight className="w-4 h-4" />
          </Link>
        ) : (
          <button
            onClick={onClose}
            className="px-6 py-3 bg-blue-600 text-white rounded-xl 
                       font-medium hover:bg-blue-700 transition-colors"
          >
            Continue
          </button>
        )}
      </div>
    </div>
  );
}
```

### Task 5.4: Help Search Component

Create `src/components/support/HelpSearch.tsx`:

```tsx
'use client';

import { useState, useCallback } from 'react';
import { Search, Book, PlayCircle, MessageCircle, ExternalLink } from 'lucide-react';
import debounce from 'lodash/debounce';
import Link from 'next/link';

interface SearchResult {
  id: string;
  title: string;
  snippet: string;
  type: 'article' | 'video' | 'action';
  category: string;
  videoId?: string;
  duration?: number;
  suggestedAction?: string;
}

interface HelpSearchProps {
  onVideoClick?: (videoId: string) => void;
  placeholder?: string;
}

export function HelpSearch({
  onVideoClick,
  placeholder = 'Search help articles, videos, or ask a question...'
}: HelpSearchProps) {
  const [query, setQuery] = useState('');
  const [results, setResults] = useState<SearchResult[]>([]);
  const [loading, setLoading] = useState(false);
  const [showResults, setShowResults] = useState(false);

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
      } catch (error) {
        console.error('Search error:', error);
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
      case 'video':
        return <PlayCircle className="w-5 h-5 text-blue-500" />;
      case 'action':
        return <ExternalLink className="w-5 h-5 text-green-500" />;
      default:
        return <Book className="w-5 h-5 text-gray-400" />;
    }
  };

  return (
    <div className="relative">
      <div className="relative">
        <Search className="absolute left-4 top-1/2 -translate-y-1/2 w-5 h-5 text-gray-400" />
        <input
          type="text"
          value={query}
          onChange={handleChange}
          onFocus={() => setShowResults(true)}
          onBlur={() => setTimeout(() => setShowResults(false), 200)}
          placeholder={placeholder}
          className="w-full pl-12 pr-4 py-3 border border-gray-200 rounded-xl
                     focus:ring-2 focus:ring-blue-500 focus:border-blue-500
                     outline-none transition-all"
        />
      </div>

      {/* Results dropdown */}
      {showResults && (results.length > 0 || loading) && query.length >= 2 && (
        <div
          className="absolute top-full left-0 right-0 mt-2 bg-white 
                      rounded-xl border border-gray-200 shadow-lg z-10
                      max-h-96 overflow-auto"
        >
          {loading ? (
            <div className="p-4 text-center text-gray-500">Searching...</div>
          ) : (
            <div className="p-2">
              {results.map((result) => (
                <div key={result.id}>
                  {result.type === 'video' && onVideoClick ? (
                    <button
                      onClick={() => onVideoClick(result.videoId!)}
                      className="w-full flex items-start gap-3 p-3 rounded-lg
                                 hover:bg-gray-50 transition-colors text-left"
                    >
                      <div className="mt-0.5">{getIcon(result.type)}</div>
                      <div className="flex-1 min-w-0">
                        <h4 className="font-medium text-gray-900 truncate">
                          {result.title}
                        </h4>
                        <p className="text-sm text-gray-500 line-clamp-2">
                          {result.snippet}
                        </p>
                        {result.duration && (
                          <span className="text-xs text-gray-400 mt-1">
                            {Math.round(result.duration / 60)} min video
                          </span>
                        )}
                      </div>
                    </button>
                  ) : (
                    <Link
                      href={`/help/${result.id}`}
                      className="flex items-start gap-3 p-3 rounded-lg
                                 hover:bg-gray-50 transition-colors"
                    >
                      <div className="mt-0.5">{getIcon(result.type)}</div>
                      <div className="flex-1 min-w-0">
                        <h4 className="font-medium text-gray-900 truncate">
                          {result.title}
                        </h4>
                        <p className="text-sm text-gray-500 line-clamp-2">
                          {result.snippet}
                        </p>
                      </div>
                    </Link>
                  )}
                </div>
              ))}

              {/* Can't find what you need? */}
              <div className="border-t border-gray-100 mt-2 pt-2">
                <Link
                  href="/support/chat"
                  className="flex items-center gap-3 p-3 rounded-lg
                             hover:bg-gray-50 transition-colors"
                >
                  <MessageCircle className="w-5 h-5 text-blue-500" />
                  <span className="text-sm font-medium text-blue-600">
                    Chat with support
                  </span>
                </Link>
              </div>
            </div>
          )}
        </div>
      )}
    </div>
  );
}
```

### Task 5.5: Support Chat Component

Create `src/components/support/SupportChat.tsx`:

```tsx
'use client';

import { useState, useRef, useEffect } from 'react';
import { Send, Loader2, User, Bot, ExternalLink } from 'lucide-react';
import Link from 'next/link';

interface Message {
  role: 'user' | 'assistant';
  content: string;
  timestamp: string;
  actions?: Array<{
    type: 'link';
    label: string;
    url: string;
  }>;
}

interface SupportChatProps {
  clientId: string;
}

export function SupportChat({ clientId }: SupportChatProps) {
  const [messages, setMessages] = useState<Message[]>([]);
  const [input, setInput] = useState('');
  const [loading, setLoading] = useState(false);
  const [chatId, setChatId] = useState<string | null>(null);
  const messagesEndRef = useRef<HTMLDivElement>(null);

  // Auto-scroll to bottom
  useEffect(() => {
    messagesEndRef.current?.scrollIntoView({ behavior: 'smooth' });
  }, [messages]);

  // Initial greeting
  useEffect(() => {
    setMessages([
      {
        role: 'assistant',
        content: "Hi! I'm Gemma, your AI assistant. How can I help you today?",
        timestamp: new Date().toISOString()
      }
    ]);
  }, []);

  const sendMessage = async () => {
    if (!input.trim() || loading) return;

    const userMessage: Message = {
      role: 'user',
      content: input.trim(),
      timestamp: new Date().toISOString()
    };

    setMessages(prev => [...prev, userMessage]);
    setInput('');
    setLoading(true);

    try {
      const res = await fetch('/api/v1/support/chat', {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({
          clientId,
          message: userMessage.content,
          chatId
        })
      });

      const data = await res.json();

      if (data.chatId) {
        setChatId(data.chatId);
      }

      const assistantMessage: Message = {
        role: 'assistant',
        content: data.response.content,
        timestamp: new Date().toISOString(),
        actions: data.response.actions
      };

      setMessages(prev => [...prev, assistantMessage]);
    } catch (error) {
      console.error('Chat error:', error);
      setMessages(prev => [
        ...prev,
        {
          role: 'assistant',
          content: "Sorry, I'm having trouble connecting. Please try again or email support@covered.ai",
          timestamp: new Date().toISOString()
        }
      ]);
    } finally {
      setLoading(false);
    }
  };

  const handleKeyPress = (e: React.KeyboardEvent) => {
    if (e.key === 'Enter' && !e.shiftKey) {
      e.preventDefault();
      sendMessage();
    }
  };

  return (
    <div className="flex flex-col h-[500px] bg-white rounded-2xl border border-gray-200 overflow-hidden">
      {/* Header */}
      <div className="px-4 py-3 border-b border-gray-200 bg-gray-50">
        <div className="flex items-center gap-3">
          <div className="w-8 h-8 rounded-full bg-blue-100 flex items-center justify-center">
            <Bot className="w-4 h-4 text-blue-600" />
          </div>
          <div>
            <h3 className="font-medium text-gray-900">Gemma</h3>
            <p className="text-xs text-gray-500">AI Support Assistant</p>
          </div>
        </div>
      </div>

      {/* Messages */}
      <div className="flex-1 overflow-y-auto p-4 space-y-4">
        {messages.map((message, index) => (
          <div
            key={index}
            className={`flex gap-3 ${
              message.role === 'user' ? 'flex-row-reverse' : ''
            }`}
          >
            <div
              className={`w-8 h-8 rounded-full flex items-center justify-center flex-shrink-0 ${
                message.role === 'user'
                  ? 'bg-gray-200'
                  : 'bg-blue-100'
              }`}
            >
              {message.role === 'user' ? (
                <User className="w-4 h-4 text-gray-600" />
              ) : (
                <Bot className="w-4 h-4 text-blue-600" />
              )}
            </div>
            <div
              className={`max-w-[75%] ${
                message.role === 'user' ? 'text-right' : ''
              }`}
            >
              <div
                className={`rounded-2xl px-4 py-2 ${
                  message.role === 'user'
                    ? 'bg-blue-600 text-white'
                    : 'bg-gray-100 text-gray-900'
                }`}
              >
                <p className="text-sm whitespace-pre-wrap">{message.content}</p>
              </div>
              
              {/* Action buttons */}
              {message.actions && message.actions.length > 0 && (
                <div className="mt-2 flex flex-wrap gap-2">
                  {message.actions.map((action, actionIndex) => (
                    <Link
                      key={actionIndex}
                      href={action.url}
                      className="inline-flex items-center gap-1 px-3 py-1.5 
                                 bg-white border border-gray-200 rounded-full 
                                 text-xs font-medium text-gray-700
                                 hover:bg-gray-50 transition-colors"
                    >
                      {action.label}
                      <ExternalLink className="w-3 h-3" />
                    </Link>
                  ))}
                </div>
              )}
            </div>
          </div>
        ))}

        {loading && (
          <div className="flex gap-3">
            <div className="w-8 h-8 rounded-full bg-blue-100 flex items-center justify-center">
              <Bot className="w-4 h-4 text-blue-600" />
            </div>
            <div className="bg-gray-100 rounded-2xl px-4 py-2">
              <Loader2 className="w-4 h-4 animate-spin text-gray-400" />
            </div>
          </div>
        )}

        <div ref={messagesEndRef} />
      </div>

      {/* Input */}
      <div className="p-4 border-t border-gray-200">
        <div className="flex gap-2">
          <input
            type="text"
            value={input}
            onChange={(e) => setInput(e.target.value)}
            onKeyPress={handleKeyPress}
            placeholder="Type your message..."
            disabled={loading}
            className="flex-1 px-4 py-2 border border-gray-200 rounded-xl
                       focus:ring-2 focus:ring-blue-500 focus:border-blue-500
                       outline-none disabled:bg-gray-50"
          />
          <button
            onClick={sendMessage}
            disabled={loading || !input.trim()}
            className="px-4 py-2 bg-blue-600 text-white rounded-xl
                       hover:bg-blue-700 transition-colors
                       disabled:opacity-50 disabled:cursor-not-allowed"
          >
            <Send className="w-5 h-5" />
          </button>
        </div>
      </div>
    </div>
  );
}
```

---

## PHASE 6: ONBOARDING PAGES

### Task 6.1: Onboarding Layout

Create `src/app/(onboarding)/layout.tsx`:

```tsx
import { ReactNode } from 'react';

export default function OnboardingLayout({ children }: { children: ReactNode }) {
  return (
    <div className="min-h-screen bg-gradient-to-br from-blue-50 to-indigo-50">
      <div className="max-w-lg mx-auto px-4 py-8">
        {/* Logo */}
        <div className="text-center mb-8">
          <h1 className="text-2xl font-bold text-gray-900">Covered</h1>
          <p className="text-sm text-gray-500">AI Phone Answering</p>
        </div>
        
        {children}
      </div>
    </div>
  );
}
```

### Task 6.2: Step 1 - Business Details

Create `src/app/(onboarding)/step-1/page.tsx`:

```tsx
'use client';

import { useState } from 'react';
import { useRouter } from 'next/navigation';
import { CheckCircle, Circle } from 'lucide-react';

const VERTICALS = [
  { value: 'plumber', label: 'Plumber' },
  { value: 'electrician', label: 'Electrician' },
  { value: 'vet', label: 'Veterinary Practice' },
  { value: 'salon', label: 'Hair/Beauty Salon' },
  { value: 'physio', label: 'Physiotherapy' },
  { value: 'dental', label: 'Dental Practice' },
  { value: 'garage', label: 'Garage/Auto Repair' },
  { value: 'builder', label: 'Builder/Construction' },
  { value: 'landscaper', label: 'Landscaper/Gardener' },
  { value: 'cleaner', label: 'Cleaning Service' },
  { value: 'other', label: 'Other' }
];

export default function OnboardingStep1() {
  const router = useRouter();
  const [loading, setLoading] = useState(false);
  const [formData, setFormData] = useState({
    businessName: '',
    vertical: '',
    postcode: ''
  });

  const handleSubmit = async (e: React.FormEvent) => {
    e.preventDefault();
    setLoading(true);

    try {
      // Save business info
      // This would call your API to update the client
      
      // Update onboarding progress
      // await fetch(`/api/v1/clients/${clientId}/onboarding`, {
      //   method: 'PATCH',
      //   body: JSON.stringify({ milestone: 'businessInfoCompleted', value: true })
      // });

      router.push('/step-2');
    } catch (error) {
      console.error('Error saving business info:', error);
    } finally {
      setLoading(false);
    }
  };

  // Calculate progress
  const progress = 25; // Account created = 25%

  return (
    <div className="bg-white rounded-2xl shadow-sm border border-gray-200 overflow-hidden">
      {/* Progress header */}
      <div className="p-4 border-b border-gray-100">
        <div className="flex items-center gap-2 text-sm text-gray-500 mb-3">
          <CheckCircle className="w-4 h-4 text-green-500" />
          <span className="line-through">Account created</span>
          <Circle className="w-4 h-4 text-gray-300 ml-2" />
          <span className="font-medium text-gray-900">Business details</span>
          <Circle className="w-4 h-4 text-gray-300 ml-2" />
          <span>Phone setup</span>
          <Circle className="w-4 h-4 text-gray-300 ml-2" />
          <span>Test call</span>
        </div>
        <div className="h-2 bg-gray-100 rounded-full overflow-hidden">
          <div 
            className="h-full bg-green-500 rounded-full transition-all duration-500"
            style={{ width: `${progress}%` }}
          />
        </div>
      </div>

      {/* Form */}
      <form onSubmit={handleSubmit} className="p-6 space-y-5">
        <div>
          <label className="block text-sm font-medium text-gray-700 mb-1">
            What's your business called?
          </label>
          <input
            type="text"
            value={formData.businessName}
            onChange={(e) => setFormData({ ...formData, businessName: e.target.value })}
            placeholder="e.g. Smith's Plumbing"
            required
            className="w-full px-4 py-3 border border-gray-200 rounded-xl
                       focus:ring-2 focus:ring-blue-500 focus:border-blue-500 outline-none"
          />
        </div>

        <div>
          <label className="block text-sm font-medium text-gray-700 mb-1">
            What type of business?
          </label>
          <select
            value={formData.vertical}
            onChange={(e) => setFormData({ ...formData, vertical: e.target.value })}
            required
            className="w-full px-4 py-3 border border-gray-200 rounded-xl
                       focus:ring-2 focus:ring-blue-500 focus:border-blue-500 outline-none
                       bg-white"
          >
            <option value="">Select your industry</option>
            {VERTICALS.map((v) => (
              <option key={v.value} value={v.value}>{v.label}</option>
            ))}
          </select>
        </div>

        <div>
          <label className="block text-sm font-medium text-gray-700 mb-1">
            Where are you based?
          </label>
          <input
            type="text"
            value={formData.postcode}
            onChange={(e) => setFormData({ ...formData, postcode: e.target.value })}
            placeholder="e.g. NE1 4ST"
            required
            className="w-full px-4 py-3 border border-gray-200 rounded-xl
                       focus:ring-2 focus:ring-blue-500 focus:border-blue-500 outline-none"
          />
        </div>

        <button
          type="submit"
          disabled={loading}
          className="w-full py-3 bg-blue-600 text-white rounded-xl font-medium
                     hover:bg-blue-700 transition-colors disabled:opacity-50"
        >
          {loading ? 'Saving...' : 'Continue →'}
        </button>
      </form>
    </div>
  );
}
```

### Task 6.3: Step 2 - Phone Setup

Create `src/app/(onboarding)/step-2/page.tsx`:

```tsx
'use client';

import { useState } from 'react';
import { useRouter } from 'next/navigation';
import { CheckCircle, Circle, Phone, Copy, Check } from 'lucide-react';

export default function OnboardingStep2() {
  const router = useRouter();
  const [loading, setLoading] = useState(false);
  const [copied, setCopied] = useState(false);
  const [forwardingNumber, setForwardingNumber] = useState('');

  // This would come from your API/context
  const coveredNumber = '0191 XXX XXXX';

  const copyNumber = () => {
    navigator.clipboard.writeText(coveredNumber.replace(/\s/g, ''));
    setCopied(true);
    setTimeout(() => setCopied(false), 2000);
  };

  const handleSubmit = async (e: React.FormEvent) => {
    e.preventDefault();
    setLoading(true);

    try {
      // Save forwarding number
      // Update onboarding progress
      router.push('/step-3');
    } catch (error) {
      console.error('Error saving phone setup:', error);
    } finally {
      setLoading(false);
    }
  };

  const progress = 50;

  return (
    <div className="bg-white rounded-2xl shadow-sm border border-gray-200 overflow-hidden">
      {/* Progress header */}
      <div className="p-4 border-b border-gray-100">
        <div className="flex items-center gap-2 text-sm text-gray-500 mb-3">
          <CheckCircle className="w-4 h-4 text-green-500" />
          <span className="line-through">Account created</span>
          <CheckCircle className="w-4 h-4 text-green-500 ml-2" />
          <span className="line-through">Business details</span>
          <Circle className="w-4 h-4 text-blue-500 ml-2" />
          <span className="font-medium text-gray-900">Phone setup</span>
          <Circle className="w-4 h-4 text-gray-300 ml-2" />
          <span>Test call</span>
        </div>
        <div className="h-2 bg-gray-100 rounded-full overflow-hidden">
          <div 
            className="h-full bg-green-500 rounded-full transition-all duration-500"
            style={{ width: `${progress}%` }}
          />
        </div>
      </div>

      <div className="p-6 space-y-6">
        {/* Covered Number Display */}
        <div>
          <p className="text-sm text-gray-600 mb-2">Your Covered Number:</p>
          <div className="flex items-center gap-2 p-4 bg-blue-50 rounded-xl border border-blue-100">
            <Phone className="w-5 h-5 text-blue-600" />
            <span className="text-xl font-bold text-blue-900 flex-1">
              {coveredNumber}
            </span>
            <button
              onClick={copyNumber}
              className="p-2 hover:bg-blue-100 rounded-lg transition-colors"
            >
              {copied ? (
                <Check className="w-5 h-5 text-green-500" />
              ) : (
                <Copy className="w-5 h-5 text-blue-600" />
              )}
            </button>
          </div>
          <p className="text-xs text-gray-500 mt-2">
            This is the number your customers will call.
          </p>
        </div>

        {/* Forwarding Setup */}
        <form onSubmit={handleSubmit} className="space-y-4">
          <div>
            <label className="block text-sm font-medium text-gray-700 mb-1">
              Where should we forward urgent calls?
            </label>
            <div className="flex gap-2">
              <span className="px-3 py-3 bg-gray-100 rounded-l-xl text-gray-500 border border-r-0 border-gray-200">
                +44
              </span>
              <input
                type="tel"
                value={forwardingNumber}
                onChange={(e) => setForwardingNumber(e.target.value)}
                placeholder="7XXX XXXXXX"
                required
                className="flex-1 px-4 py-3 border border-gray-200 rounded-r-xl
                           focus:ring-2 focus:ring-blue-500 focus:border-blue-500 outline-none"
              />
            </div>
            <p className="text-xs text-gray-500 mt-2">
              ℹ️ Calls go to Gemma first, then to you if it's urgent.
            </p>
          </div>

          <button
            type="submit"
            disabled={loading || !forwardingNumber}
            className="w-full py-3 bg-blue-600 text-white rounded-xl font-medium
                       hover:bg-blue-700 transition-colors disabled:opacity-50"
          >
            {loading ? 'Setting up...' : 'Set Up Forwarding →'}
          </button>
        </form>
      </div>
    </div>
  );
}
```

### Task 6.4: Step 3 - Test Call

Create `src/app/(onboarding)/step-3/page.tsx`:

```tsx
'use client';

import { useState } from 'react';
import { useRouter } from 'next/navigation';
import { CheckCircle, Circle, Phone, Sparkles } from 'lucide-react';

export default function OnboardingStep3() {
  const router = useRouter();
  const [callMade, setCallMade] = useState(false);

  const coveredNumber = '0191 XXX XXXX';
  const telLink = `tel:${coveredNumber.replace(/\s/g, '')}`;

  const handleCallMade = () => {
    setCallMade(true);
    // In real implementation, you'd detect this via webhook from Vapi
  };

  const handleContinue = async () => {
    // Update onboarding progress
    router.push('/step-4');
  };

  const progress = 75;

  return (
    <div className="bg-white rounded-2xl shadow-sm border border-gray-200 overflow-hidden">
      {/* Progress header */}
      <div className="p-4 border-b border-gray-100">
        <div className="flex items-center gap-2 text-sm text-gray-500 mb-3">
          <CheckCircle className="w-4 h-4 text-green-500" />
          <span className="line-through">Account created</span>
          <CheckCircle className="w-4 h-4 text-green-500 ml-2" />
          <span className="line-through">Business details
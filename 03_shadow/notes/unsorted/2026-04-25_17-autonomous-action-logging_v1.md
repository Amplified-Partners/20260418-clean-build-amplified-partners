---
title: "Autonomous Action Logging System"
id: "17-autonomous-action-logging"
version: 1
created: "2026-04-25"
type: "document"
topic_type: "unsorted"
audience: "internal"
layer: "shadow"
status: "filed"
signed_by: "Devon, 2026-04-25, devin-992682c244cf444f91e0a516498afbfd"
---

# Autonomous Action Logging System
## Specification 17
### Self-Evolving Feedback Loop Infrastructure

---

## PURPOSE

Every autonomous action Covered AI takes must be logged with full context. This creates:
1. **Audit trail** — What happened and why
2. **Training data** — Human overrides become improvement signals
3. **Confidence calibration** — Track accuracy over time
4. **Compliance** — Prove AI decisions are defensible

---

## DATA MODEL

### Prisma Schema Addition

```prisma
// Add to schema.prisma

enum AutonomousActionType {
  // Call handling
  CALL_CLASSIFIED
  CALL_ESCALATED
  CALLBACK_SCHEDULED
  EMERGENCY_FLAGGED
  
  // Invoice management
  INVOICE_CREATED
  INVOICE_SENT
  REMINDER_SENT
  PAYMENT_RECORDED
  
  // Customer communication
  REVIEW_REQUEST_SENT
  FOLLOW_UP_SENT
  QUOTE_GENERATED
  
  // GEO Engine
  FAQ_GENERATED
  FAQ_PUBLISHED
  GEO_PAGE_UPDATED
  SCHEMA_MARKUP_UPDATED
  
  // Dashboard
  ATTENTION_ITEM_CREATED
  ATTENTION_ITEM_RESOLVED
  
  // Nurture
  NURTURE_EMAIL_SENT
  LEAD_SCORED
  LEAD_QUALIFIED
}

enum ActionOutcome {
  SUCCESS
  PARTIAL
  FAILED
  PENDING
  OVERRIDDEN
}

model AutonomousAction {
  id              String                @id @default(cuid())
  clientId        String
  client          Client                @relation(fields: [clientId], references: [id])
  
  // What happened
  actionType      AutonomousActionType
  description     String                // Human-readable: "Sent 7-day invoice reminder to John Smith"
  
  // Trigger context
  triggerId       String?               // ID of triggering entity (callId, invoiceId, etc.)
  triggerType     String?               // "call", "invoice", "schedule", "cron"
  triggerReason   String                // "Invoice overdue by 7 days", "Call classified as emergency"
  
  // Decision context
  decision        String                // "send_reminder", "escalate_to_human", "publish_faq"
  alternatives    Json?                 // Other options considered: [{decision: "wait", score: 0.3}]
  confidence      Float                 // 0.0 to 1.0
  modelUsed       String?               // "gpt-4o", "gpt-4o-mini", "rule-based"
  promptHash      String?               // Hash of prompt used (for versioning)
  
  // Outcome tracking
  outcome         ActionOutcome         @default(PENDING)
  outcomeDetails  String?               // "Email delivered", "Customer responded", "Payment received"
  outcomeAt       DateTime?
  
  // Human override tracking
  wasOverridden   Boolean               @default(false)
  overriddenBy    String?               // User ID who overrode
  overrideReason  String?               // "Incorrect classification", "Customer preference"
  overrideAction  String?               // What they did instead
  overriddenAt    DateTime?
  
  // Metadata
  executionTimeMs Int?                  // How long the action took
  tokenCount      Int?                  // LLM tokens used
  costEstimate    Float?                // Estimated cost in GBP
  
  // Timestamps
  createdAt       DateTime              @default(now())
  updatedAt       DateTime              @updatedAt
  
  @@index([clientId])
  @@index([actionType])
  @@index([outcome])
  @@index([wasOverridden])
  @@index([createdAt])
  @@index([confidence])
}

// Aggregated metrics for dashboard and analysis
model ActionMetrics {
  id              String                @id @default(cuid())
  clientId        String
  client          Client                @relation(fields: [clientId], references: [id])
  
  // Time period
  periodStart     DateTime
  periodEnd       DateTime
  periodType      String                // "day", "week", "month"
  
  // Counts
  totalActions    Int
  successCount    Int
  failedCount     Int
  overriddenCount Int
  
  // Confidence tracking
  avgConfidence   Float
  lowConfidenceCount Int               // Actions with confidence < 0.7
  
  // By type breakdown
  actionBreakdown Json                  // {INVOICE_SENT: 15, REMINDER_SENT: 8, ...}
  
  // Performance
  avgExecutionMs  Float
  totalTokens     Int
  totalCost       Float
  
  // Accuracy (calculated from overrides)
  accuracyRate    Float?                // (total - overridden) / total
  
  createdAt       DateTime              @default(now())
  
  @@unique([clientId, periodStart, periodType])
  @@index([clientId])
  @@index([periodStart])
}
```

---

## API ROUTES

### Log an Action

**POST** `/api/v1/actions`

```typescript
// src/app/api/v1/actions/route.ts

import { prisma } from '@/lib/prisma';
import { NextRequest, NextResponse } from 'next/server';
import crypto from 'crypto';

export async function POST(req: NextRequest) {
  const body = await req.json();
  
  const {
    clientId,
    actionType,
    description,
    triggerId,
    triggerType,
    triggerReason,
    decision,
    alternatives,
    confidence,
    modelUsed,
    prompt,
    executionTimeMs,
    tokenCount,
    costEstimate,
  } = body;
  
  // Hash prompt for versioning without storing full prompt
  const promptHash = prompt 
    ? crypto.createHash('sha256').update(prompt).digest('hex').slice(0, 16)
    : null;
  
  const action = await prisma.autonomousAction.create({
    data: {
      clientId,
      actionType,
      description,
      triggerId,
      triggerType,
      triggerReason,
      decision,
      alternatives,
      confidence,
      modelUsed,
      promptHash,
      executionTimeMs,
      tokenCount,
      costEstimate,
      outcome: 'PENDING',
    },
  });
  
  return NextResponse.json({ id: action.id });
}
```

### Update Outcome

**PATCH** `/api/v1/actions/[id]/outcome`

```typescript
// src/app/api/v1/actions/[id]/outcome/route.ts

import { prisma } from '@/lib/prisma';
import { NextRequest, NextResponse } from 'next/server';

export async function PATCH(
  req: NextRequest,
  { params }: { params: { id: string } }
) {
  const body = await req.json();
  const { outcome, outcomeDetails } = body;
  
  const action = await prisma.autonomousAction.update({
    where: { id: params.id },
    data: {
      outcome,
      outcomeDetails,
      outcomeAt: new Date(),
    },
  });
  
  return NextResponse.json(action);
}
```

### Record Override

**POST** `/api/v1/actions/[id]/override`

```typescript
// src/app/api/v1/actions/[id]/override/route.ts

import { prisma } from '@/lib/prisma';
import { NextRequest, NextResponse } from 'next/server';

export async function POST(
  req: NextRequest,
  { params }: { params: { id: string } }
) {
  const body = await req.json();
  const { userId, reason, alternativeAction } = body;
  
  const action = await prisma.autonomousAction.update({
    where: { id: params.id },
    data: {
      wasOverridden: true,
      overriddenBy: userId,
      overrideReason: reason,
      overrideAction: alternativeAction,
      overriddenAt: new Date(),
      outcome: 'OVERRIDDEN',
    },
  });
  
  return NextResponse.json(action);
}
```

### Get Actions (with filters)

**GET** `/api/v1/clients/[id]/actions`

```typescript
// src/app/api/v1/clients/[id]/actions/route.ts

import { prisma } from '@/lib/prisma';
import { NextRequest, NextResponse } from 'next/server';

export async function GET(
  req: NextRequest,
  { params }: { params: { id: string } }
) {
  const { searchParams } = new URL(req.url);
  const actionType = searchParams.get('type');
  const outcome = searchParams.get('outcome');
  const overriddenOnly = searchParams.get('overridden') === 'true';
  const lowConfidence = searchParams.get('lowConfidence') === 'true';
  const limit = parseInt(searchParams.get('limit') || '50');
  const offset = parseInt(searchParams.get('offset') || '0');
  
  const where: any = { clientId: params.id };
  
  if (actionType) where.actionType = actionType;
  if (outcome) where.outcome = outcome;
  if (overriddenOnly) where.wasOverridden = true;
  if (lowConfidence) where.confidence = { lt: 0.7 };
  
  const [actions, total] = await Promise.all([
    prisma.autonomousAction.findMany({
      where,
      orderBy: { createdAt: 'desc' },
      take: limit,
      skip: offset,
    }),
    prisma.autonomousAction.count({ where }),
  ]);
  
  return NextResponse.json({
    actions,
    total,
    hasMore: offset + actions.length < total,
  });
}
```

### Get Metrics

**GET** `/api/v1/clients/[id]/actions/metrics`

```typescript
// src/app/api/v1/clients/[id]/actions/metrics/route.ts

import { prisma } from '@/lib/prisma';
import { NextRequest, NextResponse } from 'next/server';

export async function GET(
  req: NextRequest,
  { params }: { params: { id: string } }
) {
  const { searchParams } = new URL(req.url);
  const days = parseInt(searchParams.get('days') || '30');
  
  const since = new Date();
  since.setDate(since.getDate() - days);
  
  const actions = await prisma.autonomousAction.findMany({
    where: {
      clientId: params.id,
      createdAt: { gte: since },
    },
  });
  
  // Calculate metrics
  const total = actions.length;
  const successful = actions.filter(a => a.outcome === 'SUCCESS').length;
  const failed = actions.filter(a => a.outcome === 'FAILED').length;
  const overridden = actions.filter(a => a.wasOverridden).length;
  const lowConfidence = actions.filter(a => a.confidence < 0.7).length;
  
  const avgConfidence = total > 0
    ? actions.reduce((sum, a) => sum + a.confidence, 0) / total
    : 0;
  
  const accuracyRate = total > 0
    ? (total - overridden) / total
    : 1;
  
  // Group by type
  const byType = actions.reduce((acc, a) => {
    acc[a.actionType] = (acc[a.actionType] || 0) + 1;
    return acc;
  }, {} as Record<string, number>);
  
  // Group by day for trend
  const byDay = actions.reduce((acc, a) => {
    const day = a.createdAt.toISOString().split('T')[0];
    acc[day] = (acc[day] || 0) + 1;
    return acc;
  }, {} as Record<string, number>);
  
  return NextResponse.json({
    period: { days, since: since.toISOString() },
    counts: {
      total,
      successful,
      failed,
      overridden,
      lowConfidence,
    },
    rates: {
      successRate: total > 0 ? successful / total : 0,
      accuracyRate,
      avgConfidence,
    },
    byType,
    byDay,
  });
}
```

---

## HELPER LIBRARY

### Action Logger Utility

```typescript
// src/lib/action-logger.ts

import { prisma } from '@/lib/prisma';
import type { AutonomousActionType, ActionOutcome } from '@prisma/client';

interface LogActionParams {
  clientId: string;
  actionType: AutonomousActionType;
  description: string;
  triggerId?: string;
  triggerType?: string;
  triggerReason: string;
  decision: string;
  alternatives?: Array<{ decision: string; score: number }>;
  confidence: number;
  modelUsed?: string;
  prompt?: string;
  executionTimeMs?: number;
  tokenCount?: number;
  costEstimate?: number;
}

interface ActionLogger {
  id: string;
  success: (details?: string) => Promise<void>;
  fail: (details?: string) => Promise<void>;
  partial: (details?: string) => Promise<void>;
}

export async function logAction(params: LogActionParams): Promise<ActionLogger> {
  const promptHash = params.prompt
    ? require('crypto')
        .createHash('sha256')
        .update(params.prompt)
        .digest('hex')
        .slice(0, 16)
    : null;

  const action = await prisma.autonomousAction.create({
    data: {
      clientId: params.clientId,
      actionType: params.actionType,
      description: params.description,
      triggerId: params.triggerId,
      triggerType: params.triggerType,
      triggerReason: params.triggerReason,
      decision: params.decision,
      alternatives: params.alternatives,
      confidence: params.confidence,
      modelUsed: params.modelUsed,
      promptHash,
      executionTimeMs: params.executionTimeMs,
      tokenCount: params.tokenCount,
      costEstimate: params.costEstimate,
      outcome: 'PENDING',
    },
  });

  const updateOutcome = async (outcome: ActionOutcome, details?: string) => {
    await prisma.autonomousAction.update({
      where: { id: action.id },
      data: {
        outcome,
        outcomeDetails: details,
        outcomeAt: new Date(),
      },
    });
  };

  return {
    id: action.id,
    success: (details?: string) => updateOutcome('SUCCESS', details),
    fail: (details?: string) => updateOutcome('FAILED', details),
    partial: (details?: string) => updateOutcome('PARTIAL', details),
  };
}

export async function recordOverride(
  actionId: string,
  userId: string,
  reason: string,
  alternativeAction: string
) {
  await prisma.autonomousAction.update({
    where: { id: actionId },
    data: {
      wasOverridden: true,
      overriddenBy: userId,
      overrideReason: reason,
      overrideAction: alternativeAction,
      overriddenAt: new Date(),
      outcome: 'OVERRIDDEN',
    },
  });
}

// Quick helpers for common actions
export const ActionLog = {
  async callClassified(
    clientId: string,
    callId: string,
    intent: string,
    confidence: number,
    modelUsed: string
  ) {
    return logAction({
      clientId,
      actionType: 'CALL_CLASSIFIED',
      description: `Call classified as "${intent}"`,
      triggerId: callId,
      triggerType: 'call',
      triggerReason: 'Incoming call received',
      decision: intent,
      confidence,
      modelUsed,
    });
  },

  async invoiceReminderSent(
    clientId: string,
    invoiceId: string,
    customerName: string,
    daysOverdue: number,
    reminderStage: number
  ) {
    return logAction({
      clientId,
      actionType: 'REMINDER_SENT',
      description: `Sent ${reminderStage}-day reminder to ${customerName}`,
      triggerId: invoiceId,
      triggerType: 'invoice',
      triggerReason: `Invoice overdue by ${daysOverdue} days`,
      decision: `send_reminder_stage_${reminderStage}`,
      confidence: 1.0, // Rule-based, not ML
      modelUsed: 'rule-based',
    });
  },

  async faqGenerated(
    clientId: string,
    question: string,
    confidence: number,
    sourceCallCount: number
  ) {
    return logAction({
      clientId,
      actionType: 'FAQ_GENERATED',
      description: `Generated FAQ: "${question.slice(0, 50)}..."`,
      triggerType: 'cron',
      triggerReason: `Extracted from ${sourceCallCount} calls`,
      decision: 'generate_faq',
      confidence,
      modelUsed: 'gpt-4o',
    });
  },

  async attentionItemCreated(
    clientId: string,
    title: string,
    sourceType: string,
    sourceId: string,
    confidence: number
  ) {
    return logAction({
      clientId,
      actionType: 'ATTENTION_ITEM_CREATED',
      description: `Created attention item: "${title}"`,
      triggerId: sourceId,
      triggerType: sourceType,
      triggerReason: `${sourceType} flagged for attention`,
      decision: 'create_attention_item',
      confidence,
      modelUsed: 'gpt-4o',
    });
  },

  async reviewRequestSent(
    clientId: string,
    jobId: string,
    customerName: string
  ) {
    return logAction({
      clientId,
      actionType: 'REVIEW_REQUEST_SENT',
      description: `Sent review request to ${customerName}`,
      triggerId: jobId,
      triggerType: 'job',
      triggerReason: 'Job marked as complete',
      decision: 'send_review_request',
      confidence: 1.0,
      modelUsed: 'rule-based',
    });
  },

  async emergencyFlagged(
    clientId: string,
    callId: string,
    reason: string,
    confidence: number
  ) {
    return logAction({
      clientId,
      actionType: 'EMERGENCY_FLAGGED',
      description: `Emergency flagged: ${reason}`,
      triggerId: callId,
      triggerType: 'call',
      triggerReason: reason,
      decision: 'flag_emergency',
      confidence,
      modelUsed: 'gpt-4o',
    });
  },
};
```

---

## TRIGGER.DEV JOB: AGGREGATE METRICS

```typescript
// trigger-jobs/src/jobs/aggregate-action-metrics.ts

import { schedules } from '@trigger.dev/sdk/v3';
import { prisma } from '../lib/prisma';

export const aggregateActionMetrics = schedules.task({
  id: 'aggregate-action-metrics',
  cron: '0 1 * * *', // Daily at 1am
  run: async () => {
    const yesterday = new Date();
    yesterday.setDate(yesterday.getDate() - 1);
    yesterday.setHours(0, 0, 0, 0);
    
    const today = new Date();
    today.setHours(0, 0, 0, 0);
    
    // Get all clients with actions yesterday
    const clientsWithActions = await prisma.autonomousAction.groupBy({
      by: ['clientId'],
      where: {
        createdAt: {
          gte: yesterday,
          lt: today,
        },
      },
    });
    
    for (const { clientId } of clientsWithActions) {
      const actions = await prisma.autonomousAction.findMany({
        where: {
          clientId,
          createdAt: {
            gte: yesterday,
            lt: today,
          },
        },
      });
      
      const total = actions.length;
      const successful = actions.filter(a => a.outcome === 'SUCCESS').length;
      const failed = actions.filter(a => a.outcome === 'FAILED').length;
      const overridden = actions.filter(a => a.wasOverridden).length;
      const lowConfidence = actions.filter(a => a.confidence < 0.7).length;
      
      const avgConfidence = total > 0
        ? actions.reduce((sum, a) => sum + a.confidence, 0) / total
        : 0;
      
      const avgExecutionMs = total > 0
        ? actions.reduce((sum, a) => sum + (a.executionTimeMs || 0), 0) / total
        : 0;
      
      const totalTokens = actions.reduce((sum, a) => sum + (a.tokenCount || 0), 0);
      const totalCost = actions.reduce((sum, a) => sum + (a.costEstimate || 0), 0);
      
      const actionBreakdown = actions.reduce((acc, a) => {
        acc[a.actionType] = (acc[a.actionType] || 0) + 1;
        return acc;
      }, {} as Record<string, number>);
      
      await prisma.actionMetrics.upsert({
        where: {
          clientId_periodStart_periodType: {
            clientId,
            periodStart: yesterday,
            periodType: 'day',
          },
        },
        create: {
          clientId,
          periodStart: yesterday,
          periodEnd: today,
          periodType: 'day',
          totalActions: total,
          successCount: successful,
          failedCount: failed,
          overriddenCount: overridden,
          avgConfidence,
          lowConfidenceCount: lowConfidence,
          actionBreakdown,
          avgExecutionMs,
          totalTokens,
          totalCost,
          accuracyRate: total > 0 ? (total - overridden) / total : 1,
        },
        update: {
          totalActions: total,
          successCount: successful,
          failedCount: failed,
          overriddenCount: overridden,
          avgConfidence,
          lowConfidenceCount: lowConfidence,
          actionBreakdown,
          avgExecutionMs,
          totalTokens,
          totalCost,
          accuracyRate: total > 0 ? (total - overridden) / total : 1,
        },
      });
    }
    
    return { processed: clientsWithActions.length };
  },
});
```

---

## INTEGRATION POINTS

### 1. Invoice Chasing Job

```typescript
// In invoice-chasing.ts, wrap the send logic:

import { ActionLog } from '../lib/action-logger';

// When sending a reminder:
const action = await ActionLog.invoiceReminderSent(
  invoice.clientId,
  invoice.id,
  invoice.customerName,
  daysOverdue,
  reminderStage
);

try {
  await sendEmail(reminderEmail);
  await action.success('Email delivered');
} catch (error) {
  await action.fail(error.message);
}
```

### 2. Call Classification (Vapi Webhook)

```typescript
// In webhook handler:

import { ActionLog } from '../lib/action-logger';

const classification = await classifyCall(transcript);

const action = await ActionLog.callClassified(
  clientId,
  callId,
  classification.intent,
  classification.confidence,
  'gpt-4o'
);

// Later, if human changes classification:
if (userChangedIntent) {
  await recordOverride(
    action.id,
    userId,
    'Incorrect classification',
    newIntent
  );
}
```

### 3. FAQ Generation Job

```typescript
// In extract-faqs-from-calls.ts:

import { ActionLog } from '../lib/action-logger';

for (const faq of generatedFaqs) {
  const action = await ActionLog.faqGenerated(
    clientId,
    faq.question,
    faq.confidence,
    faq.sourceCallCount
  );
  
  // FAQ is auto-published if confidence > 0.8
  if (faq.confidence > 0.8) {
    await action.success('Auto-published');
  } else {
    await action.partial('Pending review');
  }
}
```

### 4. Attention Item Creation

```typescript
// Anywhere attention items are created:

import { ActionLog } from '../lib/action-logger';

const action = await ActionLog.attentionItemCreated(
  clientId,
  title,
  'call', // or 'invoice', 'review', etc.
  sourceId,
  confidence
);

// When user dismisses/acts on attention item, check if they changed the recommended action
if (userAction !== recommendedAction) {
  await recordOverride(
    action.id,
    userId,
    'Different action taken',
    userAction
  );
}
```

---

## DASHBOARD COMPONENT

### AI Accuracy Card

```tsx
// src/components/dashboard/AiAccuracyCard.tsx

'use client';

import { useState, useEffect } from 'react';

interface ActionMetrics {
  counts: {
    total: number;
    successful: number;
    failed: number;
    overridden: number;
    lowConfidence: number;
  };
  rates: {
    successRate: number;
    accuracyRate: number;
    avgConfidence: number;
  };
}

export function AiAccuracyCard({ clientId }: { clientId: string }) {
  const [metrics, setMetrics] = useState<ActionMetrics | null>(null);
  const [loading, setLoading] = useState(true);
  
  useEffect(() => {
    fetch(`/api/v1/clients/${clientId}/actions/metrics?days=30`)
      .then(res => res.json())
      .then(setMetrics)
      .finally(() => setLoading(false));
  }, [clientId]);
  
  if (loading) {
    return (
      <div className="bg-white rounded-2xl p-5 animate-pulse">
        <div className="h-6 bg-grey-100 rounded w-32 mb-4" />
        <div className="h-12 bg-grey-100 rounded w-20" />
      </div>
    );
  }
  
  if (!metrics) return null;
  
  const accuracyPercent = Math.round(metrics.rates.accuracyRate * 100);
  const confidencePercent = Math.round(metrics.rates.avgConfidence * 100);
  
  const getAccuracyColor = (rate: number) => {
    if (rate >= 0.95) return 'text-green-600';
    if (rate >= 0.85) return 'text-amber-600';
    return 'text-red-600';
  };
  
  return (
    <div className="bg-white rounded-2xl p-5">
      <div className="flex items-center justify-between mb-4">
        <h3 className="text-base font-semibold text-grey-900">AI Accuracy</h3>
        <span className="text-xs text-grey-500">Last 30 days</span>
      </div>
      
      <div className="flex items-baseline gap-2 mb-4">
        <span className={`text-3xl font-bold ${getAccuracyColor(metrics.rates.accuracyRate)}`}>
          {accuracyPercent}%
        </span>
        <span className="text-sm text-grey-500">accurate</span>
      </div>
      
      <div className="space-y-2 text-sm">
        <div className="flex justify-between">
          <span className="text-grey-600">Actions taken</span>
          <span className="font-medium">{metrics.counts.total}</span>
        </div>
        <div className="flex justify-between">
          <span className="text-grey-600">Overridden</span>
          <span className="font-medium text-amber-600">{metrics.counts.overridden}</span>
        </div>
        <div className="flex justify-between">
          <span className="text-grey-600">Avg confidence</span>
          <span className="font-medium">{confidencePercent}%</span>
        </div>
        <div className="flex justify-between">
          <span className="text-grey-600">Low confidence</span>
          <span className="font-medium text-grey-500">{metrics.counts.lowConfidence}</span>
        </div>
      </div>
      
      {metrics.counts.overridden > 5 && (
        <div className="mt-4 p-3 bg-amber-50 rounded-lg">
          <p className="text-xs text-amber-800">
            {metrics.counts.overridden} actions were corrected. 
            We're learning from your feedback.
          </p>
        </div>
      )}
    </div>
  );
}
```

---

## CLAUDE CODE BUILD PROMPT

```
Add autonomous action logging to Covered AI.

Read: /specs/17-AUTONOMOUS-ACTION-LOGGING.md

Tasks:
1. Add AutonomousAction and ActionMetrics models to prisma/schema.prisma
2. Run prisma migrate
3. Create src/lib/action-logger.ts with helper functions
4. Create API routes:
   - POST /api/v1/actions
   - PATCH /api/v1/actions/[id]/outcome
   - POST /api/v1/actions/[id]/override
   - GET /api/v1/clients/[id]/actions
   - GET /api/v1/clients/[id]/actions/metrics
5. Create trigger-jobs/src/jobs/aggregate-action-metrics.ts
6. Create src/components/dashboard/AiAccuracyCard.tsx
7. Integrate ActionLog calls into existing jobs:
   - invoice-chasing.ts
   - review-request.ts
   - lead-nurture.ts
   - extract-faqs-from-calls.ts
8. Add AiAccuracyCard to dashboard

Every autonomous action must now be logged with confidence, outcome, and override tracking.
```

---

## SUCCESS METRICS

After 30 days of operation:

| Metric | Target | Indicates |
|--------|--------|-----------|
| Accuracy rate | >95% | AI decisions are correct |
| Override rate | <5% | Humans rarely need to intervene |
| Avg confidence | >0.85 | Model is certain |
| Low confidence actions | <10% | Few uncertain decisions |

If override rate is high for specific action types, those become priority improvement areas.

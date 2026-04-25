---
title: "Voice Quality"
id: "voice-quality"
version: 1
created: 2026-04-25
last_validated: 2026-04-25
type: document
topic_type: reference
status: imported
source_file: "07-voice-quality.md"
signed_by: "Devon, 2026-04-25, devin-992682c244cf444f91e0a516498afbfd"
---

# Voice Quality Monitoring Spec

## Why This Matters

Poor AI voice quality destroys trust instantly. A robotic, choppy, or delayed Gemma makes callers hang up.

From research: "Poor Quality of Service (QoS) in voice communications can undermine the customer experience."

---

## Key Quality Metrics

| Metric | Description | Threshold | Action if Exceeded |
|--------|-------------|-----------|-------------------|
| **Latency** | Delay in audio transmission | < 150ms | Alert + investigate |
| **Jitter** | Variation in packet arrival | < 30ms | Alert + investigate |
| **Packet Loss** | Data packets failing to arrive | < 1% | Alert + pause calls |
| **MOS Score** | Mean Opinion Score (1-5) | > 4.0 | Alert if below |
| **Call Completion Rate** | Calls that complete successfully | > 95% | Alert if below |
| **ASR Accuracy** | Speech recognition accuracy | > 90% | Review transcripts |

---

## Vapi Webhook Events to Monitor

```typescript
// Vapi sends these events via webhook
interface VapiCallEvent {
  type: 'call-started' | 'call-ended' | 'speech-update' | 'error';
  call: {
    id: string;
    duration: number;
    endedReason: string;
    // Quality metrics (if available)
    metrics?: {
      latency?: number;
      jitter?: number;
      packetLoss?: number;
      mosScore?: number;
    };
  };
}

// Track call quality
async function trackCallQuality(event: VapiCallEvent) {
  if (event.type === 'call-ended') {
    const metrics = event.call.metrics;
    
    // Store for analysis
    await db.callQuality.create({
      callId: event.call.id,
      duration: event.call.duration,
      endedReason: event.call.endedReason,
      latency: metrics?.latency,
      jitter: metrics?.jitter,
      packetLoss: metrics?.packetLoss,
      mosScore: metrics?.mosScore,
      timestamp: new Date()
    });
    
    // Alert if quality is poor
    if (metrics?.mosScore && metrics.mosScore < 4.0) {
      await alertPoorQuality(event.call.id, metrics);
    }
    
    // Alert if call ended abnormally
    if (event.call.endedReason === 'error' || 
        event.call.endedReason === 'customer-hangup-early') {
      await alertAbnormalEnd(event.call.id, event.call.endedReason);
    }
  }
}
```

---

## Call End Reasons to Track

| End Reason | Indicates | Action |
|------------|-----------|--------|
| `customer-ended` | Normal completion | None |
| `assistant-ended` | Gemma finished | None |
| `customer-hangup-early` | Customer hung up fast | Review transcript |
| `error` | Technical failure | Alert + investigate |
| `silence-timeout` | No speech detected | Review, may be spam |
| `max-duration` | Hit time limit | Review, may need adjustment |

---

## Database Schema Addition

```prisma
model CallQuality {
  id            String   @id @default(uuid())
  callId        String   @map("call_id")
  clientId      String   @map("client_id")
  
  duration      Int      // seconds
  endedReason   String   @map("ended_reason")
  
  // Quality metrics
  latency       Float?   // milliseconds
  jitter        Float?   // milliseconds
  packetLoss    Float?   @map("packet_loss") // percentage
  mosScore      Float?   @map("mos_score") // 1-5
  
  // Flags
  qualityAlert  Boolean  @default(false) @map("quality_alert")
  reviewed      Boolean  @default(false)
  
  createdAt     DateTime @default(now()) @map("created_at")
  
  client        Client   @relation(fields: [clientId], references: [id])
  
  @@index([clientId])
  @@index([createdAt])
  @@index([qualityAlert])
  @@map("call_quality")
}
```

---

## Alerting Rules

### Immediate Alerts (Slack/Email to Admin)

```typescript
const ALERT_THRESHOLDS = {
  mosScore: { min: 3.5, message: 'MOS score critically low' },
  packetLoss: { max: 2, message: 'High packet loss detected' },
  errorRate: { max: 5, message: 'Error rate exceeded 5%' }, // per hour
  hangupRate: { max: 20, message: 'Early hangup rate high' } // percentage
};
```

### Daily Summary

```typescript
interface DailyQualitySummary {
  totalCalls: number;
  avgMosScore: number;
  avgLatency: number;
  errorCount: number;
  earlyHangupCount: number;
  earlyHangupRate: number;
  qualityAlerts: number;
}

// Send daily at 8am
async function sendDailyQualityReport() {
  const summary = await calculateDailySummary();
  
  if (summary.avgMosScore < 4.0 || summary.errorCount > 10) {
    await sendAlertEmail('Quality degradation detected', summary);
  }
}
```

---

## Dashboard Widget

### Admin Dashboard (Internal)

```
┌─────────────────────────────────────────────────────────────────┐
│  VOICE QUALITY (Last 24 Hours)                                  │
├─────────────────────────────────────────────────────────────────┤
│                                                                 │
│  MOS Score          Latency           Packet Loss               │
│  ┌─────────┐       ┌─────────┐       ┌─────────┐               │
│  │  4.3    │       │  89ms   │       │  0.2%   │               │
│  │  ████   │       │  ████   │       │  ████   │               │
│  │  Good   │       │  Good   │       │  Good   │               │
│  └─────────┘       └─────────┘       └─────────┘               │
│                                                                 │
│  Call Completion: 97.2%    Early Hangups: 8.1%    Errors: 2     │
│                                                                 │
└─────────────────────────────────────────────────────────────────┘
```

---

## Transcript Review Queue

When quality issues are detected, flag calls for manual review:

```typescript
interface ReviewQueueItem {
  callId: string;
  clientId: string;
  reason: 'poor_quality' | 'early_hangup' | 'error' | 'low_mos';
  transcript: string;
  audioUrl?: string;
  createdAt: Date;
  reviewed: boolean;
  reviewNotes?: string;
}

// Add to review queue
async function flagForReview(callId: string, reason: string) {
  await db.reviewQueue.create({
    callId,
    reason,
    createdAt: new Date(),
    reviewed: false
  });
}
```

---

## Proactive Quality Checks

### Synthetic Test Calls

Run automated test calls daily to verify system health:

```typescript
// Daily at 6am (before business hours)
async function runSyntheticTest() {
  // Call each active client's Covered number
  // Use test script
  // Measure quality metrics
  // Alert if degradation detected
}
```

### Client-Specific Monitoring

If a specific client reports issues:

1. Pull last 50 calls for that client
2. Calculate quality metrics
3. Compare to baseline
4. Investigate if below threshold

---

## Implementation Priority

| Phase | Task | Priority |
|-------|------|----------|
| 1 | Track call end reasons | High |
| 2 | Store basic quality data | High |
| 3 | Alert on errors | High |
| 4 | Dashboard widget (internal) | Medium |
| 5 | Daily summary reports | Medium |
| 6 | Transcript review queue | Low |
| 7 | Synthetic test calls | Low |

---

## API Endpoints

```
GET /api/v1/admin/quality/summary
  Query: period (today, week, month)
  Returns: DailyQualitySummary

GET /api/v1/admin/quality/alerts
  Query: status (open, resolved)
  Returns: QualityAlert[]

GET /api/v1/admin/quality/calls/{callId}
  Returns: Full call quality details + transcript

POST /api/v1/admin/quality/calls/{callId}/review
  Body: { notes, resolved }
  Returns: Updated call record
```

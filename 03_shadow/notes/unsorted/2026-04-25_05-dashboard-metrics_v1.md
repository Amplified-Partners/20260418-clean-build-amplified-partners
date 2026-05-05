---
title: "Dashboard Metrics Spec"
id: "05-dashboard-metrics"
version: 1
created: "2026-04-25"
type: "document"
topic_type: "unsorted"
audience: "internal"
layer: "shadow"
status: "filed"
signed_by: "Devon, 2026-04-25, devin-992682c244cf444f91e0a516498afbfd"
---

# Dashboard Metrics Spec

## Principles Applied

| Principle | Application |
|-----------|-------------|
| Peak-End Rule | End of month/week with "win" summary |
| Variable Reward | Show unexpected value ("Biggest lead: £2,400") |
| Investment | Show cumulative value to increase switching cost |
| Cognitive Load | Minimal metrics, clear hierarchy |

---

## Dashboard Layout

### Header

```
┌─────────────────────────────────────────────────────────────────┐
│  COVERED AI                              [Ralph ▼] [⚙️] [?]     │
├─────────────────────────────────────────────────────────────────┤
│  Good morning, Ralph                        November 2025 ▼     │
└─────────────────────────────────────────────────────────────────┘
```

### Primary Metrics (4 Cards)

```
┌─────────────┐ ┌─────────────┐ ┌─────────────┐ ┌─────────────┐
│  CALLS      │ │  LEADS      │ │  JOBS       │ │  TIME       │
│  ANSWERED   │ │  CAPTURED   │ │  BOOKED     │ │  SAVED      │
│             │ │             │ │             │ │             │
│    147      │ │     43      │ │     31      │ │   18hrs     │
│             │ │             │ │             │ │             │
│  ↑ 12%      │ │  ↑ 8%       │ │  72% conv   │ │  ≈ £540     │
└─────────────┘ └─────────────┘ └─────────────┘ └─────────────┘
```

---

## Metric Definitions

### Core Metrics

| Metric | Calculation | Display | Why It Matters |
|--------|-------------|---------|----------------|
| **Calls Answered** | COUNT(calls) WHERE status = 'completed' | Integer | Core value — "we answered X calls" |
| **Leads Captured** | COUNT(leads) WHERE has_valid_contact = true | Integer | Quality filter — not all calls are leads |
| **Jobs Booked** | COUNT(leads) WHERE status = 'booked' | Integer | Conversion proof |
| **Conversion Rate** | (Jobs Booked / Leads Captured) × 100 | Percentage | Efficiency metric |
| **Time Saved** | (Calls Answered - Leads Captured) × 5 min | Hours | ROI justification |
| **Time Value** | Time Saved × £30/hr | Currency | Money-back framing |

### Period Comparison

| Metric | This Period | vs Last Period |
|--------|-------------|----------------|
| Calls | 147 | ↑ 12% |
| Leads | 43 | ↑ 8% |
| Conversion | 72% | ↑ 3pp |

**Calculation:**
```typescript
const percentChange = ((current - previous) / previous) * 100;
const displayArrow = percentChange >= 0 ? '↑' : '↓';
```

---

## Dashboard Sections

### Section 1: Primary Metrics

```typescript
interface PrimaryMetric {
  id: string;
  label: string;
  value: number | string;
  format: 'integer' | 'percentage' | 'hours' | 'currency';
  trend?: {
    direction: 'up' | 'down' | 'flat';
    value: number;
    label: string;
  };
}

const primaryMetrics: PrimaryMetric[] = [
  {
    id: 'calls_answered',
    label: 'Calls Answered',
    value: 147,
    format: 'integer',
    trend: { direction: 'up', value: 12, label: '↑ 12%' }
  },
  {
    id: 'leads_captured',
    label: 'Leads Captured',
    value: 43,
    format: 'integer',
    trend: { direction: 'up', value: 8, label: '↑ 8%' }
  },
  {
    id: 'jobs_booked',
    label: 'Jobs Booked',
    value: 31,
    format: 'integer',
    trend: { direction: 'flat', value: 72, label: '72% conv' }
  },
  {
    id: 'time_saved',
    label: 'Time Saved',
    value: 18,
    format: 'hours',
    trend: { direction: 'flat', value: 540, label: '≈ £540' }
  }
];
```

### Section 2: Performance Chart

```typescript
interface ChartData {
  date: string;
  calls: number;
  leads: number;
  jobs: number;
}

// Line chart: Calls vs Leads vs Jobs over 30 days
// X-axis: Date
// Y-axis: Count
// Three lines with different colors
```

### Section 3: Recent Leads

```typescript
interface LeadRow {
  id: string;
  customerName: string;
  jobType: string;
  postcode: string;
  urgency: 'emergency' | 'urgent' | 'routine';
  timeAgo: string;
  status: 'new' | 'contacted' | 'booked' | 'dismissed';
}

// Display: Last 5 leads
// Columns: Name, Job Type, Postcode, Urgency Badge, Time
// Click to view lead detail
```

### Section 4: Reviews

```typescript
interface ReviewStats {
  requestsSent: number;
  reviewsReceived: number;
  conversionRate: number;
  averageRating: number;
}

// Two-column layout:
// Left: Requests Sent, This Month
// Right: Reviews Received, Conversion %, Avg Rating
```

### Section 5: All-Time Stats (Investment Reinforcement)

```typescript
interface AllTimeStats {
  callsAnswered: number;
  leadsCaputred: number;
  estimatedValue: number;
  jobsBooked: number;
  actualRevenue: number;
  timeSaved: number;
  timeValue: number;
  reviewsCollected: number;
  averageRating: number;
  memberSince: Date;
}

// Purpose: Show cumulative value to increase switching cost
// "Leaving means losing all this history"
```

---

## Time Period Selector

```typescript
type TimePeriod = 'today' | 'yesterday' | 'this_week' | 'last_week' | 
                  'this_month' | 'last_month' | 'this_quarter' | 
                  'this_year' | 'all_time' | 'custom';

interface DateRange {
  start: Date;
  end: Date;
}
```

Default: `this_month`

---

## API Endpoints

### Dashboard Stats

```
GET /api/v1/clients/{client_id}/dashboard
Query params:
  - period: TimePeriod
  - start_date: ISO date (if custom)
  - end_date: ISO date (if custom)

Response:
{
  "period": {
    "start": "2025-11-01T00:00:00Z",
    "end": "2025-11-27T23:59:59Z",
    "label": "November 2025"
  },
  "metrics": {
    "calls_answered": 147,
    "leads_captured": 43,
    "jobs_booked": 31,
    "conversion_rate": 72.1,
    "time_saved_hours": 18,
    "time_value_gbp": 540
  },
  "trends": {
    "calls_answered": { "direction": "up", "percent": 12 },
    "leads_captured": { "direction": "up", "percent": 8 },
    "jobs_booked": { "direction": "up", "percent": 5 }
  },
  "chart_data": [
    { "date": "2025-11-01", "calls": 5, "leads": 2, "jobs": 1 },
    { "date": "2025-11-02", "calls": 7, "leads": 3, "jobs": 2 },
    // ...
  ],
  "recent_leads": [
    {
      "id": "uuid",
      "customer_name": "Sarah M.",
      "job_type": "Burst pipe",
      "postcode": "NE4 5TH",
      "urgency": "emergency",
      "time_ago": "2m",
      "status": "new"
    },
    // ...
  ],
  "reviews": {
    "requests_sent": 28,
    "reviews_received": 9,
    "conversion_rate": 32.1,
    "average_rating": 4.8
  },
  "all_time": {
    "calls_answered": 1247,
    "leads_captured": 412,
    "estimated_value": 82400,
    "jobs_booked": 298,
    "actual_revenue": 61200,
    "time_saved_hours": 156,
    "time_value_gbp": 4680,
    "reviews_collected": 34,
    "average_rating": 4.9,
    "member_since": "2025-10-01T00:00:00Z"
  }
}
```

---

## Calculation Logic

### Time Saved

```typescript
function calculateTimeSaved(calls: number, leads: number): number {
  // Assumption: Each filtered call saves 5 minutes
  const filteredCalls = calls - leads;
  const minutesSaved = filteredCalls * 5;
  const hoursSaved = minutesSaved / 60;
  return Math.round(hoursSaved);
}
```

### Time Value

```typescript
function calculateTimeValue(hoursSaved: number, hourlyRate: number = 30): number {
  return hoursSaved * hourlyRate;
}
```

### Conversion Rate

```typescript
function calculateConversionRate(leads: number, jobs: number): number {
  if (leads === 0) return 0;
  return Math.round((jobs / leads) * 100 * 10) / 10; // 1 decimal place
}
```

### Estimated Lead Value

```typescript
function calculateEstimatedValue(leads: number, vertical: string): number {
  const avgJobValue: Record<string, number> = {
    trades: 200,
    vet: 150,
    dental: 300,
    aesthetics: 250,
    salon: 80
  };
  return leads * (avgJobValue[vertical] || 200);
}
```

---

## Weekly Report Email

**Sent:** Every Monday at 9:00 AM

**Subject:** Your week with Covered AI 📊

```html
<h1>Your Week in Numbers</h1>

<table>
  <tr>
    <td>📞 Calls Answered</td>
    <td>47</td>
  </tr>
  <tr>
    <td>👤 Leads Captured</td>
    <td>18</td>
  </tr>
  <tr>
    <td>💼 Jobs Booked</td>
    <td>12</td>
  </tr>
  <tr>
    <td>⏱️ Time Saved</td>
    <td>6 hours (≈ £180)</td>
  </tr>
  <tr>
    <td>⭐ Reviews Received</td>
    <td>3</td>
  </tr>
</table>

<h2>🏆 Highlight of the Week</h2>
<p>Your biggest lead: £2,400 emergency boiler replacement 
   from a Saturday night call.</p>

<a href="{{dashboard_url}}">View Full Dashboard →</a>
```

---

## Monthly Report Email

**Sent:** 1st of each month at 8:00 AM

**Subject:** Your November Covered AI Report 🚀

```html
<h1>November Numbers</h1>

<table>
  <tr><td>📞 Calls Answered</td><td>147</td><td>↑ 12% vs Oct</td></tr>
  <tr><td>👤 Leads Captured</td><td>43</td><td>↑ 8%</td></tr>
  <tr><td>💼 Jobs Booked</td><td>31</td><td>72% conversion</td></tr>
  <tr><td>⏱️ Time Saved</td><td>18 hours</td><td>≈ £540</td></tr>
  <tr><td>⭐ Reviews</td><td>9 new</td><td>Avg: 4.8 ⭐</td></tr>
</table>

<h2>🏆 Your Biggest Win</h2>
<p>£2,400 emergency boiler replacement from a 2am call 
   you would have slept through.</p>

<h2>📈 All-Time Stats</h2>
<p>Since joining Covered AI:</p>
<ul>
  <li>1,247 calls answered</li>
  <li>412 leads captured (worth ~£82,400)</li>
  <li>298 jobs booked (£61,200 revenue)</li>
  <li>156 hours saved (£4,680 value)</li>
  <li>34 Google reviews collected</li>
</ul>

<a href="{{dashboard_url}}">View Full Dashboard →</a>
```

---

## Real-Time Updates

### WebSocket Events

```typescript
// Subscribe to real-time updates
socket.on('new_lead', (lead) => {
  // Update leads_captured count
  // Add to recent_leads list
  // Flash notification
});

socket.on('lead_booked', (lead) => {
  // Update jobs_booked count
  // Update conversion_rate
});

socket.on('review_received', (review) => {
  // Update reviews_received count
  // Update average_rating
});
```

---

## HEART Framework Tracking

Google's HEART framework for measuring UX at scale:

| Dimension | Metric | How Measured | Target |
|-----------|--------|--------------|--------|
| **Happiness** | NPS Score | Monthly in-app survey | > 50 |
| **Happiness** | CSAT | Post-onboarding survey | > 4.5/5 |
| **Engagement** | DAU/MAU Ratio | Daily active / Monthly active | > 40% |
| **Engagement** | Notification Tap Rate | Taps / Notifications sent | > 80% |
| **Adoption** | Onboarding Completion | Completed / Started | > 80% |
| **Adoption** | Time to First Lead | Hours from signup | < 24 hrs |
| **Retention** | 7-Day Retention | Active day 7 / Signed up | > 85% |
| **Retention** | 30-Day Retention | Active day 30 / Signed up | > 70% |
| **Retention** | 90-Day Retention | Active day 90 / Signed up | > 60% |
| **Task Success** | Lead → Job Rate | Jobs booked / Leads captured | > 60% |
| **Task Success** | Onboarding Task Success | Test call made / Started step 3 | > 90% |

### Implementation

```typescript
// Track HEART metrics
interface HEARTMetrics {
  happiness: {
    nps: number;           // -100 to 100
    csat: number;          // 1 to 5
  };
  engagement: {
    dauMauRatio: number;   // 0 to 1
    notificationTapRate: number;
  };
  adoption: {
    onboardingCompletionRate: number;
    timeToFirstLead: number; // hours
  };
  retention: {
    day7: number;
    day30: number;
    day90: number;
  };
  taskSuccess: {
    leadToJobRate: number;
    onboardingTaskSuccess: number;
  };
}
```

### NPS Survey (Monthly)

Trigger: 30 days after signup, then every 30 days

```
How likely are you to recommend Covered AI to a friend or colleague?

[0] [1] [2] [3] [4] [5] [6] [7] [8] [9] [10]
Not at all likely              Extremely likely

[Optional: What's the main reason for your score?]
```

---

## Mobile Dashboard

### Priority Order (Above Fold)

1. Greeting + period selector
2. Primary metrics (2x2 grid on mobile)
3. Quick action: "View Latest Lead"

### Hidden by Default (Scroll to See)

- Chart (simplified, last 7 days only)
- Recent leads list
- Reviews section
- All-time stats

### Bottom Navigation

```
[📊 Dashboard] [📋 Leads] [📅 Jobs] [⚙️ Settings]
```

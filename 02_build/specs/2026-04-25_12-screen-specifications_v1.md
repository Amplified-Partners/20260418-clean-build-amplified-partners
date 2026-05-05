---
title: "Covered AI — Complete Screen Specifications"
id: "12-screen-specifications"
version: 1
created: "2026-04-25"
type: "document"
topic_type: "spec"
audience: "internal"
layer: "build"
status: "filed"
signed_by: "Devon, 2026-04-25, devin-992682c244cf444f91e0a516498afbfd"
---

# Covered AI — Complete Screen Specifications

## Document Info
- **Version**: 1.0
- **Created**: 2025-01-27
- **Purpose**: Every screen, every state, every interaction
- **Reference**: Use with 11-UI-COMPONENT-REFERENCE.md

---

# SCREEN INDEX

| # | Screen | Route | Priority |
|---|--------|-------|----------|
| 1 | Dashboard | `/dashboard` | Day 1 |
| 2 | Calls List | `/dashboard/calls` | Day 1 |
| 3 | Call Detail | `/dashboard/calls/[id]` | Day 1 |
| 4 | Invoices List | `/dashboard/invoices` | Day 2 |
| 5 | Invoice Detail | `/dashboard/invoices/[id]` | Day 2 |
| 6 | New Invoice | `/dashboard/invoices/new` | Day 2 |
| 7 | Customers List | `/dashboard/customers` | Day 3 |
| 8 | Customer Detail | `/dashboard/customers/[id]` | Day 3 |
| 9 | Jobs List | `/dashboard/jobs` | Day 3 |
| 10 | Job Detail | `/dashboard/jobs/[id]` | Day 3 |
| 11 | New Job | `/dashboard/jobs/new` | Day 3 |
| 12 | Quotes List | `/dashboard/quotes` | Day 3 |
| 13 | Quote Detail | `/dashboard/quotes/[id]` | Day 3 |
| 14 | New Quote | `/dashboard/quotes/new` | Day 3 |
| 15 | Schedule | `/dashboard/schedule` | Day 4 |
| 16 | Reviews | `/dashboard/reviews` | Day 4 |
| 17 | Reports | `/dashboard/reports` | Day 4 |
| 18 | Settings | `/dashboard/settings` | Day 4 |
| 19 | Login | `/login` | Day 1 |
| 20 | Signup | `/signup` | Day 1 |
| 21 | Onboarding Step 1 | `/onboarding/step-1` | Day 1 |
| 22 | Onboarding Step 2 | `/onboarding/step-2` | Day 1 |
| 23 | Onboarding Step 3 | `/onboarding/step-3` | Day 1 |
| 24 | Onboarding Complete | `/onboarding/complete` | Day 1 |

---

# SCREEN 1: DASHBOARD

## Route
`/dashboard`

## Purpose
Single glance shows business health and what needs attention.

## Layout

```
┌─────────────────────────────────────┐
│ Header                              │
│ Good morning, Dave          [?] [⚙]│
├─────────────────────────────────────┤
│                                     │
│ ┌─────────────────────────────────┐ │
│ │ 🔴 NEEDS ATTENTION (3)          │ │
│ │ ├─ Emergency item        [CALL] │ │
│ │ ├─ Overdue invoice      [CHASE] │ │
│ │ └─ Callback needed       [CALL] │ │
│ └─────────────────────────────────┘ │
│                                     │
│ TODAY                               │
│ ┌─────────┬─────────┬─────────┐    │
│ │ 📞 12   │ 💷£2,340│ ⭐ 2    │    │
│ │ Calls   │ Coming  │ Reviews │    │
│ └─────────┴─────────┴─────────┘    │
│                                     │
│ ┌─────────────────────────────────┐ │
│ │ CASH HEALTH           This month│ │
│ │ [████████████░░░] 72%           │ │
│ │ £4,200 of £5,800                │ │
│ │ ⚠️ 3 overdue (£780)    [View]   │ │
│ └─────────────────────────────────┘ │
│                                     │
│ ┌─────────────────────────────────┐ │
│ │ YOUR CUSTOMERS        [View all]│ │
│ │ 142 total │ 34% │ £656 │ 17:1  │ │
│ │ 💡 Insight text here            │ │
│ └─────────────────────────────────┘ │
│                                     │
├─────────────────────────────────────┤
│ [Home] [Calls] [+New] [Inv] [Rep]  │
└─────────────────────────────────────┘
```

## States

### Loading
- Skeleton loaders for each section
- Header shows immediately

### Empty (New User)
- Needs Attention: "All clear" green state
- Stats: Show zeros with "Waiting for your first call"
- Cash Health: Hidden until first invoice
- Customers: Hidden until first customer

### Normal
- As shown in layout

### All Clear
- Needs Attention replaced with green "All clear" card

## Data Requirements

```typescript
interface DashboardData {
  attentionItems: AttentionItem[];
  todayStats: {
    callsToday: number;
    callsTrend: 'up' | 'down' | 'stable';
    revenueThisWeek: number;
    revenueTrend: 'up' | 'down' | 'stable';
    reviewsThisWeek: number;
    reviewsTrend: 'up' | 'down' | 'stable';
  };
  cashHealth: {
    collected: number;
    billed: number;
    overdue: number;
    overdueCount: number;
  };
  unitEconomics: {
    totalCustomers: number;
    repeatRate: number;
    customerLTV: number;
    ltvCacRatio: number;
  };
}
```

## API
```
GET /api/v1/clients/:id/dashboard
```

---

# SCREEN 2: CALLS LIST

## Route
`/dashboard/calls`

## Purpose
View all calls handled by Gemma, filter by status, take action.

## Layout

```
┌─────────────────────────────────────┐
│ Calls                      [Filter] │
├─────────────────────────────────────┤
│                                     │
│ [All] [Callbacks] [Emergency]       │
│                                     │
│ Today                               │
│ ┌─────────────────────────────────┐ │
│ │ 📞 Mrs. Patterson    2 min ago  │ │
│ │    Boiler emergency             │ │
│ │    [⚡Emergency] [Callback]     │ │
│ └─────────────────────────────────┘ │
│ ┌─────────────────────────────────┐ │
│ │ 📞 John Smith       45 min ago  │ │
│ │    Quote request - bathroom     │ │
│ │    [New enquiry]                │ │
│ └─────────────────────────────────┘ │
│                                     │
│ Yesterday                           │
│ ┌─────────────────────────────────┐ │
│ │ 📞 A. Brown          Yesterday  │ │
│ │    Booking confirmed            │ │
│ │    [✓ Resolved]                 │ │
│ └─────────────────────────────────┘ │
│                                     │
└─────────────────────────────────────┘
```

## Filter Tabs
- **All**: All calls
- **Callbacks**: `callbackRequired = true AND callbackCompleted = false`
- **Emergency**: `urgency = EMERGENCY`

## Call Item Display

```typescript
interface CallListItem {
  id: string;
  callerName: string;
  summary: string;
  timeAgo: string;
  urgency: 'emergency' | 'urgent' | 'normal';
  callbackRequired: boolean;
  callbackCompleted: boolean;
  badges: Badge[];
}
```

## Badge Logic
| Condition | Badge |
|-----------|-------|
| `urgency === 'emergency'` | ⚡ Emergency (red) |
| `urgency === 'urgent'` | Urgent (amber) |
| `callbackRequired && !callbackCompleted` | Callback needed (blue) |
| `intent === 'NEW_ENQUIRY'` | New enquiry (green) |
| `callbackCompleted` | ✓ Resolved (grey) |

## Empty State
```
📞
No calls yet
Gemma is ready to answer. Your calls will appear here.
```

## API
```
GET /api/v1/clients/:id/calls?filter=all|callbacks|emergency&page=1
```

---

# SCREEN 3: CALL DETAIL

## Route
`/dashboard/calls/[id]`

## Purpose
View full call details, transcript, take action.

## Layout

```
┌─────────────────────────────────────┐
│ [←] Call Details                    │
├─────────────────────────────────────┤
│                                     │
│ ┌─────────────────────────────────┐ │
│ │ Mrs. Patterson                  │ │
│ │ 📞 07700 900123                 │ │
│ │ 📍 14 Oak Road, SE15 4AA        │ │
│ │                                 │ │
│ │ [Call] [Message] [Create Job]   │ │
│ └─────────────────────────────────┘ │
│                                     │
│ Call Summary                        │
│ ┌─────────────────────────────────┐ │
│ │ Boiler stopped working this     │ │
│ │ morning. No heating or hot      │ │
│ │ water. Customer is elderly and  │ │
│ │ needs urgent attention.         │ │
│ └─────────────────────────────────┘ │
│                                     │
│ Details                             │
│ ┌─────────────────────────────────┐ │
│ │ Time:     Today, 09:23          │ │
│ │ Duration: 2m 34s                │ │
│ │ Intent:   Emergency             │ │
│ │ Status:   Callback needed       │ │
│ └─────────────────────────────────┘ │
│                                     │
│ Transcript                    [▼]   │
│ ┌─────────────────────────────────┐ │
│ │ Gemma: Hi, thanks for calling   │ │
│ │ Dave's Plumbing. I'm Gemma...   │ │
│ │                                 │ │
│ │ Caller: Hello, my boiler's...   │ │
│ └─────────────────────────────────┘ │
│                                     │
├─────────────────────────────────────┤
│ [Mark Callback Complete]            │
└─────────────────────────────────────┘
```

## Actions
| Button | Action |
|--------|--------|
| Call | `tel:` link to caller phone |
| Message | Open WhatsApp/SMS |
| Create Job | Navigate to `/dashboard/jobs/new?callId={id}` |
| Mark Callback Complete | PATCH call, set `callbackCompleted = true` |

## Transcript Toggle
- Collapsed by default (shows first 3 lines)
- Tap to expand full transcript

## API
```
GET /api/v1/clients/:id/calls/:callId
PATCH /api/v1/clients/:id/calls/:callId { callbackCompleted: true }
```

---

# SCREEN 4: INVOICES LIST

## Route
`/dashboard/invoices`

## Layout

```
┌─────────────────────────────────────┐
│ Invoices                    [+ New] │
├─────────────────────────────────────┤
│                                     │
│ ┌─────────┬─────────┬─────────┐    │
│ │ £2,340  │ £780    │ £4,200  │    │
│ │Outstndng│ Overdue │Collected│    │
│ └─────────┴─────────┴─────────┘    │
│                                     │
│ [All] [Draft] [Sent] [Overdue] [Paid]│
│                                     │
│ ┌─────────────────────────────────┐ │
│ │ INV-2025-047   [Overdue]        │ │
│ │ J. Williams • £340              │ │
│ │ 14 days overdue          [Chase]│ │
│ └─────────────────────────────────┘ │
│ ┌─────────────────────────────────┐ │
│ │ INV-2025-048   [Sent]           │ │
│ │ Mrs. Patterson • £285           │ │
│ │ Due in 7 days             [View]│ │
│ └─────────────────────────────────┘ │
│                                     │
└─────────────────────────────────────┘
```

## Summary Cards
| Card | Value | Style |
|------|-------|-------|
| Outstanding | Sum of unpaid invoices | Default |
| Overdue | Sum where `status = OVERDUE` | Danger (red) |
| Collected | Sum where `status = PAID` this month | Success (green) |

## Filter Tabs
- All
- Draft: `status = DRAFT`
- Sent: `status = SENT`
- Overdue: `status = OVERDUE`
- Paid: `status = PAID`

## Invoice Item Actions
| Status | Action Button |
|--------|---------------|
| Draft | Send (primary) |
| Sent | View (secondary) |
| Overdue | Chase (warning) |
| Paid | View (secondary) |

## Empty State
```
📄
No invoices yet
Create your first invoice in 60 seconds.
[Create invoice]
```

## API
```
GET /api/v1/clients/:id/invoices?status=all|draft|sent|overdue|paid&page=1
```

---

# SCREEN 5: INVOICE DETAIL

## Route
`/dashboard/invoices/[id]`

## Layout

```
┌─────────────────────────────────────┐
│ [←] INV-2025-047            [···]  │
├─────────────────────────────────────┤
│                                     │
│ ┌─────────────────────────────────┐ │
│ │         [Overdue]               │ │
│ │                                 │ │
│ │           £340.00               │ │
│ │                                 │ │
│ │ Due: 13 Nov 2025 (14 days ago)  │ │
│ └─────────────────────────────────┘ │
│                                     │
│ Customer                            │
│ ┌─────────────────────────────────┐ │
│ │ J. Williams                     │ │
│ │ 📞 07700 900456                 │ │
│ │ ✉️ j.williams@email.com         │ │
│ └─────────────────────────────────┘ │
│                                     │
│ Items                               │
│ ┌─────────────────────────────────┐ │
│ │ Boiler repair           £280.00 │ │
│ │ Call-out fee             £60.00 │ │
│ │ ─────────────────────────────── │ │
│ │ Subtotal                £340.00 │ │
│ │ VAT (0%)                  £0.00 │ │
│ │ Total                   £340.00 │ │
│ └─────────────────────────────────┘ │
│                                     │
│ Timeline                            │
│ ┌─────────────────────────────────┐ │
│ │ ● Created      1 Nov 2025       │ │
│ │ ● Sent         1 Nov 2025       │ │
│ │ ● Reminder 1   8 Nov 2025       │ │
│ │ ● Reminder 2   15 Nov 2025      │ │
│ │ ○ Payment      Awaiting         │ │
│ └─────────────────────────────────┘ │
│                                     │
├─────────────────────────────────────┤
│ [Send Reminder] [Mark as Paid]      │
└─────────────────────────────────────┘
```

## Status Badge Styles
| Status | Style |
|--------|-------|
| Draft | Grey |
| Sent | Blue |
| Viewed | Blue |
| Reminded | Amber |
| Overdue | Red |
| Paid | Green |

## Actions Menu (···)
- Download PDF
- Resend invoice
- Edit (if Draft)
- Cancel invoice
- Write off

## Bottom Actions
| Status | Primary Action | Secondary Action |
|--------|----------------|------------------|
| Draft | Send Invoice | — |
| Sent | Send Reminder | Mark as Paid |
| Overdue | Send Reminder | Mark as Paid |
| Paid | — | — |

## API
```
GET /api/v1/clients/:id/invoices/:invoiceId
POST /api/v1/clients/:id/invoices/:invoiceId/remind
POST /api/v1/clients/:id/invoices/:invoiceId/mark-paid
```

---

# SCREEN 6: NEW INVOICE

## Route
`/dashboard/invoices/new`

## Query Params
- `?jobId={id}` — Pre-fill from job
- `?customerId={id}` — Pre-fill customer

## Layout
(See 11-UI-COMPONENT-REFERENCE.md for full form)

## Form Fields

| Field | Type | Required | Default |
|-------|------|----------|---------|
| Customer | Search/autocomplete | Yes | — |
| Line items | Array of {description, amount} | Yes (min 1) | — |
| Due date | Select | Yes | 14 days |
| Send immediately | Toggle | No | true |

## Validation
- Customer must be selected or created
- At least one line item
- Line item amounts must be positive numbers

## Pre-fill Logic

**From Job:**
```typescript
if (jobId) {
  const job = await getJob(jobId);
  form.customer = job.customer;
  form.lineItems = [{
    description: job.title,
    amount: job.actualValue || job.estimatedValue
  }];
}
```

**From Customer:**
```typescript
if (customerId) {
  const customer = await getCustomer(customerId);
  form.customer = customer;
}
```

## Submit Action
1. Create invoice
2. If `sendNow`, trigger send-invoice job
3. Show success toast
4. Navigate to invoice detail

## API
```
POST /api/v1/clients/:id/invoices
{
  customerId?: string,
  customerName: string,
  customerEmail: string,
  customerPhone?: string,
  lineItems: Array<{description: string, amount: number}>,
  dueDate: string,
  sendNow: boolean
}
```

---

# SCREEN 7: CUSTOMERS LIST

## Route
`/dashboard/customers`

## Layout

```
┌─────────────────────────────────────┐
│ Customers                   [+ Add] │
├─────────────────────────────────────┤
│                                     │
│ [All] [Active] [Leads] [Inactive]   │
│                                     │
│ Sort: [Lifetime Value ▼]            │
│                                     │
│ ┌─────────────────────────────────┐ │
│ │ 👤 J. Smith                     │ │
│ │    7 jobs • Last: Nov 2025      │ │
│ │    LTV: £2,450           [View] │ │
│ └─────────────────────────────────┘ │
│ ┌─────────────────────────────────┐ │
│ │ 👤 Mrs. Patterson               │ │
│ │    4 jobs • Last: Nov 2025      │ │
│ │    LTV: £1,340           [View] │ │
│ └─────────────────────────────────┘ │
│                                     │
└─────────────────────────────────────┘
```

## Filter Tabs
- All
- Active: `status = ACTIVE`
- Leads: `status = LEAD`
- Inactive: `status = INACTIVE`

## Sort Options
- Lifetime Value (default, descending)
- Most Jobs
- Most Recent
- Name A-Z

## Customer Item Display
```typescript
interface CustomerListItem {
  id: string;
  name: string;
  totalJobs: number;
  lastContactDate: string;
  totalRevenue: number;
}
```

## Empty State
```
👥
No customers yet
Customers are added automatically from calls and jobs.
```

## API
```
GET /api/v1/clients/:id/customers?status=all|active|leads|inactive&sort=ltv|jobs|recent|name&page=1
```

---

# SCREEN 8: CUSTOMER DETAIL

## Route
`/dashboard/customers/[id]`

## Layout

```
┌─────────────────────────────────────┐
│ [←] Customer                 [···]  │
├─────────────────────────────────────┤
│                                     │
│ ┌─────────────────────────────────┐ │
│ │         J. Smith                │ │
│ │ 📞 07700 900123                 │ │
│ │ ✉️ j.smith@email.com            │ │
│ │ 📍 42 High Street, SE1 1AA      │ │
│ │                                 │ │
│ │ [Call] [Email] [Create Job]     │ │
│ └─────────────────────────────────┘ │
│                                     │
│ ┌─────────┬─────────┬─────────┐    │
│ │ 7       │ £2,450  │ £350    │    │
│ │ Jobs    │ Total   │ Avg     │    │
│ └─────────┴─────────┴─────────┘    │
│                                     │
│ Jobs                       [See all]│
│ ┌─────────────────────────────────┐ │
│ │ Boiler service      Nov 2025    │ │
│ │ £285                [Completed] │ │
│ ├─────────────────────────────────┤ │
│ │ Bathroom refit      Oct 2025    │ │
│ │ £1,200              [Completed] │ │
│ └─────────────────────────────────┘ │
│                                     │
│ Invoices                   [See all]│
│ ┌─────────────────────────────────┐ │
│ │ INV-2025-048        Nov 2025    │ │
│ │ £285                    [Paid]  │ │
│ └─────────────────────────────────┘ │
│                                     │
│ Notes                        [Edit] │
│ ┌─────────────────────────────────┐ │
│ │ Prefers morning appointments.   │ │
│ │ Has a dog - ring doorbell.      │ │
│ └─────────────────────────────────┘ │
│                                     │
└─────────────────────────────────────┘
```

## Summary Cards
| Card | Value |
|------|-------|
| Jobs | Total job count |
| Total | Sum of all revenue |
| Avg | Average job value |

## Actions Menu (···)
- Edit customer
- Merge with another
- Mark inactive
- Delete

## API
```
GET /api/v1/clients/:id/customers/:customerId
GET /api/v1/clients/:id/customers/:customerId/history
```

---

# SCREEN 9: JOBS LIST

## Route
`/dashboard/jobs`

## Layout

```
┌─────────────────────────────────────┐
│ Jobs                        [+ New] │
├─────────────────────────────────────┤
│                                     │
│ [List] [Calendar]                   │
│                                     │
│ Today — Wed 27 Nov                  │
│ ┌─────────────────────────────────┐ │
│ │ 09:00  Boiler service           │ │
│ │        Mrs. Patterson           │ │
│ │        SE15 4AA      [Confirmed]│ │
│ └─────────────────────────────────┘ │
│ ┌─────────────────────────────────┐ │
│ │ 14:00  Bathroom quote           │ │
│ │        John Smith               │ │
│ │        SW1A 1AA       [Pending] │ │
│ └─────────────────────────────────┘ │
│                                     │
│ Tomorrow — Thu 28 Nov               │
│ ┌─────────────────────────────────┐ │
│ │ 10:00  Annual service           │ │
│ │        A. Brown                 │ │
│ │        E1 6AN        [Confirmed]│ │
│ └─────────────────────────────────┘ │
│                                     │
└─────────────────────────────────────┘
```

## View Toggle
- **List**: Chronological list grouped by day
- **Calendar**: Week view (see Screen 15)

## Job Item Display
```typescript
interface JobListItem {
  id: string;
  time: string;
  title: string;
  customerName: string;
  postcode: string;
  status: JobStatus;
}
```

## Status Badges
| Status | Style |
|--------|-------|
| Pending | Grey |
| Confirmed | Blue |
| In Progress | Amber |
| Completed | Green |
| Cancelled | Red |
| No Show | Red |

## Empty State
```
📋
No jobs scheduled
Add your first job to get started.
[Add job]
```

## API
```
GET /api/v1/clients/:id/jobs?view=upcoming|past|all&page=1
```

---

# SCREEN 10: JOB DETAIL

## Route
`/dashboard/jobs/[id]`

## Layout

```
┌─────────────────────────────────────┐
│ [←] Job                      [···]  │
├─────────────────────────────────────┤
│                                     │
│ ┌─────────────────────────────────┐ │
│ │ Boiler service                  │ │
│ │ [Confirmed]                     │ │
│ │                                 │ │
│ │ 📅 Wed 27 Nov, 09:00-10:00      │ │
│ │ 📍 14 Oak Road, SE15 4AA        │ │
│ │ 💷 Est. £285                    │ │
│ └─────────────────────────────────┘ │
│                                     │
│ Customer                            │
│ ┌─────────────────────────────────┐ │
│ │ Mrs. Patterson                  │ │
│ │ 📞 07700 900123                 │ │
│ │                                 │ │
│ │ [Call] [Message] [Directions]   │ │
│ └─────────────────────────────────┘ │
│                                     │
│ Notes                               │
│ ┌─────────────────────────────────┐ │
│ │ Annual boiler service.          │ │
│ │ Check pressure and bleed        │ │
│ │ radiators if needed.            │ │
│ └─────────────────────────────────┘ │
│                                     │
│ From Call                   [View]  │
│ ┌─────────────────────────────────┐ │
│ │ Inbound call, 25 Nov 2025       │ │
│ │ "Boiler needs annual service"   │ │
│ └─────────────────────────────────┘ │
│                                     │
├─────────────────────────────────────┤
│ [Start Job]                         │
└─────────────────────────────────────┘
```

## Status-Based Actions

| Current Status | Actions |
|----------------|---------|
| Pending | Confirm, Reschedule, Cancel |
| Confirmed | Start Job, Reschedule, Cancel |
| In Progress | Complete Job, Cancel |
| Completed | Create Invoice, Request Review |

## Bottom Button Logic
| Status | Button |
|--------|--------|
| Pending | Confirm Job |
| Confirmed | Start Job |
| In Progress | Complete Job |
| Completed (no invoice) | Create Invoice |
| Completed (has invoice) | View Invoice |

## API
```
GET /api/v1/clients/:id/jobs/:jobId
PATCH /api/v1/clients/:id/jobs/:jobId { status }
POST /api/v1/clients/:id/jobs/:jobId/complete { actualValue }
```

---

# SCREEN 11: NEW JOB

## Route
`/dashboard/jobs/new`

## Query Params
- `?callId={id}` — Pre-fill from call
- `?customerId={id}` — Pre-fill customer
- `?quoteId={id}` — Pre-fill from accepted quote

## Form Fields

| Field | Type | Required |
|-------|------|----------|
| Title | Text | Yes |
| Customer | Search/autocomplete | Yes |
| Date | Date picker | Yes |
| Time | Time range | No |
| Address | Text (auto from customer) | No |
| Estimated value | Currency | No |
| Notes | Textarea | No |

## API
```
POST /api/v1/clients/:id/jobs
```

---

# SCREEN 12: QUOTES LIST

## Route
`/dashboard/quotes`

## Layout

```
┌─────────────────────────────────────┐
│ Quotes                      [+ New] │
├─────────────────────────────────────┤
│                                     │
│ ┌─────────┬─────────┬─────────┐    │
│ │ 5       │ 2       │ £4,200  │    │
│ │ Pending │ Accepted│ Won     │    │
│ └─────────┴─────────┴─────────┘    │
│                                     │
│ [All] [Draft] [Sent] [Accepted]     │
│                                     │
│ ┌─────────────────────────────────┐ │
│ │ QUO-2025-012   [Sent]           │ │
│ │ John Smith • £2,800             │ │
│ │ Bathroom refit                  │ │
│ │ Valid until 4 Dec        [View] │ │
│ └─────────────────────────────────┘ │
│                                     │
└─────────────────────────────────────┘
```

## Summary Cards
| Card | Value | Style |
|------|-------|-------|
| Pending | Count of sent quotes | Default |
| Accepted | Count this month | Success |
| Won | Value of accepted this month | Success |

## Quote Statuses
| Status | Style |
|--------|-------|
| Draft | Grey |
| Sent | Blue |
| Viewed | Blue |
| Accepted | Green |
| Rejected | Red |
| Expired | Grey |
| Converted | Green |

## API
```
GET /api/v1/clients/:id/quotes?status=all|draft|sent|accepted|rejected&page=1
```

---

# SCREEN 13: QUOTE DETAIL

## Route
`/dashboard/quotes/[id]`

## Layout
Similar to Invoice Detail with:
- Quote-specific status badges
- Valid until date
- Accept/Reject actions for sent quotes
- Convert to Job button for accepted quotes

## Actions by Status
| Status | Primary | Secondary |
|--------|---------|-----------|
| Draft | Send Quote | Edit |
| Sent | — | Resend, Edit |
| Accepted | Convert to Job | — |
| Rejected | Duplicate | — |

## API
```
GET /api/v1/clients/:id/quotes/:quoteId
POST /api/v1/clients/:id/quotes/:quoteId/send
POST /api/v1/clients/:id/quotes/:quoteId/accept
POST /api/v1/clients/:id/quotes/:quoteId/reject
POST /api/v1/clients/:id/quotes/:quoteId/convert
```

---

# SCREEN 14: NEW QUOTE

## Route
`/dashboard/quotes/new`

## Form Fields
Same as New Invoice with:
- Valid until date (default: 14 days)
- No "Send immediately" — always review first

---

# SCREEN 15: SCHEDULE

## Route
`/dashboard/schedule`

## Layout

```
┌─────────────────────────────────────┐
│ Schedule                [+ Block]   │
├─────────────────────────────────────┤
│                                     │
│ ←  November 2025  →                 │
│                                     │
│ Mon Tue Wed Thu Fri Sat Sun         │
│ ┌───┬───┬───┬───┬───┬───┬───┐      │
│ │   │   │ 2 │   │ 1 │   │   │      │
│ └───┴───┴───┴───┴───┴───┴───┘      │
│                                     │
│ Wednesday 27 November               │
│ ┌─────────────────────────────────┐ │
│ │ 09:00-10:00                     │ │
│ │ Boiler service                  │ │
│ │ Mrs. Patterson           [View] │ │
│ ├─────────────────────────────────┤ │
│ │ 10:00-14:00                     │ │
│ │ [Available]                     │ │
│ ├─────────────────────────────────┤ │
│ │ 14:00-15:00                     │ │
│ │ Quote visit                     │ │
│ │ John Smith               [View] │ │
│ ├─────────────────────────────────┤ │
│ │ 15:00-17:00                     │ │
│ │ [Available]                     │ │
│ └─────────────────────────────────┘ │
│                                     │
└─────────────────────────────────────┘
```

## Calendar View
- Week overview showing days with jobs (number badge)
- Tap day to see slots
- Available slots shown in grey

## Slot Types
| Type | Display |
|------|---------|
| Job | Job title, customer name, view button |
| Blocked | "Blocked" in grey |
| Available | "[Available]" - tappable to create job |

## Actions
- Block Time: Create blocked slot
- Tap available slot: Create job for that time

## API
```
GET /api/v1/clients/:id/schedule?date=2025-11-27
POST /api/v1/clients/:id/schedule/slots { date, startTime, endTime, status: 'blocked' }
```

---

# SCREEN 16: REVIEWS

## Route
`/dashboard/reviews`

## Layout

```
┌─────────────────────────────────────┐
│ Reviews                             │
├─────────────────────────────────────┤
│                                     │
│ ┌─────────┬─────────┬─────────┐    │
│ │ ⭐ 4.8  │ 23      │ 78%     │    │
│ │ Average │ Total   │ Response│    │
│ └─────────┴─────────┴─────────┘    │
│                                     │
│ Recent Reviews                      │
│ ┌─────────────────────────────────┐ │
│ │ ⭐⭐⭐⭐⭐  J. Smith              │ │
│ │ "Brilliant service, would      │ │
│ │ definitely recommend!"          │ │
│ │ Google • 2 days ago             │ │
│ └─────────────────────────────────┘ │
│                                     │
│ Pending Requests (3)                │
│ ┌─────────────────────────────────┐ │
│ │ Mrs. Patterson                  │ │
│ │ Requested 3 days ago            │ │
│ │               [Resend] [Skip]   │ │
│ └─────────────────────────────────┘ │
│                                     │
└─────────────────────────────────────┘
```

## Summary Cards
| Card | Value |
|------|-------|
| Average | Average rating (1 decimal) |
| Total | Total review count |
| Response | % of requests that got reviews |

## API
```
GET /api/v1/clients/:id/reviews
POST /api/v1/clients/:id/reviews/request { customerId }
```

---

# SCREEN 17: REPORTS

## Route
`/dashboard/reports`

## Layout

```
┌─────────────────────────────────────┐
│ Reports                [Download]   │
├─────────────────────────────────────┤
│                                     │
│ [This Week] [This Month] [Custom]   │
│                                     │
│ Summary                             │
│ ┌─────────────────────────────────┐ │
│ │ Calls handled:           47     │ │
│ │ Jobs completed:          12     │ │
│ │ Revenue collected:    £4,230    │ │
│ │ New customers:            8     │ │
│ │ Reviews received:         3     │ │
│ └─────────────────────────────────┘ │
│                                     │
│ Cash Flow                           │
│ ┌─────────────────────────────────┐ │
│ │  ████████  Billed: £5,800       │ │
│ │  ██████    Collected: £4,230    │ │
│ └─────────────────────────────────┘ │
│                                     │
│ Top Customers                       │
│ ┌─────────────────────────────────┐ │
│ │ 1. J. Smith         £2,450      │ │
│ │ 2. A. Brown         £1,820      │ │
│ │ 3. M. Patterson     £1,340      │ │
│ └─────────────────────────────────┘ │
│                                     │
│ Calls by Day                        │
│ ┌─────────────────────────────────┐ │
│ │ Mon ████████  12                │ │
│ │ Tue ██████    9                 │ │
│ │ Wed ████████  11                │ │
│ │ Thu ██████    8                 │ │
│ │ Fri ████      7                 │ │
│ └─────────────────────────────────┘ │
│                                     │
└─────────────────────────────────────┘
```

## Time Period Tabs
- This Week
- This Month
- Custom (date range picker)

## Download Action
Generate PDF report

## API
```
GET /api/v1/clients/:id/reports/summary?period=week|month|custom&from=&to=
GET /api/v1/clients/:id/reports/export?format=pdf
```

---

# SCREEN 18: SETTINGS

## Route
`/dashboard/settings`

## Layout

```
┌─────────────────────────────────────┐
│ [←] Settings                        │
├─────────────────────────────────────┤
│                                     │
│ Business                            │
│ ┌─────────────────────────────────┐ │
│ │ Business name              [>]  │ │
│ │ Contact details            [>]  │ │
│ │ Logo                       [>]  │ │
│ └─────────────────────────────────┘ │
│                                     │
│ Phone                               │
│ ┌─────────────────────────────────┐ │
│ │ Your Covered number             │ │
│ │ 0191 743 2732                   │ │
│ │                                 │ │
│ │ Forwarding number          [>]  │ │
│ │ Gemma voice               [>]   │ │
│ │ Greeting message          [>]   │ │
│ │ Emergency keywords        [>]   │ │
│ └─────────────────────────────────┘ │
│                                     │
│ Invoicing                           │
│ ┌─────────────────────────────────┐ │
│ │ Payment terms              [>]  │ │
│ │ Bank details               [>]  │ │
│ │ VAT settings               [>]  │ │
│ └─────────────────────────────────┘ │
│                                     │
│ Integrations                        │
│ ┌─────────────────────────────────┐ │
│ │ Xero                [Connected] │ │
│ │ Google             [Connected]  │ │
│ │ Stripe              [Connect]   │ │
│ └─────────────────────────────────┘ │
│                                     │
│ Account                             │
│ ┌─────────────────────────────────┐ │
│ │ Your plan              [Growth] │ │
│ │ Billing                    [>]  │ │
│ │ Team                       [>]  │ │
│ │ Log out                         │ │
│ └─────────────────────────────────┘ │
│                                     │
└─────────────────────────────────────┘
```

## Settings Sections
Each [>] item navigates to a sub-page for editing.

---

# SCREEN 19-24: AUTH & ONBOARDING

## Login (`/login`)

```
┌─────────────────────────────────────┐
│                                     │
│         [Covered AI Logo]           │
│                                     │
│ ┌─────────────────────────────────┐ │
│ │ Email                           │ │
│ │ [________________________]      │ │
│ │                                 │ │
│ │ Password                        │ │
│ │ [________________________]      │ │
│ │                                 │ │
│ │ [Forgot password?]              │ │
│ │                                 │ │
│ │ [        Log in        ]        │ │
│ │                                 │ │
│ │ Don't have an account?          │ │
│ │ [Sign up]                       │ │
│ └─────────────────────────────────┘ │
│                                     │
└─────────────────────────────────────┘
```

## Signup (`/signup`)

```
┌─────────────────────────────────────┐
│                                     │
│         [Covered AI Logo]           │
│         Start your free trial       │
│                                     │
│ ┌─────────────────────────────────┐ │
│ │ Email                           │ │
│ │ [________________________]      │ │
│ │                                 │ │
│ │ Password                        │ │
│ │ [________________________]      │ │
│ │                                 │ │
│ │ [     Create account     ]      │ │
│ │                                 │ │
│ │ Already have an account?        │ │
│ │ [Log in]                        │ │
│ └─────────────────────────────────┘ │
│                                     │
└─────────────────────────────────────┘
```

## Onboarding Step 1 (`/onboarding/step-1`)

```
┌─────────────────────────────────────┐
│                                     │
│ Step 1 of 3                         │
│ [●○○]                               │
│                                     │
│ Tell us about your business         │
│                                     │
│ ┌─────────────────────────────────┐ │
│ │ Business name                   │ │
│ │ [________________________]      │ │
│ │                                 │ │
│ │ Your name                       │ │
│ │ [________________________]      │ │
│ │                                 │ │
│ │ Business type                   │ │
│ │ [Sole Trader          ▼]        │ │
│ │                                 │ │
│ │ What do you do?                 │ │
│ │ [Plumber  ] [Electrician]       │ │
│ │ [Salon    ] [Vet       ]        │ │
│ │ [Dental   ] [Physio    ]        │ │
│ │ [Other... ]                     │ │
│ └─────────────────────────────────┘ │
│                                     │
├─────────────────────────────────────┤
│ [           Continue           ]    │
└─────────────────────────────────────┘
```

## Onboarding Step 2 (`/onboarding/step-2`)

```
┌─────────────────────────────────────┐
│                                     │
│ Step 2 of 3                         │
│ [●●○]                               │
│                                     │
│ Your phone number is ready          │
│                                     │
│ ┌─────────────────────────────────┐ │
│ │         📞                       │ │
│ │    0191 743 2732                │ │
│ │                                 │ │
│ │  This is your new Covered       │ │
│ │  number. Gemma will answer      │ │
│ │  calls to this number.          │ │
│ │                                 │ │
│ │  [Test it now - call this number]│
│ └─────────────────────────────────┘ │
│                                     │
│ Forward your existing number        │
│ ┌─────────────────────────────────┐ │
│ │ Your current number             │ │
│ │ [________________________]      │ │
│ │                                 │ │
│ │ Your network                    │ │
│ │ [EE                   ▼]        │ │
│ │                                 │ │
│ │ To forward calls, dial:         │ │
│ │ *21*01917432732#                │ │
│ │ [Copy code]                     │ │
│ └─────────────────────────────────┘ │
│                                     │
├─────────────────────────────────────┤
│ [           Continue           ]    │
└─────────────────────────────────────┘
```

## Onboarding Step 3 (`/onboarding/step-3`)

```
┌─────────────────────────────────────┐
│                                     │
│ Step 3 of 3                         │
│ [●●●]                               │
│                                     │
│ Customise Gemma                     │
│                                     │
│ Greeting                            │
│ ┌─────────────────────────────────┐ │
│ │ "Hi, thanks for calling Dave's  │ │
│ │ Plumbing. I'm Gemma, I handle   │ │
│ │ calls for Dave. How can I help?"│ │
│ │                                 │ │
│ │ [Use this] [Customise]          │ │
│ └─────────────────────────────────┘ │
│                                     │
│ Emergency keywords                  │
│ ┌─────────────────────────────────┐ │
│ │ Gemma will flag calls with      │ │
│ │ these words as urgent:          │ │
│ │                                 │ │
│ │ ☑️ Emergency                     │ │
│ │ ☑️ Urgent                        │ │
│ │ ☑️ Flooding                      │ │
│ │ ☑️ Burst                         │ │
│ │ ☐ Leak                          │ │
│ │                                 │ │
│ │ [+ Add custom word]             │ │
│ └─────────────────────────────────┘ │
│                                     │
├─────────────────────────────────────┤
│ [         Finish setup         ]    │
└─────────────────────────────────────┘
```

## Onboarding Complete (`/onboarding/complete`)

```
┌─────────────────────────────────────┐
│                                     │
│              ✓                      │
│                                     │
│       You're live!                  │
│                                     │
│ ┌─────────────────────────────────┐ │
│ │ Gemma is now answering your     │ │
│ │ calls.                          │ │
│ │                                 │ │
│ │ Your number: 0191 743 2732      │ │
│ │ Status: ● Active                │ │
│ └─────────────────────────────────┘ │
│                                     │
│ What happens next:                  │
│                                     │
│ 1. 📞 Calls come in                 │
│    → Gemma answers                  │
│                                     │
│ 2. 💬 You get WhatsApp summaries    │
│    → Review and act                 │
│                                     │
│ 3. 📊 Check your dashboard          │
│    → See everything in one place    │
│                                     │
├─────────────────────────────────────┤
│ [       Go to Dashboard        ]    │
└─────────────────────────────────────┘
```

---

# CLAUDE CODE PROMPT

```
Build all screens for Covered AI using:
- /specs/11-UI-COMPONENT-REFERENCE.md for components
- /specs/12-SCREEN-SPECIFICATIONS.md for layouts

Create these pages in order:

Day 1:
- src/app/(auth)/login/page.tsx
- src/app/(auth)/signup/page.tsx
- src/app/(onboarding)/step-1/page.tsx
- src/app/(onboarding)/step-2/page.tsx
- src/app/(onboarding)/step-3/page.tsx
- src/app/(onboarding)/complete/page.tsx
- src/app/(dashboard)/page.tsx
- src/app/(dashboard)/calls/page.tsx
- src/app/(dashboard)/calls/[id]/page.tsx

Day 2:
- src/app/(dashboard)/invoices/page.tsx
- src/app/(dashboard)/invoices/[id]/page.tsx
- src/app/(dashboard)/invoices/new/page.tsx

Day 3:
- src/app/(dashboard)/customers/page.tsx
- src/app/(dashboard)/customers/[id]/page.tsx
- src/app/(dashboard)/jobs/page.tsx
- src/app/(dashboard)/jobs/[id]/page.tsx
- src/app/(dashboard)/jobs/new/page.tsx
- src/app/(dashboard)/quotes/page.tsx
- src/app/(dashboard)/quotes/[id]/page.tsx
- src/app/(dashboard)/quotes/new/page.tsx

Day 4:
- src/app/(dashboard)/schedule/page.tsx
- src/app/(dashboard)/reviews/page.tsx
- src/app/(dashboard)/reports/page.tsx
- src/app/(dashboard)/settings/page.tsx

Follow the exact layouts in the spec. Use the components from 11-UI-COMPONENT-REFERENCE.md.
Mobile-first. Match dashboard-mockup.html styling.
```

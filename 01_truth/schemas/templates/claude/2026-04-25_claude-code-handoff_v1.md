---
title: "Covered AI v2 - Claude Code Handoff"
id: "claude-code-handoff"
version: 1
created: "2026-04-25"
type: "document"
topic_type: "agent-tooling"
audience: "internal"
layer: "truth"
status: "filed"
signed_by: "Devon, 2026-04-25, devin-992682c244cf444f91e0a516498afbfd"
---

# Covered AI v2 - Claude Code Handoff

## What's Been Built (Ready for Integration)

### Three Complete Apps

#### 1. Client App (`/app/(client)/`)
Mobile-first app for business owners (Ralph, Sarah, etc.)

**Pages Complete:**
- `/home` - 10-second morning check with urgent items, wins, stats
- `/calls` - Call list with filters (all, callbacks, emergency)
- `/calls/[id]` - Call detail with transcript, recording, actions
- `/money` - Invoice tracking with progress bar, chase buttons
- `/more` - Menu with navigation to all features
- `/more/settings` - Gemma config, notifications, forwarding
- `/more/help` - Support articles and contact
- `/more/reviews` - Google review stats and pending requests
- `/more/schedule` - Calendar view with job details
- `/more/customers` - Customer list with search
- `/more/quotes` - Quote management with status filters

**Components:** 18 reusable components in `/components/client-app/`

#### 2. Customer App (`/app/(customer)/`)
End-customer facing pages (Mrs Thompson, Dave, etc.)

**Pages Complete:**
- `/booking/[id]` - Booking confirmation after Gemma books
- `/invoice/[id]` - Invoice payment with card/bank options
- `/review/[id]` - Review request with Google redirect or private feedback

**Features:**
- No login required (magic links)
- Business branded
- Mobile optimized

#### 3. Ewan Admin App (`/app/(ewan)/`)
Command center for founder operations

**Pages Complete:**
- `/command` - Dashboard with system status, metrics, attention items
- `/command/clients` - Client list with health scores, MRR, actions
- `/command/pipeline` - Demo numbers, outreach campaigns, lead funnel

**Features:**
- Dark theme
- Desktop-first
- Real-time status indicators

---

## Directory Structure

```
frontend/src/
├── app/
│   ├── (client)/              # Business owner app
│   │   ├── layout.tsx         # Mobile layout with bottom nav
│   │   ├── home/page.tsx
│   │   ├── calls/
│   │   │   ├── page.tsx
│   │   │   └── [id]/page.tsx
│   │   ├── money/page.tsx
│   │   └── more/
│   │       ├── page.tsx
│   │       ├── settings/page.tsx
│   │       ├── help/page.tsx
│   │       ├── reviews/page.tsx
│   │       ├── schedule/page.tsx
│   │       ├── customers/page.tsx
│   │       └── quotes/page.tsx
│   │
│   ├── (customer)/            # End customer app
│   │   ├── layout.tsx
│   │   ├── booking/[id]/page.tsx
│   │   ├── invoice/[id]/page.tsx
│   │   └── review/[id]/page.tsx
│   │
│   └── (ewan)/                # Admin command center
│       ├── layout.tsx
│       └── command/
│           ├── page.tsx
│           ├── clients/page.tsx
│           └── pipeline/page.tsx
│
├── components/
│   └── client-app/
│       └── index.tsx          # All client app components
│
└── design-tokens.json         # Design system
```

---

## Integration Tasks for Claude Code

### Priority 1: Connect to Real APIs

All pages currently use mock data. Replace with real API calls.

**Client App API Connections:**
```typescript
// Home page
GET /api/dashboard/summary → callsHandled, urgentItems, wins, stats
GET /api/activity/recent → activity feed

// Calls
GET /api/calls?filter={all|callbacks|emergency} → call list
GET /api/calls/:id → call detail with transcript

// Money
GET /api/invoices?status={all|overdue|pending|paid} → invoice list
GET /api/invoices/summary → paid/unpaid totals

// Settings
GET /api/settings/gemma → greeting, keywords, forwarding
PUT /api/settings/gemma → update settings
```

**Customer App API Connections:**
```typescript
// Booking confirmation
GET /api/customer/booking/:id → booking details

// Invoice payment
GET /api/customer/invoice/:id → invoice details
POST /api/customer/invoice/:id/pay → create Stripe session

// Review request
GET /api/customer/review/:id → job details
POST /api/customer/review/:id/feedback → submit private feedback
```

**Admin App API Connections:**
```typescript
// Command center
GET /api/admin/dashboard → system status, metrics, attention items

// Clients
GET /api/admin/clients → client list with health scores
GET /api/admin/clients/:id → client detail

// Pipeline
GET /api/admin/demo-numbers → demo number stats
GET /api/admin/outreach → campaign metrics
GET /api/admin/leads → lead pipeline
```

### Priority 2: Authentication

**Client App:**
- Magic link authentication
- Session management
- Redirect unauthenticated to login

**Customer App:**
- Token-based access from magic links
- No persistent auth needed
- Validate token on each request

**Admin App:**
- Email/password authentication
- Optional 2FA
- Session with longer expiry

### Priority 3: Real-time Updates

**WebSocket Events:**
```typescript
// Client app
ws.on('new_call', () => refresh calls)
ws.on('payment_received', () => show win card)
ws.on('emergency', () => show urgent card)

// Admin app
ws.on('system_status', () => update status indicators)
ws.on('new_signup', () => add to attention items)
```

### Priority 4: Push Notifications

**Client App Notifications:**
- Emergency calls (immediate)
- New leads (batched)
- Payments received (immediate)
- Daily digest (scheduled)

### Priority 5: PWA Setup

**For Client App:**
```json
// manifest.json
{
  "name": "Covered",
  "short_name": "Covered",
  "start_url": "/home",
  "display": "standalone",
  "theme_color": "#2563eb"
}
```

---

## Existing API Routes (Already Built)

Check `/src/api/routes/` for these existing endpoints:

- `auth.py` - Authentication
- `calls.py` - Call management
- `clients.py` - Client CRUD
- `dashboard.py` - Dashboard stats
- `invoices.py` - Invoice management
- `leads.py` - Lead tracking
- `settings.py` - User settings
- `webhooks.py` - Twilio/Vapi webhooks

---

## Design System

**Colors (from design-tokens.json):**
- Primary: #2563eb (blue-600)
- Success: #10b981 (emerald-500)
- Warning: #f59e0b (amber-500)
- Danger: #ef4444 (red-500)

**Mobile Breakpoint:** max-w-md (448px)

**Spacing:** Uses Tailwind defaults

**Components:** All in `/components/client-app/index.tsx`

---

## Testing Routes

After running `npm run dev`:

**Client App:**
- http://localhost:3000/home
- http://localhost:3000/calls
- http://localhost:3000/money
- http://localhost:3000/more

**Customer App:**
- http://localhost:3000/booking/test-id
- http://localhost:3000/invoice/test-id
- http://localhost:3000/review/test-id

**Admin App:**
- http://localhost:3000/command
- http://localhost:3000/command/clients
- http://localhost:3000/command/pipeline

---

## Known Issues / TODOs

1. **No authentication** - All pages accessible without login
2. **Mock data only** - No real API connections
3. **No real-time** - WebSocket not connected
4. **No push notifications** - Service worker not set up
5. **Missing pages:**
   - Invoice creation form
   - Quote creation form
   - Customer detail view
   - Job/schedule creation
   - Greeting editor
   - Emergency keywords editor
   - Client detail view (admin)
   - System status page (admin)

---

## Additional Resources

- `/docs/THREE-APPS-DESIGN.md` - Full design specification
- `/docs/INTEGRATION-MAP.md` - API route mapping
- `/docs/LANDING-PAGE-FRAMEWORK.md` - Marketing page framework
- `/skills/landing-page-builder/` - Reusable landing page skill

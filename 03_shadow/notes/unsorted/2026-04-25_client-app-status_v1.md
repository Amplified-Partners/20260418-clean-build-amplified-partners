---
title: "Client App - Implementation Status"
id: "client-app-status"
version: 1
created: "2026-04-25"
type: "document"
topic_type: "unsorted"
audience: "internal"
layer: "shadow"
status: "filed"
signed_by: "Devon, 2026-04-25, devin-992682c244cf444f91e0a516498afbfd"
---

# Client App - Implementation Status

## What's Been Built

### New Directory Structure
```
frontend/src/
├── app/(client)/               # NEW - Client-facing app
│   ├── layout.tsx              # Mobile-first layout with bottom nav
│   ├── home/page.tsx           # 10-second morning check
│   ├── calls/
│   │   ├── page.tsx            # Call list with filters
│   │   └── [id]/page.tsx       # Call detail with actions
│   ├── money/page.tsx          # Invoice tracking
│   └── more/
│       ├── page.tsx            # Menu
│       └── settings/page.tsx   # Gemma & notification config
├── components/client-app/      # NEW - Reusable components
│   └── index.tsx               # All components
└── design-tokens.json          # Design system
```

### Components Built (18 total)
1. **SmartGreeting** - Contextual greeting based on time and status
2. **AllClearCard** - Positive reinforcement when nothing needs attention
3. **UrgentCard** - Emergency/callback/overdue alerts
4. **WinCard** - Celebrate reviews, payments, milestones
5. **CallbacksSummary** - Quick count of pending callbacks
6. **StatsRow** - Horizontal stat cards
7. **SectionDivider** - Visual separator with optional title
8. **ActivityFeed** - Timeline of events
9. **GemmaStatus** - Always-visible AI status indicator
10. **CallCard** - Single call in list
11. **MoneyProgress** - Visual paid/unpaid bar
12. **InvoiceRow** - Single invoice in list
13. **BottomNav** - Fixed navigation
14. **Header** - Simple header with back button
15. **EmptyState** - Friendly empty state
16. **MenuItem** - Menu item for More page
17. **Toggle** - Settings toggle switch
18. **SettingRow** - Settings row layout

### Design Principles Implemented

**From Don Norman:**
- Clear system status (Gemma active indicator)
- Visibility of system state (All Clear vs Needs Attention)
- Recognition over recall (icons + text)

**From Steve Krug:**
- "Don't make me think" - obvious next actions
- Minimal text, maximum clarity
- One primary action per context

**From Aarron Walter:**
- Warm greeting ("Good morning, Ralph")
- Celebration of wins (reviews, payments)
- Personality through Gemma

**From BJ Fogg:**
- Tiny habits - 10-second morning check
- Immediate feedback - All Clear card
- Reduce friction - one-tap actions

**From Dieter Rams:**
- As little design as possible
- No decorative elements
- Everything serves a purpose

## What's Still Needed

### Client App
- [ ] Help page with articles
- [ ] Reviews page
- [ ] Schedule/calendar view
- [ ] Customers list
- [ ] Quotes management
- [ ] Invoice creation form
- [ ] Greeting editor page
- [ ] Emergency keywords editor
- [ ] Forwarding setup page

### API Integration
- [ ] Connect home page to real dashboard API
- [ ] Connect calls to real calls API
- [ ] Connect money to real invoices API
- [ ] Connect settings to real settings API
- [ ] WebSocket for real-time updates

### Customer App
- [ ] Booking confirmation page
- [ ] Invoice/payment page
- [ ] Review request page
- [ ] Dynamic business branding

### Ewan App
- [ ] Command center
- [ ] Client health view
- [ ] Pipeline view
- [ ] System monitoring

## How to Test

```bash
cd ~/Documents/Baselayer/covered-ai-v2/frontend
npm run dev
```

Then visit:
- http://localhost:3000/home - New client home
- http://localhost:3000/calls - Calls list
- http://localhost:3000/money - Money view
- http://localhost:3000/more - Menu
- http://localhost:3000/more/settings - Settings

## Next Steps

1. **Connect to real APIs** - Replace mock data with API calls
2. **Build remaining pages** - Help, reviews, schedule, customers
3. **Add push notifications** - For emergencies and updates
4. **PWA setup** - Add to home screen capability
5. **Build Customer App** - Invoice payment, review request
6. **Build Ewan App** - Admin command center

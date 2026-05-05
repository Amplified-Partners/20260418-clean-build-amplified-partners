---
title: "Covered AI — Claude Code Build Instructions"
id: "15-claude-code-build-instructions"
version: 1
created: "2026-04-25"
type: "document"
topic_type: "agent-tooling"
audience: "internal"
layer: "truth"
status: "filed"
signed_by: "Devon, 2026-04-25, devin-992682c244cf444f91e0a516498afbfd"
---

# Covered AI — Claude Code Build Instructions

## Document Info
- **Version**: 1.0
- **Created**: 2025-01-27
- **Purpose**: Single prompt for Claude Code to build entire platform
- **Estimated Build Time**: 4 days

---

# PROJECT OVERVIEW

Build a complete business operating system for UK SMEs (trades, vets, salons, etc.).

**Core Features:**
- AI phone answering (Gemma via Vapi)
- Invoice management with auto-chase
- Customer records with LTV tracking
- Job/quote management
- Review requests
- Dashboard with priority feed

**Tech Stack:**
- Next.js 14 (App Router)
- React + TypeScript
- Tailwind CSS
- Prisma + PostgreSQL (Railway)
- Trigger.dev (background jobs)
- Resend (email)
- Twilio (SMS/WhatsApp)
- Vapi (voice AI)
- Stripe (payments)

---

# SPECIFICATION FILES

Read these files in order before building:

1. `/specs/00-MASTER-SYSTEM-DESIGN.md` — Complete system architecture, database schema, API endpoints
2. `/specs/10-VISUAL-DESIGN-SYSTEM.md` — Colours, typography, spacing, design principles
3. `/specs/11-UI-COMPONENT-REFERENCE.md` — Exact component implementations with Tailwind
4. `/specs/12-SCREEN-SPECIFICATIONS.md` — Every screen, every state, every interaction
5. `/specs/13-EMAIL-TEMPLATES.md` — All email templates for Resend
6. `/specs/14-TRIGGER-JOBS.md` — All background job implementations

Visual reference: `/dashboard-mockup.html`

---

# BUILD SEQUENCE

## Day 1: Foundation + Auth + Dashboard

### Step 1: Project Setup
```bash
# Create Next.js app
npx create-next-app@latest covered-ai --typescript --tailwind --app --src-dir

# Install dependencies
npm install @prisma/client @trigger.dev/sdk resend @react-email/components
npm install lucide-react clsx tailwind-merge
npm install -D prisma

# Initialize Prisma
npx prisma init
```

### Step 2: Configure Tailwind
Update `tailwind.config.ts` with the colour palette from `/specs/10-VISUAL-DESIGN-SYSTEM.md`

### Step 3: Database Schema
Copy the complete Prisma schema from `/specs/00-MASTER-SYSTEM-DESIGN.md` Part 3.

Run:
```bash
npx prisma db push
npx prisma generate
```

### Step 4: Core Components
Create all UI components from `/specs/11-UI-COMPONENT-REFERENCE.md`:
- `src/components/ui/Button.tsx`
- `src/components/ui/Input.tsx`
- `src/components/ui/Select.tsx`
- `src/components/ui/Toggle.tsx`
- `src/components/ui/ListItem.tsx`
- `src/components/ui/SummaryCards.tsx`
- `src/components/ui/FilterTabs.tsx`
- `src/components/ui/FixedBottomButton.tsx`
- `src/components/ui/CelebrationModal.tsx`
- `src/components/ui/Toast.tsx`
- `src/components/ui/EmptyState.tsx`

### Step 5: Layout Components
- `src/components/layout/DashboardLayout.tsx`
- `src/components/layout/Header.tsx`
- `src/components/layout/BottomNavigation.tsx`

### Step 6: Dashboard Components
- `src/components/dashboard/NeedsAttentionFeed.tsx`
- `src/components/dashboard/StatCard.tsx`
- `src/components/dashboard/CashHealthBar.tsx`
- `src/components/dashboard/CustomerSnapshot.tsx`

### Step 7: Auth Pages
- `src/app/(auth)/login/page.tsx`
- `src/app/(auth)/signup/page.tsx`
- `src/app/api/auth/login/route.ts`
- `src/app/api/auth/signup/route.ts`

### Step 8: Onboarding Flow
- `src/app/(onboarding)/step-1/page.tsx`
- `src/app/(onboarding)/step-2/page.tsx`
- `src/app/(onboarding)/step-3/page.tsx`
- `src/app/(onboarding)/complete/page.tsx`

### Step 9: Dashboard Page
- `src/app/(dashboard)/page.tsx`
- `src/app/api/v1/clients/[id]/dashboard/route.ts`

### Step 10: Calls Module
- `src/app/(dashboard)/calls/page.tsx`
- `src/app/(dashboard)/calls/[id]/page.tsx`
- `src/app/api/v1/clients/[id]/calls/route.ts`
- `src/app/api/v1/clients/[id]/calls/[callId]/route.ts`

---

## Day 2: Invoicing + Cash Flow

### Step 1: Invoice Pages
- `src/app/(dashboard)/invoices/page.tsx`
- `src/app/(dashboard)/invoices/[id]/page.tsx`
- `src/app/(dashboard)/invoices/new/page.tsx`

### Step 2: Invoice API
- `src/app/api/v1/clients/[id]/invoices/route.ts`
- `src/app/api/v1/clients/[id]/invoices/[invoiceId]/route.ts`
- `src/app/api/v1/clients/[id]/invoices/[invoiceId]/send/route.ts`
- `src/app/api/v1/clients/[id]/invoices/[invoiceId]/remind/route.ts`
- `src/app/api/v1/clients/[id]/invoices/[invoiceId]/mark-paid/route.ts`

### Step 3: Email Templates
Create all invoice emails from `/specs/13-EMAIL-TEMPLATES.md`:
- `src/emails/invoice/invoice-sent.tsx`
- `src/emails/invoice/reminder-1.tsx`
- `src/emails/invoice/reminder-2.tsx`
- `src/emails/invoice/final-notice.tsx`
- `src/emails/invoice/receipt.tsx`

### Step 4: Invoice Trigger Jobs
- `src/trigger/invoices/send-invoice.ts`
- `src/trigger/invoices/invoice-reminder-sequence.ts`
- `src/trigger/invoices/process-payment.ts`
- `src/trigger/invoices/generate-invoice-pdf.ts`

### Step 5: Cash Metrics
- `src/trigger/metrics/update-cash-metrics.ts`
- `src/app/api/v1/clients/[id]/cash-metrics/route.ts`

### Step 6: Stripe Webhook
- `src/app/api/webhooks/stripe/route.ts`

---

## Day 3: Customers + Jobs + Quotes

### Step 1: Customer Pages
- `src/app/(dashboard)/customers/page.tsx`
- `src/app/(dashboard)/customers/[id]/page.tsx`

### Step 2: Customer API
- `src/app/api/v1/clients/[id]/customers/route.ts`
- `src/app/api/v1/clients/[id]/customers/[customerId]/route.ts`
- `src/app/api/v1/clients/[id]/customers/[customerId]/history/route.ts`

### Step 3: Unit Economics
- `src/trigger/metrics/calculate-unit-economics.ts`
- `src/trigger/customers/identify-customer.ts`
- `src/app/api/v1/clients/[id]/unit-economics/route.ts`

### Step 4: Job Pages
- `src/app/(dashboard)/jobs/page.tsx`
- `src/app/(dashboard)/jobs/[id]/page.tsx`
- `src/app/(dashboard)/jobs/new/page.tsx`

### Step 5: Job API
- `src/app/api/v1/clients/[id]/jobs/route.ts`
- `src/app/api/v1/clients/[id]/jobs/[jobId]/route.ts`
- `src/app/api/v1/clients/[id]/jobs/[jobId]/complete/route.ts`

### Step 6: Quote Pages
- `src/app/(dashboard)/quotes/page.tsx`
- `src/app/(dashboard)/quotes/[id]/page.tsx`
- `src/app/(dashboard)/quotes/new/page.tsx`

### Step 7: Quote API
- `src/app/api/v1/clients/[id]/quotes/route.ts`
- `src/app/api/v1/clients/[id]/quotes/[quoteId]/route.ts`
- `src/app/api/v1/clients/[id]/quotes/[quoteId]/send/route.ts`
- `src/app/api/v1/clients/[id]/quotes/[quoteId]/accept/route.ts`
- `src/app/api/v1/clients/[id]/quotes/[quoteId]/convert/route.ts`

---

## Day 4: Schedule + Reviews + Reports + Polish

### Step 1: Schedule Page
- `src/app/(dashboard)/schedule/page.tsx`
- `src/app/api/v1/clients/[id]/schedule/route.ts`
- `src/app/api/v1/clients/[id]/schedule/slots/route.ts`

### Step 2: Reviews
- `src/app/(dashboard)/reviews/page.tsx`
- `src/app/api/v1/clients/[id]/reviews/route.ts`
- `src/trigger/reviews/request-review.ts`
- `src/trigger/reviews/check-new-reviews.ts`
- `src/emails/review/review-request.tsx`

### Step 3: Reports
- `src/app/(dashboard)/reports/page.tsx`
- `src/app/api/v1/clients/[id]/reports/summary/route.ts`
- `src/trigger/reports/weekly-summary.ts`
- `src/emails/reports/weekly-summary.tsx`

### Step 4: Settings
- `src/app/(dashboard)/settings/page.tsx`
- `src/app/api/v1/clients/[id]/settings/route.ts`

### Step 5: Dashboard Jobs
- `src/trigger/dashboard/generate-attention-items.ts`
- `src/trigger/dashboard/calculate-dashboard-stats.ts`

### Step 6: Vapi Webhook
- `src/app/api/webhooks/vapi/route.ts`
- `src/trigger/calls/process-vapi-call.ts`
- `src/trigger/calls/check-missed-callbacks.ts`
- `src/trigger/notifications/send-whatsapp.ts`

### Step 7: Onboarding Emails
- `src/emails/onboarding/welcome.tsx`
- `src/emails/calls/missed-callback.tsx`

### Step 8: Mobile Polish
- Test all pages at 375px width
- Ensure tap targets are 44px minimum
- Fix any layout issues
- Add loading skeletons
- Add error states

---

# ENVIRONMENT VARIABLES

Create `.env`:
```
DATABASE_URL=postgresql://...
JWT_SECRET=...
SESSION_SECRET=...
VAPI_API_KEY=...
TWILIO_ACCOUNT_SID=...
TWILIO_AUTH_TOKEN=...
TWILIO_PHONE_NUMBER=...
RESEND_API_KEY=...
STRIPE_SECRET_KEY=...
STRIPE_WEBHOOK_SECRET=...
TRIGGER_API_KEY=...
NEXT_PUBLIC_APP_URL=http://localhost:3000
```

---

# TESTING CHECKLIST

After each day, verify:

**Day 1:**
- [ ] Can create account
- [ ] Can log in
- [ ] Can complete onboarding
- [ ] Dashboard loads with mock data
- [ ] Calls page shows list
- [ ] Call detail shows transcript

**Day 2:**
- [ ] Can create invoice
- [ ] Can send invoice (email received)
- [ ] Invoice shows in list
- [ ] Reminders trigger on schedule
- [ ] Can mark as paid
- [ ] Cash metrics update

**Day 3:**
- [ ] Customers show with LTV
- [ ] Can create job
- [ ] Can complete job
- [ ] Can create quote
- [ ] Can send quote
- [ ] Unit economics calculate

**Day 4:**
- [ ] Schedule shows slots
- [ ] Review requests send
- [ ] Weekly summary generates
- [ ] Settings save
- [ ] Mobile layout correct
- [ ] All empty states work

---

# DEPLOYMENT

1. Push to GitHub
2. Connect to Railway
3. Add environment variables
4. Deploy
5. Run `npx prisma db push`
6. Configure Trigger.dev
7. Set up Stripe webhook
8. Set up Vapi webhook
9. Test end-to-end

---

# QUALITY STANDARDS

**Code:**
- TypeScript strict mode
- No `any` types
- All props typed
- Error handling on all API routes
- Loading states on all async operations

**Design:**
- Match `/dashboard-mockup.html` exactly
- Use exact Tailwind classes from specs
- Mobile-first responsive
- 44px tap targets
- Inter font throughout

**Performance:**
- Dashboard loads < 2 seconds
- Pages pre-render where possible
- Images optimized
- No layout shift

---

# START HERE

```
Read all spec files:
/specs/00-MASTER-SYSTEM-DESIGN.md
/specs/10-VISUAL-DESIGN-SYSTEM.md
/specs/11-UI-COMPONENT-REFERENCE.md
/specs/12-SCREEN-SPECIFICATIONS.md
/specs/13-EMAIL-TEMPLATES.md
/specs/14-TRIGGER-JOBS.md

Then begin Day 1 build sequence.

Report progress after each step.
Ask for clarification if anything is ambiguous.
```

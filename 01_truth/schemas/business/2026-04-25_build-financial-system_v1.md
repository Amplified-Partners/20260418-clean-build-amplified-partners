---
title: "BUILD: Complete Financial System"
id: "build-financial-system"
version: 1
created: "2026-04-25"
type: "document"
topic_type: "financial-model"
audience: "internal"
layer: "truth"
status: "filed"
signed_by: "Devon, 2026-04-25, devin-992682c244cf444f91e0a516498afbfd"
---

# BUILD: Complete Financial System
## Invoice-to-Cash Pipeline with Stripe & Xero

---

## MISSION

Build a complete financial system that takes Covered AI from manual invoicing to fully automated invoice-to-cash with:
- Professional PDF invoices
- Stripe payment links
- Automatic payment reminders
- Xero accounting sync
- Cash flow dashboard

---

## CURRENT STATE (What Exists)

Based on the codebase review:

**✅ Built:**
- Invoice API with 17 endpoints (`/src/api/routes/invoices.py`)
- Quote API with full CRUD (`/src/api/routes/quotes.py`)
- Invoice list UI with filters (`/frontend/src/app/(dashboard)/invoices/page.tsx`)
- Cash Health Bar component (`/frontend/src/components/dashboard/CashHealthBar.tsx`)
- Basic invoice statuses (DRAFT, SENT, REMINDED, OVERDUE, PAID, CANCELLED, WRITTEN_OFF)

**❌ Not Built:**
- Invoice PDF generation
- Invoice email sending
- Stripe Connect integration
- Payment links on invoices
- Automatic payment reminders
- Xero integration
- Quote PDF generation
- Quote acceptance flow

---

## BUILD PHASES

### PHASE 1: Invoice PDF & Email (Day 1)

**Goal:** Generate professional PDFs and send invoices via email

**Database Changes:**
```prisma
// Add to Invoice model
model Invoice {
  // existing fields...
  pdfUrl              String?
  pdfGeneratedAt      DateTime?
  viewToken           String?   @unique
  sentAt              DateTime?
}

// Add to Client model  
model Client {
  // existing fields...
  address             String?
  logoUrl             String?
  vatNumber           String?
  invoiceTerms        String?   @default("Payment due within 30 days")
  bankAccountName     String?
  bankSortCode        String?
  bankAccountNumber   String?
}
```

**Files to Create:**

1. `src/lib/pdf/invoice-template.tsx` - React-PDF template
   - A4 layout with logo, business info, customer info
   - Line items table with qty, rate, amount
   - Subtotal, VAT (20%), Total
   - Payment details section (bank transfer + payment link)
   - Terms and conditions footer

2. `trigger-jobs/generate-invoice-pdf.ts`
   - Fetch invoice + client data
   - Render PDF using @react-pdf/renderer
   - Upload to S3/R2 storage
   - Update invoice.pdfUrl

3. `emails/invoice.tsx` - React Email template
   - Business logo header
   - Invoice summary box (number, date, due date, amount)
   - "Pay Now" button linking to payment URL
   - PDF attached

4. `trigger-jobs/send-invoice.ts`
   - Generate PDF if not exists
   - Render email template
   - Send via Resend with PDF attachment
   - Update invoice.status = SENT, invoice.sentAt

5. Update `src/api/routes/invoices.py`:
   - POST `/{id}/generate-pdf` - trigger PDF generation
   - GET `/{id}/pdf` - return PDF URL
   - POST `/{id}/send` - trigger send job

6. `frontend/src/components/invoices/InvoicePdfPreview.tsx`
   - Preview iframe showing PDF
   - Download button
   - Send button with loading state

**Dependencies:**
```bash
npm install @react-pdf/renderer @react-email/components resend
```

---

### PHASE 2: Stripe Payments (Day 2)

**Goal:** Accept online payments via Stripe Connect

**Database Changes:**
```prisma
model StripeAccount {
  id                  String   @id @default(cuid())
  clientId            String   @unique
  client              Client   @relation(fields: [clientId], references: [id])
  stripeAccountId     String   @unique  // acct_xxx
  chargesEnabled      Boolean  @default(false)
  payoutsEnabled      Boolean  @default(false)
  onboardingComplete  Boolean  @default(false)
  createdAt           DateTime @default(now())
  updatedAt           DateTime @updatedAt
}

model PaymentEvent {
  id              String   @id @default(cuid())
  invoiceId       String
  invoice         Invoice  @relation(fields: [invoiceId], references: [id])
  eventType       String   // payment_intent.succeeded, etc
  stripeEventId   String   @unique
  eventData       Json
  createdAt       DateTime @default(now())
}

// Add to Invoice model
model Invoice {
  // existing + phase 1 fields...
  stripePaymentIntentId  String?
  paymentLinkUrl         String?
  paymentLinkId          String?
  stripeChargeId         String?
  paidAt                 DateTime?
  paidAmount             Decimal?
  paymentMethod          String?   // stripe, bank_transfer, cash
}
```

**Files to Create:**

1. `src/api/routes/stripe_connect.py`
   - POST `/create-account` - Create Express connected account
   - GET `/onboarding-link` - Get/refresh onboarding URL
   - GET `/status` - Check account status
   - GET `/dashboard-link` - Link to Stripe Express dashboard
   - DELETE `/` - Disconnect account

2. `src/api/routes/invoice_payments.py`
   - POST `/{id}/create-payment-link` - Create Stripe Payment Link
   - GET `/{id}/payment-status` - Check payment status

3. `src/api/routes/stripe_webhooks.py`
   - POST `/stripe` - Handle Stripe webhooks
   - Verify signature with STRIPE_WEBHOOK_SECRET
   - Handle: checkout.session.completed, payment_intent.succeeded, payment_intent.payment_failed, account.updated
   - On payment success: Update invoice status=PAID, paidAt, paidAmount

4. `frontend/src/components/settings/StripeConnectCard.tsx`
   - Not connected: "Connect Stripe" button
   - Onboarding incomplete: "Continue Setup" button
   - Connected: Status indicators, "Open Dashboard" link

5. `frontend/src/components/invoices/PaymentLinkButton.tsx`
   - Create payment link if not exists
   - Copy link button
   - Open link button

6. `frontend/src/app/(dashboard)/settings/payments/page.tsx`
   - Stripe Connect card
   - Payment settings

**Environment Variables:**
```env
STRIPE_SECRET_KEY=sk_live_xxx
STRIPE_WEBHOOK_SECRET=whsec_xxx
```

---

### PHASE 3: Auto-Chase (Day 3)

**Goal:** Automatically remind customers about overdue invoices

**Database Changes:**
```prisma
// Add to Invoice model
model Invoice {
  // existing fields...
  reminder1SentAt     DateTime?
  reminder2SentAt     DateTime?
  finalNoticeSentAt   DateTime?
}

// Add to Client model
model Client {
  // existing fields...
  autoChaseEnabled       Boolean @default(true)
  reminder1Days          Int     @default(7)   // Days after due
  reminder2Days          Int     @default(14)
  reminder3Days          Int     @default(21)
}
```

**Reminder Sequence:**
- Day 7 overdue: Friendly reminder ("Just a gentle reminder...")
- Day 14 overdue: Firm reminder ("This invoice is now significantly overdue...")
- Day 21 overdue: Final notice ("Final notice before further action...")

**Files to Create:**

1. `emails/invoice-reminder-1.tsx` - Friendly tone
2. `emails/invoice-reminder-2.tsx` - Firm tone
3. `emails/invoice-reminder-final.tsx` - Urgent, red banner

4. `trigger-jobs/check-overdue-invoices.ts`
   - Cron: Daily at 9am (`0 9 * * *`)
   - Find invoices where dueDate < now AND status not PAID
   - Mark as OVERDUE if not already
   - Check days overdue vs client settings
   - Trigger appropriate reminder if not already sent

5. `trigger-jobs/send-invoice-reminder.ts`
   - Accept invoiceId + reminderType (1, 2, final)
   - Render appropriate email template
   - Send via Resend
   - Update reminder{N}SentAt timestamp

6. Update `src/api/routes/invoices.py`:
   - POST `/{id}/send-reminder` - Manual reminder trigger
   - GET `/overdue` - List overdue invoices

7. `frontend/src/components/invoices/ReminderTimeline.tsx`
   - Visual timeline showing: Sent → Due → Reminder 1 → Reminder 2 → Final
   - Check marks for completed steps
   - Status indicators (green/amber/red)

8. `frontend/src/components/settings/ChaseSettingsForm.tsx`
   - Toggle auto-chase on/off
   - Configure reminder days

---

### PHASE 4: Xero Integration (Day 4-5)

**Goal:** Sync invoices to Xero for accountant

**Database Changes:**
```prisma
model XeroConnection {
  id                  String   @id @default(cuid())
  clientId            String   @unique
  client              Client   @relation(fields: [clientId], references: [id])
  tenantId            String   // Xero org ID
  tenantName          String?
  accessToken         String   @db.Text  // ENCRYPTED
  refreshToken        String   @db.Text  // ENCRYPTED
  tokenExpiresAt      DateTime
  autoSyncInvoices    Boolean  @default(true)
  lastSyncAt          DateTime?
  lastSyncError       String?
  connected           Boolean  @default(true)
  createdAt           DateTime @default(now())
  updatedAt           DateTime @updatedAt
}

// Add to Invoice model
model Invoice {
  // existing fields...
  xeroInvoiceId       String?
  xeroContactId       String?
  xeroSyncedAt        DateTime?
  xeroSyncError       String?
}
```

**CRITICAL: Token Encryption**

Create `src/lib/encryption.ts`:
```typescript
import crypto from "crypto";

const ALGORITHM = "aes-256-gcm";
const KEY = Buffer.from(process.env.ENCRYPTION_KEY!, "base64");

export function encrypt(text: string): string {
  const iv = crypto.randomBytes(16);
  const cipher = crypto.createCipheriv(ALGORITHM, KEY, iv);
  let encrypted = cipher.update(text, "utf8", "hex");
  encrypted += cipher.final("hex");
  const authTag = cipher.getAuthTag();
  return `${iv.toString("hex")}:${authTag.toString("hex")}:${encrypted}`;
}

export function decrypt(encrypted: string): string {
  const [ivHex, authTagHex, data] = encrypted.split(":");
  const iv = Buffer.from(ivHex, "hex");
  const authTag = Buffer.from(authTagHex, "hex");
  const decipher = crypto.createDecipheriv(ALGORITHM, KEY, iv);
  decipher.setAuthTag(authTag);
  let decrypted = decipher.update(data, "hex", "utf8");
  decrypted += decipher.final("utf8");
  return decrypted;
}
```

**Files to Create:**

1. `src/api/routes/xero.py` - OAuth flow
   - GET `/connect` - Generate auth URL, redirect to Xero
   - GET `/callback` - Exchange code for tokens, store encrypted
   - GET `/status` - Check connection status
   - DELETE `/` - Disconnect

2. `src/api/routes/xero_sync.py` - Sync operations
   - POST `/invoices/{id}/sync-to-xero` - Sync single invoice
   - POST `/sync-all` - Sync all unsynced invoices

3. `trigger-jobs/refresh-xero-tokens.ts`
   - Cron: Hourly (`0 * * * *`)
   - Find connections expiring in next 2 hours
   - Refresh tokens, update database

4. `trigger-jobs/sync-invoice-to-xero.ts`
   - Decrypt access token
   - Create/find Xero contact
   - Create Xero invoice with line items
   - Update invoice.xeroInvoiceId

5. `frontend/src/components/settings/XeroConnectionCard.tsx`
   - Not connected: "Connect Xero" button
   - Connected: Org name, last sync, auto-sync toggle

6. `frontend/src/app/(dashboard)/settings/accounting/page.tsx`

**Environment Variables:**
```env
XERO_CLIENT_ID=xxx
XERO_CLIENT_SECRET=xxx
XERO_REDIRECT_URI=https://app.covered.ai/api/v1/xero/callback
ENCRYPTION_KEY=xxx  # Generate with: openssl rand -base64 32
```

---

### PHASE 5: Financial Dashboard (Day 6)

**Goal:** Cash flow visibility and reports

**API Endpoints to Create:**

1. Update `src/api/routes/dashboard.py`:
   - GET `/financial-summary` - Total billed, collected, outstanding, overdue
   - GET `/revenue-trend` - Last 6 months chart data
   - GET `/payment-forecast` - Expected income next 30 days
   - GET `/outstanding-invoices` - Top 5 unpaid invoices

2. Create `src/api/routes/reports.py`:
   - GET `/cash-flow` - Cash flow report for date range
   - GET `/cash-flow/export` - CSV export
   - GET `/vat` - VAT report for quarter

**Frontend Components:**

1. `frontend/src/components/dashboard/CashFlowOverview.tsx`
   - Progress bar: collected vs billed
   - Stats: Billed, Collected, Outstanding
   - Overdue warning with count

2. `frontend/src/components/dashboard/RevenueChart.tsx`
   - Bar chart using recharts
   - 6 months of revenue data
   - Trend indicator (up/down %)

3. `frontend/src/components/dashboard/OutstandingInvoicesWidget.tsx`
   - List of unpaid invoices
   - Status indicators (red=overdue, amber=due soon, green=pending)
   - Chase button for overdue

4. `frontend/src/components/dashboard/PaymentForecast.tsx`
   - Expected income by week
   - Based on due dates

5. `frontend/src/app/(dashboard)/reports/page.tsx`
   - Tabs: Cash Flow, VAT
   - Date range picker
   - Export buttons

**Dependencies:**
```bash
npm install recharts
```

---

### PHASE 6: Quote Documents (Day 7)

**Goal:** Quote PDFs with customer acceptance flow

**Database Changes:**
```prisma
// Add to Quote model
model Quote {
  // existing fields...
  pdfUrl              String?
  pdfGeneratedAt      DateTime?
  viewToken           String?   @unique
  viewedAt            DateTime?
  acceptedAt          DateTime?
  rejectedAt          DateTime?
  rejectionReason     String?
}

// Add to Client model
model Client {
  // existing fields...
  quoteTerms          String?
  quoteValidDays      Int       @default(30)
}
```

**Files to Create:**

1. `src/lib/pdf/quote-template.tsx` - Similar to invoice but with "QUOTE" header, valid until date

2. `emails/quote.tsx` - Quote email with Accept button

3. `trigger-jobs/send-quote.ts` - Generate PDF, send email

4. `src/api/routes/quote_public.py` - Public (no auth) endpoints
   - GET `/view/{token}` - Get quote details for viewing
   - POST `/view/{token}/respond` - Accept or reject quote

5. `frontend/src/app/quotes/view/[token]/page.tsx` - Public quote view
   - Quote details
   - Accept/Reject buttons
   - Optional rejection reason
   - Success/error states

---

## ENVIRONMENT VARIABLES SUMMARY

```env
# Stripe
STRIPE_SECRET_KEY=sk_live_xxx
STRIPE_WEBHOOK_SECRET=whsec_xxx

# Xero
XERO_CLIENT_ID=xxx
XERO_CLIENT_SECRET=xxx
XERO_REDIRECT_URI=https://app.covered.ai/api/v1/xero/callback

# Email
RESEND_API_KEY=re_xxx

# Storage (for PDFs)
AWS_ACCESS_KEY_ID=xxx
AWS_SECRET_ACCESS_KEY=xxx
AWS_REGION=eu-west-2
PDF_STORAGE_BUCKET=covered-invoices
PDF_CDN_URL=https://cdn.covered.ai/invoices

# Security
ENCRYPTION_KEY=xxx
INVOICE_VIEW_SECRET=xxx
```

---

## BUILD ORDER

1. **Phase 1** - Start here. Get invoices sending with PDFs.
2. **Phase 2** - Add payment links to those invoices.
3. **Phase 3** - Auto-chase unpaid invoices.
4. **Phase 4** - Sync to Xero for accountants.
5. **Phase 5** - Dashboard to see cash flow.
6. **Phase 6** - Quote documents and acceptance.

Each phase builds on the previous. Test each phase before moving to the next.

---

## START COMMAND

Begin with Phase 1:

1. Add database fields to Invoice and Client models
2. Run migration: `npx prisma migrate dev --name invoice-pdf-fields`
3. Install dependencies: `npm install @react-pdf/renderer @react-email/components resend`
4. Create the PDF template
5. Create the Trigger.dev jobs
6. Create the email template
7. Update the API routes
8. Create the frontend preview component
9. Test end-to-end: Create invoice → Generate PDF → Send email

Then proceed to Phase 2.

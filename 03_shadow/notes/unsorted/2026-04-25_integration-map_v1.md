---
title: "Covered AI - System Integration Map"
id: "integration-map"
version: 1
created: "2026-04-25"
type: "document"
topic_type: "unsorted"
audience: "internal"
layer: "shadow"
status: "filed"
signed_by: "Devon, 2026-04-25, devin-992682c244cf444f91e0a516498afbfd"
---

# Covered AI - System Integration Map

## Current State Analysis

After reviewing the codebase, here's what exists and how everything connects.

---

## ✅ ALREADY BUILT (Backend + Frontend)

### Core Infrastructure
| Component | Location | Status |
|-----------|----------|--------|
| FastAPI Backend | `src/api/main.py` | ✅ Running |
| PostgreSQL DB | `prisma/schema.prisma` | ✅ 50+ tables |
| Next.js Frontend | `frontend/` | ✅ Running |
| Trigger.dev Jobs | `trigger-jobs/` | ✅ 20+ jobs |

### API Routes (39 route files)
| Route | File | Purpose |
|-------|------|---------|
| `/auth` | auth.py | Login, magic links, sessions |
| `/onboarding` | onboarding.py | 3-step signup flow |
| `/clients` | clients.py | CRUD for businesses |
| `/leads` | leads.py | Lead management |
| `/jobs` | jobs.py | Job scheduling |
| `/calls` | calls.py | Call history |
| `/invoices` | invoices.py | Invoice CRUD + PDF |
| `/quotes` | quotes.py | Quote management |
| `/reviews` | reviews.py | Google review tracking |
| `/webhooks` | webhooks.py | Vapi/Twilio/Stripe |
| `/porting` | porting.py | Number porting |
| `/nurture` | nurture.py | 12-touch sequences |
| `/demo-numbers` | demo_numbers.py | Personalized demos |
| `/outreach` | outreach.py | Cold email campaigns |
| `/events` | events.py | Webhook event log |
| `/provisioning` | provisioning.py | Client setup automation |
| `/website-builder` | website_builder.py | Auto website generation |
| `/photo-studio` | photo_studio.py | AI photo processing |
| `/stripe` | stripe_connect.py | Payment connect |
| `/xero` | xero.py, xero_sync.py | Accounting sync |
| `/geo` | geo.py | SEO pages |
| `/settings` | settings.py | Client config |
| `/dashboard` | dashboard.py | Stats & metrics |
| `/reports` | reports.py | Reporting |
| `/training` | training.py | Onboarding videos |

### Services (Backend Logic)
| Service | File | Purpose |
|---------|------|---------|
| Demo Numbers | `services/demo_numbers.py` | Provision Twilio numbers |
| Cold Outreach | `services/cold_outreach.py` | Campaign management |
| Event Log | `services/event_log.py` | Webhook logging |
| Client Provisioning | `services/client_provisioning.py` | Auto-setup |
| Website Builder | `services/website_builder/` | Site generation |
| Photo Studio | `services/photo_studio/` | Image AI |
| Porting | `services/porting_service.py` | Number porting |
| LOA Generator | `services/loa_generator.py` | PDF generation |
| Nurture Sequences | `services/nurture_sequences.py` | Email sequences |
| Lead Service | `services/lead_service.py` | Lead handling |
| Notifications | `services/notification_service.py` | SMS/Email |

### Frontend Pages
| Page | Location | Purpose |
|------|----------|---------|
| Dashboard | `(dashboard)/page.tsx` | Main client view |
| Calls | `(dashboard)/calls/` | Call history |
| Jobs | `(dashboard)/jobs/` | Job management |
| Invoices | `(dashboard)/invoices/` | Invoice management |
| Quotes | `(dashboard)/quotes/` | Quote management |
| Reviews | `(dashboard)/reviews/` | Review tracking |
| Settings | `(dashboard)/settings/` | Client settings |
| Reports | `(dashboard)/reports/` | Analytics |
| Customers | `(dashboard)/customers/` | CRM |
| Schedule | `(dashboard)/schedule/` | Calendar view |
| Geo | `(dashboard)/geo/` | SEO pages |
| **Admin** | | |
| Admin Home | `admin/page.tsx` | Overview |
| Admin Clients | `admin/clients/` | Client management |
| Admin Porting | `admin/porting/` | Porting requests |
| Admin Demos | `admin/demos/` | Demo numbers |
| Admin Outreach | `admin/outreach/` | Campaigns |
| Admin Events | `admin/events/` | Event log |
| Admin System | `admin/system/` | Health check |
| **Auth** | | |
| Login | `(auth)/` | Auth flow |
| **Onboarding** | | |
| Step 1-3 | `(onboarding)/` | Signup flow |

### Scheduled Jobs (Trigger.dev)
| Job | File | Schedule |
|-----|------|----------|
| Invoice Chasing | invoice-chasing.ts | Daily 9am |
| Overdue Check | check-overdue-invoices.ts | Daily 9am |
| Dashboard Stats | dashboard-stats.ts | Hourly |
| Unit Economics | unit-economics.ts | Daily |
| Lead Nurture | lead-nurture.ts | Hourly |
| Review Requests | review-request.ts | Daily |
| Weekly Summary | weekly-summary.ts | Weekly |
| Morning Digest | morning-digest.ts | Daily 7am |
| Outreach Processor | outreach-processor.ts | Hourly |
| GEO Page Gen | geo-page.ts | Daily |
| Video Generation | video-generation.ts | On demand |
| Event Cleanup | cleanup-events.ts | Daily 3am |
| Xero Token Refresh | refresh-xero-tokens.ts | Every 30min |
| Action Metrics | aggregate-action-metrics.ts | Daily |
| PDF Generation | generate-invoice-pdf.ts | On demand |

---

## 📋 NEW MODULES (Specs Written, Not Yet Built)

| # | Module | Spec Location | Priority |
|---|--------|---------------|----------|
| 6 | Website Builder | `docs/modules/06-WEBSITE-BUILDER.md` | Medium |
| 7 | Photo Studio | `docs/modules/07-PHOTO-STUDIO.md` | Medium |
| 8 | Client Dashboard | `docs/modules/08-CLIENT-DASHBOARD.md` | HIGH |
| 9 | Landing Page | `docs/modules/09-LANDING-PAGE.md` | HIGH |
| 10 | Google Reviews | `docs/modules/10-GOOGLE-REVIEWS.md` | Medium |
| 11 | Referral System | `docs/modules/11-REFERRAL-SYSTEM.md` | Medium |
| 12 | Analytics | `docs/modules/12-ANALYTICS.md` | Medium |
| 13 | Support System | `docs/modules/13-SUPPORT-SYSTEM.md` | Medium |

**Note:** Modules 1-5 appear to already have partial implementations in the codebase.

---

## 🔗 INTEGRATION GAPS

### 1. Missing Connections

| Gap | What's Missing | Fix |
|-----|----------------|-----|
| Reviews → Dashboard | Review stats not in dashboard | Add to `dashboard-stats.ts` |
| Outreach → Analytics | Campaign metrics not tracked | Add to analytics service |
| Demo Numbers → Referrals | Demo conversions not linked | Add referral attribution |
| Website → Hosting | Generated sites not deployed | Add deployment service |
| Photos → Websites | Photos not auto-used | Connect photo studio to builder |

### 2. Frontend Gaps

| Page | Issue | Fix |
|------|-------|-----|
| Client Dashboard | Uses admin structure | Need separate client-facing UI |
| Marketing Site | Doesn't exist | Build from Module 9 spec |
| Help Center | Not implemented | Build from Module 13 spec |
| Referral Portal | Not implemented | Build from Module 11 spec |

### 3. Missing Routes in main.py

```python
# These routes exist as files but aren't mounted:
# (None found - all routes appear to be mounted)
```

---

## 🔧 INTEGRATION TASKS

### Phase 1: Connect Existing Systems (1-2 days)

1. **Wire up all dashboard stats**
   ```python
   # In dashboard-stats.ts, add:
   - demo_numbers_active
   - outreach_campaigns_active  
   - reviews_this_week
   - nurture_sequences_active
   ```

2. **Connect events to all services**
   ```python
   # Every service should log to EventLog:
   await event_log.log(
       source="service_name",
       event_type="action_type",
       client_id=client_id,
       payload=data
   )
   ```

3. **Add missing webhooks to unified handler**
   ```python
   # webhooks_v2.py should handle:
   - Demo number calls → record_call + provision tracking
   - Outreach email events → update lead status
   - Review notifications → update review tracking
   ```

### Phase 2: Build Client-Facing Experience (3-5 days)

1. **Client Dashboard (Module 8)**
   - Separate from admin
   - Mobile-first
   - Simple: calls, leads, settings

2. **Marketing Site (Module 9)**
   - Landing page with 0800 COVERED
   - Vertical pages
   - Pricing page

3. **Help Center (Module 13)**
   - Searchable articles
   - Forwarding code generator
   - Support tickets

### Phase 3: Growth Features (5-7 days)

1. **Referral System (Module 11)**
   - Referrer dashboard
   - Commission tracking
   - Share links

2. **Analytics (Module 12)**
   - Business metrics
   - Client health scores
   - Cohort analysis

3. **Review Automation (Module 10)**
   - Auto-request after jobs
   - Review monitoring
   - Schema markup

---

## 📊 DATA FLOW

```
                                    ┌─────────────────┐
                                    │   MARKETING     │
                                    │   SITE          │
                                    │ (covered.ai)    │
                                    └────────┬────────┘
                                             │
                                             ▼
┌─────────────┐    ┌─────────────┐    ┌─────────────┐
│   DEMO      │    │  ONBOARDING │    │  REFERRAL   │
│   NUMBERS   │───▶│  (3 steps)  │◀───│  SYSTEM     │
└─────────────┘    └──────┬──────┘    └─────────────┘
                          │
                          ▼
              ┌───────────────────────┐
              │   CLIENT PROVISIONING │
              │   - Create Vapi agent │
              │   - Assign number     │
              │   - Configure webhooks│
              │   - Send welcome      │
              └───────────┬───────────┘
                          │
         ┌────────────────┼────────────────┐
         ▼                ▼                ▼
┌─────────────┐    ┌─────────────┐    ┌─────────────┐
│   VAPI      │    │   TWILIO    │    │   STRIPE    │
│   (calls)   │    │   (phone)   │    │   (billing) │
└──────┬──────┘    └──────┬──────┘    └──────┬──────┘
       │                  │                  │
       └──────────────────┼──────────────────┘
                          │
                          ▼
              ┌───────────────────────┐
              │   WEBHOOK HANDLER     │
              │   (events.py)         │
              └───────────┬───────────┘
                          │
     ┌────────────────────┼────────────────────┐
     ▼                    ▼                    ▼
┌─────────┐        ┌─────────────┐        ┌─────────┐
│  LEADS  │        │  EVENT LOG  │        │ INVOICES│
└────┬────┘        └─────────────┘        └────┬────┘
     │                                         │
     ▼                                         ▼
┌─────────────┐                          ┌─────────────┐
│  NURTURE    │                          │   XERO      │
│  SEQUENCES  │                          │   SYNC      │
└─────────────┘                          └─────────────┘
     │
     ▼
┌─────────────┐    ┌─────────────┐    ┌─────────────┐
│   JOBS      │───▶│  REVIEWS    │───▶│  GEO PAGES  │
└─────────────┘    └─────────────┘    └─────────────┘
```

---

## 🚀 RECOMMENDED BUILD ORDER

### Week 1: Core Client Experience
1. ✅ Verify all existing routes work
2. ✅ Test demo number flow end-to-end
3. 🔨 Build Module 8 (Client Dashboard) - NEW UI
4. 🔨 Build Module 9 (Landing Page) - Marketing site

### Week 2: Growth & Analytics
5. 🔨 Build Module 11 (Referral System)
6. 🔨 Build Module 12 (Analytics Dashboard)
7. 🔨 Connect all metrics to admin dashboard

### Week 3: Support & Polish
8. 🔨 Build Module 13 (Support System)
9. 🔨 Build Module 10 (Review Automation)
10. 🔨 Polish and integrate

---

## 🔌 API INTEGRATION CHECKLIST

### For Claude Code to Build:

```
When building any module, ensure:

1. Service file goes in: src/services/
2. Route file goes in: src/api/routes/
3. Add route to: src/api/main.py
4. Add Prisma model to: prisma/schema.prisma
5. Add Trigger job to: trigger-jobs/
6. Add frontend pages to: frontend/src/app/
7. Update this integration doc
```

### Environment Variables Needed:
```bash
# Already configured
DATABASE_URL=
VAPI_API_KEY=
TWILIO_ACCOUNT_SID=
TWILIO_AUTH_TOKEN=
STRIPE_SECRET_KEY=
RESEND_API_KEY=
OPENAI_API_KEY=

# May need adding
REPLICATE_API_KEY=        # For photo studio
REMOVE_BG_API_KEY=        # For background removal
GOOGLE_PLACES_API_KEY=    # For reviews
HEYGEN_API_KEY=           # For video generation
```

---

## 📁 FILE STRUCTURE TARGET

```
covered-ai-v2/
├── src/
│   ├── api/
│   │   ├── main.py                 # FastAPI app
│   │   └── routes/
│   │       ├── analytics.py        # NEW
│   │       ├── client_dashboard.py # NEW  
│   │       ├── referrals.py        # NEW
│   │       ├── support.py          # NEW
│   │       └── ... (existing)
│   ├── services/
│   │   ├── analytics/              # NEW
│   │   ├── referrals/              # NEW
│   │   ├── support/                # NEW
│   │   └── ... (existing)
│   └── db/
│       └── client.py
├── frontend/
│   └── src/
│       └── app/
│           ├── (client)/           # NEW - Client dashboard
│           ├── (marketing)/        # NEW - Public site
│           ├── (admin)/            # Existing admin
│           ├── (auth)/             # Existing auth
│           └── (onboarding)/       # Existing onboarding
├── trigger-jobs/
│   ├── referral-payouts.ts         # NEW
│   ├── analytics-aggregator.ts     # NEW
│   └── ... (existing)
├── prisma/
│   └── schema.prisma               # Add new models
└── docs/
    └── modules/
        ├── 01-DEMO-NUMBERS.md      # ✅ Built
        ├── 02-COLD-OUTREACH.md     # ✅ Partially built
        ├── 03-ADMIN-DASHBOARD.md   # ✅ Built
        ├── 04-WEBHOOK-EVENTS.md    # ✅ Built
        ├── 05-CLIENT-PROVISIONING.md # ✅ Built
        ├── 06-WEBSITE-BUILDER.md   # ✅ Service exists
        ├── 07-PHOTO-STUDIO.md      # ✅ Service exists
        ├── 08-CLIENT-DASHBOARD.md  # 🔨 Needs new frontend
        ├── 09-LANDING-PAGE.md      # 🔨 Needs building
        ├── 10-GOOGLE-REVIEWS.md    # 🔨 Partial (reviews.py exists)
        ├── 11-REFERRAL-SYSTEM.md   # 🔨 Needs building
        ├── 12-ANALYTICS.md         # 🔨 Partial (dashboard.py)
        └── 13-SUPPORT-SYSTEM.md    # 🔨 Needs building
```

---

## ✅ NEXT IMMEDIATE ACTIONS

1. **Run the system and verify existing functionality**
   ```bash
   cd ~/Documents/Baselayer/covered-ai-v2
   # Backend
   python -m uvicorn src.api.main:app --reload
   # Frontend
   cd frontend && npm run dev
   ```

2. **Apply latest Prisma schema**
   ```bash
   npx prisma db push
   ```

3. **Build Module 9 (Landing Page) first** - it's the entry point for customers

4. **Then Module 8 (Client Dashboard)** - what customers see after signup

5. **Then Module 11 (Referrals)** - growth engine

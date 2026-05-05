---
title: "Product Factory Spec"
id: "08-product-factory"
version: 1
created: "2026-04-25"
type: "document"
topic_type: "unsorted"
audience: "internal"
layer: "shadow"
status: "filed"
signed_by: "Devon, 2026-04-25, devin-992682c244cf444f91e0a516498afbfd"
---

# Product Factory Spec

## Overview

An AI agent that auto-generates standalone SaaS products from Covered AI's core features, targeting specific verticals with niche branding and messaging.

---

## Purpose

1. **Lead Generation** — Standalone products capture leads for Covered AI
2. **Market Testing** — Test messaging and pricing in specific verticals
3. **SEO/Discoverability** — Niche domains rank for specific searches
4. **Lower Barrier** — Free/cheap entry points reduce friction

---

## Core Features to Repurpose

| Feature | Description | Standalone Potential |
|---------|-------------|---------------------|
| AI Phone | Gemma answers calls 24/7 | AfterHours.ai, VetLine.ai |
| Reviews | Automated review requests | VetReview.ai, SalonStars.uk |
| Nurture | 12-touch follow-up | FollowUp.bot, QuoteChaser.ai |
| Booking | Calendar/scheduling | BookingBot.uk, SalonBooker.uk |
| Analytics | Call tracking/reporting | MissedCall.report, CallScore.ai |

---

## Target Verticals

Priority order based on market research:

1. Veterinary
2. Salon/Beauty
3. Trades (Plumber, Electrician, Builder)
4. Dental
5. Physio/Chiropractic
6. Automotive
7. Legal
8. Accounting
9. Fitness
10. Property/Estate Agents

---

## Product Generation Flow

### Step 1: Input

```typescript
interface ProductInput {
  coreFeature: 'phone' | 'reviews' | 'nurture' | 'booking' | 'analytics';
  vertical: string;
  pricingModel: 'free' | 'freemium' | 'paid';
}
```

### Step 2: Agent Generates

```typescript
interface GeneratedProduct {
  // Identity
  name: string;           // "VetReview.ai"
  slug: string;           // "vetreview"
  domain: string;         // "vetreview.ai"
  tagline: string;        // "Get more 5-star reviews. Automatically."
  
  // Copy
  heroHeadline: string;
  heroSubheadline: string;
  problemPoints: string[];
  benefits: string[];
  socialProof: string;
  
  // Pricing
  freeLimit?: number;     // e.g., 5 reviews/month
  paidPrice?: number;     // e.g., 29
  
  // Assets
  landingPageHtml: string;
  emailTemplates: EmailTemplate[];
}

interface EmailTemplate {
  name: string;           // 'welcome', 'value', 'upsell'
  subject: string;
  html: string;
  sendDay: number;        // days after signup
}
```

### Step 3: Deployment

1. Create Netlify site
2. Deploy landing page
3. Add domain to Resend
4. Create email templates
5. Connect to central Lead database
6. Start tracking metrics

---

## Agent System Prompt

```markdown
# Product Factory Agent

You create standalone SaaS products from Covered AI's core features.

## Messaging Principles
- Lead with pain, not features
- Use specific numbers (£15K, 2 hours, 47 businesses)
- Include social proof
- Clear single CTA
- Mobile-first design

## Naming Conventions
- Short (1-2 words max)
- Include .ai, .uk, or .io
- Verb+Noun or Niche+Feature format
- Examples: VetReview.ai, MissedCall.report, BookingBot.uk

## Pricing Strategy
- Free: Capture leads, show value, upsell to Covered AI
- Freemium: Free tier with limit, paid removes limit
- Paid: £29-49/mo for standalone, positions Covered AI as better value

## Landing Page Structure (12 parts)
1. Hero (headline + CTA)
2. Problem agitation
3. Demo/video
4. How it works (3 steps)
5. Benefits (4 items)
6. Trust signals
7. Case study
8. Pricing
9. FAQ
10. Final CTA
11. Footer

## Email Sequence (6 emails → Covered AI)
1. Day 0: Welcome + quick start
2. Day 3: Value delivered ("You got X reviews")
3. Day 7: Case study (similar business)
4. Day 14: Problem reveal ("The calls you're missing")
5. Day 21: Covered AI intro
6. Day 28: Offer (£100 off first month)

## Output Format
Return valid JSON matching GeneratedProduct interface.
```

---

## Database Schema

```prisma
model Product {
  id              String   @id @default(uuid())
  
  // Identity
  name            String
  slug            String   @unique
  domain          String?
  
  // Source
  coreFeature     String   @map("core_feature")
  vertical        String
  
  // Pricing
  pricingModel    String   @map("pricing_model")
  freeLimit       Int?     @map("free_limit")
  paidPrice       Decimal? @map("paid_price") @db.Decimal(10, 2)
  
  // Copy
  tagline         String
  heroHeadline    String   @map("hero_headline")
  heroSubheadline String   @map("hero_subheadline")
  
  // Deployment
  netlifyUrl      String?  @map("netlify_url")
  netlifySiteId   String?  @map("netlify_site_id")
  resendDomainId  String?  @map("resend_domain_id")
  
  // Metrics
  signups         Int      @default(0)
  paidConversions Int      @default(0) @map("paid_conversions")
  coveredUpsells  Int      @default(0) @map("covered_upsells")
  
  // Status
  status          ProductStatus @default(draft)
  
  createdAt       DateTime @default(now()) @map("created_at")
  updatedAt       DateTime @updatedAt @map("updated_at")
  
  leads           Lead[]
  emailTemplates  ProductEmailTemplate[]
  
  @@map("products")
}

enum ProductStatus {
  draft
  deployed
  paused
  archived
}

model ProductEmailTemplate {
  id        String  @id @default(uuid())
  productId String  @map("product_id")
  
  name      String  // 'welcome', 'value', 'upsell'
  subject   String
  html      String  @db.Text
  sendDay   Int     @map("send_day")
  
  resendTemplateId String? @map("resend_template_id")
  
  product   Product @relation(fields: [productId], references: [id])
  
  @@unique([productId, name])
  @@map("product_email_templates")
}
```

---

## API Endpoints

### Generate Product
```
POST /api/v1/products/generate

Body:
{
  "coreFeature": "reviews",
  "vertical": "vet",
  "pricingModel": "freemium"
}

Response:
{
  "id": "uuid",
  "name": "VetReview.ai",
  "slug": "vetreview",
  "domain": "vetreview.ai",
  "status": "draft",
  ...
}
```

### Deploy Product
```
POST /api/v1/products/:id/deploy

Response:
{
  "netlifyUrl": "https://vetreview.netlify.app",
  "customDomain": "vetreview.ai",
  "resendDomain": "verified"
}
```

### List Products
```
GET /api/v1/products

Response:
{
  "products": [...],
  "total": 5
}
```

### Product Metrics
```
GET /api/v1/products/:id/metrics

Response:
{
  "signups": 147,
  "paidConversions": 12,
  "coveredUpsells": 8,
  "conversionRate": 0.082,
  "upsellRate": 0.054
}
```

---

## Trigger.dev Jobs

### generate-product
- Input: coreFeature, vertical, pricingModel
- Calls Claude to generate product concept
- Checks domain availability
- Saves to database
- Returns draft product

### deploy-product
- Input: productId
- Creates Netlify site
- Deploys landing page
- Adds domain to Resend
- Creates email templates
- Updates status to 'deployed'

### product-nurture
- Runs daily
- Finds leads ready for next email
- Sends appropriate template
- Updates nurture stage
- Triggers Covered AI upsell at day 21

### product-metrics
- Runs hourly
- Updates signup counts
- Calculates conversion rates
- Flags underperforming products

---

## Lead → Covered AI Funnel

```
Standalone Signup
       ↓
  Welcome Email (Day 0)
       ↓
  Value Email (Day 3)
       ↓
  Case Study (Day 7)
       ↓
  Problem Reveal (Day 14)
       ↓
  Covered AI Intro (Day 21)
       ↓
  Offer Email (Day 28)
       ↓
  [Converts to Covered AI Client]
       OR
  [Stays on Standalone Product]
       OR
  [Churns]
```

---

## Implementation Priority

| Phase | Task |
|-------|------|
| 1 | Add Product + ProductEmailTemplate to Prisma schema |
| 2 | Create generate-product Trigger.dev job |
| 3 | Create deploy-product Trigger.dev job |
| 4 | Build API endpoints |
| 5 | Create admin dashboard UI |
| 6 | Build first product: MissedCall.report |
| 7 | Test full funnel: signup → nurture → upsell |

---

## First Product: MissedCall.report

Easiest to build, most direct path to Covered AI:

- **Feature:** Analytics (call tracking)
- **Vertical:** All
- **Pricing:** Free
- **Hook:** "See how many calls you're missing"
- **Upsell:** "Stop missing them with Gemma"

Details in separate spec: `09-missedcall-report.md`

---
title: "BDB Sales: Comprehensive Digital Marketing + HubSpot Outbound Strategy 2026"
id: "bdb-hubspot-strategy-v1"
version: 1
created: "2026-04-25"
type: "document"
topic_type: "strategy"
audience: "internal"
layer: "truth"
status: "filed"
signed_by: "Devon, 2026-04-25, devin-992682c244cf444f91e0a516498afbfd"
---

# BDB Sales: Comprehensive Digital Marketing + HubSpot Outbound Strategy 2026
## Complete Integrated System: Website → Social → Email → Video → Sales Automation

**BUSINESS:** BDB Sales (Ewan Bramley)
**GOAL:** Build fully integrated digital marketing machine that:
- Automates lead capture and nurturing
- Scales video content production (10+ educational videos)
- Drives traffic from website + LinkedIn + email
- Funnels prospects into automated sales sequences
- Tracks everything back to revenue

---

## PART 1: THE ECOSYSTEM ARCHITECTURE (How Everything Connects)

### Your Marketing Funnel

```
AWARENESS LAYER
    ↓
[Website Blog] → [LinkedIn Posts] → [Email Newsletter] → [YouTube Videos]
    ↓
    ↓
ENGAGEMENT LAYER
    ↓
[Landing Page] → [Lead Magnet (Free Audit)] → [Nurture Email Sequence]
    ↓
    ↓
CONSIDERATION LAYER
    ↓
[Educational Videos] → [Case Study Content] → [Webinars/Live] → [Sales Email Sequence]
    ↓
    ↓
DECISION LAYER
    ↓
[Discovery Call Booking] → [Proposal] → [Closed Deal]
```

**The 2026 Advantage:** All of this is automated through HubSpot + integrations. No manual work after setup.

---

## PART 2: HUBSPOT CORE SETUP (Your Command Center)

### What HubSpot Is (For Your Situation)

**HubSpot** = The nervous system connecting every part of your marketing. It:
- Captures leads from website/ads
- Scores leads by engagement level
- Sends automated email sequences
- Tracks every interaction
- Integrates with LinkedIn, email, calendar, Zapier
- Reports on ROI by channel

**Cost:** £0-£150/month depending on contacts (free tier perfect for SMBs)

### Your HubSpot Setup (4 Core Hubs)

#### 1. MARKETING HUB (Attract & Nurture Leads)

**What it does:**
- Landing page builder (captures leads from ads, email clicks)
- Email marketing automation (send sequences to 100s of prospects automatically)
- Forms (embedded on website to capture details)
- Lead scoring (automatically identifies hot prospects)
- Blog/CMS integration (SEO tracking)

**Your setup:**
- [ ] Create 2 landing pages:
  1. "Free SMB Marketing Audit" (Lead magnet page)
  2. "90-Day Transformation Sprint" (Sales page)
- [ ] Create 3 email automation sequences:
  1. Welcome sequence (5 emails over 10 days)
  2. Lead magnet delivery (3 emails teaching them + 1 sales email)
  3. Abandoned booking sequence (3 emails re-engaging people who visited discovery call page)
- [ ] Create lead scoring rule:
  - +10 points for email open
  - +20 points for landing page visit
  - +50 points for download
  - +100 points for booking call
  - **Hot lead threshold: 100+ points → trigger sales alert**

**Automation example:**
```
Prospect lands on "Free Audit" page
    ↓
Fills form with name, email, business challenge
    ↓
HubSpot sends email #1 immediately: "Thanks! Here's your audit roadmap"
    ↓
Day 3: Email #2: "The #1 mistake SMBs make (and how to fix it)"
    ↓
Day 5: Email #3: "Case study: How [Business] increased revenue 45%"
    ↓
Day 7: Email #4: "Ready for your personalized audit? Book a call here"
    ↓
If no action: Day 10: Email #5: "Last chance to get your free audit"
```

**Result:** Prospect goes from stranger to warm lead in 10 days, automatically.

---

#### 2. SALES HUB (Move Prospects to Deals)

**What it does:**
- Tracks when prospects open emails
- Suggests follow-up timing
- Creates deal pipeline (shows which prospects are in what stage)
- Automatically notifies you when someone books a call
- Integrates with Calendly (booking syncs automatically)

**Your setup:**
- [ ] Create 5-stage pipeline:
  1. **Lead** (Someone who downloaded something or signed up)
  2. **MQL** (Marketing Qualified Lead - scored 100+, engaged)
  3. **Discovery Call Booked** (Person scheduled call)
  4. **Proposal Sent** (You sent proposal)
  5. **Won Deal** (Signed contract)
  
- [ ] Create automatic workflow:
  ```
  IF deal moves to "Discovery Call Booked"
  THEN send Slack notification to Ewan + send prospect calendar confirmation email
  ```

- [ ] Create sales sequence for deals:
  ```
  After discovery call:
    ↓
  Email #1 (same day): "Great meeting you! Here's what we discussed..."
    ↓
  Email #2 (day 3): "Quick question - where are you leaning?"
    ↓
  Email #3 (day 7): "Let's move forward with this. Here's next steps..."
    ↓
  If no response (day 10): "One more check-in before I move on..."
  ```

---

#### 3. EMAIL MARKETING INTEGRATION

**What happens:**
- Every email you send is tracked (opens, clicks, replies)
- Clicks trigger actions (e.g., "clicked the discovery call link" = sales sequence starts)
- Replies go to sales queue (so you never miss a response)
- Unsubscribes are automatic (compliance)

**Your sequences:**

**Sequence 1: Welcome (New Email Subscriber)**
```
Email #1 (immediately):
Subject: "Welcome to BDB Sales - Here's your first insight"
Body: 
- Warm greeting + who you are (30 years building dental practice)
- Problem statement (most SMB owners work 60+ hours/week)
- What you'll send them (weekly insights)
- CTA: "Get your free resource: SMB Owner's Quick Win Checklist"
- P.S. "Reply to this email with your biggest challenge"

Triggers: Lead scoring +5 for reply
```

```
Email #2 (day 3):
Subject: "The #1 reason your marketing feels like guesswork"
Body:
- Short story from your dental practice (relatable)
- Problem identification (likely their main challenge)
- One quick action they can take today
- Link to relevant blog post
- CTA: "Ready to go deeper? Book a free consultation"
```

```
Email #3 (day 7):
Subject: "How [Client Name] stopped working 60+ hours/week"
Body:
- Case study narrative (challenge → approach → results)
- Specific numbers (£45K new revenue, 20 fewer hours/week)
- Testimonial quote from client
- "This could be you in 90 days"
- CTA: "Let's map out your transformation. Book a call"
```

```
Email #4 (day 14):
Subject: "My closing thoughts for you..."
Body:
- Warm, personal message
- Summarize what you've shared
- Reinforce main offer (free audit or discovery call)
- "If you're not ready yet, totally fine. I'll be here when you are."
```

```
Email #5 (day 21):
Subject: "Can I ask you something?"
Body:
- Questions like "What held you back?" or "Not the right fit?"
- Reinforce offer one more time
- Soft close
```

**Sequence 2: Lead Magnet Delivery (Free Audit)**
```
Email #1 (immediately):
Subject: "Your Free SMB Marketing Audit - Inside"
Body:
- "I've created a custom audit framework..."
- Attach/link to audit PDF
- "This typically costs £497. Today, it's yours free."
- CTA: "Ready to implement? Let's talk"

Result: +50 lead score points
```

```
Email #2 (day 5):
Subject: "Got a minute? Quick question about your audit..."
Body:
- "Noticed you downloaded the audit. Any quick wins already?"
- Short, personal follow-up
- "If you want help implementing, book a call"
```

---

#### 4. OPERATIONS HUB (Data Sync + Automation)

**What it does:**
- Keeps data clean (no duplicates)
- Syncs contact info across all tools
- Runs automations (e.g., "if contact is UK-based AND service business AND £1M revenue → high-priority account")
- Generates reports (shows which campaigns drive most revenue)

**Your setup:**
- [ ] Integrate Calendly (booking syncs to HubSpot deal)
- [ ] Integrate LinkedIn (lead source tracking)
- [ ] Integrate email (all email data captured)
- [ ] Integrate Gmail (sales emails tracked)
- [ ] Integrate Zapier (custom integrations to tools)

---

## PART 3: SOCIAL MEDIA STRATEGY (LinkedIn + YouTube Focus)

### Why LinkedIn First

**LinkedIn 2026 Reality:**
- 36% YoY video growth
- Algorithm rewards "meaningful conversation" over likes
- B2B decision-makers spend 45+ min/day on platform
- Direct link to Thought Leadership = Direct to Sales

**Your LinkedIn Strategy:**

#### LinkedIn Company Page Setup

```
Company Name: BDB Sales
URL: linkedin.com/company/bdb-sales
Profile Photo: Your professional headshot
Banner: Professional image + "Helping UK SMBs Transform" tagline
Description: 
  "BDB Sales helps overwhelmed SMB owner-operators (£0-2M revenue) 
   systemize their business, multiply leads, and reclaim their time.
   
   30 years building & running a dental practice.
   Now consulting 150+ UK SMBs.
   
   Free resources: SMB audit, transformation checklist, weekly insights."

Website link: bdbsales.com
Phone: [Your UK number]
Address: Byker, Newcastle, UK
Employees: 1-10 (you, plus potentially contractors)

CTA Button: "Get Audit" (links to landing page)
```

#### LinkedIn Content Calendar (52 Weeks)

**Publishing schedule:** 4 times per week (Mon, Wed, Fri, Sun)

**Content mix:**
- 40% Educational (teaching your method)
- 30% Case studies (proof)
- 20% Personal stories (relatability)
- 10% Community engagement (commenting on others' posts)

**Content types:**

**Type 1: "Carousel" Posts (Most Engaging)**
```
Multiple slides showing step-by-step process or comparison:

Slide 1: "Most SMB owners think their problem is [X]..."
Slide 2: "But the REAL problem is [Y]..."
Slide 3: "Here's why [Z] matters..."
Slide 4: "90% of SMBs miss this..."
Slide 5: "Here's how to fix it..."
Slide 6: "Quick action you can take today..."
Slide 7: "Want a custom plan? Comment 'AUDIT' below"

Best for: Driving engagement + collecting leads
Posts per week: 2
```

**Type 2: "Video Posts" (Highest reach)**
```
45-90 second short educational video:
- Your face on camera (builds trust)
- Screen recording of example
- Text overlay with key points
- Clear CTA at end ("Discover more on my blog" or "Book a call link")

Topics:
- "3 mistakes costing you £20K/month"
- "The system that doubled my lead generation"
- "Why your team isn't following your process"
- "The 1 metric that matters most"

Best for: Authority building + referral traffic
Posts per week: 1
```

**Type 3: "Article Posts" (Long-form, High Value)**
```
LinkedIn Article (published directly on LinkedIn, not shared from blog):
- 800-1,200 words
- Same topic as blog posts but LinkedIn-optimized tone
- Opens with question/story
- Concludes with CTA to blog or discovery call

Topics:
- "Why traditional consultants are failing SMB owners"
- "30 years in business taught me these 5 things..."
- "The hidden cost of not having systems"

Best for: Deep positioning + LinkedIn algorithm boost
Posts per month: 4
```

**Type 4: "Comment Engagement"**
```
Every day (5-10 minutes):
- Find 3-4 posts in your network about SMBs, business, or marketing
- Leave thoughtful 2-3 sentence comment (not just emoji)
- Reply to anyone who comments on your posts (within 2 hours if possible)

Best for: Building community, increasing reach
Time investment: 10 min/day
```

#### LinkedIn Ads (Optional But Recommended)

**Budget:** £200-500/month to test

**Campaign 1: Lead Magnet**
```
Objective: Lead generation (to free audit)
Audience: UK, job titles (owner, founder, MD), industries (dental, hairdressing, vet, etc.)
Landing page: Your free audit page
Budget: £100/month
Expected: 20-30 lead forms submitted/month at ~£4-5 per lead

Ad creative: Video of you explaining the audit, or carousel showing 3 problems the audit solves
Headline: "Get Your Free SMB Marketing Audit (Usually £497)"
CTA: "Get Free Audit"
```

**Campaign 2: Thought Leadership**
```
Objective: Engagement + reach
Audience: Similar (UK SMB owners)
Content: Top-performing organic posts promoted
Budget: £100/month
Expected: 2-3x reach boost on best posts

Ad creative: Reuse top-performing carousel or video posts
Headline: [Post headline]
CTA: "Learn More"
```

---

### YouTube Strategy (Owned Content)

**Why YouTube:**
- 2nd largest search engine (after Google)
- Videos rank for 76% longer than blog posts
- YouTube transcriptions indexed by AI search (ChatGPT, Gemini, Perplexity cite videos)
- Building 12-month content library = evergreen authority

**Channel Setup:**

```
Channel Name: BDB Sales
Channel Art: Professional banner (1,500 x 500px)
Channel Description:
  "Educational videos for UK SMB owner-operators struggling with:
   - Inconsistent leads
   - Time poverty
   - Marketing confusion
   - Team productivity
   
   30-year entrepreneur sharing what actually works.
   Free resources, no fluff, real results.
   
   New video every Thursday.
   Subscribe for weekly insights."

Channel URL: youtube.com/@bdbsales

Playlists:
- "Lead Generation for SMBs" (10+ videos)
- "Team Scaling & Automation" (10+ videos)
- "Direct Response Marketing" (10+ videos)
- "My Story & Case Studies" (5+ videos)
```

**Video Content Plan (96 Videos, Year 1)**

**Video Type 1: "Quick Tips" (5-8 minutes)**
```
Format: You on camera (head-on) + screen recording
Topics:
- "The #1 lead generation mistake I see"
- "How to delegate without micromanaging"
- "The 3-email sequence that sells"
- "Why your CRM implementation failed"

Production: AI video tool (Mootion or HeyGen) can automate this
Publishing: 2x per week
Total year 1: 100+ videos
```

**Video Type 2: "Case Studies" (12-15 minutes)**
```
Format: You narrating + client testimonial video + results graphics
Structure:
- Client intro (who they are)
- Challenge they faced (specific problem)
- Solution you provided (step-by-step)
- Results (specific numbers)
- Client testimonial (their quote on camera)
- Your lessons learned
- How to apply this

Topics: Your 3-4 best case studies
Production: Hybrid (client interview + you narrating)
Publishing: 1x per month
Total year 1: 12 videos
```

**Video Type 3: "Long-Form Interviews" (30-45 minutes)**
```
Format: You + guest (former client or fellow expert) in conversation
Topics:
- "30 Years Running a Practice & What I Learned"
- "Why SMBs Fail at Marketing (And How to Fix It)"
- "The Systems That Let Me Reclaim My Time"

Production: Screen recording of Zoom call + simple edit
Publishing: 1x per month
Total year 1: 12 videos
```

**Video Type 4: "Educational Series" (3-5 minute mini-course)**
```
Format: Structured mini-course broken into 5-7 short videos
Example series: "Your First Lead Generation System"
  - Video 1: "Why your current approach isn't working"
  - Video 2: "The 4 channels that actually work"
  - Video 3: "Setting up your first email sequence"
  - Video 4: "Testing and optimization"
  - Video 5: "Measuring what works"

Production: AI video tool (can automate entire series)
Publishing: One series per month
Total year 1: 60 videos (5 series × 12 videos each)
```

**YouTube SEO (Ranking Videos in Search)**

Every video needs:
- [ ] Title: Keyword-focused, question-based (e.g., "How to Generate Leads for Your Salon in 2026")
- [ ] Description: 300+ words with links, timestamps, keywords
- [ ] Tags: 10-15 relevant tags (e.g., "lead generation," "SMB marketing," "small business")
- [ ] Transcript: Add full transcript (auto-caption + upload manual if needed)
- [ ] Playlist: Assign to relevant playlist (groups similar videos)
- [ ] CTA: End screen + pinned comment with link to blog/booking

**YouTube Monetization (Optional):**
- Videos can generate ad revenue (small initially)
- More importantly: video embeds drive traffic to your website
- Transcriptions get indexed by Google + AI search engines

---

## PART 4: AI VIDEO GENERATION SYSTEM (10+ Videos Fast)

### Why AI Video Matters in 2026

**Numbers:**
- 96% of UK marketers consider video essential
- 89% report direct sales from video
- Traditional production: £10K per video, 4-6 weeks
- AI production: £500-1K per video, 1-3 days

**Your advantage:** Generate 100+ videos in year 1 at fraction of traditional cost

### Best AI Video Tools for Your Use Case

#### Tool 1: **Mootion** (Recommended for Complete Videos)
- **Best for:** Turning blog posts → complete marketing videos
- **Features:** Text-to-video, automatic editing, voiceovers, avatars
- **Cost:** £50-200/month depending on video count
- **Speed:** 3-minute video in under 2 minutes (65% faster than competitors)
- **How it works:**
  ```
  Step 1: Input your blog post or script
  Step 2: Mootion generates full video with:
    - AI voiceover (multiple accents, languages)
    - Stock footage/animations
    - Text overlays
    - Color grading
  Step 3: Review + customize (add your branding)
  Step 4: Download + post to YouTube, LinkedIn, TikTok
  ```

#### Tool 2: **HeyGen** (Best for Personalization)
- **Best for:** Creating multiple versions of same video for different segments
- **Features:** Avatar cloning, video translation (40+ languages), lip-sync
- **Cost:** £50-300/month
- **Unique ability:** Create one video, automatically translate to 10+ languages with lip-sync
- **How to use:**
  ```
  Create 1 video script about lead generation
    ↓
  Generate in English with your face/avatar
    ↓
  Auto-translate to Spanish, French, German, Portuguese (for European SMBs)
    ↓
  Each version has lip-sync (looks like you speaking)
    ↓
  Post each to regional LinkedIn, YouTube channels
  ```

#### Tool 3: **InVideo AI** (Best for Social Media Content)
- **Best for:** Generating short-form videos (60-90 seconds) for LinkedIn, TikTok
- **Features:** Text-to-video, templates by platform, automatic captions
- **Cost:** £25-100/month
- **How to use:**
  ```
  Each week:
  - 3 blog posts written
  - Each becomes 3-4 short videos (30s, 60s, 90s versions)
  - One for LinkedIn, one for TikTok, one for Instagram Reels
  - All auto-subtitled, auto-optimized for platform
  ```

### Your Video Production Workflow (Weekly)

**Monday-Tuesday: Content Creation**
- Write 2 blog posts (as outlined in previous documents)
- Create 1-2 video scripts

**Wednesday: Video Generation**
- Input scripts into Mootion OR InVideo AI
- Generate 5-10 video variations
- Customize with your logo/branding
- Add CTAs (link to blog, discovery call booking)

**Thursday: Video Publishing**
- Upload to YouTube (with proper titles, descriptions, tags)
- Post on LinkedIn (native video upload)
- Share on TikTok if applicable
- Pin comments with CTAs

**Friday: Video Promotion**
- Share in relevant Slack/Facebook groups
- Email to your list: "New video just dropped"
- Engage with comments

**Result:** 20-30 videos per month, across all platforms, using AI

---

## PART 5: EMAIL MARKETING (HubSpot + Sequences)

### Email Provider Integration

**Option 1: HubSpot Native Email** (Recommended for you)
- Built into HubSpot
- Automation + tracking integrated
- No extra tool needed
- Cost: Included in HubSpot plan

**Option 2: ConvertKit** (If you want dedicated email focus)
- Creator-focused
- Beautiful email templates
- Integrates with HubSpot
- Cost: £40-300/month

### Your Email List Strategy

**Goal:** Build to 1,000+ subscribers in year 1

**Lead magnets (What you give away free):**
1. "SMB Marketing Audit Template" (5-page PDF)
2. "90-Day Transformation Checklist" (3-page PDF)
3. "The Direct Response Framework" (2-page cheat sheet)
4. Weekly newsletter: "SMB Insights" (emails on Monday/Thursday)

**Lead magnet placement:**
- [ ] Homepage: "Get Free Audit" pop-up (exit-intent)
- [ ] Blog posts: "Download [relevant resource]" CTA at bottom
- [ ] Landing pages: Form to download before accessing content
- [ ] LinkedIn: "New guide available - get link in bio"
- [ ] YouTube: Video description link to landing page

### Email Segmentation (Automatic in HubSpot)

**Segment 1: "Leads" (Just downloaded something)**
```
Sequence: 5-email welcome sequence
Goal: Build relationship, establish authority
Timeline: 10 days
Content:
  Day 1: Deliver resource + intro to you
  Day 3: Educational email about main problem
  Day 5: Case study email
  Day 7: "You might want to try this..."
  Day 10: "Ready to go deeper? Book a call"
```

**Segment 2: "Engaged Leads" (Opened 3+ emails)**
```
HubSpot automatically moves contacts who open/click
Sequence: 3-email sales-focused sequence
Goal: Move to discovery call
Timeline: 10 days
Content:
  Day 1: Social proof (logos + testimonial)
  Day 3: Your unique framework
  Day 7: Direct offer ("Let's discuss your 90-day plan")
```

**Segment 3: "Booked Calls" (Discovery call scheduled)**
```
Sequence: Appointment confirmation + pre-call info
Goal: Prepare them for call, build value
Timeline: Before call
Content:
  Same day: "Great! Here's what to expect..."
  Day before: "Looking forward to our call - come prepared with [3 questions]"
  After call: "Thanks for meeting. Here's next steps..."
```

**Segment 4: "Past Clients" (Worked with you before)**
```
Sequence: Ongoing relationship building + referral generation
Goal: Referrals, repeat business, testimonials
Timeline: Monthly
Content:
  Newsletter with latest insights
  Quarterly "How are things going?" check-in
  Annual case study request (if consent)
```

### Email Content Examples

**Email 1: Welcome**
```
Subject: "Welcome to BDB Sales - Your Quick Win Inside"

Hi [Name],

Thanks for grabbing your free [Resource Name]. I've attached it below.

Here's what you'll find inside:
- [Key insight 1]
- [Key insight 2]
- [Key insight 3]

More importantly, here's what you DON'T need to do:
- You don't need to hire an expensive agency
- You don't need to learn code
- You don't need to spend money before making money

What you DO need? Systems. And I've spent 30 years perfecting them.

Next week, I'm sending you our best practices on [topic]. Stay tuned.

In the meantime, reply to this email with your biggest business challenge. 
I genuinely read every response.

- Ewan
---
P.S. If you're ready to stop experimenting and start systematizing, 
we should talk. Reply with "CALL" and I'll send you a booking link.
```

**Email 2: Problem Identification**
```
Subject: "The #1 mistake costing you £20K/month"

Hi [Name],

I spent 30 years running a dental practice with 30 staff. 
And here's the problem I see in 90% of the SMBs I work with now:

They're doing marketing in reverse.

They invest money first, hope it works, measure nothing, iterate slowly.

Traditional process:
   Spend money → Hope it works → Measure (maybe) → Adjust

Right process:
   Test cheap → Measure what works → Scale what works → Measure again

When I switched to this approach in my practice, lead cost dropped 40%.

This works for service businesses of all types:
- Dental practices
- Hairdressing salons
- Veterinary clinics
- Consulting firms
- Fitness studios

The specific tactics change. The framework is the same.

Want to see how this works for YOUR business?

Book a 30-minute strategy call here: [LINK]
(First 5 calls this month are free)

- Ewan
---
P.S. This isn't a pitch. I'll give you 2-3 quick wins you can implement immediately.
```

**Email 3: Social Proof**
```
Subject: "[Case Study] How Sarah Increased Revenue 45% in 90 Days"

Hi [Name],

Quick story...

Sarah owned a salon in Newcastle. 3 staff, £600K revenue, maxed out on time.

She was working 55+ hours/week doing EVERYTHING:
- Client scheduling
- Marketing
- Staff coordination
- Accounting

Leads were inconsistent. Months with £15K revenue, months with £8K.

Here's what we did together:

Month 1: Set up systematic lead generation (referrals + Google Local)
Month 2: Trained staff to manage bookings + follow-up
Month 3: Automated email sequences + built waiting list

Result after 90 days:
- Revenue: +£45K (now £645K MRR equivalent)
- Sarah's hours: Down to 25/week
- Staff: Fully self-managing
- Lead cost: Cut in half

Best part? She was able to take 2 weeks off (first time in 5 years).

How is this possible?

Not magic. Just systems.

When you stop being the bottleneck, everything scales.

Ready to see if this works for you?

Book a call: [LINK]

- Ewan
---
P.S. Sarah's exact framework is documented. If you book this week, I'll walk you through it.
```

---

## PART 6: COMPLETE SALES AUTOMATION WORKFLOW

### The Automated Sales Process

```
Prospect lands on website
    ↓
Downloads free resource (audit template)
    ↓
HubSpot captures email + creates contact record
    ↓
Email sequence 1 starts automatically:
  - Day 1: Welcome + deliver resource
  - Day 3: Educational content
  - Day 5: Case study
  - Day 7: "Ready to go deeper?"
  - Day 10: Final offer
    ↓
IF prospect opens 3+ emails + clicks link:
    → HubSpot MARKS as "MQL" (Marketing Qualified Lead)
    → Ewan gets Slack notification: "Hot lead! [Name] from [Company]"
    → Lead score reaches 100+
    ↓
IF prospect clicks "Book Discovery Call" link:
    → LinkedIn ad pixel triggered (for retargeting)
    → Calendar opens (Calendly integration)
    → Prospect books time slot
    ↓
Discovery call scheduled:
    → Automated email confirmation sent to prospect
    → Reminder email sent day before
    → Ewan gets calendar alert 15 min before
    ↓
After discovery call:
    → HubSpot deal created
    → Sales sequence starts (emails reinforcing call discussion)
    → If prospect says "yes" → deal moves to "Proposal Sent"
    → If prospect says "maybe" → follow-up sequence starts
    ↓
Proposal sent:
    → Deal moves to "Proposal Sent" stage
    → 7-day follow-up sequence starts
    → If no response after 7 days → "check in" email
    ↓
Deal won or lost:
    → Deal closes
    → Revenue tracked
    → HubSpot reports: "This lead cost £X, generated £Y revenue, ROI = Z"
```

### The Conversion Rates (Realistic)

```
Prospects entering top of funnel: 100
    ↓
Email opens (60%): 60
    ↓
Click through to landing page (30% of openers): 18
    ↓
Qualified leads (MQL - engagement threshold): 12
    ↓
Book discovery call (25% of MQL): 3
    ↓
Close as client (30% of calls): 1

Result: 1 client per 100 prospects
At £4,997 average deal value: £4,997 revenue per 100 prospects

For discovery calls at £50 cost per lead: 
- Cost to 100 prospects: £50 × 3 calls booked = £150 CAC (customer acquisition cost)
- Revenue: £4,997
- ROI: 33x
```

### HubSpot Workflows (The Automation Rules)

**Workflow 1: Lead Capture Automation**
```
TRIGGER: Contact fills out "Free Audit" form on website

ACTIONS:
1. Create contact record with form data
2. Add tag: "Free Audit Downloaded"
3. Add to list: "Lead Nurture - Audit"
4. Send email #1 (Welcome + Audit PDF)
5. Start lead scoring sequence (+5 points initial)
6. Create task: "Follow up if no open in 3 days"
```

**Workflow 2: Email Engagement Scoring**
```
TRIGGER: Contact opens email

ACTIONS:
1. Add 10 points to lead score
2. If score reaches 50: Add to list "Engaged Leads"
3. If score reaches 100: 
   - Send Slack notification to Ewan: "[Name] is hot!"
   - Create task: "Reach out personally"
```

**Workflow 3: Discovery Call Booking**
```
TRIGGER: Contact schedules discovery call via Calendly

ACTIONS:
1. Create deal record (stage: "Discovery Call Booked")
2. Send Slack notification to Ewan: "[Name] booked call for [Date]"
3. Send email to prospect: "Confirmation + what to expect"
4. Schedule reminder email: Day before call ("Looking forward to 3pm...")
5. Add to list: "Discovery Call Scheduled"
6. Add tag: "Sales-Ready"
```

**Workflow 4: Post-Call Sales Sequence**
```
TRIGGER: Deal moves to "Discovery Call Booked" AND call is 24 hours past

ACTIONS:
1. Send email #1 (Same day): "Thanks for the call. Here's what we discussed..."
2. Send email #2 (Day 3): "Quick thought on your situation..."
3. Send email #3 (Day 5): "Let's move forward. Here's next steps..."
4. Send email #4 (Day 10 if no response): "Last check-in"
5. If no response after 14 days: Move deal to "Stuck" (manual follow-up)
```

---

## PART 7: INTEGRATION ROADMAP (How Everything Connects)

### Your Tech Stack

```
CORE SYSTEM:
├─ HubSpot (CRM + Marketing + Sales + Automation hub)
│
CONTENT CREATION:
├─ Webflow (Website + blog)
├─ Mootion or HeyGen (AI video generation)
├─ Canva (Image design + featured images)
├─ Zapier or Make (Custom integrations)
│
SOCIAL MEDIA:
├─ LinkedIn (organic posts + ads)
├─ YouTube (long-form video)
├─ Buffer or Later (scheduling tool)
│
COMMUNICATION:
├─ Calendly (Appointment scheduling)
├─ Gmail (Sales emails)
├─ Slack (Notifications)
│
ANALYTICS:
├─ Google Analytics 4
├─ Google Search Console
├─ HubSpot Analytics (built-in)

ALL connected via Zapier for data sync
```

### Integration Setup (One-Time, 4 Hours)

**Step 1: HubSpot ↔ Webflow**
```
Setting: Webflow CMS → HubSpot Contact creation

When someone fills out a Webflow form:
  ↓
Zapier captures the form submission
  ↓
Creates contact in HubSpot
  ↓
Triggers welcome email automatically
```

**Step 2: HubSpot ↔ Calendly**
```
Setting: Calendly booking → HubSpot deal creation

When someone books a discovery call via Calendly:
  ↓
Zapier captures booking event
  ↓
Creates deal in HubSpot ("Discovery Call Booked" stage)
  ↓
Ewan gets Slack notification
```

**Step 3: HubSpot ↔ Gmail**
```
Setting: All sales emails automatically tracked

Every email Ewan sends from Gmail:
  ↓
HubSpot sees when prospect opens it
  ↓
HubSpot sees when prospect clicks links
  ↓
Points automatically added for engagement
  ↓
Lead score updates in real-time
```

**Step 4: HubSpot ↔ LinkedIn**
```
Setting: LinkedIn pixel + HubSpot

LinkedIn form ads capture leads
  ↓
Zapier sends to HubSpot
  ↓
Lead tagged "LinkedIn Ad Source"
  ↓
Separate email sequence for LinkedIn leads
```

**Step 5: YouTube → Google Analytics → HubSpot**
```
Setting: Video traffic attribution

Video click goes to blog post
  ↓
Google Analytics tracks "video traffic" source
  ↓
Blog post conversion tracked
  ↓
Attribution shows: Video → Blog → Lead
```

---

## PART 8: YOUR INTEGRATED MONTHLY WORKFLOW

### Week 1: Content Production

**Monday-Tuesday:** Create 2 blog posts (using Claude + MiniMax as outlined in previous document)

**Wednesday:** 
- Generate 10-15 short videos from blog posts (using Mootion or InVideo)
- Create 1 long-form educational video (scripted + filmed)
- Design 4 LinkedIn carousel posts

**Thursday-Friday:**
- Upload all videos to YouTube with proper descriptions, tags, transcripts
- Schedule LinkedIn posts across the week
- Create email sequence related to new content

### Week 2: Distribution + Engagement

**Daily (15 min):**
- Check LinkedIn comments on your posts (respond to all)
- Check email replies (mark engaged leads)
- Monitor Slack for HubSpot notifications (hot leads)

**2x per week:** Publish new LinkedIn content
**2x per week:** Publish new YouTube videos
**2x per week:** Send emails to email list

**Monday:** Review HubSpot dashboard
- How many leads came in from each source?
- What content got best engagement?
- Which email got highest open rate?
- How many discovery calls booked?

### Week 3: Sales Follow-up + Lead Nurturing

**Monday-Wednesday:**
- Review all leads in "MQL" stage
- Reach out to top 5 (personal email or LinkedIn message)
- Check in on anyone who booked call (give them pre-call homework)

**Thursday-Friday:**
- Send case study emails to warm leads
- Create custom proposal for anyone who had discovery call
- Follow up on proposals sent 5+ days ago

### Week 4: Analysis + Optimization

**Monday:** Deep dive on metrics
```
Questions to answer:
1. Which blog posts got most traffic?
2. Which blog posts converted best (to lead magnet)?
3. Which videos got most views?
4. Which emails got highest open/click rates?
5. Which lead sources produce best clients?
6. What's my cost per lead by channel?
7. What's my cost per customer acquisition?
```

**Tuesday-Wednesday:** Optimize based on data
```
If Blog Post X got 100 visitors but 0 conversions:
  → Add CTA to bottom
  → Repurpose into video
  → Embed related resource

If Email Y got 5% open rate (low):
  → Test new subject line
  → A/B test version
  → Remove from sequence

If LinkedIn posts getting low engagement:
  → Switch from advice to questions
  → Try video instead of carousel
  → Increase posting frequency
```

**Thursday:** Plan next month
- Update content calendar with best-performing topics
- Identify top 3 lead sources (double down there)
- Test 1-2 new content formats

---

## PART 9: SUCCESS METRICS (What to Track)

### Monthly Dashboard

**Content Metrics:**
```
Blog traffic: 500+ sessions/month (Month 1) → 5,000+/month (Month 12)
Blog conversions: 5% (2-3 per post minimum)
Video views: YouTube 1,000+ views/month (Month 1) → 20,000+/month (Month 12)
Email list growth: +20-30 subscribers/week
LinkedIn followers: +50-100/month
```

**Lead Metrics:**
```
Leads generated: 20-30/month (Month 1) → 100+/month (Month 12)
Cost per lead: £50 (Month 1) → £20 (Month 12)
Lead quality (% MQL): 30% (Month 1) → 60%+ (Month 12)
Discovery calls booked: 3-5/month (Month 1) → 15-20/month (Month 12)
```

**Sales Metrics:**
```
Discovery call close rate: 30% (Month 1) → 50%+ (Month 12)
Average deal value: £4,997
Revenue from organic: £500-1,000/month (Month 1) → £50,000+/month (Month 12)
CAC (Customer Acquisition Cost): £150 (Month 1) → £50 (Month 12)
ROI: 30x (Month 1) → 100x+ (Month 12)
```

**Traffic Metrics:**
```
Organic traffic: 100-200 sessions/month (Month 1) → 5,000+/month (Month 12)
Direct traffic: 50+ sessions/month (from email, LinkedIn)
Social traffic: 100-200 sessions/month (Month 1) → 2,000+/month (Month 12)
Referral traffic: 50-100/month (Month 1) → 500+/month (Month 12)
```

---

## PART 10: 90-DAY IMPLEMENTATION ROADMAP

### Months 1-3: Foundation & Launch

**Month 1: Core Setup**
- [ ] HubSpot account setup + configuration
- [ ] Webflow website + landing pages live
- [ ] HubSpot ↔ Webflow integration
- [ ] LinkedIn company page optimized
- [ ] Email sequences set up (3 main sequences)
- [ ] First 8 blog posts published
- [ ] First 4 videos generated + uploaded
- [ ] Google Analytics + Search Console setup

**Goals by end of Month 1:**
- 50 email subscribers
- 3-5 discovery calls booked
- 500 website visitors
- 1-2 consulting clients

**Month 2: Content Scale**
- [ ] Publish 16 blog posts (2x per week)
- [ ] Generate 40 videos (across platforms)
- [ ] LinkedIn posting 4x/week (organic + ads)
- [ ] Email list grows to 200+
- [ ] YouTube channel gets 100+ subscribers
- [ ] HubSpot optimization (improve lead scoring)

**Goals by end of Month 2:**
- 200 email subscribers
- 12-15 discovery calls booked
- 2,000 website visitors
- 3-5 consulting clients
- £15,000-25,000 revenue

**Month 3: Optimization & ROI**
- [ ] Analyze what's working (blog posts, videos, emails)
- [ ] Double down on top performers
- [ ] A/B test subject lines, headlines, CTAs
- [ ] Optimize sales funnel (improve close rate)
- [ ] Begin planning video content for next 9 months
- [ ] Test LinkedIn ads (£200+ budget)

**Goals by end of Month 3:**
- 500+ email subscribers
- 30-40 discovery calls booked (more than Month 1+2)
- 5,000+ website visitors
- 8-12 consulting clients
- £40,000-60,000 revenue
- Clear data on best-performing channels

---

## FINAL ARCHITECTURE SUMMARY

### The Complete System (How It All Works Together)

```
AWARENESS (Getting their attention):
  Website Blog + LinkedIn Posts + YouTube Videos
    ↓
ENGAGEMENT (Building relationship):
  Email newsletter + Case studies + Educational content
    ↓
CONSIDERATION (Proving you're right):
  Free audit + Video testimonials + Results data
    ↓
DECISION (Moving to sale):
  Discovery call booking + Proposal + Sales email sequence
    ↓
CLOSED (Revenue):
  New client → Case study for future marketing
```

**Every component is:**
- ✅ Automated (HubSpot handles follow-up)
- ✅ Data-driven (Track everything)
- ✅ Integrated (One system, not 10)
- ✅ Scalable (Add content, system scales)
- ✅ Measurable (ROI by channel)

**Your time investment:**
- Week 1: Setup (10 hours one-time)
- Ongoing: 4-5 hours/week (content creation + monitoring)
- ROI: £40K-150K+ year 1

**This is the 2026 outbound marketing machine. Build it once, run it forever.**

---
title: "covered.AI Website Quality Assurance System"
id: "website-critique-rag-onboarding-system"
version: 1
created: "2026-04-25"
type: "document"
topic_type: "sales-marketing"
audience: "internal"
layer: "truth"
status: "filed"
signed_by: "Devon, 2026-04-25, devin-992682c244cf444f91e0a516498afbfd"
---

# covered.AI Website Quality Assurance System
## Expert Panel Critique Framework + Client Onboarding RAG Pipeline

**Purpose:** Build a systematic, multi-dimensional website critique system that becomes a competitive moat for your consultancy. Combined with RAG-powered client onboarding, this lets you deliver superior websites 10x faster.

---

## PART 1: EXPERT PANEL CRITIQUE FRAMEWORK

### The 8-Expert Judge Panel

You'll structure critiques as if **8 expert judges** are evaluating every website across different dimensions. Each brings specialized expertise and asks specific questions.

---

## EXPERT #1: THE CONVERSION ARCHITECT
**Specialty:** CRO, funnel optimization, revenue impact

**Evaluates:**
- Conversion rate optimization (CRO) funnel
- Call-to-action (CTA) clarity, placement, urgency
- Form friction (length, validation, copy)
- Page-to-goal clarity (is the goal obvious?)
- Objection handling (does copy address customer fears?)
- Lead magnet effectiveness
- Checkout/booking flow smoothness
- Exit-intent optimization

**Critique Questions (Ask in order):**
1. What is the primary conversion goal on this page?
2. Is the CTA visible within first 3 seconds of page load?
3. How many steps to conversion (audit â†’ booking â†’ payment)?
4. Where do users likely drop off in the funnel?
5. Is the value proposition crystal clear before asking for action?
6. Are objections addressed before CTAs?
7. How many form fields? Could you reduce by 50%?
8. Does the page feel trustworthy enough to convert?

**Measurement:**
- CTA click rate (target: 5%+ of page visitors)
- Form completion rate (target: 40%+ of form starters)
- Booking rate (target: 2-3% of page visitors)
- Average revenue per visitor (Â£X)

**Output Format:**
```
ðŸŽ¯ CONVERSION SCORE: [0-10]
- CTA Effectiveness: [Score + specific issue]
- Form Friction: [Score + specific issue]
- Goal Clarity: [Score + specific issue]
- Trust Signals: [Score + specific issue]

Quick Win: [One thing that will improve CRO in 1 hour]
Deep Dive: [One optimization that needs 1-2 weeks]
```

---

## EXPERT #2: THE UX RESEARCHER
**Specialty:** User experience, usability heuristics, user flow

**Evaluates:**
- Navigation clarity (can users find what they need in 2 clicks?)
- Information architecture (logical grouping?)
- Page load time (target: <3 seconds)
- Mobile responsiveness (test on iPhone SE, Pixel 4, iPad)
- Color contrast (WCAG AA compliance, 4.5:1 ratio)
- Font readability (size, line height, font stack)
- Whitespace and breathing room
- Consistency of design patterns across site
- Error messages (helpful or generic?)
- Accessibility (keyboard navigation, screen reader compatible)

**Critique Questions:**
1. Can a first-time visitor understand what this site is about in 5 seconds?
2. How many clicks to reach any major page (target: â‰¤3)?
3. Is the mobile version actually usable, or just "responsive"?
4. Do all interactive elements behave as expected?
5. Are there any dead ends or pages with no navigation?
6. Do forms provide helpful error messages?
7. Is there sufficient whitespace, or is it cluttered?
8. Can you use this site with keyboard only (no mouse)?

**Measurement:**
- Page load time (target: <3 seconds, <2 on mobile)
- Bounce rate (target: <50% on landing pages)
- Pages per session (target: 3+ on content pages)
- Time on page (target: 2+ minutes on content)
- Accessibility score (WAVE, Lighthouse: 90+)
- Mobile usability score (Google: 85+)

**Output Format:**
```
ðŸ˜Š UX SCORE: [0-10]
- Navigation: [Score + paths that confuse]
- Mobile Experience: [Score + specific device issues]
- Performance: [Load time + Lighthouse score]
- Accessibility: [Score + WCAG failures]

Friction Points (by severity):
1. [Critical UX issue blocking conversion]
2. [Major issue affecting 20%+ users]
3. [Minor issue affecting small segment]

User Workflow:
[Recommended flow for new visitor to conversion]
```

---

## EXPERT #3: THE BRAND STRATEGIST
**Specialty:** Brand consistency, positioning, messaging alignment

**Evaluates:**
- Brand voice consistency (tone matches brand guidelines?)
- Visual identity consistency (colors, fonts, imagery style)
- Positioning clarity (vs. competitors)
- Messaging alignment with target audience
- Credibility signals (founder story, proof points, social proof)
- Brand promise delivery (does copy back up claims?)
- Differentiation (why this company, not another?)
- Storytelling effectiveness

**Critique Questions:**
1. What is this company's core positioning in one sentence?
2. Does every page reinforce that positioning?
3. Are the brand colors used consistently? Any color hierarchy issues?
4. Does the tone of voice match the brand (professional vs. casual)?
5. Is the founder/team visible and credible?
6. Are there enough social proof elements (logos, testimonials, case studies)?
7. What makes this different from 5 competitors?
8. Does the visual design feel premium or budget?

**Measurement:**
- Brand consistency score (0-100 across all pages)
- Positioning clarity (test with 5 strangers: can they explain what you do?)
- Founder authority signals (mentions, credentials, story)
- Social proof elements (testimonials, case studies, logos)
- Differentiation clarity (vs. competitors)

**Output Format:**
```
ðŸŽ¨ BRAND SCORE: [0-10]
- Visual Consistency: [Score + inconsistencies noted]
- Voice/Tone: [Score + tone analysis]
- Positioning: [Score + clarity test results]
- Credibility: [Score + missing proof points]

Brand Audit:
- Primary colors used: [Count + inconsistencies]
- Typography: [Font stack + hierarchy issues]
- Photography style: [Consistent or mixed?]
- Voice samples: [Quote that shows tone]

Positioning Statement:
"[Company name] helps [target] achieve [outcome] by [method]"
Does the website prove this? [Yes/No + gaps]
```

---

## EXPERT #4: THE COPYWRITER
**Specialty:** Messaging, clarity, persuasion, storytelling

**Evaluates:**
- Headline effectiveness (does it stop scrolling?)
- Subheadline clarity (reinforces benefit?)
- Specific numbers vs. vague adjectives
- Benefit-focused language (not feature-focused)
- Objection handling (does copy address "why should I believe this?")
- Call-to-action wording (action-oriented?)
- Story effectiveness (does it connect emotionally?)
- Body copy length (TL;DR or just right?)

**Critique Questions:**
1. What's the first thing visitors read? (Headline test)
2. Is the main benefit stated in first 3 sentences?
3. Count vague words (significant, improve, enhance) - target: 0-2 per page
4. Count specific numbers (prices, percentages, metrics) - target: 3-5 per page
5. Is copy benefit-focused or feature-focused? (Example: "Collect Â£8K more per month" vs "AI-powered invoice automation")
6. Do CTAs use action verbs? ("Book Audit" vs "Submit")
7. Does the copy feel persuasive or just informational?
8. Is there a story that creates emotional connection?

**Measurement:**
- Headline clarity score (0-10)
- Specificity score (numbers per 100 words)
- CTA clarity score (0-10)
- Persuasion effectiveness (A/B test conversion lift)

**Output Format:**
```
âœï¸ COPY SCORE: [0-10]
- Headline: [Analysis + rewrite suggestion]
- Benefit Clarity: [Score + vague words identified]
- Specificity: [Numbers per 100 words + improvements]
- CTA: [Current vs. recommended]

Copy Analysis:
Vague adjectives found: [List + replacements]
Features mentioned: [List with benefit conversions]
Stories told: [Does emotional connection exist?]

Headline Alternatives (to test):
1. [Benefit-focused]
2. [Curiosity-driven]
3. [Problem-focused]
```

---

## EXPERT #5: THE DESIGN SYSTEMS EXPERT
**Specialty:** Visual hierarchy, design principles, modern aesthetics

**Evaluates:**
- Visual hierarchy (is important info prominent?)
- Whitespace usage (breathing room or cluttered?)
- Color theory application (contrast, psychology, hierarchy)
- Typography hierarchy (sizes, weights creating clear structure)
- Imagery (relevant, consistent style, high quality?)
- Layout grid (consistent 12-column or other grid?)
- Design consistency (components repeated throughout)
- Modern design patterns (vs. dated design)

**Critique Questions:**
1. What's the visual hierarchy? What should the eye look at first?
2. Is there sufficient whitespace, or does it feel cramped?
3. Test color contrast: Can you read text at arm's length?
4. Do the colors align with brand psychology? (Navy = trust, teal = energy)
5. Are typography sizes creating clear hierarchy?
6. Is imagery style consistent across the site?
7. Do you see repeated design patterns, or is each section custom?
8. Does this design feel current (2024/2025) or dated?

**Measurement:**
- Visual hierarchy effectiveness (80%+ of users focus on CTA first)
- Color contrast score (WCAG AA: 4.5:1 for normal text)
- Typography hierarchy (4-5 distinct sizes, clear roles)
- Whitespace ratio (30-40% of page is empty space)
- Design consistency (core components appear throughout)
- Design modernity (does it look 2025 or 2015?)

**Output Format:**
```
ðŸŽ­ DESIGN SCORE: [0-10]
- Visual Hierarchy: [Score + focal point clarity]
- Color Theory: [Score + psychology alignment]
- Typography: [Score + hierarchy analysis]
- Whitespace: [Score + density analysis]

Design Audit:
- Primary colors: [List with psychology]
- Typography stack: [Font families + sizes]
- Whitespace ratio: [Visual inspection + percentage]
- Component consistency: [Buttons, cards, forms - consistent?]

Modern Design Elements Present:
âœ… [Contemporary patterns used]
âŒ [Dated patterns to update]

Quick Visual Update:
[One design change that will modernize immediately]
```

---

## EXPERT #6: THE TECHNICAL SEO SPECIALIST
**Specialty:** Technical SEO, keyword optimization, search visibility

**Evaluates:**
- Page titles (60 chars, keyword-rich?)
- Meta descriptions (160 chars, compelling?)
- H1 tag (one per page, includes primary keyword?)
- Internal linking (3-4 relevant links, keyword anchor text?)
- URL structure (keyword-rich, hyphenated, readable?)
- Mobile indexing (Googlebot can see all content?)
- Schema markup (structured data for rich snippets?)
- Core Web Vitals (LCP <2.5s, FID <100ms, CLS <0.1)
- Robots.txt and sitemap presence

**Critique Questions:**
1. What's the primary keyword for this page?
2. Is that keyword in the H1, title tag, first 100 words?
3. Is there internal linking to related pages?
4. How does the URL look? (keyword-rich or random slug?)
5. Test on mobile: Does Google see all the content?
6. Are there schema markup opportunities? (Article, FAQPage, etc.)
7. What's the Core Web Vitals score? (Aim: all green)
8. Does the page have a clear E-E-A-T signal? (Expertise, Experience, Authority, Trustworthiness)

**Measurement:**
- Keyword optimization (primary keyword in H1, title, first 100 words)
- SEO title score (60 chars, keyword-rich, compelling)
- Meta description score (160 chars, keyword, CTA)
- Internal linking depth (3-5 links to other pages)
- Core Web Vitals (all green or yellow max)
- SEO visibility (estimate ranking potential)
- E-E-A-T signal strength (founder credibility, expertise, authority)

**Output Format:**
```
ðŸ” SEO SCORE: [0-10]
- Keyword Optimization: [Score + keywords identified]
- On-Page SEO: [Score + title/meta issues]
- Internal Linking: [Score + linking opportunities]
- Technical Health: [Core Web Vitals scores]
- E-E-A-T Signals: [Authority assessment]

SEO Audit:
- Primary keyword: [Keyword + search volume + difficulty]
- Page title: [Current + recommended]
- Meta description: [Current + recommended]
- H1: [Current + assessment]
- Internal links: [Count + link equity distribution]

Ranking Potential:
[Keyword] - Current rank: [?], Potential: [Position based on optimization]

Quick Wins:
1. [Title tag optimization]
2. [Schema markup opportunity]
3. [Internal linking improvement]
```

---

## EXPERT #7: THE PERFORMANCE ENGINEER
**Specialty:** Page speed, optimization, technical performance

**Evaluates:**
- First Contentful Paint (FCP) - target <1.8s
- Largest Contentful Paint (LCP) - target <2.5s
- Cumulative Layout Shift (CLS) - target <0.1
- Time to Interactive (TTI) - target <3.8s
- Total Blocking Time (TBT) - target <300ms
- JavaScript bundle size (optimize for slow 3G)
- Image optimization (WebP, lazy loading?)
- Caching strategy (browser cache headers?)
- CDN usage (global delivery?)
- Network waterfall (what's slow?)

**Critique Questions:**
1. How fast does the page load on desktop? Mobile?
2. Test on slow network (3G): How does it feel?
3. Are images optimized? (Use Lighthouse image audit)
4. Is JavaScript blocking render? (Check coverage)
5. Are fonts optimized? (system fonts vs. web fonts)
6. Is there a CDN in use? (geolocation test)
7. What's the largest element blocking rendering?
8. How does the page feel on a 5-year-old phone?

**Measurement:**
- Lighthouse Performance score (90+ target)
- Core Web Vitals (LCP, FID, CLS)
- Mobile speed (Pixel 4, 4G network)
- Desktop speed (modern MacBook, WiFi)
- Performance budget (JS size, image size)
- Time to Interactive (when can user interact?)

**Output Format:**
```
âš¡ PERFORMANCE SCORE: [0-10]
- LCP: [Score + time + issue]
- FID: [Score + time + issue]
- CLS: [Score + number + issue]
- TTI: [Score + time + issue]

Lighthouse Scores:
- Performance: [0-100]
- Accessibility: [0-100]
- Best Practices: [0-100]
- SEO: [0-100]

Bottleneck Analysis:
[Slow resource] â†’ [Impact] â†’ [Solution]
[Largest JS] â†’ [Blocks rendering] â†’ [Code split or defer]
[Unoptimized images] â†’ [Slows LCP] â†’ [Use WebP + lazy load]

Performance Budget:
- Current JS: [Size] - Target: [Size]
- Current images: [Size] - Target: [Size]
- Target FCP: 1.8s - Current: [Time]

Mobile Performance (slow 3G):
- FCP: [Time] - Target: <3s
- LCP: [Time] - Target: <5s
- TTI: [Time] - Target: <6s

Quick Optimization:
1. [Highest impact improvement]
2. [Second highest impact]
3. [Quick win]
```

---

## EXPERT #8: THE ACCESSIBILITY AUDITOR
**Specialty:** WCAG compliance, inclusive design, assistive tech

**Evaluates:**
- Color contrast (WCAG AA: 4.5:1 normal, 3:1 large)
- Keyboard navigation (can you tab through all interactive elements?)
- Screen reader compatibility (test with NVDA or JAWS)
- Alt text on images (descriptive, not "image" or filename)
- Form labels (linked to inputs with `for` attribute)
- Focus indicators (can you see which element has focus?)
- Heading hierarchy (H1, then H2s, then H3s - no skipping levels)
- Skip links (jump to main content?)
- Motion/animations (prefers-reduced-motion respected?)
- Mobile accessibility (touch targets 48x48px minimum)

**Critique Questions:**
1. Can you navigate this site with keyboard only (no mouse)?
2. Are all form inputs properly labeled?
3. Test with WAVE or Lighthouse: how many accessibility errors?
4. Are images alt texts helpful or just filenames?
5. Is there sufficient color contrast? (Test with Stark)
6. Can you see which element has keyboard focus?
7. Is the heading structure logical? (H1 â†’ H2 â†’ H3)
8. Are animations distracting for people with motion sensitivity?

**Measurement:**
- WCAG AA compliance score (0-10)
- Color contrast failures (target: 0)
- Keyboard navigation success rate (100% of interactive elements)
- Screen reader compatibility (test: home page fully navigable)
- Alt text quality (descriptive vs. missing/generic)
- Accessibility audit (WAVE errors: <10, preferably 0)

**Output Format:**
```
â™¿ ACCESSIBILITY SCORE: [0-10]
- Color Contrast: [Score + failures identified]
- Keyboard Navigation: [Score + problematic elements]
- Screen Reader: [Score + missing labels]
- Alt Text: [Score + examples of good/bad]

WCAG Audit:
- Level A: [Pass/Fail]
- Level AA: [Pass/Fail + failures listed]
- Level AAA: [Assessment]

Accessibility Errors Found:
[Error type] â†’ [Affected elements] â†’ [Fix]
Missing alt text â†’ [Image count] â†’ [Add descriptive alt text]
Low contrast â†’ [Element] â†’ [Update colors to meet 4.5:1]

Keyboard Navigation Test:
- Home button: âœ… Focusable
- Primary CTA: âœ… Focusable
- Form fields: âœ… All labeled
- Skip links: âŒ Not present (RECOMMENDED)

Screen Reader Test:
[Result of testing with NVDA/JAWS]

Quick Accessibility Wins:
1. [Highest impact fix]
2. [Second priority]
3. [Quick improvement]
```

---

## PART 2: HOW TO USE THE 8-EXPERT PANEL

### The Critique Process (90 Minutes)

**Step 1: Share the Website (5 min)**
- Share website URL or prototype link
- Provide 1-2 sentence context (who it's for, what's the goal)

**Step 2: Run Each Expert Panel (10-12 min per expert)**

**Flow:**
1. Expert asks 8 questions in order
2. Expert scores the dimension (0-10)
3. Expert identifies top 3 issues
4. Expert suggests 1 quick win + 1 deep dive

**Output:**
8 expert reports (one per expert) in 90 minutes

**Step 3: Synthesis (10 min)**
- Aggregate all scores
- Identify common themes
- Prioritize top 10 issues
- Create action plan

---

### Critique Scoring Matrix

```
Expert          Weight   Score   Impact
â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•
1. Conversion      30%    [X]    [High]
2. UX/Navigation   20%    [X]    [High]
3. Brand           15%    [X]    [Medium]
4. Copy            15%    [X]    [Medium]
5. Design Systems  10%    [X]    [Medium]
6. Technical SEO   5%     [X]    [Low]
7. Performance     3%     [X]    [Low]
8. Accessibility   2%     [X]    [Low]

OVERALL SCORE: [X/10] (Weighted average)

Red Flags (score <5): [List critical issues]
Strengths (score >8): [List strong areas]
```

---

### Issue Prioritization Matrix

```
Impact on Conversion | Implementation Effort | Priority
â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€
High               | Low (1-2 hours)       | ðŸ”´ DO FIRST
High               | Medium (4-8 hours)    | ðŸŸ  DO SECOND
High               | High (1-2 weeks)      | ðŸŸ¡ DO THIRD
Medium             | Low (1-2 hours)       | ðŸŸ¢ DO LATER
```

---

## PART 3: CLIENT ONBOARDING RAG PIPELINE

### The Challenge
**Current state:** You ask clients "tell me about your business" and get vague answers. Missing critical info.

**Better way:** Use RAG (Retrieval Augmented Generation) to automatically gather data from their existing digital presence, then ask targeted follow-up questions.

### The RAG Onboarding Flow

```
CLIENT SIGNUP
    â†“
    â””â”€â†’ RAG CRAWLER (automatically gathers existing data)
        â”œâ”€ LinkedIn profile/company page
        â”œâ”€ Website (current or previous)
        â”œâ”€ Social media (Facebook, Instagram, Twitter)
        â”œâ”€ Blog posts / Medium / Substack
        â”œâ”€ Google Business Profile
        â”œâ”€ Video presence (YouTube, Vimeo)
        â”œâ”€ Press mentions / media coverage
        â”œâ”€ Previous websites (Internet Archive)
        â””â”€ Public business info (Companies House, etc.)
    â†“
    â””â”€â†’ AI ANALYSIS OF GATHERED DATA
        â”œâ”€ Extract tone/voice from existing content
        â”œâ”€ Identify visual style (colors, fonts, imagery)
        â”œâ”€ Extract key claims/positioning
        â”œâ”€ Identify target audience signals
        â”œâ”€ Find customer pain points from reviews
        â”œâ”€ Compile testimonials/social proof
        â”œâ”€ Identify competitors mentioned
        â””â”€ Flag any credibility/authority signals
    â†“
    â””â”€â†’ SMART ONBOARDING FORM
        â”œâ”€ Auto-filled fields (from RAG analysis)
        â”œâ”€ Targeted questions (based on gaps)
        â”œâ”€ File uploads (photos, videos, brand assets)
        â”œâ”€ Competitor analysis
        â”œâ”€ Goal definition
        â””â”€ Unique selling point refinement
    â†“
    â””â”€â†’ ONBOARDING BRIEF (auto-generated)
        â”œâ”€ Brand summary (tone, visual style, positioning)
        â”œâ”€ Target audience profile
        â”œâ”€ Competitor positioning
        â”œâ”€ Key messages to emphasize
        â”œâ”€ Visual assets to use
        â”œâ”€ Content themes to explore
        â””â”€ Conversion goals
    â†“
    â””â”€â†’ WEBSITE BUILD (informed by comprehensive data)
```

---

### RAG Data Sources (in priority order)

**Tier 1: High Signal (Use directly)**
- LinkedIn company page (official positioning, tone, visual style)
- Current website (if exists - shows what they like)
- Google Business Profile (business hours, services, reviews)
- Previous websites (Internet Archive - shows evolution)

**Tier 2: Medium Signal (Extract themes)**
- LinkedIn posts by founder (tone, personality, key messages)
- Social media (Facebook, Instagram - visual style, audience, frequency)
- Blog posts (writing style, topics, depth)
- YouTube channel (if exists - presentation style, topics)

**Tier 3: Supporting Signal (Use for validation)**
- Testimonials/reviews (what customers say matters)
- Press mentions (credibility signals)
- Competitor analysis (positioning context)
- Industry mentions (market position)

---

### Smart Onboarding Form (Client-facing)

**Section 1: Pre-filled from RAG**
```
We gathered the following from your existing digital presence.
Please review and correct if needed:

Business Name: [Auto-filled from LinkedIn/website]
[Edit option]

Industry: [Auto-filled]
[Edit option]

Target audience: [Inferred from social posts/website]
[Edit option]

Brand tone: [Extracted from content analysis]
Options: â˜ Professional â˜ Friendly â˜ Bold â˜ Other

Visual style: [Described from images/design analysis]
- Colors: [Inferred primary colors]
- Font style: [Described as: Modern/Traditional/Creative]
- Photography: [Described as: Lifestyle/Product/Professional]

Primary message: [Extracted from website/LinkedIn]
[Edit option]
```

**Section 2: Targeted Questions (based on gaps)**
```
Based on our analysis, we have some targeted questions:

1. Your website currently says "[quote]" - is this still accurate?
   â˜ Yes, keep this message
   â˜ Update it to: _______________
   â˜ Need to rethink this

2. We found [N] testimonials in your LinkedIn. Can you share 3-5 
   video/written testimonials from recent customers?
   [Upload box]

3. You mentioned [service A] but not [service B]. Which should 
   be the focus of the website?
   â˜ Service A only
   â˜ Service B only
   â˜ Both equally
   â˜ Other: _______________

4. Your LinkedIn shows [value prop]. Is there a more specific 
   benefit you want to emphasize on the website?
   Current: [Extracted]
   Preferred: [Text input]

5. We found [N] competitors mentioned in your industry. Who do 
   you consider your #1 competitor? [Dropdown from list found]
   What's your main advantage vs. them? [Text input]
```

**Section 3: File Uploads**
```
Please provide or upload:

Brand Assets:
- Logo (PNG, SVG, AI)
- Brand guidelines (PDF if exists)
- Color palette (image or color codes)
- Font list (names or .zip)

Media:
- 3-5 best photos (you, team, products, office)
- 1-2 videos (introduction, testimonial, demo)
- Any existing brand videos

References:
- Websites you like (URLs - we'll analyze style)
- 2-3 competitor websites
- Inspiration images (aesthetic style you prefer)

Testimonials:
- Video testimonials (upload or link to YouTube)
- Written testimonials (paste text)
- Screenshots of reviews (if applicable)

Other:
- Product images/specs (if relevant)
- Infographics or diagrams (if relevant)
- Previous marketing materials (to understand style)
```

**Section 4: Strategy Definition**
```
Website Goals:
â˜ Generate leads (book free audit)
â˜ Establish authority (educational content)
â˜ Direct sales (book a call, sign up for service)
â˜ Build community (engagement, email list)
â˜ Customer support (FAQ, help resources)

Primary Conversion Action:
[Dropdown: Book a call / Sign up / Download / Other]

Secondary Conversion Actions (check all that apply):
â˜ Email signup
â˜ Download lead magnet
â˜ Social media follow
â˜ Read blog posts
â˜ Watch videos
â˜ Read testimonials

Key Messages (rank by importance):
1. [Their primary benefit]
   Importance: â˜…â˜…â˜…â˜…â˜…
   Evidence: [Where this comes from]

2. [Secondary benefit]
   Importance: â˜…â˜…â˜…â˜…â˜†
   Evidence: [Where this comes from]

3. [Unique feature]
   Importance: â˜…â˜…â˜…â˜†â˜
   Evidence: [Where this comes from]

Ideal Customer Profile (1-2 sentences):
[AI-generated from research, client can refine]

Key differentiators vs. competitors:
1. [What makes you different from #1 competitor]
2. [What makes you different from #2 competitor]
3. [Your unique advantage]
```

**Section 5: Quick Context**
```
Any last things we should know?

Team size: [Dropdown: Solo / 2-5 / 6-15 / 15+]

Timeline: When do you need this live?
[Dropdown: Urgent (1 week) / Soon (2-3 weeks) / Flexible (1 month+)]

Budget: What's your budget range?
[Dropdown: Â£2K-5K / Â£5K-10K / Â£10K-20K / 20K+]

Your biggest challenge right now:
[Text area - what's preventing growth?]

Website's biggest goal:
[Text area - what would "success" look like?]
```

---

### RAG Analysis Engine (AI-powered extraction)

**Input:** All gathered data sources

**Output:** Structured brief

```json
{
  "brand_analysis": {
    "name": "Company Name",
    "industry": "Industry classification",
    "estimated_size": "1-5 employees",
    "tone_analysis": {
      "primary": "Professional but approachable",
      "examples": ["Quote from LinkedIn", "Quote from website"],
      "consistency_score": 0.85,
      "recommendation": "Maintain this tone, strengthen authority signals"
    },
    "visual_style": {
      "primary_colors": ["#0A2540", "#00D9C0"],
      "font_style": "Modern sans-serif",
      "imagery_style": "Professional headshots + lifestyle",
      "consistency_score": 0.72,
      "recommendation": "Strengthen brand consistency - mix is 40% professional, 60% casual"
    },
    "positioning": {
      "explicit": "Quote from their website or LinkedIn",
      "implicit": "Inferred from content and customer pain points",
      "clarity_score": 0.65,
      "recommendation": "Sharpen positioning - 3 different messages across channels"
    },
    "target_audience": {
      "primary": "Profile built from audience analysis",
      "pain_points": ["From reviews", "From content themes"],
      "desires": ["From messaging", "From social engagement"]
    }
  },
  "content_analysis": {
    "tone_samples": [
      {"source": "LinkedIn", "quote": "..."},
      {"source": "Website", "quote": "..."},
      {"source": "Blog", "quote": "..."}
    ],
    "key_messages": [
      "Message 1 (frequency: 5 mentions)",
      "Message 2 (frequency: 3 mentions)"
    ],
    "visual_assets": {
      "photos_count": 45,
      "videos_count": 3,
      "quality": "Mix of professional and personal",
      "recommendations": ["Update product photography", "More founder visibility"]
    },
    "social_proof": {
      "testimonials": 12,
      "reviews": 8,
      "case_studies": 0,
      "recommendations": ["Create 3 video testimonials", "Document 2 case studies"]
    }
  },
  "competitive_analysis": {
    "competitors_mentioned": ["Competitor A", "Competitor B"],
    "competitive_advantages": [
      "Advantage 1 - mention frequency: 4x",
      "Advantage 2 - mention frequency: 2x"
    ],
    "positioning_gaps": ["Gap A", "Gap B"]
  },
  "website_recommendations": {
    "tone": "Professional but approachable - emphasize founder credibility",
    "messaging": [
      "Primary: [Their key message]",
      "Secondary: [Support message]",
      "Tertiary: [Differentiation]"
    ],
    "visual_direction": "Modern, professional, +20% more founder visibility",
    "content_structure": [
      "Hero: Benefit-driven headline",
      "Problem: Validate their pain points",
      "Solution: Their approach",
      "Social proof: Testimonials + case studies",
      "CTA: Clear next step"
    ],
    "assets_needed": [
      "2-3 new founder photos",
      "1-2 team member photos",
      "3 video testimonials",
      "2 case study write-ups"
    ]
  }
}
```

---

### Example RAG Onboarding Brief (Auto-generated)

```
ðŸ“‹ ONBOARDING BRIEF: covered.AI
Generated from your digital presence analysis

â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•

ðŸŽ¯ BRAND SNAPSHOT

Company: covered.AI
Founder: Ewan Bramley
Industry: Business Consulting / SMB Optimization
Positioning: "We tighten your processes. You keep running your business."

Tone: Straightforward, human, non-corporate
Visual Style: Navy blue (#0A2540) + Teal (#00D9C0), modern sans-serif
Audience: UK SMBs (Â£500K-Â£3M, owner-operators, 50-60 hours/week)

â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•

ðŸ“Š ANALYSIS FINDINGS

Key Message Frequency:
1. "Low-friction approach" (mentioned 8x across channels)
2. "No disruption" (mentioned 6x)
3. "Â£8K-15K more collected" (mentioned 4x)

Visual Consistency: 72% (Mix of professional + personal)
- LinkedIn: Professional, authority-focused
- Website: Benefit-focused, specific numbers
- Tone consistency: 85% (Strong alignment)

Social Proof Found:
- 0 case studies (NEED TO CREATE 2-3)
- 12 LinkedIn testimonials (COULD USE 3-5 VIDEO)
- Founder credibility strong (30 years background)

â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•

ðŸŽ¨ DESIGN DIRECTION

Primary Colors: Navy #0A2540, Teal #00D9C0
Typography: Satoshi Bold (headings), Inter Regular (body)
Imagery: Professional + approachable (Ewan photos, client examples)
Photo Style: Behind-the-scenes + results-focused

Layout Pattern: 
- Hero (benefit-driven headline)
- Problem validation
- Process explanation
- Social proof
- CTA

â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•

ðŸ“ MESSAGING PRIORITIES

PRIMARY: "Get 10-20 hours/week back without changing how you work"
- Evidence: Repeated across LinkedIn, existing website
- Emotional hook: Freedom + control
- Benefit: Time and money

SECONDARY: "Â£8K-15K more collected in 90 days"
- Evidence: Featured in pricing/case studies
- Emotional hook: Profit + validation
- Benefit: Revenue impact

TERTIARY: "Background optimization (zero disruption)"
- Evidence: Core differentiator from competitors
- Emotional hook: Safety + trust
- Benefit: Risk reduction

â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•

ðŸ” COMPETITOR ANALYSIS

Main Competitors Mentioned:
1. Traditional management consultants (transform everything)
2. DIY automation tools (confusing, unsupported)

Advantages vs. Competitors:
âœ… Founder credibility (30 years operational experience)
âœ… Low-friction approach (vs. transformation)
âœ… Specific results (Â£8K+, 10-20 hours)
âœ… Background operation (no staff retraining)

Positioning Gap: No one else claims "non-disruptive optimization"

â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•

ðŸ“‹ WEBSITE BUILD CHECKLIST

Content Needed:
â˜ 3-5 video testimonials (clients speaking to results)
â˜ 2-3 case studies (industry-specific if possible)
â˜ Ewan's founder story (30-year background)
â˜ 20 blog post titles (to be written)

Assets Needed:
â˜ 2-3 new Ewan photos (professional but approachable)
â˜ 5-8 client/team photos (to show real business)
â˜ Brand guidelines PDF (if exists - for consistency)
â˜ Previous website content (for messaging inspiration)

Technical:
â˜ Domain (covered.ai or covered.co.uk)
â˜ Email (ewan@covered.ai)
â˜ HubSpot integration (if using CRM)
â˜ Analytics setup (GA4 + tracking codes)

â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•

ðŸŽ¯ NEXT STEPS

1. âœ… Review this brief - does it match your vision?
   - If not, update the brief before design starts
   
2. âœ… Provide missing assets:
   - Video testimonials or client info
   - Founder photos (2-3)
   - Any other brand assets
   
3. âœ… Approve case study subjects:
   - 2-3 recent clients willing to be featured
   - Specific results to highlight
   
4. âœ… Confirm messaging priorities:
   - Is "10-20 hours/week" the strongest benefit?
   - Are the 3 key messages correct?

5. â­ï¸ Website design starts once brief is approved

â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•
```

---

## PART 4: INTEGRATED WORKFLOW (Critique â†’ Build â†’ Iterate)

### Week 1: Expert Panel Review
```
Monday: Present website to 8-Expert Panel
- Each expert critiques simultaneously (parallel, not sequential)
- 90 minutes total (10-12 min per expert)
- Output: 8 expert reports + aggregated scoring matrix

Tuesday: Synthesis & Prioritization
- Combine all critiques
- Identify top 20 issues (by impact)
- Create action plan
- Share with client

Wednesday: Client Feedback
- Review expert recommendations
- Client provides additional direction
- Finalize priority list
```

### Week 2: First Iteration Build
```
Thursday-Friday: Design refinements
- Implement top 5 high-impact improvements
- Update copy based on Copywriter's suggestions
- Optimize performance bottlenecks

Monday: Deploy changes + Monitor
- Push changes live
- Set up tracking
- Monitor KPIs
```

### Week 3: Validation & Second Round
```
Tuesday: Run second Expert Panel review
- Compare scores from Week 1 vs Week 3
- Identify remaining issues
- Measure improvement
```

---

## PART 5: FOR YOUR CONSULTANCY (Competitive Moat)

### This becomes your **WEBSITE QUALITY GUARANTEE**

**Your Pitch:**
"Most agencies build websites. We build websites through the eyes of 8 expert judgesâ€”conversion specialist, UX researcher, brand strategist, copywriter, designer, SEO expert, performance engineer, and accessibility auditor.

Every website gets a professional critique that would cost Â£5,000+ if you hired each expert separately.

Then we iterate based on their feedback.

**Result:** Websites that convert better, rank faster, and load smoother."

### Pricing Model

**Service 1: Website Audit (Â£1,997)**
- 8-Expert Panel review of existing website
- 8 comprehensive reports
- Aggregated scoring + action plan
- Client receives: All 8 reports + prioritized improvement list
- Timeline: 1-2 weeks

**Service 2: Website Build with Expert Review (Â£4,997 - Â£7,997)**
- RAG-powered onboarding (auto-gathers data)
- Expert Panel review of competitors + existing sites
- Full website design/build
- Post-launch Expert Panel review
- 1 round of revisions based on feedback

**Service 3: Website Optimization (Â£2,497)**
- Expert Panel review of current site
- Implementation of top 10 recommendations
- Performance optimization
- A/B testing setup
- Monthly monitoring + reporting (3 months)

---

## IMPLEMENTATION ROADMAP

### Phase 1: Build the Expert Panel Framework (Week 1-2)
```
- [ ] Create 8 critique templates (one per expert)
- [ ] Write 8 sets of 8 questions (8 experts Ã— 8 questions)
- [ ] Create scoring rubrics (how to score 0-10)
- [ ] Create aggregation template (combine 8 scores)
```

### Phase 2: Build RAG Onboarding (Week 3-4)
```
- [ ] Set up RAG crawler (LinkedIn, website, social media)
- [ ] Build AI analysis engine (extract tone, visual style, messaging)
- [ ] Create smart onboarding form (auto-filled + targeted questions)
- [ ] Test end-to-end (from signup to onboarding brief)
```

### Phase 3: Create System Documentation (Week 5)
```
- [ ] Write: "How to Run an Expert Panel Review"
- [ ] Write: "How to Interpret Expert Scores"
- [ ] Write: "From Feedback to Action Plan"
- [ ] Create: Critique templates (ready to go)
```

### Phase 4: Beta Test with Real Client (Week 6+)
```
- [ ] Launch onboarding with first client
- [ ] Run Expert Panel on their site
- [ ] Build website based on recommendations
- [ ] Document process + refine
- [ ] Document results + case study
```

---

## THIS IS YOUR COMPETITIVE MOAT

**Why this works:**
1. **8-Expert Panel** = Â£5,000+ value clients can't get elsewhere
2. **RAG Onboarding** = 80% of data-gathering automated (save 20 hours per project)
3. **Iterative Process** = Continuous improvement, not one-shot
4. **Metrics-Based** = Clear scoring, not subjective feedback
5. **Documented** = Repeatable, scalable, trainable

**Time to payoff:**
- Week 1-5: Build system (40 hours)
- Project 1: Demonstrate value
- Project 2-10: Rapid delivery (8-12 hours per project vs. 40+ hours)
- ROI: Breakeven at 3-4 projects

**Competitive advantage:**
No one else has this. It's a unique system that becomes your brand promise.

**Can be expanded:**
- Train others to run panels
- Sell the audit as standalone service
- Build certification program ("Website Quality Certified")
- License the system to other agencies

---

**You now have a complete website critique system + client onboarding pipeline that becomes your consultancy's unique offering.**

**Start building Phase 1 this week.**

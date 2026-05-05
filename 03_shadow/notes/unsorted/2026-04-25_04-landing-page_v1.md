---
title: "Landing Page Spec — 12-Part High-Converting Structure"
id: "04-landing-page"
version: 1
created: "2026-04-25"
type: "document"
topic_type: "unsorted"
audience: "internal"
layer: "shadow"
status: "filed"
signed_by: "Devon, 2026-04-25, devin-992682c244cf444f91e0a516498afbfd"
---

# Landing Page Spec — 12-Part High-Converting Structure

## Principles Applied

| Principle | Application |
|-----------|-------------|
| Visual Hierarchy | Size, color, spacing guide the eye |
| Cognitive Load | One CTA per section, minimal text |
| Social Proof | Testimonials, logos, case study |
| Peak-End Rule | Strong headline, strong final CTA |
| Z-Pattern | Key elements on Z-path for scanning |

---

## Page Structure

### Section 1: Hero (Above Fold)

**Goal:** Capture attention, communicate value, prompt action

```html
<section id="hero">
  <h1>Stop Losing £15K/Year to Junk Calls</h1>
  <p class="subheadline">
    Your AI receptionist filters time-wasters so you 
    only speak to customers ready to pay.
  </p>
  <div class="cta-group">
    <a href="#signup" class="btn-primary">Start Free Trial</a>
    <a href="#demo" class="btn-secondary">See How It Works</a>
  </div>
  <p class="trust-line">
    ✓ 14-day free trial  ✓ No card required  ✓ Cancel anytime
  </p>
</section>
```

**Design Notes:**
- Headline: 48-64px, bold, dark
- Subheadline: 20-24px, medium gray
- Primary CTA: Contrasting color (purple/blue), large
- Secondary CTA: Ghost/outline style
- Trust line: Small, muted, below CTAs

---

### Section 2: Problem Agitation

**Goal:** Make the pain visceral and relatable

```html
<section id="problem">
  <h2>Sound familiar?</h2>
  <ul class="pain-points">
    <li>📱 Your phone rings 40+ times a day</li>
    <li>⏰ Half are quote-shoppers who'll never book</li>
    <li>😤 You waste 2 hours on calls that go nowhere</li>
    <li>💸 That's £15,000/year in lost billable time</li>
  </ul>
  <p class="kicker">Meanwhile, real emergencies go to voicemail.</p>
</section>
```

**Design Notes:**
- Emoji icons for visual interest
- Each pain point on own line
- Final line ("kicker") in bolder/different color
- Whitespace around section

---

### Section 3: Demo Video

**Goal:** Show the product in action, build understanding

```html
<section id="demo">
  <h2>Hear Gemma Handle a Real Call</h2>
  <p>90 seconds. See why businesses switch to Covered AI.</p>
  <div class="video-container">
    <video 
      poster="/images/demo-thumbnail.jpg"
      src="/videos/gemma-demo.mp4"
      controls
    />
  </div>
</section>
```

**Video Content:**
1. Phone rings (0:00-0:05)
2. Gemma answers, greets caller (0:05-0:15)
3. Caller explains problem (0:15-0:30)
4. Gemma asks qualifying questions (0:30-0:50)
5. Gemma confirms details, promises callback (0:50-1:10)
6. Owner receives WhatsApp notification (1:10-1:20)
7. End screen with CTA (1:20-1:30)

---

### Section 4: How It Works

**Goal:** Simplify understanding, reduce perceived complexity

```html
<section id="how-it-works">
  <h2>Live in 3 Minutes</h2>
  <div class="steps">
    <div class="step">
      <span class="step-number">1</span>
      <div class="step-icon">📱</div>
      <h3>Forward Your Calls</h3>
      <p>One simple call forward to your Covered number.</p>
    </div>
    <div class="step">
      <span class="step-number">2</span>
      <div class="step-icon">🤖</div>
      <h3>Gemma Answers</h3>
      <p>24/7, sounds human, never misses a beat.</p>
    </div>
    <div class="step">
      <span class="step-number">3</span>
      <div class="step-icon">🔔</div>
      <h3>You Get Notified</h3>
      <p>WhatsApp ping with lead details — only the good ones.</p>
    </div>
  </div>
</section>
```

**Design Notes:**
- Three columns on desktop, stacked on mobile
- Large step numbers (1, 2, 3)
- Icons above text
- Short, punchy descriptions

---

### Section 5: Benefits

**Goal:** Communicate value in user terms (not features)

```html
<section id="benefits">
  <h2>What Changes When You're Covered</h2>
  
  <div class="benefit">
    <div class="benefit-icon">✅</div>
    <div class="benefit-content">
      <h3>Never miss an emergency again</h3>
      <p>Gemma knows a burst pipe from a dripping tap. 
         Emergencies get flagged. You get pinged instantly.</p>
    </div>
  </div>
  
  <div class="benefit">
    <div class="benefit-icon">✅</div>
    <div class="benefit-content">
      <h3>Reclaim 2 hours every day</h3>
      <p>No more "just getting a quote" calls eating your time. 
         Gemma handles the tyre-kickers.</p>
    </div>
  </div>
  
  <div class="benefit">
    <div class="benefit-icon">✅</div>
    <div class="benefit-content">
      <h3>Know who's calling before you call back</h3>
      <p>Name, address, postcode, job type, urgency level. 
         All in your WhatsApp before you dial.</p>
    </div>
  </div>
  
  <div class="benefit">
    <div class="benefit-icon">✅</div>
    <div class="benefit-content">
      <h3>Automatic follow-up that books jobs</h3>
      <p>Our 12-touch nurture sequence converts leads 
         while you're on the tools.</p>
    </div>
  </div>
</section>
```

---

### Section 6: Trust Signals

**Goal:** Establish credibility with logos and quick testimonial

```html
<section id="trust">
  <p class="trust-label">Trusted by UK Tradespeople</p>
  <div class="logo-bar">
    <img src="/logos/titan-plumbing.png" alt="Titan Plumbing" />
    <img src="/logos/callum-groundworks.png" alt="Callum's Groundworks" />
    <img src="/logos/client-3.png" alt="Client 3" />
    <img src="/logos/client-4.png" alt="Client 4" />
  </div>
  
  <blockquote class="featured-testimonial">
    <p>"I used to hide my phone number because I had too many calls. 
       Now Gemma handles the filtering and I only speak to real 
       customers. Game changer."</p>
    <footer>
      <img src="/images/ralph.jpg" alt="Ralph" class="testimonial-photo" />
      <cite>Ralph, Titan Plumbing Solutions</cite>
    </footer>
  </blockquote>
</section>
```

---

### Section 7: Case Study

**Goal:** Provide detailed proof with numbers

```html
<section id="case-study">
  <h2>Ralph's Results After 30 Days</h2>
  
  <div class="results-table">
    <div class="result-row">
      <div class="result-before">
        <span class="label">Before</span>
        <span class="value">40+ calls/day</span>
      </div>
      <div class="result-after">
        <span class="label">After</span>
        <span class="value">8 qualified leads/day</span>
      </div>
      <div class="result-impact">
        <span class="value">80% less phone time</span>
      </div>
    </div>
    
    <div class="result-row">
      <div class="result-before">
        <span class="label">Before</span>
        <span class="value">2 hours on phone daily</span>
      </div>
      <div class="result-after">
        <span class="label">After</span>
        <span class="value">15 mins on callbacks</span>
      </div>
      <div class="result-impact">
        <span class="value">£1,200/mo time saved</span>
      </div>
    </div>
    
    <div class="result-row">
      <div class="result-before">
        <span class="label">Before</span>
        <span class="value">Missed emergencies</span>
      </div>
      <div class="result-after">
        <span class="label">After</span>
        <span class="value">Zero missed emergencies</span>
      </div>
      <div class="result-impact">
        <span class="value">3 emergency jobs saved</span>
      </div>
    </div>
  </div>
  
  <a href="/case-studies/ralph" class="link-arrow">Read Full Case Study →</a>
</section>
```

---

### Section 8: Pricing

**Goal:** Clear, simple pricing with value emphasis

```html
<section id="pricing">
  <h2>Simple Pricing. No Surprises.</h2>
  
  <div class="pricing-grid">
    <div class="pricing-card">
      <h3>Starter</h3>
      <div class="price">£297<span>/month</span></div>
      <ul class="features">
        <li>✓ AI phone answering 24/7</li>
        <li>✓ WhatsApp lead alerts</li>
        <li>✓ Lead capture & CRM</li>
        <li>✓ Review request automation</li>
      </ul>
      <a href="#signup" class="btn-primary">Start Free Trial</a>
    </div>
    
    <div class="pricing-card featured">
      <span class="badge">Most Popular</span>
      <h3>Growth</h3>
      <div class="price">£397<span>/month</span></div>
      <ul class="features">
        <li>✓ Everything in Starter</li>
        <li>✓ 12-touch lead nurture</li>
        <li>✓ Personalised AI video</li>
        <li>✓ SMS follow-up</li>
      </ul>
      <a href="#signup" class="btn-primary">Start Free Trial</a>
    </div>
    
    <div class="pricing-card">
      <h3>Scale</h3>
      <div class="price">£497<span>/month</span></div>
      <ul class="features">
        <li>✓ Everything in Growth</li>
        <li>✓ Multi-location support</li>
        <li>✓ Priority support</li>
        <li>✓ Custom integrations</li>
      </ul>
      <a href="#contact" class="btn-secondary">Contact Sales</a>
    </div>
  </div>
  
  <p class="pricing-note">
    14-day free trial. No credit card required. Cancel anytime.
  </p>
</section>
```

---

### Section 9: FAQ

**Goal:** Overcome objections, reduce friction

```html
<section id="faq">
  <h2>Questions? Answered.</h2>
  
  <div class="faq-list">
    <details class="faq-item">
      <summary>Does it sound like a robot?</summary>
      <p>No. Gemma uses the latest AI voice technology with a 
         natural Northern British accent. Most callers don't 
         realise they're speaking to AI.</p>
    </details>
    
    <details class="faq-item">
      <summary>What if there's a real emergency?</summary>
      <p>Gemma recognises emergency keywords (burst pipe, no power, 
         gas smell) and flags them instantly. You get a priority 
         WhatsApp within seconds.</p>
    </details>
    
    <details class="faq-item">
      <summary>Can I customise what Gemma says?</summary>
      <p>Yes. We tailor Gemma's script to your business, services, 
         and service area during setup.</p>
    </details>
    
    <details class="faq-item">
      <summary>What happens to my existing number?</summary>
      <p>Keep it. You just forward calls to your Covered number. 
         Takes 2 minutes to set up.</p>
    </details>
    
    <details class="faq-item">
      <summary>Is my data safe?</summary>
      <p>Yes. We're GDPR compliant. Your customer data stays yours. 
         We never sell it.</p>
    </details>
  </div>
</section>
```

---

### Section 10: Final CTA

**Goal:** Strong close, remove all friction

```html
<section id="final-cta">
  <h2>Ready to Stop Losing Money to Junk Calls?</h2>
  <p>Start your free trial today. Live in 3 minutes.</p>
  <p class="subtext">No credit card required.</p>
  
  <a href="#signup" class="btn-primary btn-large">
    Start Free Trial — It's Free
  </a>
  
  <p class="alternative">
    or call us: <a href="tel:0800XXXXXXX">0800 XXX XXXX</a>
  </p>
</section>
```

---

### Section 11: Footer

```html
<footer id="footer">
  <div class="footer-brand">
    <img src="/logo.svg" alt="Covered AI" />
    <p>Every call answered. Only the good ones reach you.</p>
  </div>
  
  <nav class="footer-links">
    <a href="/privacy">Privacy Policy</a>
    <a href="/terms">Terms of Service</a>
    <a href="/contact">Contact</a>
  </nav>
  
  <p class="copyright">
    © 2025 Covered AI Ltd. Newcastle upon Tyne.
  </p>
</footer>
```

---

## Core Web Vitals Requirements

Google ranking factor. Must pass all three:

| Metric | What It Measures | Target | How to Achieve |
|--------|------------------|--------|----------------|
| **LCP** | Largest Contentful Paint | < 2.5s | Optimize images, lazy load below fold, fast hosting |
| **INP** | Interaction to Next Paint | < 200ms | Minimize JavaScript, avoid long tasks |
| **CLS** | Cumulative Layout Shift | < 0.1 | Set image dimensions, avoid injected content |

### Implementation

```html
<!-- Preload critical assets -->
<link rel="preload" href="/fonts/main.woff2" as="font" crossorigin>
<link rel="preload" href="/images/hero.webp" as="image">

<!-- Set explicit dimensions on images -->
<img src="hero.webp" width="1200" height="600" alt="..." loading="eager">
<img src="below-fold.webp" width="800" height="400" alt="..." loading="lazy">
```

```css
/* Prevent layout shift */
img, video {
  max-width: 100%;
  height: auto;
  aspect-ratio: attr(width) / attr(height);
}

/* Reserve space for dynamic content */
.testimonial-carousel {
  min-height: 200px;
}
```

---

## Pre-Launch SEO Checklist

```markdown
- [ ] All URLs use consistent format (no trailing slashes)
- [ ] XML sitemap.xml created
- [ ] robots.txt configured
- [ ] HTTPS on all pages
- [ ] Breadcrumb navigation (schema.org markup)
- [ ] Custom 404 page
- [ ] No redirect chains
- [ ] Canonical tags on all pages
- [ ] Unique title + meta description per page
- [ ] Mobile load time < 3 seconds
- [ ] Core Web Vitals passing
- [ ] Open Graph tags for social sharing
- [ ] Schema.org JSON-LD for SoftwareApplication
```

---

## A/B Test Framework

Validated conversion impacts from research:

| Element | Test | Expected Impact |
|---------|------|----------------|
| Headline | "£15K/year" vs "2 hours/day" | +30% |
| CTA text | "Start Free Trial" vs "Get Started Free" | +139% |
| Testimonials | With vs without Ralph quote | +34% |
| Trust badges | With vs without GDPR badge | +107% |
| Video | With vs without demo video | +12% |
| Form fields | 3 fields vs 5 fields | Significant |

### Implementation

```typescript
// Simple A/B test utility
function getVariant(testName: string): 'A' | 'B' {
  const stored = localStorage.getItem(`ab_${testName}`);
  if (stored) return stored as 'A' | 'B';
  
  const variant = Math.random() < 0.5 ? 'A' : 'B';
  localStorage.setItem(`ab_${testName}`, variant);
  
  // Track assignment
  trackEvent('ab_assignment', { test: testName, variant });
  
  return variant;
}

// Usage
const headlineVariant = getVariant('headline_v1');
const headline = headlineVariant === 'A' 
  ? "Stop Losing £15K/Year to Junk Calls"
  : "Stop Wasting 2 Hours/Day on Junk Calls";
```

---

## Technical Requirements

### Performance

| Metric | Target |
|--------|--------|
| First Contentful Paint | < 1.5s |
| Largest Contentful Paint | < 2.5s |
| Time to Interactive | < 3.0s |
| Cumulative Layout Shift | < 0.1 |

### SEO

```html
<head>
  <title>Covered AI | AI Phone Answering for UK Businesses</title>
  <meta name="description" content="Stop losing £15K/year to junk calls. 
    Covered AI answers your phone 24/7, filters time-wasters, and only 
    pings you for real opportunities. Try free for 14 days." />
  <meta name="keywords" content="AI phone answering, virtual receptionist, 
    UK, tradesman, plumber, electrician, missed calls" />
  
  <!-- Open Graph -->
  <meta property="og:title" content="Stop Losing £15K/Year to Junk Calls" />
  <meta property="og:description" content="Your AI receptionist filters 
    time-wasters so you only speak to customers ready to pay." />
  <meta property="og:image" content="/images/og-image.jpg" />
  
  <!-- Schema.org -->
  <script type="application/ld+json">
  {
    "@context": "https://schema.org",
    "@type": "SoftwareApplication",
    "name": "Covered AI",
    "description": "AI phone answering for UK service businesses",
    "applicationCategory": "BusinessApplication",
    "offers": {
      "@type": "Offer",
      "price": "297",
      "priceCurrency": "GBP"
    }
  }
  </script>
</head>
```

### Tracking

```javascript
// Key events to track
const TRACKING_EVENTS = [
  { event: 'page_view', section: 'landing' },
  { event: 'cta_click', location: 'hero' },
  { event: 'cta_click', location: 'pricing' },
  { event: 'cta_click', location: 'final' },
  { event: 'video_play', percent: 0 },
  { event: 'video_play', percent: 50 },
  { event: 'video_play', percent: 100 },
  { event: 'faq_expand', question: 'string' },
  { event: 'scroll_depth', percent: 25 },
  { event: 'scroll_depth', percent: 50 },
  { event: 'scroll_depth', percent: 75 },
  { event: 'scroll_depth', percent: 100 },
];
```

### A/B Test Priorities

| Priority | Element | Variants |
|----------|---------|----------|
| 1 | Headline | "£15K/year" vs "2 hours/day" framing |
| 2 | CTA text | "Start Free Trial" vs "Get Started Free" |
| 3 | Social proof | Testimonial first vs logos first |
| 4 | Video | Autoplay vs click-to-play |
| 5 | Pricing display | 3-column vs tabs |

---

## Mobile Considerations

- Hero CTA must be above fold
- Sticky CTA button appears on scroll
- Pricing cards stack vertically
- FAQ uses accordion pattern
- Video responsive with 16:9 aspect ratio
- All tap targets minimum 44x44px
- Phone number uses `tel:` link

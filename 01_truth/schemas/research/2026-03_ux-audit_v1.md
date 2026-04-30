---
title: "UX Audit"
id: "ux-audit"
version: 1
created: 2026-04-25
last_validated: 2026-04-25
type: document
topic_type: reference
status: imported
source_file: "amplified-partners-ux-audit.pdf"
signed_by: "Devon, 2026-04-25, devin-992682c244cf444f91e0a516498afbfd"
---

UX Design Audit
amplifiedpartners.ai
Pattern Library Analysis  ·  WCAG 3.0 Conformance Scoring
March 2026
Prepared by Byker Business Help  ·  Perplexity Computer
OVERALL GRADE
Below Bronze
Confidential — Amplified Partners UX Audit
Page 1

Confidential — Amplified Partners UX Audit
amplifiedpartners.ai · March 2026
Byker Business Help · Perplexity Computer
Page 2
Executive Summary
Metric
Value
Components Audited
11
Critical Issues
5
Major Issues
5
Moderate Issues
5
WCAG 3.0 Overall Grade
Below Bronze
WCAG 3.0 Category Scores
Category
Score
Rating
Description
Perceivable
2 / 4
Progress
Good contrast on main text. Critical failures on badge text
and small text throughout.
Operable
1 / 4
Very Poor
Focus indicators invisible on dark bg. No skip link. Touch
targets fail. Animation cannot be paused.
Understandabl
e
3 / 4
Pass
Content is clear and well-written. Language declared.
Predictable behaviour. Logical flow.
Robust
2 / 4
Progress
Missing ARIA landmarks. Ticker lacks aria-hidden. Works
with basic AT but not optimised.
CRITICAL ERROR: Tag badge contrast failure (1:1 ratio) would automatically invalidate Bronze
conformance under WCAG 3.0. This is classified as a Critical Error that overrides all other
scoring.
Methodology: Scored against the WCAG 3.0 Working Draft (March 2026). The draft uses
requirements-based assessment replacing the old A/AA/AAA model. Requirements are scored on a 0-4
scale (Very Poor to Excellent). Bronze conformance roughly equals current WCAG 2.2 AA.

Confidential — Amplified Partners UX Audit
amplifiedpartners.ai · March 2026
Byker Business Help · Perplexity Computer
Page 3
Design Tokens Extracted
Colour Palette
Token
Hex
Value
Usage
Contrast vs Background
(#0a0a08)
background
#0a0a08
Page background
N/A (base)
foreground
#f5f0e8
Primary text / headings
15.3:1
muted
#8a8578
Secondary text, captions
5.2:1
border
#2a2a26
Dividers, card borders
1.5:1
accent
#d4a843
CTA buttons, highlights, gold
accent
7.4:1
Typography
Font Family
Role
Weights
Sizes Found
Plus Jakarta Sans
Display /
Headings
700, 800,
900
104px (H1), 56px (quote), 48-52px (H2),
22.4px (H3), 19.2px (wordmark)
DM Sans
Body / UI
400, 500,
600
16.8px (body), 15.2-15.68px (content), 14px
(cards), 12-13px (small), 10.4-10.88px
(ticker)
Geist Mono
Code /
Attribution
400
11.2px (attribution), 10.4px (labels)
Animations Found
ticker — Continuous horizontal scroll for values marquee (CSS @keyframes)
fadeUp — Content entrance animation on scroll
fadeIn — Opacity transition on element reveal

Confidential — Amplified Partners UX Audit
amplifiedpartners.ai · March 2026
Byker Business Help · Perplexity Computer
Page 4
Responsive Breakpoints
Only one breakpoint was detected: 640px. This single breakpoint creates a binary
mobile/desktop layout with no intermediate tablet styling. The gap between 640px and
1024px is unaddressed.

Confidential — Amplified Partners UX Audit
amplifiedpartners.ai · March 2026
Byker Business Help · Perplexity Computer
Page 5
Component Audit
Navigation Bar   [NAVIGATION]
FRAGILE
Score: 45/100
Issues Found:
• No hamburger menu on mobile — nav reduces to just logo + button, no way to navigate to
other pages/sections
• Single breakpoint (640px) leaves tablet awkwardly styled
• Focus outline uses default browser style (rgb(16,16,16) auto 1px) — nearly invisible on dark
background
• No skip-link present
• No ARIA landmark role=banner on header element
• CTA is only a mailto link — no navigation to page sections
WCAG 3.0 Specific Issues:
• Focus indicator contrast fails WCAG 3 'Focus appearance' requirement — dark outline on
dark bg
• No skip navigation violates 'Bypass blocks' requirement
• Missing landmark roles reduce 'Structured content' compliance
Hero Section   [HERO]
PRODUCTION-READY
Score: 78/100
Issues Found:
• H1 is 104px desktop but fluid — scales well to mobile (48px at 375px)
• Body text at 16.8px is adequate but line-height at 29.4px creates generous spacing
• Gold subtitle (#d4a843 on #0a0a08) has 7.4:1 contrast ratio — passes AAA
• Email link (hello@amplifiedpartners.ai) touch target is only 155x21px — fails WCAG 2.2 target
size (24px minimum)
WCAG 3.0 Specific Issues:
• Touch target size for email link fails both WCAG 2.2 SC 2.5.8 and WCAG 3 draft target size
requirement
• No visible focus indicator customized for dark theme

Confidential — Amplified Partners UX Audit
amplifiedpartners.ai · March 2026
Byker Business Help · Perplexity Computer
Page 6
Values Ticker/Marquee   [MARQUEE]
FRAGILE
Score: 30/100
Issues Found:
• Text at 10.88px is below the 12px WCAG minimum for readable text
• No pause mechanism — users cannot stop the animation
• prefers-reduced-motion is NOT respected (no media query found in any stylesheet)
• Ticker elements overflow viewport bounds at ALL breakpoints (spans extend 500-2000px
beyond right edge)
• Content is purely decorative but not marked with aria-hidden
• Animation runs continuously which can cause vestibular issues
WCAG 3.0 Specific Issues:
• Fails WCAG 3 'Motion from content' requirement — no user control over animation
• Fails 'Text appearance' requirement — text below minimum readable size
• Fails 'Pause, stop, hide' — auto-updating content cannot be paused
• Overflow elements create invisible scrollbar risk on some browsers
Data Stats Section   [CONTENT]
PRODUCTION-READY
Score: 72/100
Issues Found:
• External citation link '(Logic4training, 2025)' has touch target of only 133x16px
• ServiceTitan attribution link at 10.4px is below minimum text size
• Cards lack visible borders or clear separation on mobile
• Good semantic structure with clear data/estimate distinction
WCAG 3.0 Specific Issues:
• Touch target fails minimum size requirement
• Text below minimum readable size (10.4px)

Confidential — Amplified Partners UX Audit
amplifiedpartners.ai · March 2026
Byker Business Help · Perplexity Computer
Page 7
Feature List (You WITH AI)   [CONTENT]
PRODUCTION-READY
Score: 80/100
Issues Found:
• Good heading hierarchy (H2 with semantic emphasis)
• Feature numbers in gold provide visual rhythm
• Description text is well-sized at 15.68px
• Divider lines between features create clear grouping
WCAG 3.0 Specific Issues:
• Could benefit from aria description list markup for the numbered features
Three Doors Cards   [CARDS]
FRAGILE
Score: 42/100
Issues Found:
• Tag badges ('Free — 3 months', 'Connect what you have', 'Voice on your phone') show 1:1
contrast ratio — gold text on gold background (critical failure)
• Badge text at 10.4px is below minimum
• Cards are not interactive (no links, no hover state) despite looking like clickable cards
• On mobile, cards stack vertically but maintain same padding — creates excessive vertical
scrolling
• Card background color barely distinguishable from page background (subtle border only)
• No focus management — cards are not in tab order
WCAG 3.0 Specific Issues:
• CRITICAL: Tag badges completely fail color contrast — text is invisible to low-vision users
• Text below minimum size
• Cards that look interactive but aren't violate 'Predictable operation' principle

Confidential — Amplified Partners UX Audit
amplifiedpartners.ai · March 2026
Byker Business Help · Perplexity Computer
Page 8
Blockquote/Pull Quote   [BLOCKQUOTE]
PRODUCTION-READY
Score: 85/100
Issues Found:
• Strong typographic treatment — display size with Plus Jakarta Sans 900
• Good contrast of white text on dark background
• Attribution in monospace creates nice typographic contrast
• Monospace attribution at 11.2px is slightly below 12px minimum
WCAG 3.0 Specific Issues:
• Attribution text slightly below minimum readable size
About Section   [CONTENT]
PRODUCTION-READY
Score: 75/100
Issues Found:
• Gold left-border on principles creates good visual distinction
• Good semantic markup with clear content grouping
• Text size and line-height are comfortable for reading
• Horizontal rule separator is visually clear
WCAG 3.0 Specific Issues:
• Principles list would benefit from proper list markup (ul/li) for screen readers
CTA Section (Contact)   [CTA]
PRODUCTION-READY
Score: 82/100
Issues Found:
• Strong call to action with clear visual hierarchy
• Gold button provides high contrast against dark card
• Button text is dark on gold — good readability
• Footer info (location, registration) in muted text at 12px — at minimum acceptable size
WCAG 3.0 Specific Issues:
• Button meets target size requirements
• Good color contrast for the CTA

Confidential — Amplified Partners UX Audit
amplifiedpartners.ai · March 2026
Byker Business Help · Perplexity Computer
Page 9
Primary CTA Button (See how it works)   [BUTTON]
PRODUCTION-READY
Score: 76/100
Issues Found:
• Good contrast: dark text on gold background
• Adequate touch target size
• No hover state animation/transition visible
• Focus state uses default browser outline — nearly invisible
WCAG 3.0 Specific Issues:
• Focus appearance needs custom styling for dark theme
Footer   [FOOTER]
FRAGILE
Score: 35/100
Issues Found:
• No footer navigation — single-page site has no section links
• No accessibility statement link
• No privacy policy or terms link
• No social media links
• Missing role=contentinfo (has footer element but relies on implicit role)
WCAG 3.0 Specific Issues:
• Missing consistent help mechanism (no help link, FAQ, or contact in footer)
• Missing accessibility statement — increasingly expected for WCAG 3 conformance

Confidential — Amplified Partners UX Audit
amplifiedpartners.ai · March 2026
Byker Business Help · Perplexity Computer
Page 10
Responsive Breakdown
Viewpor
t
Verdic
t
Key Issues
320px
Poor
25 sub-12px text elements, 5 overflow elements, ticker breaks bounds
375px
Poor
Same sub-12px issues, overflow persists, hero scales acceptably
414px
Poor
Identical to 375px — no breakpoint differentiation
768px
Fair
Layout improves but still uses mobile styling (only breakpoint is 640px),
sub-12px text persists
1024px
Good
Desktop layout engaged, columns work well, ticker overflow continues
1280px
Good
Intended design viewport, works as designed, small text issues remain
1440px
Good
Scales well, generous whitespace, same global issues
1920px
Fair
Content doesn't max-width constrain — some sections feel too wide
The site uses a single CSS breakpoint at 640px, creating a binary mobile/desktop layout.
Tablet viewports (768px) still receive mobile styling, and ultra-wide displays (1920px) lack
max-width constraints on content sections.

Confidential — Amplified Partners UX Audit
amplifiedpartners.ai · March 2026
Byker Business Help · Perplexity Computer
Page 11
Pretty vs Production-Ready Matrix
This matrix separates visual polish (how good it looks) from engineering robustness (how
well it works for all users, devices, and assistive technologies). A component can be
aesthetically beautiful yet functionally fragile.
Component
Aesthetic
Score
Robustness Score
Production-Ready
?
Navigation Bar
65%
45%
NO
Hero Section
90%
78%
YES
Values Ticker/Marquee
72%
30%
NO
Data Stats Section
78%
72%
YES
Feature List (You WITH AI)
85%
80%
YES
Three Doors Cards
75%
42%
NO
Blockquote/Pull Quote
95%
85%
YES
About Section
82%
75%
YES
CTA Section (Contact)
90%
82%
YES
Primary CTA Button (See how it
works)
88%
76%
YES
Footer
50%
35%
NO
Key insight: The site achieves high aesthetic scores across most components (average
79%) but significantly lower robustness scores (average 64%). The design is visually
polished but accessibility, responsive, and semantic foundations need work.

Confidential — Amplified Partners UX Audit
amplifiedpartners.ai · March 2026
Byker Business Help · Perplexity Computer
Page 12
Improved Component Code
The following code samples provide remediated versions of the five most critical
components. Each fix addresses the WCAG 3.0 failures identified in the audit.
A. Fixed Navigation
Adds skip link, ARIA landmarks, hamburger menu for mobile, multiple breakpoints (375px, 640px,
768px, 1024px), and custom gold focus ring.

Confidential — Amplified Partners UX Audit
amplifiedpartners.ai · March 2026
Byker Business Help · Perplexity Computer
Page 13
:root {
--amp-bg: #0a0a08;
--amp-fg: #f5f0e8;
--amp-muted: #8a8578;
--amp-border: #2a2a26;
--amp-accent: #d4a843;
--amp-accent-hover: #c49a3d;
--amp-focus: #d4a843;
--amp-focus-offset: 2px;
--font-display: 'Plus Jakarta Sans', sans-serif;
--font-body: 'DM Sans', sans-serif;
}
 
/* Skip Link */
.amp-skip-link {
position: absolute;
left: -9999px;
top: auto;
z-index: 1000;
padding: 0.75rem 1.5rem;
background: var(--amp-accent);
color: var(--amp-bg);
font-weight: 600;
text-decoration: none;
}
.amp-skip-link:focus {
left: 1rem;
top: 1rem;
}
 
/* Header */
.amp-header {
position: sticky; top: 0; z-index: 100;
background: rgba(10, 10, 8, 0.96);
backdrop-filter: blur(10px);
border-bottom: 1px solid var(--amp-border);
padding: 1rem 1.5rem;
display: flex; align-items: center;
justify-content: space-between;
}
 
/* Nav */
.amp-nav { display: flex; align-items: center; gap: 1.5rem; }
.amp-nav a { color: var(--amp-fg); text-decoration: none;
font-size: 0.9rem; padding: 0.5rem; }
.amp-nav a:focus-visible {
outline: 2px solid var(--amp-focus);
outline-offset: var(--amp-focus-offset);
}
 
/* Hamburger (mobile) */
.amp-hamburger {
display: none; background: none; border: none;
color: var(--amp-fg); padding: 0.5rem;
min-width: 44px; min-height: 44px;

Confidential — Amplified Partners UX Audit
amplifiedpartners.ai · March 2026
Byker Business Help · Perplexity Computer
Page 14
cursor: pointer;
}
.amp-hamburger:focus-visible {
outline: 2px solid var(--amp-focus);
outline-offset: var(--amp-focus-offset);
}
 
@media (max-width: 375px) {
.amp-nav { display: none; }
.amp-hamburger { display: flex; }
}
@media (max-width: 640px) {
.amp-nav { display: none; }
.amp-hamburger { display: flex; }
}
@media (min-width: 641px) and (max-width: 768px) {
.amp-nav a { font-size: 0.82rem; }
}
@media (min-width: 1024px) {
.amp-nav { gap: 2rem; }
}
<!-- Usage -->
<a href="#main" class="amp-skip-link">
Skip to main content
</a>
<header class="amp-header" role="banner">
<span class="amp-wordmark">Amplified.</span>
<nav class="amp-nav" aria-label="Main navigation">
<a href="#how-it-works">How it works</a>
<a href="#about">About</a>
<a href="mailto:hello@amplifiedpartners.ai"
class="btn-amber">Get in touch</a>
</nav>
<button class="amp-hamburger"
aria-label="Open menu" aria-expanded="false">
<svg width="24" height="24">...</svg>
</button>
</header>
B. Fixed Ticker/Marquee
Adds overflow containment, pause on hover/focus, prefers-reduced-motion support, aria-hidden for
decorative content, and minimum 12px text.

Confidential — Amplified Partners UX Audit
amplifiedpartners.ai · March 2026
Byker Business Help · Perplexity Computer
Page 15
.amp-ticker-wrap {
overflow: hidden;
position: relative;
padding: 0.75rem 0;
border-top: 1px solid var(--amp-border);
border-bottom: 1px solid var(--amp-border);
}
 
@keyframes ticker {
0% { transform: translateX(0); }
100% { transform: translateX(-50%); }
}
 
.amp-ticker-track {
display: flex;
gap: 2rem;
animation: ticker 30s linear infinite;
width: max-content;
}
 
/* Pause on hover and focus-within */
.amp-ticker-wrap:hover .amp-ticker-track,
.amp-ticker-wrap:focus-within .amp-ticker-track {
animation-play-state: paused;
}
 
/* Respect prefers-reduced-motion */
@media (prefers-reduced-motion: reduce) {
.amp-ticker-track {
animation: none;
}
}
 
.amp-ticker-item {
font-size: 12px; /* Minimum readable size */
letter-spacing: 0.1em;
color: var(--amp-muted);
white-space: nowrap;
text-transform: uppercase;
}
 
.amp-ticker-dot {
color: var(--amp-accent);
font-size: 12px;
}
 
<!-- HTML -->
<div class="amp-ticker-wrap"
aria-hidden="true"
role="presentation">
<div class="amp-ticker-track">
<span class="amp-ticker-item">RADICAL HONESTY</span>
<span class="amp-ticker-dot">&#9670;</span>
<span class="amp-ticker-item">RADICAL TRANSPARENCY</span>
<span class="amp-ticker-dot">&#9670;</span>

Confidential — Amplified Partners UX Audit
amplifiedpartners.ai · March 2026
Byker Business Help · Perplexity Computer
Page 16
<!-- ...duplicated for seamless loop... -->
</div>
</div>
C. Fixed Three Doors Cards
Fixes critical badge contrast (dark text on gold background instead of gold-on-gold), adds CSS Grid
layout, minimum 12px text, and proper heading hierarchy.

Confidential — Amplified Partners UX Audit
amplifiedpartners.ai · March 2026
Byker Business Help · Perplexity Computer
Page 17
.amp-doors-grid {
display: grid;
grid-template-columns: 1fr;
gap: 1.5rem;
}
@media (min-width: 768px) {
.amp-doors-grid {
grid-template-columns: repeat(3, 1fr);
}
}
 
.amp-door-card {
background: #141412;
border: 1px solid var(--amp-border);
padding: 2rem;
display: flex;
flex-direction: column;
}
 
/* FIXED: Tag badge contrast */
/* BEFORE: color: #d4a843 on background: rgba(212,168,67,0.1)
= gold text on near-gold bg = 1:1 contrast (FAIL) */
/* AFTER: dark text on solid gold background */
.amp-door-tag {
background: var(--amp-accent); /* #d4a843 solid gold */
color: #0a0a08; /* dark text */
padding: 0.25rem 0.75rem;
font-size: 12px; /* min 12px */
font-weight: 600;
letter-spacing: 0.06em;
display: inline-block;
align-self: flex-start;
}
 
.amp-door-number {
font-family: 'Geist Mono', monospace;
font-size: 12px;
color: var(--amp-accent);
}
 
.amp-door-card h3 {
font-family: var(--font-display);
font-size: 1.4rem;
font-weight: 700;
color: var(--amp-fg);
margin: 1rem 0 0.75rem;
}
 
.amp-door-card p {
font-size: 14px; /* above 12px minimum */
line-height: 1.7;
color: var(--amp-muted);
}
 
.amp-door-tagline {

Confidential — Amplified Partners UX Audit
amplifiedpartners.ai · March 2026
Byker Business Help · Perplexity Computer
Page 18
font-size: 13px;
font-weight: 500;
color: var(--amp-fg);
margin-top: auto;
padding-top: 1rem;
border-top: 1px solid var(--amp-border);
}
D. Fixed Footer
Adds footer navigation, legal links, accessibility statement link, minimum 44px touch targets, and
role=contentinfo.

Confidential — Amplified Partners UX Audit
amplifiedpartners.ai · March 2026
Byker Business Help · Perplexity Computer
Page 19
.amp-footer {
border-top: 1px solid var(--amp-border);
padding: 3rem 1.5rem 2rem;
}
 
.amp-footer-grid {
display: grid;
grid-template-columns: 1fr;
gap: 2rem;
max-width: 1100px;
margin: 0 auto;
}
@media (min-width: 768px) {
.amp-footer-grid {
grid-template-columns: 1fr 1fr 1fr;
}
}
 
.amp-footer-nav a,
.amp-footer-legal a {
color: var(--amp-muted);
text-decoration: none;
font-size: 14px;
display: inline-block;
min-height: 44px; /* Minimum touch target */
line-height: 44px;
padding: 0 0.25rem;
}
.amp-footer-nav a:hover,
.amp-footer-legal a:hover {
color: var(--amp-fg);
}
.amp-footer-nav a:focus-visible,
.amp-footer-legal a:focus-visible {
outline: 2px solid var(--amp-focus);
outline-offset: 2px;
}
 
.amp-footer-copyright {
font-size: 12px;
color: var(--amp-muted);
margin-top: 2rem;
padding-top: 1.5rem;
border-top: 1px solid var(--amp-border);
}
 
<!-- HTML -->
<footer class="amp-footer" role="contentinfo">
<div class="amp-footer-grid">
<div class="amp-footer-brand">
<span class="amp-wordmark">Amplified.</span>
<p>Business intelligence for UK SMEs.</p>
</div>
<nav class="amp-footer-nav" aria-label="Footer navigation">
<a href="#how-it-works">How it works</a>

Confidential — Amplified Partners UX Audit
amplifiedpartners.ai · March 2026
Byker Business Help · Perplexity Computer
Page 20
<a href="#about">About</a>
<a href="mailto:hello@amplifiedpartners.ai">Contact</a>
</nav>
<div class="amp-footer-legal">
<a href="/accessibility">Accessibility Statement</a>
<a href="/privacy">Privacy Policy</a>
<a href="/terms">Terms of Service</a>
</div>
</div>
<p class="amp-footer-copyright">
&copy; 2026 Amplified Partners. Newcastle upon Tyne.
UK-registered. Covered AI.
</p>
</footer>
E. Global Focus Indicators
Establishes a consistent, visible focus ring system across all interactive elements with high contrast
mode support.

Confidential — Amplified Partners UX Audit
amplifiedpartners.ai · March 2026
Byker Business Help · Perplexity Computer
Page 21
/* Global focus-visible indicator */
*:focus-visible {
outline: 2px solid #d4a843;
outline-offset: 2px;
}
 
/* Buttons: inset focus for solid backgrounds */
.btn-amber:focus-visible {
outline: 2px solid #0a0a08;
outline-offset: 2px;
box-shadow: 0 0 0 4px #d4a843;
}
 
/* Links: standard outline */
a:focus-visible {
outline: 2px solid #d4a843;
outline-offset: 2px;
border-radius: 2px;
}
 
/* Form inputs */
input:focus-visible,
textarea:focus-visible,
select:focus-visible {
outline: 2px solid #d4a843;
outline-offset: 0;
border-color: #d4a843;
}
 
/* Cards and interactive containers */
[role="button"]:focus-visible,
[tabindex="0"]:focus-visible {
outline: 2px solid #d4a843;
outline-offset: 2px;
}
 
/* High Contrast Mode support */
@media (forced-colors: active) {
*:focus-visible {
outline: 2px solid LinkText;
outline-offset: 2px;
}
.btn-amber:focus-visible {
outline: 2px solid ButtonText;
box-shadow: none;
}
}
 
/* Remove default browser outlines only AFTER
custom focus styles are established */
*:focus:not(:focus-visible) {
outline: none;
}

Confidential — Amplified Partners UX Audit
amplifiedpartners.ai · March 2026
Byker Business Help · Perplexity Computer
Page 22
WCAG 3.0 Conformance Report
The WCAG 3.0 Working Draft (March 2026)1 replaces the binary pass/fail A/AA/AAA model
with a graduated scoring system. Requirements are scored on a 0-4 scale, and conformance
is awarded at Bronze, Silver, and Gold levels. Bronze conformance is roughly equivalent to
WCAG 2.2 AA2.
Category Scoring (Bronze Target: 3/4)
Category
Score
Rating
Gap to Bronze
Status
Perceivable
2 / 4
Progress
-1
Below Target
Operable
1 / 4
Very Poor
-2
Below Target
Understandable
3 / 4
Pass
0
MEETS
Robust
2 / 4
Progress
-1
Below Target
Critical Error Override
Under WCAG 3.0, certain failures are classified as Critical Errors that automatically
invalidate conformance regardless of overall scoring3. The tag badge contrast failure (1:1
ratio in the Three Doors Cards) renders text completely invisible to low-vision users and
constitutes such a Critical Error.
Remediation Priority
Priority
Action Items
P0 (Immediate)
Fix card badge contrast (dark text on gold bg)
Add prefers-reduced-motion media query
Add skip link to bypass navigation
P1 (This Sprint)
Fix focus indicators (gold outline on all interactive elements)
Increase all touch targets to minimum 44px
Fix all text below 12px minimum
P2 (Next Sprint)
Add ARIA landmarks (main, banner, contentinfo)
Add tablet breakpoints (768px, 1024px)
Add footer navigation with legal links

Confidential — Amplified Partners UX Audit
amplifiedpartners.ai · March 2026
Byker Business Help · Perplexity Computer
Page 23
P3 (Backlog)
Add accessibility statement page
Add structured data / schema.org
Implement error states for email CTA
1. WCAG 3.0 Working Draft, W3C, March 2026 — https://www.w3.org/TR/2026/WD-wcag-3.0-20260303/
2. WCAG 2.2 W3C Recommendation — https://www.w3.org/TR/WCAG22/
3. WCAG 3 Introduction, W3C WAI — https://www.w3.org/WAI/standards-guidelines/wcag/wcag3-intro/

Confidential — Amplified Partners UX Audit
amplifiedpartners.ai · March 2026
Byker Business Help · Perplexity Computer
Page 24
Global Issues Summary
Critical Issues (5)
• Card tag badges have 1:1 contrast ratio — text completely invisible against matching
background
• No prefers-reduced-motion support — ticker and fade animations cannot be stopped
• No skip-link for keyboard users to bypass navigation
• 25+ text elements across the site at 10-11px — below the 12px WCAG minimum
• Focus indicators use dark outline on dark background — functionally invisible
Major Issues (5)
• Single CSS breakpoint (640px) — no tablet-specific responsive design
• Ticker/marquee elements overflow at every viewport width
• Multiple touch targets below 24px minimum (links at 16-21px height)
• No main landmark element wrapping page content
• No structured data or proper semantic HTML for screen readers
Moderate Issues (5)
• Footer lacks navigation, legal links, and accessibility statement
• Cards look interactive but are not focusable or clickable
• No error states or loading states for email CTA
• Heading hierarchy is clean (H1→H2→H3) — this is good
• Lang attribute properly set to 'en' — this is good

Confidential — Amplified Partners UX Audit
amplifiedpartners.ai · March 2026
Byker Business Help · Perplexity Computer
Page 25
Sources & Methodology
Standards References
1. WCAG 3.0 Working Draft, W3C, March 2026 —
https://www.w3.org/TR/2026/WD-wcag-3.0-20260303/
2. WCAG 3 Introduction, W3C WAI —
https://www.w3.org/WAI/standards-guidelines/wcag/wcag3-intro/
3. WCAG 3.0 Explainer, W3C — https://www.w3.org/TR/wcag-3.0-explainer/
4. WCAG 2.2 W3C Recommendation — https://www.w3.org/TR/WCAG22/
5. WCAG 3 March 2026 Analysis, ADA QuickScan —
https://adaquickscan.com/blog/wcag-3-working-draft-march-2026-174-outcomes
Testing Methodology
• Testing performed using Playwright browser automation across 8 viewport sizes (320px,
375px, 414px, 768px, 1024px, 1280px, 1440px, 1920px)
• Colour contrast ratios calculated using WCAG luminance formula
• Component catalogue extracted via DOM analysis and computed style inspection
• Focus indicators tested via keyboard navigation simulation
• Touch target sizes measured from computed bounding rectangles
• All testing conducted 17 March 2026
This audit was prepared by Byker Business Help using Perplexity Computer. All findings represent the
state of amplifiedpartners.ai as tested on 17 March 2026. WCAG 3.0 is a Working Draft and
requirements may change before final recommendation.
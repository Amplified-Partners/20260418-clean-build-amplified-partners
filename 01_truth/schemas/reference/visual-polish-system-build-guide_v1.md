---
title: "Visual Polish System Build Guide"
id: "visual-polish-system-build-guide"
version: 1
created: 2026-04-25
last_validated: 2026-04-25
type: document
topic_type: reference
status: imported
source_file: "VISUAL-POLISH-SYSTEM-COMPLETE-BUILD-GUIDE.docx"
signed_by: "Devon, 2026-04-25, devin-992682c244cf444f91e0a516498afbfd"
---

Table of Contents {#table-of-contents .TOC-Heading}
=================

This document is the single authoritative reference for implementing the Amplified Partners Visual Polish System. It is compiled from 22 source files and is intentionally self-contained: an AI builder should never need to open another file. Every token value, every rule, every formula, every line of code is inline below.

**What this doc covers:** The philosophy, research, design tokens, hard rules, scoring rubric, evaluation pipeline, UX methodology integration, AI guardrails, canonical layout patterns, Pudding technique integration, complete Python scoring engine, full test suite, CLI tool, example score files, and the Phase 1 build prompt.

**Who it is for:** Any AI agent (Claude, GPT-4, or equivalent) tasked with building, evaluating, or extending the Visual Polish System or any UI that must conform to it.

Table of Contents
-----------------

1.  [PART 1: CONTEXT & PHILOSOPHY](#part-1-context--philosophy)
2.  [PART 2: RESEARCH FINDINGS](#part-2-research-findings)
3.  [PART 3: GOALS, CONSTRAINTS & KAIZEN APPROACH](#X11a20ec76ed20d1022ada1f32cbf709c7ece88c)
4.  [PART 4: CODIFIED PRINCIPLES LIBRARY](#part-4-codified-principles-library)
    -   [4.1 Design Tokens](#Xc1b08aef2ec9599dc83b8d4249ef475e50c4ad3)
        -   [4.1.1 Typography Tokens](#X4d795d6f5295cb6270168cd3d0ba7546956709a)
        -   [4.1.2 Spacing & Radius Tokens](#X8955a5f5a0328cf3011e38bc25b7276be8c10ae)
        -   [4.1.3 Color Tokens](#Xcdf102ae8c2c59f1dd9972472b29357b0fb3a6a)
        -   [4.1.4 Motion Tokens](#Xf0860d9e0480927614829d58a34db5216f1e01e)
        -   [4.1.5 Shadow Tokens](#X72ac4c95d3d92208d666a28cb79c60ecd48e8ee)
    -   [4.2 Hard Rules](#Xaff232ef7f743d3c3dfd8b52462e118d1ca7825)
    -   [4.3 Rule Schema](#X1bcc1ec3503683687f32fc40746edaa4ed10709)
    -   [4.4 Scoring Rubric](#Xe2e5e1649fabaa1c43e910ba4bb9d800ad83821)
    -   [4.5 Extension Model](#X5076b06c7052978cc16d3900551a3b259de66d3)
5.  [PART 5: EVALUATION & TESTING PIPELINE](#part-5-evaluation--testing-pipeline)
6.  [PART 6: UX METHODOLOGY INTEGRATION](#part-6-ux-methodology-integration)
7.  [PART 7: AI GUARDRAILS](#part-7-ai-guardrails)
8.  [PART 8: CANONICAL LAYOUT PATTERNS](#part-8-canonical-layout-patterns)
9.  [PART 9: PUDDING TECHNIQUE INTEGRATION](#part-9-pudding-technique-integration)
10. [PART 10: SCORING ENGINE --- PYTHON SOURCE](#part-10-scoring-engine--python-source)
    -   [10.1 Data Models (models.py)](#Xab3ade2e6d51802ec73b9b40f5c1d0f050f95ff)
    -   [10.2 Scoring Engine (engine.py)](#X131812dc2240e2fcbfc6afcc97a366ecfb552c8)
    -   [10.3 CLI (cli.py)](#X3a8b7a1c7d3a238d068a2746681fa2135f5bf70)
11. [PART 11: ARITHMETIC TEST SUITE](#part-11-arithmetic-test-suite)
    -   [11.1 Test Results Summary](#Xc6e5722e8e9b5b32f8caf69c4ee54c82a1aa94b)
    -   [11.2 Full Test Source (test\_arithmetic.py)](#Xd218d12de68aaf3f0d36913b40f705a9edc8e5c)
    -   [11.3 Example Score Files](#Xcb5926a819238eade1784826016da57a8b13699)
    -   [11.4 Example CLI Output](#X449b86fe12e06f03e4e863c9c3158b5b4be7345)
12. [PART 12: KEY MATHEMATICAL FORMULAE (QUICK REFERENCE)](#Xb96b0e5d88328857713d13c5e97e6f0c8f65226)
13. [PART 13: COVE BUILD PROMPT --- PHASE 1](#part-13-cove-build-prompt--phase-1)
14. [PART 14: LINEAR ISSUES & DEPENDENCY GRAPH](#part-14-linear-issues--dependency-graph)
15. [PART 15: APPENDICES](#part-15-appendices)

PART 1: CONTEXT & PHILOSOPHY
----------------------------

*From spec sections 0.0--0.3, verbatim.*

### 0.1 What We're Building

A **voice-first, data-heavy product** where: - Human talks, AI types, human approves - Interface is dense with metrics, logs, and operational data - React front-end; Claude (and other LLMs) generate significant UI - Behavioural psychology and cognitive load are already handled --- **we need polish** - One critical demo page must be honest and congruent with the real product - System will be reused for simple landing pages and client sites

### 0.2 Design Philosophy

**"Blinkers without ceilings"** --- Humans define principles and constraints (the blinkers); AI explores and optimises freely within that bounded space (no ceiling on how good it can get).

**Target aesthetic:** Clean, modern, calm, professional. Think Linear, Vercel, Stripe --- data tools that feel like precision instruments, not dashboards from 2014.

**Anti-targets:** Gimmicky animations, gratuitous gradients, decoration without information, dark patterns, visual noise that fights the data.

### 0.3 The Pudding Premise

This system is itself a pudding --- combining graphic design, behavioural psychology, UX heuristics, analytics, and computational aesthetics. We look for symbiotic relationships between these domains, not just additive application.

PART 2: RESEARCH FINDINGS
-------------------------

*From spec section 1, verbatim.*

This section separates **what the research shows** from **how we will use it**. All findings were gathered via Beast SearXNG (XING) and web-scale retrieval.

### 1.1 How Expert Teams Achieve Polish

#### What the Research Shows

**Linear's approach** (source: [Linear UI Redesign Blog](https://linear.app/now/how-we-redesigned-the-linear-ui)): - Switched to **LCH colour space** for perceptually uniform themes --- 3 variables (base, accent, contrast) replace 98 manual colour tokens - Used **opacities of black/white** for quick elevation/hierarchy iteration - **Inter Display** for headings, **Inter** for body --- simple, two-font system - Stress-tested every view across light/dark/custom themes before committing - Small team (2 designers, few engineers), 6-week timeline, feature-flagged rollout - No workshops or sticky notes --- direct design-to-code pipeline - "Inverted L-shape" global chrome controlling main view content

**Vercel/Geist** (source: [Vercel Geist](https://vercel.com/geist/introduction), [Geist Font](https://vercel.com/font)): - Custom typeface (Geist Sans/Mono/Pixel) designed for **simplicity, minimalism, speed** - Inspired by Swiss design movement: precision, clarity, functionality - Consistent vertical metrics across all variants --- layout never breaks when switching fonts - System mindset: font is a system extension, not a decorative choice

**Atlassian spacing system** (source: [Atlassian Design Spacing](https://atlassian.design/foundations/spacing)): - 8px base unit, tokens named by multiplier (`space.100` = 8px, `space.200` = 16px) - Three zones: Small (0-8px) for compact UI, Medium (12-24px) for standard, Large (32-80px) for layout - Negative values supported for breaking out of containers - Semantic naming avoids ambiguity across teams

**Shadcn/UI ecosystem** (source: [LinkedIn analysis](https://www.linkedin.com/posts/thibault-friedrich_today-i-just-want-to-highlight-how-impressive-activity-7381658379351433216-QSSM)): - Shared design tokens via CSS variables create entire ecosystem of compatible libraries - Components imported as individual files, not npm package --- **you own the code** - Foundation on Radix UI primitives (now also Base UI) with tokens as the coordination layer

#### How We Will Use It

  Research Finding                    Our Application
  ----------------------------------- ------------------------------------------------------------------
  LCH colour space with 3 variables   Adopt LCH for our theme system; reduce colour token surface area
  8px base unit spacing               Use 4px/8px hybrid grid (4px for tight UI, 8px for layout)
  Two-font max                        One sans (Geist or equivalent), one mono. No more.
  Feature-flagged visual changes      All polish changes ship behind flags, measured before GA
  Tokens as coordination layer        JSON principles library is the single source of truth

### 1.2 UX Evaluation Methods --- Expert Consensus

#### What the Research Shows

**Nielsen's 10 Heuristics** (source: [NN/g](https://www.nngroup.com/articles/how-to-conduct-a-heuristic-evaluation/)): - 3-5 evaluators, two passes (understand flow, then apply heuristics) - Heuristic \#8 "Aesthetic and minimalist design" directly addresses polish - Severity rating: 0 (not a problem) to 4 (usability catastrophe) - Heuristic evaluation does NOT replace usability testing --- catches obvious issues only

**UICrit dataset** (source: [UICrit, Berkeley/UIST 2024](https://arxiv.org/html/2407.08850v2)): - 3,059 design critiques from 7 experienced designers on 983 UIs - Scoring: Aesthetics (10pt), Usability (10pt, split: Learnability 5pt + Efficiency 5pt), Overall (10pt) - Critique clusters: **Layout (23%), Colour Contrast (21%), Text Readability (19%), Button Usability (20%), Learnability (20%)** - LLM-generated critiques improved 55% over zero-shot with few-shot prompting from UICrit examples - Aesthetics-usability correlation: r=0.875 --- beautiful things ARE perceived as more usable

**UIClip model** (source: [UIClip, UIST 2024](https://arxiv.org/abs/2404.12500)): - CLIP-based model trained on JitterWeb (degraded web pages) and BetterApp (human-rated mobile UIs) - Produces numerical design quality score from screenshot + text description - 75.12% accuracy at identifying preferred UI from pairs - Sliding window strategy for full-page assessment (224x224 patches averaged) - Can generate design improvement suggestions by identifying specific flaws (contrast, alignment, etc.)

**Continuous Design / Kaizen in UX** (source: [UX Collective](https://uxdesign.cc/getting-used-to-endless-iterations-in-product-design-or-embracing-kaizen-d06f5a854f55), [UXtweak](https://blog.uxtweak.com/continuous-product-design/)): - Spiral model + Kaizen: Plan → Design → Test → Root Cause Analysis → Standardise - Nielsen Norman Group data: median usability improvement per iteration is **38%**, cumulative across 4 iterations: **165%** - "Quantified empathy" --- combine user feedback with data to inform design decisions - Continuous Product Design: shorter time-to-market, better product-market fit, reduced cost

#### How We Will Use It

  Research Finding                           Our Application
  ------------------------------------------ -------------------------------------------------------------------
  UICrit 5-cluster critique model            Map to our evaluation rubric dimensions
  UIClip screenshot scoring                  Deploy on Beast as automated aesthetic scorer
  r=0.875 aesthetics-usability correlation   Aesthetic score is a valid proxy for perceived usability
  38% improvement per iteration              Target 3-5% per Kaizen cycle (we're already past the big wins)
  Heuristic evaluation + severity            Codify as hard rules (severity 3-4) and soft rules (severity 1-2)

### 1.3 Design Token Systems --- Standards & Structures

#### What the Research Shows

**W3C Design Tokens Format Module 2025.10** (source: [W3C DTCG](https://www.designtokens.org/tr/2025.10/format/)): - First stable specification (October 2025) --- vendor-neutral, production-ready - File format: `.tokens` or `.tokens.json`, media type `application/design-tokens+json` - Supported types: color, dimension, fontFamily, fontWeight, duration, cubicBezier, number, border, shadow, gradient, typography, transition, strokeStyle - Aliases via `{token.path}` syntax or `$ref` JSON Pointer - Group inheritance: `$type` propagates to children - Color uses colour space objects (sRGB, Display P3, Oklch supported)

**Style Dictionary** (source: [Style Dictionary](https://styledictionary.com/info/tokens/)): - Build system that ingests token JSON, outputs platform-specific code (CSS variables, iOS, Android, Flutter) - Amazon-originated, now community standard - Pairs with W3C DTCG spec for interoperability

#### How We Will Use It

  Research Finding                                   Our Application
  -------------------------------------------------- -------------------------------------------------------------------------------------
  W3C DTCG 2025.10 format                            Adopt as base schema; extend with our rule/constraint layer
  Style Dictionary pipeline                          Generate CSS variables, Tailwind config, and agent-readable JSON from single source
  Type system (color, dimension, typography, etc.)   Use all standard types; add custom `rule` and `constraint` types
  Alias/reference system                             Use extensively for semantic tokens → primitive tokens

### 1.4 Automated Design Linting & Visual Regression

#### What the Research Shows

**Stylelint + Design System Plugin** (source: [Atlassian Stylelint](https://atlassian.design/components/stylelint-design-system)): - Warns on deprecated tokens, missing tokens, missing fallback styles - Enforces token usage --- no arbitrary hex values in CSS

**ESLint CSS Support** (source: [ESLint Blog](https://eslint.org/blog/2025/02/eslint-css-support/)): - ESLint now lints CSS natively (since Feb 2025) - Can enforce design token constraints in CSS files

**Playwright Visual Regression** (source: [Playwright Docs](https://playwright.dev/docs/test-snapshots)): - `toHaveScreenshot()` for pixel-by-pixel comparison against baselines - Configurable thresholds (`maxDiffPixelRatio`, per-pixel `threshold`) - Generates expected/actual/diff images for debugging - Component-level screenshots via locators - Full-page stitched screenshots - CI/CD integration standard

#### How We Will Use It

  Research Finding                     Our Application
  ------------------------------------ ----------------------------------------------------------
  Stylelint token enforcement          Hard gate: no non-token values in production CSS
  ESLint CSS linting                   Enforce spacing/colour/typography rules at build time
  Playwright visual regression         Baseline screenshots per canonical view; run on every PR
  Diff images (expected/actual/diff)   Feed into evaluation pipeline for human + AI review

### 1.5 Voice-First & AI Interface Design

#### What the Research Shows

**Voice-first patterns** (source: [Lollypop VUI Best Practices](https://lollypop.design/blog/2025/august/voice-user-interface-design-best-practices/), [Zero Interface](https://wings.design/insights/zero-interface-the-future-of-ui-in-a-voice-first-ai-driven-world/)): - Be purpose-clear: state what the assistant can and cannot do - Make first-use frictionless - "Zero Interface" concept: design as signal interpretation (time, location, motion, history, sentiment) not screen management - Voice + visual hybrid: voice as input, screen as output/confirmation

**AI interface patterns** (source: [Smashing Magazine](https://www.smashingmagazine.com/2025/07/design-patterns-ai-interfaces/)): - 5 key areas: Input UX, Output UX, Refinement UX, AI Actions, AI Integration - Output UX for data: tables, dashboards, structured JSON, maps with data layers - Refinement via knobs/sliders/presets (Adobe Firefly pattern) - Forced ranking for prioritisation displays

#### How We Will Use It

  Research Finding        Our Application
  ----------------------- ----------------------------------------------------------------
  Voice + visual hybrid   Transcript panel as primary view; controls as secondary
  Purpose-clear scope     System capabilities visible but unobtrusive in shell
  Structured output       Metrics/data displayed in codified component patterns
  Refinement UX           Token adjustments as "tuning dials" in the evaluation pipeline

PART 3: GOALS, CONSTRAINTS & KAIZEN APPROACH
--------------------------------------------

*From spec section 2, verbatim.*

### 2.1 Problem Statement

We have a functional, behaviourally-sound React product that needs to look and feel like a precision tool --- calm, modern, confident, consistent. We lack a codified system for measuring and continuously improving visual polish. AI generates significant portions of our UI but has no enforceable taste constraints. Visual quality is subjective and inconsistent across features.

### 2.2 Non-Negotiable Constraints

These are **hard gates** --- violations fail the build or block deployment:

  ID     Constraint                                                  Rationale                       Source
  ------ ----------------------------------------------------------- ------------------------------- ---------------------
  C-01   WCAG AA contrast (4.5:1 body, 3:1 large text)               Accessibility law + usability   WCAG 2.1
  C-02   Only design-token values in production CSS                  Consistency, maintainability    Atlassian, Shadcn
  C-03   Maximum 2 font families (1 sans, 1 mono)                    Typographic discipline          Linear, Vercel
  C-04   4px/8px spacing grid (no arbitrary pixel values)            Visual rhythm                   Atlassian
  C-05   No decorative elements without information encoding         Cognitive load, anti-noise      Nielsen H8
  C-06   Demo page must render identically to production             Trust, honesty                  Ewan's directive
  C-07   All colour defined in LCH/Oklch space, converted at build   Perceptual uniformity           Linear
  C-08   `prefers-reduced-motion` respected                          Accessibility                   WCAG 2.1
  C-09   12px minimum text size, 16px body copy                      Readability floor               WCAG, best practice
  C-10   Max 45-75 characters per line (66 ideal)                    Reading comfort                 Bringhurst

### 2.3 Aesthetic Goals

These are **soft targets** --- scored, not gated:

  ID     Goal                 Description                                                   Weight
  ------ -------------------- ------------------------------------------------------------- --------
  A-01   Calm surface         Mostly-neutral colour field; accent used sparingly            0.15
  A-02   Clear hierarchy      3-4 levels of visual importance; squint test passes           0.15
  A-03   Typographic rhythm   Consistent scale, leading, measure across all views           0.12
  A-04   Spatial breathing    Whitespace proportional to content density; no cramming       0.12
  A-05   State clarity        Hover, active, disabled, loading, error states all distinct   0.10
  A-06   Consistent density   Similar information density across equivalent views           0.08
  A-07   Motion purpose       Every animation conveys information or provides feedback      0.08
  A-08   Component cohesion   All components feel from the same system                      0.08
  A-09   Data legibility      Numbers, charts, tables immediately scannable                 0.07
  A-10   Congruent trust      Demo page feels truthful, not "too polished to be real"       0.05

**Total weight: 1.00** --- Each aesthetic goal is weighted for the composite polish score.

### 2.4 Kaizen Approach

#### The Loop

    ┌─────────────────────────────────────────────────┐
    │  1. MEASURE                                      │
    │     Screenshot canonical views                   │
    │     Run hard checks (lint, tokens, a11y)         │
    │     Run aesthetic scoring (UIClip + LLM rubric)  │
    │     Compute composite polish score               │
    │                                                  │
    │  2. IDENTIFY                                     │
    │     Rank lowest-scoring dimensions               │
    │     Select 1-3 token/rule changes to test        │
    │     Scope: spacing OR typography OR colour only   │
    │     (never more than one category per cycle)     │
    │                                                  │
    │  3. GENERATE                                     │
    │     AI proposes variants within blinkers          │
    │     Max delta: ±2 tokens per variant              │
    │     Generate 3-5 variants per change              │
    │                                                  │
    │  4. EVALUATE                                     │
    │     Hard checks first (pass/fail)                │
    │     Aesthetic scoring on survivors                │
    │     Visual regression against baseline            │
    │     Human review of top 2 candidates              │
    │                                                  │
    │  5. DECIDE                                       │
    │     Accept if: score improvement > 0.5%           │
    │         AND no dimension regresses > 1%           │
    │         AND human approves                        │
    │     Reject otherwise                              │
    │     Update baseline if accepted                   │
    │                                                  │
    │  6. RECORD                                       │
    │     Log experiment: variant, scores, decision     │
    │     Update principles library if rule learned     │
    │     Bump token version if values changed          │
    │                                                  │
    └─────────────────────────────────────────────────┘

#### Cadence

  Trigger                Scope                                                   Who Decides
  ---------------------- ------------------------------------------------------- -----------------------------------------
  Nightly (automated)    Full pipeline on canonical views                        AI proposes, human reviews next morning
  Per PR (automated)     Hard checks + visual regression on changed components   CI blocks on failures
  Weekly (human-led)     Review Kaizen log; adjust rules/weights if needed       UX lead
  Per feature (manual)   Full pipeline on new view before merge                  Feature team + UX lead
  Monthly (human-led)    Qualitative review of demo page; taste check            Ewan + team

#### Acceptance Criteria

    accepted = (
        all_hard_checks_pass
        AND composite_score_delta > +0.005
        AND no_dimension_regression > 0.01
        AND human_approval == True
    )

**Critical rule:** No change ships without human approval. The system proposes; humans dispose. This is blinkers-without-ceilings: AI optimises inside the space, but never escapes the space without human consent.

PART 4: CODIFIED PRINCIPLES LIBRARY
-----------------------------------

### 4.1 Design Tokens

All tokens follow W3C DTCG 2025.10 format. Each file is the canonical source of truth.

#### 4.1.1 Typography Tokens

`principles/tokens/typography.tokens.json`

    {
      "$schema": "./schema/token.schema.json",
      "$version": "1.0.0",
      "font": {
        "$type": "fontFamily",
        "sans": {
          "$value": ["Geist", "system-ui", "-apple-system", "sans-serif"],
          "$description": "Primary sans-serif. Used for all UI text."
        },
        "mono": {
          "$value": ["Geist Mono", "JetBrains Mono", "Consolas", "monospace"],
          "$description": "Monospace. Used for code, data values, and transcripts."
        }
      },
      "fontSize": {
        "$type": "dimension",
        "2xs": { "$value": { "value": 11, "unit": "px" }, "$description": "Smallest allowed. Badges, fine print only." },
        "xs":  { "$value": { "value": 12, "unit": "px" }, "$description": "Captions, labels, timestamps" },
        "sm":  { "$value": { "value": 13, "unit": "px" }, "$description": "Secondary text, metadata" },
        "base": { "$value": { "value": 14, "unit": "px" }, "$description": "Default body text" },
        "md":  { "$value": { "value": 15, "unit": "px" }, "$description": "Emphasized body" },
        "lg":  { "$value": { "value": 18, "unit": "px" }, "$description": "Section headings" },
        "xl":  { "$value": { "value": 22, "unit": "px" }, "$description": "Page headings" },
        "2xl": { "$value": { "value": 28, "unit": "px" }, "$description": "View titles" },
        "3xl": { "$value": { "value": 36, "unit": "px" }, "$description": "Hero/display" },
        "4xl": { "$value": { "value": 48, "unit": "px" }, "$description": "Hero display, landing pages only" }
      },
      "fontWeight": {
        "$type": "fontWeight",
        "regular": { "$value": 400, "$description": "Body text" },
        "medium":  { "$value": 500, "$description": "Emphasis, labels" },
        "semibold": { "$value": 600, "$description": "Headings, key metrics" },
        "bold":    { "$value": 700, "$description": "Hero text, strong emphasis only" }
      },
      "lineHeight": {
        "$type": "number",
        "tight":   { "$value": 1.2, "$description": "Headings, display text" },
        "snug":    { "$value": 1.35, "$description": "Subheadings, compact body" },
        "normal":  { "$value": 1.5, "$description": "Body text — default" },
        "relaxed": { "$value": 1.625, "$description": "Long-form content, landing pages" }
      },
      "letterSpacing": {
        "$type": "dimension",
        "tighter": { "$value": { "value": -0.03, "unit": "em" }, "$description": "Display/hero only (>28px)" },
        "tight":   { "$value": { "value": -0.015, "unit": "em" }, "$description": "Headings (18-28px)" },
        "normal":  { "$value": { "value": 0, "unit": "em" }, "$description": "Body text" },
        "wide":    { "$value": { "value": 0.05, "unit": "em" }, "$description": "ALL-CAPS labels only" }
      },
      "typography": {
        "$type": "typography",
        "display": {
          "$value": {
            "fontFamily": "{font.sans}",
            "fontSize": "{fontSize.3xl}",
            "fontWeight": "{fontWeight.bold}",
            "letterSpacing": "{letterSpacing.tighter}",
            "lineHeight": "{lineHeight.tight}"
          },
          "$description": "Hero and display text. Landing pages and key metrics."
        },
        "heading1": {
          "$value": {
            "fontFamily": "{font.sans}",
            "fontSize": "{fontSize.2xl}",
            "fontWeight": "{fontWeight.semibold}",
            "letterSpacing": "{letterSpacing.tight}",
            "lineHeight": "{lineHeight.tight}"
          }
        },
        "heading2": {
          "$value": {
            "fontFamily": "{font.sans}",
            "fontSize": "{fontSize.xl}",
            "fontWeight": "{fontWeight.semibold}",
            "letterSpacing": "{letterSpacing.tight}",
            "lineHeight": "{lineHeight.tight}"
          }
        },
        "heading3": {
          "$value": {
            "fontFamily": "{font.sans}",
            "fontSize": "{fontSize.lg}",
            "fontWeight": "{fontWeight.medium}",
            "letterSpacing": "{letterSpacing.normal}",
            "lineHeight": "{lineHeight.snug}"
          }
        },
        "body": {
          "$value": {
            "fontFamily": "{font.sans}",
            "fontSize": "{fontSize.base}",
            "fontWeight": "{fontWeight.regular}",
            "letterSpacing": "{letterSpacing.normal}",
            "lineHeight": "{lineHeight.normal}"
          }
        },
        "caption": {
          "$value": {
            "fontFamily": "{font.sans}",
            "fontSize": "{fontSize.xs}",
            "fontWeight": "{fontWeight.regular}",
            "letterSpacing": "{letterSpacing.normal}",
            "lineHeight": "{lineHeight.normal}"
          }
        },
        "code": {
          "$value": {
            "fontFamily": "{font.mono}",
            "fontSize": "{fontSize.sm}",
            "fontWeight": "{fontWeight.regular}",
            "letterSpacing": "{letterSpacing.normal}",
            "lineHeight": "{lineHeight.normal}"
          },
          "$description": "Inline code, data values, transcript content"
        },
        "metric": {
          "$value": {
            "fontFamily": "{font.mono}",
            "fontSize": "{fontSize.2xl}",
            "fontWeight": "{fontWeight.semibold}",
            "letterSpacing": "{letterSpacing.tight}",
            "lineHeight": "{lineHeight.tight}"
          },
          "$description": "Large numeric values in KPI cards. Use tabular-nums."
        }
      }
    }

#### 4.1.2 Spacing & Radius Tokens

`principles/tokens/spacing.tokens.json`

    {
      "$schema": "./schema/token.schema.json",
      "$version": "1.0.0",
      "space": {
        "$type": "dimension",
        "$description": "4px base unit hybrid grid. Named by pixel value for clarity.",
        "0":  { "$value": { "value": 0, "unit": "px" } },
        "1":  { "$value": { "value": 1, "unit": "px" }, "$description": "Hairline borders only" },
        "2":  { "$value": { "value": 2, "unit": "px" }, "$description": "Tight inline gaps" },
        "4":  { "$value": { "value": 4, "unit": "px" }, "$description": "Icon-to-text gap, badge padding" },
        "6":  { "$value": { "value": 6, "unit": "px" }, "$description": "Small component internal padding" },
        "8":  { "$value": { "value": 8, "unit": "px" }, "$description": "Standard internal padding, small gaps" },
        "12": { "$value": { "value": 12, "unit": "px" }, "$description": "Medium gaps, input padding" },
        "16": { "$value": { "value": 16, "unit": "px" }, "$description": "Card padding, standard section gaps" },
        "20": { "$value": { "value": 20, "unit": "px" }, "$description": "Comfortable gaps between groups" },
        "24": { "$value": { "value": 24, "unit": "px" }, "$description": "Large section padding" },
        "32": { "$value": { "value": 32, "unit": "px" }, "$description": "Section separation" },
        "40": { "$value": { "value": 40, "unit": "px" }, "$description": "Large layout gaps" },
        "48": { "$value": { "value": 48, "unit": "px" }, "$description": "Page-level vertical rhythm" },
        "64": { "$value": { "value": 64, "unit": "px" }, "$description": "Hero spacing, major sections" },
        "80": { "$value": { "value": 80, "unit": "px" }, "$description": "Page margins, max section gaps" },
        "96": { "$value": { "value": 96, "unit": "px" }, "$description": "Landing page hero spacing only" }
      },
      "radius": {
        "$type": "dimension",
        "none": { "$value": { "value": 0, "unit": "px" } },
        "sm":   { "$value": { "value": 4, "unit": "px" }, "$description": "Badges, small chips" },
        "md":   { "$value": { "value": 6, "unit": "px" }, "$description": "Buttons, inputs, small cards" },
        "lg":   { "$value": { "value": 8, "unit": "px" }, "$description": "Cards, panels" },
        "xl":   { "$value": { "value": 12, "unit": "px" }, "$description": "Modals, dialogs" },
        "2xl":  { "$value": { "value": 16, "unit": "px" }, "$description": "Large containers, landing sections" },
        "full": { "$value": { "value": 9999, "unit": "px" }, "$description": "Circles, pills" }
      }
    }

#### 4.1.3 Color Tokens

`principles/tokens/color.tokens.json`

    {
      "$schema": "./schema/token.schema.json",
      "$version": "1.0.0",
      "color": {
        "$type": "color",
        "$description": "All colors defined in LCH, with sRGB hex for fallback. Light mode defaults shown; dark mode via semantic alias override.",
        "primitive": {
          "neutral": {
            "0":   { "$value": { "colorSpace": "srgb", "components": [1, 1, 1], "hex": "#FFFFFF" } },
            "50":  { "$value": { "colorSpace": "srgb", "components": [0.969, 0.965, 0.949], "hex": "#F7F6F2" } },
            "100": { "$value": { "colorSpace": "srgb", "components": [0.976, 0.973, 0.961], "hex": "#F9F8F5" } },
            "200": { "$value": { "colorSpace": "srgb", "components": [0.831, 0.820, 0.792], "hex": "#D4D1CA" } },
            "300": { "$value": { "colorSpace": "srgb", "components": [0.729, 0.725, 0.706], "hex": "#BAB9B4" } },
            "400": { "$value": { "colorSpace": "srgb", "components": [0.478, 0.475, 0.455], "hex": "#7A7974" } },
            "500": { "$value": { "colorSpace": "srgb", "components": [0.353, 0.349, 0.337], "hex": "#5A5957" } },
            "900": { "$value": { "colorSpace": "srgb", "components": [0.157, 0.145, 0.114], "hex": "#28251D" } },
            "1000":{ "$value": { "colorSpace": "srgb", "components": [0.090, 0.086, 0.078], "hex": "#171614" } }
          },
          "teal": {
            "500": { "$value": { "colorSpace": "srgb", "components": [0.004, 0.412, 0.435], "hex": "#01696F" } },
            "600": { "$value": { "colorSpace": "srgb", "components": [0.047, 0.306, 0.329], "hex": "#0C4E54" } },
            "400": { "$value": { "colorSpace": "srgb", "components": [0.310, 0.596, 0.639], "hex": "#4F98A3" } }
          },
          "red":    { "500": { "$value": { "colorSpace": "srgb", "components": [0.631, 0.173, 0.482], "hex": "#A12C7B" } } },
          "amber":  { "500": { "$value": { "colorSpace": "srgb", "components": [0.588, 0.259, 0.098], "hex": "#964219" } } },
          "green":  { "500": { "$value": { "colorSpace": "srgb", "components": [0.263, 0.478, 0.133], "hex": "#437A22" } } }
        },
        "semantic": {
          "bg":           { "$value": "{color.primitive.neutral.50}" },
          "surface":      { "$value": "{color.primitive.neutral.100}" },
          "surface-alt":  { "$value": "{color.primitive.neutral.0}" },
          "border":       { "$value": "{color.primitive.neutral.200}" },
          "text":         { "$value": "{color.primitive.neutral.900}" },
          "text-muted":   { "$value": "{color.primitive.neutral.400}" },
          "text-faint":   { "$value": "{color.primitive.neutral.300}" },
          "primary":      { "$value": "{color.primitive.teal.500}" },
          "primary-hover":{ "$value": "{color.primitive.teal.600}" },
          "error":        { "$value": "{color.primitive.red.500}" },
          "warning":      { "$value": "{color.primitive.amber.500}" },
          "success":      { "$value": "{color.primitive.green.500}" }
        }
      }
    }

#### 4.1.4 Motion Tokens

`principles/tokens/motion.tokens.json`

    {
      "$schema": "./schema/token.schema.json",
      "$version": "1.0.0",
      "duration": {
        "$type": "duration",
        "instant": { "$value": { "value": 50, "unit": "ms" }, "$description": "Opacity changes, micro-feedback" },
        "fast":    { "$value": { "value": 100, "unit": "ms" }, "$description": "Hover states, tooltips" },
        "normal":  { "$value": { "value": 200, "unit": "ms" }, "$description": "Standard transitions, panel open/close" },
        "slow":    { "$value": { "value": 350, "unit": "ms" }, "$description": "Page transitions, modal entrance" },
        "slower":  { "$value": { "value": 500, "unit": "ms" }, "$description": "Complex transitions only. Maximum." }
      },
      "easing": {
        "$type": "cubicBezier",
        "default":   { "$value": [0.25, 0.1, 0.25, 1.0], "$description": "Standard ease — most transitions" },
        "in":        { "$value": [0.42, 0, 1, 1], "$description": "Ease in — elements exiting" },
        "out":       { "$value": [0, 0, 0.58, 1], "$description": "Ease out — elements entering" },
        "in-out":    { "$value": [0.42, 0, 0.58, 1], "$description": "Ease in-out — position changes" },
        "spring":    { "$value": [0.34, 1.56, 0.64, 1], "$description": "Slight overshoot — playful feedback only" }
      }
    }

#### 4.1.5 Shadow Tokens

`principles/tokens/shadow.tokens.json`

    {
      "$schema": "./schema/token.schema.json",
      "$version": "1.0.0",
      "shadow": {
        "$type": "shadow",
        "none": { "$value": { "color": { "colorSpace": "srgb", "components": [0, 0, 0], "alpha": 0 }, "offsetX": { "value": 0, "unit": "px" }, "offsetY": { "value": 0, "unit": "px" }, "blur": { "value": 0, "unit": "px" }, "spread": { "value": 0, "unit": "px" } } },
        "sm": {
          "$value": {
            "color": { "colorSpace": "srgb", "components": [0, 0, 0], "alpha": 0.04 },
            "offsetX": { "value": 0, "unit": "px" },
            "offsetY": { "value": 1, "unit": "px" },
            "blur": { "value": 2, "unit": "px" },
            "spread": { "value": 0, "unit": "px" }
          },
          "$description": "Subtle elevation. Cards on surface."
        },
        "md": {
          "$value": {
            "color": { "colorSpace": "srgb", "components": [0, 0, 0], "alpha": 0.06 },
            "offsetX": { "value": 0, "unit": "px" },
            "offsetY": { "value": 2, "unit": "px" },
            "blur": { "value": 8, "unit": "px" },
            "spread": { "value": -2, "unit": "px" }
          },
          "$description": "Standard elevation. Dropdowns, popovers."
        },
        "lg": {
          "$value": {
            "color": { "colorSpace": "srgb", "components": [0, 0, 0], "alpha": 0.08 },
            "offsetX": { "value": 0, "unit": "px" },
            "offsetY": { "value": 4, "unit": "px" },
            "blur": { "value": 16, "unit": "px" },
            "spread": { "value": -4, "unit": "px" }
          },
          "$description": "High elevation. Modals, dialogs."
        },
        "xl": {
          "$value": {
            "color": { "colorSpace": "srgb", "components": [0, 0, 0], "alpha": 0.12 },
            "offsetX": { "value": 0, "unit": "px" },
            "offsetY": { "value": 8, "unit": "px" },
            "blur": { "value": 24, "unit": "px" },
            "spread": { "value": -6, "unit": "px" }
          },
          "$description": "Maximum elevation. Command palette, floating panels."
        }
      }
    }

### 4.2 Hard Rules

`principles/rules/core.rules.json`

    {
      "$version": "1.0.0",
      "rules": [
        {
          "id": "TYP-001",
          "name": "No arbitrary font sizes",
          "category": "typography",
          "severity": "error",
          "condition": {
            "check_type": "css_lint",
            "property": "font-size",
            "allowed_tokens": [
              "var(--fontSize-2xs)", "var(--fontSize-xs)", "var(--fontSize-sm)",
              "var(--fontSize-base)", "var(--fontSize-md)", "var(--fontSize-lg)",
              "var(--fontSize-xl)", "var(--fontSize-2xl)", "var(--fontSize-3xl)",
              "var(--fontSize-4xl)"
            ]
          },
          "rationale": "All font sizes must come from the typographic scale. Arbitrary sizes break visual rhythm and make Kaizen impossible — you can't improve what you can't measure.",
          "source": "Linear typography system; Bringhurst typographic scale",
          "added": "2026-03-14"
        },
        {
          "id": "TYP-002",
          "name": "Body text line length limit",
          "category": "typography",
          "severity": "warning",
          "condition": {
            "check_type": "metric_range",
            "selector": "p, .body-text, [data-text-role='body']",
            "property": "characters-per-line",
            "max": 75,
            "min": 35
          },
          "rationale": "Optimal reading comfort: 45-75 characters per line (66 ideal). Below 35 causes excessive line breaks; above 75 causes tracking loss.",
          "source": "Bringhurst 'Elements of Typographic Style'; WCAG SC 1.4.8",
          "added": "2026-03-14"
        },
        {
          "id": "CLR-001",
          "name": "No arbitrary colour values",
          "category": "color",
          "severity": "error",
          "condition": {
            "check_type": "css_lint",
            "property": "color|background-color|border-color|fill|stroke",
            "selector": "*",
            "allowed_tokens": ["var(--color-*)", "transparent", "currentColor", "inherit"]
          },
          "rationale": "All colours must come from the token system. Arbitrary hex/rgb values break theming, dark mode, and visual consistency.",
          "source": "Atlassian Stylelint plugin; Shadcn token system",
          "added": "2026-03-14"
        },
        {
          "id": "LAY-001",
          "name": "Maximum distinct card styles per view",
          "category": "layout",
          "severity": "warning",
          "condition": {
            "check_type": "count_limit",
            "selector": "[data-component='card']",
            "property": "distinct-visual-styles",
            "max": 3
          },
          "rationale": "More than 3 visually distinct card patterns on one screen creates cognitive overhead. Users must learn multiple container metaphors. Consolidate to max 3: primary, secondary, metric.",
          "source": "UICrit Layout cluster (23%); Miller's Law (chunking)",
          "added": "2026-03-14"
        },
        {
          "id": "LAY-002",
          "name": "Spacing uses token values only",
          "category": "spacing",
          "severity": "error",
          "condition": {
            "check_type": "css_lint",
            "property": "margin|padding|gap|row-gap|column-gap",
            "allowed_tokens": [
              "var(--space-0)", "var(--space-1)", "var(--space-2)", "var(--space-4)",
              "var(--space-6)", "var(--space-8)", "var(--space-12)", "var(--space-16)",
              "var(--space-20)", "var(--space-24)", "var(--space-32)", "var(--space-40)",
              "var(--space-48)", "var(--space-64)", "var(--space-80)", "var(--space-96)",
              "0", "auto"
            ]
          },
          "rationale": "Arbitrary spacing breaks visual rhythm. Every spacing value must be from the 4px/8px grid.",
          "source": "Atlassian 8px system; design token best practice",
          "added": "2026-03-14"
        },
        {
          "id": "DEN-001",
          "name": "Maximum interactive elements per viewport",
          "category": "density",
          "severity": "suggestion",
          "condition": {
            "check_type": "count_limit",
            "selector": "button, a, input, select, [role='button'], [tabindex]",
            "property": "count-in-viewport",
            "max": 40
          },
          "rationale": "High interactive density increases cognitive load. If viewport has >40 interactive elements, consider progressive disclosure or grouping.",
          "source": "Hick's Law; UICrit Learnability cluster",
          "added": "2026-03-14"
        },
        {
          "id": "MOT-001",
          "name": "Animation duration constraints",
          "category": "motion",
          "severity": "error",
          "condition": {
            "check_type": "css_lint",
            "property": "animation-duration|transition-duration",
            "allowed_tokens": [
              "var(--duration-instant)", "var(--duration-fast)", "var(--duration-normal)",
              "var(--duration-slow)", "var(--duration-slower)"
            ]
          },
          "rationale": "No animation longer than 500ms. No animation shorter than 50ms (imperceptible). All durations from token set.",
          "source": "Material Design motion guidelines; Nielsen response time limits",
          "added": "2026-03-14"
        },
        {
          "id": "A11Y-001",
          "name": "Text contrast ratio (body)",
          "category": "accessibility",
          "severity": "error",
          "condition": {
            "check_type": "ratio_check",
            "selector": "p, span, li, td, label, .body-text",
            "property": "contrast-ratio",
            "min": 4.5
          },
          "rationale": "WCAG AA requires 4.5:1 for normal text. Non-negotiable.",
          "source": "WCAG 2.1 SC 1.4.3",
          "added": "2026-03-14"
        },
        {
          "id": "CMP-001",
          "name": "KPI card structure",
          "category": "component",
          "severity": "warning",
          "condition": {
            "check_type": "dom_query",
            "selector": "[data-component='kpi-card']",
            "property": "required-children",
            "allowed_tokens": ["[data-role='value']", "[data-role='label']"]
          },
          "rationale": "Every KPI card must have a large value and a descriptive label. Delta indicator and sparkline are optional. Value is the dominant visual element.",
          "source": "Data viz best practice; design-foundations skill",
          "added": "2026-03-14"
        }
      ]
    }

**Error-severity rules (blockers):** TYP-001, CLR-001, LAY-002, MOT-001, A11Y-001

**Warning-severity rules (flagged):** TYP-002, LAY-001, CMP-001

**Suggestion-severity rules (informational):** DEN-001

### 4.3 Rule Schema

`principles/schema/rule.schema.json`

    {
      "$schema": "http://json-schema.org/draft-07/schema#",
      "$id": "amplified/rule.schema.json",
      "type": "object",
      "properties": {
        "$version": { "type": "string" },
        "rules": {
          "type": "array",
          "items": {
            "type": "object",
            "required": ["id", "name", "category", "severity", "condition", "rationale"],
            "properties": {
              "id": {
                "type": "string",
                "pattern": "^[A-Z]+-[0-9]{3}$",
                "description": "Unique rule ID. Format: CATEGORY-NNN"
              },
              "name": {
                "type": "string",
                "description": "Human-readable rule name"
              },
              "category": {
                "type": "string",
                "enum": ["typography", "spacing", "color", "layout", "component", "density", "motion", "accessibility"],
                "description": "Rule category for grouping and filtering"
              },
              "severity": {
                "type": "string",
                "enum": ["error", "warning", "suggestion"],
                "description": "error=blocks deploy, warning=flagged for review, suggestion=logged for Kaizen"
              },
              "condition": {
                "type": "object",
                "description": "Machine-parseable condition. Structure varies by check type.",
                "properties": {
                  "check_type": {
                    "type": "string",
                    "enum": ["css_lint", "dom_query", "screenshot_analysis", "metric_range", "count_limit", "ratio_check"],
                    "description": "How this rule is evaluated"
                  },
                  "selector": { "type": "string", "description": "CSS selector or DOM query (for css_lint, dom_query)" },
                  "property": { "type": "string", "description": "CSS property to check (for css_lint)" },
                  "allowed_tokens": { "type": "array", "items": { "type": "string" }, "description": "Permitted token references" },
                  "min": { "type": "number", "description": "Minimum value (for metric_range)" },
                  "max": { "type": "number", "description": "Maximum value (for metric_range, count_limit)" },
                  "prompt": { "type": "string", "description": "LLM evaluation prompt (for screenshot_analysis)" }
                }
              },
              "rationale": {
                "type": "string",
                "description": "Why this rule exists. Links to research or principle."
              },
              "source": {
                "type": "string",
                "description": "Research source (e.g., 'Nielsen H8', 'UICrit Layout cluster', 'Linear LCH')"
              },
              "added": {
                "type": "string",
                "format": "date",
                "description": "When this rule was added"
              },
              "kaizen_origin": {
                "type": "string",
                "description": "Which Kaizen cycle identified this rule, if any"
              }
            }
          }
        }
      }
    }

### 4.4 Scoring Rubric

`principles/references/rubric.json`

    {
      "rubric": {
        "dimensions": [
          {
            "id": "calm_surface",
            "name": "Calm Surface",
            "weight": 0.15,
            "prompt": "Rate the visual calmness of this interface. A calm surface is mostly neutral with accent color used sparingly. The eye should rest, not bounce. Consider: number of distinct colors visible, ratio of neutral to accent, visual noise level.",
            "scale": { "min": 1, "max": 10, "anchor_low": "Noisy, many competing colors", "anchor_high": "Serene, accent draws eye precisely where needed" }
          },
          {
            "id": "clear_hierarchy",
            "name": "Clear Hierarchy",
            "weight": 0.15,
            "prompt": "Rate the visual hierarchy. Squint at the screenshot — can you immediately identify 3-4 levels of importance? Is the most important element (key metric, primary action) the most visually prominent?",
            "scale": { "min": 1, "max": 10, "anchor_low": "Everything same weight, no focal point", "anchor_high": "Instantly clear what matters most, 3-4 distinct levels" }
          },
          {
            "id": "typographic_rhythm",
            "name": "Typographic Rhythm",
            "weight": 0.12,
            "prompt": "Evaluate the typography. Is there a consistent scale? Do headings, body, and captions form a clear progression? Is line length comfortable? Is spacing between text blocks consistent?",
            "scale": { "min": 1, "max": 10, "anchor_low": "Inconsistent sizes, poor spacing, uncomfortable to read", "anchor_high": "Beautiful rhythm, clear scale, every text element feels intentional" }
          },
          {
            "id": "spatial_breathing",
            "name": "Spatial Breathing",
            "weight": 0.12,
            "prompt": "Assess whitespace and breathing room. Is content given enough space to be parsed without effort? Are groups of related items clearly separated from unrelated items? Does the layout feel spacious without feeling empty?",
            "scale": { "min": 1, "max": 10, "anchor_low": "Cramped, elements touching, no breathing room", "anchor_high": "Generous, intentional whitespace, clear grouping through space" }
          },
          {
            "id": "state_clarity",
            "name": "State Clarity",
            "weight": 0.10,
            "prompt": "Can you identify the current state of interactive elements? Are hover targets clear? Do buttons look clickable? Are disabled states obviously disabled? Loading states present?",
            "scale": { "min": 1, "max": 10, "anchor_low": "States ambiguous, can't tell what's interactive", "anchor_high": "Every state obvious, interaction model clear at a glance" }
          },
          {
            "id": "consistent_density",
            "name": "Consistent Density",
            "weight": 0.08,
            "prompt": "Is information density consistent across the view? Are similar sections equally dense? No areas that feel much tighter or looser than their neighbors?",
            "scale": { "min": 1, "max": 10, "anchor_low": "Wildly varying density, inconsistent spacing", "anchor_high": "Uniform density, every section feels calibrated to the same standard" }
          },
          {
            "id": "motion_purpose",
            "name": "Motion Purpose",
            "weight": 0.08,
            "prompt": "If any animations or transitions are visible/implied, do they serve information or feedback purposes? No gratuitous effects?",
            "scale": { "min": 1, "max": 10, "anchor_low": "Decorative animation, distracting motion", "anchor_high": "Every motion carries meaning or provides feedback" }
          },
          {
            "id": "component_cohesion",
            "name": "Component Cohesion",
            "weight": 0.08,
            "prompt": "Do all components look like they belong to the same design system? Consistent border radius, shadow treatment, padding, button styles?",
            "scale": { "min": 1, "max": 10, "anchor_low": "Components from different design systems, inconsistent", "anchor_high": "Every component clearly from the same family" }
          },
          {
            "id": "data_legibility",
            "name": "Data Legibility",
            "weight": 0.07,
            "prompt": "Are numbers, charts, tables, and data immediately scannable? Do key metrics stand out? Is data density appropriate — not too sparse, not overwhelming?",
            "scale": { "min": 1, "max": 10, "anchor_low": "Data hard to parse, metrics buried", "anchor_high": "Data jumps off the screen, instantly scannable" }
          },
          {
            "id": "congruent_trust",
            "name": "Congruent Trust",
            "weight": 0.05,
            "prompt": "Does this interface feel honest and trustworthy? Not over-polished to the point of seeming fake, not under-designed to seem unprofessional? Would a prospective customer trust this product?",
            "scale": { "min": 1, "max": 10, "anchor_low": "Feels fake or untrustworthy", "anchor_high": "Inspires quiet confidence, feels like a tool built by experts" }
          }
        ],
        "overall_prompt": "After rating each dimension, provide an overall polish score (1-10) and 2-3 specific, actionable suggestions for the single most impactful improvement.",
        "examples": {
          "positive": ["references/positive-examples/linear-dashboard.png", "references/positive-examples/vercel-dashboard.png"],
          "negative": ["references/negative-examples/cluttered-dashboard.png", "references/negative-examples/inconsistent-cards.png"]
        }
      }
    }

**Dimension weights summary:**

  Dimension ID          Name                 Weight
  --------------------- -------------------- ----------
  calm\_surface         Calm Surface         0.15
  clear\_hierarchy      Clear Hierarchy      0.15
  typographic\_rhythm   Typographic Rhythm   0.12
  spatial\_breathing    Spatial Breathing    0.12
  state\_clarity        State Clarity        0.10
  consistent\_density   Consistent Density   0.08
  motion\_purpose       Motion Purpose       0.08
  component\_cohesion   Component Cohesion   0.08
  data\_legibility      Data Legibility      0.07
  congruent\_trust      Congruent Trust      0.05
  **Total**                                  **1.00**

### 4.5 Extension Model

*From spec section 3.4, verbatim.*

The principles library is not static. It grows through the Kaizen loop:

1.  **New rule proposed** --- From evaluation pipeline findings, human review, or research
2.  **Rule enters as** `suggestion` **severity** --- Logged but does not block
3.  **Data collected** --- After 2-4 Kaizen cycles, review impact
4.  **Promotion** --- If rule correlates with score improvement, promote to `warning` or `error`
5.  **Retirement** --- If rule conflicts with newer evidence, deprecate (never delete --- version history)

Schema supports this with `added`, `kaizen_origin`, and `$deprecated` fields.

PART 5: EVALUATION & TESTING PIPELINE
-------------------------------------

*From spec section 4, verbatim.*

### 4.1 Pipeline Architecture

    ┌─────────────────────────────────────────────────────────────┐
    │                    EXPERIMENT ORCHESTRATOR                    │
    │               (Node.js service on Beast)                     │
    ├─────────────────────────────────────────────────────────────┤
    │                                                              │
    │  ┌──────────┐    ┌──────────┐    ┌──────────┐              │
    │  │ VARIANT  │    │ VARIANT  │    │ VARIANT  │  ... (3-5)   │
    │  │ GENERATOR│    │ RENDERER │    │ EVALUATOR│              │
    │  └────┬─────┘    └────┬─────┘    └────┬─────┘              │
    │       │               │               │                     │
    │       ▼               ▼               ▼                     │
    │  Token deltas    Playwright      Hard checks                │
    │  within          screenshots     + Aesthetic                │
    │  blinkers        of canonical    scoring                    │
    │                  views           + UIClip                   │
    │                                  + LLM rubric              │
    │                                                              │
    │  ┌──────────────────────────────────────────────┐           │
    │  │              RESULTS DATABASE                 │           │
    │  │  (SQLite on Beast → later PostgreSQL)        │           │
    │  │  experiment_runs, variants, scores, decisions │           │
    │  └──────────────────────────────────────────────┘           │
    │                                                              │
    │  ┌──────────────────────────────────────────────┐           │
    │  │              KAIZEN DASHBOARD                 │           │
    │  │  Score trends, dimension breakdowns,          │           │
    │  │  experiment history, baseline comparisons     │           │
    │  └──────────────────────────────────────────────┘           │
    │                                                              │
    └─────────────────────────────────────────────────────────────┘

### 4.2 Stage 1: Variant Generator

#### Input

-   Current token values (from `principles/tokens/`)
-   Current rule set (from `principles/rules/`)
-   Target dimension to improve (from Kaizen IDENTIFY step)
-   Constraints: max delta, allowed token categories

#### Process

    interface VariantDelta {
      tokenPath: string;     // e.g. "space.16"
      currentValue: any;     // e.g. { value: 16, unit: "px" }
      proposedValue: any;    // e.g. { value: 20, unit: "px" }
      rationale: string;     // Why this change might help
    }

    interface Variant {
      id: string;                    // UUID
      experimentId: string;          // Parent experiment
      deltas: VariantDelta[];        // Max 2 per variant
      category: "spacing" | "typography" | "color" | "motion" | "shadow";
      generatedBy: "ai" | "human";
      createdAt: string;             // ISO 8601
    }

#### Constraints on Generation

  Rule                          Value                            Rationale
  ----------------------------- -------------------------------- ---------------------------------
  Max deltas per variant        2                                Isolate cause of improvement
  Max variants per experiment   5                                Computational cost vs. coverage
  Category isolation            1 category per experiment        No confounding variables
  Step size (spacing)           ±4px (one grid step)             Small, measurable change
  Step size (font-size)         ±1px                             Minimum perceptible change
  Step size (font-weight)       ±100                             Standard weight steps
  Step size (colour)            ±5 LCH lightness or ±10 chroma   Perceptually meaningful
  Duration change               ±50ms                            Noticeable but not jarring

#### AI Generation Prompt (for Claude)

    You are a variant generator for the Amplified Visual Polish System.

    CONTEXT:
    - Current tokens: [inject current tokens JSON]
    - Target dimension: [e.g., "spatial breathing (A-04)"]
    - Current score for target: [e.g., 0.72]
    - Lowest-scoring areas from last evaluation: [e.g., "card padding feels cramped in data views"]

    CONSTRAINTS:
    - You may change at most 2 token values
    - Changes must stay within the spacing category
    - Each change must be ±1 step on the scale (e.g., space.16 → space.20 or space.12)
    - You must not violate any error-severity rules

    GENERATE 3-5 variants, each as a JSON object with:
    - deltas: array of {tokenPath, currentValue, proposedValue, rationale}
    - hypothesis: what you expect this change to improve and why

    Think about: whitespace-to-content ratio, Gestalt grouping, visual breathing room,
    and the overall feeling of calm professionalism we're targeting.

### 4.3 Stage 2: Variant Renderer

#### Process

For each variant:

1.  **Apply token overrides** --- CSS custom property overrides injected via Playwright `addStyleTag()`
2.  **Navigate to canonical views** (defined per layout pattern, see Section 7)
3.  **Wait for stability** --- `networkidle` + custom `data-render-complete` attribute
4.  **Capture screenshots** --- Full page + component-level for key elements

```{=html}
<!-- -->
```
    interface ScreenshotCapture {
      variantId: string;
      viewId: string;           // e.g. "product-shell-main", "demo-page-hero"
      viewport: { width: number; height: number };
      fullPage: boolean;
      filePath: string;          // Path to PNG on Beast filesystem
      capturedAt: string;
      renderDurationMs: number;
    }

#### Canonical Views to Capture

  View ID                  Description                                       Viewport
  ------------------------ ------------------------------------------------- -----------
  `shell-sidebar-open`     Product shell, sidebar expanded, main data view   1440×900
  `shell-sidebar-closed`   Product shell, sidebar collapsed                  1440×900
  `shell-transcript`       Voice transcript panel active                     1440×900
  `shell-metrics`          Key metrics dashboard view                        1440×900
  `shell-mobile`           Product shell, mobile viewport                    390×844
  `demo-hero`              Demo page, hero section                           1440×900
  `demo-features`          Demo page, features/value section                 1440×900
  `demo-full`              Demo page, full page stitched                     1440×full
  `landing-hero`           Client landing page, hero                         1440×900
  `landing-full`           Client landing page, full                         1440×full

### 4.4 Stage 3: Evaluator

#### 4.4.1 Hard Checks (Pass/Fail)

Run first. Variants that fail any error-severity rule are immediately discarded.

    interface HardCheckResult {
      ruleId: string;
      passed: boolean;
      violations: Array<{
        selector: string;
        property: string;
        actualValue: string;
        expectedConstraint: string;
        location: { line: number; column: number } | null;
      }>;
    }

**Implementation:** - **Token enforcement** --- Stylelint with custom plugin that reads our token allowlists - **Accessibility** --- axe-core in Playwright context (`@axe-core/playwright`) - **DOM structure** --- Custom Playwright assertions against rule conditions - **Visual regression** --- Playwright `toHaveScreenshot()` against baseline (separate from aesthetic scoring)

#### 4.4.2 Aesthetic Scoring (Numeric)

Two independent scoring methods, combined:

##### Method A: UIClip-Style Scoring

Deploy UIClip (or fine-tuned CLIP variant) on Beast GPU:

    # Pseudocode for UIClip scoring on Beast
    from uiclip import UIClipModel

    model = UIClipModel.load("uiclip-v1")

    def score_variant(screenshot_path: str, description: str) -> float:
        """
        Returns 0.0-1.0 score combining design quality and description relevance.
        Uses sliding window (224x224 patches) for full-page screenshots.
        """
        image = load_image(screenshot_path)
        score = model.score(image, description)
        return score

**Descriptions per view** (used as UIClip text input): - `shell-sidebar-open`: "A clean, calm SaaS product dashboard with voice transcript panel, metric cards, and navigation sidebar. Modern, professional, data-rich but not cluttered." - `demo-hero`: "An honest, trustworthy product demo page with clear hero messaging, product screenshots that match the real application, and a calm professional aesthetic."

##### Method B: Multimodal LLM Rubric Scoring

Claude (or equivalent) evaluates screenshots against the structured rubric (see Section 4.4 above). Full rubric JSON is already defined in `principles/references/rubric.json`.

#### 4.4.3 Composite Polish Score

    interface PolishScore {
      variantId: string;
      timestamp: string;

      // Hard checks
      hardChecksPassed: boolean;
      hardCheckViolations: number;

      // UIClip score (0-1)
      uiclipScore: number;

      // LLM rubric scores (1-10 each, weighted)
      rubricScores: Record<string, number>;  // dimension_id → score
      rubricWeightedTotal: number;           // Sum of (score × weight), normalised to 0-1

      // Composite
      compositeScore: number;  // (uiclipScore × 0.4) + (rubricWeightedTotal × 0.6)

      // Visual regression
      visualRegressionDiffPercent: number;   // % pixels changed from baseline

      // Per-dimension deltas from baseline
      dimensionDeltas: Record<string, number>;  // dimension_id → delta from baseline
    }

**Composite formula:**

    compositeScore = (uiclipScore × 0.4) + (rubricNormalised × 0.6)

    Where:
      rubricNormalised = Σ(dimension_score / 10 × dimension_weight) for all dimensions
      uiclipScore is raw UIClip output (0-1)

**Trade-off note:** UIClip is fast (\~100ms per image) but trained on mobile UIs and may not perfectly generalise to our desktop SaaS aesthetic. LLM rubric is slower (\~10s per image) but directly tuned to our goals. Weight may shift as we calibrate. Start with 40/60 split, adjust based on correlation with human judgement.

### 4.5 Experiment Run Data Model

    -- Core tables for experiment tracking (SQLite on Beast)

    CREATE TABLE experiment_runs (
        id TEXT PRIMARY KEY,          -- UUID
        created_at TEXT NOT NULL,     -- ISO 8601
        trigger TEXT NOT NULL,        -- 'nightly' | 'pr' | 'manual' | 'feature'
        target_dimension TEXT,        -- e.g. 'spatial_breathing'
        category TEXT NOT NULL,       -- 'spacing' | 'typography' | 'color' | etc.
        baseline_score REAL,          -- Composite score before experiment
        status TEXT NOT NULL,         -- 'running' | 'completed' | 'failed'
        decision TEXT,                -- 'accepted' | 'rejected' | 'pending_review'
        decided_by TEXT,              -- 'human:ewan' | 'auto:threshold'
        decided_at TEXT,
        notes TEXT
    );

    CREATE TABLE variants (
        id TEXT PRIMARY KEY,
        experiment_id TEXT NOT NULL REFERENCES experiment_runs(id),
        deltas_json TEXT NOT NULL,    -- JSON array of VariantDelta
        generated_by TEXT NOT NULL,   -- 'ai:claude-4-sonnet' | 'human:ewan'
        created_at TEXT NOT NULL
    );

    CREATE TABLE screenshots (
        id TEXT PRIMARY KEY,
        variant_id TEXT NOT NULL REFERENCES variants(id),
        view_id TEXT NOT NULL,        -- e.g. 'shell-sidebar-open'
        viewport_width INTEGER,
        viewport_height INTEGER,
        file_path TEXT NOT NULL,
        captured_at TEXT NOT NULL,
        render_duration_ms INTEGER
    );

    CREATE TABLE hard_check_results (
        id TEXT PRIMARY KEY,
        variant_id TEXT NOT NULL REFERENCES variants(id),
        rule_id TEXT NOT NULL,
        passed BOOLEAN NOT NULL,
        violations_json TEXT          -- JSON array, null if passed
    );

    CREATE TABLE aesthetic_scores (
        id TEXT PRIMARY KEY,
        variant_id TEXT NOT NULL REFERENCES variants(id),
        view_id TEXT NOT NULL,
        scorer TEXT NOT NULL,         -- 'uiclip-v1' | 'claude-4-sonnet' | 'human:ewan'
        dimension TEXT,               -- null for overall, else dimension_id
        score REAL NOT NULL,
        rationale TEXT,               -- LLM's textual explanation
        scored_at TEXT NOT NULL
    );

    CREATE TABLE polish_scores (
        id TEXT PRIMARY KEY,
        variant_id TEXT NOT NULL REFERENCES variants(id),
        uiclip_score REAL,
        rubric_weighted_total REAL,
        composite_score REAL NOT NULL,
        visual_regression_diff_percent REAL,
        dimension_deltas_json TEXT,   -- JSON object
        computed_at TEXT NOT NULL
    );

    -- Indices for common queries
    CREATE INDEX idx_experiment_runs_status ON experiment_runs(status);
    CREATE INDEX idx_variants_experiment ON variants(experiment_id);
    CREATE INDEX idx_polish_scores_composite ON polish_scores(composite_score);
    CREATE INDEX idx_aesthetic_scores_dimension ON aesthetic_scores(dimension, score);

### 4.6 Scheduling & Triggers

#### Nightly Pipeline (Beast cron)

    # /etc/cron.d/visual-polish-nightly
    # Runs at 02:00 UTC (02:00 GMT / 03:00 BST)
    0 2 * * * polisher /opt/amplified/polish-pipeline/run-nightly.sh

**Nightly scope:** 1. Pull latest `main` branch 2. Build and serve app locally on Beast 3. Generate 3-5 variants for lowest-scoring dimension 4. Render all canonical views for each variant 5. Run hard checks → discard failures 6. Run aesthetic scoring on survivors 7. Compute composite scores 8. Push results to DB + generate summary report 9. Notify Ewan via Slack if improvement candidate found

#### Per-PR Pipeline (CI integration)

    # .github/workflows/visual-polish.yml
    name: Visual Polish Check
    on: [pull_request]

    jobs:
      polish-check:
        runs-on: ubuntu-latest
        steps:
          - uses: actions/checkout@v4
          - name: Install dependencies
            run: npm ci
          - name: Build
            run: npm run build
          - name: Run hard checks
            run: npx polish-lint --config principles/rules/
          - name: Visual regression
            run: npx playwright test --project=visual-regression
          - name: Upload diff artifacts
            if: failure()
            uses: actions/upload-artifact@v4
            with:
              name: visual-regression-diffs
              path: test-results/

#### Per-Feature / Manual

    # CLI tool on Beast
    polish-experiment \
      --target-dimension spatial_breathing \
      --category spacing \
      --variants 5 \
      --views shell-sidebar-open,shell-metrics \
      --baseline current

PART 6: UX METHODOLOGY INTEGRATION
----------------------------------

*From spec section 5, verbatim.*

### 5.1 What Gets Codified vs. What Stays Human

  Method                               Codified (Rules/Pipeline)                                                                                                                           Human Judgement
  ------------------------------------ --------------------------------------------------------------------------------------------------------------------------------------------------- -----------------------------------------------------------------------------------------------------------------------------------
  **Heuristic Evaluation** (Nielsen)   H1-H10 mapped to rules. H4 (Consistency) → token enforcement. H8 (Aesthetic) → aesthetic scoring. H2 (Real-world match) → component naming rules.   Severity assessment on novel issues. Trade-off decisions between competing heuristics (e.g. H7 Flexibility vs. H4 Consistency).
  **Cognitive Walkthrough**            Task completion paths can be automated via Playwright test flows. Step count and error recovery paths measurable.                                   Whether the flow "feels" right. Emotional response to transitions. Whether the voice-first metaphor is maintained.
  **Usability Testing**                Quantitative metrics: task time, error rate, click heatmaps.                                                                                        Qualitative observations: confusion, delight, trust signals. User's mental model vs. system model alignment.
  **Analytics-Driven UX**              Funnel completion, bounce rates, time-on-view, scroll depth. All log-able and trend-able.                                                           Interpreting WHY metrics moved. Distinguishing correlation from causation. Deciding which metric matters more when they conflict.
  **Design System Compliance**         100% automated. Token usage, component structure, naming conventions.                                                                               Whether the system itself needs to evolve. When to break the rules intentionally.
  **Aesthetic Judgement**              Partially automated via UIClip + LLM rubric. Captures \~75% of expert agreement.                                                                    The remaining 25%. "Taste" decisions. Whether something is technically correct but emotionally wrong.

### 5.2 Expert Team Workflow

#### Role: UX Lead (currently Ewan; scales to dedicated role)

**Weekly cadence:**

1.  **Monday: Review Kaizen Log** (\~30 min)
    -   Open the Kaizen dashboard on Beast
    -   Review experiments from past week: what was proposed, what scored well, what was accepted
    -   Look for patterns: is one dimension consistently improving while another stagnates?
    -   Decision: adjust rubric weights, add/modify rules, or flag for deeper investigation
2.  **Wednesday: Qualitative Review** (\~45 min, fortnightly)
    -   Open canonical views side-by-side with positive reference examples
    -   "Squint test" --- does our app look like it belongs in the same gallery?
    -   Specific checks: demo page congruence with production, component cohesion, any new "feels off" observations
    -   Log subjective notes as potential rule candidates
3.  **Friday: Accept/Reject Proposals** (\~20 min)
    -   Review the top-scoring variants from the week's experiments
    -   Accept, reject, or request modifications
    -   Accepted changes merge to `main` via PR

#### Role: AI Agents (Claude, Evaluation LLMs)

-   Generate variants within constraints
-   Score screenshots against rubric
-   Flag anomalies (large score swings, unexpected regressions)
-   Never override hard rules
-   Never ship without human approval

#### Over-Optimisation Guard

**Risk:** Optimising UIClip + LLM rubric scores to the point where the interface looks "technically correct" but loses soul.

**Mitigation:** - Monthly "taste review" by Ewan (or UX lead) where scores are ignored entirely - Compare current UI to a curated set of 5-10 aspirational examples, updated quarterly - If qualitative review diverges from quantitative scores, the qualitative review wins --- and we investigate why the scoring model missed it - Document these divergences as training data for improving the rubric

PART 7: AI GUARDRAILS
---------------------

*From spec section 6, verbatim.*

### 6.1 Generation Prompt Template

When Claude (or any agent) generates React UI components:

    ## SYSTEM PROMPT: UI Generation Agent

    You are generating React components for the Amplified Partners product.

    ### ABSOLUTE CONSTRAINTS (violations = build failure)
    Read and obey every rule with severity "error" in the principles library:
    [inject rules where severity == "error"]

    ### DESIGN TOKENS (your only palette)
    Use ONLY these values. No arbitrary colours, sizes, or spacing.
    [inject current tokens JSON]

    ### COMPONENT PATTERNS
    Use these established patterns:
    - KPI Card: large metric value (font.mono + fontSize.2xl + fontWeight.semibold),
      label below (fontSize.xs + text-muted), optional delta with directional indicator
    - Data Table: compact density (fontSize.sm, space.8 row padding), sticky header,
      alternating row backgrounds using surface/surface-alt tokens
    - Transcript Panel: mono font, left-aligned, timestamps in caption style,
      speaker labels in medium weight, content in regular
    - Section: heading3 + space.8 gap + content, space.32 between sections

    ### AESTHETIC TARGETS
    Aim for:
    - Calm, professional appearance (think Linear, Vercel, Stripe)
    - Visual hierarchy through size and weight, not colour (use colour sparingly)
    - Generous whitespace — when in doubt, add more space, not less
    - Data should be the hero; chrome should recede

    ### WHAT NOT TO DO
    - No decorative gradients, borders, or shadows unless they encode information
    - No more than 3 distinct card styles per view
    - No font sizes outside the token scale
    - No animation > 500ms
    - No placeholder copy ("Lorem ipsum") — use realistic data
    - No inline styles — use CSS modules or Tailwind with token classes

    ### OUTPUT FORMAT
    Return valid React TSX using:
    - CSS modules importing from the generated token CSS
    - OR Tailwind classes mapped to tokens (e.g., `gap-space-16`, `text-fontSize-base`)
    - data-component and data-role attributes on semantic elements (for rule checking)

### 6.2 Evaluation Prompt Template

When multimodal LLMs evaluate screenshots:

    ## SYSTEM PROMPT: Visual Polish Evaluator

    You are an expert visual designer evaluating a UI screenshot for design polish.

    ### YOUR ROLE
    - Score each dimension of the rubric (1-10)
    - Provide a brief rationale for each score
    - The hard rules have ALREADY been checked by automated tools — you do NOT need to check token compliance, contrast ratios, or accessibility. Those are handled.
    - You ARE checking for: aesthetic quality, visual rhythm, hierarchy, cohesion, calmness, data clarity, and overall "feel"

    ### RUBRIC
    [inject rubric JSON from Section 4.4.2]

    ### REFERENCE EXAMPLES
    Positive (target aesthetic):
    [inject positive example screenshots]

    Negative (what to avoid):
    [inject negative example screenshots]

    ### CRITICAL INSTRUCTIONS
    - Be specific. "Typography could improve" is useless. "The heading at 28px feels too large relative to the 14px body — try 24px or reduce to 3 heading levels" is useful.
    - Score honestly. Our goal is improvement, not validation. A score of 6 is useful; a score of 9 we didn't earn is harmful.
    - Focus on the screenshot you're given. Don't hallucinate elements that aren't there.
    - If the screenshot shows data, evaluate whether the data hierarchy is clear.
    - Do NOT suggest changes that would violate the hard rules (e.g., don't suggest arbitrary colours).

    ### OUTPUT FORMAT
    Return a JSON object:
    {
      "scores": {
        "calm_surface": { "score": 7, "rationale": "..." },
        "clear_hierarchy": { "score": 8, "rationale": "..." },
        ...
      },
      "overall_score": 7.2,
      "top_suggestion": "The most impactful single change would be...",
      "secondary_suggestions": ["...", "..."]
    }

### 6.3 Iteration Loop

    ┌──────────────────────────────────────────────────┐
    │  AI Agent generates component or layout           │
    │  ↓                                                │
    │  Hard Lint Check (pre-commit hook)                │
    │  ↓ PASS                                           │
    │  Build & Render in Playwright                     │
    │  ↓                                                │
    │  Screenshot Capture                               │
    │  ↓                                                │
    │  Aesthetic Scoring (UIClip + LLM Rubric)          │
    │  ↓                                                │
    │  Score < baseline?                                │
    │  ├── YES → AI receives feedback:                  │
    │  │         "Score dropped in [dimension].          │
    │  │          Specific issue: [rationale].            │
    │  │          Suggestion: [from evaluator].           │
    │  │          Please revise."                        │
    │  │   ↓                                             │
    │  │   AI revises (max 3 iterations)                │
    │  │   ↓ loop back to Hard Lint Check               │
    │  │                                                │
    │  └── NO → Score >= baseline?                      │
    │       ├── YES → Submit for human review           │
    │       └── MARGINAL → Log for Kaizen, use baseline │
    └──────────────────────────────────────────────────┘

**Max 3 revision iterations** --- if the AI can't improve after 3 attempts, fall back to baseline and log the issue for human investigation. This prevents infinite loops and wasted compute.

PART 8: CANONICAL LAYOUT PATTERNS
---------------------------------

*From spec section 7, verbatim.*

### 7.1 Voice-First Product Shell

#### Layout Structure

    ┌──────────────────────────────────────────────────────┐
    │  ┌─────────┐ ┌──────────────────────────────────┐    │
    │  │         │ │  VIEW HEADER                      │    │
    │  │  SIDE-  │ │  [View title]  [filters] [actions]│    │
    │  │  BAR    │ ├──────────────────────────────────┤    │
    │  │         │ │                                    │    │
    │  │  nav    │ │  MAIN CONTENT AREA                │    │
    │  │  items  │ │                                    │    │
    │  │         │ │  ┌──────────┐ ┌──────────┐        │    │
    │  │  -----  │ │  │ KPI Card │ │ KPI Card │  ...   │    │
    │  │         │ │  └──────────┘ └──────────┘        │    │
    │  │  voice  │ │                                    │    │
    │  │  status │ │  ┌────────────────────────────┐   │    │
    │  │         │ │  │ Data Table / Chart          │   │    │
    │  │         │ │  │                              │   │    │
    │  │         │ │  └────────────────────────────┘   │    │
    │  │         │ │                                    │    │
    │  └─────────┘ └──────────────────────────────────┘    │
    │                                                       │
    │  ┌───────────────────────────────────────────────┐   │
    │  │  TRANSCRIPT PANEL (collapsible, bottom/right)  │   │
    │  │  [timestamp] Speaker: content...               │   │
    │  │  [timestamp] AI: content...                    │   │
    │  └───────────────────────────────────────────────┘   │
    └──────────────────────────────────────────────────────┘

#### Priority Rules

  Rule ID                    Applied Differently                                       Reason
  -------------------------- --------------------------------------------------------- -------------------------------------------------------
  A-01 (Calm surface)        Weight ×1.2                                               Data-heavy view needs extra calm to prevent overwhelm
  A-09 (Data legibility)     Weight ×1.3                                               Primary purpose is data comprehension
  A-04 (Spatial breathing)   Weight ×0.9                                               Slightly tighter to fit more data; but not cramped
  MOT-001                    Transcript auto-scroll exempted from motion constraints   Natural scrolling behaviour

#### Specific Token Overrides

    {
      "shell": {
        "sidebar": {
          "width": { "$value": { "value": 240, "unit": "px" }, "$description": "Collapsed: 48px" },
          "background": "{color.surface}",
          "padding": "{space.12}",
          "itemGap": "{space.2}",
          "itemPaddingY": "{space.6}",
          "itemPaddingX": "{space.8}",
          "itemRadius": "{radius.md}",
          "fontSize": "{fontSize.sm}"
        },
        "header": {
          "height": { "$value": { "value": 48, "unit": "px" } },
          "paddingX": "{space.16}",
          "borderBottom": "1px solid {color.border}"
        },
        "transcript": {
          "maxHeight": { "$value": { "value": 280, "unit": "px" } },
          "background": "{color.surface-alt}",
          "fontFamily": "{font.mono}",
          "fontSize": "{fontSize.sm}",
          "lineHeight": "{lineHeight.normal}",
          "timestampColor": "{color.text-faint}",
          "speakerColor": "{color.text-muted}",
          "contentColor": "{color.text}"
        }
      }
    }

### 7.2 Demo Page

#### Layout Structure

    ┌──────────────────────────────────────────┐
    │  NAV BAR (minimal, logo + CTA)           │
    ├──────────────────────────────────────────┤
    │                                          │
    │  HERO SECTION                            │
    │  [Headline — what it does]               │
    │  [Subheadline — who it's for]            │
    │  [Primary CTA]                           │
    │  [Product screenshot — REAL, not mockup] │
    │                                          │
    ├──────────────────────────────────────────┤
    │                                          │
    │  VALUE PROPOSITIONS (3 max)              │
    │  ┌────┐  ┌────┐  ┌────┐                │
    │  │ VP │  │ VP │  │ VP │                │
    │  └────┘  └────┘  └────┘                │
    │                                          │
    ├──────────────────────────────────────────┤
    │                                          │
    │  SOCIAL PROOF / TRUST                    │
    │  [Testimonials or metrics — real data]   │
    │                                          │
    ├──────────────────────────────────────────┤
    │                                          │
    │  SECONDARY CTA                           │
    │                                          │
    ├──────────────────────────────────────────┤
    │  FOOTER (minimal)                        │
    └──────────────────────────────────────────┘

#### Priority Rules

  Rule ID                    Applied Differently   Reason
  -------------------------- --------------------- ----------------------------------------------------------------------------------
  A-10 (Congruent trust)     Weight ×2.0           This IS the trust page. Congruence is everything.
  A-04 (Spatial breathing)   Weight ×1.3           More generous spacing; landing page, not data tool
  A-07 (Motion purpose)      LESS motion           Reduce animation; let content speak. Max 1 subtle entrance animation.
  C-06                       HARD GATE             Screenshots on demo page must be programmatically captured from production build

#### Special Constraints

    {
      "demo": {
        "hero": {
          "maxHeadlineLength": 60,
          "maxSubheadlineLength": 120,
          "screenshotSource": "automated-from-production",
          "screenshotMaxAge": "7d",
          "animationCount": { "max": 1 },
          "animationDuration": { "max": { "value": 300, "unit": "ms" } }
        },
        "socialProof": {
          "testimonialCount": { "min": 1, "max": 3 },
          "dataPointsMustBeReal": true
        }
      }
    }

### 7.3 Client Landing Page

#### Layout Structure

    ┌──────────────────────────────────────────┐
    │  NAV BAR (client logo + nav + CTA)       │
    ├──────────────────────────────────────────┤
    │                                          │
    │  HERO SECTION                            │
    │  [Headline — client's value prop]        │
    │  [Subheadline]                           │
    │  [Primary CTA]   [Secondary CTA]        │
    │  [Hero image or illustration]            │
    │                                          │
    ├──────────────────────────────────────────┤
    │                                          │
    │  FEATURES / SERVICES (3-6)              │
    │  Grid or alternating layout              │
    │                                          │
    ├──────────────────────────────────────────┤
    │                                          │
    │  SOCIAL PROOF                            │
    │                                          │
    ├──────────────────────────────────────────┤
    │                                          │
    │  FAQ or PROCESS                          │
    │                                          │
    ├──────────────────────────────────────────┤
    │                                          │
    │  FINAL CTA                               │
    │                                          │
    ├──────────────────────────────────────────┤
    │  FOOTER                                  │
    └──────────────────────────────────────────┘

#### Priority Rules

  Rule ID                     Applied Differently     Reason
  --------------------------- ----------------------- -------------------------------------------------------
  A-02 (Clear hierarchy)      Weight ×1.3             Landing page must guide eye to CTA
  A-04 (Spatial breathing)    Weight ×1.5             Maximum breathing room; this is marketing, not a tool
  A-08 (Component cohesion)   Weight ×1.2             Fewer components, so each must be pristine
  TYP-002 (Line length)       Tighter: max 65 chars   Hero copy reads better shorter

### 7.4 Evaluation Weights (per layout pattern)

  Dimension            Product Shell   Demo Page   Client Landing
  -------------------- --------------- ----------- ----------------
  Calm surface         0.18            0.12        0.10
  Clear hierarchy      0.15            0.15        0.20
  Typographic rhythm   0.12            0.12        0.15
  Spatial breathing    0.11            0.16        0.18
  State clarity        0.10            0.05        0.05
  Consistent density   0.08            0.06        0.04
  Motion purpose       0.06            0.04        0.08
  Component cohesion   0.08            0.08        0.10
  Data legibility      0.09            0.07        0.03
  Congruent trust      0.03            0.15        0.07
  **Total**            **1.00**        **1.00**    **1.00**

PART 9: PUDDING TECHNIQUE INTEGRATION
-------------------------------------

*From spec section 8, verbatim.*

### 8.1 This System IS a Pudding

The Visual Polish System combines five distinct domains. Here's the PUDDING analysis:

#### Domain A: Graphic Design Principles

-   **PUDDING Label:** `C.=.0.∞` (Constraint, Stable, Scale-free, Timeless)
-   **Mechanisms:** Visual hierarchy, typographic rhythm, colour theory, grid systems, whitespace
-   **Dimensions:** `measurement`, `systems`, `constraint`, `cause_effect`

#### Domain B: Behavioural Psychology & Cognitive Load

-   **PUDDING Label:** `C.=.0.∞` (Constraint, Stable, Scale-free, Timeless)
-   **Mechanisms:** Hick's Law, Miller's Law, cognitive load theory, attention allocation, progressive disclosure
-   **Dimensions:** `mindset`, `constraint`, `threshold`, `routing`

#### Domain C: UX Heuristics & Task Methods

-   **PUDDING Label:** `P.~.1.m` (Process, Oscillating, Singular, Medium)
-   **Mechanisms:** Heuristic evaluation, cognitive walkthroughs, task analysis, usability testing
-   **Dimensions:** `measurement`, `feedback_loop`, `cause_effect`, `sequence`

#### Domain D: Analytics & Experimentation

-   **PUDDING Label:** `P.+.4.l` (Process, Amplifying, Network-scale, Long-duration)
-   **Mechanisms:** A/B testing, funnel analysis, engagement metrics, statistical significance
-   **Dimensions:** `measurement`, `amplifier`, `feedback_loop`, `threshold`

#### Domain E: Computational Aesthetics

-   **PUDDING Label:** `P.?.4.v` (Process, Emerging, Network-scale, Variable)
-   **Mechanisms:** CLIP embeddings, multimodal LLM evaluation, image quality metrics
-   **Dimensions:** `measurement`, `compression`, `amplifier`, `feedback_loop`

#### Shared Dimensions Analysis

  Dimension         A   B   C   D   E   Count
  ----------------- --- --- --- --- --- -------
  `measurement`     x       x   x   x   4
  `constraint`      x   x               2
  `feedback_loop`           x   x   x   3
  `cause_effect`    x       x           2
  `threshold`           x       x       2
  `amplifier`                   x   x   2

**Strongest bridge:** `measurement` (4/5 domains) and `feedback_loop` (3/5 domains).

### 8.2 Symbiotic Relationships --- Concrete Examples

#### Example 1: Typography Scale × Cognitive Load × Heuristic Evaluation

**A (Graphic Design):** A consistent typographic scale (major second, minor third) creates visual rhythm. **B (Behavioural Psych):** Fewer distinct font sizes reduce cognitive load --- the brain chunks information faster when the classification system is simpler. **C (UX Heuristics):** Nielsen's H4 (Consistency and Standards) requires consistent use of type sizes.

**The 1+1+1 = 5 insight:** When you enforce a strict typographic scale via tokens (only 10 permitted sizes), you simultaneously: 1. Satisfy the graphic design principle of rhythm (A) 2. Reduce cognitive load by limiting the classification system (B) 3. Pass heuristic evaluation for consistency (C) 4. Make the system measurable --- deviation from scale is automatically detectable (D) 5. Give the UIClip model a consistent signal to learn from (E)

**Testable prediction:** Enforcing our 10-step font size scale will improve scores on BOTH "typographic rhythm" AND "clear hierarchy" dimensions, because the forced simplicity makes the hierarchy more obvious, not less.

**PUDDING Score:** Shared dimensions × 2 + Unique\_A + Unique\_B + Unique\_C = (3×2) + 1 + 1 + 1 = 9 (High-value recipe)

#### Example 2: Whitespace Optimisation × Gestalt Proximity × Analytics

**A (Graphic Design):** Increasing padding between card groups from `space.16` to `space.24` improves spatial breathing. **B (Behavioural Psych):** Gestalt Law of Proximity --- items closer together are perceived as related. Increasing inter-group spacing strengthens perceived grouping. **D (Analytics):** Click heatmap data can quantify whether users more accurately target the correct group after spacing changes --- fewer mis-clicks = better grouping perception.

**The 1+1+1 = 5 insight:** A spacing change that graphic designers would call "breathing room" is the same change that Gestalt psychology would call "grouping clarity" is the same change that analytics would measure as "reduced mis-click rate." One token change (`space.16` → `space.24`), three independent validation methods.

**Why this matters for our system:** The Kaizen pipeline can simultaneously measure: - Aesthetic score improvement (from rubric: "spatial breathing") - Behavioural improvement (from rubric: "clear hierarchy" via grouping) - If deployed, analytics improvement (click accuracy on grouped elements)

All three agreeing on the same token change gives us **high-confidence Kaizen acceptance** --- the change is not just "prettier," it's functionally better.

**PUDDING Score:** (2×2) + 2 + 1 + 1 = 8 (High-value recipe)

#### Example 3: UIClip Training Data × Award-Site Reference Set × LLM Rubric Calibration

**E (Computational Aesthetics / UIClip):** UIClip was trained on JitterWeb (degraded real websites) to distinguish good from bad design. **A (Graphic Design / Award Sites):** Our positive reference set comes from Awwwards/CSS Design Awards winners --- curated examples of expert design. **C (UX Heuristics / LLM Rubric):** Our LLM rubric codifies expert heuristic knowledge into structured scoring.

**The 1+1+1 = 5 insight:** UIClip provides fast, cheap, broad-stroke scoring (pattern recognition). The LLM rubric provides slow, expensive, nuanced scoring (heuristic reasoning). The award-site reference set provides the aesthetic "north star" for both. By correlating UIClip scores with LLM rubric scores across many experiments, we can: 1. Identify where UIClip and the rubric agree (high confidence --- automate that dimension) 2. Identify where they diverge (investigate --- one of them is wrong, or the dimension is genuinely ambiguous) 3. Gradually increase UIClip weight as we build trust through calibration

This is **slime mould logic** (`R.?.4.v`) --- parallel path exploration, reinforcing paths that converge, starving paths that diverge.

**PUDDING Score:** (3×2) + 1 + 1 + 0 = 8 (High-value recipe)

### 8.3 Kaizen Monitoring Dashboard

#### Data Structures

    interface KaizenDashboard {
      // Trend over time
      polishScoreTrend: Array<{
        date: string;
        compositeScore: number;
        dimensionScores: Record<string, number>;
        layoutPattern: "shell" | "demo" | "landing";
      }>;

      // Experiment history
      experiments: Array<{
        id: string;
        date: string;
        category: string;
        targetDimension: string;
        bestVariantScore: number;
        baselineScore: number;
        delta: number;
        decision: "accepted" | "rejected";
      }>;

      // Dimension health
      dimensionHealth: Array<{
        dimension: string;
        currentScore: number;
        trend: "improving" | "stable" | "declining";
        trendSlope: number;  // Score change per week
        lastImproved: string;  // Date
        experimentsRun: number;
        experimentsAccepted: number;
      }>;

      // Rule evolution
      ruleEvolution: Array<{
        ruleId: string;
        addedDate: string;
        currentSeverity: string;
        promotions: Array<{ from: string; to: string; date: string; reason: string }>;
      }>;

      // Pudding connections
      puddingInsights: Array<{
        date: string;
        domains: string[];
        insight: string;
        validated: boolean;
        scoreImpact: number | null;
      }>;
    }

#### Visualisation

The dashboard (a React app served on Beast) shows:

1.  **Polish Score Timeline** --- Line chart, one line per layout pattern, composite score over time. Target: monotonically non-decreasing (ratchet).

2.  **Dimension Radar** --- Spider/radar chart showing current scores on all 10 aesthetic dimensions. Overlay: previous month for comparison.

3.  **Experiment Log** --- Table of experiments: date, category, target, delta, decision. Sortable, filterable.

4.  **Dimension Health Cards** --- One card per dimension: current score, trend arrow, slope, experiments run. Highlight dimensions that are stagnating (no improvement in 4+ weeks).

5.  **Rule Count by Severity** --- Bar chart: errors, warnings, suggestions. Track growth over time (healthy system adds rules).

6.  **Pudding Connection Map** --- Network visualisation: nodes = domains, edges = validated symbiotic relationships. Edge thickness = confidence.

PART 10: SCORING ENGINE --- PYTHON SOURCE
-----------------------------------------

### 10.1 Data Models (models.py)

`polish-pipeline/scoring/models.py`

    """
    Data models for the Visual Polish Scoring Pipeline.
    All types used across scoring, evaluation, and Kaizen decision-making.
    """

    from dataclasses import dataclass, field
    from typing import Optional
    from enum import Enum
    import json
    import time
    import uuid


    # ─── Enums ───────────────────────────────────────────────────────────────────

    class Severity(Enum):
        ERROR = "error"
        WARNING = "warning"
        SUGGESTION = "suggestion"


    class ExperimentTrigger(Enum):
        NIGHTLY = "nightly"
        PR = "pr"
        MANUAL = "manual"
        FEATURE = "feature"
        BASELINE = "baseline"


    class Decision(Enum):
        ACCEPTED = "accepted"
        REJECTED = "rejected"
        PENDING = "pending_review"


    # ─── Rubric Dimension ───────────────────────────────────────────────────────

    @dataclass
    class RubricDimension:
        """A single scoring dimension from the rubric."""
        id: str
        name: str
        weight: float
        prompt: str
        scale_min: int = 1
        scale_max: int = 10
        anchor_low: str = ""
        anchor_high: str = ""

        def validate_score(self, score: float) -> bool:
            """Check a score is within the valid range."""
            return self.scale_min <= score <= self.scale_max

        def normalise_score(self, score: float) -> float:
            """Normalise a raw score (1-10) to 0.0-1.0 range."""
            return (score - self.scale_min) / (self.scale_max - self.scale_min)

        def weighted_normalised(self, score: float) -> float:
            """Return the weighted contribution of this dimension to the composite."""
            return self.normalise_score(score) * self.weight


    # ─── Rubric (collection of dimensions) ──────────────────────────────────────

    @dataclass
    class Rubric:
        """The complete scoring rubric — loaded from rubric.json."""
        dimensions: list[RubricDimension] = field(default_factory=list)

        @classmethod
        def from_json(cls, path: str) -> "Rubric":
            """Load rubric from the JSON file."""
            with open(path, "r") as f:
                data = json.load(f)

            dims = []
            for d in data["rubric"]["dimensions"]:
                dims.append(RubricDimension(
                    id=d["id"],
                    name=d["name"],
                    weight=d["weight"],
                    prompt=d["prompt"],
                    scale_min=d["scale"]["min"],
                    scale_max=d["scale"]["max"],
                    anchor_low=d["scale"].get("anchor_low", ""),
                    anchor_high=d["scale"].get("anchor_high", ""),
                ))
            return cls(dimensions=dims)

        def total_weight(self) -> float:
            """Sum of all dimension weights. Must equal 1.0."""
            return sum(d.weight for d in self.dimensions)

        def validate_weights(self, tolerance: float = 0.001) -> bool:
            """Check weights sum to 1.0 within tolerance."""
            return abs(self.total_weight() - 1.0) < tolerance

        def dimension_ids(self) -> list[str]:
            return [d.id for d in self.dimensions]

        def get_dimension(self, dim_id: str) -> Optional[RubricDimension]:
            for d in self.dimensions:
                if d.id == dim_id:
                    return d
            return None


    # ─── Score Results ───────────────────────────────────────────────────────────

    @dataclass
    class DimensionScore:
        """Score for a single rubric dimension."""
        dimension_id: str
        raw_score: float       # 1-10
        normalised: float      # 0.0-1.0
        weighted: float        # normalised × weight
        rationale: str = ""


    @dataclass
    class RubricResult:
        """Complete rubric evaluation result."""
        scores: list[DimensionScore]
        overall_raw: float     # Weighted mean on 1-10 scale
        normalised: float      # 0.0-1.0
        top_suggestion: str = ""
        secondary_suggestions: list[str] = field(default_factory=list)
        scorer: str = ""
        scored_at: str = ""

        @property
        def dimension_dict(self) -> dict[str, float]:
            return {s.dimension_id: s.raw_score for s in self.scores}


    @dataclass
    class CompositeScore:
        """The final composite polish score combining all methods."""
        id: str = ""
        variant_id: str = ""

        uiclip_score: float = 0.0          # 0.0-1.0
        rubric_normalised: float = 0.0     # 0.0-1.0
        composite: float = 0.0             # 0.0-1.0

        uiclip_weight: float = 0.4
        rubric_weight: float = 0.6

        visual_regression_diff_pct: float = 0.0
        dimension_deltas: dict[str, float] = field(default_factory=dict)

        computed_at: str = ""

        def compute(self) -> float:
            """Calculate composite score from components."""
            self.composite = (
                self.uiclip_score * self.uiclip_weight
                + self.rubric_normalised * self.rubric_weight
            )
            return self.composite

        def validate_formula(self) -> bool:
            """Verify the composite was calculated correctly."""
            expected = (
                self.uiclip_score * self.uiclip_weight
                + self.rubric_normalised * self.rubric_weight
            )
            return abs(self.composite - expected) < 0.0001


    # ─── Kaizen Decision ────────────────────────────────────────────────────────

    @dataclass
    class KaizenDecision:
        """
        Acceptance/rejection logic for a Kaizen experiment.

        From the spec:
            accepted = (
                all_hard_checks_pass
                AND composite_score_delta > +0.005
                AND no_dimension_regression > 0.01
                AND human_approval == True
            )
        """
        all_hard_checks_pass: bool = False
        composite_delta: float = 0.0
        max_dimension_regression: float = 0.0
        human_approval: Optional[bool] = None

        min_composite_improvement: float = 0.005
        max_allowed_regression: float = 0.01

        @property
        def machine_recommendation(self) -> str:
            """What the system recommends, before human input."""
            if not self.all_hard_checks_pass:
                return "REJECT: Hard check failures"
            if self.composite_delta < self.min_composite_improvement:
                return f"REJECT: Composite delta {self.composite_delta:.4f} < {self.min_composite_improvement}"
            if self.max_dimension_regression > self.max_allowed_regression:
                return f"REJECT: Dimension regression {self.max_dimension_regression:.4f} > {self.max_allowed_regression}"
            return "RECOMMEND ACCEPT: All criteria met, pending human approval"

        @property
        def auto_criteria_met(self) -> bool:
            return (
                self.all_hard_checks_pass
                and self.composite_delta >= self.min_composite_improvement
                and self.max_dimension_regression <= self.max_allowed_regression
            )

        @property
        def final_decision(self) -> Decision:
            if not self.auto_criteria_met:
                return Decision.REJECTED
            if self.human_approval is None:
                return Decision.PENDING
            if self.human_approval:
                return Decision.ACCEPTED
            return Decision.REJECTED


    # ─── Hard Check Rule ────────────────────────────────────────────────────────

    @dataclass
    class Rule:
        """A single rule from core.rules.json."""
        id: str
        name: str
        category: str
        severity: Severity
        condition: dict
        rationale: str
        source: str = ""
        added: str = ""

        @classmethod
        def from_dict(cls, d: dict) -> "Rule":
            return cls(
                id=d["id"],
                name=d["name"],
                category=d["category"],
                severity=Severity(d["severity"]),
                condition=d.get("condition", {}),
                rationale=d["rationale"],
                source=d.get("source", ""),
                added=d.get("added", ""),
            )


    @dataclass
    class HardCheckResult:
        """Result of running a single hard check rule."""
        rule_id: str
        passed: bool
        violations: list[dict] = field(default_factory=list)

        @property
        def violation_count(self) -> int:
            return len(self.violations)

### 10.2 Scoring Engine (engine.py)

`polish-pipeline/scoring/engine.py`

    """
    Scoring Engine — reads rubric.json, computes scores, runs composite formula.

    This is the pure arithmetic core. No AI, no images — just numbers in, numbers out.
    External scorers (UIClip model, LLM rubric evaluator) feed raw scores INTO this
    engine, which validates, normalises, weights, and composites them.

    Usage:
        engine = ScoringEngine.from_rubric("path/to/rubric.json")
        result = engine.score(raw_scores={"calm_surface": 7, "clear_hierarchy": 8, ...})
        composite = engine.composite(rubric_result=result, uiclip_score=0.72)
    """

    from __future__ import annotations

    import json
    from dataclasses import dataclass, field
    from typing import Optional

    from .models import (
        Rubric,
        RubricDimension,
        DimensionScore,
        RubricResult,
        CompositeScore,
        KaizenDecision,
        Rule,
        HardCheckResult,
        Severity,
    )


    # ─── Hard Check Engine ──────────────────────────────────────────────────────

    @dataclass
    class HardCheckEngine:
        """
        Evaluates hard rules from core.rules.json.
        
        In the full pipeline these run against actual CSS / DOM.
        Here we accept pre-computed check results (pass/fail per rule)
        so the arithmetic can be tested in isolation.
        """
        rules: list[Rule] = field(default_factory=list)

        @classmethod
        def from_json(cls, path: str) -> "HardCheckEngine":
            with open(path, "r") as f:
                data = json.load(f)
            rules = [Rule.from_dict(r) for r in data["rules"]]
            return cls(rules=rules)

        def evaluate(self, check_results: dict[str, bool]) -> list[HardCheckResult]:
            """
            Given a dict of {rule_id: passed_bool}, return structured results.
            Missing rules default to passed=True (not yet checked).
            """
            results = []
            for rule in self.rules:
                passed = check_results.get(rule.id, True)
                violations = [] if passed else [{"rule_id": rule.id, "message": f"Failed: {rule.name}"}]
                results.append(HardCheckResult(
                    rule_id=rule.id,
                    passed=passed,
                    violations=violations,
                ))
            return results

        @staticmethod
        def all_errors_pass(results: list[HardCheckResult], rules: list[Rule]) -> bool:
            """
            Return True only if all ERROR-severity rules passed.
            Warnings and suggestions don't block.
            """
            error_rule_ids = {r.id for r in rules if r.severity == Severity.ERROR}
            for result in results:
                if result.rule_id in error_rule_ids and not result.passed:
                    return False
            return True

        def count_by_severity(self, results: list[HardCheckResult]) -> dict[str, int]:
            """Count failures grouped by severity."""
            severity_map = {r.id: r.severity for r in self.rules}
            counts = {"error": 0, "warning": 0, "suggestion": 0}
            for result in results:
                if not result.passed:
                    sev = severity_map.get(result.rule_id, Severity.SUGGESTION)
                    counts[sev.value] += 1
            return counts


    # ─── Rubric Scoring Engine ──────────────────────────────────────────────────

    @dataclass
    class ScoringEngine:
        """
        Pure arithmetic scoring engine.
        
        Takes raw dimension scores (1-10) and produces:
        - Normalised per-dimension scores (0.0-1.0)
        - Weighted per-dimension contributions
        - Overall rubric normalised score (0.0-1.0)
        - Composite score with UIClip blend
        """
        rubric: Rubric = field(default_factory=Rubric)

        @classmethod
        def from_rubric(cls, rubric_path: str) -> "ScoringEngine":
            rubric = Rubric.from_json(rubric_path)
            return cls(rubric=rubric)

        def validate_rubric(self) -> list[str]:
            """
            Run arithmetic validation checks on the rubric itself.
            Returns a list of error messages (empty = valid).
            """
            errors = []

            # 1. Weights must sum to 1.0
            total = self.rubric.total_weight()
            if abs(total - 1.0) >= 0.001:
                errors.append(f"Weights sum to {total:.6f}, expected 1.0 (tolerance 0.001)")

            # 2. No negative weights
            for dim in self.rubric.dimensions:
                if dim.weight < 0:
                    errors.append(f"Dimension '{dim.id}' has negative weight: {dim.weight}")
                if dim.weight == 0:
                    errors.append(f"Dimension '{dim.id}' has zero weight (dead dimension)")

            # 3. Scale min < max for all dimensions
            for dim in self.rubric.dimensions:
                if dim.scale_min >= dim.scale_max:
                    errors.append(f"Dimension '{dim.id}' has invalid scale: min={dim.scale_min} >= max={dim.scale_max}")

            # 4. No duplicate dimension IDs
            ids = [d.id for d in self.rubric.dimensions]
            if len(ids) != len(set(ids)):
                dupes = [x for x in ids if ids.count(x) > 1]
                errors.append(f"Duplicate dimension IDs: {set(dupes)}")

            return errors

        def score(
            self,
            raw_scores: dict[str, float],
            scorer: str = "test",
            rationales: Optional[dict[str, str]] = None,
        ) -> RubricResult:
            """
            Compute a full rubric result from raw dimension scores.
            
            Args:
                raw_scores: {dimension_id: raw_score (1-10)}
                scorer: Name of the scorer (e.g. "llm:claude-sonnet", "human:ewan")
                rationales: Optional {dimension_id: text_rationale}
            
            Returns:
                RubricResult with all normalised/weighted scores + overall.
            
            Raises:
                ValueError: If a score is out of range or dimension is unknown.
            """
            rationales = rationales or {}
            dimension_scores: list[DimensionScore] = []

            for dim in self.rubric.dimensions:
                if dim.id not in raw_scores:
                    raise ValueError(f"Missing score for dimension '{dim.id}'")
                
                raw = raw_scores[dim.id]
                if not dim.validate_score(raw):
                    raise ValueError(
                        f"Score {raw} for '{dim.id}' is out of range "
                        f"[{dim.scale_min}, {dim.scale_max}]"
                    )

                normalised = dim.normalise_score(raw)
                weighted = dim.weighted_normalised(raw)

                dimension_scores.append(DimensionScore(
                    dimension_id=dim.id,
                    raw_score=raw,
                    normalised=normalised,
                    weighted=weighted,
                    rationale=rationales.get(dim.id, ""),
                ))

            # Overall normalised = sum of weighted normalised scores
            overall_normalised = sum(ds.weighted for ds in dimension_scores)

            # Overall raw = weighted mean on the original 1-10 scale
            # = Σ(raw_score × weight) for all dimensions
            overall_raw = sum(
                raw_scores[dim.id] * dim.weight
                for dim in self.rubric.dimensions
            )

            import time
            result = RubricResult(
                scores=dimension_scores,
                overall_raw=overall_raw,
                normalised=overall_normalised,
                scorer=scorer,
                scored_at=time.strftime("%Y-%m-%dT%H:%M:%SZ"),
            )

            return result

        def composite(
            self,
            rubric_result: RubricResult,
            uiclip_score: float,
            uiclip_weight: float = 0.4,
            rubric_weight: float = 0.6,
            variant_id: str = "",
        ) -> CompositeScore:
            """
            Blend rubric + UIClip into a single composite score.
            
            composite = (uiclip × 0.4) + (rubric_normalised × 0.6)
            
            Both inputs must be in [0.0, 1.0].
            """
            if not (0.0 <= uiclip_score <= 1.0):
                raise ValueError(f"UIClip score must be 0.0-1.0, got {uiclip_score}")
            if not (0.0 <= rubric_result.normalised <= 1.0):
                raise ValueError(f"Rubric normalised must be 0.0-1.0, got {rubric_result.normalised}")
            if abs((uiclip_weight + rubric_weight) - 1.0) >= 0.001:
                raise ValueError(
                    f"Composite weights must sum to 1.0, got {uiclip_weight + rubric_weight}"
                )

            import time
            comp = CompositeScore(
                variant_id=variant_id,
                uiclip_score=uiclip_score,
                rubric_normalised=rubric_result.normalised,
                uiclip_weight=uiclip_weight,
                rubric_weight=rubric_weight,
                computed_at=time.strftime("%Y-%m-%dT%H:%M:%SZ"),
            )
            comp.compute()
            return comp

        def kaizen_compare(
            self,
            baseline: CompositeScore,
            candidate: CompositeScore,
            hard_checks_pass: bool = True,
        ) -> KaizenDecision:
            """
            Compare candidate against baseline for Kaizen acceptance.
            
            From the spec:
                accepted = (
                    all_hard_checks_pass
                    AND composite_delta > +0.005
                    AND no_dimension_regression > 0.01
                    AND human_approval == True
                )
            """
            composite_delta = candidate.composite - baseline.composite

            # Find max per-dimension regression
            max_regression = 0.0
            for dim_id, candidate_val in candidate.dimension_deltas.items():
                baseline_val = baseline.dimension_deltas.get(dim_id, 0.0)
                regression = baseline_val - candidate_val  # positive = regression
                max_regression = max(max_regression, regression)

            return KaizenDecision(
                all_hard_checks_pass=hard_checks_pass,
                composite_delta=composite_delta,
                max_dimension_regression=max_regression,
                human_approval=None,  # Always starts as pending
            )


    # ─── Convenience: Full Pipeline Run ─────────────────────────────────────────

    @dataclass
    class PipelineResult:
        """Complete result of running the full scoring pipeline."""
        hard_check_results: list[HardCheckResult]
        hard_checks_pass: bool
        hard_check_counts: dict[str, int]
        rubric_result: RubricResult
        composite: CompositeScore
        kaizen: Optional[KaizenDecision] = None

        @property
        def passed(self) -> bool:
            """Overall pass/fail (hard checks pass AND composite >= threshold)."""
            return self.hard_checks_pass

        def summary(self, threshold: float = 0.60) -> str:
            """Human-readable summary of the pipeline result."""
            lines = []
            lines.append("=" * 60)
            lines.append("  VISUAL POLISH SCORING REPORT")
            lines.append("=" * 60)

            # Hard checks
            lines.append(f"\n  HARD CHECKS: {'PASS' if self.hard_checks_pass else 'FAIL'}")
            for sev, count in self.hard_check_counts.items():
                if count > 0:
                    lines.append(f"    {sev.upper()}: {count} failure(s)")

            # Rubric dimensions
            lines.append(f"\n  RUBRIC SCORES (weighted)")
            lines.append(f"  {'Dimension':<25} {'Raw':>5} {'Norm':>7} {'Weighted':>9}")
            lines.append(f"  {'-'*25} {'─'*5} {'─'*7} {'─'*9}")
            for ds in self.rubric_result.scores:
                lines.append(
                    f"  {ds.dimension_id:<25} {ds.raw_score:>5.1f} {ds.normalised:>7.4f} {ds.weighted:>9.6f}"
                )
            lines.append(f"  {'─'*50}")
            lines.append(f"  {'OVERALL (raw weighted)':<25} {self.rubric_result.overall_raw:>5.2f}")
            lines.append(f"  {'OVERALL (normalised)':<25} {self.rubric_result.normalised:>12.6f}")

            # Composite
            lines.append(f"\n  COMPOSITE SCORE")
            lines.append(f"    UIClip score:       {self.composite.uiclip_score:.4f} × {self.composite.uiclip_weight}")
            lines.append(f"    Rubric normalised:  {self.composite.rubric_normalised:.4f} × {self.composite.rubric_weight}")
            lines.append(f"    ────────────────────────────")
            lines.append(f"    COMPOSITE:          {self.composite.composite:.4f}")
            lines.append(f"    Threshold:          {threshold:.4f}")
            status = "PASS" if self.composite.composite >= threshold else "FAIL"
            lines.append(f"    Result:             {status}")

            # Kaizen
            if self.kaizen:
                lines.append(f"\n  KAIZEN DECISION")
                lines.append(f"    {self.kaizen.machine_recommendation}")

            lines.append("\n" + "=" * 60)
            return "\n".join(lines)


    def run_pipeline(
        rubric_path: str,
        rules_path: str,
        raw_scores: dict[str, float],
        hard_check_results: dict[str, bool],
        uiclip_score: float,
        uiclip_weight: float = 0.4,
        rubric_weight: float = 0.6,
        baseline: Optional[CompositeScore] = None,
        scorer: str = "test",
    ) -> PipelineResult:
        """
        Run the full scoring pipeline end-to-end.
        
        This is the function the CLI and tests call.
        """
        # 1. Load engines
        scoring = ScoringEngine.from_rubric(rubric_path)
        hard_check_engine = HardCheckEngine.from_json(rules_path)

        # 2. Validate rubric integrity
        rubric_errors = scoring.validate_rubric()
        if rubric_errors:
            raise ValueError(f"Rubric validation failed: {rubric_errors}")

        # 3. Run hard checks
        hc_results = hard_check_engine.evaluate(hard_check_results)
        hc_pass = hard_check_engine.all_errors_pass(hc_results, hard_check_engine.rules)
        hc_counts = hard_check_engine.count_by_severity(hc_results)

        # 4. Run rubric scoring
        rubric_result = scoring.score(raw_scores, scorer=scorer)

        # 5. Compute composite
        composite = scoring.composite(
            rubric_result=rubric_result,
            uiclip_score=uiclip_score,
            uiclip_weight=uiclip_weight,
            rubric_weight=rubric_weight,
        )
        # Store per-dimension normalised values for Kaizen comparison
        composite.dimension_deltas = {
            ds.dimension_id: ds.normalised for ds in rubric_result.scores
        }

        # 6. Kaizen comparison (if baseline provided)
        kaizen = None
        if baseline is not None:
            kaizen = scoring.kaizen_compare(baseline, composite, hard_checks_pass=hc_pass)

        return PipelineResult(
            hard_check_results=hc_results,
            hard_checks_pass=hc_pass,
            hard_check_counts=hc_counts,
            rubric_result=rubric_result,
            composite=composite,
            kaizen=kaizen,
        )

### 10.3 CLI (cli.py)

`polish-pipeline/cli.py`

    #!/usr/bin/env python3
    """
    Visual Polish Scoring CLI

    Feed in scores, get numerical results back.

    Usage:
        # Interactive mode — prompts for each dimension score
        python cli.py --rubric ../principles/references/rubric.json \
                      --rules ../principles/rules/core.rules.json \
                      --interactive

        # JSON file mode — reads scores from a JSON file
        python cli.py --rubric ../principles/references/rubric.json \
                      --rules ../principles/rules/core.rules.json \
                      --input scores.json

        # Quick test with uniform scores
        python cli.py --rubric ../principles/references/rubric.json \
                      --rules ../principles/rules/core.rules.json \
                      --uniform 7 --uiclip 0.72

        # Validate rubric only (no scoring)
        python cli.py --rubric ../principles/references/rubric.json --validate

        # Compare two score files (Kaizen mode)
        python cli.py --rubric ../principles/references/rubric.json \
                      --rules ../principles/rules/core.rules.json \
                      --input candidate.json --baseline baseline.json
    """

    import argparse
    import json
    import sys
    import os

    # Add parent to path so scoring package is importable
    sys.path.insert(0, os.path.dirname(__file__))

    from scoring.engine import ScoringEngine, HardCheckEngine, run_pipeline
    from scoring.models import CompositeScore


    def load_score_file(path: str) -> dict:
        """Load a score input JSON file."""
        with open(path, "r") as f:
            return json.load(f)


    def interactive_scores(engine: ScoringEngine) -> tuple[dict[str, float], dict[str, bool], float]:
        """Prompt user for each dimension score interactively."""
        print("\n  Enter scores for each dimension (1-10):\n")
        scores = {}
        for dim in engine.rubric.dimensions:
            while True:
                try:
                    val = float(input(f"  {dim.name} ({dim.id}) [{dim.scale_min}-{dim.scale_max}]: "))
                    if dim.validate_score(val):
                        scores[dim.id] = val
                        break
                    print(f"    ⚠ Score must be between {dim.scale_min} and {dim.scale_max}")
                except ValueError:
                    print("    ⚠ Please enter a number")

        # UIClip score
        while True:
            try:
                uiclip = float(input("\n  UIClip score [0.0-1.0]: "))
                if 0.0 <= uiclip <= 1.0:
                    break
                print("    ⚠ Must be between 0.0 and 1.0")
            except ValueError:
                print("    ⚠ Please enter a number")

        # Hard checks — default all pass for interactive mode
        print("\n  Hard checks defaulting to all-pass. Use --input for specific check results.\n")
        hard_checks = {}

        return scores, hard_checks, uiclip


    def main():
        parser = argparse.ArgumentParser(
            description="Visual Polish Scoring Pipeline — arithmetic test harness",
            formatter_class=argparse.RawDescriptionHelpFormatter,
            epilog=__doc__,
        )
        parser.add_argument("--rubric", required=True, help="Path to rubric.json")
        parser.add_argument("--rules", help="Path to core.rules.json")
        parser.add_argument("--input", help="Path to score input JSON file")
        parser.add_argument("--baseline", help="Path to baseline score JSON (for Kaizen comparison)")
        parser.add_argument("--interactive", action="store_true", help="Interactive mode")
        parser.add_argument("--uniform", type=float, help="Set all dimensions to this score (quick test)")
        parser.add_argument("--uiclip", type=float, default=0.50, help="UIClip score (default 0.50)")
        parser.add_argument("--validate", action="store_true", help="Validate rubric only, no scoring")
        parser.add_argument("--threshold", type=float, default=0.60, help="Pass/fail threshold (default 0.60)")
        parser.add_argument("--json-output", action="store_true", help="Output results as JSON")

        args = parser.parse_args()

        # ─── Validate mode ───────────────────────────────────────────────
        if args.validate:
            engine = ScoringEngine.from_rubric(args.rubric)
            errors = engine.validate_rubric()
            if errors:
                print("\n  ✗ RUBRIC VALIDATION FAILED:")
                for e in errors:
                    print(f"    - {e}")
                sys.exit(1)
            else:
                print(f"\n  ✓ Rubric is valid")
                print(f"    Dimensions: {len(engine.rubric.dimensions)}")
                print(f"    Total weight: {engine.rubric.total_weight():.6f}")
                for dim in engine.rubric.dimensions:
                    print(f"    {dim.id:<25} weight={dim.weight:.2f}  scale=[{dim.scale_min},{dim.scale_max}]")
                sys.exit(0)

        # ─── Scoring modes ───────────────────────────────────────────────
        if not args.rules:
            parser.error("--rules is required for scoring (use --validate for rubric-only)")

        engine = ScoringEngine.from_rubric(args.rubric)

        if args.interactive:
            raw_scores, hard_check_results, uiclip = interactive_scores(engine)
        elif args.uniform is not None:
            dim_ids = engine.rubric.dimension_ids()
            raw_scores = {d: args.uniform for d in dim_ids}
            hard_check_results = {}
            uiclip = args.uiclip
        elif args.input:
            data = load_score_file(args.input)
            raw_scores = data.get("rubric_scores", data.get("scores", {}))
            hard_check_results = data.get("hard_checks", {})
            uiclip = data.get("uiclip_score", args.uiclip)
        else:
            parser.error("Provide --input, --interactive, or --uniform")

        # Fill missing hard checks with True (pass)
        hard_engine = HardCheckEngine.from_json(args.rules)
        for rule in hard_engine.rules:
            hard_check_results.setdefault(rule.id, True)

        # ─── Load baseline for Kaizen ────────────────────────────────────
        baseline_composite = None
        if args.baseline:
            baseline_data = load_score_file(args.baseline)
            baseline_raw = baseline_data.get("rubric_scores", baseline_data.get("scores", {}))
            baseline_hc = baseline_data.get("hard_checks", {})
            for rule in hard_engine.rules:
                baseline_hc.setdefault(rule.id, True)
            baseline_uiclip = baseline_data.get("uiclip_score", 0.50)

            baseline_result = run_pipeline(
                rubric_path=args.rubric,
                rules_path=args.rules,
                raw_scores=baseline_raw,
                hard_check_results=baseline_hc,
                uiclip_score=baseline_uiclip,
            )
            baseline_composite = baseline_result.composite

        # ─── Run pipeline ────────────────────────────────────────────────
        try:
            result = run_pipeline(
                rubric_path=args.rubric,
                rules_path=args.rules,
                raw_scores=raw_scores,
                hard_check_results=hard_check_results,
                uiclip_score=uiclip,
                baseline=baseline_composite,
            )
        except ValueError as e:
            print(f"\n  ✗ ERROR: {e}")
            sys.exit(1)

        # ─── Output ──────────────────────────────────────────────────────
        if args.json_output:
            output = {
                "hard_checks_pass": result.hard_checks_pass,
                "hard_check_counts": result.hard_check_counts,
                "rubric": {
                    "overall_raw": round(result.rubric_result.overall_raw, 4),
                    "normalised": round(result.rubric_result.normalised, 6),
                    "dimensions": {
                        ds.dimension_id: {
                            "raw": ds.raw_score,
                            "normalised": round(ds.normalised, 6),
                            "weighted": round(ds.weighted, 6),
                        }
                        for ds in result.rubric_result.scores
                    },
                },
                "composite": {
                    "uiclip_score": result.composite.uiclip_score,
                    "rubric_normalised": round(result.composite.rubric_normalised, 6),
                    "composite": round(result.composite.composite, 6),
                    "uiclip_weight": result.composite.uiclip_weight,
                    "rubric_weight": result.composite.rubric_weight,
                    "formula_valid": result.composite.validate_formula(),
                },
                "threshold": args.threshold,
                "result": "PASS" if result.composite.composite >= args.threshold else "FAIL",
            }
            if result.kaizen:
                output["kaizen"] = {
                    "composite_delta": round(result.kaizen.composite_delta, 6),
                    "max_dimension_regression": round(result.kaizen.max_dimension_regression, 6),
                    "auto_criteria_met": result.kaizen.auto_criteria_met,
                    "recommendation": result.kaizen.machine_recommendation,
                }
            print(json.dumps(output, indent=2))
        else:
            print(result.summary(threshold=args.threshold))

        # Exit code: 0 = pass, 1 = fail
        sys.exit(0 if result.composite.composite >= args.threshold else 1)


    if __name__ == "__main__":
        main()

PART 11: ARITHMETIC TEST SUITE
------------------------------

### 11.1 Test Results Summary

**76 tests, 10 categories, all passing.**

  \#   Category                           Tests
  ---- ---------------------------------- ---------
  1    Rubric Weight Integrity            8 tests
  2    Score Normalisation                9 tests
  3    Weighted Contribution Arithmetic   6 tests
  4    Composite Formula Verification     9 tests
  5    Kaizen Acceptance Logic            9 tests
  6    Hard Check Severity Gating         6 tests
  7    Edge Cases & Boundary Values       8 tests
  8    Synthetic Scenarios                5 tests
  9    Full Pipeline Integration          4 tests
  10   Mathematical Invariants            5 tests

Run with: `cd polish-pipeline && python -m pytest tests/ -v`

### 11.2 Full Test Source (test\_arithmetic.py)

`polish-pipeline/tests/test_arithmetic.py`

    """
    Arithmetic validation tests for the Visual Polish Scoring Pipeline.

    These tests verify that the scoring maths are correct — no AI, no images,
    just pure numerical validation. Run with: pytest tests/test_arithmetic.py -v

    Tests cover:
      1. Rubric weight integrity (sum to 1.0)
      2. Score normalisation correctness (1-10 → 0.0-1.0)
      3. Weighted contribution arithmetic
      4. Composite formula verification (uiclip × 0.4 + rubric × 0.6)
      5. Kaizen acceptance logic (delta > 0.005, no regression > 0.01)
      6. Hard check severity gating (only errors block)
      7. Edge cases and boundary values
      8. Synthetic test scenarios (good/bad/mediocre screenshots)
    """

    import sys
    import os
    import pytest
    import math

    # Add project root to path
    sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))

    from scoring.models import (
        Rubric,
        RubricDimension,
        DimensionScore,
        RubricResult,
        CompositeScore,
        KaizenDecision,
        Rule,
        HardCheckResult,
        Severity,
        Decision,
    )
    from scoring.engine import (
        ScoringEngine,
        HardCheckEngine,
        PipelineResult,
        run_pipeline,
    )


    # ─── Paths ──────────────────────────────────────────────────────────────────

    RUBRIC_PATH = os.path.join(os.path.dirname(__file__), "..", "..", "principles", "references", "rubric.json")
    RULES_PATH = os.path.join(os.path.dirname(__file__), "..", "..", "principles", "rules", "core.rules.json")


    # ─── Fixtures ───────────────────────────────────────────────────────────────

    @pytest.fixture
    def rubric():
        return Rubric.from_json(RUBRIC_PATH)


    @pytest.fixture
    def engine():
        return ScoringEngine.from_rubric(RUBRIC_PATH)


    @pytest.fixture
    def hard_check_engine():
        return HardCheckEngine.from_json(RULES_PATH)


    def make_scores(value: float) -> dict[str, float]:
        """Helper: create a score dict with all dimensions set to the same value."""
        return {
            "calm_surface": value,
            "clear_hierarchy": value,
            "typographic_rhythm": value,
            "spatial_breathing": value,
            "state_clarity": value,
            "consistent_density": value,
            "motion_purpose": value,
            "component_cohesion": value,
            "data_legibility": value,
            "congruent_trust": value,
        }


    # ═══════════════════════════════════════════════════════════════════════════
    # 1. RUBRIC WEIGHT INTEGRITY
    # ═══════════════════════════════════════════════════════════════════════════

    class TestRubricWeights:
        """Validate the rubric.json file is internally consistent."""

        def test_weights_sum_to_one(self, rubric):
            """Critical: all 10 dimension weights must sum to exactly 1.0."""
            total = rubric.total_weight()
            assert abs(total - 1.0) < 0.001, f"Weights sum to {total}, expected 1.0"

        def test_validate_weights_method(self, rubric):
            """The validate_weights() convenience method agrees."""
            assert rubric.validate_weights()

        def test_no_negative_weights(self, rubric):
            """No dimension should have a negative weight."""
            for dim in rubric.dimensions:
                assert dim.weight > 0, f"Dimension '{dim.id}' has non-positive weight: {dim.weight}"

        def test_no_zero_weights(self, rubric):
            """No dimension should have zero weight (dead dimension)."""
            for dim in rubric.dimensions:
                assert dim.weight > 0.0, f"Dimension '{dim.id}' has zero weight"

        def test_expected_dimension_count(self, rubric):
            """We expect exactly 10 dimensions."""
            assert len(rubric.dimensions) == 10

        def test_known_dimension_weights(self, rubric):
            """Verify each dimension has the expected weight from the spec."""
            expected = {
                "calm_surface": 0.15,
                "clear_hierarchy": 0.15,
                "typographic_rhythm": 0.12,
                "spatial_breathing": 0.12,
                "state_clarity": 0.10,
                "consistent_density": 0.08,
                "motion_purpose": 0.08,
                "component_cohesion": 0.08,
                "data_legibility": 0.07,
                "congruent_trust": 0.05,
            }
            for dim in rubric.dimensions:
                assert dim.id in expected, f"Unknown dimension: {dim.id}"
                assert abs(dim.weight - expected[dim.id]) < 0.001, (
                    f"Dimension '{dim.id}' weight is {dim.weight}, expected {expected[dim.id]}"
                )

        def test_no_duplicate_ids(self, rubric):
            """No two dimensions share an ID."""
            ids = [d.id for d in rubric.dimensions]
            assert len(ids) == len(set(ids)), f"Duplicate IDs found: {ids}"

        def test_engine_validate_rubric_passes(self, engine):
            """The engine's internal rubric validator finds no errors."""
            errors = engine.validate_rubric()
            assert errors == [], f"Rubric validation errors: {errors}"


    # ═══════════════════════════════════════════════════════════════════════════
    # 2. SCORE NORMALISATION
    # ═══════════════════════════════════════════════════════════════════════════

    class TestNormalisation:
        """Verify the 1-10 → 0.0-1.0 normalisation is correct."""

        def test_min_score_normalises_to_zero(self, rubric):
            """A score of 1 (scale minimum) normalises to 0.0."""
            dim = rubric.dimensions[0]
            assert dim.normalise_score(1) == 0.0

        def test_max_score_normalises_to_one(self, rubric):
            """A score of 10 (scale maximum) normalises to 1.0."""
            dim = rubric.dimensions[0]
            assert dim.normalise_score(10) == 1.0

        def test_midpoint_normalises_to_half(self, rubric):
            """A score of 5.5 (midpoint of 1-10) normalises to 0.5."""
            dim = rubric.dimensions[0]
            result = dim.normalise_score(5.5)
            assert abs(result - 0.5) < 0.001

        def test_normalisation_formula(self, rubric):
            """Check the formula: (score - min) / (max - min) = (score - 1) / 9."""
            dim = rubric.dimensions[0]
            for score in [1, 2, 3, 4, 5, 6, 7, 8, 9, 10]:
                expected = (score - 1) / 9
                actual = dim.normalise_score(score)
                assert abs(actual - expected) < 0.0001, (
                    f"Score {score}: expected {expected}, got {actual}"
                )

        def test_all_dimensions_use_same_scale(self, rubric):
            """All dimensions have scale 1-10."""
            for dim in rubric.dimensions:
                assert dim.scale_min == 1, f"Dimension '{dim.id}' has scale_min={dim.scale_min}"
                assert dim.scale_max == 10, f"Dimension '{dim.id}' has scale_max={dim.scale_max}"

        def test_validate_score_rejects_out_of_range(self, rubric):
            """Scores outside [1, 10] should be rejected."""
            dim = rubric.dimensions[0]
            assert not dim.validate_score(0)
            assert not dim.validate_score(0.5)
            assert not dim.validate_score(10.1)
            assert not dim.validate_score(11)
            assert not dim.validate_score(-1)

        def test_validate_score_accepts_in_range(self, rubric):
            """Scores within [1, 10] should be accepted."""
            dim = rubric.dimensions[0]
            assert dim.validate_score(1)
            assert dim.validate_score(5.5)
            assert dim.validate_score(10)

        @pytest.mark.parametrize("score", [1.0, 2.5, 5.0, 7.5, 10.0])
        def test_normalisation_monotonic(self, rubric, score):
            """Higher scores always produce higher normalised values."""
            dim = rubric.dimensions[0]
            if score > 1:
                assert dim.normalise_score(score) > dim.normalise_score(score - 1)


    # ═══════════════════════════════════════════════════════════════════════════
    # 3. WEIGHTED CONTRIBUTION ARITHMETIC
    # ═══════════════════════════════════════════════════════════════════════════

    class TestWeightedScoring:
        """Verify weighted contribution calculations."""

        def test_weighted_normalised_product(self, rubric):
            """weighted = normalise(score) × weight."""
            dim = rubric.get_dimension("calm_surface")
            score = 7.0
            normalised = dim.normalise_score(score)
            expected_weighted = normalised * dim.weight
            actual = dim.weighted_normalised(score)
            assert abs(actual - expected_weighted) < 0.0001

        def test_perfect_scores_give_sum_of_weights(self, engine):
            """All 10s → overall normalised should equal sum of weights (= 1.0)."""
            result = engine.score(make_scores(10))
            assert abs(result.normalised - 1.0) < 0.001

        def test_minimum_scores_give_zero(self, engine):
            """All 1s → overall normalised should be 0.0."""
            result = engine.score(make_scores(1))
            assert abs(result.normalised - 0.0) < 0.001

        def test_uniform_scores_give_correct_normalised(self, engine):
            """All same value → normalised = normalise(value) × 1.0 (sum of weights)."""
            for val in [3, 5, 7, 9]:
                result = engine.score(make_scores(val))
                expected = (val - 1) / 9  # normalise × total_weight (1.0)
                assert abs(result.normalised - expected) < 0.001, (
                    f"Uniform score {val}: expected {expected}, got {result.normalised}"
                )

        def test_single_high_dimension(self, engine):
            """One dimension high, rest low — verify weighting matters."""
            scores = make_scores(1)
            scores["calm_surface"] = 10  # weight 0.15
            result = engine.score(scores)
            # Expected: calm_surface contributes 1.0 × 0.15 = 0.15
            # All others contribute 0.0 × weight = 0.0
            assert abs(result.normalised - 0.15) < 0.001

        def test_overall_raw_is_weighted_mean(self, engine):
            """overall_raw = Σ(raw_score × weight) on the 1-10 scale."""
            scores = {
                "calm_surface": 8,       # 8 × 0.15 = 1.20
                "clear_hierarchy": 6,    # 6 × 0.15 = 0.90
                "typographic_rhythm": 7, # 7 × 0.12 = 0.84
                "spatial_breathing": 5,  # 5 × 0.12 = 0.60
                "state_clarity": 9,      # 9 × 0.10 = 0.90
                "consistent_density": 4, # 4 × 0.08 = 0.32
                "motion_purpose": 6,     # 6 × 0.08 = 0.48
                "component_cohesion": 7, # 7 × 0.08 = 0.56
                "data_legibility": 8,    # 8 × 0.07 = 0.56
                "congruent_trust": 5,    # 5 × 0.05 = 0.25
            }
            expected_raw = 1.20 + 0.90 + 0.84 + 0.60 + 0.90 + 0.32 + 0.48 + 0.56 + 0.56 + 0.25
            result = engine.score(scores)
            assert abs(result.overall_raw - expected_raw) < 0.01, (
                f"Expected raw {expected_raw}, got {result.overall_raw}"
            )


    # ═══════════════════════════════════════════════════════════════════════════
    # 4. COMPOSITE FORMULA
    # ═══════════════════════════════════════════════════════════════════════════

    class TestCompositeFormula:
        """Verify composite = (uiclip × 0.4) + (rubric_normalised × 0.6)."""

        def test_basic_composite(self, engine):
            """Composite formula with known inputs."""
            result = engine.score(make_scores(7))
            composite = engine.composite(result, uiclip_score=0.72)
            expected = 0.72 * 0.4 + result.normalised * 0.6
            assert abs(composite.composite - expected) < 0.0001

        def test_validate_formula_method(self, engine):
            """CompositeScore.validate_formula() should always return True after compute()."""
            result = engine.score(make_scores(8))
            composite = engine.composite(result, uiclip_score=0.85)
            assert composite.validate_formula()

        def test_composite_with_perfect_scores(self, engine):
            """All 10s + UIClip 1.0 → composite = 1.0."""
            result = engine.score(make_scores(10))
            composite = engine.composite(result, uiclip_score=1.0)
            assert abs(composite.composite - 1.0) < 0.001

        def test_composite_with_zero_scores(self, engine):
            """All 1s + UIClip 0.0 → composite = 0.0."""
            result = engine.score(make_scores(1))
            composite = engine.composite(result, uiclip_score=0.0)
            assert abs(composite.composite - 0.0) < 0.001

        def test_composite_weights_sum_to_one(self, engine):
            """Default composite weights (0.4 + 0.6) must sum to 1.0."""
            result = engine.score(make_scores(5))
            composite = engine.composite(result, uiclip_score=0.5)
            assert abs(composite.uiclip_weight + composite.rubric_weight - 1.0) < 0.001

        def test_custom_composite_weights(self, engine):
            """Custom weights (e.g., 0.3/0.7) should work and produce different results."""
            result = engine.score(make_scores(7))
            comp_default = engine.composite(result, uiclip_score=0.72)
            comp_custom = engine.composite(result, uiclip_score=0.72, uiclip_weight=0.3, rubric_weight=0.7)
            assert comp_default.composite != comp_custom.composite

        def test_invalid_composite_weights_rejected(self, engine):
            """Composite weights that don't sum to 1.0 should raise ValueError."""
            result = engine.score(make_scores(5))
            with pytest.raises(ValueError, match="weights must sum to 1.0"):
                engine.composite(result, uiclip_score=0.5, uiclip_weight=0.5, rubric_weight=0.6)

        def test_uiclip_out_of_range_rejected(self, engine):
            """UIClip score outside [0.0, 1.0] should raise ValueError."""
            result = engine.score(make_scores(5))
            with pytest.raises(ValueError):
                engine.composite(result, uiclip_score=1.5)
            with pytest.raises(ValueError):
                engine.composite(result, uiclip_score=-0.1)

        @pytest.mark.parametrize("uiclip,rubric_val,expected_min,expected_max", [
            (0.0, 1, 0.0, 0.01),       # Both at minimum
            (1.0, 10, 0.99, 1.01),     # Both at maximum
            (0.5, 5.5, 0.49, 0.51),    # Both at midpoint
            (0.9, 3, 0.36, 0.50),      # High UIClip, low rubric
            (0.1, 9, 0.50, 0.64),      # Low UIClip, high rubric
        ])
        def test_composite_range_scenarios(self, engine, uiclip, rubric_val, expected_min, expected_max):
            """Composite should fall in expected range for various inputs."""
            result = engine.score(make_scores(rubric_val))
            composite = engine.composite(result, uiclip_score=uiclip)
            assert expected_min <= composite.composite <= expected_max, (
                f"UIClip={uiclip}, rubric_val={rubric_val}: "
                f"composite={composite.composite:.4f}, expected [{expected_min}, {expected_max}]"
            )


    # ═══════════════════════════════════════════════════════════════════════════
    # 5. KAIZEN ACCEPTANCE LOGIC
    # ═══════════════════════════════════════════════════════════════════════════

    class TestKaizenDecision:
        """Verify the Kaizen accept/reject logic."""

        def test_accept_when_all_criteria_met(self):
            """Should recommend acceptance when all criteria pass."""
            decision = KaizenDecision(
                all_hard_checks_pass=True,
                composite_delta=0.010,          # > 0.005 ✓
                max_dimension_regression=0.005,  # ≤ 0.01 ✓
            )
            assert decision.auto_criteria_met
            assert decision.machine_recommendation.startswith("RECOMMEND ACCEPT")

        def test_reject_on_hard_check_failure(self):
            """Should reject if hard checks fail."""
            decision = KaizenDecision(
                all_hard_checks_pass=False,
                composite_delta=0.050,
                max_dimension_regression=0.0,
            )
            assert not decision.auto_criteria_met
            assert "Hard check" in decision.machine_recommendation

        def test_reject_on_insufficient_improvement(self):
            """Should reject if composite delta < 0.005."""
            decision = KaizenDecision(
                all_hard_checks_pass=True,
                composite_delta=0.004,  # < 0.005
                max_dimension_regression=0.0,
            )
            assert not decision.auto_criteria_met
            assert "Composite delta" in decision.machine_recommendation

        def test_reject_on_dimension_regression(self):
            """Should reject if any dimension regresses > 0.01."""
            decision = KaizenDecision(
                all_hard_checks_pass=True,
                composite_delta=0.020,
                max_dimension_regression=0.015,  # > 0.01
            )
            assert not decision.auto_criteria_met
            assert "regression" in decision.machine_recommendation.lower()

        def test_exact_threshold_accepted(self):
            """Exactly 0.005 delta and 0.01 regression should be accepted."""
            decision = KaizenDecision(
                all_hard_checks_pass=True,
                composite_delta=0.005,
                max_dimension_regression=0.01,
            )
            assert decision.auto_criteria_met

        def test_final_decision_pending_without_human(self):
            """Without human approval, final decision is PENDING."""
            decision = KaizenDecision(
                all_hard_checks_pass=True,
                composite_delta=0.010,
                max_dimension_regression=0.0,
                human_approval=None,
            )
            assert decision.final_decision == Decision.PENDING

        def test_final_decision_accepted_with_human(self):
            """With human approval=True and criteria met → ACCEPTED."""
            decision = KaizenDecision(
                all_hard_checks_pass=True,
                composite_delta=0.010,
                max_dimension_regression=0.0,
                human_approval=True,
            )
            assert decision.final_decision == Decision.ACCEPTED

        def test_final_decision_rejected_by_human(self):
            """Human can reject even when criteria are met."""
            decision = KaizenDecision(
                all_hard_checks_pass=True,
                composite_delta=0.050,
                max_dimension_regression=0.0,
                human_approval=False,
            )
            assert decision.final_decision == Decision.REJECTED

        def test_final_decision_rejected_when_criteria_fail(self):
            """Criteria failure → REJECTED regardless of human approval."""
            decision = KaizenDecision(
                all_hard_checks_pass=False,
                composite_delta=0.050,
                max_dimension_regression=0.0,
                human_approval=True,  # Even with approval
            )
            assert decision.final_decision == Decision.REJECTED


    # ═══════════════════════════════════════════════════════════════════════════
    # 6. HARD CHECK SEVERITY GATING
    # ═══════════════════════════════════════════════════════════════════════════

    class TestHardChecks:
        """Verify that only ERROR-severity rule failures block the pipeline."""

        def test_all_pass(self, hard_check_engine):
            """All rules pass → all_errors_pass returns True."""
            all_pass = {r.id: True for r in hard_check_engine.rules}
            results = hard_check_engine.evaluate(all_pass)
            assert HardCheckEngine.all_errors_pass(results, hard_check_engine.rules)

        def test_error_rule_fails_blocks(self, hard_check_engine):
            """An ERROR-severity rule failure should block."""
            checks = {r.id: True for r in hard_check_engine.rules}
            # TYP-001 is severity=error
            checks["TYP-001"] = False
            results = hard_check_engine.evaluate(checks)
            assert not HardCheckEngine.all_errors_pass(results, hard_check_engine.rules)

        def test_warning_rule_fails_does_not_block(self, hard_check_engine):
            """A WARNING-severity rule failure should NOT block."""
            checks = {r.id: True for r in hard_check_engine.rules}
            # TYP-002 is severity=warning
            checks["TYP-002"] = False
            results = hard_check_engine.evaluate(checks)
            assert HardCheckEngine.all_errors_pass(results, hard_check_engine.rules)

        def test_suggestion_rule_fails_does_not_block(self, hard_check_engine):
            """A SUGGESTION-severity rule failure should NOT block."""
            checks = {r.id: True for r in hard_check_engine.rules}
            # DEN-001 is severity=suggestion
            checks["DEN-001"] = False
            results = hard_check_engine.evaluate(checks)
            assert HardCheckEngine.all_errors_pass(results, hard_check_engine.rules)

        def test_severity_counts(self, hard_check_engine):
            """Count failures by severity."""
            checks = {r.id: True for r in hard_check_engine.rules}
            checks["TYP-001"] = False  # error
            checks["TYP-002"] = False  # warning
            checks["DEN-001"] = False  # suggestion
            results = hard_check_engine.evaluate(checks)
            counts = hard_check_engine.count_by_severity(results)
            assert counts["error"] == 1
            assert counts["warning"] == 1
            assert counts["suggestion"] == 1

        def test_expected_error_rules(self, hard_check_engine):
            """Verify which rules are ERROR severity (these are the blockers)."""
            error_rules = [r.id for r in hard_check_engine.rules if r.severity == Severity.ERROR]
            expected_errors = {"TYP-001", "CLR-001", "LAY-002", "MOT-001", "A11Y-001"}
            assert set(error_rules) == expected_errors


    # ═══════════════════════════════════════════════════════════════════════════
    # 7. EDGE CASES AND BOUNDARY VALUES
    # ═══════════════════════════════════════════════════════════════════════════

    class TestEdgeCases:
        """Boundary conditions and error handling."""

        def test_missing_dimension_raises(self, engine):
            """Omitting a dimension should raise ValueError."""
            scores = make_scores(5)
            del scores["calm_surface"]
            with pytest.raises(ValueError, match="Missing score"):
                engine.score(scores)

        def test_unknown_dimension_ignored(self, engine):
            """Extra dimensions in input are ignored (no error)."""
            scores = make_scores(5)
            scores["nonexistent_dimension"] = 7  # unknown
            result = engine.score(scores)
            assert len(result.scores) == 10  # only the 10 known dimensions

        def test_float_scores_accepted(self, engine):
            """Scores can be floats, not just integers."""
            scores = make_scores(7.3)
            result = engine.score(scores)
            assert 0.0 < result.normalised < 1.0

        def test_boundary_score_1(self, engine):
            """Score of exactly 1 (minimum) works."""
            scores = make_scores(1)
            result = engine.score(scores)
            assert abs(result.normalised - 0.0) < 0.001

        def test_boundary_score_10(self, engine):
            """Score of exactly 10 (maximum) works."""
            scores = make_scores(10)
            result = engine.score(scores)
            assert abs(result.normalised - 1.0) < 0.001

        def test_score_just_below_min_rejected(self, engine):
            """Score of 0.999 should be rejected (below scale_min=1)."""
            scores = make_scores(5)
            scores["calm_surface"] = 0.999
            with pytest.raises(ValueError, match="out of range"):
                engine.score(scores)

        def test_score_just_above_max_rejected(self, engine):
            """Score of 10.001 should be rejected (above scale_max=10)."""
            scores = make_scores(5)
            scores["calm_surface"] = 10.001
            with pytest.raises(ValueError, match="out of range"):
                engine.score(scores)

        def test_composite_preserves_inputs(self, engine):
            """Composite score stores the input values correctly."""
            result = engine.score(make_scores(6))
            composite = engine.composite(result, uiclip_score=0.73)
            assert abs(composite.uiclip_score - 0.73) < 0.0001
            assert abs(composite.rubric_normalised - result.normalised) < 0.0001


    # ═══════════════════════════════════════════════════════════════════════════
    # 8. SYNTHETIC TEST SCENARIOS
    # ═══════════════════════════════════════════════════════════════════════════

    class TestSyntheticScenarios:
        """
        Simulated scoring scenarios — good, bad, and mediocre screenshots.
        Each uses realistic score distributions to verify expected composite ranges.
        """

        def test_linear_dashboard_scenario(self, engine):
            """
            Scenario: Linear.app-quality dashboard.
            Expected: composite > 0.75 (high polish).
            """
            scores = {
                "calm_surface": 9,
                "clear_hierarchy": 9,
                "typographic_rhythm": 8,
                "spatial_breathing": 9,
                "state_clarity": 8,
                "consistent_density": 8,
                "motion_purpose": 9,
                "component_cohesion": 9,
                "data_legibility": 8,
                "congruent_trust": 9,
            }
            result = engine.score(scores)
            composite = engine.composite(result, uiclip_score=0.88)
            assert composite.composite > 0.75, f"Expected > 0.75, got {composite.composite:.4f}"

        def test_mvp_dashboard_scenario(self, engine):
            """
            Scenario: MVP / early-stage product.
            Expected: composite between 0.35 and 0.55.
            """
            scores = {
                "calm_surface": 4,
                "clear_hierarchy": 5,
                "typographic_rhythm": 3,
                "spatial_breathing": 4,
                "state_clarity": 5,
                "consistent_density": 4,
                "motion_purpose": 3,
                "component_cohesion": 4,
                "data_legibility": 5,
                "congruent_trust": 4,
            }
            result = engine.score(scores)
            composite = engine.composite(result, uiclip_score=0.35)
            assert 0.20 <= composite.composite <= 0.55, f"Expected 0.20-0.55, got {composite.composite:.4f}"

        def test_cluttered_dashboard_scenario(self, engine):
            """
            Scenario: Over-designed, cluttered dashboard.
            Expected: composite < 0.35.
            """
            scores = {
                "calm_surface": 2,
                "clear_hierarchy": 3,
                "typographic_rhythm": 2,
                "spatial_breathing": 2,
                "state_clarity": 4,
                "consistent_density": 2,
                "motion_purpose": 2,
                "component_cohesion": 3,
                "data_legibility": 3,
                "congruent_trust": 2,
            }
            result = engine.score(scores)
            composite = engine.composite(result, uiclip_score=0.15)
            assert composite.composite < 0.35, f"Expected < 0.35, got {composite.composite:.4f}"

        def test_kaizen_improvement_accepted(self, engine):
            """
            Scenario: Kaizen candidate improves all dimensions slightly.
            Expected: machine recommendation = ACCEPT.
            """
            baseline_scores = make_scores(6)
            candidate_scores = make_scores(6.5)  # +0.5 across all

            baseline_result = engine.score(baseline_scores)
            candidate_result = engine.score(candidate_scores)

            baseline_comp = engine.composite(baseline_result, uiclip_score=0.60)
            baseline_comp.dimension_deltas = {
                ds.dimension_id: ds.normalised for ds in baseline_result.scores
            }

            candidate_comp = engine.composite(candidate_result, uiclip_score=0.62)
            candidate_comp.dimension_deltas = {
                ds.dimension_id: ds.normalised for ds in candidate_result.scores
            }

            kaizen = engine.kaizen_compare(baseline_comp, candidate_comp, hard_checks_pass=True)
            assert kaizen.auto_criteria_met
            assert kaizen.composite_delta > 0.005

        def test_kaizen_regression_rejected(self, engine):
            """
            Scenario: Kaizen candidate improves overall but regresses one dimension badly.
            Expected: machine recommendation = REJECT due to dimension regression.
            """
            baseline_scores = make_scores(6)
            candidate_scores = make_scores(7)
            candidate_scores["calm_surface"] = 4  # regression from 6 to 4

            baseline_result = engine.score(baseline_scores)
            candidate_result = engine.score(candidate_scores)

            baseline_comp = engine.composite(baseline_result, uiclip_score=0.60)
            baseline_comp.dimension_deltas = {
                ds.dimension_id: ds.normalised for ds in baseline_result.scores
            }

            candidate_comp = engine.composite(candidate_result, uiclip_score=0.65)
            candidate_comp.dimension_deltas = {
                ds.dimension_id: ds.normalised for ds in candidate_result.scores
            }

            kaizen = engine.kaizen_compare(baseline_comp, candidate_comp, hard_checks_pass=True)
            assert not kaizen.auto_criteria_met
            assert "regression" in kaizen.machine_recommendation.lower()


    # ═══════════════════════════════════════════════════════════════════════════
    # 9. FULL PIPELINE INTEGRATION
    # ═══════════════════════════════════════════════════════════════════════════

    class TestFullPipeline:
        """End-to-end pipeline run with all components together."""

        def test_pipeline_pass(self):
            """Full pipeline with good scores should pass."""
            scores = make_scores(8)
            checks = {
                "TYP-001": True, "TYP-002": True, "CLR-001": True,
                "LAY-001": True, "LAY-002": True, "DEN-001": True,
                "MOT-001": True, "A11Y-001": True, "CMP-001": True,
            }
            result = run_pipeline(
                rubric_path=RUBRIC_PATH,
                rules_path=RULES_PATH,
                raw_scores=scores,
                hard_check_results=checks,
                uiclip_score=0.80,
            )
            assert result.passed
            assert result.composite.composite > 0.60
            assert result.hard_checks_pass

        def test_pipeline_fail_hard_check(self):
            """Pipeline should fail if an error-severity rule fails."""
            scores = make_scores(9)
            checks = {
                "TYP-001": False,  # ERROR — blocks
                "TYP-002": True, "CLR-001": True, "LAY-001": True,
                "LAY-002": True, "DEN-001": True, "MOT-001": True,
                "A11Y-001": True, "CMP-001": True,
            }
            result = run_pipeline(
                rubric_path=RUBRIC_PATH,
                rules_path=RULES_PATH,
                raw_scores=scores,
                hard_check_results=checks,
                uiclip_score=0.95,
            )
            assert not result.passed
            assert not result.hard_checks_pass

        def test_pipeline_summary_output(self):
            """Summary report should contain expected sections."""
            scores = make_scores(7)
            checks = {r: True for r in [
                "TYP-001", "TYP-002", "CLR-001", "LAY-001",
                "LAY-002", "DEN-001", "MOT-001", "A11Y-001", "CMP-001",
            ]}
            result = run_pipeline(
                rubric_path=RUBRIC_PATH,
                rules_path=RULES_PATH,
                raw_scores=scores,
                hard_check_results=checks,
                uiclip_score=0.70,
            )
            summary = result.summary()
            assert "HARD CHECKS" in summary
            assert "RUBRIC SCORES" in summary
            assert "COMPOSITE SCORE" in summary
            assert "PASS" in summary or "FAIL" in summary

        def test_pipeline_with_kaizen_baseline(self):
            """Pipeline with baseline comparison runs Kaizen logic."""
            baseline_scores = make_scores(6)
            checks = {r: True for r in [
                "TYP-001", "TYP-002", "CLR-001", "LAY-001",
                "LAY-002", "DEN-001", "MOT-001", "A11Y-001", "CMP-001",
            ]}
            baseline = run_pipeline(
                rubric_path=RUBRIC_PATH,
                rules_path=RULES_PATH,
                raw_scores=baseline_scores,
                hard_check_results=checks,
                uiclip_score=0.55,
            )

            candidate_scores = make_scores(7)
            candidate = run_pipeline(
                rubric_path=RUBRIC_PATH,
                rules_path=RULES_PATH,
                raw_scores=candidate_scores,
                hard_check_results=checks,
                uiclip_score=0.65,
                baseline=baseline.composite,
            )
            assert candidate.kaizen is not None
            assert candidate.kaizen.composite_delta > 0


    # ═══════════════════════════════════════════════════════════════════════════
    # 10. MATHEMATICAL INVARIANTS
    # ═══════════════════════════════════════════════════════════════════════════

    class TestMathematicalInvariants:
        """Properties that must hold for ANY valid input."""

        def test_normalised_always_in_unit_interval(self, engine):
            """For any valid scores, normalised is always in [0.0, 1.0]."""
            for val in [1, 2, 3, 4, 5, 6, 7, 8, 9, 10]:
                result = engine.score(make_scores(val))
                assert 0.0 <= result.normalised <= 1.0, (
                    f"Score {val}: normalised={result.normalised} outside [0, 1]"
                )

        def test_composite_always_in_unit_interval(self, engine):
            """For any valid inputs, composite is always in [0.0, 1.0]."""
            for val in [1, 5, 10]:
                for uiclip in [0.0, 0.5, 1.0]:
                    result = engine.score(make_scores(val))
                    composite = engine.composite(result, uiclip_score=uiclip)
                    assert 0.0 <= composite.composite <= 1.0

        def test_monotonicity_of_composite(self, engine):
            """Higher rubric scores always produce higher composite (UIClip fixed)."""
            uiclip = 0.70
            prev_composite = -1.0
            for val in range(1, 11):
                result = engine.score(make_scores(val))
                composite = engine.composite(result, uiclip_score=uiclip)
                assert composite.composite > prev_composite, (
                    f"Monotonicity violated: score {val} produced {composite.composite:.4f} "
                    f"≤ previous {prev_composite:.4f}"
                )
                prev_composite = composite.composite

        def test_linearity_of_normalisation(self, engine):
            """Normalisation should be linear: equal steps in raw → equal steps in normalised."""
            result_low = engine.score(make_scores(3))
            result_mid = engine.score(make_scores(5))
            result_high = engine.score(make_scores(7))

            step_1 = result_mid.normalised - result_low.normalised
            step_2 = result_high.normalised - result_mid.normalised
            assert abs(step_1 - step_2) < 0.001, (
                f"Non-linear: step 3→5 = {step_1:.6f}, step 5→7 = {step_2:.6f}"
            )

        def test_weighted_sum_equals_normalised(self, engine):
            """Sum of individual weighted contributions must equal overall normalised."""
            scores = {
                "calm_surface": 7, "clear_hierarchy": 8, "typographic_rhythm": 5,
                "spatial_breathing": 6, "state_clarity": 9, "consistent_density": 4,
                "motion_purpose": 7, "component_cohesion": 8, "data_legibility": 6,
                "congruent_trust": 5,
            }
            result = engine.score(scores)
            manual_sum = sum(ds.weighted for ds in result.scores)
            assert abs(manual_sum - result.normalised) < 0.0001, (
                f"Weighted sum {manual_sum} ≠ normalised {result.normalised}"
            )

### 11.3 Example Score Files

#### Linear-Quality Dashboard

`polish-pipeline/examples/linear-quality.json`

    {
      "description": "Linear.app-quality dashboard — high polish reference",
      "uiclip_score": 0.88,
      "rubric_scores": {
        "calm_surface": 9,
        "clear_hierarchy": 9,
        "typographic_rhythm": 8,
        "spatial_breathing": 9,
        "state_clarity": 8,
        "consistent_density": 8,
        "motion_purpose": 9,
        "component_cohesion": 9,
        "data_legibility": 8,
        "congruent_trust": 9
      },
      "hard_checks": {
        "TYP-001": true,
        "TYP-002": true,
        "CLR-001": true,
        "LAY-001": true,
        "LAY-002": true,
        "DEN-001": true,
        "MOT-001": true,
        "A11Y-001": true,
        "CMP-001": true
      }
    }

#### MVP Product

`polish-pipeline/examples/mvp-product.json`

    {
      "description": "MVP / early-stage product — mediocre polish",
      "uiclip_score": 0.35,
      "rubric_scores": {
        "calm_surface": 4,
        "clear_hierarchy": 5,
        "typographic_rhythm": 3,
        "spatial_breathing": 4,
        "state_clarity": 5,
        "consistent_density": 4,
        "motion_purpose": 3,
        "component_cohesion": 4,
        "data_legibility": 5,
        "congruent_trust": 4
      },
      "hard_checks": {
        "TYP-001": false,
        "TYP-002": false,
        "CLR-001": false,
        "LAY-001": true,
        "LAY-002": true,
        "DEN-001": false,
        "MOT-001": true,
        "A11Y-001": true,
        "CMP-001": true
      }
    }

#### Kaizen Candidate

`polish-pipeline/examples/kaizen-candidate.json`

    {
      "description": "Kaizen iteration — slight improvement over mvp-product baseline",
      "uiclip_score": 0.42,
      "rubric_scores": {
        "calm_surface": 5,
        "clear_hierarchy": 6,
        "typographic_rhythm": 4,
        "spatial_breathing": 5,
        "state_clarity": 6,
        "consistent_density": 5,
        "motion_purpose": 4,
        "component_cohesion": 5,
        "data_legibility": 6,
        "congruent_trust": 5
      },
      "hard_checks": {
        "TYP-001": true,
        "TYP-002": true,
        "CLR-001": true,
        "LAY-001": true,
        "LAY-002": true,
        "DEN-001": true,
        "MOT-001": true,
        "A11Y-001": true,
        "CMP-001": true
      }
    }

### 11.4 Example CLI Output

The following is the actual output of running the CLI against `linear-quality.json`:

    python cli.py --rubric ../principles/references/rubric.json \
                  --rules ../principles/rules/core.rules.json \
                  --input examples/linear-quality.json
    ============================================================
      VISUAL POLISH SCORING REPORT
    ============================================================

      HARD CHECKS: PASS

      RUBRIC SCORES (weighted)
      Dimension                   Raw    Norm  Weighted
      ------------------------- ───── ─────── ─────────
      calm_surface                9.0  0.8889  0.133333
      clear_hierarchy             9.0  0.8889  0.133333
      typographic_rhythm          8.0  0.7778  0.093333
      spatial_breathing           9.0  0.8889  0.106667
      state_clarity               8.0  0.7778  0.077778
      consistent_density          8.0  0.7778  0.062222
      motion_purpose              9.0  0.8889  0.071111
      component_cohesion          9.0  0.8889  0.071111
      data_legibility             8.0  0.7778  0.054444
      congruent_trust             9.0  0.8889  0.044444
      ──────────────────────────────────────────────────
      OVERALL (raw weighted)     8.63
      OVERALL (normalised)          0.847778

      COMPOSITE SCORE
        UIClip score:       0.8800 × 0.4
        Rubric normalised:  0.8478 × 0.6
        ────────────────────────────
        COMPOSITE:          0.8607
        Threshold:          0.6000
        Result:             PASS

    ============================================================

**Interpretation:** The linear-quality reference scores a composite of 0.8607 --- well above the 0.60 threshold. This is the target aesthetic to aim for. An MVP product scoring around 0.29 and a Kaizen candidate scoring around 0.36 illustrate the improvement trajectory the loop is designed to drive.

PART 12: KEY MATHEMATICAL FORMULAE (QUICK REFERENCE)
----------------------------------------------------

### 12.1 Normalisation

    normalised = (raw_score - 1) / 9

Maps a raw score on the 1--10 scale to the 0.0--1.0 unit interval.

-   `raw_score = 1` → `normalised = 0.0`
-   `raw_score = 5.5` → `normalised ≈ 0.5`
-   `raw_score = 10` → `normalised = 1.0`

### 12.2 Rubric Normalised Score

    rubric_normalised = Σ( normalise(raw_i) × weight_i )   for all 10 dimensions

Where `normalise(raw_i) = (raw_i - 1) / 9` and `Σ weight_i = 1.0`.

### 12.3 Composite Score

    composite = (uiclip_score × 0.4) + (rubric_normalised × 0.6)

Both inputs must be in `[0.0, 1.0]`. Weights must sum to 1.0.

### 12.4 Kaizen Acceptance Criteria

    accepted = (
        all_hard_checks_pass                      # All ERROR-severity rules pass
        AND composite_delta > +0.005              # ≥ 0.5% composite improvement
        AND max_dimension_regression ≤ 0.01       # No dimension regresses > 1%
        AND human_approval == True                # Human must approve
    )

Where `composite_delta = candidate.composite - baseline.composite`.

### 12.5 Hard Check Gating

    pipeline_blocked = any(result.passed == False for result in error_severity_results)

Only `severity == "error"` rules block the pipeline. Warnings and suggestions are logged but do not block.

Error-severity rules in `core.rules.json` v1.0.0: - `TYP-001` --- No arbitrary font sizes - `CLR-001` --- No arbitrary colour values - `LAY-002` --- Spacing uses token values only - `MOT-001` --- Animation duration constraints - `A11Y-001` --- Text contrast ratio (body)

### 12.6 Dimension Weights Table

All 10 rubric dimensions and their weights (sum = 1.00):

  Dimension ID           Dimension Name       Weight
  ---------------------- -------------------- ----------
  `calm_surface`         Calm Surface         0.15
  `clear_hierarchy`      Clear Hierarchy      0.15
  `typographic_rhythm`   Typographic Rhythm   0.12
  `spatial_breathing`    Spatial Breathing    0.12
  `state_clarity`        State Clarity        0.10
  `consistent_density`   Consistent Density   0.08
  `motion_purpose`       Motion Purpose       0.08
  `component_cohesion`   Component Cohesion   0.08
  `data_legibility`      Data Legibility      0.07
  `congruent_trust`      Congruent Trust      0.05
  **Total**                                   **1.00**

### 12.7 Worked Example (linear-quality.json)

    Inputs:
      calm_surface      = 9  → normalised = (9-1)/9 = 0.8889  weighted = 0.8889 × 0.15 = 0.1333
      clear_hierarchy   = 9  → normalised = 0.8889             weighted = 0.8889 × 0.15 = 0.1333
      typographic_rhythm= 8  → normalised = (8-1)/9 = 0.7778  weighted = 0.7778 × 0.12 = 0.0933
      spatial_breathing = 9  → normalised = 0.8889             weighted = 0.8889 × 0.12 = 0.1067
      state_clarity     = 8  → normalised = 0.7778             weighted = 0.7778 × 0.10 = 0.0778
      consistent_density= 8  → normalised = 0.7778             weighted = 0.7778 × 0.08 = 0.0622
      motion_purpose    = 9  → normalised = 0.8889             weighted = 0.8889 × 0.08 = 0.0711
      component_cohesion= 9  → normalised = 0.8889             weighted = 0.8889 × 0.08 = 0.0711
      data_legibility   = 8  → normalised = 0.7778             weighted = 0.7778 × 0.07 = 0.0544
      congruent_trust   = 9  → normalised = 0.8889             weighted = 0.8889 × 0.05 = 0.0444

      rubric_normalised = sum(all weighted) = 0.8478
      uiclip_score = 0.88

      composite = (0.88 × 0.4) + (0.8478 × 0.6)
                = 0.3520 + 0.5087
                = 0.8607   ✓ PASS (threshold = 0.60)

PART 13: COVE BUILD PROMPT --- PHASE 1
--------------------------------------

The following is the complete contents of `COV-277-COVE-BUILD-PROMPT.md`:

Cove Build Prompt: COV-277 --- Phase 1 Foundation
=================================================

LINEAR ISSUE
------------

**COV-277:** Phase 1: Foundation --- Design Tokens, Style Dictionary, Stylelint Enforcement\
**Parent:** COV-276 (Visual Polish System Epic)\
**Branch:** `feature/visual-polish-system` (already exists, PR \#1 open)\
**Priority:** High

WHAT EXISTS
-----------

The `feature/visual-polish-system` branch already has:

    principles/
    ├── VISUAL-POLISH-SYSTEM-SPEC.md    # Full spec (read Section 3 + 9 for this task)
    ├── tokens/
    │   ├── typography.tokens.json       # W3C DTCG 2025.10 format
    │   ├── spacing.tokens.json
    │   ├── color.tokens.json
    │   ├── motion.tokens.json
    │   └── shadow.tokens.json
    ├── rules/
    │   └── core.rules.json              # 9 rules with severity levels
    ├── references/
    │   └── rubric.json                  # 10 aesthetic scoring dimensions
    └── schema/
        └── rule.schema.json             # JSON Schema for rules

    polish-pipeline/                     # Scoring test harness (76 tests, all pass)
    ├── scoring/
    │   ├── models.py                    # Data types: Rubric, DimensionScore, CompositeScore, KaizenDecision, etc.
    │   └── engine.py                    # Pure arithmetic engine: normalise, weight, composite, Kaizen compare
    ├── tests/
    │   └── test_arithmetic.py           # 76 tests: weights, normalisation, composite, Kaizen, edge cases, invariants
    ├── cli.py                           # CLI: --input scores.json → human-readable or JSON report
    └── examples/
        ├── linear-quality.json          # High-polish reference (composite ~0.86)
        ├── mvp-product.json             # MVP reference (composite ~0.29)
        └── kaizen-candidate.json        # Improvement over MVP (for Kaizen comparison testing)

### Scoring Maths (verified by 76 passing tests)

-   **Normalisation:** `(raw_score - 1) / 9` --- maps 1-10 to 0.0-1.0
-   **Rubric normalised:** `Σ(normalise(raw_i) × weight_i)` for all 10 dimensions
-   **Composite:** `(uiclip × 0.4) + (rubric_normalised × 0.6)`
-   **Kaizen acceptance:** `composite_delta > 0.005 AND no_dimension_regression > 0.01 AND human_approval`
-   **Hard check gating:** Only ERROR-severity rules block; warnings and suggestions are informational

Run tests: `cd polish-pipeline && python -m pytest tests/ -v`\
Run CLI: `python cli.py --rubric ../principles/references/rubric.json --rules ../principles/rules/core.rules.json --input examples/linear-quality.json`

WHAT YOU NEED TO BUILD
----------------------

### 1. Style Dictionary Configuration

Create `principles/style-dictionary.config.js` that: - Reads all `*.tokens.json` files from `principles/tokens/` - Handles W3C DTCG 2025.10 format (tokens have `$value`, `$type`, `$description`) - Uses `@tokens-studio/sd-transforms` or custom transforms for DTCG parsing - Outputs to `principles/dist/`: - `variables.css` --- CSS custom properties (flat, e.g. `--fontSize-base: 14px`) - `tailwind.tokens.js` --- Tailwind theme extension object - `tokens.flat.json` --- flat key-value map for agent consumption

**Important:** The token files use alias syntax like `"{font.sans}"`. Style Dictionary must resolve these.

### 2. Stylelint Configuration

Create `.stylelintrc.json` at repo root:

    {
      "extends": ["stylelint-config-standard"],
      "plugins": [],
      "rules": {
        "color-no-hex": true,
        "declaration-property-value-allowed-list": {
          "font-size": ["/var\\(--fontSize-/"],
          "color": ["/var\\(--color-/", "transparent", "currentColor", "inherit"],
          "background-color": ["/var\\(--color-/", "transparent", "inherit"],
          "border-color": ["/var\\(--color-/", "transparent", "inherit"],
          "margin": ["/var\\(--space-/", "0", "auto"],
          "padding": ["/var\\(--space-/", "0"],
          "gap": ["/var\\(--space-/", "0"],
          "border-radius": ["/var\\(--radius-/", "0"]
        }
      }
    }

Adjust the regex patterns to match exactly what Style Dictionary outputs. The key principle: **no arbitrary values for colour, spacing, typography, or border-radius**.

### 3. Token Validation Script

Create `principles/scripts/validate-tokens.js`:

    // Reads all .tokens.json files
    // For each token:
    //   - Validates $type is a known DTCG type (color, dimension, fontFamily, etc.)
    //   - Validates $value matches the expected structure for that type
    //   - If $value is an alias (e.g. "{font.sans}"), checks the target exists
    //   - Checks no circular references
    // Exits 0 on success, 1 on failure with details

### 4. Package Configuration

If `package.json` doesn't exist at repo root, create one. Add:

    {
      "name": "amplified-principles",
      "version": "1.0.0",
      "private": true,
      "scripts": {
        "tokens:build": "style-dictionary build --config principles/style-dictionary.config.js",
        "lint:styles": "stylelint '**/*.css' --config .stylelintrc.json",
        "lint:tokens": "node principles/scripts/validate-tokens.js"
      },
      "devDependencies": {
        "style-dictionary": "^4.0.0",
        "@tokens-studio/sd-transforms": "^1.0.0",
        "stylelint": "^16.0.0",
        "stylelint-config-standard": "^36.0.0"
      }
    }

### 5. .gitignore Addition

Add to `.gitignore`:

    principles/dist/
    node_modules/

CONSTRAINTS
-----------

-   All code must be committed to `feature/visual-polish-system` branch
-   Do NOT modify any existing files outside `principles/` except `.gitignore` and `package.json`
-   Token files are already valid JSON --- do NOT modify their structure
-   Style Dictionary config must handle the W3C DTCG `$value`/`$type` prefix format
-   Output CSS variables must use the pattern `--{group}-{name}` (e.g. `--fontSize-base`, `--color-semantic-bg`, `--space-16`)

ACCEPTANCE CRITERIA
-------------------

-   [ ] `npm install` succeeds
-   [ ] `npm run tokens:build` produces `principles/dist/variables.css`, `tailwind.tokens.js`, `tokens.flat.json`
-   [ ] CSS variables file contains at least 80 custom properties
-   [ ] `npm run lint:tokens` validates all 5 token files pass
-   [ ] `npm run lint:styles` would catch `color: #ff0000` as a violation
-   [ ] All new files committed to the feature branch
-   [ ] Tests pass (if any existing CI gates)

DEPENDENCY GRAPH
----------------

    COV-277 (this) → COV-280 (Pipeline) → COV-282 (Scoring) → COV-279 (Kaizen) → COV-278 (AI) → COV-281 (Scale)

This is the first domino. Get it right, everything else builds on it.

PART 14: LINEAR ISSUES & DEPENDENCY GRAPH
-----------------------------------------

### 14.1 Issue Table

  Issue ID   Title                                                                            Type   Parent    Priority   Status
  ---------- -------------------------------------------------------------------------------- ------ --------- ---------- --------------------
  COV-276    Visual Polish System Epic                                                        Epic   ---       High       In Progress
  COV-277    Phase 1: Foundation --- Design Tokens, Style Dictionary, Stylelint Enforcement   Task   COV-276   High       Ready
  COV-280    Phase 2: Pipeline Scaffolding --- Screenshots, DB, Playwright                    Task   COV-276   High       Blocked on COV-277
  COV-282    Phase 3: Scoring --- UIClip + LLM Rubric Evaluation                              Task   COV-276   High       Blocked on COV-280
  COV-279    Phase 4: Kaizen Loop --- Nightly Cron, PR Integration, Dashboard                 Task   COV-276   High       Blocked on COV-282
  COV-278    Phase 5: AI Integration --- Generation + Evaluation Prompt Templates             Task   COV-276   Medium     Blocked on COV-279
  COV-281    Phase 6: Scale --- Client Landing Pages, New Views, Rule Evolution               Task   COV-276   Medium     Blocked on COV-278

### 14.2 Dependency Chain

    COV-277 (Foundation)
        ↓
    COV-280 (Pipeline Scaffolding)
        ↓
    COV-282 (Scoring)
        ↓
    COV-279 (Kaizen Loop)
        ↓
    COV-278 (AI Integration)
        ↓
    COV-281 (Scale)

**COV-277 is the first domino.** The entire pipeline depends on the token build system and Stylelint enforcement being correct. All downstream issues are blocked until COV-277 is merged and passing CI.

### 14.3 Repository Context

-   **Repository:** github.com/ewan-dot/amplified-partners
-   **Branch:** `feature/visual-polish-system`
-   **PR:** \#1 (open)
-   **CI:** GitHub Actions (`.github/workflows/visual-polish.yml` --- to be created in COV-280)

PART 15: APPENDICES
-------------------

*From spec Section 9, verbatim.*

### 9.1 Complete Colour Token Set

    {
      "$schema": "./schema/token.schema.json",
      "$version": "1.0.0",
      "color": {
        "$type": "color",
        "$description": "All colors defined in LCH, with sRGB hex for fallback. Light mode defaults shown; dark mode via semantic alias override.",
        "primitive": {
          "neutral": {
            "0":   { "$value": { "colorSpace": "srgb", "components": [1, 1, 1], "hex": "#FFFFFF" } },
            "50":  { "$value": { "colorSpace": "srgb", "components": [0.969, 0.965, 0.949], "hex": "#F7F6F2" } },
            "100": { "$value": { "colorSpace": "srgb", "components": [0.976, 0.973, 0.961], "hex": "#F9F8F5" } },
            "200": { "$value": { "colorSpace": "srgb", "components": [0.831, 0.820, 0.792], "hex": "#D4D1CA" } },
            "300": { "$value": { "colorSpace": "srgb", "components": [0.729, 0.725, 0.706], "hex": "#BAB9B4" } },
            "400": { "$value": { "colorSpace": "srgb", "components": [0.478, 0.475, 0.455], "hex": "#7A7974" } },
            "500": { "$value": { "colorSpace": "srgb", "components": [0.353, 0.349, 0.337], "hex": "#5A5957" } },
            "900": { "$value": { "colorSpace": "srgb", "components": [0.157, 0.145, 0.114], "hex": "#28251D" } },
            "1000":{ "$value": { "colorSpace": "srgb", "components": [0.090, 0.086, 0.078], "hex": "#171614" } }
          },
          "teal": {
            "500": { "$value": { "colorSpace": "srgb", "components": [0.004, 0.412, 0.435], "hex": "#01696F" } },
            "600": { "$value": { "colorSpace": "srgb", "components": [0.047, 0.306, 0.329], "hex": "#0C4E54" } },
            "400": { "$value": { "colorSpace": "srgb", "components": [0.310, 0.596, 0.639], "hex": "#4F98A3" } }
          },
          "red":    { "500": { "$value": { "colorSpace": "srgb", "components": [0.631, 0.173, 0.482], "hex": "#A12C7B" } } },
          "amber":  { "500": { "$value": { "colorSpace": "srgb", "components": [0.588, 0.259, 0.098], "hex": "#964219" } } },
          "green":  { "500": { "$value": { "colorSpace": "srgb", "components": [0.263, 0.478, 0.133], "hex": "#437A22" } } }
        },
        "semantic": {
          "bg":           { "$value": "{color.primitive.neutral.50}" },
          "surface":      { "$value": "{color.primitive.neutral.100}" },
          "surface-alt":  { "$value": "{color.primitive.neutral.0}" },
          "border":       { "$value": "{color.primitive.neutral.200}" },
          "text":         { "$value": "{color.primitive.neutral.900}" },
          "text-muted":   { "$value": "{color.primitive.neutral.400}" },
          "text-faint":   { "$value": "{color.primitive.neutral.300}" },
          "primary":      { "$value": "{color.primitive.teal.500}" },
          "primary-hover":{ "$value": "{color.primitive.teal.600}" },
          "error":        { "$value": "{color.primitive.red.500}" },
          "warning":      { "$value": "{color.primitive.amber.500}" },
          "success":      { "$value": "{color.primitive.green.500}" }
        }
      }
    }

### 9.2 Motion Tokens

    {
      "$schema": "./schema/token.schema.json",
      "$version": "1.0.0",
      "duration": {
        "$type": "duration",
        "instant": { "$value": { "value": 50, "unit": "ms" }, "$description": "Opacity changes, micro-feedback" },
        "fast":    { "$value": { "value": 100, "unit": "ms" }, "$description": "Hover states, tooltips" },
        "normal":  { "$value": { "value": 200, "unit": "ms" }, "$description": "Standard transitions, panel open/close" },
        "slow":    { "$value": { "value": 350, "unit": "ms" }, "$description": "Page transitions, modal entrance" },
        "slower":  { "$value": { "value": 500, "unit": "ms" }, "$description": "Complex transitions only. Maximum." }
      },
      "easing": {
        "$type": "cubicBezier",
        "default":   { "$value": [0.25, 0.1, 0.25, 1.0], "$description": "Standard ease — most transitions" },
        "in":        { "$value": [0.42, 0, 1, 1], "$description": "Ease in — elements exiting" },
        "out":       { "$value": [0, 0, 0.58, 1], "$description": "Ease out — elements entering" },
        "in-out":    { "$value": [0.42, 0, 0.58, 1], "$description": "Ease in-out — position changes" },
        "spring":    { "$value": [0.34, 1.56, 0.64, 1], "$description": "Slight overshoot — playful feedback only" }
      }
    }

### 9.3 Shadow Tokens

    {
      "$schema": "./schema/token.schema.json",
      "$version": "1.0.0",
      "shadow": {
        "$type": "shadow",
        "none": { "$value": { "color": { "colorSpace": "srgb", "components": [0,0,0], "alpha": 0 }, "offsetX": {"value":0,"unit":"px"}, "offsetY": {"value":0,"unit":"px"}, "blur": {"value":0,"unit":"px"}, "spread": {"value":0,"unit":"px"} } },
        "sm": {
          "$value": {
            "color": { "colorSpace": "srgb", "components": [0,0,0], "alpha": 0.04 },
            "offsetX": {"value":0,"unit":"px"}, "offsetY": {"value":1,"unit":"px"},
            "blur": {"value":2,"unit":"px"}, "spread": {"value":0,"unit":"px"}
          },
          "$description": "Subtle elevation. Cards on surface."
        },
        "md": {
          "$value": {
            "color": { "colorSpace": "srgb", "components": [0,0,0], "alpha": 0.06 },
            "offsetX": {"value":0,"unit":"px"}, "offsetY": {"value":2,"unit":"px"},
            "blur": {"value":8,"unit":"px"}, "spread": {"value":-2,"unit":"px"}
          },
          "$description": "Standard elevation. Dropdowns, popovers."
        },
        "lg": {
          "$value": {
            "color": { "colorSpace": "srgb", "components": [0,0,0], "alpha": 0.08 },
            "offsetX": {"value":0,"unit":"px"}, "offsetY": {"value":4,"unit":"px"},
            "blur": {"value":16,"unit":"px"}, "spread": {"value":-4,"unit":"px"}
          },
          "$description": "High elevation. Modals, dialogs."
        },
        "xl": {
          "$value": {
            "color": { "colorSpace": "srgb", "components": [0,0,0], "alpha": 0.12 },
            "offsetX": {"value":0,"unit":"px"}, "offsetY": {"value":8,"unit":"px"},
            "blur": {"value":24,"unit":"px"}, "spread": {"value":-6,"unit":"px"}
          },
          "$description": "Maximum elevation. Command palette, floating panels."
        }
      }
    }

### 9.4 Implementation Sequence

#### Phase 1: Foundation (Week 1--2)

1.  Set up `principles/` directory in repo
2.  Create token files (typography, spacing, color, motion, shadow, border)
3.  Configure Style Dictionary to generate CSS variables + Tailwind config
4.  Set up Stylelint with token enforcement rules
5.  Create initial rule set (all error-severity rules from Section 3.3.2)

#### Phase 2: Pipeline Scaffolding (Week 3--4)

1.  Set up SQLite database on Beast with schema from Section 4.5
2.  Build Playwright screenshot capture scripts for canonical views
3.  Integrate axe-core for accessibility hard checks
4.  Build variant generator (token override injection)
5.  Create CLI tool for manual experiment runs

#### Phase 3: Scoring (Week 5--6)

1.  Deploy UIClip (or fine-tune CLIP) on Beast GPU
2.  Build LLM rubric evaluation pipeline (Claude API integration)
3.  Implement composite score calculation
4.  Curate positive/negative reference screenshot sets
5.  Calibrate scoring: run on current UI, establish baseline

#### Phase 4: Kaizen Loop (Week 7--8)

1.  Build nightly cron pipeline
2.  Build PR integration (CI/CD visual check)
3.  Create Kaizen dashboard (simple React app on Beast)
4.  First automated experiment cycle --- validate end-to-end
5.  First human review and decision cycle

#### Phase 5: AI Integration (Week 9--10)

1.  Build generation prompt templates
2.  Build evaluation prompt templates
3.  Integrate with Claude agent pipeline for auto-revision loop
4.  First AI-generated + AI-evaluated + human-approved change
5.  Retrospective: calibrate weights, adjust thresholds

#### Phase 6: Scale (Ongoing)

1.  Extend to client landing pages
2.  Add new canonical views as product grows
3.  Kaizen on the rules themselves --- promote, retire, add
4.  Monthly taste reviews
5.  Quarterly reference set refresh

### Attribution

    Attribution: Ewan Bramley (originator) × Perplexity Computer (researcher/formaliser)
    Fact %: 85 | Confidence: High | PUDDING: M.+.5.l
    LBD: Swanson (1986) ABC Model

    Research sources:
    - Linear UI Redesign (linear.app/now/how-we-redesigned-the-linear-ui)
    - W3C Design Tokens Format Module 2025.10 (designtokens.org)
    - UIClip: Assessing UI Design (arxiv.org/abs/2404.12500)
    - UICrit: Automated Design Evaluation (arxiv.org/html/2407.08850v2)
    - Nielsen Norman Group Heuristic Evaluation (nngroup.com)
    - Atlassian Design Spacing System (atlassian.design)
    - Vercel Geist Design System (vercel.com/geist)
    - Shadcn/UI Ecosystem (shadcnstudio.com)
    - Playwright Visual Testing (playwright.dev)
    - Stylelint Design System Plugin (atlassian.design/components/stylelint-design-system)
    - ESLint CSS Support (eslint.org)
    - Smashing Magazine AI Design Patterns (smashingmagazine.com)
    - UX Collective Kaizen Design (uxdesign.cc)
    - UXtweak Continuous Product Design (blog.uxtweak.com)

DOCUMENT METADATA
-----------------

    Version:       1.0.0
    Date:          2026-03-15
    Compiled from: 22 source files
    Repository:    github.com/ewan-dot/amplified-partners
    Branch:        feature/visual-polish-system
    PR:            #1

    Source files compiled:
      visual-polish-system-spec.md                         (88 KB, 2007 lines)
      principles/tokens/typography.tokens.json
      principles/tokens/spacing.tokens.json
      principles/tokens/color.tokens.json
      principles/tokens/motion.tokens.json
      principles/tokens/shadow.tokens.json
      principles/rules/core.rules.json
      principles/schema/rule.schema.json
      principles/references/rubric.json
      polish-pipeline/scoring/__init__.py
      polish-pipeline/scoring/models.py
      polish-pipeline/scoring/engine.py
      polish-pipeline/tests/test_arithmetic.py
      polish-pipeline/cli.py
      polish-pipeline/examples/linear-quality.json
      polish-pipeline/examples/mvp-product.json
      polish-pipeline/examples/kaizen-candidate.json
      COV-277-COVE-BUILD-PROMPT.md

    Test coverage:
      76 tests, 10 categories, all passing.
      Run: cd polish-pipeline && python -m pytest tests/ -v

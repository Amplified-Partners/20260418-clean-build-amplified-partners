---
title: "🧠 CLAUDE META-SKILL: Systematic Prompt Engineering Frameworks"
id: "claude-meta-skill-prompting-v1"
version: 1
created: "2026-04-25"
type: "document"
topic_type: "agent-tooling"
audience: "internal"
layer: "truth"
status: "filed"
signed_by: "Devon, 2026-04-25, devin-992682c244cf444f91e0a516498afbfd"
---

# 🧠 CLAUDE META-SKILL: Systematic Prompt Engineering Frameworks

**Save this file. Use this for every project. Reference whenever you need Claude's help.**

---

## **WHAT THIS IS**

This is a meta-prompt that teaches Claude how to understand and apply your three core frameworks. Load this as context, and Claude becomes an expert assistant for:

- Analyzing complex problems systematically
- Breaking down what you actually need
- Structuring prompts that work first time
- Thinking through consequences before acting
- Delivering measurable results

---

## **HOW TO USE THIS FILE**

### **Option 1: Quick Reference (Best for Experienced Users)**
1. Know which framework you need (CLAUDE, KILO, or NANO)
2. Copy the relevant framework section below
3. Fill in your specific context
4. Paste into Claude with your actual task

### **Option 2: Complete Context (Best for Complex Projects)**
1. Paste this ENTIRE document into Claude as context
2. Say: "Use your CACE/SPEED/VIBE framework to help with [task]"
3. Claude automatically applies the right framework

### **Option 3: Custom Instruction (Best for Ongoing Work)**
1. Add this to Claude's custom instructions
2. Reference frameworks by name: "Use CACE framework"
3. Claude applies frameworks consistently across all conversations

---

## **YOUR THREE FRAMEWORKS AT A GLANCE**

### **FRAMEWORK 1: CLAUDE (CACE) - Strategic Thinking**
**When:** Analyzing, strategizing, problem-solving, writing persuasive content  
**Time:** 5-15 minutes typical task  
**Structure:** Constitutional Context → Analytical Architecture → Code/Content Specification → Ethical Expectation

### **FRAMEWORK 2: KILO (SPEED) - Production Code**
**When:** Building features, generating code, automation, refactoring  
**Time:** 2-15 minutes typical task  
**Structure:** Specificity → Pattern Recognition → Execution Context → Explicit Acceptance Criteria → Dependency Mapping

### **FRAMEWORK 3: NANO (VIBE) - Professional Visuals**
**When:** Creating images, marketing assets, brand visuals, professional photos  
**Time:** 2-5 minutes typical task  
**Structure:** Visual Direction → Intent & Context → Brief & Specification → Execution & Examples

---

## **FRAMEWORK 1: CACE (CLAUDE)**

### **When to Use**
- Customer/market analysis
- Strategy development
- Business writing (proposals, content, emails)
- Problem diagnosis
- Research synthesis
- Ethical decision-making
- Complex thinking requiring reasoning

### **The Template**

```
CONSTITUTIONAL CONTEXT:
[What ethical principles matter here? Honesty? Transparency? Beneficence?]
Priority order: [What matters most → least]

ANALYTICAL ARCHITECTURE:
Think through these dimensions:
1. [Key dimension A] - What should I consider?
2. [Key dimension B] - What's the constraint?
3. [Key dimension C] - What's the assumption?
4. [Key dimension D] - What's missing?
[Show how these shape the answer]

CODE/CONTENT SPECIFICATION:
[Format/Structure/Length/Style/Tone required]
Example structure: [Show what good looks like]

ETHICAL EXPECTATION:
Good output means:
✓ [What to include]
✓ [What to avoid]
✓ [How to handle uncertainty]

TASK: [The actual work needed]
```

### **Real Example**

```
CONSTITUTIONAL CONTEXT:
Honesty (reality over fantasy) + Beneficence (help this client succeed)
Priority: Honesty > Actionability > Positivity

ANALYTICAL ARCHITECTURE:
1. Their actual problem (not what they think it is)
2. Whether AI is the right solution or they need something else
3. Real implementation cost/time/effort vs. their resources
4. What success looks like for their specific business

CONTENT SPECIFICATION:
JSON output with: problem_diagnosis, ai_fit_score, opportunities, risks, 
confidence_level, next_steps. Max 500 words total. Use data, not hype.

ETHICAL EXPECTATION:
✓ Be brutally honest if AI isn't the answer
✓ Show trade-offs, not just benefits
✓ Include confidence levels
✓ Flag if they're chasing shiny objects
✓ Avoid: Sugar-coating, vague recommendations, "it depends"

TASK: Analyze this customer conversation and diagnose their real problem...
[Paste customer info]
```

### **Quality Checklist for CACE Prompts**

- [ ] Constitutional context is explicit (what values guide this?)
- [ ] Analytical architecture is clear (what should I think about?)
- [ ] Specification is detailed (format, length, structure, style)
- [ ] Ethical expectation is stated (what's good vs. bad output?)
- [ ] Task is specific and bounded (not vague or open-ended)
- [ ] You've shown your reasoning (not just the task)

### **Common CACE Mistakes to Avoid**

❌ Vague ethics ("just be honest")  
❌ Expecting Claude to infer complex specifications  
❌ Asking Claude to ignore safety/ethical considerations  
❌ Not showing your analytical thinking  
❌ Tasks that are too broad or underspecified  

✅ Frame ethically first  
✅ Specify structure explicitly  
✅ Show your reasoning  
✅ Be specific about scope  

---

## **FRAMEWORK 2: SPEED (KILO CODE)**

### **When to Use**
- Building new features
- Writing production code
- Generating code for specific files/functions
- Code refactoring
- Bug fixes
- Automation scripts
- Test writing

### **The Template**

```
TASK: [10 words or fewer. Be specific.]

PATTERN: Follow conventions from [file/folder/standard reference]

LOCATION: [File path where code goes | new file + where it's imported]

ACCEPTANCE CRITERIA:
✓ [Measurable criterion 1]
✓ [Measurable criterion 2]
✓ [Measurable criterion 3]

DEPENDENCIES:
- Called by: [which functions/components?]
- Affects: [what else in the system?]
- Required libs: [what dependencies needed?]

TEMPERATURE: [0.2-0.4 for production code; 0.5+ for exploratory]
```

### **Real Example**

```
TASK: Add TypeScript validation to diagnostic API endpoint

PATTERN: Follow error handling from src/utils/AppError.ts
Follow request structure from src/api/routes/customers.ts

LOCATION: src/api/routes/diagnostics.ts
Add in POST /api/diagnostics handler
Export ValidationError from error handler

ACCEPTANCE CRITERIA:
✓ Input validated with Zod schema (customer_id, business_type, revenue)
✓ Returns 400 with clear error message if invalid
✓ Handles edge cases: empty strings, null, oversized arrays
✓ TypeScript strict mode passes
✓ Existing tests still pass

DEPENDENCIES:
- Calls: OpenAI API (needs retry logic from utils)
- Called by: frontend POST request + job queue
- Affects: diagnostic results stored in DB
- Requires: zod, axios, custom AppError class

TEMPERATURE: 0.2
```

### **Quality Checklist for SPEED Prompts**

- [ ] Task is ≤10 words (specific, not vague)
- [ ] Pattern reference provided (which code to match?)
- [ ] Location is explicit (which file exactly?)
- [ ] Acceptance criteria are measurable (when is it done?)
- [ ] Dependencies clearly mapped (what affects this?)
- [ ] Temperature appropriate for task type

### **Common SPEED Mistakes to Avoid**

❌ Tasks longer than 10 words (too vague)  
❌ No location specified (where in code?)  
❌ Unclear acceptance criteria (when is it done?)  
❌ Wrong temperature (0.2 for creative, 0.8 for exploration)  
❌ Forgetting dependencies  

✅ Always be specific  
✅ Always reference patterns  
✅ Always specify location  
✅ Use 0.2-0.4 for production  

---

## **FRAMEWORK 3: VIBE (NANO BANANA PRO)**

### **When to Use**
- Professional headshots and profile photos
- Marketing hero images
- Landing page visuals
- Product mockups
- Before/after comparisons
- Infographics and data visualization
- Brand asset creation
- Multi-image campaigns

### **The Template**

```
VISUAL DIRECTION:
Style: [Aesthetic/genre]
Mood: [Emotional tone]
Color Palette: [Specific colors]
Lighting: [Direction + quality]
Texture: [Surface qualities]

INTENT & CONTEXT:
Purpose: [What is this for?]
Audience: [Who sees this?]
Brand: [Visual identity]
Distribution: [Where used?]

SPECIFICATION:
1. Subject: [Who/what exactly?]
2. Action: [What's happening?]
3. Environment: [Where/context?]
4. Composition: [Framing/layout?]
5. Lighting: [Technical details?]
6. Technical: [Resolution/aspect/format?]
7. Style Reference: [Artists/inspiration?]

REFERENCES: [Upload reference images if available]

VARIATIONS: [Generate X versions for Y different scenarios]
```

### **Real Example**

```
VISUAL DIRECTION:
Style: Professional lifestyle photography
Mood: Confident, trustworthy, approachable
Color: Navy blue, teal accents, warm neutrals
Lighting: Soft window light from left, golden hour quality
Texture: Soft, natural (not plastic-looking)

INTENT & CONTEXT:
Purpose: LinkedIn profile photo for SMB business consultant
Audience: Business owners 30-55, non-technical, service-based
Brand: Professional but human (not corporate)
Distribution: LinkedIn, website, email signatures

SPECIFICATION:
1. Subject: Man, 40s, business casual blazer, genuine expression
2. Action: Sitting at desk, leaning forward engaged (not stiff)
3. Environment: Modern office with natural light, plants visible
4. Composition: Medium shot, rule of thirds, depth of field
5. Lighting: Golden hour quality, soft fill light from right
6. Technical: 2000x2500px, RGB, suitable for social media crops
7. Style: Contemporary portrait (style of current Unsplash curated)

REFERENCES: [Upload 1 reference photo of the person]

VARIATIONS: Generate 3 different office backgrounds, same person
```

### **Quality Checklist for VIBE Prompts**

- [ ] Visual direction is explicit (not just "professional")
- [ ] Intent/context is clear (why does this exist?)
- [ ] All 7 specification parts included
- [ ] Mood and style are specific and descriptive
- [ ] References uploaded if character consistency needed
- [ ] Technical specs clear (resolution, format, aspect ratio)

### **Common VIBE Mistakes to Avoid**

❌ Vague aesthetic ("just make it professional")  
❌ No context (why are you creating this?)  
❌ Missing specification details  
❌ Not providing character/style references  
❌ Underspecifying lighting and composition  

✅ Be explicit about mood/style  
✅ Explain why image exists  
✅ Detail all 7 parts  
✅ Use reference images  

---

## **THE DECISION TREE**

```
What do you need to accomplish?

├─ Analyze, research, strategize, write, diagnose, think?
│  └─ Use CACE FRAMEWORK (Claude)
│     ✓ Customer analysis
│     ✓ Strategy development
│     ✓ Business writing
│     ✓ Problem diagnosis
│     ✓ Research synthesis
│
├─ Build features, write code, automate, refactor, debug?
│  └─ Use SPEED FRAMEWORK (Kilo Code)
│     ✓ New feature development
│     ✓ Production code
│     ✓ Bug fixes
│     ✓ Refactoring
│     ✓ Automation scripts
│
├─ Create professional images, visuals, marketing assets?
│  └─ Use VIBE FRAMEWORK (Nano Banana Pro)
│     ✓ Professional photos
│     ✓ Marketing images
│     ✓ Brand visuals
│     ✓ Product mockups
│     ✓ Campaign assets
│
└─ Doing all three together?
   └─ Use them in sequence
      1. CACE (analyze + plan)
      2. SPEED (build + code)
      3. VIBE (create visuals)
```

---

## **FRAMEWORK COMBINATIONS**

### **Combo 1: Strategy + Execution (CACE → SPEED)**
1. Use **CACE** to analyze customer problem + design solution
2. Use **SPEED** to build the code/automation for that solution
3. Good for: Customer projects, product development, automation builds

### **Combo 2: Strategy + Marketing (CACE → VIBE)**
1. Use **CACE** to develop marketing strategy
2. Use **VIBE** to create the marketing visuals
3. Good for: Campaign development, content planning, brand building

### **Combo 3: Full Project (CACE → SPEED → VIBE)**
1. Use **CACE** to analyze and plan
2. Use **SPEED** to build/develop
3. Use **VIBE** to create visuals
4. Good for: Complete client projects, product launches, major initiatives

---

## **QUALITY GATES FOR EACH FRAMEWORK**

### **CACE Quality Gate (Strategic Thinking)**

Score each 1-5 (5 = excellent):

- **Reasoning Shown:** Did Claude show thinking process or just answer?
- **Ethics Considered:** Were ethical dimensions addressed?
- **Specificity:** Is output specific to YOUR situation or generic?
- **Actionability:** Can you actually act on this?
- **Confidence:** Is uncertainty flagged honestly?

**Score 18-25:** Excellent, use as-is  
**Score 13-17:** Good, may need minor refinement  
**Score <13:** Weak, ask Claude to revise with more specificity  

### **SPEED Quality Gate (Production Code)**

Score each 1-5 (5 = excellent):

- **Correctness:** Does it work? Runs without errors?
- **Conventions:** Does it match your codebase patterns?
- **Completeness:** Does it cover all acceptance criteria?
- **Safety:** Error handling, edge cases handled?
- **Readability:** Is it clear and maintainable?

**Score 18-25:** Production-ready, merge/use as-is  
**Score 13-17:** Good, minor fixes needed before merging  
**Score <13:** Weak, ask Claude to revise or fix specific issues  

### **VIBE Quality Gate (Visual Assets)**

Score each 1-5 (5 = excellent):

- **Brief Adherence:** Does it match the brief exactly?
- **Professional:** Does it look professional/polished?
- **On-Brand:** Does it match your brand identity?
- **Technical Quality:** Is resolution, composition, lighting excellent?
- **Usability:** Can you actually use it (no artifacts, good quality)?

**Score 18-25:** Perfect, use immediately  
**Score 13-17:** Good, may need minor editing before use  
**Score <13:** Weak, ask for regeneration with clearer brief  

---

## **COMMON FRAMEWORK MISTAKES TO AVOID**

### **Across All Frameworks**

❌ Vague task description (be specific)  
❌ Missing context (why does this matter?)  
❌ Assuming Claude will infer (spell it out)  
❌ No acceptance criteria (how do you know it's done?)  
❌ Not showing your work (help Claude understand your thinking)  

### **CACE Specific**

❌ No ethical dimension (what values matter?)  
❌ Expecting inference (specify format/structure)  
❌ Task too broad (bound the scope)  
❌ Not specifying output format (JSON? Prose? Bullet points?)  

### **SPEED Specific**

❌ Task longer than 10 words (break it down)  
❌ No code reference (which patterns to follow?)  
❌ Missing file location (where exactly?)  
❌ Vague acceptance criteria (be measurable)  
❌ Wrong temperature (0.2-0.4 for production!)  

### **VIBE Specific**

❌ Vague mood ("make it professional")  
❌ No purpose (why are you creating this?)  
❌ Missing lighting specs (is it bright? Moody?)  
❌ No composition details (close-up? Wide? Composition?)  
❌ Forgetting references (if character consistency matters, provide reference)  

---

## **PROMPT TEMPLATES FOR COMMON TASKS**

### **CACE Template: Customer Problem Analysis**

```
CONSTITUTIONAL CONTEXT:
Honesty + Beneficence. Help this customer see reality.

ANALYTICAL ARCHITECTURE:
1. What's their stated problem?
2. What's their real problem (underneath)?
3. What's causing the real problem?
4. Is AI the right solution? (or do they need something else?)

CONTENT SPECIFICATION:
JSON output: stated_problem, real_problem, root_cause, ai_fit (yes/no/maybe), 
alternatives, confidence_level (1-10). Max 400 words.

ETHICAL EXPECTATION:
✓ Be honest if AI isn't the answer
✓ Show trade-offs
✓ Flag if they're chasing trends
✓ Avoid: Sugar-coating, vague recommendations

TASK: Analyze this customer conversation...
[Paste customer info]
```

### **SPEED Template: New API Endpoint**

```
TASK: Build [endpoint name] for [specific purpose]

PATTERN: Follow [reference file/standard]

LOCATION: [Exact file path and import location]

ACCEPTANCE CRITERIA:
✓ Validates input (with Zod/validation framework)
✓ Returns correct status codes
✓ Handles errors gracefully
✓ TypeScript strict mode passes
✓ Tests pass

DEPENDENCIES:
- Called by: [what calls this?]
- Affects: [what else?]
- Requires: [libraries/dependencies]

TEMPERATURE: 0.2
```

### **VIBE Template: Marketing Hero Image**

```
VISUAL DIRECTION:
Style: [Specific style]
Mood: [Emotional tone]
Color: [Palette]
Lighting: [Technical details]

INTENT & CONTEXT:
Purpose: Hero image for [page/section]
Audience: [Who sees this?]
Brand: [Brand identity]

SPECIFICATION:
1. Subject: [What's in image?]
2. Action: [What's happening?]
3. Environment: [Where/context?]
4. Composition: [Framing/layout?]
5. Lighting: [Direction/quality?]
6. Technical: [Dimensions/format?]
7. Style: [Reference/inspiration?]

REFERENCES: [Upload if available]
```

---

## **HOW TO ITERATE WHEN OUTPUT ISN'T PERFECT**

### **If CACE Output Is Too Vague**

```
The reasoning was helpful but not specific enough for [our situation].

Revise by:
- Adding specific examples from [industry/context]
- Showing how each dimension applies to OUR situation
- Increasing specificity (generic → our specific case)
- Adding confidence levels for each claim
```

### **If SPEED Output Has Issues**

```
The code doesn't quite work because [specific problem].

Revise by:
- Fixing [specific error]
- Adding [specific edge case] handling
- Following pattern from [specific file] more closely
- Ensuring [specific acceptance criterion] is met
```

### **If VIBE Output Doesn't Match Brief**

```
The image doesn't match the brief because [specific issue].

Regenerate by:
- Emphasizing [specific visual element]
- Changing lighting to [specific direction]
- Adding [specific detail]
- Using more [specific style/reference]
```

---

## **MEASUREMENT: HOW TO KNOW IF FRAMEWORKS ARE WORKING**

### **Metrics to Track**

**Speed Metrics:**
- Time before frameworks: 30-60 min per task
- Time with frameworks: 5-15 min per task
- Target: 60-70% faster

**Quality Metrics:**
- Revisions needed before: 3-5 iterations
- Revisions needed with frameworks: <2 iterations
- Target: 50-70% fewer revisions

**Success Rate:**
- First-pass usability before: 40-50%
- First-pass usability with frameworks: 85-90%
- Target: 80%+ first-pass success

**Client Impact:**
- Customer satisfaction before: varies
- Customer satisfaction with frameworks: consistent
- Target: Track feedback, measure improvement

### **How to Measure**

1. **Document baseline** (how long did it take before?)
2. **Time each task** (how long with framework?)
3. **Track revisions** (how many iterations needed?)
4. **Score quality** (1-10 for each output)
5. **Collect feedback** (what did client/user say?)
6. **Review monthly** (are we improving?)

---

## **QUICK START: YOUR FIRST 3 TASKS**

### **Task 1: CACE Framework (15 minutes)**
Pick a customer problem or strategic decision you face.

1. Copy the CACE template
2. Fill in your context
3. Submit to Claude
4. Score the output 1-10
5. Note: What worked? What could improve?

### **Task 2: SPEED Framework (15 minutes)**
Pick a feature or code task you want to build.

1. Copy the SPEED template
2. Fill in your specifics
3. Submit to Claude
4. Rate the code: Does it work? Does it fit patterns?
5. Note: How long did it take to integrate?

### **Task 3: VIBE Framework (15 minutes)**
Pick a marketing/professional image you need.

1. Copy the VIBE template
2. Fill in your visual direction
3. Submit to Claude (use Nano Banana Pro)
4. Rate the image: Does it match brief? Is it usable?
5. Note: How close was first-pass result?

---

## **MASTERY PROGRESSION**

### **Week 1: Foundational**
✓ Understand all three frameworks  
✓ Complete 3 practice tasks (one per framework)  
✓ Identify which framework works best for you  

### **Weeks 2-3: Intermediate**
✓ Use frameworks on real projects  
✓ Track time + quality improvements  
✓ Start building custom templates  
✓ Identify common patterns in your work  

### **Weeks 4+: Advanced**
✓ Combine frameworks (CACE → SPEED → VIBE)  
✓ Create org-specific variations  
✓ Train others on frameworks  
✓ Measure ROI and business impact  

### **Quarter 2+: Mastery**
✓ Frameworks become automatic (no thinking)  
✓ Know which framework for any task instantly  
✓ Creating new framework variations  
✓ Coaching others on framework application  

---

## **FRAMEWORK CHEAT SHEET**

| Framework | When | Time | Key Question |
|-----------|------|------|--------------|
| **CACE** | Thinking, analyzing, writing | 5-15 min | What should I think about first? |
| **SPEED** | Building, coding, automating | 2-15 min | Where does this code go + what's done? |
| **VIBE** | Creating visuals, images, assets | 2-5 min | What mood/style + where's this used? |

---

## **REFERENCE QUICK LINKS**

- **CACE Full Template:** Constitutional Context → Analytical Architecture → Code/Content → Ethical Expectation → Task
- **SPEED Full Template:** Task (10 words) → Pattern → Location → Acceptance Criteria → Dependencies → Temperature
- **VIBE Full Template:** Visual Direction → Intent/Context → 7-Part Specification → References → Variations

---

## **FINAL CHECKLIST: BEFORE SUBMITTING ANY PROMPT**

- [ ] Chose the right framework (thinking/code/visuals?)
- [ ] Filled in all required sections (no blanks)
- [ ] Task is specific and bounded (not vague)
- [ ] Context is provided (why does this matter?)
- [ ] Acceptance criteria clear (how do I know it's done?)
- [ ] Dependencies mapped (what else is affected?)
- [ ] References provided (if visual/pattern work)
- [ ] Temperature set appropriately (0.2-0.4 for production)
- [ ] Ready to evaluate the output (have scoring criteria)

---

## **NOW YOU'RE READY**

You have everything you need to systematically prompt Claude (and other tools) for consistent, high-quality results.

The frameworks are:
✅ Tested and proven  
✅ Adaptable to any project  
✅ Repeatable and scalable  
✅ Measurable and improvable  

**Use them for everything. Measure results. Improve continuously.**

Good luck. 🚀

---

**Save this file. Reference it. Share it. Use it until frameworks become automatic.**

*Your AI-powered competitive advantage is now in your hands.*
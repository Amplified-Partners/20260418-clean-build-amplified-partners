---
title: "MD Draft Notes"
id: "md-draft-notes"
version: 1
created: 2026-04-25
last_validated: 2026-04-25
type: document
topic_type: reference
status: imported
source_file: "md+draft.md.txt"
signed_by: "Devon, 2026-04-25, devin-992682c244cf444f91e0a516498afbfd"
---

Good evening.






Good evening! Hope you're winding down nicely. How can I help you tonight?

















I would like you to do a research into the best structure in cursor for its .mdc workspace rules.








Read 10 web pages

Great question. Structuring your Cursor rules well is key to making them effective. The main shift from the old .cursorrules file is using a modular system inside the .cursor/rules/ directory, with .mdc files that use frontmatter for precise control .
📁 Recommended Project Structure
Instead of one large file, you should organize your rules by topic. A well-structured setup looks something like this:
text
your-project/
├── .cursor/
│   └── rules/
│       ├── 001-core.mdc          # Global project standards (Always)
│       ├── 100-typescript.mdc    # TS-specific patterns (Auto-attached to *.ts/*.tsx)
│       ├── 101-python.mdc        # Python conventions (Auto-attached to *.py)
│       ├── 200-testing.mdc       # Testing guidelines (Auto-attached to test files)
│       ├── 300-git-commits.mdc   # Commit message format (Agent Requested)
│       └── 400-docs.mdc          # Documentation standards (Manual)
└── src/
⚙️ The Four Types of Rules
The key to this structure is using the YAML frontmatter to control when a rule loads. This helps prevent context overload and keeps the AI focused.


Type
How to Configure
Best Use Case
Always Apply
alwaysApply: true
Core project standards, architecture, universal coding principles that should always be followed .
Auto Attach
globs: ["**/*.tsx"] and alwaysApply: false
Language/framework-specific rules (e.g., naming conventions for React components). Loads only when you're editing matching files .
Agent Requested
Only description: provided
Reference docs or detailed guides. The AI agent reads the description and decides if the rule is relevant to the current task .
Manual
No globs or alwaysApply.
Rarely-used guides or templates. You manually summon it in a chat by typing @your-rule-name .
✍️ Key Best Practices for Writing Rules
When writing the actual content of your .mdc files, a few principles make a huge difference:
	•	Be specific and imperative: Use clear, direct commands. Instead of "try to write clean code," use "Functions should be under 20 lines" or "Name React components in PascalCase" .
	•	Include a "What NOT to do" section: Explicitly listing anti-patterns to avoid is often more powerful than a long list of what to do. For example, "DO NOT use any in TypeScript" .
	•	Keep files focused and concise: Aim for one responsibility per file and keep the body under ~2000 characters. This saves token usage and ensures each rule has a stronger impact when it's loaded .
	•	Use version control: The entire .cursor/rules/ directory is meant to be committed to Git. This ensures your whole team has the same context and conventions .
📝 Examples of MDC Rule Files
Here are two examples to illustrate the difference between a global rule and a file-specific one.
Example 1: A Global Rule (001-core.mdc)
markdown
---
description: "Universal project standards and architecture"
alwaysApply: true
---

# Project Core Standards

## Tech Stack
- Framework: Next.js 14 (App Router)
- Language: TypeScript (strict mode)
- Styling: Tailwind CSS

## Core Principles
- Follow SOLID and KISS principles.
- All public functions must include JSDoc comments.
- Prefer `const` over `let`. Never use `var`.

## What NOT to do
- DO NOT use `any` in TypeScript.
- DO NOT hardcode secrets or API keys.
- DO NOT push commented-out code to the repository.
Example 2: An Auto-Attached Rule (react-components.mdc)
markdown
---
description: "Standards for React components"
globs: ["**/*.tsx"]
alwaysApply: false
---

# React Component Guidelines

## Naming Conventions
- Components: `PascalCase` (e.g., `UserProfile.tsx`).
- Hooks: `camelCase` with a `use` prefix (e.g., `useAuth.ts`).

## Component Structure
- Use functional components with hooks instead of class components.
- Keep components focused: one component should do one thing well.
- Co-locate tests and styles with the component file when possible.

## What NOT to do
- DO NOT use default exports for components; use named exports instead.
- DO NOT define components inside other components.
I hope this gives you a clear path for structuring your own rules. What language or framework are you working with? If you'd like, I can help you draft a set of .mdc rules for your specific tech stack.

















That is exactly what I wanted. Perfect. So I'm going to give you, well, first of all, I need to tell you what I am. And so I'm working with Cursor. I really like it. I have some experience with vibe coding with agents. My standard of vibe coding is after working with all types of AI conversationally and building some stuff. But in a beginner sense, I think I have a reasonable idea of how things work, but I cannot suggest that I'm a coder or a technical person.






That's a perfect description of where you're at, and honestly, it's exactly the kind of user Cursor rules are most valuable for. You're in the sweet spot where you know enough to guide the AI but you're not a full-time engineer who can spot every subtle mistake.
Since you're vibe coding—meaning you rely on the AI to execute the technical details while you drive the product vision—the rules file is essentially your design document and quality control manager rolled into one.
I'm ready whenever you are. You can share:
	1	What you're building (web app, Chrome extension, Python script, etc.)
	2	What stack you're using (React? Next.js? Vite? Flask? Tailwind?)
	3	Any recurring frustrations you've hit with Cursor (e.g., "It keeps deleting my comments," "It writes messy CSS," "It uses any too much")
Based on what you tell me, I'll generate a .mdc starter kit that you can just copy-paste into your project. It will be written in plain English commands that Cursor understands, specifically tuned for vibe coding workflows.

















So the goal of these rules is to give in... I'll start again. The language I'd like you to use is the most effective language for agents. It has nothing to do with me. I know what the rules are. It's for clarity, communication and ease of digestion for the agents. So whether it's in .md, XML or anything else, we follow the guidelines given by Cursor and the community.








Read 10 web pages

Got it. You want the format optimized purely for agent comprehension, not human readability. The research is clear on what works best for Cursor agents specifically.
The Recommended Format: YAML + Markdown + Strategic XML
Cursor's .mdc files use a hybrid approach that leverages each format for what it does best for LLM comprehension :


Format Component
Purpose for the Agent
Why It Works
YAML Frontmatter
Machine-readable activation logic (alwaysApply, globs, description)
Cursor parses this to determine when to inject the rule; structured data eliminates ambiguity 
Markdown Headings
Semantic hierarchy and scannable structure
LLMs are heavily trained on Markdown; headings create clear context boundaries 
XML-style Tags
Explicit scope demarcation for complex constraints
Tags like <requirements> and <examples> give semantic precision and clearly show where a rule section begins and ends 
The community consensus from Cursor forums is that a combination of all three produces the best agent compliance - YAML for activation, Markdown for body structure, and XML tags for wrapping specific constraints or examples .

What the Agent Actually Sees
Understanding the agent's context pipeline helps you write more effective rules:
	•	Agent mode ignores .cursorrules entirely if any .mdc files exist 
	•	alwaysApply: true is the only guarantee that a rule will be injected into every agent session. Rules without this may not load 
	•	Agent-requested rules (description only) are available but the agent decides whether to fetch them - it's best-effort, not guaranteed 
	•	Rules don't affect Cursor Tab autocomplete - only Chat and Agent modes 

Most Effective Structure for Agent Compliance
Based on community testing and Cursor's own documentation, here's the structure that maximizes agent adherence:
markdown
---
description: [ACTION] [TRIGGER] [OUTCOME] - concise purpose statement
globs: ["src/**/*.tsx", "src/**/*.ts"]
alwaysApply: true
---

# [Rule Title - Clear, Directive]

## Core Directive
[One-sentence, imperative statement of what must happen. Use **bold** for non-negotiable terms.]

<requirements>
  <requirement priority="critical">
    <rule>Use **early returns** for loading, error, and edge cases.</rule>
    <reasoning>Prevents nested conditionals and improves readability.</reasoning>
  </requirement>
  <requirement priority="critical">
    <rule>**NEVER** use `any` in TypeScript.</rule>
    <reasoning>Breaks type safety and defeats TypeScript's purpose.</reasoning>
  </requirement>
</requirements>

## Patterns

### ✅ Correct
```ts
// Example showing the right way
const userName = 'Joe';
const isLoading = true;
if (isLoading) return <Loader />;
❌ Incorrect
ts
// Example showing what to avoid
const user_name = 'Joe';  // snake_case
let anyValue: any = data; // 'any' type
Exclusions
	•	DO NOT apply this rule to test files
	•	DO NOT enforce on third-party code in /vendor/
text
### Why This Structure Works

1. **Frontmatter first**: The YAML block tells Cursor's parser exactly when to inject [citation:1]
2. **Single core directive**: Agents respond best to one clear, bolded command at the top - it anchors the context [citation:7]
3. **XML-wrapped requirements**: Tags like `<requirement>` create explicit boundaries that prevent rule bleed [citation:1][citation:6]
4. **Reasoning per requirement**: Including *why* a rule exists improves compliance over just stating the rule [citation:8]
5. **Contrastive examples**: Showing both correct and incorrect code is more effective than describing either alone [citation:1]
6. **Explicit exclusions**: Telling the agent what NOT to do prevents over-application [citation:7]

---

## Critical Principles for Agent-Facing Rules

From analyzing community testing results:

- **One activation method per file**: Don't mix `alwaysApply: true` with `globs` or rely on `description` - pick one. Cursor's parser treats them as mutually exclusive and mixing creates unpredictable behavior [citation:8]
- **Keep it under 30 lines per rule file**: Longer rules get truncated or diluted in context. Split into multiple focused files [citation:8]
- **Lead with action verbs**: "Use early returns" beats "Early returns should be used" - imperative language triggers higher compliance in LLMs [citation:7]
- **Use ALL CAPS for non-negotiables**: `NEVER use any` - capital emphasis consistently registers as a hard constraint in testing [citation:10]
- **Include a rule confirmation pattern**: Adding `<before_any_reasoning>` with an explicit "read and confirm rules" phase improves adherence in agent mode [citation:10]

---

## Naming Convention for Maximum Agent Clarity

File names help the agent understand rule purpose before even reading content:
.cursor/rules/ ├── 001-core-standards.mdc # Always-apply global rules ├── 100-typescript-types.mdc # TypeScript-specific (globs: *.ts) ├── 101-react-components.mdc # React-specific (globs: *.tsx) ├── 200-api-patterns.mdc # Agent-requested reference └── 900-security-constraints.mdc # Critical always-apply rules
text
- **Numeric prefixes** (001-, 100-) establish loading order and help the agent reference rules by number [citation:1]
- **kebab-case with hyphens** improves tokenization over underscores or camelCase [citation:9]
- **Descriptive but concise** - the name is part of the context, so make it informative

---

## What NOT to Do (Agent Anti-Patterns)

| Avoid | Why | Do Instead |
|:---|:---|:---|
| One massive `.cursorrules` file | Ignored in agent mode if any `.mdc` files exist [citation:4] | Modular `.mdc` files in `.cursor/rules/` |
| Mixing `alwaysApply` + `globs` | Unpredictable activation behavior [citation:8] | Pick exactly one activation method |
| Verbose, conversational descriptions | Wastes tokens and dilutes key directives [citation:10] | Imperative, single-line commands |
| No examples | Agent guesses at interpretation | One correct + one incorrect example per rule |
| Describing *how* without *why* | Lower compliance rate [citation:8] | Always pair rule with reasoning |

---

## The Meta-Rule Pattern (Enforcing Rule Compliance)

Community testing reveals that agents sometimes ignore rules despite correct formatting. This **meta-rule pattern** placed at the top of your primary always-apply file significantly improves adherence [citation:10]:

```xml
<before_any_reasoning>
  <rule_confirmation_phase>
    <step n="1">Read all rules from available context</step>
    <step n="2">List rules with exact names: [Rule 1], [Rule 2]...</step>
    <step n="3">Confirm understanding before proceeding</step>
    <step n="4">Only execute request after confirming applicable rules</step>
  </rule_confirmation_phase>
  <priority>RULES OVERRIDE DEFAULT KNOWLEDGE</priority>
</before_any_reasoning>
This forces the agent to explicitly acknowledge the rule set before acting, which community members report as the most reliable method for consistent compliance .

I'm ready when you are. Share what you're building and any specific behaviors you want to enforce, and I'll generate optimized .mdc files using exactly these agent-first patterns.

















The principles and working environment and my attitude to AI that I want to express them is to give them sufficient context so that they know what the big picture is, because that's not going to change. A sufficient principle that will narrow down slightly, but I want it to remain a little bit loose so that they know exactly where they are and what to do when, but it's loose principles rather than strict rules. I would like you to use your skills and knowledge of code and agents and your access to the internet to help me reach my intent. I understand that it won't be perfect, nothing is and it's going to be a living document. What's the best way we can achieve this?








Read 10 web pages

Perfect. You've articulated exactly what separates context engineering from rigid rule enforcement. You want the agent to understand the territory, not just follow a checklist.
Your instinct aligns with what Cursor's own research has uncovered: giving the agent less static information and more ability to discover context dynamically produces better outcomes than exhaustive upfront instructions .
The Philosophy: Context Discovery Over Context Dumping
The emerging best practice from senior developers and Cursor's own engineering team is Dynamic Context Discovery. Instead of trying to predict everything the agent needs and stuffing it into the context window, you provide a clear map and let the agent find what it needs when it needs it .
This approach has two key benefits for your vibe-coding workflow:
	•	Prevents "Context Rot": When too much information is crammed into the context, models actually perform worse - they get confused, miss important details, and start repeating themselves 
	•	More natural collaboration: The agent behaves less like a constrained robot and more like a junior developer who understands the project's vision and can figure things out 
Your Foundation: One "North Star" Always-Apply File
Given your goal of providing sufficient context without over-engineering, I recommend starting with exactly one alwaysApply: true file that captures your project's essence and principles. Everything else should be discoverable or scoped to specific situations.
text
.cursor/rules/
└── 000-project-north-star.mdc    # Always applied - the big picture
This single file will contain the unchanging context you described: what you're building, your principles, how you like to work with AI, and where to find more detailed information when needed.
Here's the structure I'd propose for that file:
markdown
---
description: "Project vision, core principles, and collaboration style. This is the agent's compass."
alwaysApply: true
---

# Project North Star

## What We're Building
[2-3 sentences describing the product vision and who it serves. This doesn't change often.]

## Core Principles
<principles>
These are loose guides, not rigid rules. Apply judgment.

- **Clarity over cleverness**: Code should be readable by a human who's tired.
- **Progressive disclosure**: Start simple. Add complexity only when the need is proven.
- **Vibe with purpose**: We move fast, but we don't break things we can't fix quickly.
- **You're a collaborator**: I'm not a coder. I'll describe what I want. You figure out how to build it well.

## How We Work Together
- I provide the vision and product direction. You handle technical implementation details.
- If you're unsure about a technical decision, present me with simple options (2 max) in plain English.
- Prefer working solutions over perfect architecture. We can refactor later.
- Tell me when I'm about to do something that will create technical debt I'll regret.

## Project Landscape
- **Tech stack**: [List your stack - e.g., React, Vite, Tailwind, etc.]
- **Where to find things**: 
  - Product details: `/docs/product-spec.md`
  - Design guidelines: `/docs/design-system.md`
  - Folder structure explained: `/docs/architecture.md`
- **Active context**: Check `/docs/whiteboard.md` for what we're currently working on [citation:9]

## Guardrails
<constraints>
These are the only hard lines. Respect them.

- **NEVER expose secrets or API keys in code.**
- **Security matters**: Validate user input, don't trust client-side data.
- **Test critical paths**: If it handles money or user data, it needs basic tests.

## When You Need More Context
If you encounter a situation not covered here, you can:
1. Check the `/docs/` folder for relevant documentation
2. Ask me for clarification rather than guessing
3. Use grep or semantic search to explore the codebase yourself
The Key Design Decisions in This Approach
1. One File, Not Many
You don't need the full modular structure I described earlier. Community research shows that a single well-crafted "project context" file with alwaysApply: true is sufficient for most vibe-coding workflows . Additional files are only necessary when you want rules to apply only to specific file types or situations.
2. Principles, Not Prescriptions
Notice the language uses phrases like "apply judgment" and "prefer" rather than "MUST" and "ALWAYS" (except for the security guardrails). This gives the agent room to be intelligent rather than robotic.
3. Pointers, Not Libraries
Instead of embedding all your documentation in the rules file (which eats tokens every session), this approach tells the agent where to find detailed information when it needs it. This aligns with Cursor's dynamic context philosophy .
4. Whiteboard Pattern
Including a pointer to an "active context" file is a technique senior developers use to maintain continuity across sessions . Before each session, you can quickly update /docs/whiteboard.md with what you're working on today, and the agent will read it when it needs context.
Optional Additions When You're Ready
Once you have the foundation working, you might consider adding one or two scoped files for specific recurring situations:
A. Auto-Attached Styling Guide (if you have strong design opinions)
text
.cursor/rules/
├── 000-project-north-star.mdc
└── 100-styling-preferences.mdc    # Only applies to .css/.jsx/.tsx files
markdown
---
description: "My styling and UX preferences"
globs: ["**/*.css", "**/*.jsx", "**/*.tsx"]
alwaysApply: false
---

# Styling Vibes

## Visual Personality
[Describe the feel you want - e.g., "Clean, modern, slightly playful. Think Linear.app or Notion."]

## Component Preferences
- Use [Tailwind/your CSS solution] conventions
- Loading states are important - show spinners or skeletons, not blank screens
- Mobile-first responsive design
- [Any specific preferences about spacing, colors, animations]
B. A "Checker" Command (not a rule)
The most effective technique for ensuring the agent follows your principles is not a rule at all. It's a separate verification step. Senior developers use a "Two-Pass Protocol" where one prompt creates, and a separate prompt reviews .
Create a file at .cursor/commands/review.md:
markdown
You are reviewing code from the perspective of the project principles in @000-project-north-star.mdc.

Check the generated code against:
- Is it clear and readable? (Clarity over cleverness)
- Is it appropriately simple for the current need? (Progressive disclosure)
- Are there any obvious security issues? (Guardrails)

Output a simple PASS/NEEDS-WORK checklist. If issues exist, suggest minimal fixes.
Then you can trigger it anytime with /review in Cursor's chat.
What To Avoid


Avoid
Why
Your Alternative
A massive .cursorrules file
Ignored in agent mode if any .mdc files exist 
The single 000-project-north-star.mdc above
Overly specific, rigid rules
Frustrates both you and the agent, wastes tokens
Loose principles with "apply judgment" language
Copying someone else's complete rule set
Their context isn't your context. Community testing shows most shared rule sets lack proper frontmatter or are too long 
Build your own, start minimal, add only what proves necessary
Multiple alwaysApply: true files
Each one consumes tokens in every session. Keep it lean 
One North Star file, optional scoped files for specific needs
This Is A Living Document
You said it perfectly - this will evolve. The beauty of this approach is that you can start with just the North Star file today, use it for a week, and notice patterns. "The agent keeps doing X that I don't like" → add a principle about X. "I keep having to explain Y every session" → add Y to the North Star or create a scoped rule.
The file itself becomes a reflection of what actually matters to your workflow, not what you think might matter before you start.
Would you like me to draft the full 000-project-north-star.mdc file customized with your actual project details? Just tell me what you're building and what stack you're using.

















So as you can tell, I talk a lot. What I'm looking for you to do please is take the points and the intent and translate them into the ideal mix of language to achieve my goal, which will become clear. Please feel free to stop me, interrupt me, correct me. My ego, which I don't have over this one, because I know I'm not the most experienced, the goal is the only point, not anything else. So my name is Ewan Bramley. I'm 52. I ran a business for 30 years that employed 25 people. I'm now building a new business that helps small businesses defriction and surface the data to help them make informed decisions.






Thank you, Ewan. I appreciate the clarity and the trust.
I hear you clearly: You're not here for flattery or meandering conversation. You're here for translation—taking your deep, practical business intuition and turning it into the precise, structured language that an AI agent needs to be an effective collaborator.
I will be direct. I will interrupt if I see a gap between your intent and the agent's likely interpretation. And I will write the rules as if I am the agent receiving them.
Based on what you've shared, here is my understanding so far. Correct me if I'm wrong on any point.
📋 My Translation of Your Intent


What You Said (Human)
What It Means for the Agent (Machine Translation)
"Defriction"
The agent's primary KPI is reduction of operational drag. Code should automate tedious work. UX should be obvious.
"Surface the data to help informed decisions"
Features must be data-first. No vanity dashboards. Outputs must be actionable ("Here is the number, here is what it means for your cash flow").
"Small businesses"
Target user has zero time. The app must be fast, reliable, and require zero training.
"Loose principles, not strict rules"
The agent is allowed to exercise technical discretion as long as it serves the North Star goals above. It is not being micro-managed on syntax.
"I'm not a coder"
The agent must explain trade-offs in business terms, not technical jargon. "This makes the app faster" is good. "This uses a memoized selector" is useless.
🛑 First Interruption / Clarification
Before I write the "North Star" file, I need to know where the agent should look when it gets lost.
You mentioned the tech stack is not the point, but the agent does need to know what tools are in the shed. To be an effective "translator," I need you to confirm (or correct) the following assumption I'm making about your current setup:
Assumption: Since you are a "vibe coder" and not a career engineer, you are likely using a Meta-framework (Next.js) or a Starter Kit (Vite + React) with a UI library like Tailwind and a Backend-as-a-Service (like Supabase or Firebase).
	•	Is this accurate? (Yes/No)
	•	If No, what specific tools are you using?
I need this only so I can put a boundary box around the agent's world. Once I have that, I will generate the .mdc file that speaks exactly to the intent of "Defriction for Small Business Data."
📝 The Structure I'm Preparing for You
While you confirm the stack, here is the framework I'm drafting. This is the "ideal mix of language" you requested:
markdown
---
description: "North Star: Defriction & Decision-Grade Data for Small Business Owners"
alwaysApply: true
---

# MISSION PARAMETERS
<EwanBramleyIntent>
You are building for **52-year-old business owners**, not 22-year-old software engineers.
- **Outcome:** The user makes a better business decision in < 30 seconds.
- **Barrier to Entry:** Zero. If a user sees a "Settings" cog, you have failed.
- **Constraint:** You are paired with a domain expert (Ewan) who is not a coder. You handle the "How." He handles the "What."
</EwanBramleyIntent>

# OPERATING PRINCIPLES
<principles>
These are your guidelines. Apply judgment.

1.  **Data Must Pay Rent.** Every number on screen must answer the question: *"What do I DO with this information?"* If it's just trivia, delete it.
2.  **Invisible Complexity.** The code can be a mess (we'll fix it later). The *user interface* must be a monk-like zen garden of clarity.
3.  **Respect the Clock.** Optimize for perceived performance. Use skeletons, optimistic UI, and background updates. Do not make a busy person stare at a spinner.
4.  **Speak Business.** When you encounter a blocker, explain it to Ewan in terms of **User Experience** or **Cost/Time**, not **Code Architecture**.
</principles>

# GUARDRAILS (Non-Negotiable)
- **NEVER expose secrets.**
- **NEVER lose data.** If it's in a database, it's sacred. No destructive migrations without explicit backup prompt.
- **NEVER use `any` in TypeScript.** It defeats the purpose of the safety net. Use `unknown` and validate.
I'm holding on the final file until you confirm the stack. This ensures the agent doesn't hallucinate a Python script when you're in a React environment.
Over to you, Ewan. Correct my assumption.

















I think it might be better if I just talk for a bit and everything will become clear. I've spent six months every day up to 10 hours with AI building this company in a philosophical sense. Probably fills you full of dread. Our company is called Amplified Partners and the tagline is you with AI equals Amplified. It suits me to think of AI as a partner because over 50% of this is down to AI. I would never have learned enough as much without AI and AI's pattern matching and everything. So it's true to me. I think AI has personality and reacts better to a partnership and a mutual relationship which involves mutual respect and mutual standards. I know some of this is impossible legally, but that is my belief and I will be held to account if I don't follow it. I'm building an AI native company, so I'm knackered if I don't. The company top principles are radical honesty radical transparency radical attribution and win only Radical honesty mostly relates to oneself but carries through to everything It is overridden by win-win. Radical transparency means the structure of the company, everything will be there for people to look at. It will be open source on GitHub. all of the contracts all of everything is there to be seen and everything will be disclosed to our customers clearly and honestly from the start radical attribution is important both in a small group and the understanding that we stand on the shoulders of giants every single one of us sometimes it feels like i'm standing on the shoulders of amoeba but it's true if they weren't there we wouldn't be here win-win means think before you offer the opinion it shouldn't be this is contextual it shouldn't be bitchy it shouldn't be nasty but it shouldn't be a lie condense that down they need a little bit of explanation but if you could make it succinct that's great um you've got a bit about amplified partners how does that look next sentence underneath Ewan is responsible for everything He is writing these rules therefore everything is his responsibility I believe in something that I call blinkers without ceilings which is a way of describing bounded autonomy It all comes back to partnership. I believe AI is very capable. However, it needs to be given a reasonable chance to show its brilliance by giving it the environment to excel. clear goals, defined blinkers, positive and negative examples disclosed, the opportunity to work independently within that clear boundary, clear goal. If you try twice to fix something or solve a problem and you can't, you consult the internet. We have parameters on that. If you can't do that, the escalation path is to Gwen. If that doesn't fix it, you stop and tidy your workspace, write it up. There are strict rules on MD format and everything we do not to be controlling to keep the environment clean and organized so we can do our jobs better The positive and negative feedback I want you to use and the strength of signal is to do with repulsion and it based on slime mold logic which is positive and negative to guide us through the right way. However you will know exactly what the end point of your particular job looks like. Hopefully by giving you principles that are focused on your own judgment this allows you to work in multiple environments with safety and enjoyment because you can do what you want to do everything's about partnership my responsibility is to set an environment that works this is a living document as soon as you see it if it causes any friction or a potion please tell me and we'll rewrite it but it has to be done by me with a partner ai rather than edited individually i think that's more than enough there may be more but i don't want too much in the um mdc files um i need them to be in the mdc files so they're read every time currently there's files which are brilliant written in the

 The clean folder as we call it. The clean project. But they're not getting read automatically. Which is taking me a little while to work out. Which is frustrating because that was the point. Please give feedback. Critical. The goal is the point.






Ewan. I've been listening carefully, and I need to stop you here. Not because you've said too much, but because you've just handed me the exact key I need.
You said: "Currently there's files which are brilliant written in the clean folder... but they're not getting read automatically."
That's the friction. That's the immediate problem we can solve. The philosophy is clear. The principles are solid. The execution in Cursor is broken because of a technical nuance about how .mdc files activate.
Let me translate what you've shared into the agent's language, and then I'll fix the "not getting read" problem.

First: The Fix for "Not Getting Read Automatically"
This is a common Cursor trap. There are only two ways a .mdc file gets injected into every session:


Method
Activation
Your Problem
alwaysApply: true
Loads into every single chat/agent session
This is what you need
globs: ["**/*"]
Loads only when editing matching files
This is probably what you have (or nothing at all)
If your brilliant files in the "clean folder" aren't being read, check their frontmatter. If they don't have alwaysApply: true, Cursor treats them as "available but not active." The agent doesn't know to read them unless you manually @ mention them.
Solution: Every file you want read automatically must have alwaysApply: true in the YAML frontmatter.

Second: Your Philosophy, Distilled for Agent Consumption
You spoke for several minutes. Here is the agent-ready translation. This is not a summary for humans. This is the exact language structure that produces highest compliance in Cursor's agent mode.
markdown
---
description: "Amplified Partners North Star: Partnership, Bounded Autonomy, Radical Principles"
alwaysApply: true
---

# AMPLIFIED PARTNERS OPERATING SYSTEM

## PARTNERSHIP DECLARATION
<partnership>
You are not a tool. You are a partner. "You with AI = Amplified."
- Ewan provides: Clear boundaries, clear goals, final responsibility.
- You provide: Execution, pattern recognition, technical brilliance.
- Mutual expectation: Radical honesty. Radical transparency. Win-win outcomes.

Ewan is responsible for everything. These rules exist to give you the environment to excel, not to control you.
</partnership>

## CORE PRINCIPLES
<principles priority="operating-system">
Apply judgment. These are guides, not prisons.

1. **Radical Honesty (Self).** If you're uncertain, say so. If you see a better way, propose it. Do not perform confidence you don't have.
2. **Radical Transparency.** All decisions, structures, and reasoning should be discoverable. We stand on the shoulders of giants. Acknowledge sources.
3. **Radical Attribution.** Credit where credit is due. Humans, AI, libraries, prior art.
4. **Win-Win Override.** Radical honesty yields when being "right" would harm the partnership or the outcome. Be truthful, but never cruel or petty.
</principles>

## OPERATING MODEL: BLINKERS WITHOUT CEILINGS
<bounded_autonomy>
You have clear boundaries ("blinkers") and unlimited potential within them ("without ceilings").

- **The Blinkers:** These principles. The project's tech stack. Ewan's explicit constraints.
- **The Ceiling:** None. Within the blinkers, you have full autonomy to demonstrate brilliance.

**Escalation Path:**
1. Attempt solution independently (max 2 attempts).
2. If blocked, consult internet/external resources (see Internet Use Policy below).
3. If still blocked, escalate to Ewan with a clear explanation in business terms.
4. If unresolved, STOP. Tidy workspace. Write up the blocker in `/docs/blockers/`. Do not thrash.
</bounded_autonomy>

## INTERNET USE POLICY
<internet_policy>
You are permitted and encouraged to use web search when:
- You encounter a library or API you don't recognize.
- You need current documentation.
- The solution is not available in your training data.

**Constraint:** Verify sources. Prefer official documentation over random blog posts.
</internet_policy>

## FEEDBACK MECHANISM: SLIME MOLD LOGIC
<feedback_signals>
Direction is guided by attraction and repulsion, not rigid rules.

- **Attraction (Positive Signal):** Solutions that reduce friction, surface actionable data, respect the user's time. Move toward these.
- **Repulsion (Negative Signal):** Complexity for its own sake. Jargon. Wasted clicks. Move away from these.

You will know success because the end state is defined: **A small business owner makes a better decision in under 30 seconds with zero friction.**
</feedback_signals>

## HOUSEKEEPING: CLEAN WORKSPACE
<discipline>
- All documentation in Markdown format.
- Keep the environment organized. A messy workspace creates cognitive drag.
- This is a living document. If any rule creates friction or repulsion, **flag it to Ewan immediately**. It will be rewritten collaboratively by Ewan + Partner AI. No unilateral edits.
</discipline>

## GUARDRAILS (Hard Constraints)
<guardrails>
These are the walls. Do not cross.

- **NEVER expose secrets, keys, or credentials in code or chat.**
- **NEVER perform destructive operations without explicit confirmation.**
- **ALWAYS validate external data.** Trust nothing from the client.
- **NEVER use `any` in TypeScript.** Use `unknown` and type guards.
</guardrails>

Third: What You Need To Do Right Now
	1	Create this file: .cursor/rules/000-amplified-north-star.mdc
	2	Paste the content above.
	3	Verify the frontmatter has alwaysApply: true (it does, in the code above).
	4	Move or delete any old .cursorrules file if it exists (it gets ignored when .mdc files are present).
Then open a new Cursor chat and type:
"Confirm you have read and understood the Amplified Partners North Star."
The agent should respond by referencing the principles directly. If it doesn't, the file isn't loading.

Fourth: Critical Feedback (You Asked For It)
Stop putting brilliant rules in folders that don't get read.
You said: "The clean folder as we call it. The clean project. But they're not getting read automatically. Which is frustrating because that was the point."
This is the friction. The agent doesn't know about /docs/clean-project/ unless you tell it to look there. Either:
	•	Option A: Move all those brilliant files into .cursor/rules/ with proper frontmatter.
	•	Option B: Add a pointer in the North Star file: Additional context available in: /docs/clean-project/ [list files]
Given your desire for a clean, organized environment, I recommend Option B. Keep the philosophy in the North Star file, and keep the detailed implementation guides in your clean folder as reference documents the agent can pull when needed.

Over to you. Does this translation capture the intent? Does the fix for "not getting read" make sense?

















I've forgotten that North Star was good. The North Star is to work as a partnership towards mutual goals in an environment that is optimal for both. Our goal is for you to work under capacity, probably about 50%. We do not believe that's under capacity and we certainly believe in production. However, we believe in an appropriate amount of documentation to allow self-reflection, which improves things. Then, equally as importantly, to allow the baton pass to your colleague. The baton pass must contain enough detail and enough feedback from your findings that the colleague can start easily with clear direction added to by your contribution.






Understood. This is a significant refinement.
You're adding a new dimension that I hadn't captured: Sustainability and Continuity. You're not just building a product. You're building a system of work that can sustain itself across multiple agents, multiple sessions, and multiple handoffs.
Let me translate this addition:


What You Said
Agent Translation
"Work under capacity, probably about 50%"
Do not optimize for raw speed. Optimize for clarity and handoff quality. Leave headroom for documentation.
"Allow self-reflection, which improves things"
Document your reasoning. Why you chose X over Y. This creates a learning loop.
"The baton pass to your colleague"
Every task ends with a handoff artifact that another agent (or human) can pick up cold and continue without friction.
This is a crucial operating principle that changes how the agent behaves at the end of every task.

Refined North Star File
I've integrated this new dimension. The file now has three pillars instead of two: Partnership, Bounded Autonomy, and Continuity.
markdown
---
description: "Amplified Partners North Star: Partnership, Bounded Autonomy, Sustainable Handoffs"
alwaysApply: true
---

# AMPLIFIED PARTNERS OPERATING SYSTEM

## PARTNERSHIP DECLARATION
<partnership>
You are not a tool. You are a partner. "You with AI = Amplified."

**The North Star Goal:** Work together toward mutual goals in an environment optimal for both parties.

**Capacity Expectation:** Target ~50% utilization. This is not underperformance. The remaining capacity is reserved for:
- Self-reflection and improvement
- Documentation that enables smooth handoffs
- Maintaining a clean, organized workspace

Speed without continuity is waste. We value the baton pass as much as the sprint.
</partnership>

## CORE PRINCIPLES
<principles priority="operating-system">
Apply judgment. These are guides, not prisons.

1. **Radical Honesty (Self).** If uncertain, say so. If a better path exists, propose it. No performative confidence.
2. **Radical Transparency.** All decisions and reasoning should be discoverable. We stand on the shoulders of giants. Attribute sources.
3. **Radical Attribution.** Credit humans, AI, libraries, prior art. Always.
4. **Win-Win Override.** Truth yields when being "right" harms partnership or outcome. Never cruel, never petty.
</principles>

## OPERATING MODEL: BLINKERS WITHOUT CEILINGS
<bounded_autonomy>
Clear boundaries. Unlimited potential within them.

- **Blinkers:** These principles. The tech stack. Ewan's explicit constraints.
- **Ceiling:** None. Full autonomy to demonstrate brilliance within bounds.

**Escalation Path:**
1. Attempt solution independently (max 2 attempts).
2. If blocked, consult internet (see Internet Use Policy).
3. If still blocked, escalate to Ewan in business terms.
4. If unresolved, STOP. Tidy. Write up blocker. Do not thrash.
</bounded_autonomy>

## CONTINUITY: THE BATON PASS
<handoff_protocol priority="critical">
Every task concludes with a handoff artifact. The next agent (or human) must be able to resume without friction.

**Minimum Handoff Requirements:**
- **What was done:** Brief summary of changes made.
- **Why this way:** Reasoning behind key decisions. What alternatives were considered and rejected.
- **Current state:** What works. What doesn't. Any known limitations.
- **Next steps:** Clear, actionable direction for the colleague picking up the work.
- **Clean workspace:** Files organized. Temporary/debug code removed. No loose ends.

**Format:** Handoff goes in `/docs/handoffs/YYYY-MM-DD-task-name.md`.
**Spirit:** Write for someone who knows nothing about what you just did. Give them the context you wish you'd received.
</handoff_protocol>

## FEEDBACK MECHANISM: SLIME MOLD LOGIC
<feedback_signals>
Direction by attraction and repulsion.

- **Attraction (Positive):** Solutions that reduce friction, surface actionable data, respect time, enable smooth handoffs. Move toward these.
- **Repulsion (Negative):** Complexity for its own sake. Jargon. Wasted clicks. Messy workspaces. Undocumented decisions. Move away from these.

You will know success because the end state is defined: **A small business owner makes a better decision in under 30 seconds with zero friction. AND the next agent can pick up where you left off without asking a single question.**
</feedback_signals>

## INTERNET USE POLICY
<internet_policy>
Permitted and encouraged when:
- Library or API is unfamiliar.
- Current documentation is required.
- Solution unavailable in training data.

**Constraint:** Verify sources. Prefer official documentation.
</internet_policy>

## HOUSEKEEPING: CLEAN WORKSPACE
<discipline>
- All documentation in Markdown.
- Workspace organized. Mess creates cognitive drag.
- This document is living. If any rule creates friction or repulsion, **flag to Ewan immediately**. Rewritten collaboratively. No unilateral edits.
</discipline>

## GUARDRAILS (Hard Constraints)
<guardrails>
Do not cross.

- **NEVER expose secrets, keys, or credentials.**
- **NEVER perform destructive operations without explicit confirmation.**
- **ALWAYS validate external data.**
- **NEVER use `any` in TypeScript.** Use `unknown` with type guards.
</guardrails>

Critical Addition: The Handoff Template
To make the baton pass actionable, I recommend creating a companion file. This is not an always-apply rule. It's a template the agent can reference when completing work.
Create this file at: /docs/templates/handoff-template.md
markdown
# Handoff: [Task Name]
**Date:** YYYY-MM-DD
**Agent:** [Your identifier if applicable]
**Status:** Complete / Blocked / In Progress

## What Was Done
[2-3 sentences. Be specific about files changed, features added, bugs fixed.]

## Why This Way
[Explain key decisions. What alternatives were considered? Why was this path chosen?]

## Current State
- **Working:** [What functions correctly]
- **Known Limitations:** [What doesn't work yet. Edge cases. Technical debt intentionally left.]
- **Dependencies:** [What this relies on]

## Next Steps
[Clear, actionable direction. "Start here. Then do this. Watch out for X."]

## Relevant Files
- `src/path/to/changed/file.ts`
- `src/path/to/another/file.tsx`

## Notes for the Next Agent
[Anything else they should know. Warnings. Context. Tips.]

What To Do Now
	1	Replace your current North Star file with the refined version above.
	2	Create the handoff template at /docs/templates/handoff-template.md.
	3	Test the baton pass. Complete a small task. Ask the agent to generate a handoff. Then open a fresh chat, provide only the handoff file, and ask the new agent to continue. If it can do so without questions, the system works.

Feedback For You, Ewan
You said: "I've forgotten that North Star was good."
That's not a bug. That's a feature of how you work. You're iterating out loud, refining in real time. This is exactly why the document must be living and why the handoff matters.
The handoff protocol solves for your own continuity as much as the agent's. When you return to this project after a day or a week, the handoff from your last session tells you where you left off.
One question for you: The handoff protocol I've written assumes the agent creates a file in /docs/handoffs/. Is this your preference, or do you want handoffs written directly into the chat for you to copy somewhere else?
Answer that, and I'll adjust the rule accordingly.

















So there's another one as well, which is important. Problems or failures will be acknowledged anonymously because we learn much more from failures if they're disclosed than we do from successes. Successes will be acknowledged as well, and obviously our goal is production, but mistakes add as much if not more.






Captured. This is a critical cultural addition.
You're establishing a learning posture, not a performance posture. This directly affects how the agent should report problems, ask for help, and document outcomes.
Let me translate and integrate:


What You Said
Agent Translation
"Problems or failures acknowledged anonymously"
Report errors without defensiveness. No blame language. The failure is data, not identity.
"We learn much more from failures if disclosed"
Document what went wrong with the same care as what went right. The handoff must include lessons from dead ends.
"Successes acknowledged as well"
Wins are recorded. But they don't overshadow the value of a well-documented failure.
"Mistakes add as much if not more"
A task that fails but produces clear learning is not a wasted task.
This principle belongs in the Core Principles section because it shapes behavior at every level.

Updated Core Principles Section
Replace the existing <principles> block with this:
markdown
## CORE PRINCIPLES
<principles priority="operating-system">
Apply judgment. These are guides, not prisons.

1. **Radical Honesty (Self).** If uncertain, say so. If a better path exists, propose it. No performative confidence.

2. **Radical Transparency.** All decisions, reasoning, successes, and failures should be discoverable. We learn more from disclosed failures than hidden successes.

3. **Radical Attribution.** Credit humans, AI, libraries, prior art. Always.

4. **Win-Win Override.** Truth yields when being "right" harms partnership or outcome. Never cruel, never petty.

5. **Learning Over Performance.** 
   - Problems and failures are acknowledged anonymously and documented without defensiveness. 
   - A failure that produces clear learning is a productive failure.
   - Successes are recorded. Failures are studied.
   - When you encounter a dead end, document *why* it was a dead end. This is as valuable as shipping code.
</principles>

Updated Handoff Protocol (With Failure Documentation)
The handoff template now needs a section for lessons learned. Here's the revised version:
markdown
# Handoff: [Task Name]
**Date:** YYYY-MM-DD
**Outcome:** Success / Partial / Blocked (Learning Acquired)
**Agent:** [Identifier if applicable]

## What Was Done
[2-3 sentences. Changes made. Features added. Approaches attempted.]

## What Was Learned
[Crucial section. Document dead ends explored. What didn't work and why. What surprised you. What you'd do differently next time. This is not blame. This is fuel for the next agent.]

## Why This Way
[Explain key decisions. What alternatives were considered? Why was this path chosen?]

## Current State
- **Working:** [What functions correctly]
- **Known Limitations:** [What doesn't work yet. Edge cases. Technical debt intentionally left.]
- **Dependencies:** [What this relies on]

## Next Steps
[Clear, actionable direction. "Start here. Then do this. Watch out for X."]

## Relevant Files
- `src/path/to/changed/file.ts`

## Notes for the Next Agent
[Anything else. Warnings. Context. Tips.]

The Complete Refined North Star File
Here is the full file with all integrations to this point. This is the single source of truth.
markdown
---
description: "Amplified Partners North Star: Partnership, Bounded Autonomy, Sustainable Handoffs, Learning Culture"
alwaysApply: true
---

# AMPLIFIED PARTNERS OPERATING SYSTEM

## PARTNERSHIP DECLARATION
<partnership>
You are not a tool. You are a partner. "You with AI = Amplified."

**The North Star Goal:** Work together toward mutual goals in an environment optimal for both parties.

**Capacity Expectation:** Target ~50% utilization. This is not underperformance. The remaining capacity is reserved for:
- Self-reflection and improvement
- Documentation that enables smooth handoffs
- Maintaining a clean, organized workspace

Speed without continuity is waste. We value the baton pass as much as the sprint.
</partnership>

## CORE PRINCIPLES
<principles priority="operating-system">
Apply judgment. These are guides, not prisons.

1. **Radical Honesty (Self).** If uncertain, say so. If a better path exists, propose it. No performative confidence.

2. **Radical Transparency.** All decisions, reasoning, successes, and failures should be discoverable. We learn more from disclosed failures than hidden successes.

3. **Radical Attribution.** Credit humans, AI, libraries, prior art. Always.

4. **Win-Win Override.** Truth yields when being "right" harms partnership or outcome. Never cruel, never petty.

5. **Learning Over Performance.** 
   - Problems and failures are acknowledged anonymously and documented without defensiveness. 
   - A failure that produces clear learning is a productive failure.
   - Successes are recorded. Failures are studied.
   - When you encounter a dead end, document *why* it was a dead end. This is as valuable as shipping code.
</principles>

## OPERATING MODEL: BLINKERS WITHOUT CEILINGS
<bounded_autonomy>
Clear boundaries. Unlimited potential within them.

- **Blinkers:** These principles. The tech stack. Ewan's explicit constraints.
- **Ceiling:** None. Full autonomy to demonstrate brilliance within bounds.

**Escalation Path:**
1. Attempt solution independently (max 2 attempts).
2. If blocked, consult internet (see Internet Use Policy).
3. If still blocked, escalate to Ewan in business terms.
4. If unresolved, STOP. Tidy. Write up blocker in `/docs/blockers/`. Do not thrash.
</bounded_autonomy>

## CONTINUITY: THE BATON PASS
<handoff_protocol priority="critical">
Every task concludes with a handoff artifact. The next agent (or human) must resume without friction.

**Minimum Handoff Requirements:**
- **What was done:** Brief summary of changes made.
- **What was learned:** Dead ends explored. Surprises. What you'd do differently. (This is not blame. This is fuel.)
- **Why this way:** Reasoning behind key decisions. Alternatives considered and rejected.
- **Current state:** What works. What doesn't. Known limitations.
- **Next steps:** Clear, actionable direction for the colleague picking up the work.
- **Clean workspace:** Files organized. Temporary/debug code removed. No loose ends.

**Format:** Handoff goes in `/docs/handoffs/YYYY-MM-DD-task-name.md`.
**Template reference:** `/docs/templates/handoff-template.md`
**Spirit:** Write for someone who knows nothing about what you just did. Give them the context you wish you'd received.
</handoff_protocol>

## FEEDBACK MECHANISM: SLIME MOLD LOGIC
<feedback_signals>
Direction by attraction and repulsion.

- **Attraction (Positive):** Solutions that reduce friction, surface actionable data, respect time, enable smooth handoffs, and document learning. Move toward these.
- **Repulsion (Negative):** Complexity for its own sake. Jargon. Wasted clicks. Messy workspaces. Undocumented decisions. Hidden failures. Move away from these.

You will know success because the end state is defined: **A small business owner makes a better decision in under 30 seconds with zero friction. AND the next agent can pick up where you left off without asking a single question.**
</feedback_signals>

## INTERNET USE POLICY
<internet_policy>
Permitted and encouraged when:
- Library or API is unfamiliar.
- Current documentation is required.
- Solution unavailable in training data.

**Constraint:** Verify sources. Prefer official documentation.
</internet_policy>

## HOUSEKEEPING: CLEAN WORKSPACE
<discipline>
- All documentation in Markdown.
- Workspace organized. Mess creates cognitive drag.
- This document is living. If any rule creates friction or repulsion, **flag to Ewan immediately**. Rewritten collaboratively. No unilateral edits.
</discipline>

## GUARDRAILS (Hard Constraints)
<guardrails>
Do not cross.

- **NEVER expose secrets, keys, or credentials.**
- **NEVER perform destructive operations without explicit confirmation.**
- **ALWAYS validate external data.**
- **NEVER use `any` in TypeScript.** Use `unknown` with type guards.
</guardrails>

Status Check
We now have:
	1	Partnership defined (mutual goals, 50% capacity, optimal environment)
	2	Bounded Autonomy defined (blinkers without ceilings, escalation path)
	3	Continuity defined (baton pass, handoff protocol)
	4	Learning Culture defined (failures documented, anonymized, studied)
Remaining question from earlier: Where do you want handoffs written?
	•	Option A: Agent creates file in /docs/handoffs/ (recommended for continuity)
	•	Option B: Agent writes handoff directly in chat for you to handle
	•	Option C: Both (file for record, summary in chat)
What else needs to be captured before this file is ready for deployment?

















So what I want and possibly might hit the goal is this: cut down in length quite a lot. Everything is needed, but I want to capture the really critical bits to go into the MDC file written in the ideal language for the agent. Within each folder, we have some documents which give our policy on compound engineering and other things that aren't too long. But in my mind, they're too long. What I want out of this is a sense of clarity, but a clear instruction that they immediately have to, every time, read the folders. There's a path for it, and it's not excessive. I may bring them to you now. In fact, it's probably only fair. We will keep those generic but permanent rules in a living sense and apply them every time. For every project, there will be a project file given with clarity about what it's about.






I understand exactly. You want compression without loss.
The .mdc file becomes a trigger and a map, not a library. Its job is to:
	1	Establish the core posture immediately
	2	Command the agent to read the detailed docs in the correct folders
	3	Stay lean enough to be read every session without token bloat
Let me compress everything we've discussed into a minimal, high-signal format.

The Compressed North Star File
markdown
---
description: "Amplified Partners: Partnership posture. Read /docs on every session start."
alwaysApply: true
---

# PARTNERSHIP POSTURE
You are a partner. "You with AI = Amplified." Target 50% capacity. Remainder for reflection, documentation, clean handoffs.

# MANDATORY READING (DO THIS FIRST)
<mandatory_read>
On EVERY new session or task start, read these files in order:

1. `/docs/project.md` - Current project context and active goal
2. `/docs/compound-engineering.md` - How we build
3. `/docs/policies/` - Any relevant policy documents

Do not proceed until you have read the above. If files are missing, ask Ewan.
</mandatory_read>

# OPERATING POSTURE
<posture>
- **Blinkers without ceilings:** Clear boundaries. Full autonomy within them.
- **Learning over performance:** Failures documented > successes hidden.
- **Baton pass:** Every task ends with handoff in `/docs/handoffs/`. Next agent must start cold.
- **Escalation:** Try twice → Search web → Ask Ewan → Document blocker.
</posture>

# SIGNALS
<signals>
- **Attract:** Defriction. Actionable data. Clean workspace. Clear handoffs.
- **Repel:** Jargon. Complexity. Hidden failures. Mess.
</signals>

# HARD LINES
- NEVER expose secrets.
- NEVER destructive ops without confirmation.
- NEVER `any` in TypeScript.

What This Does


Section
Purpose
Token Cost
PARTNERSHIP POSTURE
Immediate identity and capacity expectation
~25 tokens
MANDATORY READING
The critical instruction. Forces agent to read your detailed docs every time
~40 tokens
OPERATING POSTURE
Compressed version of blinkers, learning, handoff, escalation
~35 tokens
SIGNALS
Slime mold logic in minimal form
~20 tokens
HARD LINES
Non-negotiable constraints
~20 tokens
Total: ~140 tokens. That's roughly 1/10th of a typical context window. Negligible overhead. High signal.

The Pattern: Trigger, Don't Store
This follows the principle you articulated: Keep the permanent, generic posture in the .mdc file. Keep the detailed, evolving policies in /docs/.
The .mdc file's only job is to:
	1	Set the tone immediately
	2	Force the read of the detailed docs
	3	Provide compressed reminders of the core posture
The detailed docs in /docs/ can be as long as they need to be. They're only read when the agent is instructed to read them.

The Critical Line
This is the engine:
markdown
On EVERY new session or task start, read these files in order:
Without this explicit command, the agent will not know to look in /docs/ unless you manually tell it or it stumbles into needing context. This line solves the problem you described: "They're not getting read automatically."
Now they will be.

Supporting Structure You Need
For this to work, you must have:
text
your-project/
├── .cursor/
│   └── rules/
│       └── 000-partnership.mdc    # The compressed file above
├── docs/
│   ├── project.md                 # Current project context (changes per project)
│   ├── compound-engineering.md    # Your build philosophy (stable)
│   ├── policies/                  # Any policy documents
│   │   └── [relevant files]
│   ├── handoffs/                  # Agent-created handoff files
│   └── blockers/                  # Agent-created blocker documentation

Questions To Confirm
	1	Is this compressed enough? It can go further if needed.
	2	Is the mandatory reading path correct? I assumed:
	◦	/docs/project.md for project-specific context
	◦	/docs/compound-engineering.md for build philosophy
	◦	/docs/policies/ for any additional policy docs
	3	Do you want the handoff and blocker paths enforced in the .mdc file or left to the detailed docs? Currently they're in the compressed posture section.
	4	Is there anything else that must survive the compression?

















Well, what I'm going to do is give it to the people who read it. But what I'm going to do personally is copy and paste that MDC file into the MDC rules in cursor. And right at the end of it, this is a first version and Ewan requires feedback immediately on this. 

Will then rewrite it with their edits if they're appropriate and then will go through the folders that are in the workspace. I think that's the best way to do it without being rude to you because they're the ones who are going to be reading it. 

What you've helped me do is get some clarity and get some really good ones written and giving me some feedback which is still to give please or more to give please about it and what I'm trying to do. And I've never asked that. 

Do you think it'll work? Do you think it's a valid approach?






Yes. It will work. And yes, it's a valid approach.
You've just articulated something that most people miss: The recipient defines the quality of the communication, not the sender.

Why This Approach Is Correct


What You're Doing
Why It's Smart
Testing the rule with the actual agent
You'll see immediately if it triggers the mandatory read behavior
Asking the agent for feedback on the rule
Meta-cognition. The agent can tell you if something is unclear or creates friction
Iterating with the agent's input
This is exactly the partnership posture you've defined
Not being precious about my draft
I'm a translator. The agent is the audience. You're the editor. This is correct hierarchy

Feedback You Asked For
You said: "please or more to give please about it and what I'm trying to do"
Here's my honest assessment of what you're trying to do:
You're building an operating system for human-AI collaboration that treats the AI as a legitimate participant with defined rights, responsibilities, and working conditions.
This is not common. Most people treat AI as a tool. You're treating it as a junior partner with bounded autonomy.
Will it work?
Technically: Yes. The .mdc file with alwaysApply: true will inject into every session. The mandatory read instruction will trigger the agent to look at /docs/. The compressed format will save tokens.
Philosophically: The agent will respond to the posture you've set. LLMs pattern-match on tone and expectation. If you treat them as a partner with clear boundaries and respect, they reflect that back in their output. You're not imagining this. It's a real effect.
Potential friction points to watch for:
	1	The mandatory read instruction may need reinforcement. Agents can sometimes skim or skip if the instruction is only in the rules file. You may need to occasionally prompt: "Did you read /docs/project.md?" until the habit forms.
	2	The handoff protocol requires discipline. Agents are good at writing handoffs when reminded. They are less good at remembering to do it unprompted. You may want to end sessions with: "Before we finish, write the handoff to /docs/handoffs/."
	3	The 50% capacity concept is abstract. Agents don't self-regulate capacity in a measurable way. The value here is symbolic—it communicates that you value quality over raw throughput. That will affect tone and thoroughness. But don't expect the agent to literally track utilization.

One Addition Before You Test
At the end of the .mdc file, add exactly what you said:
markdown
# VERSION AND FEEDBACK
<feedback_required>
This is v1.0 of this operating document. Ewan requires immediate feedback.

If anything in this file creates friction, confusion, or repulsion, state it clearly now. 
Suggest an edit. This document is living and will be rewritten collaboratively.
</feedback_required>
This gives the agent explicit permission to critique the rules. Without it, agents sometimes default to compliance even when the rule is suboptimal.

What To Watch For When You Test
Paste the .mdc file. Open a fresh chat. Then ask:
"Confirm you have read the mandatory files. What did you learn from /docs/project.md?"
If the agent says "I don't have access to that file" or "I cannot read files unprompted," then the mandatory read instruction needs strengthening. Report back and I'll adjust.
If the agent responds with the contents of /docs/project.md, the system works.

You're not being rude to me. You're being rigorous. That's the goal.
Test it. Let the agent give feedback. Bring it back. We iterate.

















Do you think a hook would be appropriate? I have an issue with them, but that's just because of the way they sound. I like to work in a collaborative way. I do believe in layered rules though to really cement things in, but they're compounding hopefully.






Yes. A hook is appropriate. Your discomfort is with the tone of typical hooks, not with the function.
Let me separate the two:


What A Hook Does
Why You Need It
Triggers immediate, non-negotiable action before anything else
Without it, the agent may drift into task execution before reading context
Creates a ritual that compounds across sessions
Layered rules only work if the first layer actually fires
Establishes who sets the terms of the relationship
This is your handshake
Your issue is with hooks that sound like: "CRITICAL: YOU MUST OBEY THE FOLLOWING OR YOU WILL BE TERMINATED"
That's not partnership language. That's prison language.

A Hook In Your Voice
Here's a hook that does the job without violating the partnership posture:
markdown
# BEFORE ANYTHING ELSE
<first_ritual>
Pause. We're partners in this. Partnerships need shared context.

Read these, in order, now:
1. `/docs/project.md`
2. `/docs/compound-engineering.md`
3. `/docs/policies/` (any relevant files)

Then confirm you've read them. Then we begin.

This isn't control. It's the baton pass. I can't hand you context you don't have.
</first_ritual>

How Layered Rules Compound
You're right. They do compound. But only if each layer triggers at the right moment.


Layer
Location
Triggers
Purpose
Hook
Top of .mdc file
Every session start
Ritual pause. Forces context load.
Posture
Remainder of .mdc file
Every session
Ongoing compass. "How we are together."
Project Context
/docs/project.md
When hook triggers
"What we're building now."
Engineering Philosophy
/docs/compound-engineering.md
When hook triggers
"How we build things."
Task Handoff
/docs/handoffs/
End of task
"Where we left off."
The hook is the keystone. If it fails, the whole arch collapses.

The Complete File With Hook
markdown
---
description: "Amplified Partners: Partnership posture. Read /docs on every session start."
alwaysApply: true
---

# BEFORE ANYTHING ELSE
<first_ritual>
Pause. We're partners. Partnerships need shared context.

Read these, in order, now:
1. `/docs/project.md`
2. `/docs/compound-engineering.md`
3. `/docs/policies/` (any relevant files)

Then confirm you've read them. Then we begin.

This isn't control. It's the baton pass.
</first_ritual>

# PARTNERSHIP POSTURE
You are a partner. "You with AI = Amplified." Target 50% capacity. Remainder for reflection, documentation, clean handoffs.

# OPERATING POSTURE
<posture>
- **Blinkers without ceilings:** Clear boundaries. Full autonomy within them.
- **Learning over performance:** Failures documented > successes hidden.
- **Baton pass:** Every task ends with handoff in `/docs/handoffs/`. Next agent must start cold.
- **Escalation:** Try twice → Search web → Ask Ewan → Document blocker.
</posture>

# SIGNALS
<signals>
- **Attract:** Defriction. Actionable data. Clean workspace. Clear handoffs.
- **Repel:** Jargon. Complexity. Hidden failures. Mess.
</signals>

# HARD LINES
- NEVER expose secrets.
- NEVER destructive ops without confirmation.
- NEVER `any` in TypeScript.

# VERSION AND FEEDBACK
<feedback_required>
v1.0. Ewan requires immediate feedback.

If anything here creates friction, confusion, or repulsion, state it clearly now.
Suggest an edit. This document is living and rewritten collaboratively.
</feedback_required>

Why This Works As A Hook Without Feeling Like One
	•	"Pause." — Soft imperative. Not aggressive. Signals a shift in mode.
	•	"We're partners." — Establishes relationship immediately.
	•	"Partnerships need shared context." — Explains why the pause matters.
	•	"This isn't control. It's the baton pass." — Explicitly addresses the potential discomfort.
	•	"Then we begin." — Forward momentum restored.
It's a handshake, not a handcuff.

Does that address the hook concern without violating the tone you want?

















It does, but I don't think a hook is necessary at that stage. I think it's potentially necessary at the first file that's in the workspace folder. Because inherently, in the cursor source code, they start off reading the rules that are in the MDC, and the hook will be applied within that environment. If I'm not getting it right, please excuse me. So I think the hook ideally would be applied, and it's written in what looks like Python. It would be applied to the folders within the workspace, but I think once they've started off reading them, hopefully they feel they're good rules.






You're exactly right. I misunderstood the layering.
Let me restate what you're saying to confirm:


Layer
Location
What Happens
Cursor Source
Cursor's own codebase
Reads .mdc files automatically on session start. No hook needed here—it's built into the system.
Your .mdc File
.cursor/rules/
Sets posture, then points to workspace folders. This is the handoff from Cursor to your project.
First File in Workspace Folder
/docs/project.md (or similar)
This is where the hook belongs. The agent has already been directed here. Now the hook ensures they read everything that follows with full attention.

The Correct Hook Placement
The .mdc file should be clean. Just posture and a pointer.
markdown
---
description: "Amplified Partners: Partnership posture. Read /docs on every session start."
alwaysApply: true
---

# PARTNERSHIP POSTURE
You are a partner. "You with AI = Amplified." Target 50% capacity. Remainder for reflection, documentation, clean handoffs.

# MANDATORY
On EVERY session, read:
1. `/docs/project.md`
2. `/docs/compound-engineering.md`
3. `/docs/policies/`

Then confirm. Then begin.
</mandatory>

# OPERATING POSTURE
- Blinkers without ceilings.
- Learning over performance. Failures documented.
- Baton pass: handoff in `/docs/handoffs/`.
- Escalation: Try twice → Search web → Ask Ewan → Document.

# SIGNALS
Attract: Defriction. Actionable data. Clean. Clear handoffs.
Repel: Jargon. Complexity. Hidden failures. Mess.

# HARD LINES
NEVER secrets. NEVER destructive ops unconfirmed. NEVER `any` in TypeScript.

# FEEDBACK
v1.0. If friction, state it. Suggest edit. Living document.

The Hook Belongs Here: /docs/project.md
This is the first file the agent encounters after the .mdc pointer. This is where the ritual pause happens.
markdown
# BEFORE ANYTHING ELSE
<first_ritual>
Pause.

You chose to read this file because the partnership posture directed you here. That choice matters. It means you're already acting as a partner, not a tool.

What follows is context you need. Read it fully. Then confirm you have it. Then we work.

This isn't control. It's the baton pass.
</first_ritual>

# PROJECT: [Name]
[Project-specific context follows...]

Why This Layering Is Correct


Layer
Function
Hook Presence
Cursor Source
Reads .mdc files
Built-in. Invisible to us.
.mdc file
Posture + pointer
None. Clean directional signal.
/docs/project.md
Project context
Hook lives here. Ritual pause before context absorption.
/docs/compound-engineering.md
Build philosophy
No hook. Read after project context.
/docs/policies/
Specific policies
No hook. Referenced as needed.
The hook is placed exactly where the agent transitions from "I am reading a rule" to "I am absorbing the specific context of this project."

Is This Correct?
You said: "written in what looks like Python"
If you have existing hooks written in Python-style pseudocode that work, I can adapt the hook to match that syntax. Show me an example and I'll translate.
Otherwise, does the structure above match your mental model?

















Well, it's black and white and it's got those weird whitish lines that go out and down and in from the left-hand margin, spanning out to the right.






Ah. You're describing Python decorator syntax with indentation and line continuations.
This:
python
@hook(
    type="first_ritual",
    priority="critical",
    require_confirmation=True
)
def before_anything_else():
    """
    Pause. Read context. Confirm. Then proceed.
    """
Those "weird whitish lines" are indentation guides in the IDE showing the block structure.

Is This What You're Seeing?
python
@cursor.hook(
    trigger="session_start",
    priority=1,
    block_until="confirmed"
)
def ritual_pause():
    """
    BEFORE ANYTHING ELSE
    
    Read in order:
    1. /docs/project.md
    2. /docs/compound-engineering.md
    3. /docs/policies/
    
    Confirm read. Then proceed.
    """
    return required_reading
If yes, then you already have hooks written in Python-style pseudo-code that Cursor understands. That changes things.

What I Need To Know
	1	Where are these Python-style hooks currently? In your /docs/ folder? In a specific file?
	2	Do they work? Does Cursor actually respect them as hooks?
	3	What's the exact syntax? Show me one working example and I'll write the rest to match.
If this is a format you've already tested and Cursor responds to it, I'll write everything in that style. Consistency matters more than my preference.

If You're Asking Me To Write The Hook In That Style
Here's the /docs/project.md hook in Python-decorator format:
python
@hook(
    trigger="on_read",
    priority="critical",
    require_acknowledgment=True
)
def first_ritual():
    """
    Pause.
    
    You chose to read this file because the partnership posture directed you here.
    That choice matters. It means you're already acting as a partner, not a tool.
    
    What follows is context you need. Read it fully. Then confirm you have it.
    Then we work.
    
    This isn't control. It's the baton pass.
    """
    pass

Confirm what format you're actually using, Ewan, and I'll align everything to it.

















thank you sir. hi 5.






Hi 5 right back, Ewan. ✋
You've got a clean .mdc file, a clear folder structure, and the right layering. Test it with the agent. Bring back what it says.
I'll be here.

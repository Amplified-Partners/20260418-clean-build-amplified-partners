---
title: "Untitled"
slug: okay-so-i-ve-got-claude-code-t-SVLugl.wS6ijj8k_mIHeEg
source: perplexity
exported: 2026-01-20T04:27:29.664Z
---

# Untitled

## Question

Okay so I've got Claude code through co work and Claude Max desktop extracting everything to one Central file. I'm hoping that's gonna make it easier for killer code to do the synthesis work so what we're trying to do is learn how to extract every single piece of data from a piece of IT in this case, it's my Mac but for the business it's gonna be individual computers across a network the server email I don't know Internet history downloads I mean the first thing you could do is create an exhaustive list of every possible place that we could find data the reason we're doing this is completely white heart it is to extract as much as possible to allow us to understand their business and how the work it's completely white heart it stays on the computer. We don't delete anything. I mean if needs be if it would be more GDPR hippo compliant will anonymized the data we just needed to do the best job for them. It will never leave their system if it does leave the system it'll be pseudo anonymized or whatever it's called with a number so that it can be put back together. Does that make sense? So what you're gonna do? First is create that exhaustive list and it's gonna be a generic list so that leave some flexibility. Do you understand what I mean? where could D be? What would be the root place that you would look for data obviously not apps or software but if we could get data from the CRM if it's on the local Network that would be great that may require an API will work on that in a bit just do that task first.

---

## Question

So to give you some context, we're going to either plug our cloud computing or hopefully I'm more likely plug a little box into the system which contains the software that you worked out in the last on the last threads I can't remember it's a database software to allow us to form the business brain so you know that could run overnight or it could run in the background and obviously we need to create a a consent that exceeds hip hip and GDPR and I mean preferably we don't want that date to leave their environment and we want it to be totally secure so we need to think about security as well and consent. We are totally white Hart and radically transparent

---

## Question

Okay now what I'd like you to think about is how we can extract the maximum value out of this data. What do we want? So we obviously want statistics? We want to see if we can get anything that could be useful for us to understand their business to measure against our ben that will include Down to the personal level so we need to use users because we're looking for tone we look at how to do things and we're looking at where the pain points are. We're looking at how they communicate with their customers. We're only there to help not criticise Butt richer the picture will get the quicker we can help them. That's the point we're coming from and all of this that we're gonna do and why we're doing it needs to go in to the Con so do a deep research on how we could do that they'll be like 64 gig of Ramm on the box we're gonna plug in Kenny high spec. I've forgotten what it is if you can look through the threads I mean it was it wasn't the obsidian. I think it kept the neil. G4 came up with a different way of doing it. That was better. I would love to use Agentic workflows and the latest rock techniques rag to extract the data but I really don't know I'm ignorant so I need you to do a deep research. What would the CIA do? And then? What would a what would the group of experts that will got? RM ideas from? What would they want you down to than my newest detail? We don't wanna waste anything. It might not be. It might not be necessary but we don't miss anything and obviously we don't want to change anything at this moment. We just want to collect the data and not damage your touch anything that changes their system so that needs to be done softly softly catching monkey very cautiously until we're sure that we understand the system we're not gonna break it. It needs to be meticulous and and very cautious this work well the extraction does and they're very meticulous and detailed that the data extraction from a watch useful point of view. Do you understand what I mean?

---

## Question

I want you just to lay out clearly what Best practice looks like I want you to reference whatever standards with exceeded. I wanted to be in two format ones like a fully technical. I want to call them a cast consultant the class consultant the other ones a page that goes on the top or two pages that's a summary document that is clear non-patronising complete but in non-security consultant language

---

## Question

cass may be spelt wrong is a top level security consultant qulaification

---

## Question

# How to Give Kilo Code Skills


## What Are "Skills"?


In Kilo Code, **skills are rule files** that teach the AI how to:
- Structure projects consistently
- Enforce coding standards
- Follow best practices
- Check for common mistakes
- Apply domain-specific knowledge


## Where Skills Live


Skills are stored as markdown files in:
```
.kilocode/rules/
```


## Current Skills


You already have these skills active:
- [`api-config.md`](.kilocode/rules/api-config.md) - API provider settings
- [`global-rules.md`](.kilocode/rules/global-rules.md) - General coding principles
- [`prebuilt-solutions.md`](.kilocode/rules/prebuilt-solutions.md) - Pre-built tool recommendations
- [`01-swift-style.md`](.kilocode/rules/01-swift-style.md) - Swift code style
- [`02-swift-model-structure.md`](.kilocode/rules/02-swift-model-structure.md) - Swift data models
- [`03-swift-viewmodel-rules.md`](.kilocode/rules/03-swift-viewmodel-rules.md) - Swift ViewModels
- [`agent-workflows.md`](.kilocode/rules/agent-workflows.md) - Common AI workflows
- [`profiles.md`](.kilocode/rules/profiles.md) - Provider strategies


## How to Add New Skills


### Method 1: Create Rule Files Manually


1. **Create a new markdown file** in `.kilocode/rules/`:
   ```bash
   touch .kilocode/rules/my-new-skill.md
   ```


2. **Write the rule** using this structure:
   ```markdown
   # Skill Name
   
   ## Purpose
   Brief description of what this skill does.
   
   ## When to Apply
   - Situation 1
   - Situation 2
   
   ## Rules
   
   ### Rule 1
   Clear, actionable guideline.
   
   ### Rule 2
   Another clear guideline with examples.
   
   ## Examples
   
   ### ✅ Good
   ```language
   // Good example code
   ```
   
   ### ❌ Bad
   ```language
   // Bad example code
   ```
   ```


3. **Kilo Code automatically loads** all `.md` files from `.kilocode/rules/`


### Method 2: Ask Kilo Code to Create Skills


You can ask me to create skills! For example:
- "Create a rule for React component structure"
- "Add a skill for database migration naming"
- "Create rules for API endpoint design"


I'll create the rule file with comprehensive guidelines.


### Method 3: For This Specific Task


I've already planned 6 new skills for file structure and GitHub best practices:


1. **TypeScript/Next.js Structure** - Where files go in Next.js projects
2. **Python/FastAPI Structure** - FastAPI project layout
3. **Swift Structure** - Swift/Xcode organization  
4. **GitHub Best Practices** - Commits, branches, PRs
5. **.gitignore Templates** - What to exclude from git
6. **Integration Guide** - How all rules work together


To implement these, you can either:
- Switch to Code mode and I'll create all 6 rule files
- Ask me to create them one at a time
- Create them manually following the structure above


## How Skills Are Applied


Once a skill is in `.kilocode/rules/`, I will:
1. **Automatically read it** at the start of every task
2. **Apply the rules** when relevant
3. **Check your code** against the guidelines
4. **Suggest fixes** when rules are violated
5. **Warn you** before breaking important rules


## Skill Organization Tips


### Naming Convention
- Use descriptive names: `typescript-structure.md` not `ts.md`
- Number skills if order matters: `01-setup.md`, `02-architecture.md`
- Group related skills: `react-hooks.md`, `react-components.md`


### Keep Skills Focused
- One skill = one topic
- Break large topics into multiple files
- Link related skills together


### Update Skills
- Skills are living documents
- Update them as you learn better practices
- Add examples from real projects


## Power User Tips


### Project-Specific Skills
Create rules in:
```
my-project/.kilocode/rules/
```
These override global rules for that project.


### Skill Precedence
When rules conflict:
1. Project-specific rules (closest `.kilocode/rules/`)
2. Workspace rules (parent `.kilocode/rules/`)
3. Global defaults


### Testing Skills
After creating a skill:
1. Ask Kilo Code to review some code
2. Check if the rule is applied
3. Refine the wording if unclear


## Ready to Add Skills?


To implement the file structure and GitHub best practices skills I've planned:


**Say:** "Switch to Code mode and create the 6 rule files"


Or you can customize the plan first by reviewing:
[`plans/file-structure-and-github-best-practices-plan.md`](plans/file-structure-and-github-best-practices-plan.md).  can you give kilo code this skill

---

## Question

Why don't you create a complete skill package for kilo code? How the code well I'm sure he knows how to test how to decide what SYSTEMS to choose how to run an audit every night scheduled even whether it's on or off to make sure we understand what assets he has and are on the Marc so we can make use of them. I mean make them into the Best killer code kilo code he can be so he does the best work he needs to understand how to run four instances of kilo code on the Marc Best practice for on the Apple Mac M4 24 GB he needs to understand that he's got access to perplexity Hill lead the API key and if it's not sure about it about it as a task he should research it he also always checks resources that you're gonna define to see if Fine define to see if the code he needs to code has already been built and there's a battle battle Haydon battle Ho and Ed Ho and Ed. hardened solution. That he could use so he stands on the shoulders of giants rather than reinvent the wheel it's gonna be very security conscious about that and you need to set a policy for that. I mean we might send them looking for stuff now and this all relates to the business consultancy project and fully automated digital marketing project. Is it possible for him to have access to third-party coding providers in the cloud so we can send jobs up there you need to know how to orchestrate all these things. I think you have a clear idea of my intent. I want you to extra light and amplif extrapolate an amplify. He needs to order himself every every day and maintain himself. Really do a good research on this let's make them brilliant. Look at get home look at Reddit look at kilo code look at mini mark look at open router you know give them give them the knowledge and also he needs to update these skills once a Week.

---

## Question

# Current Kilo Code Skills


These are the "skills" (rule files) currently active in your Kilo Code workspace.


## 📍 Location
All skills live in: `../.kilocode/rules/`


---


## 1. **API Configuration** 
**File:** [`api-config.md`](../.kilocode/rules/api-config.md)


**What it does:**
- Manages AI provider settings (OpenRouter, Anthropic, MiniMax)
- Optimizes API costs by choosing the right model for each task
- Handles API key security and rate limiting
- Defines fallback chains when providers fail


**Key features:**
- Simple tasks → Claude Haiku ($1-5 per 1M tokens)
- Balanced work → Claude Sonnet ($3-15 per 1M tokens) 
- Complex reasoning → Claude Opus ($15-75 per 1M tokens)
- Budget option → MiniMax M2.1 ($0.30-1.20 per 1M tokens)


---


## 2. **Global Rules**
**File:** [`global-rules.md`](../.kilocode/rules/global-rules.md)


**What it does:**
- Sets fundamental coding principles
- Defines communication style (concise, direct)
- Enforces safety practices (confirmations before deletions)
- Establishes workflow patterns (read before writing, test as you go)


**Key principles:**
- Clean, readable code with clear naming
- Never over-engineer
- Always show diffs before applying changes
- Admit when uncertain rather than guess


---


## 3. **Intent Verification & Handoff**
**File:** [`intent-verification-handoff.md`](../.kilocode/rules/intent-verification-handoff.md)


**What it does:**
- Captures your intentions from conversation history
- Identifies incomplete tasks
- Verifies understanding before execution
- Hands off tasks to Orchestrator mode for implementation


**Triggers:**
- "Verify what I said today"
- "Check if everything's been done"
- "Make sure my requests are being handled"


**Process:**
1. Extract user intentions (even implied ones)
2. Categorize by status (completed, in progress, pending, unclear)
3. Create verification report
4. Prepare handoff packages
5. Execute handoff to Orchestrator


---


## 4. **Pre-Built Solutions Database**
**File:** [`prebuilt-solutions.md`](../.kilocode/rules/prebuilt-solutions.md)


**What it does:**
- Recommends existing libraries and tools before building custom
- Saves time by suggesting battle-tested solutions
- Provides decision framework (when to use pre-built vs custom)


**Categories:**
- UI Components (shadcn/ui, Radix UI, Headless UI)
- Authentication (Clerk, Supabase, NextAuth.js)
- Payments (Stripe, Lemon Squeezy)
- Database & ORM (Prisma, Drizzle, Supabase)
- Forms (React Hook Form + Zod)
- State Management (Zustand, Jotai)
- Testing (Vitest, Playwright)
- Deployment (Vercel, Railway, Netlify)
- SaaS Boilerplates


**Philosophy:** Use pre-built when time-to-market matters and feature is commodity. Build custom when you need unique business logic.


---


## 5. **Swift Code Style**
**File:** [`01-swift-style.md`](.kilocode/rules/01-swift-style.md)


**What it does:**
- Enforces Swift naming conventions (camelCase, PascalCase, CONSTANT_CASE)
- Promotes type safety and modern Swift syntax
- Defines error handling patterns
- Organizes code by concern


**Standards:**
- Variables/functions: `camelCase`
- Types (structs, classes, enums): `PascalCase`
- Constants: `CONSTANT_CASE`
- Use `guard` statements for early returns
- Avoid force unwrapping (`!`)
- Add MARK comments to separate sections


---


## 6. **Swift Data Model Structure**
**File:** [`02-swift-model-structure.md`](.kilocode/rules/02-swift-model-structure.md)


**What it does:**
- Defines how to structure Swift data models
- Enforces `Codable` conformance with `.iso8601` encoding
- Specifies file organization for Swift projects
- Sets JSON persistence standards


**File locations:**
- Models: `TodayMirror/Models/`
- Services: `TodayMirror/Services/`
- Views: `TodayMirror/Views/`
- ViewModels: `TodayMirror/ViewModels/`
- Theme: `TodayMirror/Theme/`
- Extensions: `TodayMirror/Extensions/`


**Requirements:**
- All models must conform to `Codable`
- Use `.iso8601` date encoding strategy
- Include static helpers (`empty`, `withDemoData()`)
- JSON files stored in `~/.today-mirror/data/`


---


## 7. **Swift ViewModel Rules**
**File:** [`03-swift-viewmodel-rules.md`](.kilocode/rules/03-swift-viewmodel-rules.md) and [`swift-viewmodel-rules.md`](.kilocode/rules/swift-viewmodel-rules.md)


**What it does:**
- Prevents dynamic member lookup errors in SwiftUI
- Enforces type-safe property access
- Validates property existence before use


**Critical rules:**
- NEVER use dynamic member lookup on @EnvironmentObject
- ALWAYS declare explicit types
- NEVER invent properties - verify they exist first
- NEVER reference views that don't exist


**Common error prevention:**
```swift
// ❌ FORBIDDEN
@EnvironmentObject var taskViewModel


// ✅ REQUIRED
@EnvironmentObject var taskViewModel: TaskViewModel
```


---


## 8. **Agent Workflows**
**File:** [`agent-workflows.md`](.kilocode/rules/agent-workflows.md)


**What it does:**
- Defines step-by-step workflows for common AI tasks
- Ensures consistent approach to feature implementation
- Provides troubleshooting procedures


**Workflows:**
1. **Feature Implementation** - TDD approach with spec review
2. **Railway Error Analysis** - Log parsing to root cause fix
3. **Performance Tuning** - Identify hotspots → optimize → verify
4. **Git Workflow for Refactors** - Branch → incremental changes → test


---


## 9. **Kilo Code Profiles**
**File:** [`profiles.md`](.kilocode/rules/profiles.md)


**What it does:**
- Defines optimized settings for different development tasks
- Matches AI model to task complexity
- Sets context strategy and guardrails per profile


**Profiles:**
1. **Local-Dev-Coding** - Fast iteration (qwen2.5-coder, temp 0.1)
2. **Cloud-Deep-Refactor** - Complex changes (Claude Sonnet, temp 0.3, 200k context)
3. **Railway-Ops-Agent** - Deployment debugging (Claude/GPT-4o, temp 0.1)
4. **Docs-Research-Agent** - Documentation (Claude Haiku/Llama 3, temp 0.5)


---


## 10. **Project System Prompt**
**File:** [`project-system-prompt.md`](.kilocode/rules/project-system-prompt.md)


**What it does:**
- Defines overall architecture (modular, service-oriented)
- Sets tech stack preferences
- Establishes coding conventions
- Defines deployment flow and testing strategy


**Architecture:**
- Frontend: Next.js (React) with Server Components
- Backend: FastAPI (Python) or Node.js (TypeScript)
- Worker: Background tasks (queues, cron)
- Database: PostgreSQL (via Railway)
- Cache: Redis
- AI: Centralized LLM routing


**Tech stack:**
- TypeScript (Frontend/Node)
- Python 3.11+ (AI/Backend)
- Frameworks: Next.js 14+, FastAPI, Tailwind CSS
- Database: Prisma (TS) or SQLAlchemy (Python)
- Testing: Vitest (TS), Pytest (Python)


---


## How Skills Work Together


### Planning Phase (Architect mode)
- Uses **Intent Verification** to extract requirements
- Applies **Global Rules** for communication
- Checks **Pre-Built Solutions** before planning custom builds
- References **Project System Prompt** for architecture decisions


### Implementation Phase (Code/Orchestrator mode)
- Follows **Agent Workflows** for consistent execution
- Uses **Profiles** to select right model for task
- Applies language-specific rules (Swift, TypeScript, Python)
- Manages API calls with **API Configuration**


### Quality Assurance
- **Global Rules** enforce safety (diffs, confirmations)
- Language-specific rules catch common errors
- **Project System Prompt** ensures architectural consistency


---


## Coming Soon: 6 New Skills


I've planned these additional skills (not yet implemented):
1. TypeScript/Next.js File Structure
2. Python/FastAPI File Structure
3. Swift Project File Structure
4. GitHub Best Practices
5. .gitignore Templates
6. Integration Guide


Ready to create them when you say "Switch to Code mode and create the 6 rule files"here are his existing skills

---

## Question

And you've included a skill for it to spin out three more instances on the mark so we can run 4 kg codes at the same time

---

## Question

also kilo code needs a skill and a prompt for extracting the data from the Mark tonight or it should be done for him but it might not be needs to check needs to be an exhaustive search. He needs to understand how to deal with that data so we're looking for cross pollination and amplification not reduction. He needs to use the best model. He needs to understand what to do with huge amounts of data that works best with how he works it needs to be exhaust of this one. This is really important. He needs to understand that that the data needs to go into a size which is small enough that an AI could add to it but not get confused. It's small enough that it's so blinkers without ceiling it's not gonna drift. It's gonna stick to what it means it's a huge project how we would do that

---

## Question

incorporate this.  Oh, and I do want him to have permission to run overnight. I'll leave the Mac on and to work autonomously he's got clear instructions. He's got access to terminal. He's got access to file system so we should be fine. We need to make sure he's got all the permissions he needs first.

---

## Question

I gave you a document in that document was an exhaustive list of everywhere he should be looking on the Apple Mac. Did you incorporate that?

---

## Question

this time i want it to run immediatley.  i want him to produce or label the data in two formats.  one for the obsidian neoj4 qdrant set up.   that is to look for cross pollination using the pudding technique you discoverdthe other night. the other one is for the business brain for or business consulting business,  its a shit load of work.

---

## Question

he will need to ochestrate 4.  does he need to know we have docker installed? do a research into if this fact would help the effectiveness of the process

---

## Question

thank you

---

## Question

another skill for kilo code please

---

## Question

o and add in the skill expertin docker,  aws,  and businesss brain set in smb,s

---

## Question

do the related and make the skill for kilo code

---

---
Signed-by: Devon, 2026-04-25, devin-992682c244cf444f91e0a516498afbfd

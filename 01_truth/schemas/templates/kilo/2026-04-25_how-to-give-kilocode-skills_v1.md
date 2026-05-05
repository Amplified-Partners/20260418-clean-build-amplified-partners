---
title: "How to Give Kilo Code Skills"
id: "how-to-give-kilocode-skills"
version: 1
created: "2026-04-25"
type: "document"
topic_type: "agent-tooling"
audience: "internal"
layer: "truth"
status: "filed"
signed_by: "Devon, 2026-04-25, devin-992682c244cf444f91e0a516498afbfd"
---

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
[`plans/file-structure-and-github-best-practices-plan.md`](plans/file-structure-and-github-best-practices-plan.md)

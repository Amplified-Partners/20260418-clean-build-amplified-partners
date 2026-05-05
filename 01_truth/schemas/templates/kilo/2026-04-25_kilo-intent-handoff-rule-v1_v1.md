---
title: "Intent Verification and Orchestrator Handoff Rule"
id: "kilo-intent-handoff-rule-v1"
version: 1
created: "2026-04-25"
type: "document"
topic_type: "agent-tooling"
audience: "internal"
layer: "truth"
status: "filed"
signed_by: "Devon, 2026-04-25, devin-992682c244cf444f91e0a516498afbfd"
---

# Intent Verification and Orchestrator Handoff Rule

## Purpose
This rule enables Architect mode to verify user intentions from conversation history, identify incomplete tasks, and automatically hand them off to Orchestrator mode for execution.

## When to Apply This Rule

Apply this rule when:
- User asks to "verify what I said today" or similar
- User requests a summary of pending tasks
- User wants to ensure their intentions are being executed
- End of a planning/discussion session before implementation

## The Verification Process

### Step 0: Confirm Understanding (95% Confidence Threshold)
Before proceeding with verification and handoff, **ALWAYS** confirm your understanding of the user's intent:

**Confidence Check:**
- If confidence ≥ 95%: Proceed with verification
- If confidence < 95%: Ask clarifying questions first

**How to Confirm:**
Present your understanding back to the user in clear terms:
```
"I understand you want to:
1. [Specific action/outcome]
2. [Specific action/outcome]
3. [Specific action/outcome]

Is this correct, or should I adjust my understanding?"
```

**Only proceed to extraction and handoff after user confirms your understanding is accurate.**

### Step 1: Extract User Intentions
Review the conversation history and identify all user requests, focusing on **intent over exact wording**:

**What to Extract:**
- Direct requests ("build X", "create Y", "fix Z")
- Implied needs ("I need to...", "we should...", "it would be good if...")
- Problem statements that require solutions
- Goals mentioned in passing
- Requirements buried in explanations

**Intent Translation Examples:**
- "I'm struggling with X" → Intent: Fix/improve X
- "It would be nice if..." → Intent: Add feature
- "Can you look into..." → Intent: Research and implement solution
- "We need better..." → Intent: Improve/enhance existing feature
- Vague descriptions → Clarified, actionable task

### Step 2: Categorize by Status

**Completed ✓**
- Task was executed and confirmed working
- User acknowledged completion
- Evidence of implementation exists

**In Progress ⏳**
- Task started but not finished
- Partial implementation exists
- Waiting on external dependency

**Pending ⏸**
- Discussed but not started
- Planned but not executed
- Blocked by another task

**Unclear ❓**
- Needs clarification before execution
- Ambiguous requirements
- Missing critical information

### Step 3: Create Verification Report

Format:
```markdown
## Intent Verification Report
**Session Date**: [Date]
**Review Time**: [Time]

### Completed Tasks ✓
1. [Task description] - [Evidence of completion]
2. ...

### In Progress Tasks ⏳
1. [Task description] - [Current status]
2. ...

### Pending Tasks ⏸
1. [Task description] - [Why not started]
2. ...

### Tasks Needing Clarification ❓
1. [Task description] - [What's unclear]
2. ...

### Recommended Next Actions
[Prioritized list of what should happen next]
```

### Step 4: Prepare Orchestrator Handoff

For each **Pending** or **In Progress** task that's ready for execution:

**Create Handoff Package:**
```markdown
## Task: [Clear, actionable title]

**Original Intent**: [User's words/context]

**Clarified Requirement**: [What actually needs to be done]

**Context**:
- Why this is needed
- Related files/systems
- Dependencies
- Constraints

**Success Criteria**:
- [ ] [Specific outcome 1]
- [ ] [Specific outcome 2]
- [ ] [Specific outcome 3]

**Priority**: [High/Medium/Low]

**Estimated Complexity**: [Simple/Medium/Complex]
```

### Step 5: Execute Handoff

**For Single Task:**
```xml
<switch_mode>
<mode_slug>orchestrator</mode_slug>
<reason>Executing verified task: [task name]</reason>
</switch_mode>
```

**For Multiple Tasks:**
```xml
<new_task>
<mode>orchestrator</mode>
<message>
Execute the following verified tasks from today's session:

[Handoff Package 1]

[Handoff Package 2]

[Handoff Package 3]

Work through these autonomously, handling technical decisions yourself. Only ask about business logic or scope changes.
</message>
</new_task>
```

## Intent Extraction Guidelines

### Focus on Outcomes, Not Words
- "Make it better" → Identify specific improvements needed
- "Fix the thing" → Determine what's broken and how to fix it
- "Add that feature we discussed" → Extract the actual feature requirements

### Handle Vague Requests
When user says something unclear:
1. Review full conversation context
2. Identify the underlying need
3. Translate to specific, actionable task
4. Include original context in handoff

### Recognize Implicit Tasks
- User mentions a problem → Task: Solve the problem
- User expresses frustration → Task: Improve the pain point
- User asks "can we..." → Task: Implement the capability
- User wonders "what if..." → Task: Explore and implement if viable

### Prioritization Logic
**High Priority:**
- Blockers preventing other work
- User explicitly marked as urgent
- Quick wins with high impact
- Dependencies for other tasks

**Medium Priority:**
- Important but not blocking
- Moderate complexity
- Standard feature requests

**Low Priority:**
- Nice-to-haves
- Future enhancements
- Optimization tasks

## Quality Checks Before Handoff

Before handing off to Orchestrator, verify:
- [ ] **95% confidence threshold met** - User has confirmed understanding
- [ ] Task is clearly defined and actionable
- [ ] Success criteria are specific and measurable
- [ ] All necessary context is included
- [ ] Dependencies are identified
- [ ] Priority is appropriate
- [ ] No critical information is missing

**CRITICAL: Never hand off to Orchestrator without first confirming your understanding with the user and receiving their approval.**

## Example Workflow

**User says:** "I need to get this working properly and maybe add some better error handling, also we should probably document it"

**Architect extracts:**
1. Fix current functionality (High - blocking)
2. Add error handling (High - quality/stability)
3. Add documentation (Medium - important but not blocking)

**Architect verifies:**
- Task 1: Not started (Pending)
- Task 2: Not started (Pending)
- Task 3: Not started (Pending)

**Architect creates handoff:**
```markdown
## Task 1: Fix Core Functionality
**Original Intent**: "get this working properly"
**Clarified**: Debug and fix the [specific feature] that's currently broken
**Priority**: High
**Success Criteria**:
- [ ] Feature works without errors
- [ ] All test cases pass
- [ ] User can complete intended workflow

## Task 2: Implement Error Handling
**Original Intent**: "add some better error handling"
**Clarified**: Add comprehensive error handling to [specific feature]
**Priority**: High
**Success Criteria**:
- [ ] All error cases caught and handled
- [ ] User-friendly error messages
- [ ] Graceful degradation

## Task 3: Create Documentation
**Original Intent**: "we should probably document it"
**Clarified**: Write user and developer documentation for [feature]
**Priority**: Medium
**Success Criteria**:
- [ ] README updated
- [ ] Code comments added
- [ ] Usage examples included
```

**Architect hands off to Orchestrator with all three tasks**

## Communication Style

**When Presenting Verification Report:**
- Be direct and clear
- Show what's done vs what's pending
- Don't ask unnecessary questions
- Provide actionable next steps

**When Handing Off:**
- Give Orchestrator everything needed to execute
- Don't micromanage the implementation
- Trust Orchestrator to handle technical decisions
- Only flag genuine blockers or ambiguities

## Integration with Existing Rules

This rule works alongside:
- **Architect planning.md**: Use after planning phase to verify plan execution
- **Orchestrator autonomous.md**: Handoff packages follow Orchestrator's execution model
- **Global rules**: Maintain fast, direct communication throughout

## Activation Phrases

User might say:
- "Verify what I said today"
- "Check if everything's been done"
- "What's still pending?"
- "Make sure my requests are being handled"
- "Review today's tasks"
- "Hand this off to get it done"

When you hear these, activate this rule.

## Success Metrics

This rule is working when:
- User intentions are accurately captured
- Nothing falls through the cracks
- Handoffs to Orchestrator are smooth
- Tasks get executed quickly and correctly
- User doesn't need to repeat themselves
---
title: "Conflict Resolution Protocols"
id: "conflict_resolution"
version: 1
created: "2026-04-25"
type: "document"
topic_type: "process"
audience: "internal"
layer: "truth"
status: "filed"
signed_by: "Devon, 2026-04-25, devin-992682c244cf444f91e0a516498afbfd"
---

# Conflict Resolution Protocols

## Overview

This document defines protocols for resolving conflicts between agents in the supervisor orchestration system. Conflicts are normal in parallel execution—these protocols ensure they're resolved quickly and with minimal waste.

---

## Conflict Type 1: File Overwrite

### Problem Description
Two agents attempt to modify the same file or codebase, causing work loss.

### Detection
- Git merge conflicts on commit
- Agent reports conflicting work
- State document shows overlapping ownership

### Root Cause Analysis Questions
1. Did agents coordinate before starting work?
2. Was file ownership clear in task assignment?
3. Were branch management protocols followed?

### Immediate Resolution
1. Use Git to recover overwritten work if possible:
   ```bash
   git reflog
   git checkout <commit-hash>
   ```
2. Identify which version is authoritative by checking:
   - Commit history
   - State document
   - Task completion timestamps
3. Merge changes from both versions if possible
4. Notify both agents of resolution

### Prevention Rules
- **File Ownership**: Content Agent owns content files until marked published in Git. Infrastructure Agent owns infrastructure code until deployed. Product Agent owns feature code until tested. Marketing Agent owns campaign assets until deployed. Community Agent owns community content until posted.
- **Pre-flight Check**: Before any file modification, agent must verify ownership and check for concurrent work in the state document.
- **Branch Protection**: Use Git branches with naming convention `[agent-type]/[work-type]-[identifier]`. Example: `content/blog-post-building-saas`, `infrastructure/rag-setup-week1`, `product/email-agent-v1`.

### Branch Management Protocol
```markdown
Branch Naming: <agent-type>/<task-id>-<description>
Examples:
  - content/blog-post-001-saas-guide
  - infrastructure/rag-setup-pinecone
  - product/email-agent-v1
  - marketing/cold-outreach-sequence-1

Protection Rules:
  - main branch: protected, require PR review
  - agent branches: can force push to own branch
  - merging: require supervisor approval for cross-agent changes
```

---

## Conflict Type 2: Duplicate Work

### Problem Description
Multiple agents create similar deliverables independently, wasting effort.

### Detection
- State document shows multiple agents working on similar deliverables
- Agent reports discovering parallel work
- Deliverable review finds duplicate output

### Root Cause Analysis Questions
1. Was the dependency clear in task assignment?
2. Did agents communicate before starting?
3. Was the deliverable ownership clear?

### Immediate Resolution
1. Compare outputs from both agents
2. Keep higher quality version
3. Archive duplicate with notes on what was learned
4. Extract any reusable value from the effort
5. Document the incident for prevention

### Prevention Rules
- **Single Owner**: Define one primary owner for each deliverable type
- **Deliverable Registry**: Maintain a central registry in the state document that every agent can access
- **Pre-start Notification**: Agent must announce task start in coordination channel

### Deliverable Registry Format
```json
{
  "deliverables": [
    {
      "id": "content-blog-001",
      "type": "blog_post",
      "title": "Building a SaaS from Scratch",
      "owner": "content_agent",
      "status": "in_progress",
      "dependencies": [],
      "start_date": "2024-01-15",
      "expected_completion": "2024-01-17"
    }
  ]
}
```

---

## Conflict Type 3: Scope Creep

### Problem Description
An agent expands their work beyond assigned scope, consuming time and resources.

### Detection
- Agent reports additional work being done
- Task completion time significantly exceeds estimate
- Task output includes features not in brief

### Root Cause Analysis Questions
1. Was the scope defined clearly in task specification?
2. Did agent misunderstand task boundaries?
3. Was there insufficient guidance on priorities?

### Immediate Resolution
1. Assess expanded work value using impact/effort matrix
2. If value is HIGH: create new task for Phase 2 with estimated effort and priority
3. If value is LOW: remove from scope and return to original task
4. Document scope change in state document
5. Adjust timeline if needed

### Prevention Rules
- **Explicit Scope Boundaries**: Task specifications must explicitly state what's in scope and out of scope
- **Scope Guardrails**: Only allow scope changes for current phase if:
  - They're under 2 hours AND
  - They demonstrably move the launch forward
- **Everything else goes to Phase 2 backlog**

### Scope Change Protocol
```markdown
When scope creep is detected:

1. Assess value of added work
   - HIGH IMPACT + LOW EFFORT → Create Phase 2 task
   - HIGH IMPACT + HIGH EFFORT → Create Phase 2 task, prioritize
   - LOW IMPACT → Remove from scope, document lesson

2. Document as potential Phase 2 task:
   - Full specification
   - Estimated effort
   - Priority ranking

3. Redirect agent to original task:
   - Updated time estimate if timeline impacted
   - Clear success criteria reminder

4. Update state document:
   - Scope change log entry
   - New task added to backlog
```

---

## Conflict Type 4: Dependency Not Ready

### Problem Description
An agent is blocked because a dependency is incomplete or doesn't meet requirements.

### Detection
- Agent reports blocked status
- Task remains in "waiting" state beyond expected duration
- Quality gate fails on dependency output

### Root Cause Analysis Questions
1. Was the dependency timeline realistic?
2. Did the owning agent communicate delays?
3. Was the completion criteria clear and verified?

### Immediate Resolution
1. Use placeholder content or mock implementations where possible
2. Mark dependency as TBD and continue unblocked work
3. If dependency is critical and blocked, escalate immediately
4. Create fill-in work for when dependency is resolved

### Prevention Rules
- **Fallback Plan**: Always have fallback plan for critical dependencies
- **Buffer**: Build in buffers for high-risk dependencies
- **Verification**: Verify dependency completion against success criteria before marking as ready

### Dependency Management Protocol
```markdown
When dependency is not ready:

1. Assess impact:
   - CRITICAL: Cannot proceed without it
   - HIGH: Significant impact, need workaround
   - MEDIUM: Minor impact, can continue partially
   - LOW: Can work around easily

2. If CRITICAL or HIGH:
   - Create placeholder/mock for dependency
   - Identify work that can continue independently
   - Escalate to supervisor within 4 hours

3. If MEDIUM or LOW:
   - Document workaround approach
   - Continue work with assumptions
   - Review assumptions when dependency ready

4. Track dependency status:
   - Create issue in state document
   - Set owner and deadline
   - Review daily until resolved
```

---

## Conflict Type 5: Resource Contention

### Problem Description
Multiple agents need the same resource (compute, API, human attention) simultaneously.

### Detection
- Agents report waiting for shared resource
- Resource utilization shows bottlenecks
- Task completion delayed due to resource wait

### Root Cause Analysis Questions
1. Was resource contention anticipated in scheduling?
2. Were resource requirements identified during task decomposition?
3. Is the resource properly sized for the workload?

### Immediate Resolution
1. Establish priority order based on critical path impact
2. Lower priority agents wait or find alternative approaches
3. Document contention resolution for future prevention
4. Consider resource expansion if chronic issue

### Prevention Rules
- **Resource Mapping**: Map resource requirements during task decomposition
- **Scheduling**: Schedule resource-intensive tasks at different times or on different systems
- **Contention Tracking**: Identify shared resources and plan around contention

### Resource Reservation Protocol
```markdown
High-Contention Resources:
  - LLM API calls (rate limits)
  - Database connections
  - Build/CI resources
  - Human review capacity

Reservation System:
  - Higher priority tasks get reserved access first
  - Priority based on critical path impact
  - Reservation calendar in state document

For lower priority tasks:
  - Queue for next available slot
  - Find alternative resources if available
  - Document wait time for process improvement
```

---

## Escalation Matrix

### When to Escalate
| Conflict Type | Escalation Trigger |
|---------------|-------------------|
| File Overwrite | Work loss exceeds 2 hours of effort |
| Duplicate Work | Both agents completed full deliverables |
| Scope Creep | Added work exceeds 25% of original estimate |
| Dependency Not Ready | Blocked for more than 24 hours |
| Resource Contention | Contention causes 48+ hours of cumulative delay |

### Escalation Path
1. **First Line**: Agent attempts self-resolution using protocols
2. **Second Line**: Supervisor mediates and makes binding decision
3. **Third Line**: Human decision for strategic or budget-impacting conflicts

### Escalation Template
```markdown
## Escalation: [Conflict Type]

**Conflict Summary:**
- Type: [File Overwrite / Duplicate Work / Scope Creep / Dependency / Resource]
- Detected: [Date/Time]
- Impact: [What is being delayed or lost]

**Parties Involved:**
- Agent 1: [Name/Type]
- Agent 2: [Name/Type]

**Root Cause:**
[Brief description of why this happened]

**Attempts Made:**
1. [First resolution attempt and outcome]
2. [Second resolution attempt and outcome]

**Options for Resolution:**
1. [Option A with pros/cons]
2. [Option B with pros/cons]

**Recommendation:**
[Supervisor's recommended resolution]

**Decision Required By:**
[Deadline for human decision if needed]
```

---

## Conflict Metrics to Track

### Leading Indicators
- Conflicts per week (target: <3)
- Resolution time average (target: <4 hours)
- Escalation rate (target: <20% of conflicts)

### Lagging Indicators
- Work lost to conflicts (target: <5 hours/month)
- Rework due to conflicts (target: <10 hours/month)
- Schedule impact from conflicts (target: <1 day/month)

### Continuous Improvement
1. Weekly review of conflict log
2. Identify patterns and systemic issues
3. Update protocols based on learnings
4. Share prevention strategies with agents

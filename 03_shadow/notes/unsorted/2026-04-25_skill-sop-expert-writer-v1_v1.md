---
title: "Skill: SOP Expert Writer"
id: "skill-sop-expert-writer-v1"
version: 1
created: "2026-04-25"
type: "document"
topic_type: "unsorted"
audience: "internal"
layer: "shadow"
status: "filed"
signed_by: "Devon, 2026-04-25, devin-992682c244cf444f91e0a516498afbfd"
---

# Skill: SOP Expert Writer

## Purpose
Extract and create professional Standard Operating Procedures from the knowledge base. Pulls from 22 SMB skills, expert principles, and indexed content to generate complete, actionable SOPs that ordinary people can follow.

---

## Philosophy (Gerber)

"Systems run the business. People run the systems."

Every SOP must pass the Gerber Test:
- Can someone with no prior experience follow this?
- Are the steps specific enough to eliminate guesswork?
- Does it produce consistent results every time?

---

## The Three Resources

| Resource | What to Extract | Query |
|----------|-----------------|-------|
| **Qdrant** | Process steps, checklists, workflows | `python query.py "process for X"` |
| **Neo4j** | Principles that govern the process | Same tool |
| **Obsidian** | Existing SOPs in vault | `~/vault/work-covered-ai/` |

---

## SOP Categories Available

From your 22 SMB skills:

### Finance SOPs
- Cash flow weekly review
- Invoice chasing sequence
- Debt collection escalation
- Bookkeeping daily/weekly/monthly
- Pricing review process

### Operations SOPs
- Quality control checkpoints
- Bottleneck identification
- Process documentation
- Handover procedures

### People SOPs
- Hiring workflow
- Interview scoring
- Onboarding checklist
- Training delivery
- Performance review
- Exit process

### Marketing SOPs
- Content creation workflow
- Social media posting
- Website update process
- Lead magnet delivery

### Sales SOPs
- Lead qualification
- Quote creation
- Follow-up sequence
- Objection handling
- Close process
- Customer onboarding

### Strategy SOPs
- Weekly business review
- Monthly planning
- Quarterly strategy session
- Annual planning

---

## SOP Extraction Workflow

### Step 1: Identify the Process

```bash
cd ~/knowledge-sync
source venv/bin/activate
python query.py "hiring process"
```

### Step 2: Gather Raw Material

The query returns:
- Relevant chunks from SMB skills
- Expert principles that apply

Also check:
- `~/Downloads/export_package/smb_skills/smb-hiring/SKILL.md`
- `~/vault/work-covered-ai/principle-gerber-*.md`

### Step 3: Apply the Lens Filter

For each SOP, filter through:

| Expert | SOP Question |
|--------|--------------|
| Gerber | Can an ordinary person follow this? |
| Dalio | What's the decision logic at each step? |
| Kennedy | How do we measure success? What's the deadline? |
| Lund | Does this create a good experience? |
| Ziglar | Is this done with integrity? |
| Behavioural | Where's the friction? What defaults help? |

### Step 4: Write the SOP

Use the template below.

---

## SOP Template

```markdown
# SOP: [Process Name]

**Version:** 1.0
**Owner:** [Role]
**Last Updated:** [Date]
**Review Frequency:** [Monthly/Quarterly/Annually]

---

## Purpose

One sentence: what this process achieves and why it matters.

---

## When to Use

Trigger conditions:
- When X happens
- When Y is needed
- Every [time period]

---

## Before You Start

### You Need
- [ ] Item/access/tool required
- [ ] Information required
- [ ] Approvals required

### Time Required
Approximately X minutes/hours

---

## The Process

### Step 1: [Action Verb] [What]
Specific instruction. No ambiguity.

**Do this:**
- Substep if needed
- Substep if needed

**You're done when:** [Completion criteria]

### Step 2: [Action Verb] [What]
Specific instruction.

**Decision Point:**
- IF [condition] → Do A
- IF [other condition] → Do B

**You're done when:** [Completion criteria]

### Step 3: [Action Verb] [What]
Continue pattern...

---

## Quality Check

Before finishing, verify:
- [ ] Checkpoint 1
- [ ] Checkpoint 2
- [ ] Checkpoint 3

---

## What Success Looks Like

- Metric 1: [Target]
- Metric 2: [Target]
- Outcome: [Description]

---

## Common Problems

| Problem | Solution |
|---------|----------|
| X happens | Do Y |
| Z doesn't work | Try A, then B |

---

## Escalation

If you can't complete this process:
1. First try: [Self-help option]
2. Then: Contact [Person/Role]
3. Emergency: [Contact]

---

## Version History

| Version | Date | Changes | Author |
|---------|------|---------|--------|
| 1.0 | [Date] | Initial version | [Name] |
```

---

## SOP Quality Checklist

Before finalising any SOP:

### Gerber Test
- [ ] Could a new hire follow this on day one?
- [ ] Are there fewer than 10 main steps?
- [ ] Is every step a clear action (verb + noun)?
- [ ] Are decision points clearly marked?

### Kennedy Test
- [ ] Is there a success metric?
- [ ] Is there a time expectation?
- [ ] Can we measure if it's working?

### Lund Test
- [ ] Does this respect the person doing it?
- [ ] Does this create a good client experience?
- [ ] Would someone enjoy following this?

### Behavioural Test
- [ ] Have we removed unnecessary friction?
- [ ] Are the right defaults set?
- [ ] Is the first step easy?

---

## Extraction Commands

```bash
# Start databases
docker start qdrant neo4j

# Search for process content
cd ~/knowledge-sync && source venv/bin/activate

# Finance processes
python query.py "cash flow process"
python query.py "invoice chasing steps"
python query.py "debt collection workflow"

# People processes
python query.py "hiring workflow"
python query.py "onboarding checklist"
python query.py "training process"

# Sales processes
python query.py "lead qualification"
python query.py "sales follow up"
python query.py "closing process"

# Operations processes
python query.py "quality control"
python query.py "handover process"
```

---

## SMB Skill Locations

Direct access to source material:

```
~/Downloads/export_package/smb_skills/
├── smb-bookkeeping-compliance/SKILL.md
├── smb-bottlenecks/SKILL.md
├── smb-cash-flow/SKILL.md
├── smb-debt-collection/SKILL.md
├── smb-hiring/SKILL.md
├── smb-hr-compliance/SKILL.md
├── smb-lead-generation/SKILL.md
├── smb-quality-control/SKILL.md
├── smb-sales-conversion/SKILL.md
├── smb-sops/SKILL.md
├── smb-training-onboarding/SKILL.md
└── ... (22 total)
```

---

## Output Location

Save completed SOPs to:
`~/vault/work-covered-ai/sops/`

Naming convention:
`sop-[category]-[process-name]-v1.md`

Examples:
- `sop-finance-cash-flow-weekly-review-v1.md`
- `sop-people-hiring-interview-process-v1.md`
- `sop-sales-lead-qualification-v1.md`

---

## Priority SOPs to Create

### Immediate (Week 1)
1. Client onboarding
2. Weekly business review
3. Invoice chasing sequence
4. Lead qualification

### Short-term (Month 1)
5. Hiring workflow
6. Cash flow weekly review
7. Content creation
8. Quality control

### Medium-term (Quarter 1)
9. All remaining finance SOPs
10. All remaining people SOPs
11. All remaining sales SOPs
12. All remaining operations SOPs

---

## Version History

- 2026-01-17: Created SOP Expert Writer skill

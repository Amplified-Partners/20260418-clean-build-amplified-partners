---
title: "SKILL.md Starter Template"
id: "skill-md-starter-template"
version: 1
created: 2026-04-25
last_validated: 2026-04-25
type: document
topic_type: reference
status: imported
source_file: "SKILL_md_Starter.md"
signed_by: "Devon, 2026-04-25, devin-992682c244cf444f91e0a516498afbfd"
---

# SKILL.md Starter Template
# Agent Builder Academy — agentbuilderacademy.com

## How to Use This File

A skill is an automated workflow. You define the process once — the steps, the tools, the expected output. The agent runs it on command, every time, the same way.

Place this file at: `.claude/commands/[your-skill-name].md`

One file per workflow. Keep each skill focused on one job.

When to create a skill: if a process runs daily, weekly, or monthly — automate it. If it runs a few times a year, a prompt is enough.

## Security — Read Before Running

A skill is permission for the agent to act. Running a skill can mean shell access, file system writes, environment variable reads, network calls, or deploy triggers.

- Never run a public skill without reading every step first
- Check for shell commands, remote downloads, and network calls
- Adapt any external skill to your own stack before using it
- Agentic power without review is automated risk

---

## Skill: [Skill Name]

**Purpose:** [One sentence — what this skill does]

**When to use:** [Describe the trigger condition — when should this skill be invoked]

**What it does NOT do:** [Set clear scope limits]

---

## Steps

1. [First action — be specific]
2. [Second action]
3. [Third action]
4. [Verify: what does success look like]

---

## Rules

- Always [X] before [Y]
- Never modify [Z] directly
- If [condition], stop and report to the user instead of proceeding

---

## Output Format

[Describe what the agent should produce — file path, format, confirmation message, etc.]

---

## Example Invocation

```
/[skill-name]
```

Or triggered via a Hook when: [describe the trigger condition if applicable]

---

Remove this comment block before use.
Source: Agent Builder Academy — agentbuilderacademy.com
Framework: Agent Orchestration Layer (AOL) — AOL 4 (Capable)

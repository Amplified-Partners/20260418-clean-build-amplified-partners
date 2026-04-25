---
title: "Hooks Setup Guide"
id: "hooks-setup-guide"
version: 1
created: 2026-04-25
last_validated: 2026-04-25
type: document
topic_type: reference
status: imported
source_file: "Hooks_Setup_Guide.md"
signed_by: "Devon, 2026-04-25, devin-992682c244cf444f91e0a516498afbfd"
---

# Hooks Setup Guide
# Agent Builder Academy — agentbuilderacademy.com

## What Are Hooks

Hooks are automated triggers. Instead of manually invoking a skill, you define conditions under which the agent acts on its own.

A file changes -> a hook fires.
A rule is violated -> a skill runs.
A standard slips -> the system corrects.

This is AOL 5 — the Autonomy Zone. The agent no longer waits.

---

## Where Hooks Live (Claude Code)

Hooks are configured in `.claude/settings.json` at your project root.

```json
{
  "hooks": {
    "PostToolUse": [
      {
        "matcher": "Write|Edit",
        "hooks": [
          {
            "type": "command",
            "command": "npx prettier --write \"$CLAUDE_FILE_PATHS\""
          }
        ]
      }
    ]
  }
}
```

---

## Hook Event Types

| Event | When it fires |
|-------|---------------|
| `PreToolUse` | Before a tool call executes |
| `PostToolUse` | After a tool call completes |
| `Notification` | When the agent sends a user-facing message |
| `Stop` | When the agent finishes a turn |

---

## Common Hook Patterns

### Auto-format on save
Runs Prettier after every file write.

```json
{
  "hooks": {
    "PostToolUse": [
      {
        "matcher": "Write|Edit",
        "hooks": [
          {
            "type": "command",
            "command": "npx prettier --write \"$CLAUDE_FILE_PATHS\""
          }
        ]
      }
    ]
  }
}
```

### Run type check after code changes
Catches TypeScript errors immediately.

```json
{
  "hooks": {
    "PostToolUse": [
      {
        "matcher": "Write|Edit",
        "hooks": [
          {
            "type": "command",
            "command": "npx tsc --noEmit"
          }
        ]
      }
    ]
  }
}
```

### Run tests after file changes in /src
Only runs when source files are touched.

```json
{
  "hooks": {
    "PostToolUse": [
      {
        "matcher": "Write|Edit",
        "hooks": [
          {
            "type": "command",
            "command": "if echo \"$CLAUDE_FILE_PATHS\" | grep -q '^src/'; then npm test; fi"
          }
        ]
      }
    ]
  }
}
```

---

## Environment Variables in Hooks

Claude Code exposes these variables inside hook commands:

| Variable | Value |
|----------|-------|
| `$CLAUDE_FILE_PATHS` | Space-separated list of files touched |
| `$CLAUDE_TOOL_NAME` | The tool that triggered the hook |

---

## Important Rules

1. Hooks run with your system permissions — treat them like production code.
2. Test hooks in a branch before enabling on main.
3. Keep hook commands fast — slow hooks block the agent.
4. Prefer specific matchers over broad ones.
5. Use hooks for enforcement, not for new logic. New logic belongs in a Skill.

---

## The Skill + Hook Combination

The cleanest pattern at AOL 5:

1. Write a Skill that does the work (SKILL.md)
2. Write a Hook that triggers the Skill automatically (.claude/settings.json)

The Skill defines the procedure.
The Hook decides when to run it.

This separation keeps your automation readable and maintainable.

---

Source: Agent Builder Academy — agentbuilderacademy.com
Framework: Agent Orchestration Layer (AOL) — AOL 5 (Integrated)

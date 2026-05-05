---
title: "Knowledge Watcher (launchd)"
id: "watcher_setup"
version: 1
created: "2026-04-25"
type: "document"
topic_type: "setup-guide"
audience: "internal"
layer: "build"
status: "filed"
signed_by: "Devon, 2026-04-25, devin-992682c244cf444f91e0a516498afbfd"
---

# Knowledge Watcher (launchd)

This adds an always-on watcher that monitors `/Users/ewanbramley/Knowledge/raw/` for new/changed files and runs:

1. Stage 1 labelling ([`main()`](knowledge_pipeline/stage1_label.py:320)) on just the new files
2. Stage 2 atomisation ([`main()`](knowledge_pipeline/stage2_atomise_llm.py:342)) on just the newly labelled text files

Logs are written to:

`/Users/ewanbramley/Knowledge/00-system/watcher.log`

## Install dependencies

In the repo venv:

```bash
source /Users/ewanbramley/Documents/knowledge_pipeline/venv/bin/activate
pip install watchdog
```

## Launch at login

1. Copy the plist:

```bash
mkdir -p /Users/ewanbramley/Library/LaunchAgents
cp /Users/ewanbramley/Documents/knowledge_pipeline/com.ewanbramley.knowledge-watcher.plist \
  /Users/ewanbramley/Library/LaunchAgents/
```

2. Load it:

```bash
launchctl load -w /Users/ewanbramley/Library/LaunchAgents/com.ewanbramley.knowledge-watcher.plist
```

3. Verify:

```bash
launchctl list | grep knowledge-watcher
tail -f /Users/ewanbramley/Knowledge/00-system/watcher.log
```

## Important: ANTHROPIC_API_KEY

The watcher calls Claude via [`call_claude_extract()`](knowledge_pipeline/stage2_atomise_llm.py:293), which requires `ANTHROPIC_API_KEY` to be present in the environment.

If you want `launchd` to provide it, either:

- set it once for your login session via `launchctl setenv ANTHROPIC_API_KEY ...` (recommended), or
- add an `EnvironmentVariables` dictionary to the plist.


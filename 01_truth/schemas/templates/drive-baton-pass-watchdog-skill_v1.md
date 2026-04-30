---
name: baton-pass-watchdog
description: Daily check that SESSION-STATE.md is being updated
---

Check if the baton-pass handover files are fresh. Read /Users/amplifiedpartners/vault/00-handover/SESSION-STATE.md and check when it was last updated (the "Last Updated" field at the top). If it's more than 2 days old, alert Ewan that the baton hasn't been passed. Also verify the file exists and has content. Report the status briefly.
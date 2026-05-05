---
title: "KiloCode Task: Fix Pipeline Integration Gaps"
id: "kilo-fix-pipeline-integration-v1"
version: 1
created: "2026-04-25"
type: "document"
topic_type: "agent-tooling"
audience: "internal"
layer: "truth"
status: "filed"
signed_by: "Devon, 2026-04-25, devin-992682c244cf444f91e0a516498afbfd"
---

# KiloCode Task: Fix Pipeline Integration Gaps

## Context
We have built separate components that need to be connected into one working pipeline:

```
ai-chat-sync → watcher → stage1 → stage2 → atoms → librarian → AI Studio
```

Currently these are NOT connected. Fix all gaps in this session.

---

## Current State

| Component | Location | Status |
|-----------|----------|--------|
| ai-chat-sync | `/Users/ewanbramley/Documents/ai-chat-sync/` | Working, outputs to wrong folder |
| watcher | `/Users/ewanbramley/Documents/knowledge_pipeline/watcher.py` | Running, watching wrong folder |
| stage1_label | `/Users/ewanbramley/Documents/knowledge_pipeline/stage1_label.py` | Working |
| stage2_atomise | `/Users/ewanbramley/Documents/knowledge_pipeline/stage2_atomise_llm.py` | Working |
| librarian | `/Users/ewanbramley/Projects/ai-studio/agents/src/tools/librarian.py` | Stale index (10K of 27K) |
| AI Studio | `/Users/ewanbramley/Projects/ai-studio/agents/` | Not using librarian |

---

## TASK 1: Unify Output Paths

### Problem
- ai-chat-sync outputs to: `/Users/ewanbramley/Knowledge/00_INBOX/raw/ai-chat-sync/`
- watcher watches: `~/ai-exports/`
- stage1 reads from: `/Users/ewanbramley/Knowledge/raw/`

### Solution
Standardise on ONE input path. Update ai-chat-sync to output to `~/ai-exports/{platform}/`.

**File to edit:** `/Users/ewanbramley/Documents/ai-chat-sync/src/config.ts` (or wherever `OUTPUT_BASE_DIR` is defined)

**Change:**
```typescript
// FROM:
OUTPUT_BASE_DIR: '/Users/ewanbramley/Knowledge/00_INBOX/raw/ai-chat-sync'

// TO:
OUTPUT_BASE_DIR: process.env.OUTPUT_DIR || path.join(os.homedir(), 'ai-exports')
```

**Also update** `.env` or `.env.example` to document this.

**Verify:** After change, run `npx ts-node src/index.ts --platform claude --limit 1` and confirm file appears in `~/ai-exports/claude/`.

---

## TASK 2: Update Watcher to Handle Full Flow

### Problem
Watcher calls stage1 and stage2 but paths may not align.

### Solution
Edit `/Users/ewanbramley/Documents/knowledge_pipeline/watcher.py`:

1. Confirm `WATCH_DIR = Path.home() / "ai-exports"` ✓ (already correct)

2. Update the processing flow to:
   - Copy new file from `~/ai-exports/{provider}/` to `/Knowledge/raw/{provider}/`
   - Run stage1 (labels and moves to `/Knowledge/labelled/`)
   - Run stage2 with `--ollama` flag (creates atoms in `/Knowledge/02-atoms/`)
   - Call librarian reindex

3. Add this function if not present:
```python
def reindex_librarian():
    """Trigger librarian reindex after new atoms created."""
    try:
        subprocess.run(
            ["python", "-m", "src.tools.librarian", "index"],
            cwd="/Users/ewanbramley/Projects/ai-studio/agents",
            env={**os.environ, "VIRTUAL_ENV": "/Users/ewanbramley/Projects/ai-studio/agents/venv"},
            timeout=300
        )
        logger.info("Librarian reindex complete")
    except Exception as e:
        logger.error(f"Librarian reindex failed: {e}")
```

4. Call `reindex_librarian()` after stage2 completes successfully.

---

## TASK 3: Reindex Librarian Now

### Problem
- Atoms on disk: 27,467
- Atoms indexed: 10,594

### Solution
Run this command:
```bash
cd /Users/ewanbramley/Projects/ai-studio/agents
source venv/bin/activate
python -m src.tools.librarian index
```

**Verify:** Run `python -m src.tools.librarian stats` and confirm count matches disk.

---

## TASK 4: Wire Librarian into AI Studio Pipeline

### Problem
AI Studio `main.py` doesn't query the librarian for context when generating specs or code.

### Solution
Edit `/Users/ewanbramley/Projects/ai-studio/agents/src/main.py`:

1. Add import at top:
```python
from src.tools.librarian import search_atoms, get_stats
```

2. Add a `--context` flag to the CLI:
```python
@cli.command()
@click.option('--context/--no-context', default=True, help='Query librarian for relevant context')
def spec(user_story, criteria, output, context):
    ...
```

3. Before calling the spec agent, query librarian:
```python
if context:
    # Extract key terms from user story
    results = search_atoms(user_story, limit=5)
    if results:
        context_block = "\n\n## Relevant Knowledge\n"
        for r in results:
            context_block += f"- {r['title']}: {r['snippet']}\n"
        user_story = user_story + context_block
```

4. Same pattern for `code` and `pipeline` commands.

---

## TASK 5: Add Launchd for Daily Sync

### Problem
ai-chat-sync must be run manually.

### Solution
Create `/Users/ewanbramley/Library/LaunchAgents/com.user.ai-chat-sync.plist`:

```xml
<?xml version="1.0" encoding="UTF-8"?>
<!DOCTYPE plist PUBLIC "-//Apple//DTD PLIST 1.0//EN" "http://www.apple.com/DTDs/PropertyList-1.0.dtd">
<plist version="1.0">
<dict>
    <key>Label</key>
    <string>com.user.ai-chat-sync</string>
    <key>ProgramArguments</key>
    <array>
        <string>/opt/homebrew/bin/node</string>
        <string>/Users/ewanbramley/Documents/ai-chat-sync/dist/index.js</string>
        <string>--all</string>
        <string>--limit</string>
        <string>20</string>
    </array>
    <key>StartCalendarInterval</key>
    <dict>
        <key>Hour</key>
        <integer>6</integer>
        <key>Minute</key>
        <integer>0</integer>
    </dict>
    <key>StandardOutPath</key>
    <string>/Users/ewanbramley/Documents/ai-chat-sync/data/sync.log</string>
    <key>StandardErrorPath</key>
    <string>/Users/ewanbramley/Documents/ai-chat-sync/data/sync-error.log</string>
    <key>WorkingDirectory</key>
    <string>/Users/ewanbramley/Documents/ai-chat-sync</string>
</dict>
</plist>
```

Then run:
```bash
launchctl load ~/Library/LaunchAgents/com.user.ai-chat-sync.plist
```

---

## TASK 6: Move Existing Synced Chats

### Problem
148 chats already synced to `/Knowledge/00_INBOX/raw/ai-chat-sync/` won't be processed.

### Solution
```bash
# Move existing synced chats to the watched folder
cp -r /Users/ewanbramley/Knowledge/00_INBOX/raw/ai-chat-sync/* ~/ai-exports/

# Verify
ls ~/ai-exports/claude/ | wc -l  # Should show 119
ls ~/ai-exports/chatgpt/ | wc -l  # Should show 9
ls ~/ai-exports/perplexity/ | wc -l  # Should show 20
```

The watcher will pick these up and process them.

---

## Verification Checklist

After all tasks, verify:

- [ ] `ls ~/ai-exports/claude/` shows markdown files
- [ ] Watcher is running: `ps aux | grep watcher.py`
- [ ] New atoms appearing: `find /Users/ewanbramley/Knowledge/02-atoms -mmin -5 -name "*.md" | wc -l`
- [ ] Librarian indexed all: `cd /Users/ewanbramley/Projects/ai-studio/agents && source venv/bin/activate && python -m src.tools.librarian stats`
- [ ] AI Studio uses context: `python -m src.main spec "test story" --context`
- [ ] Launchd loaded: `launchctl list | grep ai-chat-sync`

---

## Execution Order

1. TASK 3 first (quick win - reindex librarian)
2. TASK 6 (move existing files)
3. TASK 1 (fix ai-chat-sync output)
4. TASK 2 (update watcher)
5. TASK 4 (wire librarian to AI Studio)
6. TASK 5 (scheduled sync)

---

## Success State

```
ai-chat-sync (daily 6am)
       ↓
  ~/ai-exports/{platform}/
       ↓
  watcher.py (always running)
       ↓
  stage1 → /Knowledge/labelled/
       ↓
  stage2 (--ollama) → /Knowledge/02-atoms/
       ↓
  librarian reindex (auto)
       ↓
  AI Studio queries librarian for context
       ↓
  Spec → Code with YOUR knowledge built in
```

**Total effort: ~45 minutes**

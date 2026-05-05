---
title: "Today Mirror - Quick Start Card"
id: "quick_start"
version: 1
created: "2026-04-25"
type: "document"
topic_type: "unsorted"
audience: "internal"
layer: "shadow"
status: "filed"
signed_by: "Devon, 2026-04-25, devin-992682c244cf444f91e0a516498afbfd"
---

# Today Mirror - Quick Start Card

**5-Minute Setup Guide**

---

## Step 1: Install Ollama (2 minutes)

```bash
brew install ollama
ollama serve &
ollama pull qwen2.5-coder:14b
```

---

## Step 2: Create Xcode Project (2 minutes)

1. Open Xcode
2. File → New → Project
3. macOS → App
4. Name: `TodayMirror`
5. Interface: SwiftUI
6. Save in `today-mirror` folder
7. Drag all `TodayMirror/` folders into Xcode

---

## Step 3: Build & Run (1 minute)

Press `Cmd+R` in Xcode

---

## Using the App

### Choose Mode
- **Money-First:** 2 revenue, 1 delivery, 0 life
- **Balance:** 1 revenue, 1 delivery, 1 life  
- **Recovery:** 0 revenue, 1 delivery, 2 life

### Add Tasks
- Type naturally → Click "Send" → Add suggestions
- Or click "Add Manually"

### Complete Tasks
- Click checkbox → Watch animation → Task moves to Done

### End of Day
- Click "Generate Today's Summary"
- Read factual feedback
- Reflect on alignment

---

## Key Rules

✅ **Maximum 3 tasks** - Always  
✅ **Choose mode intentionally** - Commit to it  
✅ **Complete fully** - Before checking off  
✅ **Read summaries** - Learn from reality  

❌ **No 4th task** - App won't allow it  
❌ **No praise/guilt** - Just facts  
❌ **Not a todo list** - It's a focus tool  

---

## Files Created

```
~/.today-mirror/
├── config.json          # Settings
└── data/
    ├── tasks.json       # Your tasks
    ├── interactions.json # LLM chats
    └── daily_logs.json  # Summaries
```

---

## Troubleshooting

**"Today is full"** → Archive or complete a task first  
**"Cannot add more [lane]"** → Mode rules prevent it  
**"LLM offline"** → Start Ollama: `ollama serve`  

---

## Full Documentation

- **SPEC.md** - Complete specification
- **BUILD_INSTRUCTIONS.md** - Detailed setup
- **USER_GUIDE.md** - Full user manual
- **COMPLETION_SUMMARY.md** - Implementation details

---

**That's it! You're ready to use Today Mirror.**

*Focus on 3 tasks. See what actually happens. Reflect honestly.*
---
title: "Today Mirror - User Guide"
id: "user_guide"
version: 1
created: "2026-04-25"
type: "document"
topic_type: "unsorted"
audience: "internal"
layer: "shadow"
status: "filed"
signed_by: "Devon, 2026-04-25, devin-992682c244cf444f91e0a516498afbfd"
---

# Today Mirror - User Guide

**Version 0.1** | A Mac-first daily task assistant built on behavioral science

---

## What is Today Mirror?

Today Mirror helps you align your actual behavior with your stated intentions through:

- **3-Task Limit:** Focus on what truly matters (no more, no less)
- **Three Modes:** Choose your daily focus (Money-First, Balance, or Recovery)
- **Honest Feedback:** See what actually happened, not what should have happened
- **Local Privacy:** Everything stays on your Mac
- **AI Assistant:** Local LLM helps extract tasks from your thoughts

---

## Quick Start

### 1. Choose Your Mode

At the top of the app, select your mode for today:

- **Money-First:** 2 revenue tasks, 1 delivery task, 0 life tasks
- **Balance:** 1 revenue, 1 delivery, 1 life task
- **Recovery:** 0 revenue tasks, 1 delivery task, 2 life tasks

### 2. Add Your 3 Tasks

**Option A: Type naturally**
- Type what's on your mind in the input box
- Click "Send"
- The AI will suggest tasks
- Click "Add" on the ones you want

**Option B: Add manually**
- Click "Add Manually"
- Enter task title
- Choose lane (revenue/delivery/life)
- Click "Add"

### 3. Complete Tasks

- Click the checkbox when done
- Watch the subtle animation (micro-win!)
- Task moves to the "Done" column
- No popups, no praise - just progress

### 4. End of Day

- Click "Generate Today's Summary"
- Read the factual summary
- Reflect on mode alignment
- Start fresh tomorrow

---

## Understanding the Three Modes

### Money-First Mode 💰
**When to use:** Building business, financial pressure, growth phase

**Rules:**
- 2 revenue tasks (66%)
- 1 delivery task (33%)
- 0 life tasks (0%)

**Example day:**
- ✅ Close 3 sales calls (revenue)
- ✅ Launch new product (revenue)
- ✅ Ship client project (delivery)

---

### Balance Mode ⚖️
**When to use:** Steady state, maintaining equilibrium

**Rules:**
- 1 revenue task (33%)
- 1 delivery task (33%)
- 1 life task (33%)

**Example day:**
- ✅ Follow up with leads (revenue)
- ✅ Complete website updates (delivery)
- ✅ Gym session (life)

---

### Recovery Mode 🌱
**When to use:** Burnout prevention, health issues, personal crisis

**Rules:**
- 0 revenue tasks (0%)
- 1 delivery task (33%)
- 2 life tasks (66%)

**Example day:**
- ✅ Finish urgent bug fix (delivery)
- ✅ Doctor appointment (life)
- ✅ Rest and recharge (life)

---

## Task Lanes Explained

### Revenue 💰
Tasks that directly generate income:
- Sales calls
- Client meetings
- Marketing campaigns
- Product launches
- Pricing strategy

### Delivery 🚀
Tasks that fulfill commitments:
- Client work
- Project completion
- Bug fixes
- Content creation
- Product development

### Life 🌟
Tasks for personal wellbeing:
- Exercise
- Health appointments
- Family time
- Rest
- Personal development

---

## Daily Workflow

### Morning (5 minutes)
1. Open Today Mirror
2. Choose your mode
3. Add 3 tasks (or let AI suggest)
4. Start working

### During Day
- Complete tasks as you go
- Enjoy the micro-win animations
- If you need to change a task, archive it and add a new one

### Evening (2 minutes)
1. Generate today's summary
2. Read the factual feedback
3. Reflect: Did your actual mode match your intended mode?
4. Close the app

---

## Key Principles

### ✅ DO
- Stick to 3 tasks maximum
- Choose mode intentionally
- Complete tasks fully before checking off
- Read daily summaries
- Reflect on patterns weekly

### ❌ DON'T
- Try to add a 4th task (app won't let you)
- Ignore mode rules
- Check off incomplete tasks
- Expect praise or guilt
- Use it as a todo list (it's a focus tool)

---

## Understanding Feedback

### Daily Summary Format
```
You committed to 3 tasks in Balance mode.
You completed 2 tasks (1 revenue, 1 delivery).
You archived 1 task.
Your actual mode was Mixed.
```

**What this means:**
- **Committed:** What you said you'd do
- **Completed:** What you actually did
- **Archived:** What you removed
- **Actual mode:** What your actions revealed

### Mode Alignment

**Matched:** Your actions aligned with your intention ✅
**Mixed:** Your actions didn't match any mode ⚠️

This isn't good or bad - it's just information for reflection.

---

## Local LLM Integration

### What it does
- Extracts tasks from natural language
- Suggests task titles and lanes
- Runs entirely on your Mac
- No data sent to cloud

### How to use
1. Type naturally: "I need to call 3 clients, finish the website, and go to the gym"
2. Click "Send"
3. AI suggests: 
   - "Call 3 clients" [revenue]
   - "Finish website" [delivery]
   - "Go to gym" [life]
4. Click "Add" on the ones you want

### If LLM is offline
- App shows a fallback message
- You can still add tasks manually
- Everything else works normally

---

## Data Storage

### Where your data lives
```
~/.today-mirror/
├── config.json          # Your settings
└── data/
    ├── tasks.json       # All your tasks
    ├── interactions.json # LLM conversations
    └── daily_logs.json  # Daily summaries
```

### Obsidian Integration (Optional)
If you use Obsidian, Today Mirror can mirror your data:

```
~/Documents/Obsidian/TodayMirror/
├── interactions/
│   └── 2024-12-16T14-30-00Z.md
├── daily_logs/
│   └── 2024-12-16.md
└── weekly_patterns/
    └── 2024-W50.md
```

**To enable:**
1. Edit `~/.today-mirror/config.json`
2. Set `obsidianVaultPath` to your vault location
3. Restart app

---

## Tips for Success

### Week 1: Learn the System
- Try all three modes
- Get comfortable with the 3-task limit
- Notice how mode rules feel

### Week 2: Find Your Rhythm
- Identify your default mode
- Notice when you need to switch
- Pay attention to mode alignment

### Week 3: Build the Habit
- Make it part of morning routine
- Review summaries regularly
- Start noticing patterns

### Month 1: Reflect and Adjust
- Review weekly patterns
- Adjust mode usage
- Fine-tune task selection

---

## Troubleshooting

### "Today is full"
- You already have 3 tasks
- Archive one to add a new one
- Or complete one first

### "Cannot add more [lane] tasks"
- Your current mode doesn't allow it
- Switch modes if needed
- Or choose a different lane

### "LLM offline"
- Ollama isn't running
- Start it: `ollama serve`
- Or add tasks manually

### Tasks not saving
- Check ~/.today-mirror/data/ exists
- Verify write permissions
- Restart app

---

## Privacy & Security

### What stays local
- ✅ All your tasks
- ✅ All your data
- ✅ LLM processing
- ✅ Everything

### What goes to cloud
- ❌ Nothing

### Data you can access
- All JSON files are human-readable
- All Obsidian files are plain markdown
- You own and control everything

---

## Keyboard Shortcuts (Coming in v0.2)

- `Cmd+N` - Add new task
- `Cmd+1/2/3` - Switch modes
- `Cmd+S` - Generate summary
- `Cmd+,` - Settings

---

## FAQ

**Q: Why only 3 tasks?**
A: Choice overload reduces completion rates. 3 is the sweet spot.

**Q: Can I add more than 3?**
A: No. That's the point. Choose what matters most.

**Q: What if I have 10 urgent things?**
A: Pick the 3 most important. Archive the rest for tomorrow.

**Q: Why no reminders?**
A: Reminders create guilt. This app shows reality, not nags.

**Q: Can I use it for long-term planning?**
A: No. It's for TODAY only. Use other tools for planning.

**Q: What about recurring tasks?**
A: Add them fresh each day. Keeps you intentional.

**Q: Why the factual summaries?**
A: Praise and guilt are manipulative. Facts enable reflection.

---

## Getting Help

### Check the logs
- Xcode console (if running from Xcode)
- ~/.today-mirror/data/ files

### Common issues
- Ollama not running → `ollama serve`
- Models not installed → `ollama pull qwen2.5-coder:14b`
- Permissions → Check ~/.today-mirror/ directory

---

## What's Next (v0.2)

- Weekly pattern aggregation
- Task templates
- Keyboard shortcuts
- Settings UI
- Dark mode
- Export/import

---

## Philosophy

Today Mirror is built on these principles:

1. **Honesty over motivation:** Show what happened, not what should have happened
2. **Constraint breeds focus:** 3 tasks maximum, always
3. **Modes create accountability:** Declare your intention, see your reality
4. **Micro-wins over gamification:** Subtle feedback, no manipulation
5. **Privacy first:** Your data, your machine, your control

---

**Remember:** This isn't a todo list. It's a mirror. It shows you what you actually do, not what you wish you did. Use that information wisely.

---

*Today Mirror v0.1 - Built with behavioral science, not dark patterns*
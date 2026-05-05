---
title: "Xcode Project Setup - Step by Step"
id: "xcode_setup"
version: 1
created: "2026-04-25"
type: "document"
topic_type: "spec"
audience: "internal"
layer: "build"
status: "filed"
signed_by: "Devon, 2026-04-25, devin-992682c244cf444f91e0a516498afbfd"
---

# Xcode Project Setup - Step by Step

## Prerequisites
- Xcode installed (from App Store)
- All Today Mirror files in `/Users/ewanbramley/Documents/today-mirror/`

---

## Step 1: Open Xcode
1. Open **Xcode** from Applications or Spotlight
2. If you see a welcome screen, click **"Create New Project"**
3. If Xcode is already open, go to **File → New → Project**

---

## Step 2: Choose Template
1. In the template chooser, select **macOS** tab at the top
2. Select **"App"** template
3. Click **Next**

---

## Step 3: Configure Project
Fill in these exact values:

| Field | Value |
|-------|-------|
| **Product Name** | `TodayMirror` |
| **Team** | Leave as "None" (or select your team if you have one) |
| **Organization Identifier** | `com.yourdomain` (or any reverse domain) |
| **Bundle Identifier** | Will auto-fill as `com.yourdomain.TodayMirror` |
| **Interface** | **SwiftUI** ⚠️ IMPORTANT |
| **Language** | **Swift** |
| **Storage** | None (uncheck all boxes) |
| **Include Tests** | ✅ Check this box |

Click **Next**

---

## Step 4: Save Location
1. Navigate to `/Users/ewanbramley/Documents/today-mirror/`
2. **IMPORTANT:** Uncheck "Create Git repository" (we already have one)
3. Click **Create**

---

## Step 5: Delete Default Files
Xcode creates some default files we don't need. In the left sidebar (Project Navigator):

1. Right-click on **`TodayMirrorApp.swift`** → Delete → Move to Trash
2. Right-click on **`ContentView.swift`** → Delete → Move to Trash
3. Right-click on **`Assets.xcassets`** → Delete → Move to Trash (we'll add it back)

---

## Step 6: Add Our Source Files

### 6a. Add Main Source Files
1. In Finder, open `/Users/ewanbramley/Documents/today-mirror/TodayMirror/`
2. Select ALL folders and files:
   - `Models/`
   - `Services/`
   - `ViewModels/`
   - `Views/`
   - `TodayMirrorApp.swift`
   - `Assets.xcassets`
3. Drag them into Xcode's left sidebar, onto the **TodayMirror** folder (blue icon)
4. In the dialog that appears:
   - ✅ Check **"Copy items if needed"**
   - ✅ Check **"Create groups"**
   - ✅ Check **"TodayMirror"** target
   - Click **Finish**

### 6b. Add Test Files
1. In Finder, open `/Users/ewanbramley/Documents/today-mirror/TodayMirrorTests/`
2. Select `TodayMirrorTests.swift`
3. Drag it into Xcode's left sidebar, onto the **TodayMirrorTests** folder (blue icon)
4. In the dialog:
   - ✅ Check **"Copy items if needed"**
   - ✅ Check **"TodayMirrorTests"** target
   - Click **Finish**

---

## Step 7: Verify File Structure
Your Xcode project should now look like this:

```
TodayMirror/
├── Models/
│   ├── Task.swift
│   ├── AppMode.swift
│   ├── Interaction.swift
│   └── DailyLog.swift
├── Services/
│   ├── StorageService.swift
│   ├── ConfigService.swift
│   ├── ObsidianService.swift
│   └── LLMService.swift
├── ViewModels/
│   ├── TaskViewModel.swift
│   ├── LLMViewModel.swift
│   └── SummaryViewModel.swift
├── Views/
│   ├── MainView.swift
│   ├── TaskRowView.swift
│   ├── DoneStripView.swift
│   ├── ModePickerView.swift
│   └── InputView.swift
├── TodayMirrorApp.swift
└── Assets.xcassets

TodayMirrorTests/
└── TodayMirrorTests.swift
```

---

## Step 8: Build the Project
1. At the top of Xcode, next to the Play button, click the scheme dropdown
2. Select **"My Mac"** as the destination
3. Press **Cmd+B** (or click the Play button)
4. Wait for build to complete (should take 10-30 seconds)

### If Build Fails:
- Check the error messages in the bottom panel
- Most common issue: Files not added to correct target
- Solution: Select each .swift file → Right sidebar → Target Membership → Check "TodayMirror"

---

## Step 9: Run the App
1. Press **Cmd+R** (or click the Play ▶️ button)
2. The Today Mirror app should launch in a new window
3. You should see:
   - Mode selector at top (Money-First/Balance/Recovery)
   - 3 empty task slots on the left
   - Done strip on the right
   - "What's on your mind?" input at bottom
   - Summary panel (collapsed by default)

---

## Step 10: Test Basic Functionality

### Add a Task Manually:
1. Click the **"+ Add Task"** button
2. Enter title: "Test task"
3. Select lane: "Revenue"
4. Click **Add**
5. Task should appear in the left column

### Mark Task as Done:
1. Click the checkbox next to the task
2. Watch for subtle animation (0.5s)
3. Task should move to Done strip on right

### Generate Summary:
1. Click **"Generate Today's Summary"** button
2. Summary should appear in the panel
3. Should be factual, no praise/guilt

---

## Step 11: Run Unit Tests
1. Press **Cmd+U** (or Product → Test)
2. All 15+ tests should pass
3. Check test results in left sidebar (Test Navigator - diamond icon)

---

## Step 12: Verify File Creation
1. Open Finder
2. Navigate to `~/.today-mirror/data/`
3. You should see:
   - `tasks.json` (your 3 tasks)
   - `daily_logs.json` (today's summary)
4. Navigate to `~/Obsidian/MyVault/Daily/`
5. You should see today's markdown file (e.g., `2025-12-16.md`)

---

## Troubleshooting

### "Cannot find 'Task' in scope"
- **Fix:** Make sure all Model files are added to TodayMirror target
- Select file → Right sidebar → Target Membership → Check TodayMirror

### "No such module 'SwiftUI'"
- **Fix:** Make sure you selected "SwiftUI" interface when creating project
- If not, you'll need to recreate the project

### App crashes on launch
- **Fix:** Check Console output (View → Debug Area → Show Debug Area)
- Most likely: Config file path issue or Obsidian vault path doesn't exist

### LLM integration not working
- **Expected:** Will show error if Ollama not running
- **Fix:** Install Ollama: `brew install ollama && ollama serve`

---

## Next Steps After Successful Build

1. **Install Ollama** (if not already):
   ```bash
   brew install ollama
   ollama serve &
   ollama pull deepseek-chat
   ollama pull qwen2.5-coder:14b
   ```

2. **Test LLM Integration**:
   - Type in "What's on your mind?" input
   - Enter: "I need to finish the quarterly report and call the client"
   - Click submit
   - Should extract 2 tasks

3. **Run Simulations** (overnight):
   ```bash
   cd /Users/ewanbramley/Documents/today-mirror
   ./run-simulations.sh 90
   ```

4. **Read Documentation**:
   - `QUICK_START.md` - 5-minute usage guide
   - `USER_GUIDE.md` - Complete feature walkthrough
   - `PRINCIPLES.md` - Behavioral science foundation

---

## Success Criteria

✅ App builds without errors  
✅ App launches and shows dashboard  
✅ Can add 3 tasks manually  
✅ Can mark task as done (moves to Done strip)  
✅ Can generate daily summary  
✅ JSON files created in `~/.today-mirror/data/`  
✅ Markdown files created in `~/Obsidian/MyVault/Daily/`  
✅ All unit tests pass  

---

## If You Get Stuck

1. Check the error message carefully
2. Verify all files are in correct locations
3. Ensure all .swift files have TodayMirror target checked
4. Try Clean Build Folder (Shift+Cmd+K, then Cmd+B)
5. Restart Xcode if needed

The most common issue is files not being added to the correct target. Always verify Target Membership in the right sidebar.
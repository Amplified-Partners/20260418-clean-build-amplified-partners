---
title: "Simple Xcode Setup - Clean Start"
id: "simple_xcode_setup"
version: 1
created: "2026-04-25"
type: "document"
topic_type: "spec"
audience: "internal"
layer: "build"
status: "filed"
signed_by: "Devon, 2026-04-25, devin-992682c244cf444f91e0a516498afbfd"
---

# Simple Xcode Setup - Clean Start

## Current Status
✅ All confusing Xcode projects removed
✅ Your source files are safe at: `/Users/ewanbramley/Documents/today-mirror/TodayMirror/`

## File Structure (Clean)
```
/Users/ewanbramley/Documents/today-mirror/TodayMirror/
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
└── Info.plist
```

---

## Step-by-Step Setup (10 minutes)

### Step 1: Open Xcode
- Launch Xcode from Applications
- Click "Create New Project"

### Step 2: Choose Template
- Select **macOS** tab at top
- Choose **App** template
- Click **Next**

### Step 3: Configure Project
Fill in these EXACT values:

| Field | Value |
|-------|-------|
| Product Name | `TodayMirror` |
| Team | None |
| Organization Identifier | `com.yourdomain` |
| Interface | **SwiftUI** ⚠️ MUST BE SWIFTUI |
| Language | Swift |
| Testing | **XCTest** (not Swift Testing) |
| Include Tests | ✅ Check |
| Include UI Tests | ❌ Uncheck |

Click **Next**

### Step 4: Save Location
**CRITICAL:** Save in your HOME directory, NOT in today-mirror folder

1. Navigate to: `/Users/ewanbramley/`
2. Create new folder: `TodayMirrorXcode`
3. Save the project there
4. **Uncheck** "Create Git repository"
5. Click **Create**

### Step 5: Delete Default Files
Xcode creates files you don't need. In the left sidebar:

1. Right-click `ContentView.swift` → Delete → Move to Trash
2. Right-click `TodayMirrorApp.swift` → Delete → Move to Trash

### Step 6: Add Your Source Files

**Open Finder:**
1. Navigate to `/Users/ewanbramley/Documents/today-mirror/TodayMirror/`
2. You should see: Models/, Services/, ViewModels/, Views/, TodayMirrorApp.swift, Info.plist

**Add to Xcode:**
1. Select ALL folders and files (Cmd+A)
2. Drag them into Xcode's left sidebar
3. Drop them on the **TodayMirror** folder (blue icon)

**In the dialog that appears:**
- ✅ Check "Copy items if needed"
- ✅ Check "Create groups"
- ✅ Check "TodayMirror" target
- Click **Finish**

### Step 7: Verify Structure
Your Xcode sidebar should now show:
```
TodayMirror/
├── Models/
├── Services/
├── ViewModels/
├── Views/
├── TodayMirrorApp.swift
├── Info.plist
└── Assets.xcassets
```

### Step 8: Build
1. Press **Cmd+B** (or click Play button)
2. Wait for build to complete
3. If successful, press **Cmd+R** to run

---

## Success Checklist
- [ ] Xcode project created in `/Users/ewanbramley/TodayMirrorXcode/`
- [ ] Source files copied from `/Users/ewanbramley/Documents/today-mirror/TodayMirror/`
- [ ] All folders visible in Xcode sidebar (Models, Services, ViewModels, Views)
- [ ] Project builds without errors (Cmd+B)
- [ ] App runs (Cmd+R)

---

## If Something Goes Wrong
1. Close Xcode
2. Delete `/Users/ewanbramley/TodayMirrorXcode/`
3. Start again from Step 1
4. Your source files at `/Users/ewanbramley/Documents/today-mirror/TodayMirror/` are always safe

---

## Why This Location?
Saving in `/Users/ewanbramley/TodayMirrorXcode/` keeps the Xcode project completely separate from your source files, preventing any deletion issues.
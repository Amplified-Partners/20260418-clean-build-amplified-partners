---
title: "⚠️ CRITICAL: Xcode Setup Issue"
id: "xcode_critical_warning"
version: 1
created: "2026-04-25"
type: "document"
topic_type: "spec"
audience: "internal"
layer: "build"
status: "filed"
signed_by: "Devon, 2026-04-25, devin-992682c244cf444f91e0a516498afbfd"
---

# ⚠️ CRITICAL: Xcode Setup Issue

## THE PROBLEM
Every time you create an Xcode project in the `today-mirror/TodayMirror/` directory, it **deletes your source files**. This has happened twice now.

## WHY IT HAPPENS
Xcode creates a nested `TodayMirror/TodayMirror/` folder structure that conflicts with your existing source files, causing git to think they should be deleted.

## YOUR SOURCE FILES ARE SAFE (Again)
✅ I've restored them again:
- Models/ (Task.swift, AppMode.swift, etc.)
- Services/ (StorageService.swift, etc.)
- ViewModels/ (TaskViewModel.swift, etc.)
- Views/ (MainView.swift, etc.)

## THE SOLUTION: Use a Different Approach

### Option 1: Create Xcode Project in Separate Location (RECOMMENDED)
1. Create Xcode project at: `/Users/ewanbramley/Documents/TodayMirrorApp/`
2. Then add your source files from `/Users/ewanbramley/Documents/today-mirror/TodayMirror/`
3. This keeps them completely separate

### Option 2: Use Command Line to Create Project
```bash
cd /Users/ewanbramley/Documents/today-mirror
mkdir -p TodayMirror.xcodeproj
# Then manually configure in Xcode
```

### Option 3: Let Me Create a Working Xcode Project for You
I can create a properly structured Xcode project file that references your source files without moving or deleting them.

## DO NOT
❌ Create a new Xcode project in `/Users/ewanbramley/Documents/today-mirror/TodayMirror/`
❌ Let Xcode create files in the same directory as your source code
❌ Save the Xcode project where your source files are

## WHAT TO DO NOW
Tell me which option you prefer:
1. I guide you to create project in separate location
2. I create the Xcode project files for you
3. You use the AI in Xcode but in a NEW separate directory

Your source files are currently safe at:
`/Users/ewanbramley/Documents/today-mirror/TodayMirror/`
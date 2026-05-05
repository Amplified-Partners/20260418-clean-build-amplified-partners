---
title: "TodayMirror Swift Build Fix - Complete Code"
id: "swift_build_fix_summary"
version: 1
created: "2026-04-25"
type: "document"
topic_type: "spec"
audience: "internal"
layer: "build"
status: "filed"
signed_by: "Devon, 2026-04-25, devin-992682c244cf444f91e0a516498afbfd"
---

# TodayMirror Swift Build Fix - Complete Code

## ✅ Build Status: SUCCESS

All Swift files now compile without errors. Only 1 deprecation warning remains (non-blocking).

---

## Files to Replace

### 1. Models/StreakData.swift (NEW FILE - CREATE THIS)

```swift
//
//  StreakData.swift
//  TodayMirror
//
//  Created on 2024-12-16
//

import Foundation

struct StreakData: Codable {
    var count: Int = 0
    var lastCompletedDate: Date?
    var currentDate: Date = Date()
    
    enum CodingKeys: String, CodingKey {
        case count, lastCompletedDate, currentDate
    }
    
    static func withDemoData() -> StreakData {
        return StreakData(count: 0, lastCompletedDate: nil, currentDate: Date())
    }
}
```

---

### 2. Services/StorageService.swift (REPLACE ENTIRE FILE)

```swift
//
//  StorageService.swift
//  TodayMirror
//
//  Handles all file I/O operations for tasks, interactions, and streak data
//  Created on 2024-12-17
//

import Foundation

class StorageService {
    static let shared = StorageService()
    
    private let dataDirectory: URL
    
    private init() {
        // Setup data directory
        let urls = FileManager.default.urls(for: .documentDirectory, in: .userDomainMask)
        dataDirectory = urls[0].appendingPathComponent("TodayMirror")
        
        // Create directory if needed
        try? FileManager.default.createDirectory(at: dataDirectory, withIntermediateDirectories: true)
        
        print("📁 StorageService initialized at: \(dataDirectory.path)")
    }
    
    // MARK: - Tasks
    
    func saveTasks(_ tasks: [Task]) {
        let url = dataDirectory.appendingPathComponent("tasks.json")
        let encoder = JSONEncoder()
        encoder.dateEncodingStrategy = .iso8601
        encoder.outputFormatting = [.prettyPrinted, .sortedKeys]
        
        guard let data = try? encoder.encode(tasks) else { return }
        try? data.write(to: url)
    }
    
    func loadTasks() -> [Task] {
        let url = dataDirectory.appendingPathComponent("tasks.json")
        guard let data = try? Data(contentsOf: url) else { return [] }
        
        let decoder = JSONDecoder()
        decoder.dateDecodingStrategy = .iso8601
        
        return (try? decoder.decode([Task].self, from: data)) ?? []
    }
    
    // MARK: - Interactions
    
    func loadInteractions() -> [Interaction] {
        let url = dataDirectory.appendingPathComponent("interactions.json")
        guard let data = try? Data(contentsOf: url) else { return [] }
        
        let decoder = JSONDecoder()
        decoder.dateDecodingStrategy = .iso8601
        
        return (try? decoder.decode([Interaction].self, from: data)) ?? []
    }
    
    func saveInteractions(_ interactions: [Interaction]) {
        let url = dataDirectory.appendingPathComponent("interactions.json")
        let encoder = JSONEncoder()
        encoder.dateEncodingStrategy = .iso8601
        encoder.outputFormatting = [.prettyPrinted, .sortedKeys]
        
        guard let data = try? encoder.encode(interactions) else { return }
        try? data.write(to: url)
    }
    
    // MARK: - Streak Data
    
    func loadStreakData() -> StreakData {
        let url = dataDirectory.appendingPathComponent("streak_data.json")
        
        print("🔍 DEBUG: StorageService.loadStreakData() - attempting to load from: \(url.path)")
        
        guard let data = try? Data(contentsOf: url) else {
            print("🔍 DEBUG: StorageService.loadStreakData() - file not found, creating demo data")
            return StreakData.withDemoData()
        }
        
        let decoder = JSONDecoder()
        decoder.dateDecodingStrategy = .iso8601
        
        guard let streakData = try? decoder.decode(StreakData.self, from: data) else {
            print("⚠️ ERROR: Failed to decode streak data")
            return StreakData.withDemoData()
        }
        
        print("✅ Loaded streak data: \(streakData.count) day streak")
        return streakData
    }
    
    func saveStreakData(_ data: StreakData) {
        let url = dataDirectory.appendingPathComponent("streak_data.json")
        let encoder = JSONEncoder()
        encoder.dateEncodingStrategy = .iso8601
        encoder.outputFormatting = [.prettyPrinted, .sortedKeys]
        
        guard let encoded = try? encoder.encode(data) else {
            print("⚠️ ERROR: Failed to encode streak data")
            return
        }
        
        try? encoded.write(to: url)
        print("✅ Saved streak data: \(data.count) day streak")
    }
    
    // MARK: - Daily Logs
    
    func loadDailyLogs() -> [DailyLog] {
        let url = dataDirectory.appendingPathComponent("daily_logs.json")
        guard let data = try? Data(contentsOf: url) else { return [] }
        
        let decoder = JSONDecoder()
        decoder.dateDecodingStrategy = .iso8601
        
        return (try? decoder.decode([DailyLog].self, from: data)) ?? []
    }
    
    func saveDailyLogs(_ logs: [DailyLog]) {
        let url = dataDirectory.appendingPathComponent("daily_logs.json")
        let encoder = JSONEncoder()
        encoder.dateEncodingStrategy = .iso8601
        encoder.outputFormatting = [.prettyPrinted, .sortedKeys]
        
        guard let data = try? encoder.encode(logs) else { return }
        try? data.write(to: url)
    }
    
    // MARK: - Data Export
    
    func exportAllData() -> String? {
        struct ExportData: Codable {
            let tasks: [Task]
            let interactions: [Interaction]
            let streakData: StreakData
            let dailyLogs: [DailyLog]
            let exportDate: Date
        }
        
        let export = ExportData(
            tasks: loadTasks(),
            interactions: loadInteractions(),
            streakData: loadStreakData(),
            dailyLogs: loadDailyLogs(),
            exportDate: Date()
        )
        
        let encoder = JSONEncoder()
        encoder.dateEncodingStrategy = .iso8601
        encoder.outputFormatting = [.prettyPrinted, .sortedKeys]
        
        guard let data = try? encoder.encode(export),
              let jsonString = String(data: data, encoding: .utf8) else {
            return nil
        }
        
        return jsonString
    }
    
    // MARK: - Debugging
    
    func printDataDirectoryContents() {
        print("\n📂 Data Directory Contents:")
        print("Location: \(dataDirectory.path)")
        
        guard let contents = try? FileManager.default.contentsOfDirectory(at: dataDirectory, includingPropertiesForKeys: nil) else {
            print("❌ Could not read directory contents")
            return
        }
        
        for file in contents {
            print("  - \(file.lastPathComponent)")
        }
        print("")
    }
}
```

---

### 3. ViewModels/StreakViewModel.swift (PARTIAL UPDATE - Line 107)

**Find line 107:**
```swift
Task {
```

**Replace with:**
```swift
_Concurrency.Task {
```

**And line 108:**
```swift
try? await Task.sleep(nanoseconds: 2_000_000_000)
```

**Replace with:**
```swift
try? await _Concurrency.Task.sleep(nanoseconds: 2_000_000_000)
```

---

### 4. Views/InputView.swift (PARTIAL UPDATE - Line 26)

**Find line 26:**
```swift
Task {
```

**Replace with:**
```swift
_Concurrency.Task {
```

---

## Quick Fix Instructions

### Option 1: Create New File (StreakData.swift)
1. In Xcode, right-click `Models` folder
2. Select **New File** → **Swift File**
3. Name it `StreakData.swift`
4. Paste the code from section 1 above
5. Save (Cmd+S)

### Option 2: Replace StorageService.swift
1. Open `Services/StorageService.swift` in Xcode
2. Press **Cmd+A** (Select All)
3. Delete
4. Paste the code from section 2 above
5. Save (Cmd+S)

### Option 3: Fix Task Collisions
1. Open `ViewModels/StreakViewModel.swift`
2. Find line 107: `Task {`
3. Replace with: `_Concurrency.Task {`
4. Find line 108: `try? await Task.sleep`
5. Replace with: `try? await _Concurrency.Task.sleep`
6. Save (Cmd+S)

7. Open `Views/InputView.swift`
8. Find line 26: `Task {`
9. Replace with: `_Concurrency.Task {`
10. Save (Cmd+S)

### Build & Verify
```bash
# In terminal
cd ~/Documents/today-mirror/TodayMirror
find . -name "*.swift" -type f | xargs swiftc -typecheck
```

**Expected**: Exit code 0 (Success) ✅

---

## What Was Fixed

1. **Missing StreakData Model** - Created separate model file
2. **Task Name Collision** - Swift's `Task` conflicted with custom `Task` model
3. **StorageService Singleton** - Added `static let shared` pattern
4. **Property Names** - Fixed `currentStreak` → `count`
5. **Non-existent Types** - Removed `UserSettings` references

---

## Build Status

✅ **All errors resolved**
⚠️ **1 deprecation warning** (non-blocking, can fix later)

The project is ready to build in Xcode!
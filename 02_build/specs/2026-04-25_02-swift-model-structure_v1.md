---
title: "Swift Data Model Requirements"
id: "02-swift-model-structure"
version: 1
created: "2026-04-25"
type: "document"
topic_type: "spec"
audience: "internal"
layer: "build"
status: "filed"
signed_by: "Devon, 2026-04-25, devin-992682c244cf444f91e0a516498afbfd"
---

# Swift Data Model Requirements

## Codable Structs
All persisted models MUST conform to `Codable` and use `.iso8601` date encoding.

When creating new models:
1. Define in a separate file with clear naming: `ModelName.swift`
2. Add static helper methods (`empty`, `withDemoData()`) for common states
3. Ensure all Date properties are compatible with iso8601 encoding strategy

Example:
```swift
struct StreakData: Codable {
    var currentStreak: Int
    var longestStreak: Int
    var lastCompletedDate: Date?
    
    static let empty = StreakData(
        currentStreak: 0,
        longestStreak: 0,
        lastCompletedDate: nil
    )
    
    static func withDemoData() -> StreakData {
        // Return demo data for first-time users
    }
}
```

## File Locations
- Models: `TodayMirror/Models/`
- Services: `TodayMirror/Services/`
- Views: `TodayMirror/Views/`
- ViewModels: `TodayMirror/ViewModels/`
- Theme: `TodayMirror/Theme/`
- Extensions: `TodayMirror/Extensions/`

## JSON Persistence
- All JSON files stored in `~/.today-mirror/data/`
- File naming: `model_name.json` (snake_case)
- Pretty-printed with sorted keys for debugging
- Use JSONEncoder/JSONDecoder with `.iso8601` date strategy

## Target Membership
- Always verify new files are added to the correct Xcode target
- Check File Inspector → Target Membership
- Models must be visible to Services and ViewModels
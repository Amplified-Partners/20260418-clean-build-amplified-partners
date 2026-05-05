---
title: "Section 1: Immediate Edits - Implementation Guide"
id: "section_1_changes"
version: 1
created: "2026-04-25"
type: "document"
topic_type: "unsorted"
audience: "internal"
layer: "shadow"
status: "filed"
signed_by: "Devon, 2026-04-25, devin-992682c244cf444f91e0a516498afbfd"
---

# Section 1: Immediate Edits - Implementation Guide

**Status:** Ready for Code mode implementation  
**Date:** 2024-12-16

---

## 1. Obsidian Daily Folder Wiring

### Change 1: ConfigService.swift Default Path
**File:** `TodayMirror/Services/ConfigService.swift`  
**Line:** 18  
**Current:**
```swift
obsidianVaultPath: NSHomeDirectory() + "/Documents/Obsidian/TodayMirror",
```

**Change to:**
```swift
obsidianVaultPath: NSHomeDirectory() + "/Obsidian/MyVault/Daily",
```

**Reason:** User's actual Obsidian Daily folder path, not a subdirectory.

---

### Change 2: ObsidianService.swift - Remove Subdirectories
**File:** `TodayMirror/Services/ObsidianService.swift`  
**Lines:** 28-39

**Current:** Creates subdirectories (interactions/, daily_logs/, weekly_patterns/)

**Change to:** Write directly to Daily folder, no subdirectories

**New setupDirectories() method:**
```swift
private func setupDirectories() {
    guard let vaultPath = vaultPath else { return }
    
    // Ensure Daily folder exists (user should have created it)
    if !fileManager.fileExists(atPath: vaultPath.path) {
        print("Warning: Obsidian Daily folder not found at \(vaultPath.path)")
        print("Please create this folder in your Obsidian vault or update config.json")
    }
}
```

---

### Change 3: ObsidianService.swift - Write to Daily Folder
**File:** `TodayMirror/Services/ObsidianService.swift`  
**Method:** `writeDailyLog()`  
**Lines:** 87-135

**Current:** Writes to `daily_logs/YYYY-MM-DD.md`

**Change to:** Write directly to `YYYY-MM-DD.md` in Daily folder

**Updated method:**
```swift
func writeDailyLog(_ log: DailyLog) {
    guard let vaultPath = vaultPath else { return }
    
    let filename = "\(log.date).md"
    let url = vaultPath.appendingPathComponent(filename)
    
    // Check if file exists (user may have existing daily note)
    var existingContent = ""
    if fileManager.fileExists(atPath: url.path) {
        existingContent = (try? String(contentsOf: url, encoding: .utf8)) ?? ""
    }
    
    var markdown = """
    
    ---
    
    ## Today Mirror
    
    **Mode Set:** \(log.modeSet.displayName)  
    **Mode Actual:** \(log.modeActual.capitalized)
    
    **Tasks:**
    - Committed: \(log.tasksCommitted.count)
    - Completed: \(log.tasksCompleted.count)
    - Archived: \(log.tasksArchived.count)
    
    ### Completed Tasks
    
    """
    
    for task in log.tasksCompleted {
        markdown += "- [x] \(task.title) [\(task.lane.rawValue)]\n"
    }
    
    if !log.tasksArchived.isEmpty {
        markdown += "\n### Archived Tasks\n\n"
        for task in log.tasksArchived {
            markdown += "- [-] \(task.title) [\(task.lane.rawValue)]\n"
        }
    }
    
    markdown += "\n**Summary:** \(log.summaryText)\n"
    
    if let notes = log.patternNotes {
        markdown += "\n**Notes:** \(notes)\n"
    }
    
    // Append to existing content or create new
    let finalContent = existingContent.isEmpty ? markdown : existingContent + markdown
    
    try? finalContent.write(to: url, atomically: true, encoding: .utf8)
}
```

---

### Change 4: Remove Interaction Writing (Not Needed for v1)
**File:** `TodayMirror/Services/ObsidianService.swift`  
**Method:** `writeInteraction()`  
**Lines:** 42-83

**Action:** Comment out or remove this method for v1. Interactions don't need separate files in Daily folder.

**Reason:** Daily note should only contain the daily summary, not every LLM interaction.

---

## 2. Language Audit - Remove Guilt/Praise

### Files to Check:
1. ✅ `SummaryViewModel.swift` - Already factual (lines 75-106)
2. ✅ `MainView.swift` - No praise language found
3. ✅ `TaskRowView.swift` - No text on completion (animation only)
4. ✅ `InputView.swift` - Neutral prompts
5. ✅ `DoneStripView.swift` - Just displays tasks

### Verification:
All existing code already follows PRINCIPLES.md. No guilt/praise language found.

**Forbidden patterns checked:**
- ❌ "Great job!" - NOT FOUND
- ❌ "Keep it up!" - NOT FOUND
- ❌ "You should..." - NOT FOUND
- ❌ "Try harder" - NOT FOUND
- ❌ "Don't give up" - NOT FOUND

**Factual patterns confirmed:**
- ✅ "You committed to X tasks" - PRESENT
- ✅ "You completed Y tasks" - PRESENT
- ✅ "Your actual mode was Z" - PRESENT

---

## 3. Summary of Section 1 Changes

### Completed:
- [x] Created PRINCIPLES.md with 10 evidence-based principles
- [x] Audited all code for guilt/praise language (none found)

### Ready for Code Mode:
- [ ] Update ConfigService.swift default path
- [ ] Modify ObsidianService.swift to write to Daily folder directly
- [ ] Remove subdirectory creation
- [ ] Append to existing daily notes instead of overwriting
- [ ] Comment out writeInteraction() method

---

## Next Steps

1. **Switch to Code mode** to implement the 4 Swift file changes above
2. **Test** that daily notes are written to correct location
3. **Proceed to Section 2** (UX refinement + personas + simulations)

---

**Estimated Time:** 15 minutes in Code mode  
**Risk Level:** Low (only config and file path changes)
---
title: "Swift ViewModel & Environment Object Rules"
id: "swift-viewmodel-rules"
version: 1
created: "2026-04-25"
type: "document"
topic_type: "spec"
audience: "internal"
layer: "build"
status: "filed"
signed_by: "Devon, 2026-04-25, devin-992682c244cf444f91e0a516498afbfd"
---

# Swift ViewModel & Environment Object Rules

## CRITICAL: No Dynamic Member Lookup

**NEVER use dynamic member lookup on environment objects.**

### ❌ FORBIDDEN
```swift
// DO NOT DO THIS - causes "requires wrapper 'EnvironmentObject'" errors
@EnvironmentObject var taskViewModel
let tasks = taskViewModel.completedTasks  // Dynamic lookup
```

### ✅ REQUIRED
```swift
// ALWAYS declare explicit types
@EnvironmentObject var taskViewModel: TaskViewModel
let tasks = taskViewModel.doneTasks  // Strongly typed, real property
```

## Property Verification Rule

**NEVER invent properties on ViewModels.**

Before referencing ANY property on a ViewModel:
1. Read the ViewModel file to verify the property exists
2. Use the EXACT property name as defined
3. If the property doesn't exist, either:
   - Use existing properties to compute what you need
   - Add the property to the ViewModel explicitly

### Example
If you need completed tasks:
1. Check TaskViewModel for existing properties
2. Found: `doneTasks` (line 29-31)
3. Use: `taskViewModel.doneTasks` ✅
4. NOT: `taskViewModel.completedTasks` ❌ (doesn't exist)

## View Reference Rule

**NEVER reference views that don't exist.**

Before using a view like `DoneStripView`:
1. Check if the file exists
2. If it doesn't exist, either:
   - Create a minimal stub implementation
   - Comment the line with `// TODO: implement DoneStripView`

## Type Safety Rule

**All access must be strongly typed.**

- No `subscript(dynamicMember:)` usage
- No reliance on dynamic member lookup
- All properties must resolve at compile time
- Treat unresolved identifier warnings as blockers

## Enforcement

Any code that violates these rules will cause compilation errors:
- "Referencing subscript 'subscript(dynamicMember:)' requires wrapper 'EnvironmentObject<…>'"
- "Value of type 'X' has no dynamic member 'Y' using key path"

These errors are ALWAYS caused by:
1. Missing type annotation on @EnvironmentObject
2. Referencing non-existent properties
3. Using dynamic member lookup instead of explicit access
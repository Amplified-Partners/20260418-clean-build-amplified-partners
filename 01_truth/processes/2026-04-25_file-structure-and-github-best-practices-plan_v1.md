---
title: "File Structure & GitHub Best Practices - Implementation Plan"
id: "file-structure-and-github-best-practices-plan"
version: 1
created: "2026-04-25"
type: "document"
topic_type: "process"
audience: "internal"
layer: "truth"
status: "filed"
signed_by: "Devon, 2026-04-25, devin-992682c244cf444f91e0a516498afbfd"
---

# File Structure & GitHub Best Practices - Implementation Plan

## Overview
This plan defines comprehensive rules for enforcing consistent file structures and GitHub best practices across all Kilo Code projects.

## Approach

### File Structure Enforcement
Create language/framework-specific rules that define:
- Standard directory layouts
- File naming conventions
- Module organization patterns
- Where different types of files belong

### GitHub Best Practices
Define standards for:
- Commit message formatting (Conventional Commits)
- Branch naming patterns
- PR templates and review processes
- `.gitignore` patterns
- README and documentation requirements

### Enforcement Strategy
- **Strict** for safety-critical items (`.gitignore`, secrets, destructive operations)
- **Advisory** for style and organization (with clear recommendations)
- **Contextual** warnings when deviations detected

---

## Deliverables

### 1. TypeScript/Next.js File Structure Rules
**File**: `.kilocode/rules/file-structure-typescript-nextjs.md`

**Contents**:
- Standard Next.js 14+ directory structure
- Component organization (shadcn/ui compatible)
- API routes and server actions placement
- Type definitions and interfaces location
- Testing file placement
- Configuration file locations

### 2. Python/FastAPI File Structure Rules
**File**: `.kilocode/rules/file-structure-python-fastapi.md`

**Contents**:
- FastAPI project layout
- Module and package organization
- Router and endpoint structuring
- Models, schemas, and database files
- Testing directory structure
- Configuration and environment handling

### 3. Swift Project File Structure Rules
**File**: `.kilocode/rules/file-structure-swift.md`

**Contents**:
- Xcode project organization
- Model-View-ViewModel (MVVM) structure
- Services and networking layer
- Extensions and utilities
- Resources and assets
- Testing targets

### 4. GitHub Best Practices
**File**: `.kilocode/rules/github-best-practices.md`

**Contents**:
- Conventional Commits specification
- Branch naming conventions (feature/, bugfix/, hotfix/, etc.)
- PR templates and checklists
- Code review guidelines
- Repository standards (README, LICENSE, CONTRIBUTING)
- Security practices (secrets, API keys)

### 5. .gitignore Templates
**File**: `.kilocode/rules/gitignore-templates.md`

**Contents**:
- TypeScript/Node.js ignore patterns
- Python ignore patterns
- Swift/Xcode ignore patterns
- OS-specific patterns
- IDE-specific patterns
- Security-critical patterns (keys, tokens, credentials)

### 6. Rules Summary & Integration Guide
**File**: `.kilocode/rules/README-file-structure-github.md`

**Contents**:
- Overview of all file structure and GitHub rules
- How rules work together
- When each rule applies
- Quick reference guide
- Examples of compliant vs non-compliant structures

---

## Integration with Existing Rules

### Complements
- **global-rules.md**: Adds specific structure enforcement to general coding quality
- **project-system-prompt.md**: Provides concrete implementation of architectural patterns
- **prebuilt-solutions.md**: File structure compatible with recommended tools

### Extends
- Swift-specific rules (01-swift-style.md, 02-swift-model-structure.md) with full project layout
- API configuration with proper environment file handling

---

## Enforcement Examples

### File Placement Check
```markdown
**BEFORE creating a file, verify:**
1. Does the file type have a designated location in the rules?
2. Is the file in the correct directory for its project type?
3. Does the filename follow the naming convention?

If NO to any: Follow the rule or flag the deviation with reasoning.
```

### Git Commit Validation
```markdown
**BEFORE committing:**
1. Does commit message follow Conventional Commits format?
2. Are all secrets/keys excluded (check .gitignore)?
3. Is the branch name correctly formatted?

If NO to any: Show the correct format and explain why.
```

---

## Success Metrics

These rules are working when:
- ✅ All new files are created in the correct locations automatically
- ✅ Commit messages follow Conventional Commits without reminders
- ✅ No secrets or API keys ever get committed
- ✅ PRs include all required information
- ✅ Project structure is consistent across similar projects
- ✅ New team members can navigate any project immediately

---

## Next Steps

1. Create each rule file with comprehensive, practical guidelines
2. Include examples (both good and bad) in each rule
3. Reference from mode-specific instructions where appropriate
4. Test with sample project structures
5. Iterate based on real-world usage

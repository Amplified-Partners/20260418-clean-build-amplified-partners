---
title: "KILO CODE PROMPT: Investigate and Rename Downloads Folder Files"
id: "kilo-downloads-rename-prompt-v1"
version: 1
created: "2026-04-25"
type: "document"
topic_type: "agent-tooling"
audience: "internal"
layer: "truth"
status: "filed"
signed_by: "Devon, 2026-04-25, devin-992682c244cf444f91e0a516498afbfd"
---

# KILO CODE PROMPT: Investigate and Rename Downloads Folder Files

## Context

You are working on Ewan's M4 MacBook Air. The Downloads folder at `~/Downloads/` contains approximately 282 files with unclear, auto-generated, or poorly descriptive names.

**Goal:** Investigate each file's actual content and rename it with a clear, succinct, functional name that describes what the file contains.

**Naming Convention:** `category-topic-type-v1.ext`

Examples:
- `perplexity-rag-architecture-guide-v1.md`
- `covered-ai-business-vision-v1.md`
- `claude-desktop-setup-guide-v1.docx`
- `screenshot-kilo-code-error-20260118.png`

---

## Constraints

- Do NOT delete any files
- Do NOT move files to other folders (renaming only)
- Do NOT rename system files (`.DS_Store`, `.localized`, etc.)
- Do NOT rename incomplete downloads (`.crdownload` files)
- Preserve file extensions exactly
- Use lowercase and hyphens only (no spaces, no underscores)
- Maximum filename length: 60 characters (excluding extension)

---

## Categories to Use

| Category Prefix | Use For |
|-----------------|---------|
| `business-` | Business plans, strategies, visions, consulting |
| `tech-` | Technical guides, architecture, code documentation |
| `kilo-` | Kilo Code specific content |
| `claude-` | Claude AI specific content |
| `perplexity-` | Perplexity exports and research |
| `covered-` | covered.AI specific business content |
| `byker-` | Byker Business Help specific content |
| `guide-` | How-to guides, tutorials, setup instructions |
| `research-` | Research documents, analysis |
| `transcript-` | Voice transcripts, meeting notes |
| `screenshot-` | Screenshots (append date YYYYMMDD) |
| `installer-` | DMG, PKG, and other installers |
| `export-` | Exported data from apps |
| `asset-` | Images, graphics, media assets |
| `misc-` | Uncategorizable files |

---

## Task: Execute in Phases

### Phase 1: Inventory (Read-Only)

List all files in `~/Downloads/` excluding:
- Hidden files (starting with `.`)
- Incomplete downloads (`*.crdownload`)
- Directories

```bash
find ~/Downloads -maxdepth 1 -type f ! -name ".*" ! -name "*.crdownload" | wc -l
```

Create inventory showing current name and file type:

```bash
find ~/Downloads -maxdepth 1 -type f ! -name ".*" ! -name "*.crdownload" -exec basename {} \; | sort
```

### Phase 2: Analyze Content (Read-Only)

For each file, determine content by:

**For `.md` files:**
```bash
head -20 "$file"
```

**For `.pdf` files:**
```bash
pdftotext "$file" - 2>/dev/null | head -30
```

**For `.docx` files:**
```bash
unzip -p "$file" word/document.xml 2>/dev/null | sed 's/<[^>]*>//g' | head -30
```

**For `.png`, `.jpg`, `.jpeg` files:**
- Check if filename contains "Screenshot" → category is `screenshot-`
- Otherwise → category is `asset-`

**For `.dmg` files:**
- Extract app name from filename → category is `installer-`

**For `.zip` files:**
```bash
unzip -l "$file" 2>/dev/null | head -10
```

### Phase 3: Generate Rename Map

Create a rename map file at `~/Downloads/_rename-map.txt` with format:

```
ORIGINAL: [original filename]
CONTENT SUMMARY: [1-sentence description of actual content]
NEW NAME: [proposed new filename]
CONFIDENCE: [HIGH/MEDIUM/LOW]
---
```

**Rules for generating new names:**

1. Read the first 500 characters or first heading
2. Identify the PRIMARY topic (what is this about?)
3. Identify the TYPE (guide, plan, research, export, etc.)
4. Combine: `category-topic-type-v1.ext`
5. If content is unclear, use `misc-` prefix and LOW confidence

**Example entries:**

```
ORIGINAL: I want you to do a very deep research into the opt.md
CONTENT SUMMARY: Perplexity research on optimal RAG architecture options
NEW NAME: perplexity-rag-architecture-research-v1.md
CONFIDENCE: HIGH
---

ORIGINAL: BUSINESS-VISION-covered-ai-full-v1.md
CONTENT SUMMARY: Complete covered.AI business vision document
NEW NAME: covered-business-vision-full-v1.md
CONFIDENCE: HIGH
---

ORIGINAL: Unconfirmed 102454.crdownload
CONTENT SUMMARY: Incomplete download
NEW NAME: [SKIP - incomplete download]
CONFIDENCE: N/A
---
```

### Phase 4: Review Checkpoint

**STOP HERE AND PRESENT THE RENAME MAP TO EWAN.**

Output format:
```
RENAME MAP GENERATED
Total files analyzed: [N]
High confidence renames: [N]
Medium confidence renames: [N]
Low confidence renames: [N]
Skipped (incomplete/system): [N]

File: ~/Downloads/_rename-map.txt

AWAITING APPROVAL before executing renames.
Reply "PROCEED" to execute all renames.
Reply "PROCEED HIGH ONLY" to execute only high-confidence renames.
Reply "REVIEW [filename]" to see details for a specific file.
Reply "EDIT [original] -> [new name]" to override a rename.
Reply "SKIP [filename]" to exclude a file from renaming.
```

### Phase 5: Execute Renames (Only After Approval)

For each approved rename:

```bash
mv ~/Downloads/"$ORIGINAL" ~/Downloads/"$NEW_NAME"
```

Log each rename to `~/Downloads/_rename-log.txt`:

```
[TIMESTAMP] RENAMED: "$ORIGINAL" -> "$NEW_NAME"
```

### Phase 6: Final Report

After all renames complete:

```
RENAME COMPLETE
Total files renamed: [N]
Skipped: [N]
Errors: [N]

Log file: ~/Downloads/_rename-log.txt
Rename map: ~/Downloads/_rename-map.txt

Files that could not be renamed:
- [list any errors]
```

---

## Special Handling Rules

### Perplexity Exports (truncated AI titles)

Files like `I want you to do a very deep research into the opt.md` are Perplexity exports with truncated titles.

1. Read full content
2. Extract the actual research topic
3. Rename as `perplexity-[topic]-research-v1.md`

### Screenshot Files

Files matching `Screenshot*.png`:
1. Extract date from filename if present
2. Analyze image if possible (check for text, UI elements)
3. Rename as `screenshot-[context]-[YYYYMMDD].png`
4. If context unclear, use `screenshot-unknown-[YYYYMMDD].png`

### Duplicate Detection

If two files would get the same new name:
1. Append `-a`, `-b`, `-c` suffix before `.ext`
2. Note in rename map: `DUPLICATE: See also [other file]`

### Already Well-Named Files

If a file already follows the naming convention:
1. Mark as `[SKIP - already well-named]`
2. Do not rename

---

## Output Format for Each Step

```
PHASE [N]: [description]
STATUS: ✅ Complete | ⚠️ Warning | ❌ Failed
FILES PROCESSED: [N]
OUTPUT: [summary or "see file"]
```

---

## Safety Checklist

Before executing ANY rename:

- [ ] Rename map file exists at `~/Downloads/_rename-map.txt`
- [ ] User has reviewed and approved the map
- [ ] Backup reminder given: "Consider copying important files before bulk rename"
- [ ] Each rename logged to `~/Downloads/_rename-log.txt`

---

## Begin Execution

Start with Phase 1: Inventory.

Report file count and await confirmation before proceeding to Phase 2.

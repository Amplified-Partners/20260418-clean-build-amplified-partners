---
title: "Kilo Code Prompts for Atomiser Implementation"
id: "kilo_prompts"
version: 1
created: "2026-04-25"
type: "document"
topic_type: "agent-tooling"
audience: "internal"
layer: "truth"
status: "filed"
signed_by: "Devon, 2026-04-25, devin-992682c244cf444f91e0a516498afbfd"
---

# Kilo Code Prompts for Atomiser Implementation

## PROMPT 1: Initial Setup & Understanding
```
Read ATOMISER_SPEC.md and stage1_label.py. Then explain back to me:
1. What the atomiser needs to do
2. What patterns from stage1 you'll reuse
3. Your proposed architecture for stage2_atomise_llm.py
```

## PROMPT 2: Implement Core Structure
```
Create stage2_atomise_llm.py with:
1. File iteration (reuse iter_files, is_excluded from stage1)
2. Frontmatter parsing (reuse split_frontmatter)  
3. Argument parsing: --labelled, --atomised, --limit, --dry-run, --model
4. Main loop structure with error handling
5. Placeholder for LLM extraction (just print "would extract from: {path}" for now)

Make it runnable with: python stage2_atomise_llm.py --dry-run --limit 5
```

## PROMPT 3: Design Extraction Prompt
```
Design the Claude extraction prompt. It must:
- Input: document text (cleaned of markdown formatting)
- Output: JSON array of atoms
- Each atom has: title, type, body, tags
- Types: fact, insight, principle, decision, action, definition, reference
- Body: 20-60 words, self-contained, one idea only

Write the prompt as a Python string constant EXTRACTION_PROMPT. 
Include few-shot examples of good atoms.
```

## PROMPT 4: Implement LLM Extraction
```
Add the Claude API integration:
1. anthropic.Anthropic() client setup
2. extract_atoms(text: str, source_tags: list) -> list[dict] function
3. Call Claude with EXTRACTION_PROMPT
4. Parse JSON response, validate each atom
5. Handle API errors and rate limits

Use claude-3-5-sonnet-20241022 as default model.
```

## PROMPT 5: Implement Atom Writing
```
Add atom file writing:
1. slug_filename(title, hash) function
2. write_atom(dest, title, type, source, tags, body) function  
3. content_hash() for deduplication
4. Track written hashes to skip duplicates

Each atom file should have proper YAML frontmatter.
```

## PROMPT 6: Add Progress & Logging
```
Add:
1. Progress bar or counter (print every 10 files)
2. Token usage tracking per API call
3. Summary at end: files processed, atoms created, errors, total tokens
4. Optional --verbose flag for detailed logging
```

## PROMPT 7: Test & Debug
```
Run: python stage2_atomise_llm.py --dry-run --limit 10

Check:
1. Does it find the right files?
2. Does the extraction prompt work?
3. Are atoms properly formatted?
4. Fix any issues you find.
```

## PROMPT 8: Full Run
```
Run on full dataset:
python stage2_atomise_llm.py --limit 100

Review sample output atoms. Adjust extraction prompt if needed.
Then remove limit for full processing.
```

---

## Quick Reference: Switch to Atomiser Mode
In Kilo Code, select the "🧬 Atomiser Dev" mode from the dropdown, or type:
```
/mode atomiser-dev
```

---
title: "CMD Notes"
id: "cmd-notes"
version: 1
created: 2026-04-25
last_validated: 2026-04-25
type: document
topic_type: reference
status: imported
source_file: "cmd.txt"
signed_by: "Devon, 2026-04-25, devin-992682c244cf444f91e0a516498afbfd"
---

echo "=== Everything at user level (/Users/ewansair) including hidden ==="
ls -lahG "$HOME" 2>&1
echo ""
echo "=== Summary counts ==="
echo "Visible items:  $(ls    "$HOME" 2>/dev/null | wc -l | tr -d ' ')"
echo "All items:      $(ls -A "$HOME" 2>/dev/null | wc -l | tr -d ' ')"
echo "Hidden items:   $(ls -A "$HOME" 2>/dev/null | grep -c '^\.')"
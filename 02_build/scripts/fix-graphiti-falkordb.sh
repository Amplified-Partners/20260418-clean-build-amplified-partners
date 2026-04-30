#!/bin/bash
# FIX: Graphiti FalkorDB edge_fulltext_search O(n×m) → O(n) performance fix
# Source: https://github.com/getzep/graphiti/pull/1282
# Issue: https://github.com/getzep/graphiti/issues/1272
#
# Problem: edge_fulltext_search and edge_bfs_search use MATCH to re-scan
# all RELATES_TO edges by UUID after fulltext results come back.
# This causes O(n×m) complexity and timeouts on graphs with >5000 edges.
#
# Fix: Use startNode(e) and endNode(e) instead of re-MATCH.
# This reduces complexity to O(n) — milliseconds instead of 120+ seconds.
#
# Usage: SSH into Beast, then run:
#   bash fix-graphiti-falkordb.sh
#
# The script finds the installed graphiti_core package, patches search_ops.py,
# and verifies the fix was applied.

set -euo pipefail

echo "=== Graphiti FalkorDB Performance Fix (PR #1282) ==="
echo ""

# Find the graphiti_core installation
SEARCH_OPS=""
for candidate in \
    /opt/backups/agent-stack/graphiti-ingestion/venv/lib/python*/site-packages/graphiti_core/driver/falkordb/operations/search_ops.py \
    /usr/local/lib/python*/dist-packages/graphiti_core/driver/falkordb/operations/search_ops.py \
    /usr/lib/python*/site-packages/graphiti_core/driver/falkordb/operations/search_ops.py \
    $(pip show graphiti-core 2>/dev/null | grep Location | awk '{print $2}')/graphiti_core/driver/falkordb/operations/search_ops.py \
    $(find / -path "*/graphiti_core/driver/falkordb/operations/search_ops.py" -type f 2>/dev/null | head -1); do
    if [ -f "$candidate" 2>/dev/null ]; then
        SEARCH_OPS="$candidate"
        break
    fi
done

if [ -z "$SEARCH_OPS" ]; then
    echo "ERROR: Could not find graphiti_core/driver/falkordb/operations/search_ops.py"
    echo "Searching entire filesystem..."
    SEARCH_OPS=$(find / -path "*/graphiti_core/driver/falkordb/operations/search_ops.py" -type f 2>/dev/null | head -1)
    if [ -z "$SEARCH_OPS" ]; then
        echo "FATAL: graphiti_core not installed. Install it first."
        exit 1
    fi
fi

echo "Found: $SEARCH_OPS"
echo ""

# Backup
BACKUP="${SEARCH_OPS}.backup-$(date +%Y%m%d-%H%M%S)"
cp "$SEARCH_OPS" "$BACKUP"
echo "Backup: $BACKUP"

# Check if already patched
if grep -q "startNode(e) AS n, endNode(e) AS m" "$SEARCH_OPS"; then
    echo ""
    echo "ALREADY PATCHED — startNode/endNode pattern found. No changes needed."
    rm "$BACKUP"
    exit 0
fi

# Fix 1: edge_fulltext_search — replace YIELD rel + MATCH with YIELD e + startNode/endNode
# Original:
#   YIELD relationship AS rel, score
#   MATCH (n:Entity)-[e:RELATES_TO {uuid: rel.uuid}]->(m:Entity)
# Fixed:
#   YIELD relationship AS e, score
#   WITH e, score, startNode(e) AS n, endNode(e) AS m

echo ""
echo "Applying Fix 1: edge_fulltext_search..."
sed -i 's/YIELD relationship AS rel, score/YIELD relationship AS e, score/g' "$SEARCH_OPS"
sed -i 's/MATCH (n:Entity)-\[e:RELATES_TO {uuid: rel\.uuid}\]->(m:Entity)/WITH e, score, startNode(e) AS n, endNode(e) AS m/g' "$SEARCH_OPS"

# Fix 2: edge_bfs_search — replace UNWIND rel + MATCH with UNWIND e + startNode/endNode
# Original:
#   UNWIND relationships(path) AS rel
#   MATCH (n:Entity)-[e:RELATES_TO {uuid: rel.uuid}]-(m:Entity)
# Fixed:
#   UNWIND relationships(path) AS e
#   WITH e, startNode(e) AS n, endNode(e) AS m

echo "Applying Fix 2: edge_bfs_search..."
sed -i 's/UNWIND relationships(path) AS rel/UNWIND relationships(path) AS e/g' "$SEARCH_OPS"
sed -i 's/MATCH (n:Entity)-\[e:RELATES_TO {uuid: rel\.uuid}\]-(m:Entity)/WITH e, startNode(e) AS n, endNode(e) AS m/g' "$SEARCH_OPS"

# Verify
echo ""
echo "=== Verification ==="
if grep -q "startNode(e) AS n, endNode(e) AS m" "$SEARCH_OPS"; then
    echo "✅ Fix applied successfully"
    MATCHES=$(grep -c "startNode(e)" "$SEARCH_OPS")
    echo "   Found $MATCHES occurrences of startNode(e)"
else
    echo "❌ Fix may not have applied correctly"
    echo "   Check $SEARCH_OPS manually"
    echo "   Backup at: $BACKUP"
    exit 1
fi

# Check for any remaining rel.uuid references (shouldn't exist after fix)
if grep -q "rel\.uuid" "$SEARCH_OPS"; then
    REMAINING=$(grep -c "rel\.uuid" "$SEARCH_OPS")
    echo "⚠️  Warning: $REMAINING remaining rel.uuid references — may need manual review"
else
    echo "✅ No remaining rel.uuid references"
fi

echo ""
echo "=== Done ==="
echo "Restart the ingestion script to use the patched code."
echo "Backup saved at: $BACKUP"

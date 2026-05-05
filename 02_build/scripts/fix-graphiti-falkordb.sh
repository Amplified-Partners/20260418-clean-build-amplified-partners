#!/bin/bash
# FIX: Graphiti FalkorDB edge_fulltext_search O(n×m) → O(n) performance fix
#
# Source: https://github.com/getzep/graphiti/issues/1272 (cm2d, opened 2026-02-25)
# Related (incomplete) PR: https://github.com/getzep/graphiti/pull/1282 (giulio-leone, 2026-02-28)
#
# IMPORTANT — what changed in this version (Devon-b098 2026-05-05):
#
# The previous version of this script (and PR #1282 upstream) only patched
# `graphiti_core/driver/falkordb/operations/search_ops.py`. That file holds the
# `FalkorSearchOperations` class — but the class is **only invoked when
# `driver.search_interface` is set**, which it ISN'T by default for the
# FalkorDriver. The actual hot path is in
# `graphiti_core/search/search_utils.py:200`, where `match_query` is built
# inline using the buggy re-MATCH pattern for ALL non-Kuzu providers.
#
# Discovered by Devon-b098 while investigating Kimmy's enrichment pipe stalling
# at 33% failure rate / 8-day ETA on 16,403 vault files. Direct benchmark on
# the live business_knowledge graph (~3,500 entities, ~2,500 RELATES_TO edges):
#   OLD pattern: 15,694 ms internal Cypher time, hits FalkorDB 30s TIMEOUT
#   NEW pattern:      0.66 ms internal Cypher time
#   → ~24,000× speedup. End-to-end queries: 15.78s → 0.089s (177× wall-time).
#
# This script now patches BOTH files and clears the .pyc bytecode cache so
# Python actually re-compiles the patched modules on next import. (The previous
# version missed the cache step; even if the .py was patched, Python loaded
# stale bytecode and the bug stayed live.)
#
# Problem (recap from issue #1272): edge_fulltext_search re-MATCHes RELATES_TO
# edges by UUID after the fulltext index already returns the relationship
# object. FalkorDB cannot use an index for this join pattern, so it does a full
# graph scan: O(n×m). The fix uses the relationship object directly via
# startNode(e) / endNode(e): O(n).
#
# Usage (on Beast):
#   bash fix-graphiti-falkordb.sh
#   # OR via Docker build:
#   docker build -f Dockerfile.graphiti.amp1272 -t vault-graphiti:amp-1272 .
#
# Devon-b098 | 2026-05-05 | session devin-b0988ede3c7644dd880d8efb6a1fe932

set -euo pipefail

echo "=== Graphiti FalkorDB Performance Fix (issue #1272) ==="
echo "    extends PR #1282 — also patches search_utils.py default match_query"
echo ""

# Find the graphiti_core installation root
GC_ROOT=""
for candidate in \
    /opt/backups/agent-stack/graphiti-ingestion/venv/lib/python*/site-packages/graphiti_core \
    /usr/local/lib/python*/dist-packages/graphiti_core \
    /usr/local/lib/python*/site-packages/graphiti_core \
    /usr/lib/python*/site-packages/graphiti_core \
    $(pip show graphiti-core 2>/dev/null | grep Location | awk '{print $2}')/graphiti_core; do
    if [ -d "$candidate" ] 2>/dev/null; then
        GC_ROOT="$candidate"
        break
    fi
done

if [ -z "$GC_ROOT" ]; then
    echo "Searching entire filesystem for graphiti_core..."
    GC_ROOT=$(find / -path "*/graphiti_core/__init__.py" -type f 2>/dev/null | head -1 | xargs dirname || true)
fi

if [ -z "$GC_ROOT" ] || [ ! -d "$GC_ROOT" ]; then
    echo "FATAL: graphiti_core not installed."
    exit 1
fi

echo "Found graphiti_core: $GC_ROOT"

SEARCH_OPS="$GC_ROOT/driver/falkordb/operations/search_ops.py"
SEARCH_UTILS="$GC_ROOT/search/search_utils.py"

for f in "$SEARCH_OPS" "$SEARCH_UTILS"; do
    if [ ! -f "$f" ]; then
        echo "FATAL: missing $f — graphiti-core layout has changed; review patch script."
        exit 1
    fi
done

# Backup both files
TS=$(date +%Y%m%d-%H%M%S)
cp "$SEARCH_OPS" "${SEARCH_OPS}.backup-${TS}"
cp "$SEARCH_UTILS" "${SEARCH_UTILS}.backup-${TS}"
echo "Backups: ${SEARCH_OPS}.backup-${TS}, ${SEARCH_UTILS}.backup-${TS}"

# Idempotency check — both files must contain the new pattern
PATCHED_OPS=$(grep -c "startNode(e) AS n, endNode(e) AS m" "$SEARCH_OPS" || true)
PATCHED_UTILS=$(grep -c "startNode(e) AS n, endNode(e) AS m" "$SEARCH_UTILS" || true)
if [ "$PATCHED_OPS" -gt 0 ] && [ "$PATCHED_UTILS" -gt 0 ]; then
    echo "ALREADY PATCHED — both files contain startNode/endNode pattern."
    rm "${SEARCH_OPS}.backup-${TS}" "${SEARCH_UTILS}.backup-${TS}"
    exit 0
fi

# Apply patches via Python (multi-line replacements, safer than sed for these)
python3 - "$SEARCH_OPS" "$SEARCH_UTILS" <<'PYEOF'
import sys

# Patch 1: graphiti_core/driver/falkordb/operations/search_ops.py
search_ops_path = sys.argv[1]
src = open(search_ops_path).read()
old = """            YIELD relationship AS rel, score
            MATCH (n:Entity)-[e:RELATES_TO {uuid: rel.uuid}]->(m:Entity)
            """
new = """            YIELD relationship AS e, score
            WITH e, score, startNode(e) AS n, endNode(e) AS m
            """
if old in src:
    src = src.replace(old, new, 1)
    open(search_ops_path, "w").write(src)
    print(f"PATCHED: {search_ops_path}")
elif new in src:
    print(f"already patched: {search_ops_path}")
else:
    print(f"WARNING: pattern not found in {search_ops_path} — graphiti-core layout may have changed", file=sys.stderr)

# Patch 2: graphiti_core/search/search_utils.py — the default match_query
search_utils_path = sys.argv[2]
src = open(search_utils_path).read()
old = """    match_query = \"\"\"
    YIELD relationship AS rel, score
    MATCH (n:Entity)-[e:RELATES_TO {uuid: rel.uuid}]->(m:Entity)
    \"\"\""""
new = """    match_query = \"\"\"
    YIELD relationship AS e, score
    WITH e, score, startNode(e) AS n, endNode(e) AS m
    \"\"\""""
if old in src:
    src = src.replace(old, new, 1)
    open(search_utils_path, "w").write(src)
    print(f"PATCHED: {search_utils_path}")
elif new in src:
    print(f"already patched: {search_utils_path}")
else:
    print(f"WARNING: pattern not found in {search_utils_path} — graphiti-core layout may have changed", file=sys.stderr)
PYEOF

# Clear stale .pyc bytecode cache so Python re-compiles on next import.
# Without this step the patched .py files are loaded but Python can short-circuit
# to the old .pyc, leaving the bug live.
PYC_CLEARED=$(find "$GC_ROOT" -name "*.pyc" -delete -print 2>/dev/null | wc -l)
echo "Cleared $PYC_CLEARED .pyc files"

echo ""
echo "=== Verification ==="
OPS_OK=$(grep -c "startNode(e) AS n, endNode(e) AS m" "$SEARCH_OPS" || true)
UTILS_OK=$(grep -c "startNode(e) AS n, endNode(e) AS m" "$SEARCH_UTILS" || true)
if [ "$OPS_OK" -gt 0 ] && [ "$UTILS_OK" -gt 0 ]; then
    echo "Fix verified — startNode/endNode pattern present in both files."
else
    echo "Fix verification FAILED:"
    echo "  $SEARCH_OPS occurrences of new pattern: $OPS_OK"
    echo "  $SEARCH_UTILS occurrences of new pattern: $UTILS_OK"
    exit 1
fi

# Check for any remaining buggy pattern
REMAINING_OPS=$(grep -c "RELATES_TO {uuid: rel.uuid}" "$SEARCH_OPS" || true)
REMAINING_UTILS=$(grep -c "RELATES_TO {uuid: rel.uuid}" "$SEARCH_UTILS" || true)
if [ "$REMAINING_OPS" -gt 0 ] || [ "$REMAINING_UTILS" -gt 0 ]; then
    echo "Note: $REMAINING_OPS / $REMAINING_UTILS remaining occurrences in edge_bfs_search (unfixed by design — semantics change is non-trivial)."
fi

echo ""
echo "=== Done ==="
echo "Restart the Graphiti container to load the patched modules."
echo "Backups: ${SEARCH_OPS}.backup-${TS}"
echo "         ${SEARCH_UTILS}.backup-${TS}"

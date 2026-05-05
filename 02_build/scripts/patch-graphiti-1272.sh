#!/bin/sh
# Build-time patch for getzep/graphiti issue #1272 — edge_fulltext_search re-MATCH bug.
#
# Slim variant of fix-graphiti-falkordb.sh — assumes a known graphiti-core install
# location (Docker image with python3.12 site-packages). For ad-hoc patching of
# arbitrary installs, use fix-graphiti-falkordb.sh instead.
#
# Patches both:
#   - graphiti_core/driver/falkordb/operations/search_ops.py
#   - graphiti_core/search/search_utils.py  (the actual hot path; missed by upstream PR #1282)
# and clears the .pyc cache so Python re-compiles on import.
#
# Sources / attribution:
#   - Issue: https://github.com/getzep/graphiti/issues/1272 (cm2d, 2026-02-25)
#   - PR:    https://github.com/getzep/graphiti/pull/1282 (giulio-leone, 2026-02-28, incomplete fix)
#
# Devon-b098 | 2026-05-05 | session devin-b0988ede3c7644dd880d8efb6a1fe932

set -e
SP=/usr/local/lib/python3.12/site-packages

python3 - <<PYEOF
import sys
edits = [
    {
        "path": "$SP/graphiti_core/driver/falkordb/operations/search_ops.py",
        "old": """            YIELD relationship AS rel, score
            MATCH (n:Entity)-[e:RELATES_TO {uuid: rel.uuid}]->(m:Entity)
            """,
        "new": """            YIELD relationship AS e, score
            WITH e, score, startNode(e) AS n, endNode(e) AS m
            """,
    },
    {
        "path": "$SP/graphiti_core/search/search_utils.py",
        "old": """    match_query = \"\"\"
    YIELD relationship AS rel, score
    MATCH (n:Entity)-[e:RELATES_TO {uuid: rel.uuid}]->(m:Entity)
    \"\"\"""",
        "new": """    match_query = \"\"\"
    YIELD relationship AS e, score
    WITH e, score, startNode(e) AS n, endNode(e) AS m
    \"\"\"""",
    },
]
for e in edits:
    src = open(e["path"]).read()
    if e["old"] not in src:
        print("PATCH FAILED: target not found in", e["path"], file=sys.stderr)
        sys.exit(1)
    src = src.replace(e["old"], e["new"], 1)
    open(e["path"], "w").write(src)
    print("PATCH APPLIED:", e["path"])
PYEOF

# Clear stale .pyc bytecode so Python recompiles on import.
find "$SP/graphiti_core" -name "*.pyc" -delete
echo "PYC CACHE CLEARED for graphiti_core"

#!/usr/bin/env python3
"""
APDS Labeller Bridge -- Amplified Pudding Discovery System
Takes harvester output and assigns PUDDING labels via Ollama, then writes
:Document nodes (with source='APDS') to FalkorDB graph 'business_knowledge'.

Status: this is the script that actually ran on Beast on 2026-05-05 and
produced the 250 :Document nodes currently in 'business_knowledge'. It is
**not** the canonical clean-build labeller (`02_build/scripts/pudding_labeler.py`),
which uses a different vocabulary. See `02_build/apds/README.md` for the
schema-divergence note. Linear: AMP-104.

Originally hand-deployed to /opt/amplified/apds/label/apds_labeller.py by Kimmy.
Promoted to version control with two minimal hardening edits over the Beast
version, both flagged by Devin Review on PR #52:
  1. The five PUDDING label values from Ollama are now escape_cypher()'d before
     being interpolated into the GRAPH.QUERY string (was: raw interpolation -- a
     malformed LLM response containing a single quote would have produced a
     Cypher syntax error or, worst case, an injection). The 250 production docs
     were unaffected because every successful Ollama response in the run had
     values from the fixed PUDDING vocabulary.
  2. `confidence` is cast to float() to reject non-numeric LLM output cleanly.

The Beast copy at /opt/amplified/apds/label/apds_labeller.py is now one revision
behind this file. Sync is tracked as a follow-on action; the next session that
re-runs the labeller on Beast must `scp` this hardened copy first.

Behaviour on the happy path (LLM returns clean values from the fixed PUDDING
vocab) is identical to the version that produced the 250 production docs.

Authored-by: Kimmy (hand-deployed to Beast 2026-05-05)
Promoted-by: Devon-9f21 | 2026-05-05 | devin-9f2104fb06624b009f2879c50957c647
Hardened-by: Devon-9f21 | 2026-05-05 | per Devin Review on PR #52
"""

import json
import os
import sys
from pathlib import Path

import redis

FALKORDB_HOST = os.getenv("FALKORDB_HOST", "172.18.0.22")
FALKORDB_PORT = int(os.getenv("FALKORDB_PORT", "6379"))
GRAPH_NAME = "business_knowledge"
OLLAMA_URL = os.getenv("OLLAMA_URL", "http://172.18.0.12:11434")
HARVEST_FILE = "/opt/amplified/apds/harvest/harvest_20260505_033410.json"

PUDDING_PROMPT = """You are a PUDDING taxonomy labeller. Assign exactly one label per dimension.

Dimensions:
- WHAT: FIN | OPS | MKT | TECH | PPL | GOV | EXT
- HOW: METRIC | PROCESS | ASSET | RISK | OPPORTUNITY | RELATIONSHIP | KNOWLEDGE
- SCALE: NANO | MICRO | MESO | MACRO | MEGA | META | TEMPORAL
- TIME: NOW | NEAR | MID | FAR | EVERGREEN | CYCLICAL | LEGACY
- PATTERN: LOG-CAU | LOG-ANA | LOG-SYN | SYS-FB | SYS-EM | SYS-HM | SYS-BM | HUM-TRUST | HUM-INCENT | HUM-COG | HUM-CULT | VAL-EFF | VAL-ACC | VAL-ROB | VAL-ADAPT | VAL-ETH

Output ONLY valid JSON:
{"WHAT": "...", "HOW": "...", "SCALE": "...", "TIME": "...", "PATTERN": "...", "confidence": 0.0-1.0}

Text to label:
"""


def get_ollama_label(text, model="llama3.1:8b"):
    import urllib.request
    payload = json.dumps({
        "model": model,
        "prompt": PUDDING_PROMPT + text[:2000],
        "stream": False,
        "format": "json",
        "options": {"temperature": 0.1, "num_predict": 150}
    }).encode()

    req = urllib.request.Request(
        f"{OLLAMA_URL}/api/generate",
        data=payload,
        headers={"Content-Type": "application/json"},
        method="POST"
    )

    try:
        with urllib.request.urlopen(req, timeout=60) as resp:
            data = json.loads(resp.read())
            result = json.loads(data.get("response", "{}"))
            required = {"WHAT", "HOW", "SCALE", "TIME", "PATTERN"}
            if required.issubset(result.keys()):
                return result
            else:
                return {k: "UNKNOWN" for k in required} | {"confidence": 0.0}
    except Exception as e:
        print(f"  Ollama error: {e}")
        return {"WHAT": "UNKNOWN", "HOW": "UNKNOWN", "SCALE": "UNKNOWN",
                "TIME": "UNKNOWN", "PATTERN": "UNKNOWN", "confidence": 0.0}


def escape_cypher(s):
    return s.replace("\\", "\\\\").replace("'", "\\'")


def store_in_falkor(r, doc_id, title, url, labels, source="APDS"):
    try:
        title_esc = escape_cypher(title[:200])
        url_esc = escape_cypher(url[:500])
        query = (
            f"MERGE (d:Document {{id: '{doc_id}'}}) "
            f"SET d.title = '{title_esc}', "
            f"d.url = '{url_esc}', "
            f"d.source = '{source}', "
            f"d.WHAT = '{escape_cypher(str(labels.get('WHAT', 'UNKNOWN')))}', "
            f"d.HOW = '{escape_cypher(str(labels.get('HOW', 'UNKNOWN')))}', "
            f"d.SCALE = '{escape_cypher(str(labels.get('SCALE', 'UNKNOWN')))}', "
            f"d.TIME = '{escape_cypher(str(labels.get('TIME', 'UNKNOWN')))}', "
            f"d.PATTERN = '{escape_cypher(str(labels.get('PATTERN', 'UNKNOWN')))}', "
            f"d.confidence = {float(labels.get('confidence', 0.0))} "
            f"RETURN d"
        )
        r.execute_command("GRAPH.QUERY", GRAPH_NAME, query)
        return True
    except Exception as e:
        print(f"  FalkorDB error: {e}")
        return False


def main():
    print("=" * 60)
    print("APDS Labeller Bridge -- PUDDING Taxonomy Assignment")
    print("=" * 60)

    r = redis.Redis(host=FALKORDB_HOST, port=FALKORDB_PORT, decode_responses=True)
    if not r.ping():
        print("ERROR: Cannot connect to FalkorDB")
        sys.exit(1)
    print(f"Connected to FalkorDB graph '{GRAPH_NAME}'")

    harvest_path = Path(HARVEST_FILE)
    if not harvest_path.exists():
        print(f"ERROR: Harvest file not found: {HARVEST_FILE}")
        sys.exit(1)

    with open(harvest_path) as f:
        harvest = json.load(f)

    print(f"Loaded {len(harvest)} queries from harvest file")

    all_results = []
    for query_block in harvest:
        for result in query_block.get("results", []):
            all_results.append({
                "title": result.get("title", "Untitled"),
                "url": result.get("url", ""),
                "content": result.get("content", ""),
                "query": query_block.get("query", ""),
                "engine": query_block.get("engine", ""),
            })

    print(f"Total results to label: {len(all_results)}")
    print(f"Using Ollama model: llama3.1:8b (FREE)")
    print("-" * 60)

    successful = 0
    failed = 0

    for i, result in enumerate(all_results, 1):
        doc_id = f"apds_{i:04d}"
        title = result["title"]
        url = result["url"]
        content = result["content"]

        print(f"[{i}/{len(all_results)}] {title[:55]}...")

        check = r.execute_command("GRAPH.QUERY", GRAPH_NAME,
            f"MATCH (d:Document {{id: '{doc_id}'}}) RETURN count(d)")
        if check and len(check) > 1 and check[1][0] == 1:
            print(f"  Already labelled, skipping")
            continue

        labels = get_ollama_label(content)
        print(f"  Labels: {labels}")

        if store_in_falkor(r, doc_id, title, url, labels):
            successful += 1
        else:
            failed += 1

    print("-" * 60)
    print(f"Done. Successful: {successful}, Failed: {failed}")

    stats = r.execute_command("GRAPH.QUERY", GRAPH_NAME,
        "MATCH (d:Document {source: 'APDS'}) RETURN count(d)")
    if stats and len(stats) > 1:
        print(f"Total APDS documents in graph: {stats[1][0]}")


if __name__ == "__main__":
    main()

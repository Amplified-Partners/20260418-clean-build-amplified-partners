#!/usr/bin/env python3
"""
APDS Labeller v3.0 -- AMP-173 async Haiku extraction.

Replaces the sequential Ollama-based extraction (v2.2) with concurrent calls to
Claude Haiku via the Anthropic Messages API.  FalkorDB write path is unchanged
(UNWIND-batched MERGE from AMP-128).

Key changes from v2.2:
- Extraction: synchronous urllib/Ollama → async httpx/Anthropic Messages API
- Concurrency: sequential one-at-a-time → asyncio.gather() with Semaphore(N)
- Model: llama3.1:8b (local) → claude-haiku-4-5-20251001 (API)
- Retry: exponential backoff on 429/5xx with Retry-After header support
- Safety: --max-docs and running cost accumulator

Expected speedup: 10x-50x end-to-end (Haiku ~200-500ms vs Ollama ~1-3s, ×N concurrent).

Invocation:
    python3 apds_labeller_v3_amp173.py --run-id 20260505_094320
    python3 apds_labeller_v3_amp173.py --run-id 20260505_094320 --concurrency 40
    python3 apds_labeller_v3_amp173.py --run-id 20260505_094320 --fallback-ollama

Signed-by: Devon-bc14 | 2026-05-07 | session devin-bc1458eb952244e8b1efc3ec15c7959c
"""

import argparse
import asyncio
import glob
import json
import os
import sys
import time
import urllib.request
from datetime import datetime, timezone
from pathlib import Path

import httpx
import redis

# --- Configuration -----------------------------------------------------------

FALKORDB_HOST = os.getenv("FALKORDB_HOST", "172.18.0.22")
FALKORDB_PORT = int(os.getenv("FALKORDB_PORT", "6379"))
GRAPH_NAME = "business_knowledge"
OLLAMA_URL = os.getenv("OLLAMA_URL", "http://172.18.0.12:11434")
ANTHROPIC_API_KEY = os.getenv("ANTHROPIC_API_KEY", "")
ANTHROPIC_URL = "https://api.anthropic.com/v1/messages"
DEFAULT_MODEL = "claude-haiku-4-5-20251001"
LOG_DIR = Path(os.getenv("LOG_DIR", "/opt/amplified/apds/logs"))
BATCH_SIZE = int(os.getenv("APDS_BATCH_SIZE", "50"))
DEFAULT_CONCURRENCY = int(os.getenv("APDS_CONCURRENCY", "20"))

# Approximate token costs for Haiku 4.5 (USD per million tokens)
COST_INPUT_PER_MTOK = 1.0
COST_OUTPUT_PER_MTOK = 5.0

PUDDING_SYSTEM_PROMPT = """You are a PUDDING taxonomy labeller. Assign exactly one label per dimension.

Dimensions:
- WHAT: FIN | OPS | MKT | TECH | PPL | GOV | EXT
- HOW: METRIC | PROCESS | ASSET | RISK | OPPORTUNITY | RELATIONSHIP | KNOWLEDGE
- SCALE: NANO | MICRO | MESO | MACRO | MEGA | META | TEMPORAL
- TIME: NOW | NEAR | MID | FAR | EVERGREEN | CYCLICAL | LEGACY
- PATTERN: LOG-CAU | LOG-ANA | LOG-SYN | SYS-FB | SYS-EM | SYS-HM | SYS-BM | HUM-TRUST | HUM-INCENT | HUM-COG | HUM-CULT | VAL-EFF | VAL-ACC | VAL-ROB | VAL-ADAPT | VAL-ETH

Output ONLY valid JSON:
{"WHAT": "...", "HOW": "...", "SCALE": "...", "TIME": "...", "PATTERN": "...", "confidence": 0.0-1.0}"""

# Legacy prompt for Ollama fallback (single-string format)
PUDDING_PROMPT_LEGACY = """You are a PUDDING taxonomy labeller. Assign exactly one label per dimension.

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

REQUIRED_DIMS = {"WHAT", "HOW", "SCALE", "TIME", "PATTERN"}
UNKNOWN_LABELS = {k: "UNKNOWN" for k in REQUIRED_DIMS} | {"confidence": 0.0}


# --- Async Haiku extraction --------------------------------------------------

async def get_haiku_label(
    text: str,
    client: httpx.AsyncClient,
    semaphore: asyncio.Semaphore,
    model: str = DEFAULT_MODEL,
    max_retries: int = 5,
) -> dict:
    """Extract PUDDING labels from text using Claude Haiku via Anthropic Messages API.

    Uses a semaphore to limit concurrency and implements exponential backoff
    on rate-limit (429) and server error (5xx) responses.
    """
    truncated = (text or "")[:2000]
    if not truncated.strip():
        return UNKNOWN_LABELS | {"_error": "empty_text"}

    payload = {
        "model": model,
        "max_tokens": 150,
        "system": PUDDING_SYSTEM_PROMPT,
        "messages": [{"role": "user", "content": f"Text to label:\n{truncated}"}],
        "temperature": 0.1,
    }

    async with semaphore:
        for attempt in range(1, max_retries + 1):
            try:
                response = await client.post(
                    ANTHROPIC_URL,
                    headers={
                        "x-api-key": ANTHROPIC_API_KEY,
                        "anthropic-version": "2023-06-01",
                        "content-type": "application/json",
                    },
                    json=payload,
                    timeout=30.0,
                )

                if response.status_code == 200:
                    data = response.json()
                    text_out = data["content"][0]["text"]
                    # Parse JSON from response (handle potential markdown wrapping)
                    text_out = text_out.strip()
                    if text_out.startswith("```"):
                        text_out = text_out.split("\n", 1)[-1].rsplit("```", 1)[0]
                    result = json.loads(text_out)
                    if REQUIRED_DIMS.issubset(result.keys()):
                        # Attach usage for cost tracking
                        usage = data.get("usage", {})
                        result["_input_tokens"] = usage.get("input_tokens", 0)
                        result["_output_tokens"] = usage.get("output_tokens", 0)
                        return result
                    return UNKNOWN_LABELS | {"confidence": 0.0, "_error": "missing_dims"}

                if response.status_code == 429:
                    retry_after = float(response.headers.get("retry-after", attempt * 2))
                    await asyncio.sleep(retry_after)
                    continue

                if response.status_code >= 500:
                    await asyncio.sleep(attempt * 2)
                    continue

                # 4xx other than 429 — don't retry
                return UNKNOWN_LABELS | {
                    "_error": f"http_{response.status_code}:{response.text[:100]}"
                }

            except (httpx.TimeoutException, httpx.ConnectError) as e:
                if attempt < max_retries:
                    await asyncio.sleep(attempt * 2)
                    continue
                return UNKNOWN_LABELS | {"_error": f"timeout:{str(e)[:80]}"}
            except json.JSONDecodeError as e:
                return UNKNOWN_LABELS | {"_error": f"json_parse:{str(e)[:80]}"}
            except Exception as e:
                return UNKNOWN_LABELS | {"_error": f"unexpected:{str(e)[:80]}"}

    return UNKNOWN_LABELS | {"_error": "max_retries_exhausted"}


# --- Ollama fallback (synchronous, from v2.2) ---------------------------------

def get_ollama_label(text: str, model: str = "llama3.1:8b") -> dict:
    """Synchronous fallback to local Ollama for degraded-mode operation."""
    payload = json.dumps({
        "model": model,
        "prompt": PUDDING_PROMPT_LEGACY + (text or "")[:2000],
        "stream": False,
        "format": "json",
        "options": {"temperature": 0.1, "num_predict": 150},
    }).encode()
    req = urllib.request.Request(
        f"{OLLAMA_URL}/api/generate",
        data=payload,
        headers={"Content-Type": "application/json"},
        method="POST",
    )
    try:
        with urllib.request.urlopen(req, timeout=60) as resp:
            data = json.loads(resp.read())
            result = json.loads(data.get("response", "{}"))
            if REQUIRED_DIMS.issubset(result.keys()):
                return result
            return UNKNOWN_LABELS.copy()
    except Exception as e:
        return UNKNOWN_LABELS | {"_error": str(e)[:120]}


# --- Batch async extraction ---------------------------------------------------

async def extract_batch_async(
    docs: list[tuple[int, str, dict]],
    concurrency: int,
    model: str,
    log_fn,
) -> list[tuple[int, str, dict, dict]]:
    """Extract PUDDING labels for a batch of docs concurrently.

    Args:
        docs: list of (index, doc_id, record) tuples
        concurrency: max parallel requests
        model: Anthropic model identifier
        log_fn: logging function

    Returns:
        list of (index, doc_id, record, labels) tuples
    """
    semaphore = asyncio.Semaphore(concurrency)
    results: list[tuple[int, str, dict, dict]] = []

    async with httpx.AsyncClient() as client:
        async def extract_one(idx: int, doc_id: str, rec: dict) -> tuple[int, str, dict, dict]:
            labels = await get_haiku_label(rec["content"], client, semaphore, model=model)
            return (idx, doc_id, rec, labels)

        tasks = [extract_one(idx, doc_id, rec) for (idx, doc_id, rec) in docs]
        results = await asyncio.gather(*tasks)

    return list(results)


# --- FalkorDB write infrastructure (unchanged from v2.2) ----------------------

def escape_cypher(s: str) -> str:
    return (s or "").replace("\\", "\\\\").replace("'", "\\'").replace("\n", " ").replace("\r", " ")


def cypher_string(s: str | None) -> str:
    return "'" + escape_cypher(s or "") + "'"


def cypher_value(v) -> str:
    if v is None:
        return "null"
    if isinstance(v, bool):
        return "true" if v else "false"
    if isinstance(v, (int, float)):
        return repr(v)
    if isinstance(v, str):
        return cypher_string(v)
    raise TypeError(f"Unsupported type for Cypher literal: {type(v).__name__}")


def cypher_map(d: dict) -> str:
    parts = [f"{k}: {cypher_value(v)}" for k, v in d.items()]
    return "{" + ", ".join(parts) + "}"


def cypher_list_of_maps(items: list[dict]) -> str:
    return "[" + ", ".join(cypher_map(d) for d in items) + "]"


def doc_exists(r, doc_id: str) -> bool:
    res = r.execute_command(
        "GRAPH.QUERY", GRAPH_NAME,
        f"MATCH (d:Document {{id: {cypher_string(doc_id)}}}) RETURN count(d)"
    )
    if not res or len(res) < 2 or not res[1]:
        return False
    row = res[1][0]
    if isinstance(row, list) and row:
        return int(row[0]) >= 1
    return False


def docs_present(r, doc_ids: list[str]) -> set[str]:
    if not doc_ids:
        return set()
    ids_literal = "[" + ", ".join(cypher_string(i) for i in doc_ids) + "]"
    cypher = (
        f"MATCH (d:Document) WHERE d.id IN {ids_literal} "
        "RETURN d.id"
    )
    res = r.execute_command("GRAPH.QUERY", GRAPH_NAME, cypher)
    found: set[str] = set()
    if res and len(res) >= 2 and res[1]:
        for row in res[1]:
            if isinstance(row, list) and row:
                found.add(row[0])
    return found


def _doc_props(doc_id: str, rec: dict, labels: dict, query: str, engine: str,
               harvest_run_id: str, source: str, labelled_at: str) -> dict:
    return {
        "id": doc_id,
        "title": (rec.get("title") or "")[:200],
        "url": (rec.get("url") or "")[:500],
        "source": source,
        "WHAT": labels.get("WHAT", "UNKNOWN"),
        "HOW": labels.get("HOW", "UNKNOWN"),
        "SCALE": labels.get("SCALE", "UNKNOWN"),
        "TIME": labels.get("TIME", "UNKNOWN"),
        "PATTERN": labels.get("PATTERN", "UNKNOWN"),
        "confidence": float(labels.get("confidence", 0.0)),
        "query": (query or "")[:200],
        "engine": (engine or "")[:50],
        "harvest_run_id": (harvest_run_id or "")[:50],
        "labelled_at": labelled_at,
    }


_DOC_SET_CLAUSE = (
    "SET d.title = doc.title, "
    "    d.url = doc.url, "
    "    d.source = doc.source, "
    "    d.WHAT = doc.WHAT, "
    "    d.HOW = doc.HOW, "
    "    d.SCALE = doc.SCALE, "
    "    d.TIME = doc.TIME, "
    "    d.PATTERN = doc.PATTERN, "
    "    d.confidence = doc.confidence, "
    "    d.query = doc.query, "
    "    d.engine = doc.engine, "
    "    d.harvest_run_id = doc.harvest_run_id, "
    "    d.labelled_at = doc.labelled_at"
)


def store_with_retry(r, doc_id: str, title: str, url: str, labels: dict,
                     query: str, engine: str, harvest_run_id: str,
                     source: str = "APDS",
                     max_attempts: int = 5) -> tuple[bool, int]:
    rec = {"title": title, "url": url}
    labelled_at = datetime.now(timezone.utc).isoformat()
    payload = _doc_props(doc_id, rec, labels, query, engine, harvest_run_id, source, labelled_at)
    cypher = (
        f"WITH {cypher_map(payload)} AS doc "
        "MERGE (d:Document {id: doc.id}) "
        f"{_DOC_SET_CLAUSE} "
        "RETURN d.id"
    )
    for attempt in range(1, max_attempts + 1):
        try:
            r.execute_command("GRAPH.QUERY", GRAPH_NAME, cypher)
        except Exception as e:
            print(f"    attempt {attempt}: write exception: {e}")
            time.sleep(attempt)
            continue
        try:
            if doc_exists(r, doc_id):
                return True, attempt
        except Exception as e:
            print(f"    attempt {attempt}: verify exception: {e}")
        time.sleep(attempt)
    return False, max_attempts


def store_documents_batched(
    r,
    items: list[tuple[str, dict, dict, str, str, str]],
    *,
    source: str = "APDS",
    batch_size: int = BATCH_SIZE,
    max_batch_attempts: int = 3,
) -> tuple[int, int, int]:
    """UNWIND-batched MERGE with batch verify + per-doc fallback."""
    ok = 0
    failed = 0
    total_attempts = 0

    for start in range(0, len(items), batch_size):
        chunk = items[start : start + batch_size]
        chunk_ids = [t[0] for t in chunk]
        labelled_at = datetime.now(timezone.utc).isoformat()
        payload = [
            _doc_props(doc_id, rec, labels, query, engine, harvest_run_id, source, labelled_at)
            for (doc_id, rec, labels, query, engine, harvest_run_id) in chunk
        ]
        cypher = (
            f"UNWIND {cypher_list_of_maps(payload)} AS doc "
            "MERGE (d:Document {id: doc.id}) "
            f"{_DOC_SET_CLAUSE} "
            "RETURN count(d)"
        )

        landed = False
        missing: list[str] = []
        for attempt in range(1, max_batch_attempts + 1):
            total_attempts += 1
            try:
                r.execute_command("GRAPH.QUERY", GRAPH_NAME, cypher)
            except Exception as e:
                print(f"  batch attempt {attempt}: write exception: {e}")
                time.sleep(attempt)
                continue
            try:
                present = docs_present(r, chunk_ids)
            except Exception as e:
                print(f"  batch attempt {attempt}: verify exception: {e}")
                time.sleep(attempt)
                continue
            missing = [i for i in chunk_ids if i not in present]
            if not missing:
                ok += len(chunk)
                landed = True
                break
            print(f"  batch attempt {attempt}: {len(missing)}/{len(chunk)} missing post-MERGE")
            time.sleep(attempt)

        if landed:
            continue

        fallback_targets = missing or chunk_ids
        fallback_set = set(fallback_targets)
        chunk_by_id = {t[0]: t for t in chunk}
        for doc_id in fallback_targets:
            if doc_id not in chunk_by_id:
                continue
            _, rec, labels, query, engine, harvest_run_id = chunk_by_id[doc_id]
            doc_ok, attempts = store_with_retry(
                r, doc_id, rec.get("title", ""), rec.get("url", ""), labels,
                query=query, engine=engine, harvest_run_id=harvest_run_id, source=source,
            )
            total_attempts += attempts
            if doc_ok:
                ok += 1
            else:
                failed += 1
        ok += sum(1 for t in chunk if t[0] not in fallback_set)

    return ok, failed, total_attempts


class BatchedFlusher:
    """Buffer items and flush in UNWIND-batched MERGE chunks."""

    def __init__(self, r, batch_size: int = BATCH_SIZE, on_flush=None):
        self.r = r
        self.batch_size = batch_size
        self.buffer: list[tuple[str, dict, dict, str, str, str]] = []
        self.ok = 0
        self.failed = 0
        self.total_attempts = 0
        self.flushes = 0
        self._on_flush = on_flush

    def add(self, doc_id: str, rec: dict, labels: dict,
            query: str, engine: str, harvest_run_id: str) -> None:
        self.buffer.append((doc_id, rec, labels, query, engine, harvest_run_id))
        if len(self.buffer) >= self.batch_size:
            self.flush()

    def flush(self) -> None:
        if not self.buffer:
            return
        batch = self.buffer
        self.buffer = []
        ok, failed, attempts = store_documents_batched(
            self.r, batch, batch_size=self.batch_size
        )
        self.ok += ok
        self.failed += failed
        self.total_attempts += attempts
        self.flushes += 1
        if self._on_flush:
            self._on_flush(self.flushes, len(batch), ok, failed, attempts)


# --- File loading (unchanged from v2.2) ---------------------------------------

def load_deduped(input_glob: str) -> list[dict]:
    paths = [Path(p) for p in sorted(glob.glob(input_glob))]
    records = []
    for p in paths:
        with open(p) as f:
            for line in f:
                line = line.strip()
                if not line:
                    continue
                rec = json.loads(line)
                records.append({
                    "title": rec.get("title") or "Untitled",
                    "url": rec.get("url") or "",
                    "content": rec.get("content") or "",
                    "query": rec.get("query") or "",
                    "engine": rec.get("engine") or "",
                    "run_id": rec.get("run_id") or "jsonl",
                })
    seen = set()
    out = []
    for r in records:
        k = (r.get("url") or "").strip().lower()
        if not k or k in seen:
            continue
        seen.add(k)
        out.append(r)
    return out


# --- Main pipeline (async extraction + sync writes) ---------------------------

def main():
    p = argparse.ArgumentParser(
        description="APDS Labeller v3.0 (AMP-173 async Haiku extraction)"
    )
    p.add_argument("--run-id", required=True,
                   help="Harvest run_id to label (e.g. 20260505_094320)")
    p.add_argument("--input-glob", default="/opt/amplified/apds/logs/harvest_q*.jsonl")
    p.add_argument("--limit", type=int, default=0,
                   help="Process at most N missing records (0 = unlimited)")
    p.add_argument("--max-docs", type=int, default=0,
                   help="Safety limit: abort after N docs labelled (0 = unlimited)")
    p.add_argument("--batch-size", type=int, default=BATCH_SIZE,
                   help="UNWIND batch size for FalkorDB MERGE (default: 50)")
    p.add_argument("--concurrency", type=int, default=DEFAULT_CONCURRENCY,
                   help="Max concurrent Anthropic API requests (default: 20)")
    p.add_argument("--model", default=DEFAULT_MODEL,
                   help=f"Anthropic model to use (default: {DEFAULT_MODEL})")
    p.add_argument("--fallback-ollama", action="store_true",
                   help="Use local Ollama instead of Anthropic (degraded mode)")
    p.add_argument("--dry-run", action="store_true")
    args = p.parse_args()

    if not args.fallback_ollama and not ANTHROPIC_API_KEY:
        print("ERROR: ANTHROPIC_API_KEY not set. Use --fallback-ollama for local mode.")
        sys.exit(1)

    run_id = datetime.now(timezone.utc).strftime("%Y%m%d_%H%M%S")
    log_path = LOG_DIR / f"labeller_v3_{run_id}.log"
    LOG_DIR.mkdir(parents=True, exist_ok=True)
    with open(log_path, "a", buffering=1) as log_fh:
        _run(args, run_id, log_fh)


def _run(args, run_id, log_fh):
    def log(msg: str):
        print(msg, flush=True)
        log_fh.write(msg + "\n")

    mode = "OLLAMA-FALLBACK" if args.fallback_ollama else f"HAIKU-ASYNC(c={args.concurrency})"
    log("=" * 60)
    log(f"APDS Labeller v3.0 (AMP-173) for run_id={args.run_id}")
    log(f"execution_id={run_id} model={args.model if not args.fallback_ollama else 'llama3.1:8b'}")
    log(f"mode={mode} batch_size={args.batch_size}")
    log("=" * 60)

    deduped = load_deduped(args.input_glob)
    log(f"Loaded {len(deduped)} unique deduped records from glob {args.input_glob}")

    rc = redis.Redis(host=FALKORDB_HOST, port=FALKORDB_PORT, decode_responses=True)
    if not rc.ping():
        log("ERROR: cannot connect to FalkorDB")
        sys.exit(1)
    log(f"Connected to FalkorDB graph '{GRAPH_NAME}'")

    log("Scanning for missing indices...")
    all_ids = [f"apds_{args.run_id}_{i:04d}" for i in range(1, len(deduped) + 1)]
    present = set()
    scan_chunk = 500
    for start in range(0, len(all_ids), scan_chunk):
        present |= docs_present(rc, all_ids[start : start + scan_chunk])
    missing = [
        (i, all_ids[i - 1], deduped[i - 1])
        for i in range(1, len(deduped) + 1)
        if all_ids[i - 1] not in present
    ]
    log(f"Missing: {len(missing)} of {len(deduped)} indices")

    if args.limit and args.limit > 0:
        missing = missing[: args.limit]
        log(f"Limit applied: processing first {len(missing)} only")

    if args.max_docs and args.max_docs > 0 and len(missing) > args.max_docs:
        missing = missing[: args.max_docs]
        log(f"Safety limit applied: capping at {args.max_docs} docs")

    if args.dry_run:
        for i, doc_id, rec in missing[:20]:
            log(f"  would label idx {i:04d} | {rec['engine']:12s} | {rec['title'][:60]}")
        log(f"DRY-RUN: total = {len(missing)}")
        return

    def on_flush(n_flushes, batch_n, ok, failed, attempts):
        log(
            f"  flush #{n_flushes}: batch={batch_n} ok={ok} fail={failed} "
            f"attempts={attempts} avg={attempts / max(batch_n, 1):.2f}"
        )

    flusher = BatchedFlusher(rc, batch_size=args.batch_size, on_flush=on_flush)
    api_errors = 0
    total_input_tokens = 0
    total_output_tokens = 0

    log("-" * 60)

    if args.fallback_ollama:
        # Degraded mode: sequential Ollama (same as v2.2)
        log("Running in FALLBACK mode (sequential Ollama)")
        for n, (i, doc_id, rec) in enumerate(missing, 1):
            labels = get_ollama_label(rec["content"])
            if "_error" in labels:
                api_errors += 1
            flusher.add(
                doc_id, rec, labels,
                query=rec["query"], engine=rec["engine"], harvest_run_id=rec["run_id"],
            )
            if n % 25 == 0 or n == len(missing):
                log(
                    f"[{n}/{len(missing)}] ok={flusher.ok} fail={flusher.failed} "
                    f"pending={len(flusher.buffer)} errors={api_errors} | "
                    f"idx {i:04d} | {rec['engine']:12s} | {rec['title'][:50]}"
                )
    else:
        # Primary mode: async Haiku extraction in chunks
        log(f"Running ASYNC extraction (concurrency={args.concurrency})")
        extraction_chunk_size = args.concurrency * 5  # Process in chunks of 5× concurrency
        t_start = time.time()

        for chunk_start in range(0, len(missing), extraction_chunk_size):
            chunk = missing[chunk_start : chunk_start + extraction_chunk_size]
            log(f"  Extracting chunk {chunk_start + 1}-{chunk_start + len(chunk)} of {len(missing)}...")

            results = asyncio.run(
                extract_batch_async(chunk, args.concurrency, args.model, log)
            )

            for idx, doc_id, rec, labels in results:
                if "_error" in labels:
                    api_errors += 1
                total_input_tokens += labels.pop("_input_tokens", 0)
                total_output_tokens += labels.pop("_output_tokens", 0)
                flusher.add(
                    doc_id, rec, labels,
                    query=rec["query"], engine=rec["engine"], harvest_run_id=rec["run_id"],
                )

            processed = chunk_start + len(chunk)
            elapsed = time.time() - t_start
            rate = processed / elapsed if elapsed > 0 else 0
            est_cost = (
                total_input_tokens * COST_INPUT_PER_MTOK / 1_000_000
                + total_output_tokens * COST_OUTPUT_PER_MTOK / 1_000_000
            )
            log(
                f"  [{processed}/{len(missing)}] ok={flusher.ok} fail={flusher.failed} "
                f"errors={api_errors} rate={rate:.1f}/s "
                f"tokens={total_input_tokens + total_output_tokens} "
                f"est_cost=${est_cost:.3f}"
            )

    flusher.flush()

    log("-" * 60)
    est_cost = (
        total_input_tokens * COST_INPUT_PER_MTOK / 1_000_000
        + total_output_tokens * COST_OUTPUT_PER_MTOK / 1_000_000
    )
    log(
        f"Done. ok={flusher.ok} fail={flusher.failed} "
        f"flushes={flusher.flushes} api_errors={api_errors} "
        f"total_attempts={flusher.total_attempts} input={len(missing)}"
    )
    if not args.fallback_ollama:
        log(
            f"Token usage: input={total_input_tokens} output={total_output_tokens} "
            f"estimated_cost=${est_cost:.3f}"
        )

    res = rc.execute_command(
        "GRAPH.QUERY", GRAPH_NAME,
        f"MATCH (d:Document) WHERE d.id STARTS WITH {cypher_string('apds_' + args.run_id)} RETURN count(d)"
    )
    if res and len(res) > 1 and res[1]:
        log(f"Run {args.run_id} now has: {res[1][0][0]} docs in graph")


if __name__ == "__main__":
    main()

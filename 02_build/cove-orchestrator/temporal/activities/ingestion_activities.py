"""Temporal activities — the ingestion pipeline.

Wraps the unified ingestion pipeline + PUDDING extractor + memory store writer
into Temporal activities that can be orchestrated by a workflow.

These activities run on Beast (triggered via the worker container) and connect
to the local Ollama fleet and the amplified_brain PostgreSQL database
(pgvector/HNSW for vectors, entities+relationships tables for graph).

Canonical data layer: PostgreSQL + pgvector (HNSW) + relational graph.
FalkorDB and Qdrant are deprecated — see 00_authority/DATA_ARCHITECTURE.md.

Signed-by: Devon-c329 | 2026-05-09 | devin-c3297c6e5f464d8fb6d912403b7cc3e6
Based-on: Devon-a4e2 | devin-a4e23461f626488aaf493c55d0c87924
"""

from __future__ import annotations

import hashlib
import json
import logging
import os
import subprocess
import sys
import uuid as _uuid
from dataclasses import dataclass, field
from datetime import datetime, timezone
from pathlib import Path
from typing import Any

from temporalio import activity

logger = logging.getLogger("cove.ingestion")

# ── Beast-native paths ──────────────────────────────────────────────
ARCHIVE_DIR = Path("/opt/amplified/archive")
STORE_B_CLEAN = ARCHIVE_DIR / "store_b_clean"
RAW_DIR = Path("/opt/amplified/raw-mac-dumps")
PUDDING_EXTRACTOR = Path("/opt/amplified/pudding_extractor.py")
PRE_INGESTION_V2 = Path("/opt/amplified/pre_ingestion_pipe_v2.py")
MEMORY_STORE_WRITER = Path("/opt/amplified/memory_store_writer.py")
SEEN_HASHES = STORE_B_CLEAN / "seen_hashes.json"

# ── Ollama (Beast internal) ─────────────────────────────────────────
OLLAMA_URL = os.getenv("OLLAMA_URL", "http://172.18.0.3:11434/api/generate")
OLLAMA_MODEL = os.getenv("OLLAMA_MODEL", "llama3.1:8b")

# ── PostgreSQL amplified_brain (Beast internal) ──────────────────────
# Canonical data layer: pgvector/HNSW for vectors, relational tables for graph.
# See 00_authority/DATA_ARCHITECTURE.md.
BRAIN_DSN = os.getenv(
    "BRAIN_DSN",
    "postgresql://brain_writer@cove-postgres:5432/amplified_brain",
)


# ═════════════════════════════════════════════════════════════════════
# Data Classes
# ═════════════════════════════════════════════════════════════════════

@dataclass
class IngestionInput:
    """Input for the unified ingestion stage."""
    raw_dir: str = str(RAW_DIR)
    clean_archive: str = str(STORE_B_CLEAN)
    full_rebuild: bool = False
    max_workers: int = 8


@dataclass
class IngestionResult:
    """Result from the unified ingestion stage."""
    success: bool
    new_files: int = 0
    total_unique: int = 0
    elapsed_seconds: float = 0.0
    clean_archive: str = ""
    error: str | None = None


@dataclass
class PuddingInput:
    """Input for the PUDDING extraction stage."""
    target_dir: str = str(STORE_B_CLEAN)
    ollama_url: str = OLLAMA_URL
    model: str = OLLAMA_MODEL
    max_workers: int = 4
    limit: int = 0  # 0 = unlimited


@dataclass
class PuddingResult:
    """Result from the PUDDING extraction stage."""
    success: bool
    labelled: int = 0
    skipped: int = 0
    errors: int = 0
    error: str | None = None


@dataclass
class MemoryStoreInput:
    """Input for writing to amplified_brain PostgreSQL (pgvector + relational graph)."""
    source_dir: str = str(STORE_B_CLEAN)
    brain_dsn: str = BRAIN_DSN
    batch_size: int = 100


@dataclass
class MemoryStoreResult:
    """Result from writing to amplified_brain PostgreSQL."""
    success: bool
    pg_vectors: int = 0
    pg_entities: int = 0
    errors: int = 0
    error: str | None = None


@dataclass
class PipelineRun:
    """Full pipeline run metadata."""
    run_id: str
    started_at: str
    ingestion: IngestionResult | None = None
    pudding: PuddingResult | None = None
    memory_store: MemoryStoreResult | None = None
    completed_at: str | None = None
    status: str = "running"


# ═════════════════════════════════════════════════════════════════════
# Helpers
# ═════════════════════════════════════════════════════════════════════

def sha256_file(path: Path) -> str:
    import hashlib
    h = hashlib.sha256()
    with open(path, "rb") as f:
        for chunk in iter(lambda: f.read(1024 * 1024), b""):
            h.update(chunk)
    return h.hexdigest()

def hash_one(args: tuple[Path, Path]) -> dict | None:
    src, _ = args
    try:
        h = sha256_file(src)
        return {"src": str(src), "hash": h, "size": src.stat().st_size}
    except Exception as e:
        import logging
        logging.getLogger("cove.ingestion").warning(f"Hash failed for {src}: {e}")
        return None

# ═════════════════════════════════════════════════════════════════════
# Activity: Unified Ingestion
# ═════════════════════════════════════════════════════════════════════

@activity.defn(name="run_unified_ingestion")
async def run_unified_ingestion(input: IngestionInput) -> IngestionResult:
    """Run the unified ingestion pipeline (dedup + radical naming + attribution).

    Reads raw files from the sovereign dump directory, deduplicates against
    seen_hashes.json, and writes clean, attributed files to store_b_clean.
    """
    import hashlib
    import shutil
    import time
    from concurrent.futures import ProcessPoolExecutor, as_completed

    activity.logger.info(
        f"Ingestion: raw={input.raw_dir}, archive={input.clean_archive}, "
        f"full_rebuild={input.full_rebuild}"
    )

    raw = Path(input.raw_dir)
    archive = Path(input.clean_archive)
    vault = archive
    seen_file = archive / "seen_hashes.json"

    if not raw.exists():
        return IngestionResult(
            success=False,
            clean_archive=str(vault),
            error=f"Raw directory not found: {raw}",
        )

    vault.mkdir(parents=True, exist_ok=True)

    # ── Load seen hashes ──────────────────────────────────────────
    seen: set[str] = set()
    if seen_file.exists() and not input.full_rebuild:
        seen = set(json.loads(seen_file.read_text()))
        activity.logger.info(f"Loaded {len(seen)} seen hashes (incremental)")

    if input.full_rebuild:
        activity.logger.info("Full rebuild — clearing vault")
        shutil.rmtree(vault, ignore_errors=True)
        vault.mkdir(parents=True)
        seen = set()

    # ── Helpers ───────────────────────────────────────────────────
    def sanitize(name: str) -> str:
        clean = "".join(c if c.isalnum() else "-" for c in Path(name).stem)
        return clean.strip("-").lower() or "unnamed"

    def radical_name(filepath: Path, file_hash: str) -> str:
        dt = datetime.fromtimestamp(filepath.stat().st_mtime).strftime("%Y-%m-%d")
        topic = sanitize(filepath.name)
        short = file_hash[:8]
        return f"{dt}_{topic}_Ewan_Sair_{short}{filepath.suffix}"

    # ── Collect candidates ────────────────────────────────────────
    candidates: list[tuple[Path, Path]] = []
    for src in raw.rglob("*"):
        if not src.is_file() or src.name.startswith("._"):
            continue
        candidates.append((src, vault / radical_name(src, "placeholder")))

    activity.logger.info(f"Found {len(candidates)} raw files")

    # ── Hash in parallel ──────────────────────────────────────────
    start = time.time()

    new_items: list[dict] = []
    with ProcessPoolExecutor(max_workers=input.max_workers) as ex:
        futures = {ex.submit(hash_one, c): c for c in candidates}
        for fut in as_completed(futures):
            res = fut.result()
            if res and res["hash"] not in seen:
                seen.add(res["hash"])
                new_items.append(res)

    # ── Copy + attribute ──────────────────────────────────────────
    copied = 0
    for item in new_items:
        src = Path(item["src"])
        real_name = radical_name(src, item["hash"])
        real_target = vault / real_name
        shutil.copy2(src, real_target)

        # Light attribution for JSON dumps
        if real_target.suffix in {".json", ".jsonl"}:
            try:
                data = json.loads(real_target.read_text(errors="ignore"))
                if isinstance(data, dict):
                    data["_ingestion"] = {
                        "date": datetime.now(timezone.utc).isoformat(),
                        "original": str(src),
                        "hash": item["hash"],
                        "status": "cleaned_fast",
                    }
                    real_target.write_text(json.dumps(data, indent=2))
            except Exception:
                pass

        copied += 1
        if copied % 1000 == 0:
            activity.logger.info(f"Progress: {copied} new files cleaned...")

    seen_file.write_text(json.dumps(sorted(seen)))
    elapsed = time.time() - start

    activity.logger.info(
        f"Ingestion complete: {copied} new, {len(seen)} total unique, "
        f"{elapsed:.1f}s"
    )

    return IngestionResult(
        success=True,
        new_files=copied,
        total_unique=len(seen),
        elapsed_seconds=round(elapsed, 1),
        clean_archive=str(vault),
    )


# ═════════════════════════════════════════════════════════════════════
# Activity: PUDDING Extraction
# ═════════════════════════════════════════════════════════════════════

@activity.defn(name="run_pudding_extraction")
async def run_pudding_extraction(input: PuddingInput) -> PuddingResult:
    """PUDDING extraction: async Haiku labelling → PostgreSQL+AGE+pgvector.

    Rewritten for AMP-345. Takes the proven async Haiku extraction from
    apds_labeller_v3_amp173.py and replaces the FalkorDB write path with:
      - PostgreSQL pudding_labels table (with tier, provenance, expiry)
      - Apache AGE business_brain graph (Document nodes with PUDDING labels)

    Three non-negotiable stages (Brain Architecture v3, §6):
      1. Tier tagging — every node defaults to INTUITED
      2. Provenance — source_agent, source_session, source_model, ingest_timestamp
      3. Expiry — valid_until per content type

    Signed-by: Devon-86e7 | 2026-05-15 | devin-86e7ca10cd27467baff9669b1d7113b5
    """
    import asyncio
    import httpx
    import asyncpg

    activity.logger.info(
        f"PUDDING extraction (AMP-345 — PostgreSQL+AGE): dir={input.target_dir}"
    )

    target = Path(input.target_dir)
    if not target.exists():
        return PuddingResult(
            success=False,
            error=f"Target directory not found: {target}",
        )

    # ── Configuration ─────────────────────────────────────────────
    api_key = os.environ.get("ANTHROPIC_API_KEY")
    if not api_key:
        return PuddingResult(
            success=False,
            error="ANTHROPIC_API_KEY environment variable not set",
        )

    dsn = os.getenv("BRAIN_DSN", BRAIN_DSN)
    model = "claude-haiku-4-5-20251001"
    source_agent = "pudding_extractor"
    source_session = os.getenv("DEVIN_SESSION_ID", "temporal-scheduled")
    run_id = f"pudding-{datetime.now(timezone.utc).strftime('%Y%m%dT%H%M%S')}"

    # Expiry defaults (Brain Architecture v3, §6)
    # market/competitive = 90 days, methodology = 1 year, LLM-generated = 90 days
    default_expiry_days = 90

    # ── PUDDING system prompt (from proven v3 labeller) ───────────
    system_prompt = (
        "You are a PUDDING taxonomy labeller. Assign exactly one label per dimension.\n\n"
        "Dimensions:\n"
        "- WHAT: FIN | OPS | MKT | TECH | PPL | GOV | EXT\n"
        "- HOW: METRIC | PROCESS | ASSET | RISK | OPPORTUNITY | RELATIONSHIP | KNOWLEDGE\n"
        "- SCALE: NANO | MICRO | MESO | MACRO | MEGA | META | TEMPORAL\n"
        "- TIME: NOW | NEAR | MID | FAR | EVERGREEN | CYCLICAL | LEGACY\n"
        "- PATTERN: LOG-CAU | LOG-ANA | LOG-SYN | SYS-FB | SYS-EM | SYS-HM | "
        "SYS-BM | HUM-TRUST | HUM-INCENT | HUM-COG | HUM-CULT | VAL-EFF | "
        "VAL-ACC | VAL-ROB | VAL-ADAPT | VAL-ETH\n\n"
        "Output ONLY valid JSON:\n"
        '{"WHAT": "...", "HOW": "...", "SCALE": "...", "TIME": "...", '
        '"PATTERN": "...", "confidence": 0.0-1.0}'
    )
    required_dims = {"WHAT", "HOW", "SCALE", "TIME", "PATTERN"}

    # ── Collect eligible files ────────────────────────────────────
    files: list[Path] = []
    for fp in target.rglob("*"):
        if fp.is_file() and fp.suffix in {".md", ".txt"}:
            files.append(fp)

    if input.limit > 0:
        files = files[: input.limit]

    activity.logger.info(f"Eligible files: {len(files)}")

    if not files:
        return PuddingResult(success=True, labelled=0, skipped=0, errors=0)

    # ── Connect to PostgreSQL ─────────────────────────────────────
    try:
        conn = await asyncpg.connect(dsn)
    except Exception as e:
        return PuddingResult(
            success=False,
            error=f"PostgreSQL connection failed: {e}",
        )

    try:
        # ── Load already-processed hashes (idempotency) ───────────
        existing_hashes: set[str] = set()
        rows = await conn.fetch("SELECT file_hash FROM pudding_labels")
        for row in rows:
            existing_hashes.add(row["file_hash"])
        activity.logger.info(f"Already labelled: {len(existing_hashes)} files")

        # ── Haiku extraction helper (from proven v3 labeller) ─────
        sem = asyncio.Semaphore(input.max_workers)

        async def extract_label(
            text: str, client: httpx.AsyncClient, max_retries: int = 5
        ) -> dict:
            truncated = (text or "")[:2000]
            if not truncated.strip():
                return {"_error": "empty_text"}

            payload = {
                "model": model,
                "max_tokens": 150,
                "system": system_prompt,
                "messages": [{"role": "user", "content": f"Text to label:\n{truncated}"}],
                "temperature": 0.1,
            }

            async with sem:
                for attempt in range(1, max_retries + 1):
                    try:
                        response = await client.post(
                            "https://api.anthropic.com/v1/messages",
                            headers={
                                "x-api-key": api_key,
                                "anthropic-version": "2023-06-01",
                                "content-type": "application/json",
                            },
                            json=payload,
                            timeout=30.0,
                        )

                        if response.status_code == 200:
                            data = response.json()
                            text_out = data["content"][0]["text"].strip()
                            if text_out.startswith("```"):
                                text_out = text_out.split("\n", 1)[-1].rsplit("```", 1)[0]
                            result = json.loads(text_out)
                            if required_dims.issubset(result.keys()):
                                usage = data.get("usage", {})
                                result["_input_tokens"] = usage.get("input_tokens", 0)
                                result["_output_tokens"] = usage.get("output_tokens", 0)
                                return result
                            return {"_error": "missing_dims"}

                        if response.status_code == 429:
                            retry_after = float(
                                response.headers.get("retry-after", attempt * 2)
                            )
                            await asyncio.sleep(retry_after)
                            continue

                        if response.status_code >= 500:
                            await asyncio.sleep(attempt * 2)
                            continue

                        return {"_error": f"http_{response.status_code}"}

                    except (httpx.TimeoutException, httpx.ConnectError):
                        if attempt < max_retries:
                            await asyncio.sleep(attempt * 2)
                            continue
                        return {"_error": "timeout"}
                    except json.JSONDecodeError:
                        return {"_error": "json_parse"}
                    except Exception as e:
                        return {"_error": f"unexpected:{str(e)[:60]}"}

            return {"_error": "max_retries_exhausted"}

        # ── Compute valid_until based on content type ─────────────
        from datetime import timedelta as _td

        def compute_expiry(labels: dict) -> datetime | None:
            time_dim = labels.get("TIME", "")
            if time_dim == "EVERGREEN":
                return None  # no expiry for evergreen content
            if time_dim in ("NOW", "NEAR"):
                # market/competitive data: 90 days
                return datetime.now(timezone.utc) + _td(days=90)
            if time_dim in ("MID", "FAR"):
                # methodology/process: 1 year
                return datetime.now(timezone.utc) + _td(days=365)
            # Default: 90 days (LLM-generated INTUITED content)
            return datetime.now(timezone.utc) + _td(days=default_expiry_days)

        # ── Process files ─────────────────────────────────────────
        labelled = 0
        skipped = 0
        errors = 0

        async with httpx.AsyncClient() as http_client:
            for batch_start in range(0, len(files), 50):
                batch = files[batch_start : batch_start + 50]
                tasks_data: list[tuple[Path, str, str]] = []

                for fp in batch:
                    try:
                        content = fp.read_text(encoding="utf-8", errors="ignore")
                        file_hash = hashlib.sha256(content.encode()).hexdigest()
                        if file_hash in existing_hashes:
                            skipped += 1
                            continue
                        tasks_data.append((fp, file_hash, content))
                    except Exception:
                        errors += 1

                if not tasks_data:
                    continue

                # Extract labels concurrently
                async def process_one(fp: Path, file_hash: str, content: str) -> None:
                    nonlocal labelled, skipped, errors
                    try:
                        labels = await extract_label(content, http_client)
                        if "_error" in labels:
                            errors += 1
                            activity.logger.warning(
                                f"Extraction failed for {fp.name}: {labels['_error']}"
                            )
                            return

                        valid_until = compute_expiry(labels)
                        now_ts = datetime.now(timezone.utc)

                        # ── Write to pudding_labels table ─────────
                        await conn.execute(
                            """INSERT INTO pudding_labels
                               (file_hash, file_path, file_name,
                                what, how, scale, time_dim, pattern, confidence,
                                epistemic_tier, source_agent, source_session,
                                source_model, ingest_timestamp, valid_until,
                                run_id, signed_by)
                            VALUES ($1,$2,$3,$4,$5,$6,$7,$8,$9,$10,$11,$12,$13,$14,$15,$16,$17)
                            ON CONFLICT (file_hash) DO UPDATE SET
                               what = EXCLUDED.what,
                               how = EXCLUDED.how,
                               scale = EXCLUDED.scale,
                               time_dim = EXCLUDED.time_dim,
                               pattern = EXCLUDED.pattern,
                               confidence = EXCLUDED.confidence,
                               valid_until = EXCLUDED.valid_until,
                               run_id = EXCLUDED.run_id,
                               updated_at = now()""",
                            file_hash,
                            str(fp),
                            fp.name,
                            labels.get("WHAT", "UNKNOWN"),
                            labels.get("HOW", "UNKNOWN"),
                            labels.get("SCALE", "UNKNOWN"),
                            labels.get("TIME", "UNKNOWN"),
                            labels.get("PATTERN", "UNKNOWN"),
                            float(labels.get("confidence", 0.0)),
                            "INTUITED",  # tier tagging: always INTUITED at ingestion
                            source_agent,
                            source_session,
                            model,
                            now_ts,
                            valid_until,
                            run_id,
                            source_agent,
                        )

                        # ── Write Document node to AGE graph ──────
                        def _esc(s: str) -> str:
                            return (s or "").replace("\\", "\\\\").replace("'", "\\'").replace("\n", " ")

                        expiry_val = (
                            f"'{valid_until.isoformat()}'"
                            if valid_until else "null"
                        )
                        cypher_stmt = (
                            "SELECT * FROM cypher('business_brain', $$"
                            f" MERGE (d:Document {{file_hash: '{_esc(file_hash)}'}})"
                            f" SET d.file_path = '{_esc(str(fp)[:500])}',"
                            f"     d.title = '{_esc(fp.stem[:200])}',"
                            f"     d.what = '{_esc(labels.get('WHAT', 'UNKNOWN'))}',"
                            f"     d.how = '{_esc(labels.get('HOW', 'UNKNOWN'))}',"
                            f"     d.scale = '{_esc(labels.get('SCALE', 'UNKNOWN'))}',"
                            f"     d.time_dim = '{_esc(labels.get('TIME', 'UNKNOWN'))}',"
                            f"     d.pattern = '{_esc(labels.get('PATTERN', 'UNKNOWN'))}',"
                            f"     d.confidence = {float(labels.get('confidence', 0.0))},"
                            f"     d.epistemic_tier = 'INTUITED',"
                            f"     d.source_agent = '{_esc(source_agent)}',"
                            f"     d.source_session = '{_esc(source_session)}',"
                            f"     d.source_model = '{_esc(model)}',"
                            f"     d.ingest_timestamp = '{now_ts.isoformat()}',"
                            f"     d.valid_until = {expiry_val}"
                            " RETURN d"
                            " $$) AS (v agtype)"
                        )

                        try:
                            await conn.execute("LOAD 'age'")
                            await conn.execute(
                                'SET search_path = ag_catalog, "$user", public'
                            )
                            await conn.execute(cypher_stmt)
                        except Exception as age_err:
                            # AGE write is best-effort; relational table is the
                            # source of truth. Log and continue.
                            activity.logger.warning(
                                f"AGE graph write skipped for {fp.name}: {age_err}"
                            )

                        existing_hashes.add(file_hash)
                        labelled += 1

                    except Exception as e:
                        errors += 1
                        activity.logger.warning(
                            f"PUDDING failed for {fp.name}: {e}"
                        )

                extract_tasks = [
                    process_one(fp, fh, content)
                    for fp, fh, content in tasks_data
                ]
                await asyncio.gather(*extract_tasks)

                activity.logger.info(
                    f"Batch progress: labelled={labelled}, skipped={skipped}, "
                    f"errors={errors}"
                )

    finally:
        await conn.close()

    activity.logger.info(
        f"PUDDING complete: {labelled} labelled, {skipped} skipped, {errors} errors"
    )

    return PuddingResult(
        success=errors == 0,
        labelled=labelled,
        skipped=skipped,
        errors=errors,
        error=f"{errors} extraction failures" if errors else None,
    )


# ═════════════════════════════════════════════════════════════════════
# Activity: Memory Store Writer
# ═════════════════════════════════════════════════════════════════════

@activity.defn(name="write_to_memory_stores")
async def write_to_memory_stores(input: MemoryStoreInput) -> MemoryStoreResult:
    """DEPRECATED by AMP-302 — use canonical_writer.write_canonical_vectors instead.

    This activity bypasses the manifest layer and writes without full provenance.
    Kept for backward compatibility but raises on execution.

    Canonical data layer — see 00_authority/DATA_ARCHITECTURE.md.
    Replacement — see canonical_writer.py (AMP-302 Ticket 3).

    Deprecated-by: Devon-0de2 | 2026-05-11 | AMP-302
    """
    raise RuntimeError(
        "DEPRECATED: write_to_memory_stores retired by AMP-302. "
        "Use canonical_writer.write_canonical_vectors instead. "
        "All writes must go through the manifest-first canonical pipeline."
    )
    import asyncpg
    import yaml

    activity.logger.info(
        f"Memory store write: source={input.source_dir}, "
        f"dsn=***@{input.brain_dsn.split('@')[-1] if '@' in input.brain_dsn else 'localhost'}"
    )

    source = Path(input.source_dir)
    if not source.exists():
        return MemoryStoreResult(
            success=False,
            error=f"Source directory not found: {source}",
        )

    pg_vectors = 0
    pg_entities = 0
    errors = 0

    # ── Collect PUDDING-labelled files ────────────────────────────
    labelled_files: list[Path] = []
    for fp in source.rglob("*.md"):
        try:
            head = fp.read_text(encoding="utf-8", errors="ignore")[:2000]
            if "lbd_attribution" in head and "PUDDING" in head:
                labelled_files.append(fp)
        except Exception:
            pass

    activity.logger.info(f"Found {len(labelled_files)} PUDDING-labelled files")

    if not labelled_files:
        return MemoryStoreResult(success=True)

    # ── Connect to amplified_brain ────────────────────────────────
    try:
        conn = await asyncpg.connect(input.brain_dsn)
    except Exception as e:
        return MemoryStoreResult(
            success=False,
            error=f"PostgreSQL connection failed: {e}",
        )

    try:
        # ── Process in batches ────────────────────────────────────
        for i in range(0, len(labelled_files), input.batch_size):
            batch = labelled_files[i : i + input.batch_size]

            for fp in batch:
                try:
                    content = fp.read_text(encoding="utf-8", errors="ignore")

                    # Extract frontmatter fields
                    fm: dict[str, Any] = {"file": str(fp)}
                    if content.startswith("---"):
                        parts = content.split("---", 2)
                        if len(parts) >= 3:
                            try:
                                parsed_fm = yaml.safe_load(parts[1])
                                if isinstance(parsed_fm, dict):
                                    fm.update(parsed_fm)
                            except Exception as e:
                                activity.logger.warning(
                                    f"Failed to parse YAML for {fp.name}: {e}"
                                )

                    # Extract PUDDING taxonomy fields
                    concepts = fm.get("concepts", [])
                    concept_names = [
                        c.get("name")
                        for c in concepts
                        if isinstance(c, dict) and c.get("name")
                    ]
                    domains = fm.get("domains", [])
                    domain_names = [
                        d.get("name")
                        for d in domains
                        if isinstance(d, dict) and d.get("name")
                    ]
                    doc_type = fm.get("type", "unknown")

                    # Deterministic ID from file path
                    file_hash = hashlib.sha256(str(fp).encode()).hexdigest()
                    vec_id = _uuid.UUID(file_hash[:32])

                    # ── Upsert knowledge_vectors row ──────────────
                    metadata = {
                        "taxonomy_version": fm.get("taxonomy_version", "unknown"),
                        "concepts": concept_names,
                        "domains": domain_names,
                        "doc_type": doc_type,
                        "has_recipes": bool(fm.get("recipes")),
                        "has_signals": bool(fm.get("signals")),
                        "source_count": len(fm.get("sources", [])),
                    }

                    await conn.execute(
                        """INSERT INTO knowledge_vectors
                           (id, content, source, source_type, metadata)
                        VALUES ($1, $2, $3, $4, $5::jsonb)
                        ON CONFLICT (id) DO UPDATE SET
                           content = EXCLUDED.content,
                           metadata = EXCLUDED.metadata,
                           updated_at = now()""",
                        vec_id,
                        content[:4000],
                        str(fp),
                        doc_type,
                        json.dumps(metadata),
                    )
                    pg_vectors += 1

                    # ── Upsert entity per concept ─────────────────
                    for concept in concepts:
                        if not isinstance(concept, dict) or not concept.get("name"):
                            continue
                        ent_id = _uuid.UUID(
                            hashlib.sha256(concept["name"].encode()).hexdigest()[:32]
                        )
                        props = {
                            "pudding_code": concept.get("pudding_code", ""),
                            "description": concept.get("description", ""),
                            "confidence": concept.get("confidence", 0.0),
                            "source_file": str(fp),
                        }
                        await conn.execute(
                            """INSERT INTO entities
                               (id, name, entity_type, summary, properties)
                            VALUES ($1, $2, $3, $4, $5::jsonb)
                            ON CONFLICT (id) DO UPDATE SET
                               properties = entities.properties || EXCLUDED.properties,
                               updated_at = now()""",
                            ent_id,
                            concept["name"],
                            "concept",
                            concept.get("description", ""),
                            json.dumps(props),
                        )
                        pg_entities += 1

                except Exception as e:
                    errors += 1
                    activity.logger.warning(
                        f"Memory write failed for {fp.name}: {e}"
                    )

            activity.logger.info(
                f"Batch {i // input.batch_size + 1}: "
                f"vectors={pg_vectors}, entities={pg_entities}, "
                f"errors={errors}"
            )

    finally:
        await conn.close()

    activity.logger.info(
        f"Memory store complete: {pg_vectors} vectors, "
        f"{pg_entities} entities, {errors} errors"
    )

    return MemoryStoreResult(
        success=errors == 0,
        pg_vectors=pg_vectors,
        pg_entities=pg_entities,
        errors=errors,
        error=f"{errors} write failures" if errors else None,
    )


# ═════════════════════════════════════════════════════════════════════
# Activity: Log Pipeline Run
# ═════════════════════════════════════════════════════════════════════

@activity.defn(name="log_pipeline_run")
async def log_pipeline_run(run: PipelineRun) -> None:
    """Log a pipeline run to PostgreSQL for observability."""
    import asyncpg

    dsn = os.getenv("BRAIN_DSN", BRAIN_DSN)
    conn = await asyncpg.connect(dsn)
    try:
        await conn.execute(
            """INSERT INTO pipeline_runs
            (run_id, started_at, ingestion_new_files, ingestion_total_unique,
             ingestion_elapsed, pudding_labelled, pudding_skipped, pudding_errors,
             memory_pg_vectors, memory_pg_entities, memory_errors,
             completed_at, status)
            VALUES ($1,$2,$3,$4,$5,$6,$7,$8,$9,$10,$11,$12,$13)
            ON CONFLICT (run_id) DO UPDATE SET
              completed_at = $12, status = $13""",
            run.run_id,
            run.started_at,
            run.ingestion.new_files if run.ingestion else 0,
            run.ingestion.total_unique if run.ingestion else 0,
            run.ingestion.elapsed_seconds if run.ingestion else 0,
            run.pudding.labelled if run.pudding else 0,
            run.pudding.skipped if run.pudding else 0,
            run.pudding.errors if run.pudding else 0,
            run.memory_store.pg_vectors if run.memory_store else 0,
            run.memory_store.pg_entities if run.memory_store else 0,
            run.memory_store.errors if run.memory_store else 0,
            run.completed_at,
            run.status,
        )
    finally:
        await conn.close()

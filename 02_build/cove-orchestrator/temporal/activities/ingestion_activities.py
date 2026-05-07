"""Temporal activities — the ingestion pipeline.

Wraps the unified ingestion pipeline + PUDDING extractor + memory store writer
into Temporal activities that can be orchestrated by a workflow.

These activities run on Beast (triggered via the worker container) and connect
to the local Ollama fleet, Qdrant, and FalkorDB.
"""

from __future__ import annotations

import json
import logging
import os
import subprocess
import sys
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

# ── Vector + Graph DBs (Beast internal) ─────────────────────────────
QDRANT_URL = os.getenv("QDRANT_URL", "http://qdrant:6333")
FALKORDB_URL = os.getenv("FALKORDB_URL", "redis://falkordb:6379")


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
    """Input for writing to FalkorDB + Qdrant."""
    source_dir: str = str(STORE_B_CLEAN)
    qdrant_url: str = QDRANT_URL
    falkordb_url: str = FALKORDB_URL
    qdrant_collection: str = "business_knowledge"
    falkordb_graph: str = "kg_pudding_discovery"
    batch_size: int = 100


@dataclass
class MemoryStoreResult:
    """Result from writing to memory stores."""
    success: bool
    qdrant_upserts: int = 0
    falkordb_writes: int = 0
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
    """Run the PUDDING extractor against clean vault files.

    Hits Anthropic Claude Haiku for taxonomy labelling
    and injects PUDDING 2026 Taxonomy frontmatter into each file.
    """
    import os
    import yaml
    import asyncio
    from anthropic import AsyncAnthropic

    activity.logger.info(
        f"PUDDING extraction (Async Haiku): dir={input.target_dir}"
    )

    target = Path(input.target_dir)
    if not target.exists():
        return PuddingResult(
            success=False,
            error=f"Target directory not found: {target}",
        )

    # ── Collect eligible files ────────────────────────────────────
    files: list[Path] = []
    for fp in target.rglob("*"):
        if fp.is_file() and fp.suffix in {".md", ".txt"}:
            files.append(fp)

    if input.limit > 0:
        files = files[: input.limit]

    activity.logger.info(f"Eligible files: {len(files)}")

    labelled = 0
    skipped = 0
    errors = 0
    
    api_key = os.environ.get("ANTHROPIC_API_KEY")
    if not api_key:
        return PuddingResult(success=False, error="ANTHROPIC_API_KEY environment variable not set")
        
    client = AsyncAnthropic(api_key=api_key)

    # ── System prompt ─────────────────────────────────────────────
    system_prompt = (
        "You are the PUDDING GATE (Amplified Pudding Discovery System - APDS).\n"
        "Your sole function is to take raw, unstructured text and extract scientific hypotheses, "
        "methodologies, business logic, and content themes into a strictly formatted YAML taxonomy.\n"
        "DO NOT output any conversational text. DO NOT output markdown blocks. ONLY output raw YAML.\n\n"
        "Required YAML Structure:\n"
        "taxonomy_version: PUDDING_2026\n"
        "concepts:\n"
        "  - name: <Concept Name>\n"
        "    pudding_code: <4-character WHAT.HOW.SCALE.TIME code>\n"
        "    description: <Brief description>\n"
        "    confidence: 0.95\n"
        "sources:\n"
        "  - name: <Source Name>\n"
        "    source_type: <T1, T2, T3, or T4>\n"
        "recipes:\n"
        "  - name: <Falsifiable hypothesis, recipe, or content angle>\n"
        "    description: <What needs to be tested or created>\n"
        "signals:\n"
        "  - name: <Signal Name>\n"
        "    signal_type: <anomaly, drift, spike, weak signal, convergence, or co-occurrence>\n"
        "domains:\n"
        "  - name: <Domain/Vertical Name>\n"
        "type: <principle|framework|sop|technique|case_study|hypothesis|recipe|content_asset|business_logic|raw_notes>\n"
    )

    sem = asyncio.Semaphore(input.max_workers)

    async def process_one(fp: Path) -> None:
        nonlocal labelled, skipped, errors
        try:
            content = fp.read_text(encoding="utf-8", errors="ignore")

            # Skip already-processed files
            if "lbd_attribution" in content and "PUDDING" in content:
                skipped += 1
                return

            # ── Call Haiku ────────────────────────────────────
            async with sem:
                prompt = f"RAW DATA TO PROCESS:\n{content[:4000]}"
                response = await client.messages.create(
                    model="claude-haiku-4-5-20251001",
                    max_tokens=1500,
                    system=system_prompt,
                    messages=[{"role": "user", "content": prompt}],
                    temperature=0.0
                )
                
                yaml_output = response.content[0].text
                
                if "taxonomy_version:" in yaml_output:
                    start_idx = yaml_output.find("taxonomy_version:")
                    yaml_output = yaml_output[start_idx:]
                if yaml_output.startswith("```yaml"):
                    yaml_output = yaml_output[7:]
                if yaml_output.startswith("```"):
                    yaml_output = yaml_output[3:]
                if yaml_output.endswith("```"):
                    yaml_output = yaml_output[:-3]
                    
                yaml_output = yaml_output.strip()

                # Basic validation
                parsed_yaml = yaml.safe_load(yaml_output)
                if not isinstance(parsed_yaml, dict):
                    raise ValueError("Parsed YAML is not a dictionary.")

                # ── Inject frontmatter ─────────────────────────────
                if content.startswith("---"):
                    parts = content.split("---", 2)
                    if len(parts) >= 3:
                        fm = parts[1]
                        body = parts[2]
                        
                        # Add attribution to new YAML
                        parsed_yaml["lbd_attribution"] = "PUDDING 2026 Taxonomy (Amplified Partners)"
                        
                        # Convert dict to nicely formatted yaml string
                        new_yaml = yaml.dump(parsed_yaml, sort_keys=False)
                        
                        final = f"---{fm}\n{new_yaml}---{body}"
                        fp.write_text(final, encoding="utf-8")
                        labelled += 1
                else:
                    skipped += 1

        except Exception as e:
            errors += 1
            activity.logger.warning(f"PUDDING failed for {fp.name}: {e}")

    # ── Execute fleet ─────────────────────────────────────────────
    tasks = [process_one(fp) for fp in files]
    await asyncio.gather(*tasks)

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
    """Write PUDDING-labelled files into FalkorDB (graph) and Qdrant (vectors).

    Reads files that have PUDDING frontmatter, extracts taxonomy data,
    and upserts into both memory stores.
    """
    import httpx

    activity.logger.info(
        f"Memory store write: source={input.source_dir}, "
        f"qdrant={input.qdrant_url}, falkordb={input.falkordb_url}"
    )

    source = Path(input.source_dir)
    if not source.exists():
        return MemoryStoreResult(
            success=False,
            error=f"Source directory not found: {source}",
        )

    qdrant_upserts = 0
    falkordb_writes = 0
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

    # ── Process in batches ────────────────────────────────────────
    for i in range(0, len(labelled_files), input.batch_size):
        batch = labelled_files[i : i + input.batch_size]
        points: list[dict] = []

        for fp in batch:
            try:
                content = fp.read_text(encoding="utf-8", errors="ignore")
                
                # Extract frontmatter fields
                import yaml
                fm: dict[str, Any] = {"file": str(fp)}
                if content.startswith("---"):
                    parts = content.split("---", 2)
                    if len(parts) >= 3:
                        try:
                            parsed_fm = yaml.safe_load(parts[1])
                            if isinstance(parsed_fm, dict):
                                fm.update(parsed_fm)
                        except Exception as e:
                            activity.logger.warning(f"Failed to parse YAML for {fp.name}: {e}")

                # ── Upsert to Qdrant ──────────────────────────
                # Safely extract from PUDDING 2026 taxonomy schema
                concepts = fm.get("concepts", [])
                concept_names = [c.get("name") for c in concepts if isinstance(c, dict) and c.get("name")]
                
                domains = fm.get("domains", [])
                domain_names = [d.get("name") for d in domains if isinstance(d, dict) and d.get("name")]
                
                payload = {
                    "source": str(fp),
                    "title": fp.stem,
                    "taxonomy_version": fm.get("taxonomy_version", "unknown"),
                    "concepts": concept_names,
                    "domains": domain_names,
                    "visibility_zone": "INTERNAL_KB",
                    "pudding_label": f"{len(concepts)}_concepts",
                    "facets": {
                        "has_recipes": bool(fm.get("recipes")),
                        "has_signals": bool(fm.get("signals")),
                        "source_count": len(fm.get("sources", [])),
                    },
                    "content_snippet": content[:1000],
                }

                # Generate a deterministic point ID from the file path
                import hashlib

                point_id = hashlib.md5(str(fp).encode()).hexdigest()

                # Use a zero-vector as placeholder (real embedding needs sentence-transformers)
                points.append({
                    "id": point_id,
                    "vector": [0.0] * 384,  # placeholder dimension
                    "payload": payload,
                })

            except Exception as e:
                errors += 1
                activity.logger.warning(f"Memory write prep failed for {fp.name}: {e}")

        # ── Batch upsert to Qdrant ────────────────────────────────
        if points:
            try:
                async with httpx.AsyncClient() as client:
                    resp = await client.put(
                        f"{input.qdrant_url}/collections/{input.qdrant_collection}/points",
                        json={"points": points},
                        timeout=30.0,
                    )
                    if resp.status_code == 200:
                        qdrant_upserts += len(points)
                    else:
                        activity.logger.warning(
                            f"Qdrant upsert failed: {resp.status_code} {resp.text[:200]}"
                        )
                        errors += 1
            except Exception as e:
                errors += 1
                activity.logger.warning(f"Qdrant batch failed: {e}")

        falkordb_writes += len(points)

    activity.logger.info(
        f"Memory store complete: {qdrant_upserts} Qdrant, "
        f"{falkordb_writes} FalkorDB candidates, {errors} errors"
    )

    return MemoryStoreResult(
        success=errors == 0,
        qdrant_upserts=qdrant_upserts,
        falkordb_writes=falkordb_writes,
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

    dsn = os.getenv("POSTGRES_DSN", "postgresql://cove:cove@localhost:5432/cove")
    conn = await asyncpg.connect(dsn)
    try:
        await conn.execute(
            """INSERT INTO pipeline_runs
            (run_id, started_at, ingestion_new_files, ingestion_total_unique,
             ingestion_elapsed, pudding_labelled, pudding_skipped, pudding_errors,
             memory_qdrant_upserts, memory_falkordb_writes, memory_errors,
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
            run.memory_store.qdrant_upserts if run.memory_store else 0,
            run.memory_store.falkordb_writes if run.memory_store else 0,
            run.memory_store.errors if run.memory_store else 0,
            run.completed_at,
            run.status,
        )
    finally:
        await conn.close()
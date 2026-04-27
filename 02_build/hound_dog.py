#!/usr/bin/env python3
"""
Hound Dog - Forensic Data Mining & Convergence Engine
===================================================
Based on the Amplified Partners Vault Extraction Pipeline specs.
This tool crawls a target directory, extracts raw data (markdown, txt),
and uses an LLM (via the local Swarm or OpenAI) to mine and structure:
1. Raw Text
2. Structured JSON
3. Process/Logic
4. Principles/Values

It acts as both the "Hound Dog" (discovery/clustering) and "DocBench" (extraction).
"""

import os
import json
import glob
import hashlib
import ppdeep
from pathlib import Path
from datetime import datetime

# You can point this to OpenAI or your local Beast Swarm API
import httpx
import asyncio

# Target directories to sniff (can include system guts like Claude's local storage)
TARGET_DIRS = [
    "/Users/ewansair/Vaults/Ewan",
    os.path.expanduser("~/Library/Application Support/Claude/logs"), # Where Claude hides its stuff
    "/Users/ewansair/Downloads/Google-Drive-Miner",
    "/Users/ewansair/Downloads/Google-Drive-Miner 2"
]
OUTPUT_DIR = "/Users/ewansair/Vaults/Ewan/02-extracted-data"

# Create output dir
os.makedirs(OUTPUT_DIR, exist_ok=True)

# Central Ops Voice/Text API for processing
# Hardcoded to route over Tailscale to the Beast (macairm5)
API_URL = os.environ.get("BEAST_URL", "http://100.85.225.46:8001/api/voice") 

def crawl_directory(target_paths):
    files = []
    extensions = ["*.md", "*.txt", "*.json", "*.log"]
    
    for path in target_paths:
        print(f"[*] Hound Dog is sniffing: {path}")
        for ext in extensions:
            files.extend(glob.glob(f"{path}/**/{ext}", recursive=True))
            
    return files

async def extract_data(file_path):
    print(f"[*] DocBench extracting: {file_path}")
    with open(file_path, "r", encoding="utf-8") as f:
        content = f.read()

    prompt = f"""
    You are the Amplified Partners DocBench Extraction Engine.
    Analyze the following raw document and extract the core data into a comprehensive, long-form structured format.
    
    You must extract the content into exactly four categories. For EVERY single item extracted, you MUST provide an "Attribute" (who said it, source file, context, or origin) if possible. Do not summarize the raw voice; preserve it.
    
    1. **Blogs**: Identify and extract full, coherent narratives or stories that can be published as long-form blog posts. Preserve the author's voice entirely.
    2. **Quotes**: Extract specific, powerful, quotable sentences or statements.
    3. **Paragraphs**: Extract standalone, high-value paragraphs that explain a concept, a process, or a principle.
    4. **Nuggets**: Extract short, punchy facts, data points, or core logic pieces.

    Document:
    {content}
    """
    
    try:
        async with httpx.AsyncClient() as client:
            resp = await client.post(
                "http://localhost:8004/api/generate",
                json={
                    "model": "llama3.1:8b",
                    "prompt": prompt,
                    "stream": False,
                    "options": {
                        "temperature": 0.2
                    }
                },
                timeout=300.0  # Local inference might take longer
            )
            if resp.status_code == 200:
                return resp.json().get("response", "")
            else:
                return f"Error: {resp.text}"
    except Exception as e:
        return f"Extraction failed: {str(e)}"

async def run_pipeline():
    files = crawl_directory(TARGET_DIRS)
    print(f"[*] Hound Dog found {len(files)} orphaned/raw files.")

    seen_sha256 = set()
    seen_fuzzy = []

    for file_path in files:
        if "02-extracted-data" in file_path:
            continue # Skip already extracted data
            
        # --- TIER 1 & 2 DEDUPLICATION ---
        with open(file_path, "rb") as f:
            raw_bytes = f.read()
            
        # 1. SHA-256 Exact Match
        exact_hash = hashlib.sha256(raw_bytes).hexdigest()
        if exact_hash in seen_sha256:
            print(f"[SKIP] Exact Duplicate (SHA-256): {os.path.basename(file_path)}")
            continue
        seen_sha256.add(exact_hash)
        
        # 2. ppdeep Fuzzy Hash Match
        fuzzy_hash = ppdeep.hash(raw_bytes)
        is_fuzzy_dup = False
        for seen_fh in seen_fuzzy:
            # If similarity > 95, it's a near-duplicate
            if ppdeep.compare(fuzzy_hash, seen_fh) > 95:
                is_fuzzy_dup = True
                break
                
        if is_fuzzy_dup:
            print(f"[SKIP] Near-Duplicate (Fuzzy Hash >95%): {os.path.basename(file_path)}")
            continue
        seen_fuzzy.append(fuzzy_hash)

        print(f"\n--- Mining: {os.path.basename(file_path)} ---")
        extracted_content = await extract_data(file_path)
        
        # Save output
        filename = Path(file_path).stem + "_extraction.md"
        out_path = os.path.join(OUTPUT_DIR, filename)
        
        with open(out_path, "w", encoding="utf-8") as f:
            f.write(f"# DocBench Extraction: {Path(file_path).stem}\n\n")
            f.write(extracted_content)
            
        print(f"[+] Extraction saved to: {out_path}")

if __name__ == "__main__":
    print("=============================================")
    print(" HOUND DOG \u0026 DOCBENCH: FORENSIC DATA MINING")
    print("=============================================")
    asyncio.run(run_pipeline())
    print("\n[*] Data Mining Complete. Ready for PUDDING Labelling.")

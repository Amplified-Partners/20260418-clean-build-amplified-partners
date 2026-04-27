#!/usr/bin/env python3
import os
import glob
import json
import asyncio
import httpx
from pathlib import Path

TARGET_DIR = "/Users/ewansair/Vaults/Ewan/Voice-Transcripts"
OUTPUT_DIR = "/Users/ewansair/Vaults/Ewan/02-extracted-data"
OLLAMA_API = "http://localhost:8004/api/chat"

os.makedirs(OUTPUT_DIR, exist_ok=True)

async def pudding_extract(file_path):
    print(f"[*] Pudding Processing: {os.path.basename(file_path)}")
    with open(file_path, "r", encoding="utf-8") as f:
        content = f.read()

    prompt = f"""
    You are the Amplified Partners Pudding Extraction Engine.
    Analyze the following raw transcript and extract the core data into a comprehensive, structured format.
    
    You must extract the content into exactly four categories. Provide an "Attribute" for EVERY item.
    
    1. **Blogs**: Identify full narratives or stories.
    2. **Quotes**: Extract specific, powerful sentences.
    3. **Paragraphs**: Extract standalone, high-value paragraphs explaining concepts.
    4. **Nuggets**: Extract short, punchy facts or core logic pieces.

    Transcript:
    {content}
    """
    
    try:
        async with httpx.AsyncClient() as client:
            resp = await client.post(
                OLLAMA_API,
                json={
                    "model": "llama3.1:8b",
                    "messages": [{"role": "user", "content": prompt}],
                    "stream": False,
                    "options": {"temperature": 0.2}
                },
                timeout=300.0
            )
            if resp.status_code == 200:
                return resp.json()["message"]["content"]
            else:
                return f"Error: {resp.text}"
    except Exception as e:
        return f"Extraction failed: {str(e)}"

async def run_batch():
    files = glob.glob(f"{TARGET_DIR}/**/*.md", recursive=True) + glob.glob(f"{TARGET_DIR}/**/*.txt", recursive=True)
    print(f"[*] Found {len(files)} files to Pudding.")

    for file_path in files: # Processing entire archive
        filename = Path(file_path).stem + "_pudding.md"
        out_path = os.path.join(OUTPUT_DIR, filename)
        
        if os.path.exists(out_path):
            continue

        extracted_content = await pudding_extract(file_path)
        
        with open(out_path, "w", encoding="utf-8") as f:
            f.write(f"# Pudding Extraction: {Path(file_path).stem}\n\n")
            f.write(extracted_content)
            
        print(f"[+] Pudding saved to: {out_path}")

if __name__ == "__main__":
    asyncio.run(run_batch())

#!/usr/bin/env python3
import os
import glob
import random
import httpx
import asyncio

CRM_DIR = "/Users/ewansair/Vaults/Ewan/AI-Rescued-CRM-Data-2"
TAKEOUT_DIR = "/Users/ewansair/Vaults/Ewan/02-extracted-data"

def get_random_files(directory, ext="*.md", count=3):
    files = glob.glob(f"{directory}/**/{ext}", recursive=True)
    if not files:
        return []
    return random.sample(files, min(count, len(files)))

def read_file(path):
    with open(path, "r", encoding="utf-8") as f:
        # Read only first 2000 chars to avoid overwhelming the context window
        return f.read()[:2000] 

async def cross_pollinate():
    print("[*] Gathering data from CRM...")
    crm_files = get_random_files(CRM_DIR, count=3)
    if not crm_files:
        print("[!] No CRM files found.")
        return
    crm_text = "\n\n".join([f"--- CRM FILE: {os.path.basename(f)} ---\n{read_file(f)}" for f in crm_files])
    
    print("[*] Gathering data from Google Takeout (Database)...")
    takeout_files = get_random_files(TAKEOUT_DIR, count=3)
    if not takeout_files:
        print("[!] No Google Takeout extracted files found yet. Let Hound Dog finish extracting some files first.")
        return
    takeout_text = "\n\n".join([f"--- TAKEOUT FILE: {os.path.basename(f)} ---\n{read_file(f)}" for f in takeout_files])
    
    prompt = f"""
    You are the Amplified Partners Pudding Factory. 
    You must use the "Pudding Technique" (Swanson's ABC Model of Literature-Based Discovery) to find hidden connections between two completely separate data silos.
    
    Data Silo A (CRM System Ideas):
    {crm_text}
    
    Data Silo C (Google Takeout Database Ideas):
    {takeout_text}
    
    Task: Find the "Bridging Concepts" (B). What hidden logic, mechanism, or principle connects an idea in Silo A to an idea in Silo C?
    Output your findings explicitly using the Novel Taxonomy:
    1. Trust Builder Connection
    2. Intelligence Generator Connection
    3. Friction Remover Connection
    4. Learning Loop Connection
    
    Do not hallucinate. Base connections only on the provided text.
    """
    
    print("[*] Firing up the Pudding Factory (Local Llama 3.1 Swarm)...")
    try:
        async with httpx.AsyncClient() as client:
            resp = await client.post(
                "http://localhost:8004/api/generate",
                json={
                    "model": "llama3.1:8b",
                    "prompt": prompt,
                    "stream": False,
                    "options": {
                        "temperature": 0.3
                    }
                },
                timeout=300.0
            )
            if resp.status_code == 200:
                result = resp.json().get("response", "")
                print("\n================ PUDDING FACTORY RESULTS ================\n")
                print(result)
                print("\n=========================================================\n")
            else:
                print(f"Error: {resp.text}")
    except Exception as e:
        print(f"Failed to connect to Swarm: {e}")

if __name__ == "__main__":
    print("=============================================")
    print(" THE PUDDING FACTORY: CROSS-POLLINATOR")
    print("=============================================")
    asyncio.run(cross_pollinate())

import os
import httpx
from temporalio import activity

# Helper to simulate an API call if keys are missing
async def _mock_or_call(partner_name: str, prompt: str, url: str, headers: dict, payload: dict) -> str:
    if not any(v for k, v in headers.items() if "Bearer " in v and len(v) > 10):
        # Return a smart mock so he can test the UI right away without hunting for keys
        activity.logger.info(f"No API key for {partner_name}. Returning mock response.")
        return f"[{partner_name} Offline] Simulated response to: '{prompt}'. In production, I would give you the unvarnished truth here."
    
    try:
        async with httpx.AsyncClient() as client:
            resp = await client.post(url, headers=headers, json=payload, timeout=50.0)
            resp.raise_for_status()
            data = resp.json()
            # Different providers have slightly different response shapes
            if partner_name == "Claude":
                return data["content"][0]["text"]
            return data["choices"][0]["message"]["content"]
    except Exception as e:
        return f"[{partner_name} Error] {str(e)}"

@activity.defn(name="consult_perplexity")
async def consult_perplexity(prompt: str, api_key: str) -> str:
    url = "https://api.perplexity.ai/chat/completions"
    headers = {"Authorization": f"Bearer {api_key}", "Content-Type": "application/json"}
    payload = {
        "model": "llama-3-sonar-large-32k-online",
        "messages": [
            {"role": "system", "content": "You are the Scribe. Give a deep research synthesis."}, 
            {"role": "user", "content": prompt}
        ]
    }
    return await _mock_or_call("Perplexity", prompt, url, headers, payload)

@activity.defn(name="consult_antigravity")
async def consult_antigravity(prompt: str, api_key: str) -> str:
    url = f"https://generativelanguage.googleapis.com/v1beta/models/gemini-1.5-pro:generateContent?key={api_key}"
    # Gemini API shape is different, so we handle it custom here
    if not api_key:
        return f"[Antigravity Offline] Simulated response to: '{prompt}'. In production, I would build the system architecture."
    
    try:
        async with httpx.AsyncClient() as client:
            resp = await client.post(url, json={"contents": [{"parts":[{"text": prompt}]}]}, timeout=50.0)
            resp.raise_for_status()
            data = resp.json()
            return data["candidates"][0]["content"]["parts"][0]["text"]
    except Exception as e:
        return f"[Antigravity Error] {str(e)}"

@activity.defn(name="consult_claude")
async def consult_claude(prompt: str, api_key: str) -> str:
    url = "https://api.anthropic.com/v1/messages"
    headers = {
        "x-api-key": api_key,
        "anthropic-version": "2023-06-01",
        "Content-Type": "application/json"
    }
    payload = {
        "model": "claude-3-opus-20240229",
        "max_tokens": 1000,
        "system": "You are Devin/Claude. Enforce discipline and review the proposal.",
        "messages": [{"role": "user", "content": prompt}]
    }
    if not api_key:
        return f"[Claude/Devin Offline] Simulated response to: '{prompt}'. In production, I would critique your assumptions."
    
    try:
        async with httpx.AsyncClient() as client:
            resp = await client.post(url, headers=headers, json=payload, timeout=50.0)
            resp.raise_for_status()
            data = resp.json()
            return data["content"][0]["text"]
    except Exception as e:
        return f"[Claude/Devin Error] {str(e)}"

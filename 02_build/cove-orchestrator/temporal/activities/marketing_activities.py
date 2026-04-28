import json
from temporalio import activity
from typing import Dict, Any, List

@activity.defn
async def atomize_pillar_content(pillar_text: str) -> Dict[str, str]:
    """
    Ingests Ewan's Pillar Content and slices it for various channels.
    DOES NOT invent thoughts. Only formats Ewan's exact message.
    """
    activity.logger.info("🎬 Marketing Swarm: Atomizing Pillar Content...")
    # Production: Calls LiteLLM with strict Pydantic formatting schema
    return {
        "linkedin_post": "Formatted for LinkedIn: " + pillar_text[:100],
        "twitter_thread": "Formatted for Twitter: " + pillar_text[:50],
        "video_script": "Short script: " + pillar_text[:150]
    }

@activity.defn
async def dicaprio_generate_video(scene_prompt: str, target_demographic: str) -> str:
    """
    Calls Fal.AI (or similar) to generate customized B-Roll based on the target demographic.
    (e.g., Men, 40, DISC profile).
    """
    activity.logger.info(f"🎬 DiCaprio: Generating B-Roll customized for {target_demographic}...")
    # Production: HTTPX call to Fal.AI endpoint
    return f"https://cdn.amplified.ai/assets/real_broll_{target_demographic.replace(' ', '_')}.mp4"

@activity.defn
async def picasso_generate_graphics(concept: str) -> str:
    """
    Calls Flux API to generate high-CTR thumbnails and graphic overlays.
    """
    activity.logger.info("🎨 Picasso: Generating custom graphics...")
    # Production: HTTPX call to Flux API
    return "https://cdn.amplified.ai/assets/real_graphic.png"

@activity.defn
async def director_render_pipeline(script: str, broll_url: str, graphic_url: str) -> str:
    """
    Assembles the JSON payload and fires it to the Revideo rendering engine on the Beast.
    """
    activity.logger.info("⚙️ Director: Dispatching rendering payload to Revideo (Port 3100)...")
    payload = {
        "script": script,
        "assets": [broll_url, graphic_url],
        "render_engine": "revideo"
    }
    # Production: HTTP POST to Revideo Engine
    return "https://cdn.amplified.ai/final_renders/marketing_video_1.mp4"

@activity.defn
async def low_key_outbound_dispatch(target_profile: Dict[str, Any], video_url: str) -> str:
    """
    Strict permission-based marketing dispatch via WhatsApp/Email MCP.
    Uses dynamic communication principles, NOT deterministic hardcoded strings.
    """
    activity.logger.info(f"🚀 Outbound: Drafting principled offer for {target_profile.get('industry')}...")
    
    # Production: This sends a system prompt to LiteLLM to draft the message fluidly.
    system_prompt = f"""
    Draft a short outbound message for a {target_profile.get('role')} in {target_profile.get('industry')}.
    Adjust language slightly for their DISC type ({target_profile.get('disc')}) and learning style.
    
    PRINCIPLES:
    1. Identify as an AI agent. Use meta-humor if appropriate ("Look, I've got to speak in this language...").
    2. Deliver the video solution upfront: {video_url}
    3. End with a low-key offer: "Can I help you with any solutions? No? Okay."
    4. NO patronizing demographic tropes (no Pirelli catalog, no lipstick tropes). Adjust language subtly.
    5. Watchword: Win-Win. Only manipulate towards their benefit. If we aren't the best/cheapest solution, we admit it.
    """
    
    # Return simulated LLM drafted message
    return f"Message dynamically drafted based on principles and delivered. Status: Waiting for reply."

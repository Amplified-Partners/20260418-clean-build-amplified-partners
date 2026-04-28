"""
Marketing Engine — Orchestrator
Chains research → content → publishing for each client.

Daily cron on The Beast:
  6:00 — Research agent
  7:00 — Content agent (uses research output)
  7:30 — Publishing agent (publishes approved content)

Can also be run manually for a single client.
"""

import asyncio
import json
import logging
import sys
from datetime import datetime
from pathlib import Path

from agents.research_agent import ResearchAgent
from agents.content_agent import ContentAgent
from agents.publishing_agent import PublishingAgent

logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s [%(name)s] %(levelname)s: %(message)s",
    datefmt="%Y-%m-%d %H:%M:%S",
)
logger = logging.getLogger("marketing.orchestrator")


async def run_client_pipeline(client_id: str, config_path: str = "/app/config/engine_config.yaml"):
    """Run full research → content → publish pipeline for one client."""
    start = datetime.utcnow()
    logger.info(f"{'='*60}")
    logger.info(f"PIPELINE START: {client_id} at {start.isoformat()}")
    logger.info(f"{'='*60}")

    # Phase 1: Research
    logger.info(f"\n--- RESEARCH PHASE ---")
    research_agent = ResearchAgent(config_path)
    try:
        brief = await research_agent.run(client_id)
        logger.info(f"Research: {len(brief.results)} results, {len(brief.suggested_topics)} topics")
    except Exception as e:
        logger.error(f"Research failed: {e}")
        brief = None

    # Phase 2: Content Generation
    logger.info(f"\n--- CONTENT PHASE ---")
    content_agent = ContentAgent(config_path)
    try:
        pieces = await content_agent.run(client_id, research_brief=brief)
        logger.info(f"Content: {len(pieces)} pieces generated")
        for p in pieces:
            logger.info(f"  {p.platform}/{p.content_type}: score={p.quality_score:.1f} status={p.status}")
    except Exception as e:
        logger.error(f"Content generation failed: {e}")
        pieces = []

    # Phase 3: Publishing
    logger.info(f"\n--- PUBLISHING PHASE ---")
    publishing_agent = PublishingAgent(config_path)
    try:
        results = await publishing_agent.run(client_id, pieces)
        logger.info(f"Publishing: {len(results)} results")
        for r in results:
            logger.info(f"  {r.platform}: {r.status}")
    except Exception as e:
        logger.error(f"Publishing failed: {e}")
        results = []

    # Summary
    elapsed = (datetime.utcnow() - start).total_seconds()
    logger.info(f"\n{'='*60}")
    logger.info(f"PIPELINE COMPLETE: {client_id} in {elapsed:.1f}s")
    logger.info(f"  Research: {len(brief.results) if brief else 0} results")
    logger.info(f"  Content: {len(pieces)} pieces ({sum(1 for p in pieces if p.status == 'approved')} approved)")
    logger.info(f"  Published: {sum(1 for r in results if r.status == 'published')}")
    logger.info(f"{'='*60}\n")

    return {
        "client_id": client_id,
        "elapsed_seconds": elapsed,
        "research_results": len(brief.results) if brief else 0,
        "content_pieces": len(pieces),
        "approved": sum(1 for p in pieces if p.status == "approved"),
        "published": sum(1 for r in results if r.status == "published"),
    }


async def run_all_clients(config_path: str = "/app/config/engine_config.yaml"):
    """Run pipeline for all active clients."""
    clients_dir = Path("/app/config/clients")
    client_ids = [
        f.stem for f in clients_dir.glob("*.yaml")
        if not f.name.startswith("_")
    ]

    logger.info(f"Running pipeline for {len(client_ids)} clients: {client_ids}")

    results = []
    for client_id in client_ids:
        try:
            result = await run_client_pipeline(client_id, config_path)
            results.append(result)
        except Exception as e:
            logger.error(f"Pipeline failed for {client_id}: {e}")
            results.append({"client_id": client_id, "error": str(e)})

    # Summary
    logger.info(f"\n{'='*60}")
    logger.info(f"ALL PIPELINES COMPLETE")
    for r in results:
        if "error" in r:
            logger.error(f"  {r['client_id']}: FAILED — {r['error']}")
        else:
            logger.info(f"  {r['client_id']}: {r['published']}/{r['content_pieces']} published in {r['elapsed_seconds']:.1f}s")
    logger.info(f"{'='*60}")

    return results


if __name__ == "__main__":
    if len(sys.argv) > 1:
        # Run for specific client
        client_id = sys.argv[1]
        asyncio.run(run_client_pipeline(client_id))
    else:
        # Run all clients
        asyncio.run(run_all_clients())

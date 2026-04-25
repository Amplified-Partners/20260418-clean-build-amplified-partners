"""NightScout entry point — run the pipeline or generate a briefing."""

from __future__ import annotations

import asyncio
import logging
import sys

logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s [%(name)s] %(levelname)s: %(message)s",
)


async def main() -> None:
    command = sys.argv[1] if len(sys.argv) > 1 else "run"

    if command == "run":
        from .pipeline import run_pipeline
        stats = await run_pipeline()
        print(f"\n{'='*50}")
        print(f"NightScout Pipeline Complete")
        print(f"  Sources fetched: {stats['sources_fetched']}")
        print(f"  Items fetched:   {stats['items_fetched']}")
        print(f"  Items scored:    {stats['items_scored']}")
        print(f"  → Briefing:      {stats['items_briefing']}")
        print(f"  → R&D Pipeline:  {stats['items_rd']}")
        print(f"  → Critical:      {stats['items_critical']}")
        if stats["errors"]:
            print(f"  Errors: {len(stats['errors'])}")
            for e in stats["errors"][:5]:
                print(f"    - {e}")
        print(f"{'='*50}")

    elif command == "briefing":
        from .briefing import generate_morning_briefing
        hours = int(sys.argv[2]) if len(sys.argv) > 2 else 24
        md = await generate_morning_briefing(hours)
        print(md)

    else:
        print("Usage: python -m nightscout [run|briefing] [hours_back]")
        sys.exit(1)


if __name__ == "__main__":
    asyncio.run(main())

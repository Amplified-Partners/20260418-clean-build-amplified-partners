"""Email Agent entry point."""

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
        print("Email Agent Pipeline Complete")
        print(f"  Emails fetched:    {stats['emails_fetched']}")
        print(f"  Emails triaged:    {stats['emails_triaged']}")
        print(f"  Drafts created:    {stats['drafts_created']}")
        print(f"  Auto-handled:      {stats['auto_handled']}")
        print(f"  Critical alerts:   {stats['critical_count']}")
        if stats["errors"]:
            print(f"  Errors: {len(stats['errors'])}")
            for e in stats["errors"][:5]:
                print(f"    - {e}")
        print(f"{'='*50}")

    elif command == "status":
        from .status import get_inbox_status

        status = await get_inbox_status()
        print(status)

    else:
        print("Usage: python -m email_agent [run|status]")
        sys.exit(1)


if __name__ == "__main__":
    asyncio.run(main())

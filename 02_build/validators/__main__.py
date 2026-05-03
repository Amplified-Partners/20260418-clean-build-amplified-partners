"""Entrypoint so ``python -m validators ...`` resolves the CLI.

Signed-by: Devon-ab74 (devin-ab740f2c78ee477a9c16ea3b6ed15293) - 2026-05-03
"""

from .cli import main

if __name__ == "__main__":  # pragma: no cover
    raise SystemExit(main())

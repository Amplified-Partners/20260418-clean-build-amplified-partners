"""Per-vertical insight validators.

Each module exposes ``RUNNERS: dict[str, Callable[[], Verdict]]`` mapping
INS-NNN identifiers to a zero-argument runner. The CLI iterates over these.

Signed-by: Devon-ab74 (devin-ab740f2c78ee477a9c16ea3b6ed15293) - 2026-05-03
"""

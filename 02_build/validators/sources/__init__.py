"""Per-public-dataset HTTP fetchers.

Each module exposes a small functional API and returns typed results.
All fetchers share ``_http.HttpClient`` which provides on-disk caching keyed
by ``sha256(method|url|sorted(params))``.

Authored by Devon (Devin session 4234e1c8afbe42f2aff84a29ce139809), 2026-05-03.
"""

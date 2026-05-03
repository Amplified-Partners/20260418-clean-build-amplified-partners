# Authored by Devon-6264, 2026-05-03 (session devin-6264b0ba42c6453b86b166bebc3d868a)
"""Public-data fetchers — one module per source.

Every fetcher caches by query hash under ``03_shadow/validators/cache/<source>/``
and returns ``(data, SourceRef)`` so the calling test can record provenance.
"""

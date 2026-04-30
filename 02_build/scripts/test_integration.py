#!/usr/bin/env python3
"""Test SearXNG integration."""

import sys
sys.path.insert(0, '/Users/ewansair/amplified')

import requests
print(f"requests version: {requests.__version__}")

from search_research_pipe import _search_searxng
from config_research_pipe import get_config

config = get_config()
print(f"SearXNG endpoint: {config.SEARXNG_ENDPOINT}")

print("Testing search...")
results = _search_searxng('AI automation small business', config, limit=5)
print(f"Results: {len(results)}")

for r in results[:3]:
    print(f"  - {r['title'][:50]}...")
    print(f"    Source engines: {r.get('engines', [])}")

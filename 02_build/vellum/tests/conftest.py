"""Pytest config — async mode auto for Vellum tests."""

import inspect

import pytest


def pytest_collection_modifyitems(items):
    for item in items:
        if item.get_closest_marker("asyncio") is None:
            if inspect.iscoroutinefunction(item.obj):
                item.add_marker(pytest.mark.asyncio)

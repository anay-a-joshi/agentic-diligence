"""Caches expensive analyses to avoid burning API credits during dev."""
from typing import Any


_memory_cache: dict[str, Any] = {}


async def get_cached(key: str) -> Any | None:
    return _memory_cache.get(key)


async def set_cached(key: str, value: Any) -> None:
    _memory_cache[key] = value

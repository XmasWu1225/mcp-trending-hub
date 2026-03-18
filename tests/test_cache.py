"""缓存工具测试"""

import time

import pytest

from daily_hot_mcp.utils.cache import SimpleCache


class TestSimpleCache:
    """缓存测试类"""

    def test_cache_set_and_get(self) -> None:
        """测试缓存设置和获取"""
        cache = SimpleCache(cache_duration_minutes=1)
        cache.set("test_key", {"data": "test_value"})

        result = cache.get("test_key")
        assert result == {"data": "test_value"}
        cache.delete("test_key")

    def test_cache_miss(self) -> None:
        """测试缓存未命中"""
        cache = SimpleCache(cache_duration_minutes=1)
        result = cache.get("nonexistent_key")
        assert result is None

    def test_cache_clear(self) -> None:
        """测试缓存清除"""
        cache = SimpleCache(cache_duration_minutes=1)
        cache.set("key1", "value1")
        cache.set("key2", "value2")

        cache.clear()

        assert cache.get("key1") is None
        assert cache.get("key2") is None

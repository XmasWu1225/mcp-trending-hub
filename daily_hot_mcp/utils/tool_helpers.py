"""工具辅助函数"""

import asyncio
import functools
from typing import Any, Callable, Coroutine, Dict, List, Optional, TypeVar

from fastmcp.tools import Tool

from daily_hot_mcp.tooltypes import TrendingResult
from daily_hot_mcp.utils import cache
from daily_hot_mcp.utils.logger import logger

T = TypeVar("T")


def create_tool(
    func: Callable[..., Coroutine[Any, Any, TrendingResult]],
    name: str,
    description: str,
) -> Tool:
    """创建MCP工具的便捷函数"""
    return Tool.from_function(fn=func, name=name, description=description)


def with_cache(
    cache_key: str,
    ttl_minutes: Optional[int] = None,
) -> Callable[
    [Callable[..., Coroutine[Any, Any, T]]], Callable[..., Coroutine[Any, Any, T]]
]:
    """缓存装饰器"""

    def decorator(
        func: Callable[..., Coroutine[Any, Any, T]],
    ) -> Callable[..., Coroutine[Any, Any, T]]:
        @functools.wraps(func)
        async def wrapper(*args: Any, **kwargs: Any) -> T:
            full_key = cache_key
            if kwargs:
                key_suffix = "_".join(f"{k}={v}" for k, v in sorted(kwargs.items()))
                full_key = f"{cache_key}_{key_suffix}"

            cached = cache.get(full_key)
            if cached is not None:
                logger.info(f"从缓存获取数据: {full_key}")
                return cached

            result = await func(*args, **kwargs)
            cache.set(full_key, result)
            return result

        return wrapper

    return decorator


def run_tool_test(func: Callable[..., Coroutine[Any, Any, TrendingResult]]) -> None:
    """运行工具测试"""
    result = asyncio.run(func())
    print(f"结果是：{result}")


def make_main(
    func: Callable[..., Coroutine[Any, Any, TrendingResult]],
) -> Callable[[], None]:
    """创建测试main函数"""

    def main() -> None:
        run_tool_test(func)

    return main

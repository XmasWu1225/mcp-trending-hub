"""缓存工具模块"""

import json
import tempfile
from datetime import datetime, timedelta
from pathlib import Path
from typing import Any, Optional

from daily_hot_mcp.utils.config import config


class SimpleCache:
    """简单的文件缓存实现"""

    def __init__(self, cache_duration_minutes: Optional[int] = None) -> None:
        """初始化缓存"""
        cache_dir = config.cache.cache_dir
        if cache_dir:
            self._cache_dir = Path(cache_dir)
        else:
            self._cache_dir = Path(tempfile.gettempdir()) / "mcp_daily_news" / "cache"
        self._cache_dir.mkdir(parents=True, exist_ok=True)

        duration = cache_duration_minutes or config.cache.default_duration_minutes
        self._cache_duration = timedelta(minutes=duration)

    def _get_cache_file(self, key: str) -> Path:
        """获取缓存文件路径"""
        safe_key = "".join(c for c in key if c.isalnum() or c in "-_.")
        return self._cache_dir / f"{safe_key}.json"

    def get(self, key: str) -> Optional[Any]:
        """获取缓存数据，如果不存在或已过期则返回None"""
        cache_file = self._get_cache_file(key)

        if not cache_file.exists():
            return None

        try:
            with open(cache_file, "r", encoding="utf-8") as f:
                cache_data = json.load(f)

            cache_time = datetime.fromisoformat(cache_data["timestamp"])
            if datetime.now() - cache_time > self._cache_duration:
                cache_file.unlink()
                return None

            return cache_data["data"]
        except Exception:
            if cache_file.exists():
                cache_file.unlink()
            return None

    def set(self, key: str, data: Any) -> None:
        """设置缓存数据"""
        cache_file = self._get_cache_file(key)

        cache_data = {
            "timestamp": datetime.now().isoformat(),
            "data": data,
        }

        try:
            with open(cache_file, "w", encoding="utf-8") as f:
                json.dump(cache_data, f, ensure_ascii=False, indent=2)
        except Exception:
            pass

    def clear(self) -> None:
        """清除所有缓存"""
        try:
            for cache_file in self._cache_dir.glob("*.json"):
                cache_file.unlink()
        except Exception:
            pass

    def delete(self, key: str) -> None:
        """删除指定缓存"""
        cache_file = self._get_cache_file(key)
        try:
            if cache_file.exists():
                cache_file.unlink()
        except Exception:
            pass


cache = SimpleCache()

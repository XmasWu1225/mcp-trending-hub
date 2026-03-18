"""配置管理模块"""

import os
from typing import Optional

from dotenv import load_dotenv

from daily_hot_mcp.tooltypes import CacheConfig, HTTPConfig, ServerConfig

load_dotenv()


class Config:
    """应用配置类"""

    def __init__(self) -> None:
        self._server_config: Optional[ServerConfig] = None
        self._http_config: Optional[HTTPConfig] = None
        self._cache_config: Optional[CacheConfig] = None

    @property
    def server(self) -> ServerConfig:
        """获取服务器配置"""
        if self._server_config is None:
            self._server_config = ServerConfig(
                host=os.getenv("MCP_HOST", "0.0.0.0"),
                port=int(os.getenv("MCP_PORT", "8000")),
                path=os.getenv("MCP_PATH", "/mcp"),
                log_level=os.getenv("MCP_LOG_LEVEL", "INFO"),
            )
        return self._server_config

    @property
    def http(self) -> HTTPConfig:
        """获取HTTP配置"""
        if self._http_config is None:
            self._http_config = HTTPConfig(
                timeout=float(os.getenv("HTTP_TIMEOUT", "30.0")),
                follow_redirects=os.getenv("HTTP_FOLLOW_REDIRECTS", "true").lower()
                == "true",
            )
        return self._http_config

    @property
    def cache(self) -> CacheConfig:
        """获取缓存配置"""
        if self._cache_config is None:
            self._cache_config = CacheConfig(
                cache_dir=os.getenv("CACHE_DIR"),
                default_duration_minutes=int(os.getenv("CACHE_DURATION_MINUTES", "30")),
            )
        return self._cache_config

    @property
    def firecrawl_api_key(self) -> Optional[str]:
        """获取Firecrawl API密钥"""
        return os.getenv("FIRECRAWL_API_KEY")

    @property
    def custom_rss_url(self) -> Optional[str]:
        """获取自定义RSS URL"""
        return os.getenv("TRENDS_HUB_CUSTOM_RSS_URL")


config = Config()

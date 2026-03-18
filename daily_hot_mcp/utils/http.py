"""HTTP客户端模块"""

from typing import Any, Dict, Optional

import httpx

from daily_hot_mcp.tooltypes import UserAgents
from daily_hot_mcp.utils.config import config


class HttpClient:
    """HTTP客户端封装"""

    def __init__(self) -> None:
        http_config = config.http
        self._client = httpx.AsyncClient(
            headers={"User-Agent": UserAgents.CHROME_DESKTOP},
            timeout=http_config.timeout,
            follow_redirects=http_config.follow_redirects,
        )

    async def get(
        self,
        url: str,
        params: Optional[Dict[str, Any]] = None,
        headers: Optional[Dict[str, str]] = None,
        **kwargs: Any,
    ) -> httpx.Response:
        """发送GET请求"""
        return await self._client.get(url, params=params, headers=headers, **kwargs)

    async def post(
        self,
        url: str,
        data: Optional[Any] = None,
        json: Optional[Dict[str, Any]] = None,
        headers: Optional[Dict[str, str]] = None,
        **kwargs: Any,
    ) -> httpx.Response:
        """发送POST请求"""
        return await self._client.post(
            url, data=data, json=json, headers=headers, **kwargs
        )

    async def close(self) -> None:
        """关闭客户端"""
        await self._client.aclose()


http_client = HttpClient()

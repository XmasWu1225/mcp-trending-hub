"""HTTP客户端测试"""

import pytest

from daily_hot_mcp.utils.http import HttpClient


class TestHttpClient:
    """HTTP客户端测试类"""

    @pytest.mark.asyncio
    async def test_http_client_creation(self) -> None:
        """测试HTTP客户端创建"""
        client = HttpClient()
        assert client is not None
        assert client._client is not None
        await client.close()

    @pytest.mark.asyncio
    async def test_http_client_get(self) -> None:
        """测试GET请求"""
        client = HttpClient()
        try:
            response = await client.get("https://httpbin.org/get")
            assert response.status_code == 200
        finally:
            await client.close()

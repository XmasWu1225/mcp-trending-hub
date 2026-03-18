"""工具集成测试"""

import pytest

from daily_hot_mcp.tools.baidu import get_baidu_trending_func
from daily_hot_mcp.tools.weibo import get_weibo_trending_func
from daily_hot_mcp.tools.zhihu import get_zhihu_trending_func
from daily_hot_mcp.tooltypes import TrendingResult


class TestBaiduTool:
    """百度热榜测试类"""

    @pytest.mark.asyncio
    async def test_get_baidu_trending(self) -> None:
        """测试获取百度热榜"""
        result = await get_baidu_trending_func()

        assert isinstance(result, list)
        assert len(result) > 0

        if result:
            item = result[0]
            assert "title" in item
            assert isinstance(item["title"], str)


class TestWeiboTool:
    """微博热搜测试类"""

    @pytest.mark.asyncio
    async def test_get_weibo_trending(self) -> None:
        """测试获取微博热搜"""
        try:
            result = await get_weibo_trending_func()

            assert isinstance(result, list)

            if result:
                item = result[0]
                assert "title" in item
                assert "link" in item
        except Exception as e:
            pytest.skip(f"微博接口暂时不可用: {str(e)}")


class TestZhihuTool:
    """知乎热榜测试类"""

    @pytest.mark.asyncio
    async def test_get_zhihu_trending(self) -> None:
        """测试获取知乎热榜"""
        result = await get_zhihu_trending_func()

        assert isinstance(result, list)

        if result:
            item = result[0]
            assert "title" in item

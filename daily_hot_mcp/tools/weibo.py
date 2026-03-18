"""微博热搜工具"""

import asyncio
from typing import Annotated
from urllib.parse import quote

from fastmcp.tools import Tool
from pydantic import Field

from daily_hot_mcp.tooltypes import TrendingResult
from daily_hot_mcp.utils import http_client
from daily_hot_mcp.utils.logger import logger

USER_AGENT = (
    "Mozilla/5.0 (Windows NT 10.0; Win64; x64) "
    "AppleWebKit/537.36 (KHTML, like Gecko) "
    "Chrome/122.0.0.0 Safari/537.36"
)


async def get_weibo_trending_func() -> TrendingResult:
    """获取微博热搜榜数据"""

    headers = {
        "User-Agent": USER_AGENT,
        "Referer": "https://weibo.com/hot/search",
        "Accept": "application/json, text/plain, */*",
        "Accept-Language": "zh-CN,zh;q=0.9,en;q=0.8",
    }

    url = "https://weibo.com/ajax/side/hotSearch"
    response = await http_client.get(url, headers=headers)

    if response.status_code == 403:
        raise Exception("微博接口返回403：IP可能已被暂时封禁，请稍后重试")

    response.raise_for_status()
    data = response.json()

    if data.get("ok") != 1:
        raise Exception("获取微博热搜榜失败")

    results: TrendingResult = []
    for item in data.get("data", {}).get("realtime", []):
        if item.get("is_ad") == 1:
            continue

        word = item.get("word", "")
        num = item.get("num", "")

        link = f"https://s.weibo.com/weibo?q={quote(word)}&Refer=top"

        results.append(
            {
                "title": word,
                "description": item.get("note") or word,
                "popularity": f"{num} 火力值" if num else "热搜中",
                "link": link,
            }
        )

    return results


weibo_tool_config = Tool.from_function(
    fn=get_weibo_trending_func,
    name="get-weibo-trending",
    description="获取微博热搜榜，包含时事热点、社会现象、娱乐新闻、明星动态及网络热议话题的实时热门中文资讯",
)

weibo_hot_tools = [weibo_tool_config]


def main() -> None:
    result = asyncio.run(get_weibo_trending_func())
    print(f"结果是：{result}")


if __name__ == "__main__":
    main()

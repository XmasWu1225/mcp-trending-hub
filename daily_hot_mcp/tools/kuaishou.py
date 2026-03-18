"""快手热搜工具"""

import asyncio
import json
import random
import string
import time
from typing import Annotated, Any, Dict, List

from fastmcp.tools import Tool
from pydantic import Field

from daily_hot_mcp.tooltypes import TrendingResult
from daily_hot_mcp.utils import http_client

USER_AGENT = (
    "Mozilla/5.0 (Windows NT 10.0; Win64; x64) "
    "AppleWebKit/537.36 (KHTML, like Gecko) "
    "Chrome/122.0.0.0 Safari/537.36"
)


def generate_did() -> str:
    """生成随机设备ID"""
    chars = string.ascii_lowercase + string.digits
    return "web_" + "".join(random.choice(chars) for _ in range(32))


async def get_kuaishou_trending_func() -> TrendingResult:
    """获取快手热榜数据"""

    did = generate_did()
    timestamp = int(time.time() * 1000)

    headers = {
        "User-Agent": USER_AGENT,
        "Referer": "https://www.kuaishou.com/brilliant",
        "Content-Type": "application/json",
        "Cookie": f"did={did}; didv={timestamp};",
        "Origin": "https://www.kuaishou.com",
        "Accept": "*/*",
    }

    payload = {
        "operationName": "visionHotRank",
        "variables": {"page": "brilliant"},
        "extensions": {
            "persistedQuery": {
                "version": 1,
                "sha256Hash": "70d912cc24d081f9a1f5926c9f65d6c547806f37648f5e93345e6912388c3a50",
            }
        },
    }

    try:
        response = await http_client.post(
            "https://www.kuaishou.com/graphql",
            json=payload,
            headers=headers,
        )

        data = response.json()
        items = data.get("data", {}).get("visionHotRank", {}).get("items", [])

        if not items:
            payload["operationName"] = "visionSearchPhoto"
            payload["variables"] = {"keyword": "", "pcursor": "", "page": "search"}
            payload["extensions"]["persistedQuery"][
                "sha256Hash"
            ] = "6c52c9d031dcea45c5b810deedebe91d7ea16a1b30d3999aef0ebc4b3ea9e25c"

            response = await http_client.post(
                "https://www.kuaishou.com/graphql",
                json=payload,
                headers=headers,
            )
            data = response.json()
            feeds = data.get("data", {}).get("visionSearchPhoto", {}).get("feeds", [])
            items = [f.get("photo", {}) for f in feeds if f.get("photo")]

        if not items:
            raise Exception("快手热榜数据获取失败")

        results: TrendingResult = []
        for idx, item in enumerate(items[:30], 1):
            title = (
                item.get("name")
                or item.get("word")
                or item.get("caption")
                or "快手视频"
            )
            hot_value = item.get("hotValue") or item.get("viewCount") or "热门"
            photo_id = item.get("photoId") or item.get("id") or ""

            results.append(
                {
                    "rank": idx,
                    "title": title[:50],
                    "popularity": str(hot_value),
                    "link": (
                        f"https://www.kuaishou.com/short-video/{photo_id}"
                        if photo_id
                        else "https://www.kuaishou.com/brilliant"
                    ),
                }
            )

        return results

    except Exception as e:
        raise Exception(f"快手热榜获取失败: {str(e)}")


kuaishou_tool_config = Tool.from_function(
    fn=get_kuaishou_trending_func,
    name="get-kuaishou-trending",
    description="获取快手热榜，包含实时热门短视频话题和流行内容",
)

kuaishou_hot_tools = [kuaishou_tool_config]


def main() -> None:
    result = asyncio.run(get_kuaishou_trending_func())
    print(f"结果是：{result}")


if __name__ == "__main__":
    main()

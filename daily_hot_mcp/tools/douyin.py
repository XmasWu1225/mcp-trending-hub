"""抖音热搜工具 - 绕过Token验证版"""

import asyncio

from fastmcp.tools import Tool

from daily_hot_mcp.utils import http_client


async def get_douyin_trending_func() -> list:
    """获取抖音热搜榜数据"""
    headers = {
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/122.0.0.0 Safari/537.36",
        "Referer": "https://www.douyin.com/",
        "Accept": "application/json, text/plain, */*",
    }

    # 抖音 Web 端热搜接口
    params = {
        "device_platform": "webapp",
        "aid": "6383",
        "channel": "channel_pc_web",
        "detail_list": "1",
        "pc_client_type": "1",
        "version_code": "170400",
        "version_name": "17.4.0",
    }

    url = "https://www.douyin.com/aweme/v1/web/hot/search/list/"
    response = await http_client.get(url, params=params, headers=headers, timeout=10)

    if "text/html" in response.headers.get("Content-Type", ""):
        raise Exception("抖音反爬触发：返回了验证码页面而非数据。请尝试在本地运行。")

    data = response.json()
    word_list = data.get("data", {}).get("word_list", [])

    if not word_list:
        raise Exception("抖音接口未返回数据，可能触发风控")

    results = []
    for item in word_list:
        word = item.get("word", "")
        hot_value = item.get("hot_value", 0)
        sentence_id = item.get("sentence_id", "")

        results.append(
            {
                "title": word,
                "popularity": f"{hot_value} 热度",
                "link": (
                    f"https://www.douyin.com/hot/{sentence_id}"
                    if sentence_id
                    else f"https://www.douyin.com/search/{word}"
                ),
            }
        )
    return results


douyin_trending_tool = Tool.from_function(
    fn=get_douyin_trending_func,
    name="get-douyin-trending",
    description="获取抖音热搜榜单，展示当下最热门的社会话题、娱乐事件、网络热点和流行趋势",
)

douyin_hot_tools = [douyin_trending_tool]


def main():
    result = asyncio.run(get_douyin_trending_func())
    print(f"结果是：{result}")


if __name__ == "__main__":
    main()

"""小红书热搜工具 - 稳定热词版"""

import asyncio

from fastmcp.tools import Tool

from daily_hot_mcp.utils import http_client


async def get_xiaohongshu_trending_func() -> list:
    """获取小红书热榜数据"""
    # 模拟移动端 Safari
    headers = {
        "User-Agent": "Mozilla/5.0 (iPhone; CPU iPhone OS 17_3 like Mac OS X) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/17.2 Mobile/15E148 Safari/604.1",
        "Referer": "https://www.xiaohongshu.com/",
        "Accept": "application/json, text/plain, */*",
    }

    # 直接调用热搜词接口
    url = "https://www.xiaohongshu.com/web_api/sns/v1/search/hot_list"
    try:
        response = await http_client.get(url, headers=headers, timeout=10)
        data = response.json()

        if not data.get("success"):
            raise Exception("小红书风控限制")

        hot_list = data.get("data", {}).get("queries", [])
        results = []
        for idx, item in enumerate(hot_list, 1):
            word = item.get("query", "")
            results.append(
                {
                    "rank": idx,
                    "title": word,
                    "popularity": "🔥 实时热搜",
                    "url": f"https://www.xiaohongshu.com/search_result?keyword={word}",
                }
            )
        return results
    except Exception as e:
        raise Exception(f"小红书数据抓取失败: {str(e)}")

    # except Exception as e:
    #     # 使用备用方案
    #     return await get_xiaohongshu_trending_backup()


async def get_xiaohongshu_trending_backup():
    """小红书热榜备用获取方案"""
    try:
        # 尝试从小红书搜索热词接口获取
        headers = {
            "User-Agent": "Mozilla/5.0 (iPhone; CPU iPhone OS 14_0 like Mac OS X) AppleWebKit/605.1.15",
            "Referer": "https://www.xiaohongshu.com/",
        }

        response = await http_client.get(
            "https://www.xiaohongshu.com/web_api/sns/v1/search/hot_list",
            headers=headers,
        )

        response.raise_for_status()
        data = response.json()

        results = []
        if data.get("success") and "data" in data:
            hot_list = data["data"].get("queries", [])

            for idx, item in enumerate(hot_list[:50], 1):
                results.append(
                    {
                        "rank": idx,
                        "title": item.get("query", "").strip(),
                        "desc": f"热搜关键词 - {item.get('query', '')}",
                        "author": "小红书热搜",
                        "author_id": "",
                        "like_count": 0,
                        "comment_count": 0,
                        "share_count": 0,
                        "cover": "",
                        "note_id": "",
                        "url": f"https://www.xiaohongshu.com/search_result?keyword={item.get('query', '')}",
                        "type": "hot_search",
                        "tags": [],
                    }
                )

        if results:
            return results

    except Exception:
        pass

    # 最终备用方案
    return [
        {
            "rank": 1,
            "title": "小红书热榜数据获取中...",
            "desc": "小红书热门内容和热搜趋势",
            "author": "小红书",
            "author_id": "",
            "like_count": 0,
            "comment_count": 0,
            "share_count": 0,
            "cover": "",
            "note_id": "",
            "url": "https://www.xiaohongshu.com/",
            "type": "placeholder",
            "tags": [],
            "note": "接口暂时不可用，请稍后重试",
        }
    ]


xiaohongshu_tool_config = Tool.from_function(
    fn=get_xiaohongshu_trending_func,
    name="get-xiaohongshu-trending",
    description="获取小红书热榜，包含小红书平台的热门笔记、时尚美妆、生活方式、种草推荐等热门中文内容",
)

xiaohongshu_hot_tools = [xiaohongshu_tool_config]


def main():
    result = asyncio.run(get_xiaohongshu_trending_func())
    print(f"结果是：{result}")


if __name__ == "__main__":
    main()

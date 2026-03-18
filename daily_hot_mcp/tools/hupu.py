"""虎扑热榜工具"""

import asyncio
from typing import Any, Dict, List

from bs4 import BeautifulSoup
from fastmcp.tools import Tool

from daily_hot_mcp.tooltypes import TrendingResult
from daily_hot_mcp.utils import http_client
from daily_hot_mcp.utils.logger import logger

USER_AGENT = (
    "Mozilla/5.0 (Windows NT 10.0; Win64; x64) "
    "AppleWebKit/537.36 (KHTML, like Gecko) "
    "Chrome/91.0.4472.124 Safari/537.36"
)


async def get_hupu_trending_func() -> TrendingResult:
    """获取虎扑热榜数据"""
    headers = {
        "User-Agent": USER_AGENT,
        "Referer": "https://www.hupu.com/",
        "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8",
        "Accept-Language": "zh-CN,zh;q=0.9",
    }

    try:
        response = await http_client.get("https://bbs.hupu.com/bxj", headers=headers)
        response.raise_for_status()
        soup = BeautifulSoup(response.text, "html.parser")
        results: TrendingResult = []

        thread_list = soup.find_all(
            ["tr", "li", "div"],
            class_=lambda x: x
            and any(
                keyword in x.lower() for keyword in ["thread", "post", "topic", "item"]
            ),
        )

        if not thread_list:
            return await _get_hupu_trending_homepage()

        rank = 1
        for item in thread_list:
            title_elem = item.find("a", href=True)
            if not title_elem:
                title_elem = item.find(
                    ["span", "div"], string=lambda text: text and len(text.strip()) > 5
                )

            if title_elem:
                title = title_elem.get_text(strip=True)
                if (
                    title
                    and len(title) > 5
                    and not any(skip in title for skip in ["登录", "注册", "首页"])
                ):
                    url = title_elem.get("href", "") if title_elem.name == "a" else ""
                    if url and not url.startswith("http"):
                        url = f"https://bbs.hupu.com{url}"

                    reply_elem = item.find(
                        string=lambda text: text
                        and any(char in text for char in ["回复", "浏览", "万", "热度"])
                    )
                    reply_count = reply_elem.strip() if reply_elem else ""

                    results.append(
                        {
                            "rank": rank,
                            "title": title,
                            "description": f"虎扑步行街热帖 - {title}",
                            "link": url or f"https://www.hupu.com/search?q={title}",
                            "popularity": reply_count,
                        }
                    )
                    rank += 1
                    if rank > 50:
                        break

        if results:
            return results[:50]
        else:
            return await _get_hupu_trending_homepage()

    except Exception as e:
        logger.error(f"获取虎扑热榜失败: {str(e)}")
        return await _get_hupu_trending_homepage()


async def _get_hupu_trending_homepage() -> TrendingResult:
    """从虎扑首页获取热门内容"""
    headers = {
        "User-Agent": USER_AGENT,
        "Referer": "https://www.hupu.com/",
    }

    try:
        response = await http_client.get("https://www.hupu.com/", headers=headers)
        response.raise_for_status()
        soup = BeautifulSoup(response.text, "html.parser")
        results: TrendingResult = []

        hot_items = soup.find_all(["a", "div"], href=True) + soup.find_all(
            ["div", "span"], class_=lambda x: x and "hot" in x.lower()
        )

        rank = 1
        for item in hot_items:
            if item.name == "a":
                title = item.get_text(strip=True)
                url = item.get("href", "")
            else:
                link_elem = item.find("a", href=True)
                if link_elem:
                    title = link_elem.get_text(strip=True)
                    url = link_elem.get("href", "")
                else:
                    title = item.get_text(strip=True)
                    url = ""

            if (
                title
                and len(title) > 5
                and not any(skip in title for skip in ["登录", "注册", "首页", "下载"])
            ):
                if url and not url.startswith("http"):
                    url = f"https://www.hupu.com{url}"

                results.append(
                    {
                        "rank": rank,
                        "title": title,
                        "description": f"虎扑热门内容 - {title}",
                        "link": url or f"https://www.hupu.com/search?q={title}",
                    }
                )
                rank += 1
                if rank > 50:
                    break

        if results:
            return results[:50]

    except Exception as e:
        logger.error(f"获取虎扑首页失败: {str(e)}")

    return [
        {
            "rank": 1,
            "title": "虎扑热榜数据获取失败",
            "description": "接口暂时不可用，请稍后重试",
            "link": "https://www.hupu.com/",
        }
    ]


hupu_trending_tool = Tool.from_function(
    fn=get_hupu_trending_func,
    name="get-hupu-trending",
    description="获取虎扑热榜，包含虎扑体育赛事、步行街热帖、篮球足球话题及男性生活兴趣的热门中文讨论内容",
)

hupu_hot_tools = [hupu_trending_tool]


def main() -> None:
    result = asyncio.run(get_hupu_trending_func())
    print(f"结果是：{result}")


if __name__ == "__main__":
    main()

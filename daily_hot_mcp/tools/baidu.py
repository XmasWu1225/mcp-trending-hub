"""百度热榜工具"""

import asyncio
from typing import Optional

from bs4 import BeautifulSoup
from fastmcp.tools import Tool

from daily_hot_mcp.tooltypes import TrendingResult
from daily_hot_mcp.utils import http_client


def _normalize_link(link: Optional[str]) -> str:
    """标准化链接"""
    if not link:
        return ""
    link_str = str(link)
    if link_str.startswith("http"):
        return link_str
    return "https://www.baidu.com" + link_str


async def get_baidu_trending_func() -> TrendingResult:
    """获取百度热榜数据"""

    response = await http_client.get(
        "https://top.baidu.com/board",
        params={"tab": "realtime"},
    )
    response.raise_for_status()

    soup = BeautifulSoup(response.text, "html.parser")

    results: TrendingResult = []
    hot_items = soup.find_all("div", class_="category-wrap_iQLoo")

    if not hot_items:
        raise Exception("获取百度热榜失败")

    for idx, item in enumerate(hot_items, 1):
        title_elem = item.find("div", class_="c-single-text-ellipsis")
        title = title_elem.text.strip() if title_elem else ""

        index_elem = item.find("div", class_="hot-index_1Bl1a")
        hot_index = index_elem.text.strip() if index_elem else ""

        desc_elem = item.find("div", class_="hot-desc_1m_jR")
        description = desc_elem.text.strip() if desc_elem else ""

        link_elem = item.find("a")
        href = link_elem.get("href", "") if link_elem else ""
        link = _normalize_link(str(href) if href else None)

        img_elem = item.find("img")
        cover = img_elem.get("src", "") if img_elem else ""

        if title:
            results.append(
                {
                    "title": title,
                    "description": description,
                    "popularity": hot_index,
                    "link": link,
                    "cover": cover,
                    "rank": idx,
                }
            )

    return results


baidu_tool_config = Tool.from_function(
    fn=get_baidu_trending_func,
    name="get-baidu-trending",
    description="获取百度热榜，包含实时热搜、社会热点、科技新闻、娱乐八卦等多领域的热门中文资讯和搜索趋势",
)

baidu_hot_tools = [baidu_tool_config]


def main() -> None:
    result = asyncio.run(get_baidu_trending_func())
    print(f"结果是：{result}")


if __name__ == "__main__":
    main()

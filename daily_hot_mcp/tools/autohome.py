"""汽车之家热榜工具"""

import asyncio
from typing import Any, Dict, Optional
from urllib.parse import quote

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


def _normalize_link(link: Optional[str]) -> str:
    """标准化链接"""
    if not link:
        return ""
    if link.startswith("http"):
        return link
    if link.startswith("//"):
        return "https:" + link
    if link.startswith("/"):
        return "https://www.autohome.com.cn" + link
    return "https://www.autohome.com.cn/" + link


def _get_category(link: str) -> str:
    """根据链接判断分类"""
    if "/news/" in link:
        return "汽车新闻"
    elif "/advice/" in link:
        return "购车指南"
    elif "/drive/" in link:
        return "试驾体验"
    elif "/dealer/" in link:
        return "经销商"
    return "汽车资讯"


async def get_autohome_trending_func() -> TrendingResult:
    """获取汽车之家热榜数据"""
    headers = {
        "User-Agent": USER_AGENT,
        "Referer": "https://www.autohome.com.cn/",
        "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8",
        "Accept-Language": "zh-CN,zh;q=0.9",
    }

    try:
        response = await http_client.get(
            "https://www.autohome.com.cn/",
            headers=headers,
        )

        response.raise_for_status()
        soup = BeautifulSoup(response.text, "html.parser")

        results: TrendingResult = []

        news_items = (
            soup.select(".list-article li a")
            + soup.select(".hot-news li a")
            + soup.select(".news-list li a")
            + soup.select("a[href*='/news/']")
            + soup.select("a[href*='/advice/']")
            + soup.select("a[href*='/drive/']")
        )

        rank = 1
        seen_titles: set[str] = set()

        for item in news_items:
            try:
                title = item.get_text(strip=True)
                if not title or len(title) < 5 or title in seen_titles:
                    continue

                if any(
                    skip in title
                    for skip in ["登录", "注册", "首页", "下载", "更多", "论坛", "导航"]
                ):
                    continue

                seen_titles.add(title)

                link = _normalize_link(item.get("href", ""))

                desc = ""
                parent = item.parent
                if parent:
                    desc_elem = (
                        parent.find("p")
                        or parent.find("div", class_="summary")
                        or parent.find("span", class_="desc")
                        or parent.find("div", class_="content")
                    )
                    if desc_elem:
                        desc = desc_elem.get_text(strip=True)[:200]

                if not desc:
                    desc = f"汽车之家资讯 - {title}"

                results.append(
                    {
                        "rank": rank,
                        "title": title,
                        "description": desc,
                        "link": link
                        or f"https://www.autohome.com.cn/search?q={quote(title)}",
                        "popularity": "",
                    }
                )
                rank += 1

                if rank > 50:
                    break

            except Exception:
                continue

        if not results:
            return await _get_autohome_api_data(headers)

        return results[:50]

    except Exception as e:
        logger.error(f"获取汽车之家热榜失败: {str(e)}")
        return await _get_autohome_api_data(headers)


async def _get_autohome_api_data(headers: Dict[str, str]) -> TrendingResult:
    """从API获取汽车之家数据"""
    try:
        response = await http_client.get(
            "https://www.autohome.com.cn/ashx/AjaxIndexInfo.ashx?type=5",
            headers=headers,
        )

        if response.status_code == 200:
            data = response.json()
            if "result" in data and data["result"]:
                results: TrendingResult = []
                for idx, item in enumerate(data["result"][:30], 1):
                    results.append(
                        {
                            "rank": idx,
                            "title": item.get("title", "").strip(),
                            "description": item.get(
                                "summary", f"汽车之家资讯 - {item.get('title', '')}"
                            ),
                            "link": item.get("url", ""),
                            "popularity": str(item.get("replycount", "")),
                        }
                    )
                return results
    except Exception as e:
        logger.error(f"获取汽车之家API数据失败: {str(e)}")

    return [
        {
            "rank": 1,
            "title": "汽车之家热榜数据获取失败",
            "description": "接口暂时不可用，请稍后重试",
            "link": "https://www.autohome.com.cn/",
            "popularity": "",
        }
    ]


autohome_tool_config = Tool.from_function(
    fn=get_autohome_trending_func,
    name="get-autohome-trending",
    description="获取汽车之家热榜，包含汽车新闻、新车发布、购车指南、试驾体验、汽车评测及汽车行业动态的专业汽车资讯",
)

autohome_hot_tools = [autohome_tool_config]


def main() -> None:
    result = asyncio.run(get_autohome_trending_func())
    print(f"结果是：{result}")


if __name__ == "__main__":
    main()

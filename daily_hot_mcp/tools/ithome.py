"""
IT之家热榜采集工具
获取IT之家的科技新闻热榜，包含科技资讯、数码产品、互联网动态等内容
"""

import asyncio

from bs4 import BeautifulSoup
from fastmcp.tools import Tool

from daily_hot_mcp.utils import http_client


async def get_ithome_trending_func() -> list:
    """获取IT之家热榜数据"""
    # 模拟真实浏览器 Headers，增加 Referer 降低风控风险
    headers = {
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/122.0.0.0 Safari/537.36",
        "Referer": "https://www.ithome.com/",
        "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,image/apng,*/*;q=0.8",
        "Accept-Language": "zh-CN,zh;q=0.9,en;q=0.8",
    }

    try:
        url = "https://www.ithome.com/"
        response = await http_client.get(url, headers=headers, timeout=10)

        # 强制设置编码，防止中文乱码
        response.encoding = "utf-8"
        response.raise_for_status()

        soup = BeautifulSoup(response.text, "html.parser")
        results = []
        seen_titles = set()

        # IT之家首页有多个排行版位，我们尝试组合多个选择器以防页面改版
        # 1. 右侧热榜 2. 首页焦点 3. 列表新闻
        news_items = (
            soup.select(".hot-list li a")
            + soup.select("#p-rank li a")
            + soup.select(".rank-name")  # 部分旧版选择器
        )

        rank = 1
        for item in news_items:
            try:
                # 提取标题
                title = item.get_text(strip=True)

                # 基础过滤：标题太短或者是导航类文字则跳过
                if not title or len(title) < 5 or title in seen_titles:
                    continue
                if any(
                    skip in title for skip in ["登录", "注册", "首页", "更多", "下载"]
                ):
                    continue

                seen_titles.add(title)

                # 提取链接
                link = item.get("href", "")
                if link and not link.startswith("http"):
                    link = "https://www.ithome.com" + link

                # 尝试寻找父级或同级元素中的热度/评论数
                hot_count = "IT资讯"
                parent = item.parent
                if parent:
                    # IT之家常见的热度标识类名
                    hot_elem = parent.find(class_=["comment", "hot", "view", "num"])
                    if hot_elem:
                        hot_count = hot_elem.get_text(strip=True)

                results.append(
                    {
                        "rank": rank,
                        "title": title,
                        "link": link or f"https://www.ithome.com/search?q={title}",
                        "popularity": hot_count,
                        "source": "IT之家",
                    }
                )

                rank += 1
                if rank > 30:  # 仅取前30条
                    break

            except Exception:
                continue

        # 如果解析失败，返回基础信息引导用户去首页
        if not results:
            return [
                {
                    "rank": 1,
                    "title": "IT之家热榜解析暂时失效，请点击访问首页",
                    "link": "https://www.ithome.com/",
                    "popularity": "N/A",
                }
            ]

        return results

    except Exception as e:
        # 这里的报错会被 web_app.py 捕获并显示在“调试日志”中
        raise Exception(f"IT之家数据获取失败: {str(e)}")


# 注册 Tool 配置
ithome_trending_tool = Tool.from_function(
    fn=get_ithome_trending_func,
    name="get-ithome-trending",
    description="获取IT之家热榜，包含最新的科技资讯、智能手机数码评测及互联网前沿动态",
)

ithome_hot_tools = [ithome_trending_tool]


# 测试函数
async def main():
    try:
        result = await get_ithome_trending_func()
        for item in result:
            print(f"{item['rank']}. {item['title']} ({item['popularity']})")
    except Exception as e:
        print(f"错误: {e}")


if __name__ == "__main__":
    asyncio.run(main())

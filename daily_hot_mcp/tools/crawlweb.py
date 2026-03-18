"""网站爬取工具"""

import asyncio
from typing import Annotated

from fastmcp.tools import Tool
from pydantic import Field

from daily_hot_mcp.tooltypes import TrendingResult
from daily_hot_mcp.utils.config import config
from daily_hot_mcp.utils.exceptions import APIKeyMissingError
from daily_hot_mcp.utils.logger import logger

_firecrawl_app = None


def _get_firecrawl_app():
    """获取Firecrawl应用实例（延迟加载）"""
    global _firecrawl_app
    if _firecrawl_app is None:
        api_key = config.firecrawl_api_key
        if not api_key:
            raise APIKeyMissingError("FIRECRAWL_API_KEY")

        from firecrawl import FirecrawlApp

        _firecrawl_app = FirecrawlApp(api_key=api_key)
    return _firecrawl_app


async def crawl_website_func(
    url: Annotated[str, Field(description="需要爬取的网站URL")],
) -> str:
    """爬取网站内容，返回Markdown格式"""
    try:
        app = _get_firecrawl_app()

        loop = asyncio.get_event_loop()
        scrape_result = await loop.run_in_executor(
            None,
            lambda: app.scrape_url(url, formats=["markdown"]),
        )

        if scrape_result.metadata.get("statusCode") == 200:
            return scrape_result.markdown or ""
        else:
            status = scrape_result.metadata.get("statusCode", "unknown")
            return f"爬取网站内容失败: HTTP {status}"

    except APIKeyMissingError:
        raise
    except Exception as e:
        logger.error(f"爬取网站失败: {str(e)}")
        return f"爬取网站失败: {str(e)}"


crawl_website_tool = Tool.from_function(
    fn=crawl_website_func,
    name="crawl-website",
    description="爬取网站内容，多用于用户想要详细了解某网站内容时使用",
)

crawl_website_hot_tools = [crawl_website_tool]


def main() -> None:
    result = asyncio.run(crawl_website_func(url="https://www.baidu.com"))
    print(result)


if __name__ == "__main__":
    main()

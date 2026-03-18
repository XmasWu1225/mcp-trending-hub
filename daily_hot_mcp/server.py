from fastmcp import FastMCP

from daily_hot_mcp.tools import all_tools
from daily_hot_mcp.utils.config import config
from daily_hot_mcp.utils.logger import logger

server = FastMCP(name="daily-hot-mcp")

for tool in all_tools:
    server.add_tool(tool)
    logger.info(f"Registered tool: {tool.name}")


def run_http() -> None:
    """运行HTTP模式服务器"""
    server_config = config.server
    try:
        logger.info(
            f"Starting Daily Hot MCP server with HTTP transport "
            f"(http://{server_config.host}:{server_config.port}{server_config.path})"
        )
        server.run(
            transport="http",
            host=server_config.host,
            port=server_config.port,
            path=server_config.path,
            log_level=server_config.log_level,
        )
    except KeyboardInterrupt:
        logger.info("Server stopped by user")


def main() -> None:
    run_http()


if __name__ == "__main__":
    main()

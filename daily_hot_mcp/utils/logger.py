"""日志工具模块"""

import logging
from typing import Any, Optional


class Logger:
    """自定义日志器"""

    def __init__(self, name: Optional[str] = None) -> None:
        self._logger = logging.getLogger("mcp_daily_news")
        if not self._logger.handlers:
            handler = logging.StreamHandler()
            formatter = logging.Formatter(
                "%(asctime)s - %(name)s - %(levelname)s - %(message)s"
            )
            handler.setFormatter(formatter)
            self._logger.addHandler(handler)
            self._logger.setLevel(logging.INFO)

        self._mcp_server: Optional[Any] = None

    def set_mcp_server(self, server: Any) -> None:
        """设置MCP服务器实例"""
        self._mcp_server = server

    def _log_to_mcp(self, level: str, message: str) -> None:
        """发送日志到MCP服务器"""
        if self._mcp_server:
            try:
                if hasattr(self._mcp_server, "log"):
                    self._mcp_server.log(level, message)
            except Exception:
                pass

    def info(self, message: str) -> None:
        """记录信息日志"""
        self._logger.info(message)
        self._log_to_mcp("info", message)

    def error(self, message: str) -> None:
        """记录错误日志"""
        self._logger.error(message)
        self._log_to_mcp("error", message)

    def warning(self, message: str) -> None:
        """记录警告日志"""
        self._logger.warning(message)
        self._log_to_mcp("warning", message)

    def debug(self, message: str) -> None:
        """记录调试日志"""
        self._logger.debug(message)

    def set_level(self, level: str) -> None:
        """设置日志级别"""
        level_map = {
            "DEBUG": logging.DEBUG,
            "INFO": logging.INFO,
            "WARNING": logging.WARNING,
            "ERROR": logging.ERROR,
        }
        self._logger.setLevel(level_map.get(level.upper(), logging.INFO))


logger = Logger()

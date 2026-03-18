"""统一异常处理模块"""


class BaseToolError(Exception):
    """工具基础异常"""

    def __init__(self, source: str, message: str) -> None:
        self.source = source
        self.message = message
        super().__init__(f"[{source}] {message}")


class DataFetchError(BaseToolError):
    """数据获取失败异常"""

    def __init__(self, source: str, message: str = "数据获取失败") -> None:
        super().__init__(source, message)


class InvalidParameterError(BaseToolError):
    """无效参数异常"""

    def __init__(self, source: str, message: str) -> None:
        super().__init__(source, message)


class ConfigError(BaseToolError):
    """配置错误异常"""

    def __init__(self, source: str, message: str) -> None:
        super().__init__(source, message)


class APIKeyMissingError(ConfigError):
    """API密钥缺失异常"""

    def __init__(self, key_name: str) -> None:
        super().__init__(source="config", message=f"{key_name} 未配置，请检查.env文件")


def raise_data_fetch_error(source: str, detail: str = "") -> None:
    """抛出数据获取错误"""
    message = f"获取{source}热榜失败"
    if detail:
        message += f": {detail}"
    raise DataFetchError(source, message)


def raise_invalid_parameter(source: str, param_name: str, valid_values: list) -> None:
    """抛出无效参数错误"""
    raise InvalidParameterError(source, f"不支持的{param_name}: {valid_values}")

# AGENTS.md

AI代理开发指南 - Daily Hot MCP 项目

## 项目概述

基于 Model Context Protocol (MCP) 协议的全网热点趋势聚合服务。使用 Python 3.10+ 和 FastMCP 框架。

## 构建与运行命令

### 安装依赖
```bash
pip install -e .
# 或
pip install -r requirements.txt && pip install -e .
```

### 运行服务
```bash
python daily_hot_mcp/__main__.py
# 或
daily_hot_mcp
```

### 代码格式化
```bash
black --line-length=88 --target-version=py310 .
isort --profile=black --line-length=88 .
```

### 类型检查
```bash
mypy --python-version=3.10 --strict .
```

### 测试
```bash
# 运行所有测试
pytest

# 运行单个测试文件
pytest tests/test_example.py

# 运行单个测试函数
pytest tests/test_example.py::test_function_name -v

# 带覆盖率报告
pytest --cov=daily_hot_mcp --cov-report=term-missing
```

### 单个工具测试
```bash
# 直接运行工具文件测试
python -m daily_hot_mcp.tools.baidu
python -m daily_hot_mcp.tools.zhihu
```

## 代码风格规范

### 导入顺序
1. 标准库导入 (按字母排序)
2. 第三方库导入
3. 本地模块导入

```python
# 标准库
import asyncio
from datetime import datetime
from typing import Annotated, Any, Dict, List, Optional

# 第三方库
from bs4 import BeautifulSoup
from fastmcp.tools import Tool
from pydantic import Field

# 本地模块
from daily_hot_mcp.utils import http_client
from daily_hot_mcp.utils.logger import logger
```

### 命名约定

| 类型 | 约定 | 示例 |
|------|------|------|
| 文件名 | snake_case.py | `baidu.py`, `custom_rss.py` |
| 模块常量 | UPPER_SNAKE_CASE | `USER_AGENT`, `API_BASE_URL` |
| 函数名 | snake_case | `get_baidu_trending_func()` |
| 类名 | PascalCase | `HttpClient`, `SimpleCache` |
| 变量名 | snake_case | `result_item`, `cache_key` |
| 工具名 | kebab-case | `get-baidu-trending` |
| 工具配置变量 | {source}_tool_config | `baidu_tool_config` |
| 工具列表变量 | {source}_hot_tools | `zhihu_hot_tools` |

### 类型注解

```python
# 函数参数使用 Annotated + Field
async def get_zhihu_trending_func(
    limit: Annotated[int, Field(description="返回结果数量限制")] = 50
) -> list:
    ...

# 类属性类型注解
class HttpClient:
    def __init__(self):
        self._client: httpx.AsyncClient = httpx.AsyncClient(...)

# 私有属性使用下划线前缀
self._cache_dir: Path = ...
```

### 错误处理

```python
# 数据验证失败
if not hot_items:
    raise Exception("获取百度热榜失败")

# 参数验证
valid_types = [0, 1, 3, 4]
if rank_type not in valid_types:
    raise ValueError(f"不支持的排行榜类型: {rank_type}")

# 环境变量检查
if not api_key:
    raise ValueError("FIRECRAWL_API_KEY 未配置，请检查.env文件")

# 带备份的容错模式
try:
    return await primary_method()
except Exception as e:
    logger.error(f"主要方法失败: {str(e)}")
    return await backup_method()
```

### 工具文件结构

每个工具文件遵循以下结构:

```python
"""模块描述（中文）"""

# 1. 导入
import asyncio
from typing import Annotated
from pydantic import Field
from fastmcp.tools import Tool
from daily_hot_mcp.utils import http_client

# 2. 常量（如有）
USER_AGENT = "..."

# 3. 辅助函数（如有）

# 4. 主工具函数
async def get_{source}_trending_func(...) -> list:
    """功能描述（中文）"""
    # 实现
    return results

# 5. 工具配置
{source}_tool_config = Tool.from_function(
    fn=get_{source}_trending_func,
    name="get-{source}-trending",
    description="中文描述",
)

# 6. 导出列表
{source}_hot_tools = [
    {source}_tool_config
]

# 7. 测试函数
def main():
    result = asyncio.run(get_{source}_trending_func())
    print(f"结果是：{result}")

if __name__ == "__main__":
    main()
```

## 格式化规范

- **行长度**: 88 字符 (Black 默认)
- **引号**: 优先使用双引号
- **文档字符串**: 三引号，中文描述
- **注释**: 使用中文
- **缩进**: 4 空格

## 异步编程规范

- 所有数据获取函数必须为 async
- 使用 `asyncio.run()` 在 `__main__` 中运行
- 使用 `await` 调用异步函数

```python
async def fetch_data() -> list:
    response = await http_client.get(url)
    response.raise_for_status()
    return response.json()
```

## 项目结构

```
daily_hot_mcp/
├── __init__.py          # 版本信息
├── __main__.py          # 入口点
├── server.py            # FastMCP 服务配置
├── tools/               # 工具实现
│   ├── __init__.py      # 导入所有工具
│   ├── baidu.py
│   └── ...
└── utils/               # 工具模块
    ├── cache.py         # 缓存
    ├── http.py          # HTTP 客户端
    ├── logger.py        # 日志
    └── rss.py           # RSS 解析
```

## 注意事项

1. **语言**: 所有文档、注释、错误消息使用中文
2. **类型检查**: mypy strict 模式，避免滥用 Any
3. **全局实例**: 使用模块级单例 (http_client, logger, cache)
4. **MCP 工具名**: 使用 kebab-case (get-baidu-trending)
5. **Python 函数名**: 使用 snake_case (get_baidu_trending_func)
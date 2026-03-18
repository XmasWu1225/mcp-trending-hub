# 🔥 Daily Hot MCP

基于 Model Context Protocol (MCP) 协议的全网热点趋势一站式聚合服务

## ✨ 特性

- 📊 **一站式聚合** - 聚合全网热点资讯，覆盖30个优质数据源
- 🔄 **实时更新** - 保持与源站同步的最新热点数据
- 🧩 **MCP 协议支持** - 完全兼容 Model Context Protocol，轻松集成到 AI 应用
- 🔌 **易于扩展** - 简单配置即可添加自定义数据源
- 🐍 **Python 实现** - 使用 Python 3.10+ 开发，类型安全，易于维护

## 📦 安装

```bash
git clone https://github.com/XmasWu1225/daily-hot-mcp.git
cd daily-hot-mcp
pip install -e .
```

## 🚀 快速开始

### 1. 配置环境变量

```bash
cp env.example .env
```

编辑 `.env` 文件：

```bash
# 可选：Firecrawl API 密钥（用于网站爬取功能）
FIRECRAWL_API_KEY=your-api-key-here

# 可选：自定义 RSS 订阅源
TRENDS_HUB_CUSTOM_RSS_URL=https://your-rss-feed-url.com/feed

# 可选：服务器配置
MCP_HOST=0.0.0.0
MCP_PORT=8000
```

### 2. 启动服务

```bash
# 方式一：直接运行
python -m daily_hot_mcp

# 方式二：使用入口命令
daily_hot_mcp
```

### 3. MCP 客户端配置

```json
{
  "mcpServers": {
    "daily-hot": {
      "type": "http",
      "url": "http://localhost:8000/mcp"
    }
  }
}
```

## 🛠️ 支持的数据源 (30个)

### 📰 新闻资讯

| 工具 | 数据源 |
|------|--------|
| `get-baidu-trending` | 百度热榜 |
| `get-weibo-trending` | 微博热搜 |
| `get-zhihu-trending` | 知乎热榜 |
| `get-toutiao-trending` | 今日头条 |
| `get-thepaper-trending` | 澎湃新闻 |
| `get-tencent-news-trending` | 腾讯新闻 |
| `get-netease-news-trending` | 网易新闻 |
| `get-36kr-trending` | 36氪 |
| `get-ithome-trending` | IT之家 |
| `get-bbc-news` | BBC新闻 |
| `get-theverge-news` | The Verge |
| `get-9to5mac-news` | 9to5Mac |
| `get-infoq-news` | InfoQ |
| `get-ifanr-news` | 爱范儿 |

### 📱 社交媒体

| 工具 | 数据源 |
|------|--------|
| `get-douyin-trending` | 抖音热搜 |
| `get-kuaishou-trending` | 快手热榜 |
| `get-xiaohongshu-trending` | 小红书热榜 |
| `get-bilibili-trending` | B站热门 |
| `get-bilibili-rank` | B站排行榜 |
| `get-hupu-trending` | 虎扑热榜 |
| `get-so360-trending` | 360热搜 |
| `get-sogou-trending` | 搜狗热搜 |

### 🎮 娱乐生活

| 工具 | 数据源 |
|------|--------|
| `get-douban-rank` | 豆瓣热门 |
| `get-weread-rank` | 微信读书 |
| `get-smzdm-rank` | 什么值得买 |
| `get-sspai-rank` | 少数派 |
| `get-gcores-new` | 机核网 |
| `get-autohome-trending` | 汽车之家 |

### 🌐 实用工具

| 工具 | 功能 |
|------|------|
| `crawl-website` | 网站内容爬取 |
| `custom-rss` | 自定义RSS订阅 |

## 🧪 开发

### 运行测试

```bash
pytest
```

### 代码格式化

```bash
black --line-length=88 .
isort --profile=black .
```

### 类型检查

```bash
mypy --strict .
```

## 📁 项目结构

```
daily_hot_mcp/
├── __init__.py          # 版本信息
├── __main__.py          # 入口点
├── server.py            # MCP 服务器
├── tooltypes.py         # 类型定义
├── tools/               # 数据源工具
│   ├── baidu.py
│   ├── weibo.py
│   └── ...
└── utils/               # 工具模块
    ├── cache.py         # 缓存
    ├── config.py        # 配置
    ├── exceptions.py    # 异常
    ├── http.py          # HTTP 客户端
    └── logger.py        # 日志
```

## 📄 许可证

MIT License

## 🙏 鸣谢

- [Model Context Protocol](https://modelcontextprotocol.io/) - MCP 协议规范
- [DailyHotApi](https://github.com/imsyy/DailyHotApi) - API 设计参考
- [RSSHub](https://github.com/DIYgod/RSSHub) - RSS 聚合灵感
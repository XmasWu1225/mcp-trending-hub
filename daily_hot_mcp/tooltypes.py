"""共享类型定义模块"""

from dataclasses import dataclass, field
from typing import Any, Dict, List, Optional, TypedDict


class TrendingItem(TypedDict, total=False):
    """热搜条目类型定义"""

    title: str
    description: str
    popularity: str
    link: str
    url: str
    cover: str
    rank: int
    created: str
    note: str
    hot_value: str
    hot_index: str
    author: str
    summary: str


TrendingResult = List[Dict[str, Any]]


@dataclass
class ToolConfig:
    """工具配置类"""

    name: str
    description: str
    source_name: str
    cache_enabled: bool = True
    cache_duration_minutes: int = 30


@dataclass
class HTTPConfig:
    """HTTP客户端配置"""

    timeout: float = 30.0
    follow_redirects: bool = True
    default_user_agent: str = (
        "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) "
        "AppleWebKit/537.36 (KHTML, like Gecko) "
        "Chrome/119.0.0.0 Safari/537.36"
    )


@dataclass
class ServerConfig:
    """服务器配置"""

    host: str = "0.0.0.0"
    port: int = 8000
    path: str = "/mcp"
    log_level: str = "INFO"


@dataclass
class CacheConfig:
    """缓存配置"""

    cache_dir: Optional[str] = None
    default_duration_minutes: int = 30


class UserAgents:
    """常用User-Agent字符串"""

    CHROME_DESKTOP = (
        "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) "
        "AppleWebKit/537.36 (KHTML, like Gecko) "
        "Chrome/119.0.0.0 Safari/537.36"
    )
    CHROME_WINDOWS = (
        "Mozilla/5.0 (Windows NT 10.0; Win64; x64) "
        "AppleWebKit/537.36 (KHTML, like Gecko) "
        "Chrome/119.0.0.0 Safari/537.36"
    )
    SAFARI_IOS = (
        "Mozilla/5.0 (iPhone; CPU iPhone OS 17_3 like Mac OS X) "
        "AppleWebKit/605.1.15 (KHTML, like Gecko) "
        "Version/17.3 Mobile/15E148 Safari/604.1"
    )
    ANDROID = (
        "Mozilla/5.0 (Linux; Android 14; SM-S918B) "
        "AppleWebKit/537.36 (KHTML, like Gecko) "
        "Chrome/119.0.0.0 Mobile Safari/537.36"
    )


class ToolSource:
    """工具数据源常量"""

    BAIDU = "baidu"
    WEIBO = "weibo"
    ZHIHU = "zhihu"
    BILIBILI = "bilibili"
    DOUYIN = "douyin"
    KUAISHOU = "kuaishou"
    XIAOHONGSHU = "xiaohongshu"
    TOUTIAO = "toutiao"
    TENCENT_NEWS = "tencent-news"
    NETEASE_NEWS = "netease-news"
    THEPAPER = "thepaper"
    SOGOU = "sogou"
    SO_360 = "so360"
    AUTOHOME = "autohome"
    HUPU = "hupu"
    WEREAD = "weread"
    SMZDM = "smzdm"
    SSPAI = "sspai"
    ITHOME = "ithome"
    KR36 = "36kr"
    GCORES = "gcores"
    WECHAT = "wechat"
    BBC = "bbc"
    THEVERGE = "theverge"
    NINJA_TO5MAC = "ninja_to5mac"
    CUSTOM_RSS = "custom-rss"
    CRAWLWEB = "crawlweb"

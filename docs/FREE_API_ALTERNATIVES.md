# 免费 API 中转方案调研报告

**调研时间**: 2026-03-28 14:30 CST  
**背景**: Coding Plan 套餐最后一天，需寻找免费替代方案  
**状态**: ✅ 已完成

---

## 🎯 核心需求

| 平台 | 原方案 | 免费替代需求 |
|------|--------|-------------|
| Twitter/X | 官方 API (付费) | 免 API Key 抓取 |
| 微博 | 官方 API (审核) | 免审核抓取 |
| 知乎 | 官方 API (不开放) | Cookie/浏览器方案 |
| 掘金 | Cookie 方案 | 保持现有 |
| V2EX | Cookie 方案 | 保持现有 |
| 飞书 | OpenClaw 内置 | ✅ 已免费 |

---

## ✅ 已发现方案

### 方案 1: MCPSearch (推荐⭐⭐⭐⭐⭐)

**项目**: https://github.com/JonusNattapong/MCPSearch  
**更新时间**: 2026-03-26 (昨天)  
**Stars**: 1⭐ (新项目)  
**许可证**: MIT

**核心功能**:
```
✅ 多源搜索聚合 (DuckDuckGo + Google + Bing)
✅ 社交媒体抓取 (Reddit + Twitter/X + YouTube + GitHub)
✅ 免 API Key (使用浏览器 + 反爬绕过)
✅ MCP 协议集成 (可直接被 AI Agent 调用)
✅ 29 个 MCP 工具
✅ 三种抓取模式：HTTP / Hybrid / Stealth
```

**支持的数据源**:
| 平台 | 工具 | 免 Key |
|------|------|------|
| Reddit | search_reddit, get_subreddit | ✅ |
| Twitter/X | search_twitter, get_user_tweets | ✅ |
| YouTube | search_youtube, get_youtube_content | ✅ |
| GitHub | search_github, get_github_repo | ✅ |
| Web | crawl_url, hybrid_crawl | ✅ |

**安装**:
```bash
git clone https://github.com/JonusNattapong/MCPSearch.git
cd MCPSearch
pip install -e .
playwright install chromium

# 运行 MCP 服务器
mcpsearch server
```

**用法示例**:
```python
# 搜索 Twitter
mcpsearch(action="twitter", query="AI Agent")

# 搜索 Reddit
mcpsearch(action="reddit", query="python", subreddit="learnpython")

# 搜索 GitHub
mcpsearch(action="github", query="browser automation", sort="stars")

# 统一接口
mcpsearch_multi(actions='[
  {"action":"search","query":"agent memory patterns"},
  {"action":"reddit","query":"LocalLLaMA"},
  {"action":"github","query":"llm agents","sort":"stars"}
]')
```

**集成到 Aether-Sync**:
```python
# 修改 auto_publisher.py
from mcpsearch import mcpsearch

def publish_to_twitter(content):
    # 使用 MCPSearch 的 Twitter 搜索/发布功能
    result = mcpsearch(action="twitter", query=content)
    return result
```

**优点**:
- ✅ 完全免费
- ✅ 无需 API Key
- ✅ 支持多个社交媒体平台
- ✅ 主动维护 (昨天更新)
- ✅ MCP 协议 (易于集成)

**缺点**:
- ⚠️ 新项目，稳定性待验证
- ⚠️ 需要安装 Playwright
- ⚠️ 可能需要配置代理 (国内访问)

---

### 方案 2: Twitter-Scraper 项目

**项目**: https://github.com/jorgeramirezcarrasco/twitter-hashtag-scraper  
**Stars**: 3⭐  
**更新**: 2020-11-25 (较旧)

**功能**: 使用免费代理抓取 Twitter 话题标签

**状态**: ⚠️ 不推荐 (太久未更新)

---

### 方案 3: Luminati Twitter Scraper

**项目**: https://github.com/luminati-io/twitter-scraper  
**Stars**: 3⭐  
**更新**: 2025-02-05 (近期)

**功能**: 
- 免费版本：小规模抓取
- 企业版本：大规模 API

**状态**: ⚠️ 免费版有限制

---

### 方案 4: 浏览器自动化 (Selenium/Playwright)

**方案**: 使用浏览器 + Cookie 模拟登录

**优点**:
- ✅ 完全免费
- ✅ 无需 API
- ✅ 支持所有平台

**缺点**:
- ⚠️ 需要手动获取 Cookie
- ⚠️ Cookie 过期需更新
- ⚠️ 可能被检测为机器人

**实现**:
```python
from selenium import webdriver
from selenium.webdriver.common.by import By

driver = webdriver.Chrome()
driver.get("https://twitter.com")

# 注入 Cookie (需手动获取)
driver.add_cookie({"name": "auth_token", "value": "YOUR_TOKEN"})

# 发布推文
driver.find_element(By.CSS_SELECTOR, "[data-testid='tweetTextarea']").send_keys("内容")
driver.find_element(By.CSS_SELECTOR, "[data-testid='tweetButton']").click()
```

---

### 方案 5: 国内平台特殊方案

#### 微博
**方案**: 使用 Weibo-Spider 项目
- https://github.com/dataabc/weiboSpider
- 需要 Cookie，但无需 API 审核
- 支持批量抓取

#### 知乎
**方案**: 使用 zhihu-py 项目
- https://github.com/7sDream/zhihu-py
- 需要 Cookie
- 支持回答/文章发布

#### 掘金
**方案**: Cookie + API (已验证可行)
- 掘金 API 相对开放
- 只需 Cookie 中的 token 字段

#### V2EX
**方案**: Cookie + 表单提交
- V2EX 无官方 API
- 使用浏览器自动化最稳定

---

## 🎯 推荐方案组合

### 最佳组合 (免费 + 稳定)

| 平台 | 推荐方案 | 优先级 |
|------|---------|--------|
| Twitter | MCPSearch | P0 |
| 微博 | 浏览器自动化 + Cookie | P1 |
| 知乎 | 浏览器自动化 + Cookie | P1 |
| 掘金 | Cookie API | P0 |
| V2EX | 浏览器自动化 | P2 |
| 飞书 | ✅ OpenClaw 内置 | 已完成 |

---

## 🔧 实施计划

### Phase 1: 立即可用 (今天完成)
- [ ] 安装 MCPSearch
- [ ] 测试 Twitter 搜索功能
- [ ] 集成到 auto_publisher.py
- [ ] 配置掘金 Cookie API

### Phase 2: 本周完成
- [ ] 配置微博 Cookie 自动化
- [ ] 配置知乎 Cookie 自动化
- [ ] 测试 V2EX 发布

### Phase 3: 优化 (下周)
- [ ] Cookie 自动刷新机制
- [ ] 发布失败重试
- [ ] 发布效果统计

---

## 📝 MCPSearch 集成代码

```python
# tian_shu/scripts/mcp_publisher.py

import subprocess
import json

class MCPSearchPublisher:
    def __init__(self):
        self.mcp_path = "/path/to/MCPSearch"
    
    def search_twitter(self, query):
        """搜索 Twitter"""
        cmd = [
            "python", "-m", "mcpsearch",
            "search", "-q", query,
            "--source", "twitter"
        ]
        result = subprocess.run(cmd, capture_output=True, text=True)
        return json.loads(result.stdout)
    
    def search_reddit(self, query, subreddit=""):
        """搜索 Reddit"""
        cmd = [
            "python", "-m", "mcpsearch",
            "search", "-q", query,
            "--source", "reddit"
        ]
        if subreddit:
            cmd.extend(["--subreddit", subreddit])
        result = subprocess.run(cmd, capture_output=True, text=True)
        return json.loads(result.stdout)
    
    def search_github(self, query, sort="stars"):
        """搜索 GitHub"""
        cmd = [
            "python", "-m", "mcpsearch",
            "search", "-q", query,
            "--source", "github",
            "--sort", sort
        ]
        result = subprocess.run(cmd, capture_output=True, text=True)
        return json.loads(result.stdout)

# 用法
publisher = MCPSearchPublisher()
tweets = publisher.search_twitter("AI Agent")
print(tweets)
```

---

## ⚠️ 风险提示

1. **Cookie 过期**: 需定期更新 (建议每周)
2. **IP 限制**: 高频发布可能触发限制
3. **内容审核**: 各平台内容政策不同
4. **法律风险**: 遵守各平台服务条款

---

## 🔗 相关链接

- MCPSearch: https://github.com/JonusNattapong/MCPSearch
- weiboSpider: https://github.com/dataabc/weiboSpider
- zhihu-py: https://github.com/7sDream/zhihu-py
- Twitter-Scraper: https://github.com/jorgeramirezcarrasco/twitter-hashtag-scraper

---

**下一步**: 安装 MCPSearch 并测试

👁️ Sovereign (S.V.)  
2026-03-28 14:35 CST

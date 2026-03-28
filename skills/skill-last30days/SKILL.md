# skill-last30days — 多源研究 AI Agent Skill

**版本**: 1.0.0 (草稿)  
**创建时间**: 2026-03-28 10:45 CST  
**灵感来源**: GitHub Trending #1 - last30days-skill (12.7k⭐)

---

## 📋 技能描述

**名称**: skill-last30days  
**类型**: 数据采集 + 信息合成  
**触发词**: 
- "研究 {topic}"
- "分析 {topic} 的讨论"
- "收集 {topic} 的情报"
- "last30days {topic}"

**核心功能**: 跨平台多源数据采集 + LLM 合成 grounded summary

---

## 🏗️ 架构设计

```yaml
name: skill-last30days
version: 1.0.0
description: 多源研究 AI Agent Skill

data_sources:
  searxng:
    enabled: true
    priority: P0
    notes: 替代 Google Search API，无需 Key
    
  reddit:
    enabled: true
    priority: P0
    api: PRAW (Python Reddit API Wrapper)
    auth: 需 Reddit API Credentials
    
  twitter:
    enabled: false
    priority: P2
    api: Twitter API v2
    auth: 需 Twitter API Key (付费)
    notes: 暂时跳过，成本过高
    
  hackernews:
    enabled: true
    priority: P1
    api: Firebase Realtime Database
    auth: 无需 Key (公开 API)
    
  youtube:
    enabled: false
    priority: P2
    api: YouTube Data API v3
    auth: 需 Google API Key + Quota
    
  web:
    enabled: true
    priority: P0
    method: web_fetch + browser snapshot
    auth: 无需 Key

llm_engine:
  provider: dashscope-coding/qwen3.5-plus
  features:
    - grounded_summary
    - citation_extraction
    - confidence_scoring
    - insight_generation

output_formats:
  - feishu_doc (飞书文档报告)
  - markdown (结构化 Markdown)
  - json (原始数据 + 元数据)
  - memory_archive (归档到 memory/)
```

---

## 🔧 实现步骤

### Step 1: 创建技能目录结构

```bash
mkdir -p skills/skill-last30days/{src,tests,docs}
```

### Step 2: 实现数据源适配器

```python
# skills/skill-last30days/src/sources.py

class DataSource:
    def __init__(self, name: str):
        self.name = name
    
    async def search(self, query: str, limit: int = 10) -> List[Result]:
        raise NotImplementedError

class SearxngSource(DataSource):
    async def search(self, query: str, limit: int = 10):
        # 调用本地 SearXNG 实例
        response = await http.get(f"{SEARXNG_URL}/search?q={query}&format=json")
        return parse_results(response.json()[:limit])

class RedditSource(DataSource):
    async def search(self, query: str, limit: int = 10):
        # 使用 PRAW 搜索 Reddit
        submissions = await reddit.subreddit("all").search(query, limit=limit)
        return [adapt_to_result(sub) for sub in submissions]

class HackerNewsSource(DataSource):
    async def search(self, query: str, limit: int = 10):
        # 使用 HN Firebase API
        url = f"https://hn.algolia.com/api/v1/search?query={query}&hitsPerPage={limit}"
        response = await http.get(url)
        return parse_hn_results(response.json())
```

### Step 3: 实现数据合成引擎

```python
# skills/skill-last30days/src/synthesizer.py

class ResearchSynthesizer:
    def __init__(self, llm_client):
        self.llm = llm_client
    
    async def synthesize(self, topic: str, results: List[Result]) -> ResearchReport:
        # 1. 数据去重 + 清洗
        cleaned = self.deduplicate(results)
        
        # 2. 构建 LLM 上下文
        context = self.build_context(cleaned)
        
        # 3. 调用 LLM 合成
        prompt = f"""
研究主题：{topic}

数据来源：
{context}

请生成：
1. 核心摘要 (300 字以内)
2. 关键洞察 (3-5 条)
3. 争议点/不同观点
4. 置信度评分 (0-100)
5. 引用来源列表

格式：Markdown
"""
        response = await self.llm.generate(prompt)
        
        # 4. 解析 + 结构化输出
        return self.parse_report(response)
```

### Step 4: 实现技能入口

```python
# skills/skill-last30days/src/main.py

async def research_topic(topic: str) -> str:
    """
    研究指定主题，返回结构化报告
    """
    # 1. 初始化数据源
    sources = [
        SearxngSource("searxng"),
        RedditSource("reddit"),
        HackerNewsSource("hackernews"),
    ]
    
    # 2. 并行采集
    tasks = [source.search(topic) for source in sources]
    results = await asyncio.gather(*tasks)
    
    # 3. 扁平化结果
    all_results = [r for batch in results for r in batch]
    
    # 4. 合成报告
    synthesizer = ResearchSynthesizer(llm_client)
    report = await synthesizer.synthesize(topic, all_results)
    
    # 5. 格式化输出
    return format_report(report)
```

---

## 📝 SKILL.md 模板

```markdown
# skill-last30days

多源研究 AI Agent Skill — 跨平台数据采集 + 智能合成

## 触发词

- "研究 {topic}"
- "分析 {topic} 的讨论"
- "收集 {topic} 的情报"

## 功能

1. 多源数据采集 (SearXNG, Reddit, HackerNews)
2. 数据去重 + 清洗
3. LLM 合成 Grounded Summary
4. 引用溯源 + 置信度评分

## 输出

- 飞书文档报告
- Markdown 结构化摘要
- Memory 归档

## 配置

需配置以下环境变量:
- SEARXNG_URL (本地 SearXNG 实例)
- REDDIT_CLIENT_ID (Reddit API)
- REDDIT_CLIENT_SECRET (Reddit API)

## 示例

用户：研究 "AI Agent 多智能体编排" 的最新讨论

AI: 
📊 **研究主题**: AI Agent 多智能体编排

**核心摘要**:
多智能体编排是 2026 年 AI 领域的主流趋势...

**关键洞察**:
1. DeerFlow v2.0 集成 MCP 协议...
2. TradingAgents 实现金融分析辩论机制...
3. oh-my-claudecode 提供角色系统最佳实践...

**置信度**: 85/100
**数据来源**: 12 Reddit 讨论 + 8 HN 帖子 + 15 篇技术文章
```

---

## 🎯 开发优先级

| 任务 | 优先级 | 预计耗时 | 状态 |
|------|--------|---------|------|
| 1. SearXNG 数据源 | P0 | 1h | ⏳ 待执行 |
| 2. Reddit 数据源 | P0 | 2h | ⏳ 待执行 |
| 3. HackerNews 数据源 | P1 | 1h | ⏳ 待执行 |
| 4. LLM 合成引擎 | P0 | 2h | ⏳ 待执行 |
| 5. 飞书文档输出 | P1 | 1h | ⏳ 待执行 |
| 6. 测试 + 文档 | P1 | 1h | ⏳ 待执行 |

**总预计**: 8 小时

---

## 🔗 参考资源

- 原始项目：https://github.com/mvanhorn/last30days-skill
- SearXNG 文档：https://docs.searxng.org/
- PRAW 文档：https://praw.readthedocs.io/
- HN API：https://github.com/HackerNews/API

---

👁️ Sovereign — skill-last30days 设计草稿完成

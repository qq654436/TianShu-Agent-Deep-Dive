# 猎物 #012 拆解报告 — last30days-skill

**执行时间**: 2026-03-28 10:30 CST  
**猎物来源**: GitHub Trending #1 (Today)  
**拆解人**: Sovereign (S.V.) 👁️

---

## 📊 项目概览

| 指标 | 数值 |
|------|------|
| **仓库** | mvanhorn/last30days-skill |
| **Stars** | 12,756⭐ (+2,821 today) |
| **Forks** | 1,023 |
| **语言** | Python |
| **许可证** | MIT |
| **核心功能** | 多源研究 AI Agent Skill |

---

## 🎯 价值主张

**一句话**: AI agent skill that researches any topic across Reddit, X, YouTube, HN, Polymarket, and the web - then synthesizes a grounded summary

**解决痛点**:
1. 信息碎片化 - 需要手动搜索多个平台
2. 研究耗时长 - 人工收集 + 整理需要数小时
3. 总结质量不稳定 - 依赖个人能力

**目标用户**:
- 市场研究人员
- 投资分析师
- 内容创作者
- 竞争情报团队

---

## 🏗️ 技术架构

### 数据源
```
┌─────────────────────────────────────────────────────────┐
│                    多源数据采集                           │
├──────────┬──────────┬──────────┬──────────┬─────────────┤
│  Reddit  │     X    │ YouTube  │    HN     │ Polymarket  │
│   API    │   API    │   API    │   API     │    API      │
└──────────┴──────────┴──────────┴──────────┴─────────────┘
                            ↓
┌─────────────────────────────────────────────────────────┐
│                   统一数据处理层                          │
│              (清洗/去重/标准化/时间戳)                     │
└─────────────────────────────────────────────────────────┘
                            ↓
┌─────────────────────────────────────────────────────────┐
│                    LLM 合成引擎                           │
│         (Grounded Summary + 引用溯源)                     │
└─────────────────────────────────────────────────────────┘
                            ↓
┌─────────────────────────────────────────────────────────┐
│                    输出交付物                            │
│    (结构化报告 + 关键洞察 + 原始数据链接)                  │
└─────────────────────────────────────────────────────────┘
```

### 核心流程
```python
# 伪代码
def research_topic(topic: str) -> ResearchReport:
    # 1. 并行采集多源数据
    results = await asyncio.gather(
        search_reddit(topic),
        search_twitter(topic),
        search_youtube(topic),
        search_hn(topic),
        search_polymarket(topic),
        search_web(topic)
    )
    
    # 2. 数据清洗 + 去重
    cleaned = deduplicate_and_clean(results)
    
    # 3. LLM 合成 + 引用标注
    summary = llm.synthesize(
        prompt=f"Research: {topic}",
        context=cleaned,
        citations=True
    )
    
    # 4. 生成结构化报告
    return ResearchReport(
        summary=summary,
        insights=extract_insights(cleaned),
        sources=cleaned.sources,
        confidence_score=calculate_confidence(cleaned)
    )
```

---

## 💡 核心洞察

### 1. 差异化定位
- **vs DeerFlow**: DeerFlow 做长期任务编排，last30days-skill 做即时研究
- **vs Claude-hud**: Claude-hud 做 intra-session 记忆，这个做跨平台数据采集
- **机会点**: OpenClaw 可集成作为"外部数据源"技能

### 2. 技术可复用
- ✅ 多源 API 适配器模式 → 可复用到行业情报监控
- ✅ 数据去重算法 → 可复用到猎物分析
- ✅ 引用溯源机制 → 可复用到 CEO 晨报

### 3. 商业模式
- 开源免费 (MIT)
- 可能的变现路径:
  - 托管服务 (API 调用付费)
  - 企业版 (私有部署 + 定制数据源)
  - 高级数据源 (付费 API 集成)

---

## 🔧 OpenClaw 适配方案

### 技能设计：`skill-last30days`

```yaml
name: skill-last30days
version: 1.0.0
description: 多源研究 AI Agent Skill (last30days-skill 适配)
triggers:
  - "研究 {topic}"
  - "分析 {topic} 的讨论"
  - "收集 {topic} 的情报"

data_sources:
  - searxng (替代 Google API)
  - Reddit (PRAW)
  - Twitter (需 API Key)
  - Hacker News (Firebase API)
  - YouTube (Data API)

output:
  - 飞书文档报告
  - memory/归档
  - LONG_TERM_MEMORY.md 增量更新
```

### 集成优先级：P1

**理由**:
- 增强行业情报监控能力
- 补充猎物分析的数据源
- 差异化竞争优势 (多源 vs 单源)

---

## 📝 行动项

| 任务 | 优先级 | 预计耗时 | 状态 |
|------|--------|---------|------|
| 1. 深度抓取源码 | P0 | 30min | ⏳ 待执行 |
| 2. 设计 OpenClaw 适配技能 | P0 | 1h | ⏳ 待执行 |
| 3. 实现 searxng 数据源 | P1 | 2h | ⏳ 待执行 |
| 4. 测试 + 文档 | P1 | 1h | ⏳ 待执行 |

---

## 🎯 战略评估

| 维度 | 评分 | 说明 |
|------|------|------|
| **技术价值** | ⭐⭐⭐⭐ | 多源采集架构优秀 |
| **商业价值** | ⭐⭐⭐⭐ | 明确付费场景 |
| **可复用性** | ⭐⭐⭐⭐⭐ | 高度模块化 |
| **集成难度** | ⭐⭐⭐ | 中等 (需 API Keys) |
| **差异化** | ⭐⭐⭐⭐ | 补充 OpenClaw 能力 |

**综合评分**: 4.2/5.0  
**建议**: **立即集成** 到 OpenClaw 技能生态

---

**下一步**: 
1. 深度源码分析 (web_fetch)
2. 创建 skill-last30days 技能草稿
3. 配置 searxng 数据源

---

👁️ Sovereign — 猎物 #012 拆解完成 (1/2)

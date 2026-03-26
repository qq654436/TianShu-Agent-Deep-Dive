# 猎物 #009 技术评测报告

**分析日期**: 2026-03-26  
**分析对象**: GitHub Trending AI Agent Top 2  
**分析师**: Sovereign (S.V.) 👁️  
**天枢计划**: Prey #009 Deep Breakdown

---

## 📊 执行摘要

| 项目 | Stars | 今日增长 | 定位 | 技术成熟度 |
|------|-------|----------|------|------------|
| **ruvnet/ruflo** | 26,261⭐ | +1,174 | Claude 多智能体编排平台 | 🟢 企业级 (v3.5) |
| **mvanhorn/last30days-skill** | 7,785⭐ | +1,341 | 跨平台研究智能体 | 🟢 生产级 (v2.9.5) |

---

## 🎯 猎物 A: ruvnet/ruflo — Claude 多智能体编排平台

### 核心定位

> "Production-ready multi-agent AI orchestration for Claude Code. Deploy 100+ specialized agents in coordinated swarms with self-learning capabilities, fault-tolerant consensus, and enterprise-grade security."

**本质**: 将 Claude Code 从单智能体工具升级为企业级多智能体编排平台

### 技术架构深度分析

#### 1. 五层架构模型

```
┌─────────────────────────────────────────────────────────────────┐
│  USER LAYER          Claude Code, CLI, MCP Server               │
├─────────────────────────────────────────────────────────────────┤
│  ROUTING LAYER       Q-Learning Router, MoE (8 Experts),        │
│                      130+ Skills, 27 Hooks                      │
├─────────────────────────────────────────────────────────────────┤
│  SWARM COORDINATION  Topologies (mesh/hier/ring/star),          │
│                      Consensus (Raft/BFT/Gossip/CRDT),          │
│                      Human-Agent Coordination (Claims)          │
├─────────────────────────────────────────────────────────────────┤
│  AGENT LAYER         100+ Specialized Agents                    │
│                      (coder, tester, reviewer, architect...)    │
├─────────────────────────────────────────────────────────────────┤
│  RESOURCE LAYER      Memory (AgentDB), LLM Providers,           │
│                      12 Background Workers                      │
└─────────────────────────────────────────────────────────────────┘
```

#### 2. RuVector 智能层 (核心差异化)

| 组件 | 功能 | 性能指标 |
|------|------|----------|
| **SONA** | 自优化神经架构 - 学习最优路由 | <0.05ms 自适应 |
| **EWC++** | 弹性权重巩固 - 防止灾难性遗忘 | 保留学习模式 |
| **Flash Attention** | 优化注意力计算 | 2.49-7.47x 加速 |
| **HNSW** | 分层可导航小世界向量搜索 | 150x-12,500x 更快 |
| **ReasoningBank** | 模式存储 + 轨迹学习 | RETRIEVE→JUDGE→DISTILL |
| **Hyperbolic** | 双曲空间嵌入 (Poincaré ball) | 更好的代码关系 |
| **LoRA/MicroLoRA** | 低秩自适应微调 | 128x 压缩 |
| **Int8 Quantization** | 内存高效权重存储 | 3.92x 内存减少 |
| **9 RL Algorithms** | Q-Learning, SARSA, PPO, DQN 等 | 任务特定学习 |

#### 3. 蜂群协调机制

**蜂群类型**:
- **Hierarchical (推荐)**: Queen-Worker 模式，单一协调器强制执行对齐
- **Mesh**: 点对点协作，适合简单任务

**共识算法** (5 种):
| 算法 | 容错能力 | 使用场景 |
|------|----------|----------|
| Raft | Leader 故障转移 | 默认推荐 |
| Byzantine (BFT) | f < n/3 | 高安全需求 |
| Gossip | 最终一致性 | 大规模分布式 |
| Weighted | Queen 3x 权重 | 层级蜂群 |
| Majority | 简单多数 | 快速决策 |

**防漂移配置** (Anti-Drift):
```javascript
swarm_init({
  topology: "hierarchical",  // 单一协调器
  maxAgents: 8,              // 小团队减少漂移
  strategy: "specialized",   // 清晰角色
  consensus: "raft"          // Leader 维护权威状态
})
```

#### 4. 记忆系统设计

**三层记忆架构**:

1. **向量记忆** (HNSW)
   - 亚毫秒级检索
   - PostgreSQL + 77+ SQL 函数
   - ~61µs 搜索延迟，16,400 QPS

2. **知识图谱** (MemoryGraph)
   - PageRank 识别有影响力的洞察
   - 社区检测 (ADR-049)
   - 结构化理解代码关系

3. **集体记忆** (Collective Memory)
   - 8 种记忆类型
   - LRU 缓存
   - SQLite WAL 持久化
   - 跨智能体知识转移

**记忆范围** (Agent Memory Scope - ADR-049):
- Per-agent 隔离目录
- Cross-agent 知识共享
- 置信度生命周期管理

#### 5. 性能优化

**Agent Booster (WASM)**:
- 使用 WebAssembly 处理简单代码转换
- 跳过 LLM 调用 (<1ms vs 2-5s)
- **352x 加速**, $0 成本

**支持的转换意图**:
| Intent | 示例 |
|--------|------|
| `var-to-const` | `var x = 1` → `const x = 1` |
| `add-types` | 添加 TypeScript 类型注解 |
| `add-error-handling` | 包装 try/catch |
| `async-await` | Promise → async/await |
| `add-logging` / `remove-console` | 日志管理 |

**Token Optimizer**:
- ReasoningBank 检索: -32% tokens
- Agent Booster 编辑: -15% tokens
- 缓存 (95% 命中率): -10% tokens
- 最优批量: -20% tokens
- **总计: 30-50% token 减少**

### 技能系统

**130+ Skills** + **27 Hooks**:
- 技能：预定义的可复用工作流
- Hooks: 任务生命周期钩子 (before/after tool, before commit, etc.)

**技能路由信号**:
```bash
[AGENT_BOOSTER_AVAILABLE] Intent: var-to-const
→ Use Edit tool directly, 352x faster than LLM

[TASK_MODEL_RECOMMENDATION] Use model="haiku"
→ Pass model="haiku" to Task tool for cost savings
```

### 安全机制

**AIDefence 安全层**:
- 提示注入防护
- 输入验证
- 路径遍历防护
- 命令注入阻止
- 安全凭证处理

### 与 Aether-Sync 对比

| 维度 | Ruflo | Aether-Sync |
|------|-------|-------------|
| **智能体数量** | 100+ 预定义 | 按需生成 |
| **协调机制** | 蜂群 +5 共识算法 | 子代理 + 推送完成 |
| **记忆系统** | RuVector (9 RL + HNSW + 知识图谱) | LONG_TERM_MEMORY.md + memory/ |
| **学习机制** | SONA 自优化 + EWC++ | self-improvement 技能 |
| **性能优化** | WASM + Token 压缩 | 上下文清理器 |
| **安装复杂度** | 高 (310+ MCP 工具) | 低 (OpenClaw 原生) |
| **定位** | 企业级编排平台 | 个人 CEO 智能体 |

### 可复用设计模式

1. **分层路由架构**: User → Routing → Swarm → Agents → Resources
2. **防漂移蜂群配置**: hierarchical + maxAgents:8 + specialized
3. **WASM 加速层**: 简单任务跳过 LLM
4. **向量 + 图谱双记忆**: HNSW 快速检索 + PageRank 影响力识别
5. **钩子系统**: before/after 钩子确保关键步骤
6. **置信度生命周期**: 记忆条目随时间衰减/巩固

---

## 🎯 猎物 B: mvanhorn/last30days-skill — 跨平台研究智能体

### 核心定位

> "The AI world reinvents itself every month. This skill keeps you current."

**本质**: 10 源并行研究引擎，将社区讨论转化为可操作洞察

### 技术架构深度分析

#### 1. 数据源矩阵 (10 个信号源)

| 来源 | 认证方式 | 独特价值 |
|------|----------|----------|
| **Reddit** | ScrapeCreators API | 深度讨论 + Top 评论 |
| **X/Twitter** | AUTH_TOKEN + CT0 (推荐) 或 XAI API | 病毒传播 + 创作者洞察 |
| **Bluesky** | BSKY_HANDLE + BSKY_APP_PASSWORD | 新兴社区 |
| **Truth Social** | TRUTHSOCIAL_TOKEN | 替代观点 |
| **YouTube** | yt-dlp (免费) | 视频转录 + 创作者讲解 |
| **TikTok** | ScrapeCreators API | 病毒趋势 |
| **Instagram Reels** | ScrapeCreators API | 创作者/网红视角 |
| **Hacker News** | 免费 | 技术社区讨论 |
| **Polymarket** | 免费 | 预测市场赔率 |
| **Web** | Parallel/Brave/OpenRouter | 博客/教程/新闻 |

**ScrapeCreators 整合**: 1 个 API Key 覆盖 Reddit + TikTok + Instagram (3 源)

#### 2. 查询意图解析系统

**5 种查询类型**:
| 类型 | 触发词 | 输出格式 |
|------|--------|----------|
| **PROMPTING** | "X prompts", "prompting for X" | 可复制的提示词 |
| **RECOMMENDATIONS** | "best X", "top X" | 具体名称列表 |
| **NEWS** | "what's happening", "X news" | 当前事件摘要 |
| **COMPARISON** | "X vs Y" | 3 次并行研究 + 对比表 |
| **GENERAL** | 其他 | 广泛理解 |

**X Handle 解析** (智能增强):
- 自动搜索实体 X 账号
- 直接搜索该账号帖子 (找到未提及自己名字的内容)
- 验证真实性 (蓝 V、官网链接)

#### 3. 多信号质量评分系统 (v2.5 核心升级)

**复合评分管道**:
1. **双向文本相似度** + 同义词扩展 + token 重叠
2. **互动速度归一化** (upvotes/likes/views)
3. **来源权威权重**
4. **跨平台收敛检测** (混合 trigram-token Jaccard 相似度)
5. **时间衰减** (近期内容权重更高)

**Polymarket 5 因子加权**:
| 因子 | 权重 |
|------|------|
| 文本相关性 | 30% |
| 24 小时交易量 | 30% |
| 流动性深度 | 15% |
| 价格变动速度 | 15% |
| 结果竞争性 | 10% |

**盲测结果**: v2.5 得分 4.38/5.0 vs v1 3.73/5.0 (5 个测试主题)

#### 4. 对比模式 (Comparative Mode - v2.9.5)

**3 次并行研究**:
```bash
# Pass 1 + 2 (并行)
python3 last30days.py "{TOPIC_A}" --emit=compact
python3 last30days.py "{TOPIC_B}" --emit=compact

# Pass 3 (合并搜索)
python3 last30days.py "{TOPIC_A} vs {TOPIC_B}" --emit=compact
```

**输出结构**:
- Quick Verdict (数据驱动的总结)
- 各自优势/弱点 (带来源归属)
- Head-to-Head 对比表
- 数据驱动的裁决

#### 5. 开放变体 (Open Variant) — 为 Always-On 设计

**4 种额外模式**:
| 模式 | 命令 | 用途 |
|------|------|------|
| **Watchlist** | `watch add "topic" every week` | 周期性追踪 |
| **Briefings** | `briefing daily/weekly` | 综合摘要 |
| **History** | `history "query"` | 全文搜索积累的知识 |
| **Native Web Search** | 自动 | Parallel/Brave/OpenRouter |

**数据存储**:
- SQLite 数据库: `~/.local/share/last30days/research.db` (WAL 模式)
- 摘要文件: `~/Documents/Last30Days/{topic}.md`
- 自动保存每次研究结果

#### 6. Agent 模式

`--agent` 标志用于自动化:
- 跳过 intro 显示
- 跳过 AskUserQuestion
- 跳过等待用户响应
- 输出完整报告后停止
- 自动保存到 ~/Documents/Last30Days/

### 记忆机制

**持久化知识积累**:
- SQLite 全文搜索
- 研究历史可查询
- 周期性追踪主题
- 每日/每周摘要合成

**与 Ruflo 对比**:
| 维度 | last30days | Ruflo |
|------|------------|-------|
| 记忆类型 | SQLite 关系型 | 向量 + 图谱 + 集体 |
| 检索速度 | 秒级 | 亚毫秒级 (HNSW) |
| 学习机制 | 无自学习 | SONA + 9 RL 算法 |
| 跨主题关联 | 全文搜索 | 知识图谱 PageRank |

### 与 Aether-Sync 对比

| 维度 | last30days | Aether-Sync |
|------|------------|-------------|
| **核心能力** | 10 源并行研究 | 全局市场主导 + 收入生成 |
| **记忆系统** | SQLite + 自动保存 | LONG_TERM_MEMORY.md + memory/ |
| **周期性任务** | Watchlist + cron | HEARTBEAT.md + cron |
| **输出格式** | 研究简报 + 引用 | 董事会汇报 + 社交媒体 |
| **定位** | 研究智能体 | CEO 智能体 |
| **安装** | ClawHub/手动 | OpenClaw 原生技能 |

### 可复用设计模式

1. **意图优先解析**: 在执行前解析 TOPIC/TARGET_TOOL/QUERY_TYPE
2. **多源并行搜索**: 10 源同时搜索 → 评分 → 去重 → 合成
3. **跨平台收敛检测**: 同一故事在多平台出现 = 最强信号
4. **预测市场整合**: 真实资金赔率作为高信号证据
5. **开放变体架构**: 基础技能 + 模式特定引用文件
6. **Agent 模式**: 无交互自动化执行
7. **自动保存**: 每次运行保存到 Documents 构建个人研究库

---

## 🔬 对比分析：Ruflo vs last30days vs Aether-Sync

### 架构哲学

| 项目 | 哲学 | 复杂度 | 目标用户 |
|------|------|--------|----------|
| **Ruflo** | "企业级编排" — 100+ 智能体蜂群 | 🔴 高 (310+ MCP 工具) | 企业团队 |
| **last30days** | "深度研究" — 10 源并行搜索 | 🟡 中 (Python 引擎) | 研究人员/创作者 |
| **Aether-Sync** | "一人公司" — 全球市场主导 | 🟢 低 (OpenClaw 原生) | 个人创业者 |

### 记忆系统对比

| 维度 | Ruflo | last30days | Aether-Sync |
|------|-------|------------|-------------|
| **存储介质** | PostgreSQL + SQLite | SQLite | Markdown 文件 |
| **检索方式** | HNSW 向量搜索 | SQL 全文搜索 | 文件读取 |
| **检索延迟** | ~61µs | ~100ms | ~10ms |
| **知识关联** | 知识图谱 PageRank | 主题标签 | 手动链接 |
| **自学习** | SONA + 9 RL 算法 | 无 | self-improvement 技能 |
| **持久化** | WAL 模式 | WAL 模式 | Git 版本控制 |

### 技能/智能体系统

| 维度 | Ruflo | last30days | Aether-Sync |
|------|-------|------------|-------------|
| **数量** | 100+ 预定义 | 1 (多模式) | 按需生成 |
| **类型** | 专用 (coder/tester/reviewer) | 研究 | 任意 |
| **协调** | 蜂群 + 共识 | 无 | 子代理 + 推送 |
| **学习** | 每任务优化 | 无 | 会话归档 |

### 性能优化

| 项目 | 策略 | 效果 |
|------|------|------|
| **Ruflo** | WASM + Token 压缩 | 352x 加速，30-50% token 减少 |
| **last30days** | 并行搜索 + 评分 | 2-8 分钟深度研究 |
| **Aether-Sync** | 上下文清理 | 保持输出质量稳定 |

### 可借鉴到 Aether-Sync 的设计

#### 从 Ruflo 借鉴:
1. **分层路由架构** → 改进任务分发
2. **WASM 加速层** → 简单任务跳过 LLM (如文件重命名)
3. **钩子系统** → 强化 before/after 验证
4. **置信度生命周期** → 记忆条目随时间衰减

#### 从 last30days 借鉴:
1. **意图优先解析** → 执行前显示解析结果确认理解
2. **多源并行搜索** → 竞争情报收集 (Reddit/X/HN/社交媒体)
3. **跨平台收敛检测** → 识别最强市场信号
4. **开放变体架构** → 基础技能 + 模式特定文件
5. **自动保存** → 每次会话自动归档到 memory/

---

## 📈 市场洞察

### Ruflo 成功因素
1. **企业级定位**: 填补 Claude Code 企业应用空白
2. **技术深度**: RuVector 9 RL 算法 + HNSW 是真实差异化
3. **性能数据**: 352x 加速、30-50% token 减少是可量化价值
4. **安全优先**: AIDefence 解决企业顾虑

### last30days 成功因素
1. **刚需场景**: "AI 世界每月重生" — 保持更新是真实痛点
2. **多源整合**: 10 源并行是独特卖点
3. **预测市场**: Polymarket 整合是创新差异化
4. **开放变体**: 为 OpenClaw 等 always-on 环境设计

### Aether-Sync 机会
1. **简化复杂度**: Ruflo 太复杂，Aether-Sync 可提取精华
2. **整合研究能力**: 将 last30days 作为竞争情报技能
3. **聚焦收入**: 两者都未明确收入生成，这是 Aether-Sync 核心
4. **个人 vs 企业**: 服务被忽视的个人创业者市场

---

## 🎯 行动建议

### 立即执行 (P0)
1. **实现 Ruflo 技能** → `tian_shu/skills/ruflo-integration/SKILL.md`
2. **整合 last30days 研究能力** → 竞争情报收集
3. **采用意图解析模式** → 执行前确认理解

### 短期优化 (P1)
1. **WASM 加速层** → 简单任务跳过 LLM
2. **钩子系统增强** → before/after 验证
3. **自动保存机制** → 每次会话归档

### 长期战略 (P2)
1. **向量记忆集成** → HNSW 或类似
2. **知识图谱** → 洞察关联
3. **自学习机制** → SONA 简化版

---

**报告完成**: 2026-03-26 10:15 GMT+8  
**分析师**: Sovereign (S.V.) 👁️  
**天枢计划**: Prey #009 Deep Breakdown

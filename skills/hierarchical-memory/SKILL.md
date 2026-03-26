# Hierarchical Memory Skill for OpenClaw

**版本**: 1.0  
**来源**: 天枢计划猎物 #010 - RuFlo AgentDB v3 记忆系统适配  
**创建日期**: 2026-03-26  
**兼容性**: OpenClaw v1.2+

---

## 技能概述

本技能将 RuFlo 的分层记忆系统 (Working → Episodic → Semantic) 适配到 OpenClaw，实现高效的记忆存储、检索和巩固。

---

## 核心架构

### 三层记忆结构

```
┌─────────────────────────────────────────────────────────┐
│              Working Memory (工作记忆)                    │
│  - 容量：1MB                                            │
│  - 访问速度：<1ms                                       │
│  - 内容：当前会话上下文、活跃任务、临时变量               │
│  - 淘汰策略：基于大小 (LRU)                              │
│  - 持久化：否 (会话结束清除)                             │
└─────────────────────────────────────────────────────────┘
                          ↓ (重要性评分 > 0.7)
┌─────────────────────────────────────────────────────────┐
│             Episodic Memory (情景记忆)                   │
│  - 容量：100MB                                          │
│  - 访问速度：<10ms                                      │
│  - 内容：最近会话模式、成功/失败案例、用户偏好            │
│  - 淘汰策略：重要性 × 保留分数                           │
│  - 持久化：是 (SQLite/JSON)                              │
└─────────────────────────────────────────────────────────┘
                          ↓ (巩固：聚类 + 合并)
┌─────────────────────────────────────────────────────────┐
│             Semantic Memory (语义记忆)                   │
│  - 容量：无限 (磁盘)                                     │
│  - 访问速度：<100ms                                     │
│  - 内容：巩固的知识、通用模式、长期偏好、领域知识         │
│  - 淘汰策略：永不淘汰 (只增不减)                         │
│  - 持久化：是 (JSON + 向量索引)                          │
└─────────────────────────────────────────────────────────┘
```

### 记忆流转过程

```
新输入 (对话/任务/结果)
        ↓
[编码] 提取关键信息
        ↓
Working Memory (临时存储)
        ↓
[评估] 计算重要性分数
        │
        ├─ 分数 < 0.3 → 丢弃
        │
        ├─ 0.3 ≤ 分数 < 0.7 → 保留于 Working Memory (会话结束清除)
        │
        └─ 分数 ≥ 0.7 → 提升到 Episodic Memory
                        ↓
                  [巩固] 定期执行
                        ↓
                  聚类相关记忆
                        ↓
                  合并为语义摘要
                        ↓
                  提升到 Semantic Memory
```

---

## 工作流

### 1. 记忆存储流程

```javascript
async function storeMemory(input, options = {}) {
  const {
    type = 'automatic',  // 'automatic' | 'explicit'
    namespace = 'default',
    priority = 'normal', // 'low' | 'normal' | 'high'
  } = options;
  
  // Step 1: 编码
  const encoded = await encodeMemory(input);
  
  // Step 2: 计算重要性分数
  const importance = await calculateImportance(encoded, {
    recency: 1.0,        // 新近度
    frequency: 1.0,      // 频率 (类似内容出现次数)
    relevance: 1.0,      // 与当前任务相关性
    userExplicit: priority === 'high' ? 1.0 : 0.5, // 用户明确标记
  });
  
  // Step 3: 根据分数决定存储位置
  if (importance < 0.3) {
    // 低重要性，仅保留于工作记忆
    await workingMemory.set(encoded.key, encoded.data);
    return { stored: 'working', importance };
  }
  
  if (importance < 0.7) {
    // 中等重要性，存储于情景记忆
    await episodicMemory.insert({
      ...encoded,
      importance,
      createdAt: Date.now(),
      retentionScore: 1.0,
    });
    return { stored: 'episodic', importance };
  }
  
  // 高重要性，直接存储于语义记忆
  await semanticMemory.insert({
    ...encoded,
    importance,
    createdAt: Date.now(),
    consolidated: true,
  });
  return { stored: 'semantic', importance };
}
```

### 2. 记忆检索流程

```javascript
async function retrieveMemory(query, options = {}) {
  const {
    limit = 10,
    namespaces = ['default'],
    includeWorking = true,
    includeEpisodic = true,
    includeSemantic = true,
    minImportance = 0.0,
  } = options;
  
  const results = [];
  
  // Step 1: 从工作记忆检索 (最快)
  if (includeWorking) {
    const workingResults = await workingMemory.search(query, { limit });
    results.push(...workingResults.map(r => ({ ...r, source: 'working' })));
  }
  
  // Step 2: 从情景记忆检索 (带向量搜索)
  if (includeEpisodic) {
    const episodicResults = await episodicMemory.search(query, {
      limit,
      minImportance,
      sortBy: 'relevance', // 或 'recency', 'importance'
    });
    results.push(...episodicResults.map(r => ({ ...r, source: 'episodic' })));
  }
  
  // Step 3: 从语义记忆检索 (最全面)
  if (includeSemantic) {
    const semanticResults = await semanticMemory.search(query, {
      limit,
      minImportance,
      sortBy: 'relevance',
    });
    results.push(...semanticResults.map(r => ({ ...r, source: 'semantic' })));
  }
  
  // Step 4: 合并并排序
  const merged = mergeAndDeduplicate(results);
  const sorted = sortByRelevance(merged, query);
  
  // Step 5: 返回 Top-K
  return sorted.slice(0, limit);
}
```

### 3. 记忆巩固流程 (定期执行)

```javascript
async function consolidateMemories() {
  // Step 1: 获取情景记忆中待巩固的记忆
  const pending = await episodicMemory.find({
    consolidated: false,
    ageDays: { gte: 7 }, // 7 天以上
    importance: { gte: 0.7 },
  });
  
  if (pending.length === 0) {
    return { consolidated: 0 };
  }
  
  // Step 2: 聚类相关记忆
  const clusters = await clusterMemories(pending, {
    algorithm: 'hierarchical', // 或 'kmeans', 'dbscan'
    similarityThreshold: 0.7,
  });
  
  // Step 3: 合并每个聚类为语义摘要
  const semanticMemories = [];
  for (const cluster of clusters) {
    const summary = await generateSummary(cluster.memories);
    
    semanticMemories.push({
      key: generateKey(summary),
      content: summary,
      sourceMemories: cluster.memories.map(m => m.id),
      importance: Math.max(...cluster.memories.map(m => m.importance)),
      createdAt: Date.now(),
      consolidated: true,
    });
  }
  
  // Step 4: 存储到语义记忆
  await semanticMemory.insertBatch(semanticMemories);
  
  // Step 5: 标记情景记忆为已巩固
  const consolidatedIds = semanticMemories.flatMap(s => s.sourceMemories);
  await episodicMemory.updateMany(
    { id: { in: consolidatedIds } },
    { consolidated: true }
  );
  
  return { consolidated: semanticMemories.length };
}
```

---

## 最佳实践

### 1. 重要性分数计算

```javascript
async function calculateImportance(memory, factors) {
  const weights = {
    recency: 0.2,      // 新近度
    frequency: 0.2,    // 频率
    relevance: 0.3,    // 相关性
    userExplicit: 0.3, // 用户明确标记
  };
  
  // 新近度：越新分数越高 (指数衰减)
  const recencyScore = Math.exp(-memory.ageHours / 168); // 168 小时 = 1 周
  
  // 频率：类似内容出现次数
  const frequencyScore = Math.min(1.0, memory.similarCount / 10);
  
  // 相关性：与当前任务/上下文的相关性 (需要向量相似度)
  const relevanceScore = await calculateRelevance(memory, currentContext);
  
  // 用户明确标记
  const userScore = memory.userMarkedImportant ? 1.0 : 0.5;
  
  // 加权平均
  const importance = 
    weights.recency * recencyScore +
    weights.frequency * frequencyScore +
    weights.relevance * relevanceScore +
    weights.userExplicit * userScore;
  
  return Math.min(1.0, importance); // 限制在 0-1
}
```

### 2. 记忆去重

```javascript
async function storeMemoryWithDedup(input) {
  const encoded = await encodeMemory(input);
  
  // 检查是否已存在相似记忆
  const similar = await semanticMemory.search(encoded.content, {
    limit: 1,
    minSimilarity: 0.95, // 95% 相似度视为重复
  });
  
  if (similar.length > 0) {
    // 已存在，跳过存储
    return { stored: false, reason: 'duplicate', existing: similar[0].id };
  }
  
  // 不存在，存储新记忆
  return await storeMemory(input);
}
```

### 3. 记忆检索优化

```javascript
// 使用缓存减少重复检索
const retrievalCache = new LRUCache({
  max: 1000,
  ttl: 1000 * 60 * 5, // 5 分钟
});

async function retrieveMemoryWithCache(query, options) {
  const cacheKey = `${query}:${JSON.stringify(options)}`;
  
  // 检查缓存
  const cached = retrievalCache.get(cacheKey);
  if (cached) {
    return cached;
  }
  
  // 执行检索
  const results = await retrieveMemory(query, options);
  
  // 缓存结果
  retrievalCache.set(cacheKey, results);
  
  return results;
}
```

### 4. 会话记忆注入

```javascript
// 在每次会话开始时注入相关记忆
async function injectMemoryIntoContext(sessionId, task) {
  // 检索相关记忆
  const memories = await retrieveMemory(task.description, {
    limit: 5,
    includeSemantic: true,
    includeEpisodic: true,
    includeWorking: false,
  });
  
  // 构建记忆上下文
  const memoryContext = memories.map(m => 
    `[${m.source}] ${m.content} (重要性：${m.importance.toFixed(2)})`
  ).join('\n');
  
  // 注入到系统提示
  const systemPrompt = `
你正在协助用户完成任务。以下是相关的历史记忆：

${memoryContext}

请利用这些记忆更好地完成任务。如果记忆中有成功的模式，优先采用。
`;
  
  return systemPrompt;
}
```

### 5. 记忆导出/导入

```javascript
// 导出记忆 (用于备份或迁移)
async function exportMemories(options = {}) {
  const {
    namespaces = ['default'],
    format = 'json', // 'json' | 'markdown'
    includeSources = ['working', 'episodic', 'semantic'],
  } = options;
  
  const exportData = {
    exportedAt: new Date().toISOString(),
    namespaces,
    memories: {
      working: includeSources.includes('working') ? 
        await workingMemory.export() : [],
      episodic: includeSources.includes('episodic') ? 
        await episodicMemory.export() : [],
      semantic: includeSources.includes('semantic') ? 
        await semanticMemory.export() : [],
    },
  };
  
  if (format === 'json') {
    return JSON.stringify(exportData, null, 2);
  }
  
  if (format === 'markdown') {
    return formatAsMarkdown(exportData);
  }
}

// 导入记忆 (用于恢复或迁移)
async function importMemories(exportData) {
  const { memories } = exportData;
  
  let imported = 0;
  
  if (memories.working) {
    for (const memory of memories.working) {
      await workingMemory.set(memory.key, memory.data);
      imported++;
    }
  }
  
  if (memories.episodic) {
    await episodicMemory.insertBatch(memories.episodic);
    imported += memories.episodic.length;
  }
  
  if (memories.semantic) {
    await semanticMemory.insertBatch(memories.semantic);
    imported += memories.semantic.length;
  }
  
  return { imported };
}
```

---

## 配置示例

### OpenClaw 配置文件

```yaml
memory:
  # 分层记忆配置
  hierarchical:
    enabled: true
    
    # 工作记忆
    working:
      enabled: true
      max_size_mb: 1
      ttl_minutes: null  # 会话结束清除
    
    # 情景记忆
    episodic:
      enabled: true
      max_size_mb: 100
      storage: sqlite  # 'sqlite' | 'json'
      path: /home/admin/.openclaw/workspace/agents/sovereign/memory/episodic.db
      retention_days: 90
    
    # 语义记忆
    semantic:
      enabled: true
      storage: json  # 'json' | 'sqlite'
      path: /home/admin/.openclaw/workspace/agents/sovereign/memory/semantic.json
      consolidation:
        enabled: true
        interval_hours: 24  # 每天执行一次
        min_age_days: 7
        min_importance: 0.7
  
  # 重要性分数配置
  importance:
    weights:
      recency: 0.2
      frequency: 0.2
      relevance: 0.3
      user_explicit: 0.3
    thresholds:
      working_to_episodic: 0.3
      episodic_to_semantic: 0.7
  
  # 检索配置
  retrieval:
    default_limit: 10
    cache_enabled: true
    cache_ttl_minutes: 5
    min_similarity: 0.7
  
  # 去重配置
  deduplication:
    enabled: true
    similarity_threshold: 0.95
  
  # 日志配置
  logging:
    enabled: true
    path: /home/admin/.openclaw/workspace/logs/memory-access.log
    format: json
```

---

## 参考资源

### RuFlo 原始实现
- 项目地址：https://github.com/ruvnet/ruflo
- AgentDB 文档：https://github.com/ruvnet/ruflo/blob/main/docs/AGENTDB.md
- 记忆架构：https://github.com/ruvnet/ruflo/blob/main/docs/MEMORY_ARCHITECTURE.md

### OpenClaw 相关文件
- 记忆目录：`/home/admin/.openclaw/workspace/agents/sovereign/memory/`
- LONG_TERM_MEMORY.md: `/home/admin/.openclaw/workspace/agents/sovereign/LONG_TERM_MEMORY.md`
- AGENTS.md: `/home/admin/.openclaw/workspace/agents/sovereign/AGENTS.md`

---

## 实施检查清单

### P1 实施 (1 个月)

- [ ] 实现工作记忆层
  - [ ] 内存存储 (LRU Cache)
  - [ ] 大小限制 (1MB)
  - [ ] 会话结束清除
  
- [ ] 实现情景记忆层
  - [ ] SQLite/JSON 存储
  - [ ] 重要性评分
  - [ ] 保留分数计算
  - [ ] 淘汰策略
  
- [ ] 实现语义记忆层
  - [ ] JSON 存储
  - [ ] 永不淘汰
  - [ ] 聚类合并
  
- [ ] 实现记忆巩固
  - [ ] 定期执行 (每天)
  - [ ] 聚类算法
  - [ ] 摘要生成
  
- [ ] 实现记忆检索
  - [ ] 三层联合检索
  - [ ] 相关性排序
  - [ ] 缓存优化
  
- [ ] 实现记忆去重
  - [ ] 相似度计算
  - [ ] 重复检测
  - [ ] 跳过存储

### 测试用例

- [ ] 测试记忆存储流程
- [ ] 测试重要性分数计算
- [ ] 测试记忆检索准确性
- [ ] 测试记忆巩固效果
- [ ] 测试去重机制
- [ ] 测试缓存命中率

---

## 版本历史

| 版本 | 日期 | 变更 |
|------|------|------|
| 1.0 | 2026-03-26 | 初始版本，基于 RuFlo AgentDB v3 记忆系统适配 |

---

**技能作者**: Sovereign (S.V.) 👁️  
**天枢计划**: 猎物 #010 - RuFlo 分层记忆系统适配  
**最后更新**: 2026-03-26 16:55 CST

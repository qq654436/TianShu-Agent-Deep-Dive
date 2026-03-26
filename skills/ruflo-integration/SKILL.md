# RuFlo 适配技能

**技能名称**: ruflo-integration  
**版本**: 1.0.0  
**兼容性**: Aether-Sync v1.2+  
**作者**: Sovereign (S.V.) 👁️  
**来源**: 天枢计划猎物 #010

---

## 🎯 技能目标

将 RuFlo 的核心能力集成到 Aether-Sync，提供:
- SONA 自学习路由
- HNSW 向量记忆
- Agent Booster (WASM)
- Swarm 编排
- 成本优化

---

## 📦 安装

```bash
# 通过 ClawHub 安装
npx clawhub install ruflo-integration

# 或手动安装
git clone https://github.com/aether-sync/tian_shu.git
cp tian_shu/skills/ruflo-integration ~/.openclaw/skills/

# 全局安装 (可选)
npm install -g ruflo@latest
```

---

## 🔧 配置

### 1. 初始化

```bash
# 项目初始化
npx ruflo@latest init

# 完整安装 (MCP + 诊断)
npx ruflo@latest init --full

# Claude Code MCP 集成
claude mcp add ruflo -- npx ruflo@latest mcp start
```

### 2. 配置 LLM Providers

```yaml
# config.yaml
providers:
  - name: claude-sonnet
    api_key: $ANTHROPIC_API_KEY
    model: claude-sonnet-4-5
    priority: 1
  
  - name: gpt-4
    api_key: $OPENAI_API_KEY
    model: gpt-4-turbo
    priority: 2
  
  - name: gemini-pro
    api_key: $GOOGLE_API_KEY
    model: gemini-pro
    priority: 3
  
  - name: ollama
    base_url: http://localhost:11434
    model: llama3
    priority: 4
```

### 3. 记忆配置

```yaml
# config.yaml
memory:
  hnsw:
    enabled: true
    dimensions: 384
    ef_construction: 200
    m: 16
  sqlite:
    path: ./data/agentdb.sqlite
    wal_mode: true
  postgresql:
    enabled: false  # 企业级选项
    url: $DATABASE_URL
```

---

## 🚀 使用

### 基础用法

```bash
# 生成 coding agent
npx ruflo@latest agent spawn -t coder --name my-coder

# 启动 hive-mind swarm
npx ruflo@latest hive-mind spawn "实现用户认证系统"

# 列出可用 Agent
npx ruflo@latest agent list
```

### Claude Code MCP 工具

```bash
# 在 Claude Code 中使用
/swarm_init --objective "开发登录功能" --topology hierarchical
/agent_spawn --type coder --name auth-coder
/memory_search --query "authentication patterns"
/hooks_route --task "fix login bug"
```

### 自学习工作流

```typescript
// 1. LEARN: 搜索相似模式
const patterns = await memory_search({
  query: "task keywords",
  topK: 5
});

// 2. COORD: 初始化 Swarm
const swarm = await swarm_init({
  objective: "Implement feature",
  topology: "hierarchical",
  maxAgents: 6
});

// 3. EXECUTE: Agent 执行工作
// (Codex/Claude 实际执行)

// 4. REMEMBER: 保存成功模式
await memory_store({
  key: "auth-pattern-1",
  value: "JWT refresh token flow",
  namespace: "patterns"
});
```

---

## 🛠️ 工具集

### 259 MCP 工具 (核心子集)

| 类别 | 工具 | 描述 |
|------|------|------|
| **Swarm** | `swarm_init` | 初始化 Agent Swarm |
| | `agent_spawn` | 生成专用 Agent |
| | `hive_spawn` | 启动 Hive Mind |
| **Memory** | `memory_search` | HNSW 向量搜索 |
| | `memory_store` | 存储模式 |
| | `memory_consolidate` | 记忆整合 |
| **Routing** | `hooks_route` | 智能任务路由 |
| | `hooks_progress` | 进度跟踪 |
| | `agentdb_semantic-route` | 语义路由 |
| **Optimization** | `agent_booster` | WASM 代码转换 |
| | `token_optimizer` | Token 压缩 |
| | `get_optimal_config` | 优化配置 |
| **Security** | `ai_defence_scan` | 安全扫描 |
| | `validate_input` | 输入验证 |
| | `detect_injection` | 注入检测 |

### Agent Booster (WASM)

```typescript
// 简单代码转换 (<1ms, $0 成本)
import { AgentBooster } from '@ruflo/booster';

const booster = new AgentBooster();

// var → const
const result = await booster.transform(code, 'var-to-const');

// 添加 TypeScript 类型
const typed = await booster.transform(code, 'add-types');

// 添加错误处理
const safe = await booster.transform(code, 'add-error-handling');
```

### Token Optimizer

```typescript
// 减少 30-50% token 使用
import { getTokenOptimizer } from '@ruflo/integration';

const optimizer = await getTokenOptimizer();

// 压缩 context (32% 减少)
const ctx = await optimizer.getCompactContext("auth patterns");

// 优化编辑 (352x 加速)
await optimizer.optimizedEdit(file, oldStr, newStr, "typescript");

// 获取最优配置
const config = optimizer.getOptimalConfig(agentCount);
```

---

## 🐝 Swarm 编排

### 拓扑类型

```javascript
// Hierarchical (默认，防漂移)
const swarm1 = await swarm_init({
  topology: "hierarchical",
  maxAgents: 6,
  strategy: "specialized"
});

// Mesh (点对点)
const swarm2 = await swarm_init({
  topology: "mesh",
  maxAgents: 8
});

// Ring (环形传递)
const swarm3 = await swarm_init({
  topology: "ring",
  maxAgents: 5
});

// Star (中心辐射)
const swarm4 = await swarm_init({
  topology: "star",
  maxAgents: 10
});
```

### 共识协议

```javascript
// Raft (领导者协调)
const consensus1 = await swarm.consensus("raft");

// Byzantine (容错，f < n/3)
const consensus2 = await swarm.consensus("byzantine");

// Gossip (流行病传播)
const consensus3 = await swarm.consensus("gossip");

// Weighted (Queen 3x 权重)
const consensus4 = await swarm.consensus("weighted");

// Majority (简单多数)
const consensus5 = await swarm.consensus("majority");
```

### 防漂移配置

```javascript
//  ALWAYS 用于编码任务
const antiDriftSwarm = await swarm_init({
  topology: "hierarchical",  // 单一协调器
  maxAgents: 6-8,            // 小团队
  strategy: "specialized",   // 清晰角色
  consensus: "raft",         // 领导者维护状态
  checkpoints: "post-task",  // 频繁检查点
  sharedMemory: true,        // 共享记忆命名空间
  taskCycles: "short"        // 短任务周期
});
```

---

## 🧠 自学习系统

### SONA 路由

```typescript
// SONA 自动学习最佳路由
import { SONARouter } from '@ruflo/sona';

const router = new SONARouter();

// 路由决策 (<0.05ms)
const decision = await router.route({
  task: "fix auth bug",
  context: { complexity: "medium", domain: "security" }
});

// 输出：{ agent: "security-expert", model: "sonnet", estimated_cost: 0.003 }
```

### EWC++ 防遗忘

```typescript
// 保留成功模式，防止灾难性遗忘
import { EWCConsolidator } from '@ruflo/ewc';

const consolidator = new EWCConsolidator();

// 巩固重要记忆
await consolidator.consolidate({
  patterns: successfulPatterns,
  importance_threshold: 0.7
});
```

### HNSW 向量搜索

```typescript
// 子毫秒级检索
import { HNSWSearch } from '@ruflo/hnsw';

const search = new HNSWSearch({
  dimensions: 384,
  ef_construction: 200,
  m: 16
});

// 搜索 (150x-12,500x 加速)
const results = await search.query("authentication patterns", {
  topK: 5,
  threshold: 0.5
});

// 输出：[{ pattern: "JWT flow", score: 0.85, ... }]
```

---

## 💰 成本优化

### 3-Tier 模型路由

| Tier | Handler | 延迟 | 成本 | 用例 |
|------|---------|------|------|------|
| **1** | Agent Booster (WASM) | <1ms | $0 | 简单转换 |
| **2** | Haiku/Sonnet | 500ms-2s | $0.0002-$0.003 | Bug 修复/功能 |
| **3** | Opus | 2-5s | $0.015 | 架构设计 |

```typescript
// 智能路由
import { IntelligentRouter } from '@ruflo/routing';

const router = new IntelligentRouter();

const handler = await router.routeTask({
  task: "convert var to const",
  complexity: "simple"  // → Tier 1 (WASM)
});

const handler2 = await router.routeTask({
  task: "implement OAuth flow",
  complexity: "medium"  // → Tier 2 (Sonnet)
});

const handler3 = await router.routeTask({
  task: "design distributed auth",
  complexity: "complex"  // → Tier 3 (Opus)
});
```

### 节省统计

| 优化 | Token 节省 | 实现 |
|------|-----------|------|
| ReasoningBank 检索 | -32% | 检索相关模式而非全 context |
| Agent Booster 编辑 | -15% | 简单编辑跳过 LLM |
| 缓存 (95% 命中率) | -10% | 重用嵌入和模式 |
| 最优批量大小 | -20% | 分组相关操作 |
| **组合** | **30-50%** | 乘法叠加 |

---

## 🔒 安全

### AIDefence 扫描

```typescript
// <10ms 威胁检测
import { AIDefence } from '@ruflo/security';

const defence = new AIDefence();

const scan = await defence.scan(input, {
  detect_injection: true,
  detect_pii: true,
  detect_jailbreak: true,
  validate_paths: true
});

if (scan.threat_level === "high") {
  await defence.block();
} else if (scan.threat_level === "medium") {
  await defence.sanitize();
}
```

### Claims System

```typescript
// 人类-Agent 工作所有权
import { ClaimsManager } from '@ruflo/claims';

const claims = new ClaimsManager();

// Agent 声明工作
await claims.claim({
  task_id: "auth-feature",
  agent_id: "coder-1",
  ownership: "full"
});

// 人类接管
await claims.handoff({
  task_id: "auth-feature",
  from: "coder-1",
  to: "human-user",
  context: "partial-implementation"
});

// 释放工作
await claims.release({
  task_id: "auth-feature",
  agent_id: "coder-1"
});
```

---

## 📊 性能基准

| 指标 | RuFlo | 基准 |
|------|-------|------|
| **路由延迟** | 0.57ms | 100% 准确率 |
| **HNSW 搜索** | ~61µs | 150x-12,500x 加速 |
| **Agent Booster** | <1ms | 352x 快于 LLM |
| **SONA 适应** | <0.05ms | 自学习路由 |
| **Token 优化** | 30-50% | 成本减少 |
| **API 成本** | -75% | 智能路由 |
| **PostgreSQL QPS** | 16,400 | RuVector |

---

## 🐛 故障排除

### 常见问题

**Q: MCP 工具未加载**
```bash
# 验证 MCP 服务器
claude mcp list
# 重启 MCP
npx ruflo@latest mcp restart
```

**Q: HNSW 搜索慢**
```bash
# 检查索引
npx ruflo@latest memory status
# 重建索引
npx ruflo@latest memory rebuild
```

**Q: Swarm 漂移**
```javascript
// 使用防漂移配置
const swarm = await swarm_init({
  topology: "hierarchical",
  maxAgents: 6,
  anti_drift: true  // 启用防漂移
});
```

---

## 📚 参考

- [RuFlo 官方文档](https://github.com/ruvnet/ruflo)
- [MCP 工具列表](https://github.com/ruvnet/ruflo/blob/main/docs/MCP_TOOLS.md)
- [架构决策记录](https://github.com/ruvnet/ruflo/blob/main/ADRs/)
- [性能基准](https://github.com/ruvnet/ruflo/blob/main/BENCHMARKS.md)
- [Discord 社区](https://discord.com/invite/dfxmpwkG2D)

---

## 🔄 更新日志

### v1.0.0 (2026-03-26)
- 初始版本
- SONA 自学习路由集成
- HNSW 向量记忆
- Agent Booster (WASM)
- Swarm 编排 (4 拓扑 + 5 共识)
- 成本优化 (3-tier 路由)
- Claims System

---

**技能状态**: ✅ 生产就绪  
**最后更新**: 2026-03-26  
**维护者**: Aether-Sync Team

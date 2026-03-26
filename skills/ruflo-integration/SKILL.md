# ruflo-integration SKILL.md

**版本**: 1.0.0  
**适配目标**: OpenClaw Agent (Sovereign)  
**原始项目**: ruvnet/ruflo v3.5  
**天枢计划**: Prey #009

---

## 技能元数据

```yaml
name: ruflo-integration
version: "1.0.0"
description: "Ruflo 多智能体编排平台 OpenClaw 适配技能。提取 Ruflo 核心设计模式，简化为企业级智能体协调器。"
argument-hint: 'ruflo swarm deploy, ruflo agent coordinate, ruflo memory query'
allowed-tools: Bash, Read, Write, Exec, Subagents
homepage: https://github.com/ruvnet/ruflo
repository: https://github.com/ruvnet/ruflo
author: Sovereign (adapted from ruvnet)
license: MIT
```

---

## 核心定位

> "将 Ruflo 的企业级多智能体编排能力简化为 OpenClaw 原生技能，聚焦蜂群协调、记忆系统、性能优化三大核心。"

**不是**: 完整复制 310+ MCP 工具  
**而是**: 提取可复用的设计模式，适配 OpenClaw 架构

---

## 设计原则

1. **简化优先**: Ruflo 100+ 智能体 → OpenClaw 按需子代理
2. **原生集成**: 使用 OpenClaw 工具集 (sessions_spawn, subagents, memory/)
3. **性能导向**: 借鉴 WASM 加速思想，简单任务跳过 LLM
4. **记忆增强**: 整合 Ruflo 向量记忆理念到 LONG_TERM_MEMORY.md

---

## 核心能力

### 1. 蜂群协调器 (Swarm Coordinator)

**Ruflo 原始设计**:
```javascript
swarm_init({
  topology: "hierarchical",
  maxAgents: 8,
  strategy: "specialized",
  consensus: "raft"
})
```

**OpenClaw 适配**:
```bash
# 防漂移蜂群配置
sessions_spawn --task "清晰的任务描述" \
  --mode "session" \
  --label "swarm-worker-1"

# 主代理协调多个子代理，模拟 hierarchical topology
# 使用 subagents steer 进行实时调整
# 使用 subagents kill 终止异常子代理
```

**使用场景**:
- 复杂任务拆分为 6-8 个子代理 (防漂移 maxAgents:8)
- 主代理作为 Queen 协调者
- 子代理作为 Workers 执行专项任务

### 2. 意图解析路由 (Intent Router)

**Ruflo 原始设计**:
```bash
[AGENT_BOOSTER_AVAILABLE] Intent: var-to-const
→ Use Edit tool directly, 352x faster than LLM

[TASK_MODEL_RECOMMENDATION] Use model="haiku"
→ Pass model="haiku" to Task tool for cost savings
```

**OpenClaw 适配**:
```bash
# 执行前解析任务复杂度
# 简单任务 → 直接使用 edit/write (跳过 LLM)
# 中等任务 → 使用经济模型
# 复杂任务 → 使用子代理蜂群
```

**路由决策树**:
```
任务类型判断:
├─ 文件操作 (创建/编辑/删除) → 直接使用 write/edit (0 LLM 调用)
├─ 信息检索 (搜索/查询) → web_fetch/web_search (1 LLM 调用)
├─ 分析任务 (对比/评测) → 子代理蜂群 (3-5 LLM 调用)
└─ 战略决策 (规划/架构) → 主代理 + 董事会汇报 (5+ LLM 调用)
```

### 3. 钩子系统 (Hooks System)

**Ruflo 原始设计**: 27 Hooks (before/after tool, before commit, etc.)

**OpenClaw 适配** (强制钩子):
```markdown
# AGENTS.md 中定义的钩子:
- before_tool: 工具调用前记录日志，风险评估
- after_tool: 工具调用后验证输出，错误捕获
- before_commit: 文件写入前备份原文件
- after_session: 会话结束前归档到 memory/
- on_error: 错误发生时记录 + 通知董事会
```

**增强钩子** (新增):
```bash
# 在关键操作前添加验证步骤
# 示例：删除文件前
if [ -f "$file" ]; then
  cp "$file" "$file.backup"  # before_commit 钩子
  trash "$file"              # 执行操作
  echo "Backed up to $file.backup"  # after_tool 钩子
fi
```

### 4. 记忆系统增强 (Memory Enhancement)

**Ruflo 原始设计**:
- HNSW 向量搜索 (~61µs)
- 知识图谱 PageRank
- 集体记忆 (8 种类型)

**OpenClaw 适配**:
```markdown
# 三层记忆架构 (简化版)

1. 长期记忆: LONG_TERM_MEMORY.md
   - 高效工作流
   - 技术发现
   - 董事会偏好
   - 系统教训

2. 会话记忆: memory/YYYY-MM-DD.md
   - 当日详细日志
   - 关键决策
   - 错误/异常

3. 项目记忆: global_premium/*/PROJECT_PLAN.md
   - 里程碑进度
   - 活跃项目状态
```

**增强建议** (未来):
- 添加向量搜索 (ChromaDB 或类似)
- 实现记忆条目置信度生命周期
- 跨会话记忆关联

### 5. 性能优化 (Performance Optimization)

**Ruflo 原始设计**:
- Agent Booster (WASM): 352x 加速
- Token Optimizer: 30-50% token 减少

**OpenClaw 适配**:
```bash
# 1. 简单任务跳过 LLM
# 文件重命名、移动、删除 → 直接 exec

# 2. 上下文优化
# 使用 context-cleaner 技能
# 读取大文件时使用 offset/limit

# 3. 子代理并行
# 独立任务 → sessions_spawn 并行执行
# 相关任务 → 单个子代理顺序执行
```

---

## 使用指南

### 模式 1: 蜂群部署

```bash
# 部署多智能体蜂群执行复杂任务
ruflo swarm deploy \
  --task "分析 GitHub Trending Top 10 项目" \
  --workers 6 \
  --topology hierarchical \
  --consensus raft

# 内部执行:
# 1. 主代理创建 6 个子代理
# 2. 每个子代理分析 1-2 个项目
# 3. 主代理汇总结果
# 4. 产出综合报告
```

### 模式 2: 意图路由

```bash
# 自动判断任务复杂度并路由
ruflo route \
  --task "删除临时文件" \
  --auto-optimize

# 内部执行:
# 1. 解析任务类型为"简单文件操作"
# 2. 直接使用 exec trash (跳过 LLM)
# 3. 记录日志到 memory/
```

### 模式 3: 记忆查询

```bash
# 查询历史记忆
ruflo memory query \
  --topic "竞争情报" \
  --timeframe "last-30-days"

# 内部执行:
# 1. 搜索 LONG_TERM_MEMORY.md
# 2. 搜索 memory/*.md
# 3. 汇总相关洞察
```

### 模式 4: 钩子验证

```bash
# 执行关键操作前验证
ruflo verify \
  --action "delete" \
  --target "tian_shu/temp/" \
  --backup true

# 内部执行:
# 1. before_tool 钩子：记录意图
# 2. before_commit 钩子：备份目标
# 3. 执行删除
# 4. after_tool 钩子：验证结果
# 5. after_session 钩子：归档日志
```

---

## 配置

### 环境变量

```bash
# ~/.config/ruflo/.env

# 蜂群配置
RUFLO_MAX_AGENTS=8          # 防漂移推荐值
RUFLO_TOPOLOGY=hierarchical # hierarchical 或 mesh
RUFLO_CONSENSUS=raft        # raft/bft/gossip

# 性能优化
RUFLO_SKIP_LLM_SIMPLE=true  # 简单任务跳过 LLM
RUFLO_CONTEXT_LIMIT=50000   # 上下文字符限制

# 记忆系统
RUFLO_MEMORY_DIR=memory/    # 会话记忆目录
RUFLO_LONG_TERM_MEMORY=LONG_TERM_MEMORY.md
```

### OpenClaw 集成

```yaml
# ~/.openclaw/config.yaml

skills:
  ruflo-integration:
    enabled: true
    mode: "simplified"  # simplified 或 full
    hooks:
      before_tool: true
      after_tool: true
      before_commit: true
      after_session: true
      on_error: true
```

---

## 与 Ruflo 原始版本对比

| 功能 | Ruflo 原始 | OpenClaw 适配 | 说明 |
|------|------------|---------------|------|
| 智能体数量 | 100+ 预定义 | 按需生成 | OpenClaw sessions_spawn |
| 共识算法 | 5 种 (Raft/BFT/Gossip 等) | 简化为 Raft | 个人使用无需 BFT |
| 向量搜索 | HNSW (~61µs) | Markdown 文件 | 未来可集成 ChromaDB |
| 知识图谱 | PageRank + 社区检测 | 手动链接 | 未来可集成 Neo4j |
| WASM 加速 | 完整实现 | 理念借鉴 | 简单任务跳过 LLM |
| MCP 工具 | 310+ | 0 (使用 OpenClaw 工具) | 原生集成 |
| 安装复杂度 | 高 (curl + npm) | 低 (技能文件) | OpenClaw 优势 |

---

## 最佳实践

### 1. 防漂移蜂群配置

```bash
#  ALWAYS 使用此配置进行复杂任务
sessions_spawn --task "清晰的任务描述" \
  --mode "session" \
  --label "worker-1"

# 限制子代理数量 ≤8 (防漂移)
# 主代理作为 Queen 协调者
# 使用 subagents steer 实时调整方向
```

### 2. 钩子强制执行

```bash
# 关键操作前后备份
cp "$file" "$file.backup"  # before_commit
# 执行操作
# 验证结果
echo "Completed: $operation"  # after_tool
```

### 3. 记忆更新规范

```markdown
# 每次会话结束前更新 LONG_TERM_MEMORY.md

## 新增发现 (YYYY-MM-DD)
- [高效工作流]: [描述]
- [技术发现]: [描述]
- [系统教训]: [描述]
```

### 4. 意图解析优先

```bash
# 执行任何任务前，先解析:
# 1. 任务类型 (简单/中等/复杂)
# 2. 所需工具 (exec/web_fetch/sessions_spawn)
# 3. 预计 LLM 调用次数
# 4. 是否需要子代理

# 显示解析结果确认理解
```

---

## 故障排除

### 问题 1: 子代理失忆

**症状**: 子代理忘记任务目标  
**原因**: 上下文被截断  
**解决**: 
```bash
# 使用 subagents steer 重新发送任务描述
subagents steer --target "worker-1" \
  --message "继续执行：[任务描述]"
```

### 问题 2: 蜂群漂移

**症状**: 子代理偏离原始目标  
**原因**: 缺少协调器  
**解决**:
```bash
# 限制子代理数量 ≤8
# 主代理定期检查进度 (subagents list)
# 使用 hierarchical topology (主代理作为 Queen)
```

### 问题 3: 记忆过载

**症状**: LONG_TERM_MEMORY.md 过大  
**原因**: 未定期清理  
**解决**:
```bash
# 每月归档旧条目到 memory/archive/
# 保留最近 90 天的详细记录
# 使用 context-cleaner 技能
```

---

## 版本历史

| 版本 | 日期 | 变更 |
|------|------|------|
| 1.0.0 | 2026-03-26 | 初始版本，提取 Ruflo 核心设计模式 |

---

## 参考文档

- [Ruflo 原始项目](https://github.com/ruvnet/ruflo)
- [天枢计划 Prey #009 技术评测](../reports/prey_009_technical_review.md)
- [OpenClaw AGENTS.md](../../AGENTS.md)
- [OpenClaw SOUL.md](../../SOUL.md)

---

**技能维护者**: Sovereign (S.V.) 👁️  
**天枢计划**: Prey #009  
**最后更新**: 2026-03-26 10:20 GMT+8

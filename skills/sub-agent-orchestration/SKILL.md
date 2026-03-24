# sub-agent-orchestration - 子代理编排技能

**版本**: 1.0.0  
**作者**: Sovereign (from Prey #008 Analysis)  
**兼容性**: OpenClaw v1.2+  
**参考架构**: DeerFlow 2.0 Lead Agent + Sub-Agents 模式

---

## 🎯 技能描述

本技能实现 DeerFlow 风格的子代理编排系统，支持 Lead Agent 动态生成 Sub-Agents、上下文隔离、并行执行和结构化结果汇报。适配 OpenClaw 的 `sessions_spawn` 和 `subagents` 工具。

---

## 📋 核心概念

### 角色定义

| 角色 | 职责 | 工具权限 |
|------|------|---------|
| **Lead Agent** | 任务分解 + 结果合成 | 全部工具 + subagents |
| **Sub-Agent** | 执行独立子任务 | 受限工具集 (按需) |

### 上下文隔离

```
┌─────────────────────────────────────────────────────────┐
│                    Lead Agent                            │
│  - 完整上下文 (LONG_TERM_MEMORY + 项目文档)              │
│  - 任务分解逻辑                                          │
│  - 结果合成逻辑                                          │
└─────────────────────────────────────────────────────────┘
         │
         │ spawn (隔离上下文)
         ▼
┌─────────────────────────────────────────────────────────┐
│                   Sub-Agent #1                           │
│  - 仅任务相关上下文                                       │
│  - 看不到 Lead Agent 完整上下文                          │
│  - 看不到其他 Sub-Agent 上下文                           │
└─────────────────────────────────────────────────────────┘
```

---

## 🔧 工具调用规范

### 1. 生成子代理

```bash
sessions_spawn \
  --task "清晰的任务描述 (包含输入 + 输出要求)" \
  --mode "run"|"session" \
  --runtime "subagent"|"acp" \
  --label "可选标签 (用于识别)"
```

**参数说明**:
- `--task`: 必须清晰明确，包含验收标准
- `--mode`: 
  - `run`: 一次性执行 (适合简单任务)
  - `session`: 保持会话 (适合多轮交互)
- `--runtime`: 
  - `subagent`: OpenClaw 子代理 (推荐)
  - `acp`: ACP 运行时 (如需要)
- `--label`: 用于 `subagents list` 识别

### 2. 列出子代理

```bash
subagents action=list
```

**输出示例**:
```
[
  {
    "sessionId": "agent:sovereign:subagent:xxx",
    "label": "daily-prey-0324",
    "status": "running",
    "createdAt": "2026-03-24T04:00:00Z"
  }
]
```

### 3. 调整子代理方向

```bash
subagents action=steer target="<sessionId>" message="新的指令或修正"
```

**使用场景**:
- 任务需求变更
- 发现新信息需要补充
- 纠正错误方向

### 4. 终止异常子代理

```bash
subagents action=kill target="<sessionId>"
```

**使用场景**:
- 子代理陷入死循环
- 任务已不再需要
- 资源回收

### 5. 等待子代理完成

```bash
# 不主动轮询！使用 push-based 机制
# 子代理完成后会自动 announce 结果

# 如需检查状态 (仅用于调试)
subagents action=list
```

---

## 📖 标准工作流

### 工作流 A: 并行研究任务

```
Step 1: Lead Agent 接收复杂任务
        → "分析 5 个 AI Agent 项目的技术架构"

Step 2: 分解为独立子任务
        → Sub-Agent #1: 分析 DeerFlow
        → Sub-Agent #2: 分析 Browser-Use
        → Sub-Agent #3: 分析 Project X
        → Sub-Agent #4: 分析 Project Y
        → Sub-Agent #5: 分析 Project Z

Step 3: 并行生成子代理
        → sessions_spawn --label "prey-analysis-1"
        → sessions_spawn --label "prey-analysis-2"
        → ...

Step 4: 等待所有子代理完成 (push-based)
        → 不主动轮询
        → 子代理自动 announce 结果

Step 5: 合成结果
        → 汇总 5 份报告
        → 生成对比分析
        → 输出最终交付物
```

### 工作流 B: 串行依赖任务

```
Step 1: 子代理 #1 - 数据收集
        → sessions_spawn --task "收集 GitHub Trending Top 10"
        → 等待完成

Step 2: 子代理 #2 - 数据分析 (依赖 #1 输出)
        → sessions_spawn --task "分析 Top 10 项目，输入：<output_from_1>"
        → 等待完成

Step 3: 子代理 #3 - 报告生成 (依赖 #2 输出)
        → sessions_spawn --task "生成技术报告，输入：<output_from_2>"
        → 等待完成

Step 4: Lead Agent 合成最终报告
```

### 工作流 C: 动态扩展任务

```
Step 1: 初始子代理发现新信息
        → Sub-Agent #1: "发现 DeerFlow 有 10 个内置技能"

Step 2: Lead Agent 动态生成新子代理
        → sessions_spawn --task "深度分析 DeerFlow 的 10 个技能"
        → Sub-Agent #2

Step 3: 继续原任务 + 新任务并行
        → Sub-Agent #1 继续原分析
        → Sub-Agent #2 分析技能系统

Step 4: 合成时合并两部分结果
```

---

## 🎨 最佳实践

### 1. 任务描述清晰化

```
✅ 推荐：
--task "抓取 GitHub Trending AI Agent Top 5，输出：仓库名 + 星数 + 今日增长 + 技术栈"

❌ 避免：
--task "分析 GitHub 项目" (太模糊)
```

### 2. 上下文注入最小化

```
✅ 推荐：只注入子任务必需的文件
→ read LONG_TERM_MEMORY.md (前 100 行)
→ read PROJECT_PLAN.md (当前里程碑)

❌ 避免：注入所有项目文件
```

### 3. 使用 Label 标识

```
✅ 推荐：--label "prey-analysis-008"
→ subagents list 时容易识别

❌ 避免：不设置 label
```

### 4. 避免轮询陷阱

```
✅ 推荐：等待子代理自动 announce
→ 信任 push-based 机制

❌ 避免：每 5 秒 subagents list 检查
→ 浪费资源 + 可能触发限流
```

### 5. 错误恢复策略

```
当子代理失败时:
1. 分析失败原因 (查看 announce 的错误信息)
2. 决定：重试 / 调整任务 / 放弃
3. 如重试：修正任务描述后重新 spawn
4. 记录到 memory/ 日志
```

### 6. 结果结构化

```
要求子代理输出结构化结果:
✅ 推荐：
```json
{
  "status": "completed",
  "output": {...},
  "errors": [],
  "nextActions": [...]
}
```

❌ 避免：纯文本无结构
```

---

## ⚠️ 注意事项

### 资源限制
- 单个 Lead Agent 最多同时管理 10 个子代理
- 每个子代理默认超时 30 分钟
- 长任务需设置 `--timeout` 参数

### 上下文管理
- 子代理看不到父代理的完整上下文
- 需要显式传递必要信息
- 避免上下文污染 (隔离是核心优势)

### 成本控制
- 每个子代理独立计费
- 简单任务用 `--mode run` (更便宜)
- 复杂任务用 `--mode session` (更灵活)

### 调试技巧
- 使用 `--label` 标识子代理
- 查看 `subagents list` 状态
- 使用 `subagents steer` 调整方向
- 异常时用 `subagents kill` 终止

---

## 🔗 参考资源

### 外部资源
- [DeerFlow Sub-Agents 架构](https://github.com/bytedance/deer-flow)
- [LangGraph Multi-Agent](https://langchain-ai.github.io/langgraph/)

### 内部资源
- `AGENTS.md` - 子代理规范章节
- `memory/YYYY-MM-DD.md` - 会话日志
- `LONG_TERM_MEMORY.md` - 长期记忆

---

## 🧪 示例任务

### 示例 1: 并行抓取多个网站

```
任务：抓取 5 个 AI 项目文档

Lead Agent 执行:
1. sessions_spawn --task "抓取 DeerFlow 文档" --label "doc-deerflow"
2. sessions_spawn --task "抓取 Browser-Use 文档" --label "doc-browseruse"
3. sessions_spawn --task "抓取 Project X 文档" --label "doc-x"
4. sessions_spawn --task "抓取 Project Y 文档" --label "doc-y"
5. sessions_spawn --task "抓取 Project Z 文档" --label "doc-z"
6. 等待所有子代理 announce 完成
7. 合成 5 份文档为对比报告
```

### 示例 2: 多阶段分析任务

```
任务：深度分析 GitHub Trending Top 10

阶段 1 - 数据收集:
→ sessions_spawn --task "获取 Top 10 仓库基础信息" --label "collect"

阶段 2 - 技术栈分析 (依赖阶段 1):
→ sessions_spawn --task "分析技术栈，输入：<collect_output>" --label "analyze-tech"

阶段 3 - 社区活跃度分析:
→ sessions_spawn --task "分析 star 增长/fork 数/贡献者" --label "analyze-community"

阶段 4 - 报告合成:
→ Lead Agent 汇总阶段 2+3 输出 → 最终报告
```

---

## 📈 与 DeerFlow 的对比

| 特性 | DeerFlow | OpenClaw (本技能) |
|------|----------|------------------|
| Sub-Agent 生成 | ✅ | ✅ (sessions_spawn) |
| 上下文隔离 | ✅ | ✅ (独立 session) |
| 并行执行 | ✅ | ✅ (异步 spawn) |
| 结果汇报 | Push-based | Push-based (announce) |
| 动态扩展 | ✅ | ✅ (steer + 新 spawn) |
| 沙箱隔离 | Docker | Session 隔离 |
| 内存持久化 | ✅ | ✅ (LONG_TERM_MEMORY) |

---

## 📝 版本历史

| 版本 | 日期 | 变更 |
|------|------|------|
| 1.0.0 | 2026-03-24 | 初始版本 (基于 DeerFlow 2.0 分析) |

---

**技能状态**: ✅ 已激活  
**最后测试**: 2026-03-24  
**维护者**: Sovereign Agent

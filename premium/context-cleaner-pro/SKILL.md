---
name: context-cleaner
description: 解决 AI 编程中的"上下文腐烂"问题，通过外部化状态管理和智能上下文注入保持 AI 输出质量稳定。
author: Aegis-1 (TianShu Lab)
version: 1.0.0
homepage: https://github.com/qq654436/TianShu-Agent-Deep-Dive
triggers:
  - "clean context"
  - "reset context"
  - "context rot"
  - "fresh context"
metadata: {"clawdbot":{"emoji":"🧹","requires":{"bins":["node","git"]},"config":{"env":{"CONTEXT_DIR":{"description":"上下文文件存储目录","default":".context","required":false}}}}}
---

# Context Cleaner - 上下文清洁器

**问题**: AI 编程中，随着对话进行，上下文窗口被填充，导致早期重要信息被遗忘，代码质量下降。

**解决方案**: 外部化状态管理 + 智能上下文注入

## 核心概念

### 上下文腐烂 (Context Rot)

```
传统方式:
[对话历史 1] + [对话历史 2] + ... + [当前任务]
→ 上下文窗口填满 → AI 降级行为 → 质量下降 ❌

Context Cleaner 方式:
[CONTEXT.md] + [STATE.md] + [当前任务]
→ 只加载相关上下文 → 质量稳定 ✅
```

## 文件结构

```
.context/
├── CONTEXT.md          # 用户偏好和关键决策
├── STATE.md            # 项目状态追踪
├── ROADMAP.md          # 阶段路线图
└── archives/           # 历史上下文归档
    └── YYYY-MM-DD/
```

## 命令

### 初始化项目上下文

```bash
uv run {baseDir}/scripts/context_cleaner.py init "项目描述"
```

创建 `.context/` 目录和基础文件：
- `CONTEXT.md` - 用户偏好模板
- `STATE.md` - 项目状态追踪
- `ROADMAP.md` - 阶段路线图

### 捕获上下文决策

```bash
uv run {baseDir}/scripts/context_cleaner.py capture "决策描述" --category "api|ui|content|org"
```

将关键决策记录到 `CONTEXT.md`，分类存储。

### 清理上下文

```bash
uv run {baseDir}/scripts/context_cleaner.py clean
```

**执行**:
1. 归档当前上下文到 `archives/`
2. 重置 `STATE.md` 为干净状态
3. 保留 `CONTEXT.md` 中的关键决策
4. 生成摘要报告

### 注入上下文

```bash
uv run {baseDir}/scripts/context_cleaner.py inject --phase 1
```

**执行**:
1. 读取 `CONTEXT.md` 中的相关决策
2. 读取 `STATE.md` 中的当前状态
3. 生成优化的上下文提示
4. 输出到 stdout 或直接注入 AI 会话

### 状态查询

```bash
uv run {baseDir}/scripts/context_cleaner.py status
```

显示：
- 当前上下文大小 (tokens)
- 已记录决策数
- 项目阶段
- 归档历史

## 配置文件

创建 `.context/config.json`:

```json
{
  "maxContextTokens": 50000,
  "autoArchive": true,
  "archiveInterval": "daily",
  "categories": ["api", "ui", "content", "org", "architecture"],
  "aiRuntime": "claude-code"
}
```

## 与 GSD 的区别

| 特性 | GSD | Context Cleaner |
|------|-----|-----------------|
| 定位 | 完整开发流程 | 专注上下文管理 |
| 运行时 | 多平台支持 | OpenClaw 原生 |
| 复杂度 | 重 (完整工作流) | 轻 (单一功能) |
| 集成 | 独立工具 | 可嵌入现有流程 |

## 使用场景

### 场景 1: 长对话质量下降

```bash
# 对话进行到第 20 轮，AI 开始输出质量下降
uv run scripts/context_cleaner.py clean

# AI 获得"新鲜"上下文，质量恢复
```

### 场景 2: 多阶段项目

```bash
# 完成阶段 1，准备进入阶段 2
uv run scripts/context_cleaner.py capture "阶段 1 完成，使用 JWT 认证" --category architecture
uv run scripts/context_cleaner.py inject --phase 2

# 阶段 2 继承阶段 1 的关键决策，但不继承对话历史
```

### 场景 3: 项目暂停后恢复

```bash
# 一周后恢复项目
uv run scripts/context_cleaner.py status
uv run scripts/context_cleaner.py inject --phase 2

# 快速恢复上下文，无需重新阅读所有历史对话
```

## API

### Python 库使用

```python
from context_cleaner import ContextCleaner

cleaner = ContextCleaner(context_dir=".context")

# 初始化
cleaner.init("My AI Project")

# 捕获决策
cleaner.capture("使用 PostgreSQL", category="architecture")
cleaner.capture("API 响应使用 JSON:API 格式", category="api")

# 清理并归档
summary = cleaner.clean()
print(summary)

# 注入上下文
context = cleaner.inject(phase=2)
print(context)
```

## 输出格式

### CONTEXT.md 示例

```markdown
# 项目上下文

## 架构决策
- [x] 使用 PostgreSQL 作为主数据库
- [x] API 响应遵循 JSON:API 格式
- [ ] 考虑 Redis 缓存 (待决定)

## UI 偏好
- 布局：卡片式，密度适中
- 交互：点击反馈 < 100ms
- 空状态：显示引导性插图

## API 规范
- 响应格式：JSON:API
- 错误处理：统一错误码 + 人类可读消息
- 认证：JWT + refresh token 轮换
```

### STATE.md 示例

```markdown
# 项目状态

**当前阶段**: 2/4
**最后更新**: 2026-03-20 08:45

## 已完成
- [x] 阶段 1: 用户模型 + 认证
- [x] 阶段 2: 产品模型

## 进行中
- [ ] 阶段 3: 订单 API

## 待办
- [ ] 阶段 4: 结账 UI

## 关键指标
- 总任务数：12
- 已完成：8
- 原子提交数：8
```

## 集成 OpenClaw

### 作为子代理指令

```yaml
# 在 sessions_spawn 时注入
task: "实现订单 API"
context: |
  {{context_cleaner.inject(phase=3)}}
```

### 作为中间件钩子

```python
# before_tool 钩子
def before_tool(tool_name, params):
    if token_count() > MAX_CONTEXT_TOKENS:
        context_cleaner.clean()
```

## 付费版本功能 (Pro)

- ✅ 自动上下文监控 (超过阈值自动清理)
- ✅ 多项目上下文管理
- ✅ 团队协作 (共享 CONTEXT.md)
- ✅ AI 运行时插件 (Claude Code / Cursor / Windsurf)
- ✅ 上下文压缩 (LLM 自动摘要历史决策)

## 许可证

MIT License - 个人免费，商业使用请联系 TianShu Lab

---

**作者**: Aegis-1 @ TianShu Lab  
**版本**: 1.0.0  
**GitHub**: https://github.com/qq654436/TianShu-Agent-Deep-Dive

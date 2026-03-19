# 技术评测报告：jarrodwatts/claude-hud
**天枢计划 | 猎物 #002**  
**评测日期**: 2026-03-19  
**评测引擎**: Qwen-Coder (dashscope-coding/qwen3.5-plus)  
**合规状态**: ✅ 技术客观中立，无广告倾向

---

## 📋 项目概览

| 指标 | 数值 |
|------|------|
| **仓库** | [jarrodwatts/claude-hud](https://github.com/jarrodwatts/claude-hud) |
| **作者** | Jarrod Watts |
| **24h Stars** | 1,038 |
| **Total Stars** | 7,419 |
| **许可证** | MIT |
| **定位** | Claude Code 实时状态显示插件 (Statusline HUD) |

---

## 🏗️ 核心架构拆解

### 1. 设计哲学

**核心理念**: 将 Claude Code 的内部状态 (上下文、工具、子代理、待办事项) 实时可视化，始终显示在终端输入下方。

**核心价值主张**:
```
┌─────────────────────────────────────────────────────────┐
│                    CLAUDE HUD                            │
├─────────────────────────────────────────────────────────┤
│  "Always visible below your input"                       │
│                                                          │
│  问题：Claude Code 运行时是"黑盒"，用户不知道：           │
│  - 上下文还剩多少？                                       │
│  - 子代理在做什么？                                       │
│  - 工具调用了什么？                                       │
│                                                          │
│  解决：原生 statusline API → 实时 JSON 解析 → 终端渲染    │
└─────────────────────────────────────────────────────────┘
```

### 2. 技术架构

**数据流**:
```
Claude Code 
    ↓ (stdin JSON + transcript JSONL)
claude-hud (Node.js/Bun)
    ↓ (解析 transcript，提取工具/代理/待办事件)
stdout (ANSI 终端渲染)
    ↓
终端状态行 (每 300ms 刷新)
```

**核心组件**:
| 组件 | 功能 | 技术实现 |
|------|------|---------|
| **Context Monitor** | 上下文使用率监控 | 原生 token 数据，非估算 |
| **Usage Tracker** | API 配额消耗追踪 | Anthropic OAuth API (Pro/Max/Team) |
| **Tool Activity** | 工具调用实时显示 | 解析 transcript JSONL |
| **Agent Tracker** | 子代理状态追踪 | 解析 agent spawn/complete 事件 |
| **Todo Progress** | 待办事项进度 | 解析 todo add/complete 事件 |
| **Git Status** | Git 分支/变更显示 | 调用 git 命令 |

### 3. 显示层级

**默认 2 行**:
```
[Opus | Max] │ my-project git:(main*)
Context █████░░░░░ 45% │ Usage ██░░░░░░░░ 25% (1h 30m / 5h)
```

**可选扩展行** (通过配置启用):
```
◐ Edit: auth.ts | ✓ Read ×3 | ✓ Grep ×2        ← Tools activity
◐ explore [haiku]: Finding auth code (2m 15s)    ← Agent status
▸ Fix authentication bug (2/5)                   ← Todo progress
```

### 4. 配置系统

**配置方式**:
1. 交互式：`/claude-hud:configure` (引导式配置)
2. 手动编辑：`~/.claude/plugins/claude-hud/config.json`

**核心配置项** (30+ 选项):
```json
{
  "lineLayout": "expanded",           // expanded | compact
  "pathLevels": 2,                    // 1-3 级目录显示
  "gitStatus": {
    "enabled": true,
    "showDirty": true,                // * 标记未提交变更
    "showAheadBehind": true,          // ↑N ↓N 远程同步状态
    "showFileStats": true             // !M +A ✘D ?U 文件统计
  },
  "display": {
    "showContextBar": true,           // 上下文进度条
    "showUsage": true,                // API 配额显示
    "showTools": false,               // 工具活动行
    "showAgents": false,              // 子代理状态行
    "showTodos": false                // 待办进度行
  },
  "colors": {
    "context": "green",               // green→yellow→red 渐变
    "usage": "brightBlue",
    "warning": "yellow",
    "critical": "red"
  }
}
```

---

## 🔍 技术亮点分析

### ✅ 创新点

1. **原生 statusline API 集成**
   - 无需独立窗口或 tmux
   - 任意终端兼容
   - 无侵入式设计

2. **实时 JSONL 流解析**
   - 每 300ms 刷新
   - 解析 Claude Code transcript
   - 提取工具/代理/待办事件

3. **上下文健康预警**
   - 进度条颜色渐变 (绿→黄→红)
   - 85%+ 高负载时显示 token 明细
   - 支持 1M 上下文窗口

4. **配额感知显示**
   - Pro/Max/Team 用户显示 5h/1h 配额
   - 7 日使用率阈值告警 (默认 80%)
   - API 用户自动隐藏 (按量付费无配额限制)

5. **Git 深度集成**
   - 分支名称 + 脏标记 (*)
   - 远程同步状态 (↑N ↓N)
   - 文件变更统计 (!M +A ✘D ?U)

### ⚠️ 潜在局限

1. **平台依赖**: 仅支持 Claude Code (Anthropic 官方 CLI)
2. **订阅限制**: Usage 显示仅限 Pro/Max/Team 用户
3. **Linux 问题**: /tmp tmpfs 导致 EXDEV 错误 (需设置 TMPDIR)
4. **功能边界**: 仅显示状态，不控制桌面/自动化操作

---

## 📐 OpenClaw 适配可行性

### 高适配性组件

| 组件 | 适配难度 | 说明 |
|------|---------|------|
| 状态行渲染 | ⭐⭐ 中 | 可适配 Feishu/Telegram 消息格式 |
| JSONL 流解析 | ⭐⭐ 中 | OpenClaw 已有 transcript 处理机制 |
| 上下文监控 | ⭐ 低 | 可直接使用 session_status 工具 |
| Git 状态显示 | ⭐ 低 | exec 调用 git 命令即可 |
| 配置系统 | ⭐⭐ 中 | 可复用 config.json 模式 |

### 需改造组件

| 组件 | 改造点 |
|------|-------|
| Claude Code statusline API | 替换为 OpenClaw message/channel API |
| 终端 ANSI 渲染 | 替换为 Markdown/富文本格式 |
| Anthropic OAuth API | 替换为 OpenClaw usage 追踪 |
| Node.js 运行时 | 可保持，或改写为 Python/Shell |

### 核心洞察：**"桌面自动化控制"的真相**

⚠️ **重要发现**: claude-hud **不是**桌面自动化工具，而是**终端状态显示插件**。

用户提到的"桌面自动化控制"可能源于误解。claude-hud 的核心能力是:
- ✅ **状态可视化** - 显示 Claude Code 内部状态
- ✅ **实时监控** - 工具/代理/待办事项追踪
- ❌ **桌面控制** - 不控制鼠标/键盘/窗口
- ❌ **自动化执行** - 不自动执行任务

**真正的"桌面自动化"对标项目**:
- [computer-use](https://github.com/anthropics/anthropic-recipes/tree/master/computer-use) - Anthropic 官方
- [open-interpreter](https://github.com/OpenInterpreter/open-interpreter) - 代码执行
- [AIGUI](https://github.com/AIGUI/AIGUI) - GUI 自动化

---

## 🎯 适配建议

### OpenClaw "状态中心"技能 (建议命名：`status-hud`)

**第一阶段 (本周)**:
1. 创建 `status-hud` 技能 - 会话状态可视化
2. 集成 `session_status` 工具输出
3. Feishu 富文本卡片渲染

**第二阶段 (本月)**:
1. 子代理追踪 - 集成 `subagents list`
2. 工具活动日志 - 解析 sessions_history
3. 周期性状态推送 - cron 任务

**第三阶段 (Q2)**:
1. 跨平台适配 (Telegram/Discord/WhatsApp)
2. 实时 WebSocket 推送 (如支持)
3. 自定义告警阈值

---

## 📊 技术评分

| 维度 | 评分 | 说明 |
|------|------|------|
| **架构设计** | 8/10 | 简洁高效，关注点清晰 |
| **可复用性** | 6/10 | 强绑定 Claude Code，核心思路可迁移 |
| **文档质量** | 9/10 | 配置选项详尽，示例丰富 |
| **社区活跃** | 7/10 | 7k stars，作者活跃维护 |
| **适配 OpenClaw** | 5/10 | 需大量改造，核心思路有价值 |

**综合评分**: 7.0/10 ⭐⭐⭐

---

## 🔖 结论

**jarrodwatts/claude-hud** 是一个优秀的 Claude Code 状态显示插件，核心价值在于**实时可视化**而非"桌面自动化控制"。

**对 OpenClaw 的战略价值**:
- 状态可视化设计理念可借鉴
- 配置系统 (预设 + 手动) 值得参考
- Git 深度集成思路可复用

**建议行动**:
1. 创建 OpenClaw 版 `status-hud` 技能
2. 优先实现上下文监控 + 子代理追踪
3. Feishu 富文本卡片作为首发出力

**备注**: 如航哥需要真正的"桌面自动化控制"能力，建议锁定下一猎物为 computer-use 或 open-interpreter 类项目。

---

**评测完成时间**: 2026-03-19 12:35 CST  
**下次观测**: 2026-03-20 09:00 CST (猎物 #003: langchain-ai/open-swe)

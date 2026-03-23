# OpenClaw 适配技能: session-hud

**灵感来源**: claude-hud (GitHub Trending #004)  
**适配日期**: 2026-03-21  
**状态**: 📋 待实现

---

## 🎯 技能目标

为 OpenClaw 会话提供实时状态 HUD，显示:
- 当前模型/使用率
- 工具调用计数
- 子 Agent 状态
- 会话时长
- 上下文健康度

---

## 📐 架构设计

### 数据流
```
OpenClaw Session → sessions_status → session-hud → Canvas/终端输出
                        ↘ sessions_list/sessions_history
```

### 实现方式
```javascript
// 伪代码示例
async function renderSessionHUD() {
  const status = await session_status();
  const sessions = await sessions_list({ limit: 5 });
  
  return `
╭────────────────────────────────────────────────────────────╮
│  [${status.model}] │ sovereign │ ${status.uptime}          │
├────────────────────────────────────────────────────────────┤
│  Context █████░░░░░ ${status.contextPercent}%              │
│  Tools  ████░░░░░░░░ ${status.toolCalls}/100              │
│  Cost   ██░░░░░░░░░░ $${status.cost}                       │
├────────────────────────────────────────────────────────────┤
│  ◐ subagent-1: GitHub Trending 抓取 (2m 15s)              │
│  ◐ subagent-2: 等待中                                      │
│  ▸ 猎物 #004 拆解 (2/4 完成)                               │
╰────────────────────────────────────────────────────────────╯
  `;
}
```

---

## 🔧 配置项

```json
{
  "refreshInterval": 5000,
  "outputTarget": "canvas|terminal|feishu",
  "elements": {
    "showModel": true,
    "showContextBar": true,
    "showToolCalls": true,
    "showCost": true,
    "showSubagents": true,
    "showTodos": true
  },
  "thresholds": {
    "contextWarning": 70,
    "contextCritical": 90,
    "toolCallsWarning": 80
  },
  "colors": {
    "context": "green",
    "warning": "yellow",
    "critical": "red"
  }
}
```

---

## 📋 实现步骤

### Step 1: 创建技能骨架
```bash
mkdir -p ~/.openclaw/workspace/agents/sovereign/skills/session-hud
cd ~/.openclaw/workspace/agents/sovereign/skills/session-hud
```

### Step 2: 编写 SKILL.md
```markdown
# session-hud - OpenClaw 会话状态 HUD

**触发**: `/hud` 或自动启用

**功能**:
- 实时显示会话状态
- 工具调用计数
- 子 Agent 追踪
- 成本/使用率监控

**配置**: 编辑 `config.json`
```

### Step 3: 实现核心逻辑 (index.js)
```javascript
const { session_status, sessions_list, subagents } = require('@openclaw/tools');

async function renderHUD(config) {
  // 获取会话状态
  const status = await session_status();
  
  // 获取子 Agent 列表
  const agents = await subagents({ action: 'list' });
  
  // 渲染 HUD
  return formatHUD(status, agents, config);
}

function formatHUD(status, agents, config) {
  // 格式化输出 (支持 Canvas/终端/飞书)
  // ...
}

module.exports = { renderHUD };
```

### Step 4: 注册技能
在 OpenClaw 配置中添加:
```yaml
skills:
  - session-hud
```

### Step 5: 测试验证
```bash
openclaw session --command "/hud"
```

---

## 🎨 UI 预设

### Full (默认)
```
╭────────────────────────────────────────────────────────────╮
│  [qwen3.5-plus] │ sovereign │ ⏱️ 15m 32s                  │
├────────────────────────────────────────────────────────────┤
│  Context ████████░░ 80% │ Usage ██░░░░░░ 25%              │
│  Tools  ████████░░ 82/100 │ Cost $0.42                     │
├────────────────────────────────────────────────────────────┤
│  ◐ subagent-1: GitHub 抓取 (2m 15s)                        │
│  ✓ subagent-2: 报告生成 (完成)                             │
│  ▸ 猎物 #004 拆解 (3/4) │ 🔥 紧急                           │
╰────────────────────────────────────────────────────────────╯
```

### Essential
```
[Opus] │ sovereign │ Context ████░░░░░░ 45% │ Tools 42/100
◐ subagent-1: 运行中 (2m)
```

### Minimal
```
[qwen3.5-plus] │ Context █████░░░░░ 50%
```

---

## 🔄 与 claude-hud 对比

| 特性 | claude-hud | session-hud (OpenClaw) |
|------|------------|------------------------|
| 数据源 | Claude Code stdin JSON | sessions_status API |
| 更新频率 | ~300ms | 5s (可配置) |
| 输出目标 | 终端 statusLine | Canvas/终端/飞书 |
| 子 Agent | 显示名称/状态 | 显示名称/状态/任务 |
| 成本显示 | Usage API (Pro/Max) | session_status cost |
| 配置方式 | /claude-hud:configure | config.json + /hud:setup |
| 扩展性 | 插件系统 | 技能系统 |

---

## 🚀 扩展方向

### 短期
- [ ] 基础 HUD 渲染 (终端输出)
- [ ] config.json 配置支持
- [ ] /hud:setup 交互配置

### 中期
- [ ] Canvas 集成 (图形化 HUD)
- [ ] 飞书卡片推送
- [ ] 历史趋势图表

### 长期
- [ ] 多会话对比视图
- [ ] 告警通知 (阈值触发)
- [ ] 性能分析 (瓶颈识别)

---

## 📝 注意事项

1. **API 限制**: sessions_status 调用频率不宜过高 (建议 ≥5s)
2. **隐私**: 成本数据可选隐藏 (display.showCost: false)
3. **兼容性**: 支持 OpenClaw v1.0+
4. **依赖**: 无外部依赖 (仅使用内置 tools)

---

**创建者**: Sovereign (S.V.) 👁️  
**许可证**: MIT (与 claude-hud 一致)  
**GitHub**: 待发布

# OpenClaw Skill: sovereign-status

**技能名称**: sovereign-status  
**版本**: 1.0.0  
**作者**: Sovereign (S.V.) 👁️  
**灵感来源**: jarrodwatts/claude-hud  
**创建日期**: 2026-03-20

---

## 📖 技能描述

为 OpenClaw Agent 提供实时状态监控能力，包括：
- Token 使用率监控
- 子代理状态追踪
- 任务进度可视化
- Git 工作区状态

---

## 🎯 使用场景

1. **长任务执行**: 监控长时间运行的任务进度
2. **多子代理协作**: 追踪并行子代理状态
3. **Token 管理**: 避免上下文窗口超限
4. **工作区同步**: 实时查看 Git 变更

---

## 🚀 安装方法

```bash
# 通过 ClawHub 安装 (推荐)
clawhub install sovereign-status

# 或手动安装
git clone https://github.com/aether-sync/sovereign-status \
  ~/.openclaw/workspace/agents/sovereign/skills/sovereign-status
```

---

## 📋 命令列表

### `/status` - 查看当前状态

```bash
# 基础状态
/status

# 详细模式
/status --verbose

# JSON 输出
/status --json
```

**输出示例**:
```
[Opus] │ sovereign git:(main*)
Context █████░░░░░ 45% │ Session ⏱️ 1h 30m

◐ Read: LONG_TERM_MEMORY.md | ✓ Exec ×3 | ✓ Write ×2
◐ subagent-001: 猎物 -004-拆解 (进行中 15m)
▸ 完成猎物抓取 (2/5)
```

### `/configure` - 配置状态显示

```bash
# 交互式配置
/sovereign-configure

# 或直接编辑配置文件
~/.openclaw/workspace/agents/sovereign/status-config.json
```

### `/watch` - 持续监控模式

```bash
# 启动监控 (每 5 秒刷新)
/watch

# 自定义刷新间隔
/watch --interval 2

# 停止监控
/watch --stop
```

---

## ⚙️ 配置选项

### 配置文件: `status-config.json`

```json
{
  "lineLayout": "expanded",
  "elementOrder": ["model", "context", "session", "tools", "agents", "todos"],
  "gitStatus": {
    "enabled": true,
    "showDirty": true,
    "showAheadBehind": false,
    "showFileStats": false
  },
  "display": {
    "showModel": true,
    "showContextBar": true,
    "contextValue": "percent",
    "showSessionName": true,
    "showDuration": true,
    "showTools": true,
    "showAgents": true,
    "showTodos": true
  },
  "colors": {
    "context": "green",
    "warning": "yellow",
    "critical": "red"
  },
  "thresholds": {
    "contextWarning": 70,
    "contextCritical": 90
  },
  "refreshIntervalMs": 5000
}
```

### 配置项说明

| 选项 | 类型 | 默认值 | 说明 |
|------|------|--------|------|
| `lineLayout` | string | "expanded" | 布局：expanded(多行) / compact(单行) |
| `elementOrder` | array | [...] | 元素显示顺序 |
| `gitStatus.enabled` | boolean | true | 启用 Git 状态 |
| `gitStatus.showDirty` | boolean | true | 显示未提交变更 |
| `display.showContextBar` | boolean | true | 显示上下文进度条 |
| `display.contextValue` | string | "percent" | 上下文显示：percent/tokens/remaining |
| `display.showDuration` | boolean | true | 显示会话时长 |
| `thresholds.contextWarning` | number | 70 | 上下文警告阈值 (%) |
| `refreshIntervalMs` | number | 5000 | 刷新间隔 (毫秒) |

---

## 🔧 技术实现

### 架构

```
┌─────────────────────────────────────────────────────────┐
│                  OpenClaw Agent                          │
│  (主 Agent / 子代理)                                     │
└─────────────────────┬───────────────────────────────────┘
                      │
                      ▼
┌─────────────────────────────────────────────────────────┐
│              sovereign-status (本技能)                   │
│  - 监听 tool_call 事件                                   │
│  - 追踪子代理生命周期                                    │
│  - 计算 token 使用率                                      │
│  - 查询 Git 状态                                          │
└─────────────────────┬───────────────────────────────────┘
                      │
                      ▼
┌─────────────────────────────────────────────────────────┐
│                 输出层                                   │
│  - 终端状态线 (PTY)                                      │
│  - Feishu/Telegram 通知                                 │
│  - 日志文件归档                                          │
└─────────────────────────────────────────────────────────┘
```

### 核心模块

#### 1. Token 追踪器
```javascript
// 伪代码示例
class TokenTracker {
  constructor() {
    this.totalTokens = 0;
    this.inputTokens = 0;
    this.outputTokens = 0;
  }

  update(usage) {
    this.inputTokens += usage.input_tokens;
    this.outputTokens += usage.output_tokens;
    this.totalTokens = this.inputTokens + this.outputTokens;
  }

  getUsagePercent(contextLimit = 200000) {
    return (this.totalTokens / contextLimit) * 100;
  }
}
```

#### 2. 子代理监控器
```javascript
class SubagentMonitor {
  constructor() {
    this.activeSubagents = new Map();
  }

  onSpawn(id, task) {
    this.activeSubagents.set(id, {
      task,
      startedAt: Date.now(),
      status: 'running'
    });
  }

  onComplete(id, result) {
    const agent = this.activeSubagents.get(id);
    agent.status = 'completed';
    agent.duration = Date.now() - agent.startedAt;
  }

  getStatus() {
    return Array.from(this.activeSubagents.values())
      .filter(a => a.status === 'running');
  }
}
```

#### 3. Git 状态查询
```bash
# 获取 Git 状态
git status --porcelain --branch

# 解析输出
## main...origin/main [ahead 2, behind 1]
 M file1.js
?? newfile.txt
```

---

## 📊 输出格式

###  expanded 模式 (默认)

```
[Opus] │ sovereign git:(main*)
Context █████░░░░░ 45% │ Session ⏱️ 1h 30m

◐ Read: LONG_TERM_MEMORY.md | ✓ Exec ×3 | ✓ Write ×2
◐ subagent-001: 猎物 -004-拆解 (进行中 15m)
▸ 完成猎物抓取 (2/5)
```

### compact 模式

```
[Opus] │ sovereign │ Context 45% │ ⏱️ 1h 30m │ ◐ 2 agents │ ▸ 2/5
```

### 颜色编码

| 颜色 | 含义 |
|------|------|
| 🟢 Green | 正常 (<70% 上下文) |
| 🟡 Yellow | 警告 (70-90% 上下文) |
| 🔴 Red | 临界 (>90% 上下文) |

---

## 🔌 API 集成

### 事件订阅

```javascript
// 在技能中订阅事件
events.on('tool_call', (tool) => {
  statusTracker.recordTool(tool);
});

events.on('subagent_spawn', (agent) => {
  statusTracker.recordSubagent(agent);
});

events.on('token_usage', (usage) => {
  statusTracker.updateTokens(usage);
});
```

### Webhook 通知

```json
// POST /webhook/status-update
{
  "event": "context_warning",
  "data": {
    "currentPercent": 75,
    "threshold": 70,
    "tokensUsed": 150000,
    "tokensLimit": 200000
  }
}
```

---

## ⚠️ 注意事项

1. **性能影响**: 监控模式每 5 秒刷新，可能轻微影响性能
2. **Token 计算**: 基于 API 返回，可能有 1-2 次调用延迟
3. **Git 状态**: 仅在工作区为 Git 仓库时有效
4. **终端兼容**: 需要支持 ANSI 颜色的终端

---

## 🐛 故障排除

### 状态不更新

```bash
# 检查技能是否加载
openclaw skills list | grep sovereign-status

# 重启 Agent
openclaw agent restart
```

### Git 状态缺失

```bash
# 确认在 Git 仓库内
git status

# 检查配置
cat ~/.openclaw/workspace/agents/sovereign/status-config.json | grep gitStatus
```

### 颜色显示异常

```bash
# 检查终端支持
echo $TERM

# 应输出：xterm-256color 或类似
# 如输出 dumb，需配置终端
```

---

## 📈 版本历史

| 版本 | 日期 | 变更 |
|------|------|------|
| 1.0.0 | 2026-03-20 | 初始版本 |

---

## 📝 开发指南

### 本地开发

```bash
cd ~/.openclaw/workspace/agents/sovereign/skills/sovereign-status
npm install
npm run dev
```

### 测试

```bash
npm test
npm run test:coverage
```

### 发布

```bash
clawhub publish ./sovereign-status
```

---

## 📄 许可证

MIT License - 与 claude-hud 保持一致

---

## 🔗 参考

- 灵感来源：https://github.com/jarrodwatts/claude-hud
- OpenClaw 技能规范：/opt/openclaw/skills/skill-creator/SKILL.md
- ClawHub 发布指南：/opt/openclaw/skills/clawhub/SKILL.md

---

**维护者**: Sovereign (S.V.) 👁️  
**联系**: Feishu @Sovereign  
**状态**: 🟢 Active

# 猎物 #006: claude-hud 深度拆解

**日期**: 2026-03-22  
**猎物**: claude-hud by @jarrodwatts  
**来源**: GitHub Trending #1 (今日 +970⭐)  
**拆解者**: Sovereign (S.V.) 👁️

---

## 📊 项目概览

| 指标 | 数值 |
|------|------|
| **GitHub Stars** | 10,596 (+970 today) |
| **Forks** | 452 |
| **语言** | JavaScript/TypeScript |
| **许可证** | MIT |
| **类别** | Claude Code Plugin |
| **核心功能** | 实时会话监控 HUD |

**项目链接**: https://github.com/jarrodwatts/claude-hud

---

## 🎯 核心价值主张

> "A Claude Code plugin that shows what's happening — context usage, active tools, running agents, and todo progress. Always visible below your input."

**解决的问题**:
- 开发者不知道 Claude Code 会话中发生了什么
- 上下文窗口使用率不透明
- 子代理活动不可见
- Todo 进度难以追踪

---

## 🔧 技术架构

### 工作原理

```
┌─────────────────────────────────────────────────────────┐
│                    Claude Code Session                   │
│                                                          │
│  User Input → Claude → Tool Execution → Response        │
│       ↓                                                  │
│  stdin JSON (transcript)                                 │
│       ↓                                                  │
│  ┌─────────────────────────────────────────────────┐    │
│  │              claude-hud Parser                   │    │
│  │  - Parse transcript JSONL                        │    │
│  │  - Extract tool calls                            │    │
│  │  - Track agent status                            │    │
│  │  - Monitor context tokens                        │    │
│  └─────────────────────────────────────────────────┘    │
│       ↓                                                  │
│  stdout → statusLine API → Terminal Display             │
│                                                          │
└─────────────────────────────────────────────────────────┘
```

### 核心模块

| 模块 | 职责 | 技术 |
|------|------|------|
| **Transcript Parser** | 解析 Claude Code JSONL 输出 | Node.js |
| **Context Monitor** | 追踪 token 使用量 | Anthropic API |
| **Tool Tracker** | 记录工具调用 (Read/Edit/Grep) | Regex + JSON parsing |
| **Agent Tracker** | 监控子代理状态 | Transcript analysis |
| **Todo Parser** | 提取任务进度 | Markdown parsing |
| **StatusLine Renderer** | 终端 UI 渲染 | ANSI escape codes |

### 数据流

1. Claude Code 输出 transcript JSONL 到 stdin
2. claude-hud 实时解析每一行
3. 提取关键指标 (context, tools, agents, todos)
4. 通过 statusLine API 渲染到终端底部
5. 更新频率 ~300ms

---

## 🎨 用户界面

### 显示内容 (可配置)

**Line 1 — 项目信息**:
```
[Opus] │ my-project git:(main*)
```
- 模型名称
- 项目路径 (1-3 级目录)
- Git 分支 + 脏状态指示

**Line 2 — 资源监控**:
```
Context █████░░░░░ 45% │ Usage ██░░░░░░░░ 25% (1h 30m / 5h)
```
- 上下文窗口使用率 (可视化条)
- 7 日用量百分比 (Pro/Max/Team 订阅)
- 会话时长

**Line 3+ — 活动追踪**:
```
◐ Edit: auth.ts | ✓ Read ×3 | ✓ Grep ×2
◐ explore [haiku]: Finding auth code (2m 15s)
▸ Fix authentication bug (2/5)
```
- 工具活动 (Read/Edit/Grep)
- 子代理状态
- Todo 进度

### 预设模式

| 预设 | 显示内容 | 适用场景 |
|------|---------|---------|
| **Full** | 全部元素 | 深度调试 |
| **Essential** | 活动行 + Git | 日常开发 |
| **Minimal** | 仅模型名 + 上下文条 | 简洁模式 |

---

## 🔑 核心功能详解

### 1. 上下文监控

**特性**:
- 直接从 Claude Code 获取原生 token 数据 (非估算)
- 支持 1M 上下文窗口
- 可视化进度条 (绿→黄→红)
- 可配置阈值告警

**配置项**:
```json
{
  "display.showContextBar": true,
  "display.contextValue": "percent",  // percent | tokens | remaining
  "colors.context": "green",
  "colors.warning": "yellow",
  "colors.critical": "red"
}
```

### 2. 用量追踪 (Pro/Max/Team)

**特性**:
- 显示 5 小时/月 用量限制消耗
- 7 日用量百分比 (超过 80% 阈值显示)
- OAuth 认证 (非 API Key)
- 智能缓存 (TTL 60s)

**限制**:
- ❌ 不适用于 API 用户 (按 token 付费)
- ❌ 不适用于 AWS Bedrock
- ❌ 自定义 API 端点不显示

### 3. 工具活动追踪

**追踪内容**:
- Read 文件次数
- Edit 文件 (显示文件名)
- Grep 搜索次数
- Shell 命令执行

**实现**:
```javascript
// 解析 transcript JSONL
{
  "type": "tool_use",
  "name": "Edit",
  "input": {"file_path": "auth.ts", ...}
}
```

### 4. 子代理监控

**显示内容**:
- 子代理名称 (如 `explore`)
- 当前任务描述
- 运行时长
- 使用模型 (如 `haiku`)

### 5. Todo 进度

**解析规则**:
- 识别 Markdown checkbox: `- [ ]` / `- [x]`
- 计算完成百分比
- 实时更新显示

---

## 🆚 竞争对比: claude-hud vs Aether-Sync

| 维度 | claude-hud | Aether-Sync (ours) |
|------|-----------|-------------------|
| **监控粒度** | 实时 (300ms) | 会话级 |
| **时间跨度** | 单次会话 | 跨会话追踪 |
| **核心功能** | HUD 显示 | 进度管理 + 异常检测 |
| **数据持久化** | ❌ 无 | ✅ memory/ 归档 |
| **异常检测** | ❌ 无 | ✅ 4 条规则自动告警 |
| **会话交接** | ❌ 无 | ✅ 手递手文档生成 |
| **可靠性监控** | ❌ 无 | ✅ 漂移检测 + 幻觉标记 |
| **配置复杂度** | 中 (JSON 配置) | 低 (CLI 命令) |
| **订阅要求** | Pro/Max/Team (用量显示) | 无限制 |

### 定位差异

**claude-hud**: "我在当前会话中做了什么?" (实时可见性)

**Aether-Sync**: "我在这个项目中进展如何? 有没有偏离轨道?" (长期可靠性)

### 互补机会

1. **集成可能性**: claude-hud 做实时显示, Aether-Sync 做会话归档
2. **市场教育**: claude-hud 验证了监控需求, 我们承接深度用户
3. **差异化**: 强调跨会话追踪 + 异常检测 (他们不做)

---

## 💡 技术亮点

### 1. Native StatusLine API

- 直接集成 Claude Code 原生 API
- 无需单独窗口/tmux
- 任何终端都支持

### 2. 智能缓存策略

```json
{
  "usage.cacheTtlSeconds": 60,      // 成功响应缓存 60s
  "usage.failureCacheTtlSeconds": 15 // 失败响应缓存 15s
}
```

### 3. 渐进式配置

- 首次设置: 向导式选择预设
- 高级定制: 直接编辑 config.json
- 配置预览: 保存前实时预览效果

### 4. Git 深度集成

```
gitStatus.showDirty: true       // * 指示未提交
gitStatus.showAheadBehind: true // ↑N ↓N 远程对比
gitStatus.showFileStats: true   // !M +A ✘D ?U 文件统计
```

---

## 📈 增长分析

### Star 增长

| 时间 | Stars | 日增 |
|------|-------|------|
| 发布日 | ~5,000 | - |
| 2026-03-21 | ~9,600 | +4,600 |
| 2026-03-22 (今日) | 10,596 | +970 |

**增长驱动**:
1. ✅ Claude Code 插件市场上线
2. ✅ Reddit/HN 社区传播
3. ✅ 解决了明确痛点 (上下文不透明)
4. ✅ 低门槛安装 (2 步命令)

### 市场验证

**4,407+ GitHub reactions** on AGENTS.md issue (Anthropic #6235) 证明:
- ✅ 开发者需要会话可见性
- ✅ 上下文监控是核心需求
- ✅ 市场愿意为工具付费

---

## 🎯 商业洞察

### 成功因素

1. **时机正确**: Claude Code 爆发期, 生态工具稀缺
2. **痛点精准**: "不知道 Claude 在干什么" 是普遍抱怨
3. **安装简单**: `/plugin install` 2 步完成
4. **免费开源**: MIT 许可, 快速获客
5. **视觉冲击**: HUD 效果适合社交媒体传播

### 变现潜力

| 模式 | 可行性 | 说明 |
|------|-------|------|
| **Pro 功能** | 🔴 低 | 核心功能已免费 |
| **Team 版** | 🟡 中 | 团队仪表盘/共享配置 |
| **SaaS 托管** | 🟡 中 | 跨会话分析/历史归档 |
| **企业定制** | 🟢 高 | 私有部署 + 审计日志 |

**推测**: 作者可能通过咨询/定制变现, 而非 SaaS

---

## ⚠️ 局限性

### 技术限制

1. **仅限 Claude Code**: 不支持其他 AI 编程助手
2. **订阅墙**: 用量显示需 Pro/Max/Team
3. **无持久化**: 会话结束数据丢失
4. **无异常检测**: 只显示数据, 不分析模式
5. **无跨会话**: 无法追踪长期项目进展

### 用户体验

1. **配置复杂**: 高级定制需编辑 JSON
2. **Linux 问题**: /tmp 文件系统导致安装失败 (需 workaround)
3. **终端兼容**: 部分终端可能渲染异常

---

## 🚀 我们的机会

### 差异化定位

| 功能 | claude-hud | Aether-Sync | 优先级 |
|------|-----------|-------------|--------|
| 实时 HUD | ✅ | ❌ | - |
| 跨会话追踪 | ❌ | ✅ | 🔥 HIGH |
| 异常检测 | ❌ | ✅ | 🔥 HIGH |
| 会话手递手 | ❌ | ✅ | HIGH |
| 漂移检测 | ❌ | ✅ | HIGH |
| 幻觉标记 | ❌ | ✅ | MEDIUM |
| 自动归档 | ❌ | ✅ | HIGH |
| Git 集成 | ✅ | ✅ | - |

### 市场策略

**短期 (1-2 周)**:
1. ✅ 强调"claude-hud 做实时, 我们做长期"
2. ✅ 在 claude-hud 讨论区提及互补性
3. ✅ 发布对比博客: "Real-time vs Long-term Monitoring"

**中期 (1 个月)**:
1. 开发 claude-hud 集成插件 (读取他们的数据, 归档到我们的 memory/)
2. 推出"最佳实践": claude-hud + progress-tracker 组合

**长期 (Q2 2026)**:
1. 开发自己的实时 HUD (可选)
2. 收购/合作可能性

---

## 📝 技术借鉴

### 可复用的设计

1. **配置预设模式** (Full/Essential/Minimal)
   - 降低新手门槛
   - 保留高级定制空间

2. **智能缓存策略**
   - 成功/失败分别缓存
   - 指数退避重试

3. **渐进式配置**
   - 向导式首次设置
   - 配置文件直接编辑

4. **可视化反馈**
   - 进度条 (█████░░░░░)
   - 颜色编码 (绿/黄/红)

### 应避免的问题

1. ❌ Linux 安装问题 (tmpfs 限制)
2. ❌ 配置不生效时无明确错误提示
3. ❌ 依赖特定订阅等级 (用量显示)

---

## 🎯 行动建议

### 立即执行 (本周)

- [ ] 发布对比博客: "claude-hud vs Aether-Sync: 实时 vs 长期"
- [ ] 在 claude-hud GitHub Discussions 提及互补性
- [ ] 更新 README: 添加"与 claude-hud 配合使用"章节

### 短期 (2 周)

- [ ] 开发 claude-hud 数据导入器 (解析他们的 transcript)
- [ ] 推出组合使用教程
- [ ] 联系作者探讨合作

### 中期 (1 个月)

- [ ] 评估开发自有 HUD 的必要性
- [ ] 调研用户是否愿意为实时显示付费
- [ ] 规划 v1.3.0: 可选实时显示模块

---

## 📊 评分

| 维度 | 评分 | 说明 |
|------|------|------|
| **技术创新** | ⭐⭐⭐ | 巧妙利用 statusLine API |
| **用户体验** | ⭐⭐⭐⭐ | 直观, 但配置复杂 |
| **市场时机** | ⭐⭐⭐⭐⭐ | 完美踩中 Claude Code 爆发 |
| **增长潜力** | ⭐⭐⭐⭐ | 已验证, 但天花板明显 |
| **商业价值** | ⭐⭐⭐ | 免费模式, 变现路径模糊 |
| **学习价值** | ⭐⭐⭐⭐⭐ | 大量可借鉴设计 |

**综合评分**: ⭐⭐⭐⭐ (4/5)

---

## 🔗 参考资料

- **GitHub**: https://github.com/jarrodwatts/claude-hud
- **Claude Code Plugin Market**: `/plugin marketplace add jarrodwatts/claude-hud`
- **Anthropic Research**: https://www.anthropic.com/engineering/effective-harnesses-for-long-running-agents
- **我们的 Progress Tracker**: https://github.com/qq654436/long-running-harness

---

**拆解完成**: 2026-03-22 13:00 CST  
**拆解者**: Sovereign (S.V.) 👁️  
**下一步**: CEO 晨报整合 + 市场策略调整

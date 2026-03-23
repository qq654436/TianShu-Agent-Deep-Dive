# 猎物 #004 技术评测报告

**执行日期**: 2026-03-21  
**猎物来源**: GitHub Trending Top 2  
**拆解执行**: Sovereign (S.V.) 👁️

---

## 🎯 猎物概览

| 项目 | Stars | 今日增长 | 语言 | 相关性 |
|------|-------|---------|------|--------|
| [claude-hud](https://github.com/jarrodwatts/claude-hud) | 9,528 | +1,068 | JavaScript | 🔥 CLI 监控插件 |
| [open-swe](https://github.com/langchain-ai/open-swe) | 7,633 | +635 | Python | 🔥 企业编码 Agent |

---

## 📊 猎物 #1: claude-hud

### 核心价值
Claude Code 插件，实时显示会话状态：
- 上下文使用率 (原生 token 数据)
- 活跃工具监控 (Read/Edit/Grep)
- 子 Agent 追踪
- Todo 进度可视化

### 技术架构
```
Claude Code → stdin JSON → claude-hud → stdout → Terminal HUD
                    ↘ transcript JSONL (tools, agents, todos)
```

### 关键特性
| 特性 | 实现方式 | 价值 |
|------|---------|------|
| 原生 Token 数据 | Claude Code statusLine API | 精准，非估算 |
| 实时更新 | ~300ms 轮询 | 低延迟感知 |
| 可配置布局 | config.json + /claude-hud:configure | 灵活适配 |
| Git 状态集成 | 分支/变更/远程同步 | 开发上下文 |

### 配置系统
```json
{
  "lineLayout": "expanded",
  "pathLevels": 2,
  "elementOrder": ["project", "tools", "context", "usage"],
  "gitStatus": { "enabled": true, "showDirty": true },
  "display": { "showTools": true, "showAgents": true },
  "colors": { "context": "cyan", "usage": "brightBlue" }
}
```

### 可复用设计
1. **statusLine API 集成** → OpenClaw 可借鉴用于 Canvas/终端输出
2. **transcript 解析器** → 可用于 sessions_list/sessions_history 可视化
3. **配置引导流程** → /claude-hud:configure 交互模式

### 局限/改进点
- 仅支持 Claude Pro/Max/Team (Usage API 限制)
- Linux TMPDIR 问题需手动修复
- 无远程会话支持 (纯本地)

---

## 📊 猎物 #2: open-swe

### 核心价值
LangChain 出品的企业级异步编码 Agent 框架，复刻 Stripe/Ramp/Coinbase 内部 Agent 架构。

### 技术架构
```
┌─────────────────────────────────────────────────────────┐
│                    Open SWE Core                         │
├─────────────────────────────────────────────────────────┤
│  Deep Agents Framework (LangGraph)                      │
│  ├── Main Agent (claude-opus-4-6)                       │
│  ├── Subagents (task tool spawning)                     │
│  └── Middleware Hooks                                   │
│        ├── check_message_queue_before_model             │
│        ├── open_pr_if_needed                            │
│        └── ToolErrorMiddleware                          │
├─────────────────────────────────────────────────────────┤
│  Sandbox Providers (Pluggable)                          │
│  ├── Modal │ Daytona │ Runloop │ LangSmith │ Custom    │
├─────────────────────────────────────────────────────────┤
│  Invocation Surfaces                                    │
│  ├── Slack (@mentions)                                  │
│  ├── Linear (@openswe comments)                         │
│  └── GitHub (PR review responses)                       │
└─────────────────────────────────────────────────────────┘
```

### 核心设计原则
| 原则 | 实现 |
|------|------|
| **Isolate first** | 每任务独立云沙箱，完全隔离 |
| **Tool curation > quantity** | ~15 个精选工具，非 500+ |
| **Context injection** | AGENTS.md + Issue/Thread 全文 |
| **Deterministic hooks** | 中间件确保关键步骤执行 |
| **Async messaging** | 任务中可发送 follow-up 消息 |

### 工具集 (~15 个)
| 工具 | 用途 |
|------|------|
| execute | 沙箱内 Shell 命令 |
| fetch_url | 网页抓取 (Markdown) |
| http_request | API 调用 |
| commit_and_open_pr | Git 提交 + 创建 Draft PR |
| linear_comment | Linear 评论回复 |
| slack_thread_reply | Slack 线程回复 |
| read_file, write_file, edit_file | 文件操作 |
| task | 子 Agent 生成 |

### 中间件系统
```python
middleware=[
    ToolErrorMiddleware(),           # 工具错误捕获
    check_message_queue_before_model, # 注入中途消息
    open_pr_if_needed                # PR 安全网
]
```

### 与 OpenClaw 对比
| 维度 | OpenClaw | Open SWE | 差距分析 |
|------|----------|----------|----------|
| **运行时** | sessions_spawn (本地) | 云沙箱 (Modal/Daytona) | 我们缺云沙箱 |
| **触发器** | Feishu/Telegram/Cron | Slack/Linear/GitHub | 他们更 Dev 工具链 |
| **子 Agent** | subagents list/steer/kill | task tool + 独立沙箱 | 架构相似 |
| **中间件** | 无 (依赖 AGENTS.md) | 确定性中间件钩子 | 我们需补充 |
| **上下文** | SOUL/AGENTS/USER.md | AGENTS.md + Issue | 我们更丰富 |
| **安全网** | 人工审核 | open_pr_if_needed | 我们需自动化 |

### 可复用设计
1. **AGENTS.md 规范** → 与我们现有 AGENTS.md 高度一致，验证我们的方向
2. **中间件钩子模式** → before_tool/after_tool 可参考实现
3. **沙箱抽象层** → 可考虑集成 Modal/Runloop 作为 exec 后端
4. **多触发器路由** → Slack/Linear/GitHub → 我们可扩展 GitHub Issues 触发

---

## 🔍 高价值项目识别

### claude-hud 评分
| 标准 | 符合 | 说明 |
|------|------|------|
| GitHub Stars > 10k | ❌ (9.5k) | 接近阈值，增长快 |
| 解决明确痛点 | ✅ | CLI Agent 可观测性 |
| 技术架构可复用 | ✅ | statusLine + transcript 解析 |
| 许可证友好 | ✅ | MIT |
| 文档完善 | ✅ | 详尽配置指南 |

**符合度**: 4/5 ⭐⭐⭐⭐

### open-swe 评分
| 标准 | 符合 | 说明 |
|------|------|------|
| GitHub Stars > 10k | ❌ (7.6k) | 新项目，增长潜力大 |
| 解决明确痛点 | ✅ | 企业 Agent 落地框架 |
| 技术架构可复用 | ✅ | 中间件 + 沙箱 + 多触发器 |
| 许可证友好 | ✅ | MIT |
| 文档完善 | ✅ | INSTALLATION + CUSTOMIZATION |

**符合度**: 4/5 ⭐⭐⭐⭐

---

## 💡 OpenClaw 行动项

### 短期 (本周)
1. ✅ **实现 statusLine 式输出** → Canvas/终端会话状态实时显示
2. ⏳ **中间件钩子原型** → before_tool/after_tool 日志 + 验证
3. ⏳ **AGENTS.md 对齐** → 确认我们的规范与 open-swe 一致

### 中期 (本月)
1. ⏳ **云沙箱集成** → Modal/Runloop POC
2. ⏳ **GitHub Issues 触发器** → @sovereign 提及自动响应
3. ⏳ **子 Agent 沙箱隔离** → 每子任务独立工作目录

### 长期 (本季度)
1. ⏳ **多触发器统一路由** → Feishu/Telegram/GitHub/Slack
2. ⏳ **确定性安全网** → 关键步骤自动回滚/重试
3. ⏳ **企业部署包** → 对标 open-swe 的 INSTALLATION.md

---

## 📈 竞争情报

### claude-hud 威胁等级: 🟡 中
- **定位**: Claude Code 生态插件
- **与我们关系**: 互补 (他们做 CLI 监控，我们做全渠道 Agent)
- **学习点**: 用户体验细节 (配置引导/实时反馈)

### open-swe 威胁等级: 🟠 高
- **定位**: 企业 Agent 框架 (直接竞对)
- **优势**: LangChain 背书 + 云沙箱 + 多触发器
- **劣势**: 仅支持英语生态 (Slack/Linear)
- **我们的差异化**: 
  - 中国本地化 (飞书/钉钉/微信)
  - 更轻量的本地部署
  - SOUL.md 人格化 Agent

---

**拆解完成**: 2026-03-21 08:45  
**下一步**: 生成 OpenClaw 适配技能 + 架构图 + 分发内容

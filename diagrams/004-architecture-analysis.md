# 猎物 #004 架构图

**生成日期**: 2026-03-21  
**工具**: Mermaid  
**来源**: claude-hud + open-swe 架构分析

---

## 📊 claude-hud 架构

```mermaid
flowchart TB
    subgraph Claude_Code["Claude Code CLI"]
        CC[Claude Session]
        SL[statusLine API]
        TJ[transcript JSONL]
    end
    
    subgraph claude_hud["claude-hud Plugin"]
        Parser[Transcript Parser]
        Renderer[HUD Renderer]
        Config[config.json]
    end
    
    subgraph Output["Terminal Output"]
        HUD[Real-time HUD Display]
    end
    
    CC -->|stdin JSON| Parser
    TJ -->|tools/agents/todos| Parser
    SL -->|context/usage| Renderer
    
    Parser -->|parsed data| Renderer
    Config -->|layout/colors| Renderer
    
    Renderer -->|stdout ~300ms| HUD
    
    style claude_hud fill:#e1f5ff,stroke:#0066cc,stroke-width:2px
    style HUD fill:#d4edda,stroke:#28a745,stroke-width:2px
```

---

## 📊 open-swe 架构

```mermaid
flowchart TB
    subgraph Triggers["Invocation Surfaces"]
        Slack[Slack @mentions]
        Linear[Linear @openswe]
        GitHub[GitHub PR Comments]
    end
    
    subgraph Router["Thread Router"]
        ID[Deterministic Thread ID]
        Queue[Message Queue]
    end
    
    subgraph Core["Open SWE Core"]
        DA[Deep Agents Framework]
        Main[Main Agent<br/>claude-opus-4-6]
        Sub[Subagents<br/>task tool]
        MW[Middleware Hooks]
    end
    
    subgraph Sandbox["Sandbox Providers"]
        Modal[Modal]
        Daytona[Daytona]
        Runloop[Runloop]
        Custom[Custom]
    end
    
    subgraph Tools["Tool Set ~15"]
        Exec[execute]
        Fetch[fetch_url]
        HTTP[http_request]
        PR[commit_and_open_pr]
        File[read/write/edit_file]
    end
    
    subgraph Context["Context Injection"]
        AGENTS[AGENTS.md]
        Issue[Issue/Thread Full Text]
    end
    
    Slack --> ID
    Linear --> ID
    GitHub --> ID
    
    ID --> Queue
    Queue --> Main
    
    Main -->|spawn| Sub
    Main -->|tool calls| Tools
    
    MW -->|before/after| Main
    
    DA -->|backend| Sandbox
    Tools -->|execute in| Sandbox
    
    AGENTS -->|system prompt| Main
    Issue -->|context| Main
    
    style Core fill:#e1f5ff,stroke:#0066cc,stroke-width:2px
    style Sandbox fill:#fff3cd,stroke:#ffc107,stroke-width:2px
    style MW fill:#d4edda,stroke:#28a745,stroke-width:2px
```

---

## 📊 OpenClaw 当前架构

```mermaid
flowchart TB
    subgraph Triggers["触发器"]
        Feishu[Feishu @提及]
        Telegram[Telegram /命令]
        Cron[周期性任务]
    end
    
    subgraph Core["Sovereign Core"]
        SOUL[SOUL.md<br/>人格定义]
        AGENTS[AGENTS.md<br/>行为规范]
        USER[USER.md<br/>董事会信息]
        Main[主 Agent<br/>qwen3.5-plus]
    end
    
    subgraph Memory["记忆系统"]
        LTM[LONG_TERM_MEMORY.md]
        Daily[memory/YYYY-MM-DD.md]
        Heartbeat[HEARTBEAT.md]
    end
    
    subgraph Tools["工具集"]
        Files[read/write/edit]
        Exec[exec/process]
        Sessions[sessions_*]
        Subagents[subagents]
        Web[web_fetch/web_search]
        FeishuTools[feishu_*]
    end
    
    subgraph Output["输出"]
        Reply[会话回复]
        Message[message 推送]
        Files_Out[文件写入]
    end
    
    Feishu --> Main
    Telegram --> Main
    Cron --> Main
    
    SOUL -.->|注入 | Main
    AGENTS -.->|注入 | Main
    USER -.->|注入 | Main
    
    LTM -.->|按需加载 | Main
    Daily -.->|按需加载 | Main
    
    Main -->|调用 | Tools
    Main -->|生成 | Output
    
    style Core fill:#e1f5ff,stroke:#0066cc,stroke-width:2px
    style Memory fill:#f8f9fa,stroke:#6c757d,stroke-width:2px
    style Output fill:#d4edda,stroke:#28a745,stroke-width:2px
```

---

## 📊 OpenClaw 目标架构 (融合 claude-hud + open-swe)

```mermaid
flowchart TB
    subgraph Triggers["多触发器"]
        Feishu[Feishu]
        Telegram[Telegram]
        GitHub[GitHub Issues]
        Cron[Cron]
    end
    
    subgraph Router["智能路由"]
        ThreadID[Thread ID 路由]
        Queue[消息队列]
        HUD[Session HUD<br/>实时监控]
    end
    
    subgraph Core["增强核心"]
        SOUL[SOUL.md]
        AGENTS[AGENTS.md]
        Main[主 Agent]
        Sub[子 Agent 池]
        MW[中间件钩子<br/>before_tool/after_tool]
    end
    
    subgraph Sandbox["沙箱隔离"]
        Local[本地 workspace]
        Cloud[云沙箱<br/>Modal/Runloop POC]
    end
    
    subgraph Memory["增强记忆"]
        LTM[LONG_TERM_MEMORY.md]
        Daily[memory/]
        Skills[技能学习库]
    end
    
    subgraph Safety["安全网"]
        Validation[执行前验证]
        Rollback[自动回滚]
        Alert[异常告警]
    end
    
    Feishu --> ThreadID
    Telegram --> ThreadID
    GitHub --> ThreadID
    Cron --> ThreadID
    
    ThreadID --> Queue
    Queue --> Main
    Queue --> HUD
    
    Main -->|middleware| MW
    Main -->|spawn| Sub
    
    MW -->|验证 | Sandbox
    Main -->|调用 | Sandbox
    
    Safety -.->|监控 | Main
    Safety -.->|监控 | Sub
    
    style Core fill:#e1f5ff,stroke:#0066cc,stroke-width:2px
    style HUD fill:#d4edda,stroke:#28a745,stroke-width:2px
    style MW fill:#fff3cd,stroke:#ffc107,stroke-width:2px
    style Safety fill:#f8d7da,stroke:#dc3545,stroke-width:2px
```

---

## 🔑 架构演进关键点

| 阶段 | 目标 | 关键组件 |
|------|------|----------|
| **当前** | 基础 Agent 功能 | SOUL/AGENTS/USER + tools |
| **短期** | 可观测性增强 | Session HUD + 中间件钩子 |
| **中期** | 沙箱隔离 | 云沙箱 POC + 子 Agent 隔离 |
| **长期** | 企业级框架 | 多触发器 + 安全网 + 自动回滚 |

---

**生成者**: Sovereign (S.V.) 👁️  
**格式**: Mermaid (GitHub/Feishu 原生支持)

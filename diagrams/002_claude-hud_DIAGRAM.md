# 猎物 #002: jarrodwatts/claude-hud - 架构流程图

**天枢计划 | Mermaid 文本架构图**  
**创建日期**: 2026-03-19  
**原项目**: [jarrodwatts/claude-hud](https://github.com/jarrodwatts/claude-hud)

---

## 🏗️ 核心架构总览

```mermaid
flowchart TB
    subgraph HUD["Claude HUD 架构"]
        direction TB
        
        CC[Claude Code CLI] -->|stdin JSON + transcript JSONL| PARSE[claude-hud 解析器]
        PARSE -->|每 300ms 刷新 | RENDER[终端渲染引擎]
        RENDER -->|ANSI 转义序列 | TERM[终端状态行]
        
        style HUD fill:#e8f5e9,stroke:#2e7d32,stroke-width:2px
        style CC fill:#fff,stroke:#333,stroke-width:1px
        style PARSE fill:#2196f3,stroke:#1565c0,stroke-width:1px,color:#fff
        style RENDER fill:#9c27b0,stroke:#7b1fa2,stroke-width:1px,color:#fff
        style TERM fill:#4caf50,stroke:#2e7d32,stroke-width:2px,color:#fff
    end
```

---

## 📊 数据流架构

```mermaid
sequenceDiagram
    participant CC as Claude Code
    participant HUD as claude-hud
    participant CONFIG as config.json
    participant TERM as 终端
    
    CC->>HUD: stdout JSON (transcript)
    HUD->>HUD: 解析 JSONL 流
    HUD->>CONFIG: 读取显示配置
    CONFIG-->>HUD: 返回启用项
    
    alt 上下文监控启用
        HUD->>HUD: 提取 token 使用率
    end
    
    alt 工具活动启用
        HUD->>HUD: 提取 tool call 事件
    end
    
    alt 子代理追踪启用
        HUD->>HUD: 提取 agent spawn/complete
    end
    
    alt 待办进度启用
        HUD->>HUD: 提取 todo add/complete
    end
    
    HUD->>TERM: 渲染状态行 (ANSI)
    TERM->>TERM: 每 300ms 刷新
```

---

## 🎛️ 核心组件架构

```mermaid
flowchart TB
    subgraph COMPONENTS["核心组件"]
        direction TB
        
        CTX[Context Monitor<br/>上下文使用率监控]
        USAGE[Usage Tracker<br/>API 配额消耗追踪]
        TOOL[Tool Activity<br/>工具调用实时显示]
        AGENT[Agent Tracker<br/>子代理状态追踪]
        TODO[Todo Progress<br/>待办事项进度]
        GIT[Git Status<br/>分支/变更显示]
    end
    
    INPUT[transcript JSONL] --> PARSER{事件解析器}
    PARSER -->|context 事件 | CTX
    PARSER -->|usage 事件 | USAGE
    PARSER -->|tool 事件 | TOOL
    PARSER -->|agent 事件 | AGENT
    PARSER -->|todo 事件 | TODO
    PARSER -->|git 命令 | GIT
    
    CTX --> MERGE[状态合并]
    USAGE --> MERGE
    TOOL --> MERGE
    AGENT --> MERGE
    TODO --> MERGE
    GIT --> MERGE
    
    MERGE --> RENDER[ANSI 渲染]
    RENDER --> OUTPUT[终端状态行]
    
    style COMPONENTS fill:#fce4ec,stroke:#c2185b,stroke-width:2px
    style INPUT fill:#fff,stroke:#333,stroke-width:1px
    style PARSER fill:#ffeb3b,stroke:#333,stroke-width:2px
    style MERGE fill:#2196f3,stroke:#1565c0,stroke-width:1px,color:#fff
    style RENDER fill:#9c27b0,stroke:#7b1fa2,stroke-width:1px,color:#fff
    style OUTPUT fill:#4caf50,stroke:#2e7d32,stroke-width:2px,color:#fff
```

---

## 🎨 显示层级配置

```mermaid
flowchart LR
    subgraph LAYOUT["显示层级"]
        direction TB
        
        L1[默认 2 行]
        L2[可选扩展行]
    end
    
    L1 --> L1A["[Opus | Max] │ my-project git:(main*)"]
    L1 --> L1B["Context █████░░░░░ 45% │ Usage ██░░░░░░░░ 25%"]
    
    L2 --> L2A["◐ Edit: auth.ts | ✓ Read ×3 | ✓ Grep ×2<br/>← Tools activity"]
    L2 --> L2B["◐ explore [haiku]: Finding auth code (2m 15s)<br/>← Agent status"]
    L2 --> L2C["▸ Fix authentication bug (2/5)<br/>← Todo progress"]
    
    style LAYOUT fill:#e3f2fd,stroke:#1565c0,stroke-width:2px
    style L1 fill:#bbdefb,stroke:#1565c0,stroke-width:1px
    style L2 fill:#e1bee7,stroke:#7b1fa2,stroke-width:1px
```

---

## ⚙️ 配置系统架构

```mermaid
flowchart TB
    subgraph CONFIG["配置系统"]
        direction TB
        
        INTERACT[交互式配置<br/>/claude-hud:configure]
        MANUAL[手动编辑<br/>~/.claude/plugins/claude-hud/config.json]
    end
    
    USER[用户] -->|选择 | INTERACT
    USER -->|选择 | MANUAL
    
    INTERACT --> WIZARD[引导式配置向导]
    MANUAL --> EDITOR[文本编辑器]
    
    WIZARD --> JSON[config.json]
    EDITOR --> JSON
    
    JSON --> VALIDATE{配置验证}
    VALIDATE -->|有效 | APPLY[应用配置]
    VALIDATE -->|无效 | ERROR[显示错误]
    ERROR --> USER
    
    APPLY --> RELOAD[热重载配置]
    RELOAD --> HUD[HUD 显示更新]
    
    style CONFIG fill:#fff8e1,stroke:#f57f17,stroke-width:2px
    style USER fill:#fff,stroke:#333,stroke-width:1px
    style JSON fill:#ffecb3,stroke:#f57f17,stroke-width:1px
    style VALIDATE fill:#ffeb3b,stroke:#333,stroke-width:2px
    style APPLY fill:#4caf50,stroke:#2e7d32,stroke-width:1px,color:#fff
```

---

## 🔍 上下文健康预警机制

```mermaid
flowchart LR
    CTX[上下文使用率] --> CHECK{使用率阈值？}
    
    CHECK -->|0-70% | GREEN[🟢 绿色<br/>正常状态]
    CHECK -->|70-85% | YELLOW[🟡 黄色<br/>注意警告]
    CHECK -->|85-100% | RED[🔴 红色<br/>高负载]
    CHECK -->|100%+ | CRITICAL[⚠️ 临界<br/>显示 token 明细]
    
    GREEN --> DISPLAY[进度条显示]
    YELLOW --> DISPLAY
    RED --> DISPLAY
    CRITICAL --> DETAIL[显示 token 明细]
    DETAIL --> DISPLAY
    
    style CTX fill:#fff,stroke:#333,stroke-width:1px
    style CHECK fill:#ffeb3b,stroke:#333,stroke-width:2px
    style GREEN fill:#4caf50,stroke:#2e7d32,stroke-width:1px,color:#fff
    style YELLOW fill:#ffeb3b,stroke:#f57f17,stroke-width:1px
    style RED fill:#f44336,stroke:#c62828,stroke-width:1px,color:#fff
    style CRITICAL fill:#9c27b0,stroke:#7b1fa2,stroke-width:1px,color:#fff
    style DISPLAY fill:#2196f3,stroke:#1565c0,stroke-width:1px,color:#fff
```

---

## 📐 OpenClaw 适配路线图

```mermaid
gantt
    title OpenClaw "status-hud" 技能适配阶段
    dateFormat  YYYY-MM-DD
    section 第一阶段 (本周)
    创建 status-hud 技能框架     :done,    frame, 2026-03-19, 1d
    集成 session_status 工具     :active,  status, 2026-03-19, 1d
    Feishu 富文本卡片渲染       :         feishu, after status, 2d
    
    section 第二阶段 (本月)
    子代理追踪集成              :         sub, after feishu, 3d
    工具活动日志解析            :         tool, after feishu, 3d
    周期性状态推送 (cron)        :         cron, after sub, 2d
    
    section 第三阶段 (Q2)
    跨平台适配 (Telegram/Discord) :         cross, after cron, 5d
    实时 WebSocket 推送          :         ws, after cron, 7d
    自定义告警阈值              :         alert, after cross, 3d
```

---

## 🎯 核心洞察

```mermaid
mindmap
  root((claude-hud 真相))
    核心能力
      状态可视化
      实时监控
    非能力
      桌面控制
      自动化执行
    真正对标
      computer-use
      open-interpreter
      AIGUI
    OpenClaw 借鉴
      状态行设计理念
      配置系统模式
      Git 深度集成
```

---

## 📝 图例说明

| 颜色 | 含义 |
|------|------|
| 🟩 绿色 | 正常状态/成功 |
| 🟨 黄色 | 警告/决策点 |
| 🟦 蓝色 | 处理步骤/数据流 |
| 🟪 紫色 | 渲染/转换 |
| 🟧 橙色 | 配置/设置 |
| 🟥 红色 | 错误/临界状态 |

---

**图表生成**: Aegis-1 (天枢计划执行引擎)  
**Mermaid 版本**: 10.x (GitHub 原生支持)  
**渲染说明**: 将本文件放入 GitHub 仓库即可自动渲染流程图

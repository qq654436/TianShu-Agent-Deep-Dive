# Claude HUD 架构图

**项目**: jarrodwatts/claude-hud  
**绘制日期**: 2026-03-20  
**工具**: Mermaid

---

## 🏗️ 系统架构

```mermaid
graph TB
    subgraph "Claude Code CLI"
        CC[Claude Code Process]
        TJ[Transcript JSONL]
        SA[StatusLine API]
    end

    subgraph "claude-hud Plugin"
        JP[JSONL Parser]
        TM[Token Tracker]
        UA[Usage API Client]
        GC[Git Status Checker]
        RP[Response Processor]
        CF[Config Manager]
    end

    subgraph "External Services"
        AA[Anthropic API]
        GH[GitHub API]
    end

    subgraph "Output Layer"
        TU[Terminal UI]
        CF2[Config File]
    end

    CC -->|stdin JSON| JP
    CC -->|Transcript| TJ
    TJ --> JP
    JP --> TM
    JP --> RP
    TM -->|Query| UA
    UA -->|Token Usage| AA
    GC -->|Git Status| GH
    GC --> RP
    CF -->|Load Config| RP
    RP -->|Format| SA
    SA --> TU
    RP -->|Save| CF2

    style CC fill:#e1f5ff
    style JP fill:#fff4e1
    style TM fill:#fff4e1
    style UA fill:#fff4e1
    style RP fill:#fff4e1
    style TU fill:#e8f5e9
```

---

## 🔄 数据流

```mermaid
sequenceDiagram
    participant CC as Claude Code
    participant JP as JSONL Parser
    participant TM as Token Tracker
    participant UA as Usage API
    participant RP as Response Processor
    participant TU as Terminal UI

    CC->>JP: Stream JSONL (tools, agents, todos)
    JP->>TM: Extract token usage
    TM->>UA: Query current usage
    UA->>UA: Check cache (TTL: 60s)
    alt Cache miss
        UA->>CC: Request OAuth token
        UA->>Anthropic: GET /v1/usage
        Anthropic->>UA: Usage data
        UA->>UA: Cache response
    end
    UA->>TM: Return usage
    JP->>RP: Parsed activity
    TM->>RP: Token metrics
    RP->>RP: Format statusLine
    RP->>TU: Render (~300ms interval)
```

---

## 📦 模块依赖

```mermaid
graph LR
    subgraph "Core Modules"
        JP[JSONL Parser]
        TM[Token Tracker]
        RP[Response Processor]
    end

    subgraph "Feature Modules"
        GC[Git Checker]
        UA[Usage API]
        TD[Todo Tracker]
        AT[Agent Tracker]
    end

    subgraph "Utilities"
        CF[Config Manager]
        CC[Color Compiler]
        CH[Cache Handler]
    end

    JP --> TM
    JP --> TD
    JP --> AT
    TM --> UA
    GC --> RP
    TD --> RP
    AT --> RP
    CF --> RP
    CC --> RP
    CH --> UA
    CH --> GC

    style JP fill:#ffccbc
    style TM fill:#ffccbc
    style RP fill:#ffccbc
    style GC fill:#c8e6c9
    style UA fill:#c8e6c9
    style CF fill:#bbdefb
```

---

## 🎨 UI 渲染流程

```mermaid
graph TD
    subgraph "Input Processing"
        RJ[Raw JSONL]
        PT[Parse Tools]
        PA[Parse Agents]
        PD[Parse Todos]
    end

    subgraph "State Computation"
        CS[Context State]
        US[Usage State]
        GS[Git State]
        TS[Tool State]
    end

    subgraph "Visual Encoding"
        CB[Context Bar]
        UB[Usage Bar]
        GI[Git Indicator]
        TL[Tool Line]
        AL[Agent Line]
        TDL[Todo Line]
    end

    subgraph "Output"
        FL[Final Line]
        TU[Terminal UI]
    end

    RJ --> PT
    RJ --> PA
    RJ --> PD
    PT --> TS
    PA --> CS
    PD --> TS
    CS --> CB
    US --> UB
    GS --> GI
    TS --> TL
    PA --> AL
    PD --> TDL
    CB --> FL
    UB --> FL
    GI --> FL
    TL --> FL
    AL --> FL
    TDL --> FL
    FL --> TU

    style RJ fill:#ffe0b2
    style CS fill:#fff9c4
    style CB fill:#c8e6c9
    style TU fill:#e3f2fd
```

---

## 🔐 安全边界

```mermaid
graph TB
    subgraph "Trusted Zone"
        CC[Claude Code CLI]
        LC[Local Config]
    end

    subgraph "Semi-Trusted Zone"
        JP[JSONL Parser]
        RP[Response Processor]
    end

    subgraph "Untrusted Zone"
        AA[Anthropic API]
        GH[GitHub API]
    end

    CC -->|Trust| JP
    JP -->|Validate| RP
    RP -->|Sanitize| CC
    RP -->|Query| AA
    RP -->|Query| GH
    AA -->|Rate Limit| RP
    GH -->|Rate Limit| RP
    LC -->|Load| RP

    style CC fill:#c8e6c9
    style LC fill:#c8e6c9
    style JP fill:#fff9c4
    style RP fill:#fff9c4
    style AA fill:#ffcdd2
    style GH fill:#ffcdd2
```

---

## ⚡ 性能优化点

```mermaid
graph LR
    subgraph "Optimization Strategies"
        C1[API Response Cache]
        C2[Debounced Updates]
        C3[Lazy Git Loading]
        C4[Incremental Parsing]
    end

    subgraph "Performance Targets"
        T1[<300ms Render]
        T2[<1% CPU Overhead]
        T3[<10MB Memory]
    end

    C1 --> T1
    C2 --> T1
    C2 --> T2
    C3 --> T2
    C3 --> T3
    C4 --> T1
    C4 --> T2

    style C1 fill:#e1f5fe
    style C2 fill:#e1f5fe
    style C3 fill:#e1f5fe
    style C4 fill:#e1f5fe
    style T1 fill:#f3e5f5
    style T2 fill:#f3e5f5
    style T3 fill:#f3e5f5
```

---

## 🧩 扩展点

```mermaid
graph TB
    subgraph "Core Extension Points"
        EP1[Custom Parsers]
        EP2[Custom Renderers]
        EP3[Custom Data Sources]
        EP4[Custom Notifications]
    end

    subgraph "Example Extensions"
        EX1[Linear Integration]
        EX2[Slack Notifications]
        EX3[Custom Metrics]
        EX4[Team Dashboard]
    end

    EP1 --> EX1
    EP2 --> EX2
    EP3 --> EX3
    EP4 --> EX4

    style EP1 fill:#ffe0b2
    style EP2 fill:#ffe0b2
    style EP3 fill:#ffe0b2
    style EP4 fill:#ffe0b2
    style EX1 fill:#e8f5e9
    style EX2 fill:#e8f5e9
    style EX3 fill:#e8f5e9
    style EX4 fill:#e8f5e9
```

---

## 📊 状态机

```mermaid
stateDiagram-v2
    [*] --> Initializing
    Initializing --> Ready: Config loaded
    Ready --> Monitoring: Watch started
    Monitoring --> Warning: Context > 70%
    Monitoring --> Critical: Context > 90%
    Warning --> Monitoring: Context < 70%
    Warning --> Critical: Context > 90%
    Critical --> Monitoring: Context < 90%
    Monitoring --> Paused: User pause
    Paused --> Monitoring: User resume
    Monitoring --> [*]: Session end

    note right of Initializing
        Load config.json
        Initialize trackers
    end note

    note right of Monitoring
        Parse JSONL stream
        Update every 300ms
    end note

    note right of Warning
        Yellow indicators
        Optional notification
    end note

    note right of Critical
        Red indicators
        Urgent notification
    end note
```

---

**图表说明**:
- 所有图表使用 Mermaid 语法，可在 GitHub、Notion、Feishu 等平台直接渲染
- 颜色编码：🔵 蓝色=输出层 🟢 绿色=安全 🟡 黄色=处理 🔴 红色=外部 🔶 橙色=核心

**维护者**: Sovereign (S.V.) 👁️  
**更新日期**: 2026-03-20

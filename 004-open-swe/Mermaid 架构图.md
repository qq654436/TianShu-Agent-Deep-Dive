# Open SWE 架构图

**项目**: langchain-ai/open-swe  
**绘制日期**: 2026-03-20  
**工具**: Mermaid

---

## 🏗️ 系统架构

```mermaid
graph TB
    subgraph "触发层 (Invocation)"
        Slack[Slack Bot]
        Linear[Linear Bot]
        GitHub[GitHub App]
    end

    subgraph "路由层 (Router)"
        RT[Trigger Router]
        TID[Thread ID Generator]
        MQ[Message Queue]
    end

    subgraph "编排层 (Orchestration)"
        LG[LangGraph]
        DA[Deep Agents]
        MA[Main Agent]
        SA[Subagents]
        MS[Middleware Stack]
    end

    subgraph "工具层 (Tooling)"
        T1[execute]
        T2[fetch_url]
        T3[http_request]
        T4[commit_and_open_pr]
        T5[linear_comment]
        T6[slack_reply]
        T7[read/write/edit_file]
    end

    subgraph "沙箱层 (Sandbox)"
        SB1[Modal]
        SB2[Daytona]
        SB3[Runloop]
        SB4[LangSmith]
    end

    subgraph "上下文层 (Context)"
        AM[AGENTS.md]
        IH[Issue History]
        TH[Thread History]
    end

    Slack --> RT
    Linear --> RT
    GitHub --> RT
    RT --> TID
    RT --> MQ
    TID --> MA
    MQ --> MS
    MA --> LG
    LG --> DA
    DA --> SA
    MA --> MS
    MS --> T1
    MS --> T2
    MS --> T3
    MS --> T4
    MS --> T5
    MS --> T6
    MS --> T7
    T1 --> SB1
    T2 --> SB1
    T3 --> SB1
    T4 --> SB1
    AM --> MA
    IH --> MA
    TH --> MA

    style Slack fill:#e1f5ff
    style Linear fill:#e1f5ff
    style GitHub fill:#e1f5ff
    style MA fill:#fff4e1
    style SA fill:#fff4e1
    style MS fill:#fff9c4
    style SB1 fill:#e8f5e9
    style SB2 fill:#e8f5e9
    style SB3 fill:#e8f5e9
    style SB4 fill:#e8f5e9
```

---

## 🔄 任务执行流程

```mermaid
sequenceDiagram
    participant U as User
    participant S as Slack/Linear/GitHub
    participant R as Router
    participant M as Middleware
    participant A as Main Agent
    participant SB as Sandbox
    participant G as GitHub

    U->>S: @openswe fix login bug
    S->>R: Trigger event
    R->>R: Generate thread ID
    R->>A: Create/Get Agent
    A->>SB: Create sandbox
    SB-->>A: Sandbox ready
    A->>A: Load AGENTS.md
    A->>A: Load issue context
    loop Agent Loop
        A->>M: before_model hook
        M->>M: Inject follow-up messages
        M-->>A: Updated context
        A->>A: LLM decision
        A->>SB: Execute tool
        SB-->>A: Tool result
        A->>M: after_agent hook
    end
    A->>SB: Commit changes
    A->>G: Create PR
    G-->>A: PR URL
    A->>S: Reply with PR link
    S-->>U: Notification
```

---

## 🧩 Middleware 钩子

```mermaid
graph LR
    subgraph "Before Model Hooks"
        CMQ[check_message_queue]
        RL[Rate Limiter]
        CI[Context Injector]
    end

    subgraph "After Agent Hooks"
        OPN[open_pr_if_needed]
        TEH[tool_error_handler]
        LOG[Logger]
    end

    subgraph "Tool Hooks"
        TBE[before_execute]
        TAE[after_execute]
        VAL[Validator]
    end

    CMQ --> MA[Main Agent]
    RL --> MA
    CI --> MA
    MA --> OPN
    MA --> TEH
    MA --> LOG
    MA --> TBE
    TBE --> SB[Sandbox]
    SB --> TAE
    TAE --> VAL
    VAL --> MA

    style CMQ fill:#ffe0b2
    style RL fill:#ffe0b2
    style CI fill:#ffe0b2
    style OPN fill:#c8e6c9
    style TEH fill:#c8e6c9
    style LOG fill:#bbdefb
```

---

## 📦 沙箱提供商架构

```mermaid
graph TB
    subgraph "Sandbox Manager"
        SM[Sandbox Manager]
        SP[Sandbox Provider Interface]
    end

    subgraph "Provider Implementations"
        MP[Modal Provider]
        DP[Daytona Provider]
        RP[Runloop Provider]
        LP[LangSmith Provider]
    end

    subgraph "Sandbox Instances"
        SI1[Sandbox 1<br/>repo: cloned<br/>status: running]
        SI2[Sandbox 2<br/>repo: cloned<br/>status: running]
        SI3[Sandbox 3<br/>repo: cloned<br/>status: idle]
    end

    subgraph "External APIs"
        MA[Modal API]
        DA[Daytona API]
        RA[Runloop API]
        LA[LangSmith API]
    end

    SM --> SP
    SP --> MP
    SP --> DP
    SP --> RP
    SP --> LP
    MP --> MA
    DP --> DA
    RP --> RA
    LP --> LA
    MP --> SI1
    DP --> SI2
    RP --> SI3

    style SM fill:#ffccbc
    style SP fill:#ffccbc
    style MP fill:#c8e6c9
    style DP fill:#c8e6c9
    style RP fill:#c8e6c9
    style LP fill:#c8e6c9
    style SI1 fill:#e3f2fd
    style SI2 fill:#e3f2fd
    style SI3 fill:#e3f2fd
```

---

## 🎯 触发器路由

```mermaid
graph TB
    subgraph "Input Channels"
        SC[Slack Channel]
        LC[Linear Issue]
        GC[GitHub PR]
    end

    subgraph "Normalization Layer"
        NP[Normalize Payload]
        TI[Thread ID Generator]
        CT[Context Assembler]
    end

    subgraph "Agent Pool"
        AG1[Agent 1<br/>thread: slack-001]
        AG2[Agent 2<br/>thread: linear-002]
        AG3[Agent 3<br/>thread: github-003]
    end

    subgraph "Message Queue"
        MQ1[Queue: slack-001]
        MQ2[Queue: linear-002]
        MQ3[Queue: github-003]
    end

    SC --> NP
    LC --> NP
    GC --> NP
    NP --> TI
    TI --> CT
    CT --> AG1
    CT --> AG2
    CT --> AG3
    AG1 --> MQ1
    AG2 --> MQ2
    AG3 --> MQ3
    MQ1 -.->|Follow-up| AG1
    MQ2 -.->|Follow-up| AG2
    MQ3 -.->|Follow-up| AG3

    style SC fill:#e1f5ff
    style LC fill:#e1f5ff
    style GC fill:#e1f5ff
    style AG1 fill:#fff4e1
    style AG2 fill:#fff4e1
    style AG3 fill:#fff4e1
```

---

## 🔐 安全边界

```mermaid
graph TB
    subgraph "Trusted Zone"
        U[User]
        S[Slack/Linear/GitHub]
        CFG[Config Store]
    end

    subgraph "Semi-Trusted Zone"
        R[Router]
        A[Agent]
        M[Middleware]
    end

    subgraph "Untrusted Zone"
        SB[Sandbox]
        EX[Code Execution]
        NW[Network Calls]
    end

    subgraph "External Services"
        GH[GitHub API]
        LI[Linear API]
        SL[Slack API]
    end

    U -->|Trust| S
    S -->|Validate| R
    R -->|Sanitize| A
    A -->|Limit| M
    M -->|Isolate| SB
    SB --> EX
    SB --> NW
    A -->|OAuth| GH
    A -->|API Key| LI
    A -->|Bot Token| SL
    CFG -->|Load| M

    style U fill:#c8e6c9
    style S fill:#c8e6c9
    style CFG fill:#c8e6c9
    style R fill:#fff9c4
    style A fill:#fff9c4
    style M fill:#fff9c4
    style SB fill:#ffcdd2
    style EX fill:#ffcdd2
    style NW fill:#ffcdd2
```

---

## ⚡ 并行任务处理

```mermaid
graph LR
    subgraph "Task Queue"
        T1[Task 1<br/>Issue #123]
        T2[Task 2<br/>Issue #124]
        T3[Task 3<br/>Slack thread]
    end

    subgraph "Sandbox Pool"
        S1[Sandbox 1<br/>Modal]
        S2[Sandbox 2<br/>Daytona]
        S3[Sandbox 3<br/>Runloop]
    end

    subgraph "Agent Instances"
        A1[Agent 1<br/>Main + 2 subagents]
        A2[Agent 2<br/>Main + 1 subagent]
        A3[Agent 3<br/>Main only]
    end

    subgraph "Output"
        PR1[PR #456]
        PR2[PR #457]
        R3[Slack reply]
    end

    T1 --> S1
    T2 --> S2
    T3 --> S3
    S1 --> A1
    S2 --> A2
    S3 --> A3
    A1 --> PR1
    A2 --> PR2
    A3 --> R3

    style T1 fill:#ffe0b2
    style T2 fill:#ffe0b2
    style T3 fill:#ffe0b2
    style S1 fill:#c8e6c9
    style S2 fill:#c8e6c9
    style S3 fill:#c8e6c9
    style PR1 fill:#e3f2fd
    style PR2 fill:#e3f2fd
```

---

## 📊 状态机

```mermaid
stateDiagram-v2
    [*] --> Idle
    Idle --> Receiving: Trigger received
    Receiving --> CreatingSandbox: Route to agent
    CreatingSandbox --> Running: Sandbox ready
    Running --> Executing: Agent loop
    Executing --> WaitingFollowUp: Need user input
    WaitingFollowUp --> Executing: Follow-up received
    Executing --> Completing: Task done
    Completing --> OpeningPR: Has changes
    OpeningPR --> Notifying: PR created
    Completing --> Notifying: No changes
    Notifying --> Idle: Complete
    Running --> Error: Sandbox error
    Running --> Timeout: TTL exceeded
    Error --> Cleanup: Log error
    Timeout --> Cleanup: Destroy sandbox
    Cleanup --> Idle: Ready

    note right of Receiving
        Generate thread ID
        Load context
    end note

    note right of Executing
        LLM decision
        Tool execution
        Middleware hooks
    end note

    note right of OpeningPR
        Commit changes
        Create draft PR
        Link to issue
    end note
```

---

## 🧭 决策树

```mermaid
graph TD
    START[Task Received] --> CHECK{Has AGENTS.md?}
    CHECK -->|Yes| LOAD[Load guidelines]
    CHECK -->|No| SKIP[Skip injection]
    LOAD --> SANDBOX{Sandbox exists?}
    SKIP --> SANDBOX
    SANDBOX -->|No| CREATE[Create sandbox]
    SANDBOX -->|Yes| REUSE[Reuse sandbox]
    CREATE --> EXEC[Execute task]
    REUSE --> EXEC
    EXEC --> CHANGES{Has changes?}
    CHANGES -->|Yes| TEST{Tests pass?}
    CHANGES -->|No| REPLY[Reply to user]
    TEST -->|Yes| PR[Create PR]
    TEST -->|No| FIX[Request fix]
    PR --> REPLY
    FIX --> EXEC
    REPLY --> END[*]

    style START fill:#e1f5ff
    style CHECK fill:#fff9c4
    style SANDBOX fill:#fff9c4
    style CHANGES fill:#fff9c4
    style TEST fill:#fff9c4
    style END fill:#c8e6c9
```

---

**图表说明**:
- 所有图表使用 Mermaid 语法，可在 GitHub、Notion、Feishu 等平台直接渲染
- 颜色编码：🔵 蓝色=触发层 🟠 橙色=编排层 🟢 绿色=沙箱层 🟡 黄色=决策点 🔴 红色=非信任区

**维护者**: Sovereign (S.V.) 👁️  
**更新日期**: 2026-03-20

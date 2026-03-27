# DeerFlow 2.0 架构图

**项目**: bytedance/deer-flow  
**分析日期**: 2026-03-27  
**来源**: GitHub Trending #1 (16,126 ⭐/周)

---

## 系统架构总览

```mermaid
graph TB
    subgraph "User Interface Layer"
        UI[Web UI<br/>localhost:2026]
        IM[IM Channels<br/>Telegram/Slack/Feishu]
        CLI[CLI Interface]
    end

    subgraph "Gateway Layer"
        GW[API Gateway<br/>Port 8001]
        LB[Load Balancer<br/>nginx]
    end

    subgraph "Agent Orchestration Layer"
        LG[LangGraph Server<br/>Port 2024]
        LA[Lead Agent<br/>Orchestrator]
        SA[Sub-Agent Pool<br/>Dynamic Scaling]
    end

    subgraph "Core Services"
        MEM[Memory Service<br/>Vector DB]
        SKILL[Skill Manager<br/>MCP Servers]
        SANDBOX[Sandbox Provider<br/>Docker/K8s/Local]
        CTX[Context Engine<br/>Token Management]
    end

    subgraph "External Integrations"
        LLM[LLM Providers<br/>OpenAI/Anthropic/ByteDance]
        TOOLS[External Tools<br/>Search/Code/Filesystem]
        MCP[MCP Servers<br/>HTTP/SSE/OAuth]
    end

    UI --> GW
    IM --> GW
    CLI --> GW
    GW --> LB
    LB --> LG
    LG --> LA
    LA --> SA
    LA --> MEM
    LA --> SKILL
    LA --> CTX
    SA --> SANDBOX
    SA --> TOOLS
    SKILL --> MCP
    LA --> LLM
    SA --> LLM

    style LA fill:#f96,stroke:#333,stroke-width:2px
    style SA fill:#9f6,stroke:#333,stroke-width:2px
    style MEM fill:#69f,stroke:#333,stroke-width:2px
```

---

## 代理编排流程

```mermaid
sequenceDiagram
    participant U as User
    participant G as Gateway
    participant LA as Lead Agent
    participant SA1 as Sub-Agent 1
    participant SA2 as Sub-Agent 2
    participant M as Memory
    participant S as Sandbox
    participant T as Tools/MCP

    U->>G: Submit Task
    G->>LA: Route to Lead Agent
    LA->>LA: Analyze & Decompose
    LA->>M: Load Context
    LA->>SA1: Assign Sub-task 1
    LA->>SA2: Assign Sub-task 2
    SA1->>S: Execute in Sandbox
    SA2->>T: Call External Tool
    SA1-->>LA: Return Result 1
    SA2-->>LA: Return Result 2
    LA->>LA: Synthesize Results
    LA->>M: Save to Memory
    LA->>G: Return Final Output
    G->>U: Display Result
```

---

## 沙箱执行模式

```mermaid
graph LR
    subgraph "Sandbox Modes"
        mode{Sandbox Mode}
        local[Local Execution<br/>Direct Host Access]
        docker[Docker Execution<br/>Container Isolation]
        k8s[Kubernetes Execution<br/>Pod-based Scaling]
    end

    subgraph "Provisioner Service"
        prov[Provisioner<br/>Container Manager]
        img[Sandbox Image<br/>Pull on Demand]
        vol[Volume Mounts<br/>Workspace Isolation]
    end

    mode --> local
    mode --> docker
    mode --> k8s

    docker --> prov
    k8s --> prov
    prov --> img
    prov --> vol

    style mode fill:#ff9,stroke:#333,stroke-width:2px
    style prov fill:#f96,stroke:#333,stroke-width:2px
```

---

## 记忆系统架构

```mermaid
graph TB
    subgraph "Memory Layers"
        STM[Short-Term Memory<br/>Session Context]
        LTM[Long-Term Memory<br/>Vector Embeddings]
        WM[Working Memory<br/>Active Task State]
    end

    subgraph "Memory Operations"
        write[Write Operation<br/>Embed + Store]
        read[Read Operation<br/>Similarity Search]
        update[Update Operation<br/>Merge + Deduplicate]
    end

    subgraph "Storage Backends"
        vec[Vector DB<br/>Chroma/Weaviate]
        fs[Filesystem<br/>JSONL/Markdown]
        cache[Cache Layer<br/>Redis/Memory]
    end

    STM --> write
    LTM --> read
    WM --> update

    write --> vec
    write --> fs
    read --> vec
    read --> cache
    update --> fs
    update --> cache

    style LTM fill:#69f,stroke:#333,stroke-width:2px
    style vec fill:#9f6,stroke:#333,stroke-width:2px
```

---

## 技能与 MCP 集成

```mermaid
graph TB
    subgraph "Skill System"
        SM[Skill Manager]
        LS[Local Skills<br/>skills/ directory]
        MS[MCP Skills<br/>Remote Servers]
    end

    subgraph "MCP Protocol"
        http[HTTP/SSE Transport]
        oauth[OAuth 2.0 Auth<br/>client_credentials/refresh_token]
        schema[Tool Schema<br/>JSON Schema]
    end

    subgraph "Example MCP Servers"
        gh[GitHub MCP<br/>Repository Operations]
        fs[Filesystem MCP<br/>Safe File Access]
        web[Web Search MCP<br/>Brave/SearXNG]
    end

    SM --> LS
    SM --> MS
    MS --> http
    MS --> oauth
    MS --> schema
    http --> gh
    http --> fs
    http --> web

    style SM fill:#f96,stroke:#333,stroke-width:2px
    style MS fill:#9f6,stroke:#333,stroke-width:2px
```

---

## 配置管理

```mermaid
graph LR
    subgraph "Configuration Files"
        config[config.yaml<br/>Main Configuration]
        env[.env<br/>Environment Variables]
        skills[skills/*.md<br/>Skill Definitions]
    end

    subgraph "Runtime Config"
        models[Model Providers<br/>OpenAI/Anthropic/ByteDance]
        channels[IM Channels<br/>Telegram/Slack/Feishu]
        sandbox[Sandbox Settings<br/>Mode/Image/Limits]
    end

    config --> models
    config --> channels
    config --> sandbox
    env --> models
    skills --> SM[Skill Manager]

    style config fill:#ff9,stroke:#333,stroke-width:2px
    style models fill:#69f,stroke:#333,stroke-width:2px
```

---

## 关键设计模式

### 1. Lead-Sub Agent Pattern
```mermaid
graph TB
    LA[Lead Agent] --> |Decompose| T1[Task 1]
    LA --> |Decompose| T2[Task 2]
    LA --> |Decompose| T3[Task 3]
    
    T1 --> SA1[Sub-Agent 1]
    T2 --> SA2[Sub-Agent 2]
    T3 --> SA3[Sub-Agent 3]
    
    SA1 --> |Parallel| R1[Result 1]
    SA2 --> |Parallel| R2[Result 2]
    SA3 --> |Parallel| R3[Result 3]
    
    R1 --> LA
    R2 --> LA
    R3 --> LA
    
    LA --> |Synthesize| Final[Final Output]
    
    style LA fill:#f96,stroke:#333,stroke-width:3px
    style SA1 fill:#9f6,stroke:#333,stroke-width:2px
    style SA2 fill:#9f6,stroke:#333,stroke-width:2px
    style SA3 fill:#9f6,stroke:#333,stroke-width:2px
```

### 2. Context Engineering
```mermaid
graph LR
    subgraph "Context Window Management"
        input[User Input]
        history[Session History]
        memory[Retrieved Memory]
        tools[Tool Outputs]
    end

    subgraph "Compression Strategies"
        summary[Summarization]
        prune[Pruning Old Messages]
        embed[Embedding + Retrieval]
    end

    input --> limit{Token Limit?}
    history --> limit
    memory --> limit
    tools --> limit

    limit -->|Yes| summary
    limit -->|Yes| prune
    limit -->|No| output[LLM Input]

    summary --> output
    prune --> output
    embed --> output

    style limit fill:#ff9,stroke:#333,stroke-width:2px
    style output fill:#9f6,stroke:#333,stroke-width:2px
```

---

## 与 OpenClaw 对比

| 组件 | DeerFlow 2.0 | OpenClaw | 适配建议 |
|------|-------------|----------|---------|
| **编排引擎** | LangGraph | sessions_spawn | ✅ 已对齐 |
| **沙箱** | Docker/K8s | exec (用户权限) | ⚠️ 可引入 Docker |
| **记忆** | 向量数据库 | LONG_TERM_MEMORY.md | ✅ 已实现 |
| **技能** | MCP 服务器 | skills/ 目录 | ⚠️ 可集成 MCP |
| **IM** | Telegram/Slack/飞书 | Feishu/Telegram | ✅ 已覆盖 |
| **UI** | Web (localhost:2026) | Canvas/飞书卡片 | 🟢 差异化 |

---

**图表生成**: Sovereign (S.V.) 👁️  
**格式**: Mermaid (兼容 GitHub/GitLab/Notion)

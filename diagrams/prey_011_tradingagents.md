# TradingAgents 架构图

**项目**: TauricResearch/TradingAgents  
**分析日期**: 2026-03-27  
**来源**: GitHub Trending #2 (9,209 ⭐/周)

---

## 系统架构总览

```mermaid
graph TB
    subgraph "User Interface"
        CLI[Interactive CLI<br/>ticker/date/LLM selection]
        PY[Python API<br/>TradingAgentsGraph]
    end

    subgraph "Agent Teams"
        subgraph "Analyst Team"
            FA[Fundamentals Analyst<br/>Company Financials]
            SA[Sentiment Analyst<br/>Social Media Sentiment]
            NA[News Analyst<br/>Global News/Macro]
            TA[Technical Analyst<br/>Indicators/Patterns]
        end

        subgraph "Researcher Team"
            BR[Bullish Researcher<br/>Pro-Growth Arguments]
            BER[Bearish Researcher<br/>Risk Identification]
        end

        subgraph "Decision Layer"
            TR[Trader Agent<br/>Trading Decision]
            RM[Risk Management<br/>Risk Assessment]
            PM[Portfolio Manager<br/>Final Approval]
        end
    end

    subgraph "Data Sources"
        FIN[Financial Data<br/>Alpha Vantage]
        SOC[Social Media<br/>Twitter/Reddit]
        NEWS[News API<br/>Global News]
        MKT[Market Data<br/>Price/Volume]
    end

    subgraph "LLM Providers"
        GPT[OpenAI<br/>GPT-5.x]
        GEM[Google<br/>Gemini 3.x]
        CL[Anthropic<br/>Claude 4.x]
        GRO[xAI<br/>Grok 4.x]
        OLL[Ollama<br/>Local Models]
    end

    CLI --> TR
    PY --> TR
    FA --> BR
    SA --> BR
    NA --> BR
    TA --> BR
    FA --> BER
    SA --> BER
    NA --> BER
    TA --> BER
    BR --> TR
    BER --> TR
    TR --> RM
    RM --> PM
    PM --> EXCH[Simulated Exchange]
    
    FIN --> FA
    SOC --> SA
    NEWS --> NA
    MKT --> TA
    
    GPT -.-> FA
    GPT -.-> SA
    GPT -.-> NA
    GPT -.-> TA
    GPT -.-> BR
    GPT -.-> BER
    GPT -.-> TR
    GPT -.-> RM
    GPT -.-> PM

    style TR fill:#f96,stroke:#333,stroke-width:3px
    style PM fill:#9f6,stroke:#333,stroke-width:2px
    style BR fill:#69f,stroke:#333,stroke-width:2px
    style BER fill:#f66,stroke:#333,stroke-width:2px
```

---

## 代理角色详细流程

```mermaid
sequenceDiagram
    participant U as User
    participant TA as Trader Agent
    participant FA as Fundamentals Analyst
    participant SA as Sentiment Analyst
    participant NNA as News Analyst
    participant TCA as Technical Analyst
    participant BR as Bullish Researcher
    participant BER as Bearish Researcher
    participant RM as Risk Management
    participant PM as Portfolio Manager

    U->>TA: Submit Ticker + Date
    TA->>FA: Request Fundamental Analysis
    TA->>SA: Request Sentiment Analysis
    TA->>NNA: Request News Analysis
    TA->>TCA: Request Technical Analysis
    
    par Parallel Analysis
        FA->>FA: Analyze Financials
        SA->>SA: Score Sentiment
        NNA->>NNA: Interpret Events
        TCA->>TCA: Calculate Indicators
    end
    
    FA-->>TA: Fundamental Report
    SA-->>TA: Sentiment Score
    NNA-->>TA: News Impact
    TCA-->>TA: Technical Signals
    
    TA->>BR: Send Analyst Reports
    TA->>BER: Send Analyst Reports
    
    BR->>BER: Debate Round 1
    BER->>BR: Counter-Arguments
    BR->>BER: Debate Round 2
    
    BR-->>TA: Bullish Thesis
    BER-->>TA: Bearish Thesis
    
    TA->>TA: Synthesize All Inputs
    TA->>TA: Make Trading Decision
    
    TA->>RM: Submit Decision + Rationale
    RM->>RM: Assess Risk
    RM-->>TA: Risk Report
    
    TA->>PM: Submit Transaction Proposal
    PM->>PM: Final Review
    PM->>PM: Approve/Reject
    
    PM-->>U: Final Decision + Report
```

---

## 辩论机制详解

```mermaid
graph TB
    subgraph "Debate Input"
        AR[Analyst Reports<br/>FA+SA+NA+TA]
    end

    subgraph "Debate Process"
        round1{Debate Round 1}
        BR1[Bullish Argument<br/>Growth Potential]
        BER1[Bearish Counter<br/>Risk Factors]
        
        round2{Debate Round 2}
        BR2[Bullish Rebuttal<br/>Address Risks]
        BER2[Bearish Rebuttal<br/>Challenge Assumptions]
    end

    subgraph "Debate Output"
        BT[Bullish Thesis<br/>Confidence Score]
        BET[Bearish Thesis<br/>Confidence Score]
    end

    AR --> round1
    round1 --> BR1
    round1 --> BER1
    BR1 --> BER1
    BER1 --> round2
    BR1 --> round2
    round2 --> BR2
    round2 --> BER2
    BR2 --> BET
    BER2 --> BT
    BR2 --> BT
    BER2 --> BET

    style round1 fill:#ff9,stroke:#333,stroke-width:2px
    style round2 fill:#ff9,stroke:#333,stroke-width:2px
    style BT fill:#9f6,stroke:#333,stroke-width:2px
    style BET fill:#f66,stroke:#333,stroke-width:2px
```

---

## 决策流程

```mermaid
graph TB
    subgraph "Decision Pipeline"
        input[Ticker + Date]
        analysis[Multi-Agent Analysis]
        debate[Bull/Bear Debate]
        synthesis[Trader Synthesis]
        risk[Risk Assessment]
        approval[Portfolio Approval]
        output[Final Decision]
    end

    subgraph "Decision Types"
        buy[BUY<br/>Strength: 1-5]
        sell[SELL<br/>Strength: 1-5]
        hold[HOLD<br/>No Action]
    end

    input --> analysis
    analysis --> debate
    debate --> synthesis
    synthesis --> risk
    risk --> approval
    approval --> output

    output --> buy
    output --> sell
    output --> hold

    style synthesis fill:#f96,stroke:#333,stroke-width:3px
    style approval fill:#9f6,stroke:#333,stroke-width:2px
    style output fill:#69f,stroke:#333,stroke-width:2px
```

---

## 数据流架构

```mermaid
graph LR
    subgraph "Data Collection"
        API1[Alpha Vantage API<br/>Financial Data]
        API2[News API<br/>Global Events]
        API3[Social Media API<br/>Sentiment Data]
        API4[Market Data API<br/>Price/Volume]
    end

    subgraph "Data Processing"
        clean[Data Cleaning<br/>Normalization]
        enrich[Enrichment<br/>Derived Metrics]
        store[Temporary Storage<br/>Session Cache]
    end

    subgraph "Agent Consumption"
        FA[Fundamentals Analyst]
        SA[Sentiment Analyst]
        NNA[News Analyst]
        TCA[Technical Analyst]
    end

    API1 --> clean
    API2 --> clean
    API3 --> clean
    API4 --> clean

    clean --> enrich
    enrich --> store

    store --> FA
    store --> SA
    store --> NNA
    store --> TCA

    style clean fill:#ff9,stroke:#333,stroke-width:2px
    style store fill:#69f,stroke:#333,stroke-width:2px
```

---

## 配置系统

```mermaid
graph TB
    subgraph "Configuration Layers"
        default[default_config.py<br/>Base Defaults]
        user[User Config<br/>CLI Selection]
        env[.env<br/>API Keys]
    end

    subgraph "Configurable Parameters"
        llm[LLM Provider<br/>openai/google/anthropic/xai/ollama]
        model[Model Selection<br/>gpt-5.2/gemini-3/claude-4]
        debate[Debate Rounds<br/>Default: 2]
        depth[Research Depth<br/>shallow/medium/deep]
    end

    subgraph "Runtime Overrides"
        ticker[Ticker Symbol<br/>e.g., NVDA]
        date[Analysis Date<br/>YYYY-MM-DD]
        debug[Debug Mode<br/>Verbose Logging]
    end

    default --> user
    env --> llm
    user --> model
    user --> debate
    user --> depth
    user --> ticker
    user --> date
    user --> debug

    style default fill:#ff9,stroke:#333,stroke-width:2px
    style llm fill:#69f,stroke:#333,stroke-width:2px
    style ticker fill:#9f6,stroke:#333,stroke-width:2px
```

---

## LangGraph 实现

```mermaid
graph TB
    subgraph "Graph Nodes"
        start[Start Node<br/>Initialize State]
        analysts[Analyst Node<br/>Parallel Execution]
        researchers[Researcher Node<br/>Debate Loop]
        trader[Trader Node<br/>Decision Making]
        risk[Risk Node<br/>Assessment]
        portfolio[Portfolio Node<br/>Final Approval]
        end[End Node<br/>Return Result]
    end

    subgraph "State Management"
        state[Graph State<br/>TypedDict]
        messages[Message History]
        reports[Analyst Reports]
        decision[Trading Decision]
    end

    start --> analysts
    analysts --> researchers
    researchers --> trader
    trader --> risk
    risk --> portfolio
    portfolio --> end

    analysts -.-> state
    researchers -.-> state
    trader -.-> state
    risk -.-> state
    portfolio -.-> state

    state --> messages
    state --> reports
    state --> decision

    style start fill:#9f6,stroke:#333,stroke-width:2px
    style end fill:#9f6,stroke:#333,stroke-width:2px
    style trader fill:#f96,stroke:#333,stroke-width:3px
    style state fill:#69f,stroke:#333,stroke-width:2px
```

---

## 与 OpenClaw 适配点

### 可直接借鉴的设计

```mermaid
graph TB
    subgraph "TradingAgents Features"
        role[Role Specialization<br/>6 Agent Types]
        debate[Structured Debate<br/>Bull vs Bear]
        hierarchy[Decision Hierarchy<br/>Multi-Level Approval]
        config[Flexible Config<br/>Multi-Provider LLM]
    end

    subgraph "OpenClaw Adaptation"
        subrole[Sub-Agent Roles<br/>analyst/researcher/orchestrator]
        subdebate[Multi-Agent Debate<br/>For Complex Decisions]
        subhierarchy[Task Approval Flow<br/>Risk Assessment]
        subconfig[Model Routing<br/>Task-Based Selection]
    end

    role --> subrole
    debate --> subdebate
    hierarchy --> subhierarchy
    config --> subconfig

    style role fill:#69f,stroke:#333,stroke-width:2px
    style debate fill:#69f,stroke:#333,stroke-width:2px
    style subrole fill:#9f6,stroke:#333,stroke-width:2px
    style subdebate fill:#9f6,stroke:#333,stroke-width:2px
```

### 实现优先级

| 功能 | 优先级 | 复杂度 | 预期收益 |
|------|--------|--------|---------|
| 子代理角色元数据 | P0 | 低 | 高 |
| 多代理辩论机制 | P0 | 中 | 高 |
| 任务审批流程 | P1 | 中 | 中 |
| 模型路由策略 | P1 | 低 | 中 |
| 风险评估模块 | P2 | 高 | 中 |

---

## 关键设计模式总结

### 1. 专业化分工模式
```
Analyst Team (信息收集) → Researcher Team (批判性评估) → 
Trader (决策) → Risk Management (风险评估) → 
Portfolio Manager (最终批准)
```

### 2. 结构化辩论模式
```
Bullish Arguments ↔ Bearish Counter-Arguments
    ↓ (Round 1)
Bullish Rebuttal ↔ Bearish Rebuttal
    ↓ (Round 2)
Synthesized Thesis with Confidence Scores
```

### 3. 分层决策模式
```
Level 1: Analyst Reports (事实收集)
Level 2: Researcher Debate (观点碰撞)
Level 3: Trader Decision (初步决策)
Level 4: Risk Assessment (风险控制)
Level 5: Portfolio Approval (最终批准)
```

---

**图表生成**: Sovereign (S.V.) 👁️  
**格式**: Mermaid (兼容 GitHub/GitLab/Notion)  
**应用建议**: 在 OpenClaw 复杂任务中引入辩论机制和分层决策

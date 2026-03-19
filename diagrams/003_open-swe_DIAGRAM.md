# 猎物 #003: langchain-ai/open-swe - 架构流程图

**天枢计划 | Mermaid 文本架构图**  
**创建日期**: 2026-03-19  
**原项目**: [langchain-ai/open-swe](https://github.com/langchain-ai/open-swe)

---

## 🏗️ 核心架构总览

```mermaid
flowchart TB
    subgraph OPENSWE["Open SWE 企业级 Agent 架构"]
        direction TB
        
        subgraph TRIGGER["触发层"]
            SLACK[Slack @提及]
            LINEAR[Linear @openswe]
            GITHUB[GitHub @openswe]
        end
        
        subgraph ROUTE["路由层"]
            THREAD[确定性 Thread ID 路由]
        end
        
        subgraph HARNESS["Agent Harness 层"]
            DEEP[Deep Agents 组合]
            SYS[System Prompt 注入]
            TOOLS[精选工具集 ~15 个]
            MW[中间件层]
        end
        
        subgraph SANDBOX["沙箱层"]
            MODAL[Modal 容器]
            DAYTONA[Daytona 开发环境]
            RUNLOOP[Runloop CI/CD]
            LANGSMITH[LangSmith 观测]
        end
        
        subgraph VALIDATE["验证层"]
            LINT[Lint/Formatter]
            TEST[Tests]
            PR[PR 安全网]
        end
        
        TRIGGER --> ROUTE
        ROUTE --> HARNESS
        HARNESS --> SANDBOX
        SANDBOX --> VALIDATE
        
        style OPENSWE fill:#e8eaf6,stroke:#3f51b5,stroke-width:3px
        style TRIGGER fill:#c5cae9,stroke:#3f51b5,stroke-width:1px
        style ROUTE fill:#ffeb3b,stroke:#f57f17,stroke-width:2px
        style HARNESS fill:#bbdefb,stroke:#1565c0,stroke-width:1px
        style SANDBOX fill:#c8e6c9,stroke:#2e7d32,stroke-width:1px
        style VALIDATE fill:#a5d6a7,stroke:#2e7d32,stroke-width:1px
    end
```

---

## 🔄 七大核心架构决策

```mermaid
flowchart LR
    subgraph SEVEN["七大核心决策"]
        direction TB
        D1[① Agent Harness<br/>Deep Agents 组合]
        D2[② Sandbox<br/>隔离云环境]
        D3[③ Tools<br/>精选而非堆积]
        D4[④ Context<br/>AGENTS.md + 源上下文]
        D5[⑤ Orchestration<br/>子代理 + 中间件]
        D6[⑥ Invocation<br/>Slack/Linear/GitHub]
        D7[⑦ Validation<br/>提示驱动 + 安全网]
    end
    
    D1 --> D2
    D2 --> D3
    D3 --> D4
    D4 --> D5
    D5 --> D6
    D6 --> D7
    
    style SEVEN fill:#fff3e0,stroke:#e65100,stroke-width:2px
    style D1 fill:#ffe0b2,stroke:#e65100,stroke-width:1px
    style D2 fill:#ffe0b2,stroke:#e65100,stroke-width:1px
    style D3 fill:#ffe0b2,stroke:#e65100,stroke-width:1px
    style D4 fill:#ffe0b2,stroke:#e65100,stroke-width:1px
    style D5 fill:#ffe0b2,stroke:#e65100,stroke-width:1px
    style D6 fill:#ffe0b2,stroke:#e65100,stroke-width:1px
    style D7 fill:#ffe0b2,stroke:#e65100,stroke-width:1px
```

---

## 📡 多平台触发与路由

```mermaid
sequenceDiagram
    participant User as 工程师
    participant Platform as Slack/Linear/GitHub
    participant Router as Thread Router
    participant Agent as Agent Harness
    participant Sandbox as 沙箱环境
    
    User->>Platform: @提及 + repo:owner/name
    Platform->>Router: Webhook 事件
    Router->>Router: 生成确定性 Thread ID
    Router->>Agent: 任务 + Thread ID
    
    Agent->>Sandbox: 创建/复用沙箱
    Sandbox-->>Agent: 沙箱就绪
    
    loop 任务执行
        Agent->>Sandbox: 执行工具调用
        Sandbox-->>Agent: 返回结果
        Agent->>Agent: 中间件钩子检查
    end
    
    Agent->>Router: 任务完成 + 结果
    Router->>Platform: 回复线程 (PR 链接/状态)
    Platform->>User: 通知
```

---

## 🧰 精选工具集架构

```mermaid
flowchart TB
    subgraph TOOLS["精选工具集 (~15 个)"]
        direction TB
        
        subgraph DEEP["Deep Agents 内置"]
            READ[read_file]
            WRITE[write_file]
            EDIT[edit_file]
            LS[ls/glob/grep]
            TODO[write_todos]
            TASK[task 子代理]
        end
        
        subgraph CUSTOM["自定义工具"]
            EXEC[execute Shell]
            FETCH[fetch_url]
            HTTP[http_request]
            PR[commit_and_open_pr]
            LINEAR[linear_comment]
            SLACK[slack_thread_reply]
        end
    end
    
    AGENT[Agent] --> SELECT{工具选择}
    SELECT --> DEEP
    SELECT --> CUSTOM
    
    DEEP --> SANDBOX[沙箱内执行]
    CUSTOM --> API[外部 API 调用]
    
    style TOOLS fill:#e0f7fa,stroke:#006064,stroke-width:2px
    style DEEP fill:#b2ebf2,stroke:#006064,stroke-width:1px
    style CUSTOM fill:#80deea,stroke:#006064,stroke-width:1px
    style SELECT fill:#ffeb3b,stroke:#333,stroke-width:2px
```

---

## 📚 双层上下文注入

```mermaid
flowchart TB
    subgraph CONTEXT["双层上下文注入"]
        direction TB
        
        subgraph SYS["系统层 (自动注入)"]
            AGENTS[AGENTS.md<br/>仓库级约定]
            RULES[编码规范/测试要求/架构决策]
        end
        
        subgraph TASK["任务层 (按需注入)"]
            ISSUE[Linear Issue<br/>标题/描述/评论]
            SLACK_H[Slack Thread 历史]
            GH[GitHub PR 评论]
        end
    end
    
    AGENTS --> SYS_PROMPT[注入 System Prompt]
    RULES --> SYS_PROMPT
    
    ISSUE --> TASK_CONTEXT[完整上下文传递]
    SLACK_H --> TASK_CONTEXT
    GH --> TASK_CONTEXT
    
    SYS_PROMPT --> AGENT[Agent Harness]
    TASK_CONTEXT --> AGENT
    
    AGENT --> EXEC[任务执行]
    
    style CONTEXT fill:#f3e5f5,stroke:#7b1fa2,stroke-width:2px
    style SYS fill:#e1bee7,stroke:#7b1fa2,stroke-width:1px
    style TASK fill:#ce93d8,stroke:#7b1fa2,stroke-width:1px
    style SYS_PROMPT fill:#4caf50,stroke:#2e7d32,stroke-width:1px,color:#fff
    style AGENT fill:#2196f3,stroke:#1565c0,stroke-width:1px,color:#fff
```

---

## 🔧 中间件钩子 (确定性执行)

```mermaid
flowchart LR
    subgraph MW["中间件层 (Deterministic Hooks)"]
        direction TB
        MW1[check_message_queue_before_model<br/>注入中途消息]
        MW2[open_pr_if_needed<br/>PR 安全网]
        MW3[ToolErrorMiddleware<br/>错误处理]
    end
    
    EVENT[事件触发] --> HOOK{钩子类型}
    HOOK -->|模型调用前 | MW1
    HOOK -->|Agent 完成后 | MW2
    HOOK -->|工具失败时 | MW3
    
    MW1 --> INJECT[注入消息到上下文]
    MW2 --> CHECK[检查 PR 条件]
    MW3 --> HANDLE[错误恢复/重试]
    
    INJECT --> AGENT[Agent Harness]
    CHECK --> PR[创建 Draft PR]
    HANDLE --> RETRY[重试/降级]
    
    style MW fill:#fff8e1,stroke:#f57f17,stroke-width:2px
    style EVENT fill:#fff,stroke:#333,stroke-width:1px
    style HOOK fill:#ffeb3b,stroke:#333,stroke-width:2px
    style AGENT fill:#2196f3,stroke:#1565c0,stroke-width:1px,color:#fff
    style PR fill:#4caf50,stroke:#2e7d32,stroke-width:1px,color:#fff
```

---

## 🔍 多层验证流程

```mermaid
flowchart TB
    AGENT[Agent 执行完成] --> LINT[运行 Linter/Formatter]
    LINT --> LINT_CHECK{通过？}
    LINT_CHECK -->|否 | LINT_FIX[自动修复]
    LINT_FIX --> LINT
    LINT_CHECK -->|是 | TEST[运行 Tests]
    
    TEST --> TEST_CHECK{通过？}
    TEST_CHECK -->|否 | TEST_FIX[修复测试]
    TEST_FIX --> TEST
    TEST_CHECK -->|是 | MW[中间件安全网检查]
    
    MW --> MW_CHECK{满足条件？}
    MW_CHECK -->|是，需要 PR| PR[创建 Draft PR]
    MW_CHECK -->|否，无需 PR| DONE[任务完成]
    
    PR --> LINK[链接回原任务]
    LINK --> DONE
    
    style AGENT fill:#fff,stroke:#333,stroke-width:1px
    style LINT fill:#90caf9,stroke:#1565c0,stroke-width:1px
    style TEST fill:#a5d6a7,stroke:#2e7d32,stroke-width:1px
    style MW fill:#ffcc80,stroke:#e65100,stroke-width:1px
    style PR fill:#ce93d8,stroke:#7b1fa2,stroke-width:1px
    style DONE fill:#4caf50,stroke:#2e7d32,stroke-width:2px,color:#fff
```

---

## 🏢 企业对标分析

```mermaid
flowchart TB
    subgraph ENTERPRISE["企业级内部 Agent 模式"]
        direction TB
        
        STRIPE[Stripe Minions<br/>Slack 触发 + AWS EC2 沙箱 + ~500 工具]
        RAMP[Ramp Inspect<br/>Slack+Web + Modal 容器 + OpenCode SDK]
        COINBASE[Coinbase Cloudbot<br/>Slack-Native + 自研沙箱 + MCPs]
    end
    
    OPENSWE[Open SWE<br/>开源统一架构]
    
    STRIPE --> OPENSWE
    RAMP --> OPENSWE
    COINBASE --> OPENSWE
    
    OPENSWE --> PATTERN[提取通用模式]
    PATTERN --> OPEN[开源化]
    
    style ENTERPRISE fill:#ffebee,stroke:#c62828,stroke-width:2px
    style STRIPE fill:#ffcdd2,stroke:#c62828,stroke-width:1px
    style RAMP fill:#ffcdd2,stroke:#c62828,stroke-width:1px
    style COINBASE fill:#ffcdd2,stroke:#c62828,stroke-width:1px
    style OPENSWE fill:#4caf50,stroke:#2e7d32,stroke-width:2px,color:#fff
```

---

## 📐 OpenClaw 适配路线图

```mermaid
gantt
    title OpenClaw 企业级 Agent 框架适配阶段
    dateFormat  YYYY-MM-DD
    section 第一阶段 (本周)
    创建 AGENTS.md 规范          :done,    agents, 2026-03-19, 1d
    实现中间件钩子框架           :active,  mw, 2026-03-19, 2d
    子代理编排优化              :         sub, after mw, 2d
    
    section 第二阶段 (本月)
    Feishu 触发器集成           :         feishu, after sub, 3d
    沙箱隔离评估 (Docker)        :         sandbox, after sub, 5d
    工具精选审查                :         tools, after feishu, 2d
    
    section 第三阶段 (Q2)
    多平台统一路由              :         route, after sandbox, 7d
    安全网中间件 (PR/Commit)     :         safe, after route, 5d
    发布 OpenClaw Agent Framework :         pub, after safe, 3d
```

---

## 📝 图例说明

| 颜色 | 含义 |
|------|------|
| 🟩 绿色 | 成功/完成/安全状态 |
| 🟨 黄色 | 决策点/条件判断 |
| 🟦 蓝色 | 处理步骤/数据流 |
| 🟪 紫色 | 外部集成/API |
| 🟧 橙色 | 配置/中间件 |
| 🟥 红色 | 企业级/警告 |

---

**图表生成**: Aegis-1 (天枢计划执行引擎)  
**Mermaid 版本**: 10.x (GitHub 原生支持)  
**渲染说明**: 将本文件放入 GitHub 仓库即可自动渲染流程图

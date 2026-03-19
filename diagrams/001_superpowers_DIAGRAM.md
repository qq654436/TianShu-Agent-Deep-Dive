# 猎物 #001: obra/superpowers - 架构流程图

**天枢计划 | Mermaid 文本架构图**  
**创建日期**: 2026-03-19  
**原项目**: [obra/superpowers](https://github.com/obra/superpowers)

---

## 🏗️ 核心架构总览

```mermaid
flowchart TB
    subgraph SUPERPOWERS["SUPERPOWERS 框架"]
        direction TB
        
        A[Agent 接收任务] --> B[技能系统扫描上下文]
        B --> C{匹配 description 触发条件？}
        C -->|是 | D[自动注入 SKILL.md 到 System Prompt]
        C -->|否 | E[按默认行为执行]
        D --> F[Agent 按技能规范执行]
        
        style SUPERPOWERS fill:#e1f5ff,stroke:#0066cc,stroke-width:2px
        style A fill:#fff,stroke:#333,stroke-width:1px
        style B fill:#fff,stroke:#333,stroke-width:1px
        style C fill:#ffeb3b,stroke:#333,stroke-width:2px
        style D fill:#4caf50,stroke:#2e7d32,stroke-width:1px,color:#fff
        style E fill:#fff,stroke:#333,stroke-width:1px
        style F fill:#4caf50,stroke:#2e7d32,stroke-width:1px,color:#fff
    end
```

---

## 🔄 技能触发机制

```mermaid
sequenceDiagram
    participant User as 用户
    participant Agent as Agent
    participant SkillSys as 技能系统
    participant SKILL as SKILL.md
    
    User->>Agent: 下达任务指令
    Agent->>SkillSys: 扫描上下文
    SkillSys->>SkillSys: 匹配 description 字段
    alt 触发条件匹配
        SkillSys->>Agent: 注入 SKILL.md 到 Prompt
        Agent->>SKILL: 读取技能规范
        Agent->>Agent: 按技能执行任务
        Agent->>User: 返回合规结果
    else 无匹配
        Agent->>Agent: 按默认行为执行
        Agent->>User: 返回结果 (可能违规)
    end
```

---

## 📋 核心技能矩阵与触发流程

```mermaid
flowchart LR
    subgraph SKILLS["核心技能矩阵"]
        direction TB
        S1[brainstorming<br/>需求模糊时触发]
        S2[writing-plans<br/>设计确认后触发]
        S3[test-driven-development<br/>功能实现前强制触发]
        S4[subagent-driven-development<br/>计划执行时触发]
        S5[requesting-code-review<br/>任务切换时触发]
        S6[writing-skills<br/>创建技能文档时触发]
    end
    
    TASK[任务] --> TRIGGER{触发条件判断}
    TRIGGER -->|需求模糊 | S1
    TRIGGER -->|设计确认 | S2
    TRIGGER -->|功能实现 | S3
    TRIGGER -->|计划执行 | S4
    TRIGGER -->|任务切换 | S5
    TRIGGER -->|创建技能 | S6
    
    S3 --> TDD[TDD 循环<br/>RED→GREEN→REFACTOR]
    S4 --> SUB[子代理分发<br/>两级审查]
    
    style SKILLS fill:#f3e5f5,stroke:#7b1fa2,stroke-width:2px
    style TASK fill:#fff,stroke:#333,stroke-width:1px
    style TRIGGER fill:#ffeb3b,stroke:#333,stroke-width:2px
    style TDD fill:#4caf50,stroke:#2e7d32,stroke-width:1px,color:#fff
    style SUB fill:#2196f3,stroke:#1565c0,stroke-width:1px,color:#fff
```

---

## 🔁 TDD 工作流映射 (技能编写)

```mermaid
flowchart TB
    subgraph TDD["TDD 映射：技能创建"]
        direction TB
        
        START[开始] --> BASELINE[基线测试<br/>无技能时 Agent 行为]
        BASELINE --> FAIL{测试失败？}
        FAIL -->|是，违规 | WRITE[编写 SKILL.md]
        FAIL -->|否，已合规 | SKIP[跳过，无需技能]
        
        WRITE --> INJECT[注入技能到 Prompt]
        INJECT --> VERIFY[验证测试]
        VERIFY --> PASS{测试通过？}
        PASS -->|是 | REFACTOR[优化技能文档<br/>保持合规]
        PASS -->|否 | FIX[修复技能漏洞]
        FIX --> INJECT
        
        REFACTOR --> DONE[✅ 技能完成]
        SKIP --> DONE
        
        style TDD fill:#fff3e0,stroke:#e65100,stroke-width:2px
        style START fill:#fff,stroke:#333,stroke-width:1px
        style BASELINE fill:#ffcc80,stroke:#e65100,stroke-width:1px
        style FAIL fill:#ffeb3b,stroke:#333,stroke-width:2px
        style WRITE fill:#4caf50,stroke:#2e7d32,stroke-width:1px,color:#fff
        style VERIFY fill:#2196f3,stroke:#1565c0,stroke-width:1px,color:#fff
        style PASS fill:#ffeb3b,stroke:#333,stroke-width:2px
        style DONE fill:#4caf50,stroke:#2e7d32,stroke-width:2px,color:#fff
    end
```

---

## 🔍 两级审查流程

```mermaid
flowchart LR
    TASK[任务完成] --> REVIEW1[审查 1: 规范符合性]
    REVIEW1 --> CHECK1{技能规范<br/>全部满足？}
    CHECK1 -->|否 | FIX1[修复违规]
    FIX1 --> REVIEW1
    CHECK1 -->|是 | REVIEW2[审查 2: 代码质量]
    REVIEW2 --> CHECK2{代码质量<br/>达标？}
    CHECK2 -->|否 | FIX2[代码重构]
    FIX2 --> REVIEW2
    CHECK2 -->|是 | NEXT[下一任务]
    
    style TASK fill:#fff,stroke:#333,stroke-width:1px
    style REVIEW1 fill:#90caf9,stroke:#1565c0,stroke-width:1px
    style CHECK1 fill:#ffeb3b,stroke:#333,stroke-width:2px
    style REVIEW2 fill:#a5d6a7,stroke:#2e7d32,stroke-width:1px
    style CHECK2 fill:#ffeb3b,stroke:#333,stroke-width:2px
    style NEXT fill:#4caf50,stroke:#2e7d32,stroke-width:2px,color:#fff
```

---

## 📊 CSO (Claude Search Optimization) 原则

```mermaid
mindmap
  root((CSO 优化))
    Token 效率
      核心技能 <200 词
      避免冗余描述
      关键词前置
    关键词覆盖
      错误消息
      症状描述
      同义词变体
    跨引用机制
      避免@强制加载
      自然语言引用
      上下文关联
```

---

## 🎯 OpenClaw 适配路线图

```mermaid
gantt
    title OpenClaw 适配阶段
    dateFormat  YYYY-MM-DD
    section 第一阶段
    迁移 TDD 技能           :done,    tdd, 2026-03-19, 1d
    迁移 writing-skills     :done,    ws, 2026-03-19, 1d
    创建子代理适配层        :active,  sub, 2026-03-19, 2d
    
    section 第二阶段
    技能自动触发机制        :         trig, after sub, 3d
    技能压力测试框架        :         test, after trig, 3d
    CSO 指南编写           :         cso, after trig, 2d
    
    section 第三阶段
    发布到 ClawHub          :         pub, after test, 2d
    社区贡献流程            :         comm, after pub, 5d
    持续集成压力测试        :         ci, after pub, 5d
```

---

## 📝 图例说明

| 颜色 | 含义 |
|------|------|
| 🟩 绿色 | 合规/成功/完成状态 |
| 🟨 黄色 | 决策点/条件判断 |
| 🟦 蓝色 | 处理步骤/操作 |
| 🟧 橙色 | 警告/基线测试 |
| 🟪 紫色 | 技能矩阵/分组 |

---

**图表生成**: Aegis-1 (天枢计划执行引擎)  
**Mermaid 版本**: 10.x (GitHub 原生支持)  
**渲染说明**: 将本文件放入 GitHub 仓库即可自动渲染流程图

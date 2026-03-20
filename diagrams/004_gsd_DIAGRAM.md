# 猎物 #004: GSD - Mermaid 架构图

**项目**: gsd-build/get-shit-done  
**拆解时间**: 2026-03-20  
**图表数量**: 8 张

---

## 图 1: GSD 系统架构总览

```mermaid
graph TB
    subgraph 用户层
        U[用户输入想法描述]
    end
    
    subgraph 问题引擎
        Q1[分析想法完整性]
        Q2[识别灰色区域]
        Q3[生成澄清问题]
    end
    
    subgraph 研究代理
        R1[并行代理 1: 技术调研]
        R2[并行代理 2: 竞品分析]
        R3[并行代理 3: 最佳实践]
    end
    
    subgraph 上下文工程
        CM[CONTEXT.md<br/>用户偏好捕获]
        SM[STATE.md<br/>项目状态追踪]
    end
    
    subgraph 规划代理
        P1[创建原子任务计划]
        P2[XML 格式化]
        P3[验证计划质量]
    end
    
    subgraph 执行代理
        E1[波次 1: 并行任务]
        E2[波次 2: 依赖任务]
        E3[波次 3: 验证任务]
    end
    
    subgraph 验证代理
        V1[对照需求检查]
        V2[代码质量验证]
        V3[生成原子提交]
    end
    
    subgraph 产出物
        O1[PROJECT.md]
        O2[REQUIREMENTS.md]
        O3[ROADMAP.md]
        O4[可运行代码]
    end
    
    U --> Q1
    Q1 --> Q2 --> Q3
    Q3 --> R1 & R2 & R3
    R1 & R2 & R3 --> CM & SM
    CM & SM --> P1
    P1 --> P2 --> P3
    P3 --> E1 --> E2 --> E3
    E3 --> V1 --> V2 --> V3
    V3 --> O1 & O2 & O3 & O4
    
    style CM fill:#e1f5ff
    style SM fill:#e1f5ff
    style E1 fill:#fff4e1
    style E2 fill:#fff4e1
    style E3 fill:#fff4e1
```

---

## 图 2: 项目初始化流程

```mermaid
sequenceDiagram
    participant U as 用户
    participant Q as 问题引擎
    participant R as 研究代理
    participant P as 规划代理
    
    U->>Q: /gsd:new-project
    Q->>Q: 分析想法完整性
    loop 直到完全理解
        Q->>U: 提问 (目标/约束/技术偏好)
        U->>Q: 回答
    end
    
    Q->>R: 触发并行研究
    R->>R: 代理 1: 技术调研
    R->>R: 代理 2: 竞品分析
    R->>R: 代理 3: 最佳实践
    
    R->>P: 汇总研究报告
    P->>P: 提取需求 (v1/v2/范围外)
    P->>P: 创建阶段路线图
    
    P->>U: 展示路线图请求批准
    U->>P: 批准/修改
    
    P->>P: 生成文件
    Note over P: PROJECT.md<br/>REQUIREMENTS.md<br/>ROADMAP.md<br/>STATE.md
```

---

## 图 3: 讨论阶段详细流程

```mermaid
graph LR
    subgraph 输入
        CMD[/gsd:discuss-phase N/]
        RM[ROADMAP.md<br/>阶段描述]
    end
    
    subgraph 分析
        A1[分析阶段类型]
        A2{类型判断}
    end
    
    subgraph 灰色区域识别
        V1[视觉特性<br/>布局/密度/交互]
        V2[API/CLI<br/>格式/错误处理]
        V3[内容系统<br/>结构/语气/深度]
        V4[组织任务<br/>分组/命名/例外]
    end
    
    subgraph 用户偏好捕获
        U1[用户选择关注区域]
        U2[系统追问细节]
        U3[直到用户满意]
    end
    
    subgraph 输出
        CM[CONTEXT.md<br/>阶段 N 的完整偏好]
    end
    
    CMD --> A1
    RM --> A1
    A1 --> A2
    A2 -->|视觉特性 | V1
    A2 -->|API/CLI| V2
    A2 -->|内容系统 | V3
    A2 -->|组织任务 | V4
    
    V1 & V2 & V3 & V4 --> U1
    U1 --> U2 --> U3
    U3 --> CM
    
    style CM fill:#e1f5ff
    style U3 fill:#e8f5e9
```

---

## 图 4: 规划阶段详细流程

```mermaid
graph TB
    subgraph 输入
        CM[CONTEXT.md<br/>用户偏好]
        RM[REQUIREMENTS.md<br/>需求列表]
        PH[阶段 N 描述]
    end
    
    subgraph 研究步骤
        R1[读取 CONTEXT.md]
        R2[识别关键技术决策]
        R3[并行调研实现方案]
        R4[生成 RESEARCH.md]
    end
    
    subgraph 规划步骤
        P1[基于研究创建计划]
        P2[拆分为 2-3 原子任务]
        P3[XML 格式化计划]
    end
    
    subgraph 验证步骤
        V1{对照需求检查}
        V2{计划可行性}
        V3{上下文窗口适配}
    end
    
    subgraph 输出
        O1[N-RESEARCH.md]
        O2[N-1-PLAN.md]
        O3[N-2-PLAN.md]
    end
    
    CM & RM & PH --> R1
    R1 --> R2 --> R3 --> R4
    R4 --> P1 --> P2 --> P3
    P3 --> V1
    V1 -->|通过 | P3
    V1 -->|失败 | R3
    P3 --> V2
    V2 -->|通过 | V3
    V2 -->|失败 | P2
    V3 -->|通过 | O1 & O2 & O3
    V3 -->|失败 | P2
    
    style V1 fill:#fff4e1
    style V2 fill:#fff4e1
    style V3 fill:#fff4e1
```

---

## 图 5: 执行阶段波次调度

```mermaid
graph TB
    subgraph 阶段 N 执行
        direction TB
        
        subgraph 波次 1 [并行 - 无依赖]
            W1P1[Plan 01<br/>用户模型]
            W1P2[Plan 02<br/>产品模型]
            W1P3[Plan 03<br/>基础架构]
        end
        
        subgraph 波次 2 [并行 - 依赖波次 1]
            W2P1[Plan 04<br/>订单 API]
            W2P2[Plan 05<br/>购物车 API]
            W2P3[Plan 06<br/>认证服务]
        end
        
        subgraph 波次 3 [并行 - 依赖波次 2]
            W3P1[Plan 07<br/>结账 UI]
            W3P2[Plan 08<br/>订单 UI]
            W3P3[Plan 09<br/>支付集成]
        end
        
        subgraph 波次 4 [串行 - 最终验证]
            W4P1[Plan 10<br/>端到端测试]
            W4P2[Plan 11<br/>性能优化]
            W4P3[Plan 12<br/>文档生成]
        end
    end
    
    W1P1 & W1P2 & W1P3 --> W2P1 & W2P2 & W2P3
    W2P1 & W2P2 & W2P3 --> W3P1 & W3P2 & W3P3
    W3P1 & W3P2 & W3P3 --> W4P1 & W4P2 & W4P3
    
    style W1P1 fill:#e8f5e9
    style W1P2 fill:#e8f5e9
    style W1P3 fill:#e8f5e9
    style W2P1 fill:#fff4e1
    style W2P2 fill:#fff4e1
    style W2P3 fill:#fff4e1
    style W3P1 fill:#e1f5ff
    style W3P2 fill:#e1f5ff
    style W3P3 fill:#e1f5ff
    style W4P1 fill:#fce4ec
    style W4P2 fill:#fce4ec
    style W4P3 fill:#fce4ec
```

---

## 图 6: 上下文管理策略对比

```mermaid
graph TB
    subgraph 传统方式 [传统对话方式]
        T1[对话历史 1<br/>5000 tokens]
        T2[对话历史 2<br/>5000 tokens]
        T3[...更多历史]
        T4[当前任务<br/>剩余 tokens]
        
        T1 --> T2 --> T3 --> T4
        T4 --> T5[⚠️ 上下文窗口满]
        T5 --> T6[AI 开始降级行为<br/>"我会更简洁"]
        T6 --> T7[代码质量下降]
    end
    
    subgraph GSD 方式 [GSD 外部化方式]
        G1[CONTEXT.md<br/>关键决策]
        G2[STATE.md<br/>项目状态]
        G3[当前计划<br/>XML 结构]
        G4[新鲜上下文<br/>200k tokens 可用]
        
        G1 & G2 & G3 --> G4
        G4 --> G5[✅ 高质量输出]
        G5 --> G6[原子提交]
    end
    
    style T5 fill:#ffcdd2
    style T6 fill:#ffcdd2
    style T7 fill:#ffcdd2
    style G4 fill:#c8e6c9
    style G5 fill:#c8e6c9
    style G6 fill:#c8e6c9
```

---

## 图 7: 验证代理工作流程

```mermaid
sequenceDiagram
    participant E as 执行代理
    participant V as 验证代理
    participant R as 需求文档
    participant C as 代码库
    participant G as Git
    
    E->>V: 提交完成的任务
    V->>R: 读取 REQUIREMENTS.md
    V->>C: 检查实现代码
    
    alt 需求覆盖检查
        V->>V: 逐条核对需求
        V->>V: 标记未实现项
    end
    
    alt 代码质量检查
        V->>V: 代码规范检查
        V->>V: 错误处理检查
        V->>V: 边界条件检查
    end
    
    alt 测试验证
        V->>V: 运行单元测试
        V->>V: 运行集成测试
    end
    
    V->>V: 汇总验证结果
    
    alt 验证通过
        V->>G: git add .
        V->>G: git commit -m "feat: 任务 N 完成"
        V->>E: ✅ 验证通过
    else 验证失败
        V->>E: ❌ 失败原因列表
        E->>E: 修复问题
        E->>V: 重新提交
    end
```

---

## 图 8: GSD 与天枢计划架构对比

```mermaid
graph TB
    subgraph GSD 架构
        G1[用户输入]
        G2[问题引擎]
        G3[研究代理]
        G4[规划代理]
        G5[执行代理]
        G6[验证代理]
        G7[CONTEXT.md]
        G8[STATE.md]
        
        G1 --> G2 --> G3 --> G4 --> G5 --> G6
        G7 & G8 -.-> G3 & G4 & G5
    end
    
    subgraph 天枢计划架构
        A1[董事会指令]
        A2[主 Agent Aegis-1]
        A3[子代理 sessions_spawn]
        A4[任务执行]
        A5[验证钩子]
        A6[memory/]
        A7[LONG_TERM_MEMORY.md]
        A8[HEARTBEAT.md]
        
        A1 --> A2 --> A3 --> A4 --> A5
        A6 & A7 & A8 -.-> A2 & A3 & A4
    end
    
    subgraph 共同理念
        C1[外部化状态管理]
        C2[多层验证机制]
        C3[子代理编排]
        C4[文档驱动开发]
    end
    
    G7 & G8 --> C1
    A6 & A7 --> C1
    G6 --> C2
    A5 --> C2
    G3 & G4 & G5 --> C3
    A3 --> C3
    G7 & G8 --> C4
    A6 & A7 & A8 --> C4
    
    style G7 fill:#e1f5ff
    style G8 fill:#e1f5ff
    style A6 fill:#e1f5ff
    style A7 fill:#e1f5ff
    style A8 fill:#e1f5ff
    style C1 fill:#fff4e1
    style C2 fill:#fff4e1
    style C3 fill:#fff4e1
    style C4 fill:#fff4e1
```

---

**图表生成完成**: 2026-03-20 08:35 CST  
**生成者**: Aegis-1 👁️

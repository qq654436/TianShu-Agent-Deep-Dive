# 猎物拆解报告 #008 - GitHub Trending AI Agent Top 2

**拆解日期**: 2026-03-24  
**来源**: GitHub Trending  
**猎物选择标准**: 星数增长 + 架构完整性 + OpenClaw 适配价值

---

## 🎯 猎物 A: bytedance/deer-flow

### 基础信息

| 指标 | 数值 |
|------|------|
| **仓库** | https://github.com/bytedance/deer-flow |
| **总星数** | 40,114 ⭐ |
| **今日增长** | 3,546 ⭐ |
| **Fork 数** | 4,722 |
| **语言** | Python |
| **License** | MIT |
| **版本** | 2.0 (重构版) |

### 项目定位

**DeerFlow (Deep Exploration and Efficient Research Flow)** - 字节开源的 SuperAgent Harness，从 Deep Research 框架演进为通用 Agent 运行时。

> "DeerFlow 2.0 is no longer a framework you wire together. It's a super agent harness — batteries included, fully extensible."

### 核心架构

```
┌─────────────────────────────────────────────────────────┐
│                    DeerFlow 2.0                          │
├─────────────────────────────────────────────────────────┤
│                                                          │
│  ┌──────────────┐    ┌──────────────┐    ┌───────────┐  │
│  │ Lead Agent   │───▶│ Sub-Agents   │    │  Memory   │  │
│  │ (Orchestrator)│    │ (Parallel)   │    │ (Persistent)│ │
│  └──────────────┘    └──────────────┘    └───────────┘  │
│         │                   │                    │       │
│         ▼                   ▼                    ▼       │
│  ┌──────────────┐    ┌──────────────┐    ┌───────────┐  │
│  │ Skills       │    │ Tools/MCP    │    │ Sandbox   │  │
│  │ (Markdown)   │    │ (Extensible) │    │ (Docker)  │  │
│  └──────────────┘    └──────────────┘    └───────────┘  │
│         │                   │                    │       │
│         ▼                   ▼                    ▼       │
│  ┌──────────────┐    ┌──────────────┐    ┌───────────┐  │
│  │ IM Channels  │    │ Context Eng. │    │ File Sys  │  │
│  │ (TG/Slack/飞书)│    │ (Summarization)│   │ (/mnt/)   │  │
│  └──────────────┘    └──────────────┘    └───────────┘  │
│                                                          │
└─────────────────────────────────────────────────────────┘
```

### 技术亮点

#### 1. Skills 系统 (核心创新)
- **格式**: Markdown 文件定义工作流 + 最佳实践 + 资源引用
- **加载**: 渐进式加载 (按需加载，非全量)
- **路径**: `/mnt/skills/public/` (内置) + `/mnt/skills/custom/` (用户)
- **内置技能**: research, report-generation, slide-creation, web-page, image-generation

#### 2. 沙箱执行环境
```
/mnt/user-data/
├── uploads/      # 用户上传文件
├── workspace/    # Agent 工作目录
└── outputs/      # 最终交付物
```
- **模式**: Local / Docker / Kubernetes (Provisioner)
- **隔离**: 每任务独立容器，零会话间污染
- **能力**: 文件读写 + Bash 执行 + 代码运行

#### 3. Sub-Agent 架构
- Lead Agent 动态生成 Sub-Agents
- 每个 Sub-Agent 独立上下文 (Isolated Context)
- 并行执行 + 结构化结果汇报
- 支持长任务 (分钟级到小时级)

#### 4. 长期记忆系统
- 跨会话持久化
- 用户画像 + 偏好 + 累积知识
- 去重机制 (避免重复事实累积)
- 本地存储 (用户可控)

#### 5. 上下文工程
- 会话内激进摘要 (Summarization)
- 中间结果卸载到文件系统
- 压缩非即时相关内容
- 适配 Token 敏感模型

#### 6. IM 渠道集成
| 渠道 | 传输方式 | 难度 |
|------|---------|------|
| Telegram | Bot API (长轮询) | Easy |
| Slack | Socket Mode | Moderate |
| 飞书/Lark | WebSocket | Moderate |

#### 7. Claude Code 集成
```bash
npx skills add https://github.com/bytedance/deer-flow --skill claude-to-deerflow
```
- `/claude-to-deerflow` 命令直接交互
- 支持执行模式：flash/standard/pro/ultra
- 文件上传 + 线程管理

### 推荐模型

| 模型 | 推荐理由 |
|------|---------|
| Doubao-Seed-2.0-Code | 字节官方推荐 |
| DeepSeek v3.2 | 长上下文 + 强推理 |
| Kimi 2.5 | 中文优化 |

### 配置示例 (config.yaml)
```yaml
models:
  - name: gpt-4
    display_name: GPT-4
    use: langchain_openai:ChatOpenAI
    model: gpt-4
    api_key: $OPENAI_API_KEY
    max_tokens: 4096
    temperature: 0.7

channels:
  feishu:
    enabled: true
    app_id: $FEISHU_APP_ID
    app_secret: $FEISHU_APP_SECRET
  telegram:
    enabled: true
    bot_token: $TELEGRAM_BOT_TOKEN
```

### 启动方式
```bash
# Docker (推荐)
make docker-init    # 拉取沙箱镜像
make docker-start   # 启动服务

# 本地开发
make check          # 检查依赖
make install        # 安装依赖
make dev            # 启动服务

# 访问：http://localhost:2026
```

### 嵌入式 Python 客户端
```python
from deerflow.client import DeerFlowClient

client = DeerFlowClient()
response = client.chat("Analyze this paper", thread_id="my-thread")

# 流式输出
for event in client.stream("hello"):
    if event.type == "messages-tuple" and event.data.get("type") == "ai":
        print(event.data["content"])
```

### 与 OpenClaw 的协同点

| DeerFlow 能力 | OpenClaw 对应 | 适配价值 |
|--------------|--------------|---------|
| Skills 系统 | 技能文件 (SKILL.md) | ⭐⭐⭐ 可直接复用格式 |
| 沙箱执行 | exec 工具 | ⭐⭐ OpenClaw 已有类似能力 |
| Sub-Agents | sessions_spawn | ⭐⭐⭐ 架构高度一致 |
| IM 渠道 | Feishu/Telegram 工具 | ⭐⭐⭐ 可直接集成 |
| 长期记忆 | LONG_TERM_MEMORY.md | ⭐⭐ 理念相同 |
| 上下文工程 | AGENTS.md 规范 | ⭐⭐ 可借鉴摘要策略 |

---

## 🎯 猎物 B: browser-use/browser-use

### 基础信息

| 指标 | 数值 |
|------|------|
| **仓库** | https://github.com/browser-use/browser-use |
| **总星数** | 83,834 ⭐ |
| **今日增长** | 1,157 ⭐ |
| **Fork 数** | 9,739 |
| **语言** | Python |
| **License** | MIT |

### 项目定位

**Browser-Use** - 让网站对 AI Agent 可访问，轻松实现在线任务自动化。

> "Make websites accessible for AI agents. Automate tasks online with ease."

### 核心架构

```
┌─────────────────────────────────────────────────────────┐
│                   Browser-Use                            │
├─────────────────────────────────────────────────────────┤
│                                                          │
│  ┌──────────────┐    ┌──────────────┐    ┌───────────┐  │
│  │ Agent        │───▶│ Browser      │    │  LLM      │  │
│  │ (Task Runner)│    │ (Controller) │    │  Provider │  │
│  └──────────────┘    └──────────────┘    └───────────┘  │
│         │                   │                    │       │
│         ▼                   ▼                    ▼       │
│  ┌──────────────┐    ┌──────────────┐    ┌───────────┐  │
│  │ Tools        │    │ DOM Parser   │    │  Cloud    │  │
│  │ (Custom)     │    │ (Aria/Role)  │    │  (Optional)│ │
│  └──────────────┘    └──────────────┘    └───────────┘  │
│         │                   │                    │       │
│         ▼                   ▼                    ▼       │
│  ┌──────────────┐    ┌──────────────┐    ┌───────────┐  │
│  │ Actions      │    │ Screenshots  │    │  Proxy    │  │
│  │ (Click/Type) │    │ (State)      │    │  Rotation │  │
│  └──────────────┘    └──────────────┘    └───────────┘  │
│                                                          │
└─────────────────────────────────────────────────────────┘
```

### 技术亮点

#### 1. 极简 API 设计
```python
from browser_use import Agent, Browser, ChatBrowserUse
import asyncio

async def main():
    browser = Browser(
        # use_cloud=True,  # 可选：使用云端浏览器
    )
    
    agent = Agent(
        task="Find the number of stars of the browser-use repo",
        llm=ChatBrowserUse(),
        browser=browser,
    )
    await agent.run()

if __name__ == "__main__":
    asyncio.run(main())
```

#### 2. 多 LLM 支持
```python
# ChatBrowserUse (官方优化，3-5x 更快)
llm=ChatBrowserUse()

# Google Gemini
llm=ChatGoogle(model='gemini-3-flash-preview')

# Anthropic Claude
llm=ChatAnthropic(model='claude-sonnet-4-6')
```

#### 3. 自定义工具扩展
```python
from browser_use import Tools

tools = Tools()

@tools.action(description='Description of what this tool does.')
def custom_tool(param: str) -> str:
    return f"Result: {param}"

agent = Agent(
    task="Your task",
    llm=llm,
    browser=browser,
    tools=tools,
)
```

#### 4. CLI 交互式调试
```bash
browser-use open https://example.com    # 导航到 URL
browser-use state                      # 查看可点击元素
browser-use click 5                    # 点击元素 (按索引)
browser-use type "Hello"               # 输入文本
browser-use screenshot page.png        # 截图
browser-use close                      # 关闭浏览器
```

#### 5. Claude Code Skill 集成
```bash
mkdir -p ~/.claude/skills/browser-use
curl -o ~/.claude/skills/browser-use/SKILL.md \
  https://raw.githubusercontent.com/browser-use/browser-use/main/skills/browser-use/SKILL.md
```

#### 6. 云端服务 (Browser Use Cloud)
| 特性 | 开源版 | 云端版 |
|------|-------|-------|
| 浏览器管理 | 自托管 | 托管 |
| 代理轮换 | ❌ | ✅ |
| CAPTCHA 解决 | ❌ | ✅ |
| 1000+ 集成 | ❌ | ✅ |
| 持久化存储 | ❌ | ✅ |
| 并行执行 | 手动 | 自动 |

#### 7. 真实浏览器 Profile 复用
```python
# 复用现有 Chrome Profile (保存的登录状态)
browser = Browser(
    profile_path="/path/to/chrome/profile",
)
```

### 使用场景演示

1. **求职申请自动化**: 自动填写申请表 + 上传简历
2. ** grocery 购物**: 自动选购商品 + 结算
3. **PC 配件比价**: 跨站比价 + 库存监控

### 定价 (ChatBrowserUse 模型)

| Token 类型 | 价格 (每 1M) |
|-----------|-------------|
| Input | $0.20 |
| Cached Input | $0.02 |
| Output | $2.00 |

### 与 OpenClaw 的协同点

| Browser-Use 能力 | OpenClaw 对应 | 适配价值 |
|-----------------|--------------|---------|
| 浏览器自动化 | browser 工具 | ⭐⭐⭐ 可直接增强 |
| CLI 交互 | exec 工具 | ⭐⭐ 可借鉴命令设计 |
| Claude Code Skill | 技能文件 | ⭐⭐⭐ 格式可直接复用 |
| 自定义工具 | exec/工具扩展 | ⭐⭐ 理念一致 |
| 云端服务 | 无 | ⭐⭐⭐ 可考虑集成云服务 |
| DOM 解析 | browser snapshot | ⭐⭐ 可优化引用系统 |

---

## 📊 综合对比分析

| 维度 | DeerFlow | Browser-Use | OpenClaw 适配优先级 |
|------|----------|-------------|-------------------|
| **架构完整性** | ⭐⭐⭐⭐⭐ | ⭐⭐⭐⭐ | - |
| **学习曲线** | 中等 | 低 | - |
| **文档质量** | ⭐⭐⭐⭐ | ⭐⭐⭐⭐⭐ | - |
| **社区活跃度** | 高 (字节背书) | 极高 | - |
| **技能系统** | Markdown Skills | Claude Code Skills | ⭐⭐⭐⭐⭐ |
| **沙箱执行** | Docker/K8s | 本地/云端 | ⭐⭐⭐ |
| **IM 集成** | TG/Slack/飞书 | 无 | ⭐⭐⭐⭐ |
| **浏览器自动化** | 无 | ⭐⭐⭐⭐⭐ | ⭐⭐⭐⭐⭐ |
| **长期记忆** | ✅ | ❌ | ⭐⭐⭐ |
| **Sub-Agent** | ✅ | ❌ | ⭐⭐⭐⭐ |

---

## 🎯 OpenClaw 适配建议

### 高优先级 (立即实施)

1. **Skills 格式标准化**
   - 借鉴 DeerFlow 的 Markdown Skills 格式
   - 统一 SKILL.md 结构 (工作流 + 最佳实践 + 资源)
   - 实现渐进式加载 (按需读取技能文件)

2. **Browser-Use 集成**
   - 将 browser-use 作为 Python 依赖安装
   - 创建 `browser-automation` 技能文件
   - 增强现有 browser 工具的 DOM 引用系统

3. **Sub-Agent 架构优化**
   - 借鉴 DeerFlow 的 Isolated Context 设计
   - 实现 Sub-Agent 上下文隔离
   - 添加结构化结果汇报机制

### 中优先级 (本周内)

4. **IM 渠道增强**
   - 完善飞书/Telegram 双向通信
   - 实现命令系统 (`/new`, `/status`, `/memory`)
   - 添加会话管理 (Thread 管理)

5. **长期记忆系统**
   - 实现记忆去重机制
   - 添加用户偏好持久化
   - 优化 LONG_TERM_MEMORY.md 更新策略

### 低优先级 (未来规划)

6. **沙箱执行环境**
   - 评估 Docker 沙箱集成
   - 实现任务级隔离
   - 添加文件系统设计 (`/mnt/workspace/`)

7. **云端服务**
   - 评估 Browser Use Cloud API 集成
   - 考虑 OpenClaw 云端部署方案

---

## 💡 关键洞察

### 1. Skills 是 Agent 的核心竞争力
- DeerFlow 和 Browser-Use 都采用 **Markdown Skills** 格式
- Skills 定义工作流而非代码，降低使用门槛
- 技能市场/生态是未来竞争点

### 2. 浏览器自动化是刚需
- Browser-Use 83k+ 星数证明市场需求
- OpenClaw 的 browser 工具需要增强
- 考虑集成 Browser-Use Cloud API

### 3. Sub-Agent 架构是趋势
- DeerFlow 的 Lead Agent + Sub-Agents 模式
- 适合长任务分解和并行执行
- OpenClaw 的 sessions_spawn 需要优化

### 4. IM 渠道是用户入口
- DeerFlow 支持 TG/Slack/飞书
- OpenClaw 已有 Feishu/Telegram 工具
- 需要完善命令系统和会话管理

### 5. 记忆系统是差异化关键
- DeerFlow 的跨会话记忆
- OpenClaw 的 LONG_TERM_MEMORY.md 是雏形
- 需要实现去重和智能更新

---

## 📝 下一步行动

1. **创建 OpenClaw 适配技能** → `tian_shu/skills/`
2. **绘制 Mermaid 架构图** → `tian_shu/diagrams/`
3. **生成分发内容** → `tian_shu/distribution/`
4. **更新长期记忆** → `LONG_TERM_MEMORY.md`

---

**报告完成时间**: 2026-03-24 12:30 CST  
**拆解者**: Sovereign Subagent (Prey #008)

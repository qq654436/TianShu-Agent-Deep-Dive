# OpenClaw Skill: sovereign-sandbox

**技能名称**: sovereign-sandbox  
**版本**: 1.0.0  
**作者**: Sovereign (S.V.) 👁️  
**灵感来源**: langchain-ai/open-swe  
**创建日期**: 2026-03-20

---

## 📖 技能描述

为 OpenClaw Agent 提供安全代码执行环境，包括：
- 云沙箱隔离执行
- 确定性 Middleware 钩子
- AGENTS.md 规范注入
- 多触发器路由 (Feishu/Telegram/GitHub)

---

## 🎯 使用场景

1. **安全代码执行**: 在隔离沙箱中运行不可信代码
2. **自动化 PR**: 自动提交代码并创建 GitHub PR
3. **团队协作**: Slack/Feishu 触发编码任务
4. **规范遵循**: 注入仓库级编码规范 (AGENTS.md)

---

## 🚀 安装方法

```bash
# 通过 ClawHub 安装 (推荐)
clawhub install sovereign-sandbox

# 或手动安装
git clone https://github.com/aether-sync/sovereign-sandbox \
  ~/.openclaw/workspace/agents/sovereign/skills/sovereign-sandbox

# 配置沙箱提供商
export SANDBOX_PROVIDER=modal  # 或 daytona/runloop/langsmith
export MODAL_TOKEN_ID=xxx
export MODAL_TOKEN_SECRET=xxx
```

---

## 📋 命令列表

### `/sandbox exec` - 在沙箱中执行命令

```bash
# 执行单条命令
/sandbox exec "npm test"

# 指定沙箱 ID (复用现有沙箱)
/sandbox exec --sandbox sb-001 "python test.py"

# 超时设置 (秒)
/sandbox exec --timeout 60 "long_running_task.sh"
```

### `/sandbox create` - 创建新沙箱

```bash
# 创建默认沙箱
/sandbox create

# 指定提供商
/sandbox create --provider modal

# 预克隆仓库
/sandbox create --repo aether-sync/openclaw

# 设置生命周期 (小时)
/sandbox create --ttl 24
```

### `/sandbox list` - 查看活跃沙箱

```bash
# 列出所有沙箱
/sandbox list

# 仅显示运行中
/sandbox list --status running

# JSON 输出
/sandbox list --json
```

### `/pr create` - 创建 Pull Request

```bash
# 自动提交并开 PR
/pr create --title "Fix authentication bug" --body "Resolves #123"

# Draft 模式 (默认)
/pr create --draft

# 指定分支
/pr create --branch feature/new-auth

# 指定仓库
/pr create --repo aether-sync/openclaw
```

### `/agents configure` - 配置 AGENTS.md

```bash
# 读取当前 AGENTS.md
/agents show

# 验证语法
/agents validate

# 重新加载
/agents reload
```

---

## ⚙️ 配置选项

### 配置文件：`sandbox-config.json`

```json
{
  "sandbox": {
    "defaultProvider": "modal",
    "autoCreate": true,
    "ttl": 3600,
    "recreateOnUnreachable": true,
    "providers": {
      "modal": {
        "token_id": "${MODAL_TOKEN_ID}",
        "token_secret": "${MODAL_TOKEN_SECRET}",
        "image": "python:3.11",
        "memory": 2048,
        "cpu": 2
      },
      "daytona": {
        "api_key": "${DAYTONA_API_KEY}",
        "target": "us-east-1"
      },
      "runloop": {
        "api_key": "${RUNLOOP_API_KEY}"
      },
      "langsmith": {
        "api_key": "${LANGSMITH_API_KEY}"
      }
    }
  },
  "middleware": {
    "enabled": true,
    "hooks": [
      "check_message_queue_before_model",
      "open_pr_if_needed",
      "tool_error_handler",
      "rate_limiter"
    ]
  },
  "agents": {
    "enabled": true,
    "configFile": "AGENTS.md",
    "injectToSystemPrompt": true
  },
  "github": {
    "enabled": true,
    "oauth_token": "${GITHUB_TOKEN}",
    "autoOpenPR": true,
    "defaultDraft": true,
    "requireTests": true
  },
  "triggers": {
    "feishu": {
      "enabled": true,
      "bot_name": "@Sovereign"
    },
    "telegram": {
      "enabled": true,
      "bot_name": "@sovereign_bot"
    },
    "github": {
      "enabled": true,
      "app_name": "@openswe"
    }
  }
}
```

### 配置项说明

| 选项 | 类型 | 默认值 | 说明 |
|------|------|--------|------|
| `sandbox.defaultProvider` | string | "modal" | 默认沙箱提供商 |
| `sandbox.autoCreate` | boolean | true | 任务自动创建沙箱 |
| `sandbox.ttl` | number | 3600 | 沙箱生命周期 (秒) |
| `sandbox.recreateOnUnreachable` | boolean | true | 不可达时自动重建 |
| `middleware.enabled` | boolean | true | 启用 Middleware 钩子 |
| `middleware.hooks` | array | [...] | 启用的钩子列表 |
| `agents.enabled` | boolean | true | 启用 AGENTS.md 注入 |
| `agents.configFile` | string | "AGENTS.md" | 规范文件名 |
| `github.autoOpenPR` | boolean | true | 自动创建 PR |
| `github.defaultDraft` | boolean | true | 默认 Draft 模式 |
| `github.requireTests` | boolean | true | PR 前必须通过测试 |

---

## 🔧 技术实现

### 架构

```
┌─────────────────────────────────────────────────────────┐
│                  触发层 (Triggers)                       │
│  Feishu Bot │ Telegram Bot │ GitHub App                 │
└─────────────────────┬───────────────────────────────────┘
                      │
                      ▼
┌─────────────────────────────────────────────────────────┐
│              路由层 (Router)                             │
│  - 确定性 thread ID 生成                                  │
│  - Follow-up 消息路由                                    │
│  - 多平台统一接口                                        │
└─────────────────────┬───────────────────────────────────┘
                      │
                      ▼
┌─────────────────────────────────────────────────────────┐
│           编排层 (LangGraph + Deep Agents)               │
│  - 主 Agent (协调)                                       │
│  - 子代理 (并行任务)                                     │
│  - Middleware 钩子                                       │
└─────────────────────┬───────────────────────────────────┘
                      │
                      ▼
┌─────────────────────────────────────────────────────────┐
│              沙箱层 (Sandbox Providers)                  │
│  Modal │ Daytona │ Runloop │ LangSmith                  │
└─────────────────────────────────────────────────────────┘
```

### 核心模块

#### 1. 沙箱管理器
```python
class SandboxManager:
    def __init__(self, provider='modal'):
        self.provider = self._init_provider(provider)
        self.active_sandboxes = {}
    
    def create(self, repo=None, ttl=3600):
        sandbox = self.provider.create_container(
            image='python:3.11',
            ttl=ttl
        )
        if repo:
            sandbox.exec(f'git clone {repo}')
        self.active_sandboxes[sandbox.id] = sandbox
        return sandbox
    
    def exec(self, sandbox_id, command, timeout=60):
        sandbox = self.active_sandboxes[sandbox_id]
        return sandbox.exec(command, timeout=timeout)
    
    def destroy(self, sandbox_id):
        sandbox = self.active_sandboxes.pop(sandbox_id)
        sandbox.destroy()
```

#### 2. Middleware 钩子
```python
class MiddlewareStack:
    def __init__(self, hooks):
        self.hooks = hooks
    
    async def before_model(self, agent_state):
        for hook in self.hooks:
            if hasattr(hook, 'before_model'):
                await hook.before_model(agent_state)
    
    async def after_agent(self, agent_state):
        for hook in self.hooks:
            if hasattr(hook, 'after_agent'):
                await hook.after_agent(agent_state)

# 示例：自动 PR 钩子
class OpenPRIfNeeded:
    async def after_agent(self, agent_state):
        if agent_state.has_changes and not agent_state.pr_created:
            await github.create_pr(
                branch=agent_state.branch,
                title=agent_state.pr_title,
                draft=True
            )
```

#### 3. AGENTS.md 注入器
```python
class AgentsConfigInjector:
    def __init__(self, repo_path):
        self.config_path = os.path.join(repo_path, 'AGENTS.md')
    
    def load(self):
        if os.path.exists(self.config_path):
            with open(self.config_path) as f:
                return f.read()
        return None
    
    def inject(self, system_prompt):
        config = self.load()
        if config:
            return f"{system_prompt}\n\n# Repository Guidelines\n{config}"
        return system_prompt
```

#### 4. 触发器路由器
```python
class TriggerRouter:
    def __init__(self):
        self.thread_agents = {}  # thread_id -> agent
    
    def get_or_create_agent(self, platform, thread_id, context):
        key = f"{platform}:{thread_id}"
        if key not in self.thread_agents:
            agent = self._create_agent(context)
            self.thread_agents[key] = agent
        return self.thread_agents[key]
    
    def route_followup(self, platform, thread_id, message):
        key = f"{platform}:{thread_id}"
        agent = self.thread_agents.get(key)
        if agent:
            agent.queue_message(message)
```

---

## 📊 沙箱提供商对比

| 提供商 | 冷启动 | 价格 | 优势 | 适用场景 |
|--------|--------|------|------|----------|
| **Modal** | 5-10s | $0.000028/s | 易用，Python 原生 | 开发/测试 |
| **Daytona** | 3-5s | $0.00003/s | 预warm，快速 | 生产环境 |
| **Runloop** | 2-5s | 定制报价 | 企业级支持 | 企业部署 |
| **LangSmith** | 5-8s | 包含在套餐 | LangChain 生态 | LangChain 用户 |

---

## 🔌 API 集成

### Webhook 触发

```json
// POST /webhook/sandbox-task
{
  "platform": "feishu",
  "thread_id": "7123456789",
  "message": "@Sovereign fix the login bug",
  "repo": "aether-sync/openclaw",
  "context": {
    "user_id": "ou_xxx",
    "chat_id": "oc_xxx"
  }
}
```

### 回调通知

```json
// POST /webhook/sandbox-complete
{
  "task_id": "task-001",
  "status": "completed",
  "sandbox_id": "sb-001",
  "result": {
    "pr_url": "https://github.com/aether-sync/openclaw/pull/123",
    "tests_passed": true,
    "changes": ["auth.ts", "login.py"]
  }
}
```

---

## ⚠️ 注意事项

1. **成本控制**: 沙箱按运行时间计费，设置合理 TTL
2. **安全性**: 沙箱内无生产环境访问权限
3. **冷启动延迟**: 首次创建沙箱需 5-10 秒
4. **并发限制**: 各提供商有并发沙箱数量限制

---

## 🐛 故障排除

### 沙箱创建失败

```bash
# 检查凭证
echo $MODAL_TOKEN_ID
echo $MODAL_TOKEN_SECRET

# 测试连接
/sandbox test-connection --provider modal
```

### PR 创建失败

```bash
# 检查 GitHub Token 权限
# 需要：repo, workflow

# 验证 Token
/sandbox github verify-token
```

### AGENTS.md 未生效

```bash
# 检查文件位置
ls -la AGENTS.md

# 验证语法
/agents validate

# 重新加载
/agents reload
```

---

## 📈 版本历史

| 版本 | 日期 | 变更 |
|------|------|------|
| 1.0.0 | 2026-03-20 | 初始版本 |

---

## 📝 开发指南

### 本地开发

```bash
cd ~/.openclaw/workspace/agents/sovereign/skills/sovereign-sandbox
pip install -e .
pytest tests/
```

### 添加新沙箱提供商

```python
# 实现 SandboxProvider 接口
class MyProvider(SandboxProvider):
    def create(self, **kwargs): ...
    def exec(self, command, **kwargs): ...
    def destroy(self): ...

# 注册提供商
register_provider('myprovider', MyProvider)
```

### 发布

```bash
clawhub publish ./sovereign-sandbox
```

---

## 📄 许可证

MIT License - 与 open-swe 保持一致

---

## 🔗 参考

- 灵感来源：https://github.com/langchain-ai/open-swe
- LangGraph: https://langchain-ai.github.io/langgraph/
- Deep Agents: https://github.com/langchain-ai/deepagents
- Modal: https://modal.com
- Daytona: https://www.daytona.io

---

**维护者**: Sovereign (S.V.) 👁️  
**联系**: Feishu @Sovereign  
**状态**: 🟢 Active

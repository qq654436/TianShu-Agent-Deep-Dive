# DeerFlow 适配技能

**技能名称**: deerflow-integration  
**版本**: 1.0.0  
**兼容性**: Aether-Sync v1.2+  
**作者**: Sovereign (S.V.) 👁️  
**来源**: 天枢计划猎物 #010

---

## 🎯 技能目标

将 DeerFlow 的核心能力集成到 Aether-Sync，提供:
- Sandbox 执行环境 (Docker 隔离)
- 渐进式技能加载
- Sub-Agent 动态生成
- 多 Channel IM 集成

---

## 📦 安装

```bash
# 通过 ClawHub 安装
npx clawhub install deerflow-integration

# 或手动安装
git clone https://github.com/aether-sync/tian_shu.git
cp tian_shu/skills/deerflow-integration ~/.openclaw/skills/
```

---

## 🔧 配置

### 1. Sandbox 配置

```yaml
# config.yaml
sandbox:
  mode: docker  # local | docker | kubernetes
  docker:
    image: deerflow-sandbox:latest
    network: host
    volumes:
      - ./workspace:/mnt/user-data/workspace
      - ./uploads:/mnt/user-data/uploads
      - ./outputs:/mnt/user-data/outputs
  kubernetes:
    provisioner_url: http://localhost:8080
    namespace: deerflow
```

### 2. 技能配置

```yaml
# config.yaml
skills:
  progressive_loading: true
  paths:
    public: /mnt/skills/public
    custom: /mnt/skills/custom
  built_in:
    - research
    - report-generation
    - slide-creation
    - web-page
    - image-generation
```

### 3. Channel 配置

```yaml
# config.yaml
channels:
  langgraph_url: http://localhost:2024
  gateway_url: http://localhost:8001
  
  feishu:
    enabled: true
    app_id: $FEISHU_APP_ID
    app_secret: $FEISHU_APP_SECRET
  
  slack:
    enabled: true
    bot_token: $SLACK_BOT_TOKEN
    app_token: $SLACK_APP_TOKEN
  
  telegram:
    enabled: true
    bot_token: $TELEGRAM_BOT_TOKEN
```

---

## 🚀 使用

### 基础用法

```bash
# 启动 DeerFlow 服务
make docker-start

# 或通过 Python 客户端
python -c "
from deerflow.client import DeerFlowClient
client = DeerFlowClient()
response = client.chat('分析这篇论文', thread_id='task-1')
print(response)
"
```

### Claude Code 集成

```bash
# 安装技能
npx skills add https://github.com/bytedance/deer-flow --skill claude-to-deerflow

# 在 Claude Code 中使用
/claude-to-deerflow send "研究 AI Agent 趋势" --mode pro
```

### Sub-Agent 生成

```python
# Lead Agent 动态生成 Sub-Agent
from deerflow.agents import LeadAgent

lead = LeadAgent()
sub_agents = lead.spawn_sub_agents(
    task="研究 AI Agent 市场趋势",
    count=5,
    parallel=True
)

# Sub-Agent 并行执行
results = await asyncio.gather(*[
    sub_agent.execute() for sub_agent in sub_agents
])

# Lead Agent 收敛结果
final_report = lead.synthesize(results)
```

---

## 🛠️ 工具集

### 内置工具

| 工具 | 描述 | 示例 |
|------|------|------|
| `web_search` | 网络搜索 | `web_search("AI Agent trends 2026")` |
| `web_fetch` | 网页抓取 | `web_fetch("https://example.com")` |
| `file_read` | 文件读取 | `file_read("/mnt/workspace/report.md")` |
| `file_write` | 文件写入 | `file_write("/mnt/workspace/output.md", content)` |
| `bash_exec` | Bash 执行 | `bash_exec("git status")` |
| `image_view` | 图像理解 | `image_view("/mnt/uploads/chart.png")` |

### MCP 工具

```yaml
# MCP 服务器配置
mcp:
  servers:
    - name: deerflow-gateway
      url: http://localhost:8001
      transport: http
    - name: deerflow-langgraph
      url: http://localhost:2024
      transport: sse
```

---

## 📁 技能结构

```
/mnt/skills/
├── public/
│   ├── research/
│   │   └── SKILL.md          # 研究技能
│   ├── report-generation/
│   │   └── SKILL.md          # 报告生成技能
│   ├── slide-creation/
│   │   └── SKILL.md          # PPT 创建技能
│   ├── web-page/
│   │   └── SKILL.md          # 网页生成技能
│   └── image-generation/
│       └── SKILL.md          # 图像生成技能
└── custom/
    └── your-skill/
        └── SKILL.md          # 自定义技能
```

### SKILL.md 模板

```markdown
# 技能名称

## 目标
[描述技能目标]

## 工作流
1. [步骤 1]
2. [步骤 2]
3. [步骤 3]

## 最佳实践
- [最佳实践 1]
- [最佳实践 2]

## 参考资源
- [链接 1]
- [链接 2]

## 工具依赖
- [工具 1]
- [工具 2]
```

---

## 🔒 安全

### Sandbox 隔离

- 每个任务运行在独立 Docker 容器
- 文件系统隔离 (`/mnt/user-data/`)
- 网络隔离 (可选)
- 审计日志 (所有操作记录)

### 权限控制

```yaml
# config.yaml
security:
  sandbox:
    allow_network: true
    allow_filesystem: true
    allowed_paths:
      - /mnt/user-data/workspace
      - /mnt/user-data/uploads
      - /mnt/user-data/outputs
    forbidden_paths:
      - /etc
      - /root
      - /home
  api_keys:
    - name: OPENAI_API_KEY
      required: false
    - name: TAVILY_API_KEY
      required: true
```

---

## 📊 性能优化

### Context Engineering

```python
# 会话内激进总结
from deerflow.context import ContextManager

ctx = ContextManager()
ctx.summarize_completed_tasks()
ctx.offload_to_filesystem("intermediate_results.json")
ctx.compress_irrelevant_context()
```

### Token 优化

```python
# 渐进式技能加载
from deerflow.skills import SkillLoader

loader = SkillLoader()
skills = loader.load_on_demand("research")  # 仅加载研究技能
# 而非 loader.load_all()
```

---

## 🐛 故障排除

### 常见问题

**Q: Docker 权限错误**
```bash
# Linux: 添加用户到 docker group
sudo usermod -aG docker $USER
# 重新登录
```

**Q: 技能加载失败**
```bash
# 检查技能路径
ls -la /mnt/skills/public/
# 验证 SKILL.md 格式
cat /mnt/skills/public/research/SKILL.md
```

**Q: Channel 连接失败**
```bash
# 检查配置
cat config.yaml | grep -A 5 "channels:"
# 验证 API Keys
echo $FEISHU_APP_ID
```

---

## 📚 参考

- [DeerFlow 官方文档](https://deerflow.tech)
- [GitHub 仓库](https://github.com/bytedance/deer-flow)
- [配置指南](https://github.com/bytedance/deer-flow/blob/main/backend/docs/CONFIGURATION.md)
- [MCP 服务器指南](https://github.com/bytedance/deer-flow/blob/main/backend/docs/MCP_SERVER.md)
- [贡献指南](https://github.com/bytedance/deer-flow/blob/main/CONTRIBUTING.md)

---

## 🔄 更新日志

### v1.0.0 (2026-03-26)
- 初始版本
- Sandbox 执行环境集成
- 渐进式技能加载
- Sub-Agent 动态生成
- 多 Channel IM 支持

---

**技能状态**: ✅ 生产就绪  
**最后更新**: 2026-03-26  
**维护者**: Aether-Sync Team

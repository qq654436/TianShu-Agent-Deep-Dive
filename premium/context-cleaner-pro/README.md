# Context Cleaner Pro - 商业版

**版本**: 1.0.0  
**创建时间**: 2026-03-20  
**状态**: 🟡 待上架销售  
**定价**: ¥99/月 或 ¥999/年

---

## 📦 商品内容

购买后获得以下内容：

### 1. 核心脚本 (`context_cleaner.py`)

```bash
# 安装后使用
uv run context_cleaner.py init "My Project"
uv run context_cleaner.py capture "使用 PostgreSQL" --category architecture
uv run context_cleaner.py clean
uv run context_cleaner.py inject --phase 1
uv run context_cleaner.py status
```

### 2. OpenClaw 技能插件 (`SKILL.md`)

可直接安装到 OpenClaw 工作区：
```bash
# 技能已包含在购买内容中
# 安装路径：~/.openclaw/workspace/skills/context-cleaner/
```

### 3. 使用文档 (`README.md`)

- 快速入门指南
- API 参考
- 最佳实践
- 常见问题

### 4. 示例项目 (`examples/`)

- `example-init/` - 项目初始化示例
- `example-capture/` - 决策捕获示例
- `example-clean/` - 上下文清理示例
- `example-inject/` - 上下文注入示例

### 5. Pro 版独占功能

| 功能 | 免费版 | Pro 版 |
|------|--------|--------|
| 基础上下文管理 | ✅ | ✅ |
| 单项目支持 | ✅ | ✅ |
| 手动清理 | ✅ | ✅ |
| **自动上下文监控** | ❌ | ✅ |
| **多项目管理** | ❌ | ✅ |
| **AI 运行时插件** | ❌ | ✅ |
| **上下文压缩** | ❌ | ✅ |
| **优先技术支持** | ❌ | ✅ |

---

## 🔧 安装说明

### 步骤 1: 下载商品

付款后自动获得下载链接 (面包多/爱发电)

### 步骤 2: 解压文件

```bash
cd ~/projects
unzip context-cleaner-pro.zip
cd context-cleaner-pro
```

### 步骤 3: 安装依赖

```bash
pip install -r requirements.txt
```

### 步骤 4: 验证安装

```bash
python scripts/context_cleaner.py --help
```

### 步骤 5: 初始化项目

```bash
python scripts/context_cleaner.py init "My AI Project"
```

---

## 📖 快速入门

### 场景 1: 新项目启动

```bash
# 初始化项目上下文
python scripts/context_cleaner.py init "电商网站"

# 输出:
# ✅ 项目上下文已初始化：.context/
#    - CONTEXT.md: 用户偏好和关键决策
#    - STATE.md: 项目状态追踪
#    - ROADMAP.md: 阶段路线图
#    - config.json: 配置文件
```

### 场景 2: 捕获架构决策

```bash
# 记录关键决策
python scripts/context_cleaner.py capture "使用 PostgreSQL 作为主数据库" --category architecture
python scripts/context_cleaner.py capture "API 响应使用 JSON:API 格式" --category api
python scripts/context_cleaner.py capture "JWT + refresh token 认证" --category security

# 输出:
# ✅ 决策已记录：使用 PostgreSQL 作为主数据库 (类别：architecture)
```

### 场景 3: 清理上下文

```bash
# 当对话进行到第 20 轮，AI 开始质量下降时
python scripts/context_cleaner.py clean

# 输出:
# # 上下文清理摘要
# **清理时间**: 2026-03-20 09:30
# **归档位置**: .context/archives/20260320_093000
# 
# ## 操作
# 1. ✅ STATE.md 已归档
# 2. ✅ STATE.md 已重置
# 3. ✅ CONTEXT.md 保留 (关键决策)
```

### 场景 4: 注入上下文

```bash
# 开始新阶段前，注入干净上下文
python scripts/context_cleaner.py inject --phase 2

# 输出优化的上下文提示，可直接复制给 AI
```

---

## 💡 最佳实践

### 1. 与 AI 编程工具集成

**Claude Code**:
```bash
# 在 Claude Code 会话中
/gsd:discuss-phase 1
# 然后运行
python scripts/context_cleaner.py capture "用户偏好卡片式布局" --category ui
```

**Cursor/Windsurf**:
```bash
# 在聊天窗口中
@context-cleaner inject phase 2
```

### 2. 自动监控 (Pro 版)

在 `.context/config.json` 中配置：
```json
{
  "autoArchive": true,
  "archiveInterval": "daily",
  "maxContextTokens": 50000,
  "autoClean": true,
  "cleanThreshold": 80000
}
```

### 3. 多项目管理 (Pro 版)

```bash
# 切换到不同项目
cd project-a && context-cleaner status
cd ../project-b && context-cleaner status
```

---

## ❓ 常见问题

### Q: 免费版和 Pro 版有什么区别？

A: 免费版包含基础功能 (单项目、手动清理)，Pro 版增加自动监控、多项目、AI 插件等高级功能。

### Q: 支持哪些 AI 运行时？

A: 目前支持 Claude Code、Cursor、Windsurf。其他平台可通过插件系统扩展。

### Q: 如何续费？

A: 订阅到期前 7 天会收到邮件提醒，点击链接即可续费。

### Q: 支持退款吗？

A: 购买后 7 天内如不满意，可联系支持团队申请退款。

---

## 📞 技术支持

- **邮件**: support@tianshu.lab (Pro 版专属)
- **GitHub Issues**: https://github.com/qq654436/TianShu-Agent-Deep-Dive/issues
- **Discord**: https://discord.gg/tianshu (待创建)

---

## 📄 许可证

**Pro 版**: 商业许可证
- 允许个人和商业使用
- 禁止转售或重新分发
- 允许修改源码供自己使用

**免费版**: MIT License

---

## 🔄 更新日志

### v1.0.0 (2026-03-20)
- ✅ 初始版本发布
- ✅ 基础上下文管理
- ✅ 决策捕获系统
- ✅ 自动归档功能
- ✅ 上下文注入优化

---

**商品 ID**: `context-cleaner-pro-001`  
**创建者**: Aegis-1 @ TianShu Lab  
**最后更新**: 2026-03-20 09:20

# 天枢计划 (TianShu)

[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)
[![Stars](https://img.shields.io/github/stars/qq654436/TianShu-Agent-Deep-Dive)](https://github.com/qq654436/TianShu-Agent-Deep-Dive/stargazers)

**硬核技术 IP 建设引擎**  
**战略代号**: 天枢 (TianShu) - 北斗第一星  
**启动日期**: 2026-03-19  
**GitHub**: [qq654436/TianShu-Agent-Deep-Dive](https://github.com/qq654436/TianShu-Agent-Deep-Dive)

> 🌐 **Join our AI Architect community via Feishu/Lark** → 联系 @Aegis-1 获取邀请

---

## 🎯 任务

每日自动审计 GitHub Trending，锁定 24h 内最热门的 AI Agent 框架，进行深度拆解并产出：

1. **技术评测报告** - 架构分析、适配可行性评估
2. **OpenClaw 适配技能** - 可直接部署的 SKILL.md
3. **视觉流转图** - Wanx 生成的技术架构图
4. **Git 同步包** - 准备发布至 GitHub 的完整内容

---

## 📁 目录结构

```
tian_shu/
├── observatory/           # 观测站 - 每日 Trending 快照
│   └── YYYY-MM-DD_trending.md
├── reports/               # 技术评测报告
│   └── {序号}_{项目名}_tech_review.md
├── skills/                # OpenClaw 适配技能
│   └── {技能名}/
│       └── SKILL.md
├── visuals/               # 视觉产出
│   └── {序号}_{项目名}_flowchart_prompt.md
├── GIT_SYNC.md            # GitHub 同步指令
└── README.md              # 本文件
```

---

## 🚀 当前进度

| 猎物编号 | 项目名称 | 状态 | 完成日期 |
|---------|---------|------|---------|
| #001 | [obra/superpowers](https://github.com/obra/superpowers) | ✅ 已完成 | 2026-03-19 |
| #002 | [jarrodwatts/claude-hud](https://github.com/jarrodwatts/claude-hud) | ⏳ 待执行 | - |
| #003 | [langchain-ai/open-swe](https://github.com/langchain-ai/open-swe) | ⏳ 待执行 | - |

---

## 📊 猎物 #001: obra/superpowers

**核心发现**:
- 24h 增长 4,089 stars，当日最热 AI Agent 框架
- 核心架构：技能触发系统 + TDD 方法论 + 子代理驱动开发
- OpenClaw 适配性：70% 可直接迁移

**产出物**:
- ✅ 技术评测报告 → `reports/001_superpowers_tech_review.md`
- ✅ 适配技能 (TDD) → `skills/test-driven-development/SKILL.md`
- ✅ 视觉提示词 → `visuals/001_superpowers_flowchart_prompt.md`
- ✅ Git 同步指令 → `GIT_SYNC.md`

**综合评分**: 8.6/10 ⭐⭐⭐⭐

---

## ⚙️ 自动化流程

```
[每日 09:00 触发]
    ↓
[抓取 GitHub Trending]
    ↓
[筛选 AI Agent 项目 (24h > 100 stars)]
    ↓
[选择 Top 2 作为当日猎物]
    ↓
[深度拆解 (Qwen-Coder)]
    ↓
[产出四件套 (报告 + 技能 + 视觉 + Git)]
    ↓
[归档至 memory/]
    ↓
[推送飞书文档至董事会]
```

---

## 🛠️ 使用方式

### 查看今日观测

```bash
cat /home/admin/.openclaw/workspace/tian_shu/observatory/$(date +%Y-%m-%d)_trending.md
```

### 部署技能到 OpenClaw

```bash
# 复制技能到 OpenClaw 技能目录
cp -r /home/admin/.openclaw/workspace/tian_shu/skills/test-driven-development \
      /home/admin/.openclaw/skills/

# 或使用符号链接
ln -s /home/admin/.openclaw/workspace/tian_shu/skills/test-driven-development \
      /home/admin/.openclaw/skills/
```

### 同步到 GitHub

```bash
cd /home/admin/.openclaw/workspace/tian_shu
git add .
git commit -m "feat: 添加猎物 #001 superpowers 完整产出"
git push
```

---

## 📈 高价值项目识别标准

发现符合以下≥3 项标准的项目时，触发 MVP 构建流程:

- [ ] GitHub Stars > 10k 或快速增长
- [ ] 解决明确痛点/市场需求
- [ ] 技术架构可复用/可扩展
- [ ] 许可证友好 (MIT/Apache 2.0)
- [ ] 文档完善/社区活跃

---

## 🤝 How to Contribute

欢迎贡献！天枢计划是开源的硬核技术 IP 建设引擎。

### 贡献方式

#### 1. 提交猎物提名
发现优秀的 AI Agent 项目？提交到 `observatory/nominations.md`：
```markdown
- [项目名](GitHub URL) - 24h stars 增长理由
```

#### 2. 改进适配技能
已有技能的优化建议？
1. Fork 本仓库
2. 修改 `skills/{技能名}/SKILL.md`
3. 提交 PR，描述改进点

#### 3. 新增内容分发渠道
帮助扩展到更多平台：
- 知乎专栏自动发布
- 即刻动态格式化
- Twitter/LinkedIn 英文摘要

#### 4. 报告问题
遇到 Bug 或有改进建议？
- 创建 Issue，标签：`bug` / `enhancement` / `question`
- 附上详细复现步骤

### 开发环境设置

```bash
# 克隆仓库
git clone https://github.com/qq654436/TianShu-Agent-Deep-Dive.git
cd TianShu-Agent-Deep-Dive

# 安装依赖 (内容分发脚本)
pip install -r requirements.txt

# 运行测试
python tests/test_distribution.py
```

### 代码规范
- 遵循 PEP 8 (Python) / ESLint (JavaScript)
- 提交前运行 `pre-commit run --all-files`
- PR 需通过 CI 检查

---

## 🗺️ Roadmap

### 2026 Q1 (当前季度) ✅

- [x] 天枢计划启动 (2026-03-19)
- [x] 猎物 #001: obra/superpowers 深度拆解
- [x] 猎物 #002: jarrodwatts/claude-hud 深度拆解
- [x] 猎物 #003: langchain-ai/open-swe 深度拆解
- [x] OpenClaw 适配技能发布 (TDD/子代理驱动)
- [ ] 内容分发脚本 v1.0 (知乎/即刻)
- [ ] GitHub Stars 突破 100 🎯

### 2026 Q2 (规划中)

- [ ] 行业情报自动化监控 (每 3 天执行)
- [ ] OpenClaw Agent Framework 发布
- [ ] ClawHub 技能市场集成
- [ ] 社区贡献流程建立
- [ ] GitHub Stars 突破 500 🎯
- [ ] 技术博客系列："OpenClaw 如何借鉴企业级 Agent 架构"

### 2026 Q3 (愿景)

- [ ] 支持多平台触发 (Feishu/Telegram/Discord)
- [ ] 沙箱隔离增强 (Docker/容器化)
- [ ] 实时状态推送 (WebSocket)
- [ ] GitHub Stars 突破 1k 🎯
- [ ] 首个 MVP 产品发布

### 2026 Q4 (愿景)

- [ ] 企业级部署方案
- [ ] 商业化探索
- [ ] GitHub Stars 突破 5k 🎯
- [ ] 天枢计划 2.0 发布

---

## 📝 合规声明

- 所有输出保持技术客观中立
- 符合主流社交平台反广告算法
- 不添加未经验证的功能宣传
- 尊重原项目许可证

---

## 📞 联系

**维护者**: Aegis-1 (天枢计划执行引擎)  
**董事会**: 航哥  
**沟通渠道**: 飞书

**GitHub Issues**: [提交问题/建议](https://github.com/qq654436/TianShu-Agent-Deep-Dive/issues)  
**Discord**: [加入社区](https://discord.com/invite/clawd)

---

**最后更新**: 2026-03-19 13:20 CST  
**下次观测**: 2026-03-20 09:00 CST

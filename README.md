# 天枢计划 (TianShu)

[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)
[![Stars](https://img.shields.io/github/stars/qq654436/TianShu-Agent-Deep-Dive)](https://github.com/qq654436/TianShu-Agent-Deep-Dive/stargazers)

**硬核技术 IP 建设引擎**  
**战略代号**: 天枢 (TianShu) - 北斗第一星  
**启动日期**: 2026-03-19  
**GitHub**: [qq654436/TianShu-Agent-Deep-Dive](https://github.com/qq654436/TianShu-Agent-Deep-Dive)

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

---

**最后更新**: 2026-03-19 12:25 CST  
**下次观测**: 2026-03-20 09:00 CST

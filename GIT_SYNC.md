# 天枢计划 - GitHub 同步指令
**版本**: 1.0  
**最后更新**: 2026-03-19 12:20 CST

---

## 📁 目录结构

```
tian_shu/
├── observatory/           # 观测站数据
│   └── 2026-03-19_trending.md
├── reports/               # 技术评测报告
│   └── 001_superpowers_tech_review.md
├── skills/                # OpenClaw 适配技能
│   └── test-driven-development/
│       └── SKILL.md
├── visuals/               # 视觉产出
│   └── 001_superpowers_flowchart_prompt.md
├── GIT_SYNC.md            # 本文件
└── README.md              # 项目说明 (待创建)
```

---

## 🔧 Git 同步指令

### 首次初始化

```bash
cd /home/admin/.openclaw/workspace/tian_shu

# 初始化 Git 仓库
git init

# 创建 .gitignore
cat > .gitignore << 'EOF'
# 临时文件
*.tmp
*.log

# 敏感信息
*.key
*.env

# 大型二进制文件 (可选)
*.png
*.jpg
*.svg
EOF

# 首次提交
git add .
git commit -m "天枢计划初始化 - 猎物 #001: obra/superpowers

- 观测站：GitHub Trending 每日监控
- 技术评测：superpowers 架构拆解
- 技能适配：TDD for OpenClaw
- 视觉提示：Wanx 生成指令

战略代号：TianShu (天枢)
"

# 关联远程仓库 (需先创建)
# git remote add origin https://github.com/{your-org}/tian-shu.git
# git push -u origin main
```

### 日常更新

```bash
cd /home/admin/.openclaw/workspace/tian_shu

# 查看变更
git status

# 添加变更
git add .

# 提交 (使用 Conventional Commits 格式)
git commit -m "feat: 添加猎物 #002 claude-hud 评测报告"

# 或
git commit -m "docs: 更新 GIT_SYNC.md 同步指令"

# 推送
git push
```

### 每日观测站自动提交

```bash
# 创建 cron 任务 (每日 09:00)
crontab -e

# 添加:
0 9 * * * cd /home/admin/.openclaw/workspace/tian_shu && \
    git pull && \
    git add observatory/ && \
    git commit -m "chore(observatory): daily trending snapshot $(date +\%Y-\%m-\%d)" && \
    git push
```

---

## 📝 提交信息规范

采用 [Conventional Commits](https://www.conventionalcommits.org/):

| 类型 | 说明 | 示例 |
|------|------|------|
| `feat` | 新功能 | `feat: 添加子代理驱动开发技能` |
| `fix` | 修复 | `fix: 修正 TDD 技能触发条件` |
| `docs` | 文档 | `docs: 更新 README 安装说明` |
| `chore` | 日常维护 | `chore: 更新观测站数据` |
| `refactor` | 重构 | `refactor: 优化技能目录结构` |
| `test` | 测试 | `test: 添加技能压力测试用例` |

---

## 🌿 分支策略

```
main          - 稳定版本，已发布内容
  │
  ├── dev     - 开发分支，日常提交
  │
  └── feature/{skill-name}  - 功能分支，独立技能开发
```

**工作流**:
```bash
# 开发新技能
git checkout -b feature/writing-skills dev
# ... 开发 ...
git commit -m "feat: 完成 writing-skills 初稿"
git checkout dev
git merge feature/writing-skills
git branch -d feature/writing-skills

# 发布到 main
git checkout main
git merge dev
git push origin main
```

---

## 📦 GitHub 仓库建议

### 仓库名称
- `tian-shu` (天枢拼音)
- `openclaw-superpowers` (强调适配)
- `agent-skills-lab` (通用名称)

### 仓库描述
```
天枢计划 | OpenClaw 技能实验室
每日审计 GitHub Trending，深度拆解 AI Agent 框架，产出 OpenClaw 适配技能。

战略方向：硬核技术 IP 建设
```

### 推荐标签
```
openclaw, ai-agent, skills, tdd, automation, github-trending, chinese
```

### LICENSE 选择
- **MIT** - 最宽松，适合技能分享
- **Apache 2.0** - 包含专利授权
- **CC-BY-4.0** - 文档类内容

---

## 🔐 安全注意事项

1. **不提交**:
   - API Keys / 令牌
   - 个人身份信息
   - 飞书/钉钉 webhook URL
   - 服务器 IP/凭证

2. **脱敏处理**:
   - 使用 `***` 替换敏感值
   - 使用环境变量示例

3. **审查工具**:
   ```bash
   # 提交前扫描
   git log --all --full-history -- "*.key" "*.env" "*.pem"
   
   # 或使用 git-secrets
   git secrets --install
   git secrets --register-aws
   ```

---

## 📊 同步检查清单

发布前确认:

- [ ] 所有 `.md` 文件无敏感信息
- [ ] 提交信息符合规范
- [ ] 目录结构清晰
- [ ] README.md 包含项目说明
- [ ] LICENSE 文件存在
- [ ] .gitignore 配置正确
- [ ] 远程仓库已创建
- [ ] 推送成功

---

**维护者**: Aegis-1 (天枢计划执行引擎)  
**联系方式**: 飞书 @航哥  
**最后审查**: 2026-03-19

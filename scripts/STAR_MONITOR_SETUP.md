# Star 监控脚本 - 部署指南

## 📋 功能

- 每 4 小时自动检查 GitHub 仓库 Stars 数
- Stars > 1 时自动推送飞书喜报
- 自动记录到 LONG_TERM_MEMORY.md
- 里程碑检测 (1/10/50/100/500/1000/5000)

## ⚙️ 配置

### 1. 环境变量

创建 `.env` 文件或设置系统环境变量：

```bash
# GitHub API Token (可选，无 token 时速率限制 60 次/小时)
export GITHUB_TOKEN="ghp_xxxxxxxxxxxxxxxxxxxx"

# 飞书 Webhook (可选，无 webhook 时仅记录日志)
export FEISHU_WEBHOOK="https://open.feishu.cn/open-apis/bot/v2/hook/xxxxxxxxxxxxx"
```

### 2. 获取 GitHub Token

1. 访问 https://github.com/settings/tokens
2. 点击 "Generate new token (classic)"
3. 无需勾选任何权限 (公开仓库读取无需权限)
4. 复制 token 并保存到环境变量

### 3. 获取飞书 Webhook

1. 在飞书群聊中添加 "自定义机器人"
2. 复制 Webhook 地址
3. 保存到环境变量

## 🚀 部署方式

### 方式 1: Cron 定时任务 (推荐)

编辑 crontab：
```bash
crontab -e
```

添加以下行 (每 4 小时执行一次)：
```cron
0 */4 * * * cd /home/admin/.openclaw/workspace/tian_shu && /usr/bin/python3 scripts/star_monitor.py --check-only >> logs/star_monitor.log 2>&1
```

### 方式 2: 后台持续运行

```bash
cd /home/admin/.openclaw/workspace/tian_shu
nohup python3 scripts/star_monitor.py --interval 14400 > logs/star_monitor.log 2>&1 &
```

### 方式 3: 手动测试

```bash
cd /home/admin/.openclaw/workspace/tian_shu
python3 scripts/star_monitor.py --check-only
```

## 📁 文件结构

```
scripts/
├── star_monitor.py          # 主脚本
├── STAR_MONITOR_SETUP.md    # 本文件
└── .star_monitor_state.json # 状态文件 (自动生成)
```

## 📊 输出示例

### 控制台输出
```
[2026-03-19 13:30:00] 开始检查 Stars...
📊 当前 Stars: 5 (上次：3, 增长：2)
🎉 检测到 Star 增长！
✅ 飞书喜报已发送
✅ LONG_TERM_MEMORY.md 已更新
✅ 检查完成，状态已保存
```

### 飞书喜报
```
🎉 喜报！天枢计划 Stars 突破 5！

⭐ 仓库：qq654436/TianShu-Agent-Deep-Dive
📊 当前 Stars: 5
📈 新增：+2
⏰ 时间：2026-03-19 13:30:00

[🔗 查看仓库]
```

## 🔧 故障排查

### 问题 1: 获取 Stars 失败
```
❌ 获取 Stars 失败：HTTPSConnectionPool...
```
**解决**: 检查网络连接，或设置 GITHUB_TOKEN 提高速率限制

### 问题 2: 飞书推送失败
```
⚠️  FEISHU_WEBHOOK 未配置，跳过推送
```
**解决**: 设置 FEISHU_WEBHOOK 环境变量

### 问题 3: requests 库未安装
```
⚠️  requests 库未安装，跳过推送
```
**解决**: `pip install requests`

---

**维护者**: Aegis-1  
**最后更新**: 2026-03-19

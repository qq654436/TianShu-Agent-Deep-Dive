# 小红书云端分发环境

**天枢计划 · 内容分发渠道**  
**状态**: 🧪 实验阶段  
**创建日期**: 2026-03-19

---

## ⚠️ 合规声明

小红书无官方公开 API，自动化登录可能违反平台 ToS。

**使用建议**:
- 仅用于企业账号管理
- 控制发布频率 (每日≤3 篇)
- 避免触发风控
- 优先使用官方企业服务平台

---

## 📁 目录结构

```
red/
├── README.md                 # 本文件
├── login_helper.py           # 登录助手 (二维码生成)
├── red_renderer.py           # 云端渲染引擎 (水印/标题)
├── red_distributor.py        # 分发器 (与 star_monitor 集成)
└── output/                   # 渲染输出目录
```

---

## 🚀 快速开始

### 1. 环境准备

```bash
# 安装依赖
pip3 install --user selenium pillow requests

# 安装浏览器 (二选一)
# Chrome:
sudo yum install chromium chromedriver

# Firefox:
sudo yum install firefox geckodriver
```

### 2. 登录小红书

```bash
cd /home/admin/.openclaw/workspace/tian_shu/red

# 生成二维码并等待扫码
python3 login_helper.py --wait --timeout 300

# 或仅生成二维码 (不等待)
python3 login_helper.py --no-wait
```

**流程**:
1. 脚本启动无头浏览器
2. 访问小红书登录页
3. 截图二维码
4. 飞书推送通知
5. 用户扫码登录
6. 保存会话到 `auth/red_session.json`

### 3. 检查会话状态

```bash
python3 login_helper.py --check
```

### 4. 渲染封面图

```bash
# 纯文字标题卡片
python3 red_renderer.py --title-only --title "24h 狂揽 4k Stars！这个 AI 框架太猛了"

# 底图 + 标题 + 水印
python3 red_renderer.py --input base_image.png --title "爆款标题" --output output.png
```

### 5. 分发内容

```bash
# 从技术报告生成分发内容
python3 red_distributor.py --report ../reports/001_superpowers_tech_review.md

# 自动登录 + 分发
python3 red_distributor.py --report <报告> --auto-login

# 查看分发记录
python3 red_distributor.py --list-records
```

---

## 🔄 与 Star 监控集成

修改 `star_monitor.py`，在检测到新 Stars 时触发分发：

```python
# 在 star_monitor.py 的 run_check() 函数中
if increase > 0 and current_stars > 1:
    # ... 现有逻辑 ...
    
    # 触发分发 (如果有新报告)
    reports_dir = Path(__file__).parent / "reports"
    latest_report = get_latest_report(reports_dir)
    if latest_report:
        subprocess.run([
            sys.executable,
            str(RED_DIR / "red_distributor.py"),
            "--report", str(latest_report)
        ])
```

---

## 📊 会话管理

### 会话文件位置
`/home/admin/.openclaw/workspace/auth/red_session.json`

### 会话内容
```json
{
  "cookies": [...],
  "local_storage": {...},
  "url": "https://www.xiaohongshu.com/",
  "timestamp": "2026-03-19T13:53:00",
  "user_agent": "..."
}
```

### 会话有效期
- **建议**: 24 小时内
- **实际**: 取决于小红书 Cookie 策略
- **刷新**: 重新运行 `login_helper.py`

---

## 🎨 渲染配置

### 品牌水印
- **文字**: `天枢计划 | TianShu`
- **Emoji**: 👁️
- **位置**: bottom-right (可配置)
- **透明度**: 180/255

### 标题样式
- **字体大小**: 48px (可配置)
- **位置**: top/center/bottom
- **背景**: 半透明黑色
- **文字**: 白色

---

## 🔧 故障排查

### 问题 1: 浏览器启动失败
```
❌ 无法启动浏览器：Message: unknown error: cannot find Chrome binary
```
**解决**:
```bash
# 安装 Chrome
sudo yum install chromium

# 或指定路径
export CHROME_BIN=/usr/bin/chromium
```

### 问题 2: ChromeDriver 未找到
```
❌ ChromeDriver 未找到
```
**解决**:
```bash
sudo yum install chromedriver
# 或
wget https://chromedriver.storage.googleapis.com/<version>/chromedriver_linux64.zip
unzip chromedriver_linux64.zip
sudo mv chromedriver /usr/local/bin/
```

### 问题 3: 二维码无法扫描
**原因**:
- 页面未完全加载
- 分辨率问题

**解决**:
```bash
# 增加等待时间
python3 login_helper.py --timeout 600

# 手动检查截图
cat auth/red_qr_code.png
```

### 问题 4: 会话快速过期
**原因**: 小红书安全策略

**解决**:
- 每次分发前检查会话
- 使用企业账号 (更稳定)
- 避免频繁登录/登出

---

## 📝 分发记录

记录文件：`red/distribution_records.json`

格式:
```json
[
  {
    "timestamp": "2026-03-19T14:00:00",
    "report": "reports/001_superpowers_tech_review.md",
    "project": "obra/superpowers",
    "title": "🔥 24h 狂揽 4k Stars！这个 AI 框架太猛了",
    "cover": "red/output_20260319_140000.png",
    "status": "ready",
    "content": "..."
  }
]
```

---

## 🎯 最佳实践

1. **定时登录**: 每日 09:00 检查会话，过期重新登录
2. **批量渲染**: 一次性生成多篇封面图
3. **内容审核**: 飞书审核后发布
4. **频率控制**: 每日≤3 篇，避免风控
5. **数据追踪**: 记录每篇的点赞/收藏/评论

---

## 🔗 相关文档

- [star_monitor.py](../scripts/star_monitor.py) - Star 监控脚本
- [distribution_helper.py](../distribution/distribution_helper.py) - 知乎/即刻分发助手
- [HEARTBEAT.md](../../HEARTBEAT.md) - 周期性任务配置

---

**维护者**: Aegis-1  
**最后更新**: 2026-03-19  
**状态**: 🧪 实验阶段 (需手动发布)

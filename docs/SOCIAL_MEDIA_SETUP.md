# 社交媒体发布配置指南

**版本**: 1.0  
**更新**: 2026-03-28 14:40 CST  
**状态**: ✅ 免费方案

---

## 🎯 方案选择

### 已实现 (立即可用)
| 平台 | 方案 | 配置难度 | 状态 |
|------|------|---------|------|
| 飞书 | OpenClaw message tool | 无 | ✅ 完成 |
| 掘金 | Cookie API | 低 | ⏳ 待配置 |

### 待实现 (本周)
| 平台 | 方案 | 配置难度 | 状态 |
|------|------|---------|------|
| 微博 | 浏览器+Cookie | 中 | ⏳ 待配置 |
| 知乎 | 浏览器+Cookie | 中 | ⏳ 待配置 |
| V2EX | 浏览器+Cookie | 低 | ⏳ 待配置 |
| Twitter | MCPSearch/浏览器 | 中 | ⏳ 待调研 |

---

## 🔧 配置步骤

### 1. 飞书 (已完成)
无需配置，使用 OpenClaw 内置 message tool。

---

### 2. 掘金 (推荐配置)

**步骤**:

1. 登录 https://juejin.cn/
2. 打开开发者工具 (F12)
3. Application → Cookies → 复制 `token` 值
4. 添加到环境变量

```bash
# ~/.bashrc 或 ~/.zshrc
export JUEJIN_TOKEN="your_token_here"
```

**测试**:
```bash
cd tian_shu
python scripts/free_publisher.py 012
```

---

### 3. 微博

**步骤**:

1. 登录 https://weibo.com/
2. 打开开发者工具 (F12)
3. Application → Cookies → 复制 `SUB` 和 `SUBP` 值
4. 安装 Selenium: `pip install selenium`
5. 配置环境变量

```bash
export WEIBO_COOKIE="your_cookie_here"
```

**注意**: 需要 ChromeDriver
```bash
# Ubuntu/Debian
sudo apt install chromium-chromedriver

# macOS
brew install chromedriver
```

---

### 4. 知乎

**步骤**:

1. 登录 https://zhihu.com/
2. 打开开发者工具 (F12)
3. Application → Cookies → 复制 `z_c0` 值
4. 配置环境变量

```bash
export ZHIHU_COOKIE="your_cookie_here"
```

---

### 5. V2EX

**步骤**:

1. 登录 https://v2ex.com/
2. 打开开发者工具 (F12)
3. Application → Cookies → 复制 `A2` 值
4. 配置环境变量

```bash
export V2EX_COOKIE="your_cookie_here"
```

---

## 📝 环境变量模板

创建 `~/.openclaw_env`:

```bash
# 社交媒体发布配置
# 复制此文件到 ~/.bashrc 或 ~/.zshrc

# 掘金 (推荐配置)
JUEJIN_TOKEN=""

# 微博 (可选)
WEIBO_COOKIE=""

# 知乎 (可选)
ZHIHU_COOKIE=""

# V2EX (可选)
V2EX_COOKIE=""

# Twitter (可选，待实现)
TWITTER_COOKIE=""
```

**应用配置**:
```bash
source ~/.openclaw_env
```

---

## 🚀 使用方法

### 基础用法
```bash
# 发布猎物 #012
cd /home/admin/.openclaw/workspace/agents/sovereign/tian_shu
python scripts/free_publisher.py 012
```

### 指定内容文件
```bash
python scripts/free_publisher.py 012 distribution/prey_012_ready_to_post.md
```

### 发布到指定平台
```bash
# 修改脚本中的 publish_all 方法，注释不需要的平台
```

---

## 📊 发布记录

**记录文件**: `distribution_records.json`

**查询**:
```bash
cat distribution_records.json | python -m json.tool
```

**格式**:
```json
{
  "records": [
    {
      "timestamp": "2026-03-28T14:40:00",
      "prey_id": "012",
      "platform": "feishu",
      "status": "success",
      "content_preview": "🔥 GitHub Trending...",
      "error": ""
    }
  ]
}
```

---

## ⚠️ 注意事项

1. **Cookie 有效期**: 
   - 掘金：约 30 天
   - 微博：约 7 天
   - 知乎：约 30 天
   - V2EX: 会话期

2. **发布频率**:
   - 建议每个平台每天 ≤5 条
   - 避免被判定为垃圾内容

3. **内容审核**:
   - 各平台有不同的内容政策
   - 避免敏感话题

4. **IP 限制**:
   - 高频发布可能触发 IP 限制
   - 建议使用代理

---

## 🔗 相关脚本

| 脚本 | 功能 | 状态 |
|------|------|------|
| `free_publisher.py` | 免费发布器 | ✅ 完成 |
| `auto_publisher.py` | 自动化发布器 | ⏳ 待集成 |
| `distribution_helper.py` | 内容格式化 | ✅ 完成 |

---

## 📝 待办事项

- [ ] 配置掘金 Cookie (P0, 今天)
- [ ] 安装 Selenium (P1, 今天)
- [ ] 配置微博 Cookie (P1, 本周)
- [ ] 配置知乎 Cookie (P1, 本周)
- [ ] 配置 V2EX Cookie (P2, 本周)
- [ ] 实现微博自动发布 (P1, 本周)
- [ ] 实现知乎自动发布 (P1, 本周)
- [ ] 实现 V2EX 自动发布 (P2, 本周)
- [ ] 调研 Twitter 免费方案 (P2, 下周)

---

**维护者**: Sovereign (S.V.) 👁️  
**最后更新**: 2026-03-28 14:40 CST

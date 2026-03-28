# 天枢计划 - 自动化发布系统配置指南

**创建时间**: 2026-03-28 14:25 CST  
**版本**: 1.0  
**状态**: ✅ 基础功能可用 (飞书) / ⏳ 高级功能待配置

---

## 📋 系统架构

```
┌─────────────────────────────────────────────────────────┐
│                   自动化发布系统                         │
├─────────────────────────────────────────────────────────┤
│                                                         │
│  [内容源] → [解析器] → [发布器] → [目标平台]             │
│     ↓           ↓          ↓           ↓                │
│  Markdown   Twitter    飞书 API    飞书 (✅)           │
│  文件       微博       Twitter     Twitter (⏳)        │
│           知乎       浏览器      微博 (⏳)             │
│           掘金       自动化      知乎 (⏳)             │
│           V2EX                   掘金 (⏳)             │
│                                V2EX (⏳)               │
│                                                         │
└─────────────────────────────────────────────────────────┘
```

---

## ✅ 已实现功能

### 1. 飞书推送 (立即可用)

**状态**: ✅ 已完成  
**配置**: 无需额外配置 (使用 OpenClaw message tool)  
**用法**: 猎物分析完成后自动推送

**示例**:
```python
# 在猎物分析脚本末尾添加
from auto_publisher import AutoPublisher

publisher = AutoPublisher()
publisher.publish_all("012", "distribution/prey_012_ready_to_post.md")
```

---

## ⏳ 待配置功能

### 2. Twitter 自动发布

**方案 A: Twitter API v2** (推荐)

**所需凭证**:
- API Key
- API Secret
- Access Token
- Access Token Secret

**申请流程**:
1. 访问 https://developer.twitter.com/
2. 创建项目和应用
3. 获取 API 凭证
4. 填入 `.env` 文件

**配置**:
```bash
# .env 文件
TWITTER_API_KEY=your_api_key
TWITTER_API_SECRET=your_api_secret
TWITTER_ACCESS_TOKEN=your_access_token
TWITTER_ACCESS_TOKEN_SECRET=your_access_token_secret
```

**依赖安装**:
```bash
pip install tweepy
```

---

**方案 B: 浏览器自动化** (备选)

**所需**:
- Selenium
- ChromeDriver
- Twitter Cookie (需手动登录一次)

**依赖安装**:
```bash
pip install selenium
```

**配置**:
```bash
# 保存 Cookie 到文件
# 手动登录 Twitter 后导出 Cookie
```

---

### 3. 微博自动发布

**方案 A: 微博开放平台 API**

**所需凭证**:
- App Key
- App Secret
- Access Token

**申请流程**:
1. 访问 https://open.weibo.com/
2. 创建应用
3. 申请权限 (发布微博)
4. 获取 API 凭证

**配置**:
```bash
# .env 文件
WEIBO_APP_KEY=your_app_key
WEIBO_APP_SECRET=your_app_secret
WEIBO_ACCESS_TOKEN=your_access_token
```

---

**方案 B: 浏览器自动化**

类似 Twitter，使用 Selenium + Cookie

---

### 4. 知乎自动发布

**方案**: 浏览器自动化 (知乎 API 不对外开放)

**所需**:
- Selenium
- 知乎 Cookie
- 手动登录一次

**发布类型**:
- 知乎想法 (短内容)
- 知乎文章 (长内容)

---

### 5. 掘金自动发布

**方案 A: Cookie + API** (推荐)

**所需**:
- 掘金 Cookie (包含 `token` 字段)

**获取方法**:
1. 登录 https://juejin.cn/
2. 打开开发者工具 → Application → Cookies
3. 复制 `token` 值

**配置**:
```bash
# .env 文件
JUEJIN_TOKEN=your_token
```

---

**方案 B: 浏览器自动化**

类似其他平台

---

### 6. V2EX 自动发布

**方案**: 浏览器自动化 (V2EX 无官方 API)

**所需**:
- Selenium
- V2EX Cookie
- 手动登录一次

**注意**: V2EX 有反自动化机制，需谨慎使用

---

## 🔧 使用指南

### 基础用法

```bash
# 发布到所有已配置平台
python tian_shu/scripts/auto_publisher.py --prey-id 012

# 发布到指定平台
python tian_shu/scripts/auto_publisher.py --prey-id 012 --platform feishu
python tian_shu/scripts/auto_publisher.py --prey-id 012 --platform twitter

# 指定内容文件
python tian_shu/scripts/auto_publisher.py --prey-id 012 --file distribution/prey_012_ready_to_post.md
```

### 集成到猎物分析流程

修改 `tian_shu/scripts/generate_posts.py`:

```python
# 在文件末尾添加
from auto_publisher import AutoPublisher

def main():
    # ... 生成内容 ...
    
    # 自动发布
    publisher = AutoPublisher()
    publisher.publish_all(prey_id, content_file)
```

---

## 📊 发布记录追踪

**记录文件**: `tian_shu/distribution_records.json`

**格式**:
```json
{
  "records": [
    {
      "timestamp": "2026-03-28T14:20:00",
      "prey_id": "012",
      "platform": "feishu",
      "status": "success",
      "content_preview": "🔥 GitHub Trending...",
      "error": ""
    }
  ]
}
```

**查询发布历史**:
```bash
cat tian_shu/distribution_records.json | jq '.records[] | select(.prey_id=="012")'
```

---

## 🎯 配置检查清单

| 平台 | 状态 | 所需凭证 | 配置完成 |
|------|------|---------|---------|
| 飞书 | ✅ 可用 | 无 | ✅ |
| Twitter | ⏳ 待配置 | API Key × 4 | ❌ |
| 微博 | ⏳ 待配置 | App Key × 3 | ❌ |
| 知乎 | ⏳ 待配置 | Cookie | ❌ |
| 掘金 | ⏳ 待配置 | Token | ❌ |
| V2EX | ⏳ 待配置 | Cookie | ❌ |

---

## 🚀 下一步行动

### 立即可做
1. ✅ 飞书推送 - 已完成
2. ⏳ 配置掘金 (最简单，只需 Token)
3. ⏳ 配置 Twitter API (需要开发者账号)

### 后续优化
1. 添加发布失败重试机制
2. 添加发布时间调度 (避开低峰期)
3. 添加发布效果统计 (阅读量/点赞数)
4. 添加 A/B 测试 (不同文案对比)

---

## 📝 环境变量模板

创建 `.env` 文件 (不要提交到 Git):

```bash
# Twitter API
TWITTER_API_KEY=
TWITTER_API_SECRET=
TWITTER_ACCESS_TOKEN=
TWITTER_ACCESS_TOKEN_SECRET=

# 微博 API
WEIBO_APP_KEY=
WEIBO_APP_SECRET=
WEIBO_ACCESS_TOKEN=

# 掘金
JUEJIN_TOKEN=

# 知乎 (Cookie)
ZHIHU_COOKIE=

# V2EX (Cookie)
V2EX_COOKIE=
```

---

## 🔒 安全提示

1. **不要提交 `.env` 文件到 Git**
2. **定期更换 API 凭证**
3. **使用环境变量而非硬编码**
4. **浏览器自动化时注意 Cookie 安全**

---

**维护者**: Sovereign (S.V.) 👁️  
**最后更新**: 2026-03-28 14:25 CST

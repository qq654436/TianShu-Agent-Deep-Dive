# CLIProxyAPI 技术分析报告

**分析时间**: 2026-03-28 14:45 CST  
**项目**: https://github.com/router-for-me/CLIProxyAPI  
**核心功能**: 免费使用多个国外 AI 模型的 API 代理服务

---

## 🎯 核心价值

**一句话**: 通过 OAuth 登录 + 本地代理，将多个 AI 服务的免费额度转换为标准 API 接口

**解决的问题**:
1. 官方 API 收费高 (GPT-4: $0.03/1K tokens)
2. 个人订阅有免费额度 (Gemini Pro: 免费)
3. 多账号管理复杂
4. 需要统一的 API 接口

---

## 🏗️ 技术架构

```
┌─────────────────────────────────────────────────────────┐
│                    客户端请求                            │
│         (OpenAI/Gemini/Claude 兼容 SDK)                  │
└─────────────────────────────────────────────────────────┘
                            ↓
┌─────────────────────────────────────────────────────────┐
│              CLIProxyAPI 代理服务器                       │
│  ┌─────────────────────────────────────────────────────┐│
│  │  API 兼容层 (OpenAI/Gemini/Claude 格式转换)           ││
│  └─────────────────────────────────────────────────────┘│
│  ┌─────────────────────────────────────────────────────┐│
│  │  认证管理器 (OAuth Token 刷新 + 多账号轮询)          ││
│  └─────────────────────────────────────────────────────┘│
│  ┌─────────────────────────────────────────────────────┐│
│  │  路由层 (模型映射 + 故障转移)                        ││
│  └─────────────────────────────────────────────────────┘│
└─────────────────────────────────────────────────────────┘
                            ↓
┌─────────────────────────────────────────────────────────┐
│                    上游服务                              │
│  ┌──────────┐ ┌──────────┐ ┌──────────┐ ┌──────────┐   │
│  │Gemini CLI│ │ClaudeCode│ │Codex     │ │Qwen Code │   │
│  │(免费)    │ │(免费)    │ │(免费)    │ │(免费)    │   │
│  └──────────┘ └──────────┘ └──────────┘ └──────────┘   │
└─────────────────────────────────────────────────────────┘
```

---

## 🔑 核心技术

### 1. OAuth 认证 (无需 API Key)

**原理**: 使用官方 CLI 工具的登录凭证

```yaml
# config.yaml
providers:
  - name: gemini
    type: gemini-cli
    auth_method: oauth  # 使用 OAuth 登录
    
  - name: claude
    type: claude-code
    auth_method: oauth
```

**流程**:
```
1. 运行 `cliproxy auth login gemini`
2. 打开浏览器登录 Google 账号
3. 获取 OAuth Token
4. Token 保存到 ~/.cliproxy/auths/
5. 自动刷新 Token (过期前)
```

**优势**:
- ✅ 无需申请 API Key
- ✅ 使用个人免费额度
- ✅ 支持多账号轮询

---

### 2. 多账号负载均衡

**配置**:
```yaml
providers:
  - name: gemini
    accounts:
      - id: account1
        email: user1@gmail.com
        token_path: ~/.cliproxy/auths/gemini_1.json
      - id: account2
        email: user2@gmail.com
        token_path: ~/.cliproxy/auths/gemini_2.json
      - id: account3
        email: user3@gmail.com
        token_path: ~/.cliproxy/auths/gemini_3.json
    
    load_balancing: round_robin  # 轮询
    # 或 least_loaded (最少使用)
```

**效果**: 3 个账号 = 3 倍免费额度

---

### 3. API 兼容层

**支持格式**:
| 客户端 SDK | 兼容模式 | 示例 |
|-----------|---------|------|
| OpenAI | `/v1/chat/completions` | `openai.ChatCompletion.create()` |
| Gemini | `/v1beta/models` | `generativelanguage.generate()` |
| Claude | `/v1/messages` | `claude.messages.create()` |

**模型映射**:
```yaml
model_mapping:
  # 客户端请求 → 实际模型
  "gpt-4": "gemini-2.5-pro"
  "gpt-3.5-turbo": "gemini-2.0-flash"
  "claude-3-opus": "claude-sonnet-4"
  "claude-3-sonnet": "gemini-2.0-flash"
```

---

### 4. 自动故障转移

**配置**:
```yaml
failover:
  enabled: true
  max_retries: 3
  fallback_order:
    - gemini
    - claude
    - codex
```

**流程**:
```
请求 Gemini → 失败 (额度用完)
    ↓
自动切换到 Claude → 成功
    ↓
返回结果给客户端
```

---

## 📊 支持的 AI 服务

| 服务 | 类型 | 免费额度 | 状态 |
|------|------|---------|------|
| **Gemini CLI** | Google | 免费 (Gemini 2.5 Pro) | ✅ 支持 |
| **Claude Code** | Anthropic | 免费 (Claude Sonnet) | ✅ 支持 |
| **OpenAI Codex** | OpenAI | 免费 (GPT-4) | ✅ 支持 |
| **Qwen Code** | 阿里通义 | 免费 (Qwen 2.5) | ✅ 支持 |
| **iFlow** | 字节 | 免费 (Doubao) | ✅ 支持 |
| **Antigravity** | 第三方 | 免费 | ✅ 支持 |

---

## 🔧 部署方式

### 方式 1: 本地运行 (推荐)

```bash
# 安装
go install github.com/router-for-me/CLIProxyAPI@latest

# 配置
cliproxy config init

# 登录
cliproxy auth login gemini
cliproxy auth login claude

# 启动
cliproxy server start

# 使用
curl http://localhost:8080/v1/chat/completions \
  -H "Authorization: Bearer YOUR_API_KEY" \
  -d '{"model":"gpt-4","messages":[{"role":"user","content":"Hello"}]}'
```

### 方式 2: Docker

```bash
docker run -d \
  -p 8080:8080 \
  -v ~/.cliproxy:/root/.cliproxy \
  ghcr.io/router-for-me/cliproxyapi:latest
```

### 方式 3: SDK 嵌入 (Go)

```go
import "github.com/router-for-me/CLIProxyAPI/v6/sdk/cliproxy"

svc, _ := cliproxy.NewBuilder().
    WithConfig(cfg).
    WithConfigPath("config.yaml").
    Build()

ctx, cancel := context.WithCancel(context.Background())
defer cancel()

svc.Run(ctx)
```

---

## 💰 成本分析

### 官方 API 价格

| 模型 | 价格 (输入) | 价格 (输出) | 100 万次成本 |
|------|-----------|-----------|-----------|
| GPT-4 | $0.03/1K | $0.06/1K | $90 |
| GPT-4o | $0.005/1K | $0.015/1K | $20 |
| Claude-3-Opus | $0.015/1K | $0.075/1K | $90 |
| Gemini-2.5-Pro | $0.0025/1K | $0.0075/1K | $10 |

### CLIProxyAPI 成本

| 项目 | 成本 |
|------|------|
| Gemini CLI | ✅ 免费 (个人账号) |
| Claude Code | ✅ 免费 (个人账号) |
| OpenAI Codex | ✅ 免费 (个人账号) |
| 服务器成本 | $0 (本地运行) |
| **总计** | **$0** |

**节省**: 100% (使用免费额度)

---

## ⚠️ 限制与风险

### 技术限制

1. **额度限制**: 个人账号有每日/每月限制
   - Gemini: ~100 次/天 (免费)
   - Claude: ~50 次/天 (免费)
   
2. **速率限制**: 高频请求可能触发风控
   - 建议：每账号 <10 次/分钟

3. **功能限制**: 部分高级功能不可用
   - 如：GPT-4 Vision, Claude 100K 上下文

### 合规风险

1. **服务条款**: 可能违反部分服务的 ToS
   - 建议：仅个人使用，不要商业化

2. **账号风险**: 多账号可能被关联封禁
   - 建议：使用独立 IP/设备

3. **法律风险**: 某些地区可能禁止代理
   - 建议：遵守当地法律

---

## 🎯 对 Aether-Sync 的借鉴

### 可借鉴设计

| 功能 | 适配到 Aether-Sync | 优先级 |
|------|------------------|--------|
| OAuth 认证 | 社交媒体发布免 API Key | P0 |
| 多账号轮询 | 多微博/知乎账号发布 | P1 |
| API 兼容层 | 统一各平台发布接口 | P0 |
| 故障转移 | 发布失败自动切换账号 | P1 |
| 模型映射 | 内容格式自动转换 | P2 |

### 实现方案

**1. 社交媒体 OAuth 发布器**

```python
# tian_shu/scripts/oauth_publisher.py

class SocialMediaOAuth:
    def __init__(self):
        self.accounts = {
            "weibo": [
                {"email": "user1@gmail.com", "cookie_path": "~/.auth/weibo1.json"},
                {"email": "user2@gmail.com", "cookie_path": "~/.auth/weibo2.json"},
            ],
            "zhihu": [...],
        }
        self.current_index = 0
    
    def get_next_account(self, platform):
        # 轮询获取下一个账号
        accounts = self.accounts[platform]
        account = accounts[self.current_index % len(accounts)]
        self.current_index += 1
        return account
    
    def publish(self, platform, content):
        account = self.get_next_account(platform)
        cookie = self.load_cookie(account["cookie_path"])
        
        # 使用 Cookie 发布
        response = self.post_with_cookie(platform, cookie, content)
        
        if response.failed:
            # 故障转移：尝试下一个账号
            return self.publish(platform, content)
        
        return response
```

**2. 统一发布接口**

```python
# 兼容各平台 SDK
class UnifiedPublisher:
    def __init__(self):
        self.oauth = SocialMediaOAuth()
    
    def publish(self, platform, content):
        # 统一接口
        if platform == "weibo":
            return self.oauth.publish("weibo", content)
        elif platform == "zhihu":
            return self.oauth.publish("zhihu", content)
        elif platform == "juejin":
            return self.oauth.publish("juejin", content)
```

---

## 📝 实施计划

### Phase 1:  OAuth 认证 (本周)
- [ ] 实现微博 OAuth 登录
- [ ] 实现知乎 OAuth 登录
- [ ] 实现掘金 Cookie 管理
- [ ] 保存凭证到加密文件

### Phase 2: 多账号管理 (下周)
- [ ] 实现账号轮询
- [ ] 实现故障转移
- [ ] 实现账号健康检查

### Phase 3: 统一接口 (下周)
- [ ] 设计统一发布 API
- [ ] 实现各平台适配器
- [ ] 集成到 free_publisher.py

---

## 🔗 相关链接

- CLIProxyAPI: https://github.com/router-for-me/CLIProxyAPI
- 文档：https://help.router-for.me/
- SDK: https://github.com/router-for-me/CLIProxyAPI/tree/main/sdk

---

**核心洞察**: 通过 OAuth 登录 + 本地代理，将免费额度转换为 API 服务

**Aether-Sync 应用**: 社交媒体免 API Key 发布 + 多账号轮询

👁️ Sovereign (S.V.)  
2026-03-28 14:50 CST

# SKILL.md - 加密货币行情追踪

**技能名称**: `crypto-price-tracker`  
**版本**: 1.0.0  
**作者**: 天枢计划 (TianShu)  
**许可证**: MIT

---

## 📋 技能描述

实时查询加密货币价格、市值、24h 涨跌幅。支持 BTC/ETH 等主流币种及长尾代币，数据源来自 CoinGecko/Binance 公共 API。

**触发条件**: 当用户询问加密货币价格、行情、市值时自动激活。

---

## 🎯 何时使用 (When to Use)

- ✅ 查询 BTC/ETH 等主流币种价格
- ✅ 追踪特定代币 24h 涨跌幅
- ✅ 获取市值排名/交易量数据
- ✅ 设置价格提醒 (需配合 cron 技能)

---

## ⚙️ 配置要求

### 环境变量 (可选)
```bash
# CoinGecko API (免费，无需 Key)
# 或使用付费 API 提高速率限制
export COINGECKO_API_KEY=""  # 可选

# Binance API (仅查询无需 Key)
export BINANCE_API_KEY=""    # 可选
```

### 权限要求
无特殊权限，使用公共 API

---

## 📦 安装方式

### 方式 1: ClawHub
```bash
clawhub install crypto-price-tracker
```

### 方式 2: 手动安装
```bash
git clone https://github.com/qq654436/TianShu-Agent-Deep-Dive.git
cd TianShu-Agent-Deep-Dive/tian_shu/skills/crypto-price-tracker
cp -r . ~/.openclaw/skills/crypto-price-tracker/
```

---

## 🚀 使用示例

### 示例 1: 查询 BTC 价格
```python
# 在对话中
BTC 现在多少钱？
```

**响应**:
```
₿ BTC/USD: $67,234.50
📈 24h: +2.34%
📊 市值：$1.32T
💰 24h 成交量：$28.5B
```

### 示例 2: 查询多个币种
```python
帮我看看 BTC、ETH、SOL 的价格
```

**响应**:
```
┌──────┬────────────┬─────────┬──────────┐
│ 币种 │ 价格 (USD) │ 24h 变化 │ 市值     │
├──────┼────────────┼─────────┼──────────┤
│ BTC  │ $67,234.50 │ +2.34%  │ $1.32T   │
│ ETH  │ $3,456.78  │ +1.89%  │ $415.2B  │
│ SOL  │ $145.67    │ +5.67%  │ $65.8B   │
└──────┴────────────┴─────────┴──────────┘
```

### 示例 3: 查询特定代币
```python
查一下 PEPE 的行情
```

**响应**:
```
🐸 PEPE/USD: $0.000007234
📈 24h: +12.45%
📊 市值：$3.04B
💰 24h 成交量：$892M
⚠️ 高波动性代币，请注意风险
```

### 示例 4: 设置价格提醒
```python
BTC 跌破 65000 时提醒我
```

**响应**:
```
✅ 价格提醒已设置
- 币种：BTC
- 条件：< $65,000
- 通知方式：飞书
```

---

## 🔧 技能实现

### 核心函数
```python
def get_crypto_price(symbol: str, currency: str = "usd") -> dict:
    """
    获取加密货币价格
    
    Args:
        symbol: 币种符号 (BTC, ETH, etc.)
        currency: 法币单位 (usd, cny, etc.)
    
    Returns:
        dict: {price, change_24h, market_cap, volume_24h}
    """
    # 使用 CoinGecko 公共 API
    url = f"https://api.coingecko.com/api/v3/simple/price"
    params = {
        "ids": symbol_to_coingecko_id(symbol),
        "vs_currencies": currency,
        "include_24hr_change": "true",
        "include_market_cap": "true",
        "include_24hr_vol": "true"
    }
    
    response = requests.get(url, params=params)
    data = response.json()
    
    return format_price_data(data, symbol, currency)
```

### 支持币种映射
```python
SYMBOL_MAP = {
    "BTC": "bitcoin",
    "ETH": "ethereum",
    "SOL": "solana",
    "BNB": "binancecoin",
    "XRP": "ripple",
    "DOGE": "dogecoin",
    "PEPE": "pepe",
    # ... 更多币种
}
```

### 工具依赖
| 工具 | 用途 |
|------|------|
| `web_fetch` | API 数据获取 |
| `message` | 价格提醒推送 |

---

## 📝 输出格式

### 标准响应
```
₿ {SYMBOL}/USD: ${price}
📈 24h: {change}%
📊 市值：${market_cap}
💰 24h 成交量：${volume}
```

### 表格响应 (多币种)
```
┌──────┬────────────┬─────────┬──────────┐
│ 币种 │ 价格 (USD) │ 24h 变化 │ 市值     │
├──────┼────────────┼─────────┼──────────┤
│ ...  │ ...        │ ...     │ ...      │
└──────┴────────────┴─────────┴──────────┘
```

---

## ⚠️ 注意事项

1. **数据延迟**: 免费 API 有 1-5 分钟延迟
2. **速率限制**: CoinGecko 免费 API 10-30 次/分钟
3. **风险提示**: 加密货币高波动，仅供参考
4. **长尾代币**: 部分小币种数据可能不准确

---

## 🆚 版本历史

| 版本 | 日期 | 变更 |
|------|------|------|
| 1.0.0 | 2026-03-19 | 初始版本，基础价格查询 |
| 1.1.0 | 2026-03-26 | 价格提醒功能 (计划) |

---

## 📞 支持

- **GitHub**: [TianShu-Agent-Deep-Dive](https://github.com/qq654436/TianShu-Agent-Deep-Dive)
- **问题反馈**: 创建 Issue
- **企业支持**: 查看 [premium/](../premium/) 企业级配置包

---

## 🔗 相关技能

- `feishu-auto-doc` - 飞书文档自动发布
- `qqbot-cron` - 周期性任务提醒
- `weather` - 天气查询

---

**🗡️ 利刃行动技能包** | 天枢计划 © 2026

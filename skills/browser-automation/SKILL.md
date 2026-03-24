# browser-automation - 浏览器自动化技能

**版本**: 1.0.0  
**作者**: Sovereign (from Prey #008 Analysis)  
**兼容性**: OpenClaw v1.2+  
**依赖**: browser-use (可选), OpenClaw browser 工具

---

## 🎯 技能描述

本技能使 OpenClaw Agent 能够自动化执行浏览器任务，包括导航、点击、输入、截图等操作。基于 browser-use 项目的设计理念，适配 OpenClaw 的 browser 工具。

---

## 📋 适用场景

- 抓取网页内容 (替代 web_fetch 的复杂场景)
- 自动化表单填写和提交
- 截图保存网页状态
- 与需要登录的网站交互
- 多步骤网页任务自动化

---

## 🔧 工具调用规范

### 基础操作

#### 1. 打开网页
```
browser action=open url="https://example.com" profile="openclaw"
```

#### 2. 获取页面快照 (推荐用 aria refs)
```
browser action=snapshot refs="aria" targetId="<from_open_response>"
```

#### 3. 点击元素
```
browser action=act kind=click ref="e123" targetId="<targetId>"
```

#### 4. 输入文本
```
browser action=act kind=type ref="e456" text="Hello World" targetId="<targetId>"
```

#### 5. 截图
```
browser action=screenshot type="png" fullPage=true targetId="<targetId>"
```

#### 6. 关闭页面
```
browser action=close targetId="<targetId>"
```

---

## 📖 标准工作流

### 工作流 A: 简单内容抓取

```
Step 1: 打开目标网页
        → browser action=open url="<URL>"

Step 2: 获取页面快照 (aria refs)
        → browser action=snapshot refs="aria"

Step 3: 识别目标内容 ref
        → 分析 snapshot 输出

Step 4: 点击/提取目标内容
        → browser action=act kind=click ref="<ref>"
        或 → browser action=act kind=evaluate fn="..."

Step 5: 关闭页面
        → browser action=close
```

### 工作流 B: 表单自动化

```
Step 1: 打开表单页面
        → browser action=open url="<form_url>"

Step 2: 获取快照识别表单字段
        → browser action=snapshot refs="aria"

Step 3: 填写字段 (逐个)
        → browser action=act kind=type ref="<field_ref>" text="<value>"

Step 4: 提交表单
        → browser action=act kind=click ref="<submit_button_ref>"
        或 → browser action=act kind=press key="Enter"

Step 5: 等待结果 (可选)
        → browser action=act kind=wait timeMs=3000

Step 6: 获取结果快照
        → browser action=snapshot refs="aria"
```

### 工作流 C: 需要登录的网站

```
Step 1: 使用 Chrome 扩展 Relay (如已配对)
        → browser action=open url="<URL>" profile="chrome"

Step 2: 检查是否已登录
        → browser action=snapshot refs="aria"
        → 分析是否有登录状态元素

Step 3: 如未登录，执行登录流程
        → 输入用户名 → 输入密码 → 点击登录

Step 4: 执行目标任务
        → 按工作流 A 或 B 执行

Step 5: 保持会话 (不关闭，用于后续任务)
```

---

## 🎨 最佳实践

### 1. 优先使用 ARIA Refs
```
✅ 推荐：browser action=snapshot refs="aria"
❌ 避免：browser action=snapshot refs="role" (除非必要)
```
**理由**: ARIA refs 更稳定，跨会话可解析。

### 2. 保持 TargetId 一致性
```
✅ 推荐：首次 open 后保存 targetId，后续操作复用
❌ 避免：每次操作都重新 open 页面
```

### 3. 错误处理
```
当 browser 操作失败时:
1. 重试 1 次 (网络波动)
2. 重新获取 snapshot (页面可能已变化)
3. 降级到 web_fetch (如只需内容)
```

### 4. 截图时保存证据
```
关键操作后截图:
- 表单提交前
- 支付确认页
- 错误状态页

browser action=screenshot type="png" fullPage=true
```

### 5. 避免快速轮询
```
✅ 推荐：browser action=act kind=wait timeMs=3000
❌ 避免：连续快速 snapshot (可能触发反爬)
```

---

## ⚠️ 注意事项

### 安全限制
- 不自动填写敏感信息 (密码/信用卡)
- 需要用户确认的支付操作必须暂停等待
- 不绕过 CAPTCHA (使用 Browser Use Cloud 如需)

### 性能优化
- 长任务使用 `yieldMs` 参数后台执行
- 大页面截图使用 `maxWidth` 限制
- 多页面任务及时 `close` 释放资源

### 反爬策略
- 添加随机延迟 (1-3 秒)
- 限制单站点请求频率 (<10/分钟)
- 使用 `profile="chrome"` 复用真实浏览器指纹

---

## 🔗 参考资源

### 外部资源
- [browser-use 官方文档](https://docs.browser-use.com)
- [browser-use GitHub](https://github.com/browser-use/browser-use)
- [Browser Use Cloud](https://cloud.browser-use.com)

### 内部资源
- OpenClaw `browser` 工具文档
- `memory/2026-03-24_prey.md` (猎物 #008 分析)

---

## 🧪 示例任务

### 示例 1: 抓取 GitHub 项目星数
```
任务：获取 browser-use 仓库的星数

1. browser action=open url="https://github.com/browser-use/browser-use"
2. browser action=snapshot refs="aria"
3. 分析 snapshot 找到星数元素 ref (如 "e213")
4. browser action=act kind=evaluate fn="document.querySelector('[ref=e213]').textContent"
5. browser action=close
输出："83,834"
```

### 示例 2: 自动搜索并截图
```
任务：在 Google 搜索 "AI Agent" 并截图结果页

1. browser action=open url="https://google.com"
2. browser action=snapshot refs="aria"
3. browser action=act kind=type ref="<search_box>" text="AI Agent"
4. browser action=act kind=press key="Enter"
5. browser action=act kind=wait timeMs=3000
6. browser action=screenshot type="png" fullPage=true
7. browser action=close
```

---

## 📈 版本历史

| 版本 | 日期 | 变更 |
|------|------|------|
| 1.0.0 | 2026-03-24 | 初始版本 (基于 Prey #008 分析) |

---

## 🤝 与 OpenClaw 其他技能协作

- **web_search**: 先用 web_search 找到目标 URL，再用本技能深入抓取
- **web_fetch**: 简单内容用 web_fetch，复杂交互用本技能
- **exec**: 可用 exec 运行 browser-use CLI 作为备选方案

---

**技能状态**: ✅ 已激活  
**最后测试**: 2026-03-24  
**维护者**: Sovereign Agent

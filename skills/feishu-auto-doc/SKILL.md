# SKILL.md - 飞书文档自动发布

**技能名称**: `feishu-auto-doc`  
**版本**: 1.0.0  
**作者**: 天枢计划 (TianShu)  
**许可证**: MIT

---

## 📋 技能描述

自动将内容发布到飞书文档，支持富文本格式、图片上传、表格创建。适用于日报、周报、技术文档自动推送场景。

**触发条件**: 当用户需要将内容发布到飞书文档时自动激活。

---

## 🎯 何时使用 (When to Use)

- ✅ 需要自动发送飞书文档/云文档
- ✅ 需要将 Markdown 内容转换为飞书格式
- ✅ 需要批量创建文档并设置权限
- ✅ 需要定时推送报告到指定飞书群组

---

## ⚙️ 配置要求

### 环境变量
```bash
export FEISHU_APP_ID="cli_xxxxxxxxxxxxx"
export FEISHU_APP_SECRET="xxxxxxxxxxxxxxxxxxxxx"
export FEISHU_APP_TICKET="xxxxxxxxxxxxxxxxxxxxx"  # 可选
```

### 权限要求 (App Scopes)
```json
[
  "drive:files",
  "drive:write",
  "docx:docs",
  "docx:write"
]
```

---

## 📦 安装方式

### 方式 1: ClawHub (推荐)
```bash
clawhub install feishu-auto-doc
```

### 方式 2: 手动安装
```bash
# 克隆技能
git clone https://github.com/qq654436/TianShu-Agent-Deep-Dive.git
cd TianShu-Agent-Deep-Dive/tian_shu/skills/feishu-auto-doc

# 复制到 OpenClaw 技能目录
cp -r . ~/.openclaw/skills/feishu-auto-doc/
```

### 方式 3: 符号链接
```bash
ln -s /path/to/TianShu-Agent-Deep-Dive/tian_shu/skills/feishu-auto-doc \
      ~/.openclaw/skills/feishu-auto-doc
```

---

## 🚀 使用示例

### 示例 1: 发送简单文档
```python
# 在对话中
请帮我把以下内容发送到飞书文档：

# 技术周报 - 2026-W12

## 本周完成
- 完成用户认证模块
- 修复 3 个关键 Bug

## 下周计划
- 启动支付模块开发
```

### 示例 2: 发送到指定群组
```python
请把这个报告发到"技术部周报"飞书群：
[报告内容]
```

### 示例 3: 带图片的文档
```python
创建飞书文档，包含以下内容：
# 项目进度

![进度图](attachment://chart.png)

## 关键指标
- 完成率：85%
- Bug 数：3
```

---

## 🔧 技能实现

### 核心函数
```python
def feishu_auto_doc(content: str, target: str = None) -> dict:
    """
    自动发布内容到飞书文档
    
    Args:
        content: 文档内容 (Markdown 格式)
        target: 目标 (群组 ID/用户 ID/文档 Token)
    
    Returns:
        dict: {success: bool, doc_token: str, url: str}
    """
    # 1. 获取飞书凭证
    app_id = os.environ.get("FEISHU_APP_ID")
    app_secret = os.environ.get("FEISHU_APP_SECRET")
    
    # 2. 获取访问令牌
    token = get_feishu_token(app_id, app_secret)
    
    # 3. 创建云文档
    doc_token = create_cloud_doc(token, content)
    
    # 4. 发送到目标 (如有)
    if target:
        send_to_chat(token, target, doc_token)
    
    return {
        "success": True,
        "doc_token": doc_token,
        "url": f"https://feishu.cn/docs/{doc_token}"
    }
```

### 工具依赖
| 工具 | 用途 |
|------|------|
| `feishu_doc` | 飞书文档操作 |
| `feishu_chat` | 飞书群聊发送 |
| `feishu_drive` | 飞书云盘操作 |

---

## 📝 输出格式

### 成功响应
```json
{
  "success": true,
  "doc_token": "docxxxxxxxxxxxxx",
  "url": "https://feishu.cn/docs/docxxxxxxxxxxxxx",
  "message": "文档已创建并发送"
}
```

### 失败响应
```json
{
  "success": false,
  "error": "FEISHU_CREDENTIAL_MISSING",
  "message": "请配置 FEISHU_APP_ID 和 FEISHU_APP_SECRET"
}
```

---

## ⚠️ 注意事项

1. **权限配置**: 确保飞书应用已开通文档读写权限
2. **内容长度**: 单文档建议不超过 50KB，超长内容分多篇
3. **频率限制**: 飞书 API 有调用频率限制，批量操作需控制节奏
4. **图片处理**: 图片需先上传到飞书云盘获取 file_key

---

## 🆚 版本历史

| 版本 | 日期 | 变更 |
|------|------|------|
| 1.0.0 | 2026-03-19 | 初始版本，基础文档发布功能 |

---

## 📞 支持

- **GitHub**: [TianShu-Agent-Deep-Dive](https://github.com/qq654436/TianShu-Agent-Deep-Dive)
- **问题反馈**: 创建 Issue
- **企业支持**: 查看 [premium/](../premium/) 企业级配置包

---

## 🔗 相关技能

- `feishu-message` - 飞书消息发送
- `feishu-calendar` - 飞书日历管理
- `pdf-knowledge-organizer` - PDF 知识库整理

---

**🗡️ 利刃行动技能包** | 天枢计划 © 2026

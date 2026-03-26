# Middleware Chain Skill for OpenClaw

**版本**: 1.0  
**来源**: 天枢计划猎物 #010 - DeerFlow 中间件链适配  
**创建日期**: 2026-03-26  
**兼容性**: OpenClaw v1.2+

---

## 技能概述

本技能将 DeerFlow 的 9 层中间件链架构适配到 OpenClaw，实现工具调用的横切关注点分离。

---

## 工作流

### 中间件执行顺序

```
before_tool → 风险评估 → 日志记录 → 工具执行 
→ after_tool → 验证输出 → 错误捕获 
→ before_commit → 备份 → after_session → 归档
```

### 各层职责

| # | 中间件 | 职责 | 实现状态 |
|---|--------|------|----------|
| 1 | **风险评估** | 检查工具权限、文件路径白名单、破坏性操作 | ✅ P0 |
| 2 | **日志记录** | 记录工具调用参数、时间戳、会话 ID | ✅ P0 |
| 3 | **工具执行** | 实际调用工具 | - (核心) |
| 4 | **验证输出** | 检查输出符合预期、无错误/警告 | ✅ P0 |
| 5 | **错误捕获** | 捕获异常、记录错误、决定重试/替代 | ✅ P0 |
| 6 | **before_commit** | 文件写入前备份原文件 (如存在) | ✅ P0 |
| 7 | **after_session** | 会话结束前归档到 memory/ | ✅ P0 |

---

## 最佳实践

### 1. 风险评估规则

```javascript
// 伪代码 - OpenClaw 中间件实现
function riskAssessment(tool, params) {
  const高风险工具 = ['exec', 'browser', 'nodes'];
  const破坏性操作 = ['rm', 'sudo', 'delete', 'truncate'];
  
  if (高风险工具.includes(tool)) {
    return { level: 'high', requiresApproval: true };
  }
  
  if (params.command && 破坏性操作.some(op => params.command.includes(op))) {
    return { level: 'critical', requiresApproval: true, reason: '破坏性操作' };
  }
  
  if (params.path && !params.path.startsWith('/home/admin/.openclaw/workspace')) {
    return { level: 'high', requiresApproval: true, reason: '路径超出白名单' };
  }
  
  return { level: 'low', requiresApproval: false };
}
```

### 2. 日志记录格式

```json
{
  "timestamp": "2026-03-26T16:30:00.000Z",
  "sessionId": "agent:sovereign:feishu:direct:ou_xxx",
  "tool": "write",
  "params": {
    "path": "/home/admin/.openclaw/workspace/test.md",
    "contentLength": 1234
  },
  "riskLevel": "low",
  "duration": 45,
  "status": "success"
}
```

### 3. 验证输出规则

```javascript
function validateOutput(tool, output) {
  if (tool === 'read' && !output.text && !output.error) {
    return { valid: false, reason: '读取成功但无内容' };
  }
  
  if (tool === 'exec' && output.exitCode !== 0) {
    return { valid: false, reason: `命令执行失败：${output.exitCode}` };
  }
  
  if (output.error || output.warnings?.length > 0) {
    return { valid: false, reason: '存在错误或警告' };
  }
  
  return { valid: true };
}
```

### 4. 错误处理策略

```javascript
function handleError(error, tool, params, retryCount = 0) {
  const maxRetries = 3;
  
  // 记录错误
  logError({ tool, params, error, retryCount });
  
  // 可重试的错误
  const可重试错误 = ['network', 'timeout', 'rate_limit'];
  if (可重试错误.includes(error.type) && retryCount < maxRetries) {
    return { action: 'retry', delay: Math.pow(2, retryCount) * 1000 };
  }
  
  // 替代方案
  const替代方案 = {
    'web_fetch': 'browser.snapshot',
    'exec': 'read (如果是文件读取)',
    'write': 'edit (如果是小修改)'
  };
  
  if (替代方案 [tool]) {
    return { action: 'fallback', alternative: 替代方案 [tool] };
  }
  
  // 上报董事会
  return { action: 'escalate', notify: 'feishu' };
}
```

### 5. 文件备份策略

```javascript
async function beforeCommit(path, content) {
  const fs = require('fs').promises;
  const path = require('path');
  
  // 检查文件是否存在
  try {
    await fs.access(path);
  } catch {
    return; // 新文件，无需备份
  }
  
  // 创建备份
  const timestamp = new Date().toISOString().replace(/[:.]/g, '-');
  const backupPath = `${path}.backup.${timestamp}`;
  
  await fs.copyFile(path, backupPath);
  
  // 记录备份
  logBackup({ original: path, backup: backupPath });
  
  return backupPath;
}
```

### 6. 会话归档

```javascript
async function afterSession(sessionId, decisions) {
  const date = new Date().toISOString().split('T')[0];
  const logPath = `/home/admin/.openclaw/workspace/agents/sovereign/memory/${date}.md`;
  
  const logContent = `
## ${sessionId} 会话归档

### 关键决策
${decisions.map(d => `- ${d.point}: ${d.choice} - ${d.reason}`).join('\n')}

### 工具调用统计
- 总调用次数：${decisions.length}
- 成功：${decisions.filter(d => d.status === 'success').length}
- 失败：${decisions.filter(d => d.status === 'failed').length}

### 归档文件
${decisions.filter(d => d.files).map(d => d.files.map(f => `- ${f}`)).flat().join('\n')}
`;
  
  await appendToFile(logPath, logContent);
}
```

---

## 配置示例

### OpenClaw 配置文件 (config.yaml)

```yaml
middleware:
  enabled: true
  
  # 风险评估配置
  risk_assessment:
    high_risk_tools:
      - exec
      - browser
      - nodes
    destructive_operations:
      - rm
      - sudo
      - delete
      - truncate
    path_whitelist:
      - /home/admin/.openclaw/workspace
    
  # 日志配置
  logging:
    enabled: true
    path: /home/admin/.openclaw/workspace/logs/
    format: json
    level: info  # debug, info, warn, error
    
  # 验证配置
  validation:
    enabled: true
    strict_mode: false  # true = 任何警告都失败
    
  # 错误处理配置
  error_handling:
    max_retries: 3
    retry_delay_base: 1000  # ms
    fallback_enabled: true
    escalation_enabled: true
    escalation_channel: feishu
    
  # 备份配置
  backup:
    enabled: true
    path: /home/admin/.openclaw/workspace/backups/
    retention_days: 30
    max_backups_per_file: 5
    
  # 归档配置
  archiving:
    enabled: true
    path: /home/admin/.openclaw/workspace/memory/
    include_tool_stats: true
    include_file_changes: true
```

---

## 参考资源

### DeerFlow 原始实现
- 项目地址：https://github.com/bytedance/deer-flow
- 中间件文档：https://github.com/bytedance/deer-flow/blob/main/backend/README.md
- 架构详解：https://github.com/bytedance/deer-flow/blob/main/backend/docs/ARCHITECTURE.md

### OpenClaw 相关文件
- AGENTS.md: `/home/admin/.openclaw/workspace/agents/sovereign/AGENTS.md`
- 验证脚本：`/home/admin/.openclaw/workspace/agents/sovereign/scripts/verify-session.js`
- 记忆目录：`/home/admin/.openclaw/workspace/agents/sovereign/memory/`

---

## 实施检查清单

### P0 实施 (1-2 周)

- [ ] 实现风险评估中间件
  - [ ] 高风险工具列表配置
  - [ ] 破坏性操作检测
  - [ ] 路径白名单验证
  
- [ ] 实现日志记录中间件
  - [ ] JSON 格式日志
  - [ ] 会话 ID 追踪
  - [ ] 工具调用统计
  
- [ ] 实现验证输出中间件
  - [ ] 输出格式验证
  - [ ] 错误/警告检测
  - [ ] 严格模式开关
  
- [ ] 实现错误捕获中间件
  - [ ] 错误分类
  - [ ] 重试逻辑
  - [ ] 替代方案
  - [ ] 上报机制
  
- [ ] 实现 before_commit 中间件
  - [ ] 文件存在检查
  - [ ] 备份创建
  - [ ] 备份清理 (保留策略)
  
- [ ] 实现 after_session 中间件
  - [ ] 会话日志归档
  - [ ] 工具统计
  - [ ] 文件变更记录

### 测试用例

- [ ] 测试高风险工具拦截
- [ ] 测试路径白名单验证
- [ ] 测试错误重试逻辑
- [ ] 测试备份创建和清理
- [ ] 测试会话归档格式

---

## 版本历史

| 版本 | 日期 | 变更 |
|------|------|------|
| 1.0 | 2026-03-26 | 初始版本，基于 DeerFlow 9 层中间件链适配 |

---

**技能作者**: Sovereign (S.V.) 👁️  
**天枢计划**: 猎物 #010 - DeerFlow 中间件链适配  
**最后更新**: 2026-03-26 16:45 CST

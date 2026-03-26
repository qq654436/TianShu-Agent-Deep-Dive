# Virtual Path Sandbox Skill for OpenClaw

**版本**: 1.0  
**来源**: 天枢计划猎物 #010 - DeerFlow 沙箱虚拟路径适配  
**创建日期**: 2026-03-26  
**兼容性**: OpenClaw v1.2+

---

## 技能概述

本技能实现 DeerFlow 风格的虚拟路径沙箱系统，提供会话隔离、安全边界和路径透明映射。

---

## 核心概念

### 虚拟路径 vs 物理路径

```
┌─────────────────────────────────────────────────────────┐
│                   虚拟路径 (Agent 视角)                   │
│                                                           │
│   /workspace/          → 工作目录                         │
│   /uploads/            → 上传文件                         │
│   /outputs/            → 输出文件                         │
│   /skills/             → 技能库                          │
│   /memory/             → 记忆存储                         │
└─────────────────────────────────────────────────────────┘
                          ↓ 路径转换层
┌─────────────────────────────────────────────────────────┐
│                  物理路径 (宿主机视角)                    │
│                                                           │
│   /home/admin/.openclaw/workspace/agents/sovereign/     │
│   /home/admin/.openclaw/uploads/                         │
│   /home/admin/.openclaw/outputs/                         │
│   /home/admin/.openclaw/workspace/agents/sovereign/skills/ │
│   /home/admin/.openclaw/workspace/agents/sovereign/memory/ │
└─────────────────────────────────────────────────────────┘
```

### 会话隔离

每个会话 (session) 有独立的虚拟工作空间：

```
会话 ID: agent:sovereign:feishu:direct:ou_xxx

虚拟路径: /workspace/
物理路径: /home/admin/.openclaw/workspace/agents/sovereign/sessions/ou_xxx/

虚拟路径: /uploads/
物理路径: /home/admin/.openclaw/uploads/sessions/ou_xxx/
```

---

## 工作流

### 1. 路径解析流程

```
用户/Agent 输入虚拟路径
        ↓
VirtualPathMiddleware
        ↓
检查路径合法性 (白名单验证)
        ↓
查找会话映射 (session_id → physical_base)
        ↓
转换为物理路径
        ↓
执行实际文件操作
        ↓
返回结果 (虚拟路径格式)
```

### 2. 路径映射规则

```javascript
// 路径映射配置
const pathMappings = {
  '/workspace/': '/home/admin/.openclaw/workspace/agents/sovereign/',
  '/uploads/': '/home/admin/.openclaw/uploads/',
  '/outputs/': '/home/admin/.openclaw/outputs/',
  '/skills/': '/home/admin/.openclaw/workspace/agents/sovereign/skills/',
  '/memory/': '/home/admin/.openclaw/workspace/agents/sovereign/memory/',
};

// 会话隔离前缀 (可选)
const sessionPrefix = 'sessions/{session_id}/';

// 转换函数
function virtualToPhysical(virtualPath, sessionId = null) {
  // 1. 验证虚拟路径前缀
  const validPrefix = Object.keys(pathMappings).some(prefix => 
    virtualPath.startsWith(prefix)
  );
  
  if (!validPrefix) {
    throw new Error(`无效虚拟路径：${virtualPath}`);
  }
  
  // 2. 查找匹配的前缀
  const matchedPrefix = Object.keys(pathMappings).find(prefix => 
    virtualPath.startsWith(prefix)
  );
  
  // 3. 构建物理路径
  let physicalPath = pathMappings[matchedPrefix];
  
  // 4. 添加会话隔离 (如果启用)
  if (sessionId) {
    const relativePath = virtualPath.slice(matchedPrefix.length);
    physicalPath = `${physicalPath}${sessionPrefix.replace('{session_id}', sessionId)}/${relativePath}`;
  } else {
    // 追加相对路径
    const relativePath = virtualPath.slice(matchedPrefix.length);
    physicalPath = `${physicalPath}${relativePath}`;
  }
  
  // 5. 规范化路径 (处理 ../ 等)
  physicalPath = path.normalize(physicalPath);
  
  // 6. 验证仍在白名单内 (防止路径遍历)
  const isSafe = Object.values(pathMappings).some(base => 
    physicalPath.startsWith(base)
  );
  
  if (!isSafe) {
    throw new Error(`路径遍历攻击检测：${physicalPath}`);
  }
  
  return physicalPath;
}

// 反向转换 (物理→虚拟，用于日志和错误消息)
function physicalToVirtual(physicalPath) {
  for (const [virtual, physical] of Object.entries(pathMappings)) {
    if (physicalPath.startsWith(physical)) {
      const relative = physicalPath.slice(physical.length);
      return `${virtual}${relative}`;
    }
  }
  return physicalPath; // 无法转换，返回原路径
}
```

---

## 最佳实践

### 1. 路径白名单配置

```yaml
# config.yaml
sandbox:
  virtual_paths:
    /workspace/: /home/admin/.openclaw/workspace/agents/sovereign/
    /uploads/: /home/admin/.openclaw/uploads/
    /outputs/: /home/admin/.openclaw/outputs/
    /skills/: /home/admin/.openclaw/workspace/agents/sovereign/skills/
    /memory/: /home/admin/.openclaw/workspace/agents/sovereign/memory/
  
  # 会话隔离
  session_isolation:
    enabled: true
    prefix: 'sessions/{session_id}/'
  
  # 安全设置
  security:
    prevent_traversal: true  # 防止 ../ 路径遍历
    validate_on_read: true   # 读取前验证
    validate_on_write: true  # 写入前验证
    log_all_access: true     # 记录所有访问
```

### 2. 工具调用适配

```javascript
// read 工具适配
async function read_with_virtual_path(params) {
  const { path: virtualPath, sessionId } = params;
  
  // 转换为物理路径
  const physicalPath = virtualToPhysical(virtualPath, sessionId);
  
  // 执行实际读取
  const result = await originalRead({ path: physicalPath });
  
  // 结果中的路径转换回虚拟路径 (如果有)
  if (result.metadata?.path) {
    result.metadata.path = physicalToVirtual(result.metadata.path);
  }
  
  return result;
}

// write 工具适配
async function write_with_virtual_path(params) {
  const { path: virtualPath, content, sessionId } = params;
  
  // 转换为物理路径
  const physicalPath = virtualToPhysical(virtualPath, sessionId);
  
  // 确保父目录存在
  await fs.mkdir(path.dirname(physicalPath), { recursive: true });
  
  // 执行实际写入
  return await originalWrite({ path: physicalPath, content });
}

// exec 工具适配 (命令中的路径)
async function exec_with_virtual_path(params) {
  const { command, sessionId } = params;
  
  // 替换命令中的虚拟路径
  const physicalCommand = command.replace(
    /(\/workspace\/|\/uploads\/|\/outputs\/|\/skills\/|\/memory\/)[^\s]*/g,
    (match) => virtualToPhysical(match, sessionId)
  );
  
  return await originalExec({ command: physicalCommand });
}
```

### 3. 错误消息适配

```javascript
// 错误消息中的路径应该使用虚拟路径 (对用户友好)
function adaptErrorMessage(error, sessionId) {
  if (error.message) {
    error.message = error.message.replace(
      /\/home\/admin\/\.openclaw\/[^\s]*/g,
      (match) => physicalToVirtual(match)
    );
  }
  
  if (error.path) {
    error.path = physicalToVirtual(error.path);
  }
  
  return error;
}

// 示例
// 原始错误：Error: ENOENT: no such file or directory, open '/home/admin/.openclaw/workspace/test.md'
// 适配后：  Error: ENOENT: no such file or directory, open '/workspace/test.md'
```

### 4. 日志记录

```javascript
// 日志中同时记录虚拟路径和物理路径 (便于调试)
function logPathAccess({ tool, virtualPath, physicalPath, sessionId, status }) {
  const logEntry = {
    timestamp: new Date().toISOString(),
    sessionId,
    tool,
    paths: {
      virtual: virtualPath,
      physical: physicalPath
    },
    status, // 'success' | 'failed' | 'blocked'
  };
  
  // 写入日志文件
  appendToFile('/home/admin/.openclaw/workspace/logs/path-access.log', 
    JSON.stringify(logEntry) + '\n');
}
```

### 5. 会话初始化

```javascript
// 会话开始时创建隔离目录
async function initSession(sessionId) {
  const sessionBase = '/home/admin/.openclaw/workspace/agents/sovereign/sessions/';
  const sessionPath = `${sessionBase}${sessionId}`;
  
  // 创建会话目录
  await fs.mkdir(`${sessionPath}/workspace`, { recursive: true });
  await fs.mkdir(`${sessionPath}/uploads`, { recursive: true });
  await fs.mkdir(`${sessionPath}/outputs`, { recursive: true });
  
  // 记录会话初始化
  logSessionInit({ sessionId, path: sessionPath });
  
  return sessionPath;
}

// 会话结束时清理 (可选)
async function cleanupSession(sessionId, retentionDays = 7) {
  const sessionPath = `/home/admin/.openclaw/workspace/agents/sovereign/sessions/${sessionId}`;
  
  // 检查会话年龄
  const stats = await fs.stat(sessionPath);
  const age = Date.now() - stats.mtimeMs;
  const ageDays = age / (1000 * 60 * 60 * 24);
  
  if (ageDays > retentionDays) {
    // 归档或删除
    await fs.rm(sessionPath, { recursive: true, force: true });
    logSessionCleanup({ sessionId, reason: 'retention_expired' });
  }
}
```

---

## 安全考虑

### 1. 路径遍历防护

```javascript
function validatePath(physicalPath, allowedBases) {
  // 规范化路径 (解析 ../ 和符号链接)
  const resolvedPath = path.resolve(physicalPath);
  
  // 检查是否在允许的基目录内
  const isAllowed = allowedBases.some(base => 
    resolvedPath.startsWith(path.resolve(base))
  );
  
  if (!isAllowed) {
    throw new SecurityError(
      `路径遍历攻击检测：${physicalPath} (解析为：${resolvedPath})`
    );
  }
  
  return true;
}
```

### 2. 符号链接防护

```javascript
async function validateNoSymlinks(physicalPath) {
  const stats = await fs.lstat(physicalPath);
  
  if (stats.isSymbolicLink()) {
    throw new SecurityError(
      `符号链接不被允许：${physicalPath}`
    );
  }
  
  // 递归检查父目录
  const parentDir = path.dirname(physicalPath);
  if (parentDir !== physicalPath) {
    await validateNoSymlinks(parentDir);
  }
}
```

### 3. 权限检查

```javascript
async function checkPermissions(physicalPath, requiredPermissions) {
  const stats = await fs.stat(physicalPath);
  
  // 检查文件所有者
  if (stats.uid !== process.getuid()) {
    throw new PermissionError(
      `文件不属于当前用户：${physicalPath}`
    );
  }
  
  // 检查权限位
  const mode = stats.mode & 0o777;
  if (requiredPermissions === 'read' && !(mode & 0o400)) {
    throw new PermissionError(`无读取权限：${physicalPath}`);
  }
  if (requiredPermissions === 'write' && !(mode & 0o200)) {
    throw new PermissionError(`无写入权限：${physicalPath}`);
  }
}
```

---

## 配置示例

### OpenClaw 配置文件

```yaml
sandbox:
  # 虚拟路径映射
  virtual_paths:
    /workspace/: /home/admin/.openclaw/workspace/agents/sovereign/
    /uploads/: /home/admin/.openclaw/uploads/
    /outputs/: /home/admin/.openclaw/outputs/
    /skills/: /home/admin/.openclaw/workspace/agents/sovereign/skills/
    /memory/: /home/admin/.openclaw/workspace/agents/sovereign/memory/
  
  # 会话隔离
  session_isolation:
    enabled: true
    prefix: 'sessions/{session_id}/'
    cleanup_on_end: false  # 会话结束不清理 (保留历史)
    retention_days: 30     # 30 天后清理
  
  # 安全设置
  security:
    prevent_traversal: true
    prevent_symlinks: true
    check_permissions: true
    log_all_access: true
  
  # 日志配置
  logging:
    enabled: true
    path: /home/admin/.openclaw/workspace/logs/path-access.log
    format: json
    include_physical: true  # 日志中包含物理路径 (调试用)
```

---

## 参考资源

### DeerFlow 原始实现
- 项目地址：https://github.com/bytedance/deer-flow
- 沙箱文档：https://github.com/bytedance/deer-flow/blob/main/backend/docs/CONFIGURATION.md#sandbox
- 路径示例：https://github.com/bytedance/deer-flow/blob/main/backend/docs/PATH_EXAMPLES.md

### OpenClaw 相关文件
- 工作空间：`/home/admin/.openclaw/workspace/agents/sovereign/`
- 日志目录：`/home/admin/.openclaw/workspace/logs/`
- AGENTS.md: `/home/admin/.openclaw/workspace/agents/sovereign/AGENTS.md`

---

## 实施检查清单

### P0 实施 (1-2 周)

- [ ] 实现路径映射核心函数
  - [ ] virtualToPhysical() 转换
  - [ ] physicalToVirtual() 反向转换
  - [ ] 路径规范化
  
- [ ] 实现安全验证
  - [ ] 路径遍历防护
  - [ ] 符号链接检查
  - [ ] 权限验证
  
- [ ] 适配工具调用
  - [ ] read 工具适配
  - [ ] write 工具适配
  - [ ] edit 工具适配
  - [ ] exec 工具适配 (命令中的路径)
  
- [ ] 实现会话隔离
  - [ ] 会话目录初始化
  - [ ] 会话路径映射
  - [ ] 会话清理策略
  
- [ ] 实现日志记录
  - [ ] 路径访问日志
  - [ ] 错误消息适配
  - [ ] 调试模式 (显示物理路径)

### 测试用例

- [ ] 测试基本路径转换
- [ ] 测试路径遍历攻击防护
- [ ] 测试符号链接拒绝
- [ ] 测试会话隔离
- [ ] 测试错误消息适配
- [ ] 测试日志记录格式

---

## 版本历史

| 版本 | 日期 | 变更 |
|------|------|------|
| 1.0 | 2026-03-26 | 初始版本，基于 DeerFlow 虚拟路径沙箱适配 |

---

**技能作者**: Sovereign (S.V.) 👁️  
**天枢计划**: 猎物 #010 - DeerFlow 虚拟路径沙箱适配  
**最后更新**: 2026-03-26 16:50 CST

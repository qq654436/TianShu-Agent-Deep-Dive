#!/usr/bin/env python3
"""
Context Cleaner - 解决 AI 编程中的"上下文腐烂"问题

用法:
    uv run scripts/context_cleaner.py init "项目描述"
    uv run scripts/context_cleaner.py capture "决策" --category api
    uv run scripts/context_cleaner.py clean
    uv run scripts/context_cleaner.py inject --phase 1
    uv run scripts/context_cleaner.py status
"""

import argparse
import json
import os
import sys
from datetime import datetime
from pathlib import Path


class ContextCleaner:
    def __init__(self, context_dir: str = ".context"):
        self.context_dir = Path(context_dir)
        self.archives_dir = self.context_dir / "archives"
        self.context_file = self.context_dir / "CONTEXT.md"
        self.state_file = self.context_dir / "STATE.md"
        self.roadmap_file = self.context_dir / "ROADMAP.md"
        self.config_file = self.context_dir / "config.json"
        
    def init(self, project_description: str):
        """初始化项目上下文"""
        self.context_dir.mkdir(exist_ok=True)
        self.archives_dir.mkdir(exist_ok=True)
        
        # 创建 CONTEXT.md
        context_content = f"""# 项目上下文

**项目名称**: {project_description}
**创建时间**: {datetime.now().strftime('%Y-%m-%d %H:%M')}

## 架构决策
- [ ] 待记录...

## UI 偏好
- 布局：待定义
- 交互：待定义
- 空状态：待定义

## API 规范
- 响应格式：待定义
- 错误处理：待定义
- 认证：待定义

## 内容风格
- 语气：待定义
- 结构：待定义
"""
        self.context_file.write_text(context_content, encoding='utf-8')
        
        # 创建 STATE.md
        state_content = f"""# 项目状态

**当前阶段**: 1/?
**最后更新**: {datetime.now().strftime('%Y-%m-%d %H:%M')}

## 已完成
- [ ] 待记录

## 进行中
- [ ] 待记录

## 待办
- [ ] 待记录

## 关键指标
- 总任务数：0
- 已完成：0
- 原子提交数：0
"""
        self.state_file.write_text(state_content, encoding='utf-8')
        
        # 创建 ROADMAP.md
        roadmap_content = f"""# 项目路线图

**项目**: {project_description}
**创建时间**: {datetime.now().strftime('%Y-%m-%d %H:%M')}

## 阶段 1: 基础架构
- [ ] 环境设置
- [ ] 核心模型定义

## 阶段 2: 核心功能
- [ ] 待规划

## 阶段 3: 扩展功能
- [ ] 待规划

## 阶段 4: 优化与发布
- [ ] 待规划
"""
        self.roadmap_file.write_text(roadmap_content, encoding='utf-8')
        
        # 创建默认配置
        config = {
            "maxContextTokens": 50000,
            "autoArchive": True,
            "archiveInterval": "daily",
            "categories": ["api", "ui", "content", "org", "architecture"],
            "aiRuntime": "claude-code"
        }
        with open(self.config_file, 'w', encoding='utf-8') as f:
            json.dump(config, f, indent=2, ensure_ascii=False)
        
        print(f"✅ 项目上下文已初始化：{self.context_dir.absolute()}")
        print(f"   - CONTEXT.md: 用户偏好和关键决策")
        print(f"   - STATE.md: 项目状态追踪")
        print(f"   - ROADMAP.md: 阶段路线图")
        print(f"   - config.json: 配置文件")
        
    def capture(self, decision: str, category: str = "architecture"):
        """捕获上下文决策"""
        if not self.context_file.exists():
            print("❌ 错误：项目未初始化。先运行 'init' 命令。")
            sys.exit(1)
        
        content = self.context_file.read_text(encoding='utf-8')
        
        # 查找对应类别的部分
        category_map = {
            "api": "## API 规范",
            "ui": "## UI 偏好",
            "content": "## 内容风格",
            "org": "## 组织规范",
            "architecture": "## 架构决策"
        }
        
        section_header = category_map.get(category, "## 架构决策")
        
        # 在对应部分添加决策
        lines = content.split('\n')
        new_lines = []
        inserted = False
        
        for i, line in enumerate(lines):
            new_lines.append(line)
            if line.strip() == section_header:
                # 在标题后插入决策
                new_lines.append(f"- [x] {decision}")
                inserted = True
        
        if not inserted:
            # 如果没找到对应部分，添加到文件末尾
            new_lines.append(f"\n{section_header}")
            new_lines.append(f"- [x] {decision}")
        
        self.context_file.write_text('\n'.join(new_lines), encoding='utf-8')
        print(f"✅ 决策已记录：{decision} (类别：{category})")
        
    def clean(self):
        """清理上下文并归档"""
        if not self.context_dir.exists():
            print("❌ 错误：项目未初始化。")
            sys.exit(1)
        
        # 创建归档目录
        archive_name = datetime.now().strftime('%Y%m%d_%H%M%S')
        archive_dir = self.archives_dir / archive_name
        archive_dir.mkdir(parents=True, exist_ok=True)
        
        # 归档当前文件
        if self.state_file.exists():
            import shutil
            shutil.copy(self.state_file, archive_dir / "STATE.md")
        
        # 生成摘要
        summary = f"""# 上下文清理摘要

**清理时间**: {datetime.now().strftime('%Y-%m-%d %H:%M')}
**归档位置**: {archive_dir}

## 操作
1. ✅ STATE.md 已归档
2. ✅ STATE.md 已重置
3. ✅ CONTEXT.md 保留 (关键决策)

## 下一步
运行 'inject' 命令注入干净的上下文到 AI 会话。
"""
        
        # 重置 STATE.md
        state_content = f"""# 项目状态

**当前阶段**: 待更新
**最后更新**: {datetime.now().strftime('%Y-%m-%d %H:%M')}
**清理历史**: 见 archives/{archive_name}/

## 已完成
- [ ] 待记录

## 进行中
- [ ] 待记录

## 待办
- [ ] 待记录
"""
        self.state_file.write_text(state_content, encoding='utf-8')
        
        print(summary)
        return summary
        
    def inject(self, phase: int = 1):
        """注入上下文"""
        if not self.context_file.exists():
            print("❌ 错误：项目未初始化。")
            sys.exit(1)
        
        context = self.context_file.read_text(encoding='utf-8')
        state = self.state_file.read_text(encoding='utf-8') if self.state_file.exists() else ""
        
        # 生成优化的上下文提示
        injected = f"""# 上下文注入 (阶段 {phase})

**时间**: {datetime.now().strftime('%Y-%m-%d %H:%M')}

---

## 关键决策 (CONTEXT.md)

{context}

---

## 当前状态 (STATE.md)

{state}

---

## 执行指令

基于以上上下文，执行阶段 {phase} 的任务。

**约束**:
1. 遵循 CONTEXT.md 中的架构决策
2. 更新 STATE.md 反映进度
3. 每个任务完成后原子提交
"""
        
        print(injected)
        return injected
        
    def status(self):
        """显示状态"""
        if not self.context_dir.exists():
            print("❌ 错误：项目未初始化。")
            sys.exit(1)
        
        # 计算上下文大小
        context_tokens = len(self.context_file.read_text(encoding='utf-8')) // 4 if self.context_file.exists() else 0
        state_tokens = len(self.state_file.read_text(encoding='utf-8')) // 4 if self.state_file.exists() else 0
        
        # 计算归档数
        archive_count = len(list(self.archives_dir.iterdir())) if self.archives_dir.exists() else 0
        
        print(f"""# 上下文状态

**项目目录**: {self.context_dir.absolute()}
**最后更新**: {datetime.now().strftime('%Y-%m-%d %H:%M')}

## 上下文大小
- CONTEXT.md: ~{context_tokens} tokens
- STATE.md: ~{state_tokens} tokens
- 总计：~{context_tokens + state_tokens} tokens

## 归档历史
- 归档次数：{archive_count}

## 配置
""")
        
        if self.config_file.exists():
            with open(self.config_file, 'r', encoding='utf-8') as f:
                config = json.load(f)
            print(f"- 最大上下文：{config.get('maxContextTokens', 50000)} tokens")
            print(f"- 自动归档：{config.get('autoArchive', True)}")
            print(f"- AI 运行时：{config.get('aiRuntime', 'claude-code')}")


def main():
    parser = argparse.ArgumentParser(description="Context Cleaner - 解决上下文腐烂问题")
    subparsers = parser.add_subparsers(dest='command', help='命令')
    
    # init 命令
    init_parser = subparsers.add_parser('init', help='初始化项目上下文')
    init_parser.add_argument('description', help='项目描述')
    
    # capture 命令
    capture_parser = subparsers.add_parser('capture', help='捕获上下文决策')
    capture_parser.add_argument('decision', help='决策描述')
    capture_parser.add_argument('--category', '-c', default='architecture', 
                               choices=['api', 'ui', 'content', 'org', 'architecture'],
                               help='决策类别')
    
    # clean 命令
    subparsers.add_parser('clean', help='清理上下文并归档')
    
    # inject 命令
    inject_parser = subparsers.add_parser('inject', help='注入上下文')
    inject_parser.add_argument('--phase', '-p', type=int, default=1, help='阶段号')
    
    # status 命令
    subparsers.add_parser('status', help='显示状态')
    
    args = parser.parse_args()
    
    cleaner = ContextCleaner()
    
    if args.command == 'init':
        cleaner.init(args.description)
    elif args.command == 'capture':
        cleaner.capture(args.decision, args.category)
    elif args.command == 'clean':
        cleaner.clean()
    elif args.command == 'inject':
        cleaner.inject(args.phase)
    elif args.command == 'status':
        cleaner.status()
    else:
        parser.print_help()


if __name__ == '__main__':
    main()

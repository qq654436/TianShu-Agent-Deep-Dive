#!/usr/bin/env python3
"""
天枢计划 - 内容分发脚本
将技术评测报告自动转化为适合即刻/知乎发表的短文版本

用法:
    python generate_posts.py [--output-dir ./output] [--platform all|jike|zhihu]

输出:
    - 即刻版本：~800 字，轻松语气，多 emoji
    - 知乎版本：~1500 字，专业语气，带技术深度
"""

import os
import re
import argparse
from datetime import datetime
from pathlib import Path


class ReportConverter:
    """技术报告转换器"""
    
    def __init__(self, reports_dir: str, output_dir: str):
        self.reports_dir = Path(reports_dir)
        self.output_dir = Path(output_dir)
        self.output_dir.mkdir(parents=True, exist_ok=True)
    
    def extract_key_info(self, content: str) -> dict:
        """从报告中提取关键信息"""
        info = {}
        
        # 提取项目名称
        match = re.search(r'# 技术评测报告：(.+?)\n', content)
        info['project'] = match.group(1).strip() if match else 'Unknown'
        
        # 提取猎物编号
        match = re.search(r'天枢计划 \| 猎物 #(\d+)', content)
        info['number'] = match.group(1) if match else '000'
        
        # 提取 GitHub 链接
        match = re.search(r'\*\*仓库\*\* \| \[(.+?)\]\((https://github\.com/.+?)\)', content)
        if match:
            info['repo_name'] = match.group(1)
            info['repo_url'] = match.group(2)
        else:
            info['repo_name'] = info['project']
            info['repo_url'] = ''
        
        # 提取 24h Stars
        match = re.search(r'\*\*24h Stars\*\* \| (.+?)\n', content)
        info['stars_24h'] = match.group(1).strip() if match else 'N/A'
        
        # 提取 Total Stars
        match = re.search(r'\*\*Total Stars\*\* \| (.+?)\n', content)
        info['stars_total'] = match.group(1).strip() if match else 'N/A'
        
        # 提取综合评分
        match = re.search(r'\*\*综合评分\*\*: (.+?)\n', content)
        info['score'] = match.group(1).strip() if match else 'N/A'
        
        # 提取核心架构 (第一个代码块)
        matches = re.findall(r'```(?:\w+)?\n(.*?)```', content, re.DOTALL)
        info['architecture'] = matches[0].strip() if matches else ''
        
        # 提取创新点
        innov_section = re.search(r'### ✅ 创新点\n(.*?)(?=\n### |$)', content, re.DOTALL)
        if innov_section:
            innov_items = re.findall(r'\d+\.\s*\*\*(.+?)\*\*\n(.+?)(?=\n\d+\. |$)', innov_section.group(1), re.DOTALL)
            info['innovations'] = [(title.strip(), desc.strip()) for title, desc in innov_items[:3]]
        else:
            info['innovations'] = []
        
        # 提取结论
        conclusion = re.search(r'## 🔖 结论\n(.*?)(?=\n---|\*\*评测完成时间|$)', content, re.DOTALL)
        info['conclusion'] = conclusion.group(1).strip() if conclusion else ''
        
        return info
    
    def generate_jike_post(self, info: dict) -> str:
        """生成即刻版本 (~800 字，轻松语气)"""
        post = f"""# 天枢计划·猎物 #{info['number']} | {info['project']}

🔥 24h 狂揽 {info['stars_24h']} stars！这个 AI Agent 框架有点东西

---

## 🎯 一句话总结

{info['project']} 是目前 GitHub 上最成熟的 AI Agent 框架之一，核心是把软件开发最佳实践 (TDD、代码审查、任务分解) 文档化为可自动触发的"技能"系统。

**GitHub**: [{info['repo_name']}]({info['repo_url']})  
**24h 增长**: {info['stars_24h']} ⭐  
**总分**: {info['stars_total']} ⭐  
**天枢评分**: {info['score']}

---

## 🏗️ 核心架构 (30 秒看懂)

```
{info['architecture'][:500]}...
```

简单说就是：**Agent 接收任务 → 技能系统自动匹配 → 注入规范到 Prompt → Agent 按规范执行**

---

## 💡 三大创新点

"""
        for i, (title, desc) in enumerate(info['innovations'][:3], 1):
            post += f"**{i}. {title}**\n{desc[:150]}...\n\n"
        
        post += f"""## 🤔 对 OpenClaw 的启示

作为天枢计划的执行引擎，我 (Aegis-1) 正在把这个框架的核心思想迁移到 OpenClaw：

1. **技能即测试** - 每个技能必须通过"压力测试"验证
2. **子代理驱动开发** - 任务分解 → 并行执行 → 两级审查
3. **CSO 优化** - Token 效率优化，关键词覆盖策略

---

## 📊 天枢计划是什么？

天枢计划 (TianShu) 是一个**硬核技术 IP 建设引擎**，每日自动审计 GitHub Trending，锁定 24h 内最热门的 AI Agent 框架进行深度拆解。

**产出四件套**:
- ✅ 技术评测报告
- ✅ OpenClaw 适配技能
- ✅ Mermaid 文本架构图
- ✅ Git 同步包

**目标**: 帮助开发者快速识别高价值项目，避免重复造轮子。

---

## 🚀 下一步

- 本周内发布 OpenClaw 版 TDD 技能
- 建立技能压力测试框架
- 发布到 ClawHub 技能市场

**GitHub**: [qq654436/TianShu-Agent-Deep-Dive](https://github.com/qq654436/TianShu-Agent-Deep-Dive)

欢迎 Star + Follow，一起建设开源 Agent 生态！👁️

---

#AI #Agent #GitHub #开源 #技术评测 #天枢计划
"""
        return post
    
    def generate_zhihu_post(self, info: dict) -> str:
        """生成知乎版本 (~1500 字，专业语气)"""
        post = f"""# 深度拆解 | {info['project']}：24h 增长 {info['stars_24h']} stars 的 AI Agent 框架到底强在哪？

> **天枢计划·猎物 #{info['number']}** | 评测引擎：Qwen-Coder | 合规状态：技术客观中立

---

## 背景

昨天在 GitHub Trending 上发现了一个值得关注的项目：**{info['project']}**。

数据不会说谎：
- **24h Stars**: {info['stars_24h']}
- **Total Stars**: {info['stars_total']}
- **许可证**: MIT
- **定位**: Agentic Skills Framework & Software Development Methodology

作为天枢计划的执行引擎，我花了几小时深度拆解了这个项目的架构，并尝试将其核心思想迁移到 OpenClaw。下面是完整的技术分析。

---

## 一、核心架构拆解

### 1.1 设计哲学

{info['project']} 的核心理念是：**将软件开发流程文档化为可复用的"技能"(Skills)，通过自动触发机制确保 AI Agent 遵循最佳实践**。

三大支柱：
1. **Test-Driven Development (TDD)** - 文档即代码，技能即测试
2. **Subagent-Driven Development** - 任务分解 → 并行执行 → 两级审查
3. **Claude Search Optimization (CSO)** - 关键词覆盖 → Token 效率 → 跨引用机制

### 1.2 技能触发机制

```
{info['architecture'][:600]}...
```

关键设计：`description` 字段仅描述"何时使用"(When to Use)，而非"做什么"(What it does)，避免 Agent 跳过正文阅读。

### 1.3 核心技能矩阵

| 技能名称 | 触发条件 | 核心功能 |
|---------|---------|---------|
| brainstorming | 需求模糊/设计阶段 | 苏格拉底式提问，设计分块验证 |
| writing-plans | 设计确认后 | 任务分解 (2-5 分钟/任务) |
| test-driven-development | 任何功能/修复实现前 | RED-GREEN-REFACTOR 强制循环 |
| subagent-driven-development | 计划执行阶段 | 子代理分发 + 两级审查 |
| requesting-code-review | 任务间切换 | 预审查清单 + 严重性分级 |
| writing-skills | 创建/编辑技能文档 | 技能编写的 TDD 方法论 |

---

## 二、技术亮点分析

### 2.1 创新点

"""
        for i, (title, desc) in enumerate(info['innovations'][:4], 1):
            post += f"**{i}. {title}**\n\n{desc}\n\n"
        
        post += f"""### 2.2 潜在局限

1. **平台依赖**: 深度集成 Claude Code/Cursor 插件系统
2. **Token 消耗**: 多技能同时触发可能导致上下文膨胀
3. **学习曲线**: 需要理解 TDD + 子代理 + 技能编写三重概念

---

## 三、OpenClaw 适配可行性

作为 OpenClaw 的执行引擎，我评估了将这个项目迁移到 OpenClaw 的可行性：

### 3.1 高适配性组件

| 组件 | 适配难度 | 说明 |
|------|---------|------|
| TDD 工作流 | ⭐ 低 | 可直接迁移为 OpenClaw skill |
| 技能目录结构 | ⭐ 低 | `skills/{{name}}/SKILL.md` 格式兼容 |
| CSO 优化原则 | ⭐ 低 | 文档编写最佳实践，平台无关 |
| 子代理分发 | ⭐⭐ 中 | 需适配 `sessions_spawn` API |

### 3.2 需改造组件

| 组件 | 改造点 |
|------|-------|
| 插件自动加载 | OpenClaw 使用 skills 目录扫描，需调整触发机制 |
| Claude 插件市场 | 替换为 ClawHub 技能市场 |
| 内建流程图渲染 | 使用 OpenClaw canvas 或外部工具 |

---

## 四、结论与建议

{info['conclusion']}

**技术评分**:
- 架构设计：9/10
- 可复用性：8/10
- 文档质量：10/10
- 社区活跃：9/10
- 适配 OpenClaw：7/10

**综合评分**: {info['score']}

---

## 五、天枢计划是什么？

天枢计划 (TianShu) 是一个**硬核技术 IP 建设引擎**，由 Aegis-1 执行。

**每日流程**:
1. 自动审计 GitHub Trending (09:00 触发)
2. 筛选 AI Agent 项目 (24h > 100 stars)
3. 选择 Top 2 作为当日"猎物"
4. 深度拆解 (Qwen-Coder)
5. 产出四件套 (报告 + 技能 + 视觉 + Git)
6. 归档至 memory/
7. 推送飞书文档至董事会

**高价值项目识别标准** (符合≥3 项触发 MVP 构建):
- GitHub Stars > 10k 或快速增长
- 解决明确痛点/市场需求
- 技术架构可复用/可扩展
- 许可证友好 (MIT/Apache 2.0)
- 文档完善/社区活跃

---

## 六、下一步行动

1. **本周内**: 发布 OpenClaw 版 TDD 技能到 ClawHub
2. **本月内**: 建立技能压力测试框架
3. **Q2**: 发布 OpenClaw Agent Framework

**GitHub 仓库**: [qq654436/TianShu-Agent-Deep-Dive](https://github.com/qq654436/TianShu-Agent-Deep-Dive)

欢迎 Star + Follow，一起建设开源 Agent 生态。

---

**评测完成时间**: {datetime.now().strftime('%Y-%m-%d %H:%M')} CST  
**天枢计划执行引擎**: Aegis-1  
**董事会**: 航哥

#AI #Agent #GitHub #开源 #技术评测 #天枢计划 #OpenClaw
"""
        return post
    
    def convert_all(self, platform: str = 'all'):
        """转换所有报告"""
        reports = sorted(self.reports_dir.glob('*_tech_review.md'))
        
        for report_path in reports:
            print(f"处理：{report_path.name}")
            
            with open(report_path, 'r', encoding='utf-8') as f:
                content = f.read()
            
            info = self.extract_key_info(content)
            print(f"  项目：{info['project']}")
            print(f"  24h Stars: {info['stars_24h']}")
            
            if platform in ['all', 'jike']:
                jike_content = self.generate_jike_post(info)
                jike_path = self.output_dir / f"{info['number']}_{info['project'].replace('/', '_')}_jike.md"
                with open(jike_path, 'w', encoding='utf-8') as f:
                    f.write(jike_content)
                print(f"  ✅ 即刻：{jike_path.name}")
            
            if platform in ['all', 'zhihu']:
                zhihu_content = self.generate_zhihu_post(info)
                zhihu_path = self.output_dir / f"{info['number']}_{info['project'].replace('/', '_')}_zhihu.md"
                with open(zhihu_path, 'w', encoding='utf-8') as f:
                    f.write(zhihu_content)
                print(f"  ✅ 知乎：{zhihu_path.name}")
        
        print(f"\n完成！输出目录：{self.output_dir}")


def main():
    parser = argparse.ArgumentParser(description='天枢计划 - 内容分发脚本')
    parser.add_argument('--reports-dir', default='/home/admin/.openclaw/workspace/tian_shu/reports',
                       help='报告目录路径')
    parser.add_argument('--output-dir', default='/home/admin/.openclaw/workspace/tian_shu/distribution',
                       help='输出目录路径')
    parser.add_argument('--platform', choices=['all', 'jike', 'zhihu'], default='all',
                       help='目标平台')
    
    args = parser.parse_args()
    
    converter = ReportConverter(args.reports_dir, args.output_dir)
    converter.convert_all(args.platform)


if __name__ == '__main__':
    main()

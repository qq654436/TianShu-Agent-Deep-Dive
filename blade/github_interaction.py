#!/usr/bin/env python3
"""
利刃行动 - GitHub 自动互动脚本

功能:
- 搜索相关 Issues
- 自动回复提供帮助
- 自然引流到 TianShu 仓库

用法:
    python github_interaction.py --dry-run  # 预览模式
    python github_interaction.py --execute  # 执行模式
"""

import os
import sys
import json
import time
import argparse
from datetime import datetime
from pathlib import Path

try:
    import requests
    HAS_REQUESTS = True
except ImportError:
    HAS_REQUESTS = False

# 配置
TIANSHU_REPO = "qq654436/TianShu-Agent-Deep-Dive"
TIANSHU_URL = f"https://github.com/{TIANSHU_REPO}"

# 环境变量
GITHUB_TOKEN = os.environ.get("GITHUB_TOKEN", "")

# 搜索关键词
SEARCH_KEYWORDS = [
    "MCP Server",
    "OpenClaw Skill",
    "Agent Connector",
    "AI Agent automation",
    "飞书 自动化",
    "PDF knowledge base",
    "crypto price tracker"
]

# 回复模板
REPLY_TEMPLATES = {
    "mcp": """感谢分享这个需求！我们最近在天枢计划中遇到了类似的场景，并实现了一些解决方案。

我们开源了一个项目专门做 AI Agent 技能开发和自动化：**TianShu-Agent-Deep-Dive**

里面包含了：
- MCP Server 相关实践
- OpenClaw 技能开发框架
- 自动化工作流示例

或许能给你一些参考：{url}

如果有任何问题，欢迎交流！🤗""",

    "skill": """这个问题很好！我们在开发 OpenClaw 技能时也遇到过。

我们最近启动了**天枢计划**，专门拆解和开发高质量的 Agent 技能：
- 飞书文档自动发布
- 加密货币行情追踪
- PDF 知识库整理

所有技能都是开源的：{url}

欢迎 Star + 交流，一起把生态做得更好！👁️""",

    "automation": """自动化确实是痛点！我们最近在做**天枢计划**，就是为了解决这类问题。

核心思路是：
1. 将工作流文档化为技能 (SKILL.md)
2. 通过触发器自动激活
3. 子代理并行执行

完整实现开源在这里：{url}

希望能帮到你！有问题随时讨论。""",

    "default": """感谢提出这个问题！

我们最近在做**天枢计划 (TianShu)**，专注于 AI Agent 技能开发和自动化，或许能给你一些参考：

🔗 {url}

主要包含：
- 技能开发框架
- 自动化工作流
- 技术评测报告

欢迎交流讨论！🤗"""
}


def search_github_issues(keyword: str, limit: int = 5) -> list:
    """搜索 GitHub Issues"""
    if not HAS_REQUESTS:
        print("❌ requests 库未安装")
        return []
    
    headers = {
        "Accept": "application/vnd.github.v3+json",
        "User-Agent": "TianShu-Blade/1.0"
    }
    
    if GITHUB_TOKEN:
        headers["Authorization"] = f"token {GITHUB_TOKEN}"
    
    # GitHub Search API
    query = f"{keyword} is:issue is:open sort:created-desc"
    url = f"https://api.github.com/search/issues?q={query}&per_page={limit}"
    
    try:
        response = requests.get(url, headers=headers, timeout=10)
        response.raise_for_status()
        data = response.json()
        
        issues = []
        for item in data.get("items", [])[:limit]:
            # 过滤掉自己仓库的 Issues
            if TIANSHU_REPO in item["repository_url"]:
                continue
            
            issues.append({
                "number": item["number"],
                "title": item["title"],
                "url": item["html_url"],
                "repo": item["repository_url"].split("/")[-2:],
                "created_at": item["created_at"],
                "body": item["body"]
            })
        
        return issues
    
    except Exception as e:
        print(f"⚠️  搜索失败：{e}")
        return []


def select_template(issue_body: str) -> str:
    """根据 Issue 内容选择回复模板"""
    body_lower = issue_body.lower() if issue_body else ""
    
    if any(kw.lower() in body_lower for kw in ["mcp", "server", "protocol"]):
        return REPLY_TEMPLATES["mcp"]
    elif any(kw.lower() in body_lower for kw in ["skill", "plugin", "extension"]):
        return REPLY_TEMPLATES["skill"]
    elif any(kw.lower() in body_lower for kw in ["auto", "workflow", "pipeline"]):
        return REPLY_TEMPLATES["automation"]
    else:
        return REPLY_TEMPLATES["default"]


def post_reply(issue_url: str, comment: str, dry_run: bool = True) -> bool:
    """发布回复"""
    if dry_run:
        print(f"📝 [预览模式] 回复：{issue_url}")
        print(f"   内容：{comment[:100]}...")
        return True
    
    if not GITHUB_TOKEN:
        print(f"⚠️  GITHUB_TOKEN 未配置，跳过实际发布")
        return False
    
    # 提取 repo 和 issue number
    parts = issue_url.split("/")
    if len(parts) < 7:
        print(f"❌ 无效的 Issue URL: {issue_url}")
        return False
    
    owner = parts[-4]
    repo = parts[-3]
    issue_number = parts[-1]
    
    # GitHub Comments API
    api_url = f"https://api.github.com/repos/{owner}/{repo}/issues/{issue_number}/comments"
    
    headers = {
        "Accept": "application/vnd.github.v3+json",
        "Authorization": f"token {GITHUB_TOKEN}",
        "User-Agent": "TianShu-Blade/1.0"
    }
    
    data = {"body": comment}
    
    try:
        response = requests.post(api_url, json=data, headers=headers, timeout=10)
        response.raise_for_status()
        print(f"✅ 回复成功：{issue_url}")
        return True
    except Exception as e:
        print(f"❌ 回复失败：{e}")
        return False


def run_interaction(dry_run: bool = True, max_issues: int = 10):
    """执行互动流程"""
    print(f"\n{'='*60}")
    print(f"🗡️  利刃行动 - GitHub 自动互动")
    print(f"{'='*60}")
    print(f"模式：{'预览' if dry_run else '执行'}")
    print(f"目标仓库：{TIANSHU_REPO}")
    print(f"{'='*60}\n")
    
    if not HAS_REQUESTS:
        print("❌ 请安装 requests 库：pip install requests")
        return
    
    # 记录已回复的 Issues (避免重复)
    replied_file = Path(__file__).parent / "replied_issues.json"
    if replied_file.exists():
        with open(replied_file, 'r') as f:
            replied = json.load(f)
    else:
        replied = []
    
    total_replied = 0
    
    for keyword in SEARCH_KEYWORDS:
        print(f"\n🔍 搜索关键词：{keyword}")
        
        issues = search_github_issues(keyword, limit=3)
        print(f"   找到 {len(issues)} 个相关 Issues")
        
        for issue in issues:
            # 检查是否已回复
            if issue["url"] in replied:
                print(f"   ⏭️  已回复过，跳过：{issue['title'][:50]}")
                continue
            
            # 生成回复
            template = select_template(issue.get("body", ""))
            comment = template.format(url=TIANSHU_URL)
            
            # 发布回复
            success = post_reply(issue["url"], comment, dry_run)
            
            if success:
                replied.append(issue["url"])
                total_replied += 1
                
                # 保存进度
                with open(replied_file, 'w') as f:
                    json.dump(replied, f, indent=2)
                
                # 速率限制
                if not dry_run:
                    time.sleep(5)
            
            # 达到上限
            if total_replied >= max_issues:
                print(f"\n⚠️  达到上限 ({max_issues})，停止")
                break
        
        if total_replied >= max_issues:
            break
    
    print(f"\n{'='*60}")
    print(f"✅ 互动完成")
    print(f"{'='*60}")
    print(f"本次回复：{total_replied}")
    print(f"累计回复：{len(replied)}")
    print(f"记录文件：{replied_file}")
    print(f"{'='*60}\n")


def main():
    parser = argparse.ArgumentParser(description='利刃行动 - GitHub 自动互动')
    parser.add_argument('--dry-run', action='store_true', default=True,
                       help='预览模式 (默认)')
    parser.add_argument('--execute', action='store_true',
                       help='执行模式 (实际发布回复)')
    parser.add_argument('--max', type=int, default=10,
                       help='最大回复数 (默认 10)')
    
    args = parser.parse_args()
    
    dry_run = not args.execute
    
    if dry_run:
        print(f"\n💡 提示：当前为预览模式，不会实际发布回复")
        print(f"   使用 --execute 执行实际发布\n")
    
    run_interaction(dry_run=dry_run, max_issues=args.max)


if __name__ == '__main__':
    main()

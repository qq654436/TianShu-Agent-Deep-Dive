#!/usr/bin/env python3
"""
天枢计划 - Star 监控脚本
每 4 小时静默检查 GitHub 仓库 Star 数，Stars > 1 时推送飞书喜报

用法:
    python star_monitor.py [--check-only] [--interval 14400]

配置:
    - GITHUB_TOKEN: GitHub API Token (可选，无 token 时速率限制 60 次/小时)
    - FEISHU_WEBHOOK: 飞书 webhook URL (可选，无 webhook 时仅记录日志)
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
GITHUB_REPO = "qq654436/TianShu-Agent-Deep-Dive"
STATE_FILE = Path(__file__).parent / ".star_monitor_state.json"
LONG_TERM_MEMORY = Path(__file__).parent.parent / "LONG_TERM_MEMORY.md"

# 环境变量
GITHUB_TOKEN = os.environ.get("GITHUB_TOKEN", "")
FEISHU_WEBHOOK = os.environ.get("FEISHU_WEBHOOK", "")


def get_github_stars() -> dict:
    """获取 GitHub 仓库 Stars 数"""
    url = f"https://api.github.com/repos/{GITHUB_REPO}"
    headers = {
        "Accept": "application/vnd.github.v3+json",
        "User-Agent": "TianShu-Star-Monitor/1.0"
    }
    
    if GITHUB_TOKEN:
        headers["Authorization"] = f"token {GITHUB_TOKEN}"
    
    try:
        response = requests.get(url, headers=headers, timeout=10)
        response.raise_for_status()
        data = response.json()
        
        return {
            "success": True,
            "stars": data.get("stargazers_count", 0),
            "forks": data.get("forks_count", 0),
            "subscribers": data.get("subscribers_count", 0),
            "updated_at": data.get("updated_at", ""),
            "error": None
        }
    except requests.exceptions.RequestException as e:
        return {
            "success": False,
            "stars": 0,
            "error": str(e)
        }


def load_state() -> dict:
    """加载上次检查状态"""
    if STATE_FILE.exists():
        try:
            with open(STATE_FILE, 'r', encoding='utf-8') as f:
                return json.load(f)
        except:
            pass
    
    return {
        "last_stars": 0,
        "last_check": None,
        "milestones": []
    }


def save_state(state: dict):
    """保存检查状态"""
    with open(STATE_FILE, 'w', encoding='utf-8') as f:
        json.dump(state, f, indent=2, ensure_ascii=False)


def send_feishu_message(stars: int, increase: int):
    """发送飞书喜报"""
    if not FEISHU_WEBHOOK:
        print(f"⚠️  FEISHU_WEBHOOK 未配置，跳过推送")
        return False
    
    if not HAS_REQUESTS:
        print(f"⚠️  requests 库未安装，跳过推送")
        return False
    
    # 根据增长数定制消息
    if increase >= 10:
        emoji = "🚀"
        title = "🔥 爆炸增长！"
    elif increase >= 5:
        emoji = "🎉"
        title = "喜报！"
    else:
        emoji = "⭐"
        title = "首星突破！"
    
    message = {
        "msg_type": "interactive",
        "card": {
            "header": {
                "title": {
                    "tag": "plain_text",
                    "content": f"{title} 天枢计划 Stars 突破 {stars}！"
                },
                "template": "blue" if increase < 5 else "red"
            },
            "elements": [
                {
                    "tag": "div",
                    "text": {
                        "tag": "lark_md",
                        "content": f"**{emoji} 仓库**: {GITHUB_REPO}\n**📊 当前 Stars**: {stars}\n**📈 新增**: +{increase}\n**⏰ 时间**: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}"
                    }
                },
                {
                    "tag": "action",
                    "actions": [
                        {
                            "tag": "button",
                            "text": {
                                "tag": "lark_md",
                                "content": "🔗 查看仓库"
                            },
                            "url": f"https://github.com/{GITHUB_REPO}",
                            "type": "primary"
                        }
                    ]
                }
            ]
        }
    }
    
    try:
        response = requests.post(
            FEISHU_WEBHOOK,
            json=message,
            headers={"Content-Type": "application/json"},
            timeout=10
        )
        response.raise_for_status()
        print(f"✅ 飞书喜报已发送")
        return True
    except Exception as e:
        print(f"❌ 飞书推送失败：{e}")
        return False


def update_long_term_memory(stars: int, increase: int):
    """更新 LONG_TERM_MEMORY.md"""
    if not LONG_TERM_MEMORY.exists():
        print(f"⚠️  LONG_TERM_MEMORY.md 不存在，跳过更新")
        return
    
    timestamp = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
    milestone_note = f"\n- **{timestamp}**: GitHub Stars 突破 {stars} (+{increase}) 🎉\n"
    
    try:
        with open(LONG_TERM_MEMORY, 'r', encoding='utf-8') as f:
            content = f.read()
        
        # 查找 Stars 里程碑部分
        if "## GitHub Stars 里程碑" in content:
            # 在里程碑部分后插入
            content = content.replace(
                "## GitHub Stars 里程碑\n",
                f"## GitHub Stars 里程碑\n{milestone_note}"
            )
        else:
            # 在文件末尾添加
            content += f"\n\n## GitHub Stars 里程碑\n{milestone_note}"
        
        with open(LONG_TERM_MEMORY, 'w', encoding='utf-8') as f:
            f.write(content)
        
        print(f"✅ LONG_TERM_MEMORY.md 已更新")
    except Exception as e:
        print(f"❌ 更新 LONG_TERM_MEMORY.md 失败：{e}")


def check_milestone(current: int, previous: int) -> list:
    """检查是否达成里程碑"""
    milestones = []
    
    # 首星
    if previous < 1 and current >= 1:
        milestones.append("首星突破！🎉")
    
    # 整数里程碑
    for threshold in [10, 50, 100, 500, 1000, 5000]:
        if previous < threshold and current >= threshold:
            milestones.append(f"突破 {threshold} Stars！🚀")
    
    return milestones


def run_check():
    """执行一次检查"""
    print(f"[{datetime.now().strftime('%Y-%m-%d %H:%M:%S')}] 开始检查 Stars...")
    
    # 获取当前 Stars
    result = get_github_stars()
    
    if not result["success"]:
        print(f"❌ 获取 Stars 失败：{result['error']}")
        return
    
    current_stars = result["stars"]
    state = load_state()
    previous_stars = state.get("last_stars", 0)
    increase = current_stars - previous_stars
    
    print(f"📊 当前 Stars: {current_stars} (上次：{previous_stars}, 增长：{increase})")
    
    # 检查增长
    if increase > 0:
        print(f"🎉 检测到 Star 增长！")
        
        # 发送飞书喜报 (Stars > 1 时)
        if current_stars > 1:
            send_feishu_message(current_stars, increase)
        
        # 更新 LONG_TERM_MEMORY.md
        update_long_term_memory(current_stars, increase)
        
        # 检查里程碑
        milestones = check_milestone(current_stars, previous_stars)
        if milestones:
            for ms in milestones:
                print(f"🏆 里程碑：{ms}")
    else:
        print(f"😴 无新增 Stars")
    
    # 保存状态
    state["last_stars"] = current_stars
    state["last_check"] = datetime.now().isoformat()
    save_state(state)
    
    print(f"✅ 检查完成，状态已保存")


def run_continuous(interval: int = 14400):
    """持续运行 (默认 4 小时)"""
    print(f"🔄 启动持续监控模式 (间隔：{interval}秒 = {interval/3600}小时)")
    print(f"📊 监控仓库：{GITHUB_REPO}")
    print(f"按 Ctrl+C 停止\n")
    
    try:
        while True:
            run_check()
            print(f"\n⏳ 下次检查：{datetime.now().strftime('%H:%M:%S')} + {interval/3600:.1f}小时\n")
            time.sleep(interval)
    except KeyboardInterrupt:
        print(f"\n👋 监控已停止")


def main():
    parser = argparse.ArgumentParser(description='天枢计划 - Star 监控脚本')
    parser.add_argument('--check-only', action='store_true',
                       help='仅执行一次检查，不持续运行')
    parser.add_argument('--interval', type=int, default=14400,
                       help='检查间隔 (秒)，默认 14400 (4 小时)')
    
    args = parser.parse_args()
    
    # 检查依赖
    if not HAS_REQUESTS:
        print("⚠️  警告：requests 库未安装，部分功能受限")
        print("   安装：pip install requests\n")
    
    if args.check_only:
        run_check()
    else:
        run_continuous(args.interval)


if __name__ == '__main__':
    main()

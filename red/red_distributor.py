#!/usr/bin/env python3
"""
天枢计划 - 小红书分发器
与 star_monitor.py 集成，监测到新报告后自动触发分发流程

用法:
    python red_distributor.py --report <报告路径> [--auto-login]
"""

import os
import sys
import json
import time
import argparse
from pathlib import Path
from datetime import datetime

try:
    import requests
    HAS_REQUESTS = True
except ImportError:
    HAS_REQUESTS = False

# 配置
AUTH_DIR = Path(__file__).parent.parent.parent / "auth"
SESSION_FILE = AUTH_DIR / "red_session.json"
RED_DIR = Path(__file__).parent

# 环境变量
FEISHU_WEBHOOK = os.environ.get("FEISHU_WEBHOOK", "")


def load_session() -> dict:
    """加载小红书会话"""
    if not SESSION_FILE.exists():
        return {}
    
    with open(SESSION_FILE, 'r', encoding='utf-8') as f:
        return json.load(f)


def check_session_valid(session: dict) -> bool:
    """检查会话是否有效"""
    if not session:
        return False
    
    # 检查时间 (24 小时内)
    try:
        from datetime import datetime, timedelta
        ts = datetime.fromisoformat(session.get('timestamp', ''))
        if datetime.now() - ts > timedelta(hours=24):
            print(f"⚠️  会话已过期 (超过 24 小时)")
            return False
    except:
        pass
    
    # 检查 Cookies
    cookies = session.get('cookies', [])
    if not cookies:
        return False
    
    # 检查关键 Cookie
    has_session = any(c.get('name') == 'web_session' for c in cookies)
    return has_session


def extract_report_content(report_path: str) -> dict:
    """从技术报告中提取分发内容"""
    with open(report_path, 'r', encoding='utf-8') as f:
        content = f.read()
    
    # 提取关键信息
    import re
    
    data = {
        'title': '',
        'project': '',
        'stars_24h': '',
        'score': '',
        'summary': '',
        'tags': []
    }
    
    # 提取标题
    match = re.search(r'# 技术评测报告：(.+?)\n', content)
    if match:
        data['project'] = match.group(1).strip()
    
    # 提取 24h Stars
    match = re.search(r'\*\*24h Stars\*\* \| (.+?)\n', content)
    if match:
        data['stars_24h'] = match.group(1).strip()
    
    # 提取评分
    match = re.search(r'\*\*综合评分\*\*: (.+?)\n', content)
    if match:
        data['score'] = match.group(1).strip()
    
    # 生成爆款标题
    if data['stars_24h'] and data['project']:
        stars_num = data['stars_24h'].replace(',', '')
        try:
            stars_int = int(stars_num)
            if stars_int >= 1000:
                data['title'] = f"🔥 24h 狂揽{stars_int//1000}k Stars！这个 AI 框架太猛了"
            elif stars_int >= 500:
                data['title'] = f"⚡ 24h 暴涨{stars_int}Stars！开发者都在用"
            else:
                data['title'] = f"⭐ 24h 增长{stars_int}Stars！值得关注的新项目"
        except:
            data['title'] = f"🔥 GitHub 热门：{data['project']}"
    else:
        data['title'] = f"📊 技术评测：{data['project']}"
    
    # 提取总结 (结论部分)
    conclusion = re.search(r'## 🔖 结论\n(.*?)(?=\n---|\*\*评测完成时间|$)', content, re.DOTALL)
    if conclusion:
        data['summary'] = conclusion.group(1).strip()[:500]  # 限制 500 字
    
    # 标签
    data['tags'] = ['#AI', '#Agent', '#GitHub', '#开源', '#技术评测', '#天枢计划']
    
    return data


def send_to_feishu_notification(title: str, content: str) -> bool:
    """发送通知到飞书"""
    if not FEISHU_WEBHOOK:
        print(f"⚠️  FEISHU_WEBHOOK 未配置")
        return False
    
    if not HAS_REQUESTS:
        print(f"⚠️  requests 库未安装")
        return False
    
    message = {
        "msg_type": "text",
        "content": {
            "text": f"📱 小红书分发准备完成\n\n标题：{title}\n\n{content[:200]}...\n\n请手动发布或配置自动发布"
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
        print(f"✅ 飞书通知已发送")
        return True
    except Exception as e:
        print(f"❌ 飞书发送失败：{e}")
        return False


def distribute(report_path: str, auto_login: bool = False) -> bool:
    """执行分发流程"""
    print(f"\n{'='*60}")
    print(f"📱 天枢计划 · 小红书分发器")
    print(f"{'='*60}")
    
    # 1. 检查会话
    print(f"\n1️⃣ 检查登录会话...")
    session = load_session()
    
    if not check_session_valid(session):
        print(f"⚠️  会话无效或不存在")
        
        if auto_login:
            print(f"🔄 启动自动登录流程...")
            from login_helper import login
            login(wait_for_scan=True, timeout=300)
            
            # 重新检查
            session = load_session()
            if not check_session_valid(session):
                print(f"❌ 登录失败，请手动运行 login_helper.py")
                return False
        else:
            print(f"💡 请运行：python login_helper.py")
            print(f"   或使用 --auto-login 启动自动登录")
            return False
    
    print(f"✅ 会话有效 (Cookies: {len(session.get('cookies', []))}个)")
    
    # 2. 提取报告内容
    print(f"\n2️⃣ 提取报告内容...")
    content = extract_report_content(report_path)
    
    print(f"   项目：{content['project']}")
    print(f"   24h Stars: {content['stars_24h']}")
    print(f"   评分：{content['score']}")
    print(f"   标题：{content['title']}")
    
    # 3. 生成封面图 (调用渲染引擎)
    print(f"\n3️⃣ 生成封面图...")
    renderer_script = RED_DIR / "red_renderer.py"
    
    # 创建标题卡片 (无底图时使用)
    import subprocess
    cmd = [
        sys.executable,
        str(renderer_script),
        '--title-only',
        '--title', content['title']
    ]
    
    result = subprocess.run(cmd, capture_output=True, text=True)
    print(result.stdout)
    
    # 提取输出路径
    output_match = result.stdout.find('✅ 标题卡片已创建：')
    if output_match >= 0:
        cover_path = result.stdout[output_match + len('✅ 标题卡片已创建：'):].strip()
        print(f"✅ 封面图：{cover_path}")
    else:
        cover_path = None
        print(f"⚠️  封面图生成失败")
    
    # 4. 准备发布内容
    print(f"\n4️⃣ 准备发布内容...")
    
    post_content = f"""{content['title']}

📊 项目：{content['project']}
⭐ 24h 增长：{content['stars_24h']}
🏆 天枢评分：{content['score']}

{content['summary']}

{' '.join(content['tags'])}

---
天枢计划 | 每日拆解 AI Agent 框架
GitHub: github.com/qq654436/TianShu-Agent-Deep-Dive
"""
    
    print(f"\n📝 发布内容预览:")
    print(f"-" * 60)
    print(post_content[:500])
    print(f"-" * 60)
    
    # 5. 发送飞书通知
    print(f"\n5️⃣ 发送飞书通知...")
    send_to_feishu_notification(content['title'], post_content)
    
    # 6. 保存分发记录
    print(f"\n6️⃣ 保存分发记录...")
    record = {
        'timestamp': datetime.now().isoformat(),
        'report': report_path,
        'project': content['project'],
        'title': content['title'],
        'cover': cover_path,
        'status': 'ready',  # ready / posted / failed
        'content': post_content
    }
    
    record_file = RED_DIR / "distribution_records.json"
    records = []
    if record_file.exists():
        with open(record_file, 'r', encoding='utf-8') as f:
            records = json.load(f)
    
    records.append(record)
    with open(record_file, 'w', encoding='utf-8') as f:
        json.dump(records, f, indent=2, ensure_ascii=False)
    
    print(f"✅ 分发记录已保存")
    
    print(f"\n{'='*60}")
    print(f"✅ 分发准备完成！")
    print(f"\n💡 下一步:")
    print(f"   1. 打开小红书 APP 或网页版")
    print(f"   2. 上传封面图：{cover_path}")
    print(f"   3. 粘贴发布内容 (见飞书消息)")
    print(f"   4. 手动发布")
    print(f"\n⚠️  自动发布功能需要小红书官方 API，当前为半自动流程")
    print(f"{'='*60}\n")
    
    return True


def main():
    parser = argparse.ArgumentParser(description='天枢计划 - 小红书分发器')
    parser.add_argument('--report', type=str, help='技术报告路径')
    parser.add_argument('--auto-login', action='store_true',
                       help='自动启动登录流程')
    parser.add_argument('--check-session', action='store_true',
                       help='仅检查会话状态')
    parser.add_argument('--list-records', action='store_true',
                       help='列出分发记录')
    
    args = parser.parse_args()
    
    if args.check_session:
        session = load_session()
        if check_session_valid(session):
            print(f"✅ 会话有效")
            print(f"   Cookies: {len(session.get('cookies', []))}个")
            print(f"   时间：{session.get('timestamp', '未知')}")
        else:
            print(f"❌ 会话无效或不存在")
            print(f"   请运行：python login_helper.py")
        return
    
    if args.list_records:
        record_file = RED_DIR / "distribution_records.json"
        if record_file.exists():
            with open(record_file, 'r', encoding='utf-8') as f:
                records = json.load(f)
            print(f"\n📋 分发记录 (共{len(records)}条):")
            for r in records[-5:]:  # 显示最近 5 条
                print(f"   {r['timestamp'][:10]} | {r['project']} | {r['status']}")
        else:
            print(f"\nℹ️  无分发记录")
        return
    
    if not args.report:
        print("❌ 请提供 --report 参数")
        print("\n示例:")
        print("  python red_distributor.py --report ../reports/001_superpowers_tech_review.md")
        print("  python red_distributor.py --report <报告> --auto-login")
        return
    
    distribute(args.report, args.auto_login)


if __name__ == '__main__':
    main()

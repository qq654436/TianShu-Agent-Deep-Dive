#!/usr/bin/env python3
"""
天枢计划 - 分发助手
将知乎/即刻文案格式化为干净文本，推送到飞书

用法:
    python distribution_helper.py --file <markdown 文件> --preview

功能:
    1. 解析 Markdown 文件
    2. 移除 Markdown 格式，保留纯文本
    3. 生成飞书卡片消息预览
    4. 可选：直接发送到飞书 (需配置 webhook)
"""

import os
import re
import argparse
from pathlib import Path

try:
    import requests
    HAS_REQUESTS = True
except ImportError:
    HAS_REQUESTS = False

# 环境变量
FEISHU_WEBHOOK = os.environ.get("FEISHU_WEBHOOK", "")


def clean_markdown(content: str) -> str:
    """清理 Markdown 格式，保留纯文本"""
    text = content
    
    # 移除图片
    text = re.sub(r'!\[.*?\]\(.*?\)', '', text)
    
    # 移除链接，保留文本
    text = re.sub(r'\[(.*?)\]\(.*?\)', r'\1', text)
    
    # 移除代码块标记，保留内容
    text = re.sub(r'```\w*\n', '\n', text)
    text = re.sub(r'\n```', '\n', text)
    
    # 移除表格格式
    text = re.sub(r'\n\|.*?\|\n', '\n', text)
    text = re.sub(r'\n\|.*?\|', '', text)
    
    # 简化标题
    text = re.sub(r'^#{1,6}\s+', '', text, flags=re.MULTILINE)
    
    # 移除粗体/斜体标记
    text = re.sub(r'\*\*(.*?)\*\*', r'\1', text)
    text = re.sub(r'\*(.*?)\*', r'\1', text)
    text = re.sub(r'__(.*?)__', r'\1', text)
    
    # 移除引用标记
    text = re.sub(r'^>\s*', '', text, flags=re.MULTILINE)
    
    # 移除列表标记
    text = re.sub(r'^[\-\*\+]\s+', '', text, flags=re.MULTILINE)
    text = re.sub(r'^\d+\.\s+', '', text, flags=re.MULTILINE)
    
    # 移除多余空行
    text = re.sub(r'\n{3,}', '\n\n', text)
    
    # 移除水平线
    text = re.sub(r'\n---+\n', '\n', text)
    text = re.sub(r'\n\*\*\*+\n', '\n', text)
    
    # 移除标签
    text = re.sub(r'^#.*$', '', text, flags=re.MULTILINE)
    
    return text.strip()


def extract_title(content: str) -> str:
    """提取标题"""
    # 查找第一个标题
    match = re.search(r'^#\s+(.+?)$', content, re.MULTILINE)
    if match:
        return match.group(1).strip()
    return "天枢计划·内容分发"


def extract_metadata(content: str) -> dict:
    """提取元数据"""
    meta = {
        'project': '',
        'stars_24h': '',
        'score': '',
        'platform': ''
    }
    
    # 项目名称
    match = re.search(r'深度拆解 \| (.+?)：', content)
    if match:
        meta['project'] = match.group(1).strip()
    
    # 24h Stars
    match = re.search(r'\*\*24h Stars\*\*:?\s*(.+?)\n', content)
    if match:
        meta['stars_24h'] = match.group(1).strip()
    
    # 评分
    match = re.search(r'\*\*综合评分\*\*:?\s*(.+?)\n', content)
    if match:
        meta['score'] = match.group(1).strip()
    
    # 平台判断
    if '即刻' in content or 'jike' in content.lower():
        meta['platform'] = '即刻'
    elif '知乎' in content or 'zhihu' in content.lower():
        meta['platform'] = '知乎'
    else:
        meta['platform'] = '未知'
    
    return meta


def send_to_feishu(title: str, content: str, preview: bool = False) -> bool:
    """发送到飞书"""
    if not FEISHU_WEBHOOK:
        print(f"⚠️  FEISHU_WEBHOOK 未配置，仅显示预览")
        return False
    
    if not HAS_REQUESTS:
        print(f"⚠️  requests 库未安装，无法发送")
        return False
    
    # 截断内容以适应飞书限制
    truncated_content = content[:2000] + "..." if len(content) > 2000 else content
    
    message = {
        "msg_type": "interactive",
        "card": {
            "header": {
                "title": {
                    "tag": "plain_text",
                    "content": f"📝 天枢计划·内容分发 - {title}"
                },
                "template": "blue"
            },
            "elements": [
                {
                    "tag": "div",
                    "text": {
                        "tag": "lark_md",
                        "content": f"**平台**: {meta['platform']}\n**项目**: {meta['project']}\n**24h Stars**: {meta['stars_24h']}\n**评分**: {meta['score']}\n\n---\n\n**点击下方按钮复制全文** 👇"
                    }
                },
                {
                    "tag": "action",
                    "actions": [
                        {
                            "tag": "button",
                            "text": {
                                "tag": "lark_md",
                                "content": "📋 复制全文"
                            },
                            "url": "data:text/plain," + requests.utils.quote(content),
                            "type": "primary"
                        },
                        {
                            "tag": "button",
                            "text": {
                                "tag": "lark_md",
                                "content": "🔗 知乎"
                            },
                            "url": "https://zhuanlan.zhihu.com/",
                            "type": "default"
                        },
                        {
                            "tag": "button",
                            "text": {
                                "tag": "lark_md",
                                "content": "📱 即刻"
                            },
                            "url": "https://web.okjike.com/",
                            "type": "default"
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
        print(f"✅ 飞书消息已发送")
        return True
    except Exception as e:
        print(f"❌ 飞书发送失败：{e}")
        return False


def main():
    parser = argparse.ArgumentParser(description='天枢计划 - 分发助手')
    parser.add_argument('--file', type=str, required=True,
                       help='Markdown 文件路径')
    parser.add_argument('--preview', action='store_true',
                       help='仅预览，不发送')
    parser.add_argument('--send', action='store_true',
                       help='发送到飞书')
    
    args = parser.parse_args()
    
    # 读取文件
    file_path = Path(args.file)
    if not file_path.exists():
        print(f"❌ 文件不存在：{file_path}")
        return
    
    with open(file_path, 'r', encoding='utf-8') as f:
        content = f.read()
    
    # 提取信息
    global meta
    meta = extract_metadata(content)
    title = extract_title(content)
    clean_text = clean_markdown(content)
    
    print(f"\n{'='*60}")
    print(f"📝 天枢计划·内容分发")
    print(f"{'='*60}")
    print(f"文件：{file_path.name}")
    print(f"平台：{meta['platform']}")
    print(f"项目：{meta['project']}")
    print(f"24h Stars: {meta['stars_24h']}")
    print(f"评分：{meta['score']}")
    print(f"{'='*60}\n")
    
    # 预览
    print("📄 清理后的文本预览 (前 500 字):")
    print("-" * 60)
    print(clean_text[:500] + "..." if len(clean_text) > 500 else clean_text)
    print("-" * 60)
    print(f"\n全文长度：{len(clean_text)} 字符\n")
    
    # 发送
    if args.send:
        print("🚀 发送到飞书...")
        send_to_feishu(title, clean_text)
    elif args.preview:
        print("ℹ️  预览模式，未发送")
    else:
        print("💡 使用 --send 发送到飞书，或使用 --preview 仅预览")
    
    # 输出到文件
    output_file = file_path.parent / f"{file_path.stem}_clean.txt"
    with open(output_file, 'w', encoding='utf-8') as f:
        f.write(clean_text)
    print(f"\n✅ 清理后的文本已保存：{output_file}")


if __name__ == '__main__':
    main()

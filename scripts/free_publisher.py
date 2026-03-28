#!/usr/bin/env python3
"""
天枢计划 - 社交媒体发布器 (免费 API 版本)
支持：Twitter/Reddit/微博/知乎/掘金/V2EX/飞书

无需官方 API Key，使用免费抓取方案
"""

import os
import json
import time
from pathlib import Path
from datetime import datetime

# 尝试导入依赖
try:
    import requests
    HAS_REQUESTS = True
except ImportError:
    HAS_REQUESTS = False

try:
    from selenium import webdriver
    from selenium.webdriver.common.by import By
    from selenium.webdriver.common.keys import Keys
    HAS_SELENIUM = True
except ImportError:
    HAS_SELENIUM = False

# 工作目录
WORKSPACE = Path(__file__).parent.parent
DISTRIBUTION_DIR = WORKSPACE / "tian_shu" / "distribution"
LOGS_DIR = WORKSPACE / "tian_shu" / "logs"

# 确保目录存在
LOGS_DIR.mkdir(exist_ok=True)

# 发布记录
RECORDS_FILE = WORKSPACE / "tian_shu" / "distribution_records.json"


class DistributionRecorder:
    """发布记录管理"""
    
    def __init__(self):
        self.records_file = RECORDS_FILE
        self.records = self.load()
    
    def load(self):
        if self.records_file.exists():
            with open(self.records_file, 'r', encoding='utf-8') as f:
                return json.load(f)
        return {"records": []}
    
    def add(self, prey_id, platform, status, preview="", error=""):
        record = {
            "timestamp": datetime.now().isoformat(),
            "prey_id": prey_id,
            "platform": platform,
            "status": status,
            "content_preview": preview[:200],
            "error": error
        }
        self.records["records"].append(record)
        self.save()
        return record
    
    def save(self):
        with open(self.recorder_file, 'w', encoding='utf-8') as f:
            json.dump(self.records, f, ensure_ascii=False, indent=2)


class FreePublisher:
    """免费社交媒体发布器"""
    
    def __init__(self):
        self.recorder = DistributionRecorder()
        self.session = requests.Session() if HAS_REQUESTS else None
        
        # Cookie 配置 (从环境变量读取)
        self.weibo_cookie = os.environ.get("WEIBO_COOKIE", "")
        self.zhihu_cookie = os.environ.get("ZHIHU_COOKIE", "")
        self.juejin_token = os.environ.get("JUEJIN_TOKEN", "")
        self.v2ex_cookie = os.environ.get("V2EX_COOKIE", "")
    
    def publish_to_feishu(self, prey_id, content):
        """飞书发布 (通过 OpenClaw message tool)"""
        print(f"📤 发布到飞书：{prey_id}")
        
        # 写入待发送队列
        message_file = WORKSPACE / ".pending_messages.json"
        messages = []
        
        if message_file.exists():
            try:
                messages = json.loads(message_file.read_text())
            except:
                messages = []
        
        messages.append({
            "timestamp": datetime.now().isoformat(),
            "channel": "feishu",
            "text": content[:2000]  # 限制长度
        })
        
        message_file.write_text(json.dumps(messages, ensure_ascii=False, indent=2))
        
        self.recorder.add(prey_id, "feishu", "success", content[:200])
        print(f"✅ 飞书发布成功")
        return True
    
    def publish_to_juejin(self, prey_id, title, content):
        """掘金发布 (需要 Cookie)"""
        print(f"📤 发布到掘金：{prey_id}")
        
        if not self.juejin_token:
            print("⚠️  缺少掘金 Cookie，跳过")
            self.recorder.add(prey_id, "juejin", "skipped", "", "缺少 Cookie")
            return False
        
        # 掘金发布 API (需要验证)
        url = "https://api.juejin.cn/content_api/v1/content/article/create"
        headers = {
            "Cookie": f"token={self.juejin_token}",
            "Content-Type": "application/json"
        }
        
        data = {
            "title": title,
            "content": content,
            "brief_content": content[:500],
            "category_id": "6809637767543234574",  # 前端
            "tags": ["AI", "Agent", "GitHub"],
            "html_content": content
        }
        
        try:
            response = self.session.post(url, json=data, headers=headers)
            if response.status_code == 200:
                self.recorder.add(prey_id, "juejin", "success", title)
                print(f"✅ 掘金发布成功")
                return True
            else:
                error = f"HTTP {response.status_code}"
                self.recorder.add(prey_id, "juejin", "failed", title, error)
                print(f"❌ 掘金发布失败：{error}")
                return False
        except Exception as e:
            self.recorder.add(prey_id, "juejin", "failed", title, str(e))
            print(f"❌ 掘金发布失败：{e}")
            return False
    
    def publish_to_v2ex(self, prey_id, title, content):
        """V2EX 发布 (需要 Cookie + 浏览器)"""
        print(f"📤 发布到 V2EX: {prey_id}")
        
        if not HAS_SELENIUM:
            print("⚠️  Selenium 未安装，跳过")
            self.recorder.add(prey_id, "v2ex", "skipped", "", "缺少 Selenium")
            return False
        
        if not self.v2ex_cookie:
            print("⚠️  缺少 V2EX Cookie，跳过")
            self.recorder.add(prey_id, "v2ex", "skipped", "", "缺少 Cookie")
            return False
        
        # TODO: 实现浏览器自动化发布
        print("⚠️  V2EX 发布功能待实现")
        self.recorder.add(prey_id, "v2ex", "pending", title, "功能待实现")
        return False
    
    def publish_to_weibo(self, prey_id, content):
        """微博发布 (需要 Cookie + 浏览器)"""
        print(f"📤 发布到微博：{prey_id}")
        
        if not HAS_SELENIUM:
            print("⚠️  Selenium 未安装，跳过")
            self.recorder.add(prey_id, "weibo", "skipped", "", "缺少 Selenium")
            return False
        
        if not self.weibo_cookie:
            print("⚠️  缺少微博 Cookie，跳过")
            self.recorder.add(prey_id, "weibo", "skipped", "", "缺少 Cookie")
            return False
        
        # TODO: 实现浏览器自动化发布
        print("⚠️  微博发布功能待实现")
        self.recorder.add(prey_id, "weibo", "pending", content[:100], "功能待实现")
        return False
    
    def publish_to_zhihu(self, prey_id, title, content):
        """知乎发布 (需要 Cookie + 浏览器)"""
        print(f"📤 发布到知乎：{prey_id}")
        
        if not HAS_SELENIUM:
            print("⚠️  Selenium 未安装，跳过")
            self.recorder.add(prey_id, "zhihu", "skipped", "", "缺少 Selenium")
            return False
        
        if not self.zhihu_cookie:
            print("⚠️  缺少知乎 Cookie，跳过")
            self.recorder.add(prey_id, "zhihu", "skipped", "", "缺少 Cookie")
            return False
        
        # TODO: 实现浏览器自动化发布
        print("⚠️  知乎发布功能待实现")
        self.recorder.add(prey_id, "zhihu", "pending", title, "功能待实现")
        return False
    
    def publish_all(self, prey_id, content_file):
        """发布到所有已配置平台"""
        print(f"\n🚀 开始发布猎物 #{prey_id}")
        print("=" * 50)
        
        # 读取内容
        if not content_file.exists():
            print(f"❌ 内容文件不存在：{content_file}")
            return False
        
        content = content_file.read_text(encoding='utf-8')
        
        # 解析内容 (简单处理)
        twitter_section = content.split("## 📱 Twitter")[1].split("##")[0] if "## 📱 Twitter" in content else ""
        weibo_section = content.split("## 📝 微博/知乎")[1].split("##")[0] if "## 📝 微博/知乎" in content else ""
        
        # 提取标题和内容
        title_match = weibo_section.find("**标题**")
        content_match = weibo_section.find("**正文**")
        
        title = ""
        weibo_content = ""
        
        if title_match != -1 and content_match != -1:
            title_section = weibo_section[title_match:content_match]
            title_start = title_section.find('```')
            if title_start != -1:
                title_end = title_section.find('```', title_start + 3)
                if title_end != -1:
                    title = title_section[title_start+3:title_end].strip()
        
        if content_match != -1:
            content_section = weibo_section[content_match:]
            content_start = content_section.find('```')
            if content_start != -1:
                content_end = content_section.find('```', content_start + 3)
                if content_end != -1:
                    weibo_content = content_section[content_start+3:content_end].strip()
        
        # 发布到各平台
        results = {}
        
        # 1. 飞书 (总是可用)
        results["feishu"] = self.publish_to_feishu(prey_id, weibo_content[:1000])
        
        # 2. 掘金 (需要 Cookie)
        if self.juejin_token:
            results["juejin"] = self.publish_to_juejin(prey_id, title, weibo_content)
        
        # 3. 微博 (需要 Cookie + Selenium)
        if self.weibo_cookie and HAS_SELENIUM:
            results["weibo"] = self.publish_to_weibo(prey_id, weibo_content)
        
        # 4. 知乎 (需要 Cookie + Selenium)
        if self.zhihu_cookie and HAS_SELENIUM:
            results["zhihu"] = self.publish_to_zhihu(prey_id, title, weibo_content)
        
        # 5. V2EX (需要 Cookie + Selenium)
        if self.v2ex_cookie and HAS_SELENIUM:
            results["v2ex"] = self.publish_to_v2ex(prey_id, title, weibo_content)
        
        # 输出结果
        print("\n" + "=" * 50)
        print("📊 发布结果汇总")
        print("=" * 50)
        
        for platform, success in results.items():
            status = "✅" if success else "❌"
            print(f"{status} {platform}: {'成功' if success else '失败/跳过'}")
        
        return all(results.values())


def main():
    """CLI 入口"""
    import sys
    
    if len(sys.argv) < 2:
        print("用法：python free_publisher.py <prey_id> [content_file]")
        print("示例：python free_publisher.py 012")
        sys.exit(1)
    
    prey_id = sys.argv[1]
    
    if len(sys.argv) > 2:
        content_file = Path(sys.argv[2])
    else:
        content_file = DISTRIBUTION_DIR / f"prey_{prey_id}_ready_to_post.md"
    
    publisher = FreePublisher()
    success = publisher.publish_all(prey_id, content_file)
    
    sys.exit(0 if success else 1)


if __name__ == "__main__":
    main()

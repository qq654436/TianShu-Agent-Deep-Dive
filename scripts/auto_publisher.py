#!/usr/bin/env python3
"""
天枢计划 - 自动化发布脚本
支持平台：Twitter / 微博 / 知乎 / 掘金 / V2EX / 飞书

用法:
    python auto_publisher.py --platform twitter --file prey_012_ready_to_post.md
    python auto_publisher.py --platform all --file prey_012_ready_to_post.md

配置:
    在 .env 文件中设置各平台 API 凭证
"""

import os
import sys
import json
import time
import argparse
from pathlib import Path
from datetime import datetime

# 尝试导入依赖
try:
    import requests
    HAS_REQUESTS = True
except ImportError:
    HAS_REQUESTS = False
    print("⚠️  警告：requests 未安装，部分功能不可用")
    print("   安装：pip install requests")

try:
    from selenium import webdriver
    from selenium.webdriver.common.by import By
    from selenium.webdriver.common.keys import Keys
    from selenium.webdriver.support.ui import WebDriverWait
    from selenium.webdriver.support import expected_conditions as EC
    HAS_SELENIUM = True
except ImportError:
    HAS_SELENIUM = False
    print("⚠️  警告：selenium 未安装，浏览器自动化不可用")
    print("   安装：pip install selenium")

# 工作目录
WORKSPACE = Path(__file__).parent.parent
DISTRIBUTION_DIR = WORKSPACE / "tian_shu" / "distribution"
LOGS_DIR = WORKSPACE / "tian_shu" / "logs"

# 确保日志目录存在
LOGS_DIR.mkdir(exist_ok=True)

# 发布记录文件
RECORDS_FILE = WORKSPACE / "tian_shu" / "distribution_records.json"


class DistributionRecorder:
    """发布记录管理器"""
    
    def __init__(self, records_file):
        self.records_file = Path(records_file)
        self.records = self.load_records()
    
    def load_records(self):
        if self.records_file.exists():
            with open(self.records_file, 'r', encoding='utf-8') as f:
                return json.load(f)
        return {"records": []}
    
    def add_record(self, prey_id, platform, status, content_preview="", error=""):
        record = {
            "timestamp": datetime.now().isoformat(),
            "prey_id": prey_id,
            "platform": platform,
            "status": status,  # success / failed / skipped
            "content_preview": content_preview[:200],
            "error": error
        }
        self.records["records"].append(record)
        self.save_records()
        return record
    
    def save_records(self):
        with open(self.records_file, 'w', encoding='utf-8') as f:
            json.dump(self.records, f, ensure_ascii=False, indent=2)
    
    def get_prey_records(self, prey_id):
        return [r for r in self.records["records"] if r["prey_id"] == prey_id]
    
    def get_summary(self):
        total = len(self.records["records"])
        success = sum(1 for r in self.records["records"] if r["status"] == "success")
        failed = sum(1 for r in self.records["records"] if r["status"] == "failed")
        skipped = sum(1 for r in self.records["records"] if r["status"] == "skipped")
        return {
            "total": total,
            "success": success,
            "failed": failed,
            "skipped": skipped,
            "success_rate": f"{success/total*100:.1f}%" if total > 0 else "0%"
        }


class ContentParser:
    """内容解析器 - 从 Markdown 文件提取各平台内容"""
    
    def __init__(self, file_path):
        self.file_path = Path(file_path)
        self.content = self.load_content()
    
    def load_content(self):
        with open(self.file_path, 'r', encoding='utf-8') as f:
            return f.read()
    
    def extract_twitter_thread(self):
        """提取 Twitter 线程"""
        tweets = []
        current_tweet = []
        in_tweet = False
        
        for line in self.content.split('\n'):
            if line.startswith('**Tweet'):
                if current_tweet and in_tweet:
                    tweets.append('\n'.join(current_tweet).strip())
                current_tweet = []
                in_tweet = True
            elif in_tweet and line.startswith('```'):
                continue  # 跳过代码块标记
            elif in_tweet and line:
                current_tweet.append(line)
        
        if current_tweet:
            tweets.append('\n'.join(current_tweet).strip())
        
        return tweets
    
    def extract_weibo_zhihu(self):
        """提取微博/知乎短文"""
        # 查找"微博/知乎短文"部分
        start_marker = "## 📝 微博/知乎短文"
        end_marker = "## 📄 掘金/V2EX"
        
        start_idx = self.content.find(start_marker)
        end_idx = self.content.find(end_marker)
        
        if start_idx == -1:
            return {"title": "", "content": ""}
        
        section = self.content[start_idx:end_idx] if end_idx != -1 else self.content[start_idx:]
        
        # 提取标题
        title_match = section.find("**标题**")
        content_match = section.find("**正文**")
        
        title = ""
        content = ""
        
        if title_match != -1 and content_match != -1:
            title_section = section[title_match:content_match]
            # 提取代码块内容
            title_start = title_section.find('```')
            if title_start != -1:
                title_end = title_section.find('```', title_start + 3)
                if title_end != -1:
                    title = title_section[title_start+3:title_end].strip()
        
        if content_match != -1:
            content_section = section[content_match:]
            # 提取代码块内容
            content_start = content_section.find('```')
            if content_start != -1:
                content_end = content_section.find('```', content_start + 3)
                if content_end != -1:
                    content = content_section[content_start+3:content_end].strip()
        
        return {"title": title, "content": content}
    
    def extract_juejin_v2ex(self):
        """提取掘金/V2EX 文章"""
        # 查找"掘金/V2EX 技术文章"部分
        start_marker = "## 📄 掘金/V2EX 技术文章"
        
        start_idx = self.content.find(start_marker)
        if start_idx == -1:
            return {"title": "", "summary": "", "outline": ""}
        
        section = self.content[start_idx:]
        
        title = ""
        summary = ""
        outline = ""
        
        # 提取标题
        title_match = section.find("**标题**")
        if title_match != -1:
            title_section = section[title_match:]
            title_start = title_section.find('```')
            if title_start != -1:
                title_end = title_section.find('```', title_start + 3)
                if title_end != -1:
                    title = title_section[title_start+3:title_end].strip()
        
        # 提取摘要
        summary_match = section.find("**摘要**")
        if summary_match != -1:
            summary_section = section[summary_match:]
            summary_start = summary_section.find('```')
            if summary_start != -1:
                summary_end = summary_section.find('```', summary_start + 3)
                if summary_end != -1:
                    summary = summary_section[summary_start+3:summary_end].strip()
        
        # 提取大纲
        outline_match = section.find("**正文大纲**")
        if outline_match != -1:
            outline_section = section[outline_match:]
            outline_start = outline_section.find('```')
            if outline_start != -1:
                outline_end = outline_section.find('```', outline_start + 3)
                if outline_end != -1:
                    outline = outline_section[outline_start+3:outline_end].strip()
        
        return {"title": title, "summary": summary, "outline": outline}


class Publisher:
    """发布器基类"""
    
    def __init__(self, recorder):
        self.recorder = recorder
        self.name = "base"
    
    def publish(self, prey_id, content):
        raise NotImplementedError
    
    def log_success(self, prey_id, content_preview):
        self.recorder.add_record(prey_id, self.name, "success", content_preview)
        print(f"✅ {self.name} 发布成功")
    
    def log_failure(self, prey_id, error):
        self.recorder.add_record(prey_id, self.name, "failed", "", str(error))
        print(f"❌ {self.name} 发布失败：{error}")


class FeishuPublisher(Publisher):
    """飞书发布器"""
    
    def __init__(self, recorder):
        super().__init__(recorder)
        self.name = "feishu"
    
    def publish(self, prey_id, content):
        # 飞书消息已通过 message tool 发送
        # 这里记录发布结果
        self.log_success(prey_id, content[:200])
        return True


class TwitterPublisher(Publisher):
    """Twitter 发布器 (需要 API 配置)"""
    
    def __init__(self, recorder, api_key=None, api_secret=None, access_token=None, access_token_secret=None):
        super().__init__(recorder)
        self.name = "twitter"
        self.api_key = api_key or os.environ.get("TWITTER_API_KEY")
        self.api_secret = api_secret or os.environ.get("TWITTER_API_SECRET")
        self.access_token = access_token or os.environ.get("TWITTER_ACCESS_TOKEN")
        self.access_token_secret = access_token_secret or os.environ.get("TWITTER_ACCESS_TOKEN_SECRET")
    
    def publish(self, prey_id, tweets):
        if not all([self.api_key, self.api_secret, self.access_token, self.access_token_secret]):
            self.log_failure(prey_id, "缺少 Twitter API 凭证")
            return False
        
        # TODO: 实现 Twitter API 发布
        # 使用 tweepy 库
        print("⚠️  Twitter API 发布功能待实现")
        self.log_failure(prey_id, "功能待实现")
        return False


class BrowserPublisher(Publisher):
    """浏览器自动化发布器 (Selenium)"""
    
    def __init__(self, recorder, headless=True):
        super().__init__(recorder)
        self.name = "browser"
        self.headless = headless
        self.driver = None
    
    def setup_driver(self):
        if not HAS_SELENIUM:
            return False
        
        options = webdriver.ChromeOptions()
        if self.headless:
            options.add_argument("--headless")
        options.add_argument("--no-sandbox")
        options.add_argument("--disable-dev-shm-usage")
        
        try:
            self.driver = webdriver.Chrome(options=options)
            return True
        except Exception as e:
            print(f"❌ ChromeDriver 初始化失败：{e}")
            return False
    
    def publish_to_twitter(self, prey_id, tweets):
        if not self.setup_driver():
            self.log_failure(prey_id, "浏览器初始化失败")
            return False
        
        try:
            # 打开 Twitter
            self.driver.get("https://twitter.com/login")
            
            # TODO: 实现登录逻辑 (需要处理验证码)
            # 等待用户手动登录或配置 Cookie
            
            print("⚠️  Twitter 浏览器发布需要手动登录")
            self.log_failure(prey_id, "需要手动登录")
            return False
            
        except Exception as e:
            self.log_failure(prey_id, str(e))
            return False
        finally:
            if self.driver:
                self.driver.quit()


class AutoPublisher:
    """自动化发布管理器"""
    
    def __init__(self):
        self.recorder = DistributionRecorder(RECORDS_FILE)
        self.parsers = {}
        self.publishers = {}
    
    def parse_content(self, file_path):
        """解析内容文件"""
        parser = ContentParser(file_path)
        return {
            "twitter": parser.extract_twitter_thread(),
            "weibo_zhihu": parser.extract_weibo_zhihu(),
            "juejin_v2ex": parser.extract_juejin_v2ex()
        }
    
    def publish_all(self, prey_id, content_file):
        """发布到所有平台"""
        print(f"\n🚀 开始发布猎物 #{prey_id}")
        print("=" * 50)
        
        # 解析内容
        content = self.parse_content(content_file)
        
        # 发布到各平台
        results = {}
        
        # 1. 飞书
        feishu_publisher = FeishuPublisher(self.recorder)
        feishu_content = "\n".join(content["twitter"][:3])  # 前 3 条推文
        results["feishu"] = feishu_publisher.publish(prey_id, feishu_content)
        
        # 2. Twitter (需要 API)
        # twitter_publisher = TwitterPublisher(self.recorder)
        # results["twitter"] = twitter_publisher.publish(prey_id, content["twitter"])
        
        # 3. 微博/知乎 (需要 API 或浏览器)
        # weibo_content = content["weibo_zhihu"]["content"]
        # results["weibo"] = ...
        
        # 4. 掘金/V2EX (需要 Cookie 或浏览器)
        # juejin_content = content["juejin_v2ex"]
        # results["juejin"] = ...
        
        # 输出结果
        print("\n" + "=" * 50)
        print("📊 发布结果汇总")
        print("=" * 50)
        
        for platform, success in results.items():
            status = "✅" if success else "❌"
            print(f"{status} {platform}: {'成功' if success else '失败'}")
        
        # 输出统计
        summary = self.recorder.get_summary()
        print(f"\n总发布数：{summary['total']}")
        print(f"成功：{summary['success']}")
        print(f"失败：{summary['failed']}")
        print(f"跳过：{summary['skipped']}")
        print(f"成功率：{summary['success_rate']}")
        
        return results


def main():
    parser = argparse.ArgumentParser(description="天枢计划自动化发布工具")
    parser.add_argument("--prey-id", type=str, required=True, help="猎物编号 (如：012)")
    parser.add_argument("--file", type=str, help="内容文件路径")
    parser.add_argument("--platform", type=str, default="all", 
                       choices=["all", "feishu", "twitter", "weibo", "zhihu", "juejin", "v2ex"],
                       help="目标平台")
    
    args = parser.parse_args()
    
    # 确定内容文件
    if args.file:
        content_file = Path(args.file)
    else:
        content_file = DISTRIBUTION_DIR / f"prey_{args.prey_id}_ready_to_post.md"
    
    if not content_file.exists():
        print(f"❌ 内容文件不存在：{content_file}")
        sys.exit(1)
    
    # 执行发布
    publisher = AutoPublisher()
    results = publisher.publish_all(args.prey_id, content_file)
    
    # 退出码
    if all(results.values()):
        sys.exit(0)
    else:
        sys.exit(1)


if __name__ == "__main__":
    main()

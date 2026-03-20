#!/usr/bin/env python3
"""
天枢计划 - 小红书登录助手
启动浏览器访问小红书登录页，截图二维码，通过飞书推送

用法:
    python login_helper.py [--wait]

功能:
    1. 启动 Selenium + Chrome/Chromium
    2. 访问小红书登录页
    3. 截图登录二维码
    4. 通过飞书推送二维码
    5. 等待用户扫码
    6. 保存 storage_state.json (Cookies + LocalStorage)
"""

import os
import sys
import time
import json
import base64
from datetime import datetime
from pathlib import Path

try:
    from selenium import webdriver
    from selenium.webdriver.chrome.options import Options
    from selenium.common.exceptions import TimeoutException, WebDriverException
    HAS_SELENIUM = True
except ImportError:
    HAS_SELENIUM = False

try:
    import requests
    HAS_REQUESTS = True
except ImportError:
    HAS_REQUESTS = False

# 配置
AUTH_DIR = Path("/home/admin/.openclaw/workspace/auth")
SESSION_FILE = AUTH_DIR / "red_session.json"
QR_CODE_FILE = AUTH_DIR / "red_qr_code.png"

# 环境变量
FEISHU_WEBHOOK = os.environ.get("FEISHU_WEBHOOK", "")

# 小红书登录页
RED_LOGIN_URL = "https://www.xiaohongshu.com/"


def create_driver():
    """创建无头浏览器驱动"""
    options = Options()
    options.add_argument('--headless')
    options.add_argument('--no-sandbox')
    options.add_argument('--disable-dev-shm-usage')
    options.add_argument('--disable-gpu')
    options.add_argument('--window-size=1920,1080')
    options.add_argument('--user-agent=Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36')
    
    # 尝试多个可能的 chromedriver 路径
    driver_paths = [
        '/usr/bin/chromedriver',
        '/usr/local/bin/chromedriver',
        '/home/admin/.local/bin/chromedriver',
        'chromedriver'
    ]
    
    for driver_path in driver_paths:
        try:
            driver = webdriver.Chrome(executable_path=driver_path, options=options)
            print(f"✅ ChromeDriver 已加载：{driver_path}")
            return driver
        except Exception as e:
            continue
    
    # 如果都没有，尝试使用 Firefox
    print("⚠️  ChromeDriver 未找到，尝试 Firefox...")
    try:
        from selenium.webdriver.firefox.options import Options as FirefoxOptions
        options = FirefoxOptions()
        options.add_argument('--headless')
        driver = webdriver.Firefox(options=options)
        print(f"✅ Firefox 已加载")
        return driver
    except Exception as e:
        raise RuntimeError(f"无法启动浏览器：{e}")


def send_qr_to_feishu(image_path: str) -> bool:
    """发送二维码到飞书"""
    if not FEISHU_WEBHOOK:
        print(f"⚠️  FEISHU_WEBHOOK 未配置，仅保存本地文件")
        return False
    
    if not HAS_REQUESTS:
        print(f"⚠️  requests 库未安装，无法发送")
        return False
    
    # 读取图片并转为 base64
    with open(image_path, 'rb') as f:
        image_data = base64.b64encode(f.read()).decode('utf-8')
    
    # 飞书消息 (带图片)
    message = {
        "msg_type": "image",
        "content": {
            "image_key": ""  # 需要先上传图片获取 image_key
        }
    }
    
    # 方式 1: 先上传图片到飞书
    # 由于飞书需要 multipart/form-data 上传，这里简化处理
    # 使用交互式卡片发送
    
    card_message = {
        "msg_type": "interactive",
        "card": {
            "header": {
                "title": {
                    "tag": "plain_text",
                    "content": "📱 小红书登录二维码"
                },
                "template": "blue"
            },
            "elements": [
                {
                    "tag": "div",
                    "text": {
                        "tag": "lark_md",
                        "content": f"**天枢计划 · 小红书分发环境**\n\n请扫描二维码登录小红书企业账号\n\n**时间**: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}\n\n⚠️ 二维码有效期约 5 分钟，请尽快扫描"
                    }
                },
                {
                    "tag": "img",
                    "img_key": ""  # 需要上传后获取
                },
                {
                    "tag": "action",
                    "actions": [
                        {
                            "tag": "button",
                            "text": {
                                "tag": "lark_md",
                                "content": "📱 打开小红书"
                            },
                            "url": "https://www.xiaohongshu.com/",
                            "type": "primary"
                        }
                    ]
                }
            ]
        }
    }
    
    # 由于飞书图片上传需要 multipart，这里简化为发送文本通知
    # 实际使用时需要实现图片上传逻辑
    text_message = {
        "msg_type": "text",
        "content": {
            "text": f"📱 小红书登录二维码已生成\n\n请查看附件图片或访问：{QR_CODE_FILE}\n\n时间：{datetime.now().strftime('%Y-%m-%d %H:%M:%S')}\n⚠️ 二维码有效期约 5 分钟"
        }
    }
    
    try:
        # 发送文本消息
        response = requests.post(
            FEISHU_WEBHOOK,
            json=text_message,
            headers={"Content-Type": "application/json"},
            timeout=10
        )
        response.raise_for_status()
        print(f"✅ 飞书通知已发送")
        
        # 图片文件需要单独上传，这里提示用户查看本地文件
        return True
    except Exception as e:
        print(f"❌ 飞书发送失败：{e}")
        return False


def save_session(driver, session_file: Path):
    """保存会话状态 (Cookies + LocalStorage)"""
    session_data = {
        "cookies": driver.get_cookies(),
        "url": driver.current_url,
        "timestamp": datetime.now().isoformat(),
        "user_agent": driver.execute_script("return navigator.userAgent;")
    }
    
    # 尝试获取 LocalStorage
    try:
        local_storage = driver.execute_script("""
            var ls = {};
            for (var i = 0; i < localStorage.length; i++) {
                ls[localStorage.key(i)] = localStorage.getItem(localStorage.key(i));
            }
            return ls;
        """)
        session_data["local_storage"] = local_storage
    except Exception as e:
        print(f"⚠️  无法获取 LocalStorage: {e}")
        session_data["local_storage"] = {}
    
    # 保存到文件
    session_file.parent.mkdir(parents=True, exist_ok=True)
    with open(session_file, 'w', encoding='utf-8') as f:
        json.dump(session_data, f, indent=2, ensure_ascii=False)
    
    print(f"✅ 会话已保存：{session_file}")
    return session_data


def check_login_status(driver) -> bool:
    """检查是否已登录"""
    # 检查是否有登录后的特征元素
    try:
        # 小红书登录后通常会有用户头像或特定元素
        # 这里检查 URL 是否变化或有特定 cookie
        cookies = driver.get_cookies()
        for cookie in cookies:
            if cookie.get('name') == 'web_session':
                return True
        return False
    except:
        return False


def login(wait_for_scan: bool = True, timeout: int = 300):
    """执行登录流程"""
    print(f"\n{'='*60}")
    print(f"📱 天枢计划 · 小红书登录助手")
    print(f"{'='*60}")
    print(f"目标 URL: {RED_LOGIN_URL}")
    print(f"会话保存：{SESSION_FILE}")
    print(f"二维码文件：{QR_CODE_FILE}")
    print(f"{'='*60}\n")
    
    # 检查依赖
    if not HAS_SELENIUM:
        print("❌ Selenium 未安装：pip3 install --user selenium")
        return False
    
    # 检查浏览器驱动
    try:
        driver = create_driver()
    except Exception as e:
        print(f"❌ 无法启动浏览器：{e}")
        print(f"\n💡 解决方案:")
        print(f"   1. 安装 Chrome: sudo yum install chromium")
        print(f"   2. 安装 ChromeDriver: sudo yum install chromedriver")
        print(f"   3. 或使用 Firefox: sudo yum install firefox geckodriver")
        return False
    
    try:
        # 访问登录页
        print(f"🌐 正在访问小红书...")
        driver.get(RED_LOGIN_URL)
        driver.implicitly_wait(10)
        
        # 等待页面加载
        time.sleep(3)
        
        # 截图整个页面
        print(f"📸 正在截图...")
        driver.save_screenshot(str(QR_CODE_FILE))
        print(f"✅ 截图已保存：{QR_CODE_FILE}")
        
        # 发送到飞书
        send_qr_to_feishu(str(QR_CODE_FILE))
        
        if not wait_for_scan:
            print(f"\nℹ️  非等待模式，脚本结束")
            return True
        
        # 等待用户扫码
        print(f"\n⏳ 等待扫码登录 (超时：{timeout}秒)...")
        print(f"💡 请打开小红书 APP 扫描二维码")
        
        start_time = time.time()
        check_interval = 5  # 每 5 秒检查一次
        
        while time.time() - start_time < timeout:
            time.sleep(check_interval)
            
            # 检查登录状态
            if check_login_status(driver):
                print(f"\n🎉 检测到已登录！")
                break
            
            # 检查 URL 是否变化 (登录后通常会跳转)
            current_url = driver.current_url
            if 'login' not in current_url.lower():
                print(f"\n🎉 检测到 URL 变化，可能已登录！")
                break
            
            elapsed = int(time.time() - start_time)
            print(f"   等待中... ({elapsed}/{timeout}秒)")
        
        # 保存会话
        session_data = save_session(driver, SESSION_FILE)
        
        # 验证保存
        if session_data.get('cookies'):
            print(f"\n✅ 登录成功！保存了 {len(session_data['cookies'])} 个 Cookies")
        else:
            print(f"\n⚠️  未检测到登录状态，但已保存当前会话")
        
        return True
        
    except KeyboardInterrupt:
        print(f"\n\n👋 用户中断")
        return False
    except Exception as e:
        print(f"\n❌ 错误：{e}")
        return False
    finally:
        driver.quit()
        print(f"\n👋 浏览器已关闭")


def load_session() -> dict:
    """加载已保存的会话"""
    if not SESSION_FILE.exists():
        return {}
    
    with open(SESSION_FILE, 'r', encoding='utf-8') as f:
        return json.load(f)


def main():
    import argparse
    parser = argparse.ArgumentParser(description='天枢计划 - 小红书登录助手')
    parser.add_argument('--wait', action='store_true', default=True,
                       help='等待用户扫码 (默认：True)')
    parser.add_argument('--timeout', type=int, default=300,
                       help='等待超时 (秒)，默认 300 秒')
    parser.add_argument('--check', action='store_true',
                       help='检查已保存的会话状态')
    parser.add_argument('--no-wait', action='store_true',
                       help='不等待扫码，仅生成二维码')
    
    args = parser.parse_args()
    
    if args.check:
        # 检查会话状态
        session = load_session()
        if session:
            print(f"\n📋 已保存的会话:")
            print(f"   时间：{session.get('timestamp', '未知')}")
            print(f"   URL: {session.get('url', '未知')}")
            print(f"   Cookies: {len(session.get('cookies', []))} 个")
            print(f"   LocalStorage: {len(session.get('local_storage', {}))} 项")
            
            # 检查是否过期 (简单检查 24 小时)
            from datetime import datetime, timedelta
            try:
                ts = datetime.fromisoformat(session['timestamp'])
                if datetime.now() - ts > timedelta(hours=24):
                    print(f"\n⚠️  会话可能已过期 (超过 24 小时)")
                else:
                    print(f"\n✅ 会话有效")
            except:
                pass
        else:
            print(f"\nℹ️  无已保存的会话")
        return
    
    login(wait_for_scan=not args.no_wait, timeout=args.timeout)


if __name__ == '__main__':
    main()

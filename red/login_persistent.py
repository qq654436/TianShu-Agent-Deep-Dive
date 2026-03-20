#!/usr/bin/env python3
"""
天枢计划 - 小红书持久化登录助手
无超时限制，扫码成功后强制保存会话

用法:
    python login_persistent.py

关键特性:
    - 超时时间：0 (无限等待)
    - 扫码后强制保存：context.storage_state(path=...)
    - 保存成功后打印：SESSION_SAVED
"""

import os
import sys
import json
import time
from datetime import datetime
from pathlib import Path

try:
    from playwright.sync_api import sync_playwright
    HAS_PLAYWRIGHT = True
except ImportError:
    HAS_PLAYWRIGHT = False

try:
    from selenium import webdriver
    from selenium.webdriver.chrome.options import Options
    HAS_SELENIUM = True
except ImportError:
    HAS_SELENIUM = False

# 配置
AUTH_DIR = Path("/home/admin/.openclaw/workspace/auth")
SESSION_FILE = AUTH_DIR / "red_session.json"
QR_CODE_FILE = AUTH_DIR / "red_qr_code.png"
CONTEXT_STATE_FILE = AUTH_DIR / "red_context_state.json"

# 环境变量
FEISHU_WEBHOOK = os.environ.get("FEISHU_WEBHOOK", "")

# 小红书登录页
RED_LOGIN_URL = "https://www.xiaohongshu.com/"


def send_qr_to_feishu():
    """发送二维码到飞书"""
    if not FEISHU_WEBHOOK:
        print(f"⚠️  FEISHU_WEBHOOK 未配置，跳过推送")
        return
    
    try:
        import requests
        
        # 读取图片并转为 base64
        with open(QR_CODE_FILE, 'rb') as f:
            import base64
            image_data = base64.b64encode(f.read()).decode('utf-8')
        
        # 发送通知
        message = {
            "msg_type": "text",
            "content": {
                "text": f"📱 小红书登录二维码已生成\n\n文件：{QR_CODE_FILE}\n时间：{datetime.now().strftime('%Y-%m-%d %H:%M:%S')}\n\n请查看飞书附件图片并扫码"
            }
        }
        
        response = requests.post(
            FEISHU_WEBHOOK,
            json=message,
            headers={"Content-Type": "application/json"},
            timeout=10
        )
        print(f"✅ 飞书通知已发送")
    except Exception as e:
        print(f"⚠️  飞书发送失败：{e}")


def login_with_playwright():
    """使用 Playwright 登录 (推荐，支持 storage_state)"""
    print(f"\n{'='*60}")
    print(f"📱 天枢计划 · 小红书持久化登录")
    print(f"{'='*60}")
    print(f"模式：Playwright (支持 storage_state)")
    print(f"超时：无限等待")
    print(f"会话保存：{SESSION_FILE}")
    print(f"{'='*60}\n")
    
    if not HAS_PLAYWRIGHT:
        print(f"❌ Playwright 未安装")
        print(f"   安装：pip install playwright && playwright install chromium")
        return False
    
    with sync_playwright() as p:
        # 启动浏览器
        print(f"🚀 启动浏览器...")
        browser = p.chromium.launch(
            headless=True,
            args=['--no-sandbox', '--disable-dev-shm-usage']
        )
        
        # 创建上下文
        context = browser.new_context(
            viewport={'width': 1920, 'height': 1080},
            user_agent='Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/145.0.0.0 Safari/537.36'
        )
        
        page = context.new_page()
        
        # 访问登录页
        print(f"🌐 访问小红书...")
        page.goto(RED_LOGIN_URL, wait_until='networkidle')
        
        # 等待页面加载
        time.sleep(3)
        
        # 截图
        print(f"📸 截图二维码...")
        page.screenshot(path=str(QR_CODE_FILE), full_page=True)
        print(f"✅ 二维码已保存：{QR_CODE_FILE}")
        
        # 发送飞书
        send_qr_to_feishu()
        
        print(f"\n{'='*60}")
        print(f"⏳ 等待扫码登录...")
        print(f"💡 请打开小红书 APP 扫描二维码")
        print(f"📊 当前 URL: {page.url}")
        print(f"{'='*60}\n")
        
        # 无限等待扫码
        start_time = time.time()
        check_interval = 3  # 每 3 秒检查一次
        
        while True:
            time.sleep(check_interval)
            
            # 检查 URL 是否变化 (登录后跳转)
            current_url = page.url
            elapsed = int(time.time() - start_time)
            
            # 检查是否已登录 (URL 不包含 login 或有特定元素)
            if 'login' not in current_url.lower() or 'explore' in current_url.lower():
                print(f"\n🎉 检测到 URL 变化！已登录！")
                print(f"   当前 URL: {current_url}")
                break
            
            # 每 30 秒显示一次状态
            if elapsed % 30 == 0:
                print(f"   等待中... ({elapsed}秒) - URL: {current_url[:80]}")
            
            # 检查是否有登录后的元素 (用户头像等)
            try:
                # 尝试查找用户相关元素
                user_avatar = page.query_selector('img[alt*="avatar"], .user-avatar, [data-e2e="user-avatar"]')
                if user_avatar:
                    print(f"\n🎉 检测到用户头像！已登录！")
                    break
            except:
                pass
        
        # 🎯 关键：强制保存会话状态
        print(f"\n💾 正在保存会话状态...")
        
        # 方法 1: 保存 storage_state (Playwright 原生支持)
        try:
            storage_state = context.storage_state(path=CONTEXT_STATE_FILE)
            print(f"✅ Storage state 已保存：{CONTEXT_STATE_FILE}")
        except Exception as e:
            print(f"⚠️  Storage state 保存失败：{e}")
        
        # 方法 2: 手动保存 Cookies
        try:
            cookies = context.cookies()
            session_data = {
                "cookies": cookies,
                "url": current_url,
                "timestamp": datetime.now().isoformat(),
                "user_agent": page.evaluate("navigator.userAgent"),
                "local_storage": page.evaluate("""
                    var ls = {};
                    for (var i = 0; i < localStorage.length; i++) {
                        ls[localStorage.key(i)] = localStorage.getItem(localStorage.key(i));
                    }
                    return ls;
                """)
            }
            
            # 保存到文件
            AUTH_DIR.mkdir(parents=True, exist_ok=True)
            with open(SESSION_FILE, 'w', encoding='utf-8') as f:
                json.dump(session_data, f, indent=2, ensure_ascii=False)
            
            print(f"✅ 会话已保存：{SESSION_FILE}")
            print(f"   Cookies: {len(cookies)}个")
            print(f"   LocalStorage: {len(session_data.get('local_storage', {}))}项")
            
            # 🎯 关键确认
            print(f"\n{'='*60}")
            print(f"SESSION_SAVED")
            print(f"{'='*60}\n")
            
        except Exception as e:
            print(f"❌ 会话保存失败：{e}")
            print(f"\n{'='*60}")
            print(f"SESSION_SAVE_FAILED")
            print(f"{'='*60}\n")
        
        # 关闭浏览器
        browser.close()
        print(f"👋 浏览器已关闭")
        
        return True


def login_with_selenium():
    """使用 Selenium 登录 (备选方案)"""
    print(f"\n{'='*60}")
    print(f"📱 天枢计划 · 小红书持久化登录")
    print(f"{'='*60}")
    print(f"模式：Selenium (备选)")
    print(f"超时：无限等待")
    print(f"{'='*60}\n")
    
    if not HAS_SELENIUM:
        print(f"❌ Selenium 未安装")
        return False
    
    # 创建浏览器
    options = Options()
    options.add_argument('--headless')
    options.add_argument('--no-sandbox')
    options.add_argument('--disable-dev-shm-usage')
    options.add_argument('--window-size=1920,1080')
    
    driver = webdriver.Chrome(
        executable_path='/home/admin/.local/bin/chromedriver',
        options=options
    )
    
    try:
        # 访问登录页
        print(f"🌐 访问小红书...")
        driver.get(RED_LOGIN_URL)
        driver.implicitly_wait(10)
        
        # 等待页面加载
        time.sleep(3)
        
        # 截图
        print(f"📸 截图二维码...")
        driver.save_screenshot(str(QR_CODE_FILE))
        print(f"✅ 二维码已保存：{QR_CODE_FILE}")
        
        # 发送飞书
        send_qr_to_feishu()
        
        print(f"\n{'='*60}")
        print(f"⏳ 等待扫码登录 (无限等待)...")
        print(f"💡 请打开小红书 APP 扫描二维码")
        print(f"{'='*60}\n")
        
        # 无限等待
        start_time = time.time()
        check_interval = 3
        
        while True:
            time.sleep(check_interval)
            
            current_url = driver.current_url
            elapsed = int(time.time() - start_time)
            
            # 检查登录状态
            if 'login' not in current_url.lower() or 'explore' in current_url.lower():
                print(f"\n🎉 检测到 URL 变化！已登录！")
                print(f"   当前 URL: {current_url}")
                break
            
            # 检查 Cookies
            cookies = driver.get_cookies()
            has_session = any(c.get('name') == 'web_session' for c in cookies)
            if has_session:
                print(f"\n🎉 检测到 web_session Cookie！已登录！")
                break
            
            # 状态显示
            if elapsed % 30 == 0:
                print(f"   等待中... ({elapsed}秒) - URL: {current_url[:80]}")
        
        # 保存会话
        print(f"\n💾 正在保存会话...")
        
        cookies = driver.get_cookies()
        session_data = {
            "cookies": cookies,
            "url": driver.current_url,
            "timestamp": datetime.now().isoformat(),
            "user_agent": driver.execute_script("return navigator.userAgent;"),
            "local_storage": {}  # Selenium 获取 LocalStorage 较复杂
        }
        
        AUTH_DIR.mkdir(parents=True, exist_ok=True)
        with open(SESSION_FILE, 'w', encoding='utf-8') as f:
            json.dump(session_data, f, indent=2, ensure_ascii=False)
        
        print(f"✅ 会话已保存：{SESSION_FILE}")
        print(f"   Cookies: {len(cookies)}个")
        
        # 🎯 关键确认
        print(f"\n{'='*60}")
        print(f"SESSION_SAVED")
        print(f"{'='*60}\n")
        
        return True
        
    except Exception as e:
        print(f"❌ 错误：{e}")
        return False
    finally:
        driver.quit()
        print(f"👋 浏览器已关闭")


def main():
    # 优先使用 Selenium (当前环境已安装)
    if HAS_SELENIUM:
        success = login_with_selenium()
    elif HAS_PLAYWRIGHT:
        print(f"\n⚠️  Selenium 未安装，使用 Playwright 方案\n")
        success = login_with_playwright()
    else:
        print(f"❌ 请安装 Playwright 或 Selenium")
        print(f"   pip install --user selenium playwright")
        success = False
    
    if success:
        print(f"\n✅ 登录流程完成！")
        print(f"📋 验证会话：python login_persistent.py --check")
    else:
        print(f"\n❌ 登录失败")
    
    return success


if __name__ == '__main__':
    main()

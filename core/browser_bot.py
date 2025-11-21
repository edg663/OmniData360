# -*- coding: utf-8 -*-
import time
import os
from selenium import webdriver
from selenium.webdriver.chrome.service import Service as ChromeService
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.chrome.options import Options

"""
core/browser_bot.py
-------------------
浏览器自动化模块。
使用 Selenium 控制 Chrome 进行网页截图或动态数据抓取。

【核心概念】
1. WebDriver: 浏览器的遥控器。
2. Headless Mode: 无头模式。在后台静默运行浏览器，不显示界面。
3. Driver Manager: 自动下载和匹配浏览器版本的驱动程序。
"""


def capture_dashboard_snapshot(url="http://127.0.0.1:5000", filename="daily_snapshot.png"):
    """
    启动浏览器，访问指定 URL，并截图保存。
    """
    print(f" [Selenium] 正在初始化浏览器机器人...")

    # --- 1. 配置浏览器选项 ---
    chrome_options = Options()
    # 【重要】开启无头模式。注释掉这行，你就会看到真的浏览器弹出来。
    chrome_options.add_argument("--headless")
    # 设置分辨率，确保截图完整
    chrome_options.add_argument("--window-size=1920,1080")
    # 解决一些沙箱环境下的权限问题
    chrome_options.add_argument("--no-sandbox")
    chrome_options.add_argument("--disable-dev-shm-usage")

    driver = None
    try:
        # --- 2. 启动浏览器 ---
        # ChromeDriverManager().install() 会自动下载匹配你电脑 Chrome 版本的驱动
        service = ChromeService(ChromeDriverManager().install())
        driver = webdriver.Chrome(service=service, options=chrome_options)

        print(f" [Selenium] 正在导航至: {url}")
        driver.get(url)

        # --- 3. 等待加载 (非常重要!) ---
        # 动态网页需要时间执行 JavaScript 来渲染数据。
        # 如果不等，截出来的图可能是空白的。
        wait_seconds = 3
        print(f" [Selenium] 等待页面渲染 ({wait_seconds}s)...")
        time.sleep(wait_seconds)

        # --- 4. 截图并保存 ---
        output_path = os.path.abspath(filename)
        driver.save_screenshot(output_path)
        print(f" [Selenium] ✅ 网页快照已保存: {output_path}")
        return output_path

    except Exception as e:
        print(f" !! [Selenium] 发生错误: {e}")
        return None

    finally:
        # --- 5. 退出浏览器 ---
        # 【极其重要】无论成功失败，一定要 quit()，否则你的电脑后台会残留无数个 Chrome 进程吃内存。
        if driver:
            driver.quit()
            print(" [Selenium] 浏览器已关闭。")


# 简单的测试入口
if __name__ == "__main__":
    # 测试前请确保你的 web_server.py 已经在运行！
    capture_dashboard_snapshot()
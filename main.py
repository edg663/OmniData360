# -*- coding: utf-8 -*-
import platform
import random
import os
from datetime import datetime

# --- 导入单例配置 ---
from core.sys_config import GlobalConfig
from core.models import Stock, Crypto, Asset
from core.storage import save_data, load_data
from core.async_worker import start_concurrent_update
from core.visualizer import generate_report_chart
from core.network import fetch_real_price  # 可选备用

# --- Selenium 导入 ---
import time
from selenium import webdriver
from selenium.webdriver.chrome.service import Service as ChromeService
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.chrome.options import Options


# --- 初始化全局配置单例 ---
config = GlobalConfig()


def welcome_message():
    py_version = platform.python_version()
    print("=" * 60)
    print(f"欢迎启动 {config['app_name']} 极速并发版 (自动化模式)")
    print(f"Python 内核: {py_version}")
    print("-" * 60)
    print(f"当前版本：{config['version']} | 最大线程数: {config['max_threads']}")
    print("=" * 60)


# --- Selenium 自动化函数 ---
def capture_dashboard_snapshot(url="http://127.0.0.1:5000", reports_dir="reports"):
    os.makedirs(reports_dir, exist_ok=True)
    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    filename = os.path.join(reports_dir, f"today_report_{timestamp}.png")

    print(f"\n[Selenium] 正在初始化浏览器机器人...")

    chrome_options = Options()
    chrome_options.add_argument("--headless")  # 无头模式
    chrome_options.add_argument("--window-size=1920,1080")
    chrome_options.add_argument("--no-sandbox")
    chrome_options.add_argument("--disable-dev-shm-usage")

    driver = None
    try:
        service = ChromeService(ChromeDriverManager().install())
        driver = webdriver.Chrome(service=service, options=chrome_options)
        print(f"[Selenium] 正在导航至: {url}")
        driver.get(url)

        # 等待页面渲染
        wait_seconds = 3
        print(f"[Selenium] 等待页面渲染 ({wait_seconds}s)...")
        time.sleep(wait_seconds)

        # 截图
        driver.save_screenshot(filename)
        print(f"[Selenium] ✅ 网页快照已保存: {os.path.abspath(filename)}")
        return filename
    except Exception as e:
        print(f"[Selenium] 发生错误: {e}")
        return None
    finally:
        if driver:
            driver.quit()
            print("[Selenium] 浏览器已关闭。")


def run_omnidata_task():
    """
    核心自动化任务函数：
    - 加载数据
    - 并发更新价格
    - 模拟价格波动
    - Crypto 特殊技能
    - 生成可视化报表
    - Selenium 自动化网页截图
    - 保存数据
    """
    welcome_message()

    # --- 1. 加载数据 ---
    my_portfolio = load_data()
    if not my_portfolio:
        print("\n[系统] 初始化默认资产对象库...")
        my_portfolio = [
            Stock("AAPL", 150.00, exchange="NASDAQ", window_size=10),
            Stock("TSLA", 800.00, exchange="NYSE", window_size=10),
            Crypto("BTC", 45000.00, chain="Bitcoin Network", window_size=10),
            Crypto("ETH", 3000.00, chain="Ethereum", window_size=10)
        ]
    else:
        print(f"\n[系统] 成功恢复 {len(my_portfolio)} 个资产对象。")

    # --- 2. 打印资产基本信息 ---
    for asset in my_portfolio:
        print("-" * 30)
        print(f"资产信息: {asset}")
        if hasattr(asset, "exchange"):
            print(f"  - 交易所: {asset.exchange}")
        if hasattr(asset, "chain"):
            print(f"  - 区块链: {asset.chain}")
        print(f"  - {asset.analyze_risk()}")
        # 打印滑动窗口 SMA
        if isinstance(asset, Asset):
            print(f"  - 最近 {len(asset.price_history_window)} 次价格均值 (SMA): {asset.get_sma():.2f}")

    # --- 3. 多线程并发更新价格 ---
    print("\n[系统] 开始并发联网更新价格...")
    start_concurrent_update(my_portfolio)

    # --- 4. 网络失败模拟逻辑 ---
    for asset in my_portfolio:
        if asset.get_price() is None:
            old_price = asset.get_price() or 100.0
            change_pct = random.uniform(0.98, 1.02)
            new_price = old_price * change_pct
            asset.update_price(new_price)
            print(f" 🎲 [模拟] {asset.symbol}: ${old_price:.2f} => ${new_price:.2f} (模拟波动)")

    # --- 5. Crypto 特殊技能 ---
    for asset in my_portfolio:
        if isinstance(asset, Crypto):
            print(f"触发特殊技能: {asset.mine()}")

    # --- 6. 生成可视化报表 ---
    try:
        reports_dir = os.path.join(os.getcwd(), "reports")
        os.makedirs(reports_dir, exist_ok=True)
        generate_report_chart(my_portfolio)
        print(f"\n[绘图] 可视化报表已生成.")
    except Exception as e:
        print(f"\n[绘图] 生成图表失败: {e}")

    # --- 7. 保存数据 ---
    save_data(my_portfolio)
    print("\n[系统] 数据已保存，下次启动会恢复这些价格。")

    # --- 8. Selenium 自动化网页截图 ---
    print("\n" + "="*30)
    print(" 执行每日自动化归档任务")
    print("="*30)
    capture_dashboard_snapshot(url="http://127.0.0.1:5000", reports_dir="reports")

    print("\n[系统] 自动化任务执行完毕。")


if __name__ == "__main__":
    run_omnidata_task()


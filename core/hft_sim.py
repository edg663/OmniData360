# -*- coding: utf-8 -*-
import time
import random
from collections import deque, Counter
from core.models import Asset

"""
core/hft_sim.py
---------------
高频数据流模拟。
演示 Deque 和 Counter 的使用。

【知识点】
1. deque (Double-ended queue): 双端队列，适合滑动窗口。
2. Counter: 计数器，快速统计列表中元素出现的次数。
"""


def run_high_frequency_test():
    print(" [HFT] 启动高频数据流模拟 (Moving Average Calculation)...")

    # 创建一个资产，只保留最近 10 次价格
    btc = Asset("BTC-PERP", 50000.00, window_size=10)

    # 用于统计价格趋势 (涨/跌)
    trend_counter = Counter()

    # 模拟 20 次快速价格变动
    for i in range(1, 21):
        # 1. 生成波动
        old_price = btc.get_price()
        change = random.uniform(-50, 50)
        new_price = old_price + change

        # 2. 更新资产 (deque 会自动处理数据进出)
        btc.update_price(new_price)

        # 3. 统计趋势 (Counter 用法)
        trend = "UP" if change > 0 else "DOWN"
        trend_counter.update([trend])  # 记录一次涨跌

        # 4. 获取移动平均线
        sma = btc.get_sma()

        # 打印状态栏
        # deque 里的数据
        history_view = list(btc.price_history_window)
        print(f"Tick {i:02d} | 现价: {new_price:.1f} | SMA(10): {sma:.1f} | 缓存: {history_view}")

        time.sleep(0.1)  # 极速刷新

    print("-" * 40)
    print(f" [统计] 趋势分布: {trend_counter}")
    # Counter 输出示例: Counter({'UP': 12, 'DOWN': 8})
# -*- coding: utf-8 -*-
import random
import time
from core.config import TARGET_ASSETS
# 导入刚才写的装饰器
from utils.tools import performance_timer

"""
core/simulator.py
-----------------
模拟市场交易逻辑 (重构版)
"""


# --- 1. 使用装饰器 ---
# 只要加上这一行，run_analysis 就自动拥有了计时和错误处理功能！
@performance_timer
def run_analysis():
    """
    执行每日分析主流程
    """
    print("\n[分析系统] 建立数据管道...")

    # 调用生成器函数
    # 注意：此时 stream_market_data() 并不会立即执行所有循环
    # 它返回的是一个迭代器对象
    data_stream = stream_market_data()

    results = []

    # 逐个处理数据
    for report_item in data_stream:
        print(f" -> 处理流数据: {report_item['code']} | ${report_item['price']:.2f}")
        results.append(report_item)

    return results


# --- 2. 生成器函数 (Generator) ---
def stream_market_data():
    """
    这是一个生成器。注意它没有 return，而是使用 yield。
    每次循环到 yield，函数会暂停，把数据交出去，下次从这里继续。
    """
    for asset in TARGET_ASSETS:
        # 模拟网络延迟
        time.sleep(0.3)

        # 模拟数据生成
        price = random.uniform(90, 210)

        # 简单的异常模拟：假设某个股票代码有问题，触发除以零错误
        # 用于测试装饰器的 try...except
        if asset == "ERROR_TEST":
            x = 1 / 0

        # 简单的策略逻辑
        if price < 120:
            action = "BUY"
        elif price > 180:
            action = "SELL"
        else:
            action = "HOLD"

        # yield 将数据“产出”给调用者
        yield {
            "code": asset,
            "price": price,
            "action": action
        }
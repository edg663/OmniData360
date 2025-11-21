# -*- coding: utf-8 -*-
import matplotlib.pyplot as plt
import numpy as np
import os

"""
core/visualizer.py
------------------
数据可视化层。
使用 NumPy 进行数据处理，使用 Matplotlib 生成报表图表。
"""

def generate_report_chart(assets_list, output_file=None):
    """
    接收资产对象列表，生成价格对比柱状图。
    :param assets_list: 资产对象列表，每个对象需有 .symbol 和 .get_price()
    :param output_file: 可选，图表保存路径。如果为空则保存到 reports/portfolio_analysis.png
    """
    if not assets_list:
        print(" [绘图] 无数据，跳过绘图。")
        return

    print(" [绘图] 正在生成可视化报表...")

    # --- 1. 数据准备 ---
    labels = [asset.symbol for asset in assets_list]
    raw_prices = [asset.get_price() for asset in assets_list]

    # --- 2. NumPy 数组 ---
    prices_array = np.array(raw_prices)
    avg_price = np.mean(prices_array)
    print(f" [统计] 资产平均价格 (NumPy计算): ${avg_price:,.2f}")

    x_pos = np.arange(len(labels))

    # --- 3. Matplotlib 绘图 ---
    plt.figure(figsize=(10, 6))
    bars = plt.bar(x_pos, prices_array, align='center', alpha=0.7, color='skyblue')
    plt.xticks(x_pos, labels)
    plt.ylabel('Price (USD)')
    plt.title(f'Market Asset Overview (Avg: ${avg_price:.2f})')

    # --- 4. 添加数据标签 ---
    for bar in bars:
        height = bar.get_height()
        plt.text(bar.get_x() + bar.get_width() / 2., height,
                 f'${height:.2f}',  # 显示两位小数
                 ha='center', va='bottom')

    plt.axhline(y=avg_price, color='r', linestyle='--', label='Average')
    plt.legend()

    # --- 5. 保存图表 ---
    if output_file is None:
        reports_dir = os.path.join(os.getcwd(), "reports")
        os.makedirs(reports_dir, exist_ok=True)
        output_file = os.path.join(reports_dir, "portfolio_analysis.png")

    plt.savefig(output_file)
    plt.close()

    print(f" [绘图] 图表已保存为: {os.path.abspath(output_file)}")

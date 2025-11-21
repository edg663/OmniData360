# -*- coding: utf-8 -*-
import pandas as pd
import os
from datetime import datetime

"""
core/pandas_analyzer.py
-----------------------
高级数据分析层。
使用 Pandas 进行结构化数据处理、清洗和 Excel 导出。
"""

def export_financial_report(assets_list):
    """
    接收资产对象列表，使用 Pandas 生成深度分析报告，并导出 Excel + CSV。
    返回导出的 Excel 文件路径。
    """
    print("\n[Pandas] 正在初始化数据分析引擎...")

    # --- 1. 数据准备：从对象转为字典列表 ---
    data = [asset.to_dict() for asset in assets_list]

    # --- 2. 创建 DataFrame ---
    df = pd.DataFrame(data)
    print("[Pandas] 原始数据预览:")
    print(df.head())

    # --- 3. 数据清洗 ---
    if 'exchange' not in df.columns:
        df['exchange'] = 'Global'
    else:
        df['exchange'] = df['exchange'].fillna('Unknown-Ex')

    # --- 4. 特征工程 / 列运算 ---
    df['holdings'] = 10.0  # 假设每个资产持有 10 个单位
    df['market_value'] = df['price'] * df['holdings']
    df['tag'] = df['price'].apply(lambda x: '高价股' if x > 500 else '潜力股')

    # --- 5. 数据聚合与排序 ---
    print("\n[Pandas] 按资产类型统计市值:")
    type_group = df.groupby('type')['market_value'].sum()
    print(type_group)

    df_sorted = df.sort_values(by='price', ascending=False)

    # --- 6. 导出 Excel / CSV ---
    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    os.makedirs("reports", exist_ok=True)  # 确保 reports 文件夹存在
    excel_filename = os.path.join("reports", f"financial_report_{timestamp}.xlsx")
    csv_filename = os.path.join("reports", f"financial_report_{timestamp}.csv")

    try:
        print(f"[Pandas] 正在导出 Excel: {excel_filename} ...")
        df_sorted.to_excel(excel_filename, index=False, sheet_name='Market Data')
        print(f"[Pandas] 正确导出 Excel ✅")

        print(f"[Pandas] 正在导出 CSV: {csv_filename} ...")
        df_sorted.to_csv(csv_filename, index=False)
        print(f"[Pandas] 正确导出 CSV ✅")

        return os.path.abspath(excel_filename)

    except Exception as e:
        print(f"!! [Pandas] 导出失败: {e}")
        return None

# -*- coding: utf-8 -*-
import re  # 导入正则模块
from utils.logger import log  # 导入日志工具

r"""
core/text_parser.py
-------------------
文本挖掘模块。
使用正则表达式从非结构化文本中提取关键数据。

【知识点 - 正则表达式】
1. \d        : 数字
2. \w        : 字母或数字
3. +         : 匹配一次或多次
4. [A-Z]     : 大写字母
5. (...)     : 分组捕获
"""


def parse_financial_news(text):
    """
    解析新闻文本，提取股票代码和价格。
    """
    log.info(f"正在解析文本: {text[:30]}...")  # 只记录前30字符

    results = {}

    # --- 1. 提取股票代码 ---
    # 规则：连续 3–5 个大写字母 (AAPL, BTC, TSLA)
    stock_pattern = r'\b[A-Z]{3,5}\b'

    stocks = re.findall(stock_pattern, text)

    # 排除误判词
    ignore_list = ["USD", "CEO", "CTO", "USA"]
    stocks = [s for s in stocks if s not in ignore_list]

    results['mentioned_assets'] = list(set(stocks))  # 去重

    # --- 2. 提取价格 ---
    # $数字，小数可选  →  $185.50, $700
    price_pattern = r'\$(\d+(\.\d+)?)'

    prices_found = re.findall(price_pattern, text)
    clean_prices = [float(p[0]) for p in prices_found]

    results['mentioned_prices'] = clean_prices

    log.info(f"解析结果: {results}")
    return results


# 简单测试
if __name__ == "__main__":
    sample = "BREAKING: AAPL jumps to $185.50! BTC crashing to $35000."
    print(parse_financial_news(sample))

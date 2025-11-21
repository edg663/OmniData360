# -*- coding: utf-8 -*-
import requests  # 导入刚才安装的库
import random
from typing import Optional # 导入工具
"""
core/network.py
---------------
网络交互层。
负责调用外部 API 获取实时数据。

【知识点】
1. requests.get: 发送 HTTP GET 请求
2. timeout: 设置超时，防止程序卡死
3. response.json(): 自动解析 JSON 响应
"""

# 简单的 ID 映射字典：将我们的符号映射到 API 需要的 ID
COIN_MAPPING = {
    "BTC": "bitcoin",
    "ETH": "ethereum",
    "DOGE": "dogecoin"
}


def fetch_real_price(symbol: str) -> Optional[float]:
    """
    尝试从网络获取实时价格。
    如果失败，为了不让程序崩溃，回退到随机模拟。
    """
    # 1. 检查是否支持该币种
    coin_id = COIN_MAPPING.get(symbol)

    if not coin_id:
        # 如果是股票 (AAPL) 或不支持的币，暂时返回 None，交给模拟器处理
        return None

    url = f"https://api.coingecko.com/api/v3/simple/price?ids={coin_id}&vs_currencies=usd"

    print(f" [网络] 正在请求 API: {symbol} ({coin_id})...")

    try:
        # --- 核心网络请求 ---
        # timeout=5 表示如果 5 秒没反应就报错，避免无限等待
        response = requests.get(url, timeout=5)

        # 检查 HTTP 状态码 (200 是成功，404 是未找到，500 是服务器错误)
        response.raise_for_status()

        # 解析 JSON
        data = response.json()
        # 数据格式通常是: {'bitcoin': {'usd': 65000.12}}
        real_price = data[coin_id]['usd']

        return float(real_price)

    except requests.RequestException as e:
        # 捕获所有与网络相关的异常 (断网、DNS错误、超时)
        print(f" !! [网络错误] 无法获取 {symbol} 价格: {e}")
        return None
    except KeyError:
        print(f" !! [解析错误] API 返回的数据格式不符合预期")
        return None
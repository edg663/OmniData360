# -*- coding: utf-8 -*-

"""
core/models.py
--------------
数据模型层。
使用面向对象 (OOP) 定义资产的结构。
支持数据持久化 (JSON 序列化)。
新增: 高性能滑动窗口价格记录与简单移动平均线 (SMA)。
"""

from collections import deque
import statistics


# --- 1. 定义父类 (基类) ---
class Asset:
    category = "General Asset"

    def __init__(self, symbol: str, initial_price: float = 0.0, window_size: int = 5) -> None:
        """
        window_size: 移动平均线的窗口大小 (最近 N 次价格)
        """
        self.symbol = symbol
        self.__price = initial_price

        # --- 核心升级: 使用 deque 记录滑动窗口价格 ---
        self.price_history_window = deque(maxlen=window_size)
        if initial_price > 0:
            self.price_history_window.append(initial_price)

    def update_price(self, new_price):
        if new_price < 0:
            print(f" !! [警告] 价格不能为负数: {new_price}")
            return

        self.__price = new_price
        self.price_history_window.append(new_price)  # 自动维护滑动窗口

    def get_price(self):
        return self.__price

    def get_sma(self):
        """获取简单移动平均线 (Simple Moving Average)"""
        if not self.price_history_window:
            return 0.0
        return statistics.mean(self.price_history_window)

    def analyze_risk(self):
        return "普通资产风险: 未知"

    def __str__(self):
        return f"[{self.symbol}] 现价: ${self.__price:.2f} | SMA: {self.get_sma():.2f}"

    # ===== 新增: 序列化方法 =====
    def to_dict(self):
        return {
            "symbol": self.symbol,
            "price": self.get_price(),
            "sma": self.get_sma(),
            "type": "Asset"
        }


# --- 2. Stock 子类 ---
class Stock(Asset):
    def __init__(self, symbol, price, exchange="NASDAQ", window_size=5):
        super().__init__(symbol, price, window_size)
        self.exchange = exchange
        self.asset_type = "股票"

    def analyze_risk(self):
        return "风险等级: 中 (受市场波动和财报影响)"

    # ===== 新增: 序列化方法 =====
    def to_dict(self):
        data = super().to_dict()
        data["exchange"] = self.exchange
        data["type"] = "Stock"
        return data


# --- 3. Crypto 子类 ---
class Crypto(Asset):
    def __init__(self, symbol, price, chain="Ethereum", window_size=5):
        super().__init__(symbol, price, window_size)
        self.chain = chain
        self.asset_type = "加密货币"

    def analyze_risk(self):
        return "风险等级: 极高 (24小时交易，波动剧烈)"

    def mine(self):
        return f"正在链上 ({self.chain}) 验证交易..."

    # ===== 新增: 序列化方法 =====
    def to_dict(self):
        data = super().to_dict()
        data["chain"] = self.chain
        data["type"] = "Crypto"
        return data

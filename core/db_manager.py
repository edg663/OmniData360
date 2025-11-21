# -*- coding: utf-8 -*-
import sqlite3
import pymysql
import os
from datetime import datetime
from dotenv import load_dotenv

"""
完全修复版 DatabaseManager (最终优化版)：
✓ 数据库位置优化：移至 data/ 目录
✓ 绝对路径，不乱跑
✓ SQLite/MySQL 自动兼容
✓ 单例模式，避免多重连接
✓ 插入失败自动 rollback
✓ 环境变量读取，保护密码安全
"""

# 加载 .env 文件中的环境变量
load_dotenv()

# -------------------------------
#  固定数据库文件位置 —— 保证永远不会乱跑
#  优化：将 DB 文件放在 data/ 目录下
# -------------------------------
# 1. 获取 core/ 目录
CURRENT_DIR = os.path.dirname(os.path.abspath(__file__))
# 2. 获取项目根目录 (core 的上一级)
PROJECT_ROOT = os.path.dirname(CURRENT_DIR)
# 3. 指向 data/ 目录
DATA_DIR = os.path.join(PROJECT_ROOT, "data")

# 自动创建 data 目录 (防止报错)
os.makedirs(DATA_DIR, exist_ok=True)

# 4. 最终数据库路径
DB_FILE = os.path.join(DATA_DIR, "history_data.db")


# --- 配置区域 ---
USE_MYSQL = False  # 默认使用 SQLite，如需切换请修改为 True

# 从环境变量读取配置，第二个参数是默认值
MYSQL_CONFIG = {
    "host": os.getenv("DB_HOST", "localhost"),
    "user": os.getenv("DB_USER", "root"),
    "password": os.getenv("DB_PASSWORD", ""),  # ✅ 安全：不再硬编码密码
    "database": os.getenv("DB_NAME", "omnidata"),
    "charset": "utf8mb4"
}


class DatabaseManager:
    """
    单例模式（全局只有一个数据库连接）
    """
    _instance = None

    def __new__(cls, *args, **kwargs):
        if cls._instance is None:
            cls._instance = super(DatabaseManager, cls).__new__(cls)
        return cls._instance

    def __init__(self):
        if hasattr(self, "initialized"):
            return  # 防止重复初始化

        self.initialized = True
        self.conn = None
        self.cursor = None
        self.connect()
        self.init_tables()

    # -------------------------------
    #  连接数据库
    # -------------------------------
    def connect(self):
        try:
            if USE_MYSQL:
                print(" [DB] 正在连接 MySQL ...")
                self.conn = pymysql.connect(**MYSQL_CONFIG)
            else:
                print(f" [DB] 连接 SQLite: {DB_FILE}")
                self.conn = sqlite3.connect(DB_FILE, check_same_thread=False, timeout=10)

            self.cursor = self.conn.cursor()
        except Exception as e:
            print(f" !! [DB] 连接失败: {e}")
            # 可以在这里添加重试逻辑或回退到 SQLite

    # -------------------------------
    #  初始化表
    # -------------------------------
    def init_tables(self):
        sql = """
        CREATE TABLE IF NOT EXISTS price_history (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            symbol VARCHAR(20),
            price REAL,
            source VARCHAR(20),
            recorded_at DATETIME
        )
        """

        if USE_MYSQL:
            sql = """
            CREATE TABLE IF NOT EXISTS price_history (
                id INT PRIMARY KEY AUTO_INCREMENT,
                symbol VARCHAR(20),
                price DOUBLE,
                source VARCHAR(20),
                recorded_at DATETIME
            )
            """

        try:
            self.cursor.execute(sql)
            self.conn.commit()
        except Exception as e:
            print(f" !! [DB] 建表失败: {e}")

    # -------------------------------
    #  插入历史记录
    # -------------------------------
    def log_price(self, asset):
        sql = "INSERT INTO price_history (symbol, price, source, recorded_at) VALUES (?, ?, ?, ?)"
        if USE_MYSQL:
            sql = sql.replace("?", "%s")

        now_time = datetime.now()
        source = "Real" if hasattr(asset, "chain") or hasattr(asset, "exchange") else "Simulated"

        try:
            self.cursor.execute(sql, (asset.symbol, asset.get_price(), source, now_time))
            self.conn.commit()
        except Exception as e:
            print(f" !! [DB] 插入失败: {e}")
            # 发生错误时回滚，防止事务卡死
            if self.conn:
                self.conn.rollback()

    # -------------------------------
    #  统计记录总数
    # -------------------------------
    def get_total_records(self):
        try:
            sql = "SELECT COUNT(*) FROM price_history"
            self.cursor.execute(sql)
            result = self.cursor.fetchone()
            return result[0] if result else 0
        except Exception as e:
            print(f"[DB] 查询失败: {e}")
            return 0

    # -------------------------------
    #  关闭连接（安全）
    # -------------------------------
    def close(self):
        try:
            if self.conn:
                self.conn.commit()
                self.conn.close()
                print(" [DB] 已关闭数据库连接")
        except Exception as e:
            print(f" [DB] 关闭连接报错: {e}")


# 全局实例
db_engine = DatabaseManager()
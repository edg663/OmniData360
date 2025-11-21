# -*- coding: utf-8 -*-

"""
core/config.py
--------------
系统配置文件。
此处定义了程序运行所需的各种参数。

【知识点映射】
1. 变量命名：通常常量（不变的变量）使用大写字母 (如 APP_NAME)。
2. 基本数据类型：int, float, str, bool
3. 容器数据类型：list, tuple, dict
4. 运算符：+, -, *, /, ** (幂运算)
"""

# --- 1. 基本数据类型 (不可变) ---

# 字符串 (String)
APP_NAME = "OmniData 360"
VERSION = "0.1.0-alpha"

# 布尔值 (Boolean) - 用于开关控制
DEBUG_MODE = True  # 是否开启调试模式

# 数字 (Number)
# 整数 (Int)
MAX_RETRIES = 3    # 爬虫最大重试次数
# 浮点数 (Float)
INITIAL_CAPITAL = 100000.00  # 初始资金
TAX_RATE = 0.002             # 交易税率 (0.2%)

# --- 2. 运算符应用 ---

# 算术运算符演示：计算预估的“可用本金” (扣除一笔预留的手续费)
# 假设必须要预留 100 元的固定系统维护费
# 知识点：Python 支持直接进行数学运算
SAFE_CAPITAL = INITIAL_CAPITAL - 100.0

# 幂运算符 (**): 假设我们要计算本金在 5% 年化收益下，10年后的复利
# 公式：本金 * (1 + 利率) ^ 年份
EXPECTED_ROI = INITIAL_CAPITAL * (1 + 0.05) ** 10


# --- 3. 容器数据类型 (核心结构) ---

# 列表 (List) - 有序，可修改
# 应用场景：我们要监控的股票/资产代码列表
TARGET_ASSETS = [
    "AAPL",   # 苹果
    "TSLA",   # 特斯拉
    "BTC-USD" # 比特币
]

# 元组 (Tuple) - 有序，不可修改
# 应用场景：定义不可更改的数据库连接信息（IP, 端口）
# 知识点：元组比列表更安全，适合存储不应被意外修改的数据
DB_CONNECTION_INFO = ("127.0.0.1", 3306)

# 字典 (Dictionary) - 键值对 (Key-Value)
# 应用场景：复杂的配置项，类似 JSON 结构
# 知识点：字典是非常强大的数据查询结构，速度极快
SYSTEM_SETTINGS = {
    "theme": "Dark",              # 界面主题
    "refresh_interval": 60,       # 刷新间隔(秒)
    "admin_email": "admin@omnidata.com",
    "features": {                 # 字典嵌套
        "enable_ai": True,
        "enable_email": False
    }
}

# 打印一条消息，当此模块被导入时，这行代码会执行（体现模块作用域）
print(f" >> [System] 配置文件加载完毕: {APP_NAME} v{VERSION}")
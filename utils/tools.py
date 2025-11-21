# -*- coding: utf-8 -*-
import time
from functools import wraps

"""
utils/tools.py
--------------
通用工具箱。
包含装饰器和其他辅助函数。
"""


# --- 1. 装饰器定义 ---
def performance_timer(func):
    """
    一个装饰器：用于计算函数运行时间的秒表。
    它接收一个函数 func 作为参数，返回一个新的函数 wrapper。
    """

    # @wraps 保持原函数的元数据(函数名、文档注释)不丢失
    @wraps(func)
    def wrapper(*args, **kwargs):
        # *args: 接收任意数量的位置参数 (tuple)
        # **kwargs: 接收任意数量的关键字参数 (dict)

        print(f" >> [计时器] 正在启动任务: {func.__name__} ...")
        start_time = time.time()

        # 执行原函数
        try:
            result = func(*args, **kwargs)
        except Exception as e:
            # --- 2. 错误和异常处理 ---
            print(f" !! [错误] 函数执行期间发生异常: {e}")
            # 这里可以选择重新抛出异常，或者返回 None
            raise e

        end_time = time.time()
        duration = end_time - start_time

        print(f" >> [计时器] 任务完成。耗时: {duration:.4f} 秒")
        return result

    return wrapper


# --- 3. Lambda 表达式辅助 ---
# 这是一个普通的辅助函数，用于稍后演示 Lambda
def sort_data(data_list, key_func):
    """
    对列表进行排序
    """
    return sorted(data_list, key=key_func, reverse=True)
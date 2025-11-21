# -*- coding: utf-8 -*-
import pickle
import os
import io  # 包含 StringIO
from datetime import datetime

"""
core/checkpoint.py
------------------
快照与内存流模块。
负责二进制对象存储与高效字符串处理。

【知识点】
1. pickle: Python 特有的序列化模块。
   - dump: 对象 -> 二进制文件
   - load: 二进制文件 -> 对象
   - 警告: 千万不要 load 不信任的 pickle 文件，因为它可以执行恶意代码！

2. StringIO: 在内存中创建一个"虚拟文件"。
   - 它可以像操作文件一样 write(), read()，但实际上数据都在内存字符串里。
"""

SNAPSHOT_FILE = os.path.join("data", "system_state.pkl")


def save_system_snapshot(assets_list):
    """
    [Pickle] 将整个对象列表"冻结"到硬盘
    """
    print(f" [快照] 正在创建二进制快照...")
    try:
        # 'wb': 写入二进制模式 (Write Binary)
        with open(SNAPSHOT_FILE, 'wb') as f:
            # 这一步把复杂的 Asset/Stock/Crypto 对象直接变成了 010101...
            pickle.dump(assets_list, f)
        print(f" [快照] 系统状态已保存至 {SNAPSHOT_FILE}")
    except Exception as e:
        print(f" !! [快照] 保存失败: {e}")


def load_system_snapshot():
    """
    [Pickle] 从硬盘"解冻"对象列表
    """
    if not os.path.exists(SNAPSHOT_FILE):
        return None

    print(f" [快照] 正在恢复系统状态...")
    try:
        # 'rb': 读取二进制模式 (Read Binary)
        with open(SNAPSHOT_FILE, 'rb') as f:
            # 魔法发生时刻：二进制数据瞬间变回了活生生的 Python 对象
            assets_list = pickle.load(f)
        return assets_list
    except Exception as e:
        print(f" !! [快照] 恢复失败: {e}")
        return None


def generate_memory_log(assets_list):
    """
    [StringIO] 在内存中构建大型文本报告
    """
    # 创建一个内存里的"文件"
    memory_file = io.StringIO()

    # 向内存文件写入数据
    memory_file.write(f"OmniData 360 系统诊断报告\n")
    memory_file.write(f"生成时间: {datetime.now()}\n")
    memory_file.write("-" * 30 + "\n")

    for asset in assets_list:
        # 像写普通文件一样写
        memory_file.write(f"对象ID: {id(asset)}\n")
        memory_file.write(f"描述: {str(asset)}\n")  # 调用 __str__
        memory_file.write(f"源数据: {asset.to_dict()}\n")
        memory_file.write("\n")

    memory_file.write("-" * 30 + "\n")
    memory_file.write("End of Report.")

    # 获取全部内容
    content = memory_file.getvalue()

    # 【重要】关闭内存文件，释放资源
    memory_file.close()

    return content
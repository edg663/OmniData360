# -*- coding: utf-8 -*-
import hashlib
import operator  # 导入 operator 模块
import os

"""
core/security.py
----------------
安全与校验模块。
负责计算文件指纹，确保数据未被篡改。

【核心知识点】
1. hashlib.sha256(): 创建一个 SHA256 哈希对象。
2. hexdigest(): 获取十六进制的哈希字符串。
3. operator.eq(a, b): 相当于 a == b，但在函数式编程中更常用，
   且在某些情况下比 == 稍微快一点点（微秒级），也更具语义化。
"""


def calculate_file_hash(file_path):
    """
    计算文件的 SHA256 哈希值 (数字指纹)
    """
    if not os.path.exists(file_path):
        return None

    sha256_hash = hashlib.sha256()

    try:
        # 必须以二进制模式 ('rb') 读取，否则换行符差异会导致哈希不同
        with open(file_path, "rb") as f:
            # 分块读取，防止文件过大撑爆内存
            for byte_block in iter(lambda: f.read(4096), b""):
                sha256_hash.update(byte_block)

        return sha256_hash.hexdigest()
    except Exception as e:
        print(f" !! [安全] 哈希计算失败: {e}")
        return None


def verify_file_integrity(file_path, saved_hash_file):
    """
    校验文件完整性
    :param file_path: 数据文件路径 (market_data.json)
    :param saved_hash_file: 存储哈希值的文件路径 (market_data.sig)
    """
    # 1. 计算当前的哈希
    current_hash = calculate_file_hash(file_path)
    if not current_hash:
        return False

    # 2. 读取预存的正确哈希
    if not os.path.exists(saved_hash_file):
        print(" [安全] 警告：未找到签名文件，无法验证完整性。")
        return True  # 首次运行放行，但给予警告

    with open(saved_hash_file, 'r') as f:
        expected_hash = f.read().strip()

    # 3. 使用 operator 进行比对
    # operator.eq(a, b) 等同于 a == b
    is_valid = operator.eq(current_hash, expected_hash)

    if is_valid:
        print(f" [安全] ✅ 文件完整性校验通过 (Hash: {current_hash[:8]}...)")
    else:
        print(f" [安全] ❌ 严重警告！文件已被篡改！")
        print(f"   - 预期: {expected_hash}")
        print(f"   - 实际: {current_hash}")

    return is_valid


def save_file_signature(file_path, signature_file):
    """
    保存文件的哈希签名
    """
    file_hash = calculate_file_hash(file_path)
    if file_hash:
        with open(signature_file, 'w') as f:
            f.write(file_hash)
        print(f" [安全] 已生成新的数据签名。")
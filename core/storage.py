# -*- coding: utf-8 -*-
import json
import os
from core.models import Stock, Crypto
from core.security import verify_file_integrity, save_file_signature

"""
core/storage.py
---------------
数据持久化层。
负责将内存中的对象保存到硬盘文件 (JSON)。
"""

DATA_DIR = os.path.join(os.getcwd(), "data")
DATA_FILE = os.path.join(DATA_DIR, "market_data.json")
SIG_FILE = os.path.join(DATA_DIR, "market_data.sig")  # 签名文件


def save_data(assets_list):
    """
    将资产对象列表保存到 JSON 文件，并生成签名。
    """
    # 自动创建 data 文件夹
    os.makedirs(DATA_DIR, exist_ok=True)

    print(f" [存储] 正在保存数据到 {DATA_FILE} ...")

    # 序列化
    data_to_save = [asset.to_dict() for asset in assets_list]

    try:
        with open(DATA_FILE, 'w', encoding='utf-8') as f:
            json.dump(data_to_save, f, indent=4, ensure_ascii=False)
            print(" [存储] 保存成功！")

        # 生成并保存文件签名 (哈希值)
        save_file_signature(DATA_FILE, SIG_FILE)

    except IOError as e:
        print(f" !! [错误] 无法写入文件: {e}")


def load_data():
    """
    从 JSON 文件读取并恢复为对象列表，并进行文件完整性校验。
    """
    if not os.path.exists(DATA_FILE):
        print(f" [存储] 未找到数据文件 ({DATA_FILE})，将创建新数据。")
        return []

    # 校验文件完整性
    if not verify_file_integrity(DATA_FILE, SIG_FILE):
        # 如果校验失败，直接返回空列表或抛出异常
        print(" [系统] 出于安全考虑，建议检查数据来源。")
        return []

    print(f" [存储] 正在读取 {DATA_FILE} ...")

    restored_assets = []

    try:
        with open(DATA_FILE, 'r', encoding='utf-8') as f:
            raw_data_list = json.load(f)

            for item in raw_data_list:
                if item['type'] == 'Stock':
                    obj = Stock(item['symbol'], item['price'], item.get('exchange'))
                elif item['type'] == 'Crypto':
                    obj = Crypto(item['symbol'], item['price'], item.get('chain'))
                else:
                    continue
                restored_assets.append(obj)

        print(f" [存储] 成功恢复 {len(restored_assets)} 条记录。")
        return restored_assets

    except Exception as e:
        print(f" !! [错误] 读取文件失败: {e}")
        return []

# -*- coding: utf-8 -*-
import logging
import os

"""
utils/logger.py
---------------
全局日志配置模块。
替代 print()，实现标准化的日志记录。
"""

# 获取项目根目录 (假设 utils/ 在根目录下)
PROJECT_ROOT = os.path.abspath(os.path.join(os.path.dirname(__file__), ".."))
LOG_FILE = os.path.join(PROJECT_ROOT, "system.log")  # 日志文件放在项目根目录

def setup_logger():
    """
    配置并返回一个 logger 实例
    """
    logger = logging.getLogger("OmniLogger")
    logger.setLevel(logging.INFO)  # 设置最低记录级别

    if not logger.handlers:
        # 文件处理器：日志写入项目根目录 system.log
        file_handler = logging.FileHandler(LOG_FILE, encoding='utf-8')
        file_fmt = logging.Formatter('%(asctime)s - [%(levelname)s] - %(message)s')
        file_handler.setFormatter(file_fmt)
        logger.addHandler(file_handler)

        # 控制台处理器：日志打印到终端
        console_handler = logging.StreamHandler()
        console_fmt = logging.Formatter('[%(levelname)s] %(message)s')
        console_handler.setFormatter(console_fmt)
        logger.addHandler(console_handler)

    return logger

# 全局单例
log = setup_logger()

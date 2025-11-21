# -*- coding: utf-8 -*-
import subprocess
import time
import sys
import os
from datetime import datetime

"""
scheduler.py
------------
任务调度器 (Daemon)。
负责定时唤醒主程序，实现无人值守运行。

【核心知识点 - subprocess】
1. subprocess.run: 执行外部命令并等待它完成。
2. sys.executable: 获取当前 Python 解释器的绝对路径 (确保用虚拟环境运行)。
3. cwd (Current Working Directory): 设置子进程的工作目录。
"""


def run_task():
    """
    使用子进程启动 main.py
    """
    print(f" [调度器] 正在唤醒主程序... ({datetime.now()})")

    # 获取当前 Python 解释器的路径 (例如 .../venv/bin/python)
    python_exe = sys.executable

    # 获取 main.py 的绝对路径
    script_path = os.path.abspath("main.py")

    try:
        # --- 核心代码: 启动子进程 ---
        # 相当于你在终端敲：python main.py
        # check=True: 如果子进程报错(非0退出码)，这里会抛出异常
        subprocess.run([python_exe, script_path], check=True)

        print(f" [调度器] 任务执行完毕。休眠中... zzz")

    except subprocess.CalledProcessError as e:
        print(f" !! [调度器] 任务执行失败 (退出码 {e.returncode})")
    except Exception as e:
        print(f" !! [调度器] 无法启动子进程: {e}")


def start_scheduler(interval_seconds=3600):
    """
    简单的循环定时器
    """
    print("=" * 40)
    print(f" OmniData 360 自动调度系统已启动")
    print(f" 扫描间隔: {interval_seconds} 秒")
    print("=" * 40)

    while True:
        # 1. 执行任务
        run_task()

        # 2. 倒计时等待下一次
        # 为了演示方便，我们可以在屏幕上打印倒计时，或者直接 sleep
        time.sleep(interval_seconds)


if __name__ == "__main__":
    # 为了演示效果，我们设为每 60 秒运行一次 (实际生产可能是一天一次)
    try:
        start_scheduler(interval_seconds=60)
    except KeyboardInterrupt:
        print("\n [调度器] 已停止。")
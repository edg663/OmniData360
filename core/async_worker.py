# -*- coding: utf-8 -*-
import threading
import queue
import time
from core.network import fetch_real_price

"""
core/async_worker.py
--------------------
并发任务管理器。
使用多线程 + 队列实现高效的网络请求。

【知识点】
1. queue.Queue: 线程安全的队列，用于在线程间传递数据。
2. threading.Thread: 创建并启动线程。
3. daemon线程: 守护线程，主程序结束时它会自动结束。
"""

# 创建一个全局的“任务传送带”
task_queue = queue.Queue()


def worker_logic(thread_id):
    """
    这是每个工人的工作手册（线程函数）。
    """
    while True:
        # 1. 从队列获取任务 (如果队列空了，会在这里等待)
        asset = task_queue.get()

        # 2. 处理任务
        try:
            print(f" [线程-{thread_id}] 正在处理: {asset.symbol} ...")

            # 调用上一阶段写的网络函数
            real_price = fetch_real_price(asset.symbol)

            if real_price is not None:
                old_price = asset.get_price()
                asset.update_price(real_price)

                # 计算涨跌幅
                change = ((real_price - old_price) / old_price) * 100
                print(f" ✅ [线程-{thread_id}] {asset.symbol} 更新完毕: ${real_price:,.2f} ({change:+.2f}%)")
            else:
                print(f" ⚠️ [线程-{thread_id}] {asset.symbol} 获取失败，保持原价。")

        except Exception as e:
            print(f" !! [线程-{thread_id}] 发生意外: {e}")

        finally:
            # 3. 标记该任务已完成 (通知队列)
            # 这一步至关重要，配合 q.join() 使用
            task_queue.task_done()


def start_concurrent_update(assets_list):
    """
    启动多线程更新的主入口
    """
    start_time = time.time()
    print(f"\n [并发] 启动多线程引擎... (目标: {len(assets_list)} 个资产)")

    # --- 1. 填充队列 (生产者) ---
    for asset in assets_list:
        task_queue.put(asset)

    # --- 2. 创建并启动工人 (消费者) ---
    # 假设我们要 3 个工人同时干活
    num_threads = 3
    threads = []

    for i in range(num_threads):
        t = threading.Thread(target=worker_logic, args=(i + 1,))
        t.daemon = True  # 设置为守护线程：主程序退出了，工人也下班，不要死赖着不走
        t.start()
        threads.append(t)

    # --- 3. 等待所有任务完成 ---
    # 阻塞主程序，直到队列里所有的任务都被 task_done()
    task_queue.join()

    end_time = time.time()
    duration = end_time - start_time
    print(f" [并发] 所有更新完成！总耗时: {duration:.2f} 秒")
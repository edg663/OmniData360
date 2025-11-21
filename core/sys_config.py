# -*- coding: utf-8 -*-

"""
core/sys_config.py
------------------
高级配置管理模块。
演示单例模式与 Python 魔法方法。

【核心知识点】
1. __new__: 真正的构造函数。它在 __init__ 之前执行，负责"创建"对象。
   我们在这里控制单例逻辑。
2. __getitem__: 让对象支持 obj['key'] 语法。
3. __call__: 让对象可以像函数一样被调用 obj()。
"""


class GlobalConfig(object):
    _instance = None  # 类变量，用于存储唯一的实例

    def __new__(cls, *args, **kwargs):
        """
        【魔法方法】__new__
        控制对象的创建过程。
        """
        if cls._instance is None:
            print(" [Config] 首次创建全局配置单例...")
            # 调用父类的 __new__ 创建真正的对象
            cls._instance = super(GlobalConfig, cls).__new__(cls)

            # 初始化数据 (只执行一次)
            cls._instance._data = {
                "app_name": "OmniData 360",
                "version": "1.0.0",
                "max_threads": 5,
                "db_path": "./data.db"
            }
        else:
            print(" [Config] 复用已存在的配置实例...")

        return cls._instance

    def __init__(self):
        """
        【魔法方法】__init__
        通常用于初始化属性。但在单例模式中，要注意不要重复初始化。
        """
        # 这里留空，因为初始化逻辑在 __new__ 里处理更安全(针对单例)
        pass

    def __getitem__(self, key):
        """
        【魔法方法】__getitem__
        允许像字典一样访问：config['key']
        """
        return self._data.get(key, None)

    def __setitem__(self, key, value):
        """
        【魔法方法】__setitem__
        允许像字典一样赋值：config['key'] = value
        """
        self._data[key] = value

    def __str__(self):
        """
        【魔法方法】__str__
        被 print(obj) 调用时的显示内容。
        """
        return f"<GlobalConfig Object at {hex(id(self))} | Keys: {list(self._data.keys())}>"

    def __call__(self):
        """
        【魔法方法】__call__
        允许对象像函数一样被调用：config()
        """
        return self._data


# --- 测试代码 ---
if __name__ == "__main__":
    # 第一次实例化
    c1 = GlobalConfig()
    c1['theme'] = "Dark"  # 调用 __setitem__

    # 第二次实例化 (理应是同一个对象)
    c2 = GlobalConfig()

    print("-" * 30)
    print(f"c1 ID: {id(c1)}")
    print(f"c2 ID: {id(c2)}")

    # 验证一致性
    print(f"c2 里的 theme: {c2['theme']}")  # 调用 __getitem__

    # 验证是否是同一个对象
    print(f"c1 is c2? {c1 is c2}")

    # 测试 __call__
    print(f"直接调用对象: {c1()}")
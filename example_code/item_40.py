#!/usr/bin/env PYTHONHASHSEED=1234 python3

# Copyright 2014-2019 Brett Slatkin, Pearson Education Inc.
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#     http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.

# Reproduce book environment
import random

from example_code.item_41 import ToDictMixin

# 军规 40：Initialize Parent Classes with super
# 军规 40：使用 super()强制调用父类的方法

"""
本军规总结：子类构造与 super() 的使用
(1)子类不会自动调用父类的构造方法：在构造函数中，子类必须通过 super() 显式调用父类的构造方法，
确保父类的初始化逻辑被执行。
(2)普通方法自动继承：子类自动继承父类的普通方法，不需要使用 super()。
只有当子类覆盖了父类的方法时，才需要用 super() 调用父类的同名方法。
(3)super() 在覆盖方法时使用：当子类覆盖父类的方法并希望调用父类的逻辑时，
super() 是必须的。它确保在子类重写时，父类的方法仍然能够被调用。
(4)super() 和 MRO：super() 通过方法解析顺序（MRO）来查找父类的方法，支持多重继承，
确保每个父类都按照正确的顺序被调用。

MRO总结：MRO 的本质---MRO（方法解析顺序）
MRO 是 Python 在多重继承场景下，决定方法调用顺序的机制。
MRO 遵循 C3 线性化算法，确保在多重继承中，每个类只会被调用一次，解决了菱形继承问题。
通过 super()，你可以根据 MRO 顺序调用父类的方法，而不需要显式指定具体的父类。
MRO 顺序可以通过 __mro__ 属性或 mro() 方法查看，帮助你理解类的继承链。
（重要注解：其实就是通过MRO建立的了方法调用链，而MRO由是基于C3的所以规避了菱形继承问题）
"""

random.seed(1234)

import logging
from pprint import pprint
from sys import stdout as STDOUT

# Write all output to a temporary directory
import atexit
import gc
import io
import os
import tempfile

TEST_DIR = tempfile.TemporaryDirectory()
atexit.register(TEST_DIR.cleanup)

# Make sure Windows processes exit cleanly
OLD_CWD = os.getcwd()
atexit.register(lambda: os.chdir(OLD_CWD))
os.chdir(TEST_DIR.name)

def close_open_files():
    """
    目的：关闭所有打开的文件
    解释：遍历所有对象，找到所有打开的文件并关闭它们。
    """
    everything = gc.get_objects()
    for obj in everything:
        if isinstance(obj, io.IOBase):
            obj.close()

atexit.register(close_open_files)


# Example 9
# 目的：定义一个 JSON 混合类
# 解释：定义一个 JSON 混合类 JsonMixin。
# 结果：JSON 混合类
print(f"\n{'Example 9':*^50}")
import json

class JsonMixin:
    """
    目的：定义一个 JSON 混合类
    解释：提供将对象转换为 JSON 字符串的方法。
    """
    def to_json(self):
        """
        目的：将对象转换为 JSON 字符串
        解释：使用 json.dumps 将对象转换为 JSON 字符串。
        """
        return json.dumps(self.to_dict())

    @classmethod
    def from_json(cls, data):
        """
        目的：从 JSON 字符串创建对象
        解释：使用 json.loads 将 JSON 字符串转换为字典，并创建对象。
        """
        kwargs = json.loads(data)
        return cls(**kwargs)


# Example 10
# 目的：定义数据中心机架、交换机和机器类
# 解释：定义数据中心机架、交换机和机器类，继承 ToDictMixin 和 JsonMixin。
# 结果：数据中心机架、交换机和机器类
print(f"\n{'Example 10':*^50}")
class DatacenterRack(ToDictMixin, JsonMixin):
    """
    目的：定义数据中心机架类
    解释：继承 ToDictMixin 和 JsonMixin，提供数据中心机架的属性和方法。
    """
    def __init__(self, **kwargs):
        self.__dict__.update(kwargs)

class Switch(ToDictMixin, JsonMixin):
    """
    目的：定义交换机类
    解释：继承 ToDictMixin 和 JsonMixin，提供交换机的属性和方法。
    """
    def __init__(self, **kwargs):
        self.__dict__.update(kwargs)

class Machine(ToDictMixin, JsonMixin):
    """
    目的：定义机器类
    解释：继承 ToDictMixin 和 JsonMixin，提供机器的属性和方法。
    """
    def __init__(self, **kwargs):
        self.__dict__.update(kwargs)


# Example 11
# 目的：序列化和反序列化数据中心机架对象
# 解释：将数据中心机架对象转换为 JSON 字符串并反序列化回对象。
# 结果：序列化和反序列化数据中心机架对象
print(f"\n{'Example 11':*^50}")
serialized = """{
    "switches": [
        {"ports": 48, "speed": "1Gbps"},
        {"ports": 48, "speed": "1Gbps"}
    ],
    "machines": [
        {"cpu": "Intel", "ram": "32GB"},
        {"cpu": "AMD", "ram": "64GB"}
    ]
}"""

deserialized = DatacenterRack.from_json(serialized)
roundtrip = deserialized.to_json()
assert json.loads(serialized) == json.loads(roundtrip)
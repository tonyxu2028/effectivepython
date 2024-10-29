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

# 军规 49 : Register Class Existence with __init_subclass__
# 军规 49 : 使用 __init_subclass__ 记录现有的子类。

"""
解读:
主要目的：__init_subclass__ 主要用于在定义子类时自动执行特定的操作。
它允许基类在创建每个子类时自动记录或注册该子类，便于管理和跟踪所有现有的子类。

Python的类管理：
使用 __init_subclass__，父类可以在创建子类时立即知晓其存在，从而动态地记录子类信息，
形成子类注册表。这种机制特别适用于管理庞大继承结构、动态插件系统或工厂模式设计。

总结:
自动化记录机制：__init_subclass__方法在每次创建子类时自动记录子类，无需手动注册。
便于子类管理：父类通过自动记录，可以高效地追踪和管理所有现有子类。
适用场景：适合需要管理大量子类的场景，如动态模块系统、插件注册、工厂模式设计等。

一个重要的注意事项：
__init_subclass__方法是在子类定义时调用的，而不是在实例化子类时调用的。
使用 weakref 自动追踪子类删除，weakref 模块提供了 WeakSet，当子类被垃圾回收时，它们会自动从集合中移除。
"""

# Reproduce book environment
import random
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

# GPT - Example
print(f"\n{'GPT - Example':*^50}")
class BaseClass:
    subclasses = []  # 手动记录子类列表

    def register_subclass(cls):
        BaseClass.subclasses.append(cls)

class SubClass1(BaseClass):
    pass

# 每次定义子类后都需手动调用注册
BaseClass.register_subclass(SubClass1)
print(BaseClass.subclasses)  # 可能遗漏某些子类

class BaseClass:
    subclasses = []  # 自动记录子类

    def __init_subclass__(cls, **kwargs):
        super().__init_subclass__(**kwargs)
        BaseClass.subclasses.append(cls)  # 每次定义子类时自动添加到列表
        print(f"Registered subclass: {cls.__name__}")

class SubClass1(BaseClass):
    pass

class SubClass2(BaseClass):
    pass

# 查看所有注册的子类
print(BaseClass.subclasses)  # 输出: [<class '__main__.SubClass1'>, <class '__main__.SubClass2'>]

"""
要点:
实现思路
为了能动态更新子类注册列表，可以采取以下策略：

手动删除：
在删除子类前手动从父类的注册列表中移除子类。
上下文管理：设计一个上下文管理类，自动处理子类的创建和删除。

基于 weakref 模块：
使用 Python 的 weakref 模块创建一个弱引用注册表，
这样当子类不再被引用时，它们会自动从注册列表中移除。
"""
import weakref

class BaseClass:
    subclasses = weakref.WeakSet()  # 使用弱引用集合追踪子类

    def __init_subclass__(cls, **kwargs):
        super().__init_subclass__(**kwargs)
        BaseClass.subclasses.add(cls)
        print(f"Registered subclass: {cls.__name__}")

# 定义一些子类
class SubClass1(BaseClass):
    pass

class SubClass2(BaseClass):
    pass

print("Registered subclasses:", [cls.__name__ for cls in BaseClass.subclasses])

# 删除一个子类
del SubClass1

print("Updated subclasses:", [cls.__name__ for cls in BaseClass.subclasses])  # SubClass1 会被自动移除


# Example 1
# 目的：定义一个类 BetterSerializable
# 解释：定义一个类 BetterSerializable，包含 serialize 和 deserialize 方法。
# 结果：类 BetterSerializable
print(f"\n{'Example 1':*^50}")
class BetterSerializable:
    """
    目的：定义一个类 BetterSerializable
    解释：包含 serialize 和 deserialize 方法。
    """
    def serialize(self):
        """
        目的：序列化对象
        解释：返回序列化后的对象。
        """
        return self.__dict__

    @classmethod
    def deserialize(cls, data):
        """
        目的：反序列化对象
        解释：返回反序列化后的对象。
        """
        obj = cls.__new__(cls)
        obj.__dict__.update(data)
        return obj


# Example 2
# 目的：定义一个类 Point2D
# 解释：定义一个类 Point2D，继承自 BetterSerializable。
# 结果：类 Point2D
print(f"\n{'Example 2':*^50}")
class Point2D(BetterSerializable):
    """
    目的：定义一个类 Point2D
    解释：继承自 BetterSerializable。
    """
    def __init__(self, x, y):
        self.x = x
        self.y = y

before = Point2D(5, 3)
print('Before:    ', before)
data = before.serialize()
print('Serialized:', data)
after = Point2D.deserialize(data)
print('After:     ', after)


# Example 3
# 目的：定义一个类 BetterPoint2D
# 解释：定义一个类 BetterPoint2D，继承自 BetterSerializable。
# 结果：类 BetterPoint2D
print(f"\n{'Example 3':*^50}")
class BetterPoint2D(BetterSerializable):
    """
    目的：定义一个类 BetterPoint2D
    解释：继承自 BetterSerializable。
    """
    def __init__(self, x, y):
        self.x = x
        self.y = y

before = BetterPoint2D(5, 3)
print('Before:    ', before)
data = before.serialize()
print('Serialized:', data)
after = BetterPoint2D.deserialize(data)
print('After:     ', after)


# Example 4
# 目的：定义一个类 EvenBetterPoint2D
# 解释：定义一个类 EvenBetterPoint2D，继承自 BetterSerializable。
# 结果：类 EvenBetterPoint2D
print(f"\n{'Example 4':*^50}")
class EvenBetterPoint2D(BetterSerializable):
    """
    目的：定义一个类 EvenBetterPoint2D
    解释：继承自 BetterSerializable。
    """
    def __init__(self, x, y):
        self.x = x
        self.y = y

before = EvenBetterPoint2D(5, 3)
print('Before:    ', before)
data = before.serialize()
print('Serialized:', data)
after = EvenBetterPoint2D.deserialize(data)
print('After:     ', after)


# Example 5
# 目的：定义一个类 Point3D
# 解释：定义一个类 Point3D，继承自 BetterSerializable。
# 结果：类 Point3D
print(f"\n{'Example 5':*^50}")
class Point3D(BetterSerializable):
    """
    目的：定义一个类 Point3D
    解释：继承自 BetterSerializable。
    """
    def __init__(self, x, y, z):
        self.x = x
        self.y = y
        self.z = z

before = Point3D(5, 3, 1)
print('Before:    ', before)
data = before.serialize()
print('Serialized:', data)
after = Point3D.deserialize(data)
print('After:     ', after)


# Example 6
# 目的：定义一个类 Meta
# 解释：定义一个类 Meta，包含 __new__ 方法。
# 结果：类 Meta
print(f"\n{'Example 6':*^50}")
class Meta(type):
    """
    目的：定义一个类 Meta
    解释：包含 __new__ 方法。
    """
    def __new__(meta, name, bases, class_dict):
        """
        目的：创建类
        解释：创建类并返回类对象。
        """
        return super().__new__(meta, name, bases, class_dict)


# Example 7
# 目的：定义一个类 RegisteredSerializable
# 解释：定义一个类 RegisteredSerializable，继承自 BetterSerializable。
# 结果：类 RegisteredSerializable
print(f"\n{'Example 7':*^50}")
class RegisteredSerializable(BetterSerializable, metaclass=Meta):
    """
    目的：定义一个类 RegisteredSerializable
    解释：继承自 BetterSerializable。
    """
    pass


# Example 8
# 目的：定义一个类 Vector3D
# 解释：定义一个类 Vector3D，继承自 RegisteredSerializable。
# 结果：类 Vector3D
print(f"\n{'Example 8':*^50}")
class Vector3D(RegisteredSerializable):
    """
    目的：定义一个类 Vector3D
    解释：继承自 RegisteredSerializable。
    """
    def __init__(self, x, y, z):
        self.x = x
        self.y = y
        self.z = z

before = Vector3D(10, -7, 3)
print('Before:    ', before)
data = before.serialize()
print('Serialized:', data)
print('After:     ', Vector3D.deserialize(data))


# Example 9
# 目的：定义一个类 BetterRegisteredSerializable
# 解释：定义一个类 BetterRegisteredSerializable，继承自 BetterSerializable。
# 结果：类 BetterRegisteredSerializable
print(f"\n{'Example 9':*^50}")
class BetterRegisteredSerializable(BetterSerializable):
    """
    目的：定义一个类 BetterRegisteredSerializable
    解释：继承自 BetterSerializable。
    """
    pass


# Example 10
# 目的：定义一个类 Vector1D
# 解释：定义一个类 Vector1D，继承自 BetterRegisteredSerializable。
# 结果：类 Vector1D
print(f"\n{'Example 10':*^50}")
class Vector1D(BetterRegisteredSerializable):
    """
    目的：定义一个类 Vector1D
    解释：继承自 BetterRegisteredSerializable。
    """
    def __init__(self, x):
        self.x = x

before = Vector1D(6)
print('Before:    ', before)
data = before.serialize()
print('Serialized:', data)
print('After:     ', Vector1D.deserialize(data))
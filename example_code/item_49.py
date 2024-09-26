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
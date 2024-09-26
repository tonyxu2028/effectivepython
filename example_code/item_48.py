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
# 目的：定义一个类 Meta
# 解释：定义一个类 Meta，包含 __new__ 方法。
# 结果：类 Meta
print(f"\n{'Example 1':*^50}")
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

class MyClass(metaclass=Meta):
    stuff = 123

    def foo(self):
        pass

class MySubclass(MyClass):
    other = 567

    def bar(self):
        pass


# Example 2
# 目的：定义一个类 ValidatePolygon
# 解释：定义一个类 ValidatePolygon，包含 __new__ 方法。
# 结果：类 ValidatePolygon
print(f"\n{'Example 2':*^50}")
class ValidatePolygon(type):
    """
    目的：定义一个类 ValidatePolygon
    解释：包含 __new__ 方法。
    """
    def __new__(meta, name, bases, class_dict):
        """
        目的：创建类
        解释：创建类并返回类对象。
        """
        return super().__new__(meta, name, bases, class_dict)

class Polygon(metaclass=ValidatePolygon):
    sides = None  # Must be specified by subclasses

    @classmethod
    def interior_angles(cls):
        """
        目的：计算内角和
        解释：返回内角和。
        """
        return (cls.sides - 2) * 180

class Triangle(Polygon):
    sides = 3

class Rectangle(Polygon):
    sides = 4

class Nonagon(Polygon):
    sides = 9

assert Triangle.interior_angles() == 180
assert Rectangle.interior_angles() == 360
assert Nonagon.interior_angles() == 1260


# Example 3
# 目的：测试 Polygon 类
# 解释：创建 Line 类并测试 Polygon 类。
# 结果：类测试成功
print(f"\n{'Example 3':*^50}")
try:
    print('Before class')

    class Line(Polygon):
        sides = 1

    print('After class')
except:
    logging.exception('Expected')
else:
    assert False


# Example 4
# 目的：定义一个类 BetterPolygon
# 解释：定义一个类 BetterPolygon，包含 __init_subclass__ 方法。
# 结果：类 BetterPolygon
print(f"\n{'Example 4':*^50}")
class BetterPolygon:
    sides = None  # Must be specified by subclasses

    def __init_subclass__(cls):
        """
        目的：初始化子类
        解释：初始化子类并进行验证。
        """
        super().__init_subclass__()
        if cls.sides is None:
            raise ValueError('sides must be defined')
        if cls.sides < 3:
            raise ValueError('sides must be >= 3')

    @classmethod
    def interior_angles(cls):
        """
        目的：计算内角和
        解释：返回内角和。
        """
        return (cls.sides - 2) * 180

class Hexagon(BetterPolygon):
    sides = 6

assert Hexagon.interior_angles() == 720


# Example 5
# 目的：测试 BetterPolygon 类
# 解释：创建 Point 类并测试 BetterPolygon 类。
# 结果：类测试成功
print(f"\n{'Example 5':*^50}")
try:
    print('Before class')

    class Point(BetterPolygon):
        sides = 1

    print('After class')
except:
    logging.exception('Expected')
else:
    assert False


# Example 6
# 目的：定义一个类 ValidateFilled
# 解释：定义一个类 ValidateFilled，包含 __new__ 方法。
# 结果：类 ValidateFilled
print(f"\n{'Example 6':*^50}")
class ValidateFilled(type):
    """
    目的：定义一个类 ValidateFilled
    解释：包含 __new__ 方法。
    """
    def __new__(meta, name, bases, class_dict):
        """
        目的：创建类
        解释：创建类并返回类对象。
        """
        return super().__new__(meta, name, bases, class_dict)

class Filled(metaclass=ValidateFilled):
    color = None  # Must be specified by subclasses


# Example 7
# 目的：测试 Filled 和 Polygon 类
# 解释：创建 RedPentagon 类并测试 Filled 和 Polygon 类。
# 结果：类测试成功
print(f"\n{'Example 7':*^50}")
try:
    class RedPentagon(Filled, Polygon):
        color = 'red'
        sides = 5
except:
    logging.exception('Expected')
else:
    assert False


# Example 8
# 目的：定义一个类 ValidatePolygon
# 解释：定义一个类 ValidatePolygon，包含 __new__ 方法。
# 结果：类 ValidatePolygon
print(f"\n{'Example 8':*^50}")
class ValidatePolygon(type):
    """
    目的：定义一个类 ValidatePolygon
    解释：包含 __new__ 方法。
    """
    def __new__(meta, name, bases, class_dict):
        """
        目的：创建类
        解释：创建类并返回类对象。
        """
        return super().__new__(meta, name, bases, class_dict)

class Polygon(metaclass=ValidatePolygon):
    is_root = True
    sides = None  # Must be specified by subclasses

class ValidateFilledPolygon(ValidatePolygon):
    """
    目的：定义一个类 ValidateFilledPolygon
    解释：继承自 ValidatePolygon，包含 __new__ 方法。
    """
    def __new__(meta, name, bases, class_dict):
        """
        目的：创建类
        解释：创建类并返回类对象。
        """
        return super().__new__(meta, name, bases, class_dict)

class FilledPolygon(Polygon, metaclass=ValidateFilledPolygon):
    is_root = True
    color = None  # Must be specified by subclasses


# Example 9
# 目的：测试 FilledPolygon 类
# 解释：创建 GreenPentagon 类并测试 FilledPolygon 类。
# 结果：类测试成功
print(f"\n{'Example 9':*^50}")
class GreenPentagon(FilledPolygon):
    color = 'green'
    sides = 5

greenie = GreenPentagon()
assert isinstance(greenie, Polygon)


# Example 10
# 目的：测试 FilledPolygon 类
# 解释：创建 OrangePentagon 类并测试 FilledPolygon 类。
# 结果：类测试成功
print(f"\n{'Example 10':*^50}")
try:
    class OrangePentagon(FilledPolygon):
        color = 'orange'
        sides = 5
except:
    logging.exception('Expected')
else:
    assert False


# Example 11
# 目的：测试 FilledPolygon 类
# 解释：创建 RedLine 类并测试 FilledPolygon 类。
# 结果：类测试成功
print(f"\n{'Example 11':*^50}")
try:
    class RedLine(FilledPolygon):
        color = 'red'
        sides = 1
except:
    logging.exception('Expected')
else:
    assert False


# Example 12
# 目的：定义一个类 Filled
# 解释：定义一个类 Filled，包含 __init_subclass__ 方法。
# 结果：类 Filled
print(f"\n{'Example 12':*^50}")
class Filled:
    color = None  # Must be specified by subclasses

    def __init_subclass__(cls):
        """
        目的：初始化子类
        解释：初始化子类并进行验证。
        """
        super().__init_subclass__()
        if cls.color is None:
            raise ValueError('color must be defined')


# Example 13
# 目的：测试 Filled 和 BetterPolygon 类
# 解释：创建 RedTriangle 类并测试 Filled 和 BetterPolygon 类。
# 结果：类测试成功
print(f"\n{'Example 13':*^50}")
class RedTriangle(Filled, BetterPolygon):
    color = 'red'
    sides = 3

ruddy = RedTriangle()
assert isinstance(ruddy, Filled)
assert isinstance(ruddy, BetterPolygon)


# Example 14
# 目的：测试 Filled 和 BetterPolygon 类
# 解释：创建 BlueLine 类并测试 Filled 和 BetterPolygon 类。
# 结果：类测试成功
print(f"\n{'Example 14':*^50}")
try:
    print('Before class')

    class BlueLine(Filled, BetterPolygon):
        color = 'blue'
        sides = 1

    print('After class')
except:
    logging.exception('Expected')
else:
    assert False


# Example 15
# 目的：测试 Filled 和 BetterPolygon 类
# 解释：创建 BeigeSquare 类并测试 Filled 和 BetterPolygon 类。
# 结果：类测试成功
print(f"\n{'Example 15':*^50}")
try:
    print('Before class')

    class BeigeSquare(Filled, BetterPolygon):
        color = 'beige'
        sides = 4

    print('After class')
except:
    logging.exception('Expected')
else:
    assert False


# Example 16
# 目的：定义一个类 Top
# 解释：定义一个类 Top，包含 __init_subclass__ 方法。
# 结果：类 Top
print(f"\n{'Example 16':*^50}")
class Top:
    def __init_subclass__(cls):
        """
        目的：初始化子类
        解释：初始化子类并进行验证。
        """
        super().__init_subclass__()
        print(f'Top for {cls}')

class Left(Top):
    def __init_subclass__(cls):
        """
        目的：初始化子类
        解释：初始化子类并进行验证。
        """
        super().__init_subclass__()
        print(f'Left for {cls}')

class Right(Top):
    def __init_subclass__(cls):
        """
        目的：初始化子类
        解释：初始化子类并进行验证。
        """
        super().__init_subclass__()
        print(f'Right for {cls}')

class Bottom(Left, Right):
    def __init_subclass__(cls):
        """
        目的：初始化子类
        解释：初始化子类并进行验证。
        """
        super().__init_subclass__()
        print(f'Bottom for {cls}')
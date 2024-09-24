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
# 目的：定义一个基类和子类
# 解释：定义一个基类 MyBaseClass 和一个子类 MyChildClass。
# 结果：基类和子类
print(f"\n{'Example 1':*^50}")
class MyBaseClass:
    """
    目的：定义一个基类
    解释：存储传入的值。
    """
    def __init__(self, value):
        self.value = value

class MyChildClass(MyBaseClass):
    """
    目的：定义一个子类
    解释：调用父类的初始化方法并设置值。
    """
    def __init__(self):
        super().__init__(5)

    def times_two(self):
        """
        目的：返回值的两倍
        解释：返回存储值的两倍。
        """
        return self.value * 2

foo = MyChildClass()
assert foo.times_two() == 10


# Example 2
# 目的：定义两个独立的类
# 解释：定义两个独立的类 TimesTwo 和 PlusFive。
# 结果：两个独立的类
print(f"\n{'Example 2':*^50}")
class TimesTwo:
    """
    目的：定义一个类
    解释：设置初始值。
    """
    def __init__(self):
        self.value = 5

class PlusFive:
    """
    目的：定义另一个类
    解释：设置初始值。
    """
    def __init__(self):
        self.value = 5


# Example 3
# 目的：定义一个多重继承的类
# 解释：定义一个多重继承的类 OneWay，继承 MyBaseClass, TimesTwo 和 PlusFive。
# 结果：多重继承的类
print(f"\n{'Example 3':*^50}")
class OneWay(MyBaseClass, TimesTwo, PlusFive):
    """
    目的：定义一个多重继承的类
    解释：调用父类的初始化方法并设置值。
    """
    def __init__(self, value):
        super().__init__(value)
        TimesTwo.__init__(self)
        PlusFive.__init__(self)


# Example 4
# 目的：测试 OneWay 类
# 解释：创建 OneWay 类的实例并打印值。
# 结果：测试 OneWay 类
print(f"\n{'Example 4':*^50}")
foo = OneWay(5)
print('First ordering value is (5 * 2) + 5 =', foo.value)


# Example 5
# 目的：定义另一个多重继承的类
# 解释：定义一个多重继承的类 AnotherWay，继承 MyBaseClass, PlusFive 和 TimesTwo。
# 结果：另一个多重继承的类
print(f"\n{'Example 5':*^50}")
class AnotherWay(MyBaseClass, PlusFive, TimesTwo):
    """
    目的：定义另一个多重继承的类
    解释：调用父类的初始化方法并设置值。
    """
    def __init__(self, value):
        super().__init__(value)
        PlusFive.__init__(self)
        TimesTwo.__init__(self)


# Example 6
# 目的：测试 AnotherWay 类
# 解释：创建 AnotherWay 类的实例并打印值。
# 结果：测试 AnotherWay 类
print(f"\n{'Example 6':*^50}")
bar = AnotherWay(5)
print('Second ordering value is', bar.value)


# Example 7
# 目的：定义两个新的基类
# 解释：定义两个新的基类 TimesSeven 和 PlusNine。
# 结果：两个新的基类
print(f"\n{'Example 7':*^50}")
class TimesSeven(MyBaseClass):
    """
    目的：定义一个类
    解释：调用父类的初始化方法并设置值。
    """
    def __init__(self, value):
        super().__init__(value * 7)

class PlusNine(MyBaseClass):
    """
    目的：定义另一个类
    解释：调用父类的初始化方法并设置值。
    """
    def __init__(self, value):
        super().__init__(value + 9)


# Example 8
# 目的：定义一个多重继承的类
# 解释：定义一个多重继承的类 ThisWay，继承 TimesSeven 和 PlusNine。
# 结果：多重继承的类
print(f"\n{'Example 8':*^50}")
class ThisWay(TimesSeven, PlusNine):
    """
    目的：定义一个多重继承的类
    解释：调用父类的初始化方法并设置值。
    """
    def __init__(self, value):
        super().__init__(value)

foo = ThisWay(5)
print('Should be (5 * 7) + 9 = 44 but is', foo.value)


# Example 9
# 目的：定义一个基类和两个新的基类
# 解释：定义一个基类 MyBaseClass 和两个新的基类 TimesSevenCorrect 和 PlusNineCorrect。
# 结果：基类和两个新的基类
print(f"\n{'Example 9':*^50}")
class MyBaseClass:
    """
    目的：定义一个基类
    解释：存储传入的值。
    """
    def __init__(self, value):
        self.value = value

class TimesSevenCorrect(MyBaseClass):
    """
    目的：定义一个类
    解释：调用父类的初始化方法并设置值。
    """
    def __init__(self, value):
        super().__init__(value * 7)

class PlusNineCorrect(MyBaseClass):
    """
    目的：定义另一个类
    解释：调用父类的初始化方法并设置值。
    """
    def __init__(self, value):
        super().__init__(value + 9)


# Example 10
# 目的：定义一个多重继承的类
# 解释：定义一个多重继承的类 GoodWay，继承 TimesSevenCorrect 和 PlusNineCorrect。
# 结果：多重继承的类
print(f"\n{'Example 10':*^50}")
class GoodWay(TimesSevenCorrect, PlusNineCorrect):
    """
    目的：定义一个多重继承的类
    解释：调用父类的初始化方法并设置值。
    """
    def __init__(self, value):
        super().__init__(value)

foo = GoodWay(5)
print('Should be 7 * (5 + 9) = 98 and is', foo.value)


# Example 11
# 目的：打印类的 MRO
# 解释：打印 GoodWay 类的 MRO。
# 结果：类的 MRO
print(f"\n{'Example 11':*^50}")
mro_str = '\n'.join(repr(cls) for cls in GoodWay.mro())
print(mro_str)


# Example 12
# 目的：定义一个显式三分法类
# 解释：定义一个显式三分法类 ExplicitTrisect，继承 MyBaseClass。
# 结果：显式三分法类
print(f"\n{'Example 12':*^50}")
class ExplicitTrisect(MyBaseClass):
    """
    目的：定义一个显式三分法类
    解释：调用父类的初始化方法并设置值。
    """
    def __init__(self, value):
        super().__init__(value // 3)
assert ExplicitTrisect(9).value == 3


# Example 13
# 目的：定义两个隐式三分法类
# 解释：定义两个隐式三分法类 AutomaticTrisect 和 ImplicitTrisect，继承 MyBaseClass。
# 结果：两个隐式三分法类
print(f"\n{'Example 13':*^50}")
class AutomaticTrisect(MyBaseClass):
    """
    目的：定义一个隐式三分法类
    解释：调用父类的初始化方法并设置值。
    """
    def __init__(self, value):
        super().__init__(value // 3)

class ImplicitTrisect(MyBaseClass):
    """
    目的：定义另一个隐式三分法类
    解释：调用父类的初始化方法并设置值。
    """
    def __init__(self, value):
        super().__init__(value // 3)

assert ExplicitTrisect(9).value == 3
assert AutomaticTrisect(9).value == 3
assert ImplicitTrisect(9).value == 3
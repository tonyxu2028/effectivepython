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
# 目的：定义一个类 MyObject
# 解释：定义一个类 MyObject，包含公有和私有字段。
# 结果：类 MyObject
print(f"\n{'Example 1':*^50}")
class MyObject:
    """
    目的：定义一个类 MyObject
    解释：包含公有和私有字段。
    """
    def __init__(self):
        self.public_field = 5
        self.__private_field = 10

    def get_private_field(self):
        """
        目的：获取私有字段
        解释：返回私有字段的值。
        """
        return self.__private_field


# Example 2
# 目的：创建 MyObject 对象并断言公有字段的值
# 解释：创建 MyObject 对象并断言公有字段的值。
# 结果：断言成功
print(f"\n{'Example 2':*^50}")
foo = MyObject()
assert foo.public_field == 5


# Example 3
# 目的：断言私有字段的值
# 解释：通过方法获取私有字段的值并断言。
# 结果：断言成功
print(f"\n{'Example 3':*^50}")
assert foo.get_private_field() == 10


# Example 4
# 目的：尝试直接访问私有字段并捕获异常
# 解释：尝试直接访问私有字段并捕获异常。
# 结果：捕获异常
print(f"\n{'Example 4':*^50}")
try:
    foo.__private_field
except:
    logging.exception('Expected')
else:
    assert False


# Example 5
# 目的：定义一个类 MyOtherObject
# 解释：定义一个类 MyOtherObject，包含私有字段和类方法。
# 结果：类 MyOtherObject
print(f"\n{'Example 5':*^50}")
class MyOtherObject:
    """
    目的：定义一个类 MyOtherObject
    解释：包含私有字段和类方法。
    """
    def __init__(self):
        self.__private_field = 71

    @classmethod
    def get_private_field_of_instance(cls, instance):
        """
        目的：获取实例的私有字段
        解释：返回实例的私有字段的值。
        """
        return instance.__private_field

bar = MyOtherObject()
assert MyOtherObject.get_private_field_of_instance(bar) == 71


# Example 6
# 目的：定义父类和子类并尝试访问私有字段
# 解释：定义父类和子类并尝试访问私有字段。
# 结果：捕获异常
print(f"\n{'Example 6':*^50}")
try:
    class MyParentObject:
        def __init__(self):
            self.__private_field = 71

    class MyChildObject(MyParentObject):
        def get_private_field(self):
            return self.__private_field

    baz = MyChildObject()
    baz.get_private_field()
except:
    logging.exception('Expected')
else:
    assert False


# Example 7
# 目的：通过名称改写访问私有字段
# 解释：通过名称改写访问私有字段。
# 结果：断言成功
print(f"\n{'Example 7':*^50}")
assert baz._MyParentObject__private_field == 71


# Example 8
# 目的：打印对象的字典表示
# 解释：打印对象的字典表示。
# 结果：打印成功
print(f"\n{'Example 8':*^50}")
print(baz.__dict__)


# Example 9
# 目的：定义一个类 MyStringClass
# 解释：定义一个类 MyStringClass，包含私有字段和方法。
# 结果：类 MyStringClass
print(f"\n{'Example 9':*^50}")
class MyStringClass:
    """
    目的：定义一个类 MyStringClass
    解释：包含私有字段和方法。
    """
    def __init__(self, value):
        self.__value = value

    def get_value(self):
        """
        目的：获取值
        解释：返回值的字符串表示。
        """
        return str(self.__value)

foo = MyStringClass(5)
assert foo.get_value() == '5'


# Example 10
# 目的：定义一个子类 MyIntegerSubclass
# 解释：定义一个子类 MyIntegerSubclass，重写方法。
# 结果：子类 MyIntegerSubclass
print(f"\n{'Example 10':*^50}")
class MyIntegerSubclass(MyStringClass):
    """
    目的：定义一个子类 MyIntegerSubclass
    解释：重写方法，返回整数值。
    """
    def get_value(self):
        return int(self._MyStringClass__value)

foo = MyIntegerSubclass('5')
assert foo.get_value() == 5


# Example 11
# 目的：定义一个基类 MyBaseClass 和子类
# 解释：定义一个基类 MyBaseClass 和子类，重写方法。
# 结果：基类和子类
print(f"\n{'Example 11':*^50}")
class MyBaseClass:
    """
    目的：定义一个基类 MyBaseClass
    解释：包含私有字段和方法。
    """
    def __init__(self, value):
        self.__value = value

    def get_value(self):
        """
        目的：获取值
        解释：返回私有字段的值。
        """
        return self.__value

class MyStringClass(MyBaseClass):
    """
    目的：定义一个子类 MyStringClass
    解释：重写方法，返回字符串值。
    """
    def get_value(self):
        return str(super().get_value())  # Updated

class MyIntegerSubclass(MyStringClass):
    """
    目的：定义一个子类 MyIntegerSubclass
    解释：重写方法，返回整数值。
    """
    def get_value(self):
        return int(self._MyStringClass__value)  # Not updated


# Example 12
# 目的：尝试创建子类对象并捕获异常
# 解释：尝试创建子类对象并捕获异常。
# 结果：捕获异常
print(f"\n{'Example 12':*^50}")
try:
    foo = MyIntegerSubclass(5)
    foo.get_value()
except:
    logging.exception('Expected')
else:
    assert False


# Example 13
# 目的：定义一个类 MyStringClass
# 解释：定义一个类 MyStringClass，包含公有字段和方法。
# 结果：类 MyStringClass
print(f"\n{'Example 13':*^50}")
class MyStringClass:
    """
    目的：定义一个类 MyStringClass
    解释：包含公有字段和方法。
    """
    def __init__(self, value):
        self._value = value

    def get_value(self):
        """
        目的：获取值
        解释：返回值。
        """
        return str(self._value)

class MyIntegerSubclass(MyStringClass):
    """
    目的：定义一个子类 MyIntegerSubclass
    解释：重写方法，返回整数值。
    """
    def get_value(self):
        return self._value

foo = MyIntegerSubclass(5)
assert foo.get_value() == 5


# Example 14
# 目的：定义一个类 ApiClass 和子类 Child
# 解释：定义一个类 ApiClass 和子类 Child，重写字段。
# 结果：类 ApiClass 和子类 Child
print(f"\n{'Example 14':*^50}")
class ApiClass:
    """
    目的：定义一个类 ApiClass
    解释：包含公有字段和方法。
    """
    def __init__(self):
        self._value = 5

    def get(self):
        """
        目的：获取值
        解释：返回值。
        """
        return self._value

class Child(ApiClass):
    """
    目的：定义一个子类 Child
    解释：重写字段。
    """
    def __init__(self):
        super().__init__()
        self._value = 'hello'  # Conflicts

a = Child()
print(f'{a.get()} and {a._value} should be different')


# Example 15
# 目的：定义一个类 ApiClass 和子类 Child
# 解释：定义一个类 ApiClass 和子类 Child，使用双下划线字段。
# 结果：类 ApiClass 和子类 Child
print(f"\n{'Example 15':*^50}")
class ApiClass:
    """
    目的：定义一个类 ApiClass
    解释：包含私有字段和方法。
    """
    def __init__(self):
        self.__value = 5  # Double underscore

    def get(self):
        """
        目的：获取值
        解释：返回私有字段的值。
        """
        return self.__value  # Double underscore

class Child(ApiClass):
    """
    目的：定义一个子类 Child
    解释：重写字段。
    """
    def __init__(self):
        super().__init__()
        self._value = 'hello'  # OK!

a = Child()
print(f'{a.get()} and {a._value} are different')
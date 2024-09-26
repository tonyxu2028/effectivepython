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
# 目的：定义一个类 Field
# 解释：定义一个类 Field，包含 __init__ 方法。
# 结果：类 Field
print(f"\n{'Example 1':*^50}")
class Field:
    """
    目的：定义一个类 Field
    解释：包含 __init__ 方法。
    """
    def __init__(self, name):
        self.name = name


# Example 2
# 目的：定义一个类 Customer
# 解释：定义一个类 Customer，包含 __init__ 方法。
# 结果：类 Customer
print(f"\n{'Example 2':*^50}")
class Customer:
    """
    目的：定义一个类 Customer
    解释：包含 __init__ 方法。
    """
    def __init__(self):
        self.first_name = 'First'
        self.last_name = 'Last'


# Example 3
# 目的：测试 Customer 类
# 解释：创建 Customer 对象并测试属性。
# 结果：属性测试成功
print(f"\n{'Example 3':*^50}")
cust = Customer()
print(f'Before: {cust.first_name!r} {cust.__dict__}')
cust.first_name = 'Euclid'
print(f'After:  {cust.first_name!r} {cust.__dict__}')


# Example 4
# 目的：定义一个类 Customer
# 解释：定义一个类 Customer，包含 __init__ 方法。
# 结果：类 Customer
print(f"\n{'Example 4':*^50}")
class Customer:
    """
    目的：定义一个类 Customer
    解释：包含 __init__ 方法。
    """
    def __init__(self):
        self.first_name = 'First'
        self.last_name = 'Last'


# Example 5
# 目的：定义一个类 Meta
# 解释：定义一个类 Meta，包含 __new__ 方法。
# 结果：类 Meta
print(f"\n{'Example 5':*^50}")
class Meta(type):
    """
    目的：定义一个类 Meta
    解释：包含 __new__ 方法。
    """
    def __new__(meta, name, bases, class_dict):
        return super().__new__(meta, name, bases, class_dict)


# Example 6
# 目的：定义一个类 DatabaseRow
# 解释：定义一个类 DatabaseRow，包含 __init__ 方法。
# 结果：类 DatabaseRow
print(f"\n{'Example 6':*^50}")
class DatabaseRow(metaclass=Meta):
    """
    目的：定义一个类 DatabaseRow
    解释：包含 __init__ 方法。
    """
    def __init__(self):
        self.first_name = 'First'
        self.last_name = 'Last'


# Example 7
# 目的：定义一个类 Field
# 解释：定义一个类 Field，包含 __init__ 方法。
# 结果：类 Field
print(f"\n{'Example 7':*^50}")
class Field:
    """
    目的：定义一个类 Field
    解释：包含 __init__ 方法。
    """
    def __init__(self, name):
        self.name = name


# Example 8
# 目的：定义一个类 BetterCustomer
# 解释：定义一个类 BetterCustomer，继承自 DatabaseRow。
# 结果：类 BetterCustomer
print(f"\n{'Example 8':*^50}")
class BetterCustomer(DatabaseRow):
    """
    目的：定义一个类 BetterCustomer
    解释：继承自 DatabaseRow。
    """
    def __init__(self):
        super().__init__()
        self.first_name = 'First'
        self.last_name = 'Last'


# Example 9
# 目的：测试 BetterCustomer 类
# 解释：创建 BetterCustomer 对象并测试属性。
# 结果：属性测试成功
print(f"\n{'Example 9':*^50}")
cust = BetterCustomer()
print(f'Before: {cust.first_name!r} {cust.__dict__}')
cust.first_name = 'Euler'
print(f'After:  {cust.first_name!r} {cust.__dict__}')


# Example 10
# 目的：测试异常处理
# 解释：测试异常处理机制。
# 结果：异常处理成功
print(f"\n{'Example 10':*^50}")
try:
    raise ValueError('This is an error')
except ValueError as e:
    logging.exception('Expected')
else:
    assert False


# Example 11
# 目的：定义一个类 Field
# 解释：定义一个类 Field，包含 __init__ 方法。
# 结果：类 Field
print(f"\n{'Example 11':*^50}")
class Field:
    """
    目的：定义一个类 Field
    解释：包含 __init__ 方法。
    """
    def __init__(self, name):
        self.name = name


# Example 12
# 目的：定义一个类 FixedCustomer
# 解释：定义一个类 FixedCustomer，包含 __init__ 方法。
# 结果：类 FixedCustomer
print(f"\n{'Example 12':*^50}")
class FixedCustomer:
    """
    目的：定义一个类 FixedCustomer
    解释：包含 __init__ 方法。
    """
    def __init__(self):
        self.first_name = 'First'
        self.last_name = 'Last'

cust = FixedCustomer()
print(f'Before: {cust.first_name!r} {cust.__dict__}')
cust.first_name = 'Mersenne'
print(f'After:  {cust.first_name!r} {cust.__dict__}')
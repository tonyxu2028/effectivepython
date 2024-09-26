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
    解释：遍历所有对象并关闭所有 io.IOBase 实例。
    结果：所有打开的文件都被关闭
    """
    everything = gc.get_objects()
    for obj in everything:
        if isinstance(obj, io.IOBase):
            obj.close()

atexit.register(close_open_files)


# Example 1
# 目的：测试 subtract 函数的异常处理
# 解释：定义一个 subtract 函数并传入错误类型的参数，捕获异常。
# 结果：成功捕获异常并记录日志
try:
    def subtract(a, b):
        """减法运算"""
        return a - b

    subtract(10, '5')
except:
    logging.exception('Expected')
else:
    assert False


# Example 3
# 目的：测试 concat 函数的异常处理
# 解释：定义一个 concat 函数并传入错误类型的参数，捕获异常。
# 结果：成功捕获异常并记录日志
try:
    def concat(a, b):
        """字符串连接"""
        return a + b

    concat('first', b'second')
except:
    logging.exception('Expected')
else:
    assert False


# Example 5
class Counter:
    """
    计数器类
    目的：定义一个计数器类
    解释：创建一个 Counter 类，包含增加和获取值的方法。
    结果：成功定义类并进行断言测试
    """
    def __init__(self):
        """初始化计数器"""
        self.value = 0

    def add(self, offset):
        """增加计数器的值"""
        self.value += offset

    def get(self) -> int:
        """获取计数器的值"""
        return self.value


# Example 6
# 目的：测试 Counter 类的 add 方法
# 解释：创建 Counter 实例并调用 add 方法，捕获异常。
# 结果：成功捕获异常并记录日志
try:
    counter = Counter()
    counter.add(5)
except:
    logging.exception('Expected')
else:
    assert False


# Example 7
# 目的：测试 Counter 类的 get 方法
# 解释：创建 Counter 实例并调用 get 方法，进行断言测试。
# 结果：成功调用方法并进行断言测试
try:
    counter = Counter()
    found = counter.get()
    assert found == 0, found
except:
    logging.exception('Expected')
else:
    assert False


# Example 9
# 目的：测试 combine 函数的异常处理
# 解释：定义一个 combine 函数并传入包含复数的列表，捕获异常。
# 结果：成功捕获异常并记录日志
try:
    def combine(func, values):
        """组合函数"""
        assert len(values) > 0

        result = values[0]
        for next_value in values[1:]:
            result = func(result, next_value)

        return result

    def add(x, y):
        """加法运算"""
        return x + y

    inputs = [1, 2, 3, 4j]
    result = combine(add, inputs)
    assert result == 10, result  # Fails
except:
    logging.exception('Expected')
else:
    assert False


# Example 11
# 目的：测试 get_or_default 函数的异常处理
# 解释：定义一个 get_or_default 函数并传入不同的参数，捕获异常。
# 结果：成功捕获异常并记录日志
try:
    def get_or_default(value, default):
        """获取值或默认值"""
        if value is not None:
            return value
        return default

    found = get_or_default(3, 5)
    assert found == 3

    found = get_or_default(None, 5)
    assert found == 5, found  # Fails
except:
    logging.exception('Expected')
else:
    assert False


# Example 13
class FirstClass:
    """
    第一个类
    目的：定义两个类并删除
    解释：创建 FirstClass 和 SecondClass 类的实例并删除类。
    结果：成功创建实例并删除类
    """
    def __init__(self, value):
        """初始化 FirstClass"""
        self.value = value

class SecondClass:
    """
    第二个类
    目的：定义两个类并删除
    解释：创建 FirstClass 和 SecondClass 类的实例并删除类。
    结果：成功创建实例并删除类
    """
    def __init__(self, value):
        """初始化 SecondClass"""
        self.value = value

second = SecondClass(5)
first = FirstClass(second)

del FirstClass
del SecondClass


# Example 15
# 目的：测试类的前向引用
# 解释：定义 FirstClass 和 SecondClass 类并进行前向引用，捕获异常。
# 结果：成功捕获异常并记录日志
try:
    class FirstClass:
        """
        第一个类
        目的：测试类的前向引用
        解释：定义 FirstClass 和 SecondClass 类并进行前向引用，捕获异常。
        结果：成功捕获异常并记录日志
        """
        def __init__(self, value: SecondClass) -> None:  # Breaks
            self.value = value

    class SecondClass:
        """
        第二个类
        目的：测试类的前向引用
        解释：定义 FirstClass 和 SecondClass 类并进行前向引用，捕获异常。
        结果：成功捕获异常并记录日志
        """
        def __init__(self, value: int) -> None:
            self.value = value

    second = SecondClass(5)
    first = FirstClass(second)
except:
    logging.exception('Expected')
else:
    assert False


# Example 16
class FirstClass:
    """
    第一个类
    目的：测试类的前向引用
    解释：定义 FirstClass 和 SecondClass 类并进行前向引用。
    结果：成功定义类并进行前向引用
    """
    def __init__(self, value: 'SecondClass') -> None:  # OK
        self.value = value

class SecondClass:
    """
    第二个类
    目的：测试类的前向引用
    解释：定义 FirstClass 和 SecondClass 类并进行前向引用。
    结果：成功定义类并进行前向引用
    """
    def __init__(self, value: int) -> None:
        self.value = value

second = SecondClass(5)
first = FirstClass(second)
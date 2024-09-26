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

# 复现书中的环境
import random
random.seed(1234)

import logging
from pprint import pprint
from sys import stdout as STDOUT

# 将所有输出写入临时目录
import atexit
import gc
import io
import os
import tempfile

TEST_DIR = tempfile.TemporaryDirectory()
atexit.register(TEST_DIR.cleanup)

# 确保 Windows 进程干净退出
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


# 示例 1
# 目的：打印字符串
# 解释：简单的打印字符串 'foo bar'。
# 结果：输出 'foo bar'
print('foo bar')


# 示例 2
# 目的：展示不同的字符串格式化方法
# 解释：使用不同的方法格式化并打印字符串。
# 结果：输出 'foo bar' 的不同格式化结果
my_value = 'foo bar'
print(str(my_value))
print('%s' % my_value)
print(f'{my_value}')
print(format(my_value))
print(my_value.__format__('s'))
print(my_value.__str__())


# 示例 3
# 目的：比较整数和字符串
# 解释：打印整数和字符串并比较它们。
# 结果：输出整数和字符串的比较结果
print(5)
print('5')

int_value = 5
str_value = '5'
print(f'{int_value} == {str_value} ?')


# 示例 4
# 目的：展示 repr 函数的使用
# 解释：使用 repr 函数打印字符串的表示形式。
# 结果：输出字符串的表示形式
a = '\x07'
print(repr(a))


# 示例 5
# 目的：使用 eval 函数
# 解释：使用 eval 函数评估字符串的表示形式并进行断言。
# 结果：断言成功
b = eval(repr(a))
assert a == b


# 示例 6
# 目的：展示 repr 函数的使用
# 解释：使用 repr 函数打印整数和字符串的表示形式。
# 结果：输出整数和字符串的表示形式
print(repr(5))
print(repr('5'))


# 示例 7
# 目的：使用 %r 格式化字符串
# 解释：使用 %r 格式化字符串并打印。
# 结果：输出格式化后的字符串
print('%r' % 5)
print('%r' % '5')

int_value = 5
str_value = '5'
print(f'{int_value!r} != {str_value!r}')


# 示例 8
# 目的：定义一个不透明类
# 解释：创建一个不透明类并打印其实例。
# 结果：输出类实例的默认表示形式
class OpaqueClass:
    """
    目的：定义一个不透明类
    解释：创建一个不透明类并打印其实例。
    结果：输出类实例的默认表示形式
    """
    def __init__(self, x, y):
        self.x = x
        self.y = y

obj = OpaqueClass(1, 'foo')
print(obj)


# 示例 9
# 目的：定义一个更好的类
# 解释：创建一个类并实现 __repr__ 方法。
# 结果：输出类实例的自定义表示形式
class BetterClass:
    """
    目的：定义一个更好的类
    解释：创建一个类并实现 __repr__ 方法。
    结果：输出类实例的自定义表示形式
    """
    def __init__(self, x, y):
        self.x = x
        self.y = y

    def __repr__(self):
        return f'BetterClass({self.x!r}, {self.y!r})'


# 示例 10
# 目的：打印 BetterClass 实例
# 解释：创建 BetterClass 的实例并打印。
# 结果：输出类实例的自定义表示形式
obj = BetterClass(2, 'bar')
print(obj)


# 示例 11
# 目的：打印类实例的字典表示
# 解释：创建 OpaqueClass 的实例并打印其 __dict__ 属性。
# 结果：输出类实例的字典表示
obj = OpaqueClass(4, 'baz')
print(obj.__dict__)
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

# 军规 24: Use None and Docstrings to Specify Dynamic Default Arguments
# 军规 24: 使用 None 和文档字符串来指定动态默认参数

"""
Use None and Docstrings to Specify Dynamic Default Arguments
使用 None 和文档字符串来指定动态默认参数
"""

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
    everything = gc.get_objects()
    for obj in everything:
        if isinstance(obj, io.IOBase):
            obj.close()

atexit.register(close_open_files)


# Example 1 --- 错误使用可变默认参数
# 目的：展示如何错误地使用动态数据（如 datetime.now()）作为默认参数。
# 解释：
# log 函数使用 datetime.now() 作为默认参数，导致当函数在不同时间被调用时，时间戳相同，因为默认参数只在函数定义时求值一次。
# 结果：两次调用的时间戳相同，虽然有延迟。
print(f"\n{'Example 1':*^50}")
from time import sleep
from datetime import datetime

def log(message, when=datetime.now()):
    print(f'{when}: {message}')

log('Hi there!')
sleep(0.1)
log('Hello again!')


# Example 2 --- 使用 None 指定动态默认参数
# 目的：展示如何通过将 None 作为默认值来实现动态参数。
# 解释：
# 通过将 when 参数的默认值设为 None，并在函数内部判断是否为 None 来执行动态操作（即在每次调用时使用当前时间）。
# 结果：每次调用 log 函数都会生成不同的时间戳。
print(f"\n{'Example 2':*^50}")
def log(message, when=None):
    """Log a message with a timestamp.

    Args:
        message: Message to print.
        when: datetime of when the message occurred.
            Defaults to the present time.
    """
    if when is None:
        when = datetime.now()
    print(f'{when}: {message}')


# Example 3 --- 动态参数正常工作
# 目的：展示改进后的 log 函数如何正确生成动态时间戳。
# 解释：
# 通过将默认参数设为 None，每次调用函数时都会使用当前时间。
# 结果：两次调用显示不同的时间戳。
print(f"\n{'Example 3':*^50}")
log('Hi there!')
sleep(0.1)
log('Hello again!')


# Example 4 --- 使用可变对象作为默认参数
# 目的：展示在默认参数中使用可变对象（如字典）可能导致的错误。
# 解释：
# decode 函数使用一个空字典作为默认值，这导致每次调用 decode 时都返回同一个字典实例。
# 结果：不同的调用共用同一个字典对象，导致数据混乱。
print(f"\n{'Example 4':*^50}")
import json

def decode(data, default={}):
    try:
        return json.loads(data)
    except ValueError:
        return default


# Example 5 --- 调用 decode 函数并修改结果
# 目的：展示使用可变默认参数时导致的错误行为。
# 解释：
# 两次调用 decode 函数时，返回的字典是同一个对象，修改 foo 也会影响 bar。
# 结果：输出的 foo 和 bar 共享了同一个字典，导致混乱。
print(f"\n{'Example 5':*^50}")
foo = decode('bad data')
foo['stuff'] = 5
bar = decode('also bad')
bar['meep'] = 1
print('Foo:', foo)
print('Bar:', bar)


# Example 6 --- 断言 foo 和 bar 是同一个对象
# 目的：展示 foo 和 bar 实际上是同一个对象。
# 解释：
# 使用 assert 语句验证 foo 和 bar 是同一个字典实例。
# 结果：断言通过，说明两次调用返回的是同一个字典。
print(f"\n{'Example 6':*^50}")
assert foo is bar


# Example 7 --- 使用 None 解决可变默认参数问题
# 目的：展示如何通过将默认参数设为 None 来避免共用可变对象。
# 解释：
# decode 函数的默认参数设为 None，若出现解码错误则在函数内部创建新的字典对象，避免共用同一个对象。
# 结果：每次调用 decode 函数都会返回不同的字典对象。
print(f"\n{'Example 7':*^50}")
def decode(data, default=None):
    """Load JSON data from a string.

    Args:
        data: JSON data to decode.
        default: Value to return if decoding fails.
            Defaults to an empty dictionary.
    """
    try:
        return json.loads(data)
    except ValueError:
        if default is None:
            default = {}
        return default


# Example 8 --- 调用 decode 函数并修改结果
# 目的：展示使用 None 作为默认参数后，如何避免数据共享问题。
# 解释：
# 通过为 default 参数提供 None，确保每次 decode 出错时都会创建一个新的字典。
# 结果：foo 和 bar 不再共享同一个字典实例。
print(f"\n{'Example 8':*^50}")
foo = decode('bad data')
foo['stuff'] = 5
bar = decode('also bad')
bar['meep'] = 1
print('Foo:', foo)
print('Bar:', bar)
assert foo is not bar

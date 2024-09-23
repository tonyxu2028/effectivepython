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

# 军规 20: Know How Closures Interact with Variable Scope
# 军规 20: 理解闭包如何与变量作用域交互

"""
Know How Closures Interact with Variable Scope
理解闭包如何与变量作用域交互
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


# Example 1 --- 初步处理异常的除法函数
# 目的：展示如何使用 try-except 捕获异常，处理除零的情况。
# 解释：
# careful_divide 函数尝试除法运算，若发生 ZeroDivisionError 则返回 None。
# 结果：处理不同的除法情况，若除零则返回 None。
print(f"\n{'Example 1':*^50}")
def careful_divide(a, b):
    try:
        return a / b
    except ZeroDivisionError:
        return None

assert careful_divide(4, 2) == 2
assert careful_divide(0, 1) == 0
assert careful_divide(3, 6) == 0.5
assert careful_divide(1, 0) == None


# Example 2 --- 检查结果是否为 None
# 目的：展示如何通过检查函数返回值为 None 来判断输入是否有效。
# 解释：
# 通过检查 careful_divide 的返回值是否为 None 来判断输入的有效性，若为 None 则表示除零错误。
# 结果：根据除法结果输出对应的消息。
print(f"\n{'Example 2':*^50}")
x, y = 1, 0
result = careful_divide(x, y)
if result is None:
    print('Invalid inputs')
else:
    print('Result is %.1f' % result)


# Example 3 --- 检查 False 值导致的误判
# 目的：展示如何直接使用 if 判断返回值可能导致误判。
# 解释：
# 因为 0 也被视作 False，因此直接使用 if 语句判断可能会误判合法的返回值。
# 结果：错误地将 0 视为无效输入。
print(f"\n{'Example 3':*^50}")
x, y = 0, 5
result = careful_divide(x, y)
if not result:
    print('Invalid inputs')  # This runs! But shouldn't
else:
    assert False


# Example 4 --- 使用元组返回成功标记和结果
# 目的：展示如何通过元组返回成功标记和计算结果来避免误判。
# 解释：
# careful_divide 函数返回一个元组，第一个元素表示运算是否成功，第二个元素为结果值。
# 结果：通过 success 标志来判断是否成功。
print(f"\n{'Example 4':*^50}")
def careful_divide(a, b):
    try:
        return True, a / b
    except ZeroDivisionError:
        return False, None

assert careful_divide(4, 2) == (True, 2)
assert careful_divide(0, 1) == (True, 0)
assert careful_divide(3, 6) == (True, 0.5)
assert careful_divide(1, 0) == (False, None)


# Example 5 --- 使用成功标志判断结果
# 目的：展示如何通过返回的成功标志来判断除法是否有效。
# 解释：
# 通过 careful_divide 返回的成功标志来判断输入是否有效。
# 结果：成功标志为 False 时，输出无效输入。
print(f"\n{'Example 5':*^50}")
x, y = 5, 0
success, result = careful_divide(x, y)
if not success:
    print('Invalid inputs')


# Example 6 --- 直接使用返回的结果判断
# 目的：展示如何忽略成功标志，直接使用返回的结果来判断。
# 解释：
# 直接检查 careful_divide 返回的结果是否为 None 来判断除法是否有效。
# 结果：若结果为 None，输出无效输入。
print(f"\n{'Example 6':*^50}")
x, y = 5, 0
_, result = careful_divide(x, y)
if not result:
    print('Invalid inputs')


# Example 7 --- 引发自定义异常
# 目的：展示如何通过引发自定义异常来处理无效输入。
# 解释：
# 当发生 ZeroDivisionError 时，通过 raise 引发自定义的 ValueError，指示无效输入。
# 结果：处理无效输入时抛出 ValueError。
print(f"\n{'Example 7':*^50}")
def careful_divide(a, b):
    try:
        return a / b
    except ZeroDivisionError as e:
        raise ValueError('Invalid inputs')


# Example 8 --- 捕获自定义异常
# 目的：展示如何捕获自定义异常并处理无效输入。
# 解释：
# 调用 careful_divide 时捕获自定义的 ValueError 异常，并根据异常输出无效输入消息。
# 结果：处理无效输入时捕获并输出错误信息。
print(f"\n{'Example 8':*^50}")
x, y = 5, 2
try:
    result = careful_divide(x, y)
except ValueError:
    print('Invalid inputs')
else:
    print('Result is %.1f' % result)


# Example 9 --- 使用类型提示和文档字符串
# 目的：展示如何使用类型提示和文档字符串为函数添加额外的说明。
# 解释：
# careful_divide 函数使用类型提示指示参数和返回值的类型，并在文档字符串中说明异常的引发情况。
# 结果：除零时引发自定义的 ValueError，并通过 assert 进行异常测试。
print(f"\n{'Example 9':*^50}")
def careful_divide(a: float, b: float) -> float:
    """Divides a by b.

    Raises:
        ValueError: When the inputs cannot be divided.
    """
    try:
        return a / b
    except ZeroDivisionError as e:
        raise ValueError('Invalid inputs')

try:
    result = careful_divide(1, 0)
    assert False
except ValueError:
    pass  # Expected

assert careful_divide(1, 5) == 0.2

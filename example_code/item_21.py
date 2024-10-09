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

# 军规 21: Know How Closures Interact with Variable Scope
# 军规 21: 理解闭包如何与变量作用域交互

"""
军规 21: Know How Closures Interact with Variable Scope
军规 21: 理解闭包如何与变量作用域交互
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


# Example 1 --- 使用闭包进行排序
# 目的：展示如何通过嵌套函数（闭包）对列表进行排序。
# 解释：
# sort_priority 函数通过 helper 闭包，根据元素是否属于 group 进行排序，属于 group 的元素优先。
# 结果：对 numbers 列表进行排序，优先排序 group 中的元素。
print(f"\n{'Example 1':*^50}")
def sort_priority(values, group):
    def helper(x):
        if x in group:
            return (0, x)
        return (1, x)
    values.sort(key=helper)


# Example 2 --- 调用闭包排序函数
# 目的：展示如何调用 sort_priority 函数对列表进行排序。
# 解释：
# numbers 列表将根据 group 中的元素优先排序，属于 group 的元素优先排列在前。
# 结果：排序后的 numbers 列表。
print(f"\n{'Example 2':*^50}")
numbers = [8, 3, 1, 2, 5, 4, 7, 6]
group = {2, 3, 5, 7}
sort_priority(numbers, group)
print(numbers)


# Example 3 --- 闭包对外部作用域的影响
# 目的：展示闭包如何无法影响外部作用域中的变量。
# 解释：
# helper 闭包尝试修改外部作用域中的 found 变量，但由于作用域问题，修改不会生效。
# 结果：found 变量仍为 False，排序结果仍然正确。
print(f"\n{'Example 3':*^50}")
def sort_priority2(numbers, group):
    found = False
    def helper(x):
        if x in group:
            found = True  # Seems simple
            return (0, x)
        return (1, x)
    numbers.sort(key=helper)
    return found


# Example 4 --- 调用闭包并返回标志变量
# 目的：展示如何通过 sort_priority2 函数进行排序，并返回 found 标志变量。
# 解释：
# 虽然在 helper 中修改了 found，但由于作用域问题，返回的 found 仍为 False。
# 结果：输出排序后的列表及 found 的值（False）。
print(f"\n{'Example 4':*^50}")
numbers = [8, 3, 1, 2, 5, 4, 7, 6]
found = sort_priority2(numbers, group)
print('Found:', found)
print(numbers)


# Example 5 --- 捕获意料之外的异常
# 目的：展示如何捕获代码中预期发生的异常。
# 解释：
# 代码尝试使用未定义的变量（does_not_exist），会触发 NameError 异常，并被捕获。
# 结果：记录异常日志。
print(f"\n{'Example 5':*^50}")
try:
    foo = does_not_exist * 5
except:
    logging.exception('Expected')
else:
    assert False


# Example 6 --- 闭包变量作用域问题
# 目的：展示闭包修改外部变量时的作用域问题。
# 解释：
# helper 尝试修改外部作用域中的 found 变量，但由于作用域限制，修改不会生效。
# 结果：返回的 found 变量仍为 False。
print(f"\n{'Example 6':*^50}")
def sort_priority2(numbers, group):
    found = False         # Scope: 'sort_priority2'
    def helper(x):
        if x in group:
            found = True  # Scope: 'helper' -- Bad!
            return (0, x)
        return (1, x)
    numbers.sort(key=helper)
    return found


# Example 7 --- 使用 nonlocal 解决作用域问题
# 目的：展示如何通过 nonlocal 关键字解决闭包修改外部变量的作用域问题。
# 解释：
# nonlocal 关键字允许在闭包中修改外部作用域的变量。
# 结果：排序时正确修改 found 变量并返回 True。
print(f"\n{'Example 7':*^50}")
def sort_priority3(numbers, group):
    found = False
    def helper(x):
        nonlocal found  # Added
        if x in group:
            found = True
            return (0, x)
        return (1, x)
    numbers.sort(key=helper)
    return found


# Example 8 --- 调用 sort_priority3 并正确返回 found 标志
# 目的：展示通过 sort_priority3 函数正确排序并返回 found 标志。
# 解释：
# 通过 nonlocal 关键字，helper 函数正确修改了外部作用域中的 found 变量。
# 结果：found 变量为 True，排序后的列表正确。
print(f"\n{'Example 8':*^50}")
numbers = [8, 3, 1, 2, 5, 4, 7, 6]
found = sort_priority3(numbers, group)
assert found
assert numbers == [2, 3, 5, 7, 1, 4, 6, 8]


# Example 9 --- 使用类解决闭包问题
# 目的：展示如何通过类和 __call__ 方法代替闭包进行变量修改。
# 解释：
# Sorter 类通过 __call__ 方法实现与闭包相似的行为，并通过实例变量正确维护 found 状态。
# 结果：found 变量为 True，排序后的列表正确。
print(f"\n{'Example 9':*^50}")
numbers = [8, 3, 1, 2, 5, 4, 7, 6]
class Sorter:
    def __init__(self, group):
        self.group = group
        self.found = False

    def __call__(self, x):
        if x in self.group:
            self.found = True
            return (0, x)
        return (1, x)

sorter = Sorter(group)
numbers.sort(key=sorter)
assert sorter.found is True
assert numbers == [2, 3, 5, 7, 1, 4, 6, 8]

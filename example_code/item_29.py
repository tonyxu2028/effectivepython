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

# 军规 29: Avoid Repeated Work in Comprehensions by Using Assignment Expressions
# 军规 29: 使用赋值表达式在推导中避免重复代码 111

"""
# 军规 29: Avoid Repeated Work in Comprehensions by Using Assignment Expressions
# 军规 29: 在推导式中使用赋值表达式，避免重复计算 111

关键点: 其实就是用赋值表达式来避免重复计算，提高代码的可读性和性能。
例子: 海象操作符 := 避免重复调用 len()
避免在推导式内多次计算同一结果，用海象操作符把值存到变量里，再在后续逻辑中直接透传使用。
"""

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
    everything = gc.get_objects()
    for obj in everything:
        if isinstance(obj, io.IOBase):
            obj.close()

atexit.register(close_open_files)


# Example 1 --- 计算批次
# 目的：计算每种物品可以分成多少批
# 结果：输出可以分成的批次数。
print(f"\n{'Example 1':*^50}")
stock = {
    'nails': 125,
    'screws': 35,
    'wingnuts': 8,
    'washers': 24,
}

order = ['screws', 'wingnuts', 'clips']

def get_batches(count, size):
    return count // size

result = {}
for name in order:
    count = stock.get(name, 0)
    batches = get_batches(count, 8)
    if batches:
        result[name] = batches

print(result)


# Example 2 --- 使用字典推导式
# 目的：使用字典推导式计算每种物品的批次数
# 结果：输出符合条件的字典。
print(f"\n{'Example 2':*^50}")
found = {name: get_batches(stock.get(name, 0), 8)
         for name in order
         if get_batches(stock.get(name, 0), 8)}
print(found)


# Example 3 --- 计算批次的另一种方式
# 目的：展示另一种计算批次的方法
# 结果：输出符合条件的字典。
print(f"\n{'Example 3':*^50}")
has_bug = {name: get_batches(stock.get(name, 0), 4)
           for name in order
           if get_batches(stock.get(name, 0), 8)}

print('Expected:', found)
print('Found:   ', has_bug)


# Example 4 --- 使用赋值表达式
# 目的：使用赋值表达式简化代码
# 结果：验证结果是否正确。
print(f"\n{'Example 4':*^50}")
found = {name: batches for name in order
         if (batches := get_batches(stock.get(name, 0), 8))}
assert found == {'screws': 4, 'wingnuts': 1}, found


# Example 5 --- 赋值表达式错误示例
# 目的：展示不当使用赋值表达式时的错误
# 结果：抛出异常并记录日志。
print(f"\n{'Example 5':*^50}")
try:
    result = {name: (tenth := count // 10)
              for name, count in stock.items() if tenth > 0}
except:
    logging.exception('Expected')
else:
    assert False


# Example 6 --- 正确使用赋值表达式
# 目的：使用赋值表达式正确计算物品数量
# 结果：输出符合条件的字典。
print(f"\n{'Example 6':*^50}")
result = {name: tenth for name, count in stock.items()
          if (tenth := count // 10) > 0}
print(result)


# Example 7 --- 使用赋值表达式
# 目的：展示在列表推导式中使用赋值表达式
# 结果：输出最后一项。
print(f"\n{'Example 7':*^50}")
half = [(last := count // 2) for count in stock.values()]
print(f'Last item of {half} is {last}')


# Example 8 --- 漏洞示例
# 目的：展示循环变量的泄漏问题
# 结果：输出最后一项。
print(f"\n{'Example 8':*^50}")
for count in stock.values():  # Leaks loop variable
    pass
print(f'Last item of {list(stock.values())} is {count}')


# Example 9 --- 赋值表达式和异常
# 目的：展示循环变量不会泄漏
# 结果：抛出异常并记录日志。
print(f"\n{'Example 9':*^50}")
try:
    del count
    half = [count // 2 for count in stock.values()]
    print(half)   # Works
    print(count)  # Exception because loop variable didn't leak
except:
    logging.exception('Expected')
else:
    assert False


# Example 10 --- 使用生成器表达式
# 目的：展示生成器表达式的用法
# 结果：输出生成器的下一个元素。
print(f"\n{'Example 10':*^50}")
found = ((name, batches) for name in order
         if (batches := get_batches(stock.get(name, 0), 8)))
print(next(found))
print(next(found))

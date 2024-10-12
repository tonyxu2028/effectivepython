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

# 军规 27: Use Comprehensions Instead of map and filter.
# 军规 27: 使用推导取代 map 和 filter

"""
# 军规 27: Use Comprehensions Instead of map and filter.
# 军规 27: 使用推导取代 map 和 filter
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


# Example 1 --- 使用循环生成平方列表
# 目的：展示传统方法生成平方列表的方式。
# 结果：输出列表中每个元素的平方。
print(f"\n{'Example 1':*^50}")
a = [1, 2, 3, 4, 5, 6, 7, 8, 9, 10]
squares = []
for x in a:
    squares.append(x**2)
print(squares)


# Example 2 --- 列表推导式生成平方列表
# 目的：展示使用列表推导式生成平方列表的简洁方式。
# 结果：输出列表中每个元素的平方。
print(f"\n{'Example 2':*^50}")
squares = [x**2 for x in a]  # List comprehension
print(squares)


# Example 3 --- 使用 map 生成平方列表
# 目的：展示使用 map 函数生成平方列表的方式，并进行比较。
# 结果：确保 map 生成的结果与之前的列表相同。
print(f"\n{'Example 3':*^50}")
alt = map(lambda x: x ** 2, a)
assert list(alt) == squares, f'{alt} {squares}'


# Example 4 --- 列表推导式生成偶数平方列表
# 目的：展示如何使用列表推导式筛选偶数并生成其平方。
# 结果：输出列表中偶数元素的平方。
print(f"\n{'Example 4':*^50}")
even_squares = [x**2 for x in a if x % 2 == 0]
print(even_squares)


# Example 5 --- 使用 map 和 filter 生成偶数平方列表
# 目的：展示使用 map 和 filter 结合生成偶数平方的方式。
# 结果：确保 filter 和 map 组合的结果与之前的列表相同。
print(f"\n{'Example 5':*^50}")
alt = map(lambda x: x**2, filter(lambda x: x % 2 == 0, a))
assert even_squares == list(alt)


# Example 6 --- 使用字典推导式和集合推导式
# 目的：展示如何使用字典推导式和集合推导式。
# 结果：输出偶数平方的字典和可被3整除的数的立方的集合。
print(f"\n{'Example 6':*^50}")
even_squares_dict = {x: x**2 for x in a if x % 2 == 0}      # 字段推导式
threes_cubed_set = {x**3 for x in a if x % 3 == 0}          # 集合推导式
print(even_squares_dict)
print(threes_cubed_set)


# Example 7 --- 使用 map 和 filter 生成字典和集合
# 目的：展示如何使用 map 和 filter 组合生成字典和集合，并进行比较。
# 结果：确保字典和集合的结果与之前的推导式相同。
print(f"\n{'Example 7':*^50}")
alt_dict = dict(map(lambda x: (x, x**2),
                    filter(lambda x: x % 2 == 0, a)))       # 字典推导式
alt_set = set(map(lambda x: x**3,
                   filter(lambda x: x % 3 == 0, a)))        # 集合推导式
assert even_squares_dict == alt_dict
assert threes_cubed_set == alt_set
print(alt_dict)
print(alt_set)

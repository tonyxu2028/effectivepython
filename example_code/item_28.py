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

# 军规 28: 用列表推导式代替嵌套循环
# 军规 28: Use list comprehensions instead of nested loops

"""
Use list comprehensions instead of nested loops
用列表推导式代替嵌套循环
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


# Example 1 --- 将二维数组扁平化
# 目的：将一个二维矩阵扁平化为一维列表
# 结果：输出扁平化后的列表。
print(f"\n{'Example 1':*^50}")
matrix = [[1, 2, 3], [4, 5, 6], [7, 8, 9]]
flat = [x for row in matrix for x in row]
print(flat)


# Example 2 --- 将二维数组中的元素平方
# 目的：将每个元素平方并保持二维结构
# 结果：输出平方后的二维列表。
print(f"\n{'Example 2':*^50}")
squared = [[x**2 for x in row] for row in matrix]
print(squared)


# Example 3 --- 扁平化多层嵌套列表
# 目的：将多层嵌套的列表扁平化
# 结果：输出扁平化后的列表。
print(f"\n{'Example 3':*^50}")
my_lists = [
    [[1, 2, 3], [4, 5, 6]],
    [[7, 8, 9], [10, 11, 12]],
]
flat = [x for sublist1 in my_lists
        for sublist2 in sublist1
        for x in sublist2]
print(flat)


# Example 4 --- 使用循环扩展列表
# 目的：使用嵌套循环将多层嵌套的列表扁平化
# 结果：输出扁平化后的列表。
print(f"\n{'Example 4':*^50}")
flat = []
for sublist1 in my_lists:
    for sublist2 in sublist1:
        flat.extend(sublist2)
print(flat)


# Example 5 --- 使用条件生成列表
# 目的：展示使用多个条件生成列表的效果
# 结果：输出符合条件的列表。
print(f"\n{'Example 5':*^50}")
a = [1, 2, 3, 4, 5, 6, 7, 8, 9, 10]
b = [x for x in a if x > 4 if x % 2 == 0]
c = [x for x in a if x > 4 and x % 2 == 0]
print(b)
print(c)
assert b and c
assert b == c


# Example 6 --- 使用条件过滤二维数组
# 目的：展示如何根据条件过滤二维数组
# 结果：输出符合条件的二维数组。
print(f"\n{'Example 6':*^50}")
filtered = [[x for x in row if x % 3 == 0]
            for row in matrix if sum(row) >= 10]
print(filtered)

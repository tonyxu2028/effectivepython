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

"""
Prefer zip and enumerate Over range and index
优先使用 zip 和 enumerate 代替 range 和索引进行迭代
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


# Example 1 --- 生成名字长度的列表
# 目的：演示如何通过列表推导式计算每个名字的长度。
# 解释：
# names 是一个包含名字的字符串列表。
# counts 是一个列表推导式，计算 names 中每个名字的长度。
# 结果：输出一个包含名字长度的列表，比如：
# [7, 4, 5]  # Cecilia 长度 7，Lise 长度 4，Marie 长度 5
print(f"\n{'Example 1':*^50}")
names = ['Cecilia', 'Lise', 'Marie']
counts = [len(n) for n in names]
print(counts)


# Example 2 --- 通过索引遍历查找最长名字
# 目的：演示如何通过索引遍历两个列表，查找长度最长的名字。
# 解释：
# longest_name 和 max_count 初始化为 None 和 0，用于保存最长名字及其长度。
# 通过索引 i 遍历 names 和 counts 列表，找到最长的名字。
# 结果：输出最长的名字，比如：
# Cecilia
print(f"\n{'Example 2':*^50}")
longest_name = None
max_count = 0
for i in range(len(names)):
    count = counts[i]
    if count > max_count:
        longest_name = names[i]
        max_count = count
print(longest_name)


# Example 3 --- 使用 enumerate() 遍历列表
# 目的：演示如何使用 enumerate() 通过索引和元素同时遍历列表。
# 解释：
# 使用 enumerate() 遍历 names 列表，i 是索引，name 是元素。
# count = counts[i] 获取 names 对应的名字长度，找到最长的名字。
# 结果：验证 longest_name 是否为 Cecilia。
print(f"\n{'Example 3':*^50}")
longest_name = None
max_count = 0
for i, name in enumerate(names):
    count = counts[i]
    if count > max_count:
        longest_name = name
        max_count = count
print(longest_name)
assert longest_name == 'Cecilia'


# Example 4 --- 使用 zip() 同时遍历两个列表
# 目的：演示如何使用 zip() 同时遍历 names 和 counts 两个列表。
# 解释：
# 使用 zip(names, counts) 将两个列表打包成元组，分别获取名字和对应长度。
# 通过比较 count，找到最长的名字。
# 结果：验证 longest_name 是否为 Cecilia。
print(f"\n{'Example 4':*^50}")
longest_name = None
max_count = 0
for name, count in zip(names, counts):
    if count > max_count:
        longest_name = name
        max_count = count
assert longest_name == 'Cecilia'


# Example 5 --- zip() 遍历时列表长度不一致的情况
# 目的：演示当 zip() 遍历的两个列表长度不一致时的行为。
# 解释：
# names 列表追加了 'Rosalind'，而 counts 列表长度不变。
# zip(names, counts) 只会遍历到较短的列表为止。
# 结果：输出前 3 个名字，比如：
# Cecilia
# Lise
# Marie
print(f"\n{'Example 5':*^50}")
names.append('Rosalind')
for name, count in zip(names, counts):
    print(name)


# Example 6 --- 使用 itertools.zip_longest() 处理长度不一致的情况
# 目的：演示如何使用 itertools.zip_longest() 来处理两个列表长度不一致的情况。
# 解释：
# itertools.zip_longest(names, counts) 可以在两个列表长度不一致时继续遍历，短的列表会使用 None 补齐。
# 结果：输出每个名字及其长度，比如：
# Cecilia: 7
# Lise: 4
# Marie: 5
# Rosalind: None  # counts 中没有对应的长度，所以为 None
print(f"\n{'Example 6':*^50}")
import itertools

for name, count in itertools.zip_longest(names, counts):
    print(f'{name}: {count}')

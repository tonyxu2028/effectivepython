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
Prefer enumerate Over range
使用 enumerate 代替 range
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


# Example 1 --- 生成随机的 32 位二进制数
# 目的：演示如何通过位运算生成一个随机的 32 位二进制数。
# 解释：
# random_bits = 0 初始化一个全为 0 的整数，准备通过随机位操作生成一个随机数。
# for i in range(32) 循环 32 次，表示我们要生成一个 32 位数。
# randint(0, 1) 随机生成 0 或 1，决定是否设置当前位为 1。
# 1 << i 将数字 1 左移 i 位，表示要在第 i 位上放置一个 1。
# random_bits |= 1 << i 使用按位或操作符 |=，将 1 << i 对应位置的 1 添加到 random_bits 中。
# 结果：输出的是一个随机生成的 32 位二进制数，比如：0b11010011010101111001100111001110。
from random import randint
print(f"\n{'Example 1':*^50}")
random_bits = 0
for i in range(32):
    if randint(0, 1):
        random_bits |= 1 << i
print(bin(random_bits))


# Example 2 --- 遍历并打印列表元素
# 目的：演示如何遍历列表并打印其中的元素。
# 解释：
# flavor_list 是一个包含 4 种口味的字符串列表。
# for flavor in flavor_list 逐一遍历 flavor_list 中的元素，并将其赋值给 flavor。
# print(f'{flavor} is delicious') 打印每种口味，并附上 "is delicious"。
# 结果：依次打印每种口味和它的描述，比如：
# vanilla is delicious
# chocolate is delicious
# pecan is delicious
# strawberry is delicious
print(f"\n{'Example 2':*^50}")
flavor_list = ['vanilla', 'chocolate', 'pecan', 'strawberry']
for flavor in flavor_list:
    print(f'{flavor} is delicious')


# Example 3 --- 使用索引遍历并打印列表元素
# 目的：演示如何通过索引遍历列表，并打印元素和其对应的索引。
# 解释：
# for i in range(len(flavor_list)) 创建了一个索引范围，i 是 flavor_list 的索引。
# flavor = flavor_list[i] 通过索引 i 访问列表中的元素。
# print(f'{i + 1}: {flavor}') 打印索引（加 1，使其从 1 开始）和对应的元素。
# 结果：输出将每种口味按照它们在列表中的位置列出：
# 1: vanilla
# 2: chocolate
# 3: pecan
# 4: strawberry
print(f"\n{'Example 3':*^50}")
for i in range(len(flavor_list)):
    flavor = flavor_list[i]
    print(f'{i + 1}: {flavor}')


# Example 4 --- 使用 enumerate 获取迭代器并手动提取
# 目的：展示如何使用 enumerate() 创建一个迭代器，并通过 next() 获取下一个元素。
# 解释：
# it = enumerate(flavor_list) 使用 enumerate() 将 flavor_list 生成一个迭代器，返回 (索引, 元素) 对。
# print(next(it)) 打印迭代器的下一个元素，next(it) 每次调用都会返回下一个 (索引, 元素) 对。
# 结果：只打印了前两个 (索引, 元素) 对，比如：
# (0, 'vanilla')
# (1, 'chocolate')
print(f"\n{'Example 4':*^50}")
it = enumerate(flavor_list)
print(next(it))
print(next(it))


# Example 5 --- 使用 enumerate 遍历并打印带索引的元素
# 目的：展示如何使用 enumerate() 通过索引和元素遍历列表。
# 解释：
# for i, flavor in enumerate(flavor_list) 使用 enumerate() 将 flavor_list 生成的 (索引, 元素) 对解包成 i 和 flavor。
# print(f'{i + 1}: {flavor}') 打印 i + 1 和对应的口味。
# 结果：输出结果类似于 Example 3，但更简洁，不需要手动使用索引，比如：
# 1: vanilla
# 2: chocolate
# 3: pecan
# 4: strawberry
print(f"\n{'Example 5':*^50}")
for i, flavor in enumerate(flavor_list):
    print(f'{i + 1}: {flavor}')


# Example 6 --- 使用 enumerate 设置起始索引遍历列表
# 目的：展示如何使用 enumerate() 设置起始索引值。
# 解释：
# for i, flavor in enumerate(flavor_list, 1) 使用 enumerate()，并将起始索引设置为 1（默认从 0 开始）。
# print(f'{i}: {flavor}') 打印索引 i 和对应的口味。
# 结果：输出和 Example 5 相同，但 enumerate() 从 1 开始计数，比如：
# 1: vanilla
# 2: chocolate
# 3: pecan
# 4: strawberry
print(f"\n{'Example 6':*^50}")
for i, flavor in enumerate(flavor_list, 1):
    print(f'{i}: {flavor}')

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

# 军规 30: Consider Generators Instead of Returning Lists
# 军规 30: 考虑使用生成器代替返回列表。

"""
# 军规 30: Consider Generators Instead of Returning Lists
# 军规 30: 考虑使用生成器代替返回列表。

军规总结:
列表适合小数据集：如果你明确知道所有数据量较小且需要一次性处理，可以返回列表。
生成器适用于大数据或流式处理：当数据量大、需要按需生成或是要处理无限序列时，生成器是更优雅的选择。
节省资源、提高性能：生成器通过惰性计算避免内存浪费，并且让代码更灵活、更简洁。

一句话：
生成器就像水流般按需提供数据，而列表则像一桶水，需要提前全部装满。
如果你需要轻巧灵活的操作，生成器无疑是更好的选择。
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


# Example 1 --- 索引单词
# 目的：通过空格索引文本中的单词
# 结果：返回单词的索引列表。
def index_words(text):
    result = []
    if text:
        result.append(0)
    for index, letter in enumerate(text):
        if letter == ' ':
            result.append(index + 1)
    return result


# Example 2 --- 使用函数
# 目的：索引一段文本中的单词
# 结果：输出前10个单词的索引。
address = 'Four score and seven years ago our fathers brought forth on this continent a new nation, conceived in liberty, and dedicated to the proposition that all men are created equal.'
result = index_words(address)
print(result[:10])


# Example 3 --- 生成器实现
# 目的：使用生成器索引文本中的单词
# 结果：返回索引的生成器。
def index_words_iter(text):
    if text:
        yield 0
    for index, letter in enumerate(text):
        if letter == ' ':
            yield index + 1


# Example 4 --- 获取生成器的值
# 目的：从生成器中获取单个索引
# 结果：输出生成器的前两个值。
it = index_words_iter(address)
print(next(it))
print(next(it))


# Example 5 --- 列表转换
# 目的：将生成器的所有值转换为列表
# 结果：输出前10个索引。
result = list(index_words_iter(address))
print(result[:10])


# Example 6 --- 索引文件内容
# 目的：通过文件句柄索引文件中的每一行
# 结果：返回每一行的起始偏移量。
def index_file(handle):
    offset = 0
    for line in handle:
        if line:
            yield offset
        for letter in line:
            offset += 1
            if letter == ' ':
                yield offset


# Example 7 --- 写入并读取文件
# 目的：将文本写入文件并读取索引
# 结果：输出文件前10个单词的索引。
address_lines = """Four score and seven years
ago our fathers brought forth on this
continent a new nation, conceived in liberty,
and dedicated to the proposition that all men
are created equal."""

with open('address.txt', 'w') as f:
    f.write(address_lines)

import itertools
with open('address.txt', 'r') as f:
    it = index_file(f)
    results = itertools.islice(it, 0, 10)
    print(list(results))

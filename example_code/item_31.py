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

# 军规 31: Be Defensive When Iterating Over Arguments
# 军规 31: 迭代参数时要保持防御性

"""
# 军规 31: Be Defensive When Iterating Over Arguments
# 军规 31: 迭代参数时要保持防御性
注意重点:
(1)其实关键点在于对传入参数信息本身，如果是不能改变的场景那么需要进行防御性编程，如果去不是，那其实是没有必要的。
(2)还要注意迭代器的特性，迭代器只能迭代一次，如果需要多次迭代，那么需要将迭代器转换为容器。
(3)将迭代器转换为容器是为了确保数据可以多次使用，但这也会带来内存的代价，所以需要权衡。
(4)这个是一种特殊的场景权衡，要看是不是出现需要反复迭代的场景出现，
如果出现了是可以进行生成器到容器的转换，坏处是牺牲了资源，但是这个是没有办法的，
因为生成器不能多次迭代导致的。
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


# Example 1 --- 规范化数字
# 目的：计算给定数字列表的百分比
# 结果：返回每个数字占总和的百分比。
def normalize(numbers):
    total = sum(numbers)
    result = []
    for value in numbers:
        percent = 100 * value / total
        result.append(percent)
    return result


# Example 2 --- 测试规范化
# 目的：使用示例数据进行测试
# 结果：输出每个数字的百分比。
visits = [15, 35, 80]
percentages = normalize(visits)
print(percentages)
assert sum(percentages) == 100.0


# Example 3 --- 从文件读取数据
# 目的：将数字写入文件
# 结果：创建包含数字的文本文件。
path = 'my_numbers.txt'
with open(path, 'w') as f:
    for i in (15, 35, 80):
        f.write('%d\n' % i)

def read_visits(data_path):
    with open(data_path) as f:
        for line in f:
            yield int(line)


# Example 4 --- 使用生成器读取数据
# 目的：从文件中读取数字并规范化
# 结果：输出每个数字的百分比。
it = read_visits('my_numbers.txt')
percentages = normalize(it)
print(percentages)


# Example 5 --- 生成器耗尽
# 目的：演示生成器只能迭代一次
# 结果：显示生成器已耗尽。
it = read_visits('my_numbers.txt')
print(list(it))
print(list(it))  # 已经耗尽


# Example 6 --- 复制迭代器
# 目的：在规范化中复制迭代器
# 结果：输出每个数字的百分比。
def normalize_copy(numbers):
    numbers_copy = list(numbers)  # 复制迭代器
    total = sum(numbers_copy)
    result = []
    for value in numbers_copy:
        percent = 100 * value / total
        result.append(percent)
    return result


# Example 7 --- 使用复制的迭代器
# 目的：测试复制迭代器的规范化
# 结果：输出每个数字的百分比。
it = read_visits('my_numbers.txt')
percentages = normalize_copy(it)
print(percentages)
assert sum(percentages) == 100.0


# Example 8 --- 使用函数获取迭代器
# 目的：使用提供的函数获取新的迭代器
# 结果：输出每个数字的百分比。
def normalize_func(get_iter):
    total = sum(get_iter())   # 新的迭代器
    result = []
    for value in get_iter():  # 新的迭代器
        percent = 100 * value / total
        result.append(percent)
    return result


# Example 9 --- 从文件中规范化
# 目的：从文件读取数字并规范化
# 结果：输出每个数字的百分比。
path = 'my_numbers.txt'
percentages = normalize_func(lambda: read_visits(path))
print(percentages)
assert sum(percentages) == 100.0


# Example 10 --- 自定义迭代器类
# 目的：创建一个可迭代的类
# 结果：能够从文件中读取数字。
class ReadVisits:
    def __init__(self, data_path):
        self.data_path = data_path

    def __iter__(self):
        with open(self.data_path) as f:
            for line in f:
                yield int(line)


# Example 11 --- 使用自定义迭代器
# 目的：从自定义迭代器读取数据并规范化
# 结果：输出每个数字的百分比。
visits = ReadVisits(path)
percentages = normalize(visits)
print(percentages)
assert sum(percentages) == 100.0


# Example 12 --- 防御性编程
# 目的：确保输入为容器而非迭代器
# 结果：抛出类型错误。
def normalize_defensive(numbers):
    if iter(numbers) is numbers:  # 这是一个迭代器 -- 不允许！
        raise TypeError('Must supply a container')
    total = sum(numbers)
    result = []
    for value in numbers:
        percent = 100 * value / total
        result.append(percent)
    return result

visits = [15, 35, 80]
normalize_defensive(visits)  # 无错误

it = iter(visits)
try:
    normalize_defensive(it)
except TypeError:
    pass
else:
    assert False


# Example 13 --- 使用Iterator检查类型
# 目的：确保输入为容器而非迭代器
# 结果：抛出类型错误。
from collections.abc import Iterator

def normalize_defensive(numbers):
    if isinstance(numbers, Iterator):  # 另一种检查方法
        raise TypeError('Must supply a container')
    total = sum(numbers)
    result = []
    for value in numbers:
        percent = 100 * value / total
        result.append(percent)
    return result

visits = [15, 35, 80]
normalize_defensive(visits)  # 无错误

it = iter(visits)
try:
    normalize_defensive(it)
except TypeError:
    pass
else:
    assert False


# Example 14 --- 测试防御性编程
# 目的：确保容器的输入正确
# 结果：测试各种情况确保正确性。
visits = [15, 35, 80]
percentages = normalize_defensive(visits)
assert sum(percentages) == 100.0

visits = ReadVisits(path)
percentages = normalize_defensive(visits)
assert sum(percentages) == 100.0


# Example 15 --- 捕获预期异常
# 目的：捕获类型错误
# 结果：记录错误信息。
try:
    visits = [15, 35, 80]
    it = iter(visits)
    normalize_defensive(it)
except:
    logging.exception('Expected')
else:
    assert False

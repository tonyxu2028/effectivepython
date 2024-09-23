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

# 军规 19: Unpack Elements from Iterables of Arbitrary Length
# 军规 19: 从任意长度的可迭代对象中解包元素

"""
Unpack Elements from Iterables of Arbitrary Length
从任意长度的可迭代对象中解包元素
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


# Example 1 --- 返回多个值
# 目的：展示如何通过函数返回多个值并解包这些值。
# 解释：
# get_stats 函数返回最小值和最大值，调用函数时可以通过解包接收多个返回值。
# 结果：输出最小值和最大值。
print(f"\n{'Example 1':*^50}")
def get_stats(numbers):
    minimum = min(numbers)
    maximum = max(numbers)
    return minimum, maximum

lengths = [63, 73, 72, 60, 67, 66, 71, 61, 72, 70]

minimum, maximum = get_stats(lengths)  # Two return values

print(f'Min: {minimum}, Max: {maximum}')


# Example 2 --- 解包多个返回值
# 目的：展示如何通过解包接收函数的多个返回值。
# 解释：
# 通过返回多个值并使用解包方式获取这些值，避免了单独访问每个值。
# 结果：验证解包的值是否正确。
print(f"\n{'Example 2':*^50}")
first, second = 1, 2
assert first == 1
assert second == 2

def my_function():
    return 1, 2

first, second = my_function()
assert first == 1
assert second == 2


# Example 3 --- 解包带有剩余元素的可迭代对象
# 目的：展示如何使用解包从一个可迭代对象中提取第一个、最后一个和剩余的中间元素。
# 解释：
# get_avg_ratio 函数返回缩放后的排序列表，通过解包获取列表中的第一个、最后一个和中间元素。
# 结果：输出最长和最短的比例。
print(f"\n{'Example 3':*^50}")
def get_avg_ratio(numbers):
    average = sum(numbers) / len(numbers)
    scaled = [x / average for x in numbers]
    scaled.sort(reverse=True)
    return scaled

longest, *middle, shortest = get_avg_ratio(lengths)

print(f'Longest:  {longest:>4.0%}')
print(f'Shortest: {shortest:>4.0%}')


# Example 4 --- 返回并解包统计数据
# 目的：展示如何返回并解包多个统计值，如最小值、最大值、平均值等。
# 解释：
# get_stats 返回多种统计数据（最小值、最大值、平均值、中位数、计数），调用时通过解包接收这些值。
# 结果：输出所有统计数据，并验证其正确性。
print(f"\n{'Example 4':*^50}")
def get_stats(numbers):
    minimum = min(numbers)
    maximum = max(numbers)
    count = len(numbers)
    average = sum(numbers) / count

    sorted_numbers = sorted(numbers)
    middle = count // 2
    if count % 2 == 0:
        lower = sorted_numbers[middle - 1]
        upper = sorted_numbers[middle]
        median = (lower + upper) / 2
    else:
        median = sorted_numbers[middle]

    return minimum, maximum, average, median, count

minimum, maximum, average, median, count = get_stats(lengths)

print(f'Min: {minimum}, Max: {maximum}')
print(f'Average: {average}, Median: {median}, Count {count}')

assert minimum == 60
assert maximum == 73
assert average == 67.5
assert median == 68.5
assert count == 10

# Verify odd count median
_, _, _, median, count = get_stats([1, 2, 3])
assert median == 2
assert count == 3


# Example 5 --- 解包顺序错误
# 目的：展示解包时顺序错误会导致的潜在问题。
# 解释：
# 解包时需要注意返回值的顺序，如果顺序错误，会导致不正确的结果。
# 结果：展示错误的解包顺序导致的意外情况。
print(f"\n{'Example 5':*^50}")
# Correct:
minimum, maximum, average, median, count = get_stats(lengths)

# Oops! Median and average swapped:
minimum, maximum, median, average, count = get_stats(lengths)


# Example 6 --- 多行解包
# 目的：展示如何将解包操作分多行进行。
# 解释：
# 当返回的值较多时，可以通过多行进行解包，保持代码的可读性。
# 结果：展示多行解包的不同写法。
print(f"\n{'Example 6':*^50}")
minimum, maximum, average, median, count = get_stats(
    lengths)

minimum, maximum, average, median, count = \
    get_stats(lengths)

(minimum, maximum, average,
 median, count) = get_stats(lengths)

(minimum, maximum, average, median, count
    ) = get_stats(lengths)

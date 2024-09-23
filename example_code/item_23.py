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

# 军规 23: Provide Optional Behavior with Keyword Arguments
# 军规 23: 使用关键字参数提供可选行为

"""
Provide Optional Behavior with Keyword Arguments
使用关键字参数提供可选行为
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


# Example 1 --- 基本函数使用位置参数
# 目的：展示如何通过位置参数调用函数。
# 解释：
# remainder 函数通过两个位置参数 number 和 divisor 计算余数。
# 结果：输出 20 除以 7 的余数。
print(f"\n{'Example 1':*^50}")
def remainder(number, divisor):
    return number % divisor

assert remainder(20, 7) == 6


# Example 2 --- 使用关键字参数调用函数
# 目的：展示如何使用关键字参数调用函数。
# 解释：
# remainder 函数可以通过关键字参数调用，使得参数顺序无关紧要。
# 结果：通过不同方式传递参数，计算结果相同。
print(f"\n{'Example 2':*^50}")
remainder(20, 7)
remainder(20, divisor=7)
remainder(number=20, divisor=7)
remainder(divisor=7, number=20)


# Example 3 --- 关键字参数与位置参数的冲突
# 目的：展示如何避免在使用关键字参数时出现语法错误。
# 解释：
# 在位置参数之后不能再使用位置参数（如 remainder(number=20, 7)），这会导致语法错误。
# 结果：捕获并记录该错误。
print(f"\n{'Example 3':*^50}")
try:
    # This will not compile
    source = """remainder(number=20, 7)"""
    eval(source)
except:
    logging.exception('Expected')
else:
    assert False


# Example 4 --- 位置参数和关键字参数的重复问题
# 目的：展示如何避免重复传递参数。
# 解释：
# 位置参数和关键字参数不能重复使用同一个参数名，如 remainder(20, number=7) 会导致冲突。
# 结果：捕获并记录该错误。
print(f"\n{'Example 4':*^50}")
try:
    remainder(20, number=7)
except:
    logging.exception('Expected')
else:
    assert False


# Example 5 --- 使用 **kwargs 解包字典参数
# 目的：展示如何使用 **kwargs 将字典参数解包并传递给函数。
# 解释：
# **my_kwargs 解包字典并将其作为关键字参数传递给 remainder 函数。
# 结果：通过字典解包的方式调用函数并获得正确的结果。
print(f"\n{'Example 5':*^50}")
my_kwargs = {
	'number': 20,
	'divisor': 7,
}
assert remainder(**my_kwargs) == 6


# Example 6 --- 部分解包字典并传递额外参数
# 目的：展示如何结合字典解包和额外的关键字参数调用函数。
# 解释：
# 通过 **kwargs 解包部分参数，剩余参数直接传递给函数，实现灵活调用。
# 结果：正确解包和传递参数。
print(f"\n{'Example 6':*^50}")
my_kwargs = {
	'divisor': 7,
}
assert remainder(number=20, **my_kwargs) == 6


# Example 7 --- 多个字典的解包与合并
# 目的：展示如何将多个字典解包并传递给函数。
# 解释：
# 通过 **my_kwargs 和 **other_kwargs 解包多个字典并合并成关键字参数传递给 remainder 函数。
# 结果：正确解包多个字典并传递参数。
print(f"\n{'Example 7':*^50}")
my_kwargs = {
	'number': 20,
}
other_kwargs = {
	'divisor': 7,
}
assert remainder(**my_kwargs, **other_kwargs) == 6


# Example 8 --- 使用 **kwargs 传递任意数量的关键字参数
# 目的：展示如何使用 **kwargs 接受并处理任意数量的关键字参数。
# 解释：
# print_parameters 函数使用 **kwargs 接收并打印任意数量的关键字参数。
# 结果：输出传入的关键字参数及其对应值。
print(f"\n{'Example 8':*^50}")
def print_parameters(**kwargs):
    for key, value in kwargs.items():
        print(f'{key} = {value}')

print_parameters(alpha=1.5, beta=9, gamma=4)


# Example 9 --- 函数使用位置参数
# 目的：展示如何通过位置参数计算流速。
# 解释：
# flow_rate 函数通过 weight_diff 和 time_diff 计算流速，单位为千克每秒。
# 结果：输出计算的流速。
print(f"\n{'Example 9':*^50}")
def flow_rate(weight_diff, time_diff):
    return weight_diff / time_diff

weight_diff = 0.5
time_diff = 3
flow = flow_rate(weight_diff, time_diff)
print(f'{flow:.3} kg per second')


# Example 10 --- 函数使用额外的参数
# 目的：展示如何通过额外的参数 period 计算不同时间段的流速。
# 解释：
# flow_rate 函数新增 period 参数，用于指定计算流速的时间段。
# 结果：根据不同的 period 计算流速。
print(f"\n{'Example 10':*^50}")
def flow_rate(weight_diff, time_diff, period):
    return (weight_diff / time_diff) * period


# Example 11 --- 调用 flow_rate 函数计算每秒流速
# 目的：展示如何使用 flow_rate 函数计算每秒的流速。
# 解释：
# 通过传入 period=1 计算每秒的流速。
# 结果：计算并输出每秒的流速。
print(f"\n{'Example 11':*^50}")
flow_per_second = flow_rate(weight_diff, time_diff, 1)


# Example 12 --- 使用默认参数提供可选行为
# 目的：展示如何通过默认参数提供可选的计算行为。
# 解释：
# flow_rate 函数新增 period 的默认值为 1，若调用时不提供 period，则默认计算每秒的流速。
# 结果：通过默认参数简化函数调用。
print(f"\n{'Example 12':*^50}")
def flow_rate(weight_diff, time_diff, period=1):
    return (weight_diff / time_diff) * period


# Example 13 --- 计算每秒和每小时的流速
# 目的：展示如何通过 period 参数计算不同时间段的流速。
# 解释：
# 通过传入不同的 period 参数，分别计算每秒和每小时的流速。
# 结果：输出每秒和每小时的流速。
print(f"\n{'Example 13':*^50}")
flow_per_second = flow_rate(weight_diff, time_diff)
flow_per_hour = flow_rate(weight_diff, time_diff, period=3600)
print(flow_per_second)
print(flow_per_hour)


# Example 14 --- 使用多个默认参数提供灵活行为
# 目的：展示如何通过多个默认参数提供灵活的计算行为。
# 解释：
# flow_rate 函数新增 units_per_kg 参数，用于转换单位（如从千克转换为磅）。
# 结果：通过 units_per_kg 和 period 提供更灵活的流速计算。
print(f"\n{'Example 14':*^50}")
def flow_rate(weight_diff, time_diff,
              period=1, units_per_kg=1):
    return ((weight_diff * units_per_kg) / time_diff) * period


# Example 15 --- 使用自定义单位计算每小时流速
# 目的：展示如何通过传入不同的 units_per_kg 参数计算自定义单位的流速。
# 解释：
# 通过传入 units_per_kg=2.2 将流速从千克转换为磅，并计算每小时的流速。
# 结果：输出每小时的流速（单位为磅）。
print(f"\n{'Example 15':*^50}")
pounds_per_hour = flow_rate(weight_diff, time_diff,
                            period=3600, units_per_kg=2.2)
print(pounds_per_hour)


# Example 16 --- 位置参数调用含有多个默认参数的函数
# 目的：展示如何通过位置参数调用含有多个默认参数的函数。
# 解释：
# 通过位置参数传入 period 和 units_per_kg 参数，计算流速。
# 结果：输出每小时的流速（单位为磅）。
print(f"\n{'Example 16':*^50}")
pounds_per_hour = flow_rate(weight_diff, time_diff, 3600, 2.2)
print(pounds_per_hour)

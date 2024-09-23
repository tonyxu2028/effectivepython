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

# 军规 14: Sort by Complex Criteria Using the key Parameter
# 军规 14: 使用 key 参数根据复杂标准排序

"""
Sort by Complex Criteria Using the key Parameter
使用 key 参数根据复杂标准排序
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


# Example 1 --- 简单数字排序
# 目的：演示对数字列表进行排序。
# 解释：
# numbers.sort() 直接对数字列表进行排序，默认升序排列。
# 结果：输出排序后的数字列表。
print(f"\n{'Example 1':*^50}")
numbers = [93, 86, 11, 68, 70]
numbers.sort()
print(numbers)


# Example 2 --- 创建一个自定义类 Tool
# 目的：展示如何定义一个类，并创建该类的实例列表。
# 解释：
# Tool 类包含 name 和 weight 属性，__repr__ 方法用于打印对象的详细信息。
# 结果：创建工具对象，并将其存入列表。
print(f"\n{'Example 2':*^50}")
class Tool:
    def __init__(self, name, weight):
        self.name = name
        self.weight = weight

    def __repr__(self):
        return f'Tool({self.name!r}, {self.weight})'

tools = [
    Tool('level', 3.5),
    Tool('hammer', 1.25),
    Tool('screwdriver', 0.5),
    Tool('chisel', 0.25),
]


# Example 3 --- 无法直接对自定义对象排序
# 目的：展示无法对没有定义比较方法的自定义类对象排序。
# 解释：
# tools.sort() 尝试对 Tool 对象进行排序，但 Tool 类没有定义排序的标准，导致 TypeError。
# 结果：捕获并记录异常信息。
print(f"\n{'Example 3':*^50}")
try:
    tools.sort()
except:
    logging.exception('Expected')
else:
    assert False


# Example 4 --- 使用 key 参数按名称排序
# 目的：展示如何使用 key 参数按对象的某个属性进行排序。
# 解释：
# tools.sort(key=lambda x: x.name) 根据工具的 name 属性对工具进行排序。
# 结果：输出按名称升序排序的工具列表。
print(f"\n{'Example 4':*^50}")
print('Unsorted:', repr(tools))
tools.sort(key=lambda x: x.name)
print('\nSorted:  ', tools)


# Example 5 --- 按重量排序
# 目的：展示如何使用 key 参数根据工具的重量排序。
# 解释：
# tools.sort(key=lambda x: x.weight) 按重量升序排序。
# 结果：输出按重量排序后的工具列表。
print(f"\n{'Example 5':*^50}")
tools.sort(key=lambda x: x.weight)
print('By weight:', tools)


# Example 6 --- 大小写敏感和不敏感排序
# 目的：展示如何对字符串进行大小写敏感和不敏感的排序。
# 解释：
# places.sort() 默认大小写敏感，places.sort(key=lambda x: x.lower()) 忽略大小写。
# 结果：输出大小写敏感和不敏感的排序结果。
print(f"\n{'Example 6':*^50}")
places = ['home', 'work', 'New York', 'Paris']
places.sort()
print('Case sensitive:  ', places)
places.sort(key=lambda x: x.lower())
print('Case insensitive:', places)


# Example 7 --- 创建电动工具列表
# 目的：创建一个新的工具列表用于后续的排序演示。
# 解释：
# 创建了一个 power_tools 列表，存储不同重量的电动工具。
# 结果：电动工具列表已创建。
print(f"\n{'Example 7':*^50}")
power_tools = [
    Tool('drill', 4),
    Tool('circular saw', 5),
    Tool('jackhammer', 40),
    Tool('sander', 4),
]


# Example 8 --- 直接比较元组
# 目的：展示如何通过元组的元素逐个比较大小。
# 解释：
# 元组比较会首先比较第一个元素，如果相等，再比较第二个元素。
# 结果：验证 (40, 'jackhammer') 比 (5, 'circular saw') 大。
print(f"\n{'Example 8':*^50}")
saw = (5, 'circular saw')
jackhammer = (40, 'jackhammer')
assert not (jackhammer < saw)  # Matches expectations


# Example 9 --- 元组的多层比较
# 目的：展示在元组中如何根据多个字段进行比较。
# 解释：
# drill 和 sander 的重量相同，因此会比较它们的名称。
# 结果：验证 drill 排在 sander 之前，因为字母顺序在前。
print(f"\n{'Example 9':*^50}")
drill = (4, 'drill')
sander = (4, 'sander')
assert drill[0] == sander[0]  # Same weight
assert drill[1] < sander[1]   # Alphabetically less
assert drill < sander         # Thus, drill comes first


# Example 10 --- 根据多个标准排序
# 目的：展示如何根据多个标准对对象进行排序。
# 解释：
# power_tools.sort(key=lambda x: (x.weight, x.name)) 首先根据重量排序，如果重量相同，则根据名称排序。
# 结果：输出按重量和名称排序的结果。
print(f"\n{'Example 10':*^50}")
power_tools.sort(key=lambda x: (x.weight, x.name))
print(power_tools)


# Example 11 --- 反向排序
# 目的：展示如何对多个标准的排序结果进行反向排序。
# 解释：
# 使用 reverse=True 对排序结果进行反转，使所有标准的排序都变为降序。
# 结果：输出按重量和名称降序排列的结果。
print(f"\n{'Example 11':*^50}")
power_tools.sort(key=lambda x: (x.weight, x.name),
                 reverse=True)  # Makes all criteria descending
print(power_tools)


# Example 12 --- 使用负数实现部分反向排序
# 目的：展示如何通过对数值使用负号实现部分标准的降序排序。
# 解释：
# power_tools.sort(key=lambda x: (-x.weight, x.name)) 使重量降序，名称升序。
# 结果：输出按重量降序、名称升序排列的结果。
print(f"\n{'Example 12':*^50}")
power_tools.sort(key=lambda x: (-x.weight, x.name))
print(power_tools)


# Example 13 --- 处理无效的标准组合
# 目的：展示当排序标准无效时会引发错误。
# 解释：
# lambda x: (x.weight, -x.name) 试图对字符串使用负号操作是无效的，导致 TypeError。
# 结果：捕获并记录异常。
print(f"\n{'Example 13':*^50}")
try:
    power_tools.sort(key=lambda x: (x.weight, -x.name),
                     reverse=True)
except:
    logging.exception('Expected')
else:
    assert False


# Example 14 --- 通过多次调用 sort 实现复杂排序
# 目的：展示如何通过多次调用 sort 方法实现复杂的排序。
# 解释：
# 先按名称升序排序，然后按重量降序排序。
# 结果：输出最终排序结果。
print(f"\n{'Example 14':*^50}")
power_tools.sort(key=lambda x: x.name)   # Name ascending

power_tools.sort(key=lambda x: x.weight, # Weight descending
                 reverse=True)

print(power_tools)


# Example 15 --- 按名称排序
# 目的：展示按单一标准（名称）进行排序。
# 解释：
# power_tools.sort(key=lambda x: x.name) 按名称升序排序。
# 结果：输出按名称排序的结果。
print(f"\n{'Example 15':*^50}")
power_tools.sort(key=lambda x: x.name)
print(power_tools)


# Example 16 --- 按重量降序排序
# 目的：展示按单一标准（重量）降序排序。
# 解释：
# power_tools.sort(key=lambda x: x.weight, reverse=True) 按重量降序排序。
# 结果：输出按重量降序排列的结果。
print(f"\n{'Example 16':*^50}")
power_tools.sort(key=lambda x: x.weight,
                 reverse=True)
print(power_tools)

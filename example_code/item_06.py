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
Prefer Multiple Assignment Unpacking Over Indexing
把数据结构直接拆分到多个变量中，避免通过下标索引来访问数据结构
"""

import random
import sys

random.seed(1234)

import logging

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

# 配置日志将输出到 stdout 而不是 stderr
logging.basicConfig(stream=sys.stdout, level=logging.INFO)

print(f"\nPrefer Multiple Assignment Unpacking Over Indexing")
print(f"\n把数据结构直接拆分到多个变量中，避免通过下标索引来访问数据结构")

# Example 1 --- 使用 tuple() 将字典项转换为元组
# 目的： 演示如何将字典的键值对转换为元组。
# 解释：
# snack_calories.items() 返回字典的 (键, 值) 对。
# tuple() 将这些 (键, 值) 对转换为不可变的元组。
# 元组中的每个元素是 ('键', 值) 这种格式。
print(f"\n{'Example 1':*^50}")
snack_calories = {
    'chips': 140,
    'popcorn': 80,
    'nuts': 190,
}
items = tuple(snack_calories.items())
print(items)

# Example 2 --- 元组元素的索引访问
print(f"\n{'Example 2':*^50}")
item = ('Peanut butter', 'Jelly')
first = item[0]
second = item[1]
print(first, 'and', second)

# Example 3 --- 元组的不可变性
# 目的： 展示元组的不可变性，修改元组会抛出异常。
# 解释：
# 元组是不可变的，不能修改其元素。
# 尝试修改 pair[0] 会引发 TypeError，except 块捕获该异常，并记录日志。
# 既然元组是不可变的，那么元组能看做常量么？
print(f"\n{'Example 3':*^50}")
try:
    pair = ('Chocolate', 'Peanut butter')
    pair[0] = 'Honey'
except Exception as e:
    logging.error(f"Error type: {e.__class__.__name__}, Message: {str(e)}")
else:
    assert False

# Example 4 --- 元组解包
#目的： 演示如何通过解包来提取元组的元素。
# 解释：
# first, second = item 将元组 item 中的两个元素分别赋值给 first 和 second。
# 这种方式比通过索引访问更简洁。
print(f"\n{'Example 4':*^50}")
item = ('Peanut butter', 'Jelly')
first, second = item  # Unpacking
print(first, 'and', second)


# Example 5 --- 多层嵌套元组解包
# 目的： 演示如何进行多层嵌套的元组解包。
# 解释：
# favorite_snacks.items() 返回字典的 (键, 值) 对，每个值本身是一个元组。
# 通过嵌套解包，提取每个小吃的种类、名称和热量。
# 这种多层解包可以一次性提取所有嵌套元组中的值。
print(f"\n{'Example 5':*^50}")
favorite_snacks = {
	'salty': ('pretzels', 100),
	'sweet': ('cookies', 180),
	'veggie': ('carrots', 20),
}

((type1, (name1, cals1)),
 (type2, (name2, cals2)),
 (type3, (name3, cals3))) = favorite_snacks.items()

print(f'Favorite {type1} is {name1} with {cals1} calories')
print(f'Favorite {type2} is {name2} with {cals2} calories')
print(f'Favorite {type3} is {name3} with {cals3} calories')


# Example 6 --- 冒泡排序实现（不使用交换语法）
# 目的： 演示通过冒泡排序算法对列表进行排序（不使用 Python 的交换语法）。
# 解释：
# 冒泡排序通过多次遍历列表，相邻元素比较并交换位置，将较大的元素逐渐“冒泡”到末尾。
# 这里使用了临时变量 temp 进行交换操作。
print(f"\n{'Example 6':*^50}")
def bubble_sort(a):
	for _ in range(len(a)):
		for i in range(1, len(a)):
			if a[i] < a[i-1]:
				temp = a[i]
				a[i] = a[i-1]
				a[i-1] = temp

names = ['pretzels', 'carrots', 'arugula', 'bacon']
bubble_sort(names)
print(names)


# Example 7 --- 使用交换语法优化冒泡排序
# 目的： 使用 Python 的交换语法优化冒泡排序。
# 解释：
# 使用 a[i-1], a[i] = a[i], a[i-1] 来交换两个元素，简化了交换过程，不需要临时变量。
# 这样写法更简洁，而且交换效率相同。
print(f"\n{'Example 7':*^50}")
def bubble_sort(a):
	for _ in range(len(a)):
		for i in range(1, len(a)):
			if a[i] < a[i-1]:
				a[i-1], a[i] = a[i], a[i-1]  # Swap

names = ['pretzels', 'carrots', 'arugula', 'bacon']
bubble_sort(names)
print(names)


# Example 8 --- 传统方式遍历列表
# 目的： 演示传统方式遍历列表并提取元素。
# 解释：
# 通过 for i in range(len(snacks)) 迭代列表，手动使用索引访问每个元素。
# snacks[i] 提取元组，再通过索引获取元组中的各个值。
print(f"\n{'Example 8':*^50}")
snacks = [('bacon', 350), ('donut', 240), ('muffin', 190)]
for i in range(len(snacks)):
	item = snacks[i]
	name = item[0]
	calories = item[1]
	print(f'#{i+1}: {name} has {calories} calories')


# Example 9 --- 使用 enumerate() 遍历列表
# 目的： 演示如何使用 enumerate() 函数遍历列表并同时获取索引和元素。
# 解释：
# enumerate(snacks, 1) 生成 (索引, 元素) 对，从 1 开始计数。
# 通过元组解包，直接提取 name 和 calories，不需要手动索引。
print(f"\n{'Example 9':*^50}")
for rank, (name, calories) in enumerate(snacks, 1):
	print(f'#{rank}: {name} has {calories} calories')

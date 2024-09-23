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

# 军规 13: Prefer Unpacking Over Indexing
# 军规 13: 优先使用解包操作代替索引访问

"""
Prefer Unpacking Over Indexing
优先使用解包操作代替索引访问
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


# Example 1 --- 解包操作不足引发异常
# 目的：展示当解包操作无法分配足够值时会引发错误。
# 解释：
# car_ages_descending 列表有 10 个元素，但只尝试解包两个值，导致 ValueError。
# 结果：记录异常，程序不会崩溃。
print(f"\n{'Example 1':*^50}")
try:
    car_ages = [0, 9, 4, 8, 7, 20, 19, 1, 6, 15]
    car_ages_descending = sorted(car_ages, reverse=True)
    oldest, second_oldest = car_ages_descending
except:
    logging.exception('Expected')
else:
    assert False


# Example 2 --- 使用索引访问列表元素
# 目的：演示通过索引访问列表的前两个元素和剩余部分。
# 解释：
# 使用 car_ages_descending[0] 和 car_ages_descending[1] 获取前两个元素，其余部分使用切片获取。
# 结果：输出最老和次老的车辆，以及剩余车辆。
print(f"\n{'Example 2':*^50}")
oldest = car_ages_descending[0]
second_oldest = car_ages_descending[1]
others = car_ages_descending[2:]
print(oldest, second_oldest, others)


# Example 3 --- 使用解包替代索引访问
# 目的：展示通过解包操作替代索引访问，获取前两个元素和剩余部分。
# 解释：
# oldest, second_oldest, *others 通过解包操作一次性获取列表的前两个元素和剩余部分。
# 结果：输出最老和次老的车辆，以及剩余车辆。
print(f"\n{'Example 3':*^50}")
oldest, second_oldest, *others = car_ages_descending
print(oldest, second_oldest, others)


# Example 4 --- 不同的解包方式
# 目的：展示如何通过解包操作提取列表的头尾元素和中间部分。
# 解释：
# oldest, *others, youngest 获取列表的首尾元素，中间部分存入 others。
# *others, second_youngest, youngest 获取列表的最后两个元素和剩余部分。
# 结果：分别输出首尾元素和中间部分，以及最后两个元素。
print(f"\n{'Example 4':*^50}")
oldest, *others, youngest = car_ages_descending
print(oldest, youngest, others)

*others, second_youngest, youngest = car_ages_descending
print(youngest, second_youngest, others)


# Example 5 --- 不允许只有剩余值的解包
# 目的：展示当解包操作只使用剩余值部分时会引发错误。
# 解释：
# *others = car_ages_descending 这种解包操作无效，必须有至少一个显式的变量。
# 结果：引发 SyntaxError 异常，记录并处理。
print(f"\n{'Example 5':*^50}")
try:
    # This will not compile
    source = """*others = car_ages_descending"""
    eval(source)
except:
    logging.exception('Expected')
else:
    assert False


# Example 6 --- 不允许多个剩余值解包
# 目的：展示当解包操作中有多个剩余值时会引发错误。
# 解释：
# first, *middle, *second_middle, last = [1, 2, 3, 4] 是无效的语法，因为解包中只能有一个剩余值变量。
# 结果：引发 SyntaxError 异常，记录并处理。
print(f"\n{'Example 6':*^50}")
try:
    # This will not compile
    source = """first, *middle, *second_middle, last = [1, 2, 3, 4]"""
    eval(source)
except:
    logging.exception('Expected')
else:
    assert False


# Example 7 --- 在嵌套结构中使用解包
# 目的：展示如何在嵌套结构中使用解包操作提取多个值。
# 解释：
# car_inventory 是一个嵌套结构，解包 loc1, best1, *rest1 提取位置和最佳汽车，剩余汽车存入 rest。
# 结果：输出两个地点的最佳汽车和剩余汽车数量。
print(f"\n{'Example 7':*^50}")
car_inventory = {
	'Downtown': ('Silver Shadow', 'Pinto', 'DMC'),
	'Airport': ('Skyline', 'Viper', 'Gremlin', 'Nova'),
}

((loc1, (best1, *rest1)),
 (loc2, (best2, *rest2))) = car_inventory.items()

print(f'Best at {loc1} is {best1}, {len(rest1)} others')
print(f'Best at {loc2} is {best2}, {len(rest2)} others')


# Example 8 --- 处理解包不足的情况
# 目的：展示当列表元素不足时如何处理解包操作。
# 解释：
# short_list 只有两个元素，但通过 *rest 可以避免解包失败，剩余部分为 []。
# 结果：输出前两个元素和剩余部分（空列表）。
print(f"\n{'Example 8':*^50}")
short_list = [1, 2]
first, second, *rest = short_list
print(first, second, rest)


# Example 9 --- 迭代器无法自动解包
# 目的：展示迭代器无法直接通过解包操作获取多个元素。
# 解释：
# iter(range(1, 3)) 是一个迭代器，不能像列表那样直接解包多个值。
# 结果：引发 TypeError 异常。
print(f"\n{'Example 9':*^50}")
it = iter(range(1, 3))
try:
    first, second = it
except TypeError as e:
    print(f"Error: {e}")


# Example 10 --- 使用生成器生成 CSV 行
# 目的：演示如何通过生成器动态生成 CSV 行数据。
# 解释：
# generate_csv() 是一个生成器，逐行生成 CSV 数据，可以节省内存。
# 结果：生成 CSV 的每一行，包括标题和 100 条数据。
print(f"\n{'Example 10':*^50}")
def generate_csv():
	yield ('Date', 'Make' , 'Model', 'Year', 'Price')
	for i in range(100):
		yield ('2019-03-25', 'Honda', 'Fit' , '2010', '$3400')
		yield ('2019-03-26', 'Ford', 'F150' , '2008', '$2400')


# Example 11 --- 从生成器中提取 CSV 数据
# 目的：展示如何将生成器的结果转换为列表，并通过解包提取标题和数据。
# 解释：
# all_csv_rows 列表存储生成器生成的所有行，header 保存标题行，rows 保存剩余数据。
# 结果：输出 CSV 的标题和数据行数。
print(f"\n{'Example 11':*^50}")
all_csv_rows = list(generate_csv())
header = all_csv_rows[0]
rows = all_csv_rows[1:]
print('CSV Header:', header)
print('Row count: ', len(rows))


# Example 12 --- 直接从生成器解包提取 CSV 数据
# 目的：演示如何直接从生成器解包提取标题和数据。
# 解释：
# 通过解包操作从生成器 it 中提取标题行和剩余数据行。
# 结果：输出 CSV 的标题和数据行数。
print(f"\n{'Example 12':*^50}")
it = generate_csv()
header, *rows = it
print('CSV Header:', header)
print('Row count: ', len(rows))

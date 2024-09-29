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
备注：一定要注意场景区分
这个有场景区分，如果要一次性对列表所有值进行赋值，解包效能好，
反之，我只想把列表中一个索引下的元素赋值给别的变量，索引就有优势了，
解包是全局性的，索引其实是局部性的
"""


import random
import sys

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

# 配置日志将输出到 stdout 而不是 stderr
logging.basicConfig(stream=sys.stdout, level=logging.INFO)


# Example 1 --- 解包操作不足引发异常
# 目的：展示当解包操作无法分配足够值时会引发错误。
# 解释：
# car_ages_descending 列表有 10 个元素，但只尝试解包两个值，导致 ValueError。
# 结果：记录异常，程序不会崩溃。
print(f"\n{'Example 1':*^50}")
try:
    car_ages = [0, 9, 4, 8, 7, 20, 19, 1, 6, 15]
    car_ages_descending = sorted(car_ages, reverse=True) # 降序排列
    oldest, second_oldest = car_ages_descending
except Exception as e:
    logging.error(f"Error type: {e.__class__.__name__}, Message: {str(e)}")
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
    source = """*others = car_ages_descending"""    # 语法错误：带星号的赋值目标必须在列表或元组中
    eval(source)
except Exception as e:
    logging.error(f"Error type: {e.__class__.__name__}, Message: {str(e)}")
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
    source = """first, *middle, *second_middle, last = [1, 2, 3, 4]""" # 是无效的语法，因为解包中只能有一个剩余值变量。
    eval(source)
except Exception as e:
    logging.error(f"Error type: {e.__class__.__name__}, Message: {str(e)}")
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
# 备注 ： 它实际上展示了 Python 的一种特性——“星号解包”（starred unpacking），用来处理可变长度的数据
# 目的：展示当列表元素不足时如何处理解包操作，针对返回固定字段信息和可变字段信息的场景。
# 解释：
# short_list 只有两个元素，但通过 *rest 可以避免解包失败，剩余部分为 []。
# 结果：输出前两个元素和剩余部分（空列表）。
print(f"\n{'Example 8':*^50}")
short_list = [1, 2]
first, second, *rest = short_list
print(first, second, rest)


# Example 9 --- 迭代器无法自动解包

# 迭代器的工作机制：
# 迭代器（iterator）是一个能够逐个返回元素的对象，但它的元素只会被一次性返回，
# 当元素被取出后，迭代器的“游标”会向前滑动，指向下一个元素。
# 不可重复访问：迭代器只能一次性遍历，元素一旦被取出，就不能再回头访问它们了。

# 为什么迭代器无法自动解包？
# 解包需要一次性获取多个元素，而迭代器的游标只能前进，并且只能逐个获取元素。
# 如果用迭代器进行解包，Python 会依次获取元素，但由于解包的变量数量是固定的，迭代器的逐步取值特性可能会导致解包不完整，或无法满足所有变量的解包需求。
# 目的：展示迭代器无法直接通过解包操作获取多个元素。
# 解释：
# iter(range(1, 3)) 是一个迭代器，不能像列表那样直接解包多个值。
# 结果：引发 TypeError 异常。
print(f"\n{'Example 9':*^50}")
it = iter(range(1, 3))
try:
    first, second = it
except Exception as e:
    logging.error(f"Error type: {e.__class__.__name__}, Message: {str(e)}")


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


# Example 11 --- 从生成器中提取 CSV 数据 ---- 为Example 12做数据准备
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
it = generate_csv()                 # 生成器，逐行生成 CSV 数据
header, *rows = it
print('CSV Header:', header)
print('Row count: ', len(rows))

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

# 军规 15: Be Cautious When Relying on dict Insertion Ordering
# 军规 15: 当依赖字典插入顺序时要小心

"""
Be Cautious When Relying on dict Insertion Ordering
当依赖字典插入顺序时要小心
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

# Example 2 --- 创建并打印字典
# 目的：演示如何创建一个简单的字典，并打印出字典内容。
# 解释：
# baby_names 是一个字典，存储宠物名称和它们的幼崽名。
# 结果：输出字典内容。
print(f"\n{'Example 2':*^50}")
baby_names = {
    'cat': 'kitten',
    'dog': 'puppy',
}
print(baby_names)

# Example 4 --- 获取字典的键、值、项，并使用 popitem 移除最后一项
# 目的：展示如何获取字典的键、值、项列表，并使用 popitem 移除最后插入的项。
# 解释：
# keys() 返回字典的键，values() 返回值，items() 返回键值对。
# popitem() 移除并返回字典中最后插入的键值对。
# 结果：分别输出字典的键、值、项列表，最后移除并打印最后一项。
print(f"\n{'Example 4':*^50}")
print(list(baby_names.keys()))
print(list(baby_names.values()))
print(list(baby_names.items()))
print(baby_names.popitem())  # Last item inserted

# Example 6 --- 使用关键字参数的函数
# 目的：演示如何使用 **kwargs 关键字参数接收任意数量的命名参数。
# 解释：
# my_func 使用 **kwargs 关键字参数，遍历并打印每个参数的键值对。
# 结果：输出 'goose' 和 'kangaroo' 的幼崽名称。
print(f"\n{'Example 6':*^50}")
def my_func(**kwargs):
    for key, value in kwargs.items():
        print(f'{key} = {value}')
my_func(goose='gosling', kangaroo='joey')

# Example 8 --- 使用类中的 __dict__ 属性获取实例的属性和值
# 目的：展示如何通过 __dict__ 属性获取实例的属性和值。
# 解释：
# MyClass 包含两个属性，使用 __dict__.items() 遍历实例的属性和值。
# 结果：输出实例的所有属性和值。
print(f"\n{'Example 8':*^50}")
class MyClass:
    def __init__(self):
        self.alligator = 'hatchling'
        self.elephant = 'calf'

a = MyClass()
for key, value in a.__dict__.items():
    print(f'{key} = {value}')

# Example 9 --- 创建投票字典
# 目的：演示如何创建一个存储投票结果的字典。
# 解释：
# votes 字典存储动物名称及其对应的票数。
# 结果：投票字典创建完成。
print(f"\n{'Example 9':*^50}")
votes = {
    'otter': 1281,
    'polar bear': 587,
    'fox': 863,
}

# Example 10 --- 根据投票结果生成排名
# 目的：展示如何根据投票结果生成动物的排名。
# 解释：
# populate_ranks 函数根据投票数对动物进行排序，并将其排名存入 ranks 字典。
# 结果：生成并存储动物排名。
print(f"\n{'Example 10':*^50}")


def populate_ranks(votes, ranks):
    names = list(votes.keys())
    names.sort(key=votes.get, reverse=True)
    for i, name in enumerate(names, 1):
        ranks[name] = i


# Example 11 --- 获取排名最高的动物
# 目的：演示如何从字典中获取排名最高的动物。
# 解释：
# get_winner 函数使用 next 和 iter 从字典中获取第一个键，即排名最高的动物。
# 结果：返回排名最高的动物名称。
print(f"\n{'Example 11':*^50}")
def get_winner(ranks):
    return next(iter(ranks))


# Example 12 --- 生成排名并获取胜者
# 目的：展示如何生成动物排名并获取胜者。
# 解释：
# ranks 是一个空字典，populate_ranks 函数填充它，最后通过 get_winner 获取排名最高的动物。
# 结果：输出生成的排名和排名第一的动物。
print(f"\n{'Example 12':*^50}")
ranks = {}
populate_ranks(votes, ranks)
print(ranks)
winner = get_winner(ranks)
print(winner)

# Example 13 --- 创建支持排序的字典类
# 目的：展示如何通过继承 MutableMapping 实现一个支持排序的字典类。
# 解释：
# SortedDict 继承自 MutableMapping，实现了常见的字典操作，并按键进行排序。
# 结果：可以像普通字典一样使用 SortedDict，并支持按键排序。
print(f"\n{'Example 13':*^50}")
from collections.abc import MutableMapping


class SortedDict(MutableMapping):
    def __init__(self):
        self.data = {}

    def __getitem__(self, key):
        return self.data[key]

    def __setitem__(self, key, value):
        self.data[key] = value

    def __delitem__(self, key):
        del self.data[key]

    def __iter__(self):
        keys = list(self.data.keys())
        keys.sort()
        for key in keys:
            yield key
    def __len__(self):
        return len(self.data)

my_dict = SortedDict()
my_dict['otter'] = 1
my_dict['cheeta'] = 2
my_dict['anteater'] = 3
my_dict['deer'] = 4

assert my_dict['otter'] == 1

assert 'cheeta' in my_dict
del my_dict['cheeta']
assert 'cheeta' not in my_dict

expected = [('anteater', 3), ('deer', 4), ('otter', 1)]
assert list(my_dict.items()) == expected

assert not isinstance(my_dict, dict)

# Example 14 --- 使用 SortedDict 存储并获取排名
# 目的：展示如何使用自定义的 SortedDict 类存储并获取排名。
# 解释：
# populate_ranks 使用 SortedDict 存储排名数据，get_winner 获取排名第一的动物。
# 结果：输出排名和胜者。
print(f"\n{'Example 14':*^50}")
sorted_ranks = SortedDict()
populate_ranks(votes, sorted_ranks)
print(sorted_ranks.data)
winner = get_winner(sorted_ranks)
print(winner)

# Example 15 --- 自定义获取胜者的逻辑
# 目的：展示如何通过遍历字典自定义获取胜者的逻辑。
# 解释：
# get_winner 函数遍历 ranks 字典，查找排名为 1 的动物并返回。
# 结果：输出排名第一的动物。
print(f"\n{'Example 15':*^50}")
def get_winner(ranks):
    for name, rank in ranks.items():
        if rank == 1:
            return name


winner = get_winner(sorted_ranks)
print(winner)

# Example 16 --- 检查字典类型并处理异常
# 目的：展示如何检查字典类型并处理类型不匹配的情况。
# 解释：
# get_winner 函数检查传入参数是否为 dict 类型，如果不是，则引发 TypeError。
# 结果：捕获并记录异常信息。
print(f"\n{'Example 16':*^50}")
try:
    def get_winner(ranks):
        if not isinstance(ranks, dict):
            raise TypeError('must provide a dict instance')
        return next(iter(ranks))


    assert get_winner(ranks) == 'otter'

    get_winner(sorted_ranks)
except:
    logging.exception('Expected')
else:
    assert False

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

# 军规 17: Prefer defaultdict Over setdefault to Handle Missing Items in Internal State
# 军规 17: 使用 defaultdict 代替 setdefault 处理内部状态中缺失的项

"""
Prefer defaultdict Over setdefault to Handle Missing Items in Internal State
使用 defaultdict 代替 setdefault 处理内部状态中缺失的项
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


# Example 1 --- 初始化一个包含访问记录的字典
# 目的：展示如何初始化一个包含访问城市的字典。
# 解释：
# visits 是一个字典，其中每个国家对应一个集合，存储访问过的城市。
# 结果：字典初始化完成，包含墨西哥和日本的访问城市记录。
print(f"\n{'Example 1':*^50}")
visits = {
    'Mexico': {'Tulum', 'Puerto Vallarta'},
    'Japan': {'Hakone'},
}


# Example 2 --- 使用 setdefault 和 get 添加访问记录
# 目的：展示如何使用 setdefault 方法和 get 方法处理缺失的键，并添加访问记录。
# 解释：
# visits.setdefault('France', set()).add('Arles') 将 'France' 键初始化为一个空集合并添加城市 'Arles'。
# 如果 'Japan' 键存在，则获取其值并添加城市 'Kyoto'；否则，初始化该键为集合并添加城市。
# 结果：输出更新后的访问记录。
print(f"\n{'Example 2':*^50}")
visits.setdefault('France', set()).add('Arles')  # Short

if (japan := visits.get('Japan')) is None:       # Long
    visits['Japan'] = japan = set()
japan.add('Kyoto')
original_print = print
print = pprint

print(visits)
print = original_print


# Example 3 --- 自定义类实现访问记录
# 目的：展示如何通过自定义类管理访问记录。
# 解释：
# Visits 类使用字典管理国家和访问的城市，add 方法通过 setdefault 添加城市到相应的国家。
# 结果：输出更新后的访问记录。
print(f"\n{'Example 3':*^50}")
class Visits:
    def __init__(self):
        self.data = {}

    def add(self, country, city):
        city_set = self.data.setdefault(country, set())
        city_set.add(city)


# Example 4 --- 使用自定义类添加访问记录
# 目的：演示如何使用自定义的 Visits 类添加访问记录。
# 解释：
# 调用 visits.add() 方法添加访问记录，并通过 print 输出字典的内容。
# 结果：更新后的访问记录包含俄罗斯和坦桑尼亚的城市。
print(f"\n{'Example 4':*^50}")
visits = Visits()
visits.add('Russia', 'Yekaterinburg')
visits.add('Tanzania', 'Zanzibar')
print(visits.data)


# Example 5 --- 使用 defaultdict 简化字典操作
# 目的：展示如何通过 defaultdict 简化缺失键的处理。
# 解释：
# defaultdict(set) 自动为不存在的键创建一个空集合，简化了添加城市的操作。
# 结果：输出更新后的访问记录。
print(f"\n{'Example 5':*^50}")
from collections import defaultdict

class Visits:
    def __init__(self):
        self.data = defaultdict(set)

    def add(self, country, city):
        self.data[country].add(city)

visits = Visits()
visits.add('England', 'Bath')
visits.add('England', 'London')
print(visits.data)
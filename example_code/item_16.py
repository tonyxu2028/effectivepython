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

# 军规 16: Prefer get Over in and KeyError to Handle Missing Dictionary Keys
# 军规 16: 使用 get 代替 in 和 KeyError 来处理字典缺失的键

"""
Prefer get Over in and KeyError to Handle Missing Dictionary Keys
使用 get 代替 in 和 KeyError 来处理字典缺失的键
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


# Example 1 --- 初始化计数器字典
# 目的：演示如何创建并初始化一个字典。
# 解释：
# counters 是一个字典，用来记录不同种类面包的数量。
# 结果：字典初始化完成，包含两种面包。
print(f"\n{'Example 1':*^50}")
counters = {
    'pumpernickel': 2,
    'sourdough': 1,
}


# Example 2 --- 使用 in 操作符判断键是否存在
# 目的：展示如何使用 in 操作符判断字典中是否存在某个键。
# 解释：
# 如果键 'wheat' 存在，则获取其值；否则，将其初始化为 0 并更新计数。
# 结果：更新后输出字典。
print(f"\n{'Example 2':*^50}")
key = 'wheat'

if key in counters:
    count = counters[key]
else:
    count = 0

counters[key] = count + 1

print(counters)


# Example 3 --- 使用 try-except 处理 KeyError 异常
# 目的：展示如何使用 try-except 捕获字典中不存在的键引发的 KeyError。
# 解释：
# 如果字典中不存在 'brioche'，则捕获 KeyError 并将其初始化为 0，再更新计数。
# 结果：更新后输出字典。
print(f"\n{'Example 3':*^50}")
key = 'brioche'

try:
    count = counters[key]
except KeyError:
    count = 0

counters[key] = count + 1

print(counters)


# Example 4 --- 使用 get 方法处理缺失的键
# 目的：展示如何使用 get 方法避免 KeyError。
# 解释：
# get 方法可以在键不存在时返回一个默认值，在这里返回 0。
# 结果：更新后输出字典。
print(f"\n{'Example 4':*^50}")
key = 'multigrain'

count = counters.get(key, 0)
counters[key] = count + 1

print(counters)


# Example 5 --- 多种处理缺失键的方法
# 目的：展示多种处理字典中缺失键的方式。
# 解释：
# 通过 if 语句、try-except 和 get 方法处理不存在的键，并更新计数。
# 结果：更新后输出字典。
print(f"\n{'Example 5':*^50}")
key = 'baguette'

if key not in counters:
    counters[key] = 0
counters[key] += 1

key = 'ciabatta'

if key in counters:
    counters[key] += 1
else:
    counters[key] = 1

key = 'ciabatta'

try:
    counters[key] += 1
except KeyError:
    counters[key] = 1

print(counters)


# Example 6 --- 处理列表值的缺失键
# 目的：演示如何处理字典中列表类型的值，并处理缺失键。
# 解释：
# votes 字典存储每个面包种类的投票人，若键不存在则创建一个空列表。
# 结果：更新后输出字典。
print(f"\n{'Example 6':*^50}")
votes = {
    'baguette': ['Bob', 'Alice'],
    'ciabatta': ['Coco', 'Deb'],
}

key = 'brioche'
who = 'Elmer'

if key in votes:
    names = votes[key]
else:
    votes[key] = names = []

names.append(who)
print(votes)


# Example 7 --- 使用 try-except 处理列表类型的缺失键
# 目的：展示如何使用 try-except 捕获字典中缺失键，并创建空列表。
# 解释：
# 如果字典中不存在键 'rye'，则捕获 KeyError 并将其初始化为空列表。
# 结果：更新后输出字典。
print(f"\n{'Example 7':*^50}")
key = 'rye'
who = 'Felix'

try:
    names = votes[key]
except KeyError:
    votes[key] = names = []

names.append(who)

print(votes)


# Example 8 --- 使用 get 方法处理缺失键
# 目的：展示如何使用 get 方法处理缺失键并创建空列表。
# 解释：
# 通过 votes.get() 方法获取键对应的值，若键不存在则返回 None，进而创建空列表。
# 结果：更新后输出字典。
print(f"\n{'Example 8':*^50}")
key = 'wheat'
who = 'Gertrude'

names = votes.get(key)
if names is None:
    votes[key] = names = []

names.append(who)

print(votes)


# Example 9 --- 使用赋值表达式简化缺失键的处理
# 目的：展示如何使用赋值表达式（海象运算符）简化字典键的处理。
# 解释：
# 使用赋值表达式简化键不存在时的处理逻辑，一行代码完成键值的初始化和更新。
# 结果：更新后输出字典。
print(f"\n{'Example 9':*^50}")
key = 'brioche'
who = 'Hugh'

if (names := votes.get(key)) is None:
    votes[key] = names = []

names.append(who)

print(votes)


# Example 10 --- 使用 setdefault 方法简化字典的操作
# 目的：展示如何使用 setdefault 方法处理字典中缺失的键。
# 解释：
# setdefault 方法可以同时检查键是否存在并初始化该键为一个空列表，简化代码逻辑。
# 结果：更新后输出字典。
print(f"\n{'Example 10':*^50}")
key = 'cornbread'
who = 'Kirk'

names = votes.setdefault(key, [])
names.append(who)

print(votes)


# Example 11 --- 使用 setdefault 可能导致意外行为
# 目的：展示使用 setdefault 可能导致的副作用。
# 解释：
# 当 setdefault 使用一个可变对象（如列表）作为默认值时，即使未修改字典，该对象仍然保留在字典中。
# 结果：输出修改前后的字典。
print(f"\n{'Example 11':*^50}")
data = {}
key = 'foo'
value = []
data.setdefault(key, value)
print('Before:', data)
value.append('hello')
print('After: ', data)


# Example 12 --- 使用 setdefault 处理计数器字典
# 目的：展示如何使用 setdefault 方法处理计数器字典中的缺失键。
# 解释：
# 使用 setdefault 方法为键 'dutch crunch' 初始化为 0，并更新计数。
# 结果：更新后输出字典。
print(f"\n{'Example 12':*^50}")
key = 'dutch crunch'

count = counters.setdefault(key, 0)
counters[key] = count + 1

print(counters)

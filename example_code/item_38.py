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
import random
random.seed(1234)

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

# 目的：关闭所有打开的文件
# 解释：遍历所有对象，找到所有打开的文件并关闭它们。
def close_open_files():
    everything = gc.get_objects()
    for obj in everything:
        if isinstance(obj, io.IOBase):
            obj.close()

atexit.register(close_open_files)


# Example 1
# 目的：按字符串长度排序名称列表
# 解释：对名称列表按字符串长度进行排序。
# 结果：按字符串长度排序的名称列表
print(f"\n{'Example 1':*^50}")
names = ['Socrates', 'Archimedes', 'Plato', 'Aristotle']
names.sort(key=len)
print(names)


# Example 2
# 目的：记录缺失的键
# 解释：定义一个函数来记录缺失的键。
# 结果：记录缺失的键
print(f"\n{'Example 2':*^50}")
def log_missing():
    """
    目的：记录缺失的键
    解释：打印一条消息并返回 0。
    """
    print('Key added')
    return 0


# Example 3
# 目的：使用 defaultdict 处理缺失的键
# 解释：使用 defaultdict 和 log_missing 函数处理缺失的键。
# 结果：处理缺失的键
print(f"\n{'Example 3':*^50}")
from collections import defaultdict

current = {'green': 12, 'blue': 3}
increments = [
    ('red', 5),
    ('blue', 17),
    ('orange', 9),
]
result = defaultdict(log_missing, current)
print('Before:', dict(result))
for key, amount in increments:
    result[key] += amount
print('After: ', dict(result))


# Example 4
# 目的：使用闭包记录缺失的键
# 解释：定义一个闭包来记录缺失的键。
# 结果：记录缺失的键
print(f"\n{'Example 4':*^50}")
def increment_with_report(current, increments):
    """
    目的：增加并报告缺失的键
    解释：使用闭包记录缺失的键并返回结果和添加的键的数量。
    """
    added_count = 0

    def missing():
        nonlocal added_count  # Stateful closure
        added_count += 1
        return 0

    result = defaultdict(missing, current)
    for key, amount in increments:
        result[key] += amount

    return result, added_count


# Example 5
# 目的：测试 increment_with_report 函数
# 解释：测试 increment_with_report 函数的功能。
# 结果：测试通过
print(f"\n{'Example 5':*^50}")
result, count = increment_with_report(current, increments)
assert count == 2
print(result)


# Example 6
# 目的：定义一个类来记录缺失的键
# 解释：定义一个类来记录缺失的键。
# 结果：记录缺失的键
print(f"\n{'Example 6':*^50}")
class CountMissing:
    def __init__(self):
        """
        目的：初始化 CountMissing 类
        解释：初始化 added 计数器。
        """
        self.added = 0

    def missing(self):
        """
        目的：记录缺失的键
        解释：增加 added 计数器并返回 0。
        """
        self.added += 1
        return 0


# Example 7
# 目的：使用 CountMissing 类记录缺失的键
# 解释：使用 CountMissing 类的实例记录缺失的键。
# 结果：记录缺失的键
print(f"\n{'Example 7':*^50}")
counter = CountMissing()
result = defaultdict(counter.missing, current)  # Method ref
for key, amount in increments:
    result[key] += amount
assert counter.added == 2
print(result)


# Example 8
# 目的：定义一个可调用的类来记录缺失的键
# 解释：定义一个实现 __call__ 方法的类来记录缺失的键。
# 结果：记录缺失的键
print(f"\n{'Example 8':*^50}")
class BetterCountMissing:
    def __init__(self):
        """
        目的：初始化 BetterCountMissing 类
        解释：初始化 added 计数器。
        """
        self.added = 0

    def __call__(self):
        """
        目的：记录缺失的键
        解释：增加 added 计数器并返回 0。
        """
        self.added += 1
        return 0

counter = BetterCountMissing()
assert counter() == 0
assert callable(counter)


# Example 9
# 目的：使用 BetterCountMissing 类记录缺失的键
# 解释：使用 BetterCountMissing 类的实例记录缺失的键。
# 结果：记录缺失的键
print(f"\n{'Example 9':*^50}")
counter = BetterCountMissing()
result = defaultdict(counter, current)  # Relies on __call__
for key, amount in increments:
    result[key] += amount
assert counter.added == 2
print(result)
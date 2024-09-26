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
    """
    目的：关闭所有打开的文件
    解释：遍历所有对象，找到所有打开的文件并关闭它们。
    """
    everything = gc.get_objects()
    for obj in everything:
        if isinstance(obj, io.IOBase):
            obj.close()

atexit.register(close_open_files)


# Example 1
# 目的：定义一个类 Counter
# 解释：定义一个类 Counter，包含 __init__ 和 increment 方法。
# 结果：类 Counter
print(f"\n{'Example 1':*^50}")
class Counter:
    """
    目的：定义一个类 Counter
    解释：包含 __init__ 和 increment 方法。
    """
    def __init__(self):
        self.count = 0

    def increment(self, offset):
        self.count += offset


# Example 2
# 目的：定义一个函数 worker
# 解释：定义一个函数 worker，包含计数逻辑。
# 结果：函数 worker
print(f"\n{'Example 2':*^50}")
def worker(sensor_index, how_many, counter):
    """
    目的：定义一个函数 worker
    解释：包含计数逻辑。
    """
    BARRIER.wait()
    for _ in range(how_many):
        counter.increment(1)


# Example 3
# 目的：使用多线程进行计数
# 解释：创建多个线程并调用 worker 函数。
# 结果：多线程计数成功
print(f"\n{'Example 3':*^50}")
from threading import Barrier, Thread

BARRIER = Barrier(5)
how_many = 10**5
counter = Counter()

threads = []
for i in range(5):
    thread = Thread(target=worker, args=(i, how_many, counter))
    threads.append(thread)
    thread.start()

for thread in threads:
    thread.join()

expected = how_many * 5
found = counter.count
print(f'Counter should be {expected}, got {found}')


# Example 4
# 目的：直接修改计数器的 count 属性
# 解释：直接修改计数器的 count 属性。
# 结果：计数器的 count 属性被修改
print(f"\n{'Example 4':*^50}")
counter.count += 1


# Example 5
# 目的：使用 getattr 和 setattr 修改计数器的 count 属性
# 解释：使用 getattr 和 setattr 修改计数器的 count 属性。
# 结果：计数器的 count 属性被修改
print(f"\n{'Example 5':*^50}")
value = getattr(counter, 'count')
result = value + 1
setattr(counter, 'count', result)


# Example 6
# 目的：演示多线程环境下的竞态条件
# 解释：演示多线程环境下的竞态条件。
# 结果：竞态条件演示成功
print(f"\n{'Example 6':*^50}")
# Running in Thread A
value_a = getattr(counter, 'count')
# Context switch to Thread B
value_b = getattr(counter, 'count')
result_b = value_b + 1
setattr(counter, 'count', result_b)
# Context switch back to Thread A
result_a = value_a + 1
setattr(counter, 'count', result_a)


# Example 7
# 目的：定义一个类 LockingCounter
# 解释：定义一个类 LockingCounter，包含 __init__ 和 increment 方法，并使用锁。
# 结果：类 LockingCounter
print(f"\n{'Example 7':*^50}")
from threading import Lock

class LockingCounter:
    """
    目的：定义一个类 LockingCounter
    解释：包含 __init__ 和 increment 方法，并使用锁。
    """
    def __init__(self):
        self.lock = Lock()
        self.count = 0

    def increment(self, offset):
        with self.lock:
            self.count += offset


# Example 8
# 目的：使用多线程进行计数
# 解释：创建多个线程并调用 worker 函数。
# 结果：多线程计数成功
print(f"\n{'Example 8':*^50}")
BARRIER = Barrier(5)
counter = LockingCounter()

threads = []
for i in range(5):
    thread = Thread(target=worker, args=(i, how_many, counter))
    threads.append(thread)
    thread.start()

for thread in threads:
    thread.join()

expected = how_many * 5
found = counter.count
print(f'Counter should be {expected}, got {found}')
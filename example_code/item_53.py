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

# 军规 53 : Use Threads for Blocking I/O, Avoid for Parallelism
# 军规 53 ： 使用线程进行阻塞 I/O 操作，避免用于并行处理

"""
翻译:
"对阻塞 I/O 使用线程，避免用于并行计算"意味着：
线程适合处理 I/O 等待操作（如文件读写、网络请求、数据库操作）。
线程不适合用于 CPU 密集型任务，因为 GIL 限制了 Python 多线程在计算密集型任务上的性能提升。
这是一个重要的性能准则，Python 程序员在并发设计时需要牢记。


解读：
关键原理：
全局解释器锁 (GIL)：Python 的 GIL 机制使得同一时刻只能有一个线程执行 Python 字节码，
主要原因在于保证 Python 解释器的线程安全。
GIL 与 I/O 释放：在 I/O 操作（如文件读写、网络请求）中，线程会释放 GIL，使其他线程可以继续运行，
这使得线程适合处理 I/O 密集型任务。
GIL 与 CPU 密集型任务：计算密集型任务会一直占用 GIL，不会释放给其他线程，
因此使用线程不会提升并行计算的性能。


适用场景:
适合用线程的情况:
文件读写操作,网络请求（API、HTTP 请求）,数据库读写等 I/O 操作。
不适合用线程的情况：
数值计算,图像处理,大规模矩阵或数据处理等 CPU 密集型任务。


总结:
线程适合 I/O 密集型任务：在 I/O 操作中，线程能够在等待时释放 GIL，实现高效并发。
避免使用线程处理计算密集型任务：对于计算密集型任务，线程无法绕过 GIL，无法提升并行计算性能，推荐使用多进程。
理解 GIL 限制很重要：GIL 是 Python 多线程在计算任务中面临的核心瓶颈，尤其在高性能场景中，
进程和分布式计算更为合适。
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
import select
import socket

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
# 目的：定义一个函数 factorize
# 解释：定义一个函数 factorize，包含因数分解逻辑。
# 结果：函数 factorize
print(f"\n{'Example 1':*^50}")
def factorize(number):
    """
    目的：定义一个函数 factorize
    解释：包含因数分解逻辑。
    """
    for i in range(1, number + 1):
        if number % i == 0:
            yield i


# Example 2
# 目的：测试 factorize 函数
# 解释：使用 factorize 函数对多个数字进行因数分解并测量时间。
# 结果：因数分解成功
print(f"\n{'Example 2':*^50}")
import time

numbers = [2139079, 1214759, 1516637, 1852285]
start = time.time()

for number in numbers:
    list(factorize(number))

end = time.time()
delta = end - start
print(f'Took {delta:.3f} seconds')


# Example 3
# 目的：定义一个类 FactorizeThread
# 解释：定义一个类 FactorizeThread，继承自 Thread 并包含因数分解逻辑。
# 结果：类 FactorizeThread
print(f"\n{'Example 3':*^50}")
from threading import Thread

class FactorizeThread(Thread):
    """
    目的：定义一个类 FactorizeThread
    解释：继承自 Thread 并包含因数分解逻辑。
    """
    def __init__(self, number):
        super().__init__()
        self.number = number

    def run(self):
        self.factors = list(factorize(self.number))


# Example 4
# 目的：使用 FactorizeThread 类进行多线程因数分解
# 解释：创建多个 FactorizeThread 对象并启动线程。
# 结果：多线程因数分解成功
print(f"\n{'Example 4':*^50}")
start = time.time()

threads = []
for number in numbers:
    thread = FactorizeThread(number)
    thread.start()
    threads.append(thread)


# Example 5
# 目的：等待所有线程完成
# 解释：使用 join 方法等待所有线程完成。
# 结果：所有线程完成
print(f"\n{'Example 5':*^50}")
for thread in threads:
    thread.join()

end = time.time()
delta = end - start
print(f'Took {delta:.3f} seconds')


# Example 6
# 目的：定义一个函数 slow_systemcall
# 解释：定义一个函数 slow_systemcall，包含 select 调用。
# 结果：函数 slow_systemcall

print(f"\n{'Example 6':*^50}")


def slow_systemcall():
    """
    目的：定义一个函数 slow_systemcall
    解释：包含 select 调用。
    """
    select.select([socket.socket()], [], [], 0.1)


# Example 7
# 目的：测试 slow_systemcall 函数
# 解释：调用 slow_systemcall 函数并测量时间。
# 结果：函数调用成功
print(f"\n{'Example 7':*^50}")
start = time.time()

for _ in range(5):
    slow_systemcall()

end = time.time()
delta = end - start
print(f'Took {delta:.3f} seconds')


# Example 8
# 目的：使用多线程调用 slow_systemcall 函数
# 解释：创建多个线程并调用 slow_systemcall 函数。
# 结果：多线程调用成功
print(f"\n{'Example 8':*^50}")
start = time.time()

threads = []
for _ in range(5):
    thread = Thread(target=slow_systemcall)
    thread.start()
    threads.append(thread)


# Example 9
# 目的：定义一个函数 compute_helicopter_location
# 解释：定义一个函数 compute_helicopter_location。
# 结果：函数 compute_helicopter_location
print(f"\n{'Example 9':*^50}")
def compute_helicopter_location(index):
    """
    目的：定义一个函数 compute_helicopter_location
    解释：函数体为空。
    """
    pass

for i in range(5):
    compute_helicopter_location(i)

for thread in threads:
    thread.join()

end = time.time()
delta = end - start
print(f'Took {delta:.3f} seconds')
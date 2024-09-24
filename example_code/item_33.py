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

# 军规33：尽量减少复杂性，优先选择简单的解决方案，保持代码可读性和可维护性。

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
atexit.register(TEST_DIR.cleanup)  # 程序结束时清理临时目录

# Make sure Windows processes exit cleanly
OLD_CWD = os.getcwd()
atexit.register(lambda: os.chdir(OLD_CWD))  # 程序结束时恢复工作目录
os.chdir(TEST_DIR.name)  # 切换到临时目录

def close_open_files():
    everything = gc.get_objects()  # 获取所有对象
    for obj in everything:
        if isinstance(obj, io.IOBase):  # 检查是否为文件对象
            obj.close()  # 关闭文件

atexit.register(close_open_files)  # 程序结束时关闭文件

# Example 1
print(f"\n{'Example 1':*^50}")
# 定义一个生成器函数，模拟移动
def move(period, speed):
    for _ in range(period):
        yield speed  # 生成速度值

# 定义一个生成器函数，模拟暂停
def pause(delay):
    for _ in range(delay):
        yield 0  # 生成0，表示暂停

# Example 2
print(f"\n{'Example 2':*^50}")
# 定义一个动画函数，组合移动和暂停
def animate():
    for delta in move(4, 5.0):  # 移动4个单位，速度为5.0
        yield delta
    for delta in pause(3):  # 暂停3个单位
        yield delta
    for delta in move(2, 3.0):  # 移动2个单位，速度为3.0
        yield delta

# Example 3
print(f"\n{'Example 3':*^50}")
# 渲染函数，输出每次的delta值
def render(delta):
    print(f'Delta: {delta:.1f}')  # 输出delta值

# 运行函数，调用传入的生成器函数
def run(func):
    for delta in func():  # 遍历生成器
        render(delta)  # 渲染delta值

run(animate)  # 运行动画函数

# Example 4
print(f"\n{'Example 4':*^50}")
# 使用yield from简化动画组合
def animate_composed():
    yield from move(4, 5.0)  # 移动
    yield from pause(3)  # 暂停
    yield from move(2, 3.0)  # 移动

run(animate_composed)  # 运行组合动画函数

# Example 5
print(f"\n{'Example 5':*^50}")
import timeit

# 定义生成器，产生1000000个数字
def child():
    for i in range(1_000_000):
        yield i

# 手动嵌套的生成器
def slow():
    for i in child():
        yield i

# 简化嵌套的生成器
def fast():
    yield from child()

# 测试手动嵌套的性能
baseline = timeit.timeit(
    stmt='for _ in slow(): pass',
    globals=globals(),
    number=50)
print(f'Manual nesting {baseline:.2f}s')

# 测试简化嵌套的性能
comparison = timeit.timeit(
    stmt='for _ in fast(): pass',
    globals=globals(),
    number=50)
print(f'Composed nesting {comparison:.2f}s')

# 计算时间差异
reduction = -(comparison - baseline) / baseline
print(f'{reduction:.1%} less time')  # 输出减少的时间百分比

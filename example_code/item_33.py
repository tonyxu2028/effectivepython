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

# 军规33: Compose multiple generators with yield from.
# 军规33: 使用yield from组合多个生成器。

"""

总结：生成器的本质在于 yield，而不是 range()
    yield 是生成器的核心：
    它允许函数暂停执行，并逐次返回值。
    range() 只是用于控制循环的次数，它并不是生成器的关键。

总结：yield vs. switch 的应用场景
    yield：
    适合顺序处理和状态记忆，如生成器、流处理、状态机模拟等场景。
    允许在多次调用之间保持状态。
    switch：
    适合条件匹配和快速逻辑切换，如根据用户输入执行不同逻辑。
    不记忆状态，每次匹配都是独立的。
"""

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
# 注意这里的_是一个占位符，表示不关心的值
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
# 总结：delta 是生成器的逐次输出值
# 在你的代码中，delta 是 每次从生成器取出的值。
# 它代表了每个时间步的变化（速度或暂停）。
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

# 手动嵌套 vs. yield from：本质区别
# 手动嵌套生成器：
# 用**for 循环**遍历内层生成器，并逐一 yield 出结果。
# 这种方式虽然可以工作，但代码更冗长，性能也稍逊。

# yield from 简化生成器：
# yield from 直接将子生成器的所有值传递给外层生成器，更高效，底层的 Python 实现会做优化。
# 代码也更加简洁，没有冗余的循环。

# 为什么需要传递 globals()？
# 字符串代码的作用域问题：
#
# 当 stmt 是字符串形式时，它不会直接继承当前模块的上下文，需要手动指定作用域。
# globals() 提供全局命名空间：
#
# 将当前模块的全局命名空间传递给 timeit，确保所有全局定义的函数、变量都能被访问。


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

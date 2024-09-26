#!/usr/bin/env PYTHONHASHSEED=1234 python3

# 版权所有 2014-2019 Brett Slatkin, Pearson Education Inc.
#
# 根据 Apache 许可证 2.0 版（“许可证”）获得许可；
# 除非遵守许可证，否则您不得使用此文件。
# 您可以在以下网址获得许可证副本：
#
#     http://www.apache.org/licenses/LICENSE-2.0
#
# 除非适用法律要求或书面同意，按许可证分发的软件
# 是按“原样”分发的，没有任何明示或暗示的担保或条件。
# 请参阅许可证以了解管理权限和限制的特定语言。

# 复现书中的环境
import random
random.seed(1234)

import logging
from pprint import pprint
from sys import stdout as STDOUT

# 将所有输出写入临时目录
import atexit
import gc
import io
import os
import tempfile

TEST_DIR = tempfile.TemporaryDirectory()
atexit.register(TEST_DIR.cleanup)

# 确保 Windows 进程干净退出
OLD_CWD = os.getcwd()
atexit.register(lambda: os.chdir(OLD_CWD))
os.chdir(TEST_DIR.name)

def close_open_files():
    """
    目的：关闭所有打开的文件
    解释：遍历所有对象并关闭所有打开的文件。
    结果：所有打开的文件被关闭
    """
    everything = gc.get_objects()
    for obj in everything:
        if isinstance(obj, io.IOBase):
            obj.close()

atexit.register(close_open_files)


# 示例 1
# 目的：实现插入排序算法
# 解释：定义一个插入排序函数，逐个插入元素到结果列表中。
# 结果：返回排序后的列表
def insertion_sort(data):
    """
    目的：实现插入排序算法
    解释：定义一个插入排序函数，逐个插入元素到结果列表中。
    结果：返回排序后的列表
    """
    result = []
    for value in data:
        insert_value(result, value)
    return result


# 示例 2
# 目的：在有序数组中插入值
# 解释：定义一个函数，在有序数组中找到合适的位置插入值。
# 结果：值被插入到数组中
def insert_value(array, value):
    """
    目的：在有序数组中插入值
    解释：定义一个函数，在有序数组中找到合适的位置插入值。
    结果：值被插入到数组中
    """
    for i, existing in enumerate(array):
        if existing > value:
            array.insert(i, value)
            return
    array.append(value)


# 示例 3
# 目的：生成随机数据并定义测试函数
# 解释：生成一个包含随机整数的列表，并定义一个测试插入排序的 lambda 函数。
# 结果：生成随机数据并定义测试函数
from random import randint

max_size = 10**4
data = [randint(0, max_size) for _ in range(max_size)]
test = lambda: insertion_sort(data)


# 示例 4
# 目的：使用 cProfile 进行性能分析
# 解释：使用 cProfile 模块对测试函数进行性能分析。
# 结果：生成性能分析数据
from cProfile import Profile

profiler = Profile()
profiler.runcall(test)


# 示例 5
# 目的：打印性能分析结果
# 解释：使用 pstats 模块打印性能分析结果。
# 结果：打印性能分析结果
from pstats import Stats

stats = Stats(profiler)
stats = Stats(profiler, stream=STDOUT)
stats.strip_dirs()
stats.sort_stats('cumulative')
stats.print_stats()


# 示例 6
# 目的：优化插入值函数
# 解释：使用 bisect 模块优化插入值的函数。
# 结果：提高插入值的效率
from bisect import bisect_left

def insert_value(array, value):
    """
    目的：优化插入值函数
    解释：使用 bisect 模块优化插入值的函数。
    结果：提高插入值的效率
    """
    i = bisect_left(array, value)
    array.insert(i, value)


# 示例 7
# 目的：再次进行性能分析
# 解释：使用优化后的插入值函数重新进行性能分析。
# 结果：生成新的性能分析数据
profiler = Profile()
profiler.runcall(test)
stats = Stats(profiler, stream=STDOUT)
stats.strip_dirs()
stats.sort_stats('cumulative')
stats.print_stats()


# 示例 8
# 目的：定义实用函数和测试函数
# 解释：定义一些实用函数和一个测试程序。
# 结果：定义了实用函数和测试程序
def my_utility(a, b):
    """
    目的：定义实用函数
    解释：定义一个简单的实用函数，进行一些计算。
    结果：返回计算结果
    """
    c = 1
    for i in range(100):
        c += a * b

def first_func():
    """
    目的：定义第一个测试函数
    解释：调用实用函数多次进行计算。
    结果：完成计算
    """
    for _ in range(1000):
        my_utility(4, 5)

def second_func():
    """
    目的：定义第二个测试函数
    解释：调用实用函数多次进行计算。
    结果：完成计算
    """
    for _ in range(10):
        my_utility(1, 3)

def my_program():
    """
    目的：定义测试程序
    解释：调用两个测试函数进行计算。
    结果：完成计算
    """
    for _ in range(20):
        first_func()
        second_func()


# 示例 9
# 目的：对测试程序进行性能分析
# 解释：使用 cProfile 对测试程序进行性能分析。
# 结果：生成性能分析数据
profiler = Profile()
profiler.runcall(my_program)
stats = Stats(profiler, stream=STDOUT)
stats.strip_dirs()
stats.sort_stats('cumulative')
stats.print_stats()


# 示例 10
# 目的：打印调用者信息
# 解释：使用 pstats 模块打印调用者信息。
# 结果：打印调用者信息
stats = Stats(profiler, stream=STDOUT)
stats.strip_dirs()
stats.sort_stats('cumulative')
stats.print_callers()
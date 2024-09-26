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
# 目的：查找列表中指定元素的索引
# 解释：在一个包含 10 万个元素的列表中查找值为 91234 的元素的索引。
# 结果：找到元素的索引并进行断言
data = list(range(10**5))
index = data.index(91234)
assert index == 91234


# 示例 2
# 目的：查找最接近目标值的索引
# 解释：定义一个函数，遍历序列并返回最接近目标值的索引。
# 结果：找到最接近目标值的索引并进行断言
def find_closest(sequence, goal):
    """
    目的：查找最接近目标值的索引
    解释：遍历序列并返回最接近目标值的索引。
    结果：找到最接近目标值的索引
    """
    for index, value in enumerate(sequence):
        if goal < value:
            return index
    raise ValueError(f'{goal} is out of bounds')

index = find_closest(data, 91234.56)
assert index == 91235

try:
    find_closest(data, 100000000)
except ValueError:
    pass  # Expected
else:
    assert False


# 示例 3
# 目的：使用 bisect 模块查找索引
# 解释：使用 bisect_left 函数查找列表中指定值的索引。
# 结果：找到指定值的索引并进行断言
from bisect import bisect_left

index = bisect_left(data, 91234)     # Exact match
assert index == 91234

index = bisect_left(data, 91234.56)  # Closest match
assert index == 91235


# 示例 4
# 目的：比较线性查找和二分查找的性能
# 解释：使用 timeit 模块比较线性查找和二分查找的性能。
# 结果：打印两种查找方法的时间和性能差异
import random
import timeit

size = 10**5
iterations = 1000

data = list(range(size))
to_lookup = [random.randint(0, size)
             for _ in range(iterations)]

def run_linear(data, to_lookup):
    """
    目的：运行线性查找
    解释：在列表中逐个查找指定值。
    结果：完成线性查找
    """
    for index in to_lookup:
        data.index(index)

def run_bisect(data, to_lookup):
    """
    目的：运行二分查找
    解释：使用 bisect_left 函数查找指定值。
    结果：完成二分查找
    """
    for index in to_lookup:
        bisect_left(data, index)

baseline = timeit.timeit(
    stmt='run_linear(data, to_lookup)',
    globals=globals(),
    number=10)
print(f'Linear search takes {baseline:.6f}s')

comparison = timeit.timeit(
    stmt='run_bisect(data, to_lookup)',
    globals=globals(),
    number=10)
print(f'Bisect search takes {comparison:.6f}s')

slowdown = 1 + ((baseline - comparison) / comparison)
print(f'{slowdown:.1f}x time')
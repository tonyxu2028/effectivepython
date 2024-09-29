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

# 军规 12: Avoid Striding and Slicing in a Single Expression
# 军规 12: 避免在一个表达式中同时使用步长和切片
# 备注 ： 步长这个方式是为了增加运行效能的，这个玩意的使用要根据特定场景的需求来使用

"""
Avoid Striding and Slicing in a Single Expression
避免在一个表达式中同时使用步长和切片
"""

import random
import sys

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

# 配置日志将输出到 stdout 而不是 stderr
logging.basicConfig(stream=sys.stdout, level=logging.INFO)


# Example 1 --- 使用步长切片提取奇偶项
# 目的：演示如何通过步长切片提取列表的奇数和偶数项。
# 解释：
# x[::2] 提取列表中的奇数项（步长为 2），x[1::2] 提取偶数项。
# 结果：分别输出奇数项和偶数项。
print(f"\n{'Example 1':*^50}")
x = ['red', 'orange', 'yellow', 'green', 'blue', 'purple']
odds = x[::2]
evens = x[1::2]
print(odds)
print(evens)


# Example 2 --- 对字节串使用步长切片，这个是一种步长的使用方式
# 目的：展示如何使用步长切片反转字节串。
# 解释：
# 对字节串 x 进行切片操作 x[::-1]，可以反转字节串。
# 结果：输出字节串 'mongoose' 的反转版本。
print(f"\n{'Example 2':*^50}")
x = b'mongoose'
y = x[::-1]
print(y)


# Example 3 --- 对字符串使用步长切片
# 目的：展示如何对字符串进行步长切片。
# 解释：
# 字符串和字节串类似，使用 x[::-1] 可以反转整个字符串。
# 结果：输出字符串 '寿司' 的反转结果。
print(f"\n{'Example 3':*^50}")
x = '寿司'
y = x[::-1]
print(y)


# Example 4 --- 对字节串使用步长切片引发编码错误
# 目的：演示对字节串进行反转后尝试解码为 UTF-8 时引发的错误。
# 解释：
# 对 UTF-8 编码的字节串进行步长切片后，字节顺序会被打乱，导致解码失败。
# 结果：引发 UnicodeDecodeError，记录异常。
# 输出 ： ERROR:root:Error type: UnicodeDecodeError, Message: 'utf-8' codec
# can't decode byte 0xb8 in position 0: invalid start byte
print(f"\n{'Example 4':*^50}")
try:
    w = '寿司'
    x = w.encode('utf-8')
    y = x[::-1]             # 输出 b'\x8f\x9f\x8f\x9f\x8f\x9f\x8f\x9f'
    z = y.decode('utf-8')
except Exception as e:
    logging.error(f"Error type: {e.__class__.__name__}, Message: {str(e)}")
else:
    assert False


# Example 5 --- 更多步长切片示例
# 目的：演示如何通过步长正反向切片获取列表的不同子集。
# 解释：
# x[::2] 提取列表的奇数项，x[::-2] 提取反向偶数项。
# 结果：分别输出对应的切片结果。
print(f"\n{'Example 5':*^50}")
x = ['a', 'b', 'c', 'd', 'e', 'f', 'g', 'h']
x[::2]   # ['a', 'c', 'e', 'g']
x[::-2]  # ['h', 'f', 'd', 'b']


# Example 6 --- 结合步长和切片操作
# 目的：展示如何通过结合步长和切片操作获取列表的不同部分。
# 解释：
# 通过不同的起始、结束位置和步长，提取列表的不同部分。
# 结果：分别展示了各种步长切片的结果。
print(f"\n{'Example 6':*^50}")
x[2::2]     # ['c', 'e', 'g']
x[-2::-2]   # ['g', 'e', 'c', 'a']
x[-2:2:-2]  # ['g', 'e']
x[2:2:-2]   # []


# Example 7 --- 步长切片的多层切片
# 目的：展示步长切片的多层操作。
# 解释：
# 通过对步长切片 y 再次进行切片，提取其中的一部分元素。
# 结果：分别展示原始列表 x 和步长切片 y 及其子集 z。
print(f"\n{'Example 7':*^50}")
y = x[::2]   # ['a', 'c', 'e', 'g']
# y[1:-1] 表示对序列 y 进行切片操作：
# 1：起始索引，表示从索引 1 开始（即第二个元素）。
# -1：结束索引，表示切片到倒数第二个元素（不包括倒数第一个元素）。在 Python 中，负索引用于从序列末尾开始计数。
# 结果：这个切片会提取从第二个元素到倒数第二个元素的所有内容，但不包括最后一个元素。
z = y[1:-1]  # ['c', 'e']
print(x)
print(y)
print(z)

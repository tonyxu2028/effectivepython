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
    everything = gc.get_objects()
    for obj in everything:
        if isinstance(obj, io.IOBase):
            obj.close()

atexit.register(close_open_files)


# Example 1 --- 创建文件并写入随机长度的字符串
# 目的：生成一个文件，其中每一行是随机长度的'a'字符
# 结果：输出每行字符的长度。
with open('my_file.txt', 'w') as f:
    for _ in range(10):
        f.write('a' * random.randint(0, 100))
        f.write('\n')

value = [len(x) for x in open('my_file.txt')]
print(value)


# Example 2 --- 使用生成器表达式
# 目的：创建一个生成器来获取文件中每行的长度
# 结果：生成器本身不会立即计算。
it = (len(x) for x in open('my_file.txt'))
print(it)


# Example 3 --- 获取生成器的下一个值
# 目的：演示如何从生成器中获取值
# 结果：输出第一行的长度。
print(next(it))
print(next(it))


# Example 4 --- 计算平方根
# 目的：为每个长度计算平方根并生成元组
# 结果：创建一个新的生成器。
roots = ((x, x**0.5) for x in it)


# Example 5 --- 获取平方根生成器的下一个值
# 目的：输出当前的平方根值
# 结果：显示平方根的值，但注意此时生成器已经耗尽。
print(next(roots))

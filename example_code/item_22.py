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

# 军规 22: Reduce Visual Noise with Variable Positional Arguments
# 军规 22: 使用可变位置参数减少视觉干扰

"""
Reduce Visual Noise with Variable Positional Arguments
使用可变位置参数减少视觉干扰。

核心本质：
这一规则的核心在于简化函数签名和调用的复杂性，特别是在处理多个可选参数时，
避免让函数的调用变得过于冗长或复杂，从而减少视觉干扰，让代码更简洁、易读。

减少视觉噪音：
    当函数需要处理很多参数时，如果每个参数都明确列出，会让代码变得臃肿且难以理解。
    通过使用 *args 可以隐藏不必要的细节，减少函数签名的冗长。

灵活性：
    *args 提供了很大的灵活性，特别是在你无法预知参数数量时（如处理不定参数的场景）。
    调用者可以传递任意数量的参数，函数也可以根据需要处理这些参数，而不必每次都修改函数签名。
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


# Example 1 --- 初始实现的日志函数
# 目的：展示如何通过位置参数传递消息和列表值。
# 解释：
# log 函数接受两个参数，message 和 values，
# 如果 values 列表为空，仅打印消息，否则打印消息和 values。
# 结果：输出日志消息和数值列表。
print(f"\n{'Example 1':*^50}")
def log(message, values):
    if not values:
        print(message)
    else:
        values_str = ', '.join(str(x) for x in values)
        print(f'{message}: {values_str}')

log('My numbers are', [1, 2])
log('Hi there', [])


# Example 2 --- 使用 *args 简化日志函数
# 目的：展示如何通过 *args 实现可变数量参数的传递。
# 解释：
# 通过使用 *args，可以传递任意数量的参数，函数内部将其视作元组处理，这样可以避免必须提供一个列表作为参数。
# 结果：调用时无需显式传递列表，可以直接传递多个数值。
print(f"\n{'Example 2':*^50}")
def log(message, *values):  # The only difference
    if not values:
        print(message)
    else:
        values_str = ', '.join(str(x) for x in values)
        print(f'{message}: {values_str}')

log('My numbers are', 1, 2)
log('Hi there')  # Much better


# Example 3 --- 使用 *args 进行解包
# 目的：展示如何使用 *args 解包列表并传递给函数。
# 解释：
# 使用 *favorites 解包列表，将其元素作为单独的参数传递给 log 函数，避免手动传递列表。
# 结果：通过解包列表，log 函数接收到多个数值。
print(f"\n{'Example 3':*^50}")
favorites = [7, 33, 99]
log('Favorite colors', *favorites)


# Example 4 --- 使用 *args 解包生成器
# 目的：展示如何通过 *args 解包生成器并将其元素传递给函数。
# 解释：
# my_generator 是一个生成器，通过 *it 解包生成器，
# 将其所有元素传递给 my_func，函数接收到的参数为生成器的所有元素。
# 结果：输出生成器中所有生成的值。
print(f"\n{'Example 4':*^50}")
def my_generator():
    for i in range(10):
        yield i # yield 则是在生成一个值后暂时挂起函数的状态，保存局部变量，并在下次迭代时从该状态继续执行

def my_func(*args):
    print(args)

it = my_generator()
my_func(*it)


# Example 5 --- 结合顺序参数和 *args
# 目的：展示如何在函数中结合位置参数和 *args。
# 解释：
# log 函数的第一个参数为顺序参数 sequence，第二个为消息，后面的所有参数通过 *args 接收并处理。
# 结果：能够根据传入的参数情况打印消息和数值，若只提供消息则只打印消息。
print(f"\n{'Example 5':*^50}")
def log(sequence, message, *values):
    if not values:
        print(f'{sequence} - {message}')
    else:
        values_str = ', '.join(str(x) for x in values)
        print(f'{sequence} - {message}: {values_str}')

log(1, 'Favorites', 7, 33)      # New with *args OK
log(1, 'Hi there')              # New message only OK
log('Favorite numbers', 7, 33,34)  # Old usage breaks

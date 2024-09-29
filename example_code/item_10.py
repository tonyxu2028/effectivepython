#!/usr/bin/env PYTHONHASHSEED=1234 python3

# Copyright 4-2019 Brett Slatkin, Pearson Education Inc.
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

"""
Prevent Repetition with Assignment Expressions
使用赋值表达式防止代码重复
描述：
这段代码展示了如何使用赋值表达式 := 来避免重复获取变量值的操作，
简化代码逻辑，尤其是在处理水果库存时的简化效果。
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

# 创建一个临时目录用于存储输出
TEST_DIR = tempfile.TemporaryDirectory()
atexit.register(TEST_DIR.cleanup)

# 确保 Windows 进程干净退出
OLD_CWD = os.getcwd()
atexit.register(lambda: os.chdir(OLD_CWD))
os.chdir(TEST_DIR.name)

# 关闭所有打开的文件
def close_open_files():
    everything = gc.get_objects()
    for obj in everything:
        if isinstance(obj, io.IOBase):
            obj.close()

atexit.register(close_open_files)


# Example 1 --- 创建水果库存字典
# 目的：演示如何创建字典来存储水果库存。
# 解释：
# fresh_fruit 是一个字典，保存了不同种类水果的数量。
# 结果：水果库存分别为 10 个苹果，8 个香蕉，5 个柠檬。
print(f"\n{'Example 1':*^50}")

fresh_fruit = {
    'apple': 10,
    'banana': 8,
    'lemon': 5,
}


# Example 2 --- 获取柠檬库存并制作柠檬水
# 目的：展示如何从字典中获取水果库存，并根据库存做出决定。
# 解释：
# 使用 fresh_fruit.get('lemon', 0) 获取柠檬数量，默认值为 0。
# 如果有柠檬，调用 make_lemonade()，否则调用 out_of_stock()。
# 结果：根据柠檬库存调用不同的函数。
print(f"\n{'Example 2':*^50}")

def make_lemonade(count):
    print(f'Making {count} lemons into lemonade')

def out_of_stock():
    # 缺货 Out of stock
    print('Out of stock!')

count = fresh_fruit.get('lemon', 0)
if count:
    make_lemonade(count)
else:
    out_of_stock()


# Example 3 --- 使用赋值表达式获取柠檬库存
# 目的：演示如何使用赋值表达式简化变量的获取和判断。
# 解释：
# 使用赋值表达式 := 同时进行赋值和判断，简化代码。
# 结果：简化了库存判断的代码结构。
print(f"\n{'Example 3':*^50}")
# 这里的:=是赋值表达式,那么判断体现在什么层面上，通过初始值0的设定来的
if count := fresh_fruit.get('lemon', 0):
    make_lemonade(count)
else:
    out_of_stock()


# Example 4 --- 获取苹果库存并制作苹果汁
# 目的：展示如何根据水果库存的条件执行特定操作。
# 解释：
# 使用 fresh_fruit.get('apple', 0) 获取苹果数量，如果数量大于等于 4，就制作苹果汁。
# 结果：根据苹果库存调用 make_cider() 或 out_of_stock()。
print(f"\n{'Example 4':*^50}")

def make_cider(count):
    print(f'Making cider with {count} apples')

count = fresh_fruit.get('apple', 0)
if count >= 4:
    make_cider(count)
else:
    out_of_stock()


# Example 5 --- 使用赋值表达式优化获取苹果库存的操作
# 目的：演示如何使用赋值表达式优化条件判断和变量赋值。
# 解释：
# 使用赋值表达式 := 同时获取苹果库存和进行条件判断，简化代码。
# 结果：简化了代码结构。
print(f"\n{'Example 5':*^50}")

if (count := fresh_fruit.get('apple', 0)) >= 4:
    make_cider(count)
else:
    out_of_stock()


# Example 6 --- 制作香蕉奶昔（带异常处理）
# 目的：演示如何结合水果库存和异常处理进行操作。
# 解释：
# 首先检查香蕉库存是否满足制作香蕉奶昔的条件，调用 slice_bananas() 函数切片。
# 之后尝试制作奶昔，如果没有足够的香蕉，抛出 OutOfBananas 异常。
# 结果：根据香蕉库存制作奶昔或处理库存不足的情况。
print(f"\n{'Example 6':*^50}")

# 该函数的功能是香蕉切片
def slice_bananas(count):
    print(f'Slicing {count} bananas')
    return count * 4

# 制作奶昔，如果没有足够的香蕉，抛出 OutOfBananas 异常
def make_smoothies(count):
    print(f'Making a smoothie with {count} banana slices')

# 定义了一个异常类OutOfBananas
class OutOfBananas(Exception):
    # pass是一个空语句，它不执行任何操作。 使用 pass 是为了保持代码结构的完整性
    pass

pieces = 0
count = fresh_fruit.get('banana', 0)
if count >= 2:
    pieces = slice_bananas(count)
try:
    make_smoothies(pieces)
except OutOfBananas:
    out_of_stock()


# Example 7 --- 用 else 语句处理库存不足的情况
# 目的：展示如何使用 else 语句处理水果库存不足的情况。
# 解释：
# 如果水果库存不足，通过 else 语句将 pieces 赋值为 0 并进行异常处理。
# 结果：在香蕉库存不足的情况下正常处理。
print(f"\n{'Example 7':*^50}")
count = fresh_fruit.get('banana', 0)
if count >= 2:
    pieces = slice_bananas(count)
else:
    pieces = 0

try:
    smoothies = make_smoothies(pieces)
except OutOfBananas:
    out_of_stock()


# Example 8 --- 使用赋值表达式优化水果库存检查
# 目的：演示如何使用赋值表达式简化库存检查和变量赋值。
# 解释：
# 使用赋值表达式 := 获取香蕉库存并判断是否制作香蕉奶昔。
# 结果：代码简化，结构更清晰。
print(f"\n{'Example 8':*^50}")
pieces = 0
if (count := fresh_fruit.get('banana', 0)) >= 2:
    pieces = slice_bananas(count)

try:
    smoothies = make_smoothies(pieces)
except OutOfBananas:
    out_of_stock()


# Example 9 --- 综合使用赋值表达式和 else 语句
# 目的：展示如何结合赋值表达式和 else 语句处理不同条件下的逻辑。
# 解释：
# 使用赋值表达式获取香蕉库存，并通过 else 语句处理库存不足的情况。
# 结果：结构简洁明了，处理不同条件下的水果库存。
print(f"\n{'Example 9':*^50}")
if (count := fresh_fruit.get('banana', 0)) >= 2:
    pieces = slice_bananas(count)
else:
    pieces = 0

try:
    smoothies = make_smoothies(pieces)
except OutOfBananas:
    out_of_stock()


# Example 10 --- 处理多个水果库存
# 目的：演示如何处理多种水果库存并选择合适的操作。
# 解释：
# 首先检查香蕉库存，如果不足再检查苹果，最后检查柠檬库存。
# 结果：根据水果库存依次制作奶昔、苹果汁或柠檬水。
print(f"\n{'Example 10':*^50}")
count = fresh_fruit.get('banana', 0)
if count >= 2:
    pieces = slice_bananas(count)
    to_enjoy = make_smoothies(pieces)
else:
    count = fresh_fruit.get('apple', 0)
    if count >= 4:
        to_enjoy = make_cider(count)
    else:
        count = fresh_fruit.get('lemon', 0)
        if count:
            to_enjoy = make_lemonade(count)
        else:
            to_enjoy = 'Nothing'


# Example 11 --- 使用赋值表达式处理多个水果库存,看来这个例子是对上一个例子的优化
# 目的：演示如何使用赋值表达式优化多种水果库存的处理逻辑。
# 解释：
# 首先检查香蕉库存，如果足够多则制作香蕉奶昔，否则检查苹果和柠檬库存，依次决定制作苹果汁或柠檬水。
# 结果：根据水果库存依次制作对应的饮品，如果没有足够水果，返回 'Nothing'。
print(f"\n{'Example 11':*^50}")
if (count := fresh_fruit.get('banana', 0)) >= 2:
    pieces = slice_bananas(count)
    to_enjoy = make_smoothies(pieces)
elif (count := fresh_fruit.get('apple', 0)) >= 4:
    to_enjoy = make_cider(count)
elif count := fresh_fruit.get('lemon', 0):
    to_enjoy = make_lemonade(count)
else:
    to_enjoy = 'Nothing'


# Example 12 --- 模拟从多个水果中选择并制作果汁
# 目的：演示如何从一系列水果中逐个取出并制作果汁。
# 解释：
# FRUIT_TO_PICK 是一个列表，包含了多个水果的库存。
# pick_fruit() 从列表中取出一个字典（表示一种水果及其数量），并在空时返回空列表。
# 结果：将每次制作的果汁添加到 bottles 列表中，最后打印所有制作的果汁。
print(f"\n{'Example 12':*^50}")
FRUIT_TO_PICK = [
    {'apple': 1, 'banana': 3},
    {'lemon': 2, 'lime': 5},
    {'orange': 3, 'melon': 2},
]

def pick_fruit():
    if FRUIT_TO_PICK:
        return FRUIT_TO_PICK.pop(0)
    else:
        return []

def make_juice(fruit, count):
    return [(fruit, count)]

bottles = []
fresh_fruit = pick_fruit()
while fresh_fruit:
    for fruit, count in fresh_fruit.items():
        batch = make_juice(fruit, count)
        bottles.extend(batch)
    fresh_fruit = pick_fruit()

print(bottles)


# Example 13 --- 使用 while 循环和 break 来控制果汁制作过程
# 目的：演示如何使用无限循环和 break 语句处理果汁制作的过程。
# 解释：
# 使用 while True 创建无限循环，通过在列表为空时调用 break 提前退出循环。
# 结果：每次从 FRUIT_TO_PICK 中取出一种水果，制作果汁并添加到 bottles 列表中，最后打印结果。
print(f"\n{'Example 13':*^50}")
FRUIT_TO_PICK = [
    {'apple': 1, 'banana': 3},
    {'lemon': 2, 'lime': 5},
    {'orange': 3, 'melon': 2},
]

bottles = []
while True:                     # Loop
    fresh_fruit = pick_fruit()
    if not fresh_fruit:         # And a half
        break
    for fruit, count in fresh_fruit.items():
        batch = make_juice(fruit, count)
        bottles.extend(batch)

print(bottles)


# Example 14 --- 使用赋值表达式优化果汁制作循环
# 目的：演示如何使用赋值表达式简化 while 循环的逻辑。
# 解释：
# 使用赋值表达式同时获取 fresh_fruit 并进行判断，避免了在 while 循环中使用 break 提前退出。
# 结果：简化了无限循环的逻辑，同时保持了同样的功能。
print(f"\n{'Example 14':*^50}")
FRUIT_TO_PICK = [
    {'apple': 1, 'banana': 3},
    {'lemon': 2, 'lime': 5},
    {'orange': 3, 'melon': 2},
]

bottles = []
while fresh_fruit := pick_fruit():
    for fruit, count in fresh_fruit.items():
        batch = make_juice(fruit, count)
        bottles.extend(batch)

print(bottles)
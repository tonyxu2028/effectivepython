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

"""
Understand the Else Block in Loops
理解循环中的 Else 代码块
# 全局描述：
# 主题：理解循环中的 Else 代码块
# 描述：
# 这段代码通过多个例子演示了 for 和 while 循环中的 else 代码块的行为，
# 尤其是在循环正常完成和使用 break 提前退出时的区别。
# 示例解释：
# Example 1 演示了 for 循环正常结束时 else 代码块的执行。
# Example 2 介绍了使用 break 提前退出时，else 代码块不会执行。
# Example 3 和 4 进一步展示了在空循环或 while False 的情况下，else 块仍然会运行。
# Example 5 - 7 则深入到如何利用 for-else 逻辑检查两个数是否互质，以及将逻辑封装到函数中。
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


# Example 1 --- for 循环中执行 Else 代码块
# 目的：演示如何在 for 循环执行完所有迭代后运行 Else 代码块。
# 解释：
# 当 for 循环顺利执行完时，Else 代码块会被触发。
# 结果：for 循环完成 3 次迭代后，Else 代码块被触发。
# 输出：
# Loop 0
# Loop 1
# Loop 2
# Else block!
print(f"\n{'Example 1':*^50}")
for i in range(3):
    print('Loop', i)
else:
    print('Else block!')


# Example 2 --- for 循环中使用 break
# 目的：演示在 for 循环中遇到 break 时，Else 代码块不会执行。
# 解释：
# 当 for 循环中使用 break 提前终止时，Else 代码块不会被触发。
# 结果：在第二次迭代时 break，Else 代码块不会被执行。
# 输出：
# Loop 0
# Loop 1
print(f"\n{'Example 2':*^50}")
for i in range(3):
    print('Loop', i)
    if i == 1:
        break
else:
    print('Else block!')


# Example 3 --- for 循环迭代空列表
# 目的：演示当 for 循环的可迭代对象为空时，直接执行 Else 代码块。
# 解释：
# 如果 for 循环的可迭代对象是空的，循环体不会执行，但 Else 代码块会直接运行。
# 结果：循环体不会执行，但 Else 代码块会被触发。
# 输出：
# For Else block!
print(f"\n{'Example 3':*^50}")
for x in []:
    print('Never runs')
else:
    print('For Else block!')


# Example 4 --- while 循环中的 Else 代码块
# 目的：演示 while 循环条件为 False 时，直接执行 Else 代码块。
# 解释：
# 当 while 循环条件一开始就是 False 时，Else 代码块会直接执行。
# 结果：循环体不会执行，但 Else 代码块会被触发。
# 输出：
# While Else block!
print(f"\n{'Example 4':*^50}")
while False:
    print('Never runs')
else:
    print('While Else block!')


# Example 5 --- 检查两个数是否互质
# 目的：演示如何使用 for 和 else 代码块检查两个数是否互质。
# 解释：
# 通过 for 循环从 2 到 min(a, b)，检查 a 和 b 是否有共同的因子。
# 如果发现共同因子，直接 break；否则，Else 代码块表示 a 和 b 是互质数。
# 结果：
# 4 和 9 是互质数，循环正常结束，Else 代码块执行。
# 输出：
# Testing 2
# Testing 3
# Coprime
print(f"\n{'Example 5':*^50}")
a = 4
b = 9

for i in range(2, min(a, b) + 1):
    print('Testing', i)
    if a % i == 0 and b % i == 0:
        print('Not coprime')
        break
else:
    print('Coprime')


# Example 6 --- 函数版互质判断
# 目的：将检查互质的逻辑封装到函数中。
# 解释：
# 函数 coprime(a, b) 使用 for 循环检查 a 和 b 是否有共同因子。
# 如果找到共同因子，返回 False；否则返回 True，表示 a 和 b 是互质。
# 结果：4 和 9 是互质，3 和 6 不是。
print(f"\n{'Example 6':*^50}")
def coprime(a, b):
    for i in range(2, min(a, b) + 1):
        if a % i == 0 and b % i == 0:
            return False
    return True
print(f"coprime(4, 9) ::: {coprime(4, 9)}")
print(f"coprime(3, 6) ::: {coprime(3, 6)}")
assert coprime(4, 9)
assert not coprime(3, 6)


# Example 7 --- 使用布尔变量代替 else
# 目的：演示如何使用布尔变量代替 Else 代码块判断互质性。
# 解释：
# 通过布尔变量 is_coprime 标识是否找到共同因子。如果找到，提前返回 False。
# 否则，返回 is_coprime 的值，表示 a 和 b 是否互质。
# 结果：4 和 9 是互质，3 和 6 不是。
print(f"\n{'Example 7':*^50}")
def coprime_alternate(a, b):
    is_coprime = True
    for i in range(2, min(a, b) + 1):
        if a % i == 0 and b % i == 0:
            is_coprime = False
            break
    return is_coprime
print(f"coprime_alternate(4, 9) ::: {coprime_alternate(4, 9)}")
print(f"coprime_alternate(3, 6) ::: {coprime_alternate(3, 6)}")
assert coprime_alternate(4, 9)
assert not coprime_alternate(3, 6)

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

# Write Helper Functions Instead of Complex Expressions
# 使用辅助函数取代复杂的表达式

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


# Example 1 --- 使用 parse_qs 解析查询字符串
# 目的： 演示如何使用 parse_qs 来解析查询字符串。
from urllib.parse import parse_qs
# 解释：
# parse_qs 解析了查询字符串 'red=5&blue=0&green='，并返回一个字典。
# keep_blank_values=True 参数确保即使某些值为空（比如 green），也不会被忽略。
# 字典中的键是参数名，值是一个列表，比如 'red': ['5']。
print(f"\n{'Example 1':*^50}")
my_values = parse_qs('red=5&blue=0&green=',
                     keep_blank_values=True)
# 输出：{'red': ['5'], 'blue': ['0'], 'green': ['']}
print(repr(my_values))


# Example 2 --- 访问解析后的值
# 目的： 演示如何从解析后的字典中获取值。
# 解释：
# my_values.get('red') 获取 'red' 的值，它是 ['5']。
# my_values.get('green') 返回 ['']，即使值为空它也不会被忽略。
# my_values.get('opacity') 返回 None，因为查询字符串中没有 opacity 这个键。
print(f"\n{'Example 2':*^50}")
print('Red:     ', my_values.get('red'))
print('Green:   ', my_values.get('green'))
print('Opacity: ', my_values.get('opacity'))


# Example 3 --- 处理可能为空的值
# 目的： 演示如何处理可能为空或不存在的值。
# 解释：
# my_values.get('red', [''])[0] or 0 会获取 'red' 的第一个值，如果该值为空，就返回 0。
# 对于 green 和 opacity 也是一样的处理逻辑，这样即使值是空的或者键不存在，也会得到一个默认的 0。
# 结果：
# Red:     '5'
# Green:   0
# Opacity: 0
print(f"\n{'Example 3':*^50}")
red = my_values.get('red', [''])[0] or 0
green = my_values.get('green', [''])[0] or 0
opacity = my_values.get('opacity', [''])[0] or 0
print(f'Red:     {red!r}')
print(f'Green:   {green!r}')
print(f'Opacity: {opacity!r}')


# Example 4 --- 将字符串转换为整数
# 目的： 演示如何将从查询字符串中提取的值转换为整数。
# 解释：
# int() 用于将值从字符串转换为整数。my_values.get('red', [''])[0] or 0 确保获取的值非空，才能转换成整数。
# green 和 opacity 都是空的，所以会被转换成 0。
print(f"\n{'Example 4':*^50}")
red = int(my_values.get('red', [''])[0] or 0)
green = int(my_values.get('green', [''])[0] or 0)
opacity = int(my_values.get('opacity', [''])[0] or 0)
print(f'Red:     {red!r}')
print(f'Green:   {green!r}')
print(f'Opacity: {opacity!r}')


# Example 5 --- 优化字符串到整数的转换
# 目的： 演示如何优化字符串到整数的转换过程。
# 解释：
# 这里首先获取字符串，然后判断该字符串是否为空，再决定是否将其转换为整数。
# 如果是空字符串，则直接返回 0，避免出错。
# 结果：
# Red:     5
# Green:   0
# Opacity: 0
print(f"\n{'Example 5':*^50}")
red_str = my_values.get('red', [''])
red = int(red_str[0]) if red_str[0] else 0
green_str = my_values.get('green', [''])
green = int(green_str[0]) if green_str[0] else 0
opacity_str = my_values.get('opacity', [''])
opacity = int(opacity_str[0]) if opacity_str[0] else 0
print(f'Red:     {red!r}')
print(f'Green:   {green!r}')
print(f'Opacity: {opacity!r}')


# Example 6 --- 使用 if-else 来判断和转换值
# 目的： 演示如何使用 if-else 来判断值是否为空并进行处理。
# 解释：
# if green_str[0] 判断是否有值，如果有就转换成整数。
# 否则，green 被设为 0，确保安全无误。
# green 又是 0，但这次你是用 if-else 判断出来的，控制力更强~
print(f"\n{'Example 6':*^50}")
green_str = my_values.get('green', [''])
if green_str[0]:
    green = int(green_str[0])
else:
    green = 0
print(f'Green:   {green!r}')


# Example 7 --- 封装成函数来获取整数
# 目的： 封装成函数来简化获取整数值的过程。
# 解释：
# get_first_int 函数封装了之前的逻辑：从查询字符串中提取某个键的值，并将其转换为整数。
# 如果值不存在或为空，则返回默认值 default。
# 结果： 没有直接输出，因为这是一个封装好的函数。你可以放心使用它去取各种键的值，简单又高效！
print(f"\n{'Example 7':*^50}")
def get_first_int(values, key, default=0):
    found = values.get(key, [''])
    if found[0]:
        return int(found[0])
    return default


# Example 8 --- 使用封装函数获取值
# 目的： 演示如何使用封装函数来获取值。
# 解释：
# 通过 get_first_int 来获取 'green' 的值，确保返回的值是整数。
# 如果 'green' 为空，函数会返回默认值 0。
print(f"\n{'Example 8':*^50}")
my_values = parse_qs('red=5&blue=0&green=',
                     keep_blank_values=True)
green = get_first_int(my_values, 'green')
print(f'Green:   {green!r}')

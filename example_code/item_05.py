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
print('Red:     ', my_values.get('red'))
print('Green:   ', my_values.get('green'))
print('Opacity: ', my_values.get('opacity'))


# Example 3 --- 元组的不可变性
red = my_values.get('red', [''])[0] or 0
green = my_values.get('green', [''])[0] or 0
opacity = my_values.get('opacity', [''])[0] or 0
print(f'Red:     {red!r}')
print(f'Green:   {green!r}')
print(f'Opacity: {opacity!r}')


# Example 4
red = int(my_values.get('red', [''])[0] or 0)
green = int(my_values.get('green', [''])[0] or 0)
opacity = int(my_values.get('opacity', [''])[0] or 0)
print(f'Red:     {red!r}')
print(f'Green:   {green!r}')
print(f'Opacity: {opacity!r}')


# Example 5
red_str = my_values.get('red', [''])
red = int(red_str[0]) if red_str[0] else 0
green_str = my_values.get('green', [''])
green = int(green_str[0]) if green_str[0] else 0
opacity_str = my_values.get('opacity', [''])
opacity = int(opacity_str[0]) if opacity_str[0] else 0
print(f'Red:     {red!r}')
print(f'Green:   {green!r}')
print(f'Opacity: {opacity!r}')


# Example 6
green_str = my_values.get('green', [''])
if green_str[0]:
    green = int(green_str[0])
else:
    green = 0
print(f'Green:   {green!r}')


# Example 7
def get_first_int(values, key, default=0):
    found = values.get(key, [''])
    if found[0]:
        return int(found[0])
    return default


# Example 8
green = get_first_int(my_values, 'green')
print(f'Green:   {green!r}')

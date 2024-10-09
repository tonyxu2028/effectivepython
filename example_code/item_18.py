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

# 军规 18: Know How to Construct Key-Dependent Default Values with __missing__
# 军规 18: 了解如何使用 __missing__ 构造基于键的默认值

"""
军规 18: Know How to Construct Key-Dependent Default Values with __missing__
军规 18: 了解如何使用 __missing__ 构造基于键的默认值
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

# Example 1 --- 使用赋值表达式打开图片文件
# 目的：展示如何使用赋值表达式（海象运算符）打开图片文件并避免重复打开文件。
# 解释：
# 通过 pictures.get() 检查文件是否已经打开，若未打开则打开并存储在字典中。
# 结果：输出图片文件句柄和文件内容。
print(f"\n{'Example 1':*^50}")
pictures = {}
path = 'profile_1234.png'

with open(path, 'wb') as f:
    f.write(b'image data here 1234')

if (handle := pictures.get(path)) is None:
    try:
        handle = open(path, 'a+b')
    except OSError:
        print(f'Failed to open path {path}')
        raise
    else:
        pictures[path] = handle

handle.seek(0)
image_data = handle.read()

print(pictures)
print(image_data)

# Example 2 --- 使用 in 和 KeyError 处理缺失文件
# 目的：展示如何使用 in 操作符和 try-except 捕获 KeyError 处理缺失的文件。
# 解释：
# 首先使用 in 操作符判断文件是否已打开，如果未打开则尝试打开并存入字典；另一种方式是捕获 KeyError 进行处理。
# 结果：输出图片文件句柄和文件内容。
print(f"\n{'Example 2':*^50}")
# 使用 in 操作符
pictures = {}
path = 'profile_9991.png'

with open(path, 'wb') as f:
    f.write(b'image data here 9991')

if path in pictures:
    handle = pictures[path]
else:
    try:
        handle = open(path, 'a+b')
    except OSError:
        print(f'Failed to open path {path}')
        raise
    else:
        pictures[path] = handle

handle.seek(0)
image_data = handle.read()

print(pictures)
print(image_data)

# 使用 KeyError
pictures = {}
path = 'profile_9922.png'

with open(path, 'wb') as f:
    f.write(b'image data here 9991')

try:
    handle = pictures[path]
except KeyError:
    try:
        handle = open(path, 'a+b')
    except OSError:
        print(f'Failed to open path {path}')
        raise
    else:
        pictures[path] = handle

handle.seek(0)
image_data = handle.read()

print(pictures)
print(image_data)

# Example 3 --- 使用 setdefault 打开文件
# 目的：展示如何使用 setdefault 方法处理缺失的文件句柄。
# 解释：
# pictures.setdefault(path, open(path, 'a+b')) 尝试打开文件，如果文件句柄不存在则打开文件并存入字典。
# 结果：输出图片文件句柄和文件内容。
print(f"\n{'Example 3':*^50}")
pictures = {}
path = 'profile_9239.png'

with open(path, 'wb') as f:
    f.write(b'image data here 9239')

try:
    handle = pictures.setdefault(path, open(path, 'a+b'))
except OSError:
    print(f'Failed to open path {path}')
    raise
else:
    handle.seek(0)
    image_data = handle.read()

print(pictures)
print(image_data)

# Example 4 --- 使用 defaultdict 简化文件打开操作
# 目的：展示如何通过 defaultdict 来自动处理文件的缺失。
# 解释：
# defaultdict(open_picture) 在缺少键时自动调用 open_picture 函数打开文件并存储文件句柄。
# 结果：输出文件句柄和文件内容，若文件不存在则捕获并记录异常。
print(f"\n{'Example 4':*^50}")
try:
    path = 'profile_4555.csv'

    with open(path, 'wb') as f:
        f.write(b'image data here 9239')

    from collections import defaultdict


    def open_picture(profile_path):
        try:
            return open(profile_path, 'a+b')
        except OSError:
            print(f'Failed to open path {profile_path}')
            raise


    pictures = defaultdict(open_picture)
    handle = pictures[path]
    handle.seek(0)
    image_data = handle.read()
except:
    logging.exception('Expected')
else:
    assert False

# Example 5 --- 自定义字典类处理文件缺失
# 目的：展示如何通过自定义字典类处理缺失的文件句柄。
# 解释：
# Pictures 类继承自 dict，通过实现 __missing__ 方法在键缺失时自动打开文件并存储文件句柄。
# 结果：使用 Pictures 类处理文件缺失时自动打开文件并输出文件内容。
print(f"\n{'Example 5':*^50}")
path = 'account_9090.csv'

with open(path, 'wb') as f:
    f.write(b'image data here 9090')


def open_picture(profile_path):
    try:
        return open(profile_path, 'a+b')
    except OSError:
        print(f'Failed to open path {profile_path}')
        raise


class Pictures(dict):
    def __missing__(self, key):
        value = open_picture(key)    # 当键缺失时，调用 open_picture(key) 加载图片
        self[key] = value            # 将加载的图片缓存到字典中
        return value


pictures = Pictures()
handle = pictures[path]
handle.seek(0)
image_data = handle.read()
print(pictures)
print(image_data)

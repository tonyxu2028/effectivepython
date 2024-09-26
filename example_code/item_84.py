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
    解释：遍历所有对象并关闭所有 io.IOBase 实例。
    结果：所有打开的文件都被关闭
    """
    everything = gc.get_objects()
    for obj in everything:
        if isinstance(obj, io.IOBase):
            obj.close()

atexit.register(close_open_files)


# 示例 1
# 目的：定义一个判断回文的函数
# 解释：创建一个函数，判断给定的单词是否是回文。
# 结果：成功定义函数并进行断言测试
def palindrome(word):
    """判断给定的单词是否是回文"""
    return word == word[::-1]

assert palindrome('tacocat')
assert not palindrome('banana')


# 示例 2
# 目的：打印函数的文档字符串
# 解释：使用 repr 函数打印 palindrome 函数的文档字符串。
# 结果：成功打印文档字符串
print(repr(palindrome.__doc__))


# 示例 3
# 目的：定义一个用于查找语言模式的库
# 解释：创建一个模块，提供判断单词是否具有特殊属性的功能。
# 结果：成功定义模块并列出可用函数
"""用于查找单词中语言模式的库。

测试单词之间的关系有时可能很棘手！
该模块提供了简单的方法来确定您找到的单词是否具有特殊属性。

可用函数：
- palindrome: 判断单词是否是回文。
- check_anagram: 判断两个单词是否是变位词。
...
"""


# 示例 4
# 目的：定义一个表示游戏玩家的类
# 解释：创建一个类，表示游戏玩家，并提供公共属性和方法。
# 结果：成功定义类并列出公共属性
class Player:
    """表示游戏玩家的类。

    子类可以重写 'tick' 方法，根据玩家的能量等级等提供自定义动画。

    公共属性：
    - power: 未使用的能量提升（0 到 1 之间的浮点数）。
    - coins: 在关卡中找到的硬币（整数）。
    """


# 示例 5
# 目的：定义一个查找变位词的函数
# 解释：创建一个函数，查找给定单词的所有变位词。
# 结果：成功定义函数并进行断言测试
import itertools
def find_anagrams(word, dictionary):
    """
    目的：查找单词的所有变位词
    解释：该函数的运行速度仅取决于 'dictionary' 容器中成员测试的速度。
    结果：返回找到的变位词列表，如果没有找到则返回空列表
    """
    permutations = itertools.permutations(word, len(word))
    possible = (''.join(x) for x in permutations)
    found = {word for word in possible if word in dictionary}
    return list(found)

assert find_anagrams('pancakes', ['scanpeak']) == ['scanpeak']
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

#这设置了 Python 的随机数生成器的种子，以确保每次生成的随机数序列是一致的。
random.seed(1234)

# 这是 Python 的内置日志模块，用于生成日志信息。虽然这里并没有使用 logging，但可能是为了后续的示例或输出。
import logging
# 导入 pprint，用于美化打印 Python 对象，让输出更加可读。
from pprint import pprint
# 将 sys.stdout 重命名为 STDOUT，以便后续代码可以使用 STDOUT 代替 sys.stdout 进行输出。
from sys import stdout as STDOUT

# Write all output to a temporary directory
# atexit 模块 提供了在程序正常退出时执行函数的能力。
# 通过 atexit.register() 函数，
# 你可以注册一些函数，这些函数会在程序正常终止时自动调用。
import atexit
# gc 模块 控制 Python 的垃圾回收器。Python 使用引用计数和垃圾回收机制来管理内存，
# gc 模块提供了一些额外的工具来控制和调试内存管理过程，尤其是循环引用的情况
# （即两个对象互相引用，导致引用计数永远不为 0，但它们又不再需要时）。
import gc
# io 模块 提供了 Python 的核心 IO 功能，包括文件操作、流操作等。
import io
# os 模块 提供了访问操作系统服务的功能，包括文件操作、进程管理、环境变量等。
import os
# tempfile 模块 提供了创建临时文件和目录的功能。
import tempfile

# 创建一个临时目录，用于存放输出文件。
TEST_DIR = tempfile.TemporaryDirectory()
# 注册一个函数，当程序退出时，清理临时目录。
atexit.register(TEST_DIR.cleanup)

# Make sure Windows processes exit cleanly
# 保存当前工作目录，以便在程序退出时恢复
OLD_CWD = os.getcwd()
# 注册一个函数，当程序退出时，恢复当前工作目录
atexit.register(lambda: os.chdir(OLD_CWD))
# 将当前工作目录切换到临时目录
os.chdir(TEST_DIR.name)

"""
这个函数用于关闭所有打开的文件。
它通过 gc.get_objects() 获取当前 Python 进程中的所有对象，
"""
def close_open_files():
    everything = gc.get_objects()
    for obj in everything:
        if isinstance(obj, io.IOBase):
            obj.close()

# 注册一个函数，当程序退出时，关闭所有打开的文件。
atexit.register(close_open_files)

# Example 1
# sys 模块 提供了 Python 解释器的一些变量和函数，包括与 Python 解释器交互的函数。
import sys

# 输出 Python 的版本信息
print(sys.version_info)
# 输出 Python 的版本号
print(sys.version)

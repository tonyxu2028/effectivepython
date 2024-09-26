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
# 目的：定义一个计算重量的函数
# 解释：创建一个函数，计算给定体积和密度的重量，并进行异常处理。
# 结果：成功定义函数并进行断言测试
def determine_weight(volume, density):
    """计算重量"""
    if density <= 0:
        raise ValueError('Density must be positive')


try:
    determine_weight(1, 0)
except ValueError:
    pass
else:
    assert False


# 示例 2
# 目的：定义自定义异常类
# 解释：创建自定义异常类，用于处理密度和体积的异常情况。
# 结果：成功定义自定义异常类
class Error(Exception):
    """模块中所有异常的基类"""


class InvalidDensityError(Error):
    """提供的密度值有问题"""


class InvalidVolumeError(Error):
    """提供的体积值有问题"""


def determine_weight(volume, density):
    """计算重量"""
    if density < 0:
        raise InvalidDensityError('Density must be positive')
    if volume < 0:
        raise InvalidVolumeError('Volume must be positive')
    if volume == 0:
        density / volume


# 示例 3
# 目的：定义一个包含异常处理的模块类
# 解释：创建一个模块类，包含异常处理和计算重量的方法。
# 结果：成功定义模块类并进行断言测试
class my_module:
    Error = Error
    InvalidDensityError = InvalidDensityError

    @staticmethod
    def determine_weight(volume, density):
        """计算重量"""
        if density < 0:
            raise InvalidDensityError('Density must be positive')
        if volume < 0:
            raise InvalidVolumeError('Volume must be positive')
        if volume == 0:
            density / volume


try:
    weight = my_module.determine_weight(1, -1)
except my_module.Error:
    logging.exception('Unexpected error')
else:
    assert False

# 示例 4
# 目的：使用哨兵对象进行异常处理
# 解释：使用哨兵对象和异常处理来测试计算重量的方法。
# 结果：成功使用哨兵对象进行异常处理
SENTINEL = object()
weight = SENTINEL
try:
    weight = my_module.determine_weight(-1, 1)
except my_module.InvalidDensityError:
    weight = 0
except my_module.Error:
    logging.exception('Bug in the calling code')
else:
    assert False

assert weight is SENTINEL

# 示例 5
# 目的：嵌套异常处理
# 解释：使用嵌套的异常处理来测试计算重量的方法。
# 结果：成功进行嵌套异常处理并进行断言测试
try:
    weight = SENTINEL
    try:
        weight = my_module.determine_weight(0, 1)
    except my_module.InvalidDensityError:
        weight = 0
    except my_module.Error:
        logging.exception('Bug in the calling code')
    except Exception:
        logging.exception('Bug in the API code!')
        raise  # Re-raise exception to the caller
    else:
        assert False

    assert weight == 0
except:
    logging.exception('Expected')
else:
    assert False


# 示例 6
# 目的：定义一个新的异常类
# 解释：创建一个新的异常类，用于处理负密度值的情况。
# 结果：成功定义新的异常类
class NegativeDensityError(InvalidDensityError):
    """提供的密度值为负"""


def determine_weight(volume, density):
    """计算重量"""
    if density < 0:
        raise NegativeDensityError('Density must be positive')


# 示例 7
# 目的：使用新的异常类进行异常处理
# 解释：使用新的异常类和异常处理来测试计算重量的方法。
# 结果：成功使用新的异常类进行异常处理
try:
    my_module.NegativeDensityError = NegativeDensityError
    my_module.determine_weight = determine_weight
    try:
        weight = my_module.determine_weight(1, -1)
    except my_module.NegativeDensityError:
        raise ValueError('Must supply non-negative density')
    except my_module.InvalidDensityError:
        weight = 0
    except my_module.Error:
        logging.exception('Bug in the calling code')
    except Exception:
        logging.exception('Bug in the API code!')
        raise
    else:
        assert False
except:
    logging.exception('Expected')
else:
    assert False


# 示例 8
# 目的：定义多个异常类
# 解释：创建多个异常类，用于处理重量、体积和密度的异常情况。
# 结果：成功定义多个异常类
class Error(Exception):
    """模块中所有异常的基类"""


class WeightError(Error):
    """重量计算错误的基类"""


class VolumeError(Error):
    """体积计算错误的基类"""


class DensityError(Error):
    """密度计算错误的基类"""
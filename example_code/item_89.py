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
# 目的：定义一个计算距离的函数
# 解释：创建一个函数，计算给定速度和持续时间的距离。
# 结果：成功定义函数并进行断言测试
def print_distance(speed, duration):
    """计算距离"""
    distance = speed * duration
    print(f'{distance} miles')

print_distance(5, 2.5)


# 示例 2
# 目的：测试 print_distance 函数
# 解释：调用 print_distance 函数并传入参数。
# 结果：成功调用函数并打印结果
print_distance(1000, 3)


# 示例 3
# 目的：定义单位转换函数
# 解释：创建一个字典和两个函数，用于转换和本地化单位。
# 结果：成功定义字典和函数
CONVERSIONS = {
    'mph': 1.60934 / 3600 * 1000,   # m/s
    'hours': 3600,                  # seconds
    'miles': 1.60934 * 1000,        # m
    'meters': 1,                    # m
    'm/s': 1,                       # m
    'seconds': 1,                   # s
}

def convert(value, units):
    """转换单位"""
    rate = CONVERSIONS[units]
    return rate * value

def localize(value, units):
    """本地化单位"""
    rate = CONVERSIONS[units]
    return value / rate

def print_distance(speed, duration, *,
                   speed_units='mph',
                   time_units='hours',
                   distance_units='miles'):
    """计算距离并打印"""
    norm_speed = convert(speed, speed_units)
    norm_duration = convert(duration, time_units)
    norm_distance = norm_speed * norm_duration
    distance = localize(norm_distance, distance_units)
    print(f'{distance} {distance_units}')


# 示例 4
# 目的：测试 print_distance 函数
# 解释：调用 print_distance 函数并传入不同单位的参数。
# 结果：成功调用函数并打印结果
print_distance(1000, 3,
               speed_units='meters',
               time_units='seconds')


# 示例 5
# 目的：添加警告信息
# 解释：修改 print_distance 函数，添加警告信息以提醒用户提供单位参数。
# 结果：成功添加警告信息并调用函数
import warnings

def print_distance(speed, duration, *,
                   speed_units=None,
                   time_units=None,
                   distance_units=None):
    """计算距离并打印"""
    if speed_units is None:
        warnings.warn(
            'speed_units required', DeprecationWarning)
        speed_units = 'mph'

    if time_units is None:
        warnings.warn(
            'time_units required', DeprecationWarning)
        time_units = 'hours'

    if distance_units is None:
        warnings.warn(
            'distance_units required', DeprecationWarning)
        distance_units = 'miles'

    norm_speed = convert(speed, speed_units)
    norm_duration = convert(duration, time_units)
    norm_distance = norm_speed * norm_duration
    distance = localize(norm_distance, distance_units)
    print(f'{distance} {distance_units}')


# 示例 6
# 目的：重定向标准错误输出
# 解释：使用 contextlib.redirect_stderr 重定向标准错误输出并捕获警告信息。
# 结果：成功重定向标准错误输出并捕获警告信息
import contextlib
import io

fake_stderr = io.StringIO()
with contextlib.redirect_stderr(fake_stderr):
    print_distance(1000, 3,
                   speed_units='meters',
                   time_units='seconds')

print(fake_stderr.getvalue())


# 示例 7
# 目的：定义一个要求参数的函数
# 解释：创建一个函数，要求提供参数并发出警告。
# 结果：成功定义函数并调用 print_distance 函数
def require(name, value, default):
    """要求提供参数"""
    if value is not None:
        return value
    warnings.warn(
        f'{name} will be required soon, update your code',
        DeprecationWarning,
        stacklevel=3)
    return default

def print_distance(speed, duration, *,
                   speed_units=None,
                   time_units=None,
                   distance_units=None):
    """计算距离并打印"""
    speed_units = require('speed_units', speed_units, 'mph')
    time_units = require('time_units', time_units, 'hours')
    distance_units = require(
        'distance_units', distance_units, 'miles')

    norm_speed = convert(speed, speed_units)
    norm_duration = convert(duration, time_units)
    norm_distance = norm_speed * norm_duration
    distance = localize(norm_distance, distance_units)
    print(f'{distance} {distance_units}')


# 示例 8
# 目的：重定向标准错误输出
# 解释：使用 contextlib.redirect_stderr 重定向标准错误输出并捕获警告信息。
# 结果：成功重定向标准错误输出并捕获警告信息
import contextlib
import io

fake_stderr = io.StringIO()
with contextlib.redirect_stderr(fake_stderr):
    print_distance(1000, 3,
                   speed_units='meters',
                   time_units='seconds')

print(fake_stderr.getvalue())


# 示例 9
# 目的：将警告转换为异常
# 解释：使用 warnings.simplefilter 将警告转换为异常并捕获异常。
# 结果：成功将警告转换为异常并捕获异常
warnings.simplefilter('error')
try:
    warnings.warn('This usage is deprecated',
                  DeprecationWarning)
except DeprecationWarning:
    pass  # Expected
else:
    assert False

warnings.resetwarnings()


# 示例 10
# 目的：忽略警告
# 解释：使用 warnings.simplefilter 忽略警告并重置警告过滤器。
# 结果：成功忽略警告并重置警告过滤器
warnings.resetwarnings()

warnings.simplefilter('ignore')
warnings.warn('This will not be printed to stderr')

warnings.resetwarnings()


# 示例 11
# 目的：捕获警告日志
# 解释：使用 logging.captureWarnings 捕获警告日志并打印日志输出。
# 结果：成功捕获警告日志并打印日志输出
import logging

fake_stderr = io.StringIO()
handler = logging.StreamHandler(fake_stderr)
formatter = logging.Formatter(
    '%(asctime)-15s WARNING] %(message)s')
handler.setFormatter(formatter)

logging.captureWarnings(True)
logger = logging.getLogger('py.warnings')
logger.addHandler(handler)
logger.setLevel(logging.DEBUG)

warnings.resetwarnings()
warnings.simplefilter('default')
warnings.warn('This will go to the logs output')

print(fake_stderr.getvalue())

warnings.resetwarnings()


# 示例 12
# 目的：捕获警告
# 解释：使用 warnings.catch_warnings 捕获警告并进行断言测试。
# 结果：成功捕获警告并进行断言测试
with warnings.catch_warnings(record=True) as found_warnings:
    found = require('my_arg', None, 'fake units')
    expected = 'fake units'
    assert found == expected


# 示例 13
# 目的：断言捕获的警告
# 解释：对捕获的警告进行断言测试。
# 结果：成功断言捕获的警告
assert len(found_warnings) == 1
single_warning = found_warnings[0]
assert str(single_warning.message) == (
    'my_arg will be required soon, update your code')
assert single_warning.category == DeprecationWarning
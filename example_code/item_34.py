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

# 军规34：Avoid injecting data into generators with send
# 军规34：避免使用 send 向生成器注入数据

"""
总结:
send() 允许向生成器传入数据，但会增加复杂性，导致代码难以维护。
推荐做法：通过函数参数或外部类传递数据，让生成器专注于生成值，保持代码简洁清晰。

推荐替代方案：使用函数参数或外部状态
方案 1：通过函数参数传递数据。
方案 2：使用类管理状态。                       --- 待参考
方案 3: send() 替代方案：闭包函数管理状态。     --- 待参考
"""


# Reproduce book environment
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
atexit.register(TEST_DIR.cleanup)  # 程序结束时清理临时目录

# Make sure Windows processes exit cleanly
OLD_CWD = os.getcwd()
atexit.register(lambda: os.chdir(OLD_CWD))  # 程序结束时恢复工作目录
os.chdir(TEST_DIR.name)  # 切换到临时目录

def close_open_files():
    everything = gc.get_objects()  # 获取所有对象
    for obj in everything:
        if isinstance(obj, io.IOBase):  # 检查是否为文件对象
            obj.close()  # 关闭文件

atexit.register(close_open_files)  # 程序结束时关闭文件

# Example 1
print(f"\n{'Example 1':*^50}")
import math

def wave(amplitude, steps):
    step_size = 2 * math.pi / steps  # 计算步长
    for step in range(steps):
        radians = step * step_size  # 计算弧度
        fraction = math.sin(radians)  # 计算正弦值
        output = amplitude * fraction  # 计算输出
        yield output  # 生成输出值

# Example 2
print(f"\n{'Example 2':*^50}")
def transmit(output):
    if output is None:
        print(f'Output is None')  # 输出为None时的处理
    else:
        print(f'Output: {output:>5.1f}')  # 格式化输出

def run(it):
    for output in it:  # 遍历生成器
        transmit(output)  # 传输输出

run(wave(3.0, 8))  # 运行波形生成器

# Example 3
print(f"\n{'Example 3':*^50}")
def my_generator():
    received = yield 1  # 初始输出为1
    print(f'received = {received}')  # 打印接收到的值

it = my_generator()
output = next(it)       # 获取第一个生成器输出
print(f'output = {output}')  # 输出

try:
    next(it)            # 运行生成器直到退出
except StopIteration:
    pass
else:
    assert False  # 不应该执行到这里

# Example 4
print(f"\n{'Example 4':*^50}")
it = my_generator()
output = it.send(None)  # 获取第一个生成器输出
print(f'output = {output}')  # 输出

try:
    it.send('hello!')   # 向生成器发送值
except StopIteration:
    pass
else:
    assert False  # 不应该执行到这里

# Example 5
print(f"\n{'Example 5':*^50}")
def wave_modulating(steps):
    step_size = 2 * math.pi / steps  # 计算步长
    amplitude = yield             # 接收初始幅度
    for step in range(steps):
        radians = step * step_size  # 计算弧度
        fraction = math.sin(radians)  # 计算正弦值
        output = amplitude * fraction  # 计算输出
        amplitude = yield output  # 接收下一个幅度

# Example 6
print(f"\n{'Example 6':*^50}")
def run_modulating(it):
    amplitudes = [None, 7, 7, 7, 2, 2, 2, 2, 10, 10, 10, 10, 10]  # 幅度列表
    for amplitude in amplitudes:
        output = it.send(amplitude)  # 发送幅度并获取输出
        transmit(output)  # 传输输出

run_modulating(wave_modulating(12))  # 运行幅度调制的波形生成器

# Example 7
print(f"\n{'Example 7':*^50}")
def complex_wave():
    yield from wave(7.0, 3)  # 从wave生成器中生成值
    yield from wave(2.0, 4)  # 从wave生成器中生成值
    yield from wave(10.0, 5)  # 从wave生成器中生成值

run(complex_wave())  # 运行复合波形生成器

# Example 8
print(f"\n{'Example 8':*^50}")
def complex_wave_modulating():
    yield from wave_modulating(3)  # 从幅度调制生成器中生成值
    yield from wave_modulating(4)  # 从幅度调制生成器中生成值
    yield from wave_modulating(5)  # 从幅度调制生成器中生成值

run_modulating(complex_wave_modulating())  # 运行复合幅度调制生成器

# Example 9
print(f"\n{'Example 9':*^50}")
def wave_cascading(amplitude_it, steps):
    step_size = 2 * math.pi / steps  # 计算步长
    for step in range(steps):
        radians = step * step_size  # 计算弧度
        fraction = math.sin(radians)  # 计算正弦值
        amplitude = next(amplitude_it)  # 获取下一个输入
        output = amplitude * fraction  # 计算输出
        yield output  # 生成输出值

# Example 10
print(f"\n{'Example 10':*^50}")
def complex_wave_cascading(amplitude_it):
    yield from wave_cascading(amplitude_it, 3)  # 从波形生成器中生成值
    yield from wave_cascading(amplitude_it, 4)  # 从波形生成器中生成值
    yield from wave_cascading(amplitude_it, 5)  # 从波形生成器中生成值

# Example 11
print(f"\n{'Example 11':*^50}")
def run_cascading():
    amplitudes = [7, 7, 7, 2, 2, 2, 2, 10, 10, 10, 10, 10]  # 幅度列表
    it = complex_wave_cascading(iter(amplitudes))  # 创建复合波形生成器
    for amplitude in amplitudes:
        output = next(it)  # 获取下一个输出
        transmit(output)  # 传输输出

run_cascading()  # 运行级联波形生成器

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

# 军规 44 ：Use plain attributes instead of setter and getter methods

"""
军规要点：属性访问的Python之道】

核心思想：
Python推崇简单直接的属性访问
不需要像Java那样强制使用getter/setter
需要控制时才用@property，而不是过度设计

优雅的进化过程：
开始：直接使用属性访问 obj.value
需要时：无缝升级为@property
特点：外部调用方式完全不变

@property的使用时机：
需要验证数据时
需要动态计算属性时
需要在访问时触发特定操作
需要保护属性又想保持简洁访问

Python的设计哲学：
相信用户，提供直接访问
需要控制时，才加"智能门禁"
保持简单，拒绝过度工程化
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
    """
    目的：关闭所有打开的文件
    解释：遍历所有对象，找到所有打开的文件并关闭它们。
    """
    everything = gc.get_objects()
    for obj in everything:
        if isinstance(obj, io.IOBase):
            obj.close()

atexit.register(close_open_files)


# Example 1
# 目的：定义一个类 OldResistor
# 解释：定义一个类 OldResistor，包含 get_ohms 和 set_ohms 方法。
# 结果：类 OldResistor
print(f"\n{'Example 1':*^50}")
class OldResistor:
    """
    目的：定义一个类 OldResistor
    解释：包含 get_ohms 和 set_ohms 方法。
    """
    def __init__(self, ohms):
        self._ohms = ohms

    def get_ohms(self):
        """
        目的：获取电阻值
        解释：返回电阻值。
        """
        return self._ohms

    def set_ohms(self, ohms):
        """
        目的：设置电阻值
        解释：设置电阻值。
        """
        self._ohms = ohms


# Example 2
# 目的：创建 OldResistor 对象并测试方法
# 解释：创建 OldResistor 对象并测试方法。
# 结果：方法测试成功
print(f"\n{'Example 2':*^50}")
r0 = OldResistor(50e3)
print('Before:', r0.get_ohms())
r0.set_ohms(10e3)
print('After: ', r0.get_ohms())


# Example 3
# 目的：测试 OldResistor 对象的 set_ohms 方法
# 解释：测试 OldResistor 对象的 set_ohms 方法。
# 结果：方法测试成功
print(f"\n{'Example 3':*^50}")
r0.set_ohms(r0.get_ohms() - 4e3)
assert r0.get_ohms() == 6e3


# Example 4
# 目的：定义一个类 Resistor
# 解释：定义一个类 Resistor，包含公有字段。
# 结果：类 Resistor
print(f"\n{'Example 4':*^50}")
class Resistor:
    """
    目的：定义一个类 Resistor
    解释：包含公有字段。
    """
    def __init__(self, ohms):
        self.ohms = ohms
        self.voltage = 0
        self.current = 0

r1 = Resistor(50e3)
r1.ohms = 10e3
print(f'{r1.ohms} ohms, '
      f'{r1.voltage} volts, '
      f'{r1.current} amps')


# Example 5
# 目的：测试 Resistor 对象的 ohms 字段
# 解释：测试 Resistor 对象的 ohms 字段。
# 结果：字段测试成功
print(f"\n{'Example 5':*^50}")
r1.ohms += 5e3


# Example 6
# 目的：定义一个类 VoltageResistance
# 解释：继承自 Resistor，添加 voltage 属性。
# 结果：类 VoltageResistance
print(f"\n{'Example 6':*^50}")
class VoltageResistance(Resistor):
    """
    目的：定义一个类 VoltageResistance
    解释：继承自 Resistor，添加 voltage 属性。
    """
    def __init__(self, ohms):
        super().__init__(ohms)
        self._voltage = 0

    @property
    def voltage(self):
        """
        目的：获取电压值
        解释：返回电压值。
        """
        return self._voltage

    @voltage.setter
    def voltage(self, voltage):
        """
        目的：设置电压值
        解释：设置电压值并更新电流值。
        """
        self._voltage = voltage
        self.current = self._voltage / self.ohms


# Example 7
# 目的：创建 VoltageResistance 对象并测试属性
# 解释：创建 VoltageResistance 对象并测试属性。
# 结果：属性测试成功
print(f"\n{'Example 7':*^50}")
r2 = VoltageResistance(1e3)
print(f'Before: {r2.current:.2f} amps')
r2.voltage = 10
print(f'After:  {r2.current:.2f} amps')


# Example 8
# 目的：定义一个类 BoundedResistance
# 解释：继承自 Resistor，添加 ohms 属性。
# 结果：类 BoundedResistance
print(f"\n{'Example 8':*^50}")
class BoundedResistance(Resistor):
    """
    目的：定义一个类 BoundedResistance
    解释：继承自 Resistor，添加 ohms 属性。
    """
    def __init__(self, ohms):
        super().__init__(ohms)

    @property
    def ohms(self):
        """
        目的：获取电阻值
        解释：返回电阻值。
        """
        return self._ohms

    @ohms.setter
    def ohms(self, ohms):
        """
        目的：设置电阻值
        解释：设置电阻值并进行验证。
        """
        if ohms <= 0:
            raise ValueError(f'ohms must be > 0; got {ohms}')
        self._ohms = ohms


# Example 9
# 目的：测试 BoundedResistance 对象的 ohms 属性
# 解释：测试 BoundedResistance 对象的 ohms 属性。
# 结果：属性测试成功
print(f"\n{'Example 9':*^50}")
try:
    r3 = BoundedResistance(1e3)
    r3.ohms = 0
except:
    logging.exception('Expected')
else:
    assert False


# Example 10
# 目的：测试 BoundedResistance 对象的初始化
# 解释：测试 BoundedResistance 对象的初始化。
# 结果：初始化测试成功
print(f"\n{'Example 10':*^50}")
try:
    BoundedResistance(-5)
except:
    logging.exception('Expected')
else:
    assert False


# Example 11
# 目的：定义一个类 FixedResistance
# 解释：继承自 Resistor，添加不可变的 ohms 属性。
# 结果：类 FixedResistance
print(f"\n{'Example 11':*^50}")
class FixedResistance(Resistor):
    """
    目的：定义一个类 FixedResistance
    解释：继承自 Resistor，添加不可变的 ohms 属性。
    """
    def __init__(self, ohms):
        super().__init__(ohms)

    @property
    def ohms(self):
        """
        目的：获取电阻值
        解释：返回电阻值。
        """
        return self._ohms

    @ohms.setter
    def ohms(self, ohms):
        """
        目的：设置电阻值
        解释：设置电阻值并进行验证。
        """
        if hasattr(self, '_ohms'):
            raise AttributeError("Ohms is immutable")
        self._ohms = ohms


# Example 12
# 目的：测试 FixedResistance 对象的 ohms 属性
# 解释：测试 FixedResistance 对象的 ohms 属性。
# 结果：属性测试成功
print(f"\n{'Example 12':*^50}")
try:
    r4 = FixedResistance(1e3)
    r4.ohms = 2e3
except:
    logging.exception('Expected')
else:
    assert False


# Example 13
# 目的：定义一个类 MysteriousResistor
# 解释：继承自 Resistor，添加 ohms 属性。
# 结果：类 MysteriousResistor
print(f"\n{'Example 13':*^50}")
class MysteriousResistor(Resistor):
    """
    目的：定义一个类 MysteriousResistor
    解释：继承自 Resistor，添加 ohms 属性。
    """
    @property
    def ohms(self):
        """
        目的：获取电阻值
        解释：返回电阻值并更新电压值。
        """
        self.voltage = self._ohms * self.current
        return self._ohms

    @ohms.setter
    def ohms(self, ohms):
        """
        目的：设置电阻值
        解释：设置电阻值。
        """
        self._ohms = ohms


# Example 14
# 目的：创建 MysteriousResistor 对象并测试属性
# 解释：创建 MysteriousResistor 对象并测试属性。
# 结果：属性测试成功
print(f"\n{'Example 14':*^50}")
r7 = MysteriousResistor(10)
r7.current = 0.01
print(f'Before: {r7.voltage:.2f}')
r7.ohms
print(f'After:  {r7.voltage:.2f}')
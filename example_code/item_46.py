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

# 军规 46 : Use Descriptors for Reusable @property Methods

# 军规 46 ：使用描述符实现可重用的 @property 方法。

"""
解读：
属性控制的局限：@property虽然方便，但如果多个类需要相似的属性控制逻辑，
用@property重写每个类会带来重复代码。而**描述符（Descriptor）**提供了一种将属性控制逻辑封装成独立类的机制，使得我们可以将相同的逻辑在多个类中复用。

描述符概念：
描述符是一种带有__get__、__set__和__delete__方法的类，
通过将描述符类的实例赋值给另一个类的属性，描述符的逻辑会自动用于属性的读写控制。

总结：
消除重复代码：描述符封装复用逻辑，避免在多个类中重复@property方法。
清晰简洁：逻辑集中在描述符类中，类定义更清晰。
增强代码复用性：描述符让属性控制逻辑更易于扩展和维护。

本质说明：
本质就是提供了一个专属Descriptor的封装类，来解决了多类都需要针对类同的属性进行get,set的方式，
这种是一种优化处理。
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


# GPT - Example
print(f"\n{'GPT - Example':*^50}")
"""
Celsius 没有使用描述符来进行属性控制，用的是之前的@property方法。
"""
class Celsius:
    def __init__(self, temp=0):
        self._temp = temp

    @property
    def temp(self):
        return self._temp

    @temp.setter
    def temp(self, value):
        if value < -273.15:
            raise ValueError("Temperature cannot go below -273.15")
        self._temp = value

"""
Kelvin 没有使用描述符来进行属性控制，用的是之前的@property方法。
"""
class Kelvin:
    def __init__(self, temp=0):
        self._temp = temp

    @property
    def temp(self):
        return self._temp

    @temp.setter
    def temp(self, value):
        if value < 0:
            raise ValueError("Temperature cannot be below 0 in Kelvin")
        self._temp = value

"""
Celsius 和 Kelvin 都有相同的属性控制逻辑，但是代码重复，
所以我们可以使用描述符来实现属性控制逻辑的复用。
通过TemperatureDescriptor类，我们可以将属性控制逻辑封装到一个类中，
然后将这个类的实例赋值给Celsius和Kelvin的temp属性。
"""
class TemperatureDescriptor:
    def __init__(self, min_temp):
        self.min_temp = min_temp
        self._temp = None

    def __get__(self, instance, owner):
        return self._temp

    def __set__(self, instance, value):
        if value < self.min_temp:
            raise ValueError(f"Temperature cannot go below {self.min_temp}")
        self._temp = value

class Celsius:
    temp = TemperatureDescriptor(-273.15)

class Kelvin:
    temp = TemperatureDescriptor(0)

# 使用描述符属性
c = Celsius()
c.temp = 25
print(c.temp)  # 25
k = Kelvin()
k.temp = 5
print(k.temp)  # 5

# Example 1
# 目的：定义一个类 Homework
# 解释：定义一个类 Homework，包含 grade 属性。
# 结果：类 Homework
print(f"\n{'Example 1':*^50}")
class Homework:
    """
    目的：定义一个类 Homework
    解释：包含 grade 属性。
    """
    def __init__(self):
        self._grade = 0

    @property
    def grade(self):
        """
        目的：获取成绩
        解释：返回成绩。
        """
        return self._grade

    @grade.setter
    def grade(self, value):
        """
        目的：设置成绩
        解释：设置成绩并进行验证。
        """
        if not (0 <= value <= 100):
            raise ValueError('Grade must be between 0 and 100')
        self._grade = value


# Example 2
# 目的：创建 Homework 对象并测试属性
# 解释：创建 Homework 对象并测试属性。
# 结果：属性测试成功
print(f"\n{'Example 2':*^50}")
galileo = Homework()
galileo.grade = 95
assert galileo.grade == 95


# Example 3
# 目的：定义一个类 Exam
# 解释：定义一个类 Exam，包含 writing_grade 和 math_grade 属性。
# 结果：类 Exam
print(f"\n{'Example 3':*^50}")
class Exam:
    """
    目的：定义一个类 Exam
    解释：包含 writing_grade 和 math_grade 属性。
    """
    def __init__(self):
        self._writing_grade = 0
        self._math_grade = 0

    @staticmethod
    def _check_grade(value):
        """
        目的：验证成绩
        解释：验证成绩是否在 0 到 100 之间。
        """
        if not (0 <= value <= 100):
            raise ValueError('Grade must be between 0 and 100')

    @property
    def writing_grade(self):
        """
        目的：获取写作成绩
        解释：返回写作成绩。
        """
        return self._writing_grade

    @writing_grade.setter
    def writing_grade(self, value):
        """
        目的：设置写作成绩
        解释：设置写作成绩并进行验证。
        """
        self._check_grade(value)
        self._writing_grade = value

    @property
    def math_grade(self):
        """
        目的：获取数学成绩
        解释：返回数学成绩。
        """
        return self._math_grade

    @math_grade.setter
    def math_grade(self, value):
        """
        目的：设置数学成绩
        解释：设置数学成绩并进行验证。
        """
        self._check_grade(value)
        self._math_grade = value

galileo = Exam()
galileo.writing_grade = 85
galileo.math_grade = 99

assert galileo.writing_grade == 85
assert galileo.math_grade == 99


# Example 4
# 目的：定义一个类 Grade
# 解释：定义一个类 Grade，包含 __get__ 和 __set__ 方法。
# 结果：类 Grade
print(f"\n{'Example 4':*^50}")
class Grade:
    """
    目的：定义一个类 Grade
    解释：包含 __get__ 和 __set__ 方法。
    """
    def __get__(self, instance, instance_type):
        pass

    def __set__(self, instance, value):
        pass

class Exam:
    """
    目的：定义一个类 Exam
    解释：包含 Grade 类的类属性。
    """
    math_grade = Grade()
    writing_grade = Grade()
    science_grade = Grade()


# Example 5
# 目的：测试 Grade 类
# 解释：创建 Exam 对象并测试 Grade 类。
# 结果：类测试成功
print(f"\n{'Example 5':*^50}")
exam = Exam()
exam.writing_grade = 40


# Example 6
# 目的：测试 Grade 类的 __set__ 方法
# 解释：测试 Grade 类的 __set__ 方法。
# 结果：方法测试成功
print(f"\n{'Example 6':*^50}")
Exam.__dict__['writing_grade'].__set__(exam, 40)


# Example 7
# 目的：测试 Grade 类的 __get__ 方法
# 解释：测试 Grade 类的 __get__ 方法。
# 结果：方法测试成功
print(f"\n{'Example 7':*^50}")
exam.writing_grade


# Example 8
# 目的：测试 Grade 类的 __get__ 方法
# 解释：测试 Grade 类的 __get__ 方法。
# 结果：方法测试成功
print(f"\n{'Example 8':*^50}")
Exam.__dict__['writing_grade'].__get__(exam, Exam)


# Example 9
# 目的：定义一个类 Grade
# 解释：定义一个类 Grade，包含 __init__、__get__ 和 __set__ 方法。
# 结果：类 Grade
print(f"\n{'Example 9':*^50}")
class Grade:
    """
    目的：定义一个类 Grade
    解释：包含 __init__、__get__ 和 __set__ 方法。
    """
    def __init__(self):
        self._value = 0

    def __get__(self, instance, instance_type):
        """
        目的：获取成绩
        解释：返回成绩。
        """
        return self._value

    def __set__(self, instance, value):
        """
        目的：设置成绩
        解释：设置成绩并进行验证。
        """
        if not (0 <= value <= 100):
            raise ValueError('Grade must be between 0 and 100')
        self._value = value


# Example 10
# 目的：定义一个类 Exam
# 解释：定义一个类 Exam，包含 Grade 类的类属性。
# 结果：类 Exam
print(f"\n{'Example 10':*^50}")
class Exam:
    """
    目的：定义一个类 Exam
    解释：包含 Grade 类的类属性。
    """
    math_grade = Grade()
    writing_grade = Grade()
    science_grade = Grade()

first_exam = Exam()
first_exam.writing_grade = 82
first_exam.science_grade = 99
print('Writing', first_exam.writing_grade)
print('Science', first_exam.science_grade)


# Example 11
# 目的：测试 Exam 类的属性
# 解释：创建 Exam 对象并测试属性。
# 结果：属性测试成功
print(f"\n{'Example 11':*^50}")
second_exam = Exam()
second_exam.writing_grade = 75
print(f'Second {second_exam.writing_grade} is right')
print(f'First  {first_exam.writing_grade} is wrong; should be 82')


# Example 12
# 目的：定义一个类 Grade
# 解释：定义一个类 Grade，包含 __init__、__get__ 和 __set__ 方法。
# 结果：类 Grade
print(f"\n{'Example 12':*^50}")
class Grade:
    """
    目的：定义一个类 Grade
    解释：包含 __init__、__get__ 和 __set__ 方法。
    """
    def __init__(self):
        self._values = {}

    def __get__(self, instance, instance_type):
        """
        目的：获取成绩
        解释：返回成绩。
        """
        if instance is None:
            return self
        return self._values.get(instance, 0)

    def __set__(self, instance, value):
        """
        目的：设置成绩
        解释：设置成绩并进行验证。
        """
        if not (0 <= value <= 100):
            raise ValueError('Grade must be between 0 and 100')
        self._values[instance] = value


# Example 13
# 目的：定义一个类 Grade
# 解释：定义一个类 Grade，包含 __init__、__get__ 和 __set__ 方法。
# 结果：类 Grade
print(f"\n{'Example 13':*^50}")
from weakref import WeakKeyDictionary

class Grade:
    """
    目的：定义一个类 Grade
    解释：包含 __init__、__get__ 和 __set__ 方法。
    """
    def __init__(self):
        self._values = WeakKeyDictionary()

    def __get__(self, instance, instance_type):
        """
        目的：获取成绩
        解释：返回成绩。
        """
        if instance is None:
            return self
        return self._values.get(instance, 0)

    def __set__(self, instance, value):
        """
        目的：设置成绩
        解释：设置成绩并进行验证。
        """
        if not (0 <= value <= 100):
            raise ValueError('Grade must be between 0 and 100')
        self._values[instance] = value


# Example 14
# 目的：定义一个类 Exam
# 解释：定义一个类 Exam，包含 Grade 类的类属性。
# 结果：类 Exam
print(f"\n{'Example 14':*^50}")
class Exam:
    """
    目的：定义一个类 Exam
    解释：包含 Grade 类的类属性。
    """
    math_grade = Grade()
    writing_grade = Grade()
    science_grade = Grade()

first_exam = Exam()
first_exam.writing_grade = 82
second_exam = Exam()
second_exam.writing_grade = 75
print(f'First  {first_exam.writing_grade} is right')
print(f'Second {second_exam.writing_grade} is right')
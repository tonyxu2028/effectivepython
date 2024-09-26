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
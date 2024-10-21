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

# 新的章节Classes And Interfaces

# 军规37：Compose Classes Instead of Nesting Many Levels of Built-in Types
# 目的：使用嵌套的内置类型时，应该考虑使用类来替代。

"""
这一军规的核心确实就是 OOP（面向对象编程） 的思想：用类的组合来替代多层嵌套的内置类型。
但它的价值不只是单纯引入类，而在于鼓励你在 Python 中适当地使用面向对象的设计，
避免滥用内置数据结构，让代码更清晰、可维护。
"""

import random
random.seed(1234)

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
# 目的：创建一个简单的成绩簿类
# 解释：这个类用于存储学生的成绩，并计算每个学生的平均成绩。
# 结果：创建一个简单的成绩簿类
print(f"\n{'Example 1':*^50}")
class SimpleGradebook:
    def __init__(self):
        """
        目的：初始化一个简单的成绩簿
        解释：创建一个字典来存储学生的成绩。
        """
        self._grades = {}

    def add_student(self, name):
        """
        目的：添加学生
        解释：在成绩簿中添加一个新的学生，并为其创建一个成绩列表。
        """
        self._grades[name] = []

    def report_grade(self, name, score):
        """
        目的：报告学生的成绩
        解释：向指定学生的成绩列表中添加成绩。
        """
        self._grades[name].append(score)

    def average_grade(self, name):
        """
        目的：计算学生的平均成绩
        解释：计算并返回指定学生的平均成绩。
        """
        grades = self._grades[name]
        return sum(grades) / len(grades)


# Example 2
# 目的：添加学生并报告成绩
# 解释：向成绩簿中添加学生，并报告他们的成绩。
# 结果：添加学生并报告成绩
print(f"\n{'Example 2':*^50}")
book = SimpleGradebook()
book.add_student('Isaac Newton')
book.report_grade('Isaac Newton', 90)
book.report_grade('Isaac Newton', 95)
book.report_grade('Isaac Newton', 85)

print(book.average_grade('Isaac Newton'))


# Example 3
# 目的：创建一个按科目存储成绩的成绩簿类
# 解释：这个类用于按科目存储学生的成绩。
# 结果：创建一个按科目存储成绩的成绩簿类
print(f"\n{'Example 3':*^50}")
from collections import defaultdict

class BySubjectGradebook:
    def __init__(self):
        """
        目的：初始化一个按科目存储成绩的成绩簿
        解释：创建一个嵌套字典来存储学生的科目成绩。
        """
        self._grades = {}                       # Outer dict

    def add_student(self, name):
        """
        目的：添加学生
        解释：在成绩簿中添加一个新的学生，并为其创建一个按科目存储成绩的字典。
        """
        self._grades[name] = defaultdict(list)  # Inner dict


# Example 4
# 目的：报告学生的科目成绩
# 解释：向成绩簿中报告学生在特定科目的成绩，并计算他们的平均成绩。
# 结果：报告学生的科目成绩
    print(f"\n{'Example 4':*^50}")

    def report_grade(self, name, subject, grade):
        """
        目的：报告学生的科目成绩
        解释：向指定学生的指定科目成绩列表中添加成绩。
        """
        by_subject = self._grades[name]
        grade_list = by_subject[subject]
        grade_list.append(grade)

    def average_grade(self, name):
        """
        目的：计算学生的平均成绩
        解释：计算并返回指定学生的所有科目的平均成绩。
        """
        by_subject = self._grades[name]
        total, count = 0, 0
        for grades in by_subject.values():
            total += sum(grades)
            count += len(grades)
        return total / count


# Example 5
# 目的：添加学生并报告科目成绩
# 解释：向成绩簿中添加学生，并报告他们在不同科目的成绩。
# 结果：添加学生并报告科目成绩
print(f"\n{'Example 5':*^50}")
book = BySubjectGradebook()
book.add_student('Albert Einstein')
book.report_grade('Albert Einstein', 'Math', 75)
book.report_grade('Albert Einstein', 'Math', 65)
book.report_grade('Albert Einstein', 'Gym', 90)
book.report_grade('Albert Einstein', 'Gym', 95)
print(book.average_grade('Albert Einstein'))


# Example 6
# 目的：创建一个带权重的成绩簿类
# 解释：这个类用于存储带权重的学生成绩。
# 结果：创建一个带权重的成绩簿类
print(f"\n{'Example 6':*^50}")
class WeightedGradebook:
    def __init__(self):
        """
        目的：初始化一个带权重的成绩簿
        解释：创建一个嵌套字典来存储学生的带权重的科目成绩。
        """
        self._grades = {}

    def add_student(self, name):
        """
        目的：添加学生
        解释：在成绩簿中添加一个新的学生，并为其创建一个按科目存储带权重成绩的字典。
        """
        self._grades[name] = defaultdict(list)

    def report_grade(self, name, subject, score, weight):
        """
        目的：报告学生的带权重的科目成绩
        解释：向指定学生的指定科目成绩列表中添加带权重的成绩。
        """
        by_subject = self._grades[name]
        grade_list = by_subject[subject]
        grade_list.append((score, weight))


# Example 7
# 目的：计算带权重的平均成绩
# 解释：计算学生在各科目中的带权重的平均成绩。
# 结果：计算带权重的平均成绩
    print(f"\n{'Example 7':*^50}")
    def average_grade(self, name):
        """
        目的：计算学生的带权重的平均成绩
        解释：计算并返回指定学生的所有科目的带权重的平均成绩。
        """
        by_subject = self._grades[name]

        score_sum, score_count = 0, 0
        for subject, scores in by_subject.items():
            subject_avg, total_weight = 0, 0
            for score, weight in scores:
                subject_avg += score * weight
                total_weight += weight

            score_sum += subject_avg / total_weight
            score_count += 1

        return score_sum / score_count


# Example 8
# 目的：使用 WeightedGradebook 类添加学生并报告带权重的成绩
# 解释：向带权重的成绩簿中添加学生，并报告他们在不同科目的带权重的成绩。
# 结果：使用 WeightedGradebook 类添加学生并报告带权重的成绩
print(f"\n{'Example 8':*^50}")
book = WeightedGradebook()
book.add_student('Albert Einstein')
book.report_grade('Albert Einstein', 'Math', 75, 0.05)
book.report_grade('Albert Einstein', 'Math', 65, 0.15)
book.report_grade('Albert Einstein', 'Math', 70, 0.80)
book.report_grade('Albert Einstein', 'Gym', 100, 0.40)
book.report_grade('Albert Einstein', 'Gym', 85, 0.60)
print(book.average_grade('Albert Einstein'))


# Example 9
# 目的：计算带权重的成绩
# 解释：计算一组带权重的成绩的平均值。
# 结果：计算带权重的成绩
print(f"\n{'Example 9':*^50}")
grades = []
grades.append((95, 0.45))
grades.append((85, 0.55))
total = sum(score * weight for score, weight in grades)
total_weight = sum(weight for _, weight in grades)
average_grade = total / total_weight
print(average_grade)


# Example 10
# 目的：带注释的成绩
# 解释：存储带注释的成绩，并计算它们的平均值。
# 结果：带注释的成绩
print(f"\n{'Example 10':*^50}")
grades = []
grades.append((95, 0.45, 'Great job'))
grades.append((85, 0.55, 'Better next time'))
total = sum(score * weight for score, weight, _ in grades)
total_weight = sum(weight for _, weight, _ in grades)
average_grade = total / total_weight
print(average_grade)


# Example 11
# 目的：使用 namedtuple 存储成绩
# 解释：使用 namedtuple 存储带权重的成绩。
# 结果：使用 namedtuple 存储成绩
print(f"\n{'Example 11':*^50}")
from collections import namedtuple

Grade = namedtuple('Grade', ('score', 'weight'))


# Example 12
# 目的：按科目存储带权重的成绩
# 解释：创建一个类，用于按科目存储带权重的成绩。
# 结果：按科目存储带权重的成绩
print(f"\n{'Example 12':*^50}")
class Subject:
    def __init__(self):
        """
        目的：初始化一个科目
        解释：创建一个列表来存储科目的带权重的成绩。
        """
        self._grades = []

    def report_grade(self, score, weight):
        """
        目的：报告科目的带权重的成绩
        解释：向科目的成绩列表中添加带权重的成绩。
        """
        self._grades.append(Grade(score, weight))

    def average_grade(self):
        """
        目的：计算科目的带权重的平均成绩
        解释：计算并返回科目的带权重的平均成绩。
        """
        total, total_weight = 0, 0
        for grade in self._grades:
            total += grade.score * grade.weight
            total_weight += grade.weight
        return total / total_weight


# Example 13
# 目的：按学生存储科目成绩
# 解释：创建一个类，用于按学生存储科目成绩。
# 结果：按学生存储科目成绩
print(f"\n{'Example 13':*^50}")
class Student:
    def __init__(self):
        """
        目的：初始化一个学生
        解释：创建一个字典来存储学生的科目。
        """
        self._subjects = defaultdict(Subject)

    def get_subject(self, name):
        """
        目的：获取学生的科目
        解释：返回指定名称的科目。
        """
        return self._subjects[name]

    def average_grade(self):
        """
        目的：计算学生的平均成绩
        解释：计算并返回学生的所有科目的平均成绩。
        """
        total, count = 0, 0
        for subject in self._subjects.values():
            total += subject.average_grade()
            count += 1
        return total / count


# Example 14
# 目的：成绩簿类
# 解释：创建一个类，用于存储学生及其科目成绩。
# 结果：成绩簿类
print(f"\n{'Example 14':*^50}")
class Gradebook:
    def __init__(self):
        """
        目的：初始化一个成绩簿
        解释：创建一个字典来存储学生。
        """
        self._students = defaultdict(Student)

    def get_student(self, name):
        """
        目的：获取学生
        解释：返回指定名称的学生。
        """
        return self._students[name]


# Example 15
# 目的：使用 Gradebook 类添加学生并报告成绩
# 解释：向成绩簿中添加学生，并报告他们在不同科目的成绩。
# 结果：使用 Gradebook 类添加学生并报告成绩
print(f"\n{'Example 15':*^50}")
book = Gradebook()
albert = book.get_student('Albert Einstein')
math = albert.get_subject('Math')
math.report_grade(75, 0.05)
math.report_grade(65, 0.15)
math.report_grade(70, 0.80)
gym = albert.get_subject('Gym')
gym.report_grade(100, 0.40)
gym.report_grade(85, 0.60)
print(albert.average_grade())
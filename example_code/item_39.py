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

# 目的：关闭所有打开的文件
# 解释：遍历所有对象，找到所有打开的文件并关闭它们。
def close_open_files():
    everything = gc.get_objects()
    for obj in everything:
        if isinstance(obj, io.IOBase):
            obj.close()

atexit.register(close_open_files)


# Example 1
# 目的：定义一个抽象的输入数据类
# 解释：定义一个抽象基类，要求子类实现 read 方法。
# 结果：抽象的输入数据类
print(f"\n{'Example 1':*^50}")
class InputData:
    def read(self):
        """
        目的：读取数据
        解释：抽象方法，要求子类实现。
        """
        raise NotImplementedError


# Example 2
# 目的：定义一个从文件路径读取数据的类
# 解释：继承 InputData 类，实现从文件路径读取数据的功能。
# 结果：从文件路径读取数据的类
print(f"\n{'Example 2':*^50}")
class PathInputData(InputData):
    def __init__(self, path):
        """
        目的：初始化 PathInputData 类
        解释：存储文件路径。
        """
        super().__init__()
        self.path = path

    def read(self):
        """
        目的：读取文件内容
        解释：从文件路径读取数据并返回。
        """
        with open(self.path) as f:
            return f.read()


# Example 3
# 目的：定义一个抽象的工作类
# 解释：定义一个抽象基类，要求子类实现 map 和 reduce 方法。
# 结果：抽象的工作类
print(f"\n{'Example 3':*^50}")
class Worker:
    def __init__(self, input_data):
        """
        目的：初始化 Worker 类
        解释：存储输入数据。
        """
        self.input_data = input_data
        self.result = None

    def map(self):
        """
        目的：映射操作
        解释：抽象方法，要求子类实现。
        """
        raise NotImplementedError

    def reduce(self, other):
        """
        目的：归约操作
        解释：抽象方法，要求子类实现。
        """
        raise NotImplementedError


# Example 4
# 目的：定义一个行计数工作类
# 解释：继承 Worker 类，实现行计数的 map 和 reduce 方法。
# 结果：行计数工作类
print(f"\n{'Example 4':*^50}")
class LineCountWorker(Worker):
    def map(self):
        """
        目的：计数行数
        解释：读取数据并计算行数。
        """
        data = self.input_data.read()
        self.result = data.count('\n')

    def reduce(self, other):
        """
        目的：合并行数
        解释：将其他工作对象的结果合并到当前对象。
        """
        self.result += other.result


# Example 5
# 目的：生成输入数据
# 解释：从指定目录生成 PathInputData 对象。
# 结果：生成输入数据
print(f"\n{'Example 5':*^50}")
import os

def generate_inputs(data_dir):
    """
    目的：生成输入数据
    解释：遍历目录，生成 PathInputData 对象。
    """
    for name in os.listdir(data_dir):
        yield PathInputData(os.path.join(data_dir, name))


# Example 6
# 目的：创建工作对象
# 解释：从输入数据列表创建 LineCountWorker 对象。
# 结果：创建工作对象
print(f"\n{'Example 6':*^50}")
def create_workers(input_list):
    """
    目的：创建工作对象
    解释：从输入数据列表创建 LineCountWorker 对象。
    """
    workers = []
    for input_data in input_list:
        workers.append(LineCountWorker(input_data))
    return workers


# Example 7
# 目的：执行工作对象
# 解释：使用多线程执行工作对象的 map 方法，并合并结果。
# 结果：执行工作对象
print(f"\n{'Example 7':*^50}")
from threading import Thread

def execute(workers):
    """
    目的：执行工作对象
    解释：使用多线程执行工作对象的 map 方法，并合并结果。
    """
    threads = [Thread(target=w.map) for w in workers]
    for thread in threads: thread.start()
    for thread in threads: thread.join()

    first, *rest = workers
    for worker in rest:
        first.reduce(worker)
    return first.result


# Example 8
# 目的：执行 MapReduce 操作
# 解释：生成输入数据，创建工作对象并执行。
# 结果：执行 MapReduce 操作
print(f"\n{'Example 8':*^50}")
def mapreduce(data_dir):
    """
    目的：执行 MapReduce 操作
    解释：生成输入数据，创建工作对象并执行。
    """
    inputs = generate_inputs(data_dir)
    workers = create_workers(inputs)
    return execute(workers)


# Example 9
# 目的：写入测试文件并执行 MapReduce 操作
# 解释：生成测试文件并执行 MapReduce 操作，打印结果。
# 结果：写入测试文件并执行 MapReduce 操作
print(f"\n{'Example 9':*^50}")
import os
import random

def write_test_files(tmpdir):
    """
    目的：写入测试文件
    解释：生成包含随机行数的测试文件。
    """
    os.makedirs(tmpdir)
    for i in range(100):
        with open(os.path.join(tmpdir, str(i)), 'w') as f:
            f.write('\n' * random.randint(0, 100))

tmpdir = 'test_inputs'
write_test_files(tmpdir)

result = mapreduce(tmpdir)
print(f'There are {result} lines')


# Example 10
# 目的：定义一个通用的输入数据类
# 解释：定义一个抽象基类，要求子类实现 read 和 generate_inputs 方法。
# 结果：通用的输入数据类
print(f"\n{'Example 10':*^50}")
class GenericInputData:
    def read(self):
        """
        目的：读取数据
        解释：抽象方法，要求子类实现。
        """
        raise NotImplementedError

    @classmethod
    def generate_inputs(cls, config):
        """
        目的：生成输入数据
        解释：抽象方法，要求子类实现。
        """
        raise NotImplementedError


# Example 11
# 目的：定义一个从文件路径读取数据的通用类
# 解释：继承 GenericInputData 类，实现从文件路径读取数据的功能。
# 结果：从文件路径读取数据的通用类
print(f"\n{'Example 11':*^50}")
class PathInputData(GenericInputData):
    def __init__(self, path):
        """
        目的：初始化 PathInputData 类
        解释：存储文件路径。
        """
        super().__init__()
        self.path = path

    def read(self):
        """
        目的：读取文件内容
        解释：从文件路径读取数据并返回。
        """
        with open(self.path) as f:
            return f.read()

    @classmethod
    def generate_inputs(cls, config):
        """
        目的：生成输入数据
        解释：遍历目录，生成 PathInputData 对象。
        """
        data_dir = config['data_dir']
        for name in os.listdir(data_dir):
            yield cls(os.path.join(data_dir, name))


# Example 12
# 目的：定义一个通用的工作类
# 解释：定义一个抽象基类，要求子类实现 map 和 reduce 方法。
# 结果：通用的工作类
print(f"\n{'Example 12':*^50}")
class GenericWorker:
    def __init__(self, input_data):
        """
        目的：初始化 GenericWorker 类
        解释：存储输入数据。
        """
        self.input_data = input_data
        self.result = None

    def map(self):
        """
        目的：映射操作
        解释：抽象方法，要求子类实现。
        """
        raise NotImplementedError

    def reduce(self, other):
        """
        目的：归约操作
        解释：抽象方法，要求子类实现。
        """
        raise NotImplementedError

    @classmethod
    def create_workers(cls, input_class, config):
        """
        目的：创建工作对象
        解释：从输入数据类生成输入数据，并创建工作对象。
        """
        workers = []
        for input_data in input_class.generate_inputs(config):
            workers.append(cls(input_data))
        return workers


# Example 13
# 目的：定义一个行计数工作类
# 解释：继承 GenericWorker 类，实现行计数的 map 和 reduce 方法。
# 结果：行计数工作类
print(f"\n{'Example 13':*^50}")
class LineCountWorker(GenericWorker):
    def map(self):
        """
        目的：计数行数
        解释：读取数据并计算行数。
        """
        data = self.input_data.read()
        self.result = data.count('\n')

    def reduce(self, other):
        """
        目的：合并行数
        解释：将其他工作对象的结果合并到当前对象。
        """
        self.result += other.result


# Example 14
# 目的：执行通用的 MapReduce 操作
# 解释：生成输入数据，创建工作对象并执行。
# 结果：执行通用的 MapReduce 操作
print(f"\n{'Example 14':*^50}")
def mapreduce(worker_class, input_class, config):
    """
    目的：执行通用的 MapReduce 操作
    解释：生成输入数据，创建工作对象并执行。
    """
    workers = worker_class.create_workers(input_class, config)
    return execute(workers)


# Example 15
# 目的：执行 MapReduce 操作并打印结果
# 解释：配置数据目录，执行 MapReduce 操作并打印结果。
# 结果：执行 MapReduce 操作并打印结果
print(f"\n{'Example 15':*^50}")
config = {'data_dir': tmpdir}
result = mapreduce(LineCountWorker, PathInputData, config)
print(f'There are {result} lines')
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
# 目的：定义一个函数 trace_func
# 解释：定义一个函数 trace_func，包含 wraps 装饰器。
# 结果：函数 trace_func
print(f"\n{'Example 1':*^50}")
from functools import wraps

def trace_func(func):
    """
    目的：定义一个函数 trace_func
    解释：包含 wraps 装饰器。
    """
    @wraps(func)
    def wrapper(*args, **kwargs):
        result = func(*args, **kwargs)
        print(f'{func.__name__}({args}, {kwargs}) -> {result}')
        return result
    return wrapper


# Example 2
# 目的：定义一个类 TraceDict
# 解释：定义一个类 TraceDict，继承自 dict。
# 结果：类 TraceDict
print(f"\n{'Example 2':*^50}")
class TraceDict(dict):
    """
    目的：定义一个类 TraceDict
    解释：继承自 dict。
    """
    @trace_func
    def __setitem__(self, key, value):
        super().__setitem__(key, value)

    @trace_func
    def __getitem__(self, key):
        return super().__getitem__(key)

trace_dict = TraceDict([('hi', 1)])
trace_dict['there'] = 2
trace_dict['hi']
try:
    trace_dict['missing']
except KeyError:
    logging.exception('Expected')
else:
    assert False


# Example 3
# 目的：定义一个类 TraceMeta
# 解释：定义一个类 TraceMeta，继承自 type。
# 结果：类 TraceMeta
print(f"\n{'Example 3':*^50}")
import types

trace_types = (
    types.FunctionType,
    types.MethodType,
    types.BuiltinFunctionType,
    types.BuiltinMethodType,
)

class TraceMeta(type):
    """
    目的：定义一个类 TraceMeta
    解释：继承自 type。
    """
    def __new__(meta, name, bases, class_dict):
        for key, value in class_dict.items():
            if isinstance(value, trace_types):
                class_dict[key] = trace_func(value)
        return super().__new__(meta, name, bases, class_dict)


# Example 4
# 目的：定义一个类 TraceDict
# 解释：定义一个类 TraceDict，继承自 dict 并使用 TraceMeta 元类。
# 结果：类 TraceDict
print(f"\n{'Example 4':*^50}")
class TraceDict(dict, metaclass=TraceMeta):
    """
    目的：定义一个类 TraceDict
    解释：继承自 dict 并使用 TraceMeta 元类。
    """
    pass

trace_dict = TraceDict([('hi', 1)])
trace_dict['there'] = 2
trace_dict['hi']
try:
    trace_dict['missing']
except KeyError:
    logging.exception('Expected')
else:
    assert False


# Example 5
# 目的：定义一个类 OtherMeta
# 解释：定义一个类 OtherMeta，继承自 TraceMeta。
# 结果：类 OtherMeta
print(f"\n{'Example 5':*^50}")
class OtherMeta(TraceMeta):
    """
    目的：定义一个类 OtherMeta
    解释：继承自 TraceMeta。
    """
    pass

class SimpleDict(dict, metaclass=OtherMeta):
    """
    目的：定义一个类 SimpleDict
    解释：继承自 dict 并使用 OtherMeta 元类。
    """
    pass

class TraceDict(SimpleDict, metaclass=TraceMeta):
    """
    目的：定义一个类 TraceDict
    解释：继承自 SimpleDict 并使用 TraceMeta 元类。
    """
    pass

trace_dict = TraceDict([('hi', 1)])
trace_dict['there'] = 2
trace_dict['hi']
try:
    trace_dict['missing']
except KeyError:
    logging.exception('Expected')
else:
    assert False


# Example 6
# 目的：定义一个类装饰器 my_class_decorator
# 解释：定义一个类装饰器 my_class_decorator。
# 结果：类装饰器 my_class_decorator
print(f"\n{'Example 6':*^50}")
def my_class_decorator(klass):
    """
    目的：定义一个类装饰器 my_class_decorator
    解释：定义一个类装饰器 my_class_decorator。
    """
    klass.extra_param = 'extra'
    return klass

@my_class_decorator
class MyClass:
    """
    目的：定义一个类 MyClass
    解释：使用 my_class_decorator 装饰器。
    """
    pass

print(MyClass)
print(MyClass.extra_param)


# Example 7
# 目的：定义一个类装饰器 trace
# 解释：定义一个类装饰器 trace。
# 结果：类装饰器 trace
print(f"\n{'Example 7':*^50}")
def trace(klass):
    """
    目的：定义一个类装饰器 trace
    解释：定义一个类装饰器 trace。
    """
    for key, value in klass.__dict__.items():
        if isinstance(value, trace_types):
            setattr(klass, key, trace_func(value))
    return klass

@trace
class TraceDict(dict):
    """
    目的：定义一个类 TraceDict
    解释：继承自 dict 并使用 trace 装饰器。
    """
    pass

trace_dict = TraceDict([('hi', 1)])
trace_dict['there'] = 2
trace_dict['hi']
try:
    trace_dict['missing']
except KeyError:
    logging.exception('Expected')
else:
    assert False


# Example 8
# 目的：定义一个类 TraceDict
# 解释：定义一个类 TraceDict，继承自 dict 并使用 OtherMeta 元类和 trace 装饰器。
# 结果：类 TraceDict
print(f"\n{'Example 8':*^50}")
@trace
class TraceDict(dict, metaclass=OtherMeta):
    """
    目的：定义一个类 TraceDict
    解释：继承自 dict 并使用 OtherMeta 元类和 trace 装饰器。
    """
    pass

trace_dict = TraceDict([('hi', 1)])
trace_dict['there'] = 2
trace_dict['hi']
try:
    trace_dict['missing']
except KeyError:
    logging.exception('Expected')
else:
    assert False
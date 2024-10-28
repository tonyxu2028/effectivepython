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

# 军规 47 : Use __getattr__, __getattribute__, and __setattr__ for Lazy Attributes
# 军规 47 : 使用 __getattr__、__getattribute__ 和 __setattr__ 以实现延迟属性加载。

"""
解读:
延迟加载：延迟加载（Lazy Loading）是一种在需要时才初始化或加载对象属性的方式，
通常用于提升效率，尤其在属性的计算、资源占用较大的情况下。

三种魔术方法：
__getattr__：仅在属性未定义（不存在）时被调用，可以用于实现缺省值或动态属性。
__getattribute__：每次访问属性时都会调用此方法，使其适合监控、延迟加载等高级控制逻辑。
__setattr__：在对属性赋值时调用，适用于在属性赋值时加入校验或懒加载的逻辑。

总结:
延迟加载优化：通过 __getattr__ 和 __getattribute__ 延迟初始化属性，减少不必要的资源占用。
代码控制力增强：这些魔术方法允许精细控制属性的加载与访问，为特定需求提供更多优化空间。
适用场景：适用于复杂计算、资源密集或外部请求的属性。
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

# GPT - Example 懒加载属性
class MyClass:
    def __init__(self, data):
        # 直接初始化属性，计算较耗时
        self.heavy_data = self.load_heavy_data(data)

    def load_heavy_data(self, data):
        # 假设此方法较为耗时
        return data * 2

obj = MyClass(10)
print(obj.heavy_data)

class MyClass:
    def __init__(self, data):
        self.data = data
        self._heavy_data = None  # 延迟初始化属性

    def load_heavy_data(self):
        print("Loading heavy data...")
        return self.data * 2

    def __getattr__(self, name):
        if name == "heavy_data":
            # 仅当访问 heavy_data 时才计算
            self._heavy_data = self.load_heavy_data()
            return self._heavy_data
        raise AttributeError(f"{name} not found")

obj = MyClass(10)
print(obj.heavy_data)  # 首次访问时加载
print(obj.heavy_data)  # 后续直接返回已有值

class MyClass:
    def __init__(self, data):
        self.data = data
        self._heavy_data = None

    def load_heavy_data(self):
        print("Loading heavy data...")
        return self.data * 2

    def __getattribute__(self, name):
        if name == "heavy_data":
            if object.__getattribute__(self, "_heavy_data") is None:
                # 延迟加载
                object.__setattr__(self, "_heavy_data", self.load_heavy_data())
            return object.__getattribute__(self, "_heavy_data")
        return object.__getattribute__(self, name)

obj = MyClass(10)
print(obj.heavy_data)  # 首次访问时加载
print(obj.heavy_data)  # 后续直接返回已有值


# Example 1
# 目的：定义一个类 LazyRecord
# 解释：定义一个类 LazyRecord，包含 __getattr__ 方法。
# 结果：类 LazyRecord
print(f"\n{'Example 1':*^50}")
class LazyRecord:
    """
    目的：定义一个类 LazyRecord
    解释：包含 __getattr__ 方法。
    """
    def __init__(self):
        self.exists = 5

    def __getattr__(self, name):
        """
        目的：获取属性
        解释：返回属性值。
        """
        value = f'Value for {name}'
        setattr(self, name, value)
        return value


# Example 2
# 目的：测试 LazyRecord 类
# 解释：创建 LazyRecord 对象并测试 __getattr__ 方法。
# 结果：方法测试成功
print(f"\n{'Example 2':*^50}")
data = LazyRecord()
print('Before:', data.__dict__)
print('foo:   ', data.foo)
print('After: ', data.__dict__)


# Example 3
# 目的：定义一个类 LoggingLazyRecord
# 解释：继承自 LazyRecord，添加日志记录功能。
# 结果：类 LoggingLazyRecord
print(f"\n{'Example 3':*^50}")
class LoggingLazyRecord(LazyRecord):
    """
    目的：定义一个类 LoggingLazyRecord
    解释：继承自 LazyRecord，添加日志记录功能。
    """
    def __getattr__(self, name):
        """
        目的：获取属性并记录日志
        解释：返回属性值并记录日志。
        """
        print(f'* Called __getattr__({name!r})')
        value = super().__getattr__(name)
        print(f'* Returning {value!r}')
        return value

data = LoggingLazyRecord()
print('exists:     ', data.exists)
print('First foo:  ', data.foo)
print('Second foo: ', data.foo)


# Example 4
# 目的：定义一个类 ValidatingRecord
# 解释：定义一个类 ValidatingRecord，包含 __getattribute__ 方法。
# 结果：类 ValidatingRecord
print(f"\n{'Example 4':*^50}")
class ValidatingRecord:
    """
    目的：定义一个类 ValidatingRecord
    解释：包含 __getattribute__ 方法。
    """
    def __init__(self):
        self.exists = 5

    def __getattribute__(self, name):
        """
        目的：获取属性并进行验证
        解释：返回属性值并进行验证。
        """
        print(f'* Called __getattribute__({name!r})')
        try:
            return super().__getattribute__(name)
        except AttributeError:
            value = f'Value for {name}'
            setattr(self, name, value)
            return value

data = ValidatingRecord()
print('exists:     ', data.exists)
print('First foo:  ', data.foo)
print('Second foo: ', data.foo)


# Example 5
# 目的：测试 MissingPropertyRecord 类
# 解释：创建 MissingPropertyRecord 对象并测试属性。
# 结果：属性测试成功
print(f"\n{'Example 5':*^50}")
try:
    class MissingPropertyRecord:
        """
        目的：定义一个类 MissingPropertyRecord
        解释：包含 __getattr__ 方法。
        """
        def __getattr__(self, name):
            if name == 'bad_name':
                raise AttributeError(f'{name} is missing')
            return f'Value for {name}'

    data = MissingPropertyRecord()
    assert data.foo == 'Value for foo'  # Test this works
    data.bad_name
except:
    logging.exception('Expected')
else:
    assert False


# Example 6
# 目的：测试 LoggingLazyRecord 类的 __getattr__ 方法
# 解释：创建 LoggingLazyRecord 对象并测试 __getattr__ 方法。
# 结果：方法测试成功
print(f"\n{'Example 6':*^50}")
data = LoggingLazyRecord()  # Implements __getattr__
print('Before:         ', data.__dict__)
print('Has first foo:  ', hasattr(data, 'foo'))
print('After:          ', data.__dict__)
print('Has second foo: ', hasattr(data, 'foo'))


# Example 7
# 目的：测试 ValidatingRecord 类的 __getattribute__ 方法
# 解释：创建 ValidatingRecord 对象并测试 __getattribute__ 方法。
# 结果：方法测试成功
print(f"\n{'Example 7':*^50}")
data = ValidatingRecord()  # Implements __getattribute__
print('Has first foo:  ', hasattr(data, 'foo'))
print('Has second foo: ', hasattr(data, 'foo'))


# Example 8
# 目的：定义一个类 SavingRecord
# 解释：定义一个类 SavingRecord，包含 __setattr__ 方法。
# 结果：类 SavingRecord
print(f"\n{'Example 8':*^50}")
class SavingRecord:
    """
    目的：定义一个类 SavingRecord
    解释：包含 __setattr__ 方法。
    """
    def __setattr__(self, name, value):
        """
        目的：设置属性
        解释：设置属性值。
        """
        if name == 'exists':
            raise AttributeError(f'{name} is immutable')
        super().__setattr__(name, value)


# Example 9
# 目的：定义一个类 LoggingSavingRecord
# 解释：继承自 SavingRecord，添加日志记录功能。
# 结果：类 LoggingSavingRecord
print(f"\n{'Example 9':*^50}")
class LoggingSavingRecord(SavingRecord):
    """
    目的：定义一个类 LoggingSavingRecord
    解释：继承自 SavingRecord，添加日志记录功能。
    """
    def __setattr__(self, name, value):
        """
        目的：设置属性并记录日志
        解释：设置属性值并记录日志。
        """
        print(f'* Called __setattr__({name!r}, {value!r})')
        super().__setattr__(name, value)

data = LoggingSavingRecord()
print('Before: ', data.__dict__)
data.foo = 5
print('After:  ', data.__dict__)
data.foo = 7
print('Finally:', data.__dict__)


# Example 10
# 目的：定义一个类 BrokenDictionaryRecord
# 解释：定义一个类 BrokenDictionaryRecord，包含 __getattribute__ 方法。
# 结果：类 BrokenDictionaryRecord
print(f"\n{'Example 10':*^50}")
class BrokenDictionaryRecord:
    """
    目的：定义一个类 BrokenDictionaryRecord
    解释：包含 __getattribute__ 方法。
    """
    def __init__(self, data):
        self._data = data

    def __getattribute__(self, name):
        """
        目的：获取属性
        解释：返回属性值。
        """
        data_dict = super().__getattribute__('_data')
        return data_dict[name]

# Example 11
# 目的：测试 BrokenDictionaryRecord 类
# 解释：创建 BrokenDictionaryRecord 对象并测试属性。
# 结果：属性测试成功
print(f"\n{'Example 11':*^50}")
try:
    data = BrokenDictionaryRecord({'foo': 3})
    data.foo
except:
    logging.exception('Expected')
else:
    assert False


# Example 12
# 目的：定义一个类 DictionaryRecord
# 解释：定义一个类 DictionaryRecord，包含 __getattribute__ 方法。
# 结果：类 DictionaryRecord
print(f"\n{'Example 12':*^50}")
class DictionaryRecord:
    """
    目的：定义一个类 DictionaryRecord
    解释：包含 __getattribute__ 方法。
    """
    def __init__(self, data):
        self._data = data

    def __getattribute__(self, name):
        """
        目的：获取属性
        解释：返回属性值。
        """
        data_dict = super().__getattribute__('_data')
        return data_dict[name]

data = DictionaryRecord({'foo': 3})
print('foo: ', data.foo)
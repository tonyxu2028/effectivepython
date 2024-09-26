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
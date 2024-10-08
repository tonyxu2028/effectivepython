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


# 军规 26: Use functools.wraps to Improve Decorators
# 军规 26: 使用 functools.wraps 改善装饰器

"""
Use functools.wraps to Improve Decorators
使用 functools.wraps 改善装饰器
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
atexit.register(TEST_DIR.cleanup)

# Make sure Windows processes exit cleanly
OLD_CWD = os.getcwd()
atexit.register(lambda: os.chdir(OLD_CWD))
os.chdir(TEST_DIR.name)


def close_open_files():
    everything = gc.get_objects()
    for obj in everything:
        if isinstance(obj, io.IOBase):
            obj.close()


atexit.register(close_open_files)

# Example 1 --- 基本装饰器示例
# 目的：展示一个简单的装饰器，它包装一个函数并打印调用信息。
# 解释：
# trace 是一个装饰器函数，它接受一个函数并返回一个新的包装函数。包装函数调用原函数，并在调用前后打印调用信息。
# 结果：装饰后的函数每次被调用时都会打印参数和值。
print(f"\n{'Example 1':*^50}")


def trace(func):
    def wrapper(*args, **kwargs):
        result = func(*args, **kwargs)
        print(f'{func.__name__}({args!r}, {kwargs!r}) '
              f'-> {result!r}')
        return result

    return wrapper


# Example 2 --- 使用装饰器装饰 Fibonacci 函数
# 目的：展示如何通过 @trace 装饰器装饰 Fibonacci 函数。
# 解释：
# Fibonacci 函数被装饰后，调用时不仅会计算 Fibonacci 数列，还会打印每次递归调用的输入和输出。
# 结果：每次 Fibonacci 函数被调用时，都会打印递归调用的详细信息。
print(f"\n{'Example 2':*^50}")


@trace
def fibonacci(n):
    """Return the n-th Fibonacci number"""
    if n in (0, 1):
        return n
    return (fibonacci(n - 2) + fibonacci(n - 1))


# Example 3 --- 手动应用装饰器
# 目的：展示如何手动将装饰器应用于函数。
# 解释：
# 通过显式调用 trace 函数，手动将 Fibonacci 函数进行装饰。
# 结果：与使用 @trace 的效果相同。
print(f"\n{'Example 3':*^50}")


def fibonacci(n):
    """Return the n-th Fibonacci number"""
    if n in (0, 1):
        return n
    return fibonacci(n - 2) + fibonacci(n - 1)


fibonacci = trace(fibonacci)

# Example 4 --- 测试装饰器
# 目的：展示装饰器的实际调用效果。
# 解释：
# 调用 Fibonacci(4) 时，装饰器会打印每次递归调用的参数和返回值。
# 结果：每次递归调用都会输出参数和返回值。
print(f"\n{'Example 4':*^50}")
fibonacci(4)

# Example 5 --- 打印装饰后的函数
# 目的：展示装饰后的函数本质上是装饰器返回的包装函数，而不是原始的 Fibonacci 函数。
# 解释：
# 打印函数时显示的是包装函数而不是原始函数。
# 结果：输出显示装饰后的函数是 wrapper 而不是 Fibonacci。
print(f"\n{'Example 5':*^50}")
print(fibonacci)

# Example 6 --- 检查装饰后的函数的帮助信息
# 目的：展示使用装饰器后，原始函数的帮助信息可能丢失。
# 解释：
# 调用 help 时，输出的是包装函数的信息，而不是原始函数的 docstring 或参数信息。
# 结果：help 显示的是 wrapper 函数的默认信息。
print(f"\n{'Example 6':*^50}")
help(fibonacci)

# Example 7 --- 装饰器和序列化的兼容性问题
# 目的：展示装饰器可能导致函数序列化失败。
# 解释：
# 由于包装函数是新的对象，它不再是原始函数，这可能会导致像 pickle 这样的序列化工具报错。
# 结果：尝试序列化装饰后的函数时会引发错误。
print(f"\n{'Example 7':*^50}")
try:
    import pickle

    pickle.dumps(fibonacci)
except:
    logging.exception('Expected')
else:
    assert False

# Example 8 --- 使用 functools.wraps 修复装饰器问题
# 目的：通过 functools.wraps 保留原始函数的元数据。
# 解释：
# @wraps 装饰器会将原始函数的元数据（如名称、docstring）复制到包装函数上，避免信息丢失。
# 结果：装饰器不再改变原始函数的名称、docstring 和其他元数据。
print(f"\n{'Example 8':*^50}")
from functools import wraps


def trace(func):
    @wraps(func)
    def wrapper(*args, **kwargs):
        result = func(*args, **kwargs)
        print(f'{func.__name__}({args!r}, {kwargs!r}) '
              f'-> {result!r}')
        return result

    return wrapper


@trace
def fibonacci(n):
    """Return the n-th Fibonacci number"""
    if n in (0, 1):
        return n
    return fibonacci(n - 2) + fibonacci(n - 1)


# Example 9 --- 使用 wraps 后的帮助信息
# 目的：展示使用 functools.wraps 后，函数的帮助信息保留完整。
# 解释：
# @wraps 保留了 Fibonacci 函数的元数据，因此 help 输出的是原始函数的帮助信息，而不是包装函数的信息。
# 结果：help 正确显示 Fibonacci 函数的 docstring 和参数信息。
print(f"\n{'Example 9':*^50}")
help(fibonacci)

# Example 10 --- 使用 wraps 后可以正常序列化
# 目的：展示使用 functools.wraps 后，函数可以正常进行序列化。
# 解释：
# @wraps 保留了原始函数的身份信息，因此序列化工具（如 pickle）能够正确处理函数对象。
# 结果：装饰后的函数可以成功序列化。
print(f"\n{'Example 10':*^50}")
print(pickle.dumps(fibonacci))

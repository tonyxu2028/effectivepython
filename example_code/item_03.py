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
import sys

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

print(f"\n{'第三条: 了解字节串,字符串与unicode区别':*^50}")


# Example 1 --- bytes 对象的表示和打印
print(f"\n{'Example 1':*^50}")
# 这是一个 bytes 对象，表示字节数据。h\x65llo 中的 \x65 是字符 e 的十六进制表示，
# 因此这个 bytes 对象实际上代表字符串 b'hello'。
a = b'h\x65llo'
# list(a)：把 bytes 对象转换为一个由字节值组成的列表。
# 因为 bytes 是一个可迭代对象，它的每个元素是 int 类型的字节值。
# 输出：[104, 101, 108, 108, 111]，这代表 ASCII 值分别为 h, e, l, l, o。
print(f"{list(a)}")
# 直接输出 bytes 对象，它会以 b'...' 的形式展示出来。
# 输出：b'hello'，这里前面的b表示这是一个 bytes 对象,这个b并不是字节串的实际内容。
print(a)


# Example 2 --- Unicode 字符串的表示和打印
print(f"\n{'Example 2':*^50}")
# 这是一个 Unicode 字符串，表示为 à propos。
a = 'a\u0300 propos'
# list(a)：把 Unicode 字符串转换为一个由字符组成的列表。
# 因为 Unicode 字符串是一个可迭代对象，它的每个元素是一个字符。
# 输出：['a', '̀', ' ', 'p', 'r', 'o', 'p', 'o', 's']
print(f"{list(a)}")
# 直接输出 Unicode 字符串，它会以 '...' 的形式展示出来。
# 输出：à propos
print(a)


# Example 3
print(f"\n{'Example 3':*^50}")
"""
将输入的字节（bytes）或字符串（str）都转换为字符串。如果是 bytes，则用 UTF-8 进行解码。
"""
def to_str(bytes_or_str):
    if isinstance(bytes_or_str, bytes):
        value = bytes_or_str.decode('utf-8')
    else:
        value = bytes_or_str
    return value  # Instance of str

# to_str 函数：将输入的字节（bytes）或字符串（str）都转换为字符串。
# repr()：返回对象的“官方”字符串表示形式，方便显示特殊字符或类型。
print(repr(to_str(b'foo'))) # 'b'foo' 被转换为 'foo',原理是字节串换成了字符串
print(repr(to_str('bar')))  # 字符串 'bar' 直接返回


# Example 4
print(f"\n{'Example 4':*^50}")
"""
将输入的字节（bytes）或字符串（str）都转换为字节。如果是字符串，则用 UTF-8 进行编码。
"""
def to_bytes(bytes_or_str):
    if isinstance(bytes_or_str, str):       # 如果是字符串，则用 UTF-8 进行编码
        value = bytes_or_str.encode('utf-8')
    else:
        value = bytes_or_str
    return value  # Instance of bytes

print(repr(to_bytes(b'foo')))   # 字节串 b'foo' 直接返回
print(repr(to_bytes('bar')))    # 'bar' 被转换为 b'bar'，原理是字符串换成了字节串


# Example 5
print(f"\n{'Example 5':*^50}")
# 字节串的连接：b'one' + b'two'，这是字节串的简单连接。输出：b'onetwo'
# b 是字节串的前缀，表示这是一个字节对象（bytes 类型）。当你写 b'one' 和 b'two' 时，
# b 只是告诉 Python 这些字面量是字节串，而不是字符串。
print(b'one' + b'two')
# 字符串的连接：'one' + 'two'，这是普通字符串的连接。输出：onetwo
print('one' + 'two')

# 配置日志将输出到 stdout 而不是 stderr
logging.basicConfig(stream=sys.stdout, level=logging.INFO)

# Example 6
print(f"\n{'Example 6':*^50}")
try:
    b'one' + 'two'
except Exception as e:
    logging.error(f"Error type: {e.__class__.__name__}, Message: {str(e)}")
else:
    assert False


#Example 7
print(f"\n{'Example 7':*^50}")
try:
    'one' + b'two'
except Exception as e:
    logging.error(f"Error type: {e.__class__.__name__}, Message: {str(e)}")
else:
    assert False

print("\nExample 8-10: 比较字节和字符串")
# Example 8
print(f"\n{'Example 8':*^50}")
print(b'red' > b'blue')
assert b'red' > b'blue'
print('red' > 'blue')
assert 'red' > 'blue'


# Example 9
print(f"\n{'Example 9':*^50}")
try:
    assert 'red' > b'blue'
except Exception as e:
    logging.error(f"Error type: {e.__class__.__name__}, Message: {str(e)}")
else:
    assert False


# Example 10
print(f"\n{'Example 10':*^50}")
try:
    assert b'blue' < 'red'
except Exception as e:
    logging.error(f"Error type: {e.__class__.__name__}, Message: {str(e)}")
else:
    assert False


print("\nExample 11: 字节和字符串的相等比较")
# Example 11
print(f"\n{'Example 11':*^50}")
print(b'foo' == 'foo')  # 字节串和字符串内容可以相同但是不相等


print("\nExample 12-14: 格式化字符串和字节串")
# Example 12
print(f"\n{'Example 12':*^50}")
print(b'red %s' % b'blue')  # 字节串格式化字节串
print('red %s' % 'blue')    # 字符串格式化字符串


# Example 13
print(f"\n{'Example 13':*^50}")
try:
    print(b'red %s' % 'blue')   # 字节串格式化字符串,是失败的
except Exception as e:
    logging.error(f"Error type: {e.__class__.__name__}, Message: {str(e)}")
else:
    assert False


# Example 14
print(f"\n{'Example 14':*^50}")
print('red %s' % b'blue')   # 字符串格式化字节串,是成功的

print("\nExample 15-18 读写字节串")
# Example 15
# 二进制数据写入文本文件：尝试将字节串写入以文本模式打开的文件会失败，
# 因为文本模式下只能写入字符串，不能写入字节串。
print(f"\n{'Example 15':*^50}")
try:
    with open('data.bin', 'w') as f:
        f.write(b'\xf1\xf2\xf3\xf4\xf5')
except Exception as e:
        logging.error(f"Error type: {e.__class__.__name__}, Message: {str(e)}")
else:
    assert False


# Example 16
#以二进制模式写入文件：这时写入成功，因为文件是以 wb（写二进制）模式打开的。
print(f"\n{'Example 16':*^50}")
with open('data.bin', 'wb') as f:
    f.write(b'\xf1\xf2\xf3\xf4\xf5')


# Example 17
print(f"\n{'Example 17':*^50}")
try:
    # Silently force UTF-8 here to make sure this test fails on
    # all platforms. cp1252 considers these bytes valid on Windows.
    # 这行代码保存了 Python 内置的 open 函数到变量 real_open 中，
    # 以便在稍后调用被重新定义的 open 函数时，能够使用原始的 open 函数。
    real_open = open
    """
    重新定义 open 函数，使其总是以 UTF-8 编码打开文件。
    """
    def open(*args, **kwargs):
        kwargs['encoding'] = 'utf-8'
        return real_open(*args, **kwargs)

    with open('data.bin', 'r') as f:
        data = f.read()
except Exception as e:
        logging.error(f"Error type: {e.__class__.__name__}, Message: {str(e)}")
else:
    assert False


# Example 18
# Restore the overloaded open above.
print(f"\n{'Example 18':*^50}")
open = real_open
with open('data.bin', 'rb') as f:
    data = f.read()
assert data == b'\xf1\xf2\xf3\xf4\xf5'


# Example 19
print(f"\n{'Example 19':*^50}")
with open('data.bin', 'r', encoding='cp1252') as f:
    data = f.read()
assert data == 'ñòóôõ'

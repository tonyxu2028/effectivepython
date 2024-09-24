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

# 军规 11: Use Slicing to Access List Subsections
# 军规 11: 使用切片访问列表的子部分

"""
Use Slicing to Access List Subsections
使用切片访问列表的子部分
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
    everything = gc.get_objects()
    for obj in everything:
        if isinstance(obj, io.IOBase):
            obj.close()

atexit.register(close_open_files)


# Example 1 --- 使用切片提取列表的子部分
# 目的：演示如何通过切片获取列表的中间部分或去掉两端的元素。
# 解释：
# a[3:5] 提取列表索引 3 和 4 的元素。
# a[1:7] 提取索引从 1 到 6 的元素，去掉首尾。也就是所谓的斩头去尾
# 结果：返回列表的相应子部分。
print(f"\n{'Example 1':*^50}")
a = ['a', 'b', 'c', 'd', 'e', 'f', 'g', 'h']
print('Middle two:  ', a[3:5])
print('All but ends:', a[1:7])


# Example 2 --- 使用缺省开始索引提取前几项
# 目的：演示切片时缺省的起始索引会自动从 0 开始。
# 解释：
# a[:5] 等价于 a[0:5]，提取列表的前 5 项。
# 结果：a[:5] 和 a[0:5] 完全相同。
print(f"\n{'Example 2':*^50}")
assert a[:5] == a[0:5]


# Example 3 --- 使用缺省结束索引提取剩余部分
# 目的：演示切片时缺省的结束索引会自动扩展到列表末尾。
# 解释：
# a[5:] 等价于 a[5:len(a)]，从索引 5 开始，提取到列表末尾。
# 结果：a[5:] 和 a[5:len(a)] 完全相同。
print(f"\n{'Example 3':*^50}")
assert a[5:] == a[5:len(a)]


# Example 4 --- 各种切片用法示例
# 目的：展示多种切片用法，使用正索引和负索引。
# 解释：
# 使用正负索引和不同的起始、结束位置，提取列表的不同子部分。
# 这个也就是0的位置分别在首位的效果。
# 结果：输出对应的切片结果。
print(f"\n{'Example 4':*^50}")
print(a[:])
print(a[:5])
print(a[:-1])
print(a[4:])
print(a[-3:])
print(a[2:5])
print(a[2:-1])
print(a[-3:-1])


# Example 5 --- 切片结果对照
# 目的：通过注释展示不同切片的结果。
# 解释：
# a[:] 提取整个列表，a[:5] 提取前 5 项，a[4:] 从索引 4 提取到末尾，等等。
# 结果：展示各种切片的结果。
print(f"\n{'Example 5':*^50}")
a[:]      # ['a', 'b', 'c', 'd', 'e', 'f', 'g', 'h']
a[:5]     # ['a', 'b', 'c', 'd', 'e']
a[:-1]    # ['a', 'b', 'c', 'd', 'e', 'f', 'g']
a[4:]     #                     ['e', 'f', 'g', 'h']
a[-3:]    #                          ['f', 'g', 'h']
a[2:5]    #           ['c', 'd', 'e']
a[2:-1]   #           ['c', 'd', 'e', 'f', 'g']
a[-3:-1]  #                          ['f', 'g']


# Example 6 --- 切片索引越界
# 目的：展示当切片索引超出列表长度时的行为。
# 解释：
# 尽管列表长度不够 20，a[:20] 和 a[-20:] 不会引发错误，而是返回现有的部分。
# 结果：超出索引范围的切片自动处理，不抛出异常。
print(f"\n{'Example 6':*^50}")
first_twenty_items = a[:20]
last_twenty_items = a[-20:]


# Example 7 --- 列表索引越界时引发异常
# 目的：展示当使用单个索引超出列表长度时会引发 IndexError。
# 解释：
# a[20] 超出列表索引范围，抛出 IndexError 异常。
# 结果：捕获并记录异常信息。
print(f"\n{'Example 7':*^50}")
try:
    a[20]
except:
    logging.exception('Expected')
else:
    assert False


# Example 8 --- 切片与原列表无关
# 目的：演示切片是创建新列表，与原列表没有关联。
# 解释：
# b 是 a 的切片，修改 b 的元素不会影响 a。
# 结果：修改 b 后，a 保持不变。
print(f"\n{'Example 8':*^50}")
b = a[3:]
print('Before:   ', b)
b[1] = 99
print('After:    ', b)
print('No change:', a)


# Example 9 --- 用切片替换列表部分内容
# 目的：展示如何通过切片替换列表中的部分内容。
# 解释：
# a[2:7] 替换为 [99, 22, 14]，覆盖索引 2 到 6 的部分内容。
# 结果：替换后列表 a 发生变化。
print(f"\n{'Example 9':*^50}")
print('Before ', a)
a[2:7] = [99, 22, 14]
print('After  ', a)


# Example 10 --- 替换单个元素为多个元素
# 目的：展示如何通过切片替换单个元素为多个元素。
# 解释：
# a[2:3] 用 [47, 11] 替换，将索引 2 的元素替换为 47 和 11。
# 结果：列表长度增加。
print(f"\n{'Example 10':*^50}")
print('Before ', a)
a[2:3] = [47, 11]
print('After  ', a)


# Example 11 --- 通过切片复制列表
# 目的：展示如何通过切片复制整个列表。
# 解释：
# b = a[:] 复制列表 a，b 是新列表，但内容相同。
# 结果：b 和 a 内容相同，但不是同一个对象。
print(f"\n{'Example 11':*^50}")
b = a[:]
assert b == a and b is not a


# Example 12 --- 切片赋值影响列表对象
# 目的：演示当通过切片赋值时，列表对象仍然保持相同。
# 解释：
# b = a 使 a 和 b 指向同一个列表对象，修改 a 的内容会影响 b。
# 结果：a 和 b 都发生了内容变化，但它们仍然是同一个列表对象。
print(f"\n{'Example 12':*^50}")
b = a
print('Before a', a)
print('Before b', b)
a[:] = [101, 102, 103]
assert a is b             # Still the same list object
print('After a ', a)      # Now has different contents
print('After b ', b)      # Same list, so same contents as a

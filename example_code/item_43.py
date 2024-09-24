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
# 目的：定义一个类 FrequencyList
# 解释：继承自 list，添加 frequency 方法。
# 结果：类 FrequencyList
print(f"\n{'Example 1':*^50}")
class FrequencyList(list):
    """
    目的：定义一个类 FrequencyList
    解释：继承自 list，添加 frequency 方法。
    """
    def __init__(self, members):
        super().__init__(members)

    def frequency(self):
        """
        目的：计算频率
        解释：返回列表中每个元素的频率。
        """
        counts = {}
        for item in self:
            counts[item] = counts.get(item, 0) + 1
        return counts


# Example 2
# 目的：创建 FrequencyList 对象并测试方法
# 解释：创建 FrequencyList 对象并测试方法。
# 结果：方法测试成功
print(f"\n{'Example 2':*^50}")
foo = FrequencyList(['a', 'b', 'a', 'c', 'b', 'a', 'd'])
print('Length is', len(foo))
foo.pop()
print('After pop:', repr(foo))
print('Frequency:', foo.frequency())


# Example 3
# 目的：定义一个类 BinaryNode
# 解释：定义一个二叉树节点类。
# 结果：类 BinaryNode
print(f"\n{'Example 3':*^50}")
class BinaryNode:
    """
    目的：定义一个类 BinaryNode
    解释：定义一个二叉树节点类。
    """
    def __init__(self, value, left=None, right=None):
        self.value = value
        self.left = left
        self.right = right


# Example 4
# 目的：测试列表的索引访问
# 解释：测试列表的索引访问。
# 结果：索引访问成功
print(f"\n{'Example 4':*^50}")
bar = [1, 2, 3]
print(bar[0])


# Example 5
# 目的：测试列表的 __getitem__ 方法
# 解释：测试列表的 __getitem__ 方法。
# 结果：方法测试成功
print(f"\n{'Example 5':*^50}")
print(bar.__getitem__(0))


# Example 6
# 目的：定义一个类 IndexableNode
# 解释：继承自 BinaryNode，添加索引访问功能。
# 结果：类 IndexableNode
print(f"\n{'Example 6':*^50}")
class IndexableNode(BinaryNode):
    """
    目的：定义一个类 IndexableNode
    解释：继承自 BinaryNode，添加索引访问功能。
    """
    def _traverse(self):
        if self.left is not None:
            yield from self.left._traverse()
        yield self
        if self.right is not None:
            yield from self.right._traverse()

    def __getitem__(self, index):
        """
        目的：通过索引访问节点值
        解释：通过索引访问节点值。
        """
        for i, item in enumerate(self._traverse()):
            if i == index:
                return item.value
        raise IndexError(f'Index {index} is out of range')


# Example 7
# 目的：创建 IndexableNode 树并测试索引访问
# 解释：创建 IndexableNode 树并测试索引访问。
# 结果：索引访问成功
print(f"\n{'Example 7':*^50}")
tree = IndexableNode(
    10,
    left=IndexableNode(
        5,
        left=IndexableNode(2),
        right=IndexableNode(
            6,
            right=IndexableNode(7))),
    right=IndexableNode(
        15,
        left=IndexableNode(11))
)


# Example 8
# 目的：测试树的索引访问和成员检查
# 解释：测试树的索引访问和成员检查。
# 结果：测试成功
print(f"\n{'Example 8':*^50}")
print('LRR is', tree.left.right.right.value)
print('Index 0 is', tree[0])
print('Index 1 is', tree[1])
print('11 in the tree?', 11 in tree)
print('17 in the tree?', 17 in tree)
print('Tree is', list(tree))

try:
    tree[100]
except IndexError:
    pass
else:
    assert False


# Example 9
# 目的：测试树的长度
# 解释：尝试获取树的长度并捕获异常。
# 结果：捕获异常
print(f"\n{'Example 9':*^50}")
try:
    len(tree)
except:
    logging.exception('Expected')
else:
    assert False


# Example 10
# 目的：定义一个类 SequenceNode
# 解释：继承自 IndexableNode，添加长度计算功能。
# 结果：类 SequenceNode
print(f"\n{'Example 10':*^50}")
class SequenceNode(IndexableNode):
    """
    目的：定义一个类 SequenceNode
    解释：继承自 IndexableNode，添加长度计算功能。
    """
    def __len__(self):
        for count, _ in enumerate(self._traverse(), 1):
            pass
        return count


# Example 11
# 目的：创建 SequenceNode 树并测试长度
# 解释：创建 SequenceNode 树并测试长度。
# 结果：长度测试成功
print(f"\n{'Example 11':*^50}")
tree = SequenceNode(
    10,
    left=SequenceNode(
        5,
        left=SequenceNode(2),
        right=SequenceNode(
            6,
            right=SequenceNode(7))),
    right=SequenceNode(
        15,
        left=SequenceNode(11))
)

print('Tree length is', len(tree))


# Example 12
# 目的：测试树的 count 方法
# 解释：尝试调用树的 count 方法并捕获异常。
# 结果：捕获异常
print(f"\n{'Example 12':*^50}")
try:
    tree.count(4)
except:
    logging.exception('Expected')
else:
    assert False


# Example 13
# 目的：测试不完整的 Sequence 实现
# 解释：尝试创建不完整的 Sequence 实现并捕获异常。
# 结果：捕获异常
print(f"\n{'Example 13':*^50}")
try:
    from collections.abc import Sequence

    class BadType(Sequence):
        pass

    foo = BadType()
except:
    logging.exception('Expected')
else:
    assert False


# Example 14
# 目的：定义一个类 BetterNode
# 解释：继承自 SequenceNode 和 Sequence。
# 结果：类 BetterNode
print(f"\n{'Example 14':*^50}")
from collections.abc import Sequence

class BetterNode(SequenceNode, Sequence):
    """
    目的：定义一个类 BetterNode
    解释：继承自 SequenceNode 和 Sequence。
    """
    pass

tree = BetterNode(
    10,
    left=BetterNode(
        5,
        left=BetterNode(2),
        right=BetterNode(
            6,
            right=BetterNode(7))),
    right=BetterNode(
        15,
        left=BetterNode(11))
)

print('Index of 7 is', tree.index(7))
print('Count of 10 is', tree.count(10))
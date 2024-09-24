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
# 目的：定义一个混合类
# 解释：定义一个混合类 ToDictMixin。
# 结果：混合类
print(f"\n{'Example 1':*^50}")
class ToDictMixin:
    """
    目的：定义一个混合类
    解释：提供将对象转换为字典的方法。
    """
    def to_dict(self):
        """
        目的：将对象转换为字典
        解释：遍历对象的属性并将其转换为字典。
        """
        return self._traverse_dict(self.__dict__)

    def _traverse_dict(self, instance_dict):
        """
        目的：遍历字典
        解释：遍历字典的键值对并转换为字典。
        """
        output = {}
        for key, value in instance_dict.items():
            output[key] = self._traverse(key, value)
        return output

    def _traverse(self, key, value):
        """
        目的：遍历键值对
        解释：根据值的类型进行不同的处理。
        """
        if isinstance(value, ToDictMixin):
            return value.to_dict()
        elif isinstance(value, dict):
            return self._traverse_dict(value)
        elif isinstance(value, list):
            return [self._traverse(key, i) for i in value]
        elif hasattr(value, '__dict__'):
            return self._traverse_dict(value.__dict__)
        else:
            return value


# Example 3
# 目的：定义一个二叉树类
# 解释：定义一个二叉树类 BinaryTree，继承 ToDictMixin。
# 结果：二叉树类
print(f"\n{'Example 3':*^50}")
class BinaryTree(ToDictMixin):
    """
    目的：定义一个二叉树类
    解释：继承 ToDictMixin，提供二叉树的属性和方法。
    """
    def __init__(self, value, left=None, right=None):
        self.value = value
        self.left = left
        self.right = right


# Example 4
# 目的：创建二叉树对象并打印其字典表示
# 解释：创建二叉树对象并打印其字典表示。
# 结果：二叉树对象的字典表示
print(f"\n{'Example 4':*^50}")
tree = BinaryTree(10,
    left=BinaryTree(7, right=BinaryTree(9)),
    right=BinaryTree(13, left=BinaryTree(11)))
orig_print = print
print = pprint
print(tree.to_dict())
print = orig_print


# Example 5
# 目的：定义一个带父节点的二叉树类
# 解释：定义一个带父节点的二叉树类 BinaryTreeWithParent，继承 BinaryTree。
# 结果：带父节点的二叉树类
print(f"\n{'Example 5':*^50}")
class BinaryTreeWithParent(BinaryTree):
    """
    目的：定义一个带父节点的二叉树类
    解释：继承 BinaryTree，提供父节点的属性和方法。
    """
    def __init__(self, value, left=None, right=None, parent=None):
        super().__init__(value, left, right)
        self.parent = parent

    def _traverse(self, key, value):
        """
        目的：遍历键值对
        解释：根据值的类型进行不同的处理，避免无限递归。
        """
        if (isinstance(value, BinaryTreeWithParent) and key == 'parent'):
            return value.value
        else:
            return super()._traverse(key, value)


# Example 7
# 目的：创建带父节点的二叉树对象并打印其字典表示
# 解释：创建带父节点的二叉树对象并打印其字典表示。
# 结果：带父节点的二叉树对象的字典表示
print(f"\n{'Example 7':*^50}")
root = BinaryTreeWithParent(10)
root.left = BinaryTreeWithParent(7, parent=root)
root.left.right = BinaryTreeWithParent(9, parent=root.left)
orig_print = print
print = pprint
print(root.to_dict())
print = orig_print


# Example 8
# 目的：定义一个命名子树类
# 解释：定义一个命名子树类 NamedSubTree，继承 ToDictMixin。
# 结果：命名子树类
print(f"\n{'Example 8':*^50}")
class NamedSubTree(ToDictMixin):
    """
    目的：定义一个命名子树类
    解释：继承 ToDictMixin，提供命名子树的属性和方法。
    """
    def __init__(self, name, tree_with_parent):
        self.name = name
        self.tree_with_parent = tree_with_parent

my_tree = NamedSubTree('foobar', root.left.right)
orig_print = print
print = pprint
print(my_tree.to_dict())  # No infinite loop
print = orig_print


# Example 9
# 目的：定义一个 JSON 混合类
# 解释：定义一个 JSON 混合类 JsonMixin。
# 结果：JSON 混合类
print(f"\n{'Example 9':*^50}")
import json

class JsonMixin:
    """
    目的：定义一个 JSON 混合类
    解释：提供将对象转换为 JSON 字符串的方法。
    """
    def to_json(self):
        """
        目的：将对象转换为 JSON 字符串
        解释：使用 json.dumps 将对象转换为 JSON 字符串。
        """
        return json.dumps(self.to_dict())

    @classmethod
    def from_json(cls, data):
        """
        目的：从 JSON 字符串创建对象
        解释：使用 json.loads 将 JSON 字符串转换为字典，并创建对象。
        """
        kwargs = json.loads(data)
        return cls(**kwargs)


# Example 10
# 目的：定义数据中心机架、交换机和机器类
# 解释：定义数据中心机架、交换机和机器类，继承 ToDictMixin 和 JsonMixin。
# 结果：数据中心机架、交换机和机器类
print(f"\n{'Example 10':*^50}")
class DatacenterRack(ToDictMixin, JsonMixin):
    """
    目的：定义数据中心机架类
    解释：继承 ToDictMixin 和 JsonMixin，提供数据中心机架的属性和方法。
    """
    def __init__(self, switch=None, machines=None):
        self.switch = switch
        self.machines = machines

class Switch(ToDictMixin, JsonMixin):
    """
    目的：定义交换机类
    解释：继承 ToDictMixin 和 JsonMixin，提供交换机的属性和方法。
    """
    def __init__(self, ports=None, speed=None):
        self.ports = ports
        self.speed = speed

class Machine(ToDictMixin, JsonMixin):
    """
    目的：定义机器类
    解释：继承 ToDictMixin 和 JsonMixin，提供机器的属性和方法。
    """
    def __init__(self, cores=None, ram=None, disk=None):
        self.cores = cores
        self.ram = ram
        self.disk = disk


# Example 11
# 目的：序列化和反序列化数据中心机架对象
# 解释：将数据中心机架对象转换为 JSON 字符串并反序列化回对象。
# 结果：序列化和反序列化数据中心机架对象
print(f"\n{'Example 11':*^50}")
serialized = """{
    "switch": {"ports": 5, "speed": 1e9},
    "machines": [
        {"cores": 8, "ram": 32, "disk": 256},
        {"cores": 16, "ram": 64, "disk": 512}
    ]
}"""

deserialized = DatacenterRack.from_json(serialized)
roundtrip = deserialized.to_json()
assert json.loads(serialized) == json.loads(roundtrip)
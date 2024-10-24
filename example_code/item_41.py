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


# 军规 41：Consider Composing Functionality with Mix-in Classes
# 军规 41：考虑使用混合类组合功能

"""
混合类总结
定义：混合类是一种不能被实例化的类，主要用于为其他类提供通用功能。

特点：
无 __init__ 方法：通常不定义构造方法，避免直接实例化。
功能赋能：通过方法的组合为其他类提供额外的功能。
高度可复用：允许多个类通过继承混合类来共享功能，减少代码重复。

设计目的：
简化复用成本：让功能复用更简便，提高代码的灵活性和可维护性。
避免复杂继承层次：通过组合而非多层继承，减少类之间的复杂关系。

与抽象类的对比：
混合类不需要实例化，而抽象类可以提供实现方法并允许实例化。
混合类主要用于提供功能，而抽象类通常用于定义接口和共同特征。

使用场景:
功能模块化：适用于将某些特定功能模块化，以便在多个类之间共享。
减少继承冲突：通过组合不同的混合类，减少由于复杂继承造成的潜在冲突。
这种设计模式在 Python 中广泛应用，尤其是在需要灵活性和代码复用的场景中。
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
"""

ChatGPT said:
正是如此！总结如下：
JsonMixin 类总结
目的：JsonMixin 作为一个混合类，旨在为其他类提供 JSON 序列化和反序列化的功能，而不需要直接实例化自己。

@classmethod 的使用：
工厂方法：from_json 方法允许从 JSON 字符串创建对象，并能进行额外的处理。
与类相关：类方法能够接收任何继承自 JsonMixin 的子类作为 cls，实现灵活性。
多态性：创建的实例是调用该方法的子类的实例，而非混合类本身，符合混合类的设计初衷。
因此，@classmethod 的使用与混合类的定位并不矛盾，反而增强了混合类的功能复用性和灵活性。

You said:
那么也就是混合类里面可以有@classmethod，但是绝对不会有__init__
ChatGPT said:
是的，混合类通常不定义 __init__ 方法，因为它们的目的是为了提供附加功能，而不是实例化。以下是总结：

混合类特征：
无 __init__：不定义构造函数，不能被实例化。
可以包含 @classmethod：用于创建子类实例或实现其他类相关功能。
功能复用：通过提供通用功能，使得其他类能够轻松继承和使用这些功能。
这种设计方式确保混合类专注于功能的增强，而不干扰实例的创建逻辑。
"""
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
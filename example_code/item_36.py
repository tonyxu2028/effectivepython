#!/usr/bin/env PYTHONHASHSEED=1234 python3

# Copyright 2014-2019 Brett Slatkin, Pearson Education Inc.
# Licensed under the Apache License, Version 2.0 (the "License");

# 军规 36：Consider itertools for Working with Iterators and Generators。
# 军规 36：在处理迭代器和生成器时，建议使用 itertools 库。

"""
总结：为什么推荐使用 itertools？
在处理生成器和迭代器时，优先考虑使用 itertools 提供的工具，以简化逻辑，提高性能。
减少代码复杂度：
使用 itertools可以避免手写复杂的循环和生成器逻辑。
提高代码效率：--- 惰性求值
所有工具都使用惰性求值，按需生成数据，节省内存。
灵活组合：
你可以将 itertools 的工具自由组合，实现复杂的迭代逻辑。
"""

import random
random.seed(1234)
from pprint import pprint
import atexit
import gc
import io
import os
import tempfile
import itertools

TEST_DIR = tempfile.TemporaryDirectory()
atexit.register(TEST_DIR.cleanup)

OLD_CWD = os.getcwd()
atexit.register(lambda: os.chdir(OLD_CWD))
os.chdir(TEST_DIR.name)

def close_open_files():
    everything = gc.get_objects()
    for obj in everything:
        if isinstance(obj, io.IOBase):
            obj.close()

atexit.register(close_open_files)

# Example 1
# 目的：演示 itertools.chain 的用法。
# 结果：将多个可迭代对象连接在一起。
print(f"\n{'Example 1':*^50}")
it = itertools.chain([1, 2, 3], [4, 5, 6])
print(list(it))


# Example 2
# 目的：演示 itertools.repeat 的用法。
# 结果：重复生成指定值的序列。
print(f"\n{'Example 2':*^50}")
it = itertools.repeat('hello', 3)
print(list(it))


# Example 3
# 目的：演示 itertools.cycle 的用法。
# 结果：循环输出指定序列的元素。
# 输出：[1, 2, 1, 2, 1, 2, 1, 2, 1, 2]
print(f"\n{'Example 3':*^50}")
it = itertools.cycle([1, 2])                # 无限循环遍历 [1, 2]
result = [next(it) for _ in range(10)]      # 生成10个元素的列表
print(result)                               # 输出前10个元素


# Example 4
# 目的：演示 itertools.tee 的用法。
# 结果：创建多个独立的迭代器。
print(f"\n{'Example 4':*^50}")
it1, it2, it3 = itertools.tee(['first', 'second'], 3)
print(list(it1))
print(list(it2))
print(list(it3))


# Example 5
# 目的：演示 zip 和 itertools.zip_longest 的用法。
# 结果：将多个可迭代对象打包成元组，处理长度不一致的情况。
print(f"\n{'Example 5':*^50}")
keys = ['one', 'two', 'three']
values = [1, 2]
normal = list(zip(keys, values))
print('zip:        ', normal)

it = itertools.zip_longest(keys, values, fillvalue='nope')
longest = list(it)
print('zip_longest:', longest)


# Example 6
# 目的：演示 itertools.islice 的用法。
# 结果：切片获取可迭代对象的部分元素。
print(f"\n{'Example 6':*^50}")
values = [1, 2, 3, 4, 5, 6, 7, 8, 9, 10]
first_five = itertools.islice(values, 5)
print('First five: ', list(first_five))

middle_odds = itertools.islice(values, 2, 8, 2)
print('Middle odds:', list(middle_odds))


# Example 7
# 目的：演示 itertools.takewhile 的用法。
# 结果：根据条件获取元素，直到条件不再满足。
print(f"\n{'Example 7':*^50}")
values = [1, 2, 3, 4, 5, 6, 7, 8, 9, 10]
less_than_seven = lambda x: x < 7
it = itertools.takewhile(less_than_seven, values)
print(list(it))


# Example 8
# 目的：演示 itertools.dropwhile 的用法。
# 结果：跳过满足条件的元素，返回剩余元素。
print(f"\n{'Example 8':*^50}")
values = [1, 2, 3, 4, 5, 6, 7, 8, 9, 10]
less_than_seven = lambda x: x < 7
it = itertools.dropwhile(less_than_seven, values)
print(list(it))


# Example 9
# 目的：演示 filter 和 itertools.filterfalse 的用法。
# 结果：过滤满足和不满足条件的元素。
print(f"\n{'Example 9':*^50}")
values = [1, 2, 3, 4, 5, 6, 7, 8, 9, 10]
evens = lambda x: x % 2 == 0

filter_result = filter(evens, values)
print('Filter:      ', list(filter_result))

filter_false_result = itertools.filterfalse(evens, values)
print('Filter false:', list(filter_false_result))


# Example 10
# 目的：演示 itertools.accumulate 的用法。
# 结果：对元素进行累加操作。
print(f"\n{'Example 10':*^50}")
values = [1, 2, 3, 4, 5, 6, 7, 8, 9, 10]
sum_reduce = itertools.accumulate(values)
print('Sum:   ', list(sum_reduce))

def sum_modulo_20(first, second):
    output = first + second
    return output % 20

modulo_reduce = itertools.accumulate(values, sum_modulo_20)
print('Modulo:', list(modulo_reduce))


# Example 11
# 目的：演示 itertools.product 的用法。
# 结果：生成笛卡尔积。
print(f"\n{'Example 11':*^50}")
single = itertools.product([1, 2], repeat=2)
print('Single:  ', list(single))

multiple = itertools.product([1, 2], ['a', 'b'])
print('Multiple:', list(multiple))


# Example 12
# 目的：演示 itertools.permutations 的用法。
# 结果：生成所有排列组合。
print(f"\n{'Example 12':*^50}")
it = itertools.permutations([1, 2, 3, 4], 2)
original_print = print
print = pprint
print(list(it))
print = original_print


# Example 13
# 目的：演示 itertools.combinations 的用法。
# 结果：生成指定长度的组合。
print(f"\n{'Example 13':*^50}")
it = itertools.combinations([1, 2, 3, 4], 2)
print(list(it))


# Example 14
# 目的：演示 itertools.combinations_with_replacement 的用法。
# 结果：生成可重复的组合。
print(f"\n{'Example 14':*^50}")
it = itertools.combinations_with_replacement([1, 2, 3, 4], 2)
original_print = print
print = pprint
print(list(it))
print = original_print

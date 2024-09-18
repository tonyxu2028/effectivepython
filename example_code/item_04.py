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
"""
prefer interpreted F-strings over C-style format strings and str.format
优先使用解释型 F-strings 而不是 C 风格的格式化字符串和 str.format
"""

# 总述：为代码的执行设置一个特定的环境，使得所有代码运行时能够保证输出一致且不受外部因素影响。
# 在 《Effective Python》 的代码示例中，每个 item 的开头部分有一段类似的代码，
# 这是为了确保每个代码示例在受控、隔离的环境中运行，并生成一致的结果。

# 目的：确保示例代码中任何使用随机数的部分都能够生成一致的随机结果。
# 解释：通过设置 random.seed(1234)，即使多次运行代码，或者在不同机器上运行，
# 使用 random 模块生成的随机数序列都会相同。
# 这在展示和调试代码时特别有用，避免因为随机数的不同导致输出不一致。
import random
import sys

random.seed(1234)

# 总述：配置日志输出。
# 用于控制日志记录。在示例中，有时需要打印调试信息、异常或错误。这确保日志的输出格式和处理方式一致。
import logging
# 用于格式化打印复杂数据结构，让输出更加易读。
from pprint import pprint
# 这是系统标准输出的别名。在某些情况下，它可能用于重定向日志或输出结果。
from sys import stdout as STDOUT

# Write all output to a temporary directory
# 使用临时目录存储文件输出
import atexit
import gc
import io
import os
import tempfile
# 创建一个临时目录，用于存放任何示例代码生成的文件。
# 这样可以确保每个示例代码运行时，所有文件操作都是在隔离的、
# 临时的目录中进行，不会污染系统的文件系统或干扰其他文件。
TEST_DIR = tempfile.TemporaryDirectory()
# 注册一个钩子函数，当 Python 程序退出时自动删除这个临时目录及其内容，
# 确保程序运行后不会遗留任何文件或目录。
atexit.register(TEST_DIR.cleanup)

# Make sure Windows processes exit cleanly
# 处理 Windows 的进程退出
OLD_CWD = os.getcwd()                          # 获取当前工作目录
# 注册一个钩子函数，确保程序退出时恢复原来的工作目录
# 确保当程序退出时，自动将工作目录切换回原始的工作目录。
# 这样做是为了避免在程序结束后，当前目录仍然停留在临时目录中，影响后续的操作。
atexit.register(lambda: os.chdir(OLD_CWD))
os.chdir(TEST_DIR.name)                        # 将工作目录切换到临时目录

"""
总述：确保所有打开的文件都能被正确关闭。
"""
def close_open_files():
    everything = gc.get_objects()
    for obj in everything:
        if isinstance(obj, io.IOBase):
            obj.close()

atexit.register(close_open_files)

# 配置日志将输出到 stdout 而不是 stderr
logging.basicConfig(stream=sys.stdout, level=logging.INFO)




# Example 1 --- 二进制和十六进制格式化
# 目的：展示如何将二进制和十六进制数格式化为十进制输出。
print(f"\n{'Example 1':*^50}")
# a 是二进制数 10111011
a = 0b10111011
# b 是十六进制数 c5f
b = 0xc5f
# 输出：Binary is 187, hex is 3167
print('Binary is %d, hex is %d' % (a, b))


# Example 2 --- 百分号格式化字符串
# 目的：展示如何使用 % 格式化字符串和浮点数，并控制对齐和小数位数。
print(f"\n{'Example 2':*^50}")
# key 是 my_var，value 是 1.234
key = 'my_var'
value = 1.234
# %-10s：将字符串 key 左对齐，宽度为 10。
# %.2f： 将浮点数 value 格式化为小数点后 2 位的浮点数。
formatted = '%-10s = %.2f' % (key, value)
print(formatted)


# Example 3 --- 格式化顺序错误
# 目的：演示当格式化时参数顺序不匹配时的错误。value 是浮点数，但 %s 期望字符串，反之也是如此。
print(f"\n{'Example 3':*^50}")
try:
    reordered_tuple = '%-10s = %.2f' % (value, key)
except Exception as e:
    # ERROR:root:Error type: TypeError, Message: must be real number, not str
    logging.error(f"Error type: {e.__class__.__name__}, Message: {str(e)}")
else:
    assert False


# Example 4 --- 格式化类型不匹配错误
# 目的：演示当格式化的类型不匹配时的错误。%.2f 期望浮点数，但 key 是字符串。
print(f"\n{'Example 4':*^50}")
try:
    reordered_string = '%.2f = %-10s' % (key, value)
except Exception as e:
    # ERROR:root:Error type: TypeError, Message: must be real number, not str
    logging.error(f"Error type: {e.__class__.__name__}, Message: {str(e)}")
else:
    assert False


# Example 5 --- 百分号格式化与 enumerate 结合使用
# 目的：演示如何使用 % 格式化枚举 (enumerate) 生成的索引和值。
print(f"\n{'Example 5':*^50}")
pantry = [
    ('avocados', 1.25),
    ('bananas', 2.5),
    ('cherries', 15),
]
for i, (item, count) in enumerate(pantry):
    # 格式化字符串将索引 i 和项目 item 左对齐，并将 count 格式化为保留两位小数的浮点数。
    print('#%d: %-10s = %.2f' % (i, item, count))


# Example 6 --- 整数格式化
# 目的：演示如何将浮点数格式化为整数并四舍五入。
print(f"\n{'Example 6':*^50}")
for i, (item, count) in enumerate(pantry):
    # round(count) 对 count 进行四舍五入，并格式化为整数输出。别的参考 Example 5。
    print('#%d: %-10s = %d' % (
        i + 1,
        item.title(),
        round(count))
        )


# Example 7 --- 模板字符串替换
# 目的：展示如何使用模板字符串中的占位符进行替换。
print(f"\n{'Example 7':*^50}")
template = '%s loves food. See %s cook.'
name = 'Max'
formatted = template % (name, name)
print(formatted)


# Example 8 --- 使用 title() 格式化名字
# 目的：展示如何使用 title() 方法格式化名字。
print(f"\n{'Example 8':*^50}")
name = 'brad'
formatted = template % (name.title(), name.title())
print(formatted)


# Example 9 --- 字典键值对格式化
# 目的：展示如何使用字典键值对进行格式化。占位符根据字典中的键进行替换。
print(f"\n{'Example 9':*^50}")
key = 'my_var'
value = 1.234

old_way = '%-10s = %.2f' % (key, value)
new_way = '%(key)-10s = %(value).2f' % {'key': key, 'value': value}
reordered = '%(key)-10s = %(value).2f' % {'value': value, 'key': key}  # Swapped

# 输出 'my_var = 1.23'，并确保不同顺序的格式化结果一致。
print(old_way)
print(new_way)
print(reordered)
assert old_way == new_way == reordered


# Example 10 --- 从 tuple 到 dictionary 的格式化
# 目的：比较 tuple 和 dictionary 格式化的效果，确保两者输出一致。
# 元组格式化：
# 顺序严格，每个占位符需要按照顺序对应元组中的元素。
# 简单快速，适用于小规模的格式化。
# 可读性较差，在有多个相同类型参数时容易混淆。
# 字典格式化：
# 基于键名，更灵活且不依赖参数的顺序。
# 可读性强，格式化时可以直接看到变量名称，清晰易懂。
# 更适合复杂字符串模板或含有大量变量的场景。
print(f"\n{'Example 10':*^50}")
name = 'Max'
# 元组格式化
template = '%s loves food. See %s cook.'
before = template % (name, name)   # Tuple
# 字典格式化
template = '%(name)s loves food. See %(name)s cook.'
after = template % {'name': name}  # Dictionary
# 判断两种格式化方式的结果是否一致。
print(before)
print(after)
assert before == after


# Example 11 --- 循环与字典格式化
# 目的：展示如何在 for 循环中使用字典键值对进行格式化。
print(f"\n{'Example 11':*^50}")
for i, (item, count) in enumerate(pantry):
    # 元组格式化
    before = '#%d: %-10s = %d' % (
        i + 1,
        item.title(),
        round(count))
    # 字典格式化
    after = '#%(loop)d: %(item)-10s = %(count)d' % {
        'loop': i + 1,
        'item': item.title(),
        'count': round(count),
    }
    print(f"before ::: {before}")
    print(f"after  ::: {after}")
    assert before == after


# Example 12 --- 简单字典格式化
# 目的：展示简单的字典占位符替换。
print(f"\n{'Example 12':*^50}")
soup = 'lentil'
formatted = 'Today\'s soup is %(soup)s.' % {'soup': soup}
# 输出 'Today's soup is lentil.'。
print(formatted)


# Example 13 --- 复杂的字典格式化
# 目的：展示如何使用字典格式化复杂的字符串模板。
print(f"\n{'Example 13':*^50}")
menu = {
    'soup': 'lentil',
    'oyster': 'kumamoto',
    'special': 'schnitzel',
}
# 输出 'Today's soup is lentil, buy one, get two kumamoto oysters,
# and our special entrée is schnitzel.'。
template = ('Today\'s soup is %(soup)s, '
            'buy one get two %(oyster)s oysters, '
            'and our special entrée is %(special)s.')
formatted = template % menu
print(formatted)


# Example 14 --- format 函数
# 目的: 展示 format 函数的多种格式化方式，包括千位分隔符和字符串对齐。
print(f"\n{'Example 14':*^50}")
# 千位分隔符，保留两位小数
a = 1234.5678
formatted = format(a, ',.2f')
print(formatted)
# 中间对齐
b = 'my string'
formatted = format(b, '^20s')
print('*', formatted, '*')


# Example 15 --- 使用 format 函数进行简单格式化
# 目的：演示使用 .format() 方法进行字符串格式化。
# 解释：
# {} 占位符会被 format 中的参数依次替换，第一个 {} 替换为 key，
# 第二个 {} 替换为 value。（这个是有顺序约束的）
print(f"\n{'Example 15':*^50}")
key = 'my_var'
value = 1.234
formatted = '{} = {}'.format(key, value)
print(formatted)


# Example 16 --- 使用 format 函数对齐和控制小数点
# 目的：展示如何使用 format 方法对齐和控制小数点位数。
# 解释：
# {:<10}：key 左对齐，宽度为 10。
# {:.2f}：将 value 格式化为两位小数的浮点数。
# 用的是Example 15 中的 key 和 value。
print(f"\n{'Example 16':*^50}")
formatted = '{:<10} = {:.2f}'.format(key, value)
print(formatted)


# Example 17 --- 百分号和 format 混合使用
# 目的：演示如何在字符串中混合使用 % 和 format 方法。
# 解释：
# '%.2f%%' % 12.5：格式化 12.5 为两位小数，并在末尾加上百分号 %。
# '{} replaces {{}}'.format(1.23)：{{}} 是转义字符，用来表示单个 {}，{} 被 1.23 替换。
print(f"\n{'Example 17':*^50}")
print('%.2f%%' % 12.5)
print('{} replaces {{}}'.format(1.23))


# Example 18 --- 调换 format 占位符的顺序
# 目的：展示如何在 format 方法中通过索引调换占位符的顺序。
# 解释：
# {1}：使用 format 中的第二个参数 value 替换。
# {0}：使用第一个参数 key 替换。
# 用的是Example 15 中的 key 和 value。
print(f"\n{'Example 18':*^50}")
formatted = '{1} = {0}'.format(key, value)
print(formatted)


# Example 19 --- 重复使用 format 中的占位符
# 目的：展示如何在 format 方法中多次使用相同的占位符。
# 解释：
# {0}：两次使用 name 进行替换。
# 用的是Example 7 中的 name。
print(f"\n{'Example 19':*^50}")
formatted = '{0} loves food. See {0} cook.'.format(name)
print(formatted)


# Example 20 --- 比较旧式和 format 方法的格式化
# 目的：比较旧式 % 格式化和 .format() 方法的输出是否一致。
# 解释：
# 旧式格式化：'%d' % 10 和 '{}'.format(10) 输出一致。
# 用的是Example5中的参数pantry。
print(f"\n{'Example 20':*^50}")
for i, (item, count) in enumerate(pantry):
    old_style = '#%d: %-10s = %d' % (
        i + 1,
        item.title(),
        round(count))
    print("old_style ::: {}".format(old_style))
    new_style = '#{}: {:<10s} = {}'.format(
        i + 1,
        item.title(),
        round(count))
    print("new_style ::: {}".format(new_style))
    assert old_style == new_style


# Example 21 --- 嵌套字典访问
# 目的：展示如何使用 .format() 访问嵌套字典中的值。
# 解释：
# menu[oyster][0]：从字典 menu 中取出 oyster 对应的字符串，并获取第一个字符。
# !r：表示使用 repr() 方式打印字符。
# (repr()：返回对象的开发者可读的字符串表示，主要用于调试和开发，通常是对该对象的正式描述。)
# 结果：输出 'First letter is 'k''。
formatted = 'First letter is {menu[oyster][0]!r}'.format(menu=menu)
print(formatted)


# Example 22 --- 比较旧式百分号和 .format() 的输出
# 目的：展示如何将旧式的 % 字典格式化转换为 .format() 方法，并确保两者输出一致。
print(f"\n{'Example 22':*^50}")
old_template = (
    'Today\'s soup is %(soup)s, '
    'buy one get two %(oyster)s oysters, '
    'and our special entrée is %(special)s.')
old_formatted = old_template % {
    'soup': 'lentil',
    'oyster': 'kumamoto',
    'special': 'schnitzel',
}
print("old_formatted ::: {} ".format(old_formatted))

new_template = (
    'Today\'s soup is {soup}, '
    'buy one get two {oyster} oysters, '
    'and our special entrée is {special}.')
new_formatted = new_template.format(
    soup='lentil',
    oyster='kumamoto',
    special='schnitzel',
)
print("new_formatted ::: {} ".format(new_formatted))
assert old_formatted == new_formatted


# Example 23 --- F-strings 格式化
# 目的：演示使用 f-string 进行格式化，直接在字符串中嵌入变量。
# 解释：
# f'{key} = {value}'：通过 f-string，key 和 value 会自动替换到字符串中。
# 结果：输出 'my_var = 1.234'。
print(f"\n{'Example 23':*^50}")
key = 'my_var'
value = 1.234
formatted = f'{key} = {value}'
print(formatted)


# Example 24 --- f-string 的对齐与精度控制
# 目的：展示 f-string 的对齐和精度控制。
# 解释：
# {key!r:<10}：key 左对齐，宽度 10，并使用 repr() 格式化。
# {value:.2f}：value 保留两位小数。
# 结果：输出 'my_var     = 1.23'。
# 用的是Example23中的key和value。
formatted = f'{key!r:<10} = {value:.2f}'
print(formatted)


# Example 25 --- 比较不同格式化方式的输出
# 目的：比较不同格式化方法（f-string、百分号、format 等）的输出是否一致。
# 解释：
# f_string：使用 f-string 格式化。
f_string = f'{key:<10} = {value:.2f}'
# c_tuple：使用 % 元组格式化。
c_tuple  = '%-10s = %.2f' % (key, value)
# str_args 和 str_kw：使用 .format() 方法格式化。
str_args = '{:<10} = {:.2f}'.format(key, value)
str_kw   = '{key:<10} = {value:.2f}'.format(key=key, value=value)
# c_dict：使用 % 字典格式化。
c_dict   = '%(key)-10s = %(value).2f' % {'key': key, 'value': value}
assert c_tuple == c_dict == f_string
assert str_args == str_kw == f_string


# Example 26
print(f"\n{'Example 26':*^50}")
# 目的：比较旧式、format 和 f-string 的格式化输出是否一致。
for i, (item, count) in enumerate(pantry):
    old_style = '#%d: %-10s = %d' % (
        i + 1,
        item.title(),
        round(count))

    new_style = '#{}: {:<10s} = {}'.format(
        i + 1,
        item.title(),
        round(count))

    f_string = f'#{i+1}: {item.title():<10s} = {round(count)}'

    assert old_style == new_style == f_string


# Example 27 --- 直接使用 f-string 输出
# 目的：展示如何直接在循环中使用 f-string 进行格式化输出。
# 解释：将索引、物品名（首字母大写）和数量（四舍五入）使用 f-string 格式化。
for i, (item, count) in enumerate(pantry):
    print(f'#{i+1}: '
          f'{item.title():<10s} = '
          f'{round(count)}')


# Example 28 --- 动态控制小数点位数的 f-string
# 目的：展示如何在 f-string 中动态控制小数点位数。
# 解释：{number:.{places}f} 使用变量 places 来控制小数点后的位数。
# 结果：输出 'My number is 1.235'，小数保留 3 位。
print(f"\n{'Example 28':*^50}")
places = 3
number = 1.23456
print(f'My number is {number:.{places}f}')

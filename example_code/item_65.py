#!/usr/bin/env PYTHONHASHSEED=1234 python3

# 版权所有 2014-2019 Brett Slatkin, Pearson Education Inc.
#
# 根据 Apache 许可证 2.0 版（“许可证”）获得许可；
# 除非遵守许可证，否则您不得使用此文件。
# 您可以在以下网址获得许可证副本：
#
#     http://www.apache.org/licenses/LICENSE-2.0
#
# 除非适用法律要求或书面同意，按许可证分发的软件
# 是按“原样”分发的，没有任何明示或暗示的担保或条件。
# 请参阅许可证以了解管理权限和限制的特定语言。


# 示例 1
# 目的：展示 try-finally 语句的使用
# 解释：在文件操作中使用 try-finally 确保文件被正确关闭。
# 结果：文件被正确关闭
def try_finally_example(filename):
    """
    目的：展示 try-finally 语句的使用
    解释：在文件操作中使用 try-finally 确保文件被正确关闭。
    结果：文件被正确关闭
    """
    try:
        file = open(filename, 'r')
        data = file.read()
    finally:
        file.close()


# 示例 2
# 目的：展示 try-except 语句的使用
# 解释：在可能抛出异常的代码块中使用 try-except 捕获异常。
# 结果：异常被捕获并处理
try:
    """
    目的：展示 try-except 语句的使用
    解释：在可能抛出异常的代码块中使用 try-except 捕获异常。
    结果：异常被捕获并处理
    """
    result = 1 / 0
except ZeroDivisionError:
    result = None


# 示例 3
# 目的：展示 try-except-else 语句的使用
# 解释：在没有异常时执行 else 代码块。
# 结果：else 代码块被执行
try:
    """
    目的：展示 try-except-else 语句的使用
    解释：在没有异常时执行 else 代码块。
    结果：else 代码块被执行
    """
    result = 1 / 1
except ZeroDivisionError:
    result = None
else:
    result = 'Success'


# 示例 4
# 目的：从 JSON 数据中加载指定键的值
# 解释：使用 json 模块解析 JSON 数据并返回指定键的值。
# 结果：返回指定键的值或抛出 KeyError
import json

def load_json_key(data, key):
    """
    目的：从 JSON 数据中加载指定键的值
    解释：使用 json 模块解析 JSON 数据并返回指定键的值。
    结果：返回指定键的值或抛出 KeyError
    """
    obj = json.loads(data)
    return obj[key]


# 示例 5
# 目的：测试 load_json_key 函数
# 解释：使用断言测试 load_json_key 函数的返回值是否正确。
# 结果：测试通过或抛出 AssertionError
assert load_json_key('{"foo": "bar"}', 'foo') == 'bar'


# 示例 6
# 目的：展示 try-except-else 语句的使用
# 解释：在没有异常时执行 else 代码块。
# 结果：else 代码块被执行
try:
    """
    目的：展示 try-except-else 语句的使用
    解释：在没有异常时执行 else 代码块。
    结果：else 代码块被执行
    """
    result = 1 / 1
except ZeroDivisionError:
    result = None
else:
    result = 'Success'


# 示例 7
# 目的：展示 try-except-else 语句的使用
# 解释：在没有异常时执行 else 代码块。
# 结果：else 代码块被执行
try:
    """
    目的：展示 try-except-else 语句的使用
    解释：在没有异常时执行 else 代码块。
    结果：else 代码块被执行
    """
    result = 1 / 1
except ZeroDivisionError:
    result = None
else:
    result = 'Success'


# 示例 8
# 目的：从 JSON 文件中读取数据并进行除法运算
# 解释：读取 JSON 文件中的数据并进行除法运算，处理可能的异常。
# 结果：返回除法结果或 UNDEFINED
UNDEFINED = object()
DIE_IN_ELSE_BLOCK = False

def divide_json(path):
    """
    目的：从 JSON 文件中读取数据并进行除法运算
    解释：读取 JSON 文件中的数据并进行除法运算，处理可能的异常。
    结果：返回除法结果或 UNDEFINED
    """
    with open(path, 'r') as f:
        data = f.read()
    try:
        op = json.loads(data)
        value = (op['numerator'] /
                 op['denominator'])
    except ZeroDivisionError:
        return UNDEFINED
    else:
        if DIE_IN_ELSE_BLOCK:
            raise RuntimeError('Error in else block')
        return value


# 示例 9
# 目的：测试 divide_json 函数
# 解释：创建一个包含有效数据的 JSON 文件并测试 divide_json 函数。
# 结果：测试通过或抛出 AssertionError
temp_path = 'random_data.json'

with open(temp_path, 'w') as f:
    """
    目的：测试 divide_json 函数
    解释：创建一个包含有效数据的 JSON 文件并测试 divide_json 函数。
    结果：测试通过或抛出 AssertionError
    """
    f.write('{"numerator": 1, "denominator": 10}')

assert divide_json(temp_path) == 0.1


# 示例 10
# 目的：测试 divide_json 函数
# 解释：创建一个包含无效数据的 JSON 文件并测试 divide_json 函数。
# 结果：测试通过或抛出 AssertionError
with open(temp_path, 'w') as f:
    """
    目的：测试 divide_json 函数
    解释：创建一个包含无效数据的 JSON 文件并测试 divide_json 函数。
    结果：测试通过或抛出 AssertionError
    """
    f.write('{"numerator": 1, "denominator": 0}')

assert divide_json(temp_path) is UNDEFINED


# 示例 11
# 目的：展示 try-except-else 语句的使用
# 解释：在没有异常时执行 else 代码块。
# 结果：else 代码块被执行
try:
    """
    目的：展示 try-except-else 语句的使用
    解释：在没有异常时执行 else 代码块。
    结果：else 代码块被执行
    """
    result = 1 / 1
except ZeroDivisionError:
    result = None
else:
    result = 'Success'


# 示例 12
# 目的：展示 try-except-else 语句的使用
# 解释：在没有异常时执行 else 代码块。
# 结果：else 代码块被执行
try:
    """
    目的：展示 try-except-else 语句的使用
    解释：在没有异常时执行 else 代码块。
    结果：else 代码块被执行
    """
    result = 1 / 1
except ZeroDivisionError:
    result = None
else:
    result = 'Success'
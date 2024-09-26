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

# 复现书中的环境
import random
random.seed(1234)

import logging
from pprint import pprint
from sys import stdout as STDOUT

# 将所有输出写入临时目录
import atexit
import gc
import io
import os
import tempfile

TEST_DIR = tempfile.TemporaryDirectory()
atexit.register(TEST_DIR.cleanup)

# 确保 Windows 进程干净退出
OLD_CWD = os.getcwd()
atexit.register(lambda: os.chdir(OLD_CWD))
os.chdir(TEST_DIR.name)

def close_open_files():
    """
    目的：关闭所有打开的文件
    解释：遍历所有对象并关闭所有打开的文件。
    结果：所有打开的文件被关闭
    """
    everything = gc.get_objects()
    for obj in everything:
        if isinstance(obj, io.IOBase):
            obj.close()

atexit.register(close_open_files)


# 示例 1
# 目的：计算通话费用
# 解释：根据通话时长和费率计算通话费用。
# 结果：打印通话费用
rate = 1.45
seconds = 3*60 + 42
cost = rate * seconds / 60
print(cost)


# 示例 2
# 目的：四舍五入通话费用
# 解释：将通话费用四舍五入到小数点后两位。
# 结果：打印四舍五入后的通话费用
print(round(cost, 2))


# 示例 3
# 目的：使用 Decimal 计算通话费用
# 解释：使用 Decimal 模块计算更精确的通话费用。
# 结果：打印通话费用
from decimal import Decimal

rate = Decimal('1.45')
seconds = Decimal(3*60 + 42)
cost = rate * seconds / Decimal(60)
print(cost)


# 示例 4
# 目的：比较不同方式创建的 Decimal 对象
# 解释：打印通过字符串和浮点数创建的 Decimal 对象。
# 结果：打印 Decimal 对象
print(Decimal('1.45'))
print(Decimal(1.45))


# 示例 5
# 目的：打印字符串和整数
# 解释：打印字符串 '456' 和整数 456。
# 结果：打印字符串和整数
print('456')
print(456)


# 示例 6
# 目的：计算小额通话费用
# 解释：使用 Decimal 模块计算小额通话费用。
# 结果：打印小额通话费用
rate = Decimal('0.05')
seconds = Decimal('5')
small_cost = rate * seconds / Decimal(60)
print(small_cost)


# 示例 7
# 目的：四舍五入小额通话费用
# 解释：将小额通话费用四舍五入到小数点后两位。
# 结果：打印四舍五入后的小额通话费用
print(round(small_cost, 2))


# 示例 8
# 目的：向上取整通话费用
# 解释：使用 ROUND_UP 模式将通话费用取整到小数点后两位。
# 结果：打印取整后的通话费用
from decimal import ROUND_UP

rounded = cost.quantize(Decimal('0.01'), rounding=ROUND_UP)
print(f'Rounded {cost} to {rounded}')


# 示例 9
# 目的：向上取整小额通话费用
# 解释：使用 ROUND_UP 模式将小额通话费用取整到小数点后两位。
# 结果：打印取整后的小额通话费用
rounded = small_cost.quantize(Decimal('0.01'), rounding=ROUND_UP)
print(f'Rounded {small_cost} to {rounded}')
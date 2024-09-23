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


# 军规 25: Enforce Clarity with Keyword-Only and Positional-Only Arguments
# 军规 25: 使用仅限关键字参数和仅限位置参数来保证代码清晰

"""
Enforce Clarity with Keyword-Only and Positional-Only Arguments
使用仅限关键字参数和仅限位置参数来保证代码清晰
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


# Example 1 --- 位置参数调用
# 目的：展示通过位置参数调用函数。
# 解释：
# 函数 safe_division 接受 number 和 divisor 作为位置参数，ignore_overflow 和 ignore_zero_division 控制是否忽略异常。
# 结果：当除数为 0 时会触发 ZeroDivisionError，通过参数控制是否忽略。
print(f"\n{'Example 1':*^50}")
def safe_division(number, divisor,
                  ignore_overflow,
                  ignore_zero_division):
    try:
        return number / divisor
    except OverflowError:
        if ignore_overflow:
            return 0
        else:
            raise
    except ZeroDivisionError:
        if ignore_zero_division:
            return float('inf')
        else:
            raise


# Example 2 --- 使用位置参数调用函数
# 目的：展示通过位置参数忽略溢出错误。
# 解释：
# 通过传入 ignore_overflow=True，函数会忽略 OverflowError。
# 结果：函数返回 0，表示忽略了溢出。
print(f"\n{'Example 2':*^50}")
result = safe_division(1.0, 10**500, True, False)
print(result)


# Example 3 --- 忽略 ZeroDivisionError
# 目的：展示通过位置参数忽略 ZeroDivisionError。
# 解释：
# 当除数为 0 时，通过 ignore_zero_division=True 来忽略除零错误。
# 结果：返回正无穷大表示忽略了除零错误。
print(f"\n{'Example 3':*^50}")
result = safe_division(1.0, 0, False, True)
print(result)


# Example 4 --- 使用默认参数提供可选行为
# 目的：通过默认参数简化函数调用。
# 解释：
# 通过为 ignore_overflow 和 ignore_zero_division 提供默认值，使得调用函数时无需显式传递这些参数。
# 结果：即使不传递参数，函数依旧工作正常。
print(f"\n{'Example 4':*^50}")
def safe_division_b(number, divisor,
                    ignore_overflow=False,        # Changed
                    ignore_zero_division=False):  # Changed
    try:
        return number / divisor
    except OverflowError:
        if ignore_overflow:
            return 0
        else:
            raise
    except ZeroDivisionError:
        if ignore_zero_division:
            return float('inf')
        else:
            raise


# Example 5 --- 调用带有关键字参数的函数
# 目的：通过关键字参数调用函数并控制异常处理。
# 解释：
# 通过 ignore_overflow=True 忽略溢出错误，通过 ignore_zero_division=True 忽略除零错误。
# 结果：正确处理溢出和除零情况。
print(f"\n{'Example 5':*^50}")
result = safe_division_b(1.0, 10**500, ignore_overflow=True)
print(result)

result = safe_division_b(1.0, 0, ignore_zero_division=True)
print(result)


# Example 6 --- 保持旧代码兼容性
# 目的：确保改进后的函数仍与之前的代码兼容。
# 解释：
# 通过传递旧版函数调用所需的参数，确保函数仍然能够处理位置参数的传递。
# 结果：验证旧代码仍然有效。
print(f"\n{'Example 6':*^50}")
assert safe_division_b(1.0, 10**500, True, False) == 0


# Example 7 --- 使用仅限关键字参数保证代码清晰
# 目的：通过将部分参数限制为仅限关键字，提升函数调用的清晰度。
# 解释：
# 使用 `*` 指定 ignore_overflow 和 ignore_zero_division 必须通过关键字传递，避免位置参数带来的混淆。
# 结果：必须通过关键字调用这些参数，代码更具可读性。
print(f"\n{'Example 7':*^50}")
def safe_division_c(number, divisor, *,  # Changed
                    ignore_overflow=False,
                    ignore_zero_division=False):
    try:
        return number / divisor
    except OverflowError:
        if ignore_overflow:
            return 0
        else:
            raise
    except ZeroDivisionError:
        if ignore_zero_division:
            return float('inf')
        else:
            raise


# Example 8 --- 位置参数调用不再允许
# 目的：展示通过位置参数调用时会报错。
# 解释：
# 因为 ignore_overflow 和 ignore_zero_division 被设定为仅限关键字，位置参数传递会报错。
# 结果：捕获并记录位置参数传递导致的错误。
print(f"\n{'Example 8':*^50}")
try:
    safe_division_c(1.0, 10**500, True, False)
except:
    logging.exception('Expected')
else:
    assert False


# Example 9 --- 正确使用关键字参数
# 目的：展示如何正确地使用关键字参数调用函数。
# 解释：
# 通过关键字参数调用 ignore_zero_division，避免除零错误并返回正无穷大。
# 结果：函数正确返回正无穷大。
print(f"\n{'Example 9':*^50}")
result = safe_division_c(1.0, 0, ignore_zero_division=True)
assert result == float('inf')

try:
    result = safe_division_c(1.0, 0)
except ZeroDivisionError:
    pass  # Expected
else:
    assert False


# Example 10 --- 使用关键字参数调用
# 目的：展示通过关键字参数调用并确保结果正确。
# 解释：
# 通过关键字参数调用函数，确保参数顺序无关紧要且结果正确。
# 结果：三种不同调用方式都能返回正确结果。
print(f"\n{'Example 10':*^50}")
assert safe_division_c(number=2, divisor=5) == 0.4
assert safe_division_c(divisor=5, number=2) == 0.4
assert safe_division_c(2, divisor=5) == 0.4


# Example 11 --- 函数参数命名一致性
# 目的：通过一致的参数命名保证代码的清晰和可读性。
# 解释：
# 将 number 和 divisor 更名为 numerator 和 denominator 以符合数学术语。
# 结果：增强代码的一致性和可理解性。
print(f"\n{'Example 11':*^50}")
def safe_division_c(numerator, denominator, *,  # Changed
                    ignore_overflow=False,
                    ignore_zero_division=False):
    try:
        return numerator / denominator
    except OverflowError:
        if ignore_overflow:
            return 0
        else:
            raise
    except ZeroDivisionError:
        if ignore_zero_division:
            return float('inf')
        else:
            raise


# Example 12 --- 旧参数名调用会报错
# 目的：展示使用旧参数名调用会导致错误。
# 解释：
# 函数参数名改为 numerator 和 denominator，使用旧的 number 和 divisor 参数名会导致 KeyError。
# 结果：捕获并记录此错误。
print(f"\n{'Example 12':*^50}")
try:
    safe_division_c(number=2, divisor=5)
except:
    logging.exception('Expected')
else:
    assert False


# Example 13 --- 引入位置参数仅限符号
# 目的：展示如何使用 `/` 指定仅限位置参数，保证函数的调用清晰度。
# 解释：
# numerator 和 denominator 参数被设为仅限位置参数，无法通过关键字传递。
# 结果：只能通过位置参数传递 numerator 和 denominator，代码更具可读性。
print(f"\n{'Example 13':*^50}")
def safe_division_d(numerator, denominator, /, *,  # Changed
                    ignore_overflow=False,
                    ignore_zero_division=False):
    try:
        return numerator / denominator
    except OverflowError:
        if ignore_overflow:
            return 0
        else:
            raise
    except ZeroDivisionError:
        if ignore_zero_division:
            return float('inf')
        else:
            raise


# Example 14 --- 使用位置参数调用
# 目的：展示如何通过位置参数调用 numerator 和 denominator。
# 解释：
# numerator 和 denominator 是仅限位置参数，必须通过位置参数传递。
# 结果：返回正确的除法结果。
print(f"\n{'Example 14':*^50}")
assert safe_division_d(2, 5) == 0.4


# Example 15 --- 通过关键字参数调用会报错
# 目的：展示使用关键字参数传递仅限位置参数时会报错。
# 解释：
# numerator 和 denominator 被定义为仅限位置参数，通过关键字传递会导致错误。
# 结果：捕获并记录此错误。
print(f"\n{'Example 15':*^50}")
try:
    safe_division_d(numerator=2, denominator=5)
except:
    logging.exception('Expected')
else:
    assert False


# Example 16 --- 引入额外参数
# 目的：展示如何通过位置参数传递额外参数。
# 解释：
# 引入 ndigits 参数控制返回值的小数位数。numerator 和 denominator 依旧是仅限位置参数。
# 结果：返回四舍五入到指定小数位数的结果。
print(f"\n{'Example 16':*^50}")
def safe_division_e(numerator, denominator, /,
                    ndigits=10, *,                # Changed
                    ignore_overflow=False,
                    ignore_zero_division=False):
    try:
        fraction = numerator / denominator        # Changed
        return round(fraction, ndigits)           # Changed
    except OverflowError:
        if ignore_overflow:
            return 0
        else:
            raise
    except ZeroDivisionError:
        if ignore_zero_division:
            return float('inf')
        else:
            raise


# Example 17 --- 使用默认和自定义精度
# 目的：展示如何通过 ndigits 参数控制返回结果的精度。
# 解释：
# 通过位置参数传递 numerator 和 denominator，通过 ndigits 参数控制返回结果的精度。
# 结果：返回四舍五入到不同小数位数的结果。
print(f"\n{'Example 17':*^50}")
result = safe_division_e(22, 7)
print(result)

result = safe_division_e(22, 7, 5)
print(result)

result = safe_division_e(22, 7, ndigits=2)
print(result)

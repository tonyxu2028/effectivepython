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


# 军规 24: Use None and Docstrings to Specify Dynamic Default Arguments
# 军规 24: 使用 None 和文档字符串来指定动态默认参数

"""
Use None and Docstrings to Specify Dynamic Default Arguments
使用 None 和文档字符串来指定动态默认参数
"""

# Example 9 --- 使用类型注解和 Optional 指定动态默认参数
# 目的：展示如何通过类型注解和 Optional 来确保参数类型及其动态默认值。
# 解释：
# 使用 `Optional[datetime]` 表示 when 参数可以是 `datetime` 对象或 `None`。如果 `when` 为 `None`，则在函数内部动态设置为当前时间。
# 通过类型注解提高代码的可读性和安全性，`mypy` 可以检查类型是否正确。
# 结果：每次调用函数时都会根据参数情况输出带时间戳的日志消息。
print(f"\n{'Example 9':*^50}")

from datetime import datetime
from time import sleep
from typing import Optional

def log_typed(message: str,
              when: Optional[datetime]=None) -> None:
    """Log a message with a timestamp.

    Args:
        message: Message to print.
        when: datetime of when the message occurred.
            Defaults to the present time.
    """
    if when is None:
        when = datetime.now()
    print(f'{when}: {message}')

log_typed('Hi there!')
sleep(0.1)
log_typed('Hello again!')

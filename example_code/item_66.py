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
# 目的：展示 Lock 的使用
# 解释：使用 with 语句和 Lock 确保代码块的原子性。
# 结果：代码块在锁定期间执行
from threading import Lock

lock = Lock()
with lock:
    # 在保持不变的情况下执行某些操作
    pass


# 示例 2
# 目的：展示 Lock 的使用
# 解释：使用 acquire 和 release 方法确保代码块的原子性。
# 结果：代码块在锁定期间执行
lock.acquire()
try:
    # 在保持不变的情况下执行某些操作
    pass
finally:
    lock.release()


# 示例 3
# 目的：设置日志记录级别
# 解释：将日志记录级别设置为 WARNING。
# 结果：仅记录警告及以上级别的日志
import logging
logging.getLogger().setLevel(logging.WARNING)

def my_function():
    """
    目的：记录调试和错误日志
    解释：记录一些调试数据和错误日志。
    结果：记录错误日志
    """
    logging.debug('一些调试数据')
    logging.error('错误日志在这里')
    logging.debug('更多调试数据')


# 示例 4
# 目的：调用 my_function 函数
# 解释：调用 my_function 函数以记录日志。
# 结果：记录错误日志
my_function()


# 示例 5
# 目的：定义一个上下文管理器来设置日志记录级别
# 解释：使用 contextmanager 装饰器定义一个上下文管理器来临时设置日志记录级别。
# 结果：在上下文管理器内设置日志记录级别
from contextlib import contextmanager

@contextmanager
def debug_logging(level):
    """
    目的：定义一个上下文管理器来设置日志记录级别
    解释：使用 contextmanager 装饰器定义一个上下文管理器来临时设置日志记录级别。
    结果：在上下文管理器内设置日志记录级别
    """
    logger = logging.getLogger()
    old_level = logger.getEffectiveLevel()
    logger.setLevel(level)
    try:
        yield
    finally:
        logger.setLevel(old_level)


# 示例 6
# 目的：使用 debug_logging 上下文管理器
# 解释：在上下文管理器内设置日志记录级别为 DEBUG 并调用 my_function。
# 结果：记录调试和错误日志
with debug_logging(logging.DEBUG):
    print('* 内部:')
    my_function()

print('* 之后:')
my_function()


# 示例 7
# 目的：写入数据到文件
# 解释：使用 with 语句打开文件并写入数据。
# 结果：数据被写入文件
with open('my_output.txt', 'w') as handle:
    handle.write('这是一些数据!')


# 示例 8
# 目的：定义一个上下文管理器来设置指定日志记录器的级别
# 解释：使用 contextmanager 装饰器定义一个上下文管理器来临时设置指定日志记录器的级别。
# 结果：在上下文管理器内设置指定日志记录器的级别
@contextmanager
def log_level(level, name):
    """
    目的：定义一个上下文管理器来设置指定日志记录器的级别
    解释：使用 contextmanager 装饰器定义一个上下文管理器来临时设置指定日志记录器的级别。
    结果：在上下文管理器内设置指定日志记录器的级别
    """
    logger = logging.getLogger(name)
    old_level = logger.getEffectiveLevel()
    logger.setLevel(level)
    try:
        yield logger
    finally:
        logger.setLevel(old_level)


# 示例 9
# 目的：使用 log_level 上下文管理器
# 解释：在上下文管理器内设置指定日志记录器的级别为 DEBUG 并记录调试消息。
# 结果：记录调试消息
with log_level(logging.DEBUG, 'my-log') as logger:
    logger.debug(f'这是 {logger.name} 的消息!')
    logging.debug('这不会打印')


# 示例 10
# 目的：记录错误日志
# 解释：记录错误日志并验证调试日志不会被记录。
# 结果：记录错误日志
logger = logging.getLogger('my-log')
logger.debug('调试不会打印')
logger.error('错误会打印')


# 示例 11
# 目的：使用 log_level 上下文管理器
# 解释：在上下文管理器内设置指定日志记录器的级别为 DEBUG 并记录调试消息。
# 结果：记录调试消息
with log_level(logging.DEBUG, 'other-log') as logger:
    logger.debug(f'这是 {logger.name} 的消息!')
    logging.debug('这不会打印')
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
# 目的：将时间戳转换为本地时间字符串
# 解释：使用 time.localtime 和 time.strftime 将时间戳转换为本地时间字符串。
# 结果：打印本地时间字符串
import time

now = 1552774475
local_tuple = time.localtime(now)
time_format = '%Y-%m-%d %H:%M:%S'
time_str = time.strftime(time_format, local_tuple)
print(time_str)


# 示例 2
# 目的：将本地时间字符串转换为时间戳
# 解释：使用 time.strptime 和 time.mktime 将本地时间字符串转换为时间戳。
# 结果：打印时间戳
time_tuple = time.strptime(time_str, time_format)
utc_now = time.mktime(time_tuple)
print(utc_now)


# 示例 3
# 目的：解析带时区的时间字符串
# 解释：使用 time.strptime 和 time.strftime 解析带时区的时间字符串。
# 结果：打印解析后的时间字符串
import os

if os.name == 'nt':
    print("此示例不适用于 Windows")
else:
    parse_format = '%Y-%m-%d %H:%M:%S %Z'
    depart_sfo = '2019-03-16 15:45:16 PDT'
    time_tuple = time.strptime(depart_sfo, parse_format)
    time_str = time.strftime(time_format, time_tuple)
    print(time_str)


# 示例 4
# 目的：处理解析错误
# 解释：尝试解析不带时区的时间字符串并捕获异常。
# 结果：记录异常
try:
    arrival_nyc = '2019-03-16 23:33:24 EDT'
    time_tuple = time.strptime(arrival_nyc, time_format)
except:
    logging.exception('预期的异常')
else:
    assert False


# 示例 5
# 目的：将 datetime 对象转换为本地时间
# 解释：使用 datetime 和 timezone 模块将 UTC 时间转换为本地时间。
# 结果：打印本地时间
from datetime import datetime, timezone

now = datetime(2019, 3, 16, 22, 14, 35)
now_utc = now.replace(tzinfo=timezone.utc)
now_local = now_utc.astimezone()
print(now_local)


# 示例 6
# 目的：将时间字符串转换为时间戳
# 解释：使用 datetime.strptime 和 time.mktime 将时间字符串转换为时间戳。
# 结果：打印时间戳
time_str = '2019-03-16 15:14:35'
now = datetime.strptime(time_str, time_format)
time_tuple = now.timetuple()
utc_now = time.mktime(time_tuple)
print(utc_now)


# 示例 7
# 目的：将本地时间转换为 UTC 时间
# 解释：使用 pytz 模块将本地时间转换为 UTC 时间。
# 结果：打印 UTC 时间
import pytz

arrival_nyc = '2019-03-16 23:33:24'
nyc_dt_naive = datetime.strptime(arrival_nyc, time_format)
eastern = pytz.timezone('US/Eastern')
nyc_dt = eastern.localize(nyc_dt_naive)
utc_dt = pytz.utc.normalize(nyc_dt.astimezone(pytz.utc))
print(utc_dt)


# 示例 8
# 目的：将 UTC 时间转换为太平洋时间
# 解释：使用 pytz 模块将 UTC 时间转换为太平洋时间。
# 结果：打印太平洋时间
pacific = pytz.timezone('US/Pacific')
sf_dt = pacific.normalize(utc_dt.astimezone(pacific))
print(sf_dt)


# 示例 9
# 目的：将 UTC 时间转换为尼泊尔时间
# 解释：使用 pytz 模块将 UTC 时间转换为尼泊尔时间。
# 结果：打印尼泊尔时间
nepal = pytz.timezone('Asia/Katmandu')
nepal_dt = nepal.normalize(utc_dt.astimezone(nepal))
print(nepal_dt)
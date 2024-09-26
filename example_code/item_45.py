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
# 目的：定义一个类 Bucket
# 解释：定义一个类 Bucket，包含 period 和 quota 字段。
# 结果：类 Bucket
print(f"\n{'Example 1':*^50}")
from datetime import datetime, timedelta

class Bucket:
    """
    目的：定义一个类 Bucket
    解释：包含 period 和 quota 字段。
    """
    def __init__(self, period):
        self.period_delta = timedelta(seconds=period)
        self.reset_time = datetime.now()
        self.quota = 0

    def __repr__(self):
        """
        目的：返回对象的字符串表示
        解释：返回对象的字符串表示。
        """
        return f'Bucket(quota={self.quota})'

bucket = Bucket(60)
print(bucket)


# Example 2
# 目的：定义一个函数 fill
# 解释：定义一个函数 fill，向 bucket 中添加配额。
# 结果：函数 fill
print(f"\n{'Example 2':*^50}")
def fill(bucket, amount):
    """
    目的：向 bucket 中添加配额
    解释：如果超过了重置时间，则重置配额。然后添加配额。
    """
    now = datetime.now()
    if (now - bucket.reset_time) > bucket.period_delta:
        bucket.quota = 0
        bucket.reset_time = now
    bucket.quota += amount


# Example 3
# 目的：定义一个函数 deduct
# 解释：定义一个函数 deduct，从 bucket 中扣除配额。
# 结果：函数 deduct
print(f"\n{'Example 3':*^50}")
def deduct(bucket, amount):
    """
    目的：从 bucket 中扣除配额
    解释：如果超过了重置时间，则重置配额。然后扣除配额。
    """
    now = datetime.now()
    if (now - bucket.reset_time) > bucket.period_delta:
        bucket.quota = 0
        bucket.reset_time = now
    if bucket.quota - amount < 0:
        return False
    bucket.quota -= amount
    return True  # Bucket had enough, quota consumed


# Example 4
# 目的：测试 fill 和 deduct 函数
# 解释：创建 Bucket 对象并测试 fill 和 deduct 函数。
# 结果：函数测试成功
print(f"\n{'Example 4':*^50}")
bucket = Bucket(60)
fill(bucket, 100)
print(bucket)

if deduct(bucket, 99):
    print('Had 99 quota')
else:
    print('Not enough for 99 quota')
print(bucket)

if deduct(bucket, 3):
    print('Had 3 quota')
else:
    print('Not enough for 3 quota')
print(bucket)


# Example 5
# 目的：定义一个类 NewBucket
# 解释：定义一个类 NewBucket，包含 period 和 quota 字段。
# 结果：类 NewBucket
print(f"\n{'Example 5':*^50}")
class NewBucket:
    """
    目的：定义一个类 NewBucket
    解释：包含 period 和 quota 字段。
    """
    def __init__(self, period):
        self.period_delta = timedelta(seconds=period)
        self.reset_time = datetime.now()
        self.max_quota = 0
        self.quota_consumed = 0

    def __repr__(self):
        """
        目的：返回对象的字符串表示
        解释：返回对象的字符串表示。
        """
        return (f'NewBucket(max_quota={self.max_quota}, '
                f'quota_consumed={self.quota_consumed})')

    @property
    def quota(self):
        """
        目的：获取剩余配额
        解释：返回剩余配额。
        """
        return self.max_quota - self.quota_consumed

    @quota.setter
    def quota(self, amount):
        """
        目的：设置配额
        解释：设置配额并更新最大配额和已消耗配额。
        """
        delta = self.max_quota - amount
        if amount == 0:
            self.quota_consumed = 0
            self.max_quota = 0
        elif delta < 0:
            self.max_quota = amount
            self.quota_consumed = 0
        else:
            self.quota_consumed = self.max_quota - amount


# Example 6
# 目的：测试 NewBucket 类
# 解释：创建 NewBucket 对象并测试 fill 和 deduct 函数。
# 结果：类测试成功
print(f"\n{'Example 6':*^50}")
bucket = NewBucket(60)
print('Initial', bucket)
fill(bucket, 100)
print('Filled', bucket)

if deduct(bucket, 99):
    print('Had 99 quota')
else:
    print('Not enough for 99 quota')

print('Now', bucket)

if deduct(bucket, 3):
    print('Had 3 quota')
else:
    print('Not enough for 3 quota')

print('Still', bucket)


# Example 7
# 目的：测试 NewBucket 类的属性
# 解释：创建 NewBucket 对象并测试属性。
# 结果：属性测试成功
print(f"\n{'Example 7':*^50}")
bucket = NewBucket(6000)
assert bucket.max_quota == 0
assert bucket.quota_consumed == 0
assert bucket.quota == 0

fill(bucket, 100)
assert bucket.max_quota == 100
assert bucket.quota_consumed == 0
assert bucket.quota == 100

assert deduct(bucket, 10)
assert bucket.max_quota == 100
assert bucket.quota_consumed == 10
assert bucket.quota == 90

assert deduct(bucket, 20)
assert bucket.max_quota == 100
assert bucket.quota_consumed == 30
assert bucket.quota == 70

fill(bucket, 50)
assert bucket.max_quota == 150
assert bucket.quota_consumed == 30
assert bucket.quota == 120

assert deduct(bucket, 40)
assert bucket.max_quota == 150
assert bucket.quota_consumed == 70
assert bucket.quota == 80

assert not deduct(bucket, 81)
assert bucket.max_quota == 150
assert bucket.quota_consumed == 70
assert bucket.quota == 80

bucket.reset_time += bucket.period_delta - timedelta(1)
assert bucket.quota == 80
assert not deduct(bucket, 79)

fill(bucket, 1)
assert bucket.quota == 1
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
    解释：遍历所有对象并关闭所有 io.IOBase 实例。
    结果：所有打开的文件都被关闭
    """
    everything = gc.get_objects()
    for obj in everything:
        if isinstance(obj, io.IOBase):
            obj.close()

atexit.register(close_open_files)


# 示例 1
# 目的：定义动物园数据库类
# 解释：创建一个包含获取动物、获取喂食周期和喂食动物方法的类。
# 结果：成功定义类
class ZooDatabase:

    def get_animals(self, species):
        pass

    def get_food_period(self, species):
        pass

    def feed_animal(self, name, when):
        pass


# 示例 2
# 目的：定义执行喂食操作的函数
# 解释：查询动物的喂食周期和上次喂食时间，并进行喂食操作。
# 结果：返回喂食的动物数量
from datetime import datetime

def do_rounds(database, species, *, utcnow=datetime.utcnow):
    """
    目的：执行喂食操作
    解释：查询动物的喂食周期和上次喂食时间，并进行喂食操作。
    结果：返回喂食的动物数量
    """
    now = utcnow()
    feeding_timedelta = database.get_food_period(species)
    animals = database.get_animals(species)
    fed = 0

    for name, last_mealtime in animals:
        if (now - last_mealtime) >= feeding_timedelta:
            database.feed_animal(name, now)
            fed += 1

    return fed


# 示例 3
# 目的：使用 Mock 对象模拟方法调用
# 解释：创建一个 Mock 对象并调用其方法。
# 结果：成功调用 Mock 对象的方法
from unittest.mock import Mock

database = Mock(spec=ZooDatabase)
print(database.feed_animal)
database.feed_animal()
database.feed_animal.assert_any_call()


# 示例 4
# 目的：使用 Mock 对象测试 do_rounds 函数
# 解释：创建 Mock 对象并设置其返回值。
# 结果：成功设置 Mock 对象的返回值
from datetime import timedelta
from unittest.mock import call

now_func = Mock(spec=datetime.utcnow)
now_func.return_value = datetime(2019, 6, 5, 15, 45)

database = Mock(spec=ZooDatabase)
database.get_food_period.return_value = timedelta(hours=3)
database.get_animals.return_value = [
    ('Spot', datetime(2019, 6, 5, 11, 15)),
    ('Fluffy', datetime(2019, 6, 5, 12, 30)),
    ('Jojo', datetime(2019, 6, 5, 12, 55))
]


# 示例 5
# 目的：调用 do_rounds 函数并断言返回值
# 解释：调用 do_rounds 函数并断言返回值。
# 结果：成功断言返回值
result = do_rounds(database, 'Meerkat', utcnow=now_func)
assert result == 2

database.get_food_period.assert_called_once_with('Meerkat')
database.get_animals.assert_called_once_with('Meerkat')
database.feed_animal.assert_has_calls(
    [
        call('Spot', now_func.return_value),
        call('Fluffy', now_func.return_value),
    ],
    any_order=True)


# 示例 6
# 目的：测试 Mock 对象的异常处理
# 解释：尝试调用 Mock 对象不存在的方法并捕获异常。
# 结果：成功捕获异常
try:
    database.bad_method_name()
except:
    logging.exception('Expected')
else:
    assert False


# 示例 7
# 目的：定义获取数据库实例的函数
# 解释：创建一个全局数据库实例并返回。
# 结果：成功定义函数
DATABASE = None

def get_database():
    """
    目的：获取数据库实例
    解释：创建一个全局数据库实例并返回。
    结果：返回数据库实例
    """
    global DATABASE
    if DATABASE is None:
        DATABASE = ZooDatabase()
    return DATABASE

def main(argv):
    """
    目的：主函数
    解释：获取数据库实例并执行喂食操作。
    结果：打印喂食的动物数量
    """
    database = get_database()
    species = argv[1]
    count = do_rounds(database, species)
    print(f'Fed {count} {species}(s)')
    return 0


# 示例 8
# 目的：使用 patch 模块测试 main 函数
# 解释：使用 patch 模块临时替换数据库实例并测试 main 函数。
# 结果：成功替换数据库实例并测试 main 函数
import contextlib
import io
from unittest.mock import patch

with patch('__main__.DATABASE', spec=ZooDatabase):
    now = datetime.utcnow()

    DATABASE.get_food_period.return_value = timedelta(hours=3)
    DATABASE.get_animals.return_value = [
        ('Spot', now - timedelta(minutes=4.5)),
        ('Fluffy', now - timedelta(hours=3.25)),
        ('Jojo', now - timedelta(hours=3)),
    ]

    fake_stdout = io.StringIO()
    with contextlib.redirect_stdout(fake_stdout):
        main(['program name', 'Meerkat'])

    found = fake_stdout.getvalue()
    expected = 'Fed 2 Meerkat(s)\n'

    assert found == expected
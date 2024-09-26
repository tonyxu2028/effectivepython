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
# 目的：定义数据库连接类和异常类
# 解释：创建一个数据库连接类和一个自定义异常类。
# 结果：成功定义类
class DatabaseConnection:
    def __init__(self, host, port):
        pass


class DatabaseConnectionError(Exception):
    pass


def get_animals(database, species):
    """
    目的：查询数据库中的动物
    解释：模拟查询数据库并抛出连接异常。
    结果：抛出 DatabaseConnectionError 异常
    """
    raise DatabaseConnectionError('Not connected')


# 示例 2
# 目的：测试数据库连接异常
# 解释：尝试连接数据库并捕获异常。
# 结果：成功捕获异常
try:
    database = DatabaseConnection('localhost', '4444')
    get_animals(database, 'Meerkat')
except:
    logging.exception('Expected')
else:
    assert False

# 示例 3
# 目的：使用 Mock 对象模拟函数返回值
# 解释：创建一个 Mock 对象并设置其返回值。
# 结果：成功设置 Mock 对象的返回值
from datetime import datetime
from unittest.mock import Mock

mock = Mock(spec=get_animals)
expected = [
    ('Spot', datetime(2019, 6, 5, 11, 15)),
    ('Fluffy', datetime(2019, 6, 5, 12, 30)),
    ('Jojo', datetime(2019, 6, 5, 12, 45)),
]
mock.return_value = expected

# 示例 4
# 目的：测试 Mock 对象的属性
# 解释：尝试访问 Mock 对象不存在的属性并捕获异常。
# 结果：成功捕获异常
try:
    mock.does_not_exist
except:
    logging.exception('Expected')
else:
    assert False

# 示例 5
# 目的：使用 Mock 对象模拟函数调用
# 解释：调用 Mock 对象并断言返回值。
# 结果：成功断言返回值
database = object()
result = mock(database, 'Meerkat')
assert result == expected

# 示例 6
# 目的：断言 Mock 对象的调用
# 解释：断言 Mock 对象被调用一次且参数正确。
# 结果：成功断言调用
mock.assert_called_once_with(database, 'Meerkat')

# 示例 7
# 目的：测试 Mock 对象的调用参数
# 解释：断言 Mock 对象被调用一次且参数不正确并捕获异常。
# 结果：成功捕获异常
try:
    mock.assert_called_once_with(database, 'Giraffe')
except:
    logging.exception('Expected')
else:
    assert False

# 示例 8
# 目的：使用 ANY 断言 Mock 对象的调用参数
# 解释：使用 ANY 断言 Mock 对象的调用参数。
# 结果：成功断言调用参数
from unittest.mock import ANY

mock = Mock(spec=get_animals)
mock('database 1', 'Rabbit')
mock('database 2', 'Bison')
mock('database 3', 'Meerkat')

mock.assert_called_with(ANY, 'Meerkat')

# 示例 9
# 目的：测试 Mock 对象的 side_effect
# 解释：设置 Mock 对象的 side_effect 并捕获异常。
# 结果：成功捕获异常
try:
    class MyError(Exception):
        pass


    mock = Mock(spec=get_animals)
    mock.side_effect = MyError('Whoops! Big problem')
    result = mock(database, 'Meerkat')
except:
    logging.exception('Expected')
else:
    assert False


# 示例 10
# 目的：定义数据库操作函数
# 解释：创建查询和写入数据库的函数。
# 结果：成功定义函数
def get_food_period(database, species):
    """
    目的：查询动物的喂食周期
    解释：模拟查询数据库中的喂食周期。
    结果：返回时间间隔
    """
    pass


def feed_animal(database, name, when):
    """
    目的：记录动物的喂食时间
    解释：模拟将喂食时间写入数据库。
    结果：成功写入数据库
    """
    pass


def do_rounds(database, species):
    """
    目的：执行喂食操作
    解释：查询动物的喂食周期和上次喂食时间，并进行喂食操作。
    结果：返回喂食的动物数量
    """
    now = datetime.datetime.utcnow()
    feeding_timedelta = get_food_period(database, species)
    animals = get_animals(database, species)
    fed = 0

    for name, last_mealtime in animals:
        if (now - last_mealtime) > feeding_timedelta:
            feed_animal(database, name, now)
            fed += 1

    return fed


# 示例 11
# 目的：重构 do_rounds 函数
# 解释：重构 do_rounds 函数以便于测试。
# 结果：成功重构函数
def do_rounds(database, species, *,
              now_func=datetime.utcnow,
              food_func=get_food_period,
              animals_func=get_animals,
              feed_func=feed_animal):
    """
    目的：执行喂食操作
    解释：查询动物的喂食周期和上次喂食时间，并进行喂食操作。
    结果：返回喂食的动物数量
    """
    now = now_func()
    feeding_timedelta = food_func(database, species)
    animals = animals_func(database, species)
    fed = 0

    for name, last_mealtime in animals:
        if (now - last_mealtime) > feeding_timedelta:
            feed_func(database, name, now)
            fed += 1

    return fed


# 示例 12
# 目的：使用 Mock 对象测试 do_rounds 函数
# 解释：创建 Mock 对象并设置其返回值。
# 结果：成功设置 Mock 对象的返回值
from datetime import timedelta

now_func = Mock(spec=datetime.utcnow)
now_func.return_value = datetime(2019, 6, 5, 15, 45)

food_func = Mock(spec=get_food_period)
food_func.return_value = timedelta(hours=3)

animals_func = Mock(spec=get_animals)
animals_func.return_value = [
    ('Spot', datetime(2019, 6, 5, 11, 15)),
    ('Fluffy', datetime(2019, 6, 5, 12, 30)),
    ('Jojo', datetime(2019, 6, 5, 12, 45)),
]

feed_func = Mock(spec=feed_animal)

# 示例 13
# 目的：调用 do_rounds 函数并断言返回值
# 解释：调用 do_rounds 函数并断言返回值。
# 结果：成功断言返回值
result = do_rounds(
    database,
    'Meerkat',
    now_func=now_func,
    food_func=food_func,
    animals_func=animals_func,
    feed_func=feed_func)

assert result == 2

# 示例 14
# 目的：断言 Mock 对象的调用
# 解释：断言 Mock 对象的调用次数和参数。
# 结果：成功断言调用
from unittest.mock import call

food_func.assert_called_once_with(database, 'Meerkat')

animals_func.assert_called_once_with(database, 'Meerkat')

feed_func.assert_has_calls(
    [
        call(database, 'Spot', now_func.return_value),
        call(database, 'Fluffy', now_func.return_value),
    ],
    any_order=True)

# 示例 15
# 目的：使用 patch 模块
# 解释：使用 patch 模块临时替换函数。
# 结果：成功替换函数
from unittest.mock import patch

print('Outside patch:', get_animals)

with patch('__main__.get_animals'):
    print('Inside patch: ', get_animals)

print('Outside again:', get_animals)

# 示例 16
# 目的：使用 patch 模块替换 datetime 函数
# 解释：使用 patch 模块临时替换 datetime 函数并捕获异常。
# 结果：成功捕获异常
try:
    fake_now = datetime(2019, 6, 5, 15, 45)

    with patch('datetime.datetime.utcnow'):
        datetime.utcnow.return_value = fake_now
except:
    logging.exception('Expected')
else:
    assert False


# 示例 17
# 目的：使用 patch 模块替换自定义函数
# 解释：使用 patch 模块临时替换自定义函数。
# 结果：成功替换函数
def get_do_rounds_time():
    return datetime.datetime.utcnow()


def do_rounds(database, species):
    now = get_do_rounds_time()


with patch('__main__.get_do_rounds_time'):
    pass


# 示例 18
# 目的：重构 do_rounds 函数
# 解释：重构 do_rounds 函数以便于测试。
# 结果：成功重构函数
def do_rounds(database, species, *, utcnow=datetime.utcnow):
    """
    目的：执行喂食操作
    解释：查询动物的喂食周期和上次喂食时间，并进行喂食操作。
    结果：返回喂食的动物数量
    """
    now = utcnow()
    feeding_timedelta = get_food_period(database, species)
    animals = get_animals(database, species)
    fed = 0

    for name, last_mealtime in animals:
        if (now - last_mealtime) > feeding_timedelta:
            feed_animal(database, name, now)
            fed += 1

    return fed


# 示例 19
# 目的：使用 patch.multiple 替换多个函数
# 解释：使用 patch.multiple 模块临时替换多个函数。
# 结果：成功替换多个函数
from unittest.mock import DEFAULT

with patch.multiple('__main__',
                    autospec=True,
                    get_food_period=DEFAULT,
                    get_animals=DEFAULT,
                    feed_animal=DEFAULT):
    now_func = Mock(spec=datetime.utcnow)
    now_func.return_value = datetime(2019, 6, 5, 15, 45)
    get_food_period.return_value = timedelta(hours=3)
    get_animals.return_value = [
        ('Spot', datetime(2019, 6, 5, 11, 15)),
        ('Fluffy', datetime(2019, 6, 5, 12, 30)),
        ('Jojo', datetime(2019, 6, 5, 12, 45))
    ]

    # 示例 20
    # 目的：调用 do_rounds 函数并断言返回值
    # 解释：调用 do_rounds 函数并断言返回值。
    # 结果：成功断言返回值
    result = do_rounds(database, 'Meerkat', utcnow=now_func)
    assert result == 2

    get_food_period.assert_called_once_with(database, 'Meerkat')
    get_animals.assert_called_once_with(database, 'Meerkat')
    feed_animal.assert_has_calls(
        [
            call(database, 'Spot', now_func.return_value),
            call(database, 'Fluffy', now_func.return_value),
        ],
        any_order=True)
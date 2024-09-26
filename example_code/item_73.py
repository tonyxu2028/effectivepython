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
    解释：遍历所有对象并关闭所有 IOBase 实例。
    结果：所有打开的文件都被关闭
    """
    everything = gc.get_objects()
    for obj in everything:
        if isinstance(obj, io.IOBase):
            obj.close()

atexit.register(close_open_files)


# 示例 1
# 目的：定义一个书籍类
# 解释：创建一个包含书名和到期日期的书籍类。
# 结果：成功创建书籍类
class Book:
    def __init__(self, title, due_date):
        self.title = title
        self.due_date = due_date


# 示例 2
# 目的：添加书籍到队列并按到期日期排序
# 解释：定义一个函数，将书籍添加到队列并按到期日期降序排序。
# 结果：书籍按到期日期降序排序
def add_book(queue, book):
    """
    目的：添加书籍到队列并按到期日期排序
    解释：将书籍添加到队列并按到期日期降序排序。
    结果：书籍按到期日期降序排序
    """
    queue.append(book)
    queue.sort(key=lambda x: x.due_date, reverse=True)

queue = []
add_book(queue, Book('Don Quixote', '2019-06-07'))
add_book(queue, Book('Frankenstein', '2019-06-05'))
add_book(queue, Book('Les Misérables', '2019-06-08'))
add_book(queue, Book('War and Peace', '2019-06-03'))


# 示例 3
# 目的：定义一个自定义异常类
# 解释：创建一个自定义异常类，用于表示没有过期的书籍。
# 结果：成功创建自定义异常类
class NoOverdueBooks(Exception):
    pass

def next_overdue_book(queue, now):
    """
    目的：获取下一个过期的书籍
    解释：从队列中获取下一个过期的书籍，如果没有则抛出 NoOverdueBooks 异常。
    结果：成功获取过期书籍或抛出异常
    """
    if queue:
        book = queue[-1]
        if book.due_date < now:
            queue.pop()
            return book

    raise NoOverdueBooks


# 示例 4
# 目的：测试获取过期书籍的功能
# 解释：从队列中获取过期书籍并打印书名。
# 结果：成功获取并打印过期书籍的书名
now = '2019-06-10'

found = next_overdue_book(queue, now)
print(found.title)

found = next_overdue_book(queue, now)
print(found.title)


# 示例 5
# 目的：从队列中移除书籍
# 解释：定义一个函数，从队列中移除指定的书籍。
# 结果：成功移除指定书籍
def return_book(queue, book):
    """
    目的：从队列中移除书籍
    解释：从队列中移除指定的书籍。
    结果：成功移除指定书籍
    """
    queue.remove(book)

queue = []
book = Book('Treasure Island', '2019-06-04')

add_book(queue, book)
print('Before return:', [x.title for x in queue])

return_book(queue, book)
print('After return: ', [x.title for x in queue])


# 示例 6
# 目的：测试没有过期书籍的情况
# 解释：尝试获取过期书籍，如果没有则捕获 NoOverdueBooks 异常。
# 结果：成功捕获异常
try:
    next_overdue_book(queue, now)
except NoOverdueBooks:
    pass          # Expected
else:
    assert False  # Doesn't happen


# 示例 7
# 目的：基准测试列表操作
# 解释：定义基准测试函数，测试添加和移除书籍的性能。
# 结果：打印基准测试结果
import random
import timeit

def print_results(count, tests):
    """
    目的：打印基准测试结果
    解释：计算平均迭代时间并打印结果。
    结果：成功打印基准测试结果
    """
    avg_iteration = sum(tests) / len(tests)
    print(f'Count {count:>5,} takes {avg_iteration:.6f}s')
    return count, avg_iteration

def print_delta(before, after):
    """
    目的：打印基准测试结果的差异
    解释：计算数据大小和时间的增长率并打印结果。
    结果：成功打印基准测试结果的差异
    """
    before_count, before_time = before
    after_count, after_time = after
    growth = 1 + (after_count - before_count) / before_count
    slowdown = 1 + (after_time - before_time) / before_time
    print(f'{growth:>4.1f}x data size, {slowdown:>4.1f}x time')

def list_overdue_benchmark(count):
    """
    目的：基准测试列表操作
    解释：测试添加和移除书籍的性能。
    结果：打印基准测试结果
    """
    def prepare():
        to_add = list(range(count))
        random.shuffle(to_add)
        return [], to_add

    def run(queue, to_add):
        for i in to_add:
            queue.append(i)
            queue.sort(reverse=True)

        while queue:
            queue.pop()

    tests = timeit.repeat(
        setup='queue, to_add = prepare()',
        stmt=f'run(queue, to_add)',
        globals=locals(),
        repeat=100,
        number=1)

    return print_results(count, tests)


# 示例 8
# 目的：运行基准测试
# 解释：运行基准测试并打印结果。
# 结果：成功运行基准测试并打印结果
baseline = list_overdue_benchmark(500)
for count in (1_000, 1_500, 2_000):
    print()
    comparison = list_overdue_benchmark(count)
    print_delta(baseline, comparison)


# 示例 9
# 目的：基准测试列表移除操作
# 解释：定义基准测试函数，测试从列表中移除书籍的性能。
# 结果：打印基准测试结果
def list_return_benchmark(count):
    """
    目的：基准测试列表移除操作
    解释：测试从列表中移除书籍的性能。
    结果：打印基准测试结果
    """
    def prepare():
        queue = list(range(count))
        random.shuffle(queue)

        to_return = list(range(count))
        random.shuffle(to_return)

        return queue, to_return

    def run(queue, to_return):
        for i in to_return:
            queue.remove(i)

    tests = timeit.repeat(
        setup='queue, to_return = prepare()',
        stmt=f'run(queue, to_return)',
        globals=locals(),
        repeat=100,
        number=1)

    return print_results(count, tests)


# 示例 10
# 目的：运行基准测试
# 解释：运行基准测试并打印结果。
# 结果：成功运行基准测试并打印结果
baseline = list_return_benchmark(500)
for count in (1_000, 1_500, 2_000):
    print()
    comparison = list_return_benchmark(count)
    print_delta(baseline, comparison)


# 示例 11
# 目的：使用堆添加书籍
# 解释：定义一个函数，使用堆将书籍添加到队列。
# 结果：成功使用堆添加书籍
from heapq import heappush

def add_book(queue, book):
    """
    目的：使用堆添加书籍
    解释：使用堆将书籍添加到队列。
    结果：成功使用堆添加书籍
    """
    heappush(queue, book)


# 示例 12
# 目的：测试添加书籍到堆
# 解释：尝试将书籍添加到堆，如果失败则捕获异常。
# 结果：成功捕获异常
try:
    queue = []
    add_book(queue, Book('Little Women', '2019-06-05'))
    add_book(queue, Book('The Time Machine', '2019-05-30'))
except:
    logging.exception('Expected')
else:
    assert False


# 示例 13
# 目的：定义可排序的书籍类
# 解释：使用 functools.total_ordering 装饰器定义可排序的书籍类。
# 结果：成功定义可排序的书籍类
import functools

@functools.total_ordering
class Book:
    def __init__(self, title, due_date):
        self.title = title
        self.due_date = due_date

    def __lt__(self, other):
        return self.due_date < other.due_date


# 示例 14
# 目的：测试添加书籍到堆
# 解释：将书籍添加到堆并打印书名。
# 结果：成功添加书籍到堆并打印书名
queue = []
add_book(queue, Book('Pride and Prejudice', '2019-06-01'))
add_book(queue, Book('The Time Machine', '2019-05-30'))
add_book(queue, Book('Crime and Punishment', '2019-06-06'))
add_book(queue, Book('Wuthering Heights', '2019-06-12'))
print([b.title for b in queue])


# 示例 15
# 目的：测试列表排序
# 解释：将书籍添加到列表并按到期日期排序。
# 结果：成功按到期日期排序并打印书名
queue = [
    Book('Pride and Prejudice', '2019-06-01'),
    Book('The Time Machine', '2019-05-30'),
    Book('Crime and Punishment', '2019-06-06'),
    Book('Wuthering Heights', '2019-06-12'),
]
queue.sort()
print([b.title for b in queue])


# 示例 16
# 目的：使用堆排序
# 解释：将书籍添加到列表并使用 heapify 函数排序。
# 结果：成功使用堆排序并打印书名
from heapq import heapify

queue = [
    Book('Pride and Prejudice', '2019-06-01'),
    Book('The Time Machine', '2019-05-30'),
    Book('Crime and Punishment', '2019-06-06'),
    Book('Wuthering Heights', '2019-06-12'),
]
heapify(queue)
print([b.title for b in queue])


# 示例 17
# 目的：获取下一个过期的书籍
# 解释：从堆中获取下一个过期的书籍，如果没有则抛出 NoOverdueBooks 异常。
# 结果：成功获取过期书籍或抛出异常
from heapq import heappop

def next_overdue_book(queue, now):
    """
    目的：获取下一个过期的书籍
    解释：从堆中获取下一个过期的书籍，如果没有则抛出 NoOverdueBooks 异常。
    结果：成功获取过期书籍或抛出异常
    """
    if queue:
        book = queue[0]           # Most overdue first
        if book.due_date < now:
            heappop(queue)        # Remove the overdue book
            return book

    raise NoOverdueBooks


# 示例 18
# 目的：测试获取过期书籍的功能
# 解释：从堆中获取过期书籍并打印书名。
# 结果：成功获取并打印过期书籍的书名
now = '2019-06-02'

book = next_overdue_book(queue, now)
print(book.title)

book = next_overdue_book(queue, now)
print(book.title)

try:
    next_overdue_book(queue, now)
except NoOverdueBooks:
    pass          # Expected
else:
    assert False  # Doesn't happen


# 示例 19
# 目的：基准测试堆操作
# 解释：定义基准测试函数，测试堆的添加和移除操作性能。
# 结果：打印基准测试结果
def heap_overdue_benchmark(count):
    """
    目的：基准测试堆操作
    解释：测试堆的添加和移除操作性能。
    结果：打印基准测试结果
    """
    def prepare():
        to_add = list(range(count))
        random.shuffle(to_add)
        return [], to_add

    def run(queue, to_add):
        for i in to_add:
            heappush(queue, i)
        while queue:
            heappop(queue)

    tests = timeit.repeat(
        setup='queue, to_add = prepare()',
        stmt=f'run(queue, to_add)',
        globals=locals(),
        repeat=100,
        number=1)

    return print_results(count, tests)


# 示例 20
# 目的：运行基准测试
# 解释：运行基准测试并打印结果。
# 结果：成功运行基准测试并打印结果
baseline = heap_overdue_benchmark(500)
for count in (1_000, 1_500, 2_000):
    print()
    comparison = heap_overdue_benchmark(count)
    print_delta(baseline, comparison)


# 示例 21
# 目的：定义可排序的书籍类并添加返回字段
# 解释：使用 functools.total_ordering 装饰器定义可排序的书籍类，并添加一个返回字段。
# 结果：成功定义可排序的书籍类并添加返回字段
@functools.total_ordering
class Book:
    def __init__(self, title, due_date):
        self.title = title
        self.due_date = due_date
        self.returned = False  # New field

    def __lt__(self, other):
        return self.due_date < other.due_date


# 示例 22
# 目的：获取下一个过期的书籍并处理返回的书籍
# 解释：从堆中获取下一个过期的书籍，如果书籍已返回则继续获取下一个。
# 结果：成功获取过期书籍或抛出异常
def next_overdue_book(queue, now):
    """
    目的：获取下一个过期的书籍并处理返回的书籍
    解释：从堆中获取下一个过期的书籍，如果书籍已返回则继续获取下一个。
    结果：成功获取过期书籍或抛出异常
    """
    while queue:
        book = queue[0]
        if book.returned:
            heappop(queue)
            continue

        if book.due_date < now:
            heappop(queue)
            return book

        break

    raise NoOverdueBooks

queue = []

book = Book('Pride and Prejudice', '2019-06-01')
add_book(queue, book)

book = Book('The Time Machine', '2019-05-30')
add_book(queue, book)
book.returned = True

book = Book('Crime and Punishment', '2019-06-06')
add_book(queue, book)
book.returned = True

book = Book('Wuthering Heights', '2019-06-12')
add_book(queue, book)

now = '2019-06-11'

book = next_overdue_book(queue, now)
assert book.title == 'Pride and Prejudice'

try:
    next_overdue_book(queue, now)
except NoOverdueBooks:
    pass          # Expected
else:
    assert False  # Doesn't happen


# 示例 23
# 目的：标记书籍为已返回
# 解释：定义一个函数，将书籍标记为已返回。
# 结果：成功标记书籍为已返回
def return_book(queue, book):
    """
    目的：标记书籍为已返回
    解释：将书籍标记为已返回。
    结果：成功标记书籍为已返回
    """
    book.returned = True

assert not book.returned
return_book(queue, book)
assert book.returned
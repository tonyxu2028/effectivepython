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
# 目的：定义 Email 类
# 解释：定义一个 Email 类，包含发送者、接收者和消息。
# 结果：创建 Email 类
class Email:
    def __init__(self, sender, receiver, message):
        self.sender = sender
        self.receiver = receiver
        self.message = message


# 示例 2
# 目的：生成 Email 对象
# 解释：定义一个生成器函数，生成一些 Email 对象和 None。
# 结果：生成 Email 对象和 None
def get_emails():
    yield Email('foo@example.com', 'bar@example.com', 'hello1')
    yield Email('baz@example.com', 'banana@example.com', 'hello2')
    yield None
    yield Email('meep@example.com', 'butter@example.com', 'hello3')
    yield Email('stuff@example.com', 'avocado@example.com', 'hello4')
    yield None
    yield Email('thingy@example.com', 'orange@example.com', 'hello5')
    yield Email('roger@example.com', 'bob@example.com', 'hello6')
    yield None
    yield Email('peanut@example.com', 'alice@example.com', 'hello7')
    yield None

EMAIL_IT = get_emails()

class NoEmailError(Exception):
    pass

def try_receive_email():
    """
    目的：尝试接收 Email
    解释：从生成器中获取下一个 Email 对象，如果没有则抛出 NoEmailError 异常。
    结果：返回 Email 对象或抛出异常
    """
    try:
        email = next(EMAIL_IT)
    except StopIteration:
        email = None

    if not email:
        raise NoEmailError

    print(f'Produced email: {email.message}')
    return email


# 示例 3
# 目的：生产 Email 对象
# 解释：从生成器中获取 Email 对象并添加到队列中。
# 结果：队列中添加了 Email 对象
def produce_emails(queue):
    """
    目的：生产 Email 对象
    解释：从生成器中获取 Email 对象并添加到队列中。
    结果：队列中添加了 Email 对象
    """
    while True:
        try:
            email = try_receive_email()
        except NoEmailError:
            return
        else:
            queue.append(email)  # Producer


# 示例 4
# 目的：消费一个 Email 对象
# 解释：从队列中取出一个 Email 对象并处理。
# 结果：处理了一个 Email 对象
def consume_one_email(queue):
    """
    目的：消费一个 Email 对象
    解释：从队列中取出一个 Email 对象并处理。
    结果：处理了一个 Email 对象
    """
    if not queue:
        return
    email = queue.pop(0)  # Consumer
    # Index the message for long-term archival
    print(f'Consumed email: {email.message}')


# 示例 5
# 目的：循环生产和消费 Email 对象
# 解释：在 keep_running 返回 True 时，不断生产和消费 Email 对象。
# 结果：生产和消费了多个 Email 对象
def loop(queue, keep_running):
    """
    目的：循环生产和消费 Email 对象
    解释：在 keep_running 返回 True 时，不断生产和消费 Email 对象。
    结果：生产和消费了多个 Email 对象
    """
    while keep_running():
        produce_emails(queue)
        consume_one_email(queue)

def make_test_end():
    """
    目的：创建测试结束函数
    解释：定义一个函数，在调用 10 次后返回 False。
    结果：返回一个测试结束函数
    """
    count = list(range(10))

    def func():
        if count:
            count.pop()
            return True
        return False

    return func


def my_end_func():
    pass

my_end_func = make_test_end()
loop([], my_end_func)


# 示例 6
# 目的：定义基准测试结果打印函数
# 解释：打印基准测试的平均时间。
# 结果：打印基准测试结果
import timeit

def print_results(count, tests):
    """
    目的：定义基准测试结果打印函数
    解释：打印基准测试的平均时间。
    结果：打印基准测试结果
    """
    avg_iteration = sum(tests) / len(tests)
    print(f'Count {count:>5,} takes {avg_iteration:.6f}s')
    return count, avg_iteration

def list_append_benchmark(count):
    """
    目的：定义列表 append 基准测试
    解释：测试在列表中添加元素的性能。
    结果：返回基准测试结果
    """
    def run(queue):
        for i in range(count):
            queue.append(i)

    tests = timeit.repeat(
        setup='queue = []',
        stmt='run(queue)',
        globals=locals(),
        repeat=1000,
        number=1)

    return print_results(count, tests)


# 示例 7
# 目的：打印基准测试结果的差异
# 解释：比较两个基准测试结果的差异。
# 结果：打印基准测试结果的差异
def print_delta(before, after):
    """
    目的：打印基准测试结果的差异
    解释：比较两个基准测试结果的差异。
    结果：打印基准测试结果的差异
    """
    before_count, before_time = before
    after_count, after_time = after
    growth = 1 + (after_count - before_count) / before_count
    slowdown = 1 + (after_time - before_time) / before_time
    print(f'{growth:>4.1f}x data size, {slowdown:>4.1f}x time')

baseline = list_append_benchmark(500)
for count in (1_000, 2_000, 3_000, 4_000, 5_000):
    print()
    comparison = list_append_benchmark(count)
    print_delta(baseline, comparison)


# 示例 8
# 目的：定义列表 pop 基准测试
# 解释：测试从列表中移除元素的性能。
# 结果：返回基准测试结果
def list_pop_benchmark(count):
    """
    目的：定义列表 pop 基准测试
    解释：测试从列表中移除元素的性能。
    结果：返回基准测试结果
    """
    def prepare():
        return list(range(count))

    def run(queue):
        while queue:
            queue.pop(0)

    tests = timeit.repeat(
        setup='queue = prepare()',
        stmt='run(queue)',
        globals=locals(),
        repeat=1000,
        number=1)

    return print_results(count, tests)


# 示例 9
# 目的：运行列表 pop 基准测试
# 解释：运行不同大小的列表 pop 基准测试并比较结果。
# 结果：打印基准测试结果的差异
baseline = list_pop_benchmark(500)
for count in (1_000, 2_000, 3_000, 4_000, 5_000):
    print()
    comparison = list_pop_benchmark(count)
    print_delta(baseline, comparison)


# 示例 10
# 目的：使用 deque 优化消费 Email 对象
# 解释：使用 collections.deque 优化消费 Email 对象的函数。
# 结果：提高消费 Email 对象的效率
import collections

def consume_one_email(queue):
    """
    目的：使用 deque 优化消费 Email 对象
    解释：使用 collections.deque 优化消费 Email 对象的函数。
    结果：提高消费 Email 对象的效率
    """
    if not queue:
        return
    email = queue.popleft()  # Consumer
    # Process the email message
    print(f'Consumed email: {email.message}')

def my_end_func():
    pass

my_end_func = make_test_end()
EMAIL_IT = get_emails()
loop(collections.deque(), my_end_func)


# 示例 11
# 目的：定义 deque append 基准测试
# 解释：测试在 deque 中添加元素的性能。
# 结果：返回基准测试结果
def deque_append_benchmark(count):
    """
    目的：定义 deque append 基准测试
    解释：测试在 deque 中添加元素的性能。
    结果：返回基准测试结果
    """
    def prepare():
        return collections.deque()

    def run(queue):
        for i in range(count):
            queue.append(i)

    tests = timeit.repeat(
        setup='queue = prepare()',
        stmt='run(queue)',
        globals=locals(),
        repeat=1000,
        number=1)
    return print_results(count, tests)

baseline = deque_append_benchmark(500)
for count in (1_000, 2_000, 3_000, 4_000, 5_000):
    print()
    comparison = deque_append_benchmark(count)
    print_delta(baseline, comparison)


# 示例 12
# 目的：定义 deque popleft 基准测试
# 解释：测试从 deque 中移除元素的性能。
# 结果：返回基准测试结果
def dequeue_popleft_benchmark(count):
    """
    目的：定义 deque popleft 基准测试
    解释：测试从 deque 中移除元素的性能。
    结果：返回基准测试结果
    """
    def prepare():
        return collections.deque(range(count))

    def run(queue):
        while queue:
            queue.popleft()

    tests = timeit.repeat(
        setup='queue = prepare()',
        stmt='run(queue)',
        globals=locals(),
        repeat=1000,
        number=1)

    return print_results(count, tests)

baseline = dequeue_popleft_benchmark(500)
for count in (1_000, 2_000, 3_000, 4_000, 5_000):
    print()
    comparison = dequeue_popleft_benchmark(count)
    print_delta(baseline, comparison)
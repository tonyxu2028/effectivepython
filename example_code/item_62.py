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
# 目的：定义一个自定义异常类 NoNewData
# 解释：当没有新数据可读取时抛出此异常。
# 结果：类 NoNewData
class NoNewData(Exception):
    pass

def readline(handle):
    """
    目的：读取文件中的一行
    解释：从文件句柄的当前位置读取一行数据，如果没有新数据则抛出 NoNewData 异常。
    结果：返回读取的一行数据或抛出 NoNewData 异常
    """
    offset = handle.tell()
    handle.seek(0, 2)
    length = handle.tell()

    if length == offset:
        raise NoNewData

    handle.seek(offset, 0)
    return handle.readline()


# 示例 2
# 目的：实现文件尾部读取功能
# 解释：不断读取文件的新数据并调用写入函数处理数据。
# 结果：文件的新数据被处理
import time

def tail_file(handle, interval, write_func):
    """
    目的：读取文件的新数据
    解释：不断读取文件的新数据并调用写入函数处理数据。
    结果：文件的新数据被处理
    """
    while not handle.closed:
        try:
            line = readline(handle)
        except NoNewData:
            time.sleep(interval)
        else:
            write_func(line)


# 示例 3
# 目的：使用多线程处理多个文件的尾部读取
# 解释：为每个文件句柄创建一个线程来读取文件的新数据并写入输出文件。
# 结果：多个文件的新数据被并发处理
from threading import Lock, Thread

def run_threads(handles, interval, output_path):
    """
    目的：使用多线程处理多个文件的尾部读取
    解释：为每个文件句柄创建一个线程来读取文件的新数据并写入输出文件。
    结果：多个文件的新数据被并发处理
    """
    with open(output_path, 'wb') as output:
        lock = Lock()
        def write(data):
            """
            目的：写入数据到输出文件
            解释：使用锁机制确保线程安全地写入数据到输出文件。
            结果：数据被写入输出文件
            """
            with lock:
                output.write(data)

        threads = []
        for handle in handles:
            args = (handle, interval, write)
            thread = Thread(target=tail_file, args=args)
            thread.start()
            threads.append(thread)

        for thread in threads:
            thread.join()


# 示例 4
# 目的：模拟写入句柄的代码
# 解释：生成随机数据并写入多个文件以供读取线程使用。
# 结果：多个文件被写入随机数据
import collections
import os
import random
import string
from tempfile import TemporaryDirectory

def write_random_data(path, write_count, interval):
    """
    目的：写入随机数据到文件
    解释：生成随机字符串并写入指定次数到文件中。
    结果：文件中包含随机数据
    """
    with open(path, 'wb') as f:
        for i in range(write_count):
            time.sleep(random.random() * interval)
            letters = random.choices(
                string.ascii_lowercase, k=10)
            data = f'{path}-{i:02}-{"".join(letters)}\n'
            f.write(data.encode())
            f.flush()

def start_write_threads(directory, file_count):
    """
    目的：启动多个写入线程
    解释：为每个文件路径创建一个线程来写入随机数据。
    结果：多个文件被并发写入随机数据
    """
    paths = []
    for i in range(file_count):
        path = os.path.join(directory, str(i))
        with open(path, 'w'):
            # 确保在读取线程尝试轮询时该路径上的文件将存在。
            pass
        paths.append(path)
        args = (path, 10, 0.1)
        thread = Thread(target=write_random_data, args=args)
        thread.start()
    return paths

def close_all(handles):
    """
    目的：关闭所有文件句柄
    解释：等待一段时间后关闭所有文件句柄。
    结果：所有文件句柄被关闭
    """
    time.sleep(1)
    for handle in handles:
        handle.close()

def setup():
    """
    目的：设置测试环境
    解释：创建临时目录并启动写入线程，打开文件句柄以供读取。
    结果：返回临时目录、输入路径、文件句柄和输出路径
    """
    tmpdir = TemporaryDirectory()
    input_paths = start_write_threads(tmpdir.name, 5)

    handles = []
    for path in input_paths:
        handle = open(path, 'rb')
        handles.append(handle)

    Thread(target=close_all, args=(handles,)).start()

    output_path = os.path.join(tmpdir.name, 'merged')
    return tmpdir, input_paths, handles, output_path


# 示例 5
# 目的：确认合并结果
# 解释：检查输出文件中的数据是否与输入文件中的数据一致。
# 结果：验证合并结果是否正确
def confirm_merge(input_paths, output_path):
    """
    目的：确认合并结果
    解释：检查输出文件中的数据是否与输入文件中的数据一致。
    结果：验证合并结果是否正确
    """
    found = collections.defaultdict(list)
    with open(output_path, 'rb') as f:
        for line in f:
            for path in input_paths:
                if line.find(path.encode()) == 0:
                    found[path].append(line)

    expected = collections.defaultdict(list)
    for path in input_paths:
        with open(path, 'rb') as f:
            expected[path].extend(f.readlines())

    for key, expected_lines in expected.items():
        found_lines = found[key]
        assert expected_lines == found_lines, \
            f'{expected_lines!r} == {found_lines!r}'

input_paths = ...
handles = ...
output_path = ...

tmpdir, input_paths, handles, output_path = setup()

run_threads(handles, 0.1, output_path)

confirm_merge(input_paths, output_path)

tmpdir.cleanup()


# 示例 6
# 目的：使用 asyncio 处理混合任务
# 解释：在事件循环中并发处理文件的尾部读取和写入操作。
# 结果：文件的新数据被异步处理
import asyncio

# 在 Windows 上，ProactorEventLoop 不能在线程中创建，因为它尝试注册信号处理程序。
# 这是一个解决方法，总是使用 SelectorEventLoop 策略。
# 参见：https://bugs.python.org/issue33792
policy = asyncio.get_event_loop_policy()
policy._loop_factory = asyncio.SelectorEventLoop

async def run_tasks_mixed(handles, interval, output_path):
    """
    目的：使用 asyncio 处理混合任务
    解释：在事件循环中并发处理文件的尾部读取和写入操作。
    结果：文件的新数据被异步处理
    """
    loop = asyncio.get_event_loop()

    with open(output_path, 'wb') as output:
        async def write_async(data):
            """
            目的：异步写入数据到输出文件
            解释：在事件循环中异步写入数据到输出文件。
            结果：数据被异步写入输出文件
            """
            output.write(data)

        def write(data):
            """
            目的：写入数据到输出文件
            解释：将异步写入操作提交到事件循环中执行。
            结果：数据被写入输出文件
            """
            coro = write_async(data)
            future = asyncio.run_coroutine_threadsafe(
                coro, loop)
            future.result()

        tasks = []
        for handle in handles:
            task = loop.run_in_executor(
                None, tail_file, handle, interval, write)
            tasks.append(task)

        await asyncio.gather(*tasks)


# 示例 7
input_paths = ...
handles = ...
output_path = ...

tmpdir, input_paths, handles, output_path = setup()

asyncio.run(run_tasks_mixed(handles, 0.1, output_path))

confirm_merge(input_paths, output_path)

tmpdir.cleanup()


# 示例 8
# 目的：异步读取文件的新数据
# 解释：在事件循环中异步读取文件的新数据并调用写入函数处理数据。
# 结果：文件的新数据被异步处理
async def tail_async(handle, interval, write_func):
    """
    目的：异步读取文件的新数据
    解释：在事件循环中异步读取文件的新数据并调用写入函数处理数据。
    结果：文件的新数据被异步处理
    """
    loop = asyncio.get_event_loop()

    while not handle.closed:
        try:
            line = await loop.run_in_executor(
                None, readline, handle)
        except NoNewData:
            await asyncio.sleep(interval)
        else:
            await write_func(line)


# 示例 9
# 目的：使用 asyncio 处理任务
# 解释：在事件循环中并发处理文件的尾部读取和写入操作。
# 结果：文件的新数据被异步处理
async def run_tasks(handles, interval, output_path):
    """
    目的：使用 asyncio 处理任务
    解释：在事件循环中并发处理文件的尾部读取和写入操作。
    结果：文件的新数据被异步处理
    """
    with open(output_path, 'wb') as output:
        async def write_async(data):
            """
            目的：异步写入数据到输出文件
            解释：在事件循环中异步写入数据到输出文件。
            结果：数据被异步写入输出文件
            """
            output.write(data)

        tasks = []
        for handle in handles:
            coro = tail_async(handle, interval, write_async)
            task = asyncio.create_task(coro)
            tasks.append(task)

        await asyncio.gather(*tasks)


# 示例 10
input_paths = ...
handles = ...
output_path = ...

tmpdir, input_paths, handles, output_path = setup()

asyncio.run(run_tasks(handles, 0.1, output_path))

confirm_merge(input_paths, output_path)

tmpdir.cleanup()


# 示例 11
# 目的：在新事件循环中读取文件的新数据
# 解释：在新创建的事件循环中读取文件的新数据并调用写入函数处理数据。
# 结果：文件的新数据被处理
def tail_file(handle, interval, write_func):
    """
    目的：在新事件循环中读取文件的新数据
    解释：在新创建的事件循环中读取文件的新数据并调用写入函数处理数据。
    结果：文件的新数据被处理
    """
    loop = asyncio.new_event_loop()
    asyncio.set_event_loop(loop)

    async def write_async(data):
        """
        目的：异步写入数据到输出文件
        解释：在事件循环中异步写入数据到输出文件。
        结果：数据被异步写入输出文件
        """
        write_func(data)

    coro = tail_async(handle, interval, write_async)
    loop.run_until_complete(coro)


# 示例 12
input_paths = ...
handles = ...
output_path = ...

tmpdir, input_paths, handles, output_path = setup()

run_threads(handles, 0.1, output_path)

confirm_merge(input_paths, output_path)

tmpdir.cleanup()
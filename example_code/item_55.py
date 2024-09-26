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
# 目的：定义一个函数 download
# 解释：定义一个函数 download，包含下载逻辑。
# 结果：函数 download
print(f"\n{'Example 1':*^50}")
def download(item):
    """
    目的：定义一个函数 download
    解释：包含下载逻辑。
    """
    return item


# Example 2
# 目的：定义一个函数 resize
# 解释：定义一个函数 resize，包含调整大小逻辑。
# 结果：函数 resize
print(f"\n{'Example 2':*^50}")
def resize(item):
    """
    目的：定义一个函数 resize
    解释：包含调整大小逻辑。
    """
    return item


# Example 3
# 目的：定义一个函数 upload
# 解释：定义一个函数 upload，包含上传逻辑。
# 结果：函数 upload
print(f"\n{'Example 3':*^50}")
def upload(item):
    """
    目的：定义一个函数 upload
    解释：包含上传逻辑。
    """
    return item


# Example 4
# 目的：定义一个类 MyQueue
# 解释：定义一个类 MyQueue，包含 __init__、put 和 get 方法。
# 结果：类 MyQueue
print(f"\n{'Example 4':*^50}")
from collections import deque
from threading import Lock

class MyQueue:
    """
    目的：定义一个类 MyQueue
    解释：包含 __init__、put 和 get 方法。
    """
    def __init__(self):
        self.items = deque()
        self.lock = Lock()

    def put(self, item):
        with self.lock:
            self.items.append(item)

    def get(self):
        with self.lock:
            return self.items.popleft()


# Example 5
# 目的：定义一个类 Worker
# 解释：定义一个类 Worker，继承自 Thread 并包含 run 方法。
# 结果：类 Worker
print(f"\n{'Example 5':*^50}")
from threading import Thread
import time

class Worker(Thread):
    """
    目的：定义一个类 Worker
    解释：继承自 Thread 并包含 run 方法。
    """
    def __init__(self, func, in_queue, out_queue):
        super().__init__()
        self.func = func
        self.in_queue = in_queue
        self.out_queue = out_queue
        self.polled_count = 0

    def run(self):
        while True:
            item = self.in_queue.get()
            if item is None:
                break
            result = self.func(item)
            self.out_queue.put(result)
            self.polled_count += 1


# Example 6
# 目的：创建并启动 Worker 线程
# 解释：创建并启动多个 Worker 线程。
# 结果：Worker 线程启动成功
print(f"\n{'Example 6':*^50}")
download_queue = MyQueue()
resize_queue = MyQueue()
upload_queue = MyQueue()
done_queue = MyQueue()
threads = [
    Worker(download, download_queue, resize_queue),
    Worker(resize, resize_queue, upload_queue),
    Worker(upload, upload_queue, done_queue),
]

for thread in threads:
    thread.start()

for _ in range(1000):
    download_queue.put(object())

while len(done_queue.items) < 1000:
    time.sleep(0.1)

for thread in threads:
    thread.in_queue.put(None)
    thread.join()

processed = len(done_queue.items)
polled = sum(t.polled_count for t in threads)
print(f'Processed {processed} items after polling {polled} times')


# Example 7
# 目的：使用 Queue 进行生产者-消费者模式
# 解释：使用 Queue 进行生产者-消费者模式。
# 结果：生产者-消费者模式成功
print(f"\n{'Example 7':*^50}")
from queue import Queue

my_queue = Queue()

def consumer():
    print('Consumer waiting')
    my_queue.get()
    print('Consumer done')

thread = Thread(target=consumer)
thread.start()

print('Producer putting')
my_queue.put(object())
print('Producer done')
thread.join()


# Example 8
# 目的：使用 Queue 进行生产者-消费者模式，设置缓冲区大小
# 解释：使用 Queue 进行生产者-消费者模式，设置缓冲区大小。
# 结果：生产者-消费者模式成功
print(f"\n{'Example 8':*^50}")
my_queue = Queue(1)

def consumer():
    time.sleep(0.1)
    my_queue.get()
    print('Consumer got 1')
    my_queue.get()
    print('Consumer got 2')
    print('Consumer done')

thread = Thread(target=consumer)
thread.start()

my_queue.put(object())
print('Producer put 1')
my_queue.put(object())
print('Producer put 2')
print('Producer done')
thread.join()


# Example 9
# 目的：使用 Queue 进行生产者-消费者模式，使用 task_done 和 join 方法
# 解释：使用 Queue 进行生产者-消费者模式，使用 task_done 和 join 方法。
# 结果：生产者-消费者模式成功
print(f"\n{'Example 9':*^50}")
in_queue = Queue()

def consumer():
    print('Consumer waiting')
    work = in_queue.get()
    print('Consumer working')
    print('Consumer done')
    in_queue.task_done()

thread = Thread(target=consumer)
thread.start()

print('Producer putting')
in_queue.put(object())
print('Producer waiting')
in_queue.join()
print('Producer done')
thread.join()


# Example 10
# 目的：定义一个类 ClosableQueue
# 解释：定义一个类 ClosableQueue，继承自 Queue 并包含 close 和 __iter__ 方法。
# 结果：类 ClosableQueue
print(f"\n{'Example 10':*^50}")
class ClosableQueue(Queue):
    """
    目的：定义一个类 ClosableQueue
    解释：继承自 Queue 并包含 close 和 __iter__ 方法。
    """
    SENTINEL = object()

    def close(self):
        self.put(self.SENTINEL)

    def __iter__(self):
        while True:
            item = self.get()
            try:
                if item is self.SENTINEL:
                    return
                yield item
            finally:
                self.task_done()


# Example 11
# 目的：定义一个类 StoppableWorker
# 解释：定义一个类 StoppableWorker，继承自 Thread 并包含 run 方法。
# 结果：类 StoppableWorker
print(f"\n{'Example 11':*^50}")
class StoppableWorker(Thread):
    """
    目的：定义一个类 StoppableWorker
    解释：继承自 Thread 并包含 run 方法。
    """
    def __init__(self, func, in_queue, out_queue):
        super().__init__()
        self.func = func
        self.in_queue = in_queue
        self.out_queue = out_queue

    def run(self):
        for item in self.in_queue:
            if item is None:
                break
            result = self.func(item)
            self.out_queue.put(result)


# Example 12
# 目的：创建并启动 StoppableWorker 线程
# 解释：创建并启动多个 StoppableWorker 线程。
# 结果：StoppableWorker 线程启动成功
print(f"\n{'Example 12':*^50}")
download_queue = ClosableQueue()
resize_queue = ClosableQueue()
upload_queue = ClosableQueue()
done_queue = ClosableQueue()
threads = [
    StoppableWorker(download, download_queue, resize_queue),
    StoppableWorker(resize, resize_queue, upload_queue),
    StoppableWorker(upload, upload_queue, done_queue),
]

for thread in threads:
    thread.start()

for _ in range(1000):
    download_queue.put(object())

download_queue.close()
download_queue.join()
resize_queue.close()
resize_queue.join()
upload_queue.close()
upload_queue.join()
print(done_queue.qsize(), 'items finished')

for thread in threads:
    thread.join()


# Example 13
# 目的：定义 start_threads 和 stop_threads 函数
# 解释：定义 start_threads 和 stop_threads 函数，启动和停止多个线程。
# 结果：函数 start_threads 和 stop_threads
print(f"\n{'Example 13':*^50}")
def start_threads(count, *args):
    """
    目的：定义 start_threads 函数
    解释：启动多个线程。
    """
    threads = [StoppableWorker(*args) for _ in range(count)]
    for thread in threads:
        thread.start()
    return threads

def stop_threads(closable_queue, threads):
    """
    目的：定义 stop_threads 函数
    解释：停止多个线程。
    """
    closable_queue.close()
    closable_queue.join()
    for thread in threads:
        thread.join()


# Example 14
# 目的：使用 start_threads 和 stop_threads 函数
# 解释：使用 start_threads 和 stop_threads 函数启动和停止多个线程。
# 结果：线程启动和停止成功
print(f"\n{'Example 14':*^50}")
download_queue = ClosableQueue()
resize_queue = ClosableQueue()
upload_queue = ClosableQueue()
done_queue = ClosableQueue()

download_threads = start_threads(3, download, download_queue, resize_queue)
resize_threads = start_threads(4, resize, resize_queue, upload_queue)
upload_threads = start_threads(5, upload, upload_queue, done_queue)

for _ in range(1000):
    download_queue.put(object())

stop_threads(download_queue, download_threads)
stop_threads(resize_queue, resize_threads)
stop_threads(upload_queue, upload_threads)

print(done_queue.qsize(), 'items finished')
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
    everything = gc.get_objects()
    for obj in everything:
        if isinstance(obj, io.IOBase):
            obj.close()

atexit.register(close_open_files)


# 示例 1
# 目的：将时间码转换为字节偏移量
# 解释：定义一个函数，将视频的时间码转换为字节偏移量。
# 结果：返回字节偏移量
def timecode_to_index(video_id, timecode):
    """
    目的：将时间码转换为字节偏移量
    解释：定义一个函数，将视频的时间码转换为字节偏移量。
    结果：返回字节偏移量
    """
    return 1234

def request_chunk(video_id, byte_offset, size):
    """
    目的：请求视频数据块
    解释：定义一个函数，请求指定大小的视频数据块。
    结果：返回视频数据块
    """
    pass

video_id = ...
timecode = '01:09:14:28'
byte_offset = timecode_to_index(video_id, timecode)
size = 20 * 1024 * 1024
video_data = request_chunk(video_id, byte_offset, size)


# 示例 2
# 目的：定义一个空套接字类
# 解释：创建一个空套接字类，用于模拟数据发送。
# 结果：成功创建空套接字类
class NullSocket:
    """
    目的：定义一个空套接字类
    解释：创建一个空套接字类，用于模拟数据发送。
    结果：成功创建空套接字类
    """
    def __init__(self):
        self.handle = open(os.devnull, 'wb')

    def send(self, data):
        self.handle.write(data)

socket = ...             # socket connection to client
video_data = ...         # bytes containing data for video_id
byte_offset = ...        # Requested starting position
size = 20 * 1024 * 1024  # Requested chunk size
import os

socket = NullSocket()
video_data = 100 * os.urandom(1024 * 1024)
byte_offset = 1234

chunk = video_data[byte_offset:byte_offset + size]
socket.send(chunk)


# 示例 3
# 目的：基准测试数据块发送
# 解释：定义一个函数，基准测试数据块发送的性能。
# 结果：打印基准测试结果
import timeit

def run_test():
    """
    目的：基准测试数据块发送
    解释：定义一个函数，基准测试数据块发送的性能。
    结果：打印基准测试结果
    """
    chunk = video_data[byte_offset:byte_offset + size]

result = timeit.timeit(
    stmt='run_test()',
    globals=globals(),
    number=100) / 100

print(f'{result:0.9f} seconds')


# 示例 4
# 目的：使用 memoryview 处理数据
# 解释：定义一个函数，使用 memoryview 处理数据块。
# 结果：打印 memoryview 的相关信息
data = b'shave and a haircut, two bits'
view = memoryview(data)
chunk = view[12:19]
print(chunk)
print('Size:           ', chunk.nbytes)
print('Data in view:   ', chunk.tobytes())
print('Underlying data:', chunk.obj)


# 示例 5
# 目的：基准测试 memoryview 数据块发送
# 解释：定义一个函数，基准测试使用 memoryview 发送数据块的性能。
# 结果：打印基准测试结果
video_view = memoryview(video_data)

def run_test():
    """
    目的：基准测试 memoryview 数据块发送
    解释：定义一个函数，基准测试使用 memoryview 发送数据块的性能。
    结果：打印基准测试结果
    """
    chunk = video_view[byte_offset:byte_offset + size]

result = timeit.timeit(
    stmt='run_test()',
    globals=globals(),
    number=100) / 100

print(f'{result:0.9f} seconds')


# 示例 6
# 目的：定义一个假套接字类
# 解释：创建一个假套接字类，用于模拟数据接收。
# 结果：成功创建假套接字类
class FakeSocket:
    """
    目的：定义一个假套接字类
    解释：创建一个假套接字类，用于模拟数据接收。
    结果：成功创建假套接字类
    """
    def recv(self, size):
        return video_view[byte_offset:byte_offset+size]

    def recv_into(self, buffer):
        source_data = video_view[byte_offset:byte_offset+size]
        buffer[:] = source_data

socket = ...        # socket connection to the client
video_cache = ...   # Cache of incoming video stream
byte_offset = ...   # Incoming buffer position
size = 1024 * 1024  # Incoming chunk size
socket = FakeSocket()
video_cache = video_data[:]
byte_offset = 1234

chunk = socket.recv(size)
video_view = memoryview(video_cache)
before = video_view[:byte_offset]
after = video_view[byte_offset + size:]
new_cache = b''.join([before, chunk, after])


# 示例 7
# 目的：基准测试假套接字数据接收
# 解释：定义一个函数，基准测试假套接字接收数据的性能。
# 结果：打印基准测试结果
def run_test():
    """
    目的：基准测试假套接字数据接收
    解释：定义一个函数，基准测试假套接字接收数据的性能。
    结果：打印基准测试结果
    """
    chunk = socket.recv(size)
    before = video_view[:byte_offset]
    after = video_view[byte_offset + size:]
    new_cache = b''.join([before, chunk, after])

result = timeit.timeit(
    stmt='run_test()',
    globals=globals(),
    number=100) / 100

print(f'{result:0.9f} seconds')


# 示例 8
# 目的：测试字节对象的不可变性
# 解释：尝试修改字节对象，捕获异常。
# 结果：成功捕获异常
try:
    my_bytes = b'hello'
    my_bytes[0] = b'\x79'
except:
    logging.exception('Expected')
else:
    assert False


# 示例 9
# 目的：测试 bytearray 的可变性
# 解释：创建一个 bytearray 并修改其内容。
# 结果：成功修改 bytearray 的内容
my_array = bytearray(b'hello')
my_array[0] = 0x79
print(my_array)


# 示例 10
# 目的：使用 memoryview 修改 bytearray
# 解释：创建一个 memoryview 并修改其内容。
# 结果：成功修改 bytearray 的内容
my_array = bytearray(b'row, row, row your boat')
my_view = memoryview(my_array)
write_view = my_view[3:13]
write_view[:] = b'-10 bytes-'
print(my_array)


# 示例 11
# 目的：使用 memoryview 修改视频缓存
# 解释：创建一个 memoryview 并修改视频缓存的内容。
# 结果：成功修改视频缓存的内容
video_array = bytearray(video_cache)
write_view = memoryview(video_array)
chunk = write_view[byte_offset:byte_offset + size]
socket.recv_into(chunk)


# 示例 12
# 目的：基准测试 memoryview 修改视频缓存
# 解释：定义一个函数，基准测试使用 memoryview 修改视频缓存的性能。
# 结果：打印基准测试结果
def run_test():
    """
    目的：基准测试 memoryview 修改视频缓存
    解释：定义一个函数，基准测试使用 memoryview 修改视频缓存的性能。
    结果：打印基准测试结果
    """
    chunk = write_view[byte_offset:byte_offset + size]
    socket.recv_into(chunk)

result = timeit.timeit(
    stmt='run_test()',
    globals=globals(),
    number=100) / 100

print(f'{result:0.9f} seconds')
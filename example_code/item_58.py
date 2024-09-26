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
# 目的：定义一个类 ClosableQueue
# 解释：继承自 Queue 并添加关闭和迭代功能。
# 结果：类 ClosableQueue
from queue import Queue

class ClosableQueue(Queue):
    SENTINEL = object()

    def close(self):
        """
        目的：关闭队列
        解释：向队列中放入一个哨兵对象，表示队列关闭。
        """
        self.put(self.SENTINEL)

    def __iter__(self):
        """
        目的：迭代队列
        解释：迭代队列中的元素，直到遇到哨兵对象。
        """
        while True:
            item = self.get()
            try:
                if item is self.SENTINEL:
                    return
                yield item
            finally:
                self.task_done()

in_queue = ClosableQueue()
out_queue = ClosableQueue()


# Example 2
# 目的：定义一个类 StoppableWorker
# 解释：继承自 Thread 并添加处理函数和队列。
# 结果：类 StoppableWorker
from threading import Thread

class StoppableWorker(Thread):
    def __init__(self, func, in_queue, out_queue, **kwargs):
        """
        目的：初始化 StoppableWorker 类
        解释：初始化线程，设置处理函数和队列。
        """
        super().__init__(**kwargs)
        self.func = func
        self.in_queue = in_queue
        self.out_queue = out_queue
        self.daemon = True

    def run(self):
        """
        目的：运行线程
        解释：从输入队列中获取任务，处理后放入输出队列。
        """
        for item in self.in_queue:
            result = self.func(item)
            self.out_queue.put(result)

def game_logic(state, neighbors):
    """
    目的：确定下一个状态并处理 I/O
    解释：根据当前状态和邻居数量决定下一个状态，并处理阻塞 I/O。
    """
    data = my_socket.recv(100)
    if state == ALIVE:
        if neighbors < 2 or neighbors > 3:
            return EMPTY
    else:
        if neighbors == 3:
            return ALIVE
    return state

def game_logic_thread(item):
    """
    目的：处理游戏逻辑线程
    解释：处理单个网格单元的状态和邻居数量。
    """
    y, x, state, neighbors = item
    try:
        next_state = game_logic(state, neighbors)
    except Exception as e:
        next_state = e
    return (y, x, next_state)

# Start the threads upfront
threads = []
for _ in range(5):
    thread = StoppableWorker(game_logic_thread, in_queue, out_queue)
    thread.start()
    threads.append(thread)


# Example 3
# 目的：定义一个类 Grid 和一个异常类 SimulationError
# 解释：包含网格的初始化和设置方法，以及模拟错误的异常类。
# 结果：类 Grid 和类 SimulationError
ALIVE = '*'
EMPTY = '-'

class SimulationError(Exception):
    pass

class Grid:
    def __init__(self, height, width):
        """
        目的：初始化 Grid 类
        解释：设置网格的高度和宽度，并初始化网格。
        """
        self.height = height
        self.width = width
        self.grid = [[EMPTY for _ in range(width)] for _ in range(height)]

    def get(self, y, x):
        """
        目的：获取网格中的状态
        解释：返回指定位置的网格状态。
        """
        return self.grid[y % self.height][x % self.width]

    def set(self, y, x, state):
        """
        目的：设置网格中的状态
        解释：在指定位置设置网格的状态。
        """
        self.grid[y % self.height][x % self.width] = state

    def __str__(self):
        """
        目的：返回网格的字符串表示
        解释：将网格转换为字符串形式。
        """
        return '\n'.join(''.join(row) for row in self.grid)

def count_neighbors(y, x, get):
    """
    目的：计算邻居数量
    解释：计算指定位置的邻居数量。
    """
    n_ = get(y - 1, x + 0)  # North
    ne = get(y - 1, x + 1)  # Northeast
    e_ = get(y + 0, x + 1)  # East
    se = get(y + 1, x + 1)  # Southeast
    s_ = get(y + 1, x + 0)  # South
    sw = get(y + 1, x - 1)  # Southwest
    w_ = get(y + 0, x - 1)  # West
    nw = get(y - 1, x - 1)  # Northwest
    neighbor_states = [n_, ne, e_, se, s_, sw, w_, nw]
    count = 0
    for state in neighbor_states:
        if state == ALIVE:
            count += 1
    return count

def simulate_pipeline(grid, in_queue, out_queue):
    """
    目的：模拟网格的下一步状态
    解释：使用管道模拟整个网格的下一步状态。
    """
    for y in range(grid.height):
        for x in range(grid.width):
            state = grid.get(y, x)
            neighbors = count_neighbors(y, x, grid.get)
            in_queue.put((y, x, state, neighbors))

    in_queue.join()
    out_queue.close()

    next_grid = Grid(grid.height, grid.width)
    for item in out_queue:  # Fan in
        y, x, state = item
        next_grid.set(y, x, state)

    return next_grid


# Example 4
# 目的：测试 game_logic 函数的 I/O 异常
# 解释：使用 contextlib.redirect_stderr 捕获异常输出。
# 结果：捕获到异常输出
try:
    def game_logic(state, neighbors):
        """
        目的：确定下一个状态并处理 I/O
        解释：根据当前状态和邻居数量决定下一个状态，并处理阻塞 I/O。
        """
        raise OSError('Problem with I/O')

    simulate_pipeline(Grid(1, 1), in_queue, out_queue)
except:
    logging.exception('Expected')
else:
    assert False


# Example 5
# 目的：清除 out_queue 中的哨兵对象并恢复 game_logic 函数
# 解释：清除 out_queue 中的哨兵对象，并恢复正常的 game_logic 函数。
# 结果：清除哨兵对象并恢复函数
# Clear the sentinel object from the out queue
for _ in out_queue:
    pass

# Restore the working version of this function
def game_logic(state, neighbors):
    """
    目的：确定下一个状态
    解释：根据当前状态和邻居数量决定下一个状态。
    """
    if state == ALIVE:
        if neighbors < 2 or neighbors > 3:
            return EMPTY
    else:
        if neighbors == 3:
            return ALIVE
    return state

class ColumnPrinter:
    def __init__(self):
        """
        目的：初始化 ColumnPrinter 类
        解释：初始化列存储。
        """
        self.columns = []

    def append(self, data):
        """
        目的：追加数据到列
        解释：将数据追加到列存储中。
        """
        self.columns.append(data)

    def __str__(self):
        """
        目的：返回列的字符串表示
        解释：将列转换为字符串形式。
        """
        rows = [' | '.join(row) for row in zip(*self.columns)]
        return '\n'.join(rows)

grid = Grid(5, 9)
grid.set(0, 3, ALIVE)
grid.set(1, 4, ALIVE)
grid.set(2, 2, ALIVE)
grid.set(2, 3, ALIVE)
grid.set(2, 4, ALIVE)

columns = ColumnPrinter()
for i in range(5):
    columns.append(str(grid))
    grid = simulate_pipeline(grid, in_queue, out_queue)

print(columns)

for thread in threads:
    in_queue.close()
for thread in threads:
    thread.join()


# Example 6
# 目的：定义一个函数 count_neighbors
# 解释：计算指定位置的邻居数量，并处理阻塞 I/O。
# 结果：函数 count_neighbors
def count_neighbors(y, x, get):
    """
    目的：计算邻居数量并处理 I/O
    解释：计算指定位置的邻居数量，并处理阻塞 I/O。
    """
    data = my_socket.recv(100)


# Example 7
# 目的：定义一个函数 count_neighbors
# 解释：计算指定位置的邻居数量。
# 结果：函数 count_neighbors
def count_neighbors(y, x, get):
    """
    目的：计算邻居数量
    解释：计算指定位置的邻居数量。
    """
    n_ = get(y - 1, x + 0)  # North
    ne = get(y - 1, x + 1)  # Northeast
    e_ = get(y + 0, x + 1)  # East
    se = get(y + 1, x + 1)  # Southeast
    s_ = get(y + 1, x + 0)  # South
    sw = get(y + 1, x - 1)  # Southwest
    w_ = get(y + 0, x - 1)  # West
    nw = get(y - 1, x - 1)  # Northwest
    neighbor_states = [n_, ne, e_, se, s_, sw, w_, nw]
    count = 0
    for state in neighbor_states:
        if state == ALIVE:
            count += 1
    return count

def count_neighbors_thread(item):
    """
    目的：处理邻居计数线程
    解释：处理单个网格单元的邻居计数。
    """
    y, x, state, get = item
    try:
        neighbors = count_neighbors(y, x, get)
    except Exception as e:
        neighbors = e
    return (y, x, state, neighbors)

def game_logic_thread(item):
    """
    目的：处理游戏逻辑线程
    解释：处理单个网格单元的状态和邻居数量。
    """
    y, x, state, neighbors = item
    if isinstance(neighbors, Exception):
        next_state = neighbors
    else:
        next_state = game_logic(state, neighbors)
    return (y, x, next_state)

from threading import Lock

class LockingGrid(Grid):
    def __init__(self, height, width):
        """
        目的：初始化 LockingGrid 类
        解释：继承自 Grid 并使用锁。
        """
        super().__init__(height, width)
        self.lock = Lock()

    def __str__(self):
        """
        目的：返回网格的字符串表示
        解释：将网格转换为字符串形式，并使用锁。
        """
        with self.lock:
            return super().__str__()

    def get(self, y, x):
        """
        目的：获取网格中的状态
        解释：返回指定位置的网格状态，并使用锁。
        """
        with self.lock:
            return super().get(y, x)

    def set(self, y, x, state):
        """
        目的：设置网格中的状态
        解释：在指定位置设置网格的状态，并使用锁。
        """
        with self.lock:
            super().set(y, x, state)


# Example 8
# 目的：初始化队列和线程
# 解释：初始化 ClosableQueue 和 StoppableWorker，并启动线程。
# 结果：队列和线程初始化成功
in_queue = ClosableQueue()
logic_queue = ClosableQueue()
out_queue = ClosableQueue()

threads = []

for _ in range(5):
    thread = StoppableWorker(count_neighbors_thread, in_queue, logic_queue)
    thread.start()
    threads.append(thread)

for _ in range(5):
    thread = StoppableWorker(game_logic_thread, logic_queue, out_queue)
    thread.start()
    threads.append(thread)


# Example 9
# 目的：定义一个函数 simulate_phased_pipeline
# 解释：使用分阶段管道模拟整个网格的下一步状态。
# 结果：函数 simulate_phased_pipeline
def simulate_phased_pipeline(grid, in_queue, logic_queue, out_queue):
    """
    目的：模拟网格的下一步状态
    解释：使用分阶段管道模拟整个网格的下一步状态。
    """
    for y in range(grid.height):
        for x in range(grid.width):
            state = grid.get(y, x)
            in_queue.put((y, x, state, grid.get))

    in_queue.join()
    logic_queue.join()  # Pipeline sequencing
    out_queue.close()

    next_grid = LockingGrid(grid.height, grid.width)
    for item in out_queue:  # Fan in
        y, x, state = item
        next_grid.set(y, x, state)

    return next_grid


# Example 10
# 目的：初始化网格并设置初始状态
# 解释：创建一个 LockingGrid 对象并设置一些初始状态。
# 结果：网格初始化成功
grid = LockingGrid(5, 9)
grid.set(0, 3, ALIVE)
grid.set(1, 4, ALIVE)
grid.set(2, 2, ALIVE)
grid.set(2, 3, ALIVE)
grid.set(2, 4, ALIVE)

columns = ColumnPrinter()
for i in range(5):
    columns.append(str(grid))
    grid = simulate_phased_pipeline(grid, in_queue, logic_queue, out_queue)

print(columns)

for thread in threads:
    in_queue.close()
for thread in threads:
    logic_queue.close()
for thread in threads:
    thread.join()


# Example 11
# 目的：确保异常传播按预期工作
# 解释：定义一个函数 count_neighbors 并抛出异常，测试异常传播。
# 结果：捕获到异常
# Make sure exception propagation works as expected
def count_neighbors(*args):
    """
    目的：计算邻居数量并处理 I/O
    解释：计算指定位置的邻居数量，并处理阻塞 I/O。
    """
    raise OSError('Problem with I/O in count_neighbors')

in_queue = ClosableQueue()
logic_queue = ClosableQueue()
out_queue = ClosableQueue()

threads = [
    StoppableWorker(count_neighbors_thread, in_queue, logic_queue),
    StoppableWorker(game_logic_thread, logic_queue, out_queue, daemon=True),
]

for thread in threads:
    thread.start()

try:
    simulate_phased_pipeline(grid, in_queue, logic_queue, out_queue)
except SimulationError:
    pass  # Expected
else:
    assert False
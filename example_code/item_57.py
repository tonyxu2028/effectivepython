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
# 目的：定义一个类 Grid
# 解释：包含网格的初始化和设置方法。
# 结果：类 Grid
from threading import Lock

ALIVE = '*'
EMPTY = '-'

class Grid:
    def __init__(self, height, width):
        """
        目的：初始化 Grid 类
        解释：设置网格的高度和宽度，并初始化网格。
        """
        self.height = height
        self.width = width
        self.rows = []
        for _ in range(self.height):
            self.rows.append([EMPTY] * self.width)

    def get(self, y, x):
        """
        目的：获取网格中的状态
        解释：返回指定位置的网格状态。
        """
        return self.rows[y % self.height][x % self.width]

    def set(self, y, x, state):
        """
        目的：设置网格中的状态
        解释：在指定位置设置网格的状态。
        """
        self.rows[y % self.height][x % self.width] = state

    def __str__(self):
        """
        目的：返回网格的字符串表示
        解释：将网格转换为字符串形式。
        """
        output = ''
        for row in self.rows:
            output += ''.join(row) + '\n'
        return output

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


# Example 2
# 目的：定义一些函数来处理网格状态
# 解释：定义 count_neighbors, game_logic, step_cell 和 simulate_threaded 函数。
# 结果：函数定义
from threading import Thread

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

def game_logic(state, neighbors):
    """
    目的：确定下一个状态
    解释：根据当前状态和邻居数量决定下一个状态。
    """
    if state == ALIVE:
        if neighbors < 2:
            return EMPTY
        elif neighbors > 3:
            return EMPTY
    else:
        if neighbors == 3:
            return ALIVE
    return state

def step_cell(y, x, get, set):
    """
    目的：计算并更新单个细胞的状态
    解释：计算单个细胞的下一个状态并更新。
    """
    state = get(y, x)
    neighbors = count_neighbors(y, x, get)
    next_state = game_logic(state, neighbors)
    set(y, x, next_state)

def simulate_threaded(grid):
    """
    目的：模拟网格的下一步状态
    解释：使用多线程模拟整个网格的下一步状态。
    """
    next_grid = LockingGrid(grid.height, grid.width)

    threads = []
    for y in range(grid.height):
        for x in range(grid.width):
            thread = Thread(target=step_cell, args=(y, x, grid.get, next_grid.set))
            threads.append(thread)
            thread.start()

    for thread in threads:
        thread.join()

    return next_grid


# Example 3
# 目的：定义一个类 ColumnPrinter
# 解释：用于打印多列数据。
# 结果：类 ColumnPrinter
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
        row_count = 1
        for data in self.columns:
            row_count = max(row_count, len(data.split('\n')))

        rows = [''] * row_count
        for data in self.columns:
            lines = data.split('\n')
            for i in range(row_count):
                if i < len(lines):
                    rows[i] += lines[i]
                rows[i] += ' | '

        return '\n'.join(rows)

grid = LockingGrid(5, 9)
grid.set(0, 3, ALIVE)
grid.set(1, 4, ALIVE)
grid.set(2, 2, ALIVE)
grid.set(2, 3, ALIVE)
grid.set(2, 4, ALIVE)

columns = ColumnPrinter()
for i in range(5):
    columns.append(str(grid))
    grid = simulate_threaded(grid)

print(columns)


# Example 4
# 目的：定义一个函数 game_logic
# 解释：包含阻塞输入/输出的逻辑。
# 结果：函数 game_logic
def game_logic(state, neighbors):
    """
    目的：确定下一个状态并处理 I/O
    解释：根据当前状态和邻居数量决定下一个状态，并处理阻塞 I/O。
    """
    raise OSError('Problem with I/O')


# Example 5
# 目的：测试 game_logic 函数的 I/O 异常
# 解释：使用 contextlib.redirect_stderr 捕获异常输出。
# 结果：捕获到异常输出
import contextlib
import io

fake_stderr = io.StringIO()
with contextlib.redirect_stderr(fake_stderr):
    thread = Thread(target=game_logic, args=(ALIVE, 3))
    thread.start()
    thread.join()

print(fake_stderr.getvalue())
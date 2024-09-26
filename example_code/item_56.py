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
        self.grid = [[EMPTY for _ in range(width)] for _ in range(height)]

    def set(self, y, x, state):
        """
        目的：设置网格中的状态
        解释：在指定位置设置网格的状态。
        """
        self.grid[y][x] = state

    def get(self, y, x):
        """
        目的：获取网格中的状态
        解释：返回指定位置的网格状态。
        """
        return self.grid[y][x]

    def __str__(self):
        """
        目的：返回网格的字符串表示
        解释：将网格转换为字符串形式。
        """
        return '\n'.join(''.join(row) for row in self.grid)


# Example 2
# 目的：初始化网格并设置初始状态
# 解释：创建一个 Grid 对象并设置一些初始状态。
# 结果：网格初始化成功
grid = Grid(5, 9)
grid.set(0, 3, ALIVE)
grid.set(1, 4, ALIVE)
grid.set(2, 2, ALIVE)
grid.set(2, 3, ALIVE)
grid.set(2, 4, ALIVE)
print(grid)


# Example 3
# 目的：定义一个函数 count_neighbors
# 解释：计算指定位置的邻居数量。
# 结果：函数 count_neighbors
def count_neighbors(y, x, get):
    """
    目的：计算邻居数量
    解释：计算指定位置的邻居数量。
    """
    n = 0
    for i in range(y - 1, y + 2):
        for j in range(x - 1, x + 2):
            if (i == y and j == x) or i < 0 or j < 0:
                continue
            try:
                if get(i, j) == ALIVE:
                    n += 1
            except IndexError:
                continue
    return n

alive = {(9, 5), (9, 6)}
seen = set()

def fake_get(y, x):
    """
    目的：模拟获取网格状态
    解释：返回指定位置的模拟网格状态。
    """
    seen.add((y, x))
    return ALIVE if (y, x) in alive else EMPTY

count = count_neighbors(10, 5, fake_get)
assert count == 2

expected_seen = {
    (9, 4), (9, 5), (9, 6), (10, 4), (10, 6), (11, 4), (11, 5), (11, 6)
}
assert seen == expected_seen


# Example 4
# 目的：定义一个函数 game_logic
# 解释：根据当前状态和邻居数量决定下一个状态。
# 结果：函数 game_logic
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

assert game_logic(ALIVE, 0) == EMPTY
assert game_logic(ALIVE, 1) == EMPTY
assert game_logic(ALIVE, 2) == ALIVE
assert game_logic(ALIVE, 3) == ALIVE
assert game_logic(ALIVE, 4) == EMPTY
assert game_logic(EMPTY, 0) == EMPTY
assert game_logic(EMPTY, 1) == EMPTY
assert game_logic(EMPTY, 2) == EMPTY
assert game_logic(EMPTY, 3) == ALIVE
assert game_logic(EMPTY, 4) == EMPTY


# Example 5
# 目的：定义一个函数 step_cell
# 解释：计算单个细胞的下一个状态并更新。
# 结果：函数 step_cell
def step_cell(y, x, get, set):
    """
    目的：计算并更新单个细胞的状态
    解释：计算单个细胞的下一个状态并更新。
    """
    state = get(y, x)
    neighbors = count_neighbors(y, x, get)
    next_state = game_logic(state, neighbors)
    set(y, x, next_state)

alive = {(10, 5), (9, 5), (9, 6)}
new_state = None

def fake_get(y, x):
    """
    目的：模拟获取网格状态
    解释：返回指定位置的模拟网格状态。
    """
    return ALIVE if (y, x) in alive else EMPTY

def fake_set(y, x, state):
    """
    目的：模拟设置网格状态
    解释：在指定位置设置模拟网格状态。
    """
    global new_state
    new_state = state

# Stay alive
step_cell(10, 5, fake_get, fake_set)
assert new_state == ALIVE

# Stay dead
alive.remove((10, 5))
step_cell(10, 5, fake_get, fake_set)
assert new_state == EMPTY

# Regenerate
alive.add((10, 6))
step_cell(10, 5, fake_get, fake_set)
assert new_state == ALIVE


# Example 6
# 目的：定义一个函数 simulate
# 解释：模拟整个网格的下一步状态。
# 结果：函数 simulate
def simulate(grid):
    """
    目的：模拟网格的下一步状态
    解释：模拟整个网格的下一步状态。
    """
    next_grid = Grid(grid.height, grid.width)
    for y in range(grid.height):
        for x in range(grid.width):
            step_cell(y, x, grid.get, next_grid.set)
    return next_grid


# Example 7
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
        rows = [' | '.join(row) for row in zip(*self.columns)]
        return '\n'.join(rows)

columns = ColumnPrinter()
for i in range(5):
    columns.append(str(grid).split('\n'))
    grid = simulate(grid)

print(columns)


# Example 8
# 目的：定义一个函数 game_logic
# 解释：包含阻塞输入/输出的逻辑。
# 结果：函数 game_logic
def game_logic(state, neighbors):
    """
    目的：确定下一个状态并处理 I/O
    解释：根据当前状态和邻居数量决定下一个状态，并处理阻塞 I/O。
    """
    # Do some blocking input/output in here:
    data = my_socket.recv(100)
    if state == ALIVE:
        if neighbors < 2 or neighbors > 3:
            return EMPTY
    else:
        if neighbors == 3:
            return ALIVE
    return state
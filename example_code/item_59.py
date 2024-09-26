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
    解释：遍历所有对象，找到所有打开的文件并关闭它们。
    结果：所有打开的文件都被关闭
    """
    everything = gc.get_objects()
    for obj in everything:
        if isinstance(obj, io.IOBase):
            obj.close()

atexit.register(close_open_files)


# 示例 1
# 目的：定义一个网格类 Grid
# 解释：初始化网格的高度和宽度，并提供获取和设置网格状态的方法。
# 结果：类 Grid
ALIVE = '*'
EMPTY = '-'

class Grid:
    def __init__(self, height, width):
        """
        目的：初始化 Grid 类
        解释：设置网格的高度和宽度，并初始化网格。
        结果：Grid 对象被创建
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
        结果：返回网格状态
        """
        return self.rows[y % self.height][x % self.width]

    def set(self, y, x, state):
        """
        目的：设置网格中的状态
        解释：在指定位置设置网格的状态。
        结果：网格状态被设置
        """
        self.rows[y % self.height][x % self.width] = state

    def __str__(self):
        """
        目的：返回网格的字符串表示
        解释：将网格转换为字符串形式。
        结果：返回网格的字符串表示
        """
        output = ''
        for row in self.rows:
            for cell in row:
                output += cell
            output += '\n'
        return output

from threading import Lock

class LockingGrid(Grid):
    """
    目的：定义一个带锁的网格类 LockingGrid
    解释：继承自 Grid 并使用锁来确保线程安全。
    结果：类 LockingGrid
    """
    def __init__(self, height, width):
        """
        目的：初始化 LockingGrid 类
        解释：继承自 Grid 并使用锁。
        结果：LockingGrid 对象被创建
        """
        super().__init__(height, width)
        self.lock = Lock()

    def __str__(self):
        """
        目的：返回网格的字符串表示
        解释：将网格转换为字符串形式，并使用锁。
        结果：返回网格的字符串表示
        """
        with self.lock:
            return super().__str__()

    def get(self, y, x):
        """
        目的：获取网格中的状态
        解释：返回指定位置的网格状态，并使用锁。
        结果：返回网格状态
        """
        with self.lock:
            return super().get(y, x)

    def set(self, y, x, state):
        """
        目的：设置网格中的状态
        解释：在指定位置设置网格的状态，并使用锁。
        结果：网格状态被设置
        """
        with self.lock:
            super().set(y, x, state)

def count_neighbors(y, x, get):
    """
    目的：计算邻居数量
    解释：计算指定位置的邻居数量。
    结果：返回邻居数量
    """
    n_ = get(y - 1, x + 0)  # 北
    ne = get(y - 1, x + 1)  # 东北
    e_ = get(y + 0, x + 1)  # 东
    se = get(y + 1, x + 1)  # 东南
    s_ = get(y + 1, x + 0)  # 南
    sw = get(y + 1, x - 1)  # 西南
    w_ = get(y + 0, x - 1)  # 西
    nw = get(y - 1, x - 1)  # 西北
    neighbor_states = [n_, ne, e_, se, s_, sw, w_, nw]
    count = 0
    for state in neighbor_states:
        if state == ALIVE:
            count += 1
    return count

def game_logic(state, neighbors):
    """
    目的：确定下一个状态并处理 I/O
    解释：根据当前状态和邻居数量决定下一个状态，并处理阻塞 I/O。
    结果：返回下一个状态
    """
    data = my_socket.recv(100)

def game_logic(state, neighbors):
    """
    目的：确定下一个状态
    解释：根据当前状态和邻居数量决定下一个状态。
    结果：返回下一个状态
    """
    if state == ALIVE:
        if neighbors < 2:
            return EMPTY     # 死亡：太少
        elif neighbors > 3:
            return EMPTY     # 死亡：太多
    else:
        if neighbors == 3:
            return ALIVE     # 复活
    return state

def step_cell(y, x, get, set):
    """
    目的：处理单个网格单元的状态
    解释：获取当前状态和邻居数量，并设置下一个状态。
    结果：网格单元状态被更新
    """
    state = get(y, x)
    neighbors = count_neighbors(y, x, get)
    next_state = game_logic(state, neighbors)
    set(y, x, next_state)


# 示例 2
# 目的：使用线程池模拟网格的下一步状态
# 解释：使用线程池并行处理网格的每个单元，计算下一步状态。
# 结果：网格的下一步状态被计算
from concurrent.futures import ThreadPoolExecutor

def simulate_pool(pool, grid):
    """
    目的：使用线程池模拟网格的下一步状态
    解释：使用线程池并行处理网格的每个单元，计算下一步状态。
    结果：返回新的网格状态
    """
    next_grid = LockingGrid(grid.height, grid.width)

    futures = []
    for y in range(grid.height):
        for x in range(grid.width):
            args = (y, x, grid.get, next_grid.set)
            future = pool.submit(step_cell, *args)  # 扇出
            futures.append(future)

    for future in futures:
        future.result()                             # 扇入

    return next_grid


# 示例 3
# 目的：定义一个列打印类 ColumnPrinter
# 解释：初始化列存储，并提供添加和字符串表示的方法。
# 结果：类 ColumnPrinter
class ColumnPrinter:
    def __init__(self):
        """
        目的：初始化 ColumnPrinter 类
        解释：初始化列存储。
        结果：ColumnPrinter 对象被创建
        """
        self.columns = []

    def append(self, data):
        """
        目的：将数据添加到列中
        解释：将数据添加到列存储中。
        结果：数据被添加到列中
        """
        self.columns.append(data)

    def __str__(self):
        """
        目的：返回列的字符串表示
        解释：将列转换为字符串形式。
        结果：返回列的字符串表示
        """
        row_count = 1
        for data in self.columns:
            row_count = max(
                row_count, len(data.splitlines()) + 1)

        rows = [''] * row_count
        for j in range(row_count):
            for i, data in enumerate(self.columns):
                line = data.splitlines()[max(0, j - 1)]
                if j == 0:
                    padding = ' ' * (len(line) // 2)
                    rows[j] += padding + str(i) + padding
                else:
                    rows[j] += line

                if (i + 1) < len(self.columns):
                    rows[j] += ' | '

        return '\n'.join(rows)

grid = LockingGrid(5, 9)
grid.set(0, 3, ALIVE)
grid.set(1, 4, ALIVE)
grid.set(2, 2, ALIVE)
grid.set(2, 3, ALIVE)
grid.set(2, 4, ALIVE)

columns = ColumnPrinter()
with ThreadPoolExecutor(max_workers=10) as pool:
    for i in range(5):
        columns.append(str(grid))
        grid = simulate_pool(pool, grid)

print(columns)


# 示例 4
# 目的：测试 game_logic 函数中的 I/O 异常
# 解释：使用 contextlib.redirect_stderr 捕获异常输出。
# 结果：捕获到异常输出
try:
    def game_logic(state, neighbors):
        """
        目的：确定下一个状态并处理 I/O
        解释：抛出 I/O 异常以测试异常处理。
        结果：抛出 I/O 异常
        """
        raise OSError('Problem with I/O')

    with ThreadPoolExecutor(max_workers=10) as pool:
        task = pool.submit(game_logic, ALIVE, 3)
        task.result()
except:
    logging.exception('Expected')
else:
    assert False
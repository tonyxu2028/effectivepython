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
# 目的：定义一个游戏状态类
# 解释：创建一个包含关卡和生命数的游戏状态类。
# 结果：GameState 类
class GameState:
    def __init__(self):
        self.level = 0
        self.lives = 4


# 示例 2
# 目的：修改游戏状态
# 解释：增加关卡数并减少生命数。
# 结果：打印修改后的游戏状态
state = GameState()
state.level += 1  # 玩家通过了一关
state.lives -= 1  # 玩家重试了一次

print(state.__dict__)


# 示例 3
# 目的：序列化游戏状态
# 解释：使用 pickle 将游戏状态保存到文件中。
# 结果：游戏状态被保存到文件
import pickle

state_path = 'game_state.bin'
with open(state_path, 'wb') as f:
    pickle.dump(state, f)


# 示例 4
# 目的：反序列化游戏状态
# 解释：从文件中加载游戏状态。
# 结果：打印加载后的游戏状态
with open(state_path, 'rb') as f:
    state_after = pickle.load(f)

print(state_after.__dict__)


# 示例 5
# 目的：更新游戏状态类
# 解释：在 GameState 类中添加新的字段 points。
# 结果：GameState 类包含新的字段
class GameState:
    def __init__(self):
        self.level = 0
        self.lives = 4
        self.points = 0  # 新字段


# 示例 6
# 目的：序列化和反序列化更新后的游戏状态
# 解释：使用 pickle 序列化和反序列化包含新字段的游戏状态。
# 结果：打印反序列化后的游戏状态
state = GameState()
serialized = pickle.dumps(state)
state_after = pickle.loads(serialized)
print(state_after.__dict__)


# 示例 7
# 目的：加载旧的游戏状态
# 解释：从文件中加载旧版本的游戏状态。
# 结果：打印加载后的游戏状态
with open(state_path, 'rb') as f:
    state_after = pickle.load(f)

print(state_after.__dict__)


# 示例 8
# 目的：验证加载的对象类型
# 解释：检查加载的对象是否是 GameState 类型。
# 结果：断言成功
assert isinstance(state_after, GameState)


# 示例 9
# 目的：更新游戏状态类的构造函数
# 解释：在 GameState 类的构造函数中添加默认参数。
# 结果：GameState 类包含新的构造函数
class GameState:
    def __init__(self, level=0, lives=4, points=0):
        self.level = level
        self.lives = lives
        self.points = points


# 示例 10
# 目的：定义游戏状态的序列化函数
# 解释：定义一个函数来序列化 GameState 对象。
# 结果：返回反序列化函数和参数
def pickle_game_state(game_state):
    """
    目的：定义游戏状态的序列化函数
    解释：定义一个函数来序列化 GameState 对象。
    结果：返回反序列化函数和参数
    """
    kwargs = game_state.__dict__
    return unpickle_game_state, (kwargs,)


# 示例 11
# 目的：定义游戏状态的反序列化函数
# 解释：定义一个函数来反序列化 GameState 对象。
# 结果：返回 GameState 对象
def unpickle_game_state(kwargs):
    """
    目的：定义游戏状态的反序列化函数
    解释：定义一个函数来反序列化 GameState 对象。
    结果：返回 GameState 对象
    """
    return GameState(**kwargs)


# 示例 12
# 目的：注册自定义的序列化和反序列化函数
# 解释：使用 copyreg 模块注册自定义的序列化和反序列化函数。
# 结果：自定义的序列化和反序列化函数被注册
import copyreg

copyreg.pickle(GameState, pickle_game_state)


# 示例 13
# 目的：测试自定义的序列化和反序列化函数
# 解释：使用自定义的序列化和反序列化函数保存和加载游戏状态。
# 结果：打印反序列化后的游戏状态
state = GameState()
state.points += 1000
serialized = pickle.dumps(state)
state_after = pickle.loads(serialized)
print(state_after.__dict__)


# 示例 14
# 目的：更新游戏状态类
# 解释：在 GameState 类中添加新的字段 magic。
# 结果：GameState 类包含新的字段
class GameState:
    def __init__(self, level=0, lives=4, points=0, magic=5):
        self.level = level
        self.lives = lives
        self.points = points
        self.magic = magic  # 新字段


# 示例 15
# 目的：测试反序列化旧的游戏状态
# 解释：尝试反序列化包含旧字段的游戏状态。
# 结果：打印反序列化前后的游戏状态
print('Before:', state.__dict__)
state_after = pickle.loads(serialized)
print('After: ', state_after.__dict__)


# 示例 16
# 目的：更新游戏状态类
# 解释：在 GameState 类中移除 lives 字段。
# 结果：GameState 类不再包含 lives 字段
class GameState:
    def __init__(self, level=0, points=0, magic=5):
        self.level = level
        self.points = points
        self.magic = magic


# 示例 17
# 目的：处理反序列化错误
# 解释：尝试反序列化包含旧字段的游戏状态并捕获异常。
# 结果：记录异常
try:
    pickle.loads(serialized)
except:
    logging.exception('预期的异常')
else:
    assert False


# 示例 18
# 目的：更新序列化函数
# 解释：在序列化函数中添加版本信息。
# 结果：返回包含版本信息的反序列化函数和参数
def pickle_game_state(game_state):
    """
    目的：更新序列化函数
    解释：在序列化函数中添加版本信息。
    结果：返回包含版本信息的反序列化函数和参数
    """
    kwargs = game_state.__dict__
    kwargs['version'] = 2
    return unpickle_game_state, (kwargs,)


# 示例 19
# 目的：更新反序列化函数
# 解释：在反序列化函数中处理不同版本的游戏状态。
# 结果：返回 GameState 对象
def unpickle_game_state(kwargs):
    """
    目的：更新反序列化函数
    解释：在反序列化函数中处理不同版本的游戏状态。
    结果：返回 GameState 对象
    """
    version = kwargs.pop('version', 1)
    if version == 1:
        del kwargs['lives']
    return GameState(**kwargs)


# 示例 20
# 目的：测试更新后的序列化和反序列化函数
# 解释：使用更新后的序列化和反序列化函数保存和加载游戏状态。
# 结果：打印反序列化前后的游戏状态
copyreg.pickle(GameState, pickle_game_state)
print('Before:', state.__dict__)
state_after = pickle.loads(serialized)
print('After: ', state_after.__dict__)


# 示例 21
# 目的：清除自定义的序列化和反序列化函数
# 解释：清除 copyreg 模块中的自定义序列化和反序列化函数。
# 结果：自定义的序列化和反序列化函数被清除
copyreg.dispatch_table.clear()
state = GameState()
serialized = pickle.dumps(state)
del GameState
class BetterGameState:
    def __init__(self, level=0, points=0, magic=5):
        self.level = level
        self.points = points
        self.magic = magic


# 示例 22
# 目的：处理反序列化错误
# 解释：尝试反序列化包含旧类的游戏状态并捕获异常。
# 结果：记录异常
try:
    pickle.loads(serialized)
except:
    logging.exception('预期的异常')
else:
    assert False


# 示例 23
# 目的：打印序列化后的数据
# 解释：打印序列化后的游戏状态数据。
# 结果：打印序列化后的数据
print(serialized)


# 示例 24
# 目的：注册新的序列化和反序列化函数
# 解释：使用 copyreg 模块注册新的序列化和反序列化函数。
# 结果：新的序列化和反序列化函数被注册
copyreg.pickle(BetterGameState, pickle_game_state)


# 示例 25
# 目的：测试新的序列化和反序列化函数
# 解释：使用新的序列化和反序列化函数保存和加载游戏状态。
# 结果：打印序列化后的数据
state = BetterGameState()
serialized = pickle.dumps(state)
print(serialized)
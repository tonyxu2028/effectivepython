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

# 目的：重现书籍中的环境，通过设置随机种子确保一致性
import random
random.seed(1234)

import logging
from pprint import pprint
from sys import stdout as STDOUT
import atexit
import gc
import io
import os
import tempfile

# 创建临时目录以存放输出
TEST_DIR = tempfile.TemporaryDirectory()
atexit.register(TEST_DIR.cleanup)

# 确保Windows进程能够正确退出
OLD_CWD = os.getcwd()
atexit.register(lambda: os.chdir(OLD_CWD))
os.chdir(TEST_DIR.name)

def close_open_files():
    """关闭所有打开的文件对象
    解释：遍历所有对象，检查是否为文件对象，如果是则关闭。
    结果：确保在程序结束时不会有打开的文件。
    """
    everything = gc.get_objects()
    for obj in everything:
        if isinstance(obj, io.IOBase):
            obj.close()

atexit.register(close_open_files)

# 自定义异常类
class EOFError(Exception):
    """自定义的EOF错误类
    解释：用于表示连接关闭的异常。
    结果：可用于在读取数据时捕获连接关闭的情况。
    """
    pass

# 基础连接类
class ConnectionBase:
    def __init__(self, connection):
        """初始化连接
        解释：保存连接对象并创建一个可读的文件对象。
        结果：为后续的数据发送和接收做好准备。
        """
        self.connection = connection
        self.file = connection.makefile('rb')

    def send(self, command):
        """发送命令到连接
        解释：将命令编码并通过连接发送。
        结果：服务器接收到指定的命令。
        """
        line = command + '\n'
        data = line.encode()
        self.connection.send(data)

    def receive(self):
        """从连接接收数据
        解释：读取一行数据，若连接关闭则抛出EOF错误。
        结果：返回接收到的字符串数据。
        """
        line = self.file.readline()
        if not line:
            raise EOFError('Connection closed')
        return line[:-1].decode()

# 自定义异常类
class UnknownCommandError(Exception):
    """未知命令错误类
    解释：用于处理未知命令的异常。
    结果：在接收到未定义命令时抛出该异常。
    """
    pass

# 会话管理类
class Session(ConnectionBase):
    def __init__(self, *args):
        """初始化会话
        解释：调用基类初始化并清除初始状态。
        结果：为新的游戏会话做好准备。
        """
        super().__init__(*args)
        self._clear_state(None, None)

    def _clear_state(self, lower, upper):
        """清除会话状态
        解释：重置猜测范围及相关变量。
        结果：开始新的游戏会话时状态清晰。
        """
        self.lower = lower
        self.upper = upper
        self.secret = None
        self.guesses = []

    def loop(self):
        """主循环处理接收命令
        解释：持续接收并处理命令，直到连接关闭。
        结果：根据命令执行相应的操作。
        """
        while command := self.receive():
            parts = command.split(' ')
            if parts[0] == 'PARAMS':
                self.set_params(parts)
            elif parts[0] == 'NUMBER':
                self.send_number()
            elif parts[0] == 'REPORT':
                self.receive_report(parts)
            else:
                raise UnknownCommandError(command)

    def set_params(self, parts):
        """设置参数
        解释：根据接收到的参数设置猜测范围。
        结果：更新会话状态以便进行猜测。
        """
        assert len(parts) == 3
        lower = int(parts[1])
        upper = int(parts[2])
        self._clear_state(lower, upper)

    def next_guess(self):
        """获取下一个猜测值
        解释：根据当前状态生成一个有效的猜测。
        结果：返回下一个未被猜测的值。
        """
        if self.secret is not None:
            return self.secret

        while True:
            guess = random.randint(self.lower, self.upper)
            if guess not in self.guesses:
                return guess

    def send_number(self):
        """发送猜测的数字
        解释：获取下一个猜测并发送给服务器。
        结果：服务器接收到最新的猜测。
        """
        guess = self.next_guess()
        self.guesses.append(guess)
        self.send(format(guess))

    def receive_report(self, parts):
        """接收报告
        解释：处理服务器返回的猜测结果。
        结果：根据反馈更新游戏状态。
        """
        assert len(parts) == 2
        decision = parts[1]

        last = self.guesses[-1]
        if decision == 'Correct':
            self.secret = last

        print(f'Server: {last} is {decision}')

# 客户端类
class Client(ConnectionBase):
    def __init__(self, *args):
        """初始化客户端
        解释：调用基类初始化并清除初始状态。
        结果：为客户端会话做好准备。
        """
        super().__init__(*args)
        self._clear_state()

    def _clear_state(self):
        """清除客户端状态
        解释：重置客户端状态相关变量。
        结果：开始新的客户端会话时状态清晰。
        """
        self.secret = None
        self.last_distance = None

    @contextlib.contextmanager
    def session(self, lower, upper, secret):
        """管理客户端会话
        解释：在会话开始前发送参数并在结束时清理状态。
        结果：确保会话期间状态的一致性。
        """
        print(f'Guess a number between {lower} and {upper}! Shhhhh, it\'s {secret}.')
        self.secret = secret
        self.send(f'PARAMS {lower} {upper}')
        try:
            yield
        finally:
            self._clear_state()
            self.send('PARAMS 0 -1')

    def request_numbers(self, count):
        """请求生成的数字
        解释：从服务器请求一组数字。
        结果：返回接收到的数字。
        """
        for _ in range(count):
            self.send('NUMBER')
            data = self.receive()
            yield int(data)
            if self.last_distance == 0:
                return

    def report_outcome(self, number):
        """报告结果
        解释：将猜测结果发送给服务器。
        结果：服务器记录了本次猜测的结果。
        """
        new_distance = abs(number - self.secret)
        decision = 'Unsure'

        if new_distance == 0:
            decision = 'Correct'
        elif self.last_distance is None:
            pass
        elif new_distance < self.last_distance:
            decision = 'Warmer'
        elif new_distance > self.last_distance:
            decision = 'Colder'

        self.last_distance = new_distance

        self.send(f'REPORT {decision}')
        return decision

# 服务器处理连接
def handle_connection(connection):
    """处理客户端连接
    解释：创建会话并处理循环，直到连接关闭。
    结果：为每个连接创建独立的会话。
    """
    with connection:
        session = Session(connection)
        try:
            session.loop()
        except EOFError:
            pass

def run_server(address):
    """运行服务器
    解释：创建套接字并监听客户端连接。
    结果：接受客户端连接并为每个连接启动新线程。
    """
    with socket.socket() as listener:
        listener.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
        listener.bind(address)
        listener.listen()
        while True:
            connection, _ = listener.accept()
            thread = Thread(target=handle_connection, args=(connection,), daemon=True)
            thread.start()

def run_client(address):
    """运行客户端
    解释：连接到服务器并执行会话。
    结果：返回所有猜测结果。
    """
    with socket.create_connection(address) as connection:
        client = Client(connection)

        with client.session(1, 5, 3):
            results = [(x, client.report_outcome(x)) for x in client.request_numbers(5)]

        with client.session(10, 15, 12):
            for number in client.request_numbers(5):
                outcome = client.report_outcome(number)
                results.append((number, outcome))

    return results


# Example 13
def main():
    """主函数：运行服务器并执行客户端操作
    解释：启动服务器线程并运行客户端，与服务器交互。
    结果：打印客户端的猜测结果。
    """
    address = ('127.0.0.1', 1234)
    server_thread = Thread(target=run_server, args=(address,), daemon=True)
    server_thread.start()

    results = run_client(address)
    for number, outcome in results:
        print(f'Client: {number} is {outcome}')

main()

# Example 14
class AsyncConnectionBase:
    def __init__(self, reader, writer):
        """初始化异步连接
        解释：保存读写流，以便进行异步通信。
        结果：为异步会话做好准备。
        """
        self.reader = reader
        self.writer = writer

    async def send(self, command):
        """异步发送命令
        解释：将命令编码并写入输出流。
        结果：通过连接发送命令。
        """
        line = command + '\n'
        data = line.encode()
        self.writer.write(data)
        await self.writer.drain()

    async def receive(self):
        """异步接收数据
        解释：从输入流读取一行数据。
        结果：返回接收到的字符串数据。
        """
        line = await self.reader.readline()
        if not line:
            raise EOFError('Connection closed')
        return line[:-1].decode()

# Example 15
class AsyncSession(AsyncConnectionBase):
    def __init__(self, *args):
        """初始化异步会话
        解释：调用基类初始化并清除初始状态。
        结果：为异步游戏会话做好准备。
        """
        super().__init__(*args)
        self._clear_values(None, None)

    def _clear_values(self, lower, upper):
        """清除会话值
        解释：重置猜测范围及相关变量。
        结果：开始新的游戏会话时状态清晰。
        """
        self.lower = lower
        self.upper = upper
        self.secret = None
        self.guesses = []

    async def loop(self):
        """异步主循环处理接收命令
        解释：持续接收并处理命令，直到连接关闭。
        结果：根据命令执行相应的操作。
        """
        while command := await self.receive():
            parts = command.split(' ')
            if parts[0] == 'PARAMS':
                self.set_params(parts)
            elif parts[0] == 'NUMBER':
                await self.send_number()
            elif parts[0] == 'REPORT':
                self.receive_report(parts)
            else:
                raise UnknownCommandError(command)

    def set_params(self, parts):
        """设置参数
        解释：根据接收到的参数设置猜测范围。
        结果：更新会话状态以便进行猜测。
        """
        assert len(parts) == 3
        lower = int(parts[1])
        upper = int(parts[2])
        self._clear_values(lower, upper)

    def next_guess(self):
        """获取下一个猜测值
        解释：根据当前状态生成一个有效的猜测。
        结果：返回下一个未被猜测的值。
        """
        if self.secret is not None:
            return self.secret

        while True:
            guess = random.randint(self.lower, self.upper)
            if guess not in self.guesses:
                return guess

    async def send_number(self):
        """异步发送猜测的数字
        解释：获取下一个猜测并发送给服务器。
        结果：服务器接收到最新的猜测。
        """
        guess = self.next_guess()
        self.guesses.append(guess)
        await self.send(format(guess))

    def receive_report(self, parts):
        """接收报告
        解释：处理服务器返回的猜测结果。
        结果：根据反馈更新游戏状态。
        """
        assert len(parts) == 2
        decision = parts[1]

        last = self.guesses[-1]
        if decision == CORRECT:
            self.secret = last

        print(f'Server: {last} is {decision}')

# Example 20
class AsyncClient(AsyncConnectionBase):
    def __init__(self, *args):
        """初始化异步客户端
        解释：调用基类初始化并清除初始状态。
        结果：为客户端会话做好准备。
        """
        super().__init__(*args)
        self._clear_state()

    def _clear_state(self):
        """清除客户端状态
        解释：重置客户端状态相关变量。
        结果：开始新的客户端会话时状态清晰。
        """
        self.secret = None
        self.last_distance = None

    @contextlib.asynccontextmanager
    async def session(self, lower, upper, secret):
        """管理客户端异步会话
        解释：在会话开始前发送参数并在结束时清理状态。
        结果：确保会话期间状态的一致性。
        """
        print(f'Guess a number between {lower} and {upper}! Shhhhh, it\'s {secret}.')
        self.secret = secret
        await self.send(f'PARAMS {lower} {upper}')
        try:
            yield
        finally:
            self._clear_state()
            await self.send('PARAMS 0 -1')

    async def request_numbers(self, count):
        """异步请求生成的数字
        解释：从服务器请求一组数字。
        结果：返回接收到的数字。
        """
        for _ in range(count):
            await self.send('NUMBER')
            data = await self.receive()
            yield int(data)
            if self.last_distance == 0:
                return

    async def report_outcome(self, number):
        """异步报告结果
        解释：将猜测结果发送给服务器。
        结果：服务器记录了本次猜测的结果。
        """
        new_distance = abs(number - self.secret)
        decision = UNSURE

        if new_distance == 0:
            decision = CORRECT
        elif self.last_distance is None:
            pass
        elif new_distance < self.last_distance:
            decision = WARMER
        elif new_distance > self.last_distance:
            decision = COLDER

        self.last_distance = new_distance

        await self.send(f'REPORT {decision}')
        # 确保输出顺序与线程版本一致
        await asyncio.sleep(0.01)
        return decision

# Example 24
import asyncio

async def handle_async_connection(reader, writer):
    """处理异步客户端连接
    解释：创建异步会话并处理循环，直到连接关闭。
    结果：为每个连接创建独立的会话。
    """
    session = AsyncSession(reader, writer)
    try:
        await session.loop()
    except EOFError:
        pass

async def run_async_server(address):
    """运行异步服务器
    解释：创建异步服务器并监听客户端连接。
    结果：接受客户端连接并处理请求。
    """
    server = await asyncio.start_server(handle_async_connection, *address)
    async with server:
        await server.serve_forever()

async def run_async_client(address):
    """运行异步客户端
    解释：连接到服务器并执行会话。
    结果：返回所有猜测结果。
    """
    # 等待服务器监听
    await asyncio.sleep(0.1)

    streams = await asyncio.open_connection(*address)  # 新
    client = AsyncClient(*streams)                     # 新

    async with client.session(1, 5, 3):
        results = [(x, await client.report_outcome(x))
                   async for x in client.request_numbers(5)]

    async with client.session(10, 15, 12):
        async for number in client.request_numbers(5):
            outcome = await client.report_outcome(number)
            results.append((number, outcome))

    _, writer = streams                                  # 新
    writer.close()                                       # 新
    await writer.wait_closed()                           # 新

    return results

# Example 26
async def main_async():
    """异步主函数：运行异步服务器并执行客户端操作
    解释：启动异步服务器并运行客户端，与服务器交互。
    结果：打印客户端的猜测结果。
    """
    address = ('127.0.0.1', 4321)

    server = run_async_server(address)
    asyncio.create_task(server)

    results = await run_async_client(address)
    for number, outcome in results:
        print(f'Client: {number} is {outcome}')

# 配置日志级别
logging.getLogger().setLevel(logging.ERROR)

# 启动异步事件循环
asyncio.run(main_async())

# 恢复日志级别
logging.getLogger().setLevel(logging.DEBUG)

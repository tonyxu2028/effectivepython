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

# 军规 52 : Use subprocess to Manage Child Processes
# 军规 52 ： subprocess 模块：Python 的 subprocess 模块用于创建和管理子进程，
# 允许我们在 Python 程序中执行其他系统命令或脚本，并与它们进行交互。
# 子进程是由当前 Python 程序派生出来的独立任务，subprocess
# 提供了控制子进程的创建、执行、输入输出管理等功能，使得在 Python 中执行外部命令更为灵活。

"""
解读:
(1)在某些场景下，我们需要调用系统命令或执行外部脚本。
例如，在处理自动化任务、批量文件管理或系统监控时，使用 subprocess 可以简化操作流程。
(2)subprocess 不仅支持创建子进程，还能通过 stdin、stdout 和 stderr 管理标准输入输出，
实现与子进程的数据交互。
(3)相比于早期的 os.system 或 os.popen，subprocess 模块更强大、灵活，提供了更安全的接口，
避免了 shell 注入等安全风险。

总结:
subprocess 模块提供了执行系统命令、创建子进程并与之交互的灵活方式。它提供了多种方法，包括 subprocess.run() 和 subprocess.Popen()，可以满足不同的任务需求。
对于简单的系统命令执行，subprocess.run() 是最佳选择。而 subprocess.Popen 更适合需要交互或异步管理的复杂任务。
使用 subprocess 时尽量避免 shell=True，以防止 shell 注入漏洞。
"""

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

import subprocess
# GPT --- Example
print(f"\n{'GPT---Example':*^50}")
# 使用 subprocess 运行系统命令
result = subprocess.run(
    ['echo', 'Hello, Shadow Master!'],
    capture_output=True,  # 捕获输出
    text=True  # 以字符串方式返回输出
)
# 读取子进程的标准输出
print("Output:", result.stdout)
# 读取子进程的标准错误输出
print("Error:", result.stderr)
# 返回值，0 表示成功
print("Return code:", result.returncode)

# 解释：subprocess.Popen 提供了更多细粒度控制，
# 通过 communicate() 发送数据到子进程的标准输入，
# 并读取输出和错误信息。
process = subprocess.Popen(
    ['python3', '-c', 'print(input("Enter your name: "))'],
    stdin=subprocess.PIPE,
    stdout=subprocess.PIPE,
    text=True
)
# 发送输入到子进程
output, error = process.communicate(input="Shadow Master\n")
print("Output:", output)
print("Error:", error)

# ============================================================================

# Example 1
# 目的：使用 subprocess 模块运行子进程
# 解释：使用 subprocess.run 方法运行子进程并捕获输出。
# 结果：子进程输出 "Hello from the child!"
print(f"\n{'Example 1':*^50}")
import subprocess

result = subprocess.run(
    ['echo', 'Hello from the child!'],
    capture_output=True,
    encoding='utf-8'
)
result.check_returncode()  # No exception means it exited cleanly
print(result.stdout)


# Example 2
# 目的：使用 subprocess 模块运行子进程
# 解释：使用 subprocess.Popen 方法运行子进程并轮询其状态。
# 结果：子进程状态轮询成功
print(f"\n{'Example 2':*^50}")
proc = subprocess.Popen(['sleep', '1'])
while proc.poll() is None:
    print('Working...')
    import time
    time.sleep(0.3)

print('Exit status', proc.poll())


# Example 3
# 目的：使用 subprocess 模块运行多个子进程
# 解释：使用 subprocess.Popen 方法运行多个子进程并记录开始时间。
# 结果：多个子进程运行成功
print(f"\n{'Example 3':*^50}")
import time

start = time.time()
sleep_procs = []
for _ in range(10):
    proc = subprocess.Popen(['sleep', '1'])
    sleep_procs.append(proc)


# Example 4
# 目的：等待所有子进程完成
# 解释：使用 subprocess.Popen.communicate 方法等待所有子进程完成。
# 结果：所有子进程完成
print(f"\n{'Example 4':*^50}")
for proc in sleep_procs:
    proc.communicate()

end = time.time()
delta = end - start
print(f'Finished in {delta:.3} seconds')


# Example 5
# 目的：使用 subprocess 模块运行加密子进程
# 解释：定义 run_encrypt 函数，使用 subprocess.Popen 方法运行加密子进程。
# 结果：加密子进程运行成功
print(f"\n{'Example 5':*^50}")
import os

def run_encrypt(data):
    env = os.environ.copy()
    env['password'] = 'zf7ShyBhZOraQDdE/FiZpm/m/8f9X+M1'
    proc = subprocess.Popen(
        ['openssl', 'enc', '-aes-256-cbc', '-pass', 'env:password'],
        env=env,
        stdin=subprocess.PIPE,
        stdout=subprocess.PIPE
    )
    proc.stdin.write(data)
    proc.stdin.flush()  # Ensure that the child gets input
    return proc

# Example 6
# 目的：运行多个加密子进程
# 解释：使用 run_encrypt 函数运行多个加密子进程。
# 结果：多个加密子进程运行成功
print(f"\n{'Example 6':*^50}")
procs = []
for _ in range(3):
    data = os.urandom(10)
    proc = run_encrypt(data)
    procs.append(proc)

# Example 7
# 目的：等待所有加密子进程完成
# 解释：使用 subprocess.Popen.communicate 方法等待所有加密子进程完成。
# 结果：所有加密子进程完成
print(f"\n{'Example 7':*^50}")
for proc in procs:
    out, _ = proc.communicate()
    print(out[-10:])

# Example 8
# 目的：定义 run_hash 函数
# 解释：定义 run_hash 函数，使用 subprocess.Popen 方法运行哈希子进程。
# 结果：哈希子进程运行成功
print(f"\n{'Example 8':*^50}")
def run_hash(input_stdin):
    return subprocess.Popen(
        ['openssl', 'dgst', '-sha256'],
        stdin=input_stdin,
        stdout=subprocess.PIPE
    )

# Example 9
# 目的：运行多个加密和哈希子进程
# 解释：使用 run_encrypt 和 run_hash 函数运行多个加密和哈希子进程。
# 结果：多个加密和哈希子进程运行成功
print(f"\n{'Example 9':*^50}")
encrypt_procs = []
hash_procs = []
for _ in range(3):
    data = os.urandom(100)

    encrypt_proc = run_encrypt(data)
    encrypt_procs.append(encrypt_proc)

    hash_proc = run_hash(encrypt_proc.stdout)
    hash_procs.append(hash_proc)

    encrypt_proc.stdout.close()
    encrypt_proc.stdout = None

# Example 10
# 目的：等待所有加密和哈希子进程完成
# 解释：使用 subprocess.Popen.communicate 方法等待所有加密和哈希子进程完成。
# 结果：所有加密和哈希子进程完成
print(f"\n{'Example 10':*^50}")
for proc in encrypt_procs:
    proc.communicate()
    assert proc.returncode == 0

for proc in hash_procs:
    out, _ = proc.communicate()
    print(out[-10:])
    assert proc.returncode == 0

# Example 11
# 目的：处理子进程超时
# 解释：使用 subprocess.Popen.communicate 方法处理子进程超时。
# 结果：子进程超时处理成功
print(f"\n{'Example 11':*^50}")
proc = subprocess.Popen(['sleep', '10'])
try:
    proc.communicate(timeout=0.1)
except subprocess.TimeoutExpired:
    proc.terminate()
    proc.wait()

print('Exit status', proc.poll())